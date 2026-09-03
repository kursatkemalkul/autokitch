# -*- coding: utf-8 -*-
# v4 -> v5: sogutma grubu GERCEK boyuta (59 -> 25 cm, tezgah alti buzdolabi sinifi),
# kasetler 25 -> 35 cm (4-6 kg), altta ELEKTRIK bolmesi (PLC + 4 step surucu + guc)
import io, re
NL = chr(10)
t = io.open('ist3_topping4.py', encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:70])
    t = t.replace(o, n)

rep("İSTASYON 3 — TOPPING · DETAY v4 (Kemal krokisi + 4 AYRI ÇIKIŞ — ortak nozül YOK)",
    "İSTASYON 3 — TOPPING · DETAY v5 (soğutma gerçek boyut 25 cm · kasetler 35 cm · elektrik bölmesi)")
rep("→ 4 DOLU YEDEK KASET → SOĞUTMA GRUBU (tüm kabin +3 °C)",
    "→ 4 DOLU YEDEK KASET → SOĞUTMA 25 (tezgah altı buzdolabı sınıfı, +3 °C) → ELEKTRİK BÖLMESİ")

# kasetler 250 -> 350
rep("kaset(X0+px(60),Y0+px(28),px(300),px(250),'H3 KAVURMA','(arka)','5,4','#888')", "kaset(X0+px(60),Y0+px(28),px(300),px(350),'H3 KAVURMA','(arka)','5,4','#888')")
rep("kaset(X0+px(400),Y0+px(28),px(300),px(250),'H4 KUŞBAŞI','(arka)','5,4','#888')", "kaset(X0+px(400),Y0+px(28),px(300),px(350),'H4 KUŞBAŞI','(arka)','5,4','#888')")
rep("kaset(X0+px(25),Y0+px(60),px(325),px(250),'H1 KÜP SUCUK','kaset 33×42×25 · 2-4 kg')", "kaset(X0+px(25),Y0+px(60),px(325),px(350),'H1 KÜP SUCUK','kaset 35×42×35 · 4-6 kg')")
rep("kaset(X0+px(350),Y0+px(60),px(325),px(250),'H2 KAŞAR','kaset 33×42×25 · 2-4 kg')", "kaset(X0+px(350),Y0+px(60),px(325),px(350),'H2 KAŞAR','kaset 35×42×35 · 4-6 kg')")

# genel kaydirma (+100) — sadece ON GORUNUS blogu, 310..1250 araligi
def shift(m):
    n = int(m.group(1))
    return 'Y0+px(%d)' % (n + 100) if 310 <= n <= 1250 else m.group(0)
head, sep, tail = t.partition('# ================= UST GORUNUM')
head = re.sub(r'Y0\+px\((\d+)\)', shift, head)
t = head + sep + tail

# yedek kasetler 250 -> 350
rep("kaset(X0+px(60),Y0+px(1000),px(300),px(250),'YEDEK H3'", "kaset(X0+px(60),Y0+px(1000),px(300),px(350),'YEDEK H3'")
rep("kaset(X0+px(400),Y0+px(1000),px(300),px(250),'YEDEK H4'", "kaset(X0+px(400),Y0+px(1000),px(300),px(350),'YEDEK H4'")
rep("kaset(X0+px(25),Y0+px(1030),px(325),px(250),'YEDEK H1'", "kaset(X0+px(25),Y0+px(1030),px(325),px(350),'YEDEK H1'")
rep("kaset(X0+px(350),Y0+px(1030),px(325),px(250),'YEDEK H2'", "kaset(X0+px(350),Y0+px(1030),px(325),px(350),'YEDEK H2'")
rep("not_(X0+px(350),Y0+px(1315),'4 DOLU YEDEK KASET", "not_(X0+px(350),Y0+px(1415),'4 DOLU YEDEK KASET")

# SOGUTMA blogu -> 25 cm + ELEKTRIK bolmesi
start = t.index("# --- SOGUTMA")
end = t.index("# olculer")
sog = [
"# --- SOGUTMA y 1440-1690 (25 cm — tezgah alti buzdolabi sinifi)",
"ln(X0+px(15),Y0+px(1435),X0+px(685),Y0+px(1435),1.2,'#111','7,5')",
"tx(X0+px(350),Y0+px(1470),'SOĞUTMA GRUBU — 25 cm · 1/8 HP ~150 W · +3 °C tüm kabin',9.5,'middle','bold')",
"rc(X0+px(60),Y0+px(1490),px(180),px(170),1.4,3)",
"ci(X0+px(150),Y0+px(1575),px(55),1.2)",
"tx(X0+px(150),Y0+px(1580),'kompresör',8)",
"rc(X0+px(270),Y0+px(1490),px(200),px(170),1.4,3)",
"tx(X0+px(370),Y0+px(1580),'kondenser',8)",
"rc(X0+px(500),Y0+px(1490),px(140),px(170),1.4,3)",
"ci(X0+px(570),Y0+px(1575),px(45),1.1)",
"for k in range(4):",
"    a=k*math.pi/2+0.4",
"    ln(X0+px(570),Y0+px(1575),X0+px(570)+px(40)*math.cos(a),Y0+px(1575)+px(40)*math.sin(a),1.1)",
"tx(X0+px(570),Y0+px(1580)+px(70),'fan',8)",
"not_(X0+px(350),Y0+px(1685),'hesap: hacim ~0,45 m³ · duvar 60 mm PU · ısı yükü &lt; 100 W — buz yok, sadece +3',c='#555')",
"# --- ELEKTRIK y 1700-1850",
"ln(X0+px(15),Y0+px(1700),X0+px(685),Y0+px(1700),1.2,'#111','7,5')",
"tx(X0+px(350),Y0+px(1730),'ELEKTRİK BÖLMESİ — PLC I/O · 4 step sürücü · 24 V güç · tabla sürücüleri',9.5,'middle','bold')",
"rc(X0+px(50),Y0+px(1750),px(150),px(80),1.3,2); tx(X0+px(125),Y0+px(1797),'PLC I/O',8.5)",
"for i in range(4):",
"    rc(X0+px(230+i*70),Y0+px(1750),px(55),px(80),1.2,2); tx(X0+px(257+i*70),Y0+px(1797),'S%d'%(i+1),8)",
"rc(X0+px(530),Y0+px(1750),px(120),px(80),1.3,2); tx(X0+px(590),Y0+px(1797),'24V PSU',8.5)",
"",
]
t = t[:start] + NL.join(sog) + NL + t[end:]

# sag olculer — satir bazli
L2 = t.split(NL)
h1 = [i for i, L in enumerate(L2) if L.startswith("ox(xr,Y0+px(28)")]
h2 = [i for i, L in enumerate(L2) if L.startswith("ox(xr,Y0+px(720)")]
assert len(h1) == 1 and len(h2) == 1, (h1, h2)
L2[h1[0]] = "ox(xr,Y0+px(28),Y0+px(410),'kaset 38',side='r'); ox(xr,Y0+px(460),Y0+px(690),'çark+nozül 23',side='r')"
L2[h2[0]] = "ox(xr,Y0+px(720),Y0+px(960),'tabla+motor 24',side='r'); ox(xr,Y0+px(1000),Y0+px(1430),'yedek 43',side='r'); ox(xr,Y0+px(1440),Y0+px(1690),'soğutma 25',side='r'); ox(xr,Y0+px(1700),Y0+px(1850),'elektrik 15',side='r')"
t = NL.join(L2)

# notlar
rep(" ('· Tüm kabin +3 °C — yağlı küp yapışmaz','#333'),",
    " ('· Tüm kabin +3 °C — yağlı küp yapışmaz','#333')," + NL +
    " ('· Soğutma GERÇEK boyut: 25 cm bant,','#333')," + NL +
    " ('  tezgah altı buzdolabı motoru (1/8 HP);','#666')," + NL +
    " ('  kazanılan yer → kaset 35 cm (4-6 kg)','#666')," + NL +
    " ('  + elektrik bölmesi (PLC, 4 sürücü)','#666'),")
rep("'AUTOKITCH · ist3_topping_detay_v4'", "'AUTOKITCH · ist3_topping_detay_v5'")
rep("ist3_topping_detay_v4.svg", "ist3_topping_detay_v5.svg")
io.open('ist3_topping5.py', 'w', encoding='utf-8', newline='\n').write(t)
print('v5 uretici ok')
