import { type MouseEvent, useRef, useState, type ReactNode } from 'react'

import { Button, type ButtonProps } from '@/components/ui/button'
import { cn } from '@/lib/utils'

type Ripple = { x: number; y: number; id: number }

type RippleButtonProps = ButtonProps & {
  children: ReactNode
}

/** Primary buttons with material-style ripple (b.md micro-interaction) */
export function RippleButton({
  className,
  children,
  onClick,
  ...props
}: RippleButtonProps) {
  const ref = useRef<HTMLButtonElement>(null)
  const [ripples, setRipples] = useState<Ripple[]>([])

  function handleClick(e: MouseEvent<HTMLButtonElement>) {
    const btn = ref.current
    if (btn) {
      const r = btn.getBoundingClientRect()
      const x = e.clientX - r.left
      const y = e.clientY - r.top
      const id = Date.now()
      setRipples((prev) => [...prev, { x, y, id }])
      window.setTimeout(() => {
        setRipples((prev) => prev.filter((p) => p.id !== id))
      }, 600)
    }
    onClick?.(e)
  }

  return (
    <Button
      ref={ref}
      className={cn('relative overflow-hidden', className)}
      onClick={handleClick}
      {...props}
    >
      {ripples.map((r) => (
        <span
          key={r.id}
          className="pointer-events-none absolute animate-[ripple_0.55s_ease-out_forwards] rounded-full bg-white/25"
          style={{
            left: r.x,
            top: r.y,
            width: 8,
            height: 8,
            transform: 'translate(-50%, -50%)',
          }}
        />
      ))}
      {children}
    </Button>
  )
}
