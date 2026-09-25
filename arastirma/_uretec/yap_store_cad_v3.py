# -*- coding: utf-8 -*-
"""store_cad_v2 -> v3 (25 Eyl 2026): ÇEKMECE RAYI ÜÇ ELEMANLI TELESKOP
Kemal: "çekmeceler açılıyor ama havada kalıyor, çekmece rayından çıkıp havada kalıyor; onu düzelt."
  · v2'de ray iki parçaydı: dış profil (kasada, z −756…−56) + kutu boyunda iç profil (çekmeceyle 628 gelir).
    Açılınca iç profil z +41…+571'e gidiyor, dış profilin ön ucu −56'da kalıyordu → arada 97 mm boşluk, çekmece HAVADA.
  · Accuride DZ3832 gerçekte üç elemanlı, %100 açılan bilyeli teleskop: dış (kasa) · ara · iç (çekmece).
    v3: dış SABİT · ara strokun yarısı (314) · iç strok (628). İç eleman ray boyunda (692), kutu adaptör lamına bağlı.
    Tam açıkta dış–ara ve ara–iç bindirmesi ölçülüp denetlenir (≥ 250 mm).
  · Ara elemanın "yarı hız" hareketi VARSAYIM (üretici sayfası açılamadı; bilyeli teleskopta olağan hareket) — katalogla teyit edilecek.
  · Çakışma: açık konum taraması 4 ara konumda (strok × 0,25 · 0,5 · 0,75 · 1), ara ray kendi hızıyla; hareketli ↔ hareketli de taranır.
  · BOM çıktısı 1_STORE_v6.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v2.py"), encoding="utf-8").read()


def degis(a, b):
    global s
    assert s.count(a) == 1, "YOK/COK (%d): %s" % (s.count(a), a[:90])
    s = s.replace(a, b, 1)


degis('''"""AUTOKITCH · B ÇEKMECE MODÜLÜ — ÜRETİM MODELİ v2 (24 Eyl 2026)''',
      '''"""AUTOKITCH · B ÇEKMECE MODÜLÜ — ÜRETİM MODELİ v3 (25 Eyl 2026)
v3: ray ÜÇ ELEMANLI teleskop (dış sabit · ara strok/2 · iç strok) — v2'de iç profil açılınca dış profilden
    tamamen çıkıp çekmece havada kalıyordu (Kemal 25 Eyl). Önceki: store_cad_v2.py
''')
degis('''  ray     Accuride DZ3832-0070 · 700 · tam çekilir · 45,7 × 12,7 · 45–50 kg''',
      '''  ray     Accuride DZ3832-0070 · 700 · tam çekilir (%100) · 45,7 × 12,7 · 45–50 kg · 3 eleman: dış (kasa) · ara · iç (çekmece)''')
degis('''RAY_H, RAY_T, RAY_L, RAY_Y0 = 45.7, 12.7, 700.0, 4.0''',
      '''RAY_H, RAY_T, RAY_L, RAY_Y0 = 45.7, 12.7, 700.0, 4.0
# v3 · üç eleman iç içe (datasheet zarfı 45,7 × 12,7 içinde; sac kalınlıkları ve bilye kafesleri sadeleştirildi)
#   w = duvardan çekmeceye doğru mesafe · dış C (gövde w 0–1,2, flanş w 0–8,5) · ara C (gövde 1,7–2,7, flanş 1,7–10,5)
#   · iç C (çekmece tarafı gövde 11,5–12,7, flanş 3,2–12,7) · her eleman bir öncekinden 2 mm kısa, önden 2 mm geride
RAY_DIS_W, RAY_ARA_W, RAY_KISA = 8.5, 10.5, 2.0
RAY_ARA_ORAN = 0.5                     # ara eleman strokun yarısı kadar gelir [VARSAYIM — bilyeli teleskopta olağan; katalogla teyit]''')

degis('''    # ---- ray (her iki yan): dış profil sabit, iç profil kutuyla gezer ----
    for ad_, rx0 in (("sol", x0), ("sag", x1 - RAY_T)):
        ry0 = yo + RAY_Y0
        dis = kut(rx0, rx0 + RAY_T, ry0, ry0 + RAY_H, Z_CER0 - RAY_L, Z_CER0).cut(kut(rx0 + 1.2, rx0 + RAY_T - 1.2, ry0 + 1.2, ry0 + RAY_H - 1.2, Z_CER0 - RAY_L - 1, Z_CER0 + 1))
        ekle(kod + "_ray_dis_" + ad_, dis, "celik", kod,
             bom=("Teleskopik ray Accuride DZ3832-0070", 2, "700 · tam çekilir · 45,7 × 12,7 · 45–50 kg (çift)", "kolon yan duvarına 4 × M5") if ad_ == "sol" else None)
        ekle(kod + "_ray_ic_" + ad_, kut(rx0 + 3.0, rx0 + RAY_T - 3.0, ry0 + 5.0, ry0 + RAY_H - 5.0, Z_TUB0, Z_TUB1), "celik", kod, grup=G)''',
      '''    # ---- ray (her iki yan) · v3: ÜÇ ELEMANLI TELESKOP — dış (kasa) SABİT · ara strok/2 · iç (çekmece) strok ----
    #      v2'de iç profil kutu boyundaydı ve açılınca dış profilin önünden tamamen çıkıyordu (çekmece havada kalıyordu)
    for ad_, rx0, yon in (("sol", x0, 1.0), ("sag", x1, -1.0)):
        ry0 = yo + RAY_Y0
        def rk(w0, w1, y0_, y1_, z0_, z1_, _r=rx0, _s=yon, _y=ry0):
            return kut(_r + _s * w0, _r + _s * w1, _y + y0_, _y + y1_, z0_, z1_)
        za, zb = Z_CER0 - RAY_L, Z_CER0
        dis = rk(0.0, 1.2, 0.0, RAY_H, za, zb).union(rk(0.0, RAY_DIS_W, 0.0, 1.2, za, zb)).union(rk(0.0, RAY_DIS_W, RAY_H - 1.2, RAY_H, za, zb))
        ekle(kod + "_ray_dis_" + ad_, dis, "celik", kod,
             bom=("Teleskopik ray Accuride DZ3832-0070", 2, "700 · %100 açılır · 3 elemanlı · 45,7 × 12,7 · 45–50 kg (çift)", "dış eleman kolon yan duvarına 4 × M5") if ad_ == "sol" else None)
        za, zb = za + RAY_KISA, zb - RAY_KISA
        ara = rk(1.7, 2.7, 1.7, RAY_H - 1.7, za, zb).union(rk(1.7, RAY_ARA_W, 1.7, 2.7, za, zb)).union(rk(1.7, RAY_ARA_W, RAY_H - 2.7, RAY_H - 1.7, za, zb))
        ekle(kod + "_ray_ara_" + ad_, ara, "celik", kod, grup="CEKMECE_ARA")
        za, zb = za + RAY_KISA, zb - RAY_KISA
        ic = rk(RAY_T - 1.2, RAY_T, 5.0, RAY_H - 5.0, za, zb).union(rk(3.2, RAY_T, 5.0, 6.2, za, zb)).union(rk(3.2, RAY_T, RAY_H - 6.2, RAY_H - 5.0, za, zb))
        ekle(kod + "_ray_ic_" + ad_, ic, "celik", kod, grup=G)''')

degis('''    print("B CEKMECE MODULU v2 · %d parca · %d cekmece" % (len(PARCALAR), len(CEK)))''',
      '''    print("B CEKMECE MODULU v3 · %d parca · %d cekmece" % (len(PARCALAR), len(CEK)))
    # v3 · RAY: tam açıkta elemanlar birbirinin içinde kalıyor mu, kutu iç elemana boyunca bağlı mı? (katılardan ölçülür)
    en = dict(b1=1e9, b2=1e9, bag=1e9)
    for kod, tip, _n, _u, _a in ozet:
        for yan in ("sol", "sag"):
            zr = {}
            for el in ("dis", "ara", "ic"):
                bb = [p for p in PARCALAR if p["ad"] == "%s_ray_%s_%s" % (kod, el, yan)][0]["wp"].val().BoundingBox()
                k = {"dis": 0.0, "ara": RAY_ARA_ORAN, "ic": 1.0}[el] * STROK
                zr[el] = (bb.zmin + k, bb.zmax + k)
            ad_ = [p for p in PARCALAR if p["ad"] == "%s_ray_adaptor_%s" % (kod, yan)][0]["wp"].val().BoundingBox()
            b1 = min(zr["dis"][1], zr["ara"][1]) - max(zr["dis"][0], zr["ara"][0])          # dış ↔ ara boyuna örtüşme
            b2 = min(zr["ara"][1], zr["ic"][1]) - max(zr["ara"][0], zr["ic"][0])            # ara ↔ iç
            bag = min(zr["ic"][1], ad_.zmax + STROK) - max(zr["ic"][0], ad_.zmin + STROK)     # iç eleman ↔ kutu adaptör lamı
            assert b1 >= 250.0 and b2 >= 250.0, "%s %s: ray bindirmesi yetersiz (%.0f / %.0f)" % (kod, yan, b1, b2)
            assert bag >= ad_.zlen - 5.0, "%s %s: kutu ic raya boyunca bagli degil (%.0f / %.0f)" % (kod, yan, bag, ad_.zlen)
            en = dict(b1=min(en["b1"], b1), b2=min(en["b2"], b2), bag=min(en["bag"], bag))
    print("RAY (3 elemanli teleskop, %d cekmece x 2 yan, tam acik strok %.0f): en az dis-ara bindirme %.0f mm · ara-ic %.0f mm · kutu-ic ray bagi %.0f mm · ara eleman +%.0f"
          % (len(ozet), STROK, en["b1"], en["b2"], en["bag"], RAY_ARA_ORAN * STROK))''')

degis('''    t0 = _t.time()
    H = [(p, v.translate(cq.Vector(0.0, 0.0, STROK))) for p, v, _B in L if p["grup"] == "CEKMECE"]
    H = [(p, v, v.BoundingBox()) for p, v in H]
    S = [(p, v, Bb) for p, v, Bb in L if p["grup"] != "CEKMECE"]
    bul, aday = _kesis(H, S, esik, ayni=False)
    print("ACIK KONUM TARAMASI (strok %.0f): %d hareketli x %d sabit · %d aday · %d gercek kesisim · %.0f sn" % (STROK, len(H), len(S), aday, len(bul), _t.time() - t0))
    for v, a, b in bul[:40]:
        print("    %9.0f mm3  %s  <->  %s" % (v, a, b))
    assert not bul, "acik konumda %d cakisma" % len(bul)''',
      '''    # v3: çekmece (strok) + ray ara elemanı (strok × RAY_ARA_ORAN) birlikte gider; yol boyunca 4 konum taranır,
    #     hareketli ↔ hareketli de (kutu/iç ray ile ara ray farklı hızda)
    HAR = {"CEKMECE": 1.0, "CEKMECE_ARA": RAY_ARA_ORAN}
    S = [(p, v, Bb) for p, v, Bb in L if p["grup"] not in HAR]
    for oran in (0.25, 0.5, 0.75, 1.0):
        t0 = _t.time()
        H = [(p, v.translate(cq.Vector(0.0, 0.0, STROK * oran * HAR[p["grup"]]))) for p, v, _B in L if p["grup"] in HAR]
        H = [(p, v, v.BoundingBox()) for p, v in H]
        bul, aday = _kesis(H, S, esik, ayni=False)
        bul2, aday2 = _kesis([h for h in H if h[0]["grup"] == "CEKMECE"], [h for h in H if h[0]["grup"] == "CEKMECE_ARA"], esik, ayni=False)
        bul += bul2
        print("ACIK KONUM TARAMASI (strok %.0f x %.2f, ara ray x %.2f): %d hareketli x %d sabit · %d aday · %d gercek kesisim · %.0f sn"
              % (STROK, oran, oran * RAY_ARA_ORAN, len(H), len(S), aday + aday2, len(bul), _t.time() - t0))
        for v, a, b in bul[:40]:
            print("    %9.0f mm3  %s  <->  %s" % (v, a, b))
        assert not bul, "acik konumda %d cakisma" % len(bul)''')

degis('''(r"_ray_ic_(sol|sag)$", "Accuride DZ3832-0070 (iç profil)"),''',
      '''(r"_ray_ic_(sol|sag)$", "Accuride DZ3832-0070 (iç eleman)"), (r"_ray_ara_(sol|sag)$", "Accuride DZ3832-0070 (ara eleman)"),''')
degis('''    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v5")))''',
      '''    print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v6")))''')
io.open(os.path.join(U, "store_cad_v3.py"), "w", encoding="utf-8").write(s)
print("store_cad_v3.py yazildi")
