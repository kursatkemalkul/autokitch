# -*- coding: utf-8 -*-
"""HAT v3.7 · FIRIN ÜSTÜ PİZZA KUTUSU YEDEĞİ GERÇEK YIĞIN — MONTAJ METİN YAMASI TASLAĞI (1 Eki 2026 · Claude · YEREL)
Kullanım (bir sonraki yap_hat3_montaj_vN.py içinde, hat3_montaj_v6 metni üzerinde):
    import importlib.util as _ilu; _sp = _ilu.spec_from_file_location("yama_pizza_yedek", <bu dosya>); YP = _ilu.module_from_spec(_sp); _sp.loader.exec_module(YP)
    s = YP.uygula(s)          # 5 rep, her biri tekil (assert) · zaten yamalıysa aynen döner · sonunda compile

ÖNCE (v3.6): D_PIZZA_YEDEK_UST = birim(..., "KUTU", ...) → 0 parça, yer tutucu kutu (12 üçgen), dökümde / parca_kutulari'nda yok; yalnız iki denetimde
  kutu olarak vardı (FIRIN ÇAKIŞMA "D:" kutuları · HAVA ANA HATTI kutu birimleri).
YÖNTEM (U_F'teki 170 kutu = h3_ust_depo_v2.kutu_yedegi(): birim U_KUTU_YEDEK, TEK karton katı "ust_f_pizza_kutusu_yigini" = kut(PZ_X, raf üstü → + adet × 1,6,
  PZ_Z), "karton", sarf BOM satırı, üreteç PARCALAR'ında → _dis_birim ile GERÇEK birim): aynısı fırın üstü kabin üretecinde (FU = h3_firin_ust_v1):
  FU.ekle("f_ust_pizza_kutusu_yigini", FU.kut(*FU.PIZZA), "karton", "D_PIZZA_YEDEK_UST", bom=sarf) + FU.BIRIMLER / BIRIM_MODUL → _dis_birim(FU, ...)
  D_PIZZA_YEDEK_UST'u "GERCEK_FIRIN_UST" birimi olarak kurar (aynı yer, B listesinde aynı sıra · kategori URUN · mekanizma F/Kutu yedeği).
YER / ÖLÇÜ (üreteçten + dökümden): FU.PIZZA = firin_ust_kabin_cad_v1 (X0 + 20, X0 + 824, raf üstü 1348, 1348 + 320 × 1,6 = 1860, −424, −20) = eski KUTU'nun
  aynısı · raf (firin_tp10 ust_raf, h3_firin_ust_v1.raf_duzelt) 1344–1348 düz, havşalı vida başları yüzeyde → yığın rafa oturur · tavan sacı altı 1860,5 → 0,5 pay
  (U_F yığınındaki kural: üstü tavanın ≥ 0,5 altında) · tavan kirişi + ön dikme 3326–3356 → 2 mm · gazlı yay gövdesi 2502,8–2517,8 → 2,2 mm ·
  davlumbaz kutusu z ≤ −440 → 16 mm · hava ana hattı K dalı z −432 (Ø10) → 3 mm (v3.6 HAVA denetimi aynı kutuyla TEMİZ) ·
  kompresör (+20 · JUN-AIR tank 3359–3739, ayaklar ≥ 3364) → ≥ 35 mm · yeni ana pano (ELK_ANA_PANO_UF x 3490–3978, y ≥ 1863,5) → x'te 166 mm, y'de 3,5 mm.
DENETİM: (a) FIRIN ÇAKIŞMA _DG'ye gerçek katı ("D:D_PIZZA_YEDEK_UST:…"), (b) HAVA ANA HATTI'na gerçek katı, (c) YENİ: yığın ↔ fırın üstü kabin (FU) + raf ve
  fırın (FT) + kompresör (TU kompresor_ @ KOMP_KAY) + üst depo (UD) + ana pano (AP) + elektrik (EL) gerçek katı kesişimi > 1 mm³ yok → assert."""
import os

ISARET = "# ---- v3.7 · PZ37"

_YIGIN = ISARET + r''' · FIRIN ÜSTÜ PİZZA KUTUSU YEDEĞİ GERÇEK YIĞIN (yama_pizza_yedek · U_F'teki U_KUTU_YEDEK yöntemi: tek karton katı + sarf BOM, üretecin PARCALAR'ında)
if not any(p_["ad"] == "f_ust_pizza_kutusu_yigini" for p_ in FU.PARCALAR):
    _pz37 = tuple(float(v_) for v_ in FU.PIZZA)                                         # firin_ust_kabin_cad_v1.PIZZA (raf üstü → + 320 × 1,6)
    assert abs(_pz37[0] - (X_D + 20.0)) < 1e-6 and abs(_pz37[1] - (X_D + 824.0)) < 1e-6 and abs(_pz37[2] - FT.UST_RAF_Y[1]) < 1e-6 \
        and (_pz37[4], _pz37[5]) == (-424.0, -20.0), ("v3.7 · pizza yığını yeri üreteçle tutmuyor", _pz37, X_D, FT.UST_RAF_Y)
    assert FU.PIZZA_UST_KUTU == PIZZA_UST_KUTU == 320 and abs((_pz37[3] - _pz37[2]) - PIZZA_UST_KUTU * FU.KUTU_T) < 1e-6, (FU.PIZZA_UST_KUTU, PIZZA_UST_KUTU, _pz37)
    assert 0.5 - 1e-9 <= FU.Y_TAVAN - _pz37[3] <= 0.51, ("v3.7 · yığın üstü ↔ tavan sacı altı payı (U_F kuralı ≥ 0,5)", FU.Y_TAVAN, _pz37[3])
    assert _pz37[1] <= FU.KIRIS_X[0] - 2.0, ("v3.7 · tavan kirişi / ön dikme yığına değiyor", _pz37, FU.KIRIS_X)
    FU.ekle("f_ust_pizza_kutusu_yigini", FU.kut(*_pz37), "karton", "D_PIZZA_YEDEK_UST", kaynak="v3.7 montaj (U_KUTU_YEDEK yöntemi · firin_ust_kabin_cad_v1.PIZZA)",
            bom=("Pizza kutusu yedeği (düz açılım, sarf)", PIZZA_UST_KUTU, "804 × 404 × 1,6 · 32 × 32 × 4,2 E-dalga",
                 "fırın üstü SOL raf (üst %.0f) · tek yığın %d kutu %.0f mm · üstü tavan sacının %.1f altında · operatör şarjöre buradan besler · üstündeki U_F rafında 170 kutu daha"
                 % (_pz37[2], PIZZA_UST_KUTU, _pz37[3] - _pz37[2], FU.Y_TAVAN - _pz37[3]), "SARF"))
    FU.BIRIMLER.append(("D_PIZZA_YEDEK_UST", "Pizza kutusu yedeği · TEK YER: fırın üstü SOL, rafta %d kutu düz (804 × 404 × %.0f) · v3.7 GERÇEK YIĞIN (U_F'teki U_KUTU_YEDEK "
                        "yöntemi: tek karton katı + sarf BOM) · raf üstü %.0f → %.0f, tavan sacına %.1f · E şarjörü 462 + %d = 782 ≈ 2,8 gün (SPEC · şarjörün "
                        "kullanılabilir kısmı ≈ 432 → 752, karar Kemal'de) (Kemal 27 Eyl: sola koy)"
                        % (PIZZA_UST_KUTU, _pz37[3] - _pz37[2], _pz37[2], _pz37[3], FU.Y_TAVAN - _pz37[3], PIZZA_UST_KUTU)))
    FU.BIRIM_MODUL["D_PIZZA_YEDEK_UST"] = "D"
    print("v3.7 · PIZZA YEDEGI GERCEK YIGIN: f_ust_pizza_kutusu_yigini %d kutu · x %.0f–%.0f · y %.1f–%.1f · z %.0f…%.0f (birim D_PIZZA_YEDEK_UST · GERCEK_FIRIN_UST)"
          % ((PIZZA_UST_KUTU,) + _pz37))
'''
_CAPA_FU = '_dis_birim(FU, "GERCEK_FIRIN_UST", "firin_ust_kabin_cad_v1.py", "hat/oven.html")\n'
_KUTU_ESKI = ('''birim("D_PIZZA_YEDEK_UST", "Pizza kutusu yedeği · TEK YER: fırın üstü SOL, rafta %d kutu düz (804 × 404 × 512) · E şarjörü 462 + %d = 782 ≈ 2,8 gün (SPEC · şarjörün kullanılabilir kısmı ≈ 432 → 752, karar Kemal'de) (Kemal 27 Eyl: sola koy)" % (PIZZA_UST_KUTU, PIZZA_UST_KUTU), "D", "KUTU",
      (X_D + 20.0, X_D + 824.0), (FT.UST_RAF_Y[1], FT.UST_RAF_Y[1] + 512.0), (-424.0, -20.0), "karton", "v48 · kural 5.5 · v57 raf 1348")
''')
_KUTU_YENI = '# v3.7 · D_PIZZA_YEDEK_UST artık KUTU değil: yukarıda FU üretecinde gerçek yığın (PZ37) → _dis_birim(FU, ...) GERCEK_FIRIN_UST birimi olarak kurdu\n' \
             'assert [b_["durum"] for b_ in B if b_["kod"] == "D_PIZZA_YEDEK_UST"] == ["GERCEK_FIRIN_UST"], "v3.7 · pizza yedeği birimi"\n'
_DG_ESKI = '            _DG.append(("D:" + b["kod"], kutu_kat(b).val()))\n'
_DG_YENI = _DG_ESKI + ('''    for p in FU.PARCALAR:                                                                # v3.7 · pizza yedeği gerçek katı (KUTU değil) — fırın çakışma denetiminde kalır
        if p["birim"] == "D_PIZZA_YEDEK_UST": _DG.append(("D:D_PIZZA_YEDEK_UST:" + p["ad"], FU.dunya(p)))
''')
_HV_ESKI = '                    if v_ > 1.0 or v_ < 0: _hv.append((round(v_, 1), _rn, b["kod"]))\n'
_HV_YENI = _HV_ESKI + ('''        for p in FU.PARCALAR:                                                            # v3.7 · fırın üstü pizza yedeği gerçek katı — hava hattı denetiminde kalır
            if p["birim"] != "D_PIZZA_YEDEK_UST": continue
            kb = FU.dunya(p)
            if _bbk(_an, kb):
                v_ = _hacim(_an, kb)
                if v_ > 1.0 or v_ < 0: _hv.append((round(v_, 1), _rn, "D_PIZZA_YEDEK_UST:" + p["ad"]))
''')
_KOMSU_CAPA = '    assert not _hv, "hava ana hatti bir birime giriyor"\n'
_KOMSU = _KOMSU_CAPA + ('''    # ---- v3.7 · FIRIN ÜSTÜ PİZZA YEDEĞİ (gerçek yığın) ↔ fırın üstü kabin + raf / fırın + kompresör (+20) + üst depo + ana pano + elektrik (gerçek katı > 1 mm³) ----
    _py37 = [FU.dunya(p) for p in FU.PARCALAR if p["birim"] == "D_PIZZA_YEDEK_UST"]
    assert len(_py37) == 1, "v3.7 · pizza yığını yok"
    _py37 = _py37[0]; _pb37 = _py37.BoundingBox()
    _K37 = [("FU:" + p["ad"], FU.dunya(p)) for p in FU.PARCALAR if p["birim"] != "D_PIZZA_YEDEK_UST"]
    _K37 += [("FT:" + p["ad"], FT.dunya(p)) for p in FT.PARCALAR]
    _K37 += [("HAVA:" + q["ad"], q["sh"].translate(cq.Vector(X_BC + KOMP_KAY[0], KOMP_KAY[1], KOMP_KAY[2]))) for q in TU.P if q["ad"].startswith("kompresor_")]
    _K37 += [("U:" + p["ad"], UD.dunya(p)) for p in UD.PARCALAR]
    if AP is not None: _K37 += [("ANA_PANO:" + p["ad"], AP.dunya(p)) for p in AP.PARCALAR]
    _K37 += [("ELK:" + p["ad"], EL.dunya(p)) for p in EL.PARCALAR]
    _c37, _d37 = [], {}
    for c_, sc in _K37:
        if _bbk(_py37, sc):
            v_ = _hacim(_py37, sc)
            if v_ > 1.0 or v_ < 0: _c37.append((round(v_, 1), c_))
        for _on37 in ("FU:f_ust_tavan_sac", "FU:f_ust_tavan_kirisi", "HAVA:", "ANA_PANO:", "FT:ust_raf"):
            if c_.startswith(_on37) and (c_ == _on37 or _on37.endswith(":")):
                _d37[_on37] = min(_d37.get(_on37, 1e9), _py37.distance(sc))
    print("v3.7 · PIZZA YEDEGI GERCEK YIGIN (x %.0f–%.0f · y %.1f–%.1f · z %.0f…%.0f) ↔ firin ustu kabin + raf/firin + kompresor + ust depo + ana pano + elektrik (%d parca, gercek kati > 1 mm3): %s"
          " · tavan sacina %.1f · tavan kirisine %.1f · rafa %.1f · kompresore %.1f · ana panoya %.1f mm"
          % (_pb37.xmin, _pb37.xmax, _pb37.ymin, _pb37.ymax, _pb37.zmin, _pb37.zmax, len(_K37), "TEMIZ" if not _c37 else "%d BULGU %s" % (len(_c37), sorted(_c37, reverse=True)[:8]),
             _d37.get("FU:f_ust_tavan_sac", -1), _d37.get("FU:f_ust_tavan_kirisi", -1), _d37.get("FT:ust_raf", -1), _d37.get("HAVA:", -1), _d37.get("ANA_PANO:", -1)))
    assert not _c37, "v3.7: firin ustu pizza yigini bir parcaya giriyor"
''')


def uygula(s):
    """hat3_montaj metnine PZ37 (fırın üstü pizza yedeği gerçek yığın + denetimleri) · 5 rep, her biri tekil (assert) · zaten yamalıysa aynen döner"""
    if ISARET in s:
        return s
    R = [(_CAPA_FU, _YIGIN + _CAPA_FU), (_KUTU_ESKI, _KUTU_YENI), (_DG_ESKI, _DG_YENI), (_HV_ESKI, _HV_YENI), (_KOMSU_CAPA, _KOMSU)]
    for a, b in R:
        assert s.count(a) == 1, "yama_pizza_yedek: çapa yok / tekil değil (%d): %s" % (s.count(a), a[:70])
        s = s.replace(a, b, 1)
    compile(s, "hat3_montaj_pz37", "exec")
    return s


if __name__ == "__main__":
    import io, sys
    yol = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "b3", "arastirma", "_uretec", "h3", "hat3_montaj_v6.py")
    s0 = io.open(yol, encoding="utf-8").read(); s1 = uygula(s0)
    assert uygula(s1) == s1
    print("yama_pizza_yedek: 5 rep · derlendi · %+d karakter" % (len(s1) - len(s0)))
