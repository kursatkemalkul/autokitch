# -*- coding: utf-8 -*-
"""HAT v3.2 · TÜM MAKİNE HAVADA DENETİMİ v1 — montajın dünya katı dökümünden (h3/_dunya/dunya.brep + dunya.json, hat3_montaj_v2 yazar).
Kemal (30 Eyl gece): "motorlar, beyin, sürücüler havada durmasın · kablolar havada olmasın". denetim_temas_v1.havada: her parça zemine
(y ≤ zemin + tol) DEĞEN parçalar zinciriyle bağlı mı · tol 0,5 mm (montaj toleransı: cıvata / conta / yay payı) · hareketli gruplar dinlenme konumunda.
Çıktı: h3/_dunya/havada_v1.json · kategori (motor / sürücü / pano / kablo / diğer) ve birimle."""
import io, json, os, re, sys, time
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
from OCP.TopoDS import TopoDS_Iterator
import denetim_temas_v1 as DT

DD = os.path.join(H3, sys.argv[1] if len(sys.argv) > 1 else "_dunya")               # v3.2: "_dunya_tam" = elektrik + düzeltmeler dahil
ELK = re.compile(r"motor|surucu|sürücü|pano|plc|guc_|ups|psu|sensor|sensör|kablo|klemens|role|din_ray|beckhoff|siemens|valf_ada|fan|kontrol|siwarex|ndr-|hdr-|kart", re.I)


def yukle():
    idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
    c = cq.importers.importBrep(os.path.join(DD, "dunya.brep")) if hasattr(cq.importers, "importBrep") else cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
    sh = c.val() if hasattr(c, "val") else c
    it = TopoDS_Iterator(sh.wrapped); ch = []
    while it.More():
        ch.append(cq.Shape.cast(it.Value())); it.Next()
    assert len(ch) == len(idx), (len(ch), len(idx))
    return [(i[0], i[1], i[2], i[3], s) for i, s in zip(idx, ch)]


def tur(ad, mal):
    a = ad.lower()
    if re.search(r"motor", a) and not re.search(r"plaka|braket|kasnag|mil|kaplin|konsol|yatak|flans", a): return "MOTOR"
    if re.search(r"surucu|sürücü|beckhoff|plc|siwarex|ndr-|hdr-|guc_|ups|klemens|role|din_ray|kart", a): return "BEYIN/SURUCU"
    if re.search(r"pano", a): return "PANO"
    if re.search(r"kablo|hortum", a): return "KABLO/HORTUM"
    if re.search(r"sensor|sensör", a): return "SENSOR"
    return "DIGER"


if __name__ == "__main__":
    t0 = time.time()
    L = yukle()
    print("döküm: %d parça · %.0f sn" % (len(L), time.time() - t0)); sys.stdout.flush()
    ps = [("%s|%s" % (b, a), s) for b, a, m, g, s in L if not b.startswith(("INSAN",))]
    son = DT.havada(ps, zemin_y=0.0, tol=0.5)
    DT.yaz(son, en_cok=60, baslik="HAVADA · TÜM MAKİNE v3.1")
    rap = []
    for d in son["bilesen"]:
        uy = d["uye"]
        tl = sorted(set(tur(u.split("|", 1)[1], "") for u in uy))
        rap.append(dict(en=d["en"], uye=uy, tur=tl, bb=[round(v, 1) for v in (d["bb"].xmin, d["bb"].xmax, d["bb"].ymin, d["bb"].ymax, d["bb"].zmin, d["bb"].zmax)]))
    json.dump(dict(parca=son["parca"], bilesen=rap), io.open(os.path.join(DD, "havada_v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    from collections import Counter
    c = Counter(t for r in rap for t in r["tur"])
    print("HAVADA bileşen türleri:", dict(c))
    sys.stdout.flush(); os._exit(0)
