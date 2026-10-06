"""Bind candidate station geometry to its complete re-extracted source."""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_son_kaynak.py'
code=source.read_text(encoding='utf-8')
for a,b in [('plan_k.pkl','plan_k_bottom_candidate.pkl'),('k_bil.pkl','k_bil_bottom.pkl'),('k_bil.json','k_bil_bottom.json'),('k_parca.pkl','k_parca_bottom_verified.pkl'),('plan_source_binding_audit.json','bottom_plan_source_binding_audit.json')]:code=code.replace(a,b)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
