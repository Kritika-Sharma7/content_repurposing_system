"""
Interactive demonstration of the multi-agent content system.
Run a full pipeline and save detailed results.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from pipeline.orchestrator import PipelineOrchestrator
from config.user_preferences import UserPreferences
from utils.llm import LLMClient

# Sample content
SAMPLE_CONTENT = """
The Future of Remote Work: Lessons from Five Years of Distributed Teams

After leading distributed engineering teams for five years, I've learned that remote work success isn't about tools or policies—it's about trust and intentional communication.

The biggest mistake companies make is trying to replicate office culture online. Forcing 9-to-5 schedules across time zones destroys productivity. Instead, focus on async-first communication where possible. We reduced meetings by 60% by switching to written proposals with comment-based discussions.

Key insight: Documentation becomes your office. When we mandated that every decision must be documented, onboarding time dropped from 3 months to 3 weeks. New hires could trace the "why" behind every system.

However, some synchronous time is crucial. We found that 2 hours of overlapping time daily was the sweet spot—enough for real-time collaboration without forcing anyone into awkward hours.

The productivity data surprised us: Our remote team shipped 40% more features than our previous co-located team. The secret? Fewer interruptions and more deep work time. We tracked focus blocks and found remote workers averaged 4.2 hours of uninterrupted work daily, versus 2.1 hours in office.

One counterintuitive finding: Random social interactions matter more than we thought. We created "virtual water cooler" channels and short, optional daily standups focused on personal updates. Team cohesion scores improved 25% after implementing these.

The tools that made the biggest difference weren't fancy collaboration platforms—they were simple shared documents, async video messages (Loom became essential), and a well-organized knowledge base.

For managers transitioning to remote: Stop measuring hours worked. Start measuring outcomes. Trust your team until they give you a reason not to. And over-communicate context—people need to understand the "why" more than ever when they can't absorb it through office osmosis.

The future isn't fully remote or fully in-office. It's about giving people autonomy to do their best work, wherever that happens to be.
"""

def print_divider(char="=", width=80):
    print(char * width)

def print_section(title):
    print(f"\n\n{'=' * 80}")
    print(f"  {title}")
    print("=" * 80)

def print_subsection(title):
    print(f"\n{'-' * 80}")
    print(f"  {title}")
    print("-" * 80)

def display_key_points(summary):
    """Display extracted key points."""
    print_subsection("Extracted Key Points")
    print(f"\nCore Message: {summary.core_message}\n")
    
    for i, kp in enumerate(summary.key_points, 1):
        print(f"{i}. [{kp.priority.upper()}] {kp.id}")
        print(f"   {kp.label}")
        if kp.data:
            print(f"   Data: {kp.data}")
        print()

def display_formatted_content(formatted):
    """Display V1 formatted content."""
    print_subsection("V1 Formatted Content")
    
    # LinkedIn
    print("\n[LINKEDIN POST]")
    print(f"Used KPs: {', '.join(formatted.linkedin.used_kps)}")
    print(f"Word count: {len(formatted.linkedin.content.split())} words")
    print("\n" + formatted.linkedin.content)
    
    # Twitter
    print("\n\n[TWITTER THREAD]")
    print(f"Used KPs: {', '.join(formatted.twitter.used_kps)}")
    print(f"Tweet count: {len(formatted.twitter.tweets)} tweets\n")
    for i, tweet in enumerate(formatted.twitter.tweets, 1):
        print(f"{i}. [{len(tweet)} chars] {tweet}")
    
    # Newsletter
    print("\n\n[NEWSLETTER]")
    print(f"Used KPs: {', '.join(formatted.newsletter.used_kps)}")
    print(f"Word count: {len(formatted.newsletter.content.split())} words")
    print("\n" + formatted.newsletter.content)

def display_review(review):
    """Display review issues."""
    print_subsection("Review Results")
    
    print(f"\nStatus: {review.status.upper()}")
    print(f"Total Issues: {review.summary.total_issues}")
    print(f"  - Critical: {review.summary.critical}")
    print(f"  - High: {review.summary.high}")
    print(f"  - Medium: {review.summary.medium}")
    
    if review.issues:
        print("\nIssues Found:")
        for i, issue in enumerate(review.issues, 1):
            print(f"\n{i}. [{issue.priority.upper()}] {issue.type.upper()}")
            print(f"   Problem: {issue.problem}")
            print(f"   Affects: {', '.join(issue.affects)}")
            print(f"   Suggestion: {issue.suggestion}")
            if issue.missing_kps:
                print(f"   Missing KPs: {', '.join(issue.missing_kps)}")

def display_refined(refined, version_label="V2"):
    """Display refined content with changes."""
    print_subsection(f"{version_label} Refined Content")
    
    print(f"\nVersion: {refined.version}")
    print(f"Changes Made: {len(refined.changes)}")
    
    if refined.changes:
        print("\nChanges:")
        for i, change in enumerate(refined.changes, 1):
            print(f"\n{i}. Issue {change.issue_id}: {change.action.upper()}")
            print(f"   Target: {change.target}")
            print(f"   Before: {change.before[:80]}...")
            print(f"   After: {change.after[:80]}...")
    
    # Show updated content
    print("\n\n[UPDATED LINKEDIN]")
    print(refined.linkedin.content[:300] + "...")
    
    print("\n\n[UPDATED TWITTER]")
    for i, tweet in enumerate(refined.twitter.tweets[:3], 1):
        print(f"{i}. {tweet[:100]}...")

def display_comparison(result):
    """Display V1 vs Final comparison."""
    print_subsection("V1 vs Final Version Comparison")
    
    # Count words
    v1_linkedin = len(result.v1.linkedin.content.split())
    final_linkedin = len(result.v2.linkedin.content.split()) if result.v2 else v1_linkedin
    
    v1_tweets = len(result.v1.twitter.tweets)
    final_tweets = len(result.v2.twitter.tweets) if result.v2 else v1_tweets
    
    print("\nContent Evolution:")
    print(f"  LinkedIn: {v1_linkedin} -> {final_linkedin} words")
    print(f"  Twitter: {v1_tweets} -> {final_tweets} tweets")
    print(f"  Total Issues Found: {result.total_issues}")
    print(f"  Issues Fixed: {result.issues_fixed}")
    print(f"  Refinement Iterations: {len(result.iterations)}")
    final_version = result.v2.version if result.v2 else 1
    print(f"  Final Version: V{final_version}")

def save_results(result, output_dir="demo_output"):
    """Save detailed results to files."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_file = output_path / f"pipeline_result_{timestamp}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)
    
    # Save readable text
    text_file = output_path / f"readable_output_{timestamp}.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write("MULTI-AGENT CONTENT REPURPOSING - PIPELINE RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Core Message: {result.summary.core_message}\n")
        f.write(f"Key Points: {len(result.summary.key_points)}\n")
        f.write(f"Total Issues: {result.total_issues}\n")
        f.write(f"Issues Fixed: {result.issues_fixed}\n")
        f.write(f"Iterations: {len(result.iterations)}\n\n")
        
        f.write("KEY POINTS\n")
        f.write("-" * 80 + "\n")
        for kp in result.summary.key_points:
            f.write(f"[{kp.priority.upper()}] {kp.id}: {kp.label}\n")
        
        f.write("\n\nFINAL LINKEDIN POST\n")
        f.write("-" * 80 + "\n")
        final_linkedin = result.v2.linkedin if result.v2 else result.v1.linkedin
        f.write(final_linkedin.content + "\n")
        
        f.write("\n\nFINAL TWITTER THREAD\n")
        f.write("-" * 80 + "\n")
        final_twitter = result.v2.twitter if result.v2 else result.v1.twitter
        for i, tweet in enumerate(final_twitter.tweets, 1):
            f.write(f"{i}. {tweet}\n")
        
        f.write("\n\nFINAL NEWSLETTER\n")
        f.write("-" * 80 + "\n")
        final_newsletter = result.v2.newsletter if result.v2 else result.v1.newsletter
        f.write(final_newsletter.content + "\n")
        
        if result.v2:
            f.write("\n\nCHANGES MADE\n")
            f.write("-" * 80 + "\n")
            for change in result.v2.changes:
                f.write(f"\nIssue {change.issue_id}: {change.action}\n")
                f.write(f"Target: {change.target}\n")
                f.write(f"Before: {change.before}\n")
                f.write(f"After: {change.after}\n")
    
    print(f"\n\nResults saved to:")
    print(f"  - {json_file}")
    print(f"  - {text_file}")

def main():
    """Run demonstration."""
    print_section("MULTI-AGENT CONTENT REPURPOSING SYSTEM - DEMONSTRATION")
    
    print("\nInitializing pipeline...")
    
    # Create LLM client
    llm = LLMClient(model="gpt-4o-mini", temperature=0.7)
    
    # Create orchestrator
    orchestrator = PipelineOrchestrator(
        llm_client=llm,
        verbose=True,
        max_iterations=2
    )
    
    # Set preferences
    prefs = UserPreferences(
        tone="conversational",
        audience="tech leaders and engineering managers",
        goal="engagement",
        platforms=["linkedin", "twitter", "newsletter"]
    )
    
    print("\nRunning pipeline with:")
    print(f"  - Tone: {prefs.tone}")
    print(f"  - Audience: {prefs.audience}")
    print(f"  - Goal: {prefs.goal}")
    print(f"  - Platforms: {', '.join(prefs.platforms)}")
    print(f"  - Max Iterations: 2")
    
    # Run pipeline
    print_divider()
    result = orchestrator.run(SAMPLE_CONTENT, prefs)
    print_divider()
    
    # Display results
    display_key_points(result.summary)
    display_formatted_content(result.v1)
    display_review(result.review_v1)  # Show review of V1
    
    if result.v2:
        display_refined(result.v2, "V2")
        display_review(result.review_v2)  # Show review of V2
    
    if len(result.iterations) > 1:
        print_subsection(f"V{result.v2.version if result.v2 else 1} (Final)")
        print(f"\nTotal Iterations: {len(result.iterations)}")
    
    display_comparison(result)
    
    # Save results
    save_results(result)
    
    print_section("DEMONSTRATION COMPLETE")
    print("\n[OK] All agents executed successfully")
    print("[OK] Feedback loop completed")
    print("[OK] Content refined based on review")
    print("[OK] Results saved to demo_output/")
    print("\nThe multi-agent system is working perfectly!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nError during demo: {e}")
        import traceback
        traceback.print_exc()
