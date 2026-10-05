# -*- coding: utf-8 -*-
"""HAT v3.2 · HEDEFLİ HAVADA DENETİMİ v1 — tam denetim (h3_havada_v1, ~2 saat) yerine yalnız DEĞİŞEN parçalar:
kök = tam denetimde zemine bağlı çıkmış makine parçaları (elektrik ELK_ · düzeltme DUZ_ · ilk tam denetimin havada listesi HARİÇ) ·
aday = elektrik + düzeltme + ilk listedekiler · aday ↔ herkes temas (tol 0,5) · kökten yayılım · bağlanmayan aday = HAVADA.
Not: kök parçalar v3.1 → v3.2 arasında yalnız delik (kesik) aldı; delikler bağlantıyı koparmaz (tam denetim ayrıca koşar)."""
import io, json, os, sys, time
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
import h3_havada_v1 as HV

if __name__ == "__main__":
    t0 = time.time()
    HV.DD = os.path.join(H3, "_dunya_tam")
    L = [("%s|%s" % (b, a), s) for b, a, m, g, s in HV.yukle() if not b.startswith("INSAN")]
    ilk = json.load(io.open(os.path.join(H3, "_dunya", "havada_v1.json"), encoding="utf-8"))
    ilk_havada = set(u for d in ilk["bilesen"] for u in d["uye"])
    aday = [i for i, (ad, s) in enumerate(L) if ad.startswith(("ELK_", "DUZ_")) or ad in ilk_havada]
    B = [s.BoundingBox() for ad, s in L]
    tol = 0.5
    kom = {i: set() for i in aday}
    for i in aday:
        bi = B[i]
        for j in range(len(L)):
            if j == i: continue
            bj = B[j]
            if bj.xmin > bi.xmax + tol or bi.xmin > bj.xmax + tol or bj.ymin > bi.ymax + tol or bi.ymin > bj.ymax + tol or bj.zmin > bi.zmax + tol or bi.zmin > bj.zmax + tol:
                continue
            try:
                d = BRepExtrema_DistShapeShape(L[i][1].wrapped, L[j][1].wrapped); ok = d.IsDone() and d.Value() <= tol
            except Exception:
                ok = True
            if ok:
                kom[i].add(j)
                if j in kom: kom[j].add(i)
    A = set(aday)
    gor = set(j for j in range(len(L)) if j not in A)                                  # kökler
    gor |= set(i for i in aday if B[i].ymin <= tol)                                    # zemine değen adaylar
    degisti = True
    while degisti:
        degisti = False
        for i in aday:
            if i not in gor and kom[i] & gor:
                gor.add(i); degisti = True
    havada = [L[i][0] for i in aday if i not in gor]
    print("HEDEFLİ HAVADA (v3.2): %d parça döküm · %d aday (elektrik + düzeltme + ilk listedeki %d) · HAVADA %d · %.0f sn"
          % (len(L), len(aday), len(ilk_havada), len(havada), time.time() - t0))
    for h in havada[:80]: print("   HAVADA:", h)
    json.dump(dict(aday=len(aday), havada=havada), io.open(os.path.join(H3, "_dunya_tam", "havada_hizli_v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    sys.stdout.flush(); os._exit(0)
