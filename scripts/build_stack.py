"""Gera assets/stack.svg: blocos com logos e auras animadas.

Os logos ficam embutidos (data URI) porque o GitHub não deixa um SVG
carregar imagens externas.  Correr:  python scripts/build_stack.py
Com --aura, cada bloco ganha uma aura animada (o GitHub não suporta hover).
"""
import base64
import sys
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEV = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/{0}/{0}-original.svg"
LOBE = "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/{}.svg"

# grupo -> linhas -> (nome, url, aura, inverter cor do logo)
# aura: uma cor, "python" (azul/amarelo na diagonal) ou "gemini" (multicolor)
GROUPS = [
    ("linguagens", [[
        ("Java", DEV.format("java"), "#e3262b", False),
        ("C++", DEV.format("cplusplus"), "#3f8fd2", False),
        ("JavaScript", DEV.format("javascript"), "#f7df1e", False),
        ("Python", DEV.format("python"), "python", False),
        ("C#", DEV.format("csharp"), "#a179dc", False),
        ("PostgreSQL", DEV.format("postgresql"), "#4f8fc0", False),
    ]]),
    ("frameworks", [[
        ("React", DEV.format("react"), "#61dafb", False),
        ("Node.js", DEV.format("nodejs"), "#5fa04e", False),
        (".NET", DEV.format("dotnetcore"), "#7c5cff", False),
    ]]),
    ("ferramentas", [[
        ("VS Code", DEV.format("vscode"), "#23a9f2", False),
        ("Visual Studio", DEV.format("visualstudio"), "#9b6fd4", False),
        ("GitHub", DEV.format("github"), "#e6edf3", True),
        ("Figma", DEV.format("figma"), "#f24e1e", False),
        ("Notion", "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/notion.svg", "#e6edf3", True),
    ], [
        ("Claude", LOBE.format("claude-color"), "#d97757", False),
        ("ChatGPT", LOBE.format("openai"), "#74aa9c", True),
        ("Gemini", LOBE.format("gemini-color"), "gemini", False),
    ]]),
]

TILE, GAP, ICON = 56, 18, 32
PAD_X, LABEL_H, ROW_GAP, LINE_GAP = 24, 26, 22, 16
GEMINI = [("#4285f4", -1, -1), ("#9b72cb", 1, -1), ("#ea4335", 1, 1),
          ("#fbbc04", -1, 1), ("#34a853", 0, 1)]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def aura(kind, x, y, delay):
    cx, cy = x + TILE / 2, y + TILE / 2
    style = f'style="animation-delay:{delay:.2f}s"'
    if kind == "python":
        return (f'<g class="aura" {style} filter="url(#blur)">'
                f'<rect x="{x - 5}" y="{y - 5}" width="{TILE * .7}" height="{TILE * .7}" rx="14" fill="#3f86c6"/>'
                f'<rect x="{x + TILE * .3 + 5}" y="{y + TILE * .3 + 5}" width="{TILE * .7}" height="{TILE * .7}" rx="14" fill="#ffd43b"/></g>')
    if kind == "gemini":
        blobs = "".join(
            f'<circle cx="{cx + dx * 18}" cy="{cy + dy * 18}" r="20" fill="{c}"/>'
            for c, dx, dy in GEMINI)
        return f'<g class="aura" {style} filter="url(#blur)">{blobs}</g>'
    return (f'<rect class="aura" {style} filter="url(#blur)" x="{x - 2}" y="{y - 2}" '
            f'width="{TILE + 4}" height="{TILE + 4}" rx="14" fill="{kind}"/>')


def main():
    per_row = max(len(row) for _, rows in GROUPS for row in rows)
    width = PAD_X * 2 + per_row * TILE + (per_row - 1) * GAP
    parts, y, i = [], 16, 0
    for label, rows in GROUPS:
        parts.append(f'<text x="{PAD_X}" y="{y + 14}" class="lb">{label}</text>')
        y += LABEL_H
        for r, row in enumerate(rows):
            if r:
                y += TILE + LINE_GAP
            for col, (name, url, kind, invert) in enumerate(row):
                x = PAD_X + col * (TILE + GAP)
                data = base64.b64encode(fetch(url)).decode()
                inv = ' filter="url(#invert)"' if invert else ""
                if "--aura" in sys.argv:
                    parts.append(aura(kind, x, y, i * 0.35))
                parts.append(
                    f'<g><title>{name}</title>'
                    f'<rect x="{x}" y="{y}" width="{TILE}" height="{TILE}" rx="12" fill="#242938"/>'
                    f'<image x="{x + (TILE - ICON) / 2}" y="{y + (TILE - ICON) / 2}" width="{ICON}" height="{ICON}"{inv} '
                    f'href="data:image/svg+xml;base64,{data}"/></g>')
                i += 1
        y += TILE + ROW_GAP
    height = y - ROW_GAP + 16

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Stack do André: linguagens, frameworks, ferramentas e IA">
<style>
.lb{{font:12px ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace;fill:#6e7681}}
.aura{{opacity:0;animation:pulse 4.2s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:0}}50%{{opacity:.85}}}}
@media (prefers-reduced-motion:reduce){{.aura{{animation:none;opacity:.35}}}}
</style>
<defs>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>
<filter id="invert"><feColorMatrix type="matrix" values="-1 0 0 0 1  0 -1 0 0 1  0 0 -1 0 1  0 0 0 1 0"/></filter>
</defs>
{chr(10).join(parts)}
</svg>
'''
    out = ROOT / "assets" / "stack.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"{out}  {width}x{height}  {len(svg) // 1024} KB")


if __name__ == "__main__":
    main()
