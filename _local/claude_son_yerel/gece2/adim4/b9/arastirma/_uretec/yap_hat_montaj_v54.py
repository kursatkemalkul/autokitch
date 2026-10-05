# -*- coding: utf-8 -*-
"""hat_montaj_v53 → hat_montaj_v54 (27 Eyl 2026) — Kemal'in 5 maddesi:
1) TOPPING yalıtımı tek dikdörtgen, teknik cep ince saçla ayrılır → topping_uno_cad_v10.
2) K: yağ tankı + pano yukarıda (köprünün arkası) → kesme_cad_v3; K taban dolabı BOŞ.
3) (pafta) bez/eldiven kutusu fırına girmiş çizilmiş → pafta v15'te.
4) İçecek yedeği K tabanından FIRIN ÜSTÜ SAĞA: 4 koli (96 kutu) kompresörün solunda; 5. koli sığmıyor (276 mm'ye 4 × 123 = 492 ≤ 512,
   5. koli 615) → F dolabının boş pizza gözüne (fırının hemen altı) · toplam 120 = 4 gün (kural 5.3 korunur).
5) E: kalıp + kapak plakası ayakları 790'daki alt rafta biter, altı boş → kutu_cad_v4.
+ HAVA ANA HATTI yeniden yollandı (v53'te pizza yığınının arka üst köşesine 14 mm giriyordu, v10 yalıtımında tavan diliminden geçecekti):
  kompresör → z −432 (yığınların arkası, davlumbaz bölmesi) · y 1977 → F'de 1950'ye iner → TOPPING teknik cebine girer → kuru bölme;
  K dalı z −780 · y 1977 → K şartlandırıcısının tepesine (x 4085, y 1870). Yeni denetim: hava hattı ↔ kutu birimleri + TOPPING yalıtım/teknik + K parçaları."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v53.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
degis('"""v53 (27 Eyl 2026):', '"""v54 (27 Eyl 2026): TOPPING yalıtımı tek dikdörtgen + teknik cep ince saç (topping_uno_cad_v10) · K tank + pano yukarıda, taban boş (kesme_cad_v3) · içecek yedeği fırın üstü sağ 4 koli + dolapta 1 koli · E ayakları alt rafta (kutu_cad_v4) · hava ana hattı yeniden yollandı + denetimi' + NL + 'v53 (27 Eyl 2026):')
s = s.replace('"topping_uno_cad_v9.py + topping_cad_v24.py"', '"topping_uno_cad_v10.py + topping_cad_v24.py"').replace('"sac", "topping_uno_cad_v9.py", "hat/topping_v2.html")', '"sac", "topping_uno_cad_v10.py", "hat/topping_v2.html")')
degis('_sp = _ilu.spec_from_file_location("TU9", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v9.py"))',
      '_sp = _ilu.spec_from_file_location("TU10", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v10.py"))   # v54: yalıtım tek dikdörtgen + teknik ayırma saçı')
degis('ANA_V44 = [(3090, 1977, -380), (3090, 2000, -380), (3090, 2000, -415), (1640, 2000, -415), (1640, 2000, -740), (1640, 1335, -740), (1650, 1335, -740)]',
      'ANA_V44 = [(3090, 1977, -380), (3090, 1977, -432), (1830, 1977, -432), (1830, 1950, -432), (1640, 1950, -432), (1640, 1950, -740), (1640, 1335, -740), (1650, 1335, -740)]   # v54: yığınların arkası (z −432) · TOPPING teknik cebinden')
degis('ANA_K48 = [(3090, 2000, -415), (3090, 2000, -795), (3460, 2000, -795), (3460, 1700, -795)]',
      'ANA_K48 = [(3090, 1977, -432), (3090, 1977, -780), (3385, 1977, -780), (3385, 1870, -780)]   # v54: K şartlandırıcısının (MS4) tepesine · köşe dikmesinin (z −798) önünden')
degis('import kesme_cad_v2 as KS', 'import kesme_cad_v3 as KS                                  # v54: tank + pano yukarıda, taban boş')
i = s.index('    ("K_ICECEK_YEDEK", "İçecek yedeği · soğutmasız'); j = s.index(NL, i) + 1
s = s[:i] + s[j:]
s = s.replace('raise AssertionError("kesme_cad_v2 parcasi birimsiz kaldi: "', 'raise AssertionError("kesme_cad_v3 parcasi birimsiz kaldi: "')
degis('"sac", "kesme_cad_v2.py", "hat/kesme.html")', '"sac", "kesme_cad_v3.py", "hat/kesme.html")')
degis('import kutu_cad_v3 as KC                                  # v40: alt taban 123, asansör tahriki tabanın altında', 'import kutu_cad_v4 as KC                                  # v54: kalıp ayakları alt rafta (790), altı boş')
s = s.replace('raise AssertionError("kutu_cad_v3 parcasi birimsiz kaldi: "', 'raise AssertionError("kutu_cad_v4 parcasi birimsiz kaldi: "')
degis('"sac", "kutu_cad_v3.py", "hat/pack.html")', '"sac", "kutu_cad_v4.py", "hat/pack.html")')
degis('print("E KUTU MODULU (kutu_cad_v3):', 'print("E KUTU MODULU (kutu_cad_v4):')
# içecek yedeği birimleri (fırın üstü sağ + dolap)
degis('birim("D_PIZZA_YEDEK_UST",', '''birim("D_ICECEK_YEDEK_UST", "İçecek yedeği · FIRIN ÜSTÜ SAĞ (kompresörün solu) · 4 koli × 24 = 96 kutu · koli 400 × 267 × 123 (267 x yönünde) · soğutmasız (Kemal 27 Eyl)", "D", "KUTU",
      (3328.0, 3595.0), (1516.0, 2008.0), (-422.0, -22.0), "kutu", "v54 · kural 5.3 · koli ölçüsü kesme_cad_v2")
birim("D_ICECEK_YEDEK_ALT", "İçecek yedeği · 5. koli (fırın üstüne sığmadı: 276 mm'ye 4 × 123) · F dolabının boş pizza gözü önde · 24 kutu → toplam 120: soğuk 160 + 120 = 280 = 4 gün", "D", "KUTU",
      (3170.0, 3570.0), (130.0, 253.0), (-287.0, -20.0), "kutu", "v54 · kural 5.3")
birim("D_PIZZA_YEDEK_UST",''')
# hava hattı denetimi
degis('''    _kx, _ky, _kz = BM.kapi_acik_zarf()''', '''    # ---- v54 · HAVA ANA HATTI (yeniden yollandı) ↔ kutu birimleri + TOPPING yalıtım / teknik saç / teknik zarflar + K parçaları (gerçek katı) ----
    _hv = []
    _HV_ATLA = ("HAVA_KOMPRESOR", "D_DAVLUMBAZ")                                           # hat bilerek davlumbaz bölmesinden geçer
    for _rn, _rota in (("ANA", ANA_V44), ("K_DALI", ANA_K48)):
        _an = TU.boru(_rota, 5.0); _an = (_an.val() if hasattr(_an, "val") else _an).translate(cq.Vector(X_BC, 0.0, 0.0))
        for b in B:
            if b["durum"] in ("KUTU", "KATALOG") and not b["kod"].endswith("_KABIN") and b["kod"] not in _HV_ATLA:
                kb = kutu_kat(b).val()
                if _bbk(_an, kb):
                    v_ = _hacim(_an, kb)
                    if v_ > 1.0 or v_ < 0: _hv.append((round(v_, 1), _rn, b["kod"]))
        for q in TU.P:
            if q["ad"].startswith(("yalitim_blogu", "teknik_")):
                sq = q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))
                if _bbk(_an, sq):
                    v_ = _hacim(_an, sq)
                    if v_ > 1.0 or v_ < 0: _hv.append((round(v_, 1), _rn, "TOPPING:" + q["ad"]))
        for p in KS.PARCALAR:
            if p["ad"].startswith(("sol_sac", "sag_sac", "arka_sac", "ust_sac")): continue    # duvar geçişi: rakor deliği (bilinçli)
            sk = _tek(p["wp"]).translate(cq.Vector(X_K, 0.0, 0.0))
            if _bbk(_an, sk):
                v_ = _hacim(_an, sk)
                if v_ > 1.0 or v_ < 0: _hv.append((round(v_, 1), _rn, "K:" + p["ad"]))
    print("HAVA ANA HATTI (v54 yolu) ↔ kutu birimleri (pizza + icecek yedegi, dolap) + TOPPING yalitim/teknik + K parcalari (gercek kati; K sol duvari rakor deliginden gecer): %s" % ("TEMIZ" if not _hv else "%d BULGU %s" % (len(_hv), _hv[:8])))
    assert not _hv, "hava ana hatti bir birime giriyor"
    _kx, _ky, _kz = BM.kapi_acik_zarf()''')
degis('pafta="HAT v53 (27 Eyl) ·', 'pafta="HAT v54 (27 Eyl) · TOPPING yalitim tek dikdortgen + teknik cep ince sac (uno v10) · K tank + pano yukarida, taban bos (kesme v3) · icecek yedegi firin ustu sag 96 + dolapta 24 = 120 (4 gun) · E ayaklari alt rafta 790 (kutu v4) · hava ana hatti yeniden yollandi · v53:')
degis('print("ANA MONTAJ ANIMASYONU (v53):', 'print("ANA MONTAJ ANIMASYONU (v54):')
s = s.replace('hat_v53.glb', 'hat_v54.glb').replace('hat_v53.usdz', 'hat_v54.usdz').replace('"hat_v53"', '"hat_v54"')
io.open(os.path.join(U, "hat_montaj_v54.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v54.py yazildi")
