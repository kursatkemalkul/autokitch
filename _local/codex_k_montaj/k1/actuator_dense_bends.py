"""Retain source-native bend frames with the new welding timeline."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'bottom_dense_bends.py'
code=source.read_text(encoding='utf-8')
code=code.replace('plan_k_bottom_full.pkl','plan_k_actuator_full.pkl')
code=code.replace('plan_k_bottom_dense.pkl','plan_k_actuator_dense.pkl')
code=code.replace('bottom_dense_bend_morph_audit.json','actuator_dense_bend_morph_audit.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
