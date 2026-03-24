import { TrendingDown, TrendingUp } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import { ChartGradientDefs } from '@/components/charts/gradient-defs'
import { PageTransition } from '@/components/page-transition'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Tooltip as UiTooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip'
import { ChartPanel } from '@/components/charts/chart-panel'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import {
  getAnalyticsHistory,
  getAnalyticsOverview,
  getAnalyticsRecent,
  type AnalyticsHistoryRow,
  type AnalyticsOverview,
  type AnalyticsRecentRow,
} from '@/lib/api'
import { formatRelativeShort } from '@/lib/format-time'
import { cn } from '@/lib/utils'

const kpi = [
  {
    title: 'Tokens saved',
    value: '42.8%',
    sub: '+12.4% vs last week',
    up: true,
    spark: [12, 18, 15, 22, 28, 35, 42],
  },
  {
    title: 'Cost saved',
    value: '$1,847',
    sub: '+8.2% vs last week',
    up: true,
    spark: [400, 520, 480, 610, 720, 800, 847],
  },
  {
    title: 'Compression ratio',
    value: '3.2×',
    sub: 'Stable',
    up: true,
    spark: [2.8, 3.0, 3.1, 3.0, 3.2, 3.2, 3.2],
  },
  {
    title: 'Requests today',
    value: '1,284',
    sub: '+4.1% vs yesterday',
    up: true,
    spark: [200, 340, 420, 510, 780, 900, 1284],
  },
] as const

const lineData = [
  { t: 'Mon', before: 4200, after: 1800 },
  { t: 'Tue', before: 5100, after: 2100 },
  { t: 'Wed', before: 4800, after: 1900 },
  { t: 'Thu', before: 6200, after: 2400 },
  { t: 'Fri', before: 5900, after: 2200 },
  { t: 'Sat', before: 3400, after: 1400 },
  { t: 'Sun', before: 4100, after: 1700 },
]

const areaData = [
  { m: 'W1', usd: 120 },
  { m: 'W2', usd: 180 },
  { m: 'W3', usd: 210 },
  { m: 'W4', usd: 260 },
  { m: 'W5', usd: 310 },
  { m: 'W6', usd: 380 },
]

/** Shown only when the recent-activity API fails (offline / CORS). */
const DEMO_ACTIVITY_FALLBACK = [
  {
    preview: 'Summarize the following research paper on...',
    before: 842,
    after: 312,
    pct: 63,
    time: '2m ago',
  },
  {
    preview: 'You are a helpful coding assistant. Refactor...',
    before: 1204,
    after: 410,
    pct: 66,
    time: '14m ago',
  },
  {
    preview: 'Translate to French and keep tone informal...',
    before: 520,
    after: 198,
    pct: 62,
    time: '1h ago',
  },
] as const

function MiniSparkline({ data }: { data: number[] }) {
  const pts = data.map((v, i) => ({ i, v }))
  return (
    <div className="h-10 w-full min-w-0">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={pts} margin={{ top: 4, right: 0, left: 0, bottom: 0 }}>
          <Line
            type="monotone"
            dataKey="v"
            stroke="url(#strokeGrad)"
            strokeWidth={2}
            dot={false}
          />
          <ChartGradientDefs />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

/** Matches backend `AnalyticsEvent.cost_estimate` scaling (compress.py). */
const COST_PER_TOKEN_SAVED = 1.2e-6

export function DashboardPage() {
  const [overview, setOverview] = useState<AnalyticsOverview | null>(null)
  const [overviewLoading, setOverviewLoading] = useState(true)
  const [historySeries, setHistorySeries] = useState<AnalyticsHistoryRow[] | null>(
    null,
  )
  const [recentActivity, setRecentActivity] = useState<AnalyticsRecentRow[]>([])
  const [recentState, setRecentState] = useState<
    'loading' | 'ok' | 'empty' | 'error'
  >('loading')

  useEffect(() => {
    void getAnalyticsOverview()
      .then(setOverview)
      .catch(() => setOverview(null))
      .finally(() => setOverviewLoading(false))
  }, [])

  useEffect(() => {
    void getAnalyticsHistory(30)
      .then((rows) => setHistorySeries(rows.length ? rows : null))
      .catch(() => setHistorySeries(null))
  }, [])

  useEffect(() => {
    void getAnalyticsRecent(10)
      .then((rows) => {
        setRecentActivity(rows)
        setRecentState(rows.length ? 'ok' : 'empty')
      })
      .catch(() => {
        setRecentState('error')
        setRecentActivity([])
      })
  }, [])

  const dailyFromApi = useMemo(() => {
    if (!historySeries?.length) return null
    return historySeries.map((r) => ({
      t: r.date.slice(5),
      saved: r.tokens_saved,
      usd: r.tokens_saved * COST_PER_TOKEN_SAVED,
    }))
  }, [historySeries])

  const sparkTokens = useMemo(() => {
    if (!dailyFromApi?.length) return null
    return dailyFromApi.slice(-7).map((d) => d.saved)
  }, [dailyFromApi])

  const sparkUsd = useMemo(() => {
    if (!dailyFromApi?.length) return null
    return dailyFromApi.slice(-7).map((d) => Math.max(0, Math.round(d.usd * 1e6)))
  }, [dailyFromApi])

  const kpiRows = useMemo(() => {
    const rows = kpi.map((row, i) => {
      if (!overview) return { ...row }
      if (i === 0) {
        return {
          ...row,
          value: overview.total_tokens_saved.toLocaleString(),
          sub: 'from API · /analytics/overview',
        }
      }
      if (i === 1) {
        return {
          ...row,
          value: `$${overview.cost_saved_usd.toFixed(0)}`,
          sub: 'from API · /analytics/overview',
        }
      }
      if (i === 2) {
        return {
          ...row,
          value: `${overview.compression_trend_pct}%`,
          sub: 'compression_trend_pct (overview)',
        }
      }
      return { ...row, sub: 'Demo · not wired to API' }
    })
    return rows.map((row, i) => {
      if (i === 0 && sparkTokens) return { ...row, spark: sparkTokens }
      if (i === 1 && sparkUsd) return { ...row, spark: sparkUsd }
      return row
    })
  }, [overview, sparkTokens, sparkUsd])

  return (
    <PageTransition>
      <div className="space-y-8">
        <div>
          <h1 className="mb-1">Dashboard</h1>
          <p className="text-sm text-muted-foreground">
            Token economics and compression performance at a glance.
            {overviewLoading ? (
              <span className="ml-2 text-caption">Loading overview…</span>
            ) : null}
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {kpiRows.map((k) => (
            <Card key={k.title} className="overflow-hidden">
              <CardHeader className="pb-2">
                <UiTooltip>
                  <TooltipTrigger asChild>
                    <CardTitle className="cursor-help">{k.title}</CardTitle>
                  </TooltipTrigger>
                  <TooltipContent>
                    Rolling aggregate for your workspace. Click Analytics for
                    detail.
                  </TooltipContent>
                </UiTooltip>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-end justify-between gap-2">
                  <span className="text-2xl font-semibold tabular-nums tracking-tight">
                    {k.value}
                  </span>
                  <span
                    className={cn(
                      'inline-flex items-center gap-0.5 text-xs font-mono',
                      k.up ? 'text-success' : 'text-error',
                    )}
                  >
                    {k.up ? (
                      <TrendingUp className="h-3 w-3" />
                    ) : (
                      <TrendingDown className="h-3 w-3" />
                    )}
                    {k.sub}
                  </span>
                </div>
                <MiniSparkline data={[...k.spark]} />
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>
                {dailyFromApi ? 'Tokens saved (daily, API)' : 'Tokens before vs after'}
              </CardTitle>
            </CardHeader>
            <CardContent className="pl-0">
              <ChartPanel>
                <ResponsiveContainer width="100%" height="100%">
                {dailyFromApi ? (
                  <LineChart
                    data={dailyFromApi}
                    margin={{ top: 8, right: 24, left: 0, bottom: 0 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" opacity={0.4} />
                    <XAxis dataKey="t" tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} width={40} />
                    <Tooltip
                      contentStyle={{
                        background: 'var(--color-surface)',
                        border: '1px solid var(--color-border)',
                        borderRadius: 12,
                        fontSize: 12,
                      }}
                      labelStyle={{ color: 'var(--color-caption)' }}
                    />
                    <Line type="monotone" dataKey="saved" name="Saved" stroke="url(#strokeGrad)" strokeWidth={2} dot={false} />
                    <ChartGradientDefs />
                  </LineChart>
                ) : (
                  <LineChart data={lineData} margin={{ top: 8, right: 24, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" opacity={0.4} />
                    <XAxis dataKey="t" tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} width={40} />
                    <Tooltip
                      contentStyle={{
                        background: 'var(--color-surface)',
                        border: '1px solid var(--color-border)',
                        borderRadius: 12,
                        fontSize: 12,
                      }}
                      labelStyle={{ color: 'var(--color-caption)' }}
                    />
                    <Line type="monotone" dataKey="before" name="Before" stroke="#64748b" strokeWidth={2} dot={false} />
                    <Line type="monotone" dataKey="after" name="After" stroke="url(#strokeGrad)" strokeWidth={2} dot={false} />
                    <ChartGradientDefs />
                  </LineChart>
                )}
                </ResponsiveContainer>
              </ChartPanel>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>
                {dailyFromApi ? 'Est. cost impact (daily, API)' : 'Cost savings over time'}
              </CardTitle>
            </CardHeader>
            <CardContent className="pl-0">
              <ChartPanel>
                <ResponsiveContainer width="100%" height="100%">
                {dailyFromApi ? (
                  <AreaChart
                    data={dailyFromApi}
                    margin={{ top: 8, right: 24, left: 0, bottom: 0 }}
                  >
                    <defs>
                      <linearGradient id="areaGradApi" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.35} />
                        <stop offset="100%" stopColor="#22d3ee" stopOpacity={0.05} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" opacity={0.4} />
                    <XAxis dataKey="t" tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} width={36} />
                    <Tooltip
                      contentStyle={{
                        background: 'var(--color-surface)',
                        border: '1px solid var(--color-border)',
                        borderRadius: 12,
                        fontSize: 12,
                      }}
                      formatter={(v) => [`$${Number(v ?? 0).toFixed(4)}`, 'Est.']}
                    />
                    <Area type="monotone" dataKey="usd" stroke="#6366f1" fill="url(#areaGradApi)" strokeWidth={2} />
                  </AreaChart>
                ) : (
                  <AreaChart data={areaData} margin={{ top: 8, right: 24, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#8b5cf6" stopOpacity={0.35} />
                        <stop offset="100%" stopColor="#22d3ee" stopOpacity={0.05} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" opacity={0.4} />
                    <XAxis dataKey="m" tick={{ fill: 'var(--color-caption)', fontSize: 11 }} axisLine={false} tickLine={false} />
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
                    <Area type="monotone" dataKey="usd" stroke="#6366f1" fill="url(#areaGrad)" strokeWidth={2} />
                  </AreaChart>
                )}
                </ResponsiveContainer>
              </ChartPanel>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader className="flex flex-row flex-wrap items-center justify-between gap-2">
            <CardTitle>Recent activity</CardTitle>
            {recentState === 'error' ? (
              <Badge variant="warning" className="text-[10px]">
                Offline · demo rows
              </Badge>
            ) : null}
          </CardHeader>
          <CardContent className="overflow-x-auto p-0">
            <table className="w-full min-w-[640px] text-left text-sm">
              <thead>
                <tr className="border-b border-border text-caption">
                  <th className="px-5 py-3 font-medium">Prompt preview</th>
                  <th className="px-5 py-3 font-medium">Tokens</th>
                  <th className="px-5 py-3 font-medium text-right">Compression</th>
                  <th className="px-5 py-3 font-medium text-right">Time</th>
                </tr>
              </thead>
              <tbody>
                {recentState === 'loading' ? (
                  [0, 1, 2].map((i) => (
                    <tr key={i} className="border-b border-border/60">
                      <td className="px-5 py-3" colSpan={4}>
                        <Skeleton className="h-4 w-full max-w-md" />
                      </td>
                    </tr>
                  ))
                ) : recentState === 'ok' ? (
                  recentActivity.map((row, idx) => (
                    <tr
                      key={`${row.time}-${idx}`}
                      className="border-b border-border/60 transition-colors hover:bg-surface-hover/50"
                    >
                      <td className="max-w-[280px] truncate px-5 py-3 text-muted-foreground">
                        {row.preview}
                      </td>
                      <td className="px-5 py-3 font-mono text-xs tabular-nums">
                        {row.before}
                        <span className="text-caption"> → </span>
                        {row.after}
                      </td>
                      <td className="px-5 py-3 text-right font-mono text-xs text-success tabular-nums">
                        {row.pct}%
                      </td>
                      <td className="px-5 py-3 text-right text-caption font-mono text-xs">
                        {formatRelativeShort(row.time)}
                      </td>
                    </tr>
                  ))
                ) : recentState === 'empty' ? (
                  <tr>
                    <td
                      className="px-5 py-8 text-center text-sm text-muted-foreground"
                      colSpan={4}
                    >
                      No compressions in the database yet. Use the Playground or{' '}
                      <code className="font-mono text-xs">POST /api/v1/compress</code>
                      .
                    </td>
                  </tr>
                ) : (
                  DEMO_ACTIVITY_FALLBACK.map((row) => (
                    <tr
                      key={row.preview}
                      className="border-b border-border/60 transition-colors hover:bg-surface-hover/50"
                    >
                      <td className="max-w-[280px] truncate px-5 py-3 text-muted-foreground">
                        {row.preview}
                      </td>
                      <td className="px-5 py-3 font-mono text-xs tabular-nums">
                        {row.before}
                        <span className="text-caption"> → </span>
                        {row.after}
                      </td>
                      <td className="px-5 py-3 text-right font-mono text-xs text-success tabular-nums">
                        {row.pct}%
                      </td>
                      <td className="px-5 py-3 text-right text-caption font-mono text-xs">
                        {row.time}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </CardContent>
        </Card>
      </div>
    </PageTransition>
  )
}
