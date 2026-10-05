# -*- coding: utf-8 -*-
"""AUTOKITCH · MONTAJ ÖNBELLEĞİ (27 Eyl 2026) — Kemal: "her seferinde tüm montajı baştan üretme, sadece ilgili bölümü yap".

İÇERİK ADRESLİ: her ağır işlem, girdisinin GEOMETRİSİNDEN çıkan parmak iziyle diske yazılır; sonraki koşuda aynı girdi
gelirse sonuç diskten okunur. Değişen parça ve ona dokunan işlemler yeniden hesaplanır, gerisi okunur. Anahtar geometrinin
kendisi olduğu için eski sonucun yanlışlıkla kullanılması mümkün değil (kod değişse bile).

Önbelleğe alınanlar:
  · Shape.cut / fuse / intersect / clean (Compound dahil) → sonuç BRep
  · Shape.tessellate → köşe + üçgen listesi (bütün ag() fonksiyonları buradan geçer)
  · cadquery importStep → STEP dosyasının baytlarıyla anahtarlanır
Taşıma / döndürme / kopya: anahtar ebeveynden türetilir (dışa aktarma yok).
Parmak izi: parçanın BRep'i (üçgensiz) · ilk kez gerekince hesaplanır ve parçanın üstünde saklanır (._ok).
Kullanım: montaj betiğinin EN ÜSTÜNDE `import onbellek as OB` (cadquery'den hemen sonra) · sonda OB.ozet().
Kapatmak için ortam değişkeni AUTOKITCH_ONBELLEK=0. Önbellek klasörü: %LOCALAPPDATA%\\AUTOKITCH_onbellek (repo dışı)."""
import builtins, hashlib, io, os, pickle, time
import cadquery as cq
from OCP.BRepTools import BRepTools
from OCP.TopTools import TopTools_FormatVersion

SURUM = "ob1"
ACIK = os.environ.get("AUTOKITCH_ONBELLEK", "1") != "0"
KOK = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "AUTOKITCH_onbellek")
for _d in ("op", "ag", "step"):
    os.makedirs(os.path.join(KOK, _d), exist_ok=True)
SAY = dict(bb_oku=0, bb_hesap=0, op_oku=0, op_hesap=0, ag_oku=0, ag_hesap=0, step_oku=0, step_hesap=0, parmak_izi=0)
SURE = dict(op=0.0, ag=0.0, iz=0.0)
T0 = time.time()


def _h(*p):
    return hashlib.sha1("|".join(str(x) for x in p).encode("utf-8")).hexdigest()


def _brep_bayt(s):
    bio = io.BytesIO()
    BRepTools.Write_s(s.wrapped, bio, False, False, TopTools_FormatVersion.TopTools_FormatVersion_CURRENT)
    return bio.getvalue()


def anahtar(s):
    k = getattr(s, "_ok", None)
    if k:
        return k
    t = time.time()
    k = hashlib.sha1(_brep_bayt(s)).hexdigest()
    SURE["iz"] += time.time() - t; SAY["parmak_izi"] += 1
    try:
        s._ok = k
    except Exception:
        pass
    return k


def _rp(v):
    """kararlı repr: sayı / metin / demet / Vector / Location; bilinmeyen tür → None (anahtar türetilmez)"""
    if isinstance(v, (int, float, str, bool)) or v is None:
        return repr(v)
    if isinstance(v, cq.Vector):
        return "V(%r,%r,%r)" % v.toTuple()
    if isinstance(v, cq.Location):
        return "L%r" % (v.toTuple(),)
    if isinstance(v, (tuple, list)):
        r = [_rp(x) for x in v]
        return None if any(x is None for x in r) else "(" + ",".join(r) + ")"
    if isinstance(v, dict):
        r = [(k, _rp(x)) for k, x in sorted(v.items())]
        return None if any(x is None for _k, x in r) else repr(r)
    return None


def _sar_op(cls, ad):
    orj = cls.__dict__[ad]

    def w(self, *others, **kw):
        try:
            kws = _rp(kw)
            if kws is None or any(not isinstance(o, cq.Shape) for o in others):
                raise ValueError
            key = _h(SURUM, cls.__name__, ad, anahtar(self), *[anahtar(o) for o in others], kws)
        except Exception:
            return orj(self, *others, **kw)
        yol = os.path.join(KOK, "op", key[:2], key + ".brep")
        t = time.time()
        if os.path.exists(yol):
            try:
                r = cq.Shape.importBrep(yol)
                r._ok = key; SAY["op_oku"] += 1; SURE["op"] += time.time() - t
                return r
            except Exception:
                pass
        r = orj(self, *others, **kw); SAY["op_hesap"] += 1
        try:
            os.makedirs(os.path.dirname(yol), exist_ok=True)
            r.exportBrep(yol + ".tmp"); os.replace(yol + ".tmp", yol)
            r._ok = key
        except Exception:
            pass
        SURE["op"] += time.time() - t
        return r
    w.__name__ = ad; w._onbellek = True
    setattr(cls, ad, w)


def _sar_tr(cls, ad, ayni=False):
    orj = cls.__dict__[ad]

    def w(self, *a, **kw):
        r = orj(self, *a, **kw)
        k = getattr(self, "_ok", None)
        if k is not None and r is not self and isinstance(r, cq.Shape):
            if ayni:
                r._ok = k
            else:
                ar, kr = _rp(a), _rp(kw)
                if ar is not None and kr is not None:
                    try:
                        r._ok = _h(SURUM, "tr", ad, k, ar, kr)
                    except Exception:
                        pass
        return r
    w.__name__ = ad; w._onbellek = True
    setattr(cls, ad, w)


def _sar_yerinde(cls, ad):
    """yerinde değiştiren işlem (move / locate): anahtar ya türetilir ya silinir — eski anahtar ASLA kalmaz"""
    orj = cls.__dict__[ad]

    def w(self, *a, **kw):
        k = getattr(self, "_ok", None)
        r = orj(self, *a, **kw)
        if k is not None:
            ar, kr = _rp(a), _rp(kw)
            try:
                if ar is None or kr is None:
                    del self._ok
                else:
                    self._ok = _h(SURUM, "yer", ad, k, ar, kr)
            except Exception:
                try:
                    del self._ok
                except Exception:
                    pass
        return r
    w.__name__ = ad; w._onbellek = True
    setattr(cls, ad, w)


BB_YOL = os.path.join(KOK, "bb.pkl")
try:
    with open(BB_YOL, "rb") as _f:
        BB = pickle.load(_f)
except Exception:
    BB = {}
BB_YENI = [0]


def bb_kaydet():
    if not BB_YENI[0]:
        return
    try:
        with open(BB_YOL + ".tmp", "wb") as f:
            pickle.dump(BB, f, protocol=4)
        os.replace(BB_YOL + ".tmp", BB_YOL); BB_YENI[0] = 0
    except Exception:
        pass


def _sar_bb():
    """BoundingBox (BRepBndLib.AddOptimal) — ölçüldü: fırın üretecinin 23 sn'sinin 20'si. Parmak iziyle önbellek."""
    from OCP.Bnd import Bnd_Box
    orj = cq.Shape.__dict__["BoundingBox"]

    def w(self, tolerance=None):
        try:
            key = _h(SURUM, "bb", anahtar(self), repr(tolerance))
        except Exception:
            return orj(self, tolerance)
        v = BB.get(key)
        if v is None:
            r = orj(self, tolerance); SAY["bb_hesap"] += 1
            BB[key] = (r.xmin, r.ymin, r.zmin, r.xmax, r.ymax, r.zmax); BB_YENI[0] += 1
            if BB_YENI[0] >= 2000:
                bb_kaydet()
            return r
        SAY["bb_oku"] += 1
        b = Bnd_Box(); b.Update(*v)
        return cq.BoundBox(b)
    w._onbellek = True
    cq.Shape.BoundingBox = w


def _sar_tes():
    orj = cq.Shape.__dict__["tessellate"]

    def w(self, tolerance, angularTolerance=0.1):
        try:
            key = _h(SURUM, "tes", anahtar(self), repr(float(tolerance)), repr(float(angularTolerance)))
        except Exception:
            return orj(self, tolerance, angularTolerance)
        yol = os.path.join(KOK, "ag", key[:2], key + ".pkl")
        t = time.time()
        if os.path.exists(yol):
            try:
                with open(yol, "rb") as f:
                    P, T = pickle.load(f)
                SAY["ag_oku"] += 1; SURE["ag"] += time.time() - t
                return [cq.Vector(*p) for p in P], T
            except Exception:
                pass
        vs, ts = orj(self, tolerance, angularTolerance); SAY["ag_hesap"] += 1
        try:
            os.makedirs(os.path.dirname(yol), exist_ok=True)
            with open(yol + ".tmp", "wb") as f:
                pickle.dump(([v.toTuple() for v in vs], [tuple(x) for x in ts]), f, protocol=4)
            os.replace(yol + ".tmp", yol)
        except Exception:
            pass
        SURE["ag"] += time.time() - t
        return vs, ts
    w._onbellek = True
    cq.Shape.tessellate = w


def _sar_step():
    import cadquery.occ_impl.importers as _imp
    orj = _imp.importStep

    def w(fileName, *a, **kw):
        try:
            with open(fileName, "rb") as f:
                key = _h(SURUM, "step", hashlib.sha1(f.read()).hexdigest(), _rp(a), _rp(kw))
        except Exception:
            return orj(fileName, *a, **kw)
        yol = os.path.join(KOK, "step", key + ".pkl")
        if os.path.exists(yol):
            try:
                with open(yol, "rb") as f:
                    B = pickle.load(f)
                shs = []
                for i, b in enumerate(B):
                    s = cq.Shape.importBrep(io.BytesIO(b)); s._ok = _h(key, i); shs.append(s)
                SAY["step_oku"] += 1
                return cq.Workplane("XY").newObject(shs)
            except Exception:
                pass
        r = orj(fileName, *a, **kw); SAY["step_hesap"] += 1
        try:
            B = [_brep_bayt(s) for s in r.vals() if isinstance(s, cq.Shape)]
            with open(yol + ".tmp", "wb") as f:
                pickle.dump(B, f, protocol=4)
            os.replace(yol + ".tmp", yol)
            for i, s in enumerate([s for s in r.vals() if isinstance(s, cq.Shape)]):
                s._ok = _h(key, i)
        except Exception:
            pass
        return r
    _imp.importStep = w
    try:
        import cadquery.importers as _imp2
        _imp2.importStep = w
    except Exception:
        pass
    cq.importers.importStep = w


_orj_print = builtins.print


def _print(*a, **kw):
    if a and kw.get("file") is None:
        a = ("[%4.0f sn]" % (time.time() - T0),) + a
    _orj_print(*a, **kw)


def ozet():
    bb_kaydet()
    _orj_print("ONBELLEK (%s): sinir kutusu oku %d / hesapla %d · islem oku %d / hesapla %d · ag oku %d / hesapla %d · STEP oku %d / hesapla %d · parmak izi %d (%.0f sn) · islem %.0f sn · ag %.0f sn · toplam %.0f sn · klasor %s"
               % ("ACIK" if ACIK else "KAPALI", SAY["bb_oku"], SAY["bb_hesap"], SAY["op_oku"], SAY["op_hesap"], SAY["ag_oku"], SAY["ag_hesap"], SAY["step_oku"], SAY["step_hesap"],
                  SAY["parmak_izi"], SURE["iz"], SURE["op"], SURE["ag"], time.time() - T0, KOK), flush=True)


if ACIK:
    for _c in (cq.Shape, cq.Compound):
        for _m in ("cut", "fuse", "intersect"):
            if _m in _c.__dict__ and not getattr(_c.__dict__[_m], "_onbellek", False):
                _sar_op(_c, _m)
    if not getattr(cq.Shape.__dict__["clean"], "_onbellek", False):
        _sar_op(cq.Shape, "clean")
    for _m in ("translate", "rotate", "mirror", "moved", "located", "transformShape"):
        if _m in cq.Shape.__dict__ and not getattr(cq.Shape.__dict__[_m], "_onbellek", False):
            _sar_tr(cq.Shape, _m)
    for _m in ("move", "locate"):
        if _m in cq.Shape.__dict__ and not getattr(cq.Shape.__dict__[_m], "_onbellek", False):
            _sar_yerinde(cq.Shape, _m)
    if not getattr(cq.Shape.__dict__["copy"], "_onbellek", False):
        _sar_tr(cq.Shape, "copy", ayni=True)
    if not getattr(cq.Shape.__dict__["BoundingBox"], "_onbellek", False):
        _sar_bb()
    if not getattr(cq.Shape.__dict__["tessellate"], "_onbellek", False):
        _sar_tes()
    _sar_step()
    builtins.print = _print
