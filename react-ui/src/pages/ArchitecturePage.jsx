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
    <div className="page-stack space-y-8">
      {/* Hero Section */}
      <section className="card">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-900 mb-2">
              How the Multi-Agent System Works
            </h1>
            <p className="text-gray-600 max-w-2xl">
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
      <section className="card">
        <SystemPrinciples />
      </section>

      {/* Agent Cards */}
      <section className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Agent Pipeline</h2>
        <p className="text-gray-600 mb-6">
          Four specialized agents working in sequence, each with strict input/output contracts.
        </p>
        <AgentCards />
      </section>

      {/* Agent Contracts */}
      <section className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          Agent Contracts (Structured Data Flow)
        </h2>
        <p className="text-gray-600 mb-6">
          Each agent follows strict input/output schemas for deterministic data flow. Click "Show Explanation" for field details.
        </p>
        <AgentContracts />
      </section>

      {/* Two Column: Traceability + Feedback Loop */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Traceability */}
        <section className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-2">Traceability Pipeline</h2>
          <p className="text-gray-600 mb-6">
            Every output traces back to source key_points via semantic IDs.
          </p>
          <TraceabilityFlow />
        </section>

        {/* Feedback Loop */}
        <section className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-2">Iterative Feedback Loop</h2>
          <p className="text-gray-600 mb-6">
            System iterates until quality threshold (90%) or max iterations reached.
          </p>
          <FeedbackLoopViz />
        </section>
      </div>

      {/* Example Run */}
      <section className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-2">Example Pipeline Run</h2>
        <p className="text-gray-600 mb-6">
          Watch how content flows through the system from raw input to refined output.
        </p>
        <ExampleFlow />
      </section>

      {/* Technical Details (collapsed by default) */}
      <section className="card">
        <details className="group">
          <summary className="cursor-pointer font-semibold text-gray-800 hover:text-blue-600 transition-colors">
            Technical Implementation Details
          </summary>
          <div className="mt-4 space-y-4">
            <div className="p-4 bg-gray-50 rounded-xl">
              <h4 className="font-semibold text-gray-700 mb-2">Constraint Validation</h4>
              <pre className="text-xs bg-slate-900 text-slate-200 rounded-lg p-3 overflow-x-auto">
{`# Hard constraints validated per platform
validate_twitter_thread(tweets, config)  # max 280 chars, 5-8 tweets
validate_linkedin_post(hook, body, cta)  # hook required, CTA required
validate_newsletter(intro, sections)     # 3-5 sections`}
              </pre>
            </div>
            
            <div className="p-4 bg-gray-50 rounded-xl">
              <h4 className="font-semibold text-gray-700 mb-2">Scoring Logic</h4>
              <pre className="text-xs bg-slate-900 text-slate-200 rounded-lg p-3 overflow-x-auto">
{`# Deterministic coverage calculation
coverage = len(used_key_points) / len(total_key_points)

# Penalty-based scoring
if perfect_score:
    score -= perfect_score_penalty  # Prevent cheerleader mode
for violation in violations:
    score -= penalty_per_violation`}
              </pre>
            </div>

            <div className="p-4 bg-gray-50 rounded-xl">
              <h4 className="font-semibold text-gray-700 mb-2">Version Diff Tracking</h4>
              <pre className="text-xs bg-slate-900 text-slate-200 rounded-lg p-3 overflow-x-auto">
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

