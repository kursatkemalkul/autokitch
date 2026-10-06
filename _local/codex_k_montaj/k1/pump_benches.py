"""Reuse checked bottom benches plus three actual oil flat-stock weld groups."""
from pathlib import Path
H=Path(__file__).resolve().parent;variant=H/'bottom_bench_prototype.py'
ns=dict(__file__=str(variant),__name__='variant_definition')
prefix=variant.read_text(encoding='utf-8').rsplit("exec(compile(code,str(source),'exec')",1)[0]
exec(compile(prefix,str(variant),'exec'),ns)
code=ns['code'];source=ns['source']
code=code.replace('k_parca_bottom_verified.pkl','k_parca_pump_verified.pkl')
code=code.replace('bottom_station_candidate.py','pump_station.py')
code=code.replace('.split("exec(compile(code,str(source),\'exec\')")[0]',
                  '.rsplit("exec(compile(code,str(source),\'exec\')",1)[0]')
code=code.replace('bottom_bench_prototype_audit.json','pump_bench_prototype_audit.json')
code=code.replace('bottom_bench_plans.pkl','pump_bench_plans.pkl')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
