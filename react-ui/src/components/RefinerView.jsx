import AgentCard from "./AgentCard";

export default function RefinerView({ v1, v2, loading }) {
  // Handle both old (change_records) and new (changes_applied) schema
  const changeRecords = v2.changes_applied || v2.change_records || [];
  const changesMade = v2.changes_made || [];
  const addressedIssues = v2.addressed_issues || [];
  
  return (
    <AgentCard
      title="Agent 4: Refiner"
      subtitle="Targeted improvements with traceability"
      status={loading ? "running" : "complete"}
    >
      <div className="feedback-loop">Reviewer → Refiner → Updated Output</div>

      <div className="split-grid">
        <div className="card inset">
          <h4>Version 1 (Before)</h4>
          <p>{v1.linkedin?.body || 'N/A'}</p>
        </div>
        <div className="card inset">
          <h4>Version 2 (After)</h4>
          <p>{v2.linkedin?.body || 'N/A'}</p>
        </div>
      </div>

      {changeRecords.length > 0 && (
        <div className="badge-group">
          <h4>Change Records (Traceable)</h4>
          <div className="change-records">
            {changeRecords.map((change, idx) => (
              <div key={idx} className="change-record">
                <div className="change-header">
                  <span className={`pill ${change.action === 'add' || change.action === 'added' ? 'success' : 'info'}`}>
                    {(change.action || 'MODIFY').toUpperCase()}
                  </span>
                  <span className="change-location">{(change.target || change.location || '').replace('_', ' ')}</span>
                  <span className="change-issue">[{change.issue_id}]</span>
                </div>
                <p>{change.description || change.change_type}</p>
                {(change.related_key_point || change.source_insight_id) && (
                  <span className="insight-ref">Source: {change.related_key_point || change.source_insight_id}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {changesMade.length > 0 && (
        <div className="badge-group">
          <h4>Changes Summary</h4>
          {changesMade.map((item, idx) => (
            <span className="pill success" key={idx}>{item}</span>
          ))}
        </div>
      )}

      {addressedIssues.length > 0 && (
        <div className="badge-group">
          <h4>Addressed Issues</h4>
          {addressedIssues.map((item, idx) => (
            <span className="pill info" key={idx}>{item}</span>
          ))}
        </div>
      )}

      <details>
        <summary>JSON View</summary>
        <pre>{JSON.stringify(v2, null, 2)}</pre>
      </details>
    </AgentCard>
  );
}
