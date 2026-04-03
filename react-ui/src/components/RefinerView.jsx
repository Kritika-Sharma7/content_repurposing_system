import AgentCard from "./AgentCard";

export default function RefinerView({ v1, v2, loading }) {
  const changeRecords = v2?.changes || [];
  const v1LinkedIn = v1?.linkedin?.content || "N/A";
  const v2LinkedIn = v2?.linkedin?.content || "N/A";
  
  return (
    <AgentCard
      title="Agent 4: Refiner"
      subtitle="Applies reviewer issues and tracks visible changes"
      status={loading ? "running" : "complete"}
    >
      <div className="feedback-loop">Reviewer → Refiner → Updated Output</div>

      <div className="split-grid">
        <div className="card inset">
          <h4>Version 1 (Before)</h4>
          <p>{v1LinkedIn}</p>
        </div>
        <div className="card inset">
          <h4>Version 2 (After)</h4>
          <p>{v2LinkedIn}</p>
        </div>
      </div>

      {changeRecords.length > 0 && (
        <div className="badge-group">
          <h4>Change Records (Traceable)</h4>
          <div className="change-records">
            {changeRecords.map((change) => (
              <div key={`${change.issue_id}-${change.target}`} className="change-record">
                <div className="change-header">
                  <span className={`pill ${change.action === "add" ? "success" : "info"}`}>
                    {(change.action || "rewrite").toUpperCase()}
                  </span>
                  <span className="change-location">{(change.target || "").replace("_", " ")}</span>
                  <span className="change-issue">[{change.issue_id}]</span>
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
