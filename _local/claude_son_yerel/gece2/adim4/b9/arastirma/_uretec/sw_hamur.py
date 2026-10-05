# -*- coding: utf-8 -*-
# STORE — taze hamur çekmecesinin içi: çukurlu silikon tepsi GN 2/1 (530×650×30, 4×5 = 20 çukur Ø120, aralık 130)
# + 20 hamur topu (220 g, dinlenmiş kubbe Ø95 × 60). CEKMECE_taze alt montajına eklenir → 8 çekmecenin hepsinde görünür (8×20 = 160 top, 2 gün).
# Ayrıca çekmece kutusu 600 → 700 mm derinleştirilir (tepsi 650 sığsın; teknik resim: çekmece içi derinlik 740).
import os, math, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
CEK = os.path.join(ARA, "1_STORE", "cekmece", "CEKMECE_taze"); ORTAK = os.path.join(ARA, "_ortak")
W_CEK, H_CEK, DERIN = 618.0, 93.0, 700.0            # çekmece önü genişlik/yükseklik · yeni kutu derinliği
KA, KB, KC, KD = 13.7, W_CEK-13.7, 8.0, H_CEK-12.0  # kutu iç sınırları
TEPSI_W, TEPSI_D, TEPSI_H, CUKUR_R, CUKUR_H, ARALIK = 530.0, 650.0, 30.0, 60.0, 20.0, 130.0
XC, ZC = (KA+KB)/2, -(DERIN)/2                      # tepsi merkezi (çekmece yerel koordinatı)
X_CUKUR = [XC - 1.5*ARALIK + i*ARALIK for i in range(4)]
Z_CUKUR = [ZC - 2*ARALIK + j*ARALIK for j in range(5)]
Y_TEPSI = KC + 1                                     # kutu tabanı üstü

def kutu_derinlestir():
    """çekmece kutusu + arka + rayları 700 mm derinlikte yeniden üret"""
    st = Station(CEK, "CEKMECE_taze"); p = "CEK_taze_"
    for ad in ("kutu_U_1.0", "kutu_arka_1.0", "ray_teleskopik_sol_45x12.7", "ray_teleskopik_sag_45x12.7"):
        yol = os.path.join(st.pdir, p + ad + ".SLDPRT")
        if os.path.exists(yol): os.remove(yol)
    st.prism_z(p+"kutu_U_1.0", [(KA, KD), (KA, KC), (KB, KC), (KB, KD), (KB-1, KD), (KB-1, KC+1), (KA+1, KC+1), (KA+1, KD)], -DERIN, 0)
    st.box(p+"kutu_arka_1.0", KA, KB, KC, KD, -DERIN, -DERIN+1)
    st.box(p+"ray_teleskopik_sol_45x12.7", 0, 12.7, KC+10, KC+55, -DERIN+50, 0)
    st.box(p+"ray_teleskopik_sag_45x12.7", W_CEK-12.7, W_CEK, KC+10, KC+55, -DERIN+50, 0)
    print("  kutu %d mm derinlestirildi" % DERIN)

def tepsi_cukurlu():
    """GN 2/1 çukurlu silikon tepsi — yerel: çekmece koordinatında (yerinde) modellenir"""
    st = Station(os.path.join(ORTAK, "TEPSI_HAMUR_GN21"), "TEPSI_HAMUR_GN21"); p = "TPS_"
    x0, x1 = XC-TEPSI_W/2, XC+TEPSI_W/2; z0, z1 = ZC-TEPSI_D/2, ZC+TEPSI_D/2
    ops = [(TP, 'rect', (x0, x1, -z1, -z0), Y_TEPSI, Y_TEPSI+TEPSI_H, False)]
    ops += [(TP, 'circ', (cx, -cz, CUKUR_R), Y_TEPSI+TEPSI_H-CUKUR_H, Y_TEPSI+TEPSI_H+1, True) for cx in X_CUKUR for cz in Z_CUKUR]
    st.part(p+"silikon_GN21_20_cukur", ops)
    st.assemble("TEPSI_HAMUR_GN21"); print("  tepsi: 20 cukur D%d, aralik %d" % (2*CUKUR_R, ARALIK))

def hamur_topu():
    """220 g dinlenmiş hamur topu: silindir 12 + yarım küre R47,5 (Ø95 × 59,5) — yerel merkez (0,0,0) = çukur tabanı"""
    st = Station(os.path.join(ORTAK, "HAMUR_TOPU_220g"), "HAMUR_TOPU_220g"); p = "HMR_"
    doc, sk, fm, pl = st._new(); r, h_sil = 47.5, 12.0
    doc.ClearSelection2(True); pl[FR].Select2(False, 0); sk.InsertSketch(True)
    sk.CreateCenterLine(0, 0, 0, 0, (h_sil+r)*M, 0)                                  # döndürme ekseni
    sk.CreateLine(0, 0, 0, r*M, 0, 0); sk.CreateLine(r*M, 0, 0, r*M, h_sil*M, 0)
    sk.CreateArc(0, h_sil*M, 0, r*M, h_sil*M, 0, 0, (h_sil+r)*M, 0, 1)               # yarım küre
    sk.CreateLine(0, (h_sil+r)*M, 0, 0, 0, 0)
    sk.InsertSketch(True)
    f = fm.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 2*math.pi, 0, False, False, 0, 0, 0, 0, 0, True, True, True)
    if f is None: raise RuntimeError("hamur topu olusmadi")
    f.Name = p+"topu_220g_D95x59.5"
    bb = bbox_of(doc); yol = os.path.join(st.pdir, p+"topu_220g.SLDPRT")
    if not saveas(doc, yol): raise RuntimeError("kayit hatasi hamur")
    sw.CloseDoc(doc.GetTitle); st.parts.append((yol, [(bb[i]+bb[i+3])/2 for i in range(3)])); st._track(bb)
    st.assemble("HAMUR_TOPU_220g"); print("  hamur topu: D95 x %.1f mm" % (h_sil+r))

def cekmece_kur():
    """CEKMECE_taze montajını yeniden kur: kendi parçaları + tepsi + 20 hamur topu"""
    st = Station(CEK, "CEKMECE_taze"); st.load_dir(); print("  cekmece parca:", len(st.parts))
    st.add_instance(os.path.join(ORTAK, "TEPSI_HAMUR_GN21", "TEPSI_HAMUR_GN21.SLDASM"), offset_mm=(0, 0, 0))
    n = 0
    for cx in X_CUKUR:
        for cz in Z_CUKUR:
            st.add_instance(os.path.join(ORTAK, "HAMUR_TOPU_220g", "HAMUR_TOPU_220g.SLDASM"),
                            offset_mm=(cx, Y_TEPSI+TEPSI_H-CUKUR_H, cz)); n += 1
    st.assemble("CEKMECE_taze"); print("  CEKMECE_taze: tepsi + %d hamur topu" % n)

def _ana():
    sw.CloseAllDocuments(True)
    kutu_derinlestir(); tepsi_cukurlu(); hamur_topu(); cekmece_kur()
    print("BITTI — 8 taze cekmecenin hepsinde 20 top (toplam %d)" % (8*20))

if __name__ == "__main__":
    _ana()
