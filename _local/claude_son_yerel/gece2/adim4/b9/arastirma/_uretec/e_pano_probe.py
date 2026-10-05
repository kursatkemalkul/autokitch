# -*- coding: utf-8 -*-
"""E v12: pano, piston motoru, vakum/besleme parçaları — sınır kutuları (t 0) + seçilmiş anlarda hareketli olanlar"""
import kutu_cad_v12 as K

K.modul()
ON = ("surucu_", "din_rayi", "plc_", "guc_", "klemens", "kablo_kanali", "pano_", "piston_motor", "piston_kasnak", "piston_kayisi", "piston_BK", "vakum_",
      "besleyici_", "itici_", "sensor_", "asansor_motor")
for p in K.PARCALAR:
    if p["ad"].startswith(ON):
        M = K.grup_matrisi(p["grup"], 0.0) if not p["grup"].startswith("B_") else None
        sh = K.uygula(p["wp"].val(), M) if M is not None else p["wp"].val()
        b = sh.BoundingBox()
        print("%-10s %-40s %s" % (p["grup"], p["ad"][:40], [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]))
for t in (0.0, 0.5, 0.7, 1.0, 1.35, 1.65, 2.0, 2.6, 22.5, 22.8):
    print("t %.2f feed_z %.1f vac %.1f" % (t, K.feed_z(t), K.vacuum_lift(t)))
print("BESLE", K.BESLE, "VAC_Y0", K.VAC_Y0, "YB", K.YB, "T", K.T, "Y_BES_PL", K.Y_BES_PL, "H", K.H, "W", K.W, "D", K.D)
