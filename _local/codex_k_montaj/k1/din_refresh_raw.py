"""DIN refinement uses separate caches; never overwrite current K state."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'panel_refresh_raw.py';code=source.read_text(encoding='utf-8')
code=code.replace('k_bil_panel.pkl','k_bil_din.pkl').replace('k_parca_panel_raw.pkl','k_parca_din_raw.pkl')
code=code.replace('part_audit_panel_raw.json','part_audit_din_raw.json')
code=code.replace('panel_mount_candidate/A/hat3_v10u_ent.json','din_mount_candidate/A/hat3_v10v_ent.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
