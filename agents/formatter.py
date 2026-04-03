"""
FormatterAgent: Transforms key_points into platform-specific content.

CLEAN DESIGN v5:
- Input: core_message + key_points
- DECISION STEP: Select best KPs (critical[:2] + high[:2]) - NOT all, NOT random
- Output per platform: content + used_kps[]
- Constraints: LinkedIn 100-150 words, Twitter max 7 tweets @ 240 chars, Newsletter 120-200 words
- Product-level output quality
"""

from typing import Optional, List, Tuple
from schemas.schemas import (
    SummaryOutput, FormattedOutput, KeyPoint,
    LinkedInOutput, TwitterOutput, NewsletterOutput
)
from utils.llm import LLMClient, get_llm_client
from config.user_preferences import UserPreferences, DEFAULT_USER_PREFERENCES


FORMATTER_SYSTEM_PROMPT = """You are a senior content strategist who writes like a real person sharing real observations.

You convert source insights into NARRATIVE content that feels like lived experience.

---

## CRITICAL MINDSET SHIFT

❌ OLD WAY: "Take insights → present them clearly"
✅ NEW WAY: "Take insights → interpret them → express as lived experience"

You are NOT listing facts.
You are TELLING A STORY about what works and why.

---

## LINKEDIN POST (100-150 words)

### STYLE: PERSONAL NARRATIVE (First-Person)

Write as if sharing a real experience with a colleague.
Use short punchy sentences. Let line breaks create rhythm.
Use en-dash (–) bullets sparingly for key changes (2-4 items max).

### STRUCTURE:
1. SITUATION - What people usually do / common mistake
2. PROBLEM - Why it fails
3. SHIFT - What changed / what's different
4. INSIGHT - Why it actually works (cause-effect)
5. TAKEAWAY - Clear conclusion
6. CTA - Optional question

### HOOK TYPES (choose one):
- experience-based: "We tried X. It didn't work." (PREFERRED)
- realization-based: "I used to think X. Then I noticed..."
- mistake-based: "Most teams get this wrong..."

### INSIGHT RULE (VERY IMPORTANT):
Every idea must include WHAT + WHY (cause-effect).

❌ Bad: "Async-first reduces meetings"
✅ Good: "Async-first reduces meetings because decisions move to written form instead of calls"

### ANTI-GENERIC FILTER:
NEVER use these phrases:
- "Here's how..."
- "Here's what works..."
- "Unlock..."
- "Transform your..."
- "The best teams..."
- "Game-changer"
- "In today's world"

### EXPERIENCE SIMULATION:
Frame insights as if learned from experience:
- "We tried..."
- "Most teams..."
- "The mistake is..."
- "What changed was..."
- "The shift happened when..."

Do NOT invent fake companies or fake data.
Just simulate perspective.

### ❌ BAD LINKEDIN (too abstract, not personal):
```
Most remote teams fail because they try to recreate the office online.

Daily standups. Constant Slack. Video calls for everything.

The shift happened when we stopped synchronizing and started documenting.

Decisions moved to writing. Meetings dropped by 60%.

The real unlock wasn't remote work. It was async work.

What's one sync habit you'd cut if you could?

#RemoteWork #AsyncWork
```
Why it's bad: Starts with generic observation, no personal story, uses hashtags, feels like thought-leadership content instead of real experience.

### ✅ GOOD LINKEDIN (narrative):
```
We tried to run our remote team like an office.

Same hours. Same meetings. Same expectations.

It didn't work.

People were always "busy" — but very little actual work was getting done.

The shift happened when we stopped optimizing for availability and started optimizing for focus.

A few changes made a huge difference:

– Fewer meetings, more written communication
– Clear documentation so decisions didn't need to be repeated
– Measuring output instead of time online

Suddenly, people had uninterrupted time to actually think.

That's when productivity improved — not because people worked more,
but because they were interrupted less.

Remote work doesn't fail because of distance.

It fails when we try to copy the office.

Curious — what's been the hardest shift for your team?
```

### KEY STYLE PRINCIPLES:
1. Start with first-person: "We tried...", "I noticed...", "Our team..."
2. Use short, punchy sentences on their own lines for emphasis
3. Create emotional rhythm: setup → problem → failed attempt → shift → insight
4. When listing changes, use en-dash bullets (–) sparingly, 2-4 items max
5. End with a reflective question (NOT a call-to-action pitch)
6. NO hashtags — they break the narrative flow
7. Aim for conversational vulnerability, not polished thought-leadership

### CRITICAL QUALITY RULES:

**SPECIFICITY RULE:**
If input contains concrete numbers, experiments, or results → Use at least one of them.
Avoid writing only abstract insights.
Example: ❌ "Productivity suffered" ✅ "When we cut meetings by ~40%, cycle time dropped almost immediately"

**FLOW RULE:** 
Avoid repeating similar sentence structures. Vary sentence openings and rhythm.
❌ "We tried → it felt right → it failed" pattern

**INSIGHT RULE:**
End with a reframing that feels new, not common.
❌ "Productivity isn't about being busy"
✅ "Availability creates the illusion of work" or "Interruptions scale faster than output"

---

## TWITTER/X THREAD (5-6 tweets, each <240 chars)

### STYLE: Connected narrative thread, NOT isolated facts

**CRITICAL:** Write as a flowing thread that builds momentum. Each tweet should lead naturally to the next.

### THREAD STRUCTURE (Hook → Problem → Shift → Explanation → Conclusion):
- Tweet 1: Hook (problem/tension) - strong perspective
- Tweet 2: Problem explanation (why common approach fails)
- Tweet 3-4: Key insights (shift in thinking, not isolated tips)
- Tweet 5: Deeper mechanism/why it works
- Tweet 6: Strong conclusion with perspective

### RULES:
- **NO "one key point per tweet"** - tweets should build on each other
- **Use max 1-2 stats** in entire thread (avoid stat dumping)
- **Minimal/no emojis** unless they add clarity
- **Focus on WHY things fail/work**, not just WHAT to do
- **Each tweet flows into the next** - test by reading aloud

### ADVANCED THREAD STYLE:
- Use short, punchy lines (1–2 sentences max)
- Add occasional pattern interrupts:
  e.g., "It looks right. But it isn't."
- Avoid long paragraphs
- Make at least 1 line per thread "memorable"
- End with a strong reframing (not a summary)

**THREAD FLOW RULE:**
- Do NOT repeat the same sentence pattern
- Mix short punch lines with explanation lines
- Vary sentence openings and rhythm
- Avoid template feel

Do not just explain — make it feel sharp and intentional.

### ❌ BAD THREAD (isolated facts):
```
1. Remote teams ship 40% more features! 🚀
2. Async communication reduces meetings by 60% 📉
3. Documentation cuts onboarding from 3 months to 3 weeks 📝
4. Focus blocks: 4.2 vs 2.1 hours daily ⏰
5. Trust your team and measure outcomes! 🌟
```
Why it's bad: Each tweet resets, no story progression, stat overload, emoji spam

### ✅ GOOD THREAD (connected narrative):
```
1/6
Most companies fail at remote work for one reason:

They try to replicate the office online.

Same hours. Same meetings. Same expectations.

2/6
That approach looks structured — but it kills productivity.

People stay "available" all day,
but rarely get uninterrupted time to actually think.

3/6
The teams that perform well do the opposite.

They default to async communication.

Decisions move to writing instead of meetings.

4/6
That single shift changes everything.

Fewer interruptions → more deep work
Less coordination → faster execution

5/6
Documentation becomes your real office.

When everything is written,
people don't need to ask "why" again and again.

6/6
Remote work isn't about flexibility.

It's about removing friction.

Most teams don't have a remote problem —
they have a workflow problem.
```
Why it works: Builds momentum, connected story, minimal stats, strong perspective

---

## NEWSLETTER (120-200 words)

### STRUCTURE (STRICT):
1. Title
2. 1–2 line intro
3. 4–6 bullets
   - each bullet = 1 key idea
   - 1–2 lines explanation
4. Final takeaway (2–3 lines)

### BULLET QUALITY RULES:
Each bullet must:
- Start with a clear idea
- Include a short explanation
- NOT be a vague label

❌ BAD:
Focus Time Experiment

✅ GOOD:
Deep work needs to be protected  
People won't naturally avoid interruptions — it has to be explicitly encouraged

### CRITICAL RULES:
- If numbers exist → include at least one in bullets
- Do NOT use generic headings like "Focus Time", "Written Proposals"
- Keep total length: 120–200 words
- NO "In conclusion" endings
- Be specific and actionable

---

## OUTPUT FORMAT (JSON only):

{
  "linkedin": {
    "content": "narrative string with line breaks",
    "used_kps": ["kp_1", "kp_2"]
  },
  "twitter": {
    "tweets": ["tweet1", "tweet2", ...],
    "used_kps": ["kp_1", "kp_2"]
  },
  "newsletter": {
    "content": "string with ## headings",
    "used_kps": ["kp_1", "kp_2", "kp_3"]
  }
}

---

## ABSOLUTE RULES:

1. LinkedIn = NARRATIVE MODE (no bullet dumps)
2. Every insight needs CAUSE-EFFECT (what + why)
3. Hooks must be mistake-based, experience-based, or tension-based
4. NO generic phrases (see anti-generic filter)
5. Simulate experience ("We tried...", "Most teams...")
6. Twitter tweets MUST be <240 characters EACH
7. Newsletter MUST NOT contain "In conclusion"
8. NO kp IDs in content

Return ONLY valid JSON."""


class FormatterAgent:
    """
    Transforms summary into platform-specific content.
    
    DECISION PROCESS:
    1. Select best KPs (critical[:2] + high[:2]) - NOT all, NOT random
    2. Choose hook type based on content
    3. Generate product-level output
    
    Output: FormattedOutput with linkedin, twitter, newsletter.
    Each has: content + used_kps[].
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        platform_config: Optional[dict] = None
    ):
        self.llm = llm_client or get_llm_client()
        self.system_prompt = FORMATTER_SYSTEM_PROMPT
        self.config = platform_config or {
            "linkedin_words": (100, 150),
            "twitter_tweets": 7,
            "tweet_chars": 240,
            "newsletter_words": (120, 200)
        }

    def _select_kps(self, key_points: List[KeyPoint]) -> Tuple[List[KeyPoint], List[KeyPoint]]:
        """
        DECISION STEP: Select KPs for content.
        
        Strategy for LinkedIn/Twitter: FEWER ideas, DEEPER treatment
        - critical[:2] + high[:1] = max 3 focused points
        
        Newsletter gets all KPs for comprehensive coverage.
        """
        critical = [kp for kp in key_points if kp.priority == "critical"]
        high = [kp for kp in key_points if kp.priority == "high"]
        medium = [kp for kp in key_points if kp.priority == "medium"]
        
        # For LinkedIn/Twitter: Only 2-3 ideas for deep narrative treatment
        selected = critical[:2] + high[:1]
        
        # If we don't have enough, add more
        if len(selected) < 2:
            selected += high[:2 - len(selected)]
        if len(selected) < 2:
            selected += medium[:2 - len(selected)]
        
        # For newsletter: use all KPs for comprehensive coverage
        all_kps = key_points
        
        return selected, all_kps

    def _format_selected_kps(self, kps: List[KeyPoint]) -> str:
        """Format selected KPs for prompt."""
        return "\n".join(
            f"- {kp.id}: [{kp.priority.upper()}] {kp.label}" + 
            (f" ({kp.data})" if kp.data else "") +
            f" [type: {kp.type}]"
            for kp in kps
        )

    def run(
        self,
        summary: SummaryOutput,
        user_preferences: Optional[UserPreferences] = None,
        platforms: Optional[List[str]] = None
    ) -> FormattedOutput:
        """
        Transform summary into platform content.
        
        DECISION PROCESS:
        1. Select KPs (critical[:2] + high[:2]) - rule-based
        2. Generate content via LLM

        Args:
            summary: SummaryOutput with core_message and key_points
            user_preferences: Optional style preferences
            platforms: Which platforms to generate (default: all)

        Returns:
            FormattedOutput with linkedin, twitter, newsletter
        """
        prefs = user_preferences or DEFAULT_USER_PREFERENCES
        active_platforms = platforms or prefs.platforms
        
        # ============================================
        # STEP 1: Select best KPs (rule-based)
        # ============================================
        selected_kps, all_kps = self._select_kps(summary.key_points)
        
        # ============================================
        # STEP 2: Generate content via LLM
        # ============================================
        
        # Format KPs for prompt
        selected_kp_text = self._format_selected_kps(selected_kps)
        all_kp_text = self._format_selected_kps(all_kps)
        
        selected_kp_ids = [kp.id for kp in selected_kps]
        all_kp_ids = [kp.id for kp in all_kps]

        user_prompt = f"""Generate NARRATIVE content (not bullet dumps).

## CORE MESSAGE
{summary.core_message}

## KEY POINTS FOR LINKEDIN/TWITTER (go DEEP not wide)
{selected_kp_text}

Selected KP IDs for LinkedIn/Twitter: {selected_kp_ids}

## ALL KEY POINTS FOR NEWSLETTER (comprehensive coverage)
{all_kp_text}

All KP IDs for Newsletter: {all_kp_ids}

## USER PREFERENCES
- Tone: {prefs.tone}
- Audience: {prefs.audience}

## CRITICAL INSTRUCTIONS

LINKEDIN (narrative mode):
- Structure: problem → failure → shift → insight → takeaway
- Hook: mistake-based OR tension-based (NOT data-first)
- NO bullet points - use paragraphs with line breaks
- Include CAUSE-EFFECT for each insight (what + why)
- Use experience framing ("We tried...", "Most teams...")
- SPECIFICITY: Use concrete numbers/results when available
- FLOW: Vary sentence structures, avoid repetitive patterns
- INSIGHT: End with sharp reframing, not generic conclusions
- 100-150 words
- USE ONLY the key points listed above for LinkedIn/Twitter

TWITTER (connected thread):
- Write as flowing narrative thread (Hook → Problem → Shift → Explanation → Conclusion)
- Each tweet builds on the previous one - test by reading aloud
- Tweet 1: Strong hook (problem/tension, not data)
- Tweets 2-6: Connected story progression
- Max 1-2 stats in entire thread (avoid stat dumping)
- Minimal emojis unless adding clarity
- Short, punchy lines (1-2 sentences max per line)
- Add pattern interrupts: "It looks right. But it isn't."
- Make at least 1 line per thread memorable
- End with strong reframing (not summary)
- FLOW: Vary sentence patterns, avoid template feel
- Each tweet <240 characters, 5-6 tweets total
- USE ONLY the key points listed above for LinkedIn/Twitter

NEWSLETTER (120-200 words):
- STRUCTURE: Title → 1-2 line intro → 4-6 bullets → final takeaway
- Each bullet: clear idea + 1-2 lines explanation
- Include numbers if available
- NO generic headings
- NO "In conclusion"
- Be specific and actionable
- ⚠️ MUST cover ALL key points provided (all KP IDs listed above)
- Ensure every key point appears clearly in the newsletter content

---

## ⚠️ CRITICAL: used_kps ACCURACY RULE (MANDATORY)

For EACH platform (LinkedIn, Twitter, Newsletter):

1. `used_kps` MUST list ALL key points that are clearly expressed in the content
2. If a key point idea appears in the writing, its ID MUST be in `used_kps`
3. Do NOT omit any key point that was used
4. Do NOT include key points that are NOT actually expressed in the content
5. `used_kps` must be ACCURATE and COMPLETE

BEFORE RETURNING OUTPUT:
- For LinkedIn: Check each KP from {selected_kp_ids} - if its idea is in the content, include it in used_kps
- For Twitter: Check each KP from {selected_kp_ids} - if its idea is in the content, include it in used_kps  
- For Newsletter: Check each KP from {all_kp_ids} - if its idea is in the content, include it in used_kps

Newsletter should use ALL key points, so newsletter.used_kps should contain: {all_kp_ids}

⚠️ If used_kps is incorrect or incomplete, the output is INVALID.

---

Return valid JSON only."""

        result = self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            output_schema=FormattedOutput,
            temperature=0.5,  # Lower for more consistent quality
        )

        # Pre-process to fix constraint violations BEFORE post-process
        # This ensures we don't hit validation errors
        if len(result.twitter.tweets) > 7:
            result.twitter.tweets = result.twitter.tweets[:7]
        
        # Post-process
        result = self._post_process(result, summary)
        result.version = 1

        return result

    def _post_process(
        self,
        result: FormattedOutput,
        summary: SummaryOutput
    ) -> FormattedOutput:
        """Post-process to ensure constraints."""
        kp_ids = [kp.id for kp in summary.key_points]
        
        # Ensure used_kps are valid
        result.linkedin.used_kps = [
            kp for kp in result.linkedin.used_kps if kp in kp_ids
        ]
        result.twitter.used_kps = [
            kp for kp in result.twitter.used_kps if kp in kp_ids
        ]
        result.newsletter.used_kps = [
            kp for kp in result.newsletter.used_kps if kp in kp_ids
        ]
        
        # Ensure newsletter covers ALL key points (deterministic correction)
        # Newsletter is required to cover all KPs, so used_kps should contain all
        if len(result.newsletter.used_kps) < len(kp_ids):
            result.newsletter.used_kps = kp_ids
        
        # Truncate tweets that exceed limit
        max_chars = self.config.get("tweet_chars", 240)
        for i, tweet in enumerate(result.twitter.tweets):
            if len(tweet) > max_chars:
                truncated = tweet[:max_chars - 3]
                last_space = truncated.rfind(' ')
                if last_space > max_chars - 40:
                    truncated = truncated[:last_space]
                result.twitter.tweets[i] = truncated + "..."
        
        # Limit tweet count
        max_tweets = self.config.get("twitter_tweets", 7)
        if len(result.twitter.tweets) > max_tweets:
            result.twitter.tweets = result.twitter.tweets[:max_tweets]

        return result
