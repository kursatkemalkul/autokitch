"""Actual bottom fixing insertion and Allen access,2mm path samples.
Uses current verified surrounding geometry; no source activation/release.
"""
import belt_bottom_mount_candidate as B
from belt_bottom_mount_candidate import *
import time
DEST=B.DEST;records=json.loads(gzip.decompress((DEST/'geometry.json.gz').read_bytes()))['parts']
all_parts={n:p for n,p in P.items() if n not in DROP}
for n,r in records.items():all_parts[n]={'V':np.array(r['V'],float),'F':np.array(r['F'],int)}
cache={};checks=[];began=time.time()
def check_shape(sh,offset):
 v,f=PM.mesh(sh);v=v+offset;lo=v.min(0);hi=v.max(0);ss=PM.solid(v,f,ORIGIN);bad=[]
 for n,p in all_parts.items():
  sv=p['V'];sl=sv.min(0);su=sv.max(0)
  if np.any(np.minimum(hi,su)-np.maximum(lo,sl)<=.0005):continue
  if n not in cache:
   try:cache[n]=PM.solid(sv,p['F'],ORIGIN)
   except AssertionError:cache[n]=None
  if cache[n] is not None:
   vol=float((ss^cache[n]).volume())
   if vol>.02:bad.append({'part':n,'intersection_mm3':vol})
  else:
   tri=sv[p['F']];tri=tri[np.all(tri.max(1)>=lo-.01,axis=1)&np.all(tri.min(1)<=hi+.01,axis=1)]
   count=int(PM.YD.poz_kesisim(np.asarray(v[f],float),np.asarray(tri,float),.002).sum()) if len(tri) else 0
   inside=int((trimesh.proximity.signed_distance(trimesh.Trimesh(v,f,process=False),np.unique(tri.reshape(-1,3),axis=0))>.01).sum()) if len(tri) else 0
   if count or inside:bad.append({'part':n,'crossing_triangles':count,'vertices_inside':inside})
 return bad
parts,joins=B.build();by={p['ad']:p['sh'] for p in parts}
for j in joins:
 x,z=map(float,j['id'].split('_'))
 body=cylinder(x,821.35,z,5.,60.)
 tip=S._tasi(S._altigen(4.9,3.),S._cerceve((x,881.35,z),(0,1,0)))
 tool=body.fuse(tip)
 tool_paths=[]
 for sign in (-1,1):
  offsets=[np.array([sign*float(d),-4.,0]) for d in np.linspace(100,0,51)]
  offsets += [np.array([0.,float(d),0.]) for d in (-2.,0.)]
  failures=[]
  for i,o in enumerate(offsets):
   bad=check_shape(tool,o)
   if bad:failures.append({'sample':i,'offset_mm':o.tolist(),'collisions':bad});break
  tool_paths.append({'side_sign':sign,'sample_count':len(offsets),'step_mm':2.,'failures':failures,'passed':not failures})
  if not failures:break
 # Moving screw/washer must not collide with its own final source instance.
 insertion=[]
 held={name:all_parts.pop(name) for name in (j['washer'],j['screw'])}
 for name in (j['washer'],j['screw']):
  fixed=held[name]
  failures=[]
  for d in np.linspace(-20,0,11):
   bad=check_shape(by[name],np.array([0.,d,0.]))
   if bad:failures.append({'offset_y_mm':float(d),'collisions':bad});break
  all_parts[name]=fixed
  insertion.append({'part':name,'sample_count':11,'step_mm':2.,'failures':failures,'passed':not failures})
 row={'id':j['id'],'tool_AF_mm':4.9,'actual_socket_AF_nominal_mm':5.,'tool_body_diameter_mm':10.,'required_AF_plus_5_mm':10.,
      'tool_body_length_mm':60.,'tool_paths':tool_paths,'fixing_paths':insertion,
      'passed':any(p['passed'] for p in tool_paths) and all(p['passed'] for p in insertion)}
 checks.append(row);print('BOTTOM_ACCESS',j['id'],'passed',row['passed'],flush=True)
report={'source_parts_sha256':hashlib.sha256((K1/'k_parca_belt_verified.pkl').read_bytes()).hexdigest(),
        'candidate_geometry_sha256':hashlib.sha256((DEST/'geometry.json.gz').read_bytes()).hexdigest(),
        'checks':checks,'passed_access_and_insertion_only':all(r['passed'] for r in checks),'production_release':False,
        'torch_access_verified':False,'elapsed_seconds':time.time()-began}
(DEST/'access_audit.json').write_text(json.dumps(clean(report),indent=2),encoding='utf-8')
sys.stdout.flush();os._exit(0 if report['passed_access_and_insertion_only'] else 2)
