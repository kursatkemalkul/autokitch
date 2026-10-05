# -*- coding: utf-8 -*-
"""AUTOKITCH - HAT ON GORUNUS v2 (12 Eyl 2026): BASE (ustte) + PRO (altta). Tek pafta, yalniz on gorunus.

v1'den FARKLARI
  1) STORE yeniden kurgulandi:
       KURAL pide hamuru    2 gun -18  +  1 gun +3
       KURAL lahmacun hamuru MAYASIZ -> hep +3 (dolapta 1 hafta dayanir, dondurulmuyor)
       KURAL lahmacun harci  3 gun +3 (Kemal karari 12 Eyl) -> DONDURUCUYA HARC GIRMIYOR
       KURAL icecek 1 hafta  ·  tum kolonlar %95+ dolu
       BASE K1 BOLMELI: alt -18 (donmus pide) / ust +3 (lahmacun) - tek kolonda iki sicaklik
  2) ROBOT AGIR KALDIRAN secildi (Kemal karari 12 Eyl): 25 kg sinifi kobot.
       Dolu kaset 18,4 kg -> robot kaseti dolu tasiyor. Kaset kucultulmuyor, sayi 9'da kaliyor.
       Sart: kasetin celik parcalari BORU'ya cevrilecek (bos 11,01 -> 5,60 kg).
  3) Kapasite sayilari lahmacun agirlikli menuye gore guncellendi (pide %33 / lahmacun %67).

Olculer modelden: PRESS v5 · TOPPING · OVEN v4 · PACK v3 · STORE.
Kural: paftada yalniz on gorunus + olcu + parca adi; aciklama mesajda.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT  = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_BASE_PRO_v2_on_gorunus.png"
OUT  = OUT.replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 4300, 3420
S    = 0.55                      # mm -> px
BG, INK, GRAY, LINE = (255,255,255), (26,26,28), (145,145,152), (72,72,78)
FILL, ACC, RED, SOFT = (244,244,246), (0,86,184), (198,42,32), (232,232,237)
BUZ, DOLAP = (28,86,166), (14,120,90)          # -18 / +3 bolge renkleri

def F(sz, b=False):
    for n in (("arialbd.ttf","segoeuib.ttf") if b else ("arial.ttf","segoeui.ttf")):
        try: return ImageFont.truetype(n, sz)
        except Exception: pass
    return ImageFont.load_default()
f9, f11, f13, f16, f22, f38 = F(16), F(19), F(22), F(26,1), F(34,1), F(52,1)

im = Image.new("RGB", (W_PX,H_PX), BG); d = ImageDraw.Draw(im)
def txt(x,y,s,f=f11,c=INK,a="la"): d.text((x,y),s,font=f,fill=c,anchor=a)

def olcu(x0,x1,y,s,c=INK,f=f11):
    d.line([(x0,y),(x1,y)],fill=c,width=2)
    for xx in (x0,x1): d.line([(xx,y-7),(xx,y+7)],fill=c,width=2)
    tw=d.textlength(s,font=f); d.rectangle([((x0+x1)/2-tw/2-7,y-14),((x0+x1)/2+tw/2+7,y+14)],fill=BG)
    txt((x0+x1)/2,y,s,f,c,"mm")

# ---------------- istasyon cephe tablolari (mm, modelden) ----------------
PRESS=[(121,1091,"k","FERSAH PZP-400"),(760,1020,"a","O1"),(1094,1392,"k","UC CEPLERI"),
       (1120,1370,"a","O2"),(1395,1672,"k","COP"),(1675,1968,"k","ATMA"),(1697,1947,"a","O3")]
TOPPING=[(210,489,"k","KASET alt2"),(492,771,"k","KASET alt1"),(774,891,"a","AGIZ"),
         (891,1170,"k","KASET kat3"),(1173,1290,"a","AGIZ"),(1290,1569,"k","KASET kat2"),
         (1572,1689,"a","AGIZ"),(1689,1968,"k","KASET kat1")]
OVEN4=[(123,370,"k","YAG KABI"),(373,533,"a","ISLEM AGZI"),(536,816,"k","KESICI+SPREY"),
       (822,1097,"k","FIRIN 1"),(1102,1377,"k","FIRIN 2"),(1382,1657,"k","FIRIN 3"),(1662,1968,"k","EGZOZ")]
OVEN6=[(123,370,"k","YAG KABI"),(373,533,"a","ISLEM AGZI"),(536,816,"k","KESICI+SPREY"),
       (822,1097,"k","FIRIN 1-2"),(1102,1377,"k","FIRIN 3-4"),(1382,1657,"k","FIRIN 5-6"),(1662,1968,"k","EGZOZ")]
PACK=[(123,420,"k","PANO"),(423,695,"k","VAKUM+TAHRIK"),(698,948,"a","KUTULAMA AGZI"),
      (951,1880,"k","KALIP + SARJOR")]

# ---------------- STORE: (kolon_genisligi, [(adet, cekmece_yuksekligi, etiket, bolge)]) ----------------
# hucre ici 182..1660 = 1477 mm · cekmece arasi fuga 3 · bolge degisince 14 mm yalitimli ara
# BASE gunluk: 70 pide + 141 lahmacun · tepsi 20 pide / 30 lahmacun
ST_BASE=[(700,[( 7,115,"DONMUS PIDE  140 top","-18"),      #  826  -> 2 gun
               ( 7, 88,"LAHMACUN  210 top","+3")]),        #  637          K1 = 1477 (%100)
         (700,[( 4, 88,"TAZE PIDE  80 top","+3"),          #  364  -> 1 gun
               (10, 88,"LAHMACUN  300 top","+3"),          #  910
               ( 1,132,"TATLI","+3")]),                    #  135          K2 = 1409 (%95)
         (700,[( 6,132,"ICECEK  378 kutu","+3"),           #  810  -> 1 hafta
               ( 2,300,"1 L  84 sise","+3")])]             #  606          K3 = 1416 (%96)
# PRO gunluk: 114 pide + 229 lahmacun (1,63 x BASE)
ST_PRO1=[(700,[(12,115,"DONMUS PIDE  240 top","-18")]),                                  # 1416 (%96)
         (700,[( 6, 88,"TAZE PIDE  120 top","+3"),(10,88,"LAHMACUN  300 top","+3")]),    # 1456 (%99)
         (700,[(16, 88,"LAHMACUN  480 top","+3")])]                                      # 1456 (%99)
ST_PRO2=[(700,[( 6,132,"ICECEK  378 kutu","+3"),( 2,300,"1 L  84 sise","+3")]),          # 1416 (%96)
         (700,[( 4,132,"ICECEK  252 kutu","+3"),( 2,300,"1 L  84 sise","+3"),
               ( 2,132,"TATLI","+3")])]                                                  # 1416 (%96)

def _zon_etiket(cx,cw,ybas,yson,zon):
    """kolon ici bolge seridi + sicaklik etiketi"""
    if zon is None: return
    col = BUZ if zon=="-18" else DOLAP
    d.rectangle([cx+6, yson, cx+6+9, ybas], fill=col)
    s = "-18 C" if zon=="-18" else "+3 C"
    tw = d.textlength(s, font=f9)
    ym = (ybas+yson)/2
    d.rectangle([cx+20, ym-12, cx+20+tw+10, ym+12], fill=(255,255,255), outline=col, width=1)
    txt(cx+25, ym, s, f9, col, "lm")

def kabin(ox,oy,w_mm,ad,bant=None,store=None,notu=None,vur=False):
    x0,x1 = ox, ox+w_mm*S
    y0,y1 = oy, oy-1970*S
    d.rectangle([x0,y1,x1,y0],fill=FILL,outline=LINE,width=3)
    d.rectangle([x0,y0-120*S,x1,y0],fill=SOFT,outline=LINE,width=2)      # plint
    SV=30*S
    if bant:
        for (b0,b1,tip,et) in bant:
            by1,by0 = oy-b1*S, oy-b0*S
            col,fl = (RED,(253,252,252)) if tip=="a" else (LINE,(255,255,255))
            d.rectangle([x0+SV,by1,x1-SV,by0],fill=fl,outline=col,width=3 if tip=="a" else 2)
            if et and (b1-b0)>120: txt((x0+x1)/2,(by0+by1)/2,et,f9,INK,"mm")
    if store:
        cx = x0
        d.rectangle([x0+SV,oy-1968*S,x1-SV,oy-1668*S],fill=SOFT,outline=LINE,width=2)   # sogutma grubu
        txt((x0+x1)/2,oy-1818*S,"SOGUTMA GRUBU  ·  kompresor · kondenser · fan",f9,GRAY,"mm")
        for (kw,gruplar) in store:
            cw = kw*S
            d.line([(cx+cw,y1),(cx+cw,y0)],fill=LINE,width=2)            # kapi ayirici
            yy = oy-182*S; onceki=None; zon_bas=yy
            for (adet,hh,et,zon) in gruplar:
                if onceki is not None and zon != onceki:                 # BOLGE SINIRI: yalitimli ara
                    d.rectangle([cx+SV,yy-14*S,cx+cw-SV,yy],fill=INK,outline=INK,width=2)
                    et2 = "YALITIMLI ARA BOLME 14"; tw2 = d.textlength(et2, font=f9)
                    d.rectangle([cx+cw/2-tw2/2-8, yy-7*S-13, cx+cw/2+tw2/2+8, yy-7*S+13],
                                fill=(255,255,255), outline=INK, width=1)
                    txt(cx+cw/2, yy-7*S, et2, f9, INK, "mm")
                    _zon_etiket(cx,cw,zon_bas,yy-14*S,onceki); zon_bas = yy-14*S
                    yy -= 14*S
                ybas = yy
                bol = BUZ if zon=="-18" else DOLAP
                for i in range(adet):
                    d.rectangle([cx+SV,yy-hh*S,cx+cw-SV,yy],fill=(255,255,255),outline=bol,width=1)
                    yy -= (hh+3)*S
                ym = (ybas+yy)/2; tw = d.textlength(et, font=f9)
                d.rectangle([cx+cw/2-tw/2-8, ym-13, cx+cw/2+tw/2+8, ym+13], fill=(255,255,255), outline=GRAY, width=1)
                txt(cx+cw/2, ym, et, f9, INK, "mm")
                onceki = zon
            _zon_etiket(cx,cw,zon_bas,yy,onceki)
            dolu = oy-182*S - yy
            txt(cx+cw/2, oy-1660*S-16, "%%%d dolu" % round(100*dolu/(1477*S)), f9, GRAY, "md")
            cx += cw
    txt((x0+x1)/2,y1-52,ad,f13,ACC if vur else INK,"md")
    txt((x0+x1)/2,y1-26,str(w_mm),f11,GRAY,"md")
    if notu: txt((x0+x1)/2,y0+120*S+16,notu,f9,GRAY,"ma")
    return x1

def hat(oy, kabinler, etiket, alt, ray_not):
    x = 330; ilk = x
    for k in kabinler: x = kabin(x, oy, *k[0:1], **k[1])
    son = x
    ry = oy-1970*S-92
    d.line([(ilk-45,ry),(son+45,ry)],fill=LINE,width=8)
    d.ellipse([ilk+120,ry-16,ilk+152,ry+16],fill=ACC)                      # robot arabasi
    if etiket=="PRO": d.ellipse([son-300,ry-16,son-268,ry+16],fill=RED)    # 2. robot
    txt(son+62,ry,ray_not,f9,GRAY,"lm")
    olcu(ilk,son,oy+118,"%d mm   ·   %.2f m"%((son-ilk)/S,(son-ilk)/S/1000),INK,f13)
    y0_ = oy-1970*S
    d.line([(ilk-72,y0_),(ilk-72,oy)],fill=INK,width=2)
    for yy in (y0_,oy): d.line([(ilk-79,yy),(ilk-65,yy)],fill=INK,width=2)
    txt(ilk-86,(y0_+oy)/2,"1970",f11,INK,"rm")
    txt(ilk-86,y0_-58,etiket,f22,ACC if etiket=="BASE" else RED,"la")
    txt(ilk-86,y0_-22,alt,f11,GRAY,"la")
    return ilk,son

def serit(x0,x1,y,bas,ogeler,renk):
    d.rectangle([x0,y,x1,y+66],fill=(250,250,252),outline=renk,width=2)
    txt(x0+22,y+33,bas,f16,renk,"lm")
    w=(x1-x0-260)/len(ogeler)
    for i,(a,b) in enumerate(ogeler):
        cx=x0+240+i*w
        txt(cx,y+16,a,f9,GRAY,"la"); txt(cx,y+40,b,f13,INK,"la")

# ================= PAFTA =================
txt(330,62,"AUTOKITCH  ·  HAT ON GORUNUS  ·  v2",f38,INK)
txt(330,126,"BASE ve PRO  ·  yalniz on gorunus  ·  olculer mm  ·  12 Eyl 2026",f13,GRAY)
d.line([(330,168),(W_PX-330,168)],fill=LINE,width=3)

B_OY = 1420
b0,b1 = hat(B_OY,[
  (2100,{"ad":"STORE","store":ST_BASE,"notu":"3 kapi · K1 bolmeli (alt -18 / ust +3)"}),
  (700,{"ad":"PRESS","bant":PRESS,"notu":"Fersah PZP-400"}),
  (700,{"ad":"TOPPING","bant":TOPPING,"notu":"14 yuva · 9 kaset · dolu kaset 18,4 kg"}),
  (700,{"ad":"OVEN","bant":OVEN4,"notu":"3 hazne · ortak havuz","vur":True}),
  (700,{"ad":"PACK","bant":PACK,"notu":"sarjor 487 kutu"}),
],"BASE","1 ROBOT 25 kg","ROBOT RAYI · 1 kol · 25 kg sinifi")
serit(330,b1,B_OY+160,"BASE",[("pik saat","32 urun"),("gunluk","211 urun"),
      ("pide / lahmacun","70 / 141"),("robot","%82"),("firin","%54"),("STORE","%97")],ACC)

P_OY = 2960
p0,p1 = hat(P_OY,[
  (2100,{"ad":"STORE 1","store":ST_PRO1,"notu":"K1 tam dondurucu"}),
  (1400,{"ad":"STORE 2","store":ST_PRO2,"notu":"EK icecek + tatli","vur":True}),
  (700,{"ad":"PRESS","bant":PRESS,"notu":"ayni"}),
  (700,{"ad":"TOPPING","bant":TOPPING,"notu":"ayni · gunde 2 dolum"}),
  (1000,{"ad":"OVEN","bant":OVEN6,"notu":"6 hazne · 4'u yeterli","vur":True}),
  (700,{"ad":"PACK","bant":PACK,"notu":"ayni"}),
],"PRO","2 ROBOT 25 kg","ROBOT RAYI · 2 kol · bolge kilidi")
serit(330,p1,P_OY+160,"PRO",[("pik saat","52 urun"),("gunluk","343 urun"),
      ("pide / lahmacun","114 / 229"),("robot","%83"),("firin","%65"),("kazanc","1,63 x")],RED)

ly=H_PX-96
txt(330,ly,"LEJANT",f13,INK)
LEJ=[(LINE,"kapak / panel"),(RED,"ACIK agiz - robot girisi"),(BUZ,"cekmece  -18 C"),(DOLAP,"cekmece  +3 C")]
for i,(c,a) in enumerate(LEJ):
    xx=330+i*470; d.rectangle([xx,ly+30,xx+32,ly+52],fill=(255,255,255),outline=c,width=3)
    txt(xx+44,ly+41,a,f11,INK,"lm")
txt(W_PX-330,ly+41,"kabin yuksekligi 1970 (plint 120 dahil)  ·  derinlik 840",f11,GRAY,"rm")

os.makedirs(os.path.dirname(OUT),exist_ok=True); im.save(OUT); print("yazildi:",OUT)
