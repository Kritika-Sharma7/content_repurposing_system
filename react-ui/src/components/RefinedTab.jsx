import { useState } from "react";
import ContentTab from "./ContentTab";

export default function RefinedTab({ refined, original, preferences }) {
  const [showVersion, setShowVersion] = useState("v2"); // v1 or v2
  
  if (!refined) {
    return (
      <div className="text-center text-gray-500">
        No refined content available
      </div>
    );
  }

  const changes = refined.changes || [];

  return (
    <div className="space-y-6">
      {/* Version Toggle */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900">
          Refined Content
        </h3>
        
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600">Show:</span>
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setShowVersion("v1")}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                showVersion === "v1"
                  ? "bg-white text-gray-900 shadow-sm"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              Original (V1)
            </button>
            <button
              onClick={() => setShowVersion("v2")}
              className={`px-3 py-1.5 rounded text-sm font-medium transition-colors ${
                showVersion === "v2"
                  ? "bg-white text-gray-900 shadow-sm"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              Refined (V2)
            </button>
          </div>
        </div>
      </div>

      {/* Content Display */}
      <div>
        {showVersion === "v1" ? (
          <ContentTab content={original} preferences={preferences} />
        ) : (
          <ContentTab content={refined} preferences={preferences} />
        )}
      </div>

      {/* Changes Made Section */}
      {changes.length > 0 && (
        <div className="border-t pt-6">
          <h4 className="text-lg font-medium text-gray-900 mb-4">
            Changes Made ({changes.length})
          </h4>
          
          <div className="space-y-4">
            {changes.map((change, index) => (
              <ChangeCard key={change.issue_id || index} change={change} />
            ))}
          </div>
        </div>
      )}

      {/* Improvement Summary */}
      <div className="bg-green-50 border border-green-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <div className="text-green-500">✨</div>
          <div>
            <h4 className="font-medium text-green-900">Content Improved</h4>
            <p className="text-green-800 text-sm mt-1">
              {changes.length === 0 
                ? "Your original content was already high quality - no changes needed!"
                : `Applied ${changes.length} targeted improvements to enhance clarity, coverage, and engagement.`
              }
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

function ChangeCard({ change }) {
  const actionLabels = {
    add: "Added content",
    modify: "Modified content", 
    remove: "Removed content",
    rewrite: "Rewrote content",
    shorten: "Shortened content",
    restructure: "Restructured content"
  };

  const actionIcons = {
    add: "➕",
    modify: "✏️", 
    remove: "➖",
    rewrite: "🔄",
    shorten: "📝",
    restructure: "🔧"
  };

  const actionColors = {
    add: "bg-green-50 border-green-200",
    modify: "bg-blue-50 border-blue-200",
    remove: "bg-red-50 border-red-200", 
    rewrite: "bg-purple-50 border-purple-200",
    shorten: "bg-yellow-50 border-yellow-200",
    restructure: "bg-indigo-50 border-indigo-200"
  };

  return (
    <div className={`border rounded-lg p-4 ${actionColors[change.action] || "bg-gray-50 border-gray-200"}`}>
      <div className="flex items-start space-x-3">
        <div className="text-lg">
          {actionIcons[change.action] || "📝"}
        </div>
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <h5 className="font-medium text-gray-900">
              {actionLabels[change.action] || "Changed content"}
            </h5>
            <span className="text-sm text-gray-600 bg-white px-2 py-0.5 rounded border">
              {change.target}
            </span>
          </div>
          
          {change.before && change.after && (
            <div className="space-y-3 text-sm">
              <div>
                <div className="text-gray-600 font-medium mb-1">Before:</div>
                <div className="bg-white p-3 rounded border italic text-gray-700">
                  {change.before}
                </div>
              </div>
              
              <div>
                <div className="text-gray-600 font-medium mb-1">After:</div>
                <div className="bg-white p-3 rounded border text-gray-800 font-medium">
                  {change.after}
                </div>
              </div>
            </div>
          )}
          
          {change.issue_id && (
            <div className="mt-2 text-xs text-gray-500">
              Addresses issue: {change.issue_id}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}