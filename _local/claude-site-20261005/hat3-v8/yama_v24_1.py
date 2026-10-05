# -*- coding: utf-8 -*-
import io, os
H2 = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat2-v4\arastirma\_uretec\h2"


def yama(dosya, ciftler):
    P = os.path.join(H2, dosya)
    s = io.open(P, encoding="utf-8").read()
    for a, b in ciftler:
        assert s.count(a) == 1, (dosya, a[:100], s.count(a))
        s = s.replace(a, b)
    io.open(P, "w", encoding="utf-8").write(s)
    print("yamalandı:", dosya, len(ciftler))


yama("h2_elk_hat_v1.py", [
    # dolap panosu demeti rölelerin önünden (röle ön yüzü −686,5)
    ('B_PANO_KOL = dict(x=2580.0, z_kanal=-630.0, z_arka=-693.0)', 'B_PANO_KOL = dict(x=2580.0, z_kanal=-630.0, z_arka=-675.0)'),
    # E dış dikey kanal + U_KE girişi + yan kanal: E üstündeki 60'lık kutu yığınının (y ≤ 2146,5) ÜSTÜNDEN (y 2148–2176)
    ('E_RISER = dict(x=(5232.0, 5292.0), z=(-40.0, 20.0), y=(0.0, 2160.0))', 'E_RISER = dict(x=(5232.0, 5292.0), z=(-40.0, 20.0), y=(0.0, 2176.0))'),
    ('''    DELIKLER.append(("UD", "ust_ke_yan_sag", kut(5210.0, 5233.0, 2110.0, 2158.0, z0 + 3.0, z1 - 3.0), "dış dikey kanal girişi (kapak dahil)"))
    g, k = u_kanal_x(5140.0, x0 + T, 2112.0, 2158.0, z0 + 3.0, z1 - 3.0, acik="-y")''',
     '''    DELIKLER.append(("UD", "ust_ke_yan_sag", kut(5210.0, 5233.0, 2146.0, 2178.0, z0 + 3.0, z1 - 3.0), "dış dikey kanal girişi (kapak dahil)"))
    g, k = u_kanal_x(5140.0, x0 + T, 2149.5, 2176.0, z0 + 3.0, z1 - 3.0, acik="-y")'''),
    ('''    g = kut(5140.0, 5200.0, ys0, ys1, zs1, z0 + 3.0).cut(kut(5140.0 + T, 5200.0 - T, ys0 + T, ys1 + 1.0, zs1 - 1.0, z0 + 4.0))
    ekle("ust_hat_U_KE_yan", g, "kanal", B, bom=("Üst hat kablo kanalı PVC 60 × 40 + kapak (U_KE)", 1, "arka / yan saca konsollu", ""))
    ekle("ust_hat_U_KE_yan_kapak", kut(5140.0, 5200.0, ys1, ys1 + T, zs1, z0 + 3.0), "kanal", B)''',
     '''    g = kut(5140.0, 5200.0, 2148.0, 2176.0, zs1 - 30.0, z0 + 3.0).cut(kut(5140.0 + T, 5200.0 - T, 2148.0 + T, 2177.0, zs1 - 31.0, z0 + 4.0))
    ekle("ust_hat_U_KE_yan", g, "kanal", B, bom=("Üst hat kablo kanalı PVC 60 × 28 + kapak (U_KE yan · kutu yığınının üstünden)", 1, "yan saca konsollu", ""))
    ekle("ust_hat_U_KE_yan_kapak", kut(5140.0, 5200.0, 2176.0, 2176.0 + T, zs1 - 30.0, z0 + 3.0), "kanal", B)
    DELIKLER.append(("UD", "ust_ke_K_E_bolme", kut(4399.0, 4403.0, ys0 - 1.0, ys1 + 2.0, zs0 - 1.0, zs1 + 1.0), "üst hat K|E bölme geçişi"))'''),
    # E inişi pano plakasının (z ≤ −822) önünde · koli rafı bileziği aynı z
    ('''    DELIKLER.append(("UD", "ust_e_koli_rafi", sil((5100.0, 1890.0, -811.0), (5100.0, 1898.0, -811.0), 9.0), "iniş E kablo geçişi (lastik bilezik)"))
    ekle("inis_E_raf_bilezigi", sil((5100.0, 1895.0, -811.0), (5100.0, 1897.0, -811.0), 11.0).cut(sil((5100.0, 1894.0, -811.0), (5100.0, 1898.0, -811.0), 6.0)), "rakor", B)''',
     '''    DELIKLER.append(("UD", "ust_e_koli_rafi", sil((5100.0, 1890.0, -805.0), (5100.0, 1898.0, -805.0), 9.0), "iniş E kablo geçişi (lastik bilezik)"))
    ekle("inis_E_raf_bilezigi", sil((5100.0, 1895.0, -805.0), (5100.0, 1897.0, -805.0), 11.0).cut(sil((5100.0, 1894.0, -805.0), (5100.0, 1898.0, -805.0), 6.0)), "rakor", B)'''),
    ('''("E", 5100.0, 1840.0, -826.0, (("UD", "ust_ke_taban_sac"), ("KC", "ust_sac")))''', '''("E", 5100.0, 1840.0, -820.0, (("UD", "ust_ke_taban_sac"), ("KC", "ust_sac")))'''),
])
yama("h2_elk_ist_v1.py", [
    # Secop: emiş yan sacından lastikle çık · rölelerin üstünden (y 380) · klemens ön yüzüne
    ('''    DELIKLER.append(("SC", "v22_teknik_perde", cq.Solid.makeCylinder(4.6, 12.0, V(2543.5, 314.5, -660.0), V(0, 0, 1)), "Secop kablosu perde geçiş lastiği"))
    sabit("DOLAP_secop_NLE88", [(2733.8, 308.5, -244.0), (2733.8, 314.5, -244.0), (2543.5, 314.5, -244.0), (2543.5, 314.5, -712.0), (2800.0, 314.5, -712.0),
                                (2800.0, 314.5, -735.3)], 4.0, "B", haric=("B_SOGUTMA|v22_teknik_perde",),''',
     '''    DELIKLER.append(("SC", "v22_teknik_perde", cq.Solid.makeCylinder(4.6, 12.0, V(2543.5, 314.5, -660.0), V(0, 0, 1)), "Secop kablosu perde geçiş lastiği"))
    DELIKLER.append(("SC", "k4_emis_yan_sac_sol", cq.Solid.makeCylinder(4.6, 12.0, V(2547.0, 314.5, -244.0), V(1, 0, 0)), "Secop kablosu emiş yan sacı lastiği"))
    sabit("DOLAP_secop_NLE88", [(2733.8, 308.5, -244.0), (2733.8, 314.5, -244.0), (2543.5, 314.5, -244.0), (2543.5, 314.5, -700.0), (2543.5, 380.0, -700.0),
                                (2800.0, 380.0, -700.0), (2800.0, 345.0, -700.0), (2800.0, 345.0, -735.3)], 4.0, "B",
          haric=("B_SOGUTMA|v22_teknik_perde", "B_SOGUTMA|k4_emis_yan_sac_sol"),'''),
    # sol evaporatör fanları ikisi de K2 kanalına (K3'e giden yol çekmece kolonundan geçemiyor)
    ('''("fan_sol_2", (1735.0, 509.5, -628.5), 2070.0, 668.0)''', '''("fan_sol_2", (1735.0, 509.5, -628.5), 1455.0, 690.0)'''),
    # X ekseni motoru + açıcı motorları: A arka duvarı boyunca (z −780) → A|TOPPING duvarı yanından yukarı → G9 · açıcı ön motoru üstten çıkar
    ('''    for j, (nm, S, it, T_) in enumerate((("x_motoru", (647.5, 924.5, -462.0), (2, -6.0), (1195.2, 1634.0, -720.0)),
                                         ("acici_motoru_arka", (857.5, 1103.5, -506.6), (2, -6.0), (1195.2, 1646.0, -714.0)),
                                         ("acici_motoru_on", (887.5, 1145.0, -65.0), (2, -6.0), (1195.2, 1646.0, -726.0)))):
        cihaz("TOPPING_%s" % nm, S, T_, 3.0, "C", itme=it, on=(T_[0] - 25.0, T_[1], T_[2]), bolge=BOLGE_A, h=5.0,''',
     '''    for j, (nm, S, it, T_, via) in enumerate((("x_motoru", (647.5, 924.5, -462.0), (2, -6.0), (1195.2, 1634.0, -720.0),
                                                  [(647.5, 924.5, -775.0), (1160.0, 924.5, -775.0), (1160.0, 1634.0, -775.0)]),
                                                 ("acici_motoru_arka", (857.5, 1103.5, -506.6), (2, -6.0), (1195.2, 1646.0, -714.0), ()),
                                                 ("acici_motoru_on", (887.5, 1184.6, -30.0), (1, 6.0), (1195.2, 1646.0, -726.0), ()))):
        cihaz("TOPPING_%s" % nm, S, T_, 3.0, "C", itme=it, via=via, on=(T_[0] - 25.0, T_[1], T_[2]), bolge=BOLGE_A, h=5.0,'''),
])
print("tamam")
