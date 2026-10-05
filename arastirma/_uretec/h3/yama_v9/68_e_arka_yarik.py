# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 68 · E GÖVDESİ: ARKA SAC ALT / ÜST DÖNÜŞ DELİKLERİ ÖNE AÇIK YARIK (5 Eki 2026 · Claude · bulut oturumu · E montaj v2)
python 68_e_arka_yarik.py girdi.glb cikti.glb      (zincir: hat3_v10i.glb → hat3_v10j.glb)

Montaj sırası denetimi (E v2): adım 35'in E gövde bağlantıları üç eksende preslenmiş saplama —
  yanlar ↔ arka: arka sacda saplama (z) · taban → arka alt dönüşü: tabanda saplama (y, yukarı) · üst → arka üst dönüşü: üst sacta saplama (y, aşağı).
Arka sac yan dönüşlere z ekseninde arkadan sürülmek zorunda; alt / üst dönüşündeki Ø5,5 delikler ise dik (y) saplamalara geçiyor → arka sac
taban ve üst saplamalarını eksenine dik süpürür, kurulamaz.
Çözüm (F adım 67 ile aynı yöntem): arka sacın alt dönüşündeki 5 ve üst dönüşündeki 5 delik ÖNE AÇIK YARIK (genişlik 5,5 = delik çapı,
delik merkezinden dönüşün ön kenarına, z −815 → −806). Arka sac arkadan sürülür, yarıklar dik saplamalara geçer; içteki pul + fiberli somun aynı.
Saplama ↔ yarık kenarı: somun pulu (Ø10) yarığı örter (yarık 5,5).
Denetim (bu betikte): her kesici yalnız E_GOVDE__sac'ın arka sac bileşenini keser (taban / üst sacla hacim 0) · 10 yarık açılır."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
XS_ALT = (4470.0, 4642.5, 4815.0, 4987.5, 5160.0)                               # govde_bag_taban_arka_{70,242,415,587,760}
XS_UST = (4450.0, 4632.5, 4815.0, 4997.5, 5180.0)                               # govde_bag_ust_arka_{50,232,415,597,780}
ZC, ZON, R = -815.0, -805.0, 2.75                                              # delik merkezi · dönüş ön kenarı −806 (+1 taşar) · Ø5,5
Y_ALT = (126.0, 127.5)                                                          # alt dönüş 126,0–127,5 (taban üstü / pul altı: temas, hacim 0)
Y_UST = (1858.5, 1860.0)                                                        # üst dönüş 1858,5–1860,0 (üst sac 1860,5)


def yarik(x, y0, y1):
    return cq.Workplane("XY").box(2 * R, y1 - y0, ZON - ZC, centered=False).translate((x - R, y0, ZC)).val()


KES = [dict(ad="arka_yarik_alt_%d" % i, sh=yarik(x, *Y_ALT)) for i, x in enumerate(XS_ALT)] + \
      [dict(ad="arka_yarik_ust_%d" % i, sh=yarik(x, *Y_UST)) for i, x in enumerate(XS_UST)]
g = Glb(gi)
K = SE.Karsi(g, haric_onek=("E_GOVDE__celik",))                                 # saplama / pul / somun yarıktan geçer, kesilmez
for p in KES:
    m, P = SE.kesici(p)
    hed = K.tara(p, m, P)
    assert len(hed) == 1 and hed[0][0] == "E_GOVDE__sac", "ADIM 68 DUR: %s yalnız arka sacı kesmeli: %s" % (p["ad"], [(d, b["no"], v) for d, b, v in hed])
    b = hed[0][1]
    assert b["lo"][2] < -829.0 and b["hi"][2] > -807.0 and b["hi"][0] - b["lo"][0] > 800, "ADIM 68 DUR: %s arka sac değil %s %s" % (p["ad"], b["lo"], b["hi"])
kayit = K.delik_ac(KES)
assert sum(len(k.get("eleman", [])) for k in kayit) == len(KES), "ADIM 68 DUR: açılmayan yarık"
tmp = go + ".e1.glb"; g.kaydet(tmp); del g, K
SE.sikistir(tmp, go); os.remove(tmp)
LOG("ADIM 68 bitti · %s · %d yarık · %.0f sn" % (go, len(KES), time.time() - t0))
sys.stdout.flush(); os._exit(0)
