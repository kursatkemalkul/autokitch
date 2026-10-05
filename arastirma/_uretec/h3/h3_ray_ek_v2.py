# -*- coding: utf-8 -*-
"""HAT v3.4 · R · ROBOT RAYI EKLERİ v2 (1 Eki 2026 · Claude · YEREL) — h3_ray_ek_v1'in kopyası · NEDEN: Kemal "ZEMİNİN ALTINA HİÇBİR ŞEY GÖMÜLMEZ
(y < 0 parça yok) · kablolar zeminin üstünden, dolap ayaklarının arasından · QR'ye alttan YANDAN / ÖNDEN girer · hiçbir şey yükseltilmez".
DEĞİŞENLER (h3_ray_ek_v1 → v2):
  · ZEMIN_KANALI birimi KALKTI (kanal_tabani · kanal_yan_sol / sag · kanal_uc_hat / qr · kanal_ayirici · kanal_kapagi_koridor / QR_alti — şapa gömülü y −60…0).
  · oluk_tabani: eski kanal ağzı (30 × 36, x 4780) KALKTI · oluk_yan_koridor: x 5046–5096 çıkış ağzı açıldı (y 2–40 · üstte 17 mm dudak).
  · ROBOT KABLOSU (uzatma A): oluk içinde x 4988'e kadar düz → R 100 (5 × d) yayla koridor yanından çıkar (yay sonunda y 12 → 50 yükselir) → yeni
    ROBOT_KABLO_KOPRUSU (304 2 mm kapaklı köprü kanalı, zeminin ÜSTÜNDE y 0–82, x 5044–5152, z 575–670: oluk ↔ QR tekmeliği) → QR tekmeliğindeki
    giriş (a) x 5088, y 50: icotek KEL 10|3 + KT 20 (h3_elk_qr_v1 · konnektörlü kablo bölünmüş çerçeveden geçer) → QR içinde kontrol kutusu (x ≤ 5070) ile
    kangal (x ≥ 5107,5) arasından inip kangalın alt ucuna (5117,5 · 30 · 825). Uzatma kısaldı → artanı kangalda (sarım hesapla yükseldi), B yeniden hesaplandı.
  · kablo_hesabi(): "zemin kanalı" satırı yerine "oluk çıkışı + köprü kanalı" ve "QR girişi (KEL 10|3) → kangal altı".
  · Giriş (a) sabitleri TEK KAYNAK: h3_elk_qr_v1.GIRIS_A / TEKME (tekmelik QR elektrik katmanında).
AYNI KALANLAR: oluk (boy, kesit, kapaklar, uç duvarları) · enerji zinciri + braketler · standart 4 m kablo · konnektör yeri (xj) · kelepçeler · QR sabitleri.
SÖZLEŞME (v1 ile aynı): kur() · PARCALAR · dunya(p) · BIRIMLER · BIRIM_MODUL · ON_BIRIMLER · MALZEME · RZ · RX_MONTAJ · RAY_X · XF · L_ZINCIR · x_min_etkin() · kablo_hesabi()
Çalıştır (öz denetim): python ob_calistir.py h3/h3_ray_ek_v2.py [hizli]
---------------- v1 notu (aşağısı v1'den, tarihçe) ----------------
HAT VERSİYON 2 · R · ROBOT RAYI EKLERİ ADAPTÖRÜ v1 (30 Eyl 2026 · Claude · YEREL) — ray_ek_cad_v1'in v2 kopyası (yalnız sol uca bağlı değerler değişti).
v2: robot yer rayı x 707,5–5100 (h3_hesap_v1.ROBOT_RAY_X · v1 200–5100) — hattın sol grubu 507,5 sağa kaydı, sağ uç (QR, zemin kanalı, 5100) SABİT.
DEĞİŞENLER (v1 → v2):
  · RAY_X / OLUK x: 200 → 707,5 (sağ uç 5100 aynı) → oluk tabanı + iki yan 4392,5 boy · sol uç duvarı 707,5–709,5 · robot merkezi aralığı 300 → 807,5 … 5000
  · XF (zincir sabit ucu) = RAY ORTASI (SPEC kuralı, v1'de de (200 + 5100) / 2): 2650 → 2903,75 → zincir boyu igus kuralıyla 2875 → 2625,
    montaj pozunda büküm merkezi 1448 → 1700 · sabit uç braketi 2903,75 · oluk kapakları (sabit kablo bölümü) XF + 2 … 5100 (3 × 730,1; v1 3 × 814,7)
  · v1'de XF = RX_MONTAJ olduğu için robot tarafındaki kablo noktaları (kaide yanı iniş M1–M3) ve 2 kablo kelepçesi "XF + …" yazılmıştı; bunlar ROBOTA
    bağlı → v2'de RX_MONTAJ + … (yerleri v1 ile BİREBİR aynı: 2695–2725 · 2710)
  · X_BAG = XF + 70 (sabit uçtan oluğa iniş) 2720 → 2973,75 · uzatma konnektörü (4 m standart kablo biter) hesapla sağa kayar · uzatma kablosu kısalır,
    artanı QR altındaki kangala geçer (sarım sayısı hesapla)
AYNI KALANLAR: RZ 360 · RX_MONTAJ 2650 (montaj robot konumu) · oluk sağ uç duvarı 5098–5100 · zemin kanalı + kapakları · QR sabitleri · hareketli uç braketi ·
  kablo kelepçeleri · zincir kesiti (VARSAYIM igus E2 iç 28 × 50, R 150) · kablo Ø20 · 4 m + 11 m.
SÖZLEŞME (v1 ile aynı): kur() · PARCALAR · dunya(p) · BIRIMLER · BIRIM_MODUL · ON_BIRIMLER · MALZEME · RZ · RX_MONTAJ · RAY_X · XF · L_ZINCIR · x_min_etkin() · kablo_hesabi()
KOORDİNAT: DÜNYA (X sağa · Y yukarı 0 = zemin · Z koridora doğru, modül ön yüzü +79). mm.
VARSAYIM (v1 ile aynı): kablo Ø20 · zincir iç 28 × 50, dış 40 × 64, R 150 · araba yarı boyu 100 · robot tabanı içinde 300 mm kablo.
"""
import math, os, sys, time

H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_hesap_v1 as H
import qr_cad_v1 as QR                    # yalnız sabitler (konnektör, geçiş, kangal bölgesi) · QR burada KURULMAZ
import h3_elk_qr_v1 as EQ                 # v2 · yalnız sabitler: tekmelik + giriş (a) (KEL 10|3) · QR elektrik katmanı burada KURULMAZ

# ---------------------------------------------------------------- ÖLÇÜLER (dünya) ----------------------------------------------------------------
RAY_X = tuple(H.ROBOT_RAY_X)              # v2: 707,5–5100 (v1 200–5100) · FR5 yer rayı
RZ = 360.0                                # ray ekseni (DEĞİŞMEZ) · ROBOT_RAY z 240–480
RAY_Z = (RZ - 120.0, RZ + 120.0)
OLUK = dict(x=RAY_X, y=(0.0, 60.0), z=(485.0, 575.0))    # v2: oluk rayla aynı boyda (sol uç 707,5) · y / z v1 ile aynı
OT = 2.0                                  # oluk sacı AISI 304 2 mm
KAPAK_T = 3.0                             # basılır kapak 3 mm gözyaşı desenli AISI 304
KABLO_D = 20.0                            # VARSAYIM (konnektör Ø26)
Z_H = dict(hG=40.0, bA=64.0, hi=28.0, bi=50.0, R=150.0, pay=25.0, adim=25.0)   # enerji zinciri VARSAYIM (igus E2 sınıfı)
ZC = (OLUK["z"][0] + OLUK["z"][1]) / 2.0  # 530 · zincir + kablo ekseni
Y_ALT = OT + Z_H["hG"] / 2.0              # 22 · alt kol ekseni (oluk tabanına oturur)
Y_UST = Y_ALT + 2.0 * Z_H["R"]            # 322 · üst kol ekseni
XF = (RAY_X[0] + RAY_X[1]) / 2.0          # v2: 2903,75 · sabit uç = RAY ORTASI (SPEC · v1 2650 = (200 + 5100) / 2)
RX_MONTAJ = 2650.0                        # montajda robot yeri (hareketli uç) · v1 ile AYNI (montaj RX)
ARABA_YARI = 100.0                        # VARSAYIM · robot merkezi 807,5…5000 (QR önünde 5000'de durur)
ROBOT_X = (RAY_X[0] + ARABA_YARI, RAY_X[1] - ARABA_YARI)
KAIDE_Z = 450.0                           # montaj ROBOT_1 kaide kutusu z 270–450 (ray ekseni ± 90)
ROBOT_IC = 300.0                          # VARSAYIM · robot kaidesi içinden FR5 taban konnektörüne
KABLO_TOPLAM, KABLO_STD, KABLO_UZ = 15000.0, 4000.0, 11000.0       # inluxrobotics.eu FR5: standart 4 m · uzatma 11 m
KONN_L, KONN_R = 110.0, 17.0              # birleşik konnektör çifti Ø34 × 110 VARSAYIM (Ø26 konnektör + kilit somunu)
# v2 · ZEMİN KANALI (KANAL / KT / KABLO_X_KANAL, y −60…0) KALKTI → oluk çıkışı + zemin ÜSTÜ köprü kanalı + QR tekmeliği girişi (a)
X_CIKIS = EQ.GIRIS_A["x"]                 # 5088 · robot kablosunun QR'ye girdiği x (kontrol kutusu 5070 ile kangal 5107,5 arası)
Y_GIRIS = EQ.GIRIS_A["y"]                 # 50 · KT 20 lastiğinin ekseni (KEL 10|3, tekmelik y 20–81)
Z_TEKME = EQ.TEKME["z"]                   # (670, 671,5) · tekmelik sacı (servis kapağı düzlemi)
R_CIKIS = 100.0                           # oluktan çıkış yayı (xz düzleminde) = 5 × d statik büküm
X_YAY0 = X_CIKIS - R_CIKIS                # 4988 · yay başı (oluk içinde, kablo z 530'da düz gelir)
YAY_YUKSELIS = 50.0                       # yayın son 40°'sinde kablo y 12 → 50 yükselir (oluk duvarı ağzından alçakta geçer)
OLUK_AGIZ = (5046.0, 5096.0)              # oluk koridor yanında çıkış ağzı · köprü kanalının iç genişliği
AGIZ_Y = 40.0                             # ağız y 2–40 (kablo geçerken üstü ≤ ~27) · 40–57 dudak kalır
KOPRU = dict(x=(5044.0, 5152.0), y=(0.0, 82.0), z=(575.0, Z_TEKME[0]), t=2.0, kapak=2.0)   # zemin ÜSTÜ köprü kanalı · kapak üstü 82 < servis kapağı altı 84
FLG = 1500.0                             # üst kolun kendini taşıyabildiği boy VARSAYIM (katalogla teyit)
X_ROB_AC = H.X_ROB_AC                     # 1207,5 · robot topu açıcıya bırakırken (zincirle erişilmeli)

# QR sabitleri (dünya) — v2'de QR yerinde
KONN_QR = (QR.X0 + QR.KONNEKTOR[0], QR.Y0 + QR.KONNEKTOR[1], QR.Z0 + QR.KONNEKTOR[2])      # (5070, 120, 900)
GECIS = (QR.X0 + QR.GECIS_ROBOT[0], QR.Z0 + QR.GECIS_ROBOT[1])                              # (4780, 975)
KG = dict(xc=QR.X0 + QR.KANGAL["xc"], zc=QR.Z0 + QR.KANGAL["zc"], ri=QR.KANGAL["r_ic"], rd=QR.KANGAL["r_dis"], y0=QR.Y0 + QR.KANGAL["y0"])
KG_RM = (KG["ri"] + KG["rd"]) / 2.0      # 125 · kangal ortalama yarıçapı (statik büküm ≥ 5 × d = 100 VARSAYIM)


def _s(v):
    t = ("%.2f" % v).replace(".", ",").rstrip("0").rstrip(",")
    return t


PARCALAR = []
MODUL = "-"                               # SPEC: zincir oluğu + enerji zinciri + köprü kanalı + robot kablosu modül "-" (R)
BIRIMLER = [
    ("ROBOT_ZINCIR_OLUGU", "Zincir oluğu · ray boyunca x %s–%s · z 485–575 · y 0–60 · AISI 304 2 mm · x %s–%s basılır kapaklı (sabit kablo), %s–%s açık (zincir buradan kalkar) · "
     "koridor yanında x %s–%s kablo çıkış ağzı · HAT v3.4"
     % (_s(OLUK["x"][0]), _s(OLUK["x"][1]), _s(XF), _s(OLUK["x"][1]), _s(OLUK["x"][0]), _s(XF), _s(OLUK_AGIZ[0]), _s(OLUK_AGIZ[1]))),
    ("ROBOT_ENERJI_ZINCIRI", "Enerji zinciri (igus E2 sınıfı, VARSAYIM iç 28 × 50, R 150) · sabit uç x %s (ray ortası) · hareketli uç robot kaidesinde · montaj konumunda (robot x %s) U katlı · HAT v2"
     % (_s(XF), _s(RX_MONTAJ))),
    ("ROBOT_KABLOSU", "Robot kablosu (Fairino FR5 kol ↔ kontrol kutusu, tek kablo) · standart 4 m + uzatma 11 m = 15 m · oluk → köprü kanalı → QR tekmeliği (KEL 10|3) → QR içinde kangal"),
    ("ROBOT_KABLO_KOPRUSU", "Robot kablosu köprü kanalı · ZEMİNİN ÜSTÜNDE (gömme yok) · AISI 304 2 mm + 2 mm vidalı kapak · x %s–%s · y 0–%s · z 575 (oluk koridor yanı) – %s (QR tekmeliği) · HAT v3.4"
     % (_s(KOPRU["x"][0]), _s(KOPRU["x"][1]), _s(KOPRU["y"][1]), _s(KOPRU["z"][1]))),
]
BIRIM_MODUL = {k: MODUL for k, _a in BIRIMLER}
ON_BIRIMLER = tuple(k for k, _a in BIRIMLER)     # hepsi hattın önünde (z > 0) · ROBOT_ öneki montajın ÖN YÜZ istisnasında VAR (v2: ZEMIN_KANALI yok)
MALZEME = {"paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30), "zincir": dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.0, ruf=0.55),
           "kablo": dict(renk=(0.95, 0.55, 0.10, 1.0), met=0.0, ruf=0.6), "konnektor": dict(renk=(0.55, 0.56, 0.58, 1.0), met=0.8, ruf=0.35),
           "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35), "plastik": dict(renk=(0.12, 0.12, 0.13, 1.0), met=0.0, ruf=0.6)}


def kut(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ", origin=(min(x0, x1), y, z)).circle(r).extrude(abs(x1 - x0))


def boru(pts, r):
    """nokta dizisi boyunca boru (silindir + dirsek küreleri) · uçlarda küre YOK"""
    ss = []
    for a, b in zip(pts[:-1], pts[1:]):
        v = cq.Vector(*b) - cq.Vector(*a)
        if v.Length > 1e-6: ss.append(cq.Solid.makeCylinder(r, v.Length, cq.Vector(*a), v.normalized()))
    for p in pts[1:-1]: ss.append(cq.Solid.makeSphere(r, cq.Vector(*p), angleDegrees1=-90, angleDegrees2=90))
    return cq.Workplane(obj=cq.Compound.makeCompound(ss))


def uzunluk(pts):
    return sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))


def ekle(ad, wp, mal, birim, bom=None, grup="SABIT", kaynak=""):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom))


def dunya(p):
    v = p["wp"].vals()
    return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])


# ---------------------------------------------------------------- ENERJİ ZİNCİRİ HESABI (v1 ile aynı formüller) ----------------------------------------------------------------
def zincir_boyu():
    """igus uzun yol kuralı: sabit uç ortada → L = (en uzak strok yarısı) + πR + 2 × güvenlik payı · adıma yuvarlanır"""
    R = Z_H["R"]
    L0 = max(ROBOT_X[1] - XF, XF - ROBOT_X[0]) + math.pi * R + 2.0 * Z_H["pay"]
    return math.ceil(L0 / Z_H["adim"]) * Z_H["adim"]


L_ZINCIR = zincir_boyu()                  # v2 2625 (v1 2875)


def donus_x(xm):
    """dönüş (büküm) merkezinin x'i · büküm SOL (−x) tarafta: alt kol xc…XF, üst kol xc…xm"""
    return (XF + xm - L_ZINCIR + math.pi * Z_H["R"]) / 2.0


def x_min_etkin():
    """büküm dış kenarı oluk sol uç duvarına (iç yüz 709,5) 5 mm kalana dek → robotun zincirle gidebildiği en sol x"""
    sinir = OLUK["x"][0] + OT + 5.0 + Z_H["R"] + Z_H["hG"] / 2.0
    return 2.0 * sinir - XF + L_ZINCIR - math.pi * Z_H["R"]


def zincir_yolu(xm=RX_MONTAJ, n=24):
    """zincir tarafsız ekseni (dünya): sabit uç XF → alt kol → büküm → üst kol → hareketli uç xm"""
    xc = donus_x(xm); R = Z_H["R"]; yc = (Y_ALT + Y_UST) / 2.0
    pts = [(XF, Y_ALT, ZC), (xc, Y_ALT, ZC)]
    for i in range(1, n):
        a = -math.pi / 2.0 - math.pi * i / n                  # alttan (−90°) sola (−180°) üste (−270°)
        pts.append((xc + R * math.cos(a), yc + R * math.sin(a), ZC))
    pts += [(xc, Y_UST, ZC), (xm, Y_UST, ZC)]
    return pts


# ---------------------------------------------------------------- KABLO YOLU ----------------------------------------------------------------
Y_OLUK = OT + KABLO_D / 2.0                        # 12 · kablo oluk tabanında (v2: zemin kanalı Y_KANAL −48 KALKTI)
Y_QR = QR.TABAN[1] + KABLO_D / 2.0                 # 30 · kablo QR taban plakası üstünde
Y_KONN = OT + KONN_R                               # 19 · konnektör oluk tabanına oturur
X_BAG = XF + 70.0                                  # v2 2973,75 (v1 2720) · sabit uçtan oluğa iniş
X_ROB_KABLO = RX_MONTAJ + 60.0                     # 2710 · robot kaidesi yanında kablonun indiği x (v1'de "XF + 60" yazılıydı; XF = RX_MONTAJ idi)
RP = {}                                            # v2 · uzatma A nokta indeksleri (yay sonu · giriş) — kablo_hesabi bölümleri için


def rota_parcalari(N=None):
    """(robot tarafı standart parça, uzatma parça A [konnektör → kangal altı], uzatma parça B [kangal üstü → kontrol kutusu], xj, N)
    xj (konnektör ortası) standart kablo 4 m olacak şekilde, N (kangal sarım sayısı) uzatma 11 m olacak şekilde çözülür."""
    zy = zincir_yolu()
    # robot ucu → sabit uç (ters sırada) · v2: robot tarafı noktaları ROBOTA bağlı (RX_MONTAJ + 60)
    M3, M2, M1 = (X_ROB_KABLO, 800.0, 470.0), (X_ROB_KABLO, Y_UST, 470.0), (X_ROB_KABLO, Y_UST, ZC)
    robot = [M3, M2, M1] + list(reversed(zy)) + [(XF + 50.0, Y_ALT, ZC), (X_BAG, Y_OLUK, ZC)]
    L_rob = ROBOT_IC + uzunluk(robot)
    rampa = math.hypot(25.0, Y_KONN - Y_OLUK)
    # standart = L_rob + (xj − 95 − X_BAG) + rampa + 15 (düz giriş: dirsek küresi konnektöre girmesin) + KONN_L/2 = 4000
    xj = X_BAG + 95.0 + (KABLO_STD - KONN_L / 2.0 - 15.0 - rampa - L_rob)
    std = robot + [(xj - 95.0, Y_OLUK, ZC), (xj - 70.0, Y_KONN, ZC), (xj - KONN_L / 2.0, Y_KONN, ZC)]
    # v2 · oluk içinde X_YAY0'a kadar düz → R_CIKIS yayı (xz) koridor yanından çıkar, son 40°'de y Y_OLUK → Y_GIRIS → köprü kanalı → tekmelik girişi (a) düz →
    #      QR içinde kontrol kutusu ile kangal arasından inip kangal alt ucuna (eski: K8 → zemin kanalı y −48 → QR tabanından Ø40 rakor → K4 → Eb)
    Eb = (KG["xc"] - KG_RM, KG["y0"] + KABLO_D / 2.0, KG["zc"])
    A = [(xj + KONN_L / 2.0, Y_KONN, ZC), (xj + 70.0, Y_KONN, ZC), (xj + 95.0, Y_OLUK, ZC), (X_YAY0, Y_OLUK, ZC)]
    n_yay = 18
    for i in range(1, n_yay + 1):
        th = math.pi / 2.0 * i / n_yay
        f = max(0.0, (math.degrees(th) - YAY_YUKSELIS) / (90.0 - YAY_YUKSELIS)); f = f * f * (3.0 - 2.0 * f)       # yumuşak yükseliş (smoothstep)
        A.append((X_YAY0 + R_CIKIS * math.sin(th), Y_OLUK + (Y_GIRIS - Y_OLUK) * f, ZC + R_CIKIS - R_CIKIS * math.cos(th)))
    I_YAY_SON = len(A) - 1                                   # (X_CIKIS, Y_GIRIS, ZC + R) · köprü kanalında, tekmeliğe doğru düz
    A += [(X_CIKIS, Y_GIRIS, Z_TEKME[1] + 28.5),            # tekmelikten (KT 20 lastiği z 653–670) düz geçip 28,5 içeride
          (Eb[0], Y_QR, Eb[2] - 50.0), Eb]                  # kontrol kutusu (x ≤ 5070) ile kangal arası iniş → kangal alt ucu (teğet, z yönünde)
    RP["I_YAY_SON"] = I_YAY_SON; RP["I_GIRIS"] = I_YAY_SON + 1
    K1 = (KONN_QR[0] + 20.0, KONN_QR[1], KONN_QR[2])
    if N is None:
        N = 10.0
    for _i in range(8):                                   # kangal üst ucu N'ye bağlı → yakınsat
        Et = (KG["xc"] - KG_RM, KG["y0"] + N * KABLO_D - KABLO_D / 2.0, KG["zc"])
        B = [Et, K1, KONN_QR]
        kangal = KABLO_UZ - KONN_L / 2.0 - uzunluk(A) - uzunluk(B)
        N = kangal / (2.0 * math.pi * KG_RM)
    return std, A, B, xj, N


def kablo_hesabi():
    std, A, B, xj, N = rota_parcalari()
    L_std = ROBOT_IC + uzunluk(std) + KONN_L / 2.0
    kangal = N * 2.0 * math.pi * KG_RM
    L_uz = KONN_L / 2.0 + uzunluk(A) + kangal + uzunluk(B)
    zy = zincir_yolu()
    i1, i2 = RP["I_YAY_SON"], RP["I_GIRIS"]
    bol = [("robot tabanı içi (VARSAYIM)", ROBOT_IC), ("kaide yanı + araba braketi", uzunluk(std[:3]) + math.dist(std[2], zy[-1])),
           ("enerji zinciri (L)", uzunluk(zy)), ("oluk: sabit uç → konnektör", uzunluk(std[3 + len(zy) - 1:]) + KONN_L / 2.0),
           ("oluk: konnektör → çıkış yayı başı (x %.0f)" % X_YAY0, KONN_L / 2.0 + uzunluk(A[:4])),
           ("oluk çıkışı R %.0f yayı + köprü kanalı (zemin ÜSTÜ)" % R_CIKIS, uzunluk(A[3:i1 + 1])),
           ("köprü ucu → tekmelik girişi (a) KEL 10|3 → kangal altı", uzunluk(A[i1:])), ("KANGAL %.2f sarım × Ø%.0f" % (N, 2 * KG_RM), kangal), ("QR içi: kangal üstü → kontrol kutusu", uzunluk(B))]
    gerekli = sum(v for a_, v in bol if not a_.startswith("KANGAL"))
    return dict(std=std, A=A, B=B, xj=xj, N=N, L_std=L_std, L_uz=L_uz, kangal=kangal, bol=bol, gerekli=gerekli)


# ---------------------------------------------------------------- 1 · ZİNCİR OLUĞU ----------------------------------------------------------------
def oluk():
    b = "ROBOT_ZINCIR_OLUGU"
    x0, x1 = OLUK["x"]; z0, z1 = OLUK["z"]; yk = OLUK["y"][1] - KAPAK_T
    tb = kut(x0, x1, 0.0, OT, z0, z1)                                     # v2 · zemin kanalı ağzı (30 × 36) KALKTI — tabanda delik yok
    ekle("oluk_tabani", tb, "paslanmaz", b, bom=("Zincir oluğu U profil AISI 304 2 mm (taban + 2 yan)", 1, "%s × 90 × 57 · 2 parça (%s) · koridor yanında çıkış ağzı %s × %s" % (_s(x1 - x0), _s((x1 - x0) / 2.0), _s(OLUK_AGIZ[1] - OLUK_AGIZ[0]), _s(AGIZ_Y - OT)), "üretim (abkant)", "ÜRETİM"))
    ekle("oluk_yan_robot", kut(x0, x1, OT, yk, z0, z0 + OT), "paslanmaz", b)
    ekle("oluk_yan_koridor", kut(x0, x1, OT, yk, z1 - OT, z1).cut(kut(OLUK_AGIZ[0], OLUK_AGIZ[1], OT - 1.0, AGIZ_Y, z1 - OT - 1.0, z1 + 1.0)), "paslanmaz", b)   # v2 · köprü kanalına çıkış ağzı (üstte 17 mm dudak: yan tek parça)
    ekle("oluk_uc_duvari_sol", kut(x0, x0 + OT, OT, yk, z0 + OT, z1 - OT), "paslanmaz", b, bom=("Oluk uç kapağı 2 mm", 2, "86 × 55", "üretim", "ÜRETİM"))
    ekle("oluk_uc_duvari_sag", kut(x1 - OT, x1, OT, yk, z0 + OT, z1 - OT), "paslanmaz", b)
    # basılır kapaklar: yalnız sabit kablo bölümü (XF + 2 … 5100) · zincir bölümü açık (zincir buradan kalkar)
    a0 = XF + 2.0; n = 3; Lk = (x1 - a0 - 2.0 * (n - 1)) / n
    for i in range(n):
        xa = a0 + i * (Lk + 2.0)
        ekle("oluk_kapagi_%d" % i, kut(xa, xa + Lk, yk, OLUK["y"][1], z0, z1), "paslanmaz", b,
             bom=("Oluk kapağı 3 mm gözyaşı desenli AISI 304 (üstüne basılır)", n, "%.0f × 90" % Lk, "üretim · 2 × M5 havşa", "ÜRETİM") if i == 0 else None)
    return Lk


# ---------------------------------------------------------------- 2 · ENERJİ ZİNCİRİ ----------------------------------------------------------------
def zincir():
    b = "ROBOT_ENERJI_ZINCIRI"
    hG, bA, hi, bi, R = Z_H["hG"], Z_H["bA"], Z_H["hi"], Z_H["bi"], Z_H["R"]
    xc = donus_x(RX_MONTAJ); yc = (Y_ALT + Y_UST) / 2.0
    za, zb, ia, ib = ZC - bA / 2.0, ZC + bA / 2.0, ZC - bi / 2.0, ZC + bi / 2.0
    alt = kut(xc, XF, Y_ALT - hG / 2.0, Y_ALT + hG / 2.0, za, zb).cut(kut(xc - 1.0, XF + 1.0, Y_ALT - hi / 2.0, Y_ALT + hi / 2.0, ia, ib))
    ust = kut(xc, RX_MONTAJ, Y_UST - hG / 2.0, Y_UST + hG / 2.0, za, zb).cut(kut(xc - 1.0, RX_MONTAJ + 1.0, Y_UST - hi / 2.0, Y_UST + hi / 2.0, ia, ib))
    halka = silz(xc, yc, R + hG / 2.0, za, zb).cut(silz(xc, yc, R - hG / 2.0, za - 1, zb + 1)).cut(kut(xc, xc + R + hG, yc - R - hG, yc + R + hG, za - 1, zb + 1))
    halka = halka.cut(silz(xc, yc, R + hi / 2.0, ia, ib).cut(silz(xc, yc, R - hi / 2.0, ia - 1, ib + 1)))
    ekle("enerji_zinciri", alt.union(halka).union(ust), "zincir", b,
         bom=("Enerji zinciri igus E2 sınıfı · iç 28 × 50 · dış 40 × 64 · R 150", 1, "boy %.0f (strok yarısı %.0f + πR %.0f + 2 × %.0f pay)" % (L_ZINCIR, max(ROBOT_X[1] - XF, XF - ROBOT_X[0]), math.pi * R, Z_H["pay"]),
              "VARSAYIM ölçü · igus.com.tr seçim (uzun yol, üst kol desteği gerekir)", "SATIN ALMA"))
    # sabit uç braketi (oluk tabanına) · hareketli uç braketi (robot kaidesine)
    sb = kut(XF, XF + 40.0, OT, OT + 44.0, ZC - 40.0, ZC + 40.0).cut(silx(Y_ALT, ZC, 12.0, XF - 1.0, XF + 41.0))
    ekle("zincir_sabit_uc_braketi", sb, "celik", b, bom=("Zincir bağlantı braketi (sabit uç, oluk tabanına 2 × M6)", 1, "40 × 44 × 80", "igus KMA sınıfı VARSAYIM", "SATIN ALMA"))
    hb = kut(RX_MONTAJ, RX_MONTAJ + 40.0, Y_UST - 22.0, Y_UST + 22.0, ZC - 38.0, ZC + 38.0).cut(silx(Y_UST, ZC, 12.0, RX_MONTAJ - 1.0, RX_MONTAJ + 41.0))
    hb = hb.union(kut(RX_MONTAJ, RX_MONTAJ + 40.0, Y_UST + 22.0, Y_UST + 28.0, KAIDE_Z + 0.5, ZC + 38.0))
    hb = hb.union(kut(RX_MONTAJ, RX_MONTAJ + 40.0, Y_UST - 22.0, Y_UST + 128.0, KAIDE_Z + 0.5, KAIDE_Z + 6.5))
    ekle("zincir_hareketli_uc_braketi", hb, "celik", b, bom=("Zincir hareketli uç braketi + kaide kolu 6 mm", 1, "robot kaidesine 4 × M8", "üretim (lazer + büküm)", "ÜRETİM"))
    return xc


# ---------------------------------------------------------------- 3 · v2 KÖPRÜ KANALI (zemin ÜSTÜ · oluk koridor yanı → QR tekmeliği) ----------------------------------------------------------------
# v1'in ZEMİN KANALI (şapa gömülü y −60…0, x 4760–4840, z 490–1000 · 8 parça) KALKTI (Kemal 1 Eki: zemin altına hiçbir şey gömülmez).
def kopru():
    b = "ROBOT_KABLO_KOPRUSU"
    x0, x1 = KOPRU["x"]; y0, y1 = KOPRU["y"]; z0, z1 = KOPRU["z"]; t = KOPRU["t"]; yk = y1 - KOPRU["kapak"]
    ekle("kopru_tabani", kut(x0, x1, y0, y0 + t, z0, z1), "paslanmaz", b,
         bom=("Köprü kanalı AISI 304 2 mm (taban + 2 yan + 2 arka parça) · zincir oluğu ↔ QR tekmeliği · ZEMİN ÜSTÜ", 1,
              "%s × %s × %s" % (_s(x1 - x0), _s(z1 - z0), _s(yk)), "üretim (lazer + abkant) · oluğa 4 × M5 perçin somun · zemine gömme / dübel YOK", "ÜRETİM"))
    ekle("kopru_yan_sol", kut(x0, x0 + t, y0 + t, yk, z0, z1), "paslanmaz", b)
    ekle("kopru_yan_sag", kut(x1 - t, x1, y0 + t, yk, z0, z1), "paslanmaz", b)
    ekle("kopru_arka_ust", kut(x0 + t, OLUK_AGIZ[1], OLUK["y"][1] - KAPAK_T, yk, z0, z0 + t), "paslanmaz", b)        # oluk kapağının üstü (oluk ağzının üstü kapalı)
    ekle("kopru_arka_sag", kut(OLUK_AGIZ[1], x1 - t, y0 + t, yk, z0, z0 + t), "paslanmaz", b)                      # oluk sağ ucunun ötesi
    ekle("kopru_kapagi", kut(x0, x1, yk, y1, z0, z1), "paslanmaz", b,
         bom=("Köprü kanalı kapağı AISI 304 2 mm (vidalı · üstüne basılabilir)", 1, "%s × %s" % (_s(x1 - x0), _s(z1 - z0)),
              "üretim · 4 × M5 havşa · üstü y %s < servis kapağı altı %s" % (_s(y1), _s(EQ.KAPI_Y[0])), "ÜRETİM"))


# ---------------------------------------------------------------- 4 · ROBOT KABLOSU ----------------------------------------------------------------
def kablo():
    b = "ROBOT_KABLOSU"
    h = kablo_hesabi()
    r = KABLO_D / 2.0
    ekle("robot_kablosu_standart_4m", boru(h["std"], r), "kablo", b,
         bom=("Fairino robot kablosu (standart, robotla gelir)", 1, "4 m · güç + haberleşme tek kablo · Ø26 dairesel konnektör", "inluxrobotics.eu FR5 · çap VARSAYIM Ø20", "SATIN ALMA"))
    ekle("robot_kablosu_uzatma_A", boru(h["A"], r), "kablo", b,
         bom=("Fairino uzatma kablosu 11 m", 1, "standart kabloyla toplam 15 m", "inluxrobotics.eu (Fairino Extension Cable 11 m)", "SATIN ALMA"))
    ekle("robot_kablosu_uzatma_B", boru(h["B"], r), "kablo", b)
    xj = h["xj"]
    ekle("uzatma_konnektoru", silx(Y_KONN, ZC, KONN_R, xj - KONN_L / 2.0, xj + KONN_L / 2.0), "konnektor", b,
         bom=("Kablo birleşimi (Ø26 dairesel konnektör çifti) · oluk içinde", 1, "zarf Ø34 × 110", "VARSAYIM zarf", "ALT"))
    yk = KG["y0"] + h["N"] * KABLO_D
    ekle("robot_kablosu_kangal", sily(KG["xc"], KG["zc"], KG["rd"], KG["y0"], yk).cut(sily(KG["xc"], KG["zc"], KG["ri"], KG["y0"] - 1.0, yk + 1.0)), "kablo", b,
         bom=("Kablo kangalı (uzatmanın artanı) · QR alt bölmesi · 4 cırt bant", 1, "%.2f sarım × Ø%.0f · %.2f m · yük. %.0f" % (h["N"], 2 * KG_RM, h["kangal"] / 1000.0, h["N"] * KABLO_D), "hesap (bu dosya)", "ALT"))
    for i, yy in enumerate((520.0, 720.0)):                  # v2: robot kaidesine bağlı → RX_MONTAJ (v1 "XF + …", XF = RX_MONTAJ idi · yer aynı)
        ekle("kablo_kelepcesi_%d" % i, kut(RX_MONTAJ + 45.0, RX_MONTAJ + 75.0, yy, yy + 20.0, KAIDE_Z + 0.5, 485.0).cut(sily(X_ROB_KABLO, 470.0, r + 0.5, yy - 1.0, yy + 21.0)), "plastik", b,
             bom=("Kablo kelepçesi (robot kaidesine)", 2, "Ø21", "katalog", "SATIN ALMA") if i == 0 else None)
    return h


def kur():
    """İDEMPOTENT: her çağrıda baştan kurar · PARCALAR nesnesi aynı kalır"""
    PARCALAR[:] = []
    oluk(); zincir(); kopru(); kablo()                 # v2 · kanal() (zemin kanalı) yerine kopru()
    return PARCALAR


# ---------------------------------------------------------------- DENETİM ----------------------------------------------------------------
ISTISNA = [("robot_kablosu_kangal", "robot_kablosu_uzatma")]     # kangal = uzatmanın kendisi (uçlar kangal halkasına girer) · v1 ile aynı


def _ist(a, b):
    return any((p in a and q in b) or (p in b and q in a) for p, q in ISTISNA)


def _bbk(A, B, pay=0.01):
    return A.xmin < B.xmax - pay and B.xmin < A.xmax - pay and A.ymin < B.ymax - pay and B.ymin < A.ymax - pay and A.zmin < B.zmax - pay and B.zmin < A.zmax - pay


def kendi_arasinda(ps, esik=1.0):
    S = [(p["ad"], dunya(p)) for p in ps]; S = [(a, s, s.BoundingBox()) for a, s in S]
    out = []
    for i, (a, sa, A) in enumerate(S):
        for c, sc, B in S[i + 1:]:
            if not _bbk(A, B) or _ist(a, c):
                continue
            v = sa.intersect(sc).Volume()
            if v > esik: out.append((round(v, 3), a, c))
    return out


DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-150s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))


def y_alti_hacmi(sh):
    """parçanın zemin altında (y < 0) kalan hacmi (gerçek kesişim · sınır kutusu şişmesine bakmaz)"""
    b = sh.BoundingBox()
    if b.ymin >= 0.0: return 0.0
    k = cq.Solid.makeBox(b.xlen + 20.0, 1000.0, b.zlen + 20.0, cq.Vector(b.xmin - 10.0, -1000.0, b.zmin - 10.0))
    return sh.intersect(k).Volume()


if __name__ == "__main__":
    t0 = time.time(); arg = sys.argv[1:]
    kimlik = id(PARCALAR)
    kur(); ps = kur()
    gec = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("RAY EKLERİ v2 (h3_ray_ek_v2 · HAT v3.4) · %d parça · katı denetimi: %s · %.0f sn" % (len(ps), "hepsi geçerli" if not gec else gec, time.time() - t0))
    for kod, _a in BIRIMLER:
        q = [dunya(p).BoundingBox() for p in ps if p["birim"] == kod]
        print("   %-22s %2d parça · x %.1f–%.1f · y %.1f–%.1f · z %.1f–%.1f" % (kod, len(q), min(v.xmin for v in q), max(v.xmax for v in q), min(v.ymin for v in q), max(v.ymax for v in q), min(v.zmin for v in q), max(v.zmax for v in q)))
    print("DENETİM (h3_ray_ek_v2)")
    kontrol("katılar geçerli · kur() iki kez → %d parça (v1 26 − zemin kanalı 8 + köprü 6 = 24), PARCALAR nesnesi aynı (idempotent)" % len(ps), not gec and ps is PARCALAR and id(PARCALAR) == kimlik and len(ps) == 24, ", ".join(gec))
    # ZEMİN ALTI YOK (Kemal 1 Eki): her parçanın y < 0 hacmi 0 (gerçek kesişim)
    alt = [(p["ad"], round(y_alti_hacmi(dunya(p)), 3)) for p in ps]
    alt = [a for a in alt if a[1] > 1e-6]
    kontrol("ZEMİN ALTINDA PARÇA YOK: %d parçanın hiçbirinin y < 0 hacmi yok (gerçek kesişim)" % len(ps), not alt, str(alt))
    kontrol("ZEMIN_KANALI birimi ve kanal_* parçaları yok", not any(p["birim"] == "ZEMIN_KANALI" or p["ad"].startswith("kanal_") for p in ps))
    ob = [dunya(p).BoundingBox() for p in ps if p["birim"] == "ROBOT_ZINCIR_OLUGU"]
    kontrol("zincir oluğu x %.1f–%.1f · y %.0f–%.0f · z %.0f–%.0f (ray x %.1f–%.0f · y 0–60 · z 485–575)" % (min(v.xmin for v in ob), max(v.xmax for v in ob), min(v.ymin for v in ob), max(v.ymax for v in ob), min(v.zmin for v in ob), max(v.zmax for v in ob), RAY_X[0], RAY_X[1]),
            abs(min(v.xmin for v in ob) - RAY_X[0]) < 0.01 and abs(max(v.xmax for v in ob) - RAY_X[1]) < 0.01 and abs(min(v.ymin for v in ob)) < 0.01 and abs(max(v.ymax for v in ob) - 60) < 0.01
            and abs(min(v.zmin for v in ob) - 485) < 0.01 and abs(max(v.zmax for v in ob) - 575) < 0.01)
    xmin_hep = min(dunya(p).BoundingBox().xmin for p in ps)
    kontrol("SOL UÇ: bütün ray eki parçaları x ≥ %.1f (ray başı) · en sol parça x %.2f · rayın solunda parça YOK" % (RAY_X[0], xmin_hep), xmin_hep >= RAY_X[0] - 1e-6)
    kontrol("oluk ↔ robot rayı (ROBOT_RAY z %.0f–%.0f) arası %.0f mm" % (RAY_Z[0], RAY_Z[1], OLUK["z"][0] - RAY_Z[1]), OLUK["z"][0] - RAY_Z[1] >= 5.0)
    kb = [dunya(p).BoundingBox() for p in ps if p["birim"] == "ROBOT_KABLO_KOPRUSU"]
    kbx = (min(v.xmin for v in kb), max(v.xmax for v in kb)); kby = (min(v.ymin for v in kb), max(v.ymax for v in kb)); kbz = (min(v.zmin for v in kb), max(v.zmax for v in kb))
    kontrol("köprü kanalı x %.0f–%.0f · y %.1f–%.1f · z %.0f–%.0f: oluk koridor yanından (575) QR tekmeliğine (%.0f) · zeminin üstünde · üstü < servis kapağı altı %.0f"
            % (kbx + kby + kbz + (Z_TEKME[0], EQ.KAPI_Y[0])),
            abs(kbz[0] - OLUK["z"][1]) < 0.01 and abs(kbz[1] - Z_TEKME[0]) < 0.01 and kby[0] >= -1e-6 and kby[1] < EQ.KAPI_Y[0])
    fa = EQ.arayuz()["a_cerceve"]
    kontrol("giriş (a) KEL 10|3 çerçevesi x %.1f–%.1f · y %.0f–%.0f · z %.0f–%.0f köprü kanalının İÇİNDE (iç x %.0f–%.0f · y %.0f–%.0f)"
            % (fa + (kbx[0] + KOPRU["t"], kbx[1] - KOPRU["t"], KOPRU["t"], KOPRU["y"][1] - KOPRU["kapak"])),
            fa[0] >= kbx[0] + KOPRU["t"] and fa[1] <= kbx[1] - KOPRU["t"] and fa[2] >= KOPRU["t"] and fa[3] <= KOPRU["y"][1] - KOPRU["kapak"] and fa[4] >= kbz[0])
    # enerji zinciri (v1 ile aynı)
    R, hG = Z_H["R"], Z_H["hG"]
    zy = zincir_yolu()
    kontrol("zincir ekseni boyu = L (%.1f = %.0f)" % (uzunluk(zy), L_ZINCIR), abs(uzunluk(zy) - L_ZINCIR) < 2.0)
    kontrol("zincir sabit ucu XF %.2f = ray ortası" % XF, abs(XF - (RAY_X[0] + RAY_X[1]) / 2.0) < 1e-9)
    kontrol("robot x %.0f (QR önü): alt kol %.1f ≥ güvenlik payı %.0f" % (ROBOT_X[1], XF - donus_x(ROBOT_X[1]), Z_H["pay"]), XF - donus_x(ROBOT_X[1]) >= Z_H["pay"] - 0.01)
    xme = x_min_etkin()
    kontrol("robot açıcıya bırakma konumu x %.1f ≥ zincirle gidilebilen en sol x %.2f → açıcıya ERİŞİR" % (X_ROB_AC, xme), X_ROB_AC >= xme)
    zb_ = [dunya(p).BoundingBox() for p in ps if p["ad"] == "enerji_zinciri"][0]
    kontrol("montaj pozunda zincir x %.2f–%.2f oluğun içinde" % (zb_.xmin, zb_.xmax), zb_.xmin >= OLUK["x"][0] + OT + 5.0 - 1e-6 and zb_.xmax <= OLUK["x"][1] - OT)
    # kablo
    h = kablo_hesabi()
    print("ROBOT KABLOSU (modellenen yol boyunca, eksen):")
    for a_, v in h["bol"]:
        print("   %-56s %7.0f mm" % (a_, v))
    print("   %-56s %7.0f mm" % ("GEREKLİ (kangal hariç)", h["gerekli"]))
    print("   standart parça %.1f (hedef %.0f) · uzatma %.1f (hedef %.0f) · toplam %.1f · konnektör oluk içinde x %.2f" % (h["L_std"], KABLO_STD, h["L_uz"], KABLO_UZ, h["L_std"] + h["L_uz"], h["xj"]))
    kontrol("standart kablo = %.1f (4 m) · uzatma = %.1f (11 m) · konnektör x %.1f–%.1f oluğun kapaklı bölümünde (XF + 2 = %.1f … çıkış yayı başı %.0f)"
            % (h["L_std"], h["L_uz"], h["xj"] - KONN_L / 2.0, h["xj"] + KONN_L / 2.0, XF + 2.0, X_YAY0),
            abs(h["L_std"] - KABLO_STD) < 1.0 and abs(h["L_uz"] - KABLO_UZ) < 1.0 and XF + 2.0 <= h["xj"] - KONN_L / 2.0 and h["xj"] + 95.0 <= X_YAY0)
    kontrol("bölümler toplamı = kablo boyu: gerekli %.1f + kangal %.1f = 15 m (%.1f)" % (h["gerekli"], h["kangal"], h["gerekli"] + h["kangal"]), abs(h["gerekli"] + h["kangal"] - KABLO_TOPLAM) < 1.0)
    kontrol("Fairino standart 4 m YETMEZ: gereken %.2f m > 4 m" % (h["gerekli"] / 1000.0), h["gerekli"] > KABLO_STD)
    kontrol("4 m + 11 m uzatma = 15 m yeter: gereken %.2f m · artan %.2f m kangalda" % (h["gerekli"] / 1000.0, h["kangal"] / 1000.0),
            h["gerekli"] <= KABLO_TOPLAM and abs(h["L_std"] + h["L_uz"] - KABLO_TOPLAM) < 1.0)
    yk = KG["y0"] + h["N"] * KABLO_D
    kontrol("kangal %.2f sarım · Ø%.0f · yükseklik %.0f → y %.0f–%.1f QR bölgesinde (y ≤ %.0f · fan altı %.0f)" % (h["N"], 2 * KG_RM, h["N"] * KABLO_D, KG["y0"], yk,
            QR.KANGAL_BOLGE["y"][1], QR.FAN["alt"][2]), yk <= QR.KANGAL_BOLGE["y"][1] and yk < QR.FAN["alt"][2])
    kontrol("kangal x %.1f–%.1f · z %.0f–%.0f QR kangal bölgesinde (x 5080–5405)" % (KG["xc"] - KG["rd"], KG["xc"] + KG["rd"], KG["zc"] - KG["rd"], KG["zc"] + KG["rd"]),
            KG["xc"] - KG["rd"] >= QR.X0 + QR.KANGAL_BOLGE["x"][0] and KG["xc"] + KG["rd"] <= QR.X0 + QR.KANGAL_BOLGE["x"][1])
    kontrol("büküm yarıçapları: zincir R %.0f = %.1f × d · kangal %.0f = %.1f × d · oluk çıkış yayı R %.0f = %.1f × d (statik ≥ 5 × d)"
            % (R, R / KABLO_D, KG_RM, KG_RM / KABLO_D, R_CIKIS, R_CIKIS / KABLO_D), R >= 7.5 * KABLO_D and KG_RM >= 5.0 * KABLO_D and R_CIKIS >= 5.0 * KABLO_D)
    A_ = h["A"]; gi = [p_ for p_ in A_ if abs(p_[0] - X_CIKIS) < 1e-6 and abs(p_[1] - Y_GIRIS) < 1e-6]
    kontrol("uzatma A tekmelikten x %.1f · y %.1f'de DİK (z yönünde) geçer: giriş (a) KT 20 ekseni (h3_elk_qr_v1.GIRIS_A) · kesik %s içinde" % (X_CIKIS, Y_GIRIS, EQ.GIRIS_A["kesik"]),
            len(gi) >= 2 and min(p_[2] for p_ in gi) < Z_TEKME[0] - EQ.GIRIS_A["H"] and max(p_[2] for p_ in gi) > Z_TEKME[1])
    kontrol("QR içinde uzatma A kontrol kutusunun (x ≤ %.0f) ve kangalın dış yüzünün solunda: kablo kenarı x ≥ %.1f" % (QR.X0 + QR.KONTROL["x"][1], X_CIKIS - KABLO_D / 2.0),
            X_CIKIS - KABLO_D / 2.0 > QR.X0 + QR.KONTROL["x"][1] + 5.0)
    kontrol("kablo zincir iç kesitine sığar (Ø%.0f ≤ iç %.0f × %.0f, %%10 pay)" % (KABLO_D, Z_H["hi"], Z_H["bi"]), KABLO_D * 1.1 <= Z_H["hi"] and KABLO_D * 1.1 <= Z_H["bi"])
    kontrol("hareketli uç braketi kaide yüzünün (z %.0f) önünde" % KAIDE_Z, min(dunya(p).BoundingBox().zmin for p in ps if p["ad"] == "zincir_hareketli_uc_braketi") >= KAIDE_Z)
    t1 = time.time()
    cak = kendi_arasinda(ps, esik=0.1)
    print("KENDİ ARASINDA (> 0,1 mm³): %s · %.0f sn" % ("TEMİZ" if not cak else cak[:20], time.time() - t1))
    kontrol("kendi arasında çakışma = 0 (%d parça · > 0,1 mm³ · istisna: kangal = uzatmanın kendisi)" % len(ps), not cak, str(cak[:6]))
    # h3_ray_ek_v1 karşılaştırması: zemin kanalı çıktı · köprü geldi · yalnız çıkış ucu değişti
    import h3_ray_ek_v1 as R1
    R1.kur()
    b1 = {p["ad"]: (R1.dunya(p).BoundingBox(), R1.dunya(p).Volume()) for p in R1.PARCALAR}
    b2 = {p["ad"]: (dunya(p).BoundingBox(), dunya(p).Volume()) for p in ps}
    cikan = sorted(set(b1) - set(b2)); gelen = sorted(set(b2) - set(b1))
    kontrol("ÇIKAN %d parça = v1 zemin kanalı (%s)" % (len(cikan), ", ".join(cikan)),
            set(cikan) == {"kanal_tabani", "kanal_yan_sol", "kanal_yan_sag", "kanal_uc_hat", "kanal_uc_qr", "kanal_ayirici", "kanal_kapagi_koridor", "kanal_kapagi_QR_alti"})
    kontrol("GELEN %d parça = köprü kanalı (%s)" % (len(gelen), ", ".join(gelen)), set(gelen) == {"kopru_tabani", "kopru_yan_sol", "kopru_yan_sag", "kopru_arka_ust", "kopru_arka_sag", "kopru_kapagi"})
    degisen, ayni = [], []
    for a_ in sorted(set(b1) & set(b2)):
        (A, va), (B, vb) = b2[a_], b1[a_]
        d = max(abs(A.xmin - B.xmin), abs(A.xmax - B.xmax), abs(A.ymin - B.ymin), abs(A.ymax - B.ymax), abs(A.zmin - B.zmin), abs(A.zmax - B.zmax), abs(va - vb))
        (degisen if d > 1e-6 else ayni).append(a_)
        if d > 1e-6:
            print("   DEĞİŞTİ %-28s x %8.2f–%8.2f → %8.2f–%8.2f · y %6.1f–%6.1f → %6.1f–%6.1f · z %6.1f–%6.1f → %6.1f–%6.1f · hacim %9.0f → %9.0f"
                  % (a_, B.xmin, B.xmax, A.xmin, A.xmax, B.ymin, B.ymax, A.ymin, A.ymax, B.zmin, B.zmax, A.zmin, A.zmax, vb, va))
    kontrol("DEĞİŞEN %d parça yalnız oluk çıkışına bağlı olanlar (oluk tabanı: eski kanal ağzı kapandı · koridor yanı: çıkış ağzı · uzatma A + kangal + kangal üstünden çıkan B)" % len(degisen),
            set(degisen) == {"oluk_tabani", "oluk_yan_koridor", "robot_kablosu_uzatma_A", "robot_kablosu_uzatma_B", "robot_kablosu_kangal"}, str(degisen))
    kontrol("AYNI KALAN %d parça (zincir · braketler · standart kablo · konnektör · kelepçeler · oluk kapakları / uç duvarları / robot yanı)" % len(ayni), len(ayni) == 13, ", ".join(ayni))
    h1 = R1.kablo_hesabi()
    print("   v1 → v2: uzatma A eksen boyu %.0f → %.0f · kangal %.3f → %.3f sarım (%.2f → %.2f m) · kangal üstü y %.1f → %.1f · konnektör xj %.2f → %.2f"
          % (uzunluk(h1["A"]), uzunluk(h["A"]), h1["N"], h["N"], h1["kangal"] / 1000.0, h["kangal"] / 1000.0, KG["y0"] + h1["N"] * KABLO_D, yk, h1["xj"], h["xj"]))
    if "hizli" not in arg:
        # QR dolabı (qr_cad_v1) ↔ ray ekleri · h3_elk_qr_v1'in DÜŞÜRDÜĞÜ QR parçaları (alt servis kapağı + alt menteşe) hariç: yerlerinde tekmelik + kısa kapak var
        QR.kur()
        qs = [dict(ad=q["ad"], wp=q["wp"], _sh=QR.dunya(q)) for q in QR.PARCALAR if q["ad"] not in EQ.QR_DUSUR]
        cc = QR.capraz([p for p in ps], qs, esik=0.1)
        kontrol("ray ekleri ↔ QR dolabı (qr_cad_v1, %d parça · düşen %s hariç) çakışma = 0 (> 0,1 mm³)" % (len(qs), EQ.QR_DUSUR), not cc, str(cc[:6]))
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETIM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    assert not kal
    sys.stdout.flush(); os._exit(0)
