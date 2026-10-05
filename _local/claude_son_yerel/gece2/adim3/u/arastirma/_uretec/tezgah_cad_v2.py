# -*- coding: utf-8 -*-
"""AUTOKITCH · S · PERSONEL TEZGÂHI v2 — BULAŞIK MAKİNESİ ALTINDA + EL YIKAMA EVYESİ ÜSTÜNDE · CAD v2 (30 Eyl 2026)
Kemal (30 Eyl): "bulaşık makinesini de personel tezgâhının altına koy, o tezgâhı ona göre ayarla, üstüne de evye koy elini yıkamak için küçük olandan".
YER: ön zonun sağ ucundaki cep — ince duvar (z 979–1039) ile sokak duvarı (z 1879) arası, niş duvarının (x 4510–4570) solu (dükkân planı v15).
  Ön zon yalnız 84 derin: 600 derin bulaşık ince duvara bakarsa kapağı açılamaz (önde 450 > kalan 190) → bulaşık 90° döner, kapağı cebin
  solundaki bekleme alanına (−x) açılır; tezgâh cebi duvardan duvara doldurur (x 3842–4505 · z 1044–1874, duvarlara 5 mm silikon derzi).
  Kullanıcı tezgâhın solunda (x < 3842) durur, yüzü +x'e (niş duvarına) döner: solunda ince duvar, sağında sokak duvarı.
DÜZEN (önlerin yüzü x 3857, gövde x 3875–4505, tabla 870–900, 100 etek duvar kenarlarında):
  · SOL BÖLME (z 1044–1515): MEIKO M-iClean US (bulasik_cad_v3, ön yüzü önlerle aynı düzlemde, kapak −x'e) · üstünde ayırma rafı 716 +
    KİLİTLİ KİŞİSEL ÇEKMECE 720–866 (Kemal 27 Eyl: "altında elemanın kendi çekmecesi") · ince duvar tarafında yan panel YOK: bulaşık
    zemine oturur, tabla ince duvara L köşebentle + arka panele + üst yan kuşağa (700–867) bağlı.
  · SAĞ DOLAP (z 1516–1874, 4 ayar ayağı + plint): üstte EL YIKAMA HAZNESİ 300 × 300 × 150 (derin çekme, tablaya kaynaklı) + GROHE fotoselli
    batarya · altta Stiebel Eltron EIL 3 Premium ani su ısıtıcı (sıcak su — Gıda Hijyeni Yönetmeliği: el yıkamada sıcak + soğuk akan su) ·
    şişe sifon 1½" · köşe musluk ½" · priz · 2 × 5 L temizlik bidonu (damla tepsisinde) · çöp 10 L · bez / eldiven / poşet kutusu · tek kapak.
  · DUVARLAR: sokak duvarında köpük sabunluk (Tork S4) + kâğıt havluluk (Tork H2) evyenin üstünde · ince duvarda askı rayı (v1: 1650).
KATALOG (kaynak): MEIKO M-iClean US (föy) · GROHE Euroeco Cosmopolitan E 36271000 kızılötesi, karışım yok: yükseklik 107, delik Ø34, çıkış 100,
  çıkış yüksekliği 86 (tapsuk.com ürün sayfası) · Stiebel Eltron EIL 3 Premium 200134: 3,53 kW 230 V 16 A · 143 × 190 × 82 · 1,5 kg · IP25 ·
  30–50 °C (stiebel-eltron.com teknik veri) · Tork S4 561500 köpük sabunluk 113 × 105 × 286 (staples.co.uk) · Tork Xpress H2 552000
  çok katlı havluluk 302 × 444 × 102 (torkglobal: yükseklik 444, derinlik 102; genişlik 302 TEYİT) · hazne 300 × 300 × 150 standart derin çekme
  304 (tedarikçiden teyit) · sifon, köşe musluk, ayar ayağı, teleskopik ray, kam kilit: katalog sınıfı, ölçü VARSAYIM.
KOORDİNAT: doğrudan DÜNYA (mm) — x hat boyu, y yerden, z önden (sokak +z). Sözleşme (v1 ile aynı): kur() · PARCALAR · dunya(p) · BIRIMLER ·
  BIRIM_MODUL · MALZEME · X0 · TASMA (montajda X_S = X0 − TASMA = tezgâhın solu). Ön kapak "on_kapak", çekmece önü "cekmece_onu" (montaj v61 şeffaf).
Önceki: tezgah_cad_v1.py (600 × 450 × 900 sokak duvarında, x 3950–4550 — niş duvarına 40 mm giriyordu, önü ince duvara 39 cm)."""
import math, os, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
import qr_cad_v1 as QR                    # ortak yardımcılar (kut, sily, silz, silx, dunya, kendi_arasinda) + QR konumu (denetim)
import bulasik_cad_v3 as BM               # v2: bulaşık makinesi tezgâhın altında (ön yüzü −x)

# ---------------------------------------------------------------- SABİTLER (dünya, mm) ----------------------------------------------------------------
Z_INCE, Z_SOKAK, X_NIS = 1039.0, 1879.0, 4510.0          # ince duvarın ön zon yüzü · sokak duvarı iç yüzü · niş yan duvarının yüzü (dükkân v15)
DERZ = 5.0                                               # duvarlara silikon derzi
X_ON = 3857.0                                            # önlerin (bulaşık ön yüzü, çekmece önü, kapak) dış yüzü
ON_T = 18.0                                              # çift cidar önler
X_GOVDE = X_ON + ON_T                                    # 3875 · gövde ön düzlemi
X_ARKA = X_NIS - DERZ                                    # 4505 · arka panel dış yüzü
Z_SOL, Z_SAG = Z_INCE + DERZ, Z_SOKAK - DERZ             # 1044 · 1874
T = 1.2                                                  # gövde sacı AISI 304
PLINT, GOVDE_UST, TABLA = 100.0, 870.0, 30.0
TASMA = 15.0                                             # tabla ön taşması (−x)
ETEK = 100.0                                             # duvar kenarlarında tabla eteği (sıçrama)
X_TABLA = X_ON - TASMA                                   # 3842
X0, Y0, Z0 = X_ON, 0.0, Z_SOL                            # sözleşme (montaj: X_S = X0 − TASMA)
W, D, H = X_ARKA - X_ON, Z_SAG - Z_SOL, GOVDE_UST + TABLA   # 648 × 830 × 900
Z_BOL = (1515.2, 1516.4)                                 # bulaşık bölmesi | evye dolabı ayırma paneli
RAF_Y = (716.0, 717.2)                                   # bulaşık üstü ayırma rafı (makine üstü 700, ayar +12 → 712)
CEKMECE = dict(y=(720.0, 866.0), strok=500.0, derin=500.0)
HAZNE = dict(x=(3890.0, 4190.0), z=(1544.6, 1844.6), derin=150.0, t=1.0)     # iç ölçü 300 × 300 × 150
BATARYA = dict(x=4240.0, z=1694.6, h=107.0, cikis=100.0, cikis_y=86.0, delik=34.0)   # GROHE 36271000
ISITICI = dict(x=(4280.0, 4470.0), y=(560.0, 703.0), z=(1516.4, 1598.4))            # EIL 3 Premium 190 × 143 × 82 (ayırma paneline asılı)
SIFON = dict(x=4040.0, z=1694.6, r=31.5, y=(560.0, 706.0), cikis_y=640.0)
SABUNLUK = dict(x=(3955.0, 4068.0), y=(1050.0, 1336.0), z=(Z_SOKAK - 105.0, Z_SOKAK))   # Tork S4 113 × 286 × 105
HAVLULUK = dict(x=(4150.0, 4452.0), y=(1150.0, 1594.0), z=(Z_SOKAK - 102.0, Z_SOKAK))   # Tork H2 302 × 444 × 102
ASKI_Y = 1650.0
BIDON = dict(w=125.0, h=285.0, d=190.0, kapak=15.0, y0=105.0)                   # v1 ile aynı (VARSAYIM)

PARCALAR = []
MODUL = "S"
BIRIMLER = [
    ("TEZGAH_GOVDE", "Personel tezgâhı v2 · 648 × 830 × 900 · AISI 304 · cebi duvardan duvara doldurur (x 3842–4505 · z 1044–1874) · tabla 870–900 + 100 etek · "
                     "sol bölmede bulaşık makinesi, sağda evye dolabı (4 ayar ayağı + plint, tek kapak)"),
    ("TEZGAH_BULASIK", "Bulaşık makinesi · MEIKO M-iClean US (föy ölçüleri) · tezgâhın altında, zemine 4 ayar ayağıyla · kapak alttan menteşeli, bekleme alanına (−x) açılır "
                       "(önde 450) · sepet 400 × 400 · ağız 315 · 2,7 kW 230 V / 6,7 kW 400 V 3N · bağlantılar arkadan niş duvarına"),
    ("TEZGAH_CEKMECE", "Kilitli kişisel çekmece 720–866 · bulaşığın üstünde, ayırma rafı 716 · bilyalı teleskopik ray 500 tam açılım · kam kilit"),
    ("TEZGAH_EVYE", "El yıkama evyesi · hazne 300 × 300 × 150 derin çekme 304 · GROHE Euroeco Cosmopolitan E 36271000 fotoselli batarya · "
                    "Stiebel Eltron EIL 3 Premium ani su ısıtıcı (3,53 kW, 30–50 °C) · şişe sifon 1½\" · köşe musluk ½\" · priz"),
    ("TEZGAH_TEMIZLIK", "Temizlik · 2 × 5 L bidon · damla tepsisi · evye dolabında"),
    ("TEZGAH_SARF", "Bez / eldiven / poşet kutusu · evye dolabında"),
    ("TEZGAH_COP", "Çöp kovası 10 L · kapaklı · poşetli · evye dolabında"),
    ("TEZGAH_HIJYEN", "Köpük sabunluk Tork S4 561500 + kâğıt havluluk Tork Xpress H2 552000 · sokak duvarında, evyenin üstünde"),
    ("TEZGAH_ASKI", "Duvar askısı · ince duvarda y 1650 · ray 500 + 3 kanca · duvardan 70"),
]
BIRIM_MODUL = {k: MODUL for k, _a in BIRIMLER}
ON_BIRIMLER = tuple(k for k, _a in BIRIMLER)
MALZEME = {"paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30), "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35),
           "plastik": dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.0, ruf=0.6), "bidon": dict(renk=(0.20, 0.45, 0.80, 1.0), met=0.0, ruf=0.5),
           "bidon_kapak": dict(renk=(0.95, 0.80, 0.15, 1.0), met=0.0, ruf=0.5), "pp_gri": dict(renk=(0.55, 0.57, 0.60, 1.0), met=0.0, ruf=0.6),
           "cop_kova": dict(renk=(0.25, 0.27, 0.29, 1.0), met=0.0, ruf=0.55), "poset": dict(renk=(0.10, 0.10, 0.10, 1.0), met=0.0, ruf=0.4),
           "bez": dict(renk=(0.30, 0.55, 0.85, 1.0), met=0.0, ruf=0.9), "eldiven": dict(renk=(0.35, 0.35, 0.85, 1.0), met=0.0, ruf=0.7),
           "aluminyum": dict(renk=(0.86, 0.87, 0.89, 1.0), met=0.8, ruf=0.35), "krom": dict(renk=(0.88, 0.89, 0.91, 1.0), met=1.0, ruf=0.12),
           "beyaz_abs": dict(renk=(0.95, 0.95, 0.94, 1.0), met=0.0, ruf=0.45), "hortum_orgu": dict(renk=(0.70, 0.72, 0.75, 1.0), met=0.8, ruf=0.4),
           "sifon_pp": dict(renk=(0.93, 0.93, 0.92, 1.0), met=0.0, ruf=0.5), "sensor_cam": dict(renk=(0.08, 0.08, 0.10, 1.0), met=0.2, ruf=0.1)}
for _k, _v in BM.MALZEME.items():
    MALZEME.setdefault(_k, _v)
kut, sily, silz, silx = QR.kut, QR.sily, QR.silz, QR.silx


def ekle(ad, wp, mal, birim, bom=None, grup="SABIT", kaynak=""):
    """bom = (kalem, adet, tanım, kaynak/not, tür) · wp DÜNYA koordinatında"""
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom))


dunya = QR.dunya


def boru(noktalar, r):
    """eksen-hizalı çoklu doğru boru (köşelerde küre) — hortum / su hattı"""
    sh = None
    for (a, b) in zip(noktalar, noktalar[1:]):
        dx, dy, dz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
        if abs(dx) > 1e-6: s = silx(a[1], a[2], r, min(a[0], b[0]), max(a[0], b[0]))
        elif abs(dy) > 1e-6: s = sily(a[0], a[2], r, min(a[1], b[1]), max(a[1], b[1]))
        else: s = silz(a[0], a[1], r, min(a[2], b[2]), max(a[2], b[2]))
        sh = s if sh is None else sh.union(s)
    for p in noktalar[1:-1]:
        sh = sh.union(cq.Workplane(obj=cq.Solid.makeSphere(r, cq.Vector(*p))))
    return sh


def kulp(x0, x1, y0, y1, z0, z1):
    """−x yönüne 23 çıkan çubuk kulp: çubuk + iki ayak (tek katı) · uzun kenar y ya da z boyunca"""
    if (y1 - y0) >= (z1 - z0):
        return kut(x0 - 23.0, x0 - 15.0, y0, y1, z0, z1).union(kut(x0 - 15.0, x0, y0, y0 + 10.0, z0, z1)).union(kut(x0 - 15.0, x0, y1 - 10.0, y1, z0, z1))
    return kut(x0 - 23.0, x0 - 15.0, y0, y1, z0, z1).union(kut(x0 - 15.0, x0, y0, y1, z0, z0 + 10.0)).union(kut(x0 - 15.0, x0, y0, y1, z1 - 10.0, z1))


# ---------------------------------------------------------------- GÖVDE ----------------------------------------------------------------
def govde():
    b = "TEZGAH_GOVDE"
    # evye dolabı ayakları (4) + arka panelin ince duvar ucundaki ayak + taşıyıcı köşebent
    for i, (x, z) in enumerate(((X_GOVDE + 30.0, Z_BOL[1] + 30.0), (X_GOVDE + 30.0, Z_SAG - 31.2), (X_ARKA - 31.2, Z_BOL[1] + 30.0), (X_ARKA - 31.2, Z_SAG - 31.2))):
        ekle("ayar_ayagi_%d" % i, sily(x, z, 20.0, 0.0, 8.0).union(sily(x, z, 14.0, 8.0, PLINT)), "plastik", b,
             bom=("Mutfak dolabı ayar ayağı 100 mm (±15)", 5, "Ø40 taban", "VARSAYIM · katalog", "SATIN ALMA") if i == 0 else None)
    ekle("ayar_ayagi_4", sily(X_ARKA - 21.0, Z_SOL + 21.0, 20.0, 0.0, 8.0).union(sily(X_ARKA - 21.0, Z_SOL + 21.0, 14.0, 8.0, PLINT - 3.0)), "plastik", b)
    ekle("arka_ayak_kosebendi", kut(X_ARKA - 45.0, X_ARKA - T, PLINT - 3.0, PLINT, Z_SOL, Z_SOL + 40.0), "paslanmaz", b,
         bom=("Arka ayak taşıyıcı plaka 3 mm (arka panele kaynaklı)", 1, "44 × 40", "üretim", "ÜRETİM"))
    ekle("plint", kut(X_GOVDE + 50.0, X_GOVDE + 50.0 + T, 3.0, PLINT, Z_BOL[1] + 2.0, Z_SAG - 2.0), "paslanmaz", b,
         bom=("Plint 1,2 mm (klipsli, 50 geride) · evye dolabı", 1, "354 × 94", "üretim", "ÜRETİM"))
    # sokak duvarı tarafı yan panel · ayırma paneli · evye dolabı tabanı · arka panel (bulaşık bağlantı penceresi + evye delikleri)
    ekle("yan_sokak", kut(X_GOVDE, X_ARKA - T, PLINT, GOVDE_UST, Z_SAG - T, Z_SAG), "paslanmaz", b,
         bom=("Yan panel AISI 304 1,2 mm (sokak duvarı tarafı)", 1, "628,8 × 770", "üretim (abkant)", "ÜRETİM"))
    ekle("ayirma_paneli", kut(X_GOVDE, X_ARKA - T, PLINT, GOVDE_UST, Z_BOL[0], Z_BOL[1]), "paslanmaz", b,
         bom=("Ayırma paneli AISI 304 1,2 mm (bulaşık | evye dolabı)", 1, "628,8 × 770", "üretim", "ÜRETİM"))
    ekle("evye_dolabi_tabani", kut(X_GOVDE, X_ARKA - T, PLINT, PLINT + T, Z_BOL[1], Z_SAG - T), "paslanmaz", b,
         bom=("Evye dolabı tabanı AISI 304 1,2 mm", 1, "628,8 × 356,4", "üretim", "ÜRETİM"))
    ap = kut(X_ARKA - T, X_ARKA, PLINT, GOVDE_UST, Z_SOL, Z_SAG)
    ap = ap.cut(kut(X_ARKA - 2.0, X_ARKA + 1.0, PLINT - 1.0, 250.0, 1075.0, 1380.0))                     # bulaşık hortum / kablo penceresi
    ap = ap.cut(silx(SIFON["cikis_y"], SIFON["z"], 24.0, X_ARKA - 2.0, X_ARKA + 1.0))                     # sifon çıkışı Ø40 + pay
    ap = ap.cut(silx(450.0, 1600.0, 12.0, X_ARKA - 2.0, X_ARKA + 1.0))                                     # soğuk su ½"
    ap = ap.cut(silx(800.0, 1800.0, 12.0, X_ARKA - 2.0, X_ARKA + 1.0))                                     # priz kablosu
    ekle("arka_panel", ap, "paslanmaz", b, bom=("Arka panel AISI 304 1,2 mm (niş duvarına) · bulaşık bağlantı penceresi 305 × 150", 1, "830 × 770", "üretim (lazer)", "ÜRETİM"))
    # ince duvar tarafı: yalnız üst yan kuşak (çekmece rayı + raf taşır) · tabla ince duvara L köşebentle
    ekle("ust_yan_kusak_ince", kut(X_GOVDE, X_ARKA - T, 700.0, 867.0, Z_SOL, Z_SOL + T), "paslanmaz", b,
         bom=("Üst yan kuşak 1,2 mm (ince duvar tarafı, çekmece rayı + raf)", 1, "628,8 × 167", "üretim", "ÜRETİM"))
    ekle("duvar_kosebendi_ince", kut(X_GOVDE + 20.0, X_ARKA - 20.0, 830.0, 870.0, Z_INCE, Z_INCE + 3.0).union(
        kut(X_GOVDE + 20.0, X_ARKA - 20.0, 867.0, 870.0, Z_INCE, Z_INCE + 30.0)), "paslanmaz", b,
         bom=("Duvar köşebendi L 30 × 40 × 3 (ince duvara dübelli, tablayı taşır)", 1, "590", "üretim", "ÜRETİM"))
    # tabla (hazne ağzı + batarya deliği) + etekler
    tb = kut(X_TABLA, X_ARKA, GOVDE_UST, GOVDE_UST + TABLA, Z_SOL, Z_SAG)
    hx, hz, t_ = HAZNE["x"], HAZNE["z"], HAZNE["t"]
    tb = tb.cut(kut(hx[0] - t_, hx[1] + t_, GOVDE_UST - 1.0, GOVDE_UST + TABLA + 1.0, hz[0] - t_, hz[1] + t_))
    tb = tb.cut(sily(BATARYA["x"], BATARYA["z"], BATARYA["delik"] / 2.0, GOVDE_UST - 1.0, GOVDE_UST + TABLA + 1.0))
    ekle("tabla_30", tb, "paslanmaz", b, bom=("Tezgâh tablası AISI 304 1,2 mm · 30 mm bükümlü, ses yalıtımlı takviyeli · hazne ağzı + Ø34 batarya deliği", 1, "663 × 830", "üretim", "ÜRETİM"))
    ekle("etek_arka", kut(X_ARKA - T, X_ARKA, GOVDE_UST + TABLA, GOVDE_UST + TABLA + ETEK, Z_SOL, Z_SAG), "paslanmaz", b,
         bom=("Tabla eteği 100 (arka + iki yan, sıçramaya karşı · köşeleri kaynaklı)", 3, "", "üretim", "ÜRETİM"))
    ekle("etek_ince", kut(X_TABLA, X_ARKA - T, GOVDE_UST + TABLA, GOVDE_UST + TABLA + ETEK, Z_SOL, Z_SOL + T), "paslanmaz", b)
    ekle("etek_sokak", kut(X_TABLA, X_ARKA - T, GOVDE_UST + TABLA, GOVDE_UST + TABLA + ETEK, Z_SAG - T, Z_SAG), "paslanmaz", b)
    # evye dolabı kapağı (tek kanat, menteşe sokak tarafında) + kulp
    ekle("on_kapak", kut(X_ON, X_GOVDE, PLINT + 4.0, 866.0, Z_BOL[1] + 1.6, Z_SAG - 2.6), "paslanmaz", b,
         bom=("Ön kapak 18 mm çift cidar AISI 304 (evye dolabı, menteşe sokak tarafı)", 1, "353,4 × 762", "üretim", "ÜRETİM"))
    for i, y in enumerate((180.0, 760.0)):
        ekle("kapak_mentesesi_%d" % i, kut(X_GOVDE, X_GOVDE + 20.0, y, y + 40.0, Z_SAG - T - 15.0, Z_SAG - T), "celik", b,
             bom=("Gizli menteşe 110° (kapak)", 2, "", "VARSAYIM · katalog", "SATIN ALMA") if i == 0 else None)
    ekle("kapak_kulpu", kulp(X_ON, X_ON, 560.0, 700.0, Z_BOL[1] + 12.0, Z_BOL[1] + 27.0), "celik", b,
         bom=("Çubuk kulp 140 mm paslanmaz", 2, "kapak + çekmece", "katalog", "SATIN ALMA"))


def bulasik():
    """bulasik_cad_v3 parçaları (ön yüz x 3857, sol yanı ayırma bölmesinin 5 mm içinde) · ad öneki bulasik_"""
    BM.X0, BM.Y0, BM.Z0, BM.YON = X_ON, 0.0, Z_SOL + T + 5.0, -90.0              # ön yüz 3857 · zemin · sol yan = üst yan kuşağın iç yüzü 1045,2 + 5 = 1050,2 · ön −x
    for p in BM.kur():
        q = dict(p); q["ad"] = "bulasik_" + p["ad"]; q["birim"] = "TEZGAH_BULASIK"
        ekle(q["ad"], q["wp"], q["mal"], q["birim"], bom=q.get("bom"), grup=q.get("grup", "SABIT"), kaynak=q.get("kaynak", ""))
    # bulaşık bağlantıları: makinenin arka uçlarından (x 4482) niş duvarındaki çıkışlara (x 4510) — elektrik zeminde, su + tahliye pencereden
    for ad, (x, y, r) in BM.BAG.items():
        zc = BM.Z0 + x
        ekle("bulasik_hat_%s" % ad, silx(y, zc, r, BM.X0 + BM.D + BM.DUVAR_PAYI, X_NIS), "celik" if ad == "elektrik" else "mavi_touch", "TEZGAH_BULASIK",
             bom=("Bulaşık %s hattı → niş duvarı çıkışı" % ad, 1, {"elektrik": "CEE 16 A 5P (400 V 3N) / Schuko 16 A (230 V) · VARSAYIM", "tahliye": "Ø40 PP → sifonlu pis su",
                                                                   "su": "¾\" köşe musluk + Y süzgeç"}[ad], "tesisatçı", "SATIN ALMA") if ad == "elektrik" else None)


def cekmece():
    b = "TEZGAH_CEKMECE"
    y0, y1 = CEKMECE["y"]
    zi0, zi1 = Z_SOL + T, Z_BOL[0]                                                     # bölme içi 1045,2–1515,2
    # bulaşık üstü ayırma rafı (çekmece içeriği makineye düşmesin; makine öne çekilip sökülebilir) + taşıyıcı çıtalar
    ekle("bulasik_ust_rafi", kut(X_GOVDE, X_ARKA - T, RAF_Y[0], RAF_Y[1], zi0, zi1), "paslanmaz", b,
         bom=("Bulaşık üstü ayırma rafı AISI 304 1,2 mm", 1, "628,8 × 470", "üretim", "ÜRETİM"))
    ekle("raf_citasi_ince", kut(X_GOVDE + 10.0, X_ARKA - 10.0, RAF_Y[0] - 3.0, RAF_Y[0], zi0, zi0 + 15.0), "paslanmaz", b,
         bom=("Raf taşıyıcı çıta 15 × 3", 2, "608", "üretim", "ÜRETİM"))
    ekle("raf_citasi_bolme", kut(X_GOVDE + 10.0, X_ARKA - 10.0, RAF_Y[0] - 3.0, RAF_Y[0], zi1 - 15.0, zi1), "paslanmaz", b)
    ekle("cekmece_onu", kut(X_ON, X_GOVDE, y0, y1, Z_SOL + 3.0, Z_BOL[1] - 1.6).cut(silx(846.0, 1280.0, 9.75, X_ON - 1.0, X_GOVDE + 1.0)), "paslanmaz", b,
         bom=("Çekmece önü 18 mm çift cidar AISI 304", 1, "469,6 × 146", "üretim", "ÜRETİM"))
    ekle("cekmece_kulpu", kulp(X_ON, X_ON, 790.0, 805.0, 1210.0, 1350.0), "celik", b)
    ekle("kam_kilit_silindiri", silx(846.0, 1280.0, 9.75, X_ON - 2.0, X_GOVDE + 3.0), "celik", b,
         bom=("Kam kilit Ø19 (anahtarlı, 2 anahtar)", 1, "kam üst kuşağa kilitler", "VARSAYIM · katalog", "SATIN ALMA"))
    ekle("kam_kilit_dili", kut(X_GOVDE + 3.0, X_GOVDE + 6.0, 840.0, 866.0, 1272.0, 1288.0), "celik", b)
    rz = ((zi0, zi0 + 12.7), (zi1 - 12.7, zi1))
    for ad_, (za, zb) in zip(("ince", "bolme"), rz):
        ekle("teleskopik_ray_%s" % ad_, kut(X_GOVDE + 1.0, X_GOVDE + 1.0 + CEKMECE["derin"], 760.0, 805.0, za, zb), "celik", b,
             bom=("Bilyalı teleskopik ray 12,7 × 45 · 500 tam açılım (çift)", 1, "yan montaj", "Accuride DZ3832 sınıfı · boy VARSAYIM", "SATIN ALMA") if ad_ == "ince" else None)
    za, zb = rz[0][1], rz[1][0]                                                        # kutu yanları rayın iç elemanına bağlı
    xa, xb = X_GOVDE, X_GOVDE + CEKMECE["derin"]                                       # kutunun önü çekmece önüne vidalı
    ekle("cekmece_kutu_tabani", kut(xa, xb, 725.0, 725.0 + T, za, zb), "paslanmaz", b,
         bom=("Çekmece kutusu AISI 304 1,2 mm (taban + yanlar + arka)", 1, "%.0f × %.0f × 105" % (zb - za, xb - xa), "üretim", "ÜRETİM"))
    ekle("cekmece_kutu_yan_ince", kut(xa, xb, 725.0 + T, 830.0, za, za + T), "paslanmaz", b)
    ekle("cekmece_kutu_yan_bolme", kut(xa, xb, 725.0 + T, 830.0, zb - T, zb), "paslanmaz", b)
    ekle("cekmece_kutu_arka", kut(xb - T, xb, 725.0 + T, 830.0, za + T, zb - T), "paslanmaz", b)
    ekle("cekmece_kutu_on", kut(xa, xa + T, 725.0 + T, 830.0, za + T, zb - T), "paslanmaz", b)


def evye():
    b = "TEZGAH_EVYE"
    hx, hz, dy, t_ = HAZNE["x"], HAZNE["z"], HAZNE["derin"], HAZNE["t"]
    ust = GOVDE_UST + TABLA
    dis = kut(hx[0] - t_, hx[1] + t_, ust - dy - t_, ust, hz[0] - t_, hz[1] + t_)
    ic = kut(hx[0], hx[1], ust - dy, ust + 1.0, hz[0], hz[1])
    xc, zc = (hx[0] + hx[1]) / 2.0, (hz[0] + hz[1]) / 2.0
    hz_ = dis.cut(ic).cut(sily(xc, zc, 26.0, ust - dy - t_ - 1.0, ust - dy + 1.0))
    ekle("lavabo_haznesi", hz_, "paslanmaz", b, bom=("El yıkama haznesi 300 × 300 × 150 derin çekme AISI 304 1,0 mm (tablaya TIG kaynaklı, Ø52 gider)", 1,
                                                    "iç 300 × 300 × 150", "standart hazne · tedarikçiden teyit", "SATIN ALMA"))
    ekle("gider_suzgeci", sily(xc, zc, 35.0, ust - dy, ust - dy + 3.0).cut(sily(xc, zc, 20.0, ust - dy - 1.0, ust - dy + 4.0)), "krom", b,
         bom=("Süzgeçli gider 1½\" (Ø52 delik, sepetli)", 1, "Ø70 flanş", "katalog sınıfı · VARSAYIM", "SATIN ALMA"))
    ekle("gider_govdesi", sily(xc, zc, 26.0, SIFON["y"][1] + 3.0, ust - dy - t_).union(sily(xc, zc, 20.0, SIFON["y"][1] - 20.0, SIFON["y"][1] + 3.0)), "sifon_pp", b)
    ekle("sise_sifon", sily(xc, zc, SIFON["r"], SIFON["y"][0], SIFON["y"][1] - 20.0).union(silx(SIFON["cikis_y"], zc, 20.0, xc, xc + SIFON["r"] + 25.0)), "sifon_pp", b,
         bom=("Şişe sifon 1½\" PP (temizleme kapaklı)", 1, "Ø63 × 146", "katalog sınıfı · VARSAYIM", "SATIN ALMA"))
    ekle("sifon_cikisi", silx(SIFON["cikis_y"], zc, 20.0, xc + SIFON["r"] + 25.0, X_NIS), "sifon_pp", b,
         bom=("Pis su borusu Ø40 PP → niş duvarındaki gider", 1, "~480", "tesisatçı", "SATIN ALMA"))
    # batarya (GROHE 36271000): taban Ø50 × 4 · gövde Ø40 → 107 · çıkış 100 (−x), çıkış altı tabladan 86 · sensör penceresi · bağlantı gövdesi + hortum
    by, bx, bz = ust, BATARYA["x"], BATARYA["z"]
    ekle("batarya_tabani", sily(bx, bz, 25.0, by, by + 4.0), "krom", b,
         bom=("GROHE Euroeco Cosmopolitan E 36271000 · kızılötesi elektronik lavabo bataryası (karışımsız: sıcaklığı ani ısıtıcı ayarlar)", 1,
              "yükseklik 107 · çıkış 100 · çıkış yüksekliği 86 · delik Ø34", "tapsuk.com ürün sayfası", "SATIN ALMA"))
    ekle("batarya_govdesi", sily(bx, bz, 20.0, by + 4.0, by + BATARYA["h"]), "krom", b)
    cy = by + BATARYA["cikis_y"]
    ekle("batarya_cikisi", kut(bx - BATARYA["cikis"], bx - 20.0, cy + 6.0, cy + 20.0, bz - 12.0, bz + 12.0).union(sily(bx - BATARYA["cikis"] + 11.0, bz, 11.0, cy, cy + 6.0)), "krom", b)
    ekle("batarya_sensoru", kut(bx - 22.0, bx - 20.0, by + 60.0, by + 78.0, bz - 8.0, bz + 8.0), "sensor_cam", b)
    ekle("batarya_saplamasi", sily(bx, bz, 15.0, GOVDE_UST - 45.0, by), "celik", b)
    ekle("batarya_somunu", sily(bx, bz, 24.0, GOVDE_UST - 8.0, GOVDE_UST).cut(sily(bx, bz, 15.0, GOVDE_UST - 9.0, GOVDE_UST + 1.0)), "celik", b)
    # ani su ısıtıcı (EIL 3 Premium) ayırma paneline asılı · soğuk giriş + ılık çıkış üstte · köşe musluk · priz
    ix, iy, iz = ISITICI["x"], ISITICI["y"], ISITICI["z"]
    ekle("ani_su_isitici", kut(ix[0], ix[1], iy[0], iy[1], iz[0], iz[1]), "beyaz_abs", b,
         bom=("Stiebel Eltron EIL 3 Premium (200134) mini ani su ısıtıcı · tezgâh altı", 1, "143 × 190 × 82 · 3,53 kW 230 V · 16 A · IP25 · 30–50 °C · 1,5 kg",
              "stiebel-eltron.com teknik veri", "SATIN ALMA"))
    zk = (iz[0] + iz[1]) / 2.0
    ekle("isitici_soguk_giris", sily(4320.0, zk, 6.0, iy[1], iy[1] + 15.0), "krom", b)
    ekle("isitici_ilik_cikis", sily(4430.0, zk, 6.0, iy[1], iy[1] + 15.0), "krom", b)
    ekle("kose_musluk", silx(450.0, 1600.0, 13.0, X_ARKA - T - 26.0, X_ARKA - T).union(sily(X_ARKA - T - 13.0, 1600.0, 9.0, 463.0, 485.0)), "krom", b,
         bom=("Köşe musluk ½\" (filtreli)", 1, "", "katalog sınıfı", "SATIN ALMA"))
    ekle("hortum_soguk", boru([(X_ARKA - T - 13.0, 485.0, 1600.0), (X_ARKA - T - 13.0, 760.0, 1600.0), (4320.0, 760.0, 1600.0), (4320.0, 760.0, zk), (4320.0, iy[1] + 15.0, zk)], 5.0),
         "hortum_orgu", b, bom=("Örgülü esnek hortum ⅜\" (2 adet)", 2, "~500", "katalog sınıfı", "SATIN ALMA"))
    ekle("hortum_ilik", boru([(4430.0, iy[1] + 15.0, zk), (4430.0, 790.0, zk), (4430.0, 790.0, bz), (bx, 790.0, bz), (bx, GOVDE_UST - 45.0, bz)], 5.0), "hortum_orgu", b)
    ekle("priz_ip44", kut(X_ARKA - T - 50.0, X_ARKA - T, 760.0, 840.0, 1760.0, 1840.0), "beyaz_abs", b,
         bom=("Sıva üstü priz IP44 16 A (ısıtıcı) · ayrı W-otomat 16 A + 30 mA kaçak akım", 1, "80 × 80 × 50", "elektrikçi", "SATIN ALMA"))


def icerik():
    ekle("damla_tepsisi", kut(3885.0, 4090.0, PLINT + T, BIDON["y0"], 1522.0, 1800.0), "pp_gri", "TEZGAH_TEMIZLIK",
         bom=("Damla tepsisi PP (kimyasal sızıntısı)", 1, "205 × 278 × 3,8", "VARSAYIM", "SATIN ALMA"))
    for i, z in enumerate((1530.0, 1665.0)):
        yb = BIDON["y0"] + BIDON["h"]
        ekle("temizlik_bidonu_%d" % i, kut(3890.0, 3890.0 + BIDON["d"], BIDON["y0"], yb, z, z + BIDON["w"]), "bidon", "TEZGAH_TEMIZLIK",
             bom=("Temizlik kimyasalı 5 L bidon (yüzey temizleyici + dezenfektan)", 2, "125 × 285 × 190 + kapak", "tedarikçi bidonu · ölçü VARSAYIM", "SATIN ALMA") if i == 0 else None)
        ekle("temizlik_bidonu_kapagi_%d" % i, sily(3950.0, z + BIDON["w"] / 2.0, 19.0, yb, yb + BIDON["kapak"]), "bidon_kapak", "TEZGAH_TEMIZLIK")
    b = "TEZGAH_COP"
    ek = (4110.0, 4330.0, PLINT + T, 351.0, 1540.0, 1740.0)
    ekle("cop_kovasi_10L", kut(*ek).cut(kut(ek[0] + 2.0, ek[1] - 2.0, ek[2] + 2.0, ek[3] + 1.0, ek[4] + 2.0, ek[5] - 2.0)), "cop_kova", b,
         bom=("Çöp kovası 10 L kapaklı (çekip açılır)", 1, "220 × 250 × 200", "VARSAYIM", "SATIN ALMA"))
    ekle("cop_kovasi_kapagi", kut(ek[0], ek[1], ek[3], ek[3] + 15.0, ek[4], ek[5]), "cop_kova", b)
    ekle("cop_poseti", kut(ek[0] + 3.0, ek[1] - 3.0, ek[2] + 2.0, ek[3], ek[4] + 3.0, ek[5] - 3.0).cut(kut(ek[0] + 3.4, ek[1] - 3.4, ek[2] + 2.4, ek[3] + 1.0, ek[4] + 3.4, ek[5] - 3.4)),
         "poset", b, bom=("Çöp poşeti 10 L", 1, "sarf", "—", "SATIN ALMA"))
    b = "TEZGAH_SARF"
    sk = (4340.0, 4490.0, PLINT + T, 301.2, 1600.0, 1858.0)
    ekle("sarf_kutusu", kut(*sk).cut(kut(sk[0] + 2.0, sk[1] - 2.0, sk[2] + 2.0, sk[3] + 1.0, sk[4] + 2.0, sk[5] - 2.0)), "pp_gri", b,
         bom=("Saklama kutusu 3 bölmeli (bez · eldiven · poşet)", 1, "258 × 150 × 200", "VARSAYIM", "SATIN ALMA"))
    for i, z in enumerate((1686.0, 1772.0)):
        ekle("sarf_kutusu_bolme_%d" % i, kut(sk[0] + 2.0, sk[1] - 2.0, sk[2] + 2.0, sk[3], z, z + 2.0), "pp_gri", b)
    ekle("bez_yigini", kut(sk[0] + 6.0, sk[1] - 6.0, sk[2] + 2.0, sk[2] + 72.0, 1606.0, 1684.0), "bez", b)
    ekle("eldiven_kutusu", kut(sk[0] + 6.0, sk[1] - 6.0, sk[2] + 2.0, sk[2] + 92.0, 1690.0, 1770.0), "eldiven", b,
         bom=("Tek kullanımlık eldiven kutusu", 1, "sarf", "—", "SATIN ALMA"))
    ekle("poset_rulosu", silx(sk[2] + 2.0 + 35.0, 1814.0, 35.0, sk[0] + 10.0, sk[1] - 10.0), "poset", b)


def duvar():
    b = "TEZGAH_HIJYEN"
    sx, sy, sz = SABUNLUK["x"], SABUNLUK["y"], SABUNLUK["z"]
    ekle("sabunluk_tork_s4", kut(sx[0], sx[1], sy[0], sy[1], sz[0], sz[1]), "beyaz_abs", b,
         bom=("Tork S4 561500 köpük sabunluk (sokak duvarına 2 vida)", 1, "113 × 105 × 286", "staples.co.uk / tork", "SATIN ALMA"))
    ekle("sabunluk_pompa", kut(sx[0] + 36.0, sx[1] - 36.0, sy[0] - 12.0, sy[0], sz[0] + 20.0, sz[0] + 60.0), "plastik", b)
    hx, hy, hz = HAVLULUK["x"], HAVLULUK["y"], HAVLULUK["z"]
    ekle("havluluk_tork_h2", kut(hx[0], hx[1], hy[0], hy[1], hz[0], hz[1]), "beyaz_abs", b,
         bom=("Tork Xpress H2 552000 çok katlı kâğıt havluluk (sokak duvarına)", 1, "302 × 444 × 102", "torkglobal (genişlik TEYİT)", "SATIN ALMA"))
    b = "TEZGAH_ASKI"
    ekle("aski_rayi", kut(3950.0, 4450.0, ASKI_Y - 10.0, ASKI_Y + 10.0, Z_INCE, Z_INCE + 10.0), "aluminyum", b,
         bom=("Duvar askısı rayı alüminyum 20 × 10 (ince duvara 2 dübel)", 1, "500", "üretim", "ÜRETİM"))
    for i, x in enumerate((4020.0, 4200.0, 4380.0)):
        k = kut(x - 6.0, x + 6.0, ASKI_Y - 50.0, ASKI_Y - 10.0, Z_INCE, Z_INCE + 7.0)
        k = k.union(silz(x, ASKI_Y - 44.0, 5.0, Z_INCE + 7.0, Z_INCE + 63.0)).union(sily(x, Z_INCE + 63.0, 5.0, ASKI_Y - 44.0, ASKI_Y - 20.0))
        k = k.union(cq.Workplane(obj=cq.Solid.makeSphere(7.0, cq.Vector(x, ASKI_Y - 20.0, Z_INCE + 63.0), angleDegrees1=-90, angleDegrees2=90)))
        ekle("aski_kancasi_%d" % i, k, "paslanmaz", b, bom=("Askı kancası Ø10 paslanmaz (J)", 3, "duvardan 70", "üretim", "ÜRETİM") if i == 0 else None)


def kur():
    PARCALAR[:] = []
    govde(); bulasik(); cekmece(); evye(); icerik(); duvar()
    return PARCALAR


DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-118s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))


def _bb(ad):
    return [dunya(p).BoundingBox() for p in PARCALAR if p["ad"] == ad][0]


if __name__ == "__main__":
    t0 = time.time(); arg = sys.argv[1:]
    ps = kur()
    gec = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("TEZGÂH v2 · %d parça · katı denetimi: %s · %.0f sn" % (len(ps), "hepsi geçerli" if not gec else gec, time.time() - t0))
    for kod, _a in BIRIMLER:
        q = [dunya(p).BoundingBox() for p in ps if p["birim"] == kod]
        print("   %-16s %2d parça · x %.1f–%.1f · y %.1f–%.1f · z %.1f–%.1f" % (kod, len(q), min(v.xmin for v in q), max(v.xmax for v in q), min(v.ymin for v in q), max(v.ymax for v in q), min(v.zmin for v in q), max(v.zmax for v in q)))
    print("DENETİM (tezgah_cad_v2)")
    kontrol("katılar geçerli", not gec, ", ".join(gec))
    # 1 · cebe sığar: gövde + tabla x 3842–4505 · z 1044–1874 · duvar parçaları duvar yüzlerinin içinde · QR ve niş duvarından ayrı
    gv = [dunya(p).BoundingBox() for p in ps if p["birim"] not in ("TEZGAH_HIJYEN", "TEZGAH_ASKI") and "kulp" not in p["ad"] and not p["ad"].startswith(("bulasik_hat_", "sifon_cikisi"))]
    kontrol("cebe sığar: x %.1f–%.1f (tabla 3842 · arka 4505 < niş duvarı %.0f) · z %.1f–%.1f (ince duvar %.0f … sokak %.0f, derz 5)"
            % (min(v.xmin for v in gv), max(v.xmax for v in gv), X_NIS, min(v.zmin for v in gv), max(v.zmax for v in gv), Z_INCE, Z_SOKAK),
            min(v.xmin for v in gv) >= X_TABLA - 0.01 and max(v.xmax for v in gv) <= X_ARKA + 0.01 and min(v.zmin for v in gv) >= Z_INCE - 0.01 and max(v.zmax for v in gv) <= Z_SAG + 0.01)
    hep = [dunya(p).BoundingBox() for p in ps]
    kontrol("duvar parçaları duvar yüzlerinin içinde: x ≤ %.0f · z %.0f–%.0f" % (X_NIS, Z_INCE, Z_SOKAK),
            max(v.xmax for v in hep) <= X_NIS + 0.01 and min(v.zmin for v in hep) >= Z_INCE - 0.01 and max(v.zmax for v in hep) <= Z_SOKAK + 0.01)
    kontrol("QR dolabından ayrı: tezgâh x ≤ %.0f < QR x %.0f" % (max(v.xmax for v in hep), QR.X0), max(v.xmax for v in hep) < QR.X0)
    # 2 · bulaşık bölmesi: yan boşluklar ≥ 5 · üst rafa ≥ 12 (ayar ayağı +12) · arkada föy duvar payı ≥ 25
    gx, gy, gz = BM.govde_zarf()
    kontrol("bulaşık bölmesi: sol boşluk %.1f · sağ boşluk %.1f (≥ 5) · makine üstü %.0f + ayar 12 = %.0f ≤ raf altı %.0f · arka payı %.1f (≥ föy %.0f)"
            % (gz[0] - (Z_SOL + T), Z_BOL[0] - gz[1], gy[1], gy[1] + BM.AYAR, RAF_Y[0], X_ARKA - T - gx[1], BM.DUVAR_PAYI),
            gz[0] - (Z_SOL + T) >= 4.99 and Z_BOL[0] - gz[1] >= 4.99 and gy[1] + BM.AYAR <= RAF_Y[0] and X_ARKA - T - gx[1] >= BM.DUVAR_PAYI - 0.01)
    kontrol("bulaşık ön yüzü önlerle aynı düzlemde: x %.1f = %.1f" % (gx[0], X_ON), abs(gx[0] - X_ON) < 0.01)
    # 3 · kapak açık zarfı (bekleme alanına) tezgâh parçalarına girmez
    kx, ky, kz = BM.kapi_acik_zarf()
    zarf = cq.Workplane("XY").box(kx[1] - kx[0], ky[1] - ky[0], kz[1] - kz[0], centered=False).translate((kx[0], ky[0], kz[0])).val()
    kes = [(p["ad"], round(dunya(p).intersect(zarf).Volume(), 1)) for p in ps if p["birim"] != "TEZGAH_BULASIK"]
    kes = [k for k in kes if k[1] > 1.0]
    kontrol("bulaşık kapağı açık zarfı x %.0f–%.0f · y %.0f–%.0f · z %.0f–%.0f (önde %.0f, bekleme alanına) ↔ tezgâh parçaları: %s"
            % (kx + ky + kz + (kx[1] - kx[0], "BOŞ" if not kes else kes)), not kes)
    # 4 · evye: batarya çıkışı haznenin ağzında · sifon / ısıtıcı / hortum çakışmaz (aşağıda kendi arasında) · ergonomi
    cx = BATARYA["x"] - BATARYA["cikis"] + 11.0
    kontrol("batarya çıkışı (x %.0f · z %.0f) hazne ağzı içinde (x %.0f–%.0f · z %.0f–%.0f) · çıkış tabladan %.0f yukarıda (GROHE 86)"
            % (cx, BATARYA["z"], HAZNE["x"][0], HAZNE["x"][1], HAZNE["z"][0], HAZNE["z"][1], BATARYA["cikis_y"]),
            HAZNE["x"][0] + 20.0 < cx < HAZNE["x"][1] - 20.0 and HAZNE["z"][0] + 20.0 < BATARYA["z"] < HAZNE["z"][1] - 20.0)
    kontrol("hazne iç 300 × 300 × 150 · ağız kotu %.0f (EN 1116 tezgâh 850–950)" % (GOVDE_UST + TABLA), 850.0 <= GOVDE_UST + TABLA <= 950.0)
    sab = (SABUNLUK["x"][0] + SABUNLUK["x"][1]) / 2.0 - X_TABLA
    kontrol("sabunluk pompası tabla önünden %.0f içeride, hazne üstünde (z %.0f ∈ %.0f–%.0f) · tabladan %.0f yukarıda"
            % (sab, SABUNLUK["z"][0] + 40.0, HAZNE["z"][0], HAZNE["z"][1], SABUNLUK["y"][0] - GOVDE_UST - TABLA),
            sab <= 250.0 and HAZNE["z"][0] <= SABUNLUK["z"][0] + 40.0 <= HAZNE["z"][1] and SABUNLUK["y"][0] - GOVDE_UST - TABLA >= 100.0)
    kontrol("ısıtıcı (EIL 3) sifonun %.0f mm yanında, gider hattının üstünde değil" % (ISITICI["x"][0] - (SIFON["x"] + SIFON["r"])), ISITICI["x"][0] - (SIFON["x"] + SIFON["r"]) >= 50.0)
    # 5 · çekmece: raf üstünde · tam açık (500) önü x %.0f → bekleme alanında
    ck = _bb("cekmece_kutu_tabani")
    kontrol("çekmece kutusu altı %.0f > raf üstü %.0f · tam açıkta önü x %.0f (bekleme alanı)" % (ck.ymin, RAF_Y[1], X_ON - CEKMECE["strok"]), ck.ymin > RAF_Y[1])
    cak = QR.kendi_arasinda(ps, istisna=lambda a, c: False)
    print("KENDİ ARASINDA (> 1 mm³): %s" % ("TEMİZ" if not cak else cak[:20]))
    kontrol("kendi arasında çakışma = 0 (%d parça, bulaşık dahil)" % len(ps), not cak, str(len(cak)))
    import denetim_temas_v1 as DT
    DUVAR_KOK = tuple(p["ad"] for p in ps if p["birim"] in ("TEZGAH_HIJYEN", "TEZGAH_ASKI") or p["ad"] in ("duvar_kosebendi_ince", "sifon_cikisi") or p["ad"].startswith("bulasik_hat_"))
    hv = DT.havada([(p["ad"], dunya(p)) for p in ps], zemin_y=0.0, kok_adlar=DUVAR_KOK)
    nh = DT.yaz(hv, baslik="HAVADA PARCA (tezgah v2 · kok = zemin + duvara bagli parcalar)")
    kontrol("havada parça = 0 (kök: zemine oturanlar + duvara bağlı sabunluk / havluluk / askı / köşebent / hat uçları)", nh == 0, str(nh))
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETIM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    assert not kal
    sys.stdout.flush(); os._exit(0)
