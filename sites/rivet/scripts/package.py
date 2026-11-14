"""Deterministic source ZIP; excludes credentials, Git state, dependencies, and itself."""
from pathlib import Path
import zipfile, hashlib
root=Path(__file__).resolve().parent.parent
files=[]
for folder in ['public','api','lib','tests','scripts']:
    files.extend(p for p in (root/folder).rglob('*') if p.is_file() and p.suffix not in ['.zip','.pyc'] and '__pycache__' not in p.parts)
files.extend(root/name for name in ['README.md','LICENSE','package.json','package-lock.json','server.mjs','vercel.json','.gitignore'])
output=root/'public/rivet-source.zip'
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
    for path in sorted(files):
        relative=path.relative_to(root).as_posix()
        info=zipfile.ZipInfo('rivet/'+relative,date_time=(2026,11,13,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
        archive.writestr(info,path.read_bytes())
print(hashlib.sha256(output.read_bytes()).hexdigest(),output.name)
