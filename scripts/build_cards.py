"""Gera os cartões dos projetos (assets/projeto-*.svg) e assets/skills.svg.

O GitHub põe bordas nas tabelas e não aceita CSS, por isso estas secções
são imagens.  Correr:  python scripts/build_cards.py
"""
import pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
SANS = '-apple-system,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif'
MONO = 'ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace'

PROJECTS = [
    ("projeto-soletracao", ["Jogo de soletração gestual"],
     ["Jogo baseado no popular “Termo”,", "adaptado para a Língua Gestual."],
     ["JavaScript", "React"], "▶ jogar demo ↗"),
    ("projeto-objetos", ["WebApp de identificação", "de objetos"],
     ["Reconhecimento e identificação", "visual de objetos na web."],
     ["JavaScript", "HTML/CSS"], "▶ ver demo ↗"),
    ("projeto-facial", ["Reconhecimento facial"],
     ["Autenticação biométrica com", "modelos de reconhecimento facial."],
     ["JavaScript", "HTML"], "ver código ↗"),
]

W, H = 270, 180
STYLE = f"""<style>
.t{{font:600 15px {SANS};fill:#e6edf3}}
.d{{font:12.5px {SANS};fill:#8b949e}}
.b{{font:11px {MONO};fill:#8b949e}}
.l{{font:12px {MONO};fill:#58a6ff}}
.h{{font:600 20px {SANS};fill:#e6edf3}}
.n{{font:14px {MONO};fill:#6e7681}}
.i{{font:15px {SANS};fill:#c9d1d9}}
.k{{font:14px {MONO};fill:#7ee787}}
.p{{font:12px {MONO};fill:#8b949e}}
</style>"""


def project_card(title, desc, tags, link):
    out = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="8" fill="#0d1117" stroke="#30363d"/>']
    y = 30
    for line in title:
        out.append(f'<text x="16" y="{y}" class="t">{escape(line)}</text>')
        y += 20
    y += 4
    for line in desc:
        out.append(f'<text x="16" y="{y}" class="d">{escape(line)}</text>')
        y += 18
    x, ty = 16, H - 56
    for tag in tags:
        w = len(tag) * 6.7 + 14
        out.append(f'<rect x="{x}" y="{ty}" width="{w:.0f}" height="20" rx="5" fill="#21262d"/>'
                   f'<text x="{x + 7}" y="{ty + 14}" class="b">{escape(tag)}</text>')
        x += w + 6
    out.append(f'<text x="16" y="{H - 18}" class="l">{escape(link)}</text>')
    return "\n".join(out)


def heading(x, num, text):
    return (f'<text x="{x}" y="26" class="n">{num} ·</text>'
            f'<text x="{x + 48}" y="26" class="h">{escape(text)}</text>'
            f'<line x1="{x}" y1="40" x2="{x + 395}" y2="40" stroke="#21262d"/>')


def skills_svg():
    soft = ["curiosidade", "comunicação", "vontade de aprender",
            "resolução de problemas", "organização"]
    langs = [("português", "nativo"), ("inglês", "B2"), ("francês", "A2")]
    out = [heading(0, "05", "soft skills"), heading(430, "06", "idiomas")]
    for i, s in enumerate(soft):
        y = 70 + i * 26
        out.append(f'<text x="0" y="{y}" class="k">✓</text><text x="22" y="{y}" class="i">{escape(s)}</text>')
    for i, (lang, lvl) in enumerate(langs):
        y = 70 + i * 26
        out.append(f'<text x="430" y="{y}" class="i">{escape(lang)}</text>'
                   f'<rect x="530" y="{y - 14}" width="{len(lvl) * 7.3 + 14:.0f}" height="20" rx="5" fill="#21262d"/>'
                   f'<text x="537" y="{y}" class="p">{escape(lvl)}</text>')
    return "\n".join(out)


def write(name, w, h, label, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'role="img" aria-label="{escape(label)}">\n{STYLE}\n{body}\n</svg>\n')
    (ROOT / "assets" / f"{name}.svg").write_text(svg, encoding="utf-8")
    print(f"assets/{name}.svg")


def main():
    for name, title, desc, tags, link in PROJECTS:
        write(name, W, H, " ".join(title), project_card(title, desc, tags, link))
    write("skills", 830, 200, "Soft skills e idiomas", skills_svg())


if __name__ == "__main__":
    main()
