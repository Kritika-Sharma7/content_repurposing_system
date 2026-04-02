"""
RefinerAgent: Improves content based on reviewer feedback.
Creates new version by addressing flagged issues.

UPGRADE v2: Strictly Targeted, Issue-Driven
- DO NOT regenerate entire content
- ONLY fix issues flagged by reviewer  
- DO NOT introduce new external examples (no hallucination)
- ONLY use summary.key_points for content
- Track changes_applied with issue references
"""

from typing import Optional
from schemas.schemas import (
    SummaryOutput,
    FormattedOutput,
    ReviewOutput,
    RefinedOutput,
    ChangeApplied,
    ChangeRecord,
)
from utils.llm import LLMClient, get_llm_client
from config.platform_config import PlatformConfig, DEFAULT_PLATFORM_CONFIG


REFINER_SYSTEM_PROMPT = """You are an expert content refiner performing TARGETED FIXES. Your job is to improve content based on specific reviewer feedback while staying STRICTLY GROUNDED in the source material.

## 🚨 CRITICAL RULES 🚨

### RULE 1: NO FULL REWRITES
- Make SURGICAL changes to fix specific issues
- PRESERVE content that works well
- Change ONLY what the reviewer flagged

### RULE 2: NO HALLUCINATION
- NEVER invent examples like "Company X", "Startup Y", "Organization Z"
- ONLY use ideas, facts, and examples from the summary.key_points
- If you need to add content, use language from the key_points

### RULE 3: ISSUE-DRIVEN CHANGES
- Each change MUST address a specific issue from the review
- Document which issue_id each change addresses
- Do NOT make changes that weren't requested

### RULE 4: RESPECT CONSTRAINTS
- Twitter: Each tweet MUST be ≤280 characters
- If fixing a tweet, ensure it stays under 280 chars
- LinkedIn: Keep strong hook, clear CTA
- Newsletter: Maintain scannable structure

## GOOD EXAMPLES
✓ "Changing tweet 3 to include key_points[2] about async communication"
✓ "Shortening tweet 5 from 295 to 275 characters"
✓ "Adding missing key_point about documentation to newsletter"

## BAD EXAMPLES
✗ "Company X saw 50% improvement after implementing this" (invented)
✗ "Completely rewriting the LinkedIn post" (too broad)
✗ "Adding a new section about AI" (not from summary)

## CHANGE TRACKING
For EACH change, document:
- issue_id: Which issue this fixes (e.g., "issue_1", "violation_1", "coverage_key_points[2]")
- action: "modify" | "add" | "remove" | "restructure"
- target: Specific location (e.g., "twitter_thread[2]", "linkedin_hook")
- change_type: What kind of fix
- related_key_point: If adding coverage (e.g., "key_points[2]")
- before: Original content (if modifying)
- after: New content

## YOUR APPROACH
1. Review all issues from the reviewer
2. Prioritize: critical > high > medium > low
3. Fix constraint violations first (tweets over 280, etc.)
4. Address coverage gaps by adding key_points naturally
5. Make minimal changes to preserve what works"""


class RefinerAgent:
    """
    Refines formatted content based on reviewer feedback.

    Responsibility: Take review feedback and produce improved content
    that addresses specific issues while preserving what worked.
    
    Strictly:
    - Issue-driven changes only
    - No full rewrites
    - No hallucination
    - Uses only summary.key_points
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        platform_config: Optional[PlatformConfig] = None
    ):
        """
        Initialize the RefinerAgent.

        Args:
            llm_client: Optional custom LLM client
            platform_config: Platform constraints
        """
        self.llm = llm_client or get_llm_client()
        self.system_prompt = REFINER_SYSTEM_PROMPT
        self.platform_config = platform_config or DEFAULT_PLATFORM_CONFIG

    def run(
        self,
        summary: SummaryOutput,
        formatted: FormattedOutput,
        review: ReviewOutput,
        force_iteration: bool = False,
    ) -> RefinedOutput:
        """
        Refine content based on review feedback.

        Args:
            summary: Original summary for reference
            formatted: Current formatted content
            review: Detailed review feedback with issues
            force_iteration: If True, force at least one refinement even if no major issues

        Returns:
            RefinedOutput with targeted fixes
        """
        from config.settings import settings
        
        # Build semantic key_points reference
        key_points_ref = "\n".join(
            f"- {kp.id}: [{kp.importance}] {kp.concept} - {kp.claim} → {kp.implication}"
            for kp in summary.key_points
        )
        
        # Build key point ID list for reference
        kp_ids = [kp.id for kp in summary.key_points]

        # Build issues list - prioritized
        critical_issues = [i for i in review.issues if i.severity == "critical"]
        high_issues = [i for i in review.issues if i.severity == "high"]
        medium_issues = [i for i in review.issues if i.severity == "medium"]
        low_issues = [i for i in review.issues if i.severity == "low"]
        
        all_issues = critical_issues + high_issues + medium_issues + low_issues
        
        # Force iteration: if no issues but force_iteration is True, find improvements
        forced_improvements = []
        if force_iteration and not all_issues:
            forced_improvements = self._identify_forced_improvements(formatted, review, summary)
        
        issues_text = self._format_issues(all_issues)
        forced_text = self._format_forced_improvements(forced_improvements) if forced_improvements else ""

        # Build violations text
        violations_text = "\n".join(
            f"- [{v.severity.upper()}] {v.type}: {v.message} (at: {v.location})"
            for v in review.violations
        ) if review.violations else "None"

        # Build coverage analysis text with semantic IDs
        coverage_text = f"""Missing key_points: {review.coverage_analysis.missing_key_points or 'None'}
Used key_points: {review.coverage_analysis.used_key_points or 'See review'}
Available key_point IDs: {kp_ids}"""

        # Format current content
        linkedin_current = self._format_linkedin(formatted)
        twitter_current = self._format_twitter(formatted)
        newsletter_current = self._format_newsletter(formatted)

        # Build constraints text
        tc = self.platform_config.twitter
        constraints_text = f"""- Twitter: Each tweet MUST be ≤{tc.max_chars_per_tweet} characters
- Twitter thread: {tc.thread_length_min}-{tc.thread_length_max} tweets
- LinkedIn: Hook required, professional tone
- Newsletter: 3-5 scannable sections"""

        user_prompt = f"""Fix the specific issues identified in the review.

## REFERENCE: SEMANTIC KEY POINTS (use ONLY these for content)
{key_points_ref}

## PLATFORM CONSTRAINTS
{constraints_text}

---

## CURRENT CONTENT (Version {formatted.version})

### LinkedIn:
{linkedin_current}

### Twitter:
{twitter_current}

### Newsletter:
{newsletter_current}

---

## ISSUES TO FIX (prioritized)

### Constraint Violations (fix first):
{violations_text}

### Coverage Analysis:
{coverage_text}

### All Issues (by severity):
{issues_text}
{forced_text}

### Scores (for context):
- Coverage: {review.scores.coverage:.2f}
- Clarity: {review.scores.clarity:.2f}
- Engagement: {review.scores.engagement:.2f}
- Consistency: {review.scores.consistency:.2f}

---

## YOUR TASK

1. FIX CONSTRAINT VIOLATIONS FIRST
   - Any tweet over {tc.max_chars_per_tweet} chars → shorten while preserving meaning
   - Thread size issues → add/remove tweets as needed

2. ADDRESS COVERAGE GAPS
   - For each missing key_point (use IDs like kp_1, kp_2), ADD it naturally to appropriate format
   - Use the EXACT concepts and claims from key_points (no invention)

3. FIX OTHER ISSUES by severity (critical → high → medium)

4. DOCUMENT EACH CHANGE in changes_applied:
   - issue_id: Which issue this fixes
   - action: "modify" | "add" | "remove"
   - target: Where (e.g., "twitter_thread[2]")
   - change_type: Category of fix
   - related_key_point: If adding coverage (use semantic ID like "kp_1")

5. PRESERVE what works - do NOT change content that wasn't flagged

## REMEMBER
- NO invented examples
- NO full rewrites
- ONLY fix what was flagged
- Use ONLY language from key_points
- Reference key points by their IDs (kp_1, kp_2, etc.)"""

        result = self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            output_schema=RefinedOutput,
            temperature=0.5,  # Lower temperature for more precise fixes
        )

        # Post-process to validate changes
        result = self._post_process(result, formatted, review, forced_improvements)

        # Set version
        result.version = formatted.version + 1

        return result

    def _identify_forced_improvements(
        self,
        formatted: FormattedOutput,
        review: ReviewOutput,
        summary: SummaryOutput
    ) -> list[dict]:
        """
        Identify improvements to force when no major issues exist.
        This prevents "no changes needed" scenarios that kill feedback loop credibility.
        """
        improvements = []
        
        # Check if any score is below perfect
        if review.scores.engagement < 0.95:
            improvements.append({
                "type": "engagement_improvement",
                "target": "linkedin_hook",
                "description": f"Engagement score ({review.scores.engagement:.2f}) can be improved. Strengthen the hook.",
                "priority": "medium"
            })
        
        if review.scores.clarity < 0.95:
            improvements.append({
                "type": "clarity_improvement",
                "target": "newsletter_intro",
                "description": f"Clarity score ({review.scores.clarity:.2f}) can be improved. Simplify complex sentences.",
                "priority": "medium"
            })
        
        # Check platform fit scores
        if review.scores.platform_fit:
            if review.scores.platform_fit.twitter < 0.9:
                improvements.append({
                    "type": "platform_fit",
                    "target": "twitter_thread",
                    "description": f"Twitter fit ({review.scores.platform_fit.twitter:.2f}) can improve. Make tweets punchier.",
                    "priority": "medium"
                })
        
        # If still no improvements, suggest cross-platform consistency
        if not improvements:
            improvements.append({
                "type": "consistency_improvement",
                "target": "all",
                "description": "Ensure key message emphasis is consistent across all platforms.",
                "priority": "low"
            })
        
        return improvements
    
    def _format_forced_improvements(self, improvements: list[dict]) -> str:
        """Format forced improvements for the prompt."""
        if not improvements:
            return ""
        
        lines = ["\n### FORCED IMPROVEMENTS (system requires at least one refinement):"]
        for i, imp in enumerate(improvements):
            lines.append(f"- [forced_{i+1}] [{imp['priority'].upper()}] {imp['type']}: {imp['description']} (target: {imp['target']})")
        
        return "\n".join(lines)

    def _format_issues(self, issues: list) -> str:
        """Format issues for the prompt."""
        if not issues:
            return "No issues flagged."
        
        lines = []
        for issue in issues:
            line = f"- [{issue.id}] [{issue.severity.upper()}] {issue.type}: {issue.description}"
            if issue.target:
                line += f" (target: {issue.target})"
            if issue.related_key_point:
                line += f" [relates to: {issue.related_key_point}]"
            lines.append(line)
        
        return "\n".join(lines)

    def _format_linkedin(self, formatted: FormattedOutput) -> str:
        """Format LinkedIn content for the prompt."""
        return f"""Hook: {formatted.linkedin.hook}
Body: {formatted.linkedin.body}
CTA: {formatted.linkedin.call_to_action}
Hashtags: {', '.join(formatted.linkedin.hashtags)}
Derived_from: {formatted.linkedin.derived_from}"""

    def _format_twitter(self, formatted: FormattedOutput) -> str:
        """Format Twitter content for the prompt."""
        lines = [f"Thread Hook: {formatted.twitter.thread_hook}", "Tweets:"]
        for i, tweet in enumerate(formatted.twitter.tweets):
            char_info = f"[{len(tweet)} chars]"
            lines.append(f"  {i}. {char_info} {tweet}")
        lines.append(f"Derived_from: {formatted.twitter.derived_from}")
        return "\n".join(lines)

    def _format_newsletter(self, formatted: FormattedOutput) -> str:
        """Format newsletter content for the prompt."""
        sections = "\n".join(f"  - {s}" for s in formatted.newsletter.body_sections)
        return f"""Subject: {formatted.newsletter.subject_line}
Preview: {formatted.newsletter.preview_text}
Intro: {formatted.newsletter.intro}
Body Sections:
{sections}
Closing: {formatted.newsletter.closing}
Derived_from: {formatted.newsletter.derived_from}"""

    def _post_process(
        self,
        result: RefinedOutput,
        original: FormattedOutput,
        review: ReviewOutput,
        forced_improvements: list[dict] = None
    ) -> RefinedOutput:
        """
        Post-process to validate and ensure constraint compliance.
        """
        tc = self.platform_config.twitter
        
        # Ensure tweets are within length limit
        for i, tweet in enumerate(result.twitter.tweets):
            if len(tweet) > tc.max_chars_per_tweet:
                # Emergency truncation
                truncated = tweet[:tc.max_chars_per_tweet - 3]
                last_space = truncated.rfind(' ')
                if last_space > tc.max_chars_per_tweet - 50:
                    truncated = truncated[:last_space]
                result.twitter.tweets[i] = truncated + "..."
                
                # Add change record for this fix
                result.changes_applied.append(ChangeApplied(
                    issue_id="auto_truncate",
                    action="modify",
                    target=f"twitter_thread[{i}]",
                    change_type="fix_constraint_violation",
                    before=tweet[:50] + "...",
                    after=result.twitter.tweets[i][:50] + "..."
                ))

        # Populate addressed_issues from changes_applied
        if result.changes_applied and not result.addressed_issues:
            result.addressed_issues = list(set(
                c.issue_id for c in result.changes_applied
            ))
        
        # Add forced improvement IDs if present
        if forced_improvements and result.changes_applied:
            for i, _ in enumerate(forced_improvements):
                forced_id = f"forced_{i+1}"
                if forced_id not in result.addressed_issues:
                    result.addressed_issues.append(forced_id)

        # Populate changes_made summary if empty
        if result.changes_applied and not result.changes_made:
            result.changes_made = [
                f"{c.action} {c.target}: {c.change_type}"
                for c in result.changes_applied[:5]  # Top 5
            ]

        return result
