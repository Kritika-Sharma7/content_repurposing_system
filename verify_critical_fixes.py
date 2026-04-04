"""
Quick verification that all 5 critical fixes are working.
Run this after implementing the fixes.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from schemas.schemas import (
    KeyPoint, SummaryOutput, FormattedOutput, ReviewOutput, ReviewIssue,
    LinkedInOutput, TwitterOutput, NewsletterOutput, ReviewSummary
)

print("=" * 80)
print("CRITICAL FIXES VERIFICATION")
print("Testing all 5 implemented fixes")
print("=" * 80)

passed = 0
failed = 0

def test(name, test_func):
    """Run test and track results."""
    global passed, failed
    try:
        test_func()
        print(f"✅ PASS: {name}")
        passed += 1
    except Exception as e:
        print(f"❌ FAIL: {name}")
        print(f"   Error: {str(e)[:150]}")
        failed += 1

# ============================================================================
# FIX #1: Duplicate Key Point IDs
# ============================================================================
def test_fix_1_duplicate_kp_ids():
    """FIX #1: Duplicate KP IDs should be rejected."""
    try:
        summary = SummaryOutput(
            core_message="Test message",
            key_points=[
                KeyPoint(id="kp_1", label="Point A", priority="critical", type="insight"),
                KeyPoint(id="kp_1", label="Point B (DUPLICATE!)", priority="high", type="insight"),
                KeyPoint(id="kp_2", label="Point C", priority="medium", type="insight")
            ]
        )
        # If we reach here, validation failed
        raise AssertionError("Duplicate IDs were NOT rejected - FIX #1 FAILED!")
    except ValueError as e:
        # Good! Should be rejected
        if "duplicate" in str(e).lower() or "unique" in str(e).lower():
            pass  # Expected
        else:
            raise AssertionError(f"Wrong error message: {e}")

test("FIX #1: Duplicate Key Point IDs Rejected", test_fix_1_duplicate_kp_ids)

# ============================================================================
# FIX #2: Empty affects[] List
# ============================================================================
def test_fix_2_empty_affects():
    """FIX #2: ReviewIssue with empty affects[] should be rejected."""
    try:
        issue = ReviewIssue(
            issue_id="issue_1",
            type="coverage",
            priority="high",
            problem="Test problem",
            reason="Test reason",
            suggestion="Test suggestion",
            affects=[],  # EMPTY - should be rejected!
            missing_kps=["kp_1"]
        )
        # If we reach here, validation failed
        raise AssertionError("Empty affects[] was NOT rejected - FIX #2 FAILED!")
    except ValueError as e:
        # Good! Should be rejected
        if "min_length" in str(e).lower() or "at least" in str(e).lower():
            pass  # Expected
        else:
            raise AssertionError(f"Wrong error message: {e}")

test("FIX #2: Empty affects[] List Rejected", test_fix_2_empty_affects)

# ============================================================================
# FIX #3: Stuck Loop Detection Method Exists
# ============================================================================
def test_fix_3_stuck_loop_detection():
    """FIX #3: Orchestrator should have stuck loop detection method."""
    from pipeline.orchestrator import PipelineOrchestrator
    from utils.llm import LLMClient
    
    orchestrator = PipelineOrchestrator(
        llm_client=LLMClient(model="gpt-4o-mini"),
        verbose=False
    )
    
    # Check method exists
    if not hasattr(orchestrator, '_detect_stuck_loop'):
        raise AssertionError("_detect_stuck_loop method NOT found - FIX #3 FAILED!")
    
    # Test the method with mock data
    review1 = ReviewOutput(
        issues=[
            ReviewIssue(
                issue_id="issue_1",
                type="coverage",
                priority="high",
                problem="Problem A",
                reason="Reason A",
                suggestion="Fix A",
                affects=["linkedin"],
                missing_kps=["kp_1"]
            )
        ],
        status="needs_fixes"
    )
    
    review2 = ReviewOutput(
        issues=[
            ReviewIssue(
                issue_id="issue_1",  # SAME ISSUE!
                type="coverage",
                priority="high",
                problem="Problem A",
                reason="Reason A",
                suggestion="Fix A",
                affects=["linkedin"],
                missing_kps=["kp_1"]
            )
        ],
        status="needs_fixes"
    )
    
    review3 = ReviewOutput(
        issues=[
            ReviewIssue(
                issue_id="issue_1",  # SAME ISSUE AGAIN!
                type="coverage",
                priority="high",
                problem="Problem A",
                reason="Reason A",
                suggestion="Fix A",
                affects=["linkedin"],
                missing_kps=["kp_1"]
            )
        ],
        status="needs_fixes"
    )
    
    # Should detect stuck loop
    is_stuck, stuck_issues = orchestrator._detect_stuck_loop([review1, review2, review3])
    
    if not is_stuck:
        raise AssertionError("Stuck loop NOT detected - FIX #3 FAILED!")
    
    if "issue_1" not in stuck_issues:
        raise AssertionError("Stuck issue ID not identified - FIX #3 FAILED!")

test("FIX #3: Stuck Loop Detection Works", test_fix_3_stuck_loop_detection)

# ============================================================================
# FIX #4: PipelineResult has metadata field
# ============================================================================
def test_fix_4_metadata_tracking():
    """FIX #4: PipelineResult should have metadata field for tracking."""
    from schemas.schemas import PipelineResult
    
    # Check if PipelineResult has metadata field
    fields = PipelineResult.model_fields
    if 'metadata' not in fields:
        raise AssertionError("metadata field NOT found in PipelineResult - FIX #4 FAILED!")
    
    # Create a result with metadata
    summary = SummaryOutput(
        core_message="Test",
        key_points=[
            KeyPoint(id=f"kp_{i}", label=f"Point {i}", priority="high", type="insight")
            for i in range(3)
        ]
    )
    
    formatted = FormattedOutput(
        version=1,
        linkedin=LinkedInOutput(content="Test", used_kps=["kp_0"]),
        twitter=TwitterOutput(tweets=["Test"], used_kps=["kp_1"]),
        newsletter=NewsletterOutput(content="Test", used_kps=["kp_2"])
    )
    
    review = ReviewOutput(issues=[], status="ok")
    
    result = PipelineResult(
        summary=summary,
        v1=formatted,
        review_v1=review,
        metadata={
            'termination_reason': 'stuck_loop',
            'stuck_issues': ['issue_1', 'issue_2']
        }
    )
    
    if 'termination_reason' not in result.metadata:
        raise AssertionError("metadata not storing values - FIX #4 FAILED!")

test("FIX #4: Metadata Field in PipelineResult", test_fix_4_metadata_tracking)

# ============================================================================
# FIX #5: Empty String Validation
# ============================================================================
def test_fix_5_empty_strings():
    """FIX #5: Empty or whitespace-only strings should be rejected."""
    
    # Test 5a: Empty core_message
    try:
        summary = SummaryOutput(
            core_message="",  # EMPTY!
            key_points=[
                KeyPoint(id=f"kp_{i}", label=f"Point {i}", priority="high", type="insight")
                for i in range(3)
            ]
        )
        raise AssertionError("Empty core_message NOT rejected - FIX #5a FAILED!")
    except ValueError as e:
        if "empty" in str(e).lower() or "whitespace" in str(e).lower():
            pass
        else:
            raise AssertionError(f"Wrong error for empty core_message: {e}")
    
    # Test 5b: Whitespace-only core_message
    try:
        summary = SummaryOutput(
            core_message="   ",  # WHITESPACE ONLY!
            key_points=[
                KeyPoint(id=f"kp_{i}", label=f"Point {i}", priority="high", type="insight")
                for i in range(3)
            ]
        )
        raise AssertionError("Whitespace core_message NOT rejected - FIX #5b FAILED!")
    except ValueError as e:
        if "empty" in str(e).lower() or "whitespace" in str(e).lower():
            pass
        else:
            raise AssertionError(f"Wrong error for whitespace core_message: {e}")
    
    # Test 5c: Empty LinkedIn content
    try:
        linkedin = LinkedInOutput(
            content="",  # EMPTY!
            used_kps=["kp_1"]
        )
        raise AssertionError("Empty LinkedIn content NOT rejected - FIX #5c FAILED!")
    except ValueError as e:
        if "empty" in str(e).lower() or "whitespace" in str(e).lower():
            pass
        else:
            raise AssertionError(f"Wrong error for empty LinkedIn: {e}")
    
    # Test 5d: Empty Newsletter content
    try:
        newsletter = NewsletterOutput(
            content="   ",  # WHITESPACE!
            used_kps=["kp_1"]
        )
        raise AssertionError("Whitespace Newsletter content NOT rejected - FIX #5d FAILED!")
    except ValueError as e:
        if "empty" in str(e).lower() or "whitespace" in str(e).lower():
            pass
        else:
            raise AssertionError(f"Wrong error for whitespace Newsletter: {e}")

test("FIX #5: Empty/Whitespace Strings Rejected", test_fix_5_empty_strings)

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)
print(f"Total Tests: {passed + failed}")
print(f"Passed: {passed} ✅")
print(f"Failed: {failed} ❌")

if failed == 0:
    print("\n🎉 SUCCESS! All 5 critical fixes are working correctly!")
    print("\n✅ FIX #1: Duplicate KP IDs are rejected")
    print("✅ FIX #2: Empty affects[] is rejected")
    print("✅ FIX #3: Stuck loop detection is implemented")
    print("✅ FIX #4: Metadata tracking is available")
    print("✅ FIX #5: Empty/whitespace strings are rejected")
    print("\n🚀 System is production-ready!")
    sys.exit(0)
else:
    print(f"\n⚠️ WARNING: {failed} fix(es) not working correctly.")
    print("Please review the errors above and fix the issues.")
    sys.exit(1)
