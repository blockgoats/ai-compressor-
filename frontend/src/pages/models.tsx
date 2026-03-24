import { useEffect, useState } from 'react'

import { PageTransition } from '@/components/page-transition'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { ApiError, getMetaModels, type MetaModelRow } from '@/lib/api'

const FALLBACK: MetaModelRow[] = [
  {
    id: 'gpt-4.1',
    label: 'GPT-4.1',
    provider: 'openai',
    cost_hint: '$5 / 1M in',
    latency_hint: '~420ms p50',
    compat: 'Excellent',
    is_default: false,
  },
]

export function ModelsPage() {
  const [rows, setRows] = useState<MetaModelRow[]>(FALLBACK)
  const [provider, setProvider] = useState<string | null>(null)
  const [err, setErr] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    void getMetaModels()
      .then((res) => {
        setRows(res.models)
        setProvider(res.llm_provider)
        setErr(null)
      })
      .catch((e: unknown) => {
        setErr(e instanceof ApiError ? e.message : 'Could not load models')
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <PageTransition>
      <div className="space-y-8">
        <div>
          <h1 className="mb-1">Models</h1>
          <p className="text-sm text-muted-foreground">
            Compression profiles tuned per provider tokenizer and latency
            envelope.
            {provider ? (
              <span className="ml-2 font-mono text-xs text-caption">
                · Active provider: {provider}
              </span>
            ) : null}
          </p>
          {err ? (
            <p className="mt-2 text-xs text-warning">Using offline list: {err}</p>
          ) : null}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          {loading ? (
            [0, 1, 2, 3].map((i) => (
              <Card key={i}>
                <CardHeader>
                  <Skeleton className="h-5 w-40" />
                  <Skeleton className="mt-2 h-3 w-56" />
                </CardHeader>
                <CardContent className="space-y-2">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-3/4" />
                </CardContent>
              </Card>
            ))
          ) : null}
          {!loading &&
            rows.map((m) => (
            <Card key={m.id}>
              <CardHeader className="flex flex-row items-start justify-between gap-2">
                <div>
                  <CardTitle className="text-base text-foreground">
                    {m.label}
                  </CardTitle>
                  <p className="mt-1 font-mono text-[10px] text-caption">
                    {m.id} · {m.provider}
                  </p>
                </div>
                <div className="flex flex-col items-end gap-1">
                  <Badge variant="success">{m.compat}</Badge>
                  {m.is_default ? (
                    <Badge variant="default" className="text-[10px]">
                      Default
                    </Badge>
                  ) : null}
                </div>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <div className="flex justify-between gap-4">
                  <span className="text-caption">Cost / token</span>
                  <span className="font-mono tabular-nums text-foreground">
                    {m.cost_hint}
                  </span>
                </div>
                <div className="flex justify-between gap-4">
                  <span className="text-caption">Latency</span>
                  <span className="font-mono tabular-nums text-muted-foreground">
                    {m.latency_hint}
                  </span>
                </div>
                <p className="pt-2 text-xs text-caption">
                  Compression compatibility indicates expected stability of
                  semantic-preserving transforms.
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </PageTransition>
  )
}
