import { useState } from 'react';
import { ArrowDown, FileText, Brain, Palette, Search, Wrench, CheckCircle, ChevronDown, ChevronRight } from 'lucide-react';

const exampleSteps = [
  {
    stage: 'input',
    title: 'Raw Input',
    icon: FileText,
    color: 'gray',
    bgColor: 'bg-gray-50',
    borderColor: 'border-gray-300',
    textColor: 'text-gray-700',
    iconBg: 'bg-gray-100',
    content: '"Startups often prioritize rapid growth over sustainable practices. This growth-first mindset can lead to scaling problems, technical debt, and burnout..."',
    meta: '450 words',
    detail: 'Long-form article about startup growth challenges',
  },
  {
    stage: 'summarizer',
    title: 'Summarizer Output',
    icon: Brain,
    color: 'blue',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-300',
    textColor: 'text-blue-700',
    iconBg: 'bg-blue-100',
    content: 'key_points[kp_1] → "growth-first mindset" → "prioritizes acquisition over sustainability" → "can hide inefficiencies"',
    meta: '6 semantic key points',
    detail: 'Content DNA: intent=educational, tone=analytical, structure=problem-solution',
  },
  {
    stage: 'formatter',
    title: 'Formatter Output',
    icon: Palette,
    color: 'purple',
    bgColor: 'bg-purple-50',
    borderColor: 'border-purple-300',
    textColor: 'text-purple-700',
    iconBg: 'bg-purple-100',
    content: 'tweet_1 → "🚀 The startup trap: Growing fast feels great—until it doesn\'t..." | derived_from: ["kp_1"]',
    meta: 'LinkedIn + 6 tweets + Newsletter',
    detail: 'All content traced to source key_points via derived_from arrays',
  },
  {
    stage: 'reviewer',
    title: 'Reviewer Output',
    icon: Search,
    color: 'orange',
    bgColor: 'bg-orange-50',
    borderColor: 'border-orange-300',
    textColor: 'text-orange-700',
    iconBg: 'bg-orange-100',
    content: 'issue_1: { type: "missing_coverage", severity: "high", target: "twitter", related_key_point: "kp_3" }',
    meta: 'Score: 78% | 2 issues',
    detail: 'Deterministic coverage: 4/6 key_points used (67%)',
  },
  {
    stage: 'refiner',
    title: 'Refiner Output',
    icon: Wrench,
    color: 'green',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-300',
    textColor: 'text-green-700',
    iconBg: 'bg-green-100',
    content: 'change_1: { action: "add", target: "tweet_4", issue_id: "issue_1", related_key_point: "kp_3" }',
    meta: 'Added kp_3 to thread',
    detail: 'Surgical fix: Only addressed flagged issues, no full rewrite',
  },
  {
    stage: 'output',
    title: 'Final Output (v2)',
    icon: CheckCircle,
    color: 'emerald',
    bgColor: 'bg-emerald-50',
    borderColor: 'border-emerald-300',
    textColor: 'text-emerald-700',
    iconBg: 'bg-emerald-100',
    content: 'v2: LinkedIn post + 7-tweet thread + Newsletter | All key points covered | Score: 92%',
    meta: 'Threshold met ✓',
    detail: 'Full audit trail: 2 issues addressed, 4 changes applied',
  },
];

export default function ExampleFlow() {
  const [expandedStep, setExpandedStep] = useState(null);
  const [hoveredStep, setHoveredStep] = useState(null);

  const toggleStep = (stage) => {
    setExpandedStep(expandedStep === stage ? null : stage);
  };

  return (
    <div className="example-flow">
      {/* Timeline container */}
      <div className="relative">
        {/* Vertical timeline line */}
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-gray-300 via-purple-300 to-emerald-400 rounded-full hidden md:block" />

        <div className="flex flex-col gap-4">
          {exampleSteps.map((step, idx) => {
            const Icon = step.icon;
            const isExpanded = expandedStep === step.stage;
            const isHovered = hoveredStep === step.stage;

            return (
              <div key={step.stage} className="relative">
                {/* Step card */}
                <div
                  onClick={() => toggleStep(step.stage)}
                  onMouseEnter={() => setHoveredStep(step.stage)}
                  onMouseLeave={() => setHoveredStep(null)}
                  className={`
                    example-step relative ml-0 md:ml-12 p-4 rounded-xl border-2 
                    transition-all duration-300 cursor-pointer
                    ${step.bgColor} ${step.borderColor}
                    ${isHovered || isExpanded ? 'shadow-lg scale-[1.01]' : 'shadow-sm'}
                    hover:shadow-md
                  `}
                >
                  {/* Timeline dot (desktop) */}
                  <div className={`
                    hidden md:flex absolute -left-12 top-4 w-6 h-6 rounded-full 
                    items-center justify-center border-2 bg-white z-10
                    transition-all duration-300
                    ${step.borderColor}
                    ${isHovered || isExpanded ? 'scale-125 shadow-md' : ''}
                  `}>
                    <div className={`w-2.5 h-2.5 rounded-full ${step.textColor.replace('text', 'bg')}`} />
                  </div>

                  <div className="flex items-start gap-4">
                    {/* Icon */}
                    <div className={`p-2.5 rounded-xl ${step.iconBg} shadow-sm flex-shrink-0 transition-transform duration-300 ${isHovered ? 'scale-110' : ''}`}>
                      <Icon className={`w-5 h-5 ${step.textColor}`} />
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      {/* Header */}
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <h4 className={`font-semibold ${step.textColor}`}>{step.title}</h4>
                          <span className="text-xs text-gray-500 bg-white px-2 py-0.5 rounded-full shadow-sm">
                            {step.meta}
                          </span>
                        </div>
                        {isExpanded ? (
                          <ChevronDown className="w-4 h-4 text-gray-400" />
                        ) : (
                          <ChevronRight className="w-4 h-4 text-gray-400" />
                        )}
                      </div>
                      
                      {/* Main content */}
                      <code className="text-sm text-gray-700 font-mono leading-relaxed block">
                        {step.content}
                      </code>

                      {/* Expanded details */}
                      {isExpanded && (
                        <div className="mt-3 pt-3 border-t border-gray-200/50 animate-fadeIn">
                          <p className="text-sm text-gray-600 italic">
                            {step.detail}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Stage indicator bar */}
                  <div className={`
                    absolute left-0 top-0 bottom-0 w-1 rounded-l-xl
                    ${step.textColor.replace('text', 'bg')}
                  `} />
                </div>

                {/* Connector arrow (between cards) */}
                {idx < exampleSteps.length - 1 && (
                  <div className="flex justify-center py-2 md:ml-12">
                    <div className="flex items-center gap-2">
                      <ArrowDown className={`w-4 h-4 transition-colors duration-300 ${isHovered ? 'text-gray-600' : 'text-gray-400'}`} />
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Summary footer */}
      <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 via-purple-50 to-green-50 rounded-xl border border-gray-200 text-center">
        <p className="text-sm text-gray-600">
          <span className="font-semibold">End-to-end pipeline:</span> Raw content → Semantic analysis → Multi-platform generation → Quality evaluation → Targeted refinement
        </p>
      </div>
    </div>
  );
}
