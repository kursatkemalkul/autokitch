"""Compose current bottom-support bench and station plans without changing canonical files."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'k_bench_birlestir.py'
code=source.read_text(encoding='utf-8')
for old,new in [('plan_k.pkl','plan_k_bottom_candidate.pkl'),
                ('bench_plans.pkl','bottom_bench_plans.pkl'),
                ('k_parca.pkl','k_parca_bottom_verified.pkl'),
                ('plan_k_full.pkl','plan_k_bottom_full.pkl'),
                ('bench_integration_audit.json','bottom_bench_integration_audit.json')]:
    assert old in code
    code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
