# -*- coding: utf-8 -*-
# ÇEKMECE TAHRİK SİSTEMİ — MOTOR GÖRÜNÜR, KABLO ZİNCİRİ EKSİKSİZ
# Değişiklik: çekmece derinliği 740 → 700 → arkada 57 mm boşluk kaldı; motor oraya (ekseni X, ray arkasına) oturuyor.
#   ana PC ── Ethernet ──> PLC ── röle ──> 24 V kablo ──> MOTOR (ray arkasında) ──> kayış ──> çekmece
#   geri bildirim: reed sensör (kapalı) + motor enkoderi (konum)
# Kapasite: kola 7×10 = 70/çekmece (4 çekmece 280) · 1 L 6×7 = 42 · hamur 20 · donmuş 20
import os, time, pythoncom
from sw_lib import *
from PIL import Image
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); CEKD = os.path.join(ROOT, "cekmece"); ORTAK = os.path.join(ARA, "_ortak"); DETAY = os.path.join(ROOT, "detay")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
DERIN, KA, KB = 700.0, 13.7, 604.3
# tip: (ön yükseklik, taban kotu, ürün, ürün R, kanal adım x, sıra adım z, nx, nz, yuva derinliği, tepsi kalınlığı)
TIP = {
 "icecek": dict(h=118.0, kc=4.0, urun="KUTU_KOLA_330ml", r=35.0, ax=82.0, az=70.0, nx=7, nz=10, cd=12.0, kal=13.0),
 "1L":     dict(h=310.0, kc=4.0, urun="SISE_KOLA_1L",    r=46.0, ax=99.0, az=94.0, nx=6, nz=7,  cd=15.0, kal=20.0),
}
TEPSI_TIP = ("taze", "donmus")   # hamur tepsili çekmeceler (tepsi 650 derin → 700'e sığar)

def kutu_ve_ray(tip, h, kc):
    """kutu 700 derin + pasif sağ ray + MOTORLU sol ray gövdesi (motor kasada, ayrı parça)"""
    st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip; kd = h - 12.0
    for f in os.listdir(st.pdir):
        if any(k in f for k in ("kutu_U", "kutu_arka", "ray_", "cukurlu", "tepsi_taban", "kremayer")): os.remove(os.path.join(st.pdir, f))
    st.prism_z(p+"kutu_U_1.0", [(KA, kd), (KA, kc), (KB, kc), (KB, kd), (KB-1, kd), (KB-1, kc+1), (KA+1, kc+1), (KA+1, kd)], -DERIN, 0)
    st.box(p+"kutu_arka_1.0", KA, KB, kc, kd, -DERIN, -DERIN+1)
    yr = kc + 10
    st.box(p+"ray_ic_profil_sol", 0, 12.7, yr, yr+45, -660, 0)          # rayın çekmeceye vidalı iç profili
    st.box(p+"ray_ic_profil_sag", 618.0-12.7, 618.0, yr, yr+45, -660, 0)
    st.box(p+"kayis_baglanti_pabucu", 2, 12, yr+15, yr+30, -80, -40)     # motor kayışı buraya kenetlenir
    return st

def yuvali_tepsi(tip):
    """kola/şişe için çukurlu yuva tepsisi (taban sacı + halka yuvalar) ve ürün yerleşimi"""
    t = TIP[tip]; st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip
    genis = KB - KA
    X = [KA + (genis - ((t["nx"]-1)*t["ax"] + 2*t["r"]))/2 + t["r"] + i*t["ax"] for i in range(t["nx"])]
    Z = [-(2 + t["r"]) - j*t["az"] for j in range(t["nz"])]
    y0 = t["kc"] + 1; y1 = y0 + t["kal"]
    st.box(p+"tepsi_taban_saci_1.5", KA+3, KB-3, y0, y0+1.5, Z[-1]-t["r"]-8, min(Z[0]+t["r"]+8, -3))
    halka = os.path.join(ORTAK, "YUVA_%s" % tip)
    if not os.path.exists(os.path.join(halka, "YUVA_%s.SLDASM" % tip)):
        hs = Station(halka, "YUVA_%s" % tip)
        hs.part("YUVA_%s_halka" % tip, [(TP, 'circ', (0, 0, t["r"]+5.5), y0+1.5, y1, False), (TP, 'circ', (0, 0, t["r"]+2), y1-t["cd"], y1+1, True)])
        hs.assemble("YUVA_%s" % tip)
    st.load_dir(); n = 0
    for cx in X:
        for cz in Z:
            st.add_instance(os.path.join(halka, "YUVA_%s.SLDASM" % tip), offset_mm=(cx, 0, cz))
            st.add_instance(os.path.join(ORTAK, t["urun"], t["urun"] + ".SLDASM"), offset_mm=(cx, y1 - t["cd"], cz)); n += 1
    st.assemble("CEKMECE_" + tip)
    print("  CEKMECE_%s: %d adet (%dx%d) · x bosluk %.0f · z bosluk %.0f" % (tip, n, t["nx"], t["nz"], t["ax"]-2*t["r"], t["az"]-2*t["r"]))
    return n

def hamur_tepsi(tip, h, kc):
    """taze/donmuş: GN 2/1 çukurlu tepsi + 20 top (tepsi 530×650, 700 derinliğe sığar)"""
    st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip)
    from sw_hamur import TEPSI_W, TEPSI_D, TEPSI_H, CUKUR_R, CUKUR_H, ARALIK
    xc, zc = (KA+KB)/2, -DERIN/2
    X = [xc - 1.5*ARALIK + i*ARALIK for i in range(4)]; Z = [zc - 2*ARALIK + j*ARALIK for j in range(5)]
    st.load_dir()
    st.add_instance(os.path.join(ORTAK, "TEPSI_HAMUR_GN21", "TEPSI_HAMUR_GN21.SLDASM"), offset_mm=(0, kc - 3, 0))   # tepsi konumu kutu tabanına göre
    for cx in X:
        for cz in Z: st.add_instance(os.path.join(ORTAK, "HAMUR_TOPU_220g", "HAMUR_TOPU_220g.SLDASM"), offset_mm=(cx, kc + 1 + TEPSI_H - CUKUR_H, cz))
    st.assemble("CEKMECE_" + tip); print("  CEKMECE_%s: tepsi + 20 top (kutu %d)" % (tip, DERIN))

def motor_grubu():
    """MOTORLU RAY TAHRİK GRUBU (kasada sabit): 24 V redüktörlü motor Ø37×80 (ekseni X) + enkoder + kasnak + kayış + M12 soket + braket
       Yerel: kayış kasnağı ekseni (0,0,0); motor +X yönünde uzanır"""
    kok = os.path.join(ORTAK, "MOTOR_TAHRIK_GRUBU")
    if os.path.exists(os.path.join(kok, "MOTOR_TAHRIK_GRUBU.SLDASM")): return
    st = Station(kok, "MOTOR_TAHRIK_GRUBU"); p = "MTG_"
    st.cyl_z(p+"kasnak_D30_kayis", 0, 0, 15, -6, 6)                       # kayış kasnağı (çekmeceyi çeker)
    st.box(p+"reduktor_govde_37x37x40", 8, 48, -18.5, 18.5, -18.5, 18.5)  # sonsuz vida redüktör (kendinden kilitli)
    st.box(p+"motor_24V_37x37x80", 48, 128, -18.5, 18.5, -18.5, 18.5)     # DC motor gövdesi
    st.box(p+"enkoder_kapagi", 128, 143, -15, 15, -15, 15)                # Hall enkoder (konum)
    st.box(p+"M12_soket", 143, 158, -8, 8, -8, 8)                         # kablo soketi
    st.box(p+"montaj_braketi_3mm", 0, 60, -25, -18.5, -30, 30)            # kasaya vidalanır
    st.assemble("MOTOR_TAHRIK_GRUBU"); print("  MOTOR_TAHRIK_GRUBU: 24 V + reduktor + enkoder + kasnak")

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    motor_grubu()
    for tip in ("icecek", "1L"):
        t = TIP[tip]; kutu_ve_ray(tip, t["h"], t["kc"]); yuvali_tepsi(tip)
    for tip, h, kc in (("taze", 93.0, 8.0), ("donmus", 94.0, 8.0)):
        kutu_ve_ray(tip, h, kc); hamur_tepsi(tip, h, kc)
    print("BITTI — cekmeceler 700 derin, motor icin arkada 57 mm bosluk")
