import AgentCard from "./AgentCard";

export default function ReviewerView({ review, loading }) {
  const issues = review.issues || [];
  const missingPoints = review.missing_points || review.coverage_analysis?.missing_key_points || [];
  const violations = review.violations || [];
  
  // Handle both normalized (0-1) scores and legacy (1-10) scores
  const scores = review.scores || {};
  const coverage = scores.coverage !== undefined ? scores.coverage * 100 : (review.coverage_score || 0) * 10;
  const clarity = scores.clarity !== undefined ? scores.clarity * 100 : (review.clarity_score || 0) * 10;
  const engagement = scores.engagement !== undefined ? scores.engagement * 100 : (review.engagement_score || 0) * 10;
  const consistency = scores.consistency !== undefined ? scores.consistency * 100 : (review.consistency_score || 0) * 10;
  
  return (
    <AgentCard
      title="Agent 3: Reviewer"
      subtitle="Multi-dimensional evaluation with coverage analysis"
      status={loading ? "running" : "complete"}
    >
      {/* Multi-dimensional scores */}
      <div className="score-grid-4">
        <div className="score-box">
          <span>Coverage</span>
          <strong>{coverage.toFixed(0)}%</strong>
          <div className="progress"><div style={{ width: `${coverage}%` }} /></div>
        </div>
        <div className="score-box">
          <span>Clarity</span>
          <strong>{clarity.toFixed(0)}%</strong>
          <div className="progress"><div style={{ width: `${clarity}%` }} /></div>
        </div>
        <div className="score-box">
          <span>Engagement</span>
          <strong>{engagement.toFixed(0)}%</strong>
          <div className="progress"><div style={{ width: `${engagement}%` }} /></div>
        </div>
        <div className="score-box">
          <span>Consistency</span>
          <strong>{consistency.toFixed(0)}%</strong>
          <div className="progress"><div style={{ width: `${consistency}%` }} /></div>
        </div>
      </div>

      {/* Platform Fit Scores */}
      {scores.platform_fit && (
        <div className="score-grid-3">
          <div className="score-box small">
            <span>LinkedIn Fit</span>
            <strong>{(scores.platform_fit.linkedin * 100).toFixed(0)}%</strong>
          </div>
          <div className="score-box small">
            <span>Twitter Fit</span>
            <strong>{(scores.platform_fit.twitter * 100).toFixed(0)}%</strong>
          </div>
          <div className="score-box small">
            <span>Newsletter Fit</span>
            <strong>{(scores.platform_fit.newsletter * 100).toFixed(0)}%</strong>
          </div>
        </div>
      )}

      {/* Constraint Violations */}
      {violations.length > 0 && (
        <div className="badge-group">
          <h4>Constraint Violations</h4>
          {violations.map((v, idx) => (
            <div key={idx} className={`violation-item ${v.severity}`}>
              <span className={`pill ${v.severity === 'error' ? 'danger' : 'warning'}`}>
                {v.type}
              </span>
              <span>{v.message}</span>
              <span className="location">@ {v.location}</span>
            </div>
          ))}
        </div>
      )}

      {/* Missing Points Analysis */}
      {missingPoints.length > 0 && (
        <div className="badge-group">
          <h4>Missing Key Points</h4>
          {missingPoints.map((point, idx) => (
            <span className="pill danger" key={idx}>{point}</span>
          ))}
        </div>
      )}

      {/* Structured Issues */}
      {issues.length > 0 && (
        <div className="badge-group">
          <h4>Structured Issues</h4>
          {issues.map((issue) => (
            <div key={issue.id} className={`issue-card ${issue.severity}`}>
              <div className="issue-header">
                <span className={`pill ${issue.severity === 'critical' ? 'danger' : issue.severity === 'high' ? 'danger' : 'warning'}`}>
                  {issue.severity?.toUpperCase() || 'MEDIUM'}
                </span>
                <span className="issue-type">{issue.type?.replace('_', ' ') || 'issue'}</span>
                <span className="issue-id">[{issue.id}]</span>
              </div>
              <p>{issue.description}</p>
              <div className="issue-meta">
                {issue.affected_formats && <span>Affects: {issue.affected_formats.join(', ')}</span>}
                {issue.related_key_point && (
                  <span className="insight-ref">→ {issue.related_key_point}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {review.critical_issues && review.critical_issues.length > 0 && (
        <div className="badge-group">
          <h4>Critical Issues</h4>
          {review.critical_issues.map((item) => (
            <span className="pill danger" key={item}>{item}</span>
          ))}
        </div>
      )}

      {review.priority_improvements && review.priority_improvements.length > 0 && (
        <div className="badge-group">
          <h4>Priority Improvements</h4>
          {review.priority_improvements.map((item) => (
            <span className="pill warning" key={item}>{item}</span>
          ))}
        </div>
      )}

      <details>
        <summary>JSON View</summary>
        <pre>{JSON.stringify(review, null, 2)}</pre>
      </details>
    </AgentCard>
  );
}
