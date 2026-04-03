import { useState } from "react";

export default function ContentTab({ content, preferences }) {
  const [activeSubTab, setActiveSubTab] = useState("linkedin");

  if (!content) {
    return (
      <div className="text-center text-gray-500">
        No content available
      </div>
    );
  }

  const subTabs = [
    { id: "linkedin", label: "LinkedIn", icon: "💼" },
    { id: "twitter", label: "Twitter", icon: "🐦" },
    { id: "newsletter", label: "Newsletter", icon: "📧" }
  ];

  return (
    <div>
      {/* Sub-tab Navigation */}
      <div className="border-b mb-6">
        <nav className="flex space-x-6">
          {subTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveSubTab(tab.id)}
              className={`py-3 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeSubTab === tab.id
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Content Preview */}
      <div>
        {activeSubTab === "linkedin" && (
          <LinkedInPreview content={content.linkedin?.content} />
        )}
        
        {activeSubTab === "twitter" && (
          <TwitterPreview tweets={content.twitter?.tweets} />
        )}
        
        {activeSubTab === "newsletter" && (
          <NewsletterPreview content={content.newsletter?.content} />
        )}
      </div>
    </div>
  );
}

function LinkedInPreview({ content }) {
  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
        {/* Header */}
        <div className="p-4 flex items-start space-x-3">
          <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
            U
          </div>
          <div className="flex-1">
            <div className="font-semibold text-gray-900">Your Name</div>
            <div className="text-sm text-gray-500">Professional Title • Now</div>
          </div>
        </div>
        
        {/* Content */}
        <div className="px-4 pb-4">
          <div className="text-gray-800 whitespace-pre-line leading-relaxed">
            {content}
          </div>
        </div>
        
        {/* Engagement Bar */}
        <div className="border-t border-gray-100 px-4 py-3">
          <div className="flex items-center space-x-6 text-sm text-gray-500">
            <button className="flex items-center space-x-1 hover:text-blue-600">
              <span>👍</span>
              <span>Like</span>
            </button>
            <button className="flex items-center space-x-1 hover:text-blue-600">
              <span>💬</span>
              <span>Comment</span>
            </button>
            <button className="flex items-center space-x-1 hover:text-blue-600">
              <span>🔄</span>
              <span>Share</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function TwitterPreview({ tweets = [] }) {
  return (
    <div className="max-w-xl mx-auto space-y-3">
      {tweets.map((tweet, index) => (
        <div key={index} className="bg-white border border-gray-200 rounded-xl p-4">
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-semibold">
              U
            </div>
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <span className="font-semibold text-gray-900">Your Name</span>
                <span className="text-gray-500">@username</span>
                <span className="text-gray-500">•</span>
                <span className="text-gray-500">now</span>
              </div>
              <div className="text-gray-800 mb-3 leading-relaxed">
                {tweet}
              </div>
              <div className="flex items-center justify-between text-gray-500 max-w-md">
                <button className="flex items-center space-x-1 hover:text-blue-500">
                  <span>💬</span>
                  <span className="text-sm">Reply</span>
                </button>
                <button className="flex items-center space-x-1 hover:text-green-500">
                  <span>🔄</span>
                  <span className="text-sm">Retweet</span>
                </button>
                <button className="flex items-center space-x-1 hover:text-red-500">
                  <span>❤️</span>
                  <span className="text-sm">Like</span>
                </button>
              </div>
            </div>
          </div>
          
          {/* Thread indicator */}
          {index < tweets.length - 1 && (
            <div className="flex justify-center mt-3">
              <div className="w-0.5 h-4 bg-gray-300"></div>
            </div>
          )}
        </div>
      ))}
      
      <div className="text-center text-sm text-gray-500">
        Thread: {tweets.length} tweets
      </div>
    </div>
  );
}

function NewsletterPreview({ content }) {
  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-8" style={{ fontFamily: 'Georgia, serif' }}>
        <div className="bg-white p-6 rounded shadow-sm">
          <div className="border-b border-gray-200 pb-4 mb-6">
            <h2 className="text-xl font-bold text-gray-900">Newsletter Title</h2>
            <p className="text-sm text-gray-600">Issue #XX • Today</p>
          </div>
          
          <div className="prose prose-gray max-w-none">
            <div className="text-gray-800 leading-relaxed space-y-4 whitespace-pre-line">
              {content}
            </div>
          </div>
          
          <div className="border-t border-gray-200 pt-4 mt-6">
            <div className="text-sm text-gray-600 text-center">
              Thank you for reading! Forward this to a friend who might find it valuable.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}