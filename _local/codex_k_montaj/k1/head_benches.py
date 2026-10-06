"""Reuse v6 manufacturing benches for source-bound cutting-head weld group."""
from pathlib import Path
H=Path(__file__).resolve().parent;variant=H/'cap_benches.py'
ns=dict(__file__=str(variant),__name__='variant_definition')
prefix=variant.read_text(encoding='utf-8').rsplit("exec(compile(code,str(source),'exec')",1)[0]
exec(compile(prefix,str(variant),'exec'),ns)
code=ns['code'];source=ns['source']
for old,new in [('k_parca_catalog_verified.pkl','k_parca_head_verified.pkl'),('cap_station.py','head_station.py'),('cap_bench_prototype_audit.json','head_bench_prototype_audit.json'),('cap_bench_plans.pkl','head_bench_plans.pkl')]:code=code.replace(old,new)
anchor=' for names,presses in operations:'
assert code.count(anchor)==1
code=code.replace(anchor,""" if head=='kafa_adaptoru':
  operations=[([head],[])]+[(['ara_dikme_'+str(i)],[]) for i in range(3)]
  ns['olay'](0.,'Kafa alt6mm adaptör lazer kontur/delik ve havşa işlemi; üç dikme alttan fikstüre oturur. Kesintisiz TIG kaynak ve pasivasyon, üst4mm katman ve satın alınmış silindir takılmadan yapılır.')
 if head=='kafa_plakasi_8':
  operations=[([head],[]),(['k79_kafa_ust_plaka_2'],[])]
  ns['olay'](0.,'UYARI: Alt6mm+üst2mm plaka geçici fikstürle hizalanır. Üç M8x20 bağlantı sıkılana kadar fikstür bırakılmaz; bu iki katman arasında kaynak beyanı yok.')
"""+anchor)
anchor="  if '_kanat_vida_' in a:"
assert code.count(anchor)==1
code=code.replace(anchor,"""  if head=='kafa_adaptoru' and a.startswith('ara_dikme_'):
   directions=[ns['YOL']((0,-100,0)),ns['YOL']((0,-300,0))]+directions
  if head=='kafa_plakasi_8' and a=='k79_kafa_ust_plaka_2':
   directions=[ns['YOL']((0,100,0))]+directions
"""+anchor)
anchor=' # The prototype deliberately leaves welding/connection release open.'
assert code.count(anchor)==1
code=code.replace(anchor,""" if head=='kafa_adaptoru':
  for i in range(3):
   seam='k79_kafa_dikme_TIG_'+str(i)
   assert seam in parts
   ns['olay'](tt,'Dikme '+str(i+1)+': çevresinde kesintisiz2mm TIG; adaptör ve dikme fikstürde. Kaynak temizliği ve pasivasyon.')
   tt=ns['buyu'](seam,tt,.6)
"""+anchor)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
