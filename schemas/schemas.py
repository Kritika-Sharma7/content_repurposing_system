"""
Pydantic schemas for structured inter-agent communication.
All agents communicate using these typed data models - never raw text.

Schema contracts ensure:
- Type safety between agents
- Deterministic data flow
- Full traceability of transformations

UPGRADE v2: Enhanced with:
- Content DNA extraction (intent, tone, structure)
- Platform-aware formatting with constraints
- Multi-dimensional review with coverage analysis
- Targeted refinement with issue tracking
- Full versioning system

UPGRADE v3: Deep system upgrade with:
- Semantic KeyPoint units (id, concept, claim, implication)
- Hard constraint validation
- Strict scoring with penalties
- Diff-based versioning
"""

from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator


# ============================================================================
# SEMANTIC KEY POINT (NEW - Atomic reusable unit)
# ============================================================================

class SemanticKeyPoint(BaseModel):
    """
    Semantic unit of meaning - atomic, reusable across formats.
    Clean structure: id, concept, claim, implication, importance, type
    """
    id: str = Field(description="Unique identifier (e.g., 'kp_1', 'kp_2')")
    concept: str = Field(description="The core concept/topic (2-5 words)")
    claim: str = Field(description="The main assertion about this concept")
    implication: str = Field(description="Why this matters / the takeaway")
    importance: Literal["critical", "high", "medium"] = Field(
        default="high",
        description="How central this point is to the message"
    )
    type: Literal["insight", "data_point", "strategy", "observation"] = Field(
        default="insight",
        description="Type of key point"
    )


class KeyPointRelationship(BaseModel):
    """Relationship between two key points - shows how ideas connect."""
    from_id: str = Field(description="Source key point ID (e.g., 'kp_1')")
    to_id: str = Field(description="Target key point ID (e.g., 'kp_2')")
    relationship_type: Literal["supports", "contrasts", "extends", "depends_on", "examples"] = Field(
        description="Type of relationship"
    )
    explanation: Optional[str] = Field(
        default=None,
        description="Brief explanation of the relationship"
    )


class ContentDNA(BaseModel):
    """
    Simplified content DNA - just core_conflict and key_question.
    """
    core_conflict: Optional[str] = Field(
        default=None,
        description="The central tension or conflict being addressed"
    )
    key_question: Optional[str] = Field(
        default=None,
        description="The central question the content answers"
    )


class ExtractionTrace(BaseModel):
    """Traces a key point back to its source - proves no hallucination."""
    key_point_id: str = Field(description="The key point ID this trace is for")
    source_sentence: str = Field(description="The original sentence from the content")
    extraction_confidence: Literal["high", "medium", "low"] = Field(
        default="high",
        description="Confidence in this extraction"
    )


class SummaryQuality(BaseModel):
    """Simple quality assessment - just score and reason."""
    score: float = Field(
        default=7.0,
        ge=0.0, le=10.0,
        description="Overall quality score (0-10)"
    )
    reason: Optional[str] = Field(
        default=None,
        description="Brief explanation of the score"
    )


class ExtractionAttempt(BaseModel):
    """Record of an extraction attempt for retry visibility."""
    attempt_number: int
    key_points_count: int
    quality_score: Optional[float] = None
    success: bool
    failure_reason: Optional[str] = None


# ============================================================================
# SUMMARIZER OUTPUT SCHEMAS (Content DNA Extraction)
# ============================================================================

class KeyInsight(BaseModel):
    """A single key insight extracted from the source content."""
    id: str = Field(description="Unique identifier for traceability (e.g., 'insight_1')")
    topic: str = Field(description="Brief topic label")
    insight: str = Field(description="The core insight or takeaway")
    importance: Literal["critical", "high", "medium", "low"] = Field(description="Priority level")


class SummaryOutput(BaseModel):
    """
    Output from the SummarizerAgent - Clean, minimal structure.
    
    Fields: title, one_liner, intent, tone, structure, content_dna, 
            target_audience, key_points, summary_quality
    """
    # Core identification
    title: str = Field(description="Generated title for the content")
    one_liner: str = Field(description="Single sentence summary (hook-worthy)")
    
    # Content DNA (basic)
    intent: Literal["educational", "persuasive", "informational", "inspirational", "analytical"] = Field(
        default="informational",
        description="Primary intent of the content"
    )
    tone: Literal["informative", "analytical", "storytelling", "conversational", "formal", "provocative"] = Field(
        default="informative",
        description="Dominant tone of the content"
    )
    structure: Literal["problem-solution", "narrative", "listicle", "how-to", "case-study", "opinion", "research"] = Field(
        default="narrative",
        description="Content structure pattern"
    )
    
    # Deep Content DNA (simplified: core_conflict + key_question only)
    content_dna: Optional[ContentDNA] = Field(
        default=None,
        description="Content DNA: core_conflict and key_question"
    )
    
    # Target audience
    target_audience: str = Field(description="Who would benefit from this content")
    
    # Semantic key points (structured units)
    key_points: List[SemanticKeyPoint] = Field(
        description="Semantic units: id, concept, claim, implication, importance, type"
    )
    
    # Quality assessment (score + reason only)
    summary_quality: Optional[SummaryQuality] = Field(
        default=None,
        description="Quality assessment: score and reason"
    )
    
    # Internal fields (not exposed in clean output but kept for compatibility)
    core_message: str = Field(default="", exclude=True, description="The central thesis")
    main_theme: str = Field(default="", exclude=True, description="The overarching theme")
    word_count_original: int = Field(default=0, exclude=True, description="Original content word count")
    key_insights: List[KeyInsight] = Field(default_factory=list, exclude=True, description="Legacy field")
    
    @field_validator('key_points')
    @classmethod
    def validate_minimum_key_points(cls, v: List[SemanticKeyPoint]) -> List[SemanticKeyPoint]:
        """Validate minimum key points."""
        if len(v) < 3:
            raise ValueError(f"At least 3 key_points required, got {len(v)}")
        return v
    
    def get_key_point_by_id(self, kp_id: str) -> Optional[SemanticKeyPoint]:
        """Helper to get a key point by ID."""
        for kp in self.key_points:
            if kp.id == kp_id:
                return kp
        return None
    
    def get_key_point_ids(self) -> List[str]:
        """Get all key point IDs."""
        return [kp.id for kp in self.key_points]


# ============================================================================
# FORMATTER OUTPUT SCHEMAS (Platform-Aware, Traceable)
# ============================================================================

class DerivedContent(BaseModel):
    """Content with traceability to source key_points."""
    content: str = Field(description="The actual content")
    derived_from: List[str] = Field(
        description="Source key_points (e.g., ['key_points[0]', 'key_points[2]'])"
    )


class LinkedInPost(BaseModel):
    """LinkedIn post format with traceability."""
    hook: str = Field(description="Attention-grabbing opening line")
    body: str = Field(description="Main content body")
    call_to_action: str = Field(description="Closing CTA")
    hashtags: List[str] = Field(description="Relevant hashtags (3-5)")
    source_insights: List[str] = Field(
        default_factory=list,
        description="IDs of insights this post covers"
    )
    derived_from: List[str] = Field(
        default_factory=list,
        description="key_points indices used (e.g., ['key_points[0]', 'key_points[1]'])"
    )


class TweetMapping(BaseModel):
    """Maps a tweet to its source key points."""
    tweet_index: int = Field(description="Index of the tweet (0-based)")
    derived_from: List[str] = Field(
        description="List of key_point indices (e.g., ['key_points[0]', 'key_points[2]'])"
    )


class TweetWithTraceability(BaseModel):
    """A single tweet with traceability."""
    tweet: str = Field(description="Tweet content (max 280 chars)")
    derived_from: List[str] = Field(
        default_factory=list,
        description="key_points this tweet is derived from"
    )
    
    @field_validator('tweet')
    @classmethod
    def validate_tweet_length(cls, v: str) -> str:
        if len(v) > 280:
            raise ValueError(f"Tweet exceeds 280 characters ({len(v)} chars)")
        return v


class TwitterThread(BaseModel):
    """Twitter/X thread format with validation and traceability."""
    tweets: List[str] = Field(description="List of tweets (each max 280 chars)")
    thread_hook: str = Field(description="First tweet hook to grab attention")
    source_insights: List[str] = Field(
        default_factory=list,
        description="IDs of insights this thread covers"
    )
    tweet_mappings: List[TweetMapping] = Field(
        default_factory=list,
        description="Maps each tweet to source key_points"
    )
    derived_from: List[str] = Field(
        default_factory=list,
        description="All key_points used across the thread"
    )

    @field_validator('tweets')
    @classmethod
    def validate_tweet_length(cls, tweets: List[str]) -> List[str]:
        for i, tweet in enumerate(tweets):
            if len(tweet) > 280:
                raise ValueError(f"Tweet {i+1} exceeds 280 characters ({len(tweet)} chars)")
        return tweets


class NewsletterSectionContent(BaseModel):
    """A newsletter section with traceability."""
    content: str = Field(description="Section content")
    derived_from: List[str] = Field(
        default_factory=list,
        description="key_points this section covers"
    )


class NewsletterSection(BaseModel):
    """Newsletter format with enhanced traceability."""
    subject_line: str = Field(description="Email subject line (6-10 words)")
    preview_text: str = Field(description="Email preview snippet")
    intro: str = Field(description="Opening paragraph")
    body_sections: List[str] = Field(description="Main content sections")
    sections_with_traceability: List[NewsletterSectionContent] = Field(
        default_factory=list,
        description="Body sections with key_point traceability"
    )
    closing: str = Field(description="Closing paragraph with CTA")
    source_insights: List[str] = Field(
        default_factory=list,
        description="IDs of insights this newsletter covers"
    )
    derived_from: List[str] = Field(
        default_factory=list,
        description="All key_points used in the newsletter"
    )


class FormattedOutput(BaseModel):
    """Output from the FormatterAgent - Version 1 content."""
    version: int = Field(default=1, description="Content version number")
    linkedin: LinkedInPost = Field(description="LinkedIn post format")
    twitter: TwitterThread = Field(description="Twitter thread format")
    newsletter: NewsletterSection = Field(description="Newsletter format")


# ============================================================================
# REVIEWER OUTPUT SCHEMAS (Multi-Dimensional, Platform-Aware)
# ============================================================================

class FormatReview(BaseModel):
    """Review for a single content format."""
    format_name: str = Field(description="Name of the format reviewed")
    clarity_score: int = Field(ge=1, le=10, description="Clarity score 1-10")
    engagement_score: int = Field(ge=1, le=10, description="Engagement potential 1-10")
    missing_insights: List[str] = Field(description="IDs of key insights from summary not covered")
    strengths: List[str] = Field(description="What works well")
    weaknesses: List[str] = Field(description="Areas needing improvement")
    specific_suggestions: List[str] = Field(description="Actionable improvement suggestions")


class PlatformFitScores(BaseModel):
    """Platform-specific fit scores."""
    linkedin: float = Field(ge=0.0, le=1.0, description="LinkedIn platform fit (0-1)")
    twitter: float = Field(ge=0.0, le=1.0, description="Twitter platform fit (0-1)")
    newsletter: float = Field(ge=0.0, le=1.0, description="Newsletter platform fit (0-1)")


class CoverageAnalysis(BaseModel):
    """Analysis of key_point coverage across outputs."""
    missing_key_points: List[str] = Field(
        default_factory=list,
        description="key_points not covered in any output (e.g., ['key_points[2]'])"
    )
    used_key_points: List[str] = Field(
        default_factory=list,
        description="key_points that were used (e.g., ['key_points[0]', 'key_points[1]'])"
    )
    coverage_by_format: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Which key_points are in each format"
    )


class ConstraintViolation(BaseModel):
    """A platform constraint violation."""
    type: Literal[
        "twitter_length", 
        "thread_size", 
        "linkedin_length", 
        "newsletter_sections",
        "missing_hook",
        "hashtag_count"
    ] = Field(description="Type of violation")
    message: str = Field(description="Description of the violation")
    location: str = Field(description="Where the violation occurred")
    severity: Literal["error", "warning"] = Field(default="error")


class CrossFormatConsistency(BaseModel):
    """Cross-format consistency analysis."""
    missing_points: List[str] = Field(
        default_factory=list,
        description="Key points missing from one format but present in others"
    )
    contradictions: List[str] = Field(
        default_factory=list,
        description="Contradictory statements between formats"
    )
    tone_mismatch: List[str] = Field(
        default_factory=list,
        description="Tone inconsistencies between formats"
    )
    # Detailed per-format analysis
    missing_in_linkedin: List[str] = Field(
        default_factory=list,
        description="Key point IDs missing from LinkedIn"
    )
    missing_in_twitter: List[str] = Field(
        default_factory=list,
        description="Key point IDs missing from Twitter"
    )
    missing_in_newsletter: List[str] = Field(
        default_factory=list,
        description="Key point IDs missing from Newsletter"
    )


class ReviewIssue(BaseModel):
    """A specific issue identified by the reviewer."""
    id: str = Field(description="Unique issue identifier (e.g., 'issue_1')")
    type: Literal[
        "missing_coverage", 
        "clarity", 
        "engagement", 
        "length", 
        "consistency", 
        "platform_fit",
        "constraint_violation",
        "tone_mismatch"
    ] = Field(description="Category of issue")
    description: str = Field(description="What the issue is")
    target: str = Field(
        default="",
        description="Specific target (e.g., 'twitter_thread[2]', 'linkedin_post')"
    )
    affected_formats: List[Literal["linkedin", "twitter", "newsletter"]] = Field(
        description="Which formats have this issue"
    )
    severity: Literal["critical", "high", "medium", "low"] = Field(description="How important to fix")
    source_insight_id: Optional[str] = Field(default=None, description="Related insight ID if applicable")
    related_key_point: Optional[str] = Field(
        default=None, 
        description="Related key_point (e.g., 'key_points[2]')"
    )


class ReviewScores(BaseModel):
    """All review scores in normalized format (0-1)."""
    clarity: float = Field(ge=0.0, le=1.0, description="Overall clarity (0-1)")
    engagement: float = Field(ge=0.0, le=1.0, description="Engagement potential (0-1)")
    coverage: float = Field(ge=0.0, le=1.0, description="Key point coverage (0-1)")
    consistency: float = Field(ge=0.0, le=1.0, description="Cross-format consistency (0-1)")
    platform_fit: PlatformFitScores = Field(description="Per-platform fit scores")


class ReviewOutput(BaseModel):
    """Output from the ReviewerAgent - Enhanced multi-dimensional."""
    # Normalized scores (0-1 scale) - NEW
    scores: ReviewScores = Field(
        default_factory=lambda: ReviewScores(
            clarity=0.0, engagement=0.0, coverage=0.0, consistency=0.0,
            platform_fit=PlatformFitScores(linkedin=0.0, twitter=0.0, newsletter=0.0)
        ),
        description="All scores in normalized 0-1 format"
    )
    
    # Legacy scores (1-10 scale) - kept for backward compatibility
    coverage_score: int = Field(ge=1, le=10, description="Are ALL summary key_points covered? 1-10")
    clarity_score: int = Field(ge=1, le=10, description="Overall clarity across formats 1-10")
    engagement_score: int = Field(ge=1, le=10, description="Overall engagement potential 1-10")
    consistency_score: int = Field(ge=1, le=10, description="Consistency across formats 1-10")
    overall_alignment_score: int = Field(ge=1, le=10, description="How well formats align with summary")
    
    # Coverage analysis - NEW
    coverage_analysis: CoverageAnalysis = Field(
        default_factory=CoverageAnalysis,
        description="Detailed coverage analysis"
    )
    
    # Constraint violations - NEW
    violations: List[ConstraintViolation] = Field(
        default_factory=list,
        description="Platform constraint violations"
    )
    
    # Cross-format consistency - NEW
    cross_format_consistency: CrossFormatConsistency = Field(
        default_factory=CrossFormatConsistency,
        description="Cross-format consistency analysis"
    )
    
    # Legacy fields
    missing_points: List[str] = Field(
        default_factory=list, 
        description="Which key_points are missing and where"
    )
    
    # Per-format reviews
    linkedin_review: FormatReview = Field(description="LinkedIn post review")
    twitter_review: FormatReview = Field(description="Twitter thread review")
    newsletter_review: FormatReview = Field(description="Newsletter review")
    
    # Structured issues - enhanced
    issues: List[ReviewIssue] = Field(
        default_factory=list, 
        description="Structured issues with severity and traceability"
    )
    critical_issues: List[str] = Field(description="Must-fix issues across all formats")
    priority_improvements: List[str] = Field(description="Top 3-5 improvements to make")


# ============================================================================
# REFINER OUTPUT SCHEMAS (Targeted, Issue-Driven)
# ============================================================================

class ChangeApplied(BaseModel):
    """A specific change applied by the refiner - strictly targeted."""
    issue_id: str = Field(description="ID of the issue this change addresses")
    action: Literal["modify", "add", "remove", "restructure"] = Field(
        description="Type of change action"
    )
    target: str = Field(
        description="Specific target (e.g., 'twitter_thread[2]', 'linkedin_hook')"
    )
    change_type: Literal[
        "add_missing_key_point",
        "fix_constraint_violation",
        "improve_clarity",
        "improve_engagement",
        "fix_consistency",
        "fix_tone"
    ] = Field(description="Category of change")
    related_key_point: Optional[str] = Field(
        default=None,
        description="key_point reference (e.g., 'key_points[2]')"
    )
    before: Optional[str] = Field(default=None, description="Content before change")
    after: Optional[str] = Field(default=None, description="Content after change")


class ChangeRecord(BaseModel):
    """A specific change made by the refiner - legacy format."""
    issue_id: str = Field(description="ID of the issue this change addresses")
    action: Literal["added", "modified", "removed", "restructured"] = Field(description="Type of change")
    location: Literal[
        "linkedin_hook", "linkedin_body", "linkedin_cta", 
        "twitter_thread", "twitter_tweet",
        "newsletter_intro", "newsletter_body", "newsletter_closing",
        "newsletter_subject"
    ] = Field(description="Where the change was made")
    description: str = Field(description="What was changed")
    source_insight_id: Optional[str] = Field(default=None, description="Insight ID that motivated this change")


class RefinedOutput(BaseModel):
    """Output from the RefinerAgent - Targeted fixes only."""
    version: int = Field(default=2, description="Content version number")
    linkedin: LinkedInPost = Field(description="Refined LinkedIn post")
    twitter: TwitterThread = Field(description="Refined Twitter thread")
    newsletter: NewsletterSection = Field(description="Refined newsletter")
    
    # Enhanced change tracking - NEW
    changes_applied: List[ChangeApplied] = Field(
        default_factory=list,
        description="Structured changes with issue references"
    )
    
    # Legacy change tracking
    change_records: List[ChangeRecord] = Field(
        default_factory=list, 
        description="Structured change tracking"
    )
    changes_made: List[str] = Field(description="Summary of improvements made")
    addressed_issues: List[str] = Field(description="Which review issue IDs were addressed")


# ============================================================================
# PIPELINE & VERSIONING SCHEMAS
# ============================================================================

class VersionEntry(BaseModel):
    """A single version in the version history."""
    version: str = Field(description="Version identifier (e.g., 'v1', 'v2')")
    content: Dict[str, Any] = Field(description="The formatted content at this version")
    score: float = Field(description="Composite score for this version (0-1)")
    changes: List[str] = Field(
        default_factory=list,
        description="Changes made from previous version"
    )
    parent: Optional[str] = Field(
        default=None,
        description="Parent version identifier"
    )
    timestamp: Optional[str] = Field(default=None, description="When this version was created")


class VersionHistory(BaseModel):
    """Complete version history for the pipeline output."""
    versions: List[VersionEntry] = Field(
        default_factory=list,
        description="All versions in order"
    )
    current_version: str = Field(default="v1", description="Current/final version")


class IterationResult(BaseModel):
    """Result of a single review-refine iteration."""
    iteration: int = Field(description="Iteration number (1, 2, ...)")
    review: ReviewOutput = Field(description="Review from this iteration")
    refined: Optional[RefinedOutput] = Field(default=None, description="Refined output if refinement was done")
    score: float = Field(description="Composite score for this iteration (0-1 normalized)")


class PipelineResult(BaseModel):
    """Final output from the complete pipeline."""
    input_summary: SummaryOutput = Field(description="Summary of original content (Content DNA)")
    version_1: FormattedOutput = Field(description="Initial formatted content")
    review: ReviewOutput = Field(description="Final review feedback")
    version_2: RefinedOutput = Field(description="Final refined content")
    iterations: List[IterationResult] = Field(
        default_factory=list, 
        description="History of review-refine iterations"
    )
    final_score: float = Field(default=0.0, description="Final composite quality score (0-1)")
    
    # Enhanced versioning - NEW
    version_history: VersionHistory = Field(
        default_factory=VersionHistory,
        description="Complete version history with diffs"
    )
    
    # Metadata
    total_iterations: int = Field(default=0, description="Total iterations performed")
    threshold_met: bool = Field(default=False, description="Whether quality threshold was met")


# Initialize package
__all__ = [
    # Semantic Key Point (NEW)
    "SemanticKeyPoint",
    # Summary
    "KeyInsight",
    "SummaryOutput",
    # Formatter
    "DerivedContent",
    "LinkedInPost",
    "TweetMapping",
    "TweetWithTraceability",
    "TwitterThread",
    "NewsletterSectionContent",
    "NewsletterSection",
    "FormattedOutput",
    # Reviewer
    "FormatReview",
    "PlatformFitScores",
    "CoverageAnalysis",
    "ConstraintViolation",
    "CrossFormatConsistency",
    "ReviewIssue",
    "ReviewScores",
    "ReviewOutput",
    # Refiner
    "ChangeApplied",
    "ChangeRecord",
    "RefinedOutput",
    # Pipeline
    "VersionEntry",
    "VersionHistory",
    "IterationResult",
    "PipelineResult",
]
