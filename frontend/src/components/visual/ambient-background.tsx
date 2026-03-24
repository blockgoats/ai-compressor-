/**
 * Subtle math-inspired overlays — low contrast to stay within a.md (no neon overload).
 */
export function AmbientBackground() {
  return (
    <div
      className="pointer-events-none fixed inset-0 z-0 overflow-hidden"
      aria-hidden
    >
      <div
        className="absolute inset-0 opacity-[0.07]"
        style={{
          backgroundImage: `
            linear-gradient(var(--color-border) 1px, transparent 1px),
            linear-gradient(90deg, var(--color-border) 1px, transparent 1px)
          `,
          backgroundSize: '32px 32px',
        }}
      />
      <svg
        className="absolute -right-[10%] top-[15%] h-[45vh] w-[80vw] opacity-[0.11] text-indigo"
        viewBox="0 0 800 200"
        preserveAspectRatio="none"
      >
        <title>Fourier-style curve</title>
        <path
          fill="none"
          stroke="currentColor"
          strokeWidth="1.2"
          d="M0,100 Q100,20 200,100 T400,100 T600,100 T800,100"
          className="animate-[wave-drift_28s_ease-in-out_infinite]"
        />
        <path
          fill="none"
          stroke="url(#waveGrad)"
          strokeWidth="1"
          d="M0,120 C150,180 250,40 400,120 S650,60 800,110"
          className="animate-[wave-drift_22s_ease-in-out_infinite_reverse]"
        />
        <defs>
          <linearGradient id="waveGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#6366f1" stopOpacity="0.5" />
            <stop offset="50%" stopColor="#8b5cf6" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#22d3ee" stopOpacity="0.35" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-x-0 bottom-0 h-px bg-gradient-to-r from-transparent via-border to-transparent opacity-40" />
    </div>
  )
}
