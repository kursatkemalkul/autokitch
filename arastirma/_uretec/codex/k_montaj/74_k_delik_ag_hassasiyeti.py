"""Local step74 prototype: preserve K CAD, refine two front-profile hole meshes.
No model dimension, purchased latch, other station, or collision exemption is changed.
"""
from lower_support import *
import pickle,hashlib,subprocess
from scipy.spatial import cKDTree
Y=H/'yama_v9'
for q in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(q))
from m8kit import Glb

def key(tri):
 q=np.round(tri,3);return q[np.lexsort((q[:,2],q[:,1],q[:,0]))].tobytes()

def apply(source,dest):
 root=Path(__file__).resolve().parents[4];cache=root/'_local/codex_k_montaj/k1'
 P=pickle.load((cache/'k_parca.pkl').open('rb'))['P'];g=Glb(str(source));factory=K.kur();rows=[];ent={}
 for name in ('kose_dikmesi_20_42','kose_dikmesi_380_42'):
  old=P[name];shape=factory.PROF[name].kati().translate((4000,0,0));bbox=shape.BoundingBox()
  lo=np.array([bbox.xmin,bbox.ymin,bbox.zmin]);hi=np.array([bbox.xmax,bbox.ymax,bbox.zmax])
  assert np.max(np.abs(lo-old['V'].min(0)))<.01 and np.max(np.abs(hi-old['V'].max(0)))<.01
  # Every original mesh vertex belongs to the unchanged CAD surface.
  cad_distances=[shape.distance(cq.Vertex.makeVertex(*v)) for v in old['V']]
  assert max(cad_distances)<.01,(name,max(cad_distances))
  original=old['V'][old['F']];tree=cKDTree(original.mean(1));removed=0;labels=set()
  for prim in g.dprims(old['dugum']):
   tris=prim['X'][prim['T']];dd,ii=tree.query(tris.mean(1));mask=np.zeros(len(tris),dtype=bool)
   for j in np.flatnonzero(dd<.0002):
    distances=np.linalg.norm(tris[j][:,None,:]-original[ii[j]][None,:,:],axis=2)
    mask[j]=bool(np.max(distances.min(0))<.0002 and np.max(distances.min(1))<.0002)
   for i in np.flatnonzero(mask):labels.add(g._etiketler(prim,int(i)))
   removed+=int(mask.sum());g.sil(prim,mask)
  assert removed==len(old['F']),(name,removed,len(old['F']))
  assert len(labels)==1,(name,labels)
  v,f=shape.tessellate(.01,.05);vv=np.array([[x.x,x.y,x.z] for x in v]);ff=np.array(f)
  kat,mek,kpk=next(iter(labels));g.ucgen_ekle(old['dugum'],vv[ff],kat=kat,mek=mek,kpk=kpk)
  rows.append({'part':name,'old_triangles':removed,'new_triangles':len(ff),'max_original_vertex_CAD_distance_mm':max(cad_distances),'cad_dimensions_unchanged':True,'tessellation_linear_mm':.01,'angular_rad':.05})
  ent[name]={'dugum':old['dugum'],'kutu':[lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]],'tur':'profil','bom':[old['ac']]}
 temp=dest.with_suffix('.raw.glb');g.kaydet(str(temp));del g
 subprocess.run([sys.executable,str(Y/'50_sikilastir.py'),str(temp),str(dest)],env=dict(os.environ,YAMA_IS_KOK=str(Y/'kaynak')),check=True);temp.unlink()
 report={'step':74,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'parts':rows,'production_release':False}
 dest.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 dest.with_name(dest.stem+'_ent.json').write_text(json.dumps({'adim':74,'parca':ent},ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False),flush=True)

if __name__=='__main__':
 source,dest=map(Path,sys.argv[1:3]);apply(source,dest);sys.stdout.flush();os._exit(0)
