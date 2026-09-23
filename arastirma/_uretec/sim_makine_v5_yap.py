# -*- coding: utf-8 -*-
"""sim_makine_v3 -> v4 : TEPSISIZ KURGU (site animasyonu icin)

Animasyondaki "her sey kaymis" sikayetinin sebebi: model v20'ye gecti ama
sim_makine.json hala tepsili kurgunun sayilarini tasiyordu.
  strok 220...1520   -> tabla soldaki aciciya GIDEMIYOR
  pide ust_y 120     -> tepsi 12 mm + hamur 8 mm varsayimiyla hesaplanmisti
  tepsi_k 12         -> artik tepsi YOK

BU SURUM
  strok        -350 ... 1627   (sol uc ACICI, sag uc BANDA AKTARMA)
  home_x       -350
  pide.ust_y   116  = calisma diski ust yuzu 108 + hamur 8
  tepsi_k      0
  top_r        acilmis pidenin HACMINDEN cikti (V = pi r^2 h), uydurma degil
  acici        kafa konumu ve sureleri
  aktarma      kopru konumu ve bant hizi
"""
import io, math, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "sim_makine_v3.py"), encoding="utf-8").read()

s = s.replace("import topping_cad_v10 as TC", "import topping_cad_v21 as TC")
s = s.replace("import topping_hesap_v4 as H", "import topping_hesap_v5 as H")

eski = """                   strok=[220.0, 1520.0], istasyon_x=220.0, eksen_z=ZT, pivot=[Xc, 0.0, ZT], baslangic_x=Xc),"""
yeni = """                   # v4 · TEPSISIZ KURGU: strok iki ucta da uzadi.
                   #  -350 : ACICI — robot hamur topunu buraya birakir, konili kafa acar
                   #  1627 : BANDA AKTARMA — pidenin on kenari kopruye ciker, bant ceker
                   strok=[-350.0, 1637.0], istasyon_x=-350.0, acici_x=-350.0, aktarma_x=1637.0,
                   eksen_z=ZT, pivot=[Xc, 0.0, ZT], baslangic_x=Xc),"""
assert eski in s
s = s.replace(eski, yeni, 1)

eski = """               cozunurluk_mm=0.01875, home_x=220.0, limit=[205.0, 1535.0]),"""
yeni = """               cozunurluk_mm=0.01875, home_x=-350.0, limit=[-380.0, 1660.0]),"""
assert eski in s
s = s.replace(eski, yeni, 1)

V = math.pi * 140.0 ** 2 * 8.0                      # acilmis pidenin hacmi (hamur_k = 8)
RTOP = (3.0 * V / (4.0 * math.pi)) ** (1.0 / 3.0)   # ayni hacimli kurenin yaricapi

eski = """        pide=dict(yaricap=140.0, kenar=15.0, ust_y=TC.AGZ[1], tepsi_k=H.TEPSI_K, hamur_k=H.HAMUR_K),"""
yeni = ("""        # v4 · TEPSI YOK. Hamur dogrudan CALISMA DISKININ ustunde (disk ust yuzu y 108).
        # Top yaricapi UYDURMA DEGIL: acilmis pidenin hacminden geliyor (V = pi r^2 h).
        pide=dict(yaricap=140.0, kenar=0.0, disk_ust=108.0, ust_y=108.0 + H.HAMUR_K,
                  tepsi_k=0.0, hamur_k=H.HAMUR_K, top_r=%.1f),
        acici=dict(x=-350.0, park_y=1200.0, calisma_y=1128.0, in_sn=0.8, ac_sn=3.0, kalk_sn=0.6,
                   not_="konili doner acici · olculer VARSAYIM, tedarikciden gelecek"),
        aktarma=dict(x=1637.0, bant_burun_x=1815.0, bant_y=106.0, bant_hiz=120.0),""" % round(RTOP, 1))
assert eski in s
s = s.replace(eski, yeni, 1)


eski = """    Xc, ZT = 900.0, TC.ZK[0] + 30.0"""
yeni = """    # v4: tabla artik PARK KONUMUNDA ciziliyor (acicinin alti). Sayiyi burada
    # tekrar yazmiyoruz — CAD'in cizdigi yerden okunuyor ki ikisi ayrilmasin.
    Xc, ZT = TC.XC_TABLA, TC.ZK[0] + 30.0"""
assert eski in s
s = s.replace(eski, yeni, 1)

io.open(os.path.join(U, "sim_makine_v5.py"), "w", encoding="utf-8").write(s)
print("sim_makine_v5.py yazildi · hamur topu yaricapi %.1f mm" % RTOP)
