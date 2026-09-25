# -*- coding: utf-8 -*-
"""AUTOKITCH · ALTERNATİF A1 (ROBOTSUZ) MONTAJI v1 — hat_v45.glb'den türetilir (26 Eyl 2026)

Geçerli hattın GLB'si açılır; robot, ray, karşıdaki QR dolabı, çekmeceler ve çekmece gövdesi SAHNEDEN ÇIKARILIR (A, TOPPING, fırın,
kesme, kutu modülü AYNEN kalır). alt_robotsuz_cad_v1'in parçaları eklenir; 30 s'lik gösterim animasyonu yazılır:
şeritten top → asansör → itici → tabla · kutu → çıkış çatalı → döner dolap → içecek → müşteri kapağı.
Çıktı: otonom/hat3d/alt1_v1.glb (+ alt1_v1.json). Geçerli montaj (hat_v45) ve paftası DEĞİŞMEZ.
"""
import io, json, math, os, struct, sys, time

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
OUT = os.path.join(KOK, "otonom", "hat3d")
import cadquery as cq
import alt_robotsuz_cad_v1 as A
import kiyma_cad_v6 as KY
from kaset_3d_v3 import Mesh, MM

CIKAR = ("CEK_", "B_KASA", "B_KABLO", "ROBOT_", "QR_DOLABI", "URUN__")
RENK = {"pu": ((0.93, 0.88, 0.72, 0.22), 0.0, 0.8), "kapak": ((0.80, 0.83, 0.87, 0.18), 0.3, 0.4), "sac": ((0.74, 0.77, 0.80, 1.0), 0.85, 0.32),
        "celik": ((0.60, 0.62, 0.65, 1.0), 0.9, 0.35), "aluminyum": ((0.80, 0.82, 0.85, 1.0), 0.9, 0.3), "motor": ((0.18, 0.19, 0.22, 1.0), 0.5, 0.45),
        "pu_bant": ((0.95, 0.95, 0.93, 1.0), 0.0, 0.55), "hamur": ((0.93, 0.78, 0.52, 1.0), 0.0, 0.85), "pom": ((0.95, 0.95, 0.93, 1.0), 0.0, 0.42),
        "referans": ((0.62, 0.66, 0.72, 0.25), 0.0, 0.6), "pc": ((0.80, 0.88, 0.95, 0.25), 0.0, 0.05), "kabin": ((0.80, 0.83, 0.87, 0.20), 0.1, 0.4),
        "siyah": ((0.07, 0.07, 0.08, 1.0), 0.1, 0.6), "karton": ((0.74, 0.57, 0.38, 1.0), 0.0, 0.9), "kutu_icecek": ((0.80, 0.12, 0.10, 1.0), 0.6, 0.3)}


def glb_oku(yol):
    b = open(yol, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    js = json.loads(b[20:20 + n].decode("utf-8"))
    bn = struct.unpack("<I", b[20 + n:24 + n])[0]
    return js, bytearray(b[28 + n:28 + n + bn])


def main():
    t0 = time.time()
    G, BIN = glb_oku(os.path.join(OUT, "hat_v45.glb"))
    kok = G["scenes"][0]["nodes"]
    once = len(kok)
    kok[:] = [i for i in kok if not G["nodes"][i].get("name", "").startswith(CIKAR)]
    G.pop("animations", None)
    print("hat_v45: %d kök düğüm → %d (robot, ray, QR dolabı, çekmeceler, B gövdesi, ürün çıkarıldı)" % (once, len(kok)))

    def gomu(bt, hedef=None):
        while len(BIN) % 4: BIN.append(0)
        v = {"buffer": 0, "byteOffset": len(BIN), "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        G["bufferViews"].append(v); BIN.extend(bt); return len(G["bufferViews"]) - 1
    MI = {}
    def mat(k):
        if k not in MI:
            r, m, ru = RENK[k]
            d = {"name": "MA1_" + k, "pbrMetallicRoughness": {"baseColorFactor": list(r), "metallicFactor": m, "roughnessFactor": ru}, "doubleSided": True}
            if r[3] < 1.0: d["alphaMode"] = "BLEND"
            G["materials"].append(d); MI[k] = len(G["materials"]) - 1
        return MI[k]
    def mesh_ekle(ad, tonlar):
        prims = []
        for k, m in sorted(tonlar.items()):
            vp = gomu(struct.pack("<%df" % (3 * len(m.P)), *[c for p in m.P for c in p]), 34962)
            vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for n in m.N for c in n]), 34962)
            vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
            A_ = G["accessors"]
            A_.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": [min(p[i] for p in m.P) for i in range(3)], "max": [max(p[i] for p in m.P) for i in range(3)]})
            A_.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
            A_.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
            prims.append({"attributes": {"POSITION": len(A_) - 3, "NORMAL": len(A_) - 2}, "indices": len(A_) - 1, "material": mat(k)})
        G["meshes"].append({"name": ad, "primitives": prims})
        G["nodes"].append({"name": ad, "mesh": len(G["meshes"]) - 1}); kok.append(len(G["nodes"]) - 1)
        return len(G["nodes"]) - 1

    A.modul()
    gr = {}
    for p in A.PARCALAR:
        kaba = p["ad"].startswith("top_")
        m = KY.ag(p["wp"], 1.5 if kaba else 0.6, 1.2 if kaba else 1.0)
        gr.setdefault(p["grup"], {}).setdefault(p["mal"], Mesh()).ekle(m)
    ND = {g: mesh_ekle("A1__" + g, t) for g, t in gr.items()}
    # gösterim nesneleri: top · kapalı kutu · içecek kutusu (kendi merkezlerinde)
    d = A.d_top()
    top = Mesh(); top.ekle(KY.ag(cq.Workplane(obj=cq.Solid.makeSphere(d / 2.0, cq.Vector(0, 0, 0), angleDegrees1=-90, angleDegrees2=90)), 0.5, 0.8))
    ND["TOP"] = mesh_ekle("A1__TOP", {"hamur": top})
    kutu = Mesh(); kutu.ekle(KY.ag(A.kut(-160.0, 160.0, 0.0, 45.0, -160.0, 160.0), 0.5, 0.8))
    ND["KUTU"] = mesh_ekle("A1__KUTU", {"karton": kutu})
    kutu_icecek = Mesh(); kutu_icecek.ekle(KY.ag(A.sily(0.0, 0.0, 33.0, 0.0, 115.0), 0.5, 0.8))
    ND["ICECEK"] = mesh_ekle("A1__ICECEK", {"kutu_icecek": kutu_icecek})

    # ---- animasyon (30 s) ----
    FPS = 15.0; TT = [i / FPS for i in range(int(A.DONGU * FPS) + 1)]
    sm, ch = [], []
    def kanal(dugum, yol, vals):
        ti = gomu(struct.pack("<%df" % len(TT), *TT))
        G["accessors"].append({"bufferView": ti, "componentType": 5126, "count": len(TT), "type": "SCALAR", "min": [0.0], "max": [A.DONGU]})
        vo = gomu(struct.pack("<%df" % (3 * len(vals)), *[c for v in vals for c in v]))
        G["accessors"].append({"bufferView": vo, "componentType": 5126, "count": len(vals), "type": "VEC3"})
        sm.append({"input": len(G["accessors"]) - 2, "output": len(G["accessors"]) - 1, "interpolation": "LINEAR"})
        ch.append({"sampler": len(sm) - 1, "target": {"node": dugum, "path": yol}})
        G["nodes"][dugum][yol] = list(vals[0])
    for g in ND:
        if g in ("KAP", "ASANSOR", "ITICI", "CATAL") or g.startswith("RAF_"):
            kanal(ND[g], "translation", [tuple(c * MM for c in A.grup_trs(g, t)) for t in TT])
    kanal(ND["TOP"], "translation", [tuple(c * MM for c in A.top_konum(t)) for t in TT])
    kanal(ND["TOP"], "scale", [(1.0,) * 3 if t < 29.5 else (1e-4,) * 3 for t in TT])
    K0 = (A.X_E + 260.0, 1104.0 + 1.6, -206.0)                          # kapalı kutunun tabanı: kutu modülünün tepsisinde
    kanal(ND["KUTU"], "translation", [tuple((K0[i] + A.kutu_trs(t)[i]) * MM for i in range(3)) for t in TT])
    kanal(ND["KUTU"], "scale", [(1.0,) * 3 if t >= 11.0 else (1e-4,) * 3 for t in TT])
    def icecek(t):
        y_r, z_r = A.raf_konum(t, A.RAF_YUKLE)
        return ((A.X_E + 610.0) * MM, (y_r + 2.0) * MM, z_r * MM)
    kanal(ND["ICECEK"], "translation", [icecek(t) for t in TT])
    t_ic = 21.0                                                         # raf içecek oluğunun altından geçerken
    kanal(ND["ICECEK"], "scale", [(1.0,) * 3 if t >= t_ic else (1e-4,) * 3 for t in TT])
    G["animations"] = [{"name": "A1_robotsuz", "samplers": sm, "channels": ch}]

    while len(BIN) % 4: BIN.append(0)
    G["buffers"] = [{"byteLength": len(BIN)}]
    G["asset"]["generator"] = "AUTOKITCH alt_montaj_v1 (hat_v45 + alt_robotsuz_cad_v1)"
    js = json.dumps(G, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    yol = os.path.join(OUT, "alt1_v1.glb")
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(BIN))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(BIN), b"BIN\x00")); f.write(BIN)
    n_top = {t: 0 for t in A.TOP}
    for p in A.PARCALAR:
        if p["ad"].startswith("top_"): n_top[A.KATLAR[int(p["ad"].split("_")[1])][0]] += 1
    with io.open(os.path.join(OUT, "alt1_v1.json"), "w", encoding="utf-8") as f:
        json.dump(dict(surum="alt_montaj_v1 · %s" % time.strftime("%d.%m.%Y %H:%M"), top=n_top, raf=A.N_RAF, zincir_mm=round(A.pat_boy()),
                       parcalar=[dict(ad=p["ad"], not_=p["not_"]) for p in A.PARCALAR if p["not_"]]), f, ensure_ascii=False, indent=1)
    print("alt1_v1.glb · %.0f KB · %d yeni parça · top %s · %d kanal · %.0f s" % ((len(BIN) + len(js)) / 1024.0, len(A.PARCALAR), n_top, len(ch), time.time() - t0))


if __name__ == "__main__":
    main(); sys.stdout.flush(); os._exit(0)
