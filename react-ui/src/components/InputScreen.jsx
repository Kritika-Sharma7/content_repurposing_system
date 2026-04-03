import { useState, useRef, useEffect } from "react";

export default function InputScreen({ onContinue, initialText = "" }) {
  const [text, setText] = useState(initialText);
  const [wordCount, setWordCount] = useState(0);
  const [isExpanded, setIsExpanded] = useState(false);
  const textareaRef = useRef(null);

  useEffect(() => {
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    setWordCount(words);
  }, [text]);

  const handleTextChange = (e) => {
    setText(e.target.value);
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  const handleContinue = () => {
    if (text.trim()) {
      onContinue(text);
    }
  };

  const handleExpand = () => {
    setIsExpanded(true);
  };

  const handleCloseModal = () => {
    setIsExpanded(false);
  };

  const sampleText = `The Future of Remote Work: Lessons from Five Years of Distributed Teams

After leading distributed engineering teams for five years, I've learned that remote work success isn't about tools or policies—it's about trust and intentional communication.

The biggest mistake companies make is trying to replicate office culture online. Forcing 9-to-5 schedules across time zones destroys productivity. Instead, focus on async-first communication where possible. We reduced meetings by 60% by switching to written proposals with comment-based discussions.

Key insight: Documentation becomes your office. When we mandated that every decision must be documented, onboarding time dropped from 3 months to 3 weeks. New hires could trace the "why" behind every system.`;

  const placeholderText = "Paste your long-form content here (blog post, article, documentation, etc.)...\n\nFor example, you might paste a detailed blog post about remote work practices, a technical deep-dive, or insights from your industry experience.";

  return (
    <>
      <div className="p-8">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            Input Your Content
          </h2>
          <p className="text-gray-600">
            Paste your long-form content below. This could be a blog post, article, documentation, or any detailed text you want to repurpose for social media.
          </p>
        </div>

        <div className="space-y-4">
          {/* Main textarea */}
          <div className="relative">
            <textarea
              ref={textareaRef}
              value={text}
              onChange={handleTextChange}
              placeholder={placeholderText}
              className="w-full p-4 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              style={{ minHeight: "300px" }}
              rows={12}
            />
            
            {/* Expand button */}
            {!isExpanded && text.length > 500 && (
              <button
                onClick={handleExpand}
                className="absolute bottom-4 right-4 bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1.5 rounded text-sm transition-colors"
              >
                Expand
              </button>
            )}
          </div>

          {/* Word counter and sample button */}
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-500">
              {wordCount} words {wordCount < 50 && "(Minimum 50 words recommended)"}
            </div>
            
            <button
              onClick={() => setText(sampleText)}
              className="text-sm text-blue-600 hover:text-blue-700 hover:underline"
            >
              Use sample content
            </button>
          </div>

          {/* Continue button */}
          <div className="flex justify-end pt-4">
            <button
              onClick={handleContinue}
              disabled={!text.trim() || wordCount < 10}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-blue-700 transition-colors"
            >
              Continue to Preferences
            </button>
          </div>
        </div>
      </div>

      {/* Fullscreen Modal */}
      {isExpanded && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-4xl h-[80vh] flex flex-col">
            {/* Modal header */}
            <div className="p-6 border-b flex items-center justify-between">
              <h3 className="text-lg font-semibold">Edit Content</h3>
              <button
                onClick={handleCloseModal}
                className="text-gray-400 hover:text-gray-600 text-xl font-bold"
              >
                ×
              </button>
            </div>
            
            {/* Modal content */}
            <div className="flex-1 p-6">
              <textarea
                value={text}
                onChange={handleTextChange}
                className="w-full h-full p-4 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder={placeholderText}
              />
            </div>
            
            {/* Modal footer */}
            <div className="p-6 border-t flex items-center justify-between">
              <div className="text-sm text-gray-500">
                {wordCount} words
              </div>
              <div className="space-x-3">
                <button
                  onClick={handleCloseModal}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800"
                >
                  Close
                </button>
                <button
                  onClick={() => {
                    handleCloseModal();
                    if (text.trim()) handleContinue();
                  }}
                  disabled={!text.trim() || wordCount < 10}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium disabled:bg-gray-300 disabled:cursor-not-allowed hover:bg-blue-700 transition-colors"
                >
                  Continue
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}