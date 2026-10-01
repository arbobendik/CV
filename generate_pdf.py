#!/usr/bin/env python3
"""Render resume.html with Chrome and verify a single portrait A4 page."""

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-sandbox", action="store_true",
        help="Disable Chrome's sandbox when required by the execution environment.",
    )
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    chrome = os.environ.get("CHROME_BIN") or next(
        (path for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable")
         if (path := shutil.which(name))), None
    )
    if not chrome or not shutil.which("pdfinfo"):
        parser.error("Install Chrome/Chromium and pdfinfo (poppler-utils); optionally set CHROME_BIN.")

    with tempfile.TemporaryDirectory(prefix="resume-pdf-") as tmp:
        pdf = Path(tmp) / "resume.pdf"
        command = [
            chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
            f"--user-data-dir={tmp}/profile", f"--print-to-pdf={pdf}",
        ]
        if args.no_sandbox:
            command.append("--no-sandbox")
        command.append((root / "resume.html").as_uri())
        subprocess.run(command, check=True, timeout=60)
        info = subprocess.check_output(
            ["pdfinfo", str(pdf)], text=True, env={**os.environ, "LC_ALL": "C"},
        )
        pages = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
        size = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts", info, re.MULTILINE)
        if not (pages and pages[1] == "1" and size
                and abs(float(size[1]) - 595.28) < 1
                and abs(float(size[2]) - 841.89) < 1):
            raise SystemExit("Expected one portrait A4 page; existing resume.pdf was not replaced.\n" + info)
        shutil.copyfile(pdf, root / "resume.pdf")
    print(f"Generated {root / 'resume.pdf'} (1 page, A4 portrait).")


if __name__ == "__main__":
    main()
