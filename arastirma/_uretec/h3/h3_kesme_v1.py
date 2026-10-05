# -*- coding: utf-8 -*-
"""HAT VERSİYON 3 · K KESME ADAPTÖRÜ v1 (30 Eyl 2026 · Claude · YEREL) — montajda 'import h3_kesme_v1 as KS' (kesme_cad_v11 yerine).
kesme_cad_v11 YENİDEN ÇİZİLMEZ ve DEĞİŞMEZ: sabitler / zaman işlevleri AYNEN yayımlanır; yalnız PARÇA LİSTESİ v3 için düzenlenir.

Kemal HAT v2.7 ("kompresörü sola çekip yağ tenekesini onun yerine sağ tarafa koysak, arada boruyla bağlantı" · K'nın altı dolabın teknik sütunu):
  · ALT DOLAP YOK: K dolabın üstüne (788) oturur (4 ayak yok) · taban sacı + taban taşıyıcıları + alt ön / arka kayıt 665 yukarı (788–821) · köşe dikmeleri, yan + arka
    saclar 791'den başlar · alt kapak 791–883 sabit ön bant sacı · plint ve taban hortum rakoru yok (istasyon tabanındaki rakor deliği kapatılır)
  · YAĞ TENEKESİ + TARTI + TAVA FIRIN ÜSTÜNDE sağda (dünya x 3742–3985 · raf 1348 · kompresör solunda): teneke / emme lansı / adaptör / yük hücresi aynı
    katalog parçaları (öteleme) · tartı platformu 238 × 238 (v11 260: raf genişliğine göre · teneke 235 × 235) · tava 243 × 268 × 20 yeniden
  · POMPA GRUBU (raf + 2 köşebent + plaka + filtre + GJ-N21 + T + PM1704 + KBP) v11 düzeniyle AYNEN, K'nın ÜST ÖNÜNE (y +1000 · z +185): raf y 1640 · z −600…−438
  · hortumlar: emiş + dönüş teneke adaptöründen y 1828'de F|K duvarından (Ø14 / Ø12 lastik bilezikli geçiş) K'ya · basınç T'den öne → sağ yanda (x 355) iner →
    y 1215'te nozüle (v11 son parçası aynı) · adaptör çıkışında 90° LQ dirsek (tavan 1840: esnek büküm R 70'e yer yok)
KOORDİNAT: K yereli (kesme_cad_v11 ile aynı) — x 0…400 (dünya = x + 4000; fırın üstündeki teneke seti x < 0) · y yerden · z ön +79 / arka −830.
Çalıştır (öz denetim): python ob_calistir.py h3/h3_kesme_v1.py"""
import math, os, sys, time

H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_hesap_v1 as HS
import kesme_cad_v11 as K11

for _k, _v in list(vars(K11).items()):
    if _k.startswith("__") and _k.endswith("__"):
        continue
    globals()[_k] = _v

V = cq.Vector
X_K = HS.K_X[0]                                   # 4000
DY_ALT = HS.Y_DUZ - K11.Y_PLINT                   # 665 · taban 123 → 788 (dolap üstü)
Y_GOVDE0 = HS.Y_DUZ + 3.0                         # 791 · taban sacının üstü: köşe dikmeleri, yan / arka saclar buradan
T_P = (0.0, 1000.0, 185.0)                        # pompa grubu: raf y 640 → 1640 · z −785…−623 → −600…−438 (K üst önü, DGRF'nin üstü 1591)
YAG = dict(tava=(HS.YAG_X[0], HS.YAG_X[1], 1348.0, 1368.0, -418.0, -150.0),               # dünya · fırın üstü raf (1348) · kompresör açıklığının 2 sağı
           tarti=(3744.5, 3982.5, -415.0, -177.0),                                            # 238 × 238 platform (x, z) · teneke 235 × 235
           teneke_x0=3746.0)                                                                  # teneke 3746–3981 (sağdaki gazlı yay 3982: öne çekilir)
T_F = (YAG["teneke_x0"] - X_K - K11.TNK["x"][0], YAG["tava"][2] - 126.0, (YAG["tarti"][2] + YAG["tarti"][3]) / 2.0 - (K11.TNK["z"][0] + K11.TNK["z"][1]) / 2.0)
Y_GECIS = 1828.0                                  # emiş / dönüş hortumu F|K duvar geçişi (adaptör üstü 1821 · fırın üstü tavan sacı 1840)
Z_GECIS = dict(emis=-250.0, donus=-180.0)
SIL = ("plint_on", "taban_hortum_rakoru", "yag_damlama_tavasi_10", "yag_tarti_taban_plakasi", "yag_tarti_platformu",
       "yag_basinc_hortumu_TLM1008", "yag_emis_hortumu_TLM1008", "yag_donus_hortumu_TLM0806")
YUKARI = ("taban_sac_3", "taban_sac_tasiyici_", "onyuz_kayit_140_")               # +665
KES = ("kose_dikmesi_", "arka_sac", "sol_sac_urun_girisi", "sag_sac_E_penceresi", "onyuz_kapak_alt")   # y ≥ 791
TENEKE_SETI = ("yag_tarti_alt_takozu", "yag_tarti_yuk_hucresi_PW15AH", "yag_tarti_ust_takozu", "yag_tenekesi_18L", "yag_emme_lansi_1038304", "yag_agiz_adaptoru")
POMPA_SETI = ("yag_pompa_rafi", "yag_pompa_rafi_kosebendi_sol", "yag_pompa_rafi_kosebendi_sag", "yag_pompa_plakasi", "yag_emis_filtresi", "yag_boru_filtre_pompa",
              "yag_pompasi_GJ-N21_EagleDrive", "yag_boru_pompa_T", "yag_T_parcasi", "yag_basinc_sensoru_PM1704", "yag_boru_T_regulator", "yag_geri_basinc_regulatoru_KBP")
F_DUVAR_DELIKLERI = []                            # (FU parça adı, dünya kesici, not) — montaj fırın üstü kabinin sağ yan sacına keser
DEGISEN, CIKAN, YENI = [], [], []


def _tek(wp):
    if hasattr(wp, "vals"):
        v = [o for o in wp.vals() if isinstance(o, cq.Shape)]
        return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)
    return wp


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def boru_d(pts, r):
    """düz boru parçaları + köşelerde küre (rijit LQ dirsek rakorları)"""
    ss = []
    for a, b in zip(pts[:-1], pts[1:]):
        v = V(*b) - V(*a)
        if v.Length > 1e-6: ss.append(cq.Solid.makeCylinder(r, v.Length, V(*a), v.normalized()))
    for p in pts[1:-1]: ss.append(cq.Solid.makeSphere(r, V(*p), angleDegrees1=-90, angleDegrees2=90))
    s = ss[0]
    for q in ss[1:]: s = s.fuse(q)
    return s.clean()


def _bul(ad):
    q = [p for p in PARCALAR if p["ad"] == ad]
    assert len(q) == 1, (ad, len(q))
    return q[0]


def _yeni(ad, sh, mal, bom=None, grup="SABIT"):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=cq.Workplane(obj=sh), mal=mal, grup=grup, bom=bom))
    YENI.append(ad)


def lans_portlari():
    """teneke adaptörünün emiş / dönüş portları (K yereli, v3 yerinde): [(x, y üst, z)]"""
    ay = K11.teneke_ust() + K11.TENEKE["agiz_h"] + K11.LANS["kap_h"] + 8.0 + T_F[1]
    return {k: (x + T_F[0], ay, K11.TNK_AGIZ[1] + T_F[2]) for x, k in K11.LANS["port"]}


def hortum_yollari():
    P = lans_portlari()
    pg = K11.PG
    fx, ftop = pg["filtre"][0], pg["filtre"][3] + T_P[1]                     # filtre ekseni x 80 · üstü 1744,5
    bx, btop = pg["bpr"][0], pg["bpr"][3] + T_P[1]                           # KBP ekseni x 295 · üstü 1761,5
    pz = K11.POMPA_Z + T_P[2]                                                # −520
    pe, pd = P["emis"], P["donus"]
    emis = [pe, (pe[0], Y_GECIS, pe[2]), (pe[0], Y_GECIS, Z_GECIS["emis"]), (fx, Y_GECIS, Z_GECIS["emis"]), (fx, Y_GECIS, pz), (fx, ftop, pz)]
    donus = [(bx, btop, pz), (bx, Y_GECIS, pz), (bx, Y_GECIS, Z_GECIS["donus"]), (pd[0], Y_GECIS, Z_GECIS["donus"]), (pd[0], Y_GECIS, pd[2]), pd]
    ty, tz = K11.POMPA_Y + T_P[1], K11.PG["t"][5] + T_P[2]                  # T ekseni y 1688,7 · ön yüzü −510
    basinc = [(K11.PG["t"][0] + 10.0, ty, tz), (K11.PG["t"][0] + 10.0, ty, -425.0), (355.0, ty, -425.0), (355.0, K11.Y_HORTUM, -425.0),
              (K11.X_NZ, K11.Y_HORTUM, -425.0), (K11.X_NZ, K11.Y_HORTUM, K11.Z_NZ - 22.0)]
    return dict(emis=emis, donus=donus, basinc=basinc)


def modul():
    """v3 parça listesi: kesme_cad_v11.modul() → alt dolap yok + yağ seti fırın üstü / K üst önü · İDEMPOTENT"""
    t0 = time.time()
    K11.modul()
    DEGISEN[:] = []; CIKAN[:] = []; YENI[:] = []; F_DUVAR_DELIKLERI[:] = []
    PARCALAR[:] = [p for p in PARCALAR if not ((p["ad"] in SIL or p["ad"].startswith("ayak_")) and CIKAN.append(p["ad"]) is None)]
    assert set(SIL) <= set(CIKAN) and len([a for a in CIKAN if a.startswith("ayak_")]) == 4, CIKAN       # + 4 ayak (K dolabın üstünde)
    for p in PARCALAR:
        a = p["ad"]; s = _tek(p["wp"]); yeni = None
        if a.startswith(YUKARI):
            yeni = s.translate(V(0, DY_ALT, 0))
        elif a.startswith(KES):
            b = s.BoundingBox()
            if b.ymin < Y_GOVDE0 - 1e-6:
                yeni = s.intersect(kutu(b.xmin - 1, b.xmax + 1, Y_GOVDE0, b.ymax + 1, b.zmin - 1, b.zmax + 1))
        elif a in TENEKE_SETI:
            yeni = s.translate(V(*T_F))
        elif a in POMPA_SETI:
            yeni = s.translate(V(*T_P))
        elif a == "istasyon_tabani_3":
            yeni = s.fuse(cq.Solid.makeCylinder(18.5, 3.0, V(380.0, 892.0, -600.0), V(0, 1, 0))).clean()   # v11 taban rakoru deliği kapanır (basınç hattı artık üstten)
        if yeni is not None:
            p["wp"] = cq.Workplane(obj=yeni); DEGISEN.append(a)
    # alt ön bant sacının BOM'u
    p = _bul("onyuz_kapak_alt")
    if p.get("bom"):
        b = list(p["bom"]); b[0] = "Ön alt bant sacı (v3 · alt dolap yok: eski alt kapağın 791–883 kısmı, sabit)"; p["bom"] = tuple(b)
    # fırın üstündeki tava + tartı platformu (yeniden · dünya → K yereli)
    tx0, tx1, ty0, ty1, tz0, tz1 = YAG["tava"]
    tava = kutu(tx0, tx1, ty0, ty1, tz0, tz1).cut(kutu(tx0 + 1.0, tx1 - 1.0, ty0 + 1.0, ty1 + 1.0, tz0 + 1.0, tz1 - 1.0)).translate(V(-X_K, 0, 0))
    _yeni("yag_damlama_tavasi_F", tava, "sac", bom=("Yağ damlama tavası AISI 304 1,0 · köşeler kaynaklı (v11 tavası gibi · v3: fırın üstü rafta)", 1,
          "%.0f × %.0f × 20 · teneke + tartı altı" % (tx1 - tx0, tz1 - tz0), "v3 · fırın üstü", "ÜRETİM"))
    ax0, ax1, az0, az1 = YAG["tarti"]
    ya, yb = K11.TARTI["taban"][2] + T_F[1], K11.TARTI["taban"][3] + T_F[1]
    _yeni("yag_tarti_taban_plakasi", kutu(ax0, ax1, ya, yb, az0, az1).translate(V(-X_K, 0, 0)), "celik",
          bom=("Tartı taban plakası AISI 304 8 mm (v3: 238 × 238)", 1, "yük hücresinin alt takozu 2 × M8", "v3", "ÜRETİM"))
    ya, yb = K11.TARTI["plat"][2] + T_F[1], K11.TARTI["plat"][3] + T_F[1]
    _yeni("yag_tarti_platformu", kutu(ax0, ax1, ya, yb, az0, az1).translate(V(-X_K, 0, 0)), "celik",
          bom=("Tartı platformu AISI 304 4 mm (v3: 238 × 238 · teneke 235 × 235)", 1, "HBM PW15AH tek nokta yük hücresi üstünde", "v3", "ÜRETİM"))
    # hortumlar (rijit dirsekli) + duvar geçişleri
    H = hortum_yollari()
    for ad_, k, r in (("yag_basinc_hortumu_TLM1008", "basinc", 5.0), ("yag_emis_hortumu_TLM1008", "emis", 5.0), ("yag_donus_hortumu_TLM0806", "donus", 4.0)):
        uz = sum(math.dist(a, b) for a, b in zip(H[k][:-1], H[k][1:]))
        _yeni(ad_, boru_d(H[k], r), "hortum_yag", bom=("%s SMC %s PFA + LQ2 dirsek rakorları" % ({"basinc": "Basınç hattı", "emis": "Emiş hattı", "donus": "Dönüş hattı"}[k],
              "TLM1008" if r == 5.0 else "TLM0806"), 1, "≈ %.2f m · v3: %s" % (uz / 1000.0, "T → sağ yan → nozül" if k == "basinc" else "teneke (fırın üstü) ↔ pompa grubu (K üstü) · F|K duvarından y %.0f" % Y_GECIS),
              K11.KAYNAK_HORTUM, "SATIN ALMA"))
    sol = _bul("sol_sac_urun_girisi"); s = _tek(sol["wp"])
    for k, r in (("emis", 7.0), ("donus", 6.0)):
        z = Z_GECIS[k]
        s = s.cut(cq.Solid.makeCylinder(r, 4.0, V(-1.0, Y_GECIS, z), V(1, 0, 0)))
        cyl = lambda rr, x0_, x1_: cq.Solid.makeCylinder(rr, x1_ - x0_, V(x0_, Y_GECIS, z), V(1, 0, 0))
        bil = cyl(r, -1.5, 1.5).fuse(cyl(r + 3.0, -2.5, -1.5)).fuse(cyl(r + 3.0, 1.5, 2.5)).cut(cyl(r - 1.5, -3.0, 3.0)).clean()   # iki sacı (F 3998,5–4000 · K 4000–4001,5) birlikte geçer, dış yüzlerde flanş
        _yeni("yag_duvar_gecis_bilezigi_%s" % k, bil, "conta", bom=("Lastik geçiş bileziği (F|K duvarı · yağ hortumu)", 2, "EPDM · Ø%.0f delik" % (2 * r), "v3", "SATIN ALMA") if k == "emis" else None)
        F_DUVAR_DELIKLERI.append(("f_ust_yan_sag", cq.Solid.makeCylinder(r, 20.0, V(X_K - 18.0, Y_GECIS, z), V(1, 0, 0)), "yağ %s hortumu geçişi Ø%.0f" % (k, 2 * r)))
    sol["wp"] = cq.Workplane(obj=s)
    print("h3_kesme_v1 · K v3 parca listesi: %d (cikan %d · degisen %d · yeni %d) · %.0f sn" % (len(PARCALAR), len(CIKAN), len(DEGISEN), len(YENI), time.time() - t0))
    return PARCALAR


# ================================================================ DENETİM ================================================================
DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger))
    print("  %-150s %s %s" % (ad, "GECTI" if sart else "** KALDI **", deger))


def _bbk(A, B, pay=0.05):
    return A.xmin < B.xmax - pay and B.xmin < A.xmax - pay and A.ymin < B.ymax - pay and B.ymin < A.ymax - pay and A.zmin < B.zmax - pay and B.zmin < A.zmax - pay


def denetim():
    t0 = time.time()
    if not YENI: modul()
    DEN[:] = []
    GR_HARIC = ("URUN", "URUN_IZ", "REF", "SPREY")
    S = [(p["ad"], _tek(p["wp"])) for p in PARCALAR if p["grup"] not in GR_HARIC]
    alt = [a for a, s in S if s.BoundingBox().ymin < HS.Y_DUZ - 1e-6]
    kontrol("ALT DOLAP YOK: dolap üstünün (788) altında K parçası yok", not alt, str(alt[:5]))
    tb = _tek(_bul("taban_sac_3")["wp"]).BoundingBox()
    kontrol("K TABANI dolabın üstünde: taban sacı y %.1f–%.1f" % (tb.ymin, tb.ymax), abs(tb.ymin - HS.Y_DUZ) < 0.01)
    oyn = [p["ad"] for p in PARCALAR if p["ad"].startswith(("yag_", "PulsaJet", "nozul_"))]
    kontrol("YAĞ SİSTEMİ %d parça · teneke seti fırın üstünde (dünya x ≥ %.0f) · pompa grubu K üst önünde" % (len(oyn), HS.YAG_X[0]),
            all(_tek(_bul(a)["wp"]).BoundingBox().xmin + X_K >= HS.YAG_X[0] - 0.01 for a in TENEKE_SETI + ("yag_damlama_tavasi_F", "yag_tarti_platformu"))
            and all(_tek(_bul(a)["wp"]).BoundingBox().xmin >= 0.0 for a in POMPA_SETI))
    tn = _tek(_bul("yag_tenekesi_18L")["wp"]).BoundingBox(); tv = _tek(_bul("yag_damlama_tavasi_F")["wp"]).BoundingBox()
    kontrol("TENEKE dünya x %.1f–%.1f (≤ 3981: sağ gazlı yay 3982) · y %.0f–%.0f · tava x %.0f–%.0f · adaptör üstü %.0f < %.0f (hortum geçişi) < 1840 (tavan)"
            % (tn.xmin + X_K, tn.xmax + X_K, tn.ymin, tn.ymax, tv.xmin + X_K, tv.xmax + X_K, lans_portlari()["emis"][1], Y_GECIS),
            tn.xmax + X_K <= 3981.01 and lans_portlari()["emis"][1] + 5.0 <= Y_GECIS and Y_GECIS + 5.0 < 1840.0)
    # çakışma: yeni + değişen parçalar ↔ bütün K (dinlenme konumu) · hareketli grupları zaman boyunca montaj denetler
    D = set(YENI) | set(a for a in DEGISEN if a in TENEKE_SETI + POMPA_SETI)
    SH = dict(S)
    bul = []
    for a in D:
        A = SH[a]; ba = A.BoundingBox()
        for c, C in S:
            if c == a or c in D and c < a: continue
            if not _bbk(ba, C.BoundingBox()): continue
            v = A.intersect(C).Volume()
            if v > 0.1: bul.append((round(v, 2), a, c))
    bilinen = {("yag_emme_lansi_1038304", "yag_agiz_adaptoru"), ("yag_agiz_adaptoru", "yag_emme_lansi_1038304"),
               ("yag_tenekesi_18L", "yag_emme_lansi_1038304"), ("yag_emme_lansi_1038304", "yag_tenekesi_18L"), ("yag_tenekesi_18L", "yag_agiz_adaptoru"), ("yag_agiz_adaptoru", "yag_tenekesi_18L")}
    bul = [b for b in bul if (b[1], b[2]) not in bilinen]
    for b in sorted(bul, reverse=True)[:12]: print("    ", b)
    kontrol("ÇAKIŞMA yeni / taşınan yağ parçaları ↔ K (dinlenme) > 0,1 mm³ = 0 (lans ↔ teneke ↔ adaptör v11'de de iç içe)", not bul, "%d bulgu" % len(bul))
    kal = [d for d in DEN if not d[1]]
    print("DENETIM h3_kesme_v1: %d madde · %d KALDI · %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    return DEN


if __name__ == "__main__":
    modul()
    D = denetim()
    kal = [d[0] for d in D if not d[1]]
    assert not kal, kal
    sys.stdout.flush(); os._exit(0)
