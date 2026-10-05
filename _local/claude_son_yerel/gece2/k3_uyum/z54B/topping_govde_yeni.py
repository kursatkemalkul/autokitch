# -*- coding: utf-8 -*-
"""TOPPING İSTASYONU GÖVDESİ — BAŞTAN, TEMİZ, ÜRETİME YÖNELİK (Kemal 2 Eki · 7 madde, resim 67–73).
Taban hat3_v8n.glb → hat3_v8o.glb. Montaj / elektrik ÇALIŞTIRILMAZ: GLB düğüm geometrisi yerinde değiştirilir (silinen parça üçgenleri
dejenere edilir, yeni parçalar düğüme eklenir · 'kat'/'mek' etiketleri İNDİS sayısıyla, aynı düğümdeki referans parçadan kopya ·
kapak parçaları 'kpk' aralığına eklenir).

KURGU
  1 (67) ÖN DÜZLEM = KAPAK ARKASI z 39: yalıtım (PU) kapağın hemen arkasına kadar öne geldi (23 → 38); önünde TEK PARÇA ön çerçeve 430 1,0
     (z 38–39, soğuk oda ağzı 1496–2440 × 1152–2140 + kaset dili kanalları + mekanizma bandı açıklığı). Eski 23–39 arası 16 mm'lik
     boşluk, eski çerçeve sacı (kapakla gizlenen) ve yan sacların 30 mm'lik dönüş şeritleri KALKTI. PU'nun her yüzü sac / astar / çerçeve /
     gömülü elemana dayanır (yerinde köpük; kalıp = saclar). Astar, raf ve alt sac ön kenarları 38'e uzadı; raf ön büküm 35–38.
     Flipper (orta katlanır dikme) + kılavuzu +15 öne (ön yüzü 39 düzleminde, fitil ona da oturur).
  2 (68) TAVAN TEK SAC: kuru bölme servis kapağı (kapak gibi gizleniyordu → üst açık görünüyordu) kalktı; kuru bölmenin üstünde lazer
     hava çıkış yarıkları (5 × 70). Kuru bölmeye servis = sökülür arka sac (yan/arka servis panelinde bombe başlı vida izinli).
  3 (69) EVAPORATÖR HAVA IZGARALARI ayrı parça değil: astar arka duvarının iki penceresi yerine aynı yerde astara lazer yarık; fanlar arkada
     (kaset içinde, değişmedi). Kanat alt bandındaki hava yolu da doğrudan kanat sacında lazer yarık (ayrı panjur yok).
  4 (70) KANAT TEK DÜZ PARÇA 788 → 2197, z 39–79 boydan boya: alttaki 59'a çekilmiş kademe / mekanizma kanadı kalıntıları kalktı.
     Çift cidar (dış tava 1,5 + iç tava 1,0), üstte PU (1109'dan yukarı, köpük perdesiyle), altta boş tava + kaide ön pencereleri hizasında
     yarık + K1'de kondenser emiş filtresi (8 mm keçe). Fitil kanat içinde kanalda (yüzü 39'da, gövde çerçevesine basar).
  5 (71) MEKANİZMA BANDI ÇERÇEVE PROFİLLERİ (yan / orta dikmeler, alt / üst kayıt, menteşe tabanları, omega, bas-aç kalıntıları) KALKTI.
     Menteşeler gizli 180°, 3 adet / kanat, gövde yarısı yan duvar önünde (opak), kanat yarısı kanat içinde.
  6 (72) TEKNİK BÖLME (alt arka): soğutma grubu ASKILARI + TEPSİ + KÖŞE PERDESİ + 4 ped kalktı → kaide gözüne inen KAPALI CEP (304 1,5 bükümlü
     tava, taban 806) + 4 standart titreşim takozu: grup doğrudan cebin tabanına oturur. Cebin sol duvarı alt kısımda emiş ızgarası (lazer
     yarık), üstte teknik bölme ayırma perdesi = TEK SAC. Taban sacındaki büyük hava delikleri yerine kaide gözleri üstünde lazer yarık
     alanları (alt kapalı görünür). "Soldaki kutu" = kondenser EMİŞ FİLTRESİ (arka pencerede) → işlevli, KORUNDU.
  7 (73) KURU BÖLME (arka): 4 kaset motoru kablosu zikzak yerine yatay KD3 kablo kanalında (40 × 30 PVC, arka sacta 3 braket) toplanır,
     sürücülere dik yükselir · soğutma grubu kablosu G2'den düz yukarı, sos silindiri ile evaporatör kaseti arasından pano altına (2 P-kelepçe)
     · evaporatör tahliye hortumu kaset çıkışından DÜZ aşağı yoğuşma tavasına (kuru bölme tabanında yeni Ø14 geçiş) · eski kelepçeler kalktı.
DEĞİŞMEYEN: dış zarf x 1436–2500 · y 892–2200 (kanat 788) · z −830…+79 · kaset / UNO / tabla mekanizması · soğutma grubu konumu ·
  evaporatör kaseti · rakor / kanal delikleri (eski konturlarla aynı) · komşu istasyonlar.
Kullanım: python topping_govde_yeni.py giris.glb cikis.glb"""
import os, sys, json, struct, pickle, time
import numpy as np
import cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tg"))
import tgeo as G
from glbx import yukle as glb_yukle
from dikis import kati

PK = r"C:/Users/Kemal/AppData/Local/Temp/claude/C--Users-Kemal-Desktop-Kemal-WEBS-TE/f3ef876a-f062-4b29-bb81-775cc8a1a6d8/scratchpad/gece2/k3_uyum/z54B/_v7/parca_kutulari.json"
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}

# ---------------------------------------------------------------- silinecek (düğüm → etiketler)
SIL = {
    "TOPPING_MODUL__sac": ["?6", "?7", "teknik_bolme_ayirma_perdesi", "sogutma_grubu_askisi_0", "sogutma_grubu_askisi_1", "sogutma_grubu_cep_perdesi",
                           "sogutma_grubu_tepsisi"],
    "TOPPING_MODUL__silikon": ["sogutma_grubu_pedi_%d" % i for i in range(4)] + ["evap_kaseti_tahliye_hortumu"],
    "TOPPING_MODUL__celik": ["?41", "onyuz_cerceve_mek_orta_dikme_alt", "onyuz_cerceve_mek_orta_dikme_ust"] +
                            ["onyuz_mekanizma_kanadi_%s_mentese_%d_taban" % (a, i) for a in ("sol", "sag") for i in (0, 1)],
    "TOPPING_MODUL__on_seffaf": ["onyuz_K1_dis_sac", "onyuz_K2_dis_sac", "onyuz_K1_fitil", "onyuz_K2_fitil", "onyuz_K1_mentese_0", "onyuz_K1_mentese_1",
                                 "onyuz_K2_mentese_0", "onyuz_K2_mentese_1", "onyuz_basac_K1", "onyuz_basac_K2", "onyuz_soguk_cerceve_saci"] +
                                ["onyuz_mekanizma_kanadi_%s_%s" % (a, b) for a in ("sol", "sag") for b in ("mentese_0", "mentese_1", "omega")] +
                                ["onyuz_mekanizma_kanadi_sol_filtre"],
    "TOPPING_MODUL__plastik": ["onyuz_mekanizma_kanadi_sol_basac", "onyuz_mekanizma_kanadi_sag_basac"],
    "TOPPING_MODUL__paslanmaz": ["onyuz_mentese_tabani_K%d_mentese_%d" % (k, i) for k in (1, 2) for i in (0, 1)] +
                                ["arka_hava_izgarasi_alt", "arka_hava_izgarasi_ust"],
    "TOPPING_MODUL__yalitim_gorunur": ["yalitim_blogu", "alt_yalitim_PU"],
    "TOPPING_MODUL__pom": ["?18"],
    "TOPPING_MODUL__pu": ["kaset_penceresi_dolgusu"],
    "ELK_TOPPING__kablo": ["kablo_TOPPING_motor_sucuk_rotor_surucu_0", "kablo_TOPPING_motor_sucuk_helezon_surucu_1",
                           "kablo_TOPPING_motor_kasar_rotor_surucu_2", "kablo_TOPPING_motor_kasar_helezon_surucu_3", "kablo_TOPPING_sogutma_grubu_KLF66"],
    "ELK_TOPPING__celik": ["kablo_TOPPING_motor_sucuk_rotor_surucu_0_kelepce_0", "kablo_TOPPING_motor_sucuk_helezon_surucu_1_kelepce_0",
                           "kablo_TOPPING_motor_sucuk_helezon_surucu_1_kelepce_1", "kablo_TOPPING_motor_kasar_rotor_surucu_2_kelepce_0",
                           "kablo_TOPPING_motor_kasar_helezon_surucu_3_kelepce_0", "kablo_TOPPING_motor_kasar_helezon_surucu_3_kelepce_1",
                           "kablo_TOPPING_sogutma_grubu_KLF66_kelepce_0"],
}
# ---------------------------------------------------------------- yerinde uzatma / öteleme (eski ağ korunur)
UZAT = [("TOPPING_MODUL__paslanmaz", "soguk_ic_kaplama", 2, {23.0: 38.0}),               # astar yan + tavan duvarları → 38 (raf / büküm / köşebent yerinde; önüne eşik)
        ("TOPPING_MODUL__paslanmaz", "?0", 2, {23.0: 38.0})]                              # soğuk oda alt sacı ön kenarı → 38
OTELE = [("TOPPING_MODUL__on_seffaf", p, (0.0, 0.0, 15.0)) for p in ("?13", "onyuz_flipper_pimi", "onyuz_K1_flipper_mentese_0",
                                                                     "onyuz_K1_flipper_mentese_1", "onyuz_K1_flipper_mentese_2")] + \
        [("TOPPING_MODUL__pom", "onyuz_kilavuz_flipper", (0.0, 0.0, 15.0))]
# evaporatör ızgaraları kalkınca astar arka duvarına aynı pencerelerde lazer yarık (astar ağına delik açılamaz → arka duvar şeridi yeniden)
IZGARA = [(1729.0, 2103.0, 1453.0, 1569.0), (1729.0, 2103.0, 1595.0, 1699.0)]
KANAL_PEN = [(1726.0, 2106.0, 1450.0, 1572.0), (1726.0, 2106.0, 1592.0, 1702.0)]   # astardaki eski kanal pencereleri (ızgara çerçevesinin arkası)


def segment(J, D, birimler):
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    P = json.load(open(PK, encoding="utf-8"))["parca"]
    R = {}
    for ad, d in D.items():
        b = ad.split("__")[0]
        if b not in birimler: continue
        X, T, ok = d["X"], d["T"], d["ok"]
        _, inv = np.unique(np.round(X / 0.02).astype(np.int64), axis=0, return_inverse=True); inv = inv.ravel()
        TT = inv[T]; idx = np.where(ok)[0]; nv = inv.max() + 1
        g = coo_matrix((np.ones(2 * len(idx)), (np.concatenate([TT[idx, 0], TT[idx, 1]]), np.concatenate([TT[idx, 1], TT[idx, 2]]))), shape=(nv, nv))
        _, lab = connected_components(g, directed=False)
        tl = np.full(len(T), -1); tl[idx] = lab[TT[idx, 0]]
        kut = [(p[0], np.array(p[2:8], float)) for p in P.get(b, [])]
        vol = [max(k[1] - k[0], .01) * max(k[3] - k[2], .01) * max(k[5] - k[4], .01) for _, k in kut]
        at = np.array([""] * len(T), dtype=object)
        for cc in np.unique(tl[idx]):
            ti = np.where(tl == cc)[0]; Q = X[T[ti]].reshape(-1, 3); mn, mx = Q.min(0), Q.max(0); e = 0.35
            best, bv = None, 1e30
            for j, (pa, k) in enumerate(kut):
                if (mn >= k[0::2] - e).all() and (mx <= k[1::2] + e).all() and vol[j] < bv: bv, best = vol[j], pa
            at[ti] = best if best else "?%d" % cc
        R[ad] = at
    return R


def etiket_degeri(lst, tri):
    i = tri * 3
    for k in range(0, len(lst), 3):
        if lst[k + 1] <= i < lst[k + 1] + lst[k + 2]: return lst[k]
    return lst[-3] if lst else 0


def ag(solidler):
    P, I = [], []
    for s in solidler:
        for f in s.Faces():
            v, t = f.tessellate(0.1, 0.2)
            o = sum(len(p) for p in P)
            P.append(np.array([[q.x, q.y, q.z] for q in v], float))
            I.append(np.array(t, np.int64) + o if len(t) else np.zeros((0, 3), np.int64))
    X = np.vstack(P); T = np.vstack(I)
    Xf = X[T.reshape(-1)]; n = np.cross(Xf[1::3] - Xf[0::3], Xf[2::3] - Xf[0::3])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return Xf, np.repeat(n, 3, axis=0)


def yap(gi, go, cikti_dir):
    t0 = time.time()
    J, D = glb_yukle(gi)
    R = segment(J, D, ["TOPPING_MODUL", "ELK_TOPPING"])
    print("bölütleme %.0f s" % (time.time() - t0))
    # ------------------------------------------------ eski ağdan katı (gömülü elemanlar · uzatılan alt PU · astar arka şeridi)
    def lab_kati(nd, lab, uz=None):
        d = D[nd]; X = d["X"].copy(); T = d["T"][d["ok"] & (R[nd] == lab)]
        if uz:
            ax, mp = uz; used = np.unique(T.ravel())
            for a, b in mp.items():
                sel = used[np.abs(X[used, ax] - a) < 0.02]; X[sel, ax] = b
        ss = kati(X, T)
        return ss
    YENI = []                                         # (ad, katı, düğüm, referans etiket, kpk)
    def ekle(dct, nd, ref, kpk=False):
        for k, s in dct.items(): YENI.append((k, s, nd, ref, kpk))
    # 1 · dış kabuk · teknik · cep
    ekle(G.dis_kabuk(), "TOPPING_MODUL__sac", "?6")
    ekle(G.teknik(), "TOPPING_MODUL__sac", "?7")
    S_cep, A_cep = G.cep()
    ekle(S_cep, "TOPPING_MODUL__sac", "sogutma_grubu_tepsisi")
    ekle(A_cep, "TOPPING_MODUL__silikon", "sogutma_grubu_pedi_0")
    # 2 · menteşe / bas-aç + ön çerçeve
    MG, MK = G.menteseler()
    ekle(MG, "TOPPING_MODUL__paslanmaz", "?0")
    ekle(MK, "TOPPING_MODUL__on_seffaf", "onyuz_K1_dis_sac", kpk=True)
    ekle({"onyuz_on_cerceve_430": G.on_cerceve(MG)}, "TOPPING_MODUL__paslanmaz", "?0")
    # 3 · kanatlar (cepler: menteşe/bas-aç kanat yarıları + flipper menteşeleri yeni yerinde)
    fm = []
    for i in range(3):
        d = D["TOPPING_MODUL__on_seffaf"]; T = d["T"][d["ok"] & (R["TOPPING_MODUL__on_seffaf"] == "onyuz_K1_flipper_mentese_%d" % i)]
        Q = d["X"][T].reshape(-1, 3); mn, mx = Q.min(0), Q.max(0)
        fm.append(G.kutu(mn[0] - 1.0, mx[0] + 1.0, mn[1] - 1.0, mx[1] + 1.0, mn[2] + 15.0, mx[2] + 15.0 + 1.0))
        cup = G.kutu(mn[0] - 1.0, mx[0] + 1.0, mn[1] - 1.0, mx[1] + 1.0, G.ZK0 + 1.0, mx[2] + 15.0 + 1.0).cut(
            G.kutu(mn[0], mx[0], mn[1], mx[1], G.ZK0, mx[2] + 15.0))
        ekle({"onyuz_K1_flipper_mentese_cebi_%d" % i: G.tekle(cup)}, "TOPPING_MODUL__on_seffaf", "onyuz_K1_dis_sac", kpk=True)
    for kn in ("K1", "K2"):
        ekle(G.kanat(kn, list(MK.values()) + fm), "TOPPING_MODUL__on_seffaf", "onyuz_%s_dis_sac" % kn, kpk=True)
    # 4 · PU: duvar (yeni, gömülü elemanlar düşülür) + alt PU (eski ağ, öne uzatıldı)
    pu_kutu = (G.XI0, G.XI1, G.LIN[2], G.YTI, G.Z_SA + G.T_D, G.ZFC)
    gomulu, gom_ad = [], []
    for nd in [n for n in D if n.startswith("TOPPING_MODUL")]:
        if nd not in R: continue
        d = D[nd]; X, T, ok = d["X"], d["T"], d["ok"]; L = R[nd]
        for lab in set(L[ok]):
            if (nd, lab) in [("TOPPING_MODUL__paslanmaz", "soguk_ic_kaplama"), ("TOPPING_MODUL__paslanmaz", "?0")]: continue
            if lab in SIL.get(nd, []): continue
            Q = X[T[ok & (L == lab)]].reshape(-1, 3); mn, mx = Q.min(0), Q.max(0)
            if not G._kesisir_bb((mn[0], mx[0], mn[1], mx[1], mn[2], mx[2]), pu_kutu, 0.05): continue
            if mn[0] >= G.LIN[0] - 0.01 and mx[0] <= G.LIN[1] + 0.01 and mx[1] <= G.LIN[3] + 0.01 and mn[2] >= G.LIN[4] - 0.01: continue   # astar kutusunun içi/altı
            ot = [o for o in OTELE if o[0] == nd and o[1] == lab]
            XX = X.copy()
            if ot: XX = XX + np.array(ot[0][2])
            import trimesh                                                   # gömülü eleman = her bileşenin dış zarfı (dışbükey örtü): kovan / burç delikleri PU ile dolmaz
            tm = trimesh.Trimesh(XX[T[ok & (L == lab)]].reshape(-1, 3), np.arange(3 * int((ok & (L == lab)).sum())).reshape(-1, 3))
            tm.merge_vertices(digits_vertex=3)
            ss = []
            for comp in tm.split(only_watertight=False):
                hull = comp.convex_hull
                ss += kati(np.asarray(hull.vertices), np.asarray(hull.faces))
            gomulu += ss; gom_ad.append("%s|%s" % (nd, lab))
    for g in MG.values(): gomulu.append(g)
    gomulu.append(G.pencere_prizma(-640.0, -570.0))                     # evaporatör penceresi (kendi tapası var)
    print("PU gömülü eleman: %d (%s)" % (len(gom_ad), ", ".join(sorted(gom_ad))))
    pu = G.pu_duvar(gomulu)
    if G.pu_duvar.bas: print("  UYARI PU kutu ile düşüldü:", G.pu_duvar.bas)
    alt = lab_kati("TOPPING_MODUL__yalitim_gorunur", "alt_yalitim_PU")
    TK, TKD = G.taban_kovanlari()
    alt = [G.tekle(a.cut(*TKD)) for a in alt]
    ES, EP = G.esik()
    ekle(ES, "TOPPING_MODUL__paslanmaz", "soguk_ic_kaplama")
    ekle(EP, "TOPPING_MODUL__pu", "kaset_penceresi_dolgusu")
    ekle(TK, "TOPPING_MODUL__paslanmaz", "soguk_ic_kaplama")
    alt = [a.cut(*[s for s in gomulu if G._kesisir_bb(G._bb(s), G._bb(a))]) if any(G._kesisir_bb(G._bb(s), G._bb(a)) for s in gomulu) else a for a in alt]
    ekle({"soguk_oda_PU_duvar": pu}, "TOPPING_MODUL__pu", "kaset_penceresi_dolgusu")
    ekle({"soguk_oda_PU_alt_%d" % i: a for i, a in enumerate(alt)}, "TOPPING_MODUL__pu", "kaset_penceresi_dolgusu")
    # 5 · evaporatör penceresi tapası: ayrı ızgara + POM kanal bloğu + açık PU dolgusu yerine sandviç tapa (ön sacta lazer yarık)
    PS, PP = G.evap_penceresi()
    ekle(PS, "TOPPING_MODUL__paslanmaz", "soguk_ic_kaplama")
    ekle(PP, "TOPPING_MODUL__pu", "kaset_penceresi_dolgusu")
    # 6 · kuru bölme düzeni
    K, C, Rk, H = G.kuru_duzen()
    ekle(K, "ELK_TOPPING__kablo", "kablo_TOPPING_motor_sucuk_rotor_surucu_0")
    ekle(C, "ELK_TOPPING__celik", "kablo_TOPPING_sogutma_grubu_KLF66_kelepce_0")
    ekle(Rk, "ELK_TOPPING__kanal", "kanal_TOPPING_KD1_dikey")
    ekle(H, "TOPPING_MODUL__silikon", "evap_kaseti_tahliye_hortumu")
    print("yeni katı: %d · %.0f s" % (len(YENI), time.time() - t0))
    # ------------------------------------------------ GLB yazımı
    raw = open(gi, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]; JJ = json.loads(raw[20:20 + jl]); bo = 20 + jl
    bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])

    def oku(i):
        a = JJ["accessors"][i]; v = JJ["bufferViews"][a["bufferView"]]; n = {"SCALAR": 1, "VEC3": 3}[a["type"]]; dt = TD[a["componentType"]]
        off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
        r = np.frombuffer(bytes(BIN[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt).copy()
        return r.reshape(-1, n) if n > 1 else r

    def ekle_buf(arr, tip, hedef):
        while len(BIN) % 4: BIN.extend(b"\0")
        off = len(BIN); BIN.extend(arr.tobytes())
        JJ["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
        a = {"bufferView": len(JJ["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
        if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
        JJ["accessors"].append(a); return len(JJ["accessors"]) - 1

    rapor = dict(silinen=[], uzatilan=[], otelenen=[], yeni=[])
    dugumler = sorted(set(list(SIL) + [u[0] for u in UZAT] + [o[0] for o in OTELE] + [y[2] for y in YENI]))
    for nd in dugumler:
        node = [n for n in JJ["nodes"] if n.get("name") == nd][0]
        tr = np.array(node.get("translation", [0, 0, 0]), float)
        assert not any(k in node for k in ("rotation", "scale", "matrix")), nd
        pr = JJ["meshes"][node["mesh"]]["primitives"][0]
        X = oku(pr["attributes"]["POSITION"]).astype(np.float64); N = oku(pr["attributes"]["NORMAL"]).astype(np.float32)
        I = oku(pr["indices"]).astype(np.uint32); T = I.reshape(-1, 3).copy()
        Xw = (X + tr) * 1000.0
        L = R[nd]
        ex = pr.setdefault("extras", {})
        refdeg = {}
        for _a, _s, n2, ref, _k in YENI:
            if n2 == nd and ref not in refdeg:
                ti = np.where(L == ref)[0]
                assert len(ti), (nd, ref)
                refdeg[ref] = {k: etiket_degeri(ex.get(k, []), int(ti[0])) for k in ("kat", "mek")}
        for lab in SIL.get(nd, []):
            m = (L == lab) & ((T[:, 0] != T[:, 1]) | (T[:, 1] != T[:, 2]))
            if not m.any(): print("  UYARI silinecek yok:", nd, lab); continue
            T[m, 1] = T[m, 0]; T[m, 2] = T[m, 0]; rapor["silinen"].append([nd, lab, int(m.sum())])
        for n2, lab, ax, mp in UZAT:
            if n2 != nd: continue
            TL = T[(L == lab) & ((T[:, 0] != T[:, 1]) | (T[:, 1] != T[:, 2]))]
            if lab == "soguk_ic_kaplama":                                # yalnız astar duvarları (taban bandı y ≤ 1152,5 = raf / büküm / köşebent yerinde)
                ust = Xw[TL][:, :, 1].max(1) > 1152.5
                ortak = np.intersect1d(np.unique(TL[ust].ravel()), np.unique(TL[~ust].ravel()))
                if len(ortak): print("  UYARI astar/raf ortak köşe:", len(ortak))
                TL = TL[ust]
            used = np.unique(TL.ravel())
            for a, b in mp.items():
                sel = used[np.abs(Xw[used, ax] - a) < 0.02]; Xw[sel, ax] = b
                rapor["uzatilan"].append([nd, lab, "xyz"[ax], a, b, int(len(sel))])
        for n2, lab, dv in OTELE:
            if n2 != nd: continue
            used = np.unique(T[L == lab].ravel()); Xw[used] += np.array(dv); rapor["otelenen"].append([nd, lab, list(dv), int(len(used))])
        Xn = (Xw / 1000.0 - tr).astype(np.float32)
        I0 = T.reshape(-1).astype(np.uint32)
        yeniler = [(a, s, ref, k) for a, s, n2, ref, k in YENI if n2 == nd]
        Xa, Na, Ia = [Xn], [N], [I0]
        say = len(Xn); ek_kat = {"kat": [], "mek": []}; ek_kpk = []
        for a, s, ref, kp in yeniler:
            Xf, Nf = ag([s])
            Xa.append((Xf / 1000.0 - tr).astype(np.float32)); Na.append(Nf.astype(np.float32))
            n_ = len(Xf); Ia.append(np.arange(say, say + n_, dtype=np.uint32))
            bas = sum(len(i) for i in Ia[:-1])
            for k in ("kat", "mek"): ek_kat[k].append([refdeg[ref][k], bas, n_])
            if kp: ek_kpk.append([bas, n_])
            say += n_
            bb = G._bb(s)
            rapor["yeni"].append([nd, a, [round(v, 1) for v in bb], n_ // 3])
        Xall = np.vstack(Xa); Nall = np.vstack(Na); Iall = np.concatenate(Ia)
        pr["attributes"] = {"POSITION": ekle_buf(Xall, "VEC3", 34962), "NORMAL": ekle_buf(Nall, "VEC3", 34962)}
        pr["indices"] = ekle_buf(Iall, "SCALAR", 34963)
        for k in ("kat", "mek"):
            if ex.get(k) is not None:
                for e in ek_kat[k]: ex[k] = list(ex[k]) + e
        if ek_kpk:
            ex["kpk"] = list(ex.get("kpk", [])) + [v for e in ek_kpk for v in e]
        print("  %-30s sil %5d üçgen · +%d parça (%d üçgen)" % (nd, sum(r[2] for r in rapor["silinen"] if r[0] == nd), len(yeniler),
                                                           sum(r[3] for r in rapor["yeni"] if r[0] == nd)))
    JJ["buffers"][0]["byteLength"] = len(BIN)
    jb = json.dumps(JJ, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
    while len(BIN) % 4: BIN.extend(b"\0")
    open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
                         + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
    # denetim girdileri: yeni katılar BREP + dizin · gömülü eleman listesi
    os.makedirs(cikti_dir, exist_ok=True)
    comp = cq.Compound.makeCompound([s for _a, s, _n, _r, _k in YENI])
    comp.exportBrep(os.path.join(cikti_dir, "yeni_katilar.brep"))
    json.dump(dict(yeni=[[a, n, r, k] for a, _s, n, r, k in YENI], gomulu=gom_ad, rapor=rapor, sil=SIL, uzat=[[u[0], u[1], u[2], {str(k): v for k, v in u[3].items()}] for u in UZAT],
                   otele=OTELE), open(os.path.join(cikti_dir, "yeni_dizin.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("yazıldı %s · %.0f s" % (go, time.time() - t0))


if __name__ == "__main__":
    yap(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "tg", "cikti"))
    sys.stdout.flush(); os._exit(0)
