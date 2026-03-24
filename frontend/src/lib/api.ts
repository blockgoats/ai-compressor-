import { getApiV1Prefix } from '@/lib/env'

export const ACCESS_TOKEN_STORAGE_KEY = 'ramanujan_access_token'

export class ApiError extends Error {
  status: number
  body?: unknown

  constructor(message: string, status: number, body?: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.body = body
  }
}

export function getAccessToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY)
}

export function setAccessToken(token: string | null): void {
  if (typeof window === 'undefined') return
  if (token) localStorage.setItem(ACCESS_TOKEN_STORAGE_KEY, token)
  else localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY)
  window.dispatchEvent(new Event('ramanujan-auth'))
}

export type CompressMode = 'lossless' | 'lossy' | 'ramanujan'
export type CompressionLevel = 'low' | 'medium' | 'aggressive'

export type CompressRequestBody = {
  prompt: string
  mode: CompressMode
  compression_level: CompressionLevel
}

export type CompressResponse = {
  compressed_prompt: string
  tokens_before: number
  tokens_after: number
  compression_ratio: number
  insights: Record<string, unknown>
}

export type GenerateResponse = {
  output: string
  latency_ms: number
  tokens_used: number
}

export type CostSimulateResponse = {
  cost_without_compression_usd: number
  cost_with_compression_usd: number
  savings_pct: number
}

export type AnalyticsOverview = {
  total_tokens_saved: number
  cost_saved_usd: number
  compression_trend_pct: number
}

export type AnalyticsHistoryRow = {
  date: string
  tokens_saved: number
}

export type UserOut = {
  id: string
  email: string
}

export type TokenResponse = {
  access_token: string
  token_type?: string
}

function detailMessage(parsed: unknown, fallback: string): string {
  if (parsed && typeof parsed === 'object' && 'detail' in parsed) {
    const d = (parsed as { detail: unknown }).detail
    if (typeof d === 'string') return d
    if (Array.isArray(d)) return JSON.stringify(d)
  }
  return fallback
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const url = `${getApiV1Prefix()}${path.startsWith('/') ? path : `/${path}`}`
  const headers = new Headers(init.headers)
  if (
    !headers.has('Content-Type') &&
    init.body &&
    !(init.body instanceof FormData)
  ) {
    headers.set('Content-Type', 'application/json')
  }
  const token = getAccessToken()
  if (token && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${token}`)
  }
  const res = await fetch(url, { ...init, headers })
  const text = await res.text()
  let parsed: unknown = null
  if (text) {
    try {
      parsed = JSON.parse(text) as unknown
    } catch {
      parsed = text
    }
  }
  if (!res.ok) {
    throw new ApiError(
      detailMessage(parsed, `${res.status} ${res.statusText}`),
      res.status,
      parsed,
    )
  }
  return parsed as T
}

export function postJson<T>(path: string, body: unknown): Promise<T> {
  return apiFetch<T>(path, { method: 'POST', body: JSON.stringify(body) })
}

export function postCompress(body: CompressRequestBody): Promise<CompressResponse> {
  return postJson<CompressResponse>('/compress', body)
}

export function postGenerate(
  body: CompressRequestBody,
): Promise<GenerateResponse> {
  return postJson<GenerateResponse>('/generate', body)
}

export function postCostSimulate(monthlyTokens: number): Promise<CostSimulateResponse> {
  return postJson<CostSimulateResponse>('/cost-simulate', {
    monthly_tokens: monthlyTokens,
  })
}

export function getAnalyticsOverview(): Promise<AnalyticsOverview> {
  return apiFetch<AnalyticsOverview>('/analytics/overview')
}

export function getAnalyticsHistory(days = 14): Promise<AnalyticsHistoryRow[]> {
  const q = new URLSearchParams({ days: String(days) })
  return apiFetch<AnalyticsHistoryRow[]>(`/analytics/history?${q}`)
}

export type AnalyticsRecentRow = {
  preview: string
  before: number
  after: number
  pct: number
  time: string
}

export function getAnalyticsRecent(limit = 10): Promise<AnalyticsRecentRow[]> {
  const q = new URLSearchParams({ limit: String(limit) })
  return apiFetch<AnalyticsRecentRow[]>(`/analytics/recent?${q}`)
}

export function postAuthRegister(
  email: string,
  password: string,
): Promise<TokenResponse> {
  return postJson<TokenResponse>('/auth/register', { email, password })
}

export function postAuthLogin(email: string, password: string): Promise<TokenResponse> {
  return postJson<TokenResponse>('/auth/login', { email, password })
}

export function getAuthMe(): Promise<UserOut> {
  return apiFetch<UserOut>('/auth/me')
}

export type MetaModelRow = {
  id: string
  label: string
  provider: string
  cost_hint: string
  latency_hint: string
  compat: string
  is_default: boolean
}

export type MetaModelsResponse = {
  llm_provider: string
  default_model_id: string
  openai_model: string
  groq_default_model: string
  models: MetaModelRow[]
}

export function getMetaModels(): Promise<MetaModelsResponse> {
  return apiFetch<MetaModelsResponse>('/meta/models')
}
