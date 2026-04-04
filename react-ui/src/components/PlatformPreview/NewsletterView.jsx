export default function NewsletterView({ newsletter, label = "Preview" }) {
  if (!newsletter || !newsletter.content) {
    return <div className="platform-card newsletter">No content available</div>;
  }

  // Parse markdown headings for better display
  const lines = newsletter.content.split('\n');
  
  return (
    <article className="platform-card newsletter">
      <div className="platform-head">
        <div>
          <strong>ContentForge Newsletter</strong>
          <span>{label}</span>
        </div>
      </div>
      <div className="platform-body">
        <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.7' }}>
          {lines.map((line, idx) => {
            if (line.startsWith('## ')) {
              return <h4 key={idx} style={{ margin: '16px 0 8px', fontSize: 16, fontWeight: 700 }}>{line.replace('## ', '')}</h4>;
            } else if (line.startsWith('# ')) {
              return <h3 key={idx} style={{ margin: '20px 0 10px', fontSize: 18, fontWeight: 700 }}>{line.replace('# ', '')}</h3>;
            } else if (line.trim()) {
              return <p key={idx} style={{ margin: '8px 0' }}>{line}</p>;
            }
            return <br key={idx} />;
          })}
        </div>
      </div>
    </article>
  );
}
