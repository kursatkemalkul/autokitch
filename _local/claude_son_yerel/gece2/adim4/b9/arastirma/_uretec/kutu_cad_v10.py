# -*- coding: utf-8 -*-
"""v10: Tahrikli köşe / ön dil / kılavuzlu kapak takımları — KİNEMATİK PROTOTİP.
Önceki v9: Motor taban ÜSTÜNDE; orta ayaklar ön/arka hizasında; yan kapak düz, iç dönüşlü.
Kutu açınımı TASLAK; köşe tahrikleri v10 içinde eklendi. Gerçek kartonla otomatik katlama doğrulanmış değildir.
AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v9 (29 Eyl 2026 akşam · yap_kutu_v8.py) — KAPAK MASASI AÇIKÇA İKİ LEVHA (kol yarığı boydan boya; kol β 0…144° masayı x 471–726 arasında keser) · başka değişiklik yok
v7: kutu_cad_v7 (28 Eyl 2026 gece) — ÖN DÜZLEM +79 · TEMİZ KUTU (SPEC_on_duzlem_v63 §2.6, Kemal: "her istasyon kendi
  başına temiz bir kutu, önden tertemiz düz yüzeyler, içeride havada kalan parça olmasın, robotun gireceği yerlerde boşluk"). Z_ON = 79 (fırın ön yüzü),
  arka −830 SABİT → derinlik 909; iç düzen z 0 referanslı AYNEN. Ön: tam boy çerçeve + 6 tava panel (304 fırçalı 1,5 · 20 büküm · +59…+79 · derz 3):
  ALT 2 kanat (içecek yedeği, ≥ 110°) · ORTA sol sabit panel + ROBOT AĞZI (x 85–440 · y 886–1062) + sağ servis kapağı · ÜST 2 kanat (yarım kanat:
  QR yüzü z 670'e çarpmaz) · gizli menteşe + bas-aç, kulp yok. Havada parçalar bağlandı; NEMA 23 motorlar STEP'in tamamıyla. Kinematik v6 ile BİREBİR
  (olcum_v7). Üretici: yap_kutu_v7.py. Önceki: kutu_cad_v6.py
AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v6 (27 Eyl 2026 gece) — ÖN ALT SAC KALKTI (Kemal: "ön taraflara kapak koyma"): içecek yedeğinin önündeki
  sabit ön alt sac (on_alt_sac · x 1,5–828,5 · y 126–917 · 1,5 mm kabuk) silindi → 6 koli önden AÇIK. Sacın üstünde kulp / etiket / sensör / bağlantı yoktu
  (v5'te ona değen parçalar olcum_v6'da ölçülür). Başka hiçbir parça değişmedi: v5 ↔ v6 parça parça karşılaştırılır (olcum_v6). Önde kalan ön köşe
  dikmeleri (L 20 × 20) + dikey kablo kanalı → kolilerin düz çekme yolu ölçülür (icecek_on_olcum). Üretici: yap_kutu_v6.py. Önceki: kutu_cad_v5.py
AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v5 (27 Eyl 2026) — ALÇAK HAT (SPEC_alcak_hat_v57): y 400–568 dilimi çıkarıldı, her şey 168 aşağı
  (üst 1862 · tepsi 936 · alt raf 618–622 · şarjör 240–980 = 462 kutu) + önde İÇECEK YEDEĞİ 6 koli. Üretici: yap_kutu_v5.py. Önceki: kutu_cad_v4.py
AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v4 (27 Eyl 2026): kalıp + kapak plakası ayakları y 790'daki ALT RAFTA biter, rafın altı boş (Kemal). Önceki: kutu_cad_v3.py
AUTOKITCH · E · KUTU KATLAMA MODÜLÜ — ÜRETİM MODELİ v3 (25 Eyl 2026)
v3: ALT TABAN ÇİZGİSİ 123 (Kemal): gövde tabanı 80 → 123, asansör tahriki koruyuculu olarak tabanın altına,
    süpürgelik 60 geride. Çalışma kotları aynı, şarjör 567. Önceki: kutu_cad_v2.py
v2: kayis_y z işaret hatası düzeltildi (asansör + piston kayışlarının düz kolları makinenin önüne düşmüştü) ·
    piston BK12 askı ayakları kayışın iki yanına alındı. Önceki: kutu_cad_v1.py

Kemal (24 Eyl): "standart pizza kutusunu bul, nasıl katlanacağını öğren, katlanması için bizim sistemde mühendislik
çalışmasını yap ve modelle, sonra animasyonu hazırla; tüm parçalar standart, motorlar standart; her şeyi tam göster,
sorunlara çözüm üret. Banttan kutuya düşecek, sonra kapak kapanacak: önce düz, sonra katlanıyor, sonra pizza
içine giriyor, sonra kapanıyor. Robot alırken bir yere çarpıp kapanabilir, bu da bir opsiyon. Bizim ölçülere
uydurmaya çalış, olmazsa ikinci bir model yap, daha geniş."

KUTU (standart): pizza kutusu 32 × 32 × 4,2 cm, E-dalga (AmbalajPazarı · 100'lü paket; Bekar Ambalaj 32×32×4: 100 adet 16 kg)
  Dizilim "Amerikan kapama" = US 4441626 A: taban + 2 yan duvar (uçlarında köşe tırnakları) + ÇİFT ön duvar (dış + iç panel,
  iç panelin 2 kilit dili tabandaki yarıklara girer, köşe tırnakları iki ön panelin ARASINDA kalır) + arka duvar (menteşe)
  + kapak (2 yan flap + ön flap; kapanınca flaplar duvarların İÇİNE girer). Wikipedia: "yan duvarlara bağlı flapların ön
  duvarın içine katlandığı tip standart olmuştur".
  AÇILIM (hesap — üreticinin bıçak çizimi alınınca güncellenecek): 804 × 404 mm.

NEDEN 700 DEĞİL 830: açılım 804 uzun. 700'lük modülün içi ~697 → açılım boyuna sığmaz; derinliğe (830) yatırınca şarjör
  ile katlama yeri aynı izdüşümde kalıyor ve blank şarjörden katlama yerine ÇIKAMIYOR (kalıp ve tepsi yolun üstünde).
  Şarjörü üste almak (kapak dönüşünün üstü, 1560 sonrası) ≈ 250–280 kutu = 1,5 gün → 2 gün kuralı tutmuyor.
  → Modül 830 × 830 (hat +130 mm). Açılım x boyunca yatar; şarjör ARKADA, katlama ÖNDE, blank ÜSTTEN İTİLEREK gelir.

ÇEVRİM: şarjör (asansör yığını YB'de tutar: v5 981,6) → itici blankı 411 mm öne iter (kalıbın üstüne) → piston iner: taban 45,6 mm
  kalıba girer, yan duvarlar kalkar, köşe tırnakları sabit plow'larla içeri döner, ön dış duvar kalkar (köprü aşağıda:
  ön paneller serbest) → pistonun ön dudağı iç ön paneli içeri devirir, 2. vuruş kilit dillerini yarıklara basar →
  köprü kalkar (pizza yolu) → U çerçeve kapak flaplarını 90° kaldırır → kol kapağı dik tutar → [pizza K plakasından
  köprüden kayıp kutuya düşer] → kol kapağı 10° öne yatırır → piston kapağı kapatıp bastırır (flaplar içeri) → robot
  çatalı tepsinin aralıklarından girer, 55 mm kaldırır, dışarı çeker.

KOORDİNAT (modül yereli): x 0..830 soldan sağa (K tarafı 0) · y 0..1862 zeminden (v5 alçak hat) · z 0 eski ön yüz (iç düzen referansı), −830 arka ·
  v7: ÖN DÜZLEM z +79 (Z_ON) — ön panellerin dış yüzü.
  Hatta: x_hat = 4600 + x (E modülü K'nın sağında).
"""
import csv, io, json, math, os, struct, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(os.path.dirname(U))
sys.path.insert(0, U)
from kaset_3d_v3 import Mesh, MM, MALZEME
import topping_cad_v22 as TC

for _k, _v in {"sac": ((0.74, 0.77, 0.80, 1.0), 0.85, 0.32), "aluminyum": ((0.80, 0.82, 0.85, 1.0), 0.9, 0.3),
               "celik": ((0.55, 0.57, 0.60, 1.0), 0.9, 0.35), "motor": ((0.18, 0.19, 0.22, 1.0), 0.5, 0.45),
               "kart": ((0.10, 0.35, 0.22, 1.0), 0.1, 0.6), "siemens": ((0.23, 0.36, 0.40, 1.0), 0.2, 0.5),
               "plastik": ((0.55, 0.57, 0.60, 1.0), 0.0, 0.6), "uhmw": ((0.93, 0.93, 0.90, 1.0), 0.0, 0.7),
               "karton": ((0.74, 0.57, 0.38, 1.0), 0.0, 0.9), "karton_yigin": ((0.66, 0.50, 0.33, 1.0), 0.0, 0.95),
               "hamur": ((0.93, 0.78, 0.52, 1.0), 0.0, 0.85), "sos": ((0.80, 0.30, 0.16, 1.0), 0.0, 0.7),
               "robot": ((0.96, 0.62, 0.10, 1.0), 0.2, 0.45), "kayis": ((0.12, 0.12, 0.13, 1.0), 0.0, 0.8),
               "sensor": ((0.15, 0.30, 0.55, 1.0), 0.2, 0.5), "sari": ((0.93, 0.75, 0.10, 1.0), 0.2, 0.5)}.items():
    MALZEME.setdefault(_k, dict(renk=_v[0], met=_v[1], ruf=_v[2]))
MALZEME.setdefault("referans", dict(renk=(0.62, 0.66, 0.72, 0.28), met=0.0, ruf=0.6, saydam=True))
MALZEME.setdefault("kabuk", dict(renk=(0.78, 0.81, 0.85, 0.14), met=0.3, ruf=0.4, saydam=True))     # dış sac: GLB'de saydam (mekanizma görünsün)
MALZEME.setdefault("pu", dict(renk=(0.93, 0.88, 0.72, 1.0), met=0.0, ruf=0.85))        # v7 (SPEC_on_duzlem_v63): tek başına GLB çıktısında KeyError olmasın
MALZEME.setdefault("conta", dict(renk=(0.90, 0.90, 0.88, 1.0), met=0.0, ruf=0.8))

# ---------------------------------------------------------------- ÖLÇÜLER ----------------------------------------------------------------
W, H, D = 830.0, 1862.0, 830.0                 # v5 ALÇAK HAT: 2030 − 168
DILIM_Y0, DILIM_DY = 400.0, 168.0          # v5: v4'ten çıkarılan yatay dilim y 400–568 (asansör arabası üstü 300 < 400 · şarjör kapısı kulpu altı 640 > 568)
SAC = 1.5
Y_PLINT = 123.0                 # v3 (Kemal 25 Eyl): ALT TABAN ÇİZGİSİ — bütün istasyon gövdeleri yerden 123'te başlar (v2: 80)
Y_TK = Y_PLINT + 5.0           # v3: asansör kasnak düzlemi tabanın ALTINDA (kasnak 108–121, taban 123–126)
TEPSI = 936.0                   # kutu tabanının oturduğu yüz (hat süreç zinciri: kesme plakası 996 − 60) · v5: 1104 − 168
KALIP = 981.5                   # v5 (1149,5 − 168) · kalıp ray üstleri (blank bunun 0,1 üstünde kayar)
YB = 981.6                      # v5 (1149,6 − 168) · düz blankın alt yüzü (şarjör üstü = kalıp üstü: blank aynı kotta kayar)
T = 1.6                         # E-dalga kalınlığı (Wikipedia: E dalga adımı 1,0–1,8)
PLAKA_K = 996.0                 # K kesme plakası üstü (arayüz) · v5: kesme_cad_v4.BANT 996
PENCERE = (PLAKA_K - 18.0, PLAKA_K + 66.0, -372.0, -24.0)   # v5: sol duvardaki pizza penceresi y0 y1 z0 z1 = 978–1062 (v4 1146–1230) · K'nin E_PENCERE'si ile aynı
# KUTU — dış ölçü 320 × 320; ön duvar −x'te (K tarafı, pizza buradan girer), menteşe +x'te
BX0, BX1 = 100.0, 420.0
ZB = -206.0                     # kutu ekseni z. Düz blank ön yüze taşmasın diye (yan duvar 42) hattın ürün ekseni −170'ten 36 mm içeride
BZ0, BZ1 = ZB - 160.0, ZB + 160.0     # −366 … −46
ALT_RAF_Y = (618.0, 622.0)            # v4: alt raf — mekanizmanın en alt parçası flap katlayıcı motoru 629,5 altında (v5: 786–790 − 168)
H_YAN, H_ON, H_IC, H_DIL, H_ARKA = 42.0, 42.0, 40.0, 10.0, 44.0
L_KAP, W_KAP, H_KF = 312.0, 315.0, 36.0
KT_L, KT_H = 38.0, 40.0         # köşe tırnağı (yan duvarın ucunda): boy × yükseklik
X_BL0 = BX0 - H_ON - H_IC - H_DIL                 # 8
X_BL1 = BX1 + H_ARKA + L_KAP + H_KF               # 812
Z_BL0, Z_BL1 = BZ0 - H_YAN, BZ1 + H_YAN            # −408 … −4
ZL0, ZL1 = ZB - W_KAP / 2.0, ZB + W_KAP / 2.0      # kapak −363,5 … −48,5
DIL_Z = ((-300.0, -240.0), (-172.0, -112.0))       # kilit dilleri / tabandaki yarıklar
U_MAX = YB - TEPSI                                  # 45,6 · piston tabanı bu kadar indirir
# ŞARJÖR — açılım z'de 404, x'te 804; yığın ARKADA
BESLE = 411.0                   # itici blankı bu kadar öne iter
ZS0, ZS1 = Z_BL0 - BESLE, Z_BL1 - BESLE            # yığın −819 … −415
Y_PLAT = 240.0                  # tam yığında asansör platformu üstü
Y_YIGIN_UST = YB - T            # v5 980,0 · 2. blankın üstü
SARJOR_ADET = int((Y_YIGIN_UST - Y_PLAT) / T)   # v5: yığın 240–980 = 740 mm → 462 kutu @1,6 (v4 567)
# ÜST GÖVDELER
H_UST = 1310.0                  # piston kafası altı (yukarıda bekler; dik kapağın tepesi 1293,4) · v5: 1478 − 168
KOL_P = (560.0, 912.0)          # kapak kolu mili · v5: 1080 − 168
KOL_R = 166.0
KMER = (BX1, TEPSI + T / 2.0 + H_ARKA)            # kapak menteşesi (420, 980,8)
# ---- v7 · ÖN DÜZLEM +79 (SPEC_on_duzlem_v63 §1 + §2.6) — iç düzen z 0 referanslı ve arka −830 AYNEN kalır; yalnız öne 79 uzama ----
Z_ON = 79.0                     # bütün ön panellerin DIŞ yüzü = fırın gövdesinin ön yüzü (montaj sözleşmesi: KC.Z_ON = FT.ZS) · derinlik D + Z_ON = 909
TAVA, TAVA_T = 20.0, 1.5        # kuru istasyon kapağı / sabit panel: 304 fırçalı 1,5 sac, kenarlar 20 arkaya bükülü (tava panel)
Z_PANEL = Z_ON - TAVA           # +59 · tava panellerin arka kenarı = sol / sağ / üst sacın ön kenarı
Z_TABAN_ON = Z_ON - 21.5        # +57,5 · taban sacının ön kenarı (SPEC)
Z_CERCEVE = (Z_PANEL - 30.0, Z_PANEL)       # +29 … +59 · ön çerçeve (dikme + kayıt): ön yüzü kapak arkasına yaslanır (kapak dayaması)
Z_PLINT = (Z_ON - 61.5, Z_ON - 60.0)        # +17,5 … +19 · plint ön düzlemin 60 gerisinde (hat boyunca tek çizgi)
PLINT_GERI = 30.0               # hat sonunda (x 830) plint dönüşü 30 içeride (B'nin x 30 / 3970 dönüşleriyle aynı mantık)
DERZ = 3.0
Y_ALT = (Y_PLINT + DERZ, 883.0)             # ALT kanatlar (içecek yedeği) y 126–883
Y_ORTA = (886.0, 1305.0)                    # ORTA bant: sol sabit panel + ROBOT AĞZI + sağ servis kapağı
Y_UST = (1308.0, H - DERZ)                  # ÜST kanatlar y 1308–1859
X_ORTA_DERZ = (414.5, 417.5)                # iki kanat arası derz (hat x 5014,5–5017,5)
AGIZ = dict(x=(85.0, 440.0), y=(Y_ORTA[0], 1062.0))   # ROBOT AĞZI (hat x 4685–5040): çatal + kutu yolu t 13,9–17,3 (SPEC)
LAM = 1.0                       # sol dikmenin koli bandındaki lamı x 1,5–2,5 → sol sütun kolisi (x 3–403) ile 0,5 mm pay
Y_DIKME_SOL = 520.0             # sol dikmenin kutu profili bunun üstünde (koli üstü 499 + 21)
QR_Z = 670.0                    # QR teslim dolabının robot yüzü (qr_cad_v1.py:27) — kanatlar açılınca buraya çarpmamalı
AYAK_XZ = ((60.0, -110.0), (770.0, -110.0), (60.0, -770.0), (770.0, -770.0), (415.0, -110.0), (415.0, -770.0))   # v7: +2 orta ayak (taban açıklığı 827 → 413)
KAPI_ADLARI = ("onyuz_alt_kanat_sol", "onyuz_alt_kanat_sag", "onyuz_orta_servis_kapagi", "onyuz_ust_kanat_sol", "onyuz_ust_kanat_sag")
# ---- v7b (bağımsız denetim 28 Eyl) ----
MENTESE_OFSET = TAVA            # SIFIR ÇIKINTILI (zero protrusion) gizli menteşe: sanal dönme ekseni kapağın menteşe kenarının TAVA (20) DIŞINDA, ön düzlemde →
                                #   90°'de kapağın iç yüzü yan sacın iç yüzüne (sol x 1,5) gelir; koli yolu (x 3–805) kapakla kesişmez. Aday Blum CLIP top 155° zero protrusion
KAPI_MAX_ACI = 155.0            # menteşe açılış sınırı (Blum 71B7550 ailesi: 155°)
KOLI_ACI = 90.0                 # ALT kanat bu açıdan itibaren koli çekme yolu (ön düzlemin önünde koli boyu 267 dahil) SERBEST — işletme açısı
KUTU_KANAT = ("onyuz_alt_kanat_sol", "onyuz_alt_kanat_sag")   # ALT kanatlar KUTU KESİT: tava + 1,0 iç kapatma sacı (burulma: menteşeler koli bandının üstünde kalmak zorunda)
IC_SAC = 1.0
KAPLIN = dict(d=25.0, L=26.0, gobek=11.0, pay_ust=2.0)          # aday NBK MDS-25C-6.35-10 (tek diskli sıkma) · Ø25 · boy 26 + göbek 11 VARSAYIM (föy açılamadı) · üstte yatağa 2 pay
MIL_UCU = 31.557 - 10.973       # STP-MTR-23079 STEP: mil ucu flanş yüzünden 20,584 (ölçüldü)
MOTOR_INDIR = 8.5               # köprü + flap katlayıcı motorları 8,5 aşağı → mil kaplinin motor göbeğine 10,1 dalar (≤ göbek 11), pilot kaplinden 9 uzak
ESIK_DIS = ((X_BL0, 188.0), (222.0, 383.0), (417.0, 578.0), (612.0, X_BL1))   # şarjör eşiği tarağının 4 dişi (X_TIRNAK ± 2 yarıkları arası)
ESIK_AYAK = 12.5                # diş ayağı: eşiğin önüne (z −411,5 → −399) bükülü 3 mm · tabana 2 × M5 (taban delikleri z −397'den başlar)
ESIK_KOS_Y = (880.0, 930.0)     # eşik köşebentleri (sol + sağ yan saca): üst köşebentlerin (940) altında, blank yolunun (981,6) altında
FOTOSEL_BRAKET_BOM = ("Fotosel braketi Al · L 3 mm", 1, "Omron E3Z 2 × M3 ile · yan saca 27 × 20 kol, 2 × M4", "v7b · üretim (v7 ilk: 3 mm kenarla yan saca — denetim bulgusu 5)")
SENSOR_BRAKET_BOM = ("Sensör braketi · delikli sac (Ø8, M8 endüktif) + L / Z kol", 1, "sensör deliğe 2 × M8 somunla (iki ucu açık) · taşıyıcıya ≥ 10 mm bindirme, 2 × M4",
                     "v7b · üretim (v7 ilk: düz lam / teğet temas — denetim bulgusu 5)")

PARCALAR = []


def ekle(ad, wp, mal, grup="SABIT", bom=None):
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, grup=grup, bom=bom))


kut = lambda x0, x1, y0, y1, z0, z1: cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
def boru_y(x, z, r, ri, y0, y1): return sily(x, z, r, y0, y1).cut(sily(x, z, ri, y0 - 1, y1 + 1))


def _trsf(M):
    """3x4 satır matrisi -> gp_Trsf (cq.Matrix listeden kurulunca 'non-orthogonal' hatası veriyor)"""
    from OCP.gp import gp_Trsf
    t = gp_Trsf()
    t.SetValues(M[0][0], M[0][1], M[0][2], M[0][3], M[1][0], M[1][1], M[1][2], M[1][3], M[2][0], M[2][1], M[2][2], M[2][3])
    return t


def tasi(sh, M):
    return sh.moved(cq.Location(_trsf(M)))


def eksen_matrisi(ex, ey, ez, P):
    return [[ex[0], ey[0], ez[0], P[0]], [ex[1], ey[1], ez[1], P[1]], [ex[2], ey[2], ez[2], P[2]]]


def capraz(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def yerles(sh, boy, normal, P):
    """kanonik katıyı (boy = x, normal = y, enine = z; kök noktası 0) hedef eksenlere oturtur"""
    return tasi(sh, eksen_matrisi(boy, normal, capraz(boy, normal), P))


# ---------------------------------------------------------------- STANDART PARÇALAR ----------------------------------------------------------------
_RAY = {}


def hgr15(ad, L, P, boy, normal, grup="SABIT", bom=None):
    """HIWIN HGR15 ray — TraceParts STEP'inin kesiti (TC.hiwin_ray) · kök = ray tabanı ortası, boy yönünde L"""
    if L not in _RAY:
        w, _n = TC.hiwin_ray(0.0, L, 0.0)
        _RAY[L] = w.val().translate(cq.Vector(0.0, -20.5, 0.0))
    ekle(ad, cq.Workplane(obj=yerles(_RAY[L], boy, normal, P)), "celik", grup,
         bom or ("Lineer ray HIWIN HGR15R", 1, "15 × 15 · boy %.0f" % L, "hiwin.com · Linear_Guideway-E s.41"))


def hgh15(ad, P, boy, normal, grup="SABIT"):
    """HIWIN HGH15CA araba — gerçek STEP · P = ray tabanında arabanın ortası"""
    sh = TC.hiwin()["araba"].translate(cq.Vector(0.0, -20.5, 0.0))
    ekle(ad, cq.Workplane(obj=yerles(sh, boy, normal, P)), "celik", grup,
         ("Lineer araba HIWIN HGH15CA", 1, "flanşsız · 34 × 61,4 · H 28", "TraceParts 90-03042020-037166"))


Z_FLANS_STEP = 10.973           # v7: STP-MTR-23079 STEP'inde flanşın ön yüzü (ölçüldü: düzlem yüz z 10,973 · pilot Ø38,1 üstü 12,497 · mil Ø6,35 ucu 31,557)
_MOT_TAM = {}


def _nema23_tam():
    """v7 · STEP'in TAMAMI. TC.nema23() gövdeyi STEP z 0'dan kesiyor → gerçek motorun ön 11 mm'si (flanş) + pilot + mil modelde yoktu
    (gövde 64,5 görünüyordu; katalog 23079 ≈ 79). Burada flanş ön yüzü z 0: gövde −z (75,5), pilot Ø38,1 × 1,5 + mil Ø6,35 +z (ucu +20,6).
    Kablo telleri hariç (TC ile aynı ayrım: ymin < −80 olan katılar)."""
    if "g" not in _MOT_TAM:
        w = cq.importers.importStep(TC.MOTOR_STEP)
        gov = [x for x in w.val().Solids() if x.BoundingBox().ymin >= -80.0]
        g = gov[0]
        for x in gov[1:]:
            g = g.fuse(x)
        _MOT_TAM["g"] = g.translate(cq.Vector(0.0, 0.0, -Z_FLANS_STEP))
    return _MOT_TAM["g"]


def nema23(ad, P, eksen, yukari, grup="SABIT"):
    """AutomationDirect SureStep STP-MTR-23079 · gerçek STEP (v7: tam boy) · P = flanş ön yüzü (mil yüzü), gövde −eksen yönünde, mil +eksen"""
    # kanonik: mil +z, gövde −z
    ex = capraz(yukari, eksen)
    ekle(ad, cq.Workplane(obj=tasi(_nema23_tam(), eksen_matrisi(ex, yukari, eksen, P))), "motor", grup,
         ("Step motor AutomationDirect SureStep STP-MTR-23079", 1, "NEMA 23 · 1,95 N·m (276 oz-in) · 2,8 A · gövde 75,5 + pilot Ø38,1 + mil Ø6,35 × 20,6 (STEP ölçüsü, v7)",
          "automationdirect.com STP-MTR-23079 · TraceParts STEP"))


def pgcn23(ad, P, eksen, yukari, grup="SABIT"):
    """SureGear PGCN23-1025 planet redüktör 10:1 · gerçek STEP · P = çıkış yüzü, gövde −eksen yönünde (79)"""
    r = TC.suregear()
    ex = capraz(yukari, eksen)
    ekle(ad, cq.Workplane(obj=tasi(r["tum"], eksen_matrisi(ex, yukari, eksen, P))), "motor", grup,
         ("Planet redüktör SureGear PGCN23-1025", 1, "10:1 · 5 N·m · NEMA 23", "adcpn.com/pn/PGCN23-1025 · TraceParts STEP"))


def sfu16(ad, x, z, y0, y1, hatve, grup_somun, y_somun, grup="SABIT", somun_yon=1):
    """bilyalı vida SFU16xx: mil Ø16 + flanşlı somun (flanş Ø48 × 10, gövde Ø28, boy 57) · dikey"""
    ekle(ad + "_mil", sily(x, z, 8.0, y0, y1), "celik", grup,
         ("Bilyalı vida TBI/HIWIN SFU16%02d" % hatve, 1, "Ø16 · hatve %d · boy %.0f · uçları BK12/BF12 işli" % (hatve, y1 - y0), "SFU16%02d katalog (fluxelectronix / TBI)" % hatve))
    s = sily(x, z, 14.0, y_somun, y_somun + 47.0).union(sily(x, z, 24.0, y_somun + 47.0, y_somun + 57.0)).cut(sily(x, z, 8.2, y_somun - 1, y_somun + 58))
    ekle(ad + "_somun", s, "celik", grup_somun, ("Bilyalı somun SFU16%02d-4" % hatve, 1, "flanş Ø48 · gövde Ø28 · boy 57", "katalog ölçüsü"))


def bk12(ad, x, z, y0, taban_yon, grup="SABIT", bf=False):
    """BK12 / BF12 rulman yuvası: 60 × 43 × (32,5 | 20), mil merkezi tabandan 25 · y0 = alt yüz, dikey vida için yatay oturur"""
    h = 20.0 if bf else 32.5
    # yatay (dikey mil): gövde x'te 60, z'de 43, y'de h
    b = kut(x - 30.0, x + 30.0, y0, y0 + h, z - 18.0, z + 25.0).cut(sily(x, z, 8.0 if not bf else 6.0, y0 - 1, y0 + h + 1))
    ekle(ad, b, "celik", grup, (("Destek BF12 (serbest)" if bf else "Destek BK12 (sabit)"), 1, "60 × 43 × %.1f · merkez yüksekliği 25" % h, "MISUMI BK/BF · fonlinearguide.com"))


def kasnak(ad, x, y, z, dis, eksen="y", genis=11.0, grup="SABIT"):
    """GT3 kasnak (flanşlı) · PD = dis × 3 / π"""
    pd = dis * 3.0 / math.pi
    r = pd / 2.0 - 0.38
    if eksen == "y":
        k = sily(x, z, r, y, y + genis).union(sily(x, z, r + 2.5, y - 1.0, y)).union(sily(x, z, r + 2.5, y + genis, y + genis + 1.0))
    elif eksen == "x":
        k = silx(y, z, r, x, x + genis).union(silx(y, z, r + 2.5, x - 1.0, x)).union(silx(y, z, r + 2.5, x + genis, x + genis + 1.0))
    else:
        k = silz(x, y, r, z, z + genis).union(silz(x, y, r + 2.5, z - 1.0, z)).union(silz(x, y, r + 2.5, z + genis, z + genis + 1.0))
    ekle(ad, k, "aluminyum", grup, ("Kasnak GT3 %d diş" % dis, 1, "PD %.1f · 9 mm kayış" % pd, "gates.com GT3 · katalog"))
    return pd


def kayis_y(ad, x1, z1, x2, z2, y, pd1, pd2, genis=9.0, grup="SABIT"):
    """iki dikey eksenli kasnak arasında GT3 kayış (y düzleminde) — sırt 1,2 · şerit gövde"""
    t = 1.2
    dx, dz = x2 - x1, z2 - z1; L = math.hypot(dx, dz); ux, uz = dx / L, dz / L; nx, nz = -uz, ux
    r1, r2 = pd1 / 2.0, pd2 / 2.0
    parca = None
    for s in (1.0, -1.0):
        a = (x1 + s * nx * r1, z1 + s * nz * r1); b = (x2 + s * nx * r2, z2 + s * nz * r2)
        q = [(a[0] + s * nx * 0.0, a[1] + s * nz * 0.0), (b[0], b[1]), (b[0] + s * nx * t, b[1] + s * nz * t), (a[0] + s * nx * t, a[1] + s * nz * t)]
        pl = cq.Workplane("XZ", origin=(0, y, 0)).polyline([(p[0], p[1]) for p in q]).close().extrude(-genis)   # v2: XZ'de yerel v = +z (v1'de −z idi)
        parca = pl if parca is None else parca.union(pl)
    for (cx, cz, r) in ((x1, z1, r1), (x2, z2, r2)):
        parca = parca.union(sily(cx, cz, r + t, y, y + genis).cut(sily(cx, cz, r, y - 1, y + genis + 1)))
    ekle(ad, parca, "kayis", grup, ("Kayış GT3 9 mm", 1, "kapalı çevrim", "gates.com"))


def kayis_z(ad, y1, z1, y2, z2, x, pd1, pd2, genis=9.0, grup="SABIT", mal="kayis"):
    """x eksenli iki kasnak arasında kayış (x düzleminde, yz'de koşar)"""
    t = 1.2
    parca = None
    dy, dz = y2 - y1, z2 - z1; L = math.hypot(dy, dz); uy, uz = dy / L, dz / L; ny, nz = -uz, uy
    r1, r2 = pd1 / 2.0, pd2 / 2.0
    for s in (1.0, -1.0):
        a = (y1 + s * ny * r1, z1 + s * nz * r1); b = (y2 + s * ny * r2, z2 + s * nz * r2)
        q = [a, b, (b[0] + s * ny * t, b[1] + s * nz * t), (a[0] + s * ny * t, a[1] + s * nz * t)]
        pl = cq.Workplane("YZ", origin=(x, 0, 0)).polyline(q).close().extrude(genis)
        parca = pl if parca is None else parca.union(pl)
    for (cy, cz, r) in ((y1, z1, r1), (y2, z2, r2)):
        parca = parca.union(silx(cy, cz, r + t, x, x + genis).cut(silx(cy, cz, r, x - 1, x + genis + 1)))
    ekle(ad, parca, mal, grup, ("Kayış GT3 9 mm", 1, "kapalı çevrim", "gates.com"))


def kaplin(ad, x, y, z, eksen="y", grup="SABIT"):
    """v7b · tek diskli sıkma kaplin Ø25 × L (aday NBK MDS-25C-6.35-10) · y = ALT (motor tarafı) yüzü, dikey eksen.
    Motor göbeği Ø6,4 delik (mil Ø6,35 oturur, katı bindirmesi YOK) · vida göbeği Ø10 delik (BK12 uç muylusu) · ortada disk bölgesi dolu.
    v7 ilk hali: dolu Ø25 × 30 motor flanşından başlıyordu → Ø38,1 pilota 1,5 biniyordu ve istisna listesi bunu gizliyordu (denetim bulgusu 2)."""
    assert eksen == "y", "v7b: kaplin yalnız dikey eksen"
    L_, gb = KAPLIN["L"], KAPLIN["gobek"]
    k = sily(x, z, KAPLIN["d"] / 2.0, y, y + L_).cut(sily(x, z, 3.2, y - 1.0, y + gb)).cut(sily(x, z, 5.0, y + L_ - gb, y + L_ + 1.0))
    ekle(ad, k, "aluminyum", grup, ("Kaplin tek diskli sıkma Ø25 × %.0f (aday NBK MDS-25C-6.35-10)" % L_, 1,
                                    "delik 6,35 (motor) × 10 (vida muylusu) · motor mili göbeğe ≈ 10 dalar (göbek %.0f, olcum_v7 ölçer)" % gb,
                                    "nbk1560.com MDS-25C (parça no mevcut) · boy / göbek VARSAYIM (föy açılamadı)"))


def e3z(ad, x, y, z, grup="SABIT"):
    """Omron E3Z-D62 dağınık yansımalı fotosel · 10,8 × 31 × 20 (x · y · z) · x,y,z = gövdenin alt-sol-arka köşesi"""
    ekle(ad, kut(x, x + 10.8, y, y + 31.0, z, z + 20.0), "sensor", grup,
         ("Fotosel Omron E3Z-D62", 1, "dağınık yansımalı · 1 m · PNP", "omron.com E3Z · katalog ölçüsü"))


def e2e(ad, x, y, z, eksen, grup="SABIT"):
    """Omron E2E-X2D1-N endüktif M8 · Ø8 × 30"""
    s = sily(x, z, 4.0, y, y + 30.0) if eksen == "y" else (silz(x, y, 4.0, z, z + 30.0) if eksen == "z" else silx(y, z, 4.0, x, x + 30.0))
    ekle(ad, s, "sensor", grup, ("Endüktif sensör Omron E2E-X2D1-N", 1, "M8 · 2 mm · DC 2 telli", "omron.com E2E · katalog ölçüsü"))


# ---------------------------------------------------------------- GÖVDE ----------------------------------------------------------------
def govde():
    # ayaklar + taban · v7: +2 orta ayak x 415 (z −40 / −300): 3 mm taban 827 açıklıkta içecek yedeği altında ~33 mm sehim → ~2 mm (olcum_v7 hesabı)
    for i, (ax, az) in enumerate(AYAK_XZ):   # v3: ön ayaklar süpürgeliğin arkasında
        ekle("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik",
             bom=("Ayarlı ayak Elesa+Ganter LV.A-SST · M12", len(AYAK_XZ), "paslanmaz · taban Ø40 · v7: 4 köşe + 2 orta", "elesa-ganter.com LV.A-SST") if i == 0 else None)
    taban = kut(SAC, W - SAC, Y_PLINT, Y_PLINT + 3.0, -D + SAC, Z_TABAN_ON)  # v9: no drive penetrations
    ekle("taban_sac_3", taban, "sac")
    # kabuk · v7: sol / sağ / üst sac ön kenarı Z_PANEL (+59 = tava kapakların arkası) · arka −830 SABİT
    ekle("arka_sac", kut(0, W, Y_PLINT, H, -D, -D + SAC), "kabuk")
    ekle("ust_sac", kut(0, W, H - SAC, H, -D + SAC, Z_PANEL), "kabuk")
    sol = kut(0, SAC, Y_PLINT, H - SAC, -D + SAC, Z_PANEL).cut(kut(-1, SAC + 1, PENCERE[0], PENCERE[1], PENCERE[2], PENCERE[3]))   # pizza penceresi (v5 978–1062)
    ekle("sol_sac_pizza_penceresi", sol, "kabuk")
    sag = kut(W - SAC, W, Y_PLINT, H - SAC, -D + SAC, Z_PANEL).cut(kut(W - SAC - 1, W + 1, 231.0, 989.0, -823.0, -411.0))  # şarjör yan kapısı (v5 üstü 1156 − 168)
    ekle("sag_sac", sag, "kabuk")
    door = kut(W - SAC, W, 234.0, 986.0, -820.0, -414.0)
    # Continuous upper/lower returns stiffen the sheet without an exterior batten.
    for ya, yb in ((234.0, 235.5), (984.5, 986.0)):
        door = door.union(kut(818.0, W - SAC, ya, yb, -820.0, -414.0))
    ekle("sarjor_yan_kapisi", door, "sac")
    # v7: yan kapı MENTEŞESİZ + dış kulplu idi (v6: havada; kulp 22 mm dışarıda) → arka kenarda 2 gizli menteşe + ön kenarda bas-aç (ikisi de İÇTE), kulp KALKTI.
    #     Sağ kılavuz (UHMW + taşıyıcı) KAPIDA kalır: kapı açılınca yığının sağ yanı tamamen açılır (yan yükleme) — KARAR (varsayım)
    for i, yc in enumerate((300.0, 900.0)):
        ekle("sarjor_yan_kapisi_mentese_%d" % i, kut(W - SAC - 8.5, W - SAC, yc - 25.0, yc + 25.0, -826.0, -814.0), "celik",
             bom=("Gizli menteşe · yan kapı (içte, 1,5 sac kapı)", 1, "arka kenar · kapı ↔ yan sac kesim kenarı", "VARSAYIM ölçü 8,5 × 50 × 12 · üretici / parça no BULUNAMADI"))
    ekle("sarjor_yan_kapisi_basac", kut(W - SAC - 8.5, W - SAC, 590.0, 630.0, -418.0, -406.0), "plastik",
         bom=("Bas-aç mandalı (push-to-open, mıknatıslı)", 1, "yan kapı ön kenarı · içte", "VARSAYIM ölçü · Southco push-to-open ailesi, parça no BULUNAMADI"))
    # ağız üst kirişi (ön kose plow'larını tasir) — kapak dik dururken onun ONUNDE (z > -46,5)
    ekle("agiz_ust_kirisi", kut(SAC, W - SAC, 1162.0, 1177.0, -40.0, -20.0), "celik")
    # v7: on_ust_kapak + kulbu + ön köşe dikmeleri (L 20, y 126–917) KALKTI → onyuz(): tam boy ön çerçeve + tava paneller (+59…+79)


# ---------------------------------------------------------------- ÖN YÜZ (v7 · SPEC_on_duzlem_v63 §2.6) ----------------------------------------------------------------
def kutu_profil(x0, x1, y0, y1, z0, z1, et=2.0, eksen="y"):
    """v7 · dikdörtgen kutu profil (304, et kalınlığı), boyu 'eksen' yönünde (y ya da x), uçları açık"""
    if eksen == "y":
        return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + et, x1 - et, y0 - 1.0, y1 + 1.0, z0 + et, z1 - et))
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, y0 + et, y1 - et, z0 + et, z1 - et))


def tava(x0, x1, y0, y1, kes=None):
    """v7 · TAVA PANEL (SPEC §1 kuru istasyon kapağı): 304 fırçalı 1,5 sac, dört kenar 20 arkaya bükülü → z Z_PANEL…Z_ON.
    kes = kenardan açılan dikdörtgen kesik (x0, x1, y0, y1): kesik kenarları da 20 arkaya bükülü (çapaksız)"""
    dis = kut(x0, x1, y0, y1, Z_PANEL, Z_ON)
    ic = kut(x0 + TAVA_T, x1 - TAVA_T, y0 + TAVA_T, y1 - TAVA_T, Z_PANEL - 1.0, Z_ON - TAVA_T)
    if kes:
        a, b, c, d_ = kes
        dis = dis.cut(kut(a, b, c, d_, Z_PANEL - 1.0, Z_ON + 1.0))
        ic = ic.cut(kut(a - TAVA_T, b + TAVA_T, c - TAVA_T, d_ + TAVA_T, Z_PANEL - 2.0, Z_ON + 2.0))
    return dis.cut(ic)


ON_PANEL = (   # ad, x0, x1, y0, y1, menteşe tarafı ("sol" / "sag" · None = sabit panel), kenardan kesik — hepsi tava 20, z +59…+79, derz 3
    ("onyuz_alt_kanat_sol", SAC, X_ORTA_DERZ[0], Y_ALT[0], Y_ALT[1], "sol", None),
    ("onyuz_alt_kanat_sag", X_ORTA_DERZ[1], W, Y_ALT[0], Y_ALT[1], "sag", None),
    ("onyuz_orta_sabit_panel", SAC, AGIZ["x"][1], Y_ORTA[0], Y_ORTA[1], None, (AGIZ["x"][0], AGIZ["x"][1] + 1.0, Y_ORTA[0] - 1.0, AGIZ["y"][1])),
    ("onyuz_orta_servis_kapagi", AGIZ["x"][1] + DERZ, W, Y_ORTA[0], Y_ORTA[1], "sag", None),
    ("onyuz_ust_kanat_sol", SAC, X_ORTA_DERZ[0], Y_UST[0], Y_UST[1], "sol", None),
    ("onyuz_ust_kanat_sag", X_ORTA_DERZ[1], W, Y_UST[0], Y_UST[1], "sag", None),
)
# menteşe yükseklikleri: ALT kanatlarda koli bandının (y 130–499) ÜSTÜNDE — menteşe gövdesi koli yoluna girmez ·
# v7b: ALT kanatlar kutu kesit (≈ 6,7 kg) → 3 menteşe (Blum kılavuzu: ≤ 900 mm kapakta 15 lb / 6,8 kg üstü 3 menteşe — okuma VARSAYIM)
MENTESE_Y = {"onyuz_alt_kanat_sol": (560.0, 680.0, 800.0), "onyuz_alt_kanat_sag": (560.0, 680.0, 800.0), "onyuz_orta_servis_kapagi": (950.0, 1230.0),
             "onyuz_ust_kanat_sol": (1390.0, 1780.0), "onyuz_ust_kanat_sag": (1390.0, 1780.0)}
BASAC_YER = (("onyuz_alt_kanat_sol", X_ORTA_DERZ[0] - 20.0, X_ORTA_DERZ[0], Y_ALT[1] - 60.0, Y_ALT[1] - 30.0),      # orta kayıtın altında
             ("onyuz_alt_kanat_sag", X_ORTA_DERZ[1], X_ORTA_DERZ[1] + 20.0, Y_ALT[1] - 60.0, Y_ALT[1] - 30.0),
             ("onyuz_orta_servis_kapagi", AGIZ["x"][1] + DERZ, AGIZ["x"][1] + DERZ + 20.0, Y_ORTA[1] - 60.0, Y_ORTA[1] - 30.0),   # üst kayıtın altında
             ("onyuz_ust_kanat_sol", X_ORTA_DERZ[0] - 20.0, X_ORTA_DERZ[0], Y_ORTA[1], Y_ORTA[1] + 30.0),                          # üst kayıtın üstünde
             ("onyuz_ust_kanat_sag", X_ORTA_DERZ[1], X_ORTA_DERZ[1] + 20.0, Y_ORTA[1], Y_ORTA[1] + 30.0))
MENTESE_KAPI = {}               # menteşe parçası → kapak (kapak açılış denetimi kendi menteşesini saymaz)


def onyuz():
    """v7 · ÖN YÜZ (SPEC_on_duzlem_v63 §2.6): ön çerçeve (2 tam boy dikme + 2 kayıt, z +29…+59) · 6 tava panel (z +59…+79, derz 3) ·
    10 gizli menteşe + 5 bas-aç (içte) · plint (+17,5…+19). Önden yalnız düz yüzey + derz + ROBOT AĞZI görünür (kulp / vida / menteşe yok)."""
    zc0, zc1 = Z_CERCEVE
    # ön çerçeve — sol dikme: koli bandında (y 126–520) sol yan saca kaynaklı 1,0 lam (x 1,5–2,5 → sol sütun kolisinin yolu x ≥ 3 serbest),
    # üstünde 20 × 30 × 2 kutu profil · sağ dikme tam boy kutu profil x 808,5–828,5 (sağ sütun kolisi x ≤ 805, kablo kanalı x 806–826 z −50…−25)
    d_ = kut(SAC, SAC + LAM, Y_ALT[0], Y_DIKME_SOL, zc0, zc1).union(kutu_profil(SAC, SAC + 20.0, Y_DIKME_SOL, H - SAC, zc0, zc1))
    ekle("onyuz_dikme_sol", d_, "sac", bom=("Ön dikme sol · 304 kutu profil 20 × 30 × 2 + 1,0 lam", 1,
         "profil y %.0f–%.1f · lam y %.0f–%.0f (koli bandı: yol serbest) · yan saca kaynaklı" % (Y_DIKME_SOL, H - SAC, Y_ALT[0], Y_DIKME_SOL), "v7 · üretim"))
    ekle("onyuz_dikme_sag", kutu_profil(W - SAC - 20.0, W - SAC, Y_ALT[0], H - SAC, zc0, zc1), "sac",
         bom=("Ön dikme sağ · 304 kutu profil 20 × 30 × 2", 1, "y %.0f–%.1f · yan saca kaynaklı" % (Y_ALT[0], H - SAC), "v7 · üretim"))
    for ad_, y1 in (("onyuz_kayit_orta", Y_ALT[1]), ("onyuz_kayit_ust", Y_ORTA[1])):
        ekle(ad_, kutu_profil(SAC + 20.0, W - SAC - 20.0, y1 - 30.0, y1, zc0, zc1, eksen="x"), "sac",
             bom=("Ön kayıt · 304 kutu profil 30 × 30 × 2", 1, "boy %.0f · derz arkasında (üst yüzü y %.0f) · dikmelere kaynaklı" % (W - 2 * SAC - 40.0, y1), "v7 · üretim"))
    # tava paneller · v7b: ALT kanatlar KUTU KESİT — tavanın içine 1,0 kapatma sacı (z +59…+60, bükümlere kaynaklı, menteşe yerlerinde pencere):
    #   açık tava (J ≈ 505 mm⁴) burulmada yumuşaktı; menteşeler koli bandının üstünde kalmak zorunda olduğundan alt serbest köşe 404 mm konsol (denetim bulgusu 4)
    xm = {"sol": SAC + 20.0, "sag": W - SAC - 40.0}           # menteşe gövdesinin x başlangıcı (dikme iç yüzü)
    for ad_, x0, x1, y0, y1, taraf, kes in ON_PANEL:
        sh_ = tava(x0, x1, y0, y1, kes)
        if ad_ in KUTU_KANAT:
            ic_ = kut(x0 + TAVA_T, x1 - TAVA_T, y0 + TAVA_T, y1 - TAVA_T, Z_PANEL, Z_PANEL + IC_SAC)
            for yc in MENTESE_Y[ad_]:
                ic_ = ic_.cut(kut(xm[taraf] - 1.0, xm[taraf] + 21.0, yc - 31.0, yc + 31.0, Z_PANEL - 1.0, Z_PANEL + IC_SAC + 1.0))
            sh_ = sh_.union(ic_)
        ekle(ad_, sh_, "sac",
             bom=("Tava %s 304 fırçalı 1,5 · 20 büküm%s" % ("kapak" if taraf else "sabit panel", " + 1,0 iç kapatma sacı (kutu kesit)" if ad_ in KUTU_KANAT else ""), 1,
                  "%.1f × %.1f · %s" % (x1 - x0, y1 - y0, ("gizli menteşe %s (sıfır çıkıntılı 155°) · bas-aç · kulpsuz" % taraf) if taraf else
                                        "ROBOT AĞZI kesikli (x %.0f–%.0f · y %.0f–%.0f, kenarları bükülü) · arkadan kaynaklı M5 saplamalı" % (AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1])),
                  "v7 · SPEC_on_duzlem_v63"))
    # gizli menteşeler: dikmenin iç yüzü (x 21,5 | 808,5) ↔ kapağın iç ön yüzü (z +77,5) · v7b: SIFIR ÇIKINTILI — sanal eksen kapak kenarının 20 DIŞINDA (kapi_matrisi)
    MENTESE_KAPI.clear()
    n = 0
    for ad_, x0, x1, y0, y1, taraf, kes in ON_PANEL:
        if not taraf:
            continue
        xa = xm[taraf]
        for yc in MENTESE_Y[ad_]:
            m_ = "onyuz_mentese_%d" % n
            ekle(m_, kut(xa, xa + 20.0, yc - 30.0, yc + 30.0, Z_PANEL - 10.0, Z_ON - TAVA_T), "celik",
                 bom=("Gizli menteşe · sıfır çıkıntılı 155°, tam bindirme (aday Blum CLIP top 71B7550 ailesi; bas-aç için yaysız sürüm)", 1,
                      "90°'de kapak iç yüzü yan sac iç yüzünde → koli / servis yolu açık · kılavuz: ≤ 900 mm kapakta 6,8 kg'a kadar 2, üstü 3 menteşe (okuma VARSAYIM)",
                      "blum.com 71B7550 (155° zero protrusion, kapak ≤ 24 mm) · sac kapakta Ø35 kap yuvası kaynaklı · yaysız parça no + ölçü VARSAYIM 20 × 60 × 28,5"))
            MENTESE_KAPI[m_] = ad_
            n += 1
    # v7b · ALT dayama dudağı: taban ön kenarında 304 lama (y 126–129 · z +45…+59) — ALT kanatların alt bükümü + iç sacı buna yaslanır (içe dayama);
    #   koli tabanı 130 (altlık üstü) → koli yolunun 1 mm altında, yolu kapatmaz · lam (x 2,5) ile sağ dikme (x 808,5) arasında
    ekle("onyuz_alt_dayama_dudagi", kut(SAC + LAM, W - SAC - 20.0, Y_ALT[0], Y_ALT[0] + 3.0, Z_PANEL - 14.0, Z_PANEL), "sac",
         bom=("ALT kanat dayama dudağı 304 lama 3 × 14", 1, "x %.1f–%.1f · tabana kaynaklı · ALT kanatların alt kenarı yaslanır (koli yolunun 1 mm altında)" % (SAC + LAM, W - SAC - 20.0), "v7b · üretim"))
    for i, (ad_, x0, x1, y0, y1) in enumerate(BASAC_YER):
        ekle("onyuz_basac_%d" % i, kut(x0, x1, y0, y1, Z_PANEL - 20.0, Z_PANEL - 2.0), "plastik",
             bom=("Bas-aç mandalı (push-to-open, mıknatıslı)", 1, "%s serbest kenarı · kayıta vidalı · pim kapak kenar bükümüne basar (2 mm)" % ad_,
                  "VARSAYIM ölçü 20 × 30 × 18 · Southco push-to-open ailesi, parça no BULUNAMADI"))
    # plint: x 0 (K ile birleşir) … 800 + hat sonu dönüşü (x 798,5–800, 30 içeride) · klipsli, sökülür (asansör tahrikine servis)
    pl = kut(0.0, W - PLINT_GERI, 0.0, Y_PLINT, Z_PLINT[0], Z_PLINT[1]).union(kut(W - PLINT_GERI - SAC, W - PLINT_GERI, 0.0, Y_PLINT, -D + PLINT_GERI, Z_PLINT[0]))
    ekle("onyuz_plint", pl, "sac", bom=("Plint (süpürgelik) 304 fırçalı 1,5", 1, "ön x 0–%.0f · z +%.1f…+%.1f (ön düzlemin 60 gerisi) + hat sonu dönüşü · klipsli, sökülür"
                                        % (W - PLINT_GERI, Z_PLINT[0], Z_PLINT[1]), "v7"))


# ---------------------------------------------------------------- ŞARJÖR + ASANSÖR ----------------------------------------------------------------
X_TIRNAK = ((190.0, 220.0), (385.0, 415.0), (580.0, 610.0))
Z_KAPI0, Z_KAPI1 = ZS1 + 0.5, ZS1 + 3.5            # kapı plakası (itilen blankın önündeki eşik) −414,5 … −411,5
Y_KAPI_UST = Y_YIGIN_UST + 0.8                      # 980,8 (v5; v4 1148,8) · 2. blankı tutar, en üsttekini geçirir


def sarjor():
    # kılavuzlar (UHMW-PE 3 mm)
    ekle("kilavuz_sol_uhmw", kut(X_BL0 - 3.5, X_BL0 - 0.5, 244.0, 984.0, ZS0, ZS1), "uhmw",
         bom=("UHMW-PE şerit 3 mm (şarjör kılavuzu)", 3, "sol + sağ + arka", "levha"))
    ekle("kilavuz_sag_uhmw", kut(X_BL1 + 0.5, X_BL1 + 3.5, 244.0, 984.0, ZS0, ZS1), "uhmw", bom=None)
    ekle("kilavuz_sol_tasiyici", kut(SAC, X_BL0 - 3.5, 244.0, 984.0, -700.0, -680.0), "sac")
    # v9: the vertical stiffener is 10 mm behind the door skin, joined only
    # through inner top/bottom rails. No full-height batten against the outer face.
    kb = kut(815.5,818.5,244,984,-700,-680)
    for ya,yb in ((235.5,245.0),(978.0,984.5)):
        kb = kb.union(kut(815.5,828.5,ya,yb,-819,-415))
    ekle("kilavuz_sag_tasiyici", kb, "sac")
    ekle("kilavuz_arka_uhmw", kut(X_BL0, X_BL1, 244.0, 972.0, ZS0 - 3.5, ZS0 - 0.5), "uhmw")
    ekle("kilavuz_arka_tasiyici", kut(X_BL0 + 40.0, X_BL1 - 40.0, 244.0, 972.0, -D + SAC, ZS0 - 3.5), "sac")
    kapi = kut(X_BL0, X_BL1, Y_PLINT + 3.0, Y_KAPI_UST, Z_KAPI0, Z_KAPI1)      # v7: eşik tabana iner (v6: y 244'te başlıyor, hiçbir yere değmiyordu) — 4 dişli tarak
    for x0, x1 in X_TIRNAK:
        kapi = kapi.cut(kut(x0 - 2.0, x1 + 2.0, Y_PLINT + 2.0, 944.0, Z_KAPI0 - 1, Z_KAPI1 + 1))   # v7: asansör çatalı yarıkları alttan açık (platform en altta y 229)
    for x0, x1 in ESIK_DIS:     # v7b: her dişin altında ÖNE bükülü 3 mm ayak (tabana 2 × M5) — v7 ilk halinde tabana yalnız 3 mm'lik alt kenarıyla değiyordu (denetim bulgusu 3)
        kapi = kapi.union(kut(x0 + 5.0, x1 - 5.0, Y_PLINT + 3.0, Y_PLINT + 6.0, Z_KAPI1, Z_KAPI1 + ESIK_AYAK))
    ekle("sarjor_kapi_esigi", kapi, "sac", bom=("Şarjör eşiği 304 · 3 mm tarak (4 diş) + diş ayakları", 1, "804 × 855 · üst kenar 980,8 (2. blankı tutar) · ayaklar tabana 8 × M5 · "
                                                "iki yanda köşebentle yan saca", "v7b · üretim"))
    # v7b · eşik yan köşebentleri: eşiğin ön yüzüne (z −411,5) bindirme 32 × 50 + yan saca 50 × 31,5 (M5) — eşik iki ucundan mesnetli (olcum_v7 sehim hesabı)
    for ad_, x0, x1, xd0, xd1 in (("sol", SAC, X_BL0 + 32.0, SAC, SAC + 3.0), ("sag", X_BL1 - 32.0, W - SAC, W - SAC - 3.0, W - SAC)):
        k_ = kut(x0, x1, ESIK_KOS_Y[0], ESIK_KOS_Y[1], Z_KAPI1, Z_KAPI1 + 3.0).union(kut(xd0, xd1, ESIK_KOS_Y[0], ESIK_KOS_Y[1], Z_KAPI1, Z_KAPI1 + 31.5))
        ekle("sarjor_kapi_esigi_kosebendi_" + ad_, k_, "sac",
             bom=("Eşik köşebendi 304 · L 3 mm (bükümlü)", 1, "eşik ön yüzü ↔ yan sac · 2 + 2 × M5", "v7b · üretim"))
    # yığın (2. blanktan aşağısı) — en üstteki blank ayrı ve hareketli
    ekle("karton_yigini", kut(X_BL0, X_BL1, Y_PLAT, Y_YIGIN_UST, ZS0, ZS1), "karton_yigin",
         bom=("Pizza kutusu 32 × 32 × 4,2 E-dalga (düz açılım 804 × 404)", SARJOR_ADET, "yığın %.0f mm = %d adet @1,6 · %d @1,8 (v5 alçak hat; + fırın üstü yedek 320)"
              % (Y_YIGIN_UST - Y_PLAT, SARJOR_ADET, int((Y_YIGIN_UST - Y_PLAT) / 1.8)), "AmbalajPazarı · 100'lü paket (sarf)"))
    # asansör: platform + 3 çatal
    ekle("asansor_platformu", kut(X_BL0, X_BL1, Y_PLAT - 3.0, Y_PLAT, ZS0, ZS1), "aluminyum", "ASANSOR")
    for i, (x0, x1) in enumerate(X_TIRNAK):
        ekle("asansor_catali_%d" % i, kut(x0, x1, Y_PLAT - 11.0, Y_PLAT - 3.0, ZS0, -406.0), "celik", "ASANSOR")
    ekle("asansor_arabasi", kut(150.0, 650.0, 170.0, 300.0, -410.0, -406.0), "celik", "ASANSOR")
    # raylar: arka plaka z −378..−374 (kalıp rayının 1,5 mm arkası), raylar −z'ye bakar
    ekle("asansor_ray_plakasi", kut(200.0, 600.0, Y_PLINT + 3.0, 972.0, -378.0, -374.0), "sac")     # v7: tabana iner (v6: y 150'de havadaydı)
    # v7b: flanş L (yatay kol tabanda 400 × 20 · dik kol plakanın ön yüzünde 400 × 24) — v7 ilk halinde plakaya yalnız 3 mm'lik kenarıyla değiyordu
    ekle("asansor_ray_plakasi_flansi", kut(200.0, 600.0, Y_PLINT + 3.0, Y_PLINT + 6.0, -374.0, -354.0).union(kut(200.0, 600.0, Y_PLINT + 6.0, 150.0, -374.0, -371.0)), "sac",
         bom=("Ray plakası taban flanşı 304 · L 3 mm", 1, "400 × 20 tabana 4 × M6 · dik kol plakaya 4 × M5", "v7b: plakanın alt mesnedi"))
    # v7b: üst köşebentler plakanın ARKA yüzüne 30 mm bindirir (v7 ilk: aynı düzlemde uç uca 32 × 4) + yan saca dik kol (32 × 26) — L 4 mm + dik kol
    for ad_, x0, x1, xb0, xb1, xd0, xd1 in (("sol", SAC, 230.0, SAC, 230.0, SAC, SAC + 3.0), ("sag", 570.0, W - SAC, 570.0, W - SAC, W - SAC - 3.0, W - SAC)):
        k_ = kut(xb0, xb1, 940.0, 972.0, -382.0, -378.0).union(kut(x0, x1, 968.0, 972.0, -404.0, -382.0)).union(kut(xd0, xd1, 940.0, 972.0, -404.0, -378.0))
        ekle("asansor_ray_plakasi_ust_kosebendi_" + ad_, k_, "sac",
             bom=("Ray plakası üst köşebendi 304 · L 32 × 26 · 4 mm + yan saca dik kol", 1, "plakaya 30 mm bindirme (2 × M5) · yan saca 2 × M5 · yığın momenti", "v7b · üretim"))
    for i, xr in enumerate((250.0, 550.0)):
        hgr15("asansor_rayi_%d" % i, 822.0, (xr, 150.0, -378.0), (0, 1, 0), (0, 0, -1),
              bom=("Lineer ray HIWIN HGR15R", 2, "asansör · boy 822 (v5)", "hiwin.com") if i == 0 else ("Lineer ray HIWIN HGR15R", 0, "", ""))
        for j, yc in enumerate((200.0, 270.0)):
            hgh15("asansor_arabasi_%d%d" % (i, j), (xr, yc, -378.0), (0, 1, 0), (0, 0, -1), "ASANSOR")
    # trapez vida Tr16x4 (kendinden kilitli) + blok somun + yataklar + 2:1 kayış + motor (plint içinde)
    ekle("asansor_vidasi_Tr16x4", sily(405.0, -392.0, 8.0, 153.0, 957.0), "celik",
         bom=("Trapez vida Tr16×4 (DIN 103) + bronz blok somun", 1, "boy 807 (v5) + Ø12 alt uç 42 (tabandan geçer, kasnağı taşır) · kendinden kilitli (η≈0,35): güç kesilince yığın düşmez", "katalog"))
    ekle("asansor_vidasi_alt_ucu", sily(405.0, -392.0, 6.0, Y_TK - 1.0, 153.0), "celik")          # v3: işlenmiş Ø12 uç, tabanın altına iner
    ekle("asansor_somunu", kut(390.0, 420.0, 205.0, 250.0, -406.0, -380.0).cut(sily(405.0, -392.0, 8.2, 200, 260)), "celik", "ASANSOR")
    for ad_, y0 in (("asansor_alt_yatak", 153.0), ("asansor_ust_yatak", 957.0)):
        ekle(ad_, kut(385.0, 425.0, y0 - 12.0, y0, -410.0, -378.0).cut(sily(405.0, -392.0, 6.0, y0 - 13, y0 + 1)), "celik",
             bom=("Flanşlı yatak KFL001 (Ø12)", 2, "vida uçları", "katalog") if y0 < 500 else None)
    # v9: transmission INSIDE the cabinet, above the continuous bottom sheet.
    # Reuse the full-size motor, 2:1 ratio and screw. Shaft faces DOWN, body is in
    # the 65 mm service strip between the magazine and beverage cartons.
    # Nominal 750 mm / 3 mm pitch loop; motor slots provide +/-2 mm tension travel.
    r1, r2 = 60.0 / math.pi, 30.0 / math.pi
    lo, hi = 320.0, 340.0
    for _ in range(40):
        c = (lo + hi) / 2.0
        length = 2.0 * math.sqrt(c*c - (r1-r2)**2) + math.pi*(r1+r2) + 2.0*(r1-r2)*math.asin((r1-r2)/c)
        if length < 750.0: lo = c
        else: hi = c
    mx, mz, my = 405.0 + math.sqrt(c*c - 11.0**2), -381.0, 147.0
    pd1 = kasnak("asansor_kasnak_40", 405.0, Y_TK, -392.0, 40)
    pd2 = kasnak("asansor_kasnak_20", mx, Y_TK, mz, 20)
    kayis_y("asansor_kayisi", 405.0, -392.0, mx, mz, Y_TK + 1.0, pd1, pd2)
    mp = kut(704.0, 766.0, my - 3.0, my, -410.0, -351.0)
    mp = mp.cut(sily(mx - 2.0, mz, 19.5, my - 4.0, my + 1.0).union(sily(mx + 2.0, mz, 19.5, my - 4.0, my + 1.0)).union(kut(mx-2,mx+2,my-4,my+1,mz-19.5,mz+19.5)))
    for sx in (-23.57,23.57):
        for sz in (-23.57,23.57):
            slot = sily(mx+sx-2,mz+sz,2.1,my-4,my+1).union(sily(mx+sx+2,mz+sz,2.1,my-4,my+1)).union(kut(mx+sx-2,mx+sx+2,my-4,my+1,mz+sz-2.1,mz+sz+2.1))
            mp = mp.cut(slot)
    for za, zb in ((-410.0, -407.0), (-354.0, -351.0)):
        mp = mp.union(kut(704.0, 766.0, Y_PLINT + 3.0, my - 3.0, za, zb))
    ekle("asansor_motor_plakasi", mp, "sac", bom=("Motor sehpası 304 3 mm", 1, "tabana kaynaklı; motor 4xM4 ayar yarığı; 750-3M-9 kayış", "v9 · tam boy NEMA23 korunur; sipariş teyidi gerekli"))
    nema23("asansor_motoru", (mx, my, mz), (0, -1, 0), (0, 0, 1))
    # Low removable cover; shaft holes, no enlarged exterior box or floor skirt.
    kor = kut(380.0, 772.0, 126.0, 143.0, -417.0, -363.0).cut(kut(381.0, 771.0, 125.0, 142.0, -416.0, -364.0))
    kor = kor.cut(kut(384.0,426.0,140.0,144.0,-411.0,-377.0)).cut(sily(mx, mz, 14.5, 140.0, 144.0))
    kor = kor.cut(kut(703.5,766.5,125.0,144.0,-410.5,-406.5))
    ekle("asansor_kayis_koruyucu", kor, "sac", bom=("İç kayış koruyucu 304 1 mm", 1, "taban üstünde sökülür", "v9"))
    # Local service cutouts only in internal supports, never the outer shell.
    relief = kut(379.0, 773.0, 125.5, 144.0, -418.0, -365.0)
    for p in PARCALAR:
        if p["ad"] in ("asansor_ray_plakasi", "asansor_ray_plakasi_flansi", "sarjor_kapi_esigi"):
            p["wp"] = p["wp"].cut(relief)
        if p["ad"] == "asansor_ray_plakasi_flansi":
            # Z-fold: uniform full-width floor support in FRONT of the belt.
            p["wp"] = kut(200,600,147,150,-374,-354).union(kut(200,600,126,147,-357,-354)).union(kut(200,600,126,129,-363,-354))
    # Actual shaft bores, rather than overlapping solid cylinders.
    for p in PARCALAR:
        if p["ad"] == "asansor_kasnak_40": p["wp"] = p["wp"].cut(sily(405,-392,6,Y_TK-2,Y_TK+13))
        if p["ad"] == "asansor_kasnak_20": p["wp"] = p["wp"].cut(sily(mx,mz,3.175,Y_TK-2,Y_TK+13))
    e2e("asansor_alt_sensor", 610.0, 150.0, -386.0, "y")
    # v7b: delikli sensör sacı (Ø8 + 2 somun, iki uç açık) + plakanın arka yüzüne 30 × 13 bindirme (v7 ilk: 4 × 3 mm temas, sensörün alt yüzünü kapatıyordu)
    ekle("asansor_alt_sensor_braketi", kut(570.0, 618.0, 160.0, 163.0, -394.0, -378.0).cut(sily(610.0, -386.0, 4.02, 159.0, 164.0))
         .union(kut(570.0, 600.0, 150.0, 163.0, -381.0, -378.0)), "sac", bom=SENSOR_BRAKET_BOM)


# ---------------------------------------------------------------- BESLEYİCİ (İTİCİ) ----------------------------------------------------------------
Y_BES_PL = 1332.0                # v5 (1500 − 168) · besleyici üst plakası altı — dik kapağın (flapıyla 1298) ÜSTÜNDE: raylar kapağın −z flap düzlemini kesmez
Z_RAY_BES = (-828.0, -355.0)          # raylar plakadan 22 mm taşar (piston bağlantı plakası x 170–370'te, raylar x 150/650'de)
Z_BES_PL1 = -367.0                    # plaka ön kenarı: dik kapağın −z flapı −363,5'e kadar gelir


def besleyici():
    """itici: en üstteki blankı arka kenarından yakalayıp 411 mm öne (kalıbın üstüne) sürer.
    2 HGR15 ray plakanın altında (x 150 / 650), GT3 kayış plakanın üstünde (x 729,5), motor plakanın +x ucunun ötesinde."""
    pl = kut(100.0, 721.0, Y_BES_PL, Y_BES_PL + 5.0, Z_RAY_BES[0], Z_BES_PL1).cut(kut(165.0, 375.0, Y_BES_PL - 1, Y_BES_PL + 6, -400.0, Z_BES_PL1 + 1))   # piston ekseni cebi
    ekle("besleyici_plakasi", pl, "aluminyum", bom=("Besleyici plakası 6082 · 5 mm", 1, "621 × 461", "üretim"))
    for i, xr in enumerate((150.0, 650.0)):
        ekle("besleyici_plaka_askisi_%d" % i, kut(xr - 10.0, xr + 10.0, Y_BES_PL + 5.0, H - SAC, -600.0, -580.0), "aluminyum")
        hgr15("besleyici_rayi_%d" % i, Z_RAY_BES[1] - Z_RAY_BES[0], (xr, Y_BES_PL, Z_RAY_BES[0]), (0, 0, 1), (0, -1, 0),
              bom=("Lineer ray HIWIN HGR15R", 2, "besleyici · boy 473", "hiwin.com") if i == 0 else ("Lineer ray HIWIN HGR15R", 0, "", ""))
        hgh15("besleyici_arabasi_%d" % i, (xr, Y_BES_PL, -797.0), (0, 0, 1), (0, -1, 0), "ITICI")      # 411 strokta araba iki uçta da rayda (0,3 mm)
    # iki araba plakası (arka köşe plow askısı x 450–462 arada kalır) + asma plakalar + kiriş + itici çubuk
    ekle("itici_araba_plakasi_sol", kut(130.0, 168.0, Y_BES_PL - 34.0, Y_BES_PL - 28.0, -826.0, -762.0), "aluminyum", "ITICI")
    ekle("itici_araba_plakasi_sag", kut(630.0, 725.0, Y_BES_PL - 34.0, Y_BES_PL - 28.0, -826.0, -750.0), "aluminyum", "ITICI")
    for i, xr in enumerate((150.0, 650.0)):
        ekle("itici_asma_plakasi_%d" % i, kut(xr - 20.0, xr + 20.0, 1008.2, Y_BES_PL - 34.0, -826.0, -818.0), "aluminyum", "ITICI")
    ekle("itici_kirisi_40x20", kut(10.0, 810.0, 988.2, 1008.2, -826.0, -819.5), "aluminyum", "ITICI")
    ekle("itici_cubugu", kut(10.0, 810.0, YB + 0.6, 988.2, -826.0, -819.5), "celik", "ITICI",
         bom=("İtici çubuk 304 · 800 × 6,5 × 6", 1, "alt kenarı 982,2: yalnız EN ÜSTTEKİ blankı yakalar (981,6–983,2)", "üretim"))
    # kayış tahriki (plakanın üstünde): TAHRİK ÖNDE (z −345), AVARA ARKADA (z −815). Kasnak kenarları arası 446,6 mm;
    # çene (20) 411 strok yapar → önde 15 mm pay kalır. (v1 ilk hali: kasnaklar 410 aralıkta, çene strok sonunda avaraya giriyordu.)
    YK = Y_BES_PL + 25.0
    pdm = kasnak("besleyici_kasnak_tahrik", 725.0, YK, -345.0, 20, eksen="x")
    pdi = kasnak("besleyici_kasnak_avara", 725.0, YK, -815.0, 20, eksen="x")
    kayis_z("besleyici_kayisi", YK, -345.0, YK, -815.0, 726.0, pdm, pdi)
    ekle("besleyici_avara_yatagi", kut(700.0, 721.0, Y_BES_PL + 5.0, YK + 16.0, -826.0, -805.0), "aluminyum")

    ekle("besleyici_avara_mili", silx(YK, -815.0, 4.0, 700.0, 740.0), "celik")
    ekle("itici_kayis_kulagi", kut(722.0, 725.0, Y_BES_PL - 28.0, Y_BES_PL + 5.0, -803.0, -783.0), "celik", "ITICI")
    ekle("itici_kayis_cenesi", kut(722.0, 737.0, Y_BES_PL + 5.0, YK - 10.8, -803.0, -783.0), "celik", "ITICI")
    nema23("besleyici_motoru", (742.0, YK, -345.0), (-1, 0, 0), (0, 1, 0))
    ekle("besleyici_motor_braketi", kut(738.0, 742.0, YK - 30.0, YK + 30.0, -376.0, -314.0).cut(silx(YK, -345.0, 20.0, 737, 743)), "aluminyum")
    ekle("besleyici_motor_rafi", kut(738.0, W - SAC, YK - 36.0, YK - 30.0, -376.0, -314.0), "aluminyum")
    e2e("besleyici_arka_sensor", 600.0, Y_BES_PL - 18.0, -828.0 + 7.5, "z")
    for i, xr in enumerate((150.0, 650.0)):      # v7: plaka iki askıyla tek z hattında (−590) asılıydı (öne-arkaya devrilir) → önde 2 askı daha
        ekle("besleyici_plaka_askisi_%d" % (i + 2), kut(xr - 10.0, xr + 10.0, Y_BES_PL + 5.0, H - SAC, -420.0, -400.0), "aluminyum")
    # v7b: delikli sensör sacı (z −812…−809) + plakanın altına 20 × 22 kol (v7 ilk: sensöre teğet çizgiyle değen blok)
    ekle("besleyici_arka_sensor_braketi", kut(590.0, 610.0, Y_BES_PL - 26.0, Y_BES_PL, -812.0, -809.0).cut(silz(600.0, Y_BES_PL - 18.0, 4.02, -813.0, -808.0))
         .union(kut(590.0, 610.0, Y_BES_PL - 3.0, Y_BES_PL, -812.0, -790.0)), "aluminyum", bom=SENSOR_BRAKET_BOM)


# ---------------------------------------------------------------- KALIP + TEPSİ ----------------------------------------------------------------
X_CATAL = ((157.0, 183.0), (247.0, 273.0), (337.0, 363.0))     # robot çatal dişleri
X_BAR = ((BX0, 155.0), (185.0, 245.0), (275.0, 335.0), (365.0, BX1))


def kalip():
    ekle("kalip_tablasi_6", kut(90.0, 430.0, 912.0, 918.0, -372.5, -32.0), "sac")
    for i, (xp, zp) in enumerate(((110.0, -340.0), (410.0, -340.0), (110.0, -70.0), (410.0, -70.0))):
        ekle("kalip_ayagi_%d" % i, kut(xp - 20.0, xp + 20.0, ALT_RAF_Y[1], 912.0, zp - 20.0, zp + 20.0).cut(kut(xp - 17.8, xp + 17.8, ALT_RAF_Y[1] - 1, 913, zp - 17.8, zp + 17.8)), "aluminyum",
             bom=("Alüminyum profil 40 × 40 (kalıp ayağı)", 4, "boy %.0f (v4: alt rafta biter)" % (912.0 - ALT_RAF_Y[1]), "item / Bosch Rexroth 40×40") if i == 0 else None)
    # v4 · ALT RAF (Kemal): ayaklar burada biter, altı boş
    ekle("kalip_alt_rafi", kut(4.0, 800.0, ALT_RAF_Y[0], ALT_RAF_Y[1], -372.0, -24.0).cut(kut(720.0, 780.0, ALT_RAF_Y[0] - 1.0, ALT_RAF_Y[1] + 1.0, -330.0, -270.0)), "sac",   # v7: flap katlayıcı motoru (STEP tam boy, alt ucu 618,5) için 60 × 60 kesik
         bom=("Alt raf 304 · 4 mm", 1, "796 × 348", "v4: kalıp + kapak plakası ayakları üstünde · v5: altı 126–588, önde içecek yedeği 6 koli (x 3–805 · y 130–499 · z −350…−83)"))
    _y0 = ALT_RAF_Y[0]
    ekle("kalip_alt_rafi_koseben_sol", kut(SAC, 32.0, _y0 - 30.0, _y0, -372.0, -24.0).cut(kut(SAC + 3.0, 33.0, _y0 - 31.0, _y0 - 3.0, -373.0, -23.0)), "sac",   # v7: sol yan saca oturur (v6: 0,5 mm havada)
         bom=("Köşebent 30 × 30 × 3 AISI 304 (alt raf)", 4, "sol/sağ duvar + ön/arka kenar", "M6 ile duvara"))
    ekle("kalip_alt_rafi_koseben_sag", kut(770.0, 800.0, _y0 - 30.0, _y0, -372.0, -55.0).cut(kut(769.0, 797.0, _y0 - 31.0, _y0 - 3.0, -373.0, -54.0))
         .cut(kut(719.0, 781.0, _y0 - 31.0, _y0 + 1.0, -331.0, -269.0)), "sac")   # v7b: yatay kolda flap katlayıcı motoru çentiği (motor 8,5 indi, alt ucu 610)
    ekle("kalip_alt_rafi_duvar_takozu_sag", kut(800.0, W - SAC, _y0 - 30.0, _y0, -372.0, -55.0).cut(kut(802.0, W - SAC - 2.0, _y0 - 28.0, _y0 - 2.0, -373.0, -54.0)), "sac",
         bom=("Duvar takozu 304 kutu profil 28,5 × 30 × 2", 1, "sağ köşebent ↔ sağ yan sac (v6: 28,5 mm havada) · kablo kanalının arkasında biter (z −55)", "v7 · üretim"))
    ekle("kalip_alt_rafi_koseben_on", kut(32.0, 770.0, _y0 - 30.0, _y0, -54.0, -24.0).cut(kut(31.0, 771.0, _y0 - 31.0, _y0 - 3.0, -55.0, -27.0)), "sac")
    ekle("kalip_alt_rafi_koseben_arka", kut(32.0, 770.0, _y0 - 30.0, _y0, -372.0, -342.0).cut(kut(31.0, 771.0, _y0 - 31.0, _y0 - 3.0, -369.0, -341.0)), "sac")
    # tepsi çubukları (robot çatalı aralarından girer); ön çubukta kilit dili cebi
    for i, (x0, x1) in enumerate(X_BAR):
        b = kut(x0, x1, 928.0, TEPSI, BZ0, BZ1)
        if i == 0:
            for z0, z1 in DIL_Z:
                b = b.cut(kut(x0 - 1, x0 + 32.0, 926.0, TEPSI + 1, z0 - 2.0, z1 + 2.0))      # kilit dili cebi: dil devrilirken 30 mm ileriden iner
        ekle("tepsi_cubugu_%d" % i, b, "sac")
        ekle("tepsi_ayagi_%d" % i, kut((x0 + x1) / 2.0 - 8.0, (x0 + x1) / 2.0 + 8.0, 918.0, 928.0, ZB - 8.0, ZB + 8.0), "sac")
    # arka (−z) kalıp rayı ve ön (+z) tarak — tarağın dişleri arasından çatal geçer
    ekle("kalip_rayi_arka_z", kut(BX0, 405.0, 918.0, KALIP, BZ0 - T - 6.0, BZ0 - T - 0.5), "sac", bom=("Kalıp rayı 304 · 6 mm", 1, "arka yan duvarı kaldırır", "üretim"))
    for i, (x0, x1) in enumerate(X_BAR):
        ekle("kalip_taragi_on_z_%d" % i, kut(max(x0, BX0), min(x1, 405.0), 918.0, KALIP, BZ1 + T + 0.5, BZ1 + T + 6.5), "sac",
             bom=("Kalıp tarağı 304 · 6 mm (4 diş)", 1, "ön yan duvarı tutar · dişleri arasından robot çatalı geçer", "üretim") if i == 0 else None)
    ekle("kalip_on_x_rayi", kut(93.4, 97.9, 918.0, KALIP - 20.0, BZ0, BZ1), "sac", bom=("Kalıp ön rayı 304 · 4,5 mm", 1, "ön duvar 20 mm geç kalkar (köşe tırnakları önce döner)", "üretim"))
    ekle("kalip_arka_x_dayagi", kut(BX1 + T + 0.5, BX1 + T + 6.5, 918.0, TEPSI + 8.0, BZ0, BZ1), "sac")
    # KÖŞE TIRNAĞI KIVIRICISI MODELLENMEDİ (v1): sabit plow + askıları yükselen tırnakların ve kapak flaplarının
    # yolunda kalıyordu (geçiş taraması). Seçenekler sayfada: kalıp köşesinde eğik takoz / 2 küçük döner kıvırıcı.


# ---------------------------------------------------------------- KÖPRÜ (pizza yolu, düşer) ----------------------------------------------------------------
KOPRU_ALT = 30.0


def kopru():
    """pizza köprüsü: katlamada 30 mm AŞAĞIDA (ön paneller serbest kalkar), pizza gelirken kalıp kotuna çıkar"""
    ekle("kopru_plakasi", kut(2.0, 92.0, KALIP - 3.0 - KOPRU_ALT, KALIP - KOPRU_ALT, BZ0, BZ1), "sac", "KOPRU",
         bom=("Köprü sacı 304 · 3 mm", 1, "pizza yolu · katlamada 30 mm aşağıda", "üretim"))
    ekle("kopru_tasiyici", kut(30.0, 64.0, 912.0, KALIP - 3.0 - KOPRU_ALT, ZB - 40.0, ZB + 40.0).cut(sily(47.0, ZB, 9.0, 911, 952)), "aluminyum", "KOPRU")
    for i, zc in enumerate((BZ0 + 40.0, BZ1 - 40.0)):
        ekle("kopru_kilavuz_mili_%d" % i, sily(47.0, zc, 6.0, 782.0, KALIP - 3.0 - KOPRU_ALT), "celik", "KOPRU",
             bom=("Kılavuz mili Ø12 h6 + lineer burç LM12UU", 2, "köprü", "katalog") if i == 0 else None)
        ekle("kopru_burcu_%d" % i, boru_y(47.0, zc, 10.5, 6.1, 817.0, 847.0), "celik")
    bp = kut(20.0, 74.0, 847.0, 853.0, BZ0 + 20.0, BZ1 - 20.0)
    for zc in (BZ0 + 40.0, BZ1 - 40.0):
        bp = bp.cut(sily(47.0, zc, 6.3, 846, 854))
    ekle("kopru_burc_plakasi", bp.cut(sily(47.0, ZB, 9.0, 846, 854)), "aluminyum")
    ekle("kopru_plaka_tutucu", kut(SAC, 16.0, 832.0, 853.0, BZ0 + 20.0, BZ1 - 20.0).union(kut(16.0, 20.0, 847.0, 853.0, BZ0 + 20.0, BZ1 - 20.0)), "aluminyum")   # v7: üst dudak burç plakasına uzar (v6: 4 mm havada) · BK12'nin üstünden geçer
    sfu16("kopru_vidasi", 47.0, ZB, 832.0, 944.0, 5, "KOPRU", 855.0)
    bk12("kopru_BK12", 47.0, ZB, 814.5, 1)
    Y_KM = 784.5 - MOTOR_INDIR          # v7b: motor flanşı 776 (v7 ilk 784,5) — mil ucu 796,6 kaplinin motor göbeğinde (786,5–797,5)
    kaplin("kopru_kaplini", 47.0, 814.5 - KAPLIN["pay_ust"] - KAPLIN["L"], ZB)     # v7b: BK12 altı 814,5 − 2 − 26 = 786,5
    nema23("kopru_motoru", (47.0, Y_KM, ZB), (0, 1, 0), (0, 0, 1))
    ekle("kopru_motor_braketi", kut(17.0, 77.0, Y_KM, Y_KM + 6.0, ZB - 30.0, ZB + 30.0).cut(sily(47.0, ZB, 20.0, Y_KM - 1.5, Y_KM + 7.5)), "aluminyum")
    ekle("kopru_motor_askisi", kut(SAC, 17.0, Y_KM, 832.0, ZB - 30.0, ZB + 30.0), "aluminyum")   # v7: motor braketine + BK12'ye değer (v6: 1 mm havada) · v7b: braketle 8,5 iner
    e2e("kopru_alt_sensor", 72.0, 862.0, ZB + 34.0, "y")
    # v7b: Z büküm — ayak burç plakasının üstüne (15 × 20), dik kol, delikli sensör sacı (y 870–873) · v7 ilk: sensörün alt yüzünü kapatan blok
    ekle("kopru_alt_sensor_braketi", kut(50.0, 65.0, 853.0, 856.0, ZB + 24.0, ZB + 44.0).union(kut(62.0, 65.0, 856.0, 873.0, ZB + 24.0, ZB + 44.0))
         .union(kut(62.0, 86.0, 870.0, 873.0, ZB + 24.0, ZB + 44.0).cut(sily(72.0, ZB + 34.0, 4.02, 869.0, 874.0))), "aluminyum", bom=SENSOR_BRAKET_BOM)


# ---------------------------------------------------------------- PİSTON ----------------------------------------------------------------
PK_X = (112.0, 408.0)
PK_Z = (-354.0, -58.0)
Z_PBAG = (-361.0, -351.0)       # kafayı arabaya bağlayan dikey plaka (kapak −z flapının 0,5 mm içinde)


def piston():
    """zımba: tabanı kalıba basar (45,6), 2. vuruşta devrilmiş iç paneli kilitler, 3. vuruşta kapağı kapatıp bastırır.
    Vida SFU1610 üstten BK12 ile tutulur, altı serbest (sabit–serbest): bağlantı plakası vidanın arkasından geçtiği için
    alt yatağın braketi hareket yoluna düşüyordu. Kontrol: 450 mm Ø16 burkulma ~3,5 kN ≫ 170 N; kritik devir ~2760 d/dk > 1800."""
    h = H_UST
    kafa_ = cq.Workplane("XY").polyline([(PK_X[0] + 6.0, h), (PK_X[1], h), (PK_X[1], h + 20.0), (PK_X[0], h + 20.0), (PK_X[0], h + 6.0)]).close() \
        .extrude(PK_Z[1] - PK_Z[0]).translate((0, 0, PK_Z[0]))
    ekle("piston_kafasi", kafa_, "aluminyum", "PISTON",
         bom=("Piston kafası 6082 · 296 × 296 × 20 · ön alt kenar 6 mm pah", 1, "tabana basar, iç paneli kilitler, kapağı bastırır", "üretim"))
    for i, xc in enumerate((200.0, 320.0)):
        ekle("piston_kaburgasi_%d" % i, kut(xc - 4.0, xc + 4.0, h + 20.0, h + 70.0, PK_Z[0] + 5.0, PK_Z[1] - 5.0), "aluminyum", "PISTON")
    ekle("piston_baglanti_plakasi", kut(170.0, 370.0, h + 20.0, h + 535.0, Z_PBAG[0], Z_PBAG[1]), "aluminyum", "PISTON")
    ekle("piston_eksen_plakasi", kut(170.0, 370.0, 1332.0, 1847.0, -394.0, -389.0), "aluminyum")
    ekle("piston_eksen_askisi", kut(170.0, 370.0, 1847.0, H - SAC, -394.0, -380.0), "aluminyum")
    for i, xr in enumerate((200.0, 340.0)):
        hgr15("piston_rayi_%d" % i, 515.0, (xr, 1332.0, -389.0), (0, 1, 0), (0, 0, 1),
              bom=("Lineer ray HIWIN HGR15R", 2, "piston · boy 515", "hiwin.com") if i == 0 else ("Lineer ray HIWIN HGR15R", 0, "", ""))
        for j, yc in enumerate((h + 440.0, h + 500.0)):
            hgh15("piston_arabasi_%d%d" % (i, j), (xr, yc, -389.0), (0, 1, 0), (0, 0, 1), "PISTON")
    sfu16("piston_vidasi", 270.0, -325.0, 1347.0, 1840.0, 10, "PISTON", h + 417.0)
    ekle("piston_somun_braketi", kut(240.0, 300.0, h + 464.0, h + 474.0, -351.0, -299.0).cut(sily(270.0, -325.0, 14.5, h + 463, h + 475)), "aluminyum", "PISTON")
    bk12("piston_BK12", 270.0, -325.0, 1790.0, 1)
    for i, (z0, z1) in enumerate(((-345.0, -339.0), (-311.0, -305.0))):              # v2: ayaklar kayışın iki yanında (z)
        ekle("piston_BK_askisi_%d" % i, kut(240.0, 300.0, 1822.5, H - SAC, z0, z1), "aluminyum")
    pd1 = kasnak("piston_kasnak_vida", 270.0, 1827.5, -325.0, 20)
    pd2 = kasnak("piston_kasnak_motor", 340.0, 1827.5, -318.0, 20)
    kayis_y("piston_kayisi", 270.0, -325.0, 340.0, -318.0, 1828.5, pd1, pd2)
    nema23("piston_motoru", (340.0, 1822.0, -318.0), (0, 1, 0), (0, 0, 1))
    ekle("piston_motor_braketi", kut(308.0, 372.0, 1822.0, 1826.0, -350.0, -286.0).cut(sily(340.0, -318.0, 20.0, 1821, 1827)), "aluminyum")
    for i, (x0, x1) in enumerate(((308.0, 316.0), (364.0, 372.0))):
        ekle("piston_motor_askisi_%d" % i, kut(x0, x1, 1826.0, H - SAC, -350.0, -336.0), "aluminyum")
    e2e("piston_ust_sensor", 385.0, 1782.0, -389.0 + 2.0, "z")
    # v7b: U büküm — arka kol eksen plakasının ARKA yüzüne (30 × 24), kenarı dolanır, ön kol delikli sensör sacı (v7 ilk: 3 × 5 mm kenar teması)
    ekle("piston_ust_sensor_braketi", kut(340.0, 373.0, 1770.0, 1794.0, -397.0, -394.0).union(kut(370.0, 373.0, 1770.0, 1794.0, -397.0, -380.0))
         .union(kut(370.0, 395.0, 1770.0, 1794.0, -383.0, -380.0).cut(silz(385.0, 1782.0, 4.02, -384.0, -379.0))), "aluminyum", bom=SENSOR_BRAKET_BOM)
    for ad_, x0 in (("sol", 180.0), ("sag", 320.0)):      # v7: eksen plakası besleyici plakasına bağlanır (v6: yalnız üstteki 13,5 mm bloktan asılı) ·
        # v7b: L köşebent — yatay kol besleyici plakasının üstünde (40 × 20 bindirme, cebin arkasında), dik kol eksen plakasının arka yüzünde (40 × 40) · v7 ilk: 5 mm küp
        ekle("piston_eksen_plakasi_bagi_" + ad_, kut(x0, x0 + 40.0, Y_BES_PL + 5.0, Y_BES_PL + 8.0, -420.0, -394.0).union(kut(x0, x0 + 40.0, Y_BES_PL + 8.0, Y_BES_PL + 45.0, -397.0, -394.0)),
             "aluminyum", bom=("Köşebent 6082 · L 3 mm (piston eksen plakası ↔ besleyici plakası)", 1, "2 + 2 × M5", "v7b · üretim"))


PARMAK_P = (88.0, 1092.0)       # v5: 1260 − 168
PARMAK_R = 72.0
PARMAK_Z = (-350.0, -62.0)


def parmak():
    """iç ön paneli devirir: üstten iner, dik duran panelin tepesini kutunun içine iter (sonra yerçekimi + 2. vuruş)"""
    px, py = PARMAK_P
    p = kut(px - 4.0, px + 4.0, py, py + PARMAK_R, PARMAK_Z[0], PARMAK_Z[1]).union(silz(px, py, 12.0, PARMAK_Z[0], PARMAK_Z[1]))
    ekle("devirme_parmagi", p, "celik", "PARMAK", bom=("Devirme parmağı 304 · 8 mm", 1, "R 72 · 140° döner", "üretim"))
    ekle("parmak_mili", silz(px, py, 6.0, -425.0, PARMAK_Z[0]), "celik")
    for i, (z0, z1) in enumerate(((-364.0, -354.0), (-420.0, -410.0))):
        ekle("parmak_yatagi_%d" % i, kut(px - 16.0, px + 16.0, py - 16.0, py + 16.0, z0, z1).cut(silz(px, py, 6.1, z0 - 1, z1 + 1)), "celik",
             bom=("Flanşlı yatak KFL001 (Ø12)", 2, "parmak mili", "katalog") if i == 0 else None)
    ekle("parmak_yatak_askisi", kut(px - 16.0, px + 16.0, py + 16.0, Y_BES_PL, -420.0, -370.0), "aluminyum")
    ekle("parmak_yatak_kolu_on", kut(px - 16.0, px + 16.0, py + 16.0, py + 26.0, -370.0, -354.0), "aluminyum")
    pgcn23("parmak_reduktoru", (px, py, -425.0), (0, 0, 1), (0, 1, 0))
    nema23("parmak_motoru", (px, py, -504.0), (0, 0, 1), (0, 1, 0))
    ekle("parmak_red_braketi", kut(px - 29.0, px + 29.0, py + 29.0, Y_BES_PL, -432.0, -425.0), "aluminyum")
    e2e("parmak_sensor", px + 22.0, py + 20.0, -400.0, "z")
    ekle("parmak_red_flans_plakasi", kut(px - 29.0, px + 29.0, py - 29.0, py + 45.0, -425.0, -421.0).cut(silz(px, py, 12.0, -426.0, -420.0)), "aluminyum")   # v7: redüktör çıkış flanşı bu plakaya, plaka brakete (v6: 0,42 mm değmiyordu) · v7b: brakete 16 mm bindirir (ilk: 4)
    # v7b: delikli sensör sacı (z −392…−389) + yatak askısının yan yüzüne (x 104) 20 × 22 dik kol, sensörün ÜSTÜNDE (sensör x 106'dan başlar) · v7 ilk: sensöre teğet lam
    ekle("parmak_sensor_braketi", kut(104.0, 107.0, py + 28.0, py + 48.0, -392.0, -370.0).union(kut(104.0, 122.0, py + 8.0, py + 32.0, -392.0, -389.0).cut(silz(px + 22.0, py + 20.0, 4.02, -393.0, -388.0))),
         "aluminyum", bom=SENSOR_BRAKET_BOM)


# ---------------------------------------------------------------- KAPAK MASASI · U ÇERÇEVE · KOL ----------------------------------------------------------------
KM_X = (466.0, 730.0)
KOL_Z = (ZB - 10.0, ZB + 10.0)
UC_KALK = 37.6
KM_UST = TEPSI + T / 2.0 + H_ARKA - T / 2.0          # 980,0 (v5; v4 1148,0) · kapak masası üstü = kapaklı kutuda kapağın alt yüzü


def kapak_mekanizmasi():
    m = kut(KM_X[0], KM_X[1], KM_UST - 3.0, KM_UST, ZL0 + 1.5, ZL1 - 1.5).cut(kut(KM_X[0] - 1.0, 745.0, KM_UST - 4, KM_UST + 1, KOL_Z[0] - 3.0, KOL_Z[1] + 3.0))
    for _i8, (_za8, _zb8) in enumerate(((ZL0, KOL_Z[0] - 3.0), (KOL_Z[1] + 3.0, ZL1))):          # v8: yarık boydan boya → açıkça iki levha (v7: tek parça sanılıyordu)
        ekle("kapak_masasi_%d" % _i8, m.intersect(kut(KM_X[0] - 1.0, KM_X[1] + 1.0, KM_UST - 4.0, KM_UST + 1.0, _za8, _zb8)), "sac",
             bom=("Kapak masası levhası 304 · 3 mm", 2, "264 × 143 · aralarında 26 mm kol yarığı (kol β 0…144°, iz x 471–726) · her levha kendi direğine", "üretim") if _i8 == 0 else None)
    for i, zc in enumerate((ZB - 110.0, ZB + 110.0)):
        ekle("kapak_masasi_diregi_%d" % i, sily(600.0, zc, 8.0, 832.0, KM_UST - 3.0), "celik")
    ekle("kapak_alt_plakasi", kut(440.0, 800.0, 826.0, 832.0, -368.0, BZ1 + 20.0).cut(sily(750.0, -300.0, 15.0, 825, 833)), "aluminyum")
    ekle("kapak_alt_plaka_ayagi_0", kut(780.0, 800.0, ALT_RAF_Y[1], 826.0, -368.0, -348.0), "aluminyum")   # v4: alt rafta biter
    ekle("kapak_alt_plaka_ayagi_1", kut(780.0, 800.0, ALT_RAF_Y[1], 826.0, BZ1, BZ1 + 20.0), "aluminyum")
    for i, (z0, z1) in enumerate(((-368.0, -348.0), (BZ1, BZ1 + 20.0))):   # v7: kalıp tarafında 2 ayak daha (v6: plaka x 440–800 yalnız sağ ayaklarda, 340 mm konsol)
        ekle("kapak_alt_plaka_ayagi_%d" % (i + 2), kut(440.0, 460.0, ALT_RAF_Y[1], 826.0, z0, z1), "aluminyum")
    # U çerçeve: 3 ince plaka (−z, +z, +x) + +x kolunun dışında bağ; masa direkleri kılavuz
    xa = X_BL1 - H_KF - H_ARKA + T                      # kapak ucu kırımı (733,6) — kayma sonrası
    uc = kut(466.0, xa + 3.0, 944.0, KM_UST, ZL0 - 3.0 - T, ZL0 - T)
    uc = uc.union(kut(466.0, xa + 3.0, 944.0, KM_UST, ZL1 + T, ZL1 + 3.0 + T))
    uc = uc.union(kut(xa, xa + 3.0, 944.0, KM_UST, ZL0 - 3.0 - T, ZL1 + 3.0 + T))
    ekle("flap_katlayici_U", uc, "sac", "KATLAYICI", bom=("Flap katlayıcı U çerçeve 304 · 3 mm", 1, "37,6 mm kalkar: kapağın 3 flapını 90° kaldırır", "üretim"))
    ekle("flap_katlayici_alt_bagi", kut(xa + 3.0, xa + 18.0, 890.0, 944.0, ZL0 - 3.0 - T, ZL1 + 3.0 + T).cut(sily(750.0, -300.0, 10.0, 882, 952)), "aluminyum", "KATLAYICI")
    ekle("flap_katlayici_somun_kolu", kut(xa + 3.0, 770.0, 890.0, 900.0, -330.0, -270.0).cut(sily(750.0, -300.0, 8.2, 882, 902)), "aluminyum", "KATLAYICI")
    sfu16("flap_katlayici_vidasi", 750.0, -300.0, 732.0, 932.0, 5, "KATLAYICI", 833.0)
    Y_FM = 694.0 - MOTOR_INDIR          # v7b: motor flanşı 685,5 (v7 ilk 694) — gövde alt raf kesiğinden geçer, raf köşebendinde çentik
    nema23("flap_katlayici_motoru", (750.0, Y_FM, -300.0), (0, 1, 0), (0, 0, 1))
    kaplin("flap_katlayici_kaplini", 750.0, 724.0 - KAPLIN["pay_ust"] - KAPLIN["L"], -300.0)    # v7b: yatak braketi altı 724 − 2 − 26 = 696
    ekle("flap_katlayici_motor_braketi", kut(720.0, 780.0, Y_FM, Y_FM + 6.0, -330.0, -270.0).cut(sily(750.0, -300.0, 20.0, Y_FM - 1.0, Y_FM + 7.0)), "aluminyum")
    ekle("flap_katlayici_yatak_braketi", kut(720.0, 780.0, 724.0, 732.0, -330.0, -270.0).cut(sily(750.0, -300.0, 6.0, 723, 733)), "aluminyum")
    ekle("flap_katlayici_braket_ayagi", kut(780.0, 790.0, Y_FM, 826.0, -330.0, -270.0), "aluminyum")
    e2e("flap_katlayici_sensor", 700.0, 862.0, -300.0, "y")
    # v7b: Z büküm — ayak kapak alt plakasının üstüne (15 × 20), dik kol, delikli sensör sacı (y 870–873) · v7 ilk: sensörün alt yüzünü kapatan sütun
    ekle("flap_katlayici_sensor_braketi", kut(709.0, 724.0, 832.0, 835.0, -310.0, -290.0).union(kut(709.0, 712.0, 835.0, 873.0, -310.0, -290.0))
         .union(kut(690.0, 712.0, 870.0, 873.0, -310.0, -290.0).cut(sily(700.0, -300.0, 4.02, 869.0, 874.0))), "aluminyum", bom=SENSOR_BRAKET_BOM)
    # KOL (kapağı kaldırır, yatırır): mil z boyunca KOL_P'de, redüktör + motor önde
    px, py = KOL_P
    kol = kut(px, px + KOL_R, py - 6.0, py + 6.0, KOL_Z[0], KOL_Z[1]).union(silz(px, py, 14.0, KOL_Z[0], KOL_Z[1]))
    kol = kol.union(silz(px + KOL_R, py, 10.0, KOL_Z[0] - 2.0, KOL_Z[1] + 2.0))
    ekle("kapak_kolu", kol, "celik", "KOL", bom=("Kapak kolu 304 + makara Ø20 (POM)", 1, "R 166 · kapağı 85° dik tutar, 100° yatırır", "üretim"))
    ekle("kapak_kolu_mili", silz(px, py, 6.0, ZB - 26.0, -150.0), "celik")
    for i, (z0, z1) in enumerate(((ZB - 30.0, ZB - 20.0), (-170.0, -160.0))):
        ekle("kol_yatagi_%d" % i, kut(px - 18.0, px + 18.0, py - 18.0, py + 18.0, z0, z1).cut(silz(px, py, 6.1, z0 - 1, z1 + 1)), "celik",
             bom=("Flanşlı yatak KFL001 (Ø12)", 2, "kol mili", "katalog") if i == 0 else None)
        ekle("kol_yatak_ayagi_%d" % i, kut(px - 18.0, px + 18.0, 832.0, py - 18.0, z0, z1), "aluminyum")
    pgcn23("kol_reduktoru", (px, py, -150.0), (0, 0, -1), (0, 1, 0))
    nema23("kol_motoru", (px, py, -71.0), (0, 0, -1), (0, 1, 0))
    ekle("kol_reduktor_braketi", kut(px - 30.0, px + 30.0, 832.0, py - 29.0, -150.0, -140.0), "aluminyum")
    ekle("kol_red_flans_plakasi", kut(px - 30.0, px + 30.0, 870.0, py + 30.0, -154.0, -150.0).cut(silz(px, py, 12.0, -155.0, -149.0)), "aluminyum")   # v7: redüktör çıkış flanşı bu plakaya, plaka brakete (v6: 0,42 mm değmiyordu)
    e2e("kol_sensor", px + 30.0, py - 40.0, ZB + 12.0, "z")
    # v7b: delikli sensör sacı (z −170…−167) + kol yatak ayağının yan yüzüne (x 578) 24 × 10 dik kol (v7 ilk: sensöre teğet blok)
    ekle("kol_sensor_braketi", kut(px + 18.0, px + 21.0, py - 52.0, py - 28.0, -170.0, -160.0).union(kut(px + 18.0, px + 40.0, py - 52.0, py - 28.0, -170.0, -167.0)
         .cut(silz(px + 30.0, py - 40.0, 4.02, -171.0, -166.0))), "aluminyum", bom=SENSOR_BRAKET_BOM)


# ---------------------------------------------------------------- ELEKTRİK ----------------------------------------------------------------
def elektrik():
    ekle("pano_plakasi", kut(60.0, 780.0, 1397.0, 1857.0, -826.0, -822.0), "sac")
    for i, (xb, yb) in enumerate(((80.0, 1417.0), (760.0, 1417.0), (80.0, 1837.0), (760.0, 1837.0))):   # v7: pano plakası arka saca 4 burçla (v6: 2,5 mm havada)
        ekle("pano_plakasi_burcu_%d" % i, silz(xb, yb, 6.0, -D + SAC, -826.0), "celik", bom=("Mesafe burcu M5 · Ø12 × 2,5 paslanmaz", 1, "pano plakası ↔ arka sac", "katalog"))
    for i, y in enumerate((1477.0, 1697.0)):                      # v5: − 168
        ekle("din_rayi_%d" % i, kut(70.0, 770.0, y, y + 35.0, -822.0, -815.0), "celik", bom=("DIN ray 35 × 7,5", 2, "boy 700", "EN 60715") if i == 0 else None)
    zd = -815.0
    ekle("plc_S7-1200_1214C", kut(80.0, 190.0, 1444.5, 1544.5, zd, zd + 75.0), "siemens",
         bom=("PLC Siemens S7-1200 CPU 1214C DC/DC/DC", 1, "6ES7214-1AG40-0XB0 · 4 PTO ekseni (7 sürücü enable ile paylaşır; aynı anda en çok 3 eksen döner)", "110 × 100 × 75"))
    ekle("plc_SM1221_DI16", kut(194.0, 239.0, 1444.5, 1544.5, zd, zd + 75.0), "siemens", bom=("Siemens SM1221 DI16", 1, "6ES7221-1BH32-0XB0", "45 × 100 × 75"))
    ekle("plc_SM1222_DQ16", kut(243.0, 288.0, 1444.5, 1544.5, zd, zd + 75.0), "siemens", bom=("Siemens SM1222 DQ16", 1, "6ES7222-1BH32-0XB0 · yön + enable", "45 × 100 × 75"))
    x = 300.0
    for i, (ad_, bom) in enumerate((("guc_24V_NDR-240-24", ("Güç kaynağı Mean Well NDR-240-24", 1, "24 V 10 A · PLC + sensör", "TraceParts STEP")),
                                    ("guc_48V_NDR-240-48_a", ("Güç kaynağı Mean Well NDR-240-48", 2, "48 V 5 A · step sürücüler", "NDR-240 gövdesi (STEP 24 V ile aynı)")),
                                    ("guc_48V_NDR-240-48_b", None))):
        ekle(ad_, TC.din_parca(TC.GUC_STEP, x, 1432.0, zd + 122.8 + 0.0).translate((0, 0, -0.0)), "aluminyum", bom=bom)
        x += 67.0
    x = 90.0
    for i in range(7):                                  # 7 eksen: asansör · itici · köprü · piston · parmak · flap · kol
        ekle("surucu_STP-DRV-4830_%d" % i, TC.din_parca(TC.SURUCU_STEP, x, 1687.0, zd + 28.0), "kart",
             bom=("Step sürücü AutomationDirect SureStep STP-DRV-4830", 7, "3 A/faz · 12–48 VDC · adım/yön", "automationdirect.com · TraceParts STEP") if i == 0 else None)
        x += 50.0
    ekle("klemens_sirasi", kut(450.0, 760.0, 1699.0, 1745.0, zd, zd + 45.0), "plastik", bom=("Klemens sırası Phoenix UT 2,5", 40, "", "phoenixcontact.com"))
    for i, (x0, x1, y0, y1) in enumerate(((70.0, 770.0, 1577.0, 1617.0), (70.0, 770.0, 1797.0, 1837.0))):
        ekle("kablo_kanali_%d" % i, kut(x0, x1, y0, y1, -822.0, -797.0), "plastik", bom=("Kablo kanalı 40 × 25", 2, "pano", "katalog") if i == 0 else None)
    ekle("kablo_kanali_dikey_alt", kut(806.0, 826.0, Y_PLINT + 3.0, 1157.0, -50.0, -25.0), "plastik",   # v3: tabandan başlar · v7: x 801 → 806 (sağ sütun kolisinin düz yolu serbest)
         bom=("Kablo kanalı 20 × 25 (dikey)", 2, "sağ ön köşe · x 806–826", "katalog ölçüsü VARSAYIM"))
    ekle("kablo_kanali_dikey_ust", kut(806.0, 826.0, 1177.0, 1827.0, -50.0, -25.0), "plastik")
    e3z("sensor_yigin_ustu", 770.0, 1022.0, -800.0)
    e3z("sensor_blank_var", 790.0, 1022.0, -216.0)
    e3z("sensor_kutu_dolu", SAC + 1.0, 1068.0, -250.0)
    # v7: 3 fotoselin braketi yoktu (havada) → üstlerinde lam, yan saca (mercek yüzleri açık kalır) · v7b: L — yan saca 27 × 20 dik kol (v7 ilk: 3 mm kenarla 1,5 saca)
    ekle("sensor_yigin_ustu_braketi", kut(770.0, W - SAC, 1053.0, 1056.0, -800.0, -780.0).union(kut(W - SAC - 3.0, W - SAC, 1056.0, 1080.0, -800.0, -780.0)), "aluminyum", bom=FOTOSEL_BRAKET_BOM)
    ekle("sensor_blank_var_braketi", kut(790.0, W - SAC, 1053.0, 1056.0, -216.0, -196.0).union(kut(W - SAC - 3.0, W - SAC, 1056.0, 1080.0, -216.0, -196.0)), "aluminyum", bom=FOTOSEL_BRAKET_BOM)
    ekle("sensor_kutu_dolu_braketi", kut(SAC, SAC + 11.8, 1099.0, 1102.0, -250.0, -230.0).union(kut(SAC, SAC + 3.0, 1102.0, 1130.0, -250.0, -230.0)), "aluminyum", bom=FOTOSEL_BRAKET_BOM)


# ---------------------------------------------------------------- İÇECEK YEDEĞİ (v5 · ALÇAK HAT) ----------------------------------------------------------------
# SPEC_alcak_hat_v57 · Resim 1 v4: E altı önde 6 koli (24 kutu) 2 sütun × 3 kat → dolaptaki 144 + 144 = 288 (4 gün 277).
# v6 gerekçesi: ön köşe dikmeleri (z −21,5…−1,5) ve kablo_kanali_dikey_alt (x 801–826 · z −50…−25) önde olduğu için koliler geride: z −350…−83.
# v7: ön köşe dikmeleri KALKTI, dikey kanal x 806–826; koli yeri AYNI (kayıtlı ölçü) — önünde ALT kanatlar (kapak açıkken koli yolu serbest, olcum_v7).
# Arkada ilk engel asansör ray plakası (z −374); üstte alt raf köşebentleri (alt yüz 588); 4. kat sığmaz (130 + 4 × 123 = 622 > 588).
KOLI = dict(x=400.0, y=123.0, z=267.0, kutu=24)          # koli 400 × 267 × 123 · 24 kutu [VARSAYIM: ölçü resimden, üretici kolisi teyit edilmedi]
ICECEK_X = ((3.0, 403.0), (405.0, 805.0))               # 2 sütun (aralarında 2 mm)
ICECEK_Y0, ICECEK_KAT = 130.0, 3                         # koli tabanı 130 (altlık 126–130) · 3 kat → üst 499
ICECEK_Z = (-350.0, -83.0)
ICECEK_ALTLIK_Y = (Y_PLINT + 3.0, ICECEK_Y0)             # PE-HD altlık 4 mm (taban sacı üstü 126 → koli 130) [VARSAYIM]
ICECEK_YEDEK = dict(x=(ICECEK_X[0][0], ICECEK_X[-1][1]), y=(ICECEK_Y0, ICECEK_Y0 + ICECEK_KAT * KOLI["y"]), z=ICECEK_Z,
                    koli=len(ICECEK_X) * ICECEK_KAT, kutu=len(ICECEK_X) * ICECEK_KAT * KOLI["kutu"])   # montaj için özet (E yereli)
V6_CIKAN = ("on_alt_sac",)                              # v6: v5'ten çıkan parça — ön taraflara kapak yok (Kemal 27 Eyl gece)


def icecek_yedegi():
    """v5: içecek yedeği — soğutmasız, önde · E_SARJOR'un önü, alt rafın altı · v6: önü AÇIK (ön alt sac kalktı) ·
    v7: önünde ALT tava kanatlar (2 × 413 · ≥ 110°); kapak açıkken koli önü → ön düzlem (+79) yolu SERBEST (olcum_v7)"""
    ekle("icecek_yedek_altligi", kut(ICECEK_X[0][0], ICECEK_X[-1][1], ICECEK_ALTLIK_Y[0], ICECEK_ALTLIK_Y[1], ICECEK_Z[0], ICECEK_Z[1]), "plastik",
         bom=("Koli altlığı PE-HD 4 mm (içecek yedeği)", 1, "%.0f × %.0f" % (ICECEK_X[-1][1] - ICECEK_X[0][0], ICECEK_Z[1] - ICECEK_Z[0]), "VARSAYIM · levha kesim"))
    for s_, (x0, x1) in enumerate(ICECEK_X):
        for k_ in range(ICECEK_KAT):
            y0 = ICECEK_Y0 + k_ * KOLI["y"]
            ekle("icecek_yedek_koli_%d%d" % (s_, k_), kut(x0, x1, y0, y0 + KOLI["y"], ICECEK_Z[0], ICECEK_Z[1]), "karton",
                 bom=("İçecek kolisi 24 kutu (yedek, soğutmasız)", ICECEK_YEDEK["koli"], "400 × 267 × 123 · %d kutu" % ICECEK_YEDEK["kutu"],
                      "sarf · koli ölçüsü VARSAYIM (resim)") if s_ == 0 and k_ == 0 else None)


# ---------------------------------------------------------------- BLANK (hareketli kutu ağacı) ----------------------------------------------------------------
def panel(x0, x1, z0, z1, kes=None):
    p = kut(x0, x1, YB, YB + T, z0, z1)
    for c in (kes or []):
        p = p.cut(c)
    return p


def blank():
    """kutuyu KATLAMA YERİNDE, düz halde kurar; her panel kendi menteşe düğümüne bağlı (DUGUM)"""
    yarik = [kut(BX0 + T - 0.1, BX0 + 2 * T + 0.3, YB - 1, YB + T + 1, z0 - 1.0, z1 + 1.0) for z0, z1 in DIL_Z]
    ekle("B_TABAN", panel(BX0, BX1, BZ0, BZ1, yarik), "karton", "B_ROOT")
    ekle("B_YAN_ARKA", panel(BX0 + T, BX1 - T, Z_BL0, BZ0), "karton", "B_SWM")
    ekle("B_YAN_ON", panel(BX0 + T, BX1 - T, BZ1, Z_BL1), "karton", "B_SWP")
    ekle("B_TIRNAK_ARKA_ON", panel(BX0 + T - KT_L, BX0 + T - 0.3, BZ0 - KT_H - 1.0, BZ0 - 1.0), "karton", "B_CTMF")
    ekle("B_TIRNAK_ARKA_MENTESE", panel(BX1 - T + 0.3, BX1 - T + KT_L, BZ0 - KT_H - 1.0, BZ0 - 1.0), "karton", "B_CTMB")
    ekle("B_TIRNAK_ON_ON", panel(BX0 + T - KT_L, BX0 + T - 0.3, BZ1 + 1.0, BZ1 + KT_H + 1.0), "karton", "B_CTPF")
    ekle("B_TIRNAK_ON_MENTESE", panel(BX1 - T + 0.3, BX1 - T + KT_L, BZ1 + 1.0, BZ1 + KT_H + 1.0), "karton", "B_CTPB")
    ekle("B_ON_DIS", panel(BX0 - H_ON, BX0, BZ0, BZ1), "karton", "B_FO")
    ic = panel(BX0 - H_ON - H_IC, BX0 - H_ON - 0.2, BZ0 + 2.0, BZ1 - 2.0)
    for z0, z1 in DIL_Z:
        ic = ic.union(panel(X_BL0, BX0 - H_ON - H_IC + 0.1, z0, z1))
    ekle("B_ON_IC_KILITLI", ic, "karton", "B_FI")
    ekle("B_ARKA_MENTESE", panel(BX1, BX1 + H_ARKA, BZ0, BZ1), "karton", "B_BW")
    xk0 = BX1 + H_ARKA
    ekle("B_KAPAK", panel(xk0 + 0.2, xk0 + L_KAP, ZL0, ZL1), "karton", "B_LID")
    ekle("B_KAPAK_ON_FLAP", panel(xk0 + L_KAP + 0.2, X_BL1, ZL0 + 3.0, ZL1 - 3.0), "karton", "B_LF")
    ekle("B_KAPAK_YAN_ARKA", panel(xk0 + 40.0, xk0 + L_KAP - 4.0, ZL0 - H_KF, ZL0 - 0.2), "karton", "B_LSM")
    ekle("B_KAPAK_YAN_ON", panel(xk0 + 40.0, xk0 + L_KAP - 4.0, ZL1 + 0.2, ZL1 + H_KF), "karton", "B_LSP")


# DÜĞÜMLER: ad -> (ebeveyn, menteşe noktası (dünya, düz blank), eksen)
DUGUM = {
    "B_ROOT": (None, (0.0, 0.0, 0.0), None),
    "B_SWM": ("B_ROOT", (0.0, YB + T, BZ0), "x"),
    "B_SWP": ("B_ROOT", (0.0, YB + T, BZ1), "x"),
    "B_CTMF": ("B_SWM", (BX0 + T, YB + T, 0.0), "z"),
    "B_CTMB": ("B_SWM", (BX1 - T, YB + T, 0.0), "z"),
    "B_CTPF": ("B_SWP", (BX0 + T, YB + T, 0.0), "z"),
    "B_CTPB": ("B_SWP", (BX1 - T, YB + T, 0.0), "z"),
    "B_FO": ("B_ROOT", (BX0, YB + T, 0.0), "z"),
    "B_FI": ("B_FO", (BX0 - H_ON, YB + 1.5 * T, 0.0), "z"),
    "B_BW": ("B_ROOT", (BX1, YB + T / 2.0, 0.0), "z"),
    "B_LID": ("B_BW", (BX1 + H_ARKA, YB + T / 2.0, 0.0), "z"),
    "B_LF": ("B_LID", (BX1 + H_ARKA + L_KAP, YB + T, 0.0), "z"),
    "B_LSM": ("B_LID", (0.0, YB + T, ZL0), "x"),
    "B_LSP": ("B_LID", (0.0, YB + T, ZL1), "x"),
}


# ---------------------------------------------------------------- ROBOT ÇATALI · PİZZA · K REFERANSI ----------------------------------------------------------------
CATAL_DIS = 700.0


def catal_pizza():
    for i, (x0, x1) in enumerate(X_CATAL):
        ekle("robot_catal_disi_%d" % i, kut(x0, x1, 926.0, 934.0, BZ0 + 2.0 + CATAL_DIS, 60.0 + CATAL_DIS), "robot", "CATAL")
    ekle("robot_catal_govdesi", kut(140.0, 380.0, 912.0, 944.0, 60.0 + CATAL_DIS, 76.0 + CATAL_DIS), "robot", "CATAL",
         bom=("[R modülü] FR5 kutu çatalı — robot aletidir, E'ye dahil değil", 0, "3 diş 26 × 8 × 430", "robot"))
    ekle("robot_flansi", silz(260.0, 928.0, 31.5, 76.0 + CATAL_DIS, 96.0 + CATAL_DIS), "robot", "CATAL")
    # pizza (K plakasının üstünde bekler): Ø300 hamur + Ø284 sos/peynir
    ekle("pizza_hamur", sily(-300.0, -170.0, 150.0, PLAKA_K, PLAKA_K + 10.0), "hamur", "PIZZA")
    ekle("pizza_ustu", sily(-300.0, -170.0, 142.0, PLAKA_K + 10.0, PLAKA_K + 15.0), "sos", "PIZZA")
    # K modülü referansı (saydam): plakanın ucu + itici
    ekle("REF_K_kesme_plakasi_ucu", kut(-320.0, -20.0, PLAKA_K - 14.0, PLAKA_K, -470.0, -20.0), "referans", "SABIT_REF")
    ekle("REF_K_itici", kut(-490.0, -450.0, PLAKA_K + 2.0, PLAKA_K + 50.0, -320.0, -20.0), "referans", "K_ITICI")


# ---------------------------------------------------------------- KİNEMATİK (tek kaynak: GLB animasyonu + çakışma taraması) ----------------------------------------------------------------
DONGU = 20.0
# ZAMAN ÇİZELGESİ (sn) — her satır bir hareket; GLB ve çakışma taraması AYNI fonksiyonları çağırır
Z_BESLE = (0.5, 1.7)          # itici blankı şarjörden kalıba sürer
Z_ITICI_DON = (1.8, 2.8)
Z_INIS = (1.9, 2.7)           # kafa blankın üstüne iner
Z_ZIMBA = (2.7, 3.3)          # taban 45,6 mm kalıba girer, duvarlar kalkar
Z_KALK1 = (3.3, 4.0)          # kafa yukarı (parmağa yer)
Z_PARMAK = (4.0, 4.5, 5.0)    # parmak iner / döner
Z_VURUS2 = (5.0, 5.6, 5.7, 6.4)   # 2. vuruş: in, bekle, çık
Z_KOPRU = (5.8, 6.2, 18.3, 18.7)
Z_FLAP = (6.4, 6.8, 7.4, 7.8)     # U çerçeve kalkar / iner
Z_KOL = (6.8, 7.15, 8.1)          # kol temas, kapak 85°
Z_PIZZA = (8.5, 10.1, 10.35)      # K itici sürer, pizza düşer
Z_KITICI_DON = (10.3, 11.3)
Z_KAFA_HAZIR = (10.6, 10.9)       # kafa dik kapağın üstüne (H_BEKLE)
Z_YATIR = (10.9, 11.2)            # kol kapağı 100°'ye yatırır
Z_KAPAT = (11.2, 12.6, 12.9, 13.7)    # kafa kapağı kapatır, bastırır, çıkar
Z_KOL_DON = (11.25, 12.2)
Z_CATAL = (13.9, 15.1, 15.6, 17.3)    # robot çatalı gelir, kaldırır, çeker
Z_GIZLE = (19.6, 19.98)
KAPAK_BASKI = KMER[1] + T / 2.0 + 0.2          # kapak kapalıyken üst yüzü
H_BEKLE = 1299.0                 # dik kapak 85°'de: ön flap ucu 1296,3 · v5: 1467 − 168
Y_VURUS2 = TEPSI + 4.0           # v5: 2. vuruşta kafa alt yüzü = 940 (v4'te kafa() içinde sabit 1108,0 = TEPSI 1104 + 4 yazılıydı)


def ss(a, b, t):
    if t <= a: return 0.0
    if t >= b: return 1.0
    x = (t - a) / (b - a); return x * x * (3.0 - 2.0 * x)


def lin(a, b, t):
    if t <= a: return 0.0
    if t >= b: return 1.0
    return (t - a) / (b - a)


def kafa(t):
    """piston kafası alt yüzü (y)"""
    if t < Z_INIS[0]: return H_UST
    if t < Z_INIS[1]: return H_UST + (YB + T - H_UST) * ss(Z_INIS[0], Z_INIS[1], t)
    if t < Z_ZIMBA[1]: return (YB + T) + (TEPSI + T - (YB + T)) * lin(Z_ZIMBA[0], Z_ZIMBA[1], t)
    if t < Z_KALK1[1]: return (TEPSI + T) + (H_UST - (TEPSI + T)) * ss(Z_KALK1[0], Z_KALK1[1], t)
    if t < Z_VURUS2[0]: return H_UST
    if t < Z_VURUS2[1]: return H_UST + (Y_VURUS2 - H_UST) * ss(Z_VURUS2[0], Z_VURUS2[1], t)
    if t < Z_VURUS2[2]: return Y_VURUS2
    if t < Z_VURUS2[3]: return Y_VURUS2 + (H_UST - Y_VURUS2) * ss(Z_VURUS2[2], Z_VURUS2[3], t)
    if t < Z_KAFA_HAZIR[0]: return H_UST
    if t < Z_KAFA_HAZIR[1]: return H_UST + (H_BEKLE - H_UST) * ss(Z_KAFA_HAZIR[0], Z_KAFA_HAZIR[1], t)
    if t < Z_KAPAT[0]: return H_BEKLE
    if t < Z_KAPAT[1]: return H_BEKLE + (KAPAK_BASKI - H_BEKLE) * ss(Z_KAPAT[0], Z_KAPAT[1], t)
    if t < Z_KAPAT[2]: return KAPAK_BASKI
    if t < Z_KAPAT[3]: return KAPAK_BASKI + (H_UST - KAPAK_BASKI) * ss(Z_KAPAT[2], Z_KAPAT[3], t)
    return H_UST


def u_zimba(t):
    """tabanın kalıba giriş derinliği (kafa kalksa da kutu aşağıda kalır)"""
    if t < Z_ZIMBA[0]: return 0.0
    if t < Z_ZIMBA[1]: return U_MAX * lin(Z_ZIMBA[0], Z_ZIMBA[1], t)
    return U_MAX


def parmak_psi(t):
    """parmak açısı (+z etrafında, derece): 0 = dik yukarı, −140 = kutunun içine eğik"""
    return -140.0 * (ss(Z_PARMAK[0], Z_PARMAK[1], t) - ss(Z_PARMAK[1], Z_PARMAK[2], t))


def kapak_acisi_kafa(h):
    s = (h - (KMER[1] + T / 2.0 + 1.5)) / L_KAP             # 1,5: kapak ucu + flap kökü kafanın altında kalsın
    s = max(-1.0, min(1.0, s))
    return 180.0 - math.degrees(math.asin(s))


def kol_icin_beta(alfa):
    """kapak açısı alfa (derece, düz +x = 0) için kol açısı: makara kapağın dış yüzüne değer"""
    a = math.radians(alfa); hx, hy = KMER
    def f(b):
        cx = KOL_P[0] + KOL_R * math.cos(b); cy = KOL_P[1] + KOL_R * math.sin(b)
        return math.sin(a) * (cx - hx) - math.cos(a) * (cy - hy) - (10.0 + T / 2.0)
    lo, hi = 0.0, math.radians(175.0)
    flo = f(lo)
    for _ in range(80):
        mid = (lo + hi) / 2.0; fm = f(mid)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return math.degrees((lo + hi) / 2.0)


BETA_TEMAS = kol_icin_beta(0.0)
BETA_100 = kol_icin_beta(100.0)


def kapak_alfa(t):
    """kapağın dünya açısı: 0 = masada düz (+x), 90 = dik, 180 = kapalı"""
    if t < Z_KOL[1]: return 0.0
    if t < Z_KOL[2]: return 85.0 * ss(Z_KOL[1], Z_KOL[2], t)
    if t < Z_YATIR[0]: return 85.0
    if t < Z_YATIR[1]: return 85.0 + 15.0 * ss(Z_YATIR[0], Z_YATIR[1], t)
    if t < Z_KAPAT[1] + 0.05: return min(180.0, max(100.0, kapak_acisi_kafa(kafa(t))))
    return 180.0


def kol_beta(t):
    if t < Z_KOL[0]: return 0.0
    if t < Z_KOL[1]: return BETA_TEMAS * ss(Z_KOL[0], Z_KOL[1], t)
    if t < Z_YATIR[1]: return kol_icin_beta(kapak_alfa(t))
    return BETA_100 * (1.0 - ss(Z_KOL_DON[0], Z_KOL_DON[1], t))


def katlayici_dy(t):
    return UC_KALK * (ss(Z_FLAP[0], Z_FLAP[1], t) - ss(Z_FLAP[2], Z_FLAP[3], t))


def kopru_dy(t):
    return KOPRU_ALT * (ss(Z_KOPRU[0], Z_KOPRU[1], t) - ss(Z_KOPRU[2], Z_KOPRU[3], t))


def itici_dz(t):
    return BESLE * (ss(Z_BESLE[0], Z_BESLE[1], t) - ss(Z_ITICI_DON[0], Z_ITICI_DON[1], t))


def catal_trs(t):
    """çatal dinlenmede ağzın 700 mm önünde (koridorda)"""
    dz = -CATAL_DIS * ss(Z_CATAL[0], Z_CATAL[1], t) + 900.0 * ss(Z_CATAL[2], Z_CATAL[3], t)
    dy = 55.0 * ss(Z_CATAL[1], Z_CATAL[2], t)
    return (0.0, dy, dz)


def catal_kutu(t):
    """kutunun çatalla birlikte ötelenmesi (kaldırma anından itibaren)"""
    if t < Z_CATAL[1]: return (0.0, 0.0)
    c = catal_trs(t)
    return (c[1], c[2] + CATAL_DIS)


PIZZA_X0, PIZZA_Z0 = -300.0, -170.0


def pizza_trs(t):
    """K itici (2 eksen) pizzayı K plakasının üstünde 36 mm içeri kaydırır (z −170 → −206), sonra düz iter.
    Kayma pizzanın ön kenarı E'ye girmeden BİTER (x −300 → −160): köşe plow'ları ve pencere kenarı pizzanın yolunda kalmaz
    (düz 3,1° çapraz itişte pizza +z plow'una 2,6 mm, pencereye 2 mm değiyordu — pizza taraması)."""
    k = ss(Z_PIZZA[0], Z_PIZZA[1], t)
    x = PIZZA_X0 + (260.0 - PIZZA_X0) * k
    z = PIZZA_Z0 + (ZB - PIZZA_Z0) * ss(0.0, 0.25, k)
    if x <= -20.0: y = PLAKA_K
    elif x <= 40.0: y = PLAKA_K + (KALIP - PLAKA_K) * (x + 20.0) / 60.0
    else: y = KALIP
    y = y + (TEPSI + T - KALIP) * ss(Z_PIZZA[1], Z_PIZZA[2], t)
    dy_c, dz_c = catal_kutu(t)
    return (x - PIZZA_X0, y - PLAKA_K + dy_c, z - PIZZA_Z0 + dz_c)


def k_itici_trs(t):
    """K iticisinin referans hareketi: pizzayı arkasından iter (x) ve onunla birlikte 36 mm içeri kayar (z)"""
    k = ss(Z_PIZZA[0], Z_PIZZA[1], t)
    x_arka = (PIZZA_X0 + (260.0 - PIZZA_X0) * k) - 150.0          # pizzanın arka kenarı
    dz = (ZB - PIZZA_Z0) * ss(0.0, 0.25, k)
    if t <= Z_PIZZA[1]: return (max(0.0, x_arka - (-450.0)), 0.0, dz)
    geri = 1.0 - ss(Z_KITICI_DON[0], Z_KITICI_DON[1], t)
    return ((260.0 - 150.0 + 450.0) * geri, 0.0, (ZB - PIZZA_Z0) * geri)


def _kose_ustu(dy, d):
    """panel, kıvrımının (menteşe = panelin ÜST yüz kenarı) d mm dışındaki ve dy mm yukarısındaki bir köşenin
    ÜSTÜNDEN dönerek kalkar. Panelin ALT yüzü köşeye değer (kalınlık T): köşe, üst yüz çizgisinin T altında kalmalı →
    d·sinθ − dy·cosθ ≥ T  →  θ = φ + asin(T/r),  φ = atan2(dy, d), r = √(dy² + d²)"""
    r = math.hypot(dy, d)
    if r <= T:
        return 0.0
    th = math.degrees(math.atan2(dy, d) + math.asin(T / r))
    return max(0.0, min(90.0, th))


def _ray_uzeri(u, y_kose, d):
    """kalıp rayının iç üst köşesi (y_kose, kıvrımdan d mm dışarıda); kıvrım y = YB + T − u"""
    return _kose_ustu(y_kose - (YB + T - u), d)


def blank_acilar(t):
    """(kök öteleme, {düğüm: açı derece}) — açılar kalıp geometrisinden (el ile yazılmış eğri değil)"""
    u = u_zimba(t)
    dz = -BESLE * (1.0 - ss(Z_BESLE[0], Z_BESLE[1], t))
    dy = -u
    dy_c, dz_c = catal_kutu(t)
    dy += dy_c; dz += dz_c
    # yan duvarlar: arka ray / ön tarak iç üst köşesi (KALIP; kıvrımdan 2,1 mm dışarıda); sonda duvar raya yaslanır (90°)
    th_s = max(_ray_uzeri(u, KALIP, 2.1), 90.0 * ss(U_MAX - 4.0, U_MAX, u))
    # köşe tırnakları: yan duvar 30°'yi geçince içe döner (kalıp köşesi), yan duvar 80°'de bitmiş olur
    th_t = 90.0 * ss(30.0, 80.0, th_s)
    # ön dış duvar: ön ray 20 mm alçak (KALIP − 20; v4 1129,5 sabitti) → tırnaklardan SONRA kalkar; kilitlenince 90°
    th_f = _ray_uzeri(u, KALIP - 20.0, 2.1)
    if t >= Z_VURUS2[0]:
        th_f = th_f + (90.0 - th_f) * ss(Z_VURUS2[0], Z_VURUS2[1], t)
    th_bw = math.degrees(math.asin(min(u, H_ARKA - 0.001) / H_ARKA)) if u < H_ARKA else 90.0
    # iç ön panel: parmak iter (0 → −70), yerçekimiyle içeri düşer ve kilit dilleri TABANA dayanır (−145),
    # 2. vuruşta kafa paneli dikleştirir, diller yarıklardan tepsinin cebine iner (−180)
    if t < Z_PARMAK[0] + 0.12: fi = 0.0
    elif t < Z_PARMAK[1]: fi = -70.0 * ss(Z_PARMAK[0] + 0.12, Z_PARMAK[1], t)
    elif t < Z_PARMAK[1] + 0.35: fi = -70.0 - 75.0 * ss(Z_PARMAK[1], Z_PARMAK[1] + 0.35, t)
    elif t < Z_VURUS2[0] + 0.3: fi = -145.0
    else: fi = -145.0 - 35.0 * ss(Z_VURUS2[0] + 0.3, Z_VURUS2[1], t)
    alfa = kapak_alfa(t)
    gam = alfa - th_bw
    # kapak flapları: U çerçevenin kolu kırımın 1,6 mm dışında kalkar → flap kolun iç üst köşesinden döner
    if t < Z_FLAP[1]:
        th_fl = _kose_ustu(KM_UST + katlayici_dy(t) - (KM_UST + T), T)      # kolun iç üst köşesi kırımdan 1,6 dışarıda
    else:
        th_fl = 90.0
    A = {"B_SWM": th_s, "B_SWP": -th_s, "B_CTMF": -th_t, "B_CTMB": th_t, "B_CTPF": -th_t, "B_CTPB": th_t,
         "B_FO": -th_f, "B_FI": fi, "B_BW": th_bw, "B_LID": gam, "B_LF": th_fl, "B_LSM": th_fl, "B_LSP": -th_fl}
    return (0.0, dy, dz), A


def gorunur(t):
    """kutu + pizza robotla çıktıktan sonra döngü başına dönerken gizlenir"""
    return 0.0 if Z_GIZLE[0] <= t < Z_GIZLE[1] else 1.0


# ---------------------------------------------------------------- 4x4 MATRİS ----------------------------------------------------------------
def mm4(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def tr4(v):
    return [[1, 0, 0, v[0]], [0, 1, 0, v[1]], [0, 0, 1, v[2]], [0, 0, 0, 1]]


def rot4(eksen, derece):
    a = math.radians(derece); c, s = math.cos(a), math.sin(a)
    if eksen == "x": return [[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]]
    if eksen == "y": return [[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]]
    return [[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]


def quat(eksen, derece):
    a = math.radians(derece) / 2.0; s = math.sin(a)
    v = {"x": (s, 0.0, 0.0), "y": (0.0, s, 0.0), "z": (0.0, 0.0, s)}[eksen]
    return (v[0], v[1], v[2], math.cos(a))


def grup_matrisi(grup, t):
    """makine grubunun dünya dönüşümü (dinlenme konumundaki katıya uygulanır)"""
    if grup == "ITICI": return tr4((0.0, 0.0, itici_dz(t)))
    if grup == "PISTON": return tr4((0.0, kafa(t) - H_UST, 0.0))
    if grup == "KOPRU": return tr4((0.0, kopru_dy(t), 0.0))
    if grup == "KATLAYICI": return tr4((0.0, katlayici_dy(t), 0.0))
    if grup == "KOL": return mm4(mm4(tr4((KOL_P[0], KOL_P[1], 0.0)), rot4("z", kol_beta(t))), tr4((-KOL_P[0], -KOL_P[1], 0.0)))
    if grup == "PARMAK": return mm4(mm4(tr4((PARMAK_P[0], PARMAK_P[1], 0.0)), rot4("z", parmak_psi(t))), tr4((-PARMAK_P[0], -PARMAK_P[1], 0.0)))
    if grup == "CATAL": return tr4(catal_trs(t))
    if grup == "PIZZA": return tr4(pizza_trs(t))
    if grup == "K_ITICI": return tr4(k_itici_trs(t))
    return tr4((0.0, 0.0, 0.0))


def blank_dunya(t):
    """her blank düğümünün dünya matrisi × T(−menteşe): dinlenme katısına uygulanacak dönüşüm"""
    kok, A = blank_acilar(t)
    W = {}
    sira = ["B_ROOT", "B_SWM", "B_SWP", "B_FO", "B_BW", "B_CTMF", "B_CTMB", "B_CTPF", "B_CTPB", "B_FI", "B_LID", "B_LF", "B_LSM", "B_LSP"]
    for d in sira:
        par, P, eks = DUGUM[d]
        if par is None:
            W[d] = tr4(kok)
            continue
        Pp = DUGUM[par][1] if DUGUM[par][0] is not None else (0.0, 0.0, 0.0)
        lok = mm4(tr4((P[0] - Pp[0], P[1] - Pp[1], P[2] - Pp[2])), rot4(eks, A[d]))
        W[d] = mm4(W[par], lok)
    return {d: mm4(W[d], tr4((-DUGUM[d][1][0], -DUGUM[d][1][1], -DUGUM[d][1][2]))) for d in W}


def uygula(sh, M):
    return tasi(sh, M)


# ---------------------------------------------------------------- DENETİM ----------------------------------------------------------------
HAREKETLI = ("ITICI", "PISTON", "KOPRU", "KATLAYICI", "KOL", "PARMAK", "ASANSOR")
KONTROL_ANLARI = tuple(round(0.1 * i, 2) for i in range(201))          # her 0,1 sn
GECIS_ANLARI = (0.6, 0.9, 1.2, 1.5, 2.75, 2.8, 2.9, 3.0, 3.1, 3.2, 4.2, 4.35, 4.5, 4.65, 4.8, 5.3, 5.5, 6.5, 6.6, 6.7,
                7.3, 7.5, 7.7, 7.9, 10.95, 11.05, 11.15, 11.3, 11.5, 11.7, 11.9, 12.1, 12.3, 12.5, 15.2, 15.4, 15.8, 16.2, 16.6, 17.0)
PIZZA_ANLARI = tuple(round(8.5 + 0.1 * i, 2) for i in range(20)) + (12.8, 15.4, 15.8, 16.4, 17.0)
KUTU_ANLARI = (1.7, 4.0, 7.0, 8.1, 12.6, 15.6)          # kutunun durağan anları: düz · katlı · flaplar · dik kapak · kapalı · çatalda


def _bb_kesisir(A, B, pay=0.05):
    return not (A.xmin >= B.xmax - pay or B.xmin >= A.xmax - pay or A.ymin >= B.ymax - pay or B.ymin >= A.ymax - pay or A.zmin >= B.zmax - pay or B.zmin >= A.zmax - pay)


# tasarım gereği değen/kesişen çiftler (sebebiyle): bunlar sayılmaz
ISTISNA = [
    ("_rayi_", "_arabasi_"),                   # HIWIN araba ray üstünde (STEP'te boşluklu; güvenlik için)
    ("_vidasi_mil", "_vidasi_somun"),
    ("_vidasi_mil", "_BK12"), ("_vidasi_mil", "_BF12"),
    ("asansor_vidasi", "asansor_somunu"), ("asansor_vidasi", "asansor_alt_yatak"), ("asansor_vidasi", "asansor_ust_yatak"), ("asansor_vidasi", "asansor_kasnak"),
    ("_kasnak_", "_kayisi"), ("_kasnak_", "_motoru"), ("_kasnak_", "_vidasi_mil"),
    # v7b: ("_kaplini", "_motoru" | "_vidasi_mil" | "_BK12") istisnaları KALKTI — kaplin delikli, hiçbir parçaya binmiyor (olcum_v7 ölçer)
    ("kapak_kolu_mili", "kapak_kolu"), ("kapak_kolu_mili", "kol_yatagi"), ("kapak_kolu_mili", "kol_reduktoru"),
    ("parmak_mili", "devirme_parmagi"), ("parmak_mili", "parmak_yatagi"), ("parmak_mili", "parmak_reduktoru"),
    ("_reduktoru", "_motoru"),
    ("kopru_kilavuz_mili", "kopru_burcu"), ("kopru_kilavuz_mili", "kopru_burc_plakasi"),
    ("kapak_masasi_diregi", "kapak_masasi"), ("kapak_masasi_diregi", "kapak_alt_plakasi"),
    ("ayak_", "taban_sac"),
    ("motor_plakasi", "_motoru"), ("motor_plakasi", "taban_sac"), ("kayis_koruyucu", "taban_sac"),   # v3: cıvatalı yüzey temasları
    ("avara_yatagi", "avara_mili"), ("_kasnak_", "avara_mili"),
]


def _istisna(a, b):
    for p, q in ISTISNA:
        if (p in a and q in b) or (p in b and q in a):
            return True
    return False


_SABIT_ONBELLEK = []


def _katilar(t, gruplar=None):
    """t anında makine parçaları (blank ve pizza hariç) dünya konumunda · sabitler bir kez hesaplanır"""
    if not _SABIT_ONBELLEK:
        for p in PARCALAR:
            if p["grup"] == "SABIT":
                sh = p["wp"].val(); _SABIT_ONBELLEK.append((p, sh, sh.BoundingBox()))
    L = list(_SABIT_ONBELLEK)
    for p in PARCALAR:
        g = p["grup"]
        if g.startswith("B_") or g in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF", "SABIT"):
            continue
        if gruplar and g not in gruplar:
            continue
        sh = uygula(p["wp"].val(), grup_matrisi(g, t))
        L.append((p, sh, sh.BoundingBox()))
    return L


def cakisma(esik=1.0):
    t0 = time.time()
    sabit = [(p, p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT"]
    sabit = [(p, v, v.BoundingBox()) for p, v in sabit]
    bul = {}
    # 1) sabit parçalar kendi aralarında
    for i, (p, a, A) in enumerate(sabit):
        for q, b, Bb in sabit[i + 1:]:
            if not _bb_kesisir(A, Bb) or _istisna(p["ad"], q["ad"]):
                continue
            v = a.intersect(b).Volume()
            if v > esik:
                bul[(p["ad"], q["ad"])] = (v, "sabit")
    # 2) her kontrol anında hareketliler × (sabit + hareketli)
    for t in KONTROL_ANLARI:
        H_ = []
        for p in PARCALAR:
            g = p["grup"]
            if g in HAREKETLI or g == "CATAL":
                sh = uygula(p["wp"].val(), grup_matrisi(g, t))
                H_.append((p, sh, sh.BoundingBox()))
        hepsi = H_ + sabit
        for i, (p, a, A) in enumerate(H_):
            for q, b, Bb in hepsi[i + 1:]:
                if q is p or (q["grup"] == p["grup"]) or not _bb_kesisir(A, Bb) or _istisna(p["ad"], q["ad"]):
                    continue
                v = a.intersect(b).Volume()
                if v > esik and (p["ad"], q["ad"]) not in bul:
                    bul[(p["ad"], q["ad"])] = (v, "t=%.2f" % t)
    print("CAKISMA TARAMASI (makine): %d parca · %d an · %d cakisma (> %.0f mm3) · %.0f sn" % (len(PARCALAR), len(KONTROL_ANLARI), len(bul), esik, time.time() - t0))
    for (a, b), (v, an) in sorted(bul.items(), key=lambda kv: -kv[1][0])[:200]:
        print("    %10.1f mm3  %-8s %s <-> %s" % (v, an, a, b))
    return bul


def kutu_cakisma(esik=1.0, anlar=None, etiket="duragan"):
    """kutunun durağan anlarında karton × makine (+ pizza)"""
    t0 = time.time()
    bul = {}
    anlar = anlar or KUTU_ANLARI
    for t in anlar:
        W_ = blank_dunya(t)
        kart = [(p, uygula(p["wp"].val(), W_[p["grup"]])) for p in PARCALAR if p["grup"].startswith("B_")]
        kart = [(p, v, v.BoundingBox()) for p, v in kart]
        mak = _katilar(t)
        for p in PARCALAR:
            if p["grup"] in ("PIZZA", "CATAL"):
                sh = uygula(p["wp"].val(), grup_matrisi(p["grup"], t)); mak.append((p, sh, sh.BoundingBox()))
        for p, a, A in kart:
            for q, b, Bb in mak:
                if not _bb_kesisir(A, Bb):
                    continue
                v = a.intersect(b).Volume()
                if v > esik:
                    bul[(p["ad"], q["ad"], t)] = v
    print("CAKISMA TARAMASI (kutu x makine, %s): %d an · %d cakisma · %.0f sn" % (etiket, len(anlar), len(bul), time.time() - t0))
    for (a, b, t), v in sorted(bul.items(), key=lambda kv: -kv[1])[:40]:
        print("    %10.1f mm3  t=%.2f  %s <-> %s" % (v, t, a, b))
    return bul


def pizza_cakisma(esik=1.0):
    """pizza K plakasından kutuya kayarken ve robotla çıkarken: pizza × makine ve pizza × karton"""
    t0 = time.time(); bul = {}
    pz = [p for p in PARCALAR if p["grup"] == "PIZZA"]
    for t in PIZZA_ANLARI:
        Pz = [(p, uygula(p["wp"].val(), grup_matrisi("PIZZA", t))) for p in pz]
        W_ = blank_dunya(t)
        diger = _katilar(t) + [(q, uygula(q["wp"].val(), W_[q["grup"]]), None) for q in PARCALAR if q["grup"].startswith("B_")]
        diger = [(q, b_, bb_ or b_.BoundingBox()) for q, b_, bb_ in diger]
        for q in PARCALAR:
            if q["grup"] in ("CATAL", "K_ITICI"):
                sh = uygula(q["wp"].val(), grup_matrisi(q["grup"], t)); diger.append((q, sh, None))
        for p, a in Pz:
            A = a.BoundingBox()
            for q, b, Bb in diger:
                if q["ad"] == "REF_K_itici" or (q["grup"] == "SABIT_REF"):
                    continue
                if not _bb_kesisir(A, Bb or b.BoundingBox()):
                    continue
                v = a.intersect(b).Volume()
                if v > esik:
                    bul[(p["ad"], q["ad"], t)] = v
    print("CAKISMA TARAMASI (pizza): %d an · %d cakisma · %.0f sn" % (len(PIZZA_ANLARI), len(bul), time.time() - t0))
    for (a, b, t), v in sorted(bul.items(), key=lambda kv: -kv[1])[:40]:
        print("    %10.1f mm3  t=%.2f  %s <-> %s" % (v, t, a, b))
    return bul


def olcum():
    """tasarım iddialarını ölçerek yazdır (varsayım değil)"""
    W_ = blank_dunya(12.9)
    kutu = None
    for p in PARCALAR:
        if p["grup"].startswith("B_"):
            sh = uygula(p["wp"].val(), W_[p["grup"]])
            kutu = sh if kutu is None else kutu.fuse(sh)
    b = kutu.BoundingBox()
    print("KAPALI KUTU (olculdu): x %.1f..%.1f (%.1f) · y %.1f..%.1f (%.1f) · z %.1f..%.1f (%.1f)" % (b.xmin, b.xmax, b.xlen, b.ymin, b.ymax, b.ylen, b.zmin, b.zmax, b.zlen))
    W0 = blank_dunya(1.7)
    duz = None
    for p in PARCALAR:
        if p["grup"].startswith("B_"):
            sh = uygula(p["wp"].val(), W0[p["grup"]])
            duz = sh if duz is None else duz.fuse(sh)
    d = duz.BoundingBox()
    print("DUZ ACILIM (kalipta): %.0f x %.0f mm · x %.1f..%.1f · z %.1f..%.1f (v7 on cerceve arkasi +%.0f: %.1f mm iceride)" % (d.xlen, d.zlen, d.xmin, d.xmax, d.zmin, d.zmax, Z_CERCEVE[0], Z_CERCEVE[0] - d.zmax))
    assert d.zmax <= Z_CERCEVE[0] - 2.0 and d.xmin >= SAC + 2.0 and d.xmax <= W - SAC - 2.0, "duz blank modul disina tasiyor"
    tasan = []
    for p in PARCALAR:
        if p["grup"] in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF") or p["grup"].startswith("B_"):     # v7: tutamak istisnası YOK (kulp kalmadı)
            continue
        bb = p["wp"].val().BoundingBox()
        if bb.xmin < -0.5 or bb.xmax > W + 0.5 or bb.ymin < -0.5 or bb.ymax > H + 0.5 or bb.zmin < -D - 0.5 or bb.zmax > Z_ON + 0.5:
            tasan.append(p["ad"])
    print("ZARF (modul %.0f x %.0f x %.0f · z -%.0f..+%.0f, istisnasiz): %s" % (W, H, D + Z_ON, D, Z_ON, "hepsi icinde" if not tasan else "TASAN: " + ", ".join(tasan)))
    assert not tasan, "modul zarfini asan parca var"
    # v3 · ALT TABAN ÇİZGİSİ: tabanın altında yalnız ayak, süpürgelik ve koruyuculu asansör tahriki kalabilir
    ALTTA_SERBEST = ("ayak_", "onyuz_plint")
    alta = [p["ad"] for p in PARCALAR if p["grup"] not in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF") and not p["grup"].startswith("B_")
            and p["wp"].val().BoundingBox().ymin < Y_PLINT - 0.5 and not p["ad"].startswith(ALTTA_SERBEST)]
    tah = [p["wp"].val().BoundingBox() for p in PARCALAR if p["ad"].startswith(("asansor_kasnak_", "asansor_kayisi"))]
    print("ALT TABAN %.0f: govde tabani %.0f-%.0f · taban altinda yalniz ayak + supurgelik; tahrik ICERIDE (kasnak/kayis %.0f-%.0f) · baska parca %s"
          % (Y_PLINT, Y_PLINT, Y_PLINT + 3.0, min(b.ymin for b in tah), max(b.ymax for b in tah), "YOK" if not alta else ", ".join(alta)))
    assert not alta, "tabanin altina inen govde parcasi var"
    assert min(b.ymin for b in tah) >= Y_PLINT + 4.0, "kasnak/kayis taban ustunde en az 1 mm payla olmali"
    yig = Y_YIGIN_UST - Y_PLAT
    print("SARJOR: yigin %.0f mm = %d kutu @1,6 mm · %d @1,8 mm  (gunde 80 pide + 200 lahmacun = 280 urun; en az 2 lahmacun/kutu ile 180 kutu/gun)" % (yig, yig / 1.6, yig / 1.8))
    print("DONGU: blank -> katli kutu %.1f sn · kapak kapatma %.1f sn · tam dongu %.0f sn (sim varsayimi: katlama 15 sn, kapak 3 sn)" %
          (Z_KOL[2] - Z_BESLE[0], Z_KAPAT[2] - Z_YATIR[0], DONGU))
    print("KAPAK KOLU: temas %.1f der · kapak 85 der icin %.1f der · 100 der icin %.1f der" % (BETA_TEMAS, kol_icin_beta(85.0), BETA_100))
    # asansör torku (Tr16x4, eta 0,35, 2:1 kayış)
    m = (yig / 1.6) * 0.160 + 10.0
    Tm = m * 9.81 * 0.004 / (2 * math.pi * 0.35) / 2.0
    print("ASANSOR: yuk %.0f kg -> motor torku %.2f N.m (STP-MTR-23079 tutma 1,95) · Tr16x4 kendinden kilitli" % (m, Tm))
    assert Tm < 1.95 * 0.6
    # piston kuvveti (SFU1610, eta 0,9, 1:1) — 1800 d/dk'da motor ~0,3 N.m
    F = 2 * math.pi * 0.9 * 0.3 / 0.010
    print("PISTON: 1800 d/dk'da ~%.0f N itme (katlama kuvveti tahmini 50-100 N) · hiz %.0f mm/s" % (F, 1800 / 60.0 * 10.0))


# v7: olcum_v5 (v4 dilim eşdeğerliği) ve olcum_v6 (v5 ↔ v6) ÇIKARILDI — ikisi de v6 ön yüzüne (ön köşe dikmeleri, on_ust_kapak) bağlıydı;
#     v6 ↔ v7 parça parça karşılaştırma + kinematik birebirlik olcum_v7'de. (Geçmiş: kutu_cad_v6.py'de aynen duruyor.)


def icecek_on_olcum():
    """v6 · İÇECEK YEDEĞİNİN ÖNÜ — v7: bölge koli önünden ÖN DÜZLEME (+79) kadar; kapak kanatları AÇIK kabul edilir (KAPI_ADLARI hariç) ·
    katılardan ölçer, modul()'den SONRA çağrılır (montaj E_ICECEK_YEDEK metni de buradan) · dönüş biçimi v6 ile aynı.
    on: kolilerin önünden ön düzleme kadar olan bölgeye giren gövde parçaları · net: kolilerin yüksekliğinde öndeki soldaki son engel ile
    sağdaki ilk engel arası (x) · sutun: her sütunun DÜZ çekme yoluna (koli izdüşümü, koli önü → ön düzlem) binen parçalar + x bindirmesi (mm) ·
    sag_bos: sağ sütunun sağında (koli yüksekliği ve derinliğinde) ilk engele kadar boşluk · ara: iki sütun arası."""
    X_, Y_, Z_ = ICECEK_YEDEK["x"], ICECEK_YEDEK["y"], ICECEK_YEDEK["z"]
    G_ = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] in ("SABIT", "ASANSOR") and not p["ad"].startswith("icecek_") and p["ad"] not in KAPI_ADLARI]

    def kesen(x0, x1, y0, y1, z0, z1):
        b0 = kut(x0, x1, y0, y1, z0, z1).val(); B0 = b0.BoundingBox(); L = []
        for ad, sh in G_:
            b_ = sh.BoundingBox()
            if _bb_kesisir(B0, b_) and sh.intersect(b0).Volume() > 0.5:
                L.append((ad, b_))
        return L
    ZK = Z_ON + KOLI["z"]           # v7b (denetim bulgusu 1): koli TAMAMEN çıkana kadar — ön düzlemin önünde bir koli boyu (+79 … +346)
    on = kesen(X_[0], X_[1], Y_[0], Y_[1], Z_[1], ZK)
    orta = (X_[0] + X_[1]) / 2.0
    net = (max([b_.xmax for _a, b_ in on if b_.xmax <= orta] + [SAC]), min([b_.xmin for _a, b_ in on if b_.xmin >= orta] + [W - SAC]))
    sut = []
    for x0, x1 in ICECEK_X:
        eng = [(a, round(min(x1, b_.xmax) - max(x0, b_.xmin), 2)) for a, b_ in kesen(x0, x1, Y_[0], Y_[1], Z_[1], ZK)]
        sut.append(dict(x=(x0, x1), engel=eng, bindirme=max([v for _a, v in eng] + [0.0])))
    sag = kesen(X_[1], W, Y_[0], Y_[1], Z_[0], Z_[1])
    return dict(on=sorted({a for a, _b in on}), net=net, sutun=sut, sag_bos=min([b_.xmin for _a, b_ in sag] + [W]) - X_[1], ara=ICECEK_X[1][0] - ICECEK_X[0][1])


# ---- v7 · beyan: v6 → v7 parça listesi (olcum_v7 katılardan ölçüp bununla karşılaştırır) ----
V7_CIKAN = ("plint_on", "on_ust_kapak", "on_ust_kapak_kulp", "kose_dikme_on_0", "kose_dikme_on_1", "sarjor_yan_kapisi_kulp")
V7_DEGISEN = ("taban_sac_3", "ust_sac", "sol_sac_pizza_penceresi", "sag_sac", "sarjor_kapi_esigi", "asansor_ray_plakasi", "kalip_alt_rafi",
              "kalip_alt_rafi_koseben_sol", "kopru_plaka_tutucu", "kopru_motor_askisi", "kablo_kanali_dikey_alt", "kablo_kanali_dikey_ust",
              "asansor_motoru", "besleyici_motoru", "kopru_motoru", "piston_motoru", "parmak_motoru", "flap_katlayici_motoru", "kol_motoru",
              # v7b: kaplin delikli + yeri · köprü / flap motor braketi 8,5 aşağı · raf köşebendinde motor çentiği
              "kopru_kaplini", "flap_katlayici_kaplini", "kopru_motor_braketi", "flap_katlayici_motor_braketi", "flap_katlayici_braket_ayagi",
              "kalip_alt_rafi_koseben_sag")
V7_YENI = tuple(["onyuz_dikme_sol", "onyuz_dikme_sag", "onyuz_kayit_orta", "onyuz_kayit_ust"] + [q[0] for q in ON_PANEL] +
                ["onyuz_mentese_%d" % i for i in range(12)] + ["onyuz_basac_%d" % i for i in range(5)] +
                ["onyuz_alt_dayama_dudagi", "sarjor_kapi_esigi_kosebendi_sol", "sarjor_kapi_esigi_kosebendi_sag"] +
                ["onyuz_plint", "ayak_4", "ayak_5", "sarjor_yan_kapisi_mentese_0", "sarjor_yan_kapisi_mentese_1", "sarjor_yan_kapisi_basac",
                 "asansor_ray_plakasi_flansi", "asansor_ray_plakasi_ust_kosebendi_sol", "asansor_ray_plakasi_ust_kosebendi_sag", "asansor_alt_sensor_braketi",
                 "besleyici_plaka_askisi_2", "besleyici_plaka_askisi_3", "besleyici_arka_sensor_braketi", "kalip_alt_rafi_duvar_takozu_sag",
                 "kopru_alt_sensor_braketi", "piston_ust_sensor_braketi", "piston_eksen_plakasi_bagi_sol", "piston_eksen_plakasi_bagi_sag",
                 "parmak_red_flans_plakasi", "parmak_sensor_braketi", "kapak_alt_plaka_ayagi_2", "kapak_alt_plaka_ayagi_3",
                 "flap_katlayici_sensor_braketi", "kol_red_flans_plakasi", "kol_sensor_braketi"] +
                ["pano_plakasi_burcu_%d" % i for i in range(4)] + ["sensor_yigin_ustu_braketi", "sensor_blank_var_braketi", "sensor_kutu_dolu_braketi"])
V7_CIKAN = tuple(V7_CIKAN) + ("kapak_masasi",)                                   # v8: kapak masası açıkça iki levha (v7 ↔ v8 farkı beyanı)
V7_YENI = tuple(V7_YENI) + ("kapak_masasi_0", "kapak_masasi_1")
# havada denetimi: taşınan ürün / robot aleti / K referansı E'nin parçası değil (montajdan düşer ya da üründür)
HAVADA_DIS = ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF")          # + "B_*" (kutu blank'ı: kalıp raylarının 0,1 üstünde kayar)
BEYAZ = (   # idealleştirilmiş temas (SPEC §3: bilyeli ray, rulman burcu gibi) — (ad parçası a, ad parçası b, en çok aralık mm, gerekçe)
    ("_kayisi", "_kasnak_", 0.40, "GT3 kayış hatve dairesinde modellendi, kasnak dış çapı 0,38 küçük (gerçekte dişler kavraşır)"),
    ("_vidasi_somun", "_vidasi_mil", 0.25, "bilyalı somun ↔ vida mili (bilyeler modellenmedi · 0,2)"),
    ("kopru_kilavuz_mili", "kopru_burcu", 0.15, "LM12UU lineer burç ↔ Ø12 mil (bilyeler modellenmedi · 0,1)"),
)


def kapi_matrisi(ad, aci):
    """kanat açılışı · v7b: SIFIR ÇIKINTILI gizli menteşe — sanal eksen kapağın menteşe kenarının MENTESE_OFSET (20) DIŞINDA, ön düzlemde
    (sol: x0 − 20 · sağ: x1 + 20, z Z_ON). 90°'de kapağın iç yüzü yan sacın iç yüzünde: koli yolu kapakla kesişmez. Sabit eksen = gerçek çok mafsallı
    hareketin sadeleştirmesi (VARSAYIM; Blum 155° zero protrusion ailesi). v7 ilk: eksen kapağın dış köşesindeydi → 20'lik büküm koli yoluna dönüyordu
    (denetim bulgusu 1). aci derece, 0 = kapalı, en çok KAPI_MAX_ACI."""
    k = [q for q in ON_PANEL if q[0] == ad][0]
    xp = k[1] - MENTESE_OFSET if k[5] == "sol" else k[2] + MENTESE_OFSET
    fi = -aci if k[5] == "sol" else aci
    return mm4(mm4(tr4((xp, 0.0, Z_ON)), rot4("y", fi)), tr4((-xp, 0.0, -Z_ON)))


def havada_v7():
    """denetim_temas_v1 + beyaz liste: ham bileşenlerden, beyaz listedeki bir çiftle (aralık ≤ pay) zemine bağlı bir parçaya değenler bağlı sayılır"""
    import denetim_temas_v1 as DT
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    ps = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] not in HAVADA_DIS and not p["grup"].startswith("B_")]
    s = DT.havada(ps)
    S = dict(ps)
    yuzen = {a for d_ in s["bilesen"] for a in d_["uye"]}
    bagli = [a for a, _sh in ps if a not in yuzen]
    kalan, beyaz = list(s["bilesen"]), []
    degisti = True
    while degisti:
        degisti = False
        for d_ in list(kalan):
            bul = None
            for a in d_["uye"]:
                for p_, q_, pay, neden in BEYAZ:
                    for b in bagli:
                        if not ((p_ in a and q_ in b) or (q_ in a and p_ in b)):
                            continue
                        x = BRepExtrema_DistShapeShape(S[a].wrapped, S[b].wrapped)
                        if x.IsDone() and x.Value() <= pay:
                            bul = (a, b, x.Value(), neden)
                            break
                    if bul:
                        break
                if bul:
                    break
            if bul:
                kalan.remove(d_); bagli += d_["uye"]; beyaz.append(dict(uye=d_["uye"], cift=bul)); degisti = True
    return dict(ham=s, kalan=kalan, beyaz=beyaz)


def on_yuz_izgarasi(adim=10.0):
    """ön düzlem ızgarası (z Z_ON − 0,75: ön sacın içi) — her nokta ya bir panelin İÇİNDE (katı sınıflandırma, BRepClass3d), ya derzde,
    ya ROBOT AĞZINDA olmalı; ağızda panel olmamalı, derzde panel olmamalı"""
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.gp import gp_Pnt
    from OCP.TopAbs import TopAbs_IN
    pan = []
    for q in ON_PANEL:
        sh = [p for p in PARCALAR if p["ad"] == q[0]][0]["wp"].val()
        pan.append((q[0], sh, sh.BoundingBox()))
    zc = Z_ON - TAVA_T / 2.0

    def derz(x, y):
        if x < SAC or y > Y_UST[1] or y < Y_ALT[0]:
            return True
        if Y_ALT[1] < y < Y_ORTA[0] or Y_ORTA[1] < y < Y_UST[0]:
            return True
        if X_ORTA_DERZ[0] < x < X_ORTA_DERZ[1] and not (Y_ORTA[0] <= y <= Y_ORTA[1]):
            return True
        if AGIZ["x"][1] < x < AGIZ["x"][1] + DERZ and Y_ORTA[0] <= y <= Y_ORTA[1]:
            return True
        return False
    say = dict(panel=0, derz=0, agiz=0); hata = []
    for i in range(int(W / adim)):
        x = adim * (i + 0.37)                  # ızgara kenar çizgilerine (85, 415 …) denk gelmesin
        for j in range(int((H - Y_ALT[0]) / adim)):
            y = Y_ALT[0] + adim * (j + 0.37)
            icinde = []
            for a, sh, b in pan:
                if b.xmin <= x <= b.xmax and b.ymin <= y <= b.ymax:
                    if BRepClass3d_SolidClassifier(sh.wrapped, gp_Pnt(x, y, zc), 1e-6).State() == TopAbs_IN:
                        icinde.append(a)
            agiz = AGIZ["x"][0] < x < AGIZ["x"][1] and AGIZ["y"][0] <= y < AGIZ["y"][1]
            if agiz:
                say["agiz"] += 1
                if icinde:
                    hata.append((x, y, "ağızda panel", icinde))
            elif icinde:
                say["panel"] += 1
                if len(icinde) > 1 or derz(x, y):
                    hata.append((x, y, "çift / derzde panel", icinde))
            elif derz(x, y):
                say["derz"] += 1
            else:
                hata.append((x, y, "BOŞ", []))
    # v7b (denetim bulgusu 7): 10 mm ızgara (x = 10(i + 0,37)) hiçbir derz bandına düşmüyordu → derz ORTA ÇİZGİLERİ ayrıca 5 mm'de örneklenir; hiçbir panel içermemeli
    def ara(a, b, adim=5.0):
        return [a + adim * k for k in range(int((b - a) / adim) + 1)]
    xd, xs = (X_ORTA_DERZ[0] + X_ORTA_DERZ[1]) / 2.0, AGIZ["x"][1] + DERZ / 2.0
    cz = [(xd, y) for y in ara(Y_ALT[0] + 1.0, Y_ALT[1] - 1.0)] + [(xd, y) for y in ara(Y_UST[0] + 1.0, Y_UST[1] - 1.0)] + [(xs, y) for y in ara(Y_ORTA[0] + 1.0, Y_ORTA[1] - 1.0)]
    for yd in ((Y_ALT[1] + Y_ORTA[0]) / 2.0, (Y_ORTA[1] + Y_UST[0]) / 2.0, (Y_UST[1] + H) / 2.0):
        cz += [(x, yd) for x in ara(SAC + 1.0, W - 1.0)]
    cz += [(SAC / 2.0, y) for y in ara(Y_ALT[0] + 1.0, Y_UST[1] - 1.0)]            # K ile arasındaki derzin E yarısı (x 0–1,5)
    say["derz_cizgi"] = 0
    for x, y in cz:
        icinde = [a for a, sh, b in pan if b.xmin <= x <= b.xmax and b.ymin <= y <= b.ymax
                  and BRepClass3d_SolidClassifier(sh.wrapped, gp_Pnt(x, y, zc), 1e-6).State() == TopAbs_IN]
        say["derz_cizgi"] += 1
        if icinde:
            hata.append((x, y, "derz çizgisinde panel", icinde))
    return say, hata


def derz_olcum():
    """v7b (denetim bulgusu 7) · derzler PANEL KATILARININ sınır kutularından (sabitlerden değil) · dönüş {derz adı: açıklık mm}"""
    B = {q[0]: [p for p in PARCALAR if p["ad"] == q[0]][0]["wp"].val().BoundingBox() for q in ON_PANEL}
    a_s, a_g, u_s, u_g = B["onyuz_alt_kanat_sol"], B["onyuz_alt_kanat_sag"], B["onyuz_ust_kanat_sol"], B["onyuz_ust_kanat_sag"]
    o_s, o_g = B["onyuz_orta_sabit_panel"], B["onyuz_orta_servis_kapagi"]
    D = {"ALT kanatlar arası (x)": a_g.xmin - a_s.xmax, "ÜST kanatlar arası (x)": u_g.xmin - u_s.xmax, "ORTA sabit ↔ servis (x)": o_g.xmin - o_s.xmax,
         "ALT sol ↔ ORTA sabit (y)": o_s.ymin - a_s.ymax, "ALT sağ ↔ ORTA servis (y)": o_g.ymin - a_g.ymax,
         "ORTA sabit ↔ ÜST sol (y)": u_s.ymin - o_s.ymax, "ORTA servis ↔ ÜST sağ (y)": u_g.ymin - o_g.ymax,
         "ÜST ↔ tavan 1862 (y)": H - max(u_s.ymax, u_g.ymax), "ALT ↔ alt taban 123 (y)": min(a_s.ymin, a_g.ymin) - Y_PLINT,
         "K ↔ E derzinin E yarısı (x, K yarısıyla 3)": min(b.xmin for b in B.values()) * 2.0}
    hiza = max(abs(a_s.ymin - a_g.ymin), abs(a_s.ymax - a_g.ymax), abs(u_s.ymin - u_g.ymin), abs(u_s.ymax - u_g.ymax), abs(o_s.ymin - o_g.ymin), abs(o_s.ymax - o_g.ymax))
    return D, hiza


KAPI_ACILARI = (1, 2, 3) + tuple(range(5, int(KAPI_MAX_ACI) + 1, 5))      # v7b: 1°…155° (v7 ilk: 10°…120° — 180°'ye kadar bakılmıyordu, denetim bulgusu 7)


def kapi_acilma_olcum(acilar=KAPI_ACILARI):
    """her kanat 1°…155°: en uç z (QR yüzü 670'e çarpmamalı) · E'nin SABİT + ASANSÖR parçalarıyla çakışma (kendisi + kendi menteşeleri hariç) ·
    koli yolu prizmalarıyla çakışan açılar (v7b: prizma koli önü −83 → ön düzlemin önünde bir koli boyu, +346) — ≥ KOLI_ACI'da HİÇ olmamalı ·
    x taşması (sol kanatlar K'nın önüne, sağlar hat sonuna döner — z > +79'da)"""
    koli = [kut(x0, x1, ICECEK_Y0, ICECEK_YEDEK["y"][1], ICECEK_Z[1], Z_ON + KOLI["z"]).val() for x0, x1 in ICECEK_X]
    sab = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] in ("SABIT", "ASANSOR")]
    sab = [(a, sh, sh.BoundingBox()) for a, sh in sab]
    R = {}
    for ad in KAPI_ADLARI:
        kap = [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val()
        haric = {ad} | {m for m, k in MENTESE_KAPI.items() if k == ad}
        r = dict(zmax=-1e9, xmin=1e9, xmax=-1e9, cak=[], koli=[], zmin_x_disi=1e9)
        for aci in acilar:
            sh = uygula(kap, kapi_matrisi(ad, aci)); B = sh.BoundingBox()
            r["zmax"] = max(r["zmax"], B.zmax); r["xmin"] = min(r["xmin"], B.xmin); r["xmax"] = max(r["xmax"], B.xmax)
            if B.xmin < 0.0 or B.xmax > W:                  # modül dışına dönen kısmın en arka z'si (komşu kapağın ön yüzü +79'u geçmemeli)
                dis = sh.intersect(kut(-2000.0, 0.0, -10.0, H + 10.0, -D, 2000.0).val() if B.xmin < 0.0 else kut(W, W + 2000.0, -10.0, H + 10.0, -D, 2000.0).val())
                if dis.Volume() > 0.01:
                    r["zmin_x_disi"] = min(r["zmin_x_disi"], dis.BoundingBox().zmin)
            for a, s_, b in sab:
                if a in haric or not _bb_kesisir(B, b):
                    continue
                v = sh.intersect(s_).Volume()
                if v > 0.5:
                    r["cak"].append((aci, a, round(v, 1)))
            for kb in koli:
                if _bb_kesisir(B, kb.BoundingBox()) and sh.intersect(kb).Volume() > 0.01:
                    r["koli"].append(aci)
                    break
        r["koli_serbest_min"] = min([a_ for a_ in acilar if all(b_ not in r["koli"] for b_ in acilar if b_ >= a_)] + [999])
        R[ad] = r
    return R


def robot_agzi_taramasi(adim=0.05, esik=0.5, yakin=30.0):
    """robot çatalı + kutu (t 13,9–17,3, adım 0,05 sn) × E'nin BÜTÜN SABİT parçaları (çakışma) · ön parçalara en küçük aralık (pay)"""
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    t0 = time.time()
    sab = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT"]
    sab = [(a, sh, sh.BoundingBox()) for a, sh in sab]
    on_ad = set([q[0] for q in ON_PANEL] + ["onyuz_kayit_orta", "onyuz_kayit_ust", "onyuz_dikme_sol", "onyuz_dikme_sag"])
    anlar = [round(Z_CATAL[0] + adim * i, 3) for i in range(int(round((Z_CATAL[3] - Z_CATAL[0]) / adim)) + 1)]
    bul, pay = {}, {}
    for t in anlar:
        W_ = blank_dunya(t)
        hare = [(p["ad"], uygula(p["wp"].val(), grup_matrisi("CATAL", t))) for p in PARCALAR if p["grup"] == "CATAL"]
        hare += [(p["ad"], uygula(p["wp"].val(), W_[p["grup"]])) for p in PARCALAR if p["grup"].startswith("B_")]
        for a, sh in hare:
            A = sh.BoundingBox()
            for q, s_, b in sab:
                if _bb_kesisir(A, b):
                    v = sh.intersect(s_).Volume()
                    if v > esik and (a, q) not in bul:
                        bul[(a, q)] = (round(v, 1), t)
                if q in on_ad and not (A.xmin > b.xmax + yakin or b.xmin > A.xmax + yakin or A.ymin > b.ymax + yakin or b.ymin > A.ymax + yakin
                                       or A.zmin > b.zmax + yakin or b.zmin > A.zmax + yakin):
                    dd = BRepExtrema_DistShapeShape(sh.wrapped, s_.wrapped).Value()
                    if q not in pay or dd < pay[q][0]:
                        pay[q] = (dd, a, t)
    return dict(an=len(anlar), bul=bul, pay=pay, sure=time.time() - t0)


def asansor_strok_taramasi(adim=10.0, esik=0.5):
    """ASANSÖR grubu (platform, çatallar, araba, HGH15 arabaları, somun) 0 → somun üst yatağa değene kadar yukarı · × v7'de yeni / değişen SABİT parçalar
    (GLB animasyonunda asansör hareket etmiyor — bu tarama o boşluğu kapatır)"""
    def bb(ad):
        return [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val().BoundingBox()
    strok = bb("asansor_ust_yatak").ymin - bb("asansor_somunu").ymax
    asan = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] == "ASANSOR"]
    hed = [(p["ad"], p["wp"].val()) for p in PARCALAR if p["grup"] == "SABIT" and (p["ad"] in V7_YENI or p["ad"] in V7_DEGISEN)]
    hed = [(a, sh, sh.BoundingBox()) for a, sh in hed]
    n = int(strok / adim)
    bul = {}
    for i in range(n + 2):
        dy = min(strok, i * adim)
        for a, sh in asan:
            s2 = sh.translate(cq.Vector(0.0, dy, 0.0)); A = s2.BoundingBox()
            for q, s_, b in hed:
                if _bb_kesisir(A, b):
                    v = s2.intersect(s_).Volume()
                    if v > esik and (a, q) not in bul:
                        bul[(a, q)] = (round(v, 1), dy)
    return dict(strok=strok, adim=n + 2, hedef=len(hed), bul=bul)


def _kesit_I(dik):
    """dikdörtgenler (u0, u1, v0, v1) → (alan, I_u ekseni etrafında [v yönü eğilme], I_v) — ağırlık merkezine göre"""
    A = sum((u1 - u0) * (v1 - v0) for u0, u1, v0, v1 in dik)
    uc = sum((u1 - u0) * (v1 - v0) * (u0 + u1) / 2.0 for u0, u1, v0, v1 in dik) / A
    vc = sum((u1 - u0) * (v1 - v0) * (v0 + v1) / 2.0 for u0, u1, v0, v1 in dik) / A
    Iu = sum((u1 - u0) * (v1 - v0) ** 3 / 12.0 + (u1 - u0) * (v1 - v0) * ((v0 + v1) / 2.0 - vc) ** 2 for u0, u1, v0, v1 in dik)
    Iv = sum((v1 - v0) * (u1 - u0) ** 3 / 12.0 + (u1 - u0) * (v1 - v0) * ((u0 + u1) / 2.0 - uc) ** 2 for u0, u1, v0, v1 in dik)
    cv = max(max(abs(v0 - vc), abs(v1 - vc)) for u0, u1, v0, v1 in dik)
    cu = max(max(abs(u0 - uc), abs(u1 - uc)) for u0, u1, v0, v1 in dik)
    return A, Iu, Iv, cv, cu


def _sek(ad):
    return [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val()


def temas_alani(a, b, d=0.1):
    """v7b · iki katı arasındaki en büyük DÜZLEMSEL temas yaması: b altı eksen yönünde d kaydırılıp a ile kesiştirilir → alan = hacim / d (mm²) ·
    ikinci dönüş: yamanın kısa kenarı (kesişimin sınır kutusunun ortanca boyu, mm) — bindirme ≥ 10 mm denetimi için"""
    en = (0.0, 0.0)
    for v in ((d, 0, 0), (-d, 0, 0), (0, d, 0), (0, -d, 0), (0, 0, d), (0, 0, -d)):
        c = a.intersect(b.translate(cq.Vector(*v)))
        V = c.Volume()
        if V > 1e-6 and V / d > en[0]:
            bb_ = c.BoundingBox()
            en = (V / d, sorted([bb_.xlen, bb_.ylen, bb_.zlen])[1])
    return en


# v7b · denetim bulgusu 5: bağlantı elemanı olarak ölçülen temaslar — (parça, taşıyıcı): düzlemsel temas ≥ 100 mm² ve kısa kenar ≥ 9,9 mm (cıvatalı bindirme)
BAGLANTI_V7B = (
    ("asansor_alt_sensor_braketi", "asansor_ray_plakasi"), ("besleyici_arka_sensor_braketi", "besleyici_plakasi"), ("kopru_alt_sensor_braketi", "kopru_burc_plakasi"),
    ("piston_ust_sensor_braketi", "piston_eksen_plakasi"), ("parmak_sensor_braketi", "parmak_yatak_askisi"), ("flap_katlayici_sensor_braketi", "kapak_alt_plakasi"),
    ("kol_sensor_braketi", "kol_yatak_ayagi_1"), ("sensor_yigin_ustu_braketi", "sag_sac"), ("sensor_blank_var_braketi", "sag_sac"),
    ("sensor_kutu_dolu_braketi", "sol_sac_pizza_penceresi"),
    ("piston_eksen_plakasi_bagi_sol", "besleyici_plakasi"), ("piston_eksen_plakasi_bagi_sol", "piston_eksen_plakasi"),
    ("piston_eksen_plakasi_bagi_sag", "besleyici_plakasi"), ("piston_eksen_plakasi_bagi_sag", "piston_eksen_plakasi"),
    ("parmak_red_flans_plakasi", "parmak_red_braketi"), ("kol_red_flans_plakasi", "kol_reduktor_braketi"),
    ("asansor_ray_plakasi_ust_kosebendi_sol", "asansor_ray_plakasi"), ("asansor_ray_plakasi_ust_kosebendi_sol", "sol_sac_pizza_penceresi"),
    ("asansor_ray_plakasi_ust_kosebendi_sag", "asansor_ray_plakasi"), ("asansor_ray_plakasi_ust_kosebendi_sag", "sag_sac"),
    ("asansor_ray_plakasi_flansi", "asansor_ray_plakasi"), ("asansor_ray_plakasi_flansi", "taban_sac_3"),
    ("sarjor_kapi_esigi", "taban_sac_3"), ("sarjor_kapi_esigi_kosebendi_sol", "sarjor_kapi_esigi"), ("sarjor_kapi_esigi_kosebendi_sol", "sol_sac_pizza_penceresi"),
    ("sarjor_kapi_esigi_kosebendi_sag", "sarjor_kapi_esigi"), ("sarjor_kapi_esigi_kosebendi_sag", "sag_sac"),
    ("onyuz_alt_dayama_dudagi", "taban_sac_3"), ("kalip_alt_rafi_duvar_takozu_sag", "sag_sac"),
    ("besleyici_plaka_askisi_2", "besleyici_plakasi"), ("besleyici_plaka_askisi_3", "besleyici_plakasi"),
    ("kapak_alt_plaka_ayagi_2", "kalip_alt_rafi"), ("kapak_alt_plaka_ayagi_3", "kalip_alt_rafi"),
)
# M8 endüktif sensörler delikli saçta (Ø8,04 delik: katı bindirmesi yok, aralık ≤ 0,05 = değer)
SENSOR_DELIK = (("asansor_alt_sensor", "asansor_alt_sensor_braketi"), ("besleyici_arka_sensor", "besleyici_arka_sensor_braketi"),
                ("kopru_alt_sensor", "kopru_alt_sensor_braketi"), ("piston_ust_sensor", "piston_ust_sensor_braketi"), ("parmak_sensor", "parmak_sensor_braketi"),
                ("flap_katlayici_sensor", "flap_katlayici_sensor_braketi"), ("kol_sensor", "kol_sensor_braketi"))


def olcum_v7(tam=True):
    """v7 · ÖN DÜZLEM +79 — iddiaları ÖLÇER, bozulursa durur (assert). tam=False: süpürme taramaları (kapak, robot ağzı, asansör) atlanır.
    Dönüş: ölçülen değerler sözlüğü (rapor ve montaj için)."""
    import dilim_v1 as DL
    import kutu_cad_v6 as V6
    O = {}
    SAY = [0]

    def yaz(ad, sart, deger=""):
        SAY[0] += 1
        print("  %-110s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger)); sys.stdout.flush()
        assert sart, ad

    def bb(ad):
        return [p for p in PARCALAR if p["ad"] == ad][0]["wp"].val().BoundingBox()
    print("OLCUM v8 (on duzlem +%.0f · derinlik %.0f · SPEC_on_duzlem_v63 §2.6)" % (Z_ON, D + Z_ON))
    # 1 · v6 ↔ v7 parça parça (sınır kutusu ±0,01 + hacim) — beyan edilen listelerle AYNI olmalı
    V6.modul()
    k = DL.karsilastir(PARCALAR, V6.PARCALAR)
    fark_ad = sorted({f.split(":")[0] for f in k["fark"]})
    O["v6_v7"] = dict(v6=len(V6.PARCALAR), v7=len(PARCALAR), ayni=len(k["ayni"]), degisen=fark_ad, cikan=sorted(k["ref_eksik"]), yeni=sorted(k["yeni_ek"]))
    yaz("v6 ↔ v7: v6 %d → v7 %d parça · birebir %d · değişen %d · çıkan %d · yeni %d (beyan edilen listelerle aynı)"
        % (len(V6.PARCALAR), len(PARCALAR), len(k["ayni"]), len(fark_ad), len(k["ref_eksik"]), len(k["yeni_ek"])),
        set(fark_ad) == set(V7_DEGISEN) and set(k["ref_eksik"]) == set(V7_CIKAN) and set(k["yeni_ek"]) == set(V7_YENI),
        "fark: değişen %s · çıkan %s · yeni %s" % (sorted(set(fark_ad) ^ set(V7_DEGISEN)), sorted(set(k["ref_eksik"]) ^ set(V7_CIKAN)), sorted(set(k["yeni_ek"]) ^ set(V7_YENI))))
    print("     değişen: %s" % ", ".join(fark_ad))
    print("     çıkan: %s" % ", ".join(sorted(k["ref_eksik"])))
    print("     yeni: %s" % ", ".join(sorted(k["yeni_ek"])))
    # 2 · KİNEMATİK v6 ile BİREBİR (çatal / kutu yolu, kafa(t), blank açıları, pizza, itici, köprü, katlayıcı, kol, parmak)
    SABITLER = ("W", "H", "D", "SAC", "Y_PLINT", "TEPSI", "KALIP", "YB", "T", "PLAKA_K", "PENCERE", "BX0", "BX1", "ZB", "BZ0", "BZ1", "ALT_RAF_Y", "X_BL0", "X_BL1",
                "Z_BL0", "Z_BL1", "BESLE", "ZS0", "ZS1", "Y_PLAT", "SARJOR_ADET", "H_UST", "KOL_P", "KOL_R", "KMER", "X_CATAL", "X_BAR", "CATAL_DIS", "Z_CATAL",
                "KAPAK_BASKI", "H_BEKLE", "Y_VURUS2", "ICECEK_X", "ICECEK_Z", "ICECEK_Y0", "ICECEK_KAT", "KOLI", "DONGU", "PARMAK_P", "PARMAK_R", "U_MAX")
    g_ = globals()
    dif = [n for n in SABITLER if g_[n] != getattr(V6, n)]
    yaz("kaydedilmiş ölçüler + kinematik sabitleri (%d: tepsi, kalıp, blank, şarjör, çatal, içecek yedeği, döngü …) v6 ile aynı" % len(SABITLER), not dif, str(dif))
    f = 0.0
    TT = [i * 0.01 for i in range(int(round(DONGU / 0.01)) + 1)]
    for t in TT:
        f = max(f, abs(kafa(t) - V6.kafa(t)), abs(u_zimba(t) - V6.u_zimba(t)), abs(parmak_psi(t) - V6.parmak_psi(t)), abs(kapak_alfa(t) - V6.kapak_alfa(t)),
                abs(kol_beta(t) - V6.kol_beta(t)), abs(katlayici_dy(t) - V6.katlayici_dy(t)), abs(kopru_dy(t) - V6.kopru_dy(t)), abs(itici_dz(t) - V6.itici_dz(t)))
        for a_, b_ in ((catal_trs(t), V6.catal_trs(t)), (catal_kutu(t), V6.catal_kutu(t)), (pizza_trs(t), V6.pizza_trs(t)), (k_itici_trs(t), V6.k_itici_trs(t))):
            f = max(f, max(abs(x - y) for x, y in zip(a_, b_)))
        k0, A0 = blank_acilar(t); k1, A1 = V6.blank_acilar(t)
        f = max(f, max(abs(x - y) for x, y in zip(k0, k1)), max(abs(A0[g] - A1[g]) for g in A0))
    fm = 0.0
    for t in KUTU_ANLARI + GECIS_ANLARI + tuple(round(Z_CATAL[0] + 0.1 * i, 2) for i in range(35)):
        M7, M6 = blank_dunya(t), V6.blank_dunya(t)
        fm = max(fm, max(abs(M7[g][i][j] - M6[g][i][j]) for g in M7 for i in range(4) for j in range(4)))
    O["kinematik_fark"] = (f, fm)
    yaz("kinematik: %d an (0,01 sn) · kafa(t) · blank_acilar(t) · çatal · kutu · pizza · K itici · kol · parmak · köprü · katlayıcı · itici → en büyük fark %.1e · blank_dunya %.1e"
        % (len(TT), f, fm), f < 1e-12 and fm < 1e-12)
    # 3 · ÖN DÜZLEM
    zs = [(q[0], bb(q[0])) for q in ON_PANEL]
    O["on_panel"] = {a: (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax) for a, b in zs}
    yaz("ön paneller %d (6 tava): hepsinin dış yüzü z +%.1f, arka kenarı +%.1f (20 büküm) · kalınlık 1,5" % (len(zs), Z_ON, Z_PANEL),
        len(zs) == 6 and all(abs(b.zmax - Z_ON) < 0.01 and abs(b.zmin - Z_PANEL) < 0.01 for _a, b in zs))
    urun = lambda p: p["grup"] in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF") or p["grup"].startswith("B_")
    en_on = max((p["wp"].val().BoundingBox().zmax, p["ad"]) for p in PARCALAR if not urun(p))
    en_arka = min(p["wp"].val().BoundingBox().zmin for p in PARCALAR if not urun(p))
    O["zarf_z"] = (en_arka, en_on[0])
    yaz("zarf: en öndeki parça %s z +%.2f ≤ +%.1f (ön düzlem + 0,5) · en arka %.1f ≥ −%.1f · kulp / tutamak YOK" % (en_on[1], en_on[0], Z_ON + 0.5, en_arka, D + 0.5),
        en_on[0] <= Z_ON + 0.5 and en_arka >= -D - 0.5 and not [p for p in PARCALAR if "_kulp" in p["ad"]])
    kn = {a: bb(a) for a in ("sol_sac_pizza_penceresi", "sag_sac", "ust_sac", "taban_sac_3", "arka_sac", "onyuz_plint", "onyuz_dikme_sol", "onyuz_dikme_sag", "onyuz_kayit_orta", "onyuz_kayit_ust")}
    yaz("gövde kenarları: sol / sağ / üst sac ön kenarı +%.1f · taban +%.1f · arka sac −%.1f…−%.1f (SABİT) · çerçeve +%.0f…+%.0f · plint +%.1f…+%.1f"
        % (Z_PANEL, Z_TABAN_ON, D, D - SAC, Z_CERCEVE[0], Z_CERCEVE[1], Z_PLINT[0], Z_PLINT[1]),
        all(abs(kn[a].zmax - Z_PANEL) < 0.01 for a in ("sol_sac_pizza_penceresi", "sag_sac", "ust_sac")) and abs(kn["taban_sac_3"].zmax - Z_TABAN_ON) < 0.01
        and abs(kn["arka_sac"].zmin + D) < 0.01 and all(abs(kn[a].zmax - Z_CERCEVE[1]) < 0.01 and abs(kn[a].zmin - Z_CERCEVE[0]) < 0.01
                                                         for a in ("onyuz_dikme_sol", "onyuz_dikme_sag", "onyuz_kayit_orta", "onyuz_kayit_ust"))
        and abs(kn["onyuz_plint"].zmax - Z_PLINT[1]) < 0.01 and abs(kn["onyuz_plint"].ymin) < 0.01 and abs(kn["onyuz_plint"].ymax - Y_PLINT) < 0.01)
    yaz("ön çerçeve tam boy: dikmeler y %.0f–%.1f (sol + sağ) · kayıtlar derz arkasında (üst yüzleri %.0f / %.0f)" % (Y_ALT[0], H - SAC, Y_ALT[1], Y_ORTA[1]),
        all(abs(kn[a].ymin - Y_ALT[0]) < 0.01 and abs(kn[a].ymax - (H - SAC)) < 0.01 for a in ("onyuz_dikme_sol", "onyuz_dikme_sag"))
        and abs(kn["onyuz_kayit_orta"].ymax - Y_ALT[1]) < 0.01 and abs(kn["onyuz_kayit_ust"].ymax - Y_ORTA[1]) < 0.01)
    iz, iz_h = on_yuz_izgarasi()
    O["izgara"] = iz
    yaz("ön yüz ızgarası (10 mm, katı sınıflandırma): panel %d · robot ağzı %d nokta → boş %d · ağızda panel %d · v7b derz ORTA ÇİZGİLERİ %d nokta (5 mm) → panel içeren %d"
        % (iz["panel"], iz["agiz"], len([h for h in iz_h if h[2] == "BOŞ"]), len([h for h in iz_h if h[2] == "ağızda panel"]), iz["derz_cizgi"],
           len([h for h in iz_h if h[2] in ("derz çizgisinde panel", "çift / derzde panel")])), not iz_h and iz["derz_cizgi"] > 1000, str(iz_h[:4]))
    dz_, hz_ = derz_olcum()
    O["derz"] = dz_
    yaz("derzler PANEL KATILARINDAN (v7b): %s · satır hizası sapma %.2f · omega takviye gerekmez (en geniş panel %.1f ≤ 600)"
        % (" · ".join("%s %.2f" % (k_, v_) for k_, v_ in dz_.items()), hz_, max(q[2] - q[1] for q in ON_PANEL)),
        all(abs(v_ - DERZ) < 0.01 for v_ in dz_.values()) and hz_ < 0.01 and max(q[2] - q[1] for q in ON_PANEL) <= 600.0)
    # 4 · İÇECEK YEDEĞİ: 6 koli yeri AYNI · kapak açıkken koli önü → ön düzlem yolu SERBEST
    kol = [bb("icecek_yedek_koli_%d%d" % (a, b_)) for a in range(len(ICECEK_X)) for b_ in range(ICECEK_KAT)]
    kol6 = [p["wp"].val().BoundingBox() for p in V6.PARCALAR if p["ad"].startswith("icecek_yedek_koli_")]
    yaz("içecek yedeği 6 koli yeri v6 ile aynı (x %.0f–%.0f · y %.0f–%.0f · z %.0f…%.0f)" % (min(b.xmin for b in kol), max(b.xmax for b in kol), min(b.ymin for b in kol),
        max(b.ymax for b in kol), min(b.zmin for b in kol), max(b.zmax for b in kol)),
        len(kol) == 6 and sorted((b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax) for b in kol) == sorted((b.xmin, b.ymin, b.zmin, b.xmax, b.ymax, b.zmax) for b in kol6))
    ion = icecek_on_olcum()
    O["icecek_on"] = ion
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    kpay = []
    for x0, x1 in ICECEK_X:
        pr = kut(x0, x1, ICECEK_Y0, ICECEK_YEDEK["y"][1], ICECEK_Z[1], Z_ON + KOLI["z"]).val()
        m_ = min((BRepExtrema_DistShapeShape(pr.wrapped, p["wp"].val().wrapped).Value() for p in PARCALAR
                 if p["grup"] in ("SABIT", "ASANSOR") and not p["ad"].startswith("icecek_") and p["ad"] not in KAPI_ADLARI
                 and _bb_kesisir(pr.BoundingBox(), p["wp"].val().BoundingBox(), pay=-5.0)), default=99.0)
        kpay.append(round(m_, 2))
    O["koli_yolu_pay"] = kpay
    yaz("koli yolu (kapak açık, koli önü z %.0f → ön düzlemin önünde bir koli boyu +%.0f): engel %d · net açıklık x %.1f–%.1f · sütun bindirmeleri %s · en yakın parçaya pay %s mm"
        % (ICECEK_Z[1], Z_ON + KOLI["z"], len(ion["on"]), ion["net"][0], ion["net"][1], [s_["bindirme"] for s_ in ion["sutun"]], kpay),
        not ion["on"] and all(s_["bindirme"] == 0.0 for s_ in ion["sutun"]) and min(kpay) > 0.0)
    # 5 · KAPAK AÇILIŞI (v7b: 1°…155°, sıfır çıkıntılı menteşe · yarım kanat: QR yüzü z 670)
    ag_ = {a: bb(a) for a in KAPI_ADLARI}
    kutle = {a: [p for p in PARCALAR if p["ad"] == a][0]["wp"].val().Volume() * 7.93e-6 for a in [q[0] for q in ON_PANEL]}
    O["panel_kg"] = kutle
    if tam:
        R = kapi_acilma_olcum()
        O["kapak"] = R
        for a in KAPI_ADLARI:
            r = R[a]
            koli_ok = r["koli_serbest_min"] <= KOLI_ACI if a in KUTU_KANAT else not r["koli"]
            yaz("%-26s %d°…%.0f° (%d açı): en uç z +%.1f < QR %.0f (pay %.0f) · E parçalarıyla çakışma %d · koli yolu (−83 → +%.0f) %s · modül dışı kısım z ≥ +%.1f · %.1f kg"
                % (a, KAPI_ACILARI[0], KAPI_MAX_ACI, len(KAPI_ACILARI), r["zmax"], QR_Z, QR_Z - r["zmax"], len(r["cak"]), Z_ON + KOLI["z"],
                   ("≥ %.0f°'de SERBEST (kesişen açılar %s)" % (r["koli_serbest_min"], r["koli"][-3:] if r["koli"] else "yok")) if a in KUTU_KANAT else "ilgisiz (koli bandı dışında)",
                   r["zmin_x_disi"], kutle[a]),
                r["zmax"] < QR_Z and not r["cak"] and koli_ok and r["zmin_x_disi"] >= Z_ON - 0.01, str(r["cak"][:3]))
        # E sol ALT kanadı işletme açısında (90°) K'nın önünde kapladığı bölge → K ALT kapağıyla SIRA KURALI (ikisi aynı anda açılmaz)
        shk = uygula([p for p in PARCALAR if p["ad"] == "onyuz_alt_kanat_sol"][0]["wp"].val(), kapi_matrisi("onyuz_alt_kanat_sol", KOLI_ACI)).BoundingBox()
        O["k_onu_90"] = (shk.xmin, min(shk.xmax, 0.0), shk.zmin, shk.zmax)
        print("     SIRA KURALI: E sol ALT kanadı %.0f°'de x %.1f…%.1f (hat %.1f…%.1f) · z +%.1f…+%.1f → K'nın ALT (bulaşık) kapağının serbest kenarı (hat 4598,5) bu bölgeden döner:"
              " iki kapak AYNI ANDA AÇILMAZ (önce biri kapanır)" % (KOLI_ACI, shk.xmin, shk.xmax, 4600.0 + shk.xmin, 4600.0 + shk.xmax, shk.zmin, shk.zmax))
    # 5b · v7b · ALT kanat kutu kesit + dayama dudağı (denetim bulgusu 4) · kanat ↔ dudak temas yaması (kapalı konum)
    for a in KUTU_KANAT:
        t_, kk_ = temas_alani(_sek(a), _sek("onyuz_alt_dayama_dudagi"))
        O.setdefault("alt_dayama", {})[a] = t_
        yaz("%s: kutu kesit (tava 1,5 + iç sac 1,0 · %d menteşe · %.1f kg) · alt kenarı dayama dudağına yaslanır: temas %.0f mm² (kısa kenar %.1f)"
            % (a, len(MENTESE_Y[a]), kutle[a], t_, kk_), t_ >= 100.0 and len(MENTESE_Y[a]) == 3)
    bd_ = _sek("onyuz_alt_dayama_dudagi").BoundingBox()
    yaz("dayama dudağı y %.0f–%.0f < koli tabanı %.0f (koli yolunu kapatmaz) · z +%.0f…+%.0f (kanat arka kenarı +%.0f)" % (bd_.ymin, bd_.ymax, ICECEK_Y0, bd_.zmin, bd_.zmax, Z_PANEL),
        bd_.ymax < ICECEK_Y0 and abs(bd_.zmax - Z_PANEL) < 0.01)
    # 6 · ROBOT AĞZI
    yaz("ROBOT AĞZI x %.0f–%.0f (hat %.0f–%.0f) · y %.0f–%.0f · derinlik z 0…+%.0f boş (çerçeve / kayıt / panel yok)"
        % (AGIZ["x"][0], AGIZ["x"][1], 4600.0 + AGIZ["x"][0], 4600.0 + AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1], Z_ON),
        not [p["ad"] for p in PARCALAR if p["grup"] == "SABIT" and _bb_kesisir(kut(AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1], 0.0, Z_ON).val().BoundingBox(), p["wp"].val().BoundingBox())
             and p["wp"].val().intersect(kut(AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1], 0.0, Z_ON).val()).Volume() > 0.01])
    if tam:
        ra = robot_agzi_taramasi()
        O["robot_agzi"] = dict(an=ra["an"], cakisma=len(ra["bul"]), pay={q: round(v[0], 1) for q, v in ra["pay"].items()})
        yaz("robot ağzı taraması: çatal (5) + kutu (14 panel) × E SABİT parçaları · %d an (t %.1f–%.1f, 0,05 sn) · çakışma %d · %.0f sn"
            % (ra["an"], Z_CATAL[0], Z_CATAL[3], len(ra["bul"]), ra["sure"]), not ra["bul"], str(sorted(ra["bul"].items())[:4]))
        print("     ağız payları (en küçük aralık, mm): " + " · ".join("%s %.1f (%s t=%.2f)" % (q, v[0], v[1], v[2]) for q, v in sorted(ra["pay"].items(), key=lambda kv: kv[1][0])))
    # 7 · HAVADA PARÇA
    hv = havada_v7()
    O["havada"] = dict(ham=len(hv["ham"]["bilesen"]), ham_parca=sum(len(d_["uye"]) for d_ in hv["ham"]["bilesen"]), kalan=len(hv["kalan"]), beyaz=hv["beyaz"])
    yaz("havada parça (denetim_temas_v1, tol 0,05): %d parça · zemine bağlı %d · ham bileşen %d → beyaz listeyle %d · KALAN %d"
        % (hv["ham"]["parca"], hv["ham"]["bagli"], len(hv["ham"]["bilesen"]), len(hv["beyaz"]), len(hv["kalan"])), not hv["kalan"],
        " | ".join("%s (%d)" % (d_["en"], len(d_["uye"])) for d_ in hv["kalan"][:6]))
    for b_ in hv["beyaz"]:
        print("     BEYAZ LİSTE: %s … (%d parça) ← %s ~ %s %.3f mm · %s" % (b_["uye"][0], len(b_["uye"]), b_["cift"][0], b_["cift"][1], b_["cift"][2], b_["cift"][3]))
    # 7b · v7b · BAĞLANTI YAMALARI (denetim bulgusu 5): braket / köşebent ↔ taşıyıcı düzlemsel temas + sensör ↔ delik
    kotu, sat = [], []
    for a, b in BAGLANTI_V7B:
        t_, kk_ = temas_alani(_sek(a), _sek(b))
        sat.append("%s↔%s %.0f/%.0f" % (a, b, t_, kk_))
        if t_ < 100.0 or kk_ < 9.9:
            kotu.append((a, b, round(t_, 1), round(kk_, 2)))
    O["baglanti"] = dict(cift=len(BAGLANTI_V7B), kotu=kotu)
    yaz("bağlantı yamaları: %d braket / köşebent çifti · hepsi düzlemsel temas ≥ 100 mm² ve kısa kenar ≥ 10 mm (cıvatalı bindirme) · kötü %d"
        % (len(BAGLANTI_V7B), len(kotu)), not kotu, str(kotu))
    print("     (alan mm² / kısa kenar mm) " + " · ".join(sat))
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    sd_ = []
    for a, b in SENSOR_DELIK:
        A_, B_ = _sek(a), _sek(b)
        sd_.append((a, A_.intersect(B_).Volume(), _DSS(A_.wrapped, B_.wrapped).Value()))
    yaz("M8 sensörler delikli sacta (%d): katı bindirmesi en çok %.3f mm³ · aralık en çok %.3f mm (≤ 0,05 = değer) · iki ucu açık"
        % (len(sd_), max(v for _a, v, _d in sd_), max(d_ for _a, _v, d_ in sd_)), all(v < 0.01 and d_ <= 0.05 for _a, v, d_ in sd_), str(sd_))
    # 7c · v7b · KAPLİN (denetim bulgusu 2): delikli, motora / yatağa binmiyor, mil göbekte, istisna yok
    kp_ = []
    for kap, mot, yat in (("kopru_kaplini", "kopru_motoru", "kopru_BK12"), ("flap_katlayici_kaplini", "flap_katlayici_motoru", "flap_katlayici_yatak_braketi")):
        K_, M_, Y_ = _sek(kap), _sek(mot), _sek(yat)
        kb_, mb_ = K_.BoundingBox(), M_.BoundingBox()
        dal = mb_.ymax - kb_.ymin                           # mil ucu (motorun en üst noktası) − kaplinin alt yüzü
        pilot_pay = kb_.ymin - (mb_.ymax - MIL_UCU + (12.497 - 10.973))   # kaplin altı − pilot üstü
        kp_.append((kap, K_.intersect(M_).Volume(), _DSS(K_.wrapped, M_.wrapped).Value(), dal, pilot_pay, Y_.BoundingBox().ymin - kb_.ymax, K_.intersect(Y_).Volume()))
    O["kaplin"] = kp_
    yaz("kaplin (aday NBK MDS-25C-6.35-10 · Ø25 × %.0f): motorla katı bindirmesi %s mm³ · mil ↔ delik aralığı %s · mil göbeğe dalar %s ≤ göbek %.0f · pilottan pay %s · yatağa pay %s"
        % (KAPLIN["L"], "/".join("%.3f" % q[1] for q in kp_), "/".join("%.3f" % q[2] for q in kp_), "/".join("%.1f" % q[3] for q in kp_), KAPLIN["gobek"],
           "/".join("%.1f" % q[4] for q in kp_), "/".join("%.1f" % q[5] for q in kp_)),
        all(q[1] < 0.01 and q[2] <= 0.05 and 8.0 <= q[3] <= KAPLIN["gobek"] - 0.5 and q[4] >= 2.0 and q[5] >= 1.5 and q[6] < 0.01 for q in kp_))
    yaz("çakışma istisna listesinde kaplin çifti YOK (v7 ilk: (_kaplini, _motoru) pilota binmeyi gizliyordu)", not [q for q in ISTISNA if "_kaplini" in q[0] or "_kaplini" in q[1]])
    # 8 · ASANSÖR STROKU × yeni / değişen parçalar
    if tam:
        at = asansor_strok_taramasi()
        O["asansor_strok"] = dict(strok=at["strok"], cakisma=len(at["bul"]))
        yaz("asansör stroku 0…%.0f mm (somun üst yatağa değene kadar, %d konum) × v7 yeni / değişen %d parça → çakışma %d" % (at["strok"], at["adim"], at["hedef"], len(at["bul"])),
            not at["bul"], str(sorted(at["bul"].items())[:4]))
    # 9 · HESAPLAR (kaba — iddiaların sayısal dayanağı)
    E_ = 193000.0
    koli_kg = len(ICECEK_X) * ICECEK_KAT * 8.7                                      # VARSAYIM: 24 × 330 ml kutu ≈ 8,4 kg + karton ≈ 8,7 kg/koli
    q_ = koli_kg * 9.81 / ((ICECEK_X[-1][1] - ICECEK_X[0][0]) * (ICECEK_Z[1] - ICECEK_Z[0]))        # N/mm²
    serit = lambda L: (5.0 * q_ * L ** 4 / (384.0 * E_ * 3.0 ** 3 / 12.0), q_ * L ** 2 / 8.0 / (3.0 ** 2 / 6.0))
    d6, s6 = serit(W - 2.0 * SAC); d7, s7 = serit(AYAK_XZ[4][0] - SAC)
    O["taban"] = dict(kg=koli_kg, v6=(d6, s6), v7=(d7, s7))
    print("     HESAP · taban 3 mm (içecek yedeği %.0f kg → %.0f Pa, şerit yaklaşımı · kaba): v6 açıklık %.0f → sehim %.1f mm · σ %.0f MPa  |  v7 orta ayak → açıklık %.0f → %.1f mm · σ %.0f MPa (304 akma ≈ 215)"
          % (koli_kg, q_ * 1e6, W - 2 * SAC, d6, s6, AYAK_XZ[4][0] - SAC, d7, s7))
    m_y = (Y_YIGIN_UST - Y_PLAT) / 1.6 * 0.160 + 10.0
    e_ = abs((ZS0 + ZS1) / 2.0 - (-376.0))
    M_ = m_y * 9.81 * e_
    L_ = 972.0 - (Y_PLINT + 3.0)
    Hk = M_ / L_
    A_, Iu, Iv, cv, cu = _kesit_I(((-382.0, -378.0, 940.0, 972.0), (-404.0, -382.0, 968.0, 972.0)))     # u = z, v = y (köşebent kesiti · v7b: L 4 mm, plakanın arkasında)
    kol_ = 200.0 - SAC + 30.0
    sz = (Hk / 2.0) * kol_ * cu / Iv; sy = (m_y * 9.81 / 2.0) * kol_ * cv / Iu
    O["ray_plakasi"] = dict(kg=m_y, e=e_, M=M_, H=Hk, s_yatay=sz, s_duzey=sy)
    print("     HESAP · ray plakası: yığın + platform %.0f kg · dışmerkezlik %.0f mm → moment %.0f N·m · v7 alt (taban flanşı) + üst (2 köşebent) mesnet: yatay tepki %.0f N ·"
          " köşebent (konsol %.0f) σ yatay %.0f MPa · taban sehim ederse düşey yükün tamamıyla σ %.0f MPa (akma ≈ 215) · v6: plaka havadaydı (mesnetsiz)"
          % (m_y, e_, M_ / 1000.0, Hk, kol_, sz, sy))
    gk = max(kutle[a] for a in KAPI_ADLARI)
    msay = {a: len(MENTESE_Y[a]) for a in KAPI_ADLARI}
    sinir = {a: 6.8 * (msay[a] - 1) for a in KAPI_ADLARI}      # Blum kılavuzu (≤ 900 mm kapak): 2 menteşe < 15 lb (6,8 kg), 3 menteşe < 30 lb (13,6 kg) — okuma VARSAYIM
    print("     HESAP · kanat kütleleri (304 · 7,93 g/cm³): %s · menteşe sayısı / sınır (Blum kılavuzu, ≤ 900 mm): %s"
          % (" · ".join("%s %.1f" % (a[6:], kutle[a]) for a in KAPI_ADLARI), " · ".join("%s %d / %.1f kg" % (a[6:], msay[a], sinir[a]) for a in KAPI_ADLARI)))
    # v7b · ALT kanat burulması (denetim bulgusu 4): alt serbest köşe, en alttaki menteşenin altında L konsol · F köşede (VARSAYIM 20 N: koli / el)
    G_ = 77000.0
    b_k = X_ORTA_DERZ[0] - SAC - TAVA_T                     # kesit orta çizgisi genişliği
    h_k = TAVA - TAVA_T / 2.0 - IC_SAC / 2.0                # ön sac ↔ iç sac orta çizgileri arası
    J_kutu = 4.0 * (b_k * h_k) ** 2 / (b_k / TAVA_T + b_k / IC_SAC + 2.0 * h_k / TAVA_T)     # Bredt (kapalı ince cidar)
    J_acik = (b_k * TAVA_T ** 3 + 2.0 * h_k * TAVA_T ** 3) / 3.0                                # açık tava (v7 ilk)
    L_k = min(MENTESE_Y["onyuz_alt_kanat_sol"]) - 30.0 - Y_ALT[0]
    F_k = 20.0
    dk = F_k * (X_ORTA_DERZ[0] - SAC) ** 2 * L_k / (G_ * J_kutu); da = F_k * (X_ORTA_DERZ[0] - SAC) ** 2 * L_k / (G_ * J_acik)
    O["alt_kanat_burulma"] = dict(J_kutu=J_kutu, J_acik=J_acik, L=L_k, d_kutu=dk, d_acik=da)
    print("     HESAP · ALT kanat burulması: alt serbest köşe en alttaki menteşenin %.0f mm altında · köşede %.0f N (VARSAYIM) → açık tava J %.0f mm⁴: %.1f mm (v7 ilk) ·"
          " kutu kesit J %.0f mm⁴: %.2f mm (v7b) + içe dayama dudağı" % (L_k, F_k, J_acik, da, J_kutu, dk))
    # v7b · şarjör eşiği (denetim bulgusu 3): üst bant iki uçtan köşebentle mesnetli kiriş · yük = 2. blanka üstteki blankın sürtünmesi
    mu_, m_b = 0.5, 0.160                                   # VARSAYIM: karton–karton μ 0,5 · blank 0,16 kg (asansör hesabıyla aynı)
    F_e = mu_ * m_b * 9.81
    L_e = ((X_BL1 - 16.0) - (X_BL0 + 16.0))                 # köşebent bindirmelerinin ortaları arası
    I_e = (Y_KAPI_UST - 944.0) * 3.0 ** 3 / 12.0            # yalnız üst bant (dişler + ayaklar ihmal: güvenli taraf)
    de = 5.0 * F_e * L_e ** 3 / (384.0 * E_ * I_e)
    O["esik"] = dict(F=F_e, L=L_e, I=I_e, d=de)
    print("     HESAP · şarjör eşiği: 2. blanka sürtünme %.2f N (μ %.1f VARSAYIM) · üst bant %.0f × 3 (I %.0f mm⁴) iki köşebent arası %.0f mm yayılı yük → sehim %.2f mm"
          " < 2. blank kenarına pay 0,5 (üst kenar 980,8 yerinde kalır) · v7 ilk: eşik yalnız 3 mm alt kenarıyla tabanda duruyordu (mesnetsiz)" % (F_e, mu_, Y_KAPI_UST - 944.0, I_e, L_e, de))
    A_yuzey = 2.0 * (W * H + (D + Z_ON) * H + W * (D + Z_ON)) * 1e-6
    kayip = 7 * 4.0 + 3 * 10.0 + 3 * 7.0 + 10.0                                    # VARSAYIM: sürücü bekleme 4 W · aynı anda 3 eksen × 10 W · NDR-240 kaybı ~7 W · PLC 10 W
    O["isi"] = dict(W_=kayip, A=A_yuzey, dT=kayip / (5.5 * A_yuzey))
    print("     HESAP · ısı: pano + sürücü kaybı ≈ %.0f W (VARSAYIM) · kabuk yüzeyi %.1f m² × 5,5 W/m²K (doğal taşınım + ışınım, VARSAYIM) → iç sıcaklık artışı ≈ %.1f K"
          " → havalandırma yarığı gerekmez (robot ağzı %.0f × %.0f ayrıca açık)" % (kayip, A_yuzey, kayip / (5.5 * A_yuzey), AGIZ["x"][1] - AGIZ["x"][0], AGIZ["y"][1] - AGIZ["y"][0]))
    yaz("hesap sınırları: taban σ %.0f < 107 (akma/2) · köşebent σ %.0f / %.0f < 107 · kanatlar menteşe sınırında (en ağır %.1f kg) · ΔT %.1f < 10 K · "
        "ALT kanat köşesi %.2f < 0,5 mm · eşik sehimi %.2f < 0,5 mm" % (s7, sz, sy, gk, O["isi"]["dT"], dk, de),
        s7 < 107.0 and sz < 107.0 and sy < 107.0 and all(kutle[a] <= sinir[a] for a in KAPI_ADLARI) and O["isi"]["dT"] < 10.0 and dk < 0.5 and de < 0.5)
    O["denetim_sayisi"] = SAY[0]
    print("OLCUM v7: %d denetim · hepsi GEÇTİ" % SAY[0])
    return O


# ---------------------------------------------------------------- GLB (hiyerarşik düğüm + animasyon) ----------------------------------------------------------------
def _ag(wp, kaba=False):
    import kiyma_cad_v6 as _K
    if kaba:
        from OCP.BRepTools import BRepTools
        sh = wp.val().copy()
        BRepTools.Clean_s(sh.wrapped)
        return _K.ag(cq.Workplane(obj=sh), 0.6, 0.8)
    return _K.ag(wp, 0.3, 0.5)


def glb_yaz(yol, adim=1.0 / 15.0):
    """düğüm başına (grup) malzeme-mesh; blank düğümleri menteşe ağacı; animasyon aynı kinematikten örneklenir"""
    GRUPLAR = ["SABIT", "SABIT_REF", "ASANSOR", "ITICI", "PISTON", "KOPRU", "KATLAYICI", "KOL", "PARMAK", "CATAL", "PIZZA", "K_ITICI"] + list(DUGUM.keys())
    mesh_g = {g: {} for g in GRUPLAR}
    for p in PARCALAR:
        g = p["grup"]
        kaba = p["ad"].startswith(("surucu_", "guc_", "asansor_motoru", "besleyici_motoru", "piston_motoru", "kopru_motoru", "flap_katlayici_motoru", "kol_motoru", "kol_reduktoru", "parmak_motoru", "parmak_reduktoru"))
        m = _ag(p["wp"], kaba)
        mesh_g[g].setdefault(p["mal"], Mesh()).ekle(m)
    # düğüm ağacı
    nodes, idx = [], {}
    def pivot(g):
        if g == "KOL": return (KOL_P[0], KOL_P[1], 0.0)
        if g == "PARMAK": return (PARMAK_P[0], PARMAK_P[1], 0.0)
        if g in DUGUM: return DUGUM[g][1]
        return (0.0, 0.0, 0.0)
    for g in GRUPLAR:
        P = pivot(g)
        par = DUGUM[g][0] if g in DUGUM else None
        Pp = pivot(par) if par else (0.0, 0.0, 0.0)
        n = {"name": g, "translation": [(P[0] - Pp[0]) * MM, (P[1] - Pp[1]) * MM, (P[2] - Pp[2]) * MM]}
        idx[g] = len(nodes); nodes.append(n)
    for g in GRUPLAR:
        if g in DUGUM and DUGUM[g][0]:
            nodes[idx[DUGUM[g][0]]].setdefault("children", []).append(idx[g])
    kok = [idx[g] for g in GRUPLAR if not (g in DUGUM and DUGUM[g][0])]
    # mesh: köşeler düğümün menteşesine göre
    blob, views, accs, meshes, mats, mat_idx = [], [], [], [], [], {}
    off = [0]
    def gomu(bt, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt); return len(views) - 1
    def mat(k):
        if k not in mat_idx:
            d = MALZEME[k]; pbr = {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}
            mm_ = {"name": k, "pbrMetallicRoughness": pbr, "doubleSided": True}
            if d.get("saydam"): mm_["alphaMode"] = "BLEND"
            mat_idx[k] = len(mats); mats.append(mm_)
        return mat_idx[k]
    ucgen = 0
    for g in GRUPLAR:
        if not mesh_g[g]:
            continue
        P = pivot(g)
        prims = []
        for k, m in sorted(mesh_g[g].items()):
            pts = [(q[0] - P[0] * MM, q[1] - P[1] * MM, q[2] - P[2] * MM) for q in m.P]
            vp = gomu(struct.pack("<%df" % (3 * len(pts)), *[c for q in pts for c in q]), 34962)
            vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for q in m.N for c in q]), 34962)
            vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
            mn = [min(q[i] for q in pts) for i in range(3)]; mx = [max(q[i] for q in pts) for i in range(3)]
            accs.append({"bufferView": vp, "componentType": 5126, "count": len(pts), "type": "VEC3", "min": mn, "max": mx})
            accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
            accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
            prims.append({"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": mat(k)})
            ucgen += len(m.I) // 3
        meshes.append({"name": g, "primitives": prims})
        nodes[idx[g]]["mesh"] = len(meshes) - 1
    # animasyon örnekleri
    N = int(round(DONGU / adim)) + 1
    TT = [min(DONGU, i * adim) for i in range(N)]
    sm, ch = [], []
    def kanal(dugum, yol_, degerler, tip):
        ti = gomu(struct.pack("<%df" % len(TT), *TT))
        accs.append({"bufferView": ti, "componentType": 5126, "count": len(TT), "type": "SCALAR", "min": [0.0], "max": [DONGU]})
        n = 4 if tip == "VEC4" else 3
        vo = gomu(struct.pack("<%df" % (n * len(degerler)), *[c for v in degerler for c in v]))
        accs.append({"bufferView": vo, "componentType": 5126, "count": len(degerler), "type": tip})
        sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"})
        ch.append({"sampler": len(sm) - 1, "target": {"node": idx[dugum], "path": yol_}})
    def trs_kanal(g, f):
        P = nodes[idx[g]]["translation"]
        kanal(g, "translation", [(P[0] + f(t)[0] * MM, P[1] + f(t)[1] * MM, P[2] + f(t)[2] * MM) for t in TT], "VEC3")
    trs_kanal("ITICI", lambda t: (0.0, 0.0, itici_dz(t)))
    trs_kanal("PISTON", lambda t: (0.0, kafa(t) - H_UST, 0.0))
    trs_kanal("KOPRU", lambda t: (0.0, kopru_dy(t), 0.0))
    trs_kanal("KATLAYICI", lambda t: (0.0, katlayici_dy(t), 0.0))
    trs_kanal("CATAL", catal_trs)
    trs_kanal("PIZZA", pizza_trs)
    trs_kanal("K_ITICI", k_itici_trs)
    kanal("KOL", "rotation", [quat("z", kol_beta(t)) for t in TT], "VEC4")
    kanal("PARMAK", "rotation", [quat("z", parmak_psi(t)) for t in TT], "VEC4")
    trs_kanal("B_ROOT", lambda t: blank_acilar(t)[0])
    for d in DUGUM:
        if DUGUM[d][0]:
            kanal(d, "rotation", [quat(DUGUM[d][2], blank_acilar(t)[1][d]) for t in TT], "VEC4")
    for g in ("B_ROOT", "PIZZA"):
        kanal(g, "scale", [(max(1e-4, gorunur(t)),) * 3 for t in TT], "VEC3")
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH kutu_cad_v8"}, "scene": 0, "scenes": [{"nodes": kok}], "nodes": nodes, "meshes": meshes,
          "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}],
          "animations": [{"name": "kutu_katlama_dongusu", "samplers": sm, "channels": ch}]}
    js = json.dumps(gl, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    print("GLB: %s · %d KB · %d dugum · %d ucgen · %d anim kanali · %d kare" % (os.path.basename(yol), (len(bb) + len(js)) // 1024, len(nodes), ucgen, len(ch), N))


# ---------------------------------------------------------------- BOM ----------------------------------------------------------------
def _tur(ad):
    return "SATIN ALMA" if any(s in ad for s in ("HIWIN", "AutomationDirect", "SureGear", "Siemens", "Mean Well", "Omron", "Elesa", "TBI", "Bilyalı", "Trapez", "GT3", "Kaplin",
                                                  "Destek B", "KFL", "LM12", "Alüminyum profil", "DIN ray", "Klemens", "Kablo kanalı", "UHMW", "Pizza kutusu", "FR5", "İçecek kolisi",
                                                  "Gizli menteşe", "Bas-aç", "Mesafe burcu")) else "ÜRETİM"


# toplam adedi ilk örnekte yazılmış satın alma kalemlerinin DİĞER örnekleri: BOM.csv'de listelenir, özette sayılmaz
ALT_KURAL = [r"^asansor_vidasi_alt_ucu$", r"^ayak_[1-5]$", r"^kilavuz_(sag|arka)_uhmw$", r"^kalip_ayagi_[1-3]$", r"^kalip_taragi_on_z_[1-3]$",
             r"^kopru_kilavuz_mili_1$", r"^kol_yatagi_1$", r"^parmak_yatagi_1$", r"^asansor_ust_yatak$",
             r"^guc_48V_NDR-240-48_b$", r"^surucu_STP-DRV-4830_[1-6]$", r"^din_rayi_1$", r"^kablo_kanali_(1|dikey_ust)$",
             r"^icecek_yedek_koli_(0[12]|1[012])$"]


def bom_yaz(klasor):
    """BOM.csv = modeldeki her parça · BOM_OZET.csv = kalem bazında TOPLAM (her örnek kendi adedini taşır, toplanır)"""
    import re as _re
    os.makedirs(klasor, exist_ok=True)
    satir = []
    for p in PARCALAR:
        if p["grup"] in ("PIZZA", "K_ITICI", "SABIT_REF", "CATAL") or p["grup"].startswith("B_"):
            continue
        if any(_re.search(k, p["ad"]) for k in ALT_KURAL):
            satir.append((p["ad"], p["ad"].replace("_", " "), 0, "", "aynı kalemin eşi — adet ilk örnekte", "ALT")); continue
        if p["bom"]:
            ad, adet, tanim, not_ = p["bom"]
            if adet == 0 and not tanim:
                satir.append((p["ad"], ad, 0, "", "aynı kalemin eşi (adet ana satırda)", "ALT")); continue
            satir.append((p["ad"], ad, adet, tanim, not_, _tur(ad)))
        else:
            bb = p["wp"].val().BoundingBox()
            tanim = {"sac": "304 sac · lazer + büküm", "kabuk": "304 sac 1,5 · lazer + büküm (dış kabuk)", "aluminyum": "alüminyum 6082 · CNC",
                     "celik": "304 / S235 · lazer / torna", "uhmw": "UHMW-PE", "plastik": "", "motor": "", "kart": "", "karton_yigin": ""}.get(p["mal"], p["mal"])
            satir.append((p["ad"], p["ad"].replace("_", " "), 1, tanim, "zarf %.1f × %.1f × %.1f" % (bb.xlen, bb.ylen, bb.zlen), "ÜRETİM"))
    with io.open(os.path.join(klasor, "BOM.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["parça (model adı)", "kalem", "adet", "tanım / ürün", "not / ölçü", "tür"])
        for r in satir:
            w.writerow(r)
    top, bil = {}, {}
    for pad, ad, adet, tanim, not_, tur in satir:
        if tur == "ALT":
            continue
        top[ad] = top.get(ad, 0) + int(adet)
        bil.setdefault(ad, (tanim, not_, tur))
    with io.open(os.path.join(klasor, "BOM_OZET.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["tür", "kalem", "toplam adet", "tanım / ürün", "not / kaynak"])
        for k in sorted(top, key=lambda a: (0 if bil[a][2] == "SATIN ALMA" else 1, a)):
            w.writerow([bil[k][2], k, top[k], bil[k][0], bil[k][1]])
    sa = sum(1 for k in top if bil[k][2] == "SATIN ALMA")
    print("BOM: %d parca satiri · %d kalem (%d satin alma · %d uretim)" % (len(satir), len(top), sa, len(top) - sa))
    for k in sorted(top):
        if bil[k][2] == "SATIN ALMA":
            print("   %4d  %s" % (top[k], k))


# ---------------------------------------------------------------- MODÜL ----------------------------------------------------------------
def modul():
    PARCALAR[:] = []
    govde(); onyuz(); sarjor(); besleyici(); kalip(); kopru(); piston(); parmak(); kapak_mekanizmasi(); elektrik(); icecek_yedegi(); blank(); catal_pizza()
    return PARCALAR


# v10 — positive-drive tooling. All tool transforms and cardboard transforms
# share the same cycle. This is a dimensional prototype, NOT a tested die line.
MALZEME.setdefault('bronz',dict(renk=(0.64,0.43,0.18,1.0),met=0.8,ruf=0.35))
V10_U_PAUSE = 12.0
V10_PAUSE = Z_ZIMBA[0] + (Z_ZIMBA[1]-Z_ZIMBA[0])*V10_U_PAUSE/U_MAX
V10_DELAY = 3.0
V10_SIDE = _ray_uzeri(V10_U_PAUSE, KALIP, 2.1)
V10_FOLD = (3.0, 3.7)
V10_LIFT = (4.0, 4.5)
V10_RETURN = (4.7, 5.3)
V10_TOOL_STROKE = 38.0
_v9_u = u_zimba
_v9_blank = blank_acilar
_v9_parmak = parmak
_v9_piston = piston
_v9_kapak = kapak_mekanizmasi
_v9_grup = grup_matrisi
_v9_blank_make = blank
_v9_govde = govde
_v9_besleyici = besleyici
_v9_elektrik = elektrik
_v9_modul = modul
for _v10_name in ('Z_ZIMBA','Z_KALK1','Z_PARMAK','Z_VURUS2','Z_KOPRU','Z_FLAP','Z_KOL','Z_PIZZA',
                  'Z_KITICI_DON','Z_KAFA_HAZIR','Z_YATIR','Z_KAPAT','Z_KOL_DON','Z_CATAL','Z_GIZLE'):
    globals()[_v10_name] = tuple(v + V10_DELAY if v >= 3.3 else v for v in globals()[_v10_name])
DONGU += V10_DELAY
KONTROL_ANLARI = tuple(i/10 for i in range(int(DONGU*10)+1))
GECIS_ANLARI = tuple(t+3 if t>=3.3 else t for t in GECIS_ANLARI) + tuple(2.85+i*.15 for i in range(24))
PIZZA_ANLARI = tuple(t+3 for t in PIZZA_ANLARI)

def u_zimba(t):
    if t < V10_PAUSE: return U_MAX*lin(2.7,3.3,t)
    if t < V10_PAUSE+V10_DELAY: return V10_U_PAUSE
    return U_MAX*lin(2.7,3.3,t-V10_DELAY)

_v9_kafa = kafa
def kafa(t):
    if Z_ZIMBA[0] <= t < Z_ZIMBA[1]: return YB+T-u_zimba(t)
    if 6.3 <= t < 7.1: return (YB+T-U_MAX)+45*(ss(6.3,6.55,t)-ss(6.85,7.1,t))
    if 7.1 <= t < 8.2: return YB+T-U_MAX
    if 8.2 <= t < 8.7: return (YB+T-U_MAX)+(H_UST-(YB+T-U_MAX))*ss(8.2,8.7,t)
    if Z_VURUS2[0] <= t < Z_VURUS2[3]: return H_UST  # 180-degree positive tuck replaces blind second punch
    return _v9_kafa(t)

def corner_angle(t):
    return -15+15*ss(V10_PAUSE,3.0,t)+90*ss(*V10_FOLD,t)-105*ss(*V10_RETURN,t)

def corner_lift(t):
    # 38 mm clears the upright carton while forming. At the top of the press
    # stroke, use 60 mm for the tucker's 180-degree reset quadrant. Lower back
    # to 38 mm at tucker=0 before it parks at -90; then return home.
    return (V10_TOOL_STROKE*ss(*V10_LIFT,t)
            +22*(ss(8.75,9.05,t)-ss(9.5,9.75,t))
            -V10_TOOL_STROKE*ss(10.25,10.55,t))

def _v10_add(a,b): return tuple(a[i]+b[i] for i in range(3))
def _v10_mul(v,s): return tuple(x*s for x in v)
def _v10_point(M,p): return tuple(sum(M[i][j]*p[j] for j in range(3))+M[i][3] for i in range(3))
def _v10_place(wp,ex,ey,P): return cq.Workplane(obj=yerles(wp.val(),ex,ey,P))
def _v10_faceplace(wp,ex,ey,out,P):
    ez=capraz(ex,ey)
    if sum(ez[i]*out[i] for i in range(3))<0: wp=wp.mirror('XY')
    return _v10_place(wp,ex,ey,P)

def govde():
    _v9_govde()
    p=next(p for p in PARCALAR if p['ad']=='agiz_ust_kirisi')
    p['wp']=p['wp'].translate((0,0,69))  # z29..49, ahead of tool bearings ending at z28
    p['wp']=p['wp'].intersect(kut(SAC+20,W-SAC-20,1161,1178,28,50))  # butt joints to front posts, no overlapping solids

def besleyici():
    _v9_besleyici()
    p=next(p for p in PARCALAR if p['ad']=='besleyici_plakasi')
    for x0,x1 in ((67,134),(385,454)):
        p['wp']=p['wp'].cut(kut(x0,x1,1331,1338,-412,-317))

# Corner tool axes are aligned with the actual corner crease at the dwell,
# not with an arbitrary vertical axis. Shaft ends ABOVE the cardboard.
CORNER = {}
for _code,_sx,_sz in (('MF',-1,-1),('MB',1,-1),('PF',-1,1),('PB',1,1)):
    _theta = -_sz*V10_SIDE
    _R = rot4('x',_theta)
    _axis = _v10_point(_R,(0,0,_sz))
    _pivot = (BX0+T if _sx<0 else BX1-T, H_UST, BZ0 if _sz<0 else BZ1)
    CORNER['CNR_'+_code] = dict(P=_pivot,axis=_axis,sign=_sx*_sz,side=_sz,end=_sx,theta=_theta)

def corner_quat(g,t):
    a=math.radians(CORNER[g]['sign']*corner_angle(t))/2
    return tuple(x*math.sin(a) for x in CORNER[g]['axis'])+(math.cos(a),)

def corner_translation(t): return (0,kafa(t)-H_UST+corner_lift(t),0)

def _axis_rotation(axis,angle):
    x,y,z=axis; a=math.radians(angle); c=math.cos(a); s=math.sin(a); q=1-c
    return [[c+x*x*q,x*y*q-z*s,x*z*q+y*s,0],
            [y*x*q+z*s,c+y*y*q,y*z*q-x*s,0],
            [z*x*q-y*s,z*y*q+x*s,c+z*z*q,0],[0,0,0,1]]

def corner_tools():
    y=H_UST
    # Motorised common lift: keep fingers at 90, withdraw 38 mm, THEN reset.
    # At the bottom stroke the hub starts at 46+38=84 mm above the head:
    # clears the still-upright double front wall (42+40=82) by nominal 2 mm.
    bridge=kut(16,444,y+180,y+186,-222,-190)
    for x in (196,316):bridge=bridge.union(kut(x,x+8,y+76,y+180,-222,-190))
    ekle('kose_takim_sabit_kopru',bridge,'aluminyum','PISTON')
    frame=kut(16,444,y+84,y+90,-371,-15).cut(kut(76,413,y+83,y+91,-344,-68))
    frame=frame.cut(kut(132,387,y+83,y+91,-398,-348))
    # Front spindle and return strap pass through this relieved tooling window.
    # The corner bearing seat remains on x90..118, z-68..-35.
    frame=frame.cut(kut(75,135,y+83,y+91,-35,-14))
    frame=frame.cut(kut(77,87,y+83,y+91,-69,-14))
    # Rib behind the punch: stiffens the remaining rear cross-tie in bending.
    frame=frame.union(kut(76,413,y+90,y+112,-348,-344))
    for x in (30,436): frame=frame.cut(sily(x,-206,10.6,y+80,y+95))
    for x in (230,286): frame=frame.cut(kut(x-1,x+5,y+83,y+91,-17,-4))
    for c in CORNER.values():
        frame=frame.cut(_v10_place(sily(0,0,8.2,45,125),(1,0,0),c['axis'],c['P']))
    frame=frame.cut(sily(260,-35,7.1,y+80,y+95))
    ekle('kose_takim_hareketli_cerceve',frame,'aluminyum','CNR_LIFT')
    for i,x in enumerate((30,436)):
        ekle('kose_takim_kilavuz_%d'%i,sily(x,-206,6,y+66,y+210),'celik','PISTON')
        ekle('kose_takim_burc_%d'%i,boru_y(x,-206,10.5,6.1,y+66,y+96),'celik','CNR_LIFT')
        ekle('kose_takim_burc_govde_%d'%i,kut(x-14,x+14,y+64,y+97,-220,-192).cut(sily(x,-206,10.5,y+63,y+98)),'aluminyum','CNR_LIFT')
    ekle('kose_takim_vida',sily(260,-35,4,y+42,y+200),'celik','PISTON')
    ekle('kose_takim_somun',boru_y(260,-35,10,4.1,y+90,y+115),'bronz','CNR_LIFT')
    ekle('kose_takim_vida_yatagi',boru_y(260,-35,11,4.1,y+178,y+188),'celik','PISTON')
    ekle('kose_takim_vida_yatak_govdesi',kut(230,290,y+178,y+188,-55,-5).cut(sily(260,-35,11,y+177,y+189)),'aluminyum','PISTON')
    ekle('kose_takim_vida_kaplini',boru_y(260,-35,8,3.2,y+196,y+222).cut(sily(260,-35,4.05,y+195,y+202)),'aluminyum','PISTON')
    nema23('kose_takim_kaldirma_motoru',(260,y+230,-35),(0,-1,0),(0,0,1),'PISTON')
    ekle('kose_takim_motor_plakasi',kut(230,290,y+224,y+230,-65,-5).cut(sily(260,-35,20,y+223,y+231)),'aluminyum','PISTON')
    feet=kut(196,324,y+70,y+76,-206,-190)
    for x in (230,286):
        feet=feet.union(kut(x,x+4,y+76,y+224,-16,-7)).union(kut(x,x+4,y+70,y+76,-206,-7))
    ekle('kose_takim_motor_ayaklari',feet,'aluminyum','PISTON')
    for g,c in CORNER.items():
        P=c['P']; axis=c['axis']; ex=(c['end'],0,0); normal=(0,-math.cos(math.radians(c['theta'])),-math.sin(math.radians(c['theta'])))
        # Local coordinates: X = distance from crease; Y = along crease;
        # Z = outward from paper. Flat contact shoe touches the panel's outer face.
        M=eksen_matrisi(ex,axis,normal,P)
        shoe=kut(25,35,10,33,1.6,3.6)
        stem=kut(29,35,33,50,1.6,5.6).union(kut(-4,35,46,50,1.6,5.6))
        ekle('kose_'+g+'_temas_pabucu',_v10_faceplace(shoe,ex,axis,normal,P),'uhmw',g)
        ekle('kose_'+g+'_katlama_kolu',_v10_faceplace(stem,ex,axis,normal,P),'sac',g)
        # shaft and keyed radial hub; no full shaft passes through the carton.
        ekle('kose_'+g+'_mil',_v10_place(sily(0,0,4,44,92),ex,axis,P),'celik',g)
        hub=boru_y(0,0,8,4.0,46,53)
        ekle('kose_'+g+'_gobek',_v10_place(hub,ex,axis,P),'celik',g)
        for j,h in enumerate((61,77)):
            ekle('kose_'+g+'_rulman_'+str(j),_v10_place(boru_y(0,0,11,4.05,h,h+7),ex,axis,P),'celik','CNR_LIFT')
        housing=kut(-16,16,58,87,-16,16).cut(sily(0,0,4.1,57,88))
        for h in (61,77): housing=housing.cut(sily(0,0,11, h,h+7))
        ekle('kose_'+g+'_yatak_govdesi',_v10_place(housing,ex,axis,P),'aluminyum','CNR_LIFT')
        nema23('kose_'+g+'_motor',_v10_add(P,_v10_mul(axis,116)),_v10_mul(axis,-1),(1,0,0),'CNR_LIFT')
        cp=sily(0,0,8,88,114.4).cut(sily(0,0,4.05,87,94)).cut(sily(0,0,3.2,94,115))
        ekle('kose_'+g+'_kaplin',_v10_place(cp,ex,axis,P),'aluminyum',g)
        mount=kut(-30,30,110,116,-30,30).cut(sily(0,0,20,109,117))
        mount=mount.union(kut(-30,-24,84,110,-30,30)).union(kut(24,30,84,110,-30,30))
        ekle('kose_'+g+'_motor_kelepcesi',_v10_place(mount,ex,axis,P),'aluminyum','CNR_LIFT')

# The front panel folds about its SCORE. A one-sided double-bearing shaft
# leaves the rear feeding path unobstructed. Belt motor stays below the tray.
PARMAK_P=(BX0+T/2,TEPSI+T+H_ON)
PARMAK_R=38.0
def parmak_psi(t):
    return -90*(1-ss(6.55,6.85,t)+ss(9.8,10.2,t))-180*(ss(7.2,8.0,t)-ss(9.15,9.5,t))

def front_dy(t): return 100*(1-ss(6.4,6.8,t)+ss(9.5,9.8,t))
Z_KOPRU=(9.9,10.3,Z_KOPRU[2],Z_KOPRU[3])


def piston():
    _v9_piston()
    p=next(p for p in PARCALAR if p['ad']=='piston_kafasi')
    # Relieve the FULL width of the inner front flap, not only the central
    # tucker paddle. Its two end regions also sweep over the press head.
    p['wp']=p['wp'].cut(kut(111,147,H_UST-1,H_UST+21,PK_Z[0]-1,PK_Z[1]+1))
    p['bom']=("Piston kafası 6082 · ön kenar x147; 261 × 296 × 20",1,
              "ön iç duvar tam genişlik süpürmesine açık; fiziksel karton testi bekleniyor","üretim prototipi")
    corner_tools()

def kapak_mekanizmasi():
    _v9_kapak()
    for p in PARCALAR:
        if p['ad']=='flap_katlayici_somun_kolu': p['wp']=p['wp'].cut(sily(775,-330,6.2,889,901))
    # U frame is a LINEAR folder, not three hingeless rotating metal leaves.
    # Existing SFU16 motor drives a nut + carriage, now on two explicit guides.
    for i,z in enumerate((-330,-75)):
        ekle('flap_kilavuz_mili_'+str(i),sily(775,z,6,838,974),'celik')
        for j,y in enumerate((832,974)):
            ekle('flap_kilavuz_kelepce_%d%d'%(i,j),kut(763,787,y,y+6,z-12,z+12).cut(sily(775,z,6.1,y-1,y+7)),'aluminyum')
        ekle('flap_kilavuz_diregi_'+str(i),kut(792,798,832,980,z-12,z+12).union(kut(775,798,974,980,z-12,z+12)),'aluminyum')
        ekle('flap_lineer_burc_'+str(i),boru_y(775,z,10.5,6.1,900,930),'celik','KATLAYICI')
        ekle('flap_lineer_burc_govdesi_'+str(i),kut(760,790,897,933,z-15,z+15).cut(sily(775,z,10.5,896,934)),'aluminyum','KATLAYICI')
        ekle('flap_burc_baglantisi_'+str(i),kut(739,760,890,900,z-15,z+15),'aluminyum','KATLAYICI')
    ekle('flap_vida_alt_islenmis_uc',sily(750,-300,5,710,732),'celik')
    ekle('flap_vida_alt_rulmani',boru_y(750,-300,13,5.05,724,732),'celik')

def blank_acilar(t):
    root,A=_v9_blank(t)
    # Explicit 90 degree corner tools at the 12 mm dwell, not magic angles.
    a=90*ss(*V10_FOLD,t)
    A.update(B_CTMF=-a,B_CTPF=-a,B_CTMB=a,B_CTPB=a)
    # Front die captures the external wall before the double-wall tool starts.
    f=max(-A['B_FO'],90*ss(32,U_MAX,u_zimba(t)))
    A['B_FO']=-f
    A['B_FI']=-180*ss(7.2,8.0,t)
    return root,A

def grup_matrisi(g,t):
    if g=='FRONT_Y': return tr4((0,front_dy(t),0))
    if g=='PARMAK': return mm4(tr4((0,front_dy(t),0)),_v9_grup(g,t))
    if g=='CNR_LIFT': return tr4(corner_translation(t))
    if g in CORNER:
        c=CORNER[g]; P=c['P']
        return mm4(tr4(_v10_add(P,corner_translation(t))),mm4(_axis_rotation(c['axis'],c['sign']*corner_angle(t)),tr4(_v10_mul(P,-1))))
    return _v9_grup(g,t)

HAREKETLI=HAREKETLI+('CNR_LIFT','FRONT_Y')+tuple(CORNER)

# Final front-fold architecture: no separate vertical stage. The existing
# press carries the tucker, stays down during folding, then withdraws upward.
PARMAK_P=(BX0+T/2,H_UST+42)
def front_dy(t):return kafa(t)-H_UST
def parmak():
    x,y=PARMAK_P
    paddle=kut(x-7.4,x-4.4,y+6,y+37,-305,-107).union(kut(x-56,x-52,y-22,y-18,-305,-20))
    for zz in (-290,-130):
        paddle=paddle.union(kut(x-56,x-52,y-22,y+8,zz,zz+10)).union(kut(x-56,x-4.4,y+5,y+8,zz,zz+10))
    ekle('devirme_parmagi',paddle,'sac','PARMAK')
    ekle('parmak_temasi_UHMW',kut(x-4.4,x-2.4,y+6,y+33,-305,-107),'uhmw','PARMAK')
    ekle('parmak_tahrik_yan_kolu',kut(x-56,x+6,y-22,y+6,-24,-20).union(silz(x,y,10,-24,-18)),'celik','PARMAK')
    ekle('parmak_mili',silz(x,y,6,-24,28),'celik','PARMAK')
    for i,z in enumerate((-3,20)):
        ekle('parmak_yatagi_'+str(i),silz(x,y,14,z,z+8).cut(silz(x,y,6.05,z-1,z+9)),'celik','FRONT_Y')
        ekle('parmak_yatak_ayagi_'+str(i),kut(x-20,x+20,y-18,y+18,z-4,z+8).cut(silz(x,y,14,z-5,z+9)),'aluminyum','FRONT_Y')
    mx,my=340,H_UST+200
    for ad,xx,yy in (('ust',x,y),('alt',mx,my)):
        ekle('parmak_kasnak_'+ad,silz(xx,yy,10,7,18).cut(silz(xx,yy,3.2 if ad=='alt' else 6,6,19)),'aluminyum','PARMAK' if ad=='ust' else 'FRONT_Y')
    dx=x-mx;dy=y-my;ll=math.hypot(dx,dy);nx=-dy/ll;ny=dx/ll
    def capsule(r,z0,z1):
        xy=[(mx+nx*r,my+ny*r),(x+nx*r,y+ny*r),(x-nx*r,y-ny*r),(mx-nx*r,my-ny*r)]
        return cq.Workplane('XY').polyline(xy).close().extrude(z1-z0).translate((0,0,z0)).union(silz(mx,my,r,z0,z1)).union(silz(x,y,r,z0,z1))
    ekle('parmak_kayisi',capsule(12,8,17).cut(capsule(10,7,18)),'kayis','FRONT_Y')
    nema23('parmak_motoru',(mx,my,-5),(0,0,1),(0,1,0),'FRONT_Y')
    mount=kut(mx-31,mx+31,my-31,my+31,-5,1).cut(silz(mx,my,20,-6,2))
    mount=mount.union(kut(mx+31,mx+37,H_UST+70,my+31,-5,1))
    mount=mount.union(kut(316,mx+37,H_UST+70,H_UST+76,-160,1))
    ekle('parmak_motor_braketi',mount,'aluminyum','FRONT_Y')
    holder=kut(x-20,x+20,y+18,H_UST+96,0,27)
    holder=holder.union(kut(x-20,204,H_UST+90,H_UST+96,0,27))
    holder=holder.union(kut(196,204,H_UST+70,H_UST+90,0,27)).union(kut(196,204,H_UST+70,H_UST+76,-160,27))
    channel=capsule(13,6,19)
    ekle('parmak_piston_baglantisi',holder.cut(channel),'aluminyum','FRONT_Y')
    for p in PARCALAR:
        if p['ad'].startswith('parmak_yatak_ayagi_'):p['wp']=p['wp'].cut(channel)
    # Last bearing/shaft face is z=28, holder z=27: remain behind the z=29
    # cabinet cross-member throughout the complete vertical head stroke.

def elektrik():
    _v9_elektrik()
    p=next(p for p in PARCALAR if p['ad']=='klemens_sirasi')
    p['wp']=p['wp'].translate((0,-65,0))
    ekle('din_rayi_ek_klemens',kut(450,770,1632,1667,-822,-815),'celik')
    for i in range(7,12):
        ekle('surucu_STP-DRV-4830_%d'%i,TC.din_parca(TC.SURUCU_STEP,90+50*i,1687,-787),'kart')
    # Never imply that enable multiplexing turns four PTO channels into thirteen
    # independently controlled holding axes. Controller/I-O selection is OPEN.
    p=next(p for p in PARCALAR if p['ad']=='plc_S7-1200_1214C')
    p['bom']=("S7-1200 supervisory PLC; motion expansion REQUIRED",1,"12 independent motor drivers; PTO/fieldbus hardware not selected", "not an approved wiring design")

def modul():
    result=_v9_modul()
    p={p['ad']:p for p in PARCALAR}
    def pocket(a,b):p[a]['wp']=p[a]['wp'].cut(p[b]['wp'])
    # Actual fitted pockets, not collision exclusions. These leave mating faces.
    for i in range(2):
        pocket('kose_takim_sabit_kopru','kose_takim_kilavuz_'+str(i))
        pocket('kose_takim_hareketli_cerceve','kose_takim_burc_govde_'+str(i))
        pocket('flap_kilavuz_diregi_'+str(i),'flap_kilavuz_kelepce_'+str(i)+'1')
        for mate in ('flap_katlayici_alt_bagi','flap_katlayici_somun_kolu'):
            pocket('flap_burc_baglantisi_'+str(i),mate)
    pocket('kose_takim_vida_yatak_govdesi','kose_takim_motor_ayaklari')
    for g in CORNER:
        for suffix in ('rulman_1','yatak_govdesi','motor_kelepcesi'):
            pocket('kose_takim_hareketli_cerceve','kose_'+g+'_'+suffix)
        pocket('kose_'+g+'_katlama_kolu','kose_'+g+'_gobek')
        pocket('kose_'+g+'_katlama_kolu','kose_'+g+'_mil')
    pocket('devirme_parmagi','parmak_tahrik_yan_kolu')
    pocket('parmak_tahrik_yan_kolu','parmak_mili')
    pocket('parmak_motor_braketi','piston_kaburgasi_0')
    pocket('parmak_motor_braketi','parmak_piston_baglantisi')
    for i in range(2):
        pocket('parmak_piston_baglantisi','parmak_yatak_ayagi_'+str(i))
        pocket('parmak_piston_baglantisi','parmak_yatagi_'+str(i))
    pocket('flap_lineer_burc_govdesi_0','flap_katlayici_somun_kolu')
    p['flap_katlayici_kaplini']['wp']=p['flap_katlayici_kaplini']['wp'].cut(sily(750,-300,5.05,709,723))
    p['flap_katlayici_yatak_braketi']['wp']=p['flap_katlayici_yatak_braketi']['wp'].cut(sily(750,-300,13,723,733))
    return result

if __name__ == "__main__":
    import runpy
    runpy.run_path(os.path.join(U, "kutu_v10_check.py"), run_name="__main__")
