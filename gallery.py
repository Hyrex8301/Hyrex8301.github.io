#!/usr/bin/env python3
"""Build the photo galleries on the hobby pages from the images/ folders.

Workflow:
  1. Drop image files into images/<hobby>/  (one folder per hobby).
  2. Add a line for each to images/<hobby>/captions.txt:  filename | description
  3. Run:  python3 gallery.py

For every hobby this rewrites three regions and nothing else:
  - <!-- hero:start -->   .. <!-- hero:end -->            in <hobby>.html
  - <!-- gallery:start --> .. <!-- gallery:end -->        in <hobby>.html
  - <!-- thumb:<hobby>:start --> .. <!-- ...:end -->      in index.html

Text outside the markers is never touched, so you can write freely around them.
Running it again with no new files makes no changes. Standard library only, and
nothing here ships to the website: it just edits the HTML you commit.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"

# Hobby slugs. Each needs an images/<slug>/ folder and a <slug>.html page.
# Add a slug here when you add a hobby.
HOBBIES = ["climbing", "parkour", "tennis", "video-games"]

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}


def parse_captions(path: Path, warnings: list[str]) -> dict[str, str]:
    """Read captions.txt into {filename: description}."""
    captions: dict[str, str] = {}
    if not path.exists():
        return captions
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "|" not in line:
            warnings.append(f"{path}: line {lineno} has no '|', skipped")
            continue
        name, desc = line.split("|", 1)
        captions[name.strip()] = desc.strip()
    return captions


def find_images(folder: Path) -> list[str]:
    if not folder.is_dir():
        return []
    names = [
        p.name
        for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    ]
    return sorted(names)


def pick_hero(images: list[str]) -> str | None:
    """A file named hero.* wins; otherwise the first file alphabetically."""
    for name in images:
        if Path(name).stem.lower() == "hero":
            return name
    return images[0] if images else None


def replace_region(text: str, marker: str, new_inner: str, path: Path) -> str:
    pattern = re.compile(
        r"([ \t]*)(<!-- " + re.escape(marker) + r":start -->)"
        r".*?"
        r"(<!-- " + re.escape(marker) + r":end -->)",
        re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        raise SystemExit(
            f"{path.name}: missing markers "
            f"<!-- {marker}:start --> .. <!-- {marker}:end -->"
        )
    indent = m.group(1)
    replacement = f"{indent}{m.group(2)}\n{new_inner}\n{indent}{m.group(3)}"
    return text[: m.start()] + replacement + text[m.end() :]


def build_gallery(slug: str, images: list[str], captions: dict[str, str]) -> str:
    if not images:
        return (
            f"  <!-- No photos yet. Add files to images/{slug}/ and run "
            f"python3 gallery.py -->"
        )
    lines = ['  <ul class="gallery">']
    for name in images:
        src = html.escape(f"images/{slug}/{name}", quote=True)
        alt = html.escape(captions.get(name, ""), quote=True)
        lines.append(f'    <li><img src="{src}" alt="{alt}"></li>')
    lines.append("  </ul>")
    return "\n".join(lines)


def main() -> int:
    if not IMAGES.is_dir():
        print(f"No images/ folder next to {Path(__file__).name}", file=sys.stderr)
        return 1

    warnings: list[str] = []
    index_path = ROOT / "index.html"
    index_text = index_path.read_text(encoding="utf-8")

    for slug in HOBBIES:
        page = ROOT / f"{slug}.html"
        if not page.exists():
            warnings.append(f"{slug}.html not found, skipped")
            continue

        folder = IMAGES / slug
        captions = parse_captions(folder / "captions.txt", warnings)
        images = find_images(folder)

        for name in images:
            if name not in captions:
                warnings.append(
                    f'images/{slug}/{name} has no caption, using alt="" for now'
                )
        for name in captions:
            if name not in images:
                warnings.append(
                    f"images/{slug}/captions.txt lists {name}, not in the folder"
                )

        hero = pick_hero(images)
        text = page.read_text(encoding="utf-8")

        if hero is not None:
            src = html.escape(f"images/{slug}/{hero}", quote=True)
            alt = html.escape(captions.get(hero, ""), quote=True)
            hero_html = f'  <img class="hero" src="{src}" alt="{alt}">'
        else:
            hero_html = (
                f"  <!-- No photo yet. Add files to images/{slug}/ and run "
                f"python3 gallery.py -->"
            )
        text = replace_region(text, "hero", hero_html, page)

        text = replace_region(text, "gallery", build_gallery(slug, images, captions), page)
        page.write_text(text, encoding="utf-8")

        if hero is not None:
            src = html.escape(f"images/{slug}/{hero}", quote=True)
            thumb = f'        <img src="{src}" alt="" width="64" height="64">'
        else:
            thumb = (
                f"        <!-- No photo yet. Add one to images/{slug}/ and run "
                f"python3 gallery.py -->"
            )
        index_text = replace_region(index_text, f"thumb:{slug}", thumb, index_path)

        count = len(images)
        detail = f"hero {hero}" if hero else "no images"
        print(f"{slug}: {count} image{'' if count == 1 else 's'}, {detail}")

    index_path.write_text(index_text, encoding="utf-8")

    if warnings:
        print("\nwarnings:", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
