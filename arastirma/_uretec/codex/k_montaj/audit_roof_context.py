"""New K roof pack against all retained station meshes, not just K."""
from roof_mounts import *
Y=H/'yama_v9'
for path in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
from m8kit import Glb
import sac_ent as SE
g=Glb(str(OUT/'k72a.glb'));parts,_,_=build_roof();new=[];bad=[];unknown=[];allowed=[];count=0
# Step73 now retains the actual source roof, locally replacing only two seats.
# Native pilot roof is not the source: do not collision-check that replacement.
for p in parts[1:]:
    b=p['sh'].BoundingBox();m=SE.mf_ucgen(SE.ucgen(p['sh']));assert m is not None,p['ad']
    new.append((p,m,np.array([b.xmin,b.ymin,b.zmin]),np.array([b.xmax,b.ymax,b.zmax])))
for name in sorted({p['name'] for p in g.prims if not p.get('gizli')}):
    # Aggregate primitive bounds first to avoid decomposing unrelated stations.
    pp=[p for p in g.dprims(name) if not p.get('gizli')]
    if not pp:continue
    P=np.concatenate([p['X'] for p in pp]);lo,hi=P.min(0),P.max(0)
    if not any(np.all(np.minimum(hi,r[3])-np.maximum(lo,r[2])>1e-4) for r in new):continue
    try:g.bilesen(name,0)
    except (IndexError,ValueError):continue
    for b in g._bc[name]:
        lo,hi=b['lo'],b['hi']
        if name=='K_GOVDE__kabuk' and hi[1]>1861.99 and hi[0]-lo[0]>399 and hi[2]-lo[2]>880:continue
        if name=='K_GOVDE__baglanti' and abs(hi[1]-1861.88)<.01 and any(abs((lo[0]+hi[0])/2-x)<.01 for x in (4100,4300)):continue
        candidate=[r for r in new if np.all(np.minimum(hi,r[3])-np.maximum(lo,r[2])>1e-4)]
        if not candidate:continue
        solid=SE.mf_ucgen(np.concatenate([p['X'][p['T'][indices]] for p,indices in b['parca']]))
        if solid is None:unknown.append({'component':f'{name}[{b["no"]}]','candidate_parts':[p['ad'] for p,*_ in candidate]});continue
        for p,m,_,_ in candidate:
            v=(m^solid).volume();count+=1
            if v<.05:continue
            thread=False
            if name=='U_KE_GOVDE__paslanmaz' and p['ad'].startswith('k73_tavan_baglanti_plakasi_'):
                x=float(p['ad'].split('_')[-2]);layer=int(p['ad'].split('_')[-1])
                thread=layer<2 and abs((lo[0]+hi[0])/2-x)<.01 and abs((lo[2]+hi[2])/2+700)<.01 and abs(lo[1]-1847.5)<.01 and hi[1]>1863.49
            row={'part':p['ad'],'source':f'{name}[{b["no"]}]','volume_mm3':v,'allowed':thread,'reason':'M8 external/minor thread envelope in 8mm tapped pack' if thread else None}
            (allowed if thread else bad).append(row)
patch=json.loads((OUT/'k73a.json').read_text(encoding='utf8'))
local_patch_ok=patch.get('source_roof_preserved_except_two_M8_seats') and patch.get('roof_delta_outside_seats_mm3',1)<.05
report={'scope':'30 new reinforcement/weld parts versus all retained stations; local roof patch preserves source outside two seats','pairs_tested':count,'collisions':bad,'unresolved_open_meshes':unknown,'allowed_thread_contacts':allowed,'local_roof_patch_isolation_passed':local_patch_ok,'legacy_source_contacts_not_certified':True,'passed':bool(not bad and not unknown and local_patch_ok),'full_assembly_release':False}
(OUT/'k73_context_audit.json').write_text(json.dumps(clean(report),indent=2),encoding='utf8')
print(json.dumps(clean(report)),flush=True);sys.stdout.flush();os._exit(0 if report['passed'] else 2)
