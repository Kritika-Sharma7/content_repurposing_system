import AgentCard from "./AgentCard";

export default function RefinerView({ v1, v2, reviewData, loading }) {
  const changeRecords = v2?.changes || [];
  const issuesFound = reviewData?.issues?.length || 0;
  const issuesFixed = changeRecords.length;

  return (
    <AgentCard
      title="Agent 4: Refiner"
      subtitle="Applied Improvements"
      status={loading ? "running" : "complete"}
    >
      <div className="feedback-loop">V1 → V2</div>

      <div className="score-grid-4">
        <div className="score-box">
          <span>Issues Found</span>
          <strong>{issuesFound}</strong>
        </div>
        <div className="score-box">
          <span>Issues Fixed</span>
          <strong>{issuesFixed}</strong>
        </div>
        <div className="score-box">
          <span>Iterations</span>
          <strong>{changeRecords.length > 0 ? changeRecords.length : 'N/A'}</strong>
        </div>
        <div className="score-box">
          <span>Status</span>
          <strong>{issuesFixed === issuesFound ? "Complete" : "Partial"}</strong>
        </div>
      </div>

      {changeRecords.length > 0 && (
        <div className="badge-group">
          <h4>Change Records (Traceable)</h4>
          <div className="change-records">
            {changeRecords.map((change, index) => (
              <div key={`change-${index}`} className="change-record">
                <div className="change-header">
                  <span className={`pill ${change.action === "add" ? "success" : "info"}`}>
                    {(change.action || "rewrite").toUpperCase()}
                  </span>
                  <span className="change-location">{(change.target || "").replace(/_/g, " ")}</span>
                </div>
                <p><strong>Before:</strong> {change.before}</p>
                <p><strong>After:</strong> {change.after}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <details>
        <summary>JSON View</summary>
        <pre>{JSON.stringify(v2 || {}, null, 2)}</pre>
      </details>
    </AgentCard>
  );
}
