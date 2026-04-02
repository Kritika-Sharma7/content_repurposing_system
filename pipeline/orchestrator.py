"""
Pipeline Orchestrator: Coordinates the multi-agent workflow.
Manages the flow: Summarizer -> Formatter -> Reviewer -> Refiner

UPGRADE v2: Constraint-Driven, Feedback Loop, Versioning
- Iterative feedback loop with configurable threshold (0.85)
- Normalized scores (0-1 range)
- Full version history tracking with diffs
- User preference integration
- Failure handling with retries
- Cross-format consistency checks
- Force iteration support
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from copy import deepcopy

from agents.summarizer import SummarizerAgent
from agents.formatter import FormatterAgent
from agents.reviewer import ReviewerAgent
from agents.refiner import RefinerAgent
from schemas.schemas import (
    SummaryOutput,
    FormattedOutput,
    ReviewOutput,
    RefinedOutput,
    PipelineResult,
    IterationResult,
    VersionEntry,
    VersionHistory,
    CrossFormatConsistency,
)
from utils.llm import LLMClient
from config.platform_config import PlatformConfig, DEFAULT_PLATFORM_CONFIG
from config.user_preferences import UserPreferences, DEFAULT_USER_PREFERENCES
from config.settings import SystemSettings, DEFAULT_SETTINGS, ScoringWeights


class PipelineOrchestrator:
    """
    Orchestrates the multi-agent content repurposing pipeline.

    Pipeline Flow:
    1. SummarizerAgent: Raw content -> Content DNA (with retry if key_points < 3)
    2. FormatterAgent: Summary -> Formatted content (V1) with platform constraints
    3. ReviewerAgent: Summary + V1 -> Multi-dimensional review with coverage analysis
    4. RefinerAgent: Summary + V1 + Review -> Refined content (targeted fixes only)
    5. Feedback Loop: While score < threshold and iterations < max: Review -> Refine

    Features:
    - Normalized scoring (0-1 scale)
    - Full version history with diffs
    - User preference integration
    - Platform constraint enforcement
    """

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        verbose: bool = True,
        settings: Optional[SystemSettings] = None,
        platform_config: Optional[PlatformConfig] = None,
    ):
        """
        Initialize the orchestrator with all agents.

        Args:
            llm_client: Optional shared LLM client for all agents
            verbose: Whether to print progress messages
            settings: System settings including thresholds and weights
            platform_config: Platform constraints configuration
        """
        self.verbose = verbose
        self.settings = settings or DEFAULT_SETTINGS
        self.platform_config = platform_config or DEFAULT_PLATFORM_CONFIG
        
        # Extract settings
        self.score_threshold = self.settings.feedback_loop.score_threshold
        self.max_iterations = self.settings.feedback_loop.max_iterations
        self.min_key_points = self.settings.feedback_loop.min_key_points
        self.scoring_weights = self.settings.scoring_weights

        # Initialize all agents
        self.summarizer = SummarizerAgent(
            llm_client,
            min_key_points=self.min_key_points,
            max_retries=self.settings.feedback_loop.max_summarizer_retries
        )
        self.formatter = FormatterAgent(llm_client, self.platform_config)
        self.reviewer = ReviewerAgent(llm_client, self.platform_config)
        self.refiner = RefinerAgent(llm_client, self.platform_config)

        # Storage for intermediate results
        self._summary: Optional[SummaryOutput] = None
        self._formatted_v1: Optional[FormattedOutput] = None
        self._review: Optional[ReviewOutput] = None
        self._refined: Optional[RefinedOutput] = None
        self._iterations: List[IterationResult] = []
        self._version_history: List[VersionEntry] = []

    def _log(self, message: str) -> None:
        """Print a log message if verbose mode is enabled."""
        if self.verbose:
            # Replace Unicode characters for Windows compatibility
            safe_message = message.replace("✓", "[OK]").replace("✗", "[FAIL]").replace("⚠️", "[WARN]").replace("ℹ️", "[INFO]")
            try:
                print(f"[Pipeline] {safe_message}")
            except UnicodeEncodeError:
                print(f"[Pipeline] {safe_message.encode('ascii', errors='replace').decode('ascii')}")

    def _compute_score(self, review: ReviewOutput) -> float:
        """
        Compute composite quality score from review using weighted dimensions.
        Returns normalized score (0-1 scale).
        """
        w = self.scoring_weights
        
        # Use normalized scores from review
        scores = review.scores
        
        # Compute weighted average
        composite = (
            w.clarity * scores.clarity +
            w.engagement * scores.engagement +
            w.coverage * scores.coverage +
            w.consistency * scores.consistency +
            w.platform_fit * (
                (scores.platform_fit.linkedin + 
                 scores.platform_fit.twitter + 
                 scores.platform_fit.newsletter) / 3
            )
        )
        
        # Fallback to legacy scores if normalized scores are 0
        if composite == 0:
            legacy_scores = [
                review.coverage_score / 10,
                review.clarity_score / 10,
                review.engagement_score / 10,
                review.consistency_score / 10,
                review.overall_alignment_score / 10,
            ]
            composite = sum(legacy_scores) / len(legacy_scores)
        
        return min(1.0, max(0.0, composite))

    def _add_version(
        self,
        version_id: str,
        content: FormattedOutput | RefinedOutput,
        score: float,
        changes: List[str] = None,
        parent: str = None,
        diff: Dict[str, Any] = None
    ) -> None:
        """Add a version to the history with optional diff tracking."""
        entry = VersionEntry(
            version=version_id,
            content=content.model_dump(),
            score=score,
            changes=changes or [],
            parent=parent,
            timestamp=datetime.now().isoformat()
        )
        # Store diff data if provided
        if diff:
            entry.content["_diff"] = diff
        self._version_history.append(entry)
    
    def _compute_diff(
        self,
        old_content: FormattedOutput | RefinedOutput,
        new_content: FormattedOutput | RefinedOutput
    ) -> Dict[str, Any]:
        """
        Compute detailed diff between two versions.
        Returns field-level changes for auditability.
        """
        diff = {"changes": []}
        
        # Compare LinkedIn
        if old_content.linkedin.hook != new_content.linkedin.hook:
            diff["changes"].append({
                "field": "linkedin.hook",
                "before": old_content.linkedin.hook[:100] + "..." if len(old_content.linkedin.hook) > 100 else old_content.linkedin.hook,
                "after": new_content.linkedin.hook[:100] + "..." if len(new_content.linkedin.hook) > 100 else new_content.linkedin.hook
            })
        
        if old_content.linkedin.body != new_content.linkedin.body:
            diff["changes"].append({
                "field": "linkedin.body",
                "before_len": len(old_content.linkedin.body),
                "after_len": len(new_content.linkedin.body),
                "changed": True
            })
        
        if old_content.linkedin.call_to_action != new_content.linkedin.call_to_action:
            diff["changes"].append({
                "field": "linkedin.cta",
                "before": old_content.linkedin.call_to_action,
                "after": new_content.linkedin.call_to_action
            })
        
        # Compare Twitter tweets
        old_tweets = old_content.twitter.tweets
        new_tweets = new_content.twitter.tweets
        
        if len(old_tweets) != len(new_tweets):
            diff["changes"].append({
                "field": "twitter.tweet_count",
                "before": len(old_tweets),
                "after": len(new_tweets)
            })
        
        for i, (old_t, new_t) in enumerate(zip(old_tweets, new_tweets)):
            if old_t != new_t:
                diff["changes"].append({
                    "field": f"twitter.tweets[{i}]",
                    "before": old_t[:80] + "..." if len(old_t) > 80 else old_t,
                    "after": new_t[:80] + "..." if len(new_t) > 80 else new_t
                })
        
        # Compare Newsletter
        if old_content.newsletter.subject_line != new_content.newsletter.subject_line:
            diff["changes"].append({
                "field": "newsletter.subject",
                "before": old_content.newsletter.subject_line,
                "after": new_content.newsletter.subject_line
            })
        
        if old_content.newsletter.intro != new_content.newsletter.intro:
            diff["changes"].append({
                "field": "newsletter.intro",
                "changed": True
            })
        
        old_sections = old_content.newsletter.body_sections
        new_sections = new_content.newsletter.body_sections
        
        if len(old_sections) != len(new_sections):
            diff["changes"].append({
                "field": "newsletter.section_count",
                "before": len(old_sections),
                "after": len(new_sections)
            })
        
        return diff
    
    def _check_cross_format_consistency(
        self,
        formatted: FormattedOutput,
        summary: SummaryOutput
    ) -> CrossFormatConsistency:
        """
        Check consistency of key point coverage across all platforms.
        Ensures same ideas are represented (or intentionally different).
        """
        kp_ids = [kp.id for kp in summary.key_points]
        
        # Get derived_from sets
        linkedin_kps = set(formatted.linkedin.derived_from or [])
        twitter_kps = set(formatted.twitter.derived_from or [])
        newsletter_kps = set(formatted.newsletter.derived_from or [])
        
        # Find missing in each format
        missing_in_linkedin = [kp for kp in kp_ids if kp not in linkedin_kps]
        missing_in_twitter = [kp for kp in kp_ids if kp not in twitter_kps]
        missing_in_newsletter = [kp for kp in kp_ids if kp not in newsletter_kps]
        
        # Build cross-format analysis
        # A key point is "missing_points" if it appears in some formats but not all
        all_used = linkedin_kps | twitter_kps | newsletter_kps
        missing_points = []
        
        for kp in all_used:
            missing_in = []
            if kp not in linkedin_kps:
                missing_in.append("linkedin")
            if kp not in twitter_kps:
                missing_in.append("twitter")
            if kp not in newsletter_kps:
                missing_in.append("newsletter")
            if missing_in:
                missing_points.append(f"{kp} missing in: {', '.join(missing_in)}")
        
        # Contradictions would require semantic analysis - placeholder
        contradictions = []
        
        # Tone mismatch detection (basic heuristic)
        tone_mismatch = []
        
        return CrossFormatConsistency(
            missing_points=missing_points,
            contradictions=contradictions,
            tone_mismatch=tone_mismatch,
            missing_in_linkedin=missing_in_linkedin,
            missing_in_twitter=missing_in_twitter,
            missing_in_newsletter=missing_in_newsletter
        )

    def run(
        self,
        content: str,
        user_preferences: Optional[UserPreferences] = None,
    ) -> PipelineResult:
        """
        Execute the full pipeline on input content.

        Args:
            content: Raw long-form text content to process
            user_preferences: Optional user preferences for customization

        Returns:
            PipelineResult containing all versions, iterations, and scores
        """
        prefs = user_preferences or DEFAULT_USER_PREFERENCES
        
        self._log("Starting content repurposing pipeline...")
        self._log(f"Input: {len(content.split())} words")
        self._log(f"Target platforms: {', '.join(prefs.platforms)}")
        self._log(f"Score threshold: {self.score_threshold:.2f}")

        # Reset state
        self._iterations = []
        self._version_history = []

        # Stage 1: Content DNA Extraction (with retry)
        self._log("Stage 1/4: Extracting Content DNA...")
        self._summary = self.summarizer.run(content, prefs)
        
        # Validate key_points
        is_valid, issues = self.summarizer.validate_output(self._summary)
        if not is_valid:
            self._log(f"  ⚠️ Validation issues: {issues}")
            if len(self._summary.key_points) < self.min_key_points:
                self._log(f"  ⚠️ Only {len(self._summary.key_points)} key_points (need {self.min_key_points})")
        
        self._log(f"  ✓ Extracted {len(self._summary.key_points)} key_points")
        self._log(f"  ✓ Intent: {self._summary.intent}, Tone: {self._summary.tone}")
        self._log(f"  ✓ Theme: {self._summary.main_theme}")

        # Stage 2: Platform-Aware Formatting (Version 1)
        self._log("Stage 2/4: Creating platform content (V1)...")
        self._formatted_v1 = self.formatter.run(self._summary, prefs, prefs.platforms)
        
        self._log(f"  ✓ LinkedIn: {len(self._formatted_v1.linkedin.body)} chars")
        self._log(f"  ✓ Twitter: {len(self._formatted_v1.twitter.tweets)} tweets")
        self._log(f"  ✓ Newsletter: {len(self._formatted_v1.newsletter.body_sections)} sections")

        # Stage 3: Multi-Dimensional Review
        self._log("Stage 3/4: Running multi-dimensional review...")
        self._review = self.reviewer.run(self._summary, self._formatted_v1)
        
        initial_score = self._compute_score(self._review)
        self._log(f"  ✓ Composite score: {initial_score:.2f} (threshold: {self.score_threshold:.2f})")
        self._log(f"  ✓ Coverage: {self._review.scores.coverage:.2f}")
        self._log(f"  ✓ Violations: {len(self._review.violations)}")
        self._log(f"  ✓ Issues: {len(self._review.issues)}")
        
        # Cross-format consistency check
        cross_format = self._check_cross_format_consistency(self._formatted_v1, self._summary)
        self._review.cross_format_consistency = cross_format
        if cross_format.missing_points:
            self._log(f"  ⚠️ Cross-format gaps: {len(cross_format.missing_points)}")
        else:
            self._log(f"  ✓ Cross-format consistency: OK")

        # Add V1 to version history
        self._add_version("v1", self._formatted_v1, initial_score)

        # Stage 4: Iterative Feedback Loop
        current_formatted = self._formatted_v1
        current_review = self._review
        current_score = initial_score
        iteration_count = 0
        threshold_met = current_score >= self.score_threshold
        
        # Check if force iteration is enabled
        force_iteration = getattr(self.settings.feedback_loop, 'force_at_least_one_iteration', False)
        should_iterate = not threshold_met or (force_iteration and iteration_count == 0)

        while iteration_count < self.max_iterations and should_iterate:
            iteration_count += 1
            self._log(f"\nStage 4: Refinement iteration {iteration_count}/{self.max_iterations}...")
            self._log(f"  Current score: {current_score:.2f} (need: {self.score_threshold:.2f})")
            if force_iteration and threshold_met:
                self._log(f"  ⚠️ Force iteration enabled - refining despite meeting threshold")

            # Run refiner with force_iteration flag
            self._refined = self.refiner.run(
                self._summary,
                current_formatted,
                current_review,
                force_iteration=(force_iteration and iteration_count == 1)
            )
            
            changes_summary = [
                f"{c.action} {c.target}: {c.change_type}"
                for c in self._refined.changes_applied[:3]
            ]
            self._log(f"  ✓ Changes applied: {len(self._refined.changes_applied)}")
            for change in changes_summary:
                self._log(f"    - {change}")

            # Review the refined version
            refined_as_formatted = FormattedOutput(
                version=self._refined.version,
                linkedin=self._refined.linkedin,
                twitter=self._refined.twitter,
                newsletter=self._refined.newsletter,
            )
            
            new_review = self.reviewer.run(self._summary, refined_as_formatted)
            new_score = self._compute_score(new_review)
            
            # Add cross-format check to new review
            new_cross_format = self._check_cross_format_consistency(refined_as_formatted, self._summary)
            new_review.cross_format_consistency = new_cross_format
            
            self._log(f"  ✓ New score: {new_score:.2f} (Δ {new_score - current_score:+.2f})")

            # Compute diff between versions
            diff = self._compute_diff(current_formatted, refined_as_formatted)

            # Record iteration
            iteration_result = IterationResult(
                iteration=iteration_count,
                review=current_review,
                refined=self._refined,
                score=new_score,
            )
            self._iterations.append(iteration_result)

            # Add to version history with diff
            self._add_version(
                f"v{iteration_count + 1}",
                self._refined,
                new_score,
                changes=[c.action + " " + c.target for c in self._refined.changes_applied],
                parent=f"v{iteration_count}",
                diff=diff
            )

            # Update for next iteration
            current_formatted = refined_as_formatted
            current_review = new_review
            current_score = new_score
            threshold_met = current_score >= self.score_threshold
            
            # Update should_iterate for next loop check
            should_iterate = not threshold_met

            if threshold_met:
                self._log(f"  ✓ Threshold met! Score {current_score:.2f} >= {self.score_threshold:.2f}")

        # Ensure we have a refined output
        if self._refined is None:
            # No refinement was needed, create a copy of v1
            self._log("  ℹ️ No refinement needed, V1 meets threshold")
            self._refined = RefinedOutput(
                version=2,
                linkedin=self._formatted_v1.linkedin,
                twitter=self._formatted_v1.twitter,
                newsletter=self._formatted_v1.newsletter,
                changes_applied=[],
                change_records=[],
                changes_made=["No changes needed - V1 met quality threshold"],
                addressed_issues=[]
            )

        final_score = current_score
        self._log(f"\n{'='*50}")
        self._log(f"Pipeline complete!")
        self._log(f"  Final score: {final_score:.2f}")
        self._log(f"  Iterations: {iteration_count}")
        self._log(f"  Threshold met: {threshold_met}")
        self._log(f"{'='*50}")

        # Assemble final result
        return PipelineResult(
            input_summary=self._summary,
            version_1=self._formatted_v1,
            review=current_review,
            version_2=self._refined,
            iterations=self._iterations,
            final_score=final_score,
            version_history=VersionHistory(
                versions=self._version_history,
                current_version=f"v{len(self._version_history)}"
            ),
            total_iterations=iteration_count,
            threshold_met=threshold_met
        )

    def save_results(
        self,
        result: PipelineResult,
        output_dir: str = "output",
    ) -> Path:
        """
        Save pipeline results to JSON files.

        Args:
            result: The complete pipeline result
            output_dir: Directory to save outputs

        Returns:
            Path to the output directory
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save complete result
        complete_file = output_path / f"pipeline_result_{timestamp}.json"
        with open(complete_file, "w", encoding="utf-8") as f:
            json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)

        # Save individual components for easy access
        (output_path / f"summary_{timestamp}.json").write_text(
            result.input_summary.model_dump_json(indent=2),
            encoding="utf-8",
        )
        (output_path / f"version_1_{timestamp}.json").write_text(
            result.version_1.model_dump_json(indent=2),
            encoding="utf-8",
        )
        (output_path / f"review_{timestamp}.json").write_text(
            result.review.model_dump_json(indent=2),
            encoding="utf-8",
        )
        (output_path / f"version_2_{timestamp}.json").write_text(
            result.version_2.model_dump_json(indent=2),
            encoding="utf-8",
        )
        
        # Save version history
        (output_path / f"versions_{timestamp}.json").write_text(
            result.version_history.model_dump_json(indent=2),
            encoding="utf-8",
        )
        
        # Save iterations log
        iterations_data = {
            "total_iterations": result.total_iterations,
            "threshold_met": result.threshold_met,
            "final_score": result.final_score,
            "iterations": [
                {
                    "iteration": it.iteration,
                    "score": it.score,
                    "changes": len(it.refined.changes_applied) if it.refined else 0
                }
                for it in result.iterations
            ]
        }
        (output_path / f"iterations_{timestamp}.json").write_text(
            json.dumps(iterations_data, indent=2),
            encoding="utf-8",
        )

        self._log(f"Results saved to: {output_path}")
        return output_path

    def _safe_print(self, *args, **kwargs) -> None:
        """Print with fallback for encoding issues on Windows."""
        try:
            print(*args, **kwargs)
        except UnicodeEncodeError:
            text = " ".join(str(a) for a in args)
            print(text.encode("ascii", errors="replace").decode("ascii"), **kwargs)

    def print_comparison(self, result: PipelineResult) -> None:
        """
        Print a side-by-side comparison of V1 vs final version with metrics.

        Args:
            result: The complete pipeline result
        """
        self._safe_print("\n" + "=" * 80)
        self._safe_print("CONTENT COMPARISON: VERSION 1 vs FINAL VERSION")
        self._safe_print("=" * 80)

        # Summary info
        self._safe_print(f"\n[CONTENT DNA]")
        self._safe_print(f"Title: {result.input_summary.title}")
        self._safe_print(f"Intent: {result.input_summary.intent}")
        self._safe_print(f"Tone: {result.input_summary.tone}")
        self._safe_print(f"Key Points: {len(result.input_summary.key_points)}")

        # LinkedIn comparison
        self._safe_print("\n[LINKEDIN POST]")
        self._safe_print("-" * 40)
        self._safe_print("V1 HOOK:", result.version_1.linkedin.hook[:80] + "...")
        self._safe_print("V2 HOOK:", result.version_2.linkedin.hook[:80] + "...")

        # Twitter comparison
        self._safe_print("\n[TWITTER THREAD]")
        self._safe_print("-" * 40)
        self._safe_print(f"V1: {len(result.version_1.twitter.tweets)} tweets")
        self._safe_print(f"V2: {len(result.version_2.twitter.tweets)} tweets")
        if result.version_1.twitter.tweets:
            self._safe_print("V1 First:", result.version_1.twitter.tweets[0][:70] + "...")
        if result.version_2.twitter.tweets:
            self._safe_print("V2 First:", result.version_2.twitter.tweets[0][:70] + "...")

        # Newsletter comparison
        self._safe_print("\n[NEWSLETTER]")
        self._safe_print("-" * 40)
        self._safe_print("V1 Subject:", result.version_1.newsletter.subject_line)
        self._safe_print("V2 Subject:", result.version_2.newsletter.subject_line)

        # Scores comparison
        self._safe_print("\n[SCORES]")
        self._safe_print("-" * 40)
        v1_score = self._version_history[0].score if self._version_history else 0
        self._safe_print(f"V1 Score: {v1_score:.2f}")
        self._safe_print(f"Final Score: {result.final_score:.2f}")
        self._safe_print(f"Improvement: {result.final_score - v1_score:+.2f}")

        # Changes summary
        self._safe_print("\n[REFINEMENT SUMMARY]")
        self._safe_print("-" * 40)
        self._safe_print(f"Iterations: {result.total_iterations}")
        self._safe_print(f"Threshold Met: {'Yes' if result.threshold_met else 'No'}")
        
        if result.version_2.changes_applied:
            self._safe_print("\nKey Changes:")
            for change in result.version_2.changes_applied[:5]:
                self._safe_print(f"  • {change.action} {change.target}: {change.change_type}")

        self._safe_print("\n" + "=" * 80)
