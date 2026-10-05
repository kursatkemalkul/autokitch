
    RK_BOM = lambda n: ("Kablo rakoru IP68 PA (M16/M20) + kontra somun", n, "sac geçişi", "delik montajda açılır")

    # ======================================================= TOPPING (v2: pano 1215–1765 · sürücüler 1585–1712 · valf adası 1240–1548 · kaset 1778–2318) =====
    KB = ("Kablo kanalı PVC kapaklı (parmak yuvalı) · 28 × 40 / 38 × 40", 2, "arka duvara perçin somunlu", "KD1 sağ cep dikey + KD2 pano altı yatay")
    kanal_kutu("kanal_TOPPING_KD1_dikey", 2421.0, 2449.0, 905.0, 1840.0, -828.3, -788.5, "C", KB)
    kanal_kutu("kanal_TOPPING_KD2_pano_alti", 1705.0, 2449.0, 1840.0, 1879.9, -828.3, -788.5, "C", None)
    KD1 = lambda y, z=-808.0: (2449.2, y, z)
    PANO = lambda x, z: (x, 1879.8, z)
    PANO_ON = lambda x, z: (x, 1862.0, z)
    BOLGE_KURU = (1239.0, 2468.5, 1109.0, 1879.9, -828.5, -630.0)

    # (5) soğutma grubu KLF6.6 → kuru bölme tabanı rakoru G2 → pano (x 1680: sürücü şeritleri 1665 / 1698 arası)
    gecis("G2_kuru_bolme_tabani", (1700.0, 1109.0, -805.0), "y", [("TC", "kuru_bolme_tabani")], "C", r=5.0, t=1.5, yon="+", bom=RK_BOM(1))
    cihaz("TOPPING_sogutma_grubu_KLF66", (1700.0, 1087.0, -805.0), PANO(1680.0, -790.0), 5.0, "C",
          via=[((1700.0, 1140.0, -805.0), ("TOPPING_MODUL|kuru_bolme_tabani",))], on=PANO_ON(1680.0, -790.0), bolge=BOLGE_KURU,
          bom=("Soğutma grubu besleme + kontrol 5 × 1,5 (Secop KLF6.6 → pano)", 1, "", ""))
    # (1) kaset motorları → sürücüler (ön yüz) · en uzaktaki önce
    SUR = [(1698.0, "sucuk_rotor", (2311.0, 1265.5, -807.0)), (1665.0, "sucuk_helezon", (2311.0, 1161.5, -807.0)),
           (1632.0, "kasar_rotor", (2062.0, 1296.5, -807.0)), (1599.0, "kasar_helezon", (2062.0, 1141.5, -807.0))]
    for i, (xs, nm, S) in enumerate(SUR):
        cihaz("TOPPING_motor_%s_surucu_%d" % (nm, i), S, (xs, 1452.0, -699.5), 3.0, "C", itme=(1, -6.0), on=(xs, 1452.0, -684.0),
              via=[(2360.0, S[1] - 6.3, -807.0)] if S[0] > 2200.0 else (),
              bolge=BOLGE_KURU, bom=("Motor kablosu ekranlı 4 × 0,75 + fren (M23 → sürücü)", 4, "", "") if i == 0 else None)
    # (2) sürücüler → pano: kendi x'inde dik şerit (arka duvara 13,5 mm, P-kelepçe arka duvara)
    for i, xs in enumerate((1599.0, 1632.0, 1665.0, 1698.0)):
        sabit("TOPPING_surucu_%d_pano" % i, [(xs, 1477.0, -730.0), (xs, 1490.0, -730.0), (xs, 1490.0, -815.0), (xs, 1879.8, -815.0)], 3.0, "C",
              bom=("Sürücü güç + kontrol kablosu 7 × 0,5 ekranlı (sürücü → pano)", 4, "", "") if i == 0 else None)
    # (3) evaporatör fanları: kaset tavanından rakorla → KD2 alt yüzü
    for i, xf in enumerate((1928.0, 2108.0)):
        gecis("TOPPING_evap_fani_%d" % i, (xf, 1765.0, -714.0), "y", [("TC", "evap_kaseti_dis_sac"), ("TC", "evap_kaseti_PU"), ("TC", "evap_kaseti_ic_sac")],
              "C", r=2.5, t=42.5, yon="+", bom=RK_BOM(2) if i == 0 else None)
        sabit("TOPPING_evap_fani_%d" % i, [(xf, 1712.0, -714.0), (xf, 1800.0, -714.0), (xf, 1800.0, -808.0), (xf, 1839.8, -808.0)], 2.5, "C",
              haric=("TOPPING_MODUL|evap_kaseti_dis_sac", "TOPPING_MODUL|evap_kaseti_PU", "TOPPING_MODUL|evap_kaseti_ic_sac"),
              bom=("Fan kablosu 3 × 0,5 (EC fan → KD2)", 2, "", "") if i == 0 else None)
    # (4) valf adası (çok pinli soket sağ uçta) → dik pano altına (sürücü 0'ın solundan)
    cihaz("TOPPING_valf_adasi", (1548.0, 1462.0, -744.0), PANO(1562.0, -744.0), 4.5, "C", itme=(0, 6.0), on=PANO_ON(1562.0, -744.0),
          bolge=BOLGE_KURU, bom=("Valf adası çok damarlı kablo 25 × 0,34 (D-sub → pano)", 1, "", ""))
    # (6) sağ cep (v3 ile aynı) → KD1
    sabit("TOPPING_sabit_tahrik_motoru", [(2459.0, 986.5, -508.0), (2459.0, 986.5, -808.0), KD1(986.5)], 4.0, "C",
          bom=("Motor kablosu 4 × 1 + fren (sabit tahrik → KD1)", 1, "", ""))
    gecis("TOPPING_enerji_zinciri_sabit_ucu", (2459.0, 923.5, -475.0), "z", [("TC", "enerji_zinciri_kanali")], "C", r=6.0, t=3.0, yon="-", bom=RK_BOM(1))
    sabit("TOPPING_enerji_zinciri_demeti", [(2459.0, 923.5, -460.0), (2459.0, 923.5, -808.0), KD1(923.5)], 6.0, "C", haric=("TOPPING_MODUL|enerji_zinciri_kanali",),
          bom=("Enerji zinciri demeti (araba: dönüş motoru · tabla sıfır sensörü) · zincir sabit ucundan KD1'e", 1, "", "zincir içi kablolar hareketli"))
    sabit("TOPPING_sensor_x_limit_sag", [(2375.0, 920.0, -18.7), (2375.0, 920.0, -16.0), (2375.0, 927.0, -16.0), (2375.0, 927.0, 5.0), (2455.0, 927.0, 5.0),
                                           (2455.0, 1076.0, 5.0), (2455.0, 1076.0, -795.0), (2449.2, 1076.0, -795.0)], 2.0, "C")
    sabit("TOPPING_tabla_bos_sensoru", [(2360.0, 1070.0, -170.0), (2459.0, 1070.0, -170.0), (2459.0, 1070.0, -808.0), KD1(1070.0)], 2.0, "C",
          bom=("Sensör kablosu M8 3 × 0,25 PUR", 4, "", "tabla boş · x sol limit · x sıfır · x sağ limit"))
    # F yükleme bandı motoru → fırın gövdesi arkası G8 → F|TOPPING duvarı G6 → KD1 (motor yüzüne tam dayalı)
    gecis("G8_firin_govde_arka", (2780.0, 1121.5, -651.0), "z", [("FT", "govde_kabugu")], "F", r=4.0, t=1.5, yon="-", bom=RK_BOM(2))
    gecis("G6_F_TOPPING_duvari", (2516.5, 1121.5, -800.0), "x", [("TC", "dis_yan_sag"), ("FU", "f_ust_yan_sol")], "F", r=4.0, t=48.0, yon="+")
    sabit("F_yukleme_bandi_motoru", [(2780.0, 1121.5, -495.5), (2780.0, 1121.5, -651.0), (2780.0, 1121.5, -800.0), (2449.2, 1121.5, -800.0)], 4.0, "F",
          haric=("F_TP10_GOVDE|govde_kabugu", "TOPPING_MODUL|dis_yan_sag", "F_UST_KABIN|f_ust_yan_sol"),
          bom=("Motor kablosu 4 × 1 (yükleme bandı → fırın gövdesi arkası → TOPPING KD1)", 1, "", ""))
    # ======================================================= A (v3 düzeninin −228,5 kaydırılmışı) =======================================================
    DX = -228.5
    kanal_kutu("kanal_A_sag_on_dikey", 1406.0 + DX, 1434.0 + DX, 1050.0, 1545.0, -40.0, -8.0, "A",
               ("Kablo kanalı PVC kapaklı 28 × 32 (A sağ ön köşe, kapak −x yönüne)", 1, "A|TOPPING duvarına konsollu", ""))
    parca("A_sensor_dagitici_kutusu", kut(1406.0 + DX, 1434.0 + DX, 1545.0, 1655.0, -40.0, -10.0), "cihaz_koyu", "A",
          ("M12 pasif dağıtıcı kutusu 8 port (Murrelektronik Exact12 tipi) · kanalın üstünde, A|TOPPING duvarına 2 vida", 1, "110 × 28 × 30", "VARSAYIM: föyden teyit"))
    gecis("G7_A_TOPPING_duvari", (1207.5, 1560.0, -680.0), "x", [("TC", "dis_yan_sol")], "A", r=4.0, t=31.5, yon="-", bom=RK_BOM(1))
    sabit("A_sensor_ana_kablosu", [(1186.5, 1600.0, -40.3), (1186.5, 1600.0, -680.0), (1186.5, 1560.0, -680.0), (1251.5, 1560.0, -680.0),
                                   (1251.5, 1870.0, -680.0), (1251.5, 1870.0, -715.0), (1251.5, 1879.8, -715.0)], 4.0, "A", haric=("TOPPING_MODUL|dis_yan_sol",),
          bom=("Ana kablo M12 8 kutuplu (dağıtıcı → TOPPING panosu)", 1, "", ""))
    AK_BOM = ("Sensör kablosu M12 / M8 PUR (A emniyet · ışık perdesi · x eksen sensörleri → A kanalı)", 6, "", "")
    P_ = lambda pts: [(x + DX, y, z) for x, y, z in pts]
    sabit("A_emniyet_ust", P_([(1386.5, 1539.7, 42.0), (1386.5, 1530.0, 42.0), (1386.5, 1530.0, 0.0), (1414.0, 1530.0, 0.0), (1414.0, 1530.0, -7.8)]), 2.5, "A", bom=AK_BOM)
    sabit("A_emniyet_alt", P_([(1386.5, 1008.5, 42.0), (1386.5, 1020.0, 42.0), (1386.5, 1020.0, 6.0), (1386.5, 1100.0, 6.0), (1414.0, 1100.0, 6.0),
                               (1414.0, 1100.0, -7.8)]), 2.5, "A")
    sabit("A_isik_perdesi_ust", P_([(1206.3, 1175.0, 49.5), (1400.0, 1175.0, 49.5), (1400.0, 1175.0, 0.0), (1420.0, 1175.0, 0.0), (1420.0, 1175.0, -7.8)]), 2.5, "A")
    sabit("A_isik_perdesi_alt", P_([(1206.3, 846.0, 49.5), (1360.0, 846.0, 49.5), (1360.0, 1070.0, 49.5), (1360.0, 1070.0, 0.0), (1426.0, 1070.0, 0.0),
                                    (1426.0, 1070.0, -7.8)]), 2.5, "A")
    sabit("TOPPING_sensor_x_limit_sol", P_([(1056.0, 920.0, -18.7), (1056.0, 920.0, -13.0), (886.0, 920.0, -13.0), (886.0, 1200.0, -13.0), (1390.0, 1200.0, -13.0),
                                            (1390.0, 1200.0, 0.0), (1409.0, 1200.0, 0.0), (1409.0, 1200.0, -7.8)]), 2.0, "C")
    cihaz("TOPPING_sensor_x_home", (1086.0 + DX, 920.0, -19.0), (1416.0 + DX, 1210.0, -7.8), 2.0, "C", itme=(2, 5.7),
          via=[(1086.0 + DX, 902.0, -13.0), (880.0 + DX, 902.0, -13.0)], on=(1416.0 + DX, 1210.0, 0.0), bolge=(840.0 + DX, 1207.5, 893.5, 1860.5, -60.0, 60.0), h=4.0)
    # X ekseni motoru + açıcı motorları (sabit; açıcı başı pnömatik strokla iner → esnek PUR kablo + servis halkası) → A|TOPPING duvarı G9 (çok delikli conta) → pano
    gecis("G9_A_TOPPING_motor", (1207.5, 1640.0, -720.0), "x", [("TC", "dis_yan_sol")], "A", r=5.5, t=31.5, yon="-",
          bom=("Rakor M32 çok delikli conta (3 motor kablosu) · A|TOPPING duvarı", 1, "Lapp SKINTOP MS-SC", ""))
    BOLGE_A = (507.5, 1207.5, 893.5, 1860.5, -828.5, 60.0)
    for j, (nm, S, it, T_) in enumerate((("x_motoru", (647.5, 924.5, -462.0), (2, -6.0), (1195.2, 1634.0, -720.0)),
                                         ("acici_motoru_arka", (857.5, 1103.5, -506.6), (2, -6.0), (1195.2, 1646.0, -714.0)),
                                         ("acici_motoru_on", (887.5, 1145.0, -65.0), (2, -6.0), (1195.2, 1646.0, -726.0)))):
        cihaz("TOPPING_%s" % nm, S, T_, 3.0, "C", itme=it, on=(T_[0] - 25.0, T_[1], T_[2]), bolge=BOLGE_A, h=5.0,
              bom=("Motor kablosu esnek PUR 4 × 0,75 + fren (X ekseni / açıcı · açıcıda 150 mm servis halkası)", 3, "", "sürücüleri TOPPING panosunda") if j == 0 else None)
    sabit("TOPPING_A_motor_demeti", [(1240.0, 1640.0, -720.0), (1300.0, 1640.0, -720.0), (1300.0, 1879.8, -720.0)], 5.5, "C", haric=("TOPPING_MODUL|dis_yan_sol",),
          bom=("Motor demeti (X ekseni + 2 açıcı) G9 → TOPPING panosu", 1, "", ""))

    # ======================================================= K (v2: pompa + PM1704 U_KE'de, tartı fırın üstü önde) =======================================================
    BOLGE_K = (3990.0, 4398.5, 893.5, 1860.5, -828.5, 57.0)
    KT = lambda i: (4176.0 + 8.6 * i, 1640.0, -761.3)
    KT_ON = lambda i: (4176.0 + 8.6 * i, 1640.0, -745.0 + 8.0 * (i % 2))
    kk = [("K_PulsaJet", (4025.0, 1214.3, -146.4), (1, 5.0), 2.5, 0), ("K_urun_sensoru_giris_verici", (4105.0, 1010.0, -438.0), (2, -5.0), 2.0, 1),
          ("K_urun_sensoru_giris_alici", (4105.0, 1010.0, 14.0), (2, 5.0), 2.0, 2),
          ("K_DGRF_SMT8M_0", (4200.0, 1533.3, -161.3), (2, 4.0), 2.0, 4), ("K_DGRF_SMT8M_1", (4200.0, 1408.3, -161.3), (2, 4.0), 2.0, 5),
          ("K_urun_sensoru_durus_verici", (4350.0, 1010.0, -438.0), (2, -5.0), 2.0, 7), ("K_urun_sensoru_durus_alici", (4350.0, 1010.0, 14.0), (2, 5.0), 2.0, 8),
          ("K_EC5000_bant_motoru", (4354.0, 969.0, -484.3), (2, -6.0), 3.0, 9)]
    for i, (nm, S, it, r, kt) in enumerate(kk):
        cihaz(nm, S, KT(kt), r, "K", itme=it, on=KT_ON(kt), bolge=BOLGE_K,
              bom=("Cihaz kabloları K (motor 4 × 0,75 · sensör M8/M12 PUR · PulsaJet M8)", len(kk) + 2, "", "") if i == 0 else None)
    # U_KE'deki yağ pompası + PM1704 → K iniş kanalının yan yüzü (x 4280, kanal K panosuna iner)
    BOLGE_UKE = (4016.5, 4400.0, 1863.5, 2125.0, -828.5, -600.0)
    cihaz("K_yag_pompasi_GJ-N21", (4150.0, 1944.6, -739.0), (4279.8, 1944.6, -760.0), 3.0, "K", itme=(2, -6.0), on=(4258.0, 1944.6, -760.0), bolge=BOLGE_UKE)
    cihaz("K_yag_basinc_PM1704", (4225.0, 2069.7, -705.0), (4279.8, 2080.0, -760.0), 2.0, "K", itme=(1, 5.0), on=(4258.0, 2080.0, -760.0), bolge=BOLGE_UKE)
    # tartı yük hücresi (fırın üstü, ön): F|K duvarı rakoru G4 → K içinde SIWAREX alt yüzü
    gecis("G4_tarti_FK_duvari", (3983.5, 1387.5, -123.0), "x", [("FU", "f_ust_yan_sag"), ("KS", "sol_sac_urun_girisi")], "K", r=2.5, t=18.0, yon="-", bom=RK_BOM(1))
    cihaz("K_tarti_yuk_hucresi", (3930.0, 1387.5, -123.0), (4305.0, 1709.8, -773.0), 2.5, "K", on=(4305.0, 1692.0, -773.0),
          via=[((4012.0, 1387.5, -123.0), ("F_UST_KABIN|f_ust_yan_sag", "K_GOVDE|sol_sac_urun_girisi"))], bolge=BOLGE_K,
          bom=("Yük hücresi kablosu 6 × 0,25 ekranlı (PW15AH → SIWAREX WP231)", 1, "", ""))

    # ======================================================= DOLAP (B) =======================================================
    D = {ad: sb for ad, s_, sb in EO.dokum()}
    kanallar = {k.split("|")[1].replace("kablo_kanali_", ""): v for k, v in D.items() if k.startswith("B_KABLO|kablo_kanali_K")}
    n = 0
    for k, sb in sorted(D.items()):
        if not (k.startswith("CEK_") and k.endswith("_reed_acik")): continue
        grp = k.split("|")[0]; kol = grp.split("_")[1]
        kn = kanallar.get(kol); rk = D.get(k.replace("_reed_acik", "_reed_kapali"))
        if kn is None or rk is None: RAPOR["bulunamadi"].append(("DOLAP_reed_" + grp, sb[:2], sb[2:4], "kanal/kapalı sensör yok")); continue
        rxc, ryc = (sb[0] + sb[1]) / 2.0, (sb[2] + sb[3]) / 2.0
        cx, cy = sb[0] - 2.3, sb[3] + 2.0
        yc = min(ryc, kn[3] - 12.0)
        a_ = [(rxc, ryc, sb[4]), (rxc, ryc, sb[4] - 4.0), (cx, ryc, sb[4] - 4.0), (cx, cy, sb[4] - 4.0), (cx, cy, -760.0), (cx, yc, -760.0),
              (cx, yc, -777.0), (kn[0] - 0.2, yc, -777.0)]
        k_ = [(rxc, ryc, rk[4]), (rxc, ryc, -771.0), (rxc, yc, -771.0), (kn[0] - 0.2, yc, -771.0)]
        for nm, pts in (("acik", a_), ("kapali", k_)):
            q = [pts[0]]
            for p in pts[1:]:
                if math.dist(p, q[-1]) > 1e-6: q.append(p)
            sh = boru(q, 2.0)
            ok, engel = ER.temiz(sh)
            if not ok:
                RAPOR["bulunamadi"].append(("DOLAP_reed_%s_%s" % (grp, nm), q[0], q[-1], engel)); continue
            ad = "DOLAP_reed_%s_%s" % (grp, nm)
            parca("kablo_%s" % ad, sh, "kablo", "B",
                  ("Reed sensör kablosu 2 × 0,25 PUR (lamaya kablo bağıyla · kolon kanalına)", 42, "", "motor M12 soketi zaten kanala dayalı") if n == 0 else None)
            n += 1
            RAPOR["yol"].append((ad, round(EO.uzunluk(q)), len(q) - 1, 0))
    # soğutma grubu (Secop NLE8.8CN, fırın altı teknik bölme): kompresör üstünden sola · emiş yan sacının dışından arkaya · perde lastiği → klemens ön yüzü
    DELIKLER.append(("SC", "v22_teknik_perde", cq.Solid.makeCylinder(4.6, 12.0, V(2543.5, 314.5, -660.0), V(0, 0, 1)), "Secop kablosu perde geçiş lastiği"))
    sabit("DOLAP_secop_NLE88", [(2733.8, 308.5, -244.0), (2733.8, 314.5, -244.0), (2543.5, 314.5, -244.0), (2543.5, 314.5, -712.0), (2800.0, 314.5, -712.0),
                                (2800.0, 314.5, -735.3)], 4.0, "B", haric=("B_SOGUTMA|v22_teknik_perde",),
          bom=("Kompresör kablosu 3 × 1,5 + termik (Secop NLE8.8CN → dolap panosu)", 1, "", "teknik perdede kablo lastiği"))
    BOLGE_B = (509.0, 4242.0, 125.0, 786.0, -828.5, -560.0)
    for i, (nm, S, xk, yk) in enumerate((("fan_sol_1", (1555.0, 509.5, -628.5), 1455.0, 668.0), ("fan_sol_2", (1735.0, 509.5, -628.5), 2070.0, 668.0),
                                         ("fan_sag_1", (3297.0, 422.0, -628.5), 3197.0, 520.0), ("fan_sag_2", (3477.0, 422.0, -628.5), 3812.0, 520.0))):
        sg = 1.0 if S[0] > xk else -1.0
        cihaz("DOLAP_evap_%s" % nm, S, (xk + sg * 0.2, yk, -777.0), 2.5, "B", itme=(1, 6.0), on=(xk + sg * 30.0, yk, -777.0), bolge=BOLGE_B,
              bom=("Fan kablosu 3 × 0,5 (4414 FL → kolon kanalı)", 4, "", "") if i == 0 else None)
    return RAPOR
