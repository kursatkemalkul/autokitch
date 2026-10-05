# -*- coding: utf-8 -*-
# v23 -> v24: + normal UST GORUNUM (kat 1 / kat 2 / kat 3 / ALT planlari) · ALT sira duzeltmesi (zf 8 / 35, evaporator 62-74) · TEK render
import io
NL = chr(10)
t = io.open('ist3_topping23.py', encoding='utf-8').read()
def rep(o,n,c=1):
    global t
    assert t.count(o)==c, 'A(%d): %s' % (t.count(o), o[:70])
    t = t.replace(o,n)
rep("W, H = 1460, 1190", "W, H = 1460, 1560")
rep("TOPPING v23 (5 Eyl 2026) — TEK KAP TİPİ", "TOPPING v24 (5 Eyl 2026) — TEK KAP TİPİ")
rep("ALT 8 beşik · 70×197×84',15,'start','bold')", "ALT 8 beşik · + ÜST GÖRÜNÜM · 70×197×84',15,'start','bold')")
# ALT sira duzeltmesi: izometrik + on kesit
rep("for row,zf in ((0,9),(1,30)):", "for row,zf in ((0,8),(1,35)):", 2)
rep("ipoly([(0,0,52),(70,0,52),(70,58,52),(0,58,52)],.9,'#7fb3d5',ICE,None,.6)", "ipoly([(0,0,62),(70,0,62),(70,58,62),(0,58,62)],.9,'#7fb3d5',ICE,None,.6)")
rep("ipoly([(0,0,72),(70,0,72),(70,58,72),(0,58,72)],.9,'#7fb3d5',ICE,None,.5)", "ipoly([(0,0,74),(70,0,74),(70,58,74),(0,58,74)],.9,'#7fb3d5',ICE,None,.5)")
rep("t=P(35,20,62); tx(t[0],t[1],'evaporatör + fan · soğuk hava arka duvar kanalından katlara',5.6,'middle','',BLU)", "t=P(35,20,68); tx(t[0],t[1],'evaporatör + fan (12) · soğuk hava arka duvar kanalından katlara',5.6,'middle','',BLU)")
rep("ipoly([(2,58,0),(68,58,0),(68,58,50),(2,58,50)],1,'#555','#cfd8dc',None,.95)", "ipoly([(2,58,0),(68,58,0),(68,58,62),(2,58,62)],1,'#555','#cfd8dc',None,.95)")
rep("ipoly([(2,58,50),(68,58,50),(68,74,50),(2,74,50)],1,'#555','#b0bec5',None,.95)", "ipoly([(2,58,62),(68,58,62),(68,74,62),(2,74,62)],1,'#555','#b0bec5',None,.95)")
rep("ipoly([(68,58,0),(68,74,0),(68,74,50),(68,58,50)],1,'#555','#c0cbd1',None,.95)", "ipoly([(68,58,0),(68,74,0),(68,74,62),(68,58,62)],1,'#555','#c0cbd1',None,.95)")
rep("rc(XC,YC+K*(197-74),K*70,K*22,.7,0,'#7fb3d5',None,ICE); tx(XC+K*35,YC+K*(197-63),'evaporatör + fan',4.8,'middle','',BLU)",
    "rc(XC,YC+K*(197-74),K*70,K*12,.7,0,'#7fb3d5',None,ICE); tx(XC+K*35,YC+K*(197-67),'evaporatör + fan 12',4.8,'middle','',BLU)")
rep("t=P(0,-2,42); tx(t[0]-6,t[1]+8,'ALT 74: 2 sıra × 4 beşik (U yatak, tek tip) + arkada soğutma',6.5,'end','bold',GRY)",
    "t=P(0,-2,42); tx(t[0]-6,t[1]+8,'ALT 74 = plint 8 + 2 sıra × 27 beşik + evaporatör 12 · arkada soğutma',6.5,'end','bold',GRY)")
# UST GORUNUM paneli (alt satir)
ust = [
"# ================= ÜST GÖRÜNÜM (normal plan) — kat 1 / kat 2 / kat 3 / ALT =================",
"YU=1230",
"rc(40,YU-30,1390,340,1.4,4)",
"tx(56,YU-8,'ÜST GÖRÜNÜM (plan) — her kat 70 × 84 · arka duvar 10 (motorlar) · klape 4 önde · kaplar y 4-58 (önden) · süpürme R 27 kesikli yeşil',10,'start','bold')",
"KU=2.2",
"def plan(X,Y,ad,kaplar,alt=False):",
"    tx(X+KU*35,Y-6,ad,7.5,'middle','bold')",
"    rc(X,Y,KU*70,KU*84,1.3)",
"    rc(X,Y,KU*70,KU*10,.8,0,'#555',None,'#d9d9d9'); tx(X+KU*35,Y+KU*6.5,'arka duvar: motor + elektrik',4.4,'middle','','#333')",
"    if alt:",
"        rc(X+KU*2,Y+KU*10,KU*66,KU*16,.9,0,'#555',None,'#cfd8dc'); tx(X+KU*35,Y+KU*19,'SOĞUTMA GRUBU (20 derin)',4.8,'middle','bold','#37474f')",
"        for i,lab in enumerate(('park','park','çöz. kıyma','çöz. kuşbaşı')):",
"            x0=1.2+i*17.2",
"            rc(X+KU*x0,Y+KU*26,KU*16,KU*54,1,1,'#555',None,'#e4e0d4'); ln(X+KU*(x0+8),Y+KU*28,X+KU*(x0+8),Y+KU*78,1,BLU,'3,2')",
"            tx(X+KU*(x0+8),Y+KU*50,lab,4.4,'middle','bold','#444'); tx(X+KU*(x0+8),Y+KU*58,'(üstte kaşar yd)',3.8,'middle','','#777')",
"        rc(X,Y+KU*80,KU*70,KU*4,.9,0,'#555',None,'#9e9e9e'); tx(X+KU*35,Y+KU*83,'plint ızgarası',3.8,'middle','','#fff')",
"        return",
"    for (x0,nm,bos) in kaplar:",
"        col='#999' if bos else '#111'; d='3,2' if bos else None",
"        rc(X+KU*x0,Y+KU*26,KU*16,KU*54,1.1,1,col,d,LIGHT if bos else PE)",
"        if not bos:",
"            ln(X+KU*(x0+8),Y+KU*28,X+KU*(x0+8),Y+KU*78,1.4,GRN); ln(X+KU*(x0+8),Y+KU*10,X+KU*(x0+8),Y+KU*26,1,BLU,'3,2')",
"            ci(X+KU*(x0+8),Y+KU*78,2.6,1.3,GRN,None,'#fff'); ci(X+KU*(x0+8),Y+KU*78,KU*27,.8,GRN,'4,3')",
"            rc(X+KU*(x0+5),Y+KU*2,KU*6,KU*6,.9,1,BLU,None,'#dfe7fb')",
"        tx(X+KU*(x0+8),Y+KU*44,nm,5,'middle','bold','#888' if bos else '#111'); tx(X+KU*(x0+8),Y+KU*52,'boş' if bos else '16×54',4.2,'middle','','#888' if bos else '#333')",
"    rc(X,Y+KU*80,KU*70,KU*4,.9,0,BLU,None,'#dfe7fb'); tx(X+KU*35,Y+KU*83,'klape',3.8,'middle','',BLU)",
"    tx(X+KU*27,Y+KU*81.5,'x 27',3.6,'middle','bold',GRN); tx(X+KU*43,Y+KU*81.5,'x 43',3.6,'middle','bold',GRN)",
"plan(60,YU+30,'KAT 1 (z 170-197) — sucuklu-kaşarlı düzlemi',[(19,'KAŞAR A',False),(35,'SUCUK',False)])",
"plan(280,YU+30,'KAT 2 (z 129-156) — kaşarlı düzlemi',[(19,'KAŞAR B',False),(35,'boş / kavurma',True)])",
"plan(500,YU+30,'KAT 3 (z 88-115) — kıymalı / kuşbaşılı',[(19,'KIYMA',False),(35,'KUŞBAŞI',False)])",
"plan(720,YU+30,'ALT (z 0-74) — beşikler + soğutma',[],True)",
"nx,ny_=960,YU+36",
"for i,(s,c,fw) in enumerate([('Kaplar her katta aynı yerde: x 19-35 (merkez 27) ve x 35-51 (merkez 43) — dolabın orta 32 cm'+chr(39)+'i; yanlarda 19 cm boş (hava kanalı, kablo, ray).','#333',''),",
"                              ('Ağızlar kabın ön ucunda y 78 (arka duvardan) → süpürme R 27: sol kap x 0-54 / y 51-105, sağ kap x 16-70 — yan duvarlar düz.',GRN,'bold'),",
"                              ('Helezon (yeşil) kabın ortasında arkadan öne, arka uçta pençe → arka duvardaki motora (mavi kesikli ara mil).','#333',''),",
"                              ('Klape önde 4 cm, her kat ayrı; robot kabı önden çeker/iter. Yan 19 cm boşluklar kapalı panel (soğuk hacim).','#333',''),",
"                              ('ALT: soğutma grubu arka 20 cm (y 10-26), 4 beşik y 26-80 iki sırada (alt: park ×2 + çözülme ×2, üst: kaşar yedeği ×4), plint ızgarası önde.','#333',''),",
"                              ('STORE −18: 3 kap/modül (kıyma 2, kuşbaşı 2). Kaşar yedekleri +3'+chr(39)+'te ALT üst sırada.','#333',''),",
"                              ('HAT v45: TOPPING bloğu bu haliyle, KONTROL ⑦ ✓ (kol ≤ 13 kg), ⑫ tepsi Ø32 zinciri açık.',BLU,'bold')]):",
"    tx(nx,ny_+i*15.5,s,6.2,'start',fw,c)",
"",
]
rep("tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v23 · 5 Eyl 2026',7,'end','',GRY)",
    NL.join(ust) + NL + "tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v24 · 5 Eyl 2026',7,'end','',GRY)")
rep("ist3_topping_detay_v23.svg", "ist3_topping_detay_v24.svg")
io.open('ist3_topping24.py','w',encoding='utf-8',newline='\n').write(t)
print('v24 uretici ok')
