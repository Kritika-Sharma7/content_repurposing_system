import { useState } from 'react';
import { ArrowDown, Lightbulb, FileText, AlertTriangle, Wrench, MousePointer } from 'lucide-react';

const traceabilityChain = [
  {
    id: 'kp_1',
    stage: 'source',
    label: 'Key Point',
    nodeId: 'kp_1',
    content: 'async-first communication → reduces meetings by 60%',
    detail: 'Semantic unit extracted from source content',
    icon: Lightbulb,
    color: 'blue',
    borderColor: 'border-blue-400',
    bgColor: 'bg-blue-50',
    textColor: 'text-blue-700',
    ringColor: 'ring-blue-400',
    agent: 'Summarizer',
  },
  {
    id: 'linkedin',
    stage: 'formatter',
    label: 'LinkedIn Body',
    nodeId: 'linkedin_body',
    content: '"Async-first communication cut our meetings by 60% and unlocked deep work..."',
    detail: 'derived_from: ["kp_1"]',
    icon: FileText,
    color: 'purple',
    borderColor: 'border-purple-400',
    bgColor: 'bg-purple-50',
    textColor: 'text-purple-700',
    ringColor: 'ring-purple-400',
    agent: 'Formatter',
  },
  {
    id: 'issue_1',
    stage: 'reviewer',
    label: 'Reviewer Issue',
    nodeId: 'issue_1',
    content: 'Missing coverage: key_point kp_2 not represented in thread',
    detail: 'type: "missing_coverage", severity: "high"',
    icon: AlertTriangle,
    color: 'orange',
    borderColor: 'border-orange-400',
    bgColor: 'bg-orange-50',
    textColor: 'text-orange-700',
    ringColor: 'ring-orange-400',
    agent: 'Reviewer',
  },
  {
    id: 'change_1',
    stage: 'refiner',
    label: 'Refiner Change',
    nodeId: 'change_1',
    content: 'Added tweet_4 covering kp_2: documentation practices',
    detail: 'action: "add", target: "twitter_thread[3]", issue_id: "issue_1"',
    icon: Wrench,
    color: 'green',
    borderColor: 'border-green-400',
    bgColor: 'bg-green-50',
    textColor: 'text-green-700',
    ringColor: 'ring-green-400',
    agent: 'Refiner',
  },
];

export default function TraceabilityFlow() {
  const [selectedNode, setSelectedNode] = useState(null);
  const [hoveredNode, setHoveredNode] = useState(null);

  const handleNodeClick = (nodeId) => {
    setSelectedNode(selectedNode === nodeId ? null : nodeId);
  };

  // When a node is selected, we highlight the entire chain to show flow
  const getNodeState = (nodeId) => {
    if (selectedNode === null && hoveredNode === null) return 'normal';
    if (selectedNode === nodeId || hoveredNode === nodeId) return 'active';
    if (selectedNode !== null) return 'chain'; // Part of chain when something is selected
    return 'dimmed';
  };

  return (
    <div className="traceability-flow">
      {/* Interactive hint */}
      <div className="flex items-center justify-center gap-2 mb-4 text-xs text-gray-500">
        <MousePointer className="w-3 h-3" />
        <span>Click any node to see full traceability chain</span>
      </div>

      <div className="flex flex-col items-center gap-2">
        {traceabilityChain.map((node, idx) => {
          const Icon = node.icon;
          const nodeState = getNodeState(node.id);
          const isActive = nodeState === 'active';
          const isDimmed = nodeState === 'dimmed';
          const isChain = nodeState === 'chain';

          return (
            <div key={node.id} className="flex flex-col items-center w-full">
              {/* Node */}
              <div
                onClick={() => handleNodeClick(node.id)}
                onMouseEnter={() => setHoveredNode(node.id)}
                onMouseLeave={() => setHoveredNode(null)}
                className={`
                  traceability-node w-full max-w-md cursor-pointer
                  flex items-start gap-3 p-4 rounded-xl border-2
                  transition-all duration-300 ease-out
                  ${node.borderColor} ${node.bgColor}
                  ${isActive ? `ring-2 ring-offset-2 ${node.ringColor} shadow-lg scale-[1.02]` : ''}
                  ${isChain ? 'opacity-90 shadow-md' : ''}
                  ${isDimmed ? 'opacity-30 scale-95' : ''}
                  ${!isActive && !isDimmed ? 'hover:shadow-md hover:scale-[1.01]' : ''}
                `}
              >
                {/* Left color bar indicator */}
                <div className={`absolute left-0 top-0 bottom-0 w-1 rounded-l-xl ${node.textColor.replace('text', 'bg')}`} />
                
                {/* Icon */}
                <div className={`p-2 rounded-lg bg-white shadow-sm flex-shrink-0 transition-transform duration-300 ${isActive ? 'scale-110' : ''}`}>
                  <Icon className={`w-5 h-5 ${node.textColor}`} />
                </div>
                
                {/* Content */}
                <div className="flex-1 min-w-0 pl-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`font-semibold text-sm ${node.textColor}`}>
                      {node.label}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full bg-white ${node.textColor} font-mono shadow-sm`}>
                      {node.nodeId}
                    </span>
                  </div>
                  
                  {/* Main content */}
                  <p className="text-sm text-gray-700 mb-1">
                    {node.content}
                  </p>
                  
                  {/* Technical detail */}
                  <code className="text-xs text-gray-500 font-mono block">
                    {node.detail}
                  </code>

                  {/* Agent badge */}
                  <div className={`mt-2 inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs ${node.bgColor} ${node.textColor} border ${node.borderColor}`}>
                    {node.agent}
                  </div>
                </div>
              </div>

              {/* Animated connector arrow */}
              {idx < traceabilityChain.length - 1 && (
                <div className={`
                  py-1 flex flex-col items-center
                  transition-all duration-300 
                  ${isDimmed ? 'opacity-20' : 'opacity-100'}
                `}>
                  <div className={`
                    w-0.5 h-3 rounded-full
                    ${isActive || isChain ? 'bg-gray-400' : 'bg-gray-300'}
                    transition-colors duration-300
                  `} />
                  <ArrowDown className={`
                    w-4 h-4 
                    ${isActive || isChain ? 'text-gray-500' : 'text-gray-400'}
                    transition-colors duration-300
                  `} />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Legend */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="flex flex-wrap justify-center gap-4 text-xs">
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full bg-blue-400"></div>
            <span className="text-gray-600">Source (Summarizer)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full bg-purple-400"></div>
            <span className="text-gray-600">Transformation (Formatter)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full bg-orange-400"></div>
            <span className="text-gray-600">Evaluation (Reviewer)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full bg-green-400"></div>
            <span className="text-gray-600">Iteration (Refiner)</span>
          </div>
        </div>
      </div>

      {/* Selected node detail panel */}
      {selectedNode && (
        <div className="mt-4 p-3 bg-gradient-to-r from-gray-50 to-white rounded-lg border border-gray-200 text-center animate-fadeIn">
          <p className="text-sm text-gray-600">
            <span className="font-semibold">Traceability:</span> Every downstream change can be traced back to source key_points
          </p>
        </div>
      )}
    </div>
  );
}
