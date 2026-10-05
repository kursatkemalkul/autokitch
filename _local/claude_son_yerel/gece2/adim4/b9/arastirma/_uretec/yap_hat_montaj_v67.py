# -*- coding: utf-8 -*-
"""hat_montaj_v66 → hat_montaj_v67 (28 Eyl 2026) — SAHTE ŞEFFAFLIK YOK (Kemal: "yalıtım malzemesi neden şeffaf, normal yap; ön kapaklar dışında
her şey normal olsun, şeffaf malzeme değilse şeffaflaştırma").
  · yalıtım (PU) opak krem · UNO ürün silindiri ("saydam_celik", gerçekte paslanmaz) opak çelik · TU "pu" opak
  · yer tutucu malzemeler (kutu · katalog · kabin · soğuk · sıcak · robot) opak
  · v52'nin sahte "şeffaf yüzey" panelleri (A · B · C · D · E · K yan / arka / üst / alt) ÜRETİLMEZ — v63'ten beri her istasyonun gerçek sacı var
  · KALAN ŞEFFAFLAR: yalnız ön kapaklar (on_seffaf · sayfadaki çubukla) + gerçek şeffaf malzeme (kaset gövdesi / çıkış tüpü PC "cam")
Çıktılar hat_v67. Tesisat + raf yükleri ayrı sürümü artık v68."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v66.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""v66 (28 Eyl 2026):',
      '"""v67 (28 Eyl 2026): SAHTE ŞEFFAFLIK YOK — yalıtım, UNO silindiri, yer tutucular opak · sahte şeffaf yüzey panelleri kalktı · şeffaf kalan: ön kapaklar + PC kaset · çıktılar hat_v67.' + NL +
      'v66 (28 Eyl 2026):')
degis('pafta="HAT v66 (28 Eyl) ·', 'pafta="HAT v67 (28 Eyl) · SAHTE SEFFAFLIK YOK (yalitim + UNO silindiri + yer tutucular opak, seffaf yuzey panelleri kalkti; seffaf: on kapaklar + PC kaset) · v66:')
degis('print("ALCAK HAT SOZLESMESI (v66 ·', 'print("ALCAK HAT SOZLESMESI (v67 ·')
for a_ in ("hat_v66.glb", "hat_v66.usdz", '"hat_v66"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v66", "v67"))

# yer tutucu malzemeler opak
for ad_, eski, yeni in (("kutu", "renk=(0.62, 0.66, 0.72, 0.30), met=0.0, ruf=0.6, saydam=True", "renk=(0.62, 0.66, 0.72, 1.0), met=0.0, ruf=0.6, saydam=False"),
                        ("katalog", "renk=(0.42, 0.46, 0.52, 0.55), met=0.3, ruf=0.5, saydam=True", "renk=(0.42, 0.46, 0.52, 1.0), met=0.3, ruf=0.5, saydam=False"),
                        ("kabin", "renk=(0.80, 0.83, 0.87, 0.13), met=0.1, ruf=0.4, saydam=True", "renk=(0.80, 0.83, 0.87, 1.0), met=0.1, ruf=0.4, saydam=False"),
                        ("soguk", "renk=(0.25, 0.55, 0.85, 0.28), met=0.0, ruf=0.5, saydam=True", "renk=(0.25, 0.55, 0.85, 1.0), met=0.0, ruf=0.5, saydam=False"),
                        ("sicak", "renk=(0.85, 0.35, 0.22, 0.32), met=0.0, ruf=0.5, saydam=True", "renk=(0.85, 0.35, 0.22, 1.0), met=0.0, ruf=0.5, saydam=False"),
                        ("robot", "renk=(0.96, 0.62, 0.10, 0.75), met=0.2, ruf=0.45, saydam=True", "renk=(0.96, 0.62, 0.10, 1.0), met=0.2, ruf=0.45, saydam=False")):
    degis('MALZEME.setdefault("%s", dict(%s))' % (ad_, eski), 'MALZEME.setdefault("%s", dict(%s))   # v67 opak' % (ad_, yeni))
# yalıtım opak + TU'nun sahte saydamları
degis('MALZEME["yalitim_gorunur"] = dict(renk=(0.95, 0.84, 0.52, 0.38), met=0.0, ruf=0.8, saydam=True)',
      'MALZEME["yalitim_gorunur"] = dict(renk=(0.95, 0.84, 0.52, 1.0), met=0.0, ruf=0.8, saydam=False)   # v67: PU opak (Kemal)' + NL +
      'MALZEME["saydam_celik"] = dict(renk=(0.78, 0.80, 0.83, 1.0), met=0.6, ruf=0.3, saydam=False)       # v67: UNO ürün silindiri gerçekte paslanmaz → opak' + NL +
      'if "pu" in MALZEME: MALZEME["pu"] = dict(MALZEME["pu"], renk=(0.93, 0.86, 0.55, 1.0), saydam=False)  # v67: PU opak')
# sahte şeffaf yüzey panelleri üretilmez (zarf ölçüleri SEF_IST denetimler için kalır)
degis('            parcalar.append(("%s_SEFFAF__%s" % (m_, f_), msh, mal_)); _sef_n += 1',
      '            pass                                                                          # v67: sahte şeffaf yüzey paneli YOK (gerçek sac var)')
compile(s, "hat_montaj_v67.py", "exec")
io.open(os.path.join(U, "hat_montaj_v67.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v67.py yazildi · %d satir" % s.count(NL))
