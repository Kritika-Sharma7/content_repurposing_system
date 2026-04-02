import { Database, Palette, Search, RefreshCw } from 'lucide-react';

const legendItems = [
  { icon: Database, label: 'Structured Data', color: 'bg-blue-400', description: 'Summarizer' },
  { icon: Palette, label: 'Transformation', color: 'bg-purple-400', description: 'Formatter' },
  { icon: Search, label: 'Evaluation', color: 'bg-orange-400', description: 'Reviewer' },
  { icon: RefreshCw, label: 'Iteration', color: 'bg-green-400', description: 'Refiner' },
];

export default function SystemLegend() {
  return (
    <div className="system-legend inline-flex flex-wrap items-center gap-3 bg-gray-50 border border-gray-200 rounded-xl px-4 py-2">
      {legendItems.map((item) => {
        const Icon = item.icon;
        return (
          <div key={item.label} className="flex items-center gap-1.5">
            <div className={`w-2.5 h-2.5 rounded-full ${item.color}`}></div>
            <span className="text-xs text-gray-600">{item.label}</span>
          </div>
        );
      })}
    </div>
  );
}
