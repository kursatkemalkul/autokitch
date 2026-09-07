# -*- coding: utf-8 -*-
# HAT DIŞ GÖRÜNÜŞ v1 (6 Eyl 2026) — kapalı paneller, iç görünmez; robot kolunun girdiği yerler BOŞ (açıklık), eleman kapıları turuncu.
import io, xml.dom.minidom
S=3.3; X0=60; Y0=130
o=[]
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='middle',fw='',col='#111',rot=0):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif"%s>%s</text>' % (x,y,fs,anc,fw or 'normal',col,(' transform="rotate(%s %.1f %.1f)"'%(rot,x,y)) if rot else '',esc(s)))
def hatch(x,y,w,h,step=5,c='#b8b8b8',f='#e4e4e4'):
    rc(x,y,w,h,.6,0,c,None,f); k=0
    while k<w+h:
        ln(x+max(0,k-h),y+min(k,h),x+min(k,w),y+max(0,k-w),.4,c); k+=step
def dim(x1,y1,x2,y2,s,fs=8):
    ln(x1,y1,x2,y2,.8);
    for (x,y) in ((x1,y1),(x2,y2)):
        if abs(y2-y1)<abs(x2-x1): ln(x,y-4,x,y+4,.8)
        else: ln(x-4,y,x+4,y,.8)
    if abs(y2-y1)<abs(x2-x1): tx((x1+x2)/2,y1-5,s,fs,'middle','bold')
    else: tx(x1-6,(y1+y2)/2+3,s,fs,'middle','bold',rot=-90)
M=[('1 · STORE',140),('2 · PRESS',70),('3 · TOPPING',70),('4 · OVEN',70),('5 · PACK',70)]
T=sum(w for _,w in M)
PAN,PANL,OPN,ELE,GLS,DRW='#d8dadd','#cfd2d6','url(#dark)','#e6e8eb','url(#glass)','#e2e4e7'
def Z(z): return Y0+S*(197-z)
def X(x): return X0+S*x
W=int(X0+S*T+60+S*70+60); H=int(Y0+S*197+60)
o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'%(W,H,W,H)); o.append('<defs><linearGradient id="dark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0e0f11"/><stop offset="1" stop-color="#2b2e33"/></linearGradient><linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a5866"/><stop offset="0.5" stop-color="#7f8f9e"/><stop offset="1" stop-color="#3d4954"/></linearGradient><linearGradient id="body" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e9ebee"/><stop offset="1" stop-color="#c9ccd1"/></linearGradient></defs>'); rc(0,0,W,H,0,0,'none',None,'#f4f4f2')
tx(X0,40,'AUTOKITCH — HAT DIŞ GÖRÜNÜŞ v2',13,'start','bold')
ln(X0,72,W-40,72,.8,'#999')
# zemin
ln(X0-30,Z(0),X(T)+S*70+90,Z(0),2); rc(X0-30,Z(0),X(T)+S*70+120-X0,10,0,0,'none',None,'#d0d0cc')
xs=[sum(w for _,w in M[:i]) for i in range(6)]
def panel(x0,x1,z0,z1,kind,lab='',fs=7,col='#333'):
    x,y,w,h=X(x0),Z(z1),S*(x1-x0),S*(z1-z0)
    if kind=='opn':
        rc(x,y,w,h,1.4,1,'#111',None,OPN); rc(x,y,w,5,0,0,'none',None,'#000')
    elif kind=='gls':
        rc(x,y,w,h,1.2,2,'#4b5560',None,GLS); rc(x+8,y+6,w-16,3,0,0,'none',None,'#b9c6d1'); rc(x+w*0.35,y+h-9,w*0.3,4,0,1,'none',None,'#2f3a44')
    elif kind=='drw':
        rc(x,y,w,h,.8,1.5,'#9a9ea3',None,DRW); rc(x+w/2-14,y+h-8,28,3,0,1,'none',None,'#6b7075')
    elif kind=='ele':
        rc(x,y,w,h,1,2,'#9a9ea3',None,ELE); rc(x+w-9,y+h/2-9,3,18,0,1,'none',None,'#6b7075')
    else:
        rc(x,y,w,h,.7,0,'#a5a9ae',None,PAN if kind=='pan' else PANL)
# kabin govdeleri
for i,(ad,w) in enumerate(M):
    x0=xs[i]; rc(X(x0)+1,Z(197),S*w-2,S*185,2,4,'#111',None,'url(#body)')
    if i<2: rc(X(x0)+5,Z(12),4,S*12,1.2); rc(X(x0+w)-9,Z(12),4,S*12,1.2)
    else: rc(X(x0)+1,Z(12),S*w-2,S*12,1,0,'#555',None,'#9e9e9e'); pass
# ---- STORE 0–140 ----
a=xs[0]
panel(a+2,a+138,167,195,'panl','SOĞUTMA ×2 — üstten servis paneli (eleman)',7)
for k in range(4): panel(a+5,a+69,161-(k+1)*13,161-k*13,'drw','içecek %d'%(k+1),6)
panel(a+5,a+69,77,109,'drw','1 L çekmece',6)
for r in range(8): panel(a+71,a+135,161-(r+1)*10.5,161-r*10.5,'drw','taze %d'%(r+1),5.5)
panel(a+2,a+138,69,77,'panl','',6)
panel(a+5,a+69,40,69,'opn','KASET KATI KLAPESİ — robot ÇATAL (4 donmuş kap)',6.5,'#1a49b8')
panel(a+71,a+135,40,69,'panl','boş bant (sabit panel)',6,'#777')
for r in range(2):
    panel(a+5,a+69,20+r*10,30+r*10,'drw','donmuş %d'%(r+1),5.5); panel(a+71,a+135,20+r*10,30+r*10,'drw','donmuş %d'%(r+3),5.5)
# ---- PRESS ----
b=xs[1]
panel(b+3,b+67,134,195,'pan')
panel(b+3,b+33,134,178,'ele')

panel(b+3,b+67,45,134,'pan'); panel(b+10,b+60,72,108,'opn')
panel(b+3,b+67,12,45,'pan')
# ---- TOPPING ----
c=xs[2]
for k,(z0,z1) in enumerate(((156,195),(115,156),(74,115))):
    panel(c+3,c+67,z0,z1,'opn','KAT %d KLAPESİ AÇIK — tepsi düzlemi %d'%(k+1,(158,117,76)[k]),6.5,'#1a49b8')
panel(c+3,c+67,46,74,'ele','ALT klape 1 — gece robot (çatal) · eleman haftalık',6)
panel(c+3,c+67,19,46,'ele','ALT klape 2 — gece robot (çatal) · eleman haftalık',6)
panel(c+3,c+67,12,19,'panl','',6)
# ---- OVEN ----
d=xs[3]
panel(d+3,d+67,168,195,'ele','FAN + FİLTRE servis kapağı (eleman aylık)',6.5)
panel(d+3,d+67,140,168,'gls','FIRIN KAPAK 2 (cam, aşağı açılır, motorlu)',6.5,'#1a49b8')
panel(d+3,d+67,112,140,'gls','FIRIN KAPAK 1 (cam, aşağı açılır, motorlu)',6.5,'#1a49b8')
panel(d+3,d+18,82,112,'ele','YAĞ KABI',5.5)
panel(d+18,d+67,82,112,'opn','SPREY KLAPESİ — tepsi',6.5,'#1a49b8')
panel(d+3,d+67,32,82,'opn','KESME PRESİ KLAPESİ — tepsi zemine',6.5,'#1a49b8')
panel(d+3,d+67,12,32,'ele','PANO servis kapağı',6)
# ---- PACK ----
e=xs[4]
panel(e+3,e+67,104,195,'ele','ŞARJÖR ÖN KAPISI — eleman haftada 1 kutu demeti sürer',6.5)
panel(e+3,e+67,60,104,'opn','KUTULAMA KLAPESİ — tepsi eğilir · pençe kutuyu alır',6.5,'#1a49b8')
panel(e+3,e+67,12,60,'ele','PANO + MEKANİZMA servis kapağı',6)
# ---- SERVICE ----
sv=T+60/S
rc(X(sv),Z(197),S*70,S*185,2,4,'#111',None,PAN); rc(X(sv)+5,Z(12),4,S*12,1.2); rc(X(sv+70)-9,Z(12),4,S*12,1.2)
panel(sv+3,sv+67,140,195,'ele','TEKNİK — UPS · yangın tüpü',6.5)
panel(sv+3,sv+67,68,140,'ele','AMBALAJ (yassı kutu, demet)',6.5)
panel(sv+3,sv+67,12,68,'ele','TEMİZLİK — kilitli',6.5)
# olculer
for i,(ad,w) in enumerate(M): dim(X(xs[i]),Y0-22,X(xs[i+1]),Y0-22,str(w))
dim(X(0),Y0-46,X(T),Y0-46,'TOPLAM %d'%T,9)
dim(X0-34,Z(197),X0-34,Z(0),'197')
tx(W-30,H-10,'AUTOKITCH · arastirma/FULL_MAKINE/hat_dis_kapak_gorunus_v2 · 6 Eyl 2026',7,'end','','#777')
o.append('</svg>'); svg=chr(10).join(o); xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\hat_dis_kapak_gorunus_v2.svg"
io.open(out,'w',encoding='utf-8').write(svg); print('ok',W,H)
