import { useState } from "react";
import InputScreen from "../components/InputScreen";
import PreferencesScreen from "../components/PreferencesScreen";
import ResultsScreen from "../components/ResultsScreen";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export default function NewDemoPage() {
  const [currentScreen, setCurrentScreen] = useState("input"); // input, preferences, results
  const [inputText, setInputText] = useState("");
  const [preferences, setPreferences] = useState({
    tone: "",
    audience: ""
  });
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState("");
  const [error, setError] = useState("");

  const handleInputContinue = (text) => {
    setInputText(text);
    setCurrentScreen("preferences");
  };

  const handleGenerate = async (prefs) => {
    setPreferences(prefs);
    setCurrentScreen("results");
    setIsLoading(true);
    setError("");

    try {
      // Simulate step progression
      setLoadingStep("Extracting insights...");
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setLoadingStep("Formatting content...");
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setLoadingStep("Reviewing quality...");
      await new Promise(resolve => setTimeout(resolve, 1000));

      const response = await fetch(`${API_BASE}/api/pipeline-run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          input_type: "text",
          content: inputText,
          user_preferences: {
            tone: prefs.tone,
            audience: prefs.audience,
            goal: "engagement",
            platforms: ["linkedin", "twitter", "newsletter"]
          },
          save_output: true,
          output_dir: "outputs",
          model: "gpt-4o",
          temperature: 0.7,
          max_iterations: 2
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.status === "error") {
        throw new Error(data.message || "Pipeline execution failed");
      }

      setResult(data.result);
      
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
      setLoadingStep("");
    }
  };

  const handleBack = () => {
    if (currentScreen === "preferences") {
      setCurrentScreen("input");
    } else if (currentScreen === "results") {
      setCurrentScreen("preferences");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Content Repurposing Tool
          </h1>
          <p className="text-gray-600">
            Transform your long-form content into engaging posts for LinkedIn, Twitter, and newsletters
          </p>
        </div>

        {/* Progress indicator */}
        <div className="mb-8 flex items-center justify-center space-x-4">
          <div className={`flex items-center space-x-2 ${
            currentScreen === "input" ? "text-blue-600" : "text-gray-400"
          }`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
              currentScreen === "input" ? "bg-blue-600 text-white" : "bg-gray-200"
            }`}>
              1
            </div>
            <span className="hidden sm:block">Input</span>
          </div>
          
          <div className="w-8 h-1 bg-gray-200 rounded"></div>
          
          <div className={`flex items-center space-x-2 ${
            currentScreen === "preferences" ? "text-blue-600" : "text-gray-400"
          }`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
              currentScreen === "preferences" ? "bg-blue-600 text-white" : "bg-gray-200"
            }`}>
              2
            </div>
            <span className="hidden sm:block">Preferences</span>
          </div>
          
          <div className="w-8 h-1 bg-gray-200 rounded"></div>
          
          <div className={`flex items-center space-x-2 ${
            currentScreen === "results" ? "text-blue-600" : "text-gray-400"
          }`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
              currentScreen === "results" ? "bg-blue-600 text-white" : "bg-gray-200"
            }`}>
              3
            </div>
            <span className="hidden sm:block">Results</span>
          </div>
        </div>

        {/* Screen Content */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {currentScreen === "input" && (
            <InputScreen
              onContinue={handleInputContinue}
              initialText={inputText}
            />
          )}
          
          {currentScreen === "preferences" && (
            <PreferencesScreen
              onGenerate={handleGenerate}
              onBack={handleBack}
              initialPreferences={preferences}
            />
          )}
          
          {currentScreen === "results" && (
            <ResultsScreen
              result={result}
              isLoading={isLoading}
              loadingStep={loadingStep}
              error={error}
              onBack={handleBack}
              preferences={preferences}
              inputText={inputText}
            />
          )}
        </div>
      </div>
    </div>
  );
}