#!/usr/bin/env python3
"""Package kit 13 on the explicitly assigned documentation branch; never touch application code."""
from pathlib import Path
import csv,hashlib,json,subprocess,zipfile,io

ROOT=Path(__file__).resolve().parents[1]
KIT=ROOT/'hoan-thien-f02-f04-f07-f15'
BRANCH='tai_lieu_hoan_thien_F02_F04_F07_F15_docx'
ARCHIVE=ROOT/'bundles/13-integration-four-features/13-F02-F04-F07-F15-integration-kit.zip'
def sha(b):return hashlib.sha256(b).hexdigest()
def csvbytes(rows,fields):
 s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);return s.getvalue().encode()
def main():
 branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
 if branch!=BRANCH:raise SystemExit('Refusing packaging outside assigned branch')
 files=[]
 for p in sorted(KIT.rglob('*')):
  if p.is_symlink():raise ValueError('Symlink in kit')
  if p.is_file() and p.name not in ['CHECKSUMS.csv','FILE-INDEX.csv']:
   if p.stat().st_size>100*1024*1024 or p.suffix in ['.pyc','.sqlite3','.db','.key','.pem']:raise ValueError('Unsafe file size/type')
   files.append(p)
 if len(files)>20000:raise ValueError('Too many kit files')
 rows=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files]
 (KIT/'CHECKSUMS.csv').write_bytes(csvbytes(rows,['path','bytes','sha256']))
 index=[dict(r,kind='source_reference' if '/source-reference/' in r['path'] else 'historical_document' if '/archive-docs/' in r['path'] else 'current_handover') for r in rows]
 (KIT/'FILE-INDEX.csv').write_bytes(csvbytes(index,['path','bytes','sha256','kind']))
 files+= [KIT/'CHECKSUMS.csv',KIT/'FILE-INDEX.csv']
 ARCHIVE.parent.mkdir(parents=True,exist_ok=True)
 contents=[]
 with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(files):
   if p.is_relative_to(KIT/'source-reference') or p.is_relative_to(KIT/'archive-docs'):continue
   b=p.read_bytes();name=p.relative_to(ROOT).as_posix()
   i=zipfile.ZipInfo(name,(2026,10,19,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16
   z.writestr(i,b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
   contents.append({'path':name,'bytes':len(b),'sha256':sha(b),'bundle_id':'13','archive':ARCHIVE.relative_to(ROOT).as_posix()})
 (ROOT/'catalog/INTEGRATION-CONTENTS.csv').write_bytes(csvbytes(contents,['path','bytes','sha256','bundle_id','archive']))
 catalog_path=ROOT/'catalog/BUNDLES.json';catalog=json.loads(catalog_path.read_text())
 ev=json.loads((KIT/'evidence/branch-and-conflicts.json').read_text())
 record={'id':'13','title':'F02 F04 F07 F15 — bộ hoàn thiện và tích hợp an toàn','purpose':'Entry point mới trên nhánh tổng hợp; yêu cầu, prompt, conflict map, source pin, thiết kế và audit lịch sử. Không là verdict runtime.','archive':ARCHIVE.relative_to(ROOT).as_posix(),'sha256':sha(ARCHIVE.read_bytes()),'archive_bytes':ARCHIVE.stat().st_size,'file_count':len(contents),'uncompressed_bytes':sum(x['bytes'] for x in contents),'role':'review_update','contents_file':'catalog/INTEGRATION-CONTENTS.csv','application_commit':ev['refs']['main']['sha'],'feature_heads':{k:v['sha'] for k,v in ev['refs'].items() if k!='main'}}
 catalog['bundles']=[b for b in catalog['bundles'] if b['id']!='13']+[record]
 catalog_path.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'catalog/SHA256SUMS').write_text(''.join(f"{b['sha256']}  {b['archive']}\n" for b in catalog['bundles']))
 (ARCHIVE.parent/'README.md').write_text('# ZIP13 Bộ tích hợp bốn tính năng\n\n[Đọc hướng dẫn mới](../../hoan-thien-f02-f04-f07-f15/00-READ-FIRST.md).\n\n[ZIP hướng dẫn](13-F02-F04-F07-F15-integration-kit.zip) chứa tài liệu điều phối, prompt, DOCX, provenance và inventories. Source snapshots và archive-docs dung lượng lớn nằm nguyên byte trong thư mục kit trên nhánh; ZIP13 không lặp lại các file đó. Clone toàn nhánh để có đủ tài nguyên. ZIP00–12 gốc F07 giữ nguyên ở bundles; clone toàn nhánh để có cả lịch sử.\n\nKiểm tra `python3 tools/bundles.py verify`; giải nén `python3 tools/bundles.py extract 13 --dest /tmp/family-bridge-integration-reading` vào thư mục đọc riêng. Không chép snapshot lên ứng dụng hoặc tự chạy script trong archive.\n')
 print(json.dumps({'files':len(contents),'zip_bytes':ARCHIVE.stat().st_size,'sha256':record['sha256']},ensure_ascii=False))
if __name__=='__main__':main()
