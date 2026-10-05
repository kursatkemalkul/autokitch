# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 41 · TOPPING İÇ GEÇİŞLER + QR KABLO ŞERİDİ + B ÖN ÇERÇEVE DERZİ (gece 2 · adım 9 · 4 Eki 2026 · Claude · YEREL)
python 41_gecis_kablo.py girdi.glb cikti.glb      (zincir: hat3_v9h.glb → hat3_v9i.glb)
Kaynak: gece2/adim8/denetim/RAPOR.md (gerçek çakışmalar, hepsi v9f'den beri var). Bileşen numaraları v9h'deki govde_denetim_dogru.bilesenler sırası
(denetimdeki 'DÜĞÜM[no]' ile aynı); yerinde yeniden bulmak için kutu (lo/hi) kullanılır.
G1 · pnömatik piston çubukları (PISTON_SOS / _HARC / _KUSBASI, çubuk Ø11,9) silindir gövdesine (TOPPING_MODUL__aluminyum, Ø37,7 × 139) ve burun
     rakoruna (Ø23,6 × 10) dolu katı olarak giriyordu (10 / 5,75 mm): gövde + burunda çubuk kovanı Ø12,4 (çubuk + 0,25 mm radyal pay, gövde boyunca —
     gerçek silindirde çubuk keçesi / kovanı burada) · çubuk ucundaki bağlantı somunu (PISTON düğümü [1], Ø19,7 × 16) üst çubuk ucunu (8 mm) içine
     alıyordu → somunda çubuk kadar kör dişli yuva (somun − üst çubuk).
     NOT: denetim raporu bu parçaları 'evaporatör kaseti / soğuk iç kaplama' diye adlandırmıştı (parca_kutulari kutu eşlemesi); geometri (Ø37,7 × 139
     alüminyum gövde + Ø23,6 burun + arka kapak, çubuk ekseninde) bunların piston silindiri olduğunu gösteriyor → körük gerekmiyor, kovan yeterli.
G2 · bakır soğutma boruları (TOPPING_MODUL__bakir 11–18): boru uçları dirsek / manşon (rakor) içine dolu katı giriyordu (3–7,8 mm) → rakorda
     boru kadar soket (lehim soketi: rakor − boru) · boru ↔ boru (T birleşimi) → küçük boruda karşı borunun hacmi çıkarılır.
G3 · silikon hortumlar (silikon 8 / 9) ↔ hortum kelepçe bloğu (silikon 10, 16³): blokta hortum yatakları (blok − hortumlar).
G4 · döner valf gövdeleri (TOPPING_DONER__VALF_*[0], kendi ekseni etrafında döner → dönel simetrik) ↔ sabit taşıyıcılar (paslanmaz 24 / 51 / 8,
     aluminyum 12): taşıyıcıda valf kadar yuva + 0,3 mm pay (valf ekseni boyunca büyütülmüş kesici yerine valfin kendisi; dönel simetrik olduğundan
     dönüşte de boşluk korunur).
G5 · diğer TOPPING geçişleri (cıvata / pim ↔ plaka; büyük hacimli parçada küçüğün yuvası): celik 125/126 ↔ paslanmaz 17/33 · paslanmaz 18↔19,
     34↔35 · paslanmaz 56/57 ↔ saydam_celik 3 · paslanmaz 18/34 ↔ pom 1/4.
K1 · QR göz ısıtıcı kablosu ↔ Cat6A ana veri hattı (12 göz, koaksiyel üst üste, 1,34 mm): Cat6A göz çıkışları ayrı şeride → +z 3,5 mm
     (kablo Ø2,9 + 0,6 boşluk; kanal ağzının içinde, ısıtıcı kablosunun üstünde).
P1 · B_KASA ön çerçevesinde (B_KASA__on_cerceve, z 23–24) x ≈ 2090 iki parça arasında 1 mm derz → PU görünüyordu: derze aynı sacdan dolgu şeridi
     (çerçeve parçaları arasında birebir, üst ve alt kuşakta).
Etiketler: kesilen bileşenler kendi etiketini korur (m8kit donustur); yeni şerit B_KASA__on_cerceve düğümünün kat / mek değerini alır."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq
import manifold3d as mf

gi, go = sys.argv[1:3]
t0 = time.time()
LOG = SE.log
g = Glb(gi)


def bil(d, no):
    g.bilesen(d, 0); return g._bc[d][no]


def mesh(b):
    P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
    m = SE.mf_ucgen(P); assert m is not None, "kapalı değil"
    return m


def silz(x, y, z0, z1, r, n=48):
    return mf.Manifold.cylinder(z1 - z0, r, r, n).translate([x, y, z0])


TM = "TOPPING_MODUL__"
# (alıcı düğüm, no, [(kesici düğüm, no) | ('SIL', x, y, z0, z1, r)], pay)
IS = []
for pis, al_g, al_b in (("PISTON_SOS", 1, 2), ("PISTON_HARC", 5, 6), ("PISTON_KUSBASI", 13, 14)):
    pd = TM + "paslanmaz__" + pis
    c = bil(pd, 2); cx, cy = (c["lo"][:2] + c["hi"][:2]) / 2; r = (c["hi"][1] - c["lo"][1]) / 2
    lo_g = bil(TM + "aluminyum", al_g)["lo"][2]; hi_b = bil(TM + "aluminyum", al_b)["hi"][2]
    for no in (al_g, al_b):
        IS.append(("G1", TM + "aluminyum", no, [("SIL", cx, cy, lo_g - 1.0, hi_b + 1.0, r + 0.25)]))
    IS.append(("G1", pd, 1, [(pd, 0)]))
for al, kes in ((18, (17, 16)), (17, (16,)), (13, (14,)), (11, (16,)), (12, (17,)), (15, (14, 13))):
    IS.append(("G2", TM + "bakir", al, [(TM + "bakir", k) for k in kes]))
IS.append(("G3", TM + "silikon", 10, [(TM + "silikon", 8), (TM + "silikon", 9)]))
for al, no, v in (("paslanmaz", 24, "VALF_HARC"), ("paslanmaz", 51, "VALF_KUSBASI"), ("paslanmaz", 8, "VALF_SOS"), ("aluminyum", 12, "VALF_KUSBASI")):
    IS.append(("G4", TM + al, no, [("TOPPING_DONER__" + v, 0, 0.3)]))
for al, kes in ((("paslanmaz", 33), [("celik", 126)]), (("paslanmaz", 17), [("celik", 125)]), (("paslanmaz", 19), [("paslanmaz", 18)]),
                (("paslanmaz", 35), [("paslanmaz", 34)]), (("saydam_celik", 3), [("paslanmaz", 56), ("paslanmaz", 57)]),
                (("paslanmaz", 18), [("pom", 1)]), (("paslanmaz", 34), [("pom", 4)])):
    IS.append(("G5", TM + al[0], al[1], [(TM + k[0], k[1]) for k in kes]))

# kesicileri ve alıcı kutularını ÖNCE (değişiklikten önce) kur
HAZ = []
for kod, d, no, kes in IS:
    b = bil(d, no); M = None
    for k in kes:
        if k[0] == "SIL":
            km = silz(*k[1:])
        else:
            km = mesh(bil(k[0], k[1]))
            if len(k) > 2:                                                       # pay: kesiciyi merkezine göre ölçekle (dönel simetrik valf)
                bb = np.array(km.bounding_box()); c = (bb[:3] + bb[3:]) / 2; s = (bb[3:] - bb[:3])
                f = [(s[i] + 2 * k[2]) / s[i] for i in range(3)]
                km = km.translate((-c).tolist()).scale(f).translate(c.tolist())
        M = km if M is None else M + km
    HAZ.append((kod, d, no, b["lo"].copy(), b["hi"].copy(), mesh(b), M, kes))

KAYIT = []
for kod, d, no, lo, hi, m, M, kes in HAZ:
    g._bc.clear()
    b = g.bilesen(d, lo=lo, hi=hi, tol=0.3)
    m = mesh(b)                                                                  # güncel (önceki kesimlerden etkilenmiş olabilir)
    yeni = m - M
    v0, v1 = m.volume(), yeni.volume()
    if v0 - v1 < 0.01:
        LOG("  %s %s[%d]: kesişim yok (atlandı)" % (kod, d, no)); continue
    Pn = SE.mf_P(yeni); ilk = [True]
    def _f(_, Pn=Pn, ilk=ilk):
        if ilk[0]: ilk[0] = False; return Pn
        return None
    g.donustur(b, _f)
    ks = ", ".join("Ø%.1f kovan" % (2 * k[5]) if k[0] == "SIL" else "%s[%d]" % (k[0].replace(TM, ""), k[1]) for k in kes)
    KAYIT.append(dict(kod=kod, alici="%s[%d]" % (d, no), kesici=ks, hacim_once=round(v0, 1), hacim_sonra=round(v1, 1)))
    LOG("  %s %-44s − %s · −%.1f mm³" % (kod, "%s[%d]" % (d, no), ks, v0 - v1))
g._bc.clear()

# K1 · Cat6A göz çıkışları +z 3,5
d = "ELK_QR_KABLO__kablo_sinyal"
g.bilesen(d, 0)
cat = [(b["lo"].copy(), b["hi"].copy()) for b in g._bc[d] if 30 <= b["no"] <= 41]
assert len(cat) == 12
for lo, hi in cat:
    assert abs((lo[2] + hi[2]) / 2 - 1000.0) < 0.2 and hi[0] - lo[0] > 11.0, (lo, hi)
    g._bc.clear(); b = g.bilesen(d, lo=lo, hi=hi, tol=0.3); g.tasi_b(b, [0.0, 0.0, 3.5])
g._bc.clear()
LOG("K1 Cat6A göz çıkışı 12 parça +z 3,5 (ısıtıcı kablosu şeridinden ayrıldı)")

# P1 · ön çerçeve derzi: x 2085–2096 aralığında çerçeve parçalarının kenarları
d = "B_KASA__on_cerceve"
g.bilesen(d, 0)
SOL = [b for b in g._bc[d] if abs(b["hi"][0] - 2090.4) < 0.6 and b["lo"][2] > 22.5 and b["hi"][2] < 24.5]
SAG = [b for b in g._bc[d] if abs(b["lo"][0] - 2091.4) < 0.6 and b["lo"][2] > 22.5 and b["hi"][2] < 24.5]
SERIT = []
for a in SOL:
    for c in SAG:
        y0 = max(a["lo"][1], c["lo"][1]); y1 = min(a["hi"][1], c["hi"][1])
        if y1 - y0 < 5: continue
        x0, x1 = float(a["hi"][0]), float(c["lo"][0]); z0 = float(max(a["lo"][2], c["lo"][2])); z1 = float(min(a["hi"][2], c["hi"][2]))
        sh = cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0)).val()
        SERIT.append(dict(ad="b_on_cerceve_derz_dolgu_y%.0f" % y0, sh=sh, bom=["ön çerçeve derz dolgu şeridi, çerçeve sacından (304, 1 mm), kaynak + taşlama"], tur="serit"))
        LOG("P1 derz: x %.2f–%.2f · y %.1f–%.1f · z %.1f–%.1f" % (x0, x1, y0, y1, z0, z1))
if not SERIT:
    for b in g._bc[d]:
        if b["lo"][0] < 2096 and b["hi"][0] > 2085: LOG("  çerçeve bileşeni %d %s %s" % (b["no"], b["lo"].round(2), b["hi"].round(2)))
    LOG("UYARI P1: derz kenarları bulunamadı")
g._bc.clear()

tmp = go + ".e1.glb"; g.kaydet(tmp); del g
H = SE.Ham(tmp)
YENI = {}
if SERIT:
    kat, mek = H.etiket(d)
    H.koy(d, SERIT, kat=kat, mek=mek, ekle=True)
    YENI[d] = SERIT
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
SE.ent_json(go[:-4] + "_ent.json", "GECIS", [(k, YENI[k]) for k in sorted(YENI)], H.aralik, lambda a: False, "B", (), KAYIT,
            ek=dict(k1="ELK_QR_KABLO__kablo_sinyal[30..41] +z 3.5"))
LOG("ADIM 41 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
