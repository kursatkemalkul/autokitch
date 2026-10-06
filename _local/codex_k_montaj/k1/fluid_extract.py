"""Read changed319MB source once, then derive a separate small raw cache."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent
source=H/'k_cikar.py'
argv=sys.argv[:]
sys.argv=[str(source),str(H.parent/'oil_fluid_clamp_candidate/A/hat3_v10zb.glb'),str(H/'k_bil_fluid.pkl')]
try:
 exec(compile(source.read_text(encoding='utf-8'),str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
except SystemExit as error:
 if error.code not in (None,0):raise
finally:sys.argv=argv
source=H/'k_parca.py'
code=source.read_text(encoding='utf-8').replace('k_bil.pkl','k_bil_fluid.pkl').replace('k_parca.pkl','k_parca_fluid_raw.pkl').replace('part_audit.json','fluid_raw_part_audit.json')
anchor='# Native source provides'
assert anchor in code
code=code.replace(anchor,"ENT.update(json.loads((Path(HERE).parent/'oil_fluid_clamp_candidate/A/hat3_v10zb_ent.json').read_text(encoding='utf-8'))['parca'])\n"+anchor)
# Raw names are provisional. Do not apply the canonical old-source registry:
# the dedicated oil triangle rebind must prove every triangle before use.
old_registry='from k_yuz_etiket import apply as apply_verified_surface_names\nP=apply_verified_surface_names(P)'
assert old_registry in code
code=code.replace(old_registry,'# Provisional raw labels; oil_rebind_ownership.py is mandatory.')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
