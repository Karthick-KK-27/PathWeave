import { useState } from "react";
import axios from "axios";
import LandingScreen from "./components/LandingScreen";
import ProfileScreen from "./components/ProfileScreen";
import ResearchingScreen from "./components/ResearchingScreen";
import ResultsScreen from "./components/ResultsScreen";
import ScheduleScreen from "./components/ScheduleScreen";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Fallback used when the backend is unreachable, so the demo still
// clicks through end-to-end. Same shape as /api/plan returns.
const MOCK_RESULT = {
  job_requirements: { role: "ML Engineer", company: "Target Co" },
  skill_gaps: [
    { skill: "CUDA", severity: "critical" },
    { skill: "Distributed Systems", severity: "moderate" },
    { skill: "Docker", severity: "minor" },
  ],
  recommendations: [
    {
      title: "Take Embedded Systems elective",
      reasoning:
        "Closes your CUDA/hardware-adjacent gap and connects to your Team Kshatriya BMS work.",
      leverage: "high",
    },
  ],
};

function App() {
  const [screen, setScreen] = useState("landing");
  const [targetJob, setTargetJob] = useState("");
  const [resumeText, setResumeText] = useState("");
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState("Ready");

  const resetFlow = () => {
    setScreen("landing");
    setTargetJob("");
    setResumeText("");
    setResult(null);
    setStatus("Ready");
  };

  const handleSubmit = async () => {
    setScreen("researching");
    setStatus("Analyzing...");
    try {
      const response = await axios.post(
        `${API_URL}/api/plan`,
        { target_job: targetJob, resume_text: resumeText },
        { timeout: 90000 },
      );
      setResult(response.data);
      setScreen("results");
      setStatus("Ready");
    } catch (err) {
      console.error("Backend call failed, falling back to mock:", err);
      setStatus("Backend unavailable — showing sample");
      const fallback = { ...MOCK_RESULT, job_requirements: { role: targetJob || "your role" } };
      setResult(fallback);
      setScreen("results");
    }
  };

  return (
    <div className="page-shell">
      {/* Top status bar */}
      <div className="relative z-10 flex items-center justify-between px-6 py-4 border-b border-purple-900/20">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center font-bold text-sm">
            P
          </div>
          <div>
            <div className="font-semibold text-sm">
              Pathweave <span className="text-purple-300 font-normal">· VIT EEE Edition</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span
            className={`badge ${
              status === "Ready"
                ? "bg-green-500/10 text-green-300 border border-green-500/20"
                : "bg-purple-500/10 text-purple-300 border border-purple-500/20"
            }`}
          >
            Status: {status}
          </span>
          <button onClick={resetFlow} className="btn-secondary">
            Reset Flow
          </button>
        </div>
      </div>

      {/* Screen content */}
      <div className="relative z-10 px-6 py-10">
        {screen === "landing" && (
          <LandingScreen value={targetJob} onChange={setTargetJob} onNext={() => setScreen("profile")} />
        )}
        {screen === "profile" && (
          <ProfileScreen value={resumeText} onChange={setResumeText} onSubmit={handleSubmit} />
        )}
        {screen === "researching" && <ResearchingScreen />}
        {screen === "results" && (
          <ResultsScreen result={result} onViewSchedule={() => setScreen("schedule")} />
        )}
        {screen === "schedule" && (
          <ScheduleScreen recommendations={result?.recommendations || []} onBack={() => setScreen("results")} />
        )}
      </div>
    </div>
  );
}

export default App;
