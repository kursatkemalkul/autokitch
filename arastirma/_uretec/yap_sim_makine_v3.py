# -*- coding: utf-8 -*-
"""sim_makine_v2 -> v3. Kemal'in bulduklari:

1) "sos kasetlerinin parcalari eksenleri kayik biyerlerde donuyor" — DOGRU. Pompali kasette roller TERS:
   alt mil (CY 40) hazne paleti, ust mil (YC 195) POMPA ROTORU. Vidali kasette tam tersi. Sim ikisini de
   "helezon = dozaj" sayiyordu, o yuzden pompa hic donmuyor, hazne paleti doz hiziyla firil firil donuyordu.
   Cozum: her yuva hangi GRUBUN dozaj hangisinin karistirici oldugunu kendisi soyluyor.
2) "tepsi hep en soldan baslasin" — istasyon saga konmustu, sola alindi.
3) Gercekci dokulme icin agzin gercek kotu, z'si ve cikis capi lazim (uydurulmayacak).
"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "sim_makine_v2.py"), encoding="utf-8").read()

# --- agiz kotu/z'si ve cikis capi: modulun kendi parcalarindan olculur
eski = """    TB = H.S["tabla"]"""
yeni = """    AGZ_Z = {}                                                    # dozaj kovaninin z merkezi — agzin gercek yeri
    for p in TC.PARCALAR:
        if p["ad"].startswith("dozaj_kovani_"):
            b = p["wp"].val().BoundingBox()
            AGZ_Z[p["ad"][len("dozaj_kovani_"):]] = (b.zmin + b.zmax) / 2.0
    AGIZ_Y = TC.AGZ[1] + H.DUSME                                  # kovanin alt ucu = urunun serbest kaldigi kot
    TB = H.S["tabla"]"""
assert eski in s; s = s.replace(eski, yeni, 1)

# --- mil kotlarini toplarken cikis capini ve grup rollerini de al
eski = """        MIL_KOT[ad] = dict(helezon=TC.KAS[0] + mod.CY, karistirici=TC.KAS[0] + mod.YC, x=(x0 + x1) / 2.0)"""
yeni = """        MIL_KOT[ad] = dict(helezon=TC.KAS[0] + mod.CY, karistirici=TC.KAS[0] + mod.YC, x=(x0 + x1) / 2.0,
                           cap=mod.BORU_D)                        # cikis borusunun IC capi (kasetin kendi degeri)"""
assert eski in s; s = s.replace(eski, yeni, 1)

# --- yuva tanimina yeni alanlar
eski = """                            pompa=TC.KASET_CAD[ad].startswith("harc")))"""
yeni = """                            pompa=pmp,
                            # POMPALI kasette ust mil (YC) pompa rotoru, alt mil (CY) hazne paleti.
                            # VIDALI kasette alt mil (CY) dozaj helezonu, ust mil (YC) karistirici.
                            grup_doz="KARISTIRICI" if pmp else "HELEZON",
                            grup_karis="HELEZON" if pmp else "KARISTIRICI",
                            agiz_y=AGIZ_Y, agiz_z=AGZ_Z[k], cikis_cap=MIL_KOT[ad]["cap"],
                            # dokulme hizi: debi / kesit. rho 1,05 g/cm3 [V]
                            cikis_hiz=(DOZ[ad] / 10.0 / 1.05e-3) / (3.14159 * (MIL_KOT[ad]["cap"] / 2.0) ** 2),
                            # en buyuk parca: kopruleme kurali D >= 3 x parca -> parca = D/3
                            parca_mm=MIL_KOT[ad]["cap"] / 3.0))"""
assert eski in s; s = s.replace(eski, yeni, 1)

eski = """        k = ad.replace(" ", "_")
        yuvalar.append("""
yeni = """        k = ad.replace(" ", "_")
        pmp = TC.KASET_CAD[ad].startswith("harc")
        yuvalar.append("""
assert eski in s; s = s.replace(eski, yeni, 1)

# --- istasyon SOLA (Kemal: "tepsi hep en soldan baslasin")
s = s.replace('strok=[220.0, 1520.0], istasyon_x=1520.0', 'strok=[220.0, 1520.0], istasyon_x=220.0')
s = s.replace('cozunurluk_mm=0.01875, home_x=1520.0', 'cozunurluk_mm=0.01875, home_x=220.0')
assert 'istasyon_x=220.0' in s and 'home_x=220.0' in s

io.open(os.path.join(U, "sim_makine_v3.py"), "w", encoding="utf-8").write(s)
print("sim_makine_v3.py yazildi")
