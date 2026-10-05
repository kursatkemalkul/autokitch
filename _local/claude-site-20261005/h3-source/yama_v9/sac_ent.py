# -*- coding: utf-8 -*-
"""HAT v3.9 · ADIM 5-ENTEGRASYON ORTAK ARAÇLARI (gece 2 · 4 Eki 2026 · Claude · YEREL) — zincir adımları 33–36 (A, B, E, U üretim sacı).

Her adım: girdi GLB → çıktı GLB. İki evre:
  EVRE 1 (m8kit · karşı taraf): ARAYÜZ elemanlarının (cıvata, PEM, perçin somun, saplama) geçtiği MEVCUT parçalara delik açılır —
     manifold3d tam boolean FARK: kesici = elemanın kendi katısı ∪ (cıvata / saplama ise) ISO 273 orta geçiş deliği silindiri (eleman ekseni,
     eleman boyunca). Havşa başlı cıvatada baş katısı havşayı da açar. Karşı parçanın kapalı katı bileşeni (govde_denetim_dogru.bilesenler)
     yerinde yeni üçgenlerle değişir (etiketi aynı). Açık (kapalı olmayan) bileşen kesilemez → günlüğe yazılır.
     Karşı parçaya ait preslenen / perçinlenen eleman (PEM somun, perçin somun) karşı parçanın düğümüne eklenir (o düğümün montaj etiketiyle).
  EVRE 2 (ham GLB · gövde): istasyonun eski gövde düğümleri boşaltılır, üretim sacı parçaları (üreteçten, dünya koordinatı) düğümlere yazılır —
     tessellate 0,05 mm / 0,25 rad (bağımsız denetimdeki ağ), indisli, yüz başına normal · kat / mek tüm düğüm aralığına · kpk = kapakla dönenler.
  Sonunda tg/glb_sikistir (yetim tamponlar atılır). Çıktının yanına <çıktı>_ent.json (parça → düğüm + kutu + üçgen aralığı, delik günlüğü).
Determinizm: üreteçler deterministik (CadQuery), sözlük sıraları sabit, set yinelemesi yok → aynı girdi aynı çıktıyı BAYT BAYT verir."""
import os, sys, json, struct, re, subprocess, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KOK = os.environ.get("YAMA_IS_KOK") or os.getcwd()                    # zincir iş klasörü (betikler oradan çağrılır)
URETEC = os.environ.get("YAMA_URETEC") or os.path.normpath(os.path.join(HERE, "..", ".."))
H3 = os.path.join(URETEC, "h3")
os.environ.setdefault("AUTOKITCH_SAC_STANDART", os.path.join(HERE, "sac_standart"))   # K / A / B / E / U sac standardı (h3_sac_v1) — scratchpad/sac_standart ile bayt aynı
os.environ["ADIM5"] = os.path.join(HERE, "veri")                       # E / U üreteci: _bilesen_v8zq.pkl (v8zq bileşen kutuları → mekanizma FHP saplamaları) burada; üreteç yalnız OKUR
for _p in (os.path.join(KOK, "gece"), KOK, URETEC, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a); LOG.append(s); print(s, flush=True)


# =====================================================================================================================================
# geometri
# =====================================================================================================================================
def sekil(p):
    if p.get("sh") is not None: return p["sh"]
    w = p["wp"]; vs = w.vals()
    import cadquery as cq
    return vs[0] if len(vs) == 1 else cq.Compound.makeCompound(vs)


def tess(sh, tol=0.05, aci=0.25):
    vs, ts = sh.tessellate(tol, aci)
    V = np.array([(v.x, v.y, v.z) for v in vs], float); F = np.array(ts, np.int64).reshape(-1, 3)
    return V, F


def ucgen(sh, tol=0.05, aci=0.25):
    V, F = tess(sh, tol, aci); return V[F]


def mf_ucgen(P):
    """üçgenler (n,3,3) → manifold3d katısı (köşeler konumla birleşir) · kapalı değilse None"""
    import manifold3d as mf
    if not len(P): return None
    R = np.round(P.reshape(-1, 3), 4); u, inv = np.unique(R, axis=0, return_inverse=True)
    F = inv.reshape(-1, 3)
    F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
    try:
        m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=F.astype(np.uint32)))
    except Exception:
        return None
    if m.status() != mf.Error.NoError or m.is_empty(): return None
    return m


def mf_P(m):
    me = m.to_mesh(); V = np.asarray(me.vert_properties, float)[:, :3]; F = np.asarray(me.tri_verts, np.int64)
    return V[F]


GECIS = {"M3": 3.4, "M4": 4.5, "M5": 5.5, "M6": 6.6, "M8": 9.0, "M10": 11.0, "M12": 13.5}   # ISO 273 orta seri


def dis_cap(p):
    for s in ([p.get("meta", {}).get("dis")] + [str(x) for x in (p.get("bom") or ())] + [p["ad"]]):
        if not s: continue
        m = re.search(r"\bM(\d+)", str(s))
        if m and ("M" + m.group(1)) in GECIS: return "M" + m.group(1)
    return None


def vida_mi(p):
    b = " ".join(str(x) for x in (p.get("bom") or ())).lower()
    return any(k in b for k in ("cıvata", "civata", "vida", "saplama"))


def eksen_bul(sh):
    """elemanın ekseni: en küçük yarıçaplı silindirik dış yüzün ekseni (cıvata gövdesi / saplama) → (merkez nokta, birim yön)"""
    best = None
    for f in sh.Faces():
        if f.geomType() != "CYLINDER": continue
        c = f._geomAdaptor().Cylinder(); r = c.Radius(); ax = c.Axis()
        d = ax.Direction(); o = ax.Location()
        if best is None or r < best[0] - 1e-6: best = (r, np.array([o.X(), o.Y(), o.Z()]), np.array([d.X(), d.Y(), d.Z()]))
    if best is None: return None
    return best[1], best[2] / np.linalg.norm(best[2])


def silindir_mf(o, a, r, t0, t1, n=48):
    """manifold silindir: eksen o + t a (t0 → t1), yarıçap r"""
    import manifold3d as mf
    m = mf.Manifold.cylinder(t1 - t0, r, r, n)                             # z boyunca 0 → h
    a = np.asarray(a, float); z = np.array([0, 0, 1.0])
    v = np.cross(z, a); s = np.linalg.norm(v); c = float(z @ a)
    if s < 1e-9:
        R = np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
    else:
        k = v / s; K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
        R = np.eye(3) + s * K + (1 - c) * K @ K
    p0 = np.asarray(o, float) + a * t0
    M = np.c_[R, p0]
    return m.transform(M.tolist())


def kesici(p):
    """ARAYÜZ elemanının karşı parçada açacağı boşluk: katının kendisi ∪ (cıvata / saplama) geçiş deliği silindiri"""
    sh = sekil(p); P = ucgen(sh, 0.02, 0.15)
    m = mf_ucgen(P)
    if m is None: raise RuntimeError("kesici kapalı değil: %s" % p["ad"])
    if vida_mi(p):
        dis = dis_cap(p); e = eksen_bul(sh)
        if dis and e is not None:
            o, a = e; t = (P.reshape(-1, 3) - o) @ a
            m = m + silindir_mf(o, a, GECIS[dis] / 2.0, float(t.min()), float(t.max()))
    return m, P


# =====================================================================================================================================
# EVRE 1 · karşı taraf (m8kit Glb üzerinde)
# =====================================================================================================================================
def _kutu_kesisir(lo1, hi1, lo2, hi2, pay=0.05):
    return bool(np.all(hi1 >= lo2 - pay) and np.all(hi2 >= lo1 - pay))


class Karsi:
    def __init__(s, g, haric_onek=(), acik_dene=False):
        s.g = g; s.haric = tuple(haric_onek); s.acik_dene = acik_dene
        s.dkutu = {}
        for p in g.prims:
            if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
            if p["name"].startswith(s.haric): continue
            X = p["X"]; T = p["T"]; vis = (T[:, 0] != T[:, 1]) | (T[:, 1] != T[:, 2])
            if not vis.any(): continue
            Q = X[np.unique(T[vis].reshape(-1))]
            lo, hi = Q.min(0), Q.max(0)
            if p["name"] in s.dkutu:
                a, b = s.dkutu[p["name"]]; s.dkutu[p["name"]] = (np.minimum(a, lo), np.maximum(b, hi))
            else:
                s.dkutu[p["name"]] = (lo, hi)
        s.mfc = {}
        s.vurus = {}                                                       # (düğüm, bileşen no) → [eleman adı]
        s.bilesen = {}
        s.acik = []

    def komp(s, dugum):
        if dugum not in s.bilesen:
            s.g.bilesen(dugum, 0); s.bilesen[dugum] = list(s.g._bc[dugum])
        return s.bilesen[dugum]

    def mfk(s, dugum, b):
        k = (dugum, b["no"])
        if k not in s.mfc:
            P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
            s.mfc[k] = mf_ucgen(P) if (b["kapali"] or s.acik_dene) else None   # acik_dene (adım 37+): kapalı görünmeyen ağ da manifold kurulabiliyorsa kesilir
        return s.mfc[k]

    def tara(s, p, m, P, esik=0.01):
        """eleman p (kesici m) hangi bileşenleri deliyor → [(düğüm, b, hacim)]"""
        lo = P.reshape(-1, 3).min(0); hi = P.reshape(-1, 3).max(0)
        bb = m.bounding_box(); lo = np.minimum(lo, bb[:3]); hi = np.maximum(hi, bb[3:])
        out = []
        for d in sorted(s.dkutu):
            a, b_ = s.dkutu[d]
            if not _kutu_kesisir(lo, hi, a, b_): continue
            for b in s.komp(d):
                if not _kutu_kesisir(lo, hi, b["lo"], b["hi"]): continue
                mc = s.mfk(d, b)
                if mc is None:
                    # açık bileşen (T-birleşimli ağ; ör. TOPPING PU): üçgenlerinden biri kesici kutusuna giriyorsa → düzlemsel CEP (acik_cep)
                    Pc = np.concatenate([q["X"][q["T"][t]] for q, t in b["parca"]])
                    tl = Pc.min(1); th = Pc.max(1)
                    if np.any(np.all(th > lo + 0.1, 1) & np.all(tl < hi - 0.1, 1)): out.append((d, b, -1.0))
                    continue
                v = (mc ^ m).volume()
                if v > esik: out.append((d, b, v))
        return out

    def delik_ac(s, elemanlar, log=log):
        """elemanlar: [p] (ARAYÜZ) → karşı bileşenlere delik · dönüş: kayıt listesi"""
        kes = []
        for p in elemanlar:
            m, P = kesici(p)
            kes.append((p, m, P))
        hedef = {}
        for p, m, P in kes:
            for d, b, v in s.tara(p, m, P):
                k = (d, b["no"])
                hedef.setdefault(k, [d, b, []])[2].append((p["ad"], m, v))
        kayit = []
        for k in sorted(hedef):
            d, b, L = hedef[k]
            mc = s.mfk(d, b)
            if mc is None:
                kayit.append(s.acik_cep(d, b, L, log)); continue
            ks = L[0][1]
            for _, m, _ in L[1:]: ks = ks + m
            yeni = mc - ks
            Pn = mf_P(yeni)
            v0, v1 = mc.volume(), yeni.volume()
            ilk = [True]
            def f(_):
                if ilk[0]: ilk[0] = False; return Pn
                return None
            gr = set()
            for pp, tri in b["parca"]:
                for t in tri[:1]: gr.add(s.g._etiketler(pp, int(t)))
            s.g.donustur(b, f)
            kayit.append(dict(karsi="%s[%d]" % (d, b["no"]), kutu=[round(float(x), 2) for x in list(b["lo"]) + list(b["hi"])],
                              eleman=[a for a, _, _ in L], hacim_once=round(v0, 1), hacim_sonra=round(v1, 1), cikan=round(v0 - v1, 2)))
            log("  delik: %-34s ← %s · −%.1f mm³" % ("%s[%d]" % (d, b["no"]), ", ".join(sorted(set(a for a, _, _ in L)))[:110], v0 - v1))
        for a, c in s.acik: log("  UYARI açık bileşen (kesilemedi): %s ↔ %s" % (a, c))
        return kayit

    def v8zq_kutu(s, d, no):
        if not hasattr(s, "_v8"):
            import govde_denetim_dogru as G
            s._v8 = {}; s._v8D = G.glb_oku(os.path.join(KOK, "hat3_v8zq.glb")); s._G = G
        if d not in s._v8:
            s._v8[d] = [(b.lo, b.hi) for b in s._G.bilesenler(d, s._v8D[d])] if d in s._v8D else []
        L = s._v8[d]
        return L[no] if no < len(L) else None

    def saplama_ayarla(s, elemanlar, log=log):
        """FHP saplama (mekanizma / panel bağlantısı) yalnız KENDİ karşı parçasından geçmeli: arayüz kaydındaki karşı parça (ad + kutu; kutusuz
        kayıtta ad öneki + '__paslanmaz' = burç / panel plakası) dışındaki bir bileşene giriyorsa saplama boyu standart seriden (h3_sac_v1.SAPLAMA_BOY)
        engelin 0,5 mm önünde biten en uzun boya indirilir (yeniden kurulur: S.pem_saplama, aynı baş noktası / eksen). Dönüş: değişen kayıtlar."""
        import h3_sac_v1 as S
        out = []
        for i, p in enumerate(elemanlar):
            meta = p.get("meta", {}) or {}
            if meta.get("pem_tip") != "FHP": continue
            ky = (p.get("arayuz") or {}).get("karsi", "")
            m_ = re.match(r"^(\S+?)(?:\s+bbox\s+\[([^\]]+)\])?$", ky.strip())
            ad0 = m_.group(1) if m_ else ky.split()[0]
            kb = np.array([float(x) for x in m_.group(2).split(",")]) if (m_ and m_.group(2)) else None
            mi = re.match(r"^(\w+)\[(\d+)\]", ky.strip())
            if mi:                                                           # 'DÜĞÜM[no] (v8zq)' → v8zq'daki bileşen kutusu
                ad0 = mi.group(1); bv = s.v8zq_kutu(ad0, int(mi.group(2)))
                kb = None if bv is None else np.array([bv[0][0], bv[1][0], bv[0][1], bv[1][1], bv[0][2], bv[1][2]])
            def hedef_mi(d, b):
                if kb is not None:                                           # v8zq bileşen kutusu (kaba gruplama) → karşı parça bileşeni bu kutunun İÇİNDE
                    return d.startswith(ad0) and np.all(b["lo"] >= kb[[0, 2, 4]] - 1.5) and np.all(b["hi"] <= kb[[1, 3, 5]] + 1.5)
                return d.startswith(ad0.split()[0]) and d.endswith("__paslanmaz")
            m, P = kesici(p)
            vur = s.tara(p, m, P)
            sh = sekil(p); o, a = eksen_bul(sh)
            V = P.reshape(-1, 3); t = (V - o) @ a; r = np.linalg.norm((V - o) - np.outer(t, a), axis=1)
            th = t[np.argmax(r)]
            if abs(th - t.min()) < abs(th - t.max()): tb, ex = t.min(), a
            else: tb, ex = t.max(), -a
            taban = o + a * tb
            def aralik_t(d, b):                                              # bileşenin saplama ekseni boyunca [başlangıç, bitiş] (taban noktasından)
                C = np.array([[x, y, z] for x in (b["lo"][0], b["hi"][0]) for y in (b["lo"][1], b["hi"][1]) for z in (b["lo"][2], b["hi"][2])])
                q = (C - taban) @ ex; return float(q.min()), float(q.max())
            hed = [(d, b) for d, b, v in vur if v > 0 and hedef_mi(d, b)]
            # karşı parçaya ALIN oturan ince levha / burç / kanal (pano plakası, kablo kanalı tabanı) aynı vida paketidir → delinir
            paket = list(hed); deg = True
            while deg:
                deg = False
                ust = max([aralik_t(d, b)[1] for d, b in paket] + [0.0])
                for d, b, v in vur:
                    if v <= 0 or any(b is bb for _, bb in paket): continue
                    a0, a1 = aralik_t(d, b)
                    if a0 > ust + 0.6: continue                                  # pakete alın / iç içe (eksen boyunca paketin bittiği yerden önce başlar)
                    ince = re.search(r"__(sac|aluminyum|celik|paslanmaz|kanal)(__|$)", d) and (a1 - a0) <= 6.0
                    # aynı birimin gövdesi (fan kasası köşe deliği, baca yalıtım sargısı, askı lamaları) — ürün / konnektör / etiket / kablo HARİÇ
                    aile = any(d.split("__")[0] == dd.split("__")[0] for dd, _ in hed) and (a1 - a0) <= 40.0 and \
                        not re.search(r"karton|yigin|poset|urun|hamur|pizza|harting|etiket|kablo|m12|kod_|motor", d)
                    if ince or aile:
                        paket.append((d, b)); deg = True
            eng = [(d, b) for d, b, v in vur if v != 0 and not any(b is bb for _, bb in paket) and not (v < 0 and hedef_mi(d, b))]   # açık ağ (v<0) da engel
            if not eng: continue
            def ilk(d, b):                                                   # engelin saplama ekseninde başlangıcı (taban noktasından)
                q = s.mfk(d, b)
                if q is None: return float(np.min(np.abs((np.array([b["lo"], b["hi"]]) - taban) @ ex)))
                bb = np.array((q ^ m).bounding_box()); C = np.array([[x, y, z] for x in bb[[0, 3]] for y in bb[[1, 4]] for z in bb[[2, 5]]])
                return float(((C - taban) @ ex).min())
            def son(d, b):
                q = s.mfk(d, b)
                if q is None: return 0.0
                bb = np.array((q ^ m).bounding_box()); C = np.array([[x, y, z] for x in bb[[0, 3]] for y in bb[[1, 4]] for z in bb[[2, 5]]])
                return float(((C - taban) @ ex).max())
            tobs = min(ilk(d, b) for d, b in eng)
            gerek = max([son(d, b) for d, b in paket] + [0.0])
            dis = meta.get("dis", "M5"); boy0 = float(meta.get("boy", 12))
            uy = [L for L in S.SAPLAMA_BOY if L <= tobs - 0.5 and L >= gerek + 1.0]
            if not uy:
                elemanlar[i] = None                                            # saplama konamaz (engel karşı parçanın hemen üstünde) → çıkarılır, rapora
                out.append(dict(ad=p["ad"], boy_eski=boy0, boy=0, engel=["%s[%d]" % (d, b["no"]) for d, b in eng], karsi_cikis=round(gerek, 2), cikarildi=True))
                log("  UYARI saplama ÇIKARILDI: %s (engel %.1f mm'de: %s · karşı parça %s) — sacdaki Ø%.1f PEM deliği boş kalır, üreteçte düzeltilmeli" % (
                    p["ad"], tobs, ", ".join("%s[%d]" % (d, b["no"]) for d, b in eng), ", ".join("%s[%d]" % (d, b["no"]) for d, b in hed) or "YOK", float(meta.get("delik", 0))))
                continue
            L = float(uy[-1])
            yeni, c = S.pem_saplama("FHP", dis, L, tuple(taban.tolist()), tuple(ex.tolist()), ad=p["ad"], birim=p.get("birim", "BAGLANTI"))
            q = dict(p); q["sh"] = yeni["sh"]; q.pop("wp", None); q["bom"] = yeni["bom"]; q["meta"] = dict(meta, boy=L, parca=yeni["meta"]["parca"])
            elemanlar[i] = q
            out.append(dict(ad=p["ad"], boy_eski=boy0, boy=L, engel=["%s[%d]" % (d, b["no"]) for d, b in eng], karsi_cikis=round(gerek, 2)))
            log("  saplama boyu: %-26s %s×%g → %s×%g (engel %s %.1f mm · karşı parçadan çıkış %.1f mm%s)" % (
                p["ad"], dis, boy0, dis, L, ",".join("%s[%d]" % (d, b["no"]) for d, b in eng)[:60], tobs, gerek,
                "" if L >= gerek + 1.0 else " · UYARI somun payı yok"))
        elemanlar[:] = [p for p in elemanlar if p is not None]
        return out

    def acik_cep(s, d, b, L, log=log, pay=0.1):
        """AÇIK bileşende kesici başına eksen hizalı CEP: kesici kutusuna giren üçgenlerin hepsi tek eksen hizalı düzlemdeyse (ör. PU'nun sac
        tarafındaki yüzü) o düzlemden dikdörtgen çıkarılır (m8kit.delik_ucgenler) + cep duvarları + cep tabanı malzeme tarafına (üçgen normalinin
        tersi) kesici kutusunun ucuna kadar. Köpük kapağı (PEM / cıvata ucu üstüne köpüklemeden önce takılan kare kapak) ile aynı hacim."""
        import m8kit as MK
        P = np.concatenate([q["X"][q["T"][t]] for q, t in b["parca"]])
        n0 = len(P); yap = []
        G_ = []                                                            # kutuları örtüşen kesiciler tek cep (cıvata + PEM)
        for ad, m, _ in L:
            bb = np.array(m.bounding_box()); lo, hi = bb[:3] - pay, bb[3:] + pay
            for gr in G_:
                if _kutu_kesisir(lo, hi, gr[1], gr[2], 0.0):
                    gr[0].append(ad); gr[1] = np.minimum(gr[1], lo); gr[2] = np.maximum(gr[2], hi); break
            else:
                G_.append([[ad], lo, hi])
        for adl, lo, hi in G_:
            ad = "+".join(adl)
            tl = P.min(1); th = P.max(1)
            ic = np.all(th > lo + 1e-6, 1) & np.all(tl < hi - 1e-6, 1)
            if not ic.any(): continue
            Q = P[ic]
            sp = Q.reshape(-1, 3).max(0) - Q.reshape(-1, 3).min(0)
            a = int(np.argmin(sp)); c = float(Q[:, :, a].mean())
            if sp[a] > 0.02 or not (lo[a] < c < hi[a]):
                log("  UYARI açık bileşen cebi kurulamadı (düzlemsel değil): %s ↔ %s[%d]" % (ad, d, b["no"])); continue
            nrm = np.cross(Q[:, 1] - Q[:, 0], Q[:, 2] - Q[:, 0]); sg = -np.sign(nrm[:, a].sum())   # malzeme tarafı
            u, w = [i for i in range(3) if i != a]
            P = MK.delik_ucgenler(P, a, [c], lo[u], hi[u], lo[w], hi[w])
            ucu = hi[a] if sg > 0 else lo[a]
            def pt(uu, ww, vv):
                q = np.zeros(3); q[a] = vv; q[u] = uu; q[w] = ww; return q
            kos = [(lo[u], lo[w]), (hi[u], lo[w]), (hi[u], hi[w]), (lo[u], hi[w])]
            cu, cw = (lo[u] + hi[u]) / 2, (lo[w] + hi[w]) / 2
            ek = []
            for i in range(4):
                (ua, wa), (ub, wb) = kos[i], kos[(i + 1) % 4]
                Qd = [pt(ua, wa, c), pt(ub, wb, c), pt(ub, wb, ucu), pt(ua, wa, ucu)]
                for t in ((0, 1, 2), (0, 2, 3)):
                    T = np.array([Qd[j] for j in t]); nr = np.cross(T[1] - T[0], T[2] - T[0])
                    if nr @ (pt(cu, cw, T[:, a].mean()) - T.mean(0)) < 0: T = T[[0, 2, 1]]   # duvar normali cebin içine (malzemeden dışarı)
                    ek.append(T)
            Qt = [pt(*kos[i], ucu) for i in range(4)]
            for t in ((0, 1, 2), (0, 2, 3)):
                T = np.array([Qt[j] for j in t]); nr = np.cross(T[1] - T[0], T[2] - T[0])
                if nr[a] * sg > 0: T = T[[0, 2, 1]]                         # taban normali düzleme doğru
                ek.append(T)
            P = np.concatenate([P, np.array(ek)])
            yap.append(ad)
        ilk = [True]
        def f(_):
            if ilk[0]: ilk[0] = False; return P
            return None
        if yap: s.g.donustur(b, f)
        log("  cep (açık bileşen): %-24s ← %s · %d → %d üçgen" % ("%s[%d]" % (d, b["no"]), ", ".join(yap)[:110], n0, len(P)))
        return dict(karsi="%s[%d]" % (d, b["no"]), kutu=[round(float(x), 2) for x in list(b["lo"]) + list(b["hi"])], eleman=yap, cep=True)


def ekle_karsi(g, dugum, parcalar, kat, mek, log=log):
    """karşı parçaya ait preslenen / perçinlenen elemanlar → o düğüme (düz gölgeleme, m8kit)"""
    for p in parcalar:
        P = ucgen(sekil(p))
        g.ekle_dugum(dugum, P, kat=kat, mek=mek, kpk=False)
        b = sekil(p).BoundingBox()
        log("  karşı eleman: %-40s → %s (kat %d · mek %d) kutu %s" % (p["ad"], dugum, kat, mek, [round(x, 1) for x in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]))


def dunya_arayuz(g):
    """h3_govde_ortak_v1.Govde ARAYÜZ elemanları → dünya koordinatı (sh)"""
    out = []
    for p in g.ARAYUZ:
        q = dict(p); q["sh"] = g.cerceve.dunya(sekil(p)); q.pop("wp", None); out.append(q)
    return out


def pem_yeri(g, ad, x, z, dugumler, y_ust, y_alt, kayma=6.0, dis="M8", tip="SP"):
    """(x, z) dikey ekseninde y_ust'ten aşağı ilk sacın ALT yüzüne PEM somun (gövde aşağıda) · sac kalınlığı ışınla ölçülür"""
    import h3_sac_v1 as S
    for d in dugumler:
        g.bilesen(d, 0)
        for b in g._bc[d]:
            if not (b["lo"][0] - 0.1 <= x <= b["hi"][0] + 0.1 and b["lo"][2] - 0.1 <= z <= b["hi"][2] + 0.1 and b["hi"][1] <= y_ust + 0.01 and b["lo"][1] >= y_alt): continue
            P = np.concatenate([q["X"][q["T"][t]] for q, t in b["parca"]])
            ys = isin_y(P, x + kayma, z, y_ust, y_alt)
            if len(ys) < 2: continue
            y1, y2 = ys[-1], ys[-2]
            p, c, ms = S.pem_somun(tip, dis, (x, y2, z), (0, -1.0, 0), y1 - y2, ad=ad, birim=d.split("__")[0])
            return p, d, "%s[%d]" % (d, b["no"]), y1, y1 - y2
    return None, None, None, None, None


def kes_tam(parcalar, kesiciler, log=log):
    """gövde parçalarından cıvata katısının KENDİSİ çıkarılır (geçtiği sac / PU / köpük kapağında tam ölçü yuva) — yalnız gerçekten kesişenler"""
    out = []
    for p in parcalar:
        sh = sekil(p); b = sh.BoundingBox(); kes = []
        for k in kesiciler:
            kb = sekil(k).BoundingBox()
            if kb.xmax < b.xmin or b.xmax < kb.xmin or kb.ymax < b.ymin or b.ymax < kb.ymin or kb.zmax < b.zmin or b.zmax < kb.zmin: continue
            if sh.intersect(sekil(k)).Volume() > 1e-3: kes.append(k)
        if kes:
            v0 = sh.Volume(); yeni = sh.cut(*[sekil(k) for k in kes]).clean()
            if yeni.ShapeType() != "Solid" and len(yeni.Solids()) == 1: yeni = yeni.Solids()[0]
            log("  gövde yuvası: %-34s ← %s · −%.1f mm³" % (p["ad"], ", ".join(k["ad"] for k in kes)[:100], v0 - yeni.Volume()))
            q = dict(p); q["sh"] = yeni; q.pop("wp", None); out.append(q)
        else:
            out.append(p)
    return out


def kes_govde(parcalar, kesiciler, log=log, pay=0.25):
    """gövde parçalarından (CadQuery katısı) karşı elemanın baş boşluğu çıkarılır (ör. perçin somun başı → dış sacda Ø Dk + 2·pay boşluk):
    kesici = elemanın katısının eksen hizalı silindir zarfı (yarıçap = katının en büyük yarıçapı + pay) — yalnız kutusu kesişen parçalar"""
    import cadquery as cq
    out = []
    for p in parcalar:
        sh = sekil(p); b = sh.BoundingBox(); yeni = sh; ad_ = []
        for k in kesiciler:
            kb = sekil(k).BoundingBox()
            if kb.xmax < b.xmin or b.xmax < kb.xmin or kb.ymax < b.ymin or b.ymax < kb.ymin or kb.zmax < b.zmin or b.zmax < kb.zmin: continue
            ks = sekil(k)
            if yeni.intersect(ks).Volume() < 1e-3: continue
            e = eksen_bul(ks)
            if e is None: continue
            o, a = e; V = np.array([(v.X, v.Y, v.Z) for v in ks.Vertices()])
            # en büyük yarıçap: kesici katının kutusundan (eksene dik iki boyutun yarısı)
            ext = np.array([kb.xlen, kb.ylen, kb.zlen]); r = float(max(ext[i] for i in range(3) if abs(a[i]) < 0.5)) / 2.0 + pay
            ia = int(np.argmax(np.abs(a))); t0, t1 = (kb.xmin, kb.ymin, kb.zmin)[ia], (kb.xmax, kb.ymax, kb.zmax)[ia]
            c = np.array([(kb.xmin + kb.xmax) / 2, (kb.ymin + kb.ymax) / 2, (kb.zmin + kb.zmax) / 2]); c[ia] = t0
            d = [0.0, 0.0, 0.0]; d[ia] = 1.0
            cyl = cq.Solid.makeCylinder(r, t1 - t0, cq.Vector(*c), cq.Vector(*d))
            yeni = yeni.cut(cyl); ad_.append(k["ad"])
        if ad_:
            v0, v1 = sh.Volume(), yeni.Volume()
            yeni = yeni.clean()
            if yeni.ShapeType() != "Solid" and len(yeni.Solids()) == 1: yeni = yeni.Solids()[0]
            log("  gövde boşluğu: %-34s ← %s · −%.1f mm³" % (p["ad"], ", ".join(ad_)[:100], v0 - v1))
            q = dict(p); q["sh"] = yeni; q.pop("wp", None); out.append(q)
        else:
            out.append(p)
    return out


def bilesen_sil(g, dugum, secici, log=log, beklenen=None):
    """düğümde seçici(lo, hi) True olan bileşenleri sil"""
    g.bilesen(dugum, 0); L = [b for b in g._bc[dugum] if secici(b["lo"], b["hi"])]
    if beklenen is not None: assert len(L) == beklenen, (dugum, len(L), beklenen)
    for b in L: g.sil_b(b)
    log("  sil: %s · %d bileşen" % (dugum, len(L)))
    return len(L)


def isin_y(P, x, z, y0, y1):
    """dikey ışın (x, z) — y0 → y1 arasında üçgenleri kestiği y'ler (artan)"""
    v0, v1, v2 = P[:, 0], P[:, 1], P[:, 2]
    o = np.array([x, y0, z]); d = np.array([0, 1.0, 0]) * np.sign(y1 - y0); L = abs(y1 - y0)
    e1 = v1 - v0; e2 = v2 - v0; h = np.cross(d, e2); a = (e1 * h).sum(1); ok = np.abs(a) > 1e-12
    f = np.where(ok, 1.0 / np.where(ok, a, 1), 0); sv = o - v0; u = f * (sv * h).sum(1)
    q = np.cross(sv, e1); v = f * (q @ d); t = f * (e2 * q).sum(1)
    hit = ok & (u >= -1e-9) & (v >= -1e-9) & (u + v <= 1 + 1e-9) & (t > 0) & (t < L)
    ys = np.unique(np.round(y0 + np.sign(y1 - y0) * t[hit], 3))
    return sorted(ys.tolist())


# =====================================================================================================================================
# EVRE 2 · ham GLB (gövde düğümleri)
# =====================================================================================================================================
class Ham:
    def __init__(s, yol):
        raw = open(yol, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]
        s.J = json.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack("<I", raw[bo:bo + 4])[0]
        s.BIN = bytearray(raw[bo + 8:bo + 8 + bl])
        s.aralik = {}

    def _oku(s, i):
        a = s.J["accessors"][i]; v = s.J["bufferViews"][a["bufferView"]]
        n = {"SCALAR": 1, "VEC3": 3, "VEC2": 2, "VEC4": 4}[a["type"]]; dt = TD[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        r = np.frombuffer(bytes(s.BIN[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt).copy()
        return r.reshape(-1, n) if n > 1 else r

    def _ekle(s, arr, tip, hedef):
        while len(s.BIN) % 4: s.BIN.extend(b"\0")
        off = len(s.BIN); s.BIN.extend(arr.tobytes())
        s.J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
        a = {"bufferView": len(s.J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
        if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
        s.J["accessors"].append(a); return len(s.J["accessors"]) - 1

    def dugum(s, ad):
        L = [n for n in s.J["nodes"] if n.get("name") == ad]
        assert len(L) <= 1, ad
        return L[0] if L else None

    def hazirla(s, ad, sablon):
        """düğüm yoksa / ağı yoksa: sablon düğümün malzemesinden (aynı özellikler, yeni ad) ağ + tek primitif kurulur"""
        nd = s.dugum(ad)
        if nd is not None and "mesh" in nd:
            assert len(s.J["meshes"][nd["mesh"]]["primitives"]) == 1, ad
            return nd
        sb = s.dugum(sablon); assert sb is not None and "mesh" in sb, sablon
        spr = s.J["meshes"][sb["mesh"]]["primitives"][0]
        m0 = s.J["materials"][spr["material"]]
        pre = m0.get("name", "").split("_")[0]
        birim = ad.split("__")[0] + "__"                                   # malzeme öneki istasyonun kendi düğümlerinden (MA_, MB_ …)
        for n in s.J["nodes"]:
            if n.get("name", "").startswith(birim) and "mesh" in n:
                pre = s.J["materials"][s.J["meshes"][n["mesh"]]["primitives"][0]["material"]].get("name", "").split("_")[0]; break
        mad = "%s_%s" % (pre, ad)
        mi = next((i for i, m in enumerate(s.J["materials"]) if m.get("name") == mad), None)
        if mi is None:
            m = json.loads(json.dumps(m0)); m["name"] = mad; s.J["materials"].append(m); mi = len(s.J["materials"]) - 1
        s.J["meshes"].append({"name": ad, "primitives": [{"attributes": {}, "material": mi, "extras": {"kat": [0, 0, 0], "mek": [0, 0, 0], "kpk": []}}]})
        if nd is None:
            s.J["nodes"].append({"name": ad, "mesh": len(s.J["meshes"]) - 1})
            s.J["scenes"][s.J.get("scene", 0)]["nodes"].append(len(s.J["nodes"]) - 1)
            nd = s.J["nodes"][-1]
        else:
            nd["mesh"] = len(s.J["meshes"]) - 1
        log("  yeni düğüm/ağ: %s (malzeme %s ← %s)" % (ad, mad, m0.get("name")))
        return nd

    def koy(s, ad, parcalar, kat, mek, kpk_fn=lambda a: False, sablon=None, ekle=False):
        """düğümü parçalarla doldurur (ekle=True: mevcut üçgenler korunur, sona eklenir) · dönüş: {parça adı: (ilk indis, indis sayısı)}"""
        nd = s.hazirla(ad, sablon or ad)
        assert not any(k in nd for k in ("rotation", "scale", "matrix")) and not np.any(nd.get("translation", [0, 0, 0])), ad
        pr = s.J["meshes"][nd["mesh"]]["primitives"][0]
        XX, NN, II, say = [], [], [], []
        o = 0
        if ekle and "POSITION" in pr.get("attributes", {}):
            X0 = s._oku(pr["attributes"]["POSITION"]).astype(np.float32); N0 = s._oku(pr["attributes"]["NORMAL"]).astype(np.float32)
            I0 = s._oku(pr["indices"]).astype(np.uint32)
            XX.append(X0); NN.append(N0); II.append(I0); o = len(X0); ib0 = len(I0)
        else:
            ib0 = 0
        aralik = {}; ib = ib0; kp = []
        for p in parcalar:
            V, F = tess(sekil(p))
            if not len(F): continue
            N = np.zeros_like(V); fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
            for k in range(3): np.add.at(N, F[:, k], fn)
            N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)
            XX.append((V / 1000.0).astype(np.float32)); NN.append(N.astype(np.float32)); II.append((F.reshape(-1) + o).astype(np.uint32))
            n = 3 * len(F); aralik[p["ad"]] = (ib, n)
            if kpk_fn(p["ad"]):
                if kp and kp[-2] + kp[-1] == ib: kp[-1] += n
                else: kp += [ib, n]
            o += len(V); ib += n
        X = np.vstack(XX); N = np.vstack(NN); I = np.concatenate(II).astype(np.uint32)
        pr["attributes"] = {"POSITION": s._ekle(X, "VEC3", 34962), "NORMAL": s._ekle(N, "VEC3", 34962)}
        pr["indices"] = s._ekle(I, "SCALAR", 34963)
        ex = pr.setdefault("extras", {})
        if ekle and ib0:
            ex["kat"] = list(ex.get("kat", [])) + [int(kat), ib0, ib - ib0]
            ex["mek"] = list(ex.get("mek", [])) + [int(mek), ib0, ib - ib0]
            ex["kpk"] = list(ex.get("kpk", [])) + kp
        else:
            ex["kat"] = [int(kat), 0, ib]; ex["mek"] = [int(mek), 0, ib]; ex["kpk"] = kp
        s.aralik[ad] = aralik
        log("  %-26s %s %4d parça · %7d üçgen · kat %d · mek %d · kpk %d aralık" % (ad, "+" if ekle else "=", len(aralik), (ib - ib0) // 3, kat, mek, len(kp) // 2))
        return aralik

    def bosalt(s, ad):
        nd = s.dugum(ad)
        if nd is None or "mesh" not in nd: return False
        for pr in s.J["meshes"][nd["mesh"]]["primitives"]:
            X = np.zeros((3, 3), np.float32) + np.float32(1.0)
            pr["attributes"] = {"POSITION": s._ekle(X, "VEC3", 34962), "NORMAL": s._ekle(np.tile(np.float32([0, 1, 0]), (3, 1)), "VEC3", 34962)}
            pr["indices"] = s._ekle(np.zeros(3, np.uint32), "SCALAR", 34963)
            ex = pr.setdefault("extras", {})
            for k in ("kat", "mek"):
                if ex.get(k): ex[k] = [ex[k][0], 0, 3]
            ex["kpk"] = []
        log("  %-26s boşaltıldı" % ad)
        return True

    def etiket(s, ad):
        """düğümün mevcut ilk kat / mek değeri"""
        nd = s.dugum(ad)
        if nd is None or "mesh" not in nd: return None, None
        ex = s.J["meshes"][nd["mesh"]]["primitives"][0].get("extras", {})
        return (ex.get("kat") or [None])[0], (ex.get("mek") or [None])[0]

    def yaz(s, yol):
        while len(s.BIN) % 4: s.BIN.extend(b"\0")
        s.J["buffers"][0]["byteLength"] = len(s.BIN)
        jb = json.dumps(s.J, separators=(",", ":"), ensure_ascii=False).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
        with open(yol, "wb") as f:
            f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(s.BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
                    + struct.pack("<II", len(s.BIN), 0x004E4942) + bytes(s.BIN))


def sikistir(gi, go):
    r = subprocess.run([sys.executable, os.path.join(KOK, "tg", "glb_sikistir.py"), gi, go])
    assert r.returncode == 0 and os.path.exists(go), "sıkıştır başarısız"


def kutu6(p):
    b = sekil(p).BoundingBox()
    return [round(v, 2) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]


def ent_json(yol, istasyon, dugumler, aralik, kpk_fn, mek_kod, eski_birim, kayit, ek=None):
    """adım kaydı: <çıktı>_ent.json · parça → [düğüm, kpk, kutu, (ilk indis, sayı)] (parca_kutulari / mekanizma json güncellemesi bundan yapılır)"""
    P = {}
    for dug, L in dugumler:
        for p in L:
            if p["ad"] not in aralik.get(dug, {}): continue
            P[p["ad"]] = dict(dugum=dug, kpk=1 if kpk_fn(p["ad"]) else 0, kutu=kutu6(p), indis=list(aralik[dug][p["ad"]]),
                              tur=p.get("tur", ""), bom=list(p.get("bom") or ()))
    d = dict(istasyon=istasyon, mek=mek_kod, eski_birim=list(eski_birim), parca=P, karsi=kayit, log=LOG)
    if ek: d.update(ek)
    json.dump(d, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=str)


def degisen_sil(g, v8zq_yol, degisen, log=log, tol=0.3):
    """üretecin DEGISEN tablosu (v8zq düğüm + bileşen no) → v8zq'daki o bileşenlerin kutuları → girdide AYNI kutulu bileşenler silinir
    (önceki zincir adımları bileşen numaralarını kaydırabilir; kutu değişmez — delik açılan bileşende de kutu aynı). 'hepsi' → düğümün tümü."""
    import govde_denetim_dogru as G
    D = G.glb_oku(v8zq_yol)
    say = {}
    for d in sorted(degisen):
        sec = degisen[d]
        B0 = G.bilesenler(d, D[d])
        hedef = [(b.lo, b.hi) for b in B0] if sec == "hepsi" else [(B0[i].lo, B0[i].hi) for i in sec]
        g.bilesen(d, 0); L = list(g._bc[d]); n = 0; bulunmayan = 0
        for lo, hi in hedef:
            c = [b for b in L if np.all(np.abs(b["lo"] - lo) < tol) and np.all(np.abs(b["hi"] - hi) < tol)]
            if not c: bulunmayan += 1; continue
            for b in c:
                g.sil_b(b); L.remove(b); n += 1
        say[d] = (n, len(hedef), bulunmayan)
        log("  sil (v8zq kutusuyla): %-40s %d bileşen (hedef %d · bulunamayan %d)" % (d, n, len(hedef), bulunmayan))
    return say


def kutu_sil(g, dugum, kutular, log=log, tol=0.3):
    g.bilesen(dugum, 0); L = list(g._bc[dugum]); n = 0
    for lo, hi in kutular:
        for b in [b for b in L if np.all(np.abs(b["lo"] - lo) < tol) and np.all(np.abs(b["hi"] - hi) < tol)]:
            g.sil_b(b); L.remove(b); n += 1
    log("  sil (kutu): %s · %d / %d" % (dugum, n, len(kutular)))
    return n
