# Edge Case Analysis - Multi-Agent Content System

## Date: 2026-04-04

---

## EXISTING EDGE CASES (from test_edge_cases.py)

### ✅ Already Tested (12 tests)

1. **Very Short Content** - Content < 20 words
2. **Very Long Content** - Content > 1000 words  
3. **Max Iterations Limit** - Ensures no infinite loops
4. **Empty Review** - No issues found
5. **Missing API Key** - Graceful degradation
6. **Invalid Platforms** - Empty platform list
7. **Too Few Key Points** - Schema validation (< 3)
8. **Too Many Key Points** - Schema validation (> 6)
9. **Tweet Length** - Auto-truncation at 280 chars
10. **Unicode Content** - Emojis and special characters
11. **Multiple Platform Formats** - Selective generation
12. **High-Quality Content** - Minimal reviewer issues

---

## ADDITIONAL EDGE CASES TO TEST

### 🔴 CRITICAL EDGE CASES

#### 1. **Infinite Review Loop**
**Risk:** Reviewer keeps finding issues, refiner keeps making changes, but nothing improves
- **Scenario:** V1→V2→V3→V4→V5 all have issues, content quality doesn't improve
- **Current Handling:** `max_iterations=5` limit
- **Missing:** Detection of "stuck" state where same issues repeat
- **Test:** Create content that triggers repetitive issues

**Recommendation:**
```python
# Add in orchestrator.py
def _detect_stuck_loop(self, issue_history):
    """Detect if same issues keep appearing."""
    if len(issue_history) >= 3:
        last_3_issues = [set(r.issue_ids) for r in issue_history[-3:]]
        if last_3_issues[0] == last_3_issues[1] == last_3_issues[2]:
            return True  # Same issues 3 times = stuck
    return False
```

#### 2. **Reviewer Finds Issues But Refiner Refuses to Fix**
**Risk:** Refiner returns "no changes" even when issues exist
- **Scenario:** LLM decides issues can't be fixed without losing quality
- **Current Handling:** Loop exits if `len(refined.changes) == 0`
- **Missing:** Logging/tracking of unfixable issues
- **Test:** Create content with contradictory quality requirements

**Recommendation:**
```python
# In orchestrator.py feedback loop
if len(review.issues) > 0 and len(refined.changes) == 0:
    result.unfixable_issues = review.issues
    result.termination_reason = "refiner_unable_to_fix"
    break
```

#### 3. **Content Completely Unchanged Detection False Positive**
**Risk:** `_content_unchanged()` might miss subtle changes
- **Scenario:** Refiner makes meaningful changes but comparison fails
- **Current Method:** String comparison of formatted content
- **Missing:** Semantic change detection
- **Test:** Check if punctuation-only changes trigger false positive

**Recommendation:**
```python
def _content_unchanged(self, old, new):
    """Compare with normalization."""
    def normalize(text):
        return "".join(text.lower().split())  # Remove whitespace/case
    
    return (normalize(old.linkedin.content) == normalize(new.linkedin.content) and
            normalize(" ".join(old.twitter.tweets)) == normalize(" ".join(new.twitter.tweets)) and
            normalize(old.newsletter.content) == normalize(new.newsletter.content))
```

#### 4. **Key Point ID Collision**
**Risk:** Multiple KPs get same ID (kp_1, kp_1)
- **Scenario:** Summarizer generates duplicate IDs
- **Current Handling:** None explicitly
- **Missing:** Unique ID validation
- **Test:** Force duplicate IDs in summary

**Recommendation:**
```python
# Add to SummaryOutput.model_validate
@model_validator(mode='after')
def validate_unique_kp_ids(self):
    ids = [kp.id for kp in self.key_points]
    if len(ids) != len(set(ids)):
        raise ValueError("Key point IDs must be unique")
    return self
```

#### 5. **Used KPs Tracking Mismatch**
**Risk:** Formatted output claims to use KPs that don't exist
- **Scenario:** `used_kps=["kp_99"]` but summary only has kp_1 to kp_5
- **Current Handling:** None
- **Missing:** Cross-validation of used_kps against summary
- **Test:** Create formatted output with invalid KP references

**Recommendation:**
```python
# Add to FormattedOutput.model_validate
@model_validator(mode='after')
def validate_used_kps_exist(self, info):
    """Ensure used_kps reference actual key points."""
    if 'summary' in info.context:
        valid_ids = {kp.id for kp in info.context['summary'].key_points}
        all_used = (set(self.linkedin.used_kps) | 
                   set(self.twitter.used_kps) | 
                   set(self.newsletter.used_kps))
        invalid = all_used - valid_ids
        if invalid:
            raise ValueError(f"Invalid KP references: {invalid}")
    return self
```

---

### 🟡 MEDIUM PRIORITY EDGE CASES

#### 6. **Review Issue with No Affected Platforms**
**Risk:** ReviewIssue has empty `affects=[]`
- **Scenario:** Reviewer identifies issue but doesn't specify where
- **Current Handling:** Refiner might ignore it
- **Test:** Check refiner behavior with `affects=[]`

**Recommendation:**
```python
# In ReviewIssue schema
affects: List[str] = Field(..., min_length=1)  # Must have at least one
```

#### 7. **Missing Critical Priority Key Points**
**Risk:** Summarizer produces 0 critical KPs (all medium/high)
- **Scenario:** Content has no standout insights
- **Current Handling:** Validation requires 2-3 critical, but enforcement?
- **Test:** Check if validation is actually triggered

**Check:** `SummaryOutput.validate_key_points()` line in code

#### 8. **Twitter Thread > 7 Tweets**
**Risk:** Formatter generates 10+ tweets
- **Scenario:** Complex content with many points
- **Current Handling:** `validate_tweets()` auto-truncates
- **Missing:** Warning to user about truncation
- **Test:** Verify truncation works correctly

#### 9. **Newsletter Auto-Fills All KPs**
**Risk:** `used_kps` always shows all KPs even if not mentioned
- **Scenario:** Line 542 in formatter.py: fallback to all KPs
- **Current Handling:** Automatic fallback
- **Missing:** True coverage detection
- **Test:** Create newsletter that only uses 2 of 5 KPs, check if tracked correctly

**Recommendation:**
```python
# More precise tracking in formatter
newsletter_kps = self._detect_mentioned_kps(newsletter_content, selected_kps)
if not newsletter_kps:
    newsletter_kps = [kp.id for kp in selected_kps]  # Fallback only if truly none detected
```

#### 10. **Refinement Makes Content Worse**
**Risk:** V2 quality < V1 quality after refinement
- **Scenario:** Overfitting to reviewer feedback
- **Current Handling:** None
- **Missing:** Quality regression detection
- **Test:** Compare V1 vs V2 with quality metrics

**Recommendation:**
```python
# Add quality score tracking
result.quality_scores = {
    'v1': self._calculate_quality_score(v1),
    'v2': self._calculate_quality_score(v2),
    ...
}
if result.quality_scores['v2'] < result.quality_scores['v1']:
    result.warnings.append("Quality regression detected in V2")
```

---

### 🟢 LOW PRIORITY EDGE CASES

#### 11. **Platform-Specific Character Limits**
- LinkedIn: No strict limit but 100-150 words target
- Twitter: 280 chars per tweet
- Newsletter: 120-200 words target

**Test:** Content that naturally exceeds limits

#### 12. **Non-English Content**
- Summarizer, Formatter, Reviewer all use English prompts
- **Test:** Spanish, Chinese, Arabic input

#### 13. **Markdown in Source Content**
- Input has `**bold**`, `_italic_`, `[links](url)`
- **Test:** Check if formatting is preserved or stripped

#### 14. **Code Snippets in Content**
- Input contains Python/JS code blocks
- **Test:** Check if code is treated as content or preserved

#### 15. **Numeric Data Edge Cases**
- Very large numbers: 1,234,567,890
- Percentages: 123.456%
- Currency: $1.23M
- **Test:** Check if preserved correctly

#### 16. **Empty Core Message**
- Summarizer returns `core_message=""`
- **Current:** Required field, but is it validated for non-empty?

#### 17. **Reviewer Returns > 10 Issues**
- Review finds 15+ problems
- **Risk:** Refiner overwhelmed
- **Recommendation:** Cap at 5 most critical

#### 18. **Concurrent API Calls**
- Running 2+ pipelines simultaneously
- **Risk:** Rate limiting
- **Test:** Load testing with 10 concurrent pipelines

#### 19. **Token Limit Exceeded**
- Input content > model token limit (e.g., 128k tokens)
- **Current:** Likely fails at LLM API call
- **Missing:** Pre-validation and chunking

#### 20. **Network Timeout During Refinement**
- API call fails mid-pipeline
- **Current:** Exception likely bubbles up
- **Missing:** Retry logic or graceful degradation

---

## SCHEMA VALIDATION GAPS

### Current Validations ✅
- `key_points`: 3-6 length
- `tweets`: ≤7 tweets, ≤280 chars each
- `version`: Increments properly

### Missing Validations ❌
- **Unique KP IDs** - No check for duplicates
- **Valid KP references** - used_kps can reference non-existent IDs
- **Non-empty strings** - core_message, content fields could be ""
- **Priority constraints** - No validation that 2-3 critical KPs exist
- **Issue affects non-empty** - ReviewIssue.affects could be []
- **Change tracking completeness** - refined.changes count vs review.issues count

---

## RECOMMENDED TEST SUITE

### Critical Tests to Add

```python
# Test: Stuck loop detection
def test_stuck_review_loop():
    """Test that system detects when same issues repeat."""
    # Create content that triggers same issues repeatedly
    # Verify loop exits before max_iterations
    pass

# Test: KP ID uniqueness
def test_duplicate_kp_ids():
    """Test that duplicate key point IDs are rejected."""
    try:
        summary = SummaryOutput(
            core_message="Test",
            key_points=[
                KeyPoint(id="kp_1", label="A", priority="high", type="insight"),
                KeyPoint(id="kp_1", label="B", priority="high", type="insight"),  # Duplicate!
                KeyPoint(id="kp_2", label="C", priority="high", type="insight")
            ]
        )
        assert False, "Should reject duplicate IDs"
    except ValueError:
        pass  # Expected

# Test: Invalid KP references
def test_invalid_kp_references():
    """Test that used_kps referencing non-existent KPs is caught."""
    summary = SummaryOutput(
        core_message="Test",
        key_points=[KeyPoint(id="kp_1", label="A", priority="high", type="insight")] * 3
    )
    try:
        formatted = FormattedOutput(
            version=1,
            linkedin=LinkedInOutput(content="Test", used_kps=["kp_999"]),  # Invalid!
            twitter=TwitterOutput(tweets=["Test"], used_kps=["kp_1"]),
            newsletter=NewsletterOutput(content="Test", used_kps=["kp_1"])
        )
        # If validation context is passed, this should fail
    except ValueError:
        pass

# Test: Refiner unable to fix issues
def test_refiner_refuses_changes():
    """Test when refiner returns zero changes despite issues."""
    # Create scenario where refiner can't improve without breaking constraints
    # Verify orchestrator handles gracefully
    pass

# Test: Content unchanged false positive
def test_content_unchanged_detection():
    """Test that minor changes (punctuation) are detected."""
    # Create V1 and V2 that differ only in punctuation
    # Verify _content_unchanged returns False
    pass

# Test: Large token count input
def test_token_limit_exceeded():
    """Test behavior with very large input (>100k tokens)."""
    huge_content = "word " * 50000
    # Should either handle gracefully or provide clear error
    pass

# Test: Network failure during refinement
def test_api_failure_mid_pipeline():
    """Test resilience to API failures."""
    # Mock API failure at refinement stage
    # Verify pipeline doesn't crash, returns partial result
    pass

# Test: Empty/whitespace-only content
def test_empty_content():
    """Test with empty or whitespace-only input."""
    for content in ["", "   ", "\n\n\n"]:
        # Should reject or handle gracefully
        pass

# Test: Missing critical priority KPs
def test_no_critical_keypoints():
    """Test summarizer output with 0 critical priority KPs."""
    summary = SummaryOutput(
        core_message="Test",
        key_points=[
            KeyPoint(id=f"kp_{i}", label=f"Point {i}", priority="medium", type="insight")
            for i in range(5)
        ]
    )
    # Should fail validation if 2-3 critical required
```

---

## MONITORING RECOMMENDATIONS

### Runtime Metrics to Track
1. **Loop iterations count** - Flag if hitting max_iterations frequently
2. **Issue repetition rate** - Same issue appearing in V1, V2, V3
3. **Refiner success rate** - % of issues actually fixed
4. **Quality regression count** - How often V2 < V1
5. **Average KPs used** - per platform
6. **API call duration** - Detect slow responses
7. **Token usage** - Per stage (summarizer, formatter, etc.)

### Error Categories
1. **Validation errors** - Schema violations
2. **API errors** - Network, rate limit, auth
3. **Logic errors** - Infinite loops, stuck states
4. **Data errors** - Invalid references, missing fields

---

## GRACEFUL DEGRADATION STRATEGIES

### When Issues Can't Be Fixed
```python
# Option 1: Return best version achieved
if iteration >= max_iterations:
    result.status = "partially_refined"
    result.best_version = current_output
    result.remaining_issues = unresolved_issues

# Option 2: Fall back to V1
if quality_regression_detected:
    result.final_version = v1
    result.warning = "Refinement degraded quality, using V1"

# Option 3: Partial refinement
if some_issues_fixed:
    result.status = "partially_improved"
    result.fixed_issues = fixed
    result.unfixed_issues = remaining
```

### When API Fails
```python
# Retry with exponential backoff
for attempt in range(3):
    try:
        return llm.call(...)
    except NetworkError:
        if attempt < 2:
            time.sleep(2 ** attempt)
        else:
            # Return best effort or cached result
            return fallback_response
```

---

## TESTING CHECKLIST

- [ ] Run existing 12 edge case tests
- [ ] Add 8 critical edge case tests
- [ ] Add schema validation tests (5)
- [ ] Add load/stress tests (concurrent, large input)
- [ ] Test with non-English content
- [ ] Test with malformed JSON responses from LLM
- [ ] Test error recovery and retry logic
- [ ] Test graceful degradation paths
- [ ] Document all edge case behaviors
- [ ] Add monitoring for production issues

---

## IMMEDIATE ACTION ITEMS

### 1. Add Validation (Critical)
```python
# In schemas/schemas.py

# SummaryOutput - unique KP IDs
@model_validator(mode='after')
def validate_unique_kp_ids(self):
    ids = [kp.id for kp in self.key_points]
    if len(ids) != len(set(ids)):
        raise ValueError("Key point IDs must be unique")
    return self

# ReviewIssue - affects not empty
affects: List[str] = Field(..., min_length=1, description="Platforms affected")
```

### 2. Improve Orchestrator (High Priority)
```python
# In pipeline/orchestrator.py

# Add stuck loop detection
def _detect_stuck_loop(self, review_history):
    if len(review_history) >= 3:
        recent_issues = [set([i.issue_id for i in r.issues]) for r in review_history[-3:]]
        overlap = recent_issues[0] & recent_issues[1] & recent_issues[2]
        if len(overlap) > 0:
            return True, overlap
    return False, set()

# Track unfixable issues
if len(review.issues) > 0 and len(refined.changes) == 0:
    result.metadata['unfixable_issues'] = [i.dict() for i in review.issues]
    result.metadata['termination_reason'] = "refiner_unable_to_fix"
    break
```

### 3. Add Error Handling (Medium Priority)
```python
# In utils/llm.py

def call_with_retry(self, messages, max_retries=3):
    """LLM call with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return self.client.chat.completions.create(...)
        except (NetworkError, Timeout, RateLimitError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
                time.sleep(wait_time)
            else:
                raise
```

### 4. Add Monitoring (Low Priority)
```python
# In pipeline/orchestrator.py

# Track quality metrics
result.metrics = {
    'total_iterations': len(iterations),
    'total_issues_found': sum(len(r.issues) for r in reviews),
    'total_changes_made': sum(len(ref.changes) for ref in refinements),
    'hit_max_iterations': len(iterations) >= self.max_iterations,
    'final_status': result.status
}
```

---

## CONCLUSION

**Status:** System handles most edge cases well via existing validations and loop constraints.

**Critical Gaps:**
1. No unique KP ID validation
2. No detection of stuck review loops
3. No handling of unfixable issues
4. Missing validation for used_kps references

**Recommendation:** Implement the 4 critical validations above before production deployment.

**Testing Priority:**
1. ✅ Run existing test_edge_cases.py (verify 12 tests pass)
2. 🔴 Add 8 critical edge case tests
3. 🟡 Add 5 schema validation tests
4. 🟢 Add stress/load tests as needed

**Timeline Estimate:**
- Critical fixes: 2-3 hours
- Additional tests: 3-4 hours
- Monitoring setup: 1-2 hours
- **Total: ~8 hours for comprehensive edge case handling**
