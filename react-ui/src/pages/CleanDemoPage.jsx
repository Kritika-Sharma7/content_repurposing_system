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
  
  const tabs = ["Summary", "Content", "Review", "Refined", "Outcome"];
  
  // Determine available versions dynamically
  const availableVersions = ['v1'];
  if (result.v2) availableVersions.push('v2');
  if (result.v3) availableVersions.push('v3');
  if (result.v4) availableVersions.push('v4');
  if (result.v5) availableVersions.push('v5');
  
  return (
    <div>
      {/* Progress Indicator */}
      <div className="progress-bar">
        {tabs.map((tab, index) => {
          const tabKey = tab.toLowerCase();
          const currentIndex = tabs.findIndex(t => t.toLowerCase() === activeTab);
          const isCompleted = index < currentIndex;
          const isCurrent = index === currentIndex;
          const isUpcoming = index > currentIndex;
          
          return (
            <div key={tab} className="progress-step-wrapper">
              <div 
                className={`progress-step ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''} ${isUpcoming ? 'upcoming' : ''}`}
                onClick={() => setActiveTab(tabKey)}
              >
                <div className="step-dot"></div>
                <span className="step-label">{tab}</span>
              </div>
              {index < tabs.length - 1 && (
                <div className={`step-connector ${isCompleted ? 'filled' : ''}`}></div>
              )}
            </div>
          );
        })}
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
          <div className="review-container">
            {/* Show iteration history if available */}
            {result.iterations && result.iterations.length > 0 ? (
              <div>
                {/* Summary Stats - Compact inline layout */}
                <div className="review-summary-bar">
                  <h2 className="review-title">Review Summary</h2>
                  <div className="review-stats">
                    <span className="stat-item">{result.iterations.length} Iteration{result.iterations.length > 1 ? 's' : ''}</span>
                    <span className="stat-divider">|</span>
                    <span className="stat-item">{result.iterations.reduce((sum, it) => sum + (it.review?.issues?.length || 0), 0)} Issues</span>
                  </div>
                </div>

                {/* Two-column layout for iterations */}
                <div className="review-grid" style={{ gridTemplateColumns: result.iterations.length > 1 ? 'repeat(2, 1fr)' : '1fr' }}>
                  {result.iterations.map((iteration) => {
                    const review = iteration.review;
                    const totalIssues = review?.issues?.length || 0;
                    
                    return (
                      <div key={iteration.iteration} className="review-column">
                        {/* Header - Single row */}
                        <div className="review-column-header">
                          <div className="review-header-left">
                            <span className="review-version">Review of V{iteration.iteration}</span>
                            <span className="review-iteration">Iteration {iteration.iteration}</span>
                          </div>
                          <span className={`issue-count-badge ${totalIssues === 0 ? 'success' : ''}`}>
                            {totalIssues === 0 ? '✓ Passed' : `${totalIssues} Issues`}
                          </span>
                        </div>

                        {/* Issues Container with scroll */}
                        <div className="issues-scroll-container">
                          {totalIssues === 0 ? (
                            <div className="no-issues">
                              <span className="check-icon">✓</span>
                              <span>All quality checks passed</span>
                            </div>
                          ) : (
                            <>
                              {["critical", "high", "medium"].map(priority => {
                                const issues = review.issues.filter(issue => issue.priority === priority);
                                if (!issues.length) return null;
                                
                                return (
                                  <div key={priority} className="priority-group">
                                    <div className="priority-label-row">
                                      <span className={`priority-label ${priority}`}>{priority}</span>
                                      <span className="priority-count">{issues.length}</span>
                                    </div>
                                    {issues.map((issue, i) => {
                                      // Strip kp_X prefix from problem text
                                      const cleanProblem = issue.problem?.replace(/^kp_\d+\s*[\(\[]?/i, '').replace(/^\(/, '');
                                      return (
                                        <div key={i} className="issue-card">
                                          <div className="issue-problem-text">{cleanProblem}</div>
                                          <div className="issue-suggestion-text">{issue.suggestion}</div>
                                        </div>
                                      );
                                    })}
                                  </div>
                                );
                              })}
                            </>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="no-review-data">
                <p>No review data available.</p>
              </div>
            )}
          </div>
        )}
        
        {activeTab === "refined" && (
          <div className="refined-container">
            {/* Version Toggle - at top */}
            <div className="refined-header">
              <div className="version-selector">
                {availableVersions.map(v => (
                  <button 
                    key={v}
                    className={`version-btn ${refinedVersion === v ? 'active' : ''}`}
                    onClick={() => setRefinedVersion(v)}
                  >
                    {v.toUpperCase()} {v === availableVersions[availableVersions.length - 1] ? '(Final)' : ''}
                  </button>
                ))}
              </div>
              
              {/* Platform tabs */}
              <div className="platform-tabs-inline">
                {["LinkedIn", "Twitter", "Newsletter"].map(platform => (
                  <button 
                    key={platform}
                    className={`platform-tab-sm ${contentSubTab === platform.toLowerCase() ? 'active' : ''}`}
                    onClick={() => setContentSubTab(platform.toLowerCase())}
                  >
                    {platform}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Two-column layout */}
            <div className="refined-layout">
              {/* Left: Content */}
              <div className="refined-content-col">
                {(() => {
                  const currentVersion = (() => {
                    switch(refinedVersion) {
                      case 'v5': return result.v5;
                      case 'v4': return result.v4;
                      case 'v3': return result.v3;
                      case 'v2': return result.v2;
                      default: return result.v1;
                    }
                  })();
                  if (!currentVersion) return <p>No content for this version.</p>;
                  
                  return (
                    <>
                      {contentSubTab === "linkedin" && (
                        <div className="refined-linkedin">
                          <div className="refined-card-header">
                            <div className="avatar-sm">YU</div>
                            <div className="user-info-compact">
                              <span className="user-name">Your Name</span>
                              <span className="user-meta">Now</span>
                            </div>
                          </div>
                          <div className="refined-card-body">
                            {currentVersion?.linkedin?.content}
                          </div>
                          <div className="refined-card-footer">
                            <span>Like</span>
                            <span>Comment</span>
                            <span>Share</span>
                          </div>
                        </div>
                      )}
                      
                      {contentSubTab === "twitter" && (
                        <div className="refined-twitter">
                          {(currentVersion?.twitter?.tweets || []).map((tweet, i, arr) => (
                            <div key={i} className="refined-tweet">
                              <div className="tweet-left-accent"></div>
                              <div className="refined-tweet-body">
                                <div className="refined-tweet-meta">
                                  <div className="tweet-user-info">
                                    <div className="avatar-xs">YU</div>
                                    <span className="user-name">Your Username</span>
                                    <span className="user-handle">@yourusername</span>
                                  </div>
                                  <span className="tweet-num">{i + 1}/{arr.length}</span>
                                </div>
                                <div className="refined-tweet-text">{tweet}</div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                      
                      {contentSubTab === "newsletter" && (
                        <div className="refined-newsletter">
                          <div className="refined-newsletter-header">
                            <span className="newsletter-label">Your Newsletter</span>
                            <span className="newsletter-tagline">Curated insights delivered to your inbox</span>
                          </div>
                          <div className="refined-newsletter-body" dangerouslySetInnerHTML={{ 
                            __html: formatNewsletterContent(currentVersion?.newsletter?.content || '')
                          }} />
                        </div>
                      )}
                    </>
                  );
                })()}
              </div>
              
              {/* Right: Changes (sticky) */}
              {refinedVersion !== 'v1' && (
                <div className="refined-changes-col">
                  <div className="changes-panel">
                    <div className="changes-panel-header">
                      <span className="changes-title">Changes in {refinedVersion.toUpperCase()}</span>
                    </div>
                    <div className="changes-panel-body">
                      {(() => {
                        const currentChanges = (() => {
                          switch(refinedVersion) {
                            case 'v5': return result.v5?.changes;
                            case 'v4': return result.v4?.changes;
                            case 'v3': return result.v3?.changes;
                            case 'v2': return result.v2?.changes;
                            default: return [];
                          }
                        })() || [];
                        
                        return currentChanges.map((change, i) => (
                          <div key={i} className="change-card">
                            <div className="change-action">
                              <span className="action-type">{change.action}</span>
                              <span className="action-target">{change.target}</span>
                            </div>
                            {change.before && change.after && (
                              <div className="change-diff">
                                <div className="diff-before">{change.before}</div>
                                <div className="diff-after">{change.after}</div>
                              </div>
                            )}
                          </div>
                        ));
                      })()}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === "outcome" && (
          <div className="outcome-container">
            <div className="outcome-header">
              <h2>Final Output</h2>
              <p>Your content has been refined and is ready to use. Copy the content below for each platform.</p>
            </div>
            
            {/* Platform tabs */}
            <div className="platform-tabs">
              {["LinkedIn", "Twitter", "Newsletter"].map(platform => (
                <button 
                  key={platform}
                  className={`platform-tab ${contentSubTab === platform.toLowerCase() ? 'active' : ''}`}
                  onClick={() => setContentSubTab(platform.toLowerCase())}
                >
                  {platform}
                </button>
              ))}
            </div>
            
            {/* Final content - use the latest version available */}
            {(() => {
              const finalVersion = result.v5 || result.v4 || result.v3 || result.v2 || result.v1;
              if (!finalVersion) return <p>No content available.</p>;
              
              return (
                <>
                  {contentSubTab === "linkedin" && (
                    <div className="content-section">
                      <div className="linkedin-preview-compact">
                        <div className="linkedin-header-compact">
                          <div className="avatar-sm">YU</div>
                          <div className="user-info-compact">
                            <span className="user-name">Your Name</span>
                            <span className="user-meta">Now</span>
                          </div>
                        </div>
                        <div className="linkedin-body">
                          {finalVersion?.linkedin?.content}
                        </div>
                        <div className="linkedin-actions">
                          <span>Like</span>
                          <span>Comment</span>
                          <span>Share</span>
                        </div>
                      </div>
                      <div className="action-bar">
                        <button 
                          className="btn btn-primary btn-sm"
                          onClick={() => {
                            navigator.clipboard.writeText(finalVersion?.linkedin?.content || '');
                            alert('LinkedIn post copied to clipboard!');
                          }}
                        >
                          Copy LinkedIn Post
                        </button>
                      </div>
                    </div>
                  )}
                  
                  {contentSubTab === "twitter" && (
                    <div className="content-section">
                      <div className="tweet-thread-compact">
                        {(finalVersion?.twitter?.tweets || []).map((tweet, i, arr) => (
                          <div key={i} className="tweet-item">
                            <div className="tweet-left-border"></div>
                            <div className="tweet-body">
                              <div className="tweet-meta">
                                <div className="tweet-user">
                                  <div className="avatar-xs">YU</div>
                                  <span className="user-name">Your Username</span>
                                  <span className="user-handle">@yourusername</span>
                                </div>
                                <span className="tweet-count">{i + 1}/{arr.length}</span>
                              </div>
                              <div className="tweet-text">{tweet}</div>
                            </div>
                          </div>
                        ))}
                      </div>
                      <div className="action-bar">
                        <button 
                          className="btn btn-primary btn-sm"
                          onClick={() => {
                            const threadText = (finalVersion?.twitter?.tweets || []).map((t, i) => `${i + 1}/${finalVersion?.twitter?.tweets.length} ${t}`).join('\n\n');
                            navigator.clipboard.writeText(threadText);
                            alert('Twitter thread copied to clipboard!');
                          }}
                        >
                          Copy Twitter Thread
                        </button>
                      </div>
                    </div>
                  )}
                  
                  {contentSubTab === "newsletter" && (
                    <div className="content-section">
                      <div className="newsletter-compact">
                        <div className="newsletter-accent"></div>
                        <div className="newsletter-body">
                          <div className="newsletter-meta">
                            <span className="newsletter-label">Your Newsletter</span>
                            <span className="newsletter-tagline">Curated insights delivered to your inbox</span>
                          </div>
                          <div className="newsletter-text" dangerouslySetInnerHTML={{ 
                            __html: formatNewsletterContent(finalVersion?.newsletter?.content || '')
                          }} />
                        </div>
                      </div>
                      <div className="action-bar">
                        <button 
                          className="btn btn-primary btn-sm"
                          onClick={() => {
                            navigator.clipboard.writeText(finalVersion?.newsletter?.content || '');
                            alert('Newsletter copied to clipboard!');
                          }}
                        >
                          Copy Newsletter
                        </button>
                      </div>
                    </div>
                  )}
                </>
              );
            })()}
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