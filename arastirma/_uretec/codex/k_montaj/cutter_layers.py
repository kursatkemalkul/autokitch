"""Manufacturing proposal for K cutter plate packs; does not modify chain/model.

Original exterior preserved as manifold union. Flush TIG edge weld specification
requires physical access and process verification before animation release.
"""
import sys,json
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[4];Y=ROOT/'arastirma/_uretec/h3/yama_v9'
for p in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(p))
from m8kit import Glb
import sac_ent as SE
import manifold3d as mf
O=ROOT/'_local/codex_k_montaj'
g=Glb(str(O/'k73a.glb'));node='K_KESICI__sac__KESICI';g.bilesen(node,0)
rows=[];meshes=[]
for b in g._bc[node]:
    if b['no'] not in (*range(7),8):continue
    P=np.concatenate([p['X'][p['T'][i]] for p,i in b['parca']]);solid=SE.mf_ucgen(P)
    assert solid is not None,(b['no'],'open source')
    low,high=float(b['lo'][1]),float(b['hi'][1]);thickness=high-low
    family=[4.,4.] if b['no']<7 else [4.,6.]
    assert abs(sum(family)-thickness)<.001,(b['no'],thickness)
    # Intersect actual source, including all holes. No idealised bounding-box plate.
    cut=low+family[0]
    box=mf.Manifold.cube((1000.,cut-low+100.,1000.)).translate((3700.,low-100.,-700.))
    bottom=solid^box;top=solid-bottom
    assert not bottom.is_empty() and not top.is_empty()
    union=bottom+top
    missing=(solid-union).volume();extra=(union-solid).volume()
    assert missing<.001 and extra<.001,(missing,extra)
    name='kesici_kafa' if b['no']==0 else 'kesici_adapter' if b['no']==8 else f'kesici_koruyucu_kol_{b["no"]}'
    for i,s in enumerate((bottom,top)):
        mesh=s.to_mesh(); V=np.asarray(mesh.vert_properties)[:,:3];F=np.asarray(mesh.tri_verts)
        meshes.append({'name':f'{name}_katman_{i+1}','vertices':V.tolist(),'triangles':F.tolist(),'stock_mm':family[i]})
    rows.append({'part':name,'source_component':b['no'],'stock_mm':family,'interface_y_mm':cut,
                 'union_missing_mm3':missing,'union_extra_mm3':extra,
                 'method':'Laser both matching contours and holes; clamp; continuous TIG perimeter seam; grind flush; passivate.',
                 'load_allowed_before_weld':False,'weld_access_checked':False,
                 'stock_contour_hole_dfm_checked':False})
report={'units':'mm','source':'k73a.glb','proposal_only':True,'parts':rows,'meshes':meshes,
        'publish_allowed':False,'model_modified':False}
(O/'cutter_layers.json').write_text(json.dumps(report,separators=(',',':')),encoding='utf8')
print(json.dumps({'plate_packs':len(rows),'layers':len(meshes),'union_verified':True,'manufacturing_release':False}),flush=True)
