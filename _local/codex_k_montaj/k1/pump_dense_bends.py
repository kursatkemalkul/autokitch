"""Use the existing decoder/player frames on the pump-support full plan."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'k_bukum_kareleri.py'
code=source.read_text(encoding='utf-8')
code=code.replace('from k_bukum_ornekle import Decoder','from pump_bend_samples import Decoder')
anchor='from k_sac_kaynak import load'
assert anchor in code
code=code.replace(anchor,"""_loader_path=H/'k_sac_kaynak.py'
_loader_code=_loader_path.read_text(encoding='utf-8').replace('current_sheet_bending.json','current_sheet_bending_pump.json').replace('native_sheet_mapping_audit.json','native_sheet_mapping_audit_pump.json')
_loader_ns=dict(__file__=str(_loader_path),__name__='pump_loader')
exec(compile(_loader_code,str(_loader_path),'exec'),_loader_ns)
load=_loader_ns['load']""")
for old,new in [('plan_k_full.pkl','plan_k_pump_full.pkl'),
                ('current_bend_samples.json','pump_bend_samples.json'),
                ('current_sheet_bending.json','current_sheet_bending_pump.json'),
                ('plan_k_dense.pkl','plan_k_pump_dense.pkl'),
                ('dense_bend_morph_audit.json','pump_dense_bend_morph_audit.json')]:
    code=code.replace(old,new)
# Path substitution already occurred in the injected loader, keep it single.
code=code.replace('current_sheet_bending_pump_pump.json','current_sheet_bending_pump.json')
code=code.replace("assert len(m['seg'])==n", "assert len(m['seg'])==n,(a,record['name'],len(m['seg']),n)")
code=code.replace(".replace('current_sheet_bending_pump.json','current_sheet_bending_pump.json')", ".replace('current_sheet_bending.json','current_sheet_bending_pump.json')")
try:
 exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__',H=H))
except AssertionError as error:
 import traceback
 tb=error.__traceback__
 while tb.tb_next:tb=tb.tb_next
 q=tb.tb_frame.f_locals
 print('DENSE_DIAGNOSTIC',q.get('a'),q.get('n'),q.get('m'),q.get('record',{}).get('name'),error.args,flush=True)
 raise
