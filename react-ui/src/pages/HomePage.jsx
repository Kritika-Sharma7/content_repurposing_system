import { useNavigate } from "react-router-dom";

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'linear-gradient(180deg, #fafafa 0%, #ffffff 100%)' }}>
      {/* Hero Section */}
      <div style={{ flex: 1, display: 'flex', maxWidth: '1360px', margin: '0 auto', width: '100%', padding: '80px 32px', gap: '100px', alignItems: 'center' }}>
        
        {/* Left Section - Hero Text */}
        <div style={{ flex: '1 1 50%', maxWidth: '620px' }}>
          <h1 style={{ 
            fontSize: '3.5rem', 
            fontWeight: '700', 
            lineHeight: '1.1', 
            marginBottom: '28px', 
            color: '#111827', 
            letterSpacing: '-0.025em',
            maxWidth: '580px'
          }}>
            Multi-Agent Content Repurposing System
          </h1>
          <p style={{ 
            fontSize: '1.125rem', 
            lineHeight: '1.75', 
            color: '#6b7280', 
            marginBottom: '14px',
            maxWidth: '580px'
          }}>
            Turn long-form content into high-quality, platform-ready outputs using a structured multi-agent workflow with feedback and refinement.
          </p>
          <p style={{ 
            fontSize: '1rem', 
            lineHeight: '1.65', 
            color: '#3b82f6', 
            marginBottom: '40px', 
            fontWeight: '500' 
          }}>
            Not just generation — a system that improves its own output.
          </p>
          
          <div style={{ display: 'flex', gap: '14px' }}>
            <button 
              onClick={() => navigate("/demo")}
              style={{
                padding: '14px 32px',
                fontSize: '15px',
                fontWeight: '600',
                color: '#fff',
                background: '#3b82f6',
                border: 'none',
                borderRadius: '10px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                transition: 'all 0.2s ease',
                boxShadow: '0 4px 14px rgba(59, 130, 246, 0.35)'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.background = '#2563eb';
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 8px 20px rgba(59, 130, 246, 0.4)';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.background = '#3b82f6';
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 14px rgba(59, 130, 246, 0.35)';
              }}
            >
              <span>Try Demo</span>
              <span style={{ fontSize: '18px' }}>→</span>
            </button>
            
            <button 
              onClick={() => navigate("/architecture")}
              style={{
                padding: '14px 32px',
                fontSize: '15px',
                fontWeight: '600',
                color: '#374151',
                background: '#fff',
                border: '1.5px solid #e5e7eb',
                borderRadius: '10px',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.borderColor = '#9ca3af';
                e.currentTarget.style.background = '#f9fafb';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.borderColor = '#e5e7eb';
                e.currentTarget.style.background = '#fff';
              }}
            >
              View Architecture
            </button>
          </div>
        </div>

        {/* Right Section - Transformation Visual */}
        <div style={{ flex: '1 1 50%', display: 'flex', alignItems: 'center', gap: '28px', position: 'relative' }}>
          
          {/* Input Card - De-emphasized */}
          <div style={{ 
            background: '#fff', 
            border: '1px solid #e5e7eb', 
            borderRadius: '16px', 
            padding: '20px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
            opacity: 0.9,
            transform: 'scale(0.95)',
            flex: '0 0 auto',
            width: '220px'
          }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '8px', 
              fontSize: '10px', 
              fontWeight: '600', 
              color: '#f97316', 
              marginBottom: '14px', 
              textTransform: 'uppercase', 
              letterSpacing: '0.8px' 
            }}>
              <span style={{ width: '6px', height: '6px', background: '#f97316', borderRadius: '50%' }}></span>
              RAW INPUT
            </div>
            <div style={{ 
              background: '#f9fafb', 
              border: '1px solid #e5e7eb', 
              borderRadius: '10px', 
              padding: '14px 16px',
              display: 'flex',
              alignItems: 'center',
              gap: '10px'
            }}>
              <span style={{ fontSize: '20px' }}>📄</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '12px', color: '#6b7280', fontWeight: '500' }}>article_draft.md</div>
                <div style={{ fontSize: '10px', color: '#9ca3af', marginTop: '2px' }}>~1,200 words</div>
              </div>
            </div>
          </div>

          {/* Transformation Arrow */}
          <div style={{ 
            display: 'flex', 
            flexDirection: 'column', 
            alignItems: 'center', 
            gap: '6px',
            flex: '0 0 auto'
          }}>
            <div style={{ 
              width: '40px', 
              height: '2px', 
              background: 'linear-gradient(90deg, #f97316 0%, #3b82f6 100%)',
              borderRadius: '2px'
            }}></div>
            <div style={{ 
              fontSize: '24px', 
              color: '#3b82f6',
              animation: 'pulse 2s ease-in-out infinite'
            }}>→</div>
            <div style={{ 
              fontSize: '9px', 
              fontWeight: '600', 
              color: '#9ca3af', 
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>Pipeline</div>
          </div>

          {/* Output Cards - Emphasized */}
          <div style={{ 
            background: 'linear-gradient(135deg, #f8faff 0%, #ffffff 100%)', 
            border: '1.5px solid #e0e7ff', 
            borderRadius: '18px', 
            padding: '22px',
            boxShadow: '0 8px 24px rgba(59, 130, 246, 0.12)',
            flex: 1,
            maxWidth: '300px'
          }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '8px', 
              fontSize: '10px', 
              fontWeight: '700', 
              color: '#3b82f6', 
              marginBottom: '16px', 
              textTransform: 'uppercase', 
              letterSpacing: '0.8px' 
            }}>
              <span style={{ width: '6px', height: '6px', background: '#3b82f6', borderRadius: '50%' }}></span>
              PLATFORM-READY
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {/* LinkedIn Card */}
              <div style={{ 
                background: '#fff', 
                border: '1px solid #e5e7eb', 
                borderRadius: '10px', 
                padding: '14px',
                boxShadow: '0 2px 6px rgba(0,0,0,0.04)',
                transition: 'all 0.2s ease',
                cursor: 'pointer'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.boxShadow = '0 6px 16px rgba(0,0,0,0.1)';
                e.currentTarget.style.transform = 'translateY(-2px)';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.boxShadow = '0 2px 6px rgba(0,0,0,0.04)';
                e.currentTarget.style.transform = 'translateY(0)';
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                  <div style={{ width: '22px', height: '22px', background: '#0a66c2', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: '13px', fontWeight: '600' }}>in</div>
                  <span style={{ fontSize: '12px', fontWeight: '600', color: '#1a1a1a' }}>LinkedIn Post</span>
                </div>
                <div style={{ height: '4px', background: '#f3f4f6', borderRadius: '2px', marginBottom: '5px' }}></div>
                <div style={{ height: '4px', background: '#f3f4f6', borderRadius: '2px', width: '75%' }}></div>
              </div>

              {/* X/Twitter Card */}
              <div style={{ 
                background: '#fff', 
                border: '1px solid #e5e7eb', 
                borderRadius: '10px', 
                padding: '14px',
                boxShadow: '0 2px 6px rgba(0,0,0,0.04)',
                transition: 'all 0.2s ease',
                cursor: 'pointer'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.boxShadow = '0 6px 16px rgba(0,0,0,0.1)';
                e.currentTarget.style.transform = 'translateY(-2px)';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.boxShadow = '0 2px 6px rgba(0,0,0,0.04)';
                e.currentTarget.style.transform = 'translateY(0)';
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                  <div style={{ width: '22px', height: '22px', background: '#000', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: '14px', fontWeight: '700' }}>𝕏</div>
                  <span style={{ fontSize: '12px', fontWeight: '600', color: '#1a1a1a' }}>X Thread</span>
                  <span style={{ fontSize: '10px', color: '#9ca3af', marginLeft: 'auto' }}>1/3</span>
                </div>
                <div style={{ height: '4px', background: '#f3f4f6', borderRadius: '2px', marginBottom: '5px', width: '90%' }}></div>
                <div style={{ height: '4px', background: '#f3f4f6', borderRadius: '2px', width: '55%' }}></div>
              </div>

              {/* Newsletter Card */}
              <div style={{ 
                background: '#fff', 
                border: '1px solid #e5e7eb', 
                borderRadius: '10px', 
                padding: '14px',
                boxShadow: '0 2px 6px rgba(0,0,0,0.04)',
                transition: 'all 0.2s ease',
                cursor: 'pointer'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.boxShadow = '0 6px 16px rgba(0,0,0,0.1)';
                e.currentTarget.style.transform = 'translateY(-2px)';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.boxShadow = '0 2px 6px rgba(0,0,0,0.04)';
                e.currentTarget.style.transform = 'translateY(0)';
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                  <div style={{ width: '22px', height: '22px', background: '#3b82f6', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: '13px' }}>✉</div>
                  <span style={{ fontSize: '12px', fontWeight: '600', color: '#1a1a1a' }}>ContentForge Newsletter</span>
                </div>
                <div style={{ height: '4px', background: '#f3f4f6', borderRadius: '2px', marginBottom: '5px' }}></div>
                <div style={{ height: '4px', background: '#f3f4f6', borderRadius: '2px', width: '80%', marginBottom: '5px' }}></div>
                <div style={{ height: '4px', background: '#f3f4f6', borderRadius: '2px', width: '65%' }}></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div style={{ background: '#fff', borderTop: '1px solid #e5e7eb', padding: '90px 32px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          {/* Section Header */}
          <div style={{ textAlign: 'center', marginBottom: '56px' }}>
            <h2 style={{ 
              fontSize: '2.25rem', 
              fontWeight: '700', 
              color: '#111827', 
              marginBottom: '12px',
              letterSpacing: '-0.02em'
            }}>
              Why This System Works
            </h2>
            <p style={{ 
              fontSize: '1.125rem', 
              color: '#6b7280', 
              maxWidth: '680px', 
              margin: '0 auto',
              lineHeight: '1.7'
            }}>
              Designed for consistency, quality, and scalable content workflows
            </p>
          </div>
          
          {/* 2x2 Grid */}
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(2, 1fr)', 
            gap: '28px',
            maxWidth: '1000px',
            margin: '0 auto'
          }}>
            {/* Card 1 */}
            <div style={{ 
              padding: '32px', 
              background: '#fafbfc', 
              borderRadius: '14px', 
              border: '1px solid #f1f3f5',
              transition: 'all 0.2s ease',
              cursor: 'default'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 12px 28px rgba(0,0,0,0.08)';
              e.currentTarget.style.borderColor = '#e5e7eb';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
              e.currentTarget.style.borderColor = '#f1f3f5';
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                <span style={{ fontSize: '18px' }}>⚙️</span>
                <h3 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#111827', margin: 0 }}>
                  Structured Multi-Agent Workflow
                </h3>
              </div>
              <p style={{ fontSize: '0.9375rem', lineHeight: '1.65', color: '#6b7280', margin: 0 }}>
                Each agent has a clearly defined role with structured inputs and outputs, ensuring consistency and separation of responsibilities.
              </p>
            </div>

            {/* Card 2 */}
            <div style={{ 
              padding: '32px', 
              background: '#fafbfc', 
              borderRadius: '14px', 
              border: '1px solid #f1f3f5',
              transition: 'all 0.2s ease',
              cursor: 'default'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 12px 28px rgba(0,0,0,0.08)';
              e.currentTarget.style.borderColor = '#e5e7eb';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
              e.currentTarget.style.borderColor = '#f1f3f5';
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                <span style={{ fontSize: '18px' }}>🔄</span>
                <h3 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#111827', margin: 0 }}>
                  Feedback-Driven Refinement Loop
                </h3>
              </div>
              <p style={{ fontSize: '0.9375rem', lineHeight: '1.65', color: '#6b7280', margin: 0 }}>
                Reviewer identifies gaps in content, and the refiner improves outputs based strictly on that feedback — enabling measurable iteration.
              </p>
            </div>

            {/* Card 3 */}
            <div style={{ 
              padding: '32px', 
              background: '#fafbfc', 
              borderRadius: '14px', 
              border: '1px solid #f1f3f5',
              transition: 'all 0.2s ease',
              cursor: 'default'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 12px 28px rgba(0,0,0,0.08)';
              e.currentTarget.style.borderColor = '#e5e7eb';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
              e.currentTarget.style.borderColor = '#f1f3f5';
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                <span style={{ fontSize: '18px' }}>📱</span>
                <h3 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#111827', margin: 0 }}>
                  Platform-Specific Output Rendering
                </h3>
              </div>
              <p style={{ fontSize: '0.9375rem', lineHeight: '1.65', color: '#6b7280', margin: 0 }}>
                Content is tailored for platforms like LinkedIn, Twitter, and newsletters while maintaining consistency across formats.
              </p>
            </div>

            {/* Card 4 */}
            <div style={{ 
              padding: '32px', 
              background: '#fafbfc', 
              borderRadius: '14px', 
              border: '1px solid #f1f3f5',
              transition: 'all 0.2s ease',
              cursor: 'default'
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 12px 28px rgba(0,0,0,0.08)';
              e.currentTarget.style.borderColor = '#e5e7eb';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
              e.currentTarget.style.borderColor = '#f1f3f5';
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                <span style={{ fontSize: '18px' }}>📊</span>
                <h3 style={{ fontSize: '1.125rem', fontWeight: '700', color: '#111827', margin: 0 }}>
                  Transparent Versioning & Traceability
                </h3>
              </div>
              <p style={{ fontSize: '0.9375rem', lineHeight: '1.65', color: '#6b7280', margin: 0 }}>
                Track how content evolves from V1 to V2 with clear visibility into changes and improvements across iterations.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
