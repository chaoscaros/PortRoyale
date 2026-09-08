import type { CSSProperties } from "react";
export type IconName =
  | "compass"
  | "ship"
  | "port"
  | "pause"
  | "play"
  | "close"
  | "focus"
  | "map"
  | "settings"
  | "coins"
  | "arrow";
const paths: Record<IconName, string> = {
  compass:
    "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20ZM16 8l-2.5 5.5L8 16l2.5-5.5L16 8Z",
  ship: "M3 16h18l-3 5H6l-3-5ZM12 3v13M10 4v9H4L10 4ZM14 7v6h5l-5-6Z",
  port: "M5 21h14M8 21l2-12h4l2 12M9 9V5h6v4H9ZM12 2v3M6 12l-3 2m15-2 3 2",
  pause: "M8 5v14M16 5v14",
  play: "M8 4l12 8-12 8V4Z",
  close: "M6 6l12 12M6 18L18 6",
  focus:
    "M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10Z",
  map: "M3 5l6-2 6 2 6-2v16l-6 2-6-2-6 2V5ZM9 3v16m6-14v16",
  settings: "M4 6h16M4 12h16M4 18h16M8 3v6m8 0v6m-6 0v6",
  coins:
    "M12 3c5 0 8 2 8 4s-3 4-8 4-8-2-8-4 3-4 8-4ZM4 7v10c0 2 3 4 8 4s8-2 8-4V7M4 12c0 2 3 4 8 4s8-2 8-4",
  arrow: "M4 12h16m-6-6 6 6-6 6",
};
export function Icon({
  name,
  size = 20,
  style,
}: {
  name: IconName;
  size?: number;
  style?: CSSProperties;
}) {
  return (
    <svg
      style={style}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d={paths[name]} />
    </svg>
  );
}
