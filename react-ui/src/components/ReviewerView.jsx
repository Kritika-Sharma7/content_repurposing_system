import AgentCard from "./AgentCard";

export default function ReviewerView({ review, loading }) {
  const issues = review?.issues || [];
  const summary = review?.summary || { total_issues: 0, critical: 0, high: 0, medium: 0 };

  return (
    <AgentCard
      title="Agent 3: Reviewer"
      subtitle="Quality Check Summary"
      status={loading ? "running" : "complete"}
    >
      <div className="score-grid-4">
        <div className="score-box">
          <span>Total Issues</span>
          <strong>{summary.total_issues}</strong>
        </div>
        <div className="score-box">
          <span>Critical</span>
          <strong>{summary.critical}</strong>
        </div>
        <div className="score-box">
          <span>High</span>
          <strong>{summary.high}</strong>
        </div>
        <div className="score-box">
          <span>Status</span>
          <strong>{review?.status === "ok" ? "Clean" : "Needs Fixes"}</strong>
        </div>
      </div>

      {issues.length > 0 && (
        <div className="badge-group">
          <h4>Issues</h4>
          {issues.map((issue, index) => (
            <div key={`issue-${index}`} className={`issue-card ${issue.priority}`}>
              <div className="issue-header">
                <span
                  className={`pill ${
                    issue.priority === "critical"
                      ? "danger"
                      : issue.priority === "high"
                      ? "danger"
                      : "warning"
                  }`}
                >
                  {issue.priority?.toUpperCase() || "MEDIUM"}
                </span>
                <span className="issue-type">{issue.type || "issue"}</span>
              </div>
              <p><strong>Problem:</strong> {issue.problem}</p>
              <p><strong>Reason:</strong> {issue.reason}</p>
              <p><strong>Suggestion:</strong> {issue.suggestion}</p>
              <div className="issue-meta">
                <span>Affects: {Array.isArray(issue.affects) ? issue.affects.join(", ") : "Multiple"}</span>
                {issue.missing_kps && issue.missing_kps.length > 0 && (
                  <span className="insight-ref">Missing: {issue.missing_kps.join(", ")}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <details>
        <summary>JSON View</summary>
        <pre>{JSON.stringify(review || {}, null, 2)}</pre>
      </details>
    </AgentCard>
  );
}
