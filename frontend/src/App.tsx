import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { Toaster } from 'sonner'

import { DemoModeProvider } from '@/context/demo-mode-provider'
import { AppShell } from '@/components/layout/app-shell'
import { TooltipProvider } from '@/components/ui/tooltip'
import { useTheme } from '@/hooks/use-theme'
import { AnalyticsPage } from '@/pages/analytics'
import { ApiPage } from '@/pages/api-page'
import { DashboardPage } from '@/pages/dashboard'
import { ModelsPage } from '@/pages/models'
import { PlaygroundPage } from '@/pages/playground'
import { SettingsPage } from '@/pages/settings'

export default function App() {
  const theme = useTheme()

  return (
    <DemoModeProvider>
      <TooltipProvider delayDuration={200}>
        <BrowserRouter>
          <Routes>
            <Route element={<AppShell theme={theme} />}>
              <Route index element={<DashboardPage />} />
              <Route path="playground" element={<PlaygroundPage />} />
              <Route path="analytics" element={<AnalyticsPage />} />
              <Route path="api" element={<ApiPage />} />
              <Route path="models" element={<ModelsPage />} />
              <Route path="settings" element={<SettingsPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
        <Toaster
          theme={theme.isLight ? 'light' : 'dark'}
          toastOptions={{
            classNames: {
              toast:
                'border border-border bg-surface text-foreground font-sans',
            },
          }}
        />
      </TooltipProvider>
    </DemoModeProvider>
  )
}
