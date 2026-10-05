# -*- coding: utf-8 -*-
"""Isaac Sim varlik kutuphanesinde HANGI ROBOT KOLLARI var, ve bizim hatta uyani hangisi?

C:\\isaacsim\\python.bat isaac_robot_bul_v1.py

Bizim ihtiyacimiz (HAT v19 + TOPPING v11'den):
  - tepsi Ø340, urunle birlikte ~1,2 kg + tutucu -> ~3 kg yuk
  - erisim: STORE'dan PRESS'e, TOPPING'e (x 700..2500), OVEN'e — hat 3900 mm
  - gida bolgesi: IP siniflari ve yikanabilirlik onemli (katalogdan bakilacak)
"""
import os, sys

from isaacsim import SimulationApp
app = SimulationApp({"headless": True})

import carb
from isaacsim.storage.native import get_assets_root_path
import omni.client

kok = get_assets_root_path()
print("VARLIK KOKU:", kok)
if not kok:
    print("HATA: varlik koku bulunamadi (internet / Nucleus?)")
    app.close(); sys.exit(1)


def listele(yol, derinlik=0, ust=3):
    r, girdiler = omni.client.list(yol)
    if r != omni.client.Result.OK:
        return []
    return sorted([e.relative_path for e in girdiler])


print("\n=== /Isaac/Robots altinda ===")
ureticiler = listele(kok + "/Isaac/Robots")
print(ureticiler)

for u in ureticiler:
    if u.endswith("/") or "." not in u:
        alt = listele(kok + "/Isaac/Robots/" + u.rstrip("/"))
        kollar = [a for a in alt if not a.endswith(".usd")]
        print("\n--- %-22s %d giris" % (u, len(alt)))
        print("   ", ", ".join(alt[:14]))

app.close()
