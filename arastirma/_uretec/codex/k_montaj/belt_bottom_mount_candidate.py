"""Bottom-access conveyor fixing prototype; exact own parts, not source activation.

6mm tapped insert inside each support, installed and welded before its top
cap closes. Shelf PEM and old top-insert hardware are superseded explicitly.
"""
import panel_mount_candidate as PM
from lower_support import *
import pickle,hashlib,gzip,itertools,math
import trimesh
import manifold3d as mf
K1=OUT/'k1';DEST=OUT/'belt_bottom_mount_candidate';DEST.mkdir(exist_ok=True)
P=pickle.load((K1/'k_parca_belt_verified.pkl').open('rb'))['P']
ORIGIN=np.array([4200.,920.,-220.])
META=json.loads((OUT/'belt_support_candidate/audit.json').read_text(encoding='utf-8'))
OLD=json.loads((OUT/'k72_mounts.json').read_text(encoding='utf-8'))
DROP=[]
for j in OLD['connections']:
 if j['id'].startswith('M6_'):
  DROP += j['parts']+['k71_raf_PEM_'+j['id']]
assert len(DROP)==20 and all(n in P for n in DROP)

def build():
 parts=[];joins=[]
 # Two pre-existing front flange records contain non-manifold overlapping
 # surfaces. Rebuild only our3mm stock, same32x32 envelope and M6 axis.
 for x in (4065.,4335.):
  z=-3.;name=f'k72_bant_ayak_flansi_{x}_{z}'
  old=P[name]['V'];assert np.allclose(old.min(0),[x-16,892,z-16],atol=.001) and np.allclose(old.max(0),[x+16,895,z+16],atol=.001)
  sh=K.kutu(x-16,x+16,892,895,z-16,z+16).cut(cylinder(x,891,z,3.3,5))
  part=S._bp(name,sh,'laser AISI3043mm','Single closed conveyor foot flange; remove old overlapping source surfaces','32x32x3; M6 clearance6.6; original axes',malzeme='AISI304',birim='K_BANT',uretim=True,mal='sac');part['tur']='sac';parts.append(part)
 for j in META['joints']:
  x,z=map(float,j['id'].split('_'));tag=j['id']
  # Fits the actual16x16 R2 hollow interior,6mm family stock.
  face=S.yuz_dikd_r(0,0,16,16,0,2)
  mat=S._M(np.column_stack(((1,0,0),(0,0,-1),(0,1,0))),(x,895.5,z))
  insert=S._tasi(S._prizma(face,6),mat).cut(cylinder(x,895,z,3,7))
  nm='k79_bant_disli_plaka_'+tag
  part=S._bp(nm,insert,'AISI3046mm laser + tap M6','Tapped conveyor support insert','16x16x6 R2; M6 through',malzeme='AISI304',birim='K_BANT',uretim=True,mal='sac');part['tur']='sac';parts.append(part)
  wire=face.outerWire();edge=wire.Edges()[0];p=np.array(edge.startPoint().toTuple());t=np.array(edge.tangentAt(0).toTuple())
  n=np.array([t[1],-t[0],0.]);n/=np.linalg.norm(n)
  if n@p<0:n=-n
  # Interior fillet lies on the insert and against the support inner wall.
  section=cq.Wire.makePolygon([cq.Vector(*(p+[0,0,6])),cq.Vector(*(p-n*1.4+[0,0,6])),cq.Vector(*(p+[0,0,7.4]))],close=True)
  # Sweep reference wire must share the section's6mm elevation.
  path=wire.translate(cq.Vector(0,0,6))
  weld=S._tasi(cq.Solid.sweep(section,[],path,makeSolid=True,isFrenet=True),mat)
  wname='k79_bant_disli_plaka_kaynagi_'+tag
  wp=S._bp(wname,weld,'TIG141 ER308LSi','Internal continuous insert/support weld','leg1.4 throat0.99',malzeme='ER308LSi',birim='K_BANT',uretim=True,mal='paslanmaz');wp['tur']='kaynak';parts.append(wp)
  # Shelf bottom889, washer1.6: head seating887.4.16mm screw tip903.4.
  screw=S.vida('ISO4762','M6',16,(x,887.4,z),(0,1,0),ad='k79_bant_M6x16_alttan_'+tag,birim='K_BANT');screw['tur']='baglanti';parts.append(screw)
  washer=S.pul('DIN9021','M6',(x,887.4,z),(0,1,0),ad='k79_bant_M6_genis_pul_'+tag,birim='K_BANT');washer['tur']='baglanti';parts.append(washer)
  joins.append({'id':tag,'post':j['post'],'side_plate':j['plate'],'insert':nm,'insert_weld':wname,'screw':screw['ad'],'washer':washer['ad'],
   'axis':[0,1,0],'screw_head_seat_y_mm':887.4,'screw_tip_y_mm':903.4,'thread_bottom_y_mm':895.5,'thread_top_y_mm':901.5,
   'engagement_mm':6.,'nominal_diameter_mm':6.,'protrusion_mm':1.9,'pitch_mm':1.,'washer_standard':'ISO7093 M6','washer_dimensions_mm':[6.4,18,1.6],
   'thread_proxy_nominal_only':True,'machining_tap_verified':False,'torch_access_verified':False,'production_release':False})
 return parts,joins

def audit(parts,joins):
 records={p['ad']:{'V':PM.mesh(p['sh'])[0],'F':PM.mesh(p['sh'])[1],'tur':p['tur'],'description':p.get('bom')} for p in parts}
 solids={n:PM.solid(r['V'],r['F'],ORIGIN) for n,r in records.items()}
 source_solids={};clashes=[];surfaces=[]
 for a,r in records.items():
  lo=r['V'].min(0);hi=r['V'].max(0)
  for b,p in P.items():
   if b in DROP or b in records:continue
   v=p['V'];blo=v.min(0);bhi=v.max(0)
   if np.any(np.minimum(hi,bhi)-np.maximum(lo,blo)<=.0005):continue
   try:
    if b not in source_solids:source_solids[b]=PM.solid(v,p['F'],ORIGIN)
    vol=float((solids[a]^source_solids[b]).volume())
    if vol>.02:clashes.append({'candidate':a,'source':b,'intersection_mm3':vol})
   except AssertionError:
    tri=v[p['F']];tri=tri[np.all(tri.max(1)>=lo-.01,axis=1)&np.all(tri.min(1)<=hi+.01,axis=1)]
    count=int(PM.YD.poz_kesisim(np.asarray(r['V'][r['F']],float),np.asarray(tri,float),.002).sum()) if len(tri) else 0
    inside=int((trimesh.proximity.signed_distance(trimesh.Trimesh(r['V'],r['F'],process=False),np.unique(tri.reshape(-1,3),axis=0))>.01).sum()) if len(tri) else 0
    row={'candidate':a,'source':b,'crossing_triangles':count,'vertices_inside':inside,'passed':not count and not inside};surfaces.append(row)
    if not row['passed']:clashes.append(row)
 for a,b in itertools.combinations(records,2):
  vol=float((solids[a]^solids[b]).volume())
  if vol>.02:clashes.append({'candidate':a,'candidate_other':b,'intersection_mm3':vol})
 checks=[]
 for j in joins:
  r=records[j['screw']];insert=records[j['insert']];washer=records[j['washer']]
  tip=float(r['V'][:,1].max());plate_lo=float(insert['V'][:,1].min());plate_hi=float(insert['V'][:,1].max())
  engagement=min(tip,plate_hi)-plate_lo;protrusion=tip-plate_hi
  wlo=float(washer['V'][:,1].min());whi=float(washer['V'][:,1].max())
  checks.append({'id':j['id'],'actual_engagement_mm':engagement,'actual_protrusion_mm':protrusion,'washer_bottom_mm':wlo,'washer_top_mm':whi,
   'passed':abs(engagement-6)<.001 and 1<=protrusion<=3 and abs(whi-889)<.001 and abs(wlo-887.4)<.001})
 report={'source_parts_sha256':hashlib.sha256((K1/'k_parca_belt_verified.pkl').read_bytes()).hexdigest(),'superseded_parts':DROP,'joints':joins,'repaired_front_flange_names':[a for a in records if a in P],
         'geometry_checks':checks,'clashes':clashes,'open_mesh_surface_checks':surfaces,'passed_geometry_only':not clashes and all(r['passed'] for r in checks),'tool_access_verified':False,'full_montage_verified':False,'production_release':False}
 (DEST/'audit.json').write_text(json.dumps(clean(report),indent=2),encoding='utf-8')
 payload={'source_parts_sha256':report['source_parts_sha256'],'superseded_parts':DROP,'original_repaired_triangles':{a:P[a]['V'][P[a]['F']].tolist() for a in records if a in P},'parts':{n:{'V':r['V'].tolist(),'F':r['F'].tolist(),'tur':r['tur'],'description':r['description']} for n,r in records.items()}}
 (DEST/'geometry.json.gz').write_bytes(gzip.compress(json.dumps(clean(payload),separators=(',',':')).encode(),mtime=0))
 S.glb_yaz(str(DEST/'bottom_mount.glb'),parts)
 print('BOTTOM_MOUNTS',len(parts),'clashes',len(clashes),'geometry_passed',report['passed_geometry_only'],flush=True)
 if clashes:print(json.dumps(clashes[:8]),flush=True)
 return report
if __name__=='__main__':
 parts,joins=build();r=audit(parts,joins);sys.stdout.flush();os._exit(0 if r['passed_geometry_only'] else 2)
