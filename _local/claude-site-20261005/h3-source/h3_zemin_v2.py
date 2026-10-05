# -*- coding: utf-8 -*-
"""HAT v3.6 · DÜKKÂN ZEMİNİ v2 (1 Eki 2026 · Claude · YEREL) — montajda 'import h3_zemin_v2 as ZM' (GERCEK_DIS sözleşmesi: kur() · PARCALAR · dunya(p) · BIRIMLER · BIRIM_MODUL · MALZEME).
Kemal 1 Eki: "bozuk zemini yeniden modelle". v3.5'e kadar montajda AYRI BİR ZEMİN PARÇASI YOKTU: yer düzlemi olarak görünen; robot rayının yarı saydam
katalog kutusu (ROBOT_RAY, y 0–60), zincir oluğu (936–5100 × z 485–575, üstü yalnız 3020–5100 arası kapaklı), robot kablo köprüsü, elektrik zemin üstü kanalı ve
sayfanın ızgara çizgileriydi → parça parça, boşluklu, kesik bir "zemin" izlenimi.
v2: TEK DÜZEN KARO ZEMİN · üst yüz y = 0 (bütün ayaklar, oluklar, kanallar bunun ÜSTÜNDE) · 600 × 600 × 10 porselen karo, 3 mm derz · altında 20 mm şap.
Alan: makinenin bütün izdüşümü + koridor (QR dolabı, tezgâh, bina bağlantı kutusu) + 180 cm insan figürü (x −550):
  x −864 … 6336 (12 karo) · z −830 (arka duvar) … 2170 (5 karo; tezgâh önü 1880 + 290 pay).
Yalnız görsel/çevre (kategori DÜKKÂN); makine denetimlerine girmez. Ayak pabuçlarının alt yüzü katalogda −0,6 (lastik ezilme payı) → karoya 0,6 mm gömülü görünür (bilinçli)."""
import cadquery as cq

KARO, DERZ, T_KARO, T_SAP = 600.0, 3.0, 10.0, 20.0
NX, NZ = 12, 5
X0, Z0 = -864.0, -830.0
X1, Z1 = X0 + NX * KARO, Z0 + NZ * KARO
BIRIMLER = [("ZEMIN_DOSEME", "Dükkân zemini (v3.6): 600 × 600 × 10 porselen karo, 3 mm derz, 20 mm şap · üst yüz y 0 · x %.0f…%.0f · z %.0f…%.0f · makine + koridor + tezgâh tek düzen" % (X0, X1, Z0, Z1))]
BIRIM_MODUL = {"ZEMIN_DOSEME": "-"}
MALZEME = {"zemin_karo": dict(renk=(0.86, 0.86, 0.84, 1.0), met=0.0, ruf=0.85),
           "zemin_sap": dict(renk=(0.32, 0.33, 0.34, 1.0), met=0.0, ruf=0.95)}
PARCALAR = []


def _kut(x0, x1, y0, y1, z0, z1):
    return cq.Workplane(obj=cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0)))


def kur():
    PARCALAR[:] = []
    PARCALAR.append(dict(ad="zemin_sap", birim="ZEMIN_DOSEME", mal="zemin_sap", grup="SABIT",
                         wp=_kut(X0, X1, -T_KARO - T_SAP, -T_KARO, Z0, Z1)))
    h = DERZ / 2.0
    for i in range(NX):
        for k in range(NZ):
            xa, za = X0 + i * KARO, Z0 + k * KARO
            # kenar karolarda dış kenara derz bırakılmaz (alan dikdörtgeni tam dolu, kenar düz)
            x0 = xa + (h if i > 0 else 0.0); x1 = xa + KARO - (h if i < NX - 1 else 0.0)
            z0 = za + (h if k > 0 else 0.0); z1 = za + KARO - (h if k < NZ - 1 else 0.0)
            PARCALAR.append(dict(ad="zemin_karo_%02d_%d" % (i, k), birim="ZEMIN_DOSEME", mal="zemin_karo", grup="SABIT",
                                 wp=_kut(x0, x1, -T_KARO, 0.0, z0, z1)))
    # denetim: üst yüz tek düzlem y 0, karolar üst üste binmez, şap tam altta
    ys = set(round(p["wp"].val().BoundingBox().ymax, 3) for p in PARCALAR if p["ad"].startswith("zemin_karo"))
    assert ys == {0.0}, ys
    assert len(PARCALAR) == 1 + NX * NZ
    return PARCALAR


def dunya(p):
    return p["wp"].val()


if __name__ == "__main__":
    kur()
    b = cq.Compound.makeCompound([dunya(p) for p in PARCALAR]).BoundingBox()
    print("h3_zemin_v2 · %d parça · x %.0f…%.0f · y %.0f…%.0f · z %.0f…%.0f" % (len(PARCALAR), b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))
