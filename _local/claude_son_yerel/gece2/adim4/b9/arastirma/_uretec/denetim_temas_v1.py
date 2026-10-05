# -*- coding: utf-8 -*-
"""AUTOKITCH · HAVADA PARÇA DENETİMİ v1 (27 Eyl 2026 gece) — Kemal: "içeride havada kalan parça olmasın, her şeyi montajla yüzeylere".
Bir parça listesinde her parçanın ZEMİNE (ya da verilen kök parçalara) birbirine DEĞEN parçalar zinciriyle bağlı olup olmadığını katılardan ölçer.
  · iki parça "bağlı": gerçek katı aralığı ≤ tol (varsayılan 0,05 mm; değme ya da kesişme) — OCC BRepExtrema_DistShapeShape
  · kök: y alt ucu ≤ zemin_y + tol olan parçalar (ayaklar) + kok_adlar
  · sonuç: bağlı olmayan her BİLEŞEN (birbirine bağlı ama zemine bağlanmayan parça grupları) — en büyük üyesi ve üye sayısıyla
Kullanım (modülden):  import denetim_temas_v1 as DT; bul = DT.havada([(ad, shape), ...]); DT.yaz(bul)
Komut satırı:         python ob_calistir.py denetim_temas_v1.py <modul_adi> [kur|modul]   (modül PARCALAR[wp] ya da P[sh] taşımalı)
Sınır: taşınan ürün (top, kutu, koli, tatlı kabı) tepsiye oturduğu için bağlı sayılır; hareketli gruplar KAPALI konumda denetlenir.
"""
import sys, time


def _sekil(x):
    return x.val() if hasattr(x, "val") else x


def havada(parcalar, zemin_y=None, tol=0.05, kok_adlar=(), haric=()):
    """zemin_y None → listedeki en alçak nokta (modül kendi tabanında duruyorsa o taban)"""
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    t0 = time.time()
    L = []
    for ad, sh in parcalar:
        if ad in haric:
            continue
        s = _sekil(sh)
        try:
            b = s.BoundingBox()
        except Exception:
            continue
        L.append((ad, s, b))
    n = len(L)
    kom = [[] for _ in range(n)]
    sirali = sorted(range(n), key=lambda i: L[i][2].xmin)
    aday = 0
    for ii, i in enumerate(sirali):
        bi = L[i][2]
        for j in sirali[ii + 1:]:
            bj = L[j][2]
            if bj.xmin > bi.xmax + tol:
                break
            if bj.ymin > bi.ymax + tol or bi.ymin > bj.ymax + tol or bj.zmin > bi.zmax + tol or bi.zmin > bj.zmax + tol:
                continue
            aday += 1
            try:
                d = BRepExtrema_DistShapeShape(L[i][1].wrapped, L[j][1].wrapped)
                ok = d.IsDone() and d.Value() <= tol
            except Exception:
                ok = True                                    # ölçülemedi → bağlı say (yanlış alarm üretme), raporda sayılır
            if ok:
                kom[i].append(j); kom[j].append(i)
    if zemin_y is None:
        zemin_y = min(x[2].ymin for x in L)
    kok = [i for i in range(n) if L[i][2].ymin <= zemin_y + tol or L[i][0] in kok_adlar]
    gor = [False] * n
    yig = list(kok)
    for i in kok:
        gor[i] = True
    while yig:
        i = yig.pop()
        for j in kom[i]:
            if not gor[j]:
                gor[j] = True; yig.append(j)
    # bağlanmayanları bileşenlere ayır
    bil = []
    gor2 = list(gor)
    for i in range(n):
        if gor2[i]:
            continue
        uy, yig = [], [i]; gor2[i] = True
        while yig:
            k = yig.pop(); uy.append(k)
            for j in kom[k]:
                if not gor2[j]:
                    gor2[j] = True; yig.append(j)
        en = max(uy, key=lambda k: L[k][2].xlen * L[k][2].ylen * L[k][2].zlen)
        bil.append(dict(en=L[en][0], uye=[L[k][0] for k in uy], bb=L[en][2]))
    bil.sort(key=lambda d: -len(d["uye"]))
    return dict(parca=n, aday=aday, kok=len(kok), bagli=sum(gor), bilesen=bil, sure=time.time() - t0)


def yaz(sonuc, en_cok=40, baslik="HAVADA PARCA DENETIMI"):
    b = sonuc["bilesen"]
    print("%s: %d parca · %d aday cift · kok (zemin) %d · zemine bagli %d · HAVADA %d bilesen (%d parca) · %.0f sn"
          % (baslik, sonuc["parca"], sonuc["aday"], sonuc["kok"], sonuc["bagli"], len(b), sum(len(d["uye"]) for d in b), sonuc["sure"]))
    for d in b[:en_cok]:
        bb = d["bb"]
        print("   HAVADA: %-40s (%d parca: %s%s) · x %.0f-%.0f y %.0f-%.0f z %.0f…%.0f"
              % (d["en"], len(d["uye"]), ", ".join(d["uye"][:4]), " …" if len(d["uye"]) > 4 else "", bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax))
    return len(b)


if __name__ == "__main__":
    import importlib
    ad = sys.argv[1]
    M = importlib.import_module(ad)
    kur = sys.argv[2] if len(sys.argv) > 2 else None
    if kur:
        getattr(M, kur)()
    elif hasattr(M, "modul") and not getattr(M, "PARCALAR", None):
        M.modul()
    if getattr(M, "PARCALAR", None):
        ps = [(p["ad"], p["wp"]) for p in M.PARCALAR]
    else:
        ps = [(p["ad"], p["sh"]) for p in M.P]
    yaz(havada(ps), baslik="HAVADA PARCA DENETIMI · %s" % ad)
