"""Refresh whole-station contact classification on the current combined plan.

Contact classification is a worklist, not certification of a threaded joint.
"""
from pathlib import Path
H=Path(__file__).resolve().parent
source=H/'baglanti_denetim.py'
code=source.read_text(encoding='utf-8')
code=code.replace('plan_k.pkl','plan_k_bottom_full.pkl')
code=code.replace('baglanti_denetim.json','bottom_baglanti_denetim.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
source=H/'k_connection_worklist.py'
code=source.read_text(encoding='utf-8')
for old,new in [('k_parca.pkl','k_parca_bottom_verified.pkl'),
                ('plan_k.pkl','plan_k_bottom_full.pkl'),
                ('baglanti_denetim.json','bottom_baglanti_denetim.json'),
                ('connection_worklist_current.json','bottom_connection_worklist.json')]:
    code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
