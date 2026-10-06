"""Use the existing decoder/player frames on the bottom-support full plan."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'k_bukum_kareleri.py'
code=source.read_text(encoding='utf-8')
code=code.replace('from k_bukum_ornekle import Decoder','from bottom_bend_samples import Decoder')
anchor='from k_sac_kaynak import load'
assert anchor in code
code=code.replace(anchor,"""_loader_path=H/'k_sac_kaynak.py'
_loader_code=_loader_path.read_text(encoding='utf-8').replace('current_sheet_bending.json','current_sheet_bending_bottom.json').replace('native_sheet_mapping_audit.json','native_sheet_mapping_audit_bottom.json')
_loader_ns=dict(__file__=str(_loader_path),__name__='bottom_loader')
exec(compile(_loader_code,str(_loader_path),'exec'),_loader_ns)
load=_loader_ns['load']""")
for old,new in [('plan_k_full.pkl','plan_k_bottom_full.pkl'),
                ('current_bend_samples.json','bottom_bend_samples.json'),
                ('current_sheet_bending.json','current_sheet_bending_bottom.json'),
                ('plan_k_dense.pkl','plan_k_bottom_dense.pkl'),
                ('dense_bend_morph_audit.json','bottom_dense_bend_morph_audit.json')]:
    code=code.replace(old,new)
# Path substitution already occurred in the injected loader, keep it single.
code=code.replace('current_sheet_bending_bottom_bottom.json','current_sheet_bending_bottom.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__',H=H))
