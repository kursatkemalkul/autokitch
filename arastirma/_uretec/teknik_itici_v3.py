# -*- coding: utf-8 -*-
"""AUTOKITCH · AKTARMA İTİCİSİ · TEKNİK RESİM v3 (27 Eyl 2026) · ALÇAK HAT
v3: itici_cad_v4 (disk üstü 1000; bütün kotlar v2'ye göre 168 aşağı). Paftadaki her y değeri modülden okunur (IT.DISK_UST, IT.TAVAN,
IT.Y_SERBEST, IT.PIDE_UST, IT.TOP_UST, IT.BAR_Y0/1, IT.Y_TABLA_YUZ, IT.PIVOT_Y, IT.MAKARA) — v2'deki 1168/1277/1210/1224/1196/1201 sabitleri yok.
Fırın tarafı (üst görünüş x–z) firin_tp10_cad_v7 sabitlerinden; iniş boruları + tabla boş sensörü IT.kontrol_hepsi'deki konumlardan.
Kol (link + çubuk) ve kaldırma pimi v2'deki zarf kutusu yerine katıdan alınan ince dilim kesitiyle çizilir (kalkık kol üstte/yanda, inik kol önde).
Yerleşim v2 ile aynı (üst sol · yan kesit sağ üst · ön görünüş en sağ · liste alt); v2'deki üst üste binen yazılar ayrıldı,
yazı ↔ yazı ve yazı ↔ çizgi çakışması çizimden sonra otomatik denetlenir (ÇAKIŞMA satırı).
Denetim düzeltmesi (27 Eyl): parça listesinde itici_cad_v4 BOM notlarındaki iki metin hatası paftada modelden ölçülen değerle yazılır
(kol_link_cubuk "kalkınca y 1054–1058" → ölçülen 1044–1056 · kaldirma_pimi "pide üstü 1033" → topping üstü 1033; modül metni v5'te düzeltilmeli);
AÇIK 4 (topping_uno v12) kaldırıldı: SPEC v57 kararı TU'yu montajda bir kez −168 kaydırır, hat_montaj_v57 SOZLESME TU_YAL_Y0 = IT.TAVAN = 1109 denetler.
Önceki: teknik_itici_v2.py (itici_cad_v3). Kural: paftada yalnız görünüş + ölçü + parça adı; açıklama mesajda.
Çizim yardımcıları teknik_firin_tp10_v3.py'den (aynı sayfa düzeni)."""
import ast, inspect, io, math, os, sys, textwrap
U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
_yrd = io.open(os.path.join(U, "teknik_firin_tp10_v3.py"), encoding="utf-8").read().split("# ============================== VERİ")[0]
exec(compile(_yrd, "teknik_yardimci", "exec"))
import itici_cad_v4 as IT
import firin_tp10_cad_v7 as FT

SURUM = "v3"
_sayi0 = sayi


def sayi(v):                                         # v3: −0 yazmaz, eksi işareti "−"
    r = round(v, 1)
    return _sayi0(0.0 if r == 0 else r).replace("-", "−")


# ============================== VERİ (TEK KAYNAK: itici_cad_v4 · firin_tp10_cad_v7) ==============================
_YEREL = IT.yerel                                    # dünya dönüşümü (ölçüm için saklanır)
IT.yerel = lambda wp: wp                             # parçaları YEREL (s, y, w) çerçevede kur: kutu zarfları buradan
IT.kur(IT.S_HOME, True); EV = [(p["ad"], p["wp"].val().BoundingBox(), p) for p in IT.PARCALAR]
IT.kur(IT.S_END, False); SON = [(p["ad"], p["wp"].val().BoundingBox()) for p in IT.PARCALAR]
IT.kur(IT.S_HOME, False); INIK = [(p["ad"], p["wp"].val().BoundingBox(), p) for p in IT.PARCALAR]
def zarf(L, ad): return [b for a, b, *_ in L if a == ad][0]
def parca(L, ad): return [p for a, b, p in L if a == ad][0]
def dn(s_, w_):  # yerel (s, w) → dünya (x, z)
    return (IT.PC[0] + s_ * IT.U[0] + w_ * IT.W[0], IT.PC[1] + s_ * IT.U[1] + w_ * IT.W[1])
S0 = IT.S_STROK0 - IT.MY["Z"] / 2.0; S1 = IT.S_STROK0 + IT.STROK + IT.MY["Z"] / 2.0
WA = IT.W_AXIS
DU, PU, TU, T, YS = IT.DISK_UST, IT.PIDE_UST, IT.TOP_UST, IT.TAVAN, IT.Y_SERBEST       # 1000 · 1028 · 1033 · 1109 · 1042
Y_GOV0, Y_GOV1 = T - 6.0 - IT.MY["NE"], T - 6.0                                          # MY1B16 gövdesi 1075,2 · 1103 (kiriş 6 altında)
R_DISK = FT.X_DISK_KENAR - IT.C0[0]                                                       # 170 (disk kenarı 2507 − disk merkezi 2337)

# iniş boruları + tabla boş sensörü: IT.kontrol_hepsi içindeki konumlar (tek kaynak, elle yazılmaz)
ENGEL = {}
for _n in ast.walk(ast.parse(textwrap.dedent(inspect.getsource(IT.kontrol_hepsi)))):
    if isinstance(_n, ast.Assign) and len(_n.targets) == 1 and isinstance(_n.targets[0], ast.Name) and _n.targets[0].id in ("BORU_KASAR", "BORU_SUCUK", "SENSOR"):
        ENGEL[_n.targets[0].id] = eval(compile(ast.Expression(_n.value), "engel", "eval"), {"DISK_UST": IT.DISK_UST})
assert set(ENGEL) == {"BORU_KASAR", "BORU_SUCUK", "SENSOR"}, ENGEL


def _engel_kati(e):
    return (IT.sily(e[1], e[2], e[3], e[4], e[5]) if e[0] == "sil" else IT.kut(*e[1:])).val()


# ölçüm: MY1B16 gövdesi (dünya) ↔ iniş boruları / sensör en kısa mesafe (3B, OCC)
_gov = _YEREL(parca(EV, "my1b16_govde")["wp"]).val()
BOSLUK = {k: _gov.distance(_engel_kati(e)) for k, e in ENGEL.items()}
# ölçüm: kalkık çubuğun y zarfı (EV katısından, link/makara kulağı dışındaki dilim s S_HOME+25 … S_HOME+60)
_kol = parca(EV, "kol_link_cubuk")["wp"]
_dil = _kol.intersect(IT.kut(IT.S_HOME + 25.0, IT.S_HOME + 60.0, DU - 100.0, T + 100.0, -300.0, 300.0)).val().BoundingBox()
KALKIK_Y = (_dil.ymin, _dil.ymax)


def kesit(wp, kutu, secici, uv, n=720, en_az=0.0):
    """katının ince dilimle kesiti → dilim yüzünün dış tel(ler)i, çokgen (uv: Vector → görünüş koordinatı) · en_az: en büyük yüzün bu oranından küçük yüzler atlanır"""
    sl = wp.intersect(IT.kut(*kutu))
    yuz = sl.faces(secici).vals(); amax = max(f.Area() for f in yuz)
    return [[uv(f.outerWire().positionAt(i / float(n))) for i in range(n)] for f in yuz if f.Area() >= en_az * amax]


# kol (link + çubuk tek parça): v3'te zarf kutusu yerine gerçek kesit
#   yan kesit (s–y, EV kalkık): w = eksen (link + burç + çubuk + taban) ve w = makara kulağı (alt uzantı + kulak) dilimleri
#   ön görünüş (w–y, İNİK): s = plaka ortası (çubuk + link + alt uzantı + burç borusu)
_mw = WA + IT.MAKARA["w"]
KOL_YAN = (kesit(parca(EV, "kol_link_cubuk")["wp"], (-300.0, 500.0, DU - 50.0, T + 50.0, _mw + 5.0, _mw + 6.0), ">Z", lambda v: (v.x, v.y))
           + kesit(parca(EV, "kol_link_cubuk")["wp"], (-300.0, 500.0, DU - 50.0, T + 50.0, WA - 0.5, WA + 0.5), ">Z", lambda v: (v.x, v.y)))
KOL_ON = kesit(parca(INIK, "kol_link_cubuk")["wp"], (IT.S_HOME - 2.0, IT.S_HOME - 1.0, DU - 50.0, T + 50.0, -300.0, 300.0), ">X", lambda v: (v.z, v.y))
KOL_UST = kesit(parca(EV, "kol_link_cubuk")["wp"], (-300.0, 500.0, IT.PIVOT_Y - 2.0, IT.PIVOT_Y - 1.0, -300.0, 300.0), ">Y", lambda v: (v.x, v.z), en_az=0.05)
#   üst: kalkık plaka düzlemi (burç borusu duvarının 2 mm'lik dilimi atlanır: pivot braketinin altında kalır)
# kaldırma pimi (Ø8 pim + Ø18 boyun): eksenden geçen kesit
PIM_YAN = kesit(parca(EV, "kaldirma_pimi")["wp"], (-300.0, 500.0, DU - 50.0, T + 50.0, _mw - 0.5, _mw + 0.5), ">Z", lambda v: (v.x, v.y))
PIM_ON = kesit(parca(INIK, "kaldirma_pimi")["wp"], (IT.PIM_KALDIRMA_S - 0.5, IT.PIM_KALDIRMA_S + 0.5, DU - 50.0, T + 50.0, -300.0, 300.0), ">X", lambda v: (v.z, v.y))

# ============================== YERLEŞİM ==============================
# üst görünüş (x–z): sol üst · yan kesit (s–y): sağ üst · ön görünüş (w–y): en sağ, yan kesitle aynı y ölçeği · liste: alt
TIT_Y = 160.0                                          # üç görünüş başlığının satırı
UX0, UY0, US = 150.0, 395.0, 1.55                      # x 1960 → px 150 ; z 0 → py UY0
def ux(x): return UX0 + (x - 1960.0) * US
def uz(z): return UY0 + (-z) * US
KX0, KY_T, KS = 1360.0, 330.0, 2.6                     # s −190 → px 1360 ; y TAVAN → py KY_T
def kx(s_): return KX0 + (s_ + 190.0) * KS
def ky(y): return KY_T + (T - y) * KS
SL0, SL1 = -190.0, 310.0                               # yan kesit yatay çizgileri (s)
OX0, OS = 2760.0, 2.6                                  # w −110 → px 2760
def ox(w_): return OX0 + (w_ + 110.0) * OS
def oy(y): return ky(y)
WL0, WL1 = -110.0, 84.0                                # ön görünüş yatay çizgileri (w) · sağ ölçülerin (w 86) önünde biter
LX0, LY0 = 150.0, 1560.0

# ============================== YAZI KAYDI (çakışma denetimi) ==============================
YAZI = []                                              # (x, y, s, f, c, a, muaf)
MUAF = [False]


def txt(x, y, s, f=None, c=INK, a="la"):              # v3: yazılar sona ertelenir → önce bütün çizgiler, sonra çakışma ölçümü, sonra yazı
    YAZI.append((x, y, s, f or f11, c, a, MUAF[0]))


def olcu_h_kisa(x0, x1, y, s, f=None, c=INK):
    """kısa ölçü: çizgi + uçlar, yazı sol ucun dışında"""
    f = f or f9
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    txt(x0 - 8, y, s, f, c, "rm")


def rrect(pts, fill=None, outline=INK, w=2):
    d.polygon(pts, fill=fill, outline=outline, width=w)
def lokal_kutu(b, fill, outline=INK, w=2, dash=False):
    """yerel zarf (s, w) → üst görünüşte dikdörtgen"""
    pts = [ux(dn(s_, w_)[0]) for s_, w_ in ((b.xmin, b.zmin), (b.xmax, b.zmin), (b.xmax, b.zmax), (b.xmin, b.zmax))]
    pz_ = [uz(dn(s_, w_)[1]) for s_, w_ in ((b.xmin, b.zmin), (b.xmax, b.zmin), (b.xmax, b.zmax), (b.xmin, b.zmax))]
    P = list(zip(pts, pz_))
    if dash:
        for i in range(4): dline(P[i], P[(i + 1) % 4], outline, w)
    else:
        rrect(P, fill, outline, w)


def ust():
    txt(ux(1960), TIT_Y, "ÜST GÖRÜNÜŞ · x – z · evde (dolu) · sonda (kesik)", f16, ACC)
    XK = 2700.0                                                                                # görünüşün sağ kırpması
    # F fırın gövdesi (FT: ön yüzün ZS önünde … derinlik D_TP) + ön oda + giriş bandı + fırın bandı + tünel duvarları
    d.rectangle([ux(FT.X_F0), uz(FT.ZS), ux(XK), uz(FT.ZS - FT.D_TP)], fill=ODA_R, outline=LINE, width=2)
    gb = (FT.GB_XB - 11.5, FT.GB_XT + 11.5, FT.GB_Z[0] + FT.ZS, FT.GB_Z[1] + FT.ZS)          # rulo Ø20 + bant 1,5 (FT.adaptor) · z dünyada (+ZS)
    d.rectangle([ux(gb[0]), uz(gb[3]), ux(gb[1]), uz(gb[2])], fill=PASL, outline=INK, width=2)
    bz = FT.BANT_Z_D
    d.rectangle([ux(FT.BANT_X[0]), uz(bz[1]), ux(XK), uz(bz[0])], fill=(236, 236, 240), outline=INK, width=2)
    tz = FT.TUNEL_Z_D
    d.line([(ux(FT.X_DUV0), uz(tz[1])), (ux(XK), uz(tz[1]))], fill=RED, width=3); d.line([(ux(FT.X_DUV0), uz(tz[0])), (ux(XK), uz(tz[0]))], fill=RED, width=3)
    txt(ux(2570), uz(tz[1] + 16), "tünel ön duvarı %s" % sayi(tz[1]), f7, RED, "lm")
    txt(ux(2575), uz(tz[0] - 15), "tünel arka duvarı %s" % sayi(tz[0]), f7, RED, "lm")
    txt(ux((gb[0] + gb[1]) / 2), uz(-250), "giriş bandı", f7, INK, "mm")                         # disk ekseninin (−170) altında
    txt(ux(2634), uz(-360), "fırın bandı %s · eksen %s" % (sayi(FT.BANT_W), sayi((bz[0] + bz[1]) / 2)), f7, INK, "mm")
    olcu_v(ux(2685), uz(FT.ZS), uz(0), sayi(FT.ZS), f7, yon="l")                                 # gövde çıkıntısı
    # TOPPING sağ dış sac + çıkış yarığı (FT.YARIK_V2: dış · açıklık)
    yd, ya = FT.YARIK_V2
    d.rectangle([ux(yd[0]), uz(0), ux(yd[1]), uz(-500)], fill=PASL, outline=INK, width=1)
    d.rectangle([ux(yd[0]), uz(ya[5]), ux(yd[1]), uz(ya[4])], fill=BG, outline=INK, width=1)
    txt(ux(2488), uz(ya[4]), "çıkış yarığı %s…%s" % (sayi(ya[4]), sayi(ya[5])), f7, INK, "rm")
    # tabla diski + pide başlangıç / bitiş
    cx, cz = IT.C0; r = R_DISK
    d.ellipse([ux(cx - r), uz(cz + r), ux(cx + r), uz(cz - r)], fill=(238, 240, 244), outline=INK, width=2)
    rp = IT.R_PIDE
    d.ellipse([ux(cx - rp), uz(cz + rp), ux(cx + rp), uz(cz - rp)], fill=URUN, outline=INK, width=2)
    eksen((ux(cx - 190), uz(cz)), (ux(cx + 190), uz(cz)), GRAY); eksen((ux(cx), uz(cz + 190)), (ux(cx), uz(cz - 190)), GRAY)
    ex, ez = IT.C1
    for i in range(0, 360, 12):
        a0, a1 = math.radians(i), math.radians(i + 6)
        d.line([(ux(ex + rp * math.cos(a0)), uz(ez + rp * math.sin(a0))), (ux(ex + rp * math.cos(a1)), uz(ez + rp * math.sin(a1)))], fill=TURUNCU, width=2)
    d.line([(ux(cx), uz(cz)), (ux(ex), uz(ez))], fill=RED, width=4)
    # iniş boruları + sensör (IT.kontrol_hepsi konumları)
    for k, ad in (("BORU_KASAR", "kaşar iniş borusu"), ("BORU_SUCUK", "sucuk iniş borusu")):
        _, bx, bz_, br, _, _ = ENGEL[k]
        d.ellipse([ux(bx - br), uz(bz_ + br), ux(bx + br), uz(bz_ - br)], fill=BG, outline=GRAY, width=2)
    _, bx, bz_, br, _, _ = ENGEL["BORU_KASAR"]; txt(ux(bx), uz(bz_ + br + 15), "kaşar iniş borusu", f7, GRAY, "mm")
    _, bx, bz_, br, _, _ = ENGEL["BORU_SUCUK"]; txt(ux(bx + br - 6), uz(bz_ + br + 13), "sucuk iniş borusu", f7, GRAY, "rm")
    sn = ENGEL["SENSOR"]
    d.rectangle([ux(sn[1]), uz(sn[6]), ux(sn[2]), uz(sn[5])], fill=BG, outline=GRAY, width=1)
    d.line([(ux(sn[2]), uz(sn[6])), (ux(2378), uz(-151))], fill=GRAY, width=1)
    txt(ux(2380), uz(-150), "tabla boş sensörü", f7, GRAY, "lm")
    # itici: kiriş, gövde (yerel zarf), tabla + braket evde, çubuk kalkık (ev) ve inik (son)
    lokal_kutu(zarf(EV, "montaj_kirisi"), SOFT, LINE, 2)
    lokal_kutu(zarf(EV, "my1b16_govde"), (214, 224, 236), INK, 2)
    lokal_kutu(zarf(EV, "pim_braketi"), SOFT, LINE, 1)
    lokal_kutu(zarf(EV, "kizak_tablasi"), (200, 210, 224), INK, 2)
    for P in KOL_UST: d.polygon([(ux(dn(u, v)[0]), uz(dn(u, v)[1])) for u, v in P], fill=None, outline=ACC, width=2)
    lokal_kutu(zarf(SON, "kizak_tablasi"), None, INK, 1, dash=True)
    lokal_kutu(zarf(SON, "kol_link_cubuk"), None, ACC, 2, dash=True)
    px_, pz_ = dn(IT.PIM_KALDIRMA_S, WA + IT.MAKARA["w"])
    d.ellipse([ux(px_ - 4), uz(pz_ + 4), ux(px_ + 4), uz(pz_ - 4)], fill=RED, outline=INK, width=1)
    txt(ux(2136), uz(pz_), "kaldırma pimi Ø8", f7, RED, "rm")
    # ölçüler
    olcu_h(ux(cx), ux(ex), uz(100), "itme %s · düz" % sayi(ex - cx)); olcu_h(ux(FT.X_F0), ux(FT.BANT_X[0]), uz(-560), sayi(FT.BANT_X[0] - FT.X_F0))
    olcu_v(ux(1992), uz(0), uz(cz), sayi(-cz), yon="r"); olcu_v(ux(1972), uz(cz + r), uz(cz - r), "Ø%s" % sayi(2 * r), yon="l")
    txt(ux(cx), uz(34), "disk merkezi (%s · %s)" % (sayi(cx), sayi(cz)), f7, INK, "mm")
    txt(ux(2488), uz(-352), "pide sonu (%s · %s)" % (sayi(ex), sayi(ez)), f7, TURUNCU, "rm")
    p0 = dn(0, WA)
    txt(ux(1975), uz(-450), "SMC MY1B16-250 · gövde %s × %s × %s · y %s–%s · eksen z %s" % (sayi(S1 - S0), sayi(IT.MY["NW"]), sayi(IT.MY["NE"]), sayi(Y_GOV0), sayi(Y_GOV1), sayi(p0[1])), f7, INK, "lm")
    txt(ux(1975), uz(-472), "gövdenin en yakın komşulara boşluğu: kaşar iniş borusu %s · sucuk iniş borusu %s · tabla boş sensörü %s"
        % (sayi(BOSLUK["BORU_KASAR"]), sayi(BOSLUK["BORU_SUCUK"]), sayi(BOSLUK["SENSOR"])), f7, INK, "lm")
    eksen((ux(1960), uz(IT.KORIDOR_Z[1])), (ux(2500), uz(IT.KORIDOR_Z[1])), RED); eksen((ux(1960), uz(IT.KORIDOR_Z[0])), (ux(2500), uz(IT.KORIDOR_Z[0])), RED)
    txt(ux(2000), uz(IT.KORIDOR_Z[1] + 12), "pide koridoru z %s…%s · y %s altı boş" % (sayi(IT.KORIDOR_Z[1]), sayi(IT.KORIDOR_Z[0]), sayi(YS)), f7, RED, "lm")


def yan():
    txt(kx(-190), TIT_Y, "YAN KESİT · s – y · evde kalkık (dolu) · sonda inik (kesik)", f16, ACC)
    d.line([(kx(SL0), ky(T)), (kx(SL1), ky(T))], fill=INK, width=3); txt(kx(-185), ky(T) - 16, "soğuk oda tabanı %s" % sayi(T), f7, INK, "lm")
    d.line([(kx(SL0), ky(DU)), (kx(SL1), ky(DU))], fill=GRAY, width=2); txt(kx(-185), ky(DU) + 16, "disk üstü %s" % sayi(DU), f7, GRAY, "lm")
    eksen((kx(SL0), ky(YS)), (kx(SL1), ky(YS)), RED); txt(kx(240), ky(YS) - 14, "koridor çizgisi %s" % sayi(YS), f7, RED, "lm")
    d.rectangle([kx(0), ky(PU), kx(2 * IT.R_PIDE), ky(DU)], fill=URUN, outline=INK, width=2)
    txt(kx(90), ky((DU + PU) / 2), "pide Ø%s × %s (başlangıç)" % (sayi(2 * IT.R_PIDE), sayi(PU - DU)), f8, INK, "mm")
    d.line([(kx(0), ky(TU)), (kx(2 * IT.R_PIDE), ky(TU))], fill=TURUNCU, width=1); txt(kx(2 * IT.R_PIDE + 4), ky(TU), "topping %s" % sayi(TU), f7, TURUNCU, "lm")
    for ad, fill, ol in (("montaj_kirisi", SOFT, LINE), ("my1b16_govde", (214, 224, 236), INK), ("pim_braketi", SOFT, LINE), ("kizak_tablasi", (200, 210, 224), INK),
                         ("pivot_braketi", PASL, INK)):
        b = zarf(EV, ad); d.rectangle([kx(b.xmin), ky(b.ymax), kx(b.xmax), ky(b.ymin)], fill=fill, outline=ol, width=2)
    for P in PIM_YAN: d.polygon([(kx(u), ky(v)) for u, v in P], fill=(240, 200, 200), outline=RED, width=2)
    for P in KOL_YAN: d.polygon([(kx(u), ky(v)) for u, v in P], fill=(210, 226, 255), outline=ACC, width=2)
    b = zarf(EV, "kol_makarasi"); d.ellipse([kx(b.xmin), ky(b.ymax), kx(b.xmax), ky(b.ymin)], fill=BG, outline=INK, width=2)
    for ad in ("kizak_tablasi", "pivot_braketi", "kol_link_cubuk"):
        b = zarf(SON, ad); drect(kx(b.xmin), ky(b.ymax), kx(b.xmax), ky(b.ymin), ACC if ad.startswith("kol") else INK, 1)
    b = zarf(INIK, "kol_link_cubuk"); drect(kx(b.xmin), ky(b.ymax), kx(b.xmax), ky(b.ymin), GRAY, 1)
    pv = zarf(EV, "pivot_pimi"); d.ellipse([kx(pv.xmin), ky(pv.ymax), kx(pv.xmax), ky(pv.ymin)], fill=INK)
    # ölçüler
    zincir = (T, Y_GOV1, Y_GOV0, IT.Y_TABLA_YUZ, YS, IT.BAR_Y0)
    for a_, b_ in zip(zincir[:-1], zincir[1:]):
        dy = 6.0 if (a_ - b_) * KS < 20 else 0.0                                              # kısa ölçünün yazısı üst çizgiye değmesin
        d.line([(kx(-160), ky(a_)), (kx(-160), ky(b_))], fill=INK, width=2)
        for yy in (ky(a_), ky(b_)): d.line([(kx(-160) - 8, yy), (kx(-160) + 8, yy)], fill=INK, width=2)
        txt(kx(-160) - 10, (ky(a_) + ky(b_)) / 2 + dy, sayi(a_ - b_), f9, INK, "rm")
    olcu_h_kisa(kx(IT.S_HOME), kx(IT.S_TEMAS), ky(DU - 18), sayi(IT.S_TEMAS - IT.S_HOME)); olcu_h(kx(IT.S_TEMAS), kx(0), ky(DU - 18), sayi(-IT.S_TEMAS))
    olcu_h(kx(0), kx(IT.S_END), ky(DU - 28), "%s (itme %s + %s)" % (sayi(IT.S_END), sayi(IT.L_ITME), sayi(IT.S_END - IT.L_ITME)))
    olcu_h(kx(S0), kx(S1), ky(T + 25), "gövde %s = strok %s + %s" % (sayi(S1 - S0), sayi(IT.STROK), sayi(IT.MY["Z"])))
    txt(kx(IT.S_END), ky(DU - 28) + 26, "çubuk yüzü sonda", f7, ACC, "mm"); txt(kx(IT.S_HOME), ky(DU - 28) + 26, "ev %s" % sayi(IT.S_HOME), f7, INK, "mm")
    txt(kx(IT.PIM_KALDIRMA_S), ky(T) - 18, "kaldırma pimi Ø8 · altı %s" % sayi(YS), f7, RED, "mm")
    txt(kx(IT.S_HOME + 20.5), ky(YS - 7), "makara Ø%s" % sayi(2 * IT.MAKARA["r"]), f7, INK, "mm")
    txt(kx(IT.S_HOME + 60), ky(IT.PIVOT_Y), "çubuk kalkık · y %s–%s" % (sayi(KALKIK_Y[0]), sayi(KALKIK_Y[1])), f7, ACC, "lm")


def on():
    txt(ox(WL0), TIT_Y, "ÖN GÖRÜNÜŞ · w – y · çubuk inik", f16, ACC)
    d.line([(ox(WL0), oy(T)), (ox(WL1), oy(T))], fill=INK, width=3)
    d.line([(ox(WL0), oy(DU)), (ox(WL1), oy(DU))], fill=GRAY, width=2)
    eksen((ox(WL0), oy(YS)), (ox(WL1), oy(YS)), RED)
    d.rectangle([ox(WL0), oy(PU), ox(WL1), oy(DU)], fill=URUN, outline=None)
    for ad, fill, ol in (("montaj_kirisi", SOFT, LINE), ("my1b16_govde", (214, 224, 236), INK), ("pim_braketi", SOFT, LINE), ("kizak_tablasi", (200, 210, 224), INK),
                         ("pivot_braketi", PASL, INK)):
        b = zarf(INIK, ad); d.rectangle([ox(b.zmin), oy(b.ymax), ox(b.zmax), oy(b.ymin)], fill=fill, outline=ol, width=2)
    for P in PIM_ON: d.polygon([(ox(u), oy(v)) for u, v in P], fill=(240, 200, 200), outline=RED, width=2)
    for P in KOL_ON: d.polygon([(ox(u), oy(v)) for u, v in P], fill=(210, 226, 255), outline=ACC, width=2)
    for ad, fill, ol in (("kol_burcu", (240, 240, 232), INK), ("kol_makarasi", BG, INK)):
        b = zarf(INIK, ad); d.rectangle([ox(b.zmin), oy(b.ymax), ox(b.zmax), oy(b.ymin)], fill=fill, outline=ol, width=1 if ad == "kol_burcu" else 2)
    pv = zarf(INIK, "pivot_pimi"); d.line([(ox(pv.zmin), oy(IT.PIVOT_Y)), (ox(pv.zmax), oy(IT.PIVOT_Y))], fill=INK, width=4)
    olcu_h(ox(IT.BAR_W0), ox(IT.BAR_W1), oy(DU - 18), sayi(IT.BAR_W1 - IT.BAR_W0)); olcu_h(ox(WA - IT.MY["NW"] / 2.0), ox(WA + IT.MY["NW"] / 2.0), oy(T + 25), sayi(IT.MY["NW"]))
    olcu_v(ox(86), oy(IT.BAR_Y1), oy(IT.BAR_Y0), sayi(IT.BAR_Y1 - IT.BAR_Y0), yon="r"); olcu_v(ox(86), oy(IT.PIVOT_Y + 4.0), oy(IT.BAR_Y1), sayi(IT.PIVOT_Y + 4.0 - IT.BAR_Y1), yon="r")
    txt(ox(WA), oy((Y_GOV0 + Y_GOV1) / 2), "MY1B16", f7, INK, "mm")
    txt(ox(pv.zmax + 5), oy(IT.PIVOT_Y), "pivot Ø4 · %s" % sayi(IT.PIVOT_Y), f7, INK, "lm")
    txt(ox((IT.BAR_W0 + IT.BAR_W1) / 2), oy((IT.BAR_Y0 + IT.BAR_Y1) / 2), "çubuk %s × %s × 3 · altı %s" % (sayi(IT.BAR_W1 - IT.BAR_W0), sayi(IT.BAR_Y1 - IT.BAR_Y0), sayi(IT.BAR_Y0)), f7, INK, "mm")


def liste():
    x0, y0 = LX0, LY0
    txt(x0, y0 - 38, "PARÇA LİSTESİ (itici_cad_v4 · BOM)", f16, ACC)
    IT.kur(IT.S_HOME, True)
    satir = []; n = 1
    DUZELT = {"kol_link_cubuk": ("kalkınca y %.0f–%.0f aralığında" % (IT.PIVOT_Y - 2.0, IT.PIVOT_Y + 2.0),               # modül metni PIVOT_Y ± 2 (yanlış)
                                 "kalkınca y %s–%s aralığında" % (sayi(KALKIK_Y[0]), sayi(KALKIK_Y[1]))),               # katıdan ölçülen (yan kesitteki yazıyla aynı)
              "kaldirma_pimi": ("(pide üstü %.0f)" % IT.TOP_UST, "(topping üstü %s)" % sayi(IT.TOP_UST))}               # TOP_UST = topping üstü (pide üstü PIDE_UST)
    for p in IT.PARCALAR:
        if not p["bom"]: continue
        ad_, adet, kay, not_ = p["bom"]
        if p["ad"] in DUZELT:
            eski, yeni = DUZELT[p["ad"]]; assert eski in not_, (p["ad"], not_)
            not_ = not_.replace(eski, yeni)
        satir.append((str(n), ad_, str(adet), kay, not_)); n += 1
    kol = (0, 40, 620, 680, 1200)
    gen = 3050.0
    d.rectangle([x0, y0, x0 + gen, y0 + 28], fill=SOFT, outline=LINE, width=1)
    for k, b in zip(kol, ("NO", "PARÇA", "ADET", "KAYNAK / MALZEME", "NOT")):
        txt(x0 + k + 8, y0 + 14, b, f7, INK, "lm")
    y = y0 + 28
    for r in satir:
        d.line([(x0, y + 26), (x0 + gen, y + 26)], fill=(225, 225, 230), width=1)
        for k, v in zip(kol, r):
            lim = 62 if k == 40 else (56 if k == 680 else (150 if k == 1200 else 12))
            v = v if len(v) <= lim else v[:lim - 1] + "…"
            txt(x0 + k + 8, y + 13, v, f7, INK if k < 1200 else GRAY, "lm")
        y += 26
    d.rectangle([x0, y0, x0 + gen, y], outline=LINE, width=1)
    y += 40
    txt(x0, y, "AÇIK", f16, RED); y += 50
    for i, s_ in enumerate(("çubuğun pide kenarına basınç dağılımı (30 mm yüzey) — pilot",
                            "SMC MY1B16 STEP'i (föy ölçüleriyle kutu model)", "kaldırma pimi – POM makara aşınması — pilot"), 1):
        MUAF[0] = True; isaret(x0 + 15, y, i); MUAF[0] = False
        txt(x0 + 40, y, s_, f7, INK, "lm"); y += 32


def baslik():
    txt(150, 40, "AUTOKITCH  ·  AKTARMA İTİCİSİ  ·  TOPPING diskinden fırın giriş bandına · DÜZ · ALÇAK HAT  ·  TEKNİK RESİM %s" % SURUM, f30, INK)
    txt(150, 98, "3B model itici_cad_v4 (tek kaynak) · ALÇAK HAT: disk üstü %s (önce 1168) · SMC MY1B16-250 x boyunca DÜZ (θ %s°) · itme %s (+%s x · %s z) · pivotlu çubuk %s × %s, sabit pimle 90° kalkar · ana montaj v57 · ölçüler mm · 27 Eylül 2026"
        % (sayi(DU), sayi(abs(IT.THETA)), sayi(IT.L_ITME), sayi(IT.C1[0] - IT.C0[0]), sayi(IT.C1[1] - IT.C0[1]), sayi(IT.BAR_W1 - IT.BAR_W0), sayi(IT.BAR_Y1 - IT.BAR_Y0)), f11, GRAY)
    d.line([(150, 126), (W_PX - 60, 126)], fill=LINE, width=3)


# ============================== ÇAKIŞMA DENETİMİ ==============================
CIZGI_RENK = {INK, GRAY, LINE, RED, ACC, TURUNCU, KOMSU}


def _kutu(x, y, s, f, a):
    x0, y0, x1, y1 = d.d.textbbox((x * K_HD, y * K_HD), s, font=d._f(f), anchor=a)
    return (x0 / K_HD, y0 / K_HD, x1 / K_HD, y1 / K_HD)


def cakisma():
    """yazı ↔ yazı (kutular kesişiyor) ve yazı ↔ çizgi (yazı kutusunun içinde, yazılardan önce çizilmiş çizgi pikseli) · sayfa dışı"""
    kutular = [(_kutu(x, y, s, f, a), s, muaf) for (x, y, s, f, c, a, muaf) in YAZI]
    sorun = []
    for i in range(len(kutular)):
        (a0, b0, a1, b1), s_, m = kutular[i]
        if a0 < 0 or b0 < 0 or a1 > W_PX or b1 > H_PX: sorun.append(("sayfa dışı", s_, ""))
        for j in range(i + 1, len(kutular)):
            (c0, d0, c1, d1), t_, _ = kutular[j]
            if a0 < c1 - 1 and c0 < a1 - 1 and b0 < d1 - 1 and d0 < b1 - 1:
                sorun.append(("yazı ↔ yazı", s_, t_))
        if m: continue
        X0, Y0, X1, Y1 = [int(round(v * K_HD)) for v in (a0 + 1, b0 + 1, a1 - 1, b1 - 1)]
        bol = im.crop((X0, Y0, max(X0 + 1, X1), max(Y0 + 1, Y1)))
        n = sum(c for c, px in (bol.getcolors(1 << 22) or []) if px in CIZGI_RENK)
        if n: sorun.append(("yazı ↔ çizgi (%d px)" % n, s_, ""))
    return sorun


def ciz():
    global im, d
    im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)
    baslik(); ust(); yan(); on(); liste()
    sorun = cakisma()                                        # yazılar çizilmeden önce: altlarında çizgi var mı
    for (x, y, s, f, c, a, m) in YAZI:
        d.text((x, y), s, font=f, fill=c, anchor=a)
    os.makedirs(KLASOR, exist_ok=True)
    yol = os.path.join(KLASOR, "ITICI_%s_teknik.png" % SURUM)
    im.save(yol, dpi=(int(150 * K_HD), int(150 * K_HD)))
    im.save(yol.replace(".png", ".pdf"), "PDF", resolution=150.0 * K_HD)
    im2 = im.resize((int(W_PX * 0.6), int(H_PX * 0.6)), Image.LANCZOS)
    im2.save(os.path.join(U, "..", "..", "otonom", "hat", "img", "ITICI_%s_teknik.png" % SURUM), optimize=True)
    print("yazildi:", yol, im.size)
    print("ölçülen: gövde ↔ kaşar borusu %.2f · ↔ sucuk borusu %.2f · ↔ sensör %.2f · kalkık çubuk y %.2f…%.2f"
          % (BOSLUK["BORU_KASAR"], BOSLUK["BORU_SUCUK"], BOSLUK["SENSOR"], KALKIK_Y[0], KALKIK_Y[1]))
    print("ÇAKIŞMA: %d" % len(sorun))
    for s_ in sorun: print("   ", s_)
    return yol


if __name__ == "__main__":
    ciz()
    sys.stdout.flush(); os._exit(0)                          # itici_cad_v4 gibi: kapanıştaki OCC erişim ihlalini atla
