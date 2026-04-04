# ContentForge - Multi-Agent Content Repurposing System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o-green.svg" alt="OpenAI GPT-4o">
  <img src="https://img.shields.io/badge/Pydantic-v2-orange.svg" alt="Pydantic v2">
  <img src="https://img.shields.io/badge/FastAPI-Backend-teal.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-Frontend-cyan.svg" alt="React">
</p>

A disciplined multi-agent system that transforms long-form content into platform-optimized outputs for LinkedIn, Twitter/X, and newsletters. Built with explicit orchestration, structured data passing, and iterative quality refinement through feedback loops.

## Overview

This system demonstrates a production-grade multi-agent architecture designed to address the core challenge of content repurposing: maintaining quality and consistency across platforms while adapting to platform-specific constraints. Unlike monolithic LLM approaches, this implementation uses specialized agents with clearly defined responsibilities, structured data contracts, and measurable quality improvements through iterative refinement.

## System Architecture

### Workflow Design

The system implements a disciplined pipeline with clear separation of concerns:

```
Input Content → Summarizer → Formatter → [Reviewer ↔ Refiner] → Final Output
```

**Key Design Principles:**
- **Explicit Orchestration**: No framework abstractions (LangChain, CrewAI). Direct control over agent interactions.
- **Structured Data Passing**: All inter-agent communication uses typed Pydantic schemas, not raw text.
- **Iterative Refinement**: Mandatory feedback loop between Reviewer and Refiner agents.
- **Version Tracking**: Clear V1 → V2 → V3 progression with change logs.
- **Single Responsibility**: Each agent has one well-defined job.

### Agent Roles

| Agent | Responsibility | Input Schema | Output Schema | Purpose |
|-------|---------------|--------------|---------------|---------|
| **Summarizer** | Extract core message and prioritized key points | Raw text | `SummaryOutput` | Content analysis and semantic extraction |
| **Formatter** | Create platform-specific content (LinkedIn, Twitter, Newsletter) | `SummaryOutput` | `FormattedOutput` | Platform adaptation with constraint awareness |
| **Reviewer** | Evaluate content quality, identify coverage gaps and issues | `SummaryOutput` + `FormattedOutput` | `ReviewOutput` | Quality assurance and issue detection |
| **Refiner** | Apply targeted fixes based on reviewer feedback | `SummaryOutput` + `FormattedOutput` + `ReviewOutput` | `RefinedOutput` | Iterative improvement with change tracking |

### Data Flow

```
┌─────────────────┐
│  Raw Content    │
│  (Article/Post) │
└────────┬────────┘
         │
         v
┌────────────────────────────┐
│   Summarizer Agent         │
│  - Extract core message    │
│  - Identify key points     │
│  - Assign priorities       │
└────────┬───────────────────┘
         │
         v
    SummaryOutput
    {
      core_message: str
      key_points: [
        {label, priority, data}
      ]
    }
         │
         v
┌────────────────────────────┐
│   Formatter Agent          │
│  - LinkedIn post           │
│  - Twitter thread (5-8)    │
│  - Newsletter section      │
└────────┬───────────────────┘
         │
         v
    FormattedOutput (V1)
    {
      linkedin: {content, used_kps}
      twitter: {tweets[], used_kps}
      newsletter: {content, used_kps}
    }
         │
         ├────────────────────┐
         │                    │
         v                    v
┌────────────────┐    ┌──────────────┐
│ Reviewer Agent │    │              │
│ - Check gaps   │    │              │
│ - Find issues  │    │              │
│ - Score content│    │              │
└────────┬───────┘    │              │
         │            │              │
         v            │              │
    ReviewOutput      │              │
    {                 │              │
      issues: [       │              │
        {id, priority,│              │
         problem, fix}│              │
      ]               │              │
      status: str     │              │
    }                 │              │
         │            │              │
         v            │              │
┌────────────────────┐│              │
│  Refiner Agent     ││              │
│ - Apply fixes 1:1  ││              │
│ - Track changes    │◄──────────────┘
│ - Generate V2      │   (uses V1)
└────────┬───────────┘
         │
         v
    RefinedOutput (V2)
    {
      version: 2
      changes: [
        {issue_id, action, target}
      ]
      linkedin: {...}
      twitter: {...}
      newsletter: {...}
    }
```

### Feedback Loop Mechanism

The system implements a convergent feedback loop with multiple stop conditions:

```python
while iteration < max_iterations:
    # 1. Review current version
    review = reviewer.run(summary, current_output)
    
    # 2. Check stop conditions
    if review.issues_count == 0:
        break  # Quality threshold met
    
    # 3. Apply refinements
    refined = refiner.run(summary, current_output, review)
    
    # 4. Track changes and continue
    current_output = refined
    iteration += 1
```

**Stop Conditions:**
1. No issues found (quality threshold met)
2. No changes made by refiner (unable to improve)
3. Content unchanged (no-op detected)
4. Maximum iterations reached (safety limit)

**Iteration Tracking:**
- Each iteration stores: review feedback, refinements made, issues fixed
- Full traceability: Any change in V2/V3 can be traced to a specific review issue
- Quality metrics: Issues found vs. issues fixed across all iterations

## Key Features

### Core Capabilities
- **Multi-Agent Architecture**: Four specialized agents with distinct responsibilities
- **Structured Data Passing**: Typed Pydantic schemas ensure type safety and contract clarity
- **Iterative Refinement**: Automatic review-refine loop with convergence detection
- **Version Control**: Complete V1 → V2 → V3 tracking with change logs
- **Platform Optimization**: Content adapted for LinkedIn, Twitter/X threads, and newsletters
- **Quality Assurance**: Automated issue detection and targeted fixes
- **Traceability**: Every output element traces to original key points
- **Configuration**: User preferences for tone, audience, and content goals

### Platform-Specific Outputs

| Platform | Format | Constraints |
|----------|--------|-------------|
| **LinkedIn** | Professional post with hook, body, CTA | ~200-300 words, storytelling format |
| **Twitter/X** | Thread (5-8 tweets) | ≤280 characters per tweet, sequential flow |
| **Newsletter** | Email section with bullets | Scannable format, clear structure |

### Technical Implementation
- **No Framework Dependencies**: Direct agent orchestration without LangChain or CrewAI
- **Type Safety**: Pydantic v2 models for all data structures
- **Error Handling**: Graceful degradation with detailed error messages
- **API Cost Control**: Bounded iteration limits with quality thresholds
- **Modern Stack**: FastAPI backend, React frontend, Python 3.10+

## Design Principles

This system adheres to strict architectural principles:

1. **Disciplined Workflow**: Each agent has a single, well-defined responsibility
2. **No Black-Box Chaining**: All agent interactions are explicit and traceable
3. **1:1 Issue Mapping**: Every reviewer issue gets exactly one refiner fix
4. **Quality Gates**: Reviewer prevents low-quality content from passing through
5. **Structured Communication**: All data passed between agents uses typed schemas
6. **Convergence Control**: Loop terminates on quality threshold or iteration limit
7. **Full Transparency**: Every change is logged with clear before/after states

## System Requirements

### Prerequisites
- Python 3.10 or higher
- Node.js 16+ (for React UI)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Dependencies
- **Backend**: FastAPI, Pydantic v2, OpenAI Python SDK, python-dotenv
- **Frontend**: React 18, Vite, TailwindCSS
- **LLM**: OpenAI GPT-4o (configurable to other models)

## Project Structure

```
multi-agent-content/
├── agents/                    # Agent implementations
│   ├── summarizer.py         # Key point extraction and prioritization
│   ├── formatter.py          # Platform-specific content generation
│   ├── reviewer.py           # Quality evaluation and issue detection
│   └── refiner.py            # Targeted improvement and change tracking
├── schemas/
│   └── schemas.py            # Pydantic data models and contracts
├── pipeline/
│   └── orchestrator.py       # Workflow coordination and feedback loop
├── config/
│   ├── user_preferences.py   # User preference models
│   ├── platform_config.py    # Platform constraints and rules
│   └── settings.py           # System configuration
├── utils/
│   ├── llm.py                # OpenAI API client wrapper
│   └── content_fetcher.py    # URL content extraction
├── react-ui/                 # Modern React frontend
│   ├── src/
│   │   ├── pages/            # Page components
│   │   ├── components/       # Reusable UI components
│   │   └── App.jsx           # Main application
│   ├── public/
│   └── package.json
├── api_server.py             # FastAPI backend server
├── main.py                   # CLI entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── README.md                 # Documentation
└── output/                   # Generated results (gitignored)
```

## Installation

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd multi-agent-content
```

### Step 2: Python Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Required:
OPENAI_API_KEY=sk-your-api-key-here

# Optional:
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.7
```

### Step 4: Frontend Setup (Optional)

```bash
cd react-ui
npm install
cd ..
```

## Usage

### Option 1: React UI (Recommended)

Start the backend API and frontend development server:

```bash
# Terminal 1: Start backend
python api_server.py

# Terminal 2: Start frontend
cd react-ui
npm run dev
```

Access the application at `http://localhost:5173`

**Features:**
- Modern, responsive interface
- Real-time pipeline execution
- Platform-specific previews (LinkedIn, Twitter, Newsletter)
- Version comparison (V1 vs V2 vs V3)
- Interactive workflow visualization
- Export functionality

### Option 2: Command Line Interface

```bash
# Run with sample content
python main.py --sample

# Run with file input
python main.py --file article.txt

# Run with custom preferences
python main.py --file article.txt \
  --tone professional \
  --audience "business leaders" \
  --platforms linkedin twitter newsletter

# Show detailed comparison
python main.py --sample --show-comparison
```

**CLI Options:**

| Flag | Description | Example |
|------|-------------|---------|
| `--input`, `-i` | Direct text input | `--input "Article text..."` |
| `--file`, `-f` | Input file path | `--file document.txt` |
| `--sample`, `-s` | Use built-in sample | `--sample` |
| `--output`, `-o` | Output directory | `--output ./results` |
| `--tone` | Content tone | `--tone conversational` |
| `--audience` | Target audience | `--audience developers` |
| `--platforms` | Output platforms | `--platforms linkedin twitter` |
| `--show-comparison` | Display V1 vs V2 diff | `--show-comparison` |
| `--quiet`, `-q` | Minimal output | `--quiet` |

### Option 3: Programmatic API

```python
from pipeline.orchestrator import PipelineOrchestrator
from config.user_preferences import UserPreferences

# Initialize orchestrator
pipeline = PipelineOrchestrator(
    verbose=True,
    max_iterations=5
)

# Configure user preferences
prefs = UserPreferences(
    tone="professional",
    audience="startup founders",
    platforms=["linkedin", "twitter", "newsletter"]
)

# Run pipeline
content = """
Your long-form article or blog post content here...
"""

result = pipeline.run(content, user_preferences=prefs)

# Access outputs
print("Core Message:", result.summary.core_message)
print("Key Points:", len(result.summary.key_points))
print("LinkedIn Post:", result.v2.linkedin.content)
print("Twitter Thread:", len(result.v2.twitter.tweets), "tweets")
print("Issues Found:", result.total_issues)
print("Issues Fixed:", result.issues_fixed)
```

## Specification Compliance

This system is designed to meet the following core requirements:

### 1. Workflow Structure
**Requirement**: Input Content → Summarization → Format Conversion → Quality Check → Final Outputs

**Implementation**:
```
Raw Content → SummarizerAgent → FormatterAgent → ReviewerAgent → RefinerAgent → Final Output
```
- Clear linear progression through specialized agents
- Each stage has well-defined inputs and outputs
- No skipped stages or black-box shortcuts

### 2. Agent Separation of Responsibilities
**Requirement**: Each agent has a distinct, non-overlapping role

**Implementation**:

| Agent | Sole Responsibility | Does NOT Do |
|-------|---------------------|-------------|
| **Summarizer** | Extract key points and core message | Format content, evaluate quality, refine |
| **Formatter** | Create platform-specific content | Summarize, review quality, fix issues |
| **Reviewer** | Identify quality issues and gaps | Generate content, apply fixes |
| **Refiner** | Apply targeted fixes to content | Summarize, format from scratch, review |

### 3. Structured Data Passing
**Requirement**: Agents must pass structured data, not just raw text

**Implementation**:
- All inter-agent communication uses Pydantic v2 typed models
- `SummaryOutput`: Contains `core_message` (str) and `key_points` (list of KeyPoint objects)
- `FormattedOutput`: Contains `linkedin`, `twitter`, `newsletter` objects with metadata
- `ReviewOutput`: Contains `issues` (list of Issue objects), `status`, priority levels
- `RefinedOutput`: Contains platform outputs + `changes` (list of Change objects)
- No raw string passing between agents

### 4. Feedback Loop Implementation
**Requirement**: At least one feedback loop (review → refine)

**Implementation**:
```python
for iteration in range(1, max_iterations + 1):
    # Review current version
    review = reviewer.run(summary, current_output)
    
    # Stop if quality threshold met
    if review.issues_count == 0:
        break
    
    # Refine based on feedback
    refined = refiner.run(summary, current_output, review)
    
    # Update for next iteration
    current_output = refined
```

**Evidence**: 
- V1 (11 issues) → Refiner fixes → V2 (6 issues) → Refiner fixes → V3 (0 issues)
- Each iteration logged with issues found and changes made
- Clear convergence pattern

### 5. Versioning
**Requirement**: Maintain versioning (before vs after refinement)

**Implementation**:
- `FormattedOutput` = V1 (initial formatted content)
- `RefinedOutput` with version=2 = V2 (after first refinement)
- `RefinedOutput` with version=3 = V3 (after second refinement)
- Each version stored in `PipelineResult.v1`, `PipelineResult.v2`, `PipelineResult.v3`
- Change logs track every modification between versions

### 6. No Single-Prompt Solution
**Requirement**: Avoid monolithic "do everything" prompts

**Implementation**:
- 4 separate agent classes with distinct system prompts
- Each agent has a specialized role and output schema
- No agent attempts to perform another agent's job
- Clear separation in `/agents` directory

### 7. No Black-Box Chaining
**Requirement**: Transparent, traceable workflow

**Implementation**:
- Direct orchestration in `orchestrator.py` (no LangChain, CrewAI, etc.)
- Every data transformation is explicit: `output = agent.run(input)`
- Full logging of each stage with input/output visibility
- Change tracking: Every fix in V2/V3 traces to a specific review issue

### 8. Clear System Design
**Requirement**: Focus on clarity of architecture over UI polish

**Implementation**:
- Explicit pipeline in `orchestrator.py` with documented control flow
- Typed schemas in `schemas.py` show data contracts
- Agent implementations in separate files with single responsibilities
- Comprehensive logging shows execution flow
- Architecture diagram in README demonstrates design

## Example Pipeline Execution

### Input
```text
Agentic payment systems are transforming how digital transactions are executed 
by embedding decision-making directly into the payment infrastructure. Unlike 
traditional systems that rely heavily on intermediaries such as banks or payment 
gateways, agentic systems operate through predefined rules and smart logic.

[... 200 more words ...]
```

### Stage 1: Summarizer Output
```json
{
  "core_message": "Agentic payment systems challenge conventional transaction metrics by embedding decision-making into the infrastructure, but this autonomy complicates the evaluation of success and increases the risk of large-scale errors.",
  "key_points": [
    {
      "label": "Agentic payment systems reduce transaction delays...",
      "priority": "critical",
      "data": "automation benefits"
    },
    {
      "label": "Traditional metrics are insufficient...",
      "priority": "critical",
      "data": "evaluation challenges"
    },
    {
      "label": "Errors in logic can lead to scale issues...",
      "priority": "critical",
      "data": "risk management"
    }
    // ... 2 more key points
  ]
}
```

### Stage 2: Formatter Output (V1)
```json
{
  "linkedin": {
    "content": "We once believed that more automation in payment systems would simplify everything. We were wrong...",
    "used_kps": [0, 1, 2, 3, 4]
  },
  "twitter": {
    "tweets": [
      "Most teams think automating payments simplifies everything...",
      "Agentic systems reduce delays and overhead...",
      // ... 4 more tweets
    ],
    "used_kps": [0, 1, 2, 3, 4]
  },
  "newsletter": {
    "content": "Hello Reader,\n\nRethinking Metrics for Agentic Payment Systems...",
    "used_kps": [0, 1, 2, 3, 4]
  }
}
```

### Stage 3: Reviewer Output (Iteration 1)
```json
{
  "status": "needs_improvement",
  "issues": [
    {
      "issue_id": "kp_0_missing_linkedin",
      "priority": "critical",
      "problem": "Errors in logic point missing in LinkedIn",
      "suggested_fix": "Ensure error monitoring point is clearly included"
    },
    // ... 10 more issues
  ],
  "issues_count": 11
}
```

### Stage 4: Refiner Output (V2)
```json
{
  "version": 2,
  "changes": [
    {
      "issue_id": "kp_0_missing_linkedin",
      "action": "integrate",
      "target": "linkedin",
      "old_text": "The takeaway? Embrace new metrics...",
      "new_text": "Errors in logic or poorly defined rules... The takeaway? Embrace new metrics..."
    },
    // ... 10 more changes
  ],
  "linkedin": { "content": "..." },
  "twitter": { "tweets": [...] },
  "newsletter": { "content": "..." }
}
```

### Stage 5: Reviewer Output (Iteration 2)
```json
{
  "status": "needs_improvement",
  "issues": [
    {
      "issue_id": "kp_1_weak_twitter",
      "priority": "high",
      "problem": "Traditional metrics point weakly expressed in Twitter",
      "suggested_fix": "Strengthen with cause-effect reasoning"
    },
    // ... 5 more issues
  ],
  "issues_count": 6
}
```

### Stage 6: Refiner Output (V3)
```json
{
  "version": 3,
  "changes": [
    {
      "issue_id": "kp_1_weak_twitter",
      "action": "integrate",
      "target": "twitter",
      "old_text": "Traditional metrics like speed and success rate fall short...",
      "new_text": "Traditional metrics like speed and success rate fall short... We need new metrics focusing on user behavior and trust, as these determine how well systems handle real-world conditions..."
    },
    // ... 5 more changes
  ],
  "linkedin": { "content": "..." },
  "twitter": { "tweets": [...] },
  "newsletter": { "content": "..." }
}
```

### Stage 7: Reviewer Output (Iteration 3)
```json
{
  "status": "ok",
  "issues": [],
  "issues_count": 0
}
```

### Final Result
```json
{
  "summary": { /* SummaryOutput */ },
  "v1": { /* FormattedOutput */ },
  "review_v1": { /* ReviewOutput with 11 issues */ },
  "v2": { /* RefinedOutput with 11 changes */ },
  "review_v2": { /* ReviewOutput with 6 issues */ },
  "v3": { /* RefinedOutput with 6 changes */ },
  "review_v3": { /* ReviewOutput with 0 issues */ },
  "iterations": 3,
  "total_issues": 17,
  "issues_fixed": 17
}
```

**Quality Progression**: 11 issues → 6 issues → 0 issues (clear convergence)

## Performance Metrics

### Typical Execution
- **Processing Time**: 30-60 seconds (depending on content length)
- **API Calls**: 8-12 calls per run (summarizer, formatter, 2-3 review-refine cycles)
- **Iterations**: 2-3 on average before convergence
- **Quality Score**: 90-100% (based on issue resolution)
orchestrator.save_results(result, "outputs")
```


## Data Schemas

All agent communication uses strictly typed Pydantic models:

### SummaryOutput
```python
class KeyPoint(BaseModel):
    label: str              # The key insight text
    priority: str           # "critical" | "high" | "medium"
    data: Optional[str]     # Supporting data or category

class SummaryOutput(BaseModel):
    core_message: str       # Central thesis
    key_points: List[KeyPoint]  # Prioritized insights
```

### FormattedOutput (V1)
```python
class FormattedOutput(BaseModel):
    linkedin: LinkedInOutput
    twitter: TwitterOutput
    newsletter: NewsletterOutput
    
class LinkedInOutput(BaseModel):
    content: str
    used_kps: List[int]     # Tracks which key points were used

class TwitterOutput(BaseModel):
    tweets: List[str]       # Thread of 5-8 tweets
    used_kps: List[int]
    
class NewsletterOutput(BaseModel):
    content: str            # Full newsletter section
    used_kps: List[int]
```

### ReviewOutput
```python
class Issue(BaseModel):
    issue_id: str           # Unique identifier
    priority: str           # "critical" | "high" | "medium"
    problem: str            # Description of the issue
    suggested_fix: str      # Actionable suggestion
    
class ReviewOutput(BaseModel):
    status: str             # "ok" | "needs_improvement"
    issues: List[Issue]
    issues_count: int
```

### RefinedOutput (V2, V3, ...)
```python
class Change(BaseModel):
    issue_id: str           # Maps to ReviewOutput.issues
    action: str             # "integrate" | "rewrite" | "remove"
    target: str             # "linkedin" | "twitter" | "newsletter"
    old_text: str           # Before refinement
    new_text: str           # After refinement
    
class RefinedOutput(BaseModel):
    version: int            # 2, 3, 4, ...
    changes: List[Change]   # All modifications made
    linkedin: LinkedInOutput
    twitter: TwitterOutput
    newsletter: NewsletterOutput
```

## Testing

Run the test suite to verify system functionality:

```bash
# Test pipeline execution
python test_pipeline.py

# Test individual agents
python test_imports.py

# Test newsletter depth evaluation
python test_newsletter_depth_check.py

# Test reviewer strictness
python test_reviewer_strict.py
```

## Contributing

Contributions are welcome. Please follow these guidelines:

1. **Code Style**: Follow PEP 8 for Python code
2. **Type Hints**: All functions must have type annotations
3. **Documentation**: Update README and docstrings for new features
4. **Testing**: Add tests for new functionality
5. **Schemas**: Any data structure changes require schema updates

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Contact

For questions, issues, or feedback, please open an issue on GitHub or contact the maintainer.

---

**Built with disciplined multi-agent architecture. No black-box frameworks. Full transparency.**

All inter-agent communication uses typed Pydantic models for type safety and validation.

### SummaryOutput (Updated v3)

Clean, minimal structure with semantic key points:

```python
{
  "title": str,
  "one_liner": str,
  "intent": "educational | persuasive | informational | inspirational | analytical",
  "tone": "informative | analytical | storytelling | conversational | formal | provocative",
  "structure": "problem-solution | narrative | listicle | how-to | case-study | opinion | research",
  "content_dna": {
    "core_conflict": str,  # Central tension being addressed
    "key_question": str    # Question the content answers
  },
  "target_audience": str,
  "key_points": [
    {
      "id": "kp_1",
      "concept": str,       # Core concept (2-5 words)
      "claim": str,         # Main assertion
      "implication": str,   # Why it matters
      "importance": "critical | high | medium",
      "type": "insight | data_point | strategy | observation"
    }
  ],
  "summary_quality": {
    "score": float,  # 0-10
    "reason": str
  }
}
```

### FormattedOutput (V1)

Platform-specific content with traceability:

```python
{
  "version": 1,
  "linkedin": {
    "hook": str,                    # Attention-grabbing opening
    "body": str,                    # Main content
    "call_to_action": str,          # Closing CTA
    "hashtags": [str],              # 3-5 hashtags
    "derived_from": [str]           # Source key_point IDs
  },
  "twitter": {
    "thread_hook": str,
    "tweets": [str],                # Each ≤280 chars
    "derived_from": [str]
  },
  "newsletter": {
    "subject_line": str,
    "preview_text": str,
    "intro": str,
    "body_sections": [str],
    "closing": str,
    "derived_from": [str]
  }
}
```

### ReviewOutput

Multi-dimensional quality assessment:

```python
{
  "overall_alignment_score": int,   # 1-10
  "consistency_score": int,         # 1-10
  "linkedin_review": {
    "score": int,
    "strengths": [str],
    "weaknesses": [str],
    "specific_issues": [str]
  },
  "twitter_review": FormatReview,
  "newsletter_review": FormatReview,
  "critical_issues": [str],
  "priority_improvements": [str],
  "key_point_coverage": {
    "kp_1": ["linkedin", "twitter"],  # Which formats used this point
    "kp_2": ["newsletter"]
  }
}
```

### RefinedOutput (V2)

Improved content with documented changes:

```python
{
  "version": 2,
  "linkedin": LinkedInPost,
  "twitter": TwitterThread,
  "newsletter": NewsletterSection,
  "changes_made": [str],           # List of improvements
  "addressed_issues": [str],       # Issues fixed from review
  "refinement_quality": {
    "improvement_score": float,    # How much better than V1
    "confidence": str
  }
}
```

## 📤 Output Files

Results are automatically saved to timestamped JSON files:

```
outputs/
├── summary_20260402_153045.json          # Content DNA extraction
├── version_1_20260402_153045.json        # Initial formatted content
├── review_20260402_153045.json           # Quality evaluation
├── version_2_20260402_153045.json        # Refined content
└── pipeline_result_20260402_153045.json  # Complete pipeline result
```

Each file contains structured, human-readable JSON with full traceability.

## 🎯 Design Principles

### 1. **Explicit Orchestration**
No black-box frameworks (LangChain, CrewAI, AutoGPT). Every agent interaction is explicit and traceable.

### 2. **Type-Safe Communication**
All agents communicate via typed Pydantic models with full validation. No loose dictionaries or unstructured data.

### 3. **Feedback-Driven Quality**
Mandatory review → refine loop ensures outputs meet quality standards. No one-shot generation.

### 4. **Version Tracking**
Clear V1/V2 comparison with documented changes. Users see exactly what improved.

### 5. **Modularity & Testability**
Each agent is independent, single-purpose, and testable in isolation.

### 6. **Content DNA Extraction**
Semantic key points are atomic, reusable units that maintain traceability from source to output.

### 7. **Platform Awareness**
Each format respects platform constraints (character limits, structure requirements, hashtag conventions).

## 🔄 How It Works

### The 4-Agent Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                      Raw Content                            │
│              (Article, Blog Post, Report)                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  1. SUMMARIZER AGENT                        │
│  • Extracts Content DNA (core_conflict, key_question)      │
│  • Identifies 4-8 semantic key points                      │
│  • Determines intent, tone, structure                      │
│  • Assesses quality score                                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ SummaryOutput
                            │
┌─────────────────────────────────────────────────────────────┐
│                  2. FORMATTER AGENT                         │
│  • Creates LinkedIn post (hook, body, CTA, hashtags)       │
│  • Generates Twitter thread (5-8 tweets, ≤280 chars)       │
│  • Composes Newsletter (subject, intro, sections)          │
│  • Links each output to source key points                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ FormattedOutput (V1)
                            │
┌─────────────────────────────────────────────────────────────┐
│                   3. REVIEWER AGENT                         │
│  • Scores alignment (1-10)                                  │
│  • Evaluates consistency across formats                    │
│  • Identifies critical issues                              │
│  • Suggests priority improvements                          │
│  • Checks key point coverage                               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ ReviewOutput
                            │
┌─────────────────────────────────────────────────────────────┐
│                   4. REFINER AGENT                          │
│  • Applies reviewer feedback                                │
│  • Fixes identified issues                                  │
│  • Enhances clarity and engagement                         │
│  • Tracks all changes made                                 │
│  • Produces improved V2                                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ RefinedOutput (V2)
                            │
┌─────────────────────────────────────────────────────────────┐
│               Final Multi-Platform Content                  │
│         LinkedIn • Twitter • Newsletter (V2)                │
└─────────────────────────────────────────────────────────────┘
```

## 🎬 Example Pipeline Output

```
[Pipeline] Starting content repurposing pipeline...
[Pipeline] Input: 450 words

[Pipeline] Stage 1/4: Running Summarizer Agent...
  ✓ Title: "The Future of Remote Work: Trust Over Tools"
  ✓ Extracted 7 key points
  ✓ Content DNA: Trust-based management vs control-based
  ✓ Quality score: 8.5/10

[Pipeline] Stage 2/4: Running Formatter Agent...
  ✓ LinkedIn post created (1,245 chars)
  ✓ Twitter thread created (8 tweets)
  ✓ Newsletter created (4 sections)
  ✓ All content traced to key points

[Pipeline] Stage 3/4: Running Reviewer Agent...
  ✓ Overall alignment: 8/10
  ✓ Consistency score: 9/10
  ✓ Critical issues found: 2
  ✓ Improvement suggestions: 5

[Pipeline] Stage 4/4: Running Refiner Agent...
  ✓ Applied 5 improvements
  ✓ Addressed 4 critical issues
  ✓ V2 quality: 9/10

[Pipeline] ✅ Pipeline complete! Results saved to outputs/
```

## 🧪 Testing

```bash
# Run with sample content to test the pipeline
python main.py --sample

# Test with URL fetching
python main.py --url https://example.com/article --no-save

# Test specific platforms
python main.py --sample --platforms linkedin --show-comparison
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs and issues
- 💡 Suggest new features or improvements
- 📝 Improve documentation
- 🔧 Submit pull requests

### Development Setup

```bash
# Clone and set up
git clone https://github.com/yourusername/contentforge-ai.git
cd contentforge-ai/multi-agent-content

# Install dev dependencies
pip install -r requirements.txt

# Run with sample content
python main.py --sample
```

## 📝 Roadmap

- [ ] Support for more platforms (Instagram, Medium, Blog)
- [ ] Image generation for social media posts
- [ ] A/B testing suggestions for different variations
- [ ] Analytics integration for performance tracking
- [ ] Custom agent plugins
- [ ] Multi-language support
- [ ] Scheduled content publishing

## ⚠️ Known Limitations

- **API Costs**: Uses OpenAI API which incurs costs per request
- **Rate Limits**: Subject to OpenAI rate limits
- **Content Length**: Best for articles 300-2000 words
- **URL Fetching**: May not work with paywalled or JS-heavy sites
- **Quality Variance**: Output quality depends on input content quality

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Built with [OpenAI GPT-4o](https://openai.com/)
- UI powered by [Streamlit](https://streamlit.io/) and [React](https://react.dev/)
- API framework: [FastAPI](https://fastapi.tiangolo.com/)
- Type validation: [Pydantic](https://docs.pydantic.dev/)

## 📧 Contact & Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/contentforge-ai/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/contentforge-ai/discussions)
- 📧 **Email**: your.email@example.com

---

<p align="center">
  Made with ❤️ by developers who believe in transparent, traceable AI systems
</p>

<p align="center">
  <sub>⭐ Star this repo if you find it useful! ⭐</sub>
</p>
