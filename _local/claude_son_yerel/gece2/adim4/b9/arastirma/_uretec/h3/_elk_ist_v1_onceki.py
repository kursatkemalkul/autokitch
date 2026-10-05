# -*- coding: utf-8 -*-
"""HAT v3.2 · ELEKTRİK · İSTASYON İÇİ CİHAZ KABLOLARI v1 — her sabit motor / sensör / fan / sürücü / valf adası → kendi istasyon panosuna ya da kablo kanalına.
Yol bulucu (h3_elk_rota): eksenlere paralel yol, makineye + yeni parçalara karşı gerçek katı çakışması, HAREKET ZARFLARI yasak (TOPPING araba + tabla + kaset ·
K itici · K kesici) · uzun parçalara en yakın yüzeye P-kelepçe. Hareketli gruplardaki cihazlar (TOPPING arabası: dönüş motoru, tabla sıfır sensörü ·
açıcı motorları · K itici Z sensörleri) mevcut ENERJİ ZİNCİRİNDEN beslenir — sabit kablo çizilmez (animasyonda havada kalırdı).
Geçişler: TOPPING kuru bölme tabanı G1 (2200, −795) · G2 (1650, −770) · teknik bölme ön perdesi G3 · F|K duvarı G4 (tartı) — rakorlu."""
import math
import cadquery as cq
import h3_elk_ortak as EO
import h3_elk_rota as ER
from h3_elk_ortak import kut, sil, boru, rakor

V = cq.Vector
YASAK = [("TOPPING_hareket_zarfi", kut(780.0, 2620.0, 940.0, 1060.0, -515.0, 12.0)),
         ("K_itici_zarfi", kut(4028.0, 4392.0, 960.0, 1112.0, -822.0, -355.0)),
         ("K_kesici_zarfi", kut(4108.0, 4292.0, 1100.0, 1600.0, -262.0, -128.0))]
RAPOR = dict(yol=[], bulunamadi=[], askida=[])


def kur(ekle, DELIKLER, DUSUR):
    for ad, s in YASAK: ER.ekli_ekle("YASAK_" + ad, s)
    B = {"C": "ELK_TOPPING", "K": "ELK_K", "B": "ELK_DOLAP", "A": "ELK_TOPPING", "F": "ELK_TOPPING"}

    def cihaz(ad, S, T, r, ist, itme=None, via=(), mal="kablo", bom=None):
        pts, sh = None, None
        if via:                                                   # zorunlu geçiş noktaları (rakor) sırayla
            parca, cur, ok = [], S, True
            for v in list(via) + [T]:
                p, s_ = ER.bul(cur, v, r, itme=itme if cur == S else None)
                if p is None: ok = False; RAPOR["bulunamadi"].append((ad, cur, v, s_)); break
                parca += (p if not parca else p[1:]); cur = v
            if ok: pts = parca; sh = boru(pts, r)
        else:
            pts, sh = ER.bul(S, T, r, itme=itme)
            if pts is None: RAPOR["bulunamadi"].append((ad, S, T, sh)); sh = None
        if pts is None: return None
        ekle("kablo_%s" % ad, sh, mal, B[ist], bom); ER.ekli_ekle("kablo_" + ad, sh)
        kl, aski = ER.kelepceler(pts, r)
        for j, (_p, ks) in enumerate(kl):
            ekle("kablo_%s_kelepce_%d" % (ad, j), ks, "celik", B[ist]); ER.ekli_ekle("kablo_%s_kelepce_%d" % (ad, j), ks)
        RAPOR["yol"].append((ad, round(EO.uzunluk(pts)), len(pts) - 1, len(kl)))
        RAPOR["askida"] += [(ad,) + tuple(a) for a in aski]
        return pts

    def gecis(ad, p, eksen, mods, r=6.0, t=1.5, yon="+"):
        rk, d_ = rakor(p, eksen, r, t, yon=yon, disli=max(8.0, r + 3.0))
        ekle("rakor_%s" % ad, rk, "rakor", "ELK_TOPPING" if ad.startswith(("G1", "G2", "G3")) else "ELK_K", None); ER.ekli_ekle("rakor_" + ad, rk)
        for m, a in mods: DELIKLER.append((m, a, d_, "kablo geçişi %s" % ad))

    # ================= TOPPING =================
    PX = [1460.0 + 28.0 * i for i in range(19)]                # pano kutusu alt yüzü giriş noktaları (y 1879, z −770)
    PT = lambda i: (PX[i], 1879.0, -770.0)
    gecis("G1_kuru_bolme_tabani", (2200.0, 1109.0, -795.0), "y", [("TC", "kuru_bolme_tabani")], r=9.0, yon="+")
    gecis("G2_kuru_bolme_tabani", (1650.0, 1109.0, -770.0), "y", [("TC", "kuru_bolme_tabani")], r=6.0, yon="+")
    G1a, G1u = (2200.0, 1095.0, -795.0), (2200.0, 1125.0, -795.0)
    G2a, G2u = (1650.0, 1095.0, -770.0), (1650.0, 1125.0, -770.0)
    cihaz("TOPPING_kaset_kasar_helezon", (2062.0, 1142.0, -807.0), PT(18), 3.0, "C", itme=[(1, -6.0)])
    cihaz("TOPPING_kaset_kasar_rotor", (2062.0, 1296.0, -807.0), PT(17), 3.0, "C", itme=[(1, -6.0)])
    cihaz("TOPPING_kaset_sucuk_helezon", (2311.0, 1162.0, -807.0), PT(16), 3.0, "C", itme=[(1, -6.0)])
    cihaz("TOPPING_kaset_sucuk_rotor", (2311.0, 1266.0, -807.0), PT(15), 3.0, "C", itme=[(1, -6.0)])
    cihaz("TOPPING_evap_fani_0", (1826.0, 1652.0, -727.0), PT(12), 2.5, "C", itme=[(2, -8.0)])
    cihaz("TOPPING_evap_fani_1", (2006.0, 1652.0, -727.0), PT(14), 2.5, "C", itme=[(2, -8.0)])
    for i, xs in enumerate((1482.0, 1515.0, 1548.0, 1581.0)):
        cihaz("TOPPING_surucu_%d" % i, (xs, 1477.0, -730.0), PT(i), 3.0, "C", itme=[(1, 6.0)])
    cihaz("TOPPING_valf_adasi", (1844.0, 1310.0, -700.0), PT(10), 4.5, "C", itme=[(1, 6.0)])
    cihaz("TOPPING_sogutma_grubu_KLF66", (1650.0, 1087.0, -770.0), PT(6), 5.0, "C", via=[G2a, G2u])
    cihaz("TOPPING_zincir_sabit_ucu", (2200.0, 924.0, -476.0), PT(8), 6.0, "C", via=[(2200.0, 924.0, -795.0), G1a, G1u])
    cihaz("TOPPING_sabit_tahrik_motoru", (2466.0, 986.0, -506.0), PT(9), 4.0, "C", via=[(2466.0, 986.0, -780.0), (2215.0, 986.0, -780.0), (2215.0, 1095.0, -780.0)])
    for i, (nm, xs) in enumerate((("x_sifir", 1086.0), ("x_limit_sol", 1056.0), ("x_limit_sag", 2375.0))):
        cihaz("TOPPING_sensor_%s" % nm, (xs, 920.0, -26.0), PT(4 + (i % 2)), 2.0, "C", itme=[(2, -6.0)],
              via=[(2430.0, 920.0, -32.0), (2430.0, 920.0, -790.0), (2190.0, 920.0, -790.0), (2190.0, 1095.0, -790.0)])
    gecis("G3_teknik_perde", (2351.0, 1100.0, -476.0), "z", [("TC", "teknik_bolme_on_perdesi")], r=2.5, t=1.0, yon="+")
    cihaz("TOPPING_tabla_bos_sensoru", (2351.0, 1082.0, -170.0), PT(7), 2.0, "C",
          via=[(2351.0, 1100.0, -170.0), (2351.0, 1100.0, -790.0), (2205.0, 1100.0, -790.0)])
    # ================= K =================
    KT = lambda x: (x, 1614.0, -786.0)                         # K klemens sırası alt yüzü (y 1616)
    cihaz("K_EC5000_bant_motoru", (4354.0, 969.0, -485.0), KT(4250.0), 3.0, "K", itme=[(2, -6.0)])
    for i, (nm, S) in enumerate((("giris_verici", (4105.0, 1026.0, -428.0)), ("giris_alici", (4105.0, 1026.0, 4.0)),
                                 ("durus_verici", (4350.0, 1026.0, -428.0)), ("durus_alici", (4350.0, 1026.0, 4.0)))):
        cihaz("K_urun_sensoru_%s" % nm, S, KT(4176.0 + 10.0 * i), 2.0, "K", itme=[(1, 6.0)])
    for i, S in enumerate(((4200.0, 1545.0, -163.0), (4200.0, 1420.0, -163.0))):
        cihaz("K_DGRF_sensoru_%d" % i, S, KT(4220.0 + 8.0 * i), 2.0, "K", itme=[(2, -6.0)])
    for i, S in enumerate(((4055.0, 974.0, -688.0), (4305.0, 974.0, -688.0))):
        cihaz("K_itici_X_sensoru_%d" % i, S, KT(4236.0 + 8.0 * i), 2.0, "K", itme=[(1, 6.0)])
    cihaz("K_PulsaJet_nozul", (4025.0, 1214.0, -146.0), KT(4196.0), 2.5, "K", itme=[(1, 6.0)])
    cihaz("K_yag_pompasi_GJ-N21", (4150.0, 1644.0, -520.0), KT(4206.0), 3.0, "K", itme=[(1, -6.0)])
    cihaz("K_yag_basinc_PM1704", (4225.0, 1810.0, -520.0), KT(4186.0), 2.0, "K", itme=[(1, 6.0)])
    gecis("G4_tarti_FK_duvari", (3999.0, 1387.0, -296.0), "x", [("FU", "f_ust_yan_sag"), ("KS", "sol_sac_urun_girisi")], r=2.5, t=3.0, yon="+")
    cihaz("K_tarti_yuk_hucresi", (3938.0, 1387.0, -296.0), (4295.0, 1708.0, -773.0), 2.5, "K", via=[(3990.0, 1387.0, -296.0), (4010.0, 1387.0, -296.0)])
    # ================= DOLAP (B) =================
    # çekmece reed sensörleri (açık + kapalı): lama yanından (lamaya kablo bağıyla) arkaya · motor üstünden kolon kablo kanalının yan yüzüne (parmak yuvası)
    D = {ad: sb for ad, s_, sb in EO.dokum()}
    kanallar = {k.split("|")[1].replace("kablo_kanali_", ""): v for k, v in D.items() if k.startswith("B_KABLO|kablo_kanali_K")}
    n = 0
    for k, sb in sorted(D.items()):
        if not (k.startswith("CEK_") and k.endswith("_reed_acik")): continue
        grp = k.split("|")[0]; kol = grp.split("_")[1]
        kn = kanallar.get(kol); rk = D.get(k.replace("_reed_acik", "_reed_kapali"))
        if kn is None or rk is None: RAPOR["bulunamadi"].append(("DOLAP_reed_" + grp, sb[:2], sb[2:4], "kanal/kapalı sensör yok")); continue
        rxc, ryc = (sb[0] + sb[1]) / 2.0, (sb[2] + sb[3]) / 2.0
        cx, cy = sb[0] - 2.3, sb[3] + 2.0                        # lama yan yüzüne dayalı (0,3 mm) · reed üst hizası
        yc = min(ryc, kn[3] - 12.0)                               # kanal üst ucunu aşmasın
        a_ = [(rxc, ryc, sb[4]), (rxc, ryc, sb[4] - 4.0), (cx, ryc, sb[4] - 4.0), (cx, cy, sb[4] - 4.0), (cx, cy, -777.0), (cx, yc, -777.0), (kn[0] - 0.2, yc, -777.0)]
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
            ekle("kablo_%s" % ad, sh, "kablo", "ELK_DOLAP",
                 ("Reed sensör kablosu 2 × 0,25 PUR (lamaya kablo bağıyla · kolon kanalına)", 42, "", "motor M12 soketi zaten kanala dayalı") if n == 0 else None)
            ER.ekli_ekle("kablo_" + ad, sh); n += 1
            RAPOR["yol"].append((ad, round(EO.uzunluk(q)), len(q) - 1, 0))
    # soğutma grubu (Secop NLE8.8CN): kompresör üstünden kondenserin üstünü aşıp pano altı kanalının alt yüzüne
    cihaz("DOLAP_secop_NLE88", (4213.0, 308.5, -244.0), (4213.0, 410.8, -809.0), 4.0, "B",
          via=[(4213.0, 435.0, -244.0), (4213.0, 435.0, -600.0), (4213.0, 410.8, -600.0)])
    # 4 evaporatör fanı → en yakın kolon kanalının yan yüzü (evaporatörün üstünden arkaya)
    for nm, S, xk, yk in (("fan_sol_1", (1783.5, 509.5, -628.5), 1683.5, 668.0), ("fan_sol_2", (1963.5, 509.5, -628.5), 2298.5, 668.0),
                          ("fan_sag_1", (3093.5, 422.0, -628.5), 2993.5, 520.0), ("fan_sag_2", (3273.5, 422.0, -628.5), 3608.5, 520.0)):
        sg = 1.0 if S[0] > xk else -1.0
        cihaz("DOLAP_evap_%s" % nm, S, (xk + sg * 0.2, yk, -777.0), 2.5, "B", itme=[(1, 6.0)], via=[(xk + sg * 40.0, yk, -777.0)])
    return RAPOR
