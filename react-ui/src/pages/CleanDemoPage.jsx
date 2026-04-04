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
                  <div className="avatar">CF</div>
                  <div className="user-info">
                    <h4>ContentForge</h4>
                    <p className="timestamp">AI Content Creator • 2d</p>
                  </div>
                  <button className="follow-btn">+ Follow</button>
                </div>
                <div className="linkedin-content">
                  {result.v2?.linkedin?.content || result.v1?.linkedin?.content}
                </div>
                <div className="linkedin-engagement-info">
                  <span className="reaction-info">Aman Goswami and 34 others</span>
                  <div className="engagement-stats">
                    <span>10 comments</span>
                    <span>•</span>
                    <span>1 repost</span>
                  </div>
                </div>
                <div className="engagement">
                  <span className="engagement-btn">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M19.46 11l-3.91-3.91a7 7 0 01-1.69-2.74l-.49-1.47A2.76 2.76 0 0010.76 1 2.75 2.75 0 008 3.74v1.12a9.19 9.19 0 00.46 2.85L8.89 9H4.12A2.12 2.12 0 002 11.12a2.16 2.16 0 00.92 1.76A2.11 2.11 0 002 14.62a2.14 2.14 0 001.28 2 2 2 0 00-.28 1 2.12 2.12 0 002 2.12v.14A2.12 2.12 0 007.12 22h7.49a8.08 8.08 0 003.58-.84l.31-.16H21V11zM19 19h-1l-.73.37a6.14 6.14 0 01-2.69.63H7.72a1 1 0 01-1-.72l-.25-.87-.85-.41A1 1 0 015 17l.17-1-.76-.74A1 1 0 014.27 14l.66-1.09-.73-1.1a.49.49 0 01.08-.7.48.48 0 01.34-.11h7.05l-1.31-3.92A7 7 0 0110 4.86V3.75a.77.77 0 01.75-.75.75.75 0 01.71.51L12 5a9 9 0 002.13 3.5l4.5 4.5H19z"></path></svg>
                    Like
                  </span>
                  <span className="engagement-btn">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M7 9h10v1H7zm0 4h7v-1H7z" opacity=".6"></path><path d="M20.5 2h-17A1.5 1.5 0 002 3.5v13A1.5 1.5 0 003.5 18H5v3l6.29-3H20.5a1.5 1.5 0 001.5-1.5v-13A1.5 1.5 0 0020.5 2zM20 16.5a.5.5 0 01-.5.5h-11l-1.86.93L6 18.12V17H3.5a.5.5 0 01-.5-.5v-13a.5.5 0 01.5-.5h17a.5.5 0 01.5.5z"></path></svg>
                    Comment
                  </span>
                  <span className="engagement-btn">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M23 12l-4.61 7H16l4-6H8a3 3 0 01-3-3V4h2v5a1 1 0 001 1h12l-4-6h2.39z"></path></svg>
                    Repost
                  </span>
                  <span className="engagement-btn">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M21 3L0 10l7.66 4.26L16 8l-6.26 8.34L14 24z"></path></svg>
                    Send
                  </span>
                </div>
              </div>
            )}
            
            {contentSubTab === "twitter" && (
              <div className="tweet-thread">
                {(result.v2?.twitter?.tweets || result.v1?.twitter?.tweets || []).map((tweet, i, arr) => (
                  <div key={i} className="tweet-wrapper">
                    <div className="tweet-card">
                      <div className="tweet-header">
                        <div className="tweet-avatar-wrapper">
                          <div className="avatar threads-avatar">CF</div>
                          {i < arr.length - 1 && <div className="thread-line"></div>}
                        </div>
                        <div className="tweet-main-content">
                          <div className="tweet-user-header">
                            <div className="user-info">
                              <h4>ContentForge</h4>
                              <span className="verified-badge">✓</span>
                              <p className="timestamp">@contentforge • 2h</p>
                            </div>
                            <button className="tweet-menu-btn">⋯</button>
                          </div>
                          <div className="tweet-number-badge">{i + 1}/{arr.length}</div>
                          <div className="tweet-content">{tweet}</div>
                          <div className="tweet-actions">
                            <button className="action-btn">
                              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"></path></svg>
                            </button>
                            <button className="action-btn">
                              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17 1l4 4-4 4"></path><path d="M3 11V9a4 4 0 014-4h14"></path><path d="M7 23l-4-4 4-4"></path><path d="M21 13v2a4 4 0 01-4 4H3"></path></svg>
                            </button>
                            <button className="action-btn">
                              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"></path></svg>
                            </button>
                            <button className="action-btn">
                              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"></path><polyline points="16 6 12 2 8 6"></polyline><line x1="12" y1="2" x2="12" y2="15"></line></svg>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            {contentSubTab === "newsletter" && (
              <div className="newsletter-preview">
                <div className="newsletter-header">
                  <div className="newsletter-branding">
                    <div className="newsletter-icon">📧</div>
                    <div>
                      <h2 className="newsletter-title">ContentForge Newsletter</h2>
                      <p className="newsletter-subtitle">Curated insights • Issue #42 • Today</p>
                    </div>
                  </div>
                </div>
                <div className="newsletter-content">
                  <div className="newsletter-greeting">Hello Reader,</div>
                  <div dangerouslySetInnerHTML={{ 
                    __html: formatNewsletterContent(result.v2?.newsletter?.content || result.v1?.newsletter?.content || '')
                  }} />
                  <div className="newsletter-footer">
                    <div className="newsletter-cta">
                      <p className="cta-text">Found this valuable? Share it with your network.</p>
                      <button className="cta-button">Forward to a Friend</button>
                    </div>
                    <div className="newsletter-signature">
                      <p>Best regards,<br/>ContentForge Team</p>
                    </div>
                  </div>
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
                {["LinkedIn", "Twitter", "ContentForge Newsletter"].map(platform => (
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
                        <div className="linkedin-preview">
                          <div className="linkedin-header">
                            <div className="avatar">CF</div>
                            <div className="user-info">
                              <h4>ContentForge</h4>
                              <p className="timestamp">AI Content Creator • 2d</p>
                            </div>
                            <button className="follow-btn">+ Follow</button>
                          </div>
                          <div className="linkedin-content">
                            {currentVersion?.linkedin?.content}
                          </div>
                          <div className="linkedin-engagement-info">
                            <span className="reaction-info">Aman Goswami and 34 others</span>
                            <div className="engagement-stats">
                              <span>10 comments</span>
                              <span>•</span>
                              <span>1 repost</span>
                            </div>
                          </div>
                          <div className="engagement">
                            <span className="engagement-btn">
                              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M19.46 11l-3.91-3.91a7 7 0 01-1.69-2.74l-.49-1.47A2.76 2.76 0 0010.76 1 2.75 2.75 0 008 3.74v1.12a9.19 9.19 0 00.46 2.85L8.89 9H4.12A2.12 2.12 0 002 11.12a2.16 2.16 0 00.92 1.76A2.11 2.11 0 002 14.62a2.14 2.14 0 001.28 2 2 2 0 00-.28 1 2.12 2.12 0 002 2.12v.14A2.12 2.12 0 007.12 22h7.49a8.08 8.08 0 003.58-.84l.31-.16H21V11zM19 19h-1l-.73.37a6.14 6.14 0 01-2.69.63H7.72a1 1 0 01-1-.72l-.25-.87-.85-.41A1 1 0 015 17l.17-1-.76-.74A1 1 0 014.27 14l.66-1.09-.73-1.1a.49.49 0 01.08-.7.48.48 0 01.34-.11h7.05l-1.31-3.92A7 7 0 0110 4.86V3.75a.77.77 0 01.75-.75.75.75 0 01.71.51L12 5a9 9 0 002.13 3.5l4.5 4.5H19z"></path></svg>
                              Like
                            </span>
                            <span className="engagement-btn">
                              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M7 9h10v1H7zm0 4h7v-1H7z" opacity=".6"></path><path d="M20.5 2h-17A1.5 1.5 0 002 3.5v13A1.5 1.5 0 003.5 18H5v3l6.29-3H20.5a1.5 1.5 0 001.5-1.5v-13A1.5 1.5 0 0020.5 2zM20 16.5a.5.5 0 01-.5.5h-11l-1.86.93L6 18.12V17H3.5a.5.5 0 01-.5-.5v-13a.5.5 0 01.5-.5h17a.5.5 0 01.5.5z"></path></svg>
                              Comment
                            </span>
                            <span className="engagement-btn">
                              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M23 12l-4.61 7H16l4-6H8a3 3 0 01-3-3V4h2v5a1 1 0 001 1h12l-4-6h2.39z"></path></svg>
                              Repost
                            </span>
                            <span className="engagement-btn">
                              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M21 3L0 10l7.66 4.26L16 8l-6.26 8.34L14 24z"></path></svg>
                              Send
                            </span>
                          </div>
                        </div>
                      )}
                      
                      {contentSubTab === "twitter" && (
                        <div className="tweet-thread">
                          {(currentVersion?.twitter?.tweets || []).map((tweet, i, arr) => (
                            <div key={i} className="tweet-wrapper">
                              <div className="tweet-card">
                                <div className="tweet-header">
                                  <div className="tweet-avatar-wrapper">
                                    <div className="avatar threads-avatar">CF</div>
                                    {i < arr.length - 1 && <div className="thread-line"></div>}
                                  </div>
                                  <div className="tweet-main-content">
                                    <div className="tweet-user-header">
                                      <div className="user-info">
                                        <h4>ContentForge</h4>
                                        <span className="verified-badge">✓</span>
                                        <p className="timestamp">@contentforge • 2h</p>
                                      </div>
                                      <button className="tweet-menu-btn">⋯</button>
                                    </div>
                                    <div className="tweet-number-badge">{i + 1}/{arr.length}</div>
                                    <div className="tweet-content">{tweet}</div>
                                    <div className="tweet-actions">
                                      <button className="action-btn">
                                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"></path></svg>
                                      </button>
                                      <button className="action-btn">
                                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2"><path d="M17 1l4 4-4 4"></path><path d="M3 11V9a4 4 0 014-4h14"></path><path d="M7 23l-4-4 4-4"></path><path d="M21 13v2a4 4 0 01-4 4H3"></path></svg>
                                      </button>
                                      <button className="action-btn">
                                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"></path></svg>
                                      </button>
                                      <button className="action-btn">
                                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"></path><polyline points="16 6 12 2 8 6"></polyline><line x1="12" y1="2" x2="12" y2="15"></line></svg>
                                      </button>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                      
                      {contentSubTab === "newsletter" && (
                        <div className="newsletter-preview">
                          <div className="newsletter-header">
                            <div className="newsletter-branding">
                              <div className="newsletter-icon">📧</div>
                              <div>
                                <h2 className="newsletter-title">ContentForge Newsletter</h2>
                                <p className="newsletter-subtitle">Curated insights • Issue #42 • Today</p>
                              </div>
                            </div>
                          </div>
                          <div className="newsletter-content">
                            <div className="newsletter-greeting">Hello Reader,</div>
                            <div dangerouslySetInnerHTML={{ 
                              __html: formatNewsletterContent(currentVersion?.newsletter?.content || '')
                            }} />
                            <div className="newsletter-footer">
                              <div className="newsletter-cta">
                                <p className="cta-text">Found this valuable? Share it with your network.</p>
                                <button className="cta-button">Forward to a Friend</button>
                              </div>
                              <div className="newsletter-signature">
                                <p>Best regards,<br/>ContentForge Team</p>
                              </div>
                            </div>
                          </div>
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
            
            {/* Final content with better styling */}
            {(() => {
              const finalVersion = result.v5 || result.v4 || result.v3 || result.v2 || result.v1;
              if (!finalVersion) return <p>No content available.</p>;
              
              return (
                <>
                  {contentSubTab === "linkedin" && (
                    <div className="content-section">
                      <div className="linkedin-preview-compact">
                        <div className="linkedin-header-compact">
                          <div className="avatar-sm">CF</div>
                          <div className="user-info-compact">
                            <span className="user-name">ContentForge</span>
                            <span className="user-meta">AI Content Creator • 2d</span>
                          </div>
                          <button className="follow-btn-sm">+ Follow</button>
                        </div>
                        <div className="linkedin-content-compact">
                          {finalVersion?.linkedin?.content}
                        </div>
                        <div className="linkedin-engagement-info-compact">
                          <span className="reaction-info-sm">Aman Goswami and 34 others</span>
                        </div>
                        <div className="engagement-compact">
                          <span>👍 Like</span>
                          <span>💬 Comment</span>
                          <span>🔄 Repost</span>
                          <span>📤 Send</span>
                        </div>
                      </div>
                      <div className="action-bar" style={{ marginTop: '16px' }}>
                        <button 
                          className="btn btn-primary"
                          onClick={() => {
                            navigator.clipboard.writeText(finalVersion?.linkedin?.content || '');
                            alert('LinkedIn post copied to clipboard!');
                          }}
                        >
                          📋 Copy LinkedIn Post
                        </button>
                      </div>
                    </div>
                  )}
                  
                  {contentSubTab === "twitter" && (
                    <div className="content-section">
                      <div className="tweet-thread-compact">
                        {(finalVersion?.twitter?.tweets || []).map((tweet, i, arr) => (
                          <div key={i} className="tweet-wrapper-compact">
                            <div className="tweet-card-compact">
                              <div className="tweet-header-compact">
                                <div className="tweet-header-top">
                                  <div className="tweet-user-section">
                                    <span className="user-name">ContentForge</span>
                                    <span className="verified-badge-sm">✓</span>
                                    <span className="user-handle">@contentforge • 2h</span>
                                  </div>
                                  <button className="tweet-menu-btn-sm">⋯</button>
                                </div>
                                <span className="tweet-number-badge-sm">{i + 1}/{arr.length}</span>
                              </div>
                              <div className="tweet-body-compact">
                                <div className="avatar-xs">CF</div>
                                <div className="tweet-content-wrapper">
                                  <div className="tweet-content-compact">{tweet}</div>
                                  <div className="tweet-actions-compact">
                                    <button className="action-btn-sm">
                                      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"></path>
                                      </svg>
                                    </button>
                                    <button className="action-btn-sm">
                                      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M17 1l4 4-4 4M3 11V9a4 4 0 014-4h14M7 23l-4-4 4-4M21 13v2a4 4 0 01-4 4H3"></path>
                                      </svg>
                                    </button>
                                    <button className="action-btn-sm">
                                      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"></path>
                                      </svg>
                                    </button>
                                    <button className="action-btn-sm">
                                      <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8M16 6l-4-4-4 4M12 2v13"></path>
                                      </svg>
                                    </button>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                      <div className="action-bar" style={{ marginTop: '16px' }}>
                        <button 
                          className="btn btn-primary"
                          onClick={() => {
                            const threadText = (finalVersion?.twitter?.tweets || []).map((t, i) => `${i + 1}/${finalVersion?.twitter?.tweets.length} ${t}`).join('\n\n');
                            navigator.clipboard.writeText(threadText);
                            alert('Twitter thread copied to clipboard!');
                          }}
                        >
                          📋 Copy Twitter Thread
                        </button>
                      </div>
                    </div>
                  )}
                  
                  {contentSubTab === "newsletter" && (
                    <div className="content-section">
                      <div className="newsletter-preview-compact">
                        <div className="newsletter-header-compact">
                          <div className="newsletter-icon-sm">📧</div>
                          <div>
                            <h3 className="newsletter-title-compact">ContentForge Newsletter</h3>
                            <p className="newsletter-subtitle-compact">Curated insights • Issue #42 • Today</p>
                          </div>
                        </div>
                        <div className="newsletter-content-compact">
                          <div className="newsletter-greeting-sm">Hello Reader,</div>
                          <div dangerouslySetInnerHTML={{ 
                            __html: formatNewsletterContent(finalVersion?.newsletter?.content || '')
                          }} />
                        </div>
                      </div>
                      <div className="action-bar" style={{ marginTop: '16px' }}>
                        <button 
                          className="btn btn-primary"
                          onClick={() => {
                            navigator.clipboard.writeText(finalVersion?.newsletter?.content || '');
                            alert('ContentForge Newsletter copied to clipboard!');
                          }}
                        >
                          📋 Copy Newsletter
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