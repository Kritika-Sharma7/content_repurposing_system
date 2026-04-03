export default function LinkedInCard({ post, label = "Preview" }) {
  if (!post || !post.content) {
    return <div className="platform-card linkedin">No content available</div>;
  }

  return (
    <article className="platform-card linkedin">
      <div className="platform-head">
        <div className="profile-line">
          <div className="avatar" />
          <div>
            <strong>ContentForge AI</strong>
            <span>1st · just now · {label}</span>
          </div>
        </div>
      </div>
      <div className="platform-body">
        <p style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{post.content}</p>
      </div>
      <div className="platform-actions">
        <span>Like</span><span>Comment</span><span>Repost</span><span>Send</span>
      </div>
    </article>
  );
}
