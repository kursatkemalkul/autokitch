"""Compare real connection timing after site welds moved to carrier arrival."""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'bottom_connection_classify.py'
code=source.read_text(encoding='utf-8')
code=code.replace('plan_k_bottom_full.pkl','plan_k_actuator_full.pkl')
code=code.replace('bottom_baglanti_denetim.json','actuator_baglanti_denetim.json')
code=code.replace('bottom_connection_worklist.json','actuator_connection_worklist.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
