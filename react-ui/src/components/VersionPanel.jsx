export default function VersionPanel({ v1, v2 }) {
  return (
    <section className="card">
      <h3>Version History</h3>
      <details open>
        <summary>v1 - Initial Output</summary>
        <p>LinkedIn hashtags: {v1.linkedin.hashtags.join(", ")}</p>
        <p>Twitter tweets: {v1.twitter.tweets.length}</p>
        <p>Newsletter sections: {v1.newsletter.body_sections.length}</p>
      </details>
      <details open>
        <summary>v2 - Refined Output</summary>
        <p>LinkedIn hashtags: {v2.linkedin.hashtags.join(", ")}</p>
        <p>Twitter tweets: {v2.twitter.tweets.length}</p>
        <p>Newsletter sections: {v2.newsletter.body_sections.length}</p>
      </details>
    </section>
  );
}
