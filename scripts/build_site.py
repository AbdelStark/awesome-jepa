#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SITE = ROOT / "site"
ASSETS = SITE / "assets"
DIST = ROOT / "dist"


@dataclass
class Heading:
    level: int
    title: str
    slug: str
    resource_count: int = 0


def strip_markdown(value: str) -> str:
    value = re.sub(r"\[!\[[^\]]*\]\([^)]+\)\]\([^)]+\)", "", value)
    value = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"[*_`>#]", "", value)
    return html.unescape(value).strip()


def slugify(value: str, seen: dict[str, int] | None = None) -> str:
    slug = strip_markdown(value).lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    slug = slug or "section"
    if seen is None:
        return slug
    count = seen.get(slug, 0)
    seen[slug] = count + 1
    return slug if count == 0 else f"{slug}-{count + 1}"


def inline_markdown(value: str) -> str:
    escaped = html.escape(value, quote=False)

    def image(match: re.Match[str]) -> str:
        alt = html.escape(match.group(1), quote=True)
        src = html.escape(match.group(2), quote=True)
        return f'<img src="{src}" alt="{alt}" loading="lazy" decoding="async">'

    def link(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.escape(match.group(2), quote=True)
        attrs = ""
        if not href.startswith("#"):
            attrs = ' target="_blank" rel="noreferrer"'
        return f'<a href="{href}"{attrs}>{label}</a>'

    escaped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image, escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def extract_intro(lines: list[str]) -> tuple[str, str, list[str], str]:
    title = "Awesome JEPA"
    tagline = ""
    intro: list[str] = []

    for line in lines:
        if line.startswith("# "):
            title = strip_markdown(line[2:])
            break

    in_intro = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("> "):
            tagline = strip_markdown(stripped[2:])
            in_intro = True
            continue
        if in_intro:
            if stripped == "":
                continue
            if stripped.startswith("## "):
                break
            intro.append(stripped)

    checked = "June 2026"
    match = re.search(r"verified against primary sources in ([A-Za-z]+ \d{4})", "\n".join(lines))
    if match:
        checked = match.group(1)

    return title, tagline, intro, checked


def collect_headings(lines: list[str]) -> list[Heading]:
    headings: list[Heading] = []
    seen: dict[str, int] = {}
    current: Heading | None = None
    skip_contents = False

    for line in lines:
        heading = re.match(r"^(#{2,3})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            title = strip_markdown(heading.group(2))
            if level == 2 and title == "Contents":
                skip_contents = True
                current = None
                continue
            if level == 2 and skip_contents:
                skip_contents = False
            if skip_contents:
                continue
            current = Heading(level=level, title=title, slug=slugify(title, seen))
            headings.append(current)
            continue

        if skip_contents:
            continue
        if current and line.lstrip().startswith("- "):
            current.resource_count += 1

    return headings


def render_article(lines: list[str]) -> str:
    output: list[str] = []
    paragraph: list[str] = []
    in_list = False
    seen: dict[str, int] = {}
    skip_contents = False
    started = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f'<p>{" ".join(inline_markdown(part) for part in paragraph)}</p>')
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            output.append("</ul>")
            in_list = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            continue

        heading = re.match(r"^(#{2,3})\s+(.+?)\s*$", stripped)
        if heading:
            level = len(heading.group(1))
            title = strip_markdown(heading.group(2))
            if level == 2 and title == "Contents":
                skip_contents = True
                started = True
                continue
            if level == 2 and skip_contents:
                skip_contents = False
            if skip_contents:
                continue
            started = True
            flush_paragraph()
            close_list()
            slug = slugify(title, seen)
            output.append(
                f'<h{level} id="{slug}" data-heading-level="{level}">{inline_markdown(title)}</h{level}>'
            )
            continue

        if skip_contents or not started:
            continue

        if not stripped:
            flush_paragraph()
            close_list()
            continue

        if stripped.startswith("> "):
            flush_paragraph()
            close_list()
            output.append(f"<blockquote><p>{inline_markdown(stripped[2:])}</p></blockquote>")
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            if not in_list:
                output.append('<ul class="resource-list">')
                in_list = True
            output.append(f'<li class="resource-item">{inline_markdown(stripped[2:])}</li>')
            continue

        close_list()
        paragraph.append(stripped)

    flush_paragraph()
    close_list()
    return "\n".join(output)


def repo_links() -> tuple[str, str]:
    repository = os.environ.get("GITHUB_REPOSITORY", "AbdelStark/awesome-jepa")
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    repo_url = f"https://github.com/{repository}"
    readme_url = f"{repo_url}/blob/{branch}/README.md"
    return repo_url, readme_url


def render_page() -> str:
    lines = README.read_text(encoding="utf-8").splitlines()
    title, tagline, intro, checked = extract_intro(lines)
    headings = collect_headings(lines)
    article = render_article(lines)
    repo_url, readme_url = repo_links()

    resources = sum(heading.resource_count for heading in headings)
    domains = sum(1 for heading in headings if heading.level == 3)
    digest = hashlib.sha256(README.read_bytes()).hexdigest()[:12]
    hero_nodes = sorted(
        [heading for heading in headings if heading.resource_count > 0],
        key=lambda heading: heading.resource_count,
        reverse=True,
    )[:7]
    node_html = "\n".join(
        (
            f'<span class="latent-node latent-node-{index + 1}">'
            f"<span>{html.escape(heading.title)}</span>"
            f"<b>{heading.resource_count}</b>"
            "</span>"
        )
        for index, heading in enumerate(hero_nodes)
    )
    nav = "\n".join(
        f'<a class="toc-link toc-level-{heading.level}" href="#{heading.slug}">{html.escape(heading.title)}</a>'
        for heading in headings
    )
    intro_html = "\n".join(f"<p>{inline_markdown(item)}</p>" for item in intro[:2])
    site_data = json.dumps(
        {
            "title": title,
            "headings": [asdict(heading) for heading in headings],
            "resources": resources,
            "checked": checked,
        },
        separators=(",", ":"),
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(tagline, quote=True)}">
  <meta name="theme-color" content="#10140f">
  <title>{html.escape(title)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/styles.css?v={digest}">
</head>
<body>
  <a class="skip-link" href="#content">Skip to content</a>
  <header class="masthead">
    <nav class="topbar" aria-label="Primary">
      <a class="brand" href="#content" aria-label="{html.escape(title)} home">
        <span class="brand-mark" aria-hidden="true"></span>
        <span>{html.escape(title)}</span>
      </a>
      <div class="topbar-actions">
        <a href="{readme_url}" target="_blank" rel="noreferrer">README</a>
        <a href="{repo_url}" target="_blank" rel="noreferrer">GitHub</a>
      </div>
    </nav>
    <section class="hero" aria-labelledby="page-title">
      <canvas id="latent-map" aria-hidden="true"></canvas>
      <div class="latent-diagram" aria-hidden="true">{node_html}</div>
      <div class="hero-shade" aria-hidden="true"></div>
      <div class="hero-inner">
        <p class="eyebrow">Joint Embedding Predictive Architectures</p>
        <h1 id="page-title">{html.escape(title)}</h1>
        <p class="lede">{html.escape(tagline)}</p>
        <div class="intro-copy">{intro_html}</div>
        <div class="hero-tools" role="search">
          <label class="search-box" for="resource-search">
            <span class="search-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Filter resources</span>
            <input id="resource-search" type="search" autocomplete="off" placeholder="Filter papers, code, datasets">
          </label>
          <a class="hero-link" href="#foundations">Explore</a>
        </div>
        <dl class="stats" aria-label="Collection summary">
          <div>
            <dt>{resources}</dt>
            <dd>Resources</dd>
          </div>
          <div>
            <dt>{domains}</dt>
            <dd>Domains</dd>
          </div>
          <div>
            <dt>{html.escape(checked)}</dt>
            <dd>Verified</dd>
          </div>
        </dl>
      </div>
    </section>
  </header>
  <main id="content" class="page-shell">
    <aside class="toc-panel" aria-label="Table of contents">
      <div class="toc-sticky">
        <p class="toc-title">Index</p>
        <nav>{nav}</nav>
      </div>
    </aside>
    <article class="content-prose" id="resource-root">
      {article}
    </article>
  </main>
  <footer class="site-footer">
    <a href="{readme_url}" target="_blank" rel="noreferrer">README source</a>
    <span>CC0</span>
  </footer>
  <script id="site-data" type="application/json">{site_data}</script>
  <script src="assets/main.js?v={digest}"></script>
</body>
</html>
"""


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    (DIST / "assets").mkdir()
    (DIST / "index.html").write_text(render_page(), encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    for asset in ASSETS.iterdir():
        if asset.is_file():
            shutil.copy2(asset, DIST / "assets" / asset.name)


if __name__ == "__main__":
    build()
