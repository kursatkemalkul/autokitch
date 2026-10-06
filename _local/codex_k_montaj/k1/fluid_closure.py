from pathlib import Path
source=Path(__file__).with_name('k_sac_kapalilik.py')
code=source.read_text(encoding='utf-8').replace('current_sheet_bending.json','current_sheet_bending_fluid.json')
code=code.replace('physical_sheet_closure_audit.json','physical_sheet_closure_audit_fluid.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
