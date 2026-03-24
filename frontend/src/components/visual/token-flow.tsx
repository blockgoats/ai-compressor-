import { motion } from 'framer-motion'
import { ArrowRight, Cpu, Sparkles } from 'lucide-react'

import { cn } from '@/lib/utils'

type TokenFlowProps = {
  before: number
  after: number
  className?: string
}

export function TokenFlow({ before, after, className }: TokenFlowProps) {
  const ratio = before > 0 ? Math.min(1, after / before) : 0
  return (
    <div
      className={cn(
        'flex flex-wrap items-center gap-3 rounded-xl border border-border bg-surface-secondary/60 px-4 py-3',
        className,
      )}
    >
      <div className="flex items-center gap-2 text-xs text-caption">
        <span className="rounded-md bg-surface px-2 py-1 font-mono tabular-nums text-foreground">
          {before}
        </span>
        <span>in</span>
      </div>
      <ArrowRight className="h-4 w-4 shrink-0 text-muted-foreground" />
      <div className="flex items-center gap-1.5">
        <Cpu className="h-4 w-4 text-indigo" aria-hidden />
        <span className="text-xs text-caption">transform</span>
      </div>
      <ArrowRight className="h-4 w-4 shrink-0 text-muted-foreground" />
      <div className="flex items-center gap-2">
        <motion.span
          className="rounded-md border border-border-glow/40 bg-surface px-2 py-1 font-mono text-xs tabular-nums text-foreground"
          key={after}
          initial={{ scale: 0.92, opacity: 0.7 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: 'spring', stiffness: 420, damping: 28 }}
        >
          {after}
        </motion.span>
        <Sparkles className="h-3.5 w-3.5 text-cyan/80" aria-hidden />
      </div>
      <div className="ml-auto hidden font-mono text-[10px] text-caption sm:block">
        ratio{' '}
        <span className="text-foreground tabular-nums">
          {(ratio * 100).toFixed(0)}%
        </span>
      </div>
    </div>
  )
}
