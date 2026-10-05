"""Intersect every new lower part with retained source K components.

Open source meshes are unresolved, never silently counted as collision-free.
"""
from lower_support import *
Y=H/'yama_v9'
for path in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
from m8kit import Glb
import sac_ent as SE
from current_cad import factory_from_source
factory=factory_from_source(K,OUT)
native_sides={s.ad:s.kati().translate((4000,0,0)) for s in factory.SAC if s.ad in ('sol_sac_urun_girisi','sag_sac_E_penceresi')}
model=Glb(str(OUT/'hat3_v10c.glb'));parts,_,_=build();new=[];bad=[];unknown=[];tested=0;reconstructed=[]
with_mounts='--mounts' in sys.argv
mount_replacements=[]
if with_mounts:
    from mechanism_mounts import build_mounts
    mounts,mount_report=build_mounts();parts+=mounts;mount_replacements=mount_report['replace']
for p in parts:
    sh=p['sh'];b=sh.BoundingBox(); new.append((p,SE.mf_ucgen(SE.ucgen(sh)),np.array([b.xmin,b.ymin,b.zmin]),np.array([b.xmax,b.ymax,b.zmax])))
for name in sorted({p['name'] for p in model.prims if p['name'].startswith(('K_','ELK_K')) and not p.get('gizli')}):
    try:model.bilesen(name,0)
    except (IndexError,ValueError):continue
    for b in model._bc[name]:
        lo,hi=b['lo'],b['hi']
        # Explicitly replaced source parts. Base sheet remains present, but
        # its twelve new holes are independently registered by step71.
        replaced=(name=='K_GOVDE__sac' and ((abs(lo[1]-862)<.05 and abs(hi[1]-892)<.05 and hi[2]-lo[2]>800) or (abs(lo[1]-791)<.05 and abs(hi[1]-889)<.05 and abs(hi[0]-lo[0]-40)<.05)))
        replaced|=(name=='K_GOVDE__celik' and ((abs(lo[1]-795)<.05 and abs(hi[1]-799)<.05) or (abs(lo[1]-886.9)<.05 and abs(hi[1]-891.4)<.05 and hi[0]-lo[0]<9)))
        for row in mount_replacements:
            x,z=row['center_xz']
            replaced|=(name==row['node'] and abs(lo[1]-row['lo_y'])<.05 and abs(hi[1]-row['hi_y'])<.05 and abs((lo[0]+hi[0])/2-x)<.05 and abs((lo[2]+hi[2])/2-z)<.05)
        if replaced:continue
        candidates=[r for r in new if np.all(np.minimum(hi,r[3])-np.maximum(lo,r[2])>1e-4)]
        if not candidates:continue
        triangles=np.concatenate([p['X'][p['T'][idx]] for p,idx in b['parca']])
        solid=SE.mf_ucgen(triangles)
        ident=f"{name}[{b['no']}]"
        if solid is None and ident in ('K_GOVDE__kabuk[0]','K_GOVDE__kabuk[1]'):
            # Old GLB has triangle T-junctions; never fill arbitrary missing
            # faces. Use the original manufacturing solid only after checking
            # every actual vertex against its exact surface (not 128 samples).
            key='sol_sac_urun_girisi' if b['no']==0 else 'sag_sac_E_penceresi'
            shape=native_sides[key]
            points=np.unique(triangles.reshape(-1,3),axis=0)
            errors=[shape.distance(cq.Vertex.makeVertex(*v)) for v in points]
            if max(errors)<=.01:
                solid=SE.mf_ucgen(SE.ucgen(shape))
                reconstructed.append({'source':ident,'method':'source native solid; every source vertex agrees','vertices_checked':len(points),'max_vertex_distance_mm':max(errors),'continuous_surface_equivalence_claimed':False})
        if solid is None:
            unknown.append({'component':ident,'new_parts':[p['ad'] for p,*_ in candidates]});continue
        for p,m,_,_ in candidates:
            assert m is not None,p['ad']
            tested+=1;volume=(m^solid).volume()
            if volume<.05:continue
            allowed=(p.get('stage')=='base_pem' and name=='K_GOVDE__sac' and abs(lo[1]-788)<.05 and abs(hi[1]-791)<.05)
            reason='Registered new PEM hole and controlled press fit in base sheet' if allowed else None
            if p['ad'].startswith('k72_itici_ayak_kaynagi_') and name=='K_ITICI__sac':
                x,z=map(float,p['ad'].split('_')[-3:-1])
                if abs(lo[1]-900)<.05 and abs((lo[0]+hi[0])/2-x)<.05 and abs((lo[2]+hi[2])/2-z)<.05:
                    allowed=True;reason='Explicit TIG post-to-plate weld penetration'
            row={'part':p['ad'],'source':ident,'volume_mm3':round(volume,4),'allowed':allowed,'reason':reason}
            if not allowed:bad.append(row)
    print('CONTEXT',name,'tested',tested,'collisions',len(bad),'unresolved',len(unknown),flush=True)
r={'scope':'new lower parts versus retained K/ELK_K only','pairs_tested':tested,'collisions':bad,'unresolved_open_source':unknown,'reconstructed_source_sides':reconstructed,'passed':not bad and not unknown,'whole_assembly_release':False}
(OUT/('k72_context_audit.json' if with_mounts else 'k71_context_audit.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(r,ensure_ascii=False),flush=True);sys.stdout.flush();os._exit(0 if r['passed'] else 2)
