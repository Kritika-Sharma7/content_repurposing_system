export const sampleInput = `The Future of Remote Work: Lessons from Five Years of Distributed Teams

After leading distributed engineering teams for five years, I've learned that remote work success isn't about tools or policies—it's about trust and intentional communication.

The biggest mistake companies make is trying to replicate office culture online. Forcing 9-to-5 schedules across time zones destroys productivity. Instead, focus on async-first communication where possible. We reduced meetings by 60% by switching to written proposals with comment-based discussions.

Key insight: Documentation becomes your office. When we mandated that every decision must be documented, onboarding time dropped from 3 months to 3 weeks. New hires could trace the "why" behind every system.

However, some synchronous time is crucial. We found that 2 hours of overlapping time daily was the sweet spot—enough for real-time collaboration without forcing anyone into awkward hours.

The productivity data surprised us: Our remote team shipped 40% more features than our previous co-located team. The secret? Fewer interruptions and more deep work time. We tracked focus blocks and found remote workers averaged 4.2 hours of uninterrupted work daily, versus 2.1 hours in office.

One counterintuitive finding: Random social interactions matter more than we thought. We created "virtual water cooler" channels and short, optional daily standups focused on personal updates. Team cohesion scores improved 25% after implementing these.

The tools that made the biggest difference weren't fancy collaboration platforms—they were simple shared documents, async video messages (Loom became essential), and a well-organized knowledge base.

For managers transitioning to remote: Stop measuring hours worked. Start measuring outcomes. Trust your team until they give you a reason not to. And over-communicate context—people need to understand the "why" more than ever when they can't absorb it through office osmosis.

The future isn't fully remote or fully in-office. It's about giving people autonomy to do their best work, wherever that happens to be.`;

export const sampleResult = {
  input_summary: {
    title: "The Future of Remote Work: Trust, Communication, and Autonomy",
    one_liner:
      "Remote work thrives on trust, intentional communication, and autonomy, not on replicating office culture online.",
    key_points: [
      "Remote work success depends on trust and intentional communication, not tools",
      "Async-first communication reduces meetings by 60% and increases productivity",
      "Documentation cuts onboarding from 3 months to 3 weeks",
      "2 hours of daily overlap is the sweet spot for synchronous collaboration",
      "Remote teams ship 40% more features due to fewer interruptions",
    ],
    key_insights: [
      {
        id: "insight_1",
        topic: "Trust and Communication",
        insight:
          "Remote work success is built on trust and intentional communication rather than tools or policies.",
        importance: "high",
      },
      {
        id: "insight_2",
        topic: "Async-First Communication",
        insight:
          "Adopting async-first communication can reduce meetings by 60% and enhance productivity.",
        importance: "high",
      },
      {
        id: "insight_3",
        topic: "Documentation as a Tool",
        insight:
          "Mandating documentation for every decision cuts onboarding from 3 months to 3 weeks.",
        importance: "high",
      },
      {
        id: "insight_4",
        topic: "Synchronous Collaboration",
        insight:
          "2 hours of daily overlap is the sweet spot for real-time collaboration.",
        importance: "medium",
      },
      {
        id: "insight_5",
        topic: "Productivity Gains",
        insight:
          "Remote teams ship 40% more features due to 4.2 hours of uninterrupted work daily vs 2.1 in office.",
        importance: "high",
      },
    ],
    target_audience:
      "Remote team managers, HR professionals, and organizational leaders managing distributed teams.",
    main_theme:
      "The future of work is about empowering employees with trust, effective communication, and autonomy.",
    word_count_original: 450,
  },
  version_1: {
    version: 1,
    linkedin: {
      hook: "What if more meetings are not the answer to better remote work?",
      body: "Remote work is not about mimicking office culture online. It is about trust, intentional communication, and autonomy. Async-first communication can reduce meetings and increase focus. Documentation strengthens onboarding and shared context.",
      call_to_action: "How are you enabling autonomy in your remote teams?",
      hashtags: ["RemoteWork", "Leadership", "Productivity"],
      source_insights: ["insight_1", "insight_2", "insight_3"],
    },
    twitter: {
      thread_hook: "Is more communication really the key to better remote work?",
      tweets: [
        "1/ Remote work is not office work on Zoom. It is trust + intentional communication + autonomy.",
        "2/ Async-first communication can cut meetings by 60% and increase deep work.",
        "3/ Documentation is the new office memory. It cuts onboarding from 3 months to 3 weeks.",
        "4/ Measure outcomes, not hours, and your team will move faster.",
      ],
      source_insights: ["insight_1", "insight_2", "insight_3"],
      tweet_mappings: [
        { tweet_index: 0, derived_from: ["key_points[0]"] },
        { tweet_index: 1, derived_from: ["key_points[1]"] },
        { tweet_index: 2, derived_from: ["key_points[2]"] },
        { tweet_index: 3, derived_from: ["key_points[4]"] },
      ],
    },
    newsletter: {
      subject_line: "Revolutionize Remote Work with Trust and Autonomy",
      preview_text: "Empower your team with trust, not constant meetings.",
      intro:
        "As remote work matures, the teams that perform best are optimizing for trust and clarity.",
      body_sections: [
        "Trust and communication should be intentional, not noisy.",
        "Async-first systems reduce meetings by 60% and increase output.",
        "Documentation cuts onboarding from 3 months to 3 weeks.",
      ],
      closing:
        "What shift can your team make this week to improve remote collaboration?",
      source_insights: ["insight_1", "insight_2", "insight_3"],
    },
  },
  review: {
    coverage_score: 7,
    clarity_score: 8,
    engagement_score: 7,
    consistency_score: 9,
    overall_alignment_score: 8,
    missing_points: [
      "key_points[3] (2-hour overlap) not in any format",
      "key_points[4] (40% more features) only in implied form",
    ],
    linkedin_review: {
      format_name: "linkedin",
      clarity_score: 8,
      engagement_score: 7,
      missing_insights: ["insight_4", "insight_5"],
      strengths: ["Strong hook", "Clear structure"],
      weaknesses: ["Missing synchronous collaboration insight", "Missing productivity stats"],
      specific_suggestions: ["Add reference to 2-hour overlap window", "Include 40% productivity stat"],
    },
    twitter_review: {
      format_name: "twitter",
      clarity_score: 8,
      engagement_score: 7,
      missing_insights: ["insight_4"],
      strengths: ["Punchy tweets", "Good flow", "Has tweet_mappings"],
      weaknesses: ["Final tweet CTA could be stronger"],
      specific_suggestions: ["Strengthen final tweet with question"],
    },
    newsletter_review: {
      format_name: "newsletter",
      clarity_score: 8,
      engagement_score: 7,
      missing_insights: ["insight_4", "insight_5"],
      strengths: ["Scannable sections", "Good subject line"],
      weaknesses: ["Missing sync collaboration content"],
      specific_suggestions: ["Add section on synchronous overlap window"],
    },
    issues: [
      {
        id: "issue_1",
        type: "missing_insight",
        description: "Synchronous collaboration insight not covered",
        affected_formats: ["linkedin", "twitter", "newsletter"],
        severity: "high",
        source_insight_id: "insight_4",
      },
      {
        id: "issue_2",
        type: "engagement",
        description: "Twitter thread final tweet lacks strong CTA",
        affected_formats: ["twitter"],
        severity: "medium",
        source_insight_id: null,
      },
    ],
    critical_issues: [
      "Missing synchronous collaboration insight (insight_4) across all formats",
    ],
    priority_improvements: [
      "Add synchronous collaboration references to all formats",
      "Strengthen final tweet CTA for discussion",
      "Add virtual social rituals to newsletter",
    ],
  },
  version_2: {
    version: 2,
    linkedin: {
      hook: "What if more meetings are not the answer to better remote work?",
      body: "Remote work is not about copying office culture online. It is about trust, intentional communication, and autonomy. Async-first communication reduces meeting overload and creates deep-work time. Documentation keeps decisions visible. A small synchronous overlap window supports collaboration. Virtual social touchpoints improve team cohesion.",
      call_to_action: "Which remote-work operating principle has had the biggest impact on your team?",
      hashtags: ["RemoteWork", "Leadership", "Productivity", "TeamCohesion"],
      source_insights: ["insight_1", "insight_2", "insight_3", "insight_4"],
    },
    twitter: {
      thread_hook: "Is more communication really the key to better remote work?",
      tweets: [
        "1/ Remote work is not office work on Zoom. It is trust + intentional communication + autonomy.",
        "2/ Async-first communication cuts meeting noise and unlocks deep work.",
        "3/ Documentation is the operating system for distributed teams.",
        "4/ Keep a short overlap window for critical synchronous collaboration.",
        "5/ How is your team balancing async depth with human connection?",
      ],
      source_insights: ["insight_1", "insight_2", "insight_3", "insight_4"],
    },
    newsletter: {
      subject_line: "Revolutionize Remote Work with Trust and Autonomy",
      preview_text: "Empower your team with trust and intentional systems.",
      intro:
        "Remote performance improves when teams optimize for trust, clarity, and sustainable communication patterns.",
      body_sections: [
        "Run async-first to reduce interruptions and increase focused output.",
        "Use lightweight synchronous overlap for decisions that need live collaboration.",
        "Create virtual social rituals to keep cohesion high.",
        "Measure outcomes, not visible activity.",
      ],
      closing:
        "Reply with one remote-work policy your team changed that improved performance.",
      source_insights: ["insight_1", "insight_2", "insight_3", "insight_4"],
    },
    change_records: [
      {
        issue_id: "issue_1",
        action: "added",
        location: "linkedin_body",
        description: "Added synchronous overlap window reference",
        source_insight_id: "insight_4",
      },
      {
        issue_id: "issue_1",
        action: "added",
        location: "twitter_thread",
        description: "Added tweet about synchronous collaboration",
        source_insight_id: "insight_4",
      },
      {
        issue_id: "issue_2",
        action: "modified",
        location: "twitter_thread",
        description: "Strengthened final tweet with engagement question",
        source_insight_id: null,
      },
      {
        issue_id: "issue_1",
        action: "added",
        location: "newsletter_body",
        description: "Added synchronous overlap section",
        source_insight_id: "insight_4",
      },
    ],
    changes_made: [
      "Added synchronous collaboration references to all formats",
      "Strengthened CTA in Twitter thread ending",
      "Improved cross-format consistency of key insights",
    ],
    addressed_issues: ["issue_1", "issue_2"],
  },
  iterations: [
    {
      iteration: 1,
      score: 7.75,
      review: null,
      refined: null,
    },
  ],
  final_score: 8.5,
};
