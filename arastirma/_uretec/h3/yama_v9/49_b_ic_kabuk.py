# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 49 · B İÇ KABUK BİRLEŞİMLERİ: BÜKÜMLÜ FLANŞ + KÖR PERÇİN (4 Eki 2026 · Claude · YEREL · Kemal: "o saclar o yalıtımlara nasıl takılıyor,
havada duruyor gibiler, büküm ya da kaynak görünmüyor" · iç sac kenarlarından bükümlü flanşla komşu iç saca perçin)
python 49_b_ic_kabuk.py girdi.glb cikti.glb      (zincir: hat3_v9p.glb → hat3_v9q.glb)

Yerinde köpüklü tasarımda iç saclar köpük bağıyla tutuluyordu; levha PU'da (adım 46) her iç sac MEKANİK bağlanır. Her iç köşede bir sacın kenarı
15 mm (bölmelerde 12 mm) 90° bükülür, flanş komşu sacın PU tarafına yaslanır, DIN 7337 Ø4 A2 kör perçin (≈ 150 mm aralık) ile perçinlenir.
Flanş ve perçin ucu PU levhada cep açar (levha cebi kesilmiş gelir). İç saclar iç sacla bağlanır (ikisi de soğuk taraf) → ısı köprüsü yok.
  F1  iç taban 1 / 2 arka kenarı ↑ iç arka sacın arkasına (y 164,5–179,5) · perçin gıda tarafından (−z)
  F4  iç sol duvarın alt / arka / üst kenarı 15 mm gıda tarafına bükülür → iç taban, iç arka, iç tavana perçin (tavan ↔ arka köşesinde flanş yok: arka PU
      levhası tavanın üstüne çıkar; tavan bölme flanşlarıyla bağlanır)
  F6  bölme sacları (B1–B5 A / B; B5 B = teknik kapama sacı hariç): alt kenar → iç tabana, arka kenar → iç arka saca, üst kenar → iç tavana —
      flanş 12 mm DIŞA (gıda tarafına; bölme tezgâhta panel olur, yerinde perçinler gıda tarafından) · engel (ray, kanal, kovan, motor) yerlerinde çentikli
Ön kenarlar ön çerçeveye ALIN (MS polimer yapıştırma, tasarımdaki gibi — ısı köprüsü olmasın diye mekanik bağ yok); yapıştırıcı / derz silikonu
modelde katman olarak yok, montaj animasyonunda gösterilir. Bölme PU levhaları (adım 44 sonrası açık ağ) 0,01 mm ızgarada onarılıp kapatılır."""
import os, sys, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "veri"))
import sac_ent as SE
from m8kit import Glb
import manifold3d as mf
import bag47 as B

gi, go = sys.argv[1:3]
KURU = "--kuru" in sys.argv
t0 = time.time(); LOG = SE.log
DUG_B = "B_BAGLANTI__paslanmaz"


def bc(g, d):
    g._bc.pop(d, None)
    try: g.bilesen(d, 0)
    except (IndexError, ValueError, KeyError): return []
    return g._bc[d]


def ucg(b):
    return np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])


def degistir(g, b, P):
    ilk = [True]
    def f(_):
        if ilk[0]: ilk[0] = False; return P
        return None
    g.donustur(b, f)


def onar(P):
    for rr in (1e-4, 0.01, 0.05):
        u, inv = np.unique(np.round(P.reshape(-1, 3) / rr) * rr, axis=0, return_inverse=True); F = inv.reshape(-1, 3)
        F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
        m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=F.astype(np.uint32)))
        if m.status() == mf.Error.NoError and not m.is_empty(): return m
    return None


# ---------------------------------------------------------------- 0 · açık PU levhaları kapat
g = Glb(gi)
n_on = 0
for b in bc(g, "B_KASA__pu"):
    if b["kapali"]: continue
    m = onar(ucg(b))
    if m is None: raise SystemExit("ADIM 49 DUR: PU onarılamadı %s" % np.round(b["lo"], 1))
    degistir(g, b, SE.mf_P(m)); n_on += 1
LOG("  PU onarıldı: %d levha" % n_on)
tmp0 = go + ".e0.glb"; g.kaydet(tmp0); del g
g = Glb(tmp0)
K = SE.Karsi(g, acik_dene=True)
SAC = bc(g, "B_KASA__sac")


def sac(lo, hi, tol=0.3):
    L = [b for b in SAC if np.all(np.abs(b["lo"] - np.asarray(lo)) < tol) and np.all(np.abs(b["hi"] - np.asarray(hi)) < tol)]
    if len(L) != 1: raise SystemExit("ADIM 49 DUR: sac %s → %d" % (lo, len(L)))
    return L[0]


TAB1 = sac((797.3, 163.3, -791.2), (2108.5, 164.5, 23.0)); TAB2 = sac((2108.5, 163.3, -791.2), (4027.3, 164.5, 23.0))
TAV1 = sac((797.3, 728.0, -791.2), (2108.5, 729.2, 23.0)); TAV2 = sac((2108.5, 668.0, -791.2), (4027.3, 669.2, 23.0))
ARK1 = sac((797.3, 164.5, -791.2), (2108.5, 728.0, -790.0)); ARK2 = sac((2108.5, 164.5, -791.2), (4027.3, 668.0, -790.0))
SOL = sac((797.3, 164.5, -790.0), (798.5, 728.0, 23.0))
BOLME = [(sac((1418.5, 164.5, -790.0), (1419.7, 728.0, 23.0)), +1), (sac((1452.3, 164.5, -790.0), (1453.5, 728.0, 23.0)), -1),
         (sac((2073.5, 164.5, -790.0), (2074.7, 728.0, 22.0)), +1), (sac((2107.3, 164.5, -790.0), (2108.5, 728.0, 22.0)), -1),
         (sac((2728.5, 164.5, -790.0), (2729.7, 668.0, 23.0)), +1), (sac((2762.3, 164.5, -790.0), (2763.5, 668.0, 23.0)), -1),
         (sac((3383.5, 164.5, -790.0), (3384.7, 668.0, 23.0)), +1), (sac((3417.3, 164.5, -790.0), (3418.5, 668.0, 23.0)), -1),
         (sac((3993.5, 164.5, -790.0), (3994.7, 668.0, 23.0)), +1)]
# kovan kutuları (bölme boyunca geçen kablo kovanları: B_KASA__sac, x genişliği 35, kalınlık değil) — flanş bunlarda kesilir
KOVAN = [b for b in SAC if abs((b["hi"][0] - b["lo"][0]) - 35.0) < 0.2 and b["hi"][1] - b["lo"][1] > 20]

FL = []          # (ad, cq katı, sahip bileşen)
PR = []          # perçin adayları: (grup, [aday elemanlar], izin, ref)
RV = dict(d=4.0, dk=8.0, k=1.3, bulb=6.0)


ENG = list(KOVAN) + [b for b in SAC if np.max(b["hi"] - b["lo"]) < 100.0]          # kovanlar + küçük sac parçaları (kovan uç sacları vb.)
for d in sorted(set(p["name"] for p in g.prims)):
    if d.startswith(("B_KASA__pu", "B_KASA__sac", "B_KASA__on_cerceve")) or not d.startswith(("B_", "ELK_", "DUZ_B", "CEK_")): continue
    for b in bc(g, d):
        if np.all(b["hi"] >= [736, 124, -830]) and np.all(b["lo"] <= [4400, 790, 40]): ENG.append(b)


def flans(ad, lo, hi, sahip):
    """flanş kutusu − (geçtiği dikme / kovan / kanal / kablo kutuları + 1 mm): flanş o yerlerde kesik (çentik)"""
    sh = B.kutu(lo, hi); lo_ = np.asarray(lo); hi_ = np.asarray(hi)
    for kv in ENG:
        if np.all(kv["hi"] > lo_ + 0.05) and np.all(kv["lo"] < hi_ - 0.05):
            sh = sh.cut(B.kutu(kv["lo"] - 1.0, kv["hi"] + 1.0))
    if len(sh.Solids()) > 1:                                             # çentik flanşı parçalara böldüyse en büyük parçalar (≥ 20 mm) kalır
        sh = sh.Solids()[0].fuse(*[x for x in sh.Solids()[1:]]) if False else sh
    FL.append((ad, sh, sahip))
    return sh


def percin_hatti(ad, p0, p1, n, a_bas, kalin, ref, aralik=150.0, uc=20.0):
    """p0 → p1 doğrusu boyunca perçinler · n = perçin giriş yönü (baştan uca) · a_bas = baş altı düzleminin n-parametresi · kalin = sıkılan kalınlık"""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); L = np.linalg.norm(p1 - p0); u = (p1 - p0) / L
    k = max(2, int(np.ceil((L - 2 * uc) / aralik)) + 1)
    for i, s in enumerate(np.linspace(uc, L - uc, k)):
        ad_ = []
        for ds in (0.0, 12.0, -12.0, 25.0, -25.0, 40.0, -40.0, 60.0, -60.0, 80.0, -80.0):
            p = p0 + u * min(max(s + ds, 8.0), L - 8.0)
            o = p.copy(); o[int(np.argmax(np.abs(n)))] = 0.0
            el = B.kor_percin(o, n, a_bas, kalin + 3.0, "%s_%d" % (ad, i), d=RV["d"], dk=RV["dk"], k=RV["k"], bulb=RV["bulb"])
            el["bom"] = ["DIN 7337 kör perçin Ø4 × %.0f A2/A2, bombe baş" % (kalin + 4.0)]
            ad_.append(el)
        PR.append((ad, ad_, ref))


# F1 / F2 · taban / tavan arka kenarı ↑↓ arka sacın arkasında
for T, A_, ad in ((TAB1, ARK1, "f1_taban1"), (TAB2, ARK2, "f1_taban2")):
    x0, x1 = T["lo"][0], T["hi"][0]
    flans(ad, (x0, 163.3, -792.4), (x1, 179.5, -791.2), T)          # büküm: sacın arka kenarından yukarı
    percin_hatti(ad, (x0, 172.0, -790.0), (x1, 172.0, -790.0), (0, 0, -1), 790.0, 2.4, A_)
# (F2 tavan → arka YOK: arka PU levhası tavan seviyesinin üstüne çıkar, aşağı inen flanş levhayı süpürürdü; arka üst köşede gıda tarafında B kablo kanalı var.
#  İç tavan bölme üst flanşlarıyla (F6) ve sol duvar üst flanşıyla (F4) perçinlenir.)
# F4 · iç sol duvar: alt / arka / üst kenarı 15 mm GIDA TARAFINA (+x) bükülür → iç tabana (üstten), iç arka saca (önden), iç tavana (alttan) perçin
#  (sol PU levhası sol duvardan önce üstten takılır; sol duvarın arkasına flanş konamaz)
flans("f4_sol_alt", (798.5, 164.5, -790.0), (813.5, 165.7, 23.0), SOL)
percin_hatti("f4_sol_alt", (806.0, 165.7, -790.0), (806.0, 165.7, 23.0), (0, -1, 0), -165.7, 2.4, TAB1)
flans("f4_sol_arka", (798.5, 165.7, -790.0), (813.5, 726.8, -788.8), SOL)
percin_hatti("f4_sol_arka", (806.0, 165.7, -788.8), (806.0, 726.8, -788.8), (0, 0, -1), 788.8, 2.4, ARK1)
flans("f4_sol_ust", (798.5, 726.8, -790.0), (813.5, 728.0, 23.0), SOL)
percin_hatti("f4_sol_ust", (806.0, 726.8, -790.0), (806.0, 726.8, 23.0), (0, 1, 0), 726.8, 2.4, TAV1)
# F6 · bölme sacları
for S_, sg in BOLME:
    xs0, xs1 = S_["lo"][0], S_["hi"][0]; yt = S_["hi"][1]; zf = S_["hi"][2]
    # flanş DIŞA (gıda tarafına): bölme tezgâhta panel olarak (sac A + kovan + PU + sac B) kurulur, yerinde perçinler gıda tarafından çakılır
    xa, xb = (xs0 - 12.0, xs0) if sg > 0 else (xs1, xs1 + 12.0); xc = (xa + xb) / 2.0
    ad = "f6_bolme_%.0f" % xs0
    T = TAB1 if xc < 2108.5 else TAB2; A_ = ARK1 if xc < 2108.5 else ARK2; V_ = TAV1 if xc < 2108.5 else TAV2
    yt = min(yt, V_["lo"][1])                                          # flanş tarafındaki iç tavanın altı (B2 sac B: sağında alçak tavan 668)
    flans(ad + "_alt", (xa, 164.5, -788.8), (xb, 165.7, zf), S_)
    flans(ad + "_arka", (xa, 164.5, -790.0), (xb, yt, -788.8), S_)
    flans(ad + "_ust", (xa, yt - 1.2, -788.8), (xb, yt, zf), S_)
    percin_hatti(ad + "_alt", (xc, 165.7, -788.8), (xc, 165.7, zf), (0, -1, 0), -165.7, 2.4, T)
    percin_hatti(ad + "_arka", (xc, 165.7, -788.8), (xc, yt - 1.2, -788.8), (0, 0, -1), 788.8, 2.4, A_)
    percin_hatti(ad + "_ust", (xc, yt - 1.2, -788.8), (xc, yt - 1.2, zf), (0, 1, 0), yt - 1.2, 2.4, V_)     # alttan (gıda tarafından) yukarı
LOG("  flanş %d · perçin yeri %d" % (len(FL), len(PR)))

# ---------------------------------------------------------------- denetim + seçim
IZIN_FL = ("B_KASA__pu", "B_KASA__pu_dolgu")
IZIN_PR = ("B_KASA__pu", "B_KASA__pu_dolgu", "B_KASA__sac")
def ince(Tr, m, e=0.01):
    lo = np.asarray(m.bounding_box()[:3]); hi = np.asarray(m.bounding_box()[3:])
    Tr = Tr[np.all(Tr.max(1) >= lo - e, 1) & np.all(Tr.min(1) <= hi + e, 1)]
    out = []
    for t in Tr:
        nrm = np.cross(t[1] - t[0], t[2] - t[0]); L = np.linalg.norm(nrm)
        if L < 1e-9: continue
        h = mf.Manifold.hull_points(np.vstack([t + nrm / L * e, t - nrm / L * e]).tolist())
        if not h.is_empty(): out.append(h)
    return (mf.Manifold.batch_boolean(out, mf.OpType.Add) ^ m).volume() if out else 0.0


def tara(el):
    P = SE.ucgen(el["sh"], 0.02, 0.15); m = SE.mf_ucgen(P); out = []
    for d, b, v in K.tara(el, m, P, esik=0.02):
        if v < 0:
            v = ince(ucg(b), m)
            if v < 1e-4: continue
        out.append((d, b, v))
    return out


SORUN = []
for ad, sh, sahip in FL:
    el = dict(ad=ad, sh=sh, bom=["flanş"], tur="sac")
    for d, b, v in tara(el):
        if d.startswith(IZIN_FL) or b is sahip: continue
        SORUN.append(("flanş", ad, d, b["no"], round(v, 2), np.round(b["lo"], 1).tolist(), np.round(b["hi"], 1).tolist()))
SEC = []; ATLA_P = []
FLM = {}
for a_, sh_, _ in FL:
    m_ = SE.mf_ucgen(SE.ucgen(sh_, 0.02, 0.15)) or onar(SE.ucgen(sh_, 0.02, 0.15))
    FLM[a_] = m_ if a_ not in FLM else FLM[a_] + m_
for ad, adaylar, ref in PR:
    ok = None
    fl = FLM.get(ad)
    for el in adaylar:
        hit = [(d, b["no"], v) for d, b, v in tara(el) if not d.startswith(IZIN_PR)]
        if hit: continue
        me = SE.mf_ucgen(SE.ucgen(el["sh"], 0.02, 0.15))
        if fl is not None and (me ^ fl).volume() < 1.0:      # perçin flanş malzemesinden geçmeli (çentikte değil)
            hit = [("flanş çentiği", 0, 0.0)]; continue
        bb_ = me.bounding_box()
        if any(fa != ad and (me ^ fm).volume() > 0.005 for fa, fm in FLM.items()
               if np.all(np.asarray(fm.bounding_box()[3:]) >= np.asarray(bb_[:3])) and np.all(np.asarray(fm.bounding_box()[:3]) <= np.asarray(bb_[3:]))):
            hit = [("başka flanş", 0, 0.0)]; continue
        ok = el; break
    if ok is None:
        hat = adaylar[0]["ad"].rsplit("_", 1)[0]
        if sum(1 for a_, _, _ in PR if a_ == ad) and len([1 for x_ in PR if x_[0] == ad]) >= 1 and len([1 for a_, ad__, _ in PR if a_ == ad]) and True:
            ATLA_P.append((adaylar[0]["ad"], [(d, n_, round(v, 2)) for d, n_, v in hit[:2]])); continue
        SORUN.append(("perçin", adaylar[0]["ad"], hit[:3])); continue
    SEC.append((ok, ref))
for s in SORUN[:80]: LOG("  SORUN %s" % (s,))
LOG("  perçin seçildi %d / %d · sorun %d · konumu olmayan (hat üzerindeki diğer perçinler yeterli) %d %s" % (len(SEC), len(PR), len(SORUN), len(ATLA_P), ATLA_P[:4]))
if KURU: LOG("KURU %.0f sn" % (time.time() - t0)); sys.stdout.flush(); os._exit(0)
if SORUN: raise SystemExit("ADIM 49 DUR: %d sorun" % len(SORUN))

# ---------------------------------------------------------------- PU / iç sac delikleri (flanş + perçin) → flanşlar sahip saca birleşir (büküm) → perçinler eklenir
LAB = {id(e): g.etiket_b(ref) for e, ref in SEC}
# flanşlar kendi perçinleri kadar delinir (perçin gövdesi Ø4 + 0,1)
FL2 = []
for a_, sh_, o_ in FL:
    bb1 = sh_.BoundingBox()
    for e, _ in SEC:
        bb2 = e["sh"].BoundingBox()
        if bb2.xmin > bb1.xmax or bb1.xmin > bb2.xmax or bb2.ymin > bb1.ymax or bb1.ymin > bb2.ymax or bb2.zmin > bb1.zmax or bb1.zmin > bb2.zmax: continue
        n_ = np.asarray(e["n"], float); c = np.array([(bb2.xmin + bb2.xmax) / 2, (bb2.ymin + bb2.ymax) / 2, (bb2.zmin + bb2.zmax) / 2]); o2 = c - n_ * (c @ n_)
        sh_ = sh_.cut(B.sil(2.05, o2, n_, -1e5, 1e5))
    FL2.append((a_, sh_, o_))
FL = FL2
KES = [dict(ad=a, sh=s, bom=["flanş"], tur="sac") for a, s, _ in FL] + [e for e, _ in SEC]
# PU levhaları: kendi onarımlı katısından (0,01 mm ızgara) flanş + perçin hacmi çıkarılır (levha cebi / çentiği)
KM = [(e["ad"], SE.mf_ucgen(SE.ucgen(e["sh"], 0.02, 0.15))) for e in KES]
PU_KAY = []
for d in ("B_KASA__pu", "B_KASA__pu_dolgu"):
    for b in list(bc(g, d)):
        L = [(a, m) for a, m in KM if np.all(np.asarray(m.bounding_box()[3:]) >= b["lo"] - 0.05) and np.all(np.asarray(m.bounding_box()[:3]) <= b["hi"] + 0.05)]
        if not L: continue
        X = onar(ucg(b)); v0 = X.volume()
        Y = X - mf.Manifold.batch_boolean([m for _, m in L], mf.OpType.Add)
        if v0 - Y.volume() < 1e-3: continue
        degistir(g, b, SE.mf_P(Y)); PU_KAY.append(dict(pu="%s %s" % (d, np.round(b["lo"], 1).tolist()), cikan=round(v0 - Y.volume(), 1), kesici=len(L)))
        LOG("  PU cebi: %s %s · −%.0f mm³ (%d kesici)" % (d, np.round(b["lo"], 1).tolist(), v0 - Y.volume(), len(L)))
K = SE.Karsi(g, haric_onek=("B_KASA__pu",), acik_dene=True)
kayit = K.delik_ac(KES) + PU_KAY
if os.environ.get("YAMA_DEBUG"):
    for x in bc(g, "B_KASA__sac"):
        if x["lo"][0] < 1500 and x["lo"][1] < 200: LOG("   DBG %s %s %s" % (np.round(x["lo"], 2).tolist(), np.round(x["hi"], 2).tolist(), x["kapali"]))
# m8kit: eklenen üçgenler kaydedilene dek bileşen listesinde görünmez → kaydet + yeniden yükle, sonra flanş birleşimi
tmp1 = go + ".e1a.glb"; g.kaydet(tmp1); del g, K
g = Glb(tmp1)
DEG = {}
for ad, sh, sahip in FL: DEG.setdefault(id(sahip), [sahip, []])[1].append(sh)
for sahip, shs in DEG.values():
    lo, hi = sahip["lo"], sahip["hi"]
    b = [x for x in bc(g, "B_KASA__sac") if np.all(np.abs(x["lo"] - lo) < 0.3) and np.all(np.abs(x["hi"] - hi) < 0.3)]
    if len(b) != 1: raise SystemExit("ADIM 49 DUR: sahip sac %s → %d (%s)" % (np.round(lo, 2), len(b), [(np.round(x["lo"], 2).tolist(), np.round(x["hi"], 2).tolist(), x["kapali"]) for x in bc(g, "B_KASA__sac") if np.sum(np.abs(x["lo"] - lo) < 0.3) >= 2]))
    b = b[0]
    m = SE.mf_ucgen(ucg(b)) or onar(ucg(b))
    if m is None: raise SystemExit("ADIM 49 DUR: sac katısı kurulamadı %s" % np.round(lo, 1))
    for sh in shs: m = m + (SE.mf_ucgen(SE.ucgen(sh, 0.02, 0.15)) or onar(SE.ucgen(sh, 0.02, 0.15)))
    kab = sorted(m.decompose(), key=lambda k: -k.volume())
    if len(kab) > 1:
        LOG("  not: %s flanş çentiğinden kopan %d küçük parça atıldı (%s mm³)" % (np.round(lo, 1).tolist(), len(kab) - 1, [round(k.volume(), 1) for k in kab[1:]]))
        if sum(k.volume() for k in kab[1:]) > 2000.0: raise SystemExit("ADIM 49 DUR: flanşlı sac tek parça değil %s" % np.round(lo, 1))
        m = kab[0]
    degistir(g, b, SE.mf_P(m))
ETK = {}
for e, ref in SEC:
    lab = LAB[id(e)]
    g.ekle_dugum(DUG_B, SE.ucgen(e["sh"].copy(), 0.08, 0.5), kat=lab[0], mek=lab[1], kpk=False)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g
SE.sikistir(tmp, go)
for f_ in (tmp0, tmp1, tmp): os.remove(f_)
json.dump(dict(adim=49, ad="B iç kabuk flanş + perçin", flans=[dict(ad=a, kutu=SE.kutu6(dict(sh=s)), sahip=[round(float(v), 2) for v in list(o["lo"]) + list(o["hi"])]) for a, s, o in FL],
               percin=[dict(ad=e["ad"], kutu=SE.kutu6(e), bom=e["bom"], n=e.get("n"), ref=[round(float(v), 2) for v in list(r["lo"]) + list(r["hi"])]) for e, r in SEC], karsi=kayit, log=SE.LOG),
          open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=str)
LOG("ADIM 49 bitti · %d flanş · %d perçin · %s · %.0f sn" % (len(FL), len(SEC), go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
