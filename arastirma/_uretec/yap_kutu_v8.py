# -*- coding: utf-8 -*-
"""kutu_cad_v7 → kutu_cad_v8 (28 Eyl 2026) — KAPAK MASASI AÇIKÇA İKİ LEVHA (katı denetimi denetim_kati_v1.py · Kemal: "düzelt, onaylıyorum yap").
v7'de 3 mm masa tek parça ("kapak_masasi", BOM 1) yazılıydı ama 26 mm kol yarığı masayı boydan boya kesiyor → gerçekte iki ayrık levha.
Uca köprü konamaz: kol (mil x 560 · y 912 · R 166) çevrimde β 0…144° döner ve masa düzlemini x ≈ 471–726 arasında keser (denetim_kutu_v8_kol.py ölçer;
sol uçta 59 mm'lik köprü denemesi kolla 1 100 mm³'e kadar kesişti). v8: masa AÇIKÇA iki levha — kapak_masasi_0 (arka, z −363…−219) ve kapak_masasi_1
(ön, z −193…−50) · 264 × 143 × 3 · her biri kendi direğine (kapak_masasi_diregi_0 / _1) oturur. Geometri AYNI, yalnız parça ayrımı ve BOM (2 adet).
Çıktılar kutu_modulu_v8 · 5_PACK_kutu_v8. Önceki: kutu_cad_v7.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kutu_cad_v7.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v7 (28 Eyl 2026 gece)',
      '"""AUTOKITCH · E · KUTU KATLAMA · kutu_cad_v8 (28 Eyl 2026 akşam · yap_kutu_v8.py) — KAPAK MASASI AÇIKÇA İKİ LEVHA (kol yarığı boydan boya; kol β 0…144° '
      'masayı x 471–726 arasında keser) · başka değişiklik yok' + NL + 'v7: kutu_cad_v7 (28 Eyl 2026 gece)')
degis('''    ekle("kapak_masasi", m, "sac", bom=("Kapak masası 304 · 3 mm", 1, "264 × 312 · kol yarığı", "üretim"))''',
      '''    for _i8, (_za8, _zb8) in enumerate(((ZL0, KOL_Z[0] - 3.0), (KOL_Z[1] + 3.0, ZL1))):          # v8: yarık boydan boya → açıkça iki levha (v7: tek parça sanılıyordu)
        ekle("kapak_masasi_%d" % _i8, m.intersect(kut(KM_X[0] - 1.0, KM_X[1] + 1.0, KM_UST - 4.0, KM_UST + 1.0, _za8, _zb8)), "sac",
             bom=("Kapak masası levhası 304 · 3 mm", 2, "264 × 143 · aralarında 26 mm kol yarığı (kol β 0…144°, iz x 471–726) · her levha kendi direğine", "üretim") if _i8 == 0 else None)''')
degis('print("OLCUM v7 (on duzlem', 'print("OLCUM v8 (on duzlem')
degis('"generator": "AUTOKITCH kutu_cad_v7"', '"generator": "AUTOKITCH kutu_cad_v8"')
degis('print("E KUTU MODULU v7 (', 'print("E KUTU MODULU v8 (kapak masasi iki levha · ')
degis('print("CAKISMA OZETI v7:', 'print("CAKISMA OZETI v8:')
degis('"kutu_modulu_v7.glb"', '"kutu_modulu_v8.glb"')
degis('"5_PACK_kutu_v7"', '"5_PACK_kutu_v8"')
degis('                ["pano_plakasi_burcu_%d" % i for i in range(4)] + ["sensor_yigin_ustu_braketi", "sensor_blank_var_braketi", "sensor_kutu_dolu_braketi"])', '                ["pano_plakasi_burcu_%d" % i for i in range(4)] + ["sensor_yigin_ustu_braketi", "sensor_blank_var_braketi", "sensor_kutu_dolu_braketi"])' + NL + 'V7_CIKAN = tuple(V7_CIKAN) + ("kapak_masasi",)                                   # v8: kapak masası açıkça iki levha (v7 ↔ v8 farkı beyanı)' + NL + 'V7_YENI = tuple(V7_YENI) + ("kapak_masasi_0", "kapak_masasi_1")')
compile(s, "kutu_cad_v8.py", "exec")
io.open(os.path.join(U, "kutu_cad_v8.py"), "w", encoding="utf-8").write(s)
print("kutu_cad_v8.py yazildi · %d satir" % s.count(NL))
