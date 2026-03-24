export type CompressMode = 'lossless' | 'lossy' | 'ramanujan'

export type CompressionResult = {
  compressed: string
  removed: string[]
  before: number
  after: number
  latencyMs: number
  pctSaved: number
}

/** Rough token estimate (chars / 4), monospace-friendly */
export function estimateTokens(text: string): number {
  if (!text.trim()) return 0
  return Math.max(1, Math.ceil(text.length / 4))
}

function dropFactor(level: number, mode: CompressMode): number {
  const t = level / 100
  if (mode === 'lossless') return 0.04 + t * 0.08
  if (mode === 'ramanujan') return 0.12 + t * 0.28
  return 0.08 + t * 0.2
}

export function compressPrompt(
  input: string,
  level: number,
  mode: CompressMode,
): CompressionResult {
  const words = input.trim() ? input.split(/\s+/) : []
  const df = dropFactor(level, mode)
  const drop = Math.min(
    Math.max(0, Math.floor(words.length * df)),
    Math.max(0, words.length - 1),
  )
  const kept = words.slice(drop)
  const compressed = kept.join(' ')
  const before = estimateTokens(input)
  const after = Math.max(1, estimateTokens(compressed))
  const pctSaved = before <= 0 ? 0 : Math.round(((before - after) / before) * 100)
  return {
    compressed,
    removed: words.slice(0, drop),
    before,
    after,
    latencyMs: 90 + Math.round(level * 0.45) + (mode === 'ramanujan' ? 40 : 0),
    pctSaved,
  }
}

export type TokenMeta = {
  text: string
  reason: string
  frequency: number
  pattern: string
}

/** Per-token explainability for compressed output (demo metadata) */
export function tokenizeWithMeta(
  compressed: string,
  seed: number,
): { segment: string; meta: TokenMeta }[] {
  const parts = compressed.split(/(\s+)/)
  const reasons = [
    'Redundant qualifier',
    'Repeated instruction phrase',
    'Low-information connector',
    'Collapsible citation tail',
  ]
  const patterns = [
    'instruction boilerplate',
    'parallel structure',
    'section reference',
    'hedging cluster',
  ]
  let i = 0
  return parts.map((segment) => {
    const isSpace = /^\s+$/.test(segment)
    const idx = i++
    const hash = (seed + idx * 17 + segment.length) % 1000
    const meta: TokenMeta = {
      text: segment,
      reason: isSpace ? '—' : reasons[hash % reasons.length],
      frequency: isSpace ? 0 : 3 + (hash % 12),
      pattern: isSpace ? '—' : patterns[hash % patterns.length],
    }
    return { segment, meta }
  })
}

export function ramanujanMetrics(level: number, pctSaved: number) {
  const mathScore = 0.55 + (pctSaved / 100) * 0.35 + (level / 100) * 0.08
  const patternDensity = 0.2 + (level / 100) * 0.55
  const periodicity = Math.min(0.99, 0.15 + (pctSaved / 120))
  return {
    mathScore: Math.min(0.99, mathScore),
    patternDensity: Math.min(0.99, patternDensity),
    periodicity,
  }
}

export function buildFrequencyHistogram(text: string) {
  const words = text.toLowerCase().match(/\b[a-z]{3,}\b/g) ?? []
  const counts = new Map<string, number>()
  for (const w of words) {
    counts.set(w, (counts.get(w) ?? 0) + 1)
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([word, count]) => ({ word, count }))
}

export function clusterPatterns(text: string) {
  const lower = text.toLowerCase()
  const phrases = [
    { phrase: 'you are', hits: (lower.match(/you are/g) ?? []).length },
    { phrase: 'please summarize', hits: (lower.match(/please summarize/g) ?? []).length },
    { phrase: 'section', hits: (lower.match(/section/g) ?? []).length },
    { phrase: 'methodology', hits: (lower.match(/methodology/g) ?? []).length },
  ]
  return phrases.filter((p) => p.hits > 0)
}
