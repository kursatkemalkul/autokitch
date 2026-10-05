# -*- coding: utf-8 -*-
"""E (KUTU KATLAMA) MONTAJ ANİMASYONU v2 (model: hat3_v10h · zincir 00–66) · 5 Eki 2026 · Claude · bulut oturumu
Girdi: e_parca.pkl (e_parca.py), acinim_E (adım 35 E gövde: h3_e_sac_v1) · Çıktı: plan_e.pkl → e_cikti.py
Altyapı: _altyapi.py (TOPPING v6 / F v2 ile aynı: zaman çizelgesi, plan anı yol denetimi, yerleştirici).
Kapsam: kaide + ayaklar, kaynaklı alt montaj (taban + ön kasa + kulaklar), şarjör + asansör, besleyici, kalıp / köprü / kapak / köşe / parmak /
piston mekanizmaları, yan / üst / arka saclar (FHP saplama + içten pul + fiberli somun), E panosu + fiş paneli + kablolar + vakum hattı,
4 ön kapak + menteşe + bas-aç + emniyet, şarjör yan kapısı, robot çöpü. Karton yığını işletmede doldurulur → bu animasyonda yok."""
import sys, os, json, pickle, math, time, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
import sac_morf_t5 as SM
import re as _re
T0 = time.time()
D0 = pickle.load(open('e_parca.pkl', 'rb')); P = D0['P']; ENT = D0['ENT']
for a in [a for a in P if a.startswith('karton_stok')]: del P[a]

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
AD_TR = {'taban_sac_3': 'Taban 3 mm', 'sol_sac_pizza_penceresi': 'Yan sol 1,5 (pizza penceresi)', 'sag_sac': 'Yan sağ 1,5 (şarjör açıklığı)',
         'arka_sac': 'Arka sac 1,5', 'ust_sac': 'Üst sac 1,5', 'govde_kosebent_sag_arka_alt': 'Köşebent sağ arka alt',
         'kaide_e_ray_on': 'Kaide ön ray 60 × 60', 'kaide_e_ray_arka': 'Kaide arka ray 60 × 60', 'onyuz_dikme_sol': 'Ön dikme sol', 'onyuz_dikme_orta': 'Ön dikme orta',
         'onyuz_dikme_sag': 'Ön dikme sağ', 'sarjor_yan_kapisi': 'Şarjör yan kapısı 1,5', 'sarjor_yan_kapisi_ic_tava': 'Şarjör kapısı iç tava',
         'sarjor_yan_kapisi_mentese_lamasi': 'Kapı menteşe laması 3', 'sarjor_yan_kapisi_basac_lamasi': 'Bas-aç laması 3'}
def bk(x): return x.replace('_', ' ')
def tr(a):
    if a in AD_TR: return AD_TR[a]
    m = _re.match(r'onyuz_kapak_E_(alt|ust)_(sol|sag)$', a)
    if m: return 'Kapak %s %s (dış tava 1,5)' % ({'alt': 'alt', 'ust': 'üst'}[m.group(1)], {'sol': 'sol', 'sag': 'sağ'}[m.group(2)])
    return P[a]['ac'].split('·')[0].split(';')[0].strip() if a in P else a
CEVRE = [a for a in P if a.startswith('cevre')]
def kutu(a): return P[a]['V'].min(0), P[a]['V'].max(0)
def merkez(a): l, h = kutu(a); return (l + h) / 2

# ------------------------------------------------------------------ PEM / FHP saplama → sac (üretimde preslenir, sacla gelir) · host.json: baş hangi sacın yüzüyle aynı
PEM_SAC = {}
def pem_bagla(p, s, yan, ad):
    P[p]['sac'] = s; P[p]['yan'] = np.asarray(yan, float); P[p]['pem_ad'] = ad; PEM_SAC.setdefault(s, []).append(p)
HOST = json.load(open('host.json'))
for p, h in HOST.items():
    if p not in P or not h: continue
    s, yan = h
    if s not in P: continue
    pem_bagla(p, s, yan, 'PEM FHP-M6' if 'taban_3' in p or p.startswith('arayuz_mek_taban') else 'PEM FHP-M5')
for p in [a for a in P if a.startswith('govde_pem_m8_ust')]: pem_bagla(p, 'ust_sac', (0, -1.0, 0), 'PEM SP-M8')
print('PEM / saplama', {k: len(v) for k, v in PEM_SAC.items()})
# pul / somun giriş ekseni: saplamanın ucundan başa doğru (baş = yan)
for a in list(P):
    m = _re.match(r'(.+)_(pul|somun)$', a)
    if m and m.group(1) + '_saplama' in P and 'yan' in P[m.group(1) + '_saplama']:
        P[a]['eks'] = P[m.group(1) + '_saplama']['yan'].copy()
for a in [a for a in P if a.startswith(('kaide_e_vida', 'arayuz_uke_m8'))]: P[a]['eks'] = np.array([0, -1.0, 0])
for a in [a for a in P if _re.match(r'ayak_\d+(_kontra)?$', a)]: P[a]['eks'] = np.array([0, 1.0, 0])
for a in [a for a in P if _re.match(r'onyuz_kapak_E_mentese_(sol|sag)_\d_sabit_vida', a)]: P[a]['eks'] = np.array([-1.0 if '_sol_' in a else 1.0, 0, 0])

exec(open(os.path.join(HERE, '_altyapi.py'), encoding='utf-8').read())

# ------------------------------------------------------------------ çevre + beyanlı plan istisnaları
for s_, L_ in PEM_SAC.items():
    for p in L_: HARIC_PLAN.add((p, s_))
def haric(a, b, neden): HARIC_PLAN.add((a, b)); HARIC_NEDEN[(a, b)] = neden
for st_ in [a for a in P if a.startswith(('arayuz_mek', 'arayuz_j3'))]:
    lo_, hi_ = kutu(st_)
    for m_ in [m for m in P if P[m]['tur'] in ('mek',) and np.all(kutu(m)[0] <= hi_ + 1) and np.all(kutu(m)[1] >= lo_ - 1)]:
        haric(st_, m_, 'arayüz saplaması mekanizma kulağındaki deliğe eksen boyunca geçer (model sıfır boşluk)')
KAY = lambda pre: sorted(k for k in P if k.startswith(pre) and P[k]['tur'] == 'kaynak')
def koy(adlar, adaylar, metin, **k):
    global t
    if isinstance(adlar, str): adlar = [adlar]
    return yerlestir(list(adlar), adaylar, t, metin, **k)
def sira_tak(adlar, t0, yol, sure=0.5, ara=0.12, ofs0=None):
    tt = t0
    for i, a in enumerate(adlar): tt = tak(a, t0 + i * ara, sure, yol, ofs0=ofs0)
    return tt
def AD(*yon, lift=(20, 40, 120, 300, 500), yan=(30, -30), son=()):
    """yön(ler)den yaklaş · lift: yukarıdan in · yan: x ofsetle · son: son bacak (saplamaya eksen boyunca oturma)"""
    L_ = []
    for d in yon: L_.append(YOL(d))
    for d in yon:
        for e in son: L_.append(YOL(d, e))
        for h in lift: L_.append(YOL(d, (0, h, 0)))
        for x in yan: L_.append(YOL(d, (x, 0, 0)))
    return L_
ON9, ARKA9, UST6 = (0, 0, 900), (0, 0, -900), (0, 600, 0)
SAG7, SOL7 = (900, 0, 0), (-900, 0, 0)
SON = [(15, 0, 0), (-15, 0, 0), (0, 15, 0), (0, -15, 0), (0, 0, -15), (0, 0, 15), (30, 0, 0), (-30, 0, 0), (0, 30, 0), (0, -30, 0)]
def vidala(adlar, t0, yol=30.0):
    tt = t0
    for i_, a_ in enumerate(adlar):
        for b in [b for b in (a_[:-6] + '_pul',) if a_.endswith('_somun') and b in P]: tt = max(tt, tak(b, t0 + i_ * 0.12, 0.4, yol))
        tt = max(tt, tak(a_, t0 + i_ * 0.12 + 0.3, 0.5, yol))
    return tt
def somunla(rx, t0, yol=25.0):
    return vidala(sorted(a for a in P if _re.match(rx, a) and a.endswith('_somun')), t0, yol)
def var(*adlar): return [a for a in adlar if a in P]
KAM.append([0.0, [6.4, 2.6, 2.4], [4.8, 1.0, -0.4]])
t = 0.4
# ---- 1 KAİDE
adim('Kaide ve ayaklar', 'Kaide: 304 kare boru 60 × 60 × 3 ön / arka ray + 40 × 60 kayıtlar, tezgâhta TIG; raylara DIN 929 kaynak somunları (ayak M12, taban M8). Ayaklar alttan vidalanır, kontra somun.',
     'kaide (2 ray + 3 kayıt + 4 tapa) · ayak × 6 + kontra')
kamera_genel(['kaide_e_ray_on', 'kaide_e_ray_arka'], yon=(0.45, 0.55, 0.75), olcek=1.0)
KAIDE = var('kaide_e_ray_on', 'kaide_e_ray_arka', 'kaide_e_kayit_sol', 'kaide_e_kayit_orta', 'kaide_e_kayit_sag') + sorted(a for a in P if a.startswith(('kaide_e_ray_on_tapa', 'kaide_e_ray_arka_tapa', 'kaide_e_ayak_somunu', 'kaide_e_somun')))
t = koy(KAIDE, AD(UST6, lift=(), yan=()), 'Kaide (kaynaklı çerçeve, tezgâhta) → yere', tezgah_kaynak=KAY('kaide_e_kayit'))
t = sira_tak(sorted(a for a in P if _re.match(r'ayak_\d$', a)), t, 60.0, 0.5, 0.12)
t = sira_tak(sorted(a for a in P if _re.match(r'ayak_\d_kontra$', a)), t, 30.0, 0.4, 0.08); olay(t - 0.4, 'Ayarlı ayak M12 × 6 → ray kaynak somunlarına · kontra somun'); t += 0.2
# ---- 2 ALT MONTAJ
adim('Taban ve ön kasa (kaynaklı alt montaj)', 'Taban 3 mm + ön kasa (sol / orta / sağ dikme, 788 kayıtları, tapalar) + panel kulakları tezgâhta TIG; tabana FHP saplamalar preslenir. Kaidenin üstüne iner: 7 × M8 bombe başlı vida yukarıdan ray kaynak somunlarına.',
     'taban · dikme × 3 · kayıt × 2 · kulak × 18 · vida M8 × 7')
kamera_genel(['taban_sac_3', 'onyuz_dikme_sol', 'onyuz_dikme_sag'], yon=(0.45, 0.5, 0.8), olcek=0.9)
ALT = ['taban_sac_3'] + var('onyuz_dikme_sol', 'onyuz_dikme_orta', 'onyuz_dikme_sag', 'onyuz_kayit_788_sol', 'onyuz_kayit_788_sag') + sorted(a for a in P if a.startswith('onyuz_dikme_') and a.endswith('_tapa')) \
    + sorted(a for a in P if _re.match(r'govde_kulak_(sol|sag)_(on|taban)_\d+$', a))
ALT_K = KAY('onyuz_dikme_') + KAY('onyuz_kayit_788') + KAY('govde_kulak_')
t = koy(ALT, AD(UST6, lift=(), yan=()), 'Taban + ön kasa + kulaklar (tezgâhta TIG) → kaidenin üstüne', pem=sorted(PEM_SAC.get('taban_sac_3', [])), tezgah_kaynak=ALT_K)
t = sira_tak(sorted(a for a in P if a.startswith('kaide_e_vida')), t, 30.0, 0.45, 0.1); olay(t - 0.5, 'Taban ↔ kaide: M8 bombe başlı vida × 7 (ray içindeki kaynak somununa)'); t += 0.2
# ---- 3 ROBOT ÇÖPÜ + ŞARJÖR + ASANSÖR
adim('Robot çöpü, şarjör ve asansör', 'Robot çöpü (kova + poşet + oluk) yukarıdan sol öne; şarjör + asansör (hazır alt montaj: yığın tablası, vida mili, motor, kılavuzlar) yukarıdan tabanın M6 saplamalarına; yan saplamalar yan saclar gelince bağlanır.',
     'robot çöpü · şarjör + asansör')
kamera_genel(['sarjor_asansor'], yon=(0.4, 0.6, 0.7), olcek=0.9)
t = koy('robot_copu', AD(UST6, ON9, lift=(5, 20), son=SON), 'Robot çöpü → yukarıdan sol öne')
t = koy(['sarjor_asansor'], AD(UST6, ARKA9, lift=(), son=SON), 'Şarjör + asansör → yukarıdan, tabanın M6 saplamalarına')
# ---- 4 YAN SOL
adim('Yan sol', 'Yan sol (1,5 · pizza penceresi, preslenmiş FHP saplamalar) tezgâhta fiş paneli J3 ile birlikte soldan: saplamaları ön kasa / taban kulaklarından ve şarjör kulaklarından geçer; içten pul + fiberli somun.',
     'yan sol + fiş paneli J3 · pul + somun M5')
kamera_genel(['sol_sac_pizza_penceresi'], yon=(-0.8, 0.45, 0.45), olcek=0.8)
t = koy(['sol_sac_pizza_penceresi', 'fis_paneli'], AD(SOL7, lift=(0.5, 1, 2), yan=()), 'Yan sol (fiş paneli J3 tezgâhta) → soldan, saplamalar kulaklara', pem=sorted(PEM_SAC.get('sol_sac_pizza_penceresi', [])))
t = somunla(r'govde_kulak_sol_(on|taban)_\d+_bag', t, 20.0); olay(t - 0.6, 'Yan sol ↔ kulaklar: pul + fiberli somun M5 × 12'); t += 0.2
# ---- 5 ÜST
adim('Üst sac', 'Üst sac (1,5 · yan dönüşler, Harting ağzı, U ↔ E için 3 × PEM M8, mekanizma askı saplamaları) sağdan sürülür: sol dönüşü yan sol saplamalarına geçer (sağ ucu dayamada).',
     'üst sac · pul + somun')
kamera_genel(['ust_sac'], yon=(0.5, 0.7, 0.5), olcek=0.8)
t = koy('ust_sac', AD(SAG7, lift=(0.5, 1, 2, 5), yan=()), 'Üst sac → sağdan, sol dönüşü yan saplamalarına', pem=sorted(PEM_SAC.get('ust_sac', [])))
t = somunla(r'govde_(bag_ust_sol|kulak_ust_[a-z]+_bag)', t, 20.0); olay(t - 0.6, 'Üst ↔ yan sol: pul + fiberli somun'); t += 0.2
# ---- 6 KATLAMA MODÜLLERİ (sağ + arka açıkken)
adim('Katlama modülleri', 'İki alt montaj tezgâhta hazırlanır: ALT MODÜL (kalıp + yuva, köprü, kapak katlama mekanizması + kol, uç sensörleri) sağdan sürülür, sol saplamalara oturur; ÜST MODÜL (besleyici şasisi + motor + itici + vakum kolu, köşe kaldırıcılar + tutucular + piston, ön parmaklar, arka itici) arkadan girer, üst sacın askı saplamalarına alttan oturur.',
     'alt modül · üst modül')
kamera_genel(['kalip', 'besleyici_sasi'], yon=(0.8, 0.45, -0.4), olcek=0.9)
ALTM = var('kalip', 'kalip_yuva', 'kopru_govde', 'kopru', 'kapak_mekanizmasi', 'kapak_katlayici', 'elk_sensor')
USTM = var('besleyici_sasi', 'besleyici_motor', 'besleyici_itici', 'besleyici_vakum', 'kose_tutucu', 'kose_kaldirici', 'kose_piston', 'parmak', 'parmak_y', 'piston', 'piston_itici')
t = koy(ALTM, AD(SAG7, ARKA9, lift=(), yan=(), son=SON), 'Alt modül (kalıp + köprü + kapak mekanizması, tezgâhta) → sağdan, sol saplamalara')
t = koy(USTM, AD(ARKA9, SAG7, lift=(), yan=(), son=SON), 'Üst modül (besleyici + köşe + parmak + itici, tezgâhta) → arkadan, üst askı saplamalarına')
# ---- 7 YAN SAĞ
adim('Yan sağ', 'Yan sağ (şarjör kapısı açıklığı, preslenmiş saplamalar; bas-aç laması tezgâhta) sağdan: saplamaları kulaklardan, üst sacın dönüşünden ve mekanizma kulaklarından geçer; köşebent; içten pul + somunlar.',
     'yan sağ + bas-aç laması · köşebent · pul + somun')
kamera_genel(['sag_sac'], yon=(0.85, 0.45, 0.3), olcek=0.8)
t = koy(['sag_sac'] + var('sarjor_yan_kapisi_basac_lamasi', 'sarjor_yan_kapisi_basac'), AD(SAG7, lift=(0.5, 1, 2), yan=()), 'Yan sağ (bas-aç laması tezgâhta) → sağdan', pem=sorted(PEM_SAC.get('sag_sac', [])))
t = somunla(r'govde_(kulak_sag_(on|taban)_\d+_bag|bag_ust_sag|bag_kapi_basac)', t, 20.0); olay(t - 0.6, 'Yan sağ: pul + fiberli somunlar'); t += 0.2
t = koy(var('govde_kosebent_sag_arka_alt'), AD(ARKA9, lift=(0.5, 1), yan=(), son=SON), 'Köşebent → yan sağ saplamasına')
t = somunla(r'govde_bag_kosebent_yan', t, 20.0)
# ---- 8 ARKA + PANO
adim('Arka sac ve E panosu', 'Tezgâhta arka sacın iç yüzüne: E panosu (Beckhoff + Siemens + sürücüler, hazır) ve şarjör kapısı menteşe laması + menteşe gövdeleri. Arka sac (alt + üst dönüş) arkadan sürülür, saplamaları yan dönüşlerden geçer; içten pul + somunlar.',
     'arka sac + pano + menteşe laması · pul + somun')
kamera_genel(['arka_sac'], yon=(0.4, 0.45, -0.85), olcek=0.8)
ARK = ['arka_sac', 'istasyon_kutusu'] + var('sarjor_yan_kapisi_mentese_lamasi', 'sarjor_yan_kapisi_mentese_0', 'sarjor_yan_kapisi_mentese_1')
t = koy(ARK, AD(ARKA9, lift=(0.5, 1, 2), yan=()), 'Arka sac + E panosu + menteşe laması (tezgâhta) → arkadan', pem=sorted(PEM_SAC.get('arka_sac', [])))
t = somunla(r'govde_bag_(arka_(sol|sag)|taban_arka|ust_arka|kosebent_arka|kapi_lamasi)', t, 20.0); olay(t - 0.6, 'Arka ↔ yanlar / taban / üst: pul + fiberli somunlar'); t += 0.2
# ---- 9 ELEKTRİK
adim('Kablolar ve vakum hattı', 'Güç (kırmızı) ve bilgi (mavi) kabloları, vakum hattı kanallar boyunca: pano ↔ fiş paneli ↔ motorlar / sensörler.', 'kablolar · vakum hattı')
kamera_genel(['istasyon_kutusu', 'fis_paneli'], yon=(0.6, 0.5, -0.6), olcek=1.0)
for a in ('kablo_guc', 'kablo_bilgi', 'hava_hatti'): buyu(a, t, 1.0)
olay(t, 'Güç (kırmızı) / bilgi (mavi) kabloları + vakum hattı'); t += 1.2
# ---- 10 ŞARJÖR YAN KAPISI
adim('Şarjör yan kapısı', 'Kapı (dış sac + iç tava, punta) tezgâhta menteşe kanatlarıyla; sağdan menteşe gövdelerine.', 'kapı + menteşe kanatları')
kamera_genel(['sarjor_yan_kapisi'], yon=(0.9, 0.35, 0.2), olcek=1.1)
KPI = var('sarjor_yan_kapisi', 'sarjor_yan_kapisi_ic_tava', 'sarjor_yan_kapisi_mentese_0_kanat', 'sarjor_yan_kapisi_mentese_1_kanat')
t = koy(KPI, AD(SAG7, lift=(0.5, 1), yan=()), 'Şarjör yan kapısı (tezgâhta) → menteşeleriyle sağdan')
# ---- 11 KAPAKLAR
adim('Ön kapaklar', 'Bas-aç mandalları orta dikmeye, menteşe gövdeleri dikmelere (iç yandan 2 × M5), emniyet sensörleri; 4 kapak tezgâhta (dış tava + iç tava punta, köşeler TIG, karşılıklar; sol üstte robot ağzı kasası) menteşeleriyle önden.',
     'bas-aç × 6 · menteşe × 12 · emniyet × 4 · kapak × 4')
kamera_genel(['onyuz_kapak_E_ust_sol', 'onyuz_kapak_E_alt_sag'], yon=(0.35, 0.4, 0.9), olcek=0.9)
for a in sorted(a for a in P if a.startswith('onyuz_kapak_E_basac')):
    haric(a, 'onyuz_dikme_orta', 'bas-aç gövdesi orta dikmenin Ø12,2 deliğine geçme (yaylı tırnak; model sıfır boşluk)')
    koy(a, AD(ON9), 'Bas-aç → orta dikmeye', sure_bekle=0.02)
t = bitti()
for a in sorted(a for a in P if _re.match(r'onyuz_kapak_E_mentese_(sol|sag)_\d_sabit$', a)): koy(a, AD(ON9, lift=(5,), son=SON), 'Menteşe gövdesi → dikmeye', sure_bekle=0.02)
t = bitti()
t = sira_tak(sorted(a for a in P if _re.match(r'onyuz_kapak_E_mentese_(sol|sag)_\d_sabit_vida', a)), t, 20.0, 0.4, 0.05); olay(t - 0.4, 'Menteşe gövdeleri: iç yandan 2 × M5'); t += 0.2
for a in sorted(a for a in P if a.startswith('emniyet_') and not a.endswith('aktuator')): koy(a, AD(ON9, son=SON), '%s → gövdeye' % tr(a), sure_bekle=0.02)
t = bitti()
for k_ in ('alt_sol', 'alt_sag', 'ust_sol', 'ust_sag'):
    y_ = k_.split('_')[1]; u_ = k_.split('_')[0]
    KP = sorted(a for a in P if a.startswith('onyuz_kapak_E_%s' % k_) and P[a]['tur'] != 'kaynak')
    KP = ['onyuz_kapak_E_%s' % k_] + [a for a in KP if a != 'onyuz_kapak_E_%s' % k_]
    KP += sorted(a for a in P if _re.match(r'onyuz_kapak_E_mentese_%s_\d_kanat$' % y_, a) and ((int(a.split('_')[5]) < 3) == (u_ == 'alt')))
    KP += [a for a in P if a == 'emniyet_E_%s_%s_aktuator' % (u_.upper(), y_.upper())]
    t = koy(KP, AD(ON9, lift=(20, 40), yan=()), 'Kapak %s (tezgâhta hazır) → menteşeleriyle önden' % k_.replace('_', ' ').replace('ust', 'üst').replace('sag', 'sağ'), grup_kaynak=KAY('onyuz_kapak_E_%s_kose' % k_))
# ---- 13 HAT
adim('Hat bağlantısı', 'Sahada: K (silik) solda — K ↔ E 3 × M8; U (silik) üstte — U tabanından üst sacın 3 × PEM M8 somununa.', 'K · U (silik)')
t = sira_tak(sorted(a for a in P if a.startswith('arayuz_uke_m8')), t, 30.0, 0.45, 0.1)
for a in ('cevre_B', 'cevre_U', 'cevre_K', 'cevre_diger'):
    if a in P: basla(a, np.zeros(3), t); YER[a] = t; YERINDE.append(a)
olay(t, 'K ve U (silik) yerinde · U ↔ E: M8 × 3'); t += 1.0
kam(t, ([6.6, 2.8, 2.6], [4.8, 1.0, -0.4]))
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
exec(open(os.path.join(HERE, '_son.py'), encoding='utf-8').read().replace("'plan_a3.pkl'", "'plan_e.pkl'").replace('OLC = 1.75', 'OLC = 1.0'))
