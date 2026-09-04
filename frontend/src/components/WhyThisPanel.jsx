import { useState } from "react";

function WhyThisPanel({ reasoning }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="mt-2">
      <button className="link-muted" onClick={() => setOpen(!open)}>
        {open ? "Hide reasoning ↑" : "Why this? ↓"}
      </button>
      {open && (
        <p className="text-sm text-gray-400 mt-2 bg-purple-500/5 border border-purple-500/10 p-3 rounded-lg leading-relaxed">
          {reasoning}
        </p>
      )}
    </div>
  );
}

export default WhyThisPanel;