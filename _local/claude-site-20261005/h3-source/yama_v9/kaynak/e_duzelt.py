# -*- coding: utf-8 -*-
"""E (KUTU KATLAMA) — KEMAL'İN 7 MADDESİ (2 Eki akşam) · hat3_v8r.glb → hat3_v8s.glb (yalnız E düğümleri; montaj / elektrik derlemesi YOK)
DÜNYA koordinatı (mm): x hat boyunca · y yukarı · z koridora (ön +79, arka −830).

1 + 7  ŞARJÖR YAN KAPISI (sağ sac, açıklık 231–989 × −823…−411)
   NEDEN İSTASYONDA GÖRÜNMÜYORDU: kapı + 2 menteşe + bas-aç GLB'de 'kpk' (kapak takımı) etiketliydi → mekanizma-v3.js "Ön kapaklar" kaydırıcısı
   tam soldayken (istasyon görünümünde ön kapaklar kapalı) kpk üçgenlerini GİZLİYOR → yan kapı da kayboluyor, açıklıktan arkadaki sağ kılavuz
   (beyaz UHMW + ortadaki dikey taşıyıcı çıtası + üst/alt kayıtları) "kapak" gibi görünüyordu. → kpk etiketi KALDIRILDI (yan kapı ön kapak değil,
   gövdeyle birlikte hep görünür).
   KAPI: dış sac 304 1,5 · x 5228,5–5230 (yan sacla AYNI YÜZEY, lazer kesim açıklıktan çıkan parça, çevrede 3 mm derz) + İÇ TAVA 304 1,5
   (taban x 5215,5–5217 · y 236–984 · z −812…−420 + dört kenar dönüşü dış saca punta) → çift cidar, dışta vida / çıta yok.
   Sağ UHMW kılavuz (3 mm) iç tavaya havşa vidalı → kapı açılınca yığının sağ yanı açılır (yan yükleme, eski karar aynı).
   Gizli menteşe (2) + bas-aç (1) içte, eski yerinde (tava kenarları menteşeden 2 mm, bas-aç'tan 2 mm geri).
3  ŞARJÖR KILAVUZ KAFESİ ("kutu"): taşıyıcılar KALKTI — sol taşıyıcı çıta (20 × 3, z −700…−680) · sağ taşıyıcı (dikey çıta + üst/alt kayıt,
   kapı açıklığında görünen) · arka taşıyıcı (6 mm dolu levha 724 × 728). Yerine UHMW-PE levhalar DOĞRUDAN sacа (PEM saplama, dışta vida yok):
   sol 6 mm (x 4401,5–4407,5, sol saca) · arka 9 mm (z −828,5…−819,5, x 4417–5212, arka saca; sol sacın arka bükümünü geçer) · sağ 3 mm (kapı tavasına).
   Kılavuz yüzleri DEĞİŞMEDİ (sol 4407,5 · sağ 5212,5 · arka −819,5) → yığın / asansör / eşik aynı.
5 + 6  DİKEY KABLO KANALI (E_ELEKTRIK__plastik, x 5206–5226 · y 126–1827 · z −50…−25) + 3 tutturma pabucu KALKTI: içinde kablo yok, üstü
   pano kanallarına bağlanmıyor (−50'de bitiyor, pano −822'de), Elektrik görünümünde gövde gizlenince hattın dışında çubuk gibi duruyordu.
Kullanım: python e_duzelt.py hat3_v8r.glb hat3_v8s.glb"""
import os, sys, json, struct
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import e_govde_yeni as EG

kutu, bir = EG.kutu, EG.bir
XI1, X1 = EG.XI1, EG.X1                      # 5228,5 · 5230
SAC_KPK_DISI = ("sarjor_yan_kapisi", "sarjor_yan_kapisi_mentese_0", "sarjor_yan_kapisi_mentese_1", "sarjor_yan_kapisi_basac")

# ---------------------------------------------------------------- kapı (dış sac + iç tava)
TAVA = dict(x0=5215.5, x1=5217.0, y0=236.0, y1=984.0, z0=-812.0, z1=-420.0)
T = 1.5


def kapi():
    a = TAVA
    dis = kutu(XI1, X1, 234.0, 986.0, -820.0, -414.0)
    taban = kutu(a["x0"], a["x1"], a["y0"], a["y1"], a["z0"], a["z1"])
    don = [kutu(a["x1"], XI1, a["y0"], a["y0"] + T, a["z0"], a["z1"]), kutu(a["x1"], XI1, a["y1"] - T, a["y1"], a["z0"], a["z1"]),
           kutu(a["x1"], XI1, a["y0"] + T, a["y1"] - T, a["z0"], a["z0"] + T), kutu(a["x1"], XI1, a["y0"] + T, a["y1"] - T, a["z1"] - T, a["z1"])]
    return bir(dis, taban, *don)


_eski = EG.sarjor_kapisi


def sarjor_kapisi_yeni():
    _, M, kb = _eski()
    return kapi(), M, kb


EG.sarjor_kapisi = sarjor_kapisi_yeni
_kur = EG.kur


def kur_yeni():
    D, KPK = _kur()
    for a in SAC_KPK_DISI: KPK.discard(a)
    return D, KPK


EG.kur = kur_yeni


# ---------------------------------------------------------------- genel düğüm cerrahisi (üçgen başına etiket korunur)
class GLB:
    def __init__(s, yol):
        raw = open(yol, "rb").read()
        jl = struct.unpack("<I", raw[12:16])[0]; s.J = json.loads(raw[20:20 + jl]); bo = 20 + jl
        bl = struct.unpack("<I", raw[bo:bo + 4])[0]; s.BIN = bytearray(raw[bo + 8:bo + 8 + bl])

    def acc(s, i):
        a = s.J["accessors"][i]; v = s.J["bufferViews"][a["bufferView"]]
        n = {"SCALAR": 1, "VEC3": 3}[a["type"]]; dt = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        r = np.frombuffer(bytes(s.BIN[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt)
        return r.reshape(-1, n) if n > 1 else r

    def ekle(s, arr, tip, hedef):
        while len(s.BIN) % 4: s.BIN.extend(b"\0")
        off = len(s.BIN); s.BIN.extend(arr.tobytes())
        s.J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
        a = {"bufferView": len(s.J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
        if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
        s.J["accessors"].append(a); return len(s.J["accessors"]) - 1

    def dugum(s, ad):
        nd = [n for n in s.J["nodes"] if n.get("name") == ad][0]
        assert not any(k in nd for k in ("translation", "rotation", "scale", "matrix")), ad
        pr = s.J["meshes"][nd["mesh"]]["primitives"]; assert len(pr) == 1, ad
        return pr[0]

    def oku(s, ad):
        pr = s.dugum(ad)
        X = s.acc(pr["attributes"]["POSITION"]).astype(np.float64) * 1000.0
        N = s.acc(pr["attributes"]["NORMAL"]).astype(np.float32)
        I = s.acc(pr["indices"]).astype(np.int64).reshape(-1, 3)
        n = len(I); ex = pr.get("extras", {})
        lab = {}
        for k in ("kat", "mek"):
            a = np.full(n, -1, np.int64); r = ex.get(k, [])
            for i in range(0, len(r), 3): a[r[i + 1] // 3:(r[i + 1] + r[i + 2]) // 3] = r[i]
            lab[k] = a
        a = np.zeros(n, np.int64); r = ex.get("kpk", [])
        for i in range(0, len(r), 2): a[r[i] // 3:(r[i] + r[i + 1]) // 3] = 1
        lab["kpk"] = a
        return X, N, I, lab

    def yaz_dugum(s, ad, P, Nn, lab):
        """P (n,3,3) mm · Nn (n,3,3) · lab: kat/mek/kpk (n)"""
        pr = s.dugum(ad)
        Xf = (P.reshape(-1, 3) / 1000.0).astype(np.float32); Nf = Nn.reshape(-1, 3).astype(np.float32)
        pr["attributes"] = {"POSITION": s.ekle(Xf, "VEC3", 34962), "NORMAL": s.ekle(Nf, "VEC3", 34962)}
        pr["indices"] = s.ekle(np.arange(len(Xf), dtype=np.uint32), "SCALAR", 34963)
        ex = pr.setdefault("extras", {})

        def rle(a):
            out, i = [], 0
            while i < len(a):
                j = i
                while j < len(a) and a[j] == a[i]: j += 1
                out.append((int(a[i]), 3 * i, 3 * (j - i))); i = j
            return out
        for k in ("kat", "mek"):
            if k in ex: ex[k] = [v for t in rle(lab[k]) for v in t]
        ex["kpk"] = [v for (val, a, c) in rle(lab["kpk"]) if val == 1 for v in (a, c)]

    def kaydet(s, yol):
        s.J["buffers"][0]["byteLength"] = len(s.BIN)
        jb = json.dumps(s.J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
        while len(s.BIN) % 4: s.BIN.extend(b"\0")
        open(yol, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(s.BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
                              + struct.pack("<II", len(s.BIN), 0x004E4942) + bytes(s.BIN))


def kutuda(P, b, e=0.02):
    """BAĞLI BİLEŞEN bazında: kutunun tamamen içinde kalan bileşenlerin üçgenleri (komşu parçanın kutuya düşen yüzleri silinmez)"""
    lo = np.array(b[0::2]) - e; hi = np.array(b[1::2]) + e
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    _, inv = np.unique(np.round(P.reshape(-1, 3) / 0.01).astype(np.int64), axis=0, return_inverse=True); inv = inv.ravel().reshape(-1, 3)
    n = len(P); nv = inv.max() + 1
    g = coo_matrix((np.ones(3 * n), (np.repeat(np.arange(n), 3), inv.ravel())), shape=(n, nv)).tocsr()
    A = (g @ g.T)
    _, lab = connected_components(A, directed=False)
    ic = ((P >= lo) & (P <= hi)).all(axis=(1, 2))
    tam = np.zeros(lab.max() + 1, bool); tam[np.unique(lab[ic])] = True
    tam[np.unique(lab[~ic])] = False
    return tam[lab]


def etiket(G, ad, b):
    X, N, I, lab = G.oku(ad)
    m = kutuda(X[I], b); assert m.any(), (ad, b)
    v = {k: np.unique(lab[k][m]) for k in ("kat", "mek", "kpk")}
    assert all(len(x) == 1 for x in v.values()), (ad, b, v)
    return {k: int(x[0]) for k, x in v.items()}


def ameliyat(G, ad, sil_kutular, yeni=(), rapor=None):
    """sil_kutular: üçgenleri TAMAMEN içinde kalanlar silinir · yeni: [(isim, cq katı, {kat, mek, kpk})]"""
    X, N, I, lab = G.oku(ad)
    P = X[I]; Nn = N[I]
    sil = np.zeros(len(I), bool)
    for isim, b in sil_kutular:
        m = kutuda(P, b); assert m.any(), (ad, isim)
        sil |= m
        if rapor is not None: rapor.append("  − %-22s %-34s %4d üçgen · kutu %s" % (ad, isim, m.sum(), b))
    P = P[~sil]; Nn = Nn[~sil]; lab = {k: v[~sil] for k, v in lab.items()}
    for isim, s, et in yeni:
        Xn, Nnn, In, say = EG.ag([s])
        Pn = Xn.reshape(-1, 3, 3).astype(np.float64) * 1000.0; Nq = Nnn.reshape(-1, 3, 3)
        P = np.concatenate([P, Pn]); Nn = np.concatenate([Nn, Nq])
        for k in ("kat", "mek", "kpk"): lab[k] = np.concatenate([lab[k], np.full(len(Pn), et[k], np.int64)])
        if rapor is not None:
            bb = s.BoundingBox()
            rapor.append("  + %-22s %-34s %4d üçgen · kutu %s" % (ad, isim, len(Pn), [round(v, 1) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)]))
    G.yaz_dugum(ad, P, Nn, lab)


if __name__ == "__main__":
    gi, go = sys.argv[1:3]
    ara = os.path.join(HERE, "eg", "_v8s_ara.glb")
    print("1/2 E_GOVDE (e_govde_yeni + yeni kapı, yan kapı kpk dışı)")
    EG.yaz(gi, ara, os.path.join(HERE, "eg", "e_parca_kutulari_v8s.json"))
    print("2/2 E_SARJOR / E_ELEKTRIK düğüm cerrahisi")
    G = GLB(ara); R = []
    # şarjör taşıyıcıları
    ameliyat(G, "E_SARJOR__sac", [("kilavuz_sol_tasiyici", (4401.5, 4404.5, 244.0, 984.0, -700.0, -680.0)),
                                  ("kilavuz_sag_tasiyici", (5215.5, 5228.5, 235.5, 984.5, -819.0, -415.0)),
                                  ("kilavuz_arka_tasiyici", (4448.0, 5172.0, 244.0, 972.0, -828.5, -822.5))], rapor=R)
    # UHMW kılavuzlar (sağ aynı · sol 6 · arka 9)
    _, _, _, lu = G.oku("E_SARJOR__uhmw")
    et = dict(kat=int(lu["kat"][0]), mek=int(lu["mek"][0]), kpk=0)
    ameliyat(G, "E_SARJOR__uhmw", [("kilavuz_sol_uhmw (3)", (4404.5, 4407.5, 244.0, 984.0, -819.0, -415.0)),
                                   ("kilavuz_arka_uhmw (3)", (4408.0, 5212.0, 244.0, 972.0, -822.5, -819.5))],
             [("kilavuz_sol_uhmw_6", kutu(4401.5, 4407.5, 244.0, 984.0, -819.0, -415.0), et),
              ("kilavuz_arka_uhmw_9", kutu(4417.0, 5212.0, 244.0, 972.0, -828.5, -819.5), et)], rapor=R)
    # asansör iç çakışmaları (madde 2 / 6 · denetimde bulundu, v8r'de de vardı)
    #   çatallar araba plakasının içinden 4 mm geçiyordu → plakanın arka yüzünde (z −410) biter, alın kaynağı
    #   trapez vida Ø16 üst yatağın Ø12 deliğine 2 mm giriyordu → vida 945'e kadar Ø16, 945–957 işlenmiş Ø12 muylu (alt uçtaki gibi) · modelde Ø15,8 / Ø11,6 (yüzey ağı payı)
    CAT = ((4590.0, 4620.0), (4785.0, 4815.0), (4980.0, 5010.0))
    VIDA = (4797.0, 4813.1, 153.0, 957.0, -400.1, -383.9)
    ec = etiket(G, "E_SARJOR__celik", (CAT[0][0], CAT[0][1], 229.0, 237.0, -819.0, -406.0))
    ev = etiket(G, "E_SARJOR__celik", VIDA)
    vida = bir(EG.sil("y", (4805.0, 0, -392.0), 7.9, 153.0, 945.0), EG.sil("y", (4805.0, 0, -392.0), 5.8, 945.0, 957.0))   # somun deliği Ø16,4 · yatak Ø12: tess payı
    ameliyat(G, "E_SARJOR__celik", [("asansor_catali_%d" % i, (a, b, 229.0, 237.0, -819.0, -406.0)) for i, (a, b) in enumerate(CAT)] +
             [("asansor_vidasi_Tr16x4", VIDA)],
             [("asansor_catali_%d (z −410)" % i, kutu(a, b, 229.0, 237.0, -819.0, -410.0), ec) for i, (a, b) in enumerate(CAT)] +
             [("asansor_vidasi_Tr16x4 + Ø12 muylu", vida, ev)], rapor=R)
    # dikey kablo kanalı + pabuçları
    ameliyat(G, "E_ELEKTRIK__plastik", [("kablo_kanali_dikey", (5206.0, 5226.0, 126.0, 1827.0, -50.0, -25.0)),
                                        ("kanal_pabucu_1240", (5226.0, 5228.5, 1240.0, 1260.0, -45.0, -30.0)),
                                        ("kanal_pabucu_1490", (5226.0, 5228.5, 1490.0, 1510.0, -45.0, -30.0)),
                                        ("kanal_pabucu_1750", (5226.0, 5228.5, 1750.0, 1770.0, -45.0, -30.0))], rapor=R)
    G.kaydet(go)
    os.remove(ara)
    print("\n".join(R))
    print("yazıldı", go)
    sys.stdout.flush(); os._exit(0)
