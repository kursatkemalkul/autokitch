# -*- coding: utf-8 -*-
# HAT v50 = v49 + OVEN v5: tek standart yag kabi (sol), sag slot bos, 12 L = 30 gun, tek pompa
import io
SRC=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim49.py"
DST=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim50.py"
s=io.open(SRC,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt, ('%d != %d: '%(s.count(a),cnt))+a[:80]
    s=s.replace(a,b)
rep('hat_on_gorunus_teknik_v49.svg','hat_on_gorunus_teknik_v50.svg')
rep('(6 Eyl 2026, HAT v49)','(6 Eyl 2026, HAT v50)')
rep('HAT v49 · TÜM İSTASYONLAR','HAT v50 · TÜM İSTASYONLAR')
rep('OVEN v4 (Omake 2 kat · 2 STANDART YAĞ KABI + sprey ortada · KESME PRESİ · kolon 70)','OVEN v5 (Omake 2 kat · 1 STANDART YAĞ KABI + sprey ortada · KESME PRESİ · kolon 70)')
rep('"""HAT v49 (v48 + OVEN v4:','"""HAT v50 (v49 + OVEN v5: tek yag kabi sol, sag slot bos, 12 L = 30 gun, tek pompa) — v49 (v48 + OVEN v4:')
rep("PANO 20 · PLC · menteşe ×2 + pres sürücüsü · 2 SSR · 2 pompa rölesi · 24 V","PANO 20 · PLC · menteşe ×2 + pres sürücüsü · 2 SSR · pompa rölesi · 24 V")
rep("for x0_ in (35, 525):\n    rc(d0+px(x0_),Zh(108)","rc(d0+px(525),Zh(108),px(140),px(240),.8,1,'#999','4,3','none'); tx(d0+px(595),Zh(96)+2,'boş 15',4.4,'middle','','#999')\nfor x0_ in (35,):\n    rc(d0+px(x0_),Zh(108)")
rep("'10 L · 25 gün'","'12 L · 30 gün'")
rep("'YAĞ + SPREY 30 · slot 15 | tepsi 34 | slot 15 · klape 4 · sıcak dolap 42 °C'","'YAĞ + SPREY 30 · kap 15 | tepsi 34 | boş 15 · klape 4 · sıcak dolap 42 °C'")
rep("for x0_ in (35,525):\n    rc(d0+px(x0_),YT2+px(40)","for x0_ in (35,):\n    rc(d0+px(x0_),YT2+px(40)")
rep("alt zon: 2 yağ kabı 68 (slot 15) + kuru bağlantı + pompalar arkada, tepsi Ø32 ortada (34)","alt zon: 1 yağ kabı 68 (sol slot 15, sağ boş) + kuru bağlantı + pompa arkada, tepsi Ø32 ortada (34)")
rep("⑩ ✓ OVEN v4 sadeyağ: 2 STANDART KAP","⑩ ✓ OVEN v5 sadeyağ: 1 STANDART KAP")
rep("sağ/sol slot 15, 10 L = 25 gün (max 12 L = 30), dolu 12,3 kg — ELEMAN ayda 1 değiştirir, ROBOT DOKUNMAZ · 2 mini pompa 24 V arka duvarda, BEYİN biri boşalınca diğerine geçer","sol slot 15 (sağ 15 boş), 12 L = 30 gün, dolu 14,1 kg — ELEMAN ayda 1 değiştirir (kapanışta, dolapta sabaha erir), ROBOT DOKUNMAZ · 1 mini pompa 24 V arka duvarda, şamandıra 4 gün kala 'yağ az'")
rep("genişlik 15 + 34 + 15 = 64 ✓","genişlik kap 15 + tepsi 34 + boş 15 = 64 ✓")
io.open(DST,'w',encoding='utf-8').write(s); print('teknik_cizim50.py yazildi')
