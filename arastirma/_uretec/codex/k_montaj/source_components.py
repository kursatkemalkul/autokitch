from pathlib import Path
import sys,json,hashlib,collections
import numpy as np
ROOT=Path(__file__).resolve().parents[4]; Y=ROOT/'arastirma/_uretec/h3/yama_v9'
for p in (Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(p))
from m8kit import Glb
OUT=ROOT/'_local/codex_k_montaj';src=OUT/'hat3_v10c.glb'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='948b20c4520cf917711a8dea730ea037379793b11bb6e975c649155c83ef9c1d'
g=Glb(str(src)); names=sorted({p['name'] for p in g.prims if p['name'].startswith(('K_','ELK_K')) and not p.get('gizli')})
records=[]
for name in names:
 try:g.bilesen(name,no=0)
 except (ValueError,IndexError) as e:print('EMPTY',name,flush=True);continue
 for b in g._bc[name]:
  records.append({'id':name+'['+str(b['no'])+']','node':name,'component':b['no'],'lo':b['lo'].tolist(),'hi':b['hi'].tolist(),'closed':bool(b['kapali']),'triangles':sum(len(t) for p,t in b['parca'])})
 print(name,len(g._bc[name]),flush=True)
report={'source_step':61,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'unit':'mm','components':records,'current_source':True,'legacy_cad_is_authoritative':False,'publish_allowed':False}
(OUT/'source_components.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('COMPONENTS',len(records),flush=True)
