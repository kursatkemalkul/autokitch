# -*- coding: utf-8 -*-
"""v47 (26 Eyl 2026): KÖŞEDEKİ ÇIKINTILAR (Kemal: "bize bakan köşesinde çıkıntılar, fırının dışına çıkmış parçalar").
  Görsel denetim kaynağı ölçtü: aktarma bandının motoru ön yüzün 78 mm önünde, havada ve 90° ters · ön yan sac + makara uçları
  +10 · fire sileceği +10 → topping_cad_v23 ile hepsi z ≤ 0 (motor bandın arkasında, makarayla eş eksenli). Yer tutucu fırın
  bandı TOPPING tahrik makarasının 30 mm içinden başlıyordu → makaranın 3,5 mm sonrasından. Hamur topu tablada 5,7 mm havada
  duruyordu → oturur (yolculuk_v47). Montaj artık ön yüzü denetler. Açıcı kafası (+167/+180) BİLİNEN açık konu, dokunulmadı.
v46 (26 Eyl 2026): ANİMASYON DÜZELTMESİ (Kemal: "bir şeyler eksen kaçık dönüp duruyor, fırında, TOPPING'de, her yerde").
  Sebep 1: dönen parçalar dünya ağıyla "dönüş + telafi ötelemesi" alıyordu; glTF kareler arasında ötelemeyi doğrusal, dönüşü yay
  boyunca ara değerlediği için parça ekseninden savruluyordu (bant burun makarası 350 mm, koniler 96, valf 94). Artık her dönen
  TOPPING grubu kendi ekseninde duran düğüm (ağ pivota göre yerel). Sebep 2: sabit "tabla_bos_sensoru" adı "tabla" ile başladığı
  için tablanın dönen grubuna düşmüş, 2 m yarıçapla dönüyordu → SABİT. 30 kare/s. Montaj her çalışmada sapmayı ölçer.
v45 (26 Eyl 2026): K KESME + SPREY GERÇEK (kesme_cad_v1: K bandı, Festo DGRF-C kesici + PulsaJet sprey aynı kafada, itici, pano, tereyağı tankı)
· TOPPING v2 = topping_uno_cad_v5 (kama yarık; UNO pistonu/valfi, kaset helezonu/karıştırıcısı AYRI DÜĞÜM — TOPPING simülasyonu bunları çevirir)
· ANA MONTAJA 1 TAM ANİMASYON (Kemal 25 Eyl): bir pizza çekmeceden QR dolabına; istasyon GLB'leri kendi döngüsünü oynatır.
v44 (25 Eyl 2026): ALT KISIM v3 — B store_cad_v5 (tam kaplayan kapaklar, içecek tek kat, K4 depo) · F/K tabanları yeniden · kompresör K tabanı arkasında.
v43 (25 Eyl 2026): TOPPING v4 — kalın PU yalıtım tabanı yerine 3 mm taşıyıcı raf (Kemal: "incecik metal raf olmalı").
v42 (25 Eyl 2026): TOPPING v2 (UNO'lu) · topping_uno_cad_v3 + v22 tabla mekanizması · kompresör K tabanında.
v41 (25 Eyl 2026): kasetler yalnız KAŞAR + KÜP SUCUK · Codex'in Isaac deneyindeki parçaları 3B (STEP) olarak yerinde · diğer 4 kaset şimdilik yok.
v40 (25 Eyl 2026): ALT TABAN ÇİZGİSİ 123 (B store_cad_v4 · E kutu_cad_v3 · F/K taban dolapları) + ana montaj animasyonsuz (animasyon istasyon modellerinde).
v39 (25 Eyl 2026): B = store_cad_v3 — çekmece rayı ÜÇ ELEMANLI teleskop (açık çekmece artık rayda taşınıyor, havada değil).
v38 (25 Eyl 2026): E KUTU KATLAMA = kutu_cad_v2 (11 birim, 830 genişlik, hat 5430) + montajda ortak animasyon (40 sn) · STEP çıktısı yok.
v37 (24 Eyl 2026): B = store_cad_v2 (fitil, yan kayış, standart ürünler) + GLB'de çekmece çalışma animasyonu.
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
ÇIKTI: otonom/hat3d/hat_v45.glb + .usdz  ·  otonom/hat3d/durum.json (sayfa oradan okur)  ·  (v38: SolidWorks STEP'i YAZILMAZ — Kemal 25 Eyl)
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
# v38 · E = kutu_cad_v2: standart 32 × 32 × 4,2 kutunun açılımı 804 × 404 → 700'e sığmıyor, modül 830.
# PAFTA v7'de E hâlâ 700; pafta v8 Kemal'in onayını bekliyor. Model burada ÖNDEN gidiyor (bilerek).
W_E = 830.0
HAT_W = X_E + W_E                                                                        # v38: 5430 (pafta v7: 5300)
HAZNE = _g7["HAZNE"]                                                                     # firin pisirme haznesi 1400
RZ, OMUZ, ERISIM, RX = _g7["RZ"], _g7["OMUZ"], _g7["ERISIM"], _g7["RX"]
QRX, QRZ = _g7["QRX"], _g7["QRZ"]
KOLON, KOL_Y0, K1_TABAN = _g["KOLON"], _g["KOL_Y0"], _g["K1_TABAN"]
import topping_hesap_v6 as TH, topping_cad_v23 as TC                                      # TOPPING modülü: derinlik dizilimi ve yuva konumları ORADAN okunur
KASET_Z = (TH.Z_KASET[1], TH.Z_KASET[0])
T_KAS = (H_B + TC.KAS[0], H_B + TC.KAS[1])        # v35: kaset kotu CAD'den (paftadaki 1627 VARSAYIMDI)

# ---- v35 · SUREC KOTU (Kemal 24 Eyl "B": TOPPING'e dokunma, digerleri tablanin kotuna insin) ----
# Sayilar topping_cad_v22'den; yazildiktan sonra ASAGIDA parcalarin gercek kutusundan OLCULUP assert edilir.
DISK_UST_Y = 108.0                                # calisma_diski ust yuzu (yerel y)
P = H_B + DISK_UST_Y                              # 1168
BANT_UST = H_B + 106.0                            # 1166 · firin bandi ust kosu (CAD AKT_Y: diskin 2 mm alti)
ZT = TH.Z_KASET[0] + 30.0                         # -170 · tabla ekseni (topping_cad_v22 ile ayni formul)
BANT_Z = (ZT - 145.0, ZT + 145.0)                 # 290 genis · TOPPING'deki aktarma bandiyla ayni
BANT_X0 = X_BC + 2195.0 + 35.0                           # CAD'deki aktarma bandinin tahrik silindiri (hat x 2895) -> devam buradan
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
# v41 (Kemal 25 Eyl): YALNIZ Isaac/Codex deneyindeki iki kaset. KIYMA v9 · KUŞBAŞI v8 · HARÇ v4 şimdilik modelde YOK
#      (üreteçleri duruyor, geri almak = bu sözlüğe satırı geri eklemek).
KASET_CAD = {}   # v42: kaşar + sucuk kasetleri TOPPING v2 modelinin (topping_uno_cad_v3) içinde, yeni yerlerinde
YUVA_V1 = [(ad, x1 - x0, (x0 + x1) / 2.0) for ad, x0, x1, gen in TC.YUVA]     # yuva adı, genişlik, merkez (modül yerelinde)
for urun, gw, xc in YUVA_V1:
    xa = X_BC + xc - gw / 2.0; anahtar = urun.split()[0] if urun.startswith("HARÇ") else urun
    cad = KASET_CAD.get(anahtar)
    if not cad:
        continue                                                                         # v41: bu yuva şimdilik boş
    birim("KASET_" + urun.replace(" ", "_"), (cad[1] if cad else "Harç kaseti (KARAR: yap / satın al)"), "C", "GERCEK" if cad else "KUTU",
          (xa + 1.0, xa + gw - 1.0), (T_KAS[0], T_KAS[0] + 360.0), KASET_Z, "pom" if cad else "kutu",
          (cad[0] + ".py") if cad else "modellenmedi · kıyma kaseti macunu pideye YAYAMIYOR, harçta sorun daha ağır (yayıcı kararı)", cad[2] if cad else "")
birim("TOPPING_MODUL", "TOPPING v2 (UNO'lu): 4 UNO çekirdeği (sos · harç · kıyma · kuşbaşı) + kaşar ve küp sucuk kaseti + hava tesisatı · tabla mekanizması v1'den", "C", "GERCEK_MODUL",
      (X_BC, X_BC + W_BC), (H_B, H_B + TC.Y), (-DZ, 0.0), "sac", "topping_uno_cad_v5.py + topping_cad_v23.py", "hat/topping_v2.html")
birim("HAVA_KOMPRESOR", "Kompresör JUN-AIR OF302-15B (yağsız, 15 L, 25 kg) · K tabanı ARKADA (130–640) + Ø10 ana hat · K arkası → F arkası → TOPPING", "K", "GERCEK_HAVA",
      (X_BC + 1800.0, X_BC + 3900.0), (123.0, 1100.0), (-DZ, 0.0), "sac", "topping_uno_cad_v5.py", "hat/topping_v2.html")
# ---- v42 · TOPPING v2 parçaları ----
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location("TU5", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v5.py"))   # v45: kama yarık + dönen gruplar
TU = _ilu.module_from_spec(_sp); _sp.loader.exec_module(TU)
for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))
V1_CIKAN = ("pu_", "ic_kabuk", "bolme", "on_kapak", "kapak_contasi", "dozaj_kovani_", "konum_pimi_", "kovan_", "mil_", "motor_", "reduktor_",
            "soket_", "yay_", "ray_", "yuva_etiketi_", "hava_perdesi", "din_ray", "_bom")


def v1_kalir(ad):
    if ad.startswith(("ray_kirisi", "ray_ortu")): return True
    if ad.startswith("surucu_"): return ad in ("surucu_0", "surucu_1", "surucu_2", "surucu_3")
    if ad == "din_ray_ups": return True
    return not ad.startswith(V1_CIKAN)


V1_TASI = {"sogutma_grubu": (790.0, 0.0, 0.0), "pano_kutusu": (80.0, 0.0, 0.0), "ups": (140.0, 0.0, 0.0), "din_ray_ups": (140.0, 0.0, 0.0),
           "guc_kaynagi": (1196.0, 0.0, 0.0), "fire_silecegi": (520.0, 0.0, 0.0)}
for _i in range(4):
    V1_TASI["surucu_%d" % _i] = (480.0 - 605.0, 1600.0 - 1776.0, -620.0)
V3_CIKAN = ("kabin_", "tabla_diski", "pide", "baglam_", "teknik_bant_", "kompresor_", "hava_ana_hatti")
V3_HAVA = ("kompresor_", "hava_ana_hatti")
KOMP_KAY = (-70.0, -390.0, -385.0)            # v44: kompresör K tabanının önünden (y 520–1030, z −40…−420) arkasına (130–640, −425…−805)
ANA_V44 = [(3530, 646, -765), (3530, 1040, -765), (3530, 1040, -790), (1830, 1040, -790), (1830, 1100, -790), (1675, 1100, -790), (1675, 1250, -740)]

# --- B · ÇEKMECE MODÜLÜ (v36: GERÇEK üretim modeli store_cad_v1 — her çekmece ayrı birim) ---
import store_cad_v5 as SC                                  # v44: tam kaplayan kapaklar + alt kısım v3 dağılımı
Y_ALT = SC.Y_PLINT                                         # v40 · ALT TABAN ÇİZGİSİ: bütün istasyon gövdeleri yerden buradan başlar (123)
SC_OZET = {k: (t, n) for k, t, n, _u, _a in SC.modul()}
_SC_AD = {"B_KASA": "ÇEKMECE modülü gövdesi: sandviç kabuk + PU + 3 kolon bölmesi + ön çerçeve + plint",
          "B_ELEKTRIK": "K4 · Secop'un arkasında pano: Siemens S7-1200 + Mean Well NDR-240-24 + Electromen EM-324C + %d seçici röle" % len(SC.CEK),
          "B_KABLO": "Kablo kanalları 40 × 25: her kolonda dikey + üstte yatay (bölmelerden geçer)",
          "B_SOGUTMA": "Soğutma: Secop CU KLF4.0CND R290 (K4 altı, ızgaralı kapak) + 4 roll-bond evaporatör + ebm-papst fan",
          "B_DEPO": "K4 kaşar + sucuk deposu · kapaklı · +3 °C · 2 gün (GN 1/1-100 kaşar + GN 1/2-100 sucuk) · 4 günün 2. yarısı"}
_TIP_AD = {"hamur": "taze pide", "lahm": "lahmacun", "icecek": "içecek + tatlı · 2 katlı", "ic1": "içecek · tek kat · yaylı itici",
           "ic1d": "içecek · tek kat (dar) · yaylı itici", "tatli": "tatlı · 5 şerit"}
_BIRIM_AD = {"hamur": "top", "lahm": "top", "icecek": "kutu", "ic1": "kutu", "ic1d": "kutu", "tatli": "kap"}
for _kod in dict.fromkeys(p["birim"] for p in SC.PARCALAR):
    _ps = [p for p in SC.PARCALAR if p["birim"] == _kod]
    _bb = [p["wp"].val().BoundingBox() for p in _ps]
    _x = (min(q.xmin for q in _bb), max(q.xmax for q in _bb)); _y = (min(q.ymin for q in _bb), max(q.ymax for q in _bb))
    _z = (min(q.zmin for q in _bb), max(q.zmax for q in _bb))
    if _kod in SC_OZET:
        _t, _n = SC_OZET[_kod]; _kol = _kod.split("_")[1]
        _ad = "%s · %s çekmecesi %s · %d %s · fitilli · Transmotec motor + GT3 kayış · strok %.0f" % (
            _kol, _TIP_AD[_t], _kod.rsplit("_", 1)[1], _n, _BIRIM_AD[_t], SC.STROK)
    else:
        _ad = _SC_AD.get(_kod, _kod)
    birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v5.py", "")

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
birim("D_TABAN_KABIN", "F taban dolabı 123–1060 · önde bulaşık + temizlik + pizza kutusu yedeği · arkada deterjan + robot kontrol + ana pano + UPS", "D", "KUTU", (X_D, X_D + W_D), (Y_ALT, H_B), (-DZ, 0.0), "kabin", "v44 alt kısım v3")
birim("D_SUPURGELIK_KABIN", "F taban dolabı · ayak + süpürgelik 0–123 (60 geride)", "D", "KUTU", (X_D + 30.0, X_D + W_D - 30.0), (0.0, Y_ALT), (-DZ + 30.0, -60.0), "kabin", "v40 alt taban çizgisi 123")
for kod_, ad_, (a_, b_), (y0_, y1_), (z0_, z1_), kat_, kay_ in (
        ("D_BULASIK", "Bulaşık makinesi · MEIKO M-iClean US · 460 × 600 (V) × 700 · sepet 400 × 400 · giriş 315 · önde", (40.0, 500.0), (130.0, 830.0), (-620.0, -20.0), True, "meiko.com M-iClean U teknik veri · derinlik VARSAYIM"),
        ("D_TEMIZLIK", "Temizlik · 2 × 5 L bidon (deterjan / dezenfektan) + üstte bez · eldiven · poşet · önde", (510.0, 656.0), (130.0, 1045.0), (-210.0, -20.0), False, "B'nin K4 nişinden taşındı · bidon 130 × 190 × 290 VARSAYIM"),
        ("D_DETERJAN", "Makine deterjanı + parlatıcı 2 × 5 L · temizliğin arkasında · hortum bulaşık makinesine", (510.0, 656.0), (130.0, 730.0), (-410.0, -220.0), False, "VARSAYIM"),
        ("D_PIZZA_YEDEK", "Pizza kutusu yedeği · 553 kutu düz (804 × 404 × 885 + taban 15) · şarjör 567 + 553 = 1120 = 4 gün · önde", (666.0, 1470.0), (130.0, 1030.0), (-424.0, -20.0), False, "kutu 1,6 mm (kutu_cad_v3) · 1,8 mm olursa 517"),
        ("D_ROBOT_KONTROL", "Robot kontrol kutusu (FR5) · yer: UR sınıfı 475 × 423 × 268 · Fairino kompakt 245 × 180 × 89 · arkada", (666.0, 1141.0), (130.0, 553.0), (-702.0, -434.0), True, "VARSAYIM — Fairino'ya teyit"),
        ("D_ANA_PANO", "Ana pano · PLC · ana şalter · ekran yok (tablet) · arkada, robot kutusunun üstünde", (666.0, 1066.0), (565.0, 915.0), (-684.0, -434.0), False, "400 × 350 × 250 VARSAYIM"),
        ("D_UPS", "UPS APC Back-UPS BX500CI 500 VA · 115 × 213 × 185 · arkada", (1076.0, 1191.0), (565.0, 750.0), (-647.0, -434.0), True, "schneider-electric.com BX500CI")):
    birim(kod_, ad_, "D", "KATALOG" if kat_ else "KUTU", (X_D + a_, X_D + b_), (y0_, y1_), (z0_, z1_), "katalog" if kat_ else "kutu", kay_)
birim("D_FIRIN_GOVDE", "Konveyör fırın gövdesi · özel · elektrikli · taban 1060 · bant altı pay 106 (alt ısıtma: ince rezistans / taş — VARSAYIM)", "D", "KUTU",
      (X_D, X_D + W_D), (H_B, F_G1), (-DZ, 0.0), "sicak", "pafta v7 · gövde tabanı 1040 -> 1060 (taban hizası), bant 1340 -> 1166 (Kemal B)")
birim("D_HAZNE", "Pişirme haznesi 1400 · aynı anda 4 ürün (adım 350) · üst + alt ısıtma", "D", "KUTU",
      (X_D + 50.0, X_D + 50.0 + HAZNE), (H_B + 20.0, BANT_UST + 270.0), (-500.0, -10.0), "sicak", "pafta v7 · ön duvar 10 (bant z -25'e kadar geliyor)")
birim("D_BANT", "Fırın bandı (devamı) · 290 · üst yüz 1166 · TOPPING'deki bıçak burunlu aktarma bandının devamı", "D", "KUTU",
      (BANT_X0, X_K + 15.0), (BANT_UST - 61.5, BANT_UST), BANT_Z, "koyu", "PTFE kaplı cam elyaf örgü · genişlik ve eksen topping_cad_v22'den")
birim("D_DAVLUMBAZ", "Egzoz davlumbazı · fan · yağ + karbon filtre · fırın kartı + SSR + kontaktör", "D", "KUTU", (X_D, X_D + W_D), (F_G1 + 10.0, H_MAK), (-DZ, 0.0), "kutu", "pafta v7")

# --- K · KESME + SPREY (v45: GERÇEK üretim modeli kesme_cad_v1 — işlevsel birimlere ayrılır) ---
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

# --- E · KUTU KATLAMA (TEK PARCA, kesilmez) ---
# --- E · KUTU KATLAMA MODÜLÜ (v38: GERÇEK üretim modeli kutu_cad_v2 — işlevsel birimlere ayrılır) ---
import kutu_cad_v3 as KC                                  # v40: alt taban 123, asansör tahriki tabanın altında
KC.modul()
E_BIRIM = [
    ("E_GOVDE", "KUTU modülü gövdesi: 304 kabuk (saydam) · ayaklar · taban · ağız kirişi · şarjör yan kapısı", ("ayak_", "taban_sac", "plint_on", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "sarjor_yan_kapisi", "on_alt_sac", "on_ust_kapak", "agiz_ust_kirisi", "kose_dikme_")),
    ("E_SARJOR", "Şarjör + asansör: 567 kutu (1,6 mm) · Tr16×4 · 2 HGR15 · NEMA 23 · 2:1 GT3", ("kilavuz_", "sarjor_kapi_esigi", "karton_yigini", "asansor_")),
    ("E_BESLEYICI", "Besleyici itici: en üstteki blankı 411 mm öne sürer · 2 HGR15 · GT3 · NEMA 23", ("besleyici_", "itici_")),
    ("E_KALIP", "Zımba kalıbı + 4 çubuklu tepsi (robot çatalı aralardan) · arka ray · ön tarak · ön ray", ("kalip_", "tepsi_")),
    ("E_KOPRU", "Pizza köprüsü: katlamada 30 mm aşağıda · SFU1605 + NEMA 23 + 2 LM12UU", ("kopru_",)),
    ("E_PISTON", "Piston: 296 × 296 kafa · SFU1610 (üstten BK12) · 2 HGR15 · NEMA 23 · taban / kilit / kapak", ("piston_",)),
    ("E_PARMAK", "Devirme parmağı: iç ön paneli kutuya devirir · NEMA 23 + SureGear 10:1", ("devirme_parmagi", "parmak_")),
    ("E_KAPAK", "Kapak masası + U flap katlayıcı (SFU1605) + kapak kolu (NEMA 23 + SureGear 10:1)", ("kapak_", "flap_katlayici_", "kol_")),
    ("E_ELEKTRIK", "Pano: S7-1200 1214C + SM1221 + SM1222 · 7 × STP-DRV-4830 · Mean Well 24/48 V · sensörler", ("pano_", "din_rayi", "plc_", "guc_", "surucu_", "klemens_", "kablo_kanali", "sensor_")),
    ("E_KUTU", "Pizza kutusu 32 × 32 × 4,2 E-dalga: düz açılım 804 × 404 → katlanır (menteşeli paneller)", ("B_",)),
    ("E_PIZZA", "Pizza Ø300 (K plakasından kutuya kayar)", ("pizza_",)),
]
E_HARIC = ("robot_catal_", "robot_flansi", "REF_K_")          # robotun çatalı (R'nin aleti) ve K referansı montaja girmez
E_PARCA = {k: [] for k, _a, _o in E_BIRIM}
for _p in KC.PARCALAR:
    if _p["ad"].startswith(E_HARIC):
        continue
    for _k, _a, _o in E_BIRIM:
        if _p["ad"].startswith(_o):
            E_PARCA[_k].append(_p); break
    else:
        raise AssertionError("kutu_cad_v3 parcasi birimsiz kaldi: " + _p["ad"])
_W0 = KC.blank_dunya(0.0)
for _k, _a, _o in E_BIRIM:
    _bb = []
    for _p in E_PARCA[_k]:
        if "_kulp" in _p["ad"]:
            continue                                            # kapı tutamakları zarfın 18–22 mm dışına çıkar (tutamak)
        _sh = _p["wp"].val()
        if _p["grup"].startswith("B_"):
            _sh = KC.uygula(_sh, _W0[_p["grup"]])
        _bb.append(_sh.BoundingBox())
    _x = (X_E + min(q.xmin for q in _bb), X_E + max(q.xmax for q in _bb)); _y = (min(q.ymin for q in _bb), max(q.ymax for q in _bb))
    _z = (min(q.zmin for q in _bb), max(q.zmax for q in _bb))
    birim(_k, _a, "E", "GERCEK_KUTU", _x, _y, _z, "sac", "kutu_cad_v3.py", "hat/pack.html")

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


# v41 · Codex'in Isaac deneyinde değiştirdiği parçalar (STEP, kasetin yerel koordinatında) — DÜZELTİLMEDEN alınır
CODEX_3B = {"kasar_cad_v14": {"helezon_B": "kasar_v2/cad/helezon_B_v15.step", "helezon_C": "kasar_v2/cad/helezon_C_v15.step",
                              "helezon_D": "kasar_v2/cad/helezon_D_v15.step", "cikis_tupu": "kasar_v2/cad/cikis_tupu_v15.step"},
            "sucuk_cad_v7": {"helezon_D": "sucuk_v2/cad/helezon_D_v2.step", "cikis_tupu": "sucuk_v2/cad/cikis_tupu_v2.step"}}
CODEX_RAPOR = []


def kaset_parcalari(modul):
    """kasetin BÜTÜN parçaları — kendi sayfasındakiyle birebir aynı model (v5) · v41: Codex parçaları yerine konur."""
    V = importlib.import_module(modul); V.PARCALAR[:] = []; V.kap()
    ps = [p for p in V.PARCALAR if alinir(p["ad"])]
    for ad, yol in CODEX_3B.get(modul, {}).items():
        hedef = [p for p in ps if p["ad"] == ad]
        assert len(hedef) == 1, "%s: %s parcasi bulunamadi" % (modul, ad)
        eski = hedef[0]["wp"].val().BoundingBox()
        yeni_sh = cq.importers.importStep(os.path.join(KOK, "arastirma", "3_TOPPING", yol))
        yeni = yeni_sh.val().BoundingBox()
        # aynı yerel koordinat mı: eksen boyu (z) ve ağırlık bölgesi tutmalı (kanat tur sayısı x/y kutusunu değiştirebilir)
        dz = max(abs(eski.zmin - yeni.zmin), abs(eski.zmax - yeni.zmax))
        assert dz < 3.0, "%s %s: Codex parcasi baska koordinatta (z farki %.1f)" % (modul, ad, dz)
        assert yeni.xmin < eski.xmax and eski.xmin < yeni.xmax and yeni.ymin < eski.ymax and eski.ymin < yeni.ymax, "%s %s: kutular kesismiyor" % (modul, ad)
        hedef[0]["wp"] = yeni_sh
        CODEX_RAPOR.append((modul, ad, yol, (eski.xmin, eski.xmax, eski.ymin, eski.ymax, eski.zmin, eski.zmax), (yeni.xmin, yeni.xmax, yeni.ymin, yeni.ymax, yeni.zmin, yeni.zmax)))
    return V, ps


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
    if ad == "tabla_bos_sensoru": return "SABIT"                 # v46: aktarma ucundaki sabit sensör (adı "tabla" ile başlıyor)
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


ANIM = []                                                                                # v37: (dugum adi, zamanlar, oteleme) · v38: + yol (translation/rotation/scale)
T_HAT = 40.0                                                                             # v38: ortak animasyon dongusu (cekmece turu 34,8 · kutu modulu 2 × 20)
OZEL = []                                                                                # v38: menteşeli düğümler: dict(ad, ebeveyn, T (m), tonlar {malzeme: Mesh (yerel)})


E_MENTESE = ("KOL", "PARMAK")          # dönen makine grupları (kutu panelleri B_* ayrıca)
E_USDZ = []                             # v38: menteşeli düğümlerin t=0 dünya ağları (USDZ durağan kopya)


def e_mentese_dugumleri(b, ps):
    """kutu_cad_v2'nin dönen gruplarını montaj GLB'sine MENTEŞE DÜĞÜMÜ olarak ekler.
    Ağ düğümün menteşesine göre yerel (m); T = menteşe (ebeveyne göre). Kinematik KC'den (tek kaynak)."""
    def pivot(g):
        if g == "KOL": return (KC.KOL_P[0], KC.KOL_P[1], 0.0)
        if g == "PARMAK": return (KC.PARMAK_P[0], KC.PARMAK_P[1], 0.0)
        return KC.DUGUM[g][1]
    gruplar = []
    for p in ps:
        g = p["grup"]
        if (g in E_MENTESE or g.startswith("B_")) and g not in gruplar:
            gruplar.append(g)
    if b["kod"] == "E_KUTU":                                           # karton ağacının tüm düğümleri (boş ara düğüm kalmasın)
        gruplar = list(KC.DUGUM.keys())
    W0 = KC.blank_dunya(0.0)
    for g in gruplar:
        P = pivot(g)
        par = KC.DUGUM[g][0] if g.startswith("B_") else None
        Pp = pivot(par) if par else (-X_E, 0.0, 0.0)                    # kök düğüm dünyada: menteşe + hattaki E ofseti
        tonlar = {}
        for p in ps:
            if p["grup"] != g:
                continue
            m = TC_AG(p["wp"])                                              # E-yerel ağ (m)
            yerel = Mesh(); yerel.P = [(q[0] - P[0] * MM, q[1] - P[1] * MM, q[2] - P[2] * MM) for q in m.P]; yerel.N = list(m.N); yerel.I = list(m.I)
            tonlar.setdefault(mal_ad(b, p["mal"]), Mesh()).ekle(yerel)
            sh = p["wp"].val()
            sh = KC.uygula(sh, W0[g]) if g.startswith("B_") else sh
            E_USDZ.append(("%s__%s__%s_usdz" % (b["kod"], p["mal"], p["ad"]), TC_AG(cq.Workplane(obj=sh.translate(cq.Vector(X_E, 0.0, 0.0)))), mal_ad(b, p["mal"])))
        ad = "%s__%s" % (b["kod"], g)
        ebeveyn = ("E_KUTU__" + par) if par else None
        OZEL.append(dict(ad=ad, ebeveyn=ebeveyn, T=((P[0] - Pp[0]) * MM, (P[1] - Pp[1]) * MM, (P[2] - Pp[2]) * MM), tonlar=tonlar))


def glb_yaz(yol, parcalar, dokular, ozel=None, anim=True, liste=None):
    """animasyonsuz sade GLB (kaset dosyalarındaki yazıcının hat sürümü): yalnız kullanılan malzemeler yazılır"""
    import struct
    ozel = OZEL if ozel is None else ozel
    kullanilan = sorted(set(mal for _a, _m, mal in parcalar) | set(k for o in ozel for k in o["tonlar"])); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]
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
    # v38 · menteşeli düğümler: her biri kendi menteşe noktasında (T), çocukları ebeveyne göre; birden çok malzeme = birden çok primitive
    kok_dugum = list(range(len(nodes)))
    oz_idx = {}
    for o in ozel:
        prims = []
        for k_, m in sorted(o["tonlar"].items()):
            vp = gomu(struct.pack("<%df" % (3 * len(m.P)), *[c for p in m.P for c in p]), 34962)
            vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for nn in m.N for c in nn]), 34962)
            vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
            mn = [min(p[k] for p in m.P) for k in range(3)]; mx = [max(p[k] for p in m.P) for k in range(3)]
            accs.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": mn, "max": mx})
            accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
            accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
            prims.append({"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": kullanilan.index(k_)})
        n_ = {"name": o["ad"], "translation": list(o["T"])}
        if prims:
            meshes.append({"name": o["ad"], "primitives": prims}); n_["mesh"] = len(meshes) - 1
        oz_idx[o["ad"]] = len(nodes); nodes.append(n_)
    for o in ozel:
        if o["ebeveyn"]:
            nodes[oz_idx[o["ebeveyn"]]].setdefault("children", []).append(oz_idx[o["ad"]])
        else:
            kok_dugum.append(oz_idx[o["ad"]])
    anim_sm, anim_ch = [], []                                                            # v37: cekmece · v38: + kutu modulu
    _A = ANIM if liste is None else liste                                              # v45: hat = yolculuk · istasyonlar = kendi döngüleri
    if _A:
        ad2node = {n["name"]: i for i, n in enumerate(nodes)}
        for kayit in _A:
            ad_, T, V = kayit[0], kayit[1], kayit[2]
            yol_ = kayit[3] if len(kayit) > 3 else "translation"
            if ad_ not in ad2node:
                continue
            if not anim:                                                                  # v40 (Kemal): ana montajda animasyon yok — düğüm döngünün başındaki duruşta
                nodes[ad2node[ad_]][yol_] = [float(c) for c in V[0]]
                continue
            nodes[ad2node[ad_]][yol_] = [float(c) for c in V[0]]                           # v45: durağan duruş = ilk kare
            n_el = 4 if yol_ == "rotation" else 3
            vi = gomu(struct.pack("<%df" % len(T), *T))
            accs.append({"bufferView": vi, "componentType": 5126, "count": len(T), "type": "SCALAR", "min": [min(T)], "max": [max(T)]})
            vo = gomu(struct.pack("<%df" % (n_el * len(V)), *[c for v_ in V for c in v_]))
            accs.append({"bufferView": vo, "componentType": 5126, "count": len(V), "type": "VEC4" if n_el == 4 else "VEC3"})
            anim_sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"})
            anim_ch.append({"sampler": len(anim_sm) - 1, "target": {"node": ad2node[ad_], "path": yol_}})
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
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH hat_montaj_v16"}, "scene": 0, "scenes": [{"nodes": kok_dugum}], "nodes": nodes, "meshes": meshes,
         "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}],
         "images": images, "textures": textures, "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}]}
    if anim_ch:
        g["animations"] = [{"name": "hat_calisma", "samplers": anim_sm, "channels": anim_ch}]
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


# ---------------------------------------------------------------- v45 · 1 TAM ANİMASYON: ÜRÜN YOLCULUĞU ----------------------------------------------------------------
# Bu parça hat_montaj_v45.py'ye yap_hat_montaj_v45.py tarafından gömülür (tek başına çalışmaz).
def yolculuk(parcalar):
    """Kemal (25 Eyl): "ürün montajına 1 tam animasyon ekle". Bir PİZZA (sos 80 g · kaşar 100 g · küp sucuk 70 g):
    B çekmecesi → FR5 → açıcı → TOPPING (sos yayıcıda tam 1 tur, kaşar + sucuk spirali) → bant → fırın (HIZLANDIRILMIŞ) →
    K (kesme, çit, itici) → E (kutu) → FR5 → QR dolabı. Her hareket makinenin KENDİ kinematiğinden:
    TOPPING = makine_kodu_v2 sırası + topping_v2_hesap_v1 · K = kesme_cad_v1 · E = kutu_cad_v3 · B = store_cad_v5 stroku."""
    import math
    import topping_v2_hesap_v1 as TH2
    FPS = 30.0                                                        # v46: hızlı dönen makaralar karede ≤ 31°
    OX, OY = X_BC, H_B

    class Iz:
        """zaman → değer: parça parça (s2 = sürücü S-rampası · ss · l doğrusal · h0/h1 hızlanma/yavaşlama · f fonksiyon)"""
        def __init__(s, v0): s.v0 = v0; s.son = v0; s.seg = []
        def git(s, t0, t1, v1, egri="s2"):
            s.seg.append((t0, t1, s.son, v1, egri)); s.son = v1; return t1
        def f(s, t0, t1, fn):
            s.seg.append((t0, t1, None, fn, "f")); s.son = fn(t1); return t1
        def __call__(s, t):
            v = s.v0
            for t0, t1, a, b, e in s.seg:
                if t < t0: return v
                if e == "f":
                    if t < t1: return b(t)
                    v = b(t1); continue
                if t >= t1: v = b; continue
                u = (t - t0) / (t1 - t0)
                if e == "s2": u = 2 * u * u if u < 0.5 else 1 - 2 * (1 - u) * (1 - u)
                elif e == "ss": u = u * u * (3 - 2 * u)
                elif e == "h0": u = u * u
                elif e == "h1": u = 1 - (1 - u) * (1 - u)
                return a + (b - a) * u
            return v

    def gecis(x0, x1): return abs(x1 - x0) / TH2.X_HIZ + TH2.RAMPA_X

    # ================= ZAMAN ÇİZELGESİ =================
    DOZ = TH2.RECETE["pizza"]["doz"]
    SIRA = sorted(DOZ, key=lambda k: [i["x"] for i in TH2.IST if i["kod"] == k][0])
    IS = {i["kod"]: i for i in TH2.IST}
    ADIM = []
    # B + robot + top
    CEK_T = SC.STROK / (127.0 / 60.0 * math.pi * SC.KAS_PD)           # 3,3 s (çekmece motoru)
    CEK = Iz(0.0); CEK.git(0.0, CEK_T, SC.STROK, "l"); CEK.git(5.0, 5.0 + CEK_T, 0.0, "l")
    _rb = [b for b in B if b["kod"] == "ROBOT_1"][0]; RX0 = (_rb["x"][0] + _rb["x"][1]) / 2.0
    _cb = [b for b in B if b["kod"] == "CEK_K1_hamur_3"][0]
    TOP_R, TOP_K = 49.0, 0.82
    _tm = [m_ for a_, m_, _x in parcalar if a_ == "URUN__top"]
    TOP_H = (-min(q[1] for q in _tm[0].P) / MM) if _tm else TOP_R * TOP_K   # v47: topun GERÇEK yarı yüksekliği (ağdan · 34,8)
    top_x, top_y0, top_z0 = (_cb["x"][0] + _cb["x"][1]) / 2.0, _cb["y"][0] + 5.0 + TOP_H, (_cb["z"][0] + _cb["z"][1]) / 2.0
    X_AC = OX + TC.XC_TABLA
    TOPX, TOPY, TOPZ = Iz(top_x), Iz(top_y0), Iz(top_z0)
    TOPZ.f(0.0, CEK_T, lambda t: top_z0 + CEK(t))
    TOPZ.git(CEK_T, 3.5, top_z0 + SC.STROK, "l")
    TOPY.git(3.5, 4.2, 650.0); TOPX.git(4.2, 5.6, X_AC); TOPY.git(4.2, 5.6, 1215.0); TOPZ.git(4.2, 5.6, 150.0)
    TOPZ.git(5.6, 6.4, ZT); TOPY.git(6.4, 6.9, H_B + 108.0 + TOP_H + 0.5, "ss")
    ROB = Iz(RX0); ROB.git(0.3, 3.0, top_x)
    ADIM += [(0.0, "ÇEKMECE", "B'nin hamur çekmecesi açılır (strok %.0f, %.1f s); FR5 rayda çekmecenin önüne gelir." % (SC.STROK, CEK_T)),
             (3.5, "ROBOT", "FR5 hamur topunu alır, açıcının ağzından tablaya bırakır. Top 80 mm yüksek: açıcı kafası bu sırada 90 mm'ye kalkar (60 yetmiyor — AÇIK NOKTA).")]
    # TOPPING
    X = Iz(TC.XC_TABLA); TH = Iz(0.0); KAFA = Iz(1.0); ACMA = Iz(0.0); KONI = Iz(0.0); BANT = Iz(0.0)
    PIS = {k: Iz(0.0) for k in IS if "sil" in IS[k]}; VAL = {k: Iz(0.0) for k in PIS}
    HEL = {k: Iz(0.0) for k in ("KASAR", "SUCUK")}; KAR = {k: Iz(0.0) for k in HEL}
    KAFA.git(5.0, 5.6, 1.5, "ss")                                     # top girerken ek kalkış
    t = 7.2
    KAFA.git(t, t + 0.8, 0.0, "ss"); t += 0.8
    T_ACMA = t
    ACMA.git(t, t + 3.0, 1.0, "l"); KONI.git(t, t + 3.0, 35.0 / math.sin(math.radians(17.82)) * 6.0 * 3.0, "l")
    for k in [k for k in SIRA if k in PIS]:
        PIS[k].git(7.4, 8.2, TH2.uno(k, IS[k]["sil"], DOZ[k])["strok"], "l")
    t += 3.0; KAFA.git(t, t + 0.6, 1.0, "ss"); t += 0.6
    ADIM.append((7.2, "AÇICI", "Konili açıcı iner, topu Ø280'e açar (3 s, tabla kilitli). Bu sırada sos UNO'su emer."))
    REV = []                                                          # (düğüm, zaman) — üst malzeme görünür olur
    TH_SOS = None
    for k in SIRA:
        i = IS[k]; g = DOZ[k]
        if i["tip"] == "YAYICI":
            h = TH2.yayici(k, g)
            t = X.git(t, t + gecis(X.son, i["x"]), i["x"])
            ADIM.append((t - 1.5, k, "Tabla sos yayıcısının altına gelir: borunun iç ucu merkezde. %.0f g = %.1f ml · UNO Ø%.0f pistonu %.1f mm · tabla TAM 1 TUR (%.1f s, %.0f dev/dk) · katman %.2f mm · kama yarık %.1f→%.1f mm."
                         % (g, h["ml"], i["sil"], h["strok"], h["sure"], TH2.RPM_YAYICI, h["katman"], TH2.yarik_genisligi(k, 10.0), TH2.yarik_genisligi(k, 121.0))))
            VAL[k].git(t, t + TH2.VALF_SN, 1.0, "ss"); t += TH2.VALF_SN
            w = 6.0 * TH2.RPM_YAYICI
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h0"); t += TH2.RAMPA_SN
            TH_SOS = (t, TH.son)
            TH.git(t, t + h["sure"], TH.son + 360.0, "l"); PIS[k].git(t, t + h["sure"], 0.0, "l")
            for j in range(6): REV.append(("URUN__sos_%d" % j, t + (j + 0.5) / 6.0 * h["sure"]))
            t += h["sure"]
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h1"); t += TH2.RAMPA_SN + TH2.KESME_VALF_SN
            VAL[k].git(t, t + TH2.VALF_SN, 0.0, "ss")
        else:
            d = TH2.spiral(i, g); x0 = TH2.tabla_x(i, d["r_dis"])
            t = X.git(t, t + gecis(X.son, x0), x0)
            ADIM.append((t - 1.0, k, "%s: %.0f g · tabla %.0f dev/dk, %.2f tur spiral (%.1f s) · ağız r %.0f → %.0f · helezon %.0f dev/dk · katman %.1f mm."
                         % (i["ad"], g, TH2.RPM_NOKTA, d["tur"], d["sure"], d["r_dis"], d["r_ic"], i.get("rpm", 0), d["katman"])))
            w = 6.0 * TH2.RPM_NOKTA
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h0"); t += TH2.RAMPA_SN
            ts = t
            X.f(t, t + d["sure"], lambda tt, ts=ts, d=d, i=i: TH2.tabla_x(i, TH2.r_yasa(d, tt - ts)))
            TH.git(t, t + d["sure"], TH.son + w * d["sure"], "l")
            HEL[k].git(t, t + d["sure"], HEL[k].son + i["rpm"] * 6.0 * d["sure"], "l"); KAR[k].git(t, t + d["sure"], KAR[k].son + 24.0 * d["sure"], "l")
            for j, rm in enumerate((110.0, 80.0, 50.0, 17.5)):
                rm = min(d["r_dis"], max(d["r_ic"], rm))
                REV.append(("URUN__%s_%d" % (k.lower(), j), ts + d["sure"] * (d["r_dis"] ** 2 - rm ** 2) / (d["r_dis"] ** 2 - d["r_ic"] ** 2)))
            t += d["sure"]
            tg = 15.0 / i["rpm"]
            HEL[k].git(t, t + tg, HEL[k].son - 90.0, "l"); TH.git(t, t + tg, TH.son + w * tg, "l"); t += tg
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h1"); t += TH2.RAMPA_SN
    t = X.git(t, t + gecis(X.son, TH2.X_AKTARMA), TH2.X_AKTARMA)
    T_AKT = t
    ADIM.append((T_AKT - 0.5, "AKTARMA", "Tabla sağ uca gider, bıçak burunlu bant ürünü fırın bandına alır; tabla açıcının altına döner."))
    X.git(T_AKT + 0.5, T_AKT + 0.5 + gecis(TH2.X_AKTARMA, TH2.X_PARK), TH2.X_PARK)
    T_F0, T_F1 = T_AKT + 0.5, T_AKT + 10.5
    BANT.git(T_AKT, T_F1, (3940.0 - (OX + TH2.X_AKTARMA)), "l")
    ADIM.append((T_F0, "FIRIN", "Konveyör fırın — animasyonda HIZLANDIRILMIŞ: gerçekte ~4 dk pişer, burada 10 s."))
    T0K = T_F1 - KS.Z_GELIS[0]
    ADIM += [(T0K + KS.Z_GELIS[0], "KESME", "K bandı ürünü fırın bandından alıp kesme merkezine getirir. Kafa iner, 6 dilim keser (bıçak bandın 0,5 mm üstünde durur). Pizzada sprey yok; pidede aynı kafadaki nozül tereyağı püskürtür."),
             (T0K + KS.Z_TASI[0], "ÇİT + İTİCİ", "Bant ürünü 200 mm taşır, 20° çit 36 mm içeri kaydırır (kutu ekseni); itici ürünün üstünden geri gelip arkasına iner."),
             (T0K + KS.Z_ITME[0], "KUTU", "İtici ürünü katlanmış kutuya sürer (1,6 s); ürün tabana düşer, kol + piston kapağı kapatıp bastırır."),
             (T0K + KC.Z_CATAL[0], "ROBOT → QR", "FR5 kutuyu tepsinin aralıklarından çatalla alır, QR teslim dolabına koyar.")]
    ROB.git(T0K + 5.0, T0K + 9.0, X_E + 260.0)
    QR_X = QRX[0] + 15.0 + 240.0; QR_DZ = (QRZ[0] + 220.0) - (KC.ZB + KC.CATAL_DIS + 200.0); QR_DY = 1215.0 - (KC.TEPSI + KC.T + 55.0)   # 1. sütun, 1210 gözü
    TAS = Iz(0.0); TAS.git(T0K + 17.5, T0K + 19.9, 1.0, "s2")
    ROB.git(T0K + 17.5, T0K + 19.9, QR_X); ROB.git(T0K + 20.5, T0K + 24.5, RX0)
    T_J = math.ceil(T0K + 25.5)
    GIZLE = T_J - 0.6
    TT = [i_ / FPS for i_ in range(int(round(T_J * FPS)) + 1)]
    te = lambda t: min(19.5, max(0.0, t - T0K))
    tk = lambda t: min(KS.DONGU, max(0.0, t - T0K))
    tas = lambda t: ((QR_X - (X_E + 260.0)) * TAS(t), QR_DY * TAS(t), QR_DZ * TAS(t))

    # ================= ÜRÜN (düğümler, ürün merkezine göre ağ) =================
    for k_, r_ in (("hamur", (0.93, 0.78, 0.52, 1.0)), ("sos", (0.74, 0.17, 0.10, 1.0)), ("kasar", (0.97, 0.87, 0.50, 1.0)),
                   ("sucuk", (0.55, 0.12, 0.10, 1.0)), ("kesik", (0.30, 0.18, 0.10, 1.0))):
        MALZEME["MU_URUN__" + k_] = dict(renk=r_, met=0.0, ruf=0.8)
    def ekle_u(ad, sh, mal):
        parcalar.append(("URUN__" + ad, TC_AG(sh if isinstance(sh, cq.Workplane) else cq.Workplane(obj=sh)), "MU_URUN__" + mal))
    def halka(r0, r1, y0, y1, a0=None, a1=None, n=48):
        if a0 is None:
            s_ = cq.Workplane("XZ", origin=(0, y0, 0)).circle(r1).extrude(-(y1 - y0))
            return s_.cut(cq.Workplane("XZ", origin=(0, y0 - 1, 0)).circle(r0).extrude(-(y1 - y0 + 2))) if r0 > 0 else s_
        dis = [(r1 * math.cos(math.radians(a0 + (a1 - a0) * j / n)), -r1 * math.sin(math.radians(a0 + (a1 - a0) * j / n))) for j in range(n + 1)]
        ic = [(r0 * math.cos(math.radians(a1 - (a1 - a0) * j / n)), -r0 * math.sin(math.radians(a1 - (a1 - a0) * j / n))) for j in range(n + 1)]
        return cq.Workplane("XZ", origin=(0, y0, 0)).polyline(dis + ic).close().extrude(-(y1 - y0))
    ekle_u("top", cq.Workplane(obj=cq.Solid.makeSphere(TOP_R, angleDegrees1=-90, angleDegrees2=90).scale(1.0)).val().transformGeometry(cq.Matrix([[1, 0, 0, 0], [0, TOP_K, 0, 0], [0, 0, 1, 0]])), "hamur")
    ekle_u("hamur", halka(0.0, 140.0, 0.0, 8.0), "hamur")
    th_s = TH_SOS[1]
    for j in range(6):
        ekle_u("sos_%d" % j, halka(10.0, 125.0, 8.0, 9.5, -th_s - 60.0 * (j + 1), -th_s - 60.0 * j, 24), "sos")
    for j, (r0, r1) in enumerate(((95.0, 125.0), (65.0, 95.0), (35.0, 65.0), (0.0, 35.0))):
        ekle_u("kasar_%d" % j, halka(r0, r1, 9.5, 14.5), "kasar")
    for j, (rr, n) in enumerate(((110.0, 18), (80.0, 13), (50.0, 8), (22.0, 3))):
        kup = None
        for m in range(n):
            a = 2 * math.pi * (m + 0.3 * j) / n
            b_ = cq.Workplane("XY").box(14, 14, 14).translate((rr * math.cos(a), 21.5, -rr * math.sin(a)))
            kup = b_ if kup is None else kup.union(b_)
        ekle_u("sucuk_%d" % j, kup, "sucuk")
    ks_ = None
    for a in (0.0, 60.0, 120.0):
        b_ = cq.Workplane("XY").box(270.0, 1.2, 2.0).translate((0, 15.0, 0)).rotate((0, 0, 0), (0, 1, 0), a)
        ks_ = b_ if ks_ is None else ks_.union(b_)
    ekle_u("kesik", ks_, "kesik")

    def urun_C(t):
        """ürün (hamur alt yüzü merkezi) hatta: tabla → aktarma → fırın → K → kutu → robot → QR"""
        if t < T_AKT:
            return (OX + X(t), OY + 108.0, ZT)
        if t < T_F0:
            u = (t - T_AKT) / (T_F0 - T_AKT); return (OX + TH2.X_AKTARMA + 60.0 * u, OY + 108.0 - 2.0 * u, ZT)
        if t < T_F1:
            u = (t - T_F0) / (T_F1 - T_F0); x0 = OX + TH2.X_AKTARMA + 60.0; return (x0 + (3940.0 - x0) * u, KS.FIRIN_BANDI, ZT)
        tK = t - T0K
        if tK < KC.Z_PIZZA[1]:
            x, y, z = KS.urun_merkez(max(0.0, tK)); return (X_K + x, y, z)
        p = KC.pizza_trs(te(t)); c = tas(t)
        return (X_E + KC.PIZZA_X0 + p[0] + c[0], KC.PLAKA_K + p[1] + c[1], KC.PIZZA_Z0 + p[2] + c[2])
    def qy(d): a = math.radians(d) / 2.0; return (0.0, math.sin(a), 0.0, math.cos(a))
    def qax(ax, d):
        L = math.sqrt(sum(c * c for c in ax)); a = math.radians(d) / 2.0; s_ = math.sin(a) / L
        return (ax[0] * s_, ax[1] * s_, ax[2] * s_, math.cos(a))
    def qrot(q, v):
        x, y, z, w = q; vx, vy, vz = v
        tx, ty, tz = 2 * (y * vz - z * vy), 2 * (z * vx - x * vz), 2 * (x * vy - y * vx)
        return (vx + w * tx + (y * tz - z * ty), vy + w * ty + (z * tx - x * tz), vz + w * tz + (x * ty - y * tx))
    def pivotlu(P, q, ek=(0.0, 0.0, 0.0)):
        r = qrot(q, P); return ((P[0] + ek[0] - r[0]) * MM, (P[1] + ek[1] - r[1]) * MM, (P[2] + ek[2] - r[2]) * MM)
    A = []; KONTROL = []
    def kanal(ad, fn, yol="translation"):
        A.append((ad, TT, [fn(t) for t in TT], yol))
    th_urun = lambda t: TH(min(t, T_AKT))
    vis = lambda a, b: (lambda t: (1.0,) * 3 if a <= t < b else (1e-4,) * 3)
    # top
    kanal("URUN__top", lambda t: (TOPX(t) * MM, (TOPY(t) - TOP_H * ACMA(t)) * MM, TOPZ(t) * MM))   # v47: açılırken alt yüzü diskte
    kanal("URUN__top", lambda t: (1e-4,) * 3 if t >= T_ACMA + 3.0 else (1 + 1.4 * ACMA(t), max(0.02, 1 - ACMA(t)), 1 + 1.4 * ACMA(t)), "scale")
    # hamur + üstü
    u_adlar = ["URUN__hamur"] + ["URUN__sos_%d" % j for j in range(6)] + ["URUN__kasar_%d" % j for j in range(4)] + ["URUN__sucuk_%d" % j for j in range(4)] + ["URUN__kesik"]
    rv = dict(REV)
    _UAG = {}
    for a_, m_, _x in parcalar:
        if a_.startswith("URUN__"): _UAG[a_] = m_
    for ad in u_adlar:
        kanal(ad, lambda t: tuple(c * MM for c in urun_C(t)))
        kanal(ad, lambda t: qy(th_urun(t)), "rotation")
        KONTROL.append((ad, lambda t: tuple(c * MM for c in urun_C(t)), lambda t: qy(th_urun(t)), {"_": _UAG[ad]}))
    kanal("URUN__hamur", lambda t: ((0.18 + 0.82 * ACMA(t)), 1.0, (0.18 + 0.82 * ACMA(t))) if T_ACMA <= t < GIZLE else (1e-4,) * 3, "scale")
    for ad in u_adlar[1:-1]:
        kanal(ad, vis(rv[ad], GIZLE), "scale")
    kanal("URUN__kesik", vis(T0K + KS.Z_KES[0] + 0.3, GIZLE), "scale")
    # TOPPING düğümleri — v46: DÖNEN parçalar KENDİ EKSENİNDE duran ayrı düğüm (ağ pivota göre yerel).
    # v45'te dünya ağına "dönüş + telafi ötelemesi" veriliyordu; kareler arasında öteleme doğrusal, dönüş yay boyunca
    # ara değerlendiği için parça ekseninden kayıyordu (ölçüldü: bant burun makarası 350 mm, koniler 96, sos valfi 94).
    P_T = (OX + TC.XC_TABLA, OY + 108.0, ZT); A_K = (OX + TC.XC_TABLA, OY + 116.0, ZT); ya = math.radians(17.82)
    ROL = {"BANT_BURUN": ((OX + 1815.0, OY + 106.0 - 1.5 - 10.0, 0.0), 10.0), "BANT_TAHRIK": ((OX + 2195.0, OY + 106.0 - 1.5 - 30.0, 0.0), 30.0)}
    DONER = {"TABLA": (P_T, lambda t: (P_T[0] + X(t) - TC.XC_TABLA, P_T[1], P_T[2]), lambda t: qy(TH(t)))}
    for g, yon in (("KONI_ON", 1.0), ("KONI_ARKA", -1.0)):
        ax = (0.0, math.sin(ya), yon * math.cos(ya))
        DONER[g] = (A_K, lambda t: (A_K[0], A_K[1] + 60.0 * KAFA(t), A_K[2]), lambda t, ax=ax, yon=yon: qax(ax, yon * KONI(t)))
    for g, (P_, r_) in ROL.items():
        DONER[g] = (P_, lambda t, P_=P_: P_, lambda t, r_=r_: qax((0, 0, 1), -math.degrees(BANT(t) / r_)))
    for k in VAL:
        g = "VALF_" + k; P_ = (OX + TU.GRUP[g][0], TU.GRUP[g][1], TU.GRUP[g][2])
        DONER[g] = (P_, lambda t, P_=P_: P_, lambda t, k=k: qax((1, 0, 0), -90.0 * VAL[k](t)))
    for k in HEL:
        for on_, Z_ in (("HELEZON_", HEL[k]), ("KARISTIRICI_", KAR[k])):
            g = on_ + k; P_ = (OX + TU.GRUP[g][0], TU.GRUP[g][1], 0.0)
            DONER[g] = (P_, lambda t, P_=P_: P_, lambda t, Z_=Z_: qax((0, 0, 1), -Z_(t)))
    OZEL_T, HARIC = [], set()
    for g, (P_, fT, fR) in DONER.items():
        ton = {}
        for a_, m_, mal_ in parcalar:
            if a_.startswith("TOPPING_MODUL__") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == g:
                y_ = Mesh(); y_.P = [(q[0] - P_[0] * MM, q[1] - P_[1] * MM, q[2] - P_[2] * MM) for q in m_.P]; y_.N = list(m_.N); y_.I = list(m_.I)
                ton.setdefault(mal_, Mesh()).ekle(y_); HARIC.add(a_)
        if not ton:
            continue
        ad = "TOPPING_DONER__" + g
        OZEL_T.append(dict(ad=ad, ebeveyn=None, T=tuple(c * MM for c in fT(0.0)), tonlar=ton))
        kanal(ad, lambda t, fT=fT: tuple(c * MM for c in fT(t)))
        kanal(ad, fR, "rotation")
        KONTROL.append((ad, lambda t, fT=fT: tuple(c * MM for c in fT(t)), fR, ton))
    for ad in sorted({a_ for a_, _m, _x in parcalar if a_.startswith("TOPPING_MODUL__") and a_.count("__") == 2}):
        g = ad.rsplit("__", 1)[1]
        if g == "ARABA":
            kanal(ad, lambda t: ((X(t) - TC.XC_TABLA) * MM, 0.0, 0.0))
        elif g == "ACICI":
            kanal(ad, lambda t: (0.0, 60.0 * KAFA(t) * MM, 0.0))
        elif g.startswith("PISTON_") and g[7:] in PIS:
            k = g[7:]; kanal(ad, lambda t, k=k: (0.0, 0.0, -PIS[k](t) * MM))
    # B çekmecesi + robot
    for a_, _m, _x in parcalar:
        if a_.startswith("CEK_K1_hamur_3__") and a_.endswith("__CEKMECE"):
            kanal(a_, lambda t: (0.0, 0.0, CEK(t) * MM))
        elif a_.startswith("CEK_K1_hamur_3__") and a_.endswith("__CEKMECE_ARA"):
            kanal(a_, lambda t: (0.0, 0.0, CEK(t) * SC.RAY_ARA_ORAN * MM))
        elif a_ in ("ROBOT_1", "ROBOT_1_KOL"):
            kanal(a_, lambda t: ((ROB(t) - RX0) * MM, 0.0, 0.0))
    # K
    for a_, _m, _x in parcalar:
        if a_.startswith("K_") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] in ("KESICI", "ITICI_ARABA", "ITICI_KOL"):
            g_ = a_.rsplit("__", 1)[1]
            kanal(a_, lambda t, g_=g_: tuple(c * MM for c in KS.grup_trs(g_, tk(t))))
    # E (kutu modülü aynı saatte; kendi pizzası gizli — ürün kendi düğümüyle kutuya girer)
    _trs = {"ITICI": lambda t: (0.0, 0.0, KC.itici_dz(t)), "PISTON": lambda t: (0.0, KC.kafa(t) - KC.H_UST, 0.0),
            "KOPRU": lambda t: (0.0, KC.kopru_dy(t), 0.0), "KATLAYICI": lambda t: (0.0, KC.katlayici_dy(t), 0.0)}
    for a_, _m, _x in parcalar:
        if a_.startswith("E_") and a_.count("__") == 2:
            g_ = a_.rsplit("__", 1)[1]
            if g_ in _trs:
                kanal(a_, lambda t, f_=_trs[g_]: tuple(c * MM for c in f_(te(t))))
            elif g_ == "PIZZA":
                kanal(a_, lambda t: (1e-4,) * 3, "scale")
    for o in OZEL:
        g = o["ad"].split("__", 1)[1]
        if g == "KOL":
            kanal(o["ad"], lambda t: KC.quat("z", KC.kol_beta(te(t))), "rotation")
            KONTROL.append((o["ad"], lambda t, T_=o["T"]: T_, lambda t: KC.quat("z", KC.kol_beta(te(t))), o["tonlar"]))
        elif g == "PARMAK":
            kanal(o["ad"], lambda t: KC.quat("z", KC.parmak_psi(te(t))), "rotation")
            KONTROL.append((o["ad"], lambda t, T_=o["T"]: T_, lambda t: KC.quat("z", KC.parmak_psi(te(t))), o["tonlar"]))
        elif g == "B_ROOT":
            T0 = o["T"]
            kanal(o["ad"], lambda t, T0=T0: tuple(T0[j] + (KC.blank_acilar(te(t))[0][j] + tas(t)[j]) * MM for j in range(3)))
            kanal(o["ad"], lambda t: (1e-4,) * 3 if t >= GIZLE else (1.0,) * 3, "scale")
        elif g.startswith("B_"):
            kanal(o["ad"], lambda t, g=g: KC.quat(KC.DUGUM[g][2], KC.blank_acilar(te(t))[1][g]), "rotation")
            KONTROL.append((o["ad"], lambda t, T_=o["T"]: T_, lambda t, g=g: KC.quat(KC.DUGUM[g][2], KC.blank_acilar(te(t))[1][g]), o["tonlar"]))
    ADIM.sort(key=lambda a: a[0])
    # ---- v46 · ÖZ-DENETİM: her dönen düğümün kareler arasında (glTF doğrusal öteleme + slerp) TAM kinematikten sapması ----
    import numpy as _np
    def _qm(q):
        x, y, z, w = q
        return _np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                          [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    def _slerp(a, b, u):
        a = _np.array(a, float); b = _np.array(b, float); d_ = float(_np.dot(a, b))
        if d_ < 0: b = -b; d_ = -d_
        if d_ > 0.99995: r_ = a + u * (b - a); return r_ / _np.linalg.norm(r_)
        th = math.acos(min(1.0, d_)); return (math.sin((1 - u) * th) * a + math.sin(u * th) * b) / math.sin(th)
    RAPOR = []
    for ad, fT, fR, ton in KONTROL:
        pts = []
        for m_ in ton.values():
            P_ = _np.array(m_.P, float); lo, hi = P_.min(0), P_.max(0)
            pts += [(x_, y_, z_) for x_ in (lo[0], hi[0]) for y_ in (lo[1], hi[1]) for z_ in (lo[2], hi[2])]
        pts = _np.array(pts); en, en_t = 0.0, 0.0
        for i in range(len(TT) - 1):
            t0, t1 = TT[i], TT[i + 1]; tm = 0.5 * (t0 + t1)
            qi = _slerp(fR(t0), fR(t1), 0.5); Ti = 0.5 * (_np.array(fT(t0)) + _np.array(fT(t1)))
            e = float(_np.max(_np.linalg.norm((pts @ _qm(qi).T + Ti) - (pts @ _qm(fR(tm)).T + _np.array(fT(tm))), axis=1)))
            if e > en: en, en_t = e, tm
        RAPOR.append((en / MM, en_t, ad))
    RAPOR.sort(key=lambda r: -r[0])
    return A, [dict(t=round(a[0], 2), ad=a[1], not_=a[2]) for a in ADIM], float(T_J), OZEL_T, HARIC, RAPOR


if __name__ == "__main__":
    class _StepYok:                                                                      # v38: SolidWorks montajı YAZILMAZ (Kemal 25 Eyl)
        def add(self, *a, **k): pass
    t0 = time.time(); parcalar, asm, sayac, AG = [], _StepYok(), {}, None
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
            ps = [p for p in TC.PARCALAR if v1_kalir(p["ad"]) and p["ad"] not in KAPAK]
            ton = {}
            for p in ps:
                _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))
                # v26 · KUTU YOK. Kemal sirketteki BILGISAYARDAN bakiyor, telefondan
                # degil — boyut kaygisi yersizdi. Sitedeki makine Isaac'teki ikizle
                # AYNI: satin alinan her parca kendi gercek uretici CAD'iyle ciziliyor,
                # surucu de motor de redüktör de. (v25'te suruculer zarf kutusuydu.)
                # Kaba aglama duruyor: uretici STEP'leri icinde hazir ag tasidigindan
                # BRepTools.Clean'siz tolerans hic islemiyor — TC_AG(kaba=True) onu yapar.
                _kaba = p["ad"].startswith(("surucu_", "motor_", "reduktor_", "x_motoru"))
                ton.setdefault((p["mal"], grup_modul(p["ad"])), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh), _kaba))
                asm.add(sh, name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK.get(p["mal"], RENK["kutu"])))
            _v3 = [q for q in TU.P if not q["ad"].startswith(V3_CIKAN)]
            for q in _v3:
                _kaba = q["ad"].startswith(("motor_", "reduktor_", "kasar_cad", "sucuk_cad"))
                sh = q["sh"].translate(cq.Vector(b["x"][0], 0.0, 0.0))
                _g = q["grup"] if q["grup"].startswith(("PISTON_", "VALF_", "HELEZON_", "KARISTIRICI_")) else "SABIT"   # v45: sim + ana animasyon çevirir
                ton.setdefault((q["mal"], _g), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh), _kaba))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps) + len(_v3)
        elif b["durum"] == "GERCEK_HAVA":
            ton = {}
            _hv = [q for q in TU.P if q["ad"].startswith("kompresor_")]
            for q in _hv:
                ton.setdefault((q["mal"], "SABIT"), Mesh()).ekle(TC_AG(cq.Workplane(obj=q["sh"].translate(cq.Vector(X_BC + KOMP_KAY[0], KOMP_KAY[1], KOMP_KAY[2]))), False))
            _ana = TU.boru(ANA_V44, 5.0)                                        # v44 · yeni güzergâh
            _ana = _ana.val() if hasattr(_ana, "val") else _ana
            ton.setdefault(("hava_ana", "SABIT"), Mesh()).ekle(TC_AG(cq.Workplane(obj=_ana.translate(cq.Vector(X_BC, 0.0, 0.0))), False))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(_hv)
        elif b["durum"] == "GERCEK_KUTU":
            ps = E_PARCA[b["kod"]]
            ton = {}
            for p in ps:
                g = p["grup"]
                kaba = p["ad"].startswith(("surucu_", "guc_")) or p["ad"].endswith(("_motoru", "_reduktoru"))
                if g in E_MENTESE or g.startswith("B_"):
                    continue                                                   # menteşeli düğümler aşağıda (e_mentese_dugumleri)
                sh = p["wp"].val().translate(cq.Vector(X_E, 0.0, 0.0))
                gg = "SABIT" if g in ("SABIT", "ASANSOR") else g
                ton.setdefault((p["mal"], gg), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh), kaba))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            e_mentese_dugumleri(b, ps)
            b["parca"] = len(ps)
        elif b["durum"] == "GERCEK_KESME":
            ps = K_PARCA[b["kod"]]
            ton = {}
            for p in ps:
                kaba = p["ad"].startswith(("surucu_", "guc_", "itici_motoru"))
                sh = p["wp"].val().translate(cq.Vector(X_K, 0.0, 0.0))
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh), kaba))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
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
    assert len(ye) == 0, "v42: yuva etiketi olmamali (yuvalar kalkti)"
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
    assert not kas, "v42: kasetler TOPPING v2 modelinin icinde"
    print("CODEX 3B (v41): %d parca STEP'ten oldugu gibi · eski -> yeni kutu (kasetin yerel mm):" % len(CODEX_RAPOR))
    for m_, a_, y_, e_, n_ in CODEX_RAPOR:
        print("   %-14s %-11s %-38s x %.0f..%.0f y %.0f..%.0f z %.1f..%.1f  ->  x %.0f..%.0f y %.0f..%.0f z %.1f..%.1f" % ((m_, a_, y_) + e_ + n_))
    print("   v42: kaset + UNO denetimi topping_uno_cad_v3 icinde (56 madde)")
    print("   derinlik dizilimi: kapak %.0f | kulp %.0f | KASET %.0f | kavrama %.0f | yalitim %.0f | KURU MAKINE %.0f = %.0f mm"
          % (TH.ON_KAPAK, TH.KULP_BOS, TH.KASET_D, TH.KAVRAMA, TH.ARKA_PU, abs(TH.Z_KURU[1] - TH.Z_KURU[0]), DZ))

    # ---- v36 · B CEKMECE MODULU ----
    _bs = [b for b in B if b["durum"] == "GERCEK_STORE"]
    print("B CEKMECE MODULU (store_cad_v5 · alt taban %.0f · tam kaplama kapaklar): %d birim · %d parca · %d cekmece" % (Y_ALT, len(_bs), sum(b.get("parca", 0) for b in _bs), len(SC.CEK)))
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
    for k_ in ("A_KABIN", "TOPPING_MODUL", "D_FIRIN_GOVDE"):
        assert abs(_bk[k_]["y"][0] - H_B) < 0.01, "%s tabani %.1f" % (k_, _bk[k_]["y"][0])
    for k_ in ("B_KASA", "D_TABAN_KABIN"):
        assert abs(_bk[k_]["y"][1] - H_B) < 0.01, "%s ustu %.1f" % (k_, _bk[k_]["y"][1])
    assert abs(_bk["E_GOVDE"]["y"][0]) < 0.01 and abs(_bk["E_GOVDE"]["y"][1] - H_MAK) < 0.01, "E kesilmemeli (tek parca 0-2030)"
    # v40 · ALT TABAN ÇİZGİSİ: B ve E üreteçleri kendi ölçümünü assert ediyor (gövde altı); burada ikisinin ve dolapların AYNI çizgide olduğu
    assert abs(SC.Y_PLINT - Y_ALT) < 0.01 and abs(KC.Y_PLINT - Y_ALT) < 0.01, "B ve E alt taban cizgisi farkli: %.1f / %.1f" % (SC.Y_PLINT, KC.Y_PLINT)
    for k_ in ("D_TABAN_KABIN",):
        assert abs(_bk[k_]["y"][0] - Y_ALT) < 0.01, "%s alti %.1f" % (k_, _bk[k_]["y"][0])
    assert abs(KS.Y_PLINT - Y_ALT) < 0.01 and abs(KS.H_B - H_B) < 0.01, "K alt taban / istasyon tabani farkli"      # v45: K kendi denetimini yapar
    assert abs(KS.BANT - PLAKA) < 0.01, "K bandi %.1f · plaka %.1f" % (KS.BANT, PLAKA)
    _gb = min(p["wp"].val().BoundingBox().ymin for p in SC.PARCALAR if not p["ad"].startswith(("ayak_", "plint_on")))
    _ge = min(p["wp"].val().BoundingBox().ymin for p in KC.PARCALAR if p["grup"] == "SABIT" and not p["ad"].startswith(("ayak_", "plint_on", "asansor_")))
    assert abs(_gb - Y_ALT) < 0.05 and abs(_ge - Y_ALT) < 0.05, "govde altlari: B %.1f · E %.1f" % (_gb, _ge)
    print("ALT TABAN CIZGISI (v40): B %.1f · E %.1f · F dolabi %.0f · K dolabi %.0f -> ayni cizgi %.0f · altlari ayak + supurgelik · ust taraf 1060 / 1168 / 2030 aynen -> GECTI"
          % (_gb, _ge, _bk["D_TABAN_KABIN"]["y"][0], KS.Y_PLINT, Y_ALT))
    print("E KUTU MODULU (kutu_cad_v3): %d birim · %d parca · %d mentese dugumu · genislik %.0f · hat %.0f"
          % (len([b for b in B if b["durum"] == "GERCEK_KUTU"]), sum(len(v) for v in E_PARCA.values()), len(OZEL), W_E, HAT_W))
    assert not [b for b in B if "KUTU YEDE" in b["ad"].upper() or "KUTU_YEDEK" in b["kod"]], "yedek karton kutu hala var"
    print("TABAN HIZASI: A · C · F · K istasyon tabani %.0f · taban dolaplari 0-%.0f · E tek parca 0-%.0f -> GECTI" % (H_B, H_B, H_MAK))
    _ZON = ("D_FIRIN_GOVDE", "HAVA_KOMPRESOR")                              # zarf/bolge birimleri: icindekilerle kesismesi dogal
    def _kes(a_, b_):
        return all(a_[i][0] < b_[i][1] - 0.5 and b_[i][0] < a_[i][1] - 0.5 for i in range(3))
    _yeni = [b for b in B if b["modul"] in ("D", "K", "E") and not b["kod"].endswith("_KABIN") and b["durum"] not in ("GERCEK_KUTU", "GERCEK_KESME")]   # v45: K kendi taramasını yapar (kesme_cad_v1) · v38: E kendi taramasini yapiyor (kutu_cad_v2: makine 201 an + kutu 46 an + pizza 25 an = 0)
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
    _sira = ["CEK_K1_hamur_3", "CEK_K2_lahm_4", "CEK_K3_ic1_1", "CEK_K4_ic1d_2"]
    _ac = SC.STROK / (127.0 / 60.0 * 3.141592653589793 * SC.KAS_PD)               # 3,3 sn (motor hizi)
    _bek, _ara = 1.5, 0.6
    _adim = _ac + _bek + _ac + _ara
    _T_top = _adim * len(_sira)
    _dz = SC.STROK * MM
    for i_, kod_ in enumerate(_sira):
        t0_ = i_ * _adim
        T = [0.0, t0_, t0_ + _ac, t0_ + _ac + _bek, t0_ + 2 * _ac + _bek, T_HAT]
        V = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, _dz), (0.0, 0.0, _dz), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)]
        if t0_ == 0.0:
            T, V = T[1:], V[1:]
        for a_, _m, _x in parcalar:
            if a_.startswith(kod_ + "__") and a_.endswith("__CEKMECE"):
                ANIM.append((a_, T, V))
            elif a_.startswith(kod_ + "__") and a_.endswith("__CEKMECE_ARA"):            # v39: ray ara elemanı aynı anda yarı yol
                ANIM.append((a_, T, [(x_, y_, z_ * SC.RAY_ARA_ORAN) for x_, y_, z_ in V]))
    print("ANIMASYON: %d cekmece sirayla · acilma %.1f sn · cekmece turu %.1f sn · %d hareketli dugum (%d ara ray)"
          % (len(_sira), _ac, _T_top, len(ANIM), sum(1 for x_ in ANIM if x_[0].endswith("__CEKMECE_ARA"))))
    assert sum(1 for x_ in ANIM if x_[0].endswith("__CEKMECE_ARA")) == len(_sira), "her acilan cekmecenin ara ray dugumu olmali"
    # ---- v38 · KUTU MODULU: kutu_cad_v2 kinematigi (tek kaynak) 40 sn'ye iki tur ornekleniyor ----
    _n = int(round(T_HAT * 15.0)) + 1
    _TT = [min(T_HAT, i_ / 15.0) for i_ in range(_n)]
    def _te(t):
        return t % KC.DONGU
    _mm = lambda v: (v[0] * MM, v[1] * MM, v[2] * MM)
    _trs = {"ITICI": lambda t: (0.0, 0.0, KC.itici_dz(t)), "PISTON": lambda t: (0.0, KC.kafa(t) - KC.H_UST, 0.0),
            "KOPRU": lambda t: (0.0, KC.kopru_dy(t), 0.0), "KATLAYICI": lambda t: (0.0, KC.katlayici_dy(t), 0.0), "PIZZA": KC.pizza_trs}
    _say0 = len(ANIM)
    for a_, _m, _x in parcalar:
        if a_.startswith("E_") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] in _trs:
            f_ = _trs[a_.rsplit("__", 1)[1]]
            ANIM.append((a_, _TT, [_mm(f_(_te(t))) for t in _TT]))
            if a_.endswith("__PIZZA"):
                ANIM.append((a_, _TT, [(max(1e-4, KC.gorunur(_te(t))),) * 3 for t in _TT], "scale"))
    _oz = {o["ad"]: o for o in OZEL}
    for o in OZEL:
        g = o["ad"].split("__", 1)[1]
        if g == "KOL":
            ANIM.append((o["ad"], _TT, [KC.quat("z", KC.kol_beta(_te(t))) for t in _TT], "rotation"))
        elif g == "PARMAK":
            ANIM.append((o["ad"], _TT, [KC.quat("z", KC.parmak_psi(_te(t))) for t in _TT], "rotation"))
        elif g == "B_ROOT":
            T0 = o["T"]
            ANIM.append((o["ad"], _TT, [(T0[0] + KC.blank_acilar(_te(t))[0][0] * MM, T0[1] + KC.blank_acilar(_te(t))[0][1] * MM, T0[2] + KC.blank_acilar(_te(t))[0][2] * MM) for t in _TT]))
            ANIM.append((o["ad"], _TT, [(max(1e-4, KC.gorunur(_te(t))),) * 3 for t in _TT], "scale"))
        elif g.startswith("B_"):
            ANIM.append((o["ad"], _TT, [KC.quat(KC.DUGUM[g][2], KC.blank_acilar(_te(t))[1][g]) for t in _TT], "rotation"))
    print("ANIMASYON (v38): ortak dongu %.0f sn · cekmeceler 1 tur · kutu modulu %d tur · E kanali %d · toplam kanal %d"
          % (T_HAT, int(T_HAT // KC.DONGU), len(ANIM) - _say0, len(ANIM)))
    assert ANIM, "animasyon icin hareketli dugum bulunamadi"
    for a_, _m, _x in parcalar:                                                          # v45: K (modul_K) 2 × 20 sn, E ile aynı saat
        if a_.startswith("K_") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] in ("KESICI", "ITICI_ARABA", "ITICI_KOL"):
            g_ = a_.rsplit("__", 1)[1]
            ANIM.append((a_, _TT, [_mm(KS.grup_trs(g_, _te(t))) for t in _TT]))
    ANIM_HAT, ADIM_HAT, T_J, OZEL_T, HARIC_T, SAPMA = yolculuk(parcalar)
    print("ANA MONTAJ ANIMASYONU (v47): tek tam dongu %.0f sn · %d kanal · %d adim · %d eksenli doner dugum" % (T_J, len(ANIM_HAT), len(ADIM_HAT), len(OZEL_T)))
    print("SAPMA DENETIMI (kareler arasi, glTF ara degerleme <-> tam kinematik): en kotu 15 / %d dugum" % len(SAPMA))
    for e_, t_, a_ in SAPMA[:15]: print("   %8.2f mm  t=%6.2f  %s" % (e_, t_, a_))
    _kotu = [r for r in SAPMA if r[2].startswith("TOPPING_DONER__") and r[0] > 3.0]   # 3 mm: spiral sonundaki x hızı sıçraması (eksen değil)
    assert not _kotu, "TOPPING donen dugumu ekseninden kayiyor: %s" % _kotu[:3]

    # ---- çıktılar ----
    dokular = dict(DOKU); dokular.update({"ad": doku_ad("AUTOKITCH HAT v1", "%.0f × %.0f × %.0f mm  ·  beyaz = gerçek model  ·  şeffaf = henüz kutu" % (HAT_W, H_MAK, DZ), ok_sol=True),
               "montaj": doku_ad("MAKİNE ANA MONTAJI", "birimler tek tek gerçek modele çevriliyor", ok_sol=False)})
    b1 = glb_yaz(os.path.join(OUT, "hat_v47.glb"), [x for x in parcalar if x[0] not in HARIC_T], dokular, ozel=OZEL + OZEL_T, liste=ANIM_HAT)   # v46: donenler kendi ekseninde
    # v47 · ÖN YÜZ DENETİMİ: sabit makine düğümleri makinenin ön yüzünü (z 0) geçemez. İstisna: açıcı kafası (bilinen açık
    # konu), koridordaki robot + ray, QR dolabı, çekmeceler (açılır) ve ürün (taşınır).
    _IST = ("ROBOT", "QR", "CEK_", "URUN__", "TOPPING_DONER__KONI")
    # İşlevsel dış elemanlar (ölçülü izin; fazlası yakalanır): K kapı menteşeleri 20 × 140 × 22 · K acil stop Ø32 × 16 · E kapı kulpu 70 × 18 × 18
    _IZIN = {"K_GOVDE__celik": 22.5, "K_GOVDE__kirmizi": 16.5, "E_GOVDE__celik": 18.5}
    _on = []
    for a_, m_, _x in parcalar:
        if a_.startswith(_IST) or "__ACICI" in a_ or a_ in HARIC_T or not m_.P:
            continue
        zm = max(q[2] for q in m_.P) / MM
        if zm > _IZIN.get(a_, 0.5):
            _on.append((round(zm, 1), a_))
    print("   izinli dis elemanlar (islevsel): K kapi mentesesi +22 · K acil stop +16 · E kapi kulpu +18 · acici kafasi +180 (acik konu)")
    print("ON YUZ DENETIMI (z <= 0,5 mm; acici kafasi haric): %s" % ("GECTI" if not _on else "TASAN: %s" % sorted(_on, reverse=True)[:10]))
    assert not _on, "makinenin on yuzunden tasan parca var"
    print("hat_v47.glb · %d dugum · %.0f KB · animasyon %.0f sn" % (len(parcalar), b1 / 1024.0, T_J))
    _usd = [x for x in parcalar if not x[0].startswith("URUN__")]                         # ürün düğümleri yalnız animasyonda (USDZ durağan)
    b2, prim, sorun, _u = usdz_yaz([os.path.join(OUT, "hat_v47.usdz")], "hat_v47", _usd + E_USDZ, dokular)
    print("hat_v47.usdz · %.0f KB · %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI"))
    for x in sorun: print("   HATA:", x)
    # ---- her modul icin AYRI model: istasyon sayfasi kendi modulunu BUYUK gosterir ----
    MODUL_DOSYA = {}
    for mk in ("A", "B", "C", "D", "K", "E", "-"):
        hrf = "R" if mk == "-" else mk
        # KABIN zarfi modul modeline GIRMEZ: saydam da olsa en onde durup icerideki birimin secilmesini engelliyor
        #  (model-viewer materialFromPoint en one carpan malzemeyi verir). Kabin hat modelinde duruyor.
        alt = [(a_, m_, mal_) for (a_, m_, mal_) in parcalar if mal_[1] == hrf and not a_.endswith("_KABIN") and not a_.startswith("URUN__")]
        if not alt: continue
        dosya = "modul_%s" % hrf
        oz_ = [o for o in OZEL if mk == "E"]
        d1 = glb_yaz(os.path.join(OUT, dosya + ".glb"), alt, dokular, ozel=oz_)
        d2, _p, _s, _u2 = usdz_yaz([os.path.join(OUT, dosya + ".usdz")], dosya, alt + ([x for x in E_USDZ] if mk == "E" else []), dokular)
        MODUL_DOSYA[mk] = dosya
        print("   %s.glb %.0f KB · usdz %.0f KB · %d birim" % (dosya, d1 / 1024.0, d2 / 1024.0, len(alt)))

    with io.open(os.path.join(OUT, "durum.json"), "w", encoding="utf-8") as f:
        json.dump(dict(hat=dict(w=HAT_W, h=H_MAK, d=DZ, pafta="HAT_ATOSA_TABLALI v12 · v47 (on yuzden tasan parcalar iceri, animasyon v46 duzeltmesi) · K = kesme_cad_v1 (gercek) · 1 tam animasyon · alt kisim v3 · B = store_cad_v5 · kompresor K tabani arkasinda · TOPPING v2 UNO'lu (topping_uno_cad_v5) · E = kutu_cad_v3 · alt taban 123 · taban hizasi · surec 1168"), sayac=sayac, animasyon=dict(sure=T_J, adim=ADIM_HAT), modul=[dict(kod=k, ad=a, x=[x, x + w], y=list(MODUL_Y[k])) for k, a, x, w in MODUL],
                       dosya=MODUL_DOSYA, birim=[dict(kod=b["kod"], ad=b["ad"], modul=b["modul"], durum=b["durum"], olcu=b["olcu"], x=list(b["x"]), y=list(b["y"]), z=list(b["z"]), mal=mal_ad(b),
                                   kaynak=b["kaynak"], sayfa=b["sayfa"], parca=b.get("parca", 0)) for b in B]), f, ensure_ascii=False)
    g_ = sum(v for k, v in sayac.items() if k.startswith("GERCEK"))
    print("durum.json yazildi · GERCEK %d / %d birim (%%%.0f) · toplam %.0f sn" % (g_, len(B), 100.0 * g_ / len(B), time.time() - t0))
    sys.stdout.flush(); os._exit(0)
