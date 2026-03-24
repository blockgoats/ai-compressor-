import { AnimatePresence, motion } from 'framer-motion'

import { cn } from '@/lib/utils'

type SliderTokenBlocksProps = {
  words: string[]
  level: number
  className?: string
}

/** Visual token blocks that shrink / fade as compression increases */
export function SliderTokenBlocks({
  words,
  level,
  className,
}: SliderTokenBlocksProps) {
  const visible = Math.max(
    1,
    Math.ceil(words.length * (1 - (level / 100) * 0.65)),
  )
  const shown = words.slice(0, Math.min(words.length, visible))

  return (
    <div
      className={cn(
        'flex min-h-[40px] flex-wrap gap-1 rounded-lg border border-border/60 bg-background/40 p-2',
        className,
      )}
    >
      <AnimatePresence initial={false}>
        {shown.map((w, i) => (
          <motion.span
            key={`${w}-${i}`}
            layout
            initial={{ opacity: 0.4, scale: 0.85 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.6 }}
            transition={{ duration: 0.2 }}
            className="rounded-md border border-border/80 bg-surface-secondary px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground"
          >
            {w.length > 12 ? `${w.slice(0, 10)}…` : w}
          </motion.span>
        ))}
      </AnimatePresence>
    </div>
  )
}
