"""Candidate station sequence for two welded conveyor sides.
Separate outputs; does not activate source or certify temporary fixtures.
"""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_montaj.py'
code=source.read_text(encoding='utf-8')
code=code.replace("'k_parca.pkl'","'k_parca_belt_verified.pkl'")
code=code.replace('from k_sac_kaynak import load as load_current_sheets', '''
_sheet_source=HERE/'k_sac_kaynak.py'
_sheet_code=_sheet_source.read_text(encoding='utf-8').replace("'current_sheet_bending.json'","'current_sheet_bending_belt.json'").replace("'native_sheet_mapping_audit.json'","'native_sheet_mapping_audit_belt.json'")
_sheet_ns=dict(__file__=str(_sheet_source),__name__='candidate_sheet_loader')
exec(compile(_sheet_code,str(_sheet_source),'exec'),_sheet_ns)
load_current_sheets=_sheet_ns['load']
''')
start=code.index("# The conveyor's custom frame")
end=code.index('# Mount the long left wireway',start)
new='''# Real side weldments are fabricated BEFORE supplier rollers are installed.
_belt_meta=json.loads((HERE.parent/'belt_support_candidate/audit.json').read_text(encoding='utf-8'))
for rail in ('bant_yan_-421','bant_yan_-3'):
 members=[rail];seams=[]
 for j in _belt_meta['joints']:
  if j['plate']!=rail:continue
  x,z=j['id'].split('_');tag=f'{float(x)}_{float(z)}'
  members += ['k72_bant_ayak_flansi_'+tag,j['post'],j['cap']]
  seams += sorted(a for a in P if a.startswith('k72_bant_ayak_kaynagi_'+tag+'_'))+[j['cap_weld']]+j['plate_welds']
 GROUPS[rail]=members;WELDS[rail]=seams;done.update(members[1:]);done.update(seams)
for members in (['tahrik_rulosu_EC5000_354','tahrik_rulosu_EC5000_hex_mil'],['avara_rulosu_46','avara_mili_0','avara_mili_1']):
 GROUPS[members[0]]=members;done.update(members[1:])

'''
code=code[:start]+new+code[end:]
anchor='ordered=[];cycle_breaks=[]'
new_edges='''# Replace the old merged-frame contact guesses with actual open-side order.
for roller in ('tahrik_rulosu_EC5000_354','avara_rulosu_46'):
 edges.discard((roller,'bant_yan_-421'))
for wall in ('sol_sac_urun_girisi','sag_sac_E_penceresi'):
 edges.discard((wall,'bant_yan_-3'));before('bant_yan_-3',wall)
# Rear bearing support must precede factory rollers; close front side later.
for roller in ('tahrik_rulosu_EC5000_354','avara_rulosu_46'):
 before('bant_yan_-421',roller);before(roller,'bant_yan_-3')
 before(roller,'tahrik_rulosu_EC5000_M8_civata')
before('bant_yan_-3','tahrik_rulosu_EC5000_M8_civata')
for a in ('bant_traversi_0','bant_traversi_1','olu_plaka','kayma_tablasi'):
 before('bant_yan_-3',a)
# Side feet must be seated before their actual mounting hardware.
for j in json.loads((ROOT/'_local/codex_k_montaj/k72_mounts.json').read_text(encoding='utf-8'))['connections']:
 if j['id'].startswith('M6_'):
  rail='bant_yan_'+str(int(j['center_mm'][2]))
  for a in j['parts']:before(rail,a)
'''
assert anchor in code;code=code.replace(anchor,new_edges+'\n'+anchor)
# Diagnostic output names protect all previously verified canonical plans.
for old,new in [('order_constraints.json','belt_order_constraints.json'),('plan_progress.json','belt_plan_progress.json'),('plan_k.pkl','plan_k_belt_candidate.pkl'),('plan_audit.json','belt_plan_audit.json')]:code=code.replace(old,new)
code=code.replace('from k_son_kaynak import bind as bind_full_source\nbind_full_source()','')
# Explicitly visible provisional bench-support warning until real fixture audit.
code=code.replace("print('INSTALL',a,flush=True)","print('INSTALL',a,flush=True)\n if a in ('bant_yan_-421','bant_yan_-3'):olay(t,'UYARI: Yan bant kaynak alt montajı dayalıdır; geçici destek/fikstür ve kaynak torcu erişimi henüz doğrulanmadı.')")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))

