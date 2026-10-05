# -*- coding: utf-8 -*-
"""AUTOKITCH - KASET 3D/AR v1 (16 Eyl 2026)
Kasetleri telefonda gercek boyutta gormek icin GLB (Android/WebXR) + USDZ (iOS AR Quick Look) uretir.
Kutu olculeri mm: (genislik X, derinlik Z, yukseklik Y).
Cikti: otonom/kaset3d/ altina .glb ve .usdz
"""
import json, os, struct, zipfile

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "otonom", "kaset3d")
MODELLER = [
    ("kaset", 140.0, 400.0, 360.0, (0.16, 0.42, 0.72)),      # standart kaset 14 L
    ("kasar", 280.0, 400.0, 360.0, (0.86, 0.66, 0.24)),      # kasar kabi 28 L
]


def kutu(w, d, h):
    """merkezi tabanda, +Y yukari. donen: (positions, normals, indices)"""
    x, z, y = w / 2000.0, d / 2000.0, h / 1000.0
    yuz = [
        ((-x, 0, z), (x, 0, z), (x, y, z), (-x, y, z), (0, 0, 1)),      # on
        ((x, 0, -z), (-x, 0, -z), (-x, y, -z), (x, y, -z), (0, 0, -1)),  # arka
        ((x, 0, z), (x, 0, -z), (x, y, -z), (x, y, z), (1, 0, 0)),      # sag
        ((-x, 0, -z), (-x, 0, z), (-x, y, z), (-x, y, -z), (-1, 0, 0)),  # sol
        ((-x, y, z), (x, y, z), (x, y, -z), (-x, y, -z), (0, 1, 0)),    # ust
        ((-x, 0, -z), (x, 0, -z), (x, 0, z), (-x, 0, z), (0, -1, 0)),   # alt
    ]
    P, N, I = [], [], []
    for i, (a, b, c, dd, n) in enumerate(yuz):
        for v in (a, b, c, dd):
            P.append(v); N.append(n)
        o = i * 4
        I += [o, o + 1, o + 2, o, o + 2, o + 3]
    return P, N, I


def glb_yaz(yol, P, N, I, renk):
    pos = b"".join(struct.pack("<3f", *p) for p in P)
    nor = b"".join(struct.pack("<3f", *n) for n in N)
    idx = b"".join(struct.pack("<H", i) for i in I)
    while len(idx) % 4:
        idx += b"\x00"
    bin_blob = pos + nor + idx
    mn = [min(p[k] for p in P) for k in range(3)]
    mx = [max(p[k] for p in P) for k in range(3)]
    g = {
        "asset": {"version": "2.0", "generator": "AUTOKITCH kaset_3d_v1"},
        "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0, "name": "kaset"}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0, "NORMAL": 1}, "indices": 2, "material": 0}]}],
        "materials": [{"pbrMetallicRoughness": {"baseColorFactor": list(renk) + [1.0],
                                                "metallicFactor": 0.1, "roughnessFactor": 0.55},
                       "name": "govde"}],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(P), "type": "VEC3", "min": mn, "max": mx},
            {"bufferView": 1, "componentType": 5126, "count": len(N), "type": "VEC3"},
            {"bufferView": 2, "componentType": 5123, "count": len(I), "type": "SCALAR"},
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(pos), "target": 34962},
            {"buffer": 0, "byteOffset": len(pos), "byteLength": len(nor), "target": 34962},
            {"buffer": 0, "byteOffset": len(pos) + len(nor), "byteLength": len(idx), "target": 34963},
        ],
        "buffers": [{"byteLength": len(bin_blob)}],
    }
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4:
        js += b" "
    total = 12 + 8 + len(js) + 8 + len(bin_blob)
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, total))
        f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bin_blob), b"BIN\x00")); f.write(bin_blob)


def usdz_yaz(yol, ad, w, d, h, renk):
    x, z, y = w / 2000.0, d / 2000.0, h / 1000.0
    P = [(-x, 0, z), (x, 0, z), (x, y, z), (-x, y, z), (-x, 0, -z), (x, 0, -z), (x, y, -z), (-x, y, -z)]
    yuzler = [(0, 1, 2, 3), (5, 4, 7, 6), (1, 5, 6, 2), (4, 0, 3, 7), (3, 2, 6, 7), (4, 5, 1, 0)]
    pts = ", ".join("(%.4f, %.4f, %.4f)" % p for p in P)
    fvi = ", ".join(str(i) for f in yuzler for i in f)
    usda = """#usda 1.0
(
    defaultPrim = "%s"
    metersPerUnit = 1
    upAxis = "Y"
)

def Xform "%s" (kind = "component")
{
    def Mesh "govde"
    {
        float3[] extent = [(%.4f, 0, %.4f), (%.4f, %.4f, %.4f)]
        int[] faceVertexCounts = [4, 4, 4, 4, 4, 4]
        int[] faceVertexIndices = [%s]
        point3f[] points = [%s]
        color3f[] primvars:displayColor = [(%.3f, %.3f, %.3f)]
        uniform token subdivisionScheme = "none"
    }
}
""" % (ad, ad, -x, -z, x, y, z, fvi, pts, renk[0], renk[1], renk[2])
    data = usda.encode("utf-8")
    ic_ad = ad + ".usda"
    with zipfile.ZipFile(yol, "w", zipfile.ZIP_STORED) as zf:
        zi = zipfile.ZipInfo(ic_ad, date_time=(2026, 9, 16, 0, 0, 0))
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
for ad, w, d, h, renk in MODELLER:
    P, N, I = kutu(w, d, h)
    glb = os.path.join(OUT, ad + ".glb")
    usdz = os.path.join(OUT, ad + ".usdz")
    glb_yaz(glb, P, N, I, renk)
    usdz_yaz(usdz, ad, w, d, h, renk)
    print("%-8s %4.0f x %4.0f x %4.0f mm  ·  %6.1f L  ·  glb %5d B  ·  usdz %5d B"
          % (ad, w, d, h, w * d * h / 1e6, os.path.getsize(glb), os.path.getsize(usdz)))
