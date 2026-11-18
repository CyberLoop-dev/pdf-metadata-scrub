#!/usr/bin/env python3
"""Inspect PDF metadata or write a separate metadata-clean copy."""
import argparse
import json
from pathlib import Path
import sys
from pypdf import PdfReader, PdfWriter

def ensure_distinct_paths(source, destination, force=False):
    src = Path(source).expanduser().resolve()
    dst = Path(destination).expanduser().resolve()
    if src == dst:
        raise ValueError("Output path must differ from the input path.")
    if dst.exists() and not force:
        raise FileExistsError(f"{dst} already exists; pass --force to replace it.")
    return src, dst

def metadata_report(metadata):
    return {str(key): str(value) for key, value in (metadata or {}).items()}

def inspect_pdf(path):
    reader = PdfReader(str(path))
    if reader.is_encrypted:
        raise ValueError("Encrypted PDFs are not supported.")
    return {"pages": len(reader.pages), "metadata": metadata_report(reader.metadata)}

def scrub_pdf(source, destination, force=False):
    src, dst = ensure_distinct_paths(source, destination, force)
    reader = PdfReader(str(src))
    if reader.is_encrypted:
        raise ValueError("Encrypted PDFs are not supported.")
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({})
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("wb") as stream:
        writer.write(stream)
    return dst

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inspect_cmd = sub.add_parser("inspect")
    inspect_cmd.add_argument("input")
    scrub_cmd = sub.add_parser("scrub")
    scrub_cmd.add_argument("input")
    scrub_cmd.add_argument("--output", required=True)
    scrub_cmd.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "inspect":
            print(json.dumps(inspect_pdf(args.input), indent=2, ensure_ascii=False))
        else:
            print(f"Clean copy written to {scrub_pdf(args.input, args.output, args.force)}")
    except (OSError, ValueError) as exc:
        print(f"pdf-metadata-scrub: {exc}", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
