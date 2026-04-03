"""
Pydantic schemas for structured inter-agent communication.

CLEAN DESIGN v4:
- Minimal, purposeful schemas
- Structured data passing via key point IDs
- Actionable feedback (not scores)
- Visible V1 → V2 improvements
"""

from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# SUMMARIZER SCHEMAS (Minimal - core_message + key_points only)
# ============================================================================

class KeyPoint(BaseModel):
    """
    Atomic unit of meaning - complete insight with reasoning.
    """
    id: str = Field(description="Unique identifier (e.g., 'kp_1', 'kp_2')")
    label: str = Field(description="Complete insight sentence with cause-effect")
    reason: Optional[str] = Field(
        default=None,
        description="Why this insight matters or mechanism behind it"
    )
    priority: Literal["critical", "high", "medium"] = Field(
        description="How central this point is"
    )
    type: Literal["insight", "strategy", "data"] = Field(
        description="Type of key point"
    )
    data: Optional[str] = Field(
        default=None,
        description="Optional metric or fact (e.g., '40% increase') - integrate into label if present"
    )


class SummaryOutput(BaseModel):
    """
    Output from SummarizerAgent - HIGH-QUALITY INSIGHTS ONLY.
    Only core_message + key_points (5-6 max).
    """
    core_message: str = Field(description="Sharp, conflict-based thesis (1-2 sentences)")
    key_points: List[KeyPoint] = Field(
        description="5-6 high-quality insights with complete sentences"
    )
    
    @field_validator('key_points')
    @classmethod
    def validate_key_points(cls, v: List[KeyPoint]) -> List[KeyPoint]:
        if len(v) < 3:
            raise ValueError(f"At least 3 key_points required, got {len(v)}")
        if len(v) > 6:
            raise ValueError(f"Maximum 6 key_points allowed, got {len(v)}")
        return v
    
    def get_critical_kps(self) -> List[KeyPoint]:
        """Get critical priority key points."""
        return [kp for kp in self.key_points if kp.priority == "critical"]
    
    def get_kp_ids(self) -> List[str]:
        """Get all key point IDs."""
        return [kp.id for kp in self.key_points]


# ============================================================================
# FORMATTER SCHEMAS (Platform outputs with used_kps tracking)
# ============================================================================

class LinkedInOutput(BaseModel):
    """LinkedIn post - content + which KPs were used."""
    content: str = Field(description="Full LinkedIn post (100-150 words)")
    used_kps: List[str] = Field(
        description="Key point IDs used (e.g., ['kp_1', 'kp_2'])"
    )


class TwitterOutput(BaseModel):
    """Twitter thread - tweets + which KPs were used."""
    tweets: List[str] = Field(description="List of tweets (max 7, each ≤240 chars)")
    used_kps: List[str] = Field(
        description="Key point IDs used (e.g., ['kp_1', 'kp_2', 'kp_3'])"
    )
    
    @field_validator('tweets')
    @classmethod
    def validate_tweets(cls, v: List[str]) -> List[str]:
        # Auto-truncate to max 7 tweets instead of raising error
        if len(v) > 7:
            v = v[:7]
        
        # Check individual tweet lengths
        for i, tweet in enumerate(v):
            if len(tweet) > 280:
                # Truncate long tweets
                truncated = tweet[:237]
                last_space = truncated.rfind(' ')
                if last_space > 200:
                    truncated = truncated[:last_space]
                v[i] = truncated + "..."
        
        return v


class NewsletterOutput(BaseModel):
    """Newsletter - content + which KPs were used."""
    content: str = Field(description="Full newsletter (120-200 words)")
    used_kps: List[str] = Field(
        description="Key point IDs used (e.g., ['kp_1', 'kp_2', 'kp_3', 'kp_4'])"
    )


class FormattedOutput(BaseModel):
    """Output from FormatterAgent - V1 content for all platforms."""
    version: int = Field(default=1, description="Content version")
    linkedin: LinkedInOutput = Field(description="LinkedIn post")
    twitter: TwitterOutput = Field(description="Twitter thread")
    newsletter: NewsletterOutput = Field(description="Newsletter")
    
    def get_all_used_kps(self) -> List[str]:
        """Get all unique KP IDs used across platforms."""
        all_kps = set(self.linkedin.used_kps + self.twitter.used_kps + self.newsletter.used_kps)
        return list(all_kps)


# ============================================================================
# REVIEWER SCHEMAS (Issues only - no scores)
# ============================================================================

class ReviewIssue(BaseModel):
    """
    A specific, actionable issue found by reviewer.
    """
    issue_id: str = Field(description="Unique ID (e.g., 'issue_1')")
    type: Literal["coverage", "consistency", "clarity"] = Field(
        description="Category of issue"
    )
    priority: Literal["critical", "high", "medium"] = Field(
        description="How important to fix"
    )
    problem: str = Field(description="What's wrong")
    reason: str = Field(
        description="Why it's a problem (specific)"
    )
    suggestion: str = Field(
        description="Direction on how to fix (NOT rewrite)"
    )
    affects: List[str] = Field(
        default_factory=list,
        description="Platforms affected by this issue"
    )
    missing_kps: List[str] = Field(
        default_factory=list,
        description="Missing key point IDs (for coverage issues)"
    )


class ReviewSummary(BaseModel):
    """Summary of review issues."""
    total_issues: int = Field(description="Total number of issues found")
    critical: int = Field(description="Number of critical issues") 
    high: int = Field(description="Number of high priority issues")
    medium: int = Field(description="Number of medium priority issues")


class ReviewOutput(BaseModel):
    """
    Output from ReviewerAgent - ISSUES ONLY.
    No scores, just actionable feedback.
    """
    issues: List[ReviewIssue] = Field(
        description="List of specific, actionable issues"
    )
    summary: ReviewSummary = Field(description="Issue summary")
    status: Literal["ok", "needs_fixes"] = Field(
        description="Overall status"
    )
    
    def get_critical_issues(self) -> List[ReviewIssue]:
        """Get critical priority issues."""
        return [i for i in self.issues if i.priority == "critical"]
    
    def get_issues_by_target(self, target: str) -> List[ReviewIssue]:
        """Get issues for a specific platform."""
        return [i for i in self.issues if target in i.affects]
    
    def get_coverage_issues(self) -> List[ReviewIssue]:
        """Get all coverage issues."""
        return [i for i in self.issues if i.type == "coverage"]


# ============================================================================
# REFINER SCHEMAS (Changes + updated outputs)
# ============================================================================

class Change(BaseModel):
    """A specific change made by refiner."""
    issue_id: str = Field(description="Which issue this fixes")
    action: Literal["rewrite", "add", "remove", "shorten", "restructure"] = Field(
        description="Type of change"
    )
    target: str = Field(
        description="What was changed (e.g., 'linkedin_hook', 'tweet_3')"
    )
    before: str = Field(description="Content before change")
    after: str = Field(description="Content after change")
    
    @field_validator('before', 'after', mode='before')
    @classmethod
    def convert_list_to_string(cls, v):
        """Convert lists to pipe-separated strings (for Twitter thread changes)."""
        if isinstance(v, list):
            return " | ".join(str(item) for item in v)
        return v


class RefinedOutput(BaseModel):
    """
    Output from RefinerAgent - V2 with visible changes.
    """
    version: int = Field(default=2, description="Content version")
    changes: List[Change] = Field(
        description="List of changes made with before/after"
    )
    linkedin: LinkedInOutput = Field(description="Refined LinkedIn post")
    twitter: TwitterOutput = Field(description="Refined Twitter thread")
    newsletter: NewsletterOutput = Field(description="Refined newsletter")


# ============================================================================
# PIPELINE SCHEMAS
# ============================================================================

class IterationResult(BaseModel):
    """Result of a single review-refine iteration."""
    iteration: int = Field(description="Iteration number")
    review: ReviewOutput = Field(description="Review output")
    refined: Optional[RefinedOutput] = Field(
        default=None, 
        description="Refined output"
    )
    issues_fixed: int = Field(default=0, description="Number of issues fixed")


class PipelineResult(BaseModel):
    """Final output from the complete pipeline."""
    summary: SummaryOutput = Field(description="Extracted key points")
    v1: FormattedOutput = Field(description="Initial formatted content")
    review: ReviewOutput = Field(description="Review feedback")
    v2: RefinedOutput = Field(description="Final refined content")
    iterations: List[IterationResult] = Field(
        default_factory=list,
        description="Review-refine iterations"
    )
    total_issues: int = Field(default=0, description="Total issues found")
    issues_fixed: int = Field(default=0, description="Issues fixed")


# ============================================================================
# BACKWARD COMPATIBILITY (Legacy schemas - will be deprecated)
# ============================================================================

# Legacy KeyPoint format
class SemanticKeyPoint(BaseModel):
    """Legacy: Semantic key point - use KeyPoint instead."""
    id: str = Field(description="Unique identifier")
    concept: str = Field(default="", description="Core concept")
    claim: str = Field(default="", description="Main assertion")
    implication: str = Field(default="", description="Why it matters")
    importance: Literal["critical", "high", "medium"] = Field(default="high")
    type: Literal["insight", "data_point", "strategy", "observation"] = Field(default="insight")


# Legacy LinkedIn format
class LinkedInPost(BaseModel):
    """Legacy: LinkedIn post - use LinkedInOutput instead."""
    hook: str = Field(default="", description="Opening line")
    body: str = Field(default="", description="Main content")
    call_to_action: str = Field(default="", description="CTA")
    hashtags: List[str] = Field(default_factory=list)
    source_insights: List[str] = Field(default_factory=list)
    derived_from: List[str] = Field(default_factory=list)


# Legacy Twitter format
class TweetMapping(BaseModel):
    """Legacy: Tweet mapping."""
    tweet_index: int = Field(default=0)
    derived_from: List[str] = Field(default_factory=list)


class TwitterThread(BaseModel):
    """Legacy: Twitter thread - use TwitterOutput instead."""
    tweets: List[str] = Field(default_factory=list)
    thread_hook: str = Field(default="")
    source_insights: List[str] = Field(default_factory=list)
    tweet_mappings: List[TweetMapping] = Field(default_factory=list)
    derived_from: List[str] = Field(default_factory=list)


# Legacy Newsletter format
class NewsletterSection(BaseModel):
    """Legacy: Newsletter - use NewsletterOutput instead."""
    subject_line: str = Field(default="")
    preview_text: str = Field(default="")
    intro: str = Field(default="")
    body_sections: List[str] = Field(default_factory=list)
    sections_with_traceability: List[Any] = Field(default_factory=list)
    closing: str = Field(default="")
    source_insights: List[str] = Field(default_factory=list)
    derived_from: List[str] = Field(default_factory=list)


# ============================================================================
# LEGACY SCHEMAS FOR BACKWARD COMPATIBILITY (will be deprecated)
# ============================================================================

# Legacy Review schemas (used by old orchestrator)
class FormatReview(BaseModel):
    """Legacy: Format review - use ReviewOutput.issues instead."""
    format_name: str = Field(default="")
    clarity_score: int = Field(default=8, ge=1, le=10)
    engagement_score: int = Field(default=8, ge=1, le=10)
    missing_insights: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    specific_suggestions: List[str] = Field(default_factory=list)


class PlatformFitScores(BaseModel):
    """Legacy: Platform fit scores."""
    linkedin: float = Field(default=0.8, ge=0.0, le=1.0)
    twitter: float = Field(default=0.8, ge=0.0, le=1.0)
    newsletter: float = Field(default=0.8, ge=0.0, le=1.0)


class CoverageAnalysis(BaseModel):
    """Legacy: Coverage analysis."""
    missing_key_points: List[str] = Field(default_factory=list)
    used_key_points: List[str] = Field(default_factory=list)
    coverage_by_format: Dict[str, List[str]] = Field(default_factory=dict)


class ConstraintViolation(BaseModel):
    """Legacy: Constraint violation."""
    type: str = Field(default="")
    message: str = Field(default="")
    location: str = Field(default="")
    severity: str = Field(default="warning")


class CrossFormatConsistency(BaseModel):
    """Legacy: Cross-format consistency."""
    missing_points: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    tone_mismatch: List[str] = Field(default_factory=list)
    missing_in_linkedin: List[str] = Field(default_factory=list)
    missing_in_twitter: List[str] = Field(default_factory=list)
    missing_in_newsletter: List[str] = Field(default_factory=list)


class ReviewScores(BaseModel):
    """Legacy: Review scores."""
    clarity: float = Field(default=0.8, ge=0.0, le=1.0)
    engagement: float = Field(default=0.8, ge=0.0, le=1.0)
    coverage: float = Field(default=0.8, ge=0.0, le=1.0)
    consistency: float = Field(default=0.8, ge=0.0, le=1.0)
    platform_fit: PlatformFitScores = Field(default_factory=PlatformFitScores)


# Legacy ReviewIssue (different from new ReviewIssue)
class LegacyReviewIssue(BaseModel):
    """Legacy: Review issue format."""
    id: str = Field(default="")
    type: str = Field(default="")
    description: str = Field(default="")
    target: str = Field(default="")
    affected_formats: List[str] = Field(default_factory=list)
    severity: str = Field(default="medium")
    source_insight_id: Optional[str] = None
    related_key_point: Optional[str] = None


# Legacy ReviewOutput (used by old agents)
class LegacyReviewOutput(BaseModel):
    """Legacy: Full review output - use ReviewOutput instead."""
    scores: ReviewScores = Field(default_factory=ReviewScores)
    coverage_score: int = Field(default=8, ge=1, le=10)
    clarity_score: int = Field(default=8, ge=1, le=10)
    engagement_score: int = Field(default=8, ge=1, le=10)
    consistency_score: int = Field(default=8, ge=1, le=10)
    overall_alignment_score: int = Field(default=8, ge=1, le=10)
    coverage_analysis: CoverageAnalysis = Field(default_factory=CoverageAnalysis)
    violations: List[ConstraintViolation] = Field(default_factory=list)
    cross_format_consistency: CrossFormatConsistency = Field(default_factory=CrossFormatConsistency)
    missing_points: List[str] = Field(default_factory=list)
    linkedin_review: FormatReview = Field(default_factory=FormatReview)
    twitter_review: FormatReview = Field(default_factory=FormatReview)
    newsletter_review: FormatReview = Field(default_factory=FormatReview)
    issues: List[LegacyReviewIssue] = Field(default_factory=list)
    critical_issues: List[str] = Field(default_factory=list)
    priority_improvements: List[str] = Field(default_factory=list)


# Legacy Refiner schemas
class ChangeApplied(BaseModel):
    """Legacy: Change applied."""
    issue_id: str = Field(default="")
    action: str = Field(default="modify")
    target: str = Field(default="")
    change_type: str = Field(default="")
    related_key_point: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None


class ChangeRecord(BaseModel):
    """Legacy: Change record."""
    issue_id: str = Field(default="")
    action: str = Field(default="modified")
    location: str = Field(default="")
    description: str = Field(default="")
    source_insight_id: Optional[str] = None


class LegacyRefinedOutput(BaseModel):
    """Legacy: Refined output - use RefinedOutput instead."""
    version: int = Field(default=2)
    linkedin: LinkedInPost = Field(default_factory=LinkedInPost)
    twitter: TwitterThread = Field(default_factory=TwitterThread)
    newsletter: NewsletterSection = Field(default_factory=NewsletterSection)
    changes_applied: List[ChangeApplied] = Field(default_factory=list)
    change_records: List[ChangeRecord] = Field(default_factory=list)
    changes_made: List[str] = Field(default_factory=list)
    addressed_issues: List[str] = Field(default_factory=list)


# Legacy Pipeline schemas
class VersionEntry(BaseModel):
    """Legacy: Version entry."""
    version: str = Field(default="v1")
    content: Dict[str, Any] = Field(default_factory=dict)
    score: float = Field(default=0.0)
    changes: List[str] = Field(default_factory=list)
    parent: Optional[str] = None
    timestamp: Optional[str] = None


class VersionHistory(BaseModel):
    """Legacy: Version history."""
    versions: List[VersionEntry] = Field(default_factory=list)
    current_version: str = Field(default="v1")


class LegacyIterationResult(BaseModel):
    """Legacy: Iteration result."""
    iteration: int = Field(default=1)
    review: LegacyReviewOutput = Field(default_factory=LegacyReviewOutput)
    refined: Optional[LegacyRefinedOutput] = None
    score: float = Field(default=0.0)


class LegacyPipelineResult(BaseModel):
    """Legacy: Pipeline result - use PipelineResult instead."""
    input_summary: Any = Field(default=None)
    version_1: Any = Field(default=None)
    review: LegacyReviewOutput = Field(default_factory=LegacyReviewOutput)
    version_2: LegacyRefinedOutput = Field(default_factory=LegacyRefinedOutput)
    iterations: List[LegacyIterationResult] = Field(default_factory=list)
    final_score: float = Field(default=0.0)
    version_history: VersionHistory = Field(default_factory=VersionHistory)
    total_iterations: int = Field(default=0)
    threshold_met: bool = Field(default=False)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # NEW SCHEMAS (use these)
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
    
    # Legacy (backward compatibility)
    "SemanticKeyPoint",
    "LinkedInPost",
    "TweetMapping",
    "TwitterThread",
    "NewsletterSection",
    "FormatReview",
    "PlatformFitScores",
    "CoverageAnalysis",
    "ConstraintViolation",
    "CrossFormatConsistency",
    "ReviewScores",
    "LegacyReviewIssue",
    "LegacyReviewOutput",
    "ChangeApplied",
    "ChangeRecord",
    "LegacyRefinedOutput",
    "VersionEntry",
    "VersionHistory",
    "LegacyIterationResult",
    "LegacyPipelineResult",
]
