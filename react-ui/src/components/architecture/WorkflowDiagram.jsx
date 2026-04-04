import { useState } from 'react';
import { FileText, Brain, Palette, Search, Wrench, CheckCircle, ArrowRight, ChevronRight } from 'lucide-react';

const workflowSteps = [
  {
    id: 'input',
    title: 'Input',
    subtitle: 'Raw long-form content',
    dataSchema: 'text/URL',
    icon: FileText,
    borderColor: 'border-gray-300',
    bgColor: 'bg-gray-50',
    hoverBg: 'hover:bg-gray-100',
    activeBorder: 'border-gray-500',
    textColor: 'text-gray-600',
    glowColor: 'shadow-gray-200',
  },
  {
    id: 'summarizer',
    title: 'Summarizer',
    subtitle: 'Extracts structured key points',
    dataSchema: 'SummarySchema',
    icon: Brain,
    borderColor: 'border-blue-300',
    bgColor: 'bg-blue-50',
    hoverBg: 'hover:bg-blue-100',
    activeBorder: 'border-blue-500',
    textColor: 'text-blue-600',
    glowColor: 'shadow-blue-200',
  },
  {
    id: 'formatter',
    title: 'Formatter',
    subtitle: 'Generates platform-specific content',
    dataSchema: 'FormattedSchema',
    icon: Palette,
    borderColor: 'border-purple-300',
    bgColor: 'bg-purple-50',
    hoverBg: 'hover:bg-purple-100',
    activeBorder: 'border-purple-500',
    textColor: 'text-purple-600',
    glowColor: 'shadow-purple-200',
  },
  {
    id: 'reviewer',
    title: 'Reviewer',
    subtitle: 'Evaluates coverage, clarity, and consistency',
    dataSchema: 'ReviewSchema',
    icon: Search,
    borderColor: 'border-orange-300',
    bgColor: 'bg-orange-50',
    hoverBg: 'hover:bg-orange-100',
    activeBorder: 'border-orange-500',
    textColor: 'text-orange-600',
    glowColor: 'shadow-orange-200',
  },
  {
    id: 'refiner',
    title: 'Refiner',
    subtitle: 'Applies targeted fixes based on feedback',
    dataSchema: 'RefinedSchema',
    icon: Wrench,
    borderColor: 'border-green-300',
    bgColor: 'bg-green-50',
    hoverBg: 'hover:bg-green-100',
    activeBorder: 'border-green-500',
    textColor: 'text-green-600',
    glowColor: 'shadow-green-200',
  },
  {
    id: 'output',
    title: 'Output',
    subtitle: 'Refined, validated content',
    dataSchema: 'Multi-platform',
    icon: CheckCircle,
    borderColor: 'border-emerald-400',
    bgColor: 'bg-emerald-50',
    hoverBg: 'hover:bg-emerald-100',
    activeBorder: 'border-emerald-600',
    textColor: 'text-emerald-600',
    glowColor: 'shadow-emerald-200',
  },
];

export default function WorkflowDiagram() {
  const [hoveredStep, setHoveredStep] = useState(null);
  const [selectedStep, setSelectedStep] = useState(null);

  const handleStepClick = (stepId) => {
    setSelectedStep(selectedStep === stepId ? null : stepId);
  };

  return (
    <div className="workflow-diagram py-4">
      {/* Title Section */}
      <div className="text-center mb-6">
        <h3 className="text-xl font-bold text-gray-900 mb-2">Pipeline Flow</h3>
        <p className="text-sm text-gray-600">Click any step to learn more</p>
      </div>

      {/* Main workflow */}
      <div className="flex flex-wrap items-center justify-center gap-2 lg:gap-3">
        {workflowSteps.map((step, idx) => {
          const Icon = step.icon;
          const isHovered = hoveredStep === step.id;
          const isSelected = selectedStep === step.id;
          const isDimmed = (hoveredStep !== null || selectedStep !== null) && !isHovered && !isSelected;

          return (
            <div key={step.id} className="flex items-center gap-1 lg:gap-2">
              {/* Node */}
              <div
                onClick={() => handleStepClick(step.id)}
                className={`
                  workflow-node relative flex flex-col items-center justify-center
                  px-3 py-3 lg:px-4 lg:py-4 rounded-xl border-3 bg-white cursor-pointer
                  transition-all duration-300 ease-out min-w-[100px] lg:min-w-[120px]
                  ${isHovered || isSelected ? step.activeBorder : step.borderColor}
                  ${isHovered || isSelected ? `scale-110 shadow-2xl ${step.glowColor}` : 'shadow-md'}
                  ${isDimmed ? 'opacity-40 scale-95' : 'opacity-100'}
                  ${step.hoverBg}
                `}
                style={{
                  borderWidth: isHovered || isSelected ? '3px' : '2px'
                }}
                onMouseEnter={() => setHoveredStep(step.id)}
                onMouseLeave={() => setHoveredStep(null)}
              >
                {/* Icon badge */}
                <div className={`p-2 rounded-xl ${step.bgColor} mb-2 transition-transform duration-300 ${isHovered ? 'scale-125' : ''}`}>
                  <Icon className={`w-5 h-5 ${step.textColor}`} />
                </div>
                
                {/* Title */}
                <span className={`font-bold text-sm ${step.textColor} text-center leading-tight`}>
                  {step.title}
                </span>
                
                {/* Data schema label */}
                <div className={`
                  mt-1.5 px-2 py-0.5 rounded-full text-xs font-mono
                  ${step.bgColor} ${step.textColor}
                  transition-all duration-300
                  ${isHovered || isSelected ? 'opacity-100 font-semibold' : 'opacity-80'}
                `}>
                  ↓ {step.dataSchema}
                </div>

                {/* Selection indicator */}
                {isSelected && (
                  <div className={`absolute -bottom-1 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full ${step.textColor.replace('text', 'bg')}`} />
                )}
              </div>
              
              {/* Animated arrow connector */}
              {idx < workflowSteps.length - 1 && (
                <div className={`
                  hidden sm:flex items-center justify-center w-6 lg:w-8
                  transition-all duration-300
                  ${isDimmed ? 'opacity-30' : 'opacity-100'}
                `}>
                  <ChevronRight 
                    className={`
                      w-5 h-5 text-gray-500 
                      transition-transform duration-300
                      ${isHovered && idx === workflowSteps.findIndex(s => s.id === hoveredStep) ? 'translate-x-1 text-gray-700 scale-125' : ''}
                    `} 
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>
      
      {/* Feedback loop indicator - Enhanced */}
      <div className="flex justify-center mt-6">
        <div className="relative flex flex-col items-center gap-2 bg-gradient-to-br from-orange-50 via-yellow-50 to-green-50 border-2 border-orange-300 px-5 py-3 rounded-2xl shadow-lg">
          {/* Title */}
          <div className="flex items-center gap-2">
            <span className="text-orange-500 text-xl animate-spin-slow">🔁</span>
            <span className="font-bold text-gray-800 text-sm">Feedback Loop</span>
          </div>
          
          {/* Flow */}
          <div className="flex items-center gap-2">
            <div className="px-3 py-1.5 bg-green-100 border-2 border-green-400 rounded-lg">
              <span className="font-bold text-green-700 text-sm">Refiner</span>
            </div>
            <div className="flex items-center gap-1">
              <ArrowRight className="w-4 h-4 text-gray-600" />
              <ArrowRight className="w-4 h-4 text-gray-600 -ml-2" />
            </div>
            <div className="px-3 py-1.5 bg-orange-100 border-2 border-orange-400 rounded-lg">
              <span className="font-bold text-orange-700 text-sm">Reviewer</span>
            </div>
          </div>
          
          {/* Detail */}
          <div className="text-xs text-gray-600 font-medium text-center">
            Reviewer identifies structured issues → Refiner applies targeted fixes → repeated until no critical issues remain
          </div>
        </div>
      </div>

      {/* Step detail tooltip (when selected) */}
      {selectedStep && (
        <div className="mt-4 p-4 bg-white border-2 border-gray-300 rounded-xl shadow-xl max-w-lg mx-auto animate-fadeIn">
          <div className="flex items-center gap-3 mb-2">
            {(() => {
              const step = workflowSteps.find(s => s.id === selectedStep);
              const Icon = step?.icon;
              return Icon && (
                <div className={`p-2 rounded-lg ${step.bgColor}`}>
                  <Icon className={`w-5 h-5 ${step.textColor}`} />
                </div>
              );
            })()}
            <h4 className="font-bold text-lg text-gray-900">
              {workflowSteps.find(s => s.id === selectedStep)?.title}
            </h4>
          </div>
          <p className="text-sm text-gray-700 leading-relaxed">
            {selectedStep === 'input' && 'Raw long-form content enters the pipeline. Supports text and URL inputs.'}
            {selectedStep === 'summarizer' && 'Extracts structured key points that serve as the single source of truth for downstream agents.'}
            {selectedStep === 'formatter' && 'Generates platform-specific outputs from the same underlying key points.'}
            {selectedStep === 'reviewer' && 'Compares generated content against key points to detect missing ideas, weak clarity, and inconsistencies.'}
            {selectedStep === 'refiner' && 'Improves content strictly based on reviewer feedback without introducing new ideas.'}
            {selectedStep === 'output' && 'Refined, validated content with full audit trail of changes and addressed issues.'}
          </p>
        </div>
      )}
    </div>
  );
}
