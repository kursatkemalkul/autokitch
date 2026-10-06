# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 84 · E PARMAK (Y ekseni kol) + ARKA İTİCİ / PİSTON MEKANİZMALARI VİDALI (6 Eki 2026 · Claude · 2. oturum · E mekanizma montajı · KURALLAR §1.2 / §2.2 / §5)
python 84_e_parmak_itici.py girdi.glb cikti.glb      (zincir: hat3_v10o.glb → hat3_v10p.glb)

E_PARMAK (15 parça: L taşıyıcı (+ kasnak bloğu tek parça), motor braketi (6 mm plaka + taban), NEMA 23 motor (+ arka kapak / arka mil), motor kasnağı, göbek (4 mm plaka + Ø12 mil),
kasnak, 2 flanşlı rulman diski (GEÇME), kayış, sensör laması + 3 mm braketi + M8 sensör, kol (ray + 2 dikme + 3 mm plaka), 2 mm bıçak)
E_PISTON (27 parça: sabit 5 mm taşıyıcı plaka + 2 MGN15 ray + 4 araba, 10 mm piston plakası, 20 mm piston başı, 2 lama (8 × 50), somun braketi + flanşlı somun (GEÇME),
üst yatak bloğu + 2 yatak plakası, vida mili + kasnak, motor bloğu (4 mm flanş + 2 direk) + NEMA 23 motor + kasnak + kayış, 2 üst L blok (3 mm), sensör bloğu + M8 sensör)
— envanterde bağlantı elemanı 0.
  İTİCİ: raylar taşıyıcıya kendi deliklerinden 8 × M4 · arabalar piston plakasına 4 × M4 (araba dişli) · somun braketi plakanın arkasından 2 × M5 · piston başı ↔ plaka alt kenarı
  TIG köşe dikişi (3 parça, lamalar arası) · lamalar başa alttan 4 × havşa M5 · üst L bloklar taşıyıcıya 2 × havşa M4 + besleyici plakasına 2 × M4 · sensör bloğu taşıyıcıya 2 × havşa M4
  + M8 somunları · yatak plakası 1 üst yatak bloğuna alttan 2 × M4×40 · yatak plakası 0 ve motor bloğu direkleri taşıyıcıya 3 yeni 2 mm Z köşebentle (M4) ·
  motor flanş plakasına 4 × M4 (4 mm plaka) · vida mili kasnağı radyal Ø3 pim · motor kasnağı mil ucu M3 (ürün notu) ·
  PARMAK: taşıyıcı ayağı lama 0'a 4 × M5 · motor braketi tabanı lama 1'e 4 × M5 · motor 6 mm plakaya 4 × M5 · kasnaklar setskur M4 · sensör laması plakaya 2 × M4 ·
  sensör braketi lamaya TIG punta · sensör: dışta ISO 4032, içte lamaya açılan cepte ISO 4035 ince somun · kol rayı göbek plakasına TIG punta · bıçak kola 4 × havşa M3.
Hazır ürün (motor / ray / araba / sensör / rulman): ürüne dokunulmaz, bizim parça dişli; ray ve araba vidaları ürünün kendi deliklerinden (KURALLAR §3).
Denetim (betikte): baş / somun / segman / yeni parça hacmi boş · her vida tam olarak A + B'yi deliyor · diş tutuşu ≥ 1 × d · boy katalogdan."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq
import e_mek_bag as MB

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
g = Glb(gi)
M = MB.Mek(g, (4460, 1300, -430), (4820, 1870, 35))
Y, YM, X, XM, Z, ZM = (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)


def kutu(x0, y0, z0, x1, y1, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


# ---------------------------------------------------------------- İTİCİ (sabit taşıyıcı) · raylar · arabalar · piston plakası
for i, xr in ((0, 4600.0), (1, 4740.0)):
    M.vida("itici_ray_%d_vida" % i, "itici_ray_%d" % i, "itici_tasiyici", dis="M4", yon=ZM, duzlem=-389.0, pts=[(xr, 1380.0 + 60.0 * k) for k in range(8)],
           kavrama=5.0, urun="A", bas_bos=False, gomme=5.0, not_="MGN15 rayı kendi deliklerinden (60 mm aralık, havşa yuvalı) 5 mm taşıyıcı plakaya (dişli)")
for i, (xc, yc) in ((0, (4600.0, 1750.0)), (1, (4600.0, 1810.0)), (2, (4740.0, 1750.0)), (3, (4740.0, 1810.0))):
    M.vida("piston_araba_%d_vida" % i, "piston_plaka", "piston_araba_%d" % i, dis="M4", std="DIN7991", yon=ZM, duzlem=-361.0, pts=[(xc + fx * 8.0, yc + fy * 10.0) for fx in (-1, 1) for fy in (-1, 1)],
           kavrama=5.0, not_="10 mm piston plakasından (havşa; üst arabanın başları motor flanş plakasının altında kalıyor) MGN15C arabasının 4 dişli deliğine (ürün)")
M.vida("piston_somun_braketi_vida", "piston_plaka", "piston_somun_braketi", dis="M5", yon=Z, duzlem=-351.0, pts=[(4643.0, 1779.0), (4697.0, 1779.0)],
       not_="plakanın arkasından (başlar plaka ile taşıyıcı arasında) 52 mm somun braketine")
# piston başı ↔ piston plakası: baş plakanın alt kenarına köşe teması ile bitişik (üreteç) → iç köşeye 3 parça TIG köşe dikişi (lamaların dışında)
for i, (x0, x1) in enumerate(((4576.0, 4594.0), (4606.0, 4714.0), (4726.0, 4764.0))):
    M.yeni("piston_bas_kaynak_%d" % i, kutu(x0, 1330.0, -351.0, x1, 1334.0, -347.0).val(),
           ["TIG 141 köşe dikişi a 4 · ER5356 · %g mm · piston başı üst yüzü ↔ piston plakası ön yüzü (iç köşe)" % (x1 - x0), 1, "a 4 × %g" % (x1 - x0), "TIG 141", "ÜRETİM"],
           "E_MEK_BAG__kaynak", aile="piston", rol="kaynak", tur="kaynak")
for i, xl in ((0, 4600.0), (1, 4720.0)):
    M.vida("piston_lama_%d_vida" % i, "piston_bas", "piston_lama_%d" % i, dis="M5", std="DIN7991", yon=Y, duzlem=1330.0, pts=[(xl, z) for z in (-330.0, -260.0, -190.0, -120.0)],
           not_="20 mm başın altından (havşa; alt yüz kutuya basar) 8 × 50 lamanın alt kenarına dişli")
# üst L bloklar (3 mm): dik bacak taşıyıcının arkasına, ayak besleyici plakasına
for i, (xa, xb) in ((0, (4585.0, 4615.0)), (1, (4725.0, 4755.0))):
    M.vida("itici_ust_blok_%d_vida" % i, "itici_ust_blok_%d" % i, "itici_tasiyici", dis="M4", std="DIN7991", yon=Z, duzlem=-394.0, pts=[(xa, 1350.0), (xb, 1370.0)], kavrama=5.0,
           not_="L bloğun dik bacağından (3 mm, havşa) taşıyıcı plakaya (5 mm, dişli; ray dışında)")
    M.vida("itici_ust_blok_%d_taban_vida" % i, "itici_ust_blok_%d" % i, "besleyici_plaka", dis="M4", yon=YM, duzlem=1337.0, pts=[(xa + 5.0, -410.0), (xb - 5.0, -410.0)], kavrama=5.0,
           not_="L bloğun ayağından besleyici plakasına (5 mm, dişli)")
# sensör bloğu (3 mm Z): ayağı taşıyıcının arkasına · M8 sensör dudakta iki somunla
M.vida("itici_sensor_blogu_vida", "itici_sensor_blogu", "itici_tasiyici", dis="M4", std="DIN7991", yon=Z, duzlem=-394.0, pts=[(4748.0, 1776.0), (4762.0, 1788.0)], kavrama=5.0)
M.somun_mil("itici_sensor_somun_dis", "itici_sensor", "itici_sensor_blogu", yon=ZM, dis="M8", yuz=-383.0)
M.somun_mil("itici_sensor_somun_ic", "itici_sensor", "itici_sensor_blogu", yon=Z, dis="M8", yuz=-380.0, ince=True)
# ---------------------------------------------------------------- vida mili üst yatağı · yatak plakaları · motor bloğu · Z köşebentler (yeni) · motor · kasnaklar
M.vida("itici_yatak_plakasi_1_vida", "itici_ust_yatak", "itici_yatak_plakasi_1", dis="M4", yon=Y, duzlem=1822.5, pts=[(4650.0, -308.0), (4690.0, -308.0)], kavrama=7.0,
       not_="üst yatak bloğunun altından (32,5) ön yatak plakasının alt kenarına (6 mm, dişli)")
# Z köşebentler (2 mm): arka bacak taşıyıcının üst flanşının ön yüzüne (z −380; piston plakasının üstünde, y ≥ 1848), ön bacak yatak plakası 0 / motor direğinin arka yüzüne
ZB = [("itici_yatak_z_braketi", 4646.0, 4694.0, -345.0, "itici_yatak_plakasi_0", [(4652.0, 1853.0), (4688.0, 1853.0)], [(4652.0, 1850.0), (4688.0, 1850.0)], 6.0, 1838.0),
      ("itici_motor_z_braketi_0", 4706.0, 4728.0, -350.0, "itici_motor_blogu", [(4712.0, 1853.0), (4722.0, 1853.0)], [(4712.0, 1852.0)], 5.0, 1846.0),
      ("itici_motor_z_braketi_1", 4748.0, 4772.0, -350.0, "itici_motor_blogu", [(4752.0, 1853.0), (4760.0, 1853.0)], [(4768.0, 1852.0)], 5.0, 1846.0)]
for ad, x0, x1, zb, B, ptsA, ptsB, kavB, yB in ZB:   # yB: ön bacağın alt kenarı (motor direkleri: piston plakasının üstünde, y > 1845)
    sh = (kutu(x0, 1848.0, -380.0, x1, 1858.0, -378.0).union(kutu(x0, 1856.0, -380.0, x1, 1858.0, zb)).union(kutu(x0, yB, zb - 2.0, x1, 1858.0, zb))).val()
    M.yeni(ad, sh, ["Z köşebent AISI 304 2 mm · %g × 10 / 20 × %g (taşıyıcı üst flanşının ön yüzü ↔ %s arka yüzü)" % (x1 - x0, abs(-378.0 - zb + 2.0), B), 1, "2 × %g × %g" % (x1 - x0, abs(-378.0 - zb + 2.0)), "lazer + 2 büküm · 0.02 kg", "ÜRETİM"],
           "E_MEK_BAG__celik", aile="itici", kontrol=[((x0, 1848.0, -380.0), (x1, 1858.0, -378.0)), ((x0, 1856.0, -378.0), (x1, 1858.0, zb - 2.0)), ((x0, yB, zb - 2.0), (x1, 1858.0, zb))])
    M.vida("%s_tasiyici_vida" % ad, ad, "itici_tasiyici", dis="M4", yon=ZM, duzlem=-380.0, pts=ptsA, kavrama=5.0, not_="Z köşebent arka bacağından taşıyıcının üst flanşına (14 mm, dişli)")
    M.vida("%s_vida" % ad, ad, B, dis="M4", yon=Z, duzlem=zb, pts=ptsB, kavrama=kavB, not_="Z köşebent ön bacağından %s'e (dişli)" % B)
M.motor("itici_motor_vida", "itici_motor", "itici_motor_blogu", yon=Y, flans=1822.0, boy_flans=8.0, kav=4.0, dis="M4", kare=47.14, merkez=(4740.0, -318.0),
        not_="NEMA 23 flanşından 4 mm flanş plakasına; plaka 4 mm olduğundan M4 (tutuş 4 = 1 × d) — ürünün Ø5,1 delikleri M4 cıvatayla")
M.pim("itici_kasnak_mil_pim", "itici_kasnak_mil", "itici_vida_mili", yon=X, pts=[(1832.5, -324.5)], boy=12.0,
      not_="kasnak göbeği 1,1 mm (üreteç: kasnak deliği mil çapında) → setskur yeri yok; radyal Ø3 × 12 pim · açık madde: mil ucuna Ø10 muylu + kama")
M.vida("itici_kasnak_motor_vida", "itici_motor_mili", "itici_kasnak_motor", dis="M3", yon=YM, duzlem=1839.5, pts=[(4740.0, -318.0)], kavrama=4.5,
       not_="kasnak motor mili ucunda: eksenel M3 (mil ucu dişli — ürün notu; kasnak katı modelde deliksiz)")
# ---------------------------------------------------------------- PARMAK: taşıyıcı · motor braketi · motor · kasnaklar · sensör · kol · bıçak
M.vida("parmak_tasiyici_vida", "parmak_tasiyici", "piston_lama_0", dis="M5", yon=YM, duzlem=1380.0, pts=[(4600.0, z) for z in (-150.0, -120.0, -90.0, -70.0)], kavrama=7.5,
       not_="taşıyıcının 6 mm ayağından lama 0'ın üst kenarına (8 mm, dişli)")
M.vida("parmak_motor_braketi_vida", "parmak_motor_braketi", "piston_lama_1", dis="M5", yon=YM, duzlem=1380.0, pts=[(4720.0, z) for z in (-150.0, -120.0, -90.0, -70.0)], kavrama=7.5,
       not_="motor braketinin 6 mm tabanından lama 1'in üst kenarına (8 mm, dişli)")
M.motor("parmak_motor_vida", "parmak_motor", "parmak_motor_braketi", yon=Z, flans=-5.0, boy_flans=8.0, kav=5.5, dis="M5", kare=47.14, merkez=(4740.0, 1509.5))
M.setskur("parmak_kasnak_setskur", "parmak_kasnak", "parmak_gobek", yon=(-0.836, -0.549, 0.0), pts=[(4500.8 + 8.36, 1351.9 + 5.49, 12.5)], dis="M4",
           not_="kayışın sarmadığı motor tarafından radyal (kayıştan geçmez)")
M.setskur("parmak_motor_kasnagi_setskur", "parmak_motor_kasnagi", "parmak_motor", yon=X, pts=[(1509.5, 10.0)], dis="M4")
M.vida("parmak_sensor_lamasi_vida", "parmak_motor_braketi", "parmak_sensor_lamasi", dis="M4", yon=ZM, duzlem=-5.0, pts=[(4771.5, 1505.0), (4771.5, 1515.0)], kavrama=6.0,
       not_="braket plakasının +z yüzünden (6 mm) 6 × 20 sensör lamasının ucuna (dişli)")
M.yeni("parmak_sensor_braketi_kaynak", kutu(4774.5, 1517.5, -91.8, 4776.5, 1519.5, -78.8).val(),
       ["TIG punta a 2 · 1.4301 · 13 mm · sensör braketi üst kenarı ↔ sensör laması (+x yüzü)", 1, "a 2 × 13", "TIG 141", "ÜRETİM"], "E_MEK_BAG__kaynak", aile="parmak", rol="kaynak", tur="kaynak")
M.somun_mil("parmak_sensor_somun_dis", "parmak_sensor", "parmak_sensor_braketi", yon=X, dis="M8", yuz=4777.5)
M.somun_mil("parmak_sensor_somun_ic", "parmak_sensor", "parmak_sensor_lamasi", yon=XM, dis="M8", yuz=4772.5, ince=True, cep="parmak_sensor_lamasi")
M.yeni("parmak_kol_kaynak", kutu(4479.0, 1408.0, -27.0, 4484.0, 1410.0, -20.0).val(),
       ["TIG punta a 2 · ER5356 · 7 mm · kol rayı ucu ↔ göbek plakası üst kenarı", 1, "a 2 × 7", "TIG 141", "ÜRETİM"], "E_MEK_BAG__kaynak", aile="parmak", rol="kaynak", tur="kaynak")
M.vida("parmak_bicak_vida", "parmak_bicak", "parmak_kol", dis="M3", std="DIN7991", yon=Y, duzlem=1356.4, pts=[(4520.0, z) for z in (-290.0, -240.0, -190.0, -140.0)], kavrama=3.0,
       not_="2 mm bıçaktan (havşa) kolun 3 mm plakasına dişli")

M.bitir(go, "E_MEK_BAG__vida", "84", mek=36, mek_kod="E/Kutu katlama", ek=dict(aile=["parmak", "itici", "piston"]),
        ek_dugum={"_sablon": {"E_MEK_BAG__kaynak": "E_GOVDE__sac", "E_MEK_BAG__celik": "E_GOVDE__celik"}})
LOG("%.0f sn" % (time.time() - t0))
sys.stdout.flush(); os._exit(0)
