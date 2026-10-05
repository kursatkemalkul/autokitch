# -*- coding: utf-8 -*-
"""HAT VERSİYON 2 · ÜST DEPO (modül U) v1 (30 Eyl 2026 · Claude · YEREL) — A, F, K, E istasyonlarının ÜSTÜ (y 1862 → 2200) üç KAPALI kutu.
Kemal: "yukarıda boş alanlar olduğu için içecek yedekleri gibi şeyleri yukarı taşıyabilirsin" · "her istasyon kendi başına kapalı ürün, lego birleşim" ·
"simetri ve çok basit görünüm". v2'de TOPPING iki katlı → makine üstü 2200 (h3_hesap_v1.H_UST); A / F / K / E gövdeleri 1862'de kalır → üstlerinde 338 mm bant.

KUTULAR (dünya · her biri kendi tabanı + tavanı + yanları + arkası + ön kapakları olan AYRI ürün):
  U_A  x 507,5–1207,5 (açıcı üstü)      · 1 düşer kapak 507,5–1206 (A servis kapağıyla aynı hiza) · BOŞ yedek depo
  U_F  x 2500–4000 (fırın üstü)         · 2 düşer kapak 2500–3248,5 / 3251,5–4000 (fırın üstü kabin kapaklarıyla aynı hiza) · BOŞ yedek depo ·
                                          fırın davlumbaz ATIŞ KANALI 300 × 200 içinden geçer (1862 → 2200) + bina egzozu bağlantı flanşı (üst sacın altında)
  U_KE x 4000–5230 (kesme + kutu üstü)  · 2 EŞİT düşer kapak 4003–4615 / 4618–5230 · İÇECEK YEDEĞİ 6 koli (3 yan yana × 2 sıra, 400 × 267 × 123, 24 kutu) = 144
                                          raf (1,5) + 4 taşıyıcı profil üstünde · dolaptaki 144 ile 288 ≥ 4 gün 277 (h3_hesap_v1)
  TOPPING (1207,5–2500) zaten 2200'e çıkıyor — ÖRTÜLMEZ; kutular ona yalnız yan saclarıyla değer.
YAPI (firin_ust_kabin_cad_v1 ile aynı dil): 304 fırçalı 1,5 · üst sac 430 1,5 (3 kenarı 20 aşağı bükülü) · yan saclar 15 mm ön + arka iç bükümlü · tek parça arka sac ·
  ÖN: alt kayıt 30 × 30 × 2 (düşer kapak menteşelerinin sabit yaprakları) + üst kayıt 30 × 30 × 2 (tavanın ön kenarı) · tavan kirişleri 30 × 30 × 2 (z boyunca) ·
  KAPAK: tava 20 (z +59…+79) · derz 3 · ALTTAN MENTEŞELİ DÜŞER KAPAK (Sugatsune SDH-001 · kanat başına 2 · pivot alt ön kenar y 1862, z +79) · Blum TIP-ON 956.1004
  bas-aç + karşı plaka · kulp / vida / menteşe önden görünmez · kapak içinde alt bantta 1,0 C kutu (menteşe hareketli yaprakları buna).
  Fırın üstü kabinden FARKI: çekme gazlı yay YOK — kapak 335 yüksek, 90°'deki ağırlık momenti 4,7–5,8 N·m (aşağıda hesap); yan şeritler U_KE'de kolilerle dolu
  (3 × 400 = 1200 / iç 1227) → yay yeri yok. Yavaş iniş: sönümlü düşer kapak menteşesi — kapasite üreticiyle (AÇIK).
ÜST ÇİZGİ: bütün kutuların üstü 2200,0 (TOPPING dış tavanı 2198,5–2200) · kapak üstleri 2197 (TOPPING soğuk kapaklarıyla aynı) · kapak altları 1862 (alttaki
  istasyon kapaklarının üstü 1859 → derz 3). 2200'ün üstünde HİÇBİR parça yok (baca flanşı üst sacın altında; bina kanalı üstten flanşa cıvatalanır).
Sözleşme (firin_ust_kabin_cad_v1 / bulasik_cad_v2): kur() İDEMPOTENT · PARCALAR [dict(ad, wp, mal, birim, grup, kaynak, bom)] · dunya(p) · BIRIMLER · BIRIM_MODUL {kod: "U"} ·
  Z_ON = 79 · + ICECEK_YEDEK · KAPAK_EKSEN · ac(sh, aci) · MALZEME. Parçalar DÜNYA koordinatında.
MONTAJ: import h3_ust_depo_v1 as UD · UD.kur() · _dis_birim(UD, "GERCEK_UST_DEPO", "h3_ust_depo_v1.py", …) · GERCEK_DIS["GERCEK_UST_DEPO"] = UD · UD.MALZEME kaydı ·
  içecek sözleşmesi / kapasitesi UD.ICECEK_YEDEK["kutu"] = 144 (KC.ICECEK_YEDEK artık 0) · U_ICECEK_YEDEK ürün sınıfına.
AÇIK: sönümlü düşer kapak menteşesi (kanat momenti 90°'de 4,8–5,8 N·m) · U_KE'nin 2 eşit kapağı (612) alttaki K|E çizgisiyle hizalı değil (seçenek: 395,5 / 413 / 412,5
  üç kapak, eşit değil — Kemal) · U_KE yükü (52 kg koli + kutu) K ve E tavanlarına biner; E tavanı 1,5 kabuk (besleyici / piston askıları ona asılı) → taşıyıcı ayrıntı ·
  bina egzozu flanş bağlantı ayrıntısı (conta, delik düzeni).
Çalıştır (öz denetim): python ob_calistir.py h2/h3_ust_depo_v1.py   (TOPPING sınır denetimini atlamak: --topping-yok)
"""
import math, os, sys, time

H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_hesap_v1 as HS

V = cq.Vector
# ================================================================ ÖLÇÜLER (dünya) ================================================================
H_IST, H_UST = HS.H_IST, HS.H_UST              # 1862 · 2200
Z_ON = 79.0                                    # ön düzlem (fırın gövdesinin ön yüzü · bütün istasyonlarla aynı)
TAVA = 20.0
Z_TAVA = Z_ON - TAVA                           # +59 · gövde sacları burada biter
SAC, SAC_IC = 1.5, 1.0
Z_ARKA = -830.0
Z_ARKA_IC = Z_ARKA + SAC                       # −828,5
DERZ = 3.0
FLANS = 15.0                                   # yan sac ön / arka iç bükümü
Y_TABAN = (H_IST, H_IST + SAC)                 # 1862–1863,5 taban sacı (istasyon tavanlarının üstünde)
Y_TAVAN = (H_UST - SAC, H_UST)                 # 2198,5–2200 üst sac (430)
BUKUM = 20.0                                   # üst sacın aşağı bükümü
KAPAK_Y = (H_IST, H_UST - DERZ)                # 1862–2197 · alttaki kapakların üstü 1859 → derz 3 · TOPPING soğuk kapak üstü 2197
PIVOT = (KAPAK_Y[0], Z_ON)                     # düşer kapak ekseni: alt ön kenar (x boyunca)
ACI_ACIK = 90.0
PROFIL = 30.0                                  # 30 × 30 × 2 kutu profil
KAYIT_Z = (Z_TAVA - 32.0, Z_TAVA - 2.0)        # +27…+57 (fırın üstü kabin KAYIT ile aynı)
ALT_KAYIT_Y = (Y_TABAN[1], Y_TABAN[1] + PROFIL)            # 1863,5–1893,5
UST_KAYIT_Y = (Y_TAVAN[0] - PROFIL, Y_TAVAN[0])            # 2168,5–2198,5
KUTU_Y = (KAPAK_Y[0] + SAC, 1905.0)            # kapak içindeki C kutu (alt bant) · menteşe hareketli yaprağı sırtına
KUTU_Z = (Z_TAVA + SAC, Z_ON - SAC)            # 60,5 · 77,5
MENTESE_DX = 130.0
MENTESE_Y = (KAPAK_Y[0] + 4.0, KAPAK_Y[0] + 30.0)          # 1866–1892 (fırın üstü kabinde 1308 + 2,5 … + 28,5)
TIPON_Y = (2130.0, 2150.0)                     # bas-aç (üst kayıtın 18,5 altı · kolilerin 112 üstü)
RO = 7.93e-6                                   # kg/mm³ 304
KUTULAR = [
    dict(kod="A", birim="U_A_GOVDE", x=HS.A_X, kapak=[(HS.A_X[0], HS.A_X[1] - SAC)], kiris=[(842.5, 872.5)], tipon="iki",
         ad="Üst depo A (açıcı üstü)", bos=True),
    dict(kod="F", birim="U_F_GOVDE", x=HS.F_X, kapak=[(HS.F_X[0], (HS.F_X[0] + HS.F_X[1]) / 2.0 - DERZ / 2.0), ((HS.F_X[0] + HS.F_X[1]) / 2.0 + DERZ / 2.0, HS.F_X[1])],
         kiris=[(2785.0, 2815.0), (3485.0, 3515.0)], tipon="dis", ad="Üst depo F (fırın üstü)", bos=True),
    dict(kod="KE", birim="U_KE_GOVDE", x=(HS.K_X[0], HS.E_X[1]), kapak=None, kiris=[(4385.0, 4415.0), (4800.0, 4830.0)], tipon="dis",
         ad="Üst depo K + E (kesme + kutu üstü)", bos=False),
]
_ke = KUTULAR[2]; _a0 = _ke["x"][0] + DERZ
_ke["kapak"] = [(_a0, HS.E_X[0] - DERZ / 2.0), (HS.E_X[0] + DERZ / 2.0, _ke["x"][1])]   # v2 (Claude): K|E çizgisine HİZALI 4003–4398,5 · 4401,5–5230 (Kemal: hizalı ön çizgiler; U_A / U_F de alttakilerle hizalı) · ikisi açıkken ön tam açık
# fırın davlumbaz atış kanalı (firin_ust_kabin_cad_v1.ATIS: x 2950–3250 · z −720…−520 · üst sacı 1860,5–1862, açıklığı kanal iç ölçüsü)
ATIS = (2950.0, 3250.0, -720.0, -520.0)
BACA_FLANS = 30.0                              # bağlantı flanşı genişliği (kanal dış yüzünden)
BACA_FLANS_T = 3.0
# içecek yedeği (U_KE)
KOLI = dict(x=HS.KOLI["x"], z=HS.KOLI["z"], y=HS.KOLI["y"], adet=HS.KOLI["adet"], kg=8.7)       # 400 × 267 × 123 · 24 kutu · 8,7 kg [VARSAYIM kutu_cad_v14]
RAF_Y = (ALT_KAYIT_Y[1], ALT_KAYIT_Y[1] + SAC)                      # 1893,5–1895 · koli altı alt kayıtın 1,5 üstü → düz çekilir
RAF_Z = (Z_ARKA_IC + 2.5, KAYIT_Z[0] - 2.0)                         # −826 … +25
KOLI_ARA, KOLI_ARA_Z = 5.0, 3.0
KOLI_ON = RAF_Z[1] - 2.0                                            # ön sıra kolinin önü +23
RAF_KIRIS_X = None                                                  # kur() hesaplar (koli aralarının altında)

PARCALAR = []
BIRIMLER = [
    ("U_A_GOVDE", "Üst depo A · açıcı üstü x 507,5–1207,5 · y 1862–2200 · kapalı kutu (304 1,5 · üst 430) · 1 düşer kapak tava 20 (A servis kapağıyla aynı hiza) · BOŞ yedek depo"),
    ("U_F_GOVDE", "Üst depo F · fırın üstü x 2500–4000 · kapalı kutu · 2 düşer kapak (fırın üstü kabin kapaklarıyla aynı hiza) · BOŞ yedek depo · baca kanalı içinden geçer"),
    ("U_F_BACA", "Fırın davlumbaz atış kanalı uzantısı 300 × 200 (304 1,5 · 1862 → 2200, serbest kesit 297 × 197) + bina egzozu bağlantı flanşı (3 mm, üst sacın altında, 8 × M6)"),
    ("U_KE_GOVDE", "Üst depo K + E · x 4000–5230 · kapalı kutu · 2 eşit düşer kapak 612 · içecek rafı 1,5 + 4 taşıyıcı profil 30 × 30 × 2 (yük istasyon duvar hatlarına)"),
    ("U_ICECEK_YEDEK", "İçecek yedeği 6 koli × 24 = 144 kutu (3 yan yana × 2 sıra · koli 400 × 267 × 123) · U_KE rafında, soğutmasız · dolaptaki 144 ile 288 ≥ 4 gün 277"),
]
BIRIM_MODUL = {k: "U" for k, _a in BIRIMLER}
ON_BIRIMLER = ("U_A_GOVDE", "U_F_GOVDE", "U_KE_GOVDE")
MALZEME = {"sac": dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32), "paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30),
           "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35), "koyu": dict(renk=(0.10, 0.10, 0.11, 1.0), met=0.1, ruf=0.6),
           "karton": dict(renk=(0.80, 0.64, 0.42, 1.0), met=0.0, ruf=0.85)}
KAPAK_EKSEN = {}                               # kur(): grup → ((x0, y, z) eksen noktası, (1, 0, 0), açık açı °) · + açı = üst kenar öne
ICECEK_YEDEK = dict(x=(0.0, 0.0), y=(0.0, 0.0), z=(0.0, 0.0), koli=0, kutu=0, yer="U_KE")      # kur() doldurur (dünya)


# ================================================================ YARDIMCILAR ================================================================
def kut(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))


def silz(x, y, r, z0, z1):
    return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))


def kutu_profil_x(x0, x1, y0, y1, z0, z1, t=2.0):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, y0 + t, y1 - t, z0 + t, z1 - t))


def kutu_profil_z(x0, x1, y0, y1, z0, z1, t=2.0):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, z0 - 1.0, z1 + 1.0))


def ekle(ad, wp, mal, birim, bom=None, grup="SABIT", kaynak="h3_ust_depo_v1"):
    """bom = (kalem, adet, tanım, not/kaynak, tür)"""
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom))


def dunya(p):
    v = p["wp"].vals()
    return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])


def ac(sh, aci):
    """kapak parçası: alt ön kenar ekseninde (x boyunca, y 1862 · z +79) aci° — üst kenar öne (düşer kapak)"""
    return sh.rotate(V(0.0, PIVOT[0], PIVOT[1]), V(1.0, PIVOT[0], PIVOT[1]), aci)


def tipon_x(k, a, b, taraf):
    """bas-aç pistonu x (kapak boşluğunun içinde, karşı plaka tava kenarından ≥ 2) · gövde x aralığı · karşı plaka x aralığı"""
    x0, x1 = k["x"]
    if taraf == "sol":
        xp = max(x0 + SAC + 7.0, a + 10.0)
        return xp, (x0 + SAC, xp + 7.0), (xp - 8.0, xp + 8.0)
    xp = min(x1 - SAC - 7.0, b - 10.0)
    return xp, (xp - 7.0, x1 - SAC), (xp - 8.0, xp + 8.0)


# ================================================================ KUTU ================================================================
def kutu(k):
    c, B = k["kod"].lower(), k["birim"]
    x0, x1 = k["x"]
    bos = " · BOŞ yedek depo (makinenin kendi yedek parçası / sarf için)" if k["bos"] else ""
    # ---- taban (istasyon tavanlarının üstünde) ----
    t = kut(x0, x1, Y_TABAN[0], Y_TABAN[1], Z_ARKA_IC, Z_TAVA)
    if k["kod"] == "F":
        t = t.cut(kut(ATIS[0], ATIS[1], Y_TABAN[0] - 1.0, Y_TABAN[1] + 1.0, ATIS[2], ATIS[3]))
    ekle("ust_%s_taban_sac" % c, t, "sac", B, kaynak="h3_hesap_v1 UST_DEPO_Y",
         bom=("Üst depo taban sacı 304 1,5 · %.0f × %.0f" % (x1 - x0, Z_TAVA - Z_ARKA_IC), 1, "lazer",
              "istasyon tavanlarına (1862) oturur · yanlara + arkaya kaynaklı%s%s" % (" · baca kanalı açıklığı 300 × 200" if k["kod"] == "F" else "", bos), "ÜRETİM"))
    # ---- yan saclar (15 mm ön + arka iç büküm · bas-aç piston deliği ön bükümde) ----
    kap = k["kapak"]
    for tag, xa, xb, fa, fb in (("sol", x0, x0 + SAC, x0 + SAC, x0 + SAC + FLANS), ("sag", x1 - SAC, x1, x1 - SAC - FLANS, x1 - SAC)):
        w = kut(xa, xb, Y_TABAN[1], Y_TAVAN[0], Z_ARKA_IC, Z_TAVA)
        w = w.union(kut(fa, fb, Y_TABAN[1], Y_TAVAN[0], Z_TAVA - SAC, Z_TAVA)).union(kut(fa, fb, Y_TABAN[1], Y_TAVAN[0], Z_ARKA_IC, Z_ARKA_IC + SAC))
        ta = "sol" if tag == "sol" else "sag"
        a_, b_ = (kap[0] if tag == "sol" else kap[-1])
        if k["tipon"] == "iki" or k["tipon"] == "dis":
            xp, _g, _pl = tipon_x(k, a_, b_, ta)
            w = w.cut(silz(xp, (TIPON_Y[0] + TIPON_Y[1]) / 2.0, 5.0, Z_TAVA - SAC - 1.0, Z_TAVA + 1.0))
        ekle("ust_%s_yan_%s" % (c, tag), w, "sac", B,
             bom=("Üst depo yan sacı 304 fırçalı 1,5 · %.0f × %.0f + 15 ön / arka iç büküm" % (Y_TAVAN[0] - Y_TABAN[1], Z_TAVA - Z_ARKA_IC), 2, "lazer + abkant",
                  "bas-aç Ø10 deliği ön bükümde · komşu kutu / TOPPING yan sacına bitişik (lego)", "ÜRETİM") if tag == "sol" else None)
    # ---- tek parça arka sac ----
    ekle("ust_%s_arka_sac" % c, kut(x0, x1, Y_TABAN[0], H_UST, Z_ARKA, Z_ARKA_IC), "sac", B,
         bom=("Üst depo arka sacı 304 1,5 · TEK PARÇA %.0f × %.0f" % (x1 - x0, H_UST - Y_TABAN[0]), 1, "lazer", "yan saçların arka bükümlerine vidalı (servis)", "ÜRETİM"))
    # ---- üst sac 430 (sol / sağ / arka 20 aşağı büküm · ön kenar üst kayıtta) ----
    u = kut(x0, x1, Y_TAVAN[0], Y_TAVAN[1], Z_ARKA_IC, Z_TAVA)
    u = u.union(kut(x0 + SAC, x0 + 2 * SAC, Y_TAVAN[0] - BUKUM, Y_TAVAN[0], Z_ARKA_IC + SAC, Z_TAVA - SAC))
    u = u.union(kut(x1 - 2 * SAC, x1 - SAC, Y_TAVAN[0] - BUKUM, Y_TAVAN[0], Z_ARKA_IC + SAC, Z_TAVA - SAC))
    u = u.union(kut(x0 + SAC + FLANS, x1 - SAC - FLANS, Y_TAVAN[0] - BUKUM, Y_TAVAN[0], Z_ARKA_IC, Z_ARKA_IC + SAC))
    if k["kod"] == "F":
        u = u.cut(kut(ATIS[0] + SAC, ATIS[1] - SAC, Y_TAVAN[0] - 1.0, Y_TAVAN[1] + 1.0, ATIS[2] + SAC, ATIS[3] - SAC))
    ekle("ust_%s_tavan_sac" % c, u, "sac", B, kaynak="firin_ust_kabin_cad_v1 f_ust_tavan_sac ile aynı dil",
         bom=("Üst depo üst sacı 430 ferritik 1,5 · %.0f × %.0f · sol / sağ / arka 20 büküm" % (x1 - x0, Z_TAVA - Z_ARKA_IC), 1, "lazer + abkant",
              "MAKİNE ÜSTÜ 2200 (TOPPING dış tavanıyla aynı çizgi)%s" % (" · baca açıklığı 297 × 197 (kanal iç ölçüsü) + flanş cıvata delikleri" if k["kod"] == "F" else ""), "ÜRETİM"))
    # ---- ön: alt kayıt (menteşe sabit yaprakları) + üst kayıt (tavanın ön kenarı) · tavan kirişleri ----
    ekle("onyuz_ust_%s_alt_kayit" % c, kutu_profil_x(x0 + SAC, x1 - SAC, ALT_KAYIT_Y[0], ALT_KAYIT_Y[1], KAYIT_Z[0], KAYIT_Z[1]), "paslanmaz", B,
         bom=("Alt ön kayıt 304 kutu profil 30 × 30 × 2 · L %.0f" % (x1 - x0 - 2 * SAC), 1, "üretim", "yan saclara kaynaklı · düşer kapak menteşelerinin sabit yaprakları önünde · tabana oturur", "ÜRETİM"))
    ekle("onyuz_ust_%s_ust_kayit" % c, kutu_profil_x(x0 + 2 * SAC, x1 - 2 * SAC, UST_KAYIT_Y[0], UST_KAYIT_Y[1], KAYIT_Z[0], KAYIT_Z[1]), "paslanmaz", B,
         bom=("Üst ön kayıt 304 kutu profil 30 × 30 × 2 · L %.0f" % (x1 - x0 - 4 * SAC), 1, "üretim", "üst sacın ön kenarını taşır (serbest ön kenar yok) · yan saclara kaynaklı", "ÜRETİM"))
    for i, (xa, xb) in enumerate(k["kiris"]):
        ekle("ust_%s_tavan_kirisi_%d" % (c, i), kutu_profil_z(xa, xb, UST_KAYIT_Y[0], UST_KAYIT_Y[1], Z_ARKA_IC + SAC, KAYIT_Z[0]), "paslanmaz", B,
             bom=("Tavan kirişi 304 kutu profil 30 × 30 × 2 · L %.0f" % (KAYIT_Z[0] - Z_ARKA_IC - SAC), len(k["kiris"]), "üretim",
                  "üst sacın altında z boyunca (arka büküm → üst kayıt) · üst sac açıklığını ≤ %.0f'e böler" % max(b_ - a_ for a_, b_ in _araliklar(k)), "ÜRETİM") if i == 0 else None)
    # ---- kapaklar ----
    for j, (a, b) in enumerate(kap):
        tag = ("sol", "sag")[j] if len(kap) == 2 else "tek"
        g = "KAPAK_U_%s_%s" % (k["kod"], tag.upper())
        KAPAK_EKSEN[g] = ((a, PIVOT[0], PIVOT[1]), (1.0, 0.0, 0.0), ACI_ACIK)
        p = kut(a, b, KAPAK_Y[0], KAPAK_Y[1], Z_TAVA, Z_ON).cut(kut(a + SAC, b - SAC, KAPAK_Y[0] + SAC, KAPAK_Y[1] - SAC, Z_TAVA - 1.0, Z_ON - SAC))
        ekle("onyuz_ust_%s_kapak_%s" % (c, tag), p, "sac", B, grup=g, kaynak="firin_ust_kabin_cad_v1 onyuz_f_ust_kapak ile aynı dil (tava 20)",
             bom=("Üst depo kapak kanadı · tava 20 · 304 fırçalı 1,5 · %.1f × %.0f" % (b - a, KAPAK_Y[1] - KAPAK_Y[0]), len(kap), "lazer + abkant (4 kenar 20 arkaya)",
                  "alttan menteşeli DÜŞER KAPAK · kulp / vida / menteşe önden görünmez" + bos, "ÜRETİM") if j == 0 else None)
        kt = kut(a + SAC, b - SAC, KUTU_Y[0], KUTU_Y[0] + SAC_IC, KUTU_Z[0], KUTU_Z[1]).union(kut(a + SAC, b - SAC, KUTU_Y[1] - SAC_IC, KUTU_Y[1], KUTU_Z[0], KUTU_Z[1])) \
            .union(kut(a + SAC, b - SAC, KUTU_Y[0], KUTU_Y[1], KUTU_Z[0], KUTU_Z[0] + SAC_IC))
        ekle("onyuz_ust_%s_kapak_%s_alt_kutusu" % (c, tag), kt, "paslanmaz", B, grup=g,
             bom=("Kapak alt kutusu 304 1,0 · C %.0f × 17 · L %.0f" % (KUTU_Y[1] - KUTU_Y[0], b - a - 2 * SAC), 1, "abkant + punta",
                  "kapak içinde alt bantta · menteşe hareketli yaprakları sırtında", "ÜRETİM"))
        for m, xh in enumerate((a + MENTESE_DX, b - MENTESE_DX)):
            ekle("onyuz_ust_%s_mentese_sabit_%s_%d" % (c, tag, m), kut(xh - 19.0, xh + 19.0, MENTESE_Y[0], MENTESE_Y[1], KAYIT_Z[1], Z_TAVA), "celik", B,
                 kaynak="Sugatsune SDH-001 (fırın üstü kabinle aynı) — sabit yaprak + sac adaptör VARSAYIM",
                 bom=("Düşer kapak menteşesi Sugatsune SDH-001 + sac adaptör", 2 * len(kap), "katalog (sugatsune.com drop hinge)",
                      "sanal pivot kapağın alt ön kenarında (y 1862 · z +79) · 90° durdurma menteşede · SÖNÜMLÜ (yavaş iniş) sürüm + kapasite üreticiyle (AÇIK)", "SATIN ALMA") if m == 0 and j == 0 else None)
            ekle("onyuz_ust_%s_mentese_hareketli_%s_%d" % (c, tag, m), kut(xh - 19.0, xh + 19.0, MENTESE_Y[0], MENTESE_Y[1], Z_TAVA, KUTU_Z[0]), "celik", B, grup=g,
                 kaynak="Sugatsune SDH-001 hareketli yaprak (şematik)")
        # bas-aç (Blum TIP-ON 956.1004): dış köşe(ler)de yan saca braketli · piston ön bükümden kapaktaki karşı plakaya
        taraflar = (["sol", "sag"] if k["tipon"] == "iki" else (["sol"] if j == 0 else ["sag"]))
        for ta in taraflar:
            xp, (gx0, gx1), (px0, px1) = tipon_x(k, a, b, ta)
            ti = kut(gx0, gx1, TIPON_Y[0], TIPON_Y[1], 20.0, Z_TAVA - SAC).union(silz(xp, (TIPON_Y[0] + TIPON_Y[1]) / 2.0, 4.0, Z_TAVA - SAC, Z_ON - SAC - 1.0))
            ekle("onyuz_ust_%s_bas_ac_%s_%s" % (c, tag, ta), ti, "koyu", B, kaynak="Blum TIP-ON 956.1004 (fırın üstü kabinle aynı)",
                 bom=("Bas-aç itici Blum TIP-ON 956.1004 (kısa · mıknatıs uçlu · karşı plakalı set)", 1, "katalog",
                      "kanat üst dış köşesi · yan saca braketli · karşı plakası kapakta · kulp yok", "SATIN ALMA"))
            ekle("onyuz_ust_%s_kapak_%s_tipon_plakasi_%s" % (c, tag, ta), kut(px0, px1, TIPON_Y[0], TIPON_Y[1], Z_ON - SAC - 1.0, Z_ON - SAC), "celik", B, grup=g,
                 kaynak="Blum 956.1004 setindeki vidalı karşı plaka (16 × 20 × 1 VARSAYIM)",
                 bom=("TIP-ON karşı plakası (956.1004 setinde)", 1, "katalog", "kapak iç yüzüne perçin", "SET İÇİNDE"))


def _araliklar(k):
    """üst sacın serbest açıklıkları (x) — yan sac iç yüzleri ve kirişler arası"""
    xs = [k["x"][0] + 2 * SAC] + [v for ab in k["kiris"] for v in ab] + [k["x"][1] - 2 * SAC]
    return [(xs[i], xs[i + 1]) for i in range(0, len(xs), 2)]


def baca():
    """U_F içinden fırın davlumbaz atış kanalının uzantısı · alt uç fırın üstü kabinin üst sacına (açıklığı kanal iç ölçüsü) oturur"""
    B = "U_F_BACA"
    x0, x1, z0, z1 = ATIS
    k = kut(x0, x1, Y_TABAN[0], Y_TAVAN[0], z0, z1).cut(kut(x0 + SAC, x1 - SAC, Y_TABAN[0] - 1.0, Y_TAVAN[0] + 1.0, z0 + SAC, z1 - SAC))
    ekle("ust_f_baca_kanali", k, "sac", B, kaynak="firin_ust_kabin_cad_v1.ATIS (f_davlumbaz_atis_kanali ile aynı kesit)",
         bom=("Atış kanalı uzantısı 304 1,5 · 300 × 200 × %.1f" % (Y_TAVAN[0] - Y_TABAN[0]), 1, "abkant + kaynak",
              "fırın üstü kabinin üst sacındaki atış ağzından (1862) üst deponun üst sacına (2198,5) · serbest kesit 297 × 197 · taban sacı açıklığından geçer", "ÜRETİM"))
    f = kut(x0 - BACA_FLANS, x1 + BACA_FLANS, Y_TAVAN[0] - BACA_FLANS_T, Y_TAVAN[0], z0 - BACA_FLANS, z1 + BACA_FLANS).cut(
        kut(x0, x1, Y_TAVAN[0] - BACA_FLANS_T - 1.0, Y_TAVAN[0] + 1.0, z0, z1))
    ekle("ust_f_baca_flansi", f, "paslanmaz", B, kaynak="bina egzozu bağlantısı",
         bom=("Baca bağlantı flanşı 304 3 mm · %.0f × %.0f çerçeve (30 geniş) + 8 × M6 kaynak somunu" % (x1 - x0 + 2 * BACA_FLANS, z1 - z0 + 2 * BACA_FLANS), 1, "lazer + kaynak",
              "üst sacın ALTINDA (2195,5–2198,5), kanala kaynaklı · bina egzoz kanalı ÜSTTEN, üst sacı arada sıkıştırarak cıvatalanır → 2200'ün üstünde çıkıntı yok", "ÜRETİM"))


def icecek():
    """U_KE: raf (1,5) + 4 taşıyıcı profil (koli aralarının altında) + 6 koli"""
    global RAF_KIRIS_X
    k = KUTULAR[2]; x0, x1 = k["x"]
    ic0, ic1 = x0 + SAC, x1 - SAC
    gen = 3 * KOLI["x"] + 2 * KOLI_ARA
    kx0 = (ic0 + ic1) / 2.0 - gen / 2.0
    KX = [(kx0 + i * (KOLI["x"] + KOLI_ARA), kx0 + i * (KOLI["x"] + KOLI_ARA) + KOLI["x"]) for i in range(3)]
    KZ = [(KOLI_ON - KOLI["z"], KOLI_ON), (KOLI_ON - 2 * KOLI["z"] - KOLI_ARA_Z, KOLI_ON - KOLI["z"] - KOLI_ARA_Z)]
    RAF_KIRIS_X = [(ic0, ic0 + PROFIL), ((KX[0][1] + KX[1][0]) / 2.0 - PROFIL / 2.0, (KX[0][1] + KX[1][0]) / 2.0 + PROFIL / 2.0),
                   ((KX[1][1] + KX[2][0]) / 2.0 - PROFIL / 2.0, (KX[1][1] + KX[2][0]) / 2.0 + PROFIL / 2.0), (ic1 - PROFIL, ic1)]
    for i, (xa, xb) in enumerate(RAF_KIRIS_X):
        ekle("ust_ke_raf_kirisi_%d" % i, kutu_profil_z(xa, xb, Y_TABAN[1], RAF_Y[0], RAF_Z[0], RAF_Z[1]), "paslanmaz", "U_KE_GOVDE",
             bom=("Raf taşıyıcı profil 304 kutu 30 × 30 × 2 · L %.0f" % (RAF_Z[1] - RAF_Z[0]), 4, "üretim",
                  "tabana kaynaklı · koli aralarının altında · yükü istasyon duvar hatlarına (K|E 4400) yakın taşır", "ÜRETİM") if i == 0 else None)
    r = kut(ic0, ic1, RAF_Y[0], RAF_Y[1], RAF_Z[0], RAF_Z[1])
    ekle("ust_ke_icecek_rafi", r, "sac", "U_KE_GOVDE",
         bom=("İçecek rafı 304 1,5 · %.0f × %.0f" % (ic1 - ic0, RAF_Z[1] - RAF_Z[0]), 1, "lazer", "4 profile punta · koli altı 1895 > alt kayıt üstü 1893,5 → koli düz çekilir", "ÜRETİM"))
    n = 0
    for s, (xa, xb) in enumerate(KX):
        for rr, (za, zb) in enumerate(KZ):
            ekle("ust_icecek_koli_%d%d" % (s, rr), kut(xa, xb, RAF_Y[1], RAF_Y[1] + KOLI["y"], za, zb), "karton", "U_ICECEK_YEDEK",
                 bom=("İçecek kolisi 24 kutu (yedek, soğutmasız)", 6, "400 × 267 × 123 · 24 kutu · ≈ %.1f kg" % KOLI["kg"],
                      "sarf · koli ölçüsü VARSAYIM (kutu_cad_v14 ile aynı) · v1: E altı → v2: U_KE" ) if n == 0 else None)
            n += 1
    ICECEK_YEDEK.update(x=(KX[0][0], KX[-1][1]), y=(RAF_Y[1], RAF_Y[1] + KOLI["y"]), z=(KZ[1][0], KZ[0][1]), koli=n, kutu=n * KOLI["adet"], yer="U_KE",
                        sutun_x=KX, sira_z=KZ)
    return KX, KZ


def kur():
    PARCALAR[:] = []
    KAPAK_EKSEN.clear()
    for k in KUTULAR:
        kutu(k)
    baca()
    icecek()
    return PARCALAR


# ================================================================ DENETİM ================================================================
def _bbk(A, B, pay=0.05):
    return A.xmin < B.xmax - pay and B.xmin < A.xmax - pay and A.ymin < B.ymax - pay and B.ymin < A.ymax - pay and A.zmin < B.zmax - pay and B.zmin < A.zmax - pay


def capraz(S, T, esik=0.1, haric=()):
    S = [(a, s, s.BoundingBox()) for a, s in S]; T = [(a, s, s.BoundingBox()) for a, s in T]
    out = []
    for a, sa, A in S:
        for c, sc, B in T:
            if a == c or (a, c) in haric or (c, a) in haric or not _bbk(A, B): continue
            try: v = sa.intersect(sc).Volume()
            except Exception: v = -1.0
            if v > esik or v < 0: out.append((round(v, 3), a, c))
    return sorted(out, reverse=True)


def _tek(wp):
    if hasattr(wp, "vals"):
        v = [o for o in wp.vals() if isinstance(o, cq.Shape)]
        return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)
    return wp


def istasyon_ustleri(y_min=1800.0):
    """komşu istasyon parçaları (dünya) — ymax > y_min: A (h3_acici_v1, yoksa acici_kabin_cad_v1 + 507,5) · F üstü (firin_ust_kabin_cad_v1) · K (kesme_cad_v11 + 4000) · E (kutu_cad_v14 + 4400)"""
    out, kay = [], {}
    try:
        import h3_acici_v1 as AK
        AK.kur(); kay["A"] = "h3_acici_v1"
        out += [("A:" + p["ad"], AK.dunya(p)) for p in AK.PARCALAR]
    except Exception as e:
        import acici_kabin_cad_v1 as AK
        AK.kur(); kay["A"] = "acici_kabin_cad_v1 + %.1f (h3_acici_v1 yüklenemedi: %s)" % (HS.DXL, str(e)[:60])
        out += [("A:" + p["ad"], AK.dunya(p).translate(V(HS.DXL, 0, 0))) for p in AK.PARCALAR]
    import firin_ust_kabin_cad_v1 as FU
    FU.kur(); kay["F"] = "firin_ust_kabin_cad_v1"
    out += [("F:" + p["ad"], FU.dunya(p)) for p in FU.PARCALAR]
    import kesme_cad_v11 as KS
    if not KS.PARCALAR: KS.modul()
    kay["K"] = "kesme_cad_v11 + %.0f" % HS.K_X[0]
    out += [("K:" + p["ad"], _tek(p["wp"]).translate(V(HS.K_X[0], 0, 0))) for p in KS.PARCALAR if p["grup"] not in ("URUN", "URUN_IZ", "REF", "SPREY")]
    import kutu_cad_v14 as KC
    if not KC.PARCALAR: KC.modul()
    kay["E"] = "kutu_cad_v14 + %.0f (grup SABIT/ASANSOR, dinlenme)" % HS.E_X[0]
    out += [("E:" + p["ad"], _tek(p["wp"]).translate(V(HS.E_X[0], 0, 0))) for p in KC.PARCALAR if p["grup"] in ("SABIT", "ASANSOR", "PISTON", "ITICI", "VAC_Y")]
    out = [(a, s) for a, s in out if s.BoundingBox().ymax > y_min]
    return out, kay


DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger))
    print("  %-150s %s %s" % (ad, "GECTI" if sart else "** KALDI **", deger))


def denetim(topping=True):
    t0 = time.time()
    DEN[:] = []
    ps = kur()
    S = [(p["ad"], dunya(p)) for p in ps]
    SD = dict(S)
    BB = {a: s.BoundingBox() for a, s in S}
    print("UST DEPO (h3_ust_depo_v1) · %d parca (%s)" % (len(ps), " · ".join("%s %d" % (k, sum(1 for p in ps if p["birim"] == k)) for k, _a in BIRIMLER)))
    gec = [a for a, s in S if not s.isValid()]
    kontrol("KATILAR gecerli", not gec, str(gec))
    kontrol("BIRIMLER ↔ parcalar (her birimin parcasi var · BIRIM_MODUL tam, hepsi 'U')", all(any(p["birim"] == k for p in ps) for k, _a in BIRIMLER)
            and all(p["birim"] in BIRIM_MODUL for p in ps) and set(BIRIM_MODUL.values()) == {"U"})
    # ---- zarflar ----
    zar = []
    for k in KUTULAR:
        c = k["kod"].lower()
        for p in ps:
            if not (p["ad"].startswith(("ust_%s_" % c, "onyuz_ust_%s_" % c)) or (k["kod"] == "KE" and p["birim"] == "U_ICECEK_YEDEK") or (k["kod"] == "F" and p["birim"] == "U_F_BACA")):
                continue
            b = BB[p["ad"]]
            if b.xmin < k["x"][0] - 0.01 or b.xmax > k["x"][1] + 0.01 or b.ymin < H_IST - 0.01 or b.ymax > H_UST + 0.01 or b.zmin < Z_ARKA - 0.01 or b.zmax > Z_ON + 0.01:
                zar.append((p["ad"], round(b.xmin, 1), round(b.xmax, 1), round(b.ymin, 1), round(b.ymax, 1), round(b.zmin, 1), round(b.zmax, 1)))
    kontrol("ZARF: her kutunun parcasi kendi x araliginda (A %.1f–%.1f · F %.0f–%.0f · KE %.0f–%.0f) · y %.0f–%.0f · z %.0f…+%.0f"
            % (KUTULAR[0]["x"] + KUTULAR[1]["x"] + KUTULAR[2]["x"] + (H_IST, H_UST, Z_ARKA, Z_ON)), not zar, str(zar[:4]))
    ymax = max(b.ymax for b in BB.values())
    tav = {k["kod"]: BB["ust_%s_tavan_sac" % k["kod"].lower()] for k in KUTULAR}
    kontrol("UST CIZGI: en ust parca y %.2f = %.0f · uc ust sac %s · x %.1f–%.1f (TOPPING 1207,5–2500 araliginda kendi tavani) · 2200'un ustunde parca YOK"
            % (ymax, H_UST, " / ".join("%.2f" % b.ymax for b in tav.values()), tav["A"].xmin, tav["KE"].xmax),
            abs(ymax - H_UST) < 0.01 and all(abs(b.ymax - H_UST) < 0.01 for b in tav.values()))
    gv = [a for a, b in BB.items() if not a.startswith("onyuz_") and b.zmax > Z_TAVA + 0.01]
    on = [a for a, b in BB.items() if b.zmax > Z_ON + 0.01]
    kontrol("ON DUZLEM: kapak dis yuzleri +79 · govde saclari +59'da biter (+59'u gecen yalniz onyuz_ kapak / donanim) · +79'u gecen yok", not gv and not on, str(gv + on))
    # ---- derzler / eşit kapaklar / hiza ----
    kap = {k["kod"]: [BB["onyuz_ust_%s_kapak_%s" % (k["kod"].lower(), ("sol", "sag")[j] if len(k["kapak"]) == 2 else "tek")] for j in range(len(k["kapak"]))] for k in KUTULAR}
    gen = {kd: [round(b.xmax - b.xmin, 2) for b in L] for kd, L in kap.items()}
    ara = []
    for kd, L in kap.items():
        for b1, b2 in zip(L, L[1:]): ara.append(round(b2.xmin - b1.xmax, 2))
    ara += [round(kap["KE"][0].xmin - kap["F"][-1].xmax, 2)]
    ys = sorted({(round(b.ymin, 2), round(b.ymax, 2)) for L in kap.values() for b in L})
    _hz = abs((kap["KE"][0].xmax + kap["KE"][1].xmin) / 2.0 - HS.E_X[0]) < 0.01                           # v2 (Claude): U_KE derzi K|E çizgisinde
    kontrol("KAPAKLAR: A / F kutu basina esit genislik, U_KE derzi K|E cizgisinde (%s) %s · kanat arasi derzler %s (= 3) · y %s (alttaki kapak ustu 1859 → derz 3 · ust 2197 = TOPPING kapak ustu · makine ustune 3)"
            % (_hz, gen, ara, ys), all(len(set(v)) == 1 for k_, v in gen.items() if k_ != "KE") and _hz and all(abs(a - DERZ) < 0.01 for a in ara) and ys == [(KAPAK_Y[0], KAPAK_Y[1])])
    kontrol("HIZA: U_A kapagi x %.1f–%.1f = A servis kapagi (507,5–1206) · U_F kapaklari %.1f–%.1f / %.1f–%.1f = firin ustu kabin kapaklari · U_KE sol kenari %.1f = K ust kapagi (4003) · sag %.1f = E"
            % (kap["A"][0].xmin, kap["A"][0].xmax, kap["F"][0].xmin, kap["F"][0].xmax, kap["F"][1].xmin, kap["F"][1].xmax, kap["KE"][0].xmin, kap["KE"][1].xmax),
            abs(kap["A"][0].xmin - HS.A_X[0]) < 0.01 and abs(kap["A"][0].xmax - (HS.A_X[1] - 1.5)) < 0.01 and abs(kap["F"][0].xmax - 3248.5) < 0.01 and abs(kap["F"][1].xmin - 3251.5) < 0.01
            and abs(kap["KE"][0].xmin - 4003.0) < 0.01 and abs(kap["KE"][1].xmax - 5230.0) < 0.01)
    # ---- kendi arasında ----
    BAG = set()
    for p in ps:
        if "_mentese_hareketli_" in p["ad"]:
            BAG.add((p["ad"], p["ad"].replace("_hareketli_", "_sabit_")))
    c1 = []
    for i in range(len(S)):
        c1 += capraz([S[i]], S[i + 1:])
    for x_ in c1[:10]: print("   %10.3f mm3  %s  <->  %s" % x_)
    kontrol("KENDI ARASINDA cakisma > 0,1 mm³ = 0 (%d parca · kapaklar kapali)" % len(S), not c1, "%d bulgu" % len(c1))
    # ---- istasyonlar ----
    IS, kay = istasyon_ustleri()
    c2 = capraz(S, IS)
    for x_ in c2[:10]: print("   %10.3f mm3  %s  <->  %s" % x_)
    kontrol("ISTASYONLAR (%s · %d parca, ymax > 1800) ↔ ust depo > 0,1 mm³ = 0" % (" · ".join("%s %s" % kv for kv in kay.items()), len(IS)), not c2, "%d bulgu" % len(c2))
    ist_ust = max(s.BoundingBox().ymax for a, s in IS)
    kontrol("ISTASYON USTLERI: A / F / K / E'nin en ust parcasi y %.2f ≤ %.0f (1862'nin ustune cikan istasyon parcasi YOK → kesme / kaydirma gerekmedi)" % (ist_ust, H_IST),
            ist_ust <= H_IST + 0.01)
    if topping:
        try:
            import h3_topping_v1 as HT
            TC_, TU_ = HT.kur()
            TT = [("TOP:" + q["ad"], q["sh"]) for q in TC_ + TU_ if q["sh"].BoundingBox().ymax > H_IST - 1.0
                  and (q["sh"].BoundingBox().xmin < HS.A_X[1] + 5.0 or q["sh"].BoundingBox().xmax > HS.F_X[0] - 5.0)]
            c3 = capraz(S, TT)
            for x_ in c3[:6]: print("   %10.3f mm3  %s  <->  %s" % x_)
            tx = [q["sh"].BoundingBox() for q in TC_ + TU_ if q["sh"].BoundingBox().ymax > H_IST]
            kontrol("TOPPING (h3_topping_v1, %d uc parca 1862 ustunde) ↔ ust depo = 0 · TOPPING x %.1f–%.1f (U_A sagi %.1f · U_F solu %.1f) · TOPPING ustu %.2f"
                    % (len(TT), min(b.xmin for b in tx), max(b.xmax for b in tx), HS.A_X[1], HS.F_X[0], max(b.ymax for b in tx)), not c3, "%d bulgu" % len(c3))
        except Exception as e:
            print("   BILGI · TOPPING (h3_topping_v1) yuklenemedi, denetim atlandi: %s" % str(e)[:160])
    # ---- kapak süpürmesi 0°–90° ----
    GK = {}
    for p in ps:
        if p["grup"].startswith("KAPAK_U_"):
            GK.setdefault(p["grup"], []).append(p["ad"])
    SAB = [(a, s) for a, s in S if not any(a in L for L in GK.values())]
    sup = []
    for aci in (1.0, 5.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0):
        KA = [(a + "@%.0f" % aci, ac(SD[a], aci)) for L in GK.values() for a in L]
        haric = {(a + "@%.0f" % aci, c) for a, c in BAG}
        sup += capraz(KA, SAB + IS, haric=haric)
        for g1 in GK:
            for g2 in GK:
                if g1 < g2:
                    sup += capraz([(a + "@%.0f" % aci, ac(SD[a], aci)) for a in GK[g1]], [(a + "@%.0f" % aci, ac(SD[a], aci)) for a in GK[g2]])
    for x_ in sup[:8]: print("   %10.3f mm3  %s  <->  %s" % x_)
    b90 = cq.Compound.makeCompound([ac(SD[a], 90.0) for L in GK.values() for a in L]).BoundingBox()
    kontrol("KAPAK SUPURMESI 1°…90° (8 konum · %d kanat birlikte · menteşe hareketli yaprak + C kutu + karsi plaka) ↔ kutu sabitleri + istasyonlar + diger kanatlar = 0 · "
            "90°'de kanatlar y %.1f–%.1f · z %.1f…%.1f (QR dolabi z ≥ 670)" % (len(GK), b90.ymin, b90.ymax, b90.zmin, b90.zmax), not sup and b90.zmax < 670.0 and b90.ymin >= H_IST - 0.01,
            str(sup[:3]))
    # kapak momenti (sönümlü menteşe seçimi için)
    for g, L in sorted(GK.items()):
        kp = [a for a in L if "mentese" not in a]
        m = sum(SD[a].Volume() for a in kp) * RO
        cy = sum(SD[a].Volume() * SD[a].Center().y for a in kp) / sum(SD[a].Volume() for a in kp)
        print("   KANAT %-16s %.2f kg · agirlik merkezi pivottan %.0f mm · 90°'de %.1f N·m (menteşe basina %.1f)" % (g, m, cy - PIVOT[0], m * 9.81 * (cy - PIVOT[0]) / 1000.0,
                                                                                                   m * 9.81 * (cy - PIVOT[0]) / 2000.0))
    # ---- baca ----
    FUmod = sys.modules.get("firin_ust_kabin_cad_v1")
    x0, x1, z0, z1 = ATIS
    PR = kut(x0 + SAC, x1 - SAC, 1790.5, H_UST + 1.0, z0 + SAC, z1 - SAC).val()
    engel = [(a, round(s.intersect(PR).Volume(), 2)) for a, s in S + IS if _bbk(s.BoundingBox(), PR.BoundingBox()) and s.intersect(PR).Volume() > 0.01]
    kb = BB["ust_f_baca_kanali"]
    A_ = (x1 - x0 - 2 * SAC) * (z1 - z0 - 2 * SAC)
    ust_ac = SD["ust_f_tavan_sac"].intersect(kut(x0, x1, Y_TAVAN[0], Y_TAVAN[1], z0, z1).val()).Volume()
    kontrol("BACA: kanal x %.0f–%.0f · y %.1f–%.1f · z %.0f…%.0f · SERBEST KESIT %.0f × %.0f = %.0f mm² (300 × 200 − sac) · firin atis kanali (1790) → 2200 prizmasinda engel %s · ust sac acikligi = kanal ic olcusu (kalan %.1f mm³ = cerceve)"
            % (kb.xmin, kb.xmax, kb.ymin, kb.ymax, kb.zmin, kb.zmax, x1 - x0 - 2 * SAC, z1 - z0 - 2 * SAC, A_, engel or "YOK",
               ust_ac), not engel and abs(A_ - 297.0 * 197.0) < 0.01)
    if FUmod is not None:
        ak = FUmod.dunya(next(p for p in FUmod.PARCALAR if p["ad"] == "f_davlumbaz_atis_kanali")).BoundingBox()
        kontrol("BACA SUREKLI: firin atis kanali x %.0f–%.0f · z %.0f…%.0f · ust %.1f = uzantinin kesiti (x %.0f–%.0f · z %.0f…%.0f · alt %.1f) · aradaki firin ust saci (1860,5–1862) acik"
                % (ak.xmin, ak.xmax, ak.zmin, ak.zmax, ak.ymax, kb.xmin, kb.xmax, kb.zmin, kb.zmax, kb.ymin),
                all(abs(a_ - b_) < 0.01 for a_, b_ in ((ak.xmin, kb.xmin), (ak.xmax, kb.xmax), (ak.zmin, kb.zmin), (ak.zmax, kb.zmax))) and abs(kb.ymin - H_IST) < 0.01)
    # ---- içecek yedeği ----
    KX, KZ = ICECEK_YEDEK["sutun_x"], ICECEK_YEDEK["sira_z"]
    ic0, ic1 = KUTULAR[2]["x"][0] + SAC, KUTULAR[2]["x"][1] - SAC
    fb = (ic0 + FLANS, ic1 - FLANS)
    kontrol("ICECEK YEDEGI: %d koli × %d = %d kutu (hesap ICECEK_YEDEK_KOLI %d) · dolap %d + %d = %d ≥ 4 gun %d · koliler x %.1f–%.1f · y %.1f–%.1f · z %.1f…%.1f"
            % (ICECEK_YEDEK["koli"], KOLI["adet"], ICECEK_YEDEK["kutu"], HS.ICECEK_YEDEK_KOLI, HS.STOK["icecek"], ICECEK_YEDEK["kutu"], HS.STOK["icecek"] + ICECEK_YEDEK["kutu"],
               HS.ICECEK_4GUN, ICECEK_YEDEK["x"][0], ICECEK_YEDEK["x"][1], ICECEK_YEDEK["y"][0], ICECEK_YEDEK["y"][1], ICECEK_YEDEK["z"][0], ICECEK_YEDEK["z"][1]),
            ICECEK_YEDEK["koli"] == HS.ICECEK_YEDEK_KOLI == 6 and HS.STOK["icecek"] + ICECEK_YEDEK["kutu"] >= HS.ICECEK_4GUN)
    kontrol("KOLI PAYLARI: yan saclara %.1f / %.1f · koli arasi %.0f · ust kayit / kirislere %.1f · alt kayita (on) %.1f · raf ↔ alt kayit ustu %.1f (koli duz cekilir)"
            % (KX[0][0] - ic0, ic1 - KX[-1][1], KX[1][0] - KX[0][1], UST_KAYIT_Y[0] - ICECEK_YEDEK["y"][1], KAYIT_Z[0] - KZ[0][1], RAF_Y[1] - ALT_KAYIT_Y[1]),
            KX[0][0] - ic0 >= 5.0 and ic1 - KX[-1][1] >= 5.0 and UST_KAYIT_Y[0] - ICECEK_YEDEK["y"][1] >= 50.0 and RAF_Y[1] > ALT_KAYIT_Y[1])
    # çekme yolu: kanatlar 90° açık · orta koli düz · kenar koliler (yan sac ön bükümü x %.1f / %.1f) ortası boşalınca içe kaydırılıp çekilir
    ACIK = [(a + "@90", ac(SD[a], 90.0)) for g in ("KAPAK_U_KE_SOL", "KAPAK_U_KE_SAG") for a in GK[g]]
    SAB_KE = [(a, s) for a, s in SAB if a.startswith(("ust_ke_", "onyuz_ust_ke_"))] + ACIK
    yol = []
    kay_x = max(fb[0] - KX[0][0], KX[-1][1] - fb[1]) + 1.0
    for s_, (xa, xb) in enumerate(KX):
        dx = 0.0 if s_ == 1 else (kay_x if s_ == 0 else -kay_x)
        for rr in range(2):
            ad = "ust_icecek_koli_%d%d" % (s_, rr)
            for dz in (60.0, 200.0, 350.0, 500.0 + 270.0 * rr):
                yol += capraz([(ad + "@dz%.0f" % dz, SD[ad].translate(V(dx, 0.0, dz)))], SAB_KE)
    for x_ in yol[:6]: print("   %10.3f mm3  %s  <->  %s" % x_)
    kontrol("KOLI CEKME YOLU (kanatlar 90° acik): orta sutun duz · kenar sutunlar ortasi bosalinca %.1f mm ice kaydirilip (yan sac on bukumu x %.1f / %.1f) one +60…+770 ↔ U_KE sabitleri + acik kanatlar = 0"
            % (kay_x, fb[0], fb[1]), not yol, str(yol[:3]))
    # raf sehimi (tek yönlü plak, profiller arası)
    L_ = max(RAF_KIRIS_X[i + 1][0] - RAF_KIRIS_X[i][1] for i in range(len(RAF_KIRIS_X) - 1)) / 1000.0
    q_ = KOLI["kg"] * 9.81 / (KOLI["x"] * KOLI["z"] / 1e6)
    D_ = 193e9 * (SAC / 1000.0) ** 3 / (12.0 * (1.0 - 0.29 ** 2))
    sh_ = 5.0 * q_ * L_ ** 4 / (384.0 * D_) * 1000.0
    kontrol("RAF: profiller x %s · en buyuk aciklik %.0f mm · koli yuku %.0f Pa → 1,5 mm sac sehimi (basit mesnet) %.1f mm ≤ 4 · toplam yuk %.0f kg (6 × %.1f) → 4 profil"
            % (" / ".join("%.0f–%.0f" % ab for ab in RAF_KIRIS_X), L_ * 1000.0, q_, sh_, 6 * KOLI["kg"], KOLI["kg"]), sh_ <= 4.0)
    # üst sac sehimi (açıklıklar)
    for k in KUTULAR:
        a_ = max(b - a for a, b in _araliklar(k)) / 1000.0; b_ = (KAYIT_Z[0] - Z_ARKA_IC) / 1000.0
        lo, hi = min(a_, b_), max(a_, b_); r_ = hi / lo
        al = 0.00406 if r_ <= 1.0 else (0.00564 if r_ <= 1.2 else (0.00705 if r_ <= 1.4 else (0.00830 if r_ <= 1.6 else (0.00931 if r_ <= 1.8 else (0.01013 if r_ <= 2.0 else 0.01302)))))
        qs = 7930.0 * 9.81 * SAC / 1000.0
        print("   BILGI · U_%s ust sac en buyuk plak %.0f × %.0f → oz agirlik sehimi (dort kenar basit) %.1f mm" % (k["kod"], a_ * 1000.0, b_ * 1000.0, al * qs * lo ** 4 / D_ * 1000.0))
    kal = [d for d in DEN if not d[1]]
    print("DENETIM (h3_ust_depo_v1): %d madde · %d KALDI · %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    return DEN


if __name__ == "__main__":
    D = denetim(topping="--topping-yok" not in sys.argv)
    kal = [d[0] for d in D if not d[1]]
    assert not kal, kal
    sys.stdout.flush(); os._exit(0)
