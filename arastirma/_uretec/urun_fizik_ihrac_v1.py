# -*- coding: utf-8 -*-
"""TEPSI + PIDE — GERCEK GEOMETRI (dijital ikiz icin)

Dijital ikizde tepsi duz bir disk olarak konmustu ve tabla uzerinde DURMADI: 3 merkezleme
pimi tablanin 5 mm ustunde duruyor, duz tepsi onlarin icine giriyor, fizik de tepsiyi
asagi itip tablanin ALTINA kacirdi. Bu bir simulasyon hatasi degil, TASARIM bulgusu:
tepsinin pimlere oturacak CUKURLARI olmali (acik is listesinde duruyordu, artik olculdu).

BU DOSYA: tepsi ve pideyi CadQuery ile gercek gibi kurar —
  TEPSI  Ø340 · 1,5 mm sac taban + 12 mm kenar + 3 KONIK CUKUR (pim Ø10, r=100, 0/120/240°)
  PIDE   Ø280 · 8 mm hamur
ve modulun fizik npz'siyle ayni bicimde yazar.
"""
import io, json, math, os, sys
import numpy as np
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
KOK = os.path.dirname(os.path.dirname(U))
OUT = os.path.join(KOK, "otonom", "hat3d", "fizik")

import topping_cad_v11 as TC

SAC = 1.5          # tepsi saci
KENAR = 12.0       # tepsi kenar yuksekligi (hesaptaki TEPSI_K bu — DOLU kalinlik degil)
R_TEPSI = 170.0
R_PIDE = 140.0
HAMUR = 8.0
PIM_R, PIM_D, PIM_H = 100.0, 10.0, 5.0      # merkezleme pimi: yaricap, cap, tabla ustu yuksekligi
YOG_CELIK, YOG_HAMUR = 7900.0, 1000.0       # kg/m3 · ham hamur [V]


def ag(sh, tol=0.4, aci=0.5):
    """DIKKAT: CadQuery'de Workplane("XZ") normali -Y'dir; extrude AsAGIYA gider.
    Ilk surumde tepsi bu yuzden ters cikti (y -12..0) ve sahnede tablanin icine gomuldu.
    Burada Y aynalanir ve ucgen sarimi duzeltilir -> yerel y=0 tepsinin ALT yuzu olur."""
    vs, ts = sh.tessellate(tol, aci)
    V = np.array([[v.x*1e-3, -v.y*1e-3, v.z*1e-3] for v in vs], dtype=np.float32)
    F = np.array([[a, c, b] for a, b, c in ts], dtype=np.int32)      # ayna -> sarim ters cevrilir
    return V, F


def tepsi():
    """taban saci + kenar + 3 konik cukur. Cukur pimden 0,5 mm genis, 1 mm derin pay."""
    taban = cq.Workplane("XZ").circle(R_TEPSI).extrude(SAC)            # XZ duzlemi -> +Y'ye uzar
    kenar = (cq.Workplane("XZ").circle(R_TEPSI).circle(R_TEPSI - SAC).extrude(KENAR))
    t = taban.union(kenar)
    # cukurlar: pim r=100'de, 0/120/240 derece. Cukur = pimi saran konik kap, sacin USTUNE bindirilir
    for i in range(3):
        a = math.radians(i * 120.0)
        x, z = PIM_R * math.cos(a), PIM_R * math.sin(a)
        koni = (cq.Workplane("XZ").workplane(offset=SAC)
                .moveTo(x, z).circle(PIM_D / 2.0 + 1.5).workplane(offset=PIM_H + 1.0)
                .circle(PIM_D / 2.0 + 3.5).loft())
        kabuk = koni.faces("<Y").shell(-SAC) if False else koni     # ince kabuk yerine dolu koni: ayni oturma
        t = t.union(koni)
        t = t.cut(cq.Workplane("XZ").workplane(offset=SAC - 0.01)
                  .moveTo(x, z).circle(PIM_D / 2.0 + 0.5).workplane(offset=PIM_H + 1.0)
                  .circle(PIM_D / 2.0 + 2.0).loft())                # icini bosalt -> pim girer
    return t


def main():
    P = []
    t = tepsi()
    V, F = ag(t.val())
    h = abs(t.val().Volume()) * 1e-9
    P.append(dict(ad="TEPSI", kutle_kg=h * YOG_CELIK, hacim_m3=h, renk=[0.72, 0.75, 0.78],
                  not_="Ø340 · 1,5 mm sac + 12 mm kenar + 3 konik cukur (pim Ø10, r=100)", V=V, F=F))

    pide = cq.Workplane("XZ").workplane(offset=KENAR + 0.5).circle(R_PIDE).extrude(HAMUR)
    V2, F2 = ag(pide.val())
    h2 = abs(pide.val().Volume()) * 1e-9
    P.append(dict(ad="PIDE", kutle_kg=h2 * YOG_HAMUR, hacim_m3=h2, renk=[0.91, 0.84, 0.68],
                  not_="Ø280 · 8 mm ham hamur (1000 kg/m3 [V])", V=V2, F=F2))

    meta = dict(parca=[{k: v for k, v in p.items() if k not in ("V", "F")} for p in P],
                oturma=dict(tepsi_taban_y=0.0, aciklama="yerel y=0 tepsinin ALT yuzu; sahnede tabla ustune (y=100 mm) konur"))
    with io.open(os.path.join(OUT, "urun_fizik_v1.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    np.savez_compressed(os.path.join(OUT, "urun_fizik_v1.npz"),
                        **{("V%d" % i): p["V"] for i, p in enumerate(P)},
                        **{("F%d" % i): p["F"] for i, p in enumerate(P)})
    for p in P:
        print("  %-6s %8.3f kg · %6d ucgen · %s" % (p["ad"], p["kutle_kg"], len(p["F"]), p["not_"]))
    print("yazildi -> urun_fizik_v1.{json,npz}")


if __name__ == "__main__":
    main()
