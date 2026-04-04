export default function ReviewTab({ review, iterations }) {
  // If iterations are provided, show the full iteration history
  if (iterations && iterations.length > 0) {
    return <IterationHistoryView iterations={iterations} />;
  }

  // Fallback to single review display
  if (!review) {
    return (
      <div className="text-center text-gray-500">
        No review data available
      </div>
    );
  }

  return <SingleReviewView review={review} />;
}

// Show iteration-by-iteration review history
function IterationHistoryView({ iterations }) {
  const totalIterations = iterations.length;
  
  return (
    <div className="space-y-8">
      {/* Summary Header */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 border border-blue-200">
        <h2 className="text-xl font-bold text-gray-900 mb-2">
          🔄 Iterative Review & Refinement
        </h2>
        <p className="text-gray-700 mb-4">
          Your content went through {totalIterations} review iteration{totalIterations > 1 ? 's' : ''}. 
          Here's the quality improvement journey:
        </p>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div className="bg-white rounded p-3">
            <div className="text-gray-500">Iterations</div>
            <div className="text-2xl font-bold text-blue-600">{totalIterations}</div>
          </div>
          <div className="bg-white rounded p-3">
            <div className="text-gray-500">Total Issues Found</div>
            <div className="text-2xl font-bold text-orange-600">
              {iterations.reduce((sum, it) => sum + (it.review?.issues?.length || 0), 0)}
            </div>
          </div>
          <div className="bg-white rounded p-3">
            <div className="text-gray-500">Issues Fixed</div>
            <div className="text-2xl font-bold text-green-600">
              {iterations.reduce((sum, it) => sum + (it.issues_fixed || 0), 0)}
            </div>
          </div>
        </div>
      </div>

      {/* Iteration Timeline */}
      {iterations.map((iteration, index) => (
        <IterationCard 
          key={iteration.iteration} 
          iteration={iteration} 
          index={index}
          isLast={index === iterations.length - 1}
        />
      ))}
    </div>
  );
}

// Single iteration card
function IterationCard({ iteration, index, isLast }) {
  const review = iteration.review;
  const totalIssues = review?.issues?.length || 0;
  
  return (
    <div className="relative">
      {/* Timeline connector */}
      {!isLast && (
        <div className="absolute left-6 top-16 bottom-0 w-0.5 bg-gray-300"></div>
      )}
      
      <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
        {/* Iteration Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg">
              {iteration.iteration}
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900">
                Iteration {iteration.iteration}
              </h3>
              <p className="text-sm text-gray-500">
                Review of V{iteration.iteration}
              </p>
            </div>
          </div>
          
          {totalIssues === 0 ? (
            <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              ✓ No Issues
            </span>
          ) : (
            <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm font-medium">
              {totalIssues} Issue{totalIssues > 1 ? 's' : ''} Found
            </span>
          )}
        </div>

        {/* Review Content */}
        {totalIssues === 0 ? (
          <div className="text-center py-8 bg-green-50 rounded-lg">
            <div className="text-green-500 text-3xl mb-2">✅</div>
            <p className="text-green-700 font-medium">Content passed all quality checks!</p>
            {isLast && (
              <p className="text-green-600 text-sm mt-1">Ready to publish</p>
            )}
          </div>
        ) : (
          <SingleReviewView review={review} showTitle={false} />
        )}

        {/* Fixed Count */}
        {iteration.issues_fixed > 0 && (
          <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
            <div className="flex items-center space-x-2 text-blue-800 text-sm">
              <span className="font-medium">✨ Refiner addressed {iteration.issues_fixed} issue{iteration.issues_fixed > 1 ? 's' : ''}</span>
              <span className="text-blue-600">→ Creating V{iteration.iteration + 1}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// Single review display (used both standalone and within iterations)
function SingleReviewView({ review, showTitle = true }) {
  // Group issues by priority
  const criticalIssues = review.issues?.filter(issue => issue.priority === "critical") || [];
  const highIssues = review.issues?.filter(issue => issue.priority === "high") || [];
  const mediumIssues = review.issues?.filter(issue => issue.priority === "medium") || [];

  const priorityGroups = [
    {
      title: "Critical Issues",
      issues: criticalIssues,
      color: "red",
      icon: "🚨"
    },
    {
      title: "High Priority",
      issues: highIssues,
      color: "orange",
      icon: "⚠️"
    },
    {
      title: "Medium Priority", 
      issues: mediumIssues,
      color: "gray",
      icon: "ℹ️"
    }
  ];

  const totalIssues = review.issues?.length || 0;

  if (totalIssues === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-green-500 text-4xl mb-4">✅</div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Issues Found</h3>
        <p className="text-gray-600">
          Your content passed all quality checks. Ready to publish!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary (only if showTitle) */}
      {showTitle && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-medium text-gray-900 mb-3">Quality Audit Summary</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <div className="text-gray-500">Total Issues</div>
              <div className="text-2xl font-bold text-gray-900">{totalIssues}</div>
            </div>
            <div>
              <div className="text-gray-500">Critical</div>
              <div className="text-2xl font-bold text-red-600">{criticalIssues.length}</div>
            </div>
            <div>
              <div className="text-gray-500">High</div>
              <div className="text-2xl font-bold text-orange-600">{highIssues.length}</div>
            </div>
            <div>
              <div className="text-gray-500">Medium</div>
              <div className="text-2xl font-bold text-gray-600">{mediumIssues.length}</div>
            </div>
          </div>
        </div>
      )}

      {/* Issues by Priority */}
      {priorityGroups.map((group) => {
        if (group.issues.length === 0) return null;

        return (
          <div key={group.title}>
            <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <span className="mr-2">{group.icon}</span>
              {group.title} ({group.issues.length})
            </h3>
            
            <div className="space-y-4">
              {group.issues.map((issue, index) => (
                <IssueCard 
                  key={issue.issue_id || index} 
                  issue={issue} 
                  color={group.color}
                />
              ))}
            </div>
          </div>
        );
      })}

      {/* AI Reviewer Note (only if showTitle) */}
      {showTitle && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <div className="text-blue-500">🤖</div>
            <div>
              <h4 className="font-medium text-blue-900">AI Quality Reviewer</h4>
              <p className="text-blue-800 text-sm mt-1">
                These issues were identified by our AI reviewer to help improve engagement and clarity. 
                The refiner will automatically address these concerns.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function IssueCard({ issue, color }) {
  const colorClasses = {
    red: "border-red-200 bg-red-50",
    orange: "border-orange-200 bg-orange-50", 
    gray: "border-gray-200 bg-gray-50"
  };

  const badgeColors = {
    red: "bg-red-100 text-red-800",
    orange: "bg-orange-100 text-orange-800",
    gray: "bg-gray-100 text-gray-800"
  };

  return (
    <div className={`border rounded-lg p-4 ${colorClasses[color]}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h4 className="font-medium text-gray-900 mb-1">
            {issue.problem}
          </h4>
          {issue.affects && issue.affects.length > 0 && (
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <span>Affects:</span>
              <div className="flex space-x-1">
                {issue.affects.map((platform) => (
                  <span 
                    key={platform}
                    className="bg-white px-2 py-0.5 rounded text-xs border"
                  >
                    {platform}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${badgeColors[color]}`}>
          {issue.priority}
        </span>
      </div>
      
      <div className="space-y-2 text-sm">
        <div>
          <span className="font-medium text-gray-700">Why it matters:</span>
          <p className="text-gray-600 mt-1">{issue.reason}</p>
        </div>
        
        <div>
          <span className="font-medium text-gray-700">Suggestion:</span>
          <p className="text-gray-600 mt-1">{issue.suggestion}</p>
        </div>
      </div>

      {issue.missing_kps && issue.missing_kps.length > 0 && (
        <div className="mt-3 p-2 bg-white rounded border">
          <span className="text-xs font-medium text-gray-700">Missing Key Points:</span>
          <div className="flex flex-wrap gap-1 mt-1">
            {issue.missing_kps.map((kp) => (
              <span key={kp} className="bg-gray-100 px-2 py-0.5 rounded text-xs">
                {kp}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}