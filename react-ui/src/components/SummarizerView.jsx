import { useState } from "react";
import AgentCard from "./AgentCard";

export default function SummarizerView({ inputText, summary, loading }) {
  const [showJson, setShowJson] = useState(false);

  const keyPoints = summary.key_points || [];
  const wordCount = inputText ? inputText.split(/\s+/).filter(Boolean).length : 0;

  return (
    <AgentCard
      title="Agent 1 — Summarizer"
      subtitle="Core Message & Key Insights"
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

      {/* Core Message */}
      {summary.core_message && (
        <div style={{
          padding: 24,
          background: "#f8fafc",
          borderRadius: 12,
          marginBottom: 32
        }}>
          <h4 style={{ margin: "0 0 12px 0", color: "#374151", fontSize: 14, fontWeight: 600 }}>
            Core Insight
          </h4>
          <p style={{ margin: 0, fontSize: 18, fontWeight: 500, color: "#111827", lineHeight: 1.6 }}>
            {summary.core_message}
          </p>
        </div>
      )}

      {/* Key Points */}
      <div style={{ marginBottom: 24 }}>
        <h4 style={{ margin: "0 0 20px 0", color: "#374151", fontSize: 16, fontWeight: 600 }}>
          Key Insights
        </h4>
        
        {/* Group by priority */}
        {['critical', 'high', 'medium'].map(priority => {
          const pointsForPriority = keyPoints.filter(point => point.priority === priority);
          if (pointsForPriority.length === 0) return null;
          
          return (
            <div key={priority} style={{ marginBottom: 24 }}>
              <h5 style={{ 
                margin: "0 0 12px 0", 
                fontSize: 14, 
                fontWeight: 600, 
                color: "#111827",
                textTransform: "capitalize"
              }}>
                {priority}
              </h5>
              
              <div style={{ marginLeft: 0 }}>
                {pointsForPriority.map((point, idx) => {
                  const getPriorityBorder = (priority) => {
                    const colors = {
                      critical: "#ef4444",
                      high: "#f97316", 
                      medium: "#6b7280"
                    };
                    return colors[priority] || colors.medium;
                  };
                  
                  return (
                    <div key={idx} style={{
                      display: "flex",
                      alignItems: "flex-start",
                      marginBottom: 8,
                      paddingLeft: 12,
                      borderLeft: `2px solid ${getPriorityBorder(point.priority)}`
                    }}>
                      <span style={{ 
                        marginRight: 8, 
                        marginTop: 2,
                        fontSize: 14,
                        color: "#374151"
                      }}>
                        •
                      </span>
                      <div>
                        <span style={{ 
                          fontSize: 14, 
                          color: "#111827",
                          lineHeight: 1.5
                        }}>
                          {point.label}
                          {point.data && (
                            <span style={{ 
                              marginLeft: 4,
                              fontSize: 13,
                              color: "#059669",
                              fontWeight: 500
                            }}>
                              ({point.data})
                            </span>
                          )}
                        </span>
                        {point.reason && (
                          <div style={{
                            marginTop: 4,
                            fontSize: 13,
                            color: "#6b7280",
                            fontStyle: "italic",
                            lineHeight: 1.4
                          }}>
                            {point.reason}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

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
