import { Outlet } from 'react-router-dom'

import { AmbientBackground } from '@/components/visual/ambient-background'
import { Sidebar } from '@/components/layout/sidebar'
import { Topbar } from '@/components/layout/topbar'
import type { ThemeApi } from '@/hooks/use-theme'

type AppShellProps = {
  theme: ThemeApi
}

export function AppShell({ theme }: AppShellProps) {
  return (
    <div className="relative min-h-dvh bg-background text-foreground">
      <AmbientBackground />
      <div className="relative z-10">
        <Sidebar theme={theme} />
        <div className="pl-[240px] max-md:pl-16">
          <Topbar />
          <main className="mx-auto max-w-[1280px] px-6 py-8">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  )
}
