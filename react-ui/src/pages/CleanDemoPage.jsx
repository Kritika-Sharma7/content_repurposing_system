import React, { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

// Helper function to format newsletter content
function formatNewsletterContent(content) {
  if (!content) return '';
  
  return content
    // Remove markdown headers (##)
    .replace(/^##\s+(.+)$/gm, '<h3 class="newsletter-heading">$1</h3>')
    // Convert **bold** to <strong>
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Convert line breaks
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br />');
}

function InputScreen({ onGenerate }) {
  const [text, setText] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);
  const [tone, setTone] = useState("professional");
  const [audience, setAudience] = useState("general");
  const [customAudience, setCustomAudience] = useState("");
  
  const wordCount = text.trim().split(/\s+/).filter(w => w).length;
  
  const handlePaste = (e) => {
    const pastedText = e.clipboardData.getData('text');
    const cleanedText = pastedText.replace(/\s+/g, ' ').trim();
    setText(cleanedText);
    e.preventDefault();
  };
  
  const tones = [
    "Professional", "Casual", "Analytical", "Storytelling", "Persuasive"
  ];
  
  const audiences = [
    "Developers", "Founders", "Students", "General"
  ];
  
  const handleGenerate = () => {
    onGenerate({
      text,
      tone: tone.toLowerCase(),
      audience: audience === "custom" ? customAudience : audience.toLowerCase()
    });
  };
  
  const isValid = text.trim().length >= 50 && (audience !== 'custom' || customAudience.trim());
  
  return (
    <div className="text-center">
      <h1>Transform your content</h1>
      <p>Paste your article, blog post, or idea and customize your preferences</p>
      
      <div className="textarea-container">
        <textarea
          className={`textarea ${isExpanded ? 'fullscreen' : ''}`}
          placeholder="Paste your content here... We'll transform it into engaging posts for LinkedIn, Twitter, and newsletters."
          value={text}
          onChange={(e) => setText(e.target.value)}
          onPaste={handlePaste}
        />
        <div className="word-counter">{wordCount} words</div>
        <button 
          className="expand-btn"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? '↙' : '↗'}
        </button>
      </div>
      
      <div className="mb-6 mt-6">
        <h3 className="text-left mb-4">Tone</h3>
        <div className="pill-group">
          {tones.map(t => (
            <button 
              key={t}
              className={`pill ${tone === t.toLowerCase() ? 'active' : ''}`}
              onClick={() => setTone(t.toLowerCase())}
            >
              {t}
            </button>
          ))}
        </div>
      </div>
      
      <div className="mb-6">
        <h3 className="text-left mb-4">Audience</h3>
        <div className="pill-group">
          {audiences.map(a => (
            <button 
              key={a}
              className={`pill ${audience === a.toLowerCase() ? 'active' : ''}`}
              onClick={() => setAudience(a.toLowerCase())}
            >
              {a}
            </button>
          ))}
          <button 
            className={`pill ${audience === 'custom' ? 'active' : ''}`}
            onClick={() => setAudience('custom')}
          >
            Custom
          </button>
        </div>
        
        {audience === 'custom' && (
          <input 
            type="text"
            className="textarea"
            style={{ minHeight: '50px', marginTop: '16px' }}
            placeholder="e.g., startup founders, marketing managers..."
            value={customAudience}
            onChange={(e) => setCustomAudience(e.target.value)}
          />
        )}
      </div>
      
      <button 
        className="btn btn-primary mt-6"
        disabled={!isValid}
        onClick={handleGenerate}
      >
        Generate Content
      </button>
    </div>
  );
}

function ResultsScreen({ result, error, onBack }) {
  const [activeTab, setActiveTab] = useState("summary");
  const [contentSubTab, setContentSubTab] = useState("linkedin");
  const [refinedVersion, setRefinedVersion] = useState("v2");
  
  if (error) {
    return (
      <div className="text-center">
        <h2>Something went wrong</h2>
        <p className="text-sm">{error}</p>
        <button className="btn btn-primary mt-4" onClick={onBack}>
          Try Again
        </button>
      </div>
    );
  }
  
  if (!result) {
    return (
      <div className="text-center">
        <h2>No results available</h2>
        <button className="btn btn-primary" onClick={onBack}>
          Go Back
        </button>
      </div>
    );
  }
  
  const tabs = ["Summary", "Content", "Review", "Refined"];
  
  return (
    <div>
      <div className="pipeline-info text-center mb-6">
        Pipeline: Summarizer → Formatter → Reviewer → Refiner
      </div>
      
      <div className="tabs">
        {tabs.map(tab => (
          <button 
            key={tab}
            className={`tab ${activeTab === tab.toLowerCase() ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.toLowerCase())}
          >
            {tab}
          </button>
        ))}
      </div>
      
      <div className="tab-content">
        {activeTab === "summary" && (
          <div>
            <div className="card card-highlight mb-6">
              <h3>Core Message</h3>
              <p>{result.summary?.core_message}</p>
            </div>
            
            <h3>Key Points</h3>
            <div>
              {result.summary?.key_points?.map((point, i) => (
                <div key={i} className="card">
                  <div className="flex items-center justify-between mb-2">
                    <strong>{point.label}</strong>
                    <span className={`priority-badge priority-${point.priority}`}>
                      {point.priority}
                    </span>
                  </div>
                  {point.data && <p className="text-sm">{point.data}</p>}
                </div>
              ))}
            </div>
          </div>
        )}
        
        {activeTab === "content" && (
          <div>
            <div className="tabs" style={{ marginBottom: '24px' }}>
              {["LinkedIn", "Twitter", "Newsletter"].map(platform => (
                <button 
                  key={platform}
                  className={`tab ${contentSubTab === platform.toLowerCase() ? 'active' : ''}`}
                  onClick={() => setContentSubTab(platform.toLowerCase())}
                >
                  {platform}
                </button>
              ))}
            </div>
            
            {contentSubTab === "linkedin" && (
              <div className="linkedin-preview">
                <div className="linkedin-header">
                  <div className="avatar">YU</div>
                  <div className="user-info">
                    <h4>Your Name</h4>
                    <p className="timestamp">Now</p>
                  </div>
                </div>
                <div className="linkedin-content">
                  {result.v2?.linkedin?.content || result.v1?.linkedin?.content}
                </div>
                <div className="engagement">
                  <span>👍 Like</span>
                  <span>💬 Comment</span>
                  <span>↗ Share</span>
                </div>
              </div>
            )}
            
            {contentSubTab === "twitter" && (
              <div className="tweet-thread">
                {(result.v2?.twitter?.tweets || result.v1?.twitter?.tweets || []).map((tweet, i, arr) => (
                  <div key={i} className="tweet-wrapper">
                    <div className="tweet-card">
                      <div className="tweet-header">
                        <div className="avatar">YU</div>
                        <div className="user-info">
                          <h4>Your Username</h4>
                          <p className="timestamp">@yourusername</p>
                        </div>
                      </div>
                      <div className="tweet-number">{i + 1}/{arr.length}</div>
                      <div className="tweet-content">{tweet}</div>
                    </div>
                    {i < arr.length - 1 && <div className="thread-connector"></div>}
                  </div>
                ))}
              </div>
            )}
            
            {contentSubTab === "newsletter" && (
              <div className="newsletter-preview">
                <div className="newsletter-header">
                  <h2 className="newsletter-title">Your Newsletter</h2>
                  <p className="newsletter-subtitle">Curated insights delivered to your inbox</p>
                </div>
                <div className="newsletter-content">
                  <div dangerouslySetInnerHTML={{ 
                    __html: formatNewsletterContent(result.v2?.newsletter?.content || result.v1?.newsletter?.content || '')
                  }} />
                </div>
              </div>
            )}
          </div>
        )}
        
        {activeTab === "review" && (
          <div>
            {result.review?.issues?.length ? (
              <>
                {["critical", "high", "medium"].map(priority => {
                  const issues = result.review.issues.filter(issue => issue.priority === priority);
                  if (!issues.length) return null;
                  
                  return (
                    <div key={priority} className="issues-group">
                      <div className="issues-header">
                        <h3>{priority.toUpperCase()}</h3>
                        <span className={`priority-badge priority-${priority}`}>
                          {issues.length} issues
                        </span>
                      </div>
                      {issues.map((issue, i) => (
                        <div key={i} className="issue-item">
                          <div className="issue-problem">{issue.problem}</div>
                          <div className="issue-reason">{issue.reason}</div>
                          <div className="issue-suggestion">{issue.suggestion}</div>
                        </div>
                      ))}
                    </div>
                  );
                })}
              </>
            ) : (
              <div className="card text-center">
                <p>No issues found! Your content looks great.</p>
              </div>
            )}
          </div>
        )}
        
        {activeTab === "refined" && (
          <div>
            <div className="toggle-group mb-6">
              <button 
                className={`toggle-btn ${refinedVersion === 'v1' ? 'active' : ''}`}
                onClick={() => setRefinedVersion('v1')}
              >
                Show V1
              </button>
              <button 
                className={`toggle-btn ${refinedVersion === 'v2' ? 'active' : ''}`}
                onClick={() => setRefinedVersion('v2')}
              >
                Show V2
              </button>
            </div>
            
            {/* Show same content structure as Content tab but for selected version */}
            <div className="tabs" style={{ marginBottom: '24px' }}>
              {["LinkedIn", "Twitter", "Newsletter"].map(platform => (
                <button 
                  key={platform}
                  className={`tab ${contentSubTab === platform.toLowerCase() ? 'active' : ''}`}
                  onClick={() => setContentSubTab(platform.toLowerCase())}
                >
                  {platform}
                </button>
              ))}
            </div>
            
            {/* Same content display logic as Content tab */}
            {contentSubTab === "linkedin" && (
              <div className="linkedin-preview">
                <div className="linkedin-header">
                  <div className="avatar">YU</div>
                  <div className="user-info">
                    <h4>Your Name</h4>
                    <p className="timestamp">Now</p>
                  </div>
                </div>
                <div className="linkedin-content">
                  {refinedVersion === 'v2' ? result.v2?.linkedin?.content : result.v1?.linkedin?.content}
                </div>
                <div className="engagement">
                  <span>👍 Like</span>
                  <span>💬 Comment</span>
                  <span>↗ Share</span>
                </div>
              </div>
            )}
            
            {contentSubTab === "twitter" && (
              <div className="tweet-thread">
                {(refinedVersion === 'v2' ? result.v2?.twitter?.tweets : result.v1?.twitter?.tweets || []).map((tweet, i, arr) => (
                  <div key={i} className="tweet-wrapper">
                    <div className="tweet-card">
                      <div className="tweet-header">
                        <div className="avatar">YU</div>
                        <div className="user-info">
                          <h4>Your Username</h4>
                          <p className="timestamp">@yourusername</p>
                        </div>
                      </div>
                      <div className="tweet-number">{i + 1}/{arr.length}</div>
                      <div className="tweet-content">{tweet}</div>
                    </div>
                    {i < arr.length - 1 && <div className="thread-connector"></div>}
                  </div>
                ))}
              </div>
            )}
            
            {contentSubTab === "newsletter" && (
              <div className="newsletter-preview">
                <div className="newsletter-header">
                  <h2 className="newsletter-title">Your Newsletter</h2>
                  <p className="newsletter-subtitle">Curated insights delivered to your inbox</p>
                </div>
                <div className="newsletter-content">
                  <div dangerouslySetInnerHTML={{ 
                    __html: formatNewsletterContent(refinedVersion === 'v2' ? result.v2?.newsletter?.content : result.v1?.newsletter?.content || '')
                  }} />
                </div>
              </div>
            )}
            
            {result.v2?.changes?.length > 0 && (
              <div className="changes-section mt-6">
                <h3>Changes Made</h3>
                {result.v2.changes.map((change, i) => (
                  <div key={i} className="change-item">
                    <strong>{change.action}:</strong> {change.target}
                    {change.before && change.after && (
                      <div className="change-detail">
                        <div className="change-before">"{change.before}"</div>
                        <div className="change-after">"{change.after}"</div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
      
      <div className="text-center mt-8">
        <button className="btn btn-secondary" onClick={onBack}>
          Generate New Content
        </button>
      </div>
    </div>
  );
}

export default function CleanDemoPage() {
  const [step, setStep] = useState(1); // 1: Input, 2: Results
  const [inputText, setInputText] = useState("");
  const [preferences, setPreferences] = useState({
    tone: "professional",
    audience: "general"
  });
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState("");
  const [error, setError] = useState("");

  const handleGenerate = async ({ text, tone, audience }) => {
    setInputText(text);
    setPreferences({ tone, audience });
    setIsLoading(true);
    setLoadingStep("Extracting insights...");
    setError("");
    
    // Simulate loading steps
    const steps = [
      "Extracting insights...",
      "Formatting content...", 
      "Reviewing quality...",
      "Refining content..."
    ];

    let stepIndex = 0;
    const stepInterval = setInterval(() => {
      stepIndex++;
      if (stepIndex < steps.length) {
        setLoadingStep(steps[stepIndex]);
      }
    }, 1500);

    try {
      const response = await fetch(`${API_BASE}/api/pipeline-run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          input_type: "text",
          content: text,
          user_preferences: {
            tone: tone,
            audience: audience,
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
      setStep(2);
      
    } catch (err) {
      setError(err.message);
    } finally {
      clearInterval(stepInterval);
      setIsLoading(false);
      setLoadingStep("");
    }
  };

  const handleBack = () => {
    setStep(1);
    setResult(null);
    setError("");
  };

  if (isLoading) {
    return (
      <div className="loading-overlay">
        <div className="loading-content">
          <div className="loading-spinner"></div>
          <div className="loading-step">{loadingStep}</div>
          <div className="pipeline-info">
            Pipeline: Summarizer → Formatter → Reviewer → Refiner
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="container">
        {step === 1 && (
          <InputScreen onGenerate={handleGenerate} />
        )}
        
        {step === 2 && (
          <ResultsScreen 
            result={result}
            preferences={preferences}
            inputText={inputText}
            error={error}
            onBack={handleBack}
          />
        )}
      </div>
    </div>
  );
}