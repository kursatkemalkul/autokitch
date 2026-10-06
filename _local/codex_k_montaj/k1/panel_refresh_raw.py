"""Reuse existing extraction/name code in separate panel candidate caches."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'k_parca.py';code=source.read_text(encoding='utf-8')
code=code.replace("open('k_bil.pkl', 'rb')","open('k_bil_panel.pkl', 'rb')")
anchor="ENT.update(json.loads((Path(HERE)/'k_local_ent.json').read_text(encoding='utf-8'))['parca'])"
assert anchor in code
code=code.replace(anchor,anchor+"\nENT.update(json.loads((Path(HERE).parent/'panel_mount_candidate/A/hat3_v10u_ent.json').read_text(encoding='utf-8'))['parca'])")
code=code.replace('P=apply_verified_surface_names(P)','# Candidate requires its own one-to-one rebind')
code=code.replace("open('k_parca.pkl', 'wb')","open('k_parca_panel_raw.pkl', 'wb')")
code=code.replace('open("part_audit.json","w")','open("part_audit_panel_raw.json","w")')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
