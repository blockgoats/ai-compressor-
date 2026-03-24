/** Read JWT `exp` (seconds since epoch) without verifying signature — UI only. */
export function getJwtExpMs(token: string): number | null {
  const parts = token.split('.')
  if (parts.length < 2) return null
  try {
    const payload = JSON.parse(
      atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')),
    ) as { exp?: number }
    if (typeof payload.exp === 'number') return payload.exp * 1000
  } catch {
    return null
  }
  return null
}
