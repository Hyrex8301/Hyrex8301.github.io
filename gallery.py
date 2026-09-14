#!/usr/bin/env python3
"""Build the photo/video galleries on the hobby pages from the images/ folders.

Workflow:
  1. Drop image or video files into images/<hobby>/  (one folder per hobby).
  2. Add a line for each to images/<hobby>/captions.txt:  filename | caption
  3. Write the page's description in images/<hobby>/description.txt (optional).
  4. Run:  python3 gallery.py

For every hobby this rewrites three regions and nothing else:
  - <!-- lead:start -->   .. <!-- lead:end -->            in <hobby>.html
  - <!-- gallery:start --> .. <!-- gallery:end -->        in <hobby>.html
  - <!-- thumb:<hobby>:start --> .. <!-- ...:end -->      in index.html

description.txt becomes the <p class="lead"> paragraphs under the heading. Every
photo and video shows its caption from captions.txt below it, in one grid. The
index.html thumbnail is always a photo (a file named hero.* wins, otherwise the
first photo alphabetically), since a 64x64 thumbnail can't be a video frame.

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
VIDEO_EXTS = {".mp4", ".mov", ".webm"}
MEDIA_EXTS = IMAGE_EXTS | VIDEO_EXTS


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


def read_description(path: Path) -> list[str]:
    """Return the paragraphs of description.txt (blank line = new paragraph).

    Lines starting with # are ignored, so a file that is all comments counts as
    empty.
    """
    if not path.exists():
        return []
    kept = [
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if not line.lstrip().startswith("#")
    ]
    block = "\n".join(kept).strip()
    if not block:
        return []
    return [" ".join(p.split()) for p in re.split(r"\n\s*\n", block) if p.strip()]


def find_media(folder: Path) -> list[str]:
    """Photos and videos together, sorted so captions.txt works the same for both."""
    if not folder.is_dir():
        return []
    names = [
        p.name
        for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in MEDIA_EXTS
    ]
    return sorted(names)


def pick_thumb(media: list[str]) -> str | None:
    """Which photo represents this hobby on the home page.

    A file named hero.* wins; otherwise the first photo alphabetically. Videos
    are never picked, since the home page thumbnail is a 64x64 image.
    """
    photos = [name for name in media if Path(name).suffix.lower() in IMAGE_EXTS]
    for name in photos:
        if Path(name).stem.lower() == "hero":
            return name
    return photos[0] if photos else None


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


def build_gallery(slug: str, media: list[str], captions: dict[str, str]) -> str:
    if not media:
        return (
            f"  <!-- Gallery grid: every photo and video in images/{slug}/. "
            f"Add files and run python3 gallery.py -->"
        )
    lines = ['  <ul class="gallery">']
    for name in media:
        src = html.escape(f"images/{slug}/{name}", quote=True)
        caption = captions.get(name, "")
        is_video = Path(name).suffix.lower() in VIDEO_EXTS
        lines.append("    <li>")
        lines.append("      <figure>")
        if is_video:
            lines.append(f'        <video src="{src}" controls></video>')
        else:
            alt = html.escape(caption, quote=True)
            lines.append(f'        <img src="{src}" alt="{alt}">')
        if caption:
            lines.append(f"        <figcaption>{html.escape(caption)}</figcaption>")
        lines.append("      </figure>")
        lines.append("    </li>")
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
        media = find_media(folder)

        for name in media:
            if name not in captions:
                warnings.append(
                    f'images/{slug}/{name} has no caption, using alt="" for now'
                )
        for name in captions:
            if name not in media:
                warnings.append(
                    f"images/{slug}/captions.txt lists {name}, not in the folder"
                )

        thumb_photo = pick_thumb(media)
        text = page.read_text(encoding="utf-8")

        # The page description under the heading, from description.txt.
        paragraphs = read_description(folder / "description.txt")
        if paragraphs:
            lead_html = "\n".join(
                f'  <p class="lead">{html.escape(p)}</p>' for p in paragraphs
            )
        else:
            lead_html = (
                f"  <!-- Write this page's description in "
                f"images/{slug}/description.txt, then run python3 gallery.py -->"
            )
        text = replace_region(text, "lead", lead_html, page)

        # The gallery grid: every photo and video.
        text = replace_region(
            text, "gallery", build_gallery(slug, media, captions), page
        )
        page.write_text(text, encoding="utf-8")

        if thumb_photo is not None:
            src = html.escape(f"images/{slug}/{thumb_photo}", quote=True)
            thumb = f'        <img src="{src}" alt="" width="64" height="64">'
        else:
            thumb = (
                f"        <!-- No photo yet. Add one to images/{slug}/ and run "
                f"python3 gallery.py -->"
            )
        index_text = replace_region(index_text, f"thumb:{slug}", thumb, index_path)

        count = len(media)
        detail = f"thumbnail {thumb_photo}" if thumb_photo else "no photo for thumbnail"
        print(f"{slug}: {count} file{'' if count == 1 else 's'}, {detail}")

    index_path.write_text(index_text, encoding="utf-8")

    if warnings:
        print("\nwarnings:", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
