"""Existing v6 benches with four explicit native flush-cap welding operations."""
from pathlib import Path
H=Path(__file__).resolve().parent;variant=H/'catalog_benches.py'
ns=dict(__file__=str(variant),__name__='variant_definition')
prefix=variant.read_text(encoding='utf-8').rsplit("exec(compile(code,str(source),'exec')",1)[0]
exec(compile(prefix,str(variant),'exec'),ns)
code=ns['code'];source=ns['source']
code=code.replace('catalog_station.py','cap_station.py')
anchor=' # The prototype deliberately leaves welding/connection release open.'
assert code.count(anchor)==1
code=code.replace(anchor,""" if head.startswith('kose_dikmesi_'):
  cap=head+'_tapa';assert cap in members
  cap_weld_start=tt
  ns['olay'](tt,'Dikme tapası: serbest dikmenin üstüne oturur; çevresi kesintisiz TIG kaynakla bağlanır. Kaynak taşlanır ve pasive edilir; çıkıntılı ek parça yok.')
  ns['vurgu']([head,cap],tt,tt+1.6)
  tt+=1.6
"""+anchor)
anchor="bench_plans[head]['seconds']=tt"
assert code.count(anchor)==1
code=code.replace(anchor,anchor+"""
 if head.startswith('kose_dikmesi_'):
  bench_plans[head]['native_flush_cap_weld']={'profile':head,'cap':head+'_tapa','t0':cap_weld_start,'t1':tt,'process':'continuous TIG butt weld, grind flush, passivate','fixture_and_torch_access_verified':False}
""")
code=code.replace('catalog_bench_prototype_audit.json','cap_bench_prototype_audit.json').replace('catalog_bench_plans.pkl','cap_bench_plans.pkl')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
