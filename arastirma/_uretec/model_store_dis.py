# -*- coding: utf-8 -*-
# AUTOKITCH — 1 · STORE soğuk depo, DIŞ GÖVDE modeli (7 Eyl 2026)
# Deneme modeli: yalnız dış görünüş, gerçek ölçülerle, iç detay yok. Birim mm (SolidWorks'te 1:1 açılır).
# Kaynak: HAT v51 STORE bloğu + ist1_store_detay_v4. Ölçüler cm cinsinden çizimden alınıp ×10 yapıldı.
import cadquery as cq, os

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE"
# ---------------- ana ölçüler (mm) ----------------
W, D, H = 1400.0, 840.0, 1970.0          # dış: 140 × 84 × 197 cm
H_FOOT  = 120.0                           # ayak 12
H_BODY  = 1850.0                          # gövde 185
T_FRONT = 20.0                            # ön yüz (çekmece önü / panel) kalınlığı
GAP     = 6.0                             # çekmece önleri arası fuga
# modül sınırları (ön yüzde)
L0, L1 = 66.0, 690.0                      # sol modül
R0, R1 = 714.0, 1338.0                    # sağ modül
SIDE   = 66.0                             # yan kenar payı
# ---------------- ön yüz elemanları: (ad, x0, x1, z0, z1, tip) ----------------
# tip: 'cekmece' (kulplu çekmece önü) · 'klape' (aşağı açılır klape) · 'panel' (sabit)
FRONT = [
    # üst servis paneli (soğutma ×2, üstten servis)
    ('panel_sogutma',      SIDE, W-SIDE, 1670, 1950, 'panel'),
    ('panel_bant_ust',     SIDE, W-SIDE, 1610, 1664, 'panel'),
    # sol modül +3: içecek çekmeceleri ×4 + 1 L çekmecesi
    ('cekmece_icecek_1',   L0, L1, 1484, 1608, 'cekmece'),
    ('cekmece_icecek_2',   L0, L1, 1354, 1478, 'cekmece'),
    ('cekmece_icecek_3',   L0, L1, 1224, 1348, 'cekmece'),
    ('cekmece_icecek_4',   L0, L1, 1094, 1218, 'cekmece'),
    ('cekmece_1L',         L0, L1,  772, 1088, 'cekmece'),
    # sağ modül +3: taze hamur çekmeceleri ×8 (20 top / çekmece)
    ('cekmece_taze_1',     R0, R1, 1509, 1608, 'cekmece'),
    ('cekmece_taze_2',     R0, R1, 1404, 1503, 'cekmece'),
    ('cekmece_taze_3',     R0, R1, 1299, 1398, 'cekmece'),
    ('cekmece_taze_4',     R0, R1, 1194, 1293, 'cekmece'),
    ('cekmece_taze_5',     R0, R1, 1089, 1188, 'cekmece'),
    ('cekmece_taze_6',     R0, R1,  984, 1083, 'cekmece'),
    ('cekmece_taze_7',     R0, R1,  879,  978, 'cekmece'),
    ('cekmece_taze_8',     R0, R1,  774,  873, 'cekmece'),
    # yatay izoleli ayırıcı (PU 80)
    ('panel_ayirici_PU80', SIDE, W-SIDE,  690,  766, 'panel'),
    # −18 bandı: sol klapeli kaset katı (4 donmuş kap) · sağ boş bant
    ('klape_kaset_kati',   L0, L1,  403,  687, 'klape'),
    ('panel_bos_bant',     R0, R1,  403,  687, 'panel'),
    # −18 donmuş hamur çekmeceleri ×4
    ('cekmece_donmus_1',   L0, L1,  297,  391, 'cekmece'),
    ('cekmece_donmus_2',   L0, L1,  197,  291, 'cekmece'),
    ('cekmece_donmus_3',   R0, R1,  297,  391, 'cekmece'),
    ('cekmece_donmus_4',   R0, R1,  197,  291, 'cekmece'),
    ('panel_bant_alt',     SIDE, W-SIDE,  120,  191, 'panel'),
]
# dikey söveler (ön yüz çerçevesi)
RAILS = [('sove_sol', 0, SIDE), ('sove_orta', L1, R0), ('sove_sag', W-SIDE, W)]

def box(x0, y0, z0, dx, dy, dz):
    return cq.Workplane("XY").box(dx, dy, dz, centered=False).translate((x0, y0, z0))

asm = cq.Assembly(name="STORE_140x84x197")
C_GOVDE, C_CEK, C_KLAPE, C_PANEL, C_AYAK, C_KULP = (0.72,0.74,0.76), (0.86,0.88,0.90), (0.62,0.72,0.88), (0.78,0.79,0.80), (0.35,0.36,0.38), (0.30,0.31,0.33)

# --- gövde (ön yüz 20 mm geride: çekmece önleri o boşluğu doldurur)
govde = box(0, T_FRONT, H_FOOT, W, D - T_FRONT, H_BODY)
asm.add(govde, name="govde_kasa", color=cq.Color(*C_GOVDE))

# --- ayaklar 80×80×120 (4 adet)
for i, (ax, ay) in enumerate([(60, 60), (W-140, 60), (60, D-140), (W-140, D-140)], 1):
    asm.add(box(ax, ay, 0, 80, 80, H_FOOT), name="ayak_%d" % i, color=cq.Color(*C_AYAK))

# --- ön yüz dikey söveleri
for nm, x0, x1 in RAILS:
    asm.add(box(x0, 0, H_FOOT, x1-x0, T_FRONT, H_BODY), name=nm, color=cq.Color(*C_PANEL))

# --- çekmece önleri / klape / paneller
for nm, x0, x1, z0, z1, tip in FRONT:
    w, h = (x1 - x0) - GAP, (z1 - z0) - GAP
    part = box(x0 + GAP/2, 0, z0 + GAP/2, w, T_FRONT, h)
    col = {'cekmece': C_CEK, 'klape': C_KLAPE, 'panel': C_PANEL}[tip]
    # kulp: gövdeden TAŞMAZ — çekmece önüne 12 mm derin gömme tutamak (robot pençesi buradan çeker)
    if tip in ('cekmece', 'klape'):
        kw = min(300.0, w * 0.45) if tip == 'cekmece' else 180.0
        kx = x0 + GAP/2 + (w - kw)/2
        kz = z1 - GAP/2 - 60
        part = part.cut(box(kx, -1, kz, kw, 13, 34))
    asm.add(part, name=nm, color=cq.Color(*col))

os.makedirs(OUT, exist_ok=True)
step = os.path.join(OUT, "STORE_dis_v1.step")
asm.save(step)                                   # STEP AP214 — SolidWorks doğrudan açar
try:
    asm.save(os.path.join(OUT, "STORE_dis_v1.stl"))
except Exception as e:
    print('stl atlandi:', e)
# ---- gölgeli önizleme (kendi görselleştiricimiz) ----
comp = asm.toCompound()
import cq_preview
for nm, eye in (("iso", (1.0,-1.35,0.75)), ("on", (0.0,-1.0,0.10)), ("yan", (1.0,-0.05,0.10))):
    cq_preview.render(asm, os.path.join(OUT, "STORE_dis_v1_%s.svg" % nm), eye=eye)
bb = comp.BoundingBox()
print("STEP:", step)
print("gabari (mm): %.0f x %.0f x %.0f" % (bb.xlen, bb.ylen, bb.zlen))
print("parça sayısı:", len(list(asm.traverse())) - 1)
