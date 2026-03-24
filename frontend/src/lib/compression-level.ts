export type CompressionLevel = 'low' | 'medium' | 'aggressive'

/** Map UI slider 0–100 to backend `compression_level`. */
export function sliderToCompressionLevel(level: number): CompressionLevel {
  if (level <= 33) return 'low'
  if (level <= 66) return 'medium'
  return 'aggressive'
}
