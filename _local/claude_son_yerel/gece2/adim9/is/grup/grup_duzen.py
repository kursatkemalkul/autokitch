# -*- coding: utf-8 -*-
"""GRUPLAMA DÜZENİ (Kemal 3 Eki 2026 "tamam yap") — hat3_v8za.glb → hat3_v8zb.glb · GEOMETRİ DEĞİŞMEZ, yalnız extras.
IEC 81346 mantığı: her parça iki etiket
  NEREDE ('mek') : İstasyon → Ünite. Her istasyonda aynı sıra: Gövde · fonksiyonel üniteler · Elektrik · Hava · Soğutma.
                   Ünitenin motoru/redüktörü/sensörü/silindiri/valfi ünitede; KABLO (+kelepçe, rakor, kanal, Harting, pano) istasyonun Elektrik'inde.
  NE ('kat')     : disiplin. KONTROL'den SENSOR ayrıldı; GUC + tüm kablolar = ELEKTRIK.
Kullanım: python grup_duzen.py <giris.glb> <cikis.glb>
Çıktı: esleme.json (parça başına eski/yeni etiket) · ozet.md · mekanizma_v3_8.json (sayfa ağacı)"""
import json, struct, sys, os, re, collections
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(S, "gece"))
from m7_etiket import pk_yeni  # noqa: E402

GIRIS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(S, "hat3_v8za.glb")
CIKIS = sys.argv[2] if len(sys.argv) > 2 else os.path.join(S, "hat3_v8zb.glb")

# ------------------------------------------------------------------ yeni listeler
AGAC = [
    ("A", ["Gövde", "Açıcı"]),                       # A satın alınır; eski A/Elektrik yalnız sıfır alanlı artık üçgen (v3.6'da kalkan sigorta/klemens) → A/Gövde
    ("B", ["Gövde", "Çekmeceler", "Soğuk depo", "Elektrik", "Soğutma"]),
    ("TOPPING", ["Gövde", "Tabla", "Sos", "Harç", "Kıyma", "Kuşbaşı", "Kaşar", "Sucuk", "Elektrik", "Hava", "Soğutma"]),
    ("F", ["Gövde", "Fırın", "Yükleme bandı", "Davlumbaz", "Elektrik", "Hava"]),
    ("K", ["Gövde", "Bant", "Bıçak", "İtici", "Sprey", "Elektrik", "Hava"]),
    ("E", ["Gövde", "Şarjör", "Asansör", "Besleyici", "Kutu katlama", "Robot çöpü", "Elektrik", "Hava"]),
    ("U", ["Gövde", "Havalandırma", "Elektrik"]),
    ("QR", ["Gövde", "Gözler", "Müşteri paneli", "Elektrik"]),
    ("Tezgâh", ["Gövde", "Bulaşık makinesi", "Evye"]),
    ("Robot", ["Robot kolu", "Yer rayı", "Kontrol kutusu", "Elektrik"]),
    ("Elektrik", ["Ana pano", "Ana hat"]),
    ("Çevre", ["Zemin", "Ürün", "İnsan figürü"]),
]
YMEK = [dict(kod=i + "/" + g, istasyon=i, ad=g) for i, gs in AGAC for g in gs]
YMI = {m["kod"]: n for n, m in enumerate(YMEK)}
YKAT = [
    dict(kod="GOVDE", ad="Gövde", icerik="sac, şase, dış kabuk, kapaklar, menteşe / kilit, ayaklar, kaide, yalıtım", kime="sac / şase atölyesi"),
    dict(kod="MEKANIZMA", ad="Mekanizma", icerik="raylar, arabalar, vidalı miller, kayış-kasnak, yataklar, kalıp ve takımlar", kime="mekanik montaj"),
    dict(kod="MOTOR", ad="Motor", icerik="step / servo / DC motorlar, redüktörler, motor sürücüleri", kime="servo / otomasyon firması"),
    dict(kod="SENSOR", ad="Sensör", icerik="endüktif / reed / limit / sıfır sensörleri, bayrak ve mıknatısları, enkoder, tartı hücresi, basınç ve sıcaklık sensörü, QR okuyucu", kime="otomasyon firması"),
    dict(kod="HAVA", ad="Hava", icerik="kompresör, şartlandırıcı, valf adası, valfler, silindirler, vakum, hava hortumları", kime="pnömatikçi"),
    dict(kod="SOGUTMA", ad="Soğutma", icerik="soğutma grubu, evaporatör, bakır hatlar, yoğuşma / tahliye", kime="soğutmacı"),
    dict(kod="ELEKTRIK", ad="Elektrik", icerik="ana şalter, sigorta, güç kaynağı, UPS, pano kutuları, TÜM kablolar (güç + sinyal + veri), kanal, rakor, Harting, klemens", kime="elektrikçi"),
    dict(kod="KONTROL", ad="Kontrol", icerik="PLC / RevPi / Beckhoff, G/Ç kartları, ağ anahtarı, modem, ekran, tuş takımı, kilit kartı, emniyet", kime="otomasyon firması"),
    dict(kod="GIDA", ad="Gıda", icerik="gıdaya değen: hazneler, kasetler, dozaj, bantlar, fırın, nozül, yağ hattı", kime="gıda hijyeni"),
    dict(kod="ROBOT", ad="Robot", icerik="FR5, yer rayı, enerji zinciri, çatal, robot kontrol kutusu", kime="robot entegratörü"),
    dict(kod="URUN", ad="Ürün", icerik="hamur, pizza, kutu, içecek, yağ tenekesi (görsel)", kime="—"),
    dict(kod="DUKKAN", ad="Dükkân", icerik="tezgâh, bulaşık, evye, zemin kanalı, insan ölçeği (görsel)", kime="—"),
]
YKI = {k["kod"]: n for n, k in enumerate(YKAT)}

# ------------------------------------------------------------------ GLB oku
raw = open(GIRIS, "rb").read()
jl = struct.unpack("<I", raw[12:16])[0]
J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}


def acc(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
    n = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[a["type"]]; dt = TD[a["componentType"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0); st = v.get("byteStride", 0); isz = np.dtype(dt).itemsize
    if st and st != n * isz:
        b = np.frombuffer(BIN[off:off + st * a["count"]], np.uint8).reshape(a["count"], st)[:, :n * isz]
        r = np.frombuffer(b.tobytes(), dt)
    else:
        r = np.frombuffer(BIN[off:off + a["count"] * n * isz], dt)
    return r.reshape(-1, n) if n > 1 else r


def trs(nd):
    if "matrix" in nd: return np.array(nd["matrix"]).reshape(4, 4).T
    M = np.eye(4); t = nd.get("translation", [0, 0, 0]); x, y, z, w = nd.get("rotation", [0, 0, 0, 1]); s = nd.get("scale", [1, 1, 1])
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    M[:3, :3] = R * np.array(s)[None, :]; M[:3, 3] = t; return M


W = {}


def gez(i, P):
    M = P @ trs(J["nodes"][i]); W[i] = M
    for c in J["nodes"][i].get("children", []): gez(c, M)


for r in J["scenes"][0]["nodes"]: gez(r, np.eye(4))
EX = J["scenes"][0]["extras"]
EMEK = [m["kod"] for m in EX["mekanizmalar"]]; EKAT = [k["kod"] for k in EX["kategoriler"]]

PK = pk_yeni([os.path.join(S, "gece", "m7", f) for f in ("v8x_b_rapor.txt", "v8x_c_rapor.txt")])
KK = {}
for b, L in PK.items():
    L = [q for q in L if any(q[2:8])]
    if L: KK[b] = ([q[0] for q in L], np.array([q[2:8] for q in L], float))


def ad_bul(dugum, lo, hi, e=0.6):
    b = dugum.split("__")[0]
    if b not in KK: return None
    ad, K = KK[b]
    ok = (lo[None, :] >= K[:, 0::2] - e).all(1) & (hi[None, :] <= K[:, 1::2] + e).all(1)
    if not ok.any(): return None
    v = np.prod(np.maximum(K[:, 1::2] - K[:, 0::2], .01), axis=1); v[~ok] = np.inf
    return ad[int(v.argmin())]


# istasyon tarafı Harting fiş + soket birbirine değdiği için tek bileşen olarak çıkıyor → iki kutunun birleşimiyle adlandır
HKUTU = {}
if "ELK_ANA_HAT" in KK:
    _ad, _K = KK["ELK_ANA_HAT"]
    for st in ("E", "K", "TOPPING"):
        ii = [i for i, a in enumerate(_ad) if a in ("harting_%s_fis" % st, "harting_%s_soket" % st)]
        if len(ii) == 2:
            k = _K[ii]; HKUTU[st] = np.array([k[:, 0].min(), k[:, 1].max(), k[:, 2].min(), k[:, 3].max(), k[:, 4].min(), k[:, 5].max()])


def ad_bul2(dugum, lo, hi, e=0.6):
    if dugum.startswith("ELK_ANA_HAT__rakor"):
        for st, k in HKUTU.items():
            if (lo >= k[0::2] - e).all() and (hi <= k[1::2] + e).all(): return "harting_%s_fis_soket" % st
    return ad_bul(dugum, lo, hi, e)


def kod_aralik(L, n):
    out = np.full(n, -1, np.int64)
    for k in range(0, len(L) - 2, 3): out[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = L[k]
    return out


# ------------------------------------------------------------------ sınıflama kuralları
KABLO = re.compile(r"kablo|harting|cat6a|_3g2|enerji_zinciri|(^|_)rakor|kanal|klemens|din_ray|sigorta|guc_kaynagi|(^|_)pano|(^|_)ups|^qrk_|giris_plakasi|^kuru_|^plc_|surucu_dikey", re.I)
SENSOR = re.compile(r"sensor|enkoder|encoder|reed|bayragi|miknatis|sensor_lami|yuk_hucresi|okuyucu|pt100|probu|d-m9n|smt-8m|kamera|barkod|termostat", re.I)
KAB2 = re.compile(r"kablo|harting|cat6a|_3g2|rakor|kanal|klemens|din_ray|sigorta|guc_kaynagi|(^|_)ups|^qrk_|giris_plakasi|enerji_zinciri|pano_kutusu|din_plakasi|soketi?$|_soket", re.I)
ISTK = {"TOPPING": "TOPPING", "F": "F", "K": "K", "E": "E", "DOLAP": "B", "QR": "QR", "A": "A", "ROBOT": "Robot", "B": "B"}
FONK_DISI = {"Elektrik", "Hava", "Soğutma", "Gövde"}
BELIRSIZ = []


def yeni(dugum, ad, mk, kt, lo, hi):
    """(eski mek kodu, eski kat kodu) → (yeni mek kodu, yeni kat kodu, gerekçe)"""
    ist, grp = mk.split("/", 1)
    a = ad or ""; nd = dugum.split("__")[0]; neden = ""
    # 1) grup adı / üst düzey taşımalar
    g = {"Pano": "Elektrik", "Hava dağıtımı": "Hava"}.get(grp, grp)
    if mk == "F/Kompresör": g = "Hava"
    if mk in ("F/Kutu yedeği", "U/Yedek stok"): ist, g, neden = "Çevre", "Ürün", "serbest ürün yığını"
    if mk == "U/Gövde" and nd == "U_F_HAVALANDIRMA": g = "Havalandırma"
    if mk == "A/Emniyet": g, neden = "Gövde", "A/Emniyet (13 üçgen, ön yüz)"
    if ist == "Robot":
        if mk == "Robot/Kablo + zincir":
            g = "Robot kolu" if nd.startswith("ROBOT_1") else "Yer rayı" if nd == "ROBOT_RAY" else "Elektrik"
        if a.startswith("qr_giris_plakasi"): ist, g = "QR", "Elektrik"
    if a.startswith("qr_giris_plakasi"): ist, g = "QR", "Elektrik"
    # 2) hat geneli Elektrik'ten istasyona ait olanlar
    if ist == "Elektrik":
        m = re.match(r"harting_(E|K|TOPPING)_(fis|soket|rakoru)", a)
        if m: ist, g, neden = ISTK[m.group(1)], "Elektrik", "istasyon tarafı Harting"
        elif a.startswith("E_harting_ic_kablo"): ist, g = "E", "Elektrik"
        elif a.startswith(("kablo_K_tarti", "rakor_G4_tarti")): ist, g, neden = "K", "Elektrik", "K tartı kablosu"
        elif a.startswith("UF_fan_"): ist, g, neden = "U", "Elektrik", "U_F fan kablosu"
    # 3) fonksiyonel ünitedeki kablo / pano / rakor → istasyonun Elektrik'i
    kablo = False
    if ist not in ("Elektrik", "Çevre", "Tezgâh"):
        isim_kablo = bool(KABLO.search(a)) and not re.search(r"soketi?$|_soket$", a)
        if a and kt in ("GUC", "KONTROL", "MOTOR") and isim_kablo: kablo = True
        if a.startswith("f_ust_rakor_"): kablo = True
        if not a and nd.startswith("ELK_") and kt in ("GUC", "KONTROL"): kablo = True
        if a.startswith(("motor_kablosu_", "PulsaJet_M8_kablo")) or a == "tahrik_rulosu_EC5000_kablo": kablo = True
        if kablo:
            m = re.match(r"(?:kablo|harting|rakor)_(TOPPING|F|K|E|DOLAP|QR|A|ROBOT)_", a)
            if m and ist != "Robot": ist = ISTK[m.group(1)]
            if g != "Elektrik": neden = neden or "kablo/pano → Elektrik"
            g = "Elektrik"
    # 4) hava hortumu → istasyonun Hava'sı
    if a.startswith(("hava_hortumu", "vakum_dagitim_hatti")) and g not in ("Hava",): g, neden = "Hava", "hava hortumu → Hava"
    # 5) disiplin
    k = kt
    if kt == "GUC": k = "ELEKTRIK"
    tesisat = bool(KAB2.search(a)) or a.startswith("f_ust_rakor_") or (not a and nd.startswith("ELK_"))
    if kt in ("KONTROL", "MOTOR") and tesisat: k = "ELEKTRIK"      # sürücü / PLC cihazı kendi disiplininde kalır, kablosu Elektrik
    elif kt == "KONTROL" and SENSOR.search(a): k = "SENSOR"
    elif kt == "KONTROL" and re.search(r"_soketi?$|_soket$", a): k = "ELEKTRIK"
    elif kt == "KONTROL" and not a and g not in FONK_DISI and ist not in ("Elektrik", "QR", "F"):
        k = "SENSOR"; BELIRSIZ.append(("adsız KONTROL → SENSOR", dugum, mk, lo.round(1).tolist(), hi.round(1).tolist()))
    if re.search(r"d-m9n|smt-8m|yuk_hucresi|pt100|probu|termostati", a, re.I) and kt not in ("URUN",) and not tesisat: k = "SENSOR"
    if a.startswith("ust_f_fan_termostat_rayi"): k = "ELEKTRIK"
    if ist == "Elektrik" and g == "Ana hat" and kt in ("KONTROL", "MOTOR"): k = "ELEKTRIK"   # ana hat = yalnız kablo + kanal (veri kabloları KONTROL işaretliydi)
    if a.startswith(("f_ust_rakor_",)): k = "ELEKTRIK"
    if a == "ana_pano_ceyrek_tur_kilit": k = "ELEKTRIK"
    # QR göz braketleri (montaj ağında GUC işaretli mekanik parçalar)
    if ist == "QR" and g in ("Gözler", "Gövde") and kt == "GUC" and not kablo:
        k = "MOTOR" if "motor_braketi" in a else ("GOVDE" if g == "Gövde" else "MEKANIZMA")
    if ist == "Robot" and g in ("Robot kolu", "Yer rayı") and kt in ("GUC", "KONTROL"): k = "ELEKTRIK"
    if ist == "A" and g == "Elektrik": g, neden = "Gövde", "A/Elektrik sıfır alanlı artık (görünmez)"
    return ist + "/" + g, k, neden


# ------------------------------------------------------------------ parçalar (primitive içi bağlı bileşen, aynı mek)
PRIM = []; ESL = []
for ni, nd in enumerate(J["nodes"]):
    if "mesh" not in nd or ni not in W: continue
    M = W[ni]
    for pi, pr in enumerate(J["meshes"][nd["mesh"]]["primitives"]):
        T = acc(pr["indices"]).reshape(-1, 3).astype(np.int64); n = len(T)
        X = acc(pr["attributes"]["POSITION"]).astype(float)
        Xw = (X @ M[:3, :3].T + M[:3, 3]) * 1000.0
        ex = pr.get("extras", {}) or {}
        mek = kod_aralik(ex.get("mek") or [], n); kat = kod_aralik(ex.get("kat") or [], n)
        assert (mek >= 0).all() and (kat >= 0).all(), nd["name"]
        u, inv = np.unique(np.round(X, 7), axis=0, return_inverse=True); inv = inv.reshape(-1)
        ul, li = np.unique(mek, return_inverse=True)
        Vi = inv[T] * len(ul) + li[:, None]
        uv, vv = np.unique(Vi.reshape(-1), return_inverse=True); vv = vv.reshape(-1, 3)
        r_ = np.concatenate([vv[:, 0], vv[:, 1]]); c_ = np.concatenate([vv[:, 1], vv[:, 2]])
        _, cl = connected_components(coo_matrix((np.ones(len(r_)), (r_, c_)), shape=(len(uv), len(uv))), directed=False)
        tc = cl[vv[:, 0]]
        uc, tci = np.unique(tc, return_inverse=True)
        ymek = np.empty(n, np.int64); ykat = np.empty(n, np.int64)
        P = Xw[T]
        for j in range(len(uc)):
            m = np.where(tci == j)[0]; Q = P[m].reshape(-1, 3); lo, hi = Q.min(0), Q.max(0)
            mk = EMEK[mek[m[0]]]
            kc = collections.Counter(kat[m].tolist())
            ad = ad_bul2(nd["name"], lo, hi)
            # bileşen içinde birden çok kat varsa her biri ayrı sınıflanır (ör. kablo + kelepçe aynı ağda)
            for kv, cnt in kc.items():
                mm = m[kat[m] == kv]
                yk_m, yk_k, neden = yeni(nd["name"], ad, mk, EKAT[kv], lo, hi)
                ymek[mm] = YMI[yk_m]; ykat[mm] = YKI[yk_k]
                ESL.append(dict(prim=len(PRIM), dugum=nd["name"], ad=ad, ntri=int(len(mm)), eski_mek=mk, eski_kat=EKAT[kv],
                                yeni_mek=yk_m, yeni_kat=yk_k, neden=neden, lo=lo.round(1).tolist(), hi=hi.round(1).tolist()))
        PRIM.append(dict(ni=ni, mi=nd["mesh"], pi=pi, n=n, ymek=ymek, ykat=ykat, ad=nd["name"]))


def kodla(a):
    out = []; s = 0
    for i in range(1, len(a) + 1):
        if i == len(a) or a[i] != a[s]:
            out += [int(a[s]), s * 3, (i - s) * 3]; s = i
    return out


# ------------------------------------------------------------------ yaz
tot_eski = tot_yeni = 0
for p in PRIM:
    pr = J["meshes"][p["mi"]]["primitives"][p["pi"]]
    ic = J["accessors"][pr["indices"]]["count"]
    km, kk = kodla(p["ymek"]), kodla(p["ykat"])
    for L in (km, kk):
        assert sum(L[2::3]) == ic and L[1] == 0 and all(L[3 * i + 1] + L[3 * i + 2] == L[3 * i + 4] for i in range(len(L) // 3 - 1)), p["ad"]
    tot_eski += ic; tot_yeni += sum(km[2::3])
    pr.setdefault("extras", {})["mek"] = km; pr["extras"]["kat"] = kk
assert tot_eski == tot_yeni
EX["mekanizmalar"] = YMEK; EX["kategoriler"] = YKAT
EX["gruplama"] = "v1 · 3 Eki 2026 · IEC 81346: mek = montaj ağacı (istasyon/ünite), kat = disiplin (SENSOR ayrı, GUC+kablolar=ELEKTRIK)"
js = json.dumps(J, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
js += b" " * ((4 - len(js) % 4) % 4)
binc = raw[bo:]
out = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + len(binc)) + struct.pack("<II", len(js), 0x4E4F534A) + js + binc
open(CIKIS, "wb").write(out)
print("GLB:", CIKIS, len(out), "bayt · indis toplamı", tot_eski, "=", tot_yeni)

json.dump(dict(giris=os.path.basename(GIRIS), cikis=os.path.basename(CIKIS), mek=YMEK, kat=[k["kod"] for k in YKAT], parca=ESL, belirsiz=BELIRSIZ),
          open(os.path.join(HERE, "esleme.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(len(ESL), "parça kaydı ·", sum(1 for e in ESL if e["ad"]), "adlı · belirsiz", len(BELIRSIZ))

# ------------------------------------------------------------------ sayfa ağacı tablosu (mekanizma_v3_8.json)
ESKI_JSON = os.path.join(S, "..", "..", "..", "..", "..", "..", "Desktop", "Kemal", "WEBSİTE", "AUTOKITCH_COORDINATION", "worktrees",
                         "claude-hat3-v8", "otonom", "hat3d", "v3", "mekanizma_v3.json")
ESKI_JSON = sys.argv[3] if len(sys.argv) > 3 else r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\adim9\is\_v7\mekanizma_v3.json"
D0 = json.load(open(ESKI_JSON, encoding="utf-8"))
kutu = {}; parca_t = collections.defaultdict(collections.Counter)
for e in ESL:
    lo, hi = np.array(e["lo"]) / 1000.0, np.array(e["hi"]) / 1000.0
    if e["ad"]: parca_t[e["dugum"].split("__")[0] + "|" + e["ad"]][e["yeni_mek"]] += e["ntri"]
    if not (hi - lo > 1e-6).any() or e["ntri"] < 2: continue          # sıfır boyutlu / gizli artıklar kamerayı bozmasın
    k = kutu.get(e["yeni_mek"])
    b = [lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]]
    kutu[e["yeni_mek"]] = b if k is None else [min(k[0], b[0]), max(k[1], b[1]), min(k[2], b[2]), max(k[3], b[3]), min(k[4], b[4]), max(k[5], b[5])]
YEN = {"Pano": "Elektrik", "Hava dağıtımı": "Hava", "Kompresör": "Hava"}
def yeni_kod(k):
    i, g = k.split("/", 1); k2 = i + "/" + YEN.get(g, g)
    if k in ("F/Kutu yedeği", "U/Yedek stok"): k2 = "Çevre/Ürün"
    if k == "Robot/Kablo + zincir": k2 = "Robot/Elektrik"
    if k in ("A/Emniyet", "A/Elektrik"): k2 = "A/Gövde"
    return k2 if k2 in YMI else "Çevre/Ürün"
D1 = dict(surum="v3_8 gruplama v1 (3 Eki 2026) · IEC 81346 · mek = montaj ağacı, kat = disiplin", glb="hat3_v8.glb (v8zb)",
          istasyon=D0["istasyon"], liste=YMEK, parca={k: c.most_common(1)[0][0] for k, c in parca_t.items()},
          birim={b: yeni_kod(k) for b, k in D0["birim"].items()}, aralik={}, kapak={},
          kutu={k: [round(float(x), 4) for x in v] for k, v in kutu.items()}, kapsam=D0.get("kapsam"))
json.dump(D1, open(os.path.join(HERE, "mekanizma_v3_8.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("mekanizma_v3_8.json:", len(D1["liste"]), "ünite ·", len(D1["parca"]), "adlı parça ·", len(D1["kutu"]), "kutu")
