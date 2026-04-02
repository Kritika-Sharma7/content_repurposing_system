export default function AgentCard({ title, subtitle, status, children }) {
  return (
    <section className="card agent-card">
      <div className="agent-card-head">
        <div>
          <h3>{title}</h3>
          <p>{subtitle}</p>
        </div>
        {status ? <span className={`pill ${status}`}>{status}</span> : null}
      </div>
      {children}
    </section>
  );
}
