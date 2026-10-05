"""Step75 prototype: split two fused K beam bolt/nut proxies into real independent standard fasteners."""
from lower_support import *
import subprocess,hashlib
Y=H/'yama_v9'
for q in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(q))
from m8kit import Glb
import sac_ent as SE

def build():
 parts=[];rows=[]
 for i,x in enumerate((4135.,4265.)):
  y=1439.5;seat=-307.6;length=70.;tag=str(i)
  screw=S.vida('ISO4762','M8',length,(x,y,seat),(0,0,1),ad='k75_kiris_vida_'+tag,birim='K_KESICI')
  washers=[]
  for suffix,z in (('bas',-307.6),('somun',-249.5)):
   sh=cq.Solid.makeCylinder(7.5,1.6,cq.Vector(x,y,z),cq.Vector(0,0,1)).cut(cq.Solid.makeCylinder(4.2,1.8,cq.Vector(x,y,z-.1),cq.Vector(0,0,1)))
   washers.append({'ad':'k75_kiris_pul_'+suffix+'_'+tag,'sh':sh,'wp':cq.Workplane('XY').add(sh),'tur':'arayuz','mal':'celik','bom':['ISO7092 M8 A2-70; 8.4 / 15 × 1.6 mm']})
  nut=S.somun('ISO10511','M8',(x,y,-247.9),(0,0,1),ad='k75_kiris_somun_'+tag,birim='K_KESICI',malzeme='A2-70')
  protrusion=seat+length-(-247.9+nut['meta']['m']);pitch=1.25
  assert 1<=protrusion/pitch<=3 and nut['meta']['m']>=8
  parts.extend([screw,*washers,nut]);rows.append({'id':'beam_'+tag,'axis':[0,0,1],'bolt':'ISO4762 M8×70 A2-70','washers':'2 × ISO7092 M8','nut':'ISO10511 M8 A2-70','hole_mm':9.,'stack_mm':56.5,'engagement_mm':nut['meta']['m'],'protrusion_mm':protrusion,'protrusion_threads':protrusion/pitch,'parts':[screw['ad'],washers[0]['ad'],washers[1]['ad'],nut['ad']]})
 return parts,rows

def apply(source,dest):
 parts,rows=build();g=Glb(str(source));node='K_KESICI__celik';tags=[]
 for x in (4135.,4265.):
  # The existing proxy is one connected bolt + hex nut; never cut out surrounding structure.
  candidates=[]
  g.bilesen(node,0)
  for b in g._bc[node]:
   center=(b['lo']+b['hi'])/2
   if abs(center[0]-x)<.1 and abs(center[1]-1439.5)<.1 and abs(b['lo'][2]+314)<.1 and abs(b['hi'][2]+243)<.1:candidates.append(b)
  assert len(candidates)==1,(x,len(candidates))
  labels={g._etiketler(prim,int(i)) for prim,ii in candidates[0]['parca'] for i in ii};assert len(labels)==1;tags.append(next(iter(labels)))
  g.sil_b(candidates[0])
 ent={}
 for p in parts:
  kat,mek,kpk=tags[int(p['ad'].rsplit('_',1)[1])];g.ucgen_ekle(node,SE.ucgen(p['sh']),kat=kat,mek=mek,kpk=kpk)
  b=p['sh'].BoundingBox();ent[p['ad']]={'dugum':node,'kutu':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax],'tur':'arayuz','bom':p.get('bom',[])}
 temp=dest.with_suffix('.raw.glb');g.kaydet(str(temp));del g
 subprocess.run([sys.executable,str(Y/'50_sikilastir.py'),str(temp),str(dest)],env=dict(os.environ,YAMA_IS_KOK=str(Y/'kaynak')),check=True);temp.unlink()
 report={'step':75,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'connections':rows,'changed_custom_fasteners_only':True,'production_release':False}
 dest.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 dest.with_name(dest.stem+'_ent.json').write_text(json.dumps({'adim':75,'parca':ent},ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False),flush=True)

if __name__=='__main__':
 source,dest=map(Path,sys.argv[1:3]);apply(source,dest);sys.stdout.flush();os._exit(0)
