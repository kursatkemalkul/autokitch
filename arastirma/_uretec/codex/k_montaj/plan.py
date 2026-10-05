from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parents[4]
SRC=ROOT/'_local/codex_k_montaj/source_cad_full_dfm.json'
D=json.loads(SRC.read_text(encoding='utf8'))
steps=[]
def step(kind,part,text,**kw):
 steps.append(dict(number=len(steps)+1,kind=kind,part=part,text=text,**kw));return len(steps)
for s in D['sheets']:
 a=s['flat']; name=s['name']
 step('laser',name,f'{name}: düz açınımı ve bütün delikleri lazerde kes; çapakları al.',flat=a)
 # PEM locations are sourced from the actual sheet holes, not guessed from names.
 holes=[h for h in a.get('kesikler',[]) if h['tip'] in ('pem_somun','pem_saplama')]
 for h in holes:step('pem_press',name,f'{name}: {h.get("parca",h["tip"])} kendi deliğine preslenir.',hole=h,fixture='pres alt desteği',fastener_axis='sheet normal; exact CAD hardware metadata required')
 order=next((r.get('sira') for r in s['dfm'] if r.get('kural')=='abkant'),None) or [b['no'] for b in a['bukumler']]
 for no in order:
  b=next(b for b in a['bukumler'] if b['no']==no)
  step('press_brake',name,f'{name}: {no}. büküm, {b["yon"]} {b["aci"]:g} derece; iç R {b["R"]:g} mm.',bend=b,fixture='abkant V kalıp',order=order)
for p in D['profiles']:step('profile_cut',p['ad'],f'{p["ad"]}: kesim boyunda gelir; delik ve kesikleri görünür.',profile=p)
# Authoritative joint records retain every sheet, hole and connector. Assembly
# scheduling is deliberately not inferred from coincident surfaces.
joins=[]; failures=[]
for j in D['joins']:
 record={'name':j['ad'],'type':j['tip'],'axis':j.get('eksen'),'sheets':j.get('sac',[]),'holes':j.get('delikler',[]),'hardware':[p['ad'] for p in j.get('parcalar',[])],'cad':j}
 joins.append(record)
 if abs(j.get('es_eksen_sapma_mm',0))>.01:failures.append({'joint':j['ad'],'rule':'coaxial holes','value':j['es_eksen_sapma_mm']})
 for p in j.get('parcalar',[]):
  if p.get('std')=='DIN 9021 / ISO 7093':failures.append({'joint':j['ad'],'part':p['ad'],'rule':'KURALLAR 1.2: M5 ISO7089 washer','actual':p['std']})
 # Sum stack is explicit for through-sheet stud joints; leave packet-type
 # connections unresolved instead of claiming engagement based on contact.
 if j['tip']=='pem_saplama':
  hw=j['parcalar']; stud=next((p for p in hw if p['ad'].endswith('_saplama')),None); washer=next((p for p in hw if p['ad'].endswith('_pul')),None); nut=next((p for p in hw if p['ad'].endswith('_somun')),None)
  if stud and washer and nut:
   protrusion=stud['meta']['boy']-j['paket']-washer['meta']['h']-nut['meta']['m']; thread=j['dis']; pitch={'M5':.8,'M6':1.,'M8':1.25}.get(thread)
   if pitch and not (pitch-1e-6<=protrusion<=3*pitch+1e-6): failures.append({'joint':j['ad'],'rule':'1–3 threads protrusion','protrusion_mm':round(protrusion,4),'pitch_mm':pitch,'threads':round(protrusion/pitch,4)})
checks={'source_inventory_extracted':True,'sheet_dfm_passed':all(r.get('durum')=='GEÇTİ' for s in D['sheets'] for r in s['dfm']),'full_press_brake_order_checked':True,'legacy_generator_is_current_geometry':False,'source_final_geometry_matched':False,'installation_paths_2mm_checked':False,'connection_timing_checked':False,'screw_hole_and_thread_checked':False,'temporary_supported_load_checked':False,'production_release':False}
plan={'version':1,'source_step':61,'source_sha256':D['source_sha256'],'chain_steps_reserved':[70,79],'units':'mm','workshop_steps':steps,'connections':joins,'checks':checks,'legacy_generator_warnings':failures,'failures':[],'pending':['Per-piece match to final source61 surface, including chain edits','Cutting/belt/pusher/oil/electrical acquired products: exact fixing and access','Assembly sequence and visible fixture release only after positive fastening','2mm movement sampling and final position <=0.01mm','Real installation page scope remains held by old claude-k-montaj-v1'],'publish_allowed':False}
out=ROOT/'_local/codex_k_montaj';(out/'montaj_plani.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'production_steps':len(steps),'real_joints':len(joins),'standard_failures':len(failures),'dfm_passed':checks['sheet_dfm_passed'],'publish_allowed':False},ensure_ascii=False))
