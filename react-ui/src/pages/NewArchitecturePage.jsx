export default function NewArchitecturePage() {
  const pipelineSteps = [
    { icon: "1", title: "Input", description: "Long-form content" },
    { icon: "2", title: "Summarizer", description: "Extract key insights" },
    { icon: "3", title: "Formatter", description: "Platform adaptation" },
    { icon: "4", title: "Reviewer", description: "Quality assessment" },
    { icon: "5", title: "Refiner", description: "Targeted fixes" },
    { icon: "6", title: "Output", description: "Ready-to-post content" },
  ];

  const agents = [
    {
      num: 1,
      title: "Summarizer",
      subtitle: "Content analysis and extraction",
      input: "Raw long-form text (blog post, article, transcript)",
      process: "Extracts key insights, identifies themes, and prioritizes points by importance",
      output: "Structured key_points array with priorities and semantic IDs",
    },
    {
      num: 2,
      title: "Formatter",
      subtitle: "Platform-specific adaptation",
      input: "Key points plus user preferences (tone, audience)",
      process: "Adapts content for each platform constraints and best practices",
      output: "LinkedIn post, Twitter thread, Newsletter draft",
    },
    {
      num: 3,
      title: "Reviewer",
      subtitle: "Quality assessment",
      input: "Formatted content plus original key points",
      process: "Checks coverage, clarity, consistency, and platform compliance",
      output: "Issues list with severity, location, and suggestions",
    },
    {
      num: 4,
      title: "Refiner",
      subtitle: "Targeted improvements",
      input: "Content plus reviewer issues",
      process: "Applies surgical 1:1 fixes for each issue without over-editing",
      output: "Improved content plus detailed change log",
    },
  ];

  const principles = [
    { title: "Disciplined Workflow", description: "Each agent has a single, focused responsibility" },
    { title: "1:1 Issue Mapping", description: "Every issue gets exactly one fix for traceability" },
    { title: "Quality Gates", description: "Reviewer prevents low-quality content from passing" },
    { title: "Platform Awareness", description: "Content adapted for LinkedIn, Twitter, newsletter formats" },
    { title: "Convergence Control", description: "Feedback loops terminate when quality threshold is met" },
    { title: "Full Traceability", description: "Every output traces back to source via semantic IDs" },
  ];

  return (
    <div className="arch-page">
      <div className="arch-container">
        <header className="arch-header">
          <h1>System Architecture</h1>
          <p>A disciplined multi-agent pipeline that transforms long-form content into platform-specific posts through extraction, formatting, review, and refinement.</p>
        </header>

        <section className="arch-section">
          <div className="pipeline">
            {pipelineSteps.map(function(step, index) {
              return (
                <div key={step.title} className="pipeline-row">
                  <div className="pipeline-step">
                    <span className="pipeline-icon">{step.icon}</span>
                    <span className="pipeline-title">{step.title}</span>
                    <span className="pipeline-desc">{step.description}</span>
                  </div>
                  {index < pipelineSteps.length - 1 ? (
                    <span className="pipeline-arrow">-&gt;</span>
                  ) : null}
                </div>
              );
            })}
          </div>
        </section>

        <div className="feedback-loop">
          <span className="feedback-icon">*</span>
          <span className="feedback-text">
            <strong>Feedback Loop:</strong> Reviewer and Refiner iterate until 90% quality score
          </span>
        </div>

        <section className="arch-section">
          <h2 className="section-title">Agent Modules</h2>
          <div className="agents-grid">
            {agents.map(function(agent) {
              return (
                <div key={agent.num} className="agent-card">
                  <div className="agent-header">
                    <h3>Agent {agent.num}: {agent.title}</h3>
                    <span className="agent-subtitle">{agent.subtitle}</span>
                  </div>
                  <div className="agent-body">
                    <div className="agent-row">
                      <span className="agent-label">Input</span>
                      <span className="agent-value">{agent.input}</span>
                    </div>
                    <div className="agent-row">
                      <span className="agent-label">Process</span>
                      <span className="agent-value">{agent.process}</span>
                    </div>
                    <div className="agent-row">
                      <span className="agent-label">Output</span>
                      <span className="agent-value">{agent.output}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        <section className="arch-section">
          <h2 className="section-title">Design Principles</h2>
          <div className="principles-list">
            {principles.map(function(p) {
              return (
                <div key={p.title} className="principle-item">
                  <span className="principle-check">OK</span>
                  <div className="principle-content">
                    <strong>{p.title}</strong>
                    <span>{p.description}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        <section className="arch-section">
          <h2 className="section-title">Technical Implementation</h2>
          <div className="tech-grid">
            <div className="tech-card">
              <h4>Backend</h4>
              <ul>
                <li>Python FastAPI server</li>
                <li>Pydantic schema validation</li>
                <li>OpenAI GPT integration</li>
                <li>Mock mode for development</li>
              </ul>
            </div>
            <div className="tech-card">
              <h4>Frontend</h4>
              <ul>
                <li>React with Vite</li>
                <li>CSS-based styling</li>
                <li>Step-based workflow UI</li>
                <li>Platform preview components</li>
              </ul>
            </div>
            <div className="tech-card">
              <h4>Architecture</h4>
              <ul>
                <li>Microservice agent pattern</li>
                <li>Structured data flow</li>
                <li>Version comparison</li>
                <li>Change tracking system</li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}