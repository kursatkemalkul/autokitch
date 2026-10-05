# -*- coding: utf-8 -*-
"""store_cad_v9 → store_cad_v10 (29 Eyl 2026) — Kemal: "kolaları normal hamurlar gibi yap, parmaklarıyla robot alsın" · "evet yap, birde simetri,
her şeyin çok basit gözükmesi benim için önemli".
1 · STROK 628 → 700: avara −73 → −1 (çene ön kenarı avara flanşına yine 3 mm). Ray AYNI (Accuride DZ3832-0070, 700 = %100 açılır).
2 · BÜTÜN İÇERİK TEPSİDE (silikon, çukurlu) — robot parmakla alır, yaylı itici + şerit YOK:
      lahmacun 6 × 7 = 42 (hatve 88 × 85) · pide 5 × 5 = 25 (105 × 120) · içecek 6 × 8 = 48 kutu 330 (82 × 76) · tatlı 4 × 3 = 12 (105 × 120)
3 · 2 GÜN KURALI (en az çekmece, fazlası yok): lahmacun 10 (420 ≥ 400) · pide 7 (175 ≥ 160) · içecek 3 (144 ≥ 139) · tatlı 1 (12 ≥ 11) = 21 çekmece (v9: 24)
4 · SİMETRİ: K1 · K2 · K3 = 5'er çekmece, AYNI açıklık (75) ve AYNI ön çizgileri · K5 · K6 = 3'er çekmece, AYNI açıklık (130) ve ön çizgileri.
5 · BÜTÜN KUTULAR 540 (tek parça no) · K2 / K5 fan önü payı 9 / 29 → 19 mm.
Önceki: store_cad_v9.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v9.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v9 (28 Eyl 2026 akşam · yap_store_cad_v9.py)',
      '"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v10 (29 Eyl 2026 · yap_store_cad_v10.py): STROK 700 · HER ŞEY TEPSİDE (robot parmakla alır, itici yok) ·'
      ' 21 çekmece (lahmacun 10 × 42 · pide 7 × 25 · içecek 3 × 48 · tatlı 1 × 12) · SİMETRİ: K1–K3 5\'er aynı çizgide, K5–K6 3\'er aynı çizgide · kutular 540' + NL +
      'v9: ÜRETİM MODELİ v9 (28 Eyl 2026 akşam · yap_store_cad_v9.py)')
# ---- 3/4 · dağılım + simetri: kolon başına tek açıklık yüksekliği ve başlangıç kotu ----
degis('KOLON = [[(6, "lahm")], [(6, "lahm")], [(5, "hamur")], [(3, "hamur"), (1, "tatli")], [(3, "ic1")]]   # K5 alttan üste: pide, pide, pide, tatlı',
      'KOLON = [[(5, "lahm")], [(5, "lahm")], [(5, "hamur")], [(2, "hamur"), (1, "tatli")], [(3, "ic1")]]   # v10: K5 alttan üste: pide, pide, tatlı' + NL +
      '# v10 · SİMETRİ (Kemal): kolon grubunda HER çekmecenin açıklığı aynı → ön çizgileri kolonlar arasında hizalı. En alt ve en üst ön eşit olacak şekilde başlangıç kotu:' + NL +
      '#       K1–K3: 5 × (75 + 33) = 540 ≤ 558 → başlangıç 200,5 (alt ön 164,5 · orta 105 · üst 167,5) · K5–K6: 3 × (130 + 33) = 489 ≤ 498 → 191,5 (üstü fırın ısı kalkanı: 60 fazla)' + NL +
      'HH_KOL = {"K1": 75.0, "K2": 75.0, "K3": 75.0, "K5": 130.0, "K6": 130.0}' + NL +
      'Y0_KOL = {"K1": 200.5, "K2": 200.5, "K3": 200.5, "K5": 191.5, "K6": 191.5}')
degis('        yo, n = YUZ0 + BIND, {}', '        yo, n = Y0_KOL[kol], {}                                          # v10 (v9: YUZ0 + BIND = 182,5)')
degis('                yo += HH[tip] + 2 * BIND + FUGA', '                yo += HH_KOL[kol] + 2 * BIND + FUGA                         # v10: kolon başına tek açıklık')
degis('CEK, K4X = kolonlar()', 'CEK, K4X = kolonlar()' + NL + 'HH_C = {c[1]: HH_KOL[c[0]] for c in CEK}                                  # v10: çekmece kodu → açıklık yüksekliği')
degis('    wo = GEN(kol); h = HH[tip];', '    wo = GEN(kol); h = HH_C[kod];')
degis('        cer = cer.cut(kut(x0, x0 + GEN(kol), yo, yo + HH[tip], Z_CER0 - 1, Z_CER1 + 1))', '        cer = cer.cut(kut(x0, x0 + GEN(kol), yo, yo + HH_C[kod], Z_CER0 - 1, Z_CER1 + 1))')
degis('        top_ = sum(HH[c[2]] + 2 * BIND + FUGA for c in cs)', '        top_ = sum(HH_C[c[1]] + 2 * BIND + FUGA for c in cs) + (Y0_KOL[kol] - (YUZ0 + BIND))   # v10: başlangıç kotu farkı da yığına')
degis('    h_ = min(HH[c[2]] for c in CEK) + 12.0 - (KY - 8.0)', '    h_ = min(HH_C[c[1]] for c in CEK) + 12.0 - (KY - 8.0)')
degis('c[4] + HH[c[2]] > fy0]', 'c[4] + HH_C[c[1]] > fy0]')
# ---- 1 · strok 700 ----
degis('Z_MOTOR, Z_AVARA = -769.0, -73.0 ', 'Z_MOTOR, Z_AVARA = -769.0, -1.0  ')
degis('"z −73 SABİT (strok 628)"', '"z −1 SABİT (v10 strok 700; v9 −73 / 628)"')
degis('    assert abs(STROK - 628.0) < 0.01 and abs(Z_AVARA + 73.0) < 0.01, "strok 628 / avara -73 degil: %.1f" % STROK',
      '    assert abs(STROK - 700.0) < 0.01 and abs(Z_AVARA + 1.0) < 0.01, "v10: strok 700 / avara -1 degil: %.1f" % STROK' + NL +
      '    assert STROK <= RAY_L + 0.01, "strok ray boyunu (%%100 acilir) gecti"')
# ---- 5 · kutular tek boy 540 ----
degis('TUB = {"hamur": 530.0, "lahm": 550.0, "icecek": 660.0, "ic1": 660.0, "ic1d": 660.0, "tatli": 660.0}',
      'TUB = {"hamur": 540.0, "lahm": 540.0, "icecek": 540.0, "ic1": 540.0, "ic1d": 540.0, "tatli": 540.0}   # v10: TEK KUTU (iç 618) · arka −597 · K2/K5 fan önü 19')
# ---- 2 · tepsiler ----
degis('TOP = {"hamur": dict(R=47.5, hc=12.0, cr=50.0, nx=5, nz=4, ax=105.0, az=130.0, td=520.0),' + NL +
      '       "lahm": dict(R=37.5, hc=10.0, cr=40.0, nx=6, nz=6, ax=88.0, az=90.0, td=540.0)}',
      'TOP = {"hamur": dict(R=47.5, hc=12.0, cr=50.0, nx=5, nz=5, ax=105.0, az=120.0, td=600.0),     # v10: 5 × 5 = 25 (v9 5 × 4 · 130) · aralık yan 10 / ön-arka 25' + NL +
      '       "lahm": dict(R=37.5, hc=10.0, cr=40.0, nx=6, nz=7, ax=88.0, az=85.0, td=600.0)}      # v10: 6 × 7 = 42 (v9 6 × 6 · 90) · aralık yan 13 / ön-arka 10' + NL +
      '# v10 · kutu ve tatlı da TEPSİDE (robot parmakla alır; v9 şerit + yaylı itici KALKTI): silindir ürün, çukur r + 1' + NL +
      'SIL = {"ic1": dict(r=33.0, h=115.0, cr=34.0, nx=6, nz=8, ax=82.0, az=76.0, td=608.0, ad="kutu330"),   # 6 × 8 = 48 · aralık yan 16 / ön-arka 10' + NL +
      '       "tatli": dict(r=47.5, h=60.0, cr=50.0, nx=4, nz=3, ax=105.0, az=120.0, td=600.0, ad="tatlikabi")}   # 4 × 3 = 12 (2 gün 11) · pide tepsisi hatvesi')
a = s.index("    # ---- içerik (hareketli) ----")
b = s.index("        return n, y0 + hk, y1\n") + len("        return n, y0 + hk, y1\n")
YENI = '''    # ---- içerik (hareketli) · v10: HEPSİ TEPSİDE (silikon 10, çukur 7) — robot parmakla alır ----
    if tip in TOP or tip in SIL:
        t = TOP[tip] if tip in TOP else SIL[tip]
        tz1 = Z_TUB1 - 5.0; tz0 = tz1 - t["td"]                          # tepsi kutunun önüne göre (kutu iç arkası −596)
        tw = min(265.0, (kb - ka) / 2.0 - 2.0)                           # v10: dar kolonda (K6 585) tepsi kutuya sığar
        tx0, tx1 = xc - tw, xc + tw
        ty0 = kc + 1.0
        X = [xc + (i - (t["nx"] - 1) / 2.0) * t["ax"] for i in range(t["nx"])]
        Zc = (tz0 + tz1) / 2.0
        Z = [Zc + (j - (t["nz"] - 1) / 2.0) * t["az"] for j in range(t["nz"])]
        cuk = cq.Workplane("XZ").pushPoints([(a, b) for a in X for b in Z]).circle(t["cr"]).extrude(-(CUKUR_H + 1.0)).translate((0, ty0 + TEPSI_T - CUKUR_H, 0))
        ekle(kod + "_tepsi", kut(tx0, tx1, ty0, ty0 + TEPSI_T, tz0, tz1).cut(cuk), "silikon", kod, grup=G,
             bom=("Tepsi · %d çukur Ø%.0f" % (len(X) * len(Z), 2 * t["cr"]), 1, "gıda silikonu 10 mm · çukur 7 · kalıp döküm", "%.0f × %.0f" % (tx1 - tx0, t["td"])))
        if tip in TOP:
            tk, ust, adk, mal = top_kati(tip), t["hc"] + t["R"], "top", "hamur"
        else:
            tk, ust, adk, mal = sily(0.0, 0.0, t["r"], 0.0, t["h"]), t["h"], t["ad"], ("hamur" if tip == "tatli" else "kutu_icecek")
        for i, a in enumerate(X):
            for j, b in enumerate(Z):
                ekle("%s_%s_%d_%d" % (kod, adk, i, j), tk.translate((a, yo + Y_OTUR, b)), mal, kod, grup=G)
        return len(X) * len(Z), yo + Y_OTUR + ust, y1
'''
s = s[:a] + YENI + s[b:]
# ---- denetim: açılınca arka sıra dışarıda (bütün tepsi tipleri) · kapasite ----
degis('''    for tip in TOP:                                                     # v8: katılardan (tepsi kutunun önüne göre)
        ks_ = {k_ for k_, t_, _n, _u, _a in ozet if t_ == tip}
        kenar = min(BB[p["ad"]].zmin for p in PARCALAR if p["birim"] in ks_ and "_top_" in p["ad"]) + STROK''',
      '''    for tip, adk in [(t_, "_top_") for t_ in TOP] + [(t_, "_%s_" % SIL[t_]["ad"]) for t_ in SIL]:   # v10: kutu + tatlı da tepside
        ks_ = {k_ for k_, t_, _n, _u, _a in ozet if t_ == tip}
        kenar = min(BB[p["ad"]].zmin for p in PARCALAR if p["birim"] in ks_ and adk in p["ad"]) + STROK''')
degis('    assert (pide, lahm, ice, tat) == (160, 432, 144, 12), "kapasite SPEC ile ayni degil"',
      '    assert (pide, lahm, ice, tat) == (175, 420, 144, 12) and len(CEK) == 21, "v10 kapasite: pide 175 · lahmacun 420 · icecek 144 · tatli 12 · 21 cekmece"' + NL +
      '    for g_ in (("K1", "K2", "K3"), ("K5", "K6")):                                          # v10 · SİMETRİ: grupta ön çizgileri aynı' + NL +
      '        cz = [sorted((c[4], HH_C[c[1]]) for c in CEK if c[0] == k_) for k_ in g_]' + NL +
      '        assert all(c_ == cz[0] for c_ in cz), "v10: %s on cizgileri ayni degil" % (g_,)' + NL +
      '    print("SIMETRI v10: K1-K3 %d cekmece x acik %.0f (on cizgileri ayni) · K5-K6 %d x %.0f (ayni)" % (len([c for c in CEK if c[0] == "K1"]), HH_KOL["K1"], len([c for c in CEK if c[0] == "K6"]), HH_KOL["K6"]))')
degis('icecek %d kutu TEK KAT (>= 139)', 'icecek %d kutu TEPSIDE (>= 139)')
degis('beklenen 160 / 432 / 144 / 12"', 'beklenen v10 175 / 420 / 144 / 12"')
degis('print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v12")))', 'print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v13")))   # v10: yerel derleme ağacında kalır (Kemal: BOM işi yok)')
compile(s, "store_cad_v10.py", "exec")
io.open(os.path.join(U, "store_cad_v10.py"), "w", encoding="utf-8").write(s)
print("store_cad_v10.py yazildi")
