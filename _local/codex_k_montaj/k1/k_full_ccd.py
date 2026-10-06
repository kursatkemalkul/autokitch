"""Audit combined bench + station rigid-motion paths; never produces release assets.
Native bending self-contact, fixtures, fasteners and tool access are separate gates.
"""
from pathlib import Path
import os,sys,pickle,json,hashlib,time
import numpy as np
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parents[2]/'_local/claude_son_yerel/gece2/cekmece'))
import yol_denetim_v2 as Y
Y.ADIM=.002
path=H/('plan_k_full.pkl' if len(sys.argv)<2 else sys.argv[1]);D=pickle.load(path.open('rb'));T=time.time()
assert D['full_source_triangle_multiset_verified'] and not D['PLAN_SORUN']
P={a:dict(V=np.asarray(p.get('Vm',p['V']))/1000.,F=np.asarray(p.get('Fm',p['F'])),tur=p['tur']) for a,p in D['P'].items()}
inspector=Y.Denetci(P,D['HAR'],D['ROT'],D['GOR'],set(D['ISTISNA']),set(),set(tuple(sorted(pair)) for pair in D['HARIC_PLAN']))
print('FULL_CCD_START',len(P),'step_mm',Y.ADIM*1000,'source',path.name,flush=True)
original_pair_check=inspector.cift
live_issues=[]
def trace_pair(a,b):
 issue=original_pair_check(a,b)
 if issue:
  live_issues.append(issue)
  print('FULL_CCD_ISSUE',json.dumps(issue,ensure_ascii=False),flush=True)
  (H/('full_ccd_live_'+path.stem+'.json')).write_text(json.dumps({'source_plan_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'completed':False,'issues':live_issues},ensure_ascii=False,indent=2),encoding='utf-8')
 return issue
inspector.cift=trace_pair
issues=inspector.denetle(ilerleme=True)
out={'source_plan_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_model_sha256':D['source_model_sha256'],'parts':len(P),'step_mm':Y.ADIM*1000,'triangle_boundary_tolerance_mm':Y.SINIR*1000,'resting_contact_tolerance_mm':Y.OTURMA*1000,'tested_pairs':inspector.ciftsay,'path_issues':issues,'rigid_path_passed':not issues,'bending_self_collision_checked':False,'fixture_checked':False,'connection_checked':False,'production_release':False,'elapsed_seconds':time.time()-T}
(H/('full_ccd_'+path.stem+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print('FULL_CCD_COMPLETE',len(issues),'pairs',inspector.ciftsay,'seconds',round(time.time()-T,2),flush=True)
sys.stdout.flush();os._exit(0 if not issues else 2)
