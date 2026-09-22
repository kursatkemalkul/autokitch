# -*- coding: utf-8 -*-
# LAHMACUN HAMURU — ortak parcalar (12 Eyl 2026)
#   HAMUR_TOPU_110g      : 110 g dinlenmis top, silindir 10 + yarim kure R37,5  -> O75 x 47,5
#   TEPSI_LAHMACUN_GN21  : GN 2/1 silikon tepsi 530x650x30, 5x6 = 30 cukur O98, adim 105
# Pide tepsisi 20 top aliyor (cukur O120 adim 130); lahmacun topu daha kucuk oldugu icin
# ayni GN 2/1 tepsiye 30 top siginca cekmece basina kapasite %50 artiyor.
# Bu, STORE'da TAM BIR KOLON kazandiriyor (30 top/cekmece ile 4 kolon, 20 ile 5 kolon gerekirdi).
import os, math, io, json
from sw_lib import *

ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma".replace("WEBSITE", "WEBS\u0130TE")
ORTAK = os.path.join(ARA, "_ortak")

# --- cekmece yerel koordinati (CEKMECE3_* ile ayni: ka=16, kb=604, kc=8) ---
KA, KB, KC, DERIN = 16.0, 604.0, 8.0, 700.0
XC, ZC = (KA + KB) / 2.0, -DERIN / 2.0                      # 310 · -350
TEPSI_W, TEPSI_D, TEPSI_H = 530.0, 650.0, 30.0
CUKUR_R, CUKUR_H, ADIM = 49.0, 18.0, 105.0                  # O98 cukur, 18 derin, 105 adim
NX, NZ = 5, 6                                               # 5 x 6 = 30
Y_TEPSI = KC + 1.0                                          # 9 — kutu tabani ustu
X_CUKUR = [XC - (NX - 1) / 2.0 * ADIM + i * ADIM for i in range(NX)]
Z_CUKUR = [ZC - (NZ - 1) / 2.0 * ADIM + j * ADIM for j in range(NZ)]


def tepsi_lahmacun():
    """GN 2/1 cukurlu silikon tepsi — 30 cukur"""
    st = Station(os.path.join(ORTAK, "TEPSI_LAHMACUN_GN21"), "TEPSI_LAHMACUN_GN21"); p = "TPSL_"
    x0, x1 = XC - TEPSI_W / 2.0, XC + TEPSI_W / 2.0
    z0, z1 = ZC - TEPSI_D / 2.0, ZC + TEPSI_D / 2.0
    ops = [(TP, 'rect', (x0, x1, -z1, -z0), Y_TEPSI, Y_TEPSI + TEPSI_H, False)]
    ops += [(TP, 'circ', (cx, -cz, CUKUR_R), Y_TEPSI + TEPSI_H - CUKUR_H, Y_TEPSI + TEPSI_H + 1, True)
            for cx in X_CUKUR for cz in Z_CUKUR]
    st.part(p + "silikon_GN21_30_cukur", ops)
    st.assemble("TEPSI_LAHMACUN_GN21")
    print("  tepsi: %d cukur D%.0f, adim %.0f  (%dx%d)" % (NX * NZ, 2 * CUKUR_R, ADIM, NX, NZ))


def hamur_topu_110():
    """110 g dinlenmis lahmacun topu: silindir 10 + yarim kure R37,5 (O75 x 47,5)"""
    st = Station(os.path.join(ORTAK, "HAMUR_TOPU_110g"), "HAMUR_TOPU_110g"); p = "HMR110_"
    doc, sk, fm, pl = st._new(); r, h_sil = 37.5, 10.0
    doc.ClearSelection2(True); pl[FR].Select2(False, 0); sk.InsertSketch(True)
    sk.CreateCenterLine(0, 0, 0, 0, (h_sil + r) * M, 0)
    sk.CreateLine(0, 0, 0, r * M, 0, 0); sk.CreateLine(r * M, 0, 0, r * M, h_sil * M, 0)
    sk.CreateArc(0, h_sil * M, 0, r * M, h_sil * M, 0, 0, (h_sil + r) * M, 0, 1)
    sk.CreateLine(0, (h_sil + r) * M, 0, 0, 0, 0)
    sk.InsertSketch(True)
    f = fm.FeatureRevolve2(True, True, False, False, False, False, 0, 0, 2 * math.pi, 0,
                           False, False, 0, 0, 0, 0, 0, True, True, True)
    if f is None: raise RuntimeError("hamur topu 110 olusmadi")
    f.Name = p + "topu_110g_D75x47.5"
    bb = bbox_of(doc); yol = os.path.join(st.pdir, p + "topu_110g.SLDPRT")
    if not saveas(doc, yol): raise RuntimeError("kayit hatasi hamur110")
    sw.CloseDoc(doc.GetTitle); st.parts.append((yol, [(bb[i] + bb[i + 3]) / 2 for i in range(3)])); st._track(bb)
    st.assemble("HAMUR_TOPU_110g"); print("  hamur topu 110 g: D75 x %.1f mm" % (h_sil + r))


def json_ekle():
    """cekmece_icerik.json'a 'lahmacun' anahtari: 30 top + 1 tepsi (cekmece yerel merkezleri)"""
    yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cekmece_icerik.json")
    d = json.load(io.open(yol, encoding="utf-8"))
    top = os.path.join(ORTAK, "HAMUR_TOPU_110g", "HAMUR_TOPU_110g.SLDASM")
    tps = os.path.join(ORTAK, "TEPSI_LAHMACUN_GN21", "TEPSI_LAHMACUN_GN21.SLDASM")
    # add_instance center_m = [(c0+1), c1, (c2+3)] mm -> JSON'da x'i 1, z'yi 3 geri yaz
    # topun tabani y=19 (pide topuyla ayni kot) -> merkez 19 + 47,5/2 = 42,75
    icerik = [[top, [cx - 1.0, 42.75, cz - 3.0]] for cx in X_CUKUR for cz in Z_CUKUR]
    icerik.append([tps, [XC - 1.0, Y_TEPSI + TEPSI_H / 2.0, ZC - 3.0]])
    d["lahmacun"] = icerik
    io.open(yol, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
    print("  cekmece_icerik.json: 'lahmacun' anahtari yazildi (%d oge = 30 top + 1 tepsi)" % len(icerik))


if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    tepsi_lahmacun()
    hamur_topu_110()
    json_ekle()
    Station(ORTAK, "x").exit_sw()
