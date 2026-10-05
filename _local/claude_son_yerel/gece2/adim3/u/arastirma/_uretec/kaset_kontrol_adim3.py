# -*- coding: utf-8 -*-
"""ADIM 3 (gece 2) · kaset_kontrol.py maddeleri AYNEN, KASET listesi modeldeki güncel kasetlerle: python kaset_kontrol_adim3.py yeni|eski
yeni = kaşar v15 · kıyma v5 · kuşbaşı v4 · küp sucuk v9   ·   eski = kaşar v14 · kıyma v5 · kuşbaşı v4 · küp sucuk v8 (karşılaştırma için)"""
import io, os, sys
U = os.path.dirname(os.path.abspath(__file__)); hal = sys.argv[1]
src = io.open(os.path.join(U, "kaset_kontrol.py"), encoding="utf-8").read()
a = src.index("KASET = [dict("); b = src.index("SONUC = []", a)
kv, sv = ("v15", "v9") if hal == "yeni" else ("v14", "v8")
yeni = ('KASET = [dict(ad="KAŞAR KABI %s", cad="kasar_cad_%s", onek="kasar_%s", klasor="kasar_kabi_%s", model=None, kg=8.8, akis="akis.html", rotor=False),\n' % (kv, kv, kv, kv) +
        '         dict(ad="KIYMA KASETİ v5", cad="kiyma_cad_v5", onek="kiyma_v5", klasor="kiyma_kaseti_v5", model="kiyma_akis_model_v2", kg=6.4, akis="akis_kiyma.html", rotor=True),\n'
        '         dict(ad="KUŞBAŞI KASETİ v4", cad="kusbasi_cad_v4", onek="kusbasi_v4", klasor="kusbasi_kaseti_v4", model="kusbasi_akis_model_v2", kg=5.8, akis="akis_kusbasi.html", rotor=True),\n' +
        '         dict(ad="KÜP SUCUK KASETİ %s", cad="sucuk_cad_%s", onek="sucuk_%s", klasor="sucuk_kaseti_%s", model="sucuk_akis_model_v1", kg=2.8, akis="akis_sucuk.html", rotor=True)]\n' % (sv, sv, sv, sv))
src = src[:a] + yeni + src[b:]
src = src.replace('io.open(os.path.join(U, "kaset_kontrol_sonuc.json")', 'io.open(os.path.join(U, "kaset_kontrol_adim3_%s.json")' % hal)
_e = 'ak = io.open(os.path.join(K3, K["akis"]), encoding="utf-8").read()'
assert src.count(_e) == 1
src = src.replace(_e, 'ak = io.open(os.path.join(K3, K["akis"]), encoding="utf-8").read() if os.path.exists(os.path.join(K3, K["akis"])) else ""   # adim3: sayfa dosyası 28 Eyl site temizliğinde kalktıysa madde KALIR')
sys.argv = [os.path.join(U, "kaset_kontrol.py")]
exec(compile(src, "kaset_kontrol.py[adim3 %s]" % hal, "exec"), {"__name__": "__main__", "__file__": os.path.join(U, "kaset_kontrol.py")})
