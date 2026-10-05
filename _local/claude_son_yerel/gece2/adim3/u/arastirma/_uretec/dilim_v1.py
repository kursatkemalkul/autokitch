# -*- coding: utf-8 -*-
"""AUTOKITCH · DİLİM ÇIKARMA yardımcısı v1 (27 Eyl 2026) — ALÇAK HAT (montaj v57, SPEC_alcak_hat_v57.md): "her şey 168 mm aşağı".

Bir istasyon üretecinin parçalarından yatay bir DİLİM [Yc, Yc + DY] çıkarır (DY = 168):
  · parça tamamen bandın ALTINDA (ymax ≤ Yc)            → yerinde kalır
  · parça tamamen bandın ÜSTÜNDE (ymin ≥ Yc + DY)       → (0, −DY, 0) taşınır
  · parça bandı BOYDAN BOYA geçer (ymin < Yc, ymax > Yc + DY) → (parça ∩ Yc altı) ∪ (parça ∩ Yc + DY üstü) − DY
      ŞART: bandın içinde kesiti SABİT olmalı (dikey prizma: sac, dikme, kanal, vida, yığın). Ölçülür: 1 mm'lik dilim hacmi bandın
      altında / ortasında / üstünde eşit ve bant hacmi = DY × kesit. Değilse HATA (katalog deliği olan ray gibi parçalar yalnız
      `prizma_haric` ile geçer ve üreteçte katalogdan yeniden kurulur).
  · parça bandın İÇİNDE biter (ymin ya da ymax bandın içinde) → HATA: başka bant seçilir, nedeni üreteçte yazılır.

Kullanım (kesme_cad_v4 · kutu_cad_v5): yeni üreteç parçaları DOĞRUDAN yeni kotlarda kurar (sabitler yeniden bağlandı); bu modül
önceki sürümün parçalarını dilimleyip BİREBİR karşılaştırır → yeni kotların hiçbiri elle kaydırılırken kaçmadı (ölçülür)."""
import cadquery as cq

TOL = 1e-3            # sınıflandırma payı (mm)
BUYUK = 1.0e5


def sekil(p, anahtar="wp"):
    w = p[anahtar]
    return w.val() if hasattr(w, "val") else w


def _kutu(bb, y0, y1):
    return cq.Solid.makeBox(bb.xlen + 20.0, y1 - y0, bb.zlen + 20.0, cq.Vector(bb.xmin - 10.0, y0, bb.zmin - 10.0))


def _hacim(sh, bb, y0, y1):
    if y1 <= y0:
        return 0.0
    try:
        return sh.intersect(_kutu(bb, y0, y1)).Volume()
    except Exception:
        return float("nan")


def sinif(sh, Yc, DY):
    b = sh.BoundingBox()
    if b.ymax <= Yc + TOL:
        return "ALT"
    if b.ymin >= Yc + DY - TOL:
        return "UST"
    if b.ymin < Yc - TOL and b.ymax > Yc + DY + TOL:
        return "GECEN"
    return "BANTTA_BITER"


def prizma(sh, Yc, DY):
    """bant içinde kesit sabit mi → (evet/hayır, kesit alt, kesit orta, kesit üst, bant hacmi)"""
    b = sh.BoundingBox()
    a0 = _hacim(sh, b, Yc, Yc + 1.0)
    am = _hacim(sh, b, Yc + DY / 2.0 - 0.5, Yc + DY / 2.0 + 0.5)
    a1 = _hacim(sh, b, Yc + DY - 1.0, Yc + DY)
    vb = _hacim(sh, b, Yc, Yc + DY)
    pay = max(0.5, 1e-3 * max(abs(am), 1.0))
    ok = abs(a0 - am) <= pay and abs(a1 - am) <= pay and abs(vb - DY * am) <= max(1.0, 2e-3 * abs(vb))
    return ok, a0, am, a1, vb


def kes(sh, Yc, DY):
    """(sh ∩ Yc altı) ∪ (sh ∩ Yc + DY üstü) − DY"""
    b = sh.BoundingBox()
    alt = sh.intersect(_kutu(b, b.ymin - 1.0, Yc))
    ust = sh.intersect(_kutu(b, Yc + DY, b.ymax + 1.0)).translate(cq.Vector(0.0, -DY, 0.0))
    return alt.fuse(ust).clean()


def dilimle(parcalar, Yc, DY=168.0, anahtar="wp", prizma_haric=(), atla=()):
    """parça listesini dilimler → (yeni liste [dict kopyası, wp yeni], rapor {ALT, UST, GECEN: [ad]})
    prizma_haric: bandı geçen ama kesiti sabit OLMAYAN, üreteçte yeniden kurulan parçalar (ad önekleri) · atla: listeye alınmayanlar"""
    out, rapor, hata = [], {"ALT": [], "UST": [], "GECEN": []}, []
    for p in parcalar:
        if p["ad"].startswith(tuple(atla)) if atla else False:
            continue
        sh = sekil(p, anahtar)
        s = sinif(sh, Yc, DY)
        b = sh.BoundingBox()
        if s == "BANTTA_BITER":
            hata.append("%s y %.1f–%.1f bant %.0f–%.0f içinde bitiyor" % (p["ad"], b.ymin, b.ymax, Yc, Yc + DY))
            continue
        if s == "ALT":
            yeni = sh
        elif s == "UST":
            yeni = sh.translate(cq.Vector(0.0, -DY, 0.0))
        else:
            ok, a0, am, a1, vb = prizma(sh, Yc, DY)
            if not ok and not p["ad"].startswith(tuple(prizma_haric) if prizma_haric else ("\x00",)):
                hata.append("%s bantta kesiti değişiyor (1 mm dilim %.1f / %.1f / %.1f mm³ · bant %.0f ≠ %.0f)" % (p["ad"], a0, am, a1, vb, DY * am))
                continue
            yeni = kes(sh, Yc, DY)
            v0, v1 = sh.Volume(), yeni.Volume()
            if abs(v0 - vb - v1) > max(1.0, 1e-3 * v0):
                hata.append("%s dilim hacmi tutmuyor: %.0f − %.0f ≠ %.0f" % (p["ad"], v0, vb, v1))
                continue
        q = dict(p)
        q[anahtar] = cq.Workplane(obj=yeni)
        out.append(q)
        rapor[s].append(p["ad"])
    if hata:
        raise ValueError("DİLİM HATASI (bant %.0f–%.0f): " % (Yc, Yc + DY) + " | ".join(hata))
    return out, rapor


def _anahtarla(parcalar):
    say, d = {}, {}
    for p in parcalar:
        n = say.get(p["ad"], 0); say[p["ad"]] = n + 1
        d[(p["ad"], n)] = p
    return d


def karsilastir(yeni, ref, anahtar="wp", yalniz_zarf=(), tol=0.01):
    """yeni üreteç parçaları ↔ dilimlenmiş önceki sürüm: ad ad sınır kutusu (±tol mm) + hacim (±%0,01 ya da 0,5 mm³).
    yalniz_zarf: yalnız sınır kutusu karşılaştırılan (katalogdan yeniden kurulan) ad önekleri.
    → dict(ayni=[ad], fark=[metin], yeni_ek=[ad], ref_eksik=[ad])"""
    A, B = _anahtarla(yeni), _anahtarla(ref)
    ayni, fark = [], []
    for k in A:
        if k not in B:
            continue
        sa, sb = sekil(A[k], anahtar), sekil(B[k], anahtar)
        ba, bb = sa.BoundingBox(), sb.BoundingBox()
        da = max(abs(ba.xmin - bb.xmin), abs(ba.xmax - bb.xmax), abs(ba.ymin - bb.ymin), abs(ba.ymax - bb.ymax), abs(ba.zmin - bb.zmin), abs(ba.zmax - bb.zmax))
        if da > tol:
            fark.append("%s: sınır kutusu %.2f mm farklı (y %.1f–%.1f ≠ ref %.1f–%.1f)" % (k[0], da, ba.ymin, ba.ymax, bb.ymin, bb.ymax))
            continue
        if not k[0].startswith(tuple(yalniz_zarf) if yalniz_zarf else ("\x00",)):
            va, vb = sa.Volume(), sb.Volume()
            if abs(va - vb) > max(0.5, 1e-4 * abs(vb)):
                fark.append("%s: hacim %.1f ≠ ref %.1f mm³" % (k[0], va, vb))
                continue
        ayni.append(k[0])
    return dict(ayni=ayni, fark=fark, yeni_ek=[k[0] for k in A if k not in B], ref_eksik=[k[0] for k in B if k not in A])
