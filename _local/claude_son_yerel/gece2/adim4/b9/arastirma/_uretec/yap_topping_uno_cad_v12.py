# -*- coding: utf-8 -*-
"""topping_uno_cad_v11.py -> topping_uno_cad_v12.py (27 Eyl 2026 gece) · SOĞUK ODANIN ALTINA YALITIM
Kemal: "yap dediğini, altına da az da olsa yalıtım yap". v4'te 134 mm PU taban kalkmış, yerine yalnız 3 mm taşıyıcı raf kalmıştı
(soğuk odanın tabanı yalıtımsızdı). v12: rafın ALTINA, ön ve arka 40 mm bükümlerin ARASINA sac kaplı PU (alt sac 1 + PU 39) —
raf, disk ve hat kotları DEĞİŞMEZ. Rafın altından geçen her parça (UNO ağızları, kaset iniş boruları + hunileri, hava delikleri)
için yalıtımda boşluklu delik açılır; kaset boruları öne çekildiği için onların deliği öne AÇIK yarık. Delikler denetimde listelenir.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v11.py"), encoding="utf-8").read()
NL = "\n"


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120])
    s = s.replace(a, b)


degis('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v11 · 27 Eyl 2026 (v10 + YALITIM YALNIZ SOĞUK HACMİ SARAR, teknik cep dışarıda — Kemal)',
      '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v12 · 27 Eyl 2026 gece (v11 + SOĞUK ODANIN ALTINA YALITIM — Kemal: "altına da az da olsa yalıtım yap")' + NL +
      'v12: rafın altına, ön ve arka bükümlerin arasına alt sac 1 + PU 39 (y 1277–1317) · raf / disk / hat kotları aynı · rafın altından geçen parçalara' + NL +
      '    boşluklu delik (kaset borularına öne açık yarık) · soğuk oda tabanı artık yalıtımlı. Önceki: topping_uno_cad_v11.py (yap_topping_uno_cad_v12.py)' + NL +
      'v11 (27 Eyl):')

ALT = '''
# ================================================================ v12 · SOĞUK ODANIN ALTI: sac kaplı PU (Kemal: "altına da az da olsa yalıtım yap")
#   rafın (1317–1320) altı, ön büküm (z −107…−104) ile arka büküm (z −565…−562) arası, x 90–1710 (yan PU duvarlar 1277'den başlar → birleşir)
#   alt sac 1 (1277–1278) + PU 39 (1278–1317) · kalın taban geri gelmez: raf, disk ve hat kotları aynı
ALT_YAL = (BAY_A[0], BAY_B[1], YAL_Y0, SOGUK_TABAN - RAF_T, Z_BOLME[0] + RAF_T, Z_KAPAK[1] - RAF_T)   # x · y 1277–1317 · z −562…−107
ALT_PAY = 3.0
_alt = kut(*ALT_YAL)
ALT_DELIK = []
_ab = _alt.val().BoundingBox()
for p in P:
    if p["ad"].startswith(("tasiyici_raf", "raf_", "yalitim_blogu", "kabin_", "baglam", "kompresor", "hava_ana", "teknik_bant", "pide", "tabla_diski")):
        continue
    b_ = p["sh"].BoundingBox()
    if not (b_.xmin < _ab.xmax and _ab.xmin < b_.xmax and b_.ymin < _ab.ymax and _ab.ymin < b_.ymax and b_.zmin < _ab.zmax and _ab.zmin < b_.zmax):
        continue
    try:
        _k = _alt.val().intersect(p["sh"]); v_ = abs(_k.Volume()); lb = _k.BoundingBox() if v_ > 0.5 else None
    except Exception:
        v_, lb = 1.0, None
    if v_ <= 0.5 and not p["ad"].endswith("hava_hortumu"):
        continue
    if lb is not None and lb.xlen > 0.1:
        b_ = lb                                                                               # delik yalnız yalıtımın İÇİNDEKİ kısım kadar
    kaset = any(p["ad"].startswith(m_) for _a, m_, _x0, _x1 in KASET) or p["ad"].startswith(("kasar_inis", "sucuk_inis"))
    z1_ = ALT_YAL[5] + 1.0 if kaset else b_.zmax + ALT_PAY                                   # kaset: öne çekilir → yarık öne açık
    ALT_DELIK.append((p["ad"], b_.xmin - ALT_PAY, b_.xmax + ALT_PAY, b_.zmin - ALT_PAY, z1_))
for _ad, x0_, x1_, z0_, z1_ in ALT_DELIK:
    _alt = _alt.cut(kut(x0_, x1_, ALT_YAL[2] - 1.0, ALT_YAL[3] + 1.0, z0_, z1_))
ekle("alt_yalitim_saci", _alt.intersect(kut(ALT_YAL[0], ALT_YAL[1], ALT_YAL[2], ALT_YAL[2] + 1.0, ALT_YAL[4], ALT_YAL[5])).val(), "paslanmaz", "V",
     not_="v12 · AISI 304 1,0 · soğuk oda yalıtımının alt kabuğu (aşağı bakar, pişirme bölgesinin üstü) · rafın bükümlerine perçin")
ekle("alt_yalitim_PU", _alt.intersect(kut(ALT_YAL[0], ALT_YAL[1], ALT_YAL[2] + 1.0, ALT_YAL[3], ALT_YAL[4], ALT_YAL[5])).val(), "pu", "V",
     not_="v12 · PU 39 (40 kg/m³) · rafın altı, bükümlerin arası · kaset / UNO / hava geçişlerinde 3 mm boşluklu delik (kaset yarıkları öne açık)")

'''
k = "# ================================================================ 5 · DENETİM"
degis(k, ALT.lstrip(NL) + k)
KON = '''
_ay = bb("alt_yalitim_PU"); _as = bb("alt_yalitim_saci")
kontrol("v12 · soğuk oda ALTI yalıtımlı: alt sac y %.0f–%.0f + PU y %.0f–%.0f (39) · x %.0f–%.0f · z %.0f…%.0f · %d geçiş deliği"
        % (_as.ymin, _as.ymax, _ay.ymin, _ay.ymax, _ay.xmin, _ay.xmax, _ay.zmin, _ay.zmax, len(ALT_DELIK)),
        abs(_ay.ymax - (SOGUK_TABAN - RAF_T)) < 0.01 and abs(_as.ymin - YAL_Y0) < 0.01 and _ay.xmin == BAY_A[0] and _ay.xmax == BAY_B[1])
for _ad, x0_, x1_, z0_, z1_ in ALT_DELIK:
    print("     alt yalıtım deliği: %-34s x %.0f–%.0f · z %.0f…%.0f (%.0f × %.0f)" % (_ad, x0_, x1_, z0_, z1_, x1_ - x0_, z1_ - z0_))
_ya = sum((x1_ - x0_) * (z1_ - z0_) for _a, x0_, x1_, z0_, z1_ in ALT_DELIK) / ((BAY_B[1] - BAY_A[0]) * (ALT_YAL[5] - ALT_YAL[4]))
kontrol("v12 · alt yalıtımın delik payı (üst üste binenler dahil kaba) %%%.0f ≤ %%25" % (100 * _ya), _ya <= 0.25)
_ka = 0
for _yn in ("alt_yalitim_PU", "alt_yalitim_saci"):
    _ys = [q for q in P if q["ad"] == _yn][0]["sh"]
    for p in P:
        if p["ad"] in ("alt_yalitim_PU", "alt_yalitim_saci") or p["ad"].startswith(("baglam", "kompresor", "hava_ana")): continue
        try:
            if p["sh"].intersect(_ys).Volume() > 1.0: _ka += 1; print("   alt yalıtıma giren:", p["ad"])
        except Exception: pass
kontrol("v12 · alt yalıtıma hiçbir parça girmiyor", _ka == 0, "%d" % _ka)
'''
k = "# ================================================================ 6 · ANİMASYON + GLB"
degis(k, KON.lstrip(NL) + NL + k)
degis('glb_yaz(os.path.join(OUT, "topping_uno_v11.glb"))', 'glb_yaz(os.path.join(OUT, "topping_uno_v12.glb"))')
degis('open(os.path.join(OUT, "topping_uno_v11.json"), "w"', 'open(os.path.join(OUT, "topping_uno_v12.json"), "w"')
degis('surum="topping_uno_cad_v11 · %s"', 'surum="topping_uno_cad_v12 · %s"')
io.open(os.path.join(U, "topping_uno_cad_v12.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v12.py yazildi")
