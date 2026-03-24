import type { ReactNode } from 'react'

import { cn } from '@/lib/utils'

/**
 * Fixed-size wrapper so Recharts `ResponsiveContainer` always gets non-zero
 * dimensions (avoids width/height -1 warnings in flex/grid layouts).
 */
export function ChartPanel({
  children,
  className,
  heightClass = 'h-64',
}: {
  children: ReactNode
  className?: string
  heightClass?: string
}) {
  return (
    <div className={cn('w-full min-w-0 pl-0', heightClass, className)}>
      <div className="h-full w-full min-h-0 min-w-0">{children}</div>
    </div>
  )
}
