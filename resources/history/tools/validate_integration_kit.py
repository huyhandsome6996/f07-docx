#!/usr/bin/env python3
"""Read-only bounded verification of the integration handover; executes no archived code."""
from pathlib import Path, PurePosixPath
import csv, hashlib, json, zipfile

ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'hoan-thien-f02-f04-f07-f15'
MAX_FILES=20000
MAX_FILE_BYTES=100*1024*1024

def safe(name):
    p=PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and '.git' not in p.parts and '\\' not in name and ':' not in name

def checked(path):
    if path.is_symlink() or not path.resolve().is_relative_to(ROOT):raise ValueError('Unsafe source path')
    if path.stat().st_size>MAX_FILE_BYTES:raise ValueError('File exceeds validation bound')
    return path.read_bytes()

def main():
    with (KIT/'CHECKSUMS.csv').open(newline='',encoding='utf8') as f:rows=list(csv.DictReader(f))
    if not rows or len(rows)>MAX_FILES:raise ValueError('Invalid inventory size')
    if len({r['path'] for r in rows})!=len(rows):raise ValueError('Duplicate path')
    for r in rows:
        if not safe(r['path']):raise ValueError('Unsafe inventory path')
        b=checked(ROOT/r['path'])
        if len(b)!=int(r['bytes']) or hashlib.sha256(b).hexdigest()!=r['sha256']:raise ValueError('Checksum mismatch: '+r['path'])
    excluded={KIT/'CHECKSUMS.csv',KIT/'FILE-INDEX.csv'}
    actual={p.relative_to(ROOT).as_posix() for p in KIT.rglob('*') if p.is_file() and p not in excluded}
    if actual!={r['path'] for r in rows}:raise ValueError('Inventory coverage mismatch')
    with (KIT/'evidence/SOURCE-FILES.csv').open(newline='',encoding='utf8') as f:sources=list(csv.DictReader(f))
    for r in sources:
        b=checked(ROOT/r['destination'])
        if len(b)!=int(r['bytes']) or hashlib.sha256(b).hexdigest()!=r['sha256']:raise ValueError('Source provenance mismatch')
    for p in KIT.rglob('*.zip'):
        with zipfile.ZipFile(p) as z:
            infos=z.infolist()
            if len(infos)>MAX_FILES:raise ValueError('ZIP entry bound exceeded')
            names=[i.filename for i in infos if not i.is_dir()]
            if len(names)!=len(set(names)):raise ValueError('Duplicate ZIP names')
            for i in infos:
                if not safe(i.filename) or (i.external_attr>>16)&0o170000==0o120000 or i.flag_bits&1:raise ValueError('Unsafe ZIP member')
                if i.file_size>MAX_FILE_BYTES:raise ValueError('ZIP member too large')
            if z.testzip():raise ValueError('ZIP CRC failed')
    if checked(ROOT/'PROMPT-COPY-F02-F04-F07-F15.md')!=checked(KIT/'prompts/01-LEAD-HOAN-THIEN.md'):raise ValueError('Launcher prompt differs')
    json.loads(checked(KIT/'evidence/branch-and-conflicts.json'))
    print(f'PASS: {len(rows)} kit files, {len(sources)} pinned source files, original ZIP members and prompt equality. Application runtime NOT_RUN by this checker.')

if __name__=='__main__':main()
