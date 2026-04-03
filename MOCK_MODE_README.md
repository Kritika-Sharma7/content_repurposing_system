# Mock Mode Guide

## 🚀 Quick Start

During UI development, use mock mode to avoid burning API credits:

```bash
# Windows
.\start-mock-mode.bat

# Or manually set environment variable
set USE_MOCK_DATA=true
python api_server.py
```

## 🎯 What Mock Mode Does

- **Skips OpenAI API calls** → No credit usage
- **Returns realistic data** → Perfect for UI testing  
- **Same response structure** → No frontend changes needed
- **Instant responses** → Fast development cycle

## 📊 Mock Data Structure

The mock data includes a complete pipeline result:

```
MOCK_PIPELINE_RESULT/
├── summary/          # Agent 1: Key points extracted
├── v1/              # Agent 2: Initial formatted content
├── review/          # Agent 3: Issues found  
├── v2/              # Agent 4: Refined content
├── changes/         # Detailed change tracking
└── metrics/         # Performance summary
```

## 🔧 System Improvements Made

### 1. Reviewer Agent (Fixed)
- ✅ Disciplined 3-area focus (coverage, consistency, clarity)
- ✅ Hard 4-issue limit to prevent overload
- ✅ Merged cross-platform issues  
- ✅ Strict coverage validation using `used_kps`

### 2. Refiner Agent (Fixed)  
- ✅ "Fix problems, not text" approach
- ✅ Surgical precision with natural integration
- ✅ Real text anchors instead of vague targeting
- ✅ Proper fix validation (not just cosmetic changes)

### 3. Feedback Loop (Improved)
- ✅ Handles both critical AND high priority issues
- ✅ Quality convergence detection (prevents infinite loops)
- ✅ Warning system instead of hard pipeline failures
- ✅ Transparent change tracking

## 🎨 Frontend Integration

No changes needed - mock mode returns identical structure to real API:

```javascript
// Same response whether mock or real
const result = await fetch('/api/pipeline-run', {
  method: 'POST', 
  body: JSON.stringify(payload)
});
```

## ⚙️ Switch Back to Real Mode

When ready for production:

```bash
# Remove or set to false
set USE_MOCK_DATA=false
python api_server.py
```

Or simply don't set the environment variable (defaults to real mode).

## 🧪 Test Installation  

Run validation script:

```bash
python test_system.py
```

This verifies:
- ✅ No syntax errors in updated agents
- ✅ Mock data structure compatibility
- ✅ Schema validation passes
- ✅ All imports working