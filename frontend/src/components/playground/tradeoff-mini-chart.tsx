import {
  Area,
  AreaChart,
  ReferenceLine,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from 'recharts'

const curve = Array.from({ length: 11 }, (_, i) => {
  const x = i * 10
  return {
    x,
    accuracy: Math.max(38, 100 - x * 0.52),
    compression: Math.min(94, 12 + x * 0.82),
  }
})

type TradeoffMiniChartProps = {
  level: number
}

/** Inline tradeoff: accuracy vs compression (static curves + current level marker) */
export function TradeoffMiniChart({ level }: TradeoffMiniChartProps) {
  return (
    <div className="h-28 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={curve} margin={{ top: 6, right: 8, left: -24, bottom: 0 }}>
          <defs>
            <linearGradient id="accFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#6366f1" stopOpacity={0.22} />
              <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="compFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#22d3ee" stopOpacity={0.18} />
              <stop offset="100%" stopColor="#22d3ee" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis
            dataKey="x"
            type="number"
            domain={[0, 100]}
            tick={{ fontSize: 9, fill: 'var(--color-caption)' }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis hide domain={[0, 100]} />
          <ReferenceLine
            x={level}
            stroke="#8b5cf6"
            strokeDasharray="4 4"
            strokeOpacity={0.7}
          />
          <Area
            type="monotone"
            dataKey="accuracy"
            stroke="#6366f1"
            fill="url(#accFill)"
            strokeWidth={1.5}
            dot={false}
          />
          <Area
            type="monotone"
            dataKey="compression"
            stroke="#22d3ee"
            fill="url(#compFill)"
            strokeWidth={1.5}
            dot={false}
          />
        </AreaChart>
      </ResponsiveContainer>
      <div className="flex justify-between px-0.5 text-[10px] text-caption">
        <span>High accuracy</span>
        <span>High compression</span>
      </div>
    </div>
  )
}
