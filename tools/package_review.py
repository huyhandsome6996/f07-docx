#!/usr/bin/env python3
"""Rebuild supplemental review bundle 10; preserve original bundles 00-09."""
import csv
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'updates/2026-10-18-f07-review'
ARCHIVE = ROOT / 'bundles/10-independent-review/10-f07-independent-review-2026-10-18.zip'
MANIFEST = REVIEW / 'MANIFEST-SHA256.csv'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def csv_text(rows, fields):
    output = io.StringIO(newline='')
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


if not REVIEW.is_dir():
    raise SystemExit('Missing review directory')
files = []
for path in sorted(REVIEW.rglob('*')):
    if path.is_symlink() or not path.resolve().is_relative_to(REVIEW):
        raise SystemExit('Refusing a symlink or escaping review path')
    if path.is_file() and path != MANIFEST:
        if '__pycache__' in path.parts or path.suffix in {'.pyc', '.sqlite3', '.pem', '.key', '.env'}:
            raise SystemExit(f'Refusing generated/private file type: {path.name}')
        files.append(path)
manifest_rows = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                  'sha256': digest(p.read_bytes())} for p in files]
MANIFEST.write_text(csv_text(manifest_rows, ['path', 'bytes', 'sha256']), encoding='utf-8', newline='')
files.append(MANIFEST)
files.sort()
ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
inventory = []
with ZipFile(ARCHIVE, 'w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
    for path in files:
        name = path.relative_to(ROOT).as_posix()
        raw = path.read_bytes()
        info = ZipInfo(name, date_time=(2026, 10, 18, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, raw, compress_type=ZIP_DEFLATED, compresslevel=9)
        inventory.append({'path': name, 'bytes': len(raw), 'sha256': digest(raw),
                          'bundle_id': '10', 'archive': ARCHIVE.relative_to(ROOT).as_posix()})
(ROOT / 'catalog/REVIEW-CONTENTS.csv').write_text(csv_text(inventory,
    ['path', 'bytes', 'sha256', 'bundle_id', 'archive']), encoding='utf-8', newline='')
catalog_path = ROOT / 'catalog/BUNDLES.json'
catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
existing = [b for b in catalog['bundles'] if b['id'] == '10']
if existing and any(b.get('role') != 'review_update' for b in existing):
    raise SystemExit('Bundle 10 exists with a different role')
provenance = json.loads((REVIEW / 'PROVENANCE.json').read_text(encoding='utf-8'))
catalog['schema_version'] = 2
catalog['bundles'] = [b for b in catalog['bundles'] if b['id'] != '10'] + [{
    'id': '10', 'title': 'Review F07 độc lập sau coding agent',
    'purpose': 'Đọc trước: 6 finding tại bb75b2c, evidence MySQL/browser, repro và prompt tiếp tục.',
    'archive': ARCHIVE.relative_to(ROOT).as_posix(),
    'sha256': digest(ARCHIVE.read_bytes()), 'archive_bytes': ARCHIVE.stat().st_size,
    'file_count': len(inventory), 'uncompressed_bytes': sum(r['bytes'] for r in inventory),
    'role': 'review_update', 'contents_file': 'catalog/REVIEW-CONTENTS.csv',
    'application_commit': provenance['commit'],
}]
catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
(ROOT / 'catalog/SHA256SUMS').write_text(''.join(f"{b['sha256']}  {b['archive']}\n" for b in catalog['bundles']), encoding='utf-8')
(ARCHIVE.parent / 'README.md').write_text(
    '# 10 — Review F07 độc lập\n\nĐọc gói này trước bàn giao lịch sử. '
    'Có 6 finding tại bb75b2c, bằng chứng MySQL/browser, tests tái hiện, snapshot thay đổi và prompt tiếp tục.\n\n'
    f'ZIP: [{ARCHIVE.name}]({ARCHIVE.name}). Chứa {len(inventory)} tệp bổ sung, không thuộc 946 tệp lịch sử.\n\n'
    'Từ gốc repo: `python3 tools/bundles.py extract 10 --dest /tmp/f07-review-reading`. '
    'Sau đó đọc `updates/2026-10-18-f07-review/README.md`.\n\n'
    '[Đọc trực tiếp trong repo](../../updates/2026-10-18-f07-review/README.md).\n', encoding='utf-8')
print(f'Built supplemental ZIP 10: {len(inventory)} files, {ARCHIVE.stat().st_size} bytes. Original bundles preserved.')
