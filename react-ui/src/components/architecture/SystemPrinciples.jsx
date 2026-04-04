import { useState } from 'react';
import { Database, Calculator, Link2, RefreshCw, Globe, ChevronRight } from 'lucide-react';

const principles = [
  {
    icon: Database,
    title: 'Disciplined Workflow',
    description: 'Each agent has a single responsibility with no role overlap',
    details: 'Every agent input/output is a typed Pydantic model ensuring compile-time safety.',
    color: 'blue',
  },
  {
    icon: Calculator,
    title: '1:1 Issue Mapping',
    description: 'Every identified issue results in a specific, traceable fix',
    details: 'Each change links to specific issue_id for complete auditability.',
    color: 'purple',
  },
  {
    icon: Link2,
    title: 'Quality Gates',
    description: 'Reviewer enforces content quality before progression',
    details: 'System validates coverage, clarity, and consistency before allowing progression.',
    color: 'orange',
  },
  {
    icon: RefreshCw,
    title: 'Platform Awareness',
    description: 'Content is adapted per platform while preserving core ideas',
    details: 'Hard constraints per platform: tweets ≤280 chars, LinkedIn hooks required, newsletter 3-5 sections.',
    color: 'green',
  },
  {
    icon: Globe,
    title: 'Convergence Control',
    description: 'Refinement loop stops when no critical issues remain',
    details: 'System forces at least one iteration to demonstrate improvement cycle.',
    color: 'indigo',
  },
  {
    icon: ChevronRight,
    title: 'Full Traceability',
    description: 'Every output can be traced back to its source key points',
    details: 'derived_from arrays link tweets, paragraphs, and sections to their source concepts.',
    color: 'green',
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
      <div className="space-y-3">
        {principles.map((principle, idx) => {
          const Icon = principle.icon;
          const colors = colorClasses[principle.color];
          const isExpanded = expandedPrinciple === idx;
          
          return (
            <div
              key={idx}
              onClick={() => togglePrinciple(idx)}
              className={`
                group relative flex flex-col p-3 rounded-lg border cursor-pointer
                ${colors.bg} ${colors.border} ${colors.bgHover} ${colors.borderHover}
                hover:shadow-sm transition-all duration-300
                ${isExpanded ? 'ring-1 ring-offset-1 ring-opacity-50' : ''}
              `}
            >
              {/* Header */}
              <div className="flex items-center gap-2">
                <div className={`p-1.5 rounded ${colors.iconBg} flex-shrink-0`}>
                  <Icon className={`w-4 h-4 ${colors.icon}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className={`font-bold text-xs ${colors.title}`}>
                    {principle.title}
                  </h4>
                </div>
                <ChevronRight className={`w-3 h-3 text-gray-400 transition-transform duration-300 ${isExpanded ? 'rotate-90' : ''}`} />
              </div>
              
              {/* Description (always visible) */}
              <p className="text-xs text-gray-600 mt-1.5 leading-tight">
                {principle.description}
              </p>

              {/* Expanded details */}
              <div className={`
                overflow-hidden transition-all duration-300
                ${isExpanded ? 'max-h-20 mt-2 pt-2 border-t border-gray-300' : 'max-h-0'}
              `}>
                <p className="text-xs text-gray-500 italic leading-tight">
                  {principle.details}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
