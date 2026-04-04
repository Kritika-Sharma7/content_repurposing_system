import { useNavigate } from "react-router-dom";

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="page-stack">
      <section className="hero-grid card">
        <div>
          <h1>Multi-Agent Content Repurposing System</h1>
          <p>
            Turn long-form content into high-quality, platform-ready outputs using a structured multi-agent system with review, feedback, and iterative refinement.
          </p>
          <div className="row gap-sm">
            <button className="btn btn-dark" onClick={() => navigate("/demo")}>Try Demo</button>
            <button className="btn btn-outline" onClick={() => navigate("/architecture")}>View Architecture</button>
          </div>
        </div>

        <div className="flow-col">
          <div className="flow-node">Input</div>
          <div className="flow-arrow">↓</div>
          <div className="flow-node">Summarizer (extracts key ideas)</div>
          <div className="flow-arrow">↓</div>
          <div className="flow-node">Formatter (platform-specific content)</div>
          <div className="flow-arrow">↓</div>
          <div className="flow-node">Reviewer (detects gaps & issues)</div>
          <div className="flow-arrow">↓</div>
          <div className="flow-node">Refiner (improves based on feedback)</div>
          <div className="flow-arrow">↓</div>
          <div className="flow-node final">Final Output</div>
        </div>
      </section>

      <section className="features-grid">
        <article className="card"><h3>Structured Multi-Agent Workflow</h3><p>Each agent has a clearly defined role with structured inputs and outputs, ensuring consistency and separation of responsibilities.</p></article>
        <article className="card"><h3>Feedback-Driven Refinement Loop</h3><p>Reviewer identifies gaps in content, and the refiner improves outputs based strictly on that feedback — enabling measurable iteration.</p></article>
        <article className="card"><h3>Platform-Specific Output Rendering</h3><p>Content is tailored for platforms like LinkedIn, Twitter, and newsletters while maintaining consistency across formats.</p></article>
        <article className="card"><h3>Transparent Versioning & Traceability</h3><p>Track how content evolves from V1 to V2 with clear visibility into changes and improvements across iterations.</p></article>
      </section>

      <section className="card center-cta">
        <h2>Explore the Multi-Agent Workflow</h2>
        <button className="btn btn-dark" onClick={() => navigate("/demo")}>Start Demo Workspace</button>
      </section>
    </div>
  );
}
