export default function ExplanationPanel({ title = 'Why?', explanations = [] }) {
  if (!explanations?.length) return null;
  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
      <ul className="mt-4 space-y-2">
        {explanations.map((item) => (
          <li key={item} className="flex gap-2 text-sm text-slate-600">
            <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-brand-600" />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
