import { useEffect, useMemo, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import { ChartGradientDefs } from '@/components/charts/gradient-defs'
import { ChartPanel } from '@/components/charts/chart-panel'
import { Badge } from '@/components/ui/badge'
import { PageTransition } from '@/components/page-transition'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  ApiError,
  getAnalyticsHistory,
  getAnalyticsOverview,
  postCostSimulate,
  type AnalyticsOverview,
  type CostSimulateResponse,
} from '@/lib/api'
import { cn } from '@/lib/utils'

const savings = [
  { d: 'Mon', v: 120 },
  { d: 'Tue', v: 180 },
  { d: 'Wed', v: 210 },
  { d: 'Thu', v: 260 },
  { d: 'Fri', v: 240 },
  { d: 'Sat', v: 160 },
  { d: 'Sun', v: 190 },
]

const costBars = [
  { name: 'GPT-4.1', usd: 420 },
  { name: 'GPT-4o', usd: 310 },
  { name: 'Claude', usd: 260 },
  { name: 'Other', usd: 140 },
]

const pie = [
  { name: 'GPT-4.1', value: 42 },
  { name: 'GPT-4o', value: 28 },
  { name: 'Claude', value: 18 },
  { name: 'Rest', value: 12 },
]

const COLORS = ['#6366f1', '#8b5cf6', '#22d3ee', '#64748b']

/** Deterministic placeholder (no `Math.random` — stable across renders). */
function pseudoHeat(d: number, h: number): number {
  return 20 + ((d * 17 + h * 23 + 41) % 80)
}

const heat = Array.from({ length: 7 }, (_, d) =>
  Array.from({ length: 12 }, (_, h) => ({
    d,
    h,
    v: pseudoHeat(d, h),
  })),
).flat()

const effHeat = heat.map((c, i) => ({
  ...c,
  e: Math.min(100, 35 + ((i * 7 + c.d * 3 + c.h * 2) % 45)),
}))

export function AnalyticsPage() {
  const [monthlyTokens, setMonthlyTokens] = useState('2500000')
  const [costApi, setCostApi] = useState<CostSimulateResponse | null>(null)
  const [costErr, setCostErr] = useState<string | null>(null)
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null)
  const [savingsChart, setSavingsChart] = useState(savings)

  const fallbackSim = useMemo(() => {
    const tokens = Math.max(0, Number(monthlyTokens.replace(/\D/g, '')) || 0)
    const costPer1k = 0.012
    const without = (tokens / 1000) * costPer1k
    const saveRate = 0.34
    const withComp = without * (1 - saveRate)
    const savingsAmt = without - withComp
    const pct = without <= 0 ? 0 : Math.round((savingsAmt / without) * 100)
    return { without, withComp, savings: savingsAmt, pct }
  }, [monthlyTokens])

  const sim = costApi
    ? {
        without: costApi.cost_without_compression_usd,
        withComp: costApi.cost_with_compression_usd,
        savings:
          costApi.cost_without_compression_usd -
          costApi.cost_with_compression_usd,
        pct: costApi.savings_pct,
      }
    : fallbackSim

  useEffect(() => {
    const tokens = Math.max(0, Number(monthlyTokens.replace(/\D/g, '')) || 0)
    const handle = window.setTimeout(() => {
      setCostErr(null)
      postCostSimulate(tokens)
        .then(setCostApi)
        .catch((e: unknown) => {
          setCostApi(null)
          setCostErr(
            e instanceof ApiError ? e.message : 'Cost API unavailable',
          )
        })
    }, 400)
    return () => clearTimeout(handle)
  }, [monthlyTokens])

  useEffect(() => {
    void getAnalyticsOverview()
      .then(setOverview)
      .catch(() => setOverview(null))
  }, [])

  useEffect(() => {
    void getAnalyticsHistory(14)
      .then((rows) => {
        if (rows.length === 0) return
        setSavingsChart(
          rows.map((r) => ({
            d: r.date.slice(5),
            v: r.tokens_saved,
          })),
        )
      })
      .catch(() => {})
  }, [])

  return (
    <PageTransition>
      <div className="space-y-8">
        <div>
          <h1 className="mb-1">Analytics</h1>
          <p className="text-sm text-muted-foreground">
            Savings trends, model mix, and request intensity.
            {overview ? (
              <span className="ml-2 font-mono text-xs text-caption">
                · DB: {overview.total_tokens_saved.toLocaleString()} tokens saved · $
                {overview.cost_saved_usd.toFixed(2)} est. cost avoided
              </span>
            ) : null}
          </p>
          {costErr ? (
            <p className="mt-2 text-xs text-warning">
              Cost simulation: {costErr} — showing local estimate.
            </p>
          ) : null}
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Cost simulation</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-4 md:grid-cols-[minmax(0,240px)_1fr]">
            <div className="space-y-2">
              <Label htmlFor="monthly-tokens" className="text-caption">
                Expected monthly tokens
              </Label>
              <Input
                id="monthly-tokens"
                inputMode="numeric"
                value={monthlyTokens}
                onChange={(e) => setMonthlyTokens(e.target.value)}
                className="font-mono"
                placeholder="e.g. 2500000"
              />
              <p className="text-xs text-caption">
                Illustrative pricing · editable assumption ($12 / 1M in-tokens).
              </p>
            </div>
            <div className="grid gap-3 sm:grid-cols-3">
              <div className="rounded-xl border border-border bg-surface-secondary p-4">
                <p className="text-xs text-caption">Without compression</p>
                <p className="mt-1 font-mono text-lg tabular-nums text-foreground">
                  ${sim.without.toFixed(0)}
                </p>
              </div>
              <div className="rounded-xl border border-border bg-surface-secondary p-4">
                <p className="text-xs text-caption">With compression</p>
                <p className="mt-1 font-mono text-lg tabular-nums text-success">
                  ${sim.withComp.toFixed(0)}
                </p>
              </div>
              <div className="rounded-xl border border-border bg-surface-secondary p-4">
                <p className="text-xs text-caption">Savings</p>
                <p className="mt-1 font-mono text-lg tabular-nums text-foreground">
                  ${sim.savings.toFixed(0)}
                  <span className="ml-2 text-sm text-success">({sim.pct}%)</span>
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Token savings</CardTitle>
            </CardHeader>
            <CardContent className="pl-0">
              <ChartPanel>
                <ResponsiveContainer width="100%" height="100%">
                <LineChart data={savingsChart} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" opacity={0.35} />
                  <XAxis dataKey="d" tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} width={32} />
                  <Tooltip
                    contentStyle={{
                      background: 'var(--color-surface)',
                      border: '1px solid var(--color-border)',
                      borderRadius: 12,
                      fontSize: 12,
                    }}
                  />
                  <Line type="monotone" dataKey="v" stroke="url(#strokeGrad)" strokeWidth={2} dot={false} />
                  <ChartGradientDefs />
                </LineChart>
              </ResponsiveContainer>
              </ChartPanel>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row flex-wrap items-center justify-between gap-2">
              <CardTitle>Cost savings by model</CardTitle>
              <Badge variant="warning" className="text-[10px]">
                Demo data
              </Badge>
            </CardHeader>
            <CardContent className="pl-0">
              <ChartPanel>
                <ResponsiveContainer width="100%" height="100%">
                <BarChart data={costBars} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" opacity={0.35} vertical={false} />
                  <XAxis dataKey="name" tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} width={36} />
                  <Tooltip
                    contentStyle={{
                      background: 'var(--color-surface)',
                      border: '1px solid var(--color-border)',
                      borderRadius: 12,
                      fontSize: 12,
                    }}
                    formatter={(v) => [`$${Number(v ?? 0)}`, 'Saved']}
                  />
                  <Bar dataKey="usd" radius={[6, 6, 0, 0]}>
                    {costBars.map((_, i) => (
                      <Cell key={costBars[i].name} fill={COLORS[i % COLORS.length]} opacity={0.85} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              </ChartPanel>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader className="flex flex-row flex-wrap items-center justify-between gap-2">
              <CardTitle>Model usage</CardTitle>
              <Badge variant="warning" className="text-[10px]">
                Demo data
              </Badge>
            </CardHeader>
            <CardContent>
              <ChartPanel>
                <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pie}
                    dataKey="value"
                    nameKey="name"
                    innerRadius={48}
                    outerRadius={80}
                    paddingAngle={2}
                  >
                    {pie.map((_, i) => (
                      <Cell key={pie[i].name} fill={COLORS[i % COLORS.length]} stroke="transparent" />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: 'var(--color-surface)',
                      border: '1px solid var(--color-border)',
                      borderRadius: 12,
                      fontSize: 12,
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              </ChartPanel>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row flex-wrap items-center justify-between gap-2">
              <CardTitle>Token usage density</CardTitle>
              <Badge variant="warning" className="text-[10px]">
                Demo grid
              </Badge>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto pb-2">
                <div className="inline-grid min-w-[520px] grid-cols-[repeat(12,minmax(0,1fr))] gap-1">
                  {heat.map((c) => (
                    <div
                      key={`${c.d}-${c.h}`}
                      className={cn(
                        'aspect-square rounded-md border border-border/40',
                        'bg-gradient-to-br from-indigo/10 to-cyan/20',
                      )}
                      style={{ opacity: c.v / 120 }}
                      title={`D${c.d + 1} H${c.h}: ${c.v} req`}
                    />
                  ))}
                </div>
              </div>
              <p className="mt-2 text-xs text-caption">
                7×12 grid: day × hour. Scroll horizontally on small screens.
              </p>
            </CardContent>
          </Card>

          <Card className="lg:col-span-2">
            <CardHeader className="flex flex-row flex-wrap items-center justify-between gap-2">
              <CardTitle>Compression effectiveness</CardTitle>
              <Badge variant="warning" className="text-[10px]">
                Demo grid
              </Badge>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto pb-2">
                <div className="inline-grid min-w-[520px] grid-cols-[repeat(12,minmax(0,1fr))] gap-1">
                  {effHeat.map((c) => (
                    <div
                      key={`e-${c.d}-${c.h}`}
                      className="aspect-square rounded-md border border-success/20 bg-gradient-to-br from-success/15 to-emerald-500/10"
                      style={{ opacity: c.e / 130 }}
                      title={`Effectiveness ${c.e}% · D${c.d + 1} H${c.h}`}
                    />
                  ))}
                </div>
              </div>
              <p className="mt-2 text-xs text-caption">
                Per-request savings intensity (higher is better).
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </PageTransition>
  )
}
