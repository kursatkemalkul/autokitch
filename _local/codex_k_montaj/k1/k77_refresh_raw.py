"""Use the existing K naming pipeline on step77 for ownership refresh only.
This raw cache is never the release/animation part cache.
"""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'k_parca.py'
code=source.read_text(encoding='utf-8')
code=code.replace("open('k_bil.pkl', 'rb')", "open('k_bil77.pkl', 'rb')")
code=code.replace('P=apply_verified_surface_names(P)', '# Raw ownership needs a new verified registry before release')
code=code.replace("open('k_parca.pkl', 'wb')", "open('k_parca77_raw.pkl', 'wb')")
code=code.replace('open("part_audit.json","w")','open("part_audit77_raw.json","w")')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
