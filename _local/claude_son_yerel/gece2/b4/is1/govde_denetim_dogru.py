# -*- coding: utf-8 -*-
"""GÖVDE ÇAKIŞMA DENETİMİ — DOĞRU YÖNTEM (2 Eki · eski betiklerdeki iki hatanın düzeltmesi).
ESKİ HATALAR: (1) derinlik BRepExtrema_DistShapeShape(nokta, KATI) ile ölçülüyordu → katının İÇİNDEKİ nokta için 0 döner → "> 0,05 mm"
süzgeci gerçek çakışmaları eliyordu · (2) 4 mm yüzey örneklemesi 1,5 mm sacı delip geçen yüzleri kaçırıyordu.

YÖNTEM
  0  GLB tam okunur (düğüm hiyerarşisi + TRS/matris + bütün primitifler) · her düğüm KATI BİLEŞENLERİNE ayrılır: köşeler konumla birleştirilir,
     iki üçgen yalnız TAM 2 kez kullanılan + ters yönlü bir kenarla bağlanır (iki katının paylaştığı kenar / çakışık ters üçgen bağ kurmaz) ·
     bileşen KAPALI = her kenarı kendi içinde tam 2 kez, ters yönlü.
  1  ÖN ELEME: küme bileşeni ↔ diğer bütün bileşenler (küme içi dahil) eksen hizalı kutu kesişimi (± 0,06).
  2  İKİ KAPALI BİLEŞEN: manifold3d tam boolean KESİŞİM HACMİ. Hacim ≈ 0 → çakışma yok (aralık ≤ 0,05 ise TEMAS listesine).
     Hacim var → kesişim kutusunda yoğun örnekleme (adım 3).
     AÇIK BİLEŞEN (kapalı olmayan ağ: tel, şerit, yüzey): ortak kutu bölgesinde doğrudan yoğun örnekleme (yalnız kapalı tarafın içi sorulabilir).
  3  YOĞUN ÖRNEKLEME (her iki yön): (a) diğerinin yüzeyi kümenin İÇİNDE mi · (b) kümenin yüzeyi diğerinin İÇİNDE mi (ince sac geçişi / gömülü
     parça) · üçgenler en uzun kenarından ikiye bölünerek her kenar ≤ 0,6 mm olana kadar inceltilir (yalnız bölge içindekiler) → 1,5 mm sacı
     dik geçen her yüzün sacın içinde en az bir noktası olur · içerde testi VTK kapalı yüzey (ışın) · DERİNLİK = noktanın KAPSAYANIN YÜZEYİNE
     uzaklığı (vtkImplicitPolyDataDistance; katıya değil).
  4  EŞİK: derinlik > 0,05 mm = ÇAKIŞMA · ≤ 0,05 = TEMAS (ayrı liste). Her çakışma OCC ile DOĞRULANIR: kapsayan bileşen üçgenlerden OCC katısına
     dikilir (tg/dikis.kati), en derin noktalar BRepClass3d_SolidClassifier ile İÇERDE mi, derinlik = BRepExtrema(nokta, Compound(Faces)).
Kullanım:
  python govde_denetim_dogru.py model.glb cikti_klasoru --kume "A=A_GOVDE__,KAIDE_A__" --kume "TOPPING=TOPPING_MODUL__,ELK_TOPPING@degisen" --taban eski.glb
    '@degisen' → o kümede yalnız tabana göre DEĞİŞEN / YENİ bileşenler denetlenir (taban glb gerekir).
  python govde_denetim_dogru.py --test     (sahte çakışma sınaması)"""
import os, sys, json, struct, time, argparse, hashlib
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import manifold3d as mf
import vtk
from vtk.util.numpy_support import numpy_to_vtk, numpy_to_vtkIdTypeArray, vtk_to_numpy

HERE = os.path.dirname(os.path.abspath(__file__))
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
ADIM = 0.6
ESIK = 0.05
PAY = 0.06


# ============================================================================== GLB
def _quat(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def _mat(nd):
    if "matrix" in nd: return np.array(nd["matrix"], float).reshape(4, 4).T
    M = np.eye(4)
    R = _quat(nd.get("rotation", [0, 0, 0, 1])) * np.array(nd.get("scale", [1, 1, 1]))[None, :]
    M[:3, :3] = R; M[:3, 3] = nd.get("translation", [0, 0, 0]); return M


def glb_oku(yol):
    """düğüm adı → üçgen köşeleri P (n,3,3) mm (dünya koordinatı, dejenere hariç)"""
    raw = open(yol, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
    bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]

    def acc(i):
        a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
        n = {"SCALAR": 1, "VEC3": 3, "VEC2": 2, "VEC4": 4}[a["type"]]; dt = TD[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0); st = v.get("byteStride", 0)
        isz = np.dtype(dt).itemsize
        if st and st != n * isz:
            buf = np.frombuffer(BIN[off:off + st * a["count"]], np.uint8).reshape(a["count"], st)[:, :n * isz]
            arr = np.frombuffer(buf.tobytes(), dt)
        else:
            arr = np.frombuffer(BIN[off:off + a["count"] * n * isz], dt)
        return arr.reshape(-1, n) if n > 1 else arr
    D = {}
    nodes = J["nodes"]

    def gez(i, M):
        nd = nodes[i]; W = M @ _mat(nd)
        if "mesh" in nd:
            ad = nd.get("name", "dugum%d" % i)
            if ad in D: ad = "%s#%d" % (ad, i)
            parca = []
            for pr in J["meshes"][nd["mesh"]]["primitives"]:
                if pr.get("mode", 4) != 4: continue
                X = acc(pr["attributes"]["POSITION"]).astype(float)
                X = (X @ W[:3, :3].T + W[:3, 3]) * 1000.0
                T = acc(pr["indices"]).reshape(-1, 3).astype(np.int64) if "indices" in pr else np.arange(len(X)).reshape(-1, 3)
                P = X[T]
                ar = np.linalg.norm(np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), axis=1)
                parca.append(P[ar > 1e-9])
            D[ad] = np.concatenate(parca) if parca else np.zeros((0, 3, 3))
        for c in nd.get("children", []): gez(c, W)
    kok = J["scenes"][J.get("scene", 0)]["nodes"]
    for i in kok: gez(i, np.eye(4))
    return D


# ============================================================================== katı bileşenleri
class Bil:
    __slots__ = ("dugum", "no", "P", "V", "F", "kapali", "lo", "hi", "_mf", "_yz", "_occ", "ozet")

    def __init__(s, dugum, no, P, V, F, kapali):
        s.dugum, s.no, s.P, s.V, s.F, s.kapali = dugum, no, P, V, F, kapali
        s.lo = P.reshape(-1, 3).min(0); s.hi = P.reshape(-1, 3).max(0)
        s._mf = s._yz = s._occ = None
        R = np.round(P.reshape(-1, 3), 2) + 0.0; R = np.unique(R, axis=0)
        s.ozet = hashlib.md5(R.tobytes()).hexdigest()

    @property
    def ad(s): return "%s[%d]" % (s.dugum, s.no)

    def mf(s):
        if s._mf is None:
            s._mf = False
            if s.kapali:
                try:
                    m = mf.Manifold(mf.Mesh(vert_properties=s.V.astype(np.float32), tri_verts=s.F.astype(np.uint32)))
                    if m.status() == mf.Error.NoError and not m.is_empty(): s._mf = m
                except Exception:
                    pass
        return s._mf

    def yz(s):
        if s._yz is None: s._yz = vtk_yuzey(s.V, s.F)
        return s._yz


def bilesenler(dugum, P):
    out = []
    if not len(P): return out
    key = np.round(P.reshape(-1, 3), 3)
    uu, inv = np.unique(key, axis=0, return_inverse=True); vid = inv.reshape(-1, 3)
    iyi = (vid[:, 0] != vid[:, 1]) & (vid[:, 1] != vid[:, 2]) & (vid[:, 0] != vid[:, 2])
    P = P[iyi]; vid = vid[iyi]; n = len(vid); NV = len(uu)
    if not n: return out
    a = vid; b = np.roll(vid, -1, axis=1); c = np.roll(vid, -2, axis=1)
    lo = np.minimum(a, b).ravel().astype(np.int64); hi = np.maximum(a, b).ravel().astype(np.int64)
    yon = (a < b).ravel(); uc = c.ravel(); tri = np.repeat(np.arange(n), 3)
    ek = lo * NV + hi
    o = np.argsort(ek, kind="stable"); eks = ek[o]
    bas = np.r_[0, np.where(np.diff(eks))[0] + 1]; say = np.diff(np.r_[bas, len(eks)])
    iki = say == 2
    i1 = o[bas[iki]]; i2 = o[bas[iki] + 1]
    bag = yon[i1] != yon[i2]
    r, q = list(tri[i1[bag]]), list(tri[i2[bag]])
    # 2'den fazla kullanılan kenar (yüz / kenar paylaşan katılar): kenar çevresinde açıya göre sırala, iç kama = (iç +θ tarafta olan, yon False)
    # üçgen → saat yönü tersinde SONRAKİ üçgen (iç −θ tarafta, yon True) · eşit açıda önce yon True (kama kapanır), sonra False (kama açılır)
    cok = np.where(say > 2)[0]
    if len(cok):
        R1, R2 = [], []
        for g in cok:
            ii = o[bas[g]:bas[g] + say[g]]
            e0 = int(lo[ii[0]]); e1 = int(hi[ii[0]])
            p0 = uu[e0]; u = uu[e1] - p0; u /= np.linalg.norm(u)
            a1 = np.cross(u, [1.0, 0, 0]) if abs(u[0]) < 0.9 else np.cross(u, [0, 1.0, 0]); a1 /= np.linalg.norm(a1); a2 = np.cross(u, a1)
            w = uu[uc[ii]] - p0
            th = np.round(np.arctan2(w @ a2, w @ a1), 9)
            yy = yon[ii]
            s_ = np.lexsort((~yy, th))                      # açı, sonra yon True (0) önce
            ii, yy = ii[s_], yy[s_]
            k = len(ii)
            for t in range(k):
                if not yy[t] and yy[(t + 1) % k]:
                    R1.append(tri[ii[t]]); R2.append(tri[ii[(t + 1) % k]])
        r += R1; q += R2
    r = np.array(r, np.int64); q = np.array(q, np.int64)
    G = coo_matrix((np.ones(len(r)), (r, q)), shape=(n, n))
    nc, lab = connected_components(G, directed=False)
    # kapalılık: (bileşen, kenar) grubunda tam 2 kullanım, ters yön
    lb = lab[tri]
    o2 = np.lexsort((ek, lb)); k1 = lb[o2]; k2 = ek[o2]
    yeni = np.r_[True, (k1[1:] != k1[:-1]) | (k2[1:] != k2[:-1])]
    bas2 = np.where(yeni)[0]; say2 = np.diff(np.r_[bas2, len(o2)])
    yt = np.add.reduceat(yon[o2].astype(int), bas2)
    iyi_k = (say2 == 2) & (yt == 1)
    acik = np.zeros(nc, bool); acik[k1[bas2[~iyi_k]]] = True
    sira = np.argsort(lab, kind="stable"); sb = np.r_[0, np.where(np.diff(lab[sira]))[0] + 1, n]
    for j in range(len(sb) - 1):
        ii = sira[sb[j]:sb[j + 1]]; cmp = lab[ii[0]]
        vv, F = np.unique(vid[ii].ravel(), return_inverse=True)
        out.append(Bil(dugum, len(out), P[ii], uu[vv], F.reshape(-1, 3), not acik[cmp]))
    return out


# ============================================================================== VTK
def vtk_yuzey(V, F):
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(np.ascontiguousarray(V, dtype=np.float64), deep=1))
    cells = vtk.vtkCellArray(); ids = np.hstack([np.full((len(F), 1), 3), F]).astype(np.int64).ravel()
    cells.ImportLegacyFormat(numpy_to_vtkIdTypeArray(ids, deep=1))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(cells); return pd


def icerde(yz, Q):
    if not len(Q): return np.zeros(0, bool)
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(np.ascontiguousarray(Q, dtype=np.float64), deep=1))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts)
    se = vtk.vtkSelectEnclosedPoints(); se.SetInputData(pd); se.SetSurfaceData(yz); se.SetTolerance(1e-9); se.CheckSurfaceOff(); se.Update()
    return vtk_to_numpy(se.GetOutput().GetPointData().GetArray("SelectedPoints")).astype(bool)


def yuzey_uzaklik(yz, Q):
    f = vtk.vtkImplicitPolyDataDistance(); f.SetInput(yz)
    o = vtk.vtkDoubleArray(); f.FunctionValue(numpy_to_vtk(np.ascontiguousarray(Q, dtype=np.float64), deep=1), o)
    return np.abs(vtk_to_numpy(o))


# ============================================================================== yoğun örnekleme (bölge içi, kenar ≤ adım)
def _ort(Q, lo, hi):
    return ((Q.max(1) >= lo) & (Q.min(1) <= hi)).all(1)


def ornekle(P, lo, hi, adim=ADIM, sinir=4_000_000):
    """P üçgenlerinin [lo, hi] kutusundaki kısmı · en uzun kenardan ikiye bölerek her kenar ≤ adim → köşeler + ağırlık merkezleri"""
    cur = P[_ort(P, lo, hi)]; out = []; top = 0
    while len(cur):
        E = np.stack([np.linalg.norm(cur[:, 1] - cur[:, 0], axis=1), np.linalg.norm(cur[:, 2] - cur[:, 1], axis=1),
                      np.linalg.norm(cur[:, 0] - cur[:, 2], axis=1)], 1)
        L = E.max(1); k = L <= adim
        if k.any():
            Q = cur[k]; out.append(np.concatenate([Q.reshape(-1, 3), Q.mean(1)])); top += len(Q) * 4
        B = cur[~k]
        if not len(B) or top > sinir: break
        e = E[~k].argmax(1)
        B = np.stack([np.take_along_axis(B, ((e + j) % 3)[:, None, None].repeat(3, 2), 1)[:, 0] for j in range(3)], 1)   # en uzun kenar v0-v1
        m = (B[:, 0] + B[:, 1]) / 2
        N = np.concatenate([np.stack([B[:, 0], m, B[:, 2]], 1), np.stack([m, B[:, 1], B[:, 2]], 1)])
        cur = N[_ort(N, lo, hi)]
    if not out: return np.zeros((0, 3)), top > sinir
    Q = np.concatenate(out)
    Q = Q[((Q >= lo) & (Q <= hi)).all(1)]
    return np.unique(np.round(Q, 4), axis=0), top > sinir


def batma(kap, dig, lo, hi):
    """dig yüzeyinin [lo,hi] içindeki noktalarından KAP katısının içinde kalanlar → (en derin, nokta, sayı, sınır aşıldı mı)"""
    if not kap.kapali: return 0.0, None, 0, False
    Q, tasti = ornekle(dig.P, lo, hi)
    if not len(Q): return 0.0, None, 0, tasti
    m = icerde(kap.yz(), Q)
    if not m.any(): return 0.0, None, 0, tasti
    Qi = Q[m]; d = yuzey_uzaklik(kap.yz(), Qi); i = int(d.argmax())
    return float(d[i]), Qi[i], int((d > ESIK).sum()), tasti


# ============================================================================== çift değerlendirme
def cift(A, B):
    lo = np.maximum(A.lo, B.lo) - PAY; hi = np.minimum(A.hi, B.hi) + PAY
    if (lo > hi).any(): return None
    ma, mb = A.mf(), B.mf()
    hacim = None
    if ma and mb:
        I = ma ^ mb; hacim = I.volume()
        if hacim < 1e-3 or I.is_empty():
            g = ma.min_gap(mb, 0.1)
            return ("TEMAS", round(float(g), 3), hacim, None) if g <= ESIK else None
        sa = I.surface_area(); kal = 2.0 * hacim / max(sa, 1e-9)
        bb = I.bounding_box(); lo = np.array(bb[:3]) - 0.1; hi = np.array(bb[3:]) + 0.1
        if kal < 0.01:
            return ("TEMAS", 0.0, hacim, None)
    elif not A.kapali and not B.kapali:
        return None
    d1, q1, n1, t1 = batma(A, B, lo, hi)               # (a) diğeri kümenin içinde
    d2, q2, n2, t2 = batma(B, A, lo, hi)               # (b) küme diğerinin içinde
    d, q, yon = (d1, q1, "a") if d1 >= d2 else (d2, q2, "b")
    if d > ESIK: return ("CAKISMA", round(d, 3), hacim, dict(nokta=np.round(q, 1).tolist(), yon=yon, n=n1 + n2, kutu=[np.round(lo, 1).tolist(), np.round(hi, 1).tolist()],
                                                          sinir=t1 or t2))
    if (t1 or t2) and hacim is not None and hacim > 1.0:          # örnekleme sınırı aşıldı → kesin değil
        return ("INCELE", round(d, 3), hacim, dict(kutu=[np.round(lo, 1).tolist(), np.round(hi, 1).tolist()]))
    if d > 0 or hacim is not None: return ("TEMAS", round(d, 3), hacim, None)
    return None


# ============================================================================== OCC doğrulama
def occ_dogrula(kap, Q):
    try:
        sys.path.insert(0, os.path.join(HERE, "tg"))
        from dikis import kati
        import cadquery as cq
        from OCP.BRepClass3d import BRepClass3d_SolidClassifier
        from OCP.BRepExtrema import BRepExtrema_DistShapeShape
        from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
        from OCP.gp import gp_Pnt
        from OCP.TopAbs import TopAbs_IN
        if kap._occ is None:
            ss = kati(kap.V, kap.F, birlestir=False)
            kap._occ = ss[0] if len(ss) == 1 else cq.Compound.makeCompound(ss)
        s = kap._occ; kab = cq.Compound.makeCompound(s.Faces())
        cl = BRepClass3d_SolidClassifier(s.wrapped); out = []
        for q in np.atleast_2d(Q):
            cl.Perform(gp_Pnt(*q), 1e-6)
            if cl.State() != TopAbs_IN: out.append(0.0); continue
            dd = BRepExtrema_DistShapeShape(BRepBuilderAPI_MakeVertex(gp_Pnt(*q)).Vertex(), kab.wrapped); dd.Perform()
            out.append(dd.Value())
        return out
    except Exception as e:
        return "OCC hata: %s" % e


# ============================================================================== ana denetim
def eslesir(nd, desenler):
    import fnmatch
    return any(fnmatch.fnmatchcase(nd, d if "*" in d else d + "*") for d in desenler)


def yukle_bilesen(D, onekler=None):
    B = []
    for nd, P in D.items():
        if onekler is not None and not eslesir(nd, onekler): continue
        B += bilesenler(nd, P)
    return B


def denetle(glb, kumeler, taban=None, cikti=None, yaz=print, occ=True):
    t0 = time.time()
    D = glb_oku(glb)
    TUM = yukle_bilesen(D)
    yaz("model %s · %d düğüm · %d bileşen (%d kapalı) · %.0f s" % (os.path.basename(glb), len(D), len(TUM), sum(b.kapali for b in TUM), time.time() - t0))
    eski = set()
    if taban and any(k[2] for k in kumeler):
        DT = glb_oku(taban)
        for ad, onek, deg in kumeler:
            if deg: eski |= {(b.dugum, b.ozet) for b in yukle_bilesen(DT, onek)}
    LO = np.array([b.lo for b in TUM]); HI = np.array([b.hi for b in TUM])
    SONUC = {}
    for kad, onek, deg in kumeler:
        ozn = [i for i, b in enumerate(TUM) if eslesir(b.dugum, onek) and not (deg and (b.dugum, b.ozet) in eski)]
        oz = set(ozn)
        bul, tem, inc, acik = [], [], [], []
        gorulen = set()
        for i in ozn:
            A = TUM[i]
            if not A.kapali: acik.append(A.ad)
            m = ((LO <= A.hi + PAY) & (HI >= A.lo - PAY)).all(1); m[i] = False
            for j in np.where(m)[0]:
                if j in oz and (min(i, j), max(i, j)) in gorulen: continue
                gorulen.add((min(i, j), max(i, j)))
                r = cift(A, TUM[j])
                if r is None: continue
                kayit = dict(parca=A.ad, komsu=TUM[j].ad, tip=r[0], derinlik=r[1], hacim=None if r[2] is None else round(r[2], 3), bilgi=r[3])
                if r[0] == "CAKISMA":
                    if occ:
                        kap = A if r[3]["yon"] == "a" else TUM[j]
                        kayit["occ_derinlik"] = occ_dogrula(kap, np.array([r[3]["nokta"]]))
                    bul.append(kayit)
                elif r[0] == "INCELE": inc.append(kayit)
                else: tem.append(kayit)
        SONUC[kad] = dict(parca_sayisi=len(ozn), acik_ag=acik, cakisma=bul, incele=inc, temas=tem)
        yaz("\n== KÜME %s · %d bileşen (%s) · açık ağ %d · ÇAKIŞMA %d · İNCELE %d · TEMAS %d · %.0f s" %
            (kad, len(ozn), ",".join(onek), len(acik), len(bul), len(inc), len(tem), time.time() - t0))
        for r in sorted(bul, key=lambda r: -r["derinlik"]):
            yaz("   ÇAKIŞMA %-44s ↔ %-44s derinlik %.3f mm · OCC %s · hacim %s · nokta %s · yön %s" %
                (r["parca"], r["komsu"], r["derinlik"], r.get("occ_derinlik"), r["hacim"], r["bilgi"]["nokta"], r["bilgi"]["yon"]))
        for r in inc: yaz("   İNCELE  %-44s ↔ %-44s hacim %s · örnek derinlik %.3f · kutu %s" % (r["parca"], r["komsu"], r["hacim"], r["derinlik"], r["bilgi"]["kutu"]))
        if acik: yaz("   açık ağ (kapalı katı değil; yalnız diğerinin içi sorulur): %s" % ", ".join(acik[:30]))
    if cikti:
        os.makedirs(cikti, exist_ok=True)
        json.dump(SONUC, open(os.path.join(cikti, "denetim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    return SONUC


# ============================================================================== sahte çakışma sınaması
def _kutu(x0, x1, y0, y1, z0, z1):
    V = np.array([[x, y, z] for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)], float)
    F = np.array([[0, 1, 3], [0, 3, 2], [4, 6, 7], [4, 7, 5], [0, 4, 5], [0, 5, 1], [2, 3, 7], [2, 7, 6], [0, 2, 6], [0, 6, 4], [1, 5, 7], [1, 7, 3]])
    return V[F]


def _ters(P): return P[:, ::-1]


def test():
    ok = True

    def bil(ad, P): return bilesenler(ad, P)

    def sor(ad, A, B, bek):
        nonlocal ok
        r = cift(A, B); tip = r[0] if r else None
        gec = (tip == bek)
        ok &= gec
        print("  %-62s → %-9s derinlik %-7s beklenen %-9s %s" % (ad, tip, r[1] if r else "-", bek, "GEÇTİ" if gec else "KALDI"))
        return r
    print("SAHTE ÇAKIŞMA SINAMASI")
    # kutunun yönü: dışa normal mi
    S = bil("sac", _kutu(0, 400, 0, 1.5, 0, 300))[0]
    assert S.kapali, "kutu kapalı değil"
    if S.mf() and S.mf().volume() < 0: print("  ! ters yönlü kutu")
    # 1 ince sacı dik geçen levha (2 mm kalın, sacın içinden boydan boya)
    L = bil("levha", _kutu(100, 102, -50, 50, 50, 250))[0]
    r = sor("1 sac 1,5 ↔ dik geçen levha 2 mm (sac geçişi)", S, L, "CAKISMA")
    # 1b aynı, eski yöntem: 4 mm köşe/ağ. merk./kenar ortası + katıya uzaklık
    # 1b BÜYÜK levha (1000 × 200, üçgenleri iri) → eski yöntem: 4 mm barisentrik ızgara (u_ortak.ornekle) + derinlik = KATIYA uzaklık
    LB = bil("levha_buyuk", _kutu(100, 102, -500.3, 499.7, 50, 250))[0]
    sor("1b sac 1,5 ↔ büyük levha (iri üçgen) geçişi", S, LB, "CAKISMA")
    try:
        sys.path.insert(0, os.path.join(HERE, "ug")); from u_ortak import ornekle as eski_ornekle
        Q, _ = eski_ornekle(LB.P, None, 4.0, 120); ic = icerde(S.yz(), Q)
        import cadquery as cq
        from OCP.BRepExtrema import BRepExtrema_DistShapeShape
        from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
        from OCP.gp import gp_Pnt
        kut = cq.Solid.makeBox(400, 1.5, 300)
        dd = BRepExtrema_DistShapeShape(BRepBuilderAPI_MakeVertex(gp_Pnt(101, 0.75, 100)).Vertex(), kut.wrapped); dd.Perform()
        print("     ESKİ YÖNTEM: 4 mm ızgara sacın içine %d nokta düşürdü (%s) · sacın ortasındaki noktanın KATIYA uzaklığı %.3f mm → "
              "'> 0,05' süzgeci %s" % (ic.sum(), "KAÇIRIR" if not ic.any() else "yakalar", dd.Value(), "ELER (hata)" if dd.Value() <= 0.05 else "geçirir"))
    except Exception as e:
        print("     eski yöntem gösterimi yapılamadı:", e)
    # 2 dolu kutu içinde küçük parça (tamamen gömülü)
    K = bil("kutu", _kutu(0, 100, 0, 100, 0, 100))[0]
    k2 = bil("ic", _kutu(40, 45, 40, 45, 40, 45))[0]
    r = sor("2 dolu kutu ↔ içine gömülü 5 mm küp (yüzey kesişmez)", K, k2, "CAKISMA")
    r = sor("2b ters sıra (küme = gömülü küp, (b) yönü)", k2, K, "CAKISMA")
    # 3 temas: yüz yüze oturan iki kutu
    k3 = bil("ust", _kutu(0, 100, 100, 150, 0, 100))[0]
    sor("3 yüz yüze oturan iki kutu (temas)", K, k3, "TEMAS")
    # 4 0,03 mm bindirme (eşik altı) → temas
    k4 = bil("ust2", _kutu(10, 90, 99.97, 150, 10, 90))[0]
    sor("4 0,03 mm bindirme (eşik altı)", K, k4, "TEMAS")
    # 5 0,2 mm bindirme → çakışma
    k5 = bil("ust3", _kutu(10, 90, 99.8, 150, 10, 90))[0]
    sor("5 0,2 mm bindirme", K, k5, "CAKISMA")
    # 6 açık ağ (tek yüzey şerit) sacı deler
    Y = _kutu(200, 201, -20, 20, 100, 200)[[0, 1]]            # yalnız 2 üçgen: x=200 yüzü → açık ağ
    Ya = bil("serit", Y)[0]
    sor("6 açık yüzey şerit sacı deliyor", S, Ya, "CAKISMA")
    # 7 0,5 mm boşluk → hiçbir şey
    k7 = bil("bos", _kutu(0, 100, 100.5, 150, 0, 100))[0]
    sor("7 0,5 mm boşluk", K, k7, None)
    # 8 iki kutu aynı düğümde, paylaşılan yüz (bileşen ayrımı)
    PP = np.concatenate([_kutu(0, 10, 0, 10, 0, 10), _kutu(0, 10, 10, 20, 0, 10)])
    bb = bil("ikili", PP)
    g = len(bb) == 2 and all(b.kapali for b in bb); ok &= g
    print("  %-62s → %d bileşen, kapalı %s %s" % ("8 aynı düğümde yüz paylaşan iki kutu ayrılıyor", len(bb), [b.kapali for b in bb], "GEÇTİ" if g else "KALDI"))
    print("SINAMA:", "GEÇTİ" if ok else "KALDI")
    return ok


if __name__ == "__main__":
    if "--test" in sys.argv:
        r = test(); sys.stdout.flush(); os._exit(0 if r else 1)
    ap = argparse.ArgumentParser()
    ap.add_argument("glb"); ap.add_argument("cikti")
    ap.add_argument("--kume", action="append", required=True)
    ap.add_argument("--taban")
    ap.add_argument("--occsiz", action="store_true")
    a = ap.parse_args()
    K = []
    for s in a.kume:
        ad, ok_ = s.split("=", 1); deg = ok_.endswith("@degisen"); ok_ = ok_.replace("@degisen", "")
        K.append((ad, tuple(x for x in ok_.split(",") if x), deg))
    os.makedirs(a.cikti, exist_ok=True)
    LOG = open(os.path.join(a.cikti, "rapor.txt"), "w", encoding="utf-8")

    def yaz(*x):
        s = " ".join(str(v) for v in x); print(s); LOG.write(s + "\n"); LOG.flush(); sys.stdout.flush()
    denetle(a.glb, K, a.taban, a.cikti, yaz, occ=not a.occsiz)
    LOG.close(); sys.stdout.flush(); os._exit(0)
