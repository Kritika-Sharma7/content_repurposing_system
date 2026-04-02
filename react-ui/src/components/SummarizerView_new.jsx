import { useState } from "react";
import AgentCard from "./AgentCard";

export default function SummarizerView({ inputText, summary, loading }) {
  const [showJson, setShowJson] = useState(false);

  const keyPoints = summary.key_points || [];
  const contentDna = summary.content_dna || null;
  const relationships = summary.relationships || [];
  const summaryQuality = summary.summary_quality || null;
  const wordCount = summary.word_count_original || (inputText ? inputText.split(/\s+/).filter(Boolean).length : 0);

  // Get importance color
  const getImportanceStyle = (importance) => {
    const styles = {
      critical: { bg: "#fef2f2", color: "#b91c1c", border: "#fecaca" },
      high: { bg: "#fff7ed", color: "#c2410c", border: "#fed7aa" },
      medium: { bg: "#eff6ff", color: "#1d4ed8", border: "#bfdbfe" },
      supporting: { bg: "#f9fafb", color: "#4b5563", border: "#e5e7eb" }
    };
    return styles[importance] || styles.medium;
  };

  // Get type icon and color
  const getTypeStyle = (type) => {
    const styles = {
      insight: { icon: "💡", bg: "#f5f3ff", color: "#7c3aed" },
      data_point: { icon: "📊", bg: "#eff6ff", color: "#2563eb" },
      strategy: { icon: "⚡", bg: "#ecfdf5", color: "#059669" },
      observation: { icon: "👁", bg: "#fefce8", color: "#ca8a04" }
    };
    return styles[type] || styles.insight;
  };

  return (
    <AgentCard
      title="Agent 1: Summarizer"
      subtitle="Content DNA Extraction"
      status={loading ? "running" : "complete"}
    >
      {/* Word count and JSON toggle */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <span style={{ fontSize: 13, color: "#6b7280" }}>{wordCount} words analyzed</span>
        <button
          onClick={() => setShowJson(!showJson)}
          style={{
            padding: "6px 12px",
            borderRadius: 8,
            border: "1px solid #e5e7eb",
            background: showJson ? "#2563eb" : "#f9fafb",
            color: showJson ? "#fff" : "#374151",
            fontSize: 13,
            fontWeight: 500,
            cursor: "pointer"
          }}
        >
          {showJson ? "Hide JSON" : "Show JSON"}
        </button>
      </div>

      {/* Content DNA Card */}
      <div style={{
        background: "linear-gradient(135deg, #eff6ff 0%, #f5f3ff 100%)",
        borderRadius: 12,
        border: "1px solid #c7d2fe",
        padding: 16,
        marginBottom: 20
      }}>
        <h4 style={{ margin: "0 0 12px 0", color: "#3730a3", fontSize: 14, fontWeight: 700 }}>
          🧬 Content DNA
        </h4>
        
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          <div>
            <span style={{ fontSize: 11, color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Intent</span>
            <p style={{ margin: "4px 0 0", fontWeight: 600, color: "#1f2937", textTransform: "capitalize" }}>{summary.intent}</p>
          </div>
          <div>
            <span style={{ fontSize: 11, color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Tone</span>
            <p style={{ margin: "4px 0 0", fontWeight: 600, color: "#1f2937", textTransform: "capitalize" }}>{summary.tone}</p>
          </div>
          <div>
            <span style={{ fontSize: 11, color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Structure</span>
            <p style={{ margin: "4px 0 0", fontWeight: 600, color: "#1f2937", textTransform: "capitalize" }}>{summary.structure?.replace("-", " ")}</p>
          </div>
          <div>
            <span style={{ fontSize: 11, color: "#6b7280", textTransform: "uppercase", letterSpacing: "0.5px" }}>Audience</span>
            <p style={{ margin: "4px 0 0", fontWeight: 600, color: "#1f2937" }}>{summary.target_audience}</p>
          </div>
        </div>

        {/* Deep DNA */}
        {contentDna && (contentDna.core_conflict || contentDna.key_question) && (
          <div style={{ marginTop: 12, paddingTop: 12, borderTop: "1px solid rgba(199, 210, 254, 0.5)" }}>
            {contentDna.core_conflict && (
              <div style={{ background: "rgba(255,255,255,0.6)", borderRadius: 8, padding: 10, marginBottom: 8 }}>
                <span style={{ fontSize: 11, color: "#6b7280" }}>Core Conflict</span>
                <p style={{ margin: "4px 0 0", fontSize: 13, fontWeight: 500, color: "#1f2937" }}>{contentDna.core_conflict}</p>
              </div>
            )}
            {contentDna.key_question && (
              <div style={{ background: "rgba(255,255,255,0.6)", borderRadius: 8, padding: 10 }}>
                <span style={{ fontSize: 11, color: "#6b7280" }}>Key Question</span>
                <p style={{ margin: "4px 0 0", fontSize: 13, fontWeight: 500, color: "#1f2937" }}>{contentDna.key_question}</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Quality Score */}
      {summaryQuality && summaryQuality.score && (
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: 12,
          background: "#f9fafb",
          borderRadius: 10,
          marginBottom: 20
        }}>
          <span style={{
            fontSize: 18,
            fontWeight: 700,
            padding: "6px 12px",
            borderRadius: 8,
            background: summaryQuality.score >= 8 ? "#dcfce7" : summaryQuality.score >= 6 ? "#fef9c3" : "#fee2e2",
            color: summaryQuality.score >= 8 ? "#166534" : summaryQuality.score >= 6 ? "#854d0e" : "#991b1b"
          }}>
            {summaryQuality.score}/10
          </span>
          <span style={{ fontSize: 13, color: "#4b5563" }}>{summaryQuality.reason}</span>
        </div>
      )}

      {/* Core Message */}
      {summary.core_message && (
        <div style={{ padding: 12, background: "#f9fafb", borderRadius: 10, marginBottom: 20 }}>
          <span style={{ fontSize: 11, color: "#6b7280", textTransform: "uppercase" }}>Core Message</span>
          <p style={{ margin: "6px 0 0", fontWeight: 500, color: "#1f2937" }}>{summary.core_message}</p>
        </div>
      )}

      {/* Key Points */}
      <div style={{ marginBottom: 20 }}>
        <h4 style={{ display: "flex", alignItems: "center", gap: 8, margin: "0 0 12px", color: "#1f2937", fontSize: 14, fontWeight: 600 }}>
          💡 Key Points <span style={{ fontWeight: 400, color: "#6b7280" }}>({keyPoints.length})</span>
        </h4>
        
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {keyPoints.map((point, idx) => {
            const isObject = typeof point === 'object' && point !== null;
            const pointId = isObject ? point.id : `kp_${idx + 1}`;
            const concept = isObject ? point.concept : null;
            const claim = isObject ? point.claim : point;
            const implication = isObject ? point.implication : null;
            const importance = isObject ? point.importance : 'high';
            const insightType = isObject ? point.insight_type : 'insight';
            
            const impStyle = getImportanceStyle(importance);
            const typeStyle = getTypeStyle(insightType);

            return (
              <div key={idx} style={{
                padding: 16,
                background: "#fff",
                borderRadius: 12,
                border: `1px solid ${impStyle.border}`,
                borderLeft: `4px solid ${impStyle.color}`
              }}>
                {/* Header with ID and badges */}
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10, flexWrap: "wrap" }}>
                  <span style={{
                    fontFamily: "monospace",
                    fontSize: 11,
                    fontWeight: 700,
                    background: "#f3f4f6",
                    padding: "4px 8px",
                    borderRadius: 4,
                    color: "#374151"
                  }}>
                    {pointId}
                  </span>
                  <span style={{
                    fontSize: 11,
                    fontWeight: 600,
                    padding: "4px 10px",
                    borderRadius: 20,
                    background: impStyle.bg,
                    color: impStyle.color,
                    textTransform: "capitalize"
                  }}>
                    {importance}
                  </span>
                  <span style={{
                    fontSize: 11,
                    fontWeight: 500,
                    padding: "4px 10px",
                    borderRadius: 20,
                    background: typeStyle.bg,
                    color: typeStyle.color,
                    display: "flex",
                    alignItems: "center",
                    gap: 4
                  }}>
                    {typeStyle.icon} {insightType?.replace("_", " ")}
                  </span>
                </div>

                {/* Concept */}
                {concept && (
                  <h5 style={{ margin: "0 0 6px", fontSize: 14, fontWeight: 600, color: "#1f2937" }}>
                    {concept}
                  </h5>
                )}
                
                {/* Claim */}
                <p style={{ margin: 0, fontSize: 14, color: "#374151", lineHeight: 1.5 }}>
                  {claim}
                </p>
                
                {/* Implication */}
                {implication && (
                  <div style={{
                    display: "flex",
                    alignItems: "flex-start",
                    gap: 8,
                    marginTop: 10,
                    padding: 10,
                    background: "#f9fafb",
                    borderRadius: 8,
                    fontSize: 13,
                    color: "#4b5563"
                  }}>
                    <span style={{ color: "#9ca3af" }}>→</span>
                    <span>{implication}</span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Relationships */}
      {relationships.length > 0 && (
        <div style={{ marginBottom: 20 }}>
          <h4 style={{ display: "flex", alignItems: "center", gap: 8, margin: "0 0 12px", color: "#1f2937", fontSize: 14, fontWeight: 600 }}>
            🔗 Relationships
          </h4>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {relationships.map((rel, idx) => (
              <div key={idx} style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "10px 14px",
                background: "#faf5ff",
                borderRadius: 8,
                fontSize: 13
              }}>
                <span style={{ fontFamily: "monospace", fontWeight: 600, color: "#7c3aed" }}>{rel.from_id}</span>
                <span style={{ color: "#a78bfa" }}>→</span>
                <span style={{
                  padding: "3px 10px",
                  background: "#fff",
                  borderRadius: 4,
                  color: "#7c3aed",
                  fontSize: 12,
                  fontWeight: 500
                }}>
                  {rel.relationship_type}
                </span>
                <span style={{ color: "#a78bfa" }}>→</span>
                <span style={{ fontFamily: "monospace", fontWeight: 600, color: "#7c3aed" }}>{rel.to_id}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* JSON View */}
      {showJson && (
        <details open style={{ marginTop: 16 }}>
          <summary style={{ cursor: "pointer", fontSize: 13, fontWeight: 500, color: "#6b7280", marginBottom: 8 }}>
            📄 Full JSON Output
          </summary>
          <pre style={{
            padding: 12,
            background: "#1e293b",
            color: "#e2e8f0",
            borderRadius: 8,
            fontSize: 11,
            overflow: "auto",
            maxHeight: 300
          }}>
            {JSON.stringify(summary, null, 2)}
          </pre>
        </details>
      )}
    </AgentCard>
  );
}
