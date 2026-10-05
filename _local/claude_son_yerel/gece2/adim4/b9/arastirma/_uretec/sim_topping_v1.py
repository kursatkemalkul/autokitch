# -*- coding: utf-8 -*-
"""AUTOKITCH · TOPPING SIMULASYON SAHNESI v1 (22 Eyl 2026)
Kemal: "bu tepsiye animasyon verebiliyor musun? Sagda bir pencere acalim, ordan kontrol edelim, kodunu da
test edelim. Hersey gercekmis gibi dusun — motorlar, kablolar, bir sisteme/PC'ye bagli diyelim, burdaki kod
ile yonetiyoruz. Yarin oburgun birine verirken 'bak kod bu, bu kod bunu aktif ediyor, tepsi ilerliyor, sonra
kasetin ust motorunu aktif ediyor' diyebileyim. Kasarli pide deyince tepsi kasarin altina donup x'te
hareketini kasarin dokulusune gore ayarlasin. Gercek hayattaki gibi olucak."

BU DOSYA NE YAPAR: uretim modelini (topping_cad_v10 + kasetler) alir, HAREKET EDEN paketleri AYRI GRUPLARA
bolup tek bir GLB'ye yazar; yaninda makinenin eksen/motor tanimini JSON olarak verir. Tarayicidaki
kontrol yazilimi (otonom/hat/makine_kodu.js) bu JSON'u okuyup GLB'deki gruplari gercek hiz ve devirlerle
hareket ettirir. Sim, CAD'den TURETILIR — ayri bir model degil, ayni kati.

GRUPLAR
  SABIT ................ kabin, yalitim, kovanlar, raylar, kayis zinciri, X motoru, sensorler, kaset govdeleri
  ARABA ................ x'te kayan paket (bloklar, plaka, yatak, ayar bilezigi, donus motoru, apron, kol)
  TABLA ................ arabanin icinde DONEN paket (gobek, tabla, merkezleme pimleri) · pivot: tabla ekseni
  HELEZON_<yuva> ....... kasetin dozaj mili (z ekseninde doner)
  KARISTIRICI_<yuva> ... kasetin karistirici/rotor mili (z ekseninde doner)
  TEPSI · PIDE ......... tablanin ustunde tasinan tepsi ve hamur (sim icin cizilir)
"""
import io, json, math, os, struct, sys
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, U)
import topping_cad_v10 as TC
import topping_hesap_v4 as H
from kaset_3d_v3 import Mesh, MM, MALZEME

KOK = os.path.dirname(os.path.dirname(U))
OUT = os.path.join(KOK, "otonom", "hat3d")

ARABA_P = ("kizak_blogu_", "araba_plakasi", "doner_yatak", "ayar_bilezigi", "donus_motoru", "tahrik_lokmasi",
           "siyirici_apron", "kayis_kolu", "kayis_kelepcesi_", "tabla_home_sensoru", "tabla_home_bayragi", "x_bayragi")
TABLA_P = ("tabla_gobegi", "tabla", "merkezleme_pimi_")


def grup_modul(ad):
    if ad.startswith(TABLA_P) and ad != "tabla_home_sensoru" and ad != "tabla_home_bayragi": return "TABLA"
    if ad.startswith(ARABA_P): return "ARABA"
    return "SABIT"


def ag(wp, tol=0.35, aci=0.7):
    """CadQuery katisindan ag — sim icin kaba yeter (tarayicida 60 fps donecek)"""
    m = Mesh()
    vs, ts = wp.val().tessellate(tol, aci)
    P = [(v.x * MM, v.y * MM, v.z * MM) for v in vs]
    for a, b, c in ts:
        pa, pb, pc = P[a], P[b], P[c]
        ux, uy, uz = pb[0] - pa[0], pb[1] - pa[1], pb[2] - pa[2]
        vx, vy, vz = pc[0] - pa[0], pc[1] - pa[1], pc[2] - pa[2]
        nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
        L = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
        i0 = len(m.P)
        for p in (pa, pb, pc):
            m.P.append(p); m.N.append((nx / L, ny / L, nz / L))
        m.I += [i0, i0 + 1, i0 + 2]
    return m


def glb_yaz(yol, gruplar):
    """gruplar: {grup_adi: {ton: Mesh}} -> her grup bir NODE, altinda ton mesh'leri (renkler korunur)"""
    tonlar = sorted({t for g in gruplar.values() for t in g})
    blob, views, accs, meshes, nodes, kok = [], [], [], [], [], []
    off = [0]

    def gomu(bt, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt); return len(views) - 1

    for gad in sorted(gruplar):
        cocuk = []
        for ton, m in sorted(gruplar[gad].items()):
            if not m.I: continue
            vp = gomu(struct.pack("<%df" % (3 * len(m.P)), *[c for p in m.P for c in p]), 34962)
            vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for nn in m.N for c in nn]), 34962)
            vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
            mn = [min(p[k] for p in m.P) for k in range(3)]; mx = [max(p[k] for p in m.P) for k in range(3)]
            accs.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": mn, "max": mx})
            accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
            accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
            meshes.append({"name": "%s.%s" % (gad, ton), "primitives": [{"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2},
                                                                        "indices": len(accs) - 1, "material": tonlar.index(ton)}]})
            nodes.append({"mesh": len(meshes) - 1, "name": "%s.%s" % (gad, ton)}); cocuk.append(len(nodes) - 1)
        nodes.append({"name": gad, "children": cocuk}); kok.append(len(nodes) - 1)

    mats = []
    for t in tonlar:
        d = MALZEME.get(t, dict(renk=(0.8, 0.8, 0.82, 1.0), met=0.5, ruf=0.5))
        mm = {"name": t, "pbrMetallicRoughness": {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}, "doubleSided": True}
        if d.get("saydam"): mm["alphaMode"] = "BLEND"
        mats.append(mm)
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH sim_topping_v1"}, "scene": 0, "scenes": [{"nodes": kok}],
         "nodes": nodes, "meshes": meshes, "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}]}
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb)))
        f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    return len(bb) + len(js)


def kur():
    TC.PARCALAR[:] = []
    TC.modul()
    G = {}

    def ekle(gad, ton, m):
        G.setdefault(gad, {}).setdefault(ton, Mesh()).ekle(m)

    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom"): continue
        ekle(grup_modul(p["ad"]), p["mal"], ag(p["wp"]))

    # --- kasetler: govde SABIT, iki mil AYRI GRUP ---
    import importlib
    MIL_KOT = {}
    for ad, x0, x1, gen in TC.YUVA:
        mod = importlib.import_module(TC.KASET_CAD[ad])
        mod.PARCALAR[:] = []; mod.kap()
        xm, z0 = (x0 + x1) / 2.0, TC.ZK[0] - mod.D / 2.0
        MIL_KOT[ad] = dict(helezon=TC.KAS[0] + mod.CY, karistirici=TC.KAS[0] + mod.YC, x=xm)
        k = ad.replace(" ", "_")
        for p in mod.PARCALAR:
            if p["ad"] == "tasima_tapasi": continue
            sh = p["wp"].val().translate(cq.Vector(xm, TC.KAS[0], z0))
            gr = p.get("grup")
            gad = "SABIT" if not gr else ("HELEZON_" + k if gr == "helezon" else "KARISTIRICI_" + k)
            ekle(gad, p["mal"], ag(cq.Workplane(obj=sh)))

    # --- tepsi + pide (sim icin) ---
    TB = H.S["tabla"]
    Xc, ZT = 900.0, TC.ZK[0] + 30.0
    ty = TC.AGZ[1] - H.HAMUR_K - H.TEPSI_K
    tepsi = TC.sily(Xc, ZT, 170.0, ty, ty + H.TEPSI_K).cut(TC.sily(Xc, ZT, 164.0, ty + 2.0, ty + H.TEPSI_K + 1.0))
    ekle("TEPSI", "sac", ag(cq.Workplane(obj=tepsi.val())))
    pide = TC.sily(Xc, ZT, 140.0, ty + H.TEPSI_K, ty + H.TEPSI_K + H.HAMUR_K)
    MALZEME.setdefault("hamur", dict(renk=(0.92, 0.84, 0.66, 1.0), met=0.0, ruf=0.9))
    ekle("PIDE", "hamur", ag(cq.Workplane(obj=pide.val())))

    n = glb_yaz(os.path.join(OUT, "sim_topping_v1.glb"), G)
    ucgen = sum(len(m.I) // 3 for g in G.values() for m in g.values())
    print("sim_topping_v1.glb · %d grup · %d ucgen · %.0f KB" % (len(G), ucgen, n / 1024.0))

    # --- MAKINE TANIMI (kontrol yazilimi bunu okur) ---
    DEV = {"KAŞAR KABI": 42.0, "KIYMA": 14.0, "KUŞBAŞI": 13.0, "KÜP SUCUK": 8.0, "HARÇ 1": 26.0, "HARÇ 2": 26.0}
    DOZ = {"KAŞAR KABI": 100.0, "KIYMA": 160.0, "KUŞBAŞI": 145.0, "KÜP SUCUK": 70.0, "HARÇ 1": 110.0, "HARÇ 2": 80.0}
    URUN = {"KAŞAR KABI": "Kaşar", "KIYMA": "Kıyma", "KUŞBAŞI": "Kuşbaşı", "KÜP SUCUK": "Küp sucuk",
            "HARÇ 1": "Lahmacun harcı", "HARÇ 2": "Pizza sosu"}
    yuvalar = []
    for ad, x0, x1, gen in TC.YUVA:
        k = ad.replace(" ", "_")
        yuvalar.append(dict(ad=ad, kod=k, urun=URUN[ad], x=MIL_KOT[ad]["x"], genislik=gen,
                            helezon_rpm=DEV[ad], doz_g=DOZ[ad], cad=TC.KASET_CAD[ad],
                            mil_helezon_y=MIL_KOT[ad]["helezon"], mil_karistirici_y=MIL_KOT[ad]["karistirici"],
                            pompa=TC.KASET_CAD[ad].startswith("harc")))
    tanim = dict(
        modul=dict(w=TC.W, y=TC.Y, d=TC.D, agz=list(TC.AGZ), kas=list(TC.KAS)),
        tabla=dict(cap=TB["cap"], rpm=TB["rpm"], doz_sn=TB["doz_sn"], r_dis=TB["r_dis"], r_ic=TB["r_ic"],
                   t_dis=2.5, t_ic=0.3, x_doz_hiz=TB["x_doz_hiz"], x_gecis_hiz=TB["x_gecis_hiz"],
                   strok=[220.0, 1520.0], istasyon_x=1520.0, eksen_z=ZT, pivot=[Xc, 0.0, ZT], baslangic_x=Xc),
        x=dict(motor="NEMA23 kapalı çevrim step 1,2 N·m", tahrik="GT3 20 diş kasnak", mm_tur=60.0,
               cozunurluk_mm=0.01875, home_x=1520.0, limit=[205.0, 1535.0]),
        donus=dict(motor="NEMA23 pancake 57×57×41 · i=1", tork_nm=0.9, gereken_nm=0.169),
        yuvalar=yuvalar,
        pide=dict(yaricap=140.0, kenar=15.0, ust_y=TC.AGZ[1], tepsi_k=H.TEPSI_K, hamur_k=H.HAMUR_K),
    )
    with io.open(os.path.join(OUT, "sim_makine.json"), "w", encoding="utf-8") as f:
        json.dump(tanim, f, ensure_ascii=False, indent=1)
    print("sim_makine.json yazildi · %d yuva" % len(yuvalar))


if __name__ == "__main__":
    kur()
