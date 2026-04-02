import { useState } from "react";
import InputPanel from "../components/InputPanel";
import SummarizerView from "../components/SummarizerView";
import FormatterView from "../components/FormatterView";
import ReviewerView from "../components/ReviewerView";
import RefinerView from "../components/RefinerView";
import VersionPanel from "../components/VersionPanel";
import LinkedInCard from "../components/PlatformPreview/LinkedInCard";
import TwitterThread from "../components/PlatformPreview/TwitterThread";
import NewsletterView from "../components/PlatformPreview/NewsletterView";
import { sampleInput } from "../data/samplePipeline";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export default function DemoPage() {
  const [inputText, setInputText] = useState("");
  const [activeStep, setActiveStep] = useState(-1);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isRunning, setIsRunning] = useState(false);

  const runWorkflow = async () => {
    const source = inputText.trim() || sampleInput;
    setInputText(source);
    setResult(null);
    setError("");
    setIsRunning(true);
    setActiveStep(0);

    const ticker = setInterval(() => {
      setActiveStep((curr) => {
        if (curr < 3) return curr + 1;
        return 0;
      });
    }, 1100);

    try {
      const response = await fetch(`${API_BASE}/api/pipeline-run`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: source,
          save_output: true,
          output_dir: "outputs",
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data?.detail || "Workflow execution failed");
      }

      setResult(data.result);
      setActiveStep(4);
    } catch (err) {
      setError(err.message || "Unable to run workflow");
      setActiveStep(-1);
    } finally {
      clearInterval(ticker);
      setIsRunning(false);
    }
  };

  return (
    <div className="page-stack">
      <InputPanel
        inputText={inputText}
        setInputText={setInputText}
        onSample={() => setInputText(sampleInput)}
        onRun={runWorkflow}
      />

      {isRunning && (
        <section className="card">
          <h3>Agent Workflow Running</h3>
          <p>Executing real backend agents. This is not mocked.</p>
          <div className="flow-row-wrap">
            <span className={`pill ${activeStep === 0 ? "running" : "complete"}`}>Summarizer</span>
            <span className={`pill ${activeStep === 1 ? "running" : "complete"}`}>Formatter</span>
            <span className={`pill ${activeStep === 2 ? "running" : "complete"}`}>Reviewer</span>
            <span className={`pill ${activeStep === 3 ? "running" : "complete"}`}>Refiner</span>
          </div>
        </section>
      )}

      {error && (
        <section className="card">
          <h3>Execution Error</h3>
          <p>{error}</p>
          <p>Check backend server status and API key in your backend environment.</p>
        </section>
      )}

      {result && (
        <section className="pipeline-stack">
          <SummarizerView
            inputText={inputText || sampleInput}
            summary={result.input_summary}
            loading={false}
          />
          <FormatterView formatted={result.version_1} loading={false} />
          <ReviewerView review={result.review} loading={false} />
          <RefinerView v1={result.version_1} v2={result.version_2} loading={false} />
        </section>
      )}

      {result && (
        <>
          {/* Score Evolution */}
          <section className="card">
            <h3>Quality Score Evolution</h3>
            <div className="score-evolution">
              {result.iterations && result.iterations.map((iter, idx) => (
                <div key={idx} className="iteration-box">
                  <span>Iteration {iter.iteration}</span>
                  <strong>{iter.score ? (iter.score * 100).toFixed(0) : 'N/A'}%</strong>
                </div>
              ))}
              <div className="iteration-box final">
                <span>Final Score</span>
                <strong>{result.final_score ? (result.final_score * 100).toFixed(0) : 'N/A'}%</strong>
              </div>
              <div className="iteration-box">
                <span>Threshold</span>
                <strong>{result.threshold_met ? '✓ Met' : '✗ Not Met'}</strong>
              </div>
            </div>
          </section>

          <VersionPanel v1={result.version_1} v2={result.version_2} />

          <section className="card">
            <h2>Final Output Showcase</h2>
            <div className="tab-grid">
              <div>
                <h4>LinkedIn Final</h4>
                <LinkedInCard post={result.version_2.linkedin} label="V2 Final" />
              </div>
              <div>
                <h4>Twitter/X Final</h4>
                <TwitterThread thread={result.version_2.twitter} label="V2 Final" />
              </div>
              <div>
                <h4>Newsletter Final</h4>
                <NewsletterView newsletter={result.version_2.newsletter} label="V2 Final" />
              </div>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
