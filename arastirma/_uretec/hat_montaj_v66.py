# -*- coding: utf-8 -*-
"""v66 (28 Eyl 2026): İKİ LAHMACUN BİR KUTUDA — lahmacun siparişi iki çevrim (kutu açık bekler, 2. lahmacun ilkinin üstüne girer, sonra kapanır) · çıktılar hat_v66.
v65 (28 Eyl 2026): SİPARİŞ ANİMASYONLARI — ana montaj GLB'sinde 6 sipariş (kaşarlı · kıymalı · kuşbaşılı · sucuklu pide · lahmacun · pizza),
  her biri çekmeceden QR gözüne tam yolculuk (Kemal: "simülasyon tuşu olmasın, ana istasyonda sipariş verince gözüksün") · kare sadeleştirme · çıktılar hat_v65.
v64 (28 Eyl 2026): TOPPING DENETİM DÜZELTMELERİ (Kemal: "A yap") — kaset yarık dili (soğuk oda tabanı kapalı) · katlanır flipper + ön köşe pivotlu menteşeler ·
  teknik cep taşıyıcısı · itici alt lama · çıktılar hat_v64.
v63 (28 Eyl 2026): ÖN DÜZLEM +79 · TEMİZ KUTU İSTASYONLAR (SPEC_on_duzlem_v63) — bütün ön yüzler fırın ön yüzü düzleminde (z +79), arka −830 sabit, derinlik 909;
  A gerçek kabin (acici_kabin_cad_v1) · fırın üstü kabin (firin_ust_kabin_cad_v1) · her istasyon kapaklı · bulaşık ayaksız tablada · çıktılar hat_v63.
v62 (27 Eyl 2026 gece): PARÇA ETİKETİ — her parçanın adı + birimi + sınır kutusu parca_kutulari.json'a (sayfada fare etiketi) · çıktılar hat_v62.
v61 (27 Eyl 2026 gece): ÖN KAPAKLAR ŞEFFAF + 180 cm İNSAN FİGÜRÜ + TOPPING yan yalıtımı üstle aynı (topping_uno_cad_v13) · çıktılar hat_v61.
v60 (27 Eyl 2026 gece): TOPPING YALITIMI TAM — yan PU duvarları modele girdi (V3_CIKAN "kabin_" öneki onları da düşürüyordu) +
  topping_uno_cad_v12: soğuk odanın altına alt sac 1 + PU 39 (Kemal: "altına da az da olsa yalıtım yap") · çıktılar hat_v60.
v59 (27 Eyl 2026 gece): SOĞUTMA STANDART DÜZEN — B = store_cad_v7 (Kemal: "öğrendiğin yeter, cooling'de de onlarla yap" · "hamur fırıncıdan soğuk gelemez"):
  Secop CU NLE8.8CN (297 yüksek, K4 ara katman +25) · 6 roll-bond + 7 FNH fan yerine 2 bölge lamelli epoksi kaplı evaporatör + 4 × 4414 FL · bölmelerde
  arka hava geçişi · damlama teknesi → Ø12 gider → plintte kondenser atış kanalı + buharlaştırma tavası · fırın altında PU 60 yerine hava boşluğu +
  parlak paslanmaz ışınım sacı + arka yarıklar · sol yan PU 60. Montajda yalnız B kaynağı + metinler + çıktı adları (hat_v59) değişti.
v58 (27 Eyl 2026 gece): ÖN TARAFLARA KAPAK YOK + DETERJAN YOK (Kemal: "deterjanları makinenin arkasına koyma, tabii şimdilik sil" · "ön taraflara kapak koyma"):
  K = kesme_cad_v5 — bulaşığın arkasındaki kanister rafı + deterjan / parlatıcı bidonları + dozaj hortumları SİLİNDİ, K_DETERJAN birimi kalktı; bulaşık yeri AYNI,
  arkası + MEIKO arka payı BOŞ (denetlenir) · B = store_cad_v6 AYNI (robot çöpü kapağı + klapesi kalır, Kemal) · animasyon: robot topu çekmeceden açıcıya TAŞIR
  (çekmecenin açıcı tarafına park, x 700 konumuna taşır; top–omuz ≤ 779 her karede denetlenir) · E = kutu_cad_v6 — içecek yedeğinin önündeki ön alt sac kalktı →
  6 koli önden açık (önde yalnız sol ön dikme + dikey kablo kanalı; ölçüler kutu_cad_v6.icecek_on_olcum'dan) · sözleşmeye 3 v58 eşitliği · bulaşık denetimi
  deterjansız (bulaşığın arkası + arka pay BOŞ: assert) · birim metinleri (B_COP, E_ICECEK_YEDEK, E_GOVDE, K_GOVDE, K_ELEKTRIK) · çıktılar hat_v58.
v57 (27 Eyl 2026): ALÇAK HAT (Kemal: "bu teknik resme göre 3D modelle" · SPEC_alcak_hat_v57 · ALCAK_HAT_RESIM1_v4 + QR_TEZGAH_v4) — bütün mekanizma 168 aşağı:
  TEK DÜZ ÇİZGİ 788 = çekmeceli dolap üstü = A/C kabin tabanı = fırın gövdesi altı (basamak yok) · A/C mekanizma 892 (kaide 104, kaide_cad_v1) · disk 1000 ·
  fırın bandı 998 · K bandı 996 · E tepsisi 936 · makine üstü 1862 · v56'daki tek H_B (4 anlam) → Y_DUZ 788 + Y_MEK 892 (+ sözleşme assert'leri) ·
  B = store_cad_v6 (tek parça 0–4000 × 123–788, 24 çekmece, fırın altı PU 60 + taşıyıcı, robot çöpü şeridi 3810–4000) · F taban dolabı KALKTI (fırın
  firin_tp10_cad_v7 dolabın üstüne oturur · itici_cad_v4) · K = kesme_cad_v4 (taban 892) + BULAŞIK K altında (KS.BULASIK_YER) + deterjan/parlatıcı ·
  E = kutu_cad_v5 (şarjör 462, içecek yedeği 6 koli E altında) · TOPPING: TC yerel y 892'de, TU dünyada BİR KEZ −168 · hava hattı −168 ·
  YENİ MODÜL S (SERVİS / TESLİM): QR dolabı qr_cad_v1 (860 × 520 × 2050 · 12 göz · robot kontrol + ana pano + UPS içinde) + tezgâh tezgah_cad_v1 ·
  ray ekleri ray_ek_cad_v1 (zincir oluğu · enerji zinciri robot x 2650'de SABİT · robot kablosu · zemin kanalı) · yolculuk: K3 pide çekmecesi → … →
  QR gözü (sütun 1 · satır 3) robot kapağı açılır/kapanır · yeni denetimler: sözleşme, fırın ↔ dolap, kaide ↔ TOPPING/dolap, S + ray ekleri,
  QR erişim tablosu, kapasite, bulaşık K altında.
v56 (27 Eyl 2026): TOPPING yalıtımı YALNIZ SOĞUK HACMİ SARAR (uno v11, teknik cep dışarıda) · yan PU duvarlar görünür · içecek 5 koli F dolabında (fırın üstünden indi)
v55 (27 Eyl 2026): GÖRSEL — yalıtım yarı saydam krem görünür, teknik ayırma saçı mavi, pizza + içecek yığınları opak karton (Kemal: 3D'de göremedim)
v54 (27 Eyl 2026): TOPPING yalıtımı tek dikdörtgen + teknik cep ince saç (topping_uno_cad_v10) · K tank + pano yukarıda, taban boş (kesme_cad_v3) · içecek yedeği fırın üstü sağ 4 koli + dolapta 1 koli · E ayakları alt rafta (kutu_cad_v4) · hava ana hattı yeniden yollandı + denetimi
v53 (27 Eyl 2026): BULAŞIK MAKİNESİ GERÇEK MODEL (bulasik_cad_v1 · MEIKO M-iClean US föyü) — D_BULASIK kutusu yerine 16 parça; kapak açık zarfı ↔ robot denetimi
v52 (27 Eyl 2026): PİZZA KUTUSU YEDEĞİ TEK YERDE fırın üstü sol (320 kutu, 887 = 3,1 gün; dolap pizza gözü boş) + firin_tp10_cad_v6 (raf 4 mm, 10 takoz) + FIRIN KABUĞU GÖRÜNÜR (çıkıntı) + ŞEFFAF İSTASYON YÜZEYLERİ (ön hariç, eşitlik)
v51 (27 Eyl 2026): FIRIN 79 mm ÖNE (Kemal) — firin_tp10_cad_v5 (gövde + konveyör + giriş bandı + ölü plaka +79 z: çıkıntı 1500 × 517 × 79, F modülü 909; K giriş çiti YOK; ürün fırında −170) + itici_cad_v3 (düz itme 170, destek plakası YOK) + topping_uno_cad_v9 (fitil tam) + kesme_cad_v2 (ön kapaklar YOK) · ürün hattı mağazadan kesiciye −170, E −206
v50 (26 Eyl 2026 gece): v49 + itici_cad_v2 (makara/kaldırma pimi −w) + topping_uno_cad_v8 (fitil boşluğu) + yavaş çubuk kalkışı
v49 (26 Eyl 2026 gece): AKTARMA İTİCİSİ (itici_cad_v1: SMC MY1B16-250 çapraz 24,9°, pivotlu çubuk sabit pimle kalkar, destek plakası y 1167) + fırın v4 (havalandırmalı raf) + TOPPING v2 v7 (katalog yay/pim, haç 7,0) · ürün yolu çapraz itme · itici denetimi (ev/son/orta, koridor, disk, itme süpürmesi)
v48 (26 Eyl 2026 gece): F = TP10 kesitli fırın, gövde 1500 (firin_tp10_cad_v3; v2 Kemal kabul) · kompresör fırın üstünde ·
  kutu yedeği 505 + 55 · TOPPING v24 (tekne 2500'de biter) + v2 v6 (kaset yuvaları, kavrama, yalıtım bloğu, fitil) · K değişmez.
v47 (26 Eyl 2026): KÖŞEDEKİ ÇIKINTILAR (Kemal: "bize bakan köşesinde çıkıntılar, fırının dışına çıkmış parçalar").
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
DZ = _g7["DZ"]                                                                           # 830
# ---- v57 · ALÇAK HAT (SPEC_alcak_hat_v57.md · ALCAK_HAT_RESIM1_v4 + QR_TEZGAH_v4) · pafta v7'nin taban 1060 / üst 2030 / B genişliği 2500 değerleri GEÇERSİZ ----
# v56'daki tek taban sabiti (1060) dört ayrı şey demekti (B üstü · A/C kabin tabanı · TOPPING CAD orijini · K istasyon tabanı) → ikiye ayrıldı.
# Toptan yeniden adlandırma parçaları sessizce kaydırırdı (keşif riski 1); her kullanım tek tek Y_DUZ / Y_MEK yapıldı.
DY = -168.0                                   # v56 → v57 bütün mekanizma kotlarının farkı (1060 → 892)
Y_DUZ = 788.0                                 # TEK DÜZ ÇİZGİ: çekmeceli dolap üstü = A/C kabin tabanı = fırın gövdesi altı (basamak yok)
Y_MEK = 892.0                                 # A/C mekanizma tabanı (Y_DUZ + kaide 104) = TOPPING CAD (TC, yerel y) orijini = K istasyon tabanı
H_MAK = 1862.0                                # makine üstü (bütün istasyonlar)
W_B = 4000.0                                  # çekmeceli dolap TEK PARÇA 0–4000
assert abs(Y_MEK - (_g7["H_B"] + DY)) < 0.01 and abs(H_MAK - (_g7["H_MAK"] + DY)) < 0.01, "v57: pafta v7 kotlari + DY tutmuyor"


def _gk(ok):
    """v57 · denetim satırının sonucu (açık PASS / FAIL)"""
    return "GECTI [PASS]" if ok else "KALDI [FAIL]"


X_A, W_A, X_BC, W_BC = _g7["X_A"], _g7["W_A"], _g7["X_C"], _g7["W_C"]                     # A 0-700 · C 700-2500 · v57: W_B yukarıda (4000)
X_D, W_D = _g7["X_F"], _g7["W_F"]                # FIRIN: paftada F, sitede oven.html modul_D'yi yukluyor -> harf D
X_K, W_K, X_E, W_E = _g7["X_K"], _g7["W_K"], _g7["X_E"], _g7["W_E"]
# v38 · E = kutu_cad_v2: standart 32 × 32 × 4,2 kutunun açılımı 804 × 404 → 700'e sığmıyor, modül 830.
# PAFTA v7'de E hâlâ 700; pafta v8 Kemal'in onayını bekliyor. Model burada ÖNDEN gidiyor (bilerek).
W_E = 830.0
HAT_W = X_E + W_E                                                                        # v38: 5430 (pafta v7: 5300)
HAZNE = _g7["HAZNE"]                                                                     # firin pisirme haznesi 1400
RZ, OMUZ, ERISIM, RX = _g7["RZ"], _g7["OMUZ"], _g7["ERISIM"], _g7["RX"]
# v57: QR yeri ve ölçüsü qr_cad_v1'den (pafta v7'deki QR yer tutucusu kalktı) · S modülü (QR + tezgâh) · ray ekleri · A/C kaidesi — hepsi dünya koordinatı
import qr_cad_v1 as QR, tezgah_cad_v1 as TZ, ray_ek_cad_v1 as RE, kaide_cad_v2 as KD
KOLON, KOL_Y0, K1_TABAN = _g["KOLON"], _g["KOL_Y0"], _g["K1_TABAN"]
import topping_hesap_v6 as TH, topping_cad_v25 as TC                                      # v48: tekne 2500'de biter                                      # TOPPING modülü: derinlik dizilimi ve yuva konumları ORADAN okunur
KASET_Z = (TH.Z_KASET[1], TH.Z_KASET[0])
T_KAS = (Y_MEK + TC.KAS[0], Y_MEK + TC.KAS[1])    # v35: kaset kotu CAD'den · v57: Y_MEK (ölü sabit — kaset döngüsü boş)

# ---- v35 · SUREC KOTU (Kemal 24 Eyl "B": TOPPING'e dokunma, digerleri tablanin kotuna insin) ----
# Sayilar topping_cad_v22'den; yazildiktan sonra ASAGIDA parcalarin gercek kutusundan OLCULUP assert edilir.
DISK_UST_Y = 108.0                                # calisma_diski ust yuzu (yerel y)
P = Y_MEK + DISK_UST_Y                            # 1000 (v56: 1168)
BANT_UST = Y_MEK + 106.0                          # 998 · firin bandi ust kosu (CAD AKT_Y: diskin 2 mm alti) · v56: 1166
ZT = TH.Z_KASET[0] + 30.0                         # -170 · tabla ekseni (topping_cad_v22 ile ayni formul)
BANT_Z = (ZT - 145.0, ZT + 145.0)                 # 290 genis · TOPPING'deki aktarma bandiyla ayni
BANT_X0 = X_BC + 2195.0 + 35.0                           # CAD'deki aktarma bandinin tahrik silindiri (hat x 2895) -> devam buradan
PLAKA = BANT_UST - 2.0                            # 996 · kesme plakasi bandin 2 mm ALTINDA: urun hep asagi iner
TEPSI_Y = PLAKA - 60.0                            # 936 · kutu tepsisi yuzu (pafta kurali: surec - 60) -> kutu agzi ~981
E_A0, E_A1 = PLAKA - 90.0, PLAKA + 160.0          # kutulama agzi (pafta: P-90 ... P+160)
F_G1 = BANT_UST + 320.0                           # (ölü) firin govdesi ustu (pafta: bant + 320)
KAIDE = OMUZ - 152.0                              # FR5 taban -> omuz 152 [katalog Fairino FR5 d1]

X_S = TZ.X0 - TZ.TASMA                                   # v57 · S modülü solu = tezgâh tablası (3935) … sağı = QR dolabının sağı = hattın ucu (5430)
MODUL = [("A", "MODÜL A · KONİLİ AÇICI (dolap üstünde · kaide 104)", X_A, W_A), ("B", "MODÜL B · ÇEKMECELİ DOLAP (tek parça 0–4000)", X_A, W_B),
         ("C", "MODÜL C · TOPPING (dolap üstünde · kaide 104)", X_BC, W_BC), ("D", "MODÜL F · KONVEYÖR FIRIN", X_D, W_D),
         ("K", "MODÜL K · KESME + SPREY (+ taban: bulaşık)", X_K, W_K), ("E", "MODÜL E · KUTU KATLAMA (tek parça)", X_E, W_E),
         ("S", "MODÜL S · SERVİS / TESLİM (QR dolabı + tezgâh)", X_S, HAT_W - X_S)]
MODUL_Y = {"A": (Y_DUZ, H_MAK), "B": (0.0, Y_DUZ), "C": (Y_DUZ, H_MAK), "D": (Y_DUZ, H_MAK), "K": (0.0, H_MAK), "E": (0.0, H_MAK), "S": (QR.Y0, QR.Y0 + QR.H)}

# ---------------------------------------------------------------- KÜTÜK ----------------------------------------------------------------
# (kod, ad, modül, durum, x0, x1, y0, y1, z0, z1, malzeme, kaynak/not, sayfa)
B = []
def birim(kod, ad, mod, durum, x, y, z, mal="kutu", kaynak="", sayfa=""):
    B.append(dict(kod=kod, ad=ad, modul=mod, durum=durum, x=x, y=y, z=z, mal=mal, kaynak=kaynak, sayfa=sayfa))



def _dis_birim(M, durum, kaynak, sayfa):
    """v57 · dünya koordinatlı yeni üreteçlerin birimleri (bulasik_cad_v2 sözleşmesi: kur() · PARCALAR · dunya(p) · BIRIMLER · BIRIM_MODUL)"""
    for _k, _a in M.BIRIMLER:
        _bb = [M.dunya(_p).BoundingBox() for _p in M.PARCALAR if _p["birim"] == _k]
        assert _bb, "%s: %s biriminin parcasi yok" % (kaynak, _k)
        birim(_k, _a, M.BIRIM_MODUL[_k], durum, (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
              (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", kaynak, sayfa(_k) if callable(sayfa) else sayfa)


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
FT_ZS_ON = 79.0                                           # v63 · ön düzlem (fırın gövdesinin ön yüzü; FT.ZS ile sözleşmede eşitlenir)
birim("TOPPING_MODUL", "TOPPING v2 (UNO'lu): 4 UNO çekirdeği (sos · harç · kıyma · kuşbaşı) + kaşar ve küp sucuk kaseti + hava tesisatı · tabla mekanizması v1'den", "C", "GERCEK_MODUL",
      (X_BC, X_BC + W_BC), (Y_MEK, Y_MEK + TC.Y), (-DZ, FT_ZS_ON), "sac", "topping_uno_cad_v14.py (dünya y −168) + topping_cad_v25.py (yerel y + 892)", "hat/topping_v2.html")
birim("HAVA_KOMPRESOR", "Kompresör JUN-AIR OF302-15B (yağsız, 15 L, 25 kg) · FIRIN ÜSTÜNDE (havalandırmalı raf 1348, ortam sınırı 40 °C, davlumbaz bölmesinin ön yarısı, kutu yedeğinin yanı — TOPPING'in tek istisnası) · Ø10 ana hat y 1809'da fırın üstünden TOPPING teknik cebine → kuru bölme → şartlandırıcı · K'ye dal (MS4 tepesi 1692 + 10)", "D", "GERCEK_HAVA",
      (3600.0, 3980.0), (1348.0, 1858.0), (-420.0, -40.0), "sac", "topping_uno_cad_v14.py", "hat/topping_v2.html")     # v57: y −168 (raf üstü 1348 · sözleşmede ölçülür)
# ---- v42 · TOPPING v2 parçaları ----
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location("TU11", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v14.py"))   # v56: yalıtım yalnız soğuk hacmi sarar   # v54: yalıtım tek dikdörtgen + teknik ayırma saçı   # v51: fitil tam   # v49: katalog yay/pim, haç 7,0   # v48: kaset yuvaları + yalıtım bloğu + fitil   # v45: kama yarık + dönen gruplar
TU = _ilu.module_from_spec(_sp); _sp.loader.exec_module(TU)
for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))
# v55 · görünürlük: yalıtım yarı saydam krem · ayırma saçı mavi · yedek yığınları karton
MALZEME["yalitim_gorunur"] = dict(renk=(0.95, 0.84, 0.52, 0.38), met=0.0, ruf=0.8, saydam=True)
MALZEME["ayirma_saci"] = dict(renk=(0.18, 0.36, 0.92, 1.0), met=0.3, ruf=0.4, saydam=False)
MALZEME["karton"] = dict(renk=(0.80, 0.64, 0.42, 1.0), met=0.0, ruf=0.85, saydam=False)
for _q in TU.P:
    if _q["ad"] == "yalitim_blogu":
        _q["mal"] = "yalitim_gorunur"
    elif _q["ad"].startswith("teknik_ayirma_saci"):
        _q["mal"] = "ayirma_saci"
    elif _q["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU", "alt_yalitim_PU"):     # v56: yan PU duvarlar da görünür · v60: + alt yalıtım (v12)
        _q["mal"] = "yalitim_gorunur"
# ---- v57 · ALÇAK HAT: TU (topping_uno_cad_v14, DÜNYA y) BİR KEZ −168 kaydırılır — bütün parçalar + dönen grup pivotları (VALF_/PISTON_/HELEZON_/KARISTIRICI_/TABLA).
#      TC (topping_cad_v25, YEREL y) KAYDIRILMAZ: TOPPING_MODUL y0 = Y_MEK ile yerleşir. İkisi karışırsa ya iki kez ya hiç kaymaz (keşif riski 2).
for _q in TU.P:
    _q["sh"] = _q["sh"].translate(cq.Vector(0.0, DY, 0.0))
for _g in list(TU.GRUP):
    if _g != "SABIT":
        TU.GRUP[_g] = (TU.GRUP[_g][0], TU.GRUP[_g][1] + DY, TU.GRUP[_g][2])
TU_YAL_Y0 = TU.YAL_Y0 + DY                                                                # soğuk oda yalıtım altı 1277 → 1109 (aktarma iticisinin kirişi buna bağlanır: IT.TAVAN)
import firin_tp10_cad_v8 as FT                                                          # v57: alçak hat (BANT_UST_HAT 998 · gövde 788–1305 · raf 1348) · v49: havalandırmalı raf
import itici_cad_v5 as IT                                                              # v57: DISK_UST 1000 · TAVAN 1109 · v49: aktarma iticisi (dünya koordinatı)
import bulasik_cad_v2 as BM                                                            # v53: MEIKO M-iClean US gerçek modeli (föy ölçüleri)
for _k, _v in BM.MALZEME.items():
    MALZEME.setdefault(_k, dict(renk=_v["renk"], met=_v["met"], ruf=_v["ruf"], saydam=False))
for _k, _v in IT.MALZEME.items():
    MALZEME.setdefault(_k, dict(renk=_v["renk"], met=_v["met"], ruf=_v["ruf"], saydam=False))
AKTARMA_TP10 = ("bant_burun_silindiri", "bant_tahrik_silindiri", "bant", "bant_tasiyici_saci", "bant_yan_saci_0", "bant_yan_saci_1", "bant_motoru", "bant_ayagi")
YARIK_V2 = FT.kut(*FT.YARIK_V2[0]).cut(FT.kut(*FT.YARIK_V2[1])).val()                          # TOPPING çıkış yarığı çerçevesi v2 (dünya)
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
V3_CIKAN = ("kabin_taban_saci", "kabin_arka_saci", "kabin_ust_saci", "kabin_sag_teknik_sac", "tabla_diski",   # v60: yan PU duvarlar ARTIK girer (eski "kabin_" öneki onları da düşürüyordu)
            "pide", "baglam_", "teknik_bant_", "kompresor_", "hava_ana_hatti")
V3_HAVA = ("kompresor_", "hava_ana_hatti")
KOMP_KAY = (-510.0, 976.0, 0.0)               # v48: kompresör (TU x 3410–3790 · z −40…−420) → fırın üstü raf: dünya x 3600–3980 · v57: TU −168 kaydırıldığı için AYNI kalır → y 1348–1844 (raf üstü 1348)
ANA_V44 = [(3090, 1977, -380), (3090, 1977, -432), (1640, 1977, -432), (1640, 1977, -740), (1640, 1335, -740), (1650, 1335, -740)]   # v56: teknik cepte 1977 düz (zarflar 1731,5–1971,5)   # v54: yığınların arkası (z −432) · TOPPING teknik cebinden   # v48: fırın üstü → TOPPING rakoru (dünya 2500, y 2000, z −415) → teknik cep → kuru bölme → şartlandırıcı sol yüzü
ANA_K48 = [(3090, 1977, -432), (3090, 1977, -780), (3385, 1977, -780), (3385, 1870, -780)]   # v54: K şartlandırıcısının (MS4) tepesine · köşe dikmesinin (z −798) önünden   # v48: K'ye dal — K besleme hattının tepesine (dünya x 4160, y 1700, z −795)

# v57 · hava ana hattı TOPPING / fırın / K ile birlikte RİJİT −168: teknik cep 1977 → 1809 · fırın üstü 1335 → 1167 · K dalı ucu 1870 → 1702 (MS4 tepesi 1692 + 10, sözleşmede ölçülür)
ANA_V44 = [(x_, y_ + DY, z_) for x_, y_, z_ in ANA_V44]
ANA_K48 = [(x_, y_ + DY, z_) for x_, y_, z_ in ANA_K48]

# --- B · ÇEKMECE MODÜLÜ (v36: GERÇEK üretim modeli store_cad_v1 — her çekmece ayrı birim) ---
import store_cad_v8 as SC                                  # v57: TEK PARÇA çekmeceli dolap 0–4000 × 123–788 (24 çekmece · fırın altı PU 60 + taşıyıcı · robot çöpü şeridi) · v44: tam kaplayan kapaklar
Y_ALT = SC.Y_PLINT                                         # v40 · ALT TABAN ÇİZGİSİ: bütün istasyon gövdeleri yerden buradan başlar (123)
SC_OZET = {k: (t, n) for k, t, n, _u, _a in SC.modul()}
_SC_AD = {"B_KASA": "ÇEKMECELİ DOLAP gövdesi (tek parça, +3 °C): sandviç kabuk + PU + 6 bölme · 0–4000 × 123–788 · ön çerçeve + plint · sol yan PU 60 · fırın altında HAVA BOŞLUKLU ısı kalkanı (v59: PU yok — ayırma sacı 728 + parlak paslanmaz ışınım sacı 740 + arka 6 yarık · fırın kirişlere oturur)",
          "B_ELEKTRIK": "K4 · Secop'un arkasında pano: Siemens S7-1200 + Mean Well NDR-240-24 + Electromen EM-324C + %d seçici röle" % len(SC.CEK),
          "B_KABLO": "Kablo kanalları 40 × 25: her kolonda dikey + yatay (K1→K4 703–728 · K4→K6 643–668, bölmelerden geçer)",
          "B_SOGUTMA": "Soğutma (v59 standart düzen · sogutma_hesabi_v1): Secop CU NLE8.8CN R290 688 W @ −10/32 °C (gereken 552–661 W) K4 altında ızgaralı kapak arkasında · 2 bölge lamelli epoksi kaplı evaporatör (sol K2 arkası → K1–K3 · sağ K5 arkası → K4 depo + K5–K6) + davlumbaz + 4 × ebm-papst 4414 FL · bölmelerde arka hava geçişleri · damlama teknesi → Ø12 gider → plintte kondenser atış kanalı + buharlaştırma tavası",
          "B_DEPO": "K4 kaşar + sucuk deposu · kapaklı · +3 °C · 2 gün (GN 1/1-100 kaşar + GN 1/2-100 sucuk) · 4 günün 2. yarısı",
          "B_TASIYICI": "Fırın taşıyıcı çerçevesi 304: 2 kiriş 40 × 40 × 2 (y 746,5–786,5) + 3 çapraz + 6 dikme (bölmelerin içinde, altlarında ayak) · fırın 200 kg + raf 99 kg (VARSAYIM)",
          "B_COP": "ROBOT ÇÖPÜ şeridi 3810–4000 (soğuk DEĞİL, 3810'da yalıtımlı ara duvar): 15 L kova 165 × 300 × 400 (poşetli, kızaklı) · atma boşluğu · ön yüzde 130 × 130 yaylı klape (y 610–740, menteşe 748)"}
_TIP_AD = {"hamur": "taze pide", "lahm": "lahmacun", "icecek": "içecek + tatlı · 2 katlı", "ic1": "içecek · tek kat · yaylı itici",
           "ic1d": "içecek · tek kat (dar) · yaylı itici", "tatli": "tatlı · 2 şerit"}
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
    birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v8.py", "")

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
# v63: A_KABIN KUTU yer tutucusu kalktı → acici_kabin_cad_v1 (A_GOVDE + A_ONYUZ, aşağıda KD.kur() sonrası)
# ---- v57 · A + C MEKANİZMA KAİDESİ 104 (kaide_cad_v2, dünya): dolap üstü 788 → mekanizma tabanı 892 · A: açıcı kolonu + tekne sacı 892–893,5 · C: TOPPING dis_taban ----
KD.kur()
_dis_birim(KD, "GERCEK_KAIDE", "kaide_cad_v2.py", lambda k_: "hat/press.html" if KD.BIRIM_MODUL[k_] == "A" else "hat/topping_v2.html")
import acici_kabin_cad_v1 as AK                                                         # v63: A gerçek kabin (dünya · 304 1,5 · ön tava 20 · robot ağzı · ışık perdesi)
AK.kur()
_dis_birim(AK, "GERCEK_ACICI", "acici_kabin_cad_v1.py", "hat/press.html")

# ============================ v57 · ALÇAK HAT (v35 TABAN HIZASI'nın yerine) ============================
# Kemal 27 Eyl (ALCAK_HAT_RESIM1_v4): TEK DÜZ ÇİZGİ 788 — çekmeceli dolabın üstü = A/C kabin tabanı = fırın gövdesinin altı (basamak yok).
# A/C mekanizmaları kaide 104 üstünde (892) · K istasyon tabanı 892 · E (kutu katlama) KESİLMEZ: yerden 1862'ye tek parça.
# SÜREÇ: disk 1000 > fırın bandı 998 > kesme plakası 996 > kutu ağzı ~981 — ürün hep aşağı iner.
# F TABAN DOLABI KALKTI (yeri dolabın K5, K6 ve şeridi) · temizlik → tezgâh · deterjan → K altı · robot kontrol / ana pano / UPS → QR dolabı · içecek yedeği → E altı.

# --- D · (paftada F) KONVEYOR FIRIN · fırın üstü raf (1305–1348) ---
PIZZA_UST_KUTU = 320                                                                     # fırın üstü raftaki pizza kutusu yedeği (kural 5.5)
import firin_ust_kabin_cad_v1 as FU                                                     # v63: fırın üstü kabin (yanlar + üst + tek parça arka + düşer kapaklar) + davlumbaz sac kutusu + kompresör tavası
FU.kur()
_dis_birim(FU, "GERCEK_FIRIN_UST", "firin_ust_kabin_cad_v1.py", "hat/oven.html")
birim("D_PIZZA_YEDEK_UST", "Pizza kutusu yedeği · TEK YER: fırın üstü SOL, rafta %d kutu düz (804 × 404 × 512) · E şarjörü 462 + %d = 782 ≈ 2,8 gün (SPEC · şarjörün kullanılabilir kısmı ≈ 432 → 752, karar Kemal'de) (Kemal 27 Eyl: sola koy)" % (PIZZA_UST_KUTU, PIZZA_UST_KUTU), "D", "KUTU",
      (X_D + 20.0, X_D + 824.0), (FT.UST_RAF_Y[1], FT.UST_RAF_Y[1] + 512.0), (-424.0, -20.0), "karton", "v48 · kural 5.5 · v57 raf 1348")
FT.kur(ayak=False, plaka=False, uyarla=True)
for _p63 in FT.PARCALAR:                                                               # v63: fırın ön kabuğu ön saclarla aynı ton (SPEC: tek ön malzeme)
    if _p63["ad"] == "govde_kabugu": _p63["mal"] = "sac"
for _k, _a in FT.BIRIMLER:
    _bb = [FT.dunya(_p).BoundingBox() for _p in FT.PARCALAR if _p["birim"] == _k]
    birim(_k, _a, "D", "GERCEK_FIRIN", (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "firin_tp10_cad_v8.py", "hat/oven.html")
# ---- v49 · AKTARMA İTİCİSİ + DESTEK PLAKASI (modül C, dünya koordinatı; ev konumu, çubuk kalkık) ----
IT.kur(IT.S_HOME, True)
for _k, _a in IT.BIRIMLER:
    _bb = [IT.dunya(_p).BoundingBox() for _p in IT.PARCALAR if _p["birim"] == _k]
    birim(_k, _a, "C", "GERCEK_ITICI", (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "itici_cad_v5.py", "hat/oven.html#itici")

# --- K · KESME + SPREY (v45: GERÇEK üretim modeli kesme_cad_v1 — işlevsel birimlere ayrılır) ---
import kesme_cad_v6 as KS                                  # v58: deterjan + parlatıcı kanisterleri, rafı ve dozaj hortumları KALKTI (Kemal: "şimdilik sil") · kutu_cad_v7'yı içe alır · v57: alçak hat (taban 892, bant 996, üst 1862) + bulaşık yeri · v54: tank + pano yukarıda
KS.modul()
K_BIRIM = [
    ("K_GOVDE", "KESME istasyonu gövdesi: 304 kabuk · ayaklar · taban 123 · istasyon tabanı 892 (v57) · v63: 3 kapak (alt bulaşık · orta · üst, tava 20, ön düzlem +79) + ön çerçeve",
     ("ayak_", "taban_sac", "plint_on", "istasyon_tabani", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "kose_dikmesi", "taban_kapisi", "ust_kapi", "kapi_kilidi", "acil_stop",
      "onyuz_", "bulasik_")),   # v63: ön çerçeve + 3 kapak (tava 20) + bulaşık tablası / geçiş lastikleri
    ("K_BANT", "K bandı: gıda PU bant 400 · Interroll RollerDrive EC5000 Ø50 · 6 mm kayma tablası (kesim yükünü taşır) · 20° kılavuz çit · ölü plaka",
     ("bant_", "kayma_tablasi", "tabla_kirisi", "tahrik_rulosu", "kuyruk_rulosu", "olu_plaka", "cit_")),
    ("K_KESICI", "Kesici + sprey kafası: Festo DGRF-C-63-125 · yıldız bıçak Ø296 × 6 · koruma halkası · PulsaJet + TG nozül yıldızın göbeğinde",
     ("kopru_kirisi", "silindir_baglanti", "DGRF", "ara_dikme", "kafa_plakasi", "bicak_", "koruma_", "kelebek_", "PulsaJet", "sprey_dirsegi", "UniJet", "sprey_ucu", "isitmali_hortum_kafa")),
    ("K_YAG", "Tereyağı sistemi: ısıtmalı basınçlı tank 3 L (2 gün 1,41 L) · regülatör · seviye sensörü · ısıtmalı hortum", ("yag_", "isitmali_hortum_", "hava_hortumu_tank")),
    ("K_ITICI", "İtici: igus ZLW-1040 eksen + NEMA 23 · SMC MGPM20-60 kaldırma · kol + POM yüz (E'ye 110 mm girer)",
     ("ZLW", "itici_", "eksen_ayagi", "kaldirma_", "MGPM", "itme_cubugu")),
    ("K_ELEKTRIK", "Pano (arka duvarda, üstte · K tabanının altında yalnız bulaşık — v58: deterjan kalktı): S7-1200 · STP-DRV-4830 · NDR-240 · PNOZ · PWM sprey sürücüsü · şartlandırıcı + valf adası · sensörler",
     ("pano_", "din_rayi", "plc_", "emniyet_", "PWMD", "sicaklik", "guc_", "surucu_", "klemens", "kablo_kanali", "sartlandirici", "valf_adasi", "hava_besleme",
      "hava_hortumu_", "sensor_", "kesici_reed")),
    # v58: K_DETERJAN birimi kalktı — kesme_cad_v6'te "deterjan_" parçası yok (Kemal: "deterjanları makinenin arkasına koyma, tabii şimdilik sil")
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
        raise AssertionError("kesme_cad_v6 parcasi birimsiz kaldi: " + _p["ad"])
for _k, _a, _o in K_BIRIM:
    _bb = [q["wp"].val().BoundingBox() for q in K_PARCA[_k] if not q["ad"].endswith("_kulp") and q["ad"] != "acil_stop"]
    birim(_k, _a, "K", "GERCEK_KESME", (X_K + min(q.xmin for q in _bb), X_K + max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "kesme_cad_v6.py", "hat/kesme.html")

# ---- v57 · BULAŞIK MAKİNESİ K ALTINDA (bulasik_cad_v2 gerçek model · yer kesme_cad_v6'ten (v4 ile aynı) KS.BULASIK_YER = (4108,5 · 126 · −20) — denetçi düzeltmesi: makine z −645…−12) ----
# KS.modul() BM'yi kendi içinde kurar ama BM.X0/Y0/Z0 ve PARCALAR'ı geri koyar (denetçi doğruladı) → burada, KS'den SONRA kendi yerine kurulur.
BM.X0, BM.Y0, BM.Z0 = KS.BULASIK_YER
BM.kur()
BM_KOD = {"K_BULASIK": "D_BULASIK"}                                                      # montaj kodu → bulasik_cad_v2 birim kodu · site malzemeden seçer: MK_K_BULASIK
for _k, _a in BM.BIRIMLER:
    _kk = [k_ for k_, v_ in BM_KOD.items() if v_ == _k][0]
    _bb = [BM.dunya(_p).BoundingBox() for _p in BM.PARCALAR if _p["birim"] == _k]
    birim(_kk, "K altında (ön dikmelerin arasında, sağ ön dikmeye yaslı) · " + _a, "K", "GERCEK_BULASIK", (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),
          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "bulasik_cad_v2.py", "hat/kesme.html")

# --- E · KUTU KATLAMA (TEK PARCA, kesilmez) ---
# --- E · KUTU KATLAMA MODÜLÜ (v38: GERÇEK üretim modeli kutu_cad_v2 — işlevsel birimlere ayrılır) ---
import kutu_cad_v7 as KC                                  # v58: içecek yedeğinin ÖNÜ AÇIK (ön alt sac kalktı · Kemal: ön taraflara kapak yok) · v57: alçak hat (tepsi 936, alt raf 618–622, şarjör 462) + içecek yedeği 6 koli · v54: kalıp ayakları alt rafta
KC.modul()
_ION = KC.icecek_on_olcum()                                   # v58: içecek yedeğinin önü (kutu_cad_v7 katılardan ölçer: öndeki engeller · net açıklık · sütunların düz çekme yolu)
assert _ION["on"] == [] and not _ION["sutun"][0]["engel"] and not _ION["sutun"][1]["engel"], "v63: icecek yedeginin onunde (kapak acikken) engel var: %s" % _ION
E_BIRIM = [
    ("E_GOVDE", "KUTU modülü gövdesi: 304 kabuk (saydam) · ayaklar · taban · ağız kirişi · şarjör yan kapısı · üst ön kapak · alt önü AÇIK (v58: ön alt sac kalktı)", ("ayak_", "taban_sac", "plint_on", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "sarjor_yan_kapisi", "on_ust_kapak", "agiz_ust_kirisi", "kose_dikme_", "onyuz_")),   # v63: ön çerçeve + kapaklar
    ("E_SARJOR", "Şarjör + asansör: 462 kutu (1,6 mm · yığın 240–980; kullanılabilir ≈ 432: asansör somunu 935'te durur, v4'ten miras — karar Kemal'de) · Tr16×4 · 2 HGR15 · NEMA 23 · 2:1 GT3", ("kilavuz_", "sarjor_kapi_esigi", "karton_yigini", "asansor_")),
    ("E_BESLEYICI", "Besleyici itici: en üstteki blankı 411 mm öne sürer · 2 HGR15 · GT3 · NEMA 23", ("besleyici_", "itici_")),
    ("E_KALIP", "Zımba kalıbı + 4 çubuklu tepsi (robot çatalı aralardan) · arka ray · ön tarak · ön ray", ("kalip_", "tepsi_")),
    ("E_KOPRU", "Pizza köprüsü: katlamada 30 mm aşağıda · SFU1605 + NEMA 23 + 2 LM12UU", ("kopru_",)),
    ("E_PISTON", "Piston: 296 × 296 kafa · SFU1610 (üstten BK12) · 2 HGR15 · NEMA 23 · taban / kilit / kapak", ("piston_",)),
    ("E_PARMAK", "Devirme parmağı: iç ön paneli kutuya devirir · NEMA 23 + SureGear 10:1", ("devirme_parmagi", "parmak_")),
    ("E_KAPAK", "Kapak masası + U flap katlayıcı (SFU1605) + kapak kolu (NEMA 23 + SureGear 10:1)", ("kapak_", "flap_katlayici_", "kol_")),
    ("E_ELEKTRIK", "Pano: S7-1200 1214C + SM1221 + SM1222 · 7 × STP-DRV-4830 · Mean Well 24/48 V · sensörler", ("pano_", "din_rayi", "plc_", "guc_", "surucu_", "klemens_", "kablo_kanali", "sensor_")),
    ("E_KUTU", "Pizza kutusu 32 × 32 × 4,2 E-dalga: düz açılım 804 × 404 → katlanır (menteşeli paneller)", ("B_",)),
    ("E_PIZZA", "Pizza Ø300 (K plakasından kutuya kayar)", ("pizza_",)),
    ("E_ICECEK_YEDEK", "İçecek yedeği 6 koli (2 sütun × 3 kat · koli 400 × 267 × 123 · 24 kutu) = 144 · E altı önde, soğutmasız · dolaptaki 144 + 144 = 288 (4 gün 277) · ÖNÜ AÇIK (v58 · Kemal: ön taraflara kapak yok — ön alt sac kalktı) · önde yalnız sol ön dikme + dikey kablo kanalı, net açıklık %.1f: tek koli düz geçer; dikme sol sütunun önüne %.1f mm, kanal sağ sütunun önüne %.1f mm yandan biner → koli yana kaydırılıp çekilir"
     % (_ION["net"][1] - _ION["net"][0], _ION["sutun"][0]["bindirme"], _ION["sutun"][1]["bindirme"]), ("icecek_",)),
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
        raise AssertionError("kutu_cad_v7 parcasi birimsiz kaldi: " + _p["ad"])
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
    birim(_k, _a, "E", "GERCEK_KUTU", _x, _y, _z, "sac", "kutu_cad_v7.py", "hat/pack.html")

# --- ROBOT (tek FR5, yer rayinda) + QR DOLABI (hattin onunde, z > 0) ---
birim("ROBOT_RAY", "Yer rayı · tek araba · x 200–5100", "-", "KATALOG", (200.0, 5100.0), (0.0, 60.0), (RZ - 120.0, RZ + 120.0), "katalog", "pafta v7")
birim("ROBOT_1", "Fairino FR5 · tek robot (pafta konumu x %.0f)" % RX, "-", "KATALOG", (RX - 90.0, RX + 90.0), (60.0, KAIDE), (RZ - 90.0, RZ + 90.0), "robot", "katalog · kaide + araba")
birim("ROBOT_1_KOL", "FR5 omuz + kol zarfı (erişim %.0f)" % ERISIM, "-", "KATALOG", (RX - 120.0, RX + 120.0), (KAIDE, OMUZ + 180.0), (RZ - 120.0, RZ + 120.0), "robot", "yalnız ZARF · gerçek kol modeli yok")
# ---- v57 · yeni üreteçlerin (kaide · ray ekleri · QR · tezgâh) malzemeleri — store_cad_v8 / kesme_cad_v6 / kutu_cad_v7'dan SONRA kaydedilir:
#      montajda önce olan ad kendi rengini korur (ortak adlar: plastik · sensor · poset — önce kaydedilince dolap / E / K parçalarının rengi değişiyordu, inceleme)
for _M in (KD, RE, QR, TZ):
    for _k, _v in _M.MALZEME.items():
        MALZEME.setdefault(_k, dict(renk=_v["renk"], met=_v["met"], ruf=_v["ruf"], saydam=_v.get("saydam", False)))
# ---- v57 · RAY EKLERİ (ray_ek_cad_v1, modül "-"): zincir oluğu · enerji zinciri (yalnız robot x 2650 için modellendi → animasyonda SABİT) · robot kablosu 4 + 11 m · zemin kanalı ----
RE.kur()
_dis_birim(RE, "GERCEK_RAY", "ray_ek_cad_v1.py", "hat/robot.html")
# ---- v57 · MODÜL S · SERVİS / TESLİM (koridorun karşısında): QR teslim dolabı (qr_cad_v1) + personel tezgâhı (tezgah_cad_v1) ----
# pafta v7 QR yer tutucusu (x 4295–5300, z 900–1340) ve F dolabındaki robot kontrol / ana pano / UPS / temizlik kalktı → hepsi burada.
# DİKKAT (denetçi): QR.X0/Y0/Z0 DEĞİŞTİRİLMEZ — ray_ek_cad_v1 kablo yolunu import anında onlardan hesaplıyor.
QR.kur()
_dis_birim(QR, "GERCEK_QR", "qr_cad_v1.py", "hat/service.html")
TZ.kur()
_dis_birim(TZ, "GERCEK_TEZGAH", "tezgah_cad_v1.py", "hat/service.html")
# ---- v61 · ÖN KAPAKLAR ŞEFFAF (Kemal: "ön kapakları şeffaf yap, çekmeceleri de") — yalnız görünüm, parça ve denetim aynı
import re as _re61
MALZEME["on_seffaf"] = dict(renk=(0.70, 0.82, 0.95, 0.16), met=0.1, ruf=0.15, saydam=True)
ON_SEFFAF = _re61.compile(r"^(onyuz_|CEK_K\d_[a-z0-9]+_\d+_on_(dis_sac|pu|ic_sac|fitil)|k4_kapak_|k4_izgara_|serit_on_|klape_levhasi$|servis_kapagi_|"
                          r"musteri_(alt|ust)_panel$|goz_\d\d_musteri_kapisi$|on_kapak$|cekmece_onu$|on_ust_kapak$|sarjor_yan_kapisi$)")
_ON61 = {}
for _ad61, _L61 in (("B", SC.PARCALAR), ("QR", QR.PARCALAR), ("TEZGAH", TZ.PARCALAR), ("E", KC.PARCALAR), ("K", KS.PARCALAR), ("A", AK.PARCALAR), ("D", FU.PARCALAR), ("BULASIK", BM.PARCALAR), ("TU", TU.P)):
    for _p61 in _L61:
        if ON_SEFFAF.match(_p61["ad"]):
            _p61["mal"] = "on_seffaf"; _ON61[_ad61] = _ON61.get(_ad61, 0) + 1
print("v61 · ON KAPAKLAR SEFFAF (yalniz gorunum): " + " · ".join("%s %d parca" % kv for kv in sorted(_ON61.items())))
assert all(_ON61.get(k_, 0) > 0 for k_ in ("B", "QR", "TEZGAH", "E")), _ON61
GERCEK_DIS = {"GERCEK_QR": QR, "GERCEK_TEZGAH": TZ, "GERCEK_RAY": RE, "GERCEK_KAIDE": KD, "GERCEK_ACICI": AK, "GERCEK_FIRIN_UST": FU}   # v63: + A kabini + fırın üstü kabin      # dünya koordinatlı yeni üreteçler (bulasik_cad_v2 sözleşmesi)

# ---- v57 · YOLCULUK SEÇİMLERİ (store_cad_v8 ve qr_cad_v1'de VAR olmalı — aşağıda denetlenir) ----
SIPARIS = [("kasarli", "Kaşarlı pide", "CEK_K3_hamur_3"), ("kiymali", "Kıymalı pide", "CEK_K3_hamur_3"), ("kusbasili", "Kuşbaşılı pide", "CEK_K3_hamur_3"),
           ("sucuklu", "Sucuklu pide", "CEK_K3_hamur_3"), ("lahmacun", "Lahmacun", "CEK_K2_lahm_6"), ("pizza", "Pizza", "CEK_K3_hamur_3")]   # v65: kod (RECETE) · ad · çekmece
CEK_TUM = sorted(set(c_ for _k, _a, c_ in SIPARIS))
YOL_CEKMECE = "CEK_K3_hamur_3"                                                           # FR5'in hamur topunu aldığı çekmece (K3 pide · açıklık 398,5–473,5)
ISTASYON_SIRA = ("CEK_K3_hamur_3", "CEK_K1_lahm_4", "CEK_K6_ic1_1", "CEK_K5_tatli_1")     # modul_B döngüsü: K3 pide · K1 lahmacun · K6 içecek · K5 tatlı
QR_SUTUN, QR_SATIR = 0, 2                                                                # yolculuğun gözü: sütun 1 (x 4600–4980) · satır 3 (taban 850)
QR_PAY = 20.0                                                                            # çatal çekişi sonunda kutunun QR robot yüzüne payı (mm)
QR_YOL = {}
YOL_ZAMAN = {}                                                                           # v66: yolculuk() son çevrimin zamanları (T0K, T_J, FPS)
L2_ADLAR = ["hamur"] + ["harc_%d" % j for j in range(6)] + ["kesik"]                         # v66: 2. lahmacunun düğümleri (URUN__L2_*)                                                                              # yolculuk() doldurur: kutunun QR yolu + kapak açıklığı (__main__'de GÖZ YOLU denetimi)


def qr_hedef(sutun=None, satir=None):
    """v57 · kutunun QR gözündeki hedefi (dünya) — qr_cad_v1 parçalarından ÖLÇÜLÜR (v56'daki sabit 1215 ve pafta v7 QR kutusu kalktı).
    x: robot kapağının ortası (kapak motoru ağzın sol üst köşesinde → göz ortasından sağda) · y: göz tabanı (alüminyum ısı yayıcı) üstü ·
    z: kutu göz arkasına 5 mm kala (qr_cad_v1 'kapak kapanırken kutuya çarpmaz' denetimiyle aynı VARSAYIM) · kutunun çataldaki yeri kutu_cad_v7'dan (catal_kutu)."""
    sutun = QR_SUTUN if sutun is None else sutun; satir = QR_SATIR if satir is None else satir
    g_ = "%d%d" % (satir, sutun)
    def _bb(ad):
        q_ = [p for p in QR.PARCALAR if p["ad"] == ad]
        assert len(q_) == 1, "qr_cad_v1: %s yok" % ad
        return QR.dunya(q_[0]).BoundingBox()
    kp, tp, ks = _bb("goz_%s_robot_kapagi" % g_), _bb("goz_%s_taban_plakasi" % g_), _bb("goz_%s_kasasi" % g_)
    xk, zk = (KC.BX1 - KC.BX0) / 2.0, (KC.BZ1 - KC.BZ0) / 2.0                          # kutu yarı ölçüleri (320 × 320)
    hk = max(KC.H_YAN, KC.H_ON, KC.H_ARKA)                                              # katlanmış kutunun yüksekliği (en yüksek duvar)
    ck = KC.catal_kutu(KC.Z_CATAL[3] + 1.0)                                             # çatal kaldırıp çektikten sonra kutunun ötelemesi (dy, dz) · kutu_cad_v7: dz 900
    cek_z = KC.ZB + ck[1]                                                                # çatal çekişi sonunda kutu ekseni (E'nin kendi kinematiği: 694)
    bekle_z = min(cek_z, QR.Z0 - QR_PAY - zk)                                           # v57: QR robot yüzü artık z 670 → kutu yüzün QR_PAY önünde bekler (gövdeye girmez)
    kx, ky, kz = (kp.xmin + kp.xmax) / 2.0, tp.ymax, ks.zmax - 1.0 - 5.0 - zk
    gk_ = "GOZ_%s_KAPAK" % g_
    pv = QR.MENTESE[gk_][0]
    R_ = math.hypot(QR.KAPAK_MIL_Y - 6.0, 5.0)                                          # robot kapağının süpürme yarıçapı (qr_cad_v1 denetimi)
    h_ = pv[1] - (ky + hk)
    zmin = pv[2] + math.sqrt(max(0.0, R_ ** 2 - h_ ** 2))                               # kapak kapanırken kutunun robot yüzü bundan geride olmalı
    return dict(sutun=sutun, satir=satir, grup=gk_, mentese=QR.MENTESE[gk_], robot_x=QR.ROBOT_X, kx=kx, ky=ky, kz=kz, yari=zk, hk=hk,
                kutu_x=(kx - xk, kx + xk), kapak_x=(kp.xmin, kp.xmax), zmin=zmin, goz_ust=ks.ymax, cek_z=cek_z, bekle_z=bekle_z,
                geri=bekle_z - cek_z, dx=kx - (X_E + (KC.BX0 + KC.BX1) / 2.0), dy=ky - (KC.TEPSI + ck[0]), dz=kz - bekle_z)


# ============================ v57 · ALÇAK HAT SÖZLEŞMESİ: üreteçler arası kot eşitlikleri (model KURULMADAN önce; biri tutmazsa durur) ============================
_bk0 = {b["kod"]: b for b in B}
_ms4 = [p for p in KS.PARCALAR if p["ad"] == "sartlandirici_MS4"]
assert len(_ms4) == 1, "kesme_cad_v6: sartlandirici_MS4 parcasi yok"
_ms4_ust = _ms4[0]["wp"].val().BoundingBox().ymax
_komp_alt = min(q["sh"].BoundingBox().ymin for q in TU.P if q["ad"].startswith("kompresor_")) + KOMP_KAY[1]
SOZLESME = [
    ("disk: FT.DISK_UST = IT.DISK_UST = Y_MEK + 108 = P = 1000", (FT.DISK_UST, IT.DISK_UST, Y_MEK + DISK_UST_Y, P, 1000.0)),
    ("v56 disk 1168 + DY = P", (1168.0 + DY, P)),
    ("firin bandi: FT.BANT_UST_HAT = KS.FIRIN_BANDI = BANT_UST = 998", (FT.BANT_UST_HAT, KS.FIRIN_BANDI, BANT_UST, 998.0)),
    ("K bandi: FT.K_BANT = KS.BANT = KC.PLAKA_K = PLAKA = 996", (FT.K_BANT, KS.BANT, KC.PLAKA_K, PLAKA, 996.0)),
    ("E tepsisi: KC.TEPSI = TEPSI_Y = 936", (KC.TEPSI, TEPSI_Y, 936.0)),
    ("K istasyon tabani: KS.H_B = Y_MEK = 892", (KS.H_B, Y_MEK, 892.0)),
    ("duz cizgi: SC.H_B = FT.YG0 = KD.Y_DUZ = Y_DUZ = 788", (SC.H_B, FT.YG0, KD.Y_DUZ, Y_DUZ, 788.0)),
    ("mekanizma tabani: KD.Y_MEK = Y_MEK = Y_DUZ + KD.KAIDE_H (104)", (KD.Y_MEK, Y_MEK, Y_DUZ + KD.KAIDE_H)),
    ("makine ustu: KS.H = KC.H = Y_MEK + TC.Y = H_MAK = 1862", (KS.H, KC.H, Y_MEK + TC.Y, H_MAK, 1862.0)),
    ("dolap: SC.W_B = W_B = 4000", (SC.W_B, W_B, 4000.0)),
    ("itici tavani: TU yalitim alti (YAL_Y0 + DY) = IT.TAVAN = 1109", (TU_YAL_Y0, IT.TAVAN, 1109.0)),
    ("alt taban: SC.Y_PLINT = KS.Y_PLINT = KC.Y_PLINT = 123", (SC.Y_PLINT, KS.Y_PLINT, KC.Y_PLINT, 123.0)),
    ("K>E penceresi: KS.E_PENCERE = KC.PENCERE (4 deger, en buyuk fark)", (max(abs(a_ - b_) for a_, b_ in zip(KS.E_PENCERE, KC.PENCERE)), 0.0)),
    ("F>K agzi: KS.URUN_GIRISI y (932-1072) firin bandini (998) icerir (1 = evet)", (float(KS.URUN_GIRISI[0] < BANT_UST < KS.URUN_GIRISI[1]), 1.0)),
    ("hava K dali: ANA_K48 ucu = MS4 ustu + 10 = 1702", (ANA_K48[-1][1], _ms4_ust + 10.0, 1702.0)),
    ("kompresor alti = firin ustu raf ustu = HAVA_KOMPRESOR y0 = 1348", (_komp_alt, FT.UST_RAF_Y[1], _bk0["HAVA_KOMPRESOR"]["y"][0], 1348.0)),
    ("pizza yedegi alti = firin ustu raf ustu", (_bk0["D_PIZZA_YEDEK_UST"]["y"][0], FT.UST_RAF_Y[1])),
    # v63: davlumbaz artık firin_ust_kabin_cad_v1 (F_DAVLUMBAZ, köşebentleri 1275'ten) — kendi denetimi üreteçte
    ("bulasik x: BM.X0 = KS.BULASIK_YER", (BM.X0, KS.BULASIK_YER[0], 4108.5)),
    ("bulasik y: BM.Y0 = KS.BULASIK_YER (v63: ayaksız, tabla üstü 139)", (BM.Y0, KS.BULASIK_YER[1], 139.0)),
    ("bulasik z: BM.Z0 = KS.BULASIK_YER (denetci: -20)", (BM.Z0, KS.BULASIK_YER[2], -20.0)),
    ("robot rayi: QR.RZ = RE.RZ = pafta RZ = 360", (QR.RZ, RE.RZ, RZ, 360.0)),
    ("robot omzu: QR.OMUZ = pafta OMUZ = 970", (QR.OMUZ, OMUZ, 970.0)),
    ("robot erisimi: QR.ERISIM = pafta ERISIM = 779", (QR.ERISIM, ERISIM, 779.0)),
    ("S modulu sag ucu: QR.X0 + QR.W = HAT_W = 5430", (QR.X0 + QR.W, HAT_W, 5430.0)),
    ("E sarjoru: KC.SARJOR_ADET = 462", (float(KC.SARJOR_ADET), 462.0)),
    ("E icecek yedegi: KC.ICECEK_YEDEK kutu = 144", (float(KC.ICECEK_YEDEK["kutu"]), 144.0)),
    ("v58 · K deterjan_ parcasi = 0 (kesme_cad_v6 · Kemal: simdilik sil)", (float(len([p for p in KS.PARCALAR if p["ad"].startswith("deterjan_")])), 0.0)),
    ("v63 · on duzlem: SC / KS / KC / TC / TU / AK / FU Z_ON = FT.ZS = 79", (SC.Z_ON, KS.Z_ON, KC.Z_ON, TC.Z_ON, TU.Z_ON, AK.Z_ON, FU.Z_ON, FT.ZS, FT_ZS_ON, 79.0)),
    ("v58 · B_COP robot copu kapagi + klapesi yerinde (v63: store_cad_v8 13 parca)", (float(len([p for p in SC.PARCALAR if p["birim"] == "B_COP"])), 13.0)),
    ("v60 · TOPPING yalitimi modelde: yan PU 2 + alt sac + alt PU = 4 (topping_uno_cad_v14)", (float(len([q for q in TU.P if q["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU", "alt_yalitim_PU", "alt_yalitim_saci") and not q["ad"].startswith(V3_CIKAN)])), 4.0)),
    ("v59 · B lamelli evaporator + 4414 FL fan = 2 + 4 (store_cad_v8 · sogutma standart duzen)", (float(len([p for p in SC.PARCALAR if p["ad"] in ("evaporator_sol_lamel", "evaporator_sag_lamel")])
      + len([p for p in SC.PARCALAR if p["ad"] in ("fan_sol_1", "fan_sol_2", "fan_sag_1", "fan_sag_2")])), 6.0)),
    ("v58 · E on_alt_sac parcasi = 0 (kutu_cad_v7 · icecek yedeginin onu acik)", (float(len([p for p in KC.PARCALAR if p["ad"] == "on_alt_sac"])), 0.0)),
]
print("ALCAK HAT SOZLESMESI (v66 · %d esitlik · DY %.0f · Y_DUZ %.0f · Y_MEK %.0f · H_MAK %.0f):" % (len(SOZLESME), DY, Y_DUZ, Y_MEK, H_MAK))
_soz_kal = []
for _ad, _v in SOZLESME:
    _ok = max(_v) - min(_v) < 0.01
    print("   %-72s %-34s %s" % (_ad, " = ".join("%g" % v_ for v_ in _v), _gk(_ok)))
    if not _ok: _soz_kal.append(_ad)
assert not _soz_kal, "v57 alcak hat sozlesmesi tutmuyor: %s" % _soz_kal
_cek_kod = {c[1] for c in SC.CEK}
_yok = [k_ for k_ in (YOL_CEKMECE,) + tuple(ISTASYON_SIRA) if k_ not in _cek_kod]
print("   yolculuk + istasyon cekmeceleri store_cad_v8'da (%s): %s" % (", ".join((YOL_CEKMECE,) + tuple(ISTASYON_SIRA)), _gk(not _yok)))
assert not _yok, "v57: store_cad_v8'da olmayan cekmece: %s" % _yok
# ---- KAPASİTE (SPEC · 2 gün kuralı): üreteçlerin kendi sayımından ----
_kap = {}
for _t, _n in SC_OZET.values():
    _kap[_t] = _kap.get(_t, 0) + _n
KAPASITE = [("pide (dolap K3 + K5)", _kap.get("hamur", 0), 160, "2 gun 160"), ("lahmacun (K1 + K2)", _kap.get("lahm", 0), 432, "2 gun 400"),
            ("icecek (dolap K6)", _kap.get("ic1", 0), 144, "2 gun 139"), ("tatli (K5 ust cekmece)", _kap.get("tatli", 0), 12, "2 gun 11"),
            ("icecek yedegi (E alti 6 koli)", KC.ICECEK_YEDEK["kutu"], 144, "dolap + yedek 288 · 4 gun 277"),
            ("pizza kutusu (E sarjoru)", KC.SARJOR_ADET, 462, "+ firin ustu %d = %d · kullanilabilir ≈ 432 + %d = %d (asansor somunu 935'te durur, v4'ten miras, karar Kemal'de)"
             % (PIZZA_UST_KUTU, 462 + PIZZA_UST_KUTU, PIZZA_UST_KUTU, 432 + PIZZA_UST_KUTU))]
print("KAPASITE (v57 · SPEC):")
for _ad, _v, _h, _not in KAPASITE:
    print("   %-32s %4d (beklenen %d · %s)  %s" % (_ad, _v, _h, _not, _gk(_v == _h)))
assert all(_v == _h for _a, _v, _h, _n in KAPASITE), "v57: kapasite SPEC ile tutmuyor"
# ---- QR ERİŞİM TABLOSU (qr_cad_v1.erisim_tablosu) + yolculuğun gözü ----
_et = QR.erisim_tablosu()
print("QR ERISIM (qr_cad_v1 · robot x %.0f · omuz y %.0f · ray ekseni z %.0f · robot yuzu z %.0f · pratik erisim %.0f · bilek = goz tabani + %.0f VARSAYIM):"
      % (QR.ROBOT_X, QR.OMUZ, QR.RZ, QR.Z0, QR.ERISIM, QR.BILEK_PAY))
for _r, _c, _gx, _by, _hy, _d in _et:
    print("   satir %d · sutun %d · x %.0f · goz tabani %.0f · bilek y %.0f · uzaklik %.1f · pay %.1f  %s" % (_r + 1, _c + 1, _gx, _by, _hy, _d, QR.ERISIM - _d, _gk(_d <= QR.ERISIM)))
assert all(e_[5] <= QR.ERISIM for e_ in _et), "v57: QR gozu robot erisiminin disinda"
_qh = qr_hedef()
_qok = (_qh["kapak_x"][0] <= _qh["kutu_x"][0] and _qh["kutu_x"][1] <= _qh["kapak_x"][1] and _qh["kz"] - _qh["yari"] >= _qh["zmin"]
        and _qh["ky"] + _qh["hk"] < _qh["goz_ust"] and _qh["bekle_z"] + _qh["yari"] <= QR.Z0 - QR_PAY + 0.01)
print("QR HEDEF GOZU (yolculuk): sutun %d · satir %d · kutu x %.1f-%.1f (robot kapagi %.1f-%.1f) · kutu alti %.1f (goz tabani ustu) · ustu %.1f < goz %.1f · kutu z %.1f…%.1f (robot yuzu ≥ %.1f: kapak kapanirken carpmaz) · robot x %.0f · kutu otelemesi dx %.1f dy %.1f dz %.1f  %s"
      % (_qh["sutun"] + 1, _qh["satir"] + 1, _qh["kutu_x"][0], _qh["kutu_x"][1], _qh["kapak_x"][0], _qh["kapak_x"][1], _qh["ky"], _qh["ky"] + _qh["hk"], _qh["goz_ust"],
         _qh["kz"] - _qh["yari"], _qh["kz"] + _qh["yari"], _qh["zmin"], _qh["robot_x"], _qh["dx"], _qh["dy"], _qh["dz"], _gk(_qok)))
print("   catal cekisi: kutu_cad_v7 kutuyu z %.0f'ye ceker (on yuzu %.0f > QR robot yuzu %.0f) → montaj %.0f mm geri alir: kutu %.0f…%.0f'de bekler (yuz %.0f − pay %.0f)"
      % (_qh["cek_z"], _qh["cek_z"] + _qh["yari"], QR.Z0, -_qh["geri"], _qh["bekle_z"] - _qh["yari"], _qh["bekle_z"] + _qh["yari"], QR.Z0, QR_PAY))
assert _qok, "v57: QR hedef gozu (kutu kapak agzina / goze sigmiyor ya da kapak kutuya carpar)"
print("   BILGI · QR goz tabani DUZ: catal disleri kutunun altinda kalir, cekilemez (qr_cad_v1 UYARI) — animasyonda kutu tabana oturtuldu; goz tabanina dis yuvasi / kaburga karari Kemal'de")

DURUM_RENK = {"GERCEK": "gerçek CAD", "GERCEK_PARCA": "kısmen gerçek", "KUTU": "kutu (modellenmedi)", "KATALOG": "katalog (satın alınan)"}


# ---------------------------------------------------------------- GEOMETRİ ----------------------------------------------------------------
DOKU = {}                                                          # v7: kaset basina etiket dokulari (kutuk kurulurken dolar)


# ---- v51 · ÇIPLAK MODEL (Kemal 27 Eyl): yalıtım, yan/ön/arka yüzey sacları, etek (süpürgelik) ve kabin zarfları GÖRSELDE yok — sistemler görünsün.
# Yalnız GLB/USDZ çıktısı; denetimler gerçek parçalarla. Kapak/kabuk istenirse CIPLAK = False.
CIPLAK = True
# v52: govde_kabugu listeden ÇIKARILDI — fırının kendi dış kabuğu makine parçası (79 mm çıkıntı görünür olsun, Kemal)
CIPLAK_AD = ("arka_sac", "arka_dis_sac", "arka_ic_sac", "arka_pu", "yan_dis_sac", "yan_ic_sac", "yan_pu", "yan_on_donus", "on_cerceve_saci", "plint_on",
             "sol_sac", "sag_sac", "on_alt_sac", "on_ust_kapak", "sarjor_yan_kapisi", "kabin_arka_saci", "kabin_taban_saci",
             "on_fitil", "yalitim_tasyunu", "f_arka_saci", "taban_kapisi", "ust_kapi")
CIPLAK_MAL = ("kabuk", "yalitim")
CIPLAK_KUTU = ("A_KABIN", "TOPPING_MODUL", "B_KASA")                            # v57: F taban dolabı + süpürgeliği kalktı
CIPLAK_SAYAC = {"parca": 0, "kutu": 0}
CIPLAK_ADLAR = set()


def ciplak_mi(ad, mal=""):
    if CIPLAK and (str(ad).startswith(CIPLAK_AD) or mal in CIPLAK_MAL):
        CIPLAK_SAYAC["parca"] += 1; CIPLAK_ADLAR.add(str(ad).rstrip("0123456789_")); return True
    return False


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
            if ciplak_mi(p["ad"], p["mal"]): continue
            m = TC_AG(p["wp"])                                              # E-yerel ağ (m)
            yerel = Mesh(); yerel.P = [(q[0] - P[0] * MM, q[1] - P[1] * MM, q[2] - P[2] * MM) for q in m.P]; yerel.N = list(m.N); yerel.I = list(m.I)
            tonlar.setdefault(mal_ad(b, p["mal"]), Mesh()).ekle(yerel)
            sh = p["wp"].val()
            sh = KC.uygula(sh, W0[g]) if g.startswith("B_") else sh
            E_USDZ.append(("%s__%s__%s_usdz" % (b["kod"], p["mal"], p["ad"]), TC_AG(cq.Workplane(obj=sh.translate(cq.Vector(X_E, 0.0, 0.0)))), mal_ad(b, p["mal"])))
        ad = "%s__%s" % (b["kod"], g)
        ebeveyn = ("E_KUTU__" + par) if par else None
        OZEL.append(dict(ad=ad, ebeveyn=ebeveyn, T=((P[0] - Pp[0]) * MM, (P[1] - Pp[1]) * MM, (P[2] - Pp[2]) * MM), tonlar=tonlar))


def _sade(T, V, yol):
    """v65 · kare sadeleştirme: öteleme / ölçek Ramer–Douglas–Peucker (0,2 mm · 1e-3), dönüş yalnız durağan aralıklar (slerp yönü bozulmasın)"""
    import numpy as _np
    n = len(T)
    if n <= 2: return list(T), [tuple(float(c) for c in v_) for v_ in V]
    Va = _np.asarray(V, float)
    if yol == 'rotation':
        d_ = _np.max(_np.abs(_np.diff(Va, axis=0)), axis=1) > 1e-7
        tut = _np.zeros(n, bool); tut[0] = tut[-1] = True; tut[1:] |= d_; tut[:-1] |= d_
    else:
        eps = 2e-4 if yol == 'translation' else 1e-3
        Ta = _np.asarray(T, float); tut = _np.zeros(n, bool); tut[0] = tut[-1] = True; yig = [(0, n - 1)]
        while yig:
            a, b = yig.pop()
            if b - a < 2: continue
            u = (Ta[a + 1:b] - Ta[a]) / (Ta[b] - Ta[a])
            e_ = _np.max(_np.abs(Va[a + 1:b] - (Va[a] + (Va[b] - Va[a]) * u[:, None])), axis=1)
            k = int(_np.argmax(e_))
            if e_[k] > eps:
                m = a + 1 + k; tut[m] = True; yig.append((a, m)); yig.append((m, b))
    ix = _np.nonzero(tut)[0]
    return [float(T[i]) for i in ix], [tuple(float(c) for c in Va[i]) for i in ix]


def glb_yaz(yol, parcalar, dokular, ozel=None, anim=True, liste=None, animler=None):
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
    ANIMLER_ = []                                                                        # v65: birden çok animasyon (siparişler) · v37 çekmece · v38 kutu
    _AL = animler if animler else [("hat_calisma", ANIM if liste is None else liste)]
    ad2node = {n["name"]: i for i, n in enumerate(nodes)}
    for _ai, (_anad, _A) in enumerate(_AL):
        if not _A:
            continue
        anim_sm, anim_ch = [], []
        for kayit in _A:
            ad_, T, V = kayit[0], kayit[1], kayit[2]
            yol_ = kayit[3] if len(kayit) > 3 else "translation"
            if ad_ not in ad2node:
                continue
            if _ai == 0:
                nodes[ad2node[ad_]][yol_] = [float(c) for c in V[0]]                       # v45: durağan duruş = ilk kare (v65: ilk animasyonun)
            if not anim:                                                                  # v40: animasyonsuz yazım
                continue
            T, V = _sade(T, V, yol_)                                                       # v65: kare sadeleştirme
            n_el = 4 if yol_ == "rotation" else 3
            vi = gomu(struct.pack("<%df" % len(T), *T))
            accs.append({"bufferView": vi, "componentType": 5126, "count": len(T), "type": "SCALAR", "min": [min(T)], "max": [max(T)]})
            vo = gomu(struct.pack("<%df" % (n_el * len(V)), *[c for v_ in V for c in v_]))
            accs.append({"bufferView": vo, "componentType": 5126, "count": len(V), "type": "VEC4" if n_el == 4 else "VEC3"})
            anim_sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"})
            anim_ch.append({"sampler": len(anim_sm) - 1, "target": {"node": ad2node[ad_], "path": yol_}})
        if anim_ch:
            ANIMLER_.append({"name": _anad, "samplers": anim_sm, "channels": anim_ch})
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
    if ANIMLER_:
        g["animations"] = ANIMLER_
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


# ---------------------------------------------------------------- v45 · 1 TAM ANİMASYON: ÜRÜN YOLCULUĞU (v48: yolculuk_v48) ----------------------------------------------------------------
# Bu parça hat_montaj_v45.py'ye yap_hat_montaj_v45.py tarafından gömülür (tek başına çalışmaz).
def yolculuk(parcalar, urun="pizza", cekmece=None, urun_ekle=True):
    """Kemal (25 Eyl): "ürün montajına 1 tam animasyon ekle". Bir PİZZA (sos 80 g · kaşar 100 g · küp sucuk 70 g):
    B çekmecesi → FR5 → açıcı → TOPPING (sos yayıcıda tam 1 tur, kaşar + sucuk spirali) → bant → fırın (HIZLANDIRILMIŞ) →
    K (kesme, çit, itici) → E (kutu) → FR5 → QR dolabı. Her hareket makinenin KENDİ kinematiğinden:
    TOPPING = makine_kodu_v2 sırası + topping_v2_hesap_v1 · K = kesme_cad_v6 · E = kutu_cad_v7 · B = store_cad_v8 stroku · QR = qr_cad_v1 (göz robot kapağı).
    v57 ALÇAK HAT: OY = Y_MEK 892 · transfer P + 47 · QR hedefi parçalardan ölçülür (qr_hedef) · enerji zinciri robot x 2650'de SABİT."""
    import math
    import topping_v2_hesap_v1 as TH2
    FPS = 30.0                                                        # v46: hızlı dönen makaralar karede ≤ 31°
    OX, OY = X_BC, Y_MEK                                              # v57: TC orijini = mekanizma tabanı 892 (v56: 1060)

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
    DOZ = TH2.RECETE[urun]["doz"]                                    # v65: sipariş tarifi
    SIRA = sorted(DOZ, key=lambda k: [i["x"] for i in TH2.IST if i["kod"] == k][0])
    IS = {i["kod"]: i for i in TH2.IST}
    ADIM = []
    # B + robot + top
    CEK_T = SC.STROK / (127.0 / 60.0 * math.pi * SC.KAS_PD)           # 3,3 s (çekmece motoru)
    CEK = Iz(0.0); CEK.git(0.0, CEK_T, SC.STROK, "l"); CEK.git(5.0, 5.0 + CEK_T, 0.0, "l")
    _rb = [b for b in B if b["kod"] == "ROBOT_1"][0]; RX0 = (_rb["x"][0] + _rb["x"][1]) / 2.0
    CEK_KOD = cekmece or YOL_CEKMECE                                    # v65: siparişin çekmecesi
    _cb = [b for b in B if b["kod"] == CEK_KOD][0]                     # v57: K3 pide çekmecesi (store_cad_v8)
    TOP_R, TOP_K = 49.0, 0.82
    _tm = [m_ for a_, m_, _x in parcalar if a_ == "URUN__top"]
    TOP_H = (-min(q[1] for q in _tm[0].P) / MM) if _tm else TOP_R * TOP_K   # v47: topun GERÇEK yarı yüksekliği (ağdan · 34,8)
    top_x, top_y0, top_z0 = (_cb["x"][0] + _cb["x"][1]) / 2.0, _cb["y"][0] + 5.0 + TOP_H, (_cb["z"][0] + _cb["z"][1]) / 2.0
    X_AC = OX + TC.XC_TABLA
    TOPX, TOPY, TOPZ = Iz(top_x), Iz(top_y0), Iz(top_z0)
    TOPZ.f(0.0, CEK_T, lambda t: top_z0 + CEK(t))
    TOPZ.git(CEK_T, 3.5, top_z0 + SC.STROK, "l")
    TOPY.git(3.5, 4.2, 650.0); TOPX.git(4.2, 5.6, X_AC); TOPY.git(4.2, 5.6, P + 47.0); TOPZ.git(4.2, 5.6, 150.0)
    TOPZ.git(5.6, 6.4, ZT); TOPY.git(6.4, 6.9, P + TOP_H + 0.5, "ss")
    X_PARK = _cb["x"][0] - 110.0                                        # v58: robot çekmecenin AÇICI TARAFINDA, açık çekmeceye girmez (kaide yarı genişliği 90 + pay 20)
    X_ROB_AC = 700.0                                                   # v58: topu açıcıya bırakırken robot x (açıcı 350'ye erişim ≤ 915 · zincir yüzünden ≥ 508)
    ROB = Iz(RX0); ROB.git(0.3, 3.0, X_PARK); ROB.git(4.2, 5.6, X_ROB_AC)   # v58: top–robot birlikte gider (TOPX 4,2–5,6 ile aynı aralık)
    _ey = max(math.sqrt((TOPX(t_ / 20.0) - ROB(t_ / 20.0)) ** 2 + (TOPY(t_ / 20.0) - OMUZ) ** 2 + (TOPZ(t_ / 20.0) - RZ) ** 2) for t_ in range(70, 139))
    print("   v58 · ROBOT TOPU TASIR: park x %.1f (cekmece %.1f-%.1f disinda) → aciciya x %.0f · top–omuz en uzak %.0f mm (3,5–6,9 s) ≤ pratik erisim %.0f  %s"
          % (X_PARK, _cb["x"][0], _cb["x"][1], X_ROB_AC, _ey, ERISIM, _gk(_ey <= ERISIM)))
    assert _ey <= ERISIM, "v58: robot topa erisemiyor (%.0f > %.0f)" % (_ey, ERISIM)
    ADIM += [(0.0, "ÇEKMECE", "B'nin hamur çekmecesi açılır (strok %.0f, %.1f s); FR5 rayda çekmecenin yanına (açıcı tarafına) gelir; topu alıp açıcıya taşır." % (SC.STROK, CEK_T)),
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
            ADIM.append((t - 1.5, k, "Tabla %s yayıcısının altına gelir: borunun iç ucu merkezde. %.0f g = %.1f ml · UNO Ø%.0f pistonu %.1f mm · tabla TAM 1 TUR (%.1f s, %.0f dev/dk) · katman %.2f mm · kama yarık %.1f→%.1f mm."
                         % ({"SOS": "sos", "HARC": "harç"}.get(k, k.lower()), g, h["ml"], i["sil"], h["strok"], h["sure"], TH2.RPM_YAYICI, h["katman"], TH2.yarik_genisligi(k, 10.0), TH2.yarik_genisligi(k, 121.0))))
            VAL[k].git(t, t + TH2.VALF_SN, 1.0, "ss"); t += TH2.VALF_SN
            w = 6.0 * TH2.RPM_YAYICI
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h0"); t += TH2.RAMPA_SN
            TH_SOS = (t, TH.son)
            TH.git(t, t + h["sure"], TH.son + 360.0, "l"); PIS[k].git(t, t + h["sure"], 0.0, "l")
            for j in range(6): REV.append(("URUN__%s_%d" % (k.lower(), j), t + (j + 0.5) / 6.0 * h["sure"]))
            t += h["sure"]
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h1"); t += TH2.RAMPA_SN + TH2.KESME_VALF_SN
            VAL[k].git(t, t + TH2.VALF_SN, 0.0, "ss")
        else:
            d = TH2.spiral(i, g); x0 = TH2.tabla_x(i, d["r_dis"])
            t = X.git(t, t + gecis(X.son, x0), x0)
            ADIM.append((t - 1.0, k, "%s: %.0f g · tabla %.0f dev/dk, %.2f tur spiral (%.1f s) · ağız r %.0f → %.0f · %s · katman %.1f mm."
                         % (i["ad"], g, TH2.RPM_NOKTA, d["tur"], d["sure"], d["r_dis"], d["r_ic"], ("helezon %.0f dev/dk" % i["rpm"]) if i.get("rpm") else ("UNO Ø%.0f pistonu · nokta ağzı" % i["sil"]), d["katman"])))
            w = 6.0 * TH2.RPM_NOKTA
            if k not in HEL: VAL[k].git(t, t + TH2.RAMPA_SN, 1.0, "ss")                        # v65b: UNO nokta ağzı valfi açılır
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h0"); t += TH2.RAMPA_SN
            ts = t
            X.f(t, t + d["sure"], lambda tt, ts=ts, d=d, i=i: TH2.tabla_x(i, TH2.r_yasa(d, tt - ts)))
            TH.git(t, t + d["sure"], TH.son + w * d["sure"], "l")
            if k in HEL:
                HEL[k].git(t, t + d["sure"], HEL[k].son + i["rpm"] * 6.0 * d["sure"], "l"); KAR[k].git(t, t + d["sure"], KAR[k].son + 24.0 * d["sure"], "l")
            else:                                                                     # v65b: UNO pistonu dozu spiral boyunca basar
                PIS[k].git(t, t + d["sure"], 0.0, "l")
            for j, rm in enumerate((110.0, 80.0, 50.0, 17.5)):
                rm = min(d["r_dis"], max(d["r_ic"], rm))
                REV.append(("URUN__%s_%d" % (k.lower(), j), ts + d["sure"] * (d["r_dis"] ** 2 - rm ** 2) / (d["r_dis"] ** 2 - d["r_ic"] ** 2)))
            t += d["sure"]
            if k in HEL:
                tg = 15.0 / i["rpm"]
                HEL[k].git(t, t + tg, HEL[k].son - 90.0, "l"); TH.git(t, t + tg, TH.son + w * tg, "l"); t += tg
            else:
                VAL[k].git(t, t + TH2.VALF_SN, 0.0, "ss")                                # v65b: valf kapanır
            TH.git(t, t + TH2.RAMPA_SN, TH.son + 0.5 * w * TH2.RAMPA_SN, "h1"); t += TH2.RAMPA_SN
    t = X.git(t, t + gecis(X.son, TH2.X_AKTARMA), TH2.X_AKTARMA)
    T_AKT = t
    ADIM.append((T_AKT - 0.5, "AKTARMA", "Tabla sağ uca gider; İTİCİ (SMC MY1B16-250, 24,9° çapraz) çubuğunu indirir ve pideyi diskten fırının giriş bandına iter: +170 x, −79 z (fırın bandının eksenine); arkada kalan kısmı destek plakası taşır. Çubuk kalkar, araba eve döner; tabla açıcının altına döner."))
    T_IT0, T_IT1 = T_AKT + 0.2, T_AKT + 0.8                                                      # v50: çubuk iner (T_AKT…+0,2), itme (+0,2…+0,8), bekleme +1,0, dönüş temasa +1,5, eve +1,75 (son 17,5 mm'de kalkar)
    X.git(T_AKT + 1.0, T_AKT + 1.0 + gecis(TH2.X_AKTARMA, TH2.X_PARK), TH2.X_PARK)
    T_F0, T_F1 = T_IT1, T_AKT + 10.7
    BANT.git(T_IT1, T_F1, (3940.0 - IT.C1[0]), "l")
    ADIM.append((T_F0, "FIRIN", "TP10 kesitli fırın, gövdesi 1500: bant gövde dışına çıkmaz, ısıtılan 1316 mm, aynı anda 4 ürün. Ürün düz −170 ekseninde K bandına geçer (v51: giriş çiti yok). Animasyonda HIZLANDIRILMIŞ: gerçekte 3,5 dk, burada 10 s."))
    T0K = T_F1 - KS.Z_GELIS[0]
    ADIM += [(T0K + KS.Z_GELIS[0], "KESME", "K bandı ürünü fırın bandından alıp kesme merkezine getirir. Kafa iner, 6 dilim keser (bıçak bandın 0,5 mm üstünde durur). Pizzada sprey yok; pidede aynı kafadaki nozül tereyağı püskürtür."),
             (T0K + KS.Z_TASI[0], "K BANDI + İTİCİ", "Bant ürünü 200 mm taşır; itici ürünün üstünden geri gelip arkasına iner ve ürünü kutuya sürer."),
             (T0K + KS.Z_ITME[0], "KUTU", "İtici ürünü katlanmış kutuya sürer (1,6 s); ürün tabana düşer, kol + piston kapağı kapatıp bastırır."),
             (T0K + KC.Z_CATAL[0], "ROBOT → QR", "FR5 kutuyu tepsinin aralıklarından çatalla alır, rayda QR dolabının önüne (x %.0f) gider." % QR.ROBOT_X)]
    ROB.git(T0K + 5.0, T0K + 9.0, X_E + 260.0)
    QH = qr_hedef()                                                                              # v57: yeni QR dolabı (qr_cad_v1) · göz yeri parçalardan ölçülür (v56 sabit 1215 kalktı)
    TAS = Iz(0.0); TAS.git(T0K + 17.5, T0K + 18.6, 1.0, "s2")                                    # v57: 1) kutu QR yüzünün önünde x + y'de göz ağzına hizalanır (ön yüzü 650'de, gövdeye girmez)
    TAS_Z = Iz(0.0); TAS_Z.git(T0K + 18.6, T0K + 19.9, 1.0, "s2")                                # v57: 2) sonra düz z'de açık kapak ağzından göze girer (açık kapağın altından)
    KAPAK_QR = Iz(0.0); KAPAK_QR.git(T0K + 16.8, T0K + 17.5, 1.0, "ss"); KAPAK_QR.git(T0K + 20.6, T0K + 21.3, 0.0, "ss")   # göz robot kapağı: kutu girmeden açılır, robot çekilince kapanır
    ROB.git(T0K + 17.5, T0K + 19.9, QH["robot_x"]); ROB.git(T0K + 20.5, T0K + 24.5, RX0)
    ADIM.append((T0K + 16.8, "QR DOLABI", "Çatal kutuyu QR robot yüzünün %.0f mm önüne kadar çeker; göz (sütun %d · satır %d, taban %.0f) robot kapağı içeri-yukarı açılır; FR5 x %.0f'de durup kutuyu kapak ağzından göze koyar (göz arkasına 5 mm kala); robot çekilince kapak kapanır, müşteri kendi tarafındaki kapıdan QR ile alır. Enerji zinciri modelde robot x %.0f konumunda sabit (animasyonda hareket etmez)."
                 % (QR_PAY, QH["sutun"] + 1, QH["satir"] + 1, QR.GOZ_TABAN[QH["satir"]], QH["robot_x"], RE.RX_MONTAJ)))
    T_J = math.ceil(T0K + 25.5)
    GIZLE = T_J - 0.6
    TT = [i_ / FPS for i_ in range(int(round(T_J * FPS)) + 1)]
    te = lambda t: min(19.5, max(0.0, t - T0K))
    tk = lambda t: min(KS.DONGU, max(0.0, t - T0K))
    tas = lambda t: (QH["dx"] * TAS(t), QH["dy"] * TAS(t), QH["geri"] * KC.ss(KC.Z_CATAL[2], KC.Z_CATAL[3], te(t)) + QH["dz"] * TAS_Z(t))   # v57: çatal çekişi QR yüzünün önünde biter (geri) · sonra kutu E'den QR gözüne
    QR_YOL.update(t=(T0K + KC.Z_CATAL[2], T0K + 21.3), kapak=KAPAK_QR, kutu=lambda t: (X_E + (KC.BX0 + KC.BX1) / 2.0 + tas(t)[0], KC.TEPSI + KC.catal_kutu(te(t))[0] + tas(t)[1], KC.ZB + KC.catal_kutu(te(t))[1] + tas(t)[2]))   # v57: kutu tabanı ortası (dünya) · GÖZ YOLU denetimi

    # ================= ÜRÜN (düğümler, ürün merkezine göre ağ) =================
    for k_, r_ in (("hamur", (0.93, 0.78, 0.52, 1.0)), ("sos", (0.74, 0.17, 0.10, 1.0)), ("kasar", (0.97, 0.87, 0.50, 1.0)),
                   ("sucuk", (0.55, 0.12, 0.10, 1.0)), ("kesik", (0.30, 0.18, 0.10, 1.0)),
                   ("harc", (0.60, 0.24, 0.15, 1.0)), ("kiyma", (0.42, 0.24, 0.16, 1.0)), ("kusbasi", (0.48, 0.27, 0.19, 1.0))):   # v65
        MALZEME["MU_URUN__" + k_] = dict(renk=r_, met=0.0, ruf=0.8)
    def ekle_u(ad, sh, mal):
        if not urun_ekle: return                                                      # v65: ürün ağları yalnız ilk siparişte
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
    th_s = 0.5 * 6.0 * TH2.RPM_YAYICI * TH2.RAMPA_SN                                  # v65: yayıcı hep ilk üst malzeme → tabla açısı siparişten bağımsız
    assert TH_SOS is None or abs(TH_SOS[1] - th_s) < 1e-6, (TH_SOS, th_s)
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
    for j in range(6):                                                                # v65: harç (lahmacun) · yayıcı dilimleri
        ekle_u("harc_%d" % j, halka(10.0, 125.0, 8.0, 10.5, -th_s - 60.0 * (j + 1), -th_s - 60.0 * j, 24), "harc")
    for j, (r0, r1) in enumerate(((95.0, 125.0), (65.0, 95.0), (35.0, 65.0), (0.0, 35.0))):   # v65: kıyma halkaları
        ekle_u("kiyma_%d" % j, halka(r0, r1, 9.5, 12.5), "kiyma")
    for j, (rr, n) in enumerate(((110.0, 22), (80.0, 16), (50.0, 10), (22.0, 4))):  # v65: kuşbaşı küpleri
        kup = None
        for m in range(n):
            a = 2 * math.pi * (m + 0.4 * j) / n
            b_ = cq.Workplane("XY").box(12, 12, 12).translate((rr * math.cos(a), 15.5, -rr * math.sin(a)))
            kup = b_ if kup is None else kup.union(b_)
        ekle_u("kusbasi_%d" % j, kup, "kusbasi")
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
            u = min(1.0, max(0.0, (t - T_IT0) / (T_IT1 - T_IT0)))                                   # v49: çapraz itme (C0 → C1)
            return (IT.C0[0] + (IT.C1[0] - IT.C0[0]) * u, OY + 108.0, IT.C0[1] + (IT.C1[1] - IT.C0[1]) * u)
        if t < T_F1:
            u = (t - T_F0) / (T_F1 - T_F0); x0 = IT.C1[0]; x_ = x0 + (3940.0 - x0) * u                                # v49: bantlar 2507'den alır
            return (x_, OY + 108.0 if x_ <= FT.X_DISK_KENAR else KS.FIRIN_BANDI, FT.urun_z(x_))
        tK = t - T0K
        if tK < KC.Z_PIZZA[1]:
            x, y, z = KS.urun_merkez(max(0.0, tK)); xw = X_K + x; return (xw, y, FT.urun_z(xw) if xw < FT.CC_B[0] + 1.0 else z)
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
    u_adlar = (["URUN__hamur"] + ["URUN__sos_%d" % j for j in range(6)] + ["URUN__harc_%d" % j for j in range(6)] + ["URUN__kasar_%d" % j for j in range(4)]
               + ["URUN__sucuk_%d" % j for j in range(4)] + ["URUN__kiyma_%d" % j for j in range(4)] + ["URUN__kusbasi_%d" % j for j in range(4)] + ["URUN__kesik"])   # v65
    rv = dict(REV)
    _UAG = {}
    for a_, m_, _x in parcalar:
        if a_.startswith("URUN__"): _UAG[a_] = m_
    for ad in u_adlar:
        if ad in ("URUN__hamur", "URUN__kesik") or ad in rv:
            kanal(ad, lambda t: tuple(c * MM for c in urun_C(t)))
            kanal(ad, lambda t: qy(th_urun(t)), "rotation")
            KONTROL.append((ad, lambda t: tuple(c * MM for c in urun_C(t)), lambda t: qy(th_urun(t)), {"_": _UAG[ad]}))
        else:                                                                         # v65: bu siparişte olmayan üst malzeme · gizli + durağan
            kanal(ad, lambda t: tuple(c * MM for c in urun_C(0.0)))
            kanal(ad, lambda t: qy(0.0), "rotation")
    kanal("URUN__hamur", lambda t: ((0.18 + 0.82 * ACMA(t)), 1.0, (0.18 + 0.82 * ACMA(t))) if T_ACMA <= t < GIZLE else (1e-4,) * 3, "scale")
    for ad in u_adlar[1:-1]:
        kanal(ad, vis(rv[ad], GIZLE) if ad in rv else (lambda t: (1e-4,) * 3), "scale")
    kanal("URUN__kesik", vis(T0K + KS.Z_KES[0] + 0.3, GIZLE), "scale")
    # TOPPING düğümleri — v46: DÖNEN parçalar KENDİ EKSENİNDE duran ayrı düğüm (ağ pivota göre yerel).
    # v45'te dünya ağına "dönüş + telafi ötelemesi" veriliyordu; kareler arasında öteleme doğrusal, dönüş yay boyunca
    # ara değerlendiği için parça ekseninden kayıyordu (ölçüldü: bant burun makarası 350 mm, koniler 96, sos valfi 94).
    P_T = (OX + TC.XC_TABLA, OY + 108.0, ZT); A_K = (OX + TC.XC_TABLA, OY + 116.0, ZT); ya = math.radians(17.82)
    ROL = {}                                                          # v48: TOPPING'in aktarma bandı yok
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
    # v49 · AKTARMA İTİCİSİ: araba s(t) (çubuk yüzü konumu, mm) ve çubuk açısı (0 = inik, 90 = kalkık)
    def it_s(t):
        if t < T_IT0: return IT.S_HOME
        if t < T_IT1: return IT.S_HOME + (IT.S_END - IT.S_HOME) * (t - T_IT0) / (T_IT1 - T_IT0)
        if t < T_AKT + 1.0: return IT.S_END
        if t < T_AKT + 1.5: return IT.S_END + (IT.S_TEMAS - IT.S_END) * (t - T_AKT - 1.0) / 0.5                 # dönüş temasa kadar
        if t < T_AKT + 1.75: return IT.S_TEMAS + (IT.S_HOME - IT.S_TEMAS) * (t - T_AKT - 1.5) / 0.25            # son 17,5 mm yavaş (kalkış)
        return IT.S_HOME
    def it_aci(t):
        if t < T_AKT: return 90.0
        if t < T_IT0: return 90.0 * (1.0 - (t - T_AKT) / (T_IT0 - T_AKT))
        s_ = it_s(t)
        if t > T_AKT + 1.0 and s_ < IT.S_TEMAS: return 90.0 * (IT.S_TEMAS - s_) / (IT.S_TEMAS - IT.S_HOME)
        return 0.0
    def it_kay(t):
        d_ = it_s(t) - IT.S_HOME; return (d_ * IT.U[0] * MM, 0.0, d_ * IT.U[1] * MM)
    for a_, m_, mal_ in parcalar:
        if a_.startswith("C_ITICI__") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == "ARABA":
            kanal(a_, it_kay)
    IT.kur(IT.S_HOME, False)                                                                 # KOL yerel ağı: ev konumu, çubuk İNİK (dönme animasyonla)
    _piv = IT.dunya_nokta(IT.S_HOME, IT.PIVOT_Y, IT.W_AXIS)
    ton = {}
    for p in IT.PARCALAR:
        if p["grup"] != "KOL": continue
        m_ = TC_AG(cq.Workplane(obj=IT.dunya(p)))
        y_ = Mesh(); y_.P = [(q[0] - _piv[0] * MM, q[1] - _piv[1] * MM, q[2] - _piv[2] * MM) for q in m_.P]; y_.N = list(m_.N); y_.I = list(m_.I)
        ton.setdefault(mal_ad({"kod": "C_ITICI", "modul": "C"}, p["mal"]), Mesh()).ekle(y_)
    for a_, m_, mal_ in parcalar:
        if a_.startswith("C_ITICI__") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == "KOL": HARIC.add(a_)
    _fT = lambda t: (_piv[0] + (it_s(t) - IT.S_HOME) * IT.U[0], _piv[1], _piv[2] + (it_s(t) - IT.S_HOME) * IT.U[1])
    _fR = lambda t: qax((IT.W[0], 0.0, IT.W[1]), it_aci(t))
    OZEL_T.append(dict(ad="C_ITICI_DONER__KOL", ebeveyn=None, T=tuple(c * MM for c in _fT(0.0)), tonlar=ton))
    kanal("C_ITICI_DONER__KOL", lambda t: tuple(c * MM for c in _fT(t)))
    kanal("C_ITICI_DONER__KOL", _fR, "rotation")
    KONTROL.append(("C_ITICI_DONER__KOL", lambda t: tuple(c * MM for c in _fT(t)), _fR, ton))
    IT.kur(IT.S_HOME, True)
    # v48 · fırın + giriş bandı ruloları KENDİ EKSENİNDE (ağ pivota göre yerel) · bant yüzey hızıyla · dünya koordinatı
    ROL_F = {"RULO_TP_GIRIS": ((FT.RULO_X[0], FT.RULO_Y, 0.0), FT.SARIM_R), "RULO_TP_CIKIS": ((FT.RULO_X[1], FT.RULO_Y, 0.0), FT.SARIM_R),
             "RULO_GB_BURUN": ((FT.GB_XB, FT.GB_RY, 0.0), 11.5), "RULO_GB_TAHRIK": ((FT.GB_XT, FT.GB_RY, 0.0), 11.5)}
    for g, (P_, r_) in ROL_F.items():
        ton = {}
        for a_, m_, mal_ in parcalar:
            if a_.startswith("F_") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == g:
                y_ = Mesh(); y_.P = [(q[0] - P_[0] * MM, q[1] - P_[1] * MM, q[2] - P_[2] * MM) for q in m_.P]; y_.N = list(m_.N); y_.I = list(m_.I)
                ton.setdefault(mal_, Mesh()).ekle(y_); HARIC.add(a_)
        if not ton:
            continue
        ad = "F_DONER__" + g
        fR = lambda t, r_=r_: qax((0, 0, 1), -math.degrees(BANT(t) / r_))
        OZEL_T.append(dict(ad=ad, ebeveyn=None, T=tuple(c * MM for c in P_), tonlar=ton))
        kanal(ad, lambda t, P_=P_: tuple(c * MM for c in P_))
        kanal(ad, fR, "rotation")
        KONTROL.append((ad, lambda t, P_=P_: tuple(c * MM for c in P_), fR, ton))
    # v57 · QR gözünün ROBOT KAPAĞI (qr_cad_v1 · QR.MENTESE): kendi mil ekseninde duran düğüm (ağ pivota göre yerel) · kutu girerken açık
    _gq = QH["grup"]; _pq, _axq, _acq = QH["mentese"]
    ton = {}
    for a_, m_, mal_ in parcalar:
        if a_.startswith("QR_GOZLER__") and a_.count("__") == 2 and a_.rsplit("__", 1)[1] == _gq:
            y_ = Mesh(); y_.P = [(q[0] - _pq[0] * MM, q[1] - _pq[1] * MM, q[2] - _pq[2] * MM) for q in m_.P]; y_.N = list(m_.N); y_.I = list(m_.I)
            ton.setdefault(mal_, Mesh()).ekle(y_); HARIC.add(a_)
    assert ton, "v57: QR gozu %s robot kapagi dugumu bulunamadi" % _gq
    _fTq = lambda t: tuple(c * MM for c in _pq)
    _fRq = lambda t: qax(_axq, _acq * KAPAK_QR(t))
    OZEL_T.append(dict(ad="QR_DONER__" + _gq, ebeveyn=None, T=_fTq(0.0), tonlar=ton))
    kanal("QR_DONER__" + _gq, _fTq)
    kanal("QR_DONER__" + _gq, _fRq, "rotation")
    KONTROL.append(("QR_DONER__" + _gq, _fTq, _fRq, ton))
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
        if a_.startswith(CEK_KOD + "__") and a_.endswith("__CEKMECE"):
            kanal(a_, lambda t: (0.0, 0.0, CEK(t) * MM))
        elif a_.startswith(CEK_KOD + "__") and a_.endswith("__CEKMECE_ARA"):
            kanal(a_, lambda t: (0.0, 0.0, CEK(t) * SC.RAY_ARA_ORAN * MM))
        elif a_.split("__")[0] in CEK_TUM and a_.endswith(("__CEKMECE", "__CEKMECE_ARA")):   # v65: öbür siparişlerin çekmecesi bu animasyonda kapalı
            kanal(a_, lambda t: (0.0, 0.0, 0.0))
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
    if urun == "lahmacun":                                                            # v65: lahmacun metinleri
        ADIM = [(a[0], a[1], a[2].replace("hamur çekmecesi", "lahmacun çekmecesi (K2)")) if a[1] == "ÇEKMECE" else
                (a[0], a[1], a[2] + " Lahmacunda kutu 2. lahmacunu bekler; animasyonda tek lahmacun gösteriliyor.") if a[1] == "KUTU" else a for a in ADIM]
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
    YOL_ZAMAN.clear(); YOL_ZAMAN.update(T0K=T0K, T_J=float(T_J), FPS=FPS)                         # v66
    return A, [dict(t=round(a[0], 2), ad=a[1], not_=a[2]) for a in ADIM], float(T_J), OZEL_T, HARIC, RAPOR


# ---- v62 · PARÇA KUTULARI (sayfadaki fare etiketi): her TC_AG çağrısında çağıran satırın parçası (p / q) ve birimi (b) kaydedilir
import linecache as _lc62
PARCA_KUTU = {}
_TC_AG_ASIL = TC_AG


def TC_AG(wp, *a, **k):
    try:
        f_ = sys._getframe(1); L_ = f_.f_locals; sat_ = _lc62.getline(f_.f_code.co_filename, f_.f_lineno)
        pv_ = L_.get("q") if 'q["' in sat_ else (L_.get("p") if 'p["' in sat_ else None)
        bv_ = L_.get("b")
        if isinstance(pv_, dict) and "ad" in pv_ and isinstance(bv_, dict) and "kod" in bv_:
            sh_ = wp.val() if hasattr(wp, "val") else wp; bb_ = sh_.BoundingBox()
            PARCA_KUTU.setdefault(bv_["kod"], []).append([pv_["ad"], 1 if pv_.get("mal") == "on_seffaf" else 0]
                                                        + [round(v_, 1) for v_ in (bb_.xmin, bb_.xmax, bb_.ymin, bb_.ymax, bb_.zmin, bb_.zmax)])
    except Exception:
        pass
    return _TC_AG_ASIL(wp, *a, **k)


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
            for _p63 in TC.PARCALAR:                                               # v63: TOPPING ön kapakları (TC yeniden kurulunca) şeffaf gösterim
                if ON_SEFFAF.match(_p63["ad"]): _p63["mal"] = "on_seffaf"
            # Makine gorunumunde ON KAPAK ve contasi cizilmez: kapak kapaliyken kasetler ne gorunur ne secilebilir.
            # Kapak gercek: kendi STEP'i ve BOM'u topping_modul_v1 klasorunde duruyor; burada ACIK kabul ediliyor.
            # v27: ON KAPAGIN PU CEKIRDEGI DE CIZILMEZ. Liste v15'ten beri eksikti:
            # kapak o surumde masif bloktan SAC KABUK + PU CEKIRDEK'e cevrilmisti,
            # "on_kapak" ve contasi disarida birakildi ama "on_kapak_pu" listeye
            # eklenmedi. Sonuc: kapagin yalitim dolgusu tek basina duruyor ve
            # kasetlerin onunu kapatiyordu (Kemal: "kasetleri goremiyorum").
            KAPAK = ("on_kapak", "on_kapak_pu", "kapak_contasi")
            ps = [p for p in TC.PARCALAR if v1_kalir(p["ad"]) and p["ad"] not in KAPAK and p["ad"] not in AKTARMA_TP10]   # v48: aktarma bandı yok
            ton = {}
            for p in ps:
                if ciplak_mi(p["ad"], p["mal"]): continue
                _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))
                if p["ad"] == "cikis_yarigi_contasi": sh = YARIK_V2                       # v48: çerçeve −417…−13, alt çıta 1145–1155
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
                if ciplak_mi(q["ad"], q["mal"]): continue
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
            for _rota in (ANA_V44, ANA_K48):                                    # v48: fırın üstünden TOPPING'e + K'ye dal
                _ana = TU.boru(_rota, 5.0)
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
                if ciplak_mi(p["ad"], p["mal"]): continue
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
                if ciplak_mi(p["ad"], p["mal"]): continue
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
                if ciplak_mi(p["ad"], p["mal"]): continue
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(p["wp"]))
                asm.add(p["wp"].val(), name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK.get(p["mal"], RENK["kutu"])))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)
        elif b["durum"] == "GERCEK_FIRIN":                                                   # v48
            ps = [p for p in FT.PARCALAR if p["birim"] == b["kod"]]
            ton = {}
            for p in ps:
                if ciplak_mi(p["ad"], p["mal"]): continue
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=FT.dunya(p)), p["ad"].startswith("giris_bandi_motoru")))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)
        elif b["durum"] == "GERCEK_ITICI":                                                   # v49
            ps = [p for p in IT.PARCALAR if p["birim"] == b["kod"]]
            ton = {}
            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=IT.dunya(p))))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)
        elif b["durum"] == "GERCEK_BULASIK":                                                 # v53
            ps = [p for p in BM.PARCALAR if p["birim"] == BM_KOD.get(b["kod"], b["kod"])]   # v57: K_BULASIK ← bulasik_cad_v2 "D_BULASIK"
            ton = {}
            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=BM.dunya(p))))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)
        elif b["durum"] in GERCEK_DIS:                                                       # v57: QR dolabı · tezgâh · ray ekleri · kaide (dünya koordinatı, bulaşık dalı gibi)
            M_ = GERCEK_DIS[b["durum"]]
            ps = [p for p in M_.PARCALAR if p["birim"] == b["kod"]]
            ton = {}
            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=M_.dunya(p))))
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
            if CIPLAK and (b["kod"] in CIPLAK_KUTU or b["kod"].endswith("_KABIN")):
                CIPLAK_SAYAC["kutu"] += 1                                                    # v51: kabin/etek zarfı görselde yok
            else:
                parcalar.append((b["kod"], kutu_ag(b), mal_ad(b))); asm.add(kutu_kat(b), name=b["kod"], color=cq.Color(*RENK.get(b["mal"], RENK["kutu"])))
        b["olcu"] = [round(b["x"][1] - b["x"][0]), round(b["y"][1] - b["y"][0]), round(b["z"][1] - b["z"][0])]
    print("CIPLAK MODEL (v51): gorselden cikarilan parca %d · kabin/etek kutusu %d (yalitim, yan/on/arka saclar, PU duvarlar, fitil, supurgelik) — denetimler tam parcayla" % (CIPLAK_SAYAC["parca"], CIPLAK_SAYAC["kutu"]))
    print("   gizlenen ad kokleri (v52): %s" % ", ".join(sorted(CIPLAK_ADLAR)))
    ye = [a for a, _m, _x in parcalar if "__etiket_yuva_" in a]
    print("YUVA ETIKETI (v23): %d" % len(ye))
    assert len(ye) == 0, "v42: yuva etiketi olmamali (yuvalar kalkti)"
    hp = [a for a, _m, _x in parcalar if a.count("__") == 2]
    print("HAREKETLI PAKET (v17): %d dugum · %s" % (len(hp), " · ".join(sorted({a.rsplit("__", 1)[1] for a in hp}))))
    assert hp, "hicbir hareketli paket ayrilmadi — grup kurali tutmuyor"
    ucgen = sum(len(m.I) // 3 for _a, m, _mal in parcalar)
    print("BIRIM %d  ·  %s  ·  %d ucgen" % (len(B), "  ·  ".join("%s %d" % (k, v) for k, v in sorted(sayac.items())), ucgen))

    # ---- zarf denetimi: hiçbir birim hattın dışına taşmasın; kasetler yuvasında mı ----
    tasan = [b["kod"] for b in B if b["modul"] not in ("-", "S") and not (-1 <= b["x"][0] and b["x"][1] <= HAT_W + 1 and -1 <= b["y"][0] and b["y"][1] <= H_MAK + 1 and -DZ - 1 <= b["z"][0] and b["z"][1] <= FT.ZS + 1)]   # v63: bütün istasyonlar ön düzleme (+79) kadar
    print("ZARF DENETIMI: %s" % ("hepsi hattin icinde (%.0f x %.0f x %.0f; v51: F firin birimleri z +%.0f cikintiya kadar; v57: S modulu + R haric — QR 2050 yuksek, koridorun karsisinda)" % (HAT_W, H_MAK, DZ, FT.ZS) if not tasan else "TASAN: " + ", ".join(tasan)))
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

    # ---- v36 · B CEKMECE MODULU (v57: store_cad_v8 · tek parça 0–4000 × 123–788) ----
    _bs = [b for b in B if b["durum"] == "GERCEK_STORE"]
    print("B CEKMECE MODULU (store_cad_v8 · alt taban %.0f · ust %.0f · x 0-%.0f · tam kaplama kapaklar): %d birim · %d parca · %d cekmece" % (Y_ALT, Y_DUZ, W_B, len(_bs), sum(b.get("parca", 0) for b in _bs), len(SC.CEK)))
    _bust = max(b["y"][1] for b in _bs)
    print("   B birimleri ustu <= %.0f (en yuksek %.2f): %s" % (Y_DUZ, _bust, _gk(_bust <= Y_DUZ + 0.01)))
    assert all(b["y"][1] <= Y_DUZ + 0.01 for b in _bs), "B tavani %.0f'i asiyor" % Y_DUZ
    # ---- v35 · SUREC KOTU + TABAN HIZASI + CAKISMA (v57: Y_MEK 892 · Y_DUZ 788) ----
    _pp = {p["ad"]: p for p in TC.PARCALAR}
    _cd = _pp["calisma_diski"]["wp"].val().BoundingBox(); _bt = _pp["bant"]["wp"].val().BoundingBox()
    print("SUREC KOTU (CAD'den olculdu): disk ustu %.1f · firin bandi %.1f · kesme plakasi %.1f · kutu tepsisi %.1f · tabla ekseni z %.0f"
          % (Y_MEK + _cd.ymax, Y_MEK + _bt.ymax, PLAKA, TEPSI_Y, ZT))
    assert abs(Y_MEK + _cd.ymax - P) < 0.05, "disk ustu %.2f, beklenen %.2f" % (Y_MEK + _cd.ymax, P)
    assert abs(Y_MEK + _bt.ymax - BANT_UST) < 0.05, "bant ustu %.2f, beklenen %.2f" % (Y_MEK + _bt.ymax, BANT_UST)
    assert P > BANT_UST > PLAKA > TEPSI_Y, "urun yukari basamaga carpar"
    _bk = {b["kod"]: b for b in B}
    _kot = [("A_GOVDE tabani (dolap ustu · v63 gercek kabin)", _bk["A_GOVDE"]["y"][0], Y_DUZ), ("TOPPING_MODUL tabani (TC orijini)", _bk["TOPPING_MODUL"]["y"][0], Y_MEK),
            ("B_KASA ustu (duz cizgi)", _bk["B_KASA"]["y"][1], Y_DUZ), ("KAIDE_A alti", _bk["KAIDE_A"]["y"][0], Y_DUZ), ("KAIDE_C alti", _bk["KAIDE_C"]["y"][0], Y_DUZ),
            ("KAIDE_C ustu (mekanizma tabani)", _bk["KAIDE_C"]["y"][1], Y_MEK), ("F_TP10_GOVDE alti (firin dolabin ustunde)", _bk["F_TP10_GOVDE"]["y"][0], Y_DUZ),
            ("E_GOVDE alti (tek parca)", _bk["E_GOVDE"]["y"][0], 0.0), ("E_GOVDE ustu", _bk["E_GOVDE"]["y"][1], H_MAK), ("TOPPING_MODUL ustu", _bk["TOPPING_MODUL"]["y"][1], H_MAK)]
    print("TABAN HIZASI (v57 alcak hat):")
    for ad_, v_, h_ in _kot:
        print("   %-46s %8.2f = %6.0f  %s" % (ad_, v_, h_, _gk(abs(v_ - h_) < 0.01)))
    assert all(abs(v_ - h_) < 0.01 for _a, v_, h_ in _kot), "v57: taban hizasi tutmuyor"
    # v40 · ALT TABAN ÇİZGİSİ: B, K ve E üreteçleri kendi ölçümünü assert ediyor (gövde altı); burada üçünün AYNI çizgide olduğu (v57: F dolabı yok)
    assert abs(SC.Y_PLINT - Y_ALT) < 0.01 and abs(KC.Y_PLINT - Y_ALT) < 0.01, "B ve E alt taban cizgisi farkli: %.1f / %.1f" % (SC.Y_PLINT, KC.Y_PLINT)
    assert abs(KS.Y_PLINT - Y_ALT) < 0.01 and abs(KS.H_B - Y_MEK) < 0.01, "K alt taban / istasyon tabani farkli"      # v45: K kendi denetimini yapar
    assert abs(KS.BANT - PLAKA) < 0.01, "K bandi %.1f · plaka %.1f" % (KS.BANT, PLAKA)
    _gb = min(p["wp"].val().BoundingBox().ymin for p in SC.PARCALAR if not p["ad"].startswith(("ayak_", "plint_on", "onyuz_plint", "kondenser_atis_kanali", "buharlastirma_tavasi", "gider_borusu_")))
    _ge = min(p["wp"].val().BoundingBox().ymin for p in KC.PARCALAR if p["grup"] == "SABIT" and not p["ad"].startswith(("ayak_", "plint_on", "onyuz_plint", "asansor_")))
    assert abs(_gb - Y_ALT) < 0.05 and abs(_ge - Y_ALT) < 0.05, "govde altlari: B %.1f · E %.1f" % (_gb, _ge)
    print("ALT TABAN CIZGISI (v40): B %.1f · E %.1f · K dolabi %.0f -> ayni cizgi %.0f · altlari ayak + supurgelik · v57: F taban dolabi YOK (firin dolabin ustunde) -> GECTI"
          % (_gb, _ge, KS.Y_PLINT, Y_ALT))
    print("E KUTU MODULU (kutu_cad_v7): %d birim · %d parca · %d mentese dugumu · genislik %.0f · hat %.0f"
          % (len([b for b in B if b["durum"] == "GERCEK_KUTU"]), sum(len(v) for v in E_PARCA.values()), len(OZEL), W_E, HAT_W))
    assert not [b for b in B if "KARTON KULE" in b["ad"].upper() or b["kod"].endswith("KUTU_YEDEK")], "yedek karton kutu hala var"   # v48: 'kutu yedeği' metni artık kompresör/davlumbaz adında geçiyor (fırın üstü raf) — eski karton kulesi yok
    print("TABAN HIZASI: tek duz cizgi %.0f (dolap ustu = A/C kabin = firin alti) · A/C mekanizma + K istasyon tabani %.0f (kaide %.0f) · disk %.0f · makine ustu %.0f · E tek parca 0-%.0f -> GECTI"
          % (Y_DUZ, Y_MEK, Y_MEK - Y_DUZ, P, H_MAK, H_MAK))
    _ZON = ("HAVA_KOMPRESOR",)                                                # v48: fırın kutusu yok                              # zarf/bolge birimleri: icindekilerle kesismesi dogal
    def _kes(a_, b_):
        return all(a_[i][0] < b_[i][1] - 0.5 and b_[i][0] < a_[i][1] - 0.5 for i in range(3))
    _yeni = [b for b in B if b["modul"] in ("D", "K", "E") and not b["kod"].endswith("_KABIN") and b["durum"] not in ("GERCEK_KUTU", "GERCEK_KESME", "GERCEK_FIRIN")]   # v48: fırın parçaları gerçek katıyla taranır · v45: K kendi taramasını yapar (kesme_cad_v1) · v38: E kendi taramasini yapiyor (kutu_cad_v2: makine 201 an + kutu 46 an + pizza 25 an = 0)
    _cak = []
    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"] in KAPAK or p["ad"] in AKTARMA_TP10:
            continue
        bb = p["wp"].val().BoundingBox()
        z_ = ((bb.xmin + X_BC, bb.xmax + X_BC), (bb.ymin + Y_MEK, bb.ymax + Y_MEK), (bb.zmin, bb.zmax))
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
    _sira = list(ISTASYON_SIRA)                                                     # v57: store_cad_v8 çekmeceleri (K3 pide · K1 lahmacun · K6 içecek · K5 tatlı)
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
    ANIM_SIP, SIP_DURUM = [], []                                                       # v65: sipariş animasyonları
    for _i, (_kod, _ad, _cek) in enumerate(SIPARIS):
        _A, _ADIM, _T, _OZ, _HAR, _SAP = yolculuk(parcalar, urun=_kod, cekmece=_cek, urun_ekle=(_i == 0))
        if _kod == "lahmacun": LAH_Z = dict(YOL_ZAMAN)                                   # v66
        if _i == 0:
            ANIM_HAT, ADIM_HAT, T_J, OZEL_T, HARIC_T, SAPMA = _A, _ADIM, _T, _OZ, _HAR, list(_SAP)
        else:
            assert [o["ad"] for o in _OZ] == [o["ad"] for o in OZEL_T] and set(_HAR) == set(HARIC_T), "v65: siparisler arasinda donen dugumler farkli"
            SAPMA = sorted(SAPMA + list(_SAP), key=lambda r: -r[0])
        ANIM_SIP.append(("siparis_" + _kod, _A)); SIP_DURUM.append(dict(kod=_kod, ad=_ad, sure=_T, adim=_ADIM))
        print("   v65 · SIPARIS %-10s %5.1f sn · %4d kanal · %2d adim · cekmece %s" % (_kod, _T, len(_A), len(_ADIM), _cek))
    # ---- v66 · İKİ LAHMACUN BİR KUTUDA ----
    for _ad in L2_ADLAR:                                                                  # 2. ürünün düğümleri: 1. ürünün ağları, ayrı düğüm
        _src = [x_ for x_ in parcalar if x_[0] == "URUN__" + _ad][0]
        parcalar.append(("URUN__L2_" + _ad, _src[1], _src[2]))
    def iki_lahmacun(A, Z, TE_H=10.4):
        """tek lahmacun çevrimini (A, 30 fps) iki çevrime çevirir · TE_H: E'nin beklediği an (ürün düştü 10,35 · kafa hazırlığı 10,6)"""
        import numpy as _np, math as _m
        FPS, T0K, TJ = Z["FPS"], Z["T0K"], Z["T_J"]
        ch = [(a_[0], a_[3] if len(a_) > 3 else "translation", _np.asarray(a_[2], float)) for a_ in A]
        def qn(q):
            n_ = float(_np.linalg.norm(q)); return q / n_ if n_ > 0 else q
        def samp(V, t, yol):
            x_ = min(max(t, 0.0), (len(V) - 1) / FPS) * FPS; i_ = int(x_)
            if i_ >= len(V) - 1: return V[-1].copy()
            a0, a1 = V[i_], V[i_ + 1]
            if yol == "rotation" and float(_np.dot(a0, a1)) < 0: a1 = -a1
            v_ = a0 + (a1 - a0) * (x_ - i_)
            return qn(v_) if yol == "rotation" else v_
        def qmul(a, b):
            ax, ay, az, aw = a; bx, by, bz, bw = b
            return _np.array([aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx, aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz])
        def qinv(q): return _np.array([-q[0], -q[1], -q[2], q[3]])
        def fark(a, b, yol):
            return (1.0 - abs(float(_np.dot(qn(a), qn(b))))) > 1e-8 if yol == "rotation" else float(_np.max(_np.abs(a - b))) > 1e-7
        def aralik(V, yol):
            ix_ = [i_ for i_ in range(1, len(V)) if fark(V[i_], V[i_ - 1], yol)]
            return (None, None) if not ix_ else ((ix_[0] - 1) / FPS, ix_[-1] / FPS)
        def grup(ad):
            if ad.startswith("URUN__L2_"): return "urun2"
            if ad.startswith("URUN__") and ad != "URUN__top": return "urun1"
            if ad.startswith("ROBOT_1"): return "robot"
            if ad.startswith("QR_"): return "qr"
            if ad.startswith("E_"): return "e"
            return "mak"
        D, e_tabla, en = 0.0, 0.0, ("", 0.0)
        for ad, yol, V in ch:
            if grup(ad) != "mak": continue
            m_, e_ = aralik(V, yol)
            if m_ is None: continue
            if e_ - m_ > en[1]: en = (ad, e_ - m_)
            D = max(D, e_ - m_ + 0.5)
            if ad.startswith("TOPPING_DONER__TABLA") and yol == "translation": e_tabla = max(e_tabla, e_)
        D = max(D, e_tabla - 3.9)                                                         # 2. top diske inmeden (4,2 s) tabla açıcıya dönmüş olmalı
        D = _m.ceil(D * 2.0) / 2.0
        T2 = TJ + D; TT2 = [i_ / FPS for i_ in range(int(round(T2 * FPS)) + 1)]; T_H1 = T0K + TE_H
        print("   v66 · IKI LAHMACUN: ikinci cevrim D = %.1f sn (en uzun makine hareketi %s %.1f sn · tabla aciciya %.1f sn) · toplam %.1f sn · kutu %.1f–%.1f sn acik bekler"
              % (D, en[0], en[1], e_tabla, T2, T_H1, T_H1 + D))
        yeni, uyari = [], []
        for ad, yol, V in ch:
            g_ = grup(ad); out = []
            if g_ == "mak":
                m_, e_ = aralik(V, yol)
                if m_ is None:
                    out = [V[0]] * len(TT2)
                else:
                    s_ = D + m_
                    if e_ > s_ + 1e-6: uyari.append("%s %s: 1. cevrim %.1f sn'de bitiyor, 2. cevrim %.1f sn'de basliyor" % (ad, yol, e_, s_))
                    q1 = samp(V, s_, yol); q0i = qinv(qn(V[0])) if yol == "rotation" else None
                    if yol != "rotation" and float(_np.max(_np.abs(q1 - samp(V, s_ - D, yol)))) > 1e-3:
                        uyari.append("%s %s: gecis aninda %.1f mm sicrama" % (ad, yol, 1000.0 * float(_np.max(_np.abs(q1 - samp(V, s_ - D, yol))))))
                    for t in TT2:
                        if t < s_: out.append(samp(V, t, yol))
                        elif yol == "rotation": out.append(qn(qmul(qmul(samp(V, t - D, yol), q0i), q1)))
                        else: out.append(samp(V, t - D, yol))
            elif g_ == "robot":
                t_b = 6.9
                for t in TT2:
                    if t < t_b: out.append(samp(V, t, yol))
                    elif t < D: out.append(samp(V, t_b, yol))
                    elif t - D < 3.0:
                        u_ = (t - D) / 3.0; u_ = u_ * u_ * (3.0 - 2.0 * u_)
                        out.append(samp(V, t_b, yol) + (samp(V, 3.0, yol) - samp(V, t_b, yol)) * u_)
                    else: out.append(samp(V, t - D, yol))
            elif g_ == "qr":
                out = [samp(V, max(0.0, t - D), yol) for t in TT2]
            elif g_ in ("e", "urun1"):
                out = [samp(V, t if t < T_H1 else (T_H1 if t < T_H1 + D else t - D), yol) for t in TT2]
            else:
                continue
            yeni.append((ad, TT2, [tuple(float(c) for c in v_) for v_ in out], yol))
        src = {(ad, yol): V for ad, yol, V in ch}
        for l2 in L2_ADLAR:
            for yol in ("translation", "rotation", "scale"):
                V = src[("URUN__" + l2, yol)]; out = []
                for t in TT2:
                    if t < D:
                        out.append(_np.array([1e-4] * 3) if yol == "scale" else V[0])
                    else:
                        v_ = samp(V, t - D, yol).copy()
                        if yol == "translation" and t - D >= T_H1 - 2.0: v_[1] += 0.003     # 2. lahmacun kutuda 1.'nin 3 mm üstünde
                        out.append(v_)
                yeni.append(("URUN__L2_" + l2, TT2, [tuple(float(c) for c in v_) for v_ in out], yol))
        print("   v66 · IKI LAHMACUN uyari %d%s" % (len(uyari), (": " + " | ".join(uyari[:6])) if uyari else ""))
        assert not [u_ for u_ in uyari if "basliyor" in u_], "v66: iki cevrim ust uste biniyor: %s" % uyari[:3]
        return yeni, D, T2
    def iki_adim(adim, D):
        a1, a2 = [], []
        for a in adim:
            if a["ad"] in ("ROBOT → QR", "QR DOLABI"):
                a2.append(dict(t=round(a["t"] + D, 2), ad=a["ad"], not_=a["not_"])); continue
            n1 = n2 = a["not_"]
            if a["ad"] == "KUTU":
                n1 = "1. lahmacun katlanmış kutuya girer; kutunun kapağı AÇIK kalır, kutu makinesi 2. lahmacunu bekler."
                n2 = "2. lahmacun ilkinin üstüne girer; kol + piston kapağı kapatıp bastırır. Kutuda 2 lahmacun."
            if a["ad"] == "ÇEKMECE":
                n2 = "Robot 2. lahmacun topunu aynı çekmeceden alır (tabla açıcıya dönmüş)."
            a1.append(dict(t=a["t"], ad=a["ad"] + " (1)", not_=n1)); a2.append(dict(t=round(a["t"] + D, 2), ad=a["ad"] + " (2)", not_=n2))
        return sorted(a1 + a2, key=lambda x_: x_["t"])
    for _n, (_nm, _A) in enumerate(ANIM_SIP):
        if _nm == "siparis_lahmacun":
            _A2, _D, _T2 = iki_lahmacun(_A, LAH_Z)
            ANIM_SIP[_n] = (_nm, _A2)
            _sd = [s_ for s_ in SIP_DURUM if s_["kod"] == "lahmacun"][0]
            _sd["adim"] = iki_adim(_sd["adim"], _D); _sd["sure"] = _T2; _sd["ad"] = "Lahmacun (2 adet)"
        else:
            _TT = _A[0][1]
            _h0 = [a_ for a_ in _A if a_[0] == "URUN__hamur" and (a_[3] if len(a_) > 3 else "translation") == "translation"][0][2][0]
            for _ad in L2_ADLAR:
                _A.append(("URUN__L2_" + _ad, _TT, [_h0] * len(_TT), "translation"))
                _A.append(("URUN__L2_" + _ad, _TT, [(0.0, 0.0, 0.0, 1.0)] * len(_TT), "rotation"))
                _A.append(("URUN__L2_" + _ad, _TT, [(1e-4,) * 3] * len(_TT), "scale"))
    assert len(set(tuple(sorted((k_[0], k_[3] if len(k_) > 3 else 'translation') for k_ in a_)) for _n, a_ in ANIM_SIP)) == 1, "v65: siparis animasyonlarinin dugum kumesi ayni olmali"
    print("ANA MONTAJ ANIMASYONU (v58): tek tam dongu %.0f sn · %d kanal · %d adim · %d eksenli doner dugum" % (T_J, len(ANIM_HAT), len(ADIM_HAT), len(OZEL_T)))
    print("SAPMA DENETIMI (kareler arasi, glTF ara degerleme <-> tam kinematik): en kotu 15 / %d dugum" % len(SAPMA))
    for e_, t_, a_ in SAPMA[:15]: print("   %8.2f mm  t=%6.2f  %s" % (e_, t_, a_))
    _kotu = [r for r in SAPMA if r[2].startswith("TOPPING_DONER__") and r[0] > 3.0]   # 3 mm: spiral sonundaki x hızı sıçraması (eksen değil)
    assert not _kotu, "TOPPING donen dugumu ekseninden kayiyor: %s" % _kotu[:3]
    _kotu = [r for r in SAPMA if r[2].startswith("F_DONER__") and r[0] > 3.0]
    assert not _kotu, "firin / giris bandi rulosu ekseninden kayiyor: %s" % _kotu[:3]

    # ================= v48 · FIRIN DENETİMİ: gerçek katı kesişimi (mm³) + ürün yolu taraması =================
    def _hacim(a_, b_):
        try: return a_.intersect(b_).Volume()
        except Exception: return -1.0
    def _bbk(a_, b_):
        A_, B_ = a_.BoundingBox(), b_.BoundingBox()
        return A_.xmin < B_.xmax and B_.xmin < A_.xmax and A_.ymin < B_.ymax and B_.ymin < A_.ymax and A_.zmin < B_.zmax and B_.zmin < A_.zmax
    def _tek(wp):
        v = wp.vals() if hasattr(wp, "vals") else [wp]
        return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])
    _F = [(p["birim"] + ":" + p["ad"], FT.dunya(p)) for p in FT.PARCALAR]
    _DG = []
    TC.PARCALAR[:] = []; TC.modul()
    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"] in KAPAK or p["ad"] in AKTARMA_TP10 or not v1_kalir(p["ad"]):
            continue
        _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = p["wp"].val().translate(cq.Vector(X_BC + _d[0], Y_MEK + _d[1], _d[2]))
        if p["ad"] == "cikis_yarigi_contasi": sh = YARIK_V2
        if sh.BoundingBox().xmax > 2440.0: _DG.append(("TOPPING:" + p["ad"], sh))
    _TABLA = [p for p in TC.PARCALAR if grup_modul(p["ad"]) == "TABLA"]
    for p in _TABLA:                                                                     # tabla AKTARMA KONUMUNDA (dinamik)
        _DG.append(("TOPPING(aktarmada):" + p["ad"], p["wp"].val().translate(cq.Vector(X_BC + TH.X_AKTARMA - TC.XC_TABLA, Y_MEK, 0.0))))
    for q in TU.P:
        if q["ad"].startswith(V3_CIKAN): continue
        sh = q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))
        if sh.BoundingBox().xmax > 2440.0: _DG.append(("TOPPING2:" + q["ad"], sh))
    for p in KS.PARCALAR:
        if p["grup"] in K_HARIC_GRUP: continue
        sh = _tek(p["wp"]).translate(cq.Vector(X_K, 0.0, 0.0))
        if sh.BoundingBox().xmin < 4330.0: _DG.append(("K:" + p["ad"], sh))
    for _rota in (ANA_V44, ANA_K48):
        _an = TU.boru(_rota, 5.0); _an = _an.val() if hasattr(_an, "val") else _an
        _DG.append(("HAVA:ana_hat", _an.translate(cq.Vector(X_BC, 0.0, 0.0))))
    for q in TU.P:                                                                       # kompresör fırın üstünde (rafın üstü)
        if q["ad"].startswith("kompresor_"): _DG.append(("HAVA:" + q["ad"], q["sh"].translate(cq.Vector(X_BC + KOMP_KAY[0], KOMP_KAY[1], KOMP_KAY[2]))))
    for b in B:
        if b["modul"] == "D" and b["durum"] in ("KUTU", "KATALOG") and not b["kod"].startswith("D_SUPURGELIK"):
            _DG.append(("D:" + b["kod"], kutu_kat(b).val()))
    for p in BM.PARCALAR:                                                                # v53: bulaşık makinesi gerçek parçaları
        _DG.append(("BULASIK:" + p["ad"], BM.dunya(p)))
    _cak = []
    for a_, sa in _F:
        for c_, sc in _DG:
            if _bbk(sa, sc):
                v_ = _hacim(sa, sc)
                if v_ > 1.0 or v_ < 0: _cak.append((round(v_, 1), a_, c_))
    for i_, (a_, sa) in enumerate(_F):
        for c_, sc in _F[i_ + 1:]:
            if _bbk(sa, sc):
                v_ = _hacim(sa, sc)
                if v_ > 1.0 or v_ < 0: _cak.append((round(v_, 1), a_, c_))
    _CER = [x_ for x_ in _DG if x_[0] == "TOPPING:cikis_yarigi_contasi"][0]              # yeni çerçeve ↔ TOPPING (tabla aktarmada dahil)
    for c_, sc in _DG:
        if c_ == _CER[0] or not c_.startswith("TOPPING"): continue
        if _bbk(_CER[1], sc):
            v_ = _hacim(_CER[1], sc)
            if v_ > 1.0 or v_ < 0: _cak.append((round(v_, 1), _CER[0] + "(v2)", c_))
    _KOMP = [x_ for x_ in _DG if x_[0].startswith("HAVA:kompresor")]                     # kompresör ↔ raf üstündeki komşular (kutu yedeği kutusu, davlumbaz)
    for a_, sa in _KOMP:
        for c_, sc in _DG:
            if c_.startswith("HAVA:") or c_.startswith("D:D_DAVLUMBAZ") is False and not c_.startswith("D:"): continue
            if _bbk(sa, sc):
                v_ = _hacim(sa, sc)
                if v_ > 1.0 or v_ < 0: _cak.append((round(v_, 1), a_, c_))
    print("FIRIN CAKISMA (gercek kati kesisimi > 1 mm3 · TOPPING + tabla aktarmada + K + hava + kompresor + F kutulari + kendi arasinda + yeni cerceve): %s"
          % ("TEMIZ" if not _cak else "%d BULGU" % len(_cak)))
    for x_ in sorted(_cak, reverse=True)[:40]: print("   %10.1f mm3  %s  <->  %s" % x_)
    _YOL = []
    _stat = [(a_, sa) for a_, sa in _F] + [(c_, sc) for c_, sc in _DG if c_.startswith(("K:", "TOPPING"))]
    IT.kur(IT.S_HOME, True)
    _stat += [("ITICI(ev):" + p["ad"], IT.dunya(p)) for p in IT.PARCALAR if p["grup"] != "KOL"]                 # v49: itici sabitleri + araba evde (çubuk hariç: ürünle birlikte gider)
    _kon = [(IT.C0[0] + (IT.C1[0] - IT.C0[0]) * k_ / 17.0, IT.C0[1] + (IT.C1[1] - IT.C0[1]) * k_ / 17.0, R_) for R_ in (139.5, 149.5) for k_ in range(18)]   # v49: çapraz itme 10 mm adım
    _kon += [(float(x_), FT.urun_z(float(x_)), R_) for R_ in (139.5, 149.5) for x_ in range(2510, 4301, 10)]
    def _alt(xc, R_):                                                               # rijit ürün diski: ayak izinin altındaki EN YÜKSEK yüzeyin 0,5 üstü
        if xc - R_ <= 2507.0: return P + 0.5                                        # v51: rijit ürün arka kenarı DİSK KENARINI (2507) geçene kadar diskte (v50: 2492 = çerçeve; düz yolda disk sliverine giriyordu)
        if xc - R_ <= FT.BANT_X[1]: return FT.BANT_UST_HAT + 0.5
        if xc - R_ <= FT.OLU_X[1]: return KS.BANT + 2.0
        return KS.BANT + 0.5
    for xc, zc, R_ in _kon:
        y_ = _alt(xc, R_)
        cyl = cq.Solid.makeCylinder(R_, 28.0, cq.Vector(xc, y_, zc), cq.Vector(0, 1, 0))
        for a_, sa in _stat:
            if _bbk(cyl, sa):
                v_ = _hacim(cyl, sa)
                if v_ > 5.0 or v_ < 0: _YOL.append((int(round(xc)), round(zc, 1), round(v_, 1), "Ø%.0f %s" % (2 * R_ + 1, a_)))
    _n280 = len([k_ for k_ in _kon if k_[2] < 145]); _n300 = len(_kon) - _n280
    print("FIRIN URUN YOLU (O280 %d konum + O300 zarf %d konum · 28 yuksek · 10 mm adim · DUZ −170: disk + yarik + on oda + firin + K → 4300 · v51 kayma yok, cit yok): %s"
          % (_n280, _n300, "TEMIZ" if not _YOL else "%d BULGU" % len(_YOL)))
    for x_ in _YOL[:40]: print("   x %d  z %.1f  %.1f mm3  %s" % x_)
    # TOPPING teknesi modülün içinde mi (v24)
    _tx = max(p["wp"].val().BoundingBox().xmax for p in TC.PARCALAR if not p["ad"].startswith("_bom") and v1_kalir(p["ad"]) and p["ad"] not in AKTARMA_TP10 and grup_modul(p["ad"]) not in ("TABLA", "ARABA"))
    print("TOPPING SABIT PARCALARIN SAG UCU: x %.1f (dunya %.1f) · duvar 2500 → %s" % (_tx, _tx + X_BC, "ICERIDE" if _tx + X_BC <= 2500.0 else "TASIYOR"))
    assert _tx + X_BC <= 2500.0, "TOPPING sabit parcasi 2500'u geciyor"
    FIRIN_OZET = ("gerçek katı kesişimi %s (%d fırın/uyarlama parçası × %d komşu parça + yeni çerçeve + kompresör) · ürün yolu %s (Ø280 %d + Ø300 %d konum) · TOPPING sabit parçaları 2500'ün içinde (%.0f)"
                  % ("TEMİZ" if not _cak else "%d BULGU" % len(_cak), len(_F), len(_DG), "TEMİZ" if not _YOL else "%d BULGU" % len(_YOL), _n280, _n300, _tx + X_BC))
    assert not _cak and not _YOL, "v48: cakisma / urun yolu bulgusu var"
    # ================= v49 · İTİCİ DENETİMİ =================
    _DGI = []
    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"] in KAPAK or p["ad"] in AKTARMA_TP10 or not v1_kalir(p["ad"]) or grup_modul(p["ad"]) == "TABLA": continue
        _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = p["wp"].val().translate(cq.Vector(X_BC + _d[0], Y_MEK + _d[1], _d[2]))
        if p["ad"] == "cikis_yarigi_contasi": sh = YARIK_V2
        if sh.BoundingBox().xmax > 1900.0: _DGI.append(("TOPPING:" + p["ad"], sh))
    for p in _TABLA:
        for _ad_, _xk in (("park", TC.XC_TABLA), ("aktarma", TH.X_AKTARMA)):
            _DGI.append(("TABLA(%s):%s" % (_ad_, p["ad"]), p["wp"].val().translate(cq.Vector(X_BC + _xk - TC.XC_TABLA, Y_MEK, 0.0))))
    for q in TU.P:
        if q["ad"].startswith(V3_CIKAN): continue
        sh = q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))
        if sh.BoundingBox().xmax > 1900.0: _DGI.append(("TOPPING2:" + q["ad"], sh))
    _DGI += [(a_, sa) for a_, sa in _F if sa.BoundingBox().xmin < 2700.0]
    _DGI += [(c_, sc) for c_, sc in _DG if c_.startswith("K:")]
    _cak_it = []
    for _kon_, _s_, _kal_ in (("EV", IT.S_HOME, True), ("SON", IT.S_END, False), ("ORTA", (IT.S_HOME + IT.S_END) / 2.0, False)):
        IT.kur(_s_, _kal_)
        for p in IT.PARCALAR:
            sa = IT.dunya(p)
            for c_, sc in _DGI:
                if _bbk(sa, sc):
                    v_ = _hacim(sa, sc)
                    if v_ > 1.0 or v_ < 0: _cak_it.append((round(v_, 1), "ITICI(%s):%s" % (_kon_, p["ad"]), c_))
    # pide geliş koridoru (park → aktarma, Ø300 × 28 + topping 5) ve disk süpürmesi ↔ itici (evde, kalkık) + destek
    IT.kur(IT.S_HOME, True)
    _kor = FT.kut(X_BC + TC.XC_TABLA - 150.0, IT.C0[0] + 150.0, P, P + 33.0, ZT - 150.0, ZT + 150.0).val()
    _disk = FT.kut(X_BC + TC.XC_TABLA - 170.0, IT.C0[0] + 170.0, P - 14.0, P, ZT - 170.0, ZT + 170.0).val()
    for p in IT.PARCALAR:
        sa = IT.dunya(p)
        for _ad_, _sw in (("PIDE KORIDORU", _kor), ("DISK SUPURMESI", _disk)):
            if _bbk(sa, _sw):
                v_ = _hacim(sa, _sw)
                if v_ > 1.0 or v_ < 0: _cak_it.append((round(v_, 1), "ITICI(ev):" + p["ad"], _ad_))
    # çubuk itme süpürmesi: inik çubuk 20 mm adımla (temas → son) ↔ TOPPING/F/K sabitleri (tabla aktarmada)
    _sup = 0
    for _s_ in [IT.S_TEMAS + 20.0 * i_ for i_ in range(int((IT.S_END - IT.S_TEMAS) // 20.0) + 1)] + [IT.S_END]:
        IT.kur(_s_, False); _sup += 1
        for p in IT.PARCALAR:
            if p["grup"] not in ("KOL", "ARABA"): continue
            sa = IT.dunya(p)
            for c_, sc in _DGI:
                if c_.startswith("TABLA(park)"): continue
                if _bbk(sa, sc):
                    v_ = _hacim(sa, sc)
                    if v_ > 1.0 or v_ < 0: _cak_it.append((round(v_, 1), "ITICI(s=%.0f):%s" % (_s_, p["ad"]), c_))
    IT.kur(IT.S_HOME, True)
    print("ITICI DENETIMI (gercek kati kesisimi > 1 mm3 · ev/son/orta ↔ TOPPING + tabla park/aktarma + F + K · pide koridoru · disk supurmesi · itme supurmesi %d konum): %s"
          % (_sup, "TEMIZ" if not _cak_it else "%d BULGU" % len(_cak_it)))
    for x_ in sorted(_cak_it, reverse=True)[:40]: print("   %10.1f mm3  %s  <->  %s" % x_)
    ITICI_OZET = ("itici ↔ TOPPING (tabla park + aktarma) + fırın + K gerçek katı kesişimi %s (ev · son · orta) · pide geliş koridoru ve disk süpürmesi temiz · inik çubuk itme süpürmesi %d konum · ürün yolu düz −170 (18 + bantlar)"
                  % ("TEMİZ" if not _cak_it else "%d BULGU" % len(_cak_it), _sup))
    assert not _cak_it, "v49: itici cakismasi var"
    print("FIRIN YERLESIM: gövde %.0f–%.0f · ön oda %.0f–%.0f · giriş duvarı %.0f–%.0f · ISITILAN %.0f–%.0f = %.0f (aynı anda %d ürün, adım %.0f) · çıkış duvarı %.0f–%.0f · bant uçtan uca %.0f–%.0f (üst %.0f) · rulolar %.0f / %.0f · gövde y %.0f–%.0f · v51: fırın +%.0f z (çıkıntı 0…+%.0f, F modülü %.0f derin) · K çiti YOK"
          % (FT.X_F0, FT.X_F1, FT.X_F0, FT.X_DUV0, FT.X_DUV0, FT.X_TUN0, FT.X_TUN0, FT.X_TUN1, FT.ODA, FT.N_URUN, FT.ADIM, FT.X_TUN1, FT.X_F1, FT.BANT_X[0], FT.BANT_X[1], FT.BANT_UST_HAT, FT.RULO_X[0], FT.RULO_X[1], FT.YG0, FT.YG1, FT.ZS, FT.ZS, DZ + FT.ZS))

    # ================= v57 · ALÇAK HAT ARAYÜZ DENETİMLERİ (gerçek katı kesişimi > 1 mm³) =================
    def _kaynak_tek(sh):
        """compound içinde üst üste binen katılar (boru parçaları + dirsek küreleri) → tek katı (OCC kendi-kesişen argüman tuzağı · denetci_yeni_v1)"""
        ss_ = sh.Solids()
        if len(ss_) <= 1: return sh
        r_ = ss_[0]
        for x_ in ss_[1:]: r_ = r_.fuse(x_)
        return r_.clean()
    def _capraz(A_, B_, esik=1.0):
        A_ = [(a_, sa, sa.BoundingBox()) for a_, sa in A_]; B_ = [(c_, sc, sc.BoundingBox()) for c_, sc in B_]
        out = []
        for a_, sa, X_ in A_:
            for c_, sc, Y_ in B_:
                if X_.xmin < Y_.xmax and Y_.xmin < X_.xmax and X_.ymin < Y_.ymax and Y_.ymin < X_.ymax and X_.zmin < Y_.zmax and Y_.zmin < X_.zmax:
                    v_ = _hacim(sa, sc)
                    if v_ > esik or v_ < 0: out.append((round(v_, 1), a_, c_))
        return out
    _SCP = [("B:" + p["birim"] + ":" + p["ad"], _tek(p["wp"])) for p in SC.PARCALAR]
    _SCB = {a_: sb.BoundingBox() for a_, sb in _SCP}
    # 1 · FIRIN ↔ ÇEKMECELİ DOLAP: fırın dolabın düz üstüne (788) oturur, hiçbir dolap parçasına girmez
    _fir_alt = min(sa.BoundingBox().ymin for _a, sa in _F)
    _gov_alt = min(FT.dunya(p).BoundingBox().ymin for p in FT.PARCALAR if p["birim"] == "F_TP10_GOVDE")
    _dol_ust = max(bb_.ymax for bb_ in _SCB.values())
    _c1 = _capraz(_F, [(a_, sb) for a_, sb in _SCP if _SCB[a_].xmax > FT.X_F0 - 1.0 and _SCB[a_].ymax > Y_DUZ - 5.0])
    _ok1 = not _c1 and abs(_gov_alt - Y_DUZ) < 0.05 and _fir_alt >= Y_DUZ - 0.05 and abs(_dol_ust - Y_DUZ) < 0.05
    print("FIRIN ↔ CEKMECELI DOLAP (v57 · firin dolabin duz ustune oturur · %d firin × %d dolap parcasi, cekmeceler kapali): firin en alt %.2f · govde alti %.2f · dolap ustu %.2f (= %.0f) · kesisim %s  %s"
          % (len(_F), len(_SCP), _fir_alt, _gov_alt, _dol_ust, Y_DUZ, "YOK" if not _c1 else "%d BULGU" % len(_c1), _gk(_ok1)))
    for x_ in sorted(_c1, reverse=True)[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
    assert _ok1, "v57: firin ↔ cekmeceli dolap"
    print("   BILGI · robot copu klapesi ust kenari %.0f · firin cikintisi alti %.0f (z 0…+%.0f) → robot eli icin %.0f mm (denetci: robot tarafinda bakilacak)" % (SC.KLAPE_AC[3], FT.YG0, FT.ZS, FT.YG0 - SC.KLAPE_AC[3]))
    # 2 · KAİDE ↔ TOPPING (TC + açıcı + tabla aktarmada + TU) ve ↔ ÇEKMECELİ DOLAP
    _KDP = [("KAIDE:" + p["ad"], KD.dunya(p)) for p in KD.PARCALAR]
    _TCT = []
    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"] in KAPAK or p["ad"] in AKTARMA_TP10 or not v1_kalir(p["ad"]): continue
        _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = YARIK_V2 if p["ad"] == "cikis_yarigi_contasi" else p["wp"].val().translate(cq.Vector(X_BC + _d[0], Y_MEK + _d[1], _d[2]))
        _TCT.append(("TOPPING:" + p["ad"], sh))
    for p in _TABLA:
        _TCT.append(("TOPPING(aktarmada):" + p["ad"], p["wp"].val().translate(cq.Vector(X_BC + TH.X_AKTARMA - TC.XC_TABLA, Y_MEK, 0.0))))
    _TUT = [("TOPPING2:" + q["ad"], q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))) for q in TU.P if not q["ad"].startswith(V3_CIKAN)]
    _c2 = _capraz(_KDP, _TCT + _TUT)
    _c3 = _capraz(_KDP, [(a_, sb) for a_, sb in _SCP if _SCB[a_].ymax > Y_DUZ - 5.0 and _SCB[a_].xmin < X_BC + W_BC])
    _tc_alt = min(sh.BoundingBox().ymin for a_, sh in _TCT if a_.startswith("TOPPING:") and not a_.startswith("TOPPING:onyuz_"))   # v63: ön kapaklar kaide bandını örter
    _tu_alt = min(sh.BoundingBox().ymin for _a, sh in _TUT)
    _kdb = cq.Compound.makeCompound([sa for _a, sa in _KDP]).BoundingBox()
    _ok2 = not _c2 and not _c3 and _tc_alt >= Y_MEK - 0.05 and _tu_alt > Y_MEK and abs(_kdb.ymin - Y_DUZ) < 0.05
    print("KAIDE (kaide_cad_v2 · %d parca · y %.1f-%.1f) ↔ TOPPING (TC %d parca + tabla aktarmada, acici dahil + TU %d): %s · ↔ CEKMECELI DOLAP: %s · TC en alt %.2f ≥ %.0f · TU en alt %.2f  %s"
          % (len(_KDP), _kdb.ymin, _kdb.ymax, len(_TCT), len(_TUT), "YOK" if not _c2 else "%d BULGU" % len(_c2), "YOK" if not _c3 else "%d BULGU" % len(_c3), _tc_alt, Y_MEK, _tu_alt, _gk(_ok2)))
    for x_ in sorted(_c2 + _c3, reverse=True)[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
    assert _ok2, "v57: kaide ↔ TOPPING / dolap"
    # 3 · S MODÜLÜ (QR + tezgâh) + RAY EKLERİ ↔ birbiri + robot / ray birimleri (FR5 montaj konumunda)
    _QRP = [("QR:" + p["ad"], QR.dunya(p)) for p in QR.PARCALAR]
    _TZP = [("TEZGAH:" + p["ad"], TZ.dunya(p)) for p in TZ.PARCALAR]
    _REP = [("RAY_EK:" + p["ad"], _kaynak_tek(RE.dunya(p)) if p["ad"].startswith("robot_kablosu_") else RE.dunya(p)) for p in RE.PARCALAR]
    _ROB = [("KUTU:" + b["kod"], kutu_kat(b).val()) for b in B if b["kod"] in ("ROBOT_RAY", "ROBOT_1", "ROBOT_1_KOL")]
    _c4 = _capraz(_QRP, _TZP + _REP) + _capraz(_TZP, _REP) + _capraz(_QRP + _TZP + _REP, _ROB)
    print("S + RAY EKLERI (QR %d · tezgah %d · ray ekleri %d parca, robot kablosu birlesik) ↔ birbiri + robot/ray birimleri (FR5 x %.0f): %s  %s"
          % (len(_QRP), len(_TZP), len(_REP), RX, "YOK" if not _c4 else "%d BULGU" % len(_c4), _gk(not _c4)))
    for x_ in sorted(_c4, reverse=True)[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
    assert not _c4, "v57: QR / tezgah / ray ekleri cakisiyor"
    print("   BILGI · enerji zinciri yalniz robot x %.0f icin modellendi (U kol y 2-342): yolculukta SABIT · dik U zincir ↔ acik cekmeceler (K1 lahm 1-2 erisilemez, 5 cekmece yalniz soldan) ACIK KONU (denetci) — karar Kemal'de" % RE.RX_MONTAJ)
    # 4 · QR GÖZ YOLU: kutu (320 × 320 × en yüksek duvar) çatal çekişinden göze kadar 0,1 s adımla ↔ QR parçaları (göz kapağı animasyondaki açıklıkta)
    _qh = qr_hedef(); _gq = _qh["grup"]; _pv, _ax, _ac = _qh["mentese"]
    _QS = [(p["ad"], QR.dunya(p), p["grup"]) for p in QR.PARCALAR]
    _yol_c, _yol_n, t_ = [], 0, QR_YOL["t"][0]
    while t_ <= QR_YOL["t"][1] + 1e-9:
        cx_, cy_, cz_ = QR_YOL["kutu"](t_)
        kb_ = FT.kut(cx_ - _qh["yari"], cx_ + _qh["yari"], cy_, cy_ + _qh["hk"], cz_ - _qh["yari"], cz_ + _qh["yari"]).val()
        a_ = _ac * QR_YOL["kapak"](t_)
        for ad_, sh_, gr_ in _QS:
            if gr_ == _gq and abs(a_) > 1e-6: sh_ = sh_.rotate(cq.Vector(*_pv), cq.Vector(*_pv) + cq.Vector(*_ax), a_)
            if _bbk(kb_, sh_):
                v_ = _hacim(kb_, sh_)
                if v_ > 1.0 or v_ < 0: _yol_c.append((round(t_, 2), round(v_, 1), ad_))
        t_ += 0.1; _yol_n += 1
    _son = QR_YOL["kutu"](QR_YOL["t"][1])
    print("QR GOZ YOLU (kutu %.0f × %.0f × %.0f · %d an · catal cekisi → x/y hizalama → z ile goze · kapak animasyondaki aciklikta) ↔ QR parcalari: %s · son yer x %.1f · alt %.1f · z %.1f (hedef %.1f / %.1f / %.1f)  %s"
          % (2 * _qh["yari"], _qh["hk"], 2 * _qh["yari"], _yol_n, "YOK" if not _yol_c else "%d BULGU %s" % (len(_yol_c), _yol_c[:6]),
             _son[0], _son[1], _son[2], _qh["kx"], _qh["ky"], _qh["kz"], _gk(not _yol_c and abs(_son[0] - _qh["kx"]) < 0.05 and abs(_son[1] - _qh["ky"]) < 0.05 and abs(_son[2] - _qh["kz"]) < 0.05)))
    assert not _yol_c and abs(_son[0] - _qh["kx"]) < 0.05 and abs(_son[1] - _qh["ky"]) < 0.05 and abs(_son[2] - _qh["kz"]) < 0.05, "v57: kutu QR yolunda carpiyor / hedefe varmiyor"

    # ---- v52 · ŞEFFAF İSTASYON YÜZEYLERİ (Kemal 27 Eyl: "şeffaf olarak her istasyonun ön hariç tüm yüzeylerini koy, eşitlik ilkesine dikkat et") ----
    # EŞİTLİK: her istasyona aynı kural — sol · sağ · arka · üst · alt, 1,5 mm, kendi zarfının İÇİNDE (biri içeride biri dışarıda yok);
    # arka hep z −830, ön yok; üst 1862 (B: 788), alt 123 (A/C/F: 788 · v57 alçak hat). Yan/üst/alt z −828,5…0, arka tam kapak → köşeler aynı.
    # Geçiş ağızları gerçek saclardan: C→F fırın giriş yarığı (YARIK_V2 dış çerçeve) · F→K kesme sol sac ağzı · K→E E_PENCERE.
    # F yanlarında fırın gövdesinin kendi kabuğu yüzeydir (çakışan bölge açılır). Yalnız görsel: denetimlere girmez.
    SEF_T = 1.5
    SEF_IST = (("A", X_A, X_A + W_A, Y_DUZ, H_MAK), ("C", X_BC, X_BC + W_BC, Y_DUZ, H_MAK), ("B", X_A, X_A + W_B, Y_ALT, Y_DUZ),
               ("D", X_D, X_D + W_D, Y_DUZ, H_MAK), ("K", X_K, X_K + W_K, Y_ALT, H_MAK), ("E", X_E, X_E + W_E, Y_ALT, H_MAK))   # v57 alçak hat · S (koridorda) paneli YOK
    _yk = tuple(FT.YARIK_V2[0][2:]); _ka = tuple(KS.URUN_GIRISI)                                            # v57: F→K ağzı kesme_cad_v6'ten (v4 ile aynı, 932–1072)
    SEF_AGIZ = {("C", "sag"): _yk, ("D", "sol"): _yk, ("D", "sag"): _ka, ("K", "sol"): _ka, ("K", "sag"): tuple(KS.E_PENCERE), ("E", "sol"): tuple(KS.E_PENCERE)}
    SEF_ATLA = {("A", "sag"), ("C", "sol"), ("D", "alt")}   # v57: F altı paneli fırın gövdesinin altıyla (788) ve dolabın üst paneliyle çakışırdı   # ilk koşu raporu: TOPPING açıcısı + tabla arabası x 700'ün 600 mm soluna uzanıyor → A–C arasında iç duvar YOK
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
                d_.append((xa - 1.0, xb + 1.0, FT.YG0, FT.YG1, -FT.D_TP + FT.ZS, FT.ZS + 1.0))          # fırın kabuğu burada yüzey
            yz.append((taraf, _sef_panel(xa, xb, y0 + SEF_T, y1 - SEF_T, Z0 + SEF_T, FT.ZS, d_)))
        yz.append(("arka", _sef_panel(x0, x1, y0, y1, Z0, Z0 + SEF_T)))
        yz.append(("ust", _sef_panel(x0, x1, y1 - SEF_T, y1, Z0 + SEF_T, FT.ZS)))
        if (m_, "alt") not in SEF_ATLA:                                                  # v57: SEF_ATLA artık alt paneli de atlar (F altı: fırın dolabın üstünde)
            yz.append(("alt", _sef_panel(x0, x1, y0, y0 + SEF_T, Z0 + SEF_T, FT.ZS)))
        mal_ = mal_ad(dict(kod="SEFFAF_YUZEY", modul=m_, mal="seffaf_yuzey"))
        for f_, msh in yz:
            parcalar.append(("%s_SEFFAF__%s" % (m_, f_), msh, mal_)); _sef_n += 1
    print("SEFFAF YUZEY (v52): %d istasyon · %d panel (A–C arası iç duvar yok: TOPPING açıcı + tabla arabası sınırdan geçer) · %.1f mm · arka z %.0f · ust %.0f (B %.0f) · alt %.0f (A/C/F %.0f; F alti yok: firin dolabin ustunde) · on YOK · agizlar C>F, F>K, K>E · F yaninda firin kabugu yuzey"
          % (len(SEF_IST), _sef_n, SEF_T, -DZ, H_MAK, Y_DUZ, Y_ALT, Y_DUZ))
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
    # ---- çıktılar ----
    dokular = dict(DOKU); dokular.update({"ad": doku_ad("AUTOKITCH HAT v1", "%.0f × %.0f × %.0f mm  ·  beyaz = gerçek model  ·  şeffaf = istasyon yüzeyi / henüz kutu" % (HAT_W, H_MAK, DZ), ok_sol=True),
               "montaj": doku_ad("MAKİNE ANA MONTAJI", "birimler tek tek gerçek modele çevriliyor", ok_sol=False)})
    # v61 · ÖLÇEK: makinenin SOLUNDA 180 cm basit insan figürü (Kemal) — denetimlere girmez, yalnız GLB
    MALZEME["insan_180"] = dict(renk=(0.20, 0.45, 0.80, 1.0), met=0.0, ruf=0.8, saydam=False)
    _hx, _hz = -550.0, -300.0
    _ins = cq.Workplane("XY").sphere(115.0).translate((_hx, 1685.0, _hz))                                   # baş · tepe 1800
    for _sx in (-95.0, 95.0):
        _ins = _ins.union(cq.Workplane("XZ").circle(70.0).extrude(-850.0).translate((_hx + _sx, 0.0, _hz)))            # bacaklar 0–850
        _ins = _ins.union(cq.Workplane("XZ").circle(45.0).extrude(-600.0).translate((_hx + 2.5 * _sx, 820.0, _hz)))    # kollar 820–1420
    _ins = _ins.union(cq.Workplane("XY").box(380.0, 620.0, 220.0).translate((_hx, 850.0 + 310.0, _hz)))            # gövde 850–1470
    _ins = _ins.union(cq.Workplane("XZ").circle(55.0).extrude(-110.0).translate((_hx, 1460.0, _hz)))               # boyun 1460–1570
    _ib = _ins.val().BoundingBox()
    assert abs(_ib.ymax - 1800.0) < 0.5 and abs(_ib.ymin) < 0.5, "insan figuru 180 cm degil: %.0f" % (_ib.ymax - _ib.ymin)
    _im = Mesh(); _im.ekle(TC_AG(_ins))
    parcalar.append(("INSAN_180cm__insan_180", _im, "insan_180"))
    PARCA_KUTU["INSAN_180cm"] = [["insan figuru 180 cm (olcek)", 0] + [round(v_, 1) for v_ in (_ib.xmin, _ib.xmax, _ib.ymin, _ib.ymax, _ib.zmin, _ib.zmax)]]
    print("v61 · INSAN FIGURU 180 cm: x %.0f…%.0f (makinenin solunda) · y %.0f–%.0f · z %.0f…%.0f" % (_ib.xmin, _ib.xmax, _ib.ymin, _ib.ymax, _ib.zmin, _ib.zmax))
    b1 = glb_yaz(os.path.join(OUT, "hat_v66.glb"), [x for x in parcalar if x[0] not in HARIC_T], dokular, ozel=OZEL + OZEL_T, animler=ANIM_SIP)   # v46: donenler kendi ekseninde
    # v47 · ÖN YÜZ DENETİMİ: sabit makine düğümleri makinenin ön yüzünü (z 0) geçemez. İstisna: açıcı kafası (bilinen açık
    # konu), koridordaki robot + ray, QR dolabı, çekmeceler (açılır) ve ürün (taşınır).
    _IST = ("ROBOT", "QR", "TEZGAH", "ZEMIN_KANALI", "URUN__")                          # v63: açıcı / koni / çekmece istisnaları KALKTI — hepsi +79 içinde   # v57: S modülü (QR + tezgâh) ve zemin kanalı koridorda
    # İşlevsel dış elemanlar (ölçülü izin; fazlası yakalanır): K kapı menteşeleri 20 × 140 × 22 · K acil stop Ø32 × 16 · E kapı kulpu 70 × 18 × 18
    _IZIN = {}                                                                          # v63: kulp / menteşe / acil stop dışarı çıkmaz
    _on = []
    for a_, m_, _x in parcalar:
        if a_.startswith(_IST) or a_ in HARIC_T or not m_.P:
            continue
        zm = max(q[2] for q in m_.P) / MM
        if zm > FT.ZS + 0.5:                                                                     # v63: tek ön düzlem +79
            _on.append((round(zm, 1), a_))
    print("   izinli dis elemanlar (islevsel): K kapi mentesesi +22 · K acil stop +16 · E kapi kulpu +18 · acici kafasi +180 (acik konu) · v51: FIRIN CIKINTISI +%.0f (x 2500-4000, y %.0f-%.0f, Kemal) · v57: QR / TEZGAH / ZEMIN_KANALI / ROBOT koridorda" % (FT.ZS, FT.YG0, FT.YG1))
    print("ON YUZ DENETIMI (v63: butun makine z <= +79,5 · istisna yok): %s" % ("GECTI" if not _on else "TASAN: %s" % sorted(_on, reverse=True)[:10]))
    assert not _on, "makinenin on yuzunden tasan parca var"
    # ---- v51 · ROBOT ↔ FIRIN ÇIKINTISI: robot birimleri (ray, kaide, kol zarfı) hattın önünde; çıkıntı 0…+79 (x 2500–4000, y 788–1305 · v57) ----
    _rz = [b for b in B if b["kod"] in ("ROBOT_1", "ROBOT_1_KOL", "ROBOT_RAY")]
    _rzmin = min(b["z"][0] for b in _rz)
    print("ROBOT ↔ FIRIN CIKINTISI: robot birimlerinin en on z'si %.0f · cikinti +%.0f → pay %.0f mm (%s; kol zarfi kutu, gercek kol modeli yok)" % (_rzmin, FT.ZS, _rzmin - FT.ZS, "SERBEST" if _rzmin >= FT.ZS + 50.0 else "DAR"))
    assert _rzmin >= FT.ZS + 50.0, "robot birimi firin cikintisina 50 mm'den yakin"
    _cik = FT.kut(FT.X_F0, FT.X_F1, FT.YG0, FT.YG1, 0.0, FT.ZS).val()
    _cik_cak = []
    for p in FT.PARCALAR:                                                                  # çıkıntı bandında yalnız fırın kabuğu/yalıtımı/bandı olmalı; başka modül parçası girmemeli (K, TOPPING x sınırları)
        pass
    for c_, sc in _DG:
        if c_.startswith("D:"): continue
        if _bbk(_cik, sc):
            v_ = _hacim(_cik, sc)
            if v_ > 1.0 or v_ < 0: _cik_cak.append((round(v_, 1), c_))
    print("FIRIN CIKINTISI ↔ KOMSU PARCALAR (TOPPING/K/hava, gercek kati kesisimi): %s" % ("TEMIZ" if not _cik_cak else "%d BULGU %s" % (len(_cik_cak), _cik_cak[:6])))
    assert not _cik_cak, "cikinti bandina komsu parca giriyor"
    # ---- v57 · BULAŞIK MAKİNESİ K ALTINDA (bulasik_cad_v2 · BM.X0/Y0/Z0 = KS.BULASIK_YER): gerçek parçalar ↔ K parçaları + robot çöp kovası · K iç zarfı · v58: deterjan YOK (kesme_cad_v6) → bulaşığın arkası + MEIKO arka payı BOŞ ----
    _BMP = [(p["ad"], BM.dunya(p)) for p in BM.PARCALAR]
    _KSP = [("K:" + p["ad"], _tek(p["wp"]).translate(cq.Vector(X_K, 0.0, 0.0))) for p in KS.PARCALAR if p["grup"] not in K_HARIC_GRUP]
    _KOVA = [("B:" + p["ad"], _tek(p["wp"])) for p in SC.PARCALAR if p["birim"] == "B_COP"]
    _bm_cak = []
    for a_, sa in _BMP:
        for c_, sc in _KSP + _KOVA:
            if _bbk(sa, sc):
                v_ = _hacim(sa, sc)
                if v_ > 1.0 or v_ < 0: _bm_cak.append((round(v_, 1), a_, c_))
    _bmb = cq.Compound.makeCompound([sa for _a, sa in _BMP]).BoundingBox()
    _KIC = ((X_K + 1.5, X_K + W_K - 1.5), (126.0, Y_MEK - 3.0), (-DZ + 1.5, 0.5))      # K iç zarfı: yan saclar arası · K taban sacı üstü 126 … istasyon tabanı altı 889 · arka sacın önü … ön yüz
    # y alt sınırında 1 mm pay: silindirik ayar ayaklarının BoundingBox'ı gevşek (ölçülen 125,5; gerçek katı K alt sacı 123–126 ile çakışmıyor — çakışma denetimi ayrıca TEMİZ)
    _ic = (_KIC[0][0] <= _bmb.xmin and _bmb.xmax <= _KIC[0][1] and _KIC[1][0] - 1.0 <= _bmb.ymin and _bmb.ymax <= _KIC[1][1] and _KIC[2][0] <= _bmb.zmin and _bmb.zmax <= _KIC[2][1])
    _det = [c_ for c_, _s in _KSP if c_.startswith("K:deterjan_")]                     # v58: deterjan / parlatıcı parçası OLMAMALI (kesme_cad_v6)
    print("BULASIK MAKINESI K altinda (bulasik_cad_v2 · %d parca · yer %s) ↔ K parcalari (%d · deterjan/parlatici %d — v58: YOK) + robot cop kovasi (%d): %s · K ic zarfinda (x %.1f-%.1f · y %.1f-%.1f · z %.1f…%.1f ⊂ x %.1f-%.1f · y %.0f-%.0f · z %.1f…%.1f): %s  %s"
          % (len(_BMP), tuple(KS.BULASIK_YER), len(_KSP), len(_det), len(_KOVA), "TEMIZ" if not _bm_cak else "%d BULGU %s" % (len(_bm_cak), _bm_cak[:6]),
             _bmb.xmin, _bmb.xmax, _bmb.ymin, _bmb.ymax, _bmb.zmin, _bmb.zmax, _KIC[0][0], _KIC[0][1], _KIC[1][0], _KIC[1][1], _KIC[2][0], _KIC[2][1], "EVET" if _ic else "HAYIR", _gk(not _bm_cak and _ic and not _det)))
    assert not _bm_cak and _ic and not _det, "v58: bulasik makinesi K parcalarina / kovaya giriyor, K ic zarfindan tasiyor ya da deterjan parcasi kaldi"
    # v58 · bulaşığın ARKASI + MEIKO arka payı (eski kanister rafı + bidonlar + dozaj hortumlarının yeri): K arka sacının önünden makinenin arkasına kadar BOŞ
    _ab = FT.kut(BM.X0, BM.X0 + BM.W, BM.Y0, BM.Y0 + BM.H, -KS.D + KS.SAC, KS.BULASIK_ARKA_PAY[1]).val()
    _ab_k = []
    for c_, sc in _KSP:
        if c_.startswith("K:bulasik_gecis_"): continue                                   # v63: makinenin bağlantı geçişleri (kesme_cad_v6) arka payda olmalı
        if _bbk(_ab, sc):
            v_ = _hacim(_ab, sc)
            if v_ > 1.0 or v_ < 0: _ab_k.append((round(v_, 1), c_))
    print("BULASIGIN ARKASI + MEIKO arka payi (v58 · deterjan yok · x %.1f-%.1f · y %.0f-%.0f · z %.1f…%.0f; arka pay %.0f…%.0f dahil) ↔ K parcalari: %s  %s"
          % (BM.X0, BM.X0 + BM.W, BM.Y0, BM.Y0 + BM.H, -KS.D + KS.SAC, KS.BULASIK_ARKA_PAY[1], KS.BULASIK_ARKA_PAY[0], KS.BULASIK_ARKA_PAY[1],
             "BOS" if not _ab_k else "%d BULGU %s" % (len(_ab_k), _ab_k[:6]), _gk(not _ab_k)))
    assert not _ab_k, "v58: bulasigin arkasinda / MEIKO arka payinda K parcasi var: %s" % _ab_k[:6]
    # ---- v54 · HAVA ANA HATTI (yeniden yollandı) ↔ kutu birimleri + TOPPING yalıtım / teknik saç / teknik zarflar + K parçaları (gerçek katı) ----
    _hv = []
    _HV_ATLA = ("HAVA_KOMPRESOR", "F_DAVLUMBAZ", "F_UST_KABIN", "F_KOMP_AYAK", "F_UST_KAPAK")   # v63: hat üst kabinin yan saclarındaki rakorlardan geçer                                           # hat bilerek davlumbaz bölmesinden geçer
    for _rn, _rota in (("ANA", ANA_V44), ("K_DALI", ANA_K48)):
        _an = TU.boru(_rota, 5.0); _an = (_an.val() if hasattr(_an, "val") else _an).translate(cq.Vector(X_BC, 0.0, 0.0))
        for b in B:
            if b["durum"] in ("KUTU", "KATALOG") and not b["kod"].endswith("_KABIN") and b["kod"] not in _HV_ATLA:
                kb = kutu_kat(b).val()
                if _bbk(_an, kb):
                    v_ = _hacim(_an, kb)
                    if v_ > 1.0 or v_ < 0: _hv.append((round(v_, 1), _rn, b["kod"]))
        for q in TU.P:
            if q["ad"].startswith(("yalitim_blogu", "teknik_")):
                sq = q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))
                if _bbk(_an, sq):
                    v_ = _hacim(_an, sq)
                    if v_ > 1.0 or v_ < 0: _hv.append((round(v_, 1), _rn, "TOPPING:" + q["ad"]))
        for p in KS.PARCALAR:
            if p["ad"].startswith(("sol_sac", "sag_sac", "arka_sac", "ust_sac")): continue    # duvar geçişi: rakor deliği (bilinçli)
            sk = _tek(p["wp"]).translate(cq.Vector(X_K, 0.0, 0.0))
            if _bbk(_an, sk):
                v_ = _hacim(_an, sk)
                if v_ > 1.0 or v_ < 0: _hv.append((round(v_, 1), _rn, "K:" + p["ad"]))
    print("HAVA ANA HATTI (v54 yolu) ↔ kutu birimleri (pizza + icecek yedegi, dolap) + TOPPING yalitim/teknik + K parcalari (gercek kati; K sol duvari rakor deliginden gecer): %s" % ("TEMIZ" if not _hv else "%d BULGU %s" % (len(_hv), _hv[:8])))
    assert not _hv, "hava ana hatti bir birime giriyor"
    _kx, _ky, _kz = BM.kapi_acik_zarf()
    _kap = FT.kut(_kx[0], _kx[1], _ky[0], _ky[1], _kz[0], _kz[1]).val()
    _kap_c = []
    for c_, sc in _KSP + _REP + _QRP + _TZP:
        if _bbk(_kap, sc):
            v_ = _hacim(_kap, sc)
            if v_ > 1.0 or v_ < 0: _kap_c.append((round(v_, 1), c_))
    print("BULASIK KAPAK ACIK ZARFI (x %.1f-%.1f · y %.0f-%.0f · z %.0f…%.0f · K altinda) ↔ K parcalari + ray ekleri + QR + tezgah (gercek kati, bilgi): %s"
          % (_kx[0], _kx[1], _ky[0], _ky[1], _kz[0], _kz[1], "SERBEST [PASS]" if not _kap_c else "%d BULGU %s [FAIL]" % (len(_kap_c), _kap_c[:6])))
    for b in B:
        if b["kod"] in ("ROBOT_RAY", "ROBOT_1", "ROBOT_1_KOL"):
            _yz = b["y"][0] < _ky[1] and _ky[0] < b["y"][1] and b["z"][0] < _kz[1] and _kz[0] < b["z"][1]
            _gx = b["x"][1] - b["x"][0]
            print("KAPAK ACIK ZARFI (x %.0f-%.0f · y %.0f-%.0f · z %.0f…%.0f) ↔ %s (y %.0f-%.0f · z %.0f…%.0f): %s"
                  % (_kx[0], _kx[1], _ky[0], _ky[1], _kz[0], _kz[1], b["kod"], b["y"][0], b["y"][1], b["z"][0], b["z"][1],
                     ("KESISIR (y/z) → robot bu birimiyle x %.0f-%.0f arasindayken kapak ACILMAZ: servis modu kilidi" % (_kx[0] - _gx, _kx[1] + _gx)) if _yz else "SERBEST (robot her konumda)"))
    print("hat_v66.glb · %d dugum · %.0f KB · animasyon %.0f sn" % (len(parcalar), b1 / 1024.0, T_J))
    _usd = [x for x in parcalar if not x[0].startswith("URUN__")]                         # ürün düğümleri yalnız animasyonda (USDZ durağan)
    b2, prim, sorun, _u = usdz_yaz([os.path.join(OUT, "hat_v66.usdz")], "hat_v66", _usd + E_USDZ, dokular)
    print("hat_v66.usdz · %.0f KB · %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI"))
    for x in sorun: print("   HATA:", x)
    # ---- her modul icin AYRI model: istasyon sayfasi kendi modulunu BUYUK gosterir ----
    MODUL_DOSYA = {}
    for mk in ("A", "B", "C", "D", "K", "E", "S", "-"):                                 # v57: + S (SERVİS / TESLİM)
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
        json.dump(dict(hat=dict(w=HAT_W, h=H_MAK, d=DZ + FT.ZS, arka=-DZ, on=FT.ZS, pafta="HAT v66 (28 Eyl) · IKI LAHMACUN BIR KUTUDA (lahmacun siparisi iki cevrim, kutu acik bekler) · v65: SIPARIS ANIMASYONLARI (6 siparis: kasarli · kiymali · kusbasili · sucuklu pide · lahmacun · pizza; cekmeceden QR gozune) · v64: TOPPING DENETIM DUZELTMELERI (kaset yarik dili: soguk oda tabani kapali · katlanir flipper · on kose pivotlu menteseler) · v63: ON DUZLEM +79 · TEMIZ KUTU ISTASYONLAR (SPEC_on_duzlem_v63): butun on yuzler firin on yuzu duzleminde, arka -830 sabit, derinlik 909 · A gercek kabin + robot agzi · firin ustu kabin + duser kapak · TOPPING / K / E kapakli · bulasik ayaksiz tablada · v62: PARCA ETIKETI (parca_kutulari.json · fare durunca parca adi) · v61: ON KAPAKLAR SEFFAF (yalniz gorunum) + solda 180 cm insan figuru + TOPPING yan yalitimi ustle ayni (topping_uno_cad_v14: 60 kalin, on yuz -104) · v60: TOPPING YALITIMI TAM (Kemal: toppingin yan izolasyonlari nerede, alt izolasyonu neden yok): yan PU duvarlari modele girdi (eski filtre dusuruyordu) + topping_uno_cad_v14 soguk odanin altina alt sac 1 + PU 39 (kotlar ayni) · v59: SOGUTMA STANDART DUZEN (Kemal: ogrendigin yeter, coolingde de onlarla yap · hamur firincidan soguk gelemez): B = store_cad_v8 (Secop CU NLE8.8CN 688 W @ -10/32 C · 2 bolge lamelli evaporator + 4 fan 4414 FL · bolmelerde arka hava gecisi · damlama -> gider -> plintte atis kanali + buharlastirma tavasi · firin alti PU yerine hava boslugu + isinim saci · sol yan PU 60) · ACIK: sogutucu hatlari, cerceve isiticisi, havalandirma debisi olcum · v58: ON TARAFLARA KAPAK YOK + DETERJAN YOK (Kemal: deterjanlari makinenin arkasina koyma, simdilik sil · on taraflara kapak koyma): K = kesme_cad_v6 (bulasigin arkasindaki kanister rafi + deterjan/parlatici bidonlari + dozaj hortumlari silindi, K_DETERJAN birimi yok; bulasik yeri ayni, arkasi + MEIKO arka payi BOS) · B = store_cad_v8 ayni (robot copu kapagi + klapesi yerinde, Kemal: robot copu seyleri kalsin) · animasyon: robot topu cekmeceden aciciya tasir (park x cekmecenin acici tarafi, birakis x 700, top-omuz <= 779 denetlenir) · E = kutu_cad_v7 (icecek yedeginin on alt saci kalkti → 6 koli onden acik; onde yalniz sol on dikme + dikey kablo kanali: tek koli duz gecer, koliler yana kaydirilip cekilir) · ACIK: deterjanin yeri, E ust on kapagi (on_ust_kapak) kalsin mi · v57: ALCAK HAT (SPEC_alcak_hat_v57 · ALCAK_HAT_RESIM1_v4 + QR_TEZGAH_v4, Kemal onayli): butun mekanizma 168 asagi · TEK DUZ CIZGI 788 = cekmeceli dolap ustu = A/C kabin tabani = firin alti (basamak yok) · A/C mekanizma tabani 892 (kaide 104, kaide_cad_v2) · disk 1000 · firin bandi 998 · K bandi 996 · E tepsisi 936 · makine ustu 1862 · B = store_cad_v8: tek parca cekmeceli dolap 0-4000 × 123-788, 24 cekmece (pide 160 · lahmacun 432 · icecek 144 · tatli 12), firin altinda PU 60 kalkan + tasiyici cerceve, robot copu seridi 3810-4000 (15 L kova + klape) · F taban dolabi KALKTI: firin (firin_tp10_cad_v8) dolabin ustune oturur · itici_cad_v5 · K = kesme_cad_v4 (taban 892) · K altinda BULASIK MAKINESI x 4108,5-4568,5 (on dikmelerin arasinda) + arkasinda deterjan/parlatici kanisterleri · E = kutu_cad_v5 (tepsi 936, sarjor 462 kutu; kullanilabilir ≈ 432) + icecek yedegi 6 koli E altinda (144 + dolap 144 = 288 = 4 gun) · pizza kutusu 462 + firin ustu 320 = 782 · TOPPING TC yerel 892, TU dunyada bir kez −168 · hava hatti −168 (K dali MS4 1692 + 10) · YENI MODUL S (SERVIS / TESLIM): QR dolabi qr_cad_v1 860 × 520 × 2050 (12 goz 2 × 6, robot kontrol + ana pano + UPS + kilit karti icinde) + personel tezgahi tezgah_cad_v1 · ray ekleri ray_ek_cad_v1 (zincir olugu, enerji zinciri robot x 2650'de sabit, robot kablosu 4 + 11 m, zemin kanali) · robot rayi z 360 · yolculuk: K3 pide cekmecesi → acici → TOPPING → firin → K → E → QR gozu (sutun 1 · satir 3, robot kapagi acilir/kapanir) · ACIK: QR goz tabani catal disi yuvasi, dik U enerji zinciri ↔ acik cekmeceler, tezgah onu 390, sarjor 432 kullanilabilir, soguk yuk hesabi · v56: TOPPING yalitimi yalniz soguk hacmi sarar (uno v11, teknik cep disarida, L PU 30) · icecek 5 koli F dolabinda (3 + 2) · v55: GORSEL: yalitim gorunur (yari saydam), ayirma saci mavi, yedek yiginlari karton · v54: TOPPING yalitim tek dikdortgen + teknik cep ince sac (uno v10) · K tank + pano yukarida, taban bos (kesme v3) · icecek yedegi firin ustu sag 96 + dolapta 24 = 120 (4 gun) · E ayaklari alt rafta 790 (kutu v4) · hava ana hatti yeniden yollandi · v53: BULASIK MAKINESI GERCEK MODEL (bulasik_cad_v2 · MEIKO M-iClean US foy olculeri, 16 parca) · v52: KUTU YEDEGI TEK YERDE firin ustu sol 320 (887 = 3,1 gun) · raf 4 mm 10 takoz · FIRIN KABUGU GORUNUR (cikinti) · SEFFAF ISTASYON YUZEYLERI on haric, esitlik (1,5 mm, arka -830, ust 2030, alt 123) · FIRIN 79 ONE: F = TP10 kesitli 1500 firin v5, govde + konveyor + giris bandi +79 z (cikinti 1500 × 517 × 79, F modulu 909) · urun hatti magazadan kesiciye −170, E −206 · K giris citi YOK · AKTARMA ITICISI itici_cad_v3 (SMC MY1B16-250 DUZ 170, pivotlu cubuk, sabit pimle kalkar; destek plakasi YOK) · havalandirmali raf · kompresor firin ustunde · kutu yedegi 320 firin ustu sol (dolap pizza gozu bos) · TOPPING v24 + v2 v9 (katalog yay/pim, hac 7,0, fitil TAM) · K = kesme_cad_v2 (on kapaklar YOK) · CIPLAK MODEL: yalitim, yan/on/arka saclar, etek ve kabin zarflari gorselde yok (Kemal 27 Eyl) · 1 tam animasyon · B = store_cad_v5 · E = kutu_cad_v3 · alt taban 123 · surec 1168", firin_denetim=FIRIN_OZET, itici_denetim=ITICI_OZET), sayac=sayac, animasyon=dict(sure=T_J, adim=ADIM_HAT), siparis=SIP_DURUM, modul=[dict(kod=k, ad=a, x=[x, x + w], y=list(MODUL_Y[k])) for k, a, x, w in MODUL],
                       dosya=MODUL_DOSYA, birim=[dict(kod=b["kod"], ad=b["ad"], modul=b["modul"], durum=b["durum"], olcu=b["olcu"], x=list(b["x"]), y=list(b["y"]), z=list(b["z"]), mal=mal_ad(b),
                                   kaynak=b["kaynak"], sayfa=b["sayfa"], parca=b.get("parca", 0)) for b in B]), f, ensure_ascii=False)
    with io.open(os.path.join(OUT, "parca_kutulari.json"), "w", encoding="utf-8") as f:
        _PK63 = {k_: ([r_ for r_ in v_ if r_[2] >= X_E - 5.0] if k_.startswith("E_") else v_) for k_, v_ in PARCA_KUTU.items()}   # v63: E-yerel (menteşe düğümü) yinelenen kayıtlar süzülür
        json.dump(dict(birim={b["kod"]: dict(ad=b["ad"], mal=mal_ad(b)) for b in B}, parca=_PK63), f, ensure_ascii=False, separators=(",", ":"))
    print("v62 · parca_kutulari.json: %d birim · %d parca kutusu" % (len(PARCA_KUTU), sum(len(v) for v in PARCA_KUTU.values())))
    assert sum(len(v) for v in PARCA_KUTU.values()) > 1000, "v62: parca kutulari eksik"
    g_ = sum(v for k, v in sayac.items() if k.startswith("GERCEK"))
    print("durum.json yazildi · GERCEK %d / %d birim (%%%.0f) · toplam %.0f sn" % (g_, len(B), 100.0 * g_ / len(B), time.time() - t0))
    sys.stdout.flush(); os._exit(0)
