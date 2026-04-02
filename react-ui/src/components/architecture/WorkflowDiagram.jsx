import { useState } from 'react';
import { FileText, Brain, Palette, Search, Wrench, CheckCircle, ArrowRight, ChevronRight } from 'lucide-react';

const workflowSteps = [
  {
    id: 'input',
    title: 'Raw Input',
    subtitle: 'Long-form content',
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
    subtitle: 'Content DNA',
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
    subtitle: 'Multi-platform',
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
    subtitle: 'Quality eval',
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
    subtitle: 'Targeted fixes',
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
    title: 'Final Output',
    subtitle: 'Versioned content',
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
                  px-3 py-3 lg:px-4 lg:py-4 rounded-xl border-2 bg-white cursor-pointer
                  transition-all duration-300 ease-out min-w-[100px] lg:min-w-[120px]
                  ${isHovered || isSelected ? step.activeBorder : step.borderColor}
                  ${isHovered || isSelected ? `scale-105 shadow-lg ${step.glowColor}` : 'shadow-sm'}
                  ${isDimmed ? 'opacity-40 scale-95' : 'opacity-100'}
                  ${step.hoverBg}
                `}
                onMouseEnter={() => setHoveredStep(step.id)}
                onMouseLeave={() => setHoveredStep(null)}
              >
                {/* Icon badge */}
                <div className={`p-2 rounded-lg ${step.bgColor} mb-2 transition-transform duration-300 ${isHovered ? 'scale-110' : ''}`}>
                  <Icon className={`w-5 h-5 ${step.textColor}`} />
                </div>
                
                {/* Title */}
                <span className={`font-semibold text-sm ${step.textColor}`}>
                  {step.title}
                </span>
                
                {/* Data schema label */}
                <div className={`
                  mt-1.5 px-2 py-0.5 rounded-full text-xs font-mono
                  ${step.bgColor} ${step.textColor}
                  transition-all duration-300
                  ${isHovered || isSelected ? 'opacity-100' : 'opacity-70'}
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
                      w-5 h-5 text-gray-400 
                      transition-transform duration-300
                      ${isHovered && idx === workflowSteps.findIndex(s => s.id === hoveredStep) ? 'translate-x-1 text-gray-600' : ''}
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
        <div className="relative flex items-center gap-3 text-sm bg-gradient-to-r from-orange-50 via-yellow-50 to-green-50 border border-orange-200/60 px-5 py-3 rounded-2xl shadow-sm">
          {/* Animated loop icon */}
          <div className="relative">
            <span className="text-orange-500 text-xl animate-spin-slow">↻</span>
          </div>
          
          <div className="flex items-center gap-2">
            <span className="text-gray-600">Feedback loop:</span>
            <span className="font-semibold text-orange-600 bg-orange-100 px-2 py-0.5 rounded">Reviewer</span>
            <ArrowRight className="w-4 h-4 text-gray-400" />
            <span className="font-semibold text-green-600 bg-green-100 px-2 py-0.5 rounded">Refiner</span>
            <span className="text-gray-500 text-xs ml-1">until 90% score</span>
          </div>
        </div>
      </div>

      {/* Step detail tooltip (when selected) */}
      {selectedStep && (
        <div className="mt-4 p-4 bg-white border border-gray-200 rounded-xl shadow-md max-w-md mx-auto animate-fadeIn">
          <div className="flex items-center gap-2 mb-2">
            {(() => {
              const step = workflowSteps.find(s => s.id === selectedStep);
              const Icon = step?.icon;
              return Icon && <Icon className={`w-5 h-5 ${step.textColor}`} />;
            })()}
            <h4 className="font-semibold text-gray-800">
              {workflowSteps.find(s => s.id === selectedStep)?.title}
            </h4>
          </div>
          <p className="text-sm text-gray-600">
            {selectedStep === 'input' && 'Long-form content enters the pipeline. Supports text and URL inputs.'}
            {selectedStep === 'summarizer' && 'Extracts Content DNA: semantic key_points (kp_1, kp_2) with concept, claim, and implication.'}
            {selectedStep === 'formatter' && 'Transforms summary into LinkedIn, Twitter, and Newsletter formats with derived_from traceability.'}
            {selectedStep === 'reviewer' && 'Multi-dimensional evaluation: coverage, clarity, engagement, consistency. Produces structured issues.'}
            {selectedStep === 'refiner' && 'Makes targeted surgical fixes based on review issues. No full rewrites, only tracked changes.'}
            {selectedStep === 'output' && 'Final versioned content with full audit trail of changes and addressed issues.'}
          </p>
        </div>
      )}
    </div>
  );
}
