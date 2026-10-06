from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_bench_birlestir.py'
code=source.read_text(encoding='utf-8')
for old,new in [('plan_k.pkl','plan_k_catalog_candidate.pkl'),('bench_plans.pkl','catalog_bench_plans.pkl'),
                ('k_parca.pkl','k_parca_catalog_verified.pkl'),('plan_k_full.pkl','plan_k_catalog_full.pkl'),
                ('bench_integration_audit.json','catalog_bench_integration_audit.json')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
