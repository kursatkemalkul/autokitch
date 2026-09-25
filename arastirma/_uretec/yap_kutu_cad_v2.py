# -*- coding: utf-8 -*-
"""kutu_cad_v1 -> v2 (25 Eyl 2026): KAYIŞ HATASI + piston BK12 askısı
  · kayis_y(): XZ çalışma düzleminde yerel v = +z; v1 noktaları −z ile çizmişti → asansör ve piston kayışlarının
    DÜZ KOLLARI z'de aynalanıp makinenin ÖNÜNE (z +392 / +325) düşmüştü. Kasnak sarımları doğru yerdeydi, o yüzden
    çakışma taraması boşluğa düşen kolları yakalamadı; ana montajın zarf denetimi yakaladı (E_SARJOR, E_PISTON taşıyor).
  · Kayış doğru yerine gelince piston kayışı BK12 askısının x 288–300 ayağından geçecekti → askı ayakları z'nin iki
    yanına (−345…−339 ve −311…−305) alındı; kayış (z −334,6…−315,4) aradan geçer.
  · BOM çıktısı 5_PACK_v2, GLB kutu_modulu_v2.glb.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kutu_cad_v1.py"), encoding="utf-8").read()


def degis(a, b):
    global s
    assert s.count(a) == 1, "YOK/COK: " + a[:90]
    s = s.replace(a, b, 1)


degis('''"""AUTOKITCH · E · KUTU KATLAMA MODÜLÜ — ÜRETİM MODELİ v1 (25 Eyl 2026)''',
      '''"""AUTOKITCH · E · KUTU KATLAMA MODÜLÜ — ÜRETİM MODELİ v2 (25 Eyl 2026)
v2: kayis_y z işaret hatası düzeltildi (asansör + piston kayışlarının düz kolları makinenin önüne düşmüştü) ·
    piston BK12 askı ayakları kayışın iki yanına alındı. Önceki: kutu_cad_v1.py
''')
degis('''        pl = cq.Workplane("XZ", origin=(0, y, 0)).polyline([(p[0], -p[1]) for p in q]).close().extrude(-genis)''',
      '''        pl = cq.Workplane("XZ", origin=(0, y, 0)).polyline([(p[0], p[1]) for p in q]).close().extrude(-genis)   # v2: XZ'de yerel v = +z (v1'de −z idi)''')
degis('''    for i, (x0, x1) in enumerate(((240.0, 252.0), (288.0, 300.0))):
        ekle("piston_BK_askisi_%d" % i, kut(x0, x1, 1990.5, H - SAC, -343.0, -307.0), "aluminyum")''',
      '''    for i, (z0, z1) in enumerate(((-345.0, -339.0), (-311.0, -305.0))):              # v2: ayaklar kayışın iki yanında (z)
        ekle("piston_BK_askisi_%d" % i, kut(240.0, 300.0, 1990.5, H - SAC, z0, z1), "aluminyum")''')
degis('''        glb_yaz(os.path.join(KOK, "otonom", "hat3d", "kutu_modulu_v1.glb")); sys.stdout.flush()''',
      '''        glb_yaz(os.path.join(KOK, "otonom", "hat3d", "kutu_modulu_v2.glb")); sys.stdout.flush()''')
degis('''        bom_yaz(os.path.join(KOK, "arastirma", "5_PACK_v1"))''', '''        bom_yaz(os.path.join(KOK, "arastirma", "5_PACK_v2"))''')
degis('''    print("E KUTU MODULU v1: %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()''',
      '''    print("E KUTU MODULU v2: %d parca · %.0f sn" % (len(PARCALAR), time.time() - t0)); sys.stdout.flush()''')
degis('''    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH kutu_cad_v1"}''', '''    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH kutu_cad_v2"}''')
# zarf denetimi kutu üretecinin içinde de (montaj beklemeden): tutamak dışında hiçbir parça modül zarfını aşmaz
degis('''    assert d.zmax <= -2.0 and d.xmin >= SAC + 2.0 and d.xmax <= W - SAC - 2.0, "duz blank modul disina tasiyor"''',
      '''    assert d.zmax <= -2.0 and d.xmin >= SAC + 2.0 and d.xmax <= W - SAC - 2.0, "duz blank modul disina tasiyor"
    tasan = []
    for p in PARCALAR:
        if p["grup"] in ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF") or p["grup"].startswith("B_") or "_kulp" in p["ad"]:
            continue
        bb = p["wp"].val().BoundingBox()
        if bb.xmin < -0.5 or bb.xmax > W + 0.5 or bb.ymin < -0.5 or bb.ymax > H + 0.5 or bb.zmin < -D - 0.5 or bb.zmax > 0.5:
            tasan.append(p["ad"])
    print("ZARF (modul %.0f x %.0f x %.0f, tutamaklar haric): %s" % (W, H, D, "hepsi icinde" if not tasan else "TASAN: " + ", ".join(tasan)))
    assert not tasan, "modul zarfini asan parca var"''')
io.open(os.path.join(U, "kutu_cad_v2.py"), "w", encoding="utf-8").write(s)
print("kutu_cad_v2.py yazildi")
