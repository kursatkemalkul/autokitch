# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 47 · B BAĞLANTI ELEMANLARI (4 Eki 2026 · Claude · YEREL · Kemal: "bağlantı elemanı olmayan yerlere gerçek bağlantı (delik + standart
vida / perçin / PEM / somun ya da kaynak), havada parça kalmasın; M8 perçin somun kapalı uçlu + M8 × 16; evaporatör kablosu kanaldan doğru geçsin")
python 47_b_baglanti.py girdi.glb cikti.glb      (zincir: hat3_v9n.glb → hat3_v9o.glb)

Kaynak: B montaj animasyonu v3 denetimi (gece2/b3/denetim.md · MODEL AÇIKLARI 2 ve 4, vida tablosu M8 notu). Her eleman standart üründür (bkz. veri/bag47.py),
karşı parçalarda delik / yuva manifold3d boolean ile açılır (sac_ent.Karsi.delik_ac: cıvata / saplama ise ISO 273 orta geçiş deliği eleman boyunca).
Her yerleşim önce DENETLENİR: eleman katısı (geçiş deliği değil) yalnız izinli karşı parçalara girebilir (deldiği saclar); somun / pul / baş hiçbir şeye
girmez → aday konumlar sırayla denenir, hiçbiri temiz değilse betik DURUR.

 A  DİKME AYAKLARI (12): 6 modüler dikme (GFRP takozlu) + 6 taşıyıcı dikme · kutu profilin alt ucuna içeriden uç plakası (26 × 26 × 3 / 6, TIG) +
    2 × DIN 929 M5 kaynak somunu (plakaya TIG) · alttan 2 × ISO 4762 M5 × 16 + DIN 125 pul: şase üst duvarı (Ø5,5) → dış taban → GFRP → plaka.
    Şase üstündeki ayaklarda cıvata şase kutusunun içinden: alt duvarda Ø9,5 erişim deliği. Ayar ayağının (M12 saplama, şase ekseninde) yanından çapraz.
 B  EVAPORATÖR BRAKETLERİ (8): alt L braketlerin duvar flanşı (1,5) · üst düz braketlere 20 × 22 × 2 duvar kulağı (büküm) eklenir · iç arka sacta
    PEM FHS-M5-8 (baş PU tarafında gömülü) + DIN 125 + ISO 4032 M5.
 C  SOĞUTMA GRUBU (4): taban köşebent raylarının uçlarında ISO 4762 M4 × 12 + DIN 433 pul (raylar arası boşluk motor plakasının altında 4 mm →
    yalnız uçlar erişilebilir) → dış taban → şase üst duvarında M4 kapalı uçlu perçin somun; şase olmayan uçta pul + ISO 4032 M4 tabanın altında.
 D  B ELEKTRİK MONTAJ PLAKASI (6): dış arka 2'de PEM FHS-M5-8 (baş dış yüzde gömülü) + pul + somun (plakanın köşe / kenar ortaları, cihazsız bölge).
 E  İSTASYON KUTUSU (havadaydı): 2 × U konsol (2 mm paslanmaz, 2 büküm) kutunun sağ yan duvarı ↔ dış sağ yan sac: kutuya 2 × ISO 7380 M4 × 8 + pul +
    somun (içeriden) · sağ yan sacta 2 × PEM FHS-M5-8 + pul + somun.
 F  ZİNCİR KANALI (havadaydı): ayağına 2 × L konsol (2 mm, 1 büküm) · kanal duvarına 2 × DIN 7337 Ø3,2 kör perçin · tabana PEM FHS-M5-8 + pul + somun.
 G  ISI KALKANI IŞINIM SACI (12): her PTFE takozun ekseninde U kalkan tabanında PEM FHS-M4-18 → takoz (Ø4,5) → ışınım sacı (Ø4,5) → DIN 125 + ISO 4032 M4.
 H  İÇ KANALLAR (ELK_IC__kanal, B bölgesi) + B kablo kanalları: tabanı bir saca dayanan her kanal parçası tabanından, boyuna göre 1–3 PEM FHS-M4-6 +
    DIN 125 + ISO 4032 M4 (kanal içinde, kabloya değmeyen konumda) · saca 0,6–4 mm boşlukla duran parça (evaporatör önündeki fan kablosu kanalı):
    DIN 7337 Ø3,2 kör perçin + Ø7 aralık burcu.
 J  M8 PERÇİN SOMUNLARI (22): açık uçlu → KAPALI UÇLU (gövde ucu 4 mm dolu kapak, iç diş derinliği 17) · şase cıvataları ISO 4762 M8 × 20 → × 16 ·
    A / TOPPING / K kaidelerinden gelen üst M8 cıvataları M8 × 16 (uç kapalı uca değmez).
 K  EVAPORATÖR 1 FAN KABLOSU: iç kanaldaki (ic_kanal_31) iki geçiş deliğinin eksenine (+3,93 mm y) alınır; uçlarda (B kablo kanalı ve fan motoru) bağlantı
    korunur (kanal içinde eğimli geçiş) → kablo ↔ kanal kesişimi 0.
Kaynak dikişleri / puntalar modelde yok (montaj animasyonunda gösterilir)."""
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
YENI_DUG = "B_BAGLANTI__paslanmaz"


def bc(g, d):
    g._bc.pop(d, None)
    try: g.bilesen(d, 0)
    except (IndexError, ValueError, KeyError): return []
    return g._bc[d]


def ucg(b):
    return np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])


def kutu_bul(g, d, lo, hi, tol=0.3):
    L = [b for b in bc(g, d) if np.all(np.abs(b["lo"] - np.asarray(lo)) < tol) and np.all(np.abs(b["hi"] - np.asarray(hi)) < tol)]
    if len(L) != 1: raise SystemExit("ADIM 47 DUR: %s %s %s → %d bileşen" % (d, lo, hi, len(L)))
    return L[0]


def degistir(g, b, P):
    ilk = [True]
    def f(_):
        if ilk[0]: ilk[0] = False; return P
        return None
    g.donustur(b, f)


# =====================================================================================================================================
# EVRE 0 · geometri düzeltmeleri (J perçin somunu / cıvata, B üst braket kulağı, K kablo) — m8kit
# =====================================================================================================================================
g = Glb(gi)
KAY = dict(J=[], B=[], K=[])
# ---- J · kapalı uçlu perçin somun: açık gövde ucuna 4 mm dolu kapak (gövde Ø = mevcut alt halka Ø) — katı birleşim
PERCIN = []
for d in ("B_MODULER__baglanti", "B_TASIYICI__baglanti"):
    for b in bc(g, d):
        P = ucg(b); Q = P.reshape(-1, 3); c = (b["lo"] + b["hi"]) / 2.0
        r = np.hypot(Q[:, 0] - c[0], Q[:, 2] - c[2]); ya = Q[:, 1].min()
        ralt = float(r[np.abs(Q[:, 1] - ya) < 0.01].max())
        m = SE.mf_ucgen(P)
        if m is None: raise SystemExit("ADIM 47 DUR: perçin somun kapalı değil %s[%d]" % (d, b["no"]))
        kap = B.sil(ralt, (c[0], 0, c[2]), (0, 1, 0), ya - 4.0, ya + 0.05)
        km = SE.mf_ucgen(SE.ucgen(kap, 0.02, 0.15))
        yeni = m + km
        PERCIN.append((d, b, (c[0], ya, c[2])))
        degistir(g, b, SE.mf_P(yeni))
        KAY["J"].append(dict(percin="%s[%d]" % (d, b["no"]), eksen=[round(float(c[0]), 2), round(float(c[2]), 2)], uc_y_once=round(float(ya), 2), uc_y_sonra=round(float(ya - 4.0), 2)))
LOG("  J: %d perçin somun kapalı uçlu (gövde ucu −4 mm dolu)" % len(PERCIN))
assert len(PERCIN) == 22, len(PERCIN)


def kisalt(g, d, b, eks, uh, L_yeni, yon):
    """cıvata bileşeni: eksen (x, z) · uh = baş altı (y) · yon = −1 (aşağı giren) / +1 · gövde köşeleri (r ≤ 4,1) baş altından uca doğru doğrusal sıkıştırılır"""
    P = ucg(b); Q = P.reshape(-1, 3).copy(); r = np.hypot(Q[:, 0] - eks[0], Q[:, 2] - eks[1])
    uc = Q[:, 1].min() if yon < 0 else Q[:, 1].max()
    L0 = abs(uh - uc); s = L_yeni / L0
    k = (r <= 4.1) & ((Q[:, 1] < uh - 1e-3) if yon < 0 else (Q[:, 1] > uh + 1e-3))
    Q[k, 1] = uh - (uh - Q[k, 1]) * s
    degistir(g, b, Q.reshape(-1, 3, 3))
    return L0, uc, uh + yon * L_yeni


# şase cıvataları (B_KASA__paslanmaz, M8 · baş üstte, aşağı)
for d_, b_, (x, ya, z) in PERCIN:
    if ya > 400: continue
    cand = [b for b in bc(g, "B_KASA__paslanmaz") if abs((b["lo"][0] + b["hi"][0]) / 2 - x) < 0.3 and abs((b["lo"][2] + b["hi"][2]) / 2 - z) < 0.3
            and b["hi"][1] - b["lo"][1] > 20 and b["hi"][0] - b["lo"][0] < 14]
    if len(cand) != 1: raise SystemExit("ADIM 47 DUR: şase cıvatası (%.0f, %.0f) %d" % (x, z, len(cand)))
    b = cand[0]; Q = ucg(b).reshape(-1, 3); r = np.hypot(Q[:, 0] - x, Q[:, 2] - z)
    uh = float(Q[r > 5.0, 1].min())
    L0, uc0, uc1 = kisalt(g, "B_KASA__paslanmaz", b, (x, z), uh, 16.0, -1)
    KAY["J"].append(dict(civata="B_KASA__paslanmaz (%.0f, %.0f)" % (x, z), boy_once=round(L0, 2), boy_sonra=16.0, uc_y=round(uc1, 2), percin_dis_dibi=round(ya + 17.0 - 17.0, 2)))
# üst perçin somunlarına giren kaide cıvataları (A / TOPPING / K düğümleri; yukarıdan)
UST = 0
for d_, b_, (x, ya, z) in PERCIN:
    if ya < 400: continue
    bul = []
    for d in sorted(set(p["name"] for p in g.prims)):
        if d.startswith(("B_", "ELK_", "ACIL")): continue
        if not any(k in d for k in ("GOVDE", "KAIDE")): continue
        for b in bc(g, d):
            if abs((b["lo"][0] + b["hi"][0]) / 2 - x) < 0.5 and abs((b["lo"][2] + b["hi"][2]) / 2 - z) < 0.5 and b["lo"][1] < ya + 17.5 and b["hi"][1] > ya + 25:
                Q = ucg(b).reshape(-1, 3); r = np.hypot(Q[:, 0] - x, Q[:, 2] - z)
                if np.any((r < 4.1) & (Q[:, 1] < ya + 17.0)): bul.append((d, b))
    for d, b in bul:
        Q = ucg(b).reshape(-1, 3); r = np.hypot(Q[:, 0] - x, Q[:, 2] - z)
        bas = (r > 5.5) & (r < 7.0)
        uh = float(Q[bas, 1].min()) if bas.any() else float(Q[r > 4.5, 1].max())
        # pul aynı bileşendeyse baş altı = pul üstü: baş halkasının (r 6–7) en alt düzlemi
        L0, uc0, uc1 = kisalt(g, d, b, (x, z), uh, 16.0, -1)
        UST += 1
        KAY["J"].append(dict(civata="%s[%d] (%.0f, %.0f)" % (d, b["no"], x, z), boy_once=round(L0, 2), boy_sonra=16.0, uc_y=round(uc1, 2), percin_ust=round(ya + 17.0, 2)))
LOG("  J: şase cıvatası 10 + üst kaide cıvatası %d → M8 × 16" % UST)

# ---- B · üst evaporatör braketlerine duvar kulağı (2 mm, braket genişliği, 22 mm yukarı)
UST_BRK = []
for b in bc(g, "B_SOGUTMA__celik"):
    e = b["hi"] - b["lo"]
    if abs(e[1] - 2.0) < 0.05 and abs(e[0] - 20.0) < 0.05 and abs(b["lo"][2] + 790.0) < 0.05 and e[2] > 100:
        UST_BRK.append(b)
assert len(UST_BRK) == 4, len(UST_BRK)
for b in UST_BRK:
    m = SE.mf_ucgen(ucg(b)); lo, hi = b["lo"], b["hi"]
    kul = B.kutu((lo[0], lo[1], -790.0), (hi[0], hi[1] + 22.0, -788.0))
    yeni = m + SE.mf_ucgen(SE.ucgen(kul, 0.02, 0.15))
    degistir(g, b, SE.mf_P(yeni))
    KAY["B"].append(dict(ust_braket=[round(float(v), 2) for v in list(lo) + list(hi)], kulak=[float(lo[0]), float(hi[1]), float(hi[0]), float(hi[1] + 22.0)]))

# ---- K · evaporatör 1 fan kablosu: geçiş deliklerinin eksenine
KAB = [b for b in bc(g, "ELK_DOLAP__kablo_sinyal") if np.all(b["lo"] >= [1683.9, 509.0, -780.0]) and np.all(b["hi"] <= [1786.1, 666.7, -625.0])]
assert len(KAB) == 8, len(KAB)
DY = 3.93


def w(x):
    return np.clip((x - 1686.0) / 14.0, 0, 1) * np.clip((1786.0 - x) / 56.0, 0, 1)


for b in KAB:
    Q = ucg(b).reshape(-1, 3).copy(); Q[:, 1] += DY * w(Q[:, 0])
    degistir(g, b, Q.reshape(-1, 3, 3))
KAY["K"] = dict(parca=len(KAB), dy=DY, gecis="x 1686→1700 ve 1730→1786 eğimli; kanal içinde +3,93")
tmp0 = go + ".e0.glb"; g.kaydet(tmp0); del g

# =====================================================================================================================================
# EVRE 1 · bağlantı elemanları: yerleşim (denetimli) + karşı tarafta delik
# =====================================================================================================================================
g = Glb(tmp0)
# açık (adım 44 cepli) PU levhaları önce 0,01 mm ızgarada kapatılır → perçin / saplama cepleri tam boolean ile açılabilir
def _onar0(P):
    for rr in (1e-4, 0.01, 0.05):
        u, inv = np.unique(np.round(P.reshape(-1, 3) / rr) * rr, axis=0, return_inverse=True); F = inv.reshape(-1, 3)
        F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
        m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=F.astype(np.uint32)))
        if m.status() == mf.Error.NoError and not m.is_empty(): return m
    return None
n_on = 0
for b in list(bc(g, "B_KASA__pu")):
    if b["kapali"]: continue
    m = _onar0(ucg(b))
    if m is None: raise SystemExit("ADIM 47 DUR: PU onarılamadı %s" % np.round(b["lo"], 1))
    degistir(g, b, SE.mf_P(m)); n_on += 1
if n_on:
    LOG("  PU onarıldı: %d levha" % n_on); g.kaydet(tmp0 + ".o.glb"); del g; g = Glb(tmp0 + ".o.glb")
K = SE.Karsi(g, haric_onek=("B_KASA__pu",), acik_dene=True)        # PU levhaları ayrı (onarımlı katıdan) kesilir — aşağıda
PU_D = ("B_KASA__pu", "B_KASA__pu_dolgu")


def onar(P):
    for rr in (1e-4, 0.01, 0.05):
        u, inv = np.unique(np.round(P.reshape(-1, 3) / rr) * rr, axis=0, return_inverse=True); F = inv.reshape(-1, 3)
        F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
        m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=F.astype(np.uint32)))
        if m.status() == mf.Error.NoError and not m.is_empty(): return m
    return None
EL = []            # (grup, eleman, etiket kaynağı (düğüm, bileşen))
KESICI = []        # yalnız delik açan (modele eklenmeyen) kesiciler
DENETIM = []


def ince(Tr, m, e=0.01):
    """açık bileşen üçgenleri (kapalı katı kurulamayan kablo / kanal) ↔ eleman katısı: her üçgen ±e kalınlıkta prizma → kesişim hacmi"""
    lo = np.asarray(m.bounding_box()[:3]); hi = np.asarray(m.bounding_box()[3:])
    Tr = Tr[np.all(Tr.max(1) >= lo - e, 1) & np.all(Tr.min(1) <= hi + e, 1)]
    out = []
    for t in Tr:
        nrm = np.cross(t[1] - t[0], t[2] - t[0]); L = np.linalg.norm(nrm)
        if L < 1e-9: continue
        nrm = nrm / L * e
        h = mf.Manifold.hull_points(np.vstack([t + nrm, t - nrm]).tolist())
        if not h.is_empty(): out.append(h)
    if not out: return 0.0
    return (mf.Manifold.batch_boolean(out, mf.OpType.Add) ^ m).volume()


def isabet(el):
    P = SE.ucgen(el["sh"], 0.02, 0.15); m = SE.mf_ucgen(P)
    if m is None: raise SystemExit("ADIM 47 DUR: eleman kapalı değil %s" % el["ad"])
    out = []
    for d, b, v in K.tara(el, m, P, esik=0.02):
        if v < 0:
            v = ince(ucg(b), m)
            if v < 1e-4: continue
        out.append((d, b["no"], v))
    return out


def temiz(elemanlar, izin, yeni=()):
    """izin: {eleman adı: [(düğüm önekleri ...)]} — eleman yalnız bu öneklerle başlayan düğümlere girebilir · yeni: aynı adayda birbirine değmemeli"""
    for el in elemanlar:
        for d, no, v in isabet(el):
            if not any(d.startswith(o) for o in izin.get(el["ad"], ())): return False, (el["ad"], d, no, round(v, 2))
    return True, None


def delikle(els):
    """aday içindeki sac elemanlar (konsol, kelepçe) kendisinden geçen cıvata / saplama / perçin kadar delinir (ISO 273 orta geçiş Ø)"""
    vid = [e for e in els if e.get("tur") in ("civata", "saplama", "percin")]
    for e in els:
        if e.get("tur") != "sac" or e["ad"].startswith("ayak_plaka_"): continue
        sh = e["sh"]
        for v in vid:
            bb1 = sh.BoundingBox(); bb2 = v["sh"].BoundingBox()
            if bb2.xmin > bb1.xmax or bb1.xmin > bb2.xmax or bb2.ymin > bb1.ymax or bb1.ymin > bb2.ymax or bb2.zmin > bb1.zmax or bb1.zmin > bb2.zmax: continue
            n_ = np.asarray(v.get("n") or (0, 0, 1), float); c = np.array([(bb2.xmin + bb2.xmax) / 2, (bb2.ymin + bb2.ymax) / 2, (bb2.zmin + bb2.zmax) / 2])
            o_ = c - n_ * (c @ n_); dm = SE.dis_cap(v); r = (SE.GECIS[dm] / 2.0) if dm else 1.75
            sh = sh.cut(B.sil(r, o_, n_, -1e5, 1e5))
        e["sh"] = sh


def sec(grup, adaylar, ref):
    """adaylar: [(elemanlar, izin, kesiciler)] → ilk temiz aday modele girer"""
    son = None
    for i, (els, izin, kes) in enumerate(adaylar):
        delikle(els)
        ok, neden = temiz(els, izin)
        if ok:
            for e in els: EL.append((grup, e, ref))
            KESICI.extend(kes); return i
        son = neden
    raise SystemExit("ADIM 47 DUR: %s temiz aday yok (son engel %s)" % (grup, son))


SAC_IZIN = ("B_KASA__sac", "B_KASA__paslanmaz")
# ---------------------------------------------------------------- A · dikme ayakları
SASE = [b for b in bc(g, "B_MODULER__paslanmaz") if b["hi"][1] <= 123.5]
GFRP = [b for b in bc(g, "B_MODULER__gfrp") if b["hi"][1] < 130]
DIK = [("B_MODULER__paslanmaz", b) for b in bc(g, "B_MODULER__paslanmaz") if b["lo"][1] < 128 and b["hi"][1] > 700 and b["hi"][0] - b["lo"][0] < 31]
DIK += [("B_TASIYICI__celik", b) for b in bc(g, "B_TASIYICI__celik") if b["lo"][1] < 125 and b["hi"][1] > 700]
assert len(DIK) == 12, len(DIK)
OFS = [((8, 8), (-8, -8)), ((8, -8), (-8, 8)), ((8, 0), (-8, 0)), ((0, 8), (0, -8))]
for d, b in DIK:
    cx, cz = (b["lo"][0] + b["hi"][0]) / 2.0, (b["lo"][2] + b["hi"][2]) / 2.0; y0 = b["lo"][1]
    gfrp = y0 > 126
    alt = [s for s in SASE if s["lo"][0] - 0.1 < cx < s["hi"][0] + 0.1 and s["lo"][2] - 0.1 < cz < s["hi"][2] + 0.1]
    sase = bool(alt)
    p = 3.0 if (gfrp and sase) else 6.0
    adaylar = []
    for ofs in OFS:
        els, izin, kes = [], {}, []
        plsh = B.kutu((cx - 13, y0, cz - 13), (cx + 13, y0 + p, cz + 13))
        for dx, dz in ofs: plsh = plsh.cut(B.sil(2.75, (cx + dx, 0.0, cz + dz), (0, 1, 0), y0 - 1.0, y0 + p + 1.0))
        pl = dict(ad="ayak_plaka_%.0f_%.0f" % (cx, cz), sh=plsh,
                  bom=["uç plakası AISI 304 26 × 26 × %.0f (dikme alt ucu, içeriden TIG)" % p], tur="sac")
        els.append(pl); izin[pl["ad"]] = ()
        for k, (dx, dz) in enumerate(ofs):
            o = (cx + dx, 0.0, cz + dz); n = (0, 1, 0); ad = "ayak_%.0f_%.0f_%d" % (cx, cz, k)
            ks, _ = B.kaynak_somunu("M5", o, n, y0 + p, ad + "_kaynak_somunu")
            if sase:
                pu, a1 = B.pul("M5", o, n, 119.0, ad + "_pul"); cv = B.civata4762("M5", 16, o, n, 119.0, ad + "_civata")
                kes.append(dict(ad=ad + "_erisim", sh=B.sil(4.75, o, n, 61.0, 68.0), bom=["Ø9,5 erişim deliği (şase alt duvarı)"], tur="kesici"))
            else:
                pu, a1 = B.pul("M5", o, n, 122.0, ad + "_pul"); cv = B.civata4762("M5", 16, o, n, 122.0, ad + "_civata")
            els += [ks, pu, cv]
            izin[ks["ad"]] = (); izin[pu["ad"]] = (); izin[cv["ad"]] = ("B_KASA__sac", "B_MODULER__gfrp", "B_MODULER__paslanmaz") if sase else ("B_KASA__sac", "B_MODULER__gfrp")
        adaylar.append((els, izin, kes))
    i = sec("A", adaylar, (d, b))
    DENETIM.append(("A", "%s (%.0f, %.0f)" % (d, cx, cz), "aday %d" % i, "şase" if sase else "taban altı", "GFRP" if gfrp else "-"))
LOG("  A: 12 dikme ayağı")

# ---------------------------------------------------------------- G · ışınım sacı (PTFE takoz eksenleri)
TAKOZ = [b for b in bc(g, "B_KASA__koyu") if abs(b["lo"][1] - 729.2) < 0.05 and abs(b["hi"][1] - 740.0) < 0.05]
assert len(TAKOZ) == 12, len(TAKOZ)
U = kutu_bul(g, "B_KASA__sac", (2500.0, 728.0, -828.5), (3994.7, 786.5, 23.0))
for b in TAKOZ:
    cx, cz = (b["lo"][0] + b["hi"][0]) / 2.0, (b["lo"][2] + b["hi"][2]) / 2.0; o = (cx, 0.0, cz); n = (0, 1, 0); ad = "isinim_%.0f_%.0f" % (cx, cz)
    st = B.fhs("M4", 18, (cx, 729.2, cz), n, 1.2, ad + "_saplama", "(ısı kalkanı U tabanı)")
    pu, a1 = B.pul("M4", o, n, 740.8, ad + "_pul"); so, a2 = B.somun("M4", o, n, a1, ad + "_somun")
    sec("G", [([st, pu, so], {st["ad"]: ("B_KASA__sac", "B_KASA__koyu"), pu["ad"]: (), so["ad"]: ()}, [])], ("B_KASA__sac", U))
LOG("  G: 12 ışınım sacı saplaması")

# ---------------------------------------------------------------- D · B elektrik montaj plakası
PLK = kutu_bul(g, "B_ELEKTRIK__sac", (4035.0, 455.0, -828.5), (4392.0, 745.0, -826.5))
for xs in ((4043.0, 4063.0), (4213.0, 4193.0, 4233.0), (4384.0, 4364.0)):
    for y in (462.0, 738.0):
        ad_ = []
        for x in xs:
            o = (x, y, 0.0); n = (0, 0, 1); ad = "eplaka_%.0f_%.0f" % (xs[0], y)
            st = B.fhs("M5", 8, (x, y, -828.5), n, 1.5, ad + "_saplama", "(dış arka 2)")
            pu, a1 = B.pul("M5", o, n, -826.5, ad + "_pul"); so, a2 = B.somun("M5", o, n, a1, ad + "_somun")
            ad_.append(([st, pu, so], {st["ad"]: ("B_KASA__sac", "B_ELEKTRIK__sac"), pu["ad"]: (), so["ad"]: ()}, []))
        sec("D", ad_, ("B_ELEKTRIK__sac", PLK))
LOG("  D: 6 elektrik plakası saplaması")

# ---------------------------------------------------------------- B · evaporatör braketleri
ALT_BRK = [b for b in bc(g, "B_SOGUTMA__celik") if abs(b["lo"][2] + 790.0) < 0.05 and abs((b["hi"] - b["lo"])[1] - 26.5) < 0.1]
UST_BRK = [b for b in bc(g, "B_SOGUTMA__celik") if abs(b["lo"][2] + 790.0) < 0.05 and abs((b["hi"] - b["lo"])[1] - 24.0) < 0.1]
assert len(ALT_BRK) == 4 and len(UST_BRK) == 4, (len(ALT_BRK), len(UST_BRK))
for b in ALT_BRK + UST_BRK:
    cx = (b["lo"][0] + b["hi"][0]) / 2.0
    if b in ALT_BRK: y = (b["lo"][1] + 1.5 + b["hi"][1]) / 2.0; tf = 1.5
    else: y = b["hi"][1] - 11.0; tf = 2.0
    o = (cx, y, 0.0); n = (0, 0, 1); ad = "evap_%.0f_%.0f" % (cx, y)
    st = B.fhs("M5", 8, (cx, y, -790.0), n, 1.2, ad + "_saplama", "(iç arka sac)")
    pu, a1 = B.pul("M5", o, n, -790.0 + tf, ad + "_pul"); so, a2 = B.somun("M5", o, n, a1, ad + "_somun")
    sec("B", [([st, pu, so], {st["ad"]: ("B_KASA__sac", "B_SOGUTMA__celik"), pu["ad"]: (), so["ad"]: ()}, [])], ("B_SOGUTMA__celik", b))
LOG("  B: 8 evaporatör braketi saplaması")

# ---------------------------------------------------------------- C · soğutma grubu taban rayları (uçlar)
RAY = [b for b in bc(g, "B_SOGUTMA__celik") if b["hi"][0] - b["lo"][0] > 360 and b["hi"][1] - b["lo"][1] > 39]
assert len(RAY) == 2, len(RAY)
for b in RAY:
    # yatay kol: dikey kolun karşı tarafı (kesitte y 124,5–127,5 olan z aralığı) — dikey kol z ucunda 3 mm
    Q = ucg(b).reshape(-1, 3); ust = Q[Q[:, 1] > 160]; zk0, zk1 = ust[:, 2].min(), ust[:, 2].max()
    z0, z1 = b["lo"][2], b["hi"][2]
    zc = (zk1 + z1) / 2.0 if abs(zk0 - z0) < 0.1 else (z0 + zk0) / 2.0
    for xs in ((4032.5, 4033.0, 4032.0), (4393.0, 4392.5, 4393.5, 4392.0)):
        ad_ = []
        for x in xs:
            o = (x, 0.0, zc); n = (0, -1, 0); ad = "grup_%.0f_%.0f" % (xs[0], zc)
            alt = [s for s in SASE if s["lo"][0] < x < s["hi"][0] and s["lo"][2] < zc < s["hi"][2]]
            pu = dict(ad=ad + "_pul", sh=B.halka(4.0, 2.15, o, n, -128.0, -127.5), bom=["DIN 433 M4 pul A2"], tur="pul", n=list(np.asarray(n, float)))
            cv = B.civata4762("M4", 12 if alt else 10, o, n, -128.0, ad + "_civata")
            els = [pu, cv]; izin = {pu["ad"]: (), cv["ad"]: ("B_SOGUTMA__celik", "B_KASA__sac", "B_MODULER__paslanmaz")}
            if alt:
                ps = B.percin_somun_kapali((x, 124.0, zc), (0, -1, 0), ad + "_percin_somun", m="M4", bas_d=9.0, bas_h=1.0, gov_d=6.0, boy=12.0, dis_derin=10.0)
                ps["bom"] = ["M4 kapalı uçlu perçin somun, düz baş Ø9, A2 (şase üst duvarı; baş taban deliğinde Ø9,5)"]
                ps["sh"] = ps["sh"]; els.append(ps); izin[ps["ad"]] = ("B_MODULER__paslanmaz", "B_KASA__sac")
            else:
                pu2 = dict(ad=ad + "_pul_alt", sh=B.halka(4.0, 2.15, o, n, -123.0, -122.5), bom=["DIN 433 M4 pul A2"], tur="pul", n=list(np.asarray(n, float)))
                so, _ = B.somun("M4", o, n, -122.5, ad + "_somun")
                els += [pu2, so]; izin[pu2["ad"]] = (); izin[so["ad"]] = ()
            ad_.append((els, izin, []))
        sec("C", ad_, ("B_SOGUTMA__celik", b))
LOG("  C: 4 soğutma grubu ray cıvatası")

# ---------------------------------------------------------------- E · istasyon kutusu (2 U konsol → sağ yan sac)
KUTU = kutu_bul(g, "ELK_ISTASYON__pano", (4160.0, 605.0, -698.0), (4320.0, 725.0, -612.0))
for yc in (617.0, 713.0):
    y0, y1 = yc - 10.0, yc + 10.0
    k1 = B.kutu((4320.0, y0, -680.0), (4322.0, y1, -628.0)); k2 = B.kutu((4396.5, y0, -680.0), (4398.5, y1, -628.0))
    web = B.kutu((4320.0, y0, -630.0), (4398.5, y1, -628.0))
    kons = dict(ad="istasyon_konsol_%.0f" % yc, sh=k1.fuse(k2).fuse(web).clean(), bom=["U konsol AISI 304 2 mm (2 büküm) 78,5 × 52 × 20 · istasyon kutusu ↔ sağ yan"], tur="sac")
    els = [kons]; izin = {kons["ad"]: ()}
    for zc in (-665.0, -645.0):
        o = (0.0, yc, zc); n = (-1, 0, 0); ad = "istasyon_%.0f_%.0f" % (yc, zc)
        cv = B.civata7380("M4", 8, o, n, -4322.0, ad + "_civata")              # baş konsol dışında (+x), gövde −x: konsol 2 + kutu duvarı 1,2 + pul + somun
        pu, a1 = B.pul("M4", o, n, -4318.8, ad + "_pul"); so, a2 = B.somun("M4", o, n, a1, ad + "_somun")
        els += [cv, pu, so]; izin[cv["ad"]] = ("ELK_ISTASYON__pano",); izin[pu["ad"]] = (); izin[so["ad"]] = ()
    o = (0.0, yc, -654.0); n = (-1, 0, 0); ad = "istasyon_yan_%.0f" % yc
    st = B.fhs("M5", 8, (4398.5, yc, -654.0), n, 1.5, ad + "_saplama", "(dış sağ yan)")
    pu, a1 = B.pul("M5", o, n, -4396.5, ad + "_pul"); so, a2 = B.somun("M5", o, n, a1, ad + "_somun")
    els += [st, pu, so]; izin[st["ad"]] = ("B_KASA__sac",); izin[pu["ad"]] = (); izin[so["ad"]] = ()
    sec("E", [(els, izin, [])], ("ELK_ISTASYON__pano", KUTU))
LOG("  E: istasyon kutusu 2 U konsol")

# ---------------------------------------------------------------- F · zincir kanalı ayağı (2 L konsol)
ZK = kutu_bul(g, "ELK_ZINCIR__kanal", (4065.0, 128.0, -665.0), (4066.2, 575.0, -595.0))
for sx, xw in ((-1, 4065.0), (+1, 4115.0)):
    xa, xb = (xw - 2.0, xw) if sx < 0 else (xw, xw + 2.0)
    xl0, xl1 = (xw - 24.0, xw) if sx < 0 else (xw, xw + 24.0)
    dik = B.kutu((xa, 124.5, -640.0), (xb, 160.0, -620.0)); yat = B.kutu((xl0, 124.5, -640.0), (xl1, 126.5, -620.0))
    kons = dict(ad="zincir_konsol_%d" % sx, sh=dik.fuse(yat).clean(), bom=["L konsol AISI 304 2 mm (1 büküm) 24 × 35,5 × 20 · zincir kanalı ↔ dış taban"], tur="sac")
    els = [kons]; izin = {kons["ad"]: ()}
    for yc in (138.0, 152.0):
        o = (0.0, yc, -630.0); n = (-sx, 0, 0); ad = "zincir_%d_%.0f" % (sx, yc)
        pr = B.kor_percin(o, n, -sx * xa if sx < 0 else -sx * xb, 2.0 + 1.2 + 2.5, ad + "_percin")
        els.append(pr); izin[pr["ad"]] = ("ELK_ZINCIR__kanal",)
    xf = (xl0 + xa) / 2.0 if sx < 0 else (xb + xl1) / 2.0
    o = (xf, 0.0, -630.0); n = (0, 1, 0); ad = "zincir_taban_%d" % sx
    st = B.fhs("M5", 8, (xf, 124.5, -630.0), n, 1.5, ad + "_saplama", "(dış taban)")
    pu, a1 = B.pul("M5", o, n, 126.5, ad + "_pul"); so, a2 = B.somun("M5", o, n, a1, ad + "_somun")
    els += [st, pu, so]; izin[st["ad"]] = ("B_KASA__sac",); izin[pu["ad"]] = (); izin[so["ad"]] = ()
    sec("F", [(els, izin, [])], ("ELK_ZINCIR__kanal", ZK))
LOG("  F: zincir kanalı 2 L konsol")

# ---------------------------------------------------------------- H · iç kanallar (taban plakası bir saca dayanan her kanal parçası)
DESTEK = []        # (düğüm, bileşen, kalınlık ekseni, kalınlık)
for d in ("B_KASA__sac", "B_KASA__paslanmaz", "B_DEPO__sac", "B_ELEKTRIK__sac", "B_KABLO__kanal", "B_SOGUTMA__sac"):
    for b in bc(g, d):
        e = b["hi"] - b["lo"]; ax = int(np.argmin(e))
        DESTEK.append((d, b, ax, float(e[ax])))
KANAL = [b for b in bc(g, "ELK_IC__kanal") if np.all(b["lo"] >= [736, 124, -830]) and np.all(b["hi"] <= [4400, 790, 40])]
SAY_H = 0; ATLA = []
for b in KANAL:
    e = b["hi"] - b["lo"]; ax = int(np.argmin(e)); t = float(e[ax])
    if t > 1.3: continue                                                # yalnız 1,2 plakalar
    uz = [k for k in range(3) if k != ax]; Lx = sorted(((e[k], k) for k in uz), reverse=True)
    L, kL = Lx[0]; W_, kW = Lx[1]
    if L < 15.0 or W_ < 12.0: continue
    # destek: kalınlık ekseninde plakanın bir yüzüne 0–4 mm, diğer iki eksende örtüşen
    eslesme = None
    for yon in (-1, +1):
        yuz = b["lo"][ax] if yon < 0 else b["hi"][ax]
        for d, s, sax, st_ in DESTEK:
            if sax != ax and d != "B_KABLO__kanal" and d != "B_SOGUTMA__sac": continue
            sy = s["hi"][ax] if yon < 0 else s["lo"][ax]
            bos = (yuz - sy) if yon < 0 else (sy - yuz)
            if not (-0.05 <= bos <= 4.0): continue
            if any(s["hi"][k] < b["lo"][k] + 3 or s["lo"][k] > b["hi"][k] - 3 for k in uz): continue
            if eslesme is None or bos < eslesme[3]: eslesme = (d, s, yon, bos, st_)
    if eslesme is None: continue
    d, s, yon, bos, st_ = eslesme
    n = np.zeros(3); n[ax] = -yon                                       # destekten kanala doğru
    nk = 1 if L < 120 else (2 if L < 450 else 3)
    if nk == 1: ts = [0.5]
    else: ts = list(np.linspace(0.15, 0.85, nk))
    c0 = (b["lo"] + b["hi"]) / 2.0
    for j, tt in enumerate(ts):
        ad_ = []
        # v2 (4 Eki): kanal saca KÖR PERÇİNLE (kanal yerine oturduktan sonra içeriden takılır; sacta önceden çıkıntı yok → levha / sac yolları serbest).
        # Perçin ucu sacın arkasındaki PU levhada cebe açılır (levha cepli kesilir). Boşluklu (0,6–4 mm) kanalda aralık burcu.
        for (rd, rdk), dl, dw in [(r_, dl, dw) for r_ in ((4.0, 8.0), (3.2, 6.4)) for dl in (0.0, 12.0, -12.0, 25.0, -25.0, 40.0, -40.0) for dw in (0.0, 3.0, -3.0, 5.0, -5.0)]:
                p = c0.copy(); p[kL] = b["lo"][kL] + tt * L + dl; p[kW] = c0[kW] + dw
                if p[kL] < b["lo"][kL] + 6 or p[kL] > b["hi"][kL] - 6: continue
                yuz_dest = b["lo"][ax] - bos if yon < 0 else b["hi"][ax] + bos      # destek ön yüzü
                o = p.copy(); o[ax] = 0.0
                ad = "kanal_%d_%d" % (b["no"], j)
                a_bas = (yuz_dest + n[ax] * (bos + t)) * n[ax]                    # kanal taban plakasının iç yüzü
                els = []; izin = {}
                if bos > 0.6:
                    ab = dict(ad=ad + "_burc", sh=B.halka(rdk / 2.0, rd / 2.0 + 0.1, o, n, yuz_dest * n[ax], yuz_dest * n[ax] + bos), bom=["Ø%.0f × Ø%.1f aralık burcu A2, %.1f mm" % (rdk, rd + 0.2, bos)], tur="pul", n=list(np.asarray(n, float)))
                    els.append(ab); izin[ab["ad"]] = ()
                kal = st_ if (st_ < 3 and d not in ("B_KABLO__kanal", "B_SOGUTMA__sac")) else 1.2
                pr = B.kor_percin(o, -n, -a_bas, t + bos + kal + 2.5, ad + "_percin", d=rd, dk=rdk, k=1.0 if rd < 4 else 1.3, bulb=rd + 1.6)
                els.append(pr); izin[pr["ad"]] = (d, "ELK_IC__kanal", "B_KASA__pu", "B_KASA__pu_dolgu")
                ad_.append((els, izin, []))
        try:
            sec("H", ad_, ("ELK_IC__kanal", b)); SAY_H += 1
        except SystemExit as ex:
            ATLA.append((b["no"], j, str(ex), b, d, s, yon, bos, st_, ax, kL, kW, tt))
# ---- kanal içinde kabloya yer yoksa (dar kanal, kalın güç kablosu): KANAL KELEPÇESİ — 1,5 mm U kelepçe kanalın üstünden, iki ayağı saca PEM FHS-M4-6 + pul + somun
KEL = []
for (no, j, msg, b, d, s, yon, bos, st_, ax, kL, kW, tt) in ATLA:
    L = b["hi"][kL] - b["lo"][kL]
    if L < 120: continue                                                # kısa dirsek plakası: kanalın düz parçası kelepçelenir
    f = b["lo"][ax] - bos if yon < 0 else b["hi"][ax] + bos              # sac ön yüzü
    n = np.zeros(3); n[ax] = -yon
    # kanalın sactan en uzak yüzü (aynı kanal: plaka izdüşümünde 40 mm içindeki ELK_IC__kanal bileşenleri)
    on = f
    for c in KANAL:
        if any(c["hi"][k] < b["lo"][k] - 0.5 or c["lo"][k] > b["hi"][k] + 0.5 for k in (kL, kW)): continue
        u = (c["hi"][ax] if n[ax] > 0 else c["lo"][ax])
        if 0 < (u - f) * n[ax] < 40: on = u if (u - f) * n[ax] > (on - f) * n[ax] else on
    w0, w1 = b["lo"][kW], b["hi"][kW]
    ADAY = []
    for dz in (0.0, 20.0, -20.0, 40.0, -40.0, 60.0, -60.0):
      zc = b["lo"][kL] + tt * L + dz
      if zc - 10 < b["lo"][kL] + 3 or zc + 10 > b["hi"][kL] - 3: continue
      def kut(a0, a1, w_0, w_1, l0, l1):
          lo = np.zeros(3); hi = np.zeros(3)
          lo[ax], hi[ax] = sorted((f + n[ax] * a0, f + n[ax] * a1)); lo[kW], hi[kW] = w_0, w_1; lo[kL], hi[kL] = l0, l1
          return B.kutu(lo, hi)
      h = abs(on - f) + 0.5                                               # köprü kanal yüzünün 0,5 üstünde
      l0, l1 = zc - 10.0, zc + 10.0
      kel = kut(h, h + 1.5, w0 - 3.0, w1 + 3.0, l0, l1).fuse(kut(0.0, h + 1.5, w0 - 3.0, w0 - 1.5, l0, l1)).fuse(kut(0.0, h + 1.5, w1 + 1.5, w1 + 3.0, l0, l1))
      kel = kel.fuse(kut(0.0, 1.5, w0 - 13.0, w0 - 1.5, l0, l1)).fuse(kut(0.0, 1.5, w1 + 1.5, w1 + 13.0, l0, l1)).clean()
      ad = "kanal_kelepce_%d_%d" % (no, j)
      els = [dict(ad=ad, sh=kel, bom=["kanal kelepçesi AISI 304 1,5 mm (U, 4 büküm, 20 genişlik)"], tur="sac")]; izin = {ad: ()}
      for k_, wc in enumerate((w0 - 7.25, w1 + 7.25)):
          q = np.zeros(3); q[ax] = f; q[kW] = wc; q[kL] = zc; o = q.copy(); o[ax] = 0.0
          st = B.fhs("M4", 6, q, n, st_ if st_ < 3 else 1.2, ad + "_%d_saplama" % k_, "(%s)" % d)
          pu, a1 = B.pul("M4", o, n, f * n[ax] + 1.5, ad + "_%d_pul" % k_); so, a2 = B.somun("M4", o, n, a1, ad + "_%d_somun" % k_)
          els += [st, pu, so]; izin[st["ad"]] = (d,); izin[pu["ad"]] = (); izin[so["ad"]] = ()
      ADAY.append((els, izin, []))
    try:
        sec("H", ADAY, ("ELK_IC__kanal", b)); KEL.append((no, j))
    except SystemExit as ex:
        LOG("     kelepçe de sığmadı kanal[%d] %d: %s" % (no, j, ex))
ATLA = [a for a in ATLA if (a[0], a[1]) not in KEL and a[3]["hi"][a[10]] - a[3]["lo"][a[10]] >= 120]
LOG("  H: kelepçe %d" % len(KEL))
LOG("  H: %d kanal bağlantısı · atlanan %d" % (SAY_H, len(ATLA)))
for a in ATLA[:30]: LOG("     ATLA kanal[%d] %d: %s" % a[:3])
if ATLA and not KURU: raise SystemExit("ADIM 47 DUR: kanal bağlantısı yerleşmedi (%d)" % len(ATLA))

# ---- H2 · B kablo kanalları (B_KABLO__kanal: kapaklı kanal, modelde dolu kutu) — iç arka saca DIN 7337 Ø4 kör perçin (baş kanal içinde; dolu kutuda baş yuvası açılır)
IC_ARKA = [kutu_bul(g, "B_KASA__sac", (797.3, 164.5, -791.2), (2108.5, 728.0, -790.0)), kutu_bul(g, "B_KASA__sac", (2108.5, 164.5, -791.2), (4027.3, 668.0, -790.0))]
SAY_H2 = 0
for b in bc(g, "B_KABLO__kanal"):
    e = b["hi"] - b["lo"]
    if min(e) < 10 or abs(b["lo"][2] + 790.0) > 0.05: continue
    kL = 0 if e[0] > e[1] else 1; kW = 1 - kL; L = e[kL]
    nk = 1 if L < 120 else (2 if L < 450 else max(3, int(np.ceil(L / 400.0)) + 1))
    for j, tt in enumerate(np.linspace(0.12, 0.88, nk) if nk > 1 else [0.5]):
        ad_ = []
        for dl in (0.0, 15.0, -15.0, 30.0, -30.0, 50.0, -50.0):
            for dw in (0.0, 8.0, -8.0, 12.0, -12.0):
                p = (b["lo"] + b["hi"]) / 2.0; p[kL] = b["lo"][kL] + tt * L + dl; p[kW] += dw
                if p[kL] < b["lo"][kL] + 8 or p[kL] > b["hi"][kL] - 8: continue
                if not any(np.all(a["lo"][:2] + 6 <= p[:2]) and np.all(p[:2] <= a["hi"][:2] - 6) for a in IC_ARKA): continue
                o = (p[0], p[1], 0.0); ad = "bkanal_%d_%d" % (b["no"], j)
                pr = B.kor_percin(o, (0, 0, -1), 788.0, 2.0 + 1.2 + 2.5, ad + "_percin", d=4.0, dk=8.0, k=1.3, bulb=5.6)   # baş kanal içinde (taban 2), uç PU'da
                ad_.append(([pr], {pr["ad"]: ("B_KASA__sac", "B_KABLO__kanal", "B_KASA__pu")}, []))
        sec("H", ad_, ("B_KABLO__kanal", b)); SAY_H2 += 1
LOG("  H2: %d B kablo kanalı bağlantısı" % SAY_H2)

for gr in "ABCDEFGH":
    LOG("  %s: %d eleman" % (gr, sum(1 for x in EL if x[0] == gr)))
if KURU:
    LOG("KURU: %.0f sn" % (time.time() - t0)); sys.stdout.flush(); os._exit(0)

# ---------------------------------------------------------------- karşı tarafta delik / yuva
FIZ = [e for _, e, _ in EL]
kayit = K.delik_ac(FIZ + KESICI)
# PU levhaları: elemanların (perçin ucu, saplama başı) girdiği levhada cep — onarımlı katı − elemanlar
KM = []
for e in FIZ:
    P_ = SE.ucgen(e["sh"], 0.02, 0.15); m_ = SE.mf_ucgen(P_)
    if SE.vida_mi(e):
        dm = SE.dis_cap(e); ek_ = SE.eksen_bul(SE.sekil(e))
        if dm and ek_ is not None:
            o_, a_ = ek_; tt_ = (P_.reshape(-1, 3) - o_) @ a_
            m_ = m_ + SE.silindir_mf(o_, a_, SE.GECIS[dm] / 2.0, float(tt_.min()), float(tt_.max()))
    KM.append(m_)
for d in PU_D:
    for b in list(bc(g, d)):
        L_ = [m for m in KM if np.all(np.asarray(m.bounding_box()[3:]) >= b["lo"] - 0.05) and np.all(np.asarray(m.bounding_box()[:3]) <= b["hi"] + 0.05)]
        if not L_: continue
        X = onar(ucg(b))
        if X is None: raise SystemExit("ADIM 47 DUR: PU onarılamadı %s" % np.round(b["lo"], 1))
        v0 = X.volume(); Y = X - mf.Manifold.batch_boolean(L_, mf.OpType.Add)
        if v0 - Y.volume() < 1e-3: continue
        P2 = SE.mf_P(Y); ilk = [True]
        def f(_, P2=P2):
            if ilk[0]: ilk[0] = False; return P2
            return None
        g.donustur(b, f)
        kayit.append(dict(karsi="%s %s" % (d, np.round(b["lo"], 1).tolist()), cikan=round(v0 - Y.volume(), 1), eleman=len(L_)))
        LOG("  PU cebi: %s %s · −%.0f mm³ (%d eleman)" % (d, np.round(b["lo"], 1).tolist(), v0 - Y.volume(), len(L_)))
# yeni elemanlar ↔ dikme plakası / kaynak somunu: plakalar dikme düğümüne (dikmenin etiketiyle), gerisi yeni düğüme
for grup, e, (d, b) in EL:
    if e["ad"].startswith("ayak_plaka_"):
        lab = g.etiket_b(b); g.ekle_dugum(d, SE.ucgen(e["sh"].copy(), 0.08, 0.5), kat=lab[0], mek=lab[1], kpk=lab[2])
tmp = go + ".e1.glb"; g.kaydet(tmp)
ETK = {}
for grup, e, (d, b) in EL:
    ETK[e["ad"]] = g.etiket_b(b)
del g, K
H = SE.Ham(tmp)
L_ = [(e, ETK[e["ad"]]) for grup, e, ref in EL if not e["ad"].startswith("ayak_plaka_")]
nd = H.hazirla(YENI_DUG, "B_MODULER__baglanti")
pr = H.J["meshes"][nd["mesh"]]["primitives"][0]
XX, NN, II, ek, em, kp = [], [], [], [], [], []; o_ = 0; ib = 0; AR = {}
for e, (kat, mek, kpk) in L_:
    V, F = SE.tess(e["sh"].copy(), 0.08, 0.5)              # küçük bağlantı elemanı: kaba ağ (dosya boyutu)
    N = np.zeros_like(V); fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    for i in range(3): np.add.at(N, F[:, i], fn)
    N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)
    XX.append((V / 1000.0).astype(np.float32)); NN.append(N.astype(np.float32)); II.append((F.reshape(-1) + o_).astype(np.uint32))
    m = 3 * len(F); ek += [int(kat or 0), ib, m]; em += [int(mek or 0), ib, m]
    if kpk: kp += [ib, m]
    AR[e["ad"]] = (ib, m); o_ += len(V); ib += m
pr["attributes"] = {"POSITION": H._ekle(np.vstack(XX), "VEC3", 34962), "NORMAL": H._ekle(np.vstack(NN), "VEC3", 34962)}
pr["indices"] = H._ekle(np.concatenate(II).astype(np.uint32), "SCALAR", 34963)
pr["extras"] = {"kat": ek, "mek": em, "kpk": kp}
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f_ in (tmp0, tmp0 + ".o.glb", tmp, tmp + ".e2.glb"):
    if os.path.exists(f_): os.remove(f_)
PAR = {}
for grup, e, (d, b) in EL:
    PAR[e["ad"]] = dict(grup=grup, dugum=d if e["ad"].startswith("ayak_plaka_") else YENI_DUG, kutu=SE.kutu6(e), tur=e["tur"], bom=e["bom"], n=e.get("n"),
                        indis=list(AR.get(e["ad"], (0, 0))), ref="%s[%d]" % (d, b["no"]))
json.dump(dict(adim=47, ad="B bağlantı elemanları", parca=PAR, kesici=[k["ad"] for k in KESICI], karsi=kayit, duzelt=KAY, denetim=DENETIM, log=SE.LOG),
          open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=str)
LOG("ADIM 47 bitti · %d eleman · %d delik kaydı · %s · %.0f sn" % (len(EL), len(kayit), go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
