"""Rebind full candidate geometry after endpoint rails and12 fasteners."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'panel_rebind_ownership.py';code=source.read_text(encoding='utf-8')
code=code.replace('k_parca_panel_raw.pkl','k_parca_din_raw.pkl').replace('k_parca_panel_verified.pkl','k_parca_din_verified.pkl')
code=code.replace('panel_ownership_rebind_audit.json','din_ownership_rebind_audit.json')
code=code.replace('surface_ownership_registry_panel.json','surface_ownership_registry_din.json')
code=code.replace('panel_mount_candidate','din_mount_candidate').replace('hat3_v10u','hat3_v10v')
# Keep previous canonical metadata from the verified panel refinement,
# not the older849-part active animation cache.
anchor="code=source.read_text(encoding='utf-8')"
assert anchor in code
code=code.replace(anchor,anchor+"\ncode=code.replace(\"previous_path=H/'k_parca.pkl'\",\"previous_path=H/'k_parca_panel_verified.pkl'\")")
code=code.replace('REBIND_PANEL','REBIND_DIN')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
