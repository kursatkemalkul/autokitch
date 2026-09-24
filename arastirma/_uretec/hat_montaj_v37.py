# -*- coding: utf-8 -*-
"""v37 (24 Eyl 2026): B = store_cad_v2 (fitil, yan kayış, standart ürünler) + GLB'de çekmece çalışma animasyonu.
v36 (24 Eyl 2026): B ÇEKMECE MODÜLÜ GERÇEK (store_cad_v1): 21 contalı motorlu çekmece + K4 + kart bölmesi, her çekmece ayrı birim.
v35 (24 Eyl 2026): YERLESIM = HAT ATOSA TABLALI v7 (A 700 · C 1800 · F 1500 · K 600 · E 700 = 5300).
TABAN HIZASI: A, C, F, K istasyonlari 1060'ta baslar, altlari taban dolabi; E (kutu katlama) 0-2030 TEK PARCA.
SUREC KOTU TOPPING'den olculur (Kemal "B"): disk 1168 · firin bandi 1166 · kesme plakasi 1164 · kutu tepsisi 1104.
K'deki yedek kutular kaldirildi. Tek FR5 yer rayinda + QR dolabi. Onceki: hat_montaj_v34.py
v7 (22 Eyl 2026): GLB yazicisi DOKU tasiyor; kasetlerin SARI ETIKETI montaj modelinde gorunuyor;
kaset agi ince (0.12/0.35) — kasetin kendi sayfasiyla ayni detay. Onceki: hat_montaj_v6.py
v6 (22 Eyl 2026): TOPPING modulu GERCEK uretim modeli oldu (topping_cad_v1.py) — kabin, PU yalitim, 6 kaset yuvasi + ayirici,
12 tahrik (NEMA23 + planet reduktor, kuru bolmede), sogutma, pano. Kasetler yeni yuvalarina ve icerideki derinligine tasindi.
v5 (22 Eyl 2026): makine/istasyon gorunumu kasetin KENDI sayfasi gibi — butun parcalar + kendi malzemeleri (PC govde seffaf, icerideki helezon gorunur). Vurgu yok. Onceki: hat_montaj_v4.py
v4 (22 Eyl 2026): makine gorunumunde gercek kasetin PC parcalari KATI (seffaf degil) — kaset hayalet gibi durmasin, imlecle kolay secilsin. Sayfadaki 'Icini gor' dugmesi seffaflastirir. Onceki: hat_montaj_v3.py
v3 (22 Eyl 2026): her parca KENDI malzemesini korur (seffaf govde / paslanmaz / POM ayri gorunur) ve kasetin ICI de modele girer (helezon, rotor, mil, kovan, topuz). Onceki: hat_montaj_v2.py
v2 (22 Eyl 2026): her birim KENDI malzemesini alir -> sayfada uzerine gelince O BIRIM parlar, tiklayinca sayfasi acilir (model-viewer materialFromPoint). Her modul icin ayri GLB/USDZ de basilir: istasyon sayfasi kendi modulunu buyuk gosterir. Onceki: hat_montaj_v1.py
AUTOKITCH · MAKİNE ANA MONTAJI v1 (22 Eyl 2026) — TEK GERÇEK KAYNAK: her şeyin makinedeki yeri burada yazılı.
Kemal: "bu çalıştığımız şeyleri parça parça birleştirip makineyi tamamlayabilir miyiz; teknik resimde genel yerleşim var,
o yerlere bunları koyup 3B üretim modelini oluşturalım; sitede komple görüldüğü bir yer olsun; sonra SolidWorks'e ya da STEP'e dökeriz."

NASIL ÇALIŞIR
  · BIRIM listesi = makinenin bütün parçalarının kütüğü. Her satır: nerede (x0,x1 · y0,y1 · z0,z1), ne durumda, kaynağı ne.
  · durum "GERCEK"  → gerçek CAD var; katı modelden okunur, yerine taşınır, ölçüleri DOĞRULANIR (kütükteki zarfla tutmazsa hata verir).
    durum "KUTU"    → henüz modellenmedi; kütükteki ölçüyle kutu çizilir (şeffaf gri). Sıradaki iş bu kutuları gerçeğe çevirmek.
    durum "KATALOG" → satın alınan parça; ölçü kataloglardan, gövde kutu olarak durur (modellemeye gerek yok).
  · Bir birim gerçeğe dönünce: BIRIM satırında durum GERCEK yapılır + kaynak yazılır. Başka hiçbir yeri değiştirmeye gerek yok.
ÇIKTI: otonom/hat3d/hat_v37.glb + .usdz  ·  otonom/hat3d/durum.json (sayfa oradan okur)  ·  FULL_MAKINE/HAT_v37_YERLESIM.step (SolidWorks)
KOORDİNAT (sw_lib ile aynı): X sağa 0 = hattın sol ucu · Y yukarı 0 = zemin · Z öne, modül ÖN YÜZÜ z = 0, gövde z −830'a kadar.
ÖLÇÜLER: teknik_hat_2kol_v19.py (HAT v19 = geçerli pafta). Pafta değişirse buradaki sabitler de değişir; ikisi ayrı yerde yazılmaz, aşağıda v19'dan OKUNUR.
v8 (22 Eyl 2026): TOPPING modulu v2 — kuru bolme 200 (arkada bosluk yok), kaset 120 geriye + ON NIS 84,
evaporator kasetlerin icinden cikarildi, meme yarigi agizdan okunuyor, kaset<->modul cakismasi taraniyor.
Onceki: hat_montaj_v7.py
v9 (22 Eyl 2026): TOPPING v3 — meme yarigi hucre on sinirina kadar (kaset yuvadan CIKIYOR),
evaporator kasetlerin ARKASINA, huni bacasi pideye 40 mm kala biter, kaset alti bosluk 10.
v10 (22 Eyl 2026): TOPPING v4 — evaporator delikli sac perde arkasinda plenumda, baca bastan basa acik.
v11 (22 Eyl 2026): TOPPING v5 (evaporator kuru bolmede, huni yok) + kasetlerin YUVARLAK BORULU surumleri
(kasar v11 · kiyma v6 · kusbasi v5 · sucuk v4) — urun pideye kasetin kendi borusundan iniyor.
v12 (22 Eyl 2026): TOPPING v6 + HARC/SOS KASETI (harc_cad_v1, duckbill valfli) iki yuvaya girdi;
kaset borularinin tuple birlesimi konik oldu (kasar v12 · kiyma v7 · kusbasi v6 · sucuk v5).
v13 (22 Eyl 2026): TOPPING v7 — on cerceve saci kalkti (dis kabuk bes yuz) · HARC/SOS unitesi v2:
VIDA YOK, hortum pompali borulu nozzle.
v14 (22 Eyl 2026): TOPPING v8 — DONER TABLA (x arabasi + tabla O340, 35 dev/dk).
v15 (22 Eyl 2026): TOPPING v9 — kaset borulari yalitimin ust yuzunde bitiyor, yalitimda tek yuvarlak
delik + dozaj kovani; damlama teknesi ve agiz cercevesi silindi. Kasetler: kasar v13 · kiyma v8 ·
kusbasi v7 · sucuk v6 · harc v3.
v16 (22 Eyl 2026): TOPPING v10 — doner tabla TAM URETIM MODELI (tekne + kiris merdiveni + HGR15 +
araba + doner yatak + ayar bilezigi + pancake motor + GT3 kayis zinciri + apron + sensorler).
Kasetler boru ucu y 252: kasar v14 · kiyma v9 · kusbasi v8 · sucuk v7 · harc v4.
"""
import importlib, io, json, math, os, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
OUT = os.path.join(KOK, "otonom", "hat3d"); STEP = os.path.join(KOK, "arastirma", "FULL_MAKINE")
os.makedirs(OUT, exist_ok=True)
from kaset_3d_v3 import Mesh, MM, doku_ad, doku_montaj, etiket_yuzu, usdz_yaz, MALZEME
MALZEME.setdefault("kutu", dict(renk=(0.62, 0.66, 0.72, 0.30), met=0.0, ruf=0.6, saydam=True))
MALZEME.setdefault("katalog", dict(renk=(0.42, 0.46, 0.52, 0.55), met=0.3, ruf=0.5, saydam=True))
MALZEME.setdefault("kabin", dict(renk=(0.80, 0.83, 0.87, 0.13), met=0.1, ruf=0.4, saydam=True))
MALZEME.setdefault("soguk", dict(renk=(0.25, 0.55, 0.85, 0.28), met=0.0, ruf=0.5, saydam=True))
MALZEME.setdefault("sicak", dict(renk=(0.85, 0.35, 0.22, 0.32), met=0.0, ruf=0.5, saydam=True))
MALZEME.setdefault("robot", dict(renk=(0.96, 0.62, 0.10, 0.75), met=0.2, ruf=0.45, saydam=True))
MALZEME.setdefault("sac", dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32))
MALZEME.setdefault("pu", dict(renk=(0.93, 0.88, 0.72, 1.0), met=0.0, ruf=0.85))
MALZEME.setdefault("motor", dict(renk=(0.18, 0.19, 0.22, 1.0), met=0.5, ruf=0.45))
MALZEME.setdefault("bakir", dict(renk=(0.72, 0.45, 0.20, 1.0), met=0.9, ruf=0.35))
MALZEME.setdefault("kart", dict(renk=(0.10, 0.35, 0.22, 1.0), met=0.1, ruf=0.6))

# ---------------------------------------------------------------- v35 · PAFTA: HAT ATOSA TABLALI v7 ----------------------------------------------------------------
# Yerlesim (modul genislikleri, firin/kesme/kutu ic duzeni, robot, QR) ATOSA TABLALI v7'den OKUNUR.
# Cekmece modulu B'nin ic verisi (kolonlar, kotlar) v19 ile BIREBIR ayni ("ORTAK VERI") -> v19'dan okunmaya devam eder.
_p = open(os.path.join(U, "teknik_hat_2kol_v19.py"), encoding="utf-8").read()
_g = {"__name__": "_pafta", "os": os, "math": math}
exec(_p[_p.index("# ======================= VERI ======================="):_p.index("# ======================= YERLESIM =======================")], _g)
_p7 = open(os.path.join(U, "teknik_hat_atosa_tablali_v7.py"), encoding="utf-8").read()
_g7 = {"__name__": "_pafta7", "os": os, "math": math}
exec(_p7[_p7.index("# ======================= ORTAK VERI (HAT 2 KOL v19) ======================="):_p7.index("\nOX, FY_TOP")], _g7)
DZ, H_MAK, H_B = _g7["DZ"], _g7["H_MAK"], _g7["H_B"]                                    # 830 · 2030 · 1060 (TABAN HIZASI)
X_A, W_A, X_BC, W_BC, W_B = _g7["X_A"], _g7["W_A"], _g7["X_C"], _g7["W_C"], _g7["W_B"]   # A 0-700 · C 700-2500 · B 0-2500
X_D, W_D = _g7["X_F"], _g7["W_F"]                # FIRIN: paftada F, sitede oven.html modul_D'yi yukluyor -> harf D
X_K, W_K, X_E, W_E = _g7["X_K"], _g7["W_K"], _g7["X_E"], _g7["W_E"]
HAT_W = _g7["HAT"]                                                                       # 5300
HAZNE = _g7["HAZNE"]                                                                     # firin pisirme haznesi 1400
RZ, OMUZ, ERISIM, RX = _g7["RZ"], _g7["OMUZ"], _g7["ERISIM"], _g7["RX"]
QRX, QRZ = _g7["QRX"], _g7["QRZ"]
KOLON, KOL_Y0, K1_TABAN = _g["KOLON"], _g["KOL_Y0"], _g["K1_TABAN"]
import topping_hesap_v6 as TH, topping_cad_v22 as TC                                      # TOPPING modülü: derinlik dizilimi ve yuva konumları ORADAN okunur
KASET_Z = (TH.Z_KASET[1], TH.Z_KASET[0])
T_KAS = (H_B + TC.KAS[0], H_B + TC.KAS[1])        # v35: kaset kotu CAD'den (paftadaki 1627 VARSAYIMDI)

# ---- v35 · SUREC KOTU (Kemal 24 Eyl "B": TOPPING'e dokunma, digerleri tablanin kotuna insin) ----
# Sayilar topping_cad_v22'den; yazildiktan sonra ASAGIDA parcalarin gercek kutusundan OLCULUP assert edilir.
DISK_UST_Y = 108.0                                # calisma_diski ust yuzu (yerel y)
P = H_B + DISK_UST_Y                              # 1168
BANT_UST = H_B + 106.0                            # 1166 · firin bandi ust kosu (CAD AKT_Y: diskin 2 mm alti)
ZT = TH.Z_KASET[0] + 30.0                         # -170 · tabla ekseni (topping_cad_v22 ile ayni formul)
BANT_Z = (ZT - 145.0, ZT + 145.0)                 # 290 genis · TOPPING'deki aktarma bandiyla ayni
BANT_X0 = X_BC + 2195.0                           # CAD'deki aktarma bandinin tahrik silindiri (hat x 2895) -> devam buradan
PLAKA = BANT_UST - 2.0                            # 1164 · kesme plakasi bandin 2 mm ALTINDA: urun hep asagi iner
TEPSI_Y = PLAKA - 60.0                            # 1104 · kutu tepsisi yuzu (pafta kurali: surec - 60) -> kutu agzi ~1149
E_A0, E_A1 = PLAKA - 90.0, PLAKA + 160.0          # kutulama agzi (pafta: P-90 ... P+160)
F_G1 = BANT_UST + 320.0                           # 1486 · firin govdesi ustu (pafta: bant + 320)
KAIDE = OMUZ - 152.0                              # FR5 taban -> omuz 152 [katalog Fairino FR5 d1]

MODUL = [("A", "MODÜL A · KONİLİ AÇICI (B üstünde)", X_A, W_A), ("B", "MODÜL B · ÇEKMECELER (taban)", X_A, W_B),
         ("C", "MODÜL C · TOPPING (B üstünde)", X_BC, W_BC), ("D", "MODÜL F · KONVEYÖR FIRIN (+ taban)", X_D, W_D),
         ("K", "MODÜL K · KESME + SPREY (+ taban)", X_K, W_K), ("E", "MODÜL E · KUTU KATLAMA (tek parça)", X_E, W_E)]
MODUL_Y = {"A": (H_B, H_MAK), "B": (0.0, H_B), "C": (H_B, H_MAK), "D": (0.0, H_MAK), "K": (0.0, H_MAK), "E": (0.0, H_MAK)}

# ---------------------------------------------------------------- KÜTÜK ----------------------------------------------------------------
# (kod, ad, modül, durum, x0, x1, y0, y1, z0, z1, malzeme, kaynak/not, sayfa)
B = []
def birim(kod, ad, mod, durum, x, y, z, mal="kutu", kaynak="", sayfa=""):
    B.append(dict(kod=kod, ad=ad, modul=mod, durum=durum, x=x, y=y, z=z, mal=mal, kaynak=kaynak, sayfa=sayfa))

# --- C · TOPPING: dozaj kasetleri (GERÇEK olanlar burada) ---
KASET_CAD = {"KAŞAR KABI": ("kasar_cad_v14", "Kaşar kabı v14", "kaset3d/index.html?k=kasar_v14"),
             "KIYMA": ("kiyma_cad_v9", "Kıyma kaseti v9", "kaset3d/index.html?k=kiyma_v9"),
             "KUŞBAŞI": ("kusbasi_cad_v8", "Kuşbaşı kaseti v8", "kaset3d/index.html?k=kusbasi_v8"),
             "KÜP SUCUK": ("sucuk_cad_v7", "Küp sucuk kaseti v7", "kaset3d/index.html?k=sucuk_v7"),
             "HARÇ": ("harc_cad_v4", "Harç / sos ünitesi v4 · pompalı", "kaset3d/index.html?k=harc_v4")}
YUVA_V1 = [(ad, x1 - x0, (x0 + x1) / 2.0) for ad, x0, x1, gen in TC.YUVA]     # yuva adı, genişlik, merkez (modül yerelinde)
for urun, gw, xc in YUVA_V1:
    xa = X_BC + xc - gw / 2.0; anahtar = urun.split()[0] if urun.startswith("HARÇ") else urun
    cad = KASET_CAD.get(anahtar)
    birim("KASET_" + urun.replace(" ", "_"), (cad[1] if cad else "Harç kaseti (KARAR: yap / satın al)"), "C", "GERCEK" if cad else "KUTU",
          (xa + 1.0, xa + gw - 1.0), (T_KAS[0], T_KAS[0] + 360.0), KASET_Z, "pom" if cad else "kutu",
          (cad[0] + ".py") if cad else "modellenmedi · kıyma kaseti macunu pideye YAYAMIYOR, harçta sorun daha ağır (yayıcı kararı)", cad[2] if cad else "")
birim("TOPPING_MODUL", "TOPPING modülü: kabin + yalıtım + 6 yuva + 12 tahrik + soğutma + pano", "C", "GERCEK_MODUL",
      (X_BC, X_BC + W_BC), (H_B, H_B + TC.Y), (-DZ, 0.0), "sac", "topping_cad_v22.py", "")

# --- B · ÇEKMECE MODÜLÜ (v36: GERÇEK üretim modeli store_cad_v1 — her çekmece ayrı birim) ---
import store_cad_v2 as SC
SC_OZET = {k: (t, n) for k, t, n, _u, _a in SC.modul()}
_SC_AD = {"B_KASA": "ÇEKMECE modülü gövdesi: sandviç kabuk + PU + 3 kolon bölmesi + ön çerçeve + plint",
          "B_ELEKTRIK": "K1 üstü pano: Siemens S7-1200 + Mean Well NDR-240-24 + Electromen EM-324C + %d seçici röle" % len(SC.CEK),
          "B_KABLO": "Kablo kanalları 40 × 25: her kolonda dikey + üstte yatay (bölmelerden geçer)",
          "B_SOGUTMA": "Soğutma: Secop CU KLF4.0CND R290 (K4 altı, ızgaralı kapak) + 3 roll-bond evaporatör + ebm-papst fan",
          "B_DEPO": "K4 kaşar + sucuk deposu · kapaklı · +3 °C (içerik VARSAYIM)",
          "B_TEMIZLIK": "K4 temizlik malzemesi nişi · kapaklı"}
_TIP_AD = {"hamur": "taze pide", "lahm": "lahmacun", "icecek": "içecek + tatlı · 2 katlı"}
for _kod in dict.fromkeys(p["birim"] for p in SC.PARCALAR):
    _ps = [p for p in SC.PARCALAR if p["birim"] == _kod]
    _bb = [p["wp"].val().BoundingBox() for p in _ps]
    _x = (min(q.xmin for q in _bb), max(q.xmax for q in _bb)); _y = (min(q.ymin for q in _bb), max(q.ymax for q in _bb))
    _z = (min(q.zmin for q in _bb), max(q.zmax for q in _bb))
    if _kod in SC_OZET:
        _t, _n = SC_OZET[_kod]; _kol = _kod.split("_")[1]
        _ad = "%s · %s çekmecesi %s · %d %s · fitilli · Transmotec motor + GT3 kayış · strok %.0f" % (
            _kol, _TIP_AD[_t], _kod.rsplit("_", 1)[1], _n, "kutu" if _t == "icecek" else "top", SC.STROK)
    else:
        _ad = _SC_AD.get(_kod, _kod)
    birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v1.py", "")

# --- A · PRESS ---
# v28 · PRESS ARTIK "ACICI": Fersah PZP-400 komple makine olarak KULLANILAMIYOR.
# Sebebi olculdu: presin alt plakasi (1150-1170) bizim tablanin yerini istiyor ve
# tabla plakanin TAM ICINDE kaliyor (plaka 580x640, tabla Ø340) — biri digerinin
# altina giremiyor. Ustelik tepsi kalktigi icin duz presin 3-12 kN'lik kuvveti
# dogrudan tablaya, doner yataga ve raya binerdi; o yatak bunu tasimaz.
# Yerine KONILI DONEN ACICI: hamuru yuvarlayarak acar, 40-160 N ister (75 kat az).
# TOPPING'in tablasi modul A'ya girip bu kafanin altina gelir, hamur orada acilir.
# v29: ACICI birimleri MODUL C'ye yazildi. Fiziksel olarak modul A'nin ayak izinde
# duruyorlar ama ISLEVLERI TOPPING'in — ve TOPPING sayfasi ile animasyonu yalniz
# modul_C.glb yukluyor; "A" yazilinca kafa sayfada hic gorunmuyordu.
birim("A_KABIN", "AÇICI modülü kabini (B üstünde · açıcının kendisi TOPPING CAD'inde)", "A", "KUTU", (X_A, X_A + W_A), (H_B, H_MAK), (-DZ, 0.0), "kabin", "pafta ATOSA TABLALI v7")

# ============================ v35 · TABAN HIZASI ============================
# Kemal 24 Eyl: A, C, F(D), K istasyonlarinin ALT TABANI AYNI HIZADA (H_B = 1060); altlari taban dolabi.
# E (kutu katlama) KESILMEZ: yerden 2030'a tek parca (sarjor altta, katlama ustte).
# SUREC: disk 1168 > firin bandi 1166 > kesme plakasi 1164 > kutu agzi ~1149 — urun hep asagi iner.

# --- D · (paftada F) KONVEYOR FIRIN ---
birim("D_TABAN_KABIN", "F taban dolabı 0–1060 (pano · UPS · bulaşık makinesi)", "D", "KUTU", (X_D, X_D + W_D), (0.0, H_B), (-DZ, 0.0), "kabin", "v35 taban hizası")
for kod_, ad_, (a_, b_), (y0_, y1_), dz_, kat_, kay_ in (
        ("D_ROBOT_KONTROL", "Robot kontrol kutusu (FR5) · ray yanında", (60.0, 700.0), (135.0, 270.0), 180.0, True, "pafta v7 · 245 × 180 × 45"),
        ("D_ANA_PANO", "Ana pano · PLC · ana şalter · ekran yok (tablet)", (60.0, 460.0), (320.0, 670.0), 250.0, False, "pafta v7 · 400 × 350 × 250"),
        ("D_UPS", "UPS 500 VA", (480.0, 730.0), (320.0, 670.0), 350.0, True, "pafta v7 · derinlik VARSAYIM"),
        ("D_BULASIK", "Bulaşık makinesi · tezgâh altı · MEIKO M-iClean UM sınıfı · sepet 500 × 500", (760.0, 1220.0), (135.0, 865.0), 600.0, True, "MEIKO UM 460 × 600 × 730"),
        ("D_DETERJAN", "Makine deterjanı + parlatıcı 2 × 5 L bidon", (1250.0, 1440.0), (135.0, 500.0), 300.0, False, "pafta v7 · derinlik VARSAYIM")):
    birim(kod_, ad_, "D", "KATALOG" if kat_ else "KUTU", (X_D + a_, X_D + b_), (y0_, y1_), (-20.0 - dz_, -20.0), "katalog" if kat_ else "kutu", kay_)
birim("D_FIRIN_GOVDE", "Konveyör fırın gövdesi · özel · elektrikli · taban 1060 · bant altı pay 106 (alt ısıtma: ince rezistans / taş — VARSAYIM)", "D", "KUTU",
      (X_D, X_D + W_D), (H_B, F_G1), (-DZ, 0.0), "sicak", "pafta v7 · gövde tabanı 1040 -> 1060 (taban hizası), bant 1340 -> 1166 (Kemal B)")
birim("D_HAZNE", "Pişirme haznesi 1400 · aynı anda 4 ürün (adım 350) · üst + alt ısıtma", "D", "KUTU",
      (X_D + 50.0, X_D + 50.0 + HAZNE), (H_B + 20.0, BANT_UST + 270.0), (-500.0, -10.0), "sicak", "pafta v7 · ön duvar 10 (bant z -25'e kadar geliyor)")
birim("D_BANT", "Fırın bandı (devamı) · 290 · üst yüz 1166 · TOPPING'deki bıçak burunlu aktarma bandının devamı", "D", "KUTU",
      (BANT_X0, X_K + 15.0), (BANT_UST - 61.5, BANT_UST), BANT_Z, "koyu", "PTFE kaplı cam elyaf örgü · genişlik ve eksen topping_cad_v22'den")
birim("D_DAVLUMBAZ", "Egzoz davlumbazı · fan · yağ + karbon filtre · fırın kartı + SSR + kontaktör", "D", "KUTU", (X_D, X_D + W_D), (F_G1 + 10.0, H_MAK), (-DZ, 0.0), "kutu", "pafta v7")

# --- K · KESME + SPREY (ayri istasyon) ---
birim("K_TABAN_KABIN", "K taban dolabı 0–1060 · yedek kutu KALDIRILDI (Kemal 24 Eyl)", "K", "KUTU", (X_K, X_K + W_K), (0.0, H_B), (-DZ, 0.0), "kabin", "v35 taban hizası")
birim("K_YAG", "Yağ kartuşu 4 L × 2 · ısıtmalı", "K", "KUTU", (X_K + 60.0, X_K + 300.0), (140.0, 330.0), (-420.0, -20.0), "kutu", "pafta v7")
birim("K_KART", "K kontrol kartı · tahrik", "K", "KUTU", (X_K + 320.0, X_K + 540.0), (140.0, 330.0), (-220.0, -20.0), "kutu", "pafta v7")
birim("K_KABIN", "KESME + SPREY istasyonu kabini 1060–2030", "K", "KUTU", (X_K, X_K + W_K), (H_B, H_MAK), (-DZ, 0.0), "kabin", "v35 taban hizası")
birim("K_PLAKA", "Kesme plakası 560 × 450 · üstü 1164 (fırın bandının 2 mm altı)", "K", "KUTU", (X_K + 20.0, X_K + 580.0), (PLAKA - 14.0, PLAKA), (-470.0, -20.0), "sac", "pafta v7 · kot v35")
birim("K_ITICI", "İtici · kutuya süren", "K", "KUTU", (X_K + 24.0, X_K + 64.0), (PLAKA + 2.0, PLAKA + 50.0), (-470.0, -20.0), "kutu", "pafta v7")
birim("K_BICAK", "Yıldız bıçak Ø300 · 6 dilim · piston 100 strok", "K", "KUTU", (X_K + 110.0, X_K + 490.0), (PLAKA + 90.0, PLAKA + 340.0), (ZT - 150.0, ZT + 150.0), "kutu", "pafta v7")
birim("K_SPREY", "Tereyağı spreyi", "K", "KUTU", (X_K + 505.0, X_K + 535.0), (PLAKA + 105.0, PLAKA + 135.0), (ZT - 15.0, ZT + 15.0), "kutu", "pafta v7")
birim("K_ICECEK_YEDEK", "İçecek + tatlı yedeği · 4 gün (97 kutu 330 ml + 8 tatlı)", "K", "KUTU", (X_K + 33.0, X_K + W_K - 33.0), (PLAKA + 355.0, H_MAK - 2.0), (-800.0, -30.0), "kutu", "pafta v7")

# --- E · KUTU KATLAMA (TEK PARCA, kesilmez) ---
birim("E_KABIN", "KUTU katlama kabini · TEK PARÇA 0–2030 (kesilmez)", "E", "KUTU", (X_E, X_E + W_E), (0.0, H_MAK), (-DZ, 0.0), "kabin", "pafta v7")
birim("E_SARJOR", "Kutu şarjörü · alttan kaldırmalı · blank 400 × 760 yatay yığın", "E", "KUTU", (X_E + 150.0, X_E + 550.0), (123.0, E_A0 - 10.0), (-786.0, -25.0), "kutu", "pafta v7")
birim("E_AGZ", "Kutulama ağzı · kutu 320 × 320 × 45", "E", "KUTU", (X_E + 30.0, X_E + W_E - 30.0), (E_A0, E_A1), (-500.0, 0.0), "kutu", "pafta v7 · kot v35")
birim("E_TEPSI", "Kutu tepsisi Ø340 · yüzü 1104 (kutu ağzı plakanın ~15 mm altı)", "E", "KUTU", (X_E + W_E / 2.0 - 170.0, X_E + W_E / 2.0 + 170.0), (TEPSI_Y - 12.0, TEPSI_Y), (ZT - 170.0, ZT + 170.0), "sac", "pafta v7 · kot v35")
birim("E_KALIP", "Kalıp + plunger · vantuz · strok 250", "E", "KUTU", (X_E + 60.0, X_E + 400.0), (E_A1 + 30.0, E_A1 + 330.0), (-760.0, -20.0), "kutu", "pafta v7")
birim("E_VAKUM", "Vakum pompası", "E", "KUTU", (X_E + 420.0, X_E + 640.0), (E_A1 + 30.0, E_A1 + 170.0), (-400.0, -20.0), "kutu", "pafta v7")
birim("E_KART", "E kontrol kartı · tahrik", "E", "KUTU", (X_E + 420.0, X_E + 640.0), (E_A1 + 185.0, E_A1 + 330.0), (-200.0, -20.0), "kutu", "pafta v7")

# --- ROBOT (tek FR5, yer rayinda) + QR DOLABI (hattin onunde, z > 0) ---
birim("ROBOT_RAY", "Yer rayı · tek araba · x 200–5100", "-", "KATALOG", (200.0, 5100.0), (0.0, 60.0), (RZ - 120.0, RZ + 120.0), "katalog", "pafta v7")
birim("ROBOT_1", "Fairino FR5 · tek robot (pafta konumu x %.0f)" % RX, "-", "KATALOG", (RX - 90.0, RX + 90.0), (60.0, KAIDE), (RZ - 90.0, RZ + 90.0), "robot", "katalog · kaide + araba")
birim("ROBOT_1_KOL", "FR5 omuz + kol zarfı (erişim %.0f)" % ERISIM, "-", "KATALOG", (RX - 120.0, RX + 120.0), (KAIDE, OMUZ + 180.0), (RZ - 120.0, RZ + 120.0), "robot", "yalnız ZARF · gerçek kol modeli yok")
birim("QR_DOLABI", "QR teslim dolabı · 2 × 6 göz · koridorun karşısında", "-", "KUTU", QRX, (0.0, 2000.0), QRZ, "kutu", "pafta v7 · ayrıntı SERVİS_TESLİM")

DURUM_RENK = {"GERCEK": "gerçek CAD", "GERCEK_PARCA": "kısmen gerçek", "KUTU": "kutu (modellenmedi)", "KATALOG": "katalog (satın alınan)"}


# ---------------------------------------------------------------- GEOMETRİ ----------------------------------------------------------------
DOKU = {}                                                          # v7: kaset basina etiket dokulari (kutuk kurulurken dolar)


def kutu_kat(b):
    (x0, x1), (y0, y1), (z0, z1) = b["x"], b["y"], b["z"]
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def alinir(ad):
    """v5: kasetin BUTUN parcalari girer — Kemal "parcayi acinca gozuken sekilde gozuksun" dedi.
    Istasyon sayfasi artik kasetin kendi sayfasiyla ayni seyi gosteriyor."""
    return True


def kaset_parcalari(modul):
    """kasetin BÜTÜN parçaları — kendi sayfasındakiyle birebir aynı model (v5)."""
    V = importlib.import_module(modul); V.PARCALAR[:] = []; V.kap()
    return V, [p for p in V.PARCALAR if alinir(p["ad"])]


def mesh_otele(m, dx, dy, dz):
    """hazır ağı (MM ölçeğinde) kütükteki yerine taşır — etiket yüzleri katı değil, doğrudan ağ"""
    y = Mesh(); y.P = [(p[0] + dx, p[1] + dy, p[2] + dz) for p in m.P]; y.N = list(m.N); y.I = list(m.I)
    y.UV = list(m.UV) if m.UV else None
    return y


def montaj_adimlari(modul):
    """kaset üretecinin kaynağındaki doku_montaj([...]) listesini okur — etiketin montaj yüzü için.
    (etiketler() kaset üretecinde __main__ bloğunun İÇİNDE tanımlı, import edilince erişilemiyor.)"""
    import re
    yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), modul + ".py")
    k = io.open(yol, encoding="utf-8").read()
    m = re.search(r"doku_montaj\(\[(.*?)\]\)", k, re.S)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else ["MONTAJ|KASET SAYFASINDA"]


def yuva_etiketleri(b, dokular):
    """v18 · yuvanin ustundeki plakaya urun adi. Kaset govdeleri ORTAK oldugu icin urun bilgisi
    makinede duruyor (Kemal: 'belki de yuvalarin onune etiket koymak lazim').
    Kotlar topping_cad_v11'den okunur; burada tek sayi tanimlanmaz."""
    L, x0m, y0m = [], b["x"][0], b["y"][0]
    z1 = TC.ET_Z1 * MM                                            # plakanin ON yuzu (+z'ye bakar)
    for ad, x0, x1, gen in TC.YUVA:
        # DIKKAT: kodda CIFT ALT CIZGI olmamali — dugum adi "<birim>__<ton>" kalibinda, ucuncu bir "__"
        # hareketli paket sanilip sahte grup aciyor (sim3d dugum adini "__" ile boluyor).
        tr = {"Ç": "C", "Ğ": "G", "İ": "I", "Ö": "O", "Ş": "S", "Ü": "U"}
        kod = "".join(tr.get(c, c) for c in ad.replace(" ", "_"))
        kod = "".join(c if (c.isalnum() and ord(c) < 128) else "_" for c in kod)
        while "__" in kod: kod = kod.replace("__", "_")
        ton = "etiket_yuva_" + kod
        dokular[ton] = doku_ad(TC.URUN[ad], "yuva %.0f mm  ·  kaset %s" % (gen, TC.KASET_CAD[ad]), ok_sol=False)
        MALZEME.setdefault(ton, dict(MALZEME["etiket_ad"]))       # ton tablosu kaset etiketiyle ayni
        ma = mal_ad(b, ton); MALZEME[ma]["doku"] = ton
        ax0, ax1 = (x0m + x0 + 15.0) * MM, (x0m + x1 - 15.0) * MM
        ay0, ay1 = (y0m + TC.ET_Y0) * MM, (y0m + TC.ET_Y1) * MM
        m = Mesh()
        m.quad((ax0, ay0, z1), (ax1, ay0, z1), (ax1, ay1, z1), (ax0, ay1, z1), (0, 0, 1),
               uv=[(0, 1), (1, 1), (1, 0), (0, 0)])
        L.append((ton, m.duzelt(), ma))
    return L


def kaset_etiketleri(V, b, dokular):
    """kasetin sarı bandı: −x yüzünde AD, +x yüzünde MONTAJ, ikisinin arkasında sarı yüz.
    Geometri kaset üretecindekiyle birebir; doku her kasete ÖZEL üretilir (hepsinde aynı yazı çıkmasın)."""
    kod = "".join(c if (c.isalnum() and ord(c) < 128) else "_" for c in b["kod"])
    e0, e1 = (V.Y_UST - 56) * MM, (V.Y_UST - 8) * MM
    ez = (V.D / 2 - V.TP - 6) * MM; xo = (V.RB + V.ET + 0.4) * MM
    olcu = "%d × %d × %d mm" % (V.W, V.D, V.H)
    dokular["ad_" + kod] = doku_ad(b["ad"].upper(), "bu yönde tak  ·  " + olcu + "  ·  çıkış ÖNDE alttan", ok_sol=True)
    dokular["montaj_" + kod] = doku_montaj(montaj_adimlari(b["kaynak"][:-3]))
    # Malzeme adi mal_ad() kalibinda olmali: modul GLB'si parcalari mal[1] == modul harfi diye suzuyor
    # (duz "etiket_ad_..." adi o suzgece takilip modul dosyasina GIRMIYORDU). Ayrica "__" kalibi sayesinde
    # etikete gelince de kasetin kendisi seciliyor.
    for ton, dk in (("etiket_ad", "ad_" + kod), ("etiket_montaj", "montaj_" + kod), ("sari_arka", None)):
        ma = mal_ad(b, ton)
        if dk: MALZEME[ma]["doku"] = dk
    L = [("etiket_ad", etiket_yuzu(-xo, e0, e1, -ez, ez, -1)), ("etiket_montaj", etiket_yuzu(xo, e0, e1, ez, -ez, 1))]
    for _ad, xx, nx in ((1, -xo + 0.0002, 1), (2, xo - 0.0002, -1)):
        ar = Mesh(); ar.quad((xx, e0, -ez), (xx, e0, ez), (xx, e1, ez), (xx, e1, -ez), (nx, 0, 0))
        L.append(("sari_arka", ar.duzelt()))
    return [(t, m, mal_ad(b, t)) for t, m in L]


def yerlestir(sh, b, V):
    """kaset katısını kütükteki yere taşır: yerel x ortada, z ön yüz +D/2, y taban 0 → hedef kutunun sol-alt-ön köşesi"""
    (x0, x1), (y0, _), (_, z1) = b["x"], b["y"], b["z"]
    return sh.translate(cq.Vector((x0 + x1) / 2.0, y0, z1 - V.D / 2.0))


def kutu_ag(b):
    """kutu birimin ağı (6 yüz) — makine görünümünde 'henüz modellenmedi' kutusu"""
    (x0, x1), (y0, y1), (z0, z1) = b["x"], b["y"], b["z"]; m = Mesh()
    K = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    for a_, b_, c_, d_, n_ in ((0, 3, 2, 1, (0, 0, -1)), (4, 5, 6, 7, (0, 0, 1)), (0, 1, 5, 4, (0, -1, 0)), (3, 7, 6, 2, (0, 1, 0)), (0, 4, 7, 3, (-1, 0, 0)), (1, 2, 6, 5, (1, 0, 0))):
        m.quad(tuple(c * MM for c in K[a_]), tuple(c * MM for c in K[b_]), tuple(c * MM for c in K[c_]), tuple(c * MM for c in K[d_]), n_)
    return m.duzelt()


# ---- HAREKETLI PAKETLER (v17): parca adindan hangi grupta oldugu -------------------------------
# Bu liste sim_topping_v1.py'deki ayrimin aynisi; artik tek yerde, uretim modelinin icinde.
ARABA_P = ("kizak_blogu_", "araba_plakasi", "doner_yatak", "ayar_bilezigi", "donus_motoru", "tahrik_lokmasi",
           "siyirici_apron", "kayis_kolu", "kayis_kelepcesi_", "tabla_home_sensoru", "tabla_home_bayragi", "x_bayragi",
           "kilit_burcu_")                               # v20: kilit burclari ayar bileziginde -> ARABA ile gezer
# v20: CALISMA DISKI ve DISK PIMLERI tablanin ustunde, onunla birlikte doner.
# Listeye eklenmeyince SABIT sayiliyor ve tabla giderken geride kaliyorlardi
# (Kemal: "su parcalar ne, sil onlari" — ortada duran buyuk beyaz disk buydu).
TABLA_P = ("tabla_gobegi", "tabla", "merkezleme_pimi_", "calisma_diski", "disk_pimi_")


# v21 · ACICI ve BANT hareketli paketleri — animasyon icin AYRI DUGUM yazilir.
# Koniler kendi eksenlerinde doner, kafa dikeyde iner-kalkar, bant silindirleri doner.
KONI_ON_P = ("acici_konisi_on", "acici_mili_on")
KONI_ARKA_P = ("acici_konisi_arka", "acici_mili_arka")
ACICI_P = ("acici_yatagi_", "acici_reduktoru_", "acici_motoru_", "acici_askisi_", "acici_kafa_plakasi")
BANT_TAM = ("bant",)                       # bandin kendisi (yerinde durur)
BURUN_TAM = ("bant_burun_silindiri",)      # doner
TAHRIK_TAM = ("bant_tahrik_silindiri",)    # doner


def grup_modul(ad):
    if ad in BANT_TAM: return "BANT"
    if ad in BURUN_TAM: return "BANT_BURUN"
    if ad in TAHRIK_TAM: return "BANT_TAHRIK"
    if ad.startswith(KONI_ON_P): return "KONI_ON"
    if ad.startswith(KONI_ARKA_P): return "KONI_ARKA"
    if ad.startswith(ACICI_P): return "ACICI"
    if ad.startswith(TABLA_P) and ad not in ("tabla_home_sensoru", "tabla_home_bayragi"): return "TABLA"
    if ad.startswith(ARABA_P): return "ARABA"
    return "SABIT"


def dugum_ad(kod, ton, grup):
    return "%s__%s" % (kod, ton) if grup == "SABIT" else "%s__%s__%s" % (kod, ton, grup)


def mal_ad(b, ton=None):
    """Malzeme adi = M<modul>_<kod>[__<ton>]. Sayfa "__" oncesini alip hangi BIRIM oldugunu bulur;
    "__" sonrasi parcanin kendi tonudur (cam / celik / pom / silikon) — kaset renksiz tek blok gorunmesin."""
    tr = {"Ç": "C", "Ğ": "G", "İ": "I", "Ö": "O", "Ş": "S", "Ü": "U"}
    kod = "".join(tr.get(c, c) for c in b["kod"])
    kod = "".join(c if (c.isalnum() and ord(c) < 128) or c == "_" else "_" for c in kod)
    ad = "M%s_%s" % ("R" if b["modul"] == "-" else b["modul"], kod)          # USD prim adi: yalniz ASCII harf/rakam/alt cizgi
    if ton:
        ad += "__" + ton
    MALZEME.setdefault(ad, dict(MALZEME[ton or b["mal"]]))          # parca kendi tonunda kalir (PC seffaf, paslanmaz metalik, POM mat)
    return ad


ANIM = []                                                                                # v37: (dugum adi, zamanlar, oteleme) listesi


def glb_yaz(yol, parcalar, dokular):
    """animasyonsuz sade GLB (kaset dosyalarındaki yazıcının hat sürümü): yalnız kullanılan malzemeler yazılır"""
    import struct
    kullanilan = sorted(set(mal for _a, _m, mal in parcalar)); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]
    def gomu(bt, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt); return len(views) - 1
    for adi, m, mal in parcalar:
        vp = gomu(struct.pack("<%df" % (3 * len(m.P)), *[c for p in m.P for c in p]), 34962)
        vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for nn in m.N for c in nn]), 34962)
        vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
        mn = [min(p[k] for p in m.P) for k in range(3)]; mx = [max(p[k] for p in m.P) for k in range(3)]
        accs.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": mn, "max": mx})
        accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
        accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
        attr = {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}; ind = len(accs) - 1
        if m.UV:                                                                        # v7: etiket yuzleri doku koordinati tasiyor
            vu = gomu(struct.pack("<%df" % (2 * len(m.UV)), *[c for u in m.UV for c in u]), 34962)
            accs.append({"bufferView": vu, "componentType": 5126, "count": len(m.UV), "type": "VEC2"}); attr["TEXCOORD_0"] = len(accs) - 1
        meshes.append({"name": adi, "primitives": [{"attributes": attr, "indices": ind, "material": kullanilan.index(mal)}]})
        nodes.append({"mesh": len(meshes) - 1, "name": adi})
    anim_sm, anim_ch = [], []                                                            # v37: cekmece calisma animasyonu
    if ANIM:
        ad2node = {n["name"]: i for i, n in enumerate(nodes)}
        for ad_, T, V in ANIM:
            if ad_ not in ad2node:
                continue
            vi = gomu(struct.pack("<%df" % len(T), *T))
            accs.append({"bufferView": vi, "componentType": 5126, "count": len(T), "type": "SCALAR", "min": [min(T)], "max": [max(T)]})
            vo = gomu(struct.pack("<%df" % (3 * len(V)), *[c for v_ in V for c in v_]))
            accs.append({"bufferView": vo, "componentType": 5126, "count": len(V), "type": "VEC3"})
            anim_sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"})
            anim_ch.append({"sampler": len(anim_sm) - 1, "target": {"node": ad2node[ad_], "path": "translation"}})
    images, textures, doku_idx = [], [], {}
    for k_, veri in sorted(dokular.items()):                                            # v7: PNG'ler GLB'ye gomulur
        images.append({"bufferView": gomu(veri), "mimeType": "image/png"}); textures.append({"source": len(images) - 1, "sampler": 0}); doku_idx[k_] = len(textures) - 1
    mats = []
    for k in kullanilan:
        d = MALZEME[k]; pbr = {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}
        if d.get("doku") and d["doku"] in doku_idx: pbr["baseColorTexture"] = {"index": doku_idx[d["doku"]]}
        mm = {"name": k, "pbrMetallicRoughness": pbr, "doubleSided": not d.get("tekyuz", False)}
        if d.get("saydam"): mm["alphaMode"] = "BLEND"
        mats.append(mm)
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH hat_montaj_v16"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes, "meshes": meshes,
         "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}],
         "images": images, "textures": textures, "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}]}
    if anim_ch:
        g["animations"] = [{"name": "cekmece_calisma", "samplers": anim_sm, "channels": anim_ch}]
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    return len(bb) + len(js)


def TC_AG(wp, kaba=False):
    """TOPPING parçaları için ağ — kaset üreteçlerindeki ag() ile aynı, kaba ayarda.

    v24 · KABA SEÇENEĞİ: satın alınan elektroniğin (STP-DRV-4830 sürücü, STP-MTR-23079
    motor, SureGear redüktör) üretici STEP'leri DIP anahtarına, klemens dişine kadar
    modelli. On ikişer tanesi site GLB'sini telefonun kaldıramayacağı boya çıkarıyor.
    TUZAK: bu STEP'ler İÇLERİNDE HAZIR ÜÇGEN AĞI taşıyor; OpenCascade toleransı ne
    verirsen ver o hazır ağı döndürüyor (ölçüldü: 0,12 ile 2,0 arası aynı üçgen sayısı).
    O yüzden önce BRepTools.Clean ile saklı ağ siliniyor, sonra kaba ağlanıyor.
    Dış ölçüler ve konumlar AYNI kalır; yalnız süslemesi azalır."""
    import kiyma_cad_v6 as _K
    if kaba:
        from OCP.BRepTools import BRepTools
        sh = wp.val().copy()
        BRepTools.Clean_s(sh.wrapped)
        return _K.ag(cq.Workplane(obj=sh), 0.6, 0.8)
    return _K.ag(wp, 0.6, 1.0)


if __name__ == "__main__":
    t0 = time.time(); parcalar, asm, sayac, AG = [], cq.Assembly(name="HAT_v1"), {}, None
    RENK = dict(pom=(0.95, 0.95, 0.93, 1), kutu=(0.62, 0.66, 0.72, 0.4), katalog=(0.42, 0.46, 0.52, 0.6), soguk=(0.25, 0.55, 0.85, 0.35),
                sicak=(0.85, 0.35, 0.22, 0.4), robot=(0.96, 0.62, 0.10, 0.8), kabin=(0.8, 0.83, 0.87, 0.2))
    for b in B:
        sayac[b["durum"]] = sayac.get(b["durum"], 0) + 1
        if b["durum"] == "GERCEK_MODUL":
            TC.PARCALAR[:] = []; TC.modul()
            # Makine gorunumunde ON KAPAK ve contasi cizilmez: kapak kapaliyken kasetler ne gorunur ne secilebilir.
            # Kapak gercek: kendi STEP'i ve BOM'u topping_modul_v1 klasorunde duruyor; burada ACIK kabul ediliyor.
            # v27: ON KAPAGIN PU CEKIRDEGI DE CIZILMEZ. Liste v15'ten beri eksikti:
            # kapak o surumde masif bloktan SAC KABUK + PU CEKIRDEK'e cevrilmisti,
            # "on_kapak" ve contasi disarida birakildi ama "on_kapak_pu" listeye
            # eklenmedi. Sonuc: kapagin yalitim dolgusu tek basina duruyor ve
            # kasetlerin onunu kapatiyordu (Kemal: "kasetleri goremiyorum").
            KAPAK = ("on_kapak", "on_kapak_pu", "kapak_contasi")
            ps = [p for p in TC.PARCALAR if not p["ad"].startswith("_bom") and p["ad"] not in KAPAK]
            ton = {}
            for p in ps:
                sh = p["wp"].val().translate(cq.Vector(b["x"][0], b["y"][0], 0.0))
                # v26 · KUTU YOK. Kemal sirketteki BILGISAYARDAN bakiyor, telefondan
                # degil — boyut kaygisi yersizdi. Sitedeki makine Isaac'teki ikizle
                # AYNI: satin alinan her parca kendi gercek uretici CAD'iyle ciziliyor,
                # surucu de motor de redüktör de. (v25'te suruculer zarf kutusuydu.)
                # Kaba aglama duruyor: uretici STEP'leri icinde hazir ag tasidigindan
                # BRepTools.Clean'siz tolerans hic islemiyor — TC_AG(kaba=True) onu yapar.
                _kaba = p["ad"].startswith(("surucu_", "motor_", "reduktor_", "x_motoru"))
                ton.setdefault((p["mal"], grup_modul(p["ad"])), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh), _kaba))
                asm.add(sh, name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK.get(p["mal"], RENK["kutu"])))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            for i_, (ad_, m_, mal_) in enumerate(yuva_etiketleri(b, DOKU)):      # v18: yuva urun etiketleri
                parcalar.append(("%s__%s%d" % (b["kod"], ad_, i_), m_, mal_))
            b["parca"] = len(ps)
        elif b["durum"] == "GERCEK_STORE":
            ps = [p for p in SC.PARCALAR if p["birim"] == b["kod"]]
            ton = {}
            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(p["wp"]))
                asm.add(p["wp"].val(), name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK.get(p["mal"], RENK["kutu"])))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)
        elif b["durum"] == "GERCEK":
            V, ps = kaset_parcalari(b["kaynak"][:-3]); AG = AG or V
            zarf = (b["x"][1] - b["x"][0], b["y"][1] - b["y"][0], b["z"][1] - b["z"][0])
            assert abs(V.W - zarf[0]) < 0.6 and abs(V.H - zarf[1]) < 0.6 and abs(V.D - zarf[2]) < 0.6, \
                "%s: kutukte zarf %s, CAD %s — pafta ile model TUTMUYOR" % (b["kod"], zarf, (V.W, V.H, V.D))
            ton = {}                                                       # her TON ayri ag + ayri malzeme -> renkler korunur
            for p in ps:
                sh = yerlestir(p["wp"].val(), b, V)
                gr_ = p.get("grup")
                gr_ = "SABIT" if not gr_ else ("HELEZON" if gr_ == "helezon" else "KARISTIRICI")
                ton.setdefault((p["mal"], gr_), Mesh()).ekle(V.ag(cq.Workplane(obj=sh), 0.12, 0.35))   # v7: kasetin kendi sayfasiyla AYNI incelik
                asm.add(sh, name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK["pom"]))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            dx_, dy_, dz_ = (b["x"][0] + b["x"][1]) / 2.0 * MM, b["y"][0] * MM, (b["z"][1] - V.D / 2.0) * MM
            for i_, (ad_, m_, mal_) in enumerate(kaset_etiketleri(V, b, DOKU)):                   # v7: SARI ETIKET montaj modelinde
                parcalar.append(("%s__%s%d" % (b["kod"], ad_, i_), mesh_otele(m_, dx_, dy_, dz_), mal_))
            b["parca"] = len(ps)
        else:
            assert all(abs(q[1]-q[0])>0.01 for q in (b["x"],b["y"],b["z"])), "sifir olculu birim: %s %s" % (b["kod"], (b["x"],b["y"],b["z"]))
            parcalar.append((b["kod"], kutu_ag(b), mal_ad(b))); asm.add(kutu_kat(b), name=b["kod"], color=cq.Color(*RENK.get(b["mal"], RENK["kutu"])))
        b["olcu"] = [round(b["x"][1] - b["x"][0]), round(b["y"][1] - b["y"][0]), round(b["z"][1] - b["z"][0])]
    ye = [a for a, _m, _x in parcalar if "__etiket_yuva_" in a]
    print("YUVA ETIKETI (v23): %d" % len(ye))
    assert len(ye) == 6, "6 yuva etiketi bekleniyordu, %d cikti" % len(ye)
    hp = [a for a, _m, _x in parcalar if a.count("__") == 2]
    print("HAREKETLI PAKET (v17): %d dugum · %s" % (len(hp), " · ".join(sorted({a.rsplit("__", 1)[1] for a in hp}))))
    assert hp, "hicbir hareketli paket ayrilmadi — grup kurali tutmuyor"
    ucgen = sum(len(m.I) // 3 for _a, m, _mal in parcalar)
    print("BIRIM %d  ·  %s  ·  %d ucgen" % (len(B), "  ·  ".join("%s %d" % (k, v) for k, v in sorted(sayac.items())), ucgen))

    # ---- zarf denetimi: hiçbir birim hattın dışına taşmasın; kasetler yuvasında mı ----
    tasan = [b["kod"] for b in B if b["modul"] != "-" and not (-1 <= b["x"][0] and b["x"][1] <= HAT_W + 1 and -1 <= b["y"][0] and b["y"][1] <= H_MAK + 1 and -DZ - 1 <= b["z"][0] and b["z"][1] <= 1)]
    print("ZARF DENETIMI: %s" % ("hepsi hattin icinde (%.0f x %.0f x %.0f)" % (HAT_W, H_MAK, DZ) if not tasan else "TASAN: " + ", ".join(tasan)))
    assert not tasan
    kas = [b for b in B if b["kod"].startswith("KASET_")]
    cak = [(a["kod"], c["kod"]) for i, a in enumerate(kas) for c in kas[i + 1:] if a["x"][0] < c["x"][1] - 0.01 and c["x"][0] < a["x"][1] - 0.01]
    print("KASET YUVALARI: %d yuva · %s" % (len(kas), "yan yana, cakisma yok" if not cak else "CAKISMA: %s" % cak))
    assert not cak
    print("   kaset sirasi: " + " · ".join("%s %.0f–%.0f" % (b["kod"].replace("KASET_", ""), b["x"][0], b["x"][1]) for b in kas))
    print("   derinlik dizilimi: kapak %.0f | kulp %.0f | KASET %.0f | kavrama %.0f | yalitim %.0f | KURU MAKINE %.0f = %.0f mm"
          % (TH.ON_KAPAK, TH.KULP_BOS, TH.KASET_D, TH.KAVRAMA, TH.ARKA_PU, abs(TH.Z_KURU[1] - TH.Z_KURU[0]), DZ))

    # ---- v36 · B CEKMECE MODULU ----
    _bs = [b for b in B if b["durum"] == "GERCEK_STORE"]
    print("B CEKMECE MODULU (store_cad_v2): %d birim · %d parca · %d cekmece" % (len(_bs), sum(b.get("parca", 0) for b in _bs), len(SC.CEK)))
    assert all(b["y"][1] <= H_B + 0.01 for b in _bs), "B tavani 1060'i asiyor"
    # ---- v35 · SUREC KOTU + TABAN HIZASI + CAKISMA ----
    _pp = {p["ad"]: p for p in TC.PARCALAR}
    _cd = _pp["calisma_diski"]["wp"].val().BoundingBox(); _bt = _pp["bant"]["wp"].val().BoundingBox()
    print("SUREC KOTU (CAD'den olculdu): disk ustu %.1f · firin bandi %.1f · kesme plakasi %.1f · kutu tepsisi %.1f · tabla ekseni z %.0f"
          % (H_B + _cd.ymax, H_B + _bt.ymax, PLAKA, TEPSI_Y, ZT))
    assert abs(H_B + _cd.ymax - P) < 0.05, "disk ustu %.2f, beklenen %.2f" % (H_B + _cd.ymax, P)
    assert abs(H_B + _bt.ymax - BANT_UST) < 0.05, "bant ustu %.2f, beklenen %.2f" % (H_B + _bt.ymax, BANT_UST)
    assert P > BANT_UST > PLAKA > TEPSI_Y, "urun yukari basamaga carpar"
    _bk = {b["kod"]: b for b in B}
    for k_ in ("A_KABIN", "TOPPING_MODUL", "D_FIRIN_GOVDE", "K_KABIN"):
        assert abs(_bk[k_]["y"][0] - H_B) < 0.01, "%s tabani %.1f" % (k_, _bk[k_]["y"][0])
    for k_ in ("B_KASA", "D_TABAN_KABIN", "K_TABAN_KABIN"):
        assert abs(_bk[k_]["y"][1] - H_B) < 0.01, "%s ustu %.1f" % (k_, _bk[k_]["y"][1])
    assert tuple(_bk["E_KABIN"]["y"]) == (0.0, H_MAK), "E kesilmemeli"
    assert not [b for b in B if "KUTU YEDE" in b["ad"].upper() or "KUTU_YEDEK" in b["kod"]], "yedek karton kutu hala var"
    print("TABAN HIZASI: A · C · F · K istasyon tabani %.0f · taban dolaplari 0-%.0f · E tek parca 0-%.0f -> GECTI" % (H_B, H_B, H_MAK))
    _ZON = ("D_FIRIN_GOVDE", "E_AGZ")                      # zarf/bolge birimleri: icindekilerle kesismesi dogal
    def _kes(a_, b_):
        return all(a_[i][0] < b_[i][1] - 0.5 and b_[i][0] < a_[i][1] - 0.5 for i in range(3))
    _yeni = [b for b in B if b["modul"] in ("D", "K", "E") and not b["kod"].endswith("_KABIN")]
    _cak = []
    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"] in KAPAK:
            continue
        bb = p["wp"].val().BoundingBox()
        z_ = ((bb.xmin + X_BC, bb.xmax + X_BC), (bb.ymin + H_B, bb.ymax + H_B), (bb.zmin, bb.zmax))
        if z_[0][1] <= X_D:
            continue
        for b in _yeni:
            if _kes(z_, (b["x"], b["y"], b["z"])):
                _cak.append(("TOPPING:" + p["ad"], b["kod"]))
    for i, a_ in enumerate(_yeni):
        for c in _yeni[i + 1:]:
            if a_["kod"] in _ZON or c["kod"] in _ZON:
                continue
            if _kes((a_["x"], a_["y"], a_["z"]), (c["x"], c["y"], c["z"])):
                _cak.append((a_["kod"], c["kod"]))
    print("CAKISMA RAPORU (TOPPING <-> F/K/E ve F/K/E kendi arasinda): %s" % ("YOK" if not _cak else "%d cift" % len(_cak)))
    for a_, c in _cak[:60]:
        print("    %s  <->  %s" % (a_, c))

    # ---- v37 · CEKMECE CALISMA ANIMASYONU: sirayla ac (strok) · bekle · kapa ----
    _sira = ["CEK_K1_hamur_3", "CEK_K2_lahm_4", "CEK_K3_icecek_1", "CEK_K3_lahm_2"]
    _ac = SC.STROK / (127.0 / 60.0 * 3.141592653589793 * SC.KAS_PD)               # 3,3 sn (motor hizi)
    _bek, _ara = 1.5, 0.6
    _adim = _ac + _bek + _ac + _ara
    _T_top = _adim * len(_sira)
    _dz = SC.STROK * MM
    for i_, kod_ in enumerate(_sira):
        t0_ = i_ * _adim
        T = [0.0, t0_, t0_ + _ac, t0_ + _ac + _bek, t0_ + 2 * _ac + _bek, _T_top]
        V = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, _dz), (0.0, 0.0, _dz), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)]
        if t0_ == 0.0:
            T, V = T[1:], V[1:]
        for a_, _m, _x in parcalar:
            if a_.startswith(kod_ + "__") and a_.endswith("__CEKMECE"):
                ANIM.append((a_, T, V))
    print("ANIMASYON: %d cekmece sirayla · acilma %.1f sn · dongu %.1f sn · %d hareketli dugum" % (len(_sira), _ac, _T_top, len(ANIM)))
    assert ANIM, "animasyon icin hareketli dugum bulunamadi"

    # ---- çıktılar ----
    dokular = dict(DOKU); dokular.update({"ad": doku_ad("AUTOKITCH HAT v1", "%.0f × %.0f × %.0f mm  ·  beyaz = gerçek model  ·  şeffaf = henüz kutu" % (HAT_W, H_MAK, DZ), ok_sol=True),
               "montaj": doku_ad("MAKİNE ANA MONTAJI", "birimler tek tek gerçek modele çevriliyor", ok_sol=False)})
    b1 = glb_yaz(os.path.join(OUT, "hat_v37.glb"), parcalar, dokular)
    print("hat_v37.glb · %d birim · %.0f KB" % (len(parcalar), b1 / 1024.0))
    b2, prim, sorun, _u = usdz_yaz([os.path.join(OUT, "hat_v37.usdz")], "hat_v37", parcalar, dokular)
    print("hat_v37.usdz · %.0f KB · %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI"))
    for x in sorun: print("   HATA:", x)
    os.makedirs(STEP, exist_ok=True); asm.save(os.path.join(STEP, "HAT_v37_YERLESIM.step"))
    print("HAT_v37_YERLESIM.step · SolidWorks'te montaj olarak acilir · %s" % STEP)
    # ---- her modul icin AYRI model: istasyon sayfasi kendi modulunu BUYUK gosterir ----
    MODUL_DOSYA = {}
    for mk in ("A", "B", "C", "D", "K", "E", "-"):
        hrf = "R" if mk == "-" else mk
        # KABIN zarfi modul modeline GIRMEZ: saydam da olsa en onde durup icerideki birimin secilmesini engelliyor
        #  (model-viewer materialFromPoint en one carpan malzemeyi verir). Kabin hat modelinde duruyor.
        alt = [(a_, m_, mal_) for (a_, m_, mal_) in parcalar if mal_[1] == hrf and not a_.endswith("_KABIN")]
        if not alt: continue
        dosya = "modul_%s" % hrf
        d1 = glb_yaz(os.path.join(OUT, dosya + ".glb"), alt, dokular)
        d2, _p, _s, _u2 = usdz_yaz([os.path.join(OUT, dosya + ".usdz")], dosya, alt, dokular)
        MODUL_DOSYA[mk] = dosya
        print("   %s.glb %.0f KB · usdz %.0f KB · %d birim" % (dosya, d1 / 1024.0, d2 / 1024.0, len(alt)))

    with io.open(os.path.join(OUT, "durum.json"), "w", encoding="utf-8") as f:
        json.dump(dict(hat=dict(w=HAT_W, h=H_MAK, d=DZ, pafta="HAT_ATOSA_TABLALI_v7 · v37 · B = store_cad_v2 · taban hizasi · surec 1168"), sayac=sayac, modul=[dict(kod=k, ad=a, x=[x, x + w], y=list(MODUL_Y[k])) for k, a, x, w in MODUL],
                       dosya=MODUL_DOSYA, birim=[dict(kod=b["kod"], ad=b["ad"], modul=b["modul"], durum=b["durum"], olcu=b["olcu"], x=list(b["x"]), y=list(b["y"]), z=list(b["z"]), mal=mal_ad(b),
                                   kaynak=b["kaynak"], sayfa=b["sayfa"], parca=b.get("parca", 0)) for b in B]), f, ensure_ascii=False)
    g_ = sum(v for k, v in sayac.items() if k.startswith("GERCEK"))
    print("durum.json yazildi · GERCEK %d / %d birim (%%%.0f) · toplam %.0f sn" % (g_, len(B), 100.0 * g_ / len(B), time.time() - t0))
    sys.stdout.flush(); os._exit(0)
