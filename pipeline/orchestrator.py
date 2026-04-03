"""
Pipeline Orchestrator: Coordinates the multi-agent workflow.

CLEAN DESIGN v4:
Flow: Summarizer -> Formatter -> Reviewer -> Refiner
- No scores, just issue-driven feedback
- Simple iteration until no critical issues remain
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List

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
    Orchestrates the multi-agent content pipeline.

    Flow:
    1. Summarizer: Raw content -> core_message + key_points
    2. Formatter: key_points -> platform content (V1)
    3. Reviewer: V1 -> issues
    4. Refiner: V1 + issues -> V2
    5. Loop: Review V2, refine if critical issues remain
    """

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        verbose: bool = True,
        max_iterations: int = 2,
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
        Execute the full pipeline.

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
        self._log("Stage 1/4: Extracting key points...")
        summary = self.summarizer.run(content, prefs)
        self._log(f"  [OK] Extracted {len(summary.key_points)} key points")
        self._log(f"  Core: {summary.core_message[:60]}...")

        # Stage 2: Format
        self._log("Stage 2/4: Formatting for platforms...")
        v1 = self.formatter.run(summary, prefs, prefs.platforms)
        self._log(f"  [OK] LinkedIn: {len(v1.linkedin.content.split())} words")
        self._log(f"  [OK] Twitter: {len(v1.twitter.tweets)} tweets")
        self._log(f"  [OK] Newsletter: {len(v1.newsletter.content.split())} words")

        # Stage 3: Review
        self._log("Stage 3/4: Reviewing content...")
        review = self.reviewer.run(summary, v1)
        critical_count = len([i for i in review.issues if i.priority == "critical"])
        high_count = len([i for i in review.issues if i.priority == "high"])
        self._log(f"  [OK] Found {len(review.issues)} issues ({critical_count} critical, {high_count} high)")

        # Stage 4: Refine (iterate if needed)
        iterations: List[IterationResult] = []
        current_v = v1
        current_review = review
        
        for iteration in range(1, self.max_iterations + 1):
            # Check if refinement needed
            critical_issues = [i for i in current_review.issues if i.priority == "critical"]
            
            if not critical_issues and iteration > 1:
                self._log(f"  No critical issues remaining, stopping.")
                break
            
            self._log(f"Stage 4: Refinement iteration {iteration}...")
            
            # Refine
            refined = self.refiner.run(summary, current_v, current_review)
            self._log(f"  [OK] Made {len(refined.changes)} changes")
            
            # Convert refined to formatted for next review
            current_v = FormattedOutput(
                version=refined.version,
                linkedin=refined.linkedin,
                twitter=refined.twitter,
                newsletter=refined.newsletter
            )
            
            # Review again
            current_review = self.reviewer.run(summary, current_v)
            new_critical = len([i for i in current_review.issues if i.priority == "critical"])
            self._log(f"  [OK] {new_critical} critical issues remaining")
            
            # Record iteration
            iterations.append(IterationResult(
                iteration=iteration,
                review=current_review,
                refined=refined,
                issues_fixed=len(refined.changes)
            ))
            
            if new_critical == 0:
                self._log(f"  All critical issues resolved!")
                break
        
        # Build final v2
        if iterations:
            v2 = iterations[-1].refined
        else:
            # No refinement needed
            v2 = RefinedOutput(
                version=2,
                changes=[],
                linkedin=v1.linkedin,
                twitter=v1.twitter,
                newsletter=v1.newsletter
            )

        total_issues = len(review.issues)
        issues_fixed = sum(it.issues_fixed for it in iterations)
        
        self._log("=" * 50)
        self._log("Pipeline complete!")
        self._log(f"  Total issues: {total_issues}")
        self._log(f"  Issues fixed: {issues_fixed}")
        self._log(f"  Iterations: {len(iterations)}")
        self._log("=" * 50)

        return PipelineResult(
            summary=summary,
            v1=v1,
            review=review,
            v2=v2,
            iterations=iterations,
            total_issues=total_issues,
            issues_fixed=issues_fixed
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
        
        print("\n--- LINKEDIN ---")
        print(f"V1: {result.v1.linkedin.content[:100]}...")
        print(f"V2: {result.v2.linkedin.content[:100]}...")
        
        print("\n--- TWITTER (first tweet) ---")
        print(f"V1: {result.v1.twitter.tweets[0] if result.v1.twitter.tweets else 'N/A'}")
        print(f"V2: {result.v2.twitter.tweets[0] if result.v2.twitter.tweets else 'N/A'}")
        
        print("\n--- CHANGES ---")
        for change in result.v2.changes[:5]:
            print(f"  [{change.issue_id}] {change.action} {change.target}")
        
        print("=" * 60)
