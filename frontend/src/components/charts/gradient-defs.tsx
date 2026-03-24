export function ChartGradientDefs() {
  return (
    <defs>
      <linearGradient id="strokeGrad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stopColor="#6366f1" />
        <stop offset="50%" stopColor="#8b5cf6" />
        <stop offset="100%" stopColor="#22d3ee" />
      </linearGradient>
      <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#6366f1" stopOpacity={0.35} />
        <stop offset="100%" stopColor="#22d3ee" stopOpacity={0.02} />
      </linearGradient>
    </defs>
  )
}
