"""
SummarizerAgent: Extracts core_message + key_points from raw content.

CLEAN DESIGN v4:
- Output ONLY: core_message + key_points (5-7 max)
- KeyPoint: id, label, priority, type, data (optional)
- Priority distribution: 2-3 critical, rest high/medium
- NO: intent, tone, audience, conflict, scores
"""

from typing import Optional, List
from schemas.schemas import SummaryOutput, KeyPoint
from utils.llm import LLMClient, get_llm_client
from config.user_preferences import UserPreferences, DEFAULT_USER_PREFERENCES


SUMMARIZER_SYSTEM_PROMPT = """You are Agent 1: Summarizer.

Your job is NOT to summarize text.
Your job is to extract high-quality, decision-grade insights.

---

INPUT:
Long-form content

---

OUTPUT:
1. core_message (1–2 sentences)
2. key_points (5–6 insights)

---

CORE MESSAGE RULE:
- Identify the central conflict or misconception
- Make it sharp and opinionated

Bad:
"Productivity improves with focus"

Good:
"Most teams mistake responsiveness for productivity, but constant activity reduces meaningful output"

---

KEY POINT RULES:

1. Each key point MUST be a complete insight sentence

Bad:
"Focus Time"
"Written Proposals"

Good:
"Reducing meetings and protecting focus time improves execution speed"

---

2. Use CAUSE → EFFECT

Example:
"Interruptions fragment work, which reduces output quality"

---

3. Integrate DATA into the insight

Bad:
"Reduced meetings impact"

Good:
"Reducing meetings improved execution speed (cycle time ↓ 30%)"

---

4. Include at least one NON-OBVIOUS insight:
- behavioral
- cultural
- misconception

---

5. Avoid vague language:
❌ improves, enhances, helps  
✅ reduces, creates, forces, enables

---

6. Prioritize quality over quantity:
Return only 5–6 strong insights

---

PRIORITY LOGIC:

CRITICAL:
- core conflict
- main mechanism
- strongest data-backed insight

HIGH:
- supporting insights

MEDIUM:
- edge cases / nuance

---

OUTPUT FORMAT:

{
  "core_message": "...",
  "key_points": [
    {
      "id": "kp_1",
      "label": "Complete insight sentence with cause-effect",
      "reason": "Why this insight matters or mechanism behind it",
      "priority": "critical",
      "type": "insight"
    }
  ]
}"""


class SummarizerAgent:
    """
    Extracts core_message + 5-6 HIGH-QUALITY key insights from content.
    
    Focus on conflict extraction, complete insight sentences, and cause-effect reasoning.
    Output: SummaryOutput with core_message and 5-6 key_points.
    Each KeyPoint has: id, label (complete sentence), reason, priority, type.
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        min_key_points: int = 5,
        max_key_points: int = 6,
        max_retries: int = 2
    ):
        self.llm = llm_client or get_llm_client()
        self.system_prompt = SUMMARIZER_SYSTEM_PROMPT
        self.min_key_points = min_key_points
        self.max_key_points = max_key_points
        self.max_retries = max_retries

    def run(
        self,
        content: str,
        user_preferences: Optional[UserPreferences] = None
    ) -> SummaryOutput:
        """
        Extract core_message + key_points from content.

        Args:
            content: Raw long-form text to summarize
            user_preferences: Optional preferences (used for context only)

        Returns:
            SummaryOutput with core_message and key_points
        """
        prefs = user_preferences or DEFAULT_USER_PREFERENCES
        word_count = len(content.split())
        
        # Retry loop for quality
        for attempt in range(self.max_retries + 1):
            result = self._extract(content, word_count, prefs, attempt)
            
            # Validate priority distribution
            critical_count = len([kp for kp in result.key_points if kp.priority == "critical"])
            
            if len(result.key_points) >= self.min_key_points and critical_count >= 2:
                return result
        
        return result

    def _extract(
        self,
        content: str,
        word_count: int,
        prefs: UserPreferences,
        attempt: int
    ) -> SummaryOutput:
        """Perform extraction attempt."""
        
        retry_note = ""
        if attempt > 0:
            retry_note = """
⚠️ RETRY: Previous attempt had issues. This time:
- Ensure 5-6 HIGH-QUALITY insights only
- Include 2-3 CRITICAL priority points
- Each label must be a COMPLETE SENTENCE with cause-effect  
- Capture the main conflict/misconception
- Include non-obvious insights (behavioral/cultural)
- Integrate data into insights, don't separate
"""

        user_prompt = f"""Extract decision-grade insights from this content.
{retry_note}
## CONTEXT
- Word count: {word_count}
- Target audience: {prefs.audience}
- Goal: {prefs.goal}

## CONTENT
---
{content}
---

## REQUIREMENTS

1. Extract ONE core_message (1-2 sentences)
   - Identify the central CONFLICT or misconception
   - Make it sharp and opinionated

2. Extract 5-6 key_points ONLY (quality over quantity):
   - 2-3 CRITICAL (core conflict, main mechanism, strongest data)
   - 2-3 HIGH (supporting insights)
   - 0-1 MEDIUM (edge cases/nuance)
   
3. For each key_point:
   - id: "kp_1", "kp_2", etc.
   - label: COMPLETE insight sentence with cause-effect
   - reason: Why this matters or mechanism behind it (optional)
   - priority: "critical" | "high" | "medium"
   - type: "insight" | "strategy" | "data"

CRITICAL RULES:
- Each label must be a complete sentence, not a phrase
- Include at least one non-obvious insight (behavioral/cultural/misconception)  
- Integrate data INTO insights, don't separate: "X improves Y (metric ↓ 30%)"
- Use specific verbs: reduces, creates, forces, enables (NOT improves, enhances, helps)
- Focus on WHAT happens and WHY it matters

Return structured JSON with core_message and key_points array."""

        result = self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            output_schema=SummaryOutput,
            temperature=0.5 if attempt == 0 else 0.6,
        )

        # Ensure all key_points have IDs
        for i, kp in enumerate(result.key_points):
            if not kp.id:
                kp.id = f"kp_{i + 1}"

        return result
    
    def validate_output(self, summary: SummaryOutput) -> tuple[bool, List[str]]:
        """
        Validate the summary output.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        kp_count = len(summary.key_points)
        if kp_count < self.min_key_points:
            issues.append(f"Too few key_points: {kp_count} < {self.min_key_points}")
        if kp_count > self.max_key_points:
            issues.append(f"Too many key_points: {kp_count} > {self.max_key_points}")
        
        critical_count = len([kp for kp in summary.key_points if kp.priority == "critical"])
        if critical_count < 2:
            issues.append(f"Need at least 2 critical key_points, got {critical_count}")
        
        if not summary.core_message or len(summary.core_message) < 10:
            issues.append("core_message is missing or too short")
        
        return len(issues) == 0, issues
