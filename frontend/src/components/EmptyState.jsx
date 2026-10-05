export default function EmptyState({ title, detail }) {
  return (
    <div className="rounded-2xl border border-dashed border-slate-700 p-8 text-center">
      <p className="text-white">{title}</p>
      <p className="mt-2 text-sm text-slate-400">{detail}</p>
    </div>
  );
}
