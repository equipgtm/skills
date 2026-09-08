#!/usr/bin/env python3
"""EquipGTM workshop builder.

Turn a folder of module markdown files into a Workshop Studio-style static site —
persistent left sidebar, collapsible module groups, focus mode, copy buttons on every
code block, example-output terminals, and prev/next paging. The whole thing is branded
from a small brand.json, so the same engine emits an on-brand site for any company.

    python3 build_workshop.py CONTENT_DIR --brand brand.json --out site/

CONTENT_DIR holds `NN-slug.md` module files (with `title:`, `weight:`, `duration:`,
`summary:`, `group:` frontmatter) and an optional `_overview.md` for the landing page
(use the `{{MODULE_GRID}}` token where the module cards should go).
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path

import markdown

MD_EXT = ["meta", "fenced_code", "codehilite", "tables", "admonition", "attr_list", "toc"]
HERE = Path(__file__).resolve().parent
SHELL = HERE.parent / "assets" / "workshop-shell"

DEFAULT_BRAND = {
    "company": "Your Company",
    "product": "Hands-On Workshop",
    "tagline": "Learn by building on a real codebase.",
    "spark": "✳",
    "colors": {"ink": "#141413", "bg": "#faf9f5", "accent": "#d97757",
               "accent2": "#6a9bcc", "accent3": "#788c5d"},
    "fonts": {"head": "Poppins", "body": "Lora"},
    "links": [],
}


def m1(meta: dict, key: str, default: str = "") -> str:
    v = meta.get(key)
    return v[0] if v else default


def render_md(path: Path) -> dict:
    md = markdown.Markdown(extensions=MD_EXT, extension_configs={"codehilite": {"guess_lang": False}})
    body = md.convert(path.read_text(encoding="utf-8"))
    meta = md.Meta  # type: ignore[attr-defined]
    return {
        "slug": path.stem, "title": m1(meta, "title", path.stem),
        "weight": int(m1(meta, "weight", "999")), "duration": m1(meta, "duration", ""),
        "summary": m1(meta, "summary", ""), "group": m1(meta, "group", "Modules"),
        "body": body,
    }


def brand_css(brand: dict) -> str:
    c = brand["colors"]
    f = brand.get("fonts", {})
    return (
        ":root{"
        f'--ink:{c.get("ink","#141413")};--bg:{c.get("bg","#faf9f5")};'
        f'--accent:{c.get("accent","#d97757")};--accent2:{c.get("accent2","#6a9bcc")};'
        f'--accent3:{c.get("accent3","#788c5d")};'
        f'--head:"{f.get("head","Poppins")}",Arial,sans-serif;'
        f'--body-font:"{f.get("body","Lora")}",Georgia,serif;'
        "}"
    )


def fonts_link(brand: dict) -> str:
    f = brand.get("fonts", {})
    fams = []
    if f.get("head"):
        fams.append(f"{f['head'].replace(' ', '+')}:wght@400;500;600;700")
    if f.get("body") and f.get("body") != f.get("head"):
        fams.append(f"{f['body'].replace(' ', '+')}:ital,wght@0,400;0,500;0,600;1,400")
    if not fams:
        return ""
    q = "&".join(f"family={x}" for x in fams)
    return ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link href="https://fonts.googleapis.com/css2?{q}&display=swap" rel="stylesheet">')


def module_grid(mods: list[dict]) -> str:
    cards = []
    for m in mods:
        dur = f'<span>⏱ {html.escape(m["duration"])}</span>' if m["duration"] else ""
        cards.append(
            f'<a class="mod-card" href="{m["slug"]}.html"><span class="mc-num">{m["weight"]:02d}</span>'
            f'<h4>{html.escape(m["title"])}</h4><p>{html.escape(m["summary"])}</p>'
            f'<div class="mc-foot">{dur}</div></a>'
        )
    return f'<div class="module-grid">{"".join(cards)}</div>'


def sidebar(brand: dict, mods: list[dict], active: str | None, group_order: list[str]) -> str:
    home = "home" if active == "index" else ""
    parts = [
        '<div class="sb-top"><button class="sb-collapse" id="sbCollapse">‹ Focus mode</button></div>',
        f'<a class="sb-title {home}" href="index.html">{html.escape(brand["product"])}</a>',
    ]
    groups: dict[str, list[dict]] = {}
    for m in mods:
        groups.setdefault(m["group"], []).append(m)
    for g in group_order + [x for x in groups if x not in group_order]:
        if g not in groups:
            continue
        rows = []
        for m in sorted(groups[g], key=lambda x: x["weight"]):
            cls = "active" if m["slug"] == active else ""
            dur = f'<span class="dur">{html.escape(m["duration"])}</span>' if m["duration"] else ""
            rows.append(
                f'<li><a class="{cls}" href="{m["slug"]}.html">'
                f'<span class="num">{m["weight"]:02d}</span>'
                f'<span>{html.escape(m["title"])}{dur}</span></a></li>'
            )
        items = "".join(rows)
        parts.append(f'<details class="sb-group" open><summary>{html.escape(g)}</summary>'
                     f'<ul class="nav-list">{items}</ul></details>')
    if brand.get("links"):
        links = "".join(
            f'<a href="{html.escape(l["href"])}" target="_blank" rel="noopener">'
            f'{html.escape(l["label"])}<span class="ext">↗</span></a>' for l in brand["links"]
        )
        parts.append(f'<div class="sb-links">{links}</div>')
    return f'<aside class="sidebar">{"".join(parts)}</aside>'


PAGE = """<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {product}</title>{fonts}
<link rel="stylesheet" href="theme.css">
<script>try{{if(localStorage.getItem('navCollapsed')==='1')document.documentElement.classList.add('nav-collapsed');}}catch(e){{}}</script>
</head><body>
<header class="topbar"><button class="nav-toggle" id="navToggle" aria-label="Toggle sidebar">☰</button>
<span class="brand"><span class="spark">{spark}</span> {company}</span>
<span class="crumb">{crumb}</span><span class="spacer"></span></header>
<div class="shell">{sidebar}<main class="main"><div class="content">{header}{body}
<div class="pager">{prev}{next}</div></div></main></div>
<script src="app.js"></script></body></html>"""


def header_html(m: dict) -> str:
    chip = f'<span class="meta-chip">⏱ <b>{html.escape(m["duration"])}</b></span>' if m["duration"] else ""
    return (f'<div class="page-eyebrow"><span class="chip">Module {m["weight"]:02d}</span></div>'
            f'<h1>{html.escape(m["title"])}</h1><div class="duration-row">{chip}</div>')


def pager(m: dict | None, kind: str) -> str:
    if not m:
        return f'<a class="{kind} disabled"></a>'
    lbl = "Next" if kind == "next" else "Previous"
    return (f'<a class="{kind}" href="{m["slug"]}.html"><div class="lbl">{lbl}</div>'
            f'<div class="ttl">{html.escape(m["title"])}</div></a>')


def build(content_dir: Path, brand: dict, out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    mods = sorted((render_md(p) for p in content_dir.glob("*.md") if not p.stem.startswith("_")),
                  key=lambda x: x["weight"])
    group_order = brand.get("group_order", [])
    common = dict(product=html.escape(brand["product"]), company=html.escape(brand["company"]),
                  spark=html.escape(brand.get("spark", "✳")), fonts=fonts_link(brand))

    for i, m in enumerate(mods):
        (out / f'{m["slug"]}.html').write_text(PAGE.format(
            title=html.escape(m["title"]), crumb=f'<b>{html.escape(m["title"])}</b>',
            sidebar=sidebar(brand, mods, m["slug"], group_order), header=header_html(m), body=m["body"],
            prev=pager(mods[i - 1] if i else None, "prev"),
            next=pager(mods[i + 1] if i < len(mods) - 1 else None, "next"), **common), encoding="utf-8")

    ov = content_dir / "_overview.md"
    body = render_md(ov)["body"].replace("{{MODULE_GRID}}", module_grid(mods)) if ov.exists() else \
        f'<h1>{html.escape(brand["product"])}</h1><p>{html.escape(brand["tagline"])}</p>{module_grid(mods)}'
    (out / "index.html").write_text(PAGE.format(
        title="Overview", crumb=f'<b>{html.escape(brand["product"])}</b>',
        sidebar=sidebar(brand, mods, "index", group_order), header="", body=body,
        prev='<a class="prev disabled"></a>', next=pager(mods[0] if mods else None, "next"), **common),
        encoding="utf-8")

    # theme: brand override prepended to the shared shell css; then pygments
    css = brand_css(brand) + "\n" + (SHELL / "theme.css").read_text(encoding="utf-8")
    try:
        from pygments.formatters import HtmlFormatter
        css += "\n/* pygments */\n" + HtmlFormatter(style="monokai").get_style_defs(".codehilite")
    except ImportError:
        pass
    (out / "theme.css").write_text(css, encoding="utf-8")
    shutil.copy(SHELL / "app.js", out / "app.js")
    print(f"Built {len(mods)} modules for {brand['company']} → {out}")
    return len(mods)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a branded Workshop Studio-style site.")
    ap.add_argument("content_dir")
    ap.add_argument("--brand", help="brand.json (company, colors, fonts, links)")
    ap.add_argument("--out", default="site")
    a = ap.parse_args()
    brand = dict(DEFAULT_BRAND)
    if a.brand:
        user = json.loads(Path(a.brand).read_text(encoding="utf-8"))
        brand.update(user)
        brand["colors"] = {**DEFAULT_BRAND["colors"], **user.get("colors", {})}
        brand["fonts"] = {**DEFAULT_BRAND["fonts"], **user.get("fonts", {})}
    build(Path(a.content_dir), brand, Path(a.out))


if __name__ == "__main__":
    main()
