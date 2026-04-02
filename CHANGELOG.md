# Changelog

All notable changes to ContentForge AI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public release preparation
- Comprehensive README with usage examples
- Contributing guidelines
- MIT License

## [3.0.0] - 2026-04-02

### Changed
- **BREAKING**: Simplified SummaryOutput schema
  - Removed: `relationships`, `extraction_traces`, `extraction_attempts`, `importance_reason`
  - Simplified `content_dna` to only `core_conflict` and `key_question`
  - Removed heavy fields: `argument_type`, `evidence_types`, `narrative_flow`
  - Cleaned `key_points` structure to 6 essential fields only
  - Simplified `summary_quality` to only `score` and `reason`
- Internal fields now excluded from JSON output using Pydantic `exclude=True`
- Maintained backward compatibility for internal code that uses legacy fields

### Added
- Clean, minimal output structure for downstream agents
- Better traceability with `derived_from` fields in formatted content
- Enhanced documentation for schema structure

## [2.0.0] - 2026-03-15

### Added
- URL content fetching capability
- User preferences system (tone, audience, goal, platforms)
- Platform configuration with constraints
- React UI with modern design
- FastAPI backend server
- WebSocket support for real-time updates
- Content DNA extraction with semantic key points

### Changed
- Upgraded from basic insights to semantic key points
- Enhanced reviewer with multi-dimensional scoring
- Improved refiner with targeted issue addressing

## [1.0.0] - 2026-02-01

### Added
- Initial release
- 4-agent pipeline (Summarizer, Formatter, Reviewer, Refiner)
- Streamlit UI
- CLI interface
- Support for LinkedIn, Twitter, Newsletter formats
- Basic feedback loop for quality improvement
- JSON output files with timestamps
- Environment variable configuration

### Features
- Content summarization with key insight extraction
- Multi-format content generation
- Quality review and scoring
- Content refinement based on feedback
- Version tracking (V1 vs V2)

---

## Version Notes

### v3.0.0 - Schema Simplification
Focus on clean, minimal output structure while maintaining full backward compatibility for internal operations.

### v2.0.0 - Enhanced Intelligence
Introduced semantic key points, content DNA extraction, and user preference customization.

### v1.0.0 - Foundation
Established the core 4-agent pipeline with feedback-driven refinement.

---

[Unreleased]: https://github.com/yourusername/contentforge-ai/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/yourusername/contentforge-ai/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/yourusername/contentforge-ai/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/yourusername/contentforge-ai/releases/tag/v1.0.0
