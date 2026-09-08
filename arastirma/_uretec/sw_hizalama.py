# -*- coding: utf-8 -*-
# (1) İÇECEK/1 L çekmecelerine HİZALAMA SACI (hamur tepsisindeki çukur mantığı): 1,5 mm sac, her kutu/şişe yerinde delik
#     → kutular sabit merkezde durur, kaymaz. ÖN SIRA BOŞ = robotun alma pozisyonu (pençe/vantuz iner).
# (2) STORE kaset katına 4 standart kap + L raf çiftleri (önceki denemede AddComponent5 açık belge istediği için eklenememişti)
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); CEKD = os.path.join(ROOT, "cekmece"); ORTAK = os.path.join(ARA, "_ortak")
KAP = os.path.join(ARA, "3_TOPPING", "alt_montaj", "KAP_14x68x24", "KAP_14x68x24.SLDASM")
DERIN, KA, KB, KC = 740.0, 13.7, 604.3, 8.0
IC_X0, IC_W = 22.0, 590.6; ZI = -757.5; KASET_Y = 404.5
KAP_X = [151.5, 299.5, 447.5, 595.5]
KOLA_KANAL, KOLA_N, KOLA_ADIM, KOLA_R = 82.0, 11, 67.0, 33.0
SISE_KANAL, SISE_N, SISE_ADIM, SISE_R = 118.0, 8, 90.0, 44.0
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)

def kanal_merkez(adet, kanal_w):
    x0 = IC_X0 + (IC_W - adet*kanal_w)/2
    return [x0 + kanal_w/2 + k*kanal_w for k in range(adet)]

def hizalama_saci(tip, adet, kanal_w, n_derin, adim, r, z0):
    """delikli hizalama sacı 1,5 mm — kutu/şişe tabanını merkezler; ön sıra deliği de var (robot alma pozisyonu)"""
    st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip
    ad = p + "hizalama_saci_1.5"; yol = os.path.join(st.pdir, ad + ".SLDPRT")
    if os.path.exists(yol): os.remove(yol)
    y0 = KC + 4.0                                    # kutu tabanından 4 mm yukarıda (ayak sacları üstünde)
    merkez = kanal_merkez(adet, kanal_w)
    z_son = z0 - (n_derin-1)*adim
    ops = [(TP, 'rect', (KA+2, KB-2, -(0 - 5), -(z_son - r - 10)), y0, y0+1.5, False)]
    ops += [(TP, 'circ', (cx, -(z0 - j*adim), r+2), y0-1, y0+2.5, True) for cx in merkez for j in range(n_derin)]
    st.part(ad, ops); print("  %s hizalama saci: %d delik" % (tip, adet*n_derin))
    return merkez

def cekmece_kur(tip, adet, kanal_w, n_derin, adim, z0, urun, y_urun):
    """çekmeceyi yeniden kur: ÖN SIRA BOŞ (robot alma boşluğu), arkadaki sıralar dolu"""
    st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); st.load_dir()
    merkez = kanal_merkez(adet, kanal_w); n = 0
    for cx in merkez:
        for j in range(1, n_derin):                  # j=0 ön sıra BOŞ bırakılır
            st.add_instance(urun, offset_mm=(cx, y_urun, z0 - j*adim)); n += 1
    st.assemble("CEKMECE_" + tip)
    print("  CEKMECE_%s: %d dolu + %d bos alma pozisyonu (toplam yuva %d)" % (tip, n, adet, adet*n_derin))
    return n

def kaset_kati():
    """STORE kaset katı: 8 L raf + 4 standart kap — mevcut montaja eklenir (mate'ler korunur)"""
    st = Station(ROOT, "STORE"); p = "STORE_kaset_"; raflar = []
    for i, xc in enumerate(KAP_X, 1):
        for side, sx in (("sol", -1), ("sag", 1)):
            ad = p + "L_raf_%d_%s" % (i, side); yol = os.path.join(st.pdir, ad + ".SLDPRT")
            if not os.path.exists(yol):
                xe = xc + sx*54
                st.prism_z(ad, [(xe, KASET_Y), (xe+sx*2, KASET_Y), (xe+sx*2, KASET_Y+20), (xe-sx*6, KASET_Y+20), (xe-sx*6, KASET_Y+18), (xe, KASET_Y+18)], ZI+2, -20)
            raflar.append(yol)
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    var = set(c.Name2.rsplit("-", 1)[0] for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    eklendi = 0
    for yol in raflar:                                # AÇIK tut, ekle, sonra kapat (önceki hata buydu)
        ad = os.path.splitext(os.path.basename(yol))[0]
        if ad in var: continue
        dd = sw.OpenDoc6(yol, 1, 1, "", e, w); bb = bbox_of(dd)
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        if d.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2]) is not None: eklendi += 1
        sw.CloseDoc(dd.GetTitle)
    dd = sw.OpenDoc6(KAP, 2, 1, "", e, w); bb = [1e9]*3 + [-1e9]*3
    for cp in dd.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        g = cp.GetBox(False, False)
        for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
    kc = [(bb[i]+bb[i+3])/2 for i in range(3)]
    for xc in KAP_X:
        if d.AddComponent5(KAP, 0, "", False, "", kc[0] + xc*M, kc[1] + KASET_Y*M, kc[2]) is not None: eklendi += 1
    sw.CloseDoc(dd.GetTitle)
    comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith(("STORE_kaset_L_raf", "KAP_14x68x24")): c.Select4(True, NUL_, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(2)
    print("  kaset katina eklenen: %d | STORE bilesen: %d" % (eklendi, d.GetComponentCount(True)))
    for nm in ("LimitDistance1", "LimitDistance2", "LimitDistance3", "LimitDistance4"):
        p2 = d.Parameter("D1@" + nm)
        if p2 is not None: p2.SystemValue = 0.55
    mcall(d, "EditRebuild3"); time.sleep(2)
    png(d, os.path.join(ROOT, "STORE_hizalama.png"), "*Isometric")
    print("  kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    hizalama_saci("icecek", 7, KOLA_KANAL, KOLA_N, KOLA_ADIM, KOLA_R, -(2+33))
    cekmece_kur("icecek", 7, KOLA_KANAL, KOLA_N, KOLA_ADIM, -(2+33), os.path.join(ORTAK, "KUTU_KOLA_330ml", "KUTU_KOLA_330ml.SLDASM"), KC+5.5)
    hizalama_saci("1L", 5, SISE_KANAL, SISE_N, SISE_ADIM, SISE_R, -(2+44))
    cekmece_kur("1L", 5, SISE_KANAL, SISE_N, SISE_ADIM, -(2+44), os.path.join(ORTAK, "SISE_KOLA_1L", "SISE_KOLA_1L.SLDASM"), KC+5.5)
    kaset_kati()
    print("BITTI")
