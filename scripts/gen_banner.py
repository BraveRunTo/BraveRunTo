import html
from pathlib import Path

LINES = [
    " /$$$$$$$                                         /$$$$$$$                   /$$$$$$$$",
    "| $$__  $$                                       | $$__  $$                 |__  $$__/",
    r"| $$  \ $$  /$$$$$$  /$$$$$$  /$$    /$$ /$$$$$$ | $$  \ $$ /$$   /$$ /$$$$$$$ | $$  /$$$$$$",
    r"| $$$$$$$  /$$__  $$|____  $$|  $$  /$$//$$__  $$| $$$$$$$/| $$  | $$| $$__  $$| $$ /$$__  $$",
    r"| $$__  $$| $$  \__/ /$$$$$$$ \  $$/$$/| $$$$$$$$| $$__  $$| $$  | $$| $$  \ $$| $$| $$  \ $$",
    r"| $$  \ $$| $$      /$$__  $$  \  $$$/ | $$_____/| $$  \ $$| $$  | $$| $$  | $$| $$| $$  | $$",
    r"| $$$$$$$/| $$     |  $$$$$$$   \  $/  |  $$$$$$$| $$  | $$|  $$$$$$/| $$  | $$| $$|  $$$$$$/",
    r"|_______/ |__/      \_______/    \_/    \_______/|__/  |__/ \______/ |__/  |__/|__/ \______/",
]

FONT_SIZE = 10
CHAR_W = 6.0
LINE_H = 12
START_X = 14
START_Y = 44
PAD_X = 14
PAD_BOTTOM = 16


def char_color(row: int, col: int, ch: str) -> str:
    """为每个字符生成独立色相（可按需调整算法）。"""
    hue = (row * 47 + col * 19 + ord(ch) * 23) % 360
    saturation = 72 + (ord(ch) + col) % 23
    lightness = 54 + (row + ord(ch)) % 16
    return f"hsl({hue}, {saturation}%, {lightness}%)"


def main() -> None:
    max_len = max(len(line) for line in LINES)
    lines = [line.ljust(max_len) for line in LINES]

    width = int(START_X + max_len * CHAR_W + PAD_X)
    height = int(START_Y + (len(lines) - 1) * LINE_H + PAD_BOTTOM)

    chars: list[str] = []
    for row, line in enumerate(lines):
        y = START_Y + row * LINE_H
        for col, ch in enumerate(line):
            if ch == " ":
                continue
            x = START_X + col * CHAR_W
            esc = html.escape(ch)
            color = char_color(row, col, ch)
            chars.append(
                f'  <text x="{x:.1f}" y="{y}" font-size="{FONT_SIZE}" '
                f'font-family="Courier New, Courier, monospace" fill="{color}" '
                f'text-anchor="start">{esc}</text>'
            )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="Welcome banner">
  <rect width="{width}" height="{height}" rx="10" fill="#0d1117"/>
  <rect width="{width}" height="26" rx="10" fill="#161b22"/>
  <rect y="16" width="{width}" height="10" fill="#161b22"/>
  <circle cx="18" cy="13" r="5.5" fill="#ff5f57"/>
  <circle cx="36" cy="13" r="5.5" fill="#febc2e"/>
  <circle cx="54" cy="13" r="5.5" fill="#28c840"/>
  <g>
{chr(10).join(chars)}
  </g>
</svg>
"""

    out = Path(__file__).resolve().parents[1] / "assets" / "banner.svg"
    out.write_text(svg, encoding="utf-8", newline="\n")
    print(f"Wrote {out} ({width}x{height}, {len(chars)} glyphs)")


if __name__ == "__main__":
    main()
