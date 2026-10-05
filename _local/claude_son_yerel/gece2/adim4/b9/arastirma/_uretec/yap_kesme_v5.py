# -*- coding: utf-8 -*-
"""kesme_cad_v4 → kesme_cad_v5 (27 Eyl 2026 gece) — Kemal: "deterjanları makinenin arkasına koyma, tabii şimdilik sil".
K altındaki bulaşık makinesinin ARKASINDAKİ deterjan / parlatıcı düzeni silindi (9 parça, hepsi "deterjan_"):
  · deterjan_rafi (kanister rafı 304 · 5 mm · y 325–330) + deterjan_rafi_konsolu_0/1 (L konsollar)
  · deterjan_kanisteri_deterjan / _parlatici (5 L bidon) + deterjan_kanister_kapagi_deterjan / _parlatici
  · deterjan_emis_hortumu_deterjan / _parlatici (dozaj emiş hortumları, MEIKO arkasına)
  · YALNIZ onlar için eklenenler: sabitler KANISTER / KANISTER_X / KANISTER_Y0 / KANISTER_Z / KANISTER_KAPAK / RAF_Y / RAF_X / RAF_Z / KONSOL / HORTUM,
    hortum_noktalari(), malzemeler kanister / mavi_kapak / dozaj, BOM anahtarı "bidon", denetimler (raf sehimi, bidon yeri, hortum boyu, bidon değişimi UYARI'sı).
Kalan HER ŞEY aynı: bulaşık makinesinin yeri (BULASIK_YER), zarfı, arka payı (BULASIK_ARKA_PAY + BULASIK_BAGLANTI_UST · makinenin kendi bağlantıları),
gövde, bant, kesici, sprey, itici, pano, hava.
Denetim: MEIKO arka payı artık BOŞ (hiçbir K parçası) · bulaşığın arkası (arka sac → arka pay) BOŞ · v4 ↔ v5 parça parça (dilim_v1.karsilastir,
sınır kutusu ±0,01 + hacim): yalnız deterjan_ çıktı. E arayüzü kutu_cad_v6 (ön alt sac kalktı; kotlar / pencere / kinematik v5 ile aynı).
Çıktılar: kesme_v5.glb · kesme_v5.json · 4_KESME_v5/BOM*.csv. Önceki: kesme_cad_v4.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kesme_cad_v4.py"), encoding="utf-8").read()
NL = chr(10)


def d(a, b, n=1):
    """a metni TAM n kez geçmeli → b"""
    global s
    assert s.count(a) == n, (s.count(a), a[:130])
    s = s.replace(a, b)


def blok(a, b, yeni):
    """a (tek) işaretinden b (tek) işaretine kadar (b hariç) → yeni"""
    global s
    assert s.count(a) == 1, (s.count(a), a[:110])
    assert s.count(b) == 1, (s.count(b), b[:110])
    i = s.index(a); j = s.index(b)
    assert i < j, (a[:60], b[:60])
    s = s[:i] + yeni + s[j:]


# ---------------------------------------------------------------- 1 · başlık (değişiklik kaydı) + E arayüzü + malzemeler ----------------------------------------------------------------
d('"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v4 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57)',
  '"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v5 (27 Eyl 2026 gece): DETERJAN + PARLATICI KALKTI (Kemal: "deterjanları makinenin' + NL +
  'arkasına koyma, tabii şimdilik sil") — bulaşığın arkasındaki kanister rafı (y 325–330) + 2 konsol + deterjan / parlatıcı bidonları + kapakları + 2 dozaj' + NL +
  'emiş hortumu (9 parça, hepsi "deterjan_") ve YALNIZ onlar için eklenen sabitler, malzemeler, BOM anahtarı ve denetimler silindi. Bulaşık makinesinin yeri' + NL +
  'AYNI (BULASIK_YER); arkası + MEIKO arka payı artık BOŞ (ölçülür). v4 ↔ v5 parça parça karşılaştırılır (yalnız deterjan_ çıktı). E arayüzü kutu_cad_v6' + NL +
  '(E\'nin ön alt sacı kalktı; kotlar / pencere / kinematik aynı). Deterjanın yeri AÇIK (karar Kemal\'de). Üretici: yap_kesme_v5.py. Önceki: kesme_cad_v4.py' + NL +
  'v4 (27 Eyl 2026): ALÇAK HAT (SPEC_alcak_hat_v57)')
d("import kutu_cad_v5 as KC                                   # v4: ALÇAK HAT E'si",
  "import kutu_cad_v6 as KC                                   # v5: kutu_cad_v6 (E'nin ön alt sacı kalktı · kotlar / pencere / kinematik v5 ile aynı) · v4: ALÇAK HAT E'si")
d("= 978–1062 [K: kutu_cad_v5.PENCERE] · v3'te 1146–1230 sabitti", "= 978–1062 [K: kutu_cad_v6.PENCERE, v5 ile aynı] · v3'te 1146–1230 sabitti")
d('for _k, _v in {"kanister": (0.93, 0.94, 0.96, 1.0), "mavi_kapak": (0.15, 0.40, 0.85, 1.0), "dozaj": (0.90, 0.86, 0.62, 1.0)}.items():   # v4: bidon · parlatıcı kapağı · dozaj hortumu' + NL +
  '    MALZEME.setdefault(_k, dict(renk=_v, met=0.0, ruf=0.6))' + NL,
  "# v5: v4'ün kanister / mavi_kapak / dozaj malzemeleri kalktı (deterjan + parlatıcı bidonları ve dozaj hortumları yok)" + NL)

# ---------------------------------------------------------------- 2 · TABAN ALTI: yalnız bulaşık (REF) ----------------------------------------------------------------
d("# ---------------------------------------------------------------- 7 · TABAN ALTI (v4 · ALÇAK HAT): bulaşık yeri + deterjan / parlatıcı ----------------------------------------------------------------",
  "# ---------------------------------------------------------------- 7 · TABAN ALTI (v4 · ALÇAK HAT): bulaşık yeri · v5: deterjan / parlatıcı YOK ----------------------------------------------------------------")
d("# solunda önde 77, dikmenin arkasında 107 BOŞ · arkasında tek sıra deterjan + parlatıcı, raf 325–330 · makinenin bağlantıları (y ≤ 310) altta kalır." + NL,
  "# solunda önde 77, dikmenin arkasında 107 BOŞ · makinenin bağlantıları (y ≤ 310) altta kalır." + NL +
  '# v5 (Kemal 27 Eyl gece: "deterjanları makinenin arkasına koyma, tabii şimdilik sil"): arkadaki kanister rafı (325–330) + deterjan / parlatıcı bidonları +' + NL +
  "#    dozaj emiş hortumları SİLİNDİ → bulaşığın arkası (MEIKO arka payı 25 dahil) BOŞ (denetimde ölçülür). Deterjanın yeri AÇIK — karar Kemal'de." + NL)
blok("KANISTER = dict(", NL + NL + "def bulasik_parcalari():", "")
blok("def hortum_noktalari(i):", "# ---------------------------------------------------------------- 8 · ÜRÜN + REFERANSLAR",
     '''def taban():
    """v4 · ALÇAK HAT: K tabanının altı — bulaşık makinesi REF (ayrı modül) · v5: kanister rafı + deterjan / parlatıcı + dozaj hortumları KALKTI (Kemal)"""
    for ad_, sh in bulasik_parcalari()[0]:
        ekle("REF_bulasik_" + ad_, cq.Workplane(obj=sh), "referans", "REF")


''')

# ---------------------------------------------------------------- 3 · DENETİM ----------------------------------------------------------------
d('    print("DENETİM (kesme_cad_v4)")', '    print("DENETİM (kesme_cad_v5)")')
d('    """v4 · ALÇAK HAT: dilim eşdeğerliği · yeni kotlar · E arayüzü · bulaşık yeri · kanister rafı (ölçülür)"""',
  '    """v4 · ALÇAK HAT: dilim eşdeğerliği · yeni kotlar · E arayüzü · bulaşık yeri (ölçülür) · v5: v4 ↔ v5 (yalnız deterjan_ çıktı) · bulaşığın arkası BOŞ"""')
d('''    kontrol("E arayüzü kutu_cad_v5: E plakası''', '''    kontrol("E arayüzü kutu_cad_v6: E plakası''')
d('KC.__name__ == "kutu_cad_v5" and', 'KC.__name__ == "kutu_cad_v6" and')
d("    # 2 · DİLİM EŞDEĞERLİĞİ: v3'ün y 700–868 dilimi çıkarılmış hali ↔ v4 (doğrudan yeni kotlarda)",
  "    # 2 · DİLİM EŞDEĞERLİĞİ: v3'ün y 700–868 dilimi çıkarılmış hali ↔ v5 (doğrudan yeni kotlarda)")
d('    yeni_ok = all(a.startswith(("REF_bulasik_", "deterjan_")) for a in k["yeni_ek"])',
  '    yeni_ok = all(a.startswith("REF_bulasik_") for a in k["yeni_ek"])                                  # v5: deterjan_ yok')
d("↔ v4 birebir %d · fark %d · yeni %d (bulaşık REF + deterjan)", "↔ v5 birebir %d · fark %d · yeni %d (bulaşık REF · v5: deterjan yok)")
d('''    kontrol("kinematik: urun_merkez(t) = v3 − 168 (203 an, en büyük fark %.4f mm) · grup_trs(t) = v3 (201 an × 4 grup, %.4f)" % (fu, fg), fu < 1e-6 and fg < 1e-6)
''', '''    kontrol("kinematik: urun_merkez(t) = v3 − 168 (203 an, en büyük fark %.4f mm) · grup_trs(t) = v3 (201 an × 4 grup, %.4f)" % (fu, fg), fu < 1e-6 and fg < 1e-6)
    # 2b · v5: v4 ↔ v5 — yalnız deterjan_ parçaları çıktı, kalan HER parça birebir (dilim_v1.karsilastir: sınır kutusu ±0,01 + hacim)
    import kesme_cad_v4 as V4
    V4.modul()
    k5 = DL.karsilastir(PARCALAR, V4.PARCALAR)
    cik = sorted(k5["ref_eksik"]); det4 = sorted(p["ad"] for p in V4.PARCALAR if p["ad"].startswith("deterjan_"))
    H_["v4_v5"] = dict(v4=len(V4.PARCALAR), v5=len(PARCALAR), ayni=len(k5["ayni"]), cikan=cik)
    kontrol("v4 ↔ v5: v4 %d parça → v5 %d · birebir %d · fark %d · yeni %d · çıkan %d (hepsi deterjan_: raf + 2 konsol + 2 bidon + 2 kapak + 2 dozaj hortumu)"
            % (len(V4.PARCALAR), len(PARCALAR), len(k5["ayni"]), len(k5["fark"]), len(k5["yeni_ek"]), len(cik)),
            not k5["fark"] and not k5["yeni_ek"] and cik == det4 and len(cik) == 9 and len(k5["ayni"]) == len(V4.PARCALAR) - len(det4)
            and not [p for p in PARCALAR if p["ad"].startswith("deterjan_")], "; ".join(k5["fark"][:5]) + (" yeni %s" % k5["yeni_ek"][:5] if k5["yeni_ek"] else "") + " çıkan %s" % cik)
''')
d('''    g1 = giren(kutu_(Z["x"], Z["y"], Z["z"]), ("deterjan_emis_hortumu_",))
    kontrol("bulaşık zarfına (%.1f–%.1f × %.0f–%.0f × %.0f…%.0f) hiçbir K parçası girmez (dozaj hortum uçları makinenin arka yüzüne bağlanır)" % (Z["x"] + Z["y"] + Z["z"]), not g1, str(g1[:5]))''',
  '''    g1 = giren(kutu_(Z["x"], Z["y"], Z["z"]))                                                   # v5: dozaj hortumu yok → istisna yok
    kontrol("bulaşık zarfına (%.1f–%.1f × %.0f–%.0f × %.0f…%.0f) hiçbir K parçası girmez" % (Z["x"] + Z["y"] + Z["z"]), not g1, str(g1[:5]))''')
d('''    hy = max([sh.intersect(ap).BoundingBox().ymax for p, sh in K_ if p["ad"].startswith("deterjan_emis_hortumu_")] + [0.0])
    kontrol("MEIKO arka payı z %.0f…%.0f boş: yalnız 2 dozaj hortumu geçer, o da bağlantı bölgesinde (üstü %.1f ≤ %.0f)" % (BULASIK_ARKA_PAY + (hy, BULASIK_BAGLANTI_UST)),
            all(a.startswith("deterjan_emis_hortumu_") for a, _v in g4) and len(g4) == 2 and hy <= BULASIK_BAGLANTI_UST, str(g4))''',
  '''    kontrol("MEIKO arka payı z %.0f…%.0f BOŞ: hiçbir K parçası girmez (v5: dozaj hortumu yok · makinenin kendi bağlantıları y ≤ %.0f)" % (BULASIK_ARKA_PAY + (BULASIK_BAGLANTI_UST,)),
            not g4, str(g4))
    # v5 · bulaşığın ARKASI (eski kanister rafı + bidonların yeri): arka sacın önünden MEIKO arka payına kadar BOŞ
    ab = (Z["x"], Z["y"], (bbx("arka_sac").zmax, BULASIK_ARKA_PAY[0]))
    g5 = giren(kutu_(*ab))
    H_["bulasik_arka_bos"] = dict(x=ab[0], y=ab[1], z=ab[2], derinlik=ab[2][1] - ab[2][0])
    kontrol("bulaşığın arkası BOŞ (v5 · raf + bidonlar + hortumlar kalktı): x %.1f–%.1f · y %.0f–%.0f · z %.1f…%.0f (%.1f mm derin) → K parçası yok"
            % (ab[0] + ab[1] + ab[2] + (ab[2][1] - ab[2][0],)), not g5, str(g5[:5]))''')
blok("    # 4 · KANİSTER RAFI + BİDONLAR", "    for u in UYARI:",
     "    # v5: kanister rafı sehimi + bidon yeri + hortum boyu denetimleri ve bidon değişimi UYARI'sı kalktı (deterjan yok)" + NL)

# ---------------------------------------------------------------- 4 · BOM / ÇIKTILAR ----------------------------------------------------------------
d('"koli", "kolisi", "hortum", "Avara", "tank", "bidon")) else "ÜRETİM"', '"koli", "kolisi", "hortum", "Avara", "tank")) else "ÜRETİM"')
for a, b in (('print("K KESME + SPREY v4 (alcak hat: ust 1862 · taban 892 · bant 996 · altinda bulasik + deterjan): %d parca',
              'print("K KESME + SPREY v5 (alcak hat: ust 1862 · taban 892 · bant 996 · altinda yalniz bulasik · deterjan YOK): %d parca'),
             ('"generator": "AUTOKITCH kesme_cad_v4"', '"generator": "AUTOKITCH kesme_cad_v5"'), ('surum="kesme_cad_v4 · %s"', 'surum="kesme_cad_v5 · %s"'),
             ('"otonom", "hat3d", "kesme_v4.glb")', '"otonom", "hat3d", "kesme_v5.glb")'), ('"arastirma", "4_KESME_v4")', '"arastirma", "4_KESME_v5")'),
             ('"otonom", "hat3d", "kesme_v4.json")', '"otonom", "hat3d", "kesme_v5.json")')):
    d(a, b)

# ---------------------------------------------------------------- 5 · son denetim (üretilen metin) ----------------------------------------------------------------
import re
_kod = s[s.index(NL + "import csv, io, json"):]                                  # başlık (değişiklik kaydı) hariç
for _ad in (r"\bKANISTER\w*", r"\bRAF_[XYZ]\b", r"\bKONSOL\b", r"\bHORTUM\b", r"\bhortum_noktalari\b", r'"kanister"', r'"mavi_kapak"', r'"dozaj"', r'"bidon"',
            r'ekle\("deterjan_', r"kutu_cad_v5", r"kesme_v4\.(glb|json)", r"4_KESME_v4", r"AUTOKITCH kesme_cad_v4"):
    assert not re.search(_ad, _kod), "v5: eski ad kaldi: %s" % _ad
for _yeni in ("import kutu_cad_v6 as KC", "import kesme_cad_v4 as V4", 'KC.__name__ == "kutu_cad_v6"', "kesme_v5.glb", "kesme_v5.json", "4_KESME_v5", "bulasik_arka_bos"):
    assert _yeni in s, "v5: eksik: %s" % _yeni
compile(s, "kesme_cad_v5.py", "exec")
hedef = os.path.join(U, "kesme_cad_v5.py")
assert not os.path.exists(hedef), "kesme_cad_v5.py zaten var — üstüne yazılmaz"
io.open(hedef, "w", encoding="utf-8").write(s)
print("kesme_cad_v5.py yazildi")
