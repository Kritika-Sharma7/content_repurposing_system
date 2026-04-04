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
    <div className="page-stack space-y-4 max-w-7xl mx-auto px-4">
      {/* Hero Section - More Compact */}
      <section className="card" style={{ padding: '20px' }}>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
          <div className="lg:col-span-2">
            <h1 className="text-2xl md:text-3xl font-bold text-gray-900 mb-2">
              How the Multi-Agent System Works
            </h1>
            <p className="text-sm text-gray-600 leading-relaxed">
              A structured multi-agent system where each agent has a defined role, operates on structured data, and participates in a feedback loop to iteratively improve output quality.
            </p>
          </div>
          <div className="flex justify-center lg:justify-end">
            <SystemLegend />
          </div>
        </div>
      </section>

      {/* Main Dashboard Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        {/* Left Column - Pipeline */}
        <section className="xl:col-span-2 card" style={{ padding: '20px' }}>
          <h3 className="text-lg font-bold text-gray-900 mb-3 text-center">Pipeline Flow</h3>
          <WorkflowDiagram />
        </section>

        {/* Right Column - Design Principles */}
        <section className="card" style={{ padding: '20px' }}>
          <h3 className="text-lg font-bold text-gray-900 mb-3">Design Principles</h3>
          <div className="space-y-3">
            <SystemPrinciples />
          </div>
        </section>
      </div>

      {/* Agent Cards - Compact 2x2 Grid */}
      <section className="card" style={{ padding: '20px' }}>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Agent Pipeline</h2>
            <p className="text-sm text-gray-600 mb-4">
              Four specialized agents working in sequence, each with strict input/output contracts.
            </p>
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Agent Contracts</h2>
            <p className="text-sm text-gray-600 mb-4">
              Each agent follows strict input/output schemas for deterministic data flow.
            </p>
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div>
            <AgentCards />
          </div>
          <div>
            <AgentContracts />
          </div>
        </div>
      </section>

      {/* Bottom Row - Traceability + Feedback + Example */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Traceability */}
        <section className="card" style={{ padding: '16px' }}>
          <h3 className="text-base font-bold text-gray-900 mb-2">Traceability Pipeline</h3>
          <p className="text-xs text-gray-600 mb-3">
            Every output traces back to source key_points via semantic IDs.
          </p>
          <TraceabilityFlow />
        </section>

        {/* Feedback Loop */}
        <section className="card" style={{ padding: '16px' }}>
          <h3 className="text-base font-bold text-gray-900 mb-2">Iterative Feedback Loop</h3>
          <p className="text-xs text-gray-600 mb-3">
            Reviewer identifies structured issues → Refiner applies targeted fixes → repeated until no critical issues remain
          </p>
          <FeedbackLoopViz />
        </section>

        {/* Example Run */}
        <section className="card" style={{ padding: '16px' }}>
          <h3 className="text-base font-bold text-gray-900 mb-2">Example Pipeline Run</h3>
          <p className="text-xs text-gray-600 mb-3">
            Watch how content flows through the system from raw input to refined output.
          </p>
          <ExampleFlow />
        </section>
      </div>

      {/* Technical Details - Collapsed by default */}
      <section className="card" style={{ padding: '16px' }}>
        <details className="group">
          <summary className="cursor-pointer font-bold text-base text-gray-800 hover:text-blue-600 transition-colors">
            ⚙️ Technical Implementation Details
          </summary>
          <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
              <h4 className="font-bold text-gray-800 mb-1 text-sm">Backend</h4>
              <p className="text-xs text-gray-700 mb-2">LLM-based agents operating on structured schemas</p>
              <pre className="text-xs bg-slate-900 text-slate-200 rounded p-2 overflow-x-auto">
{`# Hard constraints validated per platform
validate_twitter_thread(tweets, config)
validate_linkedin_post(hook, body, cta)
validate_newsletter(intro, sections)`}
              </pre>
            </div>
            
            <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
              <h4 className="font-bold text-gray-800 mb-1 text-sm">Frontend</h4>
              <p className="text-xs text-gray-700 mb-2">Step-wise visualization of agent outputs and iterations</p>
              <pre className="text-xs bg-slate-900 text-slate-200 rounded p-2 overflow-x-auto">
{`# Deterministic coverage calculation
coverage = len(used_key_points) / len(total_key_points)

# Penalty-based scoring
for violation in violations:
    score -= penalty_per_violation`}
              </pre>
            </div>

            <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
              <h4 className="font-bold text-gray-800 mb-1 text-sm">Architecture</h4>
              <p className="text-xs text-gray-700 mb-1">Structured data contracts between agents</p>
              <p className="text-xs text-gray-700 mb-2">Explicit versioning (V1 → V2 → V3)</p>
              <pre className="text-xs bg-slate-900 text-slate-200 rounded p-2 overflow-x-auto">
{`{
  "version": "v2",
  "parent": "v1",
  "diff": {
    "changes": [
      { "field": "linkedin.hook", "before": "...", "after": "..." }
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
