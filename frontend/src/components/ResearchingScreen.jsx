import { useEffect, useState } from "react";

const steps = [
  { icon: "🔍", text: "Researching current job requirements..." },
  { icon: "🧠", text: "Analyzing your skill profile..." },
  { icon: "📊", text: "Identifying gaps..." },
  { icon: "🎯", text: "Ranking your best next moves..." },
];

function ResearchingScreen() {
  const [visible, setVisible] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setVisible((v) => (v < steps.length ? v + 1 : v));
    }, 400);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="max-w-xl mx-auto mt-24 text-center">
      <div className="w-14 h-14 mx-auto mb-8 rounded-full border-4 border-purple-500/20 border-t-purple-500 animate-spin" />
      <div className="space-y-3">
        {steps.slice(0, visible).map((s, i) => (
          <div key={i} className="text-gray-300 animate-pulse text-lg">
            {s.icon} {s.text}
          </div>
        ))}
      </div>
    </div>
  );
}

export default ResearchingScreen;