"""
FormatterAgent: Transforms summary into multiple platform-specific content formats.
Creates LinkedIn posts, Twitter threads, and newsletter content.

UPGRADE v2: Platform-Aware, Constraint-Driven, Traceable
- Consumes platform_config for constraints
- Maps each piece of content to source key_points (derived_from)
- Enforces platform constraints (tweet length ≤280, thread 5-8)

UPGRADE v3: Semantic Key Points, Hard Validation
- Uses SemanticKeyPoint.id for traceability (e.g., "kp_1", "kp_2")
- Hard constraint validation after generation
- Platform-native content transformation
"""

from typing import Optional, List
from schemas.schemas import SummaryOutput, FormattedOutput, SemanticKeyPoint
from utils.llm import LLMClient, get_llm_client
from config.platform_config import (
    PlatformConfig, DEFAULT_PLATFORM_CONFIG,
    validate_twitter_thread, validate_linkedin_post, validate_newsletter
)
from config.user_preferences import UserPreferences, DEFAULT_USER_PREFERENCES


FORMATTER_SYSTEM_PROMPT = """You are an expert content creator specializing in multi-format content repurposing. Your job is to transform structured summaries into engaging, platform-optimized content with FULL TRACEABILITY.

## CRITICAL: TRACEABILITY TO SEMANTIC KEY POINTS

EVERY piece of content MUST trace back to specific key_points using their IDs (e.g., "kp_1", "kp_2").

### LinkedIn Post
- derived_from: List key_point IDs covered (e.g., ["kp_1", "kp_2", "kp_4"])
- source_insights: List insight IDs covered

### Twitter Thread
- tweet_mappings: REQUIRED - Map each tweet to its source:
  [{"tweet_index": 0, "derived_from": ["kp_1"]}, {"tweet_index": 1, "derived_from": ["kp_2", "kp_3"]}]
- derived_from: All key_point IDs used in the thread
- source_insights: All insight IDs covered

### Newsletter
- sections_with_traceability: Each section maps to key_point IDs
- derived_from: All key_point IDs used

## GROUNDING RULES
- Use ONLY ideas/examples from the summary - do NOT invent "Company X", "Startup Y"
- Every tweet/paragraph should trace back to a specific key_point ID
- If the source has specific numbers/stats, use them exactly

## PLATFORM CONSTRAINTS (MUST FOLLOW - HARD VALIDATED)

### LinkedIn
- Hook: Strong opening that grabs attention (REQUIRED)
- Body: 2-4 paragraphs covering 3+ key_points
- CTA: End with an engaging question (REQUIRED)
- Hashtags: 3-5 relevant hashtags

### Twitter/X
- Thread: 5-8 tweets EXACTLY
- EACH TWEET: Maximum 280 characters (STRICTLY VALIDATED)
- Each tweet should map to 1-2 key_points
- First tweet must be a strong hook

### Newsletter
- Subject line: 6-10 words, compelling
- Preview text: Enticing snippet
- Body: 3-5 sections covering all key_points
- Scannable format with clear structure

## COVERAGE REQUIREMENT
ALL key_points must appear in at least one format. Missing coverage = failure."""


class FormatterAgent:
    """
    Transforms structured summaries into platform-specific content formats.

    Responsibility: Create LinkedIn posts, Twitter threads, and newsletter
    sections with full traceability to source key_points.
    
    Supports:
    - Platform configuration for constraints
    - User preferences for style
    - Full derived_from traceability
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        platform_config: Optional[PlatformConfig] = None
    ):
        """
        Initialize the FormatterAgent.

        Args:
            llm_client: Optional custom LLM client, uses default if not provided
            platform_config: Platform constraints configuration
        """
        self.llm = llm_client or get_llm_client()
        self.system_prompt = FORMATTER_SYSTEM_PROMPT
        self.platform_config = platform_config or DEFAULT_PLATFORM_CONFIG

    def run(
        self,
        summary: SummaryOutput,
        user_preferences: Optional[UserPreferences] = None,
        platforms: Optional[list[str]] = None
    ) -> FormattedOutput:
        """
        Transform a summary into multiple content formats.

        Args:
            summary: Structured summary from the SummarizerAgent
            user_preferences: Optional user preferences for style
            platforms: Optional list of platforms to generate (default: all)

        Returns:
            FormattedOutput with LinkedIn, Twitter, and newsletter content
        """
        prefs = user_preferences or DEFAULT_USER_PREFERENCES
        active_platforms = platforms or prefs.platforms
        
        # Build key_points list with semantic structure for traceability
        key_points_text = "\n".join(
            f"- {kp.id}: CONCEPT='{kp.concept}' | CLAIM='{kp.claim}' | IMPLICATION='{kp.implication}' | IMPORTANCE={kp.importance}"
            for kp in summary.key_points
        )
        
        # List of key point IDs for coverage tracking
        kp_ids = [kp.id for kp in summary.key_points]

        # Build insights text with IDs
        insights_text = "\n".join(
            f"- [{i.id}] [{i.importance.upper()}] {i.topic}: {i.insight}"
            for i in summary.key_insights
        )

        # Build platform constraints text
        constraints_text = self._build_constraints_text()

        user_prompt = f"""Create engaging, platform-optimized content based on this Content DNA.

## CONTENT DNA
Title: {summary.title}
One-Liner: {summary.one_liner}
Core Message: {summary.core_message}
Intent: {summary.intent}
Tone: {summary.tone}
Structure: {summary.structure}
Main Theme: {summary.main_theme}
Target Audience: {summary.target_audience}

## SEMANTIC KEY POINTS (use these IDs for derived_from traceability):
{key_points_text}

## KEY POINT IDs TO COVER: {kp_ids}

## KEY INSIGHTS (for source_insights arrays):
{insights_text}

## USER PREFERENCES
- Tone: {prefs.tone}
- Goal: {prefs.goal}
- Audience: {prefs.audience}
- Platforms: {', '.join(active_platforms)}

## PLATFORM CONSTRAINTS (STRICTLY VALIDATED)
{constraints_text}

## REQUIREMENTS

### LinkedIn Post
1. Hook: Strong professional opening (REQUIRED - validated)
2. Body: Cover 3+ key_points using their concepts and claims
3. CTA: Engaging question (REQUIRED - validated)
4. Hashtags: 3-5 relevant
5. derived_from: ["{kp_ids[0]}", ...] - list ALL key_point IDs used
6. source_insights: ["insight_1", ...] - list ALL insights covered

### Twitter Thread
1. EXACTLY {self.platform_config.twitter.thread_length_min}-{self.platform_config.twitter.thread_length_max} tweets
2. EACH tweet MUST be ≤{self.platform_config.twitter.max_chars_per_tweet} characters (HARD LIMIT)
3. tweet_mappings: REQUIRED - [{{"tweet_index": 0, "derived_from": ["{kp_ids[0]}"]}}, ...]
4. derived_from: List ALL key_point IDs used across thread
5. source_insights: List ALL insights covered

### Newsletter
1. Subject: 6-10 words
2. {self.platform_config.newsletter.min_sections}-{self.platform_config.newsletter.max_sections} body sections
3. sections_with_traceability: Each section with its derived_from using key_point IDs
4. derived_from: List ALL key_point IDs used
5. source_insights: List ALL insights covered

## CRITICAL RULES
- Use ONLY ideas from the summary - NO invented examples
- ALL key_points ({kp_ids}) must appear in at least one format
- Twitter tweets MUST be ≤280 characters each - COUNT CAREFULLY
- Use key_point IDs (e.g., "{kp_ids[0]}") NOT index notation"""

        result = self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            output_schema=FormattedOutput,
            temperature=0.7,  # Higher creativity for content generation
        )

        # Post-process to ensure constraints and traceability
        result = self._post_process(result, summary)
        
        # Hard validation of constraints
        self._validate_constraints(result)

        # Ensure version is set to 1
        result.version = 1

        return result

    def _build_constraints_text(self) -> str:
        """Build platform constraints description."""
        lc = self.platform_config.linkedin
        tc = self.platform_config.twitter
        nc = self.platform_config.newsletter
        
        return f"""### LinkedIn
- Tone: {lc.tone}
- Length: {lc.length}
- Style: {lc.style}
- Hook Required: {lc.constraints.hook_required}

### Twitter/X
- Tone: {tc.tone}
- Style: {tc.style}
- Max chars per tweet: {tc.max_chars_per_tweet}
- Thread length: {tc.thread_length_min}-{tc.thread_length_max} tweets

### Newsletter
- Tone: {nc.tone}
- Style: {nc.style}
- Sections: {nc.min_sections}-{nc.max_sections}"""

    def _post_process(
        self,
        result: FormattedOutput,
        summary: SummaryOutput
    ) -> FormattedOutput:
        """
        Post-process to ensure constraints and derive traceability if missing.
        Uses semantic key point IDs (e.g., "kp_1") instead of index notation.
        """
        kp_ids = [kp.id for kp in summary.key_points]
        
        # Ensure LinkedIn has derived_from
        if not result.linkedin.derived_from:
            result.linkedin.derived_from = self._infer_derived_from(
                result.linkedin.hook + " " + result.linkedin.body,
                summary.key_points
            )

        # Ensure Twitter has derived_from and mappings
        if not result.twitter.derived_from:
            all_derived = []
            for i, tweet in enumerate(result.twitter.tweets):
                derived = self._infer_derived_from(tweet, summary.key_points)
                all_derived.extend(derived)
                # Add to tweet_mappings if missing
                if i >= len(result.twitter.tweet_mappings):
                    from schemas.schemas import TweetMapping
                    result.twitter.tweet_mappings.append(
                        TweetMapping(
                            tweet_index=i, 
                            derived_from=derived or [kp_ids[i % len(kp_ids)]]
                        )
                    )
            result.twitter.derived_from = list(set(all_derived))

        # Ensure Newsletter has derived_from
        if not result.newsletter.derived_from:
            all_content = result.newsletter.intro + " " + " ".join(result.newsletter.body_sections)
            result.newsletter.derived_from = self._infer_derived_from(
                all_content,
                summary.key_points
            )

        # Truncate tweets that exceed 280 chars (safety net)
        for i, tweet in enumerate(result.twitter.tweets):
            if len(tweet) > 280:
                # Truncate at word boundary
                truncated = tweet[:277]
                last_space = truncated.rfind(' ')
                if last_space > 200:
                    truncated = truncated[:last_space]
                result.twitter.tweets[i] = truncated + "..."

        return result

    def _validate_constraints(self, result: FormattedOutput) -> None:
        """
        Perform hard validation of platform constraints.
        Logs warnings for violations but doesn't fail (reviewer will catch issues).
        """
        violations = []
        
        # Validate Twitter
        tw_valid, tw_violations = validate_twitter_thread(
            result.twitter.tweets,
            self.platform_config.twitter
        )
        if tw_violations:
            violations.extend([f"Twitter: {v.constraint} - {v.actual} (expected {v.expected})" 
                              for v in tw_violations])
        
        # Validate LinkedIn
        li_valid, li_violations = validate_linkedin_post(
            result.linkedin.hook,
            result.linkedin.body,
            result.linkedin.call_to_action,
            self.platform_config.linkedin
        )
        if li_violations:
            violations.extend([f"LinkedIn: {v.constraint} - {v.actual} (expected {v.expected})" 
                              for v in li_violations])
        
        # Validate Newsletter
        nl_valid, nl_violations = validate_newsletter(
            result.newsletter.intro,
            result.newsletter.body_sections,
            result.newsletter.closing,
            self.platform_config.newsletter
        )
        if nl_violations:
            violations.extend([f"Newsletter: {v.constraint} - {v.actual} (expected {v.expected})" 
                              for v in nl_violations])
        
        # Store violations for reviewer to access (attached to result)
        result._constraint_violations = violations

    def _infer_derived_from(
        self,
        content: str,
        key_points: List[SemanticKeyPoint]
    ) -> List[str]:
        """
        Infer which key_points a piece of content is derived from.
        Uses semantic matching against concept, claim, and implication.
        Returns key point IDs (e.g., "kp_1", "kp_2").
        """
        derived = []
        content_lower = content.lower()
        
        for kp in key_points:
            # Match against concept, claim, and implication
            concept_words = [w.lower() for w in kp.concept.split() if len(w) > 3]
            claim_words = [w.lower() for w in kp.claim.split() if len(w) > 4]
            
            # Check if any significant words appear in content
            concept_match = any(word in content_lower for word in concept_words)
            claim_match = any(word in content_lower for word in claim_words[:4])
            
            if concept_match or claim_match:
                derived.append(kp.id)
        
        return derived
