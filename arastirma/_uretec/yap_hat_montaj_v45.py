# -*- coding: utf-8 -*-
"""hat_montaj_v44 → v45: K = kesme_cad_v1 (gerçek) · TOPPING = topping_uno_cad_v5 (dönen parçalar ayrı düğüm)
· ana montaja 1 TAM ANİMASYON (bir pizzanın çekmeceden QR dolabına yolculuğu) · istasyon GLB'leri kendi döngülerini korur."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v44.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


degis('"""v44 (25 Eyl 2026):', '"""v45 (26 Eyl 2026): K KESME + SPREY GERÇEK (kesme_cad_v1: K bandı, Festo DGRF-C kesici + PulsaJet sprey aynı kafada, itici, pano, tereyağı tankı)\n'
      '· TOPPING v2 = topping_uno_cad_v5 (kama yarık; UNO pistonu/valfi, kaset helezonu/karıştırıcısı AYRI DÜĞÜM — TOPPING simülasyonu bunları çevirir)\n'
      '· ANA MONTAJA 1 TAM ANİMASYON (Kemal 25 Eyl): bir pizza çekmeceden QR dolabına; istasyon GLB\'leri kendi döngüsünü oynatır.\n'
      'v44 (25 Eyl 2026):')
degis("otonom/hat3d/hat_v44.glb + .usdz", "otonom/hat3d/hat_v45.glb + .usdz")
degis('"sac", "topping_uno_cad_v4.py + topping_cad_v22.py", "hat/topping_v2.html")', '"sac", "topping_uno_cad_v5.py + topping_cad_v22.py", "hat/topping_v2.html")')
degis('"sac", "topping_uno_cad_v4.py", "hat/topping_v2.html")', '"sac", "topping_uno_cad_v5.py", "hat/topping_v2.html")')
degis('"TU3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v4.py"))',
      '"TU5", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v5.py"))   # v45: kama yarık + dönen gruplar')

# ---- K birimleri: KUTU'lar yerine kesme_cad_v1 ----
_k0 = s.index('# --- K · KESME + SPREY (ayri istasyon) ---')
_k1 = s.index('# --- E · KUTU KATLAMA (TEK PARCA, kesilmez) ---')
s = s[:_k0] + '''# --- K · KESME + SPREY (v45: GERÇEK üretim modeli kesme_cad_v1 — işlevsel birimlere ayrılır) ---
import kesme_cad_v1 as KS
KS.modul()
K_BIRIM = [
    ("K_GOVDE", "KESME istasyonu gövdesi: 304 kabuk · ayaklar · taban 123 · istasyon tabanı 1060 · kapılar (üst PC pencereli, kilitli) · acil stop",
     ("ayak_", "taban_sac", "plint_on", "istasyon_tabani", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "kose_dikmesi", "taban_kapisi", "ust_kapi", "kapi_kilidi", "acil_stop")),
    ("K_BANT", "K bandı: gıda PU bant 400 · Interroll RollerDrive EC5000 Ø50 · 6 mm kayma tablası (kesim yükünü taşır) · 20° kılavuz çit · ölü plaka",
     ("bant_", "kayma_tablasi", "tabla_kirisi", "tahrik_rulosu", "kuyruk_rulosu", "olu_plaka", "cit_")),
    ("K_KESICI", "Kesici + sprey kafası: Festo DGRF-C-63-125 · yıldız bıçak Ø296 × 6 · koruma halkası · PulsaJet + TG nozül yıldızın göbeğinde",
     ("kopru_kirisi", "silindir_baglanti", "DGRF", "ara_dikme", "kafa_plakasi", "bicak_", "koruma_", "kelebek_", "PulsaJet", "sprey_dirsegi", "UniJet", "sprey_ucu", "isitmali_hortum_kafa")),
    ("K_YAG", "Tereyağı sistemi: ısıtmalı basınçlı tank 3 L (2 gün 1,41 L) · regülatör · seviye sensörü · ısıtmalı hortum", ("yag_", "isitmali_hortum_", "hava_hortumu_tank")),
    ("K_ITICI", "İtici: igus ZLW-1040 eksen + NEMA 23 · SMC MGPM20-60 kaldırma · kol + POM yüz (E'ye 110 mm girer)",
     ("ZLW", "itici_", "eksen_ayagi", "kaldirma_", "MGPM", "itme_cubugu")),
    ("K_ELEKTRIK", "Pano (taban arkası): S7-1200 · STP-DRV-4830 · NDR-240 · PNOZ · PWM sprey sürücüsü · şartlandırıcı + valf adası · sensörler",
     ("pano_", "din_rayi", "plc_", "emniyet_", "PWMD", "sicaklik", "guc_", "surucu_", "klemens", "kablo_kanali", "sartlandirici", "valf_adasi", "hava_besleme",
      "hava_hortumu_", "sensor_", "kesici_reed")),
    ("K_ICECEK_YEDEK", "İçecek yedeği · soğutmasız · 5 koli × 24 = 120 kutu (soğuk 160 + 120 = 280 = 4 gün)", ("icecek_",)),
]
K_HARIC_GRUP = ("URUN", "URUN_IZ", "REF", "SPREY")          # ürün, sprey konisi ve komşu referansları montaja girmez
K_PARCA = {k: [] for k, _a, _o in K_BIRIM}
for _p in KS.PARCALAR:
    if _p["grup"] in K_HARIC_GRUP:
        continue
    for _k, _a, _o in K_BIRIM:
        if _p["ad"].startswith(_o):
            K_PARCA[_k].append(_p); break
    else:
        raise AssertionError("kesme_cad_v1 parcasi birimsiz kaldi: " + _p["ad"])
for _k, _a, _o in K_BIRIM:
    _bb = [q["wp"].val().BoundingBox() for q in K_PARCA[_k] if not q["ad"].endswith("_kulp") and q["ad"] != "acil_stop"]
    birim(_k, _a, "K", "GERCEK_KESME", (X_K + min(q.xmin for q in _bb), X_K + max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "kesme_cad_v1.py", "hat/kesme.html")

''' + s[_k1:]

# ---- TOPPING v2 parçaları: dönen gruplar ayrı düğüm ----
degis('                ton.setdefault((q["mal"], "SABIT"), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh), _kaba))\n',
      '                _g = q["grup"] if q["grup"].startswith(("PISTON_", "VALF_", "HELEZON_", "KARISTIRICI_")) else "SABIT"   # v45: sim + ana animasyon çevirir\n'
      '                ton.setdefault((q["mal"], _g), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh), _kaba))\n')
# ---- GERCEK_KESME dalı ----
degis('        elif b["durum"] == "GERCEK_STORE":\n',
      '        elif b["durum"] == "GERCEK_KESME":\n'
      '            ps = K_PARCA[b["kod"]]\n'
      '            ton = {}\n'
      '            for p in ps:\n'
      '                kaba = p["ad"].startswith(("surucu_", "guc_", "itici_motoru"))\n'
      '                sh = p["wp"].val().translate(cq.Vector(X_K, 0.0, 0.0))\n'
      '                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh), kaba))\n'
      '            for (t_, g_), m_ in sorted(ton.items()):\n'
      '                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))\n'
      '            b["parca"] = len(ps)\n'
      '        elif b["durum"] == "GERCEK_STORE":\n')
# ---- denetimler: K artık gerçek model ----
degis('    for k_ in ("A_KABIN", "TOPPING_MODUL", "D_FIRIN_GOVDE", "K_KABIN"):', '    for k_ in ("A_KABIN", "TOPPING_MODUL", "D_FIRIN_GOVDE"):')
degis('    for k_ in ("B_KASA", "D_TABAN_KABIN", "K_TABAN_KABIN"):', '    for k_ in ("B_KASA", "D_TABAN_KABIN"):')
degis('    for k_ in ("D_TABAN_KABIN", "K_TABAN_KABIN"):\n        assert abs(_bk[k_]["y"][0] - Y_ALT) < 0.01, "%s alti %.1f" % (k_, _bk[k_]["y"][0])\n',
      '    for k_ in ("D_TABAN_KABIN",):\n        assert abs(_bk[k_]["y"][0] - Y_ALT) < 0.01, "%s alti %.1f" % (k_, _bk[k_]["y"][0])\n'
      '    assert abs(KS.Y_PLINT - Y_ALT) < 0.01 and abs(KS.H_B - H_B) < 0.01, "K alt taban / istasyon tabani farkli"      # v45: K kendi denetimini yapar\n'
      '    assert abs(KS.BANT - PLAKA) < 0.01, "K bandi %.1f · plaka %.1f" % (KS.BANT, PLAKA)\n')
degis('% (_gb, _ge, _bk["D_TABAN_KABIN"]["y"][0], _bk["K_TABAN_KABIN"]["y"][0], Y_ALT))', '% (_gb, _ge, _bk["D_TABAN_KABIN"]["y"][0], KS.Y_PLINT, Y_ALT))')
degis('and b["durum"] != "GERCEK_KUTU"]   # v38', 'and b["durum"] not in ("GERCEK_KUTU", "GERCEK_KESME")]   # v45: K kendi taramasını yapar (kesme_cad_v1) · v38')

# ---- glb_yaz: animasyon listesi seçilebilir ----
degis('def glb_yaz(yol, parcalar, dokular, ozel=None, anim=True):', 'def glb_yaz(yol, parcalar, dokular, ozel=None, anim=True, liste=None):')
degis('    if ANIM:\n        ad2node = {n["name"]: i for i, n in enumerate(nodes)}\n        for kayit in ANIM:\n',
      '    _A = ANIM if liste is None else liste                                              # v45: hat = yolculuk · istasyonlar = kendi döngüleri\n'
      '    if _A:\n        ad2node = {n["name"]: i for i, n in enumerate(nodes)}\n        for kayit in _A:\n')
degis('            n_el = 4 if yol_ == "rotation" else 3\n',
      '            nodes[ad2node[ad_]][yol_] = [float(c) for c in V[0]]                           # v45: durağan duruş = ilk kare\n'
      '            n_el = 4 if yol_ == "rotation" else 3\n')

# ---- K istasyon döngüsü (modul_K) + yolculuk ----
degis('    assert ANIM, "animasyon icin hareketli dugum bulunamadi"\n',
      '    assert ANIM, "animasyon icin hareketli dugum bulunamadi"\n'
      '    for a_, _m, _x in parcalar:                                                          # v45: K (modul_K) 2 × 20 sn, E ile aynı saat\n'
      '        if a_.startswith("K_") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] in ("KESICI", "ITICI_ARABA", "ITICI_KOL"):\n'
      '            g_ = a_.rsplit("__", 1)[1]\n'
      '            ANIM.append((a_, _TT, [_mm(KS.grup_trs(g_, _te(t))) for t in _TT]))\n'
      '    ANIM_HAT, ADIM_HAT, T_J = yolculuk(parcalar)\n'
      '    print("ANA MONTAJ ANIMASYONU (v45): tek tam dongu %.0f sn · %d kanal · %d adim" % (T_J, len(ANIM_HAT), len(ADIM_HAT)))\n')
degis('    b1 = glb_yaz(os.path.join(OUT, "hat_v44.glb"), parcalar, dokular, anim=False)   # v40: animasyonsuz (istasyon modellerinde oynar)\n'
      '    print("ANA MONTAJ (v40): animasyonsuz · %d hareketli dugum t = 0 durusunda · animasyon modul_B (cekmeceler) + modul_E (kutu modulu) icinde" % len({a[0] for a in ANIM}))\n'
      '    print("hat_v44.glb · %d birim · %.0f KB" % (len(parcalar), b1 / 1024.0))\n'
      '    b2, prim, sorun, _u = usdz_yaz([os.path.join(OUT, "hat_v44.usdz")], "hat_v44", parcalar + E_USDZ, dokular)\n'
      '    print("hat_v44.usdz · %.0f KB · %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI"))\n',
      '    b1 = glb_yaz(os.path.join(OUT, "hat_v45.glb"), parcalar, dokular, liste=ANIM_HAT)   # v45: 1 tam animasyon (Kemal 25 Eyl)\n'
      '    print("hat_v45.glb · %d dugum · %.0f KB · animasyon %.0f sn" % (len(parcalar), b1 / 1024.0, T_J))\n'
      '    _usd = [x for x in parcalar if not x[0].startswith("URUN__")]                         # ürün düğümleri yalnız animasyonda (USDZ durağan)\n'
      '    b2, prim, sorun, _u = usdz_yaz([os.path.join(OUT, "hat_v45.usdz")], "hat_v45", _usd + E_USDZ, dokular)\n'
      '    print("hat_v45.usdz · %.0f KB · %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI"))\n')
degis('        alt = [(a_, m_, mal_) for (a_, m_, mal_) in parcalar if mal_[1] == hrf and not a_.endswith("_KABIN")]',
      '        alt = [(a_, m_, mal_) for (a_, m_, mal_) in parcalar if mal_[1] == hrf and not a_.endswith("_KABIN") and not a_.startswith("URUN__")]')
degis('pafta="HAT_ATOSA_TABLALI_v7 (+ E 830: pafta v8 bekliyor) · v44 · alt kisim v3 · B = store_cad_v5 (tam kaplama kapaklar) · kompresor K tabani arkasinda · TOPPING v2 UNO\'lu (topping_uno_cad_v4)',
      'pafta="HAT_ATOSA_TABLALI v12 · v45 · K = kesme_cad_v1 (gercek) · 1 tam animasyon · alt kisim v3 · B = store_cad_v5 · kompresor K tabani arkasinda · TOPPING v2 UNO\'lu (topping_uno_cad_v5)')
degis('sayac=sayac, modul=[', 'sayac=sayac, animasyon=dict(sure=T_J, adim=ADIM_HAT), modul=[')

# ---- yolculuk() ----
YOL = io.open(os.path.join(U, "yolculuk_v45.py"), encoding="utf-8").read()
degis('\nif __name__ == "__main__":\n', '\n' + YOL + '\n\nif __name__ == "__main__":\n')
io.open(os.path.join(U, "hat_montaj_v45.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v45.py yazildi")
