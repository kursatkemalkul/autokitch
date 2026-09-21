# -*- coding: utf-8 -*-
"""AUTOKITCH · KASET KONTROL LİSTESİ — her kaset için AYNI maddeler, otomatik denetlenir. Kullanım: python kaset_kontrol.py [--canli]
Bir kaset eklenince / değişince bu betik çalıştırılır; KALDI varsa yayınlanmaz. (Kemal, 22 Eyl 2026: "bir check list yap, o listeye göre her şeyi kontrol et")"""
import importlib, io, json, math, os, re, struct, subprocess, sys
U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); K3 = os.path.join(KOK, "otonom", "kaset3d"); sys.path.insert(0, U); os.chdir(U)
CANLI = "--canli" in sys.argv; SITE = "https://industrialproductdesigner.com/autokitch/otonom/kaset3d/"
KASET = [dict(ad="KAŞAR KABI v10", cad="kasar_cad_v10", onek="kasar_v10", klasor="kasar_kabi_v10", model=None, kg=8.8, akis="akis.html", rotor=False),
         dict(ad="KIYMA KASETİ v5", cad="kiyma_cad_v5", onek="kiyma_v5", klasor="kiyma_kaseti_v5", model="kiyma_akis_model_v2", kg=6.4, akis="akis_kiyma.html", rotor=True),
         dict(ad="KUŞBAŞI KASETİ v4", cad="kusbasi_cad_v4", onek="kusbasi_v4", klasor="kusbasi_kaseti_v4", model="kusbasi_akis_model_v2", kg=5.8, akis="akis_kusbasi.html", rotor=True),
         dict(ad="KÜP SUCUK KASETİ v3", cad="sucuk_cad_v3", onek="sucuk_v3", klasor="sucuk_kaseti_v3", model="sucuk_akis_model_v1", kg=2.8, akis="akis_sucuk.html", rotor=True)]
SONUC = []
def m(kaset, no, madde, gecti, ayrinti=""): SONUC.append((kaset, no, madde, bool(gecti), ayrinti))


def glb_oku(yol):
    d = open(yol, "rb").read(); n = struct.unpack("<I", d[12:16])[0]; g = json.loads(d[20:20 + n].decode("utf-8")); bin0 = 20 + n + 8
    def acc(i):
        a = g["accessors"][i]; v = g["bufferViews"][a["bufferView"]]; k = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}[a["type"]]
        return [struct.unpack_from("<%df" % k, d, bin0 + v.get("byteOffset", 0) + j * 4 * k) for j in range(a["count"])]
    return g, acc


for K in KASET:
    ad = K["ad"]
    # ---------- A · ÜRETECİN KENDİ DENETİMLERİ (çıktısından okunur) ----------
    cik = subprocess.run([sys.executable, K["cad"] + ".py"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    m(ad, "A1", "bütün parçalar geçerli katı", "KATI DENETIMI: hepsi gecerli" in cik)
    m(ad, "A2", "iç içe geçen parça yok", "TEMIZ — ic ice gecen parca yok" in cik)
    m(ad, "A3", "helezon ve karıştırıcı 4 açıda döndürülünce de temiz", cik.count("donmus: temiz") == 8, "%d / 8" % cik.count("donmus: temiz"))
    m(ad, "A4", "kanat her dilimde tam çapta", "TAMAM: kanat her yerde" in cik)
    m(ad, "A5", "hatve katının üstünde ölçüldü = tasarım", re.search(r"→ TAMAM \(\d+ tur olculdu", cik) is not None)
    m(ad, "A6", "hesap modeli = CAD (aynı sayılar)", ("MODEL = CAD" in cik) if K["model"] else True, "" if K["model"] else "kaşarın modeli sayfada, ayrıca denetlenmiyor")
    m(ad, "A7", "USD (AR) biçim denetimi", "USD denetimi: GECTI" in cik)
    # ---------- B · GEOMETRİ (modül içinden) ----------
    V = importlib.import_module(K["cad"]); V.PARCALAR[:] = []; V.kap(); P = V.PARCALAR
    bb = [(p["ad"], p["wp"].val().BoundingBox()) for p in P]
    K["hacim"] = {p["ad"]: p["wp"].val().Volume() for p in P}
    ymin = min(b.ymin for _, b in bb); m(ad, "B1", "kaset (tapa takılıyken) ayaklarının üstünde durur: hiçbir parça tabanın altına inmez", ymin >= -0.01, "en alt nokta y %.1f" % ymin)
    xmaks = max(max(abs(b.xmin), abs(b.xmax)) for a_, b in bb if a_ != "kilit_pimi"); m(ad, "B2", "genişlik zarfın içinde", xmaks <= V.W / 2 + 0.01, "yarı genişlik %.1f ≤ %.0f" % (xmaks, V.W / 2))
    ymaks = max(b.ymax for _, b in bb); m(ad, "B3", "yükseklik zarfın içinde", ymaks <= V.H + 0.01, "%.0f ≤ %.0f" % (ymaks, V.H))
    m(ad, "B4", "helezon ön plakadaki delikten çıkarılabilir (kanat Ø < delik Ø)", V.R_KANAT < V.RT, "Ø%.0f < Ø%.0f" % (2 * V.R_KANAT, 2 * V.RT))
    hac = V.v4.hacim_L(V.Y_DOLUM); rho = V.RHO; dol = 100 * K["kg"] / rho / hac
    m(ad, "B5", "2 günlük stok sığıyor, doluluk ≤ %90", dol <= 90.0, "%.1f kg = %.1f L / %.1f L = %%%.0f" % (K["kg"], K["kg"] / rho, hac, dol))
    # ---------- J · BİRLEŞİM DETAYLARI (Kemal: "çubuk nasıl takılıyor, kulp nasıl takılıyor, kapak nasıl klik ediyor") ----------
    import cadquery as cq, kaset_birlesim_v1 as BR
    S = {p["ad"]: p["wp"].val() for p in P}; adlar = set(S)
    gerek = ["conta_arka", "conta_on", "insert_a", "insert_b", "oring_tup", "oring_kapak", "oring_gobek_helezon", "oring_gobek_karistirici", "oring_on_kovan"] + ["pul_arka_%d" % i_ for i_ in range(4)] + ["pul_on_0", "pul_on_1"]
    eks = [a_ for a_ in gerek if a_ not in adlar]; m(ad, "J1", "her ıslak birleşimde conta / O-ring, her somunun altında pul, tüp vidasında metal insert VAR", not eks, ", ".join(eks) or "%d parça" % len(gerek))
    sb = S["saplama_2"].BoundingBox(); gir = sb.zmax - V.ZF; d_k = S["saplama_2"].distance(S["kulp"]); v_k = S["saplama_2"].intersect(S["kulp"]).Volume()
    m(ad, "J2", "üst saplama kulpun ayağına 14 mm girer ve DİBE dayanır (dipte kilitlenir → arka somun sıkılırken dönmez), iç içe geçme yok", abs(gir - 14.0) < 0.05 and d_k < 0.02 and v_k < 1.0, "giriş %.1f mm · mesafe %.2f · ortak hacim %.2f" % (gir, d_k, v_k))
    sd = S["saplama_0"].Volume(); duz = math.pi * 9.0 * (S["saplama_0"].BoundingBox().zlen); sm = S["somun_arka_0"].BoundingBox()
    m(ad, "J3", "saplamanın uçlarında diş bölgesi modelde var (düz çubuk değil) · somun kubbeli kör somun (boy 12)", sd < duz - 80.0 and abs(sm.zlen - 12.0) < 0.05, "saplama %.0f < düz %.0f mm³ · somun boyu %.1f" % (sd, duz, sm.zlen))
    eksen = (cq.Vector(0, V.CY, 0), cq.Vector(0, V.CY, 1)); kapak = S["yatak_kapagi"]; tup = S["cikis_tupu"]
    v_kilit = kapak.intersect(tup).Volume(); d_kilit = kapak.distance(tup)
    m(ad, "J4", "KİLİTLİ konumda kapak tüple iç içe geçmiyor ve tırnak cebin tabanına OTURUYOR (mesafe 0)", v_kilit < 0.05 and d_kilit < 0.02, "ortak hacim %.3f · mesafe %.3f" % (v_kilit, d_kilit))
    acik = kapak.rotate(eksen[0], eksen[1], BR.KILIT_ACI); v_cik = max(acik.translate(cq.Vector(0, 0, dz)).intersect(tup).Volume() for dz in (0.0, 2.0, 5.0, 8.0, 11.0, 14.0))
    m(ad, "J5", "kapak %g° geri çevrilince tırnaklar giriş kanalına hizalanır: kapak eksenel olarak ÇEKİLİP ÇIKAR (0–14 mm boyunca takılma yok)" % BR.KILIT_ACI, v_cik < 0.05, "en büyük ortak hacim %.3f mm³" % v_cik)
    yari = kapak.rotate(eksen[0], eksen[1], 5.0); v_tumsek = yari.intersect(tup).Volume(); v_itili = yari.translate(cq.Vector(0, 0, -(BR.Z_TUMSEK - BR.Z_CEP) + 0.001)).intersect(tup).Volume()
    m(ad, "J6", "KLİK: kapak İTİLMEDEN çevrilirse tırnak TÜMSEĞE takılır (kendiliğinden açılmaz); %.2f mm itilince geçer" % (BR.Z_TUMSEK - BR.Z_CEP), v_tumsek > 0.3 and v_itili < 0.05, "itilmeden %.2f mm³ takılıyor · itilince %.3f" % (v_tumsek, v_itili))
    donus = [kapak.rotate(eksen[0], eksen[1], a_).translate(cq.Vector(0, 0, -(BR.Z_TUMSEK - BR.Z_CEP) + 0.001)).intersect(tup).Volume() for a_ in (8.0, 12.0, 18.0, 24.0, 30.0)]
    m(ad, "J7", "itili tutulurken 0° → %g° arası dönüş serbest (halka kanalında takılma yok)" % BR.KILIT_ACI, max(donus) < 0.05, "en büyük ortak hacim %.3f mm³" % max(donus))
    # ---------- K · KAPAK YOK DÜZENLEMESİ (Kemal 22 Eyl) + rotor/kovan kapatmaları ----------
    m(ad, "K1", "kaset KAPAKSIZ: modelde kapak parçası yok", "kapak" not in adlar, "%d parça" % len(P))
    gb = S["govde"].BoundingBox(); dudak_y = [f for f in S["govde"].Faces() if abs(f.Center().y - (V.Y_UST - 0.75)) < 0.8]
    yatay = [f for f in S["govde"].Faces() if abs(f.normalAt(f.Center()).y) > 0.9 and f.Center().y > V.Y_UST - 2.0]
    m(ad, "K2", "gövdenin ağzında İÇE 8 mm bükme dudak var (kenar keskin değil, ağız esnemez, elle tutulur)", len(yatay) >= 2 and gb.ymax <= V.Y_UST + 0.01,
      "%d yatay dudak yüzeyi · gövde en üst nokta y %.1f" % (len(yatay), gb.ymax))
    m(ad, "K3", "dudak kasetin DIŞ ölçüsünü büyütmedi (140 / 280 zarfı bozulmadı)", gb.xlen <= V.W + 0.01, "gövde genişliği %.1f ≤ %.0f" % (gb.xlen, V.W))
    if K.get("rotor"):
        ortak = sum(S["orumcek_" + a_].intersect(S["cubuk_0"]).Volume() for a_ in ("arka", "orta", "on"))
        ara = [S["orumcek_" + a_].distance(S["cubuk_0"]) for a_ in ("arka", "orta", "on")]
        m(ad, "K4", "SIYIRICI LAMA üç göbeğin de içinden geçiyor, aralık KAYNAKLANABİLİR ölçüde (≤ 0,2 mm) ve iç içe geçme yok", max(ara) <= 0.2 and ortak < 1.0,
          "göbek-lama aralığı %s mm · iç içe geçme %.2f mm³" % (" / ".join("%.2f" % x for x in ara), ortak))
        import kaset_birlesim_v1 as _BR2
        AMr = importlib.import_module(K["model"]); d_min = S["cubuk_0"].distance(S["govde"]); d_kol = S["orumcek_orta"].distance(S["govde"])
        m(ad, "K5", "kaynak yakaları lamadan DIŞARI taşmadı: kâse boşluğunu en dar tutan hâlâ lamanın kendisi", d_kol >= d_min - 0.01, "lama–kâse %.2f · kol(yakalı)–kâse %.2f mm" % (d_min, d_kol))
    lab = S["on_kovan"].intersect(S["orumcek_on"]).Volume(); d_lab = S["on_kovan"].distance(S["orumcek_on"])
    ub = S["orumcek_on"].BoundingBox(); kb = S["on_kovan"].BoundingBox()
    m(ad, "K6", "ÖN KOVAN LABİRENTİ: örümcek göbeği kovanın havşasına giriyor (ürün kare mile sürünemez), iç içe geçme yok",
      lab < 0.05 and ub.zmax > kb.zmin + 1.0 and d_lab < 0.25, "örtüşme boyu %.1f mm · radyal aralık %.2f mm · ortak hacim %.3f" % (ub.zmax - kb.zmin, d_lab, lab))
    # ---------- C · ÜRETİM DOSYALARI ----------
    ur = os.path.join(KOK, "arastirma", "3_TOPPING", K["klasor"]); eks = [p["ad"] for p in P if not (os.path.exists(os.path.join(ur, "step", p["ad"] + ".step")) and os.path.exists(os.path.join(ur, "stl", p["ad"] + ".stl")))]
    m(ad, "C1", "her parçanın STEP + STL dosyası var", not eks, "%d parça%s" % (len(P), (" · eksik: " + ", ".join(eks)) if eks else ""))
    mont = [f for f in os.listdir(ur) if f.endswith("_MONTAJ.step")]; m(ad, "C2", "montaj STEP + bölünmemiş helezon + BOM var", bool(mont) and os.path.exists(os.path.join(ur, "step", "helezon_TEK_PARCA.step")) and os.path.exists(os.path.join(ur, "BOM.csv")))
    bom = json.load(io.open(os.path.join(ur, "bom.json"), encoding="utf-8")); m(ad, "C3", "parça listesindeki adetlerin toplamı = modeldeki parça sayısı", sum(b[2] for b in bom) == len(P), "%d = %d" % (sum(b[2] for b in bom), len(P)))
    # ---------- D · ANİMASYON = HESAP ----------
    g, acc = glb_oku(os.path.join(K3, K["onek"] + "_dozaj.glb")); an = g["animations"][0]; nd = g["nodes"]
    def kanal(ad_, yol):
        for c in an["channels"]:
            if nd[c["target"]["node"]]["name"] == ad_ and c["target"]["path"] == yol: s_ = an["samplers"][c["sampler"]]; return [t[0] for t in acc(s_["input"])], acc(s_["output"])
        return None, None
    ts, kay = kanal("KAY_tabla", "translation"); _t, don = kanal("DON_tabla", "rotation")
    if K["model"]:
        AM = importlib.import_module(K["model"]); R0 = AM.r_t_k(0.0); bek_r = lambda t: AM.r_t_k(t); bek_tur = lambda t: AM.tabla_tur(t)
    else:
        from kasar_akis_model_v2 import r_t, YASA; R0 = YASA["r_dis"]; bek_r = lambda t: r_t(t); bek_tur = lambda t: 7.0 * t / 12.0
    hata = max(abs((R0 - bek_r(t)) - k_[0] * 1000.0) for t, k_ in zip(ts, kay) if t <= 10.0)
    m(ad, "D1", "dozaj animasyonunda tabla ÜRÜNÜN KENDİ hareket yasasıyla yürüyor", hata < 0.6, "en büyük fark %.2f mm" % hata)
    def tur_coz(q):                                                       # kuaterniyon dizisinden birikimli tur
        top, onc = 0.0, 0.0
        for x, y, z, w in q:
            a = 2 * math.atan2(y, w); da = (a - onc + math.pi) % (2 * math.pi) - math.pi; top += da; onc = a
            yield top / (2 * math.pi)
    turlar = list(tur_coz(don)); ht = max(abs(tt - bek_tur(t)) for t, tt in zip(ts, turlar) if t <= 10.0)
    m(ad, "D2", "tablanın dönüşü hesaptaki devirle aynı", ht < 0.02, "10 sn'de %.2f tur (hesap %.2f)" % (turlar[min(len(turlar) - 1, 100)], bek_tur(10.0)))
    # ---------- E · AR DOSYALARI (iPhone yalnız YAZILI örnekleri okur) ----------
    from pxr import Usd, UsdGeom
    for son, parca in (("_calis.usdz", "helezon_B"), ("_montaj.usdz", "helezon_A")):
        yol = os.path.join(K3, K["onek"] + son); var = os.path.exists(yol); enb, sap, ns = 999.0, 999.0, 0
        if var:
            st = Usd.Stage.Open(yol); pr = [q for q in st.Traverse() if q.GetName() == parca][0]; op = UsdGeom.Xformable(pr).GetOrderedXformOps()[0]; tz = op.GetTimeSamples(); onc = None; enb = sap = 0.0; ns = len(tz)
            for t in tz:
                mm_ = op.Get(t); a = math.degrees(math.atan2(mm_[0][1], mm_[0][0]))
                if onc is not None: enb = max(enb, abs((a - onc + 180.0) % 360.0 - 180.0))
                onc = a; e2 = mm_.Transform((0.0, V.CY / 1000.0, 0.1)); sap = max(sap, math.hypot(e2[0], e2[1] - V.CY / 1000.0) * 1000)
        m(ad, "E1" if "calis" in son else "E2", ("çalışma" if "calis" in son else "montaj") + " AR animasyonu: her karede örnek, ardışık dönüş < 180°, eksen sapması yok", var and enb < 180.0 and sap < 0.01, "%d örnek · en büyük adım %.1f° · sapma %.4f mm" % (ns, enb, sap))
    # ---------- F · SAYFA ----------
    h = io.open(os.path.join(K3, "index.html"), encoding="utf-8").read(); anahtarlar = [K["onek"], K["onek"] + "_montaj", K["onek"] + "_dozaj"]
    eks = [a_ for a_ in anahtarlar if ('data-m="%s"' % a_) not in h or ("\n  %s:{" % a_) not in h]; m(ad, "F1", "üç sekme de sayfada ve kayıtları var", not eks, ", ".join(eks))
    dosyalar = [a_ + ".glb" for a_ in anahtarlar] + [K["onek"] + x for x in (".usdz", "_calis.usdz", "_montaj.usdz")] + [K["akis"]]
    eks = [f for f in dosyalar if not os.path.exists(os.path.join(K3, f))]; m(ad, "F2", "sayfanın çağırdığı bütün dosyalar yerinde", not eks, ", ".join(eks) or "%d dosya" % len(dosyalar))
    kullanilan = set(re.findall(r'usdz:"([^"]+)"', "".join(re.findall(r"\n  %s[^\n]*:\{[^\n]*" % K["onek"], h)))); eks = [f for f in kullanilan if not os.path.exists(os.path.join(K3, f))]
    m(ad, "F3", "AR düğmesinin açtığı dosyalar var ve üretim/dozajda ANİMASYONLU olan seçili", not eks and (K["onek"] + "_calis.usdz") in kullanilan and (K["onek"] + "_montaj.usdz") in kullanilan, ", ".join(sorted(kullanilan)))
    if K["model"]:
        J = json.load(io.open(os.path.join(K3, re.sub(r"_v\d+$", "", K["onek"]) + "_model.json"), encoding="utf-8")); ak = io.open(os.path.join(K3, K["akis"]), encoding="utf-8").read()
        if "doz" in J: x = [q for q in J["doz"] if abs(q["etaF"] - 0.6) < 1e-9][0]; aranan = [("%.1f" % x["g_tur"]).replace(".", ","), ("%.2f" % x["tur"]).replace(".", ",")]
        else: aranan = ["%d mm" % J["L"], "%%%d" % J["kap"], ("%.2f" % J["H_GEREK"]).replace(".", ",")]
        eks = [a_ for a_ in aranan if a_ not in ak]; m(ad, "F4", "hesap sayfasındaki sayılar modelin ürettiği sayılarla aynı", not eks, "arananlar: " + " · ".join(aranan))
    if CANLI:
        import urllib.request
        kotu = []
        for f in dosyalar + ["index.html"]:
            try: kod = urllib.request.urlopen(urllib.request.Request(SITE + f, method="HEAD"), timeout=30).status
            except Exception as e: kod = str(e)[:40]
            if kod != 200: kotu.append("%s → %s" % (f, kod))
        m(ad, "G1", "canlı sitede bütün dosyalar açılıyor", not kotu, "; ".join(kotu) or "%d dosya 200" % (len(dosyalar) + 1))

# ---------- H · "ORTAK" iddiaları doğru mu: aynı dosyadan basılan parça gerçekten birebir aynı mı (hacim farkı < 0,5 mm³) ----------
ORTAK4 = ["oring_gobek_helezon", "oring_on_kovan", "pul_arka_0", "pul_on_0", "somun_arka_0", "somun_on_0", "insert_a", "gobek_helezon", "kavrama_helezon", "yayli_pim_helezon", "gobek_karistirici", "kavrama_karistirici", "on_kovan", "topuz", "setuskur", "kilit_pimi", "kar_mil", "helezon_cekirdek"]
fark = [a_ for a_ in ORTAK4 if max(K_["hacim"][a_] for K_ in KASET) - min(K_["hacim"][a_] for K_ in KASET) > 0.5]
m("KASETLER BİRLİKTE", "H1", "dört kasette (kaşar dahil) ORTAK denen %d parça birebir aynı" % len(ORTAK4), not fark, ", ".join(fark))
K140 = KASET[1:]; GOVDE = ["govde", "plaka_arka", "plaka_on", "kulp", "yatak_kapagi", "kar_mil", "helezon_cekirdek", "conta_arka", "conta_on", "oring_tup", "oring_kapak", "insert_a", "insert_b"] + ["saplama_%d" % i_ for i_ in range(4)] + ["somun_arka_%d" % i_ for i_ in range(4)] + ["somun_on_0", "somun_on_1", "vida_tup_a", "vida_tup_b"]
fark = [a_ for a_ in GOVDE if max(K_["hacim"][a_] for K_ in K140) - min(K_["hacim"][a_] for K_ in K140) > 0.5]
m("KASETLER BİRLİKTE", "H2", "ORTAK GÖVDE: kıyma = kuşbaşı = küp sucuk kasetinde gövde + iki uç plakası + kulp + yatak kapağı + saplamalar + contalar + O-ringler birebir aynı", not fark, ", ".join(fark) or "%d parça" % len(GOVDE))
fark = [a_ for a_ in KASET[2]["hacim"] if abs(KASET[2]["hacim"][a_] - KASET[3]["hacim"].get(a_, -1)) > 0.5] + [a_ for a_ in KASET[3]["hacim"] if a_ not in KASET[2]["hacim"]]
m("KASETLER BİRLİKTE", "H3", "küp sucuk kaseti = kuşbaşı kaseti: BÜTÜN parçalar birebir aynı (aynı dosyadan basılır)", not fark, ", ".join(fark) or "%d / %d parça" % (len(KASET[3]["hacim"]), len(KASET[2]["hacim"])))
eks_ = [(importlib.import_module(K_["cad"]).CY, importlib.import_module(K_["cad"]).YC, importlib.import_module(K_["cad"]).RT) for K_ in K140]
m("KASETLER BİRLİKTE", "H5", "140 sınıfında iki mil ekseni ve tekne çapı üç kasette aynı (makinedeki tahrik yuvaları ortak)", len(set(eks_)) == 1, " · ".join("%s %g / %g / Ø%g" % (K_["ad"].split()[0], e[0], e[1], 2 * e[2]) for K_, e in zip(K140, eks_)))
# tuzak: varsayılan argüman ürün sabitini dondurur → her tane modeli KENDİ sürtünmesiyle hesaplamalı
for K_ in (KASET[2], KASET[3]):
    AM_ = importlib.import_module(K_["model"]); MM_ = getattr(AM_, "M", AM_); G_ = MM_.G; q_m = MM_.kapasite(1.0)[4]
    q_fi = MM_.kapasite(1.0, MM_.FI_S)[4]; q_kus = MM_.kapasite(1.0, math.degrees(math.atan(0.35)))[4]
    m(K_["ad"], "H6", "kapasite ürünün KENDİ sürtünme açısıyla hesaplanıyor (varsayılan argüman tuzağı yok)", abs(q_m - q_fi) < 1e-6 and (abs(MM_.MU - 0.35) < 1e-9 or abs(q_m - q_kus) > 0.5), "μ %.2f → %.1f mL/tur (μ 0,35 olsaydı %.1f)" % (MM_.MU, q_m, q_kus))
h_ = io.open(os.path.join(K3, "index.html"), encoding="utf-8").read(); eksik_ = [k_ for k_ in set(re.findall(r'data-m="([^"]+)"', h_)) if ("  %s:{" % k_) not in h_ or not os.path.exists(os.path.join(K3, k_ + ".glb"))]
m("KASETLER BİRLİKTE", "H4", "sayfadaki HER sekmenin (arşiv dahil) kaydı ve model dosyası var", not eksik_, ", ".join(eksik_) or "%d sekme" % len(set(re.findall(r'data-m="([^"]+)"', h_))))

gec = sum(1 for s_ in SONUC if s_[3]); print("\nKASET KONTROL LİSTESİ · %d / %d GEÇTİ\n" % (gec, len(SONUC)))
onc = None
for kaset, no, madde, ok_, ayr in SONUC:
    if kaset != onc: print("── %s ──" % kaset); onc = kaset
    print("  %s %-3s %-96s %s" % ("GEÇTİ" if ok_ else "KALDI", no, madde, ayr))
json.dump([dict(kaset=a, no=b, madde=c, gecti=d, ayrinti=e) for a, b, c, d, e in SONUC], io.open(os.path.join(U, "kaset_kontrol_sonuc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.stdout.flush(); os._exit(0 if gec == len(SONUC) else 1)
