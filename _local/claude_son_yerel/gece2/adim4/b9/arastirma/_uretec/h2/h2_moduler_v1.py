# -*- coding: utf-8 -*-
# h2_moduler_v1 (30 Eyl 2026 · Claude, YEREL): HAT VERSİYON 2 · moduler_montaj_v4'ün v2 KOPYASI — bütün sabit x konumları h2_hesap_v1'den türetildi.
#   Montaj aynı çağrıyı yapar: MOD72.uygula(SimpleNamespace(SC, KS, KC, AK, KD, TC, X_K, X_E, Y_MEK)) · sonra MOD72.PARTS / MOD72.DEGISEN okunur.
#   SC = h2_store_v1 (v2 dolap, DÜNYA) · AK = h2_acici_v1 (A +507,5, DÜNYA) · KD = h2_kaide_v1 · TC yalnız RAKOR_ACICI (değişmedi) · KS / KC / X_K / X_E v1 ile aynı.
#   v1 → v2 (her satır aşağıda sabit olarak):
#     A: kendi sağ duvarı 698–699,5 → 1205,5–1207 (A_X[1] − 2) · ray/tabla ağzı kesicisi 697–701 → 1204,5–1208,5 · rakor delikleri x 697 → 1204,5 ·
#        sağ çerçeve (lento + boğaz dikmesi + alt kayıt) 668–698 → 1175,5–1205,5 · "sağ" süzgeç eşiği 650 → 1157,5 · arka kuşak / üst kayıt kırpma kutusu
#        −10…668 → 497,5…1175,5 · binen parça eşiği 668 → 1175,5 (A'nın hepsi +507,5 kaydığı için sonuç v1'in birebir +507,5'i — _test_moduler_v1 ölçer)
#     B: alt şase boyunaları 1,5…3998,5 → 509…3998,5 (sol dış sac iç yüzü) · A/C taşıyıcı kirişi 2…2502,5 → 509,5…(2502,5 | 2532,5, aşağıda)
#        dikmeler v1 17 · 700 · 1355 · 2010 (sol duvar PU · B1 · B2 · B3) → 524,5 · 1207,5 · 1862,5 · 2517,5 (B3 dilimle çıktı; K3'ün yeni sağ bölmesi B4 2500–2535)
#        B4 ekseninde store_cad_v14 fırın taşıyıcı dikmeleri TD (x 2517,5 · z −110 / −620) ZATEN var:
#          · ön hat z −110: TD dikmesi (tasiyici_dikme_0) ORTAK kullanılır — ikinci dikme YOK; kiriş v1'deki gibi 2502,5'te TD dikmesi + fırın ön taşıyıcı kirişine alın alına
#          · arka hat z −747: TD yok (TD arka −620) → B4'te yeni dikme (bolme_3 PU'sunun içinde), kiriş dikmenin üstüne 2532,5'e kadar uzar (dikme boşta kalmasın)
#        HAT KAYDIRMA (v2 · yalnız engel varsa): bir hattın dikmeleri v1 z'sinde dolabın kesilemeyen bir parçasına (PU / bölme / taban / tavan / iç yan sac DIŞINDA,
#          ör. h2_store_v1'in gider ana hattı z −738 · Ø24 kılıf B2 / B4'te) çarpıyorsa bütün hat (kiriş + dikmeleri) ÖNE 1 mm adımla, 5 mm boşlukla engelsiz ilk z'ye
#          kayar (arkaya değil: plenumun hava + kablo geçişleri z ≤ −760) · 60 mm içinde yoksa DURUR · sonuç B_AC_Z_UYGULANAN'da · engel yoksa v1 z'si AYNEN
#        taşıma pabucu solu max(1,5, x − 15) → max(509, x − 15)
#     _baglanti (v2'den beri ÇAĞRILMAZ): A cıvataları 28 / 672 → 535,5 / 1179,5 · C 728 / 2472 → 1235,5 / 2472 · B–K / K–E (x ≥ 3970) aynı
# moduler_montaj_v4 (30 Eyl 2026 · Claude, YEREL): v3 + A SAĞ YAN ÇERÇEVESİ — Kemal (A kabini ekran görüntüsü): "bunun sağ alt kısmı neden böyle, çıta ince
#   bağlı değil bir yere; bu kendi başına 4 taraftan çıtalarla kurulması lazım değil mi? kutu gibi". v3'te ray/tabla ağzı (z −510,5…+5,5) sağ duvarın önünde
#   53,5 × 149 mm'lik boşta sarkan sac şerit bırakıyordu (altı hiçbir yere bağlı değil) ve ağzın çevresinde çerçeve yoktu. v4: ağzın ön kenarı ön dikmenin
#   arka yüzüne (z 9) → sac ön dikmeye oturur · ağız 30×30×2 kutu profille çerçevelenir: LENTO (üst) + BOĞAZ DİKMESİ (arka) + ALT KAYIT (arka dikmeye) ·
#   sağ çerçeve −2 mm kayınca ona 2 mm binen 3 ön kayıt dikme yüzünde biter, 2 emniyet sensörü dikmeyle birlikte kayar. Geri kalanı v3 ile birebir.
# moduler_montaj_v3 (29 Eyl 2026 · Claude, YEREL): v2 + A–C çevre contası (EPDM) KALKTI — Kemal: A|C köşesi "iki istasyonun birleşimi gibi düşün, bağlantıları tabla ve rayıyla oluyor".
# moduler_montaj_v2 (29 Eyl 2026 · Claude, YEREL): v1 (Codex) + _baglanti() ÇAĞRILMAZ — Kemal: "delikleri kaldır, nasıl bağlanacaklarını şu an karar vermeyeceğiz, bağlanmayla ilgili şeyleri kaldır". Geri kalanı v1 ile birebir.
"""AUTOKITCH · BAĞIMSIZ İSTASYONLAR → ANA MONTAJ · HAT v2 (h2_moduler_v1 · kaynak moduler_montaj_v4 / Codex moduler_istasyon_v1 yöntemi).
Mevcut parçalar yerinde değiştirilir (p["wp"] güncellenir); yeni parçalar YENI listesinde döner (dünya koordinatı)."""
import os, sys
import cadquery as cq

H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import h2_hesap_v1 as H

V = cq.Vector


def box(x0, x1, y0, y1, z0, z1): return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))
def bb(s):
    b = s.BoundingBox(); return [b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax]
def overlap(a, b, t=.05): return all(min(a[2 * i + 1], b[2 * i + 1]) - max(a[2 * i], b[2 * i]) > t for i in range(3))
def cyl_y(x, z, r, y0, y1): return cq.Solid.makeCylinder(r, y1 - y0, V(x, y0, z), V(0, 1, 0))
def _tek(wp):
    v = [o for o in wp.vals() if isinstance(o, cq.Shape)]
    return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)


# ---------------------------------------------------------------- v2 KONUMLARI (h2_hesap_v1) ----------------------------------------------------------------
DXL = H.DXL                                             # 507,5


def v2x(x_v1):
    """v1 dünya x → v2 (h2_hesap_v1): dolabın / A'nın sol grubu (x < B_DILIM[0]) + DXL · dilimin içi YOK · x ≥ B_DILIM[1] yerinde"""
    if x_v1 < H.B_DILIM[0]: return x_v1 + DXL
    if x_v1 >= H.B_DILIM[1]: return x_v1
    raise ValueError("v1 x %.1f dolaptan çıkan dilimde (%.1f–%.1f)" % (x_v1, H.B_DILIM[0], H.B_DILIM[1]))


BOGAZ = dict(ust=1042.5, arka=-510.5, on=9.0)           # v4: ağız ön kenarı = ön dikmenin arka yüzü (v3: 5,5 → önde 53,5 mm sarkan şerit) · y / z v1 ile aynı
PROFIL = 30.0                                            # v4: A sağ yan çerçevesi 30×30×2 (arka köşe dikmesi ve üst kuşakla aynı)
XA0, XA1 = H.A_X                                         # A 507,5 … 1207,5 (v1 0 … 700)
A_KAYMA = 2.0                                            # A sağ çerçevesi −2 mm (v1 ile aynı) → kendi duvarına yer
DUVAR_T = 1.5                                            # A'nın kendi sağ duvarı 304 1,5
X_DUVAR = (XA1 - A_KAYMA, XA1 - A_KAYMA + DUVAR_T)      # 1205,5 … 1207 (v1 698 … 699,5) · C sol yan sacına (1207,5) 0,5 derz
X_BOGAZ = (X_DUVAR[0] - 1.0, X_DUVAR[1] + 1.5)          # 1204,5 … 1208,5 (v1 697 … 701) · ray / tabla ağzı kesicisi
X_RAKOR = X_DUVAR[0] - 1.0                               # 1204,5 (v1 697) · açıcı hava rakoru delikleri Ø14 × 4 kesici başı
X_CER = (XA1 - A_KAYMA - PROFIL, XA1 - A_KAYMA)         # 1175,5 … 1205,5 (v1 668 … 698) · sağ çerçeve (kayan dikmeler + lento + boğaz dikmesi + alt kayıt)
X_SAG_ESIK = XA1 - 50.0                                  # 1157,5 (v1 650) · "sag" / "lama" adlı ve bu x'ten sağda başlayan A parçaları −2 kayar
X_KIRP = (XA0 - 10.0, X_CER[0])                          # 497,5 … 1175,5 (v1 −10 … 668) · arka kuşak / üst kayıt kırpma kutusu
XB0, XB1 = H.B_X                                         # dolap 507,5 … 4000 (v1 0 … 4000)
B_SASE_X = (XB0 + 1.5, XB1 - 1.5)                        # 509 … 3998,5 (v1 1,5 … 3998,5) · B alt şase boyunaları (dış sacların içi)
B_AC_X0 = XB0 + 2.0                                      # 509,5 (v1 2) · A/C taşıyıcı kirişinin sol ucu
B_PABUC_X0 = XB0 + 1.5                                   # 509 (v1 1,5) · taşıma pabucunun sol sınırı
BOLME = 35.0                                             # store_cad_v14 bölme kalınlığı (sac 1 + PU 33 + sac 1)
TD_X0 = H.B_DILIM[1] + BOLME / 2.0                       # 2517,5 · B4 (K3|K5, eski K4|K5) bölmesinin ortası = store_cad_v14 TD_X[0] (fırın taşıyıcı dikmeleri)
TK_X0 = TD_X0 - 15.0                                     # 2502,5 = store_cad_v14 TK_X[0] (fırın taşıyıcı kirişleri + TD dikmesinin sol yüzü) = v1 kiriş sağ ucu
B_AC_Z = (-110.0, -747.0)                                # ön · arka taşıyıcı hattı (v1) — engel yoksa AYNEN kullanılır
B_AC_BOSLUK = 5.0                                        # v2: hat kaydırılırsa dikme ↔ dolabın yabancı parçası (ör. gider ana hattı kılıfı) arası en az boşluk (z)
B_AC_ARAMA = 60                                          # v2: hat yalnız ÖNE (+z) 1 mm adımla en çok 60 mm kaydırılır (arkası plenum: hava + kablo geçişleri z ≤ −760)
B_AC_DIKME_X = (XB0 + 17.0,                              # 524,5 (v1 17) · sol duvar PU'sunda: dış sac 1,5 + 0,5 + profil yarısı 15
                v2x(682.5 + BOLME / 2.0),                # 1207,5 (v1 700) · B1 bölmesi (store_cad_v14 BOLME_X[0] 682,5)
                v2x(1337.5 + BOLME / 2.0),               # 1862,5 (v1 1355) · B2 bölmesi (BOLME_X[1] 1337,5)
                TD_X0)                                   # 2517,5 (v1 2010 = B3 ortası · B3 dilimle çıktı) · K3'ün yeni sağ bölmesi B4
KONUMLAR = [                                             # belge: (ne, v1, v2) — _test_moduler_v1 yazdırır
    ("A kendi sağ duvarı x", (698.0, 699.5), X_DUVAR), ("A ray/tabla ağzı kesicisi x", (697.0, 701.0), X_BOGAZ), ("A rakor deliği kesici x", 697.0, X_RAKOR),
    ("A sağ çerçeve (lento · boğaz dikmesi · alt kayıt) x", (668.0, 698.0), X_CER), ("A 'sag'/'lama' kaydırma eşiği x ≥", 650.0, X_SAG_ESIK),
    ("A arka kuşak / üst kayıt kırpma kutusu x", (-10.0, 668.0), X_KIRP), ("A çerçeveye binen parça eşiği x >", 668.0, X_CER[0]),
    ("B alt şase boyunaları x", (1.5, 3998.5), B_SASE_X), ("B A/C kirişi sol ucu x", 2.0, B_AC_X0),
    ("B A/C kirişi sağ ucu x (ön hat · arka hat; arka hattın z'si B_AC_Z_UYGULANAN'da)", (2502.5, 2502.5), (TK_X0, TD_X0 + PROFIL / 2.0)),
    ("B A/C dikmeleri x", (17.0, 700.0, 1355.0, 2010.0), B_AC_DIKME_X), ("B taşıma pabucu sol sınırı x", 1.5, B_PABUC_X0),
    ("_baglanti A cıvataları x (çağrılmaz)", (28.0, 672.0), (XA0 + 28.0, XA1 - 28.0)), ("_baglanti C cıvataları x (çağrılmaz)", (728.0, 2472.0), (H.C_X[0] + 28.0, H.C_X[1] - 28.0)),
]

PARTS, YENI, DEGISEN = [], [], []
B_AC_ORTAK = []                                          # v2: ORTAK kullanılan mevcut dikmeler (i, j, x, z, parça adı) — ikinci dikme kurulmadı
B_AC_Z_UYGULANAN = []                                    # v2: uygula() sonrası her hat (i, v1 z, uygulanan z, v1 z'deki engeller) — kaydıysa nedeni burada


def add(name, mod, shape, mat="304", kind="frame", note=""):
    if isinstance(shape, cq.Workplane): shape = shape.val()
    p = dict(name=name, module=mod, shape=shape, material=mat, kind=kind, note=note, new=True, src=None, off=0.0)
    PARTS.append(p); YENI.append(p); return p


def rhs(name, mod, b, axis, t=3, note=""):
    inner = list(b)
    for i in range(3):
        inner[2 * i] += -1 if i == axis else t; inner[2 * i + 1] += 1 if i == axis else -t
    return add(name, mod, box(*b).cut(box(*inner)), note=note)


def _kaynak(M):
    """ana montajın B / K / E / A / kaide parçaları (dünya şekli + geri yazma bilgisi)"""
    def ekle(p, mod, off):
        s = _tek(p["wp"]).translate(V(off, 0, 0)) if off else _tek(p["wp"])
        mat, kind, name = p["mal"], "inside", p["ad"]
        if any(k in name for k in ("sac", "duvar", "yalitim", "pu_", "kapak", "govde", "profil", "kaide", "dikme", "kusak", "ayak", "onyuz")): kind = "shell"
        if mat in ("pu", "yalitim_gorunur"): mat, kind = "PU", "insulation"
        PARTS.append(dict(name=name, module=mod, shape=s, material=mat, kind=kind, note=p.get("birim", mod), new=False, src=p, off=off, s0=s))
    for p in M.SC.PARCALAR: ekle(p, "B", 0.0)
    for p in M.KS.PARCALAR: ekle(p, "K", M.X_K)
    for p in M.KC.PARCALAR:
        if p["ad"].startswith(("robot_catal_", "robot_flansi", "REF_")): continue
        ekle(p, "E", M.X_E)
    for p in M.AK.PARCALAR: ekle(p, "A", 0.0)
    for p in M.KD.PARCALAR: ekle(p, "A" if p["birim"] == "KAIDE_A" else "C", 0.0)


A_CERCEVE_V4 = []


def _A(M):
    wall = box(X_DUVAR[0], X_DUVAR[1], 893.5, 1860.5, -828.5, 59)
    throat = box(X_BOGAZ[0], X_BOGAZ[1], 892.5, BOGAZ["ust"], BOGAZ["arka"], BOGAZ["on"])
    wall = wall.cut(throat)
    for y, z in M.TC.RAKOR_ACICI:
        wall = wall.cut(cq.Solid.makeCylinder(7, 4, V(X_RAKOR, y + M.Y_MEK, z), V(1, 0, 0)))
    kayan = []
    for p in PARTS:
        if p["module"] != "A" or p["new"] or p["note"] not in ("A_GOVDE", "A_ONYUZ"): continue
        b = bb(p["shape"])
        if b[0] >= X_SAG_ESIK and ("sag" in p["name"] or "lama" in p["name"]):
            p["shape"] = p["shape"].translate(V(-A_KAYMA, 0, 0)); kayan.append(p)
        elif "kusak_arka" in p["name"] or "kayit_ust" in p["name"]:
            p["shape"] = p["shape"].intersect(box(X_KIRP[0], X_KIRP[1], 780, 1900, -850, 100))
    # v4 · kayan sağ çerçeveye binenler: emniyet sensörü dikmeyle kayar · kayıt / kuşak / omega dikme yüzünde biter · başka binen parça olmamalı (assert)
    for p in PARTS:
        if p["module"] != "A" or p["new"] or any(p is q for q in kayan): continue                      # A'nın BÜTÜN parçaları (gövde · ön yüz · kaide · açıcı)
        if bb(p["shape"])[1] <= X_CER[0] + 1e-6: continue
        if "emniyet_sensoru" in p["name"]:
            p["shape"] = p["shape"].translate(V(-A_KAYMA, 0, 0)); kayan.append(p); continue
        for q in kayan:
            if not overlap(bb(p["shape"]), bb(q["shape"])) or abs(p["shape"].intersect(q["shape"]).Volume()) <= .1: continue
            assert any(k_ in p["name"] for k_ in ("kayit", "kusak", "omega")), "v4: sağ çerçeveye binen beklenmeyen parça %s ↔ %s" % (p["name"], q["name"])
            p["shape"] = p["shape"].cut(box(*bb(q["shape"])))
    add("A_bagimsiz_sag_duvar_1p5", "A", wall, kind="shell", note="304 1,5 · A'nın kendi sağ duvarı · ray/tabla geçiş ağzı açık · v4: dört yanı çerçeveye oturur")
    # v4 · A SAĞ YAN ÇERÇEVESİ: ağız 30×30×2 kutu profille çevrilir (lento + boğaz dikmesi + alt kayıt) — sac her yanıyla çerçeveye kaynaklı
    u, a, o, k = BOGAZ["ust"], BOGAZ["arka"], BOGAZ["on"], PROFIL
    A_CERCEVE_V4[:] = [rhs("A_sag_bogaz_lentosu", "A", (X_CER[0], X_CER[1], u, u + k, a, o), 2, 2, note="30×30×2 kutu profil · ray/tabla ağzının üstü · boğaz dikmesi ↔ ön dikme"),
                       rhs("A_sag_bogaz_dikmesi", "A", (X_CER[0], X_CER[1], 893.5, u + k, a - k, a), 1, 2, note="30×30×2 kutu profil · ağzın arka kenarı · kaide sacından lentoya"),
                       rhs("A_sag_alt_kayit", "A", (X_CER[0], X_CER[1], 893.5, 893.5 + k, -798.5, a - k), 2, 2, note="30×30×2 kutu profil · arka köşe dikmesi ↔ boğaz dikmesi")]
    # v3 (Kemal 29 Eyl): A–C çevre contası KALKTI — "bağlanmayla ilgili şeyleri kaldır"; iki istasyonu yalnız tabla + ray birleştirir (A duvarı ile C yan sacı arası 0,5 mm derz)
    for p in PARTS:
        if p["new"] or p["module"] != "A" or p["note"] not in ("A_GOVDE", "A_ONYUZ", "KAIDE_A"): continue
        if overlap(bb(p["shape"]), bb(wall)):
            if abs(p["shape"].intersect(wall).Volume()) > .1: p["shape"] = p["shape"].cut(wall)


def _alt_sase(mod, feet):
    zs = sorted(set(round(z, 2) for x, z in feet)); half = 30 if mod == "B" else 20; y0 = 43 if mod == "B" else 63
    members = []
    for i, z in enumerate(zs):
        xs = [x for x, zz in feet if abs(z - zz) < .1]
        if len(xs) < 2: continue
        lo, hi = B_SASE_X if mod == "B" and z in (-110, -760) else (min(xs) - 20, max(xs) + 20)
        members.append(rhs(mod + "_alt_sasi_boyuna_" + str(i), mod, (lo, hi, y0, 123, z - half, z + half), 0, note=("60×80×3" if mod == "B" else "40×60×3") + " kutu profil"))
    for i, x in enumerate(sorted(set(round(x, 2) for x, z in feet))):
        local = [z for xx, z in feet if abs(x - xx) < .1]
        if len(local) < 2: continue
        extra = mod == "E" and len([xx for xx, zz in feet if zz == min(local)]) == 1
        r = rhs(mod + "_alt_sasi_enine_" + str(i), mod, (x - half, x + half, y0, 123, min(local) + (-half if extra else half), max(local) + (half if extra else -half)), 2, note="kutu profil · boyunaya kaynaklı")
        for other in members:
            if overlap(bb(r["shape"]), bb(other["shape"])): r["shape"] = r["shape"].cut(box(*bb(other["shape"])))
        solids = r["shape"].Solids(); r["shape"] = solids[0]; seg = [r]
        for k, s_ in enumerate(solids[1:]): seg.append(add(r["name"] + "_parca_" + str(k + 1), mod, s_, note="ayrı profil parçası"))
        members.extend(seg)
    for x, z in feet:
        bore = cyl_y(x, z, 6.5, y0 - 1, 124)
        for p in members:
            if overlap(bb(p["shape"]), bb(bore)): p["shape"] = p["shape"].cut(bore)
        add(mod + "_M12_ayak_yuvasi_%g_%g" % (x, z), mod, box(x - 12, x + 12, 108, 120, z - 12, z + 12).cut(cyl_y(x, z, 6.5, 107, 121)), note="M12 kaynak somunu")


B_KESILIR = ("bolme_", "taban_", "tavan_", "yan_ic_sac")              # _B_yuk'un keserek yer açtığı dolap parçaları (+ bütün PU) — v1 ile aynı liste


def _dikme_engeli(x, z, pay=0.0):
    """v2 · (x, z) dikme kutusunun (pabuç 123 … dikme üstü 743,5 · z'de ± pay büyütülmüş) KESEMEYECEĞİ mevcut dolap parçaları — gerçek kesişim > 0,1 mm³"""
    d = box(x - 15, x + 15, 123, 743.5, z - 15 - pay, z + 15 + pay); bd = bb(d); out = []
    for p in PARTS:
        if p["new"] or p["module"] != "B" or p["material"] == "PU" or any(k in p["name"] for k in B_KESILIR): continue
        if overlap(bb(p["shape"]), bd) and abs(p["shape"].intersect(d).Volume()) > .1: out.append(p)
    return out


def _sarar(p, x, z):
    """dolabın kendi dikey taşıyıcısı (adında 'dikme') B/AC dikmesinin ayak izini (x ± 15, z ± 15) tümüyle sarıyor mu → ORTAK kullanılabilir"""
    b = bb(p["shape"])
    return "dikme" in p["name"] and b[0] <= x - 15 + 1e-6 and x + 15 - 1e-6 <= b[1] and b[4] <= z - 15 + 1e-6 and z + 15 - 1e-6 <= b[5]


def _td_dikme(x, z):
    """v2: (x, z) ekseninde dolabın kendi dikey taşıyıcısı (store_cad_v14 fırın taşıyıcı dikmesi TD · tasiyici_dikme_*) varsa o parça → B/AC dikmesi
    kurulmaz, o dikme ORTAK kullanılır · başka bir engel varsa (dikme olmayan ya da ayak izini sarmayan) çakışan dikme kurmak yerine DURUR (assert)"""
    eng = _dikme_engeli(x, z)
    if not eng: return None
    td = [p for p in eng if _sarar(p, x, z)]
    assert td and len(td) == len(eng), "h2_moduler_v1: B/AC dikmesi x %.1f z %.0f mevcut dolap parçasına çarpıyor: %s" % (x, z, [p["name"] for p in eng])
    return td[0]


def _hat_z(z0, xs):
    """v2 · taşıyıcı hattının z'si: v1 z'si (z0) hiçbir dikmede ORTAK-olmayan engele çarpmıyorsa AYNEN · çarpıyorsa bütün hat (kiriş + dikmeleri) ÖNE 1 mm adımla,
    her dikmede B_AC_BOSLUK boşlukla engelsiz ilk z'ye kayar (arkaya kaymaz: plenumun hava + kablo geçişleri) · B_AC_ARAMA içinde yoksa DURUR (assert)"""
    ilk = sorted({p["name"] for x in xs for p in _dikme_engeli(x, z0) if not _sarar(p, x, z0)})
    if not ilk: return z0, ilk
    for k in range(1, B_AC_ARAMA + 1):
        z = z0 + k
        if all(not [p for p in _dikme_engeli(x, z, B_AC_BOSLUK) if not _sarar(p, x, z)] for x in xs):
            print("h2_moduler_v1 · B/AC hattı z %.0f → %.0f (öne %d mm): v1 z'sinde dikmeler dolap parçasına çarpıyordu %s · yeni z'de %.0f mm boşluk"
                  % (z0, z, k, ilk, B_AC_BOSLUK), flush=True)
            return z, ilk
    raise AssertionError("h2_moduler_v1: B/AC hattı z %.0f dikmeleri %s parçalarına çarpıyor, öne %d mm içinde engelsiz z yok" % (z0, ilk, B_AC_ARAMA))


def _bolme_pu(x, z):
    """v2 · dikme (x ± 15, z ± 15) bir bölmenin / sol duvarın PU'sunun İÇİNDE mi (mevcut dolap parçalarından ölçülür) → PU parçasının adı"""
    for p in PARTS:
        if p["new"] or p["module"] != "B" or p["material"] != "PU" or not p["name"].startswith(("bolme_", "yan_pu_sol")): continue
        b = bb(p["shape"])
        if b[0] - 1e-6 <= x - 15 and x + 15 <= b[1] + 1e-6 and b[4] - 1e-6 <= z - 15 and z + 15 <= b[5] + 1e-6: return p["name"]
    return None


def _B_yuk():
    xs = B_AC_DIKME_X
    B_AC_ORTAK[:] = []; B_AC_Z_UYGULANAN[:] = []
    for i, z0 in enumerate(B_AC_Z):
        z, eng0 = _hat_z(z0, xs)                                                               # v2: engel varsa hat öne kayar (kiriş + dikmeler birlikte)
        B_AC_Z_UYGULANAN.append((i, z0, z, eng0))
        ortak = {j: _td_dikme(x, z) for j, x in enumerate(xs)}
        # kirişin sağ ucu: son dikme ORTAK (TD) ise v1'deki gibi TK_X0'da alın alına (TD dikmesi + fırın taşıyıcı kirişi) · yeni dikmeyse üstüne oturur (x + 15)
        x1 = TK_X0 if ortak[len(xs) - 1] is not None else xs[-1] + PROFIL / 2.0
        rhs("B_AC_ust_kiris_" + str(i), "B", (B_AC_X0, x1, 743.5, 783.5, z - 15, z + 15), 0, 2, note="30×40×2 · A/C yükünü bölme dikmelerine")
        add("B_AC_ust_isikesici_" + str(i), "B", box(B_AC_X0, x1, 783.5, 786.5, z - 15, z + 15), "GFRP", "thermal", "3 mm GFRP ısı kesici")
        for j, x in enumerate(xs):
            if ortak[j] is not None:
                B_AC_ORTAK.append((i, j, x, z, ortak[j]["name"])); continue                    # v2: fırın TD dikmesi ORTAK — çakışan ikinci dikme YOK
            assert _bolme_pu(x, z), "h2_moduler_v1: B/AC dikmesi x %.1f z %.0f bölme / sol duvar PU'sunun içinde değil (dolap v2 bölmeleri beklenen yerde mi?)" % (x, z)
            rhs("B_AC_dikme_%d_%d" % (i, j), "B", (x - 15, x + 15, 127.5, 743.5, z - 15, z + 15), 1, 2, note="30×30×2 · bölme / duvar içinde")
            add("B_AC_alt_isikesici_%d_%d" % (i, j), "B", box(x - 15, x + 15, 124.5, 127.5, z - 15, z + 15), "GFRP", "thermal", "3 mm GFRP")
            add("B_AC_alt_pabucluk_%d_%d" % (i, j), "B", box(max(B_PABUC_X0, x - 15), x + 15, 123, 124.5, z - 15, z + 15), note="taşıma pabucu")
    ins = [p for p in PARTS if p["new"] and p["module"] == "B" and p["name"].startswith("B_AC_")]
    for p in PARTS:
        if p["new"] or p["module"] != "B": continue
        if p["material"] != "PU" and not any(k in p["name"] for k in B_KESILIR): continue
        b = bb(p["shape"])
        for q in ins:
            if overlap(b, bb(q["shape"])): p["shape"] = p["shape"].cut(q["shape"])


def _baglanti():
    """v2'den beri ÇAĞRILMAZ (Kemal 29 Eyl: bağlantı kararı sonra) · x'ler v2'ye taşındı (A / C sol grup · B–K / K–E yerinde)"""
    for label, mod, xs in [("B_K", "K", (3970, 4050)), ("K_E", "E", (4550, 4660))]:
        plate = box(xs[0] - 15, xs[1] + 15, 59, 63, -125, -95)
        if label == "B_K": plate = box(xs[0] - 15, 4000, 39, 43, -125, -95).fuse(box(3996, 4000, 43, 63, -125, -95)).fuse(box(4000, xs[1] + 15, 59, 63, -125, -95))
        for x in xs:
            y = 39 if label == "B_K" and x == xs[0] else 59
            bore = cyl_y(x, -110, 4.5, y - 1, y + 17); plate = plate.cut(bore)
            for p in PARTS:
                if p["new"] and "alt_sasi" in p["name"] and overlap(bb(p["shape"]), bb(bore)): p["shape"] = p["shape"].cut(bore)
            add("M8_baglanti_civata_" + label + "_" + str(x), mod, cyl_y(x, -110, 4, y, y + 16).fuse(cyl_y(x, -110, 6.5, y - 5, y)), kind="connection")
            add("M8_baglanti_somun_" + label + "_" + str(x), mod, box(x - 6.5, x + 6.5, y + 7, y + 14, -116.5, -103.5).cut(cyl_y(x, -110, 4.2, y + 6, y + 15)), kind="connection")
        add("montaj_baglanti_" + label, mod, plate, kind="connection", note="304 4 mm bağlama plakası · M8")
    for mod, xs in [("A", (XA0 + 28.0, XA1 - 28.0)), ("C", (H.C_X[0] + 28.0, H.C_X[1] - 28.0))]:
        for x in xs:
            z = -110; bore = cyl_y(x, z, 4.5, 770, 793)
            for p in PARTS:
                if p["module"] in (mod, "B") and p["kind"] != "inside" and overlap(bb(p["shape"]), bb(bore)): p["shape"] = p["shape"].cut(bore)
            add(mod + "_B_M8_civata_" + str(x), mod, cyl_y(x, z, 4, 771, 792).fuse(cyl_y(x, z, 6.5, 792, 797)), kind="connection")
            add(mod + "_B_M8_rondela_" + str(x), mod, cyl_y(x, z, 9, 790, 792).cut(cyl_y(x, z, 4.5, 789, 793)), kind="connection")
            add(mod + "_B_M8_disli_yuva_" + str(x), "B", box(x - 6.5, x + 6.5, 774.5, 781.5, z - 6.5, z + 6.5).cut(cyl_y(x, z, 4.2, 774, 782)), kind="connection")


def _kaplama_payi():
    st = [p for p in PARTS if p["new"] and p["kind"] == "frame"]
    for p in PARTS:
        if p["new"] or p["module"] not in ("B", "K", "E"): continue
        if not p["name"].startswith(("onyuz_plint", "taban_", "tavan_", "bolme_", "yan_pu")): continue
        b = bb(p["shape"])
        for q in st:
            if q["module"] == p["module"] and overlap(b, bb(q["shape"])):
                if abs(p["shape"].intersect(q["shape"]).Volume()) > .1: p["shape"] = p["shape"].cut(q["shape"])


def uygula(M):
    """M: ana montaj modül ad alanı (SC, KS, KC, AK, KD, TC, X_K, X_E, Y_MEK). Mevcut parçaları yerinde değiştirir, YENI döner."""
    PARTS[:] = []; YENI[:] = []; DEGISEN[:] = []
    _kaynak(M)
    _A(M)
    for mod in ("B", "K", "E"):
        feet = []
        for p in PARTS:
            if p["module"] == mod and not p["new"] and p["name"].startswith("ayak_"):
                b = bb(p["shape"]); feet.append(((b[0] + b[1]) / 2, (b[4] + b[5]) / 2))
        _alt_sase(mod, feet)
    _B_yuk(); _kaplama_payi()                                           # v2 (Kemal 29 Eyl): modüller arası BAĞLANTI YOK — "nasıl bağlanacaklarına şu an karar vermeyeceğiz" (A/C–B M8 cıvata + delik + dişli yuva, B–K / K–E bağlama plakası + M8 kalktı)
    for p in PARTS:                                                     # geri yaz: değişen mevcut parçalar
        if p["new"] or p["shape"] is p["s0"]: continue
        sh = p["shape"].translate(V(-p["off"], 0, 0)) if p["off"] else p["shape"]
        p["src"]["wp"] = cq.Workplane(obj=sh)
        DEGISEN.append(p["module"] + ":" + p["name"])
    return YENI
