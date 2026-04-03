"""
Mock data for testing UI without burning API credits.
This simulates the complete pipeline output structure.
"""

MOCK_PIPELINE_RESULT = {
    "summary": {
        "core_message": "Remote work success requires shifting from office replication to async-first communication, focusing on outcomes rather than hours, and creating intentional social connections.",
        "key_points": [
            {
                "id": "kp_1",
                "label": "Companies fail by trying to replicate office culture online with forced schedules and constant meetings",
                "reason": "This approach destroys productivity across time zones and prevents deep work",
                "priority": "critical",
                "type": "conflict",
                "data": "60% meeting reduction"
            },
            {
                "id": "kp_2", 
                "label": "Documentation becomes your office when every decision is written down",
                "reason": "Enables async work and reduces onboarding time dramatically",
                "priority": "critical",
                "type": "insight",
                "data": "3 months to 3 weeks onboarding"
            },
            {
                "id": "kp_3",
                "label": "Remote workers average 4.2 hours of deep work vs 2.1 hours in office",
                "reason": "Fewer interruptions and more focused time blocks lead to higher productivity",
                "priority": "high",
                "type": "data",
                "data": "40% more features shipped"
            },
            {
                "id": "kp_4",
                "label": "Virtual water cooler channels and optional standups recreate social connections",
                "reason": "Random social interactions matter more than expected for team cohesion",
                "priority": "high",
                "type": "insight",
                "data": "25% cohesion improvement"
            },
            {
                "id": "kp_5",
                "label": "Managers should measure outcomes instead of hours worked",
                "reason": "Trust and autonomy are fundamental to remote team success",
                "priority": "medium",
                "type": "principle",
                "data": None
            }
        ],
        "version": 1
    },
    
    "v1": {
        "linkedin": {
            "content": "Most companies get remote work wrong.\n\nThey try to replicate the office online. Same meetings. Same schedules. Same monitoring.\n\nIt doesn't work.\n\nThe shift happened when we stopped forcing office habits and started building for distributed work.\n\nKey changes:\n– Async-first communication (60% fewer meetings)\n– Written documentation for every decision\n– Focus on outcomes, not hours\n\nResult? Our remote team shipped 40% more features than our previous office team.\n\nThe secret wasn't better tools. It was fewer interruptions and more deep work time.\n\nRemote work isn't about flexibility. It's about intentional design.\n\nWhat office habit would you eliminate first?",
            "used_kps": ["kp_1", "kp_2", "kp_3"]
        },
        "twitter": {
            "tweets": [
                "1/6\n\nMost companies fail at remote work for one simple reason:\n\nThey try to recreate the office online.",
                "2/6\n\nSame schedules across time zones.\nConstant meetings.\nAlways-on availability.\n\nThis approach kills productivity before it starts.",
                "3/6\n\nThe teams that succeed do the opposite:\n\nThey design for async-first communication.\n\nDecisions move to written form instead of calls.",
                "4/6\n\nThat single shift changes everything:\n\nFewer interruptions → 4.2 hours of deep work daily\nLess coordination → 40% more features shipped\nBetter documentation → 3-week onboarding",
                "5/6\n\nVirtual water coolers replaced random office chats, improving team cohesion by 25%.\n\nSocial connection still matters—it just needs to be intentional.",
                "6/6\n\nRemote work succeeds with trust and outcomes, not by copying the office.\n\nIt's time to rethink old habits."
            ],
            "used_kps": ["kp_1", "kp_2", "kp_3", "kp_4"]
        },
        "newsletter": {
            "content": "## Remote Work: Stop Copying the Office\n\n**The mistake most companies make:** Trying to replicate office culture in a distributed environment.\n\n**Key insights from 5 years of remote leadership:**\n\n• **Async-first wins** - Reduced meetings by 60% through written proposals and comment-based discussions\n• **Documentation as office** - When decisions are written, onboarding drops from 3 months to 3 weeks  \n• **Focus time matters** - Remote workers average 4.2 hours of uninterrupted work vs 2.1 in office\n• **Intentional social connection** - Virtual water cooler channels improved team cohesion by 25%\n\n**Bottom line:** Remote teams shipped 40% more features by optimizing for deep work, not availability.\n\nSuccess isn't about better video calls—it's about rethinking how work gets done.",
            "used_kps": ["kp_1", "kp_2", "kp_3", "kp_4"]
        },
        "version": 1
    },
    
    "review": {
        "issues": [
            {
                "issue_id": "issue_1",
                "type": "coverage",
                "priority": "high",
                "problem": "Missing management guidance across all formats",
                "reason": "Key insight about measuring outcomes vs hours is absent from all platforms",
                "suggestion": "Add content about managers focusing on trust and outcomes rather than time tracking",
                "affects": ["linkedin", "twitter", "newsletter"],
                "missing_kps": ["kp_5"]
            },
            {
                "issue_id": "issue_2",
                "type": "consistency",
                "priority": "medium", 
                "problem": "Twitter thread lacks productivity data that other formats emphasize",
                "reason": "LinkedIn and newsletter highlight 40% feature improvement but Twitter thread doesn't connect this clearly",
                "suggestion": "Strengthen the productivity narrative in Twitter thread with specific results",
                "affects": ["twitter"],
                "missing_kps": []
            }
        ],
        "summary": {
            "total_issues": 2,
            "critical": 0,
            "high": 1,
            "medium": 1
        },
        "status": "needs_fixes"
    },
    
    "v2": {
        "linkedin": {
            "content": "Most companies get remote work wrong.\n\nThey try to replicate the office online. Same meetings. Same schedules. Same monitoring.\n\nIt doesn't work.\n\nThe shift happened when we stopped forcing office habits and started building for distributed work.\n\nKey changes:\n– Async-first communication (60% fewer meetings)\n– Written documentation for every decision\n– Focus on outcomes, not hours\n\nResult? Our remote team shipped 40% more features than our previous office team.\n\nThe secret wasn't better tools. It was fewer interruptions and more deep work time.\n\nFor managers: measure outputs, not hours. Trust your team until proven otherwise.\n\nRemote work isn't about flexibility. It's about intentional design.\n\nWhat office habit would you eliminate first?",
            "used_kps": ["kp_1", "kp_2", "kp_3", "kp_5"]
        },
        "twitter": {
            "tweets": [
                "1/6\n\nMost companies fail at remote work for one simple reason:\n\nThey try to recreate the office online.",
                "2/6\n\nSame schedules across time zones.\nConstant meetings.\nAlways-on availability.\n\nThis approach kills productivity before it starts.",
                "3/6\n\nThe teams that succeed do the opposite:\n\nThey design for async-first communication.\n\nDecisions move to written form instead of calls.",
                "4/6\n\nThat single shift unlocks massive productivity gains:\n\nFewer interruptions → 4.2 hours of deep work daily\nBetter focus → 40% more features shipped\nClear docs → 3-week onboarding vs 3 months",
                "5/6\n\nVirtual water coolers replaced random office chats, improving team cohesion by 25%.\n\nSocial connection still matters—it just needs to be intentional.",
                "6/6\n\nFor managers: measure outcomes, not screen time.\n\nRemote work succeeds with trust and results, not by copying the office."
            ],
            "used_kps": ["kp_1", "kp_2", "kp_3", "kp_4", "kp_5"]
        },
        "newsletter": {
            "content": "## Remote Work: Stop Copying the Office\n\n**The mistake most companies make:** Trying to replicate office culture in a distributed environment.\n\n**Key insights from 5 years of remote leadership:**\n\n• **Async-first wins** - Reduced meetings by 60% through written proposals and comment-based discussions\n• **Documentation as office** - When decisions are written, onboarding drops from 3 months to 3 weeks  \n• **Focus time matters** - Remote workers average 4.2 hours of uninterrupted work vs 2.1 in office\n• **Intentional social connection** - Virtual water cooler channels improved team cohesion by 25%\n• **Management shift required** - Measure outcomes instead of hours worked; trust teams until proven otherwise\n\n**Bottom line:** Remote teams shipped 40% more features by optimizing for deep work, not availability.\n\nSuccess isn't about better video calls—it's about rethinking how work gets done.",
            "used_kps": ["kp_1", "kp_2", "kp_3", "kp_4", "kp_5"]
        },
        "version": 2,
        "changes": [
            {
                "issue_id": "issue_1",
                "action": "add",
                "target": "linkedin_management_guidance",
                "before": "The secret wasn't better tools. It was fewer interruptions and more deep work time.",
                "after": "The secret wasn't better tools. It was fewer interruptions and more deep work time.\n\nFor managers: measure outputs, not hours. Trust your team until proven otherwise."
            },
            {
                "issue_id": "issue_2", 
                "action": "modify",
                "target": "twitter_tweet_4",
                "before": "That single shift changes everything:\n\nFewer interruptions → 4.2 hours of deep work daily\nLess coordination → 40% more features shipped\nBetter documentation → 3-week onboarding",
                "after": "That single shift unlocks massive productivity gains:\n\nFewer interruptions → 4.2 hours of deep work daily\nBetter focus → 40% more features shipped\nClear docs → 3-week onboarding vs 3 months"
            }
        ]
    },
    
    "metrics": {
        "issues_found": 2,
        "issues_fixed": 2,
        "iterations": 1,
        "status": "complete"
    }
}

# Mock input text for testing
MOCK_INPUT_TEXT = """The Future of Remote Work: Lessons from Five Years of Distributed Teams

After leading distributed engineering teams for five years, I've learned that remote work success isn't about tools or policies—it's about trust and intentional communication.

The biggest mistake companies make is trying to replicate office culture online. Forcing 9-to-5 schedules across time zones destroys productivity. Instead, focus on async-first communication where possible. We reduced meetings by 60% by switching to written proposals with comment-based discussions.

Key insight: Documentation becomes your office. When we mandated that every decision must be documented, onboarding time dropped from 3 months to 3 weeks. New hires could trace the "why" behind every system.

However, some synchronous time is crucial. We found that 2 hours of overlapping time daily was the sweet spot—enough for real-time collaboration without forcing anyone into awkward hours.

The productivity data surprised us: Our remote team shipped 40% more features than our previous co-located team. The secret? Fewer interruptions and more deep work time. We tracked focus blocks and found remote workers averaged 4.2 hours of uninterrupted work daily, versus 2.1 hours in office.

One counterintuitive finding: Random social interactions matter more than we thought. We created "virtual water cooler" channels and short, optional daily standups focused on personal updates. Team cohesion scores improved 25% after implementing these.

The tools that made the biggest difference weren't fancy collaboration platforms—they were simple shared documents, async video messages (Loom became essential), and a well-organized knowledge base.

For managers transitioning to remote: Stop measuring hours worked. Start measuring outcomes. Trust your team until they give you a reason not to. And over-communicate context—people need to understand the "why" more than ever when they can't absorb it through office osmosis.

The future isn't fully remote or fully in-office. It's about giving people autonomy to do their best work, wherever that happens to be."""