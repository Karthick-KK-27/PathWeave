import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer } from "recharts";

function GapRadarChart({ gaps = [] }) {
  const severityValue = { critical: 3, moderate: 2, minor: 1 };
  const data = (gaps || []).map((g) => ({ skill: g.skill, gap: severityValue[g.severity] || 0 }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <RadarChart data={data}>
        <PolarGrid stroke="#3f3f5f" />
        <PolarAngleAxis dataKey="skill" tick={{ fill: "#c4b5fd", fontSize: 12 }} />
        <Radar
          dataKey="gap"
          stroke="#a78bfa"
          fill="url(#radarGradient)"
          fillOpacity={0.6}
        />
        <defs>
          <linearGradient id="radarGradient" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#8b5cf6" />
            <stop offset="100%" stopColor="#3b82f6" />
          </linearGradient>
        </defs>
      </RadarChart>
    </ResponsiveContainer>
  );
}

export default GapRadarChart;