# -*- coding: utf-8 -*-
"""teknik_acici_alani_v3 → v4 (28 Eyl 2026) — Kemal: "mavi iki kutuya ayırmışsın; tek mavi kutu, birleştir, kullanılabilir alan de."
Üst hacim (Z1) + arka hacim (Z2) tek mavi alan (L kesit): aralarında çizgi yok, tek etiket "KULLANILABİLİR ALAN"; ölçü zincirleri aynı."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_acici_alani_v3.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


degis('"""AÇICI ALANI · tedarikçi paftası v3 (28 Eyl 2026)',
      '"""AÇICI ALANI · tedarikçi paftası v4 (28 Eyl 2026) — Kemal: "mavi iki kutuyu birleştir, tek kutu, kullanılabilir alan de" → Z1 + Z2 tek mavi L alan.' + NL + 'v3 (28 Eyl 2026)')
degis('"ACICI_ALANI_v3_TR.png" if TR else "ACICI_ALANI_v3.png"', '"ACICI_ALANI_v4_TR.png" if TR else "ACICI_ALANI_v4.png"')
degis('"Kemal Kul · 28.09.2026 · ACICI_ALANI v3"', '"Kemal Kul · 28.09.2026 · ACICI_ALANI v4"')
degis('DL("BLUE = the machine may use this space", "MAVİ = makine bu alanı kullanabilir")',
      'DL("BLUE = USABLE SPACE for the machine", "MAVİ = KULLANILABİLİR ALAN (makine burayı kullanabilir)")')
# önden: tek mavi dikdörtgen (arka kısım 893,5'e iner) — kırmızı ve kesikli üstüne çizilir
degis("fbox(Z1, C_Z1, BLUE, 2)" + NL + "rect((fx(XI0), fy(Y_REST)), (fx(XI1), fy(Y_FL)), C_Z2, None)",
      "rect((fx(XI0), fy(Y_KUS)), (fx(XI1), fy(Y_FL)), C_Z1, BLUE, 2)                                  # v4: tek mavi alan")
degis('txt((fx(350), fy(1500)), DL("MACHINE SPACE", "MAKİNE ALANI"), f14, BLUE)', 'txt((fx(350), fy(1500)), DL("USABLE SPACE", "KULLANILABİLİR ALAN"), f14, BLUE)')
degis('txt((fx(350), fy(1462)), "638 × 670,5" if TR else "638 × 670.5", f10, BLUE)' + NL, '')
degis('DL("(behind: also down to 893.5, see side view)", "(arkada 893,5\'e kadar iner, yan görünüşe bak)")',
      'DL("(below 1160 only in the back part, see side view)", "(1160 altında yalnız arka kısım, yan görünüşe bak)")')
# yandan: L biçimli tek alan
degis("sbox(Z1, C_Z1, BLUE, 2); sbox(Z2, C_Z1, BLUE, 2)",
      "d.polygon([(sz(Z_BI), fy(Y_FL)), (sz(Z_MEK), fy(Y_FL)), (sz(Z_MEK), fy(Y_REST)), (sz(Z_FI), fy(Y_REST)), (sz(Z_FI), fy(Y_KUS)), (sz(Z_BI), fy(Y_KUS))],"
      " fill=C_Z1, outline=BLUE, width=2)                                                  # v4: tek L alan")
degis('txt((sz(-250), fy(1500)), DL("MACHINE SPACE", "MAKİNE ALANI"), f14, BLUE)', 'txt((sz(-395), fy(1500)), DL("USABLE SPACE", "KULLANILABİLİR ALAN"), f14, BLUE)')
degis('txt((sz(-652), fy(1250)), DL("BACK", "ARKA"), f10, BLUE); txt((sz(-652), fy(1220)), DL("full height", "tam boy"), f9, BLUE)' + NL, '')
degis('txt((sz(-652), fy(1190)), DL("(column / fixing)", "(kolon / bağlantı)"), f9, BLUE)' + NL, '')
# üstten: tek dikdörtgen, bölme çizgisi yok
degis("tbox(Z2, C_Z1, BLUE, 2); tbox(Z1, C_Z2, BLUE, 2)", "rect((fx(XI0), tz(Z_BI)), (fx(XI1), tz(Z_FI)), C_Z1, BLUE, 2)                                  # v4: tek mavi alan")
degis('txt((fx(350), tz(-652) - 12), DL("BACK: full height 893.5–1830.5", "ARKA: tam boy 893,5–1830,5"), f10, BLUE)',
      'txt((fx(350), tz(-700) - 12), DL("USABLE SPACE", "KULLANILABİLİR ALAN"), f14, BLUE)')
degis('txt((fx(350), tz(-652) + 16), "638 × 293,5" if TR else "638 × 293.5", f9, BLUE)',
      'txt((fx(350), tz(-700) + 20), DL("back 293.5: full height 893.5–1830.5 · front: above 1160", "arka 293,5: tam boy 893,5–1830,5 · ön: 1160 üstü"), f9, BLUE)')
degis('txt((fx(100), tz(-420)), DL("above 1160", "1160 üstü"), f9, BLUE)' + NL, '')
# 3D: tek L prizma
degis("kutu3(Z2, C_Z1, BLUE); kutu3(MEK, C_RED, RED); kutu3(YOL, C_RED, RED)", "kutu3(MEK, C_RED, RED); kutu3(YOL, C_RED, RED)")
degis("kutu3(Z1, C_Z1, BLUE)" + NL,
      "def kutuL(fill, out, a=110, w=2):" + NL +
      "    x0, x1 = XI0, XI1; zb, zm, zf = Z_BI, Z_MEK, Z_FI; y0, ym, yt = Y_FL, Y_REST, Y_KUS" + NL +
      "    yuz = [[P(x0, zb, yt), P(x1, zb, yt), P(x1, zf, yt), P(x0, zf, yt)]," + NL +
      "           [P(x1, zb, y0), P(x1, zm, y0), P(x1, zm, ym), P(x1, zf, ym), P(x1, zf, yt), P(x1, zb, yt)]," + NL +
      "           [P(x0, zf, ym), P(x1, zf, ym), P(x1, zf, yt), P(x0, zf, yt)]," + NL +
      "           [P(x0, zm, y0), P(x1, zm, y0), P(x1, zm, ym), P(x0, zm, ym)]]" + NL +
      "    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)" + NL +
      "    for poly in yuz:" + NL +
      "        g.polygon(poly, fill=fill + (a,))" + NL +
      "    im.alpha_composite(lay)" + NL +
      "    for poly in yuz:" + NL +
      "        d.line(poly + [poly[0]], fill=out, width=w)" + NL +
      "kutuL(C_Z1, BLUE)" + NL)
compile(s, "teknik_acici_alani_v4.py", "exec")
io.open(os.path.join(U, "teknik_acici_alani_v4.py"), "w", encoding="utf-8").write(s)
print("teknik_acici_alani_v4.py yazildi")
