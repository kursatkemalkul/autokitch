# -*- coding: utf-8 -*-
"""store_cad_v10 → store_cad_v11 (29 Eyl 2026 · YEREL) — Kemal (alttan görünüş): "bu taraf neden soldaki gibi değil, öyle yap, daha düzgün temiz olur"
+ (K4 | K5 önü): "orası adamın ayağına takılır, arasında boşluk var, sac ile yalıtım arası".
1 · FIRIN ALTI AYAKLARI KENARDA: taşıyıcı dikmelerin arka ayakları z −620 → −760 (soldaki gibi: bütün ayaklar z −110 / −760) → alt şase iki boyuna profil
    boydan boya kenarda + her ayak x'inde enine profil; içeride ikinci çerçeve YOK. Arka dikme (−620) enine profilin tam üstünde kalır (yük: dikme → taban → enine 60×80×3 → ayak).
2 · K4 | K5 BÖLMESİNİN ÖNÜ KAPALI: sol taraftaki taban kademe sacının aynası — bölme sacı (x 2500) tabanda (y 124,5–164,5) ön dönüşe (+37,5) kadar uzar,
    arkası PU ile dolu; ön dönüşün ucu ile bölme arasında cep kalmaz.
Önceki: store_cad_v10.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v10.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v10 (29 Eyl 2026 · yap_store_cad_v10.py)',
      '"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v11 (29 Eyl 2026 · yap_store_cad_v11.py): FIRIN ALTI AYAKLARI KENARDA (soldaki gibi z −110 / −760)'
      ' · K4|K5 BÖLMESİNİN ÖNÜ KAPALI (kademe sacı aynası)' + NL + 'v10: ÜRETİM MODELİ v10 (29 Eyl 2026 · yap_store_cad_v10.py)')
# ---- 1 · ayaklar ----
degis('AYAK_XZ = ([(x_, z_) for x_ in (60.0, 1000.0, 1960.0) for z_ in (-110.0, -760.0)] + [(x_, z_) for x_ in TD_X for z_ in TD_Z]',
      'AYAK_Z = (-110.0, -760.0)                                            # v11: BÜTÜN ayaklar bu iki sırada (Kemal: fırın altı da soldaki gibi kenarda)' + NL +
      'AYAK_XZ = ([(x_, z_) for x_ in (60.0, 1000.0, 1960.0) for z_ in AYAK_Z] + [(x_, z_) for x_ in TD_X for z_ in AYAK_Z]')
degis('''            assert any(abs(xc_ - ax) < 0.05 and abs(zc_ - az) < 0.05 for ax, az in AYAK_XZ), "%s altinda ayak yok" % a''',
      '''            # v11: ayak dikmenin x'inde, iki sırada (−110 / −760) → dikme o x'teki enine alt şase profilinin üstünde (Codex modüler v1: her ayak x'inde enine profil)
            assert any(abs(xc_ - ax) < 0.05 and abs(zc_ - az) < 0.05 for ax, az in AYAK_XZ) or (
                any(abs(xc_ - ax) < 0.05 and abs(az - AYAK_Z[0]) < 0.05 for ax, az in AYAK_XZ) and any(abs(xc_ - ax) < 0.05 and abs(az - AYAK_Z[1]) < 0.05 for ax, az in AYAK_XZ)
                and AYAK_Z[1] < zc_ < AYAK_Z[0]), "%s altinda ayak / enine profil yok" % a''')
degis('''    print("   dikme 30×30×2: en yuklu %.0f N ·''',
      '''    print("   v11 AYAKLAR: %d adet · hepsi z %s (firin alti dahil, soldaki gibi kenarda) · arka dikme z %.0f enine alt sase profilinin ustunde (ayaklar arasi %.0f)"
          % (len(AYAK_XZ), " / ".join("%.0f" % z_ for z_ in AYAK_Z), TD_Z[1], AYAK_Z[0] - AYAK_Z[1]))
    assert {round(z_, 1) for _x, z_ in AYAK_XZ} == {round(z_, 1) for z_ in AYAK_Z}, "v11: ayak sirasi kenarda degil"
    print("   dikme 30×30×2: en yuklu %.0f N ·''')
# ---- 2 · K4 | K5 bölmesinin önü ----
degis('''    sac("bolme_3_sac_a", (XB[3], XB[3] + 1.0, Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)''',
      '''    sac("bolme_3_sac_a", (XB[3], XB[3] + 1.0, Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)
    _K3 = (XB[3], XB[3] + 1.0, Y_PLINT + 1.5, Y_TABAN, Z_CER0, ZP1)     # v11: tabanda ön dönüşe kadar (sol K4 kademe sacının aynası) · tek parça
    assert PARCALAR[-1]["ad"] == "bolme_3_sac_a"; PARCALAR[-1]["wp"] = PARCALAR[-1]["wp"].union(kut(*_K3)); SACK.append(_K3)''')
degis('''    pu("bolme_3_pu", (XB[3] + 1.0, XB[3] + BOLME - 1.0, Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)''',
      '''    pu("bolme_3_pu", (XB[3] + 1.0, XB[3] + BOLME - 1.0, Y_PLINT + 1.5, Y_TAVAN, Z_ARKA, Z_CER0), ek=g4)
    _P3 = (XB[3] + 1.0, XB[3] + BOLME - 1.0, Y_PLINT + 1.5, Y_TABAN, Z_CER0, ZP1)   # v11: ön cep PU ile dolu (ön dönüşün arkası)
    assert PARCALAR[-1]["ad"] == "bolme_3_pu"; PARCALAR[-1]["wp"] = PARCALAR[-1]["wp"].union(kut(*_P3)); PUK.append(_P3)''')
# denetim: cep kapalı mı (katılardan)
degis('''    # ---- v7 · FIRIN ALTI ISI KALKANI: PU yok, hava boşluğu (katılardan) ----''',
      '''    # ---- v11 · K4 | K5 bölmesinin önü: x 2500–2535 · y 124,5–164,5 · z +23…+37,5 cebi dolu mu (katılardan) ----
    _cep = kut(BOLME_X[3] + 0.2, BOLME_X[3] + BOLME - 0.2, Y_PLINT + 1.7, Y_TABAN - 0.2, Z_CER0 + 0.2, ZP1_ON - 0.2).val()
    _dol = sum(_cep.intersect(p["wp"].val()).Volume() for p in PARCALAR if p["ad"] in ("bolme_3_sac_a", "bolme_3_pu", "taban_pu_F"))   # taban PU'su 2534'ten başlar (cebin son 0,8 mm'si)
    print("K4|K5 BOLME ONU (v11): cep %.0f mm3 · dolu %.0f mm3 (sac + PU) -> %s" % (_cep.Volume(), _dol, "KAPALI" if _dol >= 0.99 * _cep.Volume() else "ACIK"))
    assert _dol >= 0.99 * _cep.Volume(), "v11: K4|K5 bolme onunde cep var"
    # ---- v7 · FIRIN ALTI ISI KALKANI: PU yok, hava boşluğu (katılardan) ----''')
compile(s, "store_cad_v11.py", "exec")
io.open(os.path.join(U, "store_cad_v11.py"), "w", encoding="utf-8").write(s)
print("store_cad_v11.py yazildi")
