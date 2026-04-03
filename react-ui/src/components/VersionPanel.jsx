export default function VersionPanel({ v1, v2 }) {
  if (!v1 || !v2) {
    return null;
  }

  return (
    <section className="card">
      <h3>Version Comparison</h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <details open>
          <summary style={{ fontWeight: 600, marginBottom: 12 }}>V1 - Initial Output</summary>
          <div style={{ fontSize: 13, color: '#4b5563', lineHeight: 1.8 }}>
            <p>✅ LinkedIn: {v1.linkedin?.content ? v1.linkedin.content.split(' ').length + ' words' : 'N/A'}</p>
            <p>✅ Twitter: {v1.twitter?.tweets ? v1.twitter.tweets.length + ' tweets' : 'N/A'}</p>
            <p>✅ Newsletter: {v1.newsletter?.content ? v1.newsletter.content.split(' ').length + ' words' : 'N/A'}</p>
          </div>
        </details>
        <details open>
          <summary style={{ fontWeight: 600, marginBottom: 12 }}>V2 - Refined Output</summary>
          <div style={{ fontSize: 13, color: '#4b5563', lineHeight: 1.8 }}>
            <p>✅ LinkedIn: {v2.linkedin?.content ? v2.linkedin.content.split(' ').length + ' words' : 'N/A'}</p>
            <p>✅ Twitter: {v2.twitter?.tweets ? v2.twitter.tweets.length + ' tweets' : 'N/A'}</p>
            <p>✅ Newsletter: {v2.newsletter?.content ? v2.newsletter.content.split(' ').length + ' words' : 'N/A'}</p>
            {v2.changes && v2.changes.length > 0 && (
              <p style={{ marginTop: 8, padding: 8, background: '#dcfce7', borderRadius: 6, color: '#166534', fontWeight: 500 }}>
                🔧 {v2.changes.length} improvements made
              </p>
            )}
          </div>
        </details>
      </div>
    </section>
  );
}
