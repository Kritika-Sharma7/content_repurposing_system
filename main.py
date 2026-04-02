#!/usr/bin/env python3
"""
Multi-Agent Content Repurposing Workflow

CLI entry point for running the content repurposing pipeline.
Takes long-form content and produces multiple output formats through
a multi-agent pipeline with feedback-driven refinement.

UPGRADE v2: Enhanced with URL input, user preferences, and platform selection.

Usage:
    python main.py --input "Your article text here"
    python main.py --file article.txt
    python main.py --url https://example.com/article
    python main.py --sample --platforms linkedin twitter
    python main.py --file article.txt --tone conversational --audience "startup founders"
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from pipeline.orchestrator import PipelineOrchestrator
from utils.llm import LLMClient
from utils.content_fetcher import resolve_input, ContentFetchError
from config.user_preferences import UserPreferences
from config.settings import SystemSettings, FeedbackLoopSettings, ScoringWeights


# Sample content for demonstration
SAMPLE_CONTENT = """
The Future of Remote Work: Lessons from Five Years of Distributed Teams

After leading distributed engineering teams for five years, I've learned that remote work success isn't about tools or policies—it's about trust and intentional communication.

The biggest mistake companies make is trying to replicate office culture online. Forcing 9-to-5 schedules across time zones destroys productivity. Instead, focus on async-first communication where possible. We reduced meetings by 60% by switching to written proposals with comment-based discussions.

Key insight: Documentation becomes your office. When we mandated that every decision must be documented, onboarding time dropped from 3 months to 3 weeks. New hires could trace the "why" behind every system.

However, some synchronous time is crucial. We found that 2 hours of overlapping time daily was the sweet spot—enough for real-time collaboration without forcing anyone into awkward hours.

The productivity data surprised us: Our remote team shipped 40% more features than our previous co-located team. The secret? Fewer interruptions and more deep work time. We tracked focus blocks and found remote workers averaged 4.2 hours of uninterrupted work daily, versus 2.1 hours in office.

One counterintuitive finding: Random social interactions matter more than we thought. We created "virtual water cooler" channels and short, optional daily standups focused on personal updates. Team cohesion scores improved 25% after implementing these.

The tools that made the biggest difference weren't fancy collaboration platforms—they were simple shared documents, async video messages (Loom became essential), and a well-organized knowledge base then simple shared documents, async video messages (Loom became essential), and a well-organized knowledge base.

For managers transitioning to remote: Stop measuring hours worked. Start measuring outcomes. Trust your team until they give you a reason not to. And over-communicate context—people need to understand the "why" more than ever when they can't absorb it through office osmosis.

The future isn't fully remote or fully in-office. It's about giving people autonomy to do their best work, wherever that happens to be.
"""


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Multi-Agent Content Repurposing Pipeline v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --input "Your article text here"
  python main.py --file article.txt
  python main.py --url https://example.com/article
  python main.py --sample  # Run with sample content
  python main.py --file article.txt --platforms linkedin twitter
  python main.py --sample --tone conversational --audience "startup founders"
  python main.py --sample --threshold 0.9 --max-iterations 3
        """,
    )

    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument(
        "--input", "-i",
        type=str,
        help="Direct text input to process",
    )
    input_group.add_argument(
        "--file", "-f",
        type=str,
        help="Path to text file to process",
    )
    input_group.add_argument(
        "--url", "-u",
        type=str,
        help="URL to fetch and process",
    )
    input_group.add_argument(
        "--sample", "-s",
        action="store_true",
        help="Use built-in sample content for demonstration",
    )

    # Output options
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="output",
        help="Output directory for results (default: ./output)",
    )

    # User preference options
    parser.add_argument(
        "--tone",
        type=str,
        choices=["professional", "conversational", "casual", "analytical", "storytelling"],
        default="professional",
        help="Content tone (default: professional)",
    )
    parser.add_argument(
        "--audience",
        type=str,
        default="general professionals",
        help="Target audience description",
    )
    parser.add_argument(
        "--goal",
        type=str,
        choices=["engagement", "education", "awareness", "conversion", "thought-leadership"],
        default="engagement",
        help="Content goal (default: engagement)",
    )
    parser.add_argument(
        "--platforms",
        type=str,
        nargs="+",
        choices=["linkedin", "twitter", "newsletter"],
        default=["linkedin", "twitter", "newsletter"],
        help="Platforms to generate content for (default: all)",
    )

    # Pipeline settings
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="Quality score threshold 0-1 (default: 0.85)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=2,
        help="Maximum refinement iterations (default: 2)",
    )

    # LLM options
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="gpt-4o",
        help="OpenAI model to use (default: gpt-4o)",
    )
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.7,
        help="LLM temperature (default: 0.7)",
    )

    # Display options
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress messages",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save results to files",
    )
    parser.add_argument(
        "--show-comparison",
        action="store_true",
        help="Show V1 vs final version comparison after processing",
    )

    args = parser.parse_args()

    # Determine input content
    content: str | None = None
    input_type = "text"

    if args.input:
        content = args.input
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        content = file_path.read_text(encoding="utf-8")
    elif args.url:
        content = args.url
        input_type = "url"
        if not args.quiet:
            print(f"Fetching content from URL: {args.url}")
    elif args.sample:
        content = SAMPLE_CONTENT
        if not args.quiet:
            print("Using built-in sample content for demonstration...")
    else:
        # No input provided, show help
        parser.print_help()
        print("\nError: Please provide input via --input, --file, --url, or --sample")
        return 1

    # Resolve URL if needed
    if input_type == "url":
        try:
            content = resolve_input(input_type, content)
            if not args.quiet:
                print(f"Fetched {len(content.split())} words from URL")
        except ContentFetchError as e:
            print(f"Error fetching URL: {e}", file=sys.stderr)
            return 1

    # Validate content
    if not content or len(content.strip()) < 100:
        print("Error: Content too short (minimum 100 characters)", file=sys.stderr)
        return 1

    # Build user preferences
    user_prefs = UserPreferences(
        tone=args.tone,
        audience=args.audience,
        goal=args.goal,
        platforms=args.platforms
    )

    # Build system settings
    settings = SystemSettings(
        feedback_loop=FeedbackLoopSettings(
            score_threshold=args.threshold,
            max_iterations=args.max_iterations,
            min_key_points=4,
            retry_summarizer_on_failure=True,
            max_summarizer_retries=2
        ),
        scoring_weights=ScoringWeights(),
        verbose=not args.quiet
    )

    # Initialize LLM client
    try:
        llm_client = LLMClient(
            model=args.model,
            temperature=args.temperature,
        )
    except Exception as e:
        print(f"Error initializing LLM client: {e}", file=sys.stderr)
        print("Make sure OPENAI_API_KEY environment variable is set.")
        return 1

    # Initialize and run pipeline
    orchestrator = PipelineOrchestrator(
        llm_client=llm_client,
        verbose=not args.quiet,
        settings=settings,
    )

    try:
        result = orchestrator.run(content, user_prefs)
    except Exception as e:
        print(f"Error during pipeline execution: {e}", file=sys.stderr)
        return 1

    # Save results
    if not args.no_save:
        orchestrator.save_results(result, args.output)

    # Show comparison if requested
    if args.show_comparison:
        orchestrator.print_comparison(result)

    # Print summary
    if not args.quiet:
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)
        print(f"Title: {result.input_summary.title}")
        print(f"Content DNA: {result.input_summary.intent} / {result.input_summary.tone}")
        print(f"Key points extracted: {len(result.input_summary.key_points)}")
        print(f"Iterations: {result.total_iterations}")
        print(f"Final score: {result.final_score:.2f} (threshold: {args.threshold})")
        print(f"Threshold met: {'Yes' if result.threshold_met else 'No'}")
        
        if result.version_2.changes_applied:
            print(f"\nChanges applied: {len(result.version_2.changes_applied)}")
            for change in result.version_2.changes_applied[:3]:
                print(f"  • {change.action} {change.target}: {change.change_type}")

        if not args.no_save:
            print(f"\nResults saved to: {args.output}/")

    return 0


if __name__ == "__main__":
    sys.exit(main())
