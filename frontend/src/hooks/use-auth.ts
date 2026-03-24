import { useCallback, useEffect, useState } from 'react'

import {
  ACCESS_TOKEN_STORAGE_KEY,
  getAccessToken,
  getAuthMe,
  postAuthLogin,
  postAuthRegister,
  setAccessToken,
  type UserOut,
} from '@/lib/api'
import { getJwtExpMs } from '@/lib/jwt'

export function useAuth() {
  const [user, setUser] = useState<UserOut | null>(null)
  const [loading, setLoading] = useState(true)
  const [tokenVersion, setTokenVersion] = useState(0)
  const [tokenExpiresAt, setTokenExpiresAt] = useState<number | null>(null)

  useEffect(() => {
    const t = getAccessToken()
    setTokenExpiresAt(t ? getJwtExpMs(t) : null)
  }, [tokenVersion])

  const refresh = useCallback(async () => {
    const t = localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY)
    if (!t) {
      setUser(null)
      setLoading(false)
      return
    }
    try {
      const u = await getAuthMe()
      setUser(u)
    } catch {
      setUser(null)
      setAccessToken(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void refresh()
  }, [refresh])

  useEffect(() => {
    function onCustom() {
      setTokenVersion((v) => v + 1)
      void refresh()
    }
    function onStorage(e: StorageEvent) {
      if (e.key !== ACCESS_TOKEN_STORAGE_KEY) return
      setTokenVersion((v) => v + 1)
      void refresh()
    }
    window.addEventListener('ramanujan-auth', onCustom)
    window.addEventListener('storage', onStorage)
    return () => {
      window.removeEventListener('ramanujan-auth', onCustom)
      window.removeEventListener('storage', onStorage)
    }
  }, [refresh])

  const login = useCallback(async (email: string, password: string) => {
    const { access_token } = await postAuthLogin(email, password)
    setAccessToken(access_token)
    setTokenVersion((v) => v + 1)
    await refresh()
  }, [refresh])

  const register = useCallback(async (email: string, password: string) => {
    const { access_token } = await postAuthRegister(email, password)
    setAccessToken(access_token)
    setTokenVersion((v) => v + 1)
    await refresh()
  }, [refresh])

  const logout = useCallback(() => {
    setAccessToken(null)
    setUser(null)
    setTokenVersion((v) => v + 1)
  }, [])

  return { user, loading, login, register, logout, refresh, tokenExpiresAt }
}
