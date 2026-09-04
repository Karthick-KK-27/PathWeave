import WhyThisPanel from "./WhyThisPanel";

function RecommendationsSection({ recs }) {
  const leverageColor = {
    high: "border-green-400",
    medium: "border-yellow-400",
    low: "border-gray-300",
  };

  return (
    <div>
      <h2 className="text-xl font-semibold mb-3">Recommendations</h2>
      <div className="space-y-3">
        {recs.map((r, i) => (
          <div key={i} className={`border-l-4 ${leverageColor[r.leverage]} bg-white p-4 rounded-lg shadow-sm`}>
            <div className="font-medium">{r.title}</div>
            <WhyThisPanel reasoning={r.reasoning} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecommendationsSection;