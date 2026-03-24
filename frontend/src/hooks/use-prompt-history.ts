import { useCallback, useState } from 'react'

const KEY = 'ramanujan-prompt-history-v1'
const MAX = 12

export type PromptVersion = {
  id: string
  text: string
  savedAt: number
}

function load(): PromptVersion[] {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw) as PromptVersion[]
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export function usePromptHistory() {
  const [versions, setVersions] = useState<PromptVersion[]>(() => load())

  const saveVersion = useCallback((text: string) => {
    const entry: PromptVersion = {
      id: `${Date.now()}`,
      text,
      savedAt: Date.now(),
    }
    setVersions((prev) => {
      const next = [entry, ...prev].slice(0, MAX)
      localStorage.setItem(KEY, JSON.stringify(next))
      return next
    })
  }, [])

  const removeVersion = useCallback((id: string) => {
    setVersions((prev) => {
      const next = prev.filter((v) => v.id !== id)
      localStorage.setItem(KEY, JSON.stringify(next))
      return next
    })
  }, [])

  return { versions, saveVersion, removeVersion }
}
