function ScheduleScreen({ recommendations, onBack }) {
  const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  // Simple placement: spread recommendations across the week, one per day
  const blocks = recommendations.map((r, i) => ({
    day: days[i % days.length],
    title: r.title,
  }));

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Your Week</h1>
      <div className="grid grid-cols-7 gap-2">
        {days.map((day) => (
          <div key={day} className="border rounded-lg p-2 min-h-[150px]">
            <div className="font-semibold text-sm mb-2">{day}</div>
            {blocks
              .filter((b) => b.day === day)
              .map((b, i) => (
                <div key={i} className="bg-black text-white text-xs p-2 rounded mb-1">
                  {b.title}
                </div>
              ))}
          </div>
        ))}
      </div>
      <button className="mt-6 text-blue-600 underline" onClick={onBack}>
        ← Back to results
      </button>
    </div>
  );
}

export default ScheduleScreen;