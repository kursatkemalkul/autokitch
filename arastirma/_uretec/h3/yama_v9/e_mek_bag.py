# -*- coding: utf-8 -*-
"""E MEKANİZMA BAĞLANTI MOTORU · zincir adımları 81–85 ortak araç (6 Eki 2026 · Claude · 2. oturum · KURALLAR §1.2, §2.2, §5)
Mekanizma bileşenleri veri/e_mek_parcalar.json'daki KUTULARLA bulunur (m8kit bileşeni, lo/hi ± 0,8). Her bağlantı bir satır:
  vida(A, B, ...)   : A'nın dış yüzünden B'ye (B'de dişli delik) ISO 4762 / DIN 7991 / ISO 7380 cıvata · temas yüzü kutulardan (ya da yon/duzlem verilir)
  somunlu(A, B, ...): A + B'den geçen cıvata + B'nin arka yüzünde ISO 7089 pul + ISO 10511 fiberli somun
  motor(M, B, ...)  : hazır ürün flanşından (NEMA kare deseni) bizim parçaya (B dişli) · baş flanş arkasında (gövde pahında)
  setskur(A, B, ...): DIN 916 M4 / M5 A2 · A (kaplin / kasnak / blok) dış yüzünden B'ye (mil) basar
  segman(mil, yuz)  : DIN 471 emniyet segmanı (mil üstünde, yatağın yüzüne dayanır)
  somun_mil(sensör) : silindirik M8 / M12 sensör: tutucunun yüzünde ISO 4032 somun
  sap_vida(flanş, bar): vantuz dişli sapı (M5) bar dişli deliğine
Üretim: h3_sac_v1 (vida / somun / pul / pem_somun · gerçek ölçü, BOM) · delik: sac_ent.Karsi.delik_ac (manifold boolean; cıvata + ISO 273 geçiş)
Denetim (her satırda, tutmazsa DURUR): (1) baş / somun / segman hacmi boş (pay 0,3) · (2) her vida tam olarak beklenen parçaları deliyor
(A ve B; fazla parça yok) · (3) B'de diş tutuşu ≥ 1 × d (ışınla ölçülür) · (4) vida boyu katalog serisinden.
Determinizm: sözlük sıraları sabit, set yinelemesi yok."""
import os, sys, re, json, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sac_ent as SE
from m8kit import Glb
import cadquery as cq
import h3_sac_v1 as S

LOG = SE.log
VERI = os.path.join(HERE, "veri", "e_mek_parcalar.json")
BOY = S.VIDA_BOY                                                           # [4 … 60]
SEG471 = {8: (7.6, 0.8, 11.0), 10: (9.6, 1.0, 13.5), 12: (11.5, 1.0, 15.5), 15: (14.3, 1.0, 19.0), 16: (15.2, 1.0, 20.0), 20: (19.0, 1.2, 24.5)}   # d → (groove d, t, OD)
NEMA = {56: (47.14, "M5"), 57: (47.14, "M5"), 42: (31.0, "M3"), 60: (50.0, "M5"), 86: (69.6, "M6")}
ISO4035_M = {"M4": 2.2, "M5": 2.7, "M6": 3.2, "M8": 4.0, "M10": 5.0, "M12": 6.0}                                   # ince somun yüksekliği (s: ISO 4032 ile aynı)
XYZ = "xyz"


def vek(a):
    a = np.asarray(a, float); return a / np.linalg.norm(a)


def isin(P, o, d, L=1e4, isaret=False):
    """ışın o + t d (0 < t < L) üçgenleri (n,3,3) kestiği t'ler (artan) · isaret=True: [(t, giriş −1 / çıkış +1)] (aynı t + aynı yön tek sayılır)"""
    v0, v1, v2 = P[:, 0], P[:, 1], P[:, 2]
    e1 = v1 - v0; e2 = v2 - v0; h = np.cross(d, e2); a = (e1 * h).sum(1); ok = np.abs(a) > 1e-12
    f = np.where(ok, 1.0 / np.where(ok, a, 1), 0); sv = o - v0; u = f * (sv * h).sum(1)
    q = np.cross(sv, e1); v = f * (q @ d); t = f * (e2 * q).sum(1)
    hit = ok & (u >= -1e-9) & (v >= -1e-9) & (u + v <= 1 + 1e-9) & (t > 1e-6) & (t < L)
    if not isaret: return sorted(np.unique(np.round(t[hit], 3)).tolist())
    n = np.cross(e1, e2); sg = np.where((n @ d) < 0, -1, 1)
    K = sorted(set(zip(np.round(t[hit], 3).tolist(), sg[hit].tolist())))
    return K


def kati_araliklari(P, o, d, L=1e4):
    """ışının katı içinde olduğu [t0, t1] aralıkları · giriş / çıkış sayacıyla (yüz yüze bitişik iki katı iki ayrı aralık verir; paylaşılan kenar tek sayılır)"""
    out = []; derin = 0; bas = None
    for t, sg in sorted(isin(P, o, d, L, isaret=True), key=lambda x: (x[0], -x[1])):   # aynı t'de önce çıkış (+1), sonra giriş (−1)
        if sg < 0:
            derin += 1
            if derin == 1: bas = t
        else:
            derin -= 1
            if derin <= 0:
                if bas is not None: out.append((bas, t))
                bas = None; derin = 0
    return out


def _ucgen_kutu(T, lo, hi):
    """üçgen (n,3,3) – eksen hizalı kutu kesin kesişim (ayırıcı eksen teoremi, 13 eksen) · dönüş: (n,) bool"""
    c = (lo + hi) / 2; h = (hi - lo) / 2
    V = T - c[None, None, :]
    ok = np.ones(len(T), bool)
    # 3 kutu ekseni
    for k in range(3):
        mn = V[:, :, k].min(1); mx = V[:, :, k].max(1); ok &= ~((mn > h[k]) | (mx < -h[k]))
    # üçgen normali
    e0 = V[:, 1] - V[:, 0]; e1 = V[:, 2] - V[:, 1]; e2 = V[:, 0] - V[:, 2]
    n = np.cross(e0, e1); d = (n * V[:, 0]).sum(1); r = (np.abs(n) * h[None, :]).sum(1); ok &= np.abs(d) <= r + 1e-9
    # 9 kenar × eksen çaprazı
    for e in (e0, e1, e2):
        for k in range(3):
            a = np.zeros(3); a[k] = 1.0; ax = np.cross(a[None, :], e)
            p = (V * ax[:, None, :]).sum(2); r = (np.abs(ax) * h[None, :]).sum(1)
            ok &= ~((p.min(1) > r + 1e-9) | (p.max(1) < -r - 1e-9))
    return ok


class Mek:
    def __init__(s, g, bolge_lo, bolge_hi):
        s.g = g; s.V = json.load(open(VERI, encoding="utf-8"))
        s.K = SE.Karsi(g, acik_dene=True)
        s.YENI = {}                                                       # yeni parçalar (ad → parça sözlüğü; cadquery katısı)
        s.VIDA = []; s.DIGER = []; s.kayit_vida = []; s.rapor = []; s.uyari = []
        s.bolge(bolge_lo, bolge_hi)

    # ------------------------------------------------------------ bileşen
    def yeni(s, ad, sh, bom, dugum, aile="", rol="parca", meta=None, kontrol=None, tur="parca"):
        """yeni parça (braket / tapa / kaynak dikişi): katı sh (mm, dünya) · denetim: hacmi boş (pay 0,3; kontrol: yalnız bu kutular — delikli parça;
        kontrol=[]: denetim yok, biçim komşu katıdan kesilerek kurulmuştur) · vidalarla kesilir (bitir) · tur: parca / kaynak"""
        d = []
        for lo, hi in ([s.sekil_kutu(sh)] if kontrol is None else kontrol): d += s.bos(np.asarray(lo, float), np.asarray(hi, float), 0.3)
        assert not d, "%s: yeni parça hacmi dolu %s" % (ad, sorted(set(d)))
        p = dict(ad=ad, sh=sh, bom=list(bom), tur=tur, meta=dict(meta or {}, yeni=True), dugum=dugum)
        s.YENI[ad] = p; lo, hi = s.sekil_kutu(sh)
        s.V[ad] = dict(dug=dugum, lo=lo.tolist(), hi=hi.tolist(), aile=aile, rol=rol, tip="yeni", yeni=True)
        LOG("  yeni parça %-28s %s · kutu %s → %s" % (ad, dugum, np.round(lo, 1).tolist(), np.round(hi, 1).tolist()))
        return p

    def _kutular(s, ad):
        v = s.V[ad]; K = [(v["dug"], np.array(v["lo"], float), np.array(v["hi"], float))]
        for e in v.get("ek", []): K.append((e["dug"], np.array(e["lo"], float), np.array(e["hi"], float)))
        return K

    def bs(s, ad):
        """adlı parçanın m8kit bileşenleri: ana kutu + ek kutuların içinde kalan (± 0,8) bileşenler; başka bir (daha küçük kutulu) adlı parçaya
        ait olanlar hariç (üreteç bazı parçaları yüzü yüze birkaç katıdan kurmuş: plaka + direkler; iç içe parçalar: kaplin motor bloğunun içinde)"""
        assert ad not in s.YENI, "%s yeni parça: bileşeni yok" % ad
        L = []
        for d, lo, hi in s._kutular(ad):
            if d not in s.g._bc: s.g.bilesen(d, 0)
            hac = float(np.prod(hi - lo))
            for b in s.g._bc[d]:
                if not (np.all(b["lo"] >= lo - 0.8) and np.all(b["hi"] <= hi + 0.8)): continue
                baska = False
                for a2, v2 in s.V.items():
                    if a2 == ad or v2.get("yeni"): continue
                    for d2, l2, h2 in s._kutular(a2):
                        if d2 == d and np.prod(h2 - l2) < hac and np.all(b["lo"] >= l2 - 0.8) and np.all(b["hi"] <= h2 + 0.8): baska = True; break
                    if baska: break
                if not baska and not any(b is x for x in L): L.append(b)
        assert L, "%s: kutusunda bileşen yok" % ad
        return L

    def b(s, ad):
        L = s.bs(ad); assert len(L) == 1, "%s: %d bileşen (bs kullan)" % (ad, len(L)); return L[0]

    def P(s, ad):
        if ad in s.YENI: return SE.ucgen(s.YENI[ad]["sh"], 0.05, 0.25)
        return np.concatenate([p["X"][p["T"][t]] for b in s.bs(ad) for p, t in b["parca"]])

    def ait(s, ad, dug, b):
        """m8kit bileşeni b (dug düğümünde) adlı parçaya mı ait (kutusu parçanın ana / ek kutusunda; daha küçük kutulu başka ad öncelikli)"""
        v = s.V[ad]
        if v.get("yeni"): return False
        for d, lo, hi in s._kutular(ad):
            if d != dug or not (np.all(b["lo"] >= lo - 0.8) and np.all(b["hi"] <= hi + 0.8)): continue
            hac = float(np.prod(hi - lo)); baska = False
            for a2, v2 in s.V.items():
                if a2 == ad or v2.get("yeni"): continue
                for d2, l2, h2 in s._kutular(a2):
                    if d2 == dug and np.prod(h2 - l2) < hac and np.all(b["lo"] >= l2 - 0.8) and np.all(b["hi"] <= h2 + 0.8): baska = True; break
                if baska: break
            if not baska: return True
        return False

    def kutu(s, ad):
        v = s.V[ad]; return np.array(v["lo"], float), np.array(v["hi"], float)

    # ------------------------------------------------------------ bölge üçgenleri (hacim denetimi)
    def bolge(s, lo, hi):
        s._blo = np.asarray(lo, float); s._bhi = np.asarray(hi, float)
        MN, MX, AD = [], [], []
        for p in s.g.prims:
            if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
            Q = p["X"][p["T"]]; ar = np.linalg.norm(np.cross(Q[:, 1] - Q[:, 0], Q[:, 2] - Q[:, 0]), axis=1)
            m = (ar > 1e-9) & np.all(Q.max(1) >= lo, 1) & np.all(Q.min(1) <= hi, 1)
            if not m.any(): continue
            MN.append(Q[m].min(1)); MX.append(Q[m].max(1)); AD += [p["name"]] * int(m.sum())
        s.MN = np.concatenate(MN); s.MX = np.concatenate(MX); s.AD = np.array(AD)
        s.NBB = {d: (s.MN[s.AD == d].min(0), s.MX[s.AD == d].max(0)) for d in sorted(set(AD))}   # düğüm başına bölge kutusu (içeride kalma denetimi için aday)

    def bos(s, lo, hi, pay=0.3):
        """kutu (pay kadar küçültülmüş) boş mu: önce üçgen kutularıyla kaba eleme, sonra üçgen–kutu kesin kesişim (ayırıcı eksen) ·
        hiç üçgen kesmiyorsa kutu bir katının İÇİNDE de olabilir (hiç üçgene dokunmadan da: kalın duvarın ortası) → merkezi düğüm kutusunda olan
        her düğüm için 6 yönde ışın paritesi (kapalı katı) · dönüş: dolduran düğüm adları"""
        lo = np.asarray(lo, float) + pay; hi = np.asarray(hi, float) - pay
        if np.any(hi <= lo): return []
        if not hasattr(s, "TRI"): s._tri_kur()
        m = np.all(s.MX > lo, 1) & np.all(s.MN < hi, 1)
        out = set()
        if m.any():
            idx = np.where(m)[0]; T = s.TRI[idx]; adlar = s.AD[idx]
            kes = _ucgen_kutu(T, lo, hi)
            out = set(adlar[kes].tolist())
        # kutu tümüyle bir katının içinde mi: merkezi düğümün bölge kutusunda olan düğümler için parite (kesen üçgeni olmayanlar)
        c = (lo + hi) / 2
        for d in sorted(d_ for d_, (l_, h_) in s.NBB.items() if d_ not in out and np.all(l_ <= c) and np.all(h_ >= c)):
            Td = s.TRI[s.AD == d]; ic = True
            for yon in ((1.0, 0, 0), (-1.0, 0, 0), (0, 1.0, 0), (0, -1.0, 0), (0, 0, 1.0), (0, 0, -1.0)):   # 6 yönde de tek sayıda kesişim → kapalı katının içinde
                if len(isin(Td, c, np.array(yon), 1e4)) % 2 == 0: ic = False; break
            if ic: out.add(d)
        return sorted(out)

    def _tri_kur(s):
        TRI = []
        for p in s.g.prims:
            if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
            Q = p["X"][p["T"]]; ar = np.linalg.norm(np.cross(Q[:, 1] - Q[:, 0], Q[:, 2] - Q[:, 0]), axis=1)
            m = (ar > 1e-9) & np.all(Q.max(1) >= s._blo, 1) & np.all(Q.min(1) <= s._bhi, 1)
            if m.any(): TRI.append(Q[m])
        s.TRI = np.concatenate(TRI)
        assert len(s.TRI) == len(s.AD)

    def sekil_kutu(s, sh):
        bb = sh.BoundingBox(); return np.array([bb.xmin, bb.ymin, bb.zmin]), np.array([bb.xmax, bb.ymax, bb.zmax])

    # ------------------------------------------------------------ temas yüzü
    def yuz(s, A, B, tol=0.8):
        """A ↔ B kutu bitişikliği → (eksen, A'dan B'ye yön ±1, düzlem koordinatı, örtüşme lo2, hi2 (diğer iki eksen))"""
        la, ha = s.kutu(A); lb, hb = s.kutu(B); out = []
        for a in range(3):
            o = [k for k in range(3) if k != a]
            l2 = np.maximum(la[o], lb[o]); h2 = np.minimum(ha[o], hb[o]); alan = float(np.prod(np.maximum(h2 - l2, 0)))
            if abs(ha[a] - lb[a]) <= tol: out.append((a, +1, (ha[a] + lb[a]) / 2, l2, h2, alan))
            if abs(hb[a] - la[a]) <= tol: out.append((a, -1, (hb[a] + la[a]) / 2, l2, h2, alan))
        if not out: return None
        return max(out, key=lambda x: x[5])

    @staticmethod
    def desen(l2, h2, n, pay):
        c = (l2 + h2) / 2; w = h2 - l2
        if n == 1: return [c.copy()]
        if n == 2:
            k = int(np.argmax(w)); out = []
            for f in (-1, 1):
                q = c.copy(); q[k] = c[k] + f * max(0.0, w[k] / 2 - pay); out.append(q)
            return out
        out = []
        for fx in (-1, 1):
            for fy in (-1, 1):
                out.append(np.array([c[0] + fx * max(0.0, w[0] / 2 - pay), c[1] + fy * max(0.0, w[1] / 2 - pay)]))
        if n == 3: out = out[:3]
        return out

    # ------------------------------------------------------------ cıvata
    def _duzlem(s, ad, A, B, yon, duzlem):
        if yon is None:
            y = s.yuz(A, B); assert y is not None, "%s: %s ↔ %s temas yüzü yok (yon ver)" % (ad, A, B)
            ax, sg, c, l2, h2, _ = y; e = np.zeros(3); e[ax] = sg
        else:
            e = vek(yon); ax = int(np.argmax(np.abs(e))); sg = int(np.sign(e[ax]))
            la, ha = s.kutu(A); lb, hb = s.kutu(B); o = [k for k in range(3) if k != ax]
            l2 = np.maximum(la[o], lb[o]); h2 = np.minimum(ha[o], hb[o]); c = duzlem if duzlem is not None else (ha[ax] if sg > 0 else la[ax])
        return e, ax, float(c), l2, h2

    @staticmethod
    def _birlestir(ivs, bosluk=0.05):
        """bitişik (yüz yüze) katı aralıklarını birleştir (aynı parçanın üst üste plakaları tek paket) — temas düzlemini (t = 0) geçerek birleştirmez
        (A ve B aynı parçanın iki katısı olabilir: kiriş + ayak)"""
        out = []
        for a, b in sorted(ivs):
            if out and a - out[-1][1] <= bosluk and not (out[-1][1] <= 0.3 and a >= -0.3 and abs(a) <= 0.3): out[-1] = (out[-1][0], max(out[-1][1], b))
            else: out.append((a, b))
        return out

    @staticmethod
    def _nokta(pt, o, ax, c):
        """pts öğesi: (u, w) → düzlem noktası (eksen hizalı) · (x, y, z) → doğrudan dünya noktası (eğik eksen / silindir yüzeyi)"""
        if len(pt) == 3: return np.asarray(pt, float)
        u, w = pt; p = np.zeros(3); p[o[0]] = u; p[o[1]] = w; p[ax] = c
        return p

    def _ab(s, ad, i, PA, PB, p, e):
        """düzlem noktası p'den A (geri) ve B (ileri) katı aralıkları (t: e boyunca, p'de 0) · bitişik aralıklar birleşik"""
        o0 = p - e * 300.0
        ta = s._birlestir([(t0 - 300.0, t1 - 300.0) for t0, t1 in kati_araliklari(PA, o0, e, 600.0)])
        tb = s._birlestir([(t0 - 300.0, t1 - 300.0) for t0, t1 in kati_araliklari(PB, o0, e, 600.0)])
        ia = [x for x in ta if x[1] <= 0.8 and x[1] >= -80.0]; ib = [x for x in tb if x[0] >= -0.8 and x[0] <= 80.0]
        assert ia and ib, "%s #%d: ışın A/B'yi bulamadı · A %s · B %s · nokta %s" % (ad, i, [tuple(round(v, 1) for v in x) for x in ta], [tuple(round(v, 1) for v in x) for x in tb], np.round(p, 1).tolist())
        a0 = max(ia, key=lambda x: x[1])[0]; b0, b1 = min(ib, key=lambda x: x[0])
        return float(a0), float(b0), float(b1)

    def vida(s, ad, A, B, n=2, dis="M5", std="ISO4762", yon=None, duzlem=None, pts=None, pay=None, gomme=0.0, kavrama=None, boy=None,
             hedef_ek=(), bas_bos=None, not_="", urun=None):
        """A'nın dış yüzünden B'ye (dişli) cıvata · yon: A → B birim vektör (yoksa kutulardan) · duzlem: temas koordinatı (eksen boyunca)
        pts: [(u, w)] diğer iki eksendeki noktalar (yoksa desen) · gomme: baş A'nın dış yüzünden bu kadar içeride (gömme yuva) · kavrama: B'de diş boyu ·
        urun: 'A' → A hazır ürün, vida ürünün KENDİ deliğinden geçer (delik ağda olabilir: delme beklenmez, isteğe bağlı)"""
        d = S.D_NOM[dis]
        e, ax, c, l2, h2 = s._duzlem(ad, A, B, yon, duzlem); o = [k for k in range(3) if k != ax]
        if pts is None: pts = s.desen(l2, h2, n, pay if pay is not None else max(1.0 * d + 1.0, 4.0))
        PA = s.P(A); PB = s.P(B); out = []
        for i, pt in enumerate(pts):
            p = s._nokta(pt, o, ax, c)
            a0, b0, b1 = s._ab(ad, i, PA, PB, p, e)
            st = a0 + gomme                                                   # baş oturma (t)
            dB = b1 - b0
            if kavrama is not None and kavrama >= 1.0 * d - 1e-6 and kavrama <= dB + 1e-6: kav = kavrama   # açık verilen tutuş (≥ 1×d, B içinde)
            else:
                kav = kavrama if kavrama is not None else min(1.5 * d, dB - 1.0)
                if kav < 1.0 * d:
                    assert dB >= 1.0 * d + 0.5, "%s #%d: B kalınlığı %.1f < 1×d+0,5 (somunlu bağlantı gerek)" % (ad, i, dB)
                    kav = min(1.0 * d + 0.5, dB - 0.5)
            L = -st + b0 + kav
            if boy is not None: Lb = float(boy)
            else:
                Lb = next((x for x in BOY if x >= L - 1e-6), None); assert Lb is not None, "%s: boy %.1f katalog dışı" % (ad, L)
                if Lb > -st + b1 - 0.5 and kav < dB - 1e-6:                   # B'yi deler geçerdi → bir alt boy (tam tutuş istendiyse uç yüzle aynı düzlem)
                    alt = [x for x in BOY if x <= -st + b1 - 0.5 and x >= -st + b0 + 1.0 * d]
                    assert alt, "%s #%d: uygun boy yok (A %.1f · B %.1f · gerek %.1f)" % (ad, i, -a0, dB, L)
                    Lb = alt[-1]
            nokta = tuple((p + e * st).tolist())
            nm = "%s_%d" % (ad, i) if len(pts) > 1 else ad
            v = S.vida(std, dis, float(Lb), nokta, tuple(e.tolist()), ad=nm)
            v["mek_bag"] = dict(A=A, B=B, eks=e.tolist(), seat=float(p[ax] + e[ax] * st), kav=round(float(min(Lb + st - b0, dB)), 2),
                                hedef=([B] if urun == "A" else [A, B]) + list(hedef_ek), ops=([A] if urun == "A" else []),
                                bas_bos=(gomme <= 0) if bas_bos is None else bas_bos, not_=not_, tA=round(-a0, 1), tB=round(dB, 1))
            out.append(v)
        s.VIDA += out
        LOG("  vida %-34s %s×%-3g ×%d  %s → %s · eksen %s · A %s · B %s · kavrama %s" % (ad, dis, out[0]["meta"]["boy"], len(out), A, B, np.round(e, 2).tolist(),
            [o_["mek_bag"]["tA"] for o_ in out], [o_["mek_bag"]["tB"] for o_ in out], [o_["mek_bag"]["kav"] for o_ in out]))
        return out

    # ------------------------------------------------------------ somunlu cıvata (A + B'den geçer, B arkasında pul + fiberli somun)
    def somunlu(s, ad, A, B, n=2, dis="M5", std="ISO4762", yon=None, duzlem=None, pts=None, pay=None, bas_bos=True, not_="", hedef_ek=()):
        d = S.D_NOM[dis]
        e, ax, c, l2, h2 = s._duzlem(ad, A, B, yon, duzlem); o = [k for k in range(3) if k != ax]
        if pts is None: pts = s.desen(l2, h2, n, pay if pay is not None else max(1.0 * d + 1.0, 4.0))
        PA = s.P(A); PB = s.P(B); out = []; ph = S.DIN125[dis][2]; sm = S.ISO10511[dis][1]
        for i, pt in enumerate(pts):
            p = s._nokta(pt, o, ax, c)
            a0, b0, b1 = s._ab(ad, i, PA, PB, p, e)
            L = -a0 + b1 + ph + sm + 0.5 * d
            Lb = next((x for x in BOY if x >= L - 1e-6), None); assert Lb, ad
            nokta = tuple((p + e * a0).tolist()); ek = tuple(e.tolist()); nm = "%s_%d" % (ad, i) if len(pts) > 1 else ad
            v = S.vida(std, dis, float(Lb), nokta, ek, ad=nm)
            v["mek_bag"] = dict(A=A, B=B, eks=e.tolist(), seat=float(p[ax] + e[ax] * a0), kav=round(float(Lb + a0 - b1), 2), hedef=[A, B] + list(hedef_ek), bas_bos=bas_bos, not_=not_, somunlu=True,
                                tA=round(-a0, 1), tB=round(b1 - b0, 1))
            pu = S.pul("DIN125", dis, tuple((p + e * b1).tolist()), ek, ad=nm + "_pul")
            so = S.somun("ISO10511", dis, tuple((p + e * (b1 + ph)).tolist()), ek, ad=nm + "_somun")
            for q in (pu, so): q["mek_bag"] = dict(A=A, B=B, eks=e.tolist(), hacim=True)
            out.append(v); s.DIGER += [pu, so]
        s.VIDA += out
        LOG("  somunlu %-31s %s×%-3g ×%d  %s → %s · pul + fiberli somun · taşma %s" % (ad, dis, out[0]["meta"]["boy"], len(out), A, B, [o_["mek_bag"]["kav"] for o_ in out]))
        return out

    # ------------------------------------------------------------ hazır ürün: motor (NEMA flanşı)
    def motor(s, ad, M, B, yon, flans=None, kare=None, dis=None, boy_flans=10.0, kav=14.0, merkez=None, n=4, not_="", hedef_ek=(), merkez3=None, u_vec=None):
        """M motor, B bizim parça (dişli) · yon: motordan B'ye (motor ekseni) · flans: flanş düzleminin koordinatı (B'nin yüzü) ·
        baş flanşın arkasında (gövde köşe pahında · gömme yuva delik açmada oyulur) · kare: delik kare kenarı (NEMA) · merkez: eksen merkezi (u, w)
        EĞİK eksen: merkez3 = flanş düzlemindeki eksen noktası (x, y, z) + u_vec = flanş düzleminde kare kenar yönü (ikinci kenar e × u)"""
        e = vek(yon); ax = int(np.argmax(np.abs(e))); o = [k for k in range(3) if k != ax]
        lm, hm = s.kutu(M); wm = hm - lm; en = sorted([wm[o[0]], wm[o[1]]])
        if kare is None:
            kk = min(NEMA, key=lambda k: abs(k - en[0])); kare, dis0 = NEMA[kk]
        else: dis0 = "M5"
        dis = dis or dis0; d = S.D_NOM[dis]
        L = boy_flans + kav; Lb = next(x for x in BOY if x >= L - 1e-6)
        if merkez3 is not None:                                                # eğik: 3B köşe noktaları flanş düzleminde
            c3 = np.asarray(merkez3, float); uu = vek(u_vec); ww = vek(np.cross(e, uu))
            P3 = [c3 + fx * kare / 2 * uu + fy * kare / 2 * ww for fx in (-1, 1) for fy in (-1, 1)][:n]
            flans_txt = "merkez %s" % np.round(c3, 2).tolist()
        else:
            c = np.array([(lm[o[0]] + hm[o[0]]) / 2, (lm[o[1]] + hm[o[1]]) / 2]) if merkez is None else np.asarray(merkez, float)
            P3 = []
            for fx in (-1, 1):
                for fy in (-1, 1):
                    u, w = c + np.array([fx, fy]) * kare / 2
                    p = np.zeros(3); p[o[0]] = u; p[o[1]] = w; p[ax] = flans; P3.append(p)
            P3 = P3[:n]; flans_txt = "flanş %s=%.1f" % (XYZ[ax], flans)
        out = []
        for i, p3 in enumerate(P3):
            p = p3 - e * boy_flans                                            # baş oturma: flanş düzleminden boy_flans geride
            v = S.vida("ISO4762", dis, float(Lb), tuple(p.tolist()), tuple(e.tolist()), ad="%s_%d" % (ad, i))
            v["mek_bag"] = dict(A=M, B=B, eks=e.tolist(), seat=float(p[ax]), kav=round(Lb - boy_flans, 2), hedef=[B] + list(hedef_ek), ops=[M], bas_bos=False,
                                not_=not_ or "hazır ürün flanş deliğinden (gövde köşe pahı); üründen %d × %s dişli delik İSTENMEZ — bizim parça dişli" % (n, dis))
            out.append(v)
        s.VIDA += out
        LOG("  motor %-33s %s×%-3g ×%d  %s → %s · %s · kare %.2f" % (ad, dis, Lb, n, M, B, flans_txt, kare))
        return out

    # ------------------------------------------------------------ setskur (DIN 916) · A dış yüzünden B'ye basar
    def setskur(s, ad, A, B, yon, pts=None, dis="M4", n=1, bat=0.4, not_=""):
        e = vek(yon); ax = int(np.argmax(np.abs(e))); o = [k for k in range(3) if k != ax]
        la, ha = s.kutu(A); lb, hb = s.kutu(B); d = S.D_NOM[dis]
        if pts is None:
            l2 = np.maximum(la[o], lb[o]); h2 = np.minimum(ha[o], hb[o]); c2 = (l2 + h2) / 2
            if n == 1: pts = [c2]
            else:
                k = int(np.argmax(h2 - l2)); pts = []
                for f in (-1, 1):
                    q = c2.copy(); q[k] = c2[k] + f * max(0.0, (h2[k] - l2[k]) / 2 - d - 1); pts.append(q)
        PA = s.P(A); PB = s.P(B); out = []
        for i, pt in enumerate(pts):
            p = s._nokta(pt, o, ax, la[ax] if e[ax] > 0 else ha[ax]); o0 = p - e * 150.0   # ışın: A kutusu yüzündeki (ya da verilen 3B) noktadan 150 geriden
            ta = kati_araliklari(PA, o0, e, 300.0); tb = kati_araliklari(PB, o0, e, 300.0)
            assert ta and tb, "%s #%d: ışın A/B yok %s %s" % (ad, i, ta, tb)
            t0 = ta[0][0]; tbb = [x for x in tb if x[0] > t0]
            assert tbb, "%s #%d: B, A'nın dış yüzünden sonra değil" % (ad, i)
            t1 = tbb[0][0] + bat; L = t1 - t0
            Lb = next(x for x in BOY if x >= L - 1e-6)
            nokta = o0 + e * (t1 - Lb)                                        # katalog boyu: dış ucu A yüzünden (Lb − L) kadar taşar
            sh = cq.Solid.makeCylinder(d / 2 - 0.02, Lb, cq.Vector(*nokta), cq.Vector(*e))
            nm = "%s_%d" % (ad, i) if len(pts) > 1 else ad
            q = S._bp(nm, sh, "DIN 916", "Setskur vida (dişli pim, çukur uçlu) %s×%g" % (dis, Lb), "%s×%g" % (dis, Lb), "A2-70", meta=dict(dis=dis, boy=Lb, setskur=True))
            q["mek_bag"] = dict(A=A, B=B, eks=e.tolist(), seat=float(nokta[ax]), kav=round(L - bat, 2), hedef=[A, B], bas_bos=False, not_=not_ or "DIN 916 A2 setskur (standart listesine ek; mil / kaplin tespiti)")
            out.append(q)
        s.VIDA += out
        LOG("  setskur %-31s %s×%-3g ×%d  %s → %s · eksen %s" % (ad, dis, out[0]["meta"]["boy"], len(out), A, B, np.round(e, 2).tolist()))
        return out

    # ------------------------------------------------------------ silindirik pim DIN 7 (linkaj mafsalı: A'dan B'ye)
    def pim(s, ad, A, B, yon, pts, cap=3.0, boy=None, not_="", giris=0.0):
        """A'nın dış yüzünden girer, A + B'yi geçer (boy: verilmezse A dış yüzünden B'nin arka yüzüne 1 mm kala) · delik tam pim çapı (geçiş silindiri yok) ·
        giris: pimin ucu A'nın dış yüzünden bu kadar içeride başlar (çevre parçaya sürtmesin)"""
        e = vek(yon); ax = int(np.argmax(np.abs(e))); o = [k for k in range(3) if k != ax]
        PA = s.P(A); PB = s.P(B); out = []
        la, ha = s.kutu(A)
        for i, pt in enumerate(pts):
            p = s._nokta(pt, o, ax, la[ax] if e[ax] > 0 else ha[ax]); o0 = p - e * 150.0
            ta = s._birlestir(kati_araliklari(PA, o0, e, 300.0)); tb = s._birlestir(kati_araliklari(PB, o0, e, 300.0))
            assert ta and tb, "%s #%d: ışın A/B yok %s %s" % (ad, i, ta, tb)
            t0 = ta[0][0]; tbb = [x for x in tb if x[1] > t0 + 0.5]
            assert tbb, "%s #%d: B, A'nın dış yüzünden sonra değil" % (ad, i)
            L = (boy if boy is not None else (tbb[-1][1] - 1.0 - t0))
            Lc = next((x for x in BOY if x >= L - 1e-6), None) if boy is None else boy
            if Lc is None or Lc > tbb[-1][1] - t0 - 0.3: Lc = float(math.floor(L))
            nokta = o0 + e * (t0 + giris)
            sh = cq.Solid.makeCylinder(cap / 2 - 0.01, Lc, cq.Vector(*nokta), cq.Vector(*e))
            nm = "%s_%d" % (ad, i) if len(pts) > 1 else ad
            q = S._bp(nm, sh, "DIN 7", "Silindirik pim Ø%g×%g (linkaj mafsalı, sıkı geçme)" % (cap, Lc), "Ø%g×%g" % (cap, Lc), "A2 (1.4305)", meta=dict(cap=cap, boy=Lc, pim=True))
            q["mek_bag"] = dict(A=A, B=B, eks=e.tolist(), seat=float(nokta[ax]), kav=None, hedef=[A, B], bas_bos=False, not_=not_ or "DIN 7 pim (standart listesine ek; linkaj mafsalı)")
            out.append(q)
        s.VIDA += out
        LOG("  pim %-35s Ø%g×%-3g ×%d  %s → %s · eksen %s" % (ad, cap, out[0]["meta"]["boy"], len(out), A, B, np.round(e, 2).tolist()))
        return out

    # ------------------------------------------------------------ segman DIN 471 (mil üstünde, yüzde)
    def segman(s, ad, mil, yuz_koord, yon, cap=None, merkez=None):
        """yon: milin ekseni boyunca segmanın oturduğu yüzden DIŞA doğru (segman yüzün hemen dışında) · cap: mil çapı (yoksa kutudan) ·
        merkez: eğik mil için segman merkezi (x, y, z) (yüz üstünde, mil ekseninde)"""
        e = vek(yon); ax = int(np.argmax(np.abs(e))); o = [k for k in range(3) if k != ax]
        lm, hm = s.kutu(mil); dm = cap or float(round(min(hm[o[0]] - lm[o[0]], hm[o[1]] - lm[o[1]])))
        k = min(SEG471, key=lambda x: abs(x - dm)); dg, t, od = SEG471[k]
        if merkez is not None: c = np.asarray(merkez, float)
        else: c = np.zeros(3); c[o[0]] = (lm[o[0]] + hm[o[0]]) / 2; c[o[1]] = (lm[o[1]] + hm[o[1]]) / 2; c[ax] = yuz_koord
        sh = cq.Solid.makeCylinder(od / 2, t, cq.Vector(*c), cq.Vector(*e)).cut(cq.Solid.makeCylinder(dg / 2, t + 2, cq.Vector(*(c - e)), cq.Vector(*e)))
        q = S._bp(ad, sh, "DIN 471", "Emniyet segmanı (dış) %g" % k, "d%g × s%g" % (k, t), "A2 yay çeliği", meta=dict(cap=k, t=t, segman=True))
        q["mek_bag"] = dict(A=mil, B=None, eks=e.tolist(), hacim=True, yuz=yuz_koord)
        s.DIGER.append(q)
        LOG("  segman %-32s DIN 471 d%g · %s · yüz %s=%.1f" % (ad, k, mil, XYZ[ax], yuz_koord))
        return q

    # ------------------------------------------------------------ silindirik sensör somunu (tutucunun yüzünde)
    def somun_mil(s, ad, sensor, tutucu, yon, dis="M8", yuz=None, ince=False, cep=None):
        """yon: tutucudan dışarı (somunun oturduğu yüzün normali) · sensör ekseni boyunca · yuz: yüzün eksen koordinatı (yoksa tutucu kutusundan) ·
        ince: ISO 4035 ince somun (dar yer: boşlukta ikinci somun) · cep: somun bu (bizim) parçanın içine açılan altıgen cebe oturur (yüz = cebin tabanı;
        hacim denetiminde o düğüm sayılmaz, delik açmada somun katısı o parçadan kesilir)"""
        e = vek(yon); ax = int(np.argmax(np.abs(e))); o = [k for k in range(3) if k != ax]
        ls, hs = s.kutu(sensor); lt, ht = s.kutu(tutucu)
        c = np.zeros(3); c[o[0]] = (ls[o[0]] + hs[o[0]]) / 2; c[o[1]] = (ls[o[1]] + hs[o[1]]) / 2; c[ax] = (ht[ax] if e[ax] > 0 else lt[ax]) if yuz is None else float(yuz)
        if ince:
            sm, m = S.ISO4032[dis][0], ISO4035_M[dis]; d = S.D_NOM[dis]
            sh = S._altigen(sm, m).cut(S._silindir(d / 2, m + 0.02, -0.01))
            q = S._bp(ad, S._tasi(sh, S._cerceve(tuple(c.tolist()), tuple(e.tolist()))), "ISO 4035", "İnce altıgen somun %s" % dis, "%s s%g m%g" % (dis, sm, m), "A2", meta=dict(dis=dis, s=sm, m=m))
        else:
            q = S.somun("ISO4032", dis, tuple(c.tolist()), tuple(e.tolist()), ad=ad)
        q["meta"]["somun_mil"] = True
        q["mek_bag"] = dict(A=sensor, B=tutucu, eks=e.tolist(), hacim=True)
        if cep: q["mek_bag"]["cep"] = cep; q["mek_bag"]["cep_dugum"] = s.V[cep]["dug"]; q["meta"]["cep"] = True
        s.DIGER.append(q)
        LOG("  sensör somunu %-25s %s %s · %s → %s%s" % (ad, "ISO 4035 ince" if ince else "ISO 4032", dis, sensor, tutucu, (" · cep: %s" % cep) if cep else ""))
        return q

    # ------------------------------------------------------------ vantuz dişli sapı → bar (dişli delik)
    def sap_vida(s, ad, flans, bar, yon, dis="M5", boy=8.0):
        e = vek(yon); ax = int(np.argmax(np.abs(e))); o = [k for k in range(3) if k != ax]
        lf, hf = s.kutu(flans); d = S.D_NOM[dis]
        c = np.zeros(3); c[o[0]] = (lf[o[0]] + hf[o[0]]) / 2; c[o[1]] = (lf[o[1]] + hf[o[1]]) / 2; c[ax] = (hf[ax] if e[ax] > 0 else lf[ax]) - e[ax] * 1.0
        sh = cq.Solid.makeCylinder(d / 2 - 0.02, boy + 1.0, cq.Vector(*c), cq.Vector(*e))
        q = S._bp(ad, sh, "ürün sapı", "Vantuz dişli sapı %s×%g (ürünün kendi)" % (dis, boy), "%s×%g" % (dis, boy), "A2", meta=dict(dis=dis, boy=boy, sap=True))
        q["bom"] = ("Vantuz dişli sapı (vida) %s×%g · ürünün kendi · bara dişli deliğe" % (dis, boy),) + tuple(q["bom"][1:])
        q["mek_bag"] = dict(A=flans, B=bar, eks=e.tolist(), seat=float(c[ax]), kav=boy, hedef=[flans, bar], bas_bos=False, not_="vantuz sapı bardaki dişli deliğe")
        s.VIDA.append(q)
        LOG("  vantuz sapı %-27s %s×%g · %s → %s" % (ad, dis, boy, flans, bar))
        return q

    # ------------------------------------------------------------ denetim + delik + yazma
    def _bas_kutu(s, v):
        """baş kutusu: vida katısının kutusu, oturma düzleminde kırpılmış · eğik eksende başın düzlemi aşan dilimi (r · sin θ) kadar içeri çekilir"""
        sh = SE.sekil(v); e = np.asarray(v["mek_bag"]["eks"], float); ax = int(np.argmax(np.abs(e))); o = [k for k in range(3) if k != ax]
        lo, hi = s.sekil_kutu(sh); seat = v["mek_bag"]["seat"]
        sn = float(np.sqrt(max(0.0, 1.0 - e[ax] * e[ax])))
        dil = 0.5 * max(hi[o[0]] - lo[o[0]], hi[o[1]] - lo[o[1]]) * sn if sn > 1e-9 else 0.0
        if e[ax] > 0: hi[ax] = min(hi[ax], seat - dil)
        else: lo[ax] = max(lo[ax], seat + dil)
        return lo, hi

    def denetle_hacim(s):
        """baş (A'nın dış yüzünün ötesi) · pul / somun / segman gövdesi boş mu"""
        kotu = []
        for v in s.VIDA:
            if not v["mek_bag"].get("bas_bos", True): continue
            lo, hi = s._bas_kutu(v); d = s.bos(lo, hi)
            d = [x for x in d]
            if d: kotu.append((v["ad"], "baş", d))
        for q in s.DIGER:
            lo, hi = s.sekil_kutu(SE.sekil(q)); A = q["mek_bag"].get("A"); d = []
            if A and (q["meta"].get("segman") or q["meta"].get("somun_mil")):
                # halka: milin / sensörün çevresindeki 4 dilim (milin kendi kutusu hariç)
                la, ha = s.kutu(A); e = np.asarray(q["mek_bag"]["eks"], float); ax = int(np.argmax(np.abs(e))); o = [k for k in range(3) if k != ax]
                for k in o:
                    for taraf in (0, 1):
                        l2 = lo.copy(); h2 = hi.copy()
                        if taraf == 0: h2[k] = min(h2[k], la[k])
                        else: l2[k] = max(l2[k], ha[k])
                        d += s.bos(l2, h2, 0.35)
                d = sorted(set(d))
            else:
                d = s.bos(lo, hi, 0.35)
            if q["mek_bag"].get("cep_dugum"): d = [x for x in d if x != q["mek_bag"]["cep_dugum"]]   # cep: o parça bilerek oyulur
            if d: kotu.append((q["ad"], q["meta"].get("segman") and "segman" or "somun/pul", d))
        return kotu

    def denetle_delik(s):
        """her vida tam olarak beklenen parçaları deliyor mu (+ kavrama)"""
        s.K = SE.Karsi(s.g, acik_dene=True)
        kotu = []; s.hedefler = {}
        for v in s.VIDA:
            m, P = SE.kesici(v); vur = s.K.tara(v, m, P)
            bek = v["mek_bag"]["hedef"]; ops = v["mek_bag"].get("ops", [])
            bulunan = []
            for d, b, vol in vur:
                if vol <= 0: continue
                adlar = [a for a in list(bek) + list(ops) if a and s.ait(a, d, b)]
                bulunan.append((d, b["no"], round(vol, 1), adlar[0] if adlar else None))
            adl = [x[3] for x in bulunan if x[3]]
            eksik = [a for a in bek if a and a not in adl and a not in s.YENI]
            fazla = [x for x in bulunan if not x[3]]
            if eksik or fazla: kotu.append((v["ad"], "eksik %s" % eksik if eksik else "", "fazla %s" % fazla if fazla else ""))
            s.hedefler[v["ad"]] = bulunan
        return kotu

    def kavrama_kotu(s):
        return [(v["ad"], v["mek_bag"]["kav"]) for v in s.VIDA if v["mek_bag"].get("kav") is not None and not v["mek_bag"].get("somunlu") and not v["meta"].get("setskur") and not v["meta"].get("sap") and not v["meta"].get("pim")
                and v["mek_bag"]["kav"] < 1.0 * S.D_NOM[v["meta"]["dis"]] - 1e-6]

    def delik_ac(s):
        kayit = s.K.delik_ac(s.VIDA + [q for q in s.DIGER if q["meta"].get("segman") or q["meta"].get("cep")])   # cep: somun altıgeni parçadan oyulur
        s.kayit_vida = kayit
        return kayit

    def ozet(s):
        import collections
        c = collections.Counter()
        for v in s.VIDA: c[("%s %s×%g" % (v["std"], v["meta"]["dis"], v["meta"]["boy"])) if not (v["meta"].get("setskur") or v["meta"].get("pim")) else ("DIN 916 %s" % v["meta"]["dis"] if v["meta"].get("setskur") else "DIN 7 Ø%g" % v["meta"]["cap"])] += 1
        for q in s.DIGER: c[q["std"] + " " + str(q["meta"].get("dis") or q["meta"].get("cap"))] += 1
        return c

    # ------------------------------------------------------------ bitir: denetim → delik → düğümler → sıkıştır → kayıt
    def bitir(s, go, dugum_vida, adim, mek=36, mek_kod="E/Kutu katlama", ek_dugum=None, ek=None, sablon="E_GOVDE__celik", kat=0):
        """ek_dugum: {düğüm adı: [parça]} (yeni braket vb.) · ek: kayda eklenecek sözlük"""
        t0 = time.time()
        kh = s.denetle_hacim()
        for k in kh: LOG("  HACİM DOLU: %s (%s) ← %s" % k)
        assert not kh, "ADIM %s DUR: %d baş / somun / segman hacmi dolu" % (adim, len(kh))
        kk = s.kavrama_kotu()
        assert not kk, "ADIM %s DUR: diş tutuşu < 1×d: %s" % (adim, kk)
        kd = s.denetle_delik()
        for k in kd: LOG("  DELİK: %s %s %s" % k)
        assert not kd, "ADIM %s DUR: %d vida beklenen parçaları delmiyor" % (adim, len(kd))
        LOG("  denetim: %d vida + %d diğer · baş hacmi boş · hedefler tam · kavrama ≥ 1×d · %.0f sn" % (len(s.VIDA), len(s.DIGER), time.time() - t0))
        kayit = s.delik_ac()
        # yeni parçalar: hedefi olan vidaların katısı ∪ geçiş silindiri ile kesilir (cadquery)
        for ad, p in s.YENI.items():
            kes = [v for v in s.VIDA if ad in v["mek_bag"]["hedef"]]
            if not kes: continue
            sh = p["sh"]
            for v in kes:
                vs = SE.sekil(v); sh = sh.cut(vs)
                if SE.vida_mi(v):
                    dis = SE.dis_cap(v); e = SE.eksen_bul(vs)
                    if dis and e is not None:
                        o_, a_ = e; Pv = SE.ucgen(vs, 0.05, 0.3).reshape(-1, 3); t = (Pv - o_) @ a_
                        sh = sh.cut(cq.Solid.makeCylinder(SE.GECIS[dis] / 2.0, float(t.max() - t.min()), cq.Vector(*(o_ + a_ * t.min())), cq.Vector(*a_)))
            p["sh"] = sh.clean() if hasattr(sh, "clean") else sh
            LOG("  yeni parça kesildi: %s ← %s" % (ad, ", ".join(v["ad"] for v in kes)))
        tmp = go + ".e1.glb"; s.g.kaydet(tmp)
        H = SE.Ham(tmp)
        TUM = {dugum_vida: s.VIDA + s.DIGER}
        SAB = (ek_dugum or {}).get("_sablon", {})
        for d, L_ in (ek_dugum or {}).items():
            if d != "_sablon": TUM[d] = L_
        for ad, p in s.YENI.items(): TUM.setdefault(p["dugum"], []).append(p)
        for d in sorted(TUM):
            var = H.dugum(d) is not None and "mesh" in H.dugum(d)
            H.koy(d, TUM[d], kat=kat, mek=mek, kpk_fn=lambda a: False, sablon=SAB.get(d, sablon), ekle=var)   # önceki adımın düğümü varsa üstüne eklenir
        H.yaz(tmp + ".e2.glb")
        SE.sikistir(tmp + ".e2.glb", go)
        for f in (tmp, tmp + ".e2.glb"): os.remove(f)
        for d in TUM: H.aralik[d] = {p["ad"]: (0, 0) for p in TUM[d]}
        bag = {v["ad"]: dict(v["mek_bag"], std=v["std"], dis=v["meta"].get("dis"), boy=v["meta"].get("boy")) for v in s.VIDA}
        bag.update({q["ad"]: dict(q["mek_bag"], std=q["std"], dis=q["meta"].get("dis"), cap=q["meta"].get("cap")) for q in s.DIGER})
        for ad, p in s.YENI.items(): bag[ad] = dict(yeni=True, dugum=p["dugum"], bom=p["bom"])
        SE.ent_json(go[:-4] + "_ent.json", "E_MEK_%s" % adim, [(d, TUM[d]) for d in sorted(TUM)], H.aralik, lambda a: False, mek_kod, (), kayit,
                    ek=dict(ek or {}, baglanti=bag, ozet={k: v for k, v in s.ozet().items()}, uyari=s.uyari))
        LOG("ADIM %s bitti · %s · %d vida/setskur · %d somun/pul/segman · %s · %.0f sn" % (adim, go, len(s.VIDA), len(s.DIGER), dict(s.ozet()), time.time() - t0))
