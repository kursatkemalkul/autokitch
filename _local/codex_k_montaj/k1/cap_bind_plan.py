from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_son_kaynak.py'
code=source.read_text(encoding='utf-8')
for old,new in [('plan_k.pkl','plan_k_cap_candidate.pkl'),('k_bil.pkl','k_bil_catalog.pkl'),
                ('k_bil.json','k_bil_catalog.json'),('k_parca.pkl','k_parca_catalog_verified.pkl'),
                ('plan_source_binding_audit.json','cap_plan_source_binding_audit.json')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
