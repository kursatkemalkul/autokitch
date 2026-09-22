# -*- coding: utf-8 -*-
"""AUTOKITCH - BASE · STORE + TOPPING · DERINLIK 830 (12 Eyl 2026)

ENDUSTRIYEL STANDART: dik tip GN 2/1 buzdolabi 830 derin
  (Oztiryakiler 79K4.12NMV.10 “Dort Yarim Kapili 430 K”: En 830 = DERINLIK, Boy 1344, Yukseklik 2000)
KATMAN (dis-dis): arka sac 1,5 + PU 60 + ic sac 1 + PLENUM 47,5 + CEKMECE 680 + on sandvic 40 = 830
  onceki 860 idi: plenum 57,5 + cekmece 700.  PU 60 KORUNDU (Oztiryakiler 40-42 kg/m3, 60 mm).
BEDELI: cekmece 700 -> 680 · icecek 63 -> 56 kutu · 1 L 42 -> 36 sise -> +1 icecek +1 1L cekmece (33 -> 35).

Yalniz BASE. STORE v5 kurgusu (2740 / 4 kolon x 620 / 33 cekmece) ve TOPPING v4 (14 yuva) yan yana.
Hatta aralarinda PRESS var; burada karsilastirma icin yan yana cizildi.

KUTLELER: cekmece yapisal parcalari SolidWorks hacmi x yogunluk (304: 8000, PU: 40, conta: 1200);
urunler adet x gercek birim agirlik (kutu 0,355 · sise 1,05 · top 0,22/0,11 · silikon tepsi 1,6).
Kaset bos 7,54 kg (SolidWorks olcumu, boru milli v4).
NOT: modeldeki cekmece raylari DOLU 45x12,7 blok (3,0 kg/ray). Gercek teleskopik ray ~1,0 kg.
     Tablodaki "model" sutunu modeli, "gercek" sutunu ray duzeltmesini gosterir (-4 kg/cekmece).
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\STORE_TOPPING_v2_830_on_plan_tablo.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 3000, 2760
S = 0.62
BG, INK, GRAY, LINE = (255,255,255), (26,26,28), (140,140,148), (72,72,78)
FILL, ACC, RED, SOFT = (244,244,246), (0,86,184), (198,42,32), (232,232,237)
BUZ, DOLAP, BOSL, PUC = (28,86,166), (14,120,90), (190,190,196), (255,240,200)

def F(sz, b=False):
    for n in (("arialbd.ttf","segoeuib.ttf") if b else ("arial.ttf","segoeui.ttf")):
        try: return ImageFont.truetype(n, sz)
        except Exception: pass
    return ImageFont.load_default()
f7, f8, f9, f11, f13, f16, f22, f38 = F(13), F(15), F(17), F(20), F(23), F(27,1), F(35,1), F(50,1)
im = Image.new("RGB", (W_PX,H_PX), BG); d = ImageDraw.Draw(im)
def txt(x,y,s,f=f11,c=INK,a="la"): d.text((x,y),s,font=f,fill=c,anchor=a)
def olcu(x0,x1,y,s,c=INK,f=f11,dik=False):
    if dik:
        d.line([(x0,y),(x0,x1)],fill=c,width=2)
        for yy in (y,x1): d.line([(x0-7,yy),(x0+7,yy)],fill=c,width=2)
        txt(x0-10,(y+x1)/2,s,f,c,"rm"); return
    d.line([(x0,y),(x1,y)],fill=c,width=2)
    for xx in (x0,x1): d.line([(xx,y-7),(xx,y+7)],fill=c,width=2)
    tw=d.textlength(s,font=f); d.rectangle([((x0+x1)/2-tw/2-6,y-13),((x0+x1)/2+tw/2+6,y+13)],fill=BG)
    txt((x0+x1)/2,y,s,f,c,"mm")

# ======================= VERI =======================
CELL0, CELL1, BIND, FUGA_C = 182.5, 1660.0, 15.0, 3.0
YUZ0 = CELL0 - BIND; XI, WO = 62.5, 620.0
HH  = {"donmus":115.0,"hamur":88.0,"lahm":88.0,"icecek":132.0,"1L":300.0}
AD  = {"donmus":"DONMUS PIDE","hamur":"TAZE PIDE","lahm":"LAHMACUN","icecek":"ICECEK 330 ml","1L":"1 L SISE"}
CAP = {"donmus":20,"hamur":20,"lahm":30,"icecek":56,"1L":36}     # 680 derin cekmece izgarasi
BR  = {"donmus":"top","hamur":"top","lahm":"top","icecek":"kutu","1L":"sise"}
IHT = {"donmus":140,"hamur":70,"lahm":423,"icecek":315,"1L":77}
GUN = {"donmus":"2 gun","hamur":"1 gun","lahm":"3 gun","icecek":"7 gun","1L":"7 gun"}
# SolidWorks olcumu (yapi) + urun · "gercek": ray 3,0 -> 1,0 kg x2 = -4,0
# SolidWorks olcumu 700'luk cekmeceden; 680'de boya bagli parcalar (kutu U, taban saci,
# raylar, hizalama saci) %2,9 kisaliyor -> yapi -0,4..-0,6 kg.
KG = {"donmus":(17.8, 6.00), "hamur":(17.0, 6.00), "lahm":(17.0, 4.90), "icecek":(21.0, 19.88), "1L":(26.0, 37.80)}
ST = dict(kolon=[[(7,"donmus","-18"),"ayirici",(3,"lahm","+3")],
                 [(12,"lahm","+3")],
                 [(4,"hamur","+3"),(6,"icecek","+3")],
                 [(3,"1L","+3")]],
          bolme=[65,35,35])
WS = 2*XI + 4*WO + sum(ST["bolme"])          # 2740
# --- TOPPING ---
TOPPING=[(210,489,"k","alt2"),(492,771,"k","alt1"),(774,891,"a","AGIZ"),(891,1170,"k","kat3"),
         (1173,1290,"a","AGIZ"),(1290,1569,"k","kat2"),(1572,1689,"a","AGIZ"),(1689,1968,"k","kat1")]
KASET_BOS = 7.54
K3G = {"harc":33.84,"kasar":10.71,"kiyma":9.45,"sucuk":4.20,"kusbasi":4.74}       # 3 gun kg
KYOG= {"harc":1.02,"kasar":0.38,"kiyma":1.02,"sucuk":0.55,"kusbasi":0.80}
KAD = {"harc":"LAHMACUN HARCI","kasar":"KASAR","kiyma":"KIYMA","sucuk":"SUCUK","kusbasi":"KUSBASI"}
ROBOT_NET = 16.5
import math
KASET = {}
for k, kg3 in K3G.items():
    kap_kg = min(12.5*KYOG[k], ROBOT_NET-KASET_BOS)          # kaset dolum siniri: hacim ya da robot
    n = math.ceil(kg3/kap_kg); KASET[k] = (n, kg3/n, kg3/n/KYOG[k])
# yuva yerlesimi: dozaj 6 (kat1 2, kat2 2, kat3 2) · depo 8 (alt1 4, alt2 4)
DOZAJ = ["harc","kasar","kiyma","sucuk","kusbasi",None]
DEPO  = ["harc","harc","harc","kasar","kasar","kiyma",None,None]
YUVA_KAT = {"kat1":("kasar","sucuk"),"kat2":("harc",None),"kat3":("kiyma","kusbasi"),
            "alt1":("harc","harc","harc","kasar"),"alt2":("kasar","kiyma",None,None)}

# ======================= ON GORUNUS =======================
def on_store(ox, oy):
    x0, x1 = ox, ox+WS*S; y0, y1 = oy, oy-1970*S
    d.rectangle([x0,y1,x1,y0],fill=FILL,outline=LINE,width=3)
    d.rectangle([x0,y0-120*S,x1,y0],fill=SOFT,outline=LINE,width=2)
    d.rectangle([x0+30*S,oy-1968*S,x1-30*S,oy-1668*S],fill=SOFT,outline=LINE,width=2)
    txt((x0+x1)/2,oy-1818*S,"SOGUTMA GRUBU · kompresor · kondenser · fan",f8,GRAY,"mm")
    cx = x0 + XI*S; kolx = []
    for ki, gruplar in enumerate(ST["kolon"]):
        cw = WO*S; y = YUZ0; cv = 8*S; kolx.append(cx)
        if ki:
            bw = ST["bolme"][ki-1]*S
            d.rectangle([cx-bw,oy-CELL1*S,cx,oy-YUZ0*S],fill=(INK if ST["bolme"][ki-1]>=60 else SOFT),outline=LINE,width=1)
        for g in gruplar:
            if g == "ayirici":
                yb = y+3.0; d.rectangle([cx+cv,oy-(yb+42)*S,cx+cw-cv,oy-yb*S],fill=INK); y = yb+45.0; continue
            adet, tip, zon = g; h = HH[tip]+2*BIND; ybas = y
            for i in range(adet):
                d.rectangle([cx+cv,oy-(y+h)*S,cx+cw-cv,oy-y*S],fill=(255,255,255),outline=(BUZ if zon=="-18" else DOLAP),width=1)
                y += h+FUGA_C
            et = "%s %d" % (AD[tip].split()[0] if tip!="1L" else "1 L", adet); ym = oy-((ybas+y-FUGA_C)/2)*S; tw=d.textlength(et,font=f8)
            d.rectangle([cx+cw/2-tw/2-6,ym-10,cx+cw/2+tw/2+6,ym+10],fill=(255,255,255),outline=GRAY,width=1); txt(cx+cw/2,ym,et,f8,INK,"mm")
            zt = "-18 C" if zon=="-18" else "+3 C"; tz = d.textlength(zt,font=f7)
            d.rectangle([cx+cv+4,ym-9,cx+cv+4+tz+8,ym+9],fill=(255,255,255),outline=(BUZ if zon=="-18" else DOLAP),width=1)
            txt(cx+cv+8,ym,zt,f7,(BUZ if zon=="-18" else DOLAP),"lm")
        bos = CELL1-(y-FUGA_C)
        if bos > 20:
            by1, by0 = oy-CELL1*S, oy-(y-FUGA_C)*S
            d.rectangle([cx+cv,by1,cx+cw-cv,by0],fill=(250,250,251),outline=BOSL,width=1)
            for k in range(0, int(cw-2*cv), 12):
                xx=cx+cv+k; L=min(by0-by1, cw-2*cv-k); d.line([(xx,by0),(xx+L,by0-L)],fill=(226,226,232),width=1)
            et="BOS %d" % round(bos); tw=d.textlength(et,font=f8)
            d.rectangle([cx+cw/2-tw/2-6,(by0+by1)/2-10,cx+cw/2+tw/2+6,(by0+by1)/2+10],fill=(255,255,255),outline=BOSL,width=1); txt(cx+cw/2,(by0+by1)/2,et,f8,GRAY,"mm")
        txt(cx+cw/2, oy-1660*S-13, "K%d · %%%d" % (ki+1, round(100*(y-FUGA_C-YUZ0)/(CELL1-YUZ0))), f8, GRAY, "md")
        cx += cw + (ST["bolme"][ki]*S if ki < 3 else 0)
    txt((x0+x1)/2,y1-46,"STORE v5  ·  2740 x 830",f16,ACC,"md")
    olcu(x0,x1,y0+40,"2740",INK,f11)
    for i,kx in enumerate(kolx): olcu(kx,kx+WO*S,y0+80,"620",GRAY,f8)
    olcu(x0-40,y1,y0,"1970",INK,f11,dik=True)
    return x1

def on_topping(ox, oy):
    x0, x1 = ox, ox+700*S; y0, y1 = oy, oy-1970*S
    d.rectangle([x0,y1,x1,y0],fill=FILL,outline=LINE,width=3)
    d.rectangle([x0,y0-120*S,x1,y0],fill=SOFT,outline=LINE,width=2)
    SV=30*S
    for (b0,b1,tip,et) in TOPPING:
        by1,by0 = oy-b1*S, oy-b0*S
        col,fl = (RED,(253,252,252)) if tip=="a" else (LINE,(255,255,255))
        d.rectangle([x0+SV,by1,x1-SV,by0],fill=fl,outline=col,width=3 if tip=="a" else 2)
        if tip=="k":
            yuva = YUVA_KAT[et]; n = len(yuva); kw = (640.0/n)
            for i,kk in enumerate(yuva):
                kx0 = x0+SV+i*kw*S; kx1 = kx0+kw*S
                d.rectangle([kx0+3,by1+3,kx1-3,by0-3],fill=((255,255,255) if kk else (250,250,251)),outline=(INK if kk else BOSL),width=1)
                txt((kx0+kx1)/2,(by0+by1)/2-9,(KAD[kk].split()[0] if kk else "BOS"),f7,(INK if kk else GRAY),"mm")
                if kk: txt((kx0+kx1)/2,(by0+by1)/2+9,"%.1f kg" % (KASET_BOS+KASET[kk][1]),f7,GRAY,"mm")
            txt(x0+SV+4,by1+9,et+(" DOZAJ" if et.startswith("kat") else " DEPO"),f7,GRAY,"la")
        else: txt((x0+x1)/2,(by0+by1)/2,"ROBOT AGZI · tepsi",f7,RED,"mm")
    txt((x0+x1)/2,y1-46,"TOPPING v4  ·  700 x 830",f16,ACC,"md")
    olcu(x0,x1,y0+40,"700",INK,f11)
    return x1

# ======================= PLAN KESITI =======================
DZ = 830.0    # z -790..+40  (Oztiryakiler dik dolap standardi)
def plan_store(ox, oy):
    """plan kesiti — +3 kolon cekmece seviyesinden. ox,oy = sol-ON kose (z=+40)"""
    def P(x, z): return (ox + x*S, oy + (z+790)*S)       # z=-820 arka (ustte), z=+40 on (altta)
    x0,y0 = P(0,-820); x1,y1 = P(WS,40)
    d.rectangle([x0,y0,x1,y1],fill=FILL,outline=LINE,width=3)
    # PU yan + arka
    for (a,b) in ((1.5,61.5),(WS-61.5,WS-1.5)): d.rectangle([P(a,-788.5),P(b,-16)],fill=PUC,outline=GRAY,width=1)
    d.rectangle([P(61.5,-788.5),P(WS-61.5,-728.5)],fill=PUC,outline=GRAY,width=1)
    txt(*P(WS/2,-758),"PU 60 · arka",f7,GRAY,"mm")
    cx = XI
    for ki in range(4):
        if ki:
            bw = ST["bolme"][ki-1]; d.rectangle([P(cx-bw,-727.5),P(cx,-16)],fill=(INK if bw>=60 else SOFT),outline=LINE,width=1)
        # cekmece kutusu 620 x 700 (z -700..0) + on yuz 40
        d.rectangle([P(cx+16,-680),P(cx+WO-16,0)],fill=(255,255,255),outline=DOLAP,width=2)
        d.rectangle([P(cx-15,0),P(cx+WO+15,40)],fill=(255,255,255),outline=DOLAP,width=2)
        # raylar
        for rx in (cx+1, cx+WO-15): d.rectangle([P(rx,-640),P(rx+14,0)],fill=SOFT,outline=GRAY,width=1)
        # arka plenum: evaporator + fan + motor
        d.rectangle([P(cx+190,-725),P(cx+450,-680)],fill=(220,235,255),outline=BUZ,width=1); txt(*P(cx+320,-703),"EVAP 45",f7,BUZ,"mm")
        d.rectangle([P(cx+17,-716),P(cx+67,-680)],fill=(255,230,230),outline=RED,width=1); txt(*P(cx+42,-698),"M 36",f7,RED,"mm")
        txt(*P(cx+WO/2,-350),"K%d" % (ki+1),f11,GRAY,"mm")
        txt(*P(cx+WO/2,-120),"620 x 680",f7,GRAY,"mm")
        cx += WO + (ST["bolme"][ki] if ki<3 else 0)
    txt(*P(WS/2,-702),"ARKA PLENUM 47,5 · evaporator 45 · fan 40 · motor 36",f7,GRAY,"mm")
    olcu(x0-40,y0,y1,"830",INK,f11,dik=True)
    txt(*P(WS/2, 40+70),"STORE v5 · PLAN KESITI (+3 kolon, cekmece seviyesi) · DERINLIK 830",f11,ACC,"mm")
    return x1

def plan_topping(ox, oy):
    def P(x, z): return (ox + x*S, oy + (z+790)*S)
    x0,y0 = P(0,-820); x1,y1 = P(700,40)
    d.rectangle([x0,y0,x1,y1],fill=FILL,outline=LINE,width=3)
    for (a,b) in ((1.5,61.5),(638.5,698.5)): d.rectangle([P(a,-788.5),P(b,-16)],fill=PUC,outline=GRAY,width=1)
    d.rectangle([P(61.5,-788.5),P(638.5,-728.5)],fill=PUC,outline=GRAY,width=1)
    # 2 kaset (kat) 140 x 680 (z -700..-20)
    for xc in (270, 430):
        d.rectangle([P(xc-70,-695.5),P(xc+70,-15.5)],fill=(255,255,255),outline=INK,width=2)
        txt(*P(xc,-360),"KASET",f7,INK,"mm"); txt(*P(xc,-330),"140 x 680",f7,GRAY,"mm")
        d.rectangle([P(xc-35,-775),P(xc+35,-695.5)],fill=(255,230,230),outline=RED,width=1); txt(*P(xc,-735),"SOKET+M",f7,RED,"mm")
    # tepsi O320 (agiz bandinda, altta) — plan izdusumu
    cxp, czp = P(350,-130); r = 160*S
    d.ellipse([cxp-r,czp-r,cxp+r,czp+r],outline=RED,width=2); txt(cxp,czp,"tepsi O320",f7,RED,"mm")
    txt(*P(350,40+70),"TOPPING v4 · PLAN KESITI — 830 icin kaset 4,5 mm one kayar (soket 32 mm bosluk ister)",f11,ACC,"mm")
    return x1

# ======================= TABLO =======================
def tablo(ox, oy, baslik, kolonlar, satirlar, genis, renk=INK):
    txt(ox, oy, baslik, f13, renk); y = oy+34
    d.rectangle([ox,y,ox+sum(genis),y+30],fill=SOFT,outline=LINE,width=1)
    x = ox
    for k,g in zip(kolonlar,genis): txt(x+8,y+15,k,f8,GRAY,"lm"); x += g
    y += 30
    for sat in satirlar:
        bold = sat[0].startswith("TOPLAM")
        d.rectangle([ox,y,ox+sum(genis),y+28],fill=((250,250,252) if bold else (255,255,255)),outline=LINE,width=1)
        x = ox
        for v,g in zip(sat,genis): txt(x+8,y+14,str(v),(f9 if bold else f8),INK,"lm"); x += g
        y += 28
    return y

# ======================= PAFTA =======================
txt(240,52,"AUTOKITCH  ·  BASE  ·  STORE + TOPPING",f38,INK)
txt(240,110,"on gorunus · plan kesiti · stok ve kutle tablosu  ·  olculer mm  ·  12 Eyl 2026",f13,GRAY)
d.line([(240,146),(W_PX-240,146)],fill=LINE,width=3)

OY1 = 1470
x_end = on_store(240, OY1)
on_topping(x_end+120*S, OY1)

OY2 = OY1 + 200                       # plan ustu (z=-820 arka kenar)
x_end2 = plan_store(240, OY2)
plan_topping(x_end2+120*S, OY2)

# ---- STORE tablosu ----
TY = OY2 + DZ*S + 150                # plan altindan 150 px asagi
say = {}
for K in ST["kolon"]:
    for g in K:
        if g=="ayirici": continue
        n,t,_ = g; say[t] = say.get(t,0)+n
sat = []; tb=tk=tg=0
for t in ("donmus","hamur","lahm","icecek","1L"):
    n = say[t]; yapi, urun = KG[t]; dolu = yapi+urun; gercek = dolu-4.0
    sat.append((AD[t], GUN[t], n, "%d %s" % (CAP[t],BR[t]), IHT[t], n*CAP[t], "+%d" % (n*CAP[t]-IHT[t]),
                "%.1f" % yapi, "%.1f" % urun, "%.1f" % dolu, "%.1f" % gercek, "%.0f" % (n*gercek)))
    tb += n; tk += n*dolu; tg += n*gercek
sat.append(("TOPLAM", "", tb, "", "", "", "", "", "", "", "", "%.0f" % tg))
y = tablo(240, TY, "STORE — CEKMECE · STOK · KUTLE   (kg)",
      ("urun","sure","cekmece","cekmece basina","ihtiyac","kapasite","fazla","bos yapi (model)","urun","DOLU (model)","DOLU (gercek ray)","toplam"),
      sat, (190,70,80,120,80,90,70,140,70,110,140,90))
txt(240, y+10, "bos yapi: SolidWorks hacmi x yogunluk. Model raylari dolu blok (3,0 kg/ray); gercek teleskopik ray ~1,0 kg -> 'gercek' = model - 4,0. "
               "Tepsi taban saci 1,5 mm (4,9 kg) -> 1,0 mm ile -1,6 kg daha.", f7, GRAY)

# ---- KASET tablosu ----
KX = 240 + 1490
ksat = []; kt=kk=0
for k in ("harc","kasar","kiyma","sucuk","kusbasi"):
    n, kg1, L1 = KASET[k]; dolu = KASET_BOS+kg1
    ndoz = DOZAJ.count(k); ndep = DEPO.count(k)
    ksat.append((KAD[k], "%.1f" % K3G[k], n, "%.1f" % kg1, "%.1f L" % L1, "%.1f" % dolu, ndoz, ndep))
    kt += n; kk += n*dolu
ksat.append(("TOPLAM", "%.1f" % sum(K3G.values()), kt, "", "", "%.0f" % kk, 5, 6))
y2 = tablo(KX, TY, "TOPPING — KASET · 3 GUN   (kg)",
      ("urun","3 gun kg","kaset","kg / kaset","hacim","DOLU kg","dozaj","depo"), ksat, (170,80,60,90,80,80,60,60))
txt(KX, y2+10, "kaset bos 7,54 kg (SW). Robot net 16,5 kg -> dolum <= 8,96 kg. 14 yuva: 6 dozaj + 8 depo. "
               "Kullanilan 11 · bos 3 (kat2 sag, alt2 x2). Modelde 13 kaset ornegi var.", f7, GRAY)

# ---- lejant ----
ly=H_PX-70
LEJ=[(BUZ,"-18 C"),(DOLAP,"+3 C"),(INK,"yalitim 65 / bant 42"),(BOSL,"BOS"),(RED,"acik agiz / motor"),(PUC,"PU 60 yalitim")]
for i,(c,a) in enumerate(LEJ):
    xx=240+i*300; d.rectangle([xx,ly+8,xx+26,ly+26],fill=(c if c in (INK,PUC) else (255,255,255)),outline=c,width=2); txt(xx+34,ly+17,a,f9,INK,"lm")
txt(W_PX-240,ly+17,"kabin 1970 x 830 (Oztiryakiler std) · plint 120 · cekmece 620 x 680 · alin 33 · kaset 140 x 240 x 680",f8,GRAY,"rm")
os.makedirs(os.path.dirname(OUT),exist_ok=True); im.save(OUT); print("yazildi:", OUT)
