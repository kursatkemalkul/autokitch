"""Verify every preserved cable against replacement walls, divider and lids."""
from pathlib import Path
import json, math
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union
ROOT=Path(__file__).resolve().parents[3]
A=ROOT/'otonom/hat3d/robot-integrated-v27'
p=json.loads((A/'floor_plan.json').read_text())
old=json.loads((ROOT/'otonom/hat3d/robot-integrated-v25/floor_plan.json').read_text())
def geom(rows):return unary_union([Polygon(x['outer'],x['holes']) for x in rows])
foot=geom(p['trench']);ports=geom(p['openings']);throats=geom(p['lid_passages'])
errors=[];rows=[]
for name,c in old['cables'].items():
    r=c['radius_m'];n=0;bad=[]
    for a,b in zip(c['points'],c['points'][1:]):
        steps=max(1,math.ceil(math.dist(a,b)/.002))
        for i in range(steps+1):
            q=[a[k]+(b[k]-a[k])*i/steps for k in range(3)]
            x,y,z=q
            if y-r>=0:continue
            n+=1;pt=Point(x,z);disk=pt.buffer(r+.002,quad_segs=8)
            if y-r<-.0985+.002:bad.append(('bottom',q))
            if y-r<-.003 and not foot.covers(disk):bad.append(('side',q))
            if y+r>-.003-.002 and not throats.covers(disk):bad.append(('lid/throat',q))
            if y+r>-.039-.002+.0000001 and y-r<-.0375+.002-.0000001 and not ports.covers(disk):bad.append(('divider',q))
    if bad:errors.append({'cable':name,'count':len(bad),'first':bad[:3]})
    rows.append({'cable':name,'subfloor_samples':n,'new_shell_collisions':len(bad),'source_route_unchanged':True})
out={'version':27,'sample_step_m':.002,'required_clearance_m':.002,'cables':rows,'errors':errors,'passed':not errors}
(A/'route_audit.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({'cables':len(rows),'samples':sum(x['subfloor_samples'] for x in rows),'errors':errors,'passed':not errors}))
if errors:raise SystemExit(1)
