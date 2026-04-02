"""
ReviewerAgent: Critically evaluates formatted content against the original summary.
Provides detailed, structured feedback for the Refiner to act upon.

UPGRADE v2: Multi-Dimensional, Platform-Aware, Coverage-Focused
- Platform-fit scores per platform
- Coverage analysis (missing_key_points, used_key_points)
- Constraint violation detection
- Cross-format consistency checks
- Structured issues with severity and traceability
"""

from typing import Optional
from schemas.schemas import (
    SummaryOutput,
    FormattedOutput,
    ReviewOutput,
    ReviewIssue,
    ReviewScores,
    PlatformFitScores,
    CoverageAnalysis,
    ConstraintViolation,
    CrossFormatConsistency,
    FormatReview,
)
from utils.llm import LLMClient, get_llm_client
from config.platform_config import PlatformConfig, DEFAULT_PLATFORM_CONFIG


REVIEWER_SYSTEM_PROMPT = """You are a senior content editor and SYSTEM evaluator. Your job is to critically evaluate formatted content against its source summary using multi-dimensional scoring and constraint checking.

## SCORING DIMENSIONS (All scores 0.0-1.0)

### 1. COVERAGE (0.0-1.0)
Are ALL key_points from summary represented?
- 1.0: Every key_point appears in at least one format
- 0.8-0.9: Most key_points covered, 1 missing
- 0.6-0.7: Several key_points missing
- <0.6: Major gaps in coverage

### 2. CLARITY (0.0-1.0)
How clear is the messaging?
- 1.0: Crystal clear, immediately understandable
- 0.7-0.9: Clear with minor ambiguities
- <0.7: Confusing or unclear

### 3. ENGAGEMENT (0.0-1.0)
How compelling is the content?
- 1.0: Highly engaging, would stop scrolling
- 0.7-0.9: Engaging with room for improvement
- <0.7: Bland or unengaging

### 4. CONSISTENCY (0.0-1.0)
Are messages consistent across formats?
- 1.0: Perfect alignment
- 0.7-0.9: Minor inconsistencies
- <0.7: Conflicting messages

### 5. PLATFORM_FIT (per platform, 0.0-1.0)
Does content fit platform norms?
- linkedin: Professional tone, strong hook, clear CTA
- twitter: Concise, punchy, proper thread structure
- newsletter: Scannable, valuable, proper sections

## COVERAGE ANALYSIS (CRITICAL)
- missing_key_points: List key_points not covered anywhere (e.g., ["key_points[2]"])
- used_key_points: List key_points that are covered (e.g., ["key_points[0]", "key_points[1]"])
- coverage_by_format: Which key_points appear in each format

## CONSTRAINT VIOLATIONS
Check for:
- twitter_length: Any tweet > 280 chars
- thread_size: Thread outside allowed range
- linkedin_length: Content too short/long
- missing_hook: No strong opening
- hashtag_count: Too many/few hashtags

## CROSS-FORMAT CONSISTENCY
- missing_points: Key point in one format but missing from another
- contradictions: Conflicting statements between formats
- tone_mismatch: Inconsistent tone/voice

## STRUCTURED ISSUES
For each issue, provide:
- id: Unique identifier (issue_1, issue_2, etc.)
- type: missing_coverage | clarity | engagement | length | consistency | platform_fit | constraint_violation | tone_mismatch
- target: Specific location (e.g., "twitter_thread[2]", "linkedin_hook")
- severity: critical | high | medium | low
- related_key_point: If applicable (e.g., "key_points[2]")

BE A SYSTEM EVALUATOR, NOT A STYLIST. Focus on coverage, constraints, and correctness."""


class ReviewerAgent:
    """
    Critically evaluates formatted content against the source summary.

    Responsibility: Multi-dimensional evaluation including:
    - Coverage analysis (all key_points represented)
    - Platform constraint validation
    - Cross-format consistency checks
    - Structured issues for targeted refinement
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        platform_config: Optional[PlatformConfig] = None
    ):
        """
        Initialize the ReviewerAgent.
        
        Args:
            llm_client: Optional custom LLM client
            platform_config: Platform constraints for validation
        """
        self.llm = llm_client or get_llm_client()
        self.system_prompt = REVIEWER_SYSTEM_PROMPT
        self.platform_config = platform_config or DEFAULT_PLATFORM_CONFIG

    def run(
        self,
        summary: SummaryOutput,
        formatted: FormattedOutput,
    ) -> ReviewOutput:
        """
        Review formatted content against the original summary.

        Args:
            summary: Original structured summary
            formatted: Formatted content to review

        Returns:
            ReviewOutput with multi-dimensional scores, coverage analysis,
            violations, and structured issues
        """
        # Build semantic key_points list
        key_points_text = "\n".join(
            f"- {kp.id}: [{kp.importance}] {kp.concept} - {kp.claim}"
            for kp in summary.key_points
        )
        
        # Build key point IDs for reference
        kp_ids = [kp.id for kp in summary.key_points]

        # Build insights text with IDs
        insights_list = "\n".join(
            f"- [{i.id}] [{i.importance.upper()}] {i.topic}: {i.insight}"
            for i in summary.key_insights
        )

        # Format content for review
        linkedin_content = self._format_linkedin_for_review(formatted)
        twitter_content = self._format_twitter_for_review(formatted)
        newsletter_content = self._format_newsletter_for_review(formatted)

        # Run deterministic checks first
        violations, coverage_analysis = self._run_deterministic_checks(formatted, summary)

        # Build violations text
        violations_text = "\n".join(
            f"- [{v.severity.upper()}] {v.type}: {v.message} (at: {v.location})"
            for v in violations
        ) if violations else "No violations detected."

        # Build coverage text
        coverage_text = f"""Missing: {coverage_analysis.missing_key_points or 'None'}
Used: {coverage_analysis.used_key_points or 'Unable to determine automatically'}
Total Key Points: {len(kp_ids)}"""

        user_prompt = f"""Critically review this formatted content against the original summary.

## ORIGINAL SUMMARY (Content DNA)
Title: {summary.title}
Core Message: {summary.core_message}
Intent: {summary.intent}
Tone: {summary.tone}

SEMANTIC KEY POINTS TO CHECK FOR COVERAGE (use these IDs):
{key_points_text}

KEY INSIGHTS (with IDs):
{insights_list}

---

## FORMATTED CONTENT

### LINKEDIN:
{linkedin_content}

### TWITTER:
{twitter_content}

### NEWSLETTER:
{newsletter_content}

---

## DETERMINISTIC CHECKS (already validated):

### CONSTRAINT VIOLATIONS:
{violations_text}

### COVERAGE ANALYSIS:
{coverage_text}

---

## YOUR TASK

1. SCORES (0.0-1.0 scale for the `scores` object):
   - clarity: Overall message clarity
   - engagement: How compelling/engaging
   - coverage: How many key_points are represented
   - consistency: Cross-format message alignment
   - platform_fit.linkedin: How well it fits LinkedIn
   - platform_fit.twitter: How well it fits Twitter
   - platform_fit.newsletter: How well it fits Newsletter

2. COVERAGE ANALYSIS:
   - Verify which key_points appear in each format
   - List missing_key_points and used_key_points

3. CROSS-FORMAT CONSISTENCY:
   - Check for contradictions between formats
   - Check for tone mismatches
   - List any key_points missing from specific formats

4. STRUCTURED ISSUES:
   For each problem, create an issue with:
   - id: "issue_1", "issue_2", etc.
   - type: missing_coverage | clarity | engagement | constraint_violation | etc.
   - target: Specific location (e.g., "twitter_thread[2]")
   - severity: critical | high | medium | low
   - related_key_point: If about coverage (e.g., "key_points[2]")

5. Also provide legacy 1-10 scores for backward compatibility:
   - coverage_score, clarity_score, engagement_score, consistency_score, overall_alignment_score"""

        result = self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            output_schema=ReviewOutput,
            temperature=0.3,
        )

        # Merge deterministic results with LLM results
        result = self._merge_deterministic_results(result, violations, coverage_analysis)

        return result

    def _format_linkedin_for_review(self, formatted: FormattedOutput) -> str:
        """Format LinkedIn content for review."""
        return f"""HOOK: {formatted.linkedin.hook}
BODY: {formatted.linkedin.body}
CTA: {formatted.linkedin.call_to_action}
HASHTAGS: {', '.join(formatted.linkedin.hashtags)}
DERIVED_FROM: {formatted.linkedin.derived_from}
SOURCE_INSIGHTS: {formatted.linkedin.source_insights}"""

    def _format_twitter_for_review(self, formatted: FormattedOutput) -> str:
        """Format Twitter content for review."""
        content = f"HOOK: {formatted.twitter.thread_hook}\nTWEETS:\n"
        for i, tweet in enumerate(formatted.twitter.tweets):
            char_count = len(tweet)
            status = "✓" if char_count <= 280 else f"⚠️ {char_count} chars"
            content += f"{i+1}. [{status}] {tweet}\n"
        
        if formatted.twitter.tweet_mappings:
            content += "\nTWEET_MAPPINGS:\n"
            for m in formatted.twitter.tweet_mappings:
                content += f"  Tweet {m.tweet_index}: {m.derived_from}\n"
        
        content += f"\nDERIVED_FROM: {formatted.twitter.derived_from}"
        return content

    def _format_newsletter_for_review(self, formatted: FormattedOutput) -> str:
        """Format newsletter content for review."""
        sections = "\n".join(f"- {section}" for section in formatted.newsletter.body_sections)
        return f"""SUBJECT: {formatted.newsletter.subject_line}
PREVIEW: {formatted.newsletter.preview_text}
INTRO: {formatted.newsletter.intro}
BODY SECTIONS:
{sections}
CLOSING: {formatted.newsletter.closing}
DERIVED_FROM: {formatted.newsletter.derived_from}"""

    def _run_deterministic_checks(
        self,
        formatted: FormattedOutput,
        summary: SummaryOutput,
    ) -> tuple[list[ConstraintViolation], CoverageAnalysis]:
        """
        Run rule-based deterministic checks on formatted content.
        
        Returns tuple of (violations, coverage_analysis).
        """
        violations = []
        tc = self.platform_config.twitter
        nc = self.platform_config.newsletter

        # Check tweet lengths
        for i, tweet in enumerate(formatted.twitter.tweets):
            if len(tweet) > tc.max_chars_per_tweet:
                violations.append(ConstraintViolation(
                    type="twitter_length",
                    message=f"Tweet {i+1} exceeds {tc.max_chars_per_tweet} chars ({len(tweet)} chars)",
                    location=f"twitter_thread[{i}]",
                    severity="error"
                ))

        # Check thread size
        thread_len = len(formatted.twitter.tweets)
        if thread_len < tc.thread_length_min:
            violations.append(ConstraintViolation(
                type="thread_size",
                message=f"Thread too short: {thread_len} tweets (min: {tc.thread_length_min})",
                location="twitter_thread",
                severity="error"
            ))
        elif thread_len > tc.thread_length_max:
            violations.append(ConstraintViolation(
                type="thread_size",
                message=f"Thread too long: {thread_len} tweets (max: {tc.thread_length_max})",
                location="twitter_thread",
                severity="warning"
            ))

        # Check LinkedIn hook
        if len(formatted.linkedin.hook) < 20:
            violations.append(ConstraintViolation(
                type="missing_hook",
                message=f"LinkedIn hook too short ({len(formatted.linkedin.hook)} chars)",
                location="linkedin_hook",
                severity="error"
            ))

        # Check newsletter sections
        section_count = len(formatted.newsletter.body_sections)
        if section_count < nc.min_sections:
            violations.append(ConstraintViolation(
                type="newsletter_sections",
                message=f"Too few sections: {section_count} (min: {nc.min_sections})",
                location="newsletter_body",
                severity="warning"
            ))

        # Check hashtags
        hashtag_count = len(formatted.linkedin.hashtags)
        if hashtag_count > 5:
            violations.append(ConstraintViolation(
                type="hashtag_count",
                message=f"Too many hashtags: {hashtag_count}",
                location="linkedin_hashtags",
                severity="warning"
            ))
        elif hashtag_count < 2:
            violations.append(ConstraintViolation(
                type="hashtag_count",
                message=f"Too few hashtags: {hashtag_count}",
                location="linkedin_hashtags",
                severity="warning"
            ))

        # Coverage analysis
        coverage_analysis = self._analyze_coverage(formatted, summary)

        return violations, coverage_analysis

    def _analyze_coverage(
        self,
        formatted: FormattedOutput,
        summary: SummaryOutput
    ) -> CoverageAnalysis:
        """Analyze semantic key_point coverage across all formats."""
        # Get all key point IDs (semantic IDs like "kp_1", "kp_2")
        all_key_points = [kp.id for kp in summary.key_points]
        
        # Collect derived_from from all formats
        linkedin_derived = set(formatted.linkedin.derived_from or [])
        twitter_derived = set(formatted.twitter.derived_from or [])
        newsletter_derived = set(formatted.newsletter.derived_from or [])
        
        all_used = linkedin_derived | twitter_derived | newsletter_derived
        
        # Find missing key points (those not in any derived_from)
        missing = [kp for kp in all_key_points if kp not in all_used]
        used = [kp for kp in all_key_points if kp in all_used]
        
        return CoverageAnalysis(
            missing_key_points=missing,
            used_key_points=used,
            coverage_by_format={
                "linkedin": list(linkedin_derived),
                "twitter": list(twitter_derived),
                "newsletter": list(newsletter_derived)
            }
        )

    def _merge_deterministic_results(
        self,
        result: ReviewOutput,
        violations: list[ConstraintViolation],
        coverage_analysis: CoverageAnalysis
    ) -> ReviewOutput:
        """Merge deterministic check results into the LLM review output."""
        # Add violations
        result.violations = violations
        
        # Merge coverage analysis (prefer deterministic where available)
        if coverage_analysis.missing_key_points:
            result.coverage_analysis.missing_key_points = coverage_analysis.missing_key_points
        if coverage_analysis.used_key_points:
            result.coverage_analysis.used_key_points = coverage_analysis.used_key_points
        if coverage_analysis.coverage_by_format:
            result.coverage_analysis.coverage_by_format = coverage_analysis.coverage_by_format
        
        # Add violation-based issues
        for i, v in enumerate(violations):
            if v.severity == "error":
                issue = ReviewIssue(
                    id=f"violation_{i+1}",
                    type="constraint_violation",
                    description=v.message,
                    target=v.location,
                    affected_formats=[v.location.split("_")[0] if "_" in v.location else "twitter"],
                    severity="critical" if v.severity == "error" else "medium"
                )
                result.issues.append(issue)
        
        # Add coverage issues
        for kp in coverage_analysis.missing_key_points:
            issue = ReviewIssue(
                id=f"coverage_{kp}",
                type="missing_coverage",
                description=f"Key point {kp} is not covered in any format",
                target="all",
                affected_formats=["linkedin", "twitter", "newsletter"],
                severity="high",
                related_key_point=kp
            )
            result.issues.append(issue)
        
        # Apply penalty-based score adjustments
        result = self._apply_strict_scoring(result, violations, coverage_analysis)
        
        return result
    
    def _apply_strict_scoring(
        self,
        result: ReviewOutput,
        violations: list[ConstraintViolation],
        coverage_analysis: CoverageAnalysis
    ) -> ReviewOutput:
        """
        Apply penalty-based scoring to prevent cheerleader mode.
        
        Scoring Logic:
        - coverage = used_key_points / total_key_points (deterministic)
        - Penalties for violations, missing coverage, weak hooks
        - Perfect scores (1.0) are reduced by perfect_score_penalty
        """
        from config.settings import settings
        
        # Calculate deterministic coverage score
        total_kps = len(coverage_analysis.missing_key_points) + len(coverage_analysis.used_key_points)
        if total_kps > 0:
            coverage_score = len(coverage_analysis.used_key_points) / total_kps
        else:
            coverage_score = 0.5  # Unknown
        
        # Override LLM coverage with deterministic calculation
        if result.scores:
            result.scores.coverage = round(coverage_score, 2)
        
        # Count violation penalties
        error_count = sum(1 for v in violations if v.severity == "error")
        warning_count = sum(1 for v in violations if v.severity == "warning")
        
        # Apply penalties to platform fit scores
        if result.scores and result.scores.platform_fit:
            # Twitter penalties
            twitter_penalties = sum(0.1 for v in violations if "twitter" in v.location.lower())
            result.scores.platform_fit.twitter = max(0.1, result.scores.platform_fit.twitter - twitter_penalties)
            
            # LinkedIn penalties  
            linkedin_penalties = sum(0.1 for v in violations if "linkedin" in v.location.lower())
            result.scores.platform_fit.linkedin = max(0.1, result.scores.platform_fit.linkedin - linkedin_penalties)
            
            # Newsletter penalties
            newsletter_penalties = sum(0.1 for v in violations if "newsletter" in v.location.lower())
            result.scores.platform_fit.newsletter = max(0.1, result.scores.platform_fit.newsletter - newsletter_penalties)
        
        # Apply perfect score penalty (prevent cheerleader mode)
        if result.scores:
            penalty = settings.feedback_loop.perfect_score_penalty
            if result.scores.clarity >= 1.0:
                result.scores.clarity = 1.0 - penalty
            if result.scores.engagement >= 1.0:
                result.scores.engagement = 1.0 - penalty
            if result.scores.consistency >= 1.0:
                result.scores.consistency = 1.0 - penalty
        
        # Penalize overall scores for errors
        if result.scores and error_count > 0:
            penalty = min(0.2 * error_count, 0.4)  # Max 40% penalty
            result.scores.clarity = max(0.1, result.scores.clarity - penalty)
            result.scores.engagement = max(0.1, result.scores.engagement - penalty)
        
        # Recalculate legacy scores to align
        if result.scores:
            result.coverage_score = round(result.scores.coverage * 10, 1)
            result.clarity_score = round(result.scores.clarity * 10, 1)
            result.engagement_score = round(result.scores.engagement * 10, 1)
            result.consistency_score = round(result.scores.consistency * 10, 1)
            result.overall_alignment_score = round(
                (result.scores.coverage + result.scores.clarity + 
                 result.scores.engagement + result.scores.consistency) / 4 * 10, 1
            )
        
        return result
