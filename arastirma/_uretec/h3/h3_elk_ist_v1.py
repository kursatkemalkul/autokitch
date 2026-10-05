# -*- coding: utf-8 -*-
"""HAT v3.2 · ELEKTRİK · İSTASYON İÇİ CİHAZ KABLOLARI v1 — her sabit motor / sensör / fan / sürücü / valf adası → kendi istasyon panosuna ya da kablo kanalına.
YÖNTEM (sade): cihaz ucu → en yakın kablo kanalı / pano alt yüzü · kanal içindeki kablolar çizilmez (kapaklı kanal) · uzun açık parçalar en yakın yüzeye P-kelepçeli ·
sac geçişleri IP68 rakorlu (delik montajda açılır) · hareketli gruplardaki cihazlar (TOPPING arabası · K itici Z · açıcı hazır alınır, kablosu yok) ENERJİ ZİNCİRİNDEN — sabit kablo yok.
YOL: önce h3_elk_rota (1–4 köşe) · olmazsa h3_elk_voksel (yüzey ızgarası A*, duvara yaslanan) · her yol gerçek katı denetiminden geçer.
HAREKET ZARFLARI yasak bölge: TOPPING araba + tabla · K itici (X 250 · Z 350, kesme_cad_v11.grup_trs'ten) · K kesici (−125 y).
TOPPING: KD1 sağ cepte dikey kanal (2421–2449) + KD2 pano altı yatay kanal (1890–2466, üstü panoya dayalı) · sürücüler → pano 4 şerit ·
evaporatör fanları kaset tavanından rakorla dik pano altına · A emniyet + ışık perdesi → A|TOPPING duvarında M12 dağıtıcı kutusu → tek kablo rakorla panoya ·
F yükleme bandı motoru → F|TOPPING duvarı rakoru → KD1."""
import math
import cadquery as cq
import h3_elk_ortak as EO
import h3_elk_rota as ER
import h3_elk_voksel as EV
from h3_elk_ortak import kut, sil, boru, rakor

V = cq.Vector
RAPOR = dict(yol=[], bulunamadi=[], askida=[])
KS_SUPURME = {"KESICI": (0, 0, -125, 0, 0, 0), "ITICI_ARABA": (0, 250, 0, 0, 0, 0), "ITICI_CAPRAZ": (0, 250, 0, 0, 0, 350),
              "ITICI_KOL": (0, 250, 0, 0, 0, 350), "ITICI_YUZ": (0, 250, -14.5, 0, 0, 350)}           # kesme_cad_v11.grup_trs örneklemesi (0–25 s)
TOPPING_ZARF = kut(890.0, 2520.0, 931.0, 1045.0, -345.0, -3.0)                               # bayrak + apron + araba plakası + kaset bandı (x 896 → aktarma +1279)
TOPPING_ZARF_KIZAK = kut(890.0, 2520.0, 912.0, 931.0, -345.0, -35.0)                          # kızak ayakları (ön şerit z > −35 serbest: sensörler)
TOPPING_ZARF_MOTOR = kut(1050.0, 2400.0, 898.0, 942.0, -200.0, -140.0)                       # tekneye sarkan dönüş motoru


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
    B = {"C": "ELK_TOPPING", "K": "ELK_K", "B": "ELK_DOLAP", "A": "ELK_TOPPING", "F": "ELK_TOPPING", "KT": "ELK_K_TARTI"}   # v3.7 · KT: F içindeki tartıdan K'ye (modüller arası)

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
        parca("kablo_%s" % ad, sh, "kablo", ist, bom)
        kl, aski = ER.kelepceler(pts, r)
        for j, (_p, ks) in enumerate(kl):
            parca("kablo_%s_kelepce_%d" % (ad, j), ks, "celik", ist)
        RAPOR["yol"].append((ad, round(EO.uzunluk(pts)), len(pts) - 1, len(kl)))
        RAPOR["askida"] += [(ad,) + tuple(a) for a in aski]
        return pts

    def gecis(ad, p, eksen, mods, ist, r=6.0, t=1.5, yon="+", bom=None):
        rk, d_ = rakor(p, eksen, r + 0.3, t, yon=yon, disli=max(8.0, r + 3.0))      # delik kabloya 0,3 boşluklu (conta sıkar)
        parca("rakor_%s" % ad, rk, "rakor", ist, bom)
        for m, a in mods: DELIKLER.append((m, a, d_, "kablo geçişi %s" % ad))

    RK_BOM = lambda n: ("Kablo rakoru IP68 PA M16 / M20 + kontra somun (kalın duvarda kovan + iç sacta rakor)", n, "Lapp SKINTOP ST-M 53111010 / 53111020 + GMP-GL-M 53119010 / 53119020", "delik montajda açılır")

    # ======================================================= TOPPING =======================================================
    KB = ("Kablo kanalı PVC kapaklı (parmak yuvalı) · 30 × 40 / 40 × 40 (model KD1 28 geniş: AÇIK +2 mm)", 2, "arka duvara perçin somunlu", "KD1 sağ cep dikey + KD2 pano altı yatay")
    kanal_kutu("kanal_TOPPING_KD1_dikey", 2421.0, 2449.0, 905.0, 1840.0, -828.3, -788.5, "C", KB)
    kanal_kutu("kanal_TOPPING_KD2_pano_alti", 1890.0, 2449.0, 1840.0, 1879.9, -828.3, -788.5, "C", None)
    KD1 = lambda y, z=-808.0: (2449.2, y, z)                                   # KD1 sağ yüzü (parmak yuvası)
    PANO = lambda x, z: (x, 1879.8, z)                                         # kuru bölme panosu alt yüzü
    PANO_ON = lambda x, z: (x, 1862.0, z)
    BOLGE_KURU = (1467.5, 2468.5, 1109.0, 1879.9, -828.5, -630.0)

    # (5) soğutma grubu KLF6.6 (teknik bölme) → kuru bölme tabanı rakoru G2 → pano
    gecis("G2_kuru_bolme_tabani", (1700.0, 1109.0, -805.0), "y", [("TC", "kuru_bolme_tabani")], "C", r=5.0, t=1.5, yon="+", bom=RK_BOM(1))
    cihaz("TOPPING_sogutma_grubu_KLF66", (1700.0, 1087.0, -805.0), PANO(1700.0, -800.0), 5.0, "C",
          via=[((1700.0, 1140.0, -805.0), ("TOPPING_MODUL|kuru_bolme_tabani",))], on=PANO_ON(1700.0, -800.0), bolge=BOLGE_KURU,
          bom=("Soğutma grubu besleme + kontrol 5G1,5 (Secop KLF6.6 → pano)", 1, "Lapp ÖLFLEX CLASSIC 110 5G1,5 1119305", "Ø 8,1"))
    # (1) kaset motorları → sürücüler (ön yüz konnektörü) · motor kablosu mevcut kısa ucundan (−y) başlar
    SUR = [(1581.0, "sucuk_rotor", (2311.0, 1265.5, -807.0)), (1548.0, "sucuk_helezon", (2311.0, 1161.5, -807.0)),
           (1515.0, "kasar_rotor", (2062.0, 1296.5, -807.0)), (1482.0, "kasar_helezon", (2062.0, 1141.5, -807.0))]
    for i, (xs, nm, S) in enumerate(SUR):
        cihaz("TOPPING_motor_%s_surucu_%d" % (nm, i), S, (xs, 1452.0, -699.5), 3.0, "C", itme=(1, -6.0), on=(xs, 1452.0, -684.0),
              via=[(2360.0, S[1] - 6.3, -807.0)] if S[0] > 2200.0 else (),
              bolge=BOLGE_KURU, bom=("Step motor uzatma kablosu 6,1 m (STP-MTR-23079 kendi soketi → sürücü)", 4, "AutomationDirect STP-EXT-020", "kaset motorları step (TOPPING CAD) · fren yok") if i == 0 else None)
    # (2) sürücüler → pano (v3.5 · gerçek Ø8,9): UPS ile güç kaynağı arasında DİKEY KANAL 30 × 40 (x 1523–1553 · z −816…−776, UPS DIN rayının önü) · kısa uçlar
    #     sürücü üstünden kademeli (y 1490 / 1500 / 1510 / 1520) kanalın tabanına 2 × 2 dizilir · kanal içi kablolar çizilmez
    parca("kanal_TOPPING_surucu_dikey", kut(1523.0, 1553.0, 1535.0, 1879.5, -816.0, -776.0).cut(kut(1524.5, 1551.5, 1534.0, 1880.5, -814.5, -777.5)), "kanal", "C",
          ("Sürücü kabloları kanalı PVC 30 × 40 kapaklı, alttan + üstten açık (UPS ile güç kaynağı arası)", 1, "Hager tehalit BA7A40030", "pano altına"))
    for i, (xs, yj, xd, zd) in enumerate(((1482.0, 1500.0, 1530.5, -806.0), (1515.0, 1490.0, 1545.5, -806.0), (1548.0, 1510.0, 1530.5, -786.0), (1581.0, 1520.0, 1545.5, -786.0))):
        sabit("TOPPING_surucu_%d_pano" % i, [(xs, 1477.0, -730.0), (xs, yj, -730.0), (xs, yj, zd), (xd, yj, zd), (xd, 1536.5, zd)], 4.45, "C",   # önce kendi hizasında arkaya, sonra yana: kesişme yok
              bom=("Sürücü güç + kontrol kablosu 7G0,5 ekranlı (sürücü → pano)", 4, "Lapp ÖLFLEX CLASSIC 110 CY 7G0,5 1135007", "Ø 8,9 gerçek çap") if i == 0 else None)
    # (3) evaporatör fanları: kaset tavanından rakorla dik pano altına
    for i, xf in enumerate((1826.0, 1975.0)):
        gecis("TOPPING_evap_fani_%d" % i, (xf, 1765.0, -714.0), "y", [("TC", "evap_kaseti_dis_sac"), ("TC", "evap_kaseti_PU"), ("TC", "evap_kaseti_ic_sac")],
              "C", r=2.5, t=42.5, yon="+", bom=RK_BOM(2) if i == 0 else None)
        sabit("TOPPING_evap_fani_%d" % i, [(xf, 1712.0, -714.0), (xf, 1879.8, -714.0)], 2.5, "C",
              haric=("TOPPING_MODUL|evap_kaseti_dis_sac", "TOPPING_MODUL|evap_kaseti_PU", "TOPPING_MODUL|evap_kaseti_ic_sac"),
              bom=("Fan kablosu 4 × 0,5 (San Ace 9WPA 24 V PWM + hız → pano)", 2, "Lapp ÖLFLEX CLASSIC 110 4X0,5 1119754", "Ø 5,7 · 4 damar VARSAYIM (fan föyü)") if i == 0 else None)
    # (4) valf adası (12 bobin, çok pinli soket sol uçta) → pano
    cihaz("TOPPING_valf_adasi", (1998.0, 1295.0, -744.0), (2420.8, 1295.0, -808.0), 4.5, "C", itme=(0, 5.0), on=(2400.0, 1295.0, -808.0),
          bolge=BOLGE_KURU, bom=("Valf adası çok damarlı kablo 25 × 0,3 (D-sub → KD1 → pano)", 1, "SMC AXT100-DS25-050", "VARSAYIM: ada SMC D-sub tipi ise"))
    # (6) sağ cep (teknik bölmenin sağı, tabansız) → KD1: sabit tahrik motoru · enerji zinciri sabit ucu · tabla boş sensörü · x sensörleri · F yükleme bandı
    DELIKLER.append(("TC", "st_motor_kutusu", cq.Solid.makeCylinder(4.3, 6.0, V(2459.0, 986.5, -510.0), V(0, 0, 1)), "sabit tahrik motoru kablosu · motor kutusu arka duvarı lastik bilezik"))
    sabit("TOPPING_sabit_tahrik_motoru", [(2459.0, 986.5, -505.1), (2459.0, 986.5, -808.0), KD1(986.5)], 4.0, "C", haric=("TOPPING_MODUL|st_motor_kutusu",),
          bom=("Motor kablosu 4 × 1 + fren (sabit tahrik → KD1)", 1, "", "VARSAYIM: motor üreticisi seçilince (NEMA23 kapalı çevrim step)"))
    gecis("TOPPING_enerji_zinciri_sabit_ucu", (2459.0, 923.5, -475.0), "z", [("TC", "enerji_zinciri_kanali")], "C", r=6.0, t=3.0, yon="-", bom=RK_BOM(1))   # U kanal arka duvarı 3 mm
    sabit("TOPPING_enerji_zinciri_demeti", [(2459.0, 923.5, -460.0), (2459.0, 923.5, -808.0), KD1(923.5)], 6.0, "C", haric=("TOPPING_MODUL|enerji_zinciri_kanali",),
          bom=("Enerji zinciri demeti (araba: dönüş motoru · tabla sıfır sensörü) · zincir sabit ucundan KD1'e", 1, "", "zincir içi kablolar hareketli"))
    sabit("TOPPING_sensor_x_limit_sag", [(2375.0, 920.0, -18.7), (2375.0, 920.0, -16.0), (2375.0, 927.0, -16.0), (2375.0, 927.0, 5.0), (2455.0, 927.0, 5.0),
                                           (2455.0, 1076.0, 5.0), (2455.0, 1076.0, -795.0), (2449.2, 1076.0, -795.0)], 2.0, "C")
    sabit("TOPPING_tabla_bos_sensoru", [(2360.0, 1070.0, -170.0), (2459.0, 1070.0, -170.0), (2459.0, 1070.0, -808.0), KD1(1070.0)], 2.0, "C",
          bom=("Sensör kablosu M8 3 kutup PUR 5 m (Murrelektronik 7000-08041-6300500, Ø 4,1)", 4, "", "tabla boş · x sol limit · x sıfır · x sağ limit"))
    # F yükleme bandı motoru → F|TOPPING duvarı rakoru G6 → KD1
    gecis("G8_firin_govde_arka", (2780.0, 1121.5, -651.0), "z", [("FT", "govde_kabugu")], "F", r=4.0, t=1.5, yon="-", bom=RK_BOM(2))
    gecis("G6_F_TOPPING_duvari", (2516.5, 1121.5, -800.0), "x", [("TC", "dis_yan_sag"), ("FU", "f_ust_yan_sol")], "F", r=4.0, t=48.0, yon="+")
    sabit("F_yukleme_bandi_motoru", [(2780.0, 1121.5, -495.5), (2780.0, 1121.5, -651.0), (2780.0, 1121.5, -800.0), (2449.2, 1121.5, -800.0)], 4.0, "F",
          haric=("F_TP10_GOVDE|govde_kabugu", "TOPPING_MODUL|dis_yan_sag", "F_UST_KABIN|f_ust_yan_sol"),
          bom=("Step motor uzatma kablosu 6,1 m (yükleme bandı STP-MTR-23079 → TOPPING)", 1, "AutomationDirect STP-EXT-020", "yol ≤ 6,1 m"))
    # v3.6 (1 Eki · Claude · YEREL) · Kemal: "açıcının etrafındaki elektrik vs kaldır" — A'daki KABLO KANALI (kanal_A_sag_on_dikey), 6'lı SENSÖR DEMETİ, G7 rakoru ve
    #   A emniyet / ışık perdesi kabloları KALKTI (açıcı hazır alınır: kendi emniyet devresi tedarikçide · A'da tek besleme noktası = A istasyon kutusu + Harting,
    #   h3_elk_hat_v1.istasyon_kur). TOPPING'e ait x sol limit + x sıfır sensörleri (TOPPING ekseni A kabininin içine uzanır) X motoru kablosunun yanından
    #   A|TOPPING duvarındaki G10 rakorlarıyla TOPPING panosuna.
    gecis("G9_A_TOPPING_motor", (1436.0, 1640.0, -720.0), "x", [("TC", "dis_yan_sol")], "A", r=3.0, t=31.5, yon="-", bom=RK_BOM(1))
    for j_, yg_ in enumerate((1612.0,)):                                      # x sol limit + x sıfır tek rakorda (2 delikli conta)
        gecis("G10_A_TOPPING_sensor_%d" % j_, (1436.0, yg_, -720.0), "x", [("TC", "dis_yan_sol")], "A", r=2.0, t=31.5, yon="-", bom=RK_BOM(2) if j_ == 0 else None)
    BOLGE_A9 = (737.5, 1436.0, 893.5, 1860.5, -828.5, 60.0)
    BOLGE_AX = (737.5, 1600.0, 893.5, 1879.9, -828.5, 60.0)
    cihaz("TOPPING_x_motoru", (888.0, 924.5, -462.0), (1530.0, 1879.8, -720.0), 3.0, "C", itme=(2, -6.0),     # v3.6 · motor arka yüzünün ortası delik (mil / enkoder) → kablo 12 mm yanından
          via=[(888.0, 924.5, -775.0), (1388.5, 924.5, -775.0), (1388.5, 1640.0, -775.0), (1398.7, 1640.0, -720.0),
               ((1460.0, 1640.0, -720.0), ("TOPPING_MODUL|dis_yan_sol",))],
          on=(1530.0, 1862.0, -720.0), bolge=BOLGE_A9, h=5.0,
          bom=("Motor kablosu esnek PUR 4 × 0,75 + fren (X ekseni)", 1, "", "VARSAYIM: motor üreticisi seçilince · sürücüsü TOPPING panosunda"))
    cihaz("TOPPING_sensor_x_limit_sol", (1056.0, 920.0, -19.0), (1520.0, 1879.8, -730.0), 2.0, "C", itme=(2, 5.7),
          via=[(886.0, 920.0, -13.0), ((1460.0, 1612.0, -720.0), ("TOPPING_MODUL|dis_yan_sol",))], on=(1520.0, 1862.0, -730.0), bolge=BOLGE_AX, h=5.0,
          bom=("Sensör kablosu M8 3 kutup PUR 5 m (x sol limit + x sıfır · birleşimden sonra spiral sargılı çift · G10 rakorundan TOPPING panosuna)", 2, "Murrelektronik 7000-08041-6300500", "Ø 4,1"))
    # x sıfır sensörü x sol limitin 30 mm yanında: kısa uçla x sol limit kablosuna katılır, oradan iki kablo AYNI yoldan (spiral sargılı) G10 → pano
    sabit("TOPPING_sensor_x_home", [(1086.0, 920.0, -18.7), (1086.0, 920.0, -13.0), (1058.0, 920.0, -13.0)], 2.0, "C",
          haric=("YENI|kablo_TOPPING_sensor_x_limit_sol",))

    # ======================================================= K =======================================================
    BOLGE_K = (3990.0, 4398.5, 893.5, 1860.5, -828.5, 57.0)
    KT = lambda i: (4176.0 + 8.6 * i, 1640.0, -761.3)                       # klemens sırası ön yüzü (x 4172–4255 · y 1616–1664)
    KT_ON = lambda i: (4176.0 + 8.6 * i, 1640.0, -745.0 + 8.0 * (i % 2))
    kk = [("K_PulsaJet", (4025.0, 1214.3, -146.4), (1, 5.0), 2.5, 0), ("K_urun_sensoru_giris_verici", (4105.0, 1010.0, -438.0), (2, -5.0), 2.0, 1),
          ("K_urun_sensoru_giris_alici", (4105.0, 1010.0, 14.0), (2, 5.0), 2.0, 2), ("K_yag_pompasi_GJ-N21", (4150.0, 1684.6, -554.0), (2, -6.0), 3.0, 3),
          ("K_DGRF_SMT8M_0", (4200.0, 1533.3, -161.3), (2, 4.0), 2.0, 4), ("K_DGRF_SMT8M_1", (4200.0, 1408.3, -161.3), (2, 4.0), 2.0, 5),
          ("K_urun_sensoru_durus_verici", (4350.0, 1010.0, -438.0), (2, -5.0), 2.0, 7), ("K_urun_sensoru_durus_alici", (4350.0, 1010.0, 14.0), (2, 5.0), 2.0, 8),
          ("K_EC5000_bant_motoru", (4354.0, 969.0, -484.3), (2, -6.0), 3.0, 9)]          # klemens sırası kaynağın x'ine göre · PM1704 → 6
    for i, (nm, S, it, r, kt) in enumerate(kk):
        cihaz(nm, S, KT(kt), r, "K", itme=it, on=KT_ON(kt), bolge=BOLGE_K,
              bom=("Cihaz kabloları K (step motor · sensör M8/M12 PUR · PulsaJet M8)", len(kk) + 1, "STP-EXT-020 · Murrelektronik 7000-08041-6300500 / 7000-12221-6340500", "") if i == 0 else None)
    cihaz("K_yag_basinc_PM1704", (4225.0, 1809.7, -520.0), KT(6), 2.0, "K", itme=(1, 5.0), on=KT_ON(6), bolge=BOLGE_K)
    gecis("G4_tarti_FK_duvari", (3983.5, 1387.0, -296.0), "x", [("FU", "f_ust_yan_sag"), ("KS", "sol_sac_urun_girisi")], "KT", r=2.5, t=18.0, yon="-", bom=RK_BOM(1))
    cihaz("K_tarti_yuk_hucresi", (3938.5, 1387.0, -296.0), (4305.0, 1709.8, -773.0), 2.5, "KT", on=(4305.0, 1692.0, -773.0),
          via=[((4012.0, 1387.0, -296.0), ("F_UST_KABIN|f_ust_yan_sag", "K_GOVDE|sol_sac_urun_girisi"))], bolge=BOLGE_K,
          bom=("Yük hücresi kendi kablosu 6 m (PW15AH → SIWAREX WP231)", 1, "HBM PW15AH (6 m kablo seçeneği)", "ayrı kablo yok"))

    # ======================================================= DOLAP (B) =======================================================
    # çekmece reed sensörleri (açık + kapalı): lama yanından (lamaya kablo bağıyla) arkaya · motor üstünden kolon kablo kanalının yan yüzüne (parmak yuvası)
    D = {ad: sb for ad, s_, sb in EO.dokum()}
    kanallar = {k.split("|")[1].replace("kablo_kanali_", ""): v for k, v in D.items() if k.startswith("B_KABLO|kablo_kanali_K")}
    n = 0
    for k, sb in sorted(D.items()):
        if not (k.startswith("CEK_") and k.endswith("_reed_acik")): continue
        grp = k.split("|")[0]; kol = grp.split("_")[1]
        kn = kanallar.get(kol); rk = D.get(k.replace("_reed_acik", "_reed_kapali"))
        if kn is None or rk is None: RAPOR["bulunamadi"].append(("DOLAP_reed_" + grp, sb[:2], sb[2:4], "kanal/kapalı sensör yok")); continue
        rxc, ryc = (sb[0] + sb[1]) / 2.0, (sb[2] + sb[3]) / 2.0
        cx, cy = sb[0] - 2.3, sb[3] + 2.0                        # lama yan yüzüne dayalı (0,3 mm) · reed üst hizası
        yc = min(ryc, kn[3] - 12.0)                               # kanal üst ucunu aşmasın
        a_ = [(rxc, ryc, sb[4]), (rxc, ryc, sb[4] - 4.0), (cx, ryc, sb[4] - 4.0), (cx, cy, sb[4] - 4.0), (cx, cy, -760.0), (cx, yc, -760.0),
              (cx, yc, -777.0), (kn[0] - 0.2, yc, -777.0)]
        k_ = [(rxc, ryc, rk[4]), (rxc, ryc, -771.0), (rxc, yc, -771.0), (kn[0] - 0.2, yc, -771.0)]
        for nm, pts in (("acik", a_), ("kapali", k_)):
            q = [pts[0]]
            for p in pts[1:]:
                if math.dist(p, q[-1]) > 1e-6: q.append(p)
            sh = boru(q, 2.0)
            ok, engel = ER.temiz(sh)
            if not ok:
                RAPOR["bulunamadi"].append(("DOLAP_reed_%s_%s" % (grp, nm), q[0], q[-1], engel)); continue
            ad = "DOLAP_reed_%s_%s" % (grp, nm)
            parca("kablo_%s" % ad, sh, "kablo", "B",
                  ("Reed sensör kablosu 2 × 0,25 PUR (lamaya kablo bağıyla · kolon kanalına)", 42, "", "motor M12 soketi zaten kanala dayalı") if n == 0 else None)
            n += 1
            RAPOR["yol"].append((ad, round(EO.uzunluk(q)), len(q) - 1, 0))
    # soğutma grubu (Secop NLE8.8CN): kompresör üstünden sola · kondenser contasından (kablo lastiği) arkaya · dolap dikey kanalının sağ yüzüne
    DELIKLER.append(("SC", "tk_kondenser_contasi", cq.Solid.makeCylinder(4.6, 30.0, V(4036.0, 314.5, -515.0), V(0, 0, 1)), "Secop kablosu geçiş lastiği"))
    sabit("DOLAP_secop_NLE88", [(4213.0, 308.5, -244.0), (4213.0, 314.5, -244.0), (4036.0, 314.5, -244.0), (4036.0, 314.5, -780.0), (4075.0, 314.5, -780.0),
                                (4075.0, 314.5, -809.0), (4062.2, 314.5, -809.0)], 4.0, "B", haric=("B_SOGUTMA|tk_kondenser_contasi",),
          bom=("Kompresör kablosu 3G1,5 (Secop NLE8.8CN → dolap panosu · termik koruma kompresörün içinde)", 1, "Lapp ÖLFLEX CLASSIC 110 3G1,5 1119303", "kondenser contasında kablo lastiği"))
    # 4 evaporatör fanı → en yakın kolon kanalının yan yüzü (evaporatörün üstünden arkaya)
    BOLGE_B = (740.0, 4028.0, 125.0, 786.0, -828.5, -560.0)
    for i, (nm, S, xk, yk) in enumerate((("fan_sol_1", (1783.5, 509.5, -628.5), 1683.5, 668.0), ("fan_sol_2", (1963.5, 509.5, -628.5), 2298.5, 620.0),
                                         ("fan_sag_1", (3093.5, 422.0, -628.5), 2993.5, 520.0), ("fan_sag_2", (3273.5, 422.0, -628.5), 3608.5, 520.0))):
        sg = 1.0 if S[0] > xk else -1.0
        cihaz("DOLAP_evap_%s" % nm, S, (xk + sg * 0.2, yk, -777.0), 2.5, "B", itme=(1, 6.0), on=(xk + sg * 30.0, yk, -777.0), bolge=BOLGE_B,
              bom=("Fan kablosu 2 × 0,5 (4414 FL 24 V DC → kolon kanalı)", 4, "Lapp ÖLFLEX CLASSIC 110 2X0,5 1119752", "Ø 4,8") if i == 0 else None)
    return RAPOR
