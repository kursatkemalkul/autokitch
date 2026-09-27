# -*- coding: utf-8 -*-
"""AUTOKITCH · A + C · MEKANİZMA KAİDESİ 104 · CAD v1 (27 Eyl 2026) — ALÇAK HAT v57 (SPEC_alcak_hat_v57.md · ALCAK_HAT_RESIM1_v4)
Çekmeceli dolabın üstü y 788 (tek düz çizgi) → A (açıcı) ve C (TOPPING) mekanizmaları 104 yukarıda: mekanizma tabanı 892, disk 1000.
KAİDE: çelik çerçeve (AISI 304 kutu profil 40 × 100 × 2, dik) y 788–888 + üst plaka 4 mm 888–892 · A x 8–692 · C x 708–2492 (resim
kutusu x0 + 8 … x1 − 8) · derinlik z −826…−4 (modül 830'un önünde ve arkasında 4 mm pay, VARSAYIM).
NASIL OTURUYOR (topping_cad_v24 yerel y + 892 · topping_uno_cad_v11 dünya y − 168 — montaj v57 kararı):
  · C: TC dis_taban (yerel 0–1,5, x 700–2500, z −830…0) C kaidesinin üst plakasına oturur; TC yan ve arka dış sacları dis_taban'ın
    kenarında (x 700–701,5 · 2498,5–2500 · z −830…−828,5) → kaide 8 / 4 mm içeride (UYARI, rapora bak).
  · A: TC'de A'nın tabanı YOK (dis_taban yalnız C'de). Açıcı kolonu (yerel y 0, x 290–410, z −660…−490) doğrudan A kaidesi üst plakasına
    oturur; mekanizma teknesi ve X motor kaidesi yerel 1,5 / 4,5'ten başlar → A'ya 1,5 mm TABAN SACI (892–893,5, kolon deliği) konur,
    tekne onun üstüne oturur (C'deki dis_taban'ın eşi). Kolonun altında enine profil (x 330–370) + boyuna profil (z −595…−555).
  · TU (UNO + kasetler + soğuk hacim) kaideye değmez: en alt parçası y 1013 (sos yayıcı borusu, disk 1000'in 13 üstü; TC kabuğuna asılı).
KOORDİNAT: DÜNYA. mm. Kütle yükleri VARSAYIM (aşağıda).
"""
import math, os, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
import qr_cad_v1 as QR                    # ortak denetim + BOM yardımcıları

Y_DUZ, Y_MEK = 788.0, 892.0               # dolap üstü · mekanizma tabanı (SPEC)
KAIDE_H = Y_MEK - Y_DUZ                   # 104
PL = 4.0                                  # üst plaka
PR = dict(b=40.0, h=100.0, t=2.0)         # kutu profil 40 × 100 × 2 (dik) → 788 + 100 = 888 · + plaka 4 = 892
A_X, C_X = (8.0, 692.0), (708.0, 2492.0)  # SPEC / resim
KZ = (-826.0, -4.0)                       # VARSAYIM pay 4
A_SAC = 1.5                               # A mekanizma taban sacı (TC dis_taban'ın eşi)
KOLON = dict(x=(290.0, 410.0), z=(-660.0, -490.0))   # TC acici_kolonu (x yerel −410…−290 + 700) · dünya
C_ENINE = (1154.0, 1600.0, 2046.0)        # C enine profil eksenleri (aralık ≈ 446)
C_BOYUNA_Z = (-435.0, -395.0)             # C boyuna orta profil (TC mekanizma teknesinin arka kenarı z −415 altında)
A_BOYUNA_Z = (-595.0, -555.0)             # A boyuna orta profil (kolon ekseni z −575 altında)
YUK = {"KAIDE_A": 60.0, "KAIDE_C": 400.0}   # kg · VARSAYIM: açıcı + tekne ucu · TOPPING TC + TU + dolu kasetler
RO = 7.93e-6                              # kg/mm³ AISI 304

PARCALAR = []
PROFIL_BOM = {}                           # birim → (profil parça sayısı, toplam boy mm) · BOM ile model karşılaştırılır
BIRIMLER = [
    ("KAIDE_A", "A mekanizma kaidesi 104 · x 8–692 · y 788–892 · AISI 304 kutu profil 40 × 100 × 2 + üst plaka 4 · açıcı kolonu altında enine + boyuna profil · 1,5 mm taban sacı 892–893,5 (tekne)"),
    ("KAIDE_C", "C mekanizma kaidesi 104 · x 708–2492 · y 788–892 · AISI 304 kutu profil 40 × 100 × 2 (çevre + 3 enine + boyuna) + üst plaka 4 · TOPPING dis_taban üstüne oturur"),
]
BIRIM_MODUL = {"KAIDE_A": "A", "KAIDE_C": "C"}
ON_BIRIMLER = ()                          # hattın önüne taşan parça YOK (z ≤ −4)
MALZEME = {"paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30), "sac": dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32)}
kut = QR.kut
dunya = QR.dunya


def ekle(ad, wp, mal, birim, bom=None, grup="SABIT", kaynak=""):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom))


def profil_x(x0, x1, z0, z1):
    """x boyunca kutu profil (uçları açık) · y 788–888"""
    t = PR["t"]
    return kut(x0, x1, Y_DUZ, Y_DUZ + PR["h"], z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, Y_DUZ + t, Y_DUZ + PR["h"] - t, z0 + t, z1 - t))


def profil_z(x0, x1, z0, z1):
    """z boyunca kutu profil (uçları açık)"""
    t = PR["t"]
    return kut(x0, x1, Y_DUZ, Y_DUZ + PR["h"], z0, z1).cut(kut(x0 + t, x1 - t, Y_DUZ + t, Y_DUZ + PR["h"] - t, z0 - 1.0, z1 + 1.0))


def cerceve(b, on, x0, x1, enine, boyuna_z):
    bw = PR["b"]; zf, zb = KZ[1] - bw, KZ[0] + bw
    # denetçi düzeltmesi (27 Eyl): BOM_OZET kalemi birim başına ayrı + adet = profil parça sayısı + toplam boy (önce "2 adet · KAIDE_A çerçevesi" yazıyordu)
    xs_ = [x0 + bw] + [v for xc in enine for v in (xc - bw / 2.0, xc + bw / 2.0)] + [x1 - bw]
    boy_ = 2.0 * (x1 - x0) + (2 + len(enine)) * (zf - zb) + sum(xs_[i + 1] - xs_[i] for i in range(0, len(xs_), 2))
    n_ = 4 + len(enine) + len(xs_) // 2
    ilk = [True]
    def bom_():
        if ilk[0]:
            ilk[0] = False
            return ("Kutu profil 40 × 100 × 2 AISI 304 (dik, kaynaklı çerçeve) · %s" % b, n_, "%s çerçevesi · %d parça · toplam boy %.2f m" % (b, n_, boy_ / 1000.0),
                    "üretim · profil ölçüsü VARSAYIM", "ÜRETİM")
        return None
    ekle(on + "_on_profil", profil_x(x0, x1, zf, KZ[1]), "paslanmaz", b, bom=bom_())
    ekle(on + "_arka_profil", profil_x(x0, x1, KZ[0], zb), "paslanmaz", b)
    ekle(on + "_yan_profil_sol", profil_z(x0, x0 + bw, zb, zf), "paslanmaz", b)
    ekle(on + "_yan_profil_sag", profil_z(x1 - bw, x1, zb, zf), "paslanmaz", b)
    xs = [x0 + bw]
    for i, xc in enumerate(enine):
        ekle(on + "_enine_profil_%d" % i, profil_z(xc - bw / 2.0, xc + bw / 2.0, zb, zf), "paslanmaz", b)
        xs += [xc - bw / 2.0, xc + bw / 2.0]
    xs.append(x1 - bw)
    for i in range(0, len(xs), 2):
        ekle(on + "_boyuna_profil_%d" % (i // 2), profil_x(xs[i], xs[i + 1], boyuna_z[0], boyuna_z[1]), "paslanmaz", b)
    ekle(on + "_ust_plaka_4", kut(x0, x1, Y_DUZ + PR["h"], Y_MEK, KZ[0], KZ[1]), "paslanmaz", b,
         bom=("Üst plaka AISI 304 4 mm · %s" % b, 1, "%.0f × %.0f" % (x1 - x0, KZ[1] - KZ[0]), "üretim (lazer) · mekanizma tabanına M6 perçin somunlu", "ÜRETİM"))
    PROFIL_BOM[b] = (n_, boy_)
    return n_, boy_


def kur():
    PARCALAR[:] = []
    cerceve("KAIDE_A", "kaide_A", A_X[0], A_X[1], ((KOLON["x"][0] + KOLON["x"][1]) / 2.0,), A_BOYUNA_Z)
    s = kut(A_X[0], A_X[1], Y_MEK, Y_MEK + A_SAC, KZ[0], KZ[1]).cut(kut(KOLON["x"][0] - 1.0, KOLON["x"][1] + 1.0, Y_MEK - 1.0, Y_MEK + A_SAC + 1.0, KOLON["z"][0] - 1.0, KOLON["z"][1] + 1.0))
    ekle("kaide_A_mekanizma_taban_saci", s, "sac", "KAIDE_A",
         bom=("A mekanizma taban sacı AISI 304 1,5 mm (TC dis_taban'ın A'daki eşi) · açıcı kolonu deliği 122 × 172", 1, "684 × 822", "üretim", "ÜRETİM"))
    cerceve("KAIDE_C", "kaide_C", C_X[0], C_X[1], C_ENINE, C_BOYUNA_Z)
    return PARCALAR


# ---------------------------------------------------------------- TOPPING (TC + TU) ile oturma denetimi ----------------------------------------------------------------
V1_CIKAN = ("pu_", "ic_kabuk", "bolme", "on_kapak", "kapak_contasi", "dozaj_kovani_", "konum_pimi_", "kovan_", "mil_", "motor_", "reduktor_",
            "soket_", "yay_", "ray_", "yuva_etiketi_", "hava_perdesi", "din_ray", "_bom")          # hat_montaj_v56 L193 ile aynı
AKTARMA_TP10 = ("bant_burun_silindiri", "bant_tahrik_silindiri", "bant", "bant_tasiyici_saci", "bant_yan_saci_0", "bant_yan_saci_1", "bant_motoru", "bant_ayagi")
V3_CIKAN = ("kabin_", "tabla_diski", "pide", "baglam_", "teknik_bant_", "kompresor_", "hava_ana_hatti")


def v1_kalir(ad):
    if ad.startswith(("ray_kirisi", "ray_ortu")): return True
    if ad.startswith("surucu_"): return ad in ("surucu_0", "surucu_1", "surucu_2", "surucu_3")
    if ad == "din_ray_ups": return True
    return not ad.startswith(V1_CIKAN)


def topping_denetimi(ps, kontrol):
    import topping_cad_v24 as TC
    TC.PARCALAR[:] = []; TC.modul()
    tc = [p for p in TC.PARCALAR if not p["ad"].startswith("_bom") and v1_kalir(p["ad"]) and p["ad"] not in AKTARMA_TP10 and p["ad"] not in ("on_kapak", "on_kapak_pu", "kapak_contasi")]
    TCD = [(p["ad"], p["wp"].val().translate(cq.Vector(700.0, Y_MEK, 0.0))) for p in tc]
    TCD = [(a, s, s.BoundingBox()) for a, s in TCD]
    bb = {a: B for a, _s, B in TCD}
    # oturma
    dt, ak, tk = bb["dis_taban"], bb["acici_kolonu"], bb["mekanizma_teknesi"]
    kontrol("C: TC dis_taban altı %.1f = kaide C üstü %.0f · dis_taban x %.0f–%.0f / kaide %.0f–%.0f (UYARI: yan sac altları %.0f mm dışarıda)" % (dt.ymin, Y_MEK, dt.xmin, dt.xmax, C_X[0], C_X[1], C_X[0] - dt.xmin),
            abs(dt.ymin - Y_MEK) < 0.01)
    kontrol("A: açıcı kolonu altı %.1f = kaide A üstü %.0f · kolon x %.0f–%.0f z %.0f…%.0f A plakasının içinde" % (ak.ymin, Y_MEK, ak.xmin, ak.xmax, ak.zmin, ak.zmax),
            abs(ak.ymin - Y_MEK) < 0.01 and A_X[0] <= ak.xmin and ak.xmax <= A_X[1] and KZ[0] <= ak.zmin and ak.zmax <= KZ[1]
            and abs(ak.xmin - KOLON["x"][0]) < 0.01 and abs(ak.zmin - KOLON["z"][0]) < 0.01)
    kontrol("A: mekanizma teknesi altı %.1f = A taban sacı üstü %.1f (tekne x %.0f–%.0f)" % (tk.ymin, Y_MEK + A_SAC, tk.xmin, tk.xmax), abs(tk.ymin - Y_MEK - A_SAC) < 0.01)
    aal = [(B.ymin, a) for a, _s, B in TCD if B.xmin < A_X[1] and a not in ("acici_kolonu",)]
    kontrol("A: kolon dışındaki en alçak TC parçası %s y %.1f ≥ %.1f" % (min(aal)[1], min(aal)[0], Y_MEK + A_SAC), min(aal)[0] >= Y_MEK + A_SAC - 0.01)
    kontrol("TC hiçbir parçası %.0f'nin altına inmez (en alçak %.1f)" % (Y_MEK, min(B.ymin for _a, _s, B in TCD)), min(B.ymin for _a, _s, B in TCD) >= Y_MEK - 0.01)
    K = [(p["ad"], dunya(p)) for p in ps]; K = [(a, s, s.BoundingBox()) for a, s in K]
    cak = []
    for a, sa, A in K:
        for c, sc, B in TCD:
            if QR._bbk(A, B):
                v = sa.intersect(sc).Volume()
                if v > 1.0: cak.append((round(v, 1), a, c))
    kontrol("kaide ↔ TOPPING CAD (%d parça, yerel y + 892) çakışma = 0" % len(TCD), not cak, str(cak[:6]))
    import importlib.util as ilu
    sp = ilu.spec_from_file_location("TU11", os.path.join(U, "topping_uno_cad_v11.py"))
    TU = ilu.module_from_spec(sp); sp.loader.exec_module(TU)
    tu = [q for q in TU.P if not q["ad"].startswith(V3_CIKAN)]
    ymin = min(q["sh"].BoundingBox().ymin for q in tu) - 168.0
    xmin = min(q["sh"].BoundingBox().xmin for q in tu) + 700.0
    kontrol("TU (UNO, %d parça, dünya y − 168) en alt %.2f > kaide üstü %.0f · en sol x %.0f (A kaidesine girmez)" % (len(tu), ymin, Y_MEK, xmin), ymin > Y_MEK + A_SAC)


BOM_KLASOR = os.path.join(KOK, "arastirma", "3_KAIDE_v1")
DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-110s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))


if __name__ == "__main__":
    t0 = time.time(); arg = sys.argv[1:]
    ps = kur()
    gec = [p["ad"] for p in ps if not dunya(p).isValid()]
    print("KAİDE v1 · %d parça · katı denetimi: %s · %.0f sn" % (len(ps), "hepsi geçerli" if not gec else gec, time.time() - t0))
    print("DENETİM (kaide_cad_v1)")
    kontrol("katılar geçerli", not gec, ", ".join(gec))
    kontrol("kaide yüksekliği %.0f = profil %.0f + plaka %.0f (dolap üstü %.0f → mekanizma tabanı %.0f)" % (KAIDE_H, PR["h"], PL, Y_DUZ, Y_MEK), abs(PR["h"] + PL - KAIDE_H) < 0.01)
    for kod, xr in (("KAIDE_A", A_X), ("KAIDE_C", C_X)):
        pr_ = [dunya(p).BoundingBox() for p in ps if p["birim"] == kod and "_profil" in p["ad"]]
        boy_m = sum(max(v.xlen, v.zlen) for v in pr_)
        kontrol("%s BOM profil %d parça · %.2f m = model %d parça · %.2f m" % (kod, PROFIL_BOM[kod][0], PROFIL_BOM[kod][1] / 1000.0, len(pr_), boy_m / 1000.0),
                PROFIL_BOM[kod][0] == len(pr_) and abs(PROFIL_BOM[kod][1] - boy_m) < 0.5)
        q = [dunya(p).BoundingBox() for p in ps if p["birim"] == kod]
        x0_, x1_ = min(v.xmin for v in q), max(v.xmax for v in q)
        y0_, y1_ = min(v.ymin for v in q), max(v.ymax for v in q)
        z0_, z1_ = min(v.zmin for v in q), max(v.zmax for v in q)
        vol = sum(dunya(p).Volume() for p in ps if p["birim"] == kod)
        taban = sum(dunya(p).BoundingBox().xlen * dunya(p).BoundingBox().zlen for p in ps if p["birim"] == kod and "_profil" in p["ad"])
        kontrol("%s x %.0f–%.0f · y %.1f–%.1f · z %.0f…%.0f (modül z −830…0 içinde) · kütle %.1f kg" % (kod, x0_, x1_, y0_, y1_, z0_, z1_, vol * RO),
                abs(x0_ - xr[0]) < 0.01 and abs(x1_ - xr[1]) < 0.01 and abs(y0_ - Y_DUZ) < 0.01 and z0_ >= -830.0 and z1_ <= 0.0)
        print("  YÜK: %s %.0f kg (VARSAYIM) + kendi %.1f kg → profil tabanı %.0f cm² üstünden dolap üstüne %.1f kPa (dolap üst sacı bunu taşımalı — çekmeceli dolap üretecinde denetlenmeli)"
              % (kod, YUK[kod], vol * RO, taban / 100.0, (YUK[kod] + vol * RO) * 9.81 / taban * 1e3))
    # C üst plaka: en büyük desteksiz panel · Roark (4 kenar basit mesnet, a/b = 1,2 → α 0,0616)
    a_ = (C_ENINE[1] - C_ENINE[0]) - PR["b"]; b_ = (C_BOYUNA_Z[0] - (KZ[0] + PR["b"]))
    b_ = max(b_, (KZ[1] - PR["b"]) - C_BOYUNA_Z[1])
    q_ = YUK["KAIDE_C"] * 9.81 / ((C_X[1] - C_X[0]) * (KZ[1] - KZ[0]) / 1e6)
    kb, ka = min(a_, b_) / 1000.0, max(a_, b_) / 1000.0
    w = 0.0616 * q_ * kb ** 4 / (193e9 * (PL / 1000.0) ** 3) * 1000.0
    kontrol("C üst plaka en büyük panel %.0f × %.0f · yayılı %.0f Pa → sehim %.2f mm ≤ 1 (Roark, E 193 GPa)" % (max(a_, b_), min(a_, b_), q_, w), w <= 1.0)
    cak = QR.kendi_arasinda(ps, istisna=lambda a, c: False)
    print("KENDİ ARASINDA (> 1 mm³): %s" % ("TEMİZ" if not cak else cak[:20]))
    kontrol("kendi arasında çakışma = 0 (%d parça)" % len(ps), not cak, str(len(cak)))
    if "hizli" not in arg:
        t1 = time.time()
        topping_denetimi(ps, kontrol)
        print("   (TOPPING denetimi %.0f sn)" % (time.time() - t1))
    if "bom" in arg:
        QR.bom_yaz(BOM_KLASOR, ps)
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETIM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    assert not kal
    sys.stdout.flush(); os._exit(0)
