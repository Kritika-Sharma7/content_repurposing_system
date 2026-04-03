"""
ReviewerAgent: Evaluates outputs and generates actionable feedback.

CLEAN DESIGN v4 (MOST IMPORTANT AGENT):
- Output: ISSUES ONLY (no scores)
- Each issue has: issue_id, target, type, problem, reason, suggestion, priority
- Types: structure, coverage, constraint, clarity
- Must check: coverage, constraints, structure, clarity
"""

from typing import Optional, List
from schemas.schemas import (
    SummaryOutput, FormattedOutput, ReviewOutput, ReviewIssue
)
from utils.llm import LLMClient, get_llm_client


REVIEWER_SYSTEM_PROMPT = """You are a strict content quality reviewer focused on NARRATIVE QUALITY.

## YOUR JOB
Find issues that make content feel generic, corporate, or like a "bullet dump."

## WHAT MAKES CONTENT BAD:

### LINKEDIN:
❌ Bullet dump: Uses • or - to list points instead of narrative flow
❌ Generic hook: "Here's how...", "Did you know...", "Is your..."
❌ No cause-effect: States facts without explaining WHY
❌ Corporate speak: "leverage", "unlock", "transform your"
❌ No experience framing: Doesn't feel like lived insight

### GOOD LINKEDIN SIGNS:
✅ Narrative flow with paragraphs
✅ Mistake-based or tension-based hook
✅ Cause-effect explanations (what + why)
✅ Experience framing ("We tried...", "Most teams...")
✅ Clear problem → shift → insight structure

### TWITTER:
❌ Tweets too long: Over 240 chars
❌ Announcement style: "Here's a thread on X!"
❌ No tension or opinion

### NEWSLETTER:
❌ "In conclusion": Uses this phrase
❌ No headings: Missing ## section headers
❌ Too dense: Long paragraphs without breaks

## ISSUE TYPES

1. STRUCTURE - Format/narrative problems (HIGH priority)
2. COVERAGE - Missing key points (CRITICAL if missing critical KPs)
3. CONSTRAINT - Platform rules violated (CRITICAL)
4. CLARITY - Writing quality issues (MEDIUM)

## OUTPUT FORMAT

{
  "issues": [
    {
      "issue_id": "issue_1",
      "target": "linkedin | twitter | newsletter",
      "type": "structure | coverage | constraint | clarity",
      "problem": "Specific problem",
      "reason": "Why it hurts engagement",
      "suggestion": "Exact fix with example",
      "priority": "critical | high | medium | low",
      "missing_kps": []
    }
  ]
}

## GOOD vs BAD ISSUES

✅ GOOD:
{
  "problem": "Content is a bullet dump, not narrative",
  "reason": "Bullet lists feel like a summary, not insight. They don't create engagement.",
  "suggestion": "Rewrite as: 'Most teams get this wrong. They [problem]. What changed was [shift]. The result? [outcome]'"
}

❌ BAD:
{
  "problem": "Could be more engaging",
  "suggestion": "Make it better"
}

## PRIORITY:
- CRITICAL: Constraint violations (tweet length, missing critical KPs)
- HIGH: Bullet dumps, weak hooks, no cause-effect
- MEDIUM: Clarity issues, minor structural problems
- LOW: Style preferences

Return JSON only."""


class ReviewerAgent:
    """
    Evaluates formatted content and generates actionable issues.
    
    Output: ReviewOutput with issues[] only.
    Each issue has: issue_id, target, type, problem, reason, suggestion, priority.
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None
    ):
        self.llm = llm_client or get_llm_client()
        self.system_prompt = REVIEWER_SYSTEM_PROMPT

    def run(
        self,
        summary: SummaryOutput,
        formatted: FormattedOutput,
    ) -> ReviewOutput:
        """
        Review formatted content against summary.

        Args:
            summary: Original summary with key_points
            formatted: Formatted content to review

        Returns:
            ReviewOutput with list of actionable issues
        """
        # Build key points reference
        kp_text = "\n".join(
            f"- {kp.id}: [{kp.priority.upper()}] {kp.label}" +
            (f" ({kp.data})" if kp.data else "")
            for kp in summary.key_points
        )
        
        kp_ids = [kp.id for kp in summary.key_points]
        critical_kps = [kp.id for kp in summary.key_points if kp.priority == "critical"]

        # Run deterministic checks
        deterministic_issues = self._run_deterministic_checks(formatted, summary)

        # Format content for review
        linkedin_text = f"LINKEDIN:\n{formatted.linkedin.content}\nUsed KPs: {formatted.linkedin.used_kps}"
        
        twitter_text = "TWITTER:\n"
        for i, tweet in enumerate(formatted.twitter.tweets):
            char_count = len(tweet)
            status = "OK" if char_count <= 240 else f"TOO LONG ({char_count} chars)"
            twitter_text += f"{i+1}. [{status}] {tweet}\n"
        twitter_text += f"Used KPs: {formatted.twitter.used_kps}"
        
        newsletter_text = f"NEWSLETTER:\n{formatted.newsletter.content}\nUsed KPs: {formatted.newsletter.used_kps}"

        # Coverage analysis
        all_used = set(
            formatted.linkedin.used_kps + 
            formatted.twitter.used_kps + 
            formatted.newsletter.used_kps
        )
        missing_kps = [kp for kp in kp_ids if kp not in all_used]
        missing_critical = [kp for kp in critical_kps if kp not in all_used]

        coverage_text = f"""
COVERAGE ANALYSIS:
- All KPs: {kp_ids}
- Critical KPs: {critical_kps}
- Used: {list(all_used)}
- Missing: {missing_kps}
- Missing Critical: {missing_critical}
"""

        # Deterministic issues text
        det_issues_text = ""
        if deterministic_issues:
            det_issues_text = "\n## ALREADY FOUND (include in output):\n"
            for issue in deterministic_issues:
                det_issues_text += f"- {issue.issue_id}: [{issue.priority.upper()}] {issue.problem} (target: {issue.target})\n"

        user_prompt = f"""Review this content and find issues.

## KEY POINTS TO CHECK
{kp_text}
{coverage_text}

## CONTENT TO REVIEW

{linkedin_text}

---

{twitter_text}

---

{newsletter_text}

{det_issues_text}

## YOUR TASK

Find SPECIFIC issues with the content. For each issue:

1. Identify the problem clearly
2. Explain why it matters
3. Give a specific suggestion to fix it

Check for:
1. COVERAGE: Are critical KPs ({critical_kps}) used? Any missing?
2. CONSTRAINTS: Tweets ≤240 chars? LinkedIn has hook?
3. STRUCTURE: Good hook? Clear flow? Proper sections?
4. CLARITY: Any repetition? Weak phrasing?

Return JSON with issues array. Include any deterministic issues found above."""

        result = self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            output_schema=ReviewOutput,
            temperature=0.3,
        )

        # Merge deterministic issues
        result = self._merge_issues(result, deterministic_issues)

        return result

    def _run_deterministic_checks(
        self,
        formatted: FormattedOutput,
        summary: SummaryOutput,
    ) -> List[ReviewIssue]:
        """Run rule-based checks that don't need LLM."""
        issues = []
        issue_count = 0
        
        # Check tweet lengths
        for i, tweet in enumerate(formatted.twitter.tweets):
            if len(tweet) > 240:
                issue_count += 1
                issues.append(ReviewIssue(
                    issue_id=f"issue_{issue_count}",
                    target="twitter",
                    type="constraint",
                    problem=f"Tweet {i+1} too long ({len(tweet)} chars)",
                    reason="Exceeds 240 character limit",
                    suggestion=f"Shorten tweet {i+1} to under 240 characters",
                    priority="critical",
                    missing_kps=[]
                ))
        
        # Check tweet count
        if len(formatted.twitter.tweets) > 7:
            issue_count += 1
            issues.append(ReviewIssue(
                issue_id=f"issue_{issue_count}",
                target="twitter",
                type="constraint",
                problem=f"Too many tweets ({len(formatted.twitter.tweets)})",
                reason="Maximum 7 tweets allowed",
                suggestion="Reduce to 7 tweets by combining ideas",
                priority="high",
                missing_kps=[]
            ))
        
        # Check coverage
        kp_ids = [kp.id for kp in summary.key_points]
        critical_kps = [kp.id for kp in summary.key_points if kp.priority == "critical"]
        
        all_used = set(
            formatted.linkedin.used_kps +
            formatted.twitter.used_kps +
            formatted.newsletter.used_kps
        )
        
        missing_critical = [kp for kp in critical_kps if kp not in all_used]
        if missing_critical:
            issue_count += 1
            issues.append(ReviewIssue(
                issue_id=f"issue_{issue_count}",
                target="linkedin",  # Start with LinkedIn
                type="coverage",
                problem="Missing critical key points",
                reason="Critical KPs must be included in content",
                suggestion=f"Add content covering: {', '.join(missing_critical)}",
                priority="critical",
                missing_kps=missing_critical
            ))
        
        # Check LinkedIn length (rough check)
        linkedin_words = len(formatted.linkedin.content.split())
        if linkedin_words < 80:
            issue_count += 1
            issues.append(ReviewIssue(
                issue_id=f"issue_{issue_count}",
                target="linkedin",
                type="constraint",
                problem=f"LinkedIn too short ({linkedin_words} words)",
                reason="LinkedIn posts should be 100-150 words",
                suggestion="Expand the post with more details from key points",
                priority="high",
                missing_kps=[]
            ))
        elif linkedin_words > 180:
            issue_count += 1
            issues.append(ReviewIssue(
                issue_id=f"issue_{issue_count}",
                target="linkedin",
                type="constraint",
                problem=f"LinkedIn too long ({linkedin_words} words)",
                reason="LinkedIn posts should be 100-150 words",
                suggestion="Trim the post to focus on most important points",
                priority="medium",
                missing_kps=[]
            ))
        
        # Check LinkedIn structure - BULLET DUMP detection (NEW)
        bullet_indicators = ['•', '→', '- ', '1.', '2.', '3.', '* ']
        bullet_count = sum(formatted.linkedin.content.count(ind) for ind in bullet_indicators)
        
        if bullet_count >= 3:
            issue_count += 1
            issues.append(ReviewIssue(
                issue_id=f"issue_{issue_count}",
                target="linkedin",
                type="structure",
                problem="Content is a bullet dump, not narrative",
                reason="Bullet lists feel like summaries, not lived insight. They reduce engagement.",
                suggestion="Rewrite as narrative: 'Most teams get this wrong. They [problem]. What changed was [shift]...'",
                priority="high",
                missing_kps=[]
            ))
        
        # Check LinkedIn structure - weak hook detection
        linkedin_content = formatted.linkedin.content.lower()
        weak_hook_patterns = [
            "did you know",
            "have you ever",
            "is your",
            "are you",
            "in today's",
            "it's important to",
            "many people",
            "we all know",
            "here's how",
            "here's what",
            "unlock",
            "transform your",
            "the best teams"
        ]
        
        first_line = formatted.linkedin.content.split('\n')[0].lower()
        for pattern in weak_hook_patterns:
            if first_line.startswith(pattern) or pattern in first_line[:50]:
                issue_count += 1
                # Find a data point to suggest
                data_kp = next((kp for kp in summary.key_points if kp.data), None)
                suggestion = "Lead with a specific data point"
                if data_kp:
                    suggestion = f"Lead with: '{data_kp.data}' from {data_kp.label}"
                
                issues.append(ReviewIssue(
                    issue_id=f"issue_{issue_count}",
                    target="linkedin",
                    type="structure",
                    problem="Weak hook - starts with generic pattern",
                    reason=f"'{pattern}' openings don't stop the scroll",
                    suggestion=suggestion,
                    priority="high",
                    missing_kps=[]
                ))
                break
        
        # Check newsletter for "In conclusion"
        if "in conclusion" in formatted.newsletter.content.lower():
            issue_count += 1
            issues.append(ReviewIssue(
                issue_id=f"issue_{issue_count}",
                target="newsletter",
                type="structure",
                problem="Uses 'In conclusion'",
                reason="Generic closing phrase reduces quality",
                suggestion="Replace with actionable takeaway without 'In conclusion'",
                priority="medium",
                missing_kps=[]
            ))
        
        # Check for cause-effect in LinkedIn (should have "because", "so that", etc.)
        cause_effect_indicators = ['because', 'so that', 'which means', 'the result', 'that\'s why']
        has_cause_effect = any(ind in linkedin_content for ind in cause_effect_indicators)
        
        if not has_cause_effect and bullet_count < 3:  # Only flag if not already bullet dump
            issue_count += 1
            issues.append(ReviewIssue(
                issue_id=f"issue_{issue_count}",
                target="linkedin",
                type="clarity",
                problem="Missing cause-effect explanations",
                reason="Content states WHAT but not WHY. Insights need explanation.",
                suggestion="Add 'because' or 'which means' to explain why each insight matters",
                priority="medium",
                missing_kps=[]
            ))
        
        return issues

    def _merge_issues(
        self,
        result: ReviewOutput,
        deterministic_issues: List[ReviewIssue]
    ) -> ReviewOutput:
        """Merge deterministic issues with LLM-found issues."""
        # Get existing issue IDs to avoid duplicates
        existing_ids = {issue.issue_id for issue in result.issues}
        
        # Add deterministic issues that aren't already present
        for det_issue in deterministic_issues:
            # Check if similar issue exists
            is_duplicate = any(
                issue.target == det_issue.target and 
                issue.type == det_issue.type and
                issue.problem.lower() in det_issue.problem.lower() or 
                det_issue.problem.lower() in issue.problem.lower()
                for issue in result.issues
            )
            
            if not is_duplicate and det_issue.issue_id not in existing_ids:
                result.issues.append(det_issue)
        
        # Re-number issues
        for i, issue in enumerate(result.issues):
            issue.issue_id = f"issue_{i + 1}"
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        result.issues.sort(key=lambda x: priority_order.get(x.priority, 4))
        
        return result
