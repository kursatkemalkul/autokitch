# -*- coding: utf-8 -*-
"""AUTOKITCH — HAT ON GORUNUS: BASE (ustte) + PRO (altta). Tek pafta, yalniz on gorunus.
Olculer modelden: PRESS v5 · TOPPING · OVEN v4 · PACK v3 · STORE (yeni 3 kapili kurgu).
Kural: yalniz on gorunus + olcu + parca adi; aciklama mesajda."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT  = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_BASE_PRO_on_gorunus.png"
W_PX, H_PX = 4300, 3420
S    = 0.55                      # mm -> px
BG, INK, GRAY, LINE = (255,255,255), (26,26,28), (145,145,152), (72,72,78)
FILL, ACC, RED, SOFT = (244,244,246), (0,86,184), (198,42,32), (232,232,237)

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

# STORE kolonlari: (genislik_mm, [(adet, yukseklik_mm, etiket)])
# hucre ici 182..1660 = 1477 mm (ustu sogutma grubu). Her kolon ~%95 dolu.
ST_BASE=[(700,[(5,115,"DONMUS PIDE 100"),(9,88,"LAHMACUN 270")]),          # K1  -18   1409
         (700,[(14,88,"TAZE PIDE 280"),(1,132,"TATLI")]),                   # K2  +3    1409
         (700,[(6,132,"ICECEK 378"),(2,300,"1 L  84")])]                    # K3  +3    1416
ST_PRO2=[(700,[(14,88,"TAZE PIDE +280"),(1,132,"TATLI")]),
         (700,[(5,115,"DONMUS +100"),(9,88,"LAHMACUN +270")])]

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
            yy = oy-182*S
            for (adet,hh,et) in gruplar:
                ybas = yy
                for i in range(adet):
                    d.rectangle([cx+SV,yy-hh*S,cx+cw-SV,yy],fill=(255,255,255),outline=LINE,width=1)
                    yy -= (hh+3)*S
                ym = (ybas+yy)/2; tw = d.textlength(et, font=f9)
                d.rectangle([cx+cw/2-tw/2-8, ym-13, cx+cw/2+tw/2+8, ym+13], fill=(255,255,255), outline=GRAY, width=1)
                txt(cx+cw/2, ym, et, f9, INK, "mm")
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
    txt(son+62,ry,ray_not,f9,GRAY,"lm")
    olcu(ilk,son,oy+118,"%d mm   ·   %.2f m"%((son-ilk)/S,(son-ilk)/S/1000),INK,f13)
    d.line([(ilk-72,y0_:=oy-1970*S),(ilk-72,oy)],fill=INK,width=2)
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
txt(330,62,"AUTOKITCH  ·  HAT ON GORUNUS",f38,INK)
txt(330,126,"BASE  ve  PRO  ·  yalniz on gorunus  ·  olculer mm  ·  11 Eyl 2026",f13,GRAY)
d.line([(330,168),(W_PX-330,168)],fill=LINE,width=3)

B_OY = 1420
b0,b1 = hat(B_OY,[
  (2100,{"ad":"STORE","store":ST_BASE,"notu":"3 kapi · hamur 3 gun · icecek 1 hafta"}),
  (700,{"ad":"PRESS","bant":PRESS,"notu":"Fersah PZP-400"}),
  (700,{"ad":"TOPPING","bant":TOPPING,"notu":"13 kaset · 3 gun"}),
  (700,{"ad":"OVEN","bant":OVEN4,"notu":"3 hazne · ortak havuz","vur":True}),
  (700,{"ad":"PACK","bant":PACK,"notu":"sarjor 487 kutu"}),
],"BASE","1 ROBOT","ROBOT RAYI · 1 kol")
serit(330,b1,B_OY+160,"BASE",[("pik saat","30 urun"),("gunluk","200 urun"),
      ("pide / lahmacun","112 / 88"),("robot","%80"),("STORE","%100"),("firin","%54")],ACC)

P_OY = 2960
p0,p1 = hat(P_OY,[
  (2100,{"ad":"STORE 1","store":ST_BASE,"notu":"ayni"}),
  (1400,{"ad":"STORE 2","store":ST_PRO2,"notu":"EK hamur kabini","vur":True}),
  (700,{"ad":"PRESS","bant":PRESS,"notu":"ayni"}),
  (700,{"ad":"TOPPING","bant":TOPPING,"notu":"gunluk dolum"}),
  (1000,{"ad":"OVEN","bant":OVEN6,"notu":"6 hazne · 2 tepsi yan yana","vur":True}),
  (700,{"ad":"PACK","bant":PACK,"notu":"ayni"}),
],"PRO","2 ROBOT","ROBOT RAYI · 2 kol · bolge kilidi")
serit(330,p1,P_OY+160,"PRO",[("pik saat","54 urun"),("gunluk","360 urun"),
      ("pide / lahmacun","200 / 160"),("robot","%81"),("STORE","%100"),("kazanc","1,8 x")],RED)

ly=H_PX-96
txt(330,ly,"LEJANT",f13,INK)
for i,(c,a) in enumerate([(LINE,"kapak / panel"),(RED,"ACIK agiz — robot girisi"),(GRAY,"cekmece")]):
    xx=330+i*470; d.rectangle([xx,ly+30,xx+32,ly+52],fill=(255,255,255),outline=c,width=3)
    txt(xx+44,ly+41,a,f11,INK,"lm")
txt(W_PX-330,ly+41,"kabin yuksekligi 1970 (plint 120 dahil)  ·  derinlik 840",f11,GRAY,"rm")

os.makedirs(os.path.dirname(OUT),exist_ok=True); im.save(OUT); print("yazildi:",OUT)
