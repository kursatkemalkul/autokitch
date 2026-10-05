# -*- coding: utf-8 -*-
"""sim_topping_v1.py -> sim_makine_v2.py : ARTIK GLB YAZMIYOR.

Kemal: "ana modele uygula, calismani basit sekiller gormek istemiyorum."
Sim kendi (kaba) GLB'sini uretiyordu. Artik hat_montaj_v17'nin urettigi ASIL modul_C.glb
oynatiliyor. Bu dosyanin tek isi kalan: kontrol yazilimin okudugu sim_makine.json.
Yeni alan: ofset = modulun MAKINE koordinatlarindaki basi (durum.json'dan okunur) — cunku
modul_C.glb makine koordinatlarinda, JSON'daki olculer modul-yereli.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "sim_topping_v1.py"), encoding="utf-8").read()

# 1) GLB uretimi ve grup toplama tamamen cikar: kur() govdesinin "--- MAKINE TANIMI" oncesi atilir
i = s.index("def kur():")
j = s.index("    # --- MAKINE TANIMI")
s = s[:i] + "def kur():\n" + s[j:]

# 2) artik gerekmeyen yardimcilar
for blok in ("def grup_modul(ad):", "def ag(wp, tol=0.35, aci=0.7):", "def glb_yaz(yol, gruplar):"):
    a = s.index(blok)
    b = s.index("\ndef ", a + 5)
    s = s[:a] + s[b + 1:]

# 3) MIL_KOT ve Xc/ZT kur() icinde uretiliyordu — geri koy (GLB'siz, sadece kot hesabi)
eski = "def kur():\n    # --- MAKINE TANIMI"
yeni = '''def kur():
    import importlib
    TC.PARCALAR[:] = []; TC.modul()
    MIL_KOT = {}
    for ad, x0, x1, gen in TC.YUVA:                       # kaset mil kotlari kasetin KENDI CAD'inden
        mod = importlib.import_module(TC.KASET_CAD[ad])
        mod.PARCALAR[:] = []; mod.kap()
        MIL_KOT[ad] = dict(helezon=TC.KAS[0] + mod.CY, karistirici=TC.KAS[0] + mod.YC, x=(x0 + x1) / 2.0)
    TB = H.S["tabla"]
    Xc, ZT = 900.0, TC.ZK[0] + 30.0
    ofs = modul_ofseti()

    # --- MAKINE TANIMI'''
assert eski in s
s = s.replace(eski, yeni, 1)

# 4) ofset alani + durum.json okuyucu
eski = "        pide=dict(yaricap=140.0"
yeni = '''        ofset=ofs,                                            # modul_C.glb makine koordinatlarinda
        pide=dict(yaricap=140.0'''
assert eski in s
s = s.replace(eski, yeni, 1)

eski = "def kur():\n    import importlib"
yeni = '''def modul_ofseti():
    """modul_C.glb makine koordinatlarinda yaziliyor; buradaki olculer modul-yereli.
    Farki UYDURMUYORUZ — hat_montaj'in yazdigi durum.json'dan okuyoruz."""
    with io.open(os.path.join(OUT, "durum.json"), encoding="utf-8") as f:
        d = json.load(f)
    b = [x for x in d["birim"] if x["durum"] == "GERCEK_MODUL"]
    assert len(b) == 1, "durum.json'da tek GERCEK_MODUL bekleniyordu, %d var" % len(b)
    return [b[0]["x"][0], b[0]["y"][0], 0.0]


def kur():
    import importlib'''
s = s.replace(eski, yeni, 1)

# 5) basliklar
s = s.replace("sim_topping_v1.glb", "modul_C.glb (hat_montaj_v17)")
io.open(os.path.join(U, "sim_makine_v2.py"), "w", encoding="utf-8").write(s)
print("sim_makine_v2.py yazildi")
