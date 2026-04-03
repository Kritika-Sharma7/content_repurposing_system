# Clean Design v4 - Quick Reference

## 🎯 Agent Flow

```
INPUT → SUMMARIZER → FORMATTER → REVIEWER → REFINER → OUTPUT
        (extract)    (optimize)   (review)    (improve)
```

## 📦 Agent Outputs

### Summarizer
```json
{
  "core_message": "One sentence thesis",
  "key_points": [
    {"id": "kp_1", "label": "Short phrase", "priority": "critical", "type": "insight", "data": "40%"}
  ]
}
```

### Formatter
```json
{
  "linkedin": {"content": "...", "used_kps": ["kp_1", "kp_2"]},
  "twitter": {"tweets": ["...", "..."], "used_kps": ["kp_1", "kp_3"]},
  "newsletter": {"content": "...", "used_kps": ["kp_1", "kp_2", "kp_4"]}
}
```

### Reviewer
```json
{
  "issues": [
    {
      "issue_id": "issue_1",
      "target": "linkedin",
      "type": "structure",
      "problem": "Weak hook",
      "reason": "Doesn't create curiosity",
      "suggestion": "Use data-driven opening",
      "priority": "high"
    }
  ]
}
```

### Refiner
```json
{
  "version": 2,
  "changes": [
    {
      "issue_id": "issue_1",
      "action": "rewrite",
      "target": "linkedin_hook",
      "before": "Original...",
      "after": "Improved..."
    }
  ],
  "linkedin": {...},
  "twitter": {...},
  "newsletter": {...}
}
```

## 🚀 Usage

### CLI
```bash
# Sample content
python main.py --sample

# Custom input
python main.py --file article.txt
python main.py --url https://example.com/article

# With options
python main.py --sample --tone conversational --max-iterations 3
```

### API
```bash
# Start server
python api_server.py

# Make request
curl -X POST http://localhost:8000/api/pipeline-run \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "text",
    "content": "Your article...",
    "user_preferences": {
      "tone": "professional",
      "platforms": ["linkedin", "twitter"]
    }
  }'
```

### Python
```python
from pipeline.orchestrator import PipelineOrchestrator
from config.user_preferences import UserPreferences

# Setup
prefs = UserPreferences(
    tone="professional",
    audience="tech leaders",
    platforms=["linkedin", "twitter"]
)

orchestrator = PipelineOrchestrator(verbose=True, max_iterations=2)

# Run
result = orchestrator.run(content, prefs)

# Access outputs
print(result.summary.core_message)
print(result.v2.linkedin.content)
print(result.v2.changes)
```

## 📋 Platform Constraints

| Platform | Constraint | Rule |
|----------|-----------|------|
| LinkedIn | 60-120 words | Hook → Insights → CTA |
| Twitter | Max 7 tweets, ≤240 chars | 1 idea per tweet |
| Newsletter | 200-300 words | Use ## headings |

## 🔍 Review Check Types

1. **Coverage** - Are critical KPs used?
2. **Constraint** - Word/char limits violated?
3. **Structure** - Hook present? Sections clear?
4. **Clarity** - Repetition? Weak phrasing?

## ✨ Key Improvements Over Old Design

| Old | New |
|-----|-----|
| Generic scores (95%) | Specific issues |
| "Improve engagement" | "Use data-driven hook from kp_2" |
| Black-box changes | Visible before/after |
| Complex traceability | Simple KP ID tracking |
| Score thresholds | Critical issues check |

## 📁 Files Changed

- ✅ `schemas/schemas.py` - Minimal schemas
- ✅ `agents/summarizer.py` - Clean extraction
- ✅ `agents/formatter.py` - Platform rules
- ✅ `agents/reviewer.py` - Actionable feedback
- ✅ `agents/refiner.py` - Visible changes
- ✅ `pipeline/orchestrator.py` - Issue-driven iteration
- ✅ `main.py` - Updated CLI
- ✅ `api_server.py` - Updated API

## 🧪 Testing

```bash
# Quick test
python test_pipeline.py

# Should show:
# - Core message extracted
# - 5-7 key points
# - V1 outputs
# - Issues found
# - V2 with tracked changes
```

## 🎯 Design Principles

✅ **Minimal** - Only essential data  
✅ **Structured** - KP IDs throughout  
✅ **Actionable** - Specific suggestions  
✅ **Visible** - Before/after tracking  
✅ **Real** - Actual improvements, not cosmetic  

❌ No scores without context  
❌ No vague feedback  
❌ No black-box magic  
❌ No over-engineering  
