"""Lossless local checkpoint, deterministic gzip, no publishing or chain edits."""
from pathlib import Path
import gzip,hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[4];O=ROOT/'_local/codex_k_montaj'
source=O/'k73a.glb';target=O/'k73.glb.gz'
with source.open('rb') as inp,target.open('wb') as out:
    with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0,compresslevel=6) as gz:shutil.copyfileobj(inp,gz)
def digest(stream):
    h=hashlib.sha256()
    for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
with source.open('rb') as f:a=digest(f)
with gzip.open(target,'rb') as f:b=digest(f)
assert a==b and target.stat().st_size<100_000_000
report={'source_step':61,'local_steps':[70,71,72,73],'latest_raw_sha256':a,
        'gzip_bytes':target.stat().st_size,'lossless':a==b,'full_montage_completed':False,
        'chain_integrated':False,'published':False,
        'audits':{str(i):json.loads((O/f'step{i}_audit.json').read_text(encoding='utf8'))['passed'] for i in (71,72,73)}}
(O/'checkpoint.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report),flush=True)
