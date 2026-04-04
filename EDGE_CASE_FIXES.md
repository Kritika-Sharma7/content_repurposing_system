# Edge Case Quick Reference Guide

## 🚨 Critical Issues to Fix Immediately

### 1. Add Unique KP ID Validation
**File:** `schemas/schemas.py` - `SummaryOutput` class

```python
from pydantic import model_validator

class SummaryOutput(BaseModel):
    core_message: str
    key_points: List[KeyPoint]
    
    @model_validator(mode='after')
    def validate_unique_kp_ids(self):
        """Ensure all key point IDs are unique."""
        ids = [kp.id for kp in self.key_points]
        if len(ids) != len(set(ids)):
            duplicates = [id for id in ids if ids.count(id) > 1]
            raise ValueError(f"Duplicate key point IDs found: {set(duplicates)}")
        return self
```

---

### 2. Require Non-Empty affects in ReviewIssue
**File:** `schemas/schemas.py` - `ReviewIssue` class

```python
from pydantic import Field

class ReviewIssue(BaseModel):
    issue_id: str
    type: str
    priority: str
    problem: str
    reason: str
    suggestion: str
    affects: List[str] = Field(..., min_length=1, description="Must specify at least one affected platform")
    missing_kps: List[str] = Field(default_factory=list)
```

---

### 3. Add Stuck Loop Detection
**File:** `pipeline/orchestrator.py` - Add new method

```python
def _detect_stuck_loop(self, review_history: List[ReviewOutput]) -> tuple[bool, set]:
    """
    Detect if same issues keep appearing across iterations.
    
    Returns:
        (is_stuck, repeated_issue_ids): True if stuck, with set of issue IDs that repeat
    """
    if len(review_history) < 3:
        return False, set()
    
    # Get issue IDs from last 3 reviews
    recent_issues = [
        set([issue.issue_id for issue in review.issues])
        for review in review_history[-3:]
    ]
    
    # Find issues that appear in all 3
    repeated = recent_issues[0] & recent_issues[1] & recent_issues[2]
    
    if len(repeated) > 0:
        return True, repeated
    
    return False, set()
```

**Usage in run() method:**

```python
# In the feedback loop, after review
is_stuck, repeated_issues = self._detect_stuck_loop(review_history)
if is_stuck:
    if self.verbose:
        print(f"⚠️ Stuck loop detected: issues {repeated_issues} repeating")
    result.metadata['termination_reason'] = 'stuck_loop'
    result.metadata['stuck_issues'] = list(repeated_issues)
    break
```

---

### 4. Track Unfixable Issues
**File:** `pipeline/orchestrator.py` - In feedback loop

```python
# After refiner runs
if len(review.issues) > 0 and len(refined.changes) == 0:
    # Refiner couldn't fix the issues
    if self.verbose:
        print(f"⚠️ Refiner unable to fix {len(review.issues)} issues")
    
    result.metadata['unfixable_issues'] = [issue.dict() for issue in review.issues]
    result.metadata['termination_reason'] = 'refiner_unable_to_fix'
    break
```

---

### 5. Add Non-Empty String Validation
**File:** `schemas/schemas.py` - Multiple classes

```python
from pydantic import Field, field_validator

class SummaryOutput(BaseModel):
    core_message: str = Field(..., min_length=1, description="Must not be empty")
    key_points: List[KeyPoint]
    
    @field_validator('core_message')
    @classmethod
    def validate_not_whitespace(cls, v: str) -> str:
        """Ensure core_message is not just whitespace."""
        if not v or not v.strip():
            raise ValueError("core_message cannot be empty or whitespace")
        return v.strip()

class LinkedInOutput(BaseModel):
    content: str = Field(..., min_length=1)
    used_kps: List[str]
    
    @field_validator('content')
    @classmethod
    def validate_not_whitespace(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("content cannot be empty")
        return v.strip()

# Repeat for TwitterOutput, NewsletterOutput
```

---

## ⚠️ Medium Priority Improvements

### 6. Add Retry Logic for API Calls
**File:** `utils/llm.py` - `LLMClient` class

```python
import time
from openai import OpenAI, RateLimitError, APIError, APIConnectionError

class LLMClient:
    def call_with_retry(self, messages, max_retries=3):
        """
        Call LLM with exponential backoff retry logic.
        
        Handles: rate limits, network errors, temporary API issues
        """
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    response_format={"type": "json_object"}
                )
                return response
                
            except (RateLimitError, APIConnectionError, APIError) as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 1s, 2s, 4s
                    print(f"⚠️ API error, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"❌ API error after {max_retries} attempts: {e}")
                    raise
```

---

### 7. Improve Content Unchanged Detection
**File:** `pipeline/orchestrator.py`

```python
def _content_unchanged(self, old, new) -> bool:
    """
    Detect if content is meaningfully unchanged.
    Normalizes whitespace and case for comparison.
    """
    def normalize(text: str) -> str:
        """Remove whitespace, punctuation, lowercase for comparison."""
        import re
        # Keep alphanumeric only
        normalized = re.sub(r'[^a-zA-Z0-9]', '', text.lower())
        return normalized
    
    linkedin_same = (
        normalize(old.linkedin.content) == normalize(new.linkedin.content)
    )
    
    twitter_same = (
        normalize(" ".join(old.twitter.tweets)) == 
        normalize(" ".join(new.twitter.tweets))
    )
    
    newsletter_same = (
        normalize(old.newsletter.content) == normalize(new.newsletter.content)
    )
    
    return linkedin_same and twitter_same and newsletter_same
```

---

### 8. Add Token Limit Pre-Check
**File:** `agents/summarizer.py` or `pipeline/orchestrator.py`

```python
def _estimate_tokens(self, text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return len(text) // 4

def _check_token_limit(self, content: str, max_tokens: int = 100000) -> None:
    """
    Check if content is within reasonable token limits.
    Raises ValueError if too large.
    """
    estimated = self._estimate_tokens(content)
    if estimated > max_tokens:
        raise ValueError(
            f"Content too large: ~{estimated:,} tokens (max: {max_tokens:,}). "
            f"Consider chunking or summarizing first."
        )
```

**Usage:**

```python
def run(self, content: str, preferences: UserPreferences):
    # Before processing
    self._check_token_limit(content, max_tokens=100000)
    
    # Continue with normal processing
    ...
```

---

### 9. Cap Maximum Issues from Reviewer
**File:** `agents/reviewer.py`

```python
# In the run() method, after getting issues from LLM
if len(issues) > 5:
    # Too many issues overwhelms refiner
    # Keep top 5 by priority
    priority_order = {"critical": 0, "high": 1, "medium": 2}
    issues.sort(key=lambda x: priority_order.get(x.priority, 3))
    issues = issues[:5]
    
    if self.verbose:
        print(f"⚠️ Capped issues at 5 (originally {len(issues)})")
```

---

## 📊 Recommended Monitoring

### Add to PipelineResult metadata:

```python
result.metrics = {
    # Iteration tracking
    'total_iterations': len(iterations),
    'hit_max_iterations': len(iterations) >= self.max_iterations,
    
    # Issue tracking
    'total_issues_found': sum(len(r.issues) for r in review_history),
    'issues_fixed': sum(len(ref.changes) for ref in refinements),
    'unfixable_issues': len(result.metadata.get('unfixable_issues', [])),
    
    # Quality tracking
    'versions_created': current_version,
    'final_status': result.status,
    'termination_reason': result.metadata.get('termination_reason', 'completed'),
    
    # Performance tracking
    'total_time_seconds': end_time - start_time,
    'avg_time_per_iteration': (end_time - start_time) / len(iterations) if iterations else 0,
}
```

---

## 🧪 Testing Checklist

Run these commands to verify fixes:

```bash
# 1. Run existing edge case tests
python test_edge_cases.py

# 2. Run critical edge case tests
python test_critical_edge_cases.py

# 3. Run full system test
python test_system.py

# 4. Test with large input
python -c "
from agents.summarizer import SummarizerAgent
from config.user_preferences import UserPreferences
content = 'Test sentence. ' * 10000  # Large input
agent = SummarizerAgent()
result = agent.run(content, UserPreferences())
print(f'Success: {len(result.key_points)} KPs')
"

# 5. Test duplicate KP IDs (should fail)
python -c "
from schemas.schemas import SummaryOutput, KeyPoint
try:
    s = SummaryOutput(
        core_message='Test',
        key_points=[
            KeyPoint(id='kp_1', label='A', priority='high', type='insight'),
            KeyPoint(id='kp_1', label='B', priority='high', type='insight'),  # Duplicate
            KeyPoint(id='kp_2', label='C', priority='high', type='insight')
        ]
    )
    print('❌ FAIL: Duplicates allowed')
except ValueError as e:
    print(f'✅ PASS: {e}')
"
```

---

## 📋 Implementation Priority

### Phase 1: Critical (Do First) ⚠️
- [ ] Add unique KP ID validation
- [ ] Add non-empty affects validation
- [ ] Add non-empty string validation
- [ ] Add stuck loop detection
- [ ] Track unfixable issues

**Time:** ~2 hours  
**Impact:** Prevents critical bugs

---

### Phase 2: Important (Do Soon) ⏰
- [ ] Add retry logic for API calls
- [ ] Improve content unchanged detection
- [ ] Add token limit pre-check
- [ ] Cap maximum issues from reviewer

**Time:** ~2 hours  
**Impact:** Improves reliability

---

### Phase 3: Nice to Have (Do Eventually) ✨
- [ ] Add monitoring metrics
- [ ] Add quality regression detection
- [ ] Add load testing
- [ ] Add comprehensive logging

**Time:** ~3 hours  
**Impact:** Better observability

---

## 🔍 Quick Debug Commands

```bash
# Check if schema validations work
python -c "from schemas.schemas import *; print('✓ Schemas load')"

# Test orchestrator
python -c "from pipeline.orchestrator import *; print('✓ Orchestrator loads')"

# Check for stuck loop detection
python -c "from pipeline.orchestrator import PipelineOrchestrator; o = PipelineOrchestrator(); print('Has stuck detection:', hasattr(o, '_detect_stuck_loop'))"

# Verify LLM client
python -c "from utils.llm import LLMClient; c = LLMClient(); print('✓ LLM client ready')"
```

---

## 📞 When Things Go Wrong

### Symptom: Same issues appearing across V1, V2, V3
**Fix:** Implement stuck loop detection (#3 above)

### Symptom: Refiner makes no changes
**Fix:** Track unfixable issues (#4 above)

### Symptom: Invalid KP references causing errors
**Fix:** Add unique ID validation (#1 above)

### Symptom: API rate limit errors
**Fix:** Add retry logic (#6 above)

### Symptom: Very large input crashes
**Fix:** Add token limit pre-check (#8 above)

---

## 📚 Related Files

- `EDGE_CASE_ANALYSIS.md` - Full detailed analysis
- `test_critical_edge_cases.py` - Test suite for critical issues
- `test_edge_cases.py` - Original edge case tests
- `schemas/schemas.py` - Add validations here
- `pipeline/orchestrator.py` - Add loop logic here
- `utils/llm.py` - Add retry logic here

---

**Last Updated:** 2026-04-04  
**Status:** Recommendations ready for implementation
