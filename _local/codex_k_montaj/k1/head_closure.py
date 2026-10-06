from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'k_sac_kapalilik.py'
code=source.read_text(encoding='utf-8').replace('current_sheet_bending.json','current_sheet_bending_head.json').replace('physical_sheet_closure_audit.json','physical_sheet_closure_audit_head.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
