# -*- coding: utf-8 -*-
"""HAT v3.4 · HEDEFLİ HAVADA DENETİMİ — PARALEL (h3_havada_hizli_v1 ile aynı yöntem, adaylar N sürece bölünür).
Aday = elektrik ELK_ + düzeltme DUZ_ + ilk tam denetimin havada listesi + v3.4'te DEĞİŞEN makine parçaları
(TOPPING harç ünitesi + evaporatör kaseti · A tavanı + U_A tabanı · robot kablosu / zemin üstü köprü · QR alt bölümü).
Kullanım:  python h3/h3_havada_paralel_v1.py parca K N     (K = 0 … N−1, her biri ayrı süreçte)
           python h3/h3_havada_paralel_v1.py birlestir N   (yayılım + sonuç)"""
import io, json, os, sys, time
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
import h3_havada_v1 as HV

DEGISEN = ("TOPPING_MODUL|harc", "TOPPING_MODUL|evap_kaseti", "TOPPING_MODUL|arka_duvar_kaset", "TOPPING_MODUL|kaset_penceresi",
           "ROBOT_", "A_GOVDE|a_govde_ust", "A_GOVDE|a_ust_kusak", "U_A_GOVDE|", "QR_GOVDE|servis", "ZEMIN")
TOL = 0.5


def yukle():
    HV.DD = os.path.join(H3, "_dunya_tam")
    L = [("%s|%s" % (b, a), s) for b, a, m, g, s in HV.yukle() if not b.startswith("INSAN")]
    ilk = json.load(io.open(os.path.join(H3, "_dunya", "havada_v1.json"), encoding="utf-8"))
    ilk_havada = set(u for d in ilk["bilesen"] for u in d["uye"])
    aday = [i for i, (ad, s) in enumerate(L) if ad.startswith(("ELK_", "DUZ_") + DEGISEN) or ad in ilk_havada]
    return L, aday, ilk_havada


if __name__ == "__main__":
    t0 = time.time()
    if sys.argv[1] == "parca":
        K, N = int(sys.argv[2]), int(sys.argv[3])
        L, aday, _ = yukle()
        B = [s.BoundingBox() for ad, s in L]
        kom = {}
        for i in aday[K::N]:
            bi = B[i]; kom[i] = []
            for j in range(len(L)):
                if j == i: continue
                bj = B[j]
                if bj.xmin > bi.xmax + TOL or bi.xmin > bj.xmax + TOL or bj.ymin > bi.ymax + TOL or bi.ymin > bj.ymax + TOL or bj.zmin > bi.zmax + TOL or bi.zmin > bj.zmax + TOL:
                    continue
                try:
                    d = BRepExtrema_DistShapeShape(L[i][1].wrapped, L[j][1].wrapped); ok = d.IsDone() and d.Value() <= TOL
                except Exception:
                    ok = True
                if ok: kom[i].append(j)
        json.dump(dict(n=len(L), kom={str(k): v for k, v in kom.items()}), io.open(os.path.join(H3, "_dunya_tam", "havada_par_%d.json" % K), "w", encoding="utf-8"))
        print("parça %d/%d · %d aday · %.0f sn" % (K, N, len(kom), time.time() - t0))
    else:
        N = int(sys.argv[2])
        idx = json.load(io.open(os.path.join(H3, "_dunya_tam", "dunya.json"), encoding="utf-8"))
        L = [("%s|%s" % (q[0], q[1]),) for q in idx if not q[0].startswith("INSAN")]
        ilk = json.load(io.open(os.path.join(H3, "_dunya", "havada_v1.json"), encoding="utf-8"))
        ilk_havada = set(u for d in ilk["bilesen"] for u in d["uye"])
        aday = [i for i, (ad,) in enumerate(L) if ad.startswith(("ELK_", "DUZ_") + DEGISEN) or ad in ilk_havada]
        kom = {}
        for K in range(N):
            J = json.load(io.open(os.path.join(H3, "_dunya_tam", "havada_par_%d.json" % K), encoding="utf-8"))
            assert J["n"] == len(L), (J["n"], len(L))
            for k, v in J["kom"].items(): kom.setdefault(int(k), set()).update(v)
        assert set(kom) == set(aday), "eksik parça"
        for i, v in list(kom.items()):
            for j in v:
                if j in kom: kom[j].add(i)
        # zemine değen adaylar: dökümden y alt sınırı gerekir → bbox yeniden okunmasın diye parça dosyalarında yok; ilk aday listesi için hızlı yükleme
        import h3_havada_v1 as HV2
        HV2.DD = os.path.join(H3, "_dunya_tam")
        LL = [s for b, a, m, g, s in HV2.yukle() if not b.startswith("INSAN")]
        A = set(aday)
        gor = set(j for j in range(len(L)) if j not in A) | set(i for i in aday if LL[i].BoundingBox().ymin <= TOL)
        degisti = True
        while degisti:
            degisti = False
            for i in aday:
                if i not in gor and kom[i] & gor:
                    gor.add(i); degisti = True
        havada = [L[i][0] for i in aday if i not in gor]
        print("HEDEFLİ HAVADA PARALEL (v3.4): %d parça döküm · %d aday (değişen makine parçaları dahil) · HAVADA %d · %.0f sn" % (len(L), len(aday), len(havada), time.time() - t0))
        for h in havada[:80]: print("   HAVADA:", h)
        json.dump(dict(aday=len(aday), havada=havada), io.open(os.path.join(H3, "_dunya_tam", "havada_hizli_v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    sys.stdout.flush(); os._exit(0)
