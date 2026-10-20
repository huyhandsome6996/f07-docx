#!/usr/bin/env python3
"""List, verify and extract archived reference data; never execute its content."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if not name or path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name or '\x00' in name or '.git' in path.parts:
        raise ValueError(f'Unsafe archive path: {name!r}')
    return path


def load_catalog():
    catalog = json.loads((ROOT / 'catalog/BUNDLES.json').read_text(encoding='utf-8'))
    bundles = {b['id']: b for b in catalog['bundles']}
    if len(bundles) != len(catalog['bundles']):
        raise ValueError('Duplicate bundle IDs')
    with (ROOT / 'catalog/CONTENTS.csv').open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    extra_catalogs = {b['contents_file'] for b in bundles.values() if b.get('contents_file')}
    for name in sorted(extra_catalogs):
        inventory = ROOT.joinpath(*safe_path(name).parts)
        if not inventory.resolve().is_relative_to(ROOT):
            raise ValueError('Inventory escapes repository')
        with inventory.open(newline='', encoding='utf-8') as f:
            rows.extend(csv.DictReader(f))
    if len({r['path'] for r in rows}) != len(rows):
        raise ValueError('Duplicate catalog file paths')
    return catalog, bundles, rows


def read_bundle(bundle):
    archive = ROOT.joinpath(*safe_path(bundle['archive']).parts)
    if not archive.resolve().is_relative_to(ROOT):
        raise ValueError('Archive escapes repository')
    raw = archive.read_bytes()
    if len(raw) != bundle['archive_bytes'] or sha(raw) != bundle['sha256']:
        raise ValueError(f"ZIP checksum/size mismatch: {bundle['id']}")
    result = {}
    with ZipFile(io.BytesIO(raw)) as z:
        for info in z.infolist():
            safe_path(info.filename)
            if (info.external_attr >> 16) & 0o170000 == 0o120000 or info.flag_bits & 1:
                raise ValueError('Symlink or encrypted archive entry')
            if info.is_dir():
                continue
            if info.filename in result:
                raise ValueError('Duplicate ZIP entry')
            result[info.filename] = z.read(info)
    if len(result) != bundle['file_count'] or sum(map(len, result.values())) != bundle['uncompressed_bytes']:
        raise ValueError(f"ZIP content totals mismatch: {bundle['id']}")
    return result


def check_rows(data, rows):
    if set(data) != {r['path'] for r in rows}:
        raise ValueError('ZIP paths differ from CONTENTS.csv')
    for row in rows:
        raw = data[row['path']]
        if len(raw) != int(row['bytes']) or sha(raw) != row['sha256']:
            raise ValueError(f"File checksum mismatch: {row['path']}")


def verify(catalog, bundles, rows):
    original = read_bundle(bundles['00'])
    source_rows = [r for r in rows if bundles.get(r['bundle_id'], {}).get('role') == 'partition']
    check_rows(original, source_rows)
    manifest = list(csv.DictReader(io.StringIO(original['MANIFEST-SHA256.csv'].decode('utf-8-sig'))))
    if len({r['Path'] for r in manifest}) != len(manifest):
        raise ValueError('Duplicate paths in original manifest')
    if {r['Path'] for r in manifest} != set(original) - {'MANIFEST-SHA256.csv'}:
        raise ValueError('Original manifest coverage mismatch')
    for row in manifest:
        raw = original[row['Path']]
        if len(raw) != int(row['Bytes']) or sha(raw).lower() != row['SHA256'].lower():
            raise ValueError('Original input manifest mismatch')
    seen = set()
    update_count = 0
    for key, bundle in bundles.items():
        if key == '00':
            continue
        data = read_bundle(bundle)
        selected = [r for r in rows if r['bundle_id'] == key]
        if any(r['archive'] != bundle['archive'] for r in selected):
            raise ValueError('Catalog archive mapping mismatch')
        check_rows(data, selected)
        if bundle.get('role') == 'review_update':
            update_count += len(data)
            continue
        if bundle.get('role') != 'partition':
            raise ValueError(f'Unsupported bundle role: {key}')
        if seen.intersection(data):
            raise ValueError('File appears in multiple partition bundles')
        for name, raw in data.items():
            if raw != original[name]:
                raise ValueError('Partition changed original bytes')
        seen.update(data)
    if seen != set(original) or len(seen) != catalog['source_file_count']:
        raise ValueError('Partitions do not fully reconstruct the original')
    expected = ''.join(f"{b['sha256']}  {b['archive']}\n" for b in bundles.values())
    if (ROOT / 'catalog/SHA256SUMS').read_text(encoding='utf-8') != expected:
        raise ValueError('SHA256SUMS mismatch')
    print(f"OK: {len(bundles)} ZIPs; {len(original)} original files preserved; {len(manifest)} original manifest hashes matched; partitions complete, disjoint and byte-identical; {update_count} update files verified.")


def extract(bundle, rows, destination: str):
    data = read_bundle(bundle)
    if bundle['id'] == '00':
        with (ROOT / 'catalog/CONTENTS.csv').open(newline='', encoding='utf-8') as f:
            selected = list(csv.DictReader(f))
    else:
        selected = [r for r in rows if r['bundle_id'] == bundle['id']]
    check_rows(data, selected)
    dest = Path(destination).absolute()
    if dest.is_symlink() or (dest / '.git').exists() or dest.resolve().is_relative_to(ROOT):
        raise ValueError('Choose a separate reading directory outside this repository and existing Git checkouts')
    targets = []
    for name, raw in data.items():
        target = dest.joinpath(*safe_path(name).parts)
        if target.is_symlink() or any(p.is_symlink() for p in target.parents):
            raise ValueError(f'Refusing symlink destination: {name}')
        if not target.resolve().is_relative_to(dest.resolve()):
            raise ValueError('Extraction escapes destination')
        if target.exists() and (not target.is_file() or target.read_bytes() != raw):
            raise ValueError(f'Refusing to overwrite a different existing file: {name}')
        targets.append((target, raw))
    for target, raw in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            with target.open('xb') as f:
                f.write(raw)
    print(f"OK: bundle {bundle['id']}, {len(targets)} files verified/extracted into {dest}; no scripts executed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list', help='Show available ZIP bundles')
    sub.add_parser('verify', help='Verify all ZIPs and lossless reconstruction')
    extraction = sub.add_parser('extract', help='Extract one verified bundle without overwriting changed files')
    extraction.add_argument('bundle_id')
    extraction.add_argument('--dest', required=True)
    args = parser.parse_args()
    catalog, bundles, rows = load_catalog()
    if args.command == 'list':
        for bundle in bundles.values():
            print(f"{bundle['id']} | {bundle['file_count']:3} files | {bundle['title']} | {bundle['archive']}")
    elif args.command == 'verify':
        verify(catalog, bundles, rows)
    else:
        key = args.bundle_id.zfill(2)
        if key not in bundles:
            parser.error(f'Unknown bundle ID: {args.bundle_id}')
        extract(bundles[key], rows, args.dest)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        raise SystemExit(f'ERROR: {error}')
