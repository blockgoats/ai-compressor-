import { useCallback, useMemo, useState, type ReactNode } from 'react'

import { DemoModeContext } from '@/context/demo-mode-context'

export function DemoModeProvider({ children }: { children: ReactNode }) {
  const [demoMode, setDemoMode] = useState(false)

  const toggleDemoMode = useCallback(() => {
    setDemoMode((d) => !d)
  }, [])

  const value = useMemo(
    () => ({ demoMode, setDemoMode, toggleDemoMode }),
    [demoMode, toggleDemoMode],
  )

  return (
    <DemoModeContext.Provider value={value}>
      {children}
    </DemoModeContext.Provider>
  )
}
