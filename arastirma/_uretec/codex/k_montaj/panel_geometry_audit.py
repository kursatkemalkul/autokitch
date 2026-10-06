"""Check scope, A/B equality and one-to-one source labels after panel patch."""
from pathlib import Path
source=Path(__file__).with_name('audit79_geometry.py')
code=source.read_text(encoding='utf-8').split("source=root/'A/hat3_v10s.glb'")[0]
# Reuse the established inventory routines without running the old audit.
namespace=dict(__file__=str(source),__name__='panel_audit_helpers')
exec(compile(code,str(source),'exec'),namespace)
inventory=namespace['inventory'];sha=namespace['sha'];OUT=namespace['OUT']
import json,hashlib,pickle,numpy as np

folder=OUT/'panel_mount_candidate';k1=OUT/'k1'
old=OUT/'chain73/A/hat3_v10t.glb';a=folder/'A/hat3_v10u.glb';b=folder/'B/hat3_v10u.glb'
candidate=json.loads((folder/'audit.json').read_text())
rebind=json.loads((k1/'panel_ownership_rebind_audit.json').read_text())
assert candidate['passed'] and candidate['source_model_sha256']==sha(old)
assert sha(a)==sha(b)
assert rebind['passed'] and rebind['previous_parts_sha256']==sha(k1/'k_parca.pkl')
assert rebind['raw_parts_sha256']==sha(k1/'k_parca_panel_raw.pkl')
assert rebind['repair_payload_sha256']==sha(folder/'geometry.json.gz')
before=inventory(old);after=inventory(a)
allowed={'K_ELEKTRIK__sac','K_ELEKTRIK__celik','K_GOVDE__kabuk'}
changed=[n for n in set(before)|set(after) if before.get(n)!=after.get(n)]
outside=sorted(set(changed)-allowed)
P=pickle.load((k1/'k_parca_panel_verified.pkl').open('rb'))['P'];rows=[]
for j in candidate['joints']:
    centre=np.asarray(j['centre_mm']);axis=np.asarray(j['axis'],float)
    male=P[j['parts'][0]]['V'];nut=P[j['parts'][-1]]['V']
    mi=(male-centre)@axis;fi=(nut-centre)@axis
    engagement=min(mi.max(),fi.max())-max(mi.min(),fi.min());protrusion=mi.max()-fi.max()
    holes=[]
    for name in ('pano_plakasi','arka_sac',j['parts'][1]):
        vv=P[name]['V']-centre;axial=vv@axis;radial=np.linalg.norm(vv-np.outer(axial,axis),axis=1)
        selected=np.flatnonzero(abs(radial-2.75)<.01)
        holes.append({'part':name,'bore_vertices':len(selected),'passed':len(selected)>=12})
    rows.append({'id':j['id'],'measured_engagement_mm':float(engagement),'measured_protrusion_mm':float(protrusion),
                 'host_holes':holes,'passed':bool(engagement>=4.99 and .79<=protrusion<=2.41 and all(h['passed'] for h in holes))})
report={'scope':'Four panel mount joints, exact panel/rear/spacer replacements and12 added fasteners only',
        'input_sha256':sha(old),'output_sha256':sha(a),'a_b_byte_identical':True,
        'candidate_audit_sha256':sha(folder/'audit.json'),'rebind_sha256':sha(k1/'panel_ownership_rebind_audit.json'),
        'verified_parts_sha256':sha(k1/'k_parca_panel_verified.pkl'),'parts':len(P),'triangles':sum(len(p['F']) for p in P.values()),
        'changed_nodes':sorted(changed),'changed_nodes_outside_scope':outside,
        'actual_one_to_one_triangles_matched':rebind['matched_triangles'],
        'maximum_actual_recompression_vertex_distance_mm':rebind['maximum_recompression_vertex_distance_mm'],
        'joints':rows,'passed':not outside and all(r['passed'] for r in rows),
        'source_activation':False,'manufacturing_release':False,'production_release':False,
        'remaining_checks':candidate['remaining_checks']}
(folder/'source_geometry_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PANEL_SOURCE',report['passed'],'parts',len(P),'triangles',report['triangles'],'outside',outside,flush=True)
assert report['passed']
namespace['sys'].stdout.flush();namespace['os']._exit(0)
