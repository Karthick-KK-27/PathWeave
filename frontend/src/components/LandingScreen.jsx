function LandingScreen({ value, onChange, onNext }) {
  return (
    <div className="max-w-xl mx-auto mt-16 text-center">
      <h1 className="text-5xl font-bold mb-3 gradient-text">Pathweave</h1>
      <p className="text-gray-400 mb-10 leading-relaxed">
        Tell us your dream role. We'll reverse-engineer this semester's
        decisions to get you there.
      </p>
      <div className="flex gap-3">
        <input
          className="input-field"
          placeholder="e.g. ML Engineer at NVIDIA"
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
        <button className="btn-primary whitespace-nowrap" onClick={onNext} disabled={!value}>
          Get Started
        </button>
      </div>
    </div>
  );
}

export default LandingScreen;