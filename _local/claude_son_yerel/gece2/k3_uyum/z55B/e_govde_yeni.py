# -*- coding: utf-8 -*-
"""E (KUTU KATLAMA) İSTASYONU GÖVDESİ — BAŞTAN, DÜZGÜN, TEMİZ (Kemal 2 Eki: "katlama kutu dolabını da yap, düzgün temiz"; A / B / TOPPING / U ile aynı ölçüt).
Taban hat3_v8p.glb → hat3_v8r.glb. Montaj / elektrik ÇALIŞTIRILMAZ: E_GOVDE__* düğümlerinin geometrisi baştan kurulup yerine yazılır
('kat' / 'mek' aynı değerle tüm aralık · 'kpk' = kapak görünümüne giren parçalar: kapaklar + menteşe + bas-aç + şarjör yan kapısı).
DÜNYA koordinatı (mm): x hat boyunca (E yereli + 4400) · y yukarı · z koridora (ön +79, arka −830).

ESKİ GÖVDEDE BULUNAN SORUNLAR (v8p)
  1 Kapak menteşeleri (12) tümüyle saydam kapak parçası: gövde yarısı yok; kutu x 4421,5–4441,5 / 5188,5–5208,5 · z 49–77,5 dikmenin YANINDA havada
    (z 49–59 kısmı) · alt kapaklardaki 6 menteşe kapağın iç sacını 10 mm deliyor (denetim: 6 ÇAKIŞMA).
  2 Bas-aç gövdeleri (6 · 20 × 30 × 18) 30'luk orta dikmeye ortalanmamış: her biri dikmenin dışına 6,5 mm taşıyor (x 4840–4846,5 / 4876,5–4883 havada) ·
    üst kapaklar arkası açık tava → pimin bastığı yüz yok.
  3 Sol dikme yarım: y 126–520 arası 1 mm lam + üstü 20 × 30 profil (eski içecek kolisi bandı için; koli artık U_KE'de) → yarıda kesilen profil.
  4 Alt dayama dudağı (3 × 14 lama, y 126–129, x 4402,5–5208,5) robot çöpü kovasının öne çekilme yolunda (kova altı y 127,5 < 129).
  5 Kabuk (sol / sağ / arka / tavan) TEK BİRLEŞİK KATI: ayrı sac yok, birleşim bükümü yok → üretilemez.
  6 Taban ön kenarı z 57,5, çerçeve önü 59 → dikmeler tabandan 1,5 mm taşıyor (basamak).
  7 Üst kapaklarda 4 omega takviye (ara kayıt) · alt kapaklar kutu kesit, üstler açık tava → tutarsız kapak yapısı.
YENİ KURGU (dış zarf, kotlar, kapak düzeni v3.7, ağız penceresi, klape, şarjör yan kapısı, ayaklar DEĞİŞMEZ)
  KABUK 304 1,5: sol yan (pizza penceresi 978–1062 × −372…−24 + K↔E 3 × Ø9: (y 1100 / 1750 · z −800) + (877 · −100)) · sağ yan (şarjör yan kapısı açıklığı
    231–989 × −823…−411) · ikisinde de ARKA 15 mm iç büküm (arka sacın iç yüzüne, y 126–1860,5) · ARKA sac tek parça (servis, yan bükümlere
    arkadan bombe vida) · TAVAN tek sac + sol / sağ 20 mm aşağı büküm (y 1840,5–1860,5 · z −827…+29: arka büküm ile ön dikme arasında boydan
    boya) + Harting 10B soket ağzı 66 × 36 (U_KE tabanındakiyle birebir) · ön / üst dış yüzde vida yok (bükümlere PEM, içten).
  TABAN 304 3 mm 4401,5–5228,5 · z −828,5…+59 (ön kenar çerçeve önüyle TEK ÇİZGİ).
  ÖN KASA (kaynaklı, 304 kutu profil · z 29–59 = kapak arkası): sol dikme 20 × 30 × 2 ve sağ dikme 20 × 30 × 2 TAM BOY 126–1860,5 (simetrik) ·
    orta dikme 40 × 30 × 2 TAM BOY, dikey derzin (4860/4863) ekseninde 4841,5–4881,5 (sol yüzü ağız penceresinin sağ kasasıyla aynı çizgi) ·
    788 kayıt 30 × 30 × 2 iki parça (dikmeler arasına alın kaynağı). Alt dayama dudağı KALKTI (kova yolu açık).
  KAPAKLAR (4 · zarf v3.7 ile aynı): ÇİFT CİDAR = dış tava 304 1,5 (ön yüz 77,5–79 + 20 dönüş) + iç kapatma sacı 1,0 (z 59–60, dönüşlere kaynaklı) ·
    omegalar KALKTI · sol üstte robot ağzı PENCERESİ (iki cidar kesik + 1,5 kasa dönüşü) · sol altta klape açıklığı 130 × 130 (ön yüz) + iç sacta klape
    dönüş deliği 144 × 168 (klape / menteşe / yaprak kapak içinde, değişmedi).
  MENTEŞE (12, gizli 180° kaldır-çıkar): GÖVDE YARISI dikme profilinin içinde (cep: ön duvarda pencere) — opak · KANAT YARISI kapak içinde (iç sacta
    pencere, ön yüzün iç yüzüne kaynak) — saydam kapakla birlikte. Yükseklikler aynı (alt 300 / 530 / 680 · üst 900 / 1360 / 1750).
  BAS-AÇ (6, Ø13,8 · z 31–59): orta dikmenin İÇİNDE (ön duvarda delik), her kapağa kendi pimi (x 4851 / 4872) · y 715 / 1015 / 1715 · pim kapağın
    iç sacına basar (karşılık sacı = iç sac).
KALKAN: onyuz_alt_dayama_dudagi · onyuz_kapak_E_ust_omega_0…3 · sol dikme lamı (dikme tam boy oldu).
Kullanım: python e_govde_yeni.py giris.glb cikis.glb [parca_kutulari.json]"""
import json, struct, sys, os
import numpy as np
import cadquery as cq

V = cq.Vector
XE = 4400.0
T, TI = 1.5, 1.0
X0, X1 = XE, XE + 830.0
XI0, XI1 = X0 + T, X1 - T                    # 4401,5 · 5228,5
Y0, YTB, YH = 123.0, 126.0, 1862.0
YTV = YH - T                                 # 1860,5 tavan altı
ZA, ZAI, ZON, ZK = -830.0, -828.5, 59.0, 79.0
ZC0 = 29.0                                   # ön kasa arkası (profil 30 derin: 29–59)
ARKA_BUK = 15.0                              # yan sacların arka iç bükümü
TAV_BUK = 20.0                               # tavan yan bükümleri
PENCERE = (978.0, 1062.0, -372.0, -24.0)     # K → E pizza penceresi (y0 y1 z0 z1)
SARJOR_AC = (231.0, 989.0, -823.0, -411.0)   # sağ sac şarjör kapısı açıklığı
HARTING = (5067.0, 5133.0, -778.0, -742.0)   # tavan soket ağzı (U_KE tabanında aynı)
K_M8 = ((1100.0, -800.0), (1750.0, -800.0), (877.0, -100.0))   # K ↔ E M8 (h3_k_sac_v1.M8_E · K'daki perçin somunlarının karşısı) · cıvata E içinden
AYAK_XZ = ((60.0, -110.0), (770.0, -110.0), (60.0, -770.0), (770.0, -770.0), (415.0, -110.0), (415.0, -770.0))
# ön kasa
DS = (XI0, XI0 + 20.0)                       # sol dikme 4401,5–4421,5
DG = (XI1 - 20.0, XI1)                       # sağ dikme 5208,5–5228,5
DERZ = (4860.0, 4863.0)
XM = (DERZ[0] + DERZ[1]) / 2.0               # 4861,5
DO = (XM - 20.0, XM + 20.0)                  # orta dikme 4841,5–4881,5
KY = (773.0, 803.0)                          # 788 kayıt
# kapaklar (v3.7 h3_kapak_v1: E_X, E_DERZ, B_UST, Y_DUZ, Y_TAVAN_KAPAK)
KAPAK = {"alt_sol": (4402.0, DERZ[0], 126.0, 785.0), "alt_sag": (DERZ[1], 5230.0, 126.0, 785.0),
         "ust_sol": (4402.0, DERZ[0], 788.0, 2197.0), "ust_sag": (DERZ[1], 5230.0, 788.0, 2197.0)}
AGIZ = (4485.0, 4840.0, 886.0, 1062.0)
KLAPE_AC = (4464.0, 4594.0, 610.0, 740.0)
KLAPE_IC = (4457.0, 4601.0, 603.0, 771.0)    # klape levhası 4458–4600 × 604–753,5 + yaprak 742,5–770 (± 1) → iç sacta dönüş deliği
MENT_Y = {"alt": (300.0, 530.0, 680.0), "ust": (900.0, 1360.0, 1750.0)}
MENT_H = 60.0
BASAC_Y = {"alt": (715.0,), "ust": (1015.0, 1715.0)}
BASAC_X = {"sol": 4851.0, "sag": 4872.0}
BASAC_R = 6.9


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def tek(r):
    try: r = r.clean()
    except Exception: pass
    if r.ShapeType() != "Solid":
        so = r.Solids()
        assert len(so) == 1, len(so)
        r = so[0]
    return r


def bir(*s):
    r = s[0]
    for q in s[1:]: r = r.fuse(q)
    return tek(r)


def kes(s, *al):
    al = [a for a in al if a is not None]
    return tek(s.cut(*al)) if al else s


def sil(ax, p, r, a0, a1):
    d = {"x": V(1, 0, 0), "y": V(0, 1, 0), "z": V(0, 0, 1)}[ax]
    o = list(p); o["xyz".index(ax)] = a0
    return cq.Solid.makeCylinder(r, a1 - a0, V(*o), d)


def boru(x0, x1, y0, y1, z0, z1, et=2.0):
    a = [x0, x1, y0, y1, z0, z1]; d = [x1 - x0, y1 - y0, z1 - z0]; ax = int(np.argmax(d))
    ic = [x0 + et, x1 - et, y0 + et, y1 - et, z0 + et, z1 - et]; ic[2 * ax], ic[2 * ax + 1] = a[2 * ax] - 1, a[2 * ax + 1] + 1
    return kutu(*a).cut(kutu(*ic))


# ======================================================================================= KABUK + TABAN
def kabuk():
    S = {}
    sol = kutu(X0, XI0, Y0, YTV, ZAI, ZON)
    sol = kes(sol, kutu(X0 - 1, XI0 + 1, PENCERE[0], PENCERE[1], PENCERE[2], PENCERE[3]),
              *[sil("x", (0, y, z), 4.5, X0 - 1, XI0 + 1) for y, z in K_M8])
    S["sol_sac_pizza_penceresi"] = bir(sol, kutu(XI0, XI0 + ARKA_BUK, YTB, YTV, ZAI, ZAI + T))
    sag = kes(kutu(XI1, X1, Y0, YTV, ZAI, ZON), kutu(XI1 - 1, X1 + 1, SARJOR_AC[0], SARJOR_AC[1], SARJOR_AC[2], SARJOR_AC[3]))
    S["sag_sac"] = bir(sag, kutu(XI1 - ARKA_BUK, XI1, YTB, YTV, ZAI, ZAI + T))
    S["arka_sac"] = kutu(X0, X1, Y0, YH, ZA, ZAI)
    tv = bir(kutu(X0, X1, YTV, YH, ZAI, ZON),
             kutu(XI0, XI0 + T, YTV - TAV_BUK, YTV, ZAI + T, ZC0), kutu(XI1 - T, XI1, YTV - TAV_BUK, YTV, ZAI + T, ZC0))
    S["ust_sac"] = kes(tv, kutu(HARTING[0], HARTING[1], YTV - 1, YH + 1, HARTING[2], HARTING[3]))
    return S


def taban_kasa():
    S = {"taban_sac_3": kutu(XI0, XI1, Y0, YTB, ZAI, ZON)}
    # yan dikmeler: menteşe cepleri (ön duvarda pencere = menteşe gövde yarısı genişliği)
    cep_s, cep_g = [], []
    for k in ("alt", "ust"):
        for y in MENT_Y[k]:
            cep_s.append(kutu(DS[0] + 2.0, DS[1] - 2.0, y, y + MENT_H, ZON - 2.0 - 0.01, ZON + 1))
            cep_g.append(kutu(DG[0] + 2.0, DG[1] - 2.0, y, y + MENT_H, ZON - 2.0 - 0.01, ZON + 1))
    S["onyuz_dikme_sol"] = kes(boru(DS[0], DS[1], YTB, YTV, ZC0, ZON), *cep_s)
    S["onyuz_dikme_sag"] = kes(boru(DG[0], DG[1], YTB, YTV, ZC0, ZON), *cep_g)
    ba = [sil("z", (BASAC_X[t], y, 0), BASAC_R, ZON - 2.0 - 0.01, ZON + 1) for t in BASAC_X for k in BASAC_Y for y in BASAC_Y[k]]
    S["onyuz_dikme_orta"] = kes(boru(DO[0], DO[1], YTB, YTV, ZC0, ZON), *ba)
    S["onyuz_kayit_788_sol"] = boru(DS[1], DO[0], KY[0], KY[1], ZC0, ZON)
    S["onyuz_kayit_788_sag"] = boru(DO[1], DG[0], KY[0], KY[1], ZC0, ZON)
    return S


def sarjor_kapisi():
    """kutu_cad_v14.govde() ile birebir (dünya): kapı + iki iç dönüş · 2 gizli menteşe (içte) · bas-aç (içte)"""
    k = bir(kutu(XI1, X1, 234.0, 986.0, -820.0, -414.0), kutu(XE + 818.0, XI1, 234.0, 235.5, -820.0, -414.0), kutu(XE + 818.0, XI1, 984.5, 986.0, -820.0, -414.0))
    M = {"sarjor_yan_kapisi_mentese_%d" % i: kutu(XI1 - 8.5, XI1, yc - 25.0, yc + 25.0, -826.0, -814.0) for i, yc in enumerate((300.0, 900.0))}
    return k, M, kutu(XI1 - 8.5, XI1, 590.0, 630.0, -418.0, -406.0)


def ayaklar():
    out = {}
    for i, (ax, az) in enumerate(AYAK_XZ):
        out["ayak_%d" % i] = bir(sil("y", (XE + ax, 0, az), 20.0, 0.0, 8.0), sil("y", (XE + ax, 0, az), 6.0, 8.0, Y0))
    return out


# ======================================================================================= KAPAKLAR + DONANIM
def menteseler():
    G, K = {}, {}
    for kn in KAPAK:
        k, t = kn.split("_")
        for i, y in enumerate(MENT_Y[k]):
            j = i + (0 if k == "alt" else 3)
            if t == "sol":
                G["onyuz_kapak_E_mentese_sol_%d_govde" % j] = kutu(DS[0] + 2.0, DS[1] - 2.0, y, y + MENT_H, ZC0 + 2.0, ZON)
                K["onyuz_kapak_E_mentese_sol_%d_kanat" % j] = kutu(DS[0] + 2.0, DS[1] - 2.0, y, y + MENT_H, ZON, ZK - T)
            else:
                G["onyuz_kapak_E_mentese_sag_%d_govde" % j] = kutu(DG[0] + 2.0, DG[1] - 2.0, y, y + MENT_H, ZC0 + 2.0, ZON)
                K["onyuz_kapak_E_mentese_sag_%d_kanat" % j] = kutu(DG[0] + 2.0, X1 - T, y, y + MENT_H, ZON, ZK - T)
    return G, K


def basaclar():
    B = {}
    for k in BASAC_Y:
        for i, y in enumerate(BASAC_Y[k]):
            j = i + (0 if k == "alt" else 1)
            for t in BASAC_X:
                B["onyuz_kapak_E_basac_%s_%d" % (t, j)] = sil("z", (BASAC_X[t], y, 0), BASAC_R, ZC0 + 2.0, ZON)
    return B


def dis_tava(x0, x1, y0, y1, pencere=None, on_kesik=None):
    z1, z0 = ZK, ZON
    s = bir(kutu(x0, x1, y0, y1, z1 - T, z1), kutu(x0, x1, y0, y0 + T, z0, z1 - T), kutu(x0, x1, y1 - T, y1, z0, z1 - T),
            kutu(x0, x0 + T, y0 + T, y1 - T, z0, z1 - T), kutu(x1 - T, x1, y0 + T, y1 - T, z0, z1 - T))
    if pencere:
        a0, a1, b0, b1 = pencere
        s = kes(s, kutu(a0, a1, b0, b1, z0 - 1, z1 + 1))
        s = bir(s, kutu(a0 - T, a0, b0 - T, b1 + T, z0, z1 - T), kutu(a1, a1 + T, b0 - T, b1 + T, z0, z1 - T),
                kutu(a0, a1, b0 - T, b0, z0, z1 - T), kutu(a0, a1, b1, b1 + T, z0, z1 - T))
    if on_kesik:
        a0, a1, b0, b1 = on_kesik
        s = kes(s, kutu(a0, a1, b0, b1, z1 - T - 1, z1 + 1))
    return s


def ic_sac(x0, x1, y0, y1, delikler):
    return kes(kutu(x0 + T, x1 - T, y0 + T, y1 - T, ZON, ZON + TI), *delikler)


def kapaklar(MK):
    S = {}
    for kn, (x0, x1, y0, y1) in KAPAK.items():
        pen = AGIZ if kn == "ust_sol" else None
        onk = KLAPE_AC if kn == "alt_sol" else None
        S["onyuz_kapak_E_%s" % kn] = dis_tava(x0, x1, y0, y1, pen, onk)
        dl = [m for m in MK.values() if m.BoundingBox().xmin < x1 and m.BoundingBox().xmax > x0 and m.BoundingBox().ymin < y1 and m.BoundingBox().ymax > y0]
        if pen: dl.append(kutu(pen[0] - T, pen[1] + T, pen[2] - T, pen[3] + T, ZON - 1, ZON + TI + 1))
        if onk: dl.append(kutu(KLAPE_IC[0], KLAPE_IC[1], KLAPE_IC[2], KLAPE_IC[3], ZON - 1, ZON + TI + 1))
        S["onyuz_kapak_E_%s_ic_sac" % kn] = ic_sac(x0, x1, y0, y1, dl)
    return S


# ======================================================================================= DÜĞÜMLER
def kur():
    D = {"E_GOVDE__kabuk": {}, "E_GOVDE__sac": {}, "E_GOVDE__celik": {}, "E_GOVDE__plastik": {}, "E_GOVDE__on_seffaf": {}}
    KPK = set()
    for a, s in kabuk().items(): D["E_GOVDE__kabuk"][a] = s
    for a, s in taban_kasa().items(): D["E_GOVDE__sac"][a] = s
    kp, km, kb = sarjor_kapisi()
    D["E_GOVDE__sac"]["sarjor_yan_kapisi"] = kp; KPK.add("sarjor_yan_kapisi")
    for a, s in ayaklar().items(): D["E_GOVDE__celik"][a] = s
    for a, s in km.items(): D["E_GOVDE__celik"][a] = s; KPK.add(a)
    MG, MK = menteseler()
    for a, s in MG.items(): D["E_GOVDE__celik"][a] = s; KPK.add(a)
    for a, s in basaclar().items(): D["E_GOVDE__plastik"][a] = s; KPK.add(a)
    D["E_GOVDE__plastik"]["sarjor_yan_kapisi_basac"] = kb; KPK.add("sarjor_yan_kapisi_basac")
    for a, s in kapaklar(MK).items(): D["E_GOVDE__on_seffaf"][a] = s; KPK.add(a)
    for a, s in MK.items(): D["E_GOVDE__on_seffaf"][a] = s; KPK.add(a)
    return D, KPK


KALKAN = ["onyuz_alt_dayama_dudagi", "onyuz_kapak_E_ust_omega_0", "onyuz_kapak_E_ust_omega_1", "onyuz_kapak_E_ust_omega_2", "onyuz_kapak_E_ust_omega_3",
          "onyuz_kayit_788 (tek parça → iki parça, orta dikme sürekli)", "onyuz_kapak_E_mentese_* (tek kutu → govde + kanat)", "sol dikme lamı (y 126–520)"]


def tess(s):
    P, I = [], []
    for f in s.Faces():
        v, t = f.tessellate(0.1, 0.2)
        o = sum(len(p) for p in P)
        P.append(np.array([[q.x, q.y, q.z] for q in v], float))
        I.append(np.array(t, np.int64) + o if len(t) else np.zeros((0, 3), np.int64))
    return np.vstack(P), np.vstack(I)


def ag(solidler):
    XX, TT, o, say = [], [], 0, []
    for s in solidler:
        X, Tt = tess(s); XX.append(X); TT.append(Tt + o); o += len(X); say.append(len(Tt))
    X = np.vstack(XX); Tt = np.vstack(TT)
    Xf = X[Tt.reshape(-1)]; n = np.cross(Xf[1::3] - Xf[0::3], Xf[2::3] - Xf[0::3])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return (Xf / 1000.0).astype(np.float32), np.repeat(n, 3, axis=0).astype(np.float32), np.arange(len(Xf), dtype=np.uint32), say


def yaz(gi, go, kj):
    DG_, KPK = kur()
    for nd, dct in DG_.items():
        for a, s in dct.items():
            assert s.isValid(), (nd, a)
    raw = open(gi, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
    bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])

    def ekle(arr, tip, hedef):
        while len(BIN) % 4: BIN.extend(b"\0")
        off = len(BIN); BIN.extend(arr.tobytes())
        J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
        a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
        if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
        J["accessors"].append(a); return len(J["accessors"]) - 1

    ARALIK = {}
    for dugum, dct in DG_.items():
        nd = [n for n in J["nodes"] if n.get("name") == dugum][0]
        assert not any(k in nd for k in ("translation", "rotation", "scale", "matrix")), dugum
        adlar = list(dct)
        X, N, I, say = ag([dct[a] for a in adlar])
        pr = J["meshes"][nd["mesh"]]["primitives"][0]
        pr["attributes"] = {"POSITION": ekle(X, "VEC3", 34962), "NORMAL": ekle(N, "VEC3", 34962)}
        pr["indices"] = ekle(I, "SCALAR", 34963)
        nt = len(I); ex = pr.setdefault("extras", {})
        for k in ("kat", "mek"):
            if k in ex: ex[k] = [ex[k][0], 0, nt]
        kp, b = [], 0
        for a, n_ in zip(adlar, say):
            ARALIK[a] = [dugum, 3 * b, 3 * n_]
            if a in KPK:
                if kp and kp[-2] + kp[-1] == 3 * b: kp[-1] += 3 * n_
                else: kp += [3 * b, 3 * n_]
            b += n_
        assert 3 * b == nt
        ex["kpk"] = kp
        print("  %-22s %3d parça · %6d üçgen · kpk %s" % (dugum, len(adlar), nt // 3, kp))
    J["buffers"][0]["byteLength"] = len(BIN)
    jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
    while len(BIN) % 4: BIN.extend(b"\0")
    open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
                         + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
    kut = {}
    for dugum, dct in DG_.items():
        for a, s in dct.items():
            bb = s.BoundingBox()
            kut[a] = dict(dugum=dugum, kpk=a in KPK, kutu=[round(v, 2) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)], indis=ARALIK[a][1:])
    json.dump(dict(parca=kut, kalkan=KALKAN), open(kj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("yazıldı", go, "·", len(kut), "parça")
    return DG_, KPK


if __name__ == "__main__":
    gi, go = sys.argv[1:3]
    kj = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "eg", "e_parca_kutulari.json")
    yaz(gi, go, kj)
    sys.stdout.flush(); os._exit(0)
