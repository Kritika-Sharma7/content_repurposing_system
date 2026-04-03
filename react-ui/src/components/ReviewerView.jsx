import AgentCard from "./AgentCard";

export default function ReviewerView({ review, loading }) {
  const issues = review?.issues || [];
  const criticalIssues = issues.filter((issue) => issue.priority === "critical");
  const highIssues = issues.filter((issue) => issue.priority === "high");

  return (
    <AgentCard
      title="Agent 3: Reviewer"
      subtitle="Actionable issue-based review"
      status={loading ? "running" : "complete"}
    >
      <div className="score-grid-4">
        <div className="score-box">
          <span>Total Issues</span>
          <strong>{issues.length}</strong>
        </div>
        <div className="score-box">
          <span>Critical</span>
          <strong>{criticalIssues.length}</strong>
        </div>
        <div className="score-box">
          <span>High</span>
          <strong>{highIssues.length}</strong>
        </div>
        <div className="score-box">
          <span>Status</span>
          <strong>{issues.length > 0 ? "Needs Fixes" : "Clean"}</strong>
        </div>
      </div>

      {issues.length > 0 && (
        <div className="badge-group">
          <h4>Issues</h4>
          {issues.map((issue, index) => (
            <div key={`${issue.issue_id}-${index}`} className={`issue-card ${issue.priority}`}>
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
                <span className="issue-id">[{issue.issue_id}]</span>
              </div>
              <p><strong>Problem:</strong> {issue.problem}</p>
              <p><strong>Reason:</strong> {issue.reason}</p>
              <p><strong>Suggestion:</strong> {issue.suggestion}</p>
              <div className="issue-meta">
                <span>Affects: {issue.target}</span>
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
