import { useState } from 'react';
import { Database, Calculator, Link2, RefreshCw, Globe, ChevronRight } from 'lucide-react';

const principles = [
  {
    icon: Database,
    title: 'Structured Data Flow',
    description: 'No raw text passing between agents. All agents use strict JSON schemas for deterministic data flow.',
    details: 'Every agent input/output is a typed Pydantic model ensuring compile-time safety.',
    color: 'blue',
  },
  {
    icon: Calculator,
    title: 'Deterministic Evaluation',
    description: 'Review scores computed via rule-based checks + LLM analysis. Coverage = used_kps / total_kps.',
    details: 'Scoring formula: clarity × 0.2 + engagement × 0.2 + coverage × 0.25 + consistency × 0.15 + platform_fit × 0.2',
    color: 'purple',
  },
  {
    icon: Link2,
    title: 'Full Traceability',
    description: 'Every piece of content traces back to source key_points using semantic IDs (kp_1, kp_2).',
    details: 'derived_from arrays link tweets, paragraphs, and sections to their source concepts.',
    color: 'orange',
  },
  {
    icon: RefreshCw,
    title: 'Iterative Improvement',
    description: 'Feedback loop refines content until quality threshold (0.90) or max iterations reached.',
    details: 'System forces at least one iteration to demonstrate improvement cycle.',
    color: 'green',
  },
  {
    icon: Globe,
    title: 'Platform-Aware Generation',
    description: 'Hard constraints per platform: tweets ≤280 chars, LinkedIn hooks required, newsletter 3-5 sections.',
    details: 'Violations are caught deterministically before review to ensure compliance.',
    color: 'indigo',
  },
];

const colorClasses = {
  blue: {
    bg: 'bg-blue-50',
    bgHover: 'hover:bg-blue-100',
    border: 'border-blue-200',
    borderHover: 'hover:border-blue-400',
    icon: 'text-blue-600',
    iconBg: 'bg-blue-100',
    title: 'text-blue-700',
    glow: 'hover:shadow-blue-100',
  },
  purple: {
    bg: 'bg-purple-50',
    bgHover: 'hover:bg-purple-100',
    border: 'border-purple-200',
    borderHover: 'hover:border-purple-400',
    icon: 'text-purple-600',
    iconBg: 'bg-purple-100',
    title: 'text-purple-700',
    glow: 'hover:shadow-purple-100',
  },
  orange: {
    bg: 'bg-orange-50',
    bgHover: 'hover:bg-orange-100',
    border: 'border-orange-200',
    borderHover: 'hover:border-orange-400',
    icon: 'text-orange-600',
    iconBg: 'bg-orange-100',
    title: 'text-orange-700',
    glow: 'hover:shadow-orange-100',
  },
  green: {
    bg: 'bg-green-50',
    bgHover: 'hover:bg-green-100',
    border: 'border-green-200',
    borderHover: 'hover:border-green-400',
    icon: 'text-green-600',
    iconBg: 'bg-green-100',
    title: 'text-green-700',
    glow: 'hover:shadow-green-100',
  },
  indigo: {
    bg: 'bg-indigo-50',
    bgHover: 'hover:bg-indigo-100',
    border: 'border-indigo-200',
    borderHover: 'hover:border-indigo-400',
    icon: 'text-indigo-600',
    iconBg: 'bg-indigo-100',
    title: 'text-indigo-700',
    glow: 'hover:shadow-indigo-100',
  },
};

export default function SystemPrinciples() {
  const [expandedPrinciple, setExpandedPrinciple] = useState(null);

  const togglePrinciple = (idx) => {
    setExpandedPrinciple(expandedPrinciple === idx ? null : idx);
  };

  return (
    <div className="system-principles">
      <h2 className="text-2xl font-bold text-gray-900 mb-3">Design Principles</h2>
      <p className="text-base text-gray-600 mb-6">Core architectural decisions that drive reliability and quality</p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {principles.map((principle, idx) => {
          const Icon = principle.icon;
          const colors = colorClasses[principle.color];
          const isExpanded = expandedPrinciple === idx;
          
          return (
            <div
              key={idx}
              onClick={() => togglePrinciple(idx)}
              className={`
                group relative flex flex-col p-5 rounded-xl border-2 cursor-pointer
                ${colors.bg} ${colors.border} ${colors.bgHover} ${colors.borderHover}
                hover:shadow-lg ${colors.glow}
                transition-all duration-300
                ${isExpanded ? 'ring-2 ring-offset-2 ring-opacity-50 scale-102' : ''}
              `}
              style={{ 
                '--tw-ring-color': isExpanded ? `var(--${principle.color}-400)` : undefined 
              }}
            >
              {/* Header */}
              <div className="flex items-start gap-3">
                <div className={`p-2.5 rounded-lg ${colors.iconBg} shadow-sm flex-shrink-0 transition-transform duration-300 group-hover:scale-110`}>
                  <Icon className={`w-6 h-6 ${colors.icon}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <h4 className={`font-bold text-base ${colors.title}`}>
                      {principle.title}
                    </h4>
                    <ChevronRight className={`w-5 h-5 text-gray-500 transition-transform duration-300 ${isExpanded ? 'rotate-90' : ''}`} />
                  </div>
                  <p className="text-sm text-gray-700 mt-2 leading-relaxed">
                    {principle.description}
                  </p>
                </div>
              </div>

              {/* Expanded details */}
              <div className={`
                overflow-hidden transition-all duration-300
                ${isExpanded ? 'max-h-32 mt-4 pt-4 border-t-2 border-gray-300' : 'max-h-0'}
              `}>
                <p className="text-xs text-gray-600 italic leading-relaxed">
                  {principle.details}
                </p>
              </div>

              {/* Hover indicator */}
              <div className={`
                absolute bottom-0 left-0 right-0 h-1 rounded-b-xl
                transition-all duration-300
                ${colors.icon.replace('text', 'bg')}
                ${isExpanded ? 'opacity-100' : 'opacity-0 group-hover:opacity-60'}
              `} />
            </div>
          );
        })}
      </div>
    </div>
  );
}
