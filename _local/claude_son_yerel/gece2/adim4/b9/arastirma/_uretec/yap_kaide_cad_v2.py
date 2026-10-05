# -*- coding: utf-8 -*-
"""kaide_cad_v1.py -> kaide_cad_v2.py (27 Eyl 2026 gece) · SPEC_on_duzlem_v63.md §2.2 (ÖN DÜZLEM +79 · TEMİZ KUTU İSTASYONLAR)
  · KAIDE_A + KAIDE_C ön profili z −4 → +35 (KZ[1]) — dolap üst sacı (store_cad_v8) +39'a uzuyor, kaide tam basar; önünde A/C ön çerçevesi +39…+59
  · A mekanizma taban sacı x 692 → 700 (C dis_taban'ın sol ucuna değer, 8 mm boşluk kapanır)
  · KARAR (varsayım): A boyuna profili kolon DİKMESİNİN altına (z −655…−615, dikme ekseni −635) · taban sacı kolon deliği 122 × 172 → 122 × 52 (keşif A §5)
  · TOPPING karşılaştırması: TC = topping_cad_v25 (yoksa v24) · TU = topping_uno_cad_v14 (yoksa v13; eski v11 yüklemesi kalktı)
  · yeni denetimler: A taban sacı ↔ C dis_taban x 700 teması · havada parça (denetim_temas_v1) = 0 · dolap üst sacı (store_cad_v8 varsa) kaide ön profilinin altında
  · DENETÇİ DÜZELTMESİ (28 Eyl 2026): A taban sacı x 1,5–700 · z −828,5…+39 (önce 8–700 · −826…+35) → açıcı kabininin 4 dikmesi taban sacına tam oturur
    (denetçi bulgu 6: %42–72 oturuyordu) · kaide zarf denetimi A için taban sacı sınırlarını ölçer
  · topping_cad_v25 ile: C ön yüz parçaları (onyuz_, SPEC §2.3 kanatlar 791–892'yi örter) "892'nin altına inmez" satırından ayrıldı → ayrı denetim: tamamı kaidenin önünde
Çalıştır: python yap_kaide_cad_v2.py  →  python ob_calistir.py kaide_cad_v2.py [hizli] [bom]
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kaide_cad_v1.py"), encoding="utf-8").read()
NL = "\n"


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140])
    s = s.replace(a, b)


# ---- başlık ----
degis('"""AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v1 (27 Eyl 2026) — ALÇAK HAT v57 (SPEC_alcak_hat_v57.md · ALCAK_HAT_RESIM1_v4)',
      '"""AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v2 (27 Eyl 2026 gece) — ÖN DÜZLEM +79 (SPEC_on_duzlem_v63.md §2.2) · önceki: kaide_cad_v1.py (yap_kaide_cad_v2.py)' + NL +
      'v2: ön profil z −4 → +35 (dolap üst sacı +39\'a uzar → kaide tam basar; önünde A/C ön çerçevesi +39…+59, panel +59…+79) · A taban sacı x 692 → 700' + NL +
      '    · denetçi düzeltmesi (28 Eyl): A taban sacı x 1,5–700 · z −828,5…+39 (kabin sol/arka sacı + ön çerçeve arkası) → açıcı kabininin 4 dikmesi tam oturur' + NL +
      '    (C dis_taban\'a değer) · KARAR (varsayım): A boyuna profili kolon dikmesinin altına (z −655…−615) + kolon deliği 122 × 52 · TOPPING denetimi TC v25 / TU v14' + NL +
      '    (dosya yoksa v24 / v13, çıktıda yazılır) · yeni denetim: taban sacı ↔ C dis_taban teması, havada parça = 0, dolap üst sacı (store_cad_v8) kaide önünü taşır.' + NL +
      'v1 (27 Eyl 2026) — ALÇAK HAT v57 (SPEC_alcak_hat_v57.md · ALCAK_HAT_RESIM1_v4)')
degis("KZ = (-826.0, -4.0)                       # VARSAYIM pay 4",
      "KZ = (-826.0, 35.0)                       # v2 (SPEC v63 §2.2): ön +35 = dolap üst sacı ön kenarı +39 − 4 (tam basar; ön çerçeve +39…+59) · arka pay 4 VARSAYIM · v1: −4")
degis('KOLON = dict(x=(290.0, 410.0), z=(-660.0, -490.0))   # TC acici_kolonu (x yerel −410…−290 + 700) · dünya',
      'KOLON = dict(x=(290.0, 410.0), z=(-660.0, -490.0))   # TC acici_kolonu (x yerel −410…−290 + 700) · dünya · (kutu sınırı: dikme + üst kol)' + NL +
      'KOLON_DIKME_Z = (-660.0, -610.0)          # v2: kolonun tabana oturan DİKMESİ (topping_cad_v24 acici_kolonu 120 × 50) → taban sacı deliği 122 × 52 (v1: kutu sınırından 122 × 172)' + NL +
      'X_A1 = 700.0                              # v2 (SPEC v63): A taban sacı sağ ucu = C dis_taban solu (v1: 692 → 8 mm boşluk)' + NL +
      'A_SAC_X0 = 1.5                            # v2 denetçi düzeltmesi (28 Eyl): A taban sacı solu = kabin sol yan sacının iç yüzü (v1/v2 ilk: 8 → sol dikmelerin dış duvarı boşta)' + NL +
      'A_SAC_Z = (-828.5, 39.0)                  # v2 denetçi düzeltmesi: arka = kabin arka sacının iç yüzü · ön = ön çerçevenin arkası (+39) → 4 köşe dikmesi taban sacına TAM oturur (önce −826…+35: %42–72)')
degis("A_BOYUNA_Z = (-595.0, -555.0)             # A boyuna orta profil (kolon ekseni z −575 altında)",
      "A_BOYUNA_Z = (-655.0, -615.0)             # v2 KARAR (varsayım): kolon DİKMESİNİN tam altında (dikme z −660…−610, ekseni −635) · v1 −595…−555 dikmenin 15 mm önündeydi (keşif A §5)")
degis('("KAIDE_A", "A mekanizma kaidesi 104 · x 8–692 · y 788–892 · AISI 304 kutu profil 40 × 100 × 2 + üst plaka 4 · açıcı kolonu altında enine + boyuna profil · 1,5 mm taban sacı 892–893,5 (tekne)"),',
      '("KAIDE_A", "A mekanizma kaidesi 104 · x 8–692 (taban sacı 1,5–700) · y 788–892 · z −826…+35 (taban sacı −828,5…+39) · AISI 304 kutu profil 40 × 100 × 2 + üst plaka 4 · açıcı kolonu dikmesi altında enine + boyuna profil · 1,5 mm taban sacı 892–893,5 (tekne + kabin dikmeleri) · v2 ön düzlem +79"),')
degis('("KAIDE_C", "C mekanizma kaidesi 104 · x 708–2492 · y 788–892 · AISI 304 kutu profil 40 × 100 × 2 (çevre + 3 enine + boyuna) + üst plaka 4 · TOPPING dis_taban üstüne oturur"),',
      '("KAIDE_C", "C mekanizma kaidesi 104 · x 708–2492 · y 788–892 · z −826…+35 · AISI 304 kutu profil 40 × 100 × 2 (çevre + 3 enine + boyuna) + üst plaka 4 · TOPPING dis_taban üstüne oturur · v2 ön düzlem +79"),')
degis("ON_BIRIMLER = ()                          # hattın önüne taşan parça YOK (z ≤ −4)",
      "ON_BIRIMLER = ()                          # v2: ön düzlemin (+79) önüne taşan parça YOK (kaide z ≤ +35, önünde ön çerçeve + panel) · v1: z ≤ −4")
# ---- taban sacı ----
degis('    s = kut(A_X[0], A_X[1], Y_MEK, Y_MEK + A_SAC, KZ[0], KZ[1]).cut(kut(KOLON["x"][0] - 1.0, KOLON["x"][1] + 1.0, Y_MEK - 1.0, Y_MEK + A_SAC + 1.0, KOLON["z"][0] - 1.0, KOLON["z"][1] + 1.0))',
      '    s = kut(A_SAC_X0, X_A1, Y_MEK, Y_MEK + A_SAC, A_SAC_Z[0], A_SAC_Z[1]).cut(kut(KOLON["x"][0] - 1.0, KOLON["x"][1] + 1.0, Y_MEK - 1.0, Y_MEK + A_SAC + 1.0, KOLON_DIKME_Z[0] - 1.0, KOLON_DIKME_Z[1] + 1.0))   # v2: x 1,5 → 700 · z −828,5…+39 · delik dikmeye göre')
degis('bom=("A mekanizma taban sacı AISI 304 1,5 mm (TC dis_taban\'ın A\'daki eşi) · açıcı kolonu deliği 122 × 172", 1, "684 × 822", "üretim", "ÜRETİM"))',
      'bom=("A mekanizma taban sacı AISI 304 1,5 mm (TC dis_taban\'ın A\'daki eşi) · açıcı kolonu dikmesi deliği %.0f × %.0f" % (KOLON["x"][1] - KOLON["x"][0] + 2.0, KOLON_DIKME_Z[1] - KOLON_DIKME_Z[0] + 2.0),' + NL +
      '              1, "%.1f × %.1f" % (X_A1 - A_SAC_X0, A_SAC_Z[1] - A_SAC_Z[0]), "üretim · v2: sağ ucu x 700 = C dis_taban solu (SPEC v63) · sol x 1,5 / arka −828,5 / ön +39 = kabin sacları ve ön çerçeve (köşe dikmeleri tam oturur; kaide profilinin 6,5 / 2,5 / 4 mm dışına taşan kenarlar 1,5 sacın kendisi)", "ÜRETİM"))')
# ---- TOPPING denetimi: TC v25 / TU v14 (yoksa v24 / v13) ----
degis('''def topping_denetimi(ps, kontrol):
    import topping_cad_v24 as TC
    TC.PARCALAR[:] = []; TC.modul()''',
      '''def tc_modul():
    """v2: C ajanının yeni TOPPING CAD'i (topping_cad_v25) varsa o, yoksa v24 · (modül, ad)"""
    import importlib
    for ad in ("topping_cad_v25", "topping_cad_v24"):
        if os.path.exists(os.path.join(U, ad + ".py")):
            try:
                return importlib.import_module(ad), ad
            except Exception as e:                                    # yarım yazılmış dosya → bir önceki sürüm
                print("  UYARI: %s yüklenemedi (%s) → bir önceki sürüm" % (ad, str(e)[:120]))
    raise RuntimeError("topping_cad_v24/v25 yok")


def tu_yolu():
    """v2: TU = topping_uno_cad_v14 (C ajanı) varsa o, yoksa v13 (montaj v62'nin kullandığı) · (dosya yolu, ad) · eski v11 yüklemesi kalktı"""
    for ad in ("topping_uno_cad_v14", "topping_uno_cad_v13"):
        if os.path.exists(os.path.join(U, ad + ".py")):
            return os.path.join(U, ad + ".py"), ad
    raise RuntimeError("topping_uno_cad_v13/v14 yok")


def topping_denetimi(ps, kontrol):
    TC, tc_ad = tc_modul()
    print("  (TOPPING CAD: %s)" % tc_ad)
    TC.PARCALAR[:] = []; TC.modul()''')
degis('''    kontrol("A: mekanizma teknesi altı %.1f = A taban sacı üstü %.1f (tekne x %.0f–%.0f)" % (tk.ymin, Y_MEK + A_SAC, tk.xmin, tk.xmax), abs(tk.ymin - Y_MEK - A_SAC) < 0.01)''',
      '''    kontrol("A: mekanizma teknesi altı %.1f = A taban sacı üstü %.1f (tekne x %.0f–%.0f)" % (tk.ymin, Y_MEK + A_SAC, tk.xmin, tk.xmax), abs(tk.ymin - Y_MEK - A_SAC) < 0.01)
    # v2 · A taban sacı sağ ucu = C dis_taban sol ucu (x 700): iki sac uç uca değer, tekne altında boşluk yok
    _ats = [dunya(p).BoundingBox() for p in ps if p["ad"] == "kaide_A_mekanizma_taban_saci"][0]
    kontrol("v2 · A taban sacı x %.1f–%.1f · C dis_taban x %.1f–%.1f → uç uca (boşluk %.2f mm) · aynı kot %.1f / %.1f" % (_ats.xmin, _ats.xmax, dt.xmin, dt.xmax, dt.xmin - _ats.xmax, _ats.ymax, dt.ymax),
            abs(_ats.xmax - dt.xmin) < 0.01 and abs(_ats.ymax - dt.ymax) < 0.01)
    # v2 · kolon DİKMESİ taban sacı deliğinin içinde, altında enine + boyuna profil kesişimi
    _kd = [s_ for a_, s_, _B in TCD if a_ == "acici_kolonu"][0]
    _kes = _kd.intersect(kut(A_X[0], X_A1, Y_MEK - 0.5, Y_MEK + 0.5, KZ[0], KZ[1]).val()).BoundingBox()   # kolonun 892 kotundaki kesiti
    kontrol("v2 · kolon dikmesinin taban kesiti x %.0f–%.0f · z %.0f…%.0f ⊂ delik x %.0f–%.0f · z %.0f…%.0f (122 × 52) · altında enine x %.0f–%.0f + boyuna z %.0f…%.0f"
            % (_kes.xmin, _kes.xmax, _kes.zmin, _kes.zmax, KOLON["x"][0] - 1.0, KOLON["x"][1] + 1.0, KOLON_DIKME_Z[0] - 1.0, KOLON_DIKME_Z[1] + 1.0,
               (KOLON["x"][0] + KOLON["x"][1]) / 2.0 - PR["b"] / 2.0, (KOLON["x"][0] + KOLON["x"][1]) / 2.0 + PR["b"] / 2.0, A_BOYUNA_Z[0], A_BOYUNA_Z[1]),
            KOLON["x"][0] - 1.0 <= _kes.xmin and _kes.xmax <= KOLON["x"][1] + 1.0 and KOLON_DIKME_Z[0] - 1.0 <= _kes.zmin and _kes.zmax <= KOLON_DIKME_Z[1] + 1.0
            and _kes.zmin <= A_BOYUNA_Z[1] and A_BOYUNA_Z[0] <= _kes.zmax)''')
# v2 (28 Eyl, topping_cad_v25 ile): SPEC §2.3 C mekanizma kanatları + ön çerçevesi (onyuz_) kaide bandını (791–892) ÖRTER → "892'nin altına inmez" yalnız
# mekanizma parçalarına uygulanır; onyuz_ parçaları ayrı denetlenir: tamamı kaidenin ÖNÜNDE (z ≥ +39 > kaide ön +35) ve kaideye değmeden
degis('''    kontrol("TC hiçbir parçası %.0f'nin altına inmez (en alçak %.1f)" % (Y_MEK, min(B.ymin for _a, _s, B in TCD)), min(B.ymin for _a, _s, B in TCD) >= Y_MEK - 0.01)''',
      '''    _mek = [(B.ymin, a) for a, _s, B in TCD if not a.startswith("onyuz_")]
    kontrol("TC mekanizma parçaları (%d, onyuz_ ön yüz hariç) %.0f'nin altına inmez (en alçak %s %.1f)" % (len(_mek), Y_MEK, min(_mek)[1], min(_mek)[0]), min(_mek)[0] >= Y_MEK - 0.01)
    _on = [(a, B) for a, _s, B in TCD if a.startswith("onyuz_") and B.ymin < Y_MEK - 0.01]
    if _on:                                                           # v2 · SPEC §2.3: C ön çerçevesi + mekanizma kanatları kaide bandını örter (791–892)
        kontrol("v2 · TC ön yüz parçaları kaide bandında (%d parça, en alt y %.1f) tamamı kaidenin ÖNÜNDE: z ≥ %+.1f > kaide ön %+.0f (SPEC §2.3 kanatlar 791–892'yi örter)"
                % (len(_on), min(B.ymin for _a, B in _on), min(B.zmin for _a, B in _on), KZ[1]), min(B.zmin for _a, B in _on) >= KZ[1] - 0.01)''')
degis('''    import importlib.util as ilu
    sp = ilu.spec_from_file_location("TU11", os.path.join(U, "topping_uno_cad_v11.py"))
    TU = ilu.module_from_spec(sp); sp.loader.exec_module(TU)
    tu = [q for q in TU.P if not q["ad"].startswith(V3_CIKAN)]''',
      '''    import importlib.util as ilu
    tu_yol, tu_ad = tu_yolu()
    print("  (TOPPING UNO: %s)" % tu_ad)
    sp = ilu.spec_from_file_location("TU_KAIDE", tu_yol)
    TU = ilu.module_from_spec(sp); sp.loader.exec_module(TU)
    tu = [q for q in TU.P if not q["ad"].startswith(V3_CIKAN)]
    TUD = [(q["ad"], q["sh"].translate(cq.Vector(700.0, -168.0, 0.0))) for q in tu]     # montaj v62: TU dünya y − 168, x + 700
    cak_tu = []
    for a, sa, A in K:
        for c, sc in TUD:
            B = sc.BoundingBox()
            if QR._bbk(A, B):
                v = sa.intersect(sc).Volume()
                if v > 1.0: cak_tu.append((round(v, 1), a, c))
    kontrol("kaide ↔ TOPPING UNO %s (%d parça, dünya) çakışma = 0" % (tu_ad, len(TUD)), not cak_tu, str(cak_tu[:6]))''')
degis('kontrol("TU (UNO, %d parça, dünya y − 168) en alt %.2f > kaide üstü %.0f · en sol x %.0f (A kaidesine girmez)" % (len(tu), ymin, Y_MEK, xmin), ymin > Y_MEK + A_SAC)',
      'kontrol("TU (%s, %d parça, dünya y − 168) en alt %.2f > kaide üstü %.0f · en sol x %.0f (A kaidesine girmez)" % (tu_ad, len(tu), ymin, Y_MEK, xmin), ymin > Y_MEK + A_SAC)')
# ---- ana program ----
degis('BOM_KLASOR = os.path.join(KOK, "arastirma", "3_KAIDE_v1")', 'BOM_KLASOR = os.path.join(KOK, "arastirma", "3_KAIDE_v2")')
degis('print("KAİDE v1 · %d parça · katı denetimi: %s · %.0f sn" % (len(ps), "hepsi geçerli" if not gec else gec, time.time() - t0))',
      'print("KAİDE v2 · %d parça · katı denetimi: %s · %.0f sn" % (len(ps), "hepsi geçerli" if not gec else gec, time.time() - t0))')
degis('print("DENETİM (kaide_cad_v1)")', 'print("DENETİM (kaide_cad_v2)")')
degis('''        kontrol("%s x %.0f–%.0f · y %.1f–%.1f · z %.0f…%.0f (modül z −830…0 içinde) · kütle %.1f kg" % (kod, x0_, x1_, y0_, y1_, z0_, z1_, vol * RO),
                abs(x0_ - xr[0]) < 0.01 and abs(x1_ - xr[1]) < 0.01 and abs(y0_ - Y_DUZ) < 0.01 and z0_ >= -830.0 and z1_ <= 0.0)''',
      '''        x0_bek, x1_bek = (A_SAC_X0, X_A1) if kod == "KAIDE_A" else xr         # v2: A taban sacı 1,5 → 700 (profiller 8–692)
        z0_bek, z1_bek = (A_SAC_Z[0], A_SAC_Z[1]) if kod == "KAIDE_A" else KZ  # v2: A taban sacı −828,5…+39 (profiller −826…+35)
        kontrol("%s x %.1f–%.0f · y %.1f–%.1f · z %.1f…%.0f (v2: z −830…+39 içinde — ön çerçevenin arkası; ön profil +%.0f) · kütle %.1f kg" % (kod, x0_, x1_, y0_, y1_, z0_, z1_, KZ[1], vol * RO),
                abs(x0_ - x0_bek) < 0.01 and abs(x1_ - x1_bek) < 0.01 and abs(y0_ - Y_DUZ) < 0.01 and abs(z0_ - z0_bek) < 0.01 and z0_ >= -830.0 and abs(z1_ - z1_bek) < 0.01 and z1_ <= 39.0
                and all(abs(dunya(p).BoundingBox().zmax - KZ[1]) < 0.01 for p in ps if p["birim"] == kod and "_profil" in p["ad"] and "_on_profil" in p["ad"]))''')
degis('''    kontrol("kendi arasında çakışma = 0 (%d parça)" % len(ps), not cak, str(len(cak)))''',
      '''    kontrol("kendi arasında çakışma = 0 (%d parça)" % len(ps), not cak, str(len(cak)))
    # v2 · HAVADA PARÇA (denetim_temas_v1): her parça zemine (dolap üstü 788) değen parçalar zinciriyle bağlı
    import denetim_temas_v1 as DT
    hv = DT.havada([(p["ad"], dunya(p)) for p in ps], zemin_y=Y_DUZ)
    DT.yaz(hv, baslik="HAVADA PARCA DENETIMI · kaide_cad_v2")
    kontrol("v2 · havada parça = 0 (%d parça · kök %d · bağlı %d · beyaz liste YOK)" % (hv["parca"], hv["kok"], hv["bagli"]), not hv["bilesen"], str([d_["en"] for d_ in hv["bilesen"]]))
    # v2 · kaide ön profili dolap üst sacının üstünde (store_cad_v8: tavan dış sacı +39'a uzar) — v8 yoksa BİLGİ
    if os.path.exists(os.path.join(U, "store_cad_v8.py")):
        try:
            import store_cad_v8 as SC8
            SC8.PARCALAR[:] = []; SC8.modul()
            _ts = [p for p in SC8.PARCALAR if p["ad"] == "tavan_dis_sac"]
            _tb = _ts[0]["wp"].val().BoundingBox() if _ts else None
            kontrol("v2 · dolap üst sacı (store_cad_v8 tavan_dis_sac) ön kenarı z %s ≥ kaide ön +%.0f · üst yüz y %s = %.0f"
                    % ("%.1f" % _tb.zmax if _tb else "?", KZ[1], "%.1f" % _tb.ymax if _tb else "?", Y_DUZ), bool(_tb) and _tb.zmax >= KZ[1] - 0.01 and abs(_tb.ymax - Y_DUZ) < 0.01)
        except Exception as e:
            print("  BİLGİ · store_cad_v8 yüklenemedi (%s) — B ajanı; kaide ön profilinin tam basması montajda denetlenir" % str(e)[:120])
    else:
        print("  BİLGİ · store_cad_v8 henüz yok (B ajanı) — v7'de tavan dış sacı z −40'ta bitiyor; kaide ön profili (−5…+35) v8 ile tam basar (montajda denetlenir)")''')

io.open(os.path.join(U, "kaide_cad_v2.py"), "w", encoding="utf-8").write(s)
print("kaide_cad_v2.py yazıldı · %d satır" % s.count(NL))
