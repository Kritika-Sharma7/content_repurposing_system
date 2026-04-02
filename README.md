# 🚀 ContentForge AI - Multi-Agent Content Repurposing System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o-green.svg" alt="OpenAI GPT-4o">
  <img src="https://img.shields.io/badge/Streamlit-UI-red.svg" alt="Streamlit UI">
  <img src="https://img.shields.io/badge/Pydantic-v2-orange.svg" alt="Pydantic v2">
  <img src="https://img.shields.io/badge/FastAPI-Backend-teal.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-Frontend-cyan.svg" alt="React">
</p>

> Transform long-form content into optimized, platform-specific formats using specialized AI agents with built-in feedback loops and intelligent quality refinement.

A production-quality multi-agent system that transforms long-form content (articles, blog posts, reports) into optimized formats for LinkedIn, Twitter/X, and Email newsletters using specialized AI agents with automated quality review and content refinement.

## ✨ Features

### 🎯 Core Capabilities
- **🤖 4 Specialized AI Agents** - Each with a distinct role in the content pipeline
- **🔄 Feedback Loop** - Automatic quality review and content refinement
- **📊 Version Tracking** - Clear before/after comparison (V1 → V2)
- **📤 Multi-Platform Export** - LinkedIn, Twitter/X threads, and Email newsletters
- **🎨 Modern UI** - Beautiful Streamlit & React interfaces with real-time progress
- **🔒 Secure** - API keys via environment variables, never hardcoded
- **📝 Structured Data** - All agents communicate via typed Pydantic schemas
- **🌐 URL Support** - Fetch content directly from web URLs
- **⚙️ Configurable** - User preferences for tone, audience, and platforms

### 🎨 What Makes It Different?
- **Explicit Orchestration** - No black-box frameworks (LangChain, CrewAI, etc.)
- **Content DNA Extraction** - Semantic key points with atomic, reusable units
- **Platform-Aware Formatting** - Respects character limits and platform constraints
- **Quality-Driven** - Mandatory review loop ensures high-quality outputs
- **Full Traceability** - Every output point traces back to source content

## 🎯 Output Formats

| Format | Description |
|--------|-------------|
| **LinkedIn Post** | Professional hook, body, CTA, hashtags |
| **Twitter Thread** | 5-8 tweets, each ≤280 chars, thread flow |
| **Newsletter** | Subject line, preview, intro, sections, closing |

## 🏗️ Architecture

```
Input -> Summarizer -> Formatter -> Reviewer -> Refiner -> Final Output
              |            |            |           |
         SummaryOutput  FormattedV1  ReviewOutput  RefinedV2
```

### Pipeline Flow

```
                    +------------------+
                    |   Raw Content    |
                    +--------+---------+
                             |
                             v
                    +--------+---------+
                    | SummarizerAgent  |
                    | - Extract insights|
                    | - Identify theme |
                    | - Find audience  |
                    +--------+---------+
                             |
                             v
                       SummaryOutput
                             |
                             v
                    +--------+---------+
                    | FormatterAgent   |
                    | - LinkedIn post  |
                    | - Twitter thread |
                    | - Newsletter     |
                    +--------+---------+
                             |
                             v
                      FormattedOutput (V1)
                             |
              +--------------+--------------+
              |                             |
              v                             v
    +---------+---------+         +---------+---------+
    |  ReviewerAgent    |         |                   |
    | - Score clarity   |         |                   |
    | - Find issues     |         |                   |
    | - Suggest fixes   |         |                   |
    +---------+---------+         |                   |
              |                   |                   |
              v                   |                   |
         ReviewOutput             |                   |
              |                   |                   |
              +-------------------+                   |
                        |                            |
                        v                            |
              +---------+---------+                  |
              |  RefinerAgent     |<-----------------+
              | - Apply feedback  |    (uses V1)
              | - Fix issues      |
              | - Track changes   |
              +---------+---------+
                        |
                        v
                  RefinedOutput (V2)
```

### Agents

| Agent | Responsibility | Input | Output |
|-------|---------------|-------|--------|
| **SummarizerAgent** | Extract key insights, theme, audience | Raw text | `SummaryOutput` |
| **FormatterAgent** | Create LinkedIn, Twitter, Newsletter | `SummaryOutput` | `FormattedOutput` (V1) |
| **ReviewerAgent** | Evaluate, score, find issues | `SummaryOutput` + `FormattedOutput` | `ReviewOutput` |
| **RefinerAgent** | Apply feedback, improve content | `SummaryOutput` + `FormattedOutput` + `ReviewOutput` | `RefinedOutput` (V2) |

### Feedback Loop

The system implements a mandatory feedback loop:

```
Formatted V1 -> Reviewer -> Feedback -> Refiner -> Formatted V2
```

This ensures continuous improvement with clear versioning.

## 📁 Project Structure

```
multi-agent-content/
├── agents/                    # AI Agent implementations
│   ├── summarizer.py         # Extracts Content DNA & key points
│   ├── formatter.py          # Creates platform-specific content
│   ├── reviewer.py           # Evaluates quality & finds issues
│   └── refiner.py            # Applies feedback & improves content
├── schemas/
│   └── schemas.py            # Pydantic models for type safety
├── pipeline/
│   └── orchestrator.py       # Workflow coordination & execution
├── config/
│   ├── user_preferences.py   # User preference models
│   ├── platform_config.py    # Platform constraints & rules
│   └── settings.py           # System configuration
├── utils/
│   ├── llm.py                # OpenAI API wrapper
│   └── content_fetcher.py    # URL content extraction
├── ui/
│   └── app.py                # Streamlit web interface
├── react-ui/                 # Modern React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── api_server.py             # FastAPI backend server
├── main.py                   # CLI entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute to the project
- **[Changelog](CHANGELOG.md)** - Version history and changes
- **[Schema Migration Guide](SCHEMA_MIGRATION.md)** - v3.0.0 schema changes

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 16+ (for React UI)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/contentforge-ai.git
cd contentforge-ai/multi-agent-content

# 2. Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. (Optional) Install React UI dependencies
cd react-ui
npm install
cd ..
```

### Environment Variables

Create a `.env` file in the `multi-agent-content` directory:

```env
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.7
```

## 🚀 Usage

### Option 1: Streamlit UI (Recommended)

```bash
cd multi-agent-content
streamlit run ui/app.py
```

Open http://localhost:8501 in your browser.

**Features:**
- 📝 Text input area with sample content
- 🔑 API key input (stored securely in session)
- 📊 Live pipeline execution with progress tracking
- 🎯 User preferences (tone, audience, platforms)
- 📈 Structured display of all outputs
- 🔄 V1 vs V2 comparison view
- ⭐ Review scores and detailed feedback
- 💾 Export to JSON

### Option 2: React UI (Modern Experience)

```bash
# Terminal 1: Start backend API
cd multi-agent-content
python api_server.py

# Terminal 2: Start React frontend
cd react-ui
npm run dev
```

Open http://localhost:5173 in your browser.

**Features:**
- 🎨 Modern, responsive design
- ⚡ Real-time WebSocket updates
- 🎯 Advanced configuration options
- 📊 Interactive output viewer
- 🌐 URL content fetching

### Option 3: Command Line Interface

```bash
# Run with sample content
python main.py --sample

# Run with file input
python main.py --file article.txt

# Run with URL input
python main.py --url https://example.com/article

# Run with direct text
python main.py --input "Your article text here..."

# With preferences
python main.py --file article.txt \
  --tone conversational \
  --audience "startup founders" \
  --platforms linkedin twitter

# Show V1 vs V2 comparison
python main.py --sample --show-comparison
```

### CLI Options

| Option | Description | Example |
|--------|-------------|---------|
| `--input`, `-i` | Direct text input | `--input "Your text..."` |
| `--file`, `-f` | Path to input text file | `--file article.txt` |
| `--url`, `-u` | Fetch content from URL | `--url https://example.com/blog` |
| `--sample`, `-s` | Use built-in sample content | `--sample` |
| `--output`, `-o` | Output directory | `--output ./results` |
| `--model`, `-m` | OpenAI model | `--model gpt-4o` |
| `--temperature`, `-t` | LLM temperature (0.0-1.0) | `--temperature 0.7` |
| `--tone` | Content tone | `--tone conversational` |
| `--audience` | Target audience | `--audience "developers"` |
| `--goal` | Content goal | `--goal "educational"` |
| `--platforms` | Target platforms | `--platforms linkedin twitter` |
| `--quiet`, `-q` | Suppress progress messages | `--quiet` |
| `--no-save` | Don't save results to files | `--no-save` |
| `--show-comparison` | Show V1 vs V2 comparison | `--show-comparison` |

### Programmatic Usage

```python
from pipeline.orchestrator import PipelineOrchestrator
from utils.llm import LLMClient

# Initialize
llm_client = LLMClient(api_key="your-key", model="gpt-4o")
orchestrator = PipelineOrchestrator(llm_client=llm_client)

# Run pipeline
content = "Your long-form article here..."
result = orchestrator.run(content)

# Access structured outputs
print(result.input_summary.title)
print(result.version_1.linkedin.hook)
print(result.review.overall_alignment_score)
print(result.version_2.linkedin.hook)
print(result.version_2.changes_made)

# Save results
orchestrator.save_results(result, "outputs")
```

## 📊 Data Schemas

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
