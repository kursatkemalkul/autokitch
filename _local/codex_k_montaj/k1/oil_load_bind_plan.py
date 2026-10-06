from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_son_kaynak.py'
code=source.read_text(encoding='utf-8')
for old,new in [('plan_k.pkl','plan_k_oil_load_candidate.pkl'),('k_bil.pkl','k_bil_oil_load.pkl'),
                ('k_bil.json','k_bil_oil_load.json'),('k_parca.pkl','k_parca_oil_load_verified.pkl'),
                ('plan_source_binding_audit.json','oil_load_plan_source_binding_audit.json')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
