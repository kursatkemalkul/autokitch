"""K sequence-only iteration using the unchanged TOPPING v6 path planner.
Production bending/connection release follows only after PLAN_SORUN reaches zero.
"""
from pathlib import Path
import sys,os,json,pickle,math,time
import numpy as np
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; os.chdir(HERE)
sys.path.insert(0,str(ROOT/'_local/claude_son_yerel/gece2/cekmece'));sys.path.insert(0,str(HERE))
import yol_denetim_v2 as Y
import v2geo as G
T0=time.time(); D0=pickle.load(open('k_parca.pkl','rb'));P=D0['P'];ENT=D0['ENT']
SAC={};PEM_SAC={};CEVRE=[a for a in P if P[a]['tur']=='cevre'];KAPGRUP=[]
def bk(x):return x.replace('_',' ')
def tr(a):return P[a]['ac']
exec((HERE/'_altyapi.py').read_text(encoding='utf-8'))
# The cold cabinet is the real stationary support at the K assembly interface.
if 'cevre_B' in P:
 basla('cevre_B',np.zeros(3),0.0);YER['cevre_B']=0.0;YERINDE.append('cevre_B')
def haric(a,b,neden):
 assert neden.strip();HARIC_PLAN.add((a,b));HARIC_NEDEN[(a,b)]=neden
AD=[YOL((0,700,0)),YOL((0,0,950)),YOL((0,0,-950)),YOL((-650,0,0)),YOL((650,0,0)),YOL((0,-650,0))]
def rank(a):
 v=P[a];lo=v['V'].min(0);hi=v['V'].max(0);name=a.lower()
 if name.startswith('k71_alt_') or name.startswith('k71_dikme'):phase=0
 elif name.startswith('k71_') or hi[1]<920:phase=1
 elif v['tur'] in ('kaynak','baglanti'):phase=6
 elif 'kablo' in v['tur'] or 'hortum' in name:phase=7
 elif any(w in name for w in ('kapak','tavan','arka_sac','yan_sac')):phase=5
 elif v['tur'] in ('sac','profil'):phase=2
 else:phase=3
 return phase,float(lo[1]),a
ph=None; done=set()
# Six supports are real welded subassemblies made on a bench, not floating independent weld strips.
GROUPS={};WELDS={}
for x in (4060,4340):
 for z in (700,379,58):
  tag=f'{x}_{z}'; members=[n for n in (f'k71_alt_flans_{tag}',f'k71_disli_ust_kapak_{tag}',f'k71_dik_destek_{tag}') if n in P]
  if len(members)==3:
   GROUPS[members[0]]=members;WELDS[members[0]]=[n for n in P if n.startswith('k71_kaynak_'+tag+'_')]
   done.update(members[1:]);done.update(WELDS[members[0]])
# Pressed bottom studs accompany the base sheet; their attachment must precede support installation.
PEMS=[a for a in P if a.startswith('k71_alt_saplama_')]
if 'taban_sac_3' in P:
 for a in PEMS:
  P[a]['yan']=np.array([0,1.,0]);P[a]['pem_ad']='PEM FHP-M5-15';P[a]['sac']='taban_sac_3'
  haric(a,'taban_sac_3','PEM FHP-M5-15 preslenmiş saplama: adım71 gerçek taban deliğine üretimde kenetlenir; tabanla gelir')
 done.update(PEMS)
# Base first; finished welded supports next, shelf later; enclosing panels last.
def seqrank(a):
 q=rank(a)
 if a=='taban_sac_3':return (-2,0,a)
 if a in GROUPS:return (-1,0,a)
 if a.startswith('k71_alt_pul_'):return (0,0,a)
 if a.startswith('k71_alt_somun_'):return (0,1,a)
 return q
for a in sorted([a for a in P if a not in CEVRE and a not in done],key=seqrank):
 phase=seqrank(a)[0]
 if phase!=ph:
  ph=phase;adim('K montaj aşaması '+str(phase),'Gerçek model parçaları; aday yollar mevcut v6 yerleştiriciyle denetlenir.','Sıra denemesi; üretim onayı değildir.')
 print('INSTALL',a,flush=True)
 if P[a]['tur']=='kaynak':
  # Weld appears at its true joined interface; connection audit still checks that both carriers exist.
  t=buyu(a,t,0.6)
 elif P[a]['tur']=='kablo':
  t=buyu(a,t,0.6)
 else:
  t=yerlestir(GROUPS.get(a,[a]),AD,t,tr(a),pem=PEMS if a=='taban_sac_3' else (),tezgah_kaynak=WELDS.get(a,()),sure_bekle=0.02)
 (HERE/'plan_progress.json').write_text(json.dumps({'last_part':a,'installed':len(YER),'problems':PLAN_SORUN,'elapsed_seconds':round(time.time()-T0,2)},ensure_ascii=False,indent=2),encoding='utf-8')
for a in CEVRE:
 if a not in GOR:basla(a,np.zeros(3),t);YER[a]=t
TOPLAM=bitti()+2
exec((HERE/'_son.py').read_text(encoding='utf-8').replace("'plan_a3.pkl'","'plan_k.pkl'").replace('OLC = 1.75','OLC = 1.0'))
json.dump({'source':'local k73 on step61; pending shared-chain registration','production_release':False,'plan_problems':PLAN_SORUN,'unplanned':[a for a in P if a not in GOR],'parts':len(P),'seconds':round(time.time()-T0,2)},open('plan_audit.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
