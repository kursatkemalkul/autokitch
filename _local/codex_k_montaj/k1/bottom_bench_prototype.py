"""Source-bound bench prototype including every bottom-mount support sheet.
No fixture/torch/thermal or whole-connection release is inferred.
"""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_bench_prototype.py';code=source.read_text(encoding='utf-8')
code=code.replace("D=pickle.load((HERE/'k_parca.pkl').open('rb'));P=D['P'];SAC,_=load(P)","D=pickle.load((HERE/'k_parca_bottom_verified.pkl').open('rb'));P=D['P'];SAC={}")
old="text=(HERE/'k_montaj.py').read_text(encoding='utf-8');prefix=text.split('ordered=[];cycle_breaks=[]')[0]"
new='''variant=HERE/'bottom_station_candidate.py'
variant_ns=dict(__file__=str(variant),__name__='variant_definition')
exec(compile(variant.read_text(encoding='utf-8').split("exec(compile(code,str(source),'exec')")[0],str(variant),'exec'),variant_ns)
text=variant_ns['code'];prefix=text.split('ordered=[];cycle_breaks=[]')[0]'''
assert old in code;code=code.replace(old,new)
code=code.replace("report=[];bench_plans={};t0=time.time()", "SAC=initial['SAC']\nreport=[];bench_plans={};t0=time.time()")
assert "SAC=initial['SAC']" in code
start=code.index(" if head=='bant_yan_-421':")
end=code.index(" if head=='sag_sac_E_penceresi':",start)
new=''' if head=='bant_yan_-421':
  belt=json.loads((HERE.parent/'belt_support_candidate/audit.json').read_text(encoding='utf-8'))['joints']
  bottom=json.loads((HERE.parent/'belt_bottom_mount_candidate/audit.json').read_text(encoding='utf-8'))['joints']
  operations=[];belt_weld_after={}
  for j,k in zip(belt,bottom):
   assert j['id']==k['id'];x,z=j['id'].split('_');tag=f'{float(x)}_{float(z)}'
   flange='k72_bant_ayak_flansi_'+tag
   operations += [([flange],[]),([j['post']],[]),([k['insert']],[]),([j['cap']],[])]
   belt_weld_after[j['post']]=sorted(n for n in seams if n.startswith('k72_bant_ayak_kaynagi_'+tag+'_'))
   belt_weld_after[k['insert']]=[k['insert_weld']];belt_weld_after[j['cap']]=[j['cap_weld']]
  operations += [([head],[]),(['bant_traversi_0'],[]),(['bant_traversi_1'],[]),(['tahrik_rulosu_EC5000_354','tahrik_rulosu_EC5000_hex_mil'],[]),(['avara_rulosu_46','avara_mili_0','avara_mili_1'],[]),(['bant_yan_-3'],[]),(['tahrik_rulosu_EC5000_M8_civata'],[]),(['olu_plaka'],[]),(['kayma_tablasi'],[])]
  for rail in ('bant_yan_-421','bant_yan_-3'):belt_weld_after[rail]=[n for j in belt if j['plate']==rail for n in j['plate_welds']]
  assert set(n for names,_ in operations for n in names)==set(members)
  ns['olay'](0.,'UYARI: Geçici tezgâh desteği/fikstürü açık; ön yan sacın rulolar sonrası TIG işleminde ısı koruması ve torç erişimi doğrulanmalı.')
'''
code=code[:start]+new+code[end:]
anchor="  # Separate GLB fragments of one physical source sheet bend together."
assert anchor in code
code=code.replace(anchor,"  if head=='bant_yan_-421':\n   for weld in belt_weld_after.get(a,[]):tt=ns['buyu'](weld,tt,.6)\n"+anchor)
code=code.replace('bench_prototype_audit.json','bottom_bench_prototype_audit.json').replace('bench_plans.pkl','bottom_bench_plans.pkl').replace("HERE/'k_parca.pkl'","HERE/'k_parca_bottom_verified.pkl'")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
