"""Name source belt candidate separately; current animation stays unchanged."""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'panel_refresh_raw.py'
code=source.read_text(encoding='utf-8').replace('k_bil_panel.pkl','k_bil_belt.pkl').replace('k_parca_panel_raw.pkl','k_parca_belt_raw.pkl').replace('part_audit_panel_raw.json','part_audit_belt_raw.json').replace('panel_mount_candidate/A/hat3_v10u_ent.json','belt_support_candidate/A/hat3_v10w_ent.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
