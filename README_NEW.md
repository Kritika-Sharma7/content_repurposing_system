# ContentForge - Multi-Agent Content Repurposing System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o-green.svg" alt="OpenAI GPT-4o">
  <img src="https://img.shields.io/badge/Pydantic-v2-orange.svg" alt="Pydantic v2">
  <img src="https://img.shields.io/badge/FastAPI-Backend-teal.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-Frontend-cyan.svg" alt="React">
</p>

An intelligent multi-agent system that transforms long-form content into platform-optimized outputs for LinkedIn, Twitter/X, and newsletters. Built with explicit orchestration, type-safe data contracts, and iterative quality refinement.

## Overview

ContentForge uses a production-grade multi-agent architecture to address the core challenge of content repurposing: maintaining quality and consistency across platforms while adapting to platform-specific constraints. The system employs specialized agents with clearly defined responsibilities, structured data schemas, and measurable quality improvements through iterative feedback loops.

### Key Features

- **Multi-Agent Pipeline**: Specialized agents for summarization, formatting, review, and refinement
- **Platform Optimization**: Tailored outputs for LinkedIn posts, Twitter threads, and newsletters
- **Quality Assurance**: Iterative feedback loop ensures high-quality, consistent content
- **Type-Safe Architecture**: Pydantic schemas enforce data contracts between agents
- **Modern UI**: React-based interface with real-time processing feedback
- **Dual Mode Operation**: React UI or CLI for flexible workflows

## Architecture

The system implements a disciplined pipeline with clear separation of concerns:

```
Input Content → Summarizer → Formatter → [Reviewer ↔ Refiner] → Final Output
```

### Agent Roles

| Agent | Responsibility | Purpose |
|-------|---------------|---------|
| **Summarizer** | Extract core message and prioritized key points | Content analysis and semantic extraction |
| **Formatter** | Create platform-specific content (LinkedIn, Twitter, Newsletter) | Platform adaptation with constraint awareness |
| **Reviewer** | Evaluate content quality and identify gaps | Quality assurance and issue detection |
| **Refiner** | Apply targeted fixes based on reviewer feedback | Iterative improvement with change tracking |

### Design Principles

- **Explicit Orchestration**: Direct control over agent interactions without framework abstractions
- **Structured Data Passing**: All inter-agent communication uses typed Pydantic schemas
- **Iterative Refinement**: Mandatory feedback loop between Reviewer and Refiner agents
- **Version Tracking**: Clear V1 → V2 → V3 progression with detailed change logs
- **Single Responsibility**: Each agent has one well-defined job

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 16+ (for React UI)
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multi-agent-content
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Install frontend dependencies (optional)**
   ```bash
   cd react-ui
   npm install
   cd ..
   ```

### Running the System

#### Option 1: React UI (Recommended)

Start both backend and frontend:
```bash
# Windows
start-all.bat

# Or manually:
# Terminal 1 - Backend
python api_server.py

# Terminal 2 - Frontend
cd react-ui
npm start
```

Access the UI at `http://localhost:3000`

#### Option 2: Command Line

```bash
python main.py
```

Follow the interactive prompts to:
1. Enter your content (paste or type, end with `END`)
2. Choose processing mode (full pipeline or mock mode)
3. Review generated outputs

#### Option 3: Programmatic API

```python
from pipeline.orchestrator import run_content_pipeline
from schemas.data_schemas import ContentInput

input_data = ContentInput(
    raw_text="Your long-form content here...",
    content_type="article"
)

result = run_content_pipeline(input_data)

# Access outputs
print(result.linkedin_post)
print(result.twitter_thread)
print(result.newsletter)
```

## Project Structure

```
multi-agent-content/
├── agents/              # Agent implementations
│   ├── summarizer.py    # Content analysis agent
│   ├── formatter.py     # Platform-specific formatting
│   ├── reviewer.py      # Quality evaluation agent
│   └── refiner.py       # Iterative improvement agent
├── schemas/             # Pydantic data schemas
│   └── data_schemas.py  # Type definitions
├── pipeline/            # Orchestration logic
│   └── orchestrator.py  # Pipeline coordinator
├── react-ui/            # React frontend
├── config/              # Configuration files
├── api_server.py        # FastAPI backend server
├── main.py              # CLI entry point
└── requirements.txt     # Python dependencies
```

## Platform-Specific Outputs

### LinkedIn Post
- Professional tone, 1,000-1,500 characters
- Hook-first structure with clear value proposition
- Hashtag optimization (3-5 relevant tags)

### Twitter Thread
- 5-8 connected tweets, each under 280 characters
- Engagement-focused hooks and CTAs
- Strategic emoji and hashtag usage

### Newsletter Section
- Detailed, scannable format with clear structure
- Comprehensive coverage of key points
- Professional tone suitable for email distribution

## Testing

Run the test suite to verify system functionality:

```bash
# Full system test
python test_system.py

# Pipeline test
python test_pipeline.py

# Individual component tests
python test_imports.py
python test_env.py
```

## Configuration

Edit `config/settings.py` to customize:

- **Model Selection**: Choose between GPT-4o, GPT-4, or other models
- **Temperature Settings**: Adjust creativity vs. consistency
- **Iteration Limits**: Configure max review-refine cycles
- **Platform Constraints**: Modify character limits and formatting rules

## Output Files

Generated content is saved to the `output/` directory:

- `summary.json` - Extracted core message and key points
- `formatted_v1.json` - Initial platform-specific content
- `review_*.json` - Quality evaluation results
- `refined_v*.json` - Iteratively improved content
- `final_output.txt` - Formatted final content for all platforms

## Known Limitations

- Requires OpenAI API access (no offline mode)
- Processing time varies (typically 30-60 seconds per input)
- Twitter thread length constrained to 5-8 tweets for optimal engagement
- Non-English content may require prompt adjustments

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes with clear messages
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact & Support

For questions, issues, or feedback:
- Open an issue on GitHub
- Review existing documentation in the `/docs` folder
- Check the [CHANGELOG.md](CHANGELOG.md) for recent updates

---

**Built with** ❤️ **using OpenAI GPT-4o, Python, FastAPI, and React**
