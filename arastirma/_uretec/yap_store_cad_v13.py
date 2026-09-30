# -*- coding: utf-8 -*-
"""store_cad_v12 → store_cad_v13 (29 Eyl 2026 · YEREL) — Kemal: K4 depo "iki tepsi iç içe gibi" → "tek kap, bölmeli".
K4 KAŞAR + SUCUK DEPOSU = TEK PASLANMAZ KAP: çekmece kutusunun kendisi (304 1,5 · rayda) kap olur, içinde boyuna AYIRICI (1,5) — solda kaşar, sağda sucuk ·
üstünde KAPAK (1,0, içe dönük 10'luk kenar). GN 1/1 + GN 1/2 + sökülür raf + raf tutucuları KALKTI. Bölmeler: kaşar ≈ 24 L (rende 20–22 L da sığar — v12'de
GN 1/1-100 13,5 L'ydi, rende sığmıyordu) · sucuk ≈ 7 L (2 gün 2,8 kg). Önceki: store_cad_v12.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v12.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v12 (29 Eyl 2026 · yap_store_cad_v12.py)',
      '"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v13 (29 Eyl 2026 · yap_store_cad_v13.py): K4 DEPO TEK KAP (çekmece kutusu = kap, ayırıcı + kapak;'
      ' GN kapları + raf kalktı)' + NL + 'v12: ÜRETİM MODELİ v12 (29 Eyl 2026 · yap_store_cad_v12.py)')
a = s.index('    RZ0 = Z_CER0 - 285.0                                                      # −262: raf GN 1/2')
b = s.index('\n\n\ndef _kivrimlar():')
s = s[:a] + '''    # v13 · TEK KAP (Kemal "tek kap, bölmeli"): kutunun kendisi kap · boyuna ayırıcı (solda kaşar, sağda sucuk) · üstte içe kenarlı kapak
    xd = kb - 1.5 - DEPO_SUCUK_W - 1.5                                          # ayırıcının sol yüzü (sucuk bölmesi DEPO_SUCUK_W net)
    ekle("k4_depo_ayirici_1.5", kut(xd, xd + 1.5, kc + 1.5, kd - 11.0, Z0 + 1.5, Z1 - 1.5), "sac", B_, grup=G_,
         bom=("K4 depo ayırıcı 1,5", 1, "304 · kabın tabanına ve ön/arka duvarına kaynaklı · solda kaşar, sağda sucuk", "kapak kenarının 1 altında biter"))
    kp = kut(ka, kb, kd, kd + 1.0, Z0, Z1).union(kut(ka + 1.5, kb - 1.5, kd - 10.0, kd, Z0 + 1.5, Z1 - 1.5).cut(kut(ka + 2.5, kb - 2.5, kd - 11.0, kd + 1.0, Z0 + 2.5, Z1 - 2.5)))
    ekle("k4_depo_kapak_1.0", kp, "sac", B_, grup=G_,
         bom=("K4 depo kapağı 1,0", 1, "304 · kabın duvarlarına oturur, içe dönük 10'luk kenar yerinde tutar · elle kaldırılır", "%.0f × %.0f" % (kb - ka, Z1 - Z0)))''' + s[b:]
degis('DEPO_KUTU_D, DEPO_KUTU_UST = 545.0, 600.0     # v8b · K4 depo çekmece kutusu boyu (GN 1/1 530 + pay) · yan duvar üstü (raf tutucuları taşır)',
      'DEPO_KUTU_D, DEPO_KUTU_UST = 545.0, 600.0     # v8b · K4 depo çekmece kutusu boyu · yan duvar üstü · v13: kutu = KAP (kapak bunun üstünde)' + NL +
      'DEPO_SUCUK_W = 100.0                          # v13: sucuk bölmesi net genişliği (2 gün 2,8 kg küp sucuk · ≈ 7 L) · kalanı kaşar')
degis('''    dk = yb("k4_kapak_depo_fitil"); g12 = yb("k4_depo_GN12_100"); ac1 = Y_TAVAN - 20.5''',
      '''    dk = yb("k4_kapak_depo_fitil"); g12 = yb("k4_depo_kapak_1.0"); ac1 = Y_TAVAN - 20.5          # v13: GN 1/2 yerine kabın kapağı''')
degis('GN 1/2 ustu %.1f -> cekme payi %.1f', 'kap kapagi ustu %.1f -> cekme payi %.1f')
degis('''gn_ = yb("k4_depo_GN11_100")''', '''gn_ = ku_                                            # v13: kap = kutu''')
degis('acikken GN 1/1 arkasi z %+.0f', 'acikken kap arkasi z %+.0f')
degis('''    assert b1 >= 250.0 and b2 >= 250.0 and bag >= ku_.zlen - 5.0 and gn_.zmin + STROK >= Z_ON1 + 10.0, "K4 depo cekmecesi"''',
      '''    assert b1 >= 250.0 and b2 >= 250.0 and bag >= ku_.zlen - 5.0 and gn_.zmin + STROK >= Z_ON1 + 10.0, "K4 depo cekmecesi"
    ay_ = yb("k4_depo_ayirici_1.5"); ic_h = ay_.ymax - (ku_.ymin + 1.5); ic_d = ku_.zlen - 3.0
    v_k = (ay_.xmin - (ku_.xmin + 1.5)) * ic_h * ic_d / 1e6; v_s = ((ku_.xmax - 1.5) - ay_.xmax) * ic_h * ic_d / 1e6
    print("K4 DEPO TEK KAP (v13): kaşar bolmesi %.1f L (rende 20-22 L · blok ~9 L) · sucuk bolmesi %.1f L (2 gun 2,8 kg) · kapak %.1f -> aciklik ustu %.1f"
          % (v_k, v_s, g12.ymax, ac1))
    assert v_k >= 22.0 and v_s >= 4.0 and not [p for p in PARCALAR if p["ad"].startswith(("k4_depo_GN", "k4_depo_raf"))], "v13: K4 depo tek kap degil / hacim yetmiyor"''')
compile(s, "store_cad_v13.py", "exec")
io.open(os.path.join(U, "store_cad_v13.py"), "w", encoding="utf-8").write(s)
print("store_cad_v13.py yazildi")
