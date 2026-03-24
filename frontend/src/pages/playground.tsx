import {
  ChevronDown,
  Download,
  FileJson,
  History,
  Sparkles,
  Terminal,
} from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { toast } from 'sonner'
import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip as RTooltip,
  XAxis,
  YAxis,
} from 'recharts'

import { ChartPanel } from '@/components/charts/chart-panel'
import { CopyButton } from '@/components/copy-button'
import { PageTransition } from '@/components/page-transition'
import { RamanujanMathBg } from '@/components/playground/ramanujan-math-bg'
import { SliderTokenBlocks } from '@/components/playground/slider-token-blocks'
import { TradeoffMiniChart } from '@/components/playground/tradeoff-mini-chart'
import { RippleButton } from '@/components/ui/ripple-button'
import { TokenFlow } from '@/components/visual/token-flow'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Label } from '@/components/ui/label'
import { Separator } from '@/components/ui/separator'
import { Slider } from '@/components/ui/slider'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip'
import { useDemoMode } from '@/hooks/use-demo-mode'
import { useMediaQuery } from '@/hooks/use-media-query'
import { usePromptHistory } from '@/hooks/use-prompt-history'
import {
  buildFrequencyHistogram,
  clusterPatterns,
  type CompressMode,
  compressPrompt,
  ramanujanMetrics,
  tokenizeWithMeta,
} from '@/lib/compression'
import { sliderToCompressionLevel } from '@/lib/compression-level'
import { ApiError, type GenerateResponse, postGenerate } from '@/lib/api'
import { getApiBaseUrlForDisplay } from '@/lib/env'
import { cn } from '@/lib/utils'

const SAMPLE =
  'You are an expert assistant. Please summarize the key findings from the attached paper, focusing on methodology and limitations. Keep the tone professional and cite section numbers when possible.'

const EXAMPLES = [
  {
    label: 'Research summary',
    text: 'Summarize this arXiv paper in 5 bullets. Emphasize novelty vs prior work.',
  },
  {
    label: 'Code review',
    text: 'Review the following TypeScript for security issues and suggest refactors.',
  },
  {
    label: 'Try compressing this →',
    text: SAMPLE,
  },
] as const

export function PlaygroundPage() {
  const { demoMode } = useDemoMode()
  const isMobile = useMediaQuery('(max-width: 1023px)')
  const [mobileTab, setMobileTab] = useState('input')

  const [prompt, setPrompt] = useState(SAMPLE)
  const [level, setLevel] = useState([50])
  const [mode, setMode] = useState<CompressMode>('lossy')
  const [llmSeeded, setLlmSeeded] = useState(false)
  const [apiLoading, setApiLoading] = useState(false)
  const [apiGen, setApiGen] = useState<GenerateResponse | null>(null)

  const { versions, saveVersion, removeVersion } = usePromptHistory()

  useEffect(() => {
    if (!demoMode) return
    queueMicrotask(() => {
      setPrompt(SAMPLE)
      setLevel([68])
      setMode('ramanujan')
      setLlmSeeded(true)
    })
  }, [demoMode])

  const live = useMemo(
    () => compressPrompt(prompt, level[0], mode),
    [prompt, level, mode],
  )

  const pctSaved = live.pctSaved
  const rMetrics =
    mode === 'ramanujan'
      ? ramanujanMetrics(level[0], pctSaved)
      : null

  const tokenWords = useMemo(
    () => (prompt.trim() ? prompt.split(/\s+/).slice(0, 24) : []),
    [prompt],
  )

  const freqData = useMemo(
    () => buildFrequencyHistogram(prompt).map((x) => ({ name: x.word, n: x.count })),
    [prompt],
  )

  const clusters = useMemo(() => clusterPatterns(prompt), [prompt])

  const metaSegments = useMemo(
    () => tokenizeWithMeta(live.compressed, live.after),
    [live],
  )

  const compressionLevel = useMemo(
    () => sliderToCompressionLevel(level[0]),
    [level],
  )

  useEffect(() => {
    setApiGen(null)
  }, [prompt, mode, compressionLevel])

  const exportJson = useMemo(
    () =>
      JSON.stringify(
        {
          model: 'gpt-4.1',
          mode,
          level: level[0],
          compression_level: compressionLevel,
          prompt,
          compressed: live.compressed,
        },
        null,
        2,
      ),
    [mode, level, prompt, live.compressed, compressionLevel],
  )

  const apiCurl = useMemo(() => {
    const body = {
      prompt: prompt.slice(0, 2000),
      mode,
      compression_level: compressionLevel,
    }
    const base = getApiBaseUrlForDisplay()
    return `curl -s ${base}/api/v1/generate \\
  -H "Authorization: Bearer $ACCESS_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '${JSON.stringify(body)}'`
  }, [prompt, mode, compressionLevel])

  async function runGenerate() {
    if (!prompt.trim()) {
      toast.error('Add a prompt first')
      return
    }
    setApiLoading(true)
    setApiGen(null)
    try {
      const res = await postGenerate({
        prompt: prompt.slice(0, 200_000),
        mode,
        compression_level: compressionLevel,
      })
      setApiGen(res)
      setLlmSeeded(true)
      toast.success('Compress + generate finished')
    } catch (e) {
      const msg =
        e instanceof ApiError ? e.message : 'Request failed — is the API running?'
      toast.error(msg)
    } finally {
      setApiLoading(false)
    }
  }

  const inputPanel = (
    <Card
      className={cn(
        'relative flex flex-col overflow-hidden',
        mode === 'ramanujan' &&
          'border-indigo/35 shadow-[0_0_0_1px_rgba(99,102,241,0.2),0_8px_40px_-12px_rgba(99,102,241,0.35)]',
      )}
    >
      {mode === 'ramanujan' ? <RamanujanMathBg /> : null}
      <CardHeader className="relative p-5 pb-0">
        <CardTitle>Input</CardTitle>
      </CardHeader>
      <CardContent className="relative flex flex-1 flex-col gap-4 p-5">
        {!prompt.trim() && !demoMode ? (
          <div className="rounded-xl border border-dashed border-border bg-surface-secondary/50 p-6 text-center">
            <p className="mb-3 text-sm text-muted-foreground">
              Start from an example — no blank canvas.
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {EXAMPLES.map((ex) => (
                <Button
                  key={ex.label}
                  type="button"
                  variant="secondary"
                  size="sm"
                  onClick={() => setPrompt(ex.text)}
                >
                  {ex.label}
                </Button>
              ))}
            </div>
          </div>
        ) : null}

        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Paste your prompt here..."
          className="min-h-[200px] w-full resize-y rounded-xl border border-border bg-surface-secondary p-4 font-mono text-sm text-foreground placeholder:text-caption focus-visible:outline-none focus-visible:ring-focus"
        />

        <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
          <span className="text-caption">Live estimate</span>
          <span className="font-mono tabular-nums text-foreground">
            <Tooltip>
              <TooltipTrigger asChild>
                <span className="cursor-help">
                  {live.before} tok
                </span>
              </TooltipTrigger>
              <TooltipContent>Characters ÷ 4 (approximate)</TooltipContent>
            </Tooltip>
            <span className="text-caption"> → </span>
            <span>{live.after} tok</span>
            <span className="ml-2 text-success">~{pctSaved}% saved</span>
          </span>
        </div>

        <TokenFlow before={live.before} after={live.after} />

        <div className="space-y-6">
          <div>
            <div className="mb-1 flex items-center justify-between gap-2">
              <Label className="text-caption">Compression</Label>
              <span className="font-mono text-xs text-muted-foreground">
                {level[0]}%
              </span>
            </div>
            <div className="mb-1 flex justify-between text-[10px] uppercase tracking-wide text-caption">
              <span>High accuracy</span>
              <span>High compression</span>
            </div>
            <Slider
              value={level}
              onValueChange={setLevel}
              max={100}
              step={1}
              className="py-2"
            />
            <SliderTokenBlocks words={tokenWords} level={level[0]} className="mt-2" />
            <TradeoffMiniChart level={level[0]} />
          </div>

          <div>
            <Label className="mb-2 block text-caption">Mode</Label>
            <div className="flex flex-wrap gap-2">
              {(
                [
                  ['lossless', 'Lossless'],
                  ['lossy', 'Lossy'],
                  ['ramanujan', 'Ramanujan'],
                ] as const
              ).map(([id, label]) => (
                <Button
                  key={id}
                  type="button"
                  variant={mode === id ? 'default' : 'secondary'}
                  size="sm"
                  className={cn(
                    'gap-2 transition-shadow',
                    mode === id &&
                      id === 'ramanujan' &&
                      'shadow-[0_0_20px_-4px_rgba(139,92,246,0.55)]',
                  )}
                  onClick={() => setMode(id)}
                >
                  {label}
                  {id === 'ramanujan' ? (
                    <Badge variant="gradient" className="text-[10px]">
                      Experimental
                    </Badge>
                  ) : null}
                </Button>
              ))}
            </div>
          </div>
        </div>

        <RippleButton
          type="button"
          className="w-full bg-gradient-primary-animated"
          size="lg"
          disabled={apiLoading}
          onClick={() => void runGenerate()}
        >
          {apiLoading ? 'Calling API…' : 'Compress & Generate'}
        </RippleButton>
      </CardContent>
    </Card>
  )

  const metricsBar = (
    <Card>
      <CardContent className="p-4">
        <div className="flex flex-wrap gap-4 text-sm">
          <Tooltip>
            <TooltipTrigger asChild>
              <div className="cursor-help">
                <p className="text-caption text-xs">Tokens before</p>
                <p className="font-mono text-lg tabular-nums">{live.before}</p>
              </div>
            </TooltipTrigger>
            <TooltipContent>Live estimate</TooltipContent>
          </Tooltip>
          <Separator orientation="vertical" className="hidden h-10 sm:block" />
          <Tooltip>
            <TooltipTrigger asChild>
              <div className="cursor-help">
                <p className="text-caption text-xs">Tokens after</p>
                <p className="font-mono text-lg tabular-nums">{live.after}</p>
              </div>
            </TooltipTrigger>
            <TooltipContent>After transform</TooltipContent>
          </Tooltip>
          <Separator orientation="vertical" className="hidden h-10 sm:block" />
          <div>
            <p className="text-caption text-xs">% saved</p>
            <p className="font-mono text-lg text-success tabular-nums">
              {pctSaved}%
            </p>
          </div>
          <div>
            <p className="text-caption text-xs">Latency</p>
            <p className="font-mono text-lg tabular-nums">
              {apiGen ? apiGen.latency_ms : live.latencyMs}ms
            </p>
            {apiGen ? (
              <p className="text-[10px] text-caption">
                LLM tokens: {apiGen.tokens_used}
              </p>
            ) : null}
          </div>
        </div>
      </CardContent>
    </Card>
  )

  const outputTabs = (
    <Card className="flex-1">
      <CardHeader className="pb-0">
        <CardTitle>Output</CardTitle>
      </CardHeader>
      <CardContent className="p-5 pt-2">
        <Tabs defaultValue="compressed" className="w-full">
          <TabsList
            className={cn(
              'w-full justify-start overflow-x-auto rounded-none bg-transparent p-0',
              isMobile && 'gap-1',
            )}
          >
            {(['compressed', 'llm', 'diff'] as const).map((v) => (
              <TabsTrigger
                key={v}
                value={v}
                className={cn(
                  'group relative rounded-none border-b-2 border-transparent bg-transparent px-3 py-2 text-muted-foreground data-[state=active]:border-transparent data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none',
                )}
              >
                <span className="relative z-10">
                  {v === 'compressed'
                    ? 'Compressed'
                    : v === 'llm'
                      ? 'LLM output'
                      : 'Diff view'}
                </span>
                <span className="absolute bottom-0 left-3 right-3 h-0.5 scale-x-0 rounded-full bg-gradient-to-r from-indigo via-violet to-cyan transition-transform duration-300 group-data-[state=active]:scale-x-100" />
              </TabsTrigger>
            ))}
          </TabsList>
          <TabsContent value="compressed" className="mt-3">
            <p className="mb-2 text-xs text-caption">
              Hover tokens for explainability
            </p>
            <div className="min-h-[120px] rounded-xl border border-border bg-surface-secondary p-4 font-mono text-sm leading-relaxed">
              {metaSegments.map(({ segment, meta }, i) => (
                <Tooltip key={`${i}-${segment.slice(0, 4)}`}>
                  <TooltipTrigger asChild>
                    <span
                      className={cn(
                        'inline-block cursor-help rounded px-0.5',
                        segment.trim() &&
                          /[a-z]/i.test(segment) &&
                          'bg-surface-hover/80',
                      )}
                    >
                      {segment}
                    </span>
                  </TooltipTrigger>
                  <TooltipContent className="max-w-xs text-left text-xs">
                    {segment.trim() ? (
                      <>
                        <p className="font-mono text-[10px] text-caption">
                          {meta.pattern}
                        </p>
                        <p className="mt-1">{meta.reason}</p>
                        <p className="mt-1 font-mono text-caption">
                          freq score {meta.frequency}
                        </p>
                      </>
                    ) : (
                      'Whitespace'
                    )}
                  </TooltipContent>
                </Tooltip>
              ))}
            </div>
          </TabsContent>
          <TabsContent value="llm" className="mt-3">
            <div className="min-h-[120px] rounded-xl border border-border bg-surface-secondary p-4 font-mono text-sm text-muted-foreground">
              {apiGen ? (
                <span className="whitespace-pre-wrap">{apiGen.output}</span>
              ) : llmSeeded ? (
                <>
                  A concise summary of the paper’s methodology section
                  highlights experiments A–C; limitations are noted in §4 regarding
                  sample size.
                </>
              ) : (
                'Run pipeline to call the backend /generate endpoint.'
              )}
            </div>
          </TabsContent>
          <TabsContent value="diff" className="mt-3">
            <div className="grid gap-3 md:grid-cols-2">
              <div className="rounded-xl border border-border bg-surface-secondary p-3 font-mono text-xs">
                <p className="mb-2 text-caption">Before</p>
                {prompt.slice(0, 420)}
                {prompt.length > 420 ? '…' : ''}
              </div>
              <div className="rounded-xl border border-border bg-surface-secondary p-3 font-mono text-xs">
                <p className="mb-2 text-caption">After</p>
                {live.compressed}
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )

  const devTools = (
    <details className="group rounded-2xl border border-border bg-surface">
      <summary className="flex cursor-pointer list-none items-center justify-between gap-2 px-5 py-4 font-medium text-foreground">
        <span className="flex items-center gap-2 text-sm">
          <Terminal className="h-4 w-4 text-caption" />
          Developer tools
        </span>
        <ChevronDown className="h-4 w-4 text-caption transition-transform group-open:rotate-180" />
      </summary>
      <div className="space-y-4 border-t border-border px-5 pb-5 pt-2">
        <div className="grid gap-4 lg:grid-cols-2">
          <Card className="border-border/80">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="flex items-center gap-2 text-sm">
                <History className="h-4 w-4" />
                Prompt versions
              </CardTitle>
              <Button
                type="button"
                variant="secondary"
                size="sm"
                onClick={() => {
                  saveVersion(prompt)
                  toast.success('Snapshot saved')
                }}
              >
                Save snapshot
              </Button>
            </CardHeader>
            <CardContent className="space-y-2">
              {versions.length === 0 ? (
                <p className="text-xs text-caption">No snapshots yet.</p>
              ) : (
                <ul className="max-h-40 space-y-2 overflow-y-auto text-xs">
                  {versions.map((v) => (
                    <li
                      key={v.id}
                      className="flex items-start justify-between gap-2 rounded-lg bg-surface-secondary px-2 py-2"
                    >
                      <p className="line-clamp-2 flex-1 font-mono text-muted-foreground">
                        {v.text.slice(0, 120)}
                        {v.text.length > 120 ? '…' : ''}
                      </p>
                      <div className="flex shrink-0 flex-col gap-1">
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          className="h-7 text-[10px]"
                          onClick={() => {
                            setPrompt(v.text)
                            toast.message('Restored version')
                          }}
                        >
                          Restore
                        </Button>
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          className="h-7 text-[10px] text-error"
                          onClick={() => removeVersion(v.id)}
                        >
                          Remove
                        </Button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
              {versions[0] ? (
                <p className="text-[10px] text-caption">
                  Diff vs current:{' '}
                  <span className="font-mono text-foreground">
                    {prompt.length - versions[0].text.length >= 0 ? '+' : ''}
                    {prompt.length - versions[0].text.length} chars
                  </span>
                </p>
              ) : null}
            </CardContent>
          </Card>

          <Card className="border-border/80">
            <CardHeader>
              <CardTitle className="text-sm">Reproducibility</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-xs">
              <div className="flex justify-between gap-2">
                <span className="text-caption">Model</span>
                <span className="font-mono text-foreground">gpt-4.1</span>
              </div>
              <div className="flex justify-between gap-2">
                <span className="text-caption">Config</span>
                <span className="font-mono text-foreground">
                  {mode} · {compressionLevel} ({level[0]}%)
                </span>
              </div>
              <CopyButton text={apiCurl} size="sm" className="w-full justify-center" />
              <p className="text-caption">Copies an exact curl template.</p>
            </CardContent>
          </Card>
        </div>

        <div className="flex flex-wrap gap-2">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button type="button" variant="secondary" size="sm">
                <Download className="mr-2 h-4 w-4" />
                Export
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start">
              <DropdownMenuItem
                onClick={() => {
                  void navigator.clipboard.writeText(live.compressed)
                  toast.success('Compressed prompt copied')
                }}
              >
                Copy compressed prompt
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => {
                  void navigator.clipboard.writeText(exportJson)
                  toast.success('JSON copied')
                }}
              >
                <FileJson className="mr-2 h-4 w-4" />
                Copy JSON config
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => {
                  void navigator.clipboard.writeText(apiCurl)
                  toast.success('cURL copied')
                }}
              >
                Copy API request
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </details>
  )

  const insightsCard = (
    <Card
      className={cn(
        mode === 'ramanujan' && 'ring-1 ring-indigo/30',
      )}
    >
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          Compression insights
          {mode === 'ramanujan' ? (
            <Badge variant="gradient" className="text-[10px]">
              <Sparkles className="mr-1 h-3 w-3" />
              Ramanujan
            </Badge>
          ) : null}
        </CardTitle>
      </CardHeader>
      <CardContent className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-3">
          <ul className="space-y-2 text-sm text-muted-foreground">
            <li>
              <span className="text-foreground">Transformation steps</span>
              <ol className="mt-2 list-decimal space-y-1 pl-4 text-xs">
                <li>Strip redundant system boilerplate</li>
                <li>Merge parallel instructions</li>
                <li>
                  Quantize low-salience connectors
                  {mode === 'ramanujan' ? ' (spectral)' : ''}
                </li>
              </ol>
            </li>
            {rMetrics ? (
              <li className="border-t border-border pt-2">
                <span className="text-foreground">Math score</span>{' '}
                <span className="font-mono">
                  {rMetrics.mathScore.toFixed(3)}
                </span>
                <br />
                <span className="text-foreground">Pattern density</span>{' '}
                <span className="font-mono">
                  {rMetrics.patternDensity.toFixed(3)}
                </span>
                <br />
                <span className="text-foreground">Periodic tokens</span>{' '}
                <span className="font-mono">
                  {rMetrics.periodicity.toFixed(3)}
                </span>
              </li>
            ) : null}
          </ul>
        </div>
        <div>
          <p className="mb-2 text-xs text-caption">Pattern clusters</p>
          <div className="space-y-1 rounded-xl border border-border bg-surface-secondary p-3 font-mono text-xs">
            {clusters.length === 0 ? (
              <span className="text-caption">No strong repeats detected</span>
            ) : (
              clusters.map((c) => (
                <div key={c.phrase} className="flex justify-between gap-2">
                  <span className="text-warning">{c.phrase}</span>
                  <span className="tabular-nums text-caption">×{c.hits}</span>
                </div>
              ))
            )}
          </div>
        </div>
        <div>
          <p className="mb-2 text-xs text-caption">Token frequency</p>
          <ChartPanel heightClass="h-32">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={freqData} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
                <XAxis dataKey="name" tick={{ fontSize: 9, fill: 'var(--color-caption)' }} axisLine={false} tickLine={false} />
                <YAxis hide />
                <RTooltip
                  contentStyle={{
                    background: 'var(--color-surface)',
                    border: '1px solid var(--color-border)',
                    borderRadius: 8,
                    fontSize: 11,
                  }}
                />
                <Bar dataKey="n" fill="url(#barGrad)" radius={[4, 4, 0, 0]} />
                <defs>
                  <linearGradient id="barGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#6366f1" />
                    <stop offset="100%" stopColor="#22d3ee" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </ChartPanel>
        </div>
      </CardContent>
    </Card>
  )

  const desktop = (
    <>
      <div className="grid gap-6 lg:grid-cols-2">
        {inputPanel}
        <div className="flex flex-col gap-4">
          {metricsBar}
          {outputTabs}
        </div>
      </div>
      {devTools}
      {insightsCard}
    </>
  )

  const mobile = (
    <>
      <Tabs value={mobileTab} onValueChange={setMobileTab} className="w-full">
        <TabsList className="mb-4 w-full justify-between rounded-xl bg-surface-secondary p-1">
          {[
            ['input', 'Input'],
            ['output', 'Output'],
            ['insights', 'Insights'],
          ].map(([id, label]) => (
            <TabsTrigger
              key={id}
              value={id}
              className="group relative flex-1 rounded-lg data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none"
            >
              <span className="relative z-10">{label}</span>
              <span className="absolute bottom-0 left-2 right-2 h-0.5 scale-x-0 rounded-full bg-gradient-to-r from-indigo to-cyan transition-transform group-data-[state=active]:scale-x-100" />
            </TabsTrigger>
          ))}
        </TabsList>
        <TabsContent value="input">{inputPanel}</TabsContent>
        <TabsContent value="output" className="space-y-4">
          {metricsBar}
          {outputTabs}
        </TabsContent>
        <TabsContent value="insights" className="space-y-4">
          {insightsCard}
          {devTools}
        </TabsContent>
      </Tabs>
    </>
  )

  return (
    <PageTransition>
      <div className="space-y-6">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="mb-1">Playground</h1>
            <p className="text-sm text-muted-foreground">
              Live compression preview, token flow, and reproducible API calls.
            </p>
          </div>
          {demoMode ? (
            <Badge variant="gradient" className="font-mono text-[10px]">
              Demo mode · preloaded
            </Badge>
          ) : null}
        </div>

        {isMobile ? mobile : desktop}
      </div>
    </PageTransition>
  )
}
