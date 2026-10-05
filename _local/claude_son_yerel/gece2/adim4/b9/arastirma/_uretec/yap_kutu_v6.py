# -*- coding: utf-8 -*-
"""kutu_cad_v5 → kutu_cad_v6 (27 Eyl 2026 gece) — Kemal: "ön taraflara kapak koyma".
E'nin içecek yedeğinin önündeki SABİT ÖN ALT SAC (on_alt_sac: x 1,5–828,5 · y 126–917 · z −1,5…0 · 1,5 mm kabuk) silindi → 6 koli önden açık.
  · başka parça DEĞİŞMEZ: yeni olcum_v6() kutu_cad_v5'i kurar ve parça parça karşılaştırır (dilim_v1.karsilastir: sınır kutusu ±0,01 + hacim) →
    yalnız on_alt_sac çıkar (V6_CIKAN).
  · olcum_v5: v4 dilim eşdeğerliği artık "v6'da çıkan: on_alt_sac"ı bekler · içecek yedeği boşluk listesinden "ön alt sac" çıktı.
  · olcum_v6: v5 ↔ v6 · ön yüzde (126–917) gövde parçası kalmadı · v5'te saca DEĞEN parçalar (sac bir şey taşıyor muydu?) ·
    içecek yedeğinin önü (icecek_on_olcum: öndeki engeller, net açıklık, her sütunun düz çekme yolu, yana kaydırma payı) —
    montaj E_ICECEK_YEDEK metni de icecek_on_olcum()'dan okur.
  · çıktılar: kutu_modulu_v6.glb · 5_PACK_kutu_v6/BOM*.csv
Önceki: kutu_cad_v5.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kutu_cad_v5.py"), encoding="utf-8").read()
NL = chr(10)


def d(a, b, n=1):
    """a metni TAM n kez geçmeli → b"""
    global s
    assert s.count(a) == n, (s.count(a), a[:130])
    s = s.replace(a, b)


# ---------------------------------------------------------------- 1 · başlık (değişiklik kaydı) ----------------------------------------------------------------
d('"""AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v5 (27 Eyl 2026) — ALÇAK HAT (SPEC_alcak_hat_v57)',
  '"""AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v6 (27 Eyl 2026 gece) — ÖN ALT SAC KALKTI (Kemal: "ön taraflara kapak koyma"): içecek yedeğinin önündeki' + NL +
  '  sabit ön alt sac (on_alt_sac · x 1,5–828,5 · y 126–917 · 1,5 mm kabuk) silindi → 6 koli önden AÇIK. Sacın üstünde kulp / etiket / sensör / bağlantı yoktu' + NL +
  "  (v5'te ona değen parçalar olcum_v6'da ölçülür). Başka hiçbir parça değişmedi: v5 ↔ v6 parça parça karşılaştırılır (olcum_v6). Önde kalan ön köşe" + NL +
  "  dikmeleri (L 20 × 20) + dikey kablo kanalı → kolilerin düz çekme yolu ölçülür (icecek_on_olcum). Üretici: yap_kutu_v6.py. Önceki: kutu_cad_v5.py" + NL +
  'AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v5 (27 Eyl 2026) — ALÇAK HAT (SPEC_alcak_hat_v57)')

# ---------------------------------------------------------------- 2 · gövde: ön alt sac KALKTI ----------------------------------------------------------------
d('    ekle("on_alt_sac", kut(SAC, W - SAC, Y_PLINT + 3.0, 917.0, -SAC, 0), "kabuk")' + NL,
  '    # v6 (Kemal 27 Eyl gece: "ön taraflara kapak koyma"): ÖN ALT SAC (x 1,5–828,5 · y 126–917) KALKTI → içecek yedeği önden açık · ön köşe dikmeleri yerinde' + NL)

# ---------------------------------------------------------------- 3 · içecek yedeği: önü açık ----------------------------------------------------------------
d('''    """v5: içecek yedeği — soğutmasız, önde (ön alt sac arkasında) · E_SARJOR'un önü, alt rafın altı"""''',
  '''    """v5: içecek yedeği — soğutmasız, önde · E_SARJOR'un önü, alt rafın altı · v6: önü AÇIK (ön alt sac kalktı)"""''')
d('                    koli=len(ICECEK_X) * ICECEK_KAT, kutu=len(ICECEK_X) * ICECEK_KAT * KOLI["kutu"])   # montaj için özet (E yereli)' + NL,
  '                    koli=len(ICECEK_X) * ICECEK_KAT, kutu=len(ICECEK_X) * ICECEK_KAT * KOLI["kutu"])   # montaj için özet (E yereli)' + NL +
  'V6_CIKAN = ("on_alt_sac",)                              # v6: v5\'ten çıkan parça — ön taraflara kapak yok (Kemal 27 Eyl gece)' + NL)

# ---------------------------------------------------------------- 4 · olcum_v5: v4 dilim eşdeğerliği + içecek boşlukları ----------------------------------------------------------------
d("    # 1 · DİLİM EŞDEĞERLİĞİ: v4'ün y %.0f–%.0f dilimi çıkarılmış hali ↔ v5 (doğrudan yeni kotlarda kurulan)",
  "    # 1 · DİLİM EŞDEĞERLİĞİ: v4'ün y %.0f–%.0f dilimi çıkarılmış hali ↔ v5 (doğrudan yeni kotlarda kurulan) · v6: ön alt sac (V6_CIKAN) hariç")
d('''    yaz("dilim y %.0f–%.0f: v4 %d parça (altta %d · üstte %d · boydan geçen %d, bantta biten 0) ↔ v5 birebir %d · fark %d"
        % (DILIM_Y0, DILIM_Y0 + DILIM_DY, len(ESKI.PARCALAR), len(rap["ALT"]), len(rap["UST"]), len(rap["GECEN"]), len(k["ayni"]), len(k["fark"])),
        not k["fark"] and not k["ref_eksik"] and set(k["yeni_ek"]) == yeni, "; ".join(k["fark"][:6]) + (" eksik %s" % k["ref_eksik"] if k["ref_eksik"] else "") +''',
  '''    yaz("dilim y %.0f–%.0f: v4 %d parça (altta %d · üstte %d · boydan geçen %d, bantta biten 0) ↔ v6 birebir %d · fark %d · v6'da çıkan: %s"
        % (DILIM_Y0, DILIM_Y0 + DILIM_DY, len(ESKI.PARCALAR), len(rap["ALT"]), len(rap["UST"]), len(rap["GECEN"]), len(k["ayni"]), len(k["fark"]), ", ".join(k["ref_eksik"]) or "yok"),
        not k["fark"] and k["ref_eksik"] == list(V6_CIKAN) and set(k["yeni_ek"]) == yeni, "; ".join(k["fark"][:6]) + (" eksik %s" % k["ref_eksik"] if k["ref_eksik"] != list(V6_CIKAN) else "") +''')
d('"asansor_ray_plakasi", "kalip_alt_rafi_koseben_on", "sol_sac_pizza_penceresi", "sag_sac", "on_alt_sac")}',
  '"asansor_ray_plakasi", "kalip_alt_rafi_koseben_on", "sol_sac_pizza_penceresi", "sag_sac")}   # v6: ön alt sac yok')
d('''                  sol_sac=O["icecek"]["x"][0] - ark["sol_sac_pizza_penceresi"].xmax, sag_sac=ark["sag_sac"].xmin - O["icecek"]["x"][1],
                  on_sac=ark["on_alt_sac"].zmin - O["icecek"]["z"][1])''',
  '''                  sol_sac=O["icecek"]["x"][0] - ark["sol_sac_pizza_penceresi"].xmax, sag_sac=ark["sag_sac"].xmin - O["icecek"]["x"][1])   # v6: ön alt sac yok (önü açık)''')
d('''    yaz("içecek yedeği boşlukları: ön dikme %.1f · dikey kablo kanalı %.1f · ön alt sac %.1f · asansör ray plakası %.1f · alt raf köşebendi %.1f · sol sac %.1f · sağ sac %.1f"
        % (bosluk["on_dikme"], bosluk["kablo_kanali"], bosluk["on_sac"], bosluk["ray_plakasi"], bosluk["raf_kosebent"], bosluk["sol_sac"], bosluk["sag_sac"]),''',
  '''    yaz("içecek yedeği boşlukları: ön dikme %.1f · dikey kablo kanalı %.1f · asansör ray plakası %.1f · alt raf köşebendi %.1f · sol sac %.1f · sağ sac %.1f (v6: ön alt sac yok)"
        % (bosluk["on_dikme"], bosluk["kablo_kanali"], bosluk["ray_plakasi"], bosluk["raf_kosebent"], bosluk["sol_sac"], bosluk["sag_sac"]),''')

# ---------------------------------------------------------------- 5 · YENİ: icecek_on_olcum() + olcum_v6() ----------------------------------------------------------------
YENI = '''def icecek_on_olcum():
    """v6 · İÇECEK YEDEĞİNİN ÖNÜ (ön alt sac kalktı) — katılardan ölçer, modul()'den SONRA çağrılır (montaj E_ICECEK_YEDEK metni de buradan).
    on: kolilerin önünden ön yüze (z 0) kadar olan bölgeye giren gövde parçaları · net: kolilerin yüksekliğinde öndeki soldaki son engel ile
    sağdaki ilk engel arası (x) · sutun: her sütunun DÜZ çekme yoluna (koli izdüşümü, koli önü → ön yüz) binen parçalar + x bindirmesi (mm) ·
    sag_bos: sağ sütunun sağında (koli yüksekliği ve derinliğinde) ilk engele kadar boşluk · ara: iki sütun arası."""
    X_, Y_, Z_ = ICECEK_YEDEK["x"], ICECEK_YEDEK["y"], ICECEK_YEDEK["z"]
    G_ = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] in ("SABIT", "ASANSOR") and not p["ad"].startswith("icecek_")]

    def kesen(x0, x1, y0, y1, z0, z1):
        b0 = kut(x0, x1, y0, y1, z0, z1).val(); B0 = b0.BoundingBox(); L = []
        for ad, sh in G_:
            b_ = sh.BoundingBox()
            if _bb_kesisir(B0, b_) and sh.intersect(b0).Volume() > 0.5:
                L.append((ad, b_))
        return L
    on = kesen(X_[0], X_[1], Y_[0], Y_[1], Z_[1], 0.0)
    orta = (X_[0] + X_[1]) / 2.0
    net = (max([b_.xmax for _a, b_ in on if b_.xmax <= orta] + [SAC]), min([b_.xmin for _a, b_ in on if b_.xmin >= orta] + [W - SAC]))
    sut = []
    for x0, x1 in ICECEK_X:
        eng = [(a, round(min(x1, b_.xmax) - max(x0, b_.xmin), 2)) for a, b_ in kesen(x0, x1, Y_[0], Y_[1], Z_[1], 0.0)]
        sut.append(dict(x=(x0, x1), engel=eng, bindirme=max([v for _a, v in eng] + [0.0])))
    sag = kesen(X_[1], W, Y_[0], Y_[1], Z_[0], Z_[1])
    return dict(on=sorted({a for a, _b in on}), net=net, sutun=sut, sag_bos=min([b_.xmin for _a, b_ in sag] + [W]) - X_[1], ara=ICECEK_X[1][0] - ICECEK_X[0][1])


def olcum_v6():
    """v6 · ÖN ALT SAC KALKTI (Kemal: "ön taraflara kapak koyma") — iddiaları ÖLÇER, bozulursa durur (assert). Dönüş: ölçülen değerler."""
    import dilim_v1 as DL
    import kutu_cad_v5 as V5
    O = {}

    def yaz(ad, sart, deger):
        print("  %-92s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger)); assert sart, ad
    print("OLCUM v6 (on alt sac kalkti · icecek yedeginin onu acik)")
    # 1 · v5 ↔ v6: yalnız V6_CIKAN çıktı, kalan HER parça birebir (sınır kutusu ±0,01 + hacim)
    V5.modul()
    k = DL.karsilastir(PARCALAR, V5.PARCALAR)
    O["v5_v6"] = dict(v5=len(V5.PARCALAR), v6=len(PARCALAR), ayni=len(k["ayni"]), cikan=list(k["ref_eksik"]))
    yaz("v5 ↔ v6: v5 %d parça → v6 %d · birebir %d · fark %d · yeni %d · çıkan: %s" % (len(V5.PARCALAR), len(PARCALAR), len(k["ayni"]), len(k["fark"]), len(k["yeni_ek"]),
                                                                                  ", ".join(k["ref_eksik"]) or "yok"),
        not k["fark"] and not k["yeni_ek"] and k["ref_eksik"] == list(V6_CIKAN) and len(k["ayni"]) == len(V5.PARCALAR) - len(V6_CIKAN), "; ".join(k["fark"][:6]))
    # 2 · ön yüz (eski sacın yeri): 126–917 arasında z > −1,45'te gövde parçası YOK (ön köşe dikmelerinin ön yüzü −1,5'te)
    on_b = kut(SAC, W - SAC, Y_PLINT + 3.0, 917.0, -SAC + 0.05, 0.0).val()
    kal = [p["ad"] for p in PARCALAR if p["grup"] in ("SABIT", "ASANSOR") and _bb_kesisir(on_b.BoundingBox(), p["wp"].val().BoundingBox())
           and p["wp"].val().intersect(on_b).Volume() > 0.01]
    yaz("ön yüz (eski ön alt sacın yeri x %.1f–%.1f · y %.0f–917 · z −1,45…0): gövde parçası %d → alt ön AÇIK" % (SAC, W - SAC, Y_PLINT + 3.0, len(kal)),
        not kal and not [p for p in PARCALAR if p["ad"] in V6_CIKAN], str(kal[:5]))
    # 3 · v5'te ön alt saca DEĞEN parçalar (sac bir şey taşıyor muydu? kulp / etiket / sensör / bağlantı)
    s5 = [p for p in V5.PARCALAR if p["ad"] == "on_alt_sac"][0]["wp"].val().BoundingBox()
    g5 = (s5.xmin - 0.1, s5.xmax + 0.1, s5.ymin - 0.1, s5.ymax + 0.1, s5.zmin - 0.1, s5.zmax + 0.1)
    deg = []
    for p in V5.PARCALAR:
        if p["ad"] == "on_alt_sac":
            continue
        b_ = p["wp"].val().BoundingBox()
        if b_.xmin < g5[1] and g5[0] < b_.xmax and b_.ymin < g5[3] and g5[2] < b_.ymax and b_.zmin < g5[5] and g5[4] < b_.zmax:
            deg.append(p["ad"])
    O["sac_komsu"] = sorted(deg)
    yaz("v5'te ön alt saca değen parçalar (sınır kutusu ±0,1): %s → hepsi gövde (dikme / yan sac / taban) · sac kulp, etiket, sensör, bağlantı TAŞIMIYORDU"
        % ", ".join(sorted(deg)), bool(deg) and all(a.startswith(("kose_dikme_on_", "sol_sac", "sag_sac", "taban_sac")) for a in deg), "")
    # 4 · içecek yedeğinin önü: engeller · net açıklık · düz çekme yolu · yana kaydırma
    ion = icecek_on_olcum()
    O["icecek_on"] = ion
    s0, s1 = ion["sutun"]
    yaz("içecek yedeğinin önü (koli önü z %.0f → ön yüz 0): yalnız %s · net açıklık x %.1f–%.1f = %.1f mm ≥ koli %.0f (tek koli düz geçer)"
        % (ICECEK_Z[1], " + ".join(ion["on"]), ion["net"][0], ion["net"][1], ion["net"][1] - ion["net"][0], KOLI["x"]),
        set(ion["on"]) == {"kose_dikme_on_0", "kablo_kanali_dikey_alt"} and ion["net"][1] - ion["net"][0] >= KOLI["x"], "")
    print("     BİLGİ · düz çekme yolu: sol sütun (x %.0f–%.0f) %s · sağ sütun (x %.0f–%.0f) %s"
          % (s0["x"][0], s0["x"][1], " · ".join("%s %.1f mm biner" % e for e in s0["engel"]) or "serbest",
             s1["x"][0], s1["x"][1], " · ".join("%s %.1f mm biner" % e for e in s1["engel"]) or "serbest"))
    ger = max(0.0, s0["bindirme"] - ion["ara"])
    print("     BİLGİ · koli net açıklığa (x %.1f–%.1f) hizalanıp çekilir: sağ sütun %.1f sağa (sağında %.1f boş) → sol sütun %.1f sağa kayıp düz çıkar → sağ sütun sola kayıp (x ≤ %.1f) düz çıkar%s"
          % (ion["net"][0], ion["net"][1], ger, ion["sag_bos"], s0["bindirme"], ion["net"][1], "" if ger <= ion["sag_bos"] else " · YER YETMİYOR"))
    return O


# ---------------------------------------------------------------- GLB (hiyerarşik düğüm + animasyon) ----------------------------------------------------------------'''
d('# ---------------------------------------------------------------- GLB (hiyerarşik düğüm + animasyon) ----------------------------------------------------------------', YENI)

# ---------------------------------------------------------------- 6 · çıktılar ----------------------------------------------------------------
d('"generator": "AUTOKITCH kutu_cad_v5"', '"generator": "AUTOKITCH kutu_cad_v6"')
d('''    print("E KUTU MODULU v5 (alcak hat · ust 1862 · tepsi 936 · sarjor 462 · icecek yedegi 6 koli): %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()
    olcum(); sys.stdout.flush()
    olcum_v5(); sys.stdout.flush()''',
  '''    print("E KUTU MODULU v6 (alcak hat · ust 1862 · tepsi 936 · sarjor 462 · icecek yedegi 6 koli · v6: ON ALT SAC YOK, icecek onu acik): %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()
    olcum(); sys.stdout.flush()
    olcum_v5(); sys.stdout.flush()
    olcum_v6(); sys.stdout.flush()''')
d('glb_yaz(os.path.join(KOK, "otonom", "hat3d", "kutu_modulu_v5.glb"))', 'glb_yaz(os.path.join(KOK, "otonom", "hat3d", "kutu_modulu_v6.glb"))')
d('bom_yaz(os.path.join(KOK, "arastirma", "5_PACK_kutu_v5"))', 'bom_yaz(os.path.join(KOK, "arastirma", "5_PACK_kutu_v6"))')

# ---------------------------------------------------------------- 7 · son denetim (üretilen metin) ----------------------------------------------------------------
for _eski in ('ekle("on_alt_sac"', 'ark["on_alt_sac"]', 'bosluk["on_sac"]', "kutu_modulu_v5.glb", '"5_PACK_kutu_v5"', "AUTOKITCH kutu_cad_v5"):
    assert _eski not in s, "v6: eski metin kaldi: %s" % _eski
for _yeni in ("def icecek_on_olcum():", "def olcum_v6():", "olcum_v6(); sys.stdout.flush()", "V6_CIKAN = (", "kutu_modulu_v6.glb", "5_PACK_kutu_v6"):
    assert _yeni in s, "v6: eksik: %s" % _yeni
compile(s, "kutu_cad_v6.py", "exec")
hedef = os.path.join(U, "kutu_cad_v6.py")
assert not os.path.exists(hedef), "kutu_cad_v6.py zaten var — üstüne yazılmaz"
io.open(hedef, "w", encoding="utf-8").write(s)
print("kutu_cad_v6.py yazildi")
