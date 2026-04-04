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
    role: 'Extracts structured key points that serve as the single source of truth for downstream agents',
    input: '{ raw_text: string }',
    output: 'Structured key_points array (ground truth)',
    keyFeature: 'Identifies and structures key ideas',
  },
  {
    name: 'Formatter',
    icon: Palette,
    color: 'purple',
    borderColor: 'border-purple-300',
    bgColor: 'bg-purple-50',
    textColor: 'text-purple-700',
    iconBg: 'bg-purple-100',
    role: 'Generates platform-specific outputs from the same underlying key points',
    input: 'SummaryOutput + UserPreferences',
    output: 'LinkedIn, Twitter, Newsletter variants',
    keyFeature: 'Transforms key points into format-specific content',
  },
  {
    name: 'Reviewer',
    icon: Search,
    color: 'orange',
    borderColor: 'border-orange-300',
    bgColor: 'bg-orange-50',
    textColor: 'text-orange-700',
    iconBg: 'bg-orange-100',
    role: 'Compares generated content against key points to detect missing ideas, weak clarity, and inconsistencies',
    input: 'SummaryOutput + FormattedOutput',
    output: 'Structured issues list (no rewriting)',
    keyFeature: 'Identifies coverage, clarity, and consistency issues',
  },
  {
    name: 'Refiner',
    icon: Wrench,
    color: 'green',
    borderColor: 'border-green-300',
    bgColor: 'bg-green-50',
    textColor: 'text-green-700',
    iconBg: 'bg-green-100',
    role: 'Improves content strictly based on reviewer feedback without introducing new ideas',
    input: 'SummaryOutput + FormattedOutput + ReviewOutput',
    output: 'Updated content + change log (versioned)',
    keyFeature: 'Maps each issue to a targeted fix',
  },
];

export default function AgentCards() {
  return (
    <div className="agent-cards max-w-5xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {agents.map((agent) => {
          const Icon = agent.icon;

          return (
            <div
              key={agent.name}
              className={`
                agent-card-enhanced rounded-xl border-2 p-4
                ${agent.borderColor} bg-white
                hover:shadow-lg transition-all duration-300
                hover:scale-[1.02] h-full
              `}
            >
              {/* Header */}
              <div className="flex items-start gap-3 mb-4">
                <div className={`p-2.5 rounded-xl ${agent.iconBg} shadow-sm`}>
                  <Icon className={`w-6 h-6 ${agent.textColor}`} />
                </div>
                <div className="flex-1">
                  <h3 className={`font-bold text-lg ${agent.textColor} mb-1`}>{agent.name}</h3>
                  <p className="text-sm text-gray-700 leading-snug">{agent.role}</p>
                </div>
              </div>

              {/* I/O */}
              <div className="space-y-3">
                <div>
                  <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Process</span>
                  <div className={`text-xs mt-1 p-2.5 rounded-lg ${agent.bgColor} ${agent.textColor} font-medium leading-relaxed`}>
                    {agent.keyFeature}
                  </div>
                </div>
                <div>
                  <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Output</span>
                  <div className={`text-xs mt-1 p-2.5 rounded-lg ${agent.bgColor} ${agent.textColor} font-mono leading-relaxed`}>
                    {agent.output}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
