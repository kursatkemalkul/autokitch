# -*- coding: utf-8 -*-
"""ADIM 9 · mekanizma_v3_8.json + parca_kutulari.json → v9j. parca_kutulari MODELDEN yeniden eşlenir:
python j_v9j.py mek.json pk.json cak_klasoru cikti_klasoru harf ent41.json [ent42.json] [--tasi tasi.json]
Her kayıt için: kutusunun içinde (±0,6) aynı birimin bir ÜÇGEN merkezi varsa KALIR · yoksa aynı birimde kutu boyu (±0,6 mm, 3 eksen) eşleşen
TEK bileşen varsa kutusu o bileşene GÜNCELLENİR (taşınmış) · yoksa SİLİNİR (modelde yok). Adım 41/42'nin yeni parçaları ent json'dan eklenir.
Bileşenler: govde_denetim_dogru.bilesenler (denetim cak/meta.json'u — son GLB'den kurulmuş olmalı)."""
import sys, os, json, numpy as np
from collections import Counter
arg = [a for a in sys.argv[1:]]
mj, pj, cakd, cik, harf = arg[:5]; EJ = [a for a in arg[5:] if a.endswith(".json")]
sys.path.insert(0, cakd)
os.chdir(os.path.dirname(cakd.rstrip("/\\")))
import c8a_ortak as Mo
J, B, _ = Mo.tum_bilesenler(False)
BY = {}
for b in B:
    BY.setdefault(b.dugum.split("__")[0], []).append(b)
M = json.load(open(mj, encoding="utf-8")); PK = json.load(open(pj, encoding="utf-8"))
say = Counter(); sil = []; tas = []
for birim, L in PK["parca"].items():
    C = BY.get(birim, [])
    if not C:                                                                # denetim dışı birim (ROBOT / İNSAN / ZEMİN) → dokunulmaz
        say["denetim_disi"] += len(L); continue
    Cc = np.concatenate([b.P.mean(1) for b in C])                            # üçgen ağırlık merkezleri (küçük parça büyük bileşene kaynaşmış olabilir)
    Cs = np.array([b.hi - b.lo for b in C]) if C else np.zeros((0, 3))
    yeni = []
    kullan = set()
    for e in L:
        lo = np.array(e[2::2], float); hi = np.array(e[3::2], float)
        if len(Cc) and np.any(np.all((Cc >= lo - 0.6) & (Cc <= hi + 0.6), axis=1)):
            yeni.append(e); say["kalan"] += 1; continue
        s = hi - lo
        aday = [i for i in np.where(np.all(np.abs(Cs - s) <= 0.6, axis=1))[0] if i not in kullan] if len(Cs) else []
        if len(aday) == 1:
            i = aday[0]; kullan.add(i); b = C[i]
            e2 = e[:2] + [round(float(v), 1) for pair in zip(b.lo, b.hi) for v in pair]
            yeni.append(e2); tas.append((birim, e[0])); say["tasinan"] += 1
        else:
            sil.append((birim, e[0])); say["silinen"] += 1
    PK["parca"][birim] = yeni
eklenen = Counter()
for f in EJ:
    e = json.load(open(f, encoding="utf-8"))
    for ad, p in e["parca"].items():
        b = p["dugum"].split("__")[0]
        Lb = PK["parca"].setdefault(b, [])
        Lb[:] = [x for x in Lb if x[0] != ad]
        Lb.append([ad, int(p["kpk"])] + [round(v, 1) for v in p["kutu"]])
        M["parca"]["%s|%s" % (b, ad)] = M["birim"].get(b, "?")
        eklenen[b] += 1
M["glb"] = "hat3_v8.glb (v9%s)" % harf
M["surum"] = M["surum"] + (" · v9%s (4 Eki · adım 9): TOPPING iç geçişler (piston çubuk kovanı, bakır boru soketleri, hortum kelepçe yatakları, "
                           "döner valf yuvaları) · QR Cat6A göz çıkışları ısıtıcı kablosundan ayrı şeritte · B ön çerçeve derz dolgusu · havada kalan "
                           "kanal / kablo / RevPi grupları oturtuldu · parça kutusu listesi modelden yeniden eşlendi · zincir adım 41–42" % harf)
os.makedirs(cik, exist_ok=True)
json.dump(M, open(os.path.join(cik, "mekanizma_v3_8.json"), "w", encoding="utf-8"), ensure_ascii=False)
json.dump(PK, open(os.path.join(cik, "parca_kutulari.json"), "w", encoding="utf-8"), ensure_ascii=False)
json.dump(dict(sayim=say, silinen=sil, tasinan=tas, eklenen=eklenen), open(os.path.join(cik, "pk_yeniden_esleme.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("parca_kutulari:", dict(say), "· eklenen", dict(eklenen), "· toplam", sum(len(v) for v in PK["parca"].values()))
print("silinen birim:", Counter(b for b, _ in sil).most_common(12))
print("taşınan birim:", Counter(b for b, _ in tas).most_common(12))
