"""Portable JSON/NumPy handoff, without committing intermediate pickle files.
Only load the existing trusted local caches here. Restore does not use pickle
from the archive and does not assert production release or audit completion.
"""
from pathlib import Path
import sys,json,pickle,gzip,hashlib,zipfile,io,os
import numpy as np
ROOT=Path(__file__).resolve().parent;H=ROOT/'k1';DEST=ROOT/'claude_devir'
DEST.mkdir(exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for q in iter(lambda:f.read(1024*1024),b''):h.update(q)
 return h.hexdigest()
def equal(a,b):
 if isinstance(a,np.ndarray):return isinstance(b,np.ndarray) and a.dtype==b.dtype and np.array_equal(a,b)
 if isinstance(a,np.generic):return isinstance(b,type(a)) and bool(a==b)
 if isinstance(a,dict):return type(a)==type(b) and list(a)==list(b) and all(equal(a[k],b[k]) for k in a)
 if isinstance(a,(tuple,list)):return type(a)==type(b) and len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 return type(a)==type(b) and bool(a==b)
def encode(x,z,state):
 if isinstance(x,np.ndarray):
  name='arrays/'+str(state[0])+'.npy';state[0]+=1
  data=io.BytesIO();np.save(data,x,allow_pickle=False);z.writestr(name,data.getvalue())
  return {'type':'ndarray','file':name}
 if isinstance(x,np.generic):return {'type':'numpy_scalar','dtype':x.dtype.str,'value':x.item()}
 if type(x) is dict:return {'type':'dict','items':[[encode(k,z,state),encode(v,z,state)] for k,v in x.items()]}
 if isinstance(x,(list,tuple,set,frozenset)):return {'type':type(x).__name__,'items':[encode(v,z,state) for v in x]}
 if x is None or type(x) in (str,int,float,bool):return x
 raise TypeError('Unsupported handoff type '+repr(type(x)))
def decode(x,z):
 if not isinstance(x,dict):return x
 kind=x['type']
 if kind=='ndarray':return np.load(io.BytesIO(z.read(x['file'])),allow_pickle=False)
 if kind=='numpy_scalar':return np.dtype(x['dtype']).type(x['value'])
 if kind=='dict':return {decode(k,z):decode(v,z) for k,v in x['items']}
 return {'list':list,'tuple':tuple,'set':set,'frozenset':frozenset}[kind](decode(v,z) for v in x['items'])
def pack():
 paths=['plan_k_clip_full.pkl','k_parca_clip_verified.pkl','k_bil_clip.pkl']
 originals={n:pickle.loads((H/n).read_bytes()) for n in paths};archive=DEST/'devam_verisi.zip'
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  meta=encode(originals,z,[0]);z.writestr('metadata.json',json.dumps(meta,separators=(',',':'),ensure_ascii=False))
 with zipfile.ZipFile(archive) as z:restored=decode(json.loads(z.read('metadata.json')),z)
 assert equal(originals,restored),'Roundtrip differs from current full cache'
 source=ROOT/'electrical_clip_weld_candidate/A/hat3_v10ze.glb'
 expected='9ce8fdfd34ead660b71ef13660bacb7d451848747e6b4ace648af441c4ab7158'
 assert sha(source)==expected
 compressed=DEST/'hat3_v10ze.glb.gz'
 with source.open('rb') as src,compressed.open('wb') as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=6) as dst:
   for chunk in iter(lambda:src.read(1024*1024),b''):dst.write(chunk)
 h=hashlib.sha256()
 with gzip.open(compressed,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 assert h.hexdigest()==expected
 report={'branch':'codex/k-montaj','model_sha256':expected,'archive_sha256':sha(archive),'gzip_sha256':sha(compressed),
  'archive_bytes':archive.stat().st_size,'gzip_bytes':compressed.stat().st_size,'original_model_bytes':source.stat().st_size,
  'portable_roundtrip_exact':True,'objects':{n:{'original_pickle_sha256':sha(H/n)} for n in paths},
  'pickle_bytes_after_restore_may_differ':True,'all_previous_audits_are_evidence_not_automatic_release':True,'production_release':False}
 assert max(report['archive_bytes'],report['gzip_bytes'])<100*1024*1024
 (DEST/'paket_denetimi.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print('HANDOFF_PACKED',report,flush=True)
def restore():
 archive=DEST/'devam_verisi.zip';receipt=json.loads((DEST/'paket_denetimi.json').read_text())
 assert sha(archive)==receipt['archive_sha256']
 with zipfile.ZipFile(archive) as z:objects=decode(json.loads(z.read('metadata.json')),z)
 for name,value in objects.items():
  assert Path(name).name==name
  with (H/name).open('wb') as f:pickle.dump(value,f)
 dest=ROOT/'electrical_clip_weld_candidate/A/hat3_v10ze.glb';dest.parent.mkdir(parents=True,exist_ok=True)
 compressed=DEST/'hat3_v10ze.glb.gz';assert sha(compressed)==receipt['gzip_sha256']
 with gzip.open(compressed,'rb') as src,dest.open('wb') as dst:
  for chunk in iter(lambda:src.read(1024*1024),b''):dst.write(chunk)
 assert sha(dest)==receipt['model_sha256']
 manifest=H/'k_bil_clip.json';stat=dest.stat()
 manifest.write_text(json.dumps({'source':{'path':str(dest.resolve()),'size':stat.st_size,'mtime_ns':stat.st_mtime_ns},'unit':'mm','restored_from_verified_portable_archive':True},indent=2),encoding='utf-8')
 (DEST/'restore_receipt.json').write_text(json.dumps({'source_model_sha256':sha(dest),'archive_sha256':sha(archive),
  'restored_pickle_sha256':{n:sha(H/n) for n in objects},'must_rebind_audit_hashes_after_restore':True,'production_release':False},indent=2),encoding='utf-8')
 print('HANDOFF_RESTORED; regenerate hash bindings before auditing or export',flush=True)
if __name__=='__main__':restore() if '--restore' in sys.argv else pack()
