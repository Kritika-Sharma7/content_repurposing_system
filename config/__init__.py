"""
Configuration module for the multi-agent content repurposing system.
Contains platform configurations, user preferences, and system settings.
"""

from config.platform_config import (
    PlatformConfig,
    PlatformConstraints,
    LinkedInConfig,
    TwitterConfig,
    NewsletterConfig,
    DEFAULT_PLATFORM_CONFIG,
    get_platform_config,
)
from config.user_preferences import (
    UserPreferences,
    InputConfig,
    PipelineInputConfig,
    DEFAULT_USER_PREFERENCES,
)
from config.settings import (
    SystemSettings,
    FeedbackLoopSettings,
    ScoringWeights,
    DEFAULT_SETTINGS,
)

__all__ = [
    "PlatformConfig",
    "PlatformConstraints",
    "LinkedInConfig",
    "TwitterConfig",
    "NewsletterConfig",
    "DEFAULT_PLATFORM_CONFIG",
    "get_platform_config",
    "UserPreferences",
    "InputConfig",
    "PipelineInputConfig",
    "DEFAULT_USER_PREFERENCES",
    "SystemSettings",
    "FeedbackLoopSettings",
    "ScoringWeights",
    "DEFAULT_SETTINGS",
]
