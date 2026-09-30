from pathlib import Path
import sys
U=Path(sys.argv[1])/'arastirma'/'_uretec'
old,new=map(int,sys.argv[2:4])
s=(U/f'hat_montaj_v{old}.py').read_text(encoding='utf-8-sig')
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a,s.count(a),n)
    s=s.replace(a,b)
rep('import kutu_cad_v10 as KC','import kutu_cad_v11 as KC')
s=s.replace('kutu_cad_v10.py','kutu_cad_v11.py')
rep('("besleyici_", "itici_")','("besleyici_", "itici_", "vakum_")')
rep('("kalip_", "tepsi_")','("kalip_", "tepsi_", "destek_")')
rep('Besleyici itici: en üstteki blankı 411 mm öne sürer · 2 HGR15 · GT3 · NEMA 23','Vakumlu alma/bırakma: 4 vantuz + 20 mm Z kaldırma + mevcut 411 mm ray; itici çubuk yok')
rep('Zımba kalıbı + 4 çubuklu tepsi (robot çatalı aralardan) · arka ray · ön tarak · ön ray','Kılavuzlu motorlu destek tablası: katlama boyunca tabana temas; son kot 936 korunur')
s=s.replace('12 × STP-DRV-4830','13 × STP-DRV-4830')
rep('"ITICI": lambda t: (0.0, 0.0, KC.itici_dz(t))','"ITICI": lambda t: (0.0, 0.0, KC.feed_z(t)), "VAC_Y": KC.vacuum_trs, "NEST": lambda t: (0,KC.nest_dy(t),0)',2)
s=s.replace(f'hat_v{old}',f'hat_v{new}').replace(f'hat_montaj_v{old}.py',f'hat_montaj_v{new}.py')
s=s.replace(f'pafta="HAT v{old}',f'pafta="HAT v{new}: E v11 VAKUMLU BESLEME + MOTORLU DESTEK TABLASI; KARTON PROTOTIPI. v{old}')
s=s.replace('geometry="E v10: positive-drive corner/front/lid tools; internal drive, aligned supports, flush side door"','geometry="E v11: vacuum pick/place + positively supported forming nest; v10 corner/front/lid tools; prototype"')
s=s.replace('regression="v10 changed-tool solid scan and contact checks stored in kutu_v10_check.py; v9 elevator/frame unchanged"','regression="E v11 changed tools scanned through the cycle; forming-base support contact measured. Results in _local/kutu-v11/check.json"')
s=s.replace('"804x404 assumed die line, no supplier drawing",','"804x404 assumed die line, no supplier drawing", "vacuum flow/porosity, sheet detection, Z cylinder and motion I/O selection pending", "crease springback/corner retention after release must be physically tested",')
compile(s,f'hat_montaj_v{new}.py','exec')
(U/f'hat_montaj_v{new}.py').write_text(s,encoding='utf-8')
print('generated main',new,'from',old)
