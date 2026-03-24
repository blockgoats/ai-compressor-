import { useContext } from 'react'

import { DemoModeContext } from '@/context/demo-mode-context'

export function useDemoMode() {
  const ctx = useContext(DemoModeContext)
  if (!ctx) {
    throw new Error('useDemoMode must be used within DemoModeProvider')
  }
  return ctx
}
