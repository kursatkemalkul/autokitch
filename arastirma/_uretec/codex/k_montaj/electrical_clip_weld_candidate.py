"""Four own cable-clip feet continuously welded to our bridge/side sheet.
Existing nominal1mm clips are cable straps, not load-bearing3mm brackets.
Supplier-body clips are deliberately excluded. Cables must be absent during
TIG, grinding and passivation. This private geometry still needs tool paths,
source activation and assembly sequencing; no connection is closed here.
"""
from lower_support import *
import pickle,gzip,hashlib,trimesh
import panel_mount_candidate as PM
H1=OUT/'k1';src=H1/'k_parca_head_verified.pkl'
P=pickle.loads(src.read_bytes())['P']
probe=json.loads((H1/'electrical_clip_mount_probe.json').read_text())
assert probe['source_parts_sha256']==hashlib.sha256(src.read_bytes()).hexdigest()
folder=OUT/'electrical_clip_weld_candidate';folder.mkdir(exist_ok=True)
parts={};joins=[];origin=np.array([4200.,1450.,-290.])
for row in probe['clips']:
 a=row['part'];hosts=row['mounting_face_candidates']
 if len(hosts)!=1 or hosts[0]['part'] not in ('kopru_kirisi_-286','sag_sac_E_penceresi'):continue
 host=hosts[0]['part'];face=hosts[0]['faces'][0]
 axis='xyz'.index(face['axis']);v=np.asarray(P[a]['V'])
 q=v[abs(v[:,axis]-face['plane_mm'])<.001]
 lo=q.min(0);hi=q.max(0);other=[k for k in range(3) if k!=axis]
 n=np.zeros(3);n[axis]=1 if face['side']=='lo' else -1
 # Four separate permanent seam solids, including the end closure.
 for edge,(ac,fixed,sign) in enumerate([(other[0],other[1],-1),(other[0],other[1],1),(other[1],other[0],-1),(other[1],other[0],1)]):
  p0=lo.copy();p1=lo.copy()
  p0[fixed]=p1[fixed]=lo[fixed] if sign<0 else hi[fixed]
  p1[ac]=hi[ac]
  normal=np.zeros(3);normal[fixed]=sign
  name='k79_'+a+'_TIG_'+str(edge)
  seam=S.kaynak_dikisi(tuple(p0),tuple(p1),tuple(normal),tuple(n),.7,ad=name,birim='K_ELEKTRIK',not_='Continuous TIG141 ER308LSi; cables absent, grind and passivate')
  vv,ff=PM.mesh(seam['sh']);solid=PM.solid(vv,ff,origin)
  assert str(solid.status())=='Error.NoError' and solid.volume()>0
  contacts={}
  for carrier in (a,host):
   target=trimesh.Trimesh(P[carrier]['V'],P[carrier]['F'],process=False)
   _,d,_=trimesh.proximity.closest_point(target,vv)
   contacts[carrier]=float(d.min())
  assert all(d<.001 for d in contacts.values()),contacts
  parts[name]=dict(V=vv.tolist(),F=ff.tolist(),tur='kaynak',description='Continuous weld of own cable strap foot, not a supplier body',
    carriers=[a,host],contact_min_mm=contacts,seam_length_mm=float(np.linalg.norm(p1-p0)),leg_mm=.7)
 joins.append(dict(clip=a,host=host,seams=['k79_'+a+'_TIG_'+str(e) for e in range(4)],
  method='Continuous foot-perimeter TIG141 ER308LSi; grind and passivate',
  prerequisites=['Install clip on bare bridge/side sheet before any cable','Hold foot with clamp until all four seams complete'],
  source_role_candidates=row['native_bbox_candidates'],source_geometry_contact_verified=True,torch_path_verified=False,connection_closed=False))
assert len(joins)==4 and len(parts)==16
payload=dict(source_parts_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),parts=parts,joins=joins,
 supplier_body_modified=False,shared_chain_registered=False,production_release=False)
(folder/'geometry.json.gz').write_bytes(gzip.compress(json.dumps(payload,separators=(',',':')).encode(),mtime=0))
(folder/'audit.json').write_text(json.dumps({k:v for k,v in payload.items() if k!='parts'},indent=2),encoding='utf-8')
print('CLIP_WELD_CANDIDATE',len(joins),'CLIPS',len(parts),'REAL_SEAMS; TORCH_AND_ORDER_PENDING',flush=True)
sys.stdout.flush();os._exit(0)
