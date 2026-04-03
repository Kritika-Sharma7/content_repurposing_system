export default function SummaryTab({ summary, inputText, preferences }) {
  if (!summary) {
    return (
      <div className="text-center text-gray-500">
        No summary available
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Core Message */}
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-3">Core Message</h3>
        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
          <p className="text-gray-800 leading-relaxed">
            {summary.core_message}
          </p>
        </div>
      </div>

      {/* Key Points */}
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-4">Key Points</h3>
        <div className="space-y-3">
          {summary.key_points?.map((point, index) => (
            <div key={point.id || index} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <p className="text-gray-800 mb-2">{point.label}</p>
                  {point.data && (
                    <p className="text-sm text-gray-600 bg-gray-50 px-2 py-1 rounded">
                      📊 {point.data}
                    </p>
                  )}
                </div>
                <div className="ml-4">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      point.priority === "critical"
                        ? "bg-red-100 text-red-800"
                        : point.priority === "high"
                        ? "bg-orange-100 text-orange-800"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {point.priority}
                  </span>
                </div>
              </div>
              {point.reason && (
                <p className="text-sm text-gray-600 mt-2 italic">
                  {point.reason}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Meta Information */}
      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="font-medium text-gray-900 mb-2">Processing Info</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <div className="text-gray-500">Input Words</div>
            <div className="font-medium">{inputText?.split(/\s+/).length || 0}</div>
          </div>
          <div>
            <div className="text-gray-500">Key Points</div>
            <div className="font-medium">{summary.key_points?.length || 0}</div>
          </div>
          <div>
            <div className="text-gray-500">Tone</div>
            <div className="font-medium capitalize">{preferences.tone}</div>
          </div>
          <div>
            <div className="text-gray-500">Audience</div>
            <div className="font-medium capitalize">{preferences.audience}</div>
          </div>
        </div>
      </div>
    </div>
  );
}