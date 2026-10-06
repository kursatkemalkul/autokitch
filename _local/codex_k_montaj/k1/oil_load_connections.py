"""Refresh full-source mounting classification without blanket supplier waivers."""
from pathlib import Path
source=Path(__file__).with_name('baglanti_denetim.py')
code=source.read_text(encoding='utf-8').replace('plan_k.pkl','plan_k_oil_load_full.pkl')
code=code.replace('baglanti_denetim.json','oil_load_baglanti_denetim.json')
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
