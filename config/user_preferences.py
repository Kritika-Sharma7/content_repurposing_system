"""
User preferences and input configuration for the pipeline.
Allows users to customize output style and behavior.
"""

from typing import Literal, Optional, List
from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    """User preferences for content generation."""
    tone: Literal["professional", "conversational", "casual", "analytical", "storytelling"] = Field(
        default="professional",
        description="Overall tone preference"
    )
    audience: str = Field(
        default="general professionals",
        description="Target audience description"
    )
    goal: Literal["engagement", "education", "awareness", "conversion", "thought-leadership"] = Field(
        default="engagement",
        description="Primary content goal"
    )
    platforms: List[Literal["linkedin", "twitter", "newsletter"]] = Field(
        default=["linkedin", "twitter", "newsletter"],
        description="Platforms to generate content for"
    )
    emphasis: Optional[List[str]] = Field(
        default=None,
        description="Key points or topics to emphasize"
    )
    avoid: Optional[List[str]] = Field(
        default=None,
        description="Topics or phrases to avoid"
    )
    brand_voice: Optional[str] = Field(
        default=None,
        description="Custom brand voice guidelines"
    )


class InputConfig(BaseModel):
    """Configuration for input content handling."""
    input_type: Literal["text", "url"] = Field(
        default="text",
        description="Type of input content"
    )
    content: str = Field(
        description="The actual content or URL"
    )
    title: Optional[str] = Field(
        default=None,
        description="Optional title override"
    )
    source_attribution: Optional[str] = Field(
        default=None,
        description="Source attribution for the content"
    )


# Default user preferences
DEFAULT_USER_PREFERENCES = UserPreferences(
    tone="professional",
    audience="general professionals",
    goal="engagement",
    platforms=["linkedin", "twitter", "newsletter"]
)


class PipelineInputConfig(BaseModel):
    """Complete input configuration for the pipeline."""
    input: InputConfig = Field(description="Input content configuration")
    user_preferences: UserPreferences = Field(
        default_factory=lambda: DEFAULT_USER_PREFERENCES
    )
