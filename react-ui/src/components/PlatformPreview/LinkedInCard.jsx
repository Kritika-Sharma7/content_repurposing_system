export default function LinkedInCard({ post, label = "Preview" }) {
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
        <h4>{post.hook}</h4>
        <p>{post.body}</p>
        <p><strong>{post.call_to_action}</strong></p>
        <div className="tag-row">
          {post.hashtags.map((tag) => (
            <span key={tag}>#{tag}</span>
          ))}
        </div>
      </div>
      <div className="platform-actions">
        <span>Like</span><span>Comment</span><span>Repost</span><span>Send</span>
      </div>
    </article>
  );
}
