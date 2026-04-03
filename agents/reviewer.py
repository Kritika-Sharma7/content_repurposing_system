"""
ReviewerAgent: Evaluates outputs and generates actionable feedback.

HYBRID DESIGN v2:
- Coverage + Quality: LLM evaluates each KP per format
- Python: Creates issues based on LLM evaluation
- Python: Deduplication, prioritization, limits
"""

from typing import Optional, List, Tuple, Dict
from pydantic import BaseModel
from schemas.schemas import (
    SummaryOutput, FormattedOutput, ReviewOutput, ReviewIssue, ReviewSummary, KeyPoint
)
from utils.llm import LLMClient, get_llm_client


# Internal schema for per-KP evaluation
class KPEvaluation(BaseModel):
    """Evaluation of a single key point in a single format."""
    kp_id: str
    present: bool  # Is the idea expressed in this format?
    quality: str   # "strong", "weak", or "missing"
    reason: str    # Brief explanation


class FormatEvaluation(BaseModel):
    """Evaluation of all key points in a single format."""
    format_name: str
    evaluations: List[KPEvaluation]


class ContentEvaluation(BaseModel):
    """Complete evaluation of all formats."""
    linkedin: List[KPEvaluation]
    twitter: List[KPEvaluation]
    newsletter: List[KPEvaluation]
    clarity_issues: List[str]  # General clarity problems (not KP-specific)
    consistency_issue: Optional[str]  # Contradiction if any


EVALUATION_PROMPT = """You are a content reviewer. Your job is to evaluate each key point in each format.

## YOUR TASK

For EACH key point, in EACH format (LinkedIn, Twitter, Newsletter):

1. Is this key point's idea PRESENT in the content? (yes/no)
2. If present, what is the QUALITY?
   - "strong" = explained clearly with cause-effect, concrete details
   - "weak" = mentioned briefly, vague, abstract, or buried in other content
   - "missing" = idea is not expressed at all

## EVALUATION CRITERIA

A key point is PRESENT if its core idea is expressed. Look for:
- The concept being discussed (not just keywords)
- The insight or claim being made

A key point is STRONG if:
- It has clear cause-effect explanation
- It's given appropriate emphasis
- It uses concrete language

A key point is WEAK if:
- It's mentioned but not explained
- It's buried inside another idea
- It uses vague/abstract language
- It feels like a throwaway mention

## ALSO CHECK

1. **Clarity Issues**: Flag any abstract/academic phrasing that lacks intuitive explanation
2. **Consistency Issues**: Flag ONLY if formats contradict each other (rare)

## OUTPUT FORMAT

Return JSON:
{
  "linkedin": [
    {"kp_id": "kp_1", "present": true, "quality": "strong", "reason": "..."},
    {"kp_id": "kp_2", "present": true, "quality": "weak", "reason": "..."},
    {"kp_id": "kp_3", "present": false, "quality": "missing", "reason": "..."}
  ],
  "twitter": [...],
  "newsletter": [...],
  "clarity_issues": ["specific issue description if any"],
  "consistency_issue": null
}

Be STRICT. If a key point is not clearly expressed, mark it as missing or weak.
Do NOT assume presence just because a related word appears."""


class ReviewerAgent:
    """
    Evaluates formatted content using LLM-based per-KP evaluation.
    
    Design:
    1. LLM evaluates each KP in each format (present/missing, strong/weak)
    2. Python creates issues based on evaluation results
    3. Python handles deduplication, priority, and limits
    """

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None
    ):
        self.llm = llm_client or get_llm_client()

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
            ReviewOutput with list of actionable issues (max 3)
        """
        # Build KP lookup for priority checks
        kp_lookup: Dict[str, KeyPoint] = {kp.id: kp for kp in summary.key_points}
        
        # --- STEP 1: LLM evaluates each KP in each format ---
        evaluation = self._evaluate_content(summary, formatted)
        
        if evaluation is None:
            # LLM failed, return empty review
            return self._create_empty_review()
        
        # --- STEP 2: Create issues based on evaluation ---
        issues: List[ReviewIssue] = []
        
        # Process missing/weak KPs per format
        format_evals = {
            "linkedin": evaluation.linkedin,
            "twitter": evaluation.twitter,
            "newsletter": evaluation.newsletter,
        }
        
        # Track missing KPs across formats
        missing_kps: Dict[str, List[str]] = {}  # kp_id -> [formats]
        weak_kps: Dict[str, List[str]] = {}     # kp_id -> [formats]
        
        for fmt_name, kp_evals in format_evals.items():
            for kp_eval in kp_evals:
                kp_id = kp_eval.kp_id
                if kp_eval.quality == "missing" or not kp_eval.present:
                    if kp_id not in missing_kps:
                        missing_kps[kp_id] = []
                    missing_kps[kp_id].append(fmt_name)
                elif kp_eval.quality == "weak":
                    if kp_id not in weak_kps:
                        weak_kps[kp_id] = []
                    weak_kps[kp_id].append(fmt_name)
        
        # Create coverage issues for missing KPs
        for kp_id, formats in missing_kps.items():
            kp = kp_lookup.get(kp_id)
            if kp:
                issue = self._create_coverage_issue(kp, formats)
                if issue:
                    issues.append(issue)
        
        # Create clarity issues for weak KPs (only critical/high priority)
        for kp_id, formats in weak_kps.items():
            kp = kp_lookup.get(kp_id)
            if kp and kp.priority in ("critical", "high"):
                issue = self._create_weak_issue(kp, formats)
                if issue:
                    issues.append(issue)
        
        # Add general clarity issues
        for clarity_problem in evaluation.clarity_issues[:1]:  # Limit to 1
            issues.append(ReviewIssue(
                issue_id="",
                type="clarity",
                priority="medium",
                problem=clarity_problem,
                reason="Content uses abstract or unclear phrasing.",
                suggestion="Use concrete language with cause-effect explanation.",
                affects=["linkedin", "twitter", "newsletter"],
                missing_kps=[]
            ))
        
        # Add consistency issue if any
        if evaluation.consistency_issue:
            issues.append(ReviewIssue(
                issue_id="",
                type="consistency",
                priority="high",
                problem=evaluation.consistency_issue,
                reason="Formats contain contradictory information.",
                suggestion="Ensure consistent messaging across all formats.",
                affects=["linkedin", "twitter", "newsletter"],
                missing_kps=[]
            ))
        
        # --- STEP 3: Finalize ---
        return self._finalize_issues(issues)

    def _evaluate_content(
        self,
        summary: SummaryOutput,
        formatted: FormattedOutput,
    ) -> Optional[ContentEvaluation]:
        """
        Use LLM to evaluate each KP in each format.
        Returns structured evaluation or None if LLM fails.
        """
        # Build content text
        linkedin_text = f"LINKEDIN:\n{formatted.linkedin.content}"
        
        twitter_text = "TWITTER:\n"
        for i, tweet in enumerate(formatted.twitter.tweets):
            twitter_text += f"{i+1}. {tweet}\n"
        
        newsletter_text = f"NEWSLETTER:\n{formatted.newsletter.content}"

        # Build key points list
        kp_entries = []
        for kp in summary.key_points:
            entry = f"- **{kp.id}** [{kp.priority.upper()}]: {kp.label}"
            if kp.data:
                entry += f" (Data: {kp.data})"
            kp_entries.append(entry)
        kp_text = "\n".join(kp_entries)

        user_prompt = f"""## CONTENT TO EVALUATE

{linkedin_text}

---

{twitter_text}

---

{newsletter_text}

---

## CORE MESSAGE
{summary.core_message}

---

## KEY POINTS TO CHECK

{kp_text}

---

## YOUR TASK

For EACH key point listed above, evaluate its presence and quality in EACH format.

Be STRICT:
- If a key point is only vaguely mentioned, mark as "weak"
- If a key point's core idea is not expressed, mark as "missing"
- Don't assume presence just because related words appear

Return the evaluation JSON."""

        try:
            result = self.llm.generate(
                system_prompt=EVALUATION_PROMPT,
                user_prompt=user_prompt,
                output_schema=ContentEvaluation,
                temperature=0.2,
            )
            return result
        except Exception:
            return None

    def _create_coverage_issue(
        self, 
        kp: KeyPoint, 
        missing_formats: List[str]
    ) -> Optional[ReviewIssue]:
        """
        Create a coverage issue based on key point priority and missing formats.
        
        Rules:
        - critical + missing anywhere → CRITICAL issue
        - high + missing in 2+ formats → HIGH issue
        - medium + missing in 2+ formats → MEDIUM issue
        """
        num_missing = len(missing_formats)
        
        if kp.priority == "critical" and num_missing >= 1:
            priority = "critical"
        elif kp.priority == "high" and num_missing >= 2:
            priority = "high"
        elif kp.priority == "medium" and num_missing >= 2:
            priority = "medium"
        else:
            return None

        formats_str = ", ".join(missing_formats)
        
        return ReviewIssue(
            issue_id="",
            type="coverage",
            priority=priority,
            problem=f"{kp.label} is missing in: {formats_str}",
            reason=f"This {kp.priority}-priority insight is not represented in {num_missing} format(s), leading to inconsistent messaging.",
            suggestion=f"Ensure '{kp.label}' is clearly included in: {formats_str}.",
            affects=missing_formats,
            missing_kps=[kp.id]
        )

    def _create_weak_issue(
        self, 
        kp: KeyPoint, 
        weak_formats: List[str]
    ) -> Optional[ReviewIssue]:
        """
        Create a clarity issue for weakly expressed key point.
        
        Rules:
        - critical KP weak → HIGH priority
        - high KP weak → MEDIUM priority
        """
        if kp.priority == "critical":
            priority = "high"
        elif kp.priority == "high":
            priority = "medium"
        else:
            return None  # Don't flag medium priority KPs

        formats_str = ", ".join(weak_formats)
        
        return ReviewIssue(
            issue_id="",
            type="clarity",
            priority=priority,
            problem=f"'{kp.label}' is weakly expressed in: {formats_str}",
            reason=f"This {kp.priority}-priority key point is mentioned but not explained with sufficient clarity or cause-effect.",
            suggestion=f"Strengthen the explanation of '{kp.label}' with concrete details and cause-effect reasoning.",
            affects=weak_formats,
            missing_kps=[kp.id]
        )

    def _create_empty_review(self) -> ReviewOutput:
        """Create empty review when LLM fails."""
        return ReviewOutput(
            issues=[],
            summary=ReviewSummary(total_issues=0, critical=0, high=0, medium=0),
            status="ok"
        )

    def _finalize_issues(self, issues: List[ReviewIssue]) -> ReviewOutput:
        """Sort, deduplicate, limit, and finalize issues."""
        # Deduplicate issues (same type + affects + missing_kps)
        seen = set()
        unique_issues = []
        for issue in issues:
            key = (
                issue.type,
                tuple(sorted(issue.affects)) if issue.affects else (),
                tuple(sorted(issue.missing_kps)) if issue.missing_kps else ()
            )
            if key not in seen:
                seen.add(key)
                unique_issues.append(issue)
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2}
        unique_issues.sort(key=lambda x: priority_order.get(x.priority, 3))
        
        # Limit to max 3 issues
        unique_issues = unique_issues[:3]
        
        # Assign issue IDs
        for i, issue in enumerate(unique_issues):
            issue.issue_id = f"issue_{i + 1}"
        
        # Build summary
        summary = ReviewSummary(
            total_issues=len(unique_issues),
            critical=len([i for i in unique_issues if i.priority == "critical"]),
            high=len([i for i in unique_issues if i.priority == "high"]),
            medium=len([i for i in unique_issues if i.priority == "medium"])
        )
        
        # Determine status
        status = "needs_fixes" if unique_issues else "ok"
        
        return ReviewOutput(
            issues=unique_issues,
            summary=summary,
            status=status
        )