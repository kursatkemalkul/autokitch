"""Run the unchanged naming pipeline into a separate stage79 raw cache."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'k_parca.py';code=source.read_text(encoding='utf-8')
code=code.replace("open('k_bil.pkl', 'rb')", "open('k_bil79.pkl', 'rb')")
code=code.replace('P=apply_verified_surface_names(P)', '# Stage79 registry must be rebound before use')
code=code.replace("open('k_parca.pkl', 'wb')", "open('k_parca79_raw.pkl', 'wb')")
code=code.replace('open("part_audit.json","w")','open("part_audit79_raw.json","w")')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
