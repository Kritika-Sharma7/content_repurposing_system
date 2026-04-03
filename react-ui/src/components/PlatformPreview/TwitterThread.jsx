export default function TwitterThread({ thread, label = "Preview" }) {
  if (!thread || !thread.tweets || thread.tweets.length === 0) {
    return <div className="platform-card twitter">No tweets available</div>;
  }

  return (
    <article className="platform-card twitter">
      <div className="platform-head">
        <div className="profile-line">
          <div className="avatar dark" />
          <div>
            <strong>@contentforgeai</strong>
            <span>Now · {label}</span>
          </div>
        </div>
      </div>
      <div className="platform-body">
        <div className="thread-list">
          {thread.tweets.map((tweet, idx) => (
            <div className="tweet-block" key={idx}>
              <div className="tweet-num">{idx + 1}/{thread.tweets.length}</div>
              <p>{tweet}</p>
            </div>
          ))}
        </div>
      </div>
      <div className="platform-actions dark">
        <span>Reply</span><span>Repost</span><span>Like</span><span>Share</span>
      </div>
    </article>
  );
}
