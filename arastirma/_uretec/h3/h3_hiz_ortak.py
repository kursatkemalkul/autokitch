# -*- coding: utf-8 -*-
"""HAT v3 · HIZ ORTAK (1 Eki 2026 · Claude) — denetim/derleme hızlandırma kütüphanesi. Üreteçlere ve montaja DOKUNMAZ.

  · İÇERİK ADRESLİ ŞEKİL DEPOSU: her katı BREP baytına göre (blake2b-128) _hiz/sekil/xx/<hash>.brep — aynı bayt = aynı katı
  · DÖKÜM İNDEKSİ: _dunya / _dunya_tam (dunya.brep + dunya.json) bir kez açılır → her parça [birim, ad, mal, grup, hash, bbox]
    (indeks dosya imzasıyla önbellekte: aynı döküm ikinci kez açılmaz). Denetim süreçleri büyük dökümü yüklemez, yalnız gereken parçaları depodan alır.
  · ÇİFT ÖNBELLEĞİ (sqlite): BRepExtrema mesafesi ve kesişim hacmi (hashA, hashB) SIRALI anahtarla — sonuç aynı girdiden aynı hesaplanır,
    değişmeyen çiftler bir daha hesaplanmaz (ARTIMSAL denetim). Değer ham saklanır (mesafe / hacim / hata durumu): eşik yorumu çağıranda.
  · İŞÇİ HAVUZU: eksik çiftler multiprocessing (spawn) ile, işçide YALNIZ OCP (cadquery/VTK yok → işçi ~0,3–0,7 GB) · işçi sayısı = (boş bellek − 6 GB) / 0,7 GB,
    en çok 20 / çekirdek − 2 · H3_HIZ_ISCI ile zorlanabilir · ağır (büyük BREP) çiftler önce dağıtılır.
TAM EŞDEĞERLİK: hesap aynı OCC çağrısı (BRepExtrema_DistShapeShape(a, b) / a.intersect(b).Volume()), aynı sıra (a, b), aynı katı (BREP gidiş-dönüş, üçgenleme dahil)."""
import ctypes, hashlib, io, json, os, sqlite3, sys, time

H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
HIZ = os.environ.get("H3_HIZ_DIZIN") or os.path.join(H3, "_hiz")
SEKIL = os.path.join(HIZ, "sekil")
DB = os.path.join(HIZ, "cift.sqlite")


# ---------------------------------------------------------------- şekil baytı / hash / depo ----------------------------------------------------------------
def bayt(sh):
    import cadquery as cq
    s = sh.val() if hasattr(sh, "val") else sh
    if not isinstance(s, cq.Shape): s = cq.Shape.cast(s)
    b = io.BytesIO(); s.exportBrep(b)
    return b.getvalue()


def hsh(b):
    return hashlib.blake2b(b, digest_size=16).hexdigest()


def yol(h):
    return os.path.join(SEKIL, h[:2], h + ".brep")


def sakla(h, b):
    y = yol(h)
    if os.path.exists(y): return
    os.makedirs(os.path.dirname(y), exist_ok=True)
    t = y + ".%d.tmp" % os.getpid()
    with open(t, "wb") as f: f.write(b)
    try: os.replace(t, y)
    except OSError:
        if os.path.exists(t): os.remove(t)


def kaydet(sh):
    """şekli depoya koy, hash döndür"""
    b = bayt(sh); h = hsh(b); sakla(h, b)
    return h


def ac(h):
    import cadquery as cq
    return cq.Shape.importBrep(yol(h))


class Kutu(object):
    """cq.BoundBox ile aynı alanlar (xmin … zlen) — değerler OCC'den alınan bbox'ın kendisi"""
    __slots__ = ("xmin", "xmax", "ymin", "ymax", "zmin", "zmax", "xlen", "ylen", "zlen")

    def __init__(self, v):
        self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax, self.xlen, self.ylen, self.zlen = v


def kutu_deger(bb):
    return [bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax, bb.xlen, bb.ylen, bb.zlen]


# ---------------------------------------------------------------- döküm indeksi ----------------------------------------------------------------
def _dosya_imza(*yollar):
    h = hashlib.blake2b(digest_size=16)
    for y in yollar:
        with open(y, "rb") as f:
            while True:
                c = f.read(1 << 24)
                if not c: break
                h.update(c)
    return h.hexdigest()


def dokum_indeks(DD, kutu=True, log=print):
    """DD/dunya.brep + dunya.json → [dict(b, a, m, g, h, bb, hata)] (döküm sırası) · bb: Kutu ya da None (BoundingBox hata verdiyse)"""
    t0 = time.time()
    jb, jj = os.path.join(DD, "dunya.brep"), os.path.join(DD, "dunya.json")
    imza = _dosya_imza(jb, jj)
    iy = os.path.join(HIZ, "indeks", imza + ".json")
    if os.path.exists(iy):
        R = json.load(io.open(iy, encoding="utf-8"))
        if all(os.path.exists(yol(r["h"])) for r in R):
            for r in R: r["bb"] = Kutu(r["bb"]) if r["bb"] is not None else None
            log("hız · döküm indeksi önbellekten: %d parça · %.1f sn" % (len(R), time.time() - t0))
            return R
    if not os.environ.get("H3_HIZ_ALT"):                                               # büyük döküm ayrı süreçte açılır (ana süreç hafif kalır)
        import subprocess
        e = dict(os.environ, H3_HIZ_ALT="1")
        subprocess.check_call([sys.executable, os.path.abspath(__file__), "indeks", DD], env=e)
        R = json.load(io.open(iy, encoding="utf-8"))
        for r in R: r["bb"] = Kutu(r["bb"]) if r["bb"] is not None else None
        log("hız · döküm indekslendi (alt süreç): %d parça · %d farklı katı · %.1f sn" % (len(R), len(set(r["h"] for r in R)), time.time() - t0))
        return R
    import cadquery as cq
    from OCP.TopoDS import TopoDS_Iterator
    idx = json.load(io.open(jj, encoding="utf-8"))
    sh = cq.Shape.importBrep(jb)
    it = TopoDS_Iterator(sh.wrapped); ch = []
    while it.More():
        ch.append(cq.Shape.cast(it.Value())); it.Next()
    assert len(ch) == len(idx), (len(ch), len(idx))
    R = []
    for i, s in zip(idx, ch):
        b = bayt(s); h = hsh(b); sakla(h, b)
        try: bb = kutu_deger(s.BoundingBox())
        except Exception: bb = None
        R.append(dict(b=i[0], a=i[1], m=i[2], g=i[3], h=h, bb=bb))
    del ch, sh
    os.makedirs(os.path.dirname(iy), exist_ok=True)
    json.dump(R, io.open(iy + ".tmp", "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(iy + ".tmp", iy)
    for r in R: r["bb"] = Kutu(r["bb"]) if r["bb"] is not None else None
    log("hız · döküm indekslendi: %d parça · %d farklı katı · %.1f sn" % (len(R), len(set(r["h"] for r in R)), time.time() - t0))
    return R


# ---------------------------------------------------------------- çift önbelleği ----------------------------------------------------------------
# tur: "M" = BRepExtrema mesafesi (durum 0 tamam / 1 IsDone değil / 2 istisna) · "K" = kesişim hacmi a.intersect(b).Volume() (durum 0 / 2 istisna)
def _db():
    os.makedirs(HIZ, exist_ok=True)
    c = sqlite3.connect(DB, timeout=120)
    c.execute("CREATE TABLE IF NOT EXISTS cift (tur TEXT, a TEXT, b TEXT, durum INTEGER, v REAL, PRIMARY KEY (tur, a, b))")
    return c


def oku(tur, ciftler):
    """ciftler: [(ha, hb)] → {(ha, hb): (durum, v)} (bulunanlar)"""
    out = {}
    if not ciftler: return out
    c = _db()
    try:
        c.execute("CREATE TEMP TABLE q (a TEXT, b TEXT)")
        c.executemany("INSERT INTO q VALUES (?, ?)", list(set(ciftler)))
        for a, b, d, v in c.execute("SELECT c.a, c.b, c.durum, c.v FROM cift c JOIN q ON c.a = q.a AND c.b = q.b WHERE c.tur = ?", (tur,)):
            out[(a, b)] = (d, v)
    finally:
        c.close()
    return out


def yaz(tur, sonuc):
    c = _db()
    try:
        c.executemany("INSERT OR REPLACE INTO cift VALUES (?, ?, ?, ?, ?)", [(tur, a, b, d, v) for (a, b), (d, v) in sonuc.items()])
        c.commit()
    finally:
        c.close()


# ---------------------------------------------------------------- işçiler ----------------------------------------------------------------
_SK = {}


def _ocp_ac(h):
    """işçide yalnız OCP (cadquery/VTK yüklenmez → işçi başına bellek az) · cq.Shape.importBrep ile aynı okuma"""
    from OCP.BRepTools import BRepTools
    from OCP.BRep import BRep_Builder
    from OCP.TopoDS import TopoDS_Shape
    s = TopoDS_Shape(); BRepTools.Read_s(s, yol(h), BRep_Builder())
    if s.IsNull(): raise ValueError("okunamadı: " + h)
    return s


def _sekil_al(h):
    s = _SK.get(h)
    if s is None:
        if len(_SK) > 400: _SK.clear()
        s = _SK[h] = _ocp_ac(h)
    return s


def _hacim_ocp(a, b):
    """cadquery a.intersect(b).Volume() ile aynı OCC çağrıları (BRepAlgoAPI_Common, SetRunParallel(True), Shape._mass_calc_function kuralı)"""
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
    from OCP.TopTools import TopTools_ListOfShape
    from OCP.TopoDS import TopoDS_Iterator
    from OCP.TopAbs import TopAbs_COMPOUND, TopAbs_SOLID, TopAbs_EDGE, TopAbs_WIRE, TopAbs_FACE, TopAbs_SHELL
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    op = BRepAlgoAPI_Common(); A = TopTools_ListOfShape(); A.Append(a); T = TopTools_ListOfShape(); T.Append(b)
    op.SetArguments(A); op.SetTools(T); op.SetRunParallel(True); op.Build()
    r = op.Shape()
    t = r.ShapeType()
    if t == TopAbs_COMPOUND:
        it = TopoDS_Iterator(r)
        if it.More():
            c = it.Value()
            while c.ShapeType() == TopAbs_COMPOUND: c = TopoDS_Iterator(c).Value()
            t = c.ShapeType()
        else:
            t = TopAbs_SOLID
    f = {TopAbs_EDGE: BRepGProp.LinearProperties_s, TopAbs_WIRE: BRepGProp.LinearProperties_s, TopAbs_FACE: BRepGProp.SurfaceProperties_s,
         TopAbs_SHELL: BRepGProp.SurfaceProperties_s, TopAbs_SOLID: BRepGProp.VolumeProperties_s, TopAbs_COMPOUND: BRepGProp.VolumeProperties_s}.get(t)
    if f is None: raise TypeError("hacim fonksiyonu yok (cq'da None çağrısı)")
    P = GProp_GProps(); f(r, P)
    return P.Mass()


def _hesap(tur, ha, hb):
    a, b = _sekil_al(ha), _sekil_al(hb)
    if tur == "M":
        from OCP.BRepExtrema import BRepExtrema_DistShapeShape
        try:
            d = BRepExtrema_DistShapeShape(a, b)
            if not d.IsDone(): return (1, None)
            return (0, d.Value())
        except Exception:
            return (2, None)
    if tur == "K":
        try: return (0, _hacim_ocp(a, b))
        except Exception: return (2, None)
    raise ValueError(tur)


def _is(gorev):
    tur, L = gorev
    return [((ha, hb), _hesap(tur, ha, hb)) for ha, hb in L]


def bos_bellek_mb():
    class MS(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong), ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    try:
        m = MS(); m.dwLength = ctypes.sizeof(MS); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        return min(m.ullAvailPhys, m.ullAvailPageFile) / 1048576.0
    except Exception:
        return 8000.0


def isci_sayisi(en_cok=20, is_mb=700.0):
    e = os.environ.get("H3_HIZ_ISCI")
    if e: return max(1, int(e))
    return max(1, min(en_cok, (os.cpu_count() or 4) - 2, int((bos_bellek_mb() - 6000.0) / is_mb)))   # koordinatör kuralı: işçi × GB ≤ boş bellek − 6 GB


def hesapla(tur, ciftler, log=print, parca=40):
    """ciftler [(ha, hb)] → {(ha, hb): (durum, v)} · önce önbellek, eksikler işçilerde · sonuç önbelleğe yazılır"""
    t0 = time.time()
    ciftler = list(dict.fromkeys(ciftler))
    R = oku(tur, ciftler)
    eksik = [c for c in ciftler if c not in R]
    if eksik:
        n = isci_sayisi()
        _bo = {}
        def _boy(h):
            if h not in _bo:
                try: _bo[h] = os.path.getsize(yol(h))
                except OSError: _bo[h] = 0
            return _bo[h]
        eksik.sort(key=lambda c: -(_boy(c[0]) + _boy(c[1])))                              # ağır (büyük BREP) çiftler önce → işçiler dengeli biter
        parca = max(1, min(parca, len(eksik) // (8 * max(1, isci_sayisi())) or 1))
        gorev = [(tur, eksik[i:i + parca]) for i in range(0, len(eksik), parca)]
        yeni = {}
        if n <= 1 or len(eksik) < 8:
            n = 1
            for g in gorev:
                for k, v in _is(g): yeni[k] = v
            yaz(tur, yeni)
        else:
            import multiprocessing as mp
            ctx = mp.get_context("spawn")
            ara = {}
            with ctx.Pool(n) as pool:
                for sonuc in pool.imap_unordered(_is, gorev):
                    for k, v in sonuc:
                        yeni[k] = v; ara[k] = v
                    if len(ara) >= 1000: yaz(tur, ara); ara = {}                         # ara kayıt: yarıda kalan koşu kaybolmaz
            if ara: yaz(tur, ara)
        R.update(yeni)
        log("hız · %s çifti: %d istendi · %d önbellekten · %d hesaplandı (%d işçi) · %.1f sn" % (tur, len(ciftler), len(ciftler) - len(eksik), len(eksik), n, time.time() - t0))
    else:
        log("hız · %s çifti: %d istendi · hepsi önbellekten · %.1f sn" % (tur, len(ciftler), time.time() - t0))
    return R


if __name__ == "__main__":
    if sys.argv[1] == "indeks":
        dokum_indeks(os.path.abspath(sys.argv[2]))
    sys.stdout.flush(); os._exit(0)
