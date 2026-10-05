# -*- coding: utf-8 -*-
"""HAT v3 · HIZLI MONTAJ SARMALAYICISI (1 Eki 2026 · Claude) — montaj / üreteç dosyalarına DOKUNMAZ; aynı betiği aynı süreçte çalıştırır,
yalnız SONUCU DEĞİŞTİRMEYEN tekrar hesapları önbelleğe alır.

  KUTU ÖNBELLEĞİ (BoundingBox): cadquery Shape.BoundingBox() = BRepBndLib.AddOptimal (pahalı, profilde TOPPING kurulumunun %37'si).
    Aynı katı (aynı TShape + Location → OCC IsSame) için sonuç, katının üçgenlemesi değişmedikçe AYNIDIR → ilk sonuç saklanır.
    Üçgenlemeyi değiştirebilecek her çağrıda (BRepMesh_IncrementalMesh · BRepTools.Clean) önbellek TAMAMEN boşaltılır (nesil sayacı).
    H3_HIZ_DOGRULA=1: her önbellek isabetinde asıl hesap da yapılır ve birebir karşılaştırılır (fark = AssertionError) — yavaş, yalnız doğrulama için.

  ELEKTRİK (betik adı h3_elektrik*): h3_elk_voksel.bul içindeki örnekle/işaretle bloğu → h3_hiz_vok.isaretle (aynı hücreler; numpy, PARÇA PARÇA →
    6–9 M noktalık tek diziler yok: v3.6 elektrik koşularını düşüren ArrayMemoryError'ın kaynağı) · blok metni değişmişse yalnız _ornekle değişir.

Kullanım (cwd = arastirma/_uretec, eski zincirle aynı):
  python -u h3/h3_hiz_montaj.py h3/hat3_montaj_v6.py          (≡ python -u h3/hat3_montaj_v6.py, çıktılar birebir aynı)
  python -u h3/h3_hiz_montaj.py h3/h3_elektrik_v1.py          (≡ python -u h3/h3_elektrik_v1.py)
Sonda: 'hız · kutu önbelleği: N çağrı · isabet …' satırı."""
import os, runpy, sys, time

T0 = time.time()
betik = os.path.abspath(sys.argv[1])
sys.argv = [betik] + sys.argv[2:]
sys.path.insert(0, os.path.dirname(betik))
DOGRULA = bool(os.environ.get("H3_HIZ_DOGRULA"))

# ---------------------------------------------------------------- üçgenleme değiştiren çağrılar → önbellek boşalır ----------------------------------------------------------------
import OCP.BRepMesh as _BM
import OCP.BRepTools as _BT

_KB = {}                                  # hash(TopoDS_Shape) → [(TopoDS_Shape, BoundBox)]
_SAY = dict(cagri=0, isabet=0, bosalt=0, dogrulanan=0)
_ASIL_MESH = _BM.BRepMesh_IncrementalMesh


def _bosalt():
    if _KB: _KB.clear()
    _SAY["bosalt"] += 1


def _mesh(*a, **k):
    _bosalt()
    return _ASIL_MESH(*a, **k)


_BM.BRepMesh_IncrementalMesh = _mesh
_ASIL_CLEAN = _BT.BRepTools.Clean_s


def _clean(*a, **k):
    _bosalt()
    return _ASIL_CLEAN(*a, **k)


try:
    _BT.BRepTools.Clean_s = staticmethod(_clean)
    _CLEAN_YAMA = True
except Exception:                         # yamalanamıyorsa güvenli taraf: önbellek kapalı
    _CLEAN_YAMA = False

import cadquery as cq
from cadquery.occ_impl import shapes as _S, geom as _G
for _m in (_S, _G):
    if hasattr(_m, "BRepMesh_IncrementalMesh"): _m.BRepMesh_IncrementalMesh = _mesh
    if hasattr(_m, "BRepTools") and _CLEAN_YAMA: pass   # sınıf aynı nesne (yukarıda yamalandı)

_ASIL_BB = _S.Shape.BoundingBox


def _esit(a, b):
    return (a.xmin, a.xmax, a.ymin, a.ymax, a.zmin, a.zmax) == (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)


def _bb(self, tolerance=None):
    if tolerance is not None or not _CLEAN_YAMA:
        return _ASIL_BB(self, tolerance)
    _SAY["cagri"] += 1
    w = self.wrapped
    k = hash(w)
    L = _KB.get(k)
    if L is not None:
        for w2, bb in L:
            if w2.IsSame(w):
                _SAY["isabet"] += 1
                if DOGRULA:
                    yeni = _ASIL_BB(self)
                    assert _esit(yeni, bb), "kutu önbelleği FARKLI: %s ≠ %s" % ((yeni.xmin, yeni.xmax), (bb.xmin, bb.xmax))
                    _SAY["dogrulanan"] += 1
                return bb
    bb = _ASIL_BB(self)
    if len(_KB) > 300000: _KB.clear()
    _KB.setdefault(k, []).append((w, bb))
    return bb                             # cq BoundBox değişmez kullanılır (add / enlarge yeni nesne döndürür; üreteçlerde alan ataması yok — tarandı)


_S.Shape.BoundingBox = _bb
_S.Shape._hiz_asil_bb = _ASIL_BB                                         # doğrulama betikleri için asıl fonksiyon


def _rapor():
    c = _SAY["cagri"]
    sys.stdout.write("hız · kutu önbelleği: %d çağrı · isabet %d (%%%.0f) · boşaltma %d%s · toplam %.0f sn\n"
                     % (c, _SAY["isabet"], 100.0 * _SAY["isabet"] / max(1, c), _SAY["bosalt"], (" · doğrulanan %d (hepsi aynı)" % _SAY["dogrulanan"]) if DOGRULA else "", time.time() - T0))
    sys.stdout.flush()


# ---------------------------------------------------------------- elektrik: voksel örnekleme numpy (h3_hiz_vok · noktalar birebir aynı) ----------------------------------------------------------------
if os.path.basename(betik).startswith("h3_elektrik") and not os.environ.get("H3_HIZ_VOK_KAPALI"):
    import h3_elk_voksel as _EV, h3_hiz_vok as _HV
    print("hız · voksel yaması: %s" % ("bul() parça parça işaretleme + numpy örnekleme" if _HV.yamala(_EV) else "yalnız numpy örnekleme"))

_ASIL_EXIT = os._exit


def _exit(c=0):
    _rapor()
    _ASIL_EXIT(c)


os._exit = _exit
if __name__ == "__main__":
    kod = 0
    try:
        runpy.run_path(betik, run_name="__main__")
    except SystemExit as e:
        kod = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    except BaseException:
        import traceback; traceback.print_exc(); kod = 1
    _rapor()
    sys.stdout.flush(); sys.stderr.flush()
    _ASIL_EXIT(kod)                                                                  # cadquery kapanış çökmesine girmeden (montaj da os._exit kullanır)
