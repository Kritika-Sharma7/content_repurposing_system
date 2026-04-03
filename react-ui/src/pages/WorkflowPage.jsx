import { useState } from "react";
import StepWizard from "../components/workflow/StepWizard";
import InputStep from "../components/workflow/InputStep";
import PreferencesStep from "../components/workflow/PreferencesStep";  
import SummarizerStep from "../components/workflow/SummarizerStep";
import FormatterStep from "../components/workflow/FormatterStep";
import ReviewerStep from "../components/workflow/ReviewerStep";
import ResultsStep from "../components/workflow/ResultsStep";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export default function WorkflowPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [workflowData, setWorkflowData] = useState({
    inputText: "",
    tone: "",
    audience: "", 
    result: null,
    isProcessing: false,
    error: null
  });

  const steps = [
    {
      id: "input",
      title: "Input Content", 
      component: InputStep
    },
    {
      id: "preferences",
      title: "Set Preferences",
      component: PreferencesStep  
    },
    {
      id: "summarizer",
      title: "Extract Key Points",
      component: SummarizerStep
    },
    {
      id: "formatter", 
      title: "Format Content",
      component: FormatterStep
    },
    {
      id: "reviewer",
      title: "Quality Check", 
      component: ReviewerStep
    },
    {
      id: "results",
      title: "Final Results",
      component: ResultsStep
    }
  ];

  const updateWorkflowData = (updates) => {
    setWorkflowData(prev => ({ ...prev, ...updates }));
  };

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const runPipeline = async (inputText, preferences) => {
    updateWorkflowData({ isProcessing: true, error: null });

    try {
      const response = await fetch(`${API_BASE}/api/pipeline-run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: inputText,
          user_preferences: preferences,
          save_output: true,
          output_dir: "outputs",
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.status === "error") {
        throw new Error(data.message || "Pipeline execution failed");
      }

      updateWorkflowData({ 
        result: data.result,
        isProcessing: false
      });

      // Auto-advance through processing steps
      setTimeout(() => setCurrentStep(2), 500); // Summarizer
      setTimeout(() => setCurrentStep(3), 2000); // Formatter 
      setTimeout(() => setCurrentStep(4), 3500); // Reviewer
      setTimeout(() => setCurrentStep(5), 5000); // Results

    } catch (err) {
      updateWorkflowData({
        error: err.message,
        isProcessing: false
      });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto py-8 px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Content Repurposing Workflow
          </h1>
          <p className="text-gray-600">
            Transform your long-form content into engaging posts for LinkedIn, Twitter, and newsletters
          </p>
        </div>

        <StepWizard
          steps={steps}
          currentStep={currentStep}
          onStepChange={setCurrentStep}
        />

        <div className="mt-8 bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="p-8">
            {React.createElement(steps[currentStep].component, {
              workflowData,
              updateWorkflowData,
              onNext: nextStep,
              onPrev: prevStep,
              onRun: runPipeline,
              isLastStep: currentStep === steps.length - 1,
              isFirstStep: currentStep === 0
            })}
          </div>
        </div>
      </div>
    </div>
  );
}