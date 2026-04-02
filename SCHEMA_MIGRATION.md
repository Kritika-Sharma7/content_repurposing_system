# Schema Simplification - v3.0.0 Migration Guide

## Overview

Version 3.0.0 introduces a **simplified output schema** for the SummarizerAgent. The goal is to produce clean, minimal, structured JSON output that's easy for downstream agents (Formatter, Reviewer, Refiner) to consume.

## What Changed?

### ✅ Fields Removed from Final Output

The following fields are **no longer included** in the JSON output when `model_dump()` is called:

- `relationships` - Was never present, confirmed removed
- `extraction_traces` - Was never present, confirmed removed
- `extraction_attempts` - Was never present, confirmed removed
- `importance_reason` - Was never present, confirmed removed

### ✅ Internal Fields (Excluded from Output)

These fields still exist in the Python object for backward compatibility but are **excluded from JSON serialization**:

- `core_message` - Internal field, excluded via `exclude=True`
- `main_theme` - Internal field, excluded via `exclude=True`
- `word_count_original` - Internal field, excluded via `exclude=True`
- `key_insights` - Legacy field, excluded via `exclude=True`

**Why?** These fields are still used internally by the UI, other agents, and pipeline logic, so removing them completely would break existing code. By marking them with `exclude=True`, they remain accessible in Python but don't clutter the JSON output.

### ✅ Simplified content_dna

**Before v3.0.0** (heavy structure):
```python
{
  "content_dna": {
    "core_conflict": "...",
    "key_question": "...",
    "argument_type": "...",      # REMOVED
    "evidence_types": [...],     # REMOVED
    "narrative_flow": "..."      # REMOVED
  }
}
```

**After v3.0.0** (clean structure):
```python
{
  "content_dna": {
    "core_conflict": "efficiency vs quality",
    "key_question": "How to balance speed and accuracy?"
  }
}
```

### ✅ Clean key_points Structure

Each `key_point` now has **exactly 6 fields**, no more:

```python
{
  "id": "kp_1",
  "concept": "automation",              # 2-5 word topic
  "claim": "reduces manual errors",     # Clear assertion
  "implication": "more focus time",     # Why it matters
  "importance": "critical",             # critical | high | medium
  "type": "insight"                     # insight | data_point | strategy | observation
}
```

### ✅ Simple summary_quality

**Before v3.0.0**:
```python
{
  "summary_quality": {
    "score": 8.5,
    "reason": "Good coverage",
    "confidence": "high",           # REMOVED
    "confidence_reason": "...",     # REMOVED
    "duplicate_score_field": 8.5   # REMOVED
  }
}
```

**After v3.0.0**:
```python
{
  "summary_quality": {
    "score": 8.5,
    "reason": "Good coverage with structured insights"
  }
}
```

## Final Output Structure

The complete `SummaryOutput` JSON now looks like this:

```json
{
  "title": "The Future of Remote Work",
  "one_liner": "Trust-based management beats control-based",
  "intent": "educational",
  "tone": "analytical",
  "structure": "problem-solution",
  "content_dna": {
    "core_conflict": "efficiency vs quality tradeoff",
    "key_question": "How can teams reduce meetings without losing alignment?"
  },
  "target_audience": "startup founders",
  "key_points": [
    {
      "id": "kp_1",
      "concept": "async-first communication",
      "claim": "reduces meetings by 60%",
      "implication": "enables more deep work time",
      "importance": "critical",
      "type": "insight"
    },
    {
      "id": "kp_2",
      "concept": "documentation culture",
      "claim": "every decision must be documented",
      "implication": "onboarding time drops from 3 months to 3 weeks",
      "importance": "high",
      "type": "strategy"
    }
  ],
  "summary_quality": {
    "score": 8.5,
    "reason": "Good coverage with structured insights"
  }
}
```

**Total fields**: 9 top-level fields (clean and focused)

## Backward Compatibility

### ✅ No Breaking Changes for Internal Code

- **UI Code**: Can still access `summary.main_theme`, `summary.word_count_original`, etc.
- **Agent Code**: Formatter and Reviewer can still read internal fields
- **Pipeline**: Orchestrator can still log internal fields

### ✅ JSON Output is Clean

When the result is serialized to JSON (API responses, file output), internal fields are automatically excluded:

```python
result = summarizer.run(content)

# Python access still works
print(result.main_theme)  # ✅ Works
print(result.word_count_original)  # ✅ Works

# JSON output is clean
json_output = result.model_dump()
print(json_output)  # ✅ Only contains 9 public fields
```

## Migration Steps

If you have existing code that relies on the output schema:

### 1. Check Your Code

Search for usages of removed fields:
```bash
grep -r "argument_type\|evidence_types\|narrative_flow" .
grep -r "relationships\|extraction_traces\|extraction_attempts" .
```

### 2. Update API Clients

If you're consuming the JSON API, update your client code to expect the new structure:

```python
# Before v3.0.0
summary = response.json()
theme = summary["main_theme"]  # ❌ No longer in JSON

# After v3.0.0
summary = response.json()
# Use content_dna instead
conflict = summary["content_dna"]["core_conflict"]  # ✅ Works
```

### 3. Internal Python Code

If you're working with the Python objects directly (e.g., in the UI or agents), **no changes needed**. Internal fields still work:

```python
# Still works in Python
summary.main_theme
summary.word_count_original
summary.key_insights
```

## Benefits

### 🎯 For Downstream Agents

- **Cleaner input**: Agents receive only relevant fields
- **Smaller payload**: Faster processing and lower costs
- **Better clarity**: Focus on semantic key points

### 🎯 For API Consumers

- **Smaller responses**: Less bandwidth usage
- **Clear contract**: Predictable schema
- **Easier parsing**: No confusing extra fields

### 🎯 For Developers

- **Maintainable**: Less clutter in JSON outputs
- **Type-safe**: Pydantic validation still enforced
- **Backward compatible**: Existing code doesn't break

## Testing

A comprehensive test suite validates the new structure:

```bash
python test_output_structure.py
```

Expected output:
```
✓ Expected fields: All 9 fields present
✓ No unexpected fields found
✓ content_dna structure: core_conflict, key_question
✓ key_points structure: id, concept, claim, implication, importance, type
✓ summary_quality structure: score, reason

🎉 SUCCESS: Output structure is clean and matches requirements!
```

## Support

If you encounter issues with the migration:

1. Check this guide first
2. Review the [CHANGELOG](CHANGELOG.md)
3. Open an issue on [GitHub](https://github.com/yourusername/contentforge-ai/issues)

---

**Version**: 3.0.0  
**Date**: 2026-04-02  
**Status**: ✅ Production Ready
