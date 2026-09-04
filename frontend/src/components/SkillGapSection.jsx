function SkillGapSection({ gaps }) {
  const severityStyle = {
    critical: "bg-red-500/10 text-red-300 border border-red-500/20",
    moderate: "bg-yellow-500/10 text-yellow-300 border border-yellow-500/20",
    minor: "bg-gray-500/10 text-gray-400 border border-gray-500/20",
  };

  return (
    <div className="mb-8">
      <h2 className="text-lg font-semibold mb-3 text-gray-200">Skill Gaps</h2>
      <div className="space-y-2">
        {gaps.map((g, i) => (
          <div key={i} className="card flex justify-between items-center py-3">
            <span className="font-medium text-gray-200">{g.skill}</span>
            <span className={`badge capitalize ${severityStyle[g.severity]}`}>
              {g.severity}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SkillGapSection;