"""Close four conveyor support tops and join the side plates to them.

Own fabrication only. Keep the belt seat at932.5mm, feet at895mm and
all original mounting axes. Profiles shorten2mm for sealed2mm caps.
No supplier roller, mechanism or other station is changed.
"""
import panel_mount_candidate as PM
from lower_support import *
import pickle,hashlib,gzip,itertools,math
import trimesh
import manifold3d as mf
K1=OUT/'k1';DEST=OUT/'belt_support_candidate';DEST.mkdir(exist_ok=True)
P=pickle.load((K1/'k_parca.pkl').open('rb'))['P']
ORIGIN=np.array([4200.,920.,-220.])
NAMES={(4065.,-421.):'k72_bant_ayagi_4065.0_-421.0',(4335.,-421.):'k72_bant_ayagi_4335.0_-421.0',(4065.,-3.):'bant_ayagi_65_-3',(4335.,-3.):'bant_ayagi_335_-3'}
WELD_TEMPLATE='k72_bant_ayak_kaynagi_4065.0_-421.0_0'

def rounded_cap_and_weld(x,z):
 face=S.yuz_dikd_r(0,0,20,20,0,4)
 transform=S._M(np.column_stack(((1,0,0),(0,0,-1),(0,1,0))),(x,930.5,z))
 cap=S._tasi(S._prizma(face,2),transform)
 wire=face.outerWire();edge=wire.Edges()[0]
 p=np.array(edge.startPoint().toTuple());t=np.array(edge.tangentAt(0).toTuple())
 n=np.array([t[1],-t[0],0.]);n/=np.linalg.norm(n)
 if n@p<0:n=-n
 #1.4mm equal legs give a0.99mm effective throat. Exact continuous
 # rounded path seals the profile; four straight-only beads would not.
 section=cq.Wire.makePolygon([cq.Vector(*p),cq.Vector(*(p+n*1.4)),cq.Vector(*(p+[0,0,1.4]))],close=True)
 weld=S._tasi(cq.Solid.sweep(section,[],wire,makeSolid=True,isFrenet=True),transform)
 return cap,weld,float(wire.Length())

def build():
 parts=[];joins=[];descriptions={}
 for (x,z),name in NAMES.items():
  v=P[name]['V'];assert np.max(abs(v.min(0)-[x-10,895,z-10]))<.001 and np.max(abs(v.max(0)-[x+10,932.5,z+10]))<.001
  post=K.Profil(name,'y',895,930.5,(x,z),b=20,t=2,Ro=4).parca();parts.append(post)
  cap,weld,length=rounded_cap_and_weld(x,z);tag=f'{int(x)}_{int(z)}'
  capname='k79_bant_ust_tapa_'+tag;weldname='k79_bant_tapa_cevre_kaynagi_'+tag
  cp=S._bp(capname,cap,'laser AISI3042mm','Rounded sealed conveyor foot cap','20x20x2 R4',malzeme='AISI304',birim='K_BANT',uretim=True,mal='sac');cp['tur']='sac';parts.append(cp)
  wp=S._bp(weldname,weld,'TIG141 ER308LSi','Continuous rounded cap seam','leg1.4 effective throat0.99',malzeme='ER308LSi',birim='K_BANT',uretim=True,mal='paslanmaz');wp['tur']='kaynak';parts.append(wp)
  host='bant_yan_-421' if z==-421 else 'bant_yan_-3'
  seamnames=[]
  for sign in (-1,1):
   nm=f'k79_bant_ust_kaynagi_{tag}_{sign}'
   s=S.kaynak_dikisi((x-10,932.5,z+sign*3),(x+10,932.5,z+sign*3),(0,0,sign),(0,1,0),1.4,ad=nm,birim='K_BANT',not_='TIG141 ER308LSi; effective throat0.99mm; side plate to sealed cap')
   parts.append(s);seamnames.append(nm)
  joins.append({'id':tag,'post':name,'cap':capname,'plate':host,'cap_weld':weldname,'plate_welds':seamnames,'bottom_y_mm':895.,'post_top_y_mm':930.5,'cap_top_and_belt_seat_y_mm':932.5,'cap_t_mm':2.,'stock_profile':'20x20x2 R4/R2','continuous_cap_weld_length_mm':length,'weld_leg_mm':1.4,'effective_throat_mm':1.4/math.sqrt(2),'supplier_parts_modified':False,'manufacturing_order':'Post/cap bench-weld first; mount and tighten foot to shelf; lower belt frame on caps, weld plate/cap before rollers and belt are installed','torch_path_and_load_release':False})
  for p in (post,cp,wp):descriptions[p['ad']]=p.get('bom')
 return parts,joins

def audit(parts,joins):
 records={}
 for p in parts:
  v,f=PM.mesh(p['sh']);records[p['ad']]={'V':v,'F':f,'tur':p.get('tur','profil'),'description':p.get('bom')}
 # Only reuse a source weld's render labels. This untouched mesh is bound
 # explicitly, so the generic writer has a genuine matching weld template.
 records[WELD_TEMPLATE]={'V':P[WELD_TEMPLATE]['V'],'F':P[WELD_TEMPLATE]['F'],'tur':'kaynak','description':P[WELD_TEMPLATE]['ac']}
 solids={a:PM.solid(r['V'],r['F'],ORIGIN) for a,r in records.items()}
 clashes=[];surface_checks=[];source_solids={}
 for a,r in records.items():
  if a==WELD_TEMPLATE:continue
  lo=r['V'].min(0);hi=r['V'].max(0)
  for b,p in P.items():
   if b in records:continue
   v=p['V'];blo=v.min(0);bhi=v.max(0)
   if np.any(np.minimum(hi,bhi)-np.maximum(lo,blo)<=.0005):continue
   try:
    if b not in source_solids:source_solids[b]=PM.solid(v,p['F'],ORIGIN)
    volume=float((solids[a]^source_solids[b]).volume())
    if volume>.02:clashes.append({'candidate':a,'source':b,'intersection_mm3':volume})
   except AssertionError:
    tri=v[p['F']];crop=np.all(tri.max(1)>=lo-.01,axis=1)&np.all(tri.min(1)<=hi+.01,axis=1);tri=tri[crop]
    count=int(PM.YD.poz_kesisim(np.asarray(r['V'][r['F']],float),np.asarray(tri,float),.002).sum()) if len(tri) else 0
    mesh=trimesh.Trimesh(r['V'],r['F'],process=False)
    inside=int((trimesh.proximity.signed_distance(mesh,np.unique(tri.reshape(-1,3),axis=0))>.01).sum()) if len(tri) else 0
    check={'candidate':a,'source':b,'crossing_triangles':count,'vertices_inside':inside,'passed':not count and not inside};surface_checks.append(check)
    if not check['passed']:clashes.append(check)
 for a,b in itertools.combinations(records,2):
  volume=float((solids[a]^solids[b]).volume())
  if volume>.02:clashes.append({'candidate':a,'candidate_other':b,'intersection_mm3':volume})
 contacts=[]
 for j in joins:
  # Measure actual material within0.05mm of each mating plane, not bbox
  # adjacency alone. Top plate covers a20x6mm strip of the2mm cap.
  x,z=next(c for c,n in NAMES.items() if n==j['post'])
  cap=solids[j['cap']];post=solids[j['post']]
  plate=PM.solid(P[j['plate']]['V'],P[j['plate']]['F'],ORIGIN)
  band=mf.Manifold.cube([20,.1,8]).translate((x-10-ORIGIN[0],932.45-ORIGIN[1],z-4-ORIGIN[2]))
  cap_slice=float((cap^band).volume());plate_slice=float((plate^band).volume())
  row={'id':j['id'],'cap_top_slice_mm3':cap_slice,'plate_bottom_slice_mm3':plate_slice,'cap_expected_slice_mm3':8.,'plate_expected_slice_mm3':6.,'seat_gap_mm':abs(float(records[j['cap']]['V'][:,1].max()-P[j['plate']]['V'][:,1].min())),'cap_closed_solid':str(cap.status()),'post_closed_solid':str(post.status()),'passed':abs(cap_slice-8)<.03 and abs(plate_slice-6)<.03 and abs(records[j['cap']]['V'][:,1].max()-932.5)<.001}
  contacts.append(row)
 source=json.loads((K1/'current_source_manifest.json').read_text(encoding='utf-8'))
 report={'source_model_sha256':source['source_model_sha256'],'source_parts_sha256':hashlib.sha256((K1/'k_parca.pkl').read_bytes()).hexdigest(),'changed_parts':list(NAMES.values()),'unchanged_render_template':WELD_TEMPLATE,'added_parts':[a for a in records if a not in P],'joints':joins,'contacts':contacts,'clashes':clashes,'open_mesh_surface_checks':surface_checks,'passed':not clashes and all(r['passed'] for r in contacts),'production_release':False}
 payload={'source_model_sha256':report['source_model_sha256'],'source_parts_sha256':report['source_parts_sha256'],'replacement_parts':{a:{'V':r['V'].tolist(),'F':r['F'].tolist(),'tur':r['tur'],'description':r['description']} for a,r in records.items()},'original_triangles':{a:P[a]['V'][P[a]['F']].tolist() for a in records if a in P},'added_parts':report['added_parts']}
 (DEST/'geometry.json.gz').write_bytes(gzip.compress(json.dumps(clean(payload),separators=(',',':'),allow_nan=False).encode(),mtime=0))
 (DEST/'audit.json').write_text(json.dumps(clean(report),indent=2),encoding='utf-8')
 S.glb_yaz(str(DEST/'belt_support.glb'),parts)
 print('BELT_SUPPORT',len(records),'contacts',len(contacts),'clashes',len(clashes),'passed',report['passed'],flush=True)
 if not report['passed']:print(json.dumps(clashes[:8]),flush=True);raise SystemExit(2)
 return report

if __name__=='__main__':
 parts,joins=build();audit(parts,joins);sys.stdout.flush();os._exit(0)
