export default function InputPanel({ inputText, setInputText, onSample, onRun }) {
  return (
    <section className="card input-panel">
      <div className="panel-head">
        <h2>Input Panel</h2>
        <p>Paste long-form input or use a sample article.</p>
      </div>

      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Paste article, blog post, or report text..."
      />

      <div className="row gap-sm">
        <button className="btn btn-outline" onClick={onSample}>Use Sample</button>
        <button className="btn btn-dark" onClick={onRun}>Run Workflow</button>
      </div>
    </section>
  );
}
