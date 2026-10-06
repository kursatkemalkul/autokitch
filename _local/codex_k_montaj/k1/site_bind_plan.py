"""Bind site-weld timing variant to unchanged complete source geometry."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'bottom_bind_plan.py'
code=source.read_text(encoding='utf-8')
code=code.replace('plan_k_bottom_candidate.pkl','plan_k_site_candidate.pkl')
code=code.replace('bottom_plan_source_binding_audit.json','site_plan_source_binding_audit.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
