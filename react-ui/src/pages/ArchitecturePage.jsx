import { useState } from 'react';
import {
  WorkflowDiagram,
  SystemPrinciples,
  AgentContracts,
  AgentCards,
  TraceabilityFlow,
  FeedbackLoopViz,
  ExampleFlow,
  SystemLegend,
} from '../components/architecture';

export default function ArchitecturePage() {
  const [activeSection, setActiveSection] = useState(null);

  return (
    <div className="page-stack space-y-10">
      {/* Hero Section */}
      <section className="card" style={{ padding: '32px' }}>
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-8">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
              How the Multi-Agent System Works
            </h1>
            <p className="text-base text-gray-600 max-w-2xl leading-relaxed">
              A constraint-driven, platform-aware content repurposing pipeline with full traceability, 
              iterative feedback loops, and versioning.
            </p>
          </div>
          <SystemLegend />
        </div>
        
        {/* Interactive Workflow */}
        <WorkflowDiagram />
      </section>

      {/* Design Principles */}
      <section className="card" style={{ padding: '32px' }}>
        <SystemPrinciples />
      </section>

      {/* Agent Cards */}
      <section className="card" style={{ padding: '32px' }}>
        <h2 className="text-2xl font-bold text-gray-900 mb-3">Agent Pipeline</h2>
        <p className="text-base text-gray-600 mb-8">
          Four specialized agents working in sequence, each with strict input/output contracts.
        </p>
        <AgentCards />
      </section>

      {/* Agent Contracts */}
      <section className="card" style={{ padding: '32px' }}>
        <h2 className="text-2xl font-bold text-gray-900 mb-3">
          Agent Contracts (Structured Data Flow)
        </h2>
        <p className="text-base text-gray-600 mb-8">
          Each agent follows strict input/output schemas for deterministic data flow. Click "Show Explanation" for field details.
        </p>
        <AgentContracts />
      </section>

      {/* Two Column: Traceability + Feedback Loop */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Traceability */}
        <section className="card" style={{ padding: '28px' }}>
          <h2 className="text-xl font-bold text-gray-900 mb-3">Traceability Pipeline</h2>
          <p className="text-base text-gray-600 mb-6">
            Every output traces back to source key_points via semantic IDs.
          </p>
          <TraceabilityFlow />
        </section>

        {/* Feedback Loop */}
        <section className="card" style={{ padding: '28px' }}>
          <h2 className="text-xl font-bold text-gray-900 mb-3">Iterative Feedback Loop</h2>
          <p className="text-base text-gray-600 mb-6">
            System iterates until quality threshold (90%) or max iterations reached.
          </p>
          <FeedbackLoopViz />
        </section>
      </div>

      {/* Example Run */}
      <section className="card" style={{ padding: '32px' }}>
        <h2 className="text-2xl font-bold text-gray-900 mb-3">Example Pipeline Run</h2>
        <p className="text-base text-gray-600 mb-8">
          Watch how content flows through the system from raw input to refined output.
        </p>
        <ExampleFlow />
      </section>

      {/* Technical Details (collapsed by default) */}
      <section className="card" style={{ padding: '32px' }}>
        <details className="group">
          <summary className="cursor-pointer font-bold text-lg text-gray-800 hover:text-blue-600 transition-colors">
            ⚙️ Technical Implementation Details
          </summary>
          <div className="mt-6 space-y-5">
            <div className="p-5 bg-gray-50 rounded-xl border border-gray-200">
              <h4 className="font-bold text-gray-800 mb-3 text-base">Constraint Validation</h4>
              <pre className="text-sm bg-slate-900 text-slate-200 rounded-lg p-4 overflow-x-auto">
{`# Hard constraints validated per platform
validate_twitter_thread(tweets, config)  # max 280 chars, 5-8 tweets
validate_linkedin_post(hook, body, cta)  # hook required, CTA required
validate_newsletter(intro, sections)     # 3-5 sections`}
              </pre>
            </div>
            
            <div className="p-5 bg-gray-50 rounded-xl border border-gray-200">
              <h4 className="font-bold text-gray-800 mb-3 text-base">Scoring Logic</h4>
              <pre className="text-sm bg-slate-900 text-slate-200 rounded-lg p-4 overflow-x-auto">
{`# Deterministic coverage calculation
coverage = len(used_key_points) / len(total_key_points)

# Penalty-based scoring
if perfect_score:
    score -= perfect_score_penalty  # Prevent cheerleader mode
for violation in violations:
    score -= penalty_per_violation`}
              </pre>
            </div>

            <div className="p-5 bg-gray-50 rounded-xl border border-gray-200">
              <h4 className="font-bold text-gray-800 mb-3 text-base">Version Diff Tracking</h4>
              <pre className="text-sm bg-slate-900 text-slate-200 rounded-lg p-4 overflow-x-auto">
{`{
  "version": "v2",
  "parent": "v1",
  "diff": {
    "changes": [
      { "field": "linkedin.hook", "before": "...", "after": "..." },
      { "field": "twitter.tweet_count", "before": 5, "after": 6 }
    ]
  }
}`}
              </pre>
            </div>
          </div>
        </details>
      </section>
    </div>
  );
}

