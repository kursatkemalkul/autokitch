# -*- coding: utf-8 -*-
"""HAT VERSİYON 3 · FIRIN ÜSTÜ KABİN ADAPTÖRÜ v1 (30 Eyl 2026 · Claude · YEREL) — montajda 'import h3_firin_ust_v1 as FU' (firin_ust_kabin_cad_v1 yerine).
firin_ust_kabin_cad_v1 YENİDEN ÇİZİLMEZ: yalnız x sabitleri v3 yerleşimine yazılır, kur() aynı işlevdir.
Kemal HAT v2.7 ("kompresörü sola çekip yağ tenekesini onun yerine sağ tarafa koysak"):
  · pizza yedeği 320 kutu 2520–3324 DEĞİŞMEZ · tavan kirişi + TEK ön dikme 3326–3356 (v2: kiriş 3336–3366 + kompresörün solunda 2. dikme 3560–3590 —
    v3'te ikisi de kompresörün önüne düşerdi, kompresör öne çekilemezdi) · kompresör tavası + ayaklar 241 sola (tank 3359–3739) · kompresör besleme rakoru 241 sola ·
    sağda yağ tenekesi seti (h3_kesme_v1: tava 3742–3985) · raf açıklığı firin_tp10 KOMP_ACIKLIK = h3_hesap_v1.KOMP_ACIKLIK_X (montaj FT.kur()'dan önce yazar).
  · fırın üstü tavan açıklıkları: sol yan → kiriş 1824,5 (v2 1834,5) · kiriş → sağ yan 2642,5 — v2'de 2. dikme → sağ yan 408 idi; sac 1,5 + U deposu tabanı üstte (KONTROL: montaj).
v3.6 (1 Eki 2026 · Claude · YEREL) — Kemal: "raf sacı altta → üste koy ki düz ve temiz olsun; o zaman ekstra tabla gerekmez" + "kompresörün kendi ayakları var;
  gövdedeki deliği ve benim eklediğim ayakları kaldır; standart kompresör kendi ayaklarıyla üstte dursun". DEĞİŞENLER:
  · KALKTI (F_KOMP_AYAK): f_komp_tavasi (raf açıklığına asılı 4 mm tava, taban 1324 — "ekstra tabla") · 4 × f_komp_titresim_takozu · 4 × f_komp_urun_ayagi.
  · RAF (firin_tp10_cad_v10 'ust_raf', birim F_UST_RAF — fırın gövdesi F_TP10_* DEĞİŞMEZ): kompresör açıklığı (3358–3740 × −385…−75) KAPANDI → TEK PARÇA DÜZ
    4 mm sac 2510–3990 × −420…−15, üst yüz 1348 · takoz delikleri HAVŞALI (DIN 7991 M6 havşa başlı vida, baş üst yüzle aynı düzlem: rafın üstünde somun /
    çıkıntı yok). Yük yolu: fırın üst sacı → alt takoz (1305–1315) → ışınım kalkanı (1315–1315,8) → üst takoz (1315,8–1344) → RAF SACI (1344–1348, takozların
    ÜSTÜNDE) → kompresör ayakları / pizza yığını. firin_tp10_cad_v10 dosyasına yazılmaz: FT.kur() bu modülde sarılır (raf_duzelt), montaj FU'yu FT.kur()'dan önce içe alır.
  · KOMPRESÖRÜN KENDİ AYAKLARI (JUN-AIR OF302-15B · ÜRÜNÜN PARÇASI, satın alınan kompresörle gelir): 4 × kompresor_JUNAIR_OF302_15B_ayak_N = tank ayak sacı (tanka
    üretici kaynağı) + kauçuk titreşim ayağı Ø40 × 20 (föy toplam yüksekliği 510 = tank + motor 490 + ayak 20) · ayak altı = raf üstü 1348.
    → tank 20 mm YUKARI (KOMP_KALDIR): montajda KOMP_KAY[1] 976 → 996 (HAVA_KOMPRESOR başka dosyada: hat3_montaj_vN · AYRICA RAPOR).
    Tavan sacı altı 1860,5 · motor üstü 1838 + 20 = 1858 → 2,5 mm boşluk (servis: kompresör düz raf üstünde öne kayar, kaldırma gerekmez).
v3.7 (1 Eki 2026 · Claude · YEREL) — DAVLUMBAZ FANI + FİLTRELER (eksik taraması: F_DAVLUMBAZ kutusunda fan / filtre yoktu · bizim parçamız, fırın DEĞİL):
  AKIŞ: davlumbaz kutusu ön yüzündeki 9 emiş yarığı (x 3390–3950 · y 1520–1730, kompresörün arkası) → EN 16282-6 yağ (alev) filtresi 500 × 400 × 25 AISI 304
  → aktif karbon kaseti 500 × 400 × 30 → kutu içi plenum → FAN Systemair RS 30-15 sileo (300 × 150 dikdörtgen kanal fanı · 230 V 51 W · 464 m³/h maks ·
  hava ≤ 70 °C · 6,2 kg · föy ds-rs-30-15-sileo) yatay, emişi +x (plenuma) → dikey kanal 300 × 200 (kutu içinde y 1330 → 1790, yan ağzı 298 × 148) →
  atış kanalı (FU0) → U_F baca uzantısı → bina. ÇALIŞMA NOKTASI (föy): 210 m³/h @ 228 Pa (filtre ~100 + karbon ~80 + kanal / bina ~50 Pa — VARSAYIM) ·
  gereken ≈ 195 m³/h (F kabini ısı yükü ≈ 600 W VARSAYIM, oda + 10 K) · fan altta 2 konsolda, davlumbaz tabanına vidalı. Fan kablosu: arka sacın
  'davlumbaz_fani' M20 rakoru (x 2600 · y 1825) → fan klemens kutusu (sözleşme DAV_FAN_KLEMENS) · 230 V besleme kaynağı AÇIK (ana panoda raf yeri yok).
  ⚠ RS 30-15 hava sınırı 70 °C: davlumbaz F kabini havasını emer (yanma gazı yok · elektrikli fırın); fırın tünel buharı > 70 °C ise Systemair KBT 160EC
  (120 °C, 26 kg, 437 × 384 × 473) kutuya SIĞMAZ (iç yükseklik 472) → kutu büyütülmeli (Kemal kararı)."""
import os, sys

H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_hesap_v1 as HS
import firin_ust_kabin_cad_v1 as FU0

DX = HS.KOMP_DX                                   # −241


def _x(t, i=(0, 1)):
    t = list(t)
    for j in i: t[j] = t[j] + DX
    return tuple(t)


FU0.KIRIS_X = HS.KIRIS_X
FU0.DIKME_X = (HS.KIRIS_X,)
FU0.TANK = dict(FU0.TANK, x=(FU0.TANK["x"][0] + DX, FU0.TANK["x"][1] + DX))
FU0.KOMP_ZARF = _x(FU0.KOMP_ZARF)
FU0.KOMP_GERCEK = _x(FU0.KOMP_GERCEK)
FU0.AYAK_X = tuple(x + DX for x in FU0.AYAK_X)            # üreticinin 4 ayağı tankla birlikte (3384 · 3714)
FU0.TAVA_K = dict(FU0.TAVA_K, x=(HS.KOMP_ACIKLIK_X[0] + 1.0, HS.KOMP_ACIKLIK_X[1] - 1.0))
FU0.ANA = [(x + DX if abs(x - 3790.0) < 1e-6 else x, y, z) for x, y, z in FU0.ANA]
FU0.K_DALI = [(x + DX if abs(x - 3790.0) < 1e-6 else x, y, z) for x, y, z in FU0.K_DALI]
FU0.RAKOR = [(a, rx + DX if a == "kompresor" else rx, ry, rd, rn, n) for a, rx, ry, rd, rn, n in FU0.RAKOR]
FU0.KAYIT_TAKOZ_X = (2875.0, 3250.0, 3625.0)      # ön alt kayıt takozları (y 1305–1308, z +27…+57) · kompresör öne çekilirken 1348 üstünde: değişmez
assert FU0.TAVA_K["x"][0] >= FU0.KIRIS_X[1] + 2.0 and FU0.TANK["x"][0] >= FU0.TAVA_K["x"][0] and FU0.TANK["x"][1] <= FU0.TAVA_K["x"][1]
assert HS.YAG_X[0] >= HS.KOMP_ACIKLIK_X[1] + 2.0 and FU0.PIZZA[1] <= FU0.KIRIS_X[0] - 2.0

for _k, _v in list(vars(FU0).items()):
    if _k.startswith("__") and _k.endswith("__"):
        continue
    globals()[_k] = _v
PARCALAR = FU0.PARCALAR

# ================================================================ v3.6 · DÜZ RAF + KOMPRESÖRÜN KENDİ AYAKLARI ================================================================
RAF_UST = 1348.0                                  # = firin_tp10 UST_RAF_Y[1] (raf üst yüzü · pizza yığını + kompresör ayakları buraya basar)
KOMP_AYAK_H = 20.0                                # JUN-AIR kauçuk titreşim ayağı Ø40 × 20 (föy 510 − tank + motor 490) [ölçü VARSAYIM: föyden teyit]
KOMP_AYAK_R = 20.0
KOMP_KALDIR = KOMP_AYAK_H                         # tank + motor + vana +20 (montaj KOMP_KAY[1] 976 → 996)
# tank dünyada (montaj v3.5 dökümü _dunya_tam, KALDIRMADAN önce): x 3354,6–3743,4 · y 1348,0–1652,4 · z −383,3…−76,7 → Ø ≈ 305, eksen x
TANK_V36 = dict(x=(3354.6, 3743.4), yc=1500.2 + KOMP_KALDIR, zc=-230.0, r=152.2)
AYAK_SAC = dict(w=40.0, t=30.0)                   # tank ayak sacı (üretici kaynağı) · kauçuk ayağın üstünde 40 × 30 taban, tanka kadar (VARSAYIM föy)
F_KOMP_DUS = ("f_komp_tavasi", "f_komp_titresim_takozu_", "f_komp_urun_ayagi_")
BIRIMLER = [(k, a) if k not in ("F_KOMP_AYAK", "F_DAVLUMBAZ") else
            ("F_DAVLUMBAZ", "Davlumbaz (bizim) · 304 1,5 kutu x 2501,5–3998,5 · y 1315–1790 · z −827…−440 · v3.7: EN 16282-6 yağ filtresi 500 × 400 + aktif karbon (emiş yarıklarının arkası) · "
                            "Systemair RS 30-15 sileo kanal fanı (230 V 51 W · 210 m³/h @ 228 Pa) → kutu içi dikey kanal 300 × 200 → atış kanalı → U_F baca") if k == "F_DAVLUMBAZ" else
            ("F_KOMP_AYAK", "Kompresör JUN-AIR OF302-15B'nin KENDİ 4 ayağı (ürünün parçası: tanka kaynaklı ayak sacı + kauçuk titreşim ayağı Ø40 × 20 · föy ölçüsü VARSAYIM) · "
                            "fırın üstü DÜZ rafa (üst 1348) doğrudan basar · v3.6: kompresör tavası, raf açıklığı ve bizim eklediğimiz takoz / ayaklar KALKTI · tank 20 yukarı (ayak altı 1348)")
            for k, a in FU0.BIRIMLER]
BIRIM_MODUL = {k: "D" for k, _a in BIRIMLER}


def kompresor_ayaklari_v36():
    """JUN-AIR OF302-15B'nin 4 ayağı (ÜRÜNÜN): kauçuk ayak 1348–1368 + tank ayak sacı 1368 → tank yüzeyi (kaldırılmış tankla kesilir)"""
    B = "F_KOMP_AYAK"
    t = TANK_V36
    tank = FU0.silx(t["yc"], t["zc"], t["r"], t["x"][0] - 10.0, t["x"][1] + 10.0)
    y0, y1 = RAF_UST, RAF_UST + KOMP_AYAK_H
    i = 0
    for xa in FU0.AYAK_X:
        for za in FU0.AYAK_Z:
            ayak = FU0.sily(xa, za, KOMP_AYAK_R, y0, y1)
            sac = FU0.kut(xa - AYAK_SAC["w"] / 2.0, xa + AYAK_SAC["w"] / 2.0, y1, t["yc"], za - AYAK_SAC["t"] / 2.0, za + AYAK_SAC["t"] / 2.0).cut(tank)
            FU0.ekle("kompresor_JUNAIR_OF302_15B_ayak_%d" % i, ayak.union(sac), "koyu", B,
                     kaynak="JUN-AIR OF302-15B kendi ayağı (ÜRÜNÜN · tankla gelir) — ölçü VARSAYIM (föy: toplam yükseklik 510, ayak Ø40 × 20)",
                     bom=("Kompresör ayağı JUN-AIR OF302-15B (ÜRÜNÜN KENDİ AYAĞI: tank ayak sacı + kauçuk titreşim ayağı Ø40 × 20, M8)", 4, "kompresörle birlikte gelir",
                          "v3.6 · fırın üstü DÜZ rafa (1348) doğrudan basar · tavası / raf açıklığı / bizim takozumuz YOK · CE/PED tankına üretici dışında kaynak yok", "SET İÇİNDE") if i == 0 else None)
            i += 1


# ================================================================ v3.7 · DAVLUMBAZ FANI + FİLTRELER ================================================================
DAV_IC = (FU0.DAV[0] + FU0.SAC, FU0.DAV[1] - FU0.SAC, FU0.DAV[2] + FU0.SAC, FU0.DAV[3] - FU0.SAC, FU0.DAV[4] + FU0.SAC, FU0.DAV[5] - FU0.SAC)   # 2503–3997 · 1316,5–1788,5 · −825,5…−441,5
DIKEY = dict(x=(2952.0, 3248.0), y=(1330.0, 1790.0), z=(-718.0, -522.0), t=1.5)          # kutu içi dikey kanal (üstü atış ağzına geçer, FU0 atış kanalı 1790'da başlar)
FAN_RS = dict(L=402.0, fl=15.0, gov=(340.0, 190.0), fl_dis=(320.0, 170.0), fl_ic=(298.0, 148.0), kk=(80.0, 60.0, 27.0))   # Systemair RS 30-15 sileo (föy harf ölçüleri A 402 · C 340 · D 190 · E 320 · F 170 · G 298 · H 148 · B 217 = gövde + klemens kutusu) — harf eşlemesi VARSAYIM
FAN_YC, FAN_ZC = 1491.0, -620.0                                                            # kanal ekseni (ağız 298 dik y · 148 z)
FAN_X0 = DIKEY["x"][1]                                                                      # çıkış flanşı dikey kanalın +x yüzüne dayanır (3248) · emiş 3650'de +x'e bakar
FILTRE_YAG = dict(x=(3420.0, 3920.0), y=(1350.0, 1750.0), t=25.0)                           # EN 16282-6 tip A · 500 × 400 × 25 (ölçü listeden VARSAYIM; 500 × 500 kutuya sığmaz: iç 472)
KARBON_T = 30.0
CERCEVE = dict(x=(3385.0, 3955.0), y=(1335.0, 1765.0))                                       # filtre çerçevesi: emiş yarıklarını (3390–3950 · 1520–1730) tamamen örter → by-pass yok
DAV_FAN_KLEMENS = (3460.0, 1490.0, FAN_ZC - FAN_RS["gov"][1] / 2.0 - FAN_RS["kk"][2])      # elektrik ajanı: fan klemens kutusunun dış yüzü (−z)


def davlumbaz_v37():
    B = "F_DAVLUMBAZ"
    x0, x1, y0, y1, z0, z1 = DAV_IC
    # ---- dikey kanal (kutu içi): 304 1,5 · alt kapalı · +x yüzünde fan ağzı 298 × 148 ----
    dx0, dx1 = DIKEY["x"]; dy0, dy1 = DIKEY["y"]; dz0, dz1 = DIKEY["z"]; t = DIKEY["t"]
    dk = FU0.kut(dx0, dx1, dy0, dy1, dz0, dz1).cut(FU0.kut(dx0 + t, dx1 - t, dy0 + t, dy1 + 1.0, dz0 + t, dz1 - t))
    gy, gz = FAN_RS["fl_ic"]
    dk = dk.cut(FU0.kut(dx1 - t - 1.0, dx1 + 1.0, FAN_YC - gy / 2.0, FAN_YC + gy / 2.0, FAN_ZC - gz / 2.0, FAN_ZC + gz / 2.0))
    FU0.ekle("f_davlumbaz_dikey_kanal", dk, "sac", B, kaynak="v3.7",
             bom=("Davlumbaz dikey kanalı 304 1,5 · 296 × 196 × 460 · alt kapalı · yanda 298 × 148 fan ağzı", 1, "abkant + kaynak",
                  "v3.7 · üstü kutunun atış ağzına geçer (atış kanalı 1790'da) · alt ucu kutu tabanına 2 köşebentle", "ÜRETİM"))
    for i, xa in enumerate((dx0 + 20.0, dx1 - 50.0)):
        FU0.ekle("f_davlumbaz_dikey_kanal_ayagi_%d" % i, FU0.kut(xa, xa + 30.0, y0, dy0, dz0 + 20.0, dz1 - 20.0), "paslanmaz", B,
                 bom=("Dikey kanal ayağı 304 kutu 30 × 13,5 × 156", 2, "kesim", "kutu tabanına kaynaklı", "ÜRETİM") if i == 0 else None)
    # ---- fan RS 30-15 (yatay · x boyunca · çıkış −x → dikey kanal · emiş +x) ----
    L, fl = FAN_RS["L"], FAN_RS["fl"]; cy, cz = FAN_RS["gov"]; ey, ez = FAN_RS["fl_dis"]; iy, iz = FAN_RS["fl_ic"]
    fa, fb = FAN_X0, FAN_X0 + L
    fan = FU0.kut(fa + fl, fb - fl, FAN_YC - cy / 2.0, FAN_YC + cy / 2.0, FAN_ZC - cz / 2.0, FAN_ZC + cz / 2.0)
    for xa_, xb_ in ((fa, fa + fl), (fb - fl, fb)):
        fan = fan.union(FU0.kut(xa_, xb_, FAN_YC - ey / 2.0, FAN_YC + ey / 2.0, FAN_ZC - ez / 2.0, FAN_ZC + ez / 2.0))
    fan = fan.cut(FU0.kut(fa - 1.0, fa + fl + 5.0, FAN_YC - iy / 2.0, FAN_YC + iy / 2.0, FAN_ZC - iz / 2.0, FAN_ZC + iz / 2.0))     # çıkış ağzı
    fan = fan.cut(FU0.kut(fb - fl - 5.0, fb + 1.0, FAN_YC - iy / 2.0, FAN_YC + iy / 2.0, FAN_ZC - iz / 2.0, FAN_ZC + iz / 2.0))     # emiş ağzı
    kx, ky, kz = FAN_RS["kk"]
    fan = fan.union(FU0.kut(DAV_FAN_KLEMENS[0] - kx / 2.0, DAV_FAN_KLEMENS[0] + kx / 2.0, DAV_FAN_KLEMENS[1] - ky / 2.0, DAV_FAN_KLEMENS[1] + ky / 2.0,
                            DAV_FAN_KLEMENS[2], FAN_ZC - cz / 2.0))
    FU0.ekle("f_davlumbaz_fani_Systemair_RS_30-15_sileo", fan, "celik", B,
             kaynak="Systemair RS 30-15 sileo (77284) · föy ds-rs-30-15-sileo-en.pdf: 230 V 51 W · 464 m³/h · hava ≤ 70 °C · 6,2 kg · 210 m³/h @ 228 Pa",
             bom=("Davlumbaz fanı Systemair RS 30-15 sileo (77284) · dikdörtgen kanal fanı 300 × 150 · 230 V 51 W · 464 m³/h · ≤ 70 °C", 1,
                  "katalog (systemair.com) · dış ölçü föy harfleri A 402 · C 340 · D 190 · E 320 · F 170 (eşleme VARSAYIM)",
                  "v3.7 · çalışma 210 m³/h @ 228 Pa (föy) · hız kontrolü (5 kademe trafo / tristör) · 230 V besleme AÇIK", "SATIN ALMA"))
    for i, xa in enumerate((fa + 50.0, fb - 80.0)):
        FU0.ekle("f_davlumbaz_fan_konsolu_%d" % i, FU0.kut(xa, xa + 30.0, y0, FAN_YC - cy / 2.0, FAN_ZC - cz / 2.0, FAN_ZC + cz / 2.0), "paslanmaz", B,
                 bom=("Fan konsolu 304 lama 30 × 4,5 × 190 (kutu tabanına kaynaklı, fana 2 × M8 titreşim takozlu)", 2, "kesim", "", "ÜRETİM") if i == 0 else None)
    # ---- filtre çerçevesi + EN 16282-6 yağ filtresi + aktif karbon kaseti (emiş yarıklarının arkası) ----
    zf1 = z1; zf0 = zf1 - FILTRE_YAG["t"]; zk0 = zf0 - KARBON_T
    fx0, fx1 = FILTRE_YAG["x"]; fy0, fy1 = FILTRE_YAG["y"]
    cer = FU0.kut(CERCEVE["x"][0], CERCEVE["x"][1], CERCEVE["y"][0], CERCEVE["y"][1], zk0, zf1).cut(FU0.kut(fx0, fx1, fy0, fy1, zk0 - 1.0, zf1 + 1.0))
    FU0.ekle("f_davlumbaz_filtre_cercevesi", cer, "paslanmaz", B,
             bom=("Filtre çerçevesi 304 1,5 (U ray, önden sürme) · 570 × 430 × 55", 1, "abkant + kaynak", "v3.7 · ön yüz iç tarafına perçin · emiş yarıklarının hepsini örter (by-pass yok)", "ÜRETİM"))
    FU0.ekle("f_davlumbaz_yag_filtresi_EN16282", FU0.kut(fx0, fx1, fy0, fy1, zf0, zf1), "paslanmaz", B,
             kaynak="EN 16282-6 tip A (F-1) alev / yağ filtresi AISI 304 · 500 × 500 × 25 föyü: 500 m³/h @ 100 Pa (gastroplus24) — 500 × 400 boyu VARSAYIM",
             bom=("Yağ (alev) filtresi EN 16282-6 tip A · AISI 304 labirent · 500 × 400 × 25", 1, "katalog · bulaşık makinesinde yıkanır",
                  "v3.7 · 500 × 500 standardı kutuya sığmaz (iç yükseklik 472) → 500 × 400 (ölçü teyit)", "SATIN ALMA"))
    FU0.ekle("f_davlumbaz_karbon_filtre", FU0.kut(fx0, fx1, fy0, fy1, zk0, zf0), "koyu", B,
             bom=("Aktif karbon kaseti 500 × 400 × 30 (koku)", 1, "sarf · 3–6 ayda değişim", "v3.7 · ölçü / basınç kaybı VARSAYIM (~80 Pa)", "SARF"))


def kur():
    FU0.kur()
    PARCALAR[:] = [p for p in PARCALAR if not p["ad"].startswith(F_KOMP_DUS)]
    kompresor_ayaklari_v36()
    davlumbaz_v37()
    return PARCALAR


def dunya(p):
    return FU0.dunya(p)


# ---------------- RAF: firin_tp10_cad_v10.kur() sarılır (montaj FT = firin_tp10_cad_v10, FU'yu FT.kur()'dan ÖNCE içe alır) ----------------
def raf_duzelt(FT):
    """FT.PARCALAR içindeki 'ust_raf'ı açıklıksız düz sacla değiştirir (adı / birimi aynı → montaj delikleri ve denetimleri adla bulur) · havşalı M6 delikler"""
    y0, y1 = FT.UST_RAF_Y
    assert abs(y1 - RAF_UST) < 1e-6, (FT.UST_RAF_Y, RAF_UST)
    raf = FT.kut(FT.X_F0 + 10.0, FT.X_F1 - 10.0, y0, y1, -420.0, -15.0).val()
    hv = 2.9                                                                    # DIN 7991 M6: baş Ø12 · 90° havşa → 4 mm sacta 2,9 derin, baş üst yüzle aynı
    for x, z in FT.TAKOZ_XZ:
        raf = raf.cut(cq.Solid.makeCylinder(3.3, (y1 - y0) + 2.0, cq.Vector(x, y0 - 1.0, z), cq.Vector(0, 1, 0)))
        raf = raf.cut(cq.Solid.makeCone(3.3, 6.2, hv + 0.01, cq.Vector(x, y1 - hv, z), cq.Vector(0, 1, 0)))
    n = 0
    for p in FT.PARCALAR:
        if p["ad"] == "ust_raf":
            p["wp"] = cq.Workplane(obj=raf.clean()); n += 1
            p["bom"] = ("Fırın üstü raf 4 mm · TEK PARÇA DÜZ (v3.6: kompresör açıklığı kalktı)", 1, "304 · 1480 × 405 · 10 havşalı M6 delik",
                        "takozların ÜSTÜNDE (1344–1348) · DIN 7991 M6 havşa başlı vidayla takozlardan fırın üst sacındaki perçin somunlara · üst yüz düz (somun / çıkıntı yok) · "
                        "SOLDA pizza kutusu yedeği 320 kutu 51 kg + SAĞDA kompresör 25 kg (kendi 4 ayağıyla doğrudan rafta) = 76 kg · JUN-AIR ortam sınırı 40 °C [föy]")
        elif p["ad"].startswith("ust_raf_takozu_ust_") and p.get("bom"):
            p["bom"] = ("Raf takozu üst Ø16 × 28,2", 10, "304 boru 16 × 1,5 → torna", "kalkan ile raf arasında · raf ÜSTÜNDE · üstten DIN 7991 M6 havşa başlı vida geçer (somun yok)")
    assert n == 1, n


import firin_tp10_cad_v10 as _FT10
if not getattr(_FT10.kur, "_v36_raf", False):
    _FT10_kur0 = _FT10.kur

    def _ft10_kur_v36(*a, **k):
        r = _FT10_kur0(*a, **k)
        raf_duzelt(_FT10)
        return r
    _ft10_kur_v36._v36_raf = True
    _FT10.kur = _ft10_kur_v36
