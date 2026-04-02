import { useState } from 'react';
import { ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';

const contractsData = [
  {
    name: 'SummaryOutput',
    color: 'blue',
    schema: {
      title: 'string',
      one_liner: 'string',
      core_message: 'string',
      intent: '"educational" | "persuasive" | "informational"',
      tone: '"informative" | "analytical" | "storytelling"',
      structure: '"problem-solution" | "narrative" | "listicle"',
      key_points: '[{ id, concept, claim, implication, importance }]',
      target_audience: 'string',
    },
    explanation: [
      { field: 'key_points', desc: 'Semantic units with ID for traceability (kp_1, kp_2)' },
      { field: 'concept + claim', desc: 'Structured data enabling deterministic downstream use' },
      { field: 'importance', desc: 'Priority level: critical | high | medium | supporting' },
    ],
  },
  {
    name: 'FormattedOutput',
    color: 'purple',
    schema: {
      linkedin: '{ hook, body, cta, hashtags[], derived_from[] }',
      twitter: '{ thread_hook, tweets[], tweet_mappings[], derived_from[] }',
      newsletter: '{ subject, preview, intro, body_sections[], closing, derived_from[] }',
    },
    explanation: [
      { field: 'derived_from', desc: 'Links to source key_point IDs (e.g., ["kp_1", "kp_3"])' },
      { field: 'tweet_mappings', desc: 'Per-tweet traceability: { tweet_index, derived_from[] }' },
      { field: 'constraints', desc: 'Tweets ≤280 chars, thread 5-8 tweets, hook required' },
    ],
  },
  {
    name: 'ReviewOutput',
    color: 'orange',
    schema: {
      scores: '{ clarity, engagement, coverage, consistency, platform_fit }',
      coverage_analysis: '{ missing_key_points[], used_key_points[], coverage_by_format }',
      violations: '[{ type, message, location, severity }]',
      issues: '[{ id, type, severity, target, related_key_point }]',
      cross_format_consistency: '{ missing_points[], contradictions[], tone_mismatch[] }',
    },
    explanation: [
      { field: 'coverage', desc: 'Deterministic: used_key_points / total_key_points' },
      { field: 'violations', desc: 'Hard constraint failures (tweet length, missing hook)' },
      { field: 'issues', desc: 'Structured problems for targeted refinement' },
    ],
  },
  {
    name: 'RefinedOutput',
    color: 'green',
    schema: {
      version: 'number',
      linkedin: 'LinkedInPost',
      twitter: 'TwitterThread',
      newsletter: 'NewsletterSection',
      changes_applied: '[{ issue_id, action, target, change_type, related_key_point }]',
      addressed_issues: 'string[]',
    },
    explanation: [
      { field: 'changes_applied', desc: 'Audit trail linking each change to an issue' },
      { field: 'version', desc: 'Incremented with each refinement iteration' },
      { field: 'issue_id', desc: 'References specific issue from ReviewOutput' },
    ],
  },
];

const colorClasses = {
  blue: { border: 'border-blue-300', bg: 'bg-blue-50', text: 'text-blue-700', badge: 'bg-blue-100' },
  purple: { border: 'border-purple-300', bg: 'bg-purple-50', text: 'text-purple-700', badge: 'bg-purple-100' },
  orange: { border: 'border-orange-300', bg: 'bg-orange-50', text: 'text-orange-700', badge: 'bg-orange-100' },
  green: { border: 'border-green-300', bg: 'bg-green-50', text: 'text-green-700', badge: 'bg-green-100' },
};

function ContractCard({ contract }) {
  const [showExplanation, setShowExplanation] = useState(false);
  const [copied, setCopied] = useState(false);
  const colors = colorClasses[contract.color];

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(contract.schema, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`contract-card-enhanced rounded-xl border-2 ${colors.border} bg-white overflow-hidden hover:shadow-md transition-all duration-300`}>
      {/* Header */}
      <div className={`px-4 py-3 ${colors.bg} border-b ${colors.border} flex items-center justify-between`}>
        <h4 className={`font-semibold ${colors.text}`}>{contract.name}</h4>
        <button
          onClick={handleCopy}
          className="p-1.5 rounded-lg hover:bg-white/50 transition-colors"
          title="Copy schema"
        >
          {copied ? (
            <Check className="w-4 h-4 text-green-600" />
          ) : (
            <Copy className="w-4 h-4 text-gray-500" />
          )}
        </button>
      </div>

      {/* Schema */}
      <div className="p-3">
        <pre className="text-xs bg-slate-900 text-slate-200 rounded-lg p-3 overflow-x-auto">
          {JSON.stringify(contract.schema, null, 2)}
        </pre>
      </div>

      {/* Explanation Toggle */}
      <div className="px-4 pb-3">
        <button
          onClick={() => setShowExplanation(!showExplanation)}
          className={`flex items-center gap-1 text-sm ${colors.text} hover:underline`}
        >
          {showExplanation ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          {showExplanation ? 'Hide' : 'Show'} Explanation
        </button>

        {showExplanation && (
          <div className={`mt-3 p-3 rounded-lg ${colors.bg} space-y-2`}>
            {contract.explanation.map((item, idx) => (
              <div key={idx} className="text-sm">
                <code className={`${colors.badge} ${colors.text} px-1.5 py-0.5 rounded text-xs font-mono`}>
                  {item.field}
                </code>
                <span className="text-gray-600 ml-2">→ {item.desc}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default function AgentContracts() {
  return (
    <div className="agent-contracts">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {contractsData.map((contract) => (
          <ContractCard key={contract.name} contract={contract} />
        ))}
      </div>
    </div>
  );
}
