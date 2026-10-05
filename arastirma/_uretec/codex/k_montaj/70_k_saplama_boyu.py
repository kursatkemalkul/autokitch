"""Reserved chain step70: shorten ONLY the 32 K panel FHP studs.
GLB -> GLB. No TOPPING modifications. Run twice before chain integration.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import sys,json,os,subprocess,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[4];Y=ROOT/'arastirma/_uretec/h3/yama_v9'
for p in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(p))
from m8kit import Glb
from fastener_audit import audit
CATALOG=[6,8,10,12,15,18,20,25,30]; PITCH=.8
source,dest=map(Path,sys.argv[1:3]);g=Glb(str(source)); names=sorted({p['name'] for p in g.prims if p['name'].startswith('K_GOVDE') and not p.get('gizli')}); records=[];components={}
for name in names:
 try:g.bilesen(name,no=0)
 except (IndexError,ValueError):continue
 for b in g._bc[name]:
  id_=name+'['+str(b['no'])+']'; components[id_]=b
  records.append({'id':id_,'node':name,'lo':b['lo'].tolist(),'hi':b['hi'].tolist()})
r=audit(records);assert r['washers']==32 and len(r['results'])==32 and not r['unresolved'],r
changes=[]
for item in r['results']:
 if item['passed']:continue
 b=components[item['stud']];n=components[item['nut']]; k=item['axis'];sgn=item['direction'];origin=b['lo'][k] if sgn>0 else b['hi'][k];nut_end=n['hi'][k] if sgn>0 else n['lo'][k];stack=(nut_end-origin)*sgn; old=(b['hi'][k]-b['lo'][k]);candidate=[L for L in CATALOG if PITCH-.01<=L-stack<=3*PITCH+.01 and L<old-.01];assert candidate,(item,stack,old)
 L=min(candidate); tip=origin+sgn*L
 def trim(P,k=k,sgn=sgn,tip=tip):
  Q=P.copy();Q[:,:,k]=np.minimum(Q[:,:,k],tip) if sgn>0 else np.maximum(Q[:,:,k],tip);return Q
 # Round shaft has only tip and head/shoulder rings: verify that shortening
 # does not affect any shoulder/ring or create collapsed side faces.
 Pw=np.concatenate([p['X'][p['T'][tri]] for p,tri in b['parca']]);ax=(Pw[:,:,k]-origin)*sgn;ring=np.unique(np.round(ax,3));assert not any(L+.01<x<old-.01 for x in ring),(item,ring)
 new=trim(Pw);assert np.all(np.linalg.norm(np.cross(new[:,1]-new[:,0],new[:,2]-new[:,0]),axis=1)>1e-9)
 g.donustur(b,trim);changes.append({'component':item['stud'],'old_length_mm':round(old,3),'catalog':'PEM FHP-M5-'+str(L),'new_length_mm':L,'protrusion_mm':round(L-stack,4),'threads':round((L-stack)/PITCH,4),'nut_and_washer_unchanged':True})
# Save and compact without rerunning any other station generator.
tmp=dest.with_suffix('.raw.glb');g.kaydet(str(tmp));del g
env=dict(os.environ,YAMA_IS_KOK=str(Y/'kaynak'));r=subprocess.run([sys.executable,str(Y/'50_sikilastir.py'),str(tmp),str(dest)],env=env);assert r.returncode==0;tmp.unlink()
report={'step':70,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'changes':changes,'toppping_modified':False,'source_final_position_audit_pending':True,'publication_allowed':False}
dest.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'step':70,'changed':len(changes),'sha256':report['output_sha256']}),flush=True)
sys.stdout.flush();os._exit(0)
