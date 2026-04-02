export default function TwitterThread({ thread, label = "Preview" }) {
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
        <h4>{thread.thread_hook}</h4>
        <div className="thread-list">
          {thread.tweets.map((tweet, idx) => (
            <div className="tweet-block" key={`${idx}-${tweet.slice(0, 8)}`}>
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
