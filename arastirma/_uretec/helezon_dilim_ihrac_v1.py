# -*- coding: utf-8 -*-
"""HELEZONU DILIMLEYEREK IHRAC ET — carpisma govdesi kanat arasini doldurmasin

Sorun (olculdu, kup_teshis_v3.py): helezonun KONVEKS ayristirmasi vidayi MASIF SILINDIRE
ceviriyor. Vida ekseni boyunca 10 ayri noktadan asagi atilan isinlarin HEPSI y~0,33'te
kanada carpti — hicbir yerde kanat arasi boslugu yok. Bu yuzden kupler helezona hic
giremedi ve 0 g cikti. Tasarim degil, CARPISMA GOVDESI hatasi.

Dogru cozum SDF idi ama bu kurulumda "PhysXGpu dll is incompatible" hatasi SDF cooklemeyi
engelliyor. Bu dosya GPU'ya bagli olmayan yolu kuruyor:

  Helezon Z EKSENINDE ince dilimlere bolunuyor. Bir dilimin icindeki kanat parcasi
  neredeyse duz bir kama; konveks kabugu komsu dilimin boslugunu DOLDURAMAZ.
  Dilimler ayni rijit cisme ait, yani vida yine tek parca gibi doner.

C:\\Users\\Kemal\\...\\python topping icin sistem Python'u (CadQuery) ile calisir.
"""
import io, json, math, os, sys
import numpy as np
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
KOK = os.path.dirname(os.path.dirname(U))
OUT = os.path.join(KOK, "otonom", "hat3d", "fizik")

import topping_cad_v11 as TC

KASET = "KÜP SUCUK"
DILIM = 2.5          # mm — kanat hatvesi ~24 mm, 2,5 mm dilim kanadi 10 parcaya boler
YOG = {"sac": 7900.0, "celik": 7900.0, "pom": 1410.0, "silikon": 1150.0, "cam": 1200.0}


def ag(sh, tol=0.10, aci=0.30):
    vs, ts = sh.tessellate(tol, aci)
    return (np.array([[v.x*1e-3, v.y*1e-3, v.z*1e-3] for v in vs], dtype=np.float32),
            np.array(ts, dtype=np.int32))


def main():
    TC.PARCALAR[:] = []; TC.modul()
    yuva = next((a, x0, x1) for a, x0, x1, g in TC.YUVA if a == KASET)
    ad, x0, x1 = yuva
    import importlib
    mod = importlib.import_module(TC.KASET_CAD[ad])
    mod.PARCALAR[:] = []; mod.kap()
    xm, z0 = (x0 + x1) / 2.0, TC.ZK[0] - mod.D / 2.0

    P = []
    dilimlenen = 0
    for p in mod.PARCALAR:
        if p["ad"] == "tasima_tapasi": continue
        sh = p["wp"].val().translate(cq.Vector(xm, TC.KAS[0], z0))
        gr = p.get("grup")
        grup = "SABIT" if not gr else (("HELEZON" if gr == "helezon" else "KARISTIRICI"))
        kg = abs(sh.Volume()) * 1e-9 * YOG.get(p["mal"], 7900.0)

        # KANAT parcalari dilimlenir; mil/gobek/kavrama zaten konveks, dokunma
        if grup == "HELEZON" and p["ad"].startswith("helezon_") and not p["ad"].endswith("cekirdek"):
            b = sh.BoundingBox()
            n = max(1, int(math.ceil((b.zmax - b.zmin) / DILIM)))
            kesilen = 0
            for i in range(n):
                za, zb = b.zmin + i * DILIM, min(b.zmax, b.zmin + (i + 1) * DILIM)
                if zb - za < 0.2: continue
                kutu = cq.Workplane("XY").box(b.xlen + 20, b.ylen + 20, zb - za,
                                              centered=(True, True, False)).translate(
                                              ((b.xmin + b.xmax) / 2, (b.ymin + b.ymax) / 2, za))
                try: par = sh.intersect(kutu.val())
                except Exception: continue
                if par is None or abs(par.Volume()) < 1.0: continue
                V, F = ag(par)
                if not len(F): continue
                P.append(dict(ad="%s_d%02d" % (p["ad"], i), grup=grup, mal=p["mal"],
                              kutle_kg=abs(par.Volume())*1e-9*YOG.get(p["mal"], 7900.0), V=V, F=F))
                kesilen += 1
            dilimlenen += 1
            print("  %-16s %3d dilim" % (p["ad"], kesilen))
            continue

        V, F = ag(sh)
        if not len(F): continue
        P.append(dict(ad=p["ad"], grup=grup, mal=p["mal"], kutle_kg=kg, V=V, F=F))

    # ---- tepsi/pide icin kot bilgisi + hazne sinirlari
    gov = next(p for p in mod.PARCALAR if p["ad"] == "govde")
    gb = gov["wp"].val().translate(cq.Vector(xm, TC.KAS[0], z0)).BoundingBox()
    meta = dict(kaset=KASET, dilim_mm=DILIM, dilimlenen_parca=dilimlenen,
                hazne=dict(x=[gb.xmin, gb.xmax], y=[gb.ymin, gb.ymax], z=[gb.zmin, gb.zmax]),
                agiz_y=TC.AGZ[1] + 0.0, kaset_x=xm,
                parca=[{k: v for k, v in q.items() if k not in ("V", "F")} for q in P])
    with io.open(os.path.join(OUT, "sucuk_kaset_v1.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    np.savez_compressed(os.path.join(OUT, "sucuk_kaset_v1.npz"),
                        **{("V%d" % i): q["V"] for i, q in enumerate(P)},
                        **{("F%d" % i): q["F"] for i, q in enumerate(P)})
    ucgen = sum(len(q["F"]) for q in P)
    print("\nPARCA %d (%d'i kanat dilimi) · UCGEN %d" % (len(P), sum(1 for q in P if "_d" in q["ad"]), ucgen))
    print("hazne x %.0f..%.0f  y %.0f..%.0f  z %.0f..%.0f" % (gb.xmin, gb.xmax, gb.ymin, gb.ymax, gb.zmin, gb.zmax))
    print("yazildi -> sucuk_kaset_v1.{json,npz}")


if __name__ == "__main__":
    main()
