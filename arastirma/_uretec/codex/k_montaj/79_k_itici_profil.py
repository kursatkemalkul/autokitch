"""Local stage79: four rounded20x20x2 pusher posts and their real welds.

Only K-owned posts/seams change. Envelopes, mounting holes, mechanism axes
and heights remain fixed. This prototype is not registered or released.
"""
from lower_support import *
import importlib.util,pickle,hashlib,gzip
import manifold3d as m3
Y=H/'yama_v9'
for path in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
import sac_ent as SE
K1=OUT/'k1'
spec=importlib.util.spec_from_file_location('k_topology_writer',Path(__file__).with_name('78_k_sac_topolojisi.py'))
writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)

def build_recipe(source,target):
 P=pickle.load((K1/'k_parca.pkl').open('rb'))['P']
 current=json.loads((K1/'current_source_manifest.json').read_text(encoding='utf-8'))
 assert hashlib.sha256(source.read_bytes()).hexdigest()==current['source_model_sha256']
 parts=[];postproof={}
 for i,(x,z) in enumerate(( (4040.,-755.),(4040.,-645.),(4360.,-755.),(4360.,-645.) )):
  name=f'k_itici_sac_{i}';old=P[name]['V'];lo=old.min(0);hi=old.max(0)
  assert np.max(abs(lo-[x-10,900,z-10]))<.001 and np.max(abs(hi-[x+10,958,z+10]))<.001
  profile=K.Profil(name,'y',900,958,(x,z),b=20,t=2,Ro=4)
  p=profile.parca();parts.append(p)
  postproof[name]={'outer_radius_mm':4.,'inner_radius_mm':2.,'wall_mm':2.,'envelope_mm':[[x-10,900,z-10],[x+10,958,z+10]],'original_outer_radius_mm':0.,'stock_profile_rule':'Ro=2t','stock_family':'20x20x2 AISI304 hollow profile','load_capacity_not_yet_checked':True}
  for e in range(4):
   a=[(x-6,900,z-10),(x+10,900,z-6),(x+6,900,z+10),(x-10,900,z+6)][e]
   b=[(x+6,900,z-10),(x+10,900,z+6),(x-6,900,z+10),(x-10,900,z-6)][e]
   n=[(0,0,-1),(1,0,0),(0,0,1),(-1,0,0)][e]
   name=f'k72_itici_ayak_kaynagi_{x}_{z}_{e}'
   parts.append(S.kaynak_dikisi(a,b,n,(0,1,0),1.,ad=name,birim='K_ITICI',not_='TIG141 ER308LSi; rounded profile flat landing12mm'))
 repairs={}
 for p in parts:
  name=p['ad'];q=np.asarray(SE.ucgen(p['sh']),dtype=np.float64).reshape(-1,3,3)
  v,f=np.unique(q.reshape(-1,3),axis=0,return_inverse=True);f=f.reshape(-1,3)
  solid=m3.Manifold(m3.Mesh(vert_properties=np.asarray(v,dtype=np.float32),tri_verts=np.asarray(f,dtype=np.uint32)))
  assert str(solid.status())=='Error.NoError' and solid.volume()>0,(name,solid.status(),solid.volume())
  proof={'part':name,'closed_status':str(solid.status()),'volume_mm3':solid.volume(),'maximum_declared_precision_adjustment_mm':0.,'purpose':'rounded stock post' if name in postproof else 'weld only along actual12mm flat landing','supplier_component':False}
  if name in postproof:proof.update(postproof[name])
  repairs[name]={'original_triangles':P[name]['V'][P[name]['F']].tolist(),'vertices':v.tolist(),'triangles':f.tolist(),'proof':proof}
 assert len(repairs)==20
 recipe={'source_model_sha256':current['source_model_sha256'],'source_encoding_sha256':hashlib.sha256((K1/'current_sheet_bending.json').read_bytes()).hexdigest(),'repairs':repairs}
 target.write_bytes(gzip.compress(json.dumps(recipe,separators=(',',':'),allow_nan=False).encode('utf-8'),mtime=0))
 print('PROFILE79_RECIPE',len(repairs),target.stat().st_size,flush=True)
 return set(repairs)

if __name__=='__main__':
 source,dest,payload=map(Path,sys.argv[1:4])
 if payload.exists() and '--rebuild-recipe' not in sys.argv[4:]:
  # The tracked JSON recipe must remain reproducible after local caches
  # advance. Its input hash is verified by the shared writer below.
  recipe=json.loads(gzip.decompress(payload.read_bytes()))
  expected={f'k_itici_sac_{i}' for i in range(4)}
  expected.update(f'k72_itici_ayak_kaynagi_{x}_{z}_{e}' for x in (4040.,4360.) for z in (-755.,-645.) for e in range(4))
  assert set(recipe['repairs'])==expected
 else:expected=build_recipe(source,payload)
 writer.apply(source,dest,payload,expected_names=expected,step=79,source_nodes=('K_ITICI__sac',))
 sys.stdout.flush();os._exit(0)
