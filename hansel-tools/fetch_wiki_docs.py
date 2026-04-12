"""
fetch_wiki_docs.py — Télécharge toute la documentation modding du wiki CK3.

Utilise Playwright (navigateur headless) pour contourner la protection anti-bot.

Usage:
    python tools/fetch_wiki_docs.py [--dry-run] [--category "Category:Modding"]

Sortie : docs/wiki/<nom_page>.md + docs/wiki/index.md
"""

import sys
import os
import re
import time
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import html2text
from playwright.sync_api import sync_playwright, Page

from config import SUBMOD_ROOT
from ui import info, success, warn, dim

WIKI_BASE = "https://ck3.paradoxwikis.com"
OUTPUT_DIR = os.path.join(SUBMOD_ROOT, "docs", "wiki")
RATE_LIMIT = 1.0  # secondes entre pages


def sanitize_filename(title: str) -> str:
    name = title.replace(" ", "_").replace("/", "_")
    name = re.sub(r'[<>:"\\\|?*]', "", name)
    return name + ".md"


def enumerate_category_pages(page: Page, category: str, recursive: bool = True) -> list[str]:
    """Navigue vers la page de catégorie et collecte tous les titres de pages."""
    pages: set[str] = set()
    cats_to_visit = [category]
    visited_cats: set[str] = set()

    while cats_to_visit:
        cat = cats_to_visit.pop()
        if cat in visited_cats:
            continue
        visited_cats.add(cat)

        cat_url = f"{WIKI_BASE}/{cat.replace(' ', '_')}"
        dim(f"  Catégorie : {cat_url}")
        page.goto(cat_url, wait_until="domcontentloaded")
        page.wait_for_timeout(800)

        # Liens vers les pages membres
        links = page.query_selector_all(".mw-category a, #mw-pages a")
        for link in links:
            href = link.get_attribute("href") or ""
            title = link.get_attribute("title") or ""
            if (
                    href.startswith("/")
                    and not href.startswith("/Special:")
                    and title
                    and not title.startswith("Category:")
                    and not title.startswith("Template:")
                ):
                pages.add(title)

        # Sous-catégories
        if recursive:
            subcat_links = page.query_selector_all(".CategoryTreeItem a, #mw-subcategories a")
            for link in subcat_links:
                title = link.get_attribute("title") or ""
                if title.startswith("Category:"):
                    cats_to_visit.append(title)

        # Pagination "next page"
        next_link = page.query_selector("a:has-text('next page')")
        while next_link:
            next_href = next_link.get_attribute("href") or ""
            page.goto(f"{WIKI_BASE}{next_href}", wait_until="domcontentloaded")
            page.wait_for_timeout(800)
            links = page.query_selector_all(".mw-category a, #mw-pages a")
            for link in links:
                title = link.get_attribute("title") or ""
                href = link.get_attribute("href") or ""
                if (
                    href.startswith("/")
                    and not href.startswith("/Special:")
                    and title
                    and not title.startswith("Category:")
                    and not title.startswith("Template:")
                ):
                    pages.add(title)
            next_link = page.query_selector("a:has-text('next page')")

    return sorted(pages)


def fetch_page_markdown(page: Page, title: str) -> str | None:
    """Navigue vers une page wiki et extrait le contenu en markdown."""
    url = f"{WIKI_BASE}/{title.replace(' ', '_')}"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(500)
    except Exception as e:
        warn(f"Timeout/erreur pour '{title}': {e}")
        return None

    content_el = page.query_selector("#mw-content-text")
    if not content_el:
        warn(f"Contenu introuvable : '{title}'")
        return None

    html = content_el.inner_html()

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = True
    converter.body_width = 0
    converter.protect_links = False

    md = converter.handle(html)
    header = f"# {title}\n\n> Source : {url}\n\n"
    return header + md


def main():
    parser = argparse.ArgumentParser(description="Télécharge la doc modding du wiki CK3")
    parser.add_argument("--dry-run", action="store_true", help="Énumère les pages sans télécharger")
    parser.add_argument("--category", default="Category:Modding", help="Catégorie de départ")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = ctx.new_page()

        info(f"Énumération de '{args.category}'...")
        titles = enumerate_category_pages(page, args.category, recursive=True)
        info(f"{len(titles)} pages trouvées.")

        if args.dry_run:
            for t in titles:
                dim(f"  {t}")
            browser.close()
            return

        downloaded: list[str] = []
        skipped: list[str] = []

        for i, title in enumerate(titles, 1):
            dim(f"[{i}/{len(titles)}] {title}")
            md = fetch_page_markdown(page, title)
            time.sleep(RATE_LIMIT)

            if md is None:
                skipped.append(title)
                continue

            filename = sanitize_filename(title)
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md)
            downloaded.append(title)

        browser.close()

    # Générer l'index
    index_lines = [
        "# CK3 Wiki — Documentation Modding\n\n",
        f"> {len(downloaded)} pages téléchargées depuis `{args.category}`\n\n",
    ]
    for title in sorted(downloaded):
        filename = sanitize_filename(title)
        index_lines.append(f"- [{title}]({filename})\n")

    with open(os.path.join(OUTPUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.writelines(index_lines)

    success(f"Terminé : {len(downloaded)} pages dans {OUTPUT_DIR}/")
    if skipped:
        warn(
            f"{len(skipped)} pages ignorées : "
            f"{', '.join(skipped[:5])}{'...' if len(skipped) > 5 else ''}"
        )


if __name__ == "__main__":
    main()
