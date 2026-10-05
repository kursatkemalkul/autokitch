# -*- coding: utf-8 -*-
"""F MONTAJ ANİMASYONU v2 (model: hat3_v10h · zincir 00–66) · 5 Eki 2026 · Claude · bulut oturumu
Girdi: f_parca.pkl (f_parca.py), acinim_F (adım 36 F üst kabin + adım 38 kapak / atış kanalı) · Çıktı: plan_f.pkl → f_cikti.py
Altyapı: _altyapi.py (TOPPING v6 ile aynı: zaman çizelgesi, plan anı yol denetimi, yerleştirici).
Kapsam: F üst kabin sacları + profiller, TP10 fırın, yükleme bandı, davlumbaz (atış kanalı, fan + filtre, filtre servis ağzı), kompresör + hava hattı +
emniyet valfi, F istasyon kutusu + kanallar + fiş panelleri + kablolar, iki ön kapak (menteşe, gazlı yay, acil stop, emniyet aktüatörü).
Baca (U_F içinden çıkar, flanşı U tavanına) ve pizza kutusu stoğu U montajında / işletmede → bu animasyonda yok."""
import sys, os, json, pickle, math, time, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
import sac_morf_t5 as SM
T0 = time.time()
D0 = pickle.load(open('f_parca.pkl', 'rb')); P = D0['P']; ENT = D0['ENT']
for a in [a for a in P if a.startswith(('baca_', 'arayuz_baca', 'yalitim_baca', 'd_pizza'))]: del P[a]

# ------------------------------------------------------------------ 1. sac parçaları: açınımdan ağ
SAC = {}
for f in sorted(os.listdir(SM.ACN_DIR)):
    ad = f[:-5]
    if ad not in P: continue
    s = SM.Sac(ad); SAC[ad] = s
    old = P[ad]
    V, F = (s.dunya(s.yerel({})), s.F) if s.bukum else (old['V'], old['F'])
    P[ad] = dict(old, V=V, F=F, Vm=old['V'], Fm=old['F'], model_lo=old['V'].min(0), model_hi=old['V'].max(0))
print('sac', len(SAC))
AD_TR = {'f_ust_yan_sol': 'F yan sol 1,5', 'f_ust_yan_sag': 'F yan sağ 1,5', 'f_ust_arka_sac': 'F arka sac 1,5', 'f_ust_tavan_sac': 'F tavan 1,5',
         'f_ust_taban_levhasi': 'F taban levhası 1,5', 'f_ust_taban_yalitim_kilifi_on': 'Taban yalıtım kılıfı ön 0,8', 'f_ust_taban_yalitim_kilifi_arka': 'Taban yalıtım kılıfı arka 0,8',
         'f_davlumbaz_bolme_duvari': 'Davlumbaz bölme duvarı 1,5', 'f_ust_tavan_kirisi': 'Tavan kirişi 30 × 30', 'f_ust_tavan_kirisi_tapa': 'Tavan kirişi tapası',
         'govde_fu_kosebent_sol_arka_ust': 'Köşebent sol arka üst', 'f_ust_alt_profil_on': 'Alt profil ön', 'f_ust_alt_profil_orta': 'Alt profil orta', 'f_ust_alt_profil_arka': 'Alt profil arka',
         'onyuz_f_ust_dikme_0': 'Ön dikme', 'onyuz_f_ust_ust_kayit': 'Ön üst kayıt', 'davlumbaz_atis_kanali_L1': 'Atış kanalı L1 1,5', 'davlumbaz_atis_kanali_L2': 'Atış kanalı L2 1,5',
         'filtre_servis_tapasi': 'Filtre servis tapası 1,5'}
import re as _re
def bk(x): return x.replace('_', ' ')
def tr(a):
    if a in AD_TR: return AD_TR[a]
    return P[a]['ac'].split('·')[0].split(';')[0].strip() if a in P else a
CEVRE = [a for a in P if a.startswith('cevre')]
def kutu(a): return P[a]['V'].min(0), P[a]['V'].max(0)
def merkez(a): l, h = kutu(a); return (l + h) / 2

# ------------------------------------------------------------------ PEM / saplama → sac (üretimde preslenir, sacla gelir)
PEM_SAC = {}
def pem_bagla(p, s, yan, ad):
    P[p]['sac'] = s; P[p]['yan'] = np.asarray(yan, float); P[p]['pem_ad'] = ad; PEM_SAC.setdefault(s, []).append(p)
def yon_disa(p, s):
    """saplamanın uzun ekseni boyunca sacın merkezinden saplamaya doğru (PEM sacın bu yüzüne preslenir)"""
    l, h = kutu(p); e = int(np.argmax(h - l)); ls, hs = P[s]['model_lo'] if 'model_lo' in P[s] else kutu(s)[0], P[s]['model_hi'] if 'model_hi' in P[s] else kutu(s)[1]
    y = np.zeros(3); y[e] = 1.0 if (l[e] + h[e]) / 2 > (ls[e] + hs[e]) / 2 else -1.0
    return y
for a in list(P):
    s = None
    if a.startswith('govde_fu_bag_') and a.endswith('_saplama'):
        k = a.split('_')[3]; y_ = a.split('_')[4]
        if k in ('tavan', 'bolme') and y_ in ('sol', 'sag'): s = 'f_ust_yan_' + y_
        elif k == 'tavan' and y_ == 'arka': s = 'f_ust_tavan_sac'
        elif k == 'arka': s = 'f_ust_arka_sac'
        elif k == 'kosebent': s = 'f_ust_yan_sol' if y_ == 'yan' else 'f_ust_arka_sac'
    elif a.startswith('govde_fu_pem_m8'): s = 'f_ust_tavan_sac'
    elif a.startswith('arayuz_mek_f_ust_taban_levhasi'): s = 'f_ust_taban_levhasi'
    elif a.startswith('arayuz_mek_f_ust_yan_sol') or a.startswith('arayuz_j1_burc'): s = 'f_ust_yan_sol'
    elif a.startswith('arayuz_mek_f_ust_yan_sag') or a.startswith('arayuz_j2_burc'): s = 'f_ust_yan_sag'
    elif _re.match(r'onyuz_kapak_F_(sol|sag)_mentese_\d+_pem', a): s = 'onyuz_kapak_F_%s_dis_tava' % a.split('_')[3]
    if s:
        pem_bagla(a, s, yon_disa(a, s) if 'kapak' not in a else (0, 0, -1.0), 'PEM SP-M8-1' if 'm8' in a else ('PEM SP-M5-2' if 'kapak' in a else 'PEM FHP-M5'))
print('PEM / saplama', {k: len(v) for k, v in PEM_SAC.items()})
# pul / somun / vida / perçin giriş ekseni: saplamanın ekseni boyunca sacın tarafına
for a in list(P):
    m = _re.match(r'(govde_fu_bag_.+)_(pul|somun)$', a)
    if m and m.group(1) + '_saplama' in P:
        sp = m.group(1) + '_saplama'; s = P[sp]['sac']; P[a]['eks'] = -yon_disa(sp, s)
    elif a.startswith('f_ust_kilif_percin'): P[a]['eks'] = np.array([0, 1.0, 0])
    elif _re.match(r'onyuz_kapak_F_(sol|sag)_mentese_\d+_vida', a): P[a]['eks'] = np.array([0, 0, 1.0])

exec(open(os.path.join(HERE, '_altyapi.py'), encoding='utf-8').read())

# ------------------------------------------------------------------ çevre + beyanlı plan istisnaları
for a in ('cevre_B',):
    if a in P: basla(a, np.zeros(3), 0.0); YER[a] = 0.0; YERINDE.append(a)
for s_, L_ in PEM_SAC.items():
    for p in L_: HARIC_PLAN.add((p, s_))
def haric(a, b, neden): HARIC_PLAN.add((a, b)); HARIC_NEDEN[(a, b)] = neden
KAY = lambda pre: sorted(k for k in P if k.startswith(pre) and P[k]['tur'] == 'kaynak')
UST, ON, ARKA, SOL, SAG = YOL((0, 600, 0)), YOL((0, 0, 900)), YOL((0, 0, -900)), YOL((-700, 0, 0)), YOL((700, 0, 0))
def koy(adlar, adaylar, metin, **k):
    global t
    if isinstance(adlar, str): adlar = [adlar]
    return yerlestir(list(adlar), adaylar, t, metin, **k)
def sira_tak(adlar, t0, yol, sure=0.5, ara=0.12, ofs0=None):
    tt = t0
    for i, a in enumerate(adlar): tt = tak(a, t0 + i * ara, sure, yol, ofs0=ofs0)
    return tt
def AD(*yon, lift=(20, 40, 120, 300, 500), yan=(30, -30)):
    L_ = []
    for d in yon: L_.append(YOL(d))
    for d in yon:
        for h in lift: L_.append(YOL(d, (0, h, 0)))
        for x in yan: L_.append(YOL(d, (x, 0, 0)))
    return L_
ON9, ARKA9, UST6 = (0, 0, 900), (0, 0, -900), (0, 600, 0)
def vidala(adlar, t0, yol=30.0):
    tt = t0
    for i_, a_ in enumerate(adlar):
        for b in [b for b in (a_[:-6] + '_pul',) if a_.endswith('_somun') and b in P]: tt = max(tt, tak(b, t0 + i_ * 0.15, 0.4, yol))
        tt = max(tt, tak(a_, t0 + i_ * 0.15 + 0.3, 0.5, yol))
    return tt
def somunla(on, t0, yol=25.0):
    """govde_fu_bag_<on>_*: pul + fiberli somun saplamaya"""
    return vidala(sorted(a for a in P if a.startswith('govde_fu_bag_' + on) and a.endswith('_somun')), t0, yol)

# ================================================================== PLAN
# v2 sıra (zincir 67 sonrası): yan sol → tavan / köşebent / bölme (yan saplamalarına −x) → davlumbaz + kompresör (arkadan) → arka sac (yarıklar tavan saplamalarına)
#   → arka iç elektrik (sağdan) → yan sağ (−x) → somunlar / cıvatalar → alt profil + taban → ön çerçeve → kapaklar
for a_ in ('f_ust_kabin_paslanmaz_3524_1767_-452', 'f_ust_kabin_paslanmaz_3809_1767_-452'):
    if a_ in P: pem_bagla(a_, 'f_davlumbaz_bolme_duvari', (0, 0, -1.0), 'PEM FHP-M5 (filtre çerçevesi)'); HARIC_PLAN.add((a_, 'f_davlumbaz_bolme_duvari'))
for a_ in [a for a in P if a.startswith('f_arka_civata')]: P[a_]['eks'] = np.array([0, 0, 1.0])
for a_ in [a for a in P if _re.match(r'govde_fu_bag_(arka|kosebent_arka)', a) and a.endswith(('_pul', '_somun'))]: P[a_]['eks'] = np.array([0, 0, -1.0])
for a_ in [a for a in P if a.startswith('govde_fu_bag_tavan_arka') and a.endswith(('_pul', '_somun'))]: P[a_]['eks'] = np.array([0, 1.0, 0])
for s_ in ('sol', 'sag'):
    for o_ in [a for a in P if a.startswith('f_ust_kapak_on_seffaf_yay_f_' + s_)] + ['f_ust_kabin_on_seffaf_%s' % ('2501_1597_-8' if s_ == 'sol' else '3987_1597_-8')]:
        for st_ in [a for a in P if a.startswith('arayuz_mek_f_ust_yan_' + s_)]: haric(o_, st_, 'gazlı yay ucu / kapak tamponu yandaki saplamaya eksen boyunca geçer (model sıfır boşluk)')
for a_ in [a for a in P if a.startswith('elk_plastik')]:
    for o_ in ('f_ust_arka_sac', 'f_davlumbaz_bolme_duvari'): haric(a_, o_, 'kablo geçit lastiği sac deliğine geçer (sıkı geçme)')
KAM.append([0.0, [5.2, 2.8, 2.6], [3.25, 1.3, -0.4]])
t = 0.4
# ---- 1 ÇEVRE
adim('B dolabı (silik)', 'F, B dolabının (silik) üstüne kurulur; TOPPING (solda) ve K (sağda) sahada F kurulduktan sonra bağlanır.', 'B (silik)')
olay(t, 'B dolabı yerinde (silik)'); t += 1.0
# ---- 2 FIRIN + YÜKLEME BANDI
adim('TP10 fırın ve yükleme bandı', 'TP10 tünel fırını (hazır ürün) tezgâhta yükleme bandı, bant motoru ve motor kablo kanalıyla birleşik; vinçle B\'nin üstüne iner.',
     'TP10 fırın · yükleme bandı · bant motoru · kablo kanalı')
kamera_genel(['tp10_firin'], yon=(0.4, 0.5, 0.85), olcek=0.9)
FG = ['tp10_firin', 'yukleme_bandi', 'yukleme_bandi_motor'] + [a for a in ('elk_kanal_2765_1106_2',) if a in P]
t = koy(FG, AD(UST6, lift=(300, 500, 800), yan=()), 'TP10 fırın + yükleme bandı (hazır, tezgâhta birleşik) → vinçle B\'nin üstüne')
# ---- 3 YAN SOL + TAVAN + KÖŞEBENT + BÖLME
adim('Yan sol, tavan, bölme duvarı', 'Yan sol (1,5 · 2 büküm, preslenmiş saplamalı) soldan B tavanına; tavan (1,5) sağdan sürülür, dönüşü yan saplamalarına geçer (sağ ucu dayamayla tutulur); köşebent ve davlumbaz bölme duvarı da sağdan yan saplamalarına.',
     'yan sol · tavan · köşebent · bölme duvarı + 2 filtre saplaması · kablo geçit lastiği')
kamera_genel(['f_ust_yan_sol', 'f_ust_tavan_sac'], yon=(0.5, 0.5, 0.75), olcek=0.9)
t = koy('f_ust_yan_sol', AD((-700, 0, 0), UST6, lift=(20, 300, 600), yan=()), 'Yan sol → soldan B tavanına', pem=sorted(PEM_SAC.get('f_ust_yan_sol', [])))
SAGDAN = AD((1700, 0, 0), lift=(0.5, 1, 2, 5), yan=())
TAVG = ['f_ust_tavan_sac'] + sorted(a for a in P if a.startswith('f_ust_kabin_paslanmaz') and merkez(a)[1] > 1800 and merkez(a)[2] < -700)
t = koy(TAVG, SAGDAN, 'Tavan (hortum askıları tezgâhta) → sağdan, dönüşü yan sol saplamalarına (sağ ucu dayamada)', pem=sorted(PEM_SAC.get('f_ust_tavan_sac', [])))
t = koy('govde_fu_kosebent_sol_arka_ust', AD((400, 0, 0), lift=(0.5, 1, 2), yan=()), 'Köşebent → yan sol saplamasına')
t = vidala(['govde_fu_bag_kosebent_yan_somun'], t, 20.0)
BG = ['f_davlumbaz_bolme_duvari'] + [a for a in ('elk_plastik_3578_1780',) if a in P]
t = koy(BG, SAGDAN, 'Bölme duvarı (servis ağzı açık, 2 filtre saplaması preslenmiş) → sağdan yan sol saplamalarına', pem=sorted(PEM_SAC.get('f_davlumbaz_bolme_duvari', [])))
t = vidala(sorted(a for a in P if _re.match(r'govde_fu_bag_(tavan|bolme)_sol_.*_somun$', a)), t, 20.0); olay(t - 0.6, 'Tavan + bölme duvarı ↔ yan sol: pul + fiberli somun M5'); t += 0.2
# ---- 4 DAVLUMBAZ + KOMPRESÖR (arka açıkken)
adim('Davlumbaz ve kompresör', 'Arka sac takılmadan arkadan: atış kanalı (iki L, boyuna TIG, tezgâhta), davlumbaz fanı + yağ filtresi çerçevesi (hazır; çerçeve bölme duvarının saplamalarına), kompresör + tank (hazır) titreşim ayaklarıyla; Festo emniyet valfi.',
     'atış kanalı · fan + filtre · kompresör · emniyet valfi')
kamera_genel(['davlumbaz_fan_filtre', 'kompresor'], yon=(0.4, 0.55, -0.75), olcek=0.9)
t = koy(['davlumbaz_atis_kanali_L1', 'davlumbaz_atis_kanali_L2'], AD(ARKA9, UST6), 'Atış kanalı (iki L, tezgâhta boyuna TIG) → arkadan bölme duvarına', grup_kaynak=KAY('davlumbaz_atis_kanali_boyuna'))
t = koy('davlumbaz_fan_filtre', AD(ARKA9, lift=(20, 40, 120)), 'Davlumbaz fanı + yağ filtresi (hazır) → arkadan, çerçeve bölme duvarının saplamalarına')
t = koy('kompresor', AD(ARKA9, lift=(20, 40, 120)), 'Kompresör + tank (hazır) → arkadan, titreşim ayaklarıyla')
t = koy(['hava_emniyet_valfi_govde', 'hava_emniyet_valfi_bobin', 'hava_emniyet_valfi_susturucu'], AD(ARKA9), 'Festo emniyet valfi + bobin + susturucu → kompresör çıkışına')
# ---- 5 ARKA SAC
adim('Arka sac', 'Arka sac (1,5 · 1 büküm) tezgâhta: 16 panjur lameli TIG, kablo geçit lastikleri. Arkadan sürülür: üst dönüşteki öne açık yarıklar tavan saplamalarına geçer. Yan sol + köşebent: dıştan bombe başlı M5 × 10, içte pul + somun.',
     'arka sac · panjur × 16 · geçit lastiği · cıvata M5 × 10 × 6 + pul + somun')
kamera_genel(['f_ust_arka_sac'], yon=(0.4, 0.45, -0.85), olcek=0.9)
PJ = sorted(a for a in P if a.startswith('f_ust_panjur_lameli') and P[a]['tur'] == 'sac')
PJK = sorted(a for a in P if a.startswith('f_ust_panjur_lameli') and P[a]['tur'] == 'kaynak')
GL = sorted(a for a in P if a.startswith('elk_plastik') and a != 'elk_plastik_3578_1780')
t = koy(['f_ust_arka_sac'] + PJ + GL, AD(ARKA9, lift=(0.5, 1, 2), yan=()), 'Arka sac (panjur TIG + geçit lastikleri tezgâhta) → arkadan, yarıklar tavan saplamalarına', grup_kaynak=PJK)
t = sira_tak(sorted(a for a in P if _re.match(r'f_arka_civata_(arka_sol|kosebent)', a)), t, 25.0, 0.45, 0.1)
t = vidala(sorted(a for a in P if _re.match(r'govde_fu_bag_(arka_sol|kosebent_arka).*_somun$', a)), t, 20.0); olay(t - 0.8, 'Arka ↔ yan sol + köşebent: dıştan cıvata M5 × 10, içte pul + fiberli somun'); t += 0.2
t = vidala(sorted(a for a in P if a.startswith('govde_fu_bag_tavan_arka') and a.endswith('_somun')), t, 15.0); olay(t - 0.6, 'Tavan saplamaları → arka üst dönüşü: alttan pul + fiberli somun'); t += 0.2
# ---- 6 İÇ ELEKTRİK (sağ açıkken)
adim('Arka iç elektrik', 'Yan sağ takılmadan sağdan: F istasyon kutusu (hazır) arka sacın iç yüzüne, kablo kanalları, rakorlar; fiş paneli sol yan sacın burçlarına.',
     'istasyon kutusu · kanallar · rakorlar · fiş paneli sol')
kamera_genel(['istasyon_kutusu'], yon=(0.8, 0.4, -0.4), olcek=0.8)
t = koy('istasyon_kutusu', SAGDAN + AD(UST6), 'F istasyon kutusu (hazır) → arka sacın iç yüzüne')
for a in sorted(a for a in P if a.startswith(('elk_kanal', 'elk_rakor')) and a not in FG and a not in ('elk_kanal_3445_1348', 'elk_rakor_3449_1334')):
    koy(a, SAGDAN + AD(UST6, ON9), '%s → yerine' % tr(a), sure_bekle=0.03)
t = bitti()
t = koy('fis_paneli_sol', SAGDAN + AD(UST6), 'Fiş paneli sol → yan sol burçlarına')
# ---- 7 YAN SAĞ
adim('Yan sağ', 'Yan sağ (preslenmiş saplamalı, fiş paneli sağ tezgâhta) sağdan sürülür: saplamaları tavan ve bölme duvarı dönüşlerinden geçer; arka sacla dıştan cıvata; içten pul + somunlar.',
     'yan sağ + fiş paneli sağ · pul + somun · cıvata M5 × 10 × 5')
kamera_genel(['f_ust_yan_sag'], yon=(0.8, 0.45, 0.4), olcek=0.9)
t = koy(['f_ust_yan_sag', 'fis_paneli_sag'], AD((700, 0, 0), lift=(0.5, 1, 2), yan=()), 'Yan sağ (fiş paneli tezgâhta) → sağdan', pem=sorted(PEM_SAC.get('f_ust_yan_sag', [])))
t = vidala(sorted(a for a in P if _re.match(r'govde_fu_bag_(tavan|bolme)_sag_.*_somun$', a)), t, 20.0)
t = sira_tak(sorted(a for a in P if a.startswith('f_arka_civata_arka_sag')), t, 25.0, 0.45, 0.1)
t = vidala(sorted(a for a in P if a.startswith('govde_fu_bag_arka_sag') and a.endswith('_somun')), t, 20.0); olay(t - 0.8, 'Yan sağ: pul + somunlar · arka ile dıştan cıvata M5 × 10'); t += 0.2
# ---- 8 ALT PROFİLLER + TABAN
adim('Alt profiller ve taban', 'Fırının üstünde: arka alt profil yanlara TIG; arka yalıtım + kılıf; orta profil; ön yalıtım + kılıf; ön profil; kılıflar profillere kör perçinle; taban levhası (delik kaynağı) ve rakor kovanı.',
     'alt profil × 3 · yalıtım × 2 + kılıf × 2 · kör perçin × 16 · taban levhası · rakor kovanı')
kamera_genel(['f_ust_taban_levhasi'], yon=(0.4, 0.6, 0.75), olcek=0.9)
ONUST = AD(ON9, lift=(20, 300, 450), yan=())
t = koy('f_ust_alt_profil_arka', ONUST, 'Arka alt profil → yanlara (TIG)', grup_kaynak=KAY('f_ust_alt_profil_arka_yan_kaynagi'))
t = koy(['f_ust_taban_yalitimi_arka', 'f_ust_taban_yalitim_kilifi_arka'], AD(ON9, lift=(5, 10, 20), yan=()), 'Arka taş yünü + kılıf → profilin altına')
t = koy('f_ust_alt_profil_orta', ONUST, 'Orta alt profil → yanlara (TIG)', grup_kaynak=KAY('f_ust_alt_profil_orta_yan_kaynagi'))
t = koy(['f_ust_taban_yalitimi_on', 'f_ust_taban_yalitim_kilifi_on'], AD(ON9, lift=(5, 10, 20), yan=()), 'Ön taş yünü + kılıf → profillerin altına')
t = koy('f_ust_alt_profil_on', ONUST, 'Ön alt profil → yanlara (TIG)', grup_kaynak=KAY('f_ust_alt_profil_on_yan_kaynagi'))
t = sira_tak(sorted(a for a in P if a.startswith('f_ust_kilif_percin')), t, 20.0, 0.35, 0.06); olay(t - 0.5, 'Kılıflar → profiller: kör perçin Ø3,2 × 16'); t += 0.2
t = koy('f_ust_taban_levhasi', ONUST, 'Taban levhası → profillerin üstüne (delik kaynağı, kırmızı)', pem=sorted(PEM_SAC.get('f_ust_taban_levhasi', [])), grup_kaynak=KAY('f_ust_taban_levhasi_delik'))
t = koy(['f_ust_taban_rakor_kovani'] + [a for a in ('elk_kanal_3445_1348', 'elk_rakor_3449_1334') if a in P], AD(ON9, UST6), 'Rakor kovanı + kanal → taban deliğine')
# ---- 9 ÖN ÇERÇEVE
adim('Ön çerçeve', 'Ön üst kayıt (bas-aç yuvalarıyla) ve ön dikme TIG; tavan kirişi + tapa; filtre rayları bölme duvarına; servis ağzına tapa + 2 çeyrek tur kilit.',
     'üst kayıt · dikme · tavan kirişi · filtre rayı × 4 · servis tapası')
kamera_genel(['onyuz_f_ust_ust_kayit'], yon=(0.4, 0.5, 0.85), olcek=0.9)
t = koy(['onyuz_f_ust_ust_kayit'] + sorted(a for a in P if a.startswith('f_ust_kabin_paslanmaz') and merkez(a)[2] > 30), AD(ON9, lift=(0.5, 1, 2), yan=()), 'Ön üst kayıt (bas-aç tezgâhta) → yanlara (TIG)', grup_kaynak=KAY('onyuz_f_ust_ust_kayit_yan'))
t = koy('onyuz_f_ust_dikme_0', AD(ON9, lift=(0.5, 1), yan=()), 'Ön dikme → taban + üst kayıt (TIG)', grup_kaynak=KAY('onyuz_f_ust_dikme_0_'))
t = koy(['f_ust_tavan_kirisi', 'f_ust_tavan_kirisi_tapa'], AD(ON9, lift=(-0.5, -1, -2), yan=()), 'Tavan kirişi + tapa → üst kayıt + arka (TIG)', grup_kaynak=KAY('f_ust_tavan_kirisi_kaynagi'))
t = koy(sorted(a for a in P if a.startswith('filtre_ray')), AD(ON9), 'Filtre rayları (3 mm) → bölme duvarına (punta)')
t = koy(['filtre_servis_tapasi'] + sorted(a for a in P if a.startswith(('filtre_servis_kilidi', 'filtre_servis_kami'))), AD(ON9, lift=(0.5, 1)), 'Servis tapası + 2 çeyrek tur kilit → ağıza')
buyu('hava_hatti', t, 1.0); olay(t, 'Hava hattı: hortum + askılar (kompresör → istasyonlar)')
for a in ('kablo_guc', 'kablo_bilgi'): buyu(a, t, 1.0)
olay(t, 'Güç (kırmızı) ve bilgi (mavi) kabloları kanallar boyunca'); t += 1.2
# ---- 10 KAPAKLAR
adim('Ön kapaklar', 'Kapaklar tezgâhta: dış tava (1,5 · 4 büküm, köşeler TIG), omegalar, kayıtlar, menteşe somunları, gazlı yaylar; sağ kapakta acil stop. Emniyet sensörleri ve kapak tamponları gövdeye; kapak menteşeleriyle önden gelir, menteşe vidaları.',
     'kapak × 2 · menteşe × 4 · gazlı yay × 2 · acil stop · emniyet sensörü × 2')
kamera_genel(['onyuz_kapak_F_sol_dis_tava', 'onyuz_kapak_F_sag_dis_tava'], yon=(0.35, 0.4, 0.9), olcek=0.9)
for a in [a for a in P if (a.startswith('emniyet_F_') and not a.endswith('aktuator')) or a.startswith('f_ust_kabin_on_seffaf')]: koy(a, AD(ON9), '%s → gövdeye' % tr(a), sure_bekle=0.02)
t = bitti()
for y_ in ('sol', 'sag'):
    KP = sorted(a for a in P if (a.startswith('onyuz_kapak_F_%s_' % y_) and not _re.search(r'_vida_\d+$', a)) or a.startswith('f_ust_kapak_on_seffaf_yay_f_' + y_) or a == 'emniyet_F_%s_aktuator' % y_.upper()
                or (y_ == 'sag' and a.startswith('acil_stop_F')))
    MN = sorted(a for a in P if a.startswith('f_ust_kapak_celik') and ((merkez(a)[0] < 3250) == (y_ == 'sol')))
    t = koy(KP + MN, AD(ON9, lift=(20, 40), yan=()), 'Kapak %s (tezgâhta hazır%s) → menteşeleriyle önden' % (y_, ', acil stop' if y_ == 'sag' else ''),
            pem=sorted(PEM_SAC.get('onyuz_kapak_F_%s_dis_tava' % y_, [])), grup_kaynak=KAY('onyuz_kapak_F_%s_dis_tava_kose' % y_))
    t = sira_tak(sorted(a for a in P if _re.match(r'onyuz_kapak_F_%s_mentese_\d+_vida' % y_, a)), t, 20.0, 0.4, 0.1); t += 0.2
olay(t - 0.4, 'Menteşe vidaları M5 × 6 → kapaktaki preslenmiş somunlara')
# ---- 11 HAT
adim('Hat bağlantısı', 'Sahada: TOPPING (silik) solda — F sol yanına 4 × M8 (TOPPING sayfası); K (silik) sağda; U (silik) F tavanındaki 4 × M8 somuna, baca U ile gelir (U sayfası).', 'TOPPING · K · U (silik)')
for a in ('cevre_TOPPING', 'cevre_K', 'cevre_U', 'cevre_diger'):
    if a in P: basla(a, np.zeros(3), t); YER[a] = t; YERINDE.append(a)
olay(t, 'TOPPING, K ve U (silik) yerinde'); t += 1.0
kam(t, ([5.6, 3.0, 2.9], [3.25, 1.4, -0.4]))
TOPLAM = round(bitti() + 2.0, 3)
SADE = [(r'PEM SP-M(\d)(-\d)?', r'preslenmiş somun M\1'), (r'PEM FHS-M(\d)(-\d)?', r'preslenmiş saplama M\1'), (r'PEM FHP-M(\d)(-\d+)?', r'preslenmiş saplama M\1'),
        (r'PEM S-M(\d)(-\d)?', r'preslenmiş somun M\1'), (r'\bPEM\b', 'preslenmiş'), (r'ISO 4762 ', 'cıvata '), (r'ISO 7380(-1)? ', 'bombe başlı vida '), (r'TEK ÜRÜN', 'hazır ürün')]
def sade(x):
    for a_, b_ in SADE: x = _re.sub(a_, b_, x)
    return x
for x in ADIM: x['ad'] = sade(x['ad']); x['metin'] = sade(x['metin']); x['liste'] = sade(x['liste'])
OLAY = [[o[0], sade(o[1])] for o in OLAY]
for x in ACN: x['ac'] = sade(x['ac'])
for a in P: P[a]['ac'] = sade(P[a]['ac'])
KAPGRUP = []
exec(open(os.path.join(HERE, '_son.py'), encoding='utf-8').read().replace("'plan_a3.pkl'", "'plan_f.pkl'").replace('OLC = 1.75', 'OLC = 1.0'))
