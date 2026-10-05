# -*- coding: utf-8 -*-
"""K v11 denetimi (30 Eyl 2026 · Claude) — v10 denetiminin tamamı + v10 ↔ v11 parça parça + teneke çıkarma 0 → 900 mm + ön boşluk + raf yükü
Kemal: "bunu geriye en gidebileceği kadar it ki ben ön tarafa da bir şeyler koyabileyim"
K v10 denetimi — v9 denetiminin tamamı (yağ sistemi v10: sıvı yağ tenekesi) + teneke çıkarma taraması + yağ hattı hesapları
1 · katılar geçerli · 2 · durağan (bütün parçalar evde) kesişim > 0,5 mm³ — İSTİSNASIZ · 3 · hareket taraması: hareketli gruplar ↔ her şey (0,1 s + olay anları)
4 · ürün yolu: Ø300 × 15 disk ↔ bütün parçalar · 5 · bağlantı (0,25 mm: havada parça) · 6 · kütleler → zaman denetimi
7 · v10 ↔ v11: yalnız yağ sistemi değişir (başka her parça ad · malzeme · grup · hacim · zarf AYNI)
Çıktı: _local/k-v11/denetim.json · 'hizli' → 3 ve 5 atlanır"""
import json, sys, time, hashlib, math
from pathlib import Path
import cadquery as cq

t0 = time.time()
# 7a · v10 anlık görüntüsü (v11 içe aktarılınca v10 modül değişkenleri v11 değerlerine döner — önce v10 kurulur)
import kesme_cad_v10 as K10
K10.modul()
ONCE = {}
for p in K10.PARCALAR:
    s = p["wp"].val(); b = s.BoundingBox()
    ONCE[p["ad"]] = dict(mal=p["mal"], grup=p["grup"], v=s.Volume(), bb=(b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))
import kesme_cad_v11 as K

K.modul()
P = {p["ad"]: p for p in K.PARCALAR}
assert len(P) == len(K.PARCALAR), "ad tekrar"
S = {n: p["wp"].val() for n, p in P.items()}
OUT = Path(__file__).resolve().parents[2] / "_local" / "k-v11"; OUT.mkdir(parents=True, exist_ok=True)
R = dict(kaynak_sha256=hashlib.sha256(Path(K.__file__).read_bytes()).hexdigest(), parca=len(P), gecersiz=[n for n, s in S.items() if not s.isValid()],
         bomsuz=[], durgun=[], hareket=[], urun=[], yakin={}, havada=[], kutle={}, zaman=None)
print("K v11 · %d parça (v10 %d) · geçersiz %d %s · %.0f s" % (len(P), len(ONCE), len(R["gecersiz"]), R["gecersiz"][:5], time.time() - t0), flush=True)

# 7b · v10 ↔ v11
cikan = sorted(set(ONCE) - set(P)); eklenen = sorted(set(P) - set(ONCE)); degisen, beklenmeyen = [], []
for n in sorted(set(P) & set(ONCE)):
    s = S[n]; b = s.BoundingBox(); o = ONCE[n]
    zarf = max(abs(u - v) for u, v in zip((b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax), o["bb"]))
    if P[n]["mal"] != o["mal"] or P[n]["grup"] != o["grup"] or zarf > 0.01 or abs(s.Volume() - o["v"]) > 0.01:
        degisen.append(n)
        if not n.startswith("yag_"): beklenmeyen.append(n)
R["v10_v11"] = dict(cikan=cikan, eklenen=eklenen, degisen=degisen, beklenmeyen=beklenmeyen)
ok7 = not cikan and sorted(eklenen) == sorted(K.V11_YENI) and not beklenmeyen and set(degisen) <= set(K.V11_DEGISEN)
print("   7 · v10 ↔ v11: çıkan %s · eklenen %s · değişen %d (yağ sistemi) · beklenmeyen %s → %s" % (cikan, eklenen, len(degisen), beklenmeyen, "TEMİZ" if ok7 else "BULGU"), flush=True)

GRUPSUZ = ("SPREY", "URUN", "URUN_IZ", "REF")
names = [n for n in P if P[n]["grup"] not in GRUPSUZ]
BB = {n: S[n].BoundingBox() for n in names}


def bbk(a, b, pay=0.05):
    return not (a.xmin >= b.xmax - pay or b.xmin >= a.xmax - pay or a.ymin >= b.ymax - pay or b.ymin >= a.ymax - pay or a.zmin >= b.zmax - pay or b.zmin >= a.zmax - pay)


for i, a in enumerate(names):
    for b in names[i + 1:]:
        if not bbk(BB[a], BB[b]): continue
        v = S[a].intersect(S[b]).Volume()
        if v > 0.5:
            R["durgun"].append([a, b, round(v, 2)])
print("   DURGUN kesişim: %d %s" % (len(R["durgun"]), R["durgun"][:30]), flush=True)

HAREKETLI = ("KESICI", "ITICI_ARABA", "ITICI_CAPRAZ", "ITICI_KOL", "ITICI_YUZ")


def konum(n, t):
    g = P[n]["grup"]
    if g in HAREKETLI:
        d = K.grup_trs(g, t)
        return S[n].moved(cq.Location(cq.Vector(*d))) if any(abs(c) > 1e-9 for c in d) else S[n]
    return S[n]


if "hizli" not in sys.argv:
    anlar = sorted(set([round(i * 0.1, 3) for i in range(int(K.DONGU * 10) + 1)] + list(getattr(K, "OLAY_ANLARI", ()))))
    hn = [n for n in names if P[n]["grup"] in HAREKETLI]
    ILK = set()
    for t in anlar:
        M = {n: konum(n, t) for n in names}
        MB = {n: (M[n].BoundingBox() if P[n]["grup"] in HAREKETLI else BB[n]) for n in names}
        for a in hn:
            for b in names:
                if a == b or P[a]["grup"] == P[b]["grup"]: continue
                if P[b]["grup"] in HAREKETLI and b < a: continue
                if not bbk(MB[a], MB[b]): continue
                v = M[a].intersect(M[b]).Volume()
                if v > 0.5:
                    R["hareket"].append([t, a, b, round(v, 2)])
                    if (a, b) not in ILK:
                        ILK.add((a, b)); print("      HAREKET %s ↔ %s %.1f mm³ (t %.2f)" % (a, b, v, t), flush=True)
    print("   HAREKET taraması: %d kayıt · %d çift · %.0f s" % (len(R["hareket"]), len(ILK), time.time() - t0), flush=True)

GECIS = ("bant_PU_ust", "bant_sarim_354", "olu_plaka", "kayma_tablasi", "tahrik_rulosu_EC5000_354", "bant_traversi_0", "bant_traversi_1")


def beklenen(n, t, x):
    return (n.startswith("bicak_") and K.Z_KES[0] <= t <= K.Z_KES[3]) or (x > K.X_INIS[0] and n in GECIS)


R["urun_beklenen"] = []
ILK = set()
for i in range(int(K.DONGU * 20) + 1):
    t = i * 0.05
    x, y, z = K.urun_merkez(t)
    if x < -200: continue
    disk = cq.Solid.makeCylinder(K.PZ_R, K.PZ_H, cq.Vector(x, y, z), cq.Vector(0, 1, 0))
    db = disk.BoundingBox()
    for n in names:
        sh = konum(n, t)
        if not bbk(db, sh.BoundingBox()): continue
        v = disk.intersect(sh).Volume()
        if v > 0.5 and beklenen(n, t, x):
            R["urun_beklenen"].append([round(t, 2), n, round(v, 2), round(996.0 - y, 2)])
            continue
        if v > 0.5:
            R["urun"].append([round(t, 2), n, round(v, 2)])
            if n not in ILK:
                ILK.add(n); print("      ÜRÜN ↔ %s %.1f mm³ (t %.2f · x %.0f)" % (n, v, t, x), flush=True)
print("   ÜRÜN yolu: %d kayıt · %d parça · beklenen temas %d" % (len(R["urun"]), len(ILK), len(R["urun_beklenen"])), flush=True)

if "hizli" not in sys.argv:
    graph = {n: set() for n in names}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            A, B_ = BB[a], BB[b]
            if any(getattr(A, k + "min") > getattr(B_, k + "max") + .25 or getattr(B_, k + "min") > getattr(A, k + "max") + .25 for k in "xyz"): continue
            if S[a].distance(S[b]) <= .25: graph[a].add(b); graph[b].add(a)
    todo = set(names); comps = []
    while todo:
        found = set(); stack = [next(iter(todo))]
        while stack:
            n = stack.pop()
            if n in found: continue
            found.add(n); stack.extend(graph[n] - found)
        todo -= found; comps.append(sorted(found))
    comps.sort(key=len, reverse=True)
    R["havada"] = comps[1:]
    R["raf_komsu"] = {n: sorted(graph[n]) for n in ("yag_pompa_rafi", "yag_pompa_rafi_kosebendi_sol", "yag_pompa_rafi_kosebendi_sag", "yag_pompa_plakasi", "yag_basinc_sensoru_PM1704")}
    print("   BAĞLANTI: bileşen boyları %s · havada %s" % ([len(c) for c in comps][:8], comps[1:12]), flush=True)
    print("   raf / köşebent / plaka / sensör komşuları: %s" % R["raf_komsu"], flush=True)

R["kutle"] = K.grup_kutleleri() if hasattr(K, "grup_kutleleri") else {}
if hasattr(K, "zaman_denetimi"):
    R["zaman"] = K.zaman_denetimi()
    R["sprey"] = K.sprey_ozeti()
    print("   ZAMAN: %s" % R["zaman"], flush=True)

# ---------------------------------------------------------------- v10 / v11 · YAĞ BESLEMESİ ----------------------------------------------------------------
V = {}
# 1 · teneke çıkarma: kapak açık, teneke + emme borusu + ağız adaptörü öne çekilir (emiş / dönüş hortumu esnek → birlikte gelir), 0 → 900 mm (teneke kapaktan tamamen çıkar)
TEN = ("yag_tenekesi_18L", "yag_emme_lansi_1038304", "yag_agiz_adaptoru")
ESNEK = ("yag_emis_hortumu_TLM1008", "yag_donus_hortumu_TLM0806")
KAPAK = [n for n in names if n.startswith("onyuz_kapak_alt")]
sab = [n for n in names if n not in TEN + ESNEK and n not in KAPAK and P[n]["grup"] == "SABIT"]
bul = []
BOY = int(math.ceil((79.0 - BB["yag_tenekesi_18L"].zmin) / 10.0) * 10)
for dz in range(10, BOY + 1, 10):
    for a in TEN:
        m = S[a].moved(cq.Location(cq.Vector(0.0, 0.0, float(dz)))); mb = m.BoundingBox()
        for b in sab:
            if not bbk(mb, BB[b]): continue
            v = m.intersect(S[b]).Volume()
            if v > 0.5: bul.append([dz, a, b, round(v, 1)])
V["teneke_cikarma"] = dict(adim=10, boy=BOY, kapak=KAPAK, bulgu=bul[:20], n=len(bul))
print("   TENEKE ÇIKARMA (kapak açık · teneke + emme borusu + adaptör 0 → %d mm öne, kapak düzleminin dışına): %d bulgu %s" % (BOY, len(bul), bul[:6]), flush=True)
_tk = BB["yag_tenekesi_18L"]; _ka = BB["onyuz_kayit_140_42"]; _ku = BB["onyuz_kayit_877_42"]
V["kapak_acikligi"] = dict(teneke_y=(round(_tk.ymin, 1), round(BB["yag_agiz_adaptoru"].ymax, 1)), alt_kayit_ust=round(_ka.ymax, 1), ust_kayit_alt=round(_ku.ymin, 1),
                           teneke_x=(round(_tk.xmin, 1), round(_tk.xmax, 1)))
# 2 · teneke nerede · arka kayıta pay · ön boşluk
_ak = BB["onyuz_kayit_140_-800"]
V["yerlesim"] = dict(teneke_z=(round(_tk.zmin, 1), round(_tk.zmax, 1)), tava_z=(round(BB["yag_damlama_tavasi_10"].zmin, 1), round(BB["yag_damlama_tavasi_10"].zmax, 1)),
                     tava_arka_kayit_payi=round(BB["yag_damlama_tavasi_10"].zmin - _ak.zmax, 2), on_bosluk=K.on_bosluk(),
                     raf=dict(y_ust=K.RAF["y"] + K.RAF["t"], z=K.RAF["z"]), agiz=K.TNK_AGIZ)
print("   YERLEŞİM: %s" % V["yerlesim"], flush=True)
# 3 · raf yükü: pompa grubu kütlesi (CAD hacmi × yoğunluk) · 1,5 mm raf + 20 mm ön kıvrım, iki köşebent arası basit mesnet (yayılı yük) → sehim
GRUP = ("yag_pompa_plakasi", "yag_emis_filtresi", "yag_boru_filtre_pompa", "yag_pompasi_GJ-N21_EagleDrive", "yag_boru_pompa_T", "yag_T_parcasi",
        "yag_basinc_sensoru_PM1704", "yag_boru_T_regulator", "yag_geri_basinc_regulatoru_KBP")
YG = getattr(K, "YOGUNLUK", {})
m_grup = sum(S[n].Volume() * YG.get(P[n]["mal"], 7.9e-6) for n in GRUP)
m_grup = max(m_grup, 0.0) + 1.1 - S["yag_geri_basinc_regulatoru_KBP"].Volume() * YG.get(P["yag_geri_basinc_regulatoru_KBP"]["mal"], 7.9e-6)   # KBP katalog 1,1 kg
L_ = K.RAF["x"][1] - K.RAF["x"][0] - 2 * 27.0                                            # köşebent yatay kolları arası açıklık
t_, k_ = K.RAF["t"], K.RAF["kenar"]
# ön kıvrım + ona kaynaklı 40 mm raf şeridi (L kesit) · I çevresel eksende
A1, y1 = k_ * t_, k_ / 2.0 + t_; A2, y2 = 40.0 * t_, t_ / 2.0
yc = (A1 * y1 + A2 * y2) / (A1 + A2)
I_ = t_ * k_ ** 3 / 12.0 + A1 * (y1 - yc) ** 2 + 40.0 * t_ ** 3 / 12.0 + A2 * (y2 - yc) ** 2
w_ = m_grup * 9.81 / L_
sehim = 5.0 * w_ * L_ ** 4 / (384.0 * 193000.0 * I_)                                     # E 304 = 193 GPa · yarı yük öne binse de yalnız ön kıvrım taşısın (güvenli taraf)
V["raf_yuku"] = dict(pompa_grubu_kg=round(m_grup, 2), aciklik_mm=round(L_, 1), I_mm4=round(I_, 0), sehim_mm=round(sehim, 3))
print("   RAF YÜKÜ: %s" % V["raf_yuku"], flush=True)
# 4 · yağ hattı hesapları (v10 ile aynı yöntem · yeni hat boyu)
Y = K.YAG; Tn = K.TENEKE
q_noz = 0.757 * math.sqrt(1.0 / Y["rho"]); g_s = q_noz * Y["rho"] * 1000.0 / 60.0
L_bas = K._boy(K.H_BASINC) / 1000.0
dp = {t2: 32.0 * (mu_ / 1000.0) * (1.0 / 60000.0 / (math.pi * 0.004 ** 2)) * L_bas / 0.008 ** 2 / 1e5 for t2, mu_ in ((15, Y["mu15"]), (25, Y["mu25"]), (40, Y["mu40"]))}
bpr = 2.76 + dp[15]
n_pompa = 1.0 / 0.316e-3
gun = {"80 pide": 80 * 8.0 / 1000.0, "280 ürün": 280 * 8.0 / 1000.0}
kutle = dict(teneke_brut=Tn["net_kg"] + Tn["bos_kg"], platform=round(S["yag_tarti_platformu"].Volume() * 7.9e-6, 2),
             lans_adaptor=round((S["yag_emme_lansi_1038304"].Volume() + S["yag_agiz_adaptoru"].Volume()) * 1.4e-6, 2))
yuk = kutle["teneke_brut"] + kutle["platform"] + kutle["lans_adaptor"]
V["hat"] = dict(nozul_L_dk=round(q_noz, 3), nozul_g_s=round(g_s, 1), basinc_hatti_m=round(L_bas, 2), emis_hatti_m=round(K._boy(K10._yol(K.H_EMIS)) / 1000.0, 2),
                donus_hatti_m=round(K._boy(K10._yol(K.H_DONUS)) / 1000.0, 2), kayip_bar={k2: round(v2, 2) for k2, v2 in dp.items()},
                regulator_bar=round(bpr, 2), pompa_d_dk_1L=round(n_pompa), tarti_yuk_kg=round(yuk, 2), teneke_gun={k2: round(Tn["net_kg"] / v2, 1) for k2, v2 in gun.items()})
V["ok"] = (not bul and bpr <= 6.8 and n_pompa <= 5500 and yuk <= 50.0 * 0.6 and K.R_1008 >= 65.0 and K.R_0806 >= 40.0
           and _tk.xmin >= _ka.xmin and _tk.xmax <= _ka.xmax and _tk.ymin >= _ka.ymax and BB["yag_agiz_adaptoru"].ymax <= _ku.ymin
           and V["yerlesim"]["tava_arka_kayit_payi"] >= 0.5 and V["yerlesim"]["on_bosluk"]["derinlik"] >= 450.0 and sehim <= 1.0)
print("   YAĞ HATTI: %s" % V["hat"], flush=True)
print("   v11 YAĞ: %s" % ("GEÇTİ" if V["ok"] else "KALDI"), flush=True)
R["v11"] = V
(OUT / "denetim.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
ok = (not R["gecersiz"] and not R["durgun"] and not R["hareket"] and not R["urun"] and not R["havada"] and (R["zaman"] is None or R["zaman"].get("ok"))
      and R["v11"]["ok"] and ok7)
print("K v11 DENETİM: %s · geçersiz %d · durgun %d · hareket %d · ürün %d · havada %d · v10↔v11 %s · %.0f s" % ("GEÇTİ" if ok else "KALDI", len(R["gecersiz"]), len(R["durgun"]),
      len(R["hareket"]), len(R["urun"]), len(R["havada"]), ok7, time.time() - t0), flush=True)
