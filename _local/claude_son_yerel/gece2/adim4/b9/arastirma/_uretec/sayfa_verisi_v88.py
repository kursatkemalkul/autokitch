# -*- coding: utf-8 -*-
"""v88 sayfa verisi (30 Eyl 2026 · Claude): kesme_v9.json (K sayfası) + kutu_v13.json (E sayfası) — derleme ağacında çalıştırılır:
python sayfa_verisi_v88.py <derleme_uretec_klasoru> <worktree_kok>"""
import json, math, re, sys, csv, io as _io
from pathlib import Path
URETEC, KOK = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(URETEC))
import os
os.chdir(URETEC)
import kesme_cad_v9 as KS
import kutu_cad_v13 as KC

# ---------------- K v9 ----------------
KS.modul()
Z = KS.zaman_denetimi()
den_k = json.loads((KOK / "_local" / "k-v9" / "denetim.json").read_text(encoding="utf-8"))
SP = KS.sprey_ozeti()
f = lambda v, n=1: (("%." + str(n) + "f") % v).replace(".", ",")
L_hava = math.pi / 4 * 63.0 ** 2 * 125.0 * 2 - math.pi / 4 * 20.0 ** 2 * 125.0   # mm³ · çift etkili, mil hacmi düşülür
NL = L_hava / 1e6 * 7.0                                                             # 6 bar gösterge = 7 bar mutlak
adim_k = [
    (KS.Z_GELIS[0], "GELİŞ", "Ürün fırın bandından K bandına geçer. Interroll EC5000 (49:1, ≤ 0,37 m/s) ürünü %.1f s'de kesme merkezine getirir (tepe 195 mm/s); Omron E3Z-T61 ışını ürünün ön kenarını x 350'de görünce durur. Çitler ürünü 36 mm içeri (kutu ekseni −206) kaydırır." % (KS.Z_GELIS[1] - KS.Z_GELIS[0])),
    (KS.Z_SPREY[0], "SPREY", "Yalnız pide: ürün K girişindeki SABİT gıda nozülünün (Spraying Systems PulsaJet AAB10000AUH-104210-VIFC + TPU11002 PWMD · 110° yassı yelpaze · %.0f mm yukarıda · %.0f mm genişlik) altından BÜTÜNÜYLE geçer: son 65 mm fırın bandında (%.1f s), kalanı K bandında (%.1f s). PWM darbe oranı ürün hızıyla orantılı (tepe ≈ %%%.0f) → yüzeyde eşit ≈ 8 g tereyağı (45 °C)." % (SP["yukseklik"], SP["genislik"], SP["firin_bandi_s"], KS.Z_SPREY[1] - KS.Z_SPREY[0], SP["pwm_tepe"])),
    (KS.Z_KES[0], "KESİM", "Festo DGRF-C-63-125 kafayı %.1f s'de 125 mm indirir (6 bar 1870 N); 6 bıçak birlikte keser, bıçak bandın 0,5 mm üstünde strok sonunda durur. %.1f s bekler." % (KS.Z_KES[1] - KS.Z_KES[0], KS.Z_KES[2] - KS.Z_KES[1])),
    (KS.Z_KES[2], "KALKIŞ", "Kafa %.1f s'de kalkar (strok sonu çarpma enerjisi %.2f J ≤ 1,3 J · Festo 562221)." % (KS.Z_KES[3] - KS.Z_KES[2], 0.5 * Z["kutle"]["KESICI"] * (1.4 * 125.0 / (KS.Z_KES[3] - KS.Z_KES[2]) / 1000.0) ** 2)),
    (KS.Z_TASI[0], "TAŞI", "Bant ürünü 220 mm ileri taşır (%.1f s); ön kenarı E'ye girer — E kutusu hazır bekler (kapak 85°, köprü yukarıda)." % (KS.Z_TASI[1] - KS.Z_TASI[0])),
    (KS.Z_IN[0], "İTİCİ GİRER", "SMC MY1B10G-350 (Z) iticiyi ürünün arkasına %.2f s'de getirir: 350 mm, ort. %.0f mm/s — lastik tampon sınırı (katalog s. 8-11-19, %.2f kg)." % (KS.T_Z, 350.0 / KS.T_Z, Z["kutle"]["Z_hareketli"])),
    (KS.Z_ITME[0], "İTME", "SMC MY1B10G-250 (X) ürünü %.2f s'de 240 mm kutuya sürer (ort. %.0f mm/s · iki uçta RB0805 şok emici · X arabası %.2f kg). Ürün E'nin kalıp rayına iner, sonra kutu tabanına oturur." % (KS.T_X, 250.0 / KS.T_X, Z["kutle"]["X_hareketli"])),
    (KS.Z_X_DON[0], "DÖNÜŞ", "X geri döner (%.2f s), sonra Z arkaya çekilir (%.2f s). K %.1f s'de bir sonraki ürüne hazır; K + E birlikte bir ürün %.1f s." % (KS.T_X, KS.T_Z, KS.Z_Z_DON[1], KS.DONGU_KE)),
]
hes = dict(
    kesme="Festo DGRF-C-GF-63-125-PPV-A-R · 6 bar 1870 N itme · strok 125 · bıçak yıldızı Ø296 × 6 · kesici hareketli kütle %.1f kg" % Z["kutle"]["KESICI"],
    hava="kesim başına %.1f NL (Ø63 × 125 çift etkili, 6 bar) · saatte 60 ürünle %.0f NL/dk + iki MY1B10 (ihmal edilir) · SMC AW20-F02-A 5 µm · SS5Y3-20-04 valf adası" % (NL, NL * 60 / 60.0),
    yag="pide başına 8 g [V] · günde 640 g (80 pide) · 2 gün 1,41 L → Walther Pilot MDG 3 6 bar (3,2 L dolum / 2,5 L kullanılır · nozül 2,76 bar + hortum 0,53 + yükseklik ≈ 3,4 bar) alt dolapta · pnömatik karıştırıcı 46-200 (faz ayrılması) · ısıtma manşeti + 20 mm yalıtım · SSCo 11438-45S · ifm LMT121 · Kletti DN6 ısıtmalı hortum (≈ 2,4 m) · nozül ısıtıcı blok 20 W · 3 × E5DC",
    itici="Z MY1B10G-350: %.2f s · X MY1B10G-250 + 2 × RB0805: %.2f s · MGN15 raylar · MY-J10 yüzer bağlantı · X arabası %.2f kg (6082 cepli; Codex zarfı 9,6 kg idi, silindir sınırı 5 kg)" % (KS.T_Z, KS.T_X, Z["kutle"]["X_hareketli"]),
    bant="Interroll RollerDrive EC5000 AI ø50 IP66 24 V 35 W 49:1 · Habasit CD.F20-A-UW 2 mm beyaz TPU (EU 10/2011 + FDA) 380 geniş · UHMW kayma tablası",
    pano="Siemens S7-1200 CPU 1214C DC/DC/DC (14 DI / 10 DO / 2 AI · Q0.0 PWM → PulsaJet) · Mean Well NDR-240-24 · 3 × Omron E5DC + 2 × G3PE + DC SSR · C10 sigorta",
    kot="istasyon tabanı 892 · K bandı üstü 996 · üst 1862 · ön düzlem +79 · arka −830 · genişlik 400 (K400)",
)
den = [
    dict(ad="Katılar geçerli", deger="%d parça" % den_k["parca"], sonuc="GEÇTİ" if not den_k["gecersiz"] else "KALDI"),
    dict(ad="Durağan kesişim (bütün parçalar, istisnasız)", deger="%d" % len(den_k["durgun"]), sonuc="GEÇTİ" if not den_k["durgun"] else "KALDI"),
    dict(ad="Hareket taraması (kesici + itici gruplar ↔ her şey, 0,1 s + olay anları)", deger="%d" % len(den_k["hareket"]), sonuc="GEÇTİ" if not den_k["hareket"] else "KALDI"),
    dict(ad="Ürün yolu Ø300 × 15 (0,05 s; bıçak teması ve E'ye geçiş beklenen)", deger="%d" % len(den_k["urun"]), sonuc="GEÇTİ" if not den_k["urun"] else "KALDI"),
    dict(ad="Havada parça (0,25 mm temas ağı)", deger="%d bileşen" % (1 + len(den_k["havada"])), sonuc="GEÇTİ" if not den_k["havada"] else "KALDI"),
] + [dict(ad=e["eksen"], deger="%.2f s · ort. %.0f · çarpma %.0f mm/s · %s" % (e["sure"], e["v_ort"], e["v_carpma"], e["not_"]), sonuc="GEÇTİ" if e["ok"] else "KALDI") for e in Z["eksen"]]
def _tr(t):
    return re.sub(r"(\d)\.(\d)", r",", t)
adim_k = [(a, b, _tr(c)) for a, b, c in adim_k]
hes = {k: _tr(v) for k, v in hes.items()}
for d_ in den:
    d_["deger"] = _tr(d_["deger"])
K = dict(surum="K v9 (30 Eyl 2026 · Claude · K v8 üstüne gıda sınıfı tereyağı sistemi)", sprey=SP, adim=[dict(t=a[0], ad=a[1], not_=a[2]) for a in adim_k], hesap=hes, denetim=den,
         kutle=Z["kutle"], dongu=KS.DONGU, dongu_KE=round(KS.DONGU_KE, 2), E_basla_K=round(KS.E_BASLA_K, 2), catal_K=[round(c, 2) for c in KS.CATAL_K],
         acik=["Gerçek tereyağıyla (42 mPa·s) debi + yelpaze açısı: tartarak kalibre (katalog değerleri su içindir)", "BSPT gıda kodu AAB10000AUH-104210-VIFC + PWMD yazımı: Spraying Systems teyidi",
               "Walther Pilot MDG 3: gıda uygunluk beyanı, conta sınıfı, manşet gücü", "Kletti gıda ısıtmalı hortumu: dış çap ≤ 30 mm şartı + çizim",
               "Tereyağı faz ayrılması: karıştırıcı yeterli mi / sadeyağ", "E3Z-T61 ışın ekseni yüksekliği · EC5000 AI hız önayarları"])
(KOK / "otonom" / "hat3d" / "kesme_v9.json").write_text(json.dumps(K, ensure_ascii=False, indent=1), encoding="utf-8")
_toplam = {}
for p_ in KS.PARCALAR:
    b_ = p_.get("bom")
    if not b_: continue
    ad_, adet_ = b_[0], b_[1]
    key = ad_
    if key not in _toplam: _toplam[key] = [ad_, adet_, b_[2] if len(b_) > 2 else "", b_[3] if len(b_) > 3 else "", b_[4] if len(b_) > 4 else ""]
_b = _io.StringIO(); w_ = csv.writer(_b, delimiter=";")
w_.writerow(["kalem", "adet", "olcu / not", "kaynak", "tip"])
for r_ in sorted(_toplam.values(), key=lambda r: (r[4] != "SATIN ALMA", r[0])): w_.writerow(r_)
(KOK / "otonom" / "hat3d" / "kesme_v9_bom.csv").write_text("﻿" + _b.getvalue(), encoding="utf-8")
print("kesme_v9_bom.csv yazıldı · %d kalem" % len(_toplam))
print("kesme_v9.json yazıldı · %d adım · %d denetim satırı" % (len(K["adim"]), len(den)))

# ---------------- E v13 ----------------
den_e = json.loads((KOK / "_local" / "e-v13" / "denetim.json").read_text(encoding="utf-8"))
AD_E = {"ITICI": "Vakumlu besleme arabası", "VAC_Y": "Vantuz kaldırma", "NEST": "Destek tablası", "PISTON": "Baskı kafası (piston)", "CNR_LIFT": "Köşe çerçevesi",
        "CNR": "Köşe parmakları", "PARMAK": "Ön dil katlayıcı", "KATLAYICI": "U flap katlayıcı", "KOPRU": "Pizza köprüsü", "KOL": "Kapak kolu", "CATAL": "Robot çatalı"}
hareket = []
for h in KC.zaman_ozeti_v12():
    g = h["eksen"].split()[0]
    hareket.append(dict(t=round(KC.gercek(h["t0"]), 2), sure=round(h["sure_gercek"], 2), eksen=h["eksen"], v=round(h["v_tepe_eski"] / h["phi"], 1), birim=h["birim"], sinir=h["v_sinir"]))
hareket.sort(key=lambda d: d["t"])
E = dict(surum="E v13 (30 Eyl 2026 · Claude · v12 üstüne sıfır sensörleri + Beckhoff 13 eksen + frenli kafa + SMC vakum)", dongu_eski=KC.DONGU, dongu_gercek=round(KC.DONGU_GERCEK, 2), hareket=hareket,
         denetim=dict(kesisim=len(den_e["kesisim"]), makine_karton=len(den_e.get("karton", [])), zaman_ihlal=len(den_e["zaman_ihlal"]), kafa_besleme_mm=den_e["yakin"]["en_kisa_mm"], durgun_v13=len(den_e.get("v13_durgan", []))),
         acik=list(KC.ACIK_V13), cozuldu=["13 eksen: Beckhoff CX9240 + EL6631-0010 + 7 × EL7062 (S7-1200 8/4 eksen yetmez)", "7 sıfır sensörü: Omron E2E-X2MF1 yerleşimi + bayrak / kam",
               "kafa düşmesi: Oriental PKP268D28M2 frenli motor (0,8 N·m · × 3,8)", "vakum: SMC CDQ2B16-20DZ + 4 × ZP3C-T32CFS + ZK2G15K5RWA-08", "robot çatalı: FR5 TCP 1 m/s (katalog) · rampa 0,5 s (kılavuz)"])
(KOK / "otonom" / "hat3d" / "kutu_v13.json").write_text(json.dumps(E, ensure_ascii=False, indent=1), encoding="utf-8")
print("kutu_v13.json yazıldı · %d hareket · döngü %.1f → %.2f s" % (len(hareket), KC.DONGU, KC.DONGU_GERCEK))
