import { PageTransition } from '@/components/page-transition'
import { CopyButton } from '@/components/copy-button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { getApiBaseUrlForDisplay, getApiV1Prefix } from '@/lib/env'

const PY = `import httpx

r = httpx.post(
    "${getApiV1Prefix()}/compress",
    headers={"Authorization": "Bearer $ACCESS_TOKEN"},
    json={
        "prompt": "Your long prompt...",
        "mode": "lossy",
        "compression_level": "medium",
    },
)
print(r.json())`

const NODE = `const r = await fetch('${getApiV1Prefix()}/compress', {
  method: 'POST',
  headers: {
    Authorization: 'Bearer ' + process.env.ACCESS_TOKEN,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: 'Your long prompt...',
    mode: 'lossy',
    compression_level: 'medium',
  }),
});
console.log(await r.json());`

function CodeBlock({ title, code }: { title: string; code: string }) {
  return (
    <div className="rounded-xl border border-border bg-surface-secondary">
      <div className="flex items-center justify-between border-b border-border px-4 py-2">
        <span className="text-xs font-medium text-caption">{title}</span>
        <CopyButton text={code} size="sm" className="h-8 w-8" />
      </div>
      <pre className="max-h-[280px] overflow-auto p-4 font-mono text-xs leading-relaxed text-muted-foreground">
        <code>{code}</code>
      </pre>
    </div>
  )
}

export function ApiPage() {
  return (
    <PageTransition>
      <div className="space-y-8">
        <div>
          <h1 className="mb-1">API</h1>
          <p className="text-sm text-muted-foreground">
            REST endpoints and typed SDK examples with copy-to-clipboard.
          </p>
          <p className="mt-1 font-mono text-xs text-caption break-all">
            Effective base: {getApiV1Prefix()} — set{' '}
            <code className="text-foreground">VITE_API_BASE_URL</code> or leave empty to
            use the Vite <code className="text-foreground">/api</code> proxy.
          </p>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>POST /compress</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-muted-foreground">
              <p>
                Compress a prompt and receive token counts, diff metadata, and
                optional model routing hints.
              </p>
              <p className="font-mono text-xs text-foreground break-all">
                {getApiV1Prefix()}/compress
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>POST /generate</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-muted-foreground">
              <p>
                One-shot compress + generate with the same session id for
                analytics correlation.
              </p>
              <p className="font-mono text-xs text-foreground break-all">
                {getApiV1Prefix()}/generate
              </p>
            </CardContent>
          </Card>
        </div>

        <Separator />

        <Card>
          <CardHeader>
            <CardTitle className="text-base">More endpoints</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 font-mono text-xs text-muted-foreground">
            <p className="break-all">
              <span className="text-foreground">GET</span> {getApiV1Prefix()}/health
            </p>
            <p className="break-all">
              <span className="text-foreground">GET</span> {getApiV1Prefix()}/meta/models
            </p>
            <p className="break-all">
              <span className="text-foreground">POST</span> {getApiV1Prefix()}
              /token-estimate
            </p>
            <p className="break-all">
              <span className="text-foreground">GET</span> {getApiV1Prefix()}/analytics/overview
            </p>
            <p className="break-all">
              <span className="text-foreground">GET</span> {getApiV1Prefix()}/analytics/history
            </p>
            <p className="break-all">
              <span className="text-foreground">GET</span> {getApiV1Prefix()}/analytics/recent
            </p>
            <p className="break-all">
              <span className="text-foreground">POST</span> {getApiV1Prefix()}/cost-simulate
            </p>
            <p className="break-all">
              <span className="text-foreground">POST</span> {getApiV1Prefix()}/auth/login · /register
            </p>
            <p className="break-all">
              OpenAPI:{' '}
              <a
                className="text-indigo underline underline-offset-2"
                href={`${getApiBaseUrlForDisplay()}/api/v1/openapi.json`}
                target="_blank"
                rel="noreferrer"
              >
                {getApiBaseUrlForDisplay()}/api/v1/openapi.json
              </a>
            </p>
          </CardContent>
        </Card>

        <div className="grid gap-6 lg:grid-cols-2">
          <div>
            <h3 className="mb-3 text-sm font-medium text-foreground">Python</h3>
            <CodeBlock title="client.py" code={PY} />
          </div>
          <div>
            <h3 className="mb-3 text-sm font-medium text-foreground">Node</h3>
            <CodeBlock title="compress.mjs" code={NODE} />
          </div>
        </div>
      </div>
    </PageTransition>
  )
}
