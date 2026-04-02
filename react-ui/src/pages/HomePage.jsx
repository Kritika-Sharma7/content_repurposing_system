import { useNavigate } from "react-router-dom";

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="page-stack">
      <section className="hero-grid card">
        <div>
          <h1>Multi-Agent Content Repurposing System</h1>
          <p>
            Transform long-form content into platform-ready outputs using structured AI agents
            with feedback, review, and refinement.
          </p>
          <div className="row gap-sm">
            <button className="btn btn-dark" onClick={() => navigate("/demo")}>Try Demo</button>
            <button className="btn btn-outline" onClick={() => navigate("/architecture")}>View Architecture</button>
          </div>
        </div>

        <div className="flow-col">
          <div className="flow-node">Input</div>
          <div className="flow-arrow">↓</div>
          <div className="flow-node">Summarizer</div>
          <div className="flow-arrow">↓</div>
          <div className="flow-node">Formatter</div>
          <div className="flow-arrow">↓</div>
          <div className="flow-node">Reviewer</div>
          <div className="flow-arrow">↓</div>
          <div className="flow-node">Refiner</div>
          <div className="flow-arrow">↓</div>
          <div className="flow-node final">Final Output</div>
        </div>
      </section>

      <section className="features-grid">
        <article className="card"><h3>Structured Multi-Agent Workflow</h3><p>Each role is separated with explicit input/output contracts.</p></article>
        <article className="card"><h3>Feedback-Driven Refinement Loop</h3><p>Reviewer findings directly improve final output quality.</p></article>
        <article className="card"><h3>Platform-Specific Output Rendering</h3><p>Preview content exactly how it appears per channel.</p></article>
        <article className="card"><h3>Transparent Data Flow and Versioning</h3><p>Compare V1 vs V2 with full traceability.</p></article>
      </section>

      <section className="card center-cta">
        <h2>Start Repurposing Content</h2>
        <button className="btn btn-dark" onClick={() => navigate("/demo")}>Start Demo Workspace</button>
      </section>
    </div>
  );
}
