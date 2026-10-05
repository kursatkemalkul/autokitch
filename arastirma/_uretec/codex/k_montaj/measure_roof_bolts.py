"""Measure original U M8 shaft envelopes from actual mesh vertices, read only."""
from pathlib import Path
import sys,json,numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4];Y=ROOT/'arastirma/_uretec/h3/yama_v9'
for p in (Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(p))
from m8kit import Glb
O=ROOT/'_local/codex_k_montaj';g=Glb(str(O/'hat3_v10c.glb'));node='U_KE_GOVDE__paslanmaz'
P=np.unique(np.concatenate([p['X'] for p in g.dprims(node) if not p.get('gizli')]),axis=0);rows=[]
for x in (4100.,4300.):
    radial=np.linalg.norm(P[:,[0,2]]-[x,-700.],axis=1)
    # Native thread envelope uses 0.98*d, hence r=3.92 for nominal M8.
    shaft=P[(abs(radial-3.92)<.002)&(P[:,1]>1840)&(P[:,1]<1870)]
    assert len(shaft)>10,(x,'shaft geometry not found')
    limits=[round(float(shaft[:,1].min()),3),round(float(shaft[:,1].max()),3)]
    assert limits==[1847.5,1863.5],(x,limits)
    rows.append({'node':node,'x':x,'shaft_y':limits,'vertices':len(shaft),'modeled_shaft_radius_mm':3.92,'method':'actual native M8 thread-envelope vertices, U-owned node'})
(O/'roof_bolt_measurement.json').write_text(json.dumps(rows,indent=2),encoding='utf8');print(json.dumps(rows),flush=True)
