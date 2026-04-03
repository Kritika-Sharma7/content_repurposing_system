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
    <div className="workflow-diagram py-6">
      {/* Title Section */}
      <div className="text-center mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-2">Pipeline Flow</h3>
        <p className="text-sm text-gray-600">Click any step to learn more</p>
      </div>

      {/* Main workflow */}
      <div className="flex flex-wrap items-center justify-center gap-3 lg:gap-4">
        {workflowSteps.map((step, idx) => {
          const Icon = step.icon;
          const isHovered = hoveredStep === step.id;
          const isSelected = selectedStep === step.id;
          const isDimmed = (hoveredStep !== null || selectedStep !== null) && !isHovered && !isSelected;

          return (
            <div key={step.id} className="flex items-center gap-2 lg:gap-3">
              {/* Node */}
              <div
                onClick={() => handleStepClick(step.id)}
                className={`
                  workflow-node relative flex flex-col items-center justify-center
                  px-4 py-4 lg:px-5 lg:py-5 rounded-xl border-3 bg-white cursor-pointer
                  transition-all duration-300 ease-out min-w-[110px] lg:min-w-[140px]
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
                <div className={`p-2.5 rounded-xl ${step.bgColor} mb-3 transition-transform duration-300 ${isHovered ? 'scale-125' : ''}`}>
                  <Icon className={`w-6 h-6 ${step.textColor}`} />
                </div>
                
                {/* Title */}
                <span className={`font-bold text-base ${step.textColor}`}>
                  {step.title}
                </span>
                
                {/* Data schema label */}
                <div className={`
                  mt-2 px-2.5 py-1 rounded-full text-xs font-mono
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
                  hidden sm:flex items-center justify-center w-8 lg:w-10
                  transition-all duration-300
                  ${isDimmed ? 'opacity-30' : 'opacity-100'}
                `}>
                  <ChevronRight 
                    className={`
                      w-6 h-6 text-gray-500 
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
      <div className="flex justify-center mt-10">
        <div className="relative flex flex-col items-center gap-3 bg-gradient-to-br from-orange-50 via-yellow-50 to-green-50 border-2 border-orange-300 px-6 py-4 rounded-2xl shadow-lg">
          {/* Title */}
          <div className="flex items-center gap-2">
            <span className="text-orange-500 text-2xl animate-spin-slow">🔁</span>
            <span className="font-bold text-gray-800 text-base">Feedback Loop</span>
          </div>
          
          {/* Flow */}
          <div className="flex items-center gap-3">
            <div className="px-4 py-2 bg-orange-100 border-2 border-orange-400 rounded-xl">
              <span className="font-bold text-orange-700">Reviewer</span>
            </div>
            <div className="flex items-center gap-1">
              <ArrowRight className="w-5 h-5 text-gray-600" />
              <ArrowRight className="w-5 h-5 text-gray-600 -ml-3" />
            </div>
            <div className="px-4 py-2 bg-green-100 border-2 border-green-400 rounded-xl">
              <span className="font-bold text-green-700">Refiner</span>
            </div>
          </div>
          
          {/* Detail */}
          <div className="text-sm text-gray-600 font-medium">
            Iterates until <span className="font-bold text-orange-600">90% quality score</span>
          </div>
        </div>
      </div>

      {/* Step detail tooltip (when selected) */}
      {selectedStep && (
        <div className="mt-6 p-5 bg-white border-2 border-gray-300 rounded-xl shadow-xl max-w-lg mx-auto animate-fadeIn">
          <div className="flex items-center gap-3 mb-3">
            {(() => {
              const step = workflowSteps.find(s => s.id === selectedStep);
              const Icon = step?.icon;
              return Icon && (
                <div className={`p-2.5 rounded-lg ${step.bgColor}`}>
                  <Icon className={`w-6 h-6 ${step.textColor}`} />
                </div>
              );
            })()}
            <h4 className="font-bold text-lg text-gray-900">
              {workflowSteps.find(s => s.id === selectedStep)?.title}
            </h4>
          </div>
          <p className="text-sm text-gray-700 leading-relaxed">
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
