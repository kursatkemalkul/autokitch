# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 40 · ACİL STOP BUTONLARI (gece 2 · adım 8 · 4 Eki 2026 · Claude · YEREL)
python 40_acil_stop.py girdi.glb cikti.glb      (zincir: hat3_v9g.glb → hat3_v9h.glb)
EN 60204-1 10.7 / EN ISO 13850: makinede acil stop yoktu. Her istasyona 1 (A hariç — A elektriksiz; QR'da müşteri yüzüne değil, robot / servis yüzüne).
Ürün: Schneider Electric Harmony XB4BS8442 (Ø40 kırmızı mantar, çevirerek bırakma, 1 NC) + ZBY9330T sarı etiket diski Ø60.
Model: etiket diski Ø60 × 1 · bilezik Ø29 × 10 · mantar Ø40 × 16 (kenar R4) ön yüzde; gövde + kontak bloğu 30 × 30 × 43 kapağın arkasında
(kapak sacında / camında Ø22,5 delik yerine gövde kadar cep açılır — delik_ac). Makinenin ön yüzünde sabit (açılmayan) yüz yok: bütün ön yüz kapak / çekmece
önü → butonlar KAPAĞIN üstünde (kpk = kapakla gelir); kablo menteşe tarafından esnek döngüyle istasyon iç kanalına → istasyon kutusu → güç fişinin
sinyal kontakları (mevcut E-stop zinciri). Kablo modelde ÇİZİLMEDİ (rapor: açık).
Yükseklikler (mantar merkezi): TOPPING 1,00 · B 0,75 · F 1,46 · K 1,40 · E 1,30 · QR 1,69 m (0,6–1,7 m)."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time()
# istasyon, x, y, ön yüz z, normal (+1 / −1), mek (liste indeksi: …/Elektrik), taşıyan kapak
YER = [("TOPPING", 2440.0, 1000.0, 79.0, +1, 15, "TOPPING ön kapağı (mekanizma kanadı)"),
       ("B", 4300.0, 750.0, 79.0, +1, 5, "B depo çekmecesi PU önü (B'nin önünde sabit yüz yok; x ≤ 4330: çekmece açılınca QR'a çarpmaz)"),
       ("F", 2600.0, 1460.0, 79.0, +1, 22, "F üst sol kapağı"),
       ("K", 4300.0, 1400.0, 79.0, +1, 29, "K ön kapağı"),
       ("E", 5150.0, 1300.0, 79.0, +1, 37, "E sağ üst kapağı"),
       ("QR", 5100.0, 1690.0, 670.0, -1, 46, "QR robot yüzü üst servis kapağı")]


def silz(x, y, z0, z1, r):
    a, b = min(z0, z1), max(z0, z1)
    return cq.Solid.makeCylinder(r, b - a, cq.Vector(x, y, a), cq.Vector(0, 0, 1))


def parca(ist, x, y, z0, n):
    z = lambda t: z0 + n * t
    etk = silz(x, y, z(0), z(1.0), 30.0)
    bil = silz(x, y, z(1.0), z(11.0), 14.5)
    man = silz(x, y, z(11.0), z(27.0), 20.0)
    try:
        man = cq.Workplane().add(man).faces(">Z" if n > 0 else "<Z").edges().fillet(4.0).val()
    except Exception:
        pass
    a, b = sorted((z(0), z(-43.0)))
    gov = cq.Workplane("XY").box(30, 30, b - a, centered=False).translate((x - 15, y - 15, a)).val()
    return [dict(ad="acil_stop_%s_etiket" % ist, sh=etk, bom=["Schneider ZBY9330T sarı etiket diski Ø60"], tur="etiket"),
            dict(ad="acil_stop_%s_bilezik" % ist, sh=bil, bom=["Schneider XB4 bilezik (XB4BS8442 gövdesi)"], tur="bilezik"),
            dict(ad="acil_stop_%s_mantar" % ist, sh=man, bom=["Schneider Harmony XB4BS8442 Ø40 acil stop mantarı, çevirerek bırakma, 1 NC"], tur="mantar"),
            dict(ad="acil_stop_%s_govde" % ist, sh=gov, bom=["Schneider ZB4BZ102 gövde + kontak bloğu (panel arkası ≈ 43 mm)"], tur="govde")]


P = {ist: parca(ist, x, y, z0, n) for ist, x, y, z0, n, mek, _ in YER}
g = Glb(gi)
K = SE.Karsi(g, acik_dene=True)
kayit = K.delik_ac([p for L in P.values() for p in L if p["tur"] == "govde"])     # kapak sacı / camı / PU'da gövde cebi
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K
H = SE.Ham(tmp)
DUG = {"etiket": ("ACIL_STOP__sari", "ELK_DUVAR__salter_sari"), "bilezik": ("ACIL_STOP__siyah", "K_GOVDE__siyah"),
       "govde": ("ACIL_STOP__siyah", "K_GOVDE__siyah"), "mantar": ("ACIL_STOP__kirmizi", "ELK_DUVAR__salter_kirmizi")}
dolu = set(); TUM = {}
for ist, x, y, z0, n, mek, kapak in YER:
    for tur in ("etiket", "bilezik", "govde", "mantar"):
        d, sb = DUG[tur]
        L = [p for p in P[ist] if p["tur"] == tur]
        H.koy(d, L, kat=6, mek=mek, kpk_fn=lambda a: True, sablon=sb, ekle=d in dolu)
        dolu.add(d); TUM.setdefault(d, []).extend(L)
    SE.log("  %s: (%.0f, %.0f) · %s" % (ist, x, y, kapak))
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
# ent json: aralıklar düğüm başına birikir (Ham.aralik son çağrıyı tutar) → parça kutuları yeterli
for d in TUM: H.aralik[d] = {p["ad"]: (0, 0) for p in TUM[d]}
SE.ent_json(go[:-4] + "_ent.json", "ACIL_STOP", [(d, TUM[d]) for d in sorted(TUM)], H.aralik, lambda a: True, "Elektrik", (), kayit,
            ek=dict(yer=[list(v) for v in YER]))
SE.log("ADIM 40 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
