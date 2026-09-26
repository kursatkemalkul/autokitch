# -*- coding: utf-8 -*-
"""topping_cad_v22 → v23: MAKİNENİN ÖN YÜZÜNDEN TAŞAN PARÇALAR İÇERİ ALINDI (Kemal 26 Eyl: "bize bakan köşesinde çıkıntılar
yapmışsın, fırının dışına çıkmış parçalar"). Görsel denetim (montaj v46) kaynağı ölçtü:
  · bant_motoru ön yüzün 21–78 mm ÖNÜNDE, havada (hiçbir parçaya değmiyor) ve 90° TERS dönük (mili dikey; makara mili z'de)
  · aktarma bandının ön yan sacı z 0…+10 · burun + tahrik makarası mil uçları z +10
  · fire sileceği z +10
Düzeltme: motor tahrik makarasıyla EŞ EKSENLİ, bandın ARKASINDA (mil yüzü arka yan sacın 2 mm arkası) · ön yan sac 10 mm içeri
(bant kenarına 15 mm) · mil uçları ön sacın dış yüzünde biter · fire sileceği ön kenarı z 0 · aktarma bölümünde ön yüz denetimi (z ≤ 0).
Açıcı kafası (motor + kiriş +167/+180, ön koni +24) BİLİNEN açık konu: kavram değişikliği ister, Kemal'e soruldu — burada DOKUNULMADI."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v22.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


degis('    _burun = silz(AKT_X0, BR_Y, BR_R, BZ0, BZ1).union(silz(AKT_X0, BR_Y, 6.0, BZ0 - 35.0, BZ1 + 35.0))',
      '    _burun = silz(AKT_X0, BR_Y, BR_R, BZ0, BZ1).union(silz(AKT_X0, BR_Y, 6.0, BZ0 - 35.0, BZ1 + 25.0))   # v23: ön mil ucu z 0 (ön yüzü geçmez)')
degis('    _tahrik = silz(AKT_X1, BT_Y, BT_R, BZ0, BZ1).union(silz(AKT_X1, BT_Y, 10.0, BZ0 - 35.0, BZ1 + 35.0))',
      '    _tahrik = silz(AKT_X1, BT_Y, BT_R, BZ0, BZ1).union(silz(AKT_X1, BT_Y, 10.0, BZ0 - 35.0, BZ1 + 25.0))   # v23: ön mil ucu z 0')
degis('    for i_, (z0_, z1_) in enumerate(((BZ0 - 35.0, BZ0 - 25.0), (BZ1 + 25.0, BZ1 + 35.0))):',
      '    for i_, (z0_, z1_) in enumerate(((BZ0 - 35.0, BZ0 - 25.0), (BZ1 + 15.0, BZ1 + 25.0))):   # v23: ön sac z −10…0 (v22: 0…+10, ön yüzden taşıyordu)')
degis('''    _bm = nema23()["govde"].rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90.0)
    ekle("bant_motoru", cq.Workplane(obj=_bm.translate(cq.Vector(AKT_X1, BT_Y, BZ1 + 75.0))), "motor",''',
      '''    # v23: motor tahrik makarasıyla EŞ EKSENLİ, bandın ARKASINDA. nema23 gövdesi mil yüzünden −z'ye uzar: mil yüzü arka yan
    # sacın dış yüzünün (BZ0 − 35) 2 mm arkasında → mil (+z) makara miline bakar. v22'de ön yüzün 21–78 mm önündeydi,
    # havadaydı ve x ekseninde 90° döndürülmüştü (mili dikey) — Kemal'in "köşedeki çıkıntı" dediği parça.
    _bm = nema23()["govde"]
    ekle("bant_motoru", cq.Workplane(obj=_bm.translate(cq.Vector(AKT_X1, BT_Y, BZ0 - 37.0))), "motor",''')
degis('''    ekle("fire_silecegi", kut(250.0, 270.0, 125.0, 167.0, ZT - 180.0, ZT + 180.0), "silikon",''',
      '''    ekle("fire_silecegi", kut(250.0, 270.0, 125.0, 167.0, ZT - 180.0, ZT + 170.0), "silikon",   # v23: ön kenar z 0 (v22 +10)''')
# v23 · ÇIKIŞ YARIĞI: görsel denetim — çerçeve açıklığı 24 mm (dünya 1162–1186), en yüksek ürün (hamur 8 + kaşar 6,5 + küp sucuk 14)
# diskte 1196,5'e çıkıyor → üst çubuk küplerin içinden geçiyordu (47,96–49,59 s). Açıklık 44 mm (1162–1206, üstte 9,5 pay).
# Dış yan saçtaki tabla yarığı 132'de bitiyordu (1192) → 150 (1210).
degis('''    ekle("cikis_yarigi_contasi", kut(1792.0, 1798.5, 92.0, 130.0, AKT_Z0 - 10.0, AKT_Z1 + 10.0)
         .cut(kut(1791.0, 1799.5, AKT_Y - 4.0, 126.0, AKT_Z0 - 2.0, AKT_Z1 + 2.0)), "silikon",''',
      '''    ekle("cikis_yarigi_contasi", kut(1792.0, 1798.5, 92.0, 150.0, AKT_Z0 - 10.0, AKT_Z1 + 10.0)
         .cut(kut(1791.0, 1799.5, AKT_Y - 4.0, 146.0, AKT_Z0 - 2.0, AKT_Z1 + 2.0)), "silikon",   # v23: açıklık 24 → 44 mm''')
degis('"dış yan sacta 380 × 38 yarık; pide geçer, soğuk hava ve kir geçmez"', '"açıklık 294 × 44 (en yüksek ürün 28,5 + 9,5 pay); pide geçer, soğuk hava ve kir geçmez"')
degis('        _ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 132.0, -510.0, 0.0))',
      '        _ys = _ys.cut(kut(x - 1.0, x + SAC + 1.0, 1.0, 150.0, -510.0, 0.0))   # v23: 132 → 150 (en yüksek ürün diskte 136,5)')
degis('    print("TOPPING MODULU v22 · %d parca', '    print("TOPPING MODULU v23 · %d parca')
# v23 · ÜRÜN GEÇİŞ DENETİMİ: en yüksek ürünün zarfı (diskte, aktarma yolunda) hiçbir sabit parçaya değmez
degis('''    # ---- çakışma ----
''', '''    # v23 · ÜRÜN GEÇİŞ ZARFI: en yüksek ürün (hamur 8 + kaşar 6,5 + küp sucuk 14 = 28,5) Ø280 (açıcı çıkışı, kural 3), diskte (y 108) aktarma yolunda
    # x: tabla aktarma konumu − 150 … bant ucu. Bant ve disk ürünün ALTINDA (zarf 0,5 mm yukarıdan başlar).
    _ZT = ZK[0] + 30.0                                                   # tabla ekseni (modul() içindeki ZT ile aynı formül)
    _UZ = kut(H.X_AKTARMA - 150.0, 2226.5, 108.5, 108.0 + 28.5 + 0.5, _ZT - 140.0, _ZT + 140.0).val()
    _ug = []
    for p in gercek:
        b_ = p["wp"].val().BoundingBox()
        if b_.xmax < H.X_AKTARMA - 150.0 or b_.xmin > 2235.0 or b_.ymax < 108.5 or b_.ymin > 137.0 or b_.zmax < _ZT - 140.0 or b_.zmin > _ZT + 140.0:
            continue
        try: v_ = p["wp"].val().intersect(_UZ).Volume()
        except Exception: v_ = -1.0
        if v_ > 0.5 or v_ < 0: _ug.append((p["ad"], round(v_, 1)))
    print("URUN GECIS ZARFI (O280 x 28,5 mm urun · disk -> bant): %s" % ("TEMIZ" if not _ug else "%d BULGU %s" % (len(_ug), _ug)))
    assert not _ug, "en yuksek urun aktarma yolunda sabit parcaya carpiyor"

    # ---- çakışma ----
''')
degis('''    print("ISTASYON ZARFI: %s (x %.0f...%.0f, y 0...%.0f, z %.0f...%.0f)" % ("GECTI" if not tas else "TASAN: " + ", ".join(tas), _xmin, _xmax, _ymax, _zmin, _zmax)); assert not tas
''', '''    print("ISTASYON ZARFI: %s (x %.0f...%.0f, y 0...%.0f, z %.0f...%.0f)" % ("GECTI" if not tas else "TASAN: " + ", ".join(tas), _xmin, _xmax, _ymax, _zmin, _zmax)); assert not tas
    # v23 · ÖN YÜZ DENETİMİ: açıcı kafası dışında (bilinen açık konu) HİÇBİR parça makinenin ön yüzünü (z 0) geçemez.
    _ACICI = ("acici", "koni", "kafa")
    _on = [(a, round(b.zmax, 1)) for a, b in bb if b.zmax > 0.01 and not any(k in a for k in _ACICI)]
    print("ON YUZ (z <= 0, acici haric): %s" % ("GECTI" if not _on else "TASAN: %s" % _on)); assert not _on
    _ac = sorted(((round(b.zmax, 1), a) for a, b in bb if b.zmax > 0.01), reverse=True)
    print("   on yuzden tasan (yalniz acici kafasi, bilinen acik konu): %s" % _ac[:8])
''')
# v23: ön sac içeri alınınca teknenin ön dudağıyla (y 1,5–31,5 · z −5…−8) kesişti (2614 mm³) → sacın alt kenarı y 34
# (dudağın 2,5 mm üstü). Tahrik makarası yatak deliği y 64–85, burun 88–101: ikisi de sacın içinde kalır.
degis('        _ys = kut(1802.0, AKT_X1 + 45.0, 21.0, AKT_Y + 18.0, z0_, z1_)',
      '        _ys = kut(1802.0, AKT_X1 + 45.0, 34.0, AKT_Y + 18.0, z0_, z1_)   # v23: alt kenar 21 → 34 (tekne dudağının üstü)')
# v23: STEP/STL üretim dosyaları YAZILMAZ (kural 6.7: SolidWorks/STEP çıktısı yok) — ve v22 klasörüne asla yazılmaz
degis("    # ---- üretim dosyaları ----\n", "    # v23: STEP/STL üretim dosyaları YAZILMAZ (kural 6.7: SolidWorks/STEP çıktısı yok; v22 klasörü korunur)\n"
      "    sys.stdout.flush(); os._exit(0)\n    # ---- üretim dosyaları ----\n")
degis('URETIM = os.path.join(KOK, "arastirma", "3_TOPPING", "topping_modul_v22")', 'URETIM = None   # v23: üretim klasörü YOK (kural 6.7)')
io.open(os.path.join(U, "topping_cad_v23.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v23.py yazildi")
