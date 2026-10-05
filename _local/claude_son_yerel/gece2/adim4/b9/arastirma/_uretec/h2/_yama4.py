import io
def yama(P, pairs):
    s = io.open(P, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (P, a[:80], s.count(a))
        s = s.replace(a, b)
    io.open(P, "w", encoding="utf-8").write(s)
# ---- kaide: arka emiş penceresi + filtre · enine profil kalıntısı (6 mm açık C) → dolu lama ----
yama("h2_kaide_v1.py", [
("""    PARCALAR[:] = out
    PROFIL_BOM.clear()""",
"""    # v2 · ARKA EMİŞ (Claude 30 Eyl): TOPPING daralınca yoğuşma ünitesinin EMİŞ bölgesi 1209–1631,5'e indi (v1 701,5–1631,5) → ön ızgara 5 kolon
    #      (v1 10) · 240 m³/h için ön yarıklar tek başına 5,3 m/s (v1 kuralı ≤ 3,5) → C kaidesinin ARKA profiline ön pencereyle aynı pencere + yıkanabilir
    #      filtre: hava makinenin arkasından da girer (fırın üstü kabin de arkadaki panjurlardan nefes alıyor → arkada boşluk şartı zaten var)
    for p in out:
        if p["ad"] == "kaide_C_arka_profil":
            sh = dunya(p)
            for a_, b_ in C_ARKA_PENCERE_X:
                sh = sh.cut(_kut(a_, b_, C_PENCERE_Y[0], C_PENCERE_Y[1], KZ_C[0] - 1.0, KZ_C[0] + PR["b"] + 1.0))
            p["wp"] = cq.Workplane("XY").add(_tek(sh))
        elif p["ad"] == "kaide_C_enine_profil_1":                                                # dilimden kalan 6 mm'lik açık C → dolu lama 6 × 100
            b = dunya(p).BoundingBox()
            p["wp"] = cq.Workplane("XY").add(_kut(b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))
            p["bom"] = ("Enine lama 6 × 100 AISI 304 (v2: dilimden kalan enine profil yerine dolu lama)", 1, "%.0f boy · ön / arka profile kaynak" % (b.zmax - b.zmin),
                        "v2 · emiş gözü ile ünite cebi arasında", "ÜRETİM")
    for a_, b_ in C_ARKA_PENCERE_X:
        out.append(dict(ad="kaide_C_arka_emis_filtresi", wp=cq.Workplane("XY").add(_kut(a_, b_, C_PENCERE_Y[0], C_PENCERE_Y[1], KZ_C[0] + PR["b"], KZ_C[0] + PR["b"] + 14.0)),
                        mal="paslanmaz", birim="KAIDE_C", grup="SABIT", kaynak="v2 · Claude 30 Eyl",
                        bom=("Kondenser ARKA emiş filtresi · yıkanabilir paslanmaz tel örgü + çerçeve", 1, "%.1f × %.0f × 14 · arka profilin iç yüzünde 2 klips" % (b_ - a_, C_PENCERE_Y[1] - C_PENCERE_Y[0]),
                             "v2 · ön filtreyle aynı bakım (ayda 1 · VARSAYIM) · makine arkasında ≥ 50 mm boşluk şartı [V]", "SATIN ALMA")))
    PARCALAR[:] = out
    PROFIL_BOM.clear()"""),
("""def kur():
    \"\"\"v2 kaide parçaları""", """C_ARKA_PENCERE_X = ((C_PENCERE_X["emis"][0][0], C_PENCERE_X["emis"][0][1]),)   # v2 · arka emiş = ön emiş penceresiyle aynı x (1257,5–1614)


def kur():
    \"\"\"v2 kaide parçaları"""),
])
# ---- TOPPING: ızgara 65 hatve · sol kanat yalnız EMİŞ (5) · sağ kanat ATIŞ (9) · aralık 292 · filtre emişin arkasında ----
yama("h2_topping_v1.py", [
("""    IZ_EMIS = [1257.5 + 70.0 * i_ for i_ in range(5)]                                            # 1257,5 … 1597,5
    IZ_ATIS = {"sol": [1700.0, 1770.0], "sag": [1874.5 + 70.0 * i_ for i_ in range(8)]}         # 1700–1830 · 1874,5–2424,5""",
"""    IZ_EMIS, IZ_ATIS = IZGARA["emis"], {"sol": [], "sag": IZGARA["atis"]}"""),
("""    ek("onyuz_mekanizma_kanadi_sol_filtre", kut(IZ_EMIS[0] - 5.0, IZ_EMIS[-1] + 65.0, 823.0, 886.0, TC0.Z_PAN_C[0] + 3.0, Z_ON - 1.5), "pom",
       _bom("Kondenser emiş filtresi · yıkanabilir paslanmaz tel örgü + çerçeve", 1, "%.0f × 63 × 15,5 · sol kanadın alt bandında 2 klipsle" % (IZ_EMIS[-1] + 70.0 - IZ_EMIS[0]),""",
"""    ek("onyuz_mekanizma_kanadi_sol_filtre", kut(IZ_EMIS[0] - 5.0, IZ_EMIS[-1] + 65.0, 823.0, 886.0, TC0.Z_PAN_C[0] + 3.0, Z_ON - 1.5), "pom",
       _bom("Kondenser emiş filtresi · yıkanabilir paslanmaz tel örgü + çerçeve", 1, "%.0f × 63 × 15,5 · sol kanadın alt bandında 2 klipsle" % (IZ_EMIS[-1] + 70.0 - IZ_EMIS[0]),"""),
("""FIRE_DX = 1535.0 - 1470.0 """, """# soğutma grubu (KLF6.6CND) hava yolu v2: sol kanat yalnız EMİŞ (5 yarık, ayırma perdesinin 1631,5 solunda) + C kaidesinin ARKA penceresi (h2_kaide_v1) ·
# sağ kanat ATIŞ (9 yarık, kaide atış pencereleri 1630–2090 · 2150–2450 önünde) · 65 hatve (v1 70) · emiş / atış yarıkları arası ≥ 250
IZGARA = {"emis": [1257.5 + 65.0 * i_ for i_ in range(5)], "atis": [1869.5 + 65.0 * i_ for i_ in range(9)]}   # 1257,5–1577,5 · 1869,5–2449,5
FIRE_DX = 1535.0 - 1470.0 """),
("""# ================================================================ KUR (önbellekli)""",
"""def hava_yolu():
    \"\"\"v1 denetimi (topping_cad_v32 · dunya_denetimi 8) v2 ölçüsüyle: 240 m³/h (KLF6.6CND 32 °C'de atılan ısı, hava 10 K) · yarık etkin alanı yalnız kaide
    penceresinin önündekiler · arka pencere filtreli (açık oran 0,6 [V]) · sınırlar v1: hız ≤ 3,5 m/s · emiş / atış yarıkları arası ≥ 250\"\"\"
    import h2_kaide_v1 as KD2
    Q = (TC0.KLF66[32] + 279.0 * 1.1) / (1.2 * 1006.0 * 10.0)
    et = lambda xs, pen: sum(max(0.0, min(x_ + 60.0, b_) - max(x_, a_)) for x_ in xs for a_, b_ in pen) * 6.0 * len(TC0.IZGARA_Y) * 1e-6
    pw = lambda pen: sum(b_ - a_ for a_, b_ in pen) * (KD2.C_PENCERE_Y[1] - KD2.C_PENCERE_Y[0]) * 1e-6
    on_e = et(IZGARA["emis"], KD2.C_PENCERE_X["emis"]); arka_e = 0.6 * pw(KD2.C_ARKA_PENCERE_X); at = et(IZGARA["atis"], KD2.C_PENCERE_X["atis"])
    ara = IZGARA["atis"][0] - (IZGARA["emis"][-1] + 60.0)
    d = dict(Q_m3h=Q * 3600.0, emis_on=on_e, emis_arka=arka_e, v_emis=Q / (on_e + arka_e), v_emis_yalniz_on=Q / on_e, atis=at, v_atis=Q / at, ara=ara,
             sol_ayirma=IZGARA["emis"][-1] + 60.0 <= T_AYIRMA, sag_ayirma=IZGARA["atis"][0] >= T_AYIRMA)
    d["gecti"] = d["v_emis"] <= 3.5 and d["v_atis"] <= 3.5 and ara >= 250.0 and d["sol_ayirma"] and d["sag_ayirma"]
    return d


T_AYIRMA = TC0.AYIRMA_X


# ================================================================ KUR (önbellekli)"""),
])
print("ok")
