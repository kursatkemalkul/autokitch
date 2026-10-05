"""Screen native sheet definitions against actual source61 mesh vertices.

This is a sampled one-way geometry check, NOT a watertight equality proof.
Do not promote it to the final 0.01 mm assembly acceptance check.
"""
import sys
sys.dont_write_bytecode = True
exec(open(__file__.replace('surface_match.py','inspect_source.py'), encoding='utf-8-sig').read().split('g=K.kur();')[0])
import numpy as np
Y=H/'yama_v9'
for p in (Y/'kaynak',Y/'kaynak/gece'): sys.path.insert(0,str(p))
from m8kit import Glb
import cadquery as cq
model=Glb(str(OUT/'hat3_v10c.glb'))
from current_cad import factory_from_source
factory=factory_from_source(K, OUT)
matches={r['legacy_name']:r for r in json.loads((OUT/'source_matches.json').read_text(encoding='utf8'))}
rows=[]
for sheet in factory.SAC:
    m=matches[sheet.ad]
    if sheet.ad in ('onyuz_kapak_K','onyuz_kapak_K_ic_tava'):
        box=sheet.kati().BoundingBox(); lo=np.array([box.xmin+4000,box.ymin,box.zmin]); hi=np.array([box.xmax+4000,box.ymax,box.zmax])
        candidates=json.loads((OUT/'source_components.json').read_text(encoding='utf8'))['components']
        error,q=min((max(np.max(np.abs(lo-q['lo'])),np.max(np.abs(hi-q['hi']))),q) for q in candidates if q['node']=='K_GOVDE__on_seffaf')
        m=dict(source_component=q['id'],bbox_error_mm=float(error),bbox_unique_match=bool(error<=.01))
    row={'sheet':sheet.ad,'source_component':m['source_component'],'bbox_error_mm':m['bbox_error_mm'],
         'full_surface_equality_verified':False,'suitable_for_final_assembly':False}
    if not m['bbox_unique_match']:
        row['status']='BBOX_DIFFERS'; rows.append(row); continue
    name,num=m['source_component'].rsplit('[',1); num=int(num[:-1])
    if name not in model._bc: model.bilesen(name,no=0)
    component=model._bc[name][num]
    points=np.unique(np.concatenate([p['X'][p['T'][indices]].reshape(-1,3) for p,indices in component['parca']]),axis=0)
    # Deterministic uniform sample plus the six extrema. Curved GLB vertices
    # lie on the native CAD surface; no triangulated face-center approximation.
    ids=np.unique(np.r_[np.linspace(0,len(points)-1,min(128,len(points))).astype(int),
                        points.argmin(axis=0),points.argmax(axis=0)])
    shape=sheet.kati()
    errors=[float(shape.distance(cq.Vertex.makeVertex(*(points[i]-[4000,0,0])))) for i in ids]
    row.update(sample_count=len(ids),source_vertex_count=len(points),max_sample_distance_mm=max(errors),
               worst_point_world_mm=points[ids[int(np.argmax(errors))]].tolist(),
               status='SAMPLED_VERTICES_MATCH' if max(errors)<=.01 else 'SURFACE_DIFFERS')
    rows.append(row)
    print(sheet.ad,row['status'],round(max(errors),6),flush=True)
report={'source_step':61,'method':'source mesh vertex to native CAD boundary; deterministic sample',
        'tolerance_mm':.01,'bidirectional_equality_checked':False,'publish_allowed':False,'sheets':rows}
(OUT/'sheet_surface_screen.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('MATCHED',sum(r['status']=='SAMPLED_VERTICES_MATCH' for r in rows),'/',len(rows),flush=True)
sys.stdout.flush(); os._exit(0)
