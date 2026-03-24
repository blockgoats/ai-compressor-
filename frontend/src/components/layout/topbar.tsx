import {
  Bell,
  Building2,
  ChevronDown,
  FlaskConical,
  Search,
  Shield,
} from 'lucide-react'
import { useState } from 'react'

import { useDemoMode } from '@/hooks/use-demo-mode'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip'
const API_PREVIEW = 'sk_live_••••8f3a'
const WORKSPACES = ['Production', 'Staging', 'Personal'] as const

export function Topbar() {
  const { demoMode, setDemoMode } = useDemoMode()
  const [workspace, setWorkspace] = useState<(typeof WORKSPACES)[number]>(
    'Production',
  )

  return (
    <header className="sticky top-0 z-30 flex h-14 flex-wrap items-center gap-3 border-b border-border bg-background/80 px-4 py-2 backdrop-blur-md md:flex-nowrap md:gap-4 md:px-6">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="secondary"
            size="sm"
            className="hidden gap-2 font-sans md:inline-flex"
            type="button"
          >
            <Building2 className="h-3.5 w-3.5 text-caption" />
            <span className="max-w-[120px] truncate">{workspace}</span>
            <ChevronDown className="h-3.5 w-3.5 text-caption" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start" className="w-48">
          <DropdownMenuLabel>Workspace</DropdownMenuLabel>
          <DropdownMenuSeparator />
          {WORKSPACES.map((w) => (
            <DropdownMenuItem key={w} onClick={() => setWorkspace(w)}>
              {w}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      <div className="relative min-w-0 flex-1 max-w-md">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-caption" />
        <Input
          placeholder="Search prompts, projects…"
          className="h-9 rounded-full border-border bg-surface-secondary pl-9 font-sans placeholder:text-caption"
        />
      </div>

      <div className="hidden min-w-[140px] flex-1 max-w-[200px] lg:block">
        <div className="mb-1 flex justify-between text-[10px] text-caption">
          <span>Usage</span>
          <span className="font-mono tabular-nums text-foreground">1.2M / 2M</span>
        </div>
        <div className="h-1.5 overflow-hidden rounded-full bg-surface-secondary">
          <div
            className="h-full w-[60%] rounded-full bg-gradient-to-r from-indigo via-violet to-cyan"
            title="60% of monthly token quota"
          />
        </div>
      </div>

      <div className="flex items-center gap-2 rounded-full border border-border bg-surface-secondary/80 px-2 py-1">
        <FlaskConical className="h-3.5 w-3.5 text-caption" aria-hidden />
        <span className="hidden text-xs text-muted-foreground sm:inline">
          Demo
        </span>
        <Switch
          checked={demoMode}
          onCheckedChange={setDemoMode}
          aria-label="Toggle demo mode"
        />
      </div>

      <Tooltip>
        <TooltipTrigger asChild>
          <Button
            variant="secondary"
            size="sm"
            className="hidden font-mono text-xs sm:inline-flex"
            type="button"
          >
            {API_PREVIEW}
          </Button>
        </TooltipTrigger>
        <TooltipContent>API key preview — manage in Settings</TooltipContent>
      </Tooltip>

      <Badge variant="default" className="hidden font-mono text-[10px] lg:inline-flex">
        <Shield className="mr-1 h-3 w-3" aria-hidden />
        Admin
      </Badge>

      <Button variant="ghost" size="icon" className="relative shrink-0" type="button">
        <Bell className="h-4 w-4" />
        <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-gradient-to-r from-indigo to-cyan" />
      </Button>

      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" className="shrink-0 gap-2 px-1" type="button">
            <Avatar className="h-8 w-8">
              <AvatarFallback className="text-xs">RC</AvatarFallback>
            </Avatar>
            <div className="hidden text-left sm:block">
              <p className="text-xs font-medium leading-tight">Dev User</p>
              <p className="text-[10px] text-caption">Pro · {workspace}</p>
            </div>
            <ChevronDown className="h-4 w-4 text-caption hidden sm:block" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-52">
          <DropdownMenuItem>Profile</DropdownMenuItem>
          <DropdownMenuItem>Billing</DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem>Sign out</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </header>
  )
}
