/** Animated subtle grid for Ramanujan mode — contained, not full-neon */
export function RamanujanMathBg() {
  return (
    <div
      className="pointer-events-none absolute inset-0 overflow-hidden rounded-2xl opacity-40"
      aria-hidden
    >
      <div
        className="absolute inset-0 animate-[math-pan_24s_linear_infinite]"
        style={{
          backgroundImage: `radial-gradient(circle at 20% 30%, rgba(99,102,241,0.12) 0%, transparent 45%),
            radial-gradient(circle at 80% 70%, rgba(34,211,238,0.1) 0%, transparent 40%)`,
        }}
      />
      <svg className="absolute inset-0 h-full w-full" viewBox="0 0 200 200">
        <defs>
          <pattern
            id="smallGrid"
            width="16"
            height="16"
            patternUnits="userSpaceOnUse"
          >
            <path
              d="M 16 0 L 0 0 0 16"
              fill="none"
              stroke="currentColor"
              strokeWidth="0.3"
              className="text-border"
            />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#smallGrid)" />
      </svg>
    </div>
  )
}
