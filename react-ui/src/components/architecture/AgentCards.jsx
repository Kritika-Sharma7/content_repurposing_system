import { Brain, Palette, Search, Wrench } from 'lucide-react';

const agents = [
  {
    name: 'Summarizer',
    icon: Brain,
    color: 'blue',
    borderColor: 'border-blue-300',
    bgColor: 'bg-blue-50',
    textColor: 'text-blue-700',
    iconBg: 'bg-blue-100',
    role: 'Extracts Content DNA from raw input. Outputs semantic key_points as structured units with IDs for downstream traceability.',
    input: '{ raw_text: string }',
    output: 'SummaryOutput { title, core_message, key_points[{id, concept, claim, implication}], intent, tone }',
    keyFeature: 'Semantic units enable deterministic coverage tracking',
  },
  {
    name: 'Formatter',
    icon: Palette,
    color: 'purple',
    borderColor: 'border-purple-300',
    bgColor: 'bg-purple-50',
    textColor: 'text-purple-700',
    iconBg: 'bg-purple-100',
    role: 'Transforms summary into platform-specific content with full source traceability.',
    input: 'SummaryOutput + UserPreferences',
    output: 'FormattedOutput { linkedin, twitter, newsletter } with derived_from[] per piece',
    keyFeature: 'Hard constraints: tweets ≤280 chars, thread 5-8 tweets',
  },
  {
    name: 'Reviewer',
    icon: Search,
    color: 'orange',
    borderColor: 'border-orange-300',
    bgColor: 'bg-orange-50',
    textColor: 'text-orange-700',
    iconBg: 'bg-orange-100',
    role: 'Evaluates content with deterministic scoring + LLM analysis. Produces structured issues for targeted refinement.',
    input: 'SummaryOutput + FormattedOutput',
    output: 'ReviewOutput { scores, coverage_analysis, violations[], issues[] }',
    keyFeature: 'coverage = used_key_points / total_key_points (deterministic)',
  },
  {
    name: 'Refiner',
    icon: Wrench,
    color: 'green',
    borderColor: 'border-green-300',
    bgColor: 'bg-green-50',
    textColor: 'text-green-700',
    iconBg: 'bg-green-100',
    role: 'Makes targeted fixes based on reviewer issues. No full rewrites, only surgical changes with audit trail.',
    input: 'SummaryOutput + FormattedOutput + ReviewOutput',
    output: 'RefinedOutput { content, changes_applied[{issue_id, action, target}] }',
    keyFeature: 'Each change links to specific issue_id for auditability',
  },
];

export default function AgentCards() {
  return (
    <div className="agent-cards grid grid-cols-1 md:grid-cols-2 gap-6">
      {agents.map((agent) => {
        const Icon = agent.icon;

        return (
          <div
            key={agent.name}
            className={`
              agent-card-enhanced rounded-xl border-3 p-6
              ${agent.borderColor} bg-white
              hover:shadow-2xl transition-all duration-300
              hover:scale-102
            `}
            style={{ borderWidth: '2px' }}
          >
            {/* Header */}
            <div className="flex items-start gap-4 mb-5">
              <div className={`p-3 rounded-xl ${agent.iconBg} shadow-md`}>
                <Icon className={`w-7 h-7 ${agent.textColor}`} />
              </div>
              <div>
                <h3 className={`font-bold text-xl ${agent.textColor} mb-2`}>{agent.name}</h3>
                <p className="text-sm text-gray-700 leading-relaxed">{agent.role}</p>
              </div>
            </div>

            {/* I/O */}
            <div className="space-y-4">
              <div>
                <span className="text-xs font-bold text-gray-600 uppercase tracking-wider">Input</span>
                <code className={`block text-xs mt-2 p-3 rounded-lg ${agent.bgColor} ${agent.textColor} font-mono leading-relaxed`}>
                  {agent.input}
                </code>
              </div>
              <div>
                <span className="text-xs font-bold text-gray-600 uppercase tracking-wider">Output</span>
                <code className={`block text-xs mt-2 p-3 rounded-lg ${agent.bgColor} ${agent.textColor} font-mono leading-relaxed`}>
                  {agent.output}
                </code>
              </div>
            </div>

            {/* Key feature */}
            <div className={`mt-5 pt-4 border-t-2 ${agent.borderColor}`}>
              <div className="flex items-start gap-2">
                <span className={`text-sm font-bold ${agent.textColor}`}>💡 Key Feature:</span>
                <span className="text-sm text-gray-700">{agent.keyFeature}</span>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
