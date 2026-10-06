# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 81 · E KALIP + KALIP YUVASI + KÖPRÜ MEKANİZMALARI VİDALI (6 Eki 2026 · Claude · 2. oturum · E mekanizma montajı · KURALLAR §1.2 / §2.2 / §5)
python 81_e_kalip_kopru.py girdi.glb cikti.glb      (zincir: hat3_v10l.glb → hat3_v10m.glb)

E montaj v2 bağlantı denetimi: kalıp (E_KALIP, 44 bileşen) ve köprü (E_KOPRU, 15) mekanizmalarının iç parçaları birbirine hiçbir bağlantı elemanıyla
bağlı değildi (envanter e1/e_envanter.md). Bileşenler veri/e_mek_parcalar.json adlarıyla; bağlantılar e_mek_bag.py motoruyla:
  KALIP: 4 × Ø40 kolon tabana alttan (M8) ve üst plakaya üstten (M8) · 4 kılavuz yatağı + orta blok üst plakaya üstten (M6 / M8) · motor NEMA 23
    flanşından kaplin flanşı + orta bloğa 4 × M5×60 · kaplin motor miline + vida mili ucuna 2 × DIN 916 M4 · rulman bloğu orta bloğa yandan 2 × M5 ·
    vida mili rulman bloğu üstünde DIN 471 segman · sensör bloğu sağ yatağa 2 × M4 · bayraklar + fork sensör M3 ·
    yuva: 4 kılavuz mil alt çubuğa alttan M6, üstte yuva plakalarına havşa M6 · bronz somun çubuğa 2 × M4 · bayrak M3.
  KÖPRÜ: motor motor bloğuna 4 × M5 · kaplin motor miline setskur · rulman bloğu motor bloğuna önden 2 × M5 · vida mili segman · taşıyıcı motor
    bloğuna 3 × M6 · kılavuz yatakları setskur · somun bloğu kızağa gömme 2 × M6 · köprü plakası kızağa + kılavuz millere havşa M5 · sensör tutucu 2 × M4 ·
    M8 sensör somunu.
Hazır ürün (motor / sensör) KURALLAR §3: ürüne dokunulmaz, bizim parça dişli; vida ürünün kendi deliğinden geçer.
Denetim (betikte): baş / somun / segman hacmi boş · her vida tam olarak A + B'yi deliyor (fazla parça yok) · diş tutuşu ≥ 1 × d · boy katalogdan."""
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
M = MB.Mek(g, (4390, 560, -400), (5240, 1000, 0))
Y, YM, X, XM, Z, ZM = (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)

# ================================================================= KALIP
# 1 · kolonlar (40 × 40 × 2,2 kutu profil): uç tapaları (yeni) · tapa profile 2 × M5 (−x yüzünden) · taban (4 mm plaka) alttan M8 · üst plaka üstten M8
for i in range(4):
    k = "kalip_kolon_%d" % i; lo, hi = M.kutu(k); c = ((lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2)
    for uc, y0, y1 in (("alt", 622.0, 642.0), ("ust", 892.0, 912.0)):
        ad = "%s_tapa_%s" % (k, uc)
        sh = cq.Workplane("XY").box(35.4, y1 - y0, 35.4, centered=False).translate((c[0] - 17.7, y0, c[1] - 17.7)).val()
        M.yeni(ad, sh, ["Profil uç tapası alüminyum 35,4 × 35,4 × 20 (40 × 40 × 2,2 kutu profilin içine; merkez M8 dişli, yan 2 × M5 dişli)", 1, "35.4 × 20 × 35.4", "frezeleme · 0.07 kg", "ÜRETİM"],
               "E_MEK_BAG__aluminyum", aile="kalip")
        M.vida("%s_vida" % ad, k, ad, dis="M5", yon=X, duzlem=lo[0] + 2.2, pts=[(y0 + 6.0, c[1] - 9.0), (y1 - 6.0, c[1] + 9.0)], kavrama=7.5, not_="profil duvarından (2,2) tapaya")
    ct = (c[0], c[1] + (10.0 if i % 2 == 0 else -10.0))                       # baş taban rayının (arka z −372…−342 · ön −54…−24) dışında
    M.vida("%s_taban_vida" % k, "kalip_taban", "%s_tapa_alt" % k, dis="M8", yon=Y, duzlem=622.0, pts=[ct], kavrama=16.0)
    M.vida("%s_ust_vida" % k, "kalip_ust_plaka", "%s_tapa_ust" % k, dis="M8", yon=YM, duzlem=912.0, pts=[c], kavrama=16.0)
# 2 · kılavuz yatakları (Ø24 burç deliği) → üst plakaya köşeden 2 × M5 · orta blok direkleri (6 × 6) → üst plakaya M3
for i in range(4):
    y_ = "kalip_yatak_%d" % i; lo, hi = M.kutu(y_); cx, cz = (lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2
    M.vida("%s_vida" % y_, "kalip_ust_plaka", y_, dis="M5", yon=YM, duzlem=912.0, pts=[(cx - 12.5, cz - 12.5), (cx + 12.5, cz + 12.5)])
M.vida("kalip_orta_blok_vida", "kalip_ust_plaka", "kalip_orta_blok", dis="M3", yon=YM, duzlem=912.0, pts=[(4628.0, -248.0), (4692.0, -248.0)], kavrama=4.5)
# 3 · motor (NEMA 23, flanş y 699, kendi Ø5,1 delikleri) → 6 mm flanş plakasına 4 × M4 · flanş direkleri (y 729) → orta blok alt plakasına M3 · rulman bloğu → alt plakaya alttan 2 × M4
M.motor("kalip_motor_vida", "kalip_motor", "kalip_motor_flansi", yon=Y, flans=699.0, boy_flans=8.0, kav=5.5, dis="M4", kare=47.14, merkez=(4660.0, -206.0))
M.vida("kalip_motor_flansi_vida", "kalip_orta_blok", "kalip_motor_flansi", dis="M3", yon=YM, duzlem=729.0, pts=[(4632.0, -234.0), (4688.0, -234.0)], kavrama=4.5)
M.vida("kalip_rulman_blogu_vida", "kalip_orta_blok", "kalip_rulman_blogu", dis="M4", yon=Y, duzlem=735.0, pts=[(4643.0, -223.0), (4677.0, -189.0)])
# 4 · kaplin: motor miline setskur (−x yüzünden; vida milinin muylusu kaplinin içinde, mil segmanla tutulur) · vida mili rulman bloğu üstünde segman (y 754)
M.setskur("kalip_kaplin_setskur", "kalip_kaplin", "kalip_motor", yon=X, pts=[(716.0, -205.5)], n=1)
M.segman("kalip_vida_mili_segman", "kalip_vida_mili", 754.0, Y)
# 5 · sensör bloğu (üst bandı 874–880 dolu, altı yarık) → sağ yatak (−x) 2 × M4 · fork sensör (kendi çelik kulaklarıyla yarıkta) üst banttan 1 × M3
M.vida("kalip_sensor_blogu_vida", "kalip_sensor_blogu", "kalip_yatak_3", dis="M4", yon=XM, duzlem=4809.5, pts=[(877.0, -218.5), (877.0, -193.5)])
M.vida("kalip_sensor_vida", "kalip_sensor_blogu", "kalip_sensor", dis="M3", yon=YM, duzlem=874.0, pts=[(4814.0, -206.0)], kavrama=4.5, not_="üst banttan (6 mm) sensörün kendi deliğine; 2 mm boşluk; sensör kendi çelik kulaklarıyla yarıkta")
# 6 · yuva: kılavuz miller çubuğa alttan M6 · plakalara üstten havşa M6 · bronz somun çubuğa 2 × M4 · bayrak çubuk ucuna M3
for i in range(4):
    m = "kalip_yuva_mil_%d" % i; lo, hi = M.kutu(m); c = ((lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2)
    M.vida("%s_alt_vida" % m, "kalip_yuva_cubuk", m, dis="M6", yon=Y, duzlem=871.6, pts=[c], kavrama=10.0)
    M.vida("%s_ust_vida" % m, "kalip_yuva_plaka_%d" % i, m, dis="M6", std="DIN7991", yon=YM, duzlem=973.6, pts=[c], kavrama=12.0)
M.vida("kalip_yuva_somun_vida", "kalip_yuva_cubuk", "kalip_yuva_somun", dis="M3", yon=Y, duzlem=871.6, pts=[(4648.2, -205.5), (4671.8, -205.5)], not_="Ø28 flanşın 6 mm halkasında (r 11,8); baş çubuğun altında, vida milinden 1,3 mm boşluk")
M.vida("kalip_yuva_bayrak_vida", "kalip_yuva_bayrak", "kalip_yuva_cubuk", dis="M3", std="DIN7991", yon=XM, duzlem=4805.0, pts=[(868.6, -206.0)], not_="havşa (fork sensör 1 mm önde)")

# ================================================================= KÖPRÜ
M.motor("kopru_motor_vida", "kopru_motor", "kopru_motor_blogu", yon=Y, flans=776.0, boy_flans=8.0, kav=5.5)
M.setskur("kopru_kaplin_setskur", "kopru_kaplin", "kopru_motor", yon=Z, pts=[(4446.5, 791.0)])
M.vida("kopru_rulman_blogu_vida", "kopru_rulman_blogu", "kopru_tasiyici", dis="M5", yon=Y, duzlem=847.0, pts=[(4423.0, -220.0), (4471.0, -185.0)], kavrama=5.0, boy=40.0,
       not_="alttan, taşıyıcı plakaya (6 mm dişli); uç plaka üstünden 1 mm taşar (somun bloğu 2 mm üstte)")
M.segman("kopru_vida_mili_segman", "kopru_vida_mili", 853.0, Y)
M.vida("kopru_tasiyici_vida", "kopru_tasiyici", "kopru_motor_blogu", dis="M5", yon=YM, duzlem=832.0, pts=[(4410.0, -225.0), (4410.0, -187.0)])
# kılavuz yatakları (Ø21 lineer burç, flanşsız): taşıyıcı plakanın deliğine sıkı geçme (burç) — vida yok
M.vida("kopru_somun_blogu_vida", "kopru_kizak", "kopru_somun_blogu", dis="M6", yon=YM, duzlem=912.0, pts=[(4447.0, -222.8), (4447.0, -189.2)], gomme=8.5, not_="baş kızağın gömme yuvasında (köprü plakası üstüne düz oturur)")
M.vida("kopru_plaka_vida", "kopru_plaka", "kopru_kizak", dis="M5", std="DIN7991", yon=YM, duzlem=948.5, pts=[(4436.0, -240.0), (4436.0, -172.0), (4458.0, -240.0), (4458.0, -172.0)])
for i in range(2):
    m = "kopru_kilavuz_mil_%d" % i; lo, hi = M.kutu(m); c = ((lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2)
    M.vida("%s_vida" % m, "kopru_plaka", m, dis="M5", std="DIN7991", yon=YM, duzlem=948.5, pts=[c], kavrama=9.0)
M.vida("kopru_sensor_tutucu_vida", "kopru_sensor_tutucu", "kopru_tasiyici", dis="M4", yon=YM, duzlem=853.0, pts=[(4455.0, -177.0), (4455.0, -167.0)])
M.somun_mil("kopru_sensor_somun", "kopru_sensor", "kopru_sensor_tutucu", yon=Y, dis="M8")

M.bitir(go, "E_MEK_BAG__vida", "81", mek=36, mek_kod="E/Kutu katlama", ek=dict(aile=["kalip", "kalip_yuva", "kopru"]))
LOG("%.0f sn" % (time.time() - t0))
sys.stdout.flush(); os._exit(0)
