export default function AgentCard({ title, subtitle, status, children }) {
  const getStatusDisplay = (status) => {
    if (status === 'complete') {
      return (
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: '#22c55e'
          }}></div>
          <span style={{ fontSize: 13, color: '#374151', fontWeight: 500 }}>
            Complete
          </span>
        </div>
      );
    }
    if (status === 'running') {
      return (
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <div style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: '#3b82f6'
          }}></div>
          <span style={{ fontSize: 13, color: '#374151', fontWeight: 500 }}>
            Running
          </span>
        </div>
      );
    }
    return null;
  };

  return (
    <section className="card agent-card">
      <div className="agent-card-head">
        <div>
          <h3>{title}</h3>
          <p>{subtitle}</p>
        </div>
        {getStatusDisplay(status)}
      </div>
      {children}
    </section>
  );
}
