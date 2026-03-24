import { useState } from 'react'
import { toast } from 'sonner'

import { PageTransition } from '@/components/page-transition'
import { CopyButton } from '@/components/copy-button'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Separator } from '@/components/ui/separator'
import { Switch } from '@/components/ui/switch'
import { useAuth } from '@/hooks/use-auth'
import { ApiError, getAccessToken } from '@/lib/api'

const MASKED_KEY = 'sk_live_••••••••••••8f3a'

export function SettingsPage() {
  const { user, loading, login, register, logout, tokenExpiresAt } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)

  async function handleLogin() {
    setBusy(true)
    try {
      await login(email, password)
      toast.success('Signed in')
      setPassword('')
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : 'Login failed')
    } finally {
      setBusy(false)
    }
  }

  async function handleRegister() {
    setBusy(true)
    try {
      await register(email, password)
      toast.success('Account created')
      setPassword('')
    } catch (e) {
      toast.error(e instanceof ApiError ? e.message : 'Registration failed')
    } finally {
      setBusy(false)
    }
  }

  const token = typeof window !== 'undefined' ? getAccessToken() : null

  return (
    <PageTransition>
      <div className="space-y-8">
        <div>
          <h1 className="mb-1">Settings</h1>
          <p className="text-sm text-muted-foreground">
            Profile, keys, billing, and team access.
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Account (JWT)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {loading ? (
              <p className="text-sm text-muted-foreground">Loading…</p>
            ) : user ? (
              <div className="space-y-1 text-sm">
                <p>
                  Signed in as{' '}
                  <span className="font-mono text-foreground">{user.email}</span>
                </p>
                {tokenExpiresAt ? (
                  <p className="text-xs text-caption">
                    Access token expires{' '}
                    {new Date(tokenExpiresAt).toLocaleString(undefined, {
                      dateStyle: 'medium',
                      timeStyle: 'short',
                    })}{' '}
                    (sign in again to refresh).
                  </p>
                ) : null}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                Register or log in against{' '}
                <code className="rounded bg-surface-secondary px-1 font-mono text-xs">
                  POST /api/v1/auth/*
                </code>
                . Use the same bearer token for API calls.
              </p>
            )}
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="space-y-2">
                <label className="text-xs text-caption" htmlFor="auth-email">
                  Email
                </label>
                <Input
                  id="auth-email"
                  type="email"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="font-sans"
                  placeholder="you@company.com"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs text-caption" htmlFor="auth-pass">
                  Password (8+ chars)
                </label>
                <Input
                  id="auth-pass"
                  type="password"
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="font-sans"
                />
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              <Button
                type="button"
                disabled={busy}
                onClick={() => void handleRegister()}
              >
                Register
              </Button>
              <Button
                type="button"
                variant="secondary"
                disabled={busy}
                onClick={() => void handleLogin()}
              >
                Log in
              </Button>
              {user ? (
                <Button
                  type="button"
                  variant="outline"
                  disabled={busy}
                  onClick={() => {
                    logout()
                    toast.message('Signed out')
                  }}
                >
                  Log out
                </Button>
              ) : null}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Access token</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex flex-wrap items-center gap-2 rounded-xl border border-border bg-surface-secondary px-4 py-3">
              <code className="flex-1 font-mono text-sm break-all">
                {token ? `${token.slice(0, 14)}…` : MASKED_KEY}
              </code>
              {token ? <CopyButton text={token} /> : null}
            </div>
            <p className="text-xs text-caption">
              After login, copy your JWT for{' '}
              <code className="font-mono">Authorization: Bearer</code>. API key
              products can stay separate from JWT auth.
            </p>
          </CardContent>
        </Card>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card className="border-dashed border-border/80">
            <CardHeader className="flex flex-row flex-wrap items-center justify-between gap-2">
              <CardTitle>Billing</CardTitle>
              <Badge variant="default" className="text-[10px]">
                Coming soon
              </Badge>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground">
                Plans and usage billing are not connected to this API yet. Use your
                provider dashboard for token spend.
              </p>
              <div className="flex items-center justify-between rounded-xl border border-border bg-surface-secondary/50 px-4 py-3 opacity-60">
                <div>
                  <p className="text-sm font-medium">Pro</p>
                  <p className="text-xs text-caption">Placeholder</p>
                </div>
                <Button size="sm" variant="secondary" type="button" disabled>
                  Manage
                </Button>
              </div>
              <Separator />
              <div className="flex items-center justify-between opacity-60">
                <span className="text-sm text-muted-foreground">Usage alerts</span>
                <Switch disabled defaultChecked={false} />
              </div>
            </CardContent>
          </Card>

          <Card className="border-dashed border-border/80">
            <CardHeader className="flex flex-row flex-wrap items-center justify-between gap-2">
              <CardTitle>Team</CardTitle>
              <Badge variant="default" className="text-[10px]">
                Coming soon
              </Badge>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-sm text-muted-foreground">
                Multi-user workspaces will be added with a future API. For now, JWT
                identifies a single account.
              </p>
              <div className="flex flex-wrap gap-2 opacity-60">
                <Input
                  disabled
                  placeholder="email@company.com"
                  className="max-w-xs font-sans"
                />
                <Button type="button" variant="default" disabled>
                  Invite
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </PageTransition>
  )
}
