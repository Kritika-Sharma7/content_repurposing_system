import { useState } from 'react';
import { RefreshCw, CheckCircle, ArrowDown, TrendingUp, AlertCircle, Sparkles } from 'lucide-react';

const iterations = [
  {
    iteration: 1,
    score: 0.78,
    scoreDisplay: '78%',
    status: 'has_issues',
    issues: 3,
    issueTypes: ['missing_coverage', 'tweet_length', 'weak_hook'],
    changes: 0,
    message: 'Coverage gap: kp_3 missing from thread, tweet_2 exceeds limit',
  },
  {
    iteration: 2,
    score: 0.88,
    scoreDisplay: '88%',
    status: 'improved',
    issues: 1,
    issueTypes: ['clarity'],
    changes: 4,
    message: 'Added missing content, fixed tweet lengths. Minor clarity issue.',
  },
  {
    iteration: 3,
    score: 0.92,
    scoreDisplay: '92%',
    status: 'no_critical_issues',
    issues: 0,
    issueTypes: [],
    changes: 2,
    message: 'No critical issues remain. All key_points covered.',
  },
];

export default function FeedbackLoopViz() {
  const [hoveredIteration, setHoveredIteration] = useState(null);
  const [expandedIteration, setExpandedIteration] = useState(null);
  const threshold = 0.90;

  const toggleExpand = (iterNum) => {
    setExpandedIteration(expandedIteration === iterNum ? null : iterNum);
  };

  return (
    <div className="feedback-loop-viz">
      {/* Loop header with animated icon */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <div className="relative">
            <RefreshCw className="w-5 h-5 text-orange-500 animate-spin-slow" />
            <div className="absolute inset-0 animate-ping opacity-30">
              <RefreshCw className="w-5 h-5 text-orange-500" />
            </div>
          </div>
          <span className="font-semibold text-gray-700">Iterative Feedback Loop</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="text-gray-500">Until:</span>
          <span className="font-bold text-green-600 bg-green-50 px-2 py-0.5 rounded-full border border-green-200">
            No Critical Issues
          </span>
        </div>
      </div>

      {/* Visual progress summary */}
      <div className="mb-6 p-3 bg-gradient-to-r from-orange-50 via-yellow-50 to-green-50 rounded-xl border border-gray-200">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-semibold text-gray-600 uppercase tracking-wide">Progress</span>
          <div className="flex items-center gap-3 text-sm">
            <span className="text-orange-600">78%</span>
            <span className="text-gray-400">→</span>
            <span className="text-yellow-600">88%</span>
            <span className="text-gray-400">→</span>
            <span className="text-green-600 font-bold">92%</span>
          </div>
        </div>
        <div className="relative h-3 bg-gray-200 rounded-full overflow-hidden">
          {/* Animated gradient fill */}
          <div 
            className="absolute inset-y-0 left-0 bg-gradient-to-r from-orange-400 via-yellow-400 to-green-500 rounded-full transition-all duration-1000"
            style={{ width: '92%' }}
          />
          {/* Final state marker */}
          <div 
            className="absolute top-0 bottom-0 w-0.5 bg-green-700 z-10"
            style={{ right: '8%' }}
          >
            <div className="absolute -top-5 left-1/2 -translate-x-1/2 text-xs text-green-700 font-semibold whitespace-nowrap">
              Complete
            </div>
          </div>
        </div>
      </div>

      {/* Iterations */}
      <div className="space-y-3">
        {iterations.map((it, idx) => {
          const isHovered = hoveredIteration === it.iteration;
          const isExpanded = expandedIteration === it.iteration;
          const isFinal = it.status === 'no_critical_issues';
          const progressColor = it.status === 'no_critical_issues' ? 'bg-green-500' : it.score >= 0.80 ? 'bg-yellow-500' : 'bg-orange-500';
          const borderColor = isFinal ? 'border-green-300' : it.score >= 0.80 ? 'border-yellow-200' : 'border-orange-200';
          const bgColor = isFinal ? 'bg-green-50' : it.score >= 0.80 ? 'bg-yellow-50' : 'bg-white';

          return (
            <div key={it.iteration}>
              {/* Iteration card */}
              <div
                onClick={() => toggleExpand(it.iteration)}
                className={`
                  iteration-card p-4 rounded-xl border-2 transition-all duration-300 cursor-pointer
                  ${borderColor} ${bgColor}
                  ${isHovered || isExpanded ? 'shadow-lg scale-[1.01]' : 'shadow-sm'}
                  hover:shadow-md
                `}
                onMouseEnter={() => setHoveredIteration(it.iteration)}
                onMouseLeave={() => setHoveredIteration(null)}
              >
                {/* Header row */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    {/* Iteration badge */}
                    <span className={`
                      w-9 h-9 rounded-full flex items-center justify-center text-sm font-bold shadow-sm
                      transition-transform duration-300
                      ${isFinal ? 'bg-green-500 text-white' : it.score >= 0.80 ? 'bg-yellow-400 text-yellow-900' : 'bg-orange-100 text-orange-600'}
                      ${isHovered ? 'scale-110' : ''}
                    `}>
                      {it.iteration}
                    </span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-gray-800">Iteration {it.iteration}</span>
                        {isFinal && (
                          <span className="flex items-center gap-1 text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full border border-green-200">
                            <Sparkles className="w-3 h-3" />
                            Final
                          </span>
                        )}
                        {it.changes > 0 && (
                          <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">
                            +{it.changes} changes
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  {/* Score display */}
                  <div className="flex items-center gap-2">
                    <span className={`text-2xl font-bold ${isFinal ? 'text-green-600' : it.score >= 0.80 ? 'text-yellow-600' : 'text-orange-600'}`}>
                      {it.scoreDisplay}
                    </span>
                    {isFinal && <CheckCircle className="w-6 h-6 text-green-500" />}
                    {!isFinal && it.issues > 0 && <AlertCircle className="w-5 h-5 text-orange-400" />}
                  </div>
                </div>

                {/* Progress bar */}
                <div className="mb-3">
                  <div className="h-2.5 bg-gray-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${progressColor} rounded-full transition-all duration-700 ease-out`}
                      style={{ width: `${it.score * 100}%` }}
                    />
                  </div>
                </div>

                {/* Status message */}
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">{it.message}</span>
                  {it.issues > 0 && (
                    <span className="px-2 py-0.5 bg-orange-100 text-orange-700 rounded-full text-xs font-medium">
                      {it.issues} issue{it.issues > 1 ? 's' : ''}
                    </span>
                  )}
                </div>

                {/* Expanded details */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-gray-200 animate-fadeIn">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-semibold text-gray-700">Issues Found:</span>
                        <div className="mt-1 flex flex-wrap gap-1">
                          {it.issueTypes.length > 0 ? it.issueTypes.map((type, i) => (
                            <span key={i} className="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs">
                              {type.replace('_', ' ')}
                            </span>
                          )) : (
                            <span className="text-green-600 text-xs">No issues</span>
                          )}
                        </div>
                      </div>
                      <div>
                        <span className="font-semibold text-gray-700">Changes Applied:</span>
                        <p className="text-gray-600 text-xs mt-1">
                          {it.changes > 0 ? `${it.changes} targeted modifications` : 'Initial version'}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Connector between iterations */}
              {idx < iterations.length - 1 && (
                <div className="flex justify-center py-2">
                  <div className="flex flex-col items-center">
                    <ArrowDown className="w-4 h-4 text-gray-400" />
                    <span className="text-xs text-gray-400 mt-0.5 bg-white px-2 rounded">refine</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Summary card */}
      <div className="mt-6 p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border border-green-200">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-green-100 rounded-lg">
            <TrendingUp className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <span className="font-semibold text-green-700">Quality improved by 14 points</span>
            <p className="text-gray-600 text-sm">78% → 92% across 3 iterations with 6 targeted changes</p>
          </div>
        </div>
      </div>

      {/* Algorithm code (collapsible) */}
      <details className="mt-4">
        <summary className="text-sm text-gray-500 cursor-pointer hover:text-gray-700">
          View algorithm
        </summary>
        <pre className="mt-2 text-xs bg-slate-900 text-slate-200 rounded-lg p-3 overflow-x-auto">
{`while has_critical_issues(review) and iteration < max_iterations:
    review = reviewer.run(summary, formatted)
    if has_critical_issues(review):
        refined = refiner.run(summary, formatted, review)
        formatted = refined
    iteration += 1`}
        </pre>
      </details>
    </div>
  );
}
