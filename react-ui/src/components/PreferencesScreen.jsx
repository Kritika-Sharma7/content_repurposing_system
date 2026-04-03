import { useState } from "react";

export default function PreferencesScreen({ onGenerate, onBack, initialPreferences = {} }) {
  const [tone, setTone] = useState(initialPreferences.tone || "");
  const [audience, setAudience] = useState(initialPreferences.audience || "");
  const [customAudience, setCustomAudience] = useState("");

  const toneOptions = [
    { id: "professional", label: "Professional", description: "Formal, business-focused" },
    { id: "casual", label: "Casual", description: "Friendly, conversational" },
    { id: "analytical", label: "Analytical", description: "Data-driven, logical" },
    { id: "storytelling", label: "Storytelling", description: "Narrative, engaging" },
    { id: "persuasive", label: "Persuasive", description: "Convincing, action-oriented" }
  ];

  const audienceOptions = [
    { id: "developers", label: "Developers", description: "Software engineers, technical teams" },
    { id: "founders", label: "Founders", description: "Entrepreneurs, startup leaders" },
    { id: "students", label: "Students", description: "Learning community, academics" },
    { id: "general", label: "General", description: "Broad professional audience" },
    { id: "custom", label: "Custom", description: "Define your own audience" }
  ];

  const handleGenerate = () => {
    const finalAudience = audience === "custom" ? customAudience : audience;
    if (tone && (finalAudience || customAudience)) {
      onGenerate({
        tone,
        audience: finalAudience
      });
    }
  };

  const isValid = tone && (audience !== "custom" ? audience : customAudience.trim());

  return (
    <div className="p-8">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-2">
          Set Your Preferences
        </h2>
        <p className="text-gray-600">
          Choose the tone and target audience for your repurposed content. This helps our AI tailor the messaging for maximum engagement.
        </p>
      </div>

      <div className="space-y-8">
        {/* Tone Selection */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Tone</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {toneOptions.map((option) => (
              <button
                key={option.id}
                onClick={() => setTone(option.id)}
                className={`p-4 border rounded-lg text-left transition-colors ${
                  tone === option.id
                    ? "border-blue-500 bg-blue-50 text-blue-900"
                    : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                }`}
              >
                <div className="font-medium">{option.label}</div>
                <div className="text-sm text-gray-600 mt-1">{option.description}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Audience Selection */}
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Target Audience</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {audienceOptions.map((option) => (
              <button
                key={option.id}
                onClick={() => setAudience(option.id)}
                className={`p-4 border rounded-lg text-left transition-colors ${
                  audience === option.id
                    ? "border-blue-500 bg-blue-50 text-blue-900"
                    : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                }`}
              >
                <div className="font-medium">{option.label}</div>
                <div className="text-sm text-gray-600 mt-1">{option.description}</div>
              </button>
            ))}
          </div>

          {/* Custom audience input */}
          {audience === "custom" && (
            <div className="mt-4">
              <input
                type="text"
                value={customAudience}
                onChange={(e) => setCustomAudience(e.target.value)}
                placeholder="Describe your target audience (e.g., 'Product managers at B2B SaaS companies')"
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex items-center justify-between pt-4 border-t">
          <button
            onClick={onBack}
            className="px-6 py-3 text-gray-600 hover:text-gray-800 font-medium"
          >
            ← Back to Input
          </button>

          <button
            onClick={handleGenerate}
            disabled={!isValid}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-blue-700 transition-colors"
          >
            Generate Content
          </button>
        </div>
      </div>
    </div>
  );
}