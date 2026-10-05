import sys, numpy as np
sys.path.insert(0,'.')
from glb_oku import yukle
J,D=yukle('hat3_v8n.glb')
for nd in J['nodes']:
    n=nd.get('name','')
    if 'mesh' not in nd: continue
    if not ('TOPPING' in n): continue
    X,T=D[n]; mn=X.min(0); mx=X.max(0)
    pr=J['meshes'][nd['mesh']]['primitives'][0]; ex=pr.get('extras',{})
    print("%-40s %7d  x%7.1f-%7.1f y%7.1f-%7.1f z%7.1f-%7.1f  %s"%(n,len(T),mn[0],mx[0],mn[1],mx[1],mn[2],mx[2], str({k:(v if len(str(v))<60 else str(v)[:60]) for k,v in ex.items()})))
