#!/usr/bin/env python3
"""Extract text from downloaded PDFs using pdftotext."""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    papers_dir = root / "docs" / "references" / "papers"
    text_dir = root / "docs" / "paper_notes" / "extracted_text"
    text_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    failures = 0
    for pdf_path in sorted(papers_dir.glob("*.pdf")):
        txt_path = text_dir / f"{pdf_path.stem}.txt"
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), str(txt_path)],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        status = "extracted" if result.returncode == 0 and txt_path.exists() else "failed"
        if status == "failed":
            failures += 1
        rows.append(
            {
                "pdf": str(pdf_path.relative_to(root)),
                "text": str(txt_path.relative_to(root)),
                "status": status,
                "stderr": result.stderr.strip(),
            }
        )
        print(f"{status}: {pdf_path.name}")

    manifest = text_dir / "text_manifest.csv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["pdf", "text", "status", "stderr"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote manifest: {manifest}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
