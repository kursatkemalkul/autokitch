from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'site_bind_plan.py'
code=source.read_text(encoding='utf-8')
code=code.replace('plan_k_site_candidate.pkl','plan_k_mount_candidate.pkl')
code=code.replace('site_plan_source_binding_audit.json','mount_plan_source_binding_audit.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
