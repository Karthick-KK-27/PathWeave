function ProfileScreen({ value, onChange, onSubmit }) {
  return (
    <div className="max-w-xl mx-auto mt-16">
      <h1 className="text-3xl font-bold mb-2 gradient-text">Paste your resume / transcript</h1>
      <p className="text-gray-500 text-sm mb-5">
        Don't worry about formatting — just paste what you have.
      </p>
      <textarea
        className="input-field h-64 mb-4 resize-none"
        placeholder="Paste your skills, courses, and projects here..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
      <button className="btn-primary w-full" onClick={onSubmit}>
        Analyze My Path
      </button>
    </div>
  );
}

export default ProfileScreen;