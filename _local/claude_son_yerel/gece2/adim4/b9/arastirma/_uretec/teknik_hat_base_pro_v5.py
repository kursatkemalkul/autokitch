# -*- coding: utf-8 -*-
"""AUTOKITCH - HAT ON GORUNUS v5 (12 Eyl 2026): BASE (ustte) + PRO (altta). Yalniz on gorunus.

v4'ten FARKI (Kemal, 12 Eyl):
  1) CEKMECE ESKI HALINDE: 620 genis, tek GN 2/1 tepsi (v4'teki 1255'lik genis cekmece iptal).
     Ince cekmece = ince yuvarlama: fazla kapasite %0-14 (genis cekmecede %13-20 idi).
  2) KALIN SEPERATOR YOK: ayni sicakliktaki kolonlar arasinda yalnizca 35 mm cerceve
     (iki cekmecenin raylari + dikme). Yalitimli 65'lik bolme YALNIZ -18 | +3 sinirinda.
  3) FAZLA BIR TANE BILE YOK: hamur 3 gun, icecek 7 gun, tam ihtiyac kadar cekmece. Tatli yok.
     Kalan bant BOS birakildi (taranmis).
  4) Derinlik 840.

BASE  33 cekmece · 4 kolon · 2740 mm      PRO  53 cekmece · 6 kolon · 4050 mm
  3,33 kolon gerekiyor -> 4. kolon ucte bir dolu (829 mm bos). Kabin daha dar olamiyor:
  620'lik cekmeceyle 3 kolon = 4388 mm, ihtiyac 4871 mm.

Kural: paftada yalniz on gorunus + olcu + parca adi; aciklama mesajda.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE\HAT_BASE_PRO_v5_on_gorunus.png".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 4300, 3120
S = 0.46
BG, INK, GRAY, LINE = (255,255,255), (26,26,28), (145,145,152), (72,72,78)
FILL, ACC, RED, SOFT = (244,244,246), (0,86,184), (198,42,32), (232,232,237)
BUZ, DOLAP, BOSL = (28,86,166), (14,120,90), (190,190,196)

def F(sz, b=False):
    for n in (("arialbd.ttf","segoeuib.ttf") if b else ("arial.ttf","segoeui.ttf")):
        try: return ImageFont.truetype(n, sz)
        except Exception: pass
    return ImageFont.load_default()
f7, f8, f9, f11, f13, f16, f22, f38 = F(13), F(15), F(17), F(20), F(23), F(27,1), F(35,1), F(52,1)

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
CELL0, CELL1, BIND, FUGA_C = 182.5, 1660.0, 15.0, 3.0
YUZ0 = CELL0 - BIND
XI, WO = 62.5, 620.0                                   # ic duvar · cekmece genisligi (eski, tek tepsi)
HH  = {"donmus":115.0,"hamur":88.0,"lahm":88.0,"icecek":132.0,"1L":300.0}
AD  = {"donmus":"DONMUS PIDE","hamur":"TAZE PIDE","lahm":"LAHMACUN","icecek":"ICECEK","1L":"1 L"}
CAP = {"donmus":20,"hamur":20,"lahm":30,"icecek":63,"1L":42}          # 620'lik cekmece basina
# ihtiyac (3 gun hamur / 7 gun icecek)
IHT_B = {"donmus":140,"hamur":70,"lahm":423,"icecek":315,"1L":77}
IHT_P = {"donmus":228,"hamur":114,"lahm":687,"icecek":518,"1L":126}
# kolonlar: [(adet,tip,zon) | "ayirici"]  · bolme: kolonlar arasi (65 yalitimli / 35 cerceve)
ST_BASE = dict(kolon=[[(7,"donmus","-18"),"ayirici",(3,"lahm","+3")],
                      [(12,"lahm","+3")],
                      [(4,"hamur","+3"),(5,"icecek","+3")],
                      [(2,"1L","+3")]],
               bolme=[65,35,35])
ST_PRO  = dict(kolon=[[(6,"donmus","-18"),"ayirici",(4,"lahm","+3")],
                      [(6,"donmus","-18"),"ayirici",(4,"lahm","+3")],
                      [(12,"lahm","+3")],
                      [(3,"lahm","+3"),(6,"hamur","+3"),(2,"icecek","+3")],
                      [(7,"icecek","+3"),(1,"1L","+3")],
                      [(2,"1L","+3")]],
               bolme=[35,65,35,35,35])
def store_w(st): return 2*XI + WO*len(st["kolon"]) + sum(st["bolme"])

def _zon_serit(cx,ybas,yson,zon):
    if zon is None: return
    col = BUZ if zon=="-18" else DOLAP
    d.rectangle([cx+5, yson, cx+5+7, ybas], fill=col)
    s = "-18 C" if zon=="-18" else "+3 C"
    tw = d.textlength(s, font=f7); ym=(ybas+yson)/2
    d.rectangle([cx+15, ym-10, cx+15+tw+8, ym+10], fill=(255,255,255), outline=col, width=1)
    txt(cx+19, ym, s, f7, col, "lm")

def kabin(ox,oy,w_mm,ad,bant=None,store=None,iht=None,notu=None,vur=False):
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
        cx = x0 + XI*S
        d.rectangle([x0+SV,oy-1968*S,x1-SV,oy-1668*S],fill=SOFT,outline=LINE,width=2)
        txt((x0+x1)/2,oy-1818*S,"SOGUTMA GRUBU  ·  kompresor · kondenser · fan",f8,GRAY,"mm")
        bolme = store["bolme"]; kullanilan = {}
        for ki, gruplar in enumerate(store["kolon"]):
            cw = WO*S; y = YUZ0; onceki=None; zbas=oy-y*S; cv = 8*S
            if ki:
                bw = bolme[ki-1]*S
                d.rectangle([cx-bw,oy-CELL1*S,cx,oy-YUZ0*S],fill=(INK if bolme[ki-1]>=60 else SOFT),outline=LINE,width=1)
            for g in gruplar:
                if g == "ayirici":
                    yb = y + 3.0
                    d.rectangle([cx+cv,oy-(yb+42)*S,cx+cw-cv,oy-yb*S],fill=INK,outline=INK,width=1)
                    _zon_serit(cx,zbas,oy-(yb+42)*S,onceki); zbas = oy-(yb+42)*S
                    y = yb + 42.0 + 3.0; continue
                adet, tip, zon = g; h = HH[tip] + 2*BIND
                ybas = y
                for i in range(adet):
                    col = BUZ if zon=="-18" else DOLAP
                    d.rectangle([cx+cv,oy-(y+h)*S,cx+cw-cv,oy-y*S],fill=(255,255,255),outline=col,width=1)
                    y += h + FUGA_C
                kullanilan[tip] = kullanilan.get(tip,0)+adet
                et = "%s %d" % (AD[tip], adet)
                ym = oy-((ybas+y-FUGA_C)/2)*S; tw = d.textlength(et, font=f7)
                d.rectangle([cx+cw/2-tw/2-6, ym-10, cx+cw/2+tw/2+6, ym+10], fill=(255,255,255), outline=GRAY, width=1)
                txt(cx+cw/2, ym, et, f7, INK, "mm")
                onceki = zon
            _zon_serit(cx,zbas,oy-(y-FUGA_C)*S,onceki)
            bos = CELL1 - (y - FUGA_C)
            if bos > 20:
                by1, by0 = oy-CELL1*S, oy-(y-FUGA_C)*S
                d.rectangle([cx+cv,by1,cx+cw-cv,by0],fill=(250,250,251),outline=BOSL,width=1)
                for k in range(0, int(cw-2*cv), 12):
                    xx = cx+cv+k; L = min(by0-by1, cw-2*cv-k)
                    d.line([(xx,by0),(xx+L,by0-L)],fill=(226,226,232),width=1)
                et = "BOS %d" % round(bos); tw=d.textlength(et,font=f7)
                d.rectangle([cx+cw/2-tw/2-6,(by0+by1)/2-10,cx+cw/2+tw/2+6,(by0+by1)/2+10],fill=(255,255,255),outline=BOSL,width=1)
                txt(cx+cw/2,(by0+by1)/2,et,f7,GRAY,"mm")
            txt(cx+cw/2, oy-1660*S-13, "%%%d" % round(100*(y-FUGA_C-YUZ0)/(CELL1-YUZ0)), f7, GRAY, "md")
            cx += cw + (bolme[ki]*S if ki < len(bolme) else 0)
    txt((x0+x1)/2,y1-48,ad,f13,ACC if vur else INK,"md")
    txt((x0+x1)/2,y1-24,str(int(w_mm)),f11,GRAY,"md")
    if notu: txt((x0+x1)/2,y0+120*S+14,notu,f8,GRAY,"ma")
    return x1

def hat(oy, kabinler, etiket, alt, ray_not):
    x = 300; ilk = x
    for k in kabinler: x = kabin(x, oy, *k[0:1], **k[1])
    son = x
    ry = oy-1970*S-84
    d.line([(ilk-40,ry),(son+40,ry)],fill=LINE,width=7)
    d.ellipse([ilk+100,ry-13,ilk+126,ry+13],fill=ACC)
    if etiket=="PRO": d.ellipse([son-260,ry-13,son-234,ry+13],fill=RED)
    txt(son+52,ry,ray_not,f8,GRAY,"lm")
    olcu(ilk,son,oy+104,"%d mm   ·   %.2f m"%(round((son-ilk)/S),(son-ilk)/S/1000),INK,f13)
    y0_ = oy-1970*S
    d.line([(ilk-62,y0_),(ilk-62,oy)],fill=INK,width=2)
    for yy in (y0_,oy): d.line([(ilk-69,yy),(ilk-55,yy)],fill=INK,width=2)
    txt(ilk-76,(y0_+oy)/2,"1970",f11,INK,"rm")
    txt(ilk-76,y0_-54,etiket,f22,ACC if etiket=="BASE" else RED,"la")
    txt(ilk-76,y0_-22,alt,f11,GRAY,"la")
    return ilk,son

def stok_seridi(x0,x1,y,bas,st,iht,renk,ek):
    """ihtiyac / kapasite cizelgesi — her urun icin"""
    say = {}
    for K in st["kolon"]:
        for g in K:
            if g == "ayirici": continue
            n,t,_ = g; say[t] = say.get(t,0)+n
    d.rectangle([x0,y,x1,y+58],fill=(250,250,252),outline=renk,width=2)
    txt(x0+18,y+29,bas,f16,renk,"lm")
    ogeler = [(AD[t], "%d cek · %d / %d" % (say[t], iht[t], say[t]*CAP[t])) for t in ("donmus","hamur","lahm","icecek","1L")] + ek
    w=(x1-x0-230)/len(ogeler)
    for i,(a,b) in enumerate(ogeler):
        cx=x0+210+i*w
        txt(cx,y+14,a,f7,GRAY,"la"); txt(cx,y+36,b,f11,INK,"la")

# ================= PAFTA =================
txt(300,54,"AUTOKITCH  ·  HAT ON GORUNUS  ·  v5",f38,INK)
txt(300,114,"BASE ve PRO  ·  yalniz on gorunus  ·  olculer mm  ·  derinlik 840  ·  12 Eyl 2026",f13,GRAY)
d.line([(300,152),(W_PX-300,152)],fill=LINE,width=3)

WB, WP = store_w(ST_BASE), store_w(ST_PRO)
B_OY = 1270
b0,b1 = hat(B_OY,[
  (WB,{"ad":"STORE v5","store":ST_BASE,"iht":IHT_B,"notu":"4 kolon x 620 · 33 cekmece · bolme 65 (-18|+3) / 35","vur":True}),
  (700,{"ad":"PRESS v5","bant":PRESS,"notu":"Fersah PZP-400"}),
  (700,{"ad":"TOPPING v4","bant":TOPPING,"notu":"14 yuva · kaset bos 7,54 kg"}),
  (700,{"ad":"OVEN v4","bant":OVEN4,"notu":"3 hazne · ortak havuz"}),
  (700,{"ad":"PACK v3","bant":PACK,"notu":"sarjor 487 kutu"}),
],"BASE","1 ROBOT 20 kg","ROBOT RAYI · 1 kol · 20 kg sinifi")
stok_seridi(300,b1,B_OY+142,"BASE",ST_BASE,IHT_B,ACC,[("pik / gun","32 · 211 urun"),("motor","33")])

P_OY = 2770
p0,p1 = hat(P_OY,[
  (WP,{"ad":"STORE v5-PRO","store":ST_PRO,"iht":IHT_P,"notu":"6 kolon x 620 · 53 cekmece","vur":True}),
  (700,{"ad":"PRESS v5","bant":PRESS,"notu":"ayni"}),
  (700,{"ad":"TOPPING v4","bant":TOPPING,"notu":"ayni · gunde 2 dolum"}),
  (1000,{"ad":"OVEN v4-PRO","bant":OVEN6,"notu":"6 hazne · 4'u yeterli"}),
  (700,{"ad":"PACK v3","bant":PACK,"notu":"ayni"}),
],"PRO","2 ROBOT 20 kg","ROBOT RAYI · 2 kol · bolge kilidi")
stok_seridi(300,p1,P_OY+142,"PRO",ST_PRO,IHT_P,RED,[("pik / gun","52 · 343 urun"),("motor","53")])

ly=H_PX-78
txt(300,ly,"LEJANT",f13,INK)
LEJ=[(LINE,"kapak / panel"),(RED,"ACIK agiz - robot girisi"),(BUZ,"cekmece  -18 C"),(DOLAP,"cekmece  +3 C"),(INK,"yalitim 65 / bant 42"),(BOSL,"BOS band")]
for i,(c,a) in enumerate(LEJ):
    xx=300+i*400; d.rectangle([xx,ly+26,xx+28,ly+44],fill=(255,255,255) if c not in (INK,) else INK,outline=c,width=3)
    txt(xx+38,ly+35,a,f11,INK,"lm")
txt(W_PX-300,ly+35,"kabin 1970 (plint 120 dahil) · derinlik 840 · cekmece 620 · alin 33 (15+3+15) · stok = ihtiyac / kapasite",f9,GRAY,"rm")

os.makedirs(os.path.dirname(OUT),exist_ok=True); im.save(OUT); print("yazildi:", OUT, "· STORE BASE %.0f · PRO %.0f" % (WB, WP))
