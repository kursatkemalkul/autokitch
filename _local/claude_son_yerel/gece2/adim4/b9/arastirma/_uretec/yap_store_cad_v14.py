# -*- coding: utf-8 -*-
"""store_cad_v13 → store_cad_v14 (29 Eyl 2026 · YEREL) — Kemal: "yap yapılacakları işte" (v13 sonrası iki öneri):
1 · ÇEKMECE KUTUSU TABANI 1 → 2 mm (yanlar 1 mm kalır; taban lazer, yanlar büküm, TIG kaynaklı): v13'te dolu içecek çekmecesinde taban ~12 mm
    sehiyordu (Timoshenko, 4 kenar mesnetli levha) → 2 mm'de ≤ 2 mm (denetim assert). Tepsi ve ürünler 1 mm yukarı (Y_OTUR 9 → 10).
2 · MOTOR RAMPASI 0,3 s (EM-324C yumuşak kalkış/duruş): 0,1 s'de dolu içecek çekmecesi 62 N > 60 N sürekli → 0,3 s'de ~25 N.
3 · YÜK DENETİMİ (katılardan): her çekmecenin hareketli kütlesi (dolu) ≤ ray çifti 45 kg · motor kuvveti ≤ 60 N · taban sehimi ≤ 2 mm.
Önceki: store_cad_v13.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v13.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v13 (29 Eyl 2026 · yap_store_cad_v13.py): K4 DEPO TEK KAP (çekmece kutusu = kap, ayırıcı + kapak; GN kapları + raf kalktı)\n',
      '"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v14 (29 Eyl 2026 · yap_store_cad_v14.py): KUTU TABANI 2 mm · MOTOR RAMPASI 0,3 s · yük denetimi\nv13: ÜRETİM MODELİ v13 (29 Eyl 2026 · yap_store_cad_v13.py): K4 DEPO TEK KAP (çekmece kutusu = kap, ayırıcı + kapak; GN kapları + raf kalktı)\n')
degis('Y_OTUR = KC + 1.0 + TEPSI_T - CUKUR_H  # 9\n',
      'KUTU_TABAN_T = 2.0                     # v14: kutu tabanı 2 mm (v13 1,0 — içecek çekmecesinde ~12 mm sehim) · yanlar 1,0\nRAMPA_SN = 0.3                         # v14: sürücü yumuşak kalkış / duruş rampası (EM-324C) · 0,1 s ile dolu içecek çekmecesi 62 N > 60 N sürekli\nRAY_YUK_KG = 45.0                      # Accuride DZ3832 çift · %100 açılır (katalog; 700 boyda teyit)\nY_OTUR = KC + KUTU_TABAN_T + TEPSI_T - CUKUR_H  # v14: 10 (v13 9)\n')
degis('    u = kut(ka, kb, kc, kc + 1.0, Z_TUB0, Z_TUB1).union(kut(ka, ka + 1.0, kc, kd, Z_TUB0, Z_TUB1)).union(kut(kb - 1.0, kb, kc, kd, Z_TUB0, Z_TUB1))\n    ekle(kod + "_kutu_U_1.0", u, "sac", kod, grup=G, bom=("Çekmece kutusu U 1,0", 1, "304 lazer + 2 büküm", "%d × %d × %d" % (kb - ka, kd - kc, TUB_D)))\n    ekle(kod + "_kutu_arka_1.0", kut(ka + 1.0, kb - 1.0, kc + 1.0, kd, Z_TUB0, Z_TUB0 + 1.0), "sac", kod, grup=G)\n    ekle(kod + "_kutu_on_1.0", kut(ka + 1.0, kb - 1.0, kc + 1.0, kd, Z_TUB1 - 1.0, Z_TUB1), "sac", kod, grup=G)\n',
      '    u = kut(ka, kb, kc, kc + KUTU_TABAN_T, Z_TUB0, Z_TUB1).union(kut(ka, ka + 1.0, kc, kd, Z_TUB0, Z_TUB1)).union(kut(kb - 1.0, kb, kc, kd, Z_TUB0, Z_TUB1))\n    ekle(kod + "_kutu_2.0_1.0", u, "sac", kod, grup=G, bom=("Çekmece kutusu · taban 2,0 + yanlar 1,0", 1, "304 · taban 2 mm lazer, yanlar 1 mm büküm, TIG kaynaklı (v14)", "%d × %d × %d" % (kb - ka, kd - kc, TUB_D)))\n    ekle(kod + "_kutu_arka_1.0", kut(ka + 1.0, kb - 1.0, kc + KUTU_TABAN_T, kd, Z_TUB0, Z_TUB0 + 1.0), "sac", kod, grup=G)\n    ekle(kod + "_kutu_on_1.0", kut(ka + 1.0, kb - 1.0, kc + KUTU_TABAN_T, kd, Z_TUB1 - 1.0, Z_TUB1), "sac", kod, grup=G)\n')
degis('        ty0 = kc + 1.0\n',
      '        ty0 = kc + KUTU_TABAN_T                                           # v14: 2 mm tabanın üstü\n')
degis('            kons = max(kons, ad_.zmin - BB["%s_kutu_U_1.0" % kod].zmin)\n',
      '            kons = max(kons, ad_.zmin - BB["%s_kutu_2.0_1.0" % kod].zmin)\n')
degis('    print("TAHRIK: PD3665-24-51 127 d/dk × GT3 30 dis (cevre %.1f) = %.0f mm/s · strok %.0f -> %.1f sn · surekli kuvvet %.0f N (0,853 N·m / r %.2f)"\n          % (math.pi * KAS_PD, hiz, STROK, STROK / hiz, 0.853 / (KAS_PD / 2000.0), KAS_PD / 2.0))\n',
      '    print("TAHRIK: PD3665-24-51 127 d/dk × GT3 30 dis (cevre %.1f) = %.0f mm/s · strok %.0f -> %.1f sn (+ rampa %.1f) · surekli kuvvet %.0f N (0,853 N·m / r %.2f)"\n          % (math.pi * KAS_PD, hiz, STROK, STROK / hiz, RAMPA_SN, 0.853 / (KAS_PD / 2000.0), KAS_PD / 2.0))\n    # ---- v14 · ÇEKMECE YÜKÜ (katılardan): hareketli kütle · ray · motor (sürtünme μ 0,01 VARSAYIM + rampa ivmesi) · kutu tabanı sehimi ----\n    RHO = {"sac": 7.93, "celik": 7.93, "pu": 0.04, "silikon": 1.15, "conta": 1.5, "plastik": 1.2, "aluminyum": 2.70, "koyu": 1.3}\n    ICM = {"top_hamur": 0.220, "top_lahm": 0.110, "kutu330": 0.355, "tatlikabi": 0.150}        # kg/adet · top: _ortak/HAMUR_TOPU_220g / 110g · kutu dolu 330 ml · tatlı VARSAYIM\n    F_sur = 0.853 / (KAS_PD / 2000.0); E_t, nu_t = 193000.0, 0.3; en_k = None\n    for kod, tip, _n, _u, _a in ozet:\n        bos = ic = tp = 0.0\n        for p in PARCALAR:\n            if p["birim"] != kod or p["grup"] not in ("CEKMECE", "CEKMECE_ARA"):\n                continue\n            k_ = [k for k in ("kutu330", "tatlikabi") if "_%s_" % k in p["ad"]] or (["top_" + tip] if "_top_" in p["ad"] else [])\n            if k_:\n                ic += ICM[k_[0]]; continue\n            m_ = p["wp"].val().Volume() * RHO.get(p["mal"], 7.93) / 1e6\n            bos += m_ * (0.5 if p["grup"] == "CEKMECE_ARA" else 1.0)\n            if p["ad"].endswith("_tepsi"):\n                tp = m_\n        M_ = bos + ic; F_ = M_ * 9.81 * 0.01 + M_ * (hiz / 1000.0) / RAMPA_SN\n        kb_ = BB["%s_kutu_2.0_1.0" % kod]; a_ = min(kb_.xlen, kb_.zlen); b_ = max(kb_.xlen, kb_.zlen)\n        D_ = E_t * KUTU_TABAN_T ** 3 / (12.0 * (1.0 - nu_t ** 2)); q_ = (ic + tp) * 9.81 / (a_ * b_)\n        w_ = (0.00406 if b_ / a_ < 1.05 else 0.00485 if b_ / a_ < 1.15 else 0.00564) * q_ * a_ ** 4 / D_       # Timoshenko, 4 kenar mesnetli (b/a 1,0 · 1,1 · 1,2)\n        if en_k is None or M_ > en_k[1]:\n            en_k = (kod, M_, F_, w_)\n        assert M_ <= RAY_YUK_KG and F_ <= F_sur and w_ <= 2.0, "%s: yuk %.1f kg / motor %.0f N / taban sehimi %.1f mm" % (kod, M_, F_, w_)\n    print("CEKMECE YUKU v14 (katilardan): en agir %s dolu %.1f kg (ray cifti %.0f kg) · motor surtunme + %.1f s rampa %.0f N / %.0f N surekli · taban %.1f mm -> sehim %.1f mm (<= 2)"\n          % (en_k[0], en_k[1], RAY_YUK_KG, RAMPA_SN, en_k[2], F_sur, KUTU_TABAN_T, en_k[3]))\n')
compile(s, "store_cad_v14.py", "exec")
io.open(os.path.join(U, "store_cad_v14.py"), "w", encoding="utf-8").write(s)
print("store_cad_v14.py yazildi")
