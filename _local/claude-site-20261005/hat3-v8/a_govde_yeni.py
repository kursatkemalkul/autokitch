# -*- coding: utf-8 -*-
"""A + U_A GÖVDESİ YENİDEN (Kemal 2 Eki: "tüm montajı yeniden çalışmaktansa gövdeyi baştan oluştur, kısa sürer, temiz olur").
Tek temiz kutu x 736–1436 · y 788–2200 · z −830…+59 (ön kapak A_ONYUZ ayrı, değişmez · sağ duvar = TOPPING dis_yan_sol · kaide KAIDE_A değişmez).
GLB'de A_GOVDE__paslanmaz / __sac düğümlerinin geometrisi bununla değişir; A_GOVDE__plastik + U_A_GOVDE__* boşaltılır;
A bölgesindeki (x 736–1404 · y ≥ 1862) artık elektrik parçaları (açıcı ana hat ucu, konsol) silinir.
Kullanım: python a_govde_yeni.py giris.glb cikis.glb"""
import json, struct, sys
import numpy as np
import cadquery as cq

T_SAC = 1.5
K = 30.0                                     # 30 × 30 × 2 kare profil (mevcut A çerçevesiyle aynı)
X0, X1 = 736.0, 1436.0
XS0, XS1 = 737.5, 1434.5                     # çerçeve dış x (sol yan sacın içi · sağ yan sacın içi) · A kendi sağ yan sacıyla KAPALI ÜRÜN
Y0, YT = 788.0, 2200.0
YK = YT - T_SAC                              # tavan sacı altı 2198,5
ZA, ZO = -830.0, 59.0                        # arka dış · ön çerçeve önü (kapak 59–79)
ZAI = ZA + T_SAC                             # arka sacın içi −828,5


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def kare_boru(x0, x1, y0, y1, z0, z1, et=2.0):           # 30 × 30 × 2 boru: uzun eksen boyunca içi boş
    d = [x1 - x0, y1 - y0, z1 - z0]; ax = int(np.argmax(d))
    dis = kutu(x0, x1, y0, y1, z0, z1)
    ic = [x0 + et, x1 - et, y0 + et, y1 - et, z0 + et, z1 - et]
    ic[2 * ax], ic[2 * ax + 1] = [x0, x1, y0, y1, z0, z1][2 * ax] - 1, [x0, x1, y0, y1, z0, z1][2 * ax + 1] + 1
    return dis.cut(kutu(*ic))


SAC = {
    "a_govde_sol_yan": kutu(X0, X0 + T_SAC, Y0, YK, ZA, ZO),                       # sol yan sac tek parça 788–2198,5
    "a_govde_arka": kutu(X0 + T_SAC, X1 - T_SAC, Y0, YK, ZA, ZAI),                        # arka sac tek parça (sökülür servis sacı)
    "a_govde_tavan": kutu(X0, X1, YK, YT, ZA, ZO),                                # tavan sacı (U_A tavanı yerine)
    "a_govde_sag_yan": kutu(X1 - T_SAC, X1, Y0, YK, ZA, ZO).cut(kutu(X1 - T_SAC - 1, X1 + 1, 894.0, 1042.0, -510.0, 4.0)),   # sağ yan sac tek parça · TABLA GEÇİŞ AĞZI TOPPING sol sacındaki ağızla birebir (y 894–1042 · z −510…+4)
}
YU0, YU1 = YK - K, YK                                                             # üst kuşak 2168,5–2198,5
ZO0 = ZO - K                                                                      # ön çerçeve 29–59
CERCEVE = {
    "onyuz_cerceve_sol_dikme": kare_boru(XS0, XS0 + K, 893.5, YU0, ZO0, ZO),      # ön dikmeler alt bandın üstünden (kaide profiliyle çakışmaz)
    "onyuz_cerceve_sag_dikme": kare_boru(XS1 - K, XS1, 893.5, YU0, ZO0, ZO),
    "a_kose_dikmesi_arka_sol": kare_boru(XS0, XS0 + K, 893.5, YU0, ZAI, ZAI + K),  # arka dikmeler kaide plakası üstünden
    "a_kose_dikmesi_arka_sag": kare_boru(XS1 - K, XS1, 893.5, YU0, ZAI, ZAI + K),
    "onyuz_cerceve_ust_kayit": kare_boru(XS0, XS1, YU0, YU1, ZO0, ZO),            # üst çerçeve halkası (tek kat, tavanın altında)
    "a_ust_kusak_arka": kare_boru(XS0, XS1, YU0, YU1, ZAI, ZAI + K),
    "a_ust_kusak_sol": kare_boru(XS0, XS0 + K, YU0, YU1, ZAI + K, ZO0),
    "a_ust_kusak_sag": kare_boru(XS1 - K, XS1, YU0, YU1, ZAI + K, ZO0),
    "onyuz_cerceve_alt_kayit": kutu(XS0, XS1, Y0, 893.5, ZO - 20.0, ZO).fuse(kutu(XS0, XS1, Y0, 892.0, 35.0, ZO - 20.0)).clean(),   # boşluksuz: kaide ön profiline + üst plakaya dayanır (z 35), taban sacı kenarı üstte          # ön alt bant TEK DÜZ PARÇA tam genişlik (köşeden köşeye), dikmeler üstünde · basamaksız
    "a_govde_sol_yan_omega": kutu(XS0, XS0 + 15.0, 1280.0, 1320.0, ZAI + K, ZO0), # sac omegaları aynı hizada 1280–1320
    "a_govde_arka_omega": kutu(XS0 + K, XS1 - K, 1280.0, 1320.0, ZAI, ZAI + 15.0),
}


# ---- KAİDE A (788–893,5) · 40 × 100 × 2 profil çevre + ORTADA bir enine + ORTADA bir boyuna · üst plaka 4 + mekanizma taban sacı 1,5 · hepsi birbirine dayanır ----
KX0, KX1, KZA, KZO = XS0, XS1, ZAI, 35.0
KZM = (KZA + 40.0 + KZO - 40.0) / 2.0                                            # iç derinliğin ortası
KXM = (KX0 + KX1) / 2.0
KAIDE_P = {
    "kaide_A_on_profil": kare_boru(KX0, KX1, Y0, 888.0, KZO - 40.0, KZO),
    "kaide_A_arka_profil": kare_boru(KX0, KX1, Y0, 888.0, KZA, KZA + 40.0),
    "kaide_A_yan_profil_sol": kare_boru(KX0, KX0 + 40.0, Y0, 888.0, KZA + 40.0, KZO - 40.0),
    "kaide_A_yan_profil_sag": kare_boru(KX1 - 40.0, KX1, Y0, 888.0, KZA + 40.0, KZO - 40.0),
    "kaide_A_enine_profil_0": kare_boru(KXM - 20.0, KXM + 20.0, Y0, 888.0, KZA + 40.0, KZO - 40.0),
    "kaide_A_boyuna_profil_0": kare_boru(KX0 + 40.0, KXM - 20.0, Y0, 888.0, KZM - 20.0, KZM + 20.0),
    "kaide_A_boyuna_profil_1": kare_boru(KXM + 20.0, KX1 - 40.0, Y0, 888.0, KZM - 20.0, KZM + 20.0),
}
KAIDE_S = {"kaide_A_ust_plaka_4": kutu(KX0, KX1, 888.0, 892.0, KZA, KZO), "kaide_A_mekanizma_taban_saci": kutu(KX0, KX1, 892.0, 893.5, KZA, 39.0)}


def ag(solidler):
    P, I = [], []
    for s in solidler:
        for f in s.Faces():
            v, t = f.tessellate(0.1, 0.2)
            o = sum(len(p) for p in P)
            P.append(np.array([[q.x, q.y, q.z] for q in v], float))
            I.append(np.array(t, np.uint32) + o if len(t) else np.zeros((0, 3), np.uint32))
    X = np.vstack(P); T = np.vstack(I).astype(np.uint32)
    # düz gölgeleme: üçgen başına köşe çoğalt + yüz normali
    Xf = X[T.reshape(-1)]; n = np.cross(Xf[1::3] - Xf[0::3], Xf[2::3] - Xf[0::3])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    N = np.repeat(n, 3, axis=0)
    return (Xf / 1000.0).astype(np.float32), N.astype(np.float32), np.arange(len(Xf), dtype=np.uint32)


gi, go = sys.argv[1:3]
raw = open(gi, "rb").read()
jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])


def ekle(arr, tip, hedef):
    global BIN
    while len(BIN) % 4: BIN += b"\0"
    off = len(BIN); BIN += arr.tobytes()
    J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
    a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr) if arr.ndim > 1 else arr.size), "type": tip}
    if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
    J["accessors"].append(a); return len(J["accessors"]) - 1


def koy(dugum, solidler):
    X, N, I = ag(solidler)
    nd = [n for n in J["nodes"] if n.get("name") == dugum][0]
    pr = J["meshes"][nd["mesh"]]["primitives"][0]
    pr["attributes"] = {"POSITION": ekle(X, "VEC3", 34962), "NORMAL": ekle(N, "VEC3", 34962)}
    pr["indices"] = ekle(I, "SCALAR", 34963)
    nt = len(I); ex = pr.get("extras", {})                                  # GLB 'kat'/'mek' aralıkları İNDİS sayısıyla (üçgen × 3)
    if "kat" in ex: ex["kat"] = [ex["kat"][0], 0, nt]
    if "mek" in ex: ex["mek"] = [ex["mek"][0], 0, nt]
    ex["kpk"] = []
    print("  %-26s %d üçgen" % (dugum, nt // 3))


def bosalt(dugum):
    nd = [n for n in J["nodes"] if n.get("name") == dugum]
    if not nd: return
    pr = J["meshes"][nd[0]["mesh"]]["primitives"][0]
    X = np.zeros((3, 3), np.float32) + np.float32(1.0)
    pr["attributes"] = {"POSITION": ekle(X, "VEC3", 34962), "NORMAL": ekle(np.tile(np.float32([0, 1, 0]), (3, 1)), "VEC3", 34962)}
    pr["indices"] = ekle(np.zeros(3, np.uint32), "SCALAR", 34963)
    for k in ("kat", "mek"):
        if k in pr.get("extras", {}): pr["extras"][k] = [pr["extras"][k][0], 0, 3]
    print("  %-26s boşaltıldı" % dugum)


koy("A_GOVDE__sac", list(SAC.values()))
koy("A_GOVDE__paslanmaz", list(CERCEVE.values()))
koy("KAIDE_A__paslanmaz", list(KAIDE_P.values()))
koy("KAIDE_A__sac", list(KAIDE_S.values()))
for d in ["A_GOVDE__plastik", "U_A_GOVDE__paslanmaz", "U_A_GOVDE__sac"] + [n["name"] for n in J["nodes"] if n.get("name", "").startswith("A_MODULER__")]:
    bosalt(d)                                                                       # A_MODULER: eski A çerçevesinin modüler sağ dikme/cep parçaları (y ≤ 1860,5) — yeni gövdeyle üst üste biniyordu
# robot yer tutucu kutuları (ROBOT_RAY / ROBOT_1 / ROBOT_1_KOL) mekanizma etiketsizdi → her istasyon görünümünde açılıyordu: Robot mekanizmasına bağla
_M = J["scenes"][0].get("extras", {}).get("mekanizmalar", [])
_ri = next((i for i, m in enumerate(_M) if m.get("istasyon") == "Robot"), None)
for n in J["nodes"]:
    if n.get("name", "").startswith(("ROBOT_RAY", "ROBOT_1")) and "mesh" in n and _ri is not None:
        for pr in J["meshes"][n["mesh"]]["primitives"]:
            nt = J["accessors"][pr["indices"]]["count"]
            ex = pr.setdefault("extras", {}); ex["mek"] = [_ri, 0, nt]; ex.setdefault("kat", [0, 0, nt]); ex.setdefault("kpk", [])
            print("  %-26s → mekanizma %s" % (n["name"], _M[_ri].get("kod")))

# A bölgesindeki artık elektrik (açıcı ana hat ucu / konsol): ELK_* düğümlerinde x 736–1404 · y ≥ 1862 içinde kalan üçgenler dejenere
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}
sil = 0
for nd in J["nodes"]:
    if not nd.get("name", "").startswith("ELK_") or "mesh" not in nd: continue
    for pr in J["meshes"][nd["mesh"]]["primitives"]:
        ax = J["accessors"][pr["attributes"]["POSITION"]]; v = J["bufferViews"][ax["bufferView"]]
        o = v.get("byteOffset", 0) + ax.get("byteOffset", 0)
        X = np.frombuffer(bytes(BIN[o:o + ax["count"] * 12]), np.float32).reshape(-1, 3) * 1000.0
        ai = J["accessors"][pr["indices"]]; vi = J["bufferViews"][ai["bufferView"]]; dt = TD[ai["componentType"]]
        oi = vi.get("byteOffset", 0) + ai.get("byteOffset", 0)
        I = np.frombuffer(bytes(BIN[oi:oi + ai["count"] * np.dtype(dt).itemsize]), dt).copy().reshape(-1, 3)
        ic = ((X[:, 0] > 736) & (X[:, 0] < 1404) & (X[:, 1] > 1862) & (X[:, 1] < 2200) & (X[:, 2] > -830) & (X[:, 2] < 59)) | ((X[:, 0] > 1380) & (X[:, 0] < 1437) & (X[:, 1] > 1090) & (X[:, 1] < 1475) & (X[:, 2] > -790) & (X[:, 2] < -760))   # + A sağ sacına giren X motoru kablo kelepçeleri (elektrik finalde yeniden)
        m = ic[I].all(axis=1) & (I[:, 0] != I[:, 1])
        if m.any():
            I[m, 1] = I[m, 0]; I[m, 2] = I[m, 0]; BIN[oi:oi + I.nbytes] = I.astype(dt).tobytes(); sil += int(m.sum())
            print("  %-26s -%d üçgen (A üstü artık elektrik)" % (nd["name"], int(m.sum())))
J["buffers"][0]["byteLength"] = len(BIN)
jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
while len(BIN) % 4: BIN += b"\0"
open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
print("yazıldı", go)
