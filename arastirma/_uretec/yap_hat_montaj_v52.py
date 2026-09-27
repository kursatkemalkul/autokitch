# -*- coding: utf-8 -*-
"""hat_montaj_v51 → hat_montaj_v52 (27 Eyl 2026):
1) PİZZA KUTUSU YEDEĞİ TEK YERDE — fırın üstü SOL (Kemal: "sola koy işte, 4 gün ne diyon"). Dolaptaki 505'lik pizza gözü kalkar;
   fırın üstü sol yığın 1516–2028 = 320 kutu; şarjör 567 + 320 = 887 = 3,1 gün. firin_tp10_cad_v6 (raf 4 mm, 10 takoz).
2) FIRIN KABUĞU GÖRÜNÜR (Kemal: "fırını öne taşıdık, çıkıntısını silmişsin"): v51 çıplak filtresi fırının kendi dış kabuğunu
   (govde_kabugu) da gizliyordu → çıkıntı görselde yok gibiydi. Fırın kabuğu makine parçasıdır, filtreden çıkarıldı.
3) ŞEFFAF İSTASYON YÜZEYLERİ (Kemal: "şeffaf olarak her istasyonun ön hariç tüm yüzeylerini koy, eşitlik ilkesine dikkat et"):
   her istasyona AYNI kural — sol · sağ · arka · üst · alt, 1,5 mm, kendi zarfının içinde; arka hep −830, üst 2030 (B 1060), alt 123
   (A/C 1060); ön yok. Geçiş ağızları gerçek saclardan. Denetimlere girmez (görsel)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v51.py"), encoding="utf-8").read()
assert "CIPLAK = True" in s


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
degis('"""v51 (27 Eyl 2026): FIRIN 79 mm ÖNE (Kemal)', '"""v52 (27 Eyl 2026): PİZZA KUTUSU YEDEĞİ TEK YERDE fırın üstü sol (320 kutu, 887 = 3,1 gün; dolap pizza gözü boş) + firin_tp10_cad_v6 (raf 4 mm, 10 takoz) + FIRIN KABUĞU GÖRÜNÜR (çıkıntı) + ŞEFFAF İSTASYON YÜZEYLERİ (ön hariç, eşitlik)' + NL + 'v51 (27 Eyl 2026): FIRIN 79 mm ÖNE (Kemal)')
degis('import firin_tp10_cad_v5 as FT', 'import firin_tp10_cad_v6 as FT')
degis('"sac", "firin_tp10_cad_v5.py", "hat/oven.html")', '"sac", "firin_tp10_cad_v6.py", "hat/oven.html")')
i = s.index('        ("D_PIZZA_YEDEK", "Pizza kutusu yedeği · dolapta 505 kutu düz'); j = s.index("\n", i) + 1
s = s[:i] + s[j:]
degis('· önde bulaşık + temizlik + pizza kutusu yedeği · arkada', '· önde bulaşık + temizlik (v52: pizza gözü BOŞ — yedekler fırın üstünde solda) · arkada')
degis('birim("D_PIZZA_YEDEK_UST", "Pizza kutusu yedeği · fırın üstü rafta 55 kutu düz (804 × 404 × 88) · dolaptaki 505 ile 560 = 2 gün", "D", "KUTU", (X_D + 20.0, X_D + 824.0), (1516.0, 1604.0), (-424.0, -20.0), "kutu",',
      'birim("D_PIZZA_YEDEK_UST", "Pizza kutusu yedeği · TEK YER: fırın üstü SOL, rafta 320 kutu düz (804 × 404 × 512) · şarjör 567 + 320 = 887 = 3,1 gün (Kemal 27 Eyl: sola koy)", "D", "KUTU", (X_D + 20.0, X_D + 824.0), (1516.0, 2028.0), (-424.0, -20.0), "kutu",')
# ---- 2) fırın kabuğu çıplak filtresinden çıkar + gizlenen adları listele ----
degis('"yalitim_blogu", "on_fitil", "govde_kabugu", "yalitim_tasyunu",', '"yalitim_blogu", "on_fitil", "yalitim_tasyunu",')
degis('CIPLAK = True\n', 'CIPLAK = True\n# v52: govde_kabugu listeden ÇIKARILDI — fırının kendi dış kabuğu makine parçası (79 mm çıkıntı görünür olsun, Kemal)\n')
degis('CIPLAK_SAYAC = {"parca": 0, "kutu": 0}', 'CIPLAK_SAYAC = {"parca": 0, "kutu": 0}\nCIPLAK_ADLAR = set()')
degis('        CIPLAK_SAYAC["parca"] += 1; return True', '        CIPLAK_SAYAC["parca"] += 1; CIPLAK_ADLAR.add(str(ad).rstrip("0123456789_")); return True')
degis('— denetimler tam parcayla" % (CIPLAK_SAYAC["parca"], CIPLAK_SAYAC["kutu"]))',
      '— denetimler tam parcayla" % (CIPLAK_SAYAC["parca"], CIPLAK_SAYAC["kutu"]))\n    print("   gizlenen ad kokleri (v52): %s" % ", ".join(sorted(CIPLAK_ADLAR)))')
# ---- 3) şeffaf istasyon yüzeyleri ----
SEF = r'''    # ---- v52 · ŞEFFAF İSTASYON YÜZEYLERİ (Kemal 27 Eyl: "şeffaf olarak her istasyonun ön hariç tüm yüzeylerini koy, eşitlik ilkesine dikkat et") ----
    # EŞİTLİK: her istasyona aynı kural — sol · sağ · arka · üst · alt, 1,5 mm, kendi zarfının İÇİNDE (biri içeride biri dışarıda yok);
    # arka hep z −830, ön yok; üst 2030 (B: 1060), alt 123 (A/C: 1060). Yan/üst/alt z −828,5…0, arka tam kapak → köşeler aynı.
    # Geçiş ağızları gerçek saclardan: C→F fırın giriş yarığı (YARIK_V2 dış çerçeve) · F→K kesme sol sac ağzı · K→E E_PENCERE.
    # F yanlarında fırın gövdesinin kendi kabuğu yüzeydir (çakışan bölge açılır). Yalnız görsel: denetimlere girmez.
    SEF_T = 1.5
    SEF_IST = (("A", X_A, X_A + W_A, H_B, H_MAK), ("C", X_BC, X_BC + W_BC, H_B, H_MAK), ("B", X_A, X_A + W_B, Y_ALT, H_B),
               ("D", X_D, X_D + W_D, Y_ALT, H_MAK), ("K", X_K, X_K + W_K, Y_ALT, H_MAK), ("E", X_E, X_E + W_E, Y_ALT, H_MAK))
    _yk = tuple(FT.YARIK_V2[0][2:]); _ka = (1100.0, 1240.0, -420.0, -8.0)
    SEF_AGIZ = {("C", "sag"): _yk, ("D", "sol"): _yk, ("D", "sag"): _ka, ("K", "sol"): _ka, ("K", "sag"): tuple(KS.E_PENCERE), ("E", "sol"): tuple(KS.E_PENCERE)}
    SEF_ATLA = {("A", "sag"), ("C", "sol")}   # ilk koşu raporu: TOPPING açıcısı + tabla arabası x 700'ün 600 mm soluna uzanıyor → A–C arasında iç duvar YOK
    MALZEME["seffaf_yuzey"] = dict(renk=(0.70, 0.80, 0.90, 0.12), met=0.0, ruf=0.3, saydam=True)

    def _sef_panel(x0, x1, y0, y1, z0, z1, delik=()):
        w = FT.kut(x0, x1, y0, y1, z0, z1)
        for d_ in delik:
            w = w.cut(FT.kut(*d_))
        return TC_AG(w)

    _sef_n = 0
    for m_, x0, x1, y0, y1 in SEF_IST:
        Z0 = -DZ
        yz = []
        for taraf, (xa, xb) in (("sol", (x0, x0 + SEF_T)), ("sag", (x1 - SEF_T, x1))):
            if (m_, taraf) in SEF_ATLA:
                continue                                                                 # A–C arası: TOPPING açıcı + tabla arabası sınırdan geçer
            d_ = []
            if (m_, taraf) in SEF_AGIZ:
                a_ = SEF_AGIZ[(m_, taraf)]; d_.append((xa - 1.0, xb + 1.0, a_[0], a_[1], a_[2], a_[3]))
            if m_ == "D":
                d_.append((xa - 1.0, xb + 1.0, FT.YG0, FT.YG1, -FT.D_TP + FT.ZS, 1.0))          # fırın kabuğu burada yüzey
            yz.append((taraf, _sef_panel(xa, xb, y0 + SEF_T, y1 - SEF_T, Z0 + SEF_T, 0.0, d_)))
        yz.append(("arka", _sef_panel(x0, x1, y0, y1, Z0, Z0 + SEF_T)))
        yz.append(("ust", _sef_panel(x0, x1, y1 - SEF_T, y1, Z0 + SEF_T, 0.0)))
        yz.append(("alt", _sef_panel(x0, x1, y0, y0 + SEF_T, Z0 + SEF_T, 0.0)))
        mal_ = mal_ad(dict(kod="SEFFAF_YUZEY", modul=m_, mal="seffaf_yuzey"))
        for f_, msh in yz:
            parcalar.append(("%s_SEFFAF__%s" % (m_, f_), msh, mal_)); _sef_n += 1
    print("SEFFAF YUZEY (v52): %d istasyon · %d panel (A–C arası iç duvar yok: TOPPING açıcı + tabla arabası sınırdan geçer) · %.1f mm · arka z %.0f · ust %.0f (B %.0f) · alt %.0f (A/C %.0f) · on YOK · agizlar C>F, F>K, K>E · F yaninda firin kabugu yuzey"
          % (len(SEF_IST), _sef_n, SEF_T, -DZ, H_MAK, H_B, Y_ALT, H_B))
    # EŞİTLİK DENETİMİ (bilgi): istasyon zarfının dışına taşan düğümler (ön hariç; yerdeki istasyonlarda ayaklar hariç).
    # Not: dönen/animasyonlu düğümler pivot-yerel olabilir → orada çıkan değer yanıltıcı olabilir, adına bakılır.
    _zr = {m_: (x0, x1, y0, y1) for m_, x0, x1, y0, y1 in SEF_IST}
    _tas = []
    for a_, msh, mal_ in parcalar:
        if "_SEFFAF__" in a_ or a_.startswith(("URUN__", "ROBOT", "QR")) or not msh.P or len(mal_) < 2 or mal_[1] not in _zr:
            continue
        x0, x1, y0, y1 = _zr[mal_[1]]
        xs = [q[0] / MM for q in msh.P]; ys = [q[1] / MM for q in msh.P]; zs = [q[2] / MM for q in msh.P]
        t_ = []
        if min(xs) < x0 - 2.0: t_.append("sol %.0f" % (x0 - min(xs)))
        if max(xs) > x1 + 2.0: t_.append("sag %.0f" % (max(xs) - x1))
        if y0 > Y_ALT + 1.0 and min(ys) < y0 - 2.0: t_.append("alt %.0f" % (y0 - min(ys)))
        if max(ys) > y1 + 2.0: t_.append("ust %.0f" % (max(ys) - y1))
        if min(zs) < -DZ - 2.0: t_.append("arka %.0f" % (-DZ - min(zs)))
        if t_: _tas.append("%s [%s]" % (a_, ", ".join(t_)))
    print("ESITLIK · ISTASYON ZARFINI GECEN DUGUMLER (bilgi, on haric): %s" % ("YOK" if not _tas else "%d" % len(_tas)))
    for x_ in _tas: print("   " + x_)
    # ---- çıktılar ----'''
degis('    # ---- çıktılar ----', SEF)
degis('beyaz = gerçek model  ·  şeffaf = henüz kutu"', 'beyaz = gerçek model  ·  şeffaf = istasyon yüzeyi / henüz kutu"')
degis('pafta="HAT v51 (27 Eyl) · FIRIN 79 ONE:', 'pafta="HAT v52 (27 Eyl) · KUTU YEDEGI TEK YERDE firin ustu sol 320 (887 = 3,1 gun) · raf 4 mm 10 takoz · FIRIN KABUGU GORUNUR (cikinti) · SEFFAF ISTASYON YUZEYLERI on haric, esitlik (1,5 mm, arka -830, ust 2030, alt 123) · FIRIN 79 ONE:')
degis('· kutu yedegi 505 + 55 ·', '· kutu yedegi 320 firin ustu sol (dolap pizza gozu bos) ·')
degis('print("ANA MONTAJ ANIMASYONU (v51):', 'print("ANA MONTAJ ANIMASYONU (v52):')
s = s.replace('hat_v51.glb', 'hat_v52.glb').replace('hat_v51.usdz', 'hat_v52.usdz').replace('"hat_v51"', '"hat_v52"')
io.open(os.path.join(U, "hat_montaj_v52.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v52.py yazildi")
