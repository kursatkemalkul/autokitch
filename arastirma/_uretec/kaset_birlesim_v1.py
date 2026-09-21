# -*- coding: utf-8 -*-
"""AUTOKITCH · KASET BİRLEŞİM DETAYLARI v1 (22 Eyl 2026) — DÖRT KASETE AYNI KOD UYGULANIR (kaşar v9 · kıyma v4 · kuşbaşı v3 · küp sucuk v2)
Kemal (AR'da bakıp): "çubuk o plastiğe nasıl takılıyor · metal tutma kolu nasıl takılıyor, içinde ne var · plastik kapak dönüyor kapanıyor ama nasıl,
içinde geçme var mı, nasıl click ediyor — bunlar tüm kasetlerde çözülmemiş, yarın üretime gitsem hep sorun."  → HAKLI. Eski modelde:
  · saplama düz çubuk, somun düz altıgen blok, pul yok            · kulp İKİ dişli ayaklı TEK parça → iki sabit saplamaya vidalanamaz (montaj sırası yanlıştı)
  · bayonette kanal + pim vardı ama KİLİT yoktu (pim 35°'de boşta duruyordu), pim Ø5 baskı, conta yok
  · gövde–plaka arasında conta yok · plaka deliğinden geçen muylularda keçe yok · tüp vidası plastiğe diş
ÇÖZÜM (hepsi burada, tek yerde):
  1 SAPLAMA M6: iki ucu 16 mm diş (modelde oluklu gösterilir), gövdesi düz Ø6 · PUL DIN 125 + KÖR SOMUN DIN 1587 (kubbeli)
  2 KULP: 2 dolu ayak Ø14 (tabanı Ø20 flanş) + Ø10 çubuk TIG kaynak = tek parça · ayakta M6 × 14 KÖR diş. MONTAJ: üst iki saplama ÖNCE kulpa dibe
    kadar vidalanır (saplama döner, kulp değil) → kulp + 2 saplama ÖNDEN geçirilir → arkadan pul + kör somun sıkılır (saplama dipte kilitli, dönmez)
  3 BAYONET: tüpte 3 TIRNAK (8 × 4 × 3,2 · tüple tek parça, arka kenarları 0,5 pahlı) · kapakta 3 L-KANAL: giriş → halka → 0,25 mm TÜMSEK → CEP + dayama.
    Kapağın dibindeki O-ring yay görevi görür: İT (O-ring ezilir) → 35° ÇEVİR → tümseği aşınca BIRAK = KLİK, tırnak cebe oturur. O-ring aynı anda tüp ucunu
    sızdırmaz yapar. Kilitleme yönü = helezonun sürükleme yönü (önden bakınca saat yönü) → çalışırken kapak dayamaya doğru itilir, açılmaz.
  4 CONTALAR: gövde–plaka düz silikon conta (1,5 → 1,0 mm) · muylularda O-ring 18 × 2,5 (2 göbek + ön kovan) · tüp faturasında O-ring · ön plakada M4 insert
VARSAYIM (katalogdan teyit edilecek): O-ring ezilme oranları genel kuraldan (statik yüz ≈ %15–30, dönen mil ≈ %10–12); tümsek kuvveti HESAPLANMADI, denenecek."""
import math
import cadquery as cq

TIRNAK_Z0, TIRNAK_Z1, TIRNAK_GEN, KILIT_ACI = 240.5, 244.5, 8.0, 35.0
Z_HALKA, Z_CEP, Z_TUMSEK, Z_KANAL_UST, KAPAK_BOS = 240.3, 240.5, 240.75, 245.0, 0.25
TIRNAK_ACILARI = (90.0, 210.0, 330.0)


def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def boru(x, y, r0, r1, z0, z1): return cq.Workplane("XY").center(x, y).circle(r1).circle(r0).extrude(z1 - z0).translate((0, 0, z0))
def kut(x0, x1, y0, y1, z0, z1): return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
def torus(x, y, z, R, r):
    """O-ring: SEKİZGEN kesitli halka (gerçek torus web modelini 2600 üçgenle şişiriyordu; sekizgen ≈ 300). Düz yüzleri oturduğu yüzeylere tam değer."""
    c = r / math.cos(math.radians(22.5)); pts = [(R + c * math.cos(math.radians(22.5 + 45.0 * k)), c * math.sin(math.radians(22.5 + 45.0 * k))) for k in range(8)]
    g = cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))          # eksen YEREL koordinatta
    return cq.Workplane(obj=g.val().translate(cq.Vector(x, y, z)))


def sektor(r0, r1, a0, a1, z0, z1):
    """halka dilimi (eksen orijinde, açılar derece) — yaylar 3°'lik kirişlerle; r0/r1 kapak duvarının DIŞINDA kaldığı için kirişler parçada iz bırakmaz"""
    n = max(2, int(math.ceil(abs(a1 - a0) / 3.0)) + 1); A = [math.radians(a0 + (a1 - a0) * i / (n - 1)) for i in range(n)]
    pts = [(r1 * math.cos(a), r1 * math.sin(a)) for a in A] + [(r0 * math.cos(a), r0 * math.sin(a)) for a in reversed(A)]
    return cq.Workplane("XY").polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0))


def _dogrula(yeni, v_bek_min, v_bek_max, ad):
    s = yeni.val(); v = s.Volume()
    assert s.isValid() and v_bek_min <= v <= v_bek_max, "%s: birlesim/kesim bozuk (hacim %.1f, beklenen %.1f–%.1f, gecerli=%s)" % (ad, v, v_bek_min, v_bek_max, s.isValid())
    return yeni


def _islem(a, b, tur, vmin, vmax, ad):
    """OpenCascade boolean'ı sessizce yanlış sonuç verebiliyor → her işlem HACİMLE doğrulanır; clean=True tutmazsa clean=False denenir"""
    son = None
    for clean in (True, False):
        try:
            r = a.union(b, clean=clean) if tur == "+" else a.cut(b, clean=clean)
            if r.val().isValid() and vmin <= r.val().Volume() <= vmax: return r
            son = (r.val().Volume(), r.val().isValid())
        except Exception as e: son = str(e)[:80]
    raise AssertionError("%s: boolean tutmadi %s (beklenen %.1f–%.1f)" % (ad, son, vmin, vmax))


# ---------------------------------------------------------------- 3 · BAYONET ----------------------------------------------------------------
def tirnak_ekle(tup, RD, CY):
    """tüpün dış yüzünde 3 bayonet TIRNAĞI — 8 (teğet) × 4 (eksen) × 3,2 (çap yönünde), tüp duvarına 0,5 gömülü = tüple TEK PARÇA (freze / baskı).
    Arka yüzün iki teğet kenarı 0,5 pahlı: tümseğin üstünden kayarak geçsin."""
    for a in TIRNAK_ACILARI:
        t = cq.Workplane("XY").box(3.7, TIRNAK_GEN, TIRNAK_Z1 - TIRNAK_Z0, centered=(False, True, False)).translate((RD - 0.5, 0, TIRNAK_Z0)).edges("|X").edges("<Z").chamfer(0.5)
        t = cq.Workplane(obj=t.val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), a).translate(cq.Vector(0, CY, 0)))
        v0 = tup.val().Volume(); tup = _islem(tup, t, "+", v0 + 85.0, v0 + 118.0, "tirnak %d" % a)
    return tup


def kanal_acilari(RD):
    th_w = math.degrees(math.asin((TIRNAK_GEN / 2 + 0.5) / (RD + 0.3)))      # cep yarı açısı: tırnağın iki yanında 0,5 mm boşluk (en dar yerde)
    th_h = math.degrees(2.0 / (RD + 2.0))                                     # tümsek: yay boyu 2 mm
    return th_w, th_h


def yatak_kapagi(RT, CY, TUP_Z1):
    """bayonet yatak kapağı · KİLİTLİ konumda modellenir. Kanal kapak duvarını BOYDAN BOYA keser (dışarıdan görünür, yıkanır, kir tutmaz)."""
    RD = RT + 3.0; th_w, th_h = kanal_acilari(RD)
    kp = silz(0, CY, RD + 4.0, 236.0, 254.5).cut(silz(0, CY, RD + 0.3, 235.0, TUP_Z1 + KAPAK_BOS)).cut(silz(0, CY, 6.2, TUP_Z1 - 1, 253.2))
    kp = kp.union(kut(-(RD - 1.0), RD - 1.0, CY - 4, CY + 4, 254.5, 266.0))                                  # tutma kanadı
    kp = kp.cut(boru(0, CY, RT + 0.3, RT + 2.7, TUP_Z1 - 0.5, TUP_Z1 + KAPAK_BOS + 1.4))                     # O-ring kanalı 2,4 × 1,4 (kordon 2,0 → 0,6 taşar)
    r0, r1 = RD - 0.2, RD + 4.5
    for a in TIRNAK_ACILARI:
        for a0, a1, z0, z1 in ((a - KILIT_ACI - th_w, a + th_w, Z_TUMSEK, Z_KANAL_UST),                     # kanalın tümsek kotundan yukarısı: boydan boya
                               (a - KILIT_ACI - th_w, a - th_w - th_h, Z_HALKA, Z_TUMSEK + 0.05),           # HALKA: serbest dönme bölgesi
                               (a - th_w, a + th_w, Z_CEP, Z_TUMSEK + 0.05),                                # CEP: tırnağın oturduğu yer · uzak duvarı = DAYAMA
                               (a - KILIT_ACI - th_w, a - KILIT_ACI + th_w, 234.0, Z_HALKA + 0.05)):        # GİRİŞ: ağızdan eksenel
            c = cq.Workplane(obj=sektor(r0, r1, a0, a1, z0, z1).val().translate(cq.Vector(0, CY, 0)))
            v0 = kp.val().Volume(); kp = _islem(kp, c, "-", v0 * 0.80, v0 - 1.0, "kapak kanali %d" % a)
    return kp


# ---------------------------------------------------------------- 1 · SAPLAMA + SOMUN + PUL ----------------------------------------------------------------
def saplama(x, y, z0, z1, dis=16.0):
    """M6 saplama: iki ucunda 'dis' mm diş (OLUKLU gösterim — gerçek helis değil, satın alınan parça), arası düz Ø6"""
    pts = [(0.0, z0), (2.6, z0)]
    def dis_bolgesi(za, zb):
        z = za
        while z < zb - 1e-6: pts.append((3.0, z + 0.5)); pts.append((2.4, z + 1.5)); z += 2.0          # GÖSTERİM adımı 2 mm (gerçek M6 adımı 1 mm; web modeli hafif kalsın)
    dis_bolgesi(z0, z0 + dis); pts.append((3.0, z0 + dis + 0.5)); pts.append((3.0, z1 - dis - 0.5)); dis_bolgesi(z1 - dis, z1); pts += [(2.6, z1), (0.0, z1)]
    g = cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))          # eksen YEREL koordinatta (XZ düzleminde +y = global z)
    return _dogrula(cq.Workplane(obj=g.val().translate(cq.Vector(x, y, 0))), 0.80 * math.pi * 9 * (z1 - z0), math.pi * 9 * (z1 - z0), "saplama")


def kor_somun(x, y, z_taban, yon):
    """DIN 1587 M6 kör somun: altıgen AA 10 × 5,5 + kubbe, toplam 12 · diş derinliği 8 · yon = kubbenin baktığı yön (±1)"""
    n = cq.Workplane("XY").polygon(6, 11.5).extrude(5.5)
    kubbe = cq.Workplane("XZ").polyline([(0.0, 5.0), (4.7, 5.0), (4.7, 8.2), (4.1, 10.0), (2.9, 11.3), (1.4, 11.85), (0.0, 12.0)]).close().revolve(360, (0, 0, 0), (0, 1, 0))
    n = n.union(kubbe).cut(silz(0, 0, 3.0, -1.0, 8.0))
    s = n.val()
    if yon < 0: s = s.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 180.0)
    return _dogrula(cq.Workplane(obj=s.translate(cq.Vector(x, y, z_taban))), 450.0, 900.0, "kor somun")


def pul(x, y, z0): return boru(x, y, 3.2, 6.0, z0, z0 + 1.6)


# ---------------------------------------------------------------- 2 · KULP ----------------------------------------------------------------
def kulp(xs, y, ZF):
    """kaynaklı paslanmaz kulp: 2 DOLU ayak Ø14 × 46 (tabanda Ø20 × 3 flanş: plastik plakaya geniş oturur) + Ø10 çubuk · ayakta M6 × 14 KÖR diş"""
    k = None
    for s in (-1, 1):
        a = silz(s * xs, y, 7.0, ZF, ZF + 46.0).union(silz(s * xs, y, 10.0, ZF, ZF + 3.0)).faces(">Z").edges().chamfer(1.5)
        k = a if k is None else k.union(a)
    k = k.union(silx(y, ZF + 37.0, 5.0, -xs, xs))
    for s in (-1, 1): k = k.cut(silz(s * xs, y, 3.0, ZF - 1.0, ZF + 14.0))
    return _dogrula(k, 1.0, 1e9, "kulp")


# ---------------------------------------------------------------- WEB AĞI ----------------------------------------------------------------
KABA = ("saplama_", "somun_", "pul_", "oring_", "insert_", "vida_", "yayli_pim", "setuskur")
def web_ag(ag, p):
    """küçük bağlantı elemanları web modelinde KABA ağla gider (dişli saplama tek başına 3600 üçgendi). Katının KOPYASI ağlanır: STL için üretilmiş
    ince ağ katının üstünde saklı kalıyor ve OpenCascade kaba istek gelince onu geri veriyor — kopya ağı taşımaz."""
    if p["ad"].startswith(KABA): return ag(cq.Workplane(obj=p["wp"].val().copy()), 0.4, 0.8)
    return ag(p["wp"])


# ---------------------------------------------------------------- HEPSİNİ UYGULA ----------------------------------------------------------------
def uygula(g):
    P = g["PARCALAR"]; AD = {p["ad"]: p for p in P}; ekle = g["ekle"]; kesit = g["kesit"]
    ZF, ZB, ZFI, ZBI, TP, ET, OYUK, D = g["ZF"], g["ZB"], g["ZFI"], g["ZBI"], g["TP"], g["ET"], g["OYUK"], g["D"]
    CY, YC, RT, Y_UST, SAP, TUP_Z1 = g["CY"], g["YC"], g["RT"], g["Y_UST"], g["SAPLAMA"], g["TUP_Z1"]
    EZ = 1.0                                                                   # contanın ezilmiş kalınlığı (serbest 1,5)

    # ---- 4a · gövde contası: gövde iki uçtan 1 mm kısalır, kanalın dibine gövde kesitinde düz conta ----
    govde = kesit(ET, Y_UST).extrude(D - 2 * TP + 2 * (OYUK - EZ)).translate((0, 0, ZBI - (OYUK - EZ))).cut(kesit(0.0, Y_UST + 1).extrude(D).translate((0, 0, ZB - 1)))
    v_es = AD["govde"]["wp"].val().Volume(); AD["govde"]["wp"] = _dogrula(govde, v_es * 0.98, v_es * 0.9999, "govde")
    AD["govde"]["bom"] = AD["govde"]["bom"][:3] + ("iki plakanın 4 mm kanalına oturur · kanal dibinde 1,5 mm silikon CONTA (saplamalar sıkınca 1,0'a ezilir)",)
    halka2d = lambda: kesit(ET, Y_UST).extrude(EZ).cut(kesit(0.0, Y_UST + 1).extrude(EZ + 2).translate((0, 0, -1)))
    for ad_, z0 in (("conta_arka", ZBI - OYUK), ("conta_on", ZFI + OYUK - EZ)):
        ekle(ad_, _dogrula(halka2d().translate((0, 0, z0)), 100.0, 1e6, ad_), "silikon",
             bom=("Gövde contası (gövde kesitinde)", 2, "FDA silikon 60 ShA levha 1,5 mm · su jeti / bıçak kesim", "plaka kanalının dibine oturur · 1,5 → 1,0 mm ezilir · gövde–plaka birleşimini sızdırmaz yapar") if ad_ == "conta_arka" else None)

    # ---- 4c · ön plaka: M4 insert yuvaları. Tüp O-ringi faturanın dibine oturur: faturayı DERİNLEŞTİRMEK OLMAZ — arkasında gövde kanalı var,
    #      arada yalnız 1 mm et kalıyor. Onun yerine tüpün geçmesi 2,8 → 1,3 mm kısaltıldı (üreteçte), açılan 1,7 mm'ye kordon 2,0 O-ring girer. ----
    po = AD["plaka_on"]["wp"]; xi = RT + 11.0
    for s in (1, -1): v0 = po.val().Volume(); po = _islem(po, silz(s * xi, CY, 2.8, ZF - 6.5, ZF + 1.0), "-", v0 - 90.0, v0 - 60.0, "insert yuvasi")
    AD["plaka_on"]["wp"] = po; AD["plaka_on"]["bom"] = AD["plaka_on"]["bom"][:3] + ("kanal · tüp geçişi Ø%.0f + fatura Ø%.1f × 3 (dibinde O-ring) · yatak Ø22,4 · 2 × M4 insert yuvası Ø5,6 × 6,5" % (2 * RT, 2 * RT + 6.4),)
    for s in (1, -1):
        ekle("insert_%s" % ("a" if s > 0 else "b"), boru(s * xi, CY, 1.95, 2.8, ZF - 6.2, ZF - 0.2), "celik",
             bom=("Dişli insert M4 × 6 (ısıyla / presle çakma)", 2, "pirinç ya da A2", "ön plakada · tüp vidası plastiğe değil METALE sıkılır: sök-tak dişi yemez") if s > 0 else None)
    ekle("oring_tup", torus(0, CY, ZF - 3.0 + 0.85, RT + 1.6, 0.85), "silikon",
         bom=("O-ring %.0f × 2" % (2 * RT + 1.0), 2, "FDA silikon / EPDM 70 ShA", "1 adet ön plakadaki tüp faturasının dibinde · 1 adet yatak kapağının içinde (hem conta hem bayonetin YAYI)"))
    ekle("oring_kapak", torus(0, CY, TUP_Z1 + (KAPAK_BOS + 1.4) / 2, RT + 1.5, (KAPAK_BOS + 1.4) / 2), "silikon")

    # ---- 4b · muylu O-ringleri: 2 tahrik göbeği + ön kovan (plaka deliği Ø22,4 · muylu Ø22 · kanal dibi Ø18 · kordon 2,5 → 2,2) ----
    for ad_, y, zm, grup in (("gobek_helezon", CY, ZB + 4.0, "helezon"), ("gobek_karistirici", YC, ZB + 4.0, "karistirici"), ("on_kovan", YC, ZFI + 4.0, "karistirici")):
        v0 = AD[ad_]["wp"].val().Volume(); AD[ad_]["wp"] = _islem(AD[ad_]["wp"], boru(0, y, 9.0, 12.5, zm - 1.65, zm + 1.65), "-", v0 - 440.0, v0 - 380.0, ad_ + " O-ring kanali")
        ekle("oring_" + ad_, torus(0, y, zm, 10.1, 1.1), "silikon", grup,
             bom=("O-ring 18 × 2,5", 3, "FDA silikon / EPDM 70 ShA", "2 tahrik göbeği + ön kovan muylusundaki kanalda · plaka deliğinden sızıntıyı keser (≤ 42 dev/dk)") if ad_ == "gobek_helezon" else None)
    AD["gobek_helezon"]["bom"] = AD["gobek_helezon"]["bom"][:3] + ("içeriden takılır: flanş Ø32 + muylu Ø22 (O-ring kanalı 3,3 × 2) + kare yuva 8,3 × 12",)

    # ---- 1 · saplama + pul + kör somun ----
    for i, (x, y) in enumerate(SAP):
        ust = y > 300
        AD["saplama_%d" % i]["wp"] = saplama(x, y, ZB - 9.0, ZF + (14.0 if ust else 9.0))
        AD["somun_arka_%d" % i]["wp"] = kor_somun(x, y, ZB - 1.6, -1)
        ekle("pul_arka_%d" % i, pul(x, y, ZB - 1.6), "celik", bom=("Pul M6 · Ø12 × 1,6", 6, "A2 · DIN 125", "plastik plakada somunun yükünü yayar · arka 4 + ön alt 2") if i == 0 else None)
        if not ust:
            AD["somun_on_%d" % i]["wp"] = kor_somun(x, y, ZF + 1.6, +1); ekle("pul_on_%d" % i, pul(x, y, ZF), "celik")
    AD["saplama_0"]["bom"] = ("Saplama M6 × 343 (alt)", 2, "A2 · iki ucu 16 mm diş, gövdesi düz Ø6", "plaka deliği Ø6,5'ten geçer · iki ucunda pul + kör somun · gövdenin DIŞINDA (gıdaya değmez)")
    AD["saplama_2"]["bom"] = ("Saplama M6 × 348 (üst)", 2, "A2 · iki ucu 16 mm diş, gövdesi düz Ø6", "ön ucu KULPUN ayağına dibe kadar vidalanır (14 mm) · arka ucunda pul + kör somun · dolum çizgisinin üstünde")
    AD["somun_arka_0"]["bom"] = ("Kör somun M6", 6, "A2 · DIN 1587", "arka 4 + ön alt 2 · kubbeli: diş ucu açıkta kalmaz, el kesmez")

    # ---- 2 · kulp ----
    xs = max(abs(x) for x, y in SAP if y > 300); yk = max(y for x, y in SAP)
    AD["kulp"]["wp"] = kulp(xs, yk, ZF)
    AD["kulp"]["bom"] = ("Kulp %.0f mm · kaynaklı" % (2 * xs), 1, "AISI 304 · 2 dolu ayak Ø14 (taban flanşı Ø20) + Ø10 çubuk TIG kaynak · ayakta M6 × 14 KÖR diş",
                         "ÜST iki saplama önce kulpa dibe kadar vidalanır, sonra kulp + saplamalar önden geçirilir, arkadan somun sıkılır")
