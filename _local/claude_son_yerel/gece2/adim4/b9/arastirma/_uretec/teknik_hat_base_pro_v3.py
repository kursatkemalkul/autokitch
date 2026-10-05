# -*- coding: utf-8 -*-
"""AUTOKITCH - HAT ON GORUNUS v3 (12 Eyl 2026): BASE (ustte) + PRO (altta). Tek pafta, yalniz on gorunus.

v2'den FARKI - STORE DUZELTILDI:
  v2'de cekmeceler arasindaki zorunlu ALIN 33 (bindirme 15 + fuga 3 + bindirme 15) hesaba
  katilmamisti; kolon kapasitesi %30 fazla sanildi. Dogrusu: n cekmece = SUM(h) + 33*(n-1).
  Kolon basina aciklik bandi 182,5..1645 = 1462,5 mm.
  3 gunluk stok 3,50 kolon tutuyor -> BASE STORE 2100/3 kolon DEGIL, 2800/4 kolon.
  BASE hat 4900 -> 5600 mm · PRO hat 6600 -> 7300 mm.

  Ayrica LAHMACUN TEPSISI eklendi: GN 2/1'e 5x6 = 30 cukur O98 (110 g top O75).
  Pide tepsisi ayni tepsiye 20 top aliyor. Bu %50 fark BASE'de bir, PRO'da iki kolon kazandiriyor.

Olculer modelden: STORE v4 · PRESS v5 · TOPPING v4 · OVEN v4 · PACK v3.
Kural: paftada yalniz on gorunus + olcu + parca adi; aciklama mesajda.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_BASE_PRO_v3_on_gorunus.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 4900, 3500
S = 0.50                          # mm -> px
BG, INK, GRAY, LINE = (255,255,255), (26,26,28), (145,145,152), (72,72,78)
FILL, ACC, RED, SOFT = (244,244,246), (0,86,184), (198,42,32), (232,232,237)
BUZ, DOLAP = (28,86,166), (14,120,90)

def F(sz, b=False):
    for n in (("arialbd.ttf","segoeuib.ttf") if b else ("arial.ttf","segoeui.ttf")):
        try: return ImageFont.truetype(n, sz)
        except Exception: pass
    return ImageFont.load_default()
f8, f9, f11, f13, f16, f22, f38 = F(14), F(16), F(19), F(22), F(26,1), F(34,1), F(52,1)

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

# ---------------- STORE ----------------
# cekmece ON YUZU = aciklik + 2x15 bindirme · iki on yuz arasi 3 fuga -> ADIM = h + 33
CELL0, BIND, FUGA_C, ALIN = 182.5, 15.0, 3.0, 33.0
YUZ0 = CELL0 - BIND            # 167,5 en alttaki on yuzun alt kenari
HH = {"donmus":115.0, "hamur":88.0, "lahm":88.0, "icecek":132.0, "1L":300.0}
AD = {"donmus":"DONMUS PIDE", "hamur":"TAZE PIDE", "lahm":"LAHMACUN", "icecek":"ICECEK", "1L":"1 L"}
# kolon: (genislik, [(adet, tip, bolge) ...])   "ayirici" -> -18|+3 yalitim bandi 42
ST_BASE=[(700,[(7,"donmus","-18"),"ayirici",(3,"lahm","+3")]),
         (700,[(4,"hamur","+3"),(8,"lahm","+3")]),
         (700,[(8,"lahm","+3"),(3,"icecek","+3")]),
         (700,[(5,"icecek","+3"),(2,"1L","+3")])]
ST_PRO =[(700,[(10,"donmus","-18")]),
         (700,[(2,"donmus","-18"),"ayirici",(9,"lahm","+3")]),
         (700,[(6,"hamur","+3"),(6,"lahm","+3")]),
         (700,[(8,"lahm","+3"),(3,"icecek","+3")]),
         (700,[(9,"icecek","+3")]),
         (700,[(3,"1L","+3"),(2,"icecek","+3")])]

def _zon_serit(cx,cw,ybas,yson,zon):
    if zon is None: return
    col = BUZ if zon=="-18" else DOLAP
    d.rectangle([cx+6, yson, cx+6+8, ybas], fill=col)
    s = "-18 C" if zon=="-18" else "+3 C"
    tw = d.textlength(s, font=f8); ym=(ybas+yson)/2
    d.rectangle([cx+18, ym-11, cx+18+tw+8, ym+11], fill=(255,255,255), outline=col, width=1)
    txt(cx+22, ym, s, f8, col, "lm")

def kabin(ox,oy,w_mm,ad,bant=None,store=None,notu=None,vur=False):
    x0,x1 = ox, ox+w_mm*S
    y0,y1 = oy, oy-1970*S
    d.rectangle([x0,y1,x1,y0],fill=FILL,outline=LINE,width=3)
    d.rectangle([x0,y0-120*S,x1,y0],fill=SOFT,outline=LINE,width=2)
    SV=30*S
    if bant:
        for (b0,b1,tip,et) in bant:
            by1,by0 = oy-b1*S, oy-b0*S
            col,fl = (RED,(253,252,252)) if tip=="a" else (LINE,(255,255,255))
            d.rectangle([x0+SV,by1,x1-SV,by0],fill=fl,outline=col,width=3 if tip=="a" else 2)
            if et and (b1-b0)>120: txt((x0+x1)/2,(by0+by1)/2,et,f8,INK,"mm")
    if store:
        cx = x0
        d.rectangle([x0+SV,oy-1968*S,x1-SV,oy-1668*S],fill=SOFT,outline=LINE,width=2)
        txt((x0+x1)/2,oy-1818*S,"SOGUTMA GRUBU  ·  kompresor · kondenser · fan",f8,GRAY,"mm")
        for (kw,gruplar) in store:
            cw = kw*S; y = YUZ0; onceki=None; zbas=oy-y*S
            d.line([(cx+cw,y1),(cx+cw,y0)],fill=LINE,width=2)
            for g in gruplar:
                if g == "ayirici":
                    yb = y + 3.0
                    d.rectangle([cx+SV,oy-(yb+42)*S,cx+cw-SV,oy-yb*S],fill=INK,outline=INK,width=1)
                    _zon_serit(cx,cw,zbas,oy-(yb+42)*S,onceki); zbas = oy-(yb+42)*S
                    y = yb + 42.0 + 3.0
                    continue
                adet, tip, zon = g; h = HH[tip] + 2*BIND
                ybas = y
                for i in range(adet):
                    col = BUZ if zon=="-18" else DOLAP
                    d.rectangle([cx+SV,oy-(y+h)*S,cx+cw-SV,oy-y*S],fill=(255,255,255),outline=col,width=1)
                    y += h + FUGA_C
                et = "%s  %d" % (AD[tip], adet)
                ym = oy-((ybas+y-FUGA_C)/2)*S; tw = d.textlength(et, font=f8)
                d.rectangle([cx+cw/2-tw/2-7, ym-11, cx+cw/2+tw/2+7, ym+11], fill=(255,255,255), outline=GRAY, width=1)
                txt(cx+cw/2, ym, et, f8, INK, "mm")
                onceki = zon
            _zon_serit(cx,cw,zbas,oy-(y-FUGA_C)*S,onceki)
            txt(cx+cw/2, oy-1660*S-14, "%%%d dolu" % round(100*(y-FUGA_C-YUZ0)/(1660.0-YUZ0)), f8, GRAY, "md")
            cx += cw
    txt((x0+x1)/2,y1-50,ad,f13,ACC if vur else INK,"md")
    txt((x0+x1)/2,y1-26,str(w_mm),f11,GRAY,"md")
    if notu: txt((x0+x1)/2,y0+120*S+14,notu,f8,GRAY,"ma")
    return x1

def hat(oy, kabinler, etiket, alt, ray_not):
    x = 300; ilk = x
    for k in kabinler: x = kabin(x, oy, *k[0:1], **k[1])
    son = x
    ry = oy-1970*S-88
    d.line([(ilk-40,ry),(son+40,ry)],fill=LINE,width=7)
    d.ellipse([ilk+110,ry-14,ilk+138,ry+14],fill=ACC)
    if etiket=="PRO": d.ellipse([son-280,ry-14,son-252,ry+14],fill=RED)
    txt(son+56,ry,ray_not,f8,GRAY,"lm")
    olcu(ilk,son,oy+110,"%d mm   ·   %.2f m"%(round((son-ilk)/S),(son-ilk)/S/1000),INK,f13)
    y0_ = oy-1970*S
    d.line([(ilk-66,y0_),(ilk-66,oy)],fill=INK,width=2)
    for yy in (y0_,oy): d.line([(ilk-73,yy),(ilk-59,yy)],fill=INK,width=2)
    txt(ilk-80,(y0_+oy)/2,"1970",f11,INK,"rm")
    txt(ilk-80,y0_-56,etiket,f22,ACC if etiket=="BASE" else RED,"la")
    txt(ilk-80,y0_-22,alt,f11,GRAY,"la")
    return ilk,son

def serit(x0,x1,y,bas,ogeler,renk):
    d.rectangle([x0,y,x1,y+62],fill=(250,250,252),outline=renk,width=2)
    txt(x0+20,y+31,bas,f16,renk,"lm")
    w=(x1-x0-240)/len(ogeler)
    for i,(a,b) in enumerate(ogeler):
        cx=x0+220+i*w
        txt(cx,y+15,a,f8,GRAY,"la"); txt(cx,y+38,b,f13,INK,"la")

# ================= PAFTA =================
txt(300,58,"AUTOKITCH  ·  HAT ON GORUNUS  ·  v3",f38,INK)
txt(300,120,"BASE ve PRO  ·  yalniz on gorunus  ·  olculer mm  ·  12 Eyl 2026",f13,GRAY)
d.line([(300,160),(W_PX-300,160)],fill=LINE,width=3)

B_OY = 1360
b0,b1 = hat(B_OY,[
  (2800,{"ad":"STORE v4","store":ST_BASE,"notu":"4 kapi · 40 cekmece · K1 bolmeli (-18/+3)","vur":True}),
  (700,{"ad":"PRESS v5","bant":PRESS,"notu":"Fersah PZP-400"}),
  (700,{"ad":"TOPPING v4","bant":TOPPING,"notu":"14 yuva · kaset bos 7,54 kg"}),
  (700,{"ad":"OVEN v4","bant":OVEN4,"notu":"3 hazne · ortak havuz"}),
  (700,{"ad":"PACK v3","bant":PACK,"notu":"sarjor 487 kutu"}),
],"BASE","1 ROBOT 20 kg","ROBOT RAYI · 1 kol · 20 kg sinifi (FR20)")
serit(300,b1,B_OY+150,"BASE",[("pik saat","32 urun"),("gunluk","211 urun"),
      ("pide / lahmacun","70 / 141"),("stok","pide 3,1 g · lahm 4,0 g"),("robot","%82"),("firin","%54")],ACC)

P_OY = 2960
p0,p1 = hat(P_OY,[
  (4200,{"ad":"STORE v4-PRO","store":ST_PRO,"notu":"6 kapi · 58 cekmece · K1 tam -18","vur":True}),
  (700,{"ad":"PRESS v5","bant":PRESS,"notu":"ayni"}),
  (700,{"ad":"TOPPING v4","bant":TOPPING,"notu":"ayni · gunde 2 dolum"}),
  (1000,{"ad":"OVEN v4-PRO","bant":OVEN6,"notu":"6 hazne · 4'u yeterli"}),
  (700,{"ad":"PACK v3","bant":PACK,"notu":"ayni"}),
],"PRO","2 ROBOT 20 kg","ROBOT RAYI · 2 kol · bolge kilidi")
serit(300,p1,P_OY+150,"PRO",[("pik saat","52 urun"),("gunluk","343 urun"),
      ("pide / lahmacun","114 / 229"),("stok","3 gun"),("robot","%83"),("kazanc","1,63 x")],RED)

ly=H_PX-90
txt(300,ly,"LEJANT",f13,INK)
LEJ=[(LINE,"kapak / panel"),(RED,"ACIK agiz - robot girisi"),(BUZ,"cekmece on yuzu  -18 C"),(DOLAP,"cekmece on yuzu  +3 C")]
for i,(c,a) in enumerate(LEJ):
    xx=300+i*500; d.rectangle([xx,ly+28,xx+30,ly+48],fill=(255,255,255),outline=c,width=3)
    txt(xx+40,ly+38,a,f11,INK,"lm")
txt(W_PX-300,ly+38,"kabin 1970 yuksek (plint 120 dahil) · derinlik 840 · cekmece alini 33 (15+3+15)",f11,GRAY,"rm")

os.makedirs(os.path.dirname(OUT),exist_ok=True); im.save(OUT); print("yazildi:", OUT)
