"""
Schema exports for multi-agent content system.

CLEAN DESIGN v4: Export new schemas + legacy for backward compatibility.
"""

# New schemas (use these)
from schemas.schemas import (
    KeyPoint,
    SummaryOutput,
    LinkedInOutput,
    TwitterOutput,
    NewsletterOutput,
    FormattedOutput,
    ReviewIssue,
    ReviewOutput,
    Change,
    RefinedOutput,
    IterationResult,
    PipelineResult,
)

# Legacy schemas (backward compatibility)
from schemas.schemas import (
    SemanticKeyPoint,
    LinkedInPost,
    TwitterThread,
    NewsletterSection,
    FormatReview,
    LegacyReviewOutput,
    LegacyRefinedOutput,
    LegacyPipelineResult,
)

__all__ = [
    # New schemas
    "KeyPoint",
    "SummaryOutput",
    "LinkedInOutput",
    "TwitterOutput",
    "NewsletterOutput",
    "FormattedOutput",
    "ReviewIssue",
    "ReviewOutput",
    "Change",
    "RefinedOutput",
    "IterationResult",
    "PipelineResult",
    # Legacy
    "SemanticKeyPoint",
    "LinkedInPost",
    "TwitterThread",
    "NewsletterSection",
    "FormatReview",
    "LegacyReviewOutput",
    "LegacyRefinedOutput",
    "LegacyPipelineResult",
]
