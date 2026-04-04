export default function ArchitecturePage() {
  // SVG Icon Components
  const DocumentIcon = () => (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
      <polyline points="14 2 14 8 20 8"></polyline>
      <line x1="16" y1="13" x2="8" y2="13"></line>
      <line x1="16" y1="17" x2="8" y2="17"></line>
      <polyline points="10 9 9 9 8 9"></polyline>
    </svg>
  );

  const SparklesIcon = () => (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
      <path d="M12 3L13.5 7.5L18 9L13.5 10.5L12 15L10.5 10.5L6 9L10.5 7.5L12 3Z" fill="#f59e0b" stroke="#f59e0b" strokeWidth="1.5"/>
      <path d="M19 14L19.5 15.5L21 16L19.5 16.5L19 18L18.5 16.5L17 16L18.5 15.5L19 14Z" fill="#f59e0b" stroke="#f59e0b" strokeWidth="1.5"/>
    </svg>
  );

  const ClipboardIcon = () => (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
      <rect x="8" y="2" width="8" height="4" rx="1" fill="#f97316" stroke="#f97316" strokeWidth="1.5"/>
      <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" stroke="#f97316" strokeWidth="1.5" fill="none"/>
      <line x1="9" y1="11" x2="15" y2="11" stroke="#f97316" strokeWidth="1.5"/>
      <line x1="9" y1="15" x2="15" y2="15" stroke="#f97316" strokeWidth="1.5"/>
    </svg>
  );

  const ShieldIcon = () => (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="#3b82f6" stroke="#3b82f6" strokeWidth="1.5"/>
    </svg>
  );

  const DiamondIcon = () => (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
      <path d="M2.7 10.3l8.5 11.7c.4.5 1.2.5 1.6 0l8.5-11.7c.3-.4.2-.9-.1-1.2l-5-5c-.3-.3-.7-.5-1.1-.5H9.9c-.4 0-.8.2-1.1.5l-5 5c-.3.3-.4.8-.1 1.2z" fill="#06b6d4" stroke="#06b6d4" strokeWidth="1.5"/>
    </svg>
  );

  const RocketIcon = () => (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
      <path d="M9 11l3 3L22 4 9 11z" fill="#ef4444" stroke="#ef4444" strokeWidth="1.5"/>
      <path d="M22 4l-7 18-3-9-9-3L22 4z" fill="#ef4444" stroke="#ef4444" strokeWidth="1.5"/>
    </svg>
  );

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(180deg, #fafafa 0%, #ffffff 100%)', paddingBottom: '80px' }}>
      {/* Hero Section */}
      <section style={{ padding: '80px 24px 40px', textAlign: 'center' }}>
        <p style={{ 
          fontSize: '11px', 
          fontWeight: '700', 
          textTransform: 'uppercase', 
          letterSpacing: '0.15em', 
          color: '#3b82f6', 
          marginBottom: '16px' 
        }}>
          MULTI-AGENT CONTENT REPURPOSING SYSTEM
        </p>
        <h1 style={{ 
          fontSize: '3.5rem', 
          fontWeight: '700', 
          color: '#111827', 
          marginBottom: '20px',
          letterSpacing: '-0.02em'
        }}>
          System Architecture
        </h1>
        <p style={{ 
          fontSize: '1.125rem', 
          lineHeight: '1.75', 
          color: '#6b7280', 
          maxWidth: '700px', 
          margin: '0 auto' 
        }}>
          A structured multi-agent pipeline that transforms long-form content into high-quality, platform-ready outputs.
        </p>
      </section>

      {/* Pipeline Diagram */}
      <section style={{ padding: '40px 24px', maxWidth: '1400px', margin: '0 auto' }}>
        <div style={{ 
          background: '#f8f9fb', 
          border: '1px solid #e5e7eb', 
          borderRadius: '20px', 
          padding: '60px 40px',
          position: 'relative'
        }}>
          {/* Pipeline Flow */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'relative', marginBottom: '100px' }}>
            {/* Input */}
            <div style={{ textAlign: 'center', flex: '0 0 auto', zIndex: 2 }}>
              <div style={{ 
                width: '90px', 
                height: '90px', 
                background: '#fff', 
                borderRadius: '16px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                margin: '0 auto 12px'
              }}>
                <DocumentIcon />
              </div>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#111827', marginBottom: '4px' }}>Input</div>
              <div style={{ fontSize: '11px', color: '#9ca3af', maxWidth: '100px' }}>Long-form content ingestion</div>
            </div>

            <div style={{ width: '40px', height: '2px', background: '#d1d5db', flex: '0 0 auto' }}></div>

            {/* Summarizer */}
            <div style={{ textAlign: 'center', flex: '0 0 auto', zIndex: 2 }}>
              <div style={{ 
                width: '90px', 
                height: '90px', 
                background: '#fff', 
                borderRadius: '16px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                margin: '0 auto 12px'
              }}>
                <SparklesIcon />
              </div>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#111827', marginBottom: '4px' }}>Summarizer</div>
              <div style={{ fontSize: '11px', color: '#9ca3af', maxWidth: '100px' }}>Extracts key insights</div>
            </div>

            <div style={{ width: '40px', height: '2px', background: '#d1d5db', flex: '0 0 auto' }}></div>

            {/* Formatter */}
            <div style={{ textAlign: 'center', flex: '0 0 auto', zIndex: 2 }}>
              <div style={{ 
                width: '90px', 
                height: '90px', 
                background: '#fff', 
                borderRadius: '16px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                margin: '0 auto 12px'
              }}>
                <ClipboardIcon />
              </div>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#111827', marginBottom: '4px' }}>Formatter</div>
              <div style={{ fontSize: '11px', color: '#9ca3af', maxWidth: '100px' }}>Structures for each platform</div>
            </div>

            <div style={{ width: '40px', height: '2px', background: '#d1d5db', flex: '0 0 auto' }}></div>

            {/* Reviewer */}
            <div style={{ textAlign: 'center', flex: '0 0 auto', position: 'relative', zIndex: 2 }}>
              <div style={{ 
                width: '90px', 
                height: '90px', 
                background: '#fff', 
                borderRadius: '16px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                margin: '0 auto 12px'
              }}>
                <ShieldIcon />
              </div>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#111827', marginBottom: '4px' }}>Reviewer</div>
              <div style={{ fontSize: '11px', color: '#9ca3af', maxWidth: '100px' }}>Validates quality & tone</div>
            </div>

            <div style={{ width: '40px', height: '2px', background: '#d1d5db', flex: '0 0 auto' }}></div>

            {/* Refiner */}
            <div style={{ textAlign: 'center', flex: '0 0 auto', zIndex: 2 }}>
              <div style={{ 
                width: '90px', 
                height: '90px', 
                background: '#fff', 
                borderRadius: '16px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                margin: '0 auto 12px'
              }}>
                <DiamondIcon />
              </div>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#111827', marginBottom: '4px' }}>Refiner</div>
              <div style={{ fontSize: '11px', color: '#9ca3af', maxWidth: '100px' }}>Polishes final output</div>
            </div>

            <div style={{ width: '40px', height: '2px', background: '#d1d5db', flex: '0 0 auto' }}></div>

            {/* Output */}
            <div style={{ textAlign: 'center', flex: '0 0 auto', zIndex: 2 }}>
              <div style={{ 
                width: '90px', 
                height: '90px', 
                background: '#fff', 
                borderRadius: '16px', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
                margin: '0 auto 12px'
              }}>
                <RocketIcon />
              </div>
              <div style={{ fontSize: '14px', fontWeight: '600', color: '#111827', marginBottom: '4px' }}>Output</div>
              <div style={{ fontSize: '11px', color: '#9ca3af', maxWidth: '100px' }}>Platform-ready content</div>
            </div>

            {/* Feedback Loop Arrow - Curved from Refiner back to Reviewer */}
            <svg 
              style={{ 
                position: 'absolute',
                bottom: '-80px',
                left: '50%',
                transform: 'translateX(-50%)',
                width: '550px',
                height: '100px',
                zIndex: 1
              }}
              viewBox="0 0 550 100"
            >
              <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
                  <polygon points="0 0, 10 3, 0 6" fill="#3b82f6" />
                </marker>
              </defs>
              {/* Curved path from Refiner (position 5) back to Reviewer (position 4) */}
              <path
                d="M 440 20 Q 440 80, 410 80 L 385 80 Q 360 80, 360 20"
                stroke="#3b82f6"
                strokeWidth="2.5"
                fill="none"
                strokeDasharray="6 4"
                markerEnd="url(#arrowhead)"
              />
            </svg>
          </div>

          {/* Feedback Loop Label */}
          <div style={{ 
            position: 'absolute',
            bottom: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            textAlign: 'center',
            maxWidth: '520px',
            zIndex: 3
          }}>
            <div style={{ 
              display: 'inline-block',
              background: '#eff6ff',
              border: '1px solid #bfdbfe',
              borderRadius: '12px',
              padding: '14px 28px'
            }}>
              <div style={{ fontSize: '13px', fontWeight: '700', color: '#3b82f6', marginBottom: '4px' }}>
                Feedback Loop
              </div>
              <div style={{ fontSize: '12px', color: '#6b7280', lineHeight: '1.5' }}>
                Refiner sends improved content back to Reviewer, iterating until no issues are encountered
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Agent Responsibilities */}
      <section style={{ padding: '60px 24px', maxWidth: '1400px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <h2 style={{ fontSize: '2.25rem', fontWeight: '700', color: '#111827', marginBottom: '12px' }}>
            Agent Responsibilities
          </h2>
          <p style={{ fontSize: '1.0625rem', color: '#6b7280' }}>
            Each agent operates autonomously with a clear mandate.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px', maxWidth: '1200px', margin: '0 auto' }}>
          {/* Summarizer Agent */}
          <div style={{ 
            background: '#fff', 
            border: '1px solid #e5e7eb', 
            borderRadius: '16px', 
            padding: '32px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
            transition: 'all 0.2s ease'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.1)';
            e.currentTarget.style.transform = 'translateY(-4px)';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)';
            e.currentTarget.style.transform = 'translateY(0)';
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
              <div style={{ 
                width: '40px', 
                height: '40px', 
                background: '#fef3c7', 
                borderRadius: '10px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <SparklesIcon />
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '700', color: '#111827', margin: 0 }}>
                Summarizer Agent
              </h3>
            </div>
            <p style={{ fontSize: '0.9375rem', lineHeight: '1.65', color: '#6b7280', marginBottom: '20px' }}>
              Distills long-form content into concise, high-signal summaries while preserving core arguments and key takeaways.
            </p>
            <div style={{ marginBottom: '12px' }}>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>INPUT</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Raw long-form content (articles, transcripts, threads)</div>
            </div>
            <div style={{ marginBottom: '12px' }}>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>PROCESS</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>NLP extraction, key-point identification, redundancy removal</div>
            </div>
            <div>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>OUTPUT</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Structured summary with ranked insights</div>
            </div>
          </div>

          {/* Formatter Agent */}
          <div style={{ 
            background: '#fff', 
            border: '1px solid #e5e7eb', 
            borderRadius: '16px', 
            padding: '32px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
            transition: 'all 0.2s ease'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.1)';
            e.currentTarget.style.transform = 'translateY(-4px)';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)';
            e.currentTarget.style.transform = 'translateY(0)';
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
              <div style={{ 
                width: '40px', 
                height: '40px', 
                background: '#fed7aa', 
                borderRadius: '10px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <ClipboardIcon />
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '700', color: '#111827', margin: 0 }}>
                Formatter Agent
              </h3>
            </div>
            <p style={{ fontSize: '0.9375rem', lineHeight: '1.65', color: '#6b7280', marginBottom: '20px' }}>
              Adapts summarized content into platform-native formats, respecting character limits, tone, and structural conventions.
            </p>
            <div style={{ marginBottom: '12px' }}>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>INPUT</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Structured summary from Summarizer</div>
            </div>
            <div style={{ marginBottom: '12px' }}>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>PROCESS</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Platform template matching, tone adjustment, length optimization</div>
            </div>
            <div>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>OUTPUT</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Platform-specific drafts (LinkedIn, Twitter, Newsletter)</div>
            </div>
          </div>

          {/* Reviewer Agent */}
          <div style={{ 
            background: '#fff', 
            border: '1px solid #e5e7eb', 
            borderRadius: '16px', 
            padding: '32px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
            transition: 'all 0.2s ease'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.1)';
            e.currentTarget.style.transform = 'translateY(-4px)';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)';
            e.currentTarget.style.transform = 'translateY(0)';
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
              <div style={{ 
                width: '40px', 
                height: '40px', 
                background: '#dbeafe', 
                borderRadius: '10px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <ShieldIcon />
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '700', color: '#111827', margin: 0 }}>
                Reviewer Agent
              </h3>
            </div>
            <p style={{ fontSize: '0.9375rem', lineHeight: '1.65', color: '#6b7280', marginBottom: '20px' }}>
              Evaluates formatted outputs against quality rubrics for clarity, accuracy, engagement, and brand consistency.
            </p>
            <div style={{ marginBottom: '12px' }}>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>INPUT</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Formatted drafts from Formatter</div>
            </div>
            <div style={{ marginBottom: '12px' }}>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>PROCESS</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Multi-criteria scoring, hallucination check, tone validation</div>
            </div>
            <div>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>OUTPUT</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Quality report with actionable feedback</div>
            </div>
          </div>

          {/* Refiner Agent */}
          <div style={{ 
            background: '#fff', 
            border: '1px solid #e5e7eb', 
            borderRadius: '16px', 
            padding: '32px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
            transition: 'all 0.2s ease'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.boxShadow = '0 8px 24px rgba(0,0,0,0.1)';
            e.currentTarget.style.transform = 'translateY(-4px)';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.04)';
            e.currentTarget.style.transform = 'translateY(0)';
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
              <div style={{ 
                width: '40px', 
                height: '40px', 
                background: '#cffafe', 
                borderRadius: '10px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <DiamondIcon />
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '700', color: '#111827', margin: 0 }}>
                Refiner Agent
              </h3>
            </div>
            <p style={{ fontSize: '0.9375rem', lineHeight: '1.65', color: '#6b7280', marginBottom: '20px' }}>
              Incorporates reviewer feedback to polish content, fix issues, and elevate quality until the threshold is met.
            </p>
            <div style={{ marginBottom: '12px' }}>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>INPUT</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Quality feedback from Reviewer</div>
            </div>
            <div style={{ marginBottom: '12px' }}>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>PROCESS</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Targeted rewriting, style refinement, final polish</div>
            </div>
            <div>
              <div style={{ fontSize: '11px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.05em', color: '#93c5fd', marginBottom: '6px' }}>OUTPUT</div>
              <div style={{ fontSize: '13px', color: '#4b5563' }}>Publication-ready content</div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ 
        borderTop: '1px solid #e5e7eb', 
        padding: '32px 24px', 
        textAlign: 'center', 
        fontSize: '12px', 
        color: '#9ca3af' 
      }}>
        Multi-Agent Content Repurposing System · Architecture Overview
      </footer>
    </div>
  );
}

