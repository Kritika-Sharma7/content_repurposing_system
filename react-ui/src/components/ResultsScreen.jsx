import { useState } from "react";
import SummaryTab from "./SummaryTab";
import ContentTab from "./ContentTab";
import ReviewTab from "./ReviewTab";
import RefinedTab from "./RefinedTab";

export default function ResultsScreen({ 
  result, 
  isLoading, 
  loadingStep, 
  error, 
  onBack, 
  preferences,
  inputText 
}) {
  const [activeTab, setActiveTab] = useState("summary");

  const tabs = [
    { id: "summary", label: "Summary", icon: "📊" },
    { id: "content", label: "Content", icon: "📝" },
    { id: "review", label: "Review", icon: "🔍" },
    { id: "refined", label: "Refined", icon: "✨" }
  ];

  if (error) {
    return (
      <div className="p-8">
        <div className="text-center">
          <div className="text-red-500 text-xl mb-4">⚠️ Error</div>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={onBack}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="text-center">
          <div className="mb-6">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Processing your content...
          </h3>
          <p className="text-gray-600 mb-8">{loadingStep}</p>
          
          {/* Pipeline visualization */}
          <div className="max-w-md mx-auto">
            <div className="text-sm text-gray-500 mb-3">Pipeline:</div>
            <div className="flex items-center justify-center space-x-2 text-sm">
              <span className="text-blue-600">Summarizer</span>
              <span className="text-gray-300">→</span>
              <span className="text-blue-600">Formatter</span>
              <span className="text-gray-300">→</span>
              <span className="text-blue-600">Reviewer</span>
              <span className="text-gray-300">→</span>
              <span className="text-blue-600">Refiner</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="p-8">
        <div className="text-center">
          <p className="text-gray-600">No results available.</p>
          <button
            onClick={onBack}
            className="mt-4 bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div>
      {/* Header with back button */}
      <div className="p-6 border-b bg-gray-50">
        <div className="flex items-center justify-between">
          <div>
            <button
              onClick={onBack}
              className="text-gray-600 hover:text-gray-800 font-medium mb-2"
            >
              ← Back to Preferences
            </button>
            <h2 className="text-xl font-semibold text-gray-900">Content Results</h2>
            <div className="text-sm text-gray-500 mt-1">
              Tone: <span className="capitalize">{preferences.tone}</span> • 
              Audience: <span className="capitalize">{preferences.audience}</span>
            </div>
          </div>
          
          {/* Pipeline indicator */}
          <div className="hidden md:flex items-center space-x-1 text-xs text-gray-500">
            <span>Summarizer</span>
            <span>→</span>
            <span>Formatter</span>
            <span>→</span>
            <span>Reviewer</span>
            <span>→</span>
            <span>Refiner</span>
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="border-b">
        <nav className="flex space-x-8 px-6">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.id
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {activeTab === "summary" && (
          <SummaryTab 
            summary={result.summary}
            inputText={inputText}
            preferences={preferences}
          />
        )}
        
        {activeTab === "content" && (
          <ContentTab 
            content={result.v1}
            preferences={preferences}
          />
        )}
        
        {activeTab === "review" && (
          <ReviewTab 
            review={result.review}
          />
        )}
        
        {activeTab === "refined" && (
          <RefinedTab 
            refined={result.v2}
            original={result.v1}
            preferences={preferences}
          />
        )}
      </div>
    </div>
  );
}