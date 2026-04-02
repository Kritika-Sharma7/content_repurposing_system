"""
SummarizerAgent: Extracts Content DNA from raw content.
First agent in the pipeline - transforms raw text into structured, atomic summary data.

Outputs clean, minimal structure:
- title, one_liner, intent, tone, structure
- content_dna (core_conflict, key_question)
- target_audience
- key_points (id, concept, claim, implication, importance, type)
- summary_quality (score, reason)
"""

from typing import Optional, List, Tuple
from schemas.schemas import (
    SummaryOutput, KeyInsight, SemanticKeyPoint,
    ContentDNA, SummaryQuality
)
from utils.llm import LLMClient, get_llm_client
from config.user_preferences import UserPreferences, DEFAULT_USER_PREFERENCES


# Audience-specific extraction strategies
AUDIENCE_STRATEGIES = {
    "founders": {
        "focus": ["business impact", "decision-making", "ROI", "market insights", "growth strategies"],
        "priority": "Extract insights that help with strategic decisions and business outcomes."
    },
    "engineers": {
        "focus": ["systems", "workflows", "technical implementation", "architecture", "efficiency"],
        "priority": "Focus on technical details, implementation patterns, and system design."
    },
    "marketers": {
        "focus": ["audience engagement", "messaging", "conversion", "brand positioning", "trends"],
        "priority": "Emphasize messaging angles, audience psychology, and engagement tactics."
    },
    "general professionals": {
        "focus": ["practical applications", "career impact", "productivity", "collaboration"],
        "priority": "Extract broadly applicable insights for professional development."
    },
    "investors": {
        "focus": ["market trends", "financial impact", "risk assessment", "competitive landscape"],
        "priority": "Focus on data-driven insights, market positioning, and growth indicators."
    },
    "default": {
        "focus": ["key takeaways", "practical applications", "evidence", "implications"],
        "priority": "Extract the most valuable, actionable insights from the content."
    }
}


SUMMARIZER_SYSTEM_PROMPT = """You are an expert content analyst performing CONTENT DNA EXTRACTION.

Your goal is to extract structured, atomic, and semantically rich units from content.

---

## 🧠 CONTENT DNA (REQUIRED)

Extract:
- core_conflict: What tension/problem drives this content?
- key_question: What question is this content answering?

---

## 🧩 KEY POINTS (4-8 REQUIRED)

Each key_point MUST have EXACTLY these fields:

{
  "id": "kp_1",
  "concept": "2-5 word topic",
  "claim": "Clear assertion",
  "implication": "Why it matters",
  "importance": "critical | high | medium",
  "type": "insight | data_point | strategy | observation"
}

---

## 🎯 QUALITY REQUIREMENTS

- Extract BOTH explicit AND implicit ideas
- Avoid generic phrasing
- Each point must be specific and actionable
- Claims must be verifiable from source

---

## 🚫 STRICT RULES

- DO NOT invent facts
- DO NOT output vague concepts
- DO NOT collapse multiple ideas into one key_point
- DO NOT add extra fields to key_points

---

Output must be structured JSON with: title, one_liner, intent, tone, structure, content_dna, target_audience, key_points, summary_quality."""


class SummarizerAgent:
    """
    Extracts Content DNA from raw content.

    Outputs clean structure:
    - title, one_liner, intent, tone, structure
    - content_dna (core_conflict, key_question)
    - target_audience
    - key_points (id, concept, claim, implication, importance, type)
    - summary_quality (score, reason)
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        min_key_points: int = 4,
        max_retries: int = 2,
        min_quality_score: float = 7.0
    ):
        """
        Initialize the SummarizerAgent.

        Args:
            llm_client: Optional custom LLM client
            min_key_points: Minimum required key_points (default 4)
            max_retries: Max retries if quality insufficient (default 2)
            min_quality_score: Minimum quality score to accept (default 7.0)
        """
        self.llm = llm_client or get_llm_client()
        self.system_prompt = SUMMARIZER_SYSTEM_PROMPT
        self.min_key_points = min_key_points
        self.max_retries = max_retries
        self.min_quality_score = min_quality_score

    def run(
        self,
        content: str,
        user_preferences: Optional[UserPreferences] = None
    ) -> SummaryOutput:
        """
        Process raw content and produce Content DNA.

        Args:
            content: Raw long-form text content to summarize
            user_preferences: Optional user preferences to guide extraction

        Returns:
            SummaryOutput with key_points, content_dna, summary_quality
        """
        prefs = user_preferences or DEFAULT_USER_PREFERENCES
        word_count = len(content.split())
        
        # Attempt extraction with quality-based retries
        result = None
        for attempt in range(self.max_retries + 1):
            result = self._extract(content, word_count, prefs, attempt)
            
            # Get quality score
            quality_score = result.summary_quality.score if result.summary_quality else 0
            
            # Check if quality meets threshold (score >= 8)
            if len(result.key_points) >= self.min_key_points and quality_score >= 8:
                return result
            
            if attempt < self.max_retries:
                continue
        
        # Return best attempt
        return result

    def _get_audience_strategy(self, audience: str) -> dict:
        """Get extraction strategy for audience type."""
        audience_lower = audience.lower()
        for key, strategy in AUDIENCE_STRATEGIES.items():
            if key in audience_lower:
                return strategy
        return AUDIENCE_STRATEGIES["default"]

    def _extract(
        self,
        content: str,
        word_count: int,
        prefs: UserPreferences,
        attempt: int
    ) -> SummaryOutput:
        """Perform a single extraction attempt."""
        
        # Get audience-specific strategy
        strategy = self._get_audience_strategy(prefs.audience)
        
        # Build retry context if this is a retry
        retry_context = ""
        if attempt > 0:
            retry_context = """
⚠️ PREVIOUS ATTEMPT INSUFFICIENT
FOR THIS RETRY:
- Extract DEEPER insights (look for implicit ideas)
- Be MORE specific in claims and implications
- Ensure content_dna has core_conflict and key_question
"""

        user_prompt = f"""Analyze the following content and extract its CONTENT DNA.
{retry_context}
## USER PREFERENCES
- Target Audience: {prefs.audience}
- Content Goal: {prefs.goal}
- Preferred Tone: {prefs.tone}
- Platforms: {', '.join(prefs.platforms)}

## AUDIENCE-SPECIFIC EXTRACTION STRATEGY
For {prefs.audience}:
- Focus areas: {', '.join(strategy['focus'])}
- Priority: {strategy['priority']}

## CONTENT TO ANALYZE
---
{content}
---

Word count: {word_count}

## REQUIRED OUTPUT (EXACT STRUCTURE)

### 1. key_points: Array of {self.min_key_points}-8 objects
Each key_point MUST have EXACTLY these fields (no extras):
{{
  "id": "kp_1",
  "concept": "async-first communication",
  "claim": "reduces meetings by 60%",
  "implication": "enables more deep work time",
  "importance": "critical | high | medium",
  "type": "insight | data_point | strategy | observation"
}}

### 2. content_dna: Simple DNA object (REQUIRED)
{{
  "core_conflict": "efficiency vs quality tradeoff",
  "key_question": "How can teams reduce meetings without losing alignment?"
}}

### 3. summary_quality: Self-assessment
{{
  "score": 8.5,
  "reason": "Good coverage with structured insights"
}}

### 4. Other required fields:
- title: Generated title
- one_liner: Single sentence hook
- intent: "educational" | "persuasive" | "informational" | "inspirational" | "analytical"
- tone: "informative" | "analytical" | "storytelling" | "conversational" | "formal" | "provocative"
- structure: "problem-solution" | "narrative" | "listicle" | "how-to" | "case-study" | "opinion" | "research"
- target_audience: "{prefs.audience}"

Extract intelligently for {prefs.audience} with goal: {prefs.goal}."""

        # Generate structured output via LLM
        result = self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            output_schema=SummaryOutput,
            temperature=0.5 if attempt == 0 else 0.65,
        )

        # Ensure word count is captured
        result.word_count_original = word_count

        # Ensure all key_points have IDs
        for i, kp in enumerate(result.key_points):
            if not kp.id:
                kp.id = f"kp_{i + 1}"

        # Fallback: derive key_points from insights if empty
        if not result.key_points and result.key_insights:
            result.key_points = [
                SemanticKeyPoint(
                    id=f"kp_{i + 1}",
                    concept=ins.topic,
                    claim=ins.insight,
                    implication="Key insight from content",
                    importance="high" if ins.importance == "high" else "medium",
                    type="insight"
                )
                for i, ins in enumerate(result.key_insights)
            ]

        # Ensure core_message is set
        if not result.core_message:
            result.core_message = result.one_liner

        # Simple quality score if LLM didn't provide one
        if not result.summary_quality:
            score, reason = self._compute_simple_quality(result)
            result.summary_quality = SummaryQuality(score=score, reason=reason)

        return result
    
    def _compute_simple_quality(self, summary: SummaryOutput) -> Tuple[float, str]:
        """Simple quality score - just count and coverage."""
        kp_count = len(summary.key_points) if summary.key_points else 0
        has_dna = summary.content_dna is not None
        
        # Base score from key points (target: 6)
        score = min(kp_count / 6, 1.0) * 7  # Up to 7 points
        
        # Bonus for content DNA
        if has_dna:
            score += 2.0
        
        # Bonus for variety (has critical points)
        if kp_count > 0:
            has_critical = any(kp.importance == "critical" for kp in summary.key_points)
            if has_critical:
                score += 1.0
        
        score = min(round(score, 1), 10.0)
        
        # Simple reason
        if score >= 8.5:
            reason = "Good coverage with structured insights"
        elif not has_dna:
            reason = "Could include content DNA (core_conflict, key_question)"
        elif kp_count < 5:
            reason = "Could extract more key points"
        else:
            reason = "Good extraction"
        
        return score, reason
    
    def validate_output(self, summary: SummaryOutput) -> Tuple[bool, List[str]]:
        """
        Validate the summary output.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        if len(summary.key_points) < self.min_key_points:
            issues.append(
                f"Insufficient key_points: {len(summary.key_points)} < {self.min_key_points}"
            )
        
        if not summary.content_dna:
            issues.append("Missing content_dna")
        
        if summary.summary_quality and summary.summary_quality.score < self.min_quality_score:
            issues.append(f"Quality score below threshold: {summary.summary_quality.score}")
        
        return len(issues) == 0, issues
