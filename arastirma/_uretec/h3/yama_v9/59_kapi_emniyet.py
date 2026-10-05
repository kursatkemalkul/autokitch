# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 59 · KAPI EMNİYET ANAHTARLARI (5 Eki 2026 · Claude · bulut oturumu · Kemal: STANDART_DURUM.md madde 3 "yapalım")
python 59_kapi_emniyet.py girdi.glb cikti.glb      (zincir: hat3_v9z.glb → hat3_v10a.glb)

EN ISO 14119 / 14120: hareketli tehlikeye açılan her ön kapak kilit anahtarlı — açılınca o istasyonun tehlikeli hareketi durur (hava boşalır, sürücüler
güvenli tork kesme), kapanınca kendiliğinden başlamaz. 10 kapak: A · TOPPING K1 / K2 · F sol / sağ üst · K · E üst sol / sağ · alt sol / sağ.
Ürün: Schmersal RSS36 (RFID kodlu emniyet sensörü, IP69K, hijyenik; gövde ≈ 25 × 72 × 18) + RST36 aktüatör (≈ 25 × 72 × 12) — kapak başına 1 çift.
K (Ø296 yıldız bıçak, pnömatik, yerçekimli): KİLİTLİ tip Schmersal AZM40 (gövde ≈ 40 × 120 × 20, bıçak durup hava boşalana kadar kapak açılmaz) + aktüatör.
Ölçüler yaklaşık (katalog teyidi açık · teyit.md'ye girecek).
Yer: her kapağın mandal (bas-aç) tarafında, kapağın arkasında; aktüatör kapağın iç yüzüne (kapakla döner, kpk), sensör gövdeye, aralarında 3 mm.
Yerler model ağında aranarak seçildi (gece2 · yerbul: aktüatör + sensör kutusu boş, sensör bir sabit parçaya ≤ 25 mm); bu betik o yerleri SABİT tablodan kurar.
Sensör gövdesi sabit parçaya değmiyorsa arkasına / yanına 2 mm paslanmaz L braket kurulur (en yakın sabit yüzeye; aradaki hacim boşsa).
Kablo çizilmedi: sensör M12 → istasyon kutusu → güvenlik devresi (Claude + Codex şeması, sonra)."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time()
# ad, istasyon, mek (…/Elektrik ya da Gövde), kapak düğüm eki, aktüatör kutusu (lo, hi), sensör kutusu (lo, hi), tip
YER = [("A", 0, "", ((1372.5, 894.0, 47.0), (1397.5, 966.0, 59.0)), ((1372.5, 894.0, 26.0), (1397.5, 966.0, 44.0)), "RSS36"),
       ("TOPPING_K1", 16, "", ((1892.5, 894.0, 27.0), (1917.5, 966.0, 39.0)), ((1892.5, 894.0, 6.0), (1917.5, 966.0, 24.0)), "RSS36"),
       ("TOPPING_K2", 16, "", ((2016.5, 894.0, 27.0), (2041.5, 966.0, 39.0)), ((2016.5, 894.0, 6.0), (2041.5, 966.0, 24.0)), "RSS36"),
       ("F_SOL", 23, "__KAPAK_F_SOL", ((2519.0, 2137.5, 65.5), (2591.0, 2162.5, 77.5)), ((2519.0, 2137.5, 44.5), (2591.0, 2162.5, 62.5)), "RSS36"),
       ("F_SAG", 23, "__KAPAK_F_SAG", ((3909.0, 2137.5, 65.5), (3981.0, 2162.5, 77.5)), ((3909.0, 2137.5, 44.5), (3981.0, 2162.5, 62.5)), "RSS36"),
       ("K", 30, "", ((4332.5, 924.0, 47.0), (4357.5, 996.0, 59.0)), ((4325.0, 900.0, 24.0), (4365.0, 1020.0, 44.0)), "AZM40"),
       ("E_UST_SOL", 38, "", ((4832.5, 1864.0, 47.0), (4857.5, 1936.0, 59.0)), ((4832.5, 1864.0, 26.0), (4857.5, 1936.0, 44.0)), "RSS36"),
       ("E_UST_SAG", 38, "", ((4882.5, 864.0, 47.0), (4907.5, 936.0, 59.0)), ((4882.5, 864.0, 26.0), (4907.5, 936.0, 44.0)), "RSS36"),
       ("E_ALT_SOL", 38, "", ((4812.5, 164.0, 47.0), (4837.5, 236.0, 59.0)), ((4812.5, 164.0, 26.0), (4837.5, 236.0, 44.0)), "RSS36"),
       ("E_ALT_SAG", 38, "", ((4882.5, 164.0, 47.0), (4907.5, 236.0, 59.0)), ((4882.5, 164.0, 26.0), (4907.5, 236.0, 44.0)), "RSS36")]
BOM = {"RSS36": ("Schmersal RSS36 RFID kodlu emniyet sensörü (IP69K, M12)", "Schmersal RST36-1 aktüatör"),
       "AZM40": ("Schmersal AZM40 kilitli emniyet anahtarı (kapak kilidi, M12)", "Schmersal AZM40 aktüatörü")}
BRAKET_T = 2.0
SINIR = 25.0


def kutu(lo, hi, pay=0.0):
    lo = np.array(lo, float) + pay; hi = np.array(hi, float) - pay
    return cq.Workplane("XY").box(*(hi - lo), centered=False).translate(tuple(lo)).val()


g = Glb(gi)
# sabit (kpk olmayan) üçgenler: braket için en yakın yüzey · kutu boşluk denetimi
MN, MX, KK, AD = [], [], [], []
for p in g.prims:
    if p.get("gizli") or p["pr"].get("mode", 4) != 4: continue
    P = p["X"][p["T"]]
    kp = p["pr"].get("extras", {}).get("kpk", []); kk = np.zeros(len(P), bool)
    for a, n in zip(kp[0::2], kp[1::2]): kk[a // 3:(a + n) // 3] = True
    m = np.all(P.max(1) >= [700, 0, -200], 1) & np.all(P.min(1) <= [5300, 2300, 100], 1)
    MN.append(P[m].min(1)); MX.append(P[m].max(1)); KK.append(kk[m]); AD += [p["name"]] * int(m.sum())
MN = np.concatenate(MN); MX = np.concatenate(MX); KK = np.concatenate(KK); AD = np.array(AD)


def bos(lo, hi, pay=0.3):
    lo = np.array(lo) + pay; hi = np.array(hi) - pay
    return not np.any(np.all(MX > lo, 1) & np.all(MN < hi, 1))


def braket(lo, hi):
    """sensör kutusunun 6 yüzünden en yakın sabit yüzeye boşluk; ≤ 1 mm ise braket yok (doğrudan vidalı)"""
    lo = np.array(lo, float); hi = np.array(hi, float); en = None
    for ax in range(3):
        for sg in (-1, +1):
            o = [i for i in range(3) if i != ax]
            m = ~KK & np.all(MX[:, o] > lo[o] + 2.0, 1) & np.all(MN[:, o] < hi[o] - 2.0, 1)
            if sg > 0: m &= MN[:, ax] >= hi[ax] - 0.3; d = MN[m, ax] - hi[ax] if m.any() else None
            else: m &= MX[:, ax] <= lo[ax] + 0.3; d = lo[ax] - MX[m, ax] if m.any() else None
            if d is None: continue
            k = int(np.argmin(d)); d = max(float(d[k]), 0.0)
            if en is None or d < en[0]: en = (d, ax, sg, AD[m][k])
    return en


P = []; KAYIT = []
for ad, mek, ek, (alo, ahi), (slo, shi), tip in YER:
    assert bos(alo, ahi) and bos(slo, shi), "ADIM 59 DUR: %s kutusu dolu" % ad
    sb, ab = BOM[tip]
    P.append(dict(ad="emniyet_%s_sensor" % ad, sh=kutu(slo, shi), bom=[sb], tur="sensor", mek=mek, ek=ek))
    P.append(dict(ad="emniyet_%s_aktuator" % ad, sh=kutu(alo, ahi), bom=[ab], tur="aktuator", mek=mek, ek=ek))
    d, ax, sg, karsi = braket(slo, shi)
    assert d <= SINIR, "ADIM 59 DUR: %s sensörü sabit parçadan %.1f mm uzak" % (ad, d)
    br = None
    if d > 1.0:
        lo = np.array(slo, float); hi = np.array(shi, float)
        o = [i for i in range(3) if i != ax]
        blo = lo.copy(); bhi = hi.copy()
        for i in o: blo[i] += 2.0; bhi[i] -= 2.0                          # braket yüzü sensörden 2 mm içerde
        if sg > 0: blo[ax], bhi[ax] = hi[ax], hi[ax] + d
        else: blo[ax], bhi[ax] = lo[ax] - d, lo[ax]
        assert bos(blo, bhi), "ADIM 59 DUR: %s braket hacmi dolu" % ad
        P.append(dict(ad="emniyet_%s_braket" % ad, sh=kutu(blo, bhi), bom=["Paslanmaz 304 braket 2 mm (sensör → %s)" % karsi], tur="braket", mek=mek, ek=ek))
        br = [round(float(v), 2) for v in list(blo) + list(bhi)]
    KAYIT.append(dict(kapak=ad, tip=tip, karsi=str(karsi), bosluk=round(d, 2), braket=br))
    SE.log("  %-11s %-5s sensör %s · aktüatör %s · tutunan %s (%.1f mm)%s" % (ad, tip, slo, alo, karsi, d, " · braket" if br else ""))
tmp = go + ".e1.glb"; g.kaydet(tmp); del g
H = SE.Ham(tmp)
DUG = {"sensor": ("EMNIYET__sari", "ELK_ANA_PANO_UF__salter_sari__KAPAK_ANA_PANO"),
       "aktuator": ("EMNIYET__siyah", "K_GOVDE__siyah"),
       "braket": ("EMNIYET__paslanmaz", "U_F_GOVDE__paslanmaz")}
dolu = set(); TUM = {}
for p in P:
    d, sb = DUG[p["tur"]]
    if p["tur"] == "aktuator": d = d + p["ek"]                                # F kapaklarında aktüatör kapak düğümüyle aynı ek
    kpk = p["tur"] == "aktuator"
    H.koy(d, [p], kat=3, mek=p["mek"], kpk_fn=lambda a, k=kpk: k, sablon=sb, ekle=d in dolu)
    dolu.add(d); TUM.setdefault(d, []).append(p)
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f in (tmp, tmp + ".e2.glb"): os.remove(f)
for d in TUM: H.aralik[d] = {p["ad"]: (0, 0) for p in TUM[d]}
SE.ent_json(go[:-4] + "_ent.json", "EMNIYET", [(d, TUM[d]) for d in sorted(TUM)], H.aralik, lambda a: a.endswith("_aktuator"), "Elektrik", (), KAYIT,
            ek=dict(yer=[[a, m, e, list(map(list, ak)), list(map(list, sk)), t] for a, m, e, ak, sk, t in YER]))
SE.log("ADIM 59 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
