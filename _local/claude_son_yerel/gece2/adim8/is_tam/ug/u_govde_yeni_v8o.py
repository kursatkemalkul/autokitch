# -*- coding: utf-8 -*-
"""U_F + U_KE ÜST DEPO GÖVDELERİ — BAŞTAN, TEMİZ, ÜRETİME YÖNELİK (Kemal 2 Eki: "üst dolaplara bak"; A / B / TOPPING ile aynı ölçüt).
v3.7'de kapaklar birleşti (fırın üstü 2 düşer kapak 1308–2197 · K tek kapak 788–2197 · E üst kapaklar 788–2197) → U_F / U_KE'nin KENDİ ön kapağı
ve menteşesi yok; önleri alttaki istasyon kapaklarıyla kapanır. Bu yüzden ön kayıt profilleri (30 × 30 × 2, düşer kapak menteşe taşıyıcısı +
tavan ön kenarı) görevsiz kaldı → kalkar; ön çerçeve sacın kendi bükümüyle kurulur.

KURGU (her kutu x0–x1 · y 1862–2200 · z −830…+59; içerik / komşular değişmez):
  TABAN 304 1,5   y 1862–1863,5 · z −828,5…+59 · ÖN KENARI 30 YUKARI BÜKÜLÜ (y 1863,5–1893,5 · z 57,5–59, yan sac ön bükümleri arası) = eski alt kayıt
                  profili yerine; raf üstü 1895 > büküm üstü 1893,5 → koli / kutu düz çekilir. U_F'de baca açıklığı 300 × 200 (kanal dış ölçüsü).
                  İstasyon tavanına (F üst kabin / K / E, üstü 1862) DOĞRUDAN oturur: çift sac, arada boşluk yok (U ayrı taşınan kapalı ürün).
                  U_KE'de K ve E Harting soket ağızları 66 × 36 (istasyon tavanındaki ağızla birebir · x 4267–4333 / 5067–5133 · z −778…−742).
  YAN SAC 304 1,5 (2) y 1863,5–2198,5 · 15 mm ön + arka iç büküm (değişmedi) · U_F'de bas-aç Ø10 deliği ön bükümde (F kapaklarının bas-açı) ·
                  ana hat kanal geçiş delikleri (mevcut konturla aynı: U_F sol 2104–2169 × −827…−689 · U_F sağ / U_KE sol 2142–2166 × −827…−765).
  TAVAN 430 1,5   y 2198,5–2200 · sol / sağ / arka 20 aşağı büküm (değişmedi) + ÖN 30 AŞAĞI BÜKÜM (y 2168,5–2198,5 · z 57,5–59) = eski üst kayıt
                  profili yerine. U_F'de baca açıklığı 297 × 197 (kanal iç ölçüsü, flanş altta).
  TAVAN OMEGASI 304 1,2 · tavanın altına punta (gizli) · arka büküm → ön büküm boydan boya (yarım çıta yok) · 60 geniş (taç 30) × 20 yüksek ·
                  U_F: 1 adet x 3325 (ana pano toplama kanalı askıları buna asılır — önce tavanın 20 altında havadaydı) · U_KE: 1 adet ortada x 4615
                  (simetrik). Eski 30 × 30 × 2 tavan kirişleri (U_F 2 · U_KE 2, simetrik değildi) kalkar.
  ARKA SAC 304 1,5 tek parça (servis, yan arka bükümlerine + tavan arka bükümüne ISO 7380 bombe vida — arka yüzde izinli) · U_F: 4 fan
                  önünde yarık ızgara 9 × 100 × 6 (değişmedi).
  RAF 304 1,5 + TAŞIYICI 30 × 30 × 2 (z boyunca, tabana kaynaklı): U_F kutu rafı x 2501,5–3329 (yan saca dayanır; eski 2515 → 13,5 mm boşluk
                  vardı) · U_KE içecek rafı z −520…+25 (koli arka sırası −514'e kadar; eski −826 arkaya 2,5 mm boşluk bırakıyordu, arka 300 mm kablo
                  inişlerine boş kalır). Taşıyıcılar aynı yerde, raf ile aynı boyda.
KALKAN: alt ön kayıt (2) · üst ön kayıt (2) · tavan kirişi (4).   EKLENEN: tavan omegası (2) · taban / tavan ön bükümleri (parçanın kendisi).
BİRLEŞİM: taban + yanlar + tavan + raf taşıyıcıları TIG (iç köşe) → tek rijit gövde; ön dış yüzde vida yok. U kutusu istasyon tavanına içeriden
  M8 (U tabanından, istasyon tavanındaki perçin somuna) — istasyon tavanındaki somun komşu işi (AÇIK).
Kullanım: python u_govde_yeni.py giris.glb cikis.glb [kutular.json]"""
import json, struct, sys
import numpy as np
import cadquery as cq

T, TI = 1.5, 1.2
Y0, YT = 1862.0, 2200.0
YTB = Y0 + T                       # 1863,5 taban üstü
YTV = YT - T                       # 2198,5 tavan altı
ZA, ZAI, ZO = -830.0, -828.5, 59.0
FL = 15.0                          # yan sac ön / arka büküm
ONB = 30.0                         # taban / tavan ön büküm boyu
BUK = 20.0                         # tavan yan / arka büküm
ATIS = (2950.0, 3250.0, -720.0, -520.0)   # baca kanalı dış ölçüsü
PROF = 30.0


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def bir(*s):
    r = s[0]
    for q in s[1:]: r = r.fuse(q)
    r = r.clean()
    if r.ShapeType() != "Solid":
        so = r.Solids()
        assert len(so) == 1, len(so)
        r = so[0]
    return r


def boru_z(x0, x1, y0, y1, z0, z1, et=2.0):
    return kutu(x0, x1, y0, y1, z0, z1).cut(kutu(x0 + et, x1 - et, y0 + et, y1 - et, z0 - 1, z1 + 1))


def silz(x, y, r, z0, z1):
    return cq.Solid.makeCylinder(r, z1 - z0, cq.Vector(x, y, z0), cq.Vector(0, 0, 1))


def omega(xc, z0, z1):
    """şapka profil 1,2: kanatlar tavanın altında (y 2197,3–2198,5), taç y 2178,5–2179,7 · taç 30 · toplam 60"""
    yk0 = YTV - TI; yt0 = YTV - 20.0
    return bir(kutu(xc - 30.0, xc - 15.0, yk0, YTV, z0, z1), kutu(xc + 15.0, xc + 30.0, yk0, YTV, z0, z1),
               kutu(xc - 15.0, xc - 15.0 + TI, yt0, YTV, z0, z1), kutu(xc + 15.0 - TI, xc + 15.0, yt0, YTV, z0, z1),
               kutu(xc - 15.0, xc + 15.0, yt0, yt0 + TI, z0, z1))


def govde(kod, x0, x1, gecis_sol, gecis_sag, basac_x, omegalar, baca, fan, taban_delik=()):
    S, P = {}, {}
    c = kod.lower()
    # taban + ön büküm
    tb = bir(kutu(x0, x1, Y0, YTB, ZAI, ZO), kutu(x0 + T + FL, x1 - T - FL, YTB, YTB + ONB, ZO - T, ZO))
    if baca: tb = tb.cut(kutu(ATIS[0], ATIS[1], Y0 - 1, YTB + 1, ATIS[2], ATIS[3]))
    for (a0, a1, b0, b1) in taban_delik: tb = tb.cut(kutu(a0, a1, Y0 - 1, YTB + 1, b0, b1))
    S["ust_%s_taban_sac" % c] = tb
    # yan saclar
    for tag, xa, xb, fa, fb, gc in (("sol", x0, x0 + T, x0 + T, x0 + T + FL, gecis_sol), ("sag", x1 - T, x1, x1 - T - FL, x1 - T, gecis_sag)):
        w = bir(kutu(xa, xb, YTB, YTV, ZAI, ZO), kutu(fa, fb, YTB, YTV, ZO - T, ZO), kutu(fa, fb, YTB, YTV, ZAI, ZAI + T))
        if gc: w = w.cut(kutu(xa - 1, xb + 1, gc[0], gc[1], gc[2], gc[3]))
        if basac_x:
            xp = basac_x[0] if tag == "sol" else basac_x[1]
            w = w.cut(silz(xp, 2140.0, 5.0, ZO - T - 1, ZO + 1))
        S["ust_%s_yan_%s" % (c, tag)] = w
    # arka sac (tek parça)
    ar = kutu(x0, x1, Y0, YT, ZA, ZAI)
    for (xc, yc) in fan:
        for j in range(9):
            yy = yc - 48.0 + 12.0 * j
            ar = ar.cut(kutu(xc - 50.0, xc + 50.0, yy - 3.0, yy + 3.0, ZA - 1, ZAI + 1))
    S["ust_%s_arka_sac" % c] = ar
    # tavan 430: üst + sol / sağ / arka 20 + ön 30
    tv = bir(kutu(x0, x1, YTV, YT, ZAI, ZO),
             kutu(x0 + T, x0 + 2 * T, YTV - BUK, YTV, ZAI + T, ZO - T), kutu(x1 - 2 * T, x1 - T, YTV - BUK, YTV, ZAI + T, ZO - T),
             kutu(x0 + T + FL, x1 - T - FL, YTV - BUK, YTV, ZAI, ZAI + T),
             kutu(x0 + T + FL, x1 - T - FL, YTV - ONB, YTV, ZO - T, ZO))
    if baca: tv = tv.cut(kutu(ATIS[0] + T, ATIS[1] - T, YTV - 1, YT + 1, ATIS[2] + T, ATIS[3] - T))
    S["ust_%s_tavan_sac" % c] = tv
    for i, xc in enumerate(omegalar):
        P["ust_%s_tavan_omegasi_%d" % (c, i)] = omega(xc, ZAI + T, ZO - T)
    return S, P


# ---------------- U_F ----------------
SF, PF = govde("F", 2500.0, 4000.0, (2104.0, 2169.0, -827.0, -689.0), (2142.0, 2166.0, -827.0, -765.0), (2510.0, 3990.0), [3325.0], True,
               [(3660.0, 1930.0), (3860.0, 1930.0), (2640.0, 2075.0), (2820.0, 2075.0)])
RAF_Y = (YTB + PROF, YTB + PROF + T)               # 1893,5–1895
RZ_F = (-430.0, 25.0)
SF["ust_f_kutu_rafi"] = kutu(2501.5, 3329.0, RAF_Y[0], RAF_Y[1], RZ_F[0], RZ_F[1])
for i, (xa, xb) in enumerate(((2501.5, 2531.5), (2907.0, 2937.0), (3299.0, 3329.0))):
    PF["ust_f_raf_kirisi_%d" % i] = boru_z(xa, xb, YTB, RAF_Y[0], RZ_F[0], RZ_F[1])
# ---------------- U_KE ----------------
SK, PK = govde("KE", 4000.0, 5230.0, (2142.0, 2166.0, -827.0, -765.0), None, None, [4615.0], False, [],
               taban_delik=[(4267.0, 4333.0, -778.0, -742.0), (5067.0, 5133.0, -778.0, -742.0)])   # K / E Harting soket ağzı (istasyon tavanındakiyle aynı 66 × 36)
RZ_K = (-520.0, 25.0)
SK["ust_ke_icecek_rafi"] = kutu(4001.5, 5228.5, RAF_Y[0], RAF_Y[1], RZ_K[0], RZ_K[1])
for i, (xa, xb) in enumerate(((4001.5, 4031.5), (4397.5, 4427.5), (4802.5, 4832.5), (5198.5, 5228.5))):
    PK["ust_ke_raf_kirisi_%d" % i] = boru_z(xa, xb, YTB, RAF_Y[0], RZ_K[0], RZ_K[1])

DUGUM = {"U_F_GOVDE__sac": SF, "U_F_GOVDE__paslanmaz": PF, "U_KE_GOVDE__sac": SK, "U_KE_GOVDE__paslanmaz": PK}
PARCA = {**SF, **PF, **SK, **PK}
NODE = {a: n for n, d in DUGUM.items() for a in d}
KALKAN = ["onyuz_ust_f_alt_kayit", "onyuz_ust_f_ust_kayit", "ust_f_tavan_kirisi_0", "ust_f_tavan_kirisi_1",
          "onyuz_ust_ke_alt_kayit", "onyuz_ust_ke_ust_kayit", "ust_ke_tavan_kirisi_0", "ust_ke_tavan_kirisi_1"]


def tess(s):
    P, I = [], []
    for f in s.Faces():
        v, t = f.tessellate(0.1, 0.2)
        o = sum(len(p) for p in P)
        P.append(np.array([[q.x, q.y, q.z] for q in v], float))
        I.append(np.array(t, np.int64) + o if len(t) else np.zeros((0, 3), np.int64))
    return np.vstack(P), np.vstack(I)


def ag(solidler):
    XX, TT, o = [], [], 0
    for s in solidler:
        X, Tt = tess(s); XX.append(X); TT.append(Tt + o); o += len(X)
    X = np.vstack(XX); Tt = np.vstack(TT)
    Xf = X[Tt.reshape(-1)]; n = np.cross(Xf[1::3] - Xf[0::3], Xf[2::3] - Xf[0::3])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return (Xf / 1000.0).astype(np.float32), np.repeat(n, 3, axis=0).astype(np.float32), np.arange(len(Xf), dtype=np.uint32)


if __name__ == "__main__":
    gi, go = sys.argv[1:3]
    raw = open(gi, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
    bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])

    def ekle(arr, tip, hedef):
        global BIN
        while len(BIN) % 4: BIN += b"\0"
        off = len(BIN); BIN += arr.tobytes()
        J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
        a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
        if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
        J["accessors"].append(a); return len(J["accessors"]) - 1

    ARALIK = {}
    for dugum, dct in DUGUM.items():
        nd = [n for n in J["nodes"] if n.get("name") == dugum][0]
        assert not any(k in nd for k in ("translation", "rotation", "scale", "matrix")), dugum
        X, N, I = ag(list(dct.values()))
        pr = J["meshes"][nd["mesh"]]["primitives"][0]
        pr["attributes"] = {"POSITION": ekle(X, "VEC3", 34962), "NORMAL": ekle(N, "VEC3", 34962)}
        pr["indices"] = ekle(I, "SCALAR", 34963)
        nt = len(I); ex = pr.setdefault("extras", {})
        for k in ("kat", "mek"):
            if k in ex: ex[k] = [ex[k][0], 0, nt]
        ex["kpk"] = []
        b = 0
        for a, s in dct.items():
            n_ = len(tess(s)[1]); ARALIK[a] = [dugum, b, n_]; b += n_
        assert b * 3 == nt
        print("  %-24s %3d parça · %d üçgen" % (dugum, len(dct), nt // 3))
    J["buffers"][0]["byteLength"] = len(BIN)
    jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
    while len(BIN) % 4: BIN += b"\0"
    open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
                         + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
    kut = {}
    for a, s in PARCA.items():
        bb = s.BoundingBox()
        kut[a] = dict(dugum=NODE[a], kutu=[round(v, 2) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)], ucgen=ARALIK[a][1:])
    json.dump(dict(parca=kut, kalkan=KALKAN), open(sys.argv[3] if len(sys.argv) > 3 else "ug/u_parca_kutulari.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("yazıldı", go)
