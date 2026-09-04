import GapRadarChart from "./GapRadarChart";
import SkillGapSection from "./SkillGapSection";
import RecommendationsSection from "./RecommendationsSection";

function ResultsScreen({ result, onViewSchedule }) {
  if (!result) return null;
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-8">
        Your Path to <span className="gradient-text">{result.job_requirements?.role || "your role"}</span>
      </h1>

      <div className="card mb-8">
        <GapRadarChart gaps={result.skill_gaps} />
      </div>

      <SkillGapSection gaps={result.skill_gaps} />
      <RecommendationsSection recs={result.recommendations} />

      <button className="btn-primary mt-4" onClick={onViewSchedule}>
        Turn This Into a Schedule →
      </button>
    </div>
  );
}

export default ResultsScreen;