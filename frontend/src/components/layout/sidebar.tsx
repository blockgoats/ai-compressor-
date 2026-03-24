import {
  BarChart3,
  Cpu,
  KeyRound,
  LayoutDashboard,
  Moon,
  Settings,
  Sparkles,
  Sun,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'

import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip'
import { cn } from '@/lib/utils'
import type { ThemeApi } from '@/hooks/use-theme'

const nav = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/playground', label: 'Playground', icon: Sparkles },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/api', label: 'API', icon: KeyRound },
  { to: '/models', label: 'Models', icon: Cpu },
  { to: '/settings', label: 'Settings', icon: Settings },
] as const

type SidebarProps = {
  theme: ThemeApi
}

export function Sidebar({ theme }: SidebarProps) {
  return (
    <aside
      className={cn(
        'fixed left-0 top-0 z-40 flex h-dvh w-[240px] flex-col border-r border-border bg-surface-secondary/80 backdrop-blur-md',
        'max-md:w-16 max-md:items-center',
      )}
    >
      <div className="flex h-14 items-center gap-2 border-b border-border px-4 max-md:justify-center max-md:px-2">
        <div className="h-8 w-8 rounded-lg bg-gradient-primary opacity-90" />
        <span className="text-lg font-semibold text-gradient max-md:hidden">
          Ramanujan
        </span>
      </div>

      <nav className="flex flex-1 flex-col gap-1 p-3">
        {nav.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              cn(
                'group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-muted-foreground transition-colors',
                'max-md:justify-center max-md:px-0',
                isActive &&
                  'bg-gradient-primary text-white shadow-sm text-white [&_svg]:text-white',
                !isActive && 'hover:bg-surface hover:text-foreground',
              )
            }
          >
            <Icon className="h-4 w-4 shrink-0" aria-hidden />
            <span className="max-md:sr-only">{label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="flex flex-col gap-2 border-t border-border p-3">
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant="ghost"
              className="w-full justify-start gap-3 max-md:justify-center max-md:px-0"
              onClick={theme.toggle}
              type="button"
            >
              {theme.isLight ? (
                <Moon className="h-4 w-4" />
              ) : (
                <Sun className="h-4 w-4" />
              )}
              <span className="max-md:sr-only">
                {theme.isLight ? 'Dark mode' : 'Light mode'}
              </span>
            </Button>
          </TooltipTrigger>
          <TooltipContent side="right">
            {theme.isLight ? 'Switch to dark' : 'Switch to light'}
          </TooltipContent>
        </Tooltip>

        <div className="flex items-center gap-3 rounded-xl px-2 py-2 max-md:justify-center">
          <Avatar className="h-9 w-9">
            <AvatarFallback>RC</AvatarFallback>
          </Avatar>
          <div className="min-w-0 flex-1 max-md:hidden">
            <p className="truncate text-sm font-medium text-foreground">
              Dev User
            </p>
            <p className="truncate text-xs text-caption">Pro plan</p>
          </div>
        </div>
      </div>
    </aside>
  )
}
