"""
System settings for the multi-agent pipeline.
Controls iteration thresholds, retries, and other system-level behavior.

UPGRADE v3: Stricter settings for better feedback loop demonstration.
"""

from pydantic import BaseModel, Field


class FeedbackLoopSettings(BaseModel):
    """Settings for the feedback loop mechanism."""
    score_threshold: float = Field(
        default=0.90,  # Increased from 0.85 for stricter validation
        ge=0.0,
        le=1.0,
        description="Minimum normalized score to accept (0-1 scale)"
    )
    max_iterations: int = Field(
        default=2,
        ge=1,
        le=5,
        description="Maximum refinement iterations"
    )
    min_key_points: int = Field(
        default=4,  # Increased from 3
        ge=1,
        description="Minimum key_points required from summarizer"
    )
    retry_summarizer_on_failure: bool = Field(
        default=True,
        description="Whether to retry summarizer if key_points < min_key_points"
    )
    max_summarizer_retries: int = Field(
        default=2,
        ge=1,
        description="Maximum summarizer retry attempts"
    )
    force_at_least_one_iteration: bool = Field(
        default=True,  # NEW: Forces feedback loop demonstration
        description="Force at least one refinement iteration even if V1 meets threshold"
    )
    perfect_score_penalty: float = Field(
        default=0.05,  # NEW: Prevents "cheerleader" 100% scores
        description="Penalty applied when reviewer gives perfect scores (prevents unrealistic scoring)"
    )


class ScoringWeights(BaseModel):
    """Weights for computing composite scores."""
    clarity: float = Field(default=0.20, ge=0.0, le=1.0)
    engagement: float = Field(default=0.20, ge=0.0, le=1.0)
    coverage: float = Field(default=0.25, ge=0.0, le=1.0)  # Coverage is weighted highest
    consistency: float = Field(default=0.15, ge=0.0, le=1.0)
    platform_fit: float = Field(default=0.20, ge=0.0, le=1.0)


class SystemSettings(BaseModel):
    """Complete system settings."""
    feedback_loop: FeedbackLoopSettings = Field(
        default_factory=FeedbackLoopSettings
    )
    scoring_weights: ScoringWeights = Field(
        default_factory=ScoringWeights
    )
    verbose: bool = Field(
        default=True,
        description="Enable verbose logging"
    )
    save_intermediate_results: bool = Field(
        default=False,
        description="Save intermediate pipeline results"
    )
    strict_constraint_validation: bool = Field(
        default=True,  # NEW: Enables hard constraint checking
        description="Enforce hard platform constraints (tweet length, thread size, etc.)"
    )


# Default system settings - STRICT MODE
DEFAULT_SETTINGS = SystemSettings(
    feedback_loop=FeedbackLoopSettings(
        score_threshold=0.90,  # Stricter threshold
        max_iterations=2,
        min_key_points=4,
        retry_summarizer_on_failure=True,
        max_summarizer_retries=2,
        force_at_least_one_iteration=True,
        perfect_score_penalty=0.05
    ),
    scoring_weights=ScoringWeights(
        clarity=0.20,
        engagement=0.20,
        coverage=0.25,
        consistency=0.15,
        platform_fit=0.20
    ),
    verbose=True,
    save_intermediate_results=False,
    strict_constraint_validation=True
)

# Alias for backward compatibility
settings = DEFAULT_SETTINGS
