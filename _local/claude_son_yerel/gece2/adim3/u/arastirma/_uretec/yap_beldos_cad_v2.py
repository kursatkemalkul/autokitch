# -*- coding: utf-8 -*-
"""beldos_cad_v1 → beldos_cad_v2 (28 Eyl 2026) — SAHTE ŞEFFAFLIK YOK (Kemal: "ön kapaklar dışında her şey normal olsun, şeffaf malzeme değilse
şeffaflaştırma").
  · UNO ürün silindiri Ø52 (gerçekte paslanmaz) → opak paslanmaz
  · UNO kasa kutu sacı (gerçekte paslanmaz sac) → opak fırçalı paslanmaz
  · bizim bağlantı plakası → opak mavi
  · şartlandırıcı filtre kabı → gerçek PC kap (şeffaf kalır, "pc")
  · GERÇEK şeffaflar aynen: Mini-fill dolum ünitesi (PC) · 15 L hazne (yarı saydam PP)
Geometri, ölçüler, animasyon, denetimler v1 ile aynı. Çıktılar _v2 adlarıyla (v1 dosyaları yerinde kalır)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "beldos_cad_v1.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('3B MODEL v1 (25 Eyl 2026)', '3B MODEL v2 (28 Eyl 2026) · v1 (25 Eyl 2026)')
degis('STEP / SolidWorks çıktısı YOK',
      'v2 (28 Eyl 2026 · Kemal: "şeffaf malzeme değilse şeffaflaştırma"): UNO ürün silindiri, kasa kutu sacı ve bizim bağlantı plakası OPAK;' + NL +
      '  şartlandırıcı filtre kabı gerçek PC kap ("pc"); şeffaf kalan yalnız gerçek şeffaflar (dolum ünitesi PC, 15 L hazne PP, filtre kabı PC).' + NL +
      'STEP / SolidWorks çıktısı YOK')
degis('ÇIKTI: otonom/hat3d/beldos_minifill_ep_v1.glb · beldos_uno275_v1.glb · beldos_v1.json',
      'ÇIKTI: otonom/hat3d/beldos_minifill_ep_v2.glb · beldos_uno275_v2.glb · beldos_v2.json')
degis('"saydam_celik": dict(renk=(0.82, 0.85, 0.89, 0.32), met=0.6, ruf=0.25, saydam=True),',
      '"saydam_celik": dict(renk=(0.80, 0.82, 0.85, 1.0), met=0.95, ruf=0.26),                  # v2: opak paslanmaz (ad geriye uyum için)')
degis('"kabuk":        dict(renk=(0.78, 0.81, 0.85, 0.24), met=0.4, ruf=0.35, saydam=True),',
      '"kabuk":        dict(renk=(0.74, 0.76, 0.79, 1.0), met=0.9, ruf=0.42),                   # v2: opak fırçalı paslanmaz sac')
degis('"bizim":        dict(renk=(0.30, 0.55, 0.95, 0.45), met=0.0, ruf=0.6, saydam=True),',
      '"bizim":        dict(renk=(0.30, 0.55, 0.95, 1.0), met=0.0, ruf=0.6),                    # v2: opak mavi')
degis('not_="Ø52 (30–151 ml) [B]; boy [Ö]; içi görünsün diye SAYDAM çizildi (gerçekte paslanmaz)")',
      'not_="Ø52 (30–151 ml) [B]; boy [Ö]; paslanmaz (v2: opak)")')
degis('UN.ekle("kasa_kutu_saci", kasa, "kabuk", "Ö", not_="içi görünsün diye SAYDAM çizildi (gerçekte paslanmaz sac)")',
      'UN.ekle("kasa_kutu_saci", kasa, "kabuk", "Ö", not_="paslanmaz sac (v2: opak)")')
degis('UN.ekle("sartlandirici_filtre_kabi", silz(rc[0], rc[1], 15.0, 3.0, 68.0), "saydam_celik", "Ö+V")',
      'UN.ekle("sartlandirici_filtre_kabi", silz(rc[0], rc[1], 15.0, 3.0, 68.0), "pc", "Ö+V", not_="şeffaf PC filtre kabı (gerçek şeffaf)")')
for a_ in ("beldos_minifill_ep_v1.glb", "beldos_uno275_v1.glb", "beldos_v1.json", 'surum="beldos_cad_v1'):
    n_ = s.count(a_)
    assert n_ >= 1, a_
    s = s.replace(a_, a_.replace("v1", "v2"))
compile(s, "beldos_cad_v2.py", "exec")
io.open(os.path.join(U, "beldos_cad_v2.py"), "w", encoding="utf-8").write(s)
print("beldos_cad_v2.py yazildi · %d satir" % s.count(NL))
