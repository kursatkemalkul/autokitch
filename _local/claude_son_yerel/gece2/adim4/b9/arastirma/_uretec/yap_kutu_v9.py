"""v8 -> v9: contained elevator drive, aligned feet, flush side refill door.
Box die line and folding physics are NOT vendor-approved by this revision.
"""
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / 'kutu_cad_v8.py').read_text(encoding='utf-8-sig')
def replace(a, b, count=1):
    global s
    assert s.count(a) == count, (a[:100], s.count(a), count)
    s = s.replace(a, b)

replace('Y_TK = Y_PLINT - 14.0', 'Y_TK = Y_PLINT + 5.0')
replace('(415.0, -40.0), (415.0, -300.0)', '(415.0, -110.0), (415.0, -770.0)')
a = s.index('    taban = kut(SAC, W - SAC, Y_PLINT,')
b = s.index('    ekle("taban_sac_3", taban, "sac")', a)
s = s[:a] + '    taban = kut(SAC, W - SAC, Y_PLINT, Y_PLINT + 3.0, -D + SAC, Z_TABAN_ON)  # v9: no drive penetrations\n' + s[b:]
replace('232.0, 988.0, -822.0, -412.0', '231.0, 989.0, -823.0, -411.0')
# Same outer side plane (x830), 3 mm reveal; shallow returns on the inside only.
replace('ekle("sarjor_yan_kapisi", kut(W - SAC, W, 234.0, 986.0, -820.0, -414.0), "kabuk")',
'''door = kut(W - SAC, W, 234.0, 986.0, -820.0, -414.0)
    # Continuous upper/lower returns stiffen the sheet without an exterior batten.
    for ya, yb in ((234.0, 235.5), (984.5, 986.0)):
        door = door.union(kut(818.0, W - SAC, ya, yb, -820.0, -414.0))
    ekle("sarjor_yan_kapisi", door, "sac")''')
replace('ekle("kilavuz_sag_tasiyici", kut(X_BL1 + 3.5, W - SAC, 244.0, 984.0, -700.0, -680.0), "sac")',
'''# v9: the vertical stiffener is 10 mm behind the door skin, joined only
    # through inner top/bottom rails. No full-height batten against the outer face.
    kb = kut(815.5,818.5,244,984,-700,-680)
    for ya,yb in ((235.5,245.0),(978.0,984.5)):
        kb = kb.union(kut(815.5,828.5,ya,yb,-819,-415))
    ekle("kilavuz_sag_tasiyici", kb, "sac")''')
replace('sily(405.0, -392.0, 8.0, 150.0, 957.0)', 'sily(405.0, -392.0, 8.0, 153.0, 957.0)')
replace('sily(405.0, -392.0, 6.0, Y_TK - 1.0, 150.0)', 'sily(405.0, -392.0, 6.0, Y_TK - 1.0, 153.0)')
replace('(("asansor_alt_yatak", 150.0), ("asansor_ust_yatak", 957.0))', '(("asansor_alt_yatak", 153.0), ("asansor_ust_yatak", 957.0))')
a = s.index('    # v3: TAHRİK TABANIN ALTINDA')
b = s.index('    e2e("asansor_alt_sensor"', a)
s = s[:a] + '''    # v9: transmission INSIDE the cabinet, above the continuous bottom sheet.
    # Reuse the full-size motor, 2:1 ratio and screw. Shaft faces DOWN, body is in
    # the 65 mm service strip between the magazine and beverage cartons.
    # Nominal 750 mm / 3 mm pitch loop; motor slots provide +/-2 mm tension travel.
    r1, r2 = 60.0 / math.pi, 30.0 / math.pi
    lo, hi = 320.0, 340.0
    for _ in range(40):
        c = (lo + hi) / 2.0
        length = 2.0 * math.sqrt(c*c - (r1-r2)**2) + math.pi*(r1+r2) + 2.0*(r1-r2)*math.asin((r1-r2)/c)
        if length < 750.0: lo = c
        else: hi = c
    mx, mz, my = 405.0 + math.sqrt(c*c - 11.0**2), -381.0, 147.0
    pd1 = kasnak("asansor_kasnak_40", 405.0, Y_TK, -392.0, 40)
    pd2 = kasnak("asansor_kasnak_20", mx, Y_TK, mz, 20)
    kayis_y("asansor_kayisi", 405.0, -392.0, mx, mz, Y_TK + 1.0, pd1, pd2)
    mp = kut(704.0, 766.0, my - 3.0, my, -410.0, -351.0)
    mp = mp.cut(sily(mx - 2.0, mz, 19.5, my - 4.0, my + 1.0).union(sily(mx + 2.0, mz, 19.5, my - 4.0, my + 1.0)).union(kut(mx-2,mx+2,my-4,my+1,mz-19.5,mz+19.5)))
    for sx in (-23.57,23.57):
        for sz in (-23.57,23.57):
            slot = sily(mx+sx-2,mz+sz,2.1,my-4,my+1).union(sily(mx+sx+2,mz+sz,2.1,my-4,my+1)).union(kut(mx+sx-2,mx+sx+2,my-4,my+1,mz+sz-2.1,mz+sz+2.1))
            mp = mp.cut(slot)
    for za, zb in ((-410.0, -407.0), (-354.0, -351.0)):
        mp = mp.union(kut(704.0, 766.0, Y_PLINT + 3.0, my - 3.0, za, zb))
    ekle("asansor_motor_plakasi", mp, "sac", bom=("Motor sehpası 304 3 mm", 1, "tabana kaynaklı; motor 4xM4 ayar yarığı; 750-3M-9 kayış", "v9 · tam boy NEMA23 korunur; sipariş teyidi gerekli"))
    nema23("asansor_motoru", (mx, my, mz), (0, -1, 0), (0, 0, 1))
    # Low removable cover; shaft holes, no enlarged exterior box or floor skirt.
    kor = kut(380.0, 772.0, 126.0, 143.0, -417.0, -363.0).cut(kut(381.0, 771.0, 125.0, 142.0, -416.0, -364.0))
    kor = kor.cut(kut(384.0,426.0,140.0,144.0,-411.0,-377.0)).cut(sily(mx, mz, 14.5, 140.0, 144.0))
    kor = kor.cut(kut(703.5,766.5,125.0,144.0,-410.5,-406.5))
    ekle("asansor_kayis_koruyucu", kor, "sac", bom=("İç kayış koruyucu 304 1 mm", 1, "taban üstünde sökülür", "v9"))
    # Local service cutouts only in internal supports, never the outer shell.
    relief = kut(379.0, 773.0, 125.5, 144.0, -418.0, -365.0)
    for p in PARCALAR:
        if p["ad"] in ("asansor_ray_plakasi", "asansor_ray_plakasi_flansi", "sarjor_kapi_esigi"):
            p["wp"] = p["wp"].cut(relief)
        if p["ad"] == "asansor_ray_plakasi_flansi":
            # Z-fold: uniform full-width floor support in FRONT of the belt.
            p["wp"] = kut(200,600,147,150,-374,-354).union(kut(200,600,126,147,-357,-354)).union(kut(200,600,126,129,-363,-354))
    # Actual shaft bores, rather than overlapping solid cylinders.
    for p in PARCALAR:
        if p["ad"] == "asansor_kasnak_40": p["wp"] = p["wp"].cut(sily(405,-392,6,Y_TK-2,Y_TK+13))
        if p["ad"] == "asansor_kasnak_20": p["wp"] = p["wp"].cut(sily(mx,mz,3.175,Y_TK-2,Y_TK+13))
''' + s[b:]
s = s.replace('kutu_cad_v8 (28 Eyl', 'kutu_cad_v9 (29 Eyl', 1)
s = s.replace('"""AUTOKITCH', '"""v9: Motor taban ÜSTÜNDE; orta ayaklar ön/arka hizasında; yan kapak düz, iç dönüşlü.\nKutu açınımı TASLAK, köşe tırnağı kıvırıcısı eksik: tam otomatik katlama doğrulanmış değildir.\nAUTOKITCH', 1)
replace('assert max(b.ymax for b in tah) <= Y_PLINT - 1.0, "kasnak/kayis tabana degiyor"',
        'assert min(b.ymin for b in tah) >= Y_PLINT + 4.0, "kasnak/kayis taban ustunde en az 1 mm payla olmali"')
replace('tabanin altinda yalniz ayak + supurgelik + asansor tahriki (kasnak/kayis %.0f-%.0f, koruyuculu)',
        'taban altinda yalniz ayak + supurgelik; tahrik ICERIDE (kasnak/kayis %.0f-%.0f)')
replace('ALTTA_SERBEST = ("ayak_", "onyuz_plint", "asansor_kasnak_", "asansor_kayisi", "asansor_motoru", "asansor_motor_plakasi", "asansor_kayis_koruyucu", "asansor_vidasi_alt_ucu")',
        'ALTTA_SERBEST = ("ayak_", "onyuz_plint")')
replace('3 lahmacun/kutu ile ~170 kutu/gun', 'en az 2 lahmacun/kutu ile 180 kutu/gun')
# The new standalone entry point runs its own versioned checks, not v7's
# intentionally strict equality against v6. No separate model/BOM is exported.
a = s.index('if __name__ == "__main__":')
s = s[:a] + '''if __name__ == "__main__":
    import runpy
    runpy.run_path(os.path.join(U, "kutu_v9_check.py"), run_name="__main__")
'''
compile(s, 'kutu_cad_v9.py', 'exec')
(U / 'kutu_cad_v9.py').write_text(s, encoding='utf-8')
print('kutu_cad_v9.py generated')
