/**
 * Base URL for API requests (no trailing slash).
 * - Empty / `proxy`: same-origin (`/api/...`) so Vite `server.proxy` can forward to the backend.
 * - Absolute URL: direct calls (e.g. production or explicit dev URL).
 */
export function getApiBaseUrl(): string {
  const raw = import.meta.env.VITE_API_BASE_URL
  if (typeof raw === 'string') {
    const t = raw.trim()
    if (t === '' || t === 'proxy') return ''
    return t.replace(/\/$/, '')
  }
  if (import.meta.env.DEV) return ''
  if (typeof window !== 'undefined') return ''
  return 'http://127.0.0.1:8000'
}

export function getApiV1Prefix(): string {
  const base = getApiBaseUrl()
  return base ? `${base}/api/v1` : '/api/v1'
}

/** Absolute base for curl snippets and docs (browser origin when using proxy). */
export function getApiBaseUrlForDisplay(): string {
  const base = getApiBaseUrl()
  if (base) return base
  if (typeof window !== 'undefined') return window.location.origin
  return 'http://127.0.0.1:8000'
}
