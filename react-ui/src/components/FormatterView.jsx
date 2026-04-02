import AgentCard from "./AgentCard";
import LinkedInCard from "./PlatformPreview/LinkedInCard";
import TwitterThread from "./PlatformPreview/TwitterThread";
import NewsletterView from "./PlatformPreview/NewsletterView";

export default function FormatterView({ formatted, loading }) {
  return (
    <AgentCard
      title="Agent 2: Formatter"
      subtitle="Converts summary into LinkedIn, Twitter/X, and Newsletter"
      status={loading ? "running" : "complete"}
    >
      <div className="tab-grid">
        <div>
          <h4>LinkedIn</h4>
          <LinkedInCard post={formatted.linkedin} label="V1" />
        </div>
        <div>
          <h4>Twitter/X Thread</h4>
          <TwitterThread thread={formatted.twitter} label="V1" />
        </div>
        <div>
          <h4>Newsletter</h4>
          <NewsletterView newsletter={formatted.newsletter} label="V1" />
        </div>
      </div>
    </AgentCard>
  );
}
