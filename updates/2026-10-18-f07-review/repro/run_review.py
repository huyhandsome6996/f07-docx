#!/usr/bin/env python3
"""Run review checks in the application's isolated Django test database."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', required=True, type=Path)
parser.add_argument('--database', choices=['sqlite', 'mysql'], default='sqlite')
args = parser.parse_args()
repo = args.repo.resolve()
if not (repo / 'tests/feature-lab/manage.py').is_file():
    parser.error('Expected a Family Bridge application checkout')
child = os.environ.copy()
child.update(DJANGO_SETTINGS_MODULE='harness.settings', DJANGO_ENV='test', FB_TEST_DB=args.database,
    FB_FEATURES='f01_identity,f15_privacy,f05_inbox,f03_cards,f04_ai,f06_drafts,f07_mood,f08_journal,f10_signal,f11_supporters,f13_help,f12_appointments,f09_activities,f02_program,f14_surveys,admin_core,f16_classroom')
child['PYTHONPATH'] = str(Path(__file__).resolve().parent) + os.pathsep + child.get('PYTHONPATH', '')
if args.database == 'mysql':
    required = ['FB_MYSQL_DB', 'FB_MYSQL_USER', 'FB_MYSQL_PASSWORD', 'FB_MYSQL_HOST', 'FB_MYSQL_PORT']
    missing = [name for name in required if not child.get(name)]
    if missing:
        parser.error('Missing local test DB bindings: ' + ', '.join(missing))
    if child['FB_MYSQL_HOST'] not in {'127.0.0.1', 'localhost', '::1'}:
        parser.error('Use a disposable MySQL instance bound to loopback')
raise SystemExit(subprocess.run([sys.executable, 'manage.py', 'test', 'review_regressions', '--noinput', '-v', '2'],
    cwd=repo / 'tests/feature-lab', env=child).returncode)
