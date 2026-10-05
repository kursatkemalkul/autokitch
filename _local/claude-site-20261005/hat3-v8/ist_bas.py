# -*- coding: utf-8 -*-
"""HAT v2.4 (v3.2 yönteminin v2 yerleşimine uyarlaması · Claude 1 Eki) · ELEKTRİK · İSTASYON İÇİ CİHAZ KABLOLARI v1 — her sabit motor / sensör / fan / sürücü / valf adası → kendi istasyon panosuna ya da kablo kanalına.
YÖNTEM (sade): cihaz ucu → en yakın kablo kanalı / pano alt yüzü · kanal içindeki kablolar çizilmez (kapaklı kanal) · uzun açık parçalar en yakın yüzeye P-kelepçeli ·
sac geçişleri IP68 rakorlu (delik montajda açılır) · hareketli gruplardaki cihazlar (TOPPING arabası · açıcı · K itici Z) ENERJİ ZİNCİRİNDEN — sabit kablo yok.
YOL: önce h2_elk_rota (1–4 köşe) · olmazsa h2_elk_voksel (yüzey ızgarası A*, duvara yaslanan) · her yol gerçek katı denetiminden geçer.
HAREKET ZARFLARI yasak bölge: TOPPING araba + tabla · K itici (X 250 · Z 350, kesme_cad_v11.grup_trs'ten) · K kesici (−125 y).
TOPPING: KD1 sağ cepte dikey kanal (2421–2449) + KD2 pano altı yatay kanal (1890–2466, üstü panoya dayalı) · sürücüler → pano 4 şerit ·
evaporatör fanları kaset tavanından rakorla dik pano altına · A emniyet + ışık perdesi → A|TOPPING duvarında M12 dağıtıcı kutusu → tek kablo rakorla panoya ·
F yükleme bandı motoru → F|TOPPING duvarı rakoru → KD1."""
import math
import cadquery as cq
import h2_elk_ortak as EO
import h2_elk_rota as ER
import h2_elk_voksel as EV
from h2_elk_ortak import kut, sil, boru, rakor

V = cq.Vector
RAPOR = dict(yol=[], bulunamadi=[], askida=[])
KS_SUPURME = {"KESICI": (0, 0, -125, 0, 0, 0), "ITICI_ARABA": (0, 250, 0, 0, 0, 0), "ITICI_CAPRAZ": (0, 250, 0, 0, 0, 350),
              "ITICI_KOL": (0, 250, 0, 0, 0, 350), "ITICI_YUZ": (0, 250, -14.5, 0, 0, 350)}           # kesme_cad_v11.grup_trs örneklemesi (0–25 s)
TOPPING_ZARF = kut(661.5, 2520.0, 931.0, 1045.0, -345.0, -3.0)                               # bayrak + apron + araba plakası + kaset bandı (x 896 → aktarma +1279)
TOPPING_ZARF_KIZAK = kut(661.5, 2520.0, 912.0, 931.0, -345.0, -35.0)                          # kızak ayakları (ön şerit z > −35 serbest: sensörler)
TOPPING_ZARF_MOTOR = kut(821.5, 2400.0, 898.0, 942.0, -200.0, -140.0)                       # tekneye sarkan dönüş motoru


def _yorunge(g):
    """grup öteleme yörüngesi → yön değiştirdiği noktalar (tekrarsız)"""
    import kesme_cad_v11 as K11
    P = []
    for i in range(0, 262):
        p = tuple(round(v, 1) for v in K11.grup_trs(g, i * 0.1))
        if not P or math.dist(p, P[-1]) > 0.05: P.append(p)
    anah = [P[0]]
    for i in range(1, len(P) - 1):
        a, b, c = anah[-1], P[i], P[i + 1]
        d1 = [b[k] - a[k] for k in range(3)]; d2 = [c[k] - b[k] for k in range(3)]
        cr = (d1[1] * d2[2] - d1[2] * d2[1], d1[2] * d2[0] - d1[0] * d2[2], d1[0] * d2[1] - d1[1] * d2[0])
        if math.sqrt(sum(v * v for v in cr)) > 1e-3 or sum(d1[k] * d2[k] for k in range(3)) < 0: anah.append(b)
    anah.append(P[-1])
    return anah


def _supurmeler():
    import json, io, os
    idx = json.load(io.open(os.path.join(EO.DD, "dunya.json"), encoding="utf-8"))
    G = {"%s|%s" % (i[0], i[1]): i[3] for i in idx}
    Y = {g: _yorunge(g) for g in KS_SUPURME}
    out = []
    for ad, s, b in EO.dokum():
        g = G.get(ad)
        if g not in Y or not ad.startswith("K_"): continue
        A = Y[g]
        for j, (p, q) in enumerate(zip(A[:-1], A[1:])):
            out.append(("SUPURME_%s_%d" % (ad, j), kut(b[0] + min(p[0], q[0]), b[1] + max(p[0], q[0]), b[2] + min(p[1], q[1]), b[3] + max(p[1], q[1]),
                                                       b[4] + min(p[2], q[2]), b[5] + max(p[2], q[2]))))
    return out


def kur(ekle, DELIKLER, DUSUR):
    ER.ekli_ekle("YASAK_TOPPING_araba_zarfi", TOPPING_ZARF); ER.ekli_ekle("YASAK_TOPPING_kizak_zarfi", TOPPING_ZARF_KIZAK)
    ER.ekli_ekle("YASAK_TOPPING_donus_motoru_zarfi", TOPPING_ZARF_MOTOR)
    for ad, s in _supurmeler(): ER.ekli_ekle("YASAK_" + ad, s)
    B = {"C": "ELK_TOPPING", "K": "ELK_K", "B": "ELK_DOLAP", "A": "ELK_TOPPING", "F": "ELK_TOPPING"}

    def parca(ad, sh, mal, ist, bom=None):
        ekle(ad, sh, mal, B[ist], bom); ER.ekli_ekle(ad, sh)

    def kanal_kutu(ad, x0, x1, y0, y1, z0, z1, ist, bom, t=1.5):
        """kapaklı PVC kablo kanalı (kapalı kutu kesit — kablolar yan yüzdeki parmak yuvalarından girer)"""
        sh = kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, z0 + t, z1 - t))
        parca(ad, sh, "kanal", ist, bom)

    def yol_bul(a, b, r, haric=(), bolge=None, h=4.0):
        p, sh = ER.bul(a, b, r, haric=haric)
        if p is not None: return p, None
        neden = None
        for pay in (1.0, 3.0, 5.0):
            p, neden = EV.bul(a, b, r, bolge=bolge, haric=haric, h=h, pay=pay)
            if p is None: return None, neden
            ok, engel = ER.temiz(boru(p, r), haric)
            if ok: return p, None
            neden = "voksel yolu gerçek denetimde: " + str(engel)
        return None, neden

    def cihaz(ad, S, T, r, ist, itme=None, via=(), bolge=None, h=4.0, bom=None, on=None):
        """S cihaz yüzünde · itme (eksen, mm) dışarı · via: nokta ya da (nokta, haric) · T kanal / pano yüzünde · on: T'ye yaklaşma ön noktası"""
        if itme:                                                              # kablo cihaz yüzünden 0,3 mm açıkta başlar (eğri yüz / döküm gürültüsü)
            S = list(S); S[itme[0]] += 0.3 * (1.0 if itme[1] > 0 else -1.0); S = tuple(S)
        pts = [tuple(S)]
        cur = tuple(S)
        if itme:
            c2 = list(S); c2[itme[0]] += itme[1]; cur = tuple(c2); pts.append(cur)
        durak = [(tuple(v), ()) if isinstance(v[0], (int, float)) else (tuple(v[0]), v[1]) for v in via]
        if on is not None: durak.append((tuple(on), ()))
        durak.append((tuple(T), ()))
        for v, har in durak:
            if math.dist(cur, v) < 1e-6: continue
            p, neden = yol_bul(cur, v, r, haric=har, bolge=bolge, h=h)
            if p is None:
                RAPOR["bulunamadi"].append((ad, cur, v, neden)); return None
            pts += list(p[1:]); cur = v
        q = [pts[0]]
        for p_ in pts[1:]:
            if math.dist(p_, q[-1]) > 0.05: q.append(p_)
        sh = boru(q, r)
        parca("kablo_%s" % ad, sh, "kablo", ist, bom)
        kl, aski = ER.kelepceler(q, r)
        for j, (_p, ks) in enumerate(kl):
            parca("kablo_%s_kelepce_%d" % (ad, j), ks, "celik", ist)
        RAPOR["yol"].append((ad, round(EO.uzunluk(q)), len(q) - 1, len(kl)))
        RAPOR["askida"] += [(ad,) + tuple(a) for a in aski]
        return q

    def sabit(ad, pts, r, ist, bom=None, haric=()):
        """elle tasarlanmış yol · gerçek katı denetimi"""
        sh = boru(pts, r)
        ok, engel = ER.temiz(sh, haric)
        if not ok:
            RAPOR["bulunamadi"].append((ad, pts[0], pts[-1], engel)); return None
