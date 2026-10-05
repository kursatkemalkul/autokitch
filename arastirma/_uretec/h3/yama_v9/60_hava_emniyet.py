# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 60 · HAVA HATTI EMNİYET VALFİ (5 Eki 2026 · Claude · bulut oturumu · STANDART_DURUM.md madde 8, Kemal: "yapalım")
python 60_hava_emniyet.py girdi.glb cikti.glb      (zincir: hat3_v10a.glb → hat3_v10b.glb)

EN ISO 4414 + EN ISO 13849-1: enerji kesilince / acil stopta / kapı açılınca hattaki hava BOŞALIR, yeniden verilince YUMUŞAK dolar (beklenmedik hareket yok).
Bütün istasyonların havası kompresör (JUN-AIR OF302-15B, F üst kabin) çıkışından tek hortumla (HAVA_KOMPRESOR__hava_ana, x 3544–3554 · y 1804–1814,
z −740…−437) gider → emniyet valfi bu hortumun düz bölümüne, kompresör çıkış rakoru grubunun arkasına girer: z −700…−610.
Ürün: Festo MS6-SV-E (emniyetli yumuşak başlatma + hızlı boşaltma valfi, PL d / kat. 4'e uygun iki kanallı; gövde ≈ 62 × 62 × 90, bobin + M12 −x yüzünde ≈ 18 × 40 × 40)
+ susturucu (+y yüzünde Ø25 × 15 — tavana 20 mm). Ölçüler yaklaşık (katalog teyidi açık).
Bakım kilitleme: ana şalter (OHYS2AJ, 3 asma kilit) kilitlenince valf boşaltır, kompresör durur; kompresör TANKI (15 L) ayrı: kendi tahliye musluğuyla
boşaltılır (kılavuz). Hortumun bu bölümü iki parçaya bölünür (kesit aynı: −740…−700 ve −610…−437; uçlar valf gövdesine dayanır).
Denetim (bu betikte): hortum bileşeni tek ve beklenen kutuda · valf / bobin / susturucu hacmi boş."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
HORTUM = ("HAVA_KOMPRESOR__hava_ana", (3544.0, 1804.0, -740.0), (3554.0, 1814.0, -437.0))
Z0, Z1 = -700.0, -610.0                                                    # valf gövdesi z aralığı
CX, CY = 3549.0, 1809.0                                                    # hortum ekseni
GOVDE = ((CX - 31.0, CY - 31.0, Z0), (CX + 31.0, CY + 31.0, Z1))
BOBIN = ((CX - 31.0 - 18.0, CY - 20.0, -675.0), (CX - 31.0, CY + 20.0, -635.0))
SUS = ((CX, CY + 31.0, -655.0), (CX, CY + 46.0, -655.0), 12.5)            # susturucu silindiri (p0, p1, r)


def kutu(lo, hi):
    lo = np.array(lo, float); hi = np.array(hi, float)
    return cq.Workplane("XY").box(*(hi - lo), centered=False).translate(tuple(lo)).val()


g = Glb(gi)
b = g.bilesen(HORTUM[0], lo=np.array(HORTUM[1]), hi=np.array(HORTUM[2]), tol=0.3)
P0 = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
zs = np.unique(np.round(P0[:, :, 2], 3))
assert set(zs.tolist()) == {-740.0, -437.0}, "ADIM 60 DUR: hortum köşeleri yalnız iki uçta değil %s" % zs
LOG("hortum: %d üçgen · uçlar z %s" % (len(P0), zs.tolist()))

# boşluk denetimi (hortum hariç)
MN, MX, AD = [], [], []
for p in g.prims:
    if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
    P = p["X"][p["T"]]; m = np.all(P.max(1) >= [3400, 1700, -800], 1) & np.all(P.min(1) <= [3700, 1900, -500], 1)
    if p["name"] == HORTUM[0]: m &= ~(np.all(P[:, :, 0] >= 3543.9, 1) & np.all(P[:, :, 0] <= 3554.1, 1) & np.all(P[:, :, 1] >= 1803.9, 1) & np.all(P[:, :, 1] <= 1814.1, 1))
    MN.append(P[m].min(1)); MX.append(P[m].max(1)); AD += [p["name"]] * int(m.sum())
MN = np.concatenate(MN); MX = np.concatenate(MX)
def bos(lo, hi, pay=0.3):
    lo = np.array(lo) + pay; hi = np.array(hi) - pay
    return not np.any(np.all(MX > lo, 1) & np.all(MN < hi, 1))
sl = np.array(SUS[0]) - [SUS[2], 0, SUS[2]]; sh = np.array(SUS[1]) + [SUS[2], 0, SUS[2]]
for ad, (lo, hi) in (("gövde", GOVDE), ("bobin", BOBIN), ("susturucu", (sl, sh))):
    assert bos(lo, hi), "ADIM 60 DUR: %s hacmi dolu" % ad


def bol(P):
    Z = P[:, :, 2]
    A = P.copy(); A[:, :, 2] = np.where(np.abs(Z - (-437.0)) < 1e-3, Z0, Z)      # −740 … −700
    B = P.copy(); B[:, :, 2] = np.where(np.abs(Z - (-740.0)) < 1e-3, Z1, Z)      # −610 … −437
    return np.concatenate([A, B])


n = g.donustur(b, bol)
LOG("hortum iki parça: %d üçgen" % n)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g
H = SE.Ham(tmp)
sus = cq.Solid.makeCylinder(SUS[2], SUS[1][1] - SUS[0][1], cq.Vector(*SUS[0]), cq.Vector(0, 1, 0))
PAR = [("HAVA_EMNIYET__aluminyum", "E_KOSE__aluminyum__CNR_LIFT", dict(ad="hava_emniyet_valfi_govde", sh=kutu(*GOVDE),
                                                                        bom=["Festo MS6-SV-E emniyetli yumuşak başlatma + boşaltma valfi (PL d)"])),
       ("HAVA_EMNIYET__siyah", "K_GOVDE__siyah", dict(ad="hava_emniyet_valfi_bobin", sh=kutu(*BOBIN), bom=["MS6-SV-E bobin + M12 soket (24 V DC, güvenlik devresi)"])),
       ("HAVA_EMNIYET__siyah", "K_GOVDE__siyah", dict(ad="hava_emniyet_valfi_susturucu", sh=sus, bom=["Festo U-1/2 susturucu (boşaltma çıkışı)"]))]
dolu = set(); TUM = {}
for d, sb, p in PAR:
    H.koy(d, [p], kat=4, mek=24, sablon=sb, ekle=d in dolu)                # kat 4 Hava · mek 24 F/Hava
    dolu.add(d); TUM.setdefault(d, []).append(p)
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
for d in TUM: H.aralik[d] = {p["ad"]: (0, 0) for p in TUM[d]}
SE.ent_json(go[:-4] + "_ent.json", "HAVA_EMNIYET", [(d, TUM[d]) for d in sorted(TUM)], H.aralik, lambda a: False, "F/Hava", (), [],
            ek=dict(govde=GOVDE, bobin=BOBIN, hortum_kesik=[Z0, Z1]))
LOG("ADIM 60 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
