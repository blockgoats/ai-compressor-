import { useCallback, useState } from 'react'

const STORAGE_KEY = 'ramanujan-theme'

export type ThemeApi = {
  isLight: boolean
  toggle: () => void
}

function readInitialLight(): boolean {
  if (typeof localStorage === 'undefined') return false
  const stored = localStorage.getItem(STORAGE_KEY)
  const light = stored === 'light'
  document.documentElement.classList.toggle('light', light)
  return light
}

export function useTheme(): ThemeApi {
  const [isLight, setIsLight] = useState(readInitialLight)

  const toggle = useCallback(() => {
    setIsLight((prev) => {
      const next = !prev
      document.documentElement.classList.toggle('light', next)
      localStorage.setItem(STORAGE_KEY, next ? 'light' : 'dark')
      return next
    })
  }, [])

  return { isLight, toggle }
}
