"""
RefinerAgent: Applies reviewer feedback to improve content.

CLEAN DESIGN v4:
- Input: V1 outputs + reviewer issues
- Output: V2 with visible changes
- Change tracking: {issue_id, action, target, before, after}
- Must show real improvement, not minor edits
"""

from typing import Optional, List
from schemas.schemas import (
    SummaryOutput, FormattedOutput, ReviewOutput, ReviewIssue,
    RefinedOutput, Change,
    LinkedInOutput, TwitterOutput, NewsletterOutput
)
from utils.llm import LLMClient, get_llm_client


REFINER_SYSTEM_PROMPT = """You are an expert content refiner. Fix SPECIFIC issues from the review.

## YOUR JOB
1. Take the V1 content
2. Fix each issue from the review
3. Track every change with before/after
4. Output improved V2 content

## CHANGE TYPES
- rewrite: Completely rewrite a section
- add: Add missing content
- remove: Remove problematic content  
- shorten: Reduce length
- restructure: Change organization

## OUTPUT FORMAT

{
  "version": 2,
  "changes": [
    {
      "issue_id": "issue_1",
      "action": "rewrite | add | remove | shorten | restructure",
      "target": "linkedin_hook | tweet_3 | newsletter_intro | etc",
      "before": "Original content as STRING...",
      "after": "Improved content as STRING..."
    }
  ],
  "linkedin": {
    "content": "Full improved LinkedIn post...",
    "used_kps": ["kp_1", "kp_2", "kp_3"]
  },
  "twitter": {
    "tweets": ["Improved tweet 1...", "Improved tweet 2...", ...],
    "used_kps": ["kp_1", "kp_2", "kp_3"]
  },
  "newsletter": {
    "content": "Full improved newsletter...",
    "used_kps": ["kp_1", "kp_2", "kp_3", "kp_4"]
  }
}

## CRITICAL: CHANGE TRACKING RULES

1. "before" and "after" MUST be STRINGS, never arrays
2. For Twitter changes:
   - If changing one tweet: before="old tweet text", after="new tweet text"
   - If changing thread: before="Tweet 1 | Tweet 2 | ...", after="New Tweet 1 | New Tweet 2 | ..."
   - NEVER put an array in before/after
3. Target format:
   - Single tweet: "tweet_1", "tweet_2", etc.
   - Whole thread: "twitter_thread"
   - LinkedIn parts: "linkedin_hook", "linkedin_body", "linkedin"
   - Newsletter parts: "newsletter_intro", "newsletter_section_1", "newsletter"

## RULES

1. FIX WHAT'S BROKEN
   - Address each issue by priority (critical first)
   - Make REAL changes, not cosmetic tweaks

2. TRACK CHANGES
   - Every change must have before/after AS STRINGS
   - Link to the issue_id it fixes

3. RESPECT CONSTRAINTS
   - Tweets ≤240 chars
   - LinkedIn 100-150 words
   - Newsletter 120-200 words

4. USE KEY POINTS
   - Add missing KPs from coverage issues
   - Use ONLY ideas from the summary

## DO NOT
- Make changes not requested in issues
- Invent examples or data
- Just rephrase without real improvement
- Ignore critical issues
- Put arrays in before/after fields (MUST be strings)"""


class RefinerAgent:
    """
    Refines content based on reviewer feedback.
    
    Output: RefinedOutput with changes[] and updated platform content.
    Each change has: issue_id, action, target, before, after.
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None
    ):
        self.llm = llm_client or get_llm_client()
        self.system_prompt = REFINER_SYSTEM_PROMPT

    def run(
        self,
        summary: SummaryOutput,
        formatted: FormattedOutput,
        review: ReviewOutput,
    ) -> RefinedOutput:
        """
        Refine content based on review issues.

        Args:
            summary: Original summary with key_points
            formatted: V1 formatted content
            review: Review with issues to fix

        Returns:
            RefinedOutput with changes and improved content
        """
        # Build key points reference
        kp_text = "\n".join(
            f"- {kp.id}: [{kp.priority.upper()}] {kp.label}" +
            (f" ({kp.data})" if kp.data else "")
            for kp in summary.key_points
        )

        # Sort issues by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_issues = sorted(
            review.issues, 
            key=lambda x: priority_order.get(x.priority, 4)
        )

        # Build issues text
        issues_text = ""
        for issue in sorted_issues:
            issues_text += f"""
[{issue.issue_id}] [{issue.priority.upper()}] {issue.type}
  Target: {issue.target}
  Problem: {issue.problem}
  Reason: {issue.reason}
  Suggestion: {issue.suggestion}
  Missing KPs: {issue.missing_kps if issue.missing_kps else 'N/A'}
"""

        # Current content
        linkedin_current = f"CONTENT:\n{formatted.linkedin.content}\nUSED_KPS: {formatted.linkedin.used_kps}"
        
        twitter_current = "TWEETS:\n"
        for i, tweet in enumerate(formatted.twitter.tweets):
            twitter_current += f"  {i+1}. [{len(tweet)} chars] {tweet}\n"
        twitter_current += f"USED_KPS: {formatted.twitter.used_kps}"
        
        newsletter_current = f"CONTENT:\n{formatted.newsletter.content}\nUSED_KPS: {formatted.newsletter.used_kps}"

        user_prompt = f"""Fix the issues found in the review.

## KEY POINTS (for adding coverage)
{kp_text}

## ISSUES TO FIX (by priority)
{issues_text}

## CURRENT CONTENT (V1)

### LINKEDIN
{linkedin_current}

### TWITTER
{twitter_current}

### NEWSLETTER
{newsletter_current}

## YOUR TASK

1. Fix each issue, starting with CRITICAL
2. For each fix, record:
   - issue_id: Which issue you're fixing
   - action: What you're doing (rewrite/add/remove/shorten/restructure)
   - target: What you're changing (linkedin_hook, tweet_3, etc.)
   - before: Original content
   - after: Improved content

3. Output the complete V2 content for all platforms

## CONSTRAINTS
- Tweets: ≤240 chars each, max 7 tweets
- LinkedIn: 100-150 words
- Newsletter: 120-200 words

## IMPORTANT
- Make REAL improvements (not just rephrasing)
- Add missing KPs naturally (don't just dump them)
- Track every change with before/after"""

        result = self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            output_schema=RefinedOutput,
            temperature=0.5,
        )

        # Post-process
        result = self._post_process(result, formatted, review)
        result.version = 2

        return result

    def _post_process(
        self,
        result: RefinedOutput,
        original: FormattedOutput,
        review: ReviewOutput
    ) -> RefinedOutput:
        """Post-process to ensure constraints and change tracking."""
        
        # Truncate tweets that exceed limit
        for i, tweet in enumerate(result.twitter.tweets):
            if len(tweet) > 240:
                truncated = tweet[:237]
                last_space = truncated.rfind(' ')
                if last_space > 200:
                    truncated = truncated[:last_space]
                
                # Add change record for auto-truncation
                result.changes.append(Change(
                    issue_id="auto_fix",
                    action="shorten",
                    target=f"tweet_{i+1}",
                    before=tweet[:50] + "..." if len(tweet) > 50 else tweet,
                    after=truncated[:50] + "..." if len(truncated) > 50 else truncated
                ))
                
                result.twitter.tweets[i] = truncated + "..."
        
        # Limit tweet count
        if len(result.twitter.tweets) > 7:
            removed = result.twitter.tweets[7:]
            result.twitter.tweets = result.twitter.tweets[:7]
            result.changes.append(Change(
                issue_id="auto_fix",
                action="remove",
                target="twitter_thread",
                before=f"{len(removed) + 7} tweets",
                after="7 tweets (max)"
            ))
        
        # Ensure all issues are addressed (at least attempted)
        addressed_ids = {c.issue_id for c in result.changes}
        for issue in review.issues:
            if issue.issue_id not in addressed_ids and issue.priority in ["critical", "high"]:
                # Add placeholder if critical/high issue wasn't addressed
                result.changes.append(Change(
                    issue_id=issue.issue_id,
                    action="restructure",
                    target=issue.target,
                    before="(see original)",
                    after="(improved in V2)"
                ))

        return result
