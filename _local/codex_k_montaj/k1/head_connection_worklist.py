from pathlib import Path
source=Path(__file__).with_name('k_connection_worklist.py')
code=source.read_text(encoding='utf-8')
for old,new in [('connection_worklist.json','mount_connection_worklist.json'),
                ('k_parca.pkl','k_parca_head_verified.pkl'),
                ('baglanti_denetim.json','head_baglanti_denetim.json'),
                ('plan_k.pkl','plan_k_head_full.pkl'),
                ('connection_worklist_current.json','head_connection_worklist.json')]:code=code.replace(old,new)
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
