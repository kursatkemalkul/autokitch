# -*- coding: utf-8 -*-
"""KASET KONTROL LİSTESİ · küp sucuk v7 → v8 karşılaştırması (28 Eyl 2026 · örümcek kaynak yakaları · Kemal: "düzelt, onaylıyorum yap").
kaset_kontrol.py'nin kasete özgü maddeleri (A · B · J · K · C · D · E · F) AYNEN, ama KASET listesi yayındaki sucuk_cad_v7 ve yeni sucuk_cad_v8.
Kural: v7'de GEÇEN her madde v8'de de GEÇMELİ; v7'de zaten KALAN maddeler "önceden var" diye ayrı yazılır. H (dört kaset birlikte) maddeleri
bu karşılaştırmaya girmez (kaset_kontrol.py hâlâ birleşim v1 dönemi sürümlerini — kaşar v10 · kıyma v5 · kuşbaşı v4 · sucuk v3 — sayıyor).
Kullanım: python kaset_kontrol_sucuk_v8.py (sayfa F maddeleri için kaset3d/index.html sucuk_v8 sekmeleriyle güncellenmiş olmalı)."""
import io, os, re, sys
U = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(U, "kaset_kontrol.py"), encoding="utf-8").read()
a = src.index("KASET = [dict("); b = src.index("SONUC = []", a)
src = src[:a] + '''KASET = [dict(ad="KÜP SUCUK v7 (yayında)", cad="sucuk_cad_v7", onek="sucuk_v7", klasor="sucuk_kaseti_v7", model="sucuk_akis_model_v1", kg=2.8, akis="akis_sucuk.html", rotor=True),
         dict(ad="KÜP SUCUK v8 (yeni)", cad="sucuk_cad_v8", onek="sucuk_v8", klasor="sucuk_kaseti_v8", model="sucuk_akis_model_v1", kg=2.8, akis="akis_sucuk.html", rotor=True)]
''' + src[b:]
h0 = src.index("# ---------- H · "); h1 = src.index("gec = sum(")
src = src[:h0] + src[h1:]
src = src.replace('io.open(os.path.join(U, "kaset_kontrol_sonuc.json")', 'io.open(os.path.join(U, "kaset_kontrol_sucuk_v8_sonuc.json")')
src = src.replace("sys.stdout.flush(); os._exit(0 if gec == len(SONUC) else 1)", "sys.stdout.flush()")
sys.argv = [os.path.join(U, "kaset_kontrol.py")]
G = {"__name__": "__main__", "__file__": os.path.join(U, "kaset_kontrol.py")}
exec(compile(src, "kaset_kontrol.py[sucuk v7↔v8]", "exec"), G)
SONUC = G["SONUC"]
v7 = {s_[1]: s_ for s_ in SONUC if s_[0].startswith("KÜP SUCUK v7")}
v8 = {s_[1]: s_ for s_ in SONUC if s_[0].startswith("KÜP SUCUK v8")}
print("\nKARŞILAŞTIRMA v7 → v8 (madde madde)")
bozulan, duzelen, once = [], [], []
for no in v7:
    a7, a8 = v7[no][3], v8.get(no, (None, None, None, False, "YOK"))[3]
    if a7 and not a8: bozulan.append(no)
    if not a7 and a8: duzelen.append(no)
    if not a7 and not a8: once.append(no)
    print("  %-3s v7 %-5s → v8 %-5s  %s   ‖ v8: %s" % (no, "GEÇTİ" if a7 else "KALDI", "GEÇTİ" if a8 else "KALDI", v7[no][2][:70], v8.get(no, ("", "", "", "", ""))[4]))
print("\nSONUÇ · bozulan (v7 geçiyordu, v8 kaldı): %s · düzelen: %s · önceden var (ikisinde de KALDI): %s" % (bozulan or "YOK", duzelen or "yok", once or "yok"))
sys.stdout.flush(); os._exit(1 if bozulan else 0)
