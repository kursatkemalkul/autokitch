# -*- coding: utf-8 -*-
"""AUTOKITCH · MAKİNE ANA MONTAJI v1 (22 Eyl 2026) — TEK GERÇEK KAYNAK: her şeyin makinedeki yeri burada yazılı.
Kemal: "bu çalıştığımız şeyleri parça parça birleştirip makineyi tamamlayabilir miyiz; teknik resimde genel yerleşim var,
o yerlere bunları koyup 3B üretim modelini oluşturalım; sitede komple görüldüğü bir yer olsun; sonra SolidWorks'e ya da STEP'e dökeriz."

NASIL ÇALIŞIR
  · BIRIM listesi = makinenin bütün parçalarının kütüğü. Her satır: nerede (x0,x1 · y0,y1 · z0,z1), ne durumda, kaynağı ne.
  · durum "GERCEK"  → gerçek CAD var; katı modelden okunur, yerine taşınır, ölçüleri DOĞRULANIR (kütükteki zarfla tutmazsa hata verir).
    durum "KUTU"    → henüz modellenmedi; kütükteki ölçüyle kutu çizilir (şeffaf gri). Sıradaki iş bu kutuları gerçeğe çevirmek.
    durum "KATALOG" → satın alınan parça; ölçü kataloglardan, gövde kutu olarak durur (modellemeye gerek yok).
  · Bir birim gerçeğe dönünce: BIRIM satırında durum GERCEK yapılır + kaynak yazılır. Başka hiçbir yeri değiştirmeye gerek yok.
ÇIKTI: otonom/hat3d/hat_v1.glb + .usdz  ·  otonom/hat3d/durum.json (sayfa oradan okur)  ·  FULL_MAKINE/HAT_v1_YERLESIM.step (SolidWorks)
KOORDİNAT (sw_lib ile aynı): X sağa 0 = hattın sol ucu · Y yukarı 0 = zemin · Z öne, modül ÖN YÜZÜ z = 0, gövde z −830'a kadar.
ÖLÇÜLER: teknik_hat_2kol_v19.py (HAT v19 = geçerli pafta). Pafta değişirse buradaki sabitler de değişir; ikisi ayrı yerde yazılmaz, aşağıda v19'dan OKUNUR.
"""
import importlib, io, json, math, os, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
OUT = os.path.join(KOK, "otonom", "hat3d"); STEP = os.path.join(KOK, "arastirma", "FULL_MAKINE")
os.makedirs(OUT, exist_ok=True)
from kaset_3d_v3 import Mesh, MM, doku_ad, usdz_yaz, MALZEME
MALZEME.setdefault("kutu", dict(renk=(0.62, 0.66, 0.72, 0.30), met=0.0, ruf=0.6, saydam=True))
MALZEME.setdefault("katalog", dict(renk=(0.42, 0.46, 0.52, 0.55), met=0.3, ruf=0.5, saydam=True))
MALZEME.setdefault("kabin", dict(renk=(0.80, 0.83, 0.87, 0.13), met=0.1, ruf=0.4, saydam=True))
MALZEME.setdefault("soguk", dict(renk=(0.25, 0.55, 0.85, 0.28), met=0.0, ruf=0.5, saydam=True))
MALZEME.setdefault("sicak", dict(renk=(0.85, 0.35, 0.22, 0.32), met=0.0, ruf=0.5, saydam=True))
MALZEME.setdefault("robot", dict(renk=(0.96, 0.62, 0.10, 0.75), met=0.2, ruf=0.45, saydam=True))

# ---------------------------------------------------------------- PAFTA v19'DAN OKUNAN ÖLÇÜLER ----------------------------------------------------------------
_p = open(os.path.join(U, "teknik_hat_2kol_v19.py"), encoding="utf-8").read()
_g = {"__name__": "_pafta", "os": os, "math": math}
exec(_p[_p.index("# ======================= VERI ======================="):_p.index("# ======================= YERLESIM =======================")], _g)
DZ, H_MAK, H_B = _g["DZ"], _g["H_MAK"], _g["H_B"]                                       # 830 derin · 2030 yüksek · çekmece modülü 1060
X_A, X_BC, X_D, X_E = _g["X_A"], _g["X_BC"], _g["X_D"], _g["X_E"]
W_A, W_BC, W_D, W_E = _g["W_A"], _g["W_BC"], _g["W_D"], _g["W_E"]
HAT_W = W_A + W_BC + W_D + W_E                                                           # 3900
T_AGZ, T_BAS, T_KAS, T_SOG = _g["T_AGZ"], _g["T_BAS"], _g["T_KAS"], _g["T_SOG"]
YUVA, PZP, FIR, TEK, YAG, KES = _g["YUVA"], _g["PZP"], _g["FIR"], _g["TEK"], _g["YAG"], _g["KES"]
E_MEK, E_AGZ, E_SAR = _g["E_MEK"], _g["E_AGZ"], _g["E_SAR"]
R1X, R2X, RZ, KAIDE, OMUZ, ERISIM = _g["R1X"], _g["R2X"], _g["RZ"], _g["KAIDE"], _g["OMUZ"], _g["ERISIM"]
KOLON, KOL_Y0, K1_TABAN = _g["KOLON"], _g["KOL_Y0"], _g["K1_TABAN"]
KASET_Z0 = -325.0                                                                        # kaset ÖN YÜZÜ z = 0 (modül önüyle aynı düzlem), arkası −325
TAHRIK_Z = (-480.0, -325.0)                                                              # kasetin arkasındaki 505 mm'nin ilk 155'i: redüktör + tahrik yuvası

MODUL = [("A", "MODÜL A · PRESS kolonu", X_A, W_A), ("B", "MODÜL B · ÇEKMECELER", X_BC, W_BC),
         ("C", "MODÜL C · TOPPING (B üstünde)", X_BC, W_BC), ("D", "MODÜL D · FIRIN kolonu", X_D, W_D), ("E", "MODÜL E · KUTU kolonu", X_E, W_E)]
MODUL_Y = {"A": (0.0, H_MAK), "B": (0.0, H_B), "C": (H_B, H_MAK), "D": (0.0, H_MAK), "E": (0.0, H_MAK)}

# ---------------------------------------------------------------- KÜTÜK ----------------------------------------------------------------
# (kod, ad, modül, durum, x0, x1, y0, y1, z0, z1, malzeme, kaynak/not, sayfa)
B = []
def birim(kod, ad, mod, durum, x, y, z, mal="kutu", kaynak="", sayfa=""):
    B.append(dict(kod=kod, ad=ad, modul=mod, durum=durum, x=x, y=y, z=z, mal=mal, kaynak=kaynak, sayfa=sayfa))

# --- C · TOPPING: dozaj kasetleri (GERÇEK olanlar burada) ---
KASET_CAD = {"KAŞAR KABI": ("kasar_cad_v10", "Kaşar kabı v10", "kaset3d/index.html"), "KIYMA": ("kiyma_cad_v5", "Kıyma kaseti v5", "kaset3d/index.html"),
             "KUŞBAŞI": ("kusbasi_cad_v4", "Kuşbaşı kaseti v4", "kaset3d/index.html"), "SUCUK": ("sucuk_cad_v3", "Küp sucuk kaseti v3", "kaset3d/index.html")}
YUVA_V1 = [("HARÇ 1", 280.0, 370.0), ("HARÇ 2", 280.0, 650.0), ("KIYMA", 140.0, 860.0), ("KUŞBAŞI", 140.0, 1000.0),
           ("KAŞAR KABI", 280.0, 1210.0), ("SUCUK", 140.0, 1420.0)]        # v19'da sucuk 180'lik DİLİMLEYİCİYDİ; Kemal 21 Eyl'de küp sucuk kasetine geçti → 140 (kaşarın bitişine yaslandı: 1350–1490, sağda 40 mm serbest kaldı)
for urun, gw, xc in YUVA_V1:
    xa = X_BC + xc - gw / 2.0; anahtar = urun.split()[0] if urun.startswith("HARÇ") else urun
    cad = KASET_CAD.get(anahtar)
    birim("KASET_" + urun.replace(" ", "_"), (cad[1] if cad else "Harç kaseti (KARAR: yap / satın al)"), "C", "GERCEK" if cad else "KUTU",
          (xa, xa + gw), (T_KAS[0], T_KAS[0] + 360.0), (KASET_Z0, 0.0), "pom" if cad else "kutu",
          (cad[0] + ".py") if cad else "modellenmedi · kıyma kaseti macunu pideye YAYAMIYOR, harçta sorun daha ağır (yayıcı kararı)", cad[2] if cad else "")
    birim("TAHRIK_" + urun.replace(" ", "_"), "Tahrik: 2 × redüktör + yaylı kavrama yuvası", "C", "KUTU",
          (xa + 10.0, xa + gw - 10.0), (T_KAS[0] + 20.0, T_KAS[0] + 320.0), TAHRIK_Z, "katalog", "NMRV030 sınıfı ×2 · kasetin arkasındaki 505 mm'ye oturur (AÇIK İŞ: motor yerleşimi)")
birim("TOPPING_AGZ", "Robot ağzı 1740 × 110 (tepsi buradan geçer)", "C", "KUTU", (X_BC + 30.0, X_BC + 1770.0), T_AGZ, (-140.0, 0.0), "kutu", "pafta v19")
birim("TOPPING_BAS", "Dozaj başlıkları bandı (çıkış tüpleri + memeler)", "C", "GERCEK_PARCA", (X_BC + 33.0, X_BC + 1767.0), T_BAS, (-200.0, 0.0), "kutu", "kasetlerin çıkış tüpü bu banda iner")
birim("TOPPING_SOG", "C teknik bandı: soğutma grubu + evaporatör + sürücüler + ana pano + UPS", "C", "KUTU", (X_BC + 33.0, X_BC + 1767.0), T_SOG, (-DZ + 20.0, -20.0), "kutu", "pafta v19 · 6 kart + PLC + 500 VA UPS")
birim("TOPPING_KABIN", "TOPPING kabini (+3 °C · önden kaset takılır)", "C", "KUTU", (X_BC, X_BC + W_BC), (H_B, H_MAK), (-DZ, 0.0), "soguk", "pafta v19")

# --- B · ÇEKMECELER (STORE, TOPPING'in altında) ---
_yk = {"hamur": 108.0, "lahm": 93.0, "icecek": 274.0}
for ki, (kolon, y0) in enumerate(zip(KOLON, KOL_Y0)):
    xk = X_A + ki * 700.0; y = y0
    for adet, tip in kolon:
        for j in range(adet):
            birim("CEK_%s_%s_%d" % (_g["KOLON_AD"][ki], tip, j + 1), "%s çekmecesi (motorlu · contalı)" % _g["AD"][tip].split("·")[0].strip(), "B", "KUTU",
                  (xk + 20.0, xk + 680.0), (y, y + _yk[tip] - 3.0), (-760.0, 0.0), "soguk",
                  "SolidWorks'te var: 1_STORE_v4 (CadQuery'ye alınmadı) · %s" % (("%d %s" % _g["CAP"][tip]) if _g["CAP"][tip][0] else _g["CAP"][tip][1]))
            y += _yk[tip]
birim("B_SOGUTMA", "B soğutma grubu (K1 altı)", "B", "KATALOG", (X_A + 20.0, X_A + 680.0), (0.0, K1_TABAN), (-DZ + 20.0, -20.0), "katalog", "⅕ HP")
birim("B_KABIN", "ÇEKMECE modülü kabini (+3 / −18 bölmeli)", "B", "KUTU", (X_A, X_BC + W_BC), (0.0, H_B), (-DZ, 0.0), "soguk", "pafta v19 · 20 çekmece")

# --- A · PRESS ---
birim("PRESS", "Fersah PZP-400 hamur presi", "A", "KATALOG", (X_A + 30.0, X_A + 670.0), PZP, (-800.0, 0.0), "katalog", "640 × 800 × 950 · 170 kg · 3,5 kW (katalog)")
birim("PRESS_PLAKA", "Pres alt plakası (hamur bırakma kotu)", "A", "KUTU", (X_A + 60.0, X_A + 640.0), (_g["PLAKA"], _g["PLAKA"] + 20.0), (-700.0, -60.0), "kutu", "VARSAYIM: kot 1150 katalogda yok")

# --- D · FIRIN ---
birim("D_KABIN", "FIRIN kolonu kabini", "D", "KUTU", (X_D, X_D + W_D), (0.0, H_MAK), (-DZ, 0.0), "sicak", "pafta v19")
birim("D_TEKNIK", "Fırın teknik bölmesi (pano · fan)", "D", "KUTU", (X_D + 30.0, X_D + 670.0), TEK, (-DZ + 20.0, -20.0), "kutu", "pafta v19")
birim("D_YAG", "Yağ / sprey bölmesi", "D", "KUTU", (X_D + 30.0, X_D + 670.0), YAG, (-700.0, -20.0), "kutu", "pafta v19")
birim("D_KESME", "Kesme bölmesi", "D", "KUTU", (X_D + 30.0, X_D + 670.0), KES, (-700.0, -20.0), "kutu", "pafta v19")
for i, (y0, y1, ad) in enumerate(FIR):
    birim("FIRIN_%d" % (i + 1), "Fırın haznesi %d (pide · pizza · lahmacun)" % (i + 1), "D", "KUTU", (X_D + 40.0, X_D + 660.0), (y0, y1), (-680.0, -40.0), "sicak", "pafta v19 · ayarlı sıcaklık + süre")

# --- E · KUTULAMA ---
birim("E_KABIN", "KUTU kolonu kabini", "E", "KUTU", (X_E, X_E + W_E), (0.0, H_MAK), (-DZ, 0.0), "kutu", "pafta v19")
birim("E_MEK", "Kutu mekanizması (plunger + vakum)", "E", "KUTU", (X_E + 30.0, X_E + 670.0), E_MEK, (-700.0, -20.0), "kutu", "5_PACK_v3 SolidWorks'te var")
birim("E_AGZ", "Kutulama ağzı", "E", "KUTU", (X_E + 30.0, X_E + 670.0), E_AGZ, (-500.0, 0.0), "kutu", "pafta v19")
birim("E_SARJOR", "Kutu şarjörü (blank)", "E", "KUTU", (X_E + 30.0, X_E + 670.0), E_SAR, (-700.0, -20.0), "kutu", "pafta v19")

# --- ROBOTLAR (hattın ÖNÜNDE, z = +RZ) ---
for i, rx in enumerate((R1X, R2X)):
    birim("ROBOT_%d" % (i + 1), "Fairino FR10 kobot %d (erişim %.0f)" % (i + 1, ERISIM), "-", "KATALOG",
          (rx - 90.0, rx + 90.0), (0.0, KAIDE), (RZ - 90.0, RZ + 90.0), "robot", "katalog · kaide")
    birim("ROBOT_%d_KOL" % (i + 1), "Kobot %d omuz + kol zarfı" % (i + 1), "-", "KATALOG",
          (rx - 140.0, rx + 140.0), (KAIDE, OMUZ + 180.0), (RZ - 140.0, RZ + 140.0), "robot", "yalnız ZARF · gerçek kol modeli yok")

DURUM_RENK = {"GERCEK": "gerçek CAD", "GERCEK_PARCA": "kısmen gerçek", "KUTU": "kutu (modellenmedi)", "KATALOG": "katalog (satın alınan)"}


# ---------------------------------------------------------------- GEOMETRİ ----------------------------------------------------------------
def kutu_kat(b):
    (x0, x1), (y0, y1), (z0, z1) = b["x"], b["y"], b["z"]
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


DIS = ("govde", "plaka_arka", "plaka_on", "kulp", "cikis_tupu", "yatak_kapagi", "conta_arka", "conta_on") + tuple("saplama_%d" % i for i in range(4)) + ("somun_arka_0", "somun_arka_1", "somun_arka_2", "somun_arka_3", "somun_on_0", "somun_on_1", "topuz", "kilit_pimi")


def kaset_parcalari(modul):
    """kasetin DIŞ kabuğu (makine görünümü için): gövde, plakalar, kapak, kulp, tüp, yatak kapağı, saplamalar.
    İç parçalar (helezon, rotor, 56 parçanın tamamı) kendi sayfasında duruyor — makine modelini şişirmemek için buraya alınmaz."""
    V = importlib.import_module(modul); V.PARCALAR[:] = []; V.kap()
    return V, [p for p in V.PARCALAR if p["ad"] in DIS]


def yerlestir(sh, b, V):
    """kaset katısını kütükteki yere taşır: yerel x ortada, z ön yüz +D/2, y taban 0 → hedef kutunun sol-alt-ön köşesi"""
    (x0, x1), (y0, _), (_, z1) = b["x"], b["y"], b["z"]
    return sh.translate(cq.Vector((x0 + x1) / 2.0, y0, z1 - V.D / 2.0))


def kutu_ag(b):
    """kutu birimin ağı (6 yüz) — makine görünümünde 'henüz modellenmedi' kutusu"""
    (x0, x1), (y0, y1), (z0, z1) = b["x"], b["y"], b["z"]; m = Mesh()
    K = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    for a_, b_, c_, d_, n_ in ((0, 3, 2, 1, (0, 0, -1)), (4, 5, 6, 7, (0, 0, 1)), (0, 1, 5, 4, (0, -1, 0)), (3, 7, 6, 2, (0, 1, 0)), (0, 4, 7, 3, (-1, 0, 0)), (1, 2, 6, 5, (1, 0, 0))):
        m.quad(tuple(c * MM for c in K[a_]), tuple(c * MM for c in K[b_]), tuple(c * MM for c in K[c_]), tuple(c * MM for c in K[d_]), n_)
    return m.duzelt()


def glb_yaz(yol, parcalar, dokular):
    """animasyonsuz sade GLB (kaset dosyalarındaki yazıcının hat sürümü): yalnız kullanılan malzemeler yazılır"""
    import struct
    kullanilan = sorted(set(mal for _a, _m, mal in parcalar)); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]
    def gomu(bt, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt); return len(views) - 1
    for adi, m, mal in parcalar:
        vp = gomu(struct.pack("<%df" % (3 * len(m.P)), *[c for p in m.P for c in p]), 34962)
        vn = gomu(struct.pack("<%df" % (3 * len(m.N)), *[c for nn in m.N for c in nn]), 34962)
        vi = gomu(struct.pack("<%dI" % len(m.I), *m.I), 34963)
        mn = [min(p[k] for p in m.P) for k in range(3)]; mx = [max(p[k] for p in m.P) for k in range(3)]
        accs.append({"bufferView": vp, "componentType": 5126, "count": len(m.P), "type": "VEC3", "min": mn, "max": mx})
        accs.append({"bufferView": vn, "componentType": 5126, "count": len(m.N), "type": "VEC3"})
        accs.append({"bufferView": vi, "componentType": 5125, "count": len(m.I), "type": "SCALAR"})
        meshes.append({"name": adi, "primitives": [{"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": kullanilan.index(mal)}]})
        nodes.append({"mesh": len(meshes) - 1, "name": adi})
    mats = []
    for k in kullanilan:
        d = MALZEME[k]; mm = {"name": k, "pbrMetallicRoughness": {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}, "doubleSided": True}
        if d.get("saydam"): mm["alphaMode"] = "BLEND"
        mats.append(mm)
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH hat_montaj_v1"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes, "meshes": meshes,
         "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}]}
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    return len(bb) + len(js)


if __name__ == "__main__":
    t0 = time.time(); parcalar, asm, sayac, AG = [], cq.Assembly(name="HAT_v1"), {}, None
    RENK = dict(pom=(0.95, 0.95, 0.93, 1), kutu=(0.62, 0.66, 0.72, 0.4), katalog=(0.42, 0.46, 0.52, 0.6), soguk=(0.25, 0.55, 0.85, 0.35),
                sicak=(0.85, 0.35, 0.22, 0.4), robot=(0.96, 0.62, 0.10, 0.8), kabin=(0.8, 0.83, 0.87, 0.2))
    for b in B:
        sayac[b["durum"]] = sayac.get(b["durum"], 0) + 1
        if b["durum"] == "GERCEK":
            V, ps = kaset_parcalari(b["kaynak"][:-3]); AG = AG or V
            zarf = (b["x"][1] - b["x"][0], b["y"][1] - b["y"][0], b["z"][1] - b["z"][0])
            assert abs(V.W - zarf[0]) < 0.6 and abs(V.H - zarf[1]) < 0.6 and abs(V.D - zarf[2]) < 0.6, \
                "%s: kutukte zarf %s, CAD %s — pafta ile model TUTMUYOR" % (b["kod"], zarf, (V.W, V.H, V.D))
            m = Mesh()
            for p in ps:
                sh = yerlestir(p["wp"].val(), b, V); m.ekle(V.ag(cq.Workplane(obj=sh), 0.5, 0.9))
                asm.add(sh, name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK["pom"]))
            parcalar.append((b["kod"], m, b["mal"])); b["parca"] = len(ps)
        else:
            parcalar.append((b["kod"], kutu_ag(b), b["mal"])); asm.add(kutu_kat(b), name=b["kod"], color=cq.Color(*RENK.get(b["mal"], RENK["kutu"])))
        b["olcu"] = [round(b["x"][1] - b["x"][0]), round(b["y"][1] - b["y"][0]), round(b["z"][1] - b["z"][0])]
    ucgen = sum(len(m.I) // 3 for _a, m, _mal in parcalar)
    print("BIRIM %d  ·  %s  ·  %d ucgen" % (len(B), "  ·  ".join("%s %d" % (k, v) for k, v in sorted(sayac.items())), ucgen))

    # ---- zarf denetimi: hiçbir birim hattın dışına taşmasın; kasetler yuvasında mı ----
    tasan = [b["kod"] for b in B if b["modul"] != "-" and not (-1 <= b["x"][0] and b["x"][1] <= HAT_W + 1 and -1 <= b["y"][0] and b["y"][1] <= H_MAK + 1 and -DZ - 1 <= b["z"][0] and b["z"][1] <= 1)]
    print("ZARF DENETIMI: %s" % ("hepsi hattin icinde (%.0f x %.0f x %.0f)" % (HAT_W, H_MAK, DZ) if not tasan else "TASAN: " + ", ".join(tasan)))
    assert not tasan
    kas = [b for b in B if b["kod"].startswith("KASET_")]
    cak = [(a["kod"], c["kod"]) for i, a in enumerate(kas) for c in kas[i + 1:] if a["x"][0] < c["x"][1] - 0.01 and c["x"][0] < a["x"][1] - 0.01]
    print("KASET YUVALARI: %d yuva · %s" % (len(kas), "yan yana, cakisma yok" if not cak else "CAKISMA: %s" % cak))
    assert not cak
    print("   kaset sirasi: " + " · ".join("%s %.0f–%.0f" % (b["kod"].replace("KASET_", ""), b["x"][0], b["x"][1]) for b in kas))
    print("   kaset arkasinda kalan bosluk: %.0f mm (kaset %.0f + tahrik %.0f)" % (DZ - 325.0, 325.0, TAHRIK_Z[1] - TAHRIK_Z[0]))

    # ---- çıktılar ----
    dokular = {"ad": doku_ad("AUTOKITCH HAT v1", "%.0f × %.0f × %.0f mm  ·  beyaz = gerçek model  ·  şeffaf = henüz kutu" % (HAT_W, H_MAK, DZ), ok_sol=True),
               "montaj": doku_ad("MAKİNE ANA MONTAJI", "birimler tek tek gerçek modele çevriliyor", ok_sol=False)}
    b1 = glb_yaz(os.path.join(OUT, "hat_v1.glb"), parcalar, dokular)
    print("hat_v1.glb · %d birim · %.0f KB" % (len(parcalar), b1 / 1024.0))
    b2, prim, sorun, _u = usdz_yaz([os.path.join(OUT, "hat_v1.usdz")], "hat_v1", parcalar, dokular)
    print("hat_v1.usdz · %.0f KB · %d prim · USD denetimi: %s" % (b2 / 1024.0, prim, "GECTI" if not sorun else "KALDI"))
    for x in sorun: print("   HATA:", x)
    os.makedirs(STEP, exist_ok=True); asm.save(os.path.join(STEP, "HAT_v1_YERLESIM.step"))
    print("HAT_v1_YERLESIM.step · SolidWorks'te montaj olarak acilir · %s" % STEP)
    with io.open(os.path.join(OUT, "durum.json"), "w", encoding="utf-8") as f:
        json.dump(dict(hat=dict(w=HAT_W, h=H_MAK, d=DZ, pafta="HAT_2KOL_v19"), sayac=sayac, modul=[dict(kod=k, ad=a, x=[x, x + w], y=list(MODUL_Y[k])) for k, a, x, w in MODUL],
                       birim=[dict(kod=b["kod"], ad=b["ad"], modul=b["modul"], durum=b["durum"], olcu=b["olcu"], x=list(b["x"]), y=list(b["y"]), z=list(b["z"]),
                                   kaynak=b["kaynak"], sayfa=b["sayfa"], parca=b.get("parca", 0)) for b in B]), f, ensure_ascii=False)
    g_ = sayac.get("GERCEK", 0) + sayac.get("GERCEK_PARCA", 0)
    print("durum.json yazildi · GERCEK %d / %d birim (%%%.0f) · toplam %.0f sn" % (g_, len(B), 100.0 * g_ / len(B), time.time() - t0))
    sys.stdout.flush(); os._exit(0)
