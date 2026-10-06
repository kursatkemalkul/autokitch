from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_bench_birlestir.py'
code=source.read_text(encoding='utf-8')
for old,new in [('plan_k.pkl','plan_k_pump_candidate.pkl'),('bench_plans.pkl','pump_bench_plans.pkl'),
                ('k_parca.pkl','k_parca_pump_verified.pkl'),('plan_k_full.pkl','plan_k_pump_full.pkl'),
                ('bench_integration_audit.json','pump_bench_integration_audit.json')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
