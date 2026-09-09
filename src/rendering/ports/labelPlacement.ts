export interface ScreenRect { left: number; top: number; right: number; bottom: number }
/** Small deterministic candidate search; never cover a protected sail or landmark. */
export function placePortLabel(
  anchor: { x: number; y: number },
  viewport: { width: number; height: number },
  obstacles: readonly ScreenRect[],
): { x: number; y: number } | null {
  const halfWidth = 58, halfHeight = 19;
  const offsets = [[0, 0], [-140, 0], [140, 0], [0, 75], [-160, 75], [160, 75], [-240, 30], [240, 30], [-340, 80], [340, 80], [0, 150], [-340, 150], [340, 150]];
  for (const [dx, dy] of offsets) {
    const x = Math.max(halfWidth + 12, Math.min(viewport.width - halfWidth - 12, anchor.x + dx));
    const y = Math.max(100, Math.min(viewport.height - 100, anchor.y + dy));
    const rect = { left: x - halfWidth, right: x + halfWidth, top: y - halfHeight, bottom: y + halfHeight };
    if (!obstacles.some(o => rect.left < o.right + 8 && rect.right > o.left - 8 && rect.top < o.bottom + 8 && rect.bottom > o.top - 8)) return { x, y };
  }
  return null;
}
