/** Format ISO timestamps from the API as short relative labels. */
export function formatRelativeShort(iso: string): string {
  const t = Date.parse(iso)
  if (Number.isNaN(t)) return iso
  const sec = Math.round((Date.now() - t) / 1000)
  if (sec < 60) return `${sec}s ago`
  const min = Math.round(sec / 60)
  if (min < 60) return `${min}m ago`
  const hr = Math.round(min / 60)
  if (hr < 48) return `${hr}h ago`
  return new Date(t).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}
