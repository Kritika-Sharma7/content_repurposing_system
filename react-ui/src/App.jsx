import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import DemoPage from "./pages/DemoPage";
import NewDemoPage from "./pages/NewDemoPage";
import CleanDemoPage from "./pages/CleanDemoPage";
import ArchitecturePage from "./pages/ArchitecturePage";

function SimpleArchPage() {
  return (
    <div style={{padding: "40px", maxWidth: "900px", margin: "0 auto"}}>
      <h1 style={{textAlign: "center", marginBottom: "20px"}}>System Architecture</h1>
      <p style={{textAlign: "center", color: "#666", marginBottom: "40px"}}>
        A disciplined multi-agent pipeline that transforms long-form content into platform-specific posts.
      </p>
      
      <div style={{display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "8px", marginBottom: "24px", padding: "24px", background: "#fff", borderRadius: "12px", border: "1px solid #e5e5e5"}}>
        <div style={{padding: "16px 20px", border: "1px solid #e5e5e5", borderRadius: "10px", textAlign: "center", minWidth: "100px"}}>
          <div style={{fontSize: "24px"}}>1</div>
          <div style={{fontWeight: "600"}}>Input</div>
          <div style={{fontSize: "12px", color: "#666"}}>Long-form content</div>
        </div>
        <span style={{alignSelf: "center", color: "#999"}}>→</span>
        <div style={{padding: "16px 20px", border: "1px solid #e5e5e5", borderRadius: "10px", textAlign: "center", minWidth: "100px"}}>
          <div style={{fontSize: "24px"}}>2</div>
          <div style={{fontWeight: "600"}}>Summarizer</div>
          <div style={{fontSize: "12px", color: "#666"}}>Extract insights</div>
        </div>
        <span style={{alignSelf: "center", color: "#999"}}>→</span>
        <div style={{padding: "16px 20px", border: "1px solid #e5e5e5", borderRadius: "10px", textAlign: "center", minWidth: "100px"}}>
          <div style={{fontSize: "24px"}}>3</div>
          <div style={{fontWeight: "600"}}>Formatter</div>
          <div style={{fontSize: "12px", color: "#666"}}>Platform adapt</div>
        </div>
        <span style={{alignSelf: "center", color: "#999"}}>→</span>
        <div style={{padding: "16px 20px", border: "1px solid #e5e5e5", borderRadius: "10px", textAlign: "center", minWidth: "100px"}}>
          <div style={{fontSize: "24px"}}>4</div>
          <div style={{fontWeight: "600"}}>Reviewer</div>
          <div style={{fontSize: "12px", color: "#666"}}>Quality check</div>
        </div>
        <span style={{alignSelf: "center", color: "#999"}}>→</span>
        <div style={{padding: "16px 20px", border: "1px solid #e5e5e5", borderRadius: "10px", textAlign: "center", minWidth: "100px"}}>
          <div style={{fontSize: "24px"}}>5</div>
          <div style={{fontWeight: "600"}}>Refiner</div>
          <div style={{fontSize: "12px", color: "#666"}}>Targeted fixes</div>
        </div>
        <span style={{alignSelf: "center", color: "#999"}}>→</span>
        <div style={{padding: "16px 20px", border: "1px solid #e5e5e5", borderRadius: "10px", textAlign: "center", minWidth: "100px"}}>
          <div style={{fontSize: "24px"}}>6</div>
          <div style={{fontWeight: "600"}}>Output</div>
          <div style={{fontSize: "12px", color: "#666"}}>Ready posts</div>
        </div>
      </div>
      
      <div style={{background: "#f0f9ff", border: "1px solid #bae6fd", borderRadius: "8px", padding: "12px 20px", textAlign: "center", marginBottom: "24px", color: "#0369a1"}}>
        <strong>Feedback Loop:</strong> Reviewer and Refiner iterate until 90% quality score
      </div>
      
      <div style={{background: "#fff", border: "1px solid #e5e5e5", borderRadius: "12px", padding: "24px", marginBottom: "24px"}}>
        <h2 style={{fontSize: "1.25rem", marginBottom: "20px"}}>Agent Modules</h2>
        <div style={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px"}}>
          <div style={{border: "1px solid #e5e5e5", borderRadius: "10px", padding: "20px"}}>
            <h3 style={{margin: "0 0 4px"}}>Agent 1: Summarizer</h3>
            <div style={{fontSize: "14px", color: "#666", marginBottom: "16px"}}>Content analysis and extraction</div>
            <div style={{marginBottom: "8px"}}><strong style={{fontSize: "12px", color: "#374151"}}>INPUT</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Raw long-form text</span></div>
            <div style={{marginBottom: "8px"}}><strong style={{fontSize: "12px", color: "#374151"}}>PROCESS</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Extracts key insights and prioritizes</span></div>
            <div><strong style={{fontSize: "12px", color: "#374151"}}>OUTPUT</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Structured key_points array</span></div>
          </div>
          <div style={{border: "1px solid #e5e5e5", borderRadius: "10px", padding: "20px"}}>
            <h3 style={{margin: "0 0 4px"}}>Agent 2: Formatter</h3>
            <div style={{fontSize: "14px", color: "#666", marginBottom: "16px"}}>Platform-specific adaptation</div>
            <div style={{marginBottom: "8px"}}><strong style={{fontSize: "12px", color: "#374151"}}>INPUT</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Key points + preferences</span></div>
            <div style={{marginBottom: "8px"}}><strong style={{fontSize: "12px", color: "#374151"}}>PROCESS</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Adapts for each platform</span></div>
            <div><strong style={{fontSize: "12px", color: "#374151"}}>OUTPUT</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>LinkedIn, Twitter, Newsletter</span></div>
          </div>
          <div style={{border: "1px solid #e5e5e5", borderRadius: "10px", padding: "20px"}}>
            <h3 style={{margin: "0 0 4px"}}>Agent 3: Reviewer</h3>
            <div style={{fontSize: "14px", color: "#666", marginBottom: "16px"}}>Quality assessment</div>
            <div style={{marginBottom: "8px"}}><strong style={{fontSize: "12px", color: "#374151"}}>INPUT</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Formatted content + key points</span></div>
            <div style={{marginBottom: "8px"}}><strong style={{fontSize: "12px", color: "#374151"}}>PROCESS</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Checks coverage and compliance</span></div>
            <div><strong style={{fontSize: "12px", color: "#374151"}}>OUTPUT</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Issues list with suggestions</span></div>
          </div>
          <div style={{border: "1px solid #e5e5e5", borderRadius: "10px", padding: "20px"}}>
            <h3 style={{margin: "0 0 4px"}}>Agent 4: Refiner</h3>
            <div style={{fontSize: "14px", color: "#666", marginBottom: "16px"}}>Targeted improvements</div>
            <div style={{marginBottom: "8px"}}><strong style={{fontSize: "12px", color: "#374151"}}>INPUT</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Content + reviewer issues</span></div>
            <div style={{marginBottom: "8px"}}><strong style={{fontSize: "12px", color: "#374151"}}>PROCESS</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Applies surgical 1:1 fixes</span></div>
            <div><strong style={{fontSize: "12px", color: "#374151"}}>OUTPUT</strong><br/><span style={{fontSize: "14px", color: "#4b5563"}}>Improved content + change log</span></div>
          </div>
        </div>
      </div>
      
      <div style={{background: "#fff", border: "1px solid #e5e5e5", borderRadius: "12px", padding: "24px", marginBottom: "24px"}}>
        <h2 style={{fontSize: "1.25rem", marginBottom: "20px"}}>Design Principles</h2>
        <div style={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px"}}>
          <div style={{display: "flex", gap: "12px", padding: "12px", background: "#f9fafb", borderRadius: "8px"}}><span style={{color: "#22c55e", fontWeight: "bold"}}>OK</span><div><strong>Disciplined Workflow</strong><br/><span style={{color: "#666"}}>Each agent has a single responsibility</span></div></div>
          <div style={{display: "flex", gap: "12px", padding: "12px", background: "#f9fafb", borderRadius: "8px"}}><span style={{color: "#22c55e", fontWeight: "bold"}}>OK</span><div><strong>1:1 Issue Mapping</strong><br/><span style={{color: "#666"}}>Every issue gets exactly one fix</span></div></div>
          <div style={{display: "flex", gap: "12px", padding: "12px", background: "#f9fafb", borderRadius: "8px"}}><span style={{color: "#22c55e", fontWeight: "bold"}}>OK</span><div><strong>Quality Gates</strong><br/><span style={{color: "#666"}}>Reviewer prevents low-quality content</span></div></div>
          <div style={{display: "flex", gap: "12px", padding: "12px", background: "#f9fafb", borderRadius: "8px"}}><span style={{color: "#22c55e", fontWeight: "bold"}}>OK</span><div><strong>Platform Awareness</strong><br/><span style={{color: "#666"}}>Content adapted per platform</span></div></div>
          <div style={{display: "flex", gap: "12px", padding: "12px", background: "#f9fafb", borderRadius: "8px"}}><span style={{color: "#22c55e", fontWeight: "bold"}}>OK</span><div><strong>Convergence Control</strong><br/><span style={{color: "#666"}}>Loops terminate on quality threshold</span></div></div>
          <div style={{display: "flex", gap: "12px", padding: "12px", background: "#f9fafb", borderRadius: "8px"}}><span style={{color: "#22c55e", fontWeight: "bold"}}>OK</span><div><strong>Full Traceability</strong><br/><span style={{color: "#666"}}>Outputs trace to source</span></div></div>
        </div>
      </div>
      
      <div style={{background: "#fff", border: "1px solid #e5e5e5", borderRadius: "12px", padding: "24px"}}>
        <h2 style={{fontSize: "1.25rem", marginBottom: "20px"}}>Technical Implementation</h2>
        <div style={{display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "16px"}}>
          <div style={{background: "#f9fafb", borderRadius: "8px", padding: "16px"}}>
            <h4 style={{margin: "0 0 12px"}}>Backend</h4>
            <ul style={{margin: 0, paddingLeft: "20px", color: "#4b5563"}}><li>Python FastAPI server</li><li>Pydantic validation</li><li>OpenAI GPT integration</li><li>Mock mode</li></ul>
          </div>
          <div style={{background: "#f9fafb", borderRadius: "8px", padding: "16px"}}>
            <h4 style={{margin: "0 0 12px"}}>Frontend</h4>
            <ul style={{margin: 0, paddingLeft: "20px", color: "#4b5563"}}><li>React with Vite</li><li>CSS styling</li><li>Step-based workflow</li><li>Platform previews</li></ul>
          </div>
          <div style={{background: "#f9fafb", borderRadius: "8px", padding: "16px"}}>
            <h4 style={{margin: "0 0 12px"}}>Architecture</h4>
            <ul style={{margin: 0, paddingLeft: "20px", color: "#4b5563"}}><li>Microservice pattern</li><li>Structured data flow</li><li>Version comparison</li><li>Change tracking</li></ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="main-wrap">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/demo" element={<CleanDemoPage />} />
          <Route path="/demo-tailwind" element={<NewDemoPage />} />
          <Route path="/demo-old" element={<DemoPage />} />
          <Route path="/architecture" element={<SimpleArchPage />} />
          <Route path="/architecture-old" element={<ArchitecturePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
