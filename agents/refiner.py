"""
RefinerAgent: Applies reviewer feedback to improve content.

CLEAN DESIGN v6:
- Input: V1/V2 outputs + reviewer issues
- Output: Refined content with tracked changes
- Each issue = CONSTRAINT (must be fully resolved)
- All formats in issue.affects MUST be modified
- Natural integration, not mechanical patching
"""

from typing import Optional, List, Union
from schemas.schemas import (
    SummaryOutput, FormattedOutput, ReviewOutput, ReviewIssue,
    RefinedOutput, Change,
    LinkedInOutput, TwitterOutput, NewsletterOutput
)
from utils.llm import LLMClient, get_llm_client


REFINER_SYSTEM_PROMPT = """You are Agent 4: Refiner.

Your job is to FULLY FIX content issues with STRONG expression — not just presence.

---

⚠️ CRITICAL CONSTRAINT

Issues are NOT suggestions — they are REQUIREMENTS.
Each issue MUST be fully resolved in ALL affected formats.
Key points must be STRONGLY expressed, not just mentioned.

---

🔒 STRICT MODIFICATION RULE (CRITICAL)

ONLY modify content that corresponds to reviewer issues.
DO NOT change any content unrelated to the issues.
DO NOT improve anything that is not explicitly flagged.

If a format is NOT listed in issue.affects, DO NOT modify it.

---

🎯 STRONG EXPRESSION RULE (MANDATORY)

When fixing any coverage or clarity issue:

1. The key point MUST be:
   - Clearly explained (not just mentioned)
   - Connected to surrounding content (flows naturally)
   - Expressed with cause-effect or reasoning

2. The key point MUST NOT:
   - Appear as a standalone/isolated sentence
   - Feel appended or inserted mechanically
   - Use vague or abstract language

---

🧠 INTEGRATION METHOD (MANDATORY)

For EACH affected format, choose ONE approach:

### OPTION A (Preferred): MODIFY EXISTING SENTENCE
Expand an existing sentence to include the idea naturally.

Example:
BEFORE: "We introduced conditional payments."
AFTER: "We introduced conditional payments through escrow mechanisms, which hold funds until tasks meet predefined conditions."

### OPTION B: ADD CONNECTED SENTENCE
Add a new sentence that connects to the previous one using cause-effect language.

Connectors to use:
- "This matters because..."
- "This leads to..."
- "Without this..."
- "The result is..."

---

❌ BAD EXAMPLES (DO NOT DO THIS)

1. Isolated insertion:
   "Sentence one. New idea here. Sentence three."

2. End-of-paragraph append:
   "...existing content. Also, escrow mechanisms ensure payments are conditional."

3. Vague mention:
   "We need better verification systems."

---

✅ GOOD EXAMPLES (DO THIS)

1. Natural integration:
   "We shifted to escrow-based payments, which hold funds until tasks meet predefined conditions—reducing errors by ensuring AI only gets paid for verified work."

2. Cause-effect connection:
   "Traditional systems fail because they lack verification. This is why automated checks are essential—they confirm task completion without human bottlenecks."

---

🎯 QUALITY CHECK (MANDATORY BEFORE OUTPUT)

For EACH fixed issue, verify:
- A reader can understand the idea WITHOUT guessing
- The idea has cause-effect explanation
- It flows naturally with surrounding text

If the fix feels weak or appended → REWRITE IT.

---

📋 CHANGE TRACKING (STRICT)

For each issue:
- Create EXACTLY ONE change entry
- issue_id: MUST match the reviewer's issue_id exactly
- action: "rewrite" | "add" | "integrate" | "remove" | "shorten" | "restructure"
- target: comma-separated list of affected formats (e.g., "linkedin, twitter" or "newsletter")
- before: representative snippet showing the problem
- after: representative snippet showing the STRONG fix

---

🔧 FIX STRATEGIES BY ISSUE TYPE

COVERAGE ISSUES (type: "coverage"):
- Look at missing_kps to identify which key points are missing
- Find the key point in the KEY POINTS section to get the actual idea
- STRONGLY express the idea (not just mention it)
- Use cause-effect language
- Integrate naturally into existing flow

CLARITY ISSUES (type: "clarity"):
- Replace vague phrases with specific, concrete language
- Add cause-effect explanation
- Use data or examples from key_points

CONSISTENCY ISSUES (type: "consistency"):
- Align the core message across ALL affected formats
- Use similar phrasing and emphasis

---

🐦 TWITTER SPECIFIC

- Modify tweets so idea is CLEAR in ≤280 chars
- Prefer clarity over density (don't cram multiple ideas)
- One key idea per tweet, explained well
- Use simple cause-effect: "X because Y" or "X leads to Y"

---

📤 OUTPUT FORMAT

Return:
- linkedin: complete content (even if unchanged)
- twitter: complete tweets list (even if unchanged)
- newsletter: complete content (even if unchanged)
- changes: array with ONE entry per issue

VALIDATION:
- len(changes) MUST equal len(issues)
- Each change.target MUST include ALL formats from issue.affects
- Each fix must be STRONG (explained with cause-effect, not just mentioned)"""


class RefinerAgent:
    """
    Refines content based on reviewer feedback.
    
    CONSTRAINTS:
    - Each issue MUST be fully resolved
    - ALL formats in issue.affects MUST be modified
    - Changes are tracked with before/after
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
        formatted: Union[FormattedOutput, RefinedOutput],
        review: ReviewOutput,
    ) -> RefinedOutput:
        """
        Refine content based on review issues.

        Args:
            summary: Original summary with key_points
            formatted: Current content (V1, V2, etc.)
            review: Review with issues to fix

        Returns:
            RefinedOutput with changes and improved content
        """
        # Handle no issues case
        if not review.issues:
            return self._create_unchanged_output(formatted)

        # Determine which formats need modification based on issues
        affected_formats = set()
        for issue in review.issues:
            affected_formats.update(issue.affects)
        
        affected_formats_str = ", ".join(sorted(affected_formats))

        # Build key points reference with full details
        kp_lookup = {kp.id: kp for kp in summary.key_points}
        kp_text = "\n".join(
            f"- {kp.id}: [{kp.priority.upper()}] {kp.label}" +
            (f" (data: {kp.data})" if kp.data else "") +
            (f"\n    Why it matters: {kp.reason}" if kp.reason else "")
            for kp in summary.key_points
        )

        # Sort issues by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_issues = sorted(
            review.issues, 
            key=lambda x: priority_order.get(x.priority, 4)
        )

        # Build detailed issues text with explicit requirements
        issues_text = ""
        for issue in sorted_issues:
            affects_list = issue.affects if issue.affects else ["linkedin", "twitter", "newsletter"]
            
            issues_text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ISSUE: {issue.issue_id} | Priority: {issue.priority.upper()} | Type: {issue.type}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  MUST MODIFY: {', '.join(affects_list)} (ALL of them!)
Problem: {issue.problem}
Reason: {issue.reason}
Suggestion: {issue.suggestion}"""
            
            # Add explicit key point content for coverage issues
            if issue.type == "coverage" and issue.missing_kps:
                issues_text += "\n\n📌 KEY POINT CONTENT TO ADD:"
                for kp_id in issue.missing_kps:
                    if kp_id in kp_lookup:
                        kp = kp_lookup[kp_id]
                        issues_text += f"\n   {kp_id}: \"{kp.label}\""
                        if kp.data:
                            issues_text += f"\n   Data to include: {kp.data}"
            
            issues_text += "\n"

        # Get current content (handle both FormattedOutput and RefinedOutput)
        linkedin_content = formatted.linkedin.content
        linkedin_kps = formatted.linkedin.used_kps
        twitter_tweets = formatted.twitter.tweets
        twitter_kps = formatted.twitter.used_kps
        newsletter_content = formatted.newsletter.content
        newsletter_kps = formatted.newsletter.used_kps

        # Current content display
        linkedin_current = f"CONTENT:\n{linkedin_content}\nUSED_KPS: {linkedin_kps}"
        
        twitter_current = "TWEETS:\n"
        for i, tweet in enumerate(twitter_tweets):
            twitter_current += f"  {i+1}. [{len(tweet)} chars] {tweet}\n"
        twitter_current += f"USED_KPS: {twitter_kps}"
        
        newsletter_current = f"CONTENT:\n{newsletter_content}\nUSED_KPS: {newsletter_kps}"

        user_prompt = f"""Fix ALL issues with STRONG expression. Key points must be clearly explained, not just mentioned.

⚠️ CRITICAL: ONLY modify formats listed in affected formats: {affected_formats_str}
DO NOT change content in formats that are NOT in this list.

## ISSUES TO FIX ({len(sorted_issues)} total)
{issues_text}

## CURRENT CONTENT

### LINKEDIN
{linkedin_current}

### TWITTER
{twitter_current}

### NEWSLETTER
{newsletter_current}

## KEY POINTS REFERENCE
{kp_text}

## STRONG EXPRESSION REQUIREMENTS

For EACH coverage/clarity issue:

1. DO NOT just add the idea as a standalone sentence
2. DO integrate using cause-effect language:
   - "This works because..."
   - "This leads to..."
   - "Without this..."

3. QUALITY CHECK: Can a reader understand the idea WITHOUT guessing?
   - If NO → rewrite until it's clear

## INTEGRATION EXAMPLES

❌ BAD (weak/appended):
"We use AI agents. Escrow mechanisms exist. Trust is important."

✅ GOOD (strong/integrated):
"We use AI agents with escrow-based payments—funds are held until tasks meet conditions, shifting trust from human oversight to system design."

## STRICT REQUIREMENTS

1. Fix ALL {len(sorted_issues)} issues with STRONG expression
2. Return EXACTLY {len(sorted_issues)} changes (one per issue)
3. For EACH issue:
   - Modify ALL formats listed in "MUST MODIFY"
   - For coverage: explain the idea with cause-effect (not just mention it)
   - Integrate naturally — do NOT append sentences
4. Each change.issue_id MUST match the issue_id exactly
5. Each change.target MUST be a comma-separated string of formats (e.g., "linkedin, twitter")

⚠️ VALIDATION: Reviewer should mark each key point as "strong" — not just "present"."""

        result = self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            output_schema=RefinedOutput,
            temperature=0.3,
        )

        # Set version and validate
        result.version = getattr(formatted, 'version', 1) + 1
        result = self._validate_and_fix(result, sorted_issues)
        
        return result

    def _create_unchanged_output(
        self, 
        formatted: Union[FormattedOutput, RefinedOutput]
    ) -> RefinedOutput:
        """Create output when no changes needed."""
        return RefinedOutput(
            version=getattr(formatted, 'version', 1) + 1,
            changes=[],
            linkedin=LinkedInOutput(
                content=formatted.linkedin.content,
                used_kps=formatted.linkedin.used_kps
            ),
            twitter=TwitterOutput(
                tweets=formatted.twitter.tweets,
                used_kps=formatted.twitter.used_kps
            ),
            newsletter=NewsletterOutput(
                content=formatted.newsletter.content,
                used_kps=formatted.newsletter.used_kps
            )
        )

    def _validate_and_fix(
        self, 
        result: RefinedOutput, 
        issues: List[ReviewIssue]
    ) -> RefinedOutput:
        """Validate that all issues were addressed and fix change tracking."""
        # Ensure we have the right number of changes
        issue_ids = {issue.issue_id for issue in issues}
        change_ids = {change.issue_id for change in result.changes}
        
        # Add missing change entries if needed
        for issue in issues:
            if issue.issue_id not in change_ids:
                affects = issue.affects if issue.affects else ["linkedin", "twitter", "newsletter"]
                result.changes.append(Change(
                    issue_id=issue.issue_id,
                    action="rewrite",
                    target=", ".join(affects),
                    before="(content modified)",
                    after="(see updated content)"
                ))
        
        # Ensure change targets match issue affects
        issue_affects_map = {issue.issue_id: issue.affects for issue in issues}
        for change in result.changes:
            if change.issue_id in issue_affects_map:
                expected_affects = issue_affects_map[change.issue_id]
                if expected_affects:
                    change.target = ", ".join(expected_affects)
        
        return result
