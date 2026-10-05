# -*- coding: utf-8 -*-
"""h3_govde_ortak_v1 — AUTOKITCH İSTASYON GÖVDESİ ORTAK YARDIMCILARI v1 (2 Eki 2026 · Claude · YEREL · G0 adımı · montaja bağlı DEĞİL)

K pilotundaki (h3_k_sac_v1, denetimi temiz) istasyondan bağımsız yardımcılar buraya taşındı ve parametreli yapıldı; 6 istasyon ajanı aynı
dosyayı paralel kullanır. Bu dosyada İSTASYONA ÖZGÜ SABİT YOK (kot, ölçü, ad listesi istasyon üretecinde kalır). Sac kütüphanesi: h3_sac_v1 (S).
Doğrulama: <scratchpad>/sac_ortak/test_ortak_k_v1.py — K'nın parçaları bu modülle yeniden üretilip h3_k_sac_v1 çıktısıyla hacim / bbox karşılaştırılır.

=====================================================================================================================================
API (imzalar)
=====================================================================================================================================
  Cerceve(ad='yerel', dx=0, dy=0, dz=0)                     modül YEREL → DÜNYA ötelemesi (montaj modülleri yalnız ötelenir)
      .dunya(sh) · .yerel(sh) · .nokta(p) · .gecis(hedef) · .ozet()          ör. Cerceve('K', 4000) · Cerceve('TC', X_BC, Y_MEK) · Cerceve('TU', X_BC)
  Govde(birim, surum, istasyon='?', cerceve=None)           kayıt defteri: SAC · PROF · ELEMAN · KAYNAK · BIRLESIM · ARAYUZ · KULAK · KAPAK · M8 · KARSI_DELIK
      .sac(ad, rol, kabuk=False, doner=None, **k) → S.Sac        (kabuk=True: dış görünür panel → mal 'kabuk' · doner=Kapak: kapakla döner)
      .profil(ad, eksen, a0, a1, c, b=40, t=2, Ro=None, not_='') → Profil
      .eleman(p, mal='celik', doner=None, sabit=None) · .kaynak(p | [p]) · .arayuz(p, karsi, gerek, not_='')
      .ozel(ad, sh, std, tanim, olcu, malzeme='AISI 304', mal='celik', uretim=False, tur='baglanti', meta=None) → parça (kaydetmez)
      .mal(p) · .kapakla_doner(ad) · .doner_guncelle() · .not_(metin)
  Profil(ad, eksen, a0, a1, c, b=40, t=2, Ro=None, birim, kaynak, not_='')   gerçek dış R'li 304 kare boru (EN 10219 · R = 2t)
      .merkez(a) · .duvar_delik(yuz, a, kayma, cap, tip, not_) · .duvar_pencere(yuz, a, kayma, la, lk, r=1, tip, not_)
      .duvar_delik_nokta(yuz, P, cap, ...) · .duvar_pencere_nokta(yuz, P, la, lk, ...)   (P dünya/yerel nokta → a + kayma otomatik)
      .kaynak_bolgesi(yuz, a0, a1) · .kati() · .dfm() · .parca() · .kesim_satiri()
  uc_kaynaklari(ad, nokta, yon_ray, yuzler, b=40, a=2, flat=None, Ro=4, birim) → [kaynak]     kuşak ucu ↔ dikme yüzü köşe kaynakları
  dikme_tapasi(g, profil, uc='ust', t=2, pah=2.5) → S.Sac
  kulak(g, ad, A, stud, u, v, v_cerceve, L_kaynak=25, gen=25, uc=9.75, dis='M5', rol='braket') → (sac, panel, birlesim)
  vida_konumlari(a0, a1, maks=200, uc=40, min_adet=2) · vida_araligi_denetle(konumlar, a0, a1, maks=200, kose=80, min_adet=2, ad='')
  kapak(g, ad, u0, u1, v0, v1, w_dis, w_ic, O=(0,0,0), ex=(1,0,0), ey=(0,1,0), ustte='yatay', punta_u=None, punta_v=None,
        punta_aralik=150, punta_uc=40, acikliklar=(), mal='on_seffaf') → Kapak
      Kapak.kf(u, v, w) · .uv(kenar, s, a, b) · .eksenler(kenar) · .pivot() · .doner · .sabit · .D / .I (dış / iç tava paneli) · .kd / .ki
  aciklik(K, ad, u, v, boy, en, r=0, tip='pencere'|'klape', kasa=True, kasa_ayak=15, kasa_bosluk=0.5, punta_aralik=100)   kapakta pencere / klape açıklığı
  gizli_mentese(g, K, dikme, kenar, konumlar, olcu=None) → [ad]       dikme içi gizli 180° kaldır-çıkar menteşe (MENTESE ölçüleri TEMSİLİ)
  bas_ac(g, K, dikme, kenar, konumlar, a=22, olcu=None) → [ad]        dikme içi bas-aç (push-to-open) + kapakta karşılık plakası
  m8_noktasi(g, etiket, profil, a, yuz, panel, karsi, karsi_kod='?', karsi_t=1.5, vida_boy=25, kayma=0, yer='', cerceve=None) → kayıt
      dikme / kuşak dış duvarında M8 perçin somun + ara pul + yan sacta Ø9 + karşı sacta Ø9 KAYDI + arayüz cıvatası (ISO 4762 + DIN 125)
  govde_parcalari(g, anahtar='wp', hedef=None) → [parça]   montaj sözleşmesi (ad · wp|sh · mal · grup · bom · kaynak · birim · tur · sac · meta)
  uygula(L, yeni, eski_adlar, isaret, onekler=None, rapor=None, etiket='') → L      eski gövdeyi çıkar, yenisini koy (idempotent, assert'li)
  dunya_listesi(L, cerceve) · kapak_dunya(L, cerceve, doner) · dunya_ciftleri(L, cerceve, onek='')
  elk_hedefleri(modul_kodu, elk_json=None) · ad_denetimi(modul_kodu, yeni_adlar, eski_adlar=(), esleme=None, elk_json=None)
  DENETİM: cakisma(A, B, esik=0.5, ayni=False, izin=None) · denetle_sac(g, acinim_klasoru=None) · denetle_profil(g) ·
           arayuz_karsi_delik(g, cerceve, adaylar) · kapak_supurme(g, K, gw, mw=(), nw=(), cerceve, acilar=10–100/10) ·
           denetle(g, cerceve=None, mekanizma=(), komsu=(), bilinen=None, acinim_klasoru=None, abkant=True, supurme=True, acilar=10–100/10,
                   esik=0.5, sup_esik=1.0, log=print, ayrinti=…) → R (R['temiz'] True olmadan montaj YOK) · profil_kesim_listesi(g, yol=None)

İSKELET (istasyon üreteci · örnek)
  import h3_govde_ortak_v1 as GO
  g = GO.Govde('E_GOVDE', 'h3_e_sac_v1', istasyon='E', cerceve=GO.Cerceve('E', X_E))          # parçalar E YERELİNDE kurulur
  d = g.profil('kose_dikmesi_20_42', 'y', 791, 1856.5, (20, 42)); d.kaynak_bolgesi('+x', 862, 892); GO.dikme_tapasi(g, d)
  g.kaynak(GO.uc_kaynaklari('onyuz_kayit_kaynak_orta_42_40', (40, 877, 42), (1, 0, 0), [(0, -1, 0)], birim=g.birim))
  s = g.sac('sol_sac_…', 'dis', kabuk=True); P = s.taban(…); P.flans(…)                       # panel kurgusu istasyonda (h3_sac_v1)
  GO.kulak(g, 'govde_kulak_sol_on_900', P, (1.5, 900, 8), (0, 1, 0), (0, 0, 1), 19.0)
  GO.m8_noktasi(g, 'K_1100_800', d_arka, 1100.0, '-x', P, 'K_GOVDE sag_sac_E_penceresi', karsi_kod='K')
  K = GO.kapak(g, 'onyuz_kapak_E', u0, u1, v0, v1, w_dis=79, w_ic=59)
  GO.gizli_mentese(g, K, d, 'sol', (950, 1360, 1750)); GO.bas_ac(g, K, d_sag, 'sag', (1000, 1430, 1800))
  R = GO.denetle(g, mekanizma=GO.dunya_ciftleri(MEK, g.cerceve), komsu=KOMSU, bilinen={…}); assert R['temiz']
  def uygula_xx(MOD): return GO.uygula(MOD.PARCALAR, GO.govde_parcalari(g), ESKI_GOVDE, 'onyuz_kapak_E_ic_tava', onekler=GOVDE_ONEK, etiket='E')

=====================================================================================================================================
İSTASYON GÖVDE REÇETESİ (her istasyon ajanı bu sırayla kurar — K pilotu: h3_k_sac_v1)
=====================================================================================================================================
0 · ÖNCE  arayüz kotlarını / dış ölçüleri / açıklıkları istasyonun MEVCUT gövdesinden al, DEĞİŞTİRME (ölçü değişirse komşu istasyon sahibine
    koordinatör notu). Modülü YEREL çerçevede kur (mevcut üreteç hangi çerçevedeyse o: K x 0–400 · dünya = + X_K). Mekanizmaya dokunma.
1 · İSKELET (profil iskeletli istasyon) = KAYNAKLI ALT MONTAJ, tek parça gelir.
    · 304 kare boru 40 × 40 × 2 (kararlar) — dar istasyonda 30 × 30 × 2 (K pilotu) SAPMA olarak raporlanır. Dış köşe R = 2t (gerçek R'li katı: Profil).
    · 4 dikme + alt / orta / üst kuşak (ön + arka) + alt / orta yan kuşak. Kuşak uçları dikmeye 90° alın: uc_kaynaklari() yalnız İÇBÜKEY köşe olan
      yüzlere dikiş koyar (dikmeyle aynı düzlemdeki yüz = alın dikişi, taşlanır → katı yok).
    · Delik / pencere yalnız düz yüzde (köşe R'sine taşmaz), boru ucundan ≥ 3, kaynaklı birleşim bölgesinde YOK (Profil.kaynak_bolgesi ile kaydet →
      Profil.dfm denetler) · boy ≤ 6000 · dikme başları 2 mm tapa (dikme_tapasi, köşeler 2,5 pah, çevresi TIG taşlanır).
    · Kendinden taşıyıcı (bükümlü kutu) istasyonlar kutu olarak KALIR; iki kurgu karıştırılmaz.
2 · PANELLER (sökülebilir, servis)
    · Dış kabuk 1,5 (Kemal kuralı) · iç panel 1,2 · raf/tabla 1,5 · braket/kulak 3,0 · AISI 304 2B, dış yüz 240 kum satine, hat boyunca yatay.
    · Büküm iç R = 1,5t · K 0,45 (kararlar) · paneller tava: ön/arka kenar 90° iç dönüş (flans olcu='dis', köşe 'bindirme' + TIG görünürde, 'acik' gizlide).
    · Panel → iskelet: 3 mm L KULAK (kulak()) iskelete kaynaklı; panele PEM FHP-M5 gömme saplama (bükümden ÖNCE, düz sacta) + DIN 9021 pul +
      ISO 10511 fiberli somun İÇERİDEN. Arka / teknik panel: ISO 7380 M5 + PEM SP-M5 (vidali_birlesim 'pem_somun'). PEM CLS ve FH4 YASAK (304).
    · Her sac: S.Sac → dogrula() (açınımdan yeniden büküm ΔV < %0,5 · kalınlık · kesit R) + dfm(abkant=True) 0 HATA.
3 · VİDA ARALIĞI: panel kenarı boyunca ≤ 200 (sektör 150–250) · köşeden ≤ 80 · contalı birleşimde ≤ 150 · kenar başına ≥ 2 (vida_konumlari /
    vida_araligi_denetle). K pilotunda yan sac kulakları 210–450 aralıklı (rijit iskelet) → yeni istasyonda 200'e uy, uyulamıyorsa UYARI rapora yazılır.
4 · GÖRÜNÜR VİDA: ön ve üst DIŞ yüzde HİÇ YOK · komşu istasyona dayanan yan yüz: FHP gömme saplama (dışta iz yok) · arka / teknik bölme / servis
    kapağı: ISO 7380 A2 bombe başlı izinli · gıda bölgesinde bağlantı elemanı ve bindirme YOK, iç köşe R ≥ 3 · sıçrama bölgesinde açık diş yok
    (DIN 1587 kör somun) · görünür panele punta YOK (iz bırakır).
5 · KAPAK (kapak()): çift cidar — dış tava 1,5 (dönüş = kapak derinliği, köşeler bindirme + TIG, yatay dönüşler üstte) + iç tava 1,0 (dönüş 15,
    köşe açık), iç-dış boşluk 0,5, iç tava dönüşleri dış tava dönüşlerine punta ≈ 150 aralık. Derz 3 (komşu kapak / gövde kenarı). KULP YOK.
    · Menteşe: gizli 180° KALDIR-ÇIKAR (temizlikte kapak sökülür) — gövde yarısı DİKME İÇİNDE (gizli_mentese), h ≤ 900: 2, ≤ 1500: 3 adet.
      Sanal pivot = kapağın menteşe kenarındaki dış köşesi (kapak süpürmesi bununla). Ölçüler TEMSİLİ (Southco R6 / EMKA 1046 sınıfı) → katalogdan teyit.
    · Kilit: bas-aç (push-to-open) DİKME İÇİNDE (bas_ac) + iç tavaya punta karşılık plakası.
    · Pencere / klape açıklığı: aciklik() — iki cidarda hizalı kesik + 4 L kasa çıtası (iç tavaya punta, dış tavaya 0,5 + gıda silikonu). Klapenin
      kendi kanadı ayrı kapak() çağrısıyla kurulur.
6 · BAĞLANTI (istasyon ↔ istasyon): M8 — K tarafı dikme / kuşak dış duvarında M8 PERÇİN SOMUN (rivnut, delik Ø11) + ara pul (yan sac ↔ perçin başı
    boşluğunu doldurur) + yan sacta Ø9; cıvata ISO 4762 M8 × 25 A2-70 + DIN 125 KOMŞUNUN İÇİNDEN takılır → komşu sacta Ø9 gerekir: m8_noktasi()
    bunu KARSI_DELIK + ARAYUZ olarak kaydeder (cıvata/pul montaja GİRMEZ, karşı istasyon sahibine liste gider). İskelet içi bağlantı M6 perçin somun.
    Mekanizma ayakları istasyon tabanında PEM SP-M6 / SP-M5 (alttan) — mekanizma tarafı ARAYÜZ kaydı.
7 · ADLANDIRMA (elektrik katmanı parçaları ADIYLA bulur):
    · Eski gövde parça adları KORUNUR. Özellikle h3/_elk/elk.json 'delik' listesindeki (modül, ad) hedefleri: montaj elektrik geçiş deliklerini
      _ELK_DELIK[ad] ile ADLA keser, kesilemeyen ad `_eksik32` assert'ini düşürür → bu adlar MUTLAKA yeni listede aynı adla olmalı (delik sacda
      zaten açıksa montajın kesimi boşa gider, sorun değil). 'dusur' listesi: montaj bu adları çıkarır (yoksa UYARI).
    · Bir eski ad kalkıyorsa ESLEME tablosu (eski → yeni) verilir; ad_denetimi() HATA vermemeli. Tek parçaya inen çoklu parça (ör. 3 kapak → 1) eşlemede yazılır.
    · Yeni parça adları: govde_kulak_<taraf>_<yer>_<konum> · govde_bag_<…> · govde_m8_<karşı>_<…> · govde_m8_ara_pul_<…> · <kapak>_ic_tava ·
      <kapak>_mentese_<i>_{sabit,sabit_vida_a/b,kanat,pem_a/b,kanat_vida_a/b} · <kapak>_basac_<i> · <kapak>_karsilik_<i> ·
      <kapak>_<açıklık>_kasa_{sol,sag,alt,ust} · <profil>_tapa · *_kaynak_* / *_kose_kaynagi_* (kaynak) · arayuz_* (montaja girmez).
    · Montajdaki birim önek listesine (<X>_BIRIM … önekler) yeni önekler ('govde_' gibi) yama ile eklenir; uygula(onekler=…) bunu denetler.
    · Elektrik modül kodları (_ELK_ONEK): KS=K kesme · KC=E kutu · SC=B store · TC/TU=topping · FU/FT=fırın · UD=üst depo · QR · AK=A · KD=kaide.
8 · MONTAJ SÖZLEŞMESİ: govde_parcalari() → modül YEREL çerçevesinde parça listesi (KS.PARCALAR biçimi: ad · wp · mal · grup 'SABIT' · bom · …).
    İstasyon üreteci uygula(L, yeni, ESKI_GOVDE, isaret=<yalnız yeni gövdede olan ad>, onekler=GOVDE_ONEK) ile eski gövdeyi değiştirir (idempotent);
    süpürme taraması için dunya_listesi(L, Cerceve) ve kapak_dunya(L, Cerceve, g.kapakla_doner). Montaj modülleri DÜNYAYA YALNIZ ÖTELEMEYLE geçer
    (X_K / X_E / X_BC (+ Y_MEK)) → Cerceve parametresi; parçayı kurarken dünya koordinatı KULLANMA.
9 · DENETİM (montajdan ÖNCE, denetle()): her sac doğrula + DFM 0 HATA · profil DFM 0 HATA · çakışma gövde↔gövde / gövde↔mekanizma / gövde↔komşu
    0 izinsiz (bilinen temaslar gerekçeli 'bilinen' sözlüğünde) · arayüz elemanlarının kestiği parça listesi (karşı delik / diş) · her kapak için
    açılma süpürmesi 10–100° TEMİZ · ad_denetimi HATA yok. R['temiz'] False iken montaj YOK.
10 · ATÖLYE SIRASI (rapora yazılır): lazer (N₂) → PEM/saplama düz sacta → abkant (DFM'in bulduğu çarpmasız sıra, meta 'abkant_sira') → iskelet kaynaklı
    alt montaj (fikstür, kısa atlamalı dikiş) + kulaklar → taşlama + satine → dekapaj + pasivasyon (ASTM A380/A967) → perçin somunlar → mekanizma
    (gövdesiz iskelette) → paneller → kapak (iç tava + karşılık + kanat → dış tava punta → menteşe gövdeleri → as) → saha (M8 komşu cıvataları).
"""
import os, sys, re, json, math, time, collections
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S

SURUM = "h3_govde_ortak_v1"
V = cq.Vector
EKSEN = {"x": np.array([1.0, 0, 0]), "y": np.array([0, 1.0, 0]), "z": np.array([0, 0, 1.0])}
PROFIL_STD = dict(b=40.0, t=2.0)                       # kararlar: 40 × 40 × 2 · dış R = 2t
MAL_GECERLI = ("celik", "conta", "siyah", "sac", "kabuk")
DON_DESEN = r"mentese|_pim$|basac|bas_ac|mandal|tipon|yay_pimi|gazli_yay|dayama"     # süpürmede engel sayılmayan menteşe/kilit donanımı
# gizli 180° kaldır-çıkar menteşe — ölçüler TEMSİLİ (Southco R6 / EMKA 1046 sınıfı, katalogdan doğrulanacak) · a: kapağın menteşe kenarından içeri ·
# b: menteşe ekseni boyunca (yarı ölçü) · derinlik / vida_derinlik: dikme ÖN yüzünden geriye · plaka / cep / kol: kapak iç düzlemine (w_ic) göre
MENTESE = dict(sinif="Southco R6 / EMKA 1046 sınıfı", malzeme="AISI 316 pasive", dis="M5",
               govde_a=(14.5, 27.0), govde_b=25.0, govde_derinlik=26.0, vida_b=15.0, vida_derinlik=13.0, dis_yiv=8.0, vida_boy=None,
               pencere_pay=(0.25, 1.0), plaka_a=(14.0, 45.0), plaka_b=30.0, plaka_t=1.5, plaka_delik_a=39.0, plaka_delik_b=20.0, plaka_delik_cap=5.5,
               cep_a=(15.0, 27.0), cep_b=25.0, cep_h=11.0, kol_a=(17.0, 25.0), kol_b=18.0, ic_cep=(14.75, 27.75, 25.5), kanat_vida_boy=6)
BASAC = dict(sinif="Southco 97 / EMKA 1080 sınıfı", malzeme="AISI 316 / POM", govde_cap=12.0, delik_cap=12.2, govde_boy=26.0, bas_cap=14.0, bas_h=1.0,
             uc_cap=6.0, strok=7.0, karsilik=(12.0, 20.0), karsilik_rol="dis", punta=((-7.0, -13.0), (7.0, 13.0)))
M8 = dict(dis="M8", ara_dis=16.0, ara_ic=9.2, vida_std="ISO4762", pul_std="DIN125")


# =====================================================================================================================================
# 0 · küçük geometri
# =====================================================================================================================================
def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def silindir(p0, eksen, r, L):
    e = np.asarray(eksen, float); e = e / np.linalg.norm(e)
    return cq.Solid.makeCylinder(float(r), float(L), V(*map(float, p0)), V(*map(float, e)))


def halka(merkez, eksen, r_dis, r_ic, h):
    return silindir(merkez, eksen, r_dis, h).cut(silindir(np.asarray(merkez, float) - np.asarray(eksen, float) * 1.0, eksen, r_ic, h + 2.0))


def bir(*ss):
    s = ss[0]
    for q in ss[1:]: s = s.fuse(q)
    return s.clean()


def _sekil(p):
    if p.get("sh") is not None: return p["sh"]
    w = p["wp"]
    return w.val() if hasattr(w, "val") else w


def _yuz_adi(v):
    """eksene paralel birim vektör → '+x' / '-y' …"""
    v = np.asarray(v, float); i = int(np.argmax(np.abs(v)))
    if abs(abs(v[i]) - 1.0) > 1e-9 or np.sum(np.abs(v)) - abs(v[i]) > 1e-9: raise ValueError("eksene paralel değil: %s" % v)
    return ("+" if v[i] > 0 else "-") + "xyz"[i]


def _yuz_vektor(yuz):
    return EKSEN[yuz[1]] * (1.0 if yuz[0] == "+" else -1.0)


def _dizi(a0, a1, aralik, uc):
    """a0 + uc … a1 − uc arası eşit aralıklı, aralık ≤ 'aralik', en az 2 nokta"""
    L = a1 - a0 - 2.0 * uc
    if L <= 0: return [(a0 + a1) / 2.0]
    n = max(2, int(math.ceil(L / aralik - 1e-9)) + 1)
    return [a0 + uc + L * i / (n - 1) for i in range(n)]


# =====================================================================================================================================
# 1 · ÇERÇEVE (modül yereli ↔ dünya) · GÖVDE KAYIT DEFTERİ
# =====================================================================================================================================
class Cerceve:
    """dünya = yerel + (dx, dy, dz). Montaj modülleri döndürülmez, yalnız ötelenir (KS: X_K · KC: X_E · TC: X_BC, Y_MEK · TU: X_BC)."""
    def __init__(self, ad="yerel", dx=0.0, dy=0.0, dz=0.0):
        self.ad, self.d = ad, (float(dx), float(dy), float(dz))

    def __repr__(self):
        return "<Cerceve %s %s>" % (self.ad, self.d)

    def bos(self):
        return not any(self.d)

    def dunya(self, sh):
        return sh if self.bos() else sh.translate(V(*self.d))

    def yerel(self, sh):
        return sh if self.bos() else sh.translate(V(*(-c for c in self.d)))

    def nokta(self, p):
        return np.asarray(p, float) + np.asarray(self.d)

    def yerel_nokta(self, p):
        return np.asarray(p, float) - np.asarray(self.d)

    def gecis(self, hedef):
        """bu çerçevenin yerelinden 'hedef' çerçevenin yereline öteleme"""
        return Cerceve("%s→%s" % (self.ad, hedef.ad), *(a - b for a, b in zip(self.d, hedef.d)))

    def ozet(self):
        return dict(ad=self.ad, oteleme=list(self.d))


class Govde:
    """bir istasyon gövdesinin bütün parçaları (kayıt defteri). Her istasyon üreteci bir örnek tutar."""
    def __init__(self, birim, surum, istasyon="?", cerceve=None):
        self.birim, self.surum, self.istasyon = birim, surum, istasyon
        self.cerceve = cerceve or Cerceve()
        self.SAC, self.ELEMAN, self.KAYNAK, self.BIRLESIM, self.ARAYUZ, self.KULAK, self.KAPAK = [], [], [], [], [], [], []
        self.PROF = collections.OrderedDict()
        self.PANEL, self.NOT, self.M8, self.KARSI_DELIK, self.ESLEME = {}, [], [], [], {}
        self.KABUK, self.DONER_SAC, self.DONER = set(), {}, {}

    @property
    def PROFIL(self):
        return list(self.PROF.values())

    def not_(self, m):
        self.NOT.append(m)

    def sac(self, ad, rol, kabuk=False, doner=None, **k):
        if doner is not None: k.setdefault("mal", "on_seffaf")
        s = S.Sac(ad, rol=rol, birim=self.birim, kaynak=self.surum, **k)
        self.SAC.append(s)
        if kabuk: self.KABUK.add(ad)
        if doner is not None:
            self.DONER_SAC[ad] = doner.ad; doner.saclar.append(s)
            for a in _sac_parca_adlari(s): self.DONER[a] = doner.ad
        return s

    def profil(self, ad, eksen, a0, a1, c, b=None, t=None, Ro=None, not_=""):
        if ad in self.PROF: raise ValueError("profil adı çift: %s" % ad)
        p = Profil(ad, eksen, a0, a1, c, b=b if b is not None else PROFIL_STD["b"], t=t if t is not None else PROFIL_STD["t"], Ro=Ro,
                   birim=self.birim, kaynak=self.surum, not_=not_)
        self.PROF[ad] = p
        return p

    def eleman(self, p, mal="celik", doner=None, sabit=None):
        """bağlantı / katalog / özel parça kaydı · doner=Kapak: kapakla döner · sabit=Kapak: menteşe/kilit sabit yarısı (süpürmede engel değil)"""
        p["mal"] = p.get("mal") if p.get("mal") not in (None, "katalog", "paslanmaz") else mal
        p["birim"] = self.birim
        self.ELEMAN.append(p)
        if doner is not None:
            p.setdefault("meta", {})["kapakla_doner"] = True
            self.DONER[p["ad"]] = doner.ad; doner.doner.add(p["ad"])
        if sabit is not None: sabit.sabit.add(p["ad"])
        return p

    def kaynak(self, p):
        for q in (p if isinstance(p, (list, tuple)) else [p]): self.KAYNAK.append(q)
        return p

    def arayuz(self, p, karsi, gerek, not_=""):
        """montaja GİRMEYEN, karşı tarafta delik / diş isteyen eleman (cıvata, pul, saplama)"""
        p["tur"] = "arayuz"; p["arayuz"] = dict(karsi=karsi, gerek=gerek, not_=not_); p["birim"] = self.birim
        self.ARAYUZ.append(p)
        return p

    def ozel(self, ad, sh, std, tanim, olcu, malzeme="AISI 304", mal="celik", uretim=False, tur="baglanti", meta=None):
        p = S._bp(ad, sh, std, tanim, olcu, malzeme, birim=self.birim, meta=meta or {}, uretim=uretim, mal=mal)
        p["tur"] = tur
        return p

    def mal(self, p):
        """montaj malzeme sözleşmesi: kapakla dönen → on_seffaf · dış kabuk sacı → kabuk · diğer sac / profil / kaynak → sac · eleman → kendi (geçerliyse) / celik"""
        ad = p["ad"]
        if ad in self.DONER: return "on_seffaf"
        if p.get("tur") == "sac": return "kabuk" if ad in self.KABUK else "sac"
        if p.get("tur") in ("profil", "kaynak"): return "sac"
        return p.get("mal") if p.get("mal") in MAL_GECERLI else "celik"

    def doner_guncelle(self):
        """kapak saclarının sonradan eklenen köşe kaynaklarını da dönen parçalara yazar"""
        for s in self.SAC:
            if s.ad in self.DONER_SAC:
                for a in _sac_parca_adlari(s): self.DONER[a] = self.DONER_SAC[s.ad]

    def kapakla_doner(self, ad):
        if ad not in self.DONER: self.doner_guncelle()
        return ad in self.DONER


def _sac_parca_adlari(s):
    """S.Sac.parcalar() adları (sac + köşe kaynakları) — h3_sac_v1.kaynak_parcalari adlandırmasıyla aynı"""
    return [s.ad] + ["%s_kose_kaynagi_%d" % (s.ad, i + 1) for i, k in enumerate(s.kaynaklar) if k["tip"] == "kose"]


# =====================================================================================================================================
# 2 · KARE PROFİL (gerçek dış R'li) + duvar kesikleri + kesim listesi + DFM
# =====================================================================================================================================
class Profil:
    """304 kare boru b × b × t · eksen boyunca a0 → a1 · c = dik eksenlerdeki merkez: x için (y, z) · y için (x, z) · z için (x, y) · dış R = Ro (vars. 2t)"""
    def __init__(self, ad, eksen, a0, a1, c, b=40.0, t=2.0, Ro=None, birim="GOVDE", kaynak=SURUM, not_=""):
        self.ad, self.eksen, self.a0, self.a1, self.c = ad, eksen, float(a0), float(a1), tuple(map(float, c))
        self.b, self.t = float(b), float(t)
        self.Ro = float(Ro) if Ro is not None else 2.0 * self.t
        self.birim, self.kaynak, self.not_ = birim, kaynak, not_
        self.kesikler, self.uc_kaynak = [], []
        self._sh = None
        if self.a1 <= self.a0: raise ValueError("%s: a1 ≤ a0" % ad)

    def merkez(self, a):
        p = np.zeros(3); p["xyz".index(self.eksen)] = a
        dik = [k for k in "xyz" if k != self.eksen]
        p["xyz".index(dik[0])], p["xyz".index(dik[1])] = self.c
        return p

    def _govde(self):
        dis = S.yuz_dikd_r(0.0, 0.0, self.b, self.b, 0.0, self.Ro)
        ic = S.yuz_dikd_r(0.0, 0.0, self.b - 2 * self.t, self.b - 2 * self.t, 0.0, self.Ro - self.t)
        sh = S._prizma(dis.cut(ic), self.a1 - self.a0)
        dik = [k for k in "xyz" if k != self.eksen]
        ex, ey, ez = EKSEN[dik[0]], EKSEN[dik[1]], EKSEN[self.eksen]
        if np.linalg.det(np.column_stack([ex, ey, ez])) < 0: ey = -ey
        return S._tasi(sh, S._M(np.column_stack([ex, ey, ez]), self.merkez(self.a0)))

    def duvar_delik(self, yuz, a, kayma, cap, tip="delik", not_=""):
        """yuz: '+x' / '-x' / '+y' / '-y' / '+z' / '-z' (dış normal) · a: eksen boyunca konum (mutlak) · kayma: duvar düzleminde, eksene dik ikinci
        eksen yönünde merkezden"""
        n = _yuz_vektor(yuz)
        dik = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        p = self.merkez(a) + n * (self.b / 2.0 + 1.0) + EKSEN[dik] * kayma
        cut = silindir(p, -n, cap / 2.0, self.t + 1.6)
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, cap=cap, not_=not_)); self._sh = None
        return cut

    def duvar_pencere(self, yuz, a, kayma, la, lk, r=1.0, tip="pencere", not_=""):
        """dikdörtgen pencere: eksen boyunca la · dik yönde lk · yalnız o duvar (iç yüzden 0,6 içeri)"""
        sg = 1.0 if yuz[0] == "+" else -1.0
        dik = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        c = self.merkez(a)
        lo, hi = np.zeros(3), np.zeros(3)
        for i, k in enumerate("xyz"):
            if k == self.eksen: lo[i], hi[i] = a - la / 2.0, a + la / 2.0
            elif k == dik: lo[i], hi[i] = c[i] + kayma - lk / 2.0, c[i] + kayma + lk / 2.0
            else:
                d0, d1 = c[i] + sg * (self.b / 2.0 - self.t - 0.6), c[i] + sg * (self.b / 2.0 + 1.0)
                lo[i], hi[i] = min(d0, d1), max(d0, d1)
        cut = kutu(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, olcu=[la, lk], not_=not_)); self._sh = None
        return cut

    def _a_kayma(self, yuz, P):
        P = np.asarray(P, float)
        dik = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        a = float(P["xyz".index(self.eksen)])
        return a, float(P["xyz".index(dik)] - self.merkez(a)["xyz".index(dik)])

    def duvar_delik_nokta(self, yuz, P, cap, tip="delik", not_=""):
        """P: deliğin istenen merkezinden geçen herhangi bir nokta (eksen konumu + dik kayma P'den)"""
        a, k = self._a_kayma(yuz, P)
        return self.duvar_delik(yuz, a, k, cap, tip=tip, not_=not_)

    def duvar_pencere_nokta(self, yuz, P, la, lk, r=1.0, tip="pencere", not_=""):
        a, k = self._a_kayma(yuz, P)
        return self.duvar_pencere(yuz, a, k, la, lk, r=r, tip=tip, not_=not_)

    def kaynak_bolgesi(self, yuz, a0, a1):
        """bu yüze kaynaklı birleşim (kuşak ucu vb.) mutlak a0–a1 aralığında → DFM bu bölgede kesik istemez"""
        self.uc_kaynak.append((yuz, a0 - self.a0, a1 - self.a0))

    def kati(self):
        if self._sh is None:
            sh = self._govde()
            for k in self.kesikler: sh = sh.cut(k["sh"])
            self._sh = sh.clean()
        return self._sh

    def dfm(self):
        """kesik düz yüz içinde mi (köşe R'sine taşmaz) · boru ucundan ≥ 3 · kaynaklı birleşim bölgesinde değil · boy ≤ 6000"""
        out = []
        duz = self.b / 2.0 - self.Ro
        L = self.a1 - self.a0
        for k in self.kesikler:
            yar = (k.get("cap") or k["olcu"][1]) / 2.0
            ok = abs(k["kayma"]) + yar <= duz + 1e-6
            out.append(dict(kural="profil_duz_yuz", durum="GEÇTİ" if ok else "HATA", detay="%s %s %s Ø/en %.1f kayma %.1f · düz yüz ±%.1f" % (self.ad, k["tip"], k["yuz"], 2 * yar, k["kayma"], duz)))
            la = (k.get("cap") or k["olcu"][0]) / 2.0
            uc = min(k["a"] - la, L - k["a"] - la)
            out.append(dict(kural="profil_uc", durum="GEÇTİ" if uc >= 3.0 else "HATA", detay="%s %s → boru ucu %.1f (≥ 3)" % (self.ad, k["tip"], uc)))
            for (yz, b0, b1) in self.uc_kaynak:
                if yz == k["yuz"] and b0 - la - 3.0 < k["a"] < b1 + la + 3.0:
                    out.append(dict(kural="profil_kaynak_bolgesi", durum="HATA", detay="%s %s kaynaklı birleşim bölgesinde (%s %.0f–%.0f)" % (self.ad, k["tip"], yz, b0, b1)))
        out.append(dict(kural="profil_boy", durum="GEÇTİ" if L <= 6000 else "HATA", detay="%s L %.1f ≤ 6000 (boy stoğu)" % (self.ad, L)))
        return out

    def parca(self):
        sh = self.kati(); L = self.a1 - self.a0
        kg = sh.Volume() * S.YOGUNLUK
        kes = [dict({k: v for k, v in x.items() if k != "sh"}) for x in self.kesikler]
        return dict(ad=self.ad, wp=cq.Workplane("XY").add(sh), sh=sh, mal="sac", birim=self.birim, grup="SABIT", kaynak=self.kaynak, tur="profil",
                    bom=("Kare boru AISI 304 %g × %g × %g (EN 10217-7 / ASTM A554 · dış R %g) · %s" % (self.b, self.b, self.t, self.Ro, self.not_), 1, "L %.1f" % L,
                         "boru lazer / şerit testere 90° · %d kesik · %.2f kg" % (len(kes), kg), "ÜRETİM"),
                    meta=dict(tur="profil", eksen=self.eksen, L=round(L, 2), kesit=[self.b, self.b, self.t, self.Ro], kesikler=kes, kg=round(kg, 3)))

    def kesim_satiri(self):
        pp = self.parca(); d = self.dfm()
        return dict(ad=self.ad, eksen=self.eksen, L=pp["meta"]["L"], kg=pp["meta"]["kg"], kesit=pp["meta"]["kesit"], kesikler=pp["meta"]["kesikler"],
                    dfm_hata=[m for m in d if m["durum"] == "HATA"], uc_kesim="90° (dikmeye alın) · uçlar kaynakla kapanır")


def uc_kaynaklari(ad, nokta, yon_ray, yuzler, b=40.0, a=2.0, flat=None, Ro=4.0, birim="GOVDE"):
    """kuşak ucu ↔ dikme yüzü köşe kaynakları · nokta: birleşim düzleminde kuşak ekseni · yon_ray: kuşak boyunca dikmeden uzağa ·
    yuzler: İÇBÜKEY köşe oluşturan kuşak yan yüz normalleri (dikmeyle aynı düzlemdeki yüz = alın dikişi, taşlanır → verilmez) · flat: dikiş boyu (vars. b − 2Ro)"""
    flat = flat if flat is not None else b - 2 * Ro
    e = np.asarray(yon_ray, float); out = []
    for i, nf in enumerate(yuzler):
        nf = np.asarray(nf, float); w = np.cross(e, nf)
        p = np.asarray(nokta, float) + nf * (b / 2.0)
        out.append(S.kaynak_dikisi(p - w * flat / 2.0, p + w * flat / 2.0, e, nf, a, ad="%s_%d" % (ad, i), birim=birim, taraf="dis (köşe)",
                                   not_="kuşak ucu ↔ dikme · TIG 141 · ER308LSi"))
    return out


def dikme_tapasi(g, profil, uc="ust", t=2.0, pah=2.5, ad=None):
    """profil ucuna b × b × t tapa (köşeler 'pah' kırık · çevresi TIG alın, taşlanır → kaynak katısı yok) · uc 'ust' = a1 ucu, 'alt' = a0 ucu"""
    ex, ey = {"y": ((1.0, 0, 0), (0, 0, -1.0)), "x": ((0, 1.0, 0), (0, 0, 1.0)), "z": ((1.0, 0, 0), (0, 1.0, 0))}[profil.eksen]
    ex, ey = np.array(ex), np.array(ey)
    if uc == "alt": ey = -ey
    a = profil.a1 if uc == "ust" else profil.a0
    O = EKSEN[profil.eksen] * a
    C = profil.merkez(a)
    cu, cv = float(np.dot(C, ex)), float(np.dot(C, ey)); h = profil.b / 2.0; c = pah
    u0, u1, v0, v1 = cu - h, cu + h, cv - h, cv + h
    s = g.sac(ad or profil.ad + "_tapa", "braket", t=t)
    s.taban([(u0 + c, v0), (u1 - c, v0), (u1, v0 + c), (u1, v1 - c), (u1 - c, v1), (u0 + c, v1), (u0, v1 - c), (u0, v0 + c)],
            O=tuple(O), ex=tuple(ex), ey=tuple(ey), ad="tapa")
    return s


# =====================================================================================================================================
# 3 · PANEL KULAĞI (3 mm L) + FHP saplamalı bağlantı + kaynaklar · vida aralığı
# =====================================================================================================================================
def kulak(g, ad, A, stud, u, v, v_cerceve, L_kaynak=25.0, gen=25.0, uc=9.75, dis="M5", rol="braket"):
    """3 mm L kulak: taban = saplama ayağı (A panelinin iç yüzüne oturur) · flanş = kaynak ayağı (iskelet yüzüne kaynaklı).
    A: panel (S.Panel) · stud: A iç yüzündeki saplama noktası · u: kulak genişlik yönü · v: saplamadan iskelet yüzüne doğru (v_cerceve mm sonra
    iskelet yüzü) · u × v = A'dan UZAĞA (iskelet içine) normal · uc: saplamadan kulağın serbest kenarına."""
    s = g.sac(ad, rol)
    stud = np.asarray(stud, float); u, v = np.asarray(u, float), np.asarray(v, float)
    t, R = s.t, s.R
    vb = v_cerceve - (R + t)
    va = -uc
    if vb < S.DIN9021[dis][1] / 2.0 + 1.0 - 1e-9: raise ValueError("%s: pul büküme taşar (saplama → büküm %.1f · v_cerceve %.1f)" % (ad, vb, v_cerceve))
    if uc < S.PEM_SAPLAMA[dis]["kenar"] - 1e-9: raise ValueError("%s: saplama kenar mesafesi %.2f < %.2f" % (ad, uc, S.PEM_SAPLAMA[dis]["kenar"]))
    n = np.cross(u, v)
    zA = A.yerel(stud + n * 1.0)[2]
    if -1e-6 < zA < A.sac.t + 1e-6: raise ValueError("%s: u × v A panelinin içine bakıyor (kulak sacın içinde kalır)" % ad)
    P = s.taban([(-gen / 2, va), (gen / 2, va), (gen / 2, vb), (-gen / 2, vb)], O=tuple(stud), ex=tuple(u), ey=tuple(v), ad="saplama_ayagi")
    P.flans(2, L_kaynak, yon=+1, ad="kaynak_ayagi")
    for sg in (+1, -1):
        p0 = stud + u * sg * gen / 2.0 + v * v_cerceve + n * (R + t)
        p1 = stud + u * sg * gen / 2.0 + v * v_cerceve + n * L_kaynak
        g.kaynak(S.kaynak_dikisi(p0, p1, u * sg, -v, min(t, 3.0), ad=ad + "_kaynak_%s" % ("a" if sg > 0 else "b"), birim=g.birim, taraf="dis (köşe)",
                                 not_="kulak ↔ iskelet"))
    b = S.vidali_birlesim(A, P, tuple(stud), "pem_saplama", dis=dis, ad=ad + "_bag", birim=g.birim)
    for q in b["parcalar"]: g.eleman(q)
    g.BIRLESIM.append(b); g.KULAK.append(s)
    return s, P, b


def vida_konumlari(a0, a1, maks=200.0, uc=40.0, min_adet=2):
    """kenar boyunca bağlantı konumları: uçlardan 'uc' (≤ 80), aralık ≤ maks (contalıda 150), en az min_adet"""
    L = a1 - a0
    if L < 2 * uc: uc = L / 4.0
    n = max(min_adet, int(math.ceil((L - 2 * uc) / maks - 1e-9)) + 1)
    return [a0 + uc + (L - 2 * uc) * i / (n - 1) for i in range(n)]


def vida_araligi_denetle(konumlar, a0, a1, maks=200.0, kose=80.0, min_adet=2, ad=""):
    """reçete 3: ≤ maks · köşeden ≤ kose · kenar başına ≥ min_adet → maddeler (aşım UYARI, adet eksik HATA)"""
    k = sorted(konumlar); out = []
    out.append(dict(kural="vida_adet", durum="GEÇTİ" if len(k) >= min_adet else "HATA", detay="%s %d ≥ %d" % (ad, len(k), min_adet)))
    if k:
        for nm, d in (("bas", k[0] - a0), ("son", a1 - k[-1])):
            out.append(dict(kural="vida_kose", durum="GEÇTİ" if d <= kose + 1e-6 else "UYARI", detay="%s %s köşeden %.1f ≤ %g" % (ad, nm, d, kose)))
        ar = [b - a for a, b in zip(k, k[1:])]
        if ar: out.append(dict(kural="vida_araligi", durum="GEÇTİ" if max(ar) <= maks + 1e-6 else "UYARI", detay="%s en büyük aralık %.1f ≤ %g" % (ad, max(ar), maks)))
    return out


# =====================================================================================================================================
# 4 · ÇİFT CİDARLI KAPAK · pencere / klape açıklığı · dikme içi gizli menteşe · dikme içi bas-aç
# =====================================================================================================================================
class Kapak:
    """kapak çerçevesi: (u, v, w) → O + u·ex + v·ey + w·n (n = ex × ey = DIŞA, koridora). w_dis: dış yüz · w_ic: gövde ön düzlemi (iç tava arka yüzü).
    Menteşe / kilit yerel çerçevesi (a, b): a = kapağın 'kenar'ından içeri, b = kenar boyunca; a × b = n (sol/sağ/alt/üst)."""
    def __init__(self, g, ad, u0, u1, v0, v1, w_dis, w_ic, O, ex, ey, mal):
        self.g, self.ad, self.mal = g, ad, mal
        self.u0, self.u1, self.v0, self.v1, self.w_dis, self.w_ic = float(u0), float(u1), float(v0), float(v1), float(w_dis), float(w_ic)
        self.O = np.asarray(O, float); self.ex = S._n(ex); ey = np.asarray(ey, float); self.ey = S._n(ey - np.dot(ey, self.ex) * self.ex)
        self.n = np.cross(self.ex, self.ey)
        self.kd = self.ki = self.D = self.I = None
        self.saclar, self.doner, self.sabit = [], set(), set()
        self.mentese_kenari, self.menteseler, self.basaclar, self.acikliklar = None, [], [], []

    def __repr__(self):
        return "<Kapak %s %.0f–%.0f × %.0f–%.0f · w %.1f/%.1f>" % (self.ad, self.u0, self.u1, self.v0, self.v1, self.w_ic, self.w_dis)

    def kf(self, u, v, w):
        return self.O + u * self.ex + v * self.ey + w * self.n

    def uv(self, kenar, s, a, b):
        if kenar == "sol": return self.u0 + a, s + b
        if kenar == "sag": return self.u1 - a, s - b
        if kenar == "alt": return s - b, self.v0 + a
        if kenar == "ust": return s + b, self.v1 - a
        raise ValueError("kenar: sol / sag / alt / ust")

    def eksenler(self, kenar):
        return {"sol": (self.ex, self.ey), "sag": (-self.ex, -self.ey), "alt": (self.ey, -self.ex), "ust": (-self.ey, self.ex)}[kenar]

    def pivot(self):
        """sanal pivot (menteşe kenarındaki dış köşe, kapak yereli) — eksen = eksenler(kenar)[1], dışa açılış = −açı"""
        k = self.mentese_kenari
        if k is None: return None
        u, v = {"sol": (self.u0, 0.0), "sag": (self.u1, 0.0), "alt": (0.0, self.v0), "ust": (0.0, self.v1)}[k]
        return self.kf(u, v, self.w_dis)

    def eksen(self):
        return self.eksenler(self.mentese_kenari)[1] if self.mentese_kenari else None


def kapak(g, ad, u0, u1, v0, v1, w_dis, w_ic, O=(0.0, 0.0, 0.0), ex=(1.0, 0, 0), ey=(0, 1.0, 0), ustte="yatay", punta_u=None, punta_v=None,
          punta_aralik=150.0, punta_uc=40.0, acikliklar=(), mal="on_seffaf", dis_rol="kapak_dis", ic_rol="kapak_ic", ic_ad=None):
    """ÇİFT CİDARLI KAPAK: dış tava (dis_rol → 1,5) dış ölçüsü u0–u1 × v0–v1, dönüş derinliği w_dis − w_ic (köşe bindirme + TIG; ustte 'yatay' →
    alt/üst dönüş üstte, 'dusey' → sol/sağ) · iç tava (ic_rol → 1,0) iç-dış boşluk (standart 0,5) içeride, dönüş ic_donus (15), köşe açık ·
    iç tava dönüşleri dış tava dönüşlerine punta (punta_u / punta_v listeleri ya da punta_aralik ile otomatik) ·
    acikliklar: [dict(ad, u, v, boy, en, r=0, tip='pencere'|'klape', kasa=True, …)] → aciklik()"""
    K = Kapak(g, ad, u0, u1, v0, v1, w_dis, w_ic, O, ex, ey, mal)
    if w_dis - w_ic <= 0: raise ValueError("kapak: w_dis ≤ w_ic")
    kd = g.sac(ad, dis_rol, mal=mal, doner=K); gk = kd.R + kd.t
    D = kd.taban([(u0 + gk, v0 + gk), (u1 - gk, v0 + gk), (u1 - gk, v1 - gk), (u0 + gk, v1 - gk)], O=tuple(K.kf(0.0, 0.0, w_dis - kd.t)), ex=tuple(K.ex),
                 ey=tuple(K.ey), ad="on_yuz")
    fa = [D.flans(i, w_dis - w_ic, yon=-1, ad=a) for i, a in enumerate(("alt_donus", "sag_donus", "ust_donus", "sol_donus"))]
    if ustte == "yatay":
        kd.kose(fa[0], fa[1], "bindirme", ustte=fa[0]); kd.kose(fa[1], fa[2], "bindirme", ustte=fa[2])
        kd.kose(fa[2], fa[3], "bindirme", ustte=fa[2]); kd.kose(fa[3], fa[0], "bindirme", ustte=fa[0])
    else:
        kd.kose(fa[0], fa[1], "bindirme", ustte=fa[1]); kd.kose(fa[1], fa[2], "bindirme", ustte=fa[1])
        kd.kose(fa[2], fa[3], "bindirme", ustte=fa[3]); kd.kose(fa[3], fa[0], "bindirme", ustte=fa[3])
    ki = g.sac(ic_ad or ad + "_ic_tava", ic_rol, mal=mal, doner=K); gi = ki.R + ki.t
    st = S.STD.kapak(); b = st["ic_dis_bosluk"]
    ui0, ui1, vi0, vi1 = u0 + kd.t + b, u1 - kd.t - b, v0 + kd.t + b, v1 - kd.t - b
    if st["ic_donus"] > (w_dis - kd.t) - (w_ic + ki.t) + 1e-6: raise ValueError("kapak: iç tava dönüşü %.1f kapak boşluğuna sığmıyor" % st["ic_donus"])
    I = ki.taban([(ui0 + gi, vi0 + gi), (ui1 - gi, vi0 + gi), (ui1 - gi, vi1 - gi), (ui0 + gi, vi1 - gi)], O=tuple(K.kf(0.0, 0.0, w_ic)), ex=tuple(K.ex),
                 ey=tuple(K.ey), ad="ic_tava")
    fi = [I.flans(i, st["ic_donus"], yon=+1, ad=a) for i, a in enumerate(("alt_donus", "sag_donus", "ust_donus", "sol_donus"))]
    for i in range(4): ki.kose(fi[i], fi[(i + 1) % 4], "acik")
    wp = w_ic + ki.t + st["ic_donus"] / 2.0
    pu = list(punta_u) if punta_u is not None else _dizi(u0, u1, punta_aralik, punta_uc)
    pv = list(punta_v) if punta_v is not None else _dizi(v0, v1, punta_aralik, punta_uc)
    nok = [tuple(K.kf(x, vi0 - b / 2.0, wp)) for x in pu] + [tuple(K.kf(x, vi1 + b / 2.0, wp)) for x in pu]
    nok += [tuple(K.kf(ui0 - b / 2.0, y, wp)) for y in pv] + [tuple(K.kf(ui1 + b / 2.0, y, wp)) for y in pv]
    ki.punta(kd, nok, not_="iç tava dönüşleri → dış tava dönüşleri (%.1f boşluk elektrotla kapanır) · ≤ %g aralık" % (b, punta_aralik))
    K.kd, K.ki, K.D, K.I = kd, ki, D, I
    K.ic_kutu = (ui0, ui1, vi0, vi1)
    g.PANEL[ad] = dict(dis=D, ic=I, kd=kd, ki=ki, kapak=K)
    g.KAPAK.append(K)
    for A in acikliklar: aciklik(K, **A)
    return K


def aciklik(K, ad, u, v, boy, en, r=0.0, tip="pencere", kasa=True, kasa_ayak=15.0, kasa_bosluk=0.5, kasa_rol="kapak_ic", punta_aralik=100.0):
    """kapakta pencere / klape açıklığı (merkez u, v · boy × en kapak yerelinde): iki cidarda hizalı kesik + 4 L kasa çıtası.
    Kasa çıtası: düz ayağı iç tavanın kapak boşluğu tarafına punta, dik ayağı açıklığı astarlar (dış yüzü açıklık kenarında) ve dış tavanın iç yüzüne
    'kasa_bosluk' kalır (gıda silikonu) — dış tavaya punta YOK (satine yüz). Köşelerde düşey çıtalar tam boy, yatay çıtalar t + 0,5 kısa."""
    g = K.g; kd, ki = K.kd, K.ki
    uo0, uo1, vo0, vo1 = u - boy / 2.0, u + boy / 2.0, v - en / 2.0, v + en / 2.0
    K.D.dikdortgen(u, v, boy, en, r=r, tip=tip + "_acikligi", parca="%s açıklığı %g × %g" % (tip, boy, en))
    K.I.dikdortgen(u, v, boy, en, r=r, tip=tip + "_acikligi", parca="%s açıklığı (iç tava)" % tip)
    kayit = dict(ad=ad, tip=tip, merkez=[u, v], boy=boy, en=en, r=r, kasa=[])
    if kasa:
        ks_t = S.STD.t(kasa_rol); ks_R = S.STD.R(ks_t); e = ks_R + ks_t
        hk = (K.w_dis - kd.t - kasa_bosluk) - (K.w_ic + ki.t)
        ui0, ui1, vi0, vi1 = K.ic_kutu
        gi = ki.R + ki.t
        if uo0 - e - kasa_ayak < ui0 + gi + 2.0 or uo1 + e + kasa_ayak > ui1 - gi - 2.0 or vo0 - e - kasa_ayak < vi0 + gi + 2.0 or vo1 + e + kasa_ayak > vi1 - gi - 2.0:
            raise ValueError("aciklik %s: kasa çıtası iç tavanın düz alanına sığmıyor" % ad)
        ua, ub = uo0 + ks_t + 0.5, uo1 - ks_t - 0.5
        yanlar = [("sol", [(uo0 - e - kasa_ayak, vo0), (uo0 - e, vo0), (uo0 - e, vo1), (uo0 - e - kasa_ayak, vo1)], 1),
                  ("sag", [(uo1 + e, vo0), (uo1 + e + kasa_ayak, vo0), (uo1 + e + kasa_ayak, vo1), (uo1 + e, vo1)], 3),
                  ("alt", [(ua, vo0 - e - kasa_ayak), (ub, vo0 - e - kasa_ayak), (ub, vo0 - e), (ua, vo0 - e)], 2),
                  ("ust", [(ua, vo1 + e), (ub, vo1 + e), (ub, vo1 + e + kasa_ayak), (ua, vo1 + e + kasa_ayak)], 0)]
        wk = K.w_ic + ki.t
        for yan, poly, kenar in yanlar:
            s = g.sac("%s_%s_kasa_%s" % (K.ad, ad, yan), kasa_rol, mal=K.mal, doner=K)
            P = s.taban(poly, O=tuple(K.kf(0.0, 0.0, wk)), ex=tuple(K.ex), ey=tuple(K.ey), ad="ayak")
            P.flans(kenar, hk, yon=+1, ad="kasa")
            us = [p[0] for p in poly]; vs = [p[1] for p in poly]
            if yan in ("sol", "sag"):
                um = (min(us) + max(us)) / 2.0; nk = [tuple(K.kf(um, y, wk)) for y in _dizi(vo0, vo1, punta_aralik, 20.0)]
            else:
                vm = (min(vs) + max(vs)) / 2.0; nk = [tuple(K.kf(x, vm, wk)) for x in _dizi(ua, ub, punta_aralik, 20.0)]
            s.punta(ki, nk, not_="kasa çıtası düz ayağı → iç tava (kapak boşluğu tarafı)")
            kayit["kasa"].append(s.ad)
        g.not_("%s %s: kasa çıtası dik ayağı ↔ dış tava iç yüzü %.1f boşluk → gıda sınıfı silikon (punta YOK, satine yüz)" % (K.ad, ad, kasa_bosluk))
    K.acikliklar.append(kayit)
    return kayit


def _hinge_L(K, kenar, s):
    return lambda a, b, w: K.kf(*K.uv(kenar, s, a, b), w)


def _kutu_l(L, a0, a1, b0, b1, w0, w1):
    p, q = L(a0, b0, w0), L(a1, b1, w1)
    return kutu(p[0], q[0], p[1], q[1], p[2], q[2])


def _dikme_yeri(K, dikme, kenar, L, a_ref):
    """dikme merkezinin menteşe yerelinde a'sı ve kapak w'si · dikme ekseni = menteşe ekseni olmalı"""
    av, bv = K.eksenler(kenar)
    ei = "xyz".index(dikme.eksen)
    if abs(abs(bv[ei]) - 1.0) > 1e-9: raise ValueError("dikme %s ekseni (%s) kapak kenarına paralel değil" % (dikme.ad, dikme.eksen))
    H = L(a_ref, 0.0, K.w_ic)
    C = dikme.merkez(H[ei])
    a_c = float(np.dot(C - L(0.0, 0.0, 0.0), av))
    w_c = float(np.dot(C - K.O, K.n))
    return C, a_c, w_c


def gizli_mentese(g, K, dikme, kenar, konumlar, olcu=None):
    """DİKME İÇİ GİZLİ 180° KALDIR-ÇIKAR MENTEŞE (Southco R6 / EMKA 1046 sınıfı · ölçüler TEMSİLİ).
    GÖVDE yarısı dikmenin içinde (ön duvarda pencere, dikmenin içe bakan yan duvarından 2 × M5 ISO 7380) · KANAT yarısı: plaka iç tavanın arkasında,
    cep kutusu kapak boşluğunda (iç tavada cep kesiği), kol dikme ön yüzünden plakaya · plaka iç tavadaki 2 × PEM SP-M5'e ISO 7380 M5 ile.
    konumlar: kenar boyunca kapak yereli konumları (sol/sağ: v · alt/üst: u). Sanal pivot = kapağın 'kenar'ındaki dış köşesi."""
    m = dict(MENTESE, **(olcu or {}))
    av, bv = K.eksenler(kenar); nv = K.n
    yuz_on, yuz_ic = _yuz_adi(nv), _yuz_adi(av)
    if K.mentese_kenari not in (None, kenar): raise ValueError("%s: menteşe kenarı zaten %s" % (K.ad, K.mentese_kenari))
    K.mentese_kenari = kenar
    I, ki = K.I, K.ki
    dis = m["dis"]; ga0, ga1 = m["govde_a"]; gb = m["govde_b"]; vb_ = m["vida_b"]; vd = m["vida_derinlik"]
    pa0, pa1 = m["plaka_a"]; pb = m["plaka_b"]; pt = m["plaka_t"]; pda, pdb = m["plaka_delik_a"], m["plaka_delik_b"]
    ca0, ca1 = m["cep_a"]; cb = m["cep_b"]; ch = m["cep_h"]; ka0, ka1 = m["kol_a"]; kb = m["kol_b"]; ic0, ic1, icb = m["ic_cep"]
    if K.w_ic + ch > K.w_dis - K.kd.t - 1e-6: raise ValueError("%s: menteşe cebi (%g) kapak boşluğuna sığmıyor" % (K.ad, ch))
    adlar = []
    i0 = len(K.menteseler)
    for j, s in enumerate(konumlar):
        i = i0 + j; ad = "%s_mentese_%d" % (K.ad, i)
        L = _hinge_L(K, kenar, s)
        C, a_c, w_c = _dikme_yeri(K, dikme, kenar, L, (ga0 + ga1) / 2.0)
        h = dikme.b / 2.0; w_on = w_c + h; a_ic = a_c + h
        if not (a_c - h + dikme.t <= ga0 and ga1 <= a_c + h - dikme.t): raise ValueError("%s: menteşe gövdesi (a %g–%g) dikme %s boşluğuna sığmıyor (a %.1f–%.1f)"
                                                                                           % (ad, ga0, ga1, dikme.ad, a_c - h + dikme.t, a_c + h - dikme.t))
        if w_on - m["govde_derinlik"] < w_c - h + dikme.t - 1e-6: raise ValueError("%s: menteşe gövdesi dikmenin arka duvarına çarpar" % ad)
        if w_on > K.w_ic - pt + 1e-6: raise ValueError("%s: dikme ön yüzü (w %.1f) kapak iç düzlemine çok yakın" % (ad, w_on))
        # dikme: ön duvarda pencere · iç yan duvarda 2 × vida deliği
        dikme.duvar_pencere_nokta(yuz_on, L((ga0 + ga1) / 2.0, 0.0, w_on), 2 * (gb + m["pencere_pay"][1]), (ga1 - ga0) + 2 * m["pencere_pay"][0],
                                  tip="mentese_penceresi", not_="gizli menteşe gövdesi")
        for db in (-vb_, vb_):
            dikme.duvar_delik_nokta(yuz_ic, L(a_ic, db, w_on - vd), S.STD.delik_iso273(dis), tip="mentese_vidasi", not_="menteşe gövdesi 2 × %s" % dis)
        # gövde yarısı (dikme içinde) + dişli delikler
        L_vida = m["vida_boy"] or S._boy_sec((a_ic - ga1) + m["dis_yiv"] - 1.0, S.VIDA_BOY)
        h0, h1 = min(ga1 - m["dis_yiv"], a_ic - L_vida - 1.0), ga1 + 1.0
        gov = _kutu_l(L, ga0, ga1, -gb, gb, w_on - m["govde_derinlik"], w_on)
        for db in (-vb_, vb_):
            gov = gov.cut(silindir(L(h0, db, w_on - vd), av, S.D_NOM[dis] / 2.0, h1 - h0))
        g.eleman(g.ozel(ad + "_sabit", gov, m["sinif"], "Gizli 180° kaldır-çıkar menteşe · GÖVDE yarısı (dikme içine gömülü) %s" % m["malzeme"].rsplit(" ", 1)[0],
                        "%g × %g × %g · 2 × %s (dikme iç yan duvarından)" % (ga1 - ga0, 2 * gb, m["govde_derinlik"], dis), malzeme=m["malzeme"], mal="celik",
                        meta=dict(kaldir_cikar=True, aci=180, kenar=kenar, pivot=[round(float(c), 3) for c in K.kf(*K.uv(kenar, s, 0.0, 0.0), K.w_dis)])),
                 sabit=K)
        for db, ek in ((-vb_, "a"), (vb_, "b")):
            g.eleman(S.vida("ISO7380", dis, L_vida, tuple(L(a_ic, db, w_on - vd)), tuple(-av), ad=ad + "_sabit_vida_" + ek, birim=g.birim), sabit=K)
        # kanat yarısı: plaka (iç tava arkasında) + cep kutusu (kapak boşluğunda) + kol · plaka vidalarının başı dikme ön yüzüne bakar →
        # vida ekseni dikmenin iç yan yüzünü baş yarıçapı + 1 geçmeli (geniş dikmede plaka bu kadar uzar; K 30 × 30'da uzama yok)
        pw0 = K.w_ic - pt
        pda, pa1 = m["plaka_delik_a"], m["plaka_a"][1]
        pda_min = a_ic + S.ISO7380[dis][0] / 2.0 + 1.0
        uzama = max(0.0, pda_min - pda)
        if uzama > 0: pda, pa1 = pda + uzama, pa1 + uzama
        pl = _kutu_l(L, pa0, pa1, -pb, pb, pw0, K.w_ic)
        for db in (-pdb, pdb):
            pl = pl.cut(silindir(L(pda, db, pw0 - 0.5), nv, m["plaka_delik_cap"] / 2.0, pt + 1.5))
        parcalar = [pl, _kutu_l(L, ca0, ca1, -cb, cb, K.w_ic, K.w_ic + ch)]
        if pw0 - w_on > 1e-6: parcalar.append(_kutu_l(L, ka0, ka1, -kb, kb, w_on, pw0))
        g.eleman(g.ozel(ad + "_kanat", bir(*parcalar), m["sinif"], "Gizli 180° kaldır-çıkar menteşe · KANAT yarısı + kol (kapakla döner)",
                        "plaka %g × %g × %g + cep %g × %g × %g" % (pa1 - pa0, 2 * pb, pt, ca1 - ca0, 2 * cb, ch), malzeme=m["malzeme"], mal="celik",
                        meta=dict(kapakla_doner=True, plaka_uzama=round(uzama, 2))), doner=K)
        uc_, vc_ = K.uv(kenar, s, (ic0 + ic1) / 2.0, 0.0)
        bo, en = ((ic1 - ic0), 2 * icb) if abs(abs(np.dot(av, K.ex)) - 1.0) < 1e-9 else (2 * icb, (ic1 - ic0))
        I.dikdortgen(uc_, vc_, bo, en, tip="mentese_cebi", parca="menteşe kanat cebi (kol geçişi)")
        for db, ek in ((-pdb, "a"), (pdb, "b")):
            ps, c, ms = S.pem_somun("SP", dis, tuple(L(pda, db, K.w_ic + ki.t)), tuple(nv), ki.t, ad=ad + "_pem_" + ek, birim=g.birim)
            ps["meta"]["kapakla_doner"] = True
            uu, vv = K.uv(kenar, s, pda, db)
            I.delik(uu, vv, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
            g.eleman(ps, doner=K)
            vdd = S.vida("ISO7380", dis, m["kanat_vida_boy"], tuple(L(pda, db, pw0)), tuple(nv), ad=ad + "_kanat_vida_" + ek, birim=g.birim)
            vdd["meta"]["kapakla_doner"] = True
            g.eleman(vdd, doner=K)
        if uzama > 0: g.not_("%s: kanat plakası %.2f uzatıldı (dikme %s b %g · vida başı dikme ön yüzünden kaçar) — katalog/adaptör teyidi" % (ad, uzama, dikme.ad, dikme.b))
        K.menteseler.append(dict(ad=ad, kenar=kenar, konum=s, dikme=dikme.ad, vida_boy=L_vida, plaka_uzama=round(uzama, 2)))
        adlar.append(ad)
    return adlar


def bas_ac(g, K, dikme, kenar, konumlar, a=22.0, olcu=None):
    """DİKME İÇİ BAS-AÇ (push-to-open, Southco 97 / EMKA 1080 sınıfı · geçme gövde): dikme ön duvarında Ø12,2 · gövde dikmenin içinde, baş ön yüzde,
    uç kapak iç düzlemine kadar · kapakta iç tavanın boşluk tarafına punta karşılık plakası (1,5). a: kapağın 'kenar'ından içeri."""
    m = dict(BASAC, **(olcu or {}))
    av, bv = K.eksenler(kenar); nv = K.n
    yuz_on = _yuz_adi(nv)
    ki = K.ki
    hu, hv = m["karsilik"]
    adlar = []
    i0 = len(K.basaclar)
    for j, s in enumerate(konumlar):
        i = i0 + j; ad = "%s_basac_%d" % (K.ad, i)
        L = _hinge_L(K, kenar, s)
        C, a_c, w_c = _dikme_yeri(K, dikme, kenar, L, a)
        h = dikme.b / 2.0; w_on = w_c + h
        rg = m["govde_cap"] / 2.0
        if not (a_c - h + dikme.t <= a - rg and a + rg <= a_c + h - dikme.t): raise ValueError("%s: bas-aç gövdesi dikme %s boşluğuna sığmıyor" % (ad, dikme.ad))
        uc_len = K.w_ic - w_on - m["bas_h"]
        if uc_len <= 1e-6: raise ValueError("%s: dikme ön yüzü kapak iç düzlemine çok yakın (bas-aç ucu yok)" % ad)
        dikme.duvar_delik_nokta(yuz_on, L(a, 0.0, w_on), m["delik_cap"], tip="basac_deligi", not_="bas-aç gövdesi (geçme)")
        sh = silindir(L(a, 0.0, w_on - m["govde_boy"]), nv, rg, m["govde_boy"]).fuse(silindir(L(a, 0.0, w_on), nv, m["bas_cap"] / 2.0, m["bas_h"])) \
            .fuse(silindir(L(a, 0.0, w_on + m["bas_h"]), nv, m["uc_cap"] / 2.0, uc_len))
        g.eleman(g.ozel(ad, sh, m["sinif"], "Bas-aç mandalı (push-to-open, geçme gövde Ø%g · O-ring) — dikme ön yüzünde Ø%g" % (m["govde_cap"], m["delik_cap"]),
                        "Ø%g × %g · baş Ø%g × %g · strok %g" % (m["govde_cap"], m["govde_boy"], m["bas_cap"], m["bas_h"], m["strok"]), malzeme=m["malzeme"],
                        mal="siyah"), sabit=K)
        dp = g.sac("%s_karsilik_%d" % (K.ad, i), m["karsilik_rol"], mal=K.mal, doner=K)
        uc_, vc_ = K.uv(kenar, s, a, 0.0)
        su, sv = (hu, hv) if abs(abs(np.dot(av, K.ex)) - 1.0) < 1e-9 else (hv, hu)
        dp.taban([(uc_ - su, vc_ - sv), (uc_ + su, vc_ - sv), (uc_ + su, vc_ + sv), (uc_ - su, vc_ + sv)], O=tuple(K.kf(0.0, 0.0, K.w_ic + ki.t)),
                 ex=tuple(K.ex), ey=tuple(K.ey), ad="plaka")
        dp.punta(ki, [tuple(L(a + pa, pb, K.w_ic + ki.t)) for pa, pb in m["punta"]], not_="karşılık takviyesi → iç tava (kapak kapanmadan önce)")
        K.basaclar.append(dict(ad=ad, kenar=kenar, konum=s, a=a, dikme=dikme.ad))
        adlar.append(ad)
    return adlar


# =====================================================================================================================================
# 5 · İSTASYON ↔ İSTASYON M8 NOKTASI (perçin somun + ara pul + karşı Ø9 kaydı + arayüz cıvatası)
# =====================================================================================================================================
def m8_noktasi(g, etiket, profil, a, yuz, panel, karsi, karsi_kod="?", karsi_t=1.5, vida_boy=25, kayma=0.0, yer="", cerceve=None):
    """profil (dikme / kuşak) 'yuz' duvarında (komşuya bakan dış duvar) eksen konumu a'da M8 PERÇİN SOMUN (delik Ø11, kavrama = profil t) ·
    perçin başı ile yan sac iç yüzü arasına AISI 304 ARA PUL (kalınlık otomatik) · yan sacta (panel) Ø9 · komşu sac iç yüzünden ISO 4762 M8 + DIN 125
    → ARAYÜZ (montaja girmez) · komşu sacta Ø9 → KARSI_DELIK kaydı (dünya merkezi). Adlar: govde_m8_<etiket> · govde_m8_ara_pul_<etiket> ·
    arayuz_m8_<etiket>(_pul)."""
    cer = cerceve or g.cerceve
    d = _yuz_vektor(yuz)
    dik = [k for k in "xyz" if k not in (profil.eksen, yuz[1])][0]
    P = profil.merkez(a) + EKSEN[dik] * kayma
    Pf = P + d * profil.b / 2.0                                                       # profil dış duvarı (perçin başı oturur)
    ps, c = S.percin_somun(M8["dis"], profil.t, tuple(Pf), tuple(-d), ad="govde_m8_" + etiket, birim=g.birim)
    profil.duvar_delik(yuz, a, kayma, c["delik"], tip="m8_percin_somun", not_="%s↔%s M8" % (g.istasyon, karsi_kod))
    g.eleman(ps)
    uv = panel.yerel(Pf)
    F = [panel.dunya(uv[0], uv[1], z) for z in (0.0, panel.sac.t)]
    ic_y = max(F, key=lambda q: float(np.dot(q, -d))); dis_y = max(F, key=lambda q: float(np.dot(q, d)))
    ara = float(np.dot(Pf - ic_y, -d)) - c["hk"]
    if ara < -1e-6: raise ValueError("m8 %s: perçin somun başı yan sacın içine giriyor (%.2f)" % (etiket, ara))
    if ara > 0.2:
        sh = halka(Pf + d * c["hk"], d, M8["ara_dis"] / 2.0, M8["ara_ic"] / 2.0, ara)
        g.eleman(g.ozel("govde_m8_ara_pul_" + etiket, sh, "özel (304 · lazer)", "Ara pul AISI 304 Ø%g / Ø%g × %g (yan sac ↔ perçin somun başı)"
                        % (M8["ara_dis"], M8["ara_ic"], round(ara, 2)), "Ø%g × %g" % (M8["ara_dis"], round(ara, 2)), uretim=True, mal="sac"))
    gecis = S.STD.delik_iso273(M8["dis"])
    panel.delik(uv[0], uv[1], gecis, tip="vida_deligi", parca="%s↔%s M8 (ISO 273 orta)" % (g.istasyon, karsi_kod))
    Pk = dis_y + d * karsi_t                                                          # komşu sacın iç yüzü
    hp = S.DIN125[M8["dis"]][2]
    pu = S.pul(M8["pul_std"], M8["dis"], tuple(Pk + d * hp), tuple(-d), ad="arayuz_m8_%s_pul" % etiket, birim=g.birim)
    vd = S.vida(M8["vida_std"], M8["dis"], vida_boy, tuple(Pk + d * hp), tuple(-d), ad="arayuz_m8_%s" % etiket, birim=g.birim)
    g.arayuz(pu, karsi, "komşu yan sacta Ø%g delik (aynı eksen)" % gecis, "")
    g.arayuz(vd, karsi, "ISO 4762 M8 × %g A2-70 + DIN 125 · komşu istasyonun içinden takılır" % vida_boy, "")
    kd = dict(etiket=etiket, karsi=karsi, karsi_kod=karsi_kod, cap=gecis, sac_t=karsi_t, eksen=[float(x) for x in -d],
              merkez_dunya=[round(float(x), 2) for x in cer.nokta(Pk)], merkez_yerel=[round(float(x), 2) for x in Pk])
    g.KARSI_DELIK.append(kd)
    r = dict(etiket=etiket, taraf=karsi_kod, yer=yer or profil.ad, profil=profil.ad, a=a, ara_pul=round(ara, 3),
             dunya=[round(float(x), 1) for x in cer.nokta(Pk)], karsi_delik=kd)
    g.M8.append(r)
    return r


# =====================================================================================================================================
# 6 · MONTAJ SÖZLEŞMESİ (parça listesi · uygula · dünya kopyası · kapak bileşiği · ad denetimi)
# =====================================================================================================================================
def govde_parcalari(g, anahtar="wp", hedef=None):
    """montaja girecek gövde parçaları (arayüz elemanları HARİÇ) · g.cerceve yerelinde (hedef=Cerceve verilirse o çerçevenin yereline ötelenir) ·
    anahtar 'wp' (Workplane, KS.PARCALAR biçimi) ya da 'sh' (TU.P biçimi)"""
    L = []
    for s in g.SAC:
        ps = s.parcalar()
        if s.ad in g.DONER_SAC:
            beklenen = set(_sac_parca_adlari(s))
            for p in ps:
                assert p["ad"] in beklenen, ("kapak sacı parça adı beklenmiyor", p["ad"])
                g.DONER[p["ad"]] = g.DONER_SAC[s.ad]
        L += ps
    L += [p.parca() for p in g.PROF.values()] + g.ELEMAN + g.KAYNAK
    gec = g.cerceve.gecis(hedef) if hedef is not None else None
    out = []
    for p in L:
        sh = _sekil(p)
        if gec is not None and not gec.bos(): sh = gec.dunya(sh)
        q = dict(ad=p["ad"], mal=g.mal(p), grup="SABIT", bom=tuple(p["bom"]) if p.get("bom") else None, kaynak=g.surum, birim=g.birim, tur=p.get("tur", "sac"))
        q[anahtar] = cq.Workplane("XY").add(sh) if anahtar == "wp" else sh
        if p.get("sac"): q["sac"] = p["sac"]
        if p.get("meta"): q["meta"] = p["meta"]
        out.append(q)
    adlar = [q["ad"] for q in out]
    assert len(adlar) == len(set(adlar)), "çift ad: %s" % sorted(a for a in set(adlar) if adlar.count(a) > 1)
    return out


def uygula(L, yeni, eski_adlar, isaret, onekler=None, rapor=None, etiket=""):
    """modülün parça listesine (KS.PARCALAR / TU.P …) yeni gövdeyi uygular: eski gövde adlarını çıkarır, yenileri ekler · idempotent
    (listede 'isaret' adlı parça varsa dokunmaz) · eski ad eksikse / mekanizmayla ad çakışırsa / önek dışı ad varsa assert"""
    if any(p["ad"] == isaret for p in L):
        return L
    assert any(q["ad"] == isaret for q in yeni), ("%s: işaret adı yeni gövdede yok" % etiket, isaret)
    var = set(p["ad"] for p in L); eski = set(eski_adlar)
    eksik = [a for a in eski_adlar if a not in var]
    assert not eksik, ("%s: eski gövde parçası listede yok" % etiket, eksik)
    L[:] = [p for p in L if p["ad"] not in eski]
    cak = set(p["ad"] for p in L) & set(q["ad"] for q in yeni)
    assert not cak, ("%s: mekanizmayla ad çakışması" % etiket, sorted(cak))
    if onekler:
        bilinmeyen = [q["ad"] for q in yeni if not q["ad"].startswith(tuple(onekler))]
        assert not bilinmeyen, ("%s: gövde önekine uymayan ad" % etiket, bilinmeyen[:5])
    L.extend(yeni)
    if rapor is not None: rapor.append("%s üretim sacı gövdesi: −%d eski · +%d yeni (%s)" % (etiket, len(eski), len(yeni), SURUM))
    return L


def dunya_listesi(L, cerceve):
    """parça listesinin dünya kopyaları (wp ve/veya sh ötelenir) — süpürme / çakışma taraması için"""
    out = []
    for p in L:
        q = dict(p)
        if p.get("wp") is not None:
            s = p["wp"].val() if hasattr(p["wp"], "val") else p["wp"]
            q["wp"] = cq.Workplane("XY").add(cerceve.dunya(s))
        if p.get("sh") is not None: q["sh"] = cerceve.dunya(p["sh"])
        out.append(q)
    return out


def kapak_dunya(L, cerceve, doner):
    """kapakla dönen bütün parçaların dünya bileşiği · doner: callable(ad) ya da ad kümesi (g.kapakla_doner · Kapak.doner)"""
    f = doner if callable(doner) else (lambda a: a in doner)
    return cq.Compound.makeCompound([cerceve.dunya(_sekil(p)) for p in L if f(p["ad"])])


def dunya_ciftleri(L, cerceve, onek="", meta=False):
    """[(ad, dünya şekli, meta)] — denetle(mekanizma=…, komsu=…) girdisi"""
    return [(onek + p["ad"], cerceve.dunya(_sekil(p)), (p.get("meta") or {}) if meta else {}) for p in L]


def elk_hedefleri(modul_kodu, elk_json=None):
    """elektrik katmanının bu modülde ADIYLA aradığı parçalar (h3/_elk/elk.json: 'delik' [modül, ad, not] · 'dusur' [modül, ad])"""
    yol = elk_json or os.path.join(H3, "_elk", "elk.json")
    if not os.path.exists(yol): return dict(delik=[], dusur=[], yol=yol, var=False)
    J = json.load(open(yol, encoding="utf-8"))
    return dict(delik=sorted(set(x[1] for x in J.get("delik", []) if x[0] == modul_kodu)),
                dusur=sorted(set(x[1] for x in J.get("dusur", []) if x[0] == modul_kodu)), yol=yol, var=True)


def ad_denetimi(modul_kodu, yeni_adlar, eski_adlar=(), esleme=None, elk_json=None):
    """reçete 7 · elektrik delik hedefleri yeni listede AYNI adla olmalı (HATA) · düşürülecekler (UYARI) · kalkan eski adlar ESLEME'de (UYARI)"""
    E = elk_hedefleri(modul_kodu, elk_json); yeni = set(yeni_adlar); esleme = esleme or {}
    out = []
    if not E["var"]: out.append(dict(kural="elk_kaynak", durum="UYARI", detay="elk.json yok: %s" % E["yol"]))
    for a in E["delik"]:
        if a in yeni: out.append(dict(kural="elk_delik_hedefi", durum="GEÇTİ", detay="%s|%s korunuyor" % (modul_kodu, a)))
        else: out.append(dict(kural="elk_delik_hedefi", durum="HATA", detay="%s|%s YOK — montaj _ELK_DELIK ADLA keser, _eksik32 assert'i düşer (ad korunmalı%s)"
                                                                             % (modul_kodu, a, "; eşleme yetmez → %s" % esleme[a] if a in esleme else "")))
    for a in E["dusur"]:
        if a not in yeni: out.append(dict(kural="elk_dusur", durum="UYARI", detay="%s|%s düşürülecek ama listede yok" % (modul_kodu, a)))
    for a in eski_adlar:
        if a in yeni: continue
        if a not in esleme: out.append(dict(kural="ad_esleme", durum="UYARI", detay="eski ad kalktı, ESLEME (eski → yeni) yok: %s" % a))
        else:
            hedef = esleme[a] if isinstance(esleme[a], (list, tuple)) else [esleme[a]]
            ilk = [str(h).split()[0] for h in hedef]
            durum = "GEÇTİ" if any(h in yeni for h in ilk) else "UYARI"
            out.append(dict(kural="ad_esleme", durum=durum, detay="%s → %s" % (a, hedef)))
    return out


# =====================================================================================================================================
# 7 · DENETİM ŞABLONU (doğrula + DFM + çakışma + arayüz karşı delik + kapak açılma süpürmesi)
# =====================================================================================================================================
def bbk(a, b, pay=0.0):
    return a.xmin < b.xmax + pay and b.xmin < a.xmax + pay and a.ymin < b.ymax + pay and b.ymin < a.ymax + pay and a.zmin < b.zmax + pay and b.zmin < a.zmax + pay


def hacim(a, b):
    try:
        return a.intersect(b).Volume()
    except Exception:
        return -1.0


def cakisma(A, B, esik=0.5, ayni=False, izin=None):
    """A, B: [(ad, şekil, meta)] · dönüş [(a, b, hacim mm³)] (> esik ya da hesap hatası)"""
    bA = [s.BoundingBox() for _a, s, _e in A]; bB = bA if ayni else [s.BoundingBox() for _a, s, _e in B]
    out = []
    for i, (a, sa, ea) in enumerate(A):
        for j in (range(i + 1, len(A)) if ayni else range(len(B))):
            b, sb, eb = B[j]
            if not bbk(bA[i], bB[j], -1e-4): continue
            if izin and izin(a, ea, b, eb): continue
            v = hacim(sa, sb)
            if v > esik or v < 0: out.append((a, b, round(v, 3)))
    return out


def ic_ice_izni(a, ea, b, eb):
    """PEM gömme saplama başı sacın içinde (meta ic_ice)"""
    return (b in (ea.get("ic_ice") or [])) or (a in (eb.get("ic_ice") or []))


def denetle_sac(g, acinim_klasoru=None, abkant=True, log=print, ayrinti=lambda s: True):
    """her sac: dogrula() + dfm(abkant) (+ açınım JSON) → (rapor, özet)"""
    R, ht, ut = {}, 0, 0
    if acinim_klasoru: os.makedirs(acinim_klasoru, exist_ok=True)
    for s in g.SAC:
        r = s.dogrula(); d = s.dfm(abkant=abkant); a = s.acinim()
        if acinim_klasoru:
            with open(os.path.join(acinim_klasoru, s.ad + ".json"), "w", encoding="utf-8") as f: json.dump(a, f, ensure_ascii=False, indent=1)
        h = [m for m in d if m["durum"] == "HATA"]; u = [m for m in d if m["durum"] == "UYARI"]
        ht += len(h); ut += len(u)
        ab = [m for m in d if m["kural"] == "abkant"]
        gecti = bool(r.get("acinim_gecti")) and bool(r["kalinlik"]["gecti"]) and r.get("kesit_gecti") is not False
        R[s.ad] = dict(t=s.t, R=s.R, K=s.K, rol=s.rol, bukum=len(s.bukumler), levha=a["levha"], delik=len(a["ic_konturlar"]), abkant_sira=(ab[0].get("sira") if ab else None),
                       dogrula=dict(acinim_gecti=r.get("acinim_gecti"), hacim_farki_yuzde=r.get("hacim_farki_yuzde"), simetrik_fark_yuzde=r.get("simetrik_fark_yuzde"),
                                    kalinlik_gecti=r["kalinlik"]["gecti"], kesit_gecti=r.get("kesit_gecti"), gecerli=r.get("gecerli"), hata=r.get("yeniden_bukum_hatasi")),
                       gecti=gecti, dfm_hata=h, dfm_uyari=u, punta=s.puntalar)
        if h or u or not gecti or ayrinti(s):
            log("%-34s t%.1f · %d büküm · açınım %.0f×%.0f %.2f kg · ΔV %s sim %s · kalınlık %s · kesit %s · DFM %d HATA %d UYARI"
                % (s.ad, s.t, len(s.bukumler), a["levha"]["boy"], a["levha"]["en"], a["levha"]["kutle_kg"], r.get("hacim_farki_yuzde"), r.get("simetrik_fark_yuzde"),
                   r["kalinlik"]["gecti"], r.get("kesit_gecti"), len(h), len(u)))
        for m in h + u: log("        %s %-18s %s" % (m["durum"], m["kural"], m["detay"][:200]))
    kalan = [a for a, x in R.items() if not x["gecti"]]
    oz = dict(adet=len(g.SAC), dfm_hata=ht, dfm_uyari=ut, dogrulama_kalan=kalan)
    log("SAC: %d · DFM %d HATA · %d UYARI · doğrulama kalan %s" % (len(g.SAC), ht, ut, kalan))
    return R, oz


def denetle_profil(g, log=print):
    sat, ph = [], 0
    for p in g.PROF.values():
        k = p.kesim_satiri(); ph += len(k["dfm_hata"]); sat.append(k)
        for m in k["dfm_hata"]: log("   PROFİL HATA %s" % m["detay"])
    oz = dict(adet=len(sat), dfm_hata=ph, toplam_boy_m=round(sum(x["L"] for x in sat) / 1000.0, 3), kg=round(sum(x["kg"] for x in sat), 2))
    log("PROFİL: %d boru · %.2f m · %.1f kg · DFM %d HATA" % (oz["adet"], oz["toplam_boy_m"], oz["kg"], ph))
    return sat, oz


def profil_kesim_listesi(g, yol=None):
    sat, oz = denetle_profil(g, log=lambda m: None)
    d = dict(not_="304 kare boru · kesim boyu = L · delik/pencere konumu 'a' borunun a0 ucundan · 'kayma' yüz ortasından", ozet=oz, profiller=sat)
    if yol:
        with open(yol, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=1)
    return d


def arayuz_karsi_delik(g, cerceve, adaylar, esik=0.05):
    """arayüz elemanlarının (cıvata / pul / saplama) kestiği parçalar → karşı tarafta delik / diş gerekir · adaylar: [(ad, dünya şekli, meta)]"""
    aw = [(p["ad"], cerceve.dunya(_sekil(p)), {}) for p in g.ARAYUZ]
    c = cakisma(aw, adaylar, esik=esik)
    gerek = collections.defaultdict(list)
    for a, b, v in c: gerek[b].append(a)
    kayit = [dict(ad=p["ad"], karsi=p["arayuz"]["karsi"], gerek=p["arayuz"]["gerek"], not_=p["arayuz"]["not_"], bom=list(p.get("bom") or ())) for p in g.ARAYUZ]
    return kayit, {b: sorted(v) for b, v in sorted(gerek.items())}


def kapak_supurme(g, K, gw, mw=(), nw=(), cerceve=None, acilar=tuple(range(10, 101, 10)), esik=1.0, don_desen=DON_DESEN):
    """kapak açılma süpürmesi: K'nın dönen parçaları (K.doner + kapak sacları) sanal pivot etrafında dışa 10–100° döndürülür · engel = gövdenin
    dönmeyen parçaları (K.sabit ve menteşe/kilit donanımı hariç) + mekanizma + komşular (donanım hariç) · gw/mw/nw: [(ad, dünya şekli, meta)]"""
    cer = cerceve or g.cerceve
    if K.mentese_kenari is None: return dict(kapak=K.ad, atlandi="menteşe yok", bulgu=[])
    DON = re.compile(don_desen)
    don = set(K.doner) | set(a for a, k in g.DONER.items() if k == K.ad)
    kap = [s for a, s, _e in gw if a in don]
    kapw = cq.Compound.makeCompound(kap)
    eng = [(a, s) for a, s, _e in gw if a not in don and a not in K.sabit and not DON.search(a)] + [(a, s) for a, s, _e in mw] + \
          [(a, s) for a, s, _e in nw if not DON.search(a)]
    pv = cer.nokta(K.pivot()); ek = K.eksen()
    bul = []
    ebb = [(a, e, e.BoundingBox()) for a, e in eng]
    for ang in acilar:
        k = kapw.rotate(V(*pv), V(*(pv + ek)), -ang); kb = k.BoundingBox()
        for a, e, eb in ebb:
            if not bbk(kb, eb): continue
            v = hacim(k, e)
            if v > esik: bul.append((ang, a, round(v, 1)))
    return dict(kapak=K.ad, kapak_parcasi=len(kap), engel=len(eng), aci="%d–%d°" % (min(acilar), max(acilar)), pivot_dunya=[round(float(x), 3) for x in pv],
                eksen=[float(x) for x in ek], bulgu=bul)


def denetle(g, cerceve=None, mekanizma=(), komsu=(), bilinen=None, acinim_klasoru=None, abkant=True, supurme=True, acilar=tuple(range(10, 101, 10)),
            esik=0.5, sup_esik=1.0, don_desen=DON_DESEN, log=print, ayrinti=lambda s: False):
    """İSTASYON GÖVDESİ DENETİMİ (montajdan önce) · mekanizma / komsu: [(ad, dünya şekli, meta)] (dunya_ciftleri) · bilinen: {(gövde_ad, karşı_ad): gerekçe}
    (karşı ad 'B|x' ise '|x' sonu da eşleşir) → R · R['temiz']"""
    cer = cerceve or g.cerceve
    T0 = time.time()
    R = dict(surum=SURUM, govde=g.surum, birim=g.birim, istasyon=g.istasyon, cerceve=cer.ozet(), standart=S.STD.ozet())
    GOV = govde_parcalari(g)
    R["sac"], R["sac_ozet"] = denetle_sac(g, acinim_klasoru, abkant, log, ayrinti)
    R["profil"], R["profil_ozet"] = denetle_profil(g, log)
    gw = [(p["ad"], cer.dunya(_sekil(p)), p.get("meta", {})) for p in GOV]
    mw, nw = list(mekanizma), list(komsu)
    c_ic = cakisma(gw, gw, esik=esik, ayni=True, izin=ic_ice_izni)
    c_mek = cakisma(gw, mw, esik=esik) if mw else []
    c_kom = cakisma(gw, nw, esik=esik) if nw else []
    bilinen = bilinen or {}

    def ayir(L):
        iz, kal = [], []
        for a, b, v in L:
            k = next((n for (x, y), n in bilinen.items() if a == x and (b == y or b.endswith("|" + y) or b == y.split("|")[-1])), None)
            (iz if k else kal).append((a, b, v, k) if k else (a, b, v))
        return iz, kal
    iz_i, kal_i = ayir(c_ic); iz_m, kal_m = ayir(c_mek); iz_n, kal_n = ayir(c_kom)
    R["cakisma"] = dict(govde_govde=kal_i, govde_mekanizma=kal_m, govde_komsu=kal_n, izinli_bilinen=iz_i + iz_m + iz_n, izinsiz_toplam=len(kal_i) + len(kal_m) + len(kal_n))
    log("ÇAKIŞMA: gövde %d · mekanizma %d · komşu %d → gövde↔gövde %d · ↔mekanizma %d · ↔komşu %d · bilinen %d"
        % (len(gw), len(mw), len(nw), len(kal_i), len(kal_m), len(kal_n), len(R["cakisma"]["izinli_bilinen"])))
    for x in (kal_i + kal_m + kal_n)[:12]: log("   ÇAKIŞMA %s" % (x,))
    R["arayuz"], R["arayuz_karsi_delik"] = arayuz_karsi_delik(g, cer, mw + nw + gw)
    R["karsi_delik"] = g.KARSI_DELIK
    log("ARAYÜZ: %d eleman · kestiği parça %d → %s" % (len(g.ARAYUZ), len(R["arayuz_karsi_delik"]), sorted(R["arayuz_karsi_delik"])[:10]))
    R["supurme"] = []
    if supurme:
        for K in g.KAPAK:
            s = kapak_supurme(g, K, gw, mw, nw, cer, acilar, sup_esik, don_desen)
            R["supurme"].append(s)
            log("KAPAK SÜPÜRMESİ %s: %s parça · %s engel · %s" % (K.ad, s.get("kapak_parcasi"), s.get("engel"), "TEMİZ" if not s["bulgu"] else s["bulgu"][:8]))
    sup_n = sum(len(s["bulgu"]) for s in R["supurme"])
    R["ozet"] = dict(govde_parca=len(GOV), sac=len(g.SAC), profil=len(g.PROF), eleman=len(g.ELEMAN), kaynak=len(g.KAYNAK), arayuz=len(g.ARAYUZ),
                     dfm_hata=R["sac_ozet"]["dfm_hata"], dfm_uyari=R["sac_ozet"]["dfm_uyari"], profil_dfm_hata=R["profil_ozet"]["dfm_hata"],
                     dogrulama_kalan=len(R["sac_ozet"]["dogrulama_kalan"]), cakisma_izinsiz=R["cakisma"]["izinsiz_toplam"], supurme=sup_n, sure_sn=round(time.time() - T0, 1))
    R["temiz"] = R["ozet"]["dfm_hata"] == 0 and R["ozet"]["profil_dfm_hata"] == 0 and R["ozet"]["dogrulama_kalan"] == 0 and R["ozet"]["cakisma_izinsiz"] == 0 and sup_n == 0
    R["notlar"] = g.NOT
    log("DENETİM %s · %s" % ("TEMİZ" if R["temiz"] else "TEMİZ DEĞİL", json.dumps(R["ozet"], ensure_ascii=False)))
    return R
