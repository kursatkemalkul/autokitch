# -*- coding: utf-8 -*-
"""MADDE 6 (91.png) · kapaklar gizliyken govdenin onunde havada kalan kucuk kare bloklar.
91.png: B sogutma bolmesi (x 4012–4400, y 126–453) sokulebilir panelinin 4 PANEL KLIPSI (tk_panel_klipsi_0…3, 16–27 × 20 × 21 mm,
z 24–45: on cerceveden (z 24) panelin icine (z 39–45) uzanir). Klips = panelin arkasindaki erkek gecme; panelle takilir/sokulur →
KAPAGA AIT → kpk etiketi (panelle gizlenir; "yalniz kapaklar" gorunumunde panelle gorunur).
TUM HAT TARAMASI (_kapak_tara.py + _havada_tara.py): ayni sorunlu digerleri — hepsi kapak mekanizmasi dugumunde ama kpk'siz:
  · QR goz kapilari musteri tarafi: QR_GOZLER__celik__GOZ_xx_KAPI (12 adet kapi mandali/kulp, z 1170–1176, kapinin arkasinda)
  · QR goz kapaklari robot tarafi: QR_GOZLER__celik__GOZ_xx_KAPAK (11 adet kapak menteşe seridi) + QR_DONER__GOZ_20_KAPAK (göz 20 kapak paneli)
  · ana pano kapagi kilidi: ELK_ANA_PANO_UF__cihaz_koyu__KAPAK_ANA_PANO
  hepsi kapakla birlikte hareket eden dugumler → kpk.
Govdedeki menteşe tabanlari / bas-ac govde yarilari zaten cerceveye gomulu (dokunulmadi).
Kullanim: python m6_kapak_parcalari_kpk.py giris.glb cikis.glb"""
import sys, re, numpy as np
sys.path.insert(0, r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\b4\51b\gece")
import glbkit

gi, go = sys.argv[1:3]
G = glbkit.Glb(gi)


def kpk_ekle(p, m):
    """ucgen maskesini kpk araliklarina ekle (ardisik kosular)"""
    ex = p["pr"].setdefault("extras", {}); k = list(ex.get("kpk") or [])
    eski = G.kpk_maske(p); m = m & ~eski
    idx = np.where(m)[0]
    if not len(idx): return 0
    br = np.where(np.diff(idx) > 1)[0]
    bas = np.r_[idx[0], idx[br + 1]]; son = np.r_[idx[br], idx[-1]]
    for a, b in zip(bas, son): k += [int(a * 3), int((b - a + 1) * 3)]
    ex["kpk"] = k; return int(m.sum())


p = G.bul("B_SOGUTMA__celik"); tl, kut = G.komp(p)
s = [i for i, (a, b, n) in kut.items() if a[2] >= 23.9 and b[2] <= 45.1 and (b - a).max() < 30 and ((4013.9 <= a[0] and b[0] <= 4030.1) or (4371.4 <= a[0] and b[0] <= 4398.6)) and a[1] >= 189.9 and b[1] <= 410.1]
print("  B_SOGUTMA panel klipsi", len(s), "· kpk +", kpk_ekle(p, np.isin(tl, s) & G.gorunur(p)))
for pr in G.prims:
    if re.match(r"^QR_GOZLER__celik__GOZ_\d\d_(KAPI|KAPAK)$", pr["name"]) or pr["name"] in ("QR_DONER__GOZ_20_KAPAK", "ELK_ANA_PANO_UF__cihaz_koyu__KAPAK_ANA_PANO"):
        print("  %-46s kpk + %d" % (pr["name"], kpk_ekle(pr, G.gorunur(pr))))
G.kaydet(go); print("yazildi", go)
