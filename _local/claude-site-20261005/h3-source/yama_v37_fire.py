# -*- coding: utf-8 -*-
"""HAT v3.7 · FİRE SİLECEĞİ ürün yolundan çıkar + PİDE KORİDORU denetimi ürün durumuna göre — MONTAJ METİN YAMASI TASLAĞI (1 Eki 2026 · Claude · YEREL)
Kullanım (bir sonraki yap_hat3_montaj_vN.py içinde, hat3_montaj_v6 metni üzerinde):
    import importlib.util as _ilu; _sp = _ilu.spec_from_file_location("yama_fire_silecegi", <bu dosya>); YF = _ilu.module_from_spec(_sp); _sp.loader.exec_module(YF)
    s = YF.uygula(s)          # 3 rep, her biri tekil (assert) · zaten yamalıysa aynen döner · sonunda compile

BULGU (test_fire_silecegi.py · dünya mm): v3.6 montajındaki "PIDE KORIDORU … 96000 mm³ ↔ fire_silecegi_lastigi" GERÇEK sorun (yalnız zarf hatası değil):
  · lastik x 1535–1555 · y 1017–1059 (park: diskten 17 yukarı, iner → 1000) · z −350…0 — h3_topping_v1 FIRE_DX = +65 ile v1'deki 1470–1490'dan "yayıcılarla
    kıyma arasına" alınmış. Kıyma ağzı 1596 (TARAF +1): tabla dozajda 1707,8 → 1616'ya iner; 1680'in altında kıymalı yüzey (kaplanan r ≤ 125) lastiğin altında
    döner (tabla 1616'da lastik sağ yüzü merkezden 61 mm). Karışıkta sos (1645) kıymadan sonra: lastik r 90–110'da kıymalı + soslu yüzeyin üstünde.
  · Yükseklik: hamur 8 + kıyma şeridi 2–9 mm (160 g · debi / yüzey hızı: r 61–112'de kesit 36–66 mm², örtüşmeyle ≈ 4, yuvarlak ip Ø7–9) = 10–17 mm ·
    lastik altı 17 → pay 0–7 mm; hat kuralı (HS.Y_KORIDOR 1033 = Ø300 × 28 + üst malzeme 5; dozaj ağızları 1048) 16 mm ihlal → lastik kıymanın üstünü silebilir.
DÜZELTME (bu yama): 4 parça (lastik · CJ2 silindiri · 2 kılavuz mili) birlikte −91 x → lastik 1444–1464 (askı yine alt yalıtım sacına, 1109):
  · ilk dozaj konumu (kıyma r_ic 1616) − 150 = 1466 → dolu ürün koridoruna 2 mm · hamur kenarına (r 140) 12 · kaplanan yüzeye (r 125) 27 mm;
    altından yalnız ÇIPLAK HAMUR geçer (8 mm → park altı 1017: 9 mm pay). Silecek kinematiği aynı (17 mm strok, diske iner).
  · komşu: dış yan sac (1436–1437,5) 6,5 mm · elektrik (x limit kablosu) 397 mm · alt yalıtım sacı = askı yüzü (temas, kesişim 0).
  · fire akışı: tabla aktarmadan dönerken (sağdan sola) inmiş lastiğin altından geçer → yapışan pide lastiğin sağına (1464–1744) düşer → mekanizma teknesi
    (836–2495) tutar; kırıntı çekmecesi 1536'dan başlıyor (AÇIK · TOPPING sahibi: çekmece sol ucu ~1440'a uzatılabilir).
  · KALICI YERİ h3_topping_v1.FIRE_DX (TOPPING sahibinin dosyası, bu yamada YAZILMADI): 1535 − 1470 → 1444 − 1470. O yazılınca bu sarmalayıcı kendiliğinden
    0 kaydırır (kaydırma lastiğin o anki yerinden hesaplanır — çift kayma olmaz).
DENETİM: v3.6'ya kadar 33 mm kutu park'tan aktarmaya kadar uzanıyordu (açıcıdan ilk dozaja kadar ürün ÇIPLAK HAMUR — kutu orada fazla) ve yalnız "bilgi"ydi.
  v3.7: (a) çıplak hamur kutusu park − 150 → aktarma + 150, y P+0,5 … P + 8 + 5 · (b) dolu ürün Ø300 stadyumu (disk süpürmesi) ilk dozaj konumundan (montajın
  kendi _IST listesinden) aktarmaya, y P+0,5 … P+33 · ikisi de TOPPING sabitleriyle (açıcı / koniler / dozaj ağızları hariç) TEMİZ olmalı → assert."""
import os

ISARET = "# ---- v3.7 · FIRE37"

_SARMA = ISARET + r''' · FİRE SİLECEĞİ ürün yolundan çıktı (yama_fire_silecegi): v3'te lastik 1535–1555 (h3_topping_v1 FIRE_DX +65), park altı 1017 (diskten 17) —
#      kıyma dozajında (tabla 1707,8 → 1616, ağız 1596) ve karışıkta sos dozajında (1645) dolu ürün (kaplanan r ≤ 125) lastiğin altında dönüyordu (koridor 33 kuralı) →
#      4 parça (lastik · silindir · 2 kılavuz) birlikte x'te: lastik 1444–1464 = yalnız çıplak hamurun (8 mm, 9 mm pay) geçtiği yer · ilk dozajın Ø300 koridoru 1466'dan başlar.
#      Kalıcı yeri h3_topping_v1.FIRE_DX (1444 − 1470): yazılınca kaydırma 0 olur (lastiğin o anki yerinden hesaplanır).
FIRE37_X = (1444.0, 1464.0)                                                               # lastik dünya x (20 kalın · silindir + kılavuzlar ekseni 1454)
_TC_MODUL36 = TC.modul


def _tc_modul37():
    r_ = _TC_MODUL36()
    _fs = [p_ for p_ in TC.PARCALAR if p_["ad"].startswith("fire_silecegi_")]
    _la = [p_ for p_ in _fs if p_["ad"] == "fire_silecegi_lastigi"]
    assert len(_fs) == 4 and len(_la) == 1, "v3.7 · fire sileceği parçaları: %s" % [p_["ad"] for p_ in _fs]
    _b = _la[0]["wp"].val().BoundingBox()
    _dx = FIRE37_X[0] - (X_BC + _b.xmin)
    assert abs((_b.xmax - _b.xmin) - (FIRE37_X[1] - FIRE37_X[0])) < 0.01, "v3.7 · lastik kalınlığı değişmiş: %.2f" % (_b.xmax - _b.xmin)
    if abs(_dx) > 1e-6:
        for p_ in _fs: p_["wp"] = p_["wp"].translate((_dx, 0.0, 0.0))
    return r_


TC.modul = _tc_modul37
TC.PARCALAR[:] = []; TC.modul()
'''

_KOR_ESKI = ('''    # (3) pide koridoru park → aktarma (Ø300 × 28 + üst malzeme 5, kaset bandı üstünden) ↔ TOPPING sabitleri (açıcı / koniler / dozaj ağızları hariç: onlar pideye çalışır)
    _kor = FT.kut(X_BC + TC.XC_TABLA - 150.0, X_BC + TH.X_AKTARMA + 150.0, P + 0.5, P + 33.0, ZT - 150.0, ZT + 150.0).val()
    _kor_hit = []
    for c_, sc in _ENG:
        if _bbk(_kor, sc):
            v_ = _hacim(_kor, sc)
            if v_ > 1.0 or v_ < 0: _kor_hit.append((round(v_, 1), "PIDE KORIDORU", c_))
''')
_KOR_YENI = ('''    # (3) v3.7 · PİDE KORİDORU ürün durumuna göre (Ø300, kaset bandı üstünden) ↔ TOPPING sabitleri (açıcı / koniler / dozaj ağızları hariç: onlar pideye çalışır):
    #     (a) ÇIPLAK HAMUR park → aktarma: hamur 8 + pay 5 (açıcıdan ilk dozaja ürün yalnız hamur) · (b) DOLU ÜRÜN Ø300 stadyumu (disk süpürmesi)
    #     ilk dozaj konumundan (_IST en küçük tabla x) aktarmaya: 28 + üst malzeme 5 = 33 (HS.Y_KORIDOR) · v3.6'ya kadar 33 mm kutu park'tan başlıyordu (yalnız bilgi)
    _HAM37 = 8.0                                                                           # açıcının açtığı hamur [topping_v2_hesap_v2 PIDE_UST 1176 − disk 1168]
    _xd37 = min(a_[1] for a_ in _IST); _xa37 = X_BC + TH.X_AKTARMA                       # ilk dozaj (kıyma r_ic 1616) · aktarma 2365,4
    _korH = FT.kut(X_BC + TC.XC_TABLA - 150.0, _xa37 + 150.0, P + 0.5, P + _HAM37 + 5.0, ZT - 150.0, ZT + 150.0).val()
    _korD = cq.Workplane("XZ").center((_xd37 + _xa37) / 2.0, ZT).slot2D(_xa37 - _xd37 + 300.0, 300.0, 0).extrude(-(33.0 - 0.5)).translate((0, P + 0.5, 0)).val()
    assert abs(_korD.BoundingBox().ymin - (P + 0.5)) < 1e-6 and abs(_korD.BoundingBox().ymax - (P + 33.0)) < 1e-6 and abs(_korD.BoundingBox().xmin - (_xd37 - 150.0)) < 1e-6
    _kor_hit = []
    for c_, sc in _ENG:
        for _kn37, _kk37 in (("HAMUR KORIDORU", _korH), ("DOLU URUN KORIDORU", _korD)):
            if _bbk(_kk37, sc):
                v_ = _hacim(_kk37, sc)
                if v_ > 1.0 or v_ < 0: _kor_hit.append((round(v_, 1), _kn37, c_))
    _fs37 = [sc.BoundingBox() for c_, sc in _ENG if c_ == "TOPPING:fire_silecegi_lastigi"]
    assert len(_fs37) == 1, "v3.7 · fire sileceği lastiği denetimde yok"; _fs37 = _fs37[0]
''')
_YAZ_ESKI = ('''    print("PIDE KORIDORU park → aktarma (bilgi · dozaj ağızları pideye çalışır): %s" % ("TEMIZ" if not _kor_hit else "%d temas" % len(_kor_hit)))
    for x_ in sorted(_kor_hit, reverse=True)[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
''')
_YAZ_YENI = ('''    print("PIDE KORIDORU v3.7 (urun durumuna gore · ciplak hamur park → aktarma y %.1f–%.1f · dolu urun Ø300 stadyum x %.1f → %.1f, y %.1f–%.1f): %s · "
          "fire silecegi lastigi x %.1f–%.1f · y %.1f–%.1f (park) → dolu koridora %.1f mm · hamura %.1f mm"
          % (P + 0.5, P + _HAM37 + 5.0, _xd37 - 150.0, _xa37 + 150.0, P + 0.5, P + 33.0, "TEMIZ" if not _kor_hit else "%d BULGU" % len(_kor_hit),
             _fs37.xmin, _fs37.xmax, _fs37.ymin, _fs37.ymax, (_xd37 - 150.0) - _fs37.xmax, _fs37.ymin - (P + _HAM37)))
    for x_ in sorted(_kor_hit, reverse=True)[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
    assert not _kor_hit, "v3.7: pide koridorunda TOPPING sabit parcasi var"
''')
_CAPA_SARMA = "KASET_Z = (TH.Z_KASET[1], TH.Z_KASET[0])\n"


def uygula(s):
    """hat3_montaj metnine FIRE37 (silecek yeri) + ürün durumuna göre koridor denetimi · her rep tekil (assert) · zaten yamalıysa aynen döner"""
    if ISARET in s:
        return s
    R = [(_CAPA_SARMA, _SARMA + _CAPA_SARMA), (_KOR_ESKI, _KOR_YENI), (_YAZ_ESKI, _YAZ_YENI)]
    for a, b in R:
        assert s.count(a) == 1, "yama_fire_silecegi: çapa yok / tekil değil (%d): %s" % (s.count(a), a[:70])
        s = s.replace(a, b, 1)
    compile(s, "hat3_montaj_fire37", "exec")
    return s


if __name__ == "__main__":
    import io, sys
    yol = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "b3", "arastirma", "_uretec", "h3", "hat3_montaj_v6.py")
    s0 = io.open(yol, encoding="utf-8").read(); s1 = uygula(s0)
    assert uygula(s1) == s1
    print("yama_fire_silecegi: 3 rep · derlendi · %+d karakter" % (len(s1) - len(s0)))
