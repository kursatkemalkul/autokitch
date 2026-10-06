"""Local step78 prototype: repair only three current K sheet mesh topologies.

Consumes the audited small repair payload. Matches every original triangle on
the inherited 0.0001 mm naming grid, keeps existing material/mechanism labels,
and never replaces a purchased component. This is not chain registration or a
production release. Re-extraction and all manufacturing audits remain required.
"""
from lower_support import *
from pathlib import Path
import pickle,hashlib,subprocess
from collections import Counter
Y=H/'yama_v9'
for path in (Y,Y/'kaynak',Y/'kaynak/gece'):sys.path.insert(0,str(path))
from m8kit import Glb

def key(t):
 q=np.round(t,4)
 # Preserve winding; tolerate cyclic starting-vertex permutations only.
 return min(np.roll(q,i,axis=0).tobytes() for i in range(3))

def apply(source,dest,payload):
 proposal=pickle.load(payload.open('rb'));repairs=proposal['repairs']
 assert set(repairs)=={'sol_sac_urun_girisi','sag_sac_E_penceresi','ust_sac'}
 wanted={a:Counter(key(t) for t in r['original_triangles']) for a,r in repairs.items()}
 assert not (set(wanted['sol_sac_urun_girisi'])&set(wanted['sag_sac_E_penceresi']))
 origin_by_key={}
 for a,keys in wanted.items():
  for k in keys:
   assert k not in origin_by_key,'Ambiguous repair ownership'
   origin_by_key[k]=a
 g=Glb(str(source));selections=[];templates={};matched=Counter();adjustments=[]
 for p in g.dprims('K_GOVDE__kabuk'):
  if p.get('gizli'):continue
  selected=[]
  for i,t in enumerate(p['X'][p['T']]):
   k=key(t);a=origin_by_key.get(k)
   if a is None or wanted[a][k]<=0:continue
   labels=g._etiketler(p,i)
   if a in templates:assert labels==templates[a][1],(a,'mixed source labels')
   else:templates[a]=(p,labels)
   wanted[a][k]-=1;selected.append(i);matched[a]+=1
   adjustments.append(float(np.max(np.linalg.norm(t-np.round(t,4),axis=1))))
  if selected:selections.append((p,np.asarray(selected,dtype=int)))
 assert all(not any(c.values()) for c in wanted.values()),{a:sum(c.values()) for a,c in wanted.items()}
 assert set(templates)==set(repairs)
 for p,indices in selections:
  mask=np.zeros(len(p['T']),dtype=bool);mask[indices]=True;g.sil(p,mask)
 for a,r in repairs.items():
  proof=r['proof'];assert proof['closed_status']=='Error.NoError'
  assert proof['maximum_declared_precision_adjustment_mm']<=.001
  p,(kat,mek,kpk)=templates[a]
  g._ekle_dunya(p,r['vertices'][r['triangles']],kat,mek,kpk)
 dest.parent.mkdir(parents=True,exist_ok=True);raw=dest.with_suffix('.raw.glb');g.kaydet(str(raw));del g
 subprocess.run([sys.executable,str(Y/'50_sikilastir.py'),str(raw),str(dest)],env=dict(os.environ,YAMA_IS_KOK=str(Y/'kaynak')),check=True);raw.unlink()
 report={'step':78,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'payload_sha256':hashlib.sha256(payload.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'matched_source_triangles':dict(matched),'naming_grid_mm':.0001,'maximum_naming_grid_adjustment_mm':max(adjustments),'repairs':[r['proof'] for r in repairs.values()],'source_labels_retained':True,'source_interfaces_intended_unchanged':True,'unrelated_geometry_audit_required':True,'reextraction_required':True,'production_release':False}
 dest.with_suffix('.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
 print('STEP78',report['output_sha256'],dict(matched),flush=True)

if __name__=='__main__':
 apply(*map(Path,sys.argv[1:4]));sys.stdout.flush();os._exit(0)
