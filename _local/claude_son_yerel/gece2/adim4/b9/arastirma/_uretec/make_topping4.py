# -*- coding: utf-8 -*-
# sw_topping4.py ureteci: sw_topping3.py'den turetilir, v3'e DOKUNULMAZ. Yeni klasor 3_TOPPING_v4.
#
# TEK DEGISIKLIK (12 Eyl 2026, Kemal karari "agir kaldiran robot"):
#   Kaset celik parcalari DOLU cubuktan BORU'ya cevriliyor ki robot kaseti dolu tasiyabilsin.
#     KAPD_tarak_gobek_304_D30    O30 DOLU (3,53 kg) -> O30x2 BORU (ic O26)  = 0,88 kg
#     KAPD_helezon_mili_304_D20   O20 DOLU (1,65 kg) -> O20x3 BORU (ic O14)  = 0,84 kg
#   Bos kaset 11,01 -> 7,55 kg · dolu (harc) 23,76 -> 20,30 kg
#   Burulma: gobek %44, mil %76 rijitlik kalir. Gobek 10 W tarak motoru tasiyor (yeterli),
#   mil NEMA17 dozaj torkunu tasiyor (%76 yeterli). Kendi agirligiyla sehim degismiyor
#   (kutle ve atalet ayni oranda dusuyor).
# Geometri disinda hicbir sey degismedi: 14 yuva, kap kesiti, LAYOUT, klape, tahrik arayuzu ayni.
import io, os

S = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec\sw_topping3.py".replace("WEBSITE", "WEBS\u0130TE")
D = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec\sw_topping4.py".replace("WEBSITE", "WEBS\u0130TE")
s = io.open(S, encoding="utf-8").read()


def rep(a, b, n=1):
    global s
    assert a in s, "YOK: " + a[:90]
    s = s.replace(a, b, n)


# ---------- baslik ----------
i = s.index("import sys, os, math, time")
s = """# -*- coding: utf-8 -*-
# AUTOKITCH - 3 · TOPPING v4 (12 Eyl 2026) - KASET CELIGI BORU   (v3 = 3_TOPPING, dokunulmadi)
#
# KARAR (Kemal, 12 Eyl): robot 20 kg sinifi kobot (Fairino FR20 tipi) olacak, kaset KUCULTULMEYECEK.
# Robotun dolu kaseti tasiyabilmesi icin kasetin celik parcalari boruya cevrildi:
#     tarak gobegi  O30 DOLU 625 mm  3,53 kg  ->  O30x2 boru  0,88 kg
#     helezon mili  O20 DOLU 655 mm  1,65 kg  ->  O20x3 boru  0,84 kg
#     BOS KASET 11,01 -> 7,55 kg   ·   DOLU (harc 12,5 L) 23,76 -> 20,30 kg
# FR20 net tasima 16,5 kg (20 - 3,5 el) -> harc kaseti 8,8 L'ye kadar dolduruluyor, 4 kaset/3 gun.
# 14 yuvanin 11'i kullaniliyor. Kabin, kap kesiti, LAYOUT, klape, tahrik arayuzu AYNEN v3.
#
""" + s[i:]

# ---------- klasor ----------
rep('ROOT = os.path.join(ARA, "3_TOPPING"); ALT = os.path.join(ROOT, "alt_montaj")',
    'ROOT = os.path.join(ARA, "3_TOPPING_v4"); ALT = os.path.join(ROOT, "alt_montaj")')

# ---------- 1) tarak gobegi: DOLU -> BORU O30x2 ----------
rep('''    st.part(p+"tarak_gobek_304_D30", [(FR,'circ',(0,YD,15), -685.0, -60.0, False)])''',
    '''    st.part(p+"tarak_gobek_304_D30x2_BORU", [(FR,'circ',(0,YD,15), -685.0, -60.0, False),
                                             (FR,'circ',(0,YD,13), -686.0, -59.0, True)])   # ic O26 -> BORU''')

# ---------- 2) helezon mili: DOLU -> BORU O20x3 ----------
rep('''    st.part(p+"helezon_mili_304_D20",   [(FR,'circ',(0,YT,10), ZB, -45.0, False)])''',
    '''    st.part(p+"helezon_mili_304_D20x3_BORU", [(FR,'circ',(0,YT,10), ZB, -45.0, False),
                                              (FR,'circ',(0,YT,7), ZB-1.0, -44.0, True)])   # ic O14 -> BORU''')

# ---------- montaj adi ----------
rep('st.assemble("TOPPING")', 'st.assemble("TOPPING")')

io.open(D, "w", encoding="utf-8").write(s)
print("sw_topping4.py yazildi ->", D)
print("degisen parca: KAPD_tarak_gobek_304_D30x2_BORU · KAPD_helezon_mili_304_D20x3_BORU")
