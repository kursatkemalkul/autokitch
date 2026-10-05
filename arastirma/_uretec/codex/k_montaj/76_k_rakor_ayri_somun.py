"""Step76 prototype: separate the existing M16 gland body and locknut for assembly.
Retains center, exterior envelope, cable passage and original 18 mm F/K stack.
No change to purchased product dimensions; this separates the old fused proxy.
"""
from lower_support import *
import subprocess,hashlib
Y=H/'yama_v9'
for q in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(q))
from m8kit import Glb
import sac_ent as SE

def apply(source,dest):
 g=Glb(str(source));node='ELK_K__rakor'
 # Discover the real tagged node rather than inventing a station/category label.
 matches=[]
 for n in sorted({p['name'] for p in g.prims if p['pr'].get('mode',4)==4 and not p.get('gizli')}):
  if 'rakor' not in n:continue
  try:g.bilesen(n,0)
  except IndexError:continue
  for b in g._bc[n]:
   if np.max(np.abs(b['lo']-np.array([3971.5,1375.53,-307.5])))<.05 and np.max(np.abs(b['hi']-np.array([4009.5,1398.47,-284.5])))<.05:matches.append((n,b))
 assert len(matches)==1,[(n,b['lo'].tolist()) for n,b in matches]
 node,b=matches[0];labels={g._etiketler(pr,int(i)) for pr,ii in b['parca'] for i in ii};assert len(labels)==1
 tags=next(iter(labels));g.sil_b(b)
 v=cq.Vector; axis=v(1,0,0);c=lambda x:v(x,1387.,-296.)
 body=cq.Solid.makeCylinder(11.5,12,c(3971.5),axis).fuse(cq.Solid.makeCylinder(8.,26,c(3983.5),axis)).cut(cq.Solid.makeCylinder(2.8,40,c(3970.5),axis)).clean()
 nut=cq.Solid.makeCylinder(11.,5,c(4001.5),axis).cut(cq.Solid.makeCylinder(8.,5.2,c(4001.4),axis)).clean()
 ent={}
 for name,shape in [('k76_tarti_rakor_M16_govde',body),('k76_tarti_rakor_M16_kilit_somunu',nut)]:
  g.ucgen_ekle(node,SE.ucgen(shape),kat=tags[0],mek=tags[1],kpk=tags[2]);b=shape.BoundingBox()
  ent[name]={'dugum':node,'kutu':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax],'tur':'arayuz','bom':['Existing M16 gland proxy, separated body / locknut; catalog dimensional confirmation remains open']}
 temp=dest.with_suffix('.raw.glb');g.kaydet(str(temp));del g
 subprocess.run([sys.executable,str(Y/'50_sikilastir.py'),str(temp),str(dest)],env=dict(os.environ,YAMA_IS_KOK=str(Y/'kaynak')),check=True);temp.unlink()
 r={'step':76,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'center_mm':[3983.5,1387.,-296.],'thread_diameter_mm':16.,'K_hole_mm':16.5,'stack_mm':18.,'thread_length_mm':26.,'locknut_mm':5.,'protrusion_mm':3.,'external_envelope_preserved':True,'production_release':False}
 dest.with_suffix('.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');dest.with_name(dest.stem+'_ent.json').write_text(json.dumps({'adim':76,'parca':ent},ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(r),flush=True)
if __name__=='__main__':
 source,dest=map(Path,sys.argv[1:3]);apply(source,dest);sys.stdout.flush();os._exit(0)
