"""Non-destructive check of local requirements. Not a substitute for live GitHub/Jenkins evidence."""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def check(label, good, detail=""):
    print(f"{'PASS' if good else 'FAIL'} {label}" + (f" — {detail}" if detail else ""))
    return bool(good)


def git(*args):
    p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else ''


def main():
    results = []
    required_dirs = ['app','scripts','config','logs','backup','tests','tools']
    results.append(check('Project directories', all((ROOT / d).is_dir() for d in required_dirs)))
    results.append(check('Files', all((ROOT / p).is_file() for p in [
        'Dockerfile','docker-compose.yml','Jenkinsfile','.gitignore',
        'logs/application.log','private.txt','public.txt','app/student.json'
    ])))
    logs = (ROOT / 'logs/application.log').read_text(encoding='utf-8').splitlines()
    results.append(check('Log: >= 10 lines', len(logs) >= 10))
    results.append(check('Log contains ERROR and WARNING', any('ERROR' in x for x in logs) and any('WARNING' in x for x in logs)))
    results.append(check('private.txt chmod 600', (ROOT/'private.txt').stat().st_mode & 0o777 == 0o600))
    results.append(check('public.txt chmod 644', (ROOT/'public.txt').stat().st_mode & 0o777 == 0o644))
    results.append(check('Five local Git commits', len(git('rev-list', '--all', '--count').splitlines()) == 1 and int(git('rev-list','--all','--count') or '0') >= 5, git('log','-1','--oneline')))
    results.append(check('GitHub remote configured', 'github.com/' in git('remote','get-url','origin')))
    ignore = subprocess.run(['git','check-ignore','logs/application.log'], cwd=ROOT,capture_output=True,text=True)
    results.append(check('Application log is ignored by Git',ignore.returncode == 0))
    print('\nLOCAL CHECKS:',sum(results),'/',len(results),'passed')
    print('Additionally demonstrate live Docker, GitHub and Jenkins in your own environment.')
    return 0 if all(results) else 1


if __name__ == '__main__':
    sys.exit(main())
