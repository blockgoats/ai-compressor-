import { AnimatePresence, motion } from 'framer-motion'
import { Check, Copy } from 'lucide-react'
import { useState } from 'react'

import { Button } from '@/components/ui/button'
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip'
import { cn } from '@/lib/utils'

type CopyButtonProps = {
  text: string
  className?: string
  size?: 'default' | 'sm' | 'icon'
  label?: string
}

export function CopyButton({
  text,
  className,
  size = 'icon',
  label,
}: CopyButtonProps) {
  const [done, setDone] = useState(false)

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(text)
      setDone(true)
      setTimeout(() => setDone(false), 2000)
    } catch {
      // clipboard denied
    }
  }

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button
          type="button"
          variant="ghost"
          size={size}
          className={cn('shrink-0', className)}
          onClick={handleCopy}
          aria-label="Copy"
        >
          <AnimatePresence mode="wait" initial={false}>
            {done ? (
              <motion.span
                key="ok"
                initial={{ opacity: 0, y: 2 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -2 }}
                className="flex items-center gap-1 text-success"
              >
                <Check className="h-4 w-4" />
                {size !== 'icon' ? (
                  <span className="text-xs font-medium">Copied ✓</span>
                ) : null}
              </motion.span>
            ) : (
              <motion.span
                key="copy"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex items-center gap-1"
              >
                <Copy className="h-4 w-4" />
              </motion.span>
            )}
          </AnimatePresence>
          {label ? <span className="ml-1 font-mono text-xs">{label}</span> : null}
        </Button>
      </TooltipTrigger>
      <TooltipContent>Copy</TooltipContent>
    </Tooltip>
  )
}
