# -*- coding: utf-8 -*-
"""AUTOKITCH · KASET KONTROL LİSTESİ — her kaset için AYNI maddeler, otomatik denetlenir. Kullanım: python kaset_kontrol.py [--canli]
Bir kaset eklenince / değişince bu betik çalıştırılır; KALDI varsa yayınlanmaz. (Kemal, 22 Eyl 2026: "bir check list yap, o listeye göre her şeyi kontrol et")"""
import importlib, io, json, math, os, re, struct, subprocess, sys
U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); K3 = os.path.join(KOK, "otonom", "kaset3d"); sys.path.insert(0, U); os.chdir(U)
CANLI = "--canli" in sys.argv; SITE = "https://industrialproductdesigner.com/autokitch/otonom/kaset3d/"
KASET = [dict(ad="KAŞAR KABI v8", cad="kasar_cad_v8", onek="kasar_v8", klasor="kasar_kabi_v8", model=None, kg=8.8, akis="akis.html"),
         dict(ad="KIYMA KASETİ v2", cad="kiyma_cad_v2", onek="kiyma_v2", klasor="kiyma_kaseti_v2", model="kiyma_akis_model_v1", kg=6.4, akis="akis_kiyma.html"),
         dict(ad="KUŞBAŞI KASETİ v1", cad="kusbasi_cad_v1", onek="kusbasi_v1", klasor="kusbasi_kaseti_v1", model="kusbasi_akis_model_v1", kg=5.8, akis="akis_kusbasi.html")]
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

# ---------- H · "ORTAK PARÇA" iddiası doğru mu: aynı parçadan üç kasete de basılabilir mi ----------
ORTAK3 = ["gobek_helezon", "kavrama_helezon", "yayli_pim_helezon", "gobek_karistirici", "kavrama_karistirici", "on_kovan", "topuz", "setuskur", "kilit_pimi", "kar_mil", "helezon_cekirdek"]
fark = [a_ for a_ in ORTAK3 if max(K_["hacim"][a_] for K_ in KASET) - min(K_["hacim"][a_] for K_ in KASET) > 0.5]
m("ÜÇ KASET BİRLİKTE", "H1", "üç kasette ORTAK denen %d parça gerçekten birebir aynı (hacim farkı < 0,5 mm³)" % len(ORTAK3), not fark, ", ".join(fark))
ROTOR = ["orumcek_arka", "orumcek_orta", "orumcek_on", "cubuk_0", "cubuk_1", "kapak", "kulp", "saplama_0", "saplama_2", "somun_arka_0"]
fark = [a_ for a_ in ROTOR if abs(KASET[1]["hacim"][a_] - KASET[2]["hacim"][a_]) > 0.5]
m("ÜÇ KASET BİRLİKTE", "H2", "kıyma ile kuşbaşında ORTAK denen rotor + kapak + kulp + saplamalar birebir aynı (gövde ve plakalar FARKLI — tekne çapı başka)", not fark, ", ".join(fark) or "%d parça" % len(ROTOR))
yuk = ["%s %g / %g" % (K_["ad"].split()[0], importlib.import_module(K_["cad"]).CY, importlib.import_module(K_["cad"]).YC) for K_ in KASET]
m("ÜÇ KASET BİRLİKTE", "H3", "140 sınıfında ALT mil ekseni ortak (üst eksen ürüne bağlı: rotor–kanat aralığı kuralı)", importlib.import_module(KASET[1]["cad"]).CY == importlib.import_module(KASET[2]["cad"]).CY, " · ".join(yuk))
h_ = io.open(os.path.join(K3, "index.html"), encoding="utf-8").read(); eksik_ = [k_ for k_ in set(re.findall(r'data-m="([^"]+)"', h_)) if ("  %s:{" % k_) not in h_ or not os.path.exists(os.path.join(K3, k_ + ".glb"))]
m("ÜÇ KASET BİRLİKTE", "H4", "sayfadaki HER sekmenin (arşiv dahil) kaydı ve model dosyası var", not eksik_, ", ".join(eksik_) or "%d sekme" % len(set(re.findall(r'data-m="([^"]+)"', h_))))

gec = sum(1 for s_ in SONUC if s_[3]); print("\nKASET KONTROL LİSTESİ · %d / %d GEÇTİ\n" % (gec, len(SONUC)))
onc = None
for kaset, no, madde, ok_, ayr in SONUC:
    if kaset != onc: print("── %s ──" % kaset); onc = kaset
    print("  %s %-3s %-96s %s" % ("GEÇTİ" if ok_ else "KALDI", no, madde, ayr))
json.dump([dict(kaset=a, no=b, madde=c, gecti=d, ayrinti=e) for a, b, c, d, e in SONUC], io.open(os.path.join(U, "kaset_kontrol_sonuc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.stdout.flush(); os._exit(0 if gec == len(SONUC) else 1)
