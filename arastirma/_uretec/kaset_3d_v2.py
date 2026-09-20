# -*- coding: utf-8 -*-
"""AUTOKITCH · KASET 3D/AR v2 (20 Eyl 2026)
Kemal: "Picnic kaseti varya bunun gibi cizebilirmisin ama bizim olculerde, tum bu detaylarla."
Referans: Picnic CHEESE HOPPER — seffaf huni govde, ustte kapak, on yuzde sari etiket bandi,
alt yatakta yatay helezon, ucunda kaplin, iki yanda ayak, arkada asma tirnaklari.

BIZIM OLCULER (16 Eyl karari, 2 gunluk ritim):
  STANDART KASET   140 x 400 x 360 mm · brut 20,2 L · kullanilabilir 14 L · dolu 12,5 kg
  KASAR KABI       280 x 400 x 360 mm · 28 L · dolu 8,8 kg · icinde karistirici + vida

Cikti: otonom/kaset3d/ altina kaset_pro.glb + .usdz ve kasar_pro.glb + .usdz
Cok parcali glTF (her parca kendi malzemesi): seffaf govde/kapak, sari bant, beyaz helezon.
Kural: olculer paftadan, uydurma yok; degisen her sey buradan uretilir.
"""
import json, math, os, struct, zipfile

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "otonom", "kaset3d")

# ---- malzeme renkleri (RGBA) ----
SEFFAF = (0.86, 0.90, 0.94, 0.30)      # polikarbonat govde + kapak
SARI   = (0.98, 0.78, 0.09, 1.00)      # etiket bandi
BEYAZ  = (0.94, 0.94, 0.92, 1.00)      # helezon, kaplin, ayak (POM)
GRI    = (0.62, 0.64, 0.68, 1.00)      # paslanmaz yatak
KOYU   = (0.20, 0.21, 0.24, 1.00)      # conta


# ======================= GEOMETRI YARDIMCILARI =======================
def _yuz(P, N, I, a, b, c, d, n):
    o = len(P)
    for v in (a, b, c, d):
        P.append(v); N.append(n)
    I += [o, o + 1, o + 2, o, o + 2, o + 3]


def _norm(u, v, w):
    L = math.sqrt(u * u + v * v + w * w) or 1.0
    return (u / L, v / L, w / L)


def kutu(x0, x1, y0, y1, z0, z1):
    P, N, I = [], [], []
    _yuz(P, N, I, (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1), (0, 0, 1))
    _yuz(P, N, I, (x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0), (0, 0, -1))
    _yuz(P, N, I, (x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (1, 0, 0))
    _yuz(P, N, I, (x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0), (-1, 0, 0))
    _yuz(P, N, I, (x0, y1, z1), (x1, y1, z1), (x1, y1, z0), (x0, y1, z0), (0, 1, 0))
    _yuz(P, N, I, (x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1), (0, -1, 0))
    return P, N, I


def huni_duvar(ust_x, alt_x, y_ust, y_alt, z0, z1, et):
    """iki yan duvar: ustte +-ust_x, altta +-alt_x (V kesit) · et kalinligi kadar kabuk"""
    P, N, I = [], [], []
    for s in (1.0, -1.0):
        xo_u, xo_a = s * ust_x, s * alt_x
        xi_u, xi_a = s * (ust_x - et), s * (alt_x - et)
        n = _norm(s * (y_ust - y_alt), 0, 0) if abs(ust_x - alt_x) < 1e-6 else _norm(s * (y_ust - y_alt), s * s * (ust_x - alt_x), 0)
        _yuz(P, N, I, (xo_a, y_alt, z1), (xo_u, y_ust, z1), (xo_u, y_ust, z0), (xo_a, y_alt, z0), (s, 0, 0))   # dis
        _yuz(P, N, I, (xi_a, y_alt, z0), (xi_u, y_ust, z0), (xi_u, y_ust, z1), (xi_a, y_alt, z1), (-s, 0, 0))  # ic
        _yuz(P, N, I, (xi_u, y_ust, z1), (xo_u, y_ust, z1), (xo_u, y_ust, z0), (xi_u, y_ust, z0), (0, 1, 0))   # ust kenar
        _yuz(P, N, I, (xo_a, y_alt, z1), (xi_a, y_alt, z1), (xi_a, y_alt, z0), (xo_a, y_alt, z0), (0, -1, 0))  # alt kenar
        for z in (z0, z1):
            nn = (0, 0, -1) if z == z0 else (0, 0, 1)
            _yuz(P, N, I, (xi_a, y_alt, z), (xo_a, y_alt, z), (xo_u, y_ust, z), (xi_u, y_ust, z), nn)
    return P, N, I


def silindir(r, z0, z1, eksen="z", merkez=(0.0, 0.0), dilim=28, kapak=True):
    """eksen z: (x,y)=merkez · eksen y: (x,z)=merkez"""
    P, N, I = [], [], []
    for i in range(dilim):
        a0 = 2 * math.pi * i / dilim
        a1 = 2 * math.pi * (i + 1) / dilim
        if eksen == "z":
            cx, cy = merkez
            p = lambda a, z: (cx + r * math.cos(a), cy + r * math.sin(a), z)
            n0 = (math.cos(a0), math.sin(a0), 0); n1 = (math.cos(a1), math.sin(a1), 0)
        else:
            cx, cz = merkez
            p = lambda a, y: (cx + r * math.cos(a), y, cz + r * math.sin(a))
            n0 = (math.cos(a0), 0, math.sin(a0)); n1 = (math.cos(a1), 0, math.sin(a1))
        o = len(P)
        P += [p(a0, z0), p(a1, z0), p(a1, z1), p(a0, z1)]
        N += [n0, n1, n1, n0]
        I += [o, o + 1, o + 2, o, o + 2, o + 3]
    if kapak:
        for z, nn in ((z0, -1), (z1, 1)):
            o = len(P)
            if eksen == "z":
                P.append((merkez[0], merkez[1], z)); N.append((0, 0, nn))
            else:
                P.append((merkez[0], z, merkez[1])); N.append((0, nn, 0))
            for i in range(dilim + 1):
                a = 2 * math.pi * i / dilim
                if eksen == "z":
                    P.append((merkez[0] + r * math.cos(a), merkez[1] + r * math.sin(a), z)); N.append((0, 0, nn))
                else:
                    P.append((merkez[0] + r * math.cos(a), z, merkez[1] + r * math.sin(a))); N.append((0, nn, 0))
            for i in range(dilim):
                if nn > 0: I += [o, o + 1 + i, o + 2 + i]
                else: I += [o, o + 2 + i, o + 1 + i]
    return P, N, I


def helezon(r_mil, r_dis, z0, z1, tur, cy, kalinlik=2.0, adim=16):
    """yatay helezon: mil z ekseninde, kanat spiral serit (iki yuzlu)"""
    P, N, I = [], [], []
    n = int(tur * adim)
    k = kalinlik / 2000.0                        # kanat yari kalinligi (mm -> m), EKSEN (z) yonunde
    nok = lambda a, r, z: (r * math.cos(a), cy + r * math.sin(a), z)
    for i in range(n):
        t0, t1 = i / float(n), (i + 1) / float(n)
        a0, a1 = 2 * math.pi * tur * t0, 2 * math.pi * tur * t1
        zz0, zz1 = z0 + (z1 - z0) * t0, z0 + (z1 - z0) * t1
        for dz in (k, -k):
            nn = (0, 0, 1) if dz > 0 else (0, 0, -1)
            _yuz(P, N, I, nok(a0, r_mil, zz0 + dz), nok(a0, r_dis, zz0 + dz),
                 nok(a1, r_dis, zz1 + dz), nok(a1, r_mil, zz1 + dz), nn)
        _yuz(P, N, I, nok(a0, r_dis, zz0 + k), nok(a0, r_dis, zz0 - k),
             nok(a1, r_dis, zz1 - k), nok(a1, r_dis, zz1 + k), _norm(math.cos(a0), math.sin(a0), 0))
    return P, N, I


def tekne(r, cy, z0, z1, et=2.0, dilim=22):
    """yarim silindir tekne (alt yari) · ustu acik · iki ucu kapali"""
    P, N, I = [], [], []
    e = et / 1000.0
    nok = lambda a, rr, z: (rr * math.cos(a), cy + rr * math.sin(a), z)
    for i in range(dilim):
        a0 = math.pi + math.pi * i / dilim
        a1 = math.pi + math.pi * (i + 1) / dilim
        _yuz(P, N, I, nok(a0, r, z0), nok(a1, r, z0), nok(a1, r, z1), nok(a0, r, z1),
             _norm(math.cos(a0), math.sin(a0), 0))
        _yuz(P, N, I, nok(a0, r - e, z1), nok(a1, r - e, z1), nok(a1, r - e, z0), nok(a0, r - e, z0),
             _norm(-math.cos(a0), -math.sin(a0), 0))
        for z, nn in ((z0, (0, 0, -1)), (z1, (0, 0, 1))):
            _yuz(P, N, I, nok(a0, r - e, z), nok(a1, r - e, z), nok(a1, r, z), nok(a0, r, z), nn)
    return P, N, I


def koni(r0, r1, z0, z1, cy, dilim=22):
    """cikis hunisi: z0'da r0, z1'de r1"""
    P, N, I = [], [], []
    for i in range(dilim):
        a0 = 2 * math.pi * i / dilim
        a1 = 2 * math.pi * (i + 1) / dilim
        p = lambda a, r, z: (r * math.cos(a), cy + r * math.sin(a), z)
        _yuz(P, N, I, p(a0, r0, z0), p(a1, r0, z0), p(a1, r1, z1), p(a0, r1, z1),
             _norm(math.cos(a0), math.sin(a0), (r0 - r1) / max(1e-6, z1 - z0)))
    return P, N, I


def tasi(g, dx=0.0, dy=0.0, dz=0.0):
    P, N, I = g
    return [(p[0] + dx, p[1] + dy, p[2] + dz) for p in P], N, I


# ======================= MODEL =======================
def kaset_modeli(W, D, H, kasar=False):
    """W genislik (X) · D derinlik (Z) · H yukseklik (Y) mm → parca listesi [(ad, (P,N,I), malzeme)]"""
    m = 0.001                                   # mm → m
    w, d, h = W * m, D * m, H * m
    et = 3.0 * m                                 # cidar 3 mm
    ust_x, alt_x = w / 2.0, (0.070 if not kasar else 0.110) / 2.0 * 2 / 2  # alt agiz yarim genisligi
    alt_x = (0.035 if not kasar else 0.055)
    y_huni_alt = 0.090                           # huni alt kotu (helezon yatagi ustu)
    y_ust = h
    z0, z1 = -d / 2.0, d / 2.0
    r_mil, r_dis = 0.010, 0.028                  # helezon: mil Ø20 · kanat Ø56
    cy = 0.048                                   # helezon ekseni kotu

    P = []
    ekle = lambda ad, g, mal: P.append((ad, g, mal))

    # 1 · huni govde (iki yan duvar V, on/arka duz)
    ekle("govde_yan", huni_duvar(ust_x, alt_x, y_ust, y_huni_alt, z0, z1, et), "seffaf")
    ekle("govde_on", kutu(-ust_x, ust_x, y_huni_alt, y_ust, z1 - et, z1), "seffaf")
    ekle("govde_arka", kutu(-ust_x, ust_x, y_huni_alt, y_ust, z0, z0 + et), "seffaf")

    # 2 · helezon yatagi: seffaf yarim silindir tekne (Picnic'te oldugu gibi helezon disaridan gorunur)
    ekle("yatak", tekne(r_dis + 0.004, cy, z0, z1, et=2.0), "seffaf")

    # 3 · helezon mili + kanat + kaplin
    ekle("mil", silindir(r_mil, z0 + 0.010, z1 + 0.055, "z", (0.0, cy)), "beyaz")
    ekle("kanat", helezon(r_mil, r_dis, z0 + 0.030, z1 - 0.020, tur=7, cy=cy), "beyaz")
    ekle("cikis_hunisi", koni(r_dis + 0.006, 0.014, z1 - 0.004, z1 + 0.042, cy), "beyaz")
    ekle("cikis_agzi", silindir(0.014, z1 + 0.042, z1 + 0.062, "z", (0.0, cy)), "beyaz")
    ekle("kaplin_bilezik", silindir(0.019, z1 + 0.056, z1 + 0.064, "z", (0.0, cy)), "beyaz")

    # 4 · kapak (ustte, contali)
    ekle("kapak", kutu(-ust_x - 0.004, ust_x + 0.004, y_ust, y_ust + 0.012, z0 - 0.004, z1 + 0.004), "seffaf")
    ekle("conta", kutu(-ust_x - 0.002, ust_x + 0.002, y_ust - 0.004, y_ust, z0 - 0.002, z1 + 0.002), "koyu")

    # 5 · sari etiket bandi (on yuz ust)
    bant_y0, bant_y1 = y_ust - 0.062, y_ust - 0.004
    ekle("bant", kutu(-ust_x - 0.001, ust_x + 0.001, bant_y0, bant_y1, z1 - 0.002, z1 + 0.002), "sari")

    # 6 · iki yanda ayak (one uzanan destek)
    for s in (1, -1):
        x = s * (ust_x - 0.006)
        ekle("ayak%d" % s, kutu(x - 0.006 * s, x + 0.006 * s, 0.0, y_huni_alt + 0.030, z1 - 0.030, z1 + 0.006), "beyaz")
        ekle("ayak_taban%d" % s, kutu(x - 0.010 * s, x + 0.010 * s, 0.0, 0.008, z1 - 0.040, z1 + 0.010), "beyaz")
    # arka ayak
    ekle("ayak_arka", kutu(-ust_x + 0.004, ust_x - 0.004, 0.0, 0.020, z0, z0 + 0.016), "beyaz")

    # 7 · arkada asma tirnaklari (makineye oturtma)
    for s in (1, -1):
        x = s * (ust_x - 0.018)
        ekle("tirnak%d" % s, kutu(x - 0.008, x + 0.008, y_ust - 0.090, y_ust - 0.050, z0 - 0.014, z0), "beyaz")

    # 8 · kasar kabinda karistirici (dikey mil + iki kanat)
    if kasar:
        ekle("karistirici_mil", silindir(0.009, y_huni_alt + 0.010, y_ust + 0.030, "y", (0.0, 0.0)), "beyaz")
        for s in (1, -1):
            ekle("karistirici_kanat%d" % s, kutu(0.0 if s > 0 else -ust_x + 0.010, ust_x - 0.010 if s > 0 else 0.0,
                                                 y_huni_alt + 0.020, y_huni_alt + 0.034, -0.006, 0.006), "beyaz")
    return P


# ======================= glTF YAZICI (cok parcali) =======================
MALZEME = {
    "seffaf": (SEFFAF, 0.0, 0.12, True),
    "sari":   (SARI, 0.0, 0.45, False),
    "beyaz":  (BEYAZ, 0.0, 0.42, False),
    "gri":    (GRI, 0.7, 0.35, False),
    "koyu":   (KOYU, 0.1, 0.80, False),
}


def glb_yaz(yol, parcalar, ad):
    mal_ad = list(MALZEME.keys())
    bin_parts, views, accs, meshes, nodes = [], [], [], [], []
    off = 0
    for i, (pad, (P, N, I), mal) in enumerate(parcalar):
        pos = b"".join(struct.pack("<3f", *p) for p in P)
        nor = b"".join(struct.pack("<3f", *n) for n in N)
        idx = b"".join(struct.pack("<I", v) for v in I)
        mn = [min(p[k] for p in P) for k in range(3)]
        mx = [max(p[k] for p in P) for k in range(3)]
        for blob, tgt in ((pos, 34962), (nor, 34962), (idx, 34963)):
            views.append({"buffer": 0, "byteOffset": off, "byteLength": len(blob), "target": tgt})
            bin_parts.append(blob); off += len(blob)
            while off % 4:
                bin_parts.append(b"\x00"); off += 1
        b = len(views) - 3
        accs.append({"bufferView": b, "componentType": 5126, "count": len(P), "type": "VEC3", "min": mn, "max": mx})
        accs.append({"bufferView": b + 1, "componentType": 5126, "count": len(N), "type": "VEC3"})
        accs.append({"bufferView": b + 2, "componentType": 5125, "count": len(I), "type": "SCALAR"})
        a = len(accs) - 3
        meshes.append({"name": pad, "primitives": [{"attributes": {"POSITION": a, "NORMAL": a + 1},
                                                    "indices": a + 2, "material": mal_ad.index(mal)}]})
        nodes.append({"mesh": len(meshes) - 1, "name": pad})
    mats = []
    for k in mal_ad:
        renk, met, ruf, saydam = MALZEME[k]
        m = {"name": k, "pbrMetallicRoughness": {"baseColorFactor": list(renk), "metallicFactor": met, "roughnessFactor": ruf},
             "doubleSided": True}
        if saydam:
            m["alphaMode"] = "BLEND"
        mats.append(m)
    bin_blob = b"".join(bin_parts)
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH kaset_3d_v2"},
         "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes,
         "meshes": meshes, "materials": mats, "accessors": accs, "bufferViews": views,
         "buffers": [{"byteLength": len(bin_blob)}]}
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4:
        js += b" "
    total = 12 + 8 + len(js) + 8 + len(bin_blob)
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, total))
        f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bin_blob), b"BIN\x00")); f.write(bin_blob)
    return len(nodes), len(bin_blob)


def usdz_yaz(yol, parcalar, ad):
    govde = []
    for pad, (P, N, I) in [(p[0], p[1]) for p in parcalar]:
        renk = MALZEME[[q[2] for q in parcalar if q[0] == pad][0]][0]
        pts = ", ".join("(%.4f, %.4f, %.4f)" % p for p in P)
        fvc = ", ".join("3" for _ in range(len(I) // 3))
        fvi = ", ".join(str(i) for i in I)
        mn = [min(p[k] for p in P) for k in range(3)]
        mx = [max(p[k] for p in P) for k in range(3)]
        govde.append("""    def Mesh "%s"
    {
        float3[] extent = [(%.4f, %.4f, %.4f), (%.4f, %.4f, %.4f)]
        int[] faceVertexCounts = [%s]
        int[] faceVertexIndices = [%s]
        point3f[] points = [%s]
        color3f[] primvars:displayColor = [(%.3f, %.3f, %.3f)]
        float[] primvars:displayOpacity = [%.2f]
        uniform token subdivisionScheme = "none"
    }""" % (pad.replace("-", "_"), mn[0], mn[1], mn[2], mx[0], mx[1], mx[2], fvc, fvi, pts,
            renk[0], renk[1], renk[2], renk[3]))
    usda = '#usda 1.0\n(\n    defaultPrim = "%s"\n    metersPerUnit = 1\n    upAxis = "Y"\n)\n\ndef Xform "%s" (kind = "component")\n{\n%s\n}\n' % (ad, ad, "\n".join(govde))
    data = usda.encode("utf-8")
    ic_ad = ad + ".usda"
    with zipfile.ZipFile(yol, "w", zipfile.ZIP_STORED) as zf:
        zi = zipfile.ZipInfo(ic_ad, date_time=(2026, 9, 20, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_STORED
        offset = zf.fp.tell()
        head = 30 + len(ic_ad.encode())
        pad = (64 - ((offset + head) % 64)) % 64
        if 0 < pad < 4:
            pad += 64
        if pad:
            zi.extra = struct.pack("<HH", 0x1986, pad - 4) + b"\x00" * (pad - 4)
        zf.writestr(zi, data)


os.makedirs(OUT, exist_ok=True)
for ad, W, D, H, kasar in (("kaset_pro", 140.0, 400.0, 360.0, False),
                           ("kasar_pro", 280.0, 400.0, 360.0, True)):
    parcalar = kaset_modeli(W, D, H, kasar)
    n, boy = glb_yaz(os.path.join(OUT, ad + ".glb"), parcalar, ad)
    usdz_yaz(os.path.join(OUT, ad + ".usdz"), parcalar, ad)
    print("yazildi: %s · %d parca · %.0f KB" % (ad, n, boy / 1024.0))
