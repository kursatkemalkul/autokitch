"""Actual candidate contacts and tools at explicitly stated assembly stages."""
import panel_mount_candidate as PM
from lower_support import *
import pickle, hashlib, trimesh
H=OUT/'k1'; folder=OUT/(sys.argv[1] if len(sys.argv)>1 else 'cut_head_weld_candidate')
source=H/'k_parca_catalog_verified.pkl'
P=pickle.loads(source.read_bytes())['P']
payload=json.loads(gzip.decompress((folder/'geometry.json.gz').read_bytes()))
assert payload['source_parts_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
changed=payload['parts']
for name,r in changed.items():
    P[name]={'V':np.asarray(r['V'],float),'F':np.asarray(r['F'],np.int32)}
recipe=json.loads((folder/'audit.json').read_text())
origin=np.array([4200.,1200.,-206.]);cache={};checks=[]
for j in recipe['joins']:
    x,y,z=j['center_mm']
    # M8 DIN7991 uses5mm hex. 10mm envelope includes the required +5mm.
    shape=cylinder(x,y-80.,z,5.,79.95)
    v,f=PM.mesh(shape);tool=PM.solid(v,f,origin);lo=v.min(0);hi=v.max(0);issues=[]
    deferred = []
    if j['id'].startswith('yoke_'):
        # Top bolts must be tightened before the lower knife cassette
        # obstructs their axial drives. These are explicit assembly order
        # constraints, not permanent collision exceptions.
        deferred = [name for name in P if name in ('kafa_plakasi_8','k79_kafa_ust_plaka_2','bicak_gobek_halkasi','bicak_koruma_halkasi')
                    or name.startswith(('bicak_','koruma_braketi_','kelebek_somun_','k79_kafa_alt_M8x20_'))]
    for name,r in P.items():
        if name in deferred:continue
        if name==j['screw']:continue
        w=r['V']
        if np.any(np.minimum(hi,w.max(0))-np.maximum(lo,w.min(0))<=.001):continue
        try:
            if name not in cache:cache[name]=PM.solid(w,r['F'],origin)
            vol=float((tool^cache[name]).volume())
            if vol>.02:issues.append({'part':name,'volume_mm3':vol})
        except AssertionError:
            t=w[r['F']];t=t[np.all(t.max(1)>=lo-.01,axis=1)&np.all(t.min(1)<=hi+.01,axis=1)]
            n=int(PM.YD.poz_kesisim(np.asarray(v[f],float),np.asarray(t,float),.002).sum()) if len(t) else 0
            if n:issues.append({'part':name,'surface_crossing_pairs':n})
    checks.append({'joint':j['id'],'hex_mm':5.,'tool_clearance_envelope_diameter_mm':10.,
                   'axial_approach_mm':80.,'issues':issues,'passed':not issues,
                   'must_be_installed_after_torquing_this_joint':deferred})

contacts=[]
for item in recipe['continuous_rod_welds']:
    weld=P[item['weld']]
    for other in (item['rod'],item['adaptor']):
        r=P[other]
        mesh=trimesh.Trimesh(vertices=r['V'],faces=r['F'],process=False)
        _,dist,_=trimesh.proximity.closest_point(mesh,weld['V'])
        # Verify source vertices along each entire weld interface, not bbox touching.
        close=weld['V'][dist<.01]
        contact_extent=np.ptp(close[:,[0,2]],axis=0) if len(close) else np.zeros(2)
        contacts.append({'weld':item['weld'],'touches':other,'source_surface_vertices':int(len(close)),
                         'xz_contact_extent_mm':contact_extent.tolist(),
                         'passed':len(close)>=12 and bool(np.all(contact_extent>15.))})
report={'source_model_sha256':recipe['source_model_sha256'],'source_parts_sha256':payload['source_parts_sha256'],
        'candidate_geometry_sha256':hashlib.sha256((folder/'geometry.json.gz').read_bytes()).hexdigest(),
        'bottom_tool_checks':checks,'weld_contacts':contacts,
        'passed_bottom_tool_access':all(x['passed'] for x in checks),
        'passed_continuous_weld_contacts':all(x['passed'] for x in contacts),
        'supplier_yoke_mount_verified':False,'adaptor_layer_retention_verified':False,
        'stage_exclusions_are_order_constraints_not_permanent_exceptions':True,
        'manufacturing_release':False,'production_release':False}
(folder/'access_audit.json').write_text(json.dumps(clean(report),indent=2),encoding='utf-8')
print('HEAD_ACCESS',report['passed_bottom_tool_access'],'WELD_CONTACTS',report['passed_continuous_weld_contacts'],
      [c for c in checks if not c['passed']],flush=True)
sys.stdout.flush();os._exit(0 if report['passed_bottom_tool_access'] and report['passed_continuous_weld_contacts'] else 2)
