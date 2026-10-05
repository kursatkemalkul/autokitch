# -*- coding: utf-8 -*-
import io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h3_topping_v1.py")
s = io.open(P, encoding="utf-8").read()
R = [
("""        if a.startswith(("sos", "harc")):
            k = "sos" if a.startswith("sos") else "harc"
            TU.append(dict(q, sh=kay(DX_UST[k], DY_U))); _say(sayu, "ust_kat"); continue""",
"""        if a == "harc_hazne_bizim":
            _say(sayu, "v3_yeniden"); continue                                                   # v3 · harç haznesi 380 genişlikte yeniden (yeni_tu a0)
        if a.startswith(("sos", "harc")):
            k = "sos" if a.startswith("sos") else "harc"
            TU.append(dict(q, sh=kay(DX_UST[k], DY_U))); _say(sayu, "ust_kat"); continue"""),
("""    bul = {q["ad"]: q["sh"] for q in TUm}
    X0, X1 = KX; ZF = IZ[1]""",
"""    bul = {q["ad"]: q["sh"] for q in TUm}
    X0, X1 = KX; ZF = IZ[1]
    # ---- (a0) v3 · HARÇ HAZNESİ 380 × 440 (v2 440 × 440 sağ duvara taşardı) · üstü dünya 2099 · aynı boyun + huni kurgusu (topping_uno_cad_v19) ----
    cxT = X_V1["harc"] - TU0.DX_DUNYA; hw = HARC_HAZNE["w"]; hustT = HARC_HAZNE["ust"] - (TU0.DY_DUNYA + DY_U)
    dis = TU0.loft_y(TU0.cember_y(cxT, 1452, TU0.VZ, 32), TU0.dikdort_y(cxT, 1632, -340.0, hw, 440)).fuse(TU0.kut(cxT - hw / 2, cxT + hw / 2, 1632, hustT, -120, -560).val())
    ic = TU0.loft_y(TU0.cember_y(cxT, 1451, TU0.VZ, 30.3), TU0.dikdort_y(cxT, 1632.5, -340.0, hw - 3, 437)).fuse(
        TU0.kut(cxT - hw / 2 + 1.5, cxT + hw / 2 - 1.5, 1632, hustT + 1, -121.5, -558.5).val())
    ek("harc_hazne_bizim", tasi(dis.cut(ic), TU0.DX_DUNYA + DX_UST["harc"], TU0.DY_DUNYA + DY_U), "paslanmaz",
       "v3 · bizim soğuk hazne %.0f × 440 · üstü %.0f · brüt %.1f L ≥ 2 gün harç %.1f L (200 lahmacun × 105 ml)" % (hw, HARC_HAZNE["ust"], ic.Volume() / 1e6, HARC_HAZNE["iki_gun_L"]),
       kaynak="V3")"""),
("""HORTUM_R = 21.0 """, """HARC_HAZNE = dict(w=380.0, ust=2099.0, iki_gun_L=2 * 200 * 105.0 / 1000.0)   # v3 · 2247 ± 190 → 2057–2437 (iç duvar 2440) · 42 L gerekli
HORTUM_R = 21.0 """),
]
for a, b in R:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
