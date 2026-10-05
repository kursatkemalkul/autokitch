# -*- coding: utf-8 -*-
"""HAT VERSİYON 2 · A + C MEKANİZMA KAİDESİ ADAPTÖRÜ v1 (30 Eyl 2026 · Claude · YEREL) — kaide_cad_v4'ün v2 yerleşimi (montajda KD yerine girer).
YÖNTEM (v1'in denetlenmiş parçaları kullanılır, yeniden çizilmez · her kur()'da kaide_cad_v4.kur() baştan koşar):
  · A KAİDESİ (açıcı): bütün parçalar x + 507,5 (h2_hesap_v1.DXL) → profiller + plaka 509–1207,5 · taban sacı 509–1207,5 (v1 1,5–700) · y / z aynı.
  · C KAİDESİ (TOPPING): TOPPING ile AYNI DİLİM (h2_hesap_v1.C_DILIM, v1 dünya x 1106,5 … 1614): solu +507,5 · sağı yerinde · aşan parça kesilip birleşir ·
    içindeki parça atılır. Soğutma grubu cebi (3. göz 1620–2100) ve 1614'ün sağındaki pencereler / plaka kesikleri v1 ile AYNI. C v2: x 1207,5–2500.
      atılan: kaide_C_enine_profil_0 (1134–1174) · kaide_C_boyuna_profil_1 (1174–1580, emiş penceresi 1184–1570 ile)
      kesilen: ön / arka profil · üst plaka (1. emiş kesiği 745–1106,5 → 1252,5–1614) · boyuna profil 0 (740–1106,5 → 1247,5–1614, emiş penceresi 1257,5–1614) ·
               enine profil 1 (1580–1620 → yalnız 1614–1620 kalır: 6 mm'lik C kesit — rapora bak)
  · x taşıyan sabitler aynı dilimle yeniden yayımlanır: A_X · C_X · A_SAC_X0 · X_A1 · KOLON · C_ENINE_X · C_PENCERE_X · C_PLAKA_KESIK · C_GOZ_X.
  · Ad / malzeme / birim / grup / kaynak / BOM kalan her parçada v1 ile AYNI (yalnız wp değişir).
Dünya ölçüleri: x hat boyunca, y yukarı, z derinlik (ön +79 · arka −830).
SÖZLEŞME (kaide_cad_v4 ile aynı): kur() · PARCALAR · dunya(p) · BIRIMLER · BIRIM_MODUL · Y_MEK · Y_DUZ · KAIDE_H · MALZEME · ON_BIRIMLER · PROFIL_BOM
kur() İDEMPOTENT (her çağrı v1'den baştan kurar) · PARCALAR listesinin kimliği korunur (PARCALAR[:] = …).
Çalıştır (öz denetim): python -u ob_calistir.py h2/h2_kaide_v1.py [hizli]   (hizli: çekmeceli dolap v2 ile çakışma denetimi atlanır)"""
import math, os, re, sys, time

H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h2_hesap_v1 as H
import kaide_cad_v4 as KD0

V = cq.Vector
EPS = 1e-6
# ---------------------------------------------------------------- v2 YERLEŞİM (h2_hesap_v1 tek sayı kaynağı)
DXL = H.DXL                                     # 507,5 · A kaidesi ve C'nin sol dilimi sağa kayar
C_DILIM = H.C_DILIM                             # (1106,5 · 1614) v1 dünya x · TOPPING ile aynı dilim
assert abs(C_DILIM[1] - C_DILIM[0] - DXL) < 1e-9 and abs(KD0.A_X[1] + DXL - H.A_X[1]) < 1e-9 and abs(KD0.C_X[1] - H.C_X[1]) < 1e-9

# ---------------------------------------------------------------- v1 ile AYNI (y / z / profil / yük)
Y_DUZ, Y_MEK, KAIDE_H, PL, PR = KD0.Y_DUZ, KD0.Y_MEK, KD0.KAIDE_H, KD0.PL, dict(KD0.PR)
KZ_A, KZ_C, KZ, A_SAC, A_SAC_Z, KOLON_DIKME_Z = KD0.KZ_A, KD0.KZ_C, KD0.KZ, KD0.A_SAC, KD0.A_SAC_Z, KD0.KOLON_DIKME_Z
C_PENCERE_Y, C_BOYUNA_Z, A_BOYUNA_Z, YUK, RO = KD0.C_PENCERE_Y, KD0.C_BOYUNA_Z, KD0.A_BOYUNA_Z, dict(KD0.YUK), KD0.RO
MALZEME, ON_BIRIMLER = KD0.MALZEME, tuple(KD0.ON_BIRIMLER)
BIRIM_MODUL = dict(KD0.BIRIM_MODUL)
kut = KD0.kut
dunya = KD0.dunya                               # qr_cad_v1.dunya: wp.vals() → tek şekil / Compound (DÜNYA)


def _xc(x):
    """v1 dünya x → v2 (C dilimi: solu +DXL, sağı yerinde, içi None)"""
    if x <= C_DILIM[0] + EPS: return x + DXL
    if x >= C_DILIM[1] - EPS: return x
    return None


def _aralik_c(a, b):
    """v1 x aralığı → v2 aralıkları (C dilimi): sol parça +DXL, sağ parça yerinde, bitişikse birleşir"""
    out = []
    if a < C_DILIM[0] - EPS: out.append([a + DXL, min(b, C_DILIM[0]) + DXL])
    if b > C_DILIM[1] + EPS:
        s0 = max(a, C_DILIM[1])
        if out and abs(out[-1][1] - s0) < EPS: out[-1][1] = b
        else: out.append([s0, b])
    return [tuple(q) for q in out]


# x taşıyan sabitler (v2)
A_X = (KD0.A_X[0] + DXL, KD0.A_X[1] + DXL)                                     # 509 · 1207,5 (v1 1,5 · 700)
C_X = (KD0.C_X[0] + DXL, KD0.C_X[1])                                           # 1207,5 · 2500 (v1 700 · 2500)
A_SAC_X0, X_A1 = KD0.A_SAC_X0 + DXL, KD0.X_A1 + DXL                            # A taban sacı 509 … 1207,5 = C sol ucu
KOLON = dict(KD0.KOLON, x=(KD0.KOLON["x"][0] + DXL, KD0.KOLON["x"][1] + DXL))    # açıcı kolonu 797,5–917,5
C_ENINE_X = tuple(iv for xc in KD0.C_ENINE for iv in _aralik_c(xc - PR["b"] / 2.0, xc + PR["b"] / 2.0))   # ((1614, 1620) kalıntı · (2100, 2140))
C_PENCERE_X = {k: tuple(iv for a, b in v for iv in _aralik_c(a, b)) for k, v in KD0.C_PENCERE_X.items()}  # emiş (1257,5–1614) · atış (1630–2090) (2150–2450)
C_PLAKA_KESIK = [(a2, b2, z0, z1) for a, b, z0, z1 in KD0.C_PLAKA_KESIK for a2, b2 in _aralik_c(a, b)]
_xs = [C_X[0] + PR["b"]] + [v for iv in C_ENINE_X for v in iv] + [C_X[1] - PR["b"]]
C_GOZ_X = [(_xs[i], _xs[i + 1]) for i in range(0, len(_xs), 2)]                  # C gözleri (profil iç yüzleri arası): 1247,5–1614 · 1620–2100 · 2140–2460


def _s(v):
    t = ("%.1f" % v).replace(".", ",")
    return t[:-2] if t.endswith(",0") else t


BIRIMLER = [
    ("KAIDE_A", "A mekanizma kaidesi 104 · HAT v2 x %s–%s (v1 kaidesi +%s · taban sacı %s–%s) · y 788–892 · z −828,5…+35 (taban sacı …+39) · AISI 304 kutu profil 40 × 100 × 2 + üst plaka 4 · "
                "açıcı kolonu dikmesi altında enine + boyuna profil · 1,5 mm taban sacı 892–893,5 (tekne + kabin dikmeleri) · ön düzlem +79"
                % (_s(A_X[0]), _s(A_X[1]), _s(DXL), _s(A_SAC_X0), _s(X_A1))),
    ("KAIDE_C", "C mekanizma kaidesi 104 · HAT v2 x %s–%s (TOPPING ile aynı dilim: v1 %s–%s çıktı) · y 788–892 · z −830…+35 · AISI 304 kutu profil 40 × 100 × 2 (çevre + enine + boyuna) "
                "+ üst plaka 4 · TOPPING dis_taban üstüne oturur · SOĞUTMA GRUBU CEBİ (3. göz 1620–2100, v1 ile aynı) · hava pencereleri 66 yüksek (y 800–866): emiş %s · atış %s + plakada açıklıklar"
                % (_s(C_X[0]), _s(C_X[1]), _s(C_DILIM[0]), _s(C_DILIM[1]), " / ".join("%s–%s" % (_s(a), _s(b)) for a, b in C_PENCERE_X["emis"]),
                   " / ".join("%s–%s" % (_s(a), _s(b)) for a, b in C_PENCERE_X["atis"]))),
]
assert [k for k, _a in BIRIMLER] == [k for k, _a in KD0.BIRIMLER]

PARCALAR = []
PROFIL_BOM = {}          # v2 geometriden: birim → (profil parça sayısı, toplam boy mm) · BOM satırları v1 metniyle korunur (rapora bak)
RAPOR = {}


def _tek(sh):
    ss = sh.Solids()
    if len(ss) == 1: return ss[0]
    return cq.Compound.makeCompound(ss) if ss else sh


def _kut(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def _sinif(b):
    if b.xmax <= C_DILIM[0] + EPS: return "sol"
    if b.xmin >= C_DILIM[1] - EPS: return "sag"
    if b.xmin >= C_DILIM[0] - EPS and b.xmax <= C_DILIM[1] + EPS: return "ic"
    return "dilim"


def dilimle(sh):
    """v1 dünya şeklinden C_DILIM'i çıkarır: solu +DXL, sağı yerinde, içi atılır · tamamen içindeyse None (h2_topping_v1.dilimle ile aynı kural)"""
    b = sh.BoundingBox(); s = _sinif(b)
    if s == "sol": return sh.translate(V(DXL, 0.0, 0.0))
    if s == "sag": return sh
    if s == "ic": return None
    ss = []
    if b.xmin < C_DILIM[0] - EPS:
        sol = sh.intersect(_kut(b.xmin - 10.0, C_DILIM[0], b.ymin - 10.0, b.ymax + 10.0, b.zmin - 10.0, b.zmax + 10.0))
        if sol.Volume() > EPS: ss.append(sol.translate(V(DXL, 0.0, 0.0)))
    if b.xmax > C_DILIM[1] + EPS:
        sag = sh.intersect(_kut(C_DILIM[1], b.xmax + 10.0, b.ymin - 10.0, b.ymax + 10.0, b.zmin - 10.0, b.zmax + 10.0))
        if sag.Volume() > EPS: ss.append(sag)
    if not ss: return None
    if len(ss) == 1: return _tek(ss[0].clean())
    return _tek(ss[0].fuse(ss[1]).clean())


C_ARKA_PENCERE_X = ((C_PENCERE_X["emis"][0][0], C_PENCERE_X["emis"][0][1]),)   # v2 · arka emiş = ön emiş penceresiyle aynı x (1257,5–1614)


def kur():
    """v2 kaide parçaları (dünya) → PARCALAR · A: +DXL · C: dilim · İDEMPOTENT (her çağrı kaide_cad_v4.kur()'dan baştan)"""
    KD0.kur()
    out, atilan, sinif = [], [], {}
    for p in KD0.PARCALAR:
        sh = dunya(p)
        if p["birim"] == "KAIDE_A":
            yeni, s = sh.translate(V(DXL, 0.0, 0.0)), "A"
        else:
            s = _sinif(sh.BoundingBox()); yeni = dilimle(sh)
            if yeni is None:
                atilan.append(p["ad"]); continue
        sinif[p["ad"]] = s
        out.append(dict(p, wp=cq.Workplane("XY").add(yeni)))
    # v2 · ARKA EMİŞ (Claude 30 Eyl): TOPPING daralınca yoğuşma ünitesinin EMİŞ bölgesi 1209–1631,5'e indi (v1 701,5–1631,5) → ön ızgara 5 kolon
    #      (v1 10) · 240 m³/h için ön yarıklar tek başına 5,3 m/s (v1 kuralı ≤ 3,5) → C kaidesinin ARKA profiline ön pencereyle aynı pencere + yıkanabilir
    #      filtre: hava makinenin arkasından da girer (fırın üstü kabin de arkadaki panjurlardan nefes alıyor → arkada boşluk şartı zaten var)
    for p in out:
        if p["ad"] == "kaide_C_arka_profil":
            sh = dunya(p)
            for a_, b_ in C_ARKA_PENCERE_X:
                sh = sh.cut(_kut(a_, b_, C_PENCERE_Y[0], C_PENCERE_Y[1], KZ_C[0] - 1.0, KZ_C[0] + PR["b"] + 1.0))
            p["wp"] = cq.Workplane("XY").add(_tek(sh))
        elif p["ad"] == "kaide_C_enine_profil_1":                                                # dilimden kalan 6 mm'lik açık C → dolu lama 6 × 100
            b = dunya(p).BoundingBox()
            p["wp"] = cq.Workplane("XY").add(_kut(b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))
            p["bom"] = ("Enine lama 6 × 100 AISI 304 (v2: dilimden kalan enine profil yerine dolu lama)", 1, "%.0f boy · ön / arka profile kaynak" % (b.zmax - b.zmin),
                        "v2 · emiş gözü ile ünite cebi arasında", "ÜRETİM")
    for a_, b_ in C_ARKA_PENCERE_X:
        out.append(dict(ad="kaide_C_arka_emis_filtresi", wp=cq.Workplane("XY").add(_kut(a_, b_, C_PENCERE_Y[0], C_PENCERE_Y[1], KZ_C[0] + PR["b"], KZ_C[0] + PR["b"] + 14.0)),
                        mal="paslanmaz", birim="KAIDE_C", grup="SABIT", kaynak="v2 · Claude 30 Eyl",
                        bom=("Kondenser ARKA emiş filtresi · yıkanabilir paslanmaz tel örgü + çerçeve", 1, "%.1f × %.0f × 14 · arka profilin iç yüzünde 2 klips" % (b_ - a_, C_PENCERE_Y[1] - C_PENCERE_Y[0]),
                             "v2 · ön filtreyle aynı bakım (ayda 1 · VARSAYIM) · makine arkasında ≥ 50 mm boşluk şartı [V]", "SATIN ALMA")))
    PARCALAR[:] = out
    PROFIL_BOM.clear()
    for b_ in ("KAIDE_A", "KAIDE_C"):
        pr_ = [dunya(p).BoundingBox() for p in PARCALAR if p["birim"] == b_ and "_profil" in p["ad"]]
        PROFIL_BOM[b_] = (len(pr_), sum(max(v.xlen, v.zlen) for v in pr_))
    RAPOR.clear(); RAPOR.update(atilan=atilan, sinif=sinif)
    return PARCALAR


# ---------------------------------------------------------------- ÖZ DENETİM
DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-160s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger)); sys.stdout.flush()


def _bbt(s):
    b = s.BoundingBox(); return (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)


def _capraz(L1, L2, esik=1.0):
    out = []
    for a, sa, A in L1:
        for c, sc, B in L2:
            if A.xmin < B.xmax - 0.01 and B.xmin < A.xmax - 0.01 and A.ymin < B.ymax - 0.01 and B.ymin < A.ymax - 0.01 and A.zmin < B.zmax - 0.01 and B.zmin < A.zmax - 0.01:
                v_ = sa.intersect(sc).Volume()
                if v_ > esik: out.append((round(v_, 2), a, c))
    return out


if __name__ == "__main__":
    t0 = time.time(); arg = sys.argv[1:]
    ps = kur(); kimlik = id(PARCALAR)
    ps2 = [dict(p) for p in kur()]; ps = kur()
    KD0.kur(); v1 = {p["ad"]: (p, dunya(p)) for p in KD0.PARCALAR}
    print("h2_kaide_v1 · %d parça (v1 %d) · A +%.1f · C dilim %s · atılan %s · %.1f sn" % (len(ps), len(v1), DXL, C_DILIM, RAPOR["atilan"], time.time() - t0))
    print("ÖZ DENETİM (h2_kaide_v1)")
    idem = max(max(abs(a - b) for a, b in zip(_bbt(dunya(p)), _bbt(dunya(q)))) for p, q in zip(ps, ps2))
    kontrol("İDEMPOTENT: kur() 3 kez → %d = %d parça · adlar aynı sırada · en büyük sınır kutusu farkı %.1e · PARCALAR nesnesi aynı" % (len(ps), len(ps2), idem),
            len(ps) == len(ps2) and [p["ad"] for p in ps] == [p["ad"] for p in ps2] and idem < 1e-9 and id(PARCALAR) == kimlik and ps is PARCALAR)
    # 1 · A: her parça v1 + DXL · C: sağ yerinde, sol + DXL, dilimi aşan hacim korunumu · meta aynı
    fa, fc, meta, gec, dh = 0.0, 0.0, [], [], 0.0
    kutu_d = _kut(C_DILIM[0], C_DILIM[1], 700.0, 1000.0, -900.0, 100.0)
    for p in ps:
        q, sq = v1[p["ad"]]; s2 = dunya(p); a, b = _bbt(s2), _bbt(sq); k = RAPOR["sinif"][p["ad"]]
        if k in ("A", "sol"):
            fa = max(fa, abs(a[0] - b[0] - DXL), abs(a[1] - b[1] - DXL), *(abs(a[i] - b[i]) for i in range(2, 6)), abs(s2.Volume() - sq.Volume()))
        elif k == "sag":
            fc = max(fc, max(abs(a[i] - b[i]) for i in range(6)), abs(s2.Volume() - sq.Volume()))
        else:
            dh = max(dh, abs(sq.Volume() - sq.intersect(kutu_d).Volume() - s2.Volume()) / sq.Volume())
        if any(p[k_] != q[k_] for k_ in ("mal", "birim", "grup", "bom", "kaynak")): meta.append(p["ad"])
        if not s2.isValid() or len(s2.Solids()) != 1: gec.append(p["ad"])
    nd = [a for a, k in RAPOR["sinif"].items() if k == "dilim"]
    kontrol("A kaidesi + C'nin sol parçaları v1 + %.1f (sınır kutusu + hacim, sapma %.1e) · C'nin sağ parçaları yerinde (sapma %.1e) · dilimi aşan %d parça hacmi v2 = v1 − dilim içi (bağıl %.1e)"
            % (DXL, fa, fc, len(nd), dh), fa < 1e-6 and fc < 1e-6 and dh < 1e-9, ", ".join(nd))
    kontrol("atılan (dilimin içinde) %s · ad / malzeme / birim / grup / BOM / kaynak v1 ile aynı · katılar geçerli ve tek parça (%d)" % (RAPOR["atilan"], len(ps)),
            sorted(RAPOR["atilan"]) == ["kaide_C_boyuna_profil_1", "kaide_C_enine_profil_0"] and not meta and not gec, str((meta + gec)[:6]))
    # 2 · zarf: A ⊂ [507,5 · 1207,5] · C = [1207,5 · 2500] · A|C uç uca
    za = [dunya(p).BoundingBox() for p in ps if p["birim"] == "KAIDE_A"]; zc = [dunya(p).BoundingBox() for p in ps if p["birim"] == "KAIDE_C"]
    ax = (min(b.xmin for b in za), max(b.xmax for b in za)); cx = (min(b.xmin for b in zc), max(b.xmax for b in zc))
    ts = dunya([p for p in ps if p["ad"] == "kaide_A_mekanizma_taban_saci"][0]).BoundingBox()
    kontrol("ZARF: A x %.2f–%.2f ⊂ [%.1f, %.1f] · C x %.2f–%.2f = [%.1f, %.0f] · A taban sacı sağ ucu %.2f = C sol ucu %.2f · y %.0f–%.1f"
            % (ax[0], ax[1], H.A_X[0], H.A_X[1], cx[0], cx[1], H.C_X[0], H.C_X[1], ts.xmax, cx[0], min(b.ymin for b in za + zc), max(b.ymax for b in za + zc)),
            H.A_X[0] - 0.01 <= ax[0] and ax[1] <= H.A_X[1] + 0.01 and abs(cx[0] - H.C_X[0]) < 0.01 and abs(cx[1] - H.C_X[1]) < 0.01 and abs(ts.xmax - cx[0]) < 0.01
            and abs(min(b.ymin for b in za + zc) - Y_DUZ) < 0.01 and abs(max(b.ymax for b in zc) - Y_MEK) < 0.01)
    # 3 · pencereler + plaka kesikleri katılardan: C_PENCERE_X / C_PLAKA_KESIK açık, pencere uçlarında malzeme var
    P = {p["ad"]: dunya(p) for p in ps}
    op, bp = P["kaide_C_on_profil"], [P[a] for a in P if a.startswith("kaide_C_boyuna_profil_")]
    ac = []
    for k_, pl_ in C_PENCERE_X.items():
        for a, b in pl_:
            ac.append(op.intersect(_kut(a + 0.01, b - 0.01, C_PENCERE_Y[0] + 0.01, C_PENCERE_Y[1] - 0.01, KZ[1] - PR["b"] - 1.0, KZ[1] + 1.0)).Volume())
            for s_ in bp:
                bb_ = s_.BoundingBox()
                if bb_.xmin - 0.01 <= a and b <= bb_.xmax + 0.01:
                    ac.append(s_.intersect(_kut(a + 0.01, b - 0.01, C_PENCERE_Y[0] + 0.01, C_PENCERE_Y[1] - 0.01, C_BOYUNA_Z[0] - 1.0, C_BOYUNA_Z[1] + 1.0)).Volume())
    uc_ = [op.intersect(_kut(b, b + 5.0, C_PENCERE_Y[0] + 1.0, C_PENCERE_Y[1] - 1.0, KZ[1] - PR["b"] - 1.0, KZ[1] + 1.0)).Volume() for pl_ in C_PENCERE_X.values() for _a, b in pl_]
    plk = [P["kaide_C_ust_plaka_4"].intersect(_kut(a + 0.01, b - 0.01, Y_DUZ + PR["h"] - 1.0, Y_MEK + 1.0, z0 + 0.01, z1 - 0.01)).Volume() for a, b, z0, z1 in C_PLAKA_KESIK]
    kontrol("PENCERELER (katıdan): emiş %s · atış %s · y %.0f–%.0f → ön + boyuna profilde açık (%d ölçüm, kalan %.3f mm³) · her pencerenin sağ ucunda 5 mm dolu profil (en az %.0f mm³) · plaka kesikleri %s açık (kalan %.3f mm³)"
            % (C_PENCERE_X["emis"], C_PENCERE_X["atis"], C_PENCERE_Y[0], C_PENCERE_Y[1], len(ac), sum(ac), min(uc_), [(a, b) for a, b, _z0, _z1 in C_PLAKA_KESIK], sum(plk)),
            sum(ac) < 1e-3 and min(uc_) > 100.0 and sum(plk) < 1e-3 and C_PENCERE_X["emis"] == ((1257.5, 1614.0),))
    # 4 · soğutma grubu cebi (3. göz) + sağ taraf v1 ile aynı
    cep = [a for a, b, z0, z1 in C_PLAKA_KESIK if abs(a - 1628.0) < 1e-6 and abs(b - 2095.0) < 1e-6 and abs(z0 + 790.0) < 1e-6]
    kontrol("SOĞUTMA GRUBU CEBİ: plaka kesiği 1628–2095 × −790…−477 v1 ile aynı · göz %s (enine profil iç yüzleri) · tepsi köşebendi yerinde"
            % ("%.1f–%.1f" % C_GOZ_X[1]), bool(cep) and abs(C_GOZ_X[1][0] - 1620.0) < 1e-6 and abs(C_GOZ_X[1][1] - 2100.0) < 1e-6 and RAPOR["sinif"]["kaide_C_tepsi_kosebendi"] == "sag")
    en1 = P["kaide_C_enine_profil_1"].BoundingBox()
    print("  BİLGİ · C gözleri v2 %s (v1: 740–1134 · 1174–1580 · 1620–2100 · 2140–2460) · kaide_C_enine_profil_1 kalıntısı x %.1f–%.1f (%.0f mm: sağ et 1618–1620 + üst/alt flanş 4 mm, "
          "sol yüzü AÇIK C kesit) · emiş penceresi sağ ucu %.1f = kalıntının sol yüzü (v1 kuralı 'profil kenarından ≥ 5 mm içeride' burada 0 mm)"
          % (C_GOZ_X, en1.xmin, en1.xmax, en1.xlen, C_PENCERE_X["emis"][0][1]))
    # 5 · kendi arasında + havada
    import qr_cad_v1 as QR
    cak = QR.kendi_arasinda(ps, istisna=lambda a, c: False)
    kontrol("kendi arasında çakışma > 1 mm³ = %d (%d parça)" % (len(cak), len(ps)), not cak, str(cak[:6]))
    import denetim_temas_v1 as DT
    hv = DT.havada([(p["ad"], dunya(p)) for p in ps], zemin_y=Y_DUZ)
    DT.yaz(hv, baslik="HAVADA PARCA DENETIMI · h2_kaide_v1")
    kontrol("havada parça = 0 (%d parça · kök %d · bağlı %d · beyaz liste YOK)" % (hv["parca"], hv["kok"], hv["bagli"]), not hv["bilesen"], str([d_["en"] for d_ in hv["bilesen"]]))
    # 6 · BOM profil sayısı / boyu (v2 geometriden) · C üst plaka sehimi + pencere üstü şerit (kaide_cad_v4 hesabı, v2 C boyu ile)
    print("  BİLGİ · PROFIL_BOM v2 (geometriden): %s · v1 BOM satırı (korundu): %s" % ({k: (n, round(l_ / 1000.0, 2)) for k, (n, l_) in PROFIL_BOM.items()},
                                                                                   {k: (n, round(l_ / 1000.0, 2)) for k, (n, l_) in KD0.PROFIL_BOM.items()}))
    _xs4 = [C_X[0] + PR["b"]] + [v for iv in C_ENINE_X for v in iv] + [C_X[1] - PR["b"]]
    a_ = max(_xs4[i + 1] - _xs4[i] for i in range(0, len(_xs4), 2)); b_ = (KZ[1] - PR["b"]) - C_BOYUNA_Z[1]
    for etiket, gen in (("v1 boyu 1800 (kaide_cad_v4)", KD0.C_X[1] - KD0.C_X[0]), ("v2 boyu %.1f (aynı %d kg daha dar alana)" % (C_X[1] - C_X[0], YUK["KAIDE_C"]), C_X[1] - C_X[0])):
        q_ = YUK["KAIDE_C"] * 9.81 / (gen * (KZ[1] - KZ[0]) / 1e6)
        kb, ka = min(a_, b_) / 1000.0, max(a_, b_) / 1000.0; _ar = max(a_, b_) / min(a_, b_)
        _al = 0.0616 + (0.0770 - 0.0616) * min(1.0, max(0.0, (_ar - 1.2) / 0.2)) if _ar <= 1.4 else 0.0906
        w = _al * q_ * kb ** 4 / (193e9 * (PL / 1000.0) ** 3) * 1000.0
        _Lp = max(b__ - a__ for a__, b__ in C_PENCERE_X["emis"] + C_PENCERE_X["atis"]) / 1000.0
        _qp = q_ * ((KZ[1] - KZ[0]) / 2.0 / 1000.0); _hs = PR["h"] - 2.0 - (C_PENCERE_Y[1] - Y_DUZ)
        _A = 40.0 * 2.0 + 2.0 * 2.0 * _hs; _yc = (40.0 * 2.0 * (_hs + 1.0) + 2.0 * 2.0 * _hs * _hs / 2.0) / _A
        _I = 40.0 * 2.0 ** 3 / 12.0 + 40.0 * 2.0 * (_hs + 1.0 - _yc) ** 2 + 2.0 * (2.0 * _hs ** 3 / 12.0 + 2.0 * _hs * (_hs / 2.0 - _yc) ** 2)
        _S = _I / max(_yc, _hs + 2.0 - _yc); _M = _qp * _Lp ** 2 / 12.0 * 1000.0
        kontrol("C YÜK (%s · %d kg VARSAYIM): en büyük kesiksiz panel %.0f × %.0f · %.0f Pa → plaka sehimi %.2f mm ≤ 1 · pencere üstü şerit %.0f mm açıklık σ %.0f MPa ≤ 102,5"
                % (etiket, YUK["KAIDE_C"], max(a_, b_), min(a_, b_), q_, w, _Lp * 1000.0, _M / _S), w <= 1.0 and _M / _S <= 102.5)
    # 7 · ÇEKMECELİ DOLAP v2 (h2_store_v1) üstüyle çakışma · v1'de değen çiftler serbest (kaide_cad_v4 ↔ store_cad_v14)
    if "hizli" not in arg:
        t1 = time.time()
        import h2_store_v1 as HS
        HS.modul()
        ust2 = [(p["ad"], HS._sekil(p["wp"])) for p in HS.PARCALAR]
        ust2 = [(a, s_, s_.BoundingBox()) for a, s_ in ust2]; ust2 = [x for x in ust2 if x[2].ymax > Y_DUZ - 5.0]
        K2 = [(p["ad"], dunya(p)) for p in ps]; K2 = [(a, s_, s_.BoundingBox()) for a, s_ in K2]
        c2 = _capraz(K2, ust2)
        ust1 = [(p["ad"], HS._sekil(p["wp"])) for p in HS.V1_PARCALAR]
        ust1 = [(a, s_, s_.BoundingBox()) for a, s_ in ust1]; ust1 = [x for x in ust1 if x[2].ymax > Y_DUZ - 5.0]
        K1 = [(a, s_, s_.BoundingBox()) for a, (_q, s_) in v1.items()]
        c1 = _capraz(K1, ust1)
        serbest = {(a, c) for _v, a, c in c1}
        yeni = [x for x in c2 if (x[1], x[2]) not in serbest]
        ts2 = [x for x in ust2 if x[0] == "tavan_dis_sac"][0][2]
        alt_ = [p["ad"] for p in ps if dunya(p).BoundingBox().ymin < Y_DUZ - 0.01]
        kontrol("KAİDE ↔ ÇEKMECELİ DOLAP v2 (h2_store_v1 · üst bandı %d parça, kaide %d): kesişim > 1 mm³ = %d · v1'de (kaide_cad_v4 ↔ store_cad_v14) %d → yeni %d · dolap üst sacı x %.1f–%.1f · y üstü %.1f "
                "kaidenin altını tam taşır (kaide x %.1f–%.1f) · kaideden 788 altına inen parça %d · %.0f sn"
                % (len(ust2), len(K2), len(c2), len(c1), len(yeni), ts2.xmin, ts2.xmax, ts2.ymax, ax[0], cx[1], len(alt_), time.time() - t1),
                not yeni and ts2.xmin <= ax[0] + 0.01 and ts2.xmax >= cx[1] - 0.01 and abs(ts2.ymax - Y_DUZ) < 0.01 and ts2.zmin <= KZ[0] + 0.01 and ts2.zmax >= KZ[1] - 0.01 and not alt_,
                str((yeni + ([("alt",) + tuple(alt_)] if alt_ else []))[:6]))
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETİM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    sys.stdout.flush(); os._exit(1 if kal else 0)
