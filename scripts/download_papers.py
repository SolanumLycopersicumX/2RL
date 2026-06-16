#!/usr/bin/env python3
"""Download arXiv PDFs listed in docs/references/paper_index.md."""

from __future__ import annotations

import csv
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ARXIV_ABS_RE = re.compile(r"https://arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5})")


@dataclass(frozen=True)
class PaperEntry:
    title: str
    arxiv_id: str
    abs_url: str
    pdf_url: str
    filename: str


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", title.strip().lower()).strip("_")
    return re.sub(r"_+", "_", slug)[:90]


def parse_markdown_table(index_path: Path) -> list[PaperEntry]:
    entries: list[PaperEntry] = []
    seen: set[str] = set()
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        match = ARXIV_ABS_RE.search(line)
        if not match:
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 4 or parts[0] == "Priority":
            continue
        title = parts[1]
        arxiv_id = match.group(1)
        if arxiv_id in seen:
            continue
        seen.add(arxiv_id)
        entries.append(
            PaperEntry(
                title=title,
                arxiv_id=arxiv_id,
                abs_url=f"https://arxiv.org/abs/{arxiv_id}",
                pdf_url=f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                filename=f"{arxiv_id}_{slugify(title)}.pdf",
            )
        )
    return entries


def download(url: str, destination: Path, timeout: int = 60) -> tuple[str, str]:
    if destination.exists() and destination.stat().st_size > 0:
        return "exists", ""

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "2RL-literature-downloader/0.1 "
            "(research project; contact: local user)"
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read()
    except urllib.error.HTTPError as exc:
        return "failed", f"HTTP {exc.code}: {exc.reason}"
    except urllib.error.URLError as exc:
        return "failed", str(exc.reason)
    except TimeoutError as exc:
        return "failed", str(exc)

    if not data.startswith(b"%PDF"):
        return "failed", "downloaded content is not a PDF"
    destination.write_bytes(data)
    return "downloaded", ""


def write_manifest(manifest_path: Path, rows: list[dict[str, str]]) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "title",
                "arxiv_id",
                "abs_url",
                "pdf_url",
                "filename",
                "status",
                "error",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index_path = root / "docs" / "references" / "paper_index.md"
    output_dir = root / "docs" / "references" / "papers"
    manifest_path = output_dir / "papers_manifest.csv"
    output_dir.mkdir(parents=True, exist_ok=True)

    entries = parse_markdown_table(index_path)
    if not entries:
        print("No arXiv entries found.", file=sys.stderr)
        return 1

    rows: list[dict[str, str]] = []
    failures = 0
    for index, entry in enumerate(entries, start=1):
        destination = output_dir / entry.filename
        status, error = download(entry.pdf_url, destination)
        if status == "failed":
            failures += 1
        print(f"[{index:02d}/{len(entries):02d}] {status}: {entry.arxiv_id} {entry.title}")
        if error:
            print(f"  error: {error}")
        rows.append(
            {
                "title": entry.title,
                "arxiv_id": entry.arxiv_id,
                "abs_url": entry.abs_url,
                "pdf_url": entry.pdf_url,
                "filename": entry.filename,
                "status": status,
                "error": error,
            }
        )
        time.sleep(0.5)

    write_manifest(manifest_path, rows)
    print(f"Wrote manifest: {manifest_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
