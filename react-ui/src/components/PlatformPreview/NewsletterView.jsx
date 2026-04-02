export default function NewsletterView({ newsletter, label = "Preview" }) {
  return (
    <article className="platform-card newsletter">
      <div className="platform-head">
        <div>
          <strong>Newsletter Draft</strong>
          <span>{label}</span>
        </div>
      </div>
      <div className="platform-body">
        <h4>{newsletter.subject_line}</h4>
        <p className="preview">{newsletter.preview_text}</p>
        <p>{newsletter.intro}</p>
        <ul>
          {newsletter.body_sections.map((section) => (
            <li key={section.slice(0, 20)}>{section}</li>
          ))}
        </ul>
        <p><strong>{newsletter.closing}</strong></p>
      </div>
    </article>
  );
}
