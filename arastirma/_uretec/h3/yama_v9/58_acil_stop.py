# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 58 · TEK ACİL STOP — ŞALTERİN ÖNÜNDEKİ KAPAKTA (5 Eki 2026 · Claude · bulut oturumu)
python 58_acil_stop.py girdi.glb cikti.glb      (zincir: hat3_v9y.glb → hat3_v9z.glb)
Kemal (5 Eki): "tek bir acil butonu, o da şalterin önündeki kapakta" · "küçük olsun". Adım 45'te 6 buton kaldırılmıştı; bu adım TEK buton koyar.
Ana şalter (ABB OT40 + OHYS2AJ kolu) U_F ana pano kapağında x 3590–3782, y 2070–2147, z −91…−53. Önündeki kapak = F sağ üst kapağı (KAPAK_F_SAG:
x 3251,5–4000 · y 1308–2197 · z 59–79 · altta menteşeli, gazlı yaylı). Buton bu kapakta, panjur yarıkları (y 1405–1434 / 1810–1839) ve
omegalar (x 3493,5–3509,5 / 3742–3758, y 1445–1795) arasında: merkez (3625, 1600) → yerden 1,60 m (EN 60204-1 / EN ISO 13850 erişilebilir; 0,6–1,7 m).
Kapak arkası z 16–77,5 bu noktada BOŞ (yalnız kapak ön sacı) — denetlendi.
Ürün: Schneider Electric Harmony XB4BS8442 (Ø40 kırmızı mantar — acil stopun yaygın en küçük boyu, çevirerek bırakma, 1 NC) + ZBY9330T sarı etiket diski Ø60.
Model (adım 40 ile aynı): etiket Ø60 × 1 · bilezik Ø29 × 10 · mantar Ø40 × 16 (R4) ön yüzde; gövde + kontak bloğu 30 × 30 × 43 kapağın arkasında
(kapak sacında gövde kadar cep — delik_ac; Ø60 etiket cebi önden örter). Parçalar kapakla döner (kpk) · düğümler __KAPAK_F_SAG ekli.
Kablo menteşe tarafından esnek döngüyle F iç kanalına → F kutusu → güvenlik devresi (şema Claude + Codex, sonra). Kablo modelde ÇİZİLMEDİ."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time()
# istasyon, x, y, ön yüz z, normal (+1 / −1), mek (liste indeksi: …/Elektrik), taşıyan kapak
YER = [("F", 3625.0, 1600.0, 79.0, +1, 23, "F sağ üst kapağı (KAPAK_F_SAG) — ana şalterin önündeki kapak")]     # mek 23 = F/Elektrik


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
DUG = {"etiket": ("ACIL_STOP__sari__KAPAK_F_SAG", "ELK_ANA_PANO_UF__salter_sari__KAPAK_ANA_PANO"), "bilezik": ("ACIL_STOP__siyah__KAPAK_F_SAG", "K_GOVDE__siyah"),
       "govde": ("ACIL_STOP__siyah__KAPAK_F_SAG", "K_GOVDE__siyah"), "mantar": ("ACIL_STOP__kirmizi__KAPAK_F_SAG", "ELK_ANA_PANO_UF__salter_kirmizi__KAPAK_ANA_PANO")}
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
SE.log("ADIM 58 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
