import { createContext } from 'react'

export type DemoModeContextValue = {
  demoMode: boolean
  setDemoMode: (v: boolean) => void
  toggleDemoMode: () => void
}

export const DemoModeContext = createContext<DemoModeContextValue | null>(null)
