#!/usr/bin/env python3
"""Build/verify this F04 archive without executing archived content."""
import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATED = {"catalog/CONTENTS.csv", "catalog/SHA256SUMS"}

def entries():
    result = []
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts or not path.is_file() or str(rel) in GENERATED:
            continue
        if path.is_symlink():
            raise SystemExit(f"Unexpected symlink: {rel}")
        data = path.read_bytes()
        result.append((str(rel), len(data), hashlib.sha256(data).hexdigest()))
    return result

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    rows = entries()
    if mode == "build":
        (ROOT / "catalog").mkdir(exist_ok=True)
        with (ROOT / "catalog/CONTENTS.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["path", "bytes", "sha256"])
            writer.writerows(rows)
        (ROOT / "catalog/SHA256SUMS").write_text(
            "".join(f"{digest}  {name}\n" for name, size, digest in rows), encoding="utf-8")
    elif mode == "verify":
        with (ROOT / "catalog/CONTENTS.csv").open(encoding="utf-8", newline="") as f:
            expected = [(r["path"], int(r["bytes"]), r["sha256"]) for r in csv.DictReader(f)]
        if rows != expected:
            raise SystemExit("FAILED: inventory, size, or checksum differs; inspect before rebuilding")
        checksum_text = "".join(f"{digest}  {name}\n" for name, size, digest in rows)
        if (ROOT / "catalog/SHA256SUMS").read_text(encoding="utf-8") != checksum_text:
            raise SystemExit("FAILED: SHA256SUMS differs")
    else:
        raise SystemExit("Usage: python3 tools/catalog.py build|verify")
    print(f"{mode.upper()} OK: {len(rows)} files, {sum(size for _, size, _ in rows)} bytes")

if __name__ == "__main__":
    main()
