# -*- coding: utf-8 -*-
# AUTOKITCH — 1 · STORE v4 (12 Eyl 2026) — 2800 mm · 4 KAPI · DİKEY BÖLGELER
# v1/v2/v3 DEĞİŞMEDİ; bu sürüm 1_STORE_v4 altında.
#
# v3'ten FARKI — bölgeler YATAY değil DİKEY:
#   v3: 1400 mm, 2 kolon, alt buzluk (−18) / üst dolap (+3), dipte kaset katı (4 TOPPING kabı)
#   v4: 2800 mm, 4 kolon (her biri 620 çekmece), kolon bazlı bölge, KASET KATI YOK
#       (harç artık 3 gün +3'te duruyor ve kasetler TOPPING'de — STORE'a kaset girmiyor)
#
# NEDEN 2800 (2100 DEĞİL): iki çekmece AÇIKLIĞI arasında zorunlu ALIN 33 var
#   (bindirme 15 + fuga 3 + bindirme 15 — bkz. on_yuz()). Yani n çekmece = Σh + 33·(n−1).
#   Açıklık bandı kolon başına 182,5..1645 = 1462,5 mm. 3 günlük stok 3,50 kolon tutuyor
#   → 3 kolon YETMEZ, 4 kolon şart. (Alın hesaba katılmadığında 3 kolon sanılmıştı.)
#
# BÖLGE KURGUSU (12 Eyl kararları):
#   K1  BÖLMELİ kolon — alt −18 / üst +3, aralarında yatay ayırıcı bant 42 (sac 1 + PU 40 + sac 1)
#       alt: DONMUŞ PİDE 7 × 20 = 140 top  ("pide 2 gün donmuş + 1 gün taze" kuralı)
#       üst: LAHMACUN 3 × 30 = 90 top
#   K2  tam +3 — TAZE PİDE 4 × 20 = 80 top (1 gün) · LAHMACUN 8 × 30 = 240 top
#   K3  tam +3 — LAHMACUN 8 × 30 = 240 top · İÇECEK 3 × 63 = 189 kutu
#   K4  tam +3 — İÇECEK 5 × 63 (biri TATLI) · 1 L 2 × 42 = 84 şişe
#
# 3 GÜN KONTROLÜ (günde 70 pide + 141 lahmacun):
#   pide     140 donmuş + 80 taze = 220 top → 3,14 gün ✓
#   lahmacun 19 çekmece × 30      = 570 top → 4,04 gün ✓  (mayasız hamur, dolapta 1 hafta dayanır)
#   içecek   7 × 63 = 441 kutu + 84 şişe    → 1 haftadan uzun ✓   · tatlı 1 çekmece
#   KOLON DOLULUĞU: K1 %96 · K2 %97 · K3 %98 · K4 %100 — boş yer yok
#
# LAHMACUN TEPSİSİ (yeni, sw_lahmacun.py): GN 2/1'e 5×6 = 30 çukur Ø98 adım 105 (110 g top Ø75).
#   Pide tepsisi aynı GN 2/1'e 20 top alıyor. Bu %50 fark TAM BİR KOLON kazandırıyor
#   (20 top/çekmece ile 5 kolon = 3500 mm gerekirdi).
#
# GEOMETRİ: 4 kolon × 620 = 2480 · 3 dikey bölme × 65 = 195 · iç açıklık 2675 (62,5..2737,5)
#   K1 | K2 bölmesi −18 ile +3'ü ayırır → PU 63 dolgu
#   teknik bölme 250 (1720..1970): 4 soğutma grubu + pano · 40 çekmece sürücüsü
#   her açıklık contalı: bindirme 15 + fuga 3 + bindirme 15 = alın 33 · KULP YOK
import sys, os, io, json, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE_v4"); CEKD = os.path.join(ROOT, "cekmece")
W, PU = 2800.0, 60.0
SOVE, BIND, FUGA = 45.0, 15.0, 3.0
CZ0, CZ1 = -15.0, 0.0            # conta bölgesi (profil 21 × 18,5 · kanal 6,3 · diş 8,3; sıkışmış 15)
FRZ0, FRZ1 = -16.0, -15.0        # ön çerçeve sacı 1,0
WO = 620.0
ALIN = 2*BIND + FUGA                 # 33 — iki cekmece ACIKLIGI arasindaki zorunlu mesafe
K1X, K2X, K3X, K4X = 62.5, 747.5, 1432.5, 2117.5   # dort kolonun sol kenari (her biri WO=620)
BOLME = ((682.5, 747.5), (1367.5, 1432.5), (2052.5, 2117.5))   # 3 dikey bolme x 65
KOLON = ((K1X, "K1"), (K2X, "K2"), (K3X, "K3"), (K4X, "K4"))
CELL0, CELL1 = 182.5, 1660.0     # hücre alt tabanı · üst hücre tavanı
ACIK_UST = CELL1 - BIND          # 1645 — en ustteki acikligin tavani (on yuz bindirmesi CELL1'de biter)
AYR0, AYR1 = 1203.5, 1245.5      # ayırıcı bant 42 — YALNIZ K1 ICINDE (alt -18 / ust +3)
TEK0 = 1720.0                    # teknik bölme tabanı (1720..1970 = 250)
CERC_Y0 = CELL0 - BIND           # 167,5 — on cerceve sacinin alt kenari (v3'te MENT_Y idi)
TIP = {"1L": 300.0, "icecek": 132.0, "hamur88": 88.0, "donmus115": 115.0,
       "lahm88": 88.0,                                 # YENI: 30 lahmacun topu (pide tepsisi 20 aliyor)
       "hamur88_alt": 88.0, "donmus115_alt": 115.0}    # kutu ayni, ON YUZU uzun (cephe hizasi)
# alt bindirme: normalde BIND(15). Kolon dibindeki iki cekmecede on yuz asagi uzatiliyor ki
# sol kolondaki komsusuyla ayni hizada bitsin (Kemal: "merdiven olmus").
ALT_BIND = {"hamur88_alt": 40.0,      # on yuz alti 670 = 1 L cekmecesinin on yuz alti
            "donmus115_alt": 49.0}    # on yuz alti 148,5 = klape on yuzunun alti
# KLAPE — 90° AÇILIR VE AÇIK İÇ YÜZÜ KASET RAFI İLE AYNI KOTTA (y = KAP_Y = 200) OLMALI.
# Kural: menteşe ekseni (Yh, Zh) için  Yh + Zh = 200  VE klapenin hiçbir noktası eksenin
# ALTINDA olmayacak. Zh = 40 (cephe düzlemi) → Yh = 160. Süpürme hacmi böylece y ≥ 160 · z ≥ 0
# içinde kalır: kabine hiç girmez, alt panele/çerçeve sacına/kaset rafına çarpmaz.
# Klape alt kenarı 163 (menteşe kulağı 160..192 arası, 3 mm fuga).
# Klape alt kenari 166: mentese ekseninden 6 mm uzakta. 163 iken acik klapenin dis saci
# Ø8 mile 1 mm giriyordu (olculdu). 6 > mil yaricapi 4 -> temiz.
KLAPE_H = 307.0    # aciklik 182,5..455,5 · on yuz 148,5..470,5
#           supurme tepesi 472,9 · ustteki donmus rafinin on yuz alti 478,5 -> 5,6 mm pay
MENT_Y, MENT_Z = 142.5, 40.0       # klape menteşe ekseni: açık klapenin iç yüzü = 182,5 = hücre tabanı
ICERIK_KEY = {"1L": "1L", "icecek": "icecek", "hamur88": "taze", "donmus115": "donmus",
              "lahm88": "lahmacun",
              "hamur88_alt": "taze", "donmus115_alt": "donmus"}
# yerleşim: (tip, x0, y0) — açıklık sol-alt köşesi
def _kolon(x0, gruplar, y0=CELL0):
    """bir kolonu alttan yukari dizer. gruplar: [(adet, tip) ...] veya ("ayirici",) isareti.
       ADIM = cekmece yuksekligi + ALIN(33): bindirme 15 + fuga 3 + bindirme 15."""
    out, y = [], y0
    for g in gruplar:
        if g == "ayirici":                 # -18 | +3 bandi: on yuz ustu +15, fuga 3, bant 42, fuga 3, on yuz -15
            y += (BIND + 3.0 + 42.0 + 3.0 + BIND) - ALIN   # ALIN zaten eklenmisti -> fark 45
            continue
        adet, tip = g
        for _ in range(adet):
            out.append((tip, x0, y)); y += TIP[tip] + ALIN
    return out

ORNEK = (
    # K1 — BOLMELI: alt -18 donmus pide · yalitim bandi · ust +3 lahmacun
    _kolon(K1X, [(7, "donmus115"), "ayirici", (3, "lahm88")]) +
    # K2 — +3 : taze pide (1 gunluk) + lahmacun
    _kolon(K2X, [(4, "hamur88"), (8, "lahm88")]) +
    # K3 — +3 : lahmacun + icecek
    _kolon(K3X, [(8, "lahm88"), (3, "icecek")]) +
    # K4 — +3 : icecek (6 kutu + 1 tatli) + 1 L
    _kolon(K4X, [(5, "icecek"), (2, "1L")])
)
KLAPE_ORNEK = []       # KASET KATI KALDIRILDI (12 Eyl): harc 3 gun +3, kasetler TOPPING'de
ACIKLIKLAR = [(x0, x0+WO, y0, y0+TIP[t]) for t, x0, y0 in ORNEK]

# ---- KAPASITE DENETIMI (uretim oncesi, SolidWorks'e girmeden) ----
_TOP = {"donmus115": 20, "hamur88": 20, "lahm88": 30}            # cekmece basina hamur topu
_say = lambda t: sum(1 for a, _, _ in ORNEK if a == t)
for _t, _x, _y in ORNEK:
    assert CELL0 <= _y and _y + TIP[_t] <= ACIK_UST, ("TASIYOR", _t, _x, _y, _y + TIP[_t])
assert len(ORNEK) == 40, len(ORNEK)
PIDE_TOP = (_say("donmus115") + _say("hamur88")) * 20
LAHM_TOP = _say("lahm88") * 30
if __name__ == "__main__":
    print("STORE v4 · W=%.0f · 4 kolon · %d cekmece" % (W, len(ORNEK)))
    print("  pide     %3d top (donmus %d + taze %d cekmece) -> %.1f gun" %
          (PIDE_TOP, _say("donmus115"), _say("hamur88"), PIDE_TOP / 70.0))
    print("  lahmacun %3d top (%d cekmece x 30)             -> %.1f gun" %
          (LAHM_TOP, _say("lahm88"), LAHM_TOP / 141.0))
    print("  icecek   %3d kutu (%d cekmece x 63) + 1 L %d sise (%d x 42)" %
          (_say("icecek") * 63, _say("icecek"), _say("1L") * 42, _say("1L")))
    for _x, _ad in KOLON:
        _c = [(t, y) for t, xx, y in ORNEK if xx == _x]
        _dolu = (max(y + TIP[t] for t, y in _c) - CELL0) / (ACIK_UST - CELL0)
        print("  %s: %2d cekmece · %%%.0f dolu" % (_ad, len(_c), 100 * _dolu))

def _zon(x0, y0):
    """cekmecenin ait oldugu SICAKLIK BOLGESI — yalniz K1 ikiye bolunmus, K2/K3/K4 tek parca."""
    return (x0, y0 < AYR0) if x0 == K1X else (x0, True)

def enalt():
    """her bölge için sıranın EN ALTTAKİ çekmecesinin y0'ı.
       kayış o çekmecede YANDAN (dy=73), diğerlerinde ALTTAN (dy=3) geçer."""
    E = {}
    for tip, x0, y0 in ORNEK:
        k = _zon(x0, y0); E[k] = min(E.get(k, 1e9), y0)
    return E

def kayis_dy(E, x0, y0):
    return 73.0 if y0 == E[_zon(x0, y0)] else 3.0
ICERIK = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cekmece_icerik.json"), encoding="utf-8"))

# ---------------------------------------------------------------- ortak ön yüz
def on_yuz(st, p, h, alt_bind=BIND, conta_ic=0.0, conta_ust=BIND):
    """bindirmeli contalı ön yüz — yerel: açıklık sol-alt köşesi (0,0); ön yüz z 0..40, conta z −15..0
       alt_bind=0  → ALT bindirme yok (klape: alt kenar menteşe ekseninde olmalı, aksi halde
                     açılırken kuyruk kabine geri süpürür)
       conta_ic>0  → alt conta şeridi AÇIKLIĞIN İÇİNDE (0..conta_ic); klapede alt bindirme
                     olmadığı için sızdırmazlık buradan sağlanır
       conta_ust=0 → ÜST conta şeridi YOK. Klape 90° açılınca üst şerit y+15 lik bir EŞİK
                     oluşturup kasetin yolunu kesiyordu; üst conta da KABİNDE sabit."""
    a, b, c, d = -BIND, WO+BIND, -alt_bind, h+BIND
    st.box(p+"on_ic_sac_1.0",  a, b, c, d, 0.0, 1.0)
    st.box(p+"on_pu_37.5",     a, b, c, d, 1.0, 38.5)
    st.box(p+"on_dis_sac_1.5", a, b, c, d, 38.5, 40.0)
    st.box(p+"conta_manyetik_21x18.5", a, b, c, h+conta_ust, CZ0, CZ1,
           [(0.0, WO, conta_ic, h + (conta_ust and 1.0), CZ0-1, CZ1+1)])

# ---------------------------------------------------------------- delikli hizalama sacı
# ESKI: her urun icin ayri halka yuva (YUVA_1L x42 + YUVA_icecek x70 = 112 parca) — halkalarin
# dis caplari komsusuna giriyordu (icecek 11 mm, 1 L 9 mm cakisma).
# YENI: cekmece basina TEK sac, urun basina bir DELIK. Tek lazer kesim + 2 bukum.
# Delik capi = urun capi + 4 · adimlar en az 6 mm et kalacak sekilde secildi.
TEPSI = {
 "icecek": dict(dh=68.0, ax=82.0, az=75.0, h=45.0, urun="KUTU_KOLA_330ml_DIK"),   # kutu Ø66 + 2 pay
 "1L":     dict(dh=90.0, ax=96.0, az=96.0, h=70.0, urun="SISE_KOLA_1L"),          # sise Ø88 + 2 pay
}
KENAR = 6.0      # sac kenari ile en dis delik arasindaki en az et (0 birakilirsa kesik olusmuyor)
# ON KENAR AYRI: en ondeki urunun ON YUZU cekmece contasinin (z −15..0) ARKASINDA kalmali.
# Aksi halde robot urunu ustten tutup DIK kaldirirken urun y=h yi gecer gecmez contanin
# ust bandina giriyor (olculdu: 5 mm ic ice). 13 mm ile kutu on yuzu z = −17 → 2 mm acik.
# icecek adimi 76 -> 75 dusuruldu ki sira sayisi (9) ve kapasite (63) AYNI kalsin.
KENAR_ON = 13.0

def hizalama_saci(st, p, tip, ka, kb, kc):
    """cekmece basina TEK delikli sac + urun ornekleri. Delik izgarasi ici hacme gore hesaplanir."""
    t = TEPSI[tip]; r = t["dh"] / 2.0
    x0, x1 = ka + 3.0, kb - 3.0
    z0, z1 = -3.0, -697.0
    nx = int(((x1 - x0) - 2 * KENAR - t["dh"]) // t["ax"]) + 1
    nz = int((abs(z1 - z0) - KENAR_ON - KENAR - t["dh"]) // t["az"]) + 1
    cx0 = x0 + ((x1 - x0) - ((nx - 1) * t["ax"] + t["dh"])) / 2.0 + r
    X = [cx0 + i * t["ax"] for i in range(nx)]
    Z = [(z0 - KENAR_ON - r) - j * t["az"] for j in range(nz)]
    taban = kc + 2.5                      # tepsi taban sacinin ust yuzu (urun buna oturur)
    h = taban + t["h"]                    # hizalama saci kotu (urunun belden tutuldugu yer)
    st.part(p + "hizalama_saci_1.5",
            [(TP, 'rect',  (x0, x1, -z0, -z1), h, h + 1.5, False),
             (TP, 'circs', [(cx, -cz, r) for cx in X for cz in Z], h - 1.0, h + 2.5, True),
             (FR, 'rect',  (x0, x0 + 1.5, taban, h), z1, z0, False),      # sol bukum bacagi
             (FR, 'rect',  (x1 - 1.5, x1, taban, h), z1, z0, False)])     # sag bukum bacagi
    yol = os.path.join(ARA, "_ortak", t["urun"], t["urun"] + ".SLDASM")
    for cx in X:
        for cz in Z: st.add_instance(yol, offset_mm=(cx, taban, cz))
    return nx, nz


def cekmece(tip):
    """çekmece alt montajı: contalı ön yüz + U kutu + arka + tepsi tabanı + iç ray ×2 +
       kayış pabucu ×2 + reed mıknatısı + İÇERİK (yuva/tepsi + ürün) — kulp YOK"""
    h = TIP[tip]; st = Station(os.path.join(CEKD, "CEKMECE3_" + tip), "CEKMECE3_" + tip); p = "CEK3_%s_" % tip
    on_yuz(st, p, h, alt_bind=ALT_BIND.get(tip, BIND))
    ka, kb, kc, kd = 16.0, WO-16.0, 8.0, h-10.0
    st.prism_z(p+"kutu_U_1.0", [(ka, kd), (ka, kc), (kb, kc), (kb, kd), (kb-1, kd), (kb-1, kc+1), (ka+1, kc+1), (ka+1, kd)], -700.0, 0.0)
    st.box(p+"kutu_arka_1.0", ka+1, kb-1, kc+1, kd, -700.0, -699.0)
    st.box(p+"tepsi_taban_saci_1.5", ka+1, kb-1, kc+1, kc+2.5, -698.0, -3.0)
    st.box(p+"ray_ic_profil_sol_45x12.7", 0.0, 12.7, kc+8, kc+53, -660.0, 0.0)
    st.box(p+"ray_ic_profil_sag_45x12.7", WO-12.7, WO, kc+8, kc+53, -660.0, 0.0)
    st.box(p+"kayis_pabucu_alt", 13.0, 21.0, kc-5.0, kc+1.0, -80.0, -40.0)
    st.box(p+"kayis_pabucu_yan", 13.0, 17.0, min(72.0, kd-8), min(80.0, kd), -80.0, -40.0)
    st.box(p+"miknatis_15x8x3", WO-16.0, WO-8.0, min(72.0, kd-8), min(80.0, kd), -32.0, -27.0)
    if tip in TEPSI:
        nx, nz = hizalama_saci(st, p, tip, ka, kb, kc)
        st.assemble("CEKMECE3_" + tip)
        print("  CEKMECE3_%-10s h=%3.0f · TEK delikli sac, %d x %d = %d delik" % (tip, h, nx, nz, nx*nz))
    else:
        for yol, c in ICERIK[ICERIK_KEY[tip]]:
            if os.path.exists(yol): st.add_instance(yol, center_m=[(c[0]+1)*M, c[1]*M, (c[2]+3)*M])
        st.assemble("CEKMECE3_" + tip)
        print("  CEKMECE3_%-10s h=%3.0f · %3d icerik" % (tip, h, len(ICERIK[ICERIK_KEY[tip]])))

def klape():
    """kaset katı klapesi — 90° AÇILIR, açık iç yüzü kaset rafı ile aynı kotta (y=200).
       ALT BİNDİRME YOK: klapenin alt kenarı = 163, menteşe ekseni y=160 / z=40 (cephe düzlemi).
       Menteşe kulağı z 32..40 · y 160..192: eksenin altında ve önünde madde yok → geri süpürme yok."""
    if not KLAPE_ORNEK:                       # v4: kaset kati yok -> klape uretilmiyor
        print("  KLAPE atlandi (v4'te kaset kati yok)"); return
    st = Station(os.path.join(CEKD, "KLAPE3_KASET"), "KLAPE3_KASET"); p = "KLP3_"
    # conta_ic=-1 → klapede ALT conta seridi YOK (U conta). Acilinca kaset yolunda esik olusturuyordu
    # (olculdu: 90 derecede y 215 = duz yuzeyin 15 mm ustunde). Alt conta KABINDE sabit (S3_klape_alt_conta).
    on_yuz(st, p, KLAPE_H, alt_bind=0.0, conta_ic=-1.0, conta_ust=0.0)
    vy = MENT_Y - KLAPE_ORNEK[0][1]                     # menteşe ekseni, klape yerelinde y = −3,0
    for i, kx in enumerate((100.0, 460.0), 1):          # yerel x (global 163..223 · 523..583)
        st.part(p+"mentese_kulagi_%d" % i,
                [(RT, 'rect', (-MENT_Z, -MENT_Z+8.0, vy, vy+32.0), kx, kx+60.0, False),
                 (RT, 'circ', (-MENT_Z, vy, 4.2),                  kx-1.0, kx+61.0, True)])
    st.assemble("KLAPE3_KASET"); print("  KLAPE3_KASET h=%.1f · mentese ekseni y%.0f/z%.0f" % (KLAPE_H, MENT_Y, MENT_Z))

# ---------------------------------------------------------------- kasa
def kasa(st):
    p = "S4_"
    shell(st, p, W, "plint")            # dış kabuk 1,5 + PLİNT 120 (hat boyunca tek hiza; eski 4 ayak iptal)
    ZE = FRZ0
    xi0, xi1 = T_DIS+PU+T_IC, W-T_DIS-PU-T_IC; zi = ZK+T_DIS+PU+T_IC          # 62,5 · 1337,5 · −757,5
    # yalıtımlı kabuk — hepsi çerçeve sacının arkasında biter
    st.box(p+"pu_yan_sol", T_DIS, T_DIS+PU, Y0+T_DIS, TEK0, ZK+T_DIS, ZE)
    st.box(p+"pu_yan_sag", W-T_DIS-PU, W-T_DIS, Y0+T_DIS, TEK0, ZK+T_DIS, ZE)
    st.box(p+"pu_arka", T_DIS+PU, W-T_DIS-PU, Y0+T_DIS, TEK0, ZK+T_DIS, ZK+T_DIS+PU)
    st.box(p+"pu_alt", T_DIS+PU, W-T_DIS-PU, Y0+T_DIS, CELL0-T_IC, zi-T_IC, ZE)
    st.box(p+"ic_yan_sol", xi0-T_IC, xi0, CELL0-T_IC, CELL1+T_IC, zi-T_IC, ZE)
    st.box(p+"ic_yan_sag", xi1, xi1+T_IC, CELL0-T_IC, CELL1+T_IC, zi-T_IC, ZE)
    st.box(p+"ic_arka", xi0, xi1, CELL0-T_IC, CELL1+T_IC, zi-T_IC, zi)
    st.box(p+"ic_alt", xi0, xi1, CELL0-T_IC, CELL0, zi, ZE)
    st.box(p+"ic_tavan", xi0, xi1, CELL1, CELL1+T_IC, zi, ZE)
    st.box(p+"pu_tavan", T_DIS+PU, W-T_DIS-PU, CELL1+T_IC, TEK0-T_IC, zi-T_IC, ZE)
    st.box(p+"teknik_taban", T_DIS+PU, W-T_DIS-PU, TEK0-T_IC, TEK0, zi-T_IC, ZE)
    # ayırıcı bant 42 — YALNIZ K1 ICINDE (alt -18 / ust +3). K2 ve K3 tek sicaklik, bant yok.
    st.box(p+"ayirici_sac_alt_K1", xi0, BOLME[0][0], AYR0, AYR0+T_IC, zi, ZE)
    st.box(p+"ayirici_pu_40_K1",   xi0, BOLME[0][0], AYR0+T_IC, AYR1-T_IC, zi, ZE)
    st.box(p+"ayirici_sac_ust_K1", xi0, BOLME[0][0], AYR1-T_IC, AYR1, zi, ZE)
    # DİKEY BÖLMELER 57,5 (sac 1 + PU 55,5 + sac 1) — A bolmesi -18 ile +3'u ayirdigi icin kalin
    for nm, (b0, b1) in zip("ABC", BOLME):
        st.box(p+"dikey_bolme_sac_sol_"+nm, b0, b0+T_IC, CELL0, CELL1, zi, ZE)
        st.box(p+"dikey_bolme_pu_63_"+nm,   b0+T_IC, b1-T_IC, CELL0, CELL1, zi, ZE)
        st.box(p+"dikey_bolme_sac_sag_"+nm, b1-T_IC, b1, CELL0, CELL1, zi, ZE)
    # ÖN ÇERÇEVE SACI 1,0 — contanın bastığı alın, 18 açıklık lazer kesim
    st.box(p+"on_cerceve_saci_1.0", SOVE, W-SOVE, CERC_Y0, CELL1, FRZ0, FRZ1,
           [(a, b, c, d, FRZ0-1, FRZ1+1) for a, b, c, d in ACIKLIKLAR])
    # söve + sabit paneller: 40 mm sandviç (çerçeve düzleminden ön yüze kadar dolu)
    def sandvic(ad, x0, x1, y0, y1, ic=True):
        if ic: st.box(p+ad+"_ic_sac_1.0", x0, x1, y0, y1, FRZ0, FRZ1)
        st.box(p+ad+"_pu_37.5", x0, x1, y0, y1, FRZ1, ZF0)
        st.box(p+ad+"_dis_sac_1.5", x0, x1, y0, y1, ZF0, ZF1)
    sandvic("sove_sol", T_DIS, SOVE, Y0+T_DIS, H-T_DIS)
    sandvic("sove_sag", W-SOVE, W-T_DIS, Y0+T_DIS, H-T_DIS)
    sandvic("panel_bant_ust", SOVE, W-SOVE, CELL1, TEK0)
    sandvic("panel_bant_alt", SOVE, W-SOVE, Y0+T_DIS, CERC_Y0)      # plint ustu ile en alt cekmecenin on yuzu arasi
    # dış kabuk ön dönüşleri — üst/alt/yan köşeler kapalı
    st.box(p+"dis_yan_on_donus_sol", 0.0, T_DIS, Y0, H, 0.0, ZF1)
    st.box(p+"dis_yan_on_donus_sag", W-T_DIS, W, Y0, H, 0.0, ZF1)
    st.box(p+"dis_ust_on_donus", 0.0, W, H-T_DIS, H, 0.0, ZF1)
    st.box(p+"dis_alt_on_donus", T_DIS, W-T_DIS, Y0, Y0+T_DIS, 0.0, ZF1)
    # teknik bölme servis paneli — bükme 1,5, kenarları kapalı, sökülebilir
    st.prism_y(p+"panel_teknik_bukme_1.5", [(SOVE, ZF1), (SOVE, 0), (SOVE+1.5, 0), (SOVE+1.5, ZF0),
                                            (W-SOVE-1.5, ZF0), (W-SOVE-1.5, 0), (W-SOVE, 0), (W-SOVE, ZF1)], TEK0, H-T_DIS)
    st.box(p+"panel_teknik_alt_donus", SOVE+1.5, W-SOVE-1.5, TEK0, TEK0+1.5, 0.0, ZF0)
    st.box(p+"panel_teknik_ust_donus", SOVE+1.5, W-SOVE-1.5, H-T_DIS-1.5, H-T_DIS, 0.0, ZF0)
    # ---- TEKNİK BÖLME (1720..1970 = 250): 2 soğutma grubu + pano
    # UC GRUP: 1 = K1 alt (-18 buzluk) · 2 = K1 ust + K2 (+3) · 3 = K3 (+3)
    for i, (xk, xf, xc0, xc1) in enumerate((( 200.0,  420.0,  120.0,  580.0),   # G1  K1 alt  -18
                                            ( 900.0, 1120.0,  820.0, 1280.0),   # G2  K1 ust + K2  +3
                                            (1600.0, 1820.0, 1520.0, 1980.0),   # G3  K3  +3
                                            (2300.0, 2520.0, 2220.0, 2680.0)), 1):  # G4  K4  +3
        st.cyl_y(p+"sog%d_kompresor_D120_h200" % i, xk, -200.0, 60.0, 1730.0, 1930.0)   # DİK çalışır (yağ karteri)
        st.box(p+"sog%d_kondenser_dik" % i, xc0, xc1, 1730.0, 1950.0, -810.0, -790.0)   # arka duvara DİK
        st.cyl_z(p+"sog%d_fan_D200" % i, xf, 1830.0, 100.0, -780.0, -740.0)
    # PANO — 3 sogutma grubunun arasindaki serbest banda (x 1150..1600), z -702..-700
    # PANO — z -702..-700 (kompresor z -260..-140, fan -780..-740, kondenser -810..-790: cakismaz)
    st.box(p+"pano_montaj_plakasi", 600, 1350, 1730, 1950, -702, -700)
    st.box(p+"pano_plc_modbus", 1150, 1250, 1880, 1945, -700, -650)
    st.box(p+"pano_guc_kaynagi_24V_20A", 1260, 1340, 1880, 1945, -700, -640)
    for i in range(40):                                                        # 40 cekmece surucusu
        st.box(p+"pano_surucu_%02d" % (i+1), 610+(i % 10)*36, 638+(i % 10)*36,
               1742+(i//10)*32, 1770+(i//10)*32, -700, -670)
    st.box(p+"pano_klemens_rayi", 600, 1350, 1730, 1737.5, -700, -670)
    # ---- EVAPORATÖR + FAN: dört hücre çeyreğinin arka plenumunda
    # üst hücre (+3): modül başına 1 evaporatör · alt hücre (−18): tek evaporatör sağ modülde,
    # sol modül havayı orta bölmedeki iki geçişten alır (kaset katı derinliği evaporatöre yer bırakmıyor)
    # x bandı 300..640 / 920..1260: çekmece tahrik motorlarının x bandı (sol 65..238 · sağ 718..891)
    # ile ÇAKIŞMASIN. Fan evaporatörün ALTINDA, aynı x ekseninde (yandaki motor bandını boşaltır).
    # DORT EVAPORATOR: K1 alt (-18) · K1 ust (+3) · K2 (+3) · K3 (+3).
    # Her biri kendi kolonunun ORTASINDA (x0+310 civari) — cekmece tahrik motorlari x0+17'de,
    # rayllar x0+1 ve x0+605'te; orta bant bos.
    # x: her kolonun sol kenarindan +190..+450. Cekmece 24 V kablosu x0+180'de (D5 -> x0+177,5..182,5)
    # oldugu icin +190 ile 7,5 mm acik kaliyor (olculdu: +180'de 450 mm3 ic ice giriyordu).
    for i, (ex0, ex1, ey0, ey1, fy) in enumerate(((K1X+190, K1X+450, 1040, 1140,  940),   # K1 alt  -18 (bant altinda)
                                                  (K1X+190, K1X+450, 1460, 1560, 1360),   # K1 ust  +3  (fan alti 1270 > bant ustu 1245,5)
                                                  (K2X+190, K2X+450, 1480, 1580, 1380),   # K2      +3
                                                  (K3X+190, K3X+450, 1480, 1580, 1380),   # K3      +3
                                                  (K4X+190, K4X+450, 1480, 1580, 1380)),  # K4      +3
                                                 1):
        st.box(p+"evaporator_%d" % i, ex0, ex1, ey0, ey1, -753, -708)
        st.cyl_z(p+"evap_fan_%d" % i, (ex0+ex1)/2.0, fy, 90, -753, -713)
    # ---- ARKA PLENUM AYIRICI SACI: KALDIRILDI (Kemal, 10 Eyl 2026 — "gerek yok").
    # Onceden z −706..−704,5 te 4 parcali 1,5 sac vardi; evaporator/fan/17 motoru cekmece
    # hacminden ayiriyor ve sogutucu havayi alt/ust yariklardan yonlendiriyordu. Artik yok:
    # arka plenum ile cekmece hacmi tek hacim. (Hava yonlendirmesi gerekirse geri konur.)
    # ---- KASET KATI KALDIRILDI (12 Eyl 2026, Kemal): harc artik 3 gun +3'te duruyor,
    # kasetlerin hepsi TOPPING'de. STORE'a kaset girmiyor -> klape, mentese mili, braket,
    # alt/ust conta ve kaset rafi saci YOK. Kolonun dibi dogrudan en alttaki cekmeceye ait.

# ---------------------------------------------------------------- montaj
def asm():
    st = Station(ROOT, "STORE_v4"); st.load_dir(); print("kasa parca yuklendi:", len(st.parts))
    O = lambda g: os.path.join(ARA, "_ortak", g, g + ".SLDASM")
    for tip, x0, y0 in ORNEK:
        st.add_instance(os.path.join(CEKD, "CEKMECE3_" + tip, "CEKMECE3_" + tip + ".SLDASM"), offset_mm=(x0, y0, 0))
    for x0, y0 in KLAPE_ORNEK:
        st.add_instance(os.path.join(CEKD, "KLAPE3_KASET", "KLAPE3_KASET.SLDASM"), offset_mm=(x0, y0, 0))
    # ---- TAHRİK: motor ARKA PLENUMDA (z −745..−709), ayırıcı sacın ARKASINDA.
    # v3'te motor çekmecenin ÜSTÜNDEKİ 33 mm alın boşluğuna konmuştu; motor 44 mm olduğu için
    # taşıyor ve alttaki çekmecenin kutularına giriyordu (ölçüldü: 1 L üstünde 3,5 mm boşluk,
    # içecek üstünde 0,5 mm İÇ İÇE). Ayrıca kayış x0+77'de, çekmecenin kayış pabucu x0+13..21'de
    # idi → 64 mm açık: tahrik geometrik olarak BAĞLI DEĞİLDİ. v2'deki doğru dizilim geri alındı.
    E = enalt()
    for tip, x0, y0 in ORNEK:
        st.add_instance(O("RAY_DIS_PROFIL"), offset_mm=(x0+1, y0+16, 0))
        st.add_instance(O("RAY_DIS_PROFIL"), offset_mm=(x0+WO-15, y0+16, 0))
        dy = kayis_dy(E, x0, y0)                       # 73 → yan pabuç (sıranın en altı) · 3 → alt pabuç
        st.add_instance(O("KAYIS_GT3_6mm"), offset_mm=(x0+14, y0+dy, -40))
        st.add_instance(O("MOTOR_TAHRIK_GRUBU"), offset_mm=(x0+17, y0+dy+1.5, -727))
        st.add_instance(O("KABLO_24V_D5"), offset_mm=(x0+180, y0+dy+1.5, -735))
        st.add_instance(O("SENSOR_REED_D12"), offset_mm=(x0+611, y0+80, -37))   # kutu duvarının dışında, mıknatısın 5 mm arkasında
    # KLAPE TAHRIKI — ACIK KARAR (bkz. mesaj): mentese ekseni cephe duzlemine (y160/z40) alininca
    # eski KLAPE_MOTOR_GRUBU calismiyor. Icerideki itme kolu, klapeye ulasmak icin cerceve sacini
    # ACIKLIGIN DISINDA delmek zorunda kaliyor (olculdu: kol <-> klape ust contasi 1350 mm3,
    # kol <-> hamur cekmecesi contasi 990 mm3). Tahrik cozumu secilene kadar montaja EKLENMIYOR.
    # KASET KATI YOK (12 Eyl): KAP_DETAY ornekleri ve klape sensoru kaldirildi.
    # AYAR AYAKLARI — 2800 mm icin kose 4 + ORTA 2 (on acikligi 2700, tek acikliga 4 ayak az)
    for ax, az in list(AYAK_YERI(W)) + [(W/2.0, -50.0), (W/2.0, ZK+50.0)]:
        st.add_instance(O("AYAK_AYAR_M12"), offset_mm=(ax, 0.0, az))
    st.assemble("STORE_v4")

if __name__ == "__main__":
    faz = sys.argv[1]; sw.CloseAllDocuments(True)
    if faz == "cekmece":
        # ornek: python sw_store_v4.py cekmece lahm88   -> yalniz o tipi uretir
        hedef = sys.argv[2:] if len(sys.argv) > 2 else list(TIP)
        for t in hedef: cekmece(t)
        klape(); Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        st = Station(ROOT, "STORE_v4")
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
        kasa(st); print("kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "parca":                       # ornek: python sw_store_v3.py parca "plint|ayak_"
        import re
        pat = re.compile(sys.argv[2]); st = Station(ROOT, "STORE_v4"); n = [0]
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt") and pat.search(f): os.remove(os.path.join(st.pdir, f))
        orij, ocy, ocz = Station.part, Station.cyl_y, Station.cyl_z
        def sadece(self, fname, ops, _retry=2):
            if not pat.search(fname): return None
            n[0] += 1; return orij(self, fname, ops, _retry)
        def scy(self, fname, *a):                      # silindirler de SUZULUR (eskiden no-op idi:
            if not pat.search(fname): return None      # evap_fan / kompresor yeniden uretilemiyordu)
            n[0] += 1; return ocy(self, fname, *a)
        def scz(self, fname, *a):
            if not pat.search(fname): return None
            n[0] += 1; return ocz(self, fname, *a)
        Station.part, Station.cyl_y, Station.cyl_z = sadece, scy, scz
        kasa(st); print("yeniden uretilen parca:", n[0]); st.exit_sw()
    elif faz == "asm":
        asm(); Station(ROOT, "x").exit_sw()
