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
from k_sac_kaynak import load as load_current_sheets
SAC,SHEET_AUDIT=load_current_sheets(P)
assert all(r['passed'] for r in SHEET_AUDIT),'Current manufacturing mesh mapping failed'
PEM_SAC={};CEVRE=[a for a in P if P[a]['tur']=='cevre'];KAPGRUP=[]
def bk(x):return x.replace('_',' ')
def tr(a):return P[a]['ac']
exec((HERE/'_altyapi.py').read_text(encoding='utf-8'))
# The cold cabinet is the real stationary support at the K assembly interface.
if 'cevre_B' in P:
 basla('cevre_B',np.zeros(3),0.0);YER['cevre_B']=0.0;YERINDE.append('cevre_B')
def haric(a,b,neden):
 assert neden.strip();HARIC_PLAN.add((a,b));HARIC_NEDEN[(a,b)]=neden
AD=[YOL((0,700,0)),YOL((0,0,950)),YOL((0,0,-950)),YOL((-650,0,0)),YOL((650,0,0)),YOL((0,-650,0))]
# Approach above the frame, descend with 50 mm stud clearance, then seat along X.
AD.extend([YOL((0,700,0),(50,0,0)),YOL((0,700,0),(-50,0,0)),YOL((0,0,950),(50,0,0)),YOL((0,0,950),(-50,0,0))])
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
# Source-defined welded tube sleeves travel with their carrier; weld seams are real declared interfaces.
if 'taban_sac_tasiyici_20' in P:
 members=['taban_sac_tasiyici_20']+[a for a in P if a.startswith('taban_sac_tasiyici_20_kovan_') and 'kaynagi' not in a]
 GROUPS[members[0]]=members;WELDS[members[0]]=[a for a in P if a.startswith('taban_sac_tasiyici_20_kovan_kaynagi_')]
 done.update(members[1:]);done.update(WELDS[members[0]])
if 'k71_istasyon_rafi' in P:
 members=['k71_istasyon_rafi']+[a for a in ('k71_raf_yan_sac_4005','k71_raf_yan_sac_4395') if a in P]
 GROUPS[members[0]]=members;WELDS[members[0]]=[a for a in P if a.startswith('k71_raf_yan_kaynagi_')]
 done.update(members[1:]);done.update(WELDS[members[0]])
# Door skins, latch counterplates and hinge leaves are joined on the bench before the lift-off door enters the frame.
if all(a in P for a in ('k_govde_on_seffaf_0','k_govde_on_seffaf_1')):
 door=[a for a in P if a.startswith('k_govde_on_seffaf_')]+[a for a in P if a.startswith('onyuz_kapak_K_') and ('_karsilik_' in a or '_kanat' in a or '_pem_' in a)]
 seams=[a for a in P if P[a]['tur']=='kaynak' and ('onyuz_kapak_K' in a)]
 GROUPS[door[0]]=door;WELDS[door[0]]=seams;done.update(door[1:]);done.update(seams)

# Supplier-built actuator end caps and moving table are delivered as one unit; our feet, sensors and fittings remain separate.
for prefix in ('itici_X_MY1B10G-250','itici_Z_MY1B10G-350'):
 head=prefix+'_profil';members=[a for a in (head,prefix+'_uc_kapagi_0',prefix+'_uc_kapagi_1',prefix+'_masa') if a in P]
 if len(members)==4:GROUPS[head]=members;done.update(members[1:])
# PulsaJet supplier cover and internal electrical socket arrive with the complete nozzle body.
head='PulsaJet_AAB10000AUH-104210-VIFC'
if head in P:
 members=[a for a in (head,'PulsaJet_kapak_CP104218-SS','PulsaJet_M8_soketi_9') if a in P]
 GROUPS[head]=members;done.update(members[1:])

# Build the DIN panel on the rear sheet on a bench, then enter from the rear before the cabinet closes.
rear_members=['arka_sac']+[a for a in P if a.startswith(('pano_','din_rayi_','plc_','guc_24V','sigorta_','klemens_','valf_','sartlandirici_'))]
if 'arka_sac' in P and 'pano_plakasi' in rear_members:
 GROUPS['arka_sac']=rear_members;done.update(rear_members[1:])

# Pressed bottom studs accompany the base sheet; their attachment must precede support installation.
PEMS=[a for a in P if a.startswith('k71_alt_saplama_')]
if 'taban_sac_3' in P:
 for a in PEMS:
  P[a]['yan']=np.array([0,1.,0]);P[a]['pem_ad']='PEM FHP-M5-15';P[a]['sac']='taban_sac_3'
  haric(a,'taban_sac_3','PEM FHP-M5-15 preslenmiş saplama: adım71 gerçek taban deliğine üretimde kenetlenir; tabanla gelir')
 done.update(PEMS)
SHELFPEMS=[a for a in P if a.startswith('k71_raf_PEM_')]
for a in SHELFPEMS:
 P[a]['yan']=np.array([0,-1.,0]);P[a]['pem_ad']='PEM SP';P[a]['sac']='k71_istasyon_rafi'
 haric(a,'k71_istasyon_rafi','PEM SP somun: adım71 eşleşen lazer deliğine preslenir; sacla birlikte gelir, dişli bağlayıcıdır')
done.update(SHELFPEMS)
THREAD_AXES={}
for file in ('k71_lower.json','k72_mounts.json'):
 data=json.loads((ROOT/'_local/codex_k_montaj'/file).read_text(encoding='utf-8'))
 for j in data['connections']:
  members=[a for a in j['parts'] if a in P]
  if j['id'].startswith('top_'):
   screw,cap=members[:2]
   haric(screw,cap,'DIN7991 M5×10 / diş açılmış 6 mm kapak: adım71 doğrulanan 6 mm diş kavraması; düz nominal vida ağı helis diş yerine kullanılır, hareket yalnız diş eksenindedir')
   THREAD_AXES[screw]=[0,100,0]
  elif file=='k72_mounts.json':
   screw=next(a for a in members if 'vida' in a);nut=next(a for a in members if 'somun' in a)
   haric(screw,nut,'ISO4762 / ISO10511 eş çaplı diş çifti: adım72 kavrama ve 1–3 diş taşması denetlenmiş; nominal düz ağ diş kavramasını temsil eder, montaj yalnız ortak eksende')
   THREAD_AXES[screw]=[0,100,0];THREAD_AXES[nut]=[0,-100,0]
   for a in members:
    if 'alt_pul' in a:THREAD_AXES[a]=[0,-100,0]
   female='k71_raf_PEM_'+j['id']
   if female in P:haric(screw,female,'Adım71 PEM SP ve adım72 eş M5/M6 vida: ortak lazer deliğinde belirtilen dişli kavrama; yalnız ortak Y ekseni boyunca takılır')
PRESS_BY_SHEET={'taban_sac_3':PEMS,'k71_istasyon_rafi':SHELFPEMS}
LEGACY={a['name']:a for a in json.loads((ROOT/'_local/codex_k_montaj/legacy_catalog.json').read_text(encoding='utf-8'))}
for a,c in LEGACY.items():
 meta=c.get('meta') or {};receivers=meta.get('ic_ice',[])
 if a not in P or not meta.get('pem_tip') or not receivers:continue
 receiver=next((q for q in receivers if q in P and P[q]['tur'] in ('sac','profil','mek')),None)
 if receiver is None:continue
 extent=HI[a]-LO[a];axis=int(np.argmin(np.abs(extent-meta['boy']))) if meta.get('boy') else int(np.argmin(extent))
 # Folded panels have off-centre boxes: determine the head end from the stud's actual radial rings.
 points=P[a]['V'];perp=[q for q in range(3) if q!=axis];centre=(LO[a]+HI[a])/2
 radial=np.linalg.norm(points[:,perp]-centre[perp],axis=1)
 low_radius=radial[points[:,axis]<=LO[a][axis]+.02].max();high_radius=radial[points[:,axis]>=HI[a][axis]-.02].max()
 e=np.zeros(3);e[axis]=-1. if high_radius>low_radius+1e-4 else 1.
 P[a]['yan']=e;P[a]['pem_ad']=meta.get('std','PEM');P[a]['sac']=receiver
 PRESS_BY_SHEET.setdefault(receiver,[]).append(a);done.add(a)
 haric(a,receiver,'Kaynak CAD bağlantı kaydı: '+meta.get('std','PEM')+' doğrudan '+receiver+' eşleşen deliğine preslenir; sacla birlikte gelir; diğer parçalar için istisna değildir')
 base=a.rsplit('_saplama',1)[0]
 for suffix in ('_pul','_somun'):
  nut=base+suffix
  if nut in P:
   THREAD_AXES[nut]=(e*50).tolist()
   if suffix=='_somun':haric(a,nut,'Kaynak CAD aynı merkez/eksenli '+meta.get('dis','M5')+' PEM saplama ve ISO10511 somun diş çifti; nominal ağın dişli kavraması, yalnız ortak eksende takma')
# Rivet nuts are set into the original drilled receiving profiles before the profiles enter the frame.
for a in P:
 if not a.startswith('govde_m8_') or 'ara_pul' in a:continue
 _,_,side,yy,zz=a.split('_');yy=float(yy);zz=float(zz)
 x=20 if side=='F' else 380
 receiver=('k71_raf_yan_sac_'+str(4005 if side=='F' else 4395)) if yy==877 else f'kose_dikmesi_{x}_{int(-zz)}'
 if receiver not in P:continue
 e=np.array([-1.,0,0]) if side=='F' else np.array([1.,0,0])
 P[a].update(yan=e,pem_ad='M8 rivet nut',sac=receiver)
 PRESS_BY_SHEET.setdefault('k71_istasyon_rafi' if yy==877 else receiver,[]).append(a);done.add(a)
 haric(a,receiver,'Source h3_k_sac_v1.m8_noktalari: M8 rivet nut installed in its own Ø11 drilled receiving profile, expansion grip on wall; travels with receiving part')
# Explicit axial directions from the source hinge screw definitions; no collision exemption for an undrilled solid proxy.
for a in P:
 if '_mentese_' in a and '_sabit_vida_' in a:
  THREAD_AXES[a]=[40.,0,0];female=a.split('_sabit_vida_')[0]+'_sabit'
  if female in P:haric(a,female,'Source h3_k_sac_v1 hinge body contains Ø5×9 axial blind M5 bore; ISO7380 M5×12 into this specified threaded bore; nominal Ø5 mesh replaces helical thread only')
 if '_mentese_' in a and '_kanat_vida_' in a:
  THREAD_AXES[a]=[0,0,-40.]
  female=a.replace('_kanat_vida_','_pem_')
  if female in P:haric(a,female,'Source h3_k_sac_v1 hinge leaf: ISO7380 M5×6 into matching SP-M5-1; nominal thread proxy pair on common Z axis')
# Native DGRF mounting interface: four M10 screws enter from the back along Z.
for a in P:
 if a.startswith('DGRF_M10_civata_'):
  THREAD_AXES[a]=[0,0,-100.]
  haric(a,'DGRF-C-63-125_govde','Native kesme_cad_v8 DGRF body: four M10 threaded mounting bores, T2 24 mm; nominal cylindrical thread surfaces, axial screw insertion only')
  for b in ('DGRF_ZBH-12_0','DGRF_ZBH-12_1'):
   if b in P and np.linalg.norm(((LO[a]+HI[a])/2)[:2]-((LO[b]+HI[b])/2)[:2])<.01:
    haric(a,b,'Native DGRF ZBH-12-B centring bush Ø10 screw passage: nominal equal-diameter cylindrical mating; same M10 axis, no exception for brackets')
 if a.startswith('DGRF_ZBH-12_'):
  THREAD_AXES[a]=[0,0,100.]
  haric(a,'DGRF_baglanti_plakasi','Native DGRF mounting plate has Ø12 H7 centring seat, 5 mm deep; ZBH-12 exact-diameter fit, axial insertion')
  haric(a,'DGRF-C-63-125_govde','Native DGRF body has Ø12 × 2.6 centring seat; manufacturer centring bush exact-diameter fit, axial insertion')
 if a=='tahrik_rulosu_EC5000_M8_civata':THREAD_AXES[a]=[0,0,100.]

for a in P:
 if a.startswith('itici_X_MY1B10G-250_D-M9N_'):THREAD_AXES[a]=[0,0,100.]
 if a.startswith('itici_Z_MY1B10G-350_D-M9N_'):THREAD_AXES[a]=[100.,0,0]

if 'k76_tarti_rakor_M16_govde' in P:
 THREAD_AXES['k76_tarti_rakor_M16_govde']=[-100.,0,0]
 THREAD_AXES['k76_tarti_rakor_M16_kilit_somunu']=[100.,0,0]
 haric('k76_tarti_rakor_M16_govde','k76_tarti_rakor_M16_kilit_somunu','Adım76: M16 boyun / M16 kilit somunu ortak X ekseninde nominal dişli yüzey teması; sac ve çevre için istisna yok')
for a in P:
 if a.startswith('k75_kiris_vida_') or a.startswith('k75_kiris_pul_bas_'):THREAD_AXES[a]=[0,0,-100.]
 if a.startswith('k75_kiris_somun_') or a.startswith('k75_kiris_pul_somun_'):THREAD_AXES[a]=[0,0,100.]

# Base first; finished welded supports next, shelf later; enclosing panels last.
def seqrank(a):
 q=rank(a)
 if a=='taban_sac_3':return (-2,0,a)
 if a=='ust_sac':return (8,0,a)
 if a in ('sol_sac_urun_girisi','sag_sac_E_penceresi','arka_sac'):return (7,0,a)
 if a.startswith('k71_alt_flans_'):return (-1,0,a)
 if a.startswith('k71_alt_pul_'):return (0,0,a)
 if a.startswith('k71_alt_somun_'):return (0,1,a)
 if a.startswith('k_govde_on_seffaf_'):return (10,0,a)
 if a=='k71_istasyon_rafi':return (1,0,a)
 return q
# Resolve previously observed blocked paths by precedence, without removing any obstacles.
items=[a for a in P if a not in CEVRE and a not in done and P[a]['tur'] not in ('kaynak','kablo')]
alias={a:a for a in items}
for head,members in GROUPS.items():
 for member in members+WELDS.get(head,[]):alias[member]=head
for receiver,presses in PRESS_BY_SHEET.items():
 for a in presses:alias[a]=receiver
edges=set()
def before(a,b):
 a=alias.get(a,a);b=alias.get(b,b)
 if b=='k71_istasyon_rafi' and a not in GROUPS and not a.startswith(('k71_alt_somun_','k71_alt_pul_')) and a!='taban_sac_3':return
 if a!=b and a in items and b in items:edges.add((a,b))
for group in GROUPS:
 if group.startswith('k71_alt_flans_') or group=='taban_sac_tasiyici_20':before('taban_sac_3',group);before(group,'k71_istasyon_rafi')
for a in P:
 if a.startswith('k71_alt_somun_'):before(a,'k71_istasyon_rafi')
for a in ('sol_sac_urun_girisi','sag_sac_E_penceresi','arka_sac','k_govde_on_seffaf_0','k_govde_on_seffaf_1'):
 before('k71_istasyon_rafi',a)
previous=HERE/'no_previous_constraints.json'
if previous.exists():
 for problem in json.loads(previous.read_text(encoding='utf-8'))['plan_problems']:
  for a,b in problem['sorun']:
   if a not in THREAD_AXES and a not in ('k71_istasyon_rafi','sol_sac_urun_girisi','sag_sac_E_penceresi','arka_sac') and (a,b) not in HARIC_PLAN and (b,a) not in HARIC_PLAN:before(a,b)
for file in ('k71_lower.json','k72_mounts.json'):
 for j in json.loads((ROOT/'_local/codex_k_montaj'/file).read_text(encoding='utf-8'))['connections']:
  names=j['parts']
  if j['id'].startswith('base_'):
   before(names[1],names[2]);before(names[2],names[3])
  elif j['id'].startswith('top_'):
   before(names[1],names[0]);before(names[2],names[0])
  else:
   screw=names[0];before('k71_istasyon_rafi',screw)
   for a in names[1:]:
    if 'ust_pul' in a:before(a,screw)
    else:before(screw,a)
   for nut in names:
    if 'somun' in nut:
     for washer in names:
      if 'alt_pul' in washer:before(washer,nut)
   for a in P:
    if a.startswith('k72_') and P[a]['tur'] in ('sac','profil'):
     lo=P[a]['V'].min(0);hi=P[a]['V'].max(0);x,_,z=j['center_mm']
     if lo[0]-.1<=x<=hi[0]+.1 and lo[2]-.1<=z<=hi[2]+.1:before(a,screw)
# Thread-axis probes identify the only remaining obstruction: install nuts before the upper electrical devices.
for a in THREAD_AXES:
 if '_mentese_' in a and '_sabit_vida_' in a:before('kose_dikmesi_20_42',a);before(a.split('_sabit_vida_')[0]+'_sabit',a)
 if '_mentese_' in a and '_kanat_vida_' in a:before(a.split('_kanat_vida_')[0]+'_kanat',a)
 if a.endswith('_somun'):
  base=a[:-len('_somun')];before(base+'_pul',a)
  stud=base+'_saplama';receiver=P.get(stud,{}).get('sac')
  if receiver:before(receiver,base+'_pul');before(receiver,a)
  if a in ('govde_kulak_ust_arka_80_bag_somun','govde_kulak_ust_arka_200_bag_somun'):
   before(a,'k_elektrik_aluminyum_1');before(a,'k_elektrik_siemens_0')
# Source-defined assembly precedence: roller shafts before end plates close around them.
for roller in ('avara_rulosu_46','tahrik_rulosu_EC5000_354','avara_mili_0','tahrik_rulosu_EC5000_hex_mil'):
 for obstruction in ('bant_yan_-3','bant_yan_-421','bant_traversi_0','bant_traversi_1','kopru_kirisi_-126','kopru_kirisi_-286'):
  before(roller,obstruction)
for lower,upper in zip(('yag_tarti_taban_plakasi','yag_tarti_alt_takozu','yag_tarti_yuk_hucresi_PW15AH','yag_tarti_ust_takozu','yag_tarti_platformu'),('yag_tarti_alt_takozu','yag_tarti_yuk_hucresi_PW15AH','yag_tarti_ust_takozu','yag_tarti_platformu','yag_tenekesi_18L')):
 before(lower,upper)
# A finished RollerDrive is supplied with its end shaft; the driven roller screw is fitted later.
# The load-cell stack is assembled from its fixed base towards the removable platform.
oil_parts=[a for a in P if any(q in a for q in ('tarti','PW15AH','ara_takoz','ara_mesafe'))]
(HERE/'oil_stack_inventory.json').write_text(json.dumps({a:{'lo':LO[a].tolist(),'hi':HI[a].tolist(),'description':tr(a)} for a in oil_parts},ensure_ascii=False,indent=2),encoding='utf-8')

# Install inner DIN equipment before closing front cable ducts; its own rear plate remains first.
control=[a for a in P if a.startswith(('plc_','guc_24V','din_ray_','klemens_','sigorta_','valf_','hava_sartlandirici_'))]
for a in control:
 before('pano_plakasi',a)
 for b in P:
  if b.startswith(('elk_ic_kanal_','elk_zincir_kanal_')):before(a,b)
for i in range(3):
 fixed=f'onyuz_kapak_K_mentese_{i}_sabit';leaf=f'onyuz_kapak_K_mentese_{i}_kanat'
 before(fixed,leaf)
 for suffix in ('a','b'):before(fixed,fixed+'_vida_'+suffix)
# Belt supports precede the closed loop; sensor brackets and guides are fitted last.
for a in P:
 if a.startswith(('bant_yan_','bant_traversi_','avara_','tahrik_rulosu_')):
  for b in P:
   if b.startswith(('cit_braketi_','urun_sensoru_')):before(a,b)
for a in ('bant_traversi_0','bant_traversi_1'):before(a,'kayma_tablasi')

# Rear wall fasteners are inserted through the source-defined 13.5 mm gap before the DIN panel closes access.
for a in P:
 if a.startswith('govde_bag_arka_') and a.endswith(('_pul','_somun')):
  for b in P:
   if b.startswith('pano_plakasi') and alias.get(b,b)!='arka_sac':before(a,b)
for a in ('elk_k_tarti_rakor_0','yag_duvar_gecis_bilezigi_emis','yag_duvar_gecis_bilezigi_donus'):
 before('sol_sac_urun_girisi',a)

for a in P:
 if a.startswith('DGRF_ZBH-12_'):
  before('DGRF_baglanti_plakasi',a);before(a,'DGRF-C-63-125_govde')
 if a.startswith('DGRF_M10_civata_'):
  before('DGRF_baglanti_plakasi',a);before('DGRF-C-63-125_govde',a)

for i in range(3):
 before(f'onyuz_kapak_K_basac_{i}','k_govde_on_seffaf_0')
 before(f'onyuz_kapak_K_mentese_{i}_sabit','k_govde_on_seffaf_0')
 for suffix in ('a','b'):before(f'onyuz_kapak_K_mentese_{i}_sabit_vida_{suffix}','k_govde_on_seffaf_0')

for axis in ('X','Z'):
 prefix='itici_'+axis+('_MY1B10G-250' if axis=='X' else '_MY1B10G-350')
 for a in P:
  if a.startswith(prefix+'_D-M9N_'):before(prefix+'_profil',a)
for a in P:
 if a.startswith(('itici_','kesici_','nozul_','PulsaJet_','hava_ic_kanal_')):
  before(a,'yag_pompa_rafi');before(a,'yag_pompa_plakasi')

# The open frame is closed after belt end plates have entered axially; no path is exempted.
for rail in ('bant_yan_-3','bant_yan_-421'):
 for post in ('kose_dikmesi_20_42','kose_dikmesi_380_42','kose_dikmesi_20_-800','kose_dikmesi_380_-800','emniyet_sari_0','emniyet_siyah_0'):
  before(post,rail)
for a in P:
 if a.startswith(('itici_X_','itici_Z_')):before('bant_yan_-421',a)
 if a.startswith(('yag_pompasi_','yag_emis_filtresi','yag_basinc_sensoru_','yag_geri_basinc_','yag_T_parcasi')):
  before('yag_pompa_rafi',a);before('yag_pompa_plakasi',a)
  for control_part in control:before(control_part,a)
 if a.startswith('yag_tarti_') or a=='yag_tenekesi_18L':before('elk_k_tarti_rakor_0',a)
for i in range(2):before('itici_Z_MY1B10G-350_D-M9N_'+str(i),'itici_Z_yukseltme_97')
before('kayma_tablasi','itici_Z_MY1B10G-350_profil')
before('itici_X_MY-J10_blok_0','itici_Z_plaka');before('itici_X_MY-J10_blok_0','itici_X_merkez_yukseltme')

for i in range(2):
 tag=str(i);before('kopru_kirisi_-286','k75_kiris_pul_bas_'+tag);before('k75_kiris_pul_bas_'+tag,'k75_kiris_vida_'+tag)
 before('DGRF_baglanti_plakasi','k75_kiris_vida_'+tag);before('k75_kiris_vida_'+tag,'k75_kiris_pul_somun_'+tag);before('k75_kiris_pul_somun_'+tag,'k75_kiris_somun_'+tag)
for a in P:
 if a.startswith('k_itici_sac_') or a=='itici_sabit_plaka':before('bant_yan_-421',a)
 if a.startswith('yag_boru_'):before('yag_pompa_plakasi',a)
 if a.startswith('emniyet_'):before('tahrik_rulosu_EC5000_M8_civata',a)
before('itici_X_MY-J10_blok_0','itici_Z_MY1B10G-350_profil');before('itici_X_merkez_yukseltme','itici_Z_MY1B10G-350_profil')

# Access-sensitive installation order; every changed order is checked by the same full path solver.
for a in P:
 if a.startswith('bicak_') and a!='bicak_koruma_halkasi':before('bicak_koruma_halkasi',a)
 if a.startswith(('PulsaJet_','nozul_')):before(a,'kopru_kirisi_yan_20');before(a,'kopru_kirisi_-126')
 if a.startswith(('itici_Z_yukseltme_','itici_Z_ray_')):before('itici_X_merkez_yukseltme',a)
 if a.startswith(('hava_ic_kanal_','elk_zincir_paslanmaz_','elk_zincir_etiket_')):
  before('itici_X_MY-J10_blok_0',a);before('itici_X_merkez_yukseltme',a);before('elk_ic_kanal_6',a)
 if a.startswith(('yag_emme_lansi_','k_yag_pom_','d3_')):
  before('sol_sac_urun_girisi',a);before('yag_tenekesi_18L',a)
for a in ('elk_ic_kanal_6','elk_ic_kanal_8'):before(a,'kopru_kirisi_yan_380')
before('yag_pompasi_GJ-N21_EagleDrive','elk_ic_kanal_2');before('yag_T_parcasi','elk_ic_kanal_2')
# The T union is assembled before fitting its pressure transmitter.
before('yag_T_parcasi','yag_basinc_sensoru_PM1704')
edges.discard((alias.get('yag_basinc_sensoru_PM1704','yag_basinc_sensoru_PM1704'),alias.get('yag_T_parcasi','yag_T_parcasi')))

for a in P:
 if a.startswith('bicak_') and a!='bicak_koruma_halkasi':before(a,'kopru_kirisi_-286')
 if a.startswith(('elk_k_tarti_celik_','elk_zincir_harting_','elk_zincir_rakor_','elk_zincir_hava_')):before('elk_ic_kanal_6',a)
 if a.startswith('hava_ic_aski_'):
  before('hava_ic_kanal_0',a);before('hava_ic_kanal_1',a)
 if a.startswith('yag_pompa_rafi_kosebendi_'):
  before('elk_zincir_paslanmaz_4',a);before('elk_zincir_paslanmaz_5',a)
 if a.startswith('yag_boru_') or a=='yag_basinc_sensoru_PM1704':before(a,'elk_ic_kanal_2')
before('hava_ic_kanal_0','kopru_kirisi_yan_380')
before('sol_sac_urun_girisi','elk_zincir_kanal_1')
before('sol_sac_urun_girisi','k76_tarti_rakor_M16_govde')
before('yag_tarti_taban_plakasi','k76_tarti_rakor_M16_govde')
before('k76_tarti_rakor_M16_govde','k76_tarti_rakor_M16_kilit_somunu')

for a in P:
 if a.startswith(('elk_zincir_m12_','elk_zincir_kod_')):before('elk_ic_kanal_6',a)
 if a in ('elk_k_celik_7','elk_k_celik_1','elk_k_celik_3','elk_ic_kanal_5'):
  before('hava_ic_kanal_1',a);before('elk_ic_kanal_6',a)
for i in (0,3):
 before('elk_zincir_rakor_'+str(i),'elk_zincir_m12_'+str(i));before('elk_zincir_rakor_'+str(i),'elk_zincir_kod_mavi_'+str(i))
for a in ('elk_zincir_hava_1','elk_zincir_kanal_1'):before('elk_zincir_kanal_0',a)
before('elk_zincir_kanal_2','elk_zincir_hava_2')
before('k76_tarti_rakor_M16_kilit_somunu','elk_ic_kanal_1')

remaining=set(items);# Correctly separated side returns must be installed before the rear studs,
# belt endplates and inner fixtures obstruct their lateral entry. Neighbouring
# modules remain visible context only after K factory assembly, as in v6.
for wall in ('sol_sac_urun_girisi','sag_sac_E_penceresi'):
 before(wall,'arka_sac');before(wall,'ust_sac')
 for a in P:
  if a.startswith(('bant_yan_','cit_','elk_ic_kanal_','elk_zincir_kanal_','itici_','DGRF','PulsaJet','yag_tarti_','yag_pompa_')) or a=='yag_tenekesi_18L':before(wall,a)
before('arka_sac','ust_sac')
# Keep the top access open while fittings that enter through it are installed.
for a in ('elk_ic_kanal_8','hava_ic_kanal_0','hava_ic_kanal_1','elk_ic_kanal_5','yag_pompa_rafi','yag_pompa_plakasi','hava_ic_aski_2','hava_ic_aski_3','yag_emis_filtresi','yag_geri_basinc_regulatoru_KBP','yag_pompasi_GJ-N21_EagleDrive','elk_zincir_kanal_1','elk_ic_kanal_2','elk_ic_kanal_3'):
 before(a,'ust_sac')
for a in P:
 if a.startswith(('elk_zincir_paslanmaz_','elk_zincir_harting_','elk_k_tarti_celik_','elk_k_celik_')):before(a,'ust_sac')
before('sol_sac_urun_girisi','yag_damlama_tavasi_F')
# The source feet must be seated before their new step72 screws and washers.
for a in P:
 if a.startswith(('itici_taban_','bant_ayagi_')):
  for file in ('k72_mounts.json',):
   for j in json.loads((ROOT/'_local/codex_k_montaj'/file).read_text(encoding='utf-8'))['connections']:
    x,_,z=j['center_mm']
    if LO[a][0]-.1<=x<=HI[a][0]+.1 and LO[a][2]-.1<=z<=HI[a][2]+.1:
     for b in j['parts']:before(a,b)
ordered=[];cycle_breaks=[]
while remaining:
 ready=[a for a in remaining if not any(b==a and x in remaining for x,b in edges)]
 if not ready:
  a=min(remaining,key=lambda a:(sum(1 for x,b in edges if b==a and x in remaining),seqrank(a)))
  cycle_breaks.append({'part':a,'incoming':[x for x,b in edges if b==a and x in remaining]})
 else:a=min(ready,key=seqrank)
 ordered.append(a);remaining.remove(a)
(HERE/'order_constraints.json').write_text(json.dumps({'edges':sorted(edges),'cycles_requiring_path_recheck':cycle_breaks,'order':ordered},ensure_ascii=False,indent=2),encoding='utf-8')
ordered+=sorted([a for a in P if a not in CEVRE and a not in done and a not in items],key=seqrank)
for a in ordered:
 phase=seqrank(a)[0]
 if phase!=ph:
  ph=phase;adim('K montaj aşaması '+str(phase),'Gerçek model parçaları; aday yollar mevcut v6 yerleştiriciyle denetlenir.','Sıra denemesi; üretim onayı değildir.')
 print('INSTALL',a,flush=True)
 if P[a]['tur'] in ('kaynak','silikon'):
  # Weld appears at its true joined interface; connection audit still checks that both carriers exist.
  t=buyu(a,t,0.6)
 elif P[a]['tur']=='kablo':
  t=buyu(a,t,0.6)
 else:
  if a in THREAD_AXES and not a.startswith('govde_bag_arka_'):
   axial=np.array(THREAD_AXES[a],float);axial=axial/np.linalg.norm(axial)*20
   alternatives=[YOL(axial)]
   for q in range(3):
    if abs(axial[q])<1e-5:
     for sign in (-1,1):
      side=np.zeros(3);side[q]=sign*300;alternatives.append(YOL(side,axial))
  elif a.startswith('govde_bag_arka_') and a.endswith(('_pul','_somun')):
   axial=np.array([0,0,6. if a.endswith('_somun') else 8.]);alternatives=[]
   for q in (0,1):
    for sign in (-1,1):
     side=np.zeros(3);side[q]=sign*100;alternatives.append(YOL(side,axial))
  elif a=='elk_zincir_kanal_0':alternatives=[YOL((0,35,0))]+AD
  elif a=='elk_zincir_kanal_2':alternatives=[YOL((-35,0,0))]+AD
  elif a=='arka_sac':alternatives=[YOL((0,0,-950))]+AD
  elif a=='sag_sac_E_penceresi':alternatives=[YOL((650,0,0)),YOL((0,0,950),(24,0,0))]+AD
  elif a=='sol_sac_urun_girisi':alternatives=[YOL((-650,0,0)),YOL((0,0,950),(-24,0,0)),YOL((0,0,-950),(-24,0,0))]+AD
  elif a=='bant_yan_-3':alternatives=[YOL((0,700,0),(0,0,12)),YOL((0,0,950))]+AD
  elif a=='bant_yan_-421':alternatives=[YOL((0,700,0),(0,0,-12)),YOL((0,0,-950))]+AD
  else:alternatives=AD
  t=yerlestir(GROUPS.get(a,[a]),alternatives,t,tr(a),pem=PRESS_BY_SHEET.get(a,()),tezgah_kaynak=WELDS.get(a,()),sure_bekle=0.02)
 (HERE/'plan_progress.json').write_text(json.dumps({'last_part':a,'installed':len(YER),'problems':PLAN_SORUN,'elapsed_seconds':round(time.time()-T0,2)},ensure_ascii=False,indent=2),encoding='utf-8')
for a in CEVRE:
 if a not in GOR:basla(a,np.zeros(3),t);YER[a]=t
TOPLAM=bitti()+2
exec((HERE/'_son.py').read_text(encoding='utf-8').replace("'plan_a3.pkl'","'plan_k.pkl'").replace('OLC = 1.75','OLC = 1.0'))
json.dump({'source':'local steps74-76 prototypes on registered step73; each two runs byte-identical; no production release','production_release':False,'plan_problems':PLAN_SORUN,'unplanned':[a for a in P if a not in GOR],'parts':len(P),'seconds':round(time.time()-T0,2)},open('plan_audit.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
