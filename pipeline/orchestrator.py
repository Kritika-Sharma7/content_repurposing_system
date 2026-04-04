"""
Pipeline Orchestrator: Coordinates the multi-agent workflow.

CLEAN DESIGN v6:
Flow: Summarizer -> Formatter -> [Reviewer <-> Refiner] loop -> Final Output
- True iterative feedback loop
- Stop conditions: no issues, no changes, max iterations
- Versioning: V1 -> V2 -> V3 -> ...
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Union, Dict

from agents.summarizer import SummarizerAgent
from agents.formatter import FormatterAgent
from agents.reviewer import ReviewerAgent
from agents.refiner import RefinerAgent
from schemas.schemas import (
    SummaryOutput, FormattedOutput, ReviewOutput, RefinedOutput,
    PipelineResult, IterationResult,
    LinkedInOutput, TwitterOutput, NewsletterOutput
)
from utils.llm import LLMClient
from config.user_preferences import UserPreferences, DEFAULT_USER_PREFERENCES


class PipelineOrchestrator:
    """
    Orchestrates the multi-agent content pipeline with iterative refinement.

    Flow:
    1. Summarizer: Raw content -> core_message + key_points
    2. Formatter: key_points -> platform content (V1)
    3. Feedback Loop:
       - Reviewer: Current version -> issues
       - Refiner: Current version + issues -> Next version
       - Repeat until: no issues, no changes, or max iterations
    """

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        verbose: bool = True,
        max_iterations: int = 5,
        settings: Optional[dict] = None,
        platform_config: Optional[dict] = None,
    ):
        self.verbose = verbose
        self.max_iterations = max_iterations
        
        # Initialize agents
        self.summarizer = SummarizerAgent(llm_client)
        self.formatter = FormatterAgent(llm_client)
        self.reviewer = ReviewerAgent(llm_client)
        self.refiner = RefinerAgent(llm_client)

    def _log(self, message: str) -> None:
        """Print log message if verbose."""
        if self.verbose:
            safe_msg = message.replace("✓", "[OK]").replace("✗", "[FAIL]")
            print(f"[Pipeline] {safe_msg}")

    def run(
        self,
        content: str,
        user_preferences: Optional[UserPreferences] = None,
    ) -> PipelineResult:
        """
        Execute the full pipeline with iterative refinement.

        Args:
            content: Raw text to process
            user_preferences: Optional user preferences

        Returns:
            PipelineResult with summary, v1, review, v2, iterations
        """
        prefs = user_preferences or DEFAULT_USER_PREFERENCES
        
        self._log("Starting pipeline...")
        self._log(f"Input: {len(content.split())} words")

        # Stage 1: Summarize
        self._log("Stage 1: Extracting key points...")
        summary = self.summarizer.run(content, prefs)
        self._log(f"  [OK] Extracted {len(summary.key_points)} key points")
        self._log(f"  Core: {summary.core_message[:60]}...")

        # Stage 2: Format (V1)
        self._log("Stage 2: Formatting for platforms...")
        v1 = self.formatter.run(summary, prefs, prefs.platforms)
        self._log(f"  [OK] LinkedIn: {len(v1.linkedin.content.split())} words")
        self._log(f"  [OK] Twitter: {len(v1.twitter.tweets)} tweets")
        self._log(f"  [OK] Newsletter: {len(v1.newsletter.content.split())} words")

        # Stage 3: Feedback Loop (Review <-> Refine)
        self._log("Stage 3: Feedback loop starting...")
        
        current_output: Union[FormattedOutput, RefinedOutput] = v1
        iterations: List[IterationResult] = []
        total_issues = 0
        total_fixed = 0
        
        # Initialize all version tracking
        all_reviews: Dict[int, ReviewOutput] = {}
        all_versions: Dict[int, Union[FormattedOutput, RefinedOutput]] = {1: v1}
        final_refined: Optional[RefinedOutput] = None
        
        # CRITICAL FIX #3: Track review history for stuck loop detection
        review_history: List[ReviewOutput] = []
        
        for iteration in range(1, self.max_iterations + 1):
            self._log(f"  --- Iteration {iteration}/{self.max_iterations} ---")
            
            # Review current output
            self._log(f"  Reviewing V{iteration}...")
            review = self.reviewer.run(summary, current_output)
            
            # Store all reviews
            all_reviews[iteration] = review
            review_history.append(review)
            
            issues_count = len(review.issues)
            total_issues += issues_count
            self._log(f"  [OK] Found {issues_count} issues (status: {review.status})")
            
            # CRITICAL FIX #3: Check for stuck loop
            is_stuck, stuck_issues = self._detect_stuck_loop(review_history)
            if is_stuck:
                self._log(f"  [WARN] Stuck loop detected: issues {stuck_issues} repeating across iterations")
                result_metadata = {
                    'termination_reason': 'stuck_loop',
                    'stuck_issues': list(stuck_issues)
                }
                # Create final result with stuck loop metadata
                return self._create_final_result(
                    summary, v1, all_versions, all_reviews, 
                    iterations, total_issues, total_fixed, result_metadata
                )
            
            # STOP CONDITION 1: No issues
            if review.status == "ok" or issues_count == 0:
                self._log(f"  [OK] No issues found - stopping loop")
                # Create unchanged output for final version if not already final
                if iteration < self.max_iterations:
                    final_refined = self._create_refined_from_current(current_output, iteration + 1)
                    all_versions[iteration + 1] = final_refined
                else:
                    final_refined = current_output if isinstance(current_output, RefinedOutput) else None
                
                iterations.append(IterationResult(
                    iteration=iteration,
                    review=review,
                    refined=None,
                    issues_fixed=0
                ))
                break
            
            # Refine based on review
            self._log(f"  Refining to V{iteration + 1}...")
            refined = self.refiner.run(summary, current_output, review)
            final_refined = refined
            
            # Store this version
            all_versions[iteration + 1] = refined
            
            changes_count = len(refined.changes)
            total_fixed += changes_count
            self._log(f"  [OK] Made {changes_count} changes")
            
            # Track iteration
            iterations.append(IterationResult(
                iteration=iteration,
                review=review,
                refined=refined,
                issues_fixed=changes_count
            ))
            
            # CRITICAL FIX #4: Check if refiner refused to fix issues
            if issues_count > 0 and changes_count == 0:
                self._log(f"  [WARN] Refiner unable to fix {issues_count} issues - stopping loop")
                result_metadata = {
                    'termination_reason': 'refiner_unable_to_fix',
                    'unfixable_issues': [issue.dict() for issue in review.issues]
                }
                return self._create_final_result(
                    summary, v1, all_versions, all_reviews,
                    iterations, total_issues, total_fixed, result_metadata
                )
            
            # STOP CONDITION 2: No changes made
            if changes_count == 0:
                self._log(f"  [WARN] No changes made - stopping loop")
                break
            
            # STOP CONDITION 3: Content unchanged (detect no-op refinement)
            if self._content_unchanged(current_output, refined):
                self._log(f"  [WARN] Content unchanged - stopping loop")
                break
            
            # Update current output for next iteration
            current_output = refined
            
            self._log(f"  V{iteration + 1} ready")

        # Ensure we have final outputs
        if final_refined is None:
            final_refined = self._create_refined_from_current(current_output, len(iterations) + 1)
        
        # Extract individual version data from tracked versions
        v2_data = all_versions.get(2) if isinstance(all_versions.get(2), RefinedOutput) else None
        v3_data = all_versions.get(3) if isinstance(all_versions.get(3), RefinedOutput) else None
        v4_data = all_versions.get(4) if isinstance(all_versions.get(4), RefinedOutput) else None
        v5_data = all_versions.get(5) if isinstance(all_versions.get(5), RefinedOutput) else None

        self._log("=" * 50)
        self._log("Pipeline complete!")
        self._log(f"  Iterations: {len(iterations)}")
        self._log(f"  Total issues found: {total_issues}")
        self._log(f"  Total issues fixed: {total_fixed}")
        max_version = max(all_versions.keys())
        self._log(f"  Final version: V{max_version}")
        self._log("=" * 50)

        return PipelineResult(
            summary=summary,
            v1=v1,
            review_v1=all_reviews.get(1),
            v2=v2_data,
            review_v2=all_reviews.get(2),
            v3=v3_data,
            review_v3=all_reviews.get(3),
            v4=v4_data,
            review_v4=all_reviews.get(4),
            v5=v5_data,
            review_v5=all_reviews.get(5),
            iterations=iterations,
            total_issues=total_issues,
            issues_fixed=total_fixed,
            metadata={}
        )

    def _detect_stuck_loop(self, review_history: List[ReviewOutput]) -> tuple:
        """
        CRITICAL FIX #3: Detect if same issues keep appearing across iterations.
        
        Returns:
            (is_stuck, repeated_issue_ids): True if stuck, with set of issue IDs that repeat
        """
        if len(review_history) < 3:
            return False, set()
        
        # Get issue IDs from last 3 reviews
        recent_issues = [
            set([issue.issue_id for issue in review.issues])
            for review in review_history[-3:]
        ]
        
        # Find issues that appear in all 3 recent reviews
        if len(recent_issues) >= 3:
            repeated = recent_issues[0] & recent_issues[1] & recent_issues[2]
            
            if len(repeated) > 0:
                return True, repeated
        
        return False, set()
    
    def _create_final_result(
        self,
        summary: SummaryOutput,
        v1: FormattedOutput,
        all_versions: Dict[int, Union[FormattedOutput, RefinedOutput]],
        all_reviews: Dict[int, ReviewOutput],
        iterations: List[IterationResult],
        total_issues: int,
        total_fixed: int,
        metadata: Dict[str, Any]
    ) -> PipelineResult:
        """
        CRITICAL FIX #4: Helper to create PipelineResult with metadata tracking.
        """
        # Extract individual version data
        v2_data = all_versions.get(2) if isinstance(all_versions.get(2), RefinedOutput) else None
        v3_data = all_versions.get(3) if isinstance(all_versions.get(3), RefinedOutput) else None
        v4_data = all_versions.get(4) if isinstance(all_versions.get(4), RefinedOutput) else None
        v5_data = all_versions.get(5) if isinstance(all_versions.get(5), RefinedOutput) else None
        
        self._log("=" * 50)
        self._log(f"Pipeline terminated: {metadata.get('termination_reason', 'completed')}")
        self._log(f"  Iterations: {len(iterations)}")
        self._log(f"  Total issues found: {total_issues}")
        self._log(f"  Total issues fixed: {total_fixed}")
        self._log("=" * 50)
        
        return PipelineResult(
            summary=summary,
            v1=v1,
            review_v1=all_reviews.get(1),
            v2=v2_data,
            review_v2=all_reviews.get(2),
            v3=v3_data,
            review_v3=all_reviews.get(3),
            v4=v4_data,
            review_v4=all_reviews.get(4),
            v5=v5_data,
            review_v5=all_reviews.get(5),
            iterations=iterations,
            total_issues=total_issues,
            issues_fixed=total_fixed,
            metadata=metadata
        )

    def _content_unchanged(
        self, 
        before: Union[FormattedOutput, RefinedOutput], 
        after: RefinedOutput
    ) -> bool:
        """Check if content is unchanged between versions."""
        return (
            before.linkedin.content == after.linkedin.content and
            before.twitter.tweets == after.twitter.tweets and
            before.newsletter.content == after.newsletter.content
        )

    def _create_refined_from_current(
        self, 
        current: Union[FormattedOutput, RefinedOutput],
        version: int
    ) -> RefinedOutput:
        """Create a RefinedOutput from current output when no refinement needed."""
        return RefinedOutput(
            version=version,
            changes=[],
            linkedin=LinkedInOutput(
                content=current.linkedin.content,
                used_kps=current.linkedin.used_kps
            ),
            twitter=TwitterOutput(
                tweets=current.twitter.tweets,
                used_kps=current.twitter.used_kps
            ),
            newsletter=NewsletterOutput(
                content=current.newsletter.content,
                used_kps=current.newsletter.used_kps
            )
        )

    def save_results(
        self,
        result: PipelineResult,
        output_dir: str = "output",
    ) -> Path:
        """Save pipeline results to JSON files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save complete result
        complete_file = output_path / f"pipeline_result_{timestamp}.json"
        with open(complete_file, "w", encoding="utf-8") as f:
            json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)

        # Save readable outputs
        readable = output_path / f"content_{timestamp}.md"
        with open(readable, "w", encoding="utf-8") as f:
            f.write("# Generated Content\n\n")
            
            f.write("## Core Message\n")
            f.write(f"{result.summary.core_message}\n\n")
            
            f.write("## Key Points\n")
            for kp in result.summary.key_points:
                f.write(f"- **{kp.label}** [{kp.priority}]")
                if kp.data:
                    f.write(f" - {kp.data}")
                f.write("\n")
            f.write("\n")
            
            f.write("## LinkedIn Post\n")
            f.write(f"{result.v2.linkedin.content}\n\n")
            
            f.write("## Twitter Thread\n")
            for i, tweet in enumerate(result.v2.twitter.tweets, 1):
                f.write(f"{i}. {tweet}\n")
            f.write("\n")
            
            f.write("## Newsletter\n")
            f.write(f"{result.v2.newsletter.content}\n\n")
            
            f.write("## Changes Made\n")
            for change in result.v2.changes:
                f.write(f"- [{change.issue_id}] {change.action} {change.target}\n")

        self._log(f"Results saved to {output_path}/")
        return output_path

    def print_comparison(self, result: PipelineResult) -> None:
        """Print V1 vs V2 comparison."""
        print("\n" + "=" * 60)
        print("V1 vs V2 COMPARISON")
        print("=" * 60)
        
        print("\n--- REVIEW V1 ---")
        print(f"Issues found: {len(result.review_v1.issues)}")
        for issue in result.review_v1.issues[:3]:
            print(f"  [{issue.priority}] {issue.problem}")
        
        print("\n--- LINKEDIN ---")
        print(f"V1: {result.v1.linkedin.content[:100]}...")
        print(f"V2: {result.v2.linkedin.content[:100]}...")
        
        print("\n--- TWITTER (first tweet) ---")
        print(f"V1: {result.v1.twitter.tweets[0] if result.v1.twitter.tweets else 'N/A'}")
        print(f"V2: {result.v2.twitter.tweets[0] if result.v2.twitter.tweets else 'N/A'}")
        
        print("\n--- CHANGES ---")
        for change in result.v2.changes[:5]:
            print(f"  [{change.issue_id}] {change.action} {change.target}")
        
        print("\n--- REVIEW V2 ---")
        print(f"Issues found: {len(result.review_v2.issues)}")
        print(f"Status: {result.review_v2.status}")
        
        print("=" * 60)
