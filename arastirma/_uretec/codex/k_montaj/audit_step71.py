"""Step71 repeatability and strict station ownership audit (not full §5)."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parents[4];Y=ROOT/'arastirma/_uretec/h3/yama_v9'
for p in (Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(p))
from m8kit import Glb
OUT=ROOT/'_local/codex_k_montaj'
step=73 if '--step73' in sys.argv else 72 if '--step72' in sys.argv else 71
permitted=('K_GOVDE__kabuk','K_GOVDE__sac','K_GOVDE__baglanti') if step==73 else ('K_BANT__sac','K_BANT__celik','K_ITICI__sac','K_ITICI__celik') if step==72 else ('K_GOVDE__sac','K_GOVDE__celik')
source=Path(sys.argv[1]);a=Glb(str(source));b=Glb(str(OUT/f'k{step}a.glb'))
def sig(g):
    out={}
    for p in g.prims:
        if p.get('gizli') or p['name'] in permitted:continue
        P=p['X'][p['T']]
        P=P[np.linalg.norm(np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]),axis=1)>1e-6]
        Q=np.round(P,2)
        Q=Q[np.linalg.norm(np.cross(Q[:,1]-Q[:,0],Q[:,2]-Q[:,0]),axis=1)>1e-6]
        rows=np.sort(Q.view([('x','<f8'),('y','<f8'),('z','<f8')]).reshape(-1,3),axis=1).view('<f8').reshape(-1,9)
        out.setdefault(p['name'],[]).extend(sorted(set(row.tobytes() for row in rows)))
    return {k:hashlib.sha256(b''.join(sorted(v))).hexdigest() for k,v in out.items()}
s1,s2=sig(a),sig(b);changed=sorted(k for k in set(s1)|set(s2) if s1.get(k)!=s2.get(k))
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
r={'step':step,'two_runs_byte_identical':sha(OUT/f'k{step}a.glb')==sha(OUT/f'k{step}b.glb'),'changed_nodes_outside_K_lower_body':changed,'ownership_tolerance_mm':.01,'permitted_nodes':list(permitted),'subassembly_audit':json.loads((OUT/('k73_roof_audit.json' if step==73 else 'k72_mount_audit.json' if step==72 else 'k71_lower_audit.json')).read_text(encoding='utf8')),'full_assembly_release':False}
r['passed']=r['two_runs_byte_identical'] and not changed and r['subassembly_audit']['passed']
(OUT/f'step{step}_audit.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in r.items() if k!='subassembly_audit'}),flush=True)
