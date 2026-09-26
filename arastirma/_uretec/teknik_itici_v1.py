# -*- coding: utf-8 -*-
"""AUTOKITCH · AKTARMA İTİCİSİ · TEKNİK RESİM v1 (26 Eyl 2026 gece)
Ölçüler 3B modelden (itici_cad_v1 · tek kaynak). Kural: paftada yalnız görünüş + ölçü + parça adı; açıklama mesajda.
Çizim yardımcıları teknik_firin_tp10_v3.py'den (aynı sayfa düzeni)."""
import io, math, os, sys
U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
_yrd = io.open(os.path.join(U, "teknik_firin_tp10_v3.py"), encoding="utf-8").read().split("# ============================== VERİ")[0]
exec(compile(_yrd, "teknik_yardimci", "exec"))
import itici_cad_v1 as IT

# ============================== VERİ (TEK KAYNAK: itici_cad_v1) ==============================
IT.yerel = lambda wp: wp                          # parçaları YEREL (s, y, w) çerçevede kur: kutu zarfları buradan
IT.kur(IT.S_HOME, True); EV = [(p["ad"], p["wp"].val().BoundingBox(), p) for p in IT.PARCALAR]
IT.kur(IT.S_END, False); SON = [(p["ad"], p["wp"].val().BoundingBox()) for p in IT.PARCALAR]
IT.kur(IT.S_HOME, False); INIK = [(p["ad"], p["wp"].val().BoundingBox()) for p in IT.PARCALAR]
def zarf(L, ad): return [b for a, b, *_ in L if a == ad][0]
def dn(s_, w_):  # yerel (s, w) → dünya (x, z)
    return (IT.PC[0] + s_ * IT.U[0] + w_ * IT.W[0], IT.PC[1] + s_ * IT.U[1] + w_ * IT.W[1])
S0 = IT.S_STROK0 - IT.MY["Z"] / 2.0; S1 = IT.S_STROK0 + IT.STROK + IT.MY["Z"] / 2.0
WA = IT.W_AXIS

# ============================== YERLEŞİM ==============================
# üst görünüş (x–z): sol üst · yan kesit (s–y): sağ üst · ön görünüş (w–y): sağ orta · liste: alt
UX0, UY0, US = 150.0, 260.0, 1.55                      # x 1960 → px 150 ; z 0 → py UY0
def ux(x): return UX0 + (x - 1960.0) * US
def uz(z): return UY0 + (-z) * US
KX0, KY0, KS = 1360.0, 300.0, 2.6                      # s −190 → px 1360 ; y 1290 → py KY0
def kx(s_): return KX0 + (s_ + 190.0) * KS
def ky(y): return KY0 + (1290.0 - y) * KS
OX0, OY0, OS = 2620.0, 300.0, 2.6                      # w −125 → px 2620
def ox(w_): return OX0 + (w_ + 125.0) * OS
def oy(y): return OY0 + (1290.0 - y) * OS
LX0, LY0 = 150.0, 1420.0


def rrect(pts, fill=None, outline=INK, w=2):
    d.polygon(pts, fill=fill, outline=outline, width=w)
def lokal_kutu(b, fill, outline=INK, w=2, dash=False):
    """yerel zarf (s, w) → üst görünüşte döndürülmüş dikdörtgen"""
    pts = [ux(dn(s_, w_)[0]) for s_, w_ in ((b.xmin, b.zmin), (b.xmax, b.zmin), (b.xmax, b.zmax), (b.xmin, b.zmax))]
    pz_ = [uz(dn(s_, w_)[1]) for s_, w_ in ((b.xmin, b.zmin), (b.xmax, b.zmin), (b.xmax, b.zmax), (b.xmin, b.zmax))]
    P = list(zip(pts, pz_))
    if dash:
        for i in range(4): dline(P[i], P[(i + 1) % 4], outline, w)
    else:
        rrect(P, fill, outline, w)


def ust():
    txt(ux(1960), UY0 - 60, "ÜST GÖRÜNÜŞ · dünya x–z · tabla aktarma konumunda · itici evde (çubuk kalkık) ve sonda (kesik)", f16, ACC)
    # F ön oda + giriş bandı + fırın bandı başı + tünel duvarları
    d.rectangle([ux(2500), uz(0), ux(2700), uz(-730)], fill=ODA_R, outline=LINE, width=2)
    d.rectangle([ux(2505), uz(-89), ux(2569), uz(-409)], fill=PASL, outline=INK, width=2)
    d.rectangle([ux(2568), uz(-92.5), ux(2700), uz(-473.5)], fill=(236, 236, 240), outline=INK, width=2)
    d.line([(ux(2564), uz(-79)), (ux(2700), uz(-79))], fill=RED, width=3); d.line([(ux(2564), uz(-485)), (ux(2700), uz(-485))], fill=RED, width=3)
    txt(ux(2610), uz(-60), "tünel ön duvarı −79", f7, RED, "lm"); txt(ux(2610), uz(-500), "tünel arka duvarı −485", f7, RED, "lm")
    txt(ux(2537), uz(-249), "giriş bandı", f7, INK, "mm"); txt(ux(2640), uz(-283), "fırın bandı 381 · eksen −283", f7, INK, "mm")
    # TOPPING sağ dış sac + çıkış yarığı + tekne sağ ucu (2500'e kadar)
    d.rectangle([ux(2492), uz(0), ux(2498.5), uz(-830 + 330)], fill=PASL, outline=INK, width=1)
    d.rectangle([ux(2492), uz(-13), ux(2498.5), uz(-417)], fill=BG, outline=INK, width=1)
    txt(ux(2495), uz(-440), "çıkış yarığı −417…−13", f7, INK, "mm")
    # tabla diski + pide başlangıç / bitiş
    cx, cz = IT.C0; r = 170.0
    d.ellipse([ux(cx - r), uz(cz + r), ux(cx + r), uz(cz - r)], fill=(238, 240, 244), outline=INK, width=2)
    d.ellipse([ux(cx - 150), uz(cz + 150), ux(cx + 150), uz(cz - 150)], fill=URUN, outline=INK, width=2)
    eksen((ux(cx - 190), uz(cz)), (ux(cx + 190), uz(cz)), GRAY); eksen((ux(cx), uz(cz + 190)), (ux(cx), uz(cz - 190)), GRAY)
    ex, ez = IT.C1
    for i in range(0, 360, 12):
        a0, a1 = math.radians(i), math.radians(i + 6)
        d.line([(ux(ex + 150 * math.cos(a0)), uz(ez + 150 * math.sin(a0))), (ux(ex + 150 * math.cos(a1)), uz(ez + 150 * math.sin(a1)))], fill=TURUNCU, width=2)
    d.line([(ux(cx), uz(cz)), (ux(ex), uz(ez))], fill=RED, width=4)
    txt(ux((cx + ex) / 2) - 20, uz((cz + ez) / 2) - 26, "itme %s · %s°" % (sayi(IT.L_ITME), sayi(IT.THETA)), f9, RED, "mm")
    # destek plakası
    d.rectangle([ux(2200), uz(-345), ux(2490), uz(-420)], fill=PASL, outline=INK, width=2); txt(ux(2345), uz(-382), "destek plakası · üstü 1167 · 2 mm 304", f7, INK, "mm")
    # iniş boruları + sensör
    for (bx, bz, br, ad) in ((2061, -150, 25, "kaşar iniş borusu"), (2310, -150, 24, "sucuk iniş borusu")):
        d.ellipse([ux(bx - br), uz(bz + br), ux(bx + br), uz(bz - br)], fill=BG, outline=GRAY, width=2); txt(ux(bx), uz(bz + 40), ad, f7, GRAY, "mm")
    d.rectangle([ux(2341), uz(-161), ux(2359), uz(-179)], fill=BG, outline=GRAY, width=1); txt(ux(2350), uz(-195), "tabla boş sensörü", f7, GRAY, "mm")
    # itici: kiriş, gövde (yerel zarf döndürülmüş), tabla + braket evde, çubuk kalkık (ev) ve inik (son)
    lokal_kutu(zarf(EV, "montaj_kirisi"), SOFT, LINE, 2)
    lokal_kutu(zarf(EV, "my1b16_govde"), (214, 224, 236), INK, 2)
    lokal_kutu(zarf(EV, "pim_braketi"), SOFT, LINE, 1)
    lokal_kutu(zarf(EV, "kizak_tablasi"), (200, 210, 224), INK, 2)
    lokal_kutu(zarf(EV, "kol_link_cubuk"), None, ACC, 2)
    lokal_kutu(zarf(SON, "kizak_tablasi"), None, INK, 1, dash=True)
    lokal_kutu(zarf(SON, "kol_link_cubuk"), None, ACC, 2, dash=True)
    px_, pz_ = dn(IT.PIM_KALDIRMA_S, WA + IT.MAKARA["w"])
    d.ellipse([ux(px_ - 4), uz(pz_ + 4), ux(px_ + 4), uz(pz_ - 4)], fill=RED, outline=INK, width=1)
    txt(ux(px_) + 12, uz(pz_) - 14, "kaldırma pimi Ø8", f7, RED, "lm")
    # ölçüler
    olcu_h(ux(cx), ux(ex), uz(60), sayi(ex - cx)); olcu_v(ux(2560), uz(cz), uz(ez), sayi(cz - ez), yon="r")
    olcu_h(ux(2200), ux(2490), uz(-450), "290"); olcu_h(ux(2500), ux(2568), uz(-560), "68")
    olcu_v(ux(1990), uz(0), uz(cz), "170", yon="l"); olcu_v(ux(1990), uz(cz), uz(-340), "Ø340", yon="l")
    txt(ux(cx - 60), uz(cz + 60), "disk merkezi (%s · %s)" % (sayi(cx), sayi(cz)), f7, INK, "mm")
    txt(ux(ex), uz(ez + 175), "pide sonu (%s · %s)" % (sayi(ex), sayi(ez)), f7, TURUNCU, "mm")
    b = zarf(EV, "my1b16_govde"); p0, p1 = dn(b.xmin, WA), dn(b.xmax, WA)
    txt(ux(1960), uz(-540), "SMC MY1B16-250 · gövde %s (mavi, tabanın altında 1243–1271) · ekseni çubuk çizgisinin %s gerisinde, iniş borularının arasından" % (sayi(S1 - S0), sayi(-WA)), f7, INK, "lm")
    eksen((ux(1960), uz(-20)), (ux(2500), uz(-20)), RED); eksen((ux(1960), uz(-320)), (ux(2500), uz(-320)), RED)
    txt(ux(1975), uz(-8), "pide geliş koridoru z −20…−320 · üstünde 1210'a kadar boş", f7, RED, "lm")


def yan():
    txt(kx(-190), KY0 - 60, "YAN KESİT · itme doğrultusu s – y · evde kalkık (dolu) · sonda inik (kesik)", f16, ACC)
    d.line([(kx(-190), ky(1277)), (kx(330), ky(1277))], fill=INK, width=3); txt(kx(-185), ky(1277) - 16, "soğuk oda tabanı 1277", f7, INK, "lm")
    d.line([(kx(-190), ky(1168)), (kx(330), ky(1168))], fill=GRAY, width=2); txt(kx(-185), ky(1168) + 16, "disk üstü 1168", f7, GRAY, "lm")
    eksen((kx(-190), ky(1210)), (kx(330), ky(1210)), RED); txt(kx(240), ky(1210) - 14, "koridor çizgisi 1210", f7, RED, "lm")
    d.rectangle([kx(0), ky(1196), kx(300), ky(1168)], fill=URUN, outline=INK, width=2); txt(kx(150), ky(1182), "pide Ø300 × 28 (başlangıç)", f8, INK, "mm")
    d.line([(kx(0), ky(1201)), (kx(300), ky(1201))], fill=TURUNCU, width=1); txt(kx(305), ky(1201), "topping 1201", f7, TURUNCU, "lm")
    for ad, fill, ol in (("montaj_kirisi", SOFT, LINE), ("my1b16_govde", (214, 224, 236), INK), ("pim_braketi", SOFT, LINE), ("kizak_tablasi", (200, 210, 224), INK),
                         ("pivot_braketi", PASL, INK), ("kaldirma_pimi", (240, 200, 200), RED)):
        b = zarf(EV, ad); d.rectangle([kx(b.xmin), ky(b.ymax), kx(b.xmax), ky(b.ymin)], fill=fill, outline=ol, width=2)
    b = zarf(EV, "kol_link_cubuk"); d.rectangle([kx(b.xmin), ky(b.ymax), kx(b.xmax), ky(b.ymin)], fill=(210, 226, 255), outline=ACC, width=2)
    b = zarf(EV, "kol_makarasi"); d.ellipse([kx(b.xmin), ky(b.ymax), kx(b.xmax), ky(b.ymin)], fill=BG, outline=INK, width=2)
    for ad in ("kizak_tablasi", "pivot_braketi", "kol_link_cubuk"):
        b = zarf(SON, ad); drect(kx(b.xmin), ky(b.ymax), kx(b.xmax), ky(b.ymin), ACC if ad.startswith("kol") else INK, 1)
    b = zarf(INIK, "kol_link_cubuk"); drect(kx(b.xmin), ky(b.ymax), kx(b.xmax), ky(b.ymin), GRAY, 1)
    txt(kx(IT.S_HOME - 3), ky(1232) - 30, "pivot 1224", f7, INK, "mm")
    pv = zarf(EV, "pivot_pimi"); d.ellipse([kx(pv.xmin), ky(pv.ymax), kx(pv.xmax), ky(pv.ymin)], fill=INK)
    # ölçüler
    olcu_v(kx(-160), ky(1277), ky(1271), "6", yon="l"); olcu_v(kx(-160), ky(1271), ky(1243.2), "27,8", yon="l"); olcu_v(kx(-160), ky(1243.2), ky(1234), "9,2", yon="l")
    olcu_v(kx(-160), ky(1234), ky(1210), "24", yon="l"); olcu_v(kx(-160), ky(1210), ky(1170), "40", yon="l")
    olcu_h(kx(IT.S_HOME), kx(IT.S_TEMAS), ky(1150), sayi(IT.S_TEMAS - IT.S_HOME)); olcu_h(kx(IT.S_TEMAS), kx(0), ky(1150), "20")
    olcu_h(kx(0), kx(IT.S_END), ky(1140), "%s (itme %s + 15)" % (sayi(IT.S_END), sayi(IT.L_ITME)))
    olcu_h(kx(S0), kx(S1), ky(1300), "gövde %s = strok 250 + 160" % sayi(S1 - S0))
    txt(kx(IT.S_END), ky(1160) + 60, "çubuk yüzü sonda", f7, ACC, "mm"); txt(kx(IT.S_HOME), ky(1160) + 60, "ev −37,5", f7, INK, "mm")
    txt(kx(IT.PIM_KALDIRMA_S), ky(1271) - 18, "kaldırma pimi Ø8 · 1210'a iner", f7, RED, "mm")
    txt(kx(60), ky(1226), "çubuk kalkık 1222–1226", f7, ACC, "lm")


def on():
    txt(ox(-125), OY0 - 60, "ÖN GÖRÜNÜŞ · itme yönünden (w – y) · evde, çubuk inik", f16, ACC)
    d.line([(ox(-125), oy(1277)), (ox(100), oy(1277))], fill=INK, width=3)
    d.line([(ox(-125), oy(1168)), (ox(100), oy(1168))], fill=GRAY, width=2)
    eksen((ox(-125), oy(1210)), (ox(100), oy(1210)), RED)
    d.rectangle([ox(-125), oy(1196), ox(100), oy(1168)], fill=URUN, outline=None)
    for ad, fill, ol in (("montaj_kirisi", SOFT, LINE), ("my1b16_govde", (214, 224, 236), INK), ("pim_braketi", SOFT, LINE), ("kizak_tablasi", (200, 210, 224), INK),
                         ("pivot_braketi", PASL, INK), ("kaldirma_pimi", (240, 200, 200), RED), ("kol_link_cubuk", (210, 226, 255), ACC), ("kol_makarasi", BG, INK)):
        b = zarf(INIK, ad); d.rectangle([ox(b.zmin), oy(b.ymax), ox(b.zmax), oy(b.ymin)], fill=fill, outline=ol, width=2)
    pv = zarf(INIK, "pivot_pimi"); d.line([(ox(pv.zmin), oy(1224)), (ox(pv.zmax), oy(1224))], fill=INK, width=4)
    b = zarf(INIK, "kol_link_cubuk")
    olcu_h(ox(IT.BAR_W0), ox(IT.BAR_W1), oy(1150), "%s" % sayi(IT.BAR_W1 - IT.BAR_W0)); olcu_h(ox(WA - 18.5), ox(WA + 18.5), oy(1300), "37")
    olcu_v(ox(90), oy(1200), oy(1170), "30", yon="r"); olcu_v(ox(90), oy(1228), oy(1200), "28", yon="r")
    txt(ox(WA), oy(1258), "MY1B16", f7, INK, "mm"); txt(ox(WA + IT.MAKARA["w"]), oy(1205), "makara Ø8 · pim Ø8", f7, RED, "mm")
    txt(ox(-5), oy(1185), "çubuk 170 × 30 × 3 · altı 1170", f7, INK, "mm")


def liste():
    x0, y0 = LX0, LY0
    txt(x0, y0 - 38, "PARÇA LİSTESİ (itici_cad_v1 · BOM)", f16, ACC)
    IT.kur(IT.S_HOME, True)
    satir = []; n = 1
    for p in IT.PARCALAR:
        if not p["bom"]: continue
        ad_, adet, kay, not_ = p["bom"]
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
    txt(x0, y, "AÇIK", f16, RED); y += 34
    for i, s_ in enumerate(("çubuğun pide kenarına basınç dağılımı (30 mm yüzey) — pilot", "destek plakası sürtünmesi (PTFE kaplama seçeneği) — pilot",
                            "SMC MY1B16 STEP'i (föy ölçüleriyle kutu model)", "kaldırma pimi – POM makara aşınması — pilot"), 1):
        isaret(x0 + 15, y, i); txt(x0 + 40, y, s_, f7, INK, "lm"); y += 32


def baslik():
    txt(150, 40, "AUTOKITCH  ·  AKTARMA İTİCİSİ  ·  TOPPING diskinden fırın giriş bandına  ·  TEKNİK RESİM v1", f30, INK)
    txt(150, 98, "3B model itici_cad_v1 (tek kaynak) · SMC MY1B16-250 çapraz %s° · itme %s (+%s x · %s z) · pivotlu çubuk 170 × 30, sabit pimle 90° kalkar · destek plakası y 1167 · ana montaj v49 · ölçüler mm"
        % (sayi(IT.THETA), sayi(IT.L_ITME), sayi(IT.C1[0] - IT.C0[0]), sayi(IT.C1[1] - IT.C0[1])), f11, GRAY)
    d.line([(150, 126), (W_PX - 60, 126)], fill=LINE, width=3)


def ciz():
    global im, d
    im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)
    baslik(); ust(); yan(); on(); liste()
    os.makedirs(KLASOR, exist_ok=True)
    yol = os.path.join(KLASOR, "ITICI_v1_teknik.png")
    im.save(yol, dpi=(int(150 * K_HD), int(150 * K_HD)))
    im.save(yol.replace(".png", ".pdf"), "PDF", resolution=150.0 * K_HD)
    im2 = im.resize((int(W_PX * 0.6), int(H_PX * 0.6)), Image.LANCZOS)
    im2.save(os.path.join(U, "..", "..", "otonom", "hat", "img", "ITICI_v1_teknik.png"), optimize=True)
    print("yazildi:", yol, im.size)
    return yol


if __name__ == "__main__":
    ciz()
