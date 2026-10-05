# -*- coding: utf-8 -*-
"""hat_montaj_v63 → hat_montaj_v64 (28 Eyl 2026) — TOPPING DENETİM DÜZELTMELERİ (denetim_C.md · Kemal: "A yap", iki kararda da (a)):
  (1a) kaset U-yarıkları: tüpe sıkılı POM yarık dili kasetle birlikte çıkar → soğuk oda tabanında ürün kanalları dışında açık alan 0 (v63: ≈21 350 mm²)
  (2a) K1 | K2 arası katlanır flipper: kam oluklu kılavuz + burulma yayı, K2 kapalıyken K1 açılır; kapak menteşeleri sanal pivot ön dış köşede
  + menteşe tabanları yan sac ön dönüşünde · teknik cep L taşıyıcı · T çerçevesi takozu · yarık bantları · itici alt lama · eski TC parçaları BOM dışı ·
  mandallar simetrik. Üreteçler aynı dosya adlarıyla (topping_uno_cad_v14 v14b · topping_cad_v25 v25b · itici_cad_v5) yeniden koşuldu; montajda yalnız
  metin + çıktı adları değişir. Çıktılar hat_v64."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v63.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""v63 (28 Eyl 2026):',
      '"""v64 (28 Eyl 2026): TOPPING DENETİM DÜZELTMELERİ (Kemal: "A yap") — kaset yarık dili (soğuk oda tabanı kapalı) · katlanır flipper + ön köşe pivotlu menteşeler ·' + NL +
      '  teknik cep taşıyıcısı · itici alt lama · çıktılar hat_v64.' + NL +
      'v63 (28 Eyl 2026):')
degis('pafta="HAT v63 (28 Eyl) ·', 'pafta="HAT v64 (28 Eyl) · TOPPING DENETIM DUZELTMELERI (kaset yarik dili: soguk oda tabani kapali · katlanir flipper · on kose pivotlu menteseler) · v63:')
degis('print("ALCAK HAT SOZLESMESI (v63 ·', 'print("ALCAK HAT SOZLESMESI (v64 ·')
for a_ in ("hat_v63.glb", "hat_v63.usdz", '"hat_v63"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v63", "v64"))
compile(s, "hat_montaj_v64.py", "exec")
io.open(os.path.join(U, "hat_montaj_v64.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v64.py yazildi · %d satir" % s.count(NL))
