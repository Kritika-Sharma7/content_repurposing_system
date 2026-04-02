"""
Platform configuration for content formatting.
Defines constraints and style requirements for each target platform.

UPGRADE v3: Added hard constraint validation functions.
"""

from typing import Literal, Optional, List, Tuple
from pydantic import BaseModel, Field


class PlatformConstraints(BaseModel):
    """Generic constraints for a platform."""
    max_length: Optional[int] = Field(default=None, description="Maximum character length")
    min_length: Optional[int] = Field(default=None, description="Minimum character length")
    hook_required: bool = Field(default=False, description="Whether a hook is required")
    cta_required: bool = Field(default=False, description="Whether a CTA is required")


class ConstraintViolation(BaseModel):
    """A constraint violation with details."""
    constraint: str
    actual: str
    expected: str
    severity: Literal["error", "warning"] = "error"


class LinkedInConfig(BaseModel):
    """LinkedIn-specific configuration."""
    tone: Literal["professional", "conversational", "thought-leadership"] = Field(
        default="professional",
        description="Writing tone for LinkedIn"
    )
    length: Literal["short", "medium", "medium-long", "long"] = Field(
        default="medium-long",
        description="Content length preference"
    )
    style: Literal["insight-led", "storytelling", "analytical", "listicle"] = Field(
        default="insight-led",
        description="Content style"
    )
    constraints: PlatformConstraints = Field(
        default_factory=lambda: PlatformConstraints(
            hook_required=True,
            cta_required=True,
            min_length=100,
            max_length=3000
        )
    )


class TwitterConfig(BaseModel):
    """Twitter/X-specific configuration."""
    tone: Literal["concise", "conversational", "provocative", "informative"] = Field(
        default="concise",
        description="Writing tone for Twitter"
    )
    length: Literal["short", "medium"] = Field(
        default="short",
        description="Content length preference"
    )
    style: Literal["thread", "single", "quote-led"] = Field(
        default="thread",
        description="Content style"
    )
    constraints: PlatformConstraints = Field(
        default_factory=lambda: PlatformConstraints(max_length=280)
    )
    max_chars_per_tweet: int = Field(default=280, description="Maximum characters per tweet")
    thread_length_min: int = Field(default=5, description="Minimum tweets in thread")
    thread_length_max: int = Field(default=8, description="Maximum tweets in thread")


class NewsletterConfig(BaseModel):
    """Newsletter-specific configuration."""
    tone: Literal["conversational", "professional", "casual", "educational"] = Field(
        default="conversational",
        description="Writing tone for newsletter"
    )
    length: Literal["short", "medium", "long"] = Field(
        default="medium",
        description="Content length preference"
    )
    style: Literal["structured", "narrative", "curated", "deep-dive"] = Field(
        default="structured",
        description="Content style"
    )
    constraints: PlatformConstraints = Field(
        default_factory=lambda: PlatformConstraints(
            min_length=200,
            max_length=5000
        )
    )
    min_sections: int = Field(default=3, description="Minimum body sections")
    max_sections: int = Field(default=5, description="Maximum body sections")


class PlatformConfig(BaseModel):
    """Complete platform configuration."""
    linkedin: LinkedInConfig = Field(default_factory=LinkedInConfig)
    twitter: TwitterConfig = Field(default_factory=TwitterConfig)
    newsletter: NewsletterConfig = Field(default_factory=NewsletterConfig)


# Default platform configuration
DEFAULT_PLATFORM_CONFIG = PlatformConfig(
    linkedin=LinkedInConfig(
        tone="professional",
        length="medium-long",
        style="insight-led",
        constraints=PlatformConstraints(
            hook_required=True,
            cta_required=True,
            min_length=100,
            max_length=3000
        )
    ),
    twitter=TwitterConfig(
        tone="concise",
        length="short",
        style="thread",
        constraints=PlatformConstraints(max_length=280),
        max_chars_per_tweet=280,
        thread_length_min=5,
        thread_length_max=8
    ),
    newsletter=NewsletterConfig(
        tone="conversational",
        length="medium",
        style="structured",
        constraints=PlatformConstraints(min_length=200, max_length=5000),
        min_sections=3,
        max_sections=5
    )
)


# ============================================================================
# HARD CONSTRAINT VALIDATION FUNCTIONS
# ============================================================================

def validate_twitter_thread(
    tweets: List[str],
    config: TwitterConfig
) -> Tuple[bool, List[ConstraintViolation]]:
    """
    Validate a Twitter thread against hard constraints.
    
    Returns:
        Tuple of (is_valid, list_of_violations)
    """
    violations = []
    
    # Check thread length
    if len(tweets) < config.thread_length_min:
        violations.append(ConstraintViolation(
            constraint="thread_length_min",
            actual=str(len(tweets)),
            expected=f">= {config.thread_length_min}",
            severity="error"
        ))
    
    if len(tweets) > config.thread_length_max:
        violations.append(ConstraintViolation(
            constraint="thread_length_max",
            actual=str(len(tweets)),
            expected=f"<= {config.thread_length_max}",
            severity="warning"
        ))
    
    # Check each tweet length
    for i, tweet in enumerate(tweets):
        if len(tweet) > config.max_chars_per_tweet:
            violations.append(ConstraintViolation(
                constraint=f"tweet_{i}_length",
                actual=f"{len(tweet)} chars",
                expected=f"<= {config.max_chars_per_tweet} chars",
                severity="error"
            ))
    
    return len([v for v in violations if v.severity == "error"]) == 0, violations


def validate_linkedin_post(
    hook: str,
    body: str,
    cta: str,
    config: LinkedInConfig
) -> Tuple[bool, List[ConstraintViolation]]:
    """
    Validate a LinkedIn post against hard constraints.
    
    Returns:
        Tuple of (is_valid, list_of_violations)
    """
    violations = []
    total_length = len(hook) + len(body) + len(cta)
    
    # Check hook requirement
    if config.constraints.hook_required and (not hook or len(hook.strip()) < 10):
        violations.append(ConstraintViolation(
            constraint="hook_required",
            actual=f"hook length: {len(hook)}",
            expected="meaningful hook (>= 10 chars)",
            severity="error"
        ))
    
    # Check CTA requirement
    if config.constraints.cta_required and (not cta or len(cta.strip()) < 10):
        violations.append(ConstraintViolation(
            constraint="cta_required",
            actual=f"cta length: {len(cta)}",
            expected="meaningful CTA (>= 10 chars)",
            severity="error"
        ))
    
    # Check length constraints
    if config.constraints.min_length and total_length < config.constraints.min_length:
        violations.append(ConstraintViolation(
            constraint="min_length",
            actual=f"{total_length} chars",
            expected=f">= {config.constraints.min_length} chars",
            severity="warning"
        ))
    
    if config.constraints.max_length and total_length > config.constraints.max_length:
        violations.append(ConstraintViolation(
            constraint="max_length",
            actual=f"{total_length} chars",
            expected=f"<= {config.constraints.max_length} chars",
            severity="error"
        ))
    
    return len([v for v in violations if v.severity == "error"]) == 0, violations


def validate_newsletter(
    intro: str,
    sections: List[str],
    closing: str,
    config: NewsletterConfig
) -> Tuple[bool, List[ConstraintViolation]]:
    """
    Validate a newsletter against hard constraints.
    
    Returns:
        Tuple of (is_valid, list_of_violations)
    """
    violations = []
    total_length = len(intro) + sum(len(s) for s in sections) + len(closing)
    
    # Check section count
    if len(sections) < config.min_sections:
        violations.append(ConstraintViolation(
            constraint="min_sections",
            actual=str(len(sections)),
            expected=f">= {config.min_sections}",
            severity="error"
        ))
    
    if len(sections) > config.max_sections:
        violations.append(ConstraintViolation(
            constraint="max_sections",
            actual=str(len(sections)),
            expected=f"<= {config.max_sections}",
            severity="warning"
        ))
    
    # Check length constraints
    if config.constraints.min_length and total_length < config.constraints.min_length:
        violations.append(ConstraintViolation(
            constraint="min_length",
            actual=f"{total_length} chars",
            expected=f">= {config.constraints.min_length} chars",
            severity="warning"
        ))
    
    if config.constraints.max_length and total_length > config.constraints.max_length:
        violations.append(ConstraintViolation(
            constraint="max_length",
            actual=f"{total_length} chars",
            expected=f"<= {config.constraints.max_length} chars",
            severity="error"
        ))
    
    return len([v for v in violations if v.severity == "error"]) == 0, violations


def validate_all_platforms(
    linkedin_data: dict,
    twitter_data: dict,
    newsletter_data: dict,
    config: PlatformConfig = DEFAULT_PLATFORM_CONFIG
) -> Tuple[bool, dict]:
    """
    Validate all platform outputs against constraints.
    
    Returns:
        Tuple of (all_valid, violations_by_platform)
    """
    all_violations = {}
    all_valid = True
    
    # Validate LinkedIn
    li_valid, li_violations = validate_linkedin_post(
        linkedin_data.get("hook", ""),
        linkedin_data.get("body", ""),
        linkedin_data.get("call_to_action", ""),
        config.linkedin
    )
    if not li_valid:
        all_valid = False
    if li_violations:
        all_violations["linkedin"] = [v.model_dump() for v in li_violations]
    
    # Validate Twitter
    tw_valid, tw_violations = validate_twitter_thread(
        twitter_data.get("tweets", []),
        config.twitter
    )
    if not tw_valid:
        all_valid = False
    if tw_violations:
        all_violations["twitter"] = [v.model_dump() for v in tw_violations]
    
    # Validate Newsletter
    nl_valid, nl_violations = validate_newsletter(
        newsletter_data.get("intro", ""),
        newsletter_data.get("body_sections", []),
        newsletter_data.get("closing", ""),
        config.newsletter
    )
    if not nl_valid:
        all_valid = False
    if nl_violations:
        all_violations["newsletter"] = [v.model_dump() for v in nl_violations]
    
    return all_valid, all_violations


def get_platform_config(platform: str = None) -> PlatformConfig:
    """
    Get platform configuration.
    
    Args:
        platform: Optional specific platform name to get config for.
                  If None, returns full config.
    
    Returns:
        PlatformConfig or specific platform config if requested.
    """
    if platform is None:
        return DEFAULT_PLATFORM_CONFIG
    
    platform_lower = platform.lower()
    if platform_lower == "linkedin":
        return DEFAULT_PLATFORM_CONFIG.linkedin
    elif platform_lower == "twitter":
        return DEFAULT_PLATFORM_CONFIG.twitter
    elif platform_lower == "newsletter":
        return DEFAULT_PLATFORM_CONFIG.newsletter
    else:
        return DEFAULT_PLATFORM_CONFIG
