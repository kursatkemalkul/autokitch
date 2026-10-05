# -*- coding: utf-8 -*-
"""TOPPING MONTAJ ANİMASYONU v5 (model: hat3_v9w · zincir 00–55 · yeni 7 ürün yerleşimi) · 5 Eki 2026 · yerel
Girdi: t5_parca.pkl (t5_parca.py), acinim_TOPPING (adım 53 delikleri eklenmiş) · Çıktı: plan_t5.pkl → t5_cikti.py (denetim + GLB/JSON)
Altyapı: _altyapi.py (zaman çizelgesi, plan anı yol denetimi, yerleştirici) · plan: plan_TOPPING.md"""
import sys, os, json, pickle, math, time, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
import sac_morf_t5 as SM
T0 = time.time()
D0 = pickle.load(open('t5_parca.pkl', 'rb')); P = D0['P']; ENT = D0['ENT']

# ------------------------------------------------------------------ 1. sac parçaları: açınımdan ağ (bükümlü olanlar; düz parçalar model ağıyla kalır)
SAC = {}
for f in sorted(os.listdir(SM.ACN_DIR)):
    ad = f[:-5]; s = SM.Sac(ad); SAC[ad] = s
    old = P[ad]
    V, F = (s.dunya(s.yerel({})), s.F) if (s.bukum and not ad.startswith('evaporator_ayagi')) else (old['V'], old['F'])   # 5 Eki: evaporatör ayakları kasete kaynaklı hazır gelir → model ağı (adım 56: ayak 1 27 mm)
    P[ad] = dict(old, V=V, F=F, Vm=old['V'], Fm=old['F'], model_lo=old['V'].min(0), model_hi=old['V'].max(0))   # 5 Eki: Vm/Fm = model ağı (yol denetimi gerçek geometriyle; açınım ağı yalnız gösterim)
print('sac', len(SAC))
AD_TR = {'dis_yan_sol': 'Dış yan sol 1,5', 'dis_yan_sag': 'Dış yan sağ 1,5', 'dis_tavan': 'Dış tavan 1,5', 'dis_taban': 'Dış taban 1,5', 'dis_arka_servis': 'Arka servis sacı 1,5',
         'soguk_alt_sac': 'Soğuk oda alt sacı 1,5', 'soguk_arka_dis_sac': 'Soğuk oda arka dış sacı 1,5', 'astar_arka': 'İç sac arka 1,0', 'astar_sol': 'İç sac sol 1,0', 'astar_sag': 'İç sac sağ 1,0',
         'astar_tavan': 'İç sac tavan 1,0', 'raf': 'Raf 3,0', 'ust_raf': 'Üst raf 3,0', 'soguk_esik': 'Eşik 1,2', 'on_cerceve_430': 'Ön çerçeve 430 1,0', 'kuru_bolme_tabani': 'Kuru bölme tabanı 1,5',
         'teknik_on_perde': 'Teknik ön perde 1,5', 'teknik_sag_perde': 'Teknik sağ perde 1,5', 'ayirma_perdesi_cep_sol': 'Ayırma perdesi 1,5', 'sogutma_cebi': 'Soğutma cebi 1,5',
         'kaide_ust_plaka_4': 'Kaide plakası 4 mm', 'kaide_on_perde_menfezli': 'Menfezli ön perde C 2,0', 'kaide_enine_lama_6': 'Kaide enine lama 6', 'dil_kanali_kasar': 'Dil kanalı kaşar 1,0',
         'dil_kanali_sucuk': 'Dil kanalı sucuk 1,0', 'raf_kosebendi_sol': 'Raf köşebendi sol 3,0', 'raf_kosebendi_sag': 'Raf köşebendi sağ 3,0', 'ust_raf_kosebendi_sol': 'Üst raf köşebendi sol 3,0',
         'ust_raf_kosebendi_sag': 'Üst raf köşebendi sağ 3,0', 'kaide_cep_tasiyici_0': 'Cep taşıyıcı L (arka)', 'kaide_cep_tasiyici_1': 'Cep taşıyıcı L (ön)', 'kanal_gecis_kapagi': 'Kanal geçiş kapağı 1,5',
         'evaporator_ayagi_0': 'Evaporatör ayağı 2,5', 'evaporator_ayagi_1': 'Evaporatör ayağı 2,5', 'evaporator_ayagi_2': 'Evaporatör ayağı 2,5', 'evaporator_ayagi_3': 'Evaporatör ayağı 2,5',
         'kaide_arka_boru': 'Kaide arka boru 100 × 40', 'kaide_sol_boru': 'Kaide sol boru 40 × 100', 'kaide_sag_boru': 'Kaide sağ boru 40 × 100', 'kaide_enine_boru': 'Kaide enine boru 40 × 100',
         'kaide_boyuna_boru_1': 'Boyuna boru 1', 'kaide_boyuna_boru_2': 'Boyuna boru 2', 'kaide_boyuna_boru_3': 'Boyuna boru 3'}
import re as _re
def bk(x): return x.replace('_', ' ')
def tr(a):
    if a in AD_TR: return AD_TR[a]
    m = _re.match(r'evap_kanal_kovani_(\d)_L(\d)', a)
    if m: return 'Evaporatör kanal kovanı %s · L%s 1,0' % (int(m.group(1)) + 1, m.group(2))
    m = _re.match(r'dusme_kovani_(\w+)_L(\d)', a)
    if m: return 'Düşme kovanı %s · L%s 3,0' % ({'kiyma': 'tavuk', 'kusbasi': 'kuşbaşı'}.get(m.group(1), m.group(1)), m.group(2))
    return P[a]['ac'].split('·')[0].strip() if a in P else a
CEVRE = [a for a in P if a.startswith('cevre')]
def kutu(a): return P[a]['V'].min(0), P[a]['V'].max(0)
def merkez(a): l, h = kutu(a); return (l + h) / 2

# ------------------------------------------------------------------ PEM / saplama → sac (üretimde preslenir, sacla gelir)
PEM_SAC = {}
def pem_bagla(p, s, yan, ad):
    P[p]['sac'] = s; P[p]['yan'] = np.asarray(yan, float); P[p]['pem_ad'] = ad; PEM_SAC.setdefault(s, []).append(p)
for a in list(P):
    if a.startswith('kaide_plaka_pem_M6'): pem_bagla(a, 'kaide_ust_plaka_4', (0, -1.0, 0), 'PEM SP-M6-2')
    elif a.startswith('servis_arka_') and ('_burc' in a):
        s = {'yan_sol': 'dis_yan_sol', 'yan_sag': 'dis_yan_sag', 'tavan': 'dis_tavan', 'taban': 'dis_taban'}['_'.join(a.split('_')[2:4]) if a.split('_')[2] == 'yan' else a.split('_')[2]]
        pem_bagla(a, s, (0, 0, 1.0), 'TIG punta' if '_punta_' in a else 'kaynak burcu M5')
    elif (a.startswith(('evaporator_ayak_', 'kanal_kapagi_')) and a.endswith('_pem')): pem_bagla(a, 'kuru_bolme_tabani', (0, -1.0, 0), 'PEM SP-M5-1')
    elif a == 'elk_rakor_1689_1099': pem_bagla(a, 'kuru_bolme_tabani', (0, -1.0, 0), 'kablo rakoru (tezgâhta takılır)')
    elif a.startswith('pem_M8_A') and not a.endswith('kapagi'): pem_bagla(a, 'dis_yan_sol', (1.0, 0, 0), 'PEM SP-M8-1')
    elif a.startswith('pem_M8_F'): pem_bagla(a, 'dis_yan_sag', (-1.0, 0, 0), 'PEM SP-M8-1')
    elif a.startswith('cep_takoz_pem'): pem_bagla(a, 'sogutma_cebi', (0, -1.0, 0), 'PEM SP-M8-1')
    elif a.startswith('mentese_sol_') and a.endswith('_saplama'): pem_bagla(a, 'dis_yan_sol', (1.0, 0, 0), 'PEM FHS-M4 (menteşe)')       # v6 adım 64
    elif a.startswith('mentese_sag_') and a.endswith('_saplama'): pem_bagla(a, 'dis_yan_sag', (-1.0, 0, 0), 'PEM FHS-M4 (menteşe)')
    elif a.startswith('x_sensor_braket_') and a.endswith('_saplama'): pem_bagla(a, 'soguk_alt_sac', (0, -1.0, 0), 'PEM FHS-M3 (sensör braketi)')
    elif a.startswith(('arayuz_mek_', 'arayuz_j1_')):
        k = a.split('_')[2]
        s = {'yan': 'dis_yan_sag', 'taban': 'dis_taban', 'arka': 'dis_arka_servis', 'soguk': 'soguk_arka_dis_sac', 'raf': 'raf', 'alt': 'soguk_alt_sac', 'kuru': 'kuru_bolme_tabani', 'burc': 'dis_yan_sag'}[k]
        l, h = kutu(a); e = int(np.argmax(h - l)); ls, hs = kutu(s); cs = (ls[e] + hs[e]) / 2
        yan = np.zeros(3); yan[e] = -1.0 if abs(l[e] - cs) < abs(h[e] - cs) else 1.0
        pem_bagla(a, s, yan, 'PEM FHP-M5-25' if '_j1_' in a else 'PEM FHP-M5-12')
        P[a]['eks_sap'] = -yan
print('PEM / saplama', {k: len(v) for k, v in PEM_SAC.items()})
for a in list(P):
    if a.startswith('arayuz_kb_'): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.startswith('arayuz_kaide_M6'): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.startswith('arayuz_m8_F'): P[a]['eks'] = np.array([-1.0, 0, 0])
    elif a.startswith('servis_arka') and a.endswith('_vida'): P[a]['eks'] = np.array([0, 0, 1.0])
    elif a.startswith(('evaporator_ayak_', 'kanal_kapagi_')) and a.endswith('_vida'): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.startswith('astar_percin_tavan'): P[a]['eks'] = np.array([0, 1.0, 0])
    elif a.startswith('astar_percin_'): P[a]['eks'] = np.array([0, 0, -1.0])
    elif a.startswith('percin_somun'): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.endswith('kopuk_kapagi'): P[a]['eks'] = np.array([-1.0, 0, 0])

# ------------------------------------------------------------------ 2. animasyonda üretilen punta / TIG işaretleri (modelde dikiş yok · 0,1 mm · beyanlı)
def punta(ad, p, eks, ac):
    V, F = G.mesh(G.silindir(p, eks, 2.0, 0.1, 16)); P[ad] = dict(V=V, F=F, m='kaynak', tur='kaynak', ac=ac, uretilen=True)
PUNTA = collections.OrderedDict()
def punta_dizi(anah, noktalar, eks, ac):
    L_ = []
    for i, p in enumerate(noktalar):
        ad = 'punta_%s_%d' % (anah, i); punta(ad, p, eks, ac); L_.append(ad)
    PUNTA[anah] = L_
Vt = P['dis_taban']['V']
xl = Vt[(Vt[:, 0] < 1445) & (Vt[:, 1] > 900)][:, 0].max(); xr = Vt[(Vt[:, 0] > 2490) & (Vt[:, 1] > 900)][:, 0].min()
punta_dizi('yan_sol_taban', [(xl, 902.0, z) for z in (-780.0, -600.0)], (1, 0, 0), 'TIG: dış taban yan dönüşü ↔ dış yan sol')
punta_dizi('yan_sag_taban', [(xr - 0.1, 902.0, z) for z in (-780.0, -600.0)], (1, 0, 0), 'TIG: dış taban yan dönüşü ↔ dış yan sağ')
punta_dizi('tavan_yanlar', [(x, 2200.0, z) for x in (1440.0, 2496.0) for z in (-700.0, -300.0, 20.0)], (0, 1, 0), 'TIG: dış tavan ↔ yan saclar (üst köşe)')
print('üretilen işaret', sum(len(v) for v in PUNTA.values()))

exec(open(os.path.join(HERE, '_altyapi.py'), encoding='utf-8').read())

# ------------------------------------------------------------------ çevre + beyanlı plan istisnaları (hepsi denetim.md'de gerekçeli)
for a in CEVRE:
    if a == 'cevre_B': basla(a, np.zeros(3), 0.0); YER[a] = 0.0; YERINDE.append(a)
for s_, L_ in PEM_SAC.items():
    for p in L_: HARIC_PLAN.add((p, s_))
def haric(a, b, neden): HARIC_PLAN.add((a, b)); HARIC_NEDEN[(a, b)] = neden
for v_ in [a for a in P if a.startswith('servis_arka') and (a.endswith('_vida') or a.endswith('_burc'))]:
    for s_ in ('dis_yan_sol', 'dis_yan_sag', 'dis_tavan', 'dis_taban', 'dis_arka_servis'): haric(v_, s_, 'çökertme (dimple): servis sacı + dönüş birlikte preslenir, vida başı / burç dimple konisine oturur')
for y_ in ('sol', 'sag'):
    for z_ in (910, 947): haric('mentese_%s_893' % y_, 'mentese_%s_%d_saplama' % (y_, z_), 'menteşe gövdesinin deliği saplamaya eksen boyunca geçer (model sıfır boşluk)')
for m_ in ('kasar', 'sucuk'):
    for y_ in ('sol', 'sag'): haric('motor_%s_%s_dolgu' % (m_, y_), 'motor_' + m_, 'dolgu motor gövdesinin yan yüzüne yüzey teması, arkadan kayarak girer (model sıfır boşluk)')
haric('pem_M8_A_1300_300_kopuk_kapagi', 'pem_M8_A_1300_300', 'köpük kapağı somunun üstüne geçer'); haric('pem_M8_A_2000_300_kopuk_kapagi', 'pem_M8_A_2000_300', 'köpük kapağı somunun üstüne geçer')
for b_ in [a for a in P if a.startswith('burc_')]:
    for w_ in ('soguk_arka_dis_sac', 'pu_levha_arka', 'astar_arka', 'yapistirici_arka', 'evaporator_R'): haric(b_, w_, 'POM burç / burç kılıfı duvar deliğine sıkı geçme (delik Ø = burç Ø; çokgen farkı ≤ 0,4 mm)')
for ad_ in ('kasar', 'sucuk'):
    haric('motor_' + ad_, 'burc_motor_' + ad_, 'kaplin burcun içinden geçer (yuva = kaplin, sıfır boşluk)')
    haric('motor_' + ad_, 'kaset_' + ad_, 'kaplin kasetin kaplinine geçer (geçme)')
UNO = ('tavuk', 'kusbasi', 'patates', 'harc', 'kiyma')
for ad_ in UNO:
    for b_ in ('burc_uno_' + ad_, 'uno_%s_on' % ad_): haric('uno_%s_arka' % ad_, b_, 'piston mili burçtan geçer, ucu pistona vidalanır (sıfır boşluk)')
haric('uno_kiyma_arka', 'burc_kilifi_kiyma', 'piston mili burç kılıfının içinden geçer (sıfır boşluk)')
for k_ in ('sol', 'sag', 'arka', 'tavan'): haric('pu_levha_' + k_, 'yapistirici_' + k_, 'levha yapıştırıcı katmanına bastırılır (yüzey teması)')
for pu_ in ('pu_levha_sol', 'pu_levha_sag', 'pu_levha_arka', 'yapistirici_arka', 'yapistirici_sol', 'yapistirici_sag', 'pu_levha_tavan', 'yapistirici_tavan'):
    haric(pu_, 'dis_tavan', 'levha üst yüzü dış tavanın alt yüzüne sıfır boşlukla temas (yüzey boyunca kayma)')
# iç sac bükümlü kenarları ↔ PU levha yuvaları: üreteç yuvayı flanş ölçüsünde açar (boşluk 0) — flanş yuvaya sürtünerek girer (PU esner) · ölçülen kayma ≤ 2,4 mm (arka / kendi levhası), tavan levhası ↔ yan üst flanş: tavan iç sacı ile levha arasına sıfır boşluklu kızak
PU_YUVA = 'iç sac bükümlü kenarı PU levhadaki yuvasına sıfır boşlukla sürülür (üreteç yuvayı flanş ölçüsünde açar; PU esner)'
for a_ in ('astar_sol', 'astar_sag', 'astar_tavan', 'astar_arka'):
    for p_ in ('pu_levha_arka', 'pu_levha_sol', 'pu_levha_sag', 'pu_levha_tavan'): haric(a_, p_, PU_YUVA)
for a_ in ('astar_sol', 'astar_sag'): haric(a_, 'astar_tavan', 'yan iç sacın üst kenarı tavan iç sacının üstüne sıfır boşlukla sürülür (perçinle bağlanır)')
for kv_ in [a for a in P if a.startswith('dusme_kovani')]:
    for o_ in ['pu_raf_esik', 'raf', 'soguk_alt_sac'] + ['uno_%s_on' % u_ for u_ in UNO]: haric(o_, kv_, 'düşme kovanı deliğe / yuvaya sıfır boşlukla geçer (model teması)')
for o_ in ('raf_kosebendi_sol', 'raf_kosebendi_sag'): haric(o_, 'pu_raf_esik', 'köşebent PU raf levhasının kenar yuvasına sıfır boşlukla iner (PU esner)')
for o_ in ('astar_sol', 'astar_sag', 'astar_arka'): haric('raf', o_, 'raf kenarı iç sac yüzüne sıfır boşlukla kayar (yüzey teması, derz silikonu sonra)')
for o_ in ('ust_raf_kosebendi_sol', 'ust_raf_kosebendi_sag', 'astar_sol', 'astar_sag'): haric('ust_raf', o_, 'üst raf köşebentlerin üstünde sıfır boşlukla kayar (yüzey teması)')
for ad_ in ('kasar', 'sucuk'):
    for o_ in [a for a in P if a.startswith(('dil_kesik_kose_silikonu', 'esik_on_yiv', 'raf_esik_yiv'))]: haric('kaset_' + ad_, o_, 'kaset dili eşik kesiğinden sıfır boşlukla geçer (köşe silikonu / yiv dolgusu teması)')
    for o_ in ('kaset_%s_mandal' % ad_, 'kaset_%s_conta' % ad_, 'dil_kanali_' + ad_, 'kaset_ray_' + ad_): haric('kaset_' + ad_, o_, 'yaylı kilit mandalı / kovan contası / dil kanalı / ray: kaset dili sürülürken sıfır boşluk teması')
haric('x_ekseni', 'x_motor', 'ray tabanı ucu motor braketinin yuvasına geçer (bağlantı, tezgâhta)')
haric('kanal_gecis_kapagi', 'kondenser_kanali', 'kapak yarığı boruya 0,5 mm boşlukla sürülür')
for r_ in [a for a in P if a.startswith('astar_percin_') and not a.endswith('_pul')]:
    for o_ in [a for a in P if a.startswith(('astar_', 'pu_levha', 'on_cerceve'))]:
        if o_ != r_: haric(r_, o_, 'kör perçin: gövdesi deliğe girer, arka ucu çekilince şişer (yuva levhada açık)')
for s_ in ('dis_yan_sol', 'dis_yan_sag', 'dis_tavan', 'dis_taban'): haric('dis_arka_servis', s_, 'çökertme (dimple): servis sacının konisi dönüşün konisine iç içe oturur (son 1,5 mm)')
for st_ in [a for a in P if a.startswith('arayuz_mek_arka')]: haric('servis_cihaz', st_, 'saplama cihaz braketinin deliğinden geçer (somun sonra)')
haric('kanat_K1', 'kanat_K2', 'K1 iç yüzü (z 39) K2 orta kaydının ön yüzüne (z 39) kapanır: son anda sıfır boşluk temas (manyetik fitil yüzü)')
haric('dis_tavan', 'dis_yan_sag', 'tavan kenarı (x 2498,5) yan sacın iç yüzüne sıfır boşlukla temas, yüzey boyunca iner (yan sacın büyük üçgenleri kutu taramasında yanlış çakışma verir)')
haric('on_cerceve_430', 'dis_tavan', 'çerçeve üst kenarı dış tavanın altına sıfır boşlukla kayar (yüzey teması)')
for u_ in ('patates', 'harc', 'kiyma'):
    for o_ in ('uno_%s_raf_conta' % u_, 'ust_raf'): haric('uno_%s_on' % u_, o_, 'UNO çıkış borusu üst raf deliğindeki contanın içinden iner (conta sıfır boşluk)')
    haric('uno_%s_cikis' % u_, 'uno_%s_conta' % u_, 'çıkış borusu kovan contasının içinden geçer (sıfır boşluk)')
    haric('uno_%s_cikis' % u_, 'uno_%s_hortum' % u_, 'hortum ucu boruya geçer'); haric('uno_%s_kelepce' % u_, 'uno_%s_cikis' % u_, 'kelepçe boru ağzına geçer'); haric('uno_%s_kelepce' % u_, 'uno_%s_hortum' % u_, 'kelepçe hortum ucuna geçer')
    haric('uno_%s_raf_flans' % u_, 'uno_%s_hortum' % u_, 'hortum flanşın içinden geçer')
for o_ in ('uno_kiyma_raf_conta', 'ust_raf'): haric('uno_kiyma_dirsek', o_, 'dirseğin dik bacağı üst raf deliğindeki contanın içinden iner (conta sıfır boşluk)')
for o_ in ('uno_kiyma_hortum', 'uno_kiyma_raf_flans'): haric('uno_kiyma_dirsek', o_, 'hortum dirsek ucuna geçer')
haric('burc_kilifi_kiyma', 'uno_kiyma_arka', 'silindir kılıfın içinden geçer')
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
UNO_TR = {'tavuk': 'tavuk', 'kusbasi': 'kuşbaşı', 'patates': 'patates', 'harc': 'lahmacun harcı', 'kiyma': 'kıyma'}
# v6 (zincir 62–64): yeni bağlantı elemanlarının giriş yönü (baştan uca) · pul + vida aynı eksende
def _eks(a):
    if a.startswith(('uno_', 'motor_')) and ('_sol_' in a): return (1.0, 0, 0)
    if a.startswith(('uno_', 'motor_')) and ('_sag_' in a): return (-1.0, 0, 0)
    if a.startswith('valf_adasi_'): return (0, 0, -1.0)
    if a.startswith('emniyet_') and a.endswith('_vida'): return (0, 0, -1.0)
    if a.startswith('x_ekseni_pabuc_arka'): return (0, 0, 1.0)
    if a.startswith('x_ekseni_pabuc_on'): return (0, 0, -1.0)
    if a.startswith('mentese_sol_'): return (-1.0, 0, 0)
    if a.startswith('mentese_sag_'): return (1.0, 0, 0)
    if a.startswith('x_sensor_braket_') and a.endswith('_saplama'): return (0, -1.0, 0)
    if a.startswith('mentese_') and a.endswith('_saplama'): return (1.0 if '_sol_' in a else -1.0, 0, 0)
    return None
for a_ in [a for a in P if P[a]['tur'] == 'baglanti' and a.endswith(('_vida', '_pul', '_somun', '_saplama', '_vida_pul'))]:
    e_ = _eks(a_)
    if e_ is not None: P[a_]['eks'] = e_
def vidala(adlar, t0, yol=30.0):
    """pul önce, sonra vida / somun (her biri kendi ekseninde)"""
    tt = t0
    for i_, a_ in enumerate(adlar):
        pul_ = [b for b in (a_ + '_pul', a_[:-5] + '_pul') if b in P][:1]          # pul adı: <vida>_pul (adım 64) ya da <pabuç>_pul (adım 63)
        for b in pul_: tt = max(tt, tak(b, t0 + i_ * 0.2, 0.4, yol))
        tt = max(tt, tak(a_, t0 + i_ * 0.2 + 0.3, 0.6, yol))
    return tt
def pabuc_kaynak(adlar, t0, yol, metin):
    tt = t0
    for a_ in adlar:
        k_ = [c for c in (a_ + '_kaynak', a_.replace('_braket', '') + '_kaynak') if c in P][:1]
        assert k_, ('kaynak yok', a_)
        tt = max(tt, koy(a_, [YOL(yol)], metin, grup_kaynak=k_, sure_bekle=0.05))
    return tt

# ================================================================== PLAN (plan_TOPPING.md)
KAM.append([0.0, [3.4, 2.6, 2.4], [1.97, 1.2, -0.4]])
t = 0.4
# ---- 1 B TAVANI HAZIRLIĞI
adim('B tavanı: karşı dişler', 'TOPPING, B dolabının (silik) tavanına kurulur. B üst kirişinin deliklerinde 4 kapalı uçlu M8 perçin somun B montajında takılmıştır (B dış tavanı üstlerini kapatır); TOPPING cıvataları bunlara girecek.',
     'M8 kapalı perçin somun × 4 → B üst kirişi')
PS = sorted(a for a in P if a.startswith('percin_somun'))   # 5 Eki: B montajında takılı (Ø11 gövde B dış tavanının Ø9 deliğinden geçemez) → baştan yerinde
yakin(merkez(PS[0]) + np.array([0, 40, 0]), 0.4, tt=t)
for a in PS: basla(a, np.zeros(3), 0.0); YER[a] = 0.0; YERINDE.append(a); ISTISNA.add(a); vurgu([a], t, t + 1.4)
olay(t, 'B kirişindeki 4 kapalı uçlu M8 perçin somun (B montajında takıldı) → TOPPING cıvatalarının karşı dişi'); t += 1.4
# ---- 2 KAİDE ÇERÇEVESİ
adim('Kaide çerçevesi', 'Kaide 304 dikdörtgen borudan (kesim boyunda): arka boru 100 × 40, sol / sağ / enine boru 40 × 100, aralarına 3 boyuna boru ve 6 mm enine lama. Uçlar karşı boruya TIG köşe dikişiyle kaynaklanır (kırmızı, kalıcı).',
     'arka boru · sol / sağ / enine boru · boyuna boru × 3 · enine lama 6 · TIG köşe dikişi × 14')
kamera_genel(['kaide_arka_boru', 'kaide_sol_boru', 'kaide_sag_boru'], yon=(0.45, 0.75, 0.75), olcek=0.7)
t = koy('kaide_arka_boru', [UST], 'Kaide arka boru (100 × 40 × 2, kesim boyu 1064) → B tavanı üstüne', sure_bekle=0.1)
for a in ('kaide_sol_boru', 'kaide_sag_boru', 'kaide_enine_boru'):
    koy(a, [UST], '%s ↔ arka boru: TIG köşe dikişi' % tr(a), grup_kaynak=KAY(a + '_kaynak_arka'), sure_bekle=0.05)
t = bitti() + 0.2
yakin(merkez('kaide_sol_boru_kaynak_arka_0'), 0.35, yon=(0.5, 0.75, 0.45), tt=t - 0.6)
koy('kaide_enine_lama_6', [UST], 'Enine lama 6 mm → arka boru ile ön perde arasına · arka boruya TIG (kırmızı)', grup_kaynak=KAY('kaide_enine_lama_6_kaynak_arka'))
for a in ('kaide_boyuna_boru_1', 'kaide_boyuna_boru_2', 'kaide_boyuna_boru_3'):
    koy(a, [UST], '%s ↔ yan / enine boru: TIG köşe dikişi' % tr(a), grup_kaynak=KAY(a + '_kaynak'), sure_bekle=0.05)
t = bitti() + 0.5
# ---- 3 KAİDE PLAKASI + PERDE + CEP TAŞIYICI
adim('Kaide: cep taşıyıcı, ön perde, plaka', 'İki cep taşıyıcı L (3 mm, lazer → 1 büküm) borulara oturur; menfezli ön perde C (2 mm, lazer → 2 büküm) önden boruların uçlarına; 4 mm kaide plakası lazerde kesilir, altından 2 somun preslenir, borulara iner ve 17 delik kaynağıyla bağlanır. Kondenser emiş filtresi kaide gözüne arkadan.',
     'cep taşıyıcı L × 2 · menfezli ön perde C · kaide plakası 4 mm · preslenmiş somun M6 × 2 · delik kaynağı × 17 · emiş filtresi')
kamera_genel(['kaide_cep_tasiyici_0', 'kaide_cep_tasiyici_1'], yon=(0.4, 0.8, 0.6), olcek=0.9)
for a in ('kaide_cep_tasiyici_0', 'kaide_cep_tasiyici_1'): t = koy(a, [UST], '%s → enine lama ile enine boru arasına, iki ucu TIG (kırmızı)' % tr(a), grup_kaynak=KAY(a + '_kaynak'))
kamera_genel(['kaide_on_perde_menfezli'], yon=(0.3, 0.45, 0.9), olcek=0.9)
t = koy('kaide_on_perde_menfezli', [ON, UST], 'Menfezli ön perde C → boruların ön uçlarına (punta) · enine lama ön perdeye TIG (kırmızı)', grup_kaynak=KAY('kaide_enine_lama_6_kaynak_on'))
kamera_genel(['kaide_ust_plaka_4'], yon=(0.4, 0.8, 0.7), olcek=0.8)
t = koy('kaide_arka_emis_filtresi', [UST, ARKA], 'Kondenser emiş filtresi → kaide gözüne yukarıdan, arka boruya klips (plaka kapanmadan)')
t = koy('kaide_ust_plaka_4', [YOL((0, 420, 0))], 'Kaide plakası → borular (somunlar altta)', pem=sorted(PEM_SAC['kaide_ust_plaka_4']))
yakin(merkez('kaide_ust_plaka_delik_kaynagi_0'), 0.42, yon=(0.35, 0.85, 0.4), tt=t - 0.2)
for k in KAY('kaide_ust_plaka_delik_kaynagi'): buyu(k, t, 0.6)
olay(t, 'Delik kaynağı × 17: plaka yarıkları ↔ kaide boruları (TIG, yüz taşlanır)'); t += 1.0
# ---- 4 TOPPING → B
adim('TOPPING → B bağlantısı', '4 cıvata M8 × 25 + küçük pul M8 (Ø15) kaide plakası ve boru üst duvarındaki Ø16 servis deliğinden boru içine iner; baş boru alt duvarına oturur, cıvata B dış tavanından (Ø9) ve GFRP pedden geçip kirişteki perçin somuna girer.',
     'cıvata M8 × 25 × 4 · küçük pul M8 × 4 → B kirişi M8 perçin somun')
KBp = sorted(a for a in P if a.startswith('arayuz_kb_') and a.endswith('_pul')); KBv = sorted(a for a in P if a.startswith('arayuz_kb_') and not a.endswith('_pul'))
yakin(merkez(KBv[0]) + np.array([0, 60, 0]), 0.42, tt=t)
for i, (p, v) in enumerate(zip(KBp, KBv)): tak(p, t + i * 0.15, 0.6, 130.0); tak(v, t + 0.35 + i * 0.15, 0.7, 140.0)
olay(t, 'Pul (Ø15) + cıvata M8 × 25: Ø16 servis deliğinden → boru alt duvarı Ø9 → B dış tavanı → perçin somun (alyan 6)')
t = bitti() + 0.5
# ---- 5 DIŞ TABAN
adim('Dış taban', 'Dış taban (1,5 mm) lazerde kesilir, abkantta 3 kenarı yukarı bükülür; arka dönüşe servis sacı için 4 kaynak burcu puntalanır, mekanizma için 4 saplama preslenir. Kaide plakasına iner. Teknik ön perde (lazer → 2 büküm) yukarıdan tabana oturur; 2 cıvata M6 × 12 perde flanşının yarığından tabandan geçip plakadaki somuna, ikisini birlikte sıkar.',
     'dış taban · 3 büküm · kaynak burcu M5 × 4 · saplama M5 × 4 · teknik ön perde · cıvata M6 × 12 × 2 → somun M6')
kamera_genel(['dis_taban'], yon=(0.45, 0.8, 0.65), olcek=0.8)
t = koy('dis_taban', [YOL((0, 450, 0))], 'Dış taban → kaide plakası', pem=sorted(PEM_SAC['dis_taban']))
XPAB = sorted(a for a in P if a.startswith('x_ekseni_pabuc_') and P[a]['tur'] == 'mek')
t = pabuc_kaynak(XPAB, t, (0, 200, 0), 'X ekseni bağlama pabucu (3 mm L) → dış tabana, dış kenarı TIG (kırmızı)')
M6 = sorted(a for a in P if a.startswith('arayuz_kaide_M6'))
kamera_genel(['teknik_on_perde'], yon=(0.35, 0.6, 0.8), olcek=0.8)
t = koy('teknik_on_perde', AD(UST6), 'Teknik ön perde (lazer → 2 büküm) → yukarıdan dış tabana; alt flanşındaki yarıklar cıvata yerlerine (punta)')
yakin(merkez(M6[0]), 0.3, yon=(0.4, 0.8, 0.5), tt=t)
t = sira_tak(M6, t, 40.0, 0.55, 0.25); olay(t - 0.5, '2 cıvata M6 × 12: perde flanşı yarığından → dış taban → kaide plakasındaki somun (flanşı ve tabanı sıkar)'); t += 0.5
# ---- 6 X EKSENİ (yan saclar kapanmadan: ray tabanı her iki yan sacın tabla ağzından geçer)
adim('X ekseni (tabla hattı)', 'X ekseni ünitesi (ray tabanı + 2 lineer ray + araba + bantlı tabla + kayış, hazır ürün) yan saclar kapanmadan yukarıdan iner: ray tabanı A tarafına uzanır, iki yan sacın tabla geçiş ağzından geçecek. Ünite A kaidesine bağlanır (A sayfası). Motoru (braket + kasnak) sağ yan sac takılmadan sağdan gelir, teknik ön perdenin altından ray tabanının ucuna oturur.',
     'X ekseni ünitesi + motoru (hazır)')
kamera_genel(['x_ekseni'], yon=(0.3, 0.6, 0.85), olcek=0.75)
P['x_ekseni']['tezgah'] = True; P['x_motor']['tezgah'] = True
t = koy('x_ekseni', AD(UST6, lift=(5, 10, 50)), 'X ekseni ünitesi → yukarıdan, pabuçların arasına (ray tabanı A kaidesine de bağlanır, A sayfasında)')
yakin(merkez(XPAB[0]), 0.4, tt=t)
t = vidala([a + '_vida' for a in XPAB], t, 25.0); olay(t - 1.2, 'Pabuç → ray tabanı: 4 × ISO 4762 M5 × 10 + pul (ray tabanındaki M5 perçin somuna)'); t += 0.3
t = koy('x_motor', [YOL((700, 0, 0), (0, 20, 0)), YOL((700, 0, 0), (0, 25, 0))], 'X ekseni motoru (braket + kasnak) → sağdan, taban dönüşünün üstünden; braketi ray tabanının ucuna iner (perdenin altından)')
# ---- 7 DIŞ YAN SAĞ
adim('Dış yan sağ', 'Sağ yan sac (F tarafı, fiş paneli ağzı) lazerde kesilir, abkantta 1 büküm; 4 somun M8 (F bağlantısı), 6 kaynak burcu (servis sacı), 2 uzun saplama (fiş paneli) ve 4 saplama preslenir. Yukarıdan tabla ağzı ray tabanının üstünden geçerek dış tabanın yan dönüşüne oturur, içeriden TIG.',
     'dış yan sağ · 1 büküm · 16 somun / saplama / burç · TIG')
kamera_genel(['dis_yan_sag', 'dis_taban'], yon=(0.6, 0.45, 0.65), olcek=0.75)
t = koy('dis_yan_sag', AD(UST6, (700, 0, 0)), 'Dış yan sağ → yukarıdan, dış tabanın yan dönüşüne (TIG)', pem=sorted(PEM_SAC['dis_yan_sag']), grup_kaynak=PUNTA['yan_sag_taban'])
# ---- 8 KURU BÖLME + SOĞUTMA GRUBU
adim('Kuru bölme + soğutma grubu', 'Soğutma cebi (lazer → 3 büküm → 4 somun M8) taşıyıcılara iner; soğutma grubu (hazır ürün) cebe oturur. Ayırma perdesi, teknik ön perde ve sağ perde yukarıdan yerine. Kondenser kanalının alt braketi ve kanalı; kuru bölme tabanı (kablo rakoru tezgâhta takılı) yukarıdan kanalın üstünden geçerek iner; kanal geçiş kapağı sağdan sürülür, 2 vida.',
     'soğutma cebi + 4 somun · soğutma grubu · 3 perde · kanal braketi · kondenser kanalı · kuru bölme tabanı + 5 somun + rakor · kanal kapağı + 2 vida')
kamera_genel(['sogutma_cebi', 'teknik_on_perde'], yon=(0.35, 0.6, -0.75), olcek=0.8)
t = koy('sogutma_cebi', AD(UST6, ARKA9), 'Soğutma cebi → cep taşıyıcılara (punta)', pem=sorted(PEM_SAC['sogutma_cebi']))
t = koy('sogutma_grubu', AD(UST6, ARKA9), 'Soğutma grubu (hazır ürün) → yukarıdan cebe iner')
t = koy('sogutma_parca_2492_957', AD(UST6, ARKA9, ON9), 'Silikon tapa → sağ yan geçişine')
t = koy('ayirma_perdesi_cep_sol', AD(UST6, ARKA9), '%s → yukarıdan yerine, dış tabana 3 × 40 mm TIG (kırmızı)' % tr('ayirma_perdesi_cep_sol'), grup_kaynak=KAY('ayirma_perdesi_cep_sol_kaynak'))
t = koy('teknik_sag_perde', AD(UST6, ARKA9), '%s → yukarıdan yerine, dış tabana 3 × 40 mm TIG (kırmızı)' % tr('teknik_sag_perde'), grup_kaynak=KAY('teknik_sag_perde_kaynak'))
t = koy('kondenser_braketi', AD(UST6, ARKA9), 'Kondenser kanalı alt braketi → dış tabanın saplamalarına')
t = koy('kondenser_kanali', AD(ARKA9, UST6), 'Kondenser kanalı (dirsekli boru) → braketine')
kamera_genel(['kuru_bolme_tabani'], yon=(0.4, 0.8, -0.6), olcek=0.8)
t = koy('kuru_bolme_tabani', AD(UST6, ARKA9, lift=(300, 500)), 'Kuru bölme tabanı → yukarıdan iner, kanal borusu tabandaki delikten geçer (punta)', pem=sorted(PEM_SAC['kuru_bolme_tabani']))
yakin(merkez('kanal_gecis_kapagi'), 0.35, yon=(0.6, 0.6, -0.5), tt=t)
t = koy('kanal_gecis_kapagi', [YOL((0, 300, 0), (150, 0, 0)), YOL((0, 300, 0), (160, 0, 0)), YOL((0, 300, 0), (180, 0, 0))], 'Kanal geçiş kapağı → borunun sağında iner, yarığıyla sola sürülür')
KKV = sorted(a for a in P if a.startswith('kanal_kapagi_') and a.endswith('_vida'))
t = sira_tak(KKV, t, 30.0, 0.45, 0.2); olay(t - 0.5, 'Kapak: 2 vida M5 → tabandaki preslenmiş somunlara'); t += 0.4
# ---- 9 SOĞUK ODA TABAN + ARKA DUVAR
adim('Soğuk oda: taban + arka duvar', 'Soğuk oda alt sacı (6 düşme deliği, saplamalı) ve arka dış sacı yerine girer; 4 evaporatör kanal kovanı (iki L + boyuna kaynak) ağızlara; arka duvara POM geçiş blokları. Dış saca yapıştırıcı (yeşil) sürülür, ölçüsünde kesilmiş arka PU levhası önden bastırılır.',
     'alt sac · arka dış sac · kanal kovanı × 4 · POM geçiş bloğu · yapıştırıcı · PU levha arka')
kamera_genel(['soguk_alt_sac', 'soguk_arka_dis_sac'], yon=(0.35, 0.5, 0.85), olcek=0.75)
XB_ = sorted(a for a in P if a.startswith('x_sensor_braket_') and P[a]['tur'] == 'mek')   # v6: dördü de X ekseni ↔ alt sac arasında; 5 Eki: X ekseninin üstünde sıfır boşluk → alt sactan önce X ekseninin üstüne, alt sacın saplaması iner, somun aynı adımda
for a in XB_: koy(a, AD(ON9, (-700, 0, 0)), 'X ekseni sensör braketi → X ekseninin üstüne (alt sacın saplaması deliğinden inecek, somun)', sure_bekle=0.05)
t = bitti()
t = koy('soguk_alt_sac', AD(UST6, ON9, ARKA9), 'Soğuk oda alt sacı → teknik perdelerin üstüne (punta)', pem=sorted(PEM_SAC['soguk_alt_sac']))
t = koy('soguk_arka_dis_sac', AD(ARKA9, ON9, UST6), 'Soğuk oda arka dış sacı → alt sac + yanlar (punta)', pem=sorted(PEM_SAC['soguk_arka_dis_sac']))
BRK_ = sorted(a for a in P if (a.startswith('motor_') and a.endswith('_braket')) or a.startswith('valf_adasi_braket_')) 
BRK_ = [a for a in BRK_ if P[a]['tur'] == 'mek']
t = pabuc_kaynak(BRK_, t, (0, 0, -300), 'Braket (3 mm, lazer + büküm) → arka dış sacın arka yüzüne, TIG (kırmızı): motor × 4 · valf adası × 2')
for k in range(4):
    for j in (1, 2):
        koy('evap_kanal_kovani_%d_L%d' % (k, j), AD(ON9), '%s → arka dış sacın ağzına' % tr('evap_kanal_kovani_%d_L%d' % (k, j)),
            grup_kaynak=(KAY('evap_kanal_kovani_%d_boyuna_kaynak' % k) if j == 2 else ()), sure_bekle=0.05)
    t += 0.4
t = bitti() + 0.2
for a in sorted(a for a in P if a.startswith('pom_gecis')): koy(a, AD(ON9, ARKA9), 'POM geçiş bloğu → arka duvara', sure_bekle=0.05)
t = bitti() + 0.3
kamera_genel(['pu_levha_arka'], yon=(0.25, 0.4, 0.9), olcek=0.7)
buyu('yapistirici_arka', t, 0.6); olay(t, 'Yapıştırıcı (yeşil) → arka dış sacın iç yüzüne'); t += 0.8
t = koy('pu_levha_arka', AD(ON9), 'PU levha arka (ölçüsünde kesilmiş, yan / tavan iç sacının flanş yuvaları açık) → yapıştırıcıya bastırılır')
# ---- 9b HAVA KANALI + VALF ADASI (5 Eki: evaporatörlerden ve silindirlerden önce — sonra arkaları kapanır)
adim('Hava kanalı + valf adası', 'Evaporatörler gelmeden kuru bölmede: hava kanalı askıları arka dış sacın saplamalarına (saplama ekseninde, arkadan) ve kuru tabanın saplamalarına (yukarıdan); hava kanalları askıların üstüne; valf adası (12 valf, hazır ürün) arkadan yerine.',
     'hava askısı × 13 · hava kanalı × 3 · valf adası')
kamera_genel(['valf_adasi', 'hava_kanal_2014_1259'], yon=(0.35, 0.45, -0.85), olcek=1.0)
for a in sorted(a for a in P if a.startswith('hava_aski')):
    ek_ = [YOL((-300, 0, 0), (0, 0, -20)), YOL((300, 0, 0), (0, 0, -20)), YOL((-60, 0, 0), (0, 0, -20))] if a == 'hava_aski_2193_1276' else []
    koy(a, AD(ARKA9, UST6) + ek_, 'Hava askısı → saplamaya', sure_bekle=0.03)
t = bitti()
for a in sorted(a for a in P if a.startswith('hava_kanal')): t = koy(a, AD(UST6, ARKA9, lift=(40,)), 'Hava kanalı → askılara')
t = koy('valf_adasi', AD(ARKA9, UST6), 'Valf adası → arkadan, Z braketlerin önüne')
t = vidala(sorted(a for a in P if a.startswith('valf_adasi_') and a.endswith('_vida')), t, 10.0); olay(t - 0.8, 'Valf adası → Z braketler: 2 × ISO 4762 M5 × 12 + pul (valfin ön yüzündeki M5 dişe) · duvar ile braket arası 27 mm: vida yandan sokulur, kısa altıgen anahtar'); t += 0.2
# ---- 10 EVAPORATÖRLER (tavan kapanmadan, yukarıdan)
adim('Evaporatörler', 'Tavan kapanmadan: iki evaporatör kaseti (serpantin + fan + PU kaset + conta, ayakları üreticide kaynaklı · hazır ürün) yukarıdan iner, ağızları kanal kovanlarına, ayakları kuru bölme tabanına; her ayak 1 vida M5 → tabandaki preslenmiş somun. Sağ kasette kıyma silindiri için yalıtımlı cep. Bakır hatlar (lehim) ve yoğuşma hortumu yerinde uzar.',
     'evaporatör L + R (hazır) · vida M5 × 4 → somun · bakır hatlar · yoğuşma hortumu')
kamera_genel(['evaporator_L', 'evaporator_R'], yon=(0.35, 0.7, -0.75), olcek=0.8)
for nm, ay in (('evaporator_L', ['evaporator_ayagi_0', 'evaporator_ayagi_1']), ('evaporator_R', ['evaporator_ayagi_2', 'evaporator_ayagi_3'])):
    t = koy([nm] + ay, AD(UST6, ARKA9, lift=(20, 60)), 'Evaporatör kaseti (hazır ürün, ayakları kaynaklı) → yukarıdan kanal kovanı ağzına, ayaklar kuru bölme tabanına')
EAV = sorted(a for a in P if a.startswith('evaporator_ayak_') and a.endswith('_vida'))
yakin(merkez(EAV[0]), 0.3, yon=(0.4, 0.7, -0.6), tt=t)
t = sira_tak(EAV, t, 30.0, 0.45, 0.2); olay(t - 0.5, 'Her ayak: 1 vida M5 × 6 → kuru bölme tabanındaki preslenmiş somun'); t += 0.4
buyu('bakir_hat', t, 1.0)
olay(t, 'Bakır hatlar (lehim): grup ↔ evaporatörler · yoğuşma hortumu silindirlerden sonra (esnek)'); t += 1.2
# ---- 11 DIŞ YAN SOL + TAVAN
adim('Dış yan sol + dış tavan', 'Sol yan (A tarafı): lazer → 1 büküm → 4 somun M8 + 2 kaynak burcu; yukarıdan, tabla ağzı ray tabanının üstünden geçerek tabanın yan dönüşüne, içeriden TIG; A tarafındaki 2 somunun iç yüzüne köpük kapağı. Dış tavan: lazer → 3 büküm → 5 kaynak burcu → yan sacların üstüne, TIG.',
     'dış yan sol + somun / burç · köpük kapağı × 2 · dış tavan + 5 burç · TIG')
kamera_genel(['dis_yan_sol', 'dis_taban'], yon=(-0.6, 0.45, 0.65), olcek=0.75)
t = koy('dis_yan_sol', AD(UST6, (-700, 0, 0)), 'Dış yan sol → yukarıdan, dış tabanın yan dönüşüne (TIG)', pem=sorted(PEM_SAC['dis_yan_sol']), grup_kaynak=PUNTA['yan_sol_taban'])
KK = sorted(a for a in P if a.endswith('kopuk_kapagi'))
yakin(merkez(KK[0]), 0.3, yon=(0.8, 0.3, 0.5), tt=t)
for i, a in enumerate(KK): tak(a, t + i * 0.2, 0.5, 40.0)
olay(t, 'Köpük kapağı × 2 → A tarafı somunlarının iç yüzüne'); t = bitti() + 0.3
kamera_genel(['dis_tavan', 'dis_yan_sol'], yon=(0.45, 0.85, 0.6), olcek=0.75)
t = koy('dis_tavan', AD(UST6), 'Dış tavan → yan sacların üstüne (TIG)', pem=sorted(PEM_SAC['dis_tavan']), grup_kaynak=PUNTA['tavan_yanlar'])
# ---- 12 YALITIM + İÇ SAC
adim('Yalıtım levhaları + iç sac', 'Yüzey yüzey: dış saca yapıştırıcı (yeşil), ölçüsünde kesilmiş PU levha (sol, sağ, tavan) önden bastırılır. İç sac kaynaksız: bükümlü kenarlar komşu levhanın yuvasına girer. Önce tavan iç sacı önden; sonra sol ve sağ iç sac önden (arka kenarı arka levhanın yuvasına, üst kenarı tavan iç sacının üstüne); arka iç sac en son önden. POM ısı kesici pullar perçin yerlerine, kör perçinler içeriden (mavi).',
     'yapıştırıcı × 3 · PU levha sol / sağ / tavan · iç sac tavan / sol / sağ / arka (bükümlü) · POM pul · tavan dikişi kör perçin Ø3,2')
PUL = lambda pre: sorted(a for a in P if a.startswith('astar_percin_' + pre) and a.endswith('_pul'))
PER = lambda pre: sorted(a for a in P if a.startswith('astar_percin_' + pre) and not a.endswith('_pul'))
for tr_ in ('sol', 'sag', 'tavan'):
    kamera_genel(['pu_levha_' + tr_], yon=(0.25, 0.4, 0.9), olcek=0.7)
    buyu('yapistirici_' + tr_, t, 0.6); olay(t, 'Yapıştırıcı (yeşil) → dış sacın iç yüzüne'); t += 0.8
    ic_ = {'sol': (20, 0, 0), 'sag': (-20, 0, 0), 'tavan': (0, -20, 0)}[tr_]   # 5 Eki: önden 20 mm içeride gelir, sonra duvara bastırılır (somun / saplama başları levha yuvasına)
    t = koy('pu_levha_' + tr_, [YOL(ON9, ic_), YOL(ON9, tuple(2 * x for x in ic_))] + AD(ON9, lift=(2, -2)), 'PU levha %s (ölçüsünde kesilmiş) → önden, yapıştırıcıya bastırılır' % {'sol': 'sol', 'sag': 'sağ', 'tavan': 'tavan'}[tr_])
kamera_genel(['pu_levha_sol'], yon=(0.6, 0.4, 0.75), olcek=0.8)
BURC = sorted(a for a in P if a.startswith('pom_burc'))   # 5 Eki: burç dış sac ile iç sac arasında, PU levhanın deliğinde → iç sactan ÖNCE, içeriden levha deliğine
for i, a in enumerate(BURC):
    e_ = np.asarray(P[a]['eks'], float); t_ = t + i * 0.08
    basla(a, e_ * 80.0, t_); git(a, np.zeros(3), t_, 0.5); vurgu([a], t_ + 0.3, t_ + 1.2); YER[a] = t_ + 0.5; YERINDE.append(a)
olay(t, 'Raf askı burcu POM × 16 → içeriden PU levhanın deliğine, dış sacın iç yüzüne (iç sac sonra üstünü kapatır)'); t = bitti() + 0.5
kamera_genel(['astar_tavan'], yon=(0.25, 0.3, 0.9), olcek=0.7)
t = koy(['astar_tavan'] + PUL('tavan_'), AD(ON9, lift=(2, -2)), 'Tavan iç sacı (arka kenarı aşağı, ön kenarı yukarı bükümlü · üstünde POM pullar) → önden, levha yuvalarına')
for tr_ in ('sol', 'sag'):
    kamera_genel(['astar_' + tr_], yon=(0.6 if tr_ == 'sag' else -0.6, 0.4, 0.75), olcek=0.8)
    t = koy('astar_' + tr_, AD(ON9, lift=(2, -2)), '%s iç sacı (arka ve üst kenarı içe, ön kenarı dışa bükümlü) → önden; arka kenarı arka levhanın yuvasına, üst kenarı tavan iç sacının üstüne' % {'sol': 'Sol', 'sag': 'Sağ'}[tr_])
kamera_genel(['astar_arka'], yon=(0.25, 0.3, 0.9), olcek=0.7)
t = koy(['astar_arka'] + PUL('arka_'), AD(ON9), 'Arka iç sac (düz · arka yüzünde POM pullar) → en son önden, yan flanşlarının önüne')
yakin(merkez(PER('tavan_')[0]), 0.35, yon=(0.6, 0.3, 0.75), tt=t)
t = sira_tak(PER('tavan_'), t, 25.0, 0.35, 0.05)
olay(t - 1.0, 'Kör perçin Ø3,2 × %d içeriden: tavan iç sacı → POM pul → yan iç sacın üst flanşı (sızdırmaz kapalı uç) · arka dikişler raf oturunca' % len(PER('tavan_'))); t += 0.4
# ---- 13 RAF, KOVANLAR, EŞİK
adim('Raf, kovanlar, eşik', '7 düşme kovanı alt sacın deliklerine (tavuk / kuşbaşı iki L + boyuna kaynak; patates / harç / kıyma boru Ø38; kaşar / sucuk POM); PU raf levhası yukarıdan kovanların üstünden; raf köşebentleri levhanın kenar yuvasına, kaset kilit mandalları cebine; raf (3 mm, lazer → 4 büküm, 4 saplama) üstüne iner, arka köşe dolgu kaynağı (kırmızı). Kovan contaları, dil kanalları, eşik, yiv dolguları + köşe silikonu (yeşil).',
     'düşme kovanı × 7 · PU raf levhası · köşebent × 2 · mandal × 2 · raf + 4 saplama · arka dikiş kör perçinleri · conta × 5 · dil kanalı × 2 · eşik · yiv dolgusu · silikon')
kamera_genel(['raf', 'raf_kosebendi_sol'], yon=(0.35, 0.7, 0.75), olcek=0.75)
for a in ('dusme_kovani_kiyma_L1', 'dusme_kovani_kiyma_L2', 'dusme_kovani_kusbasi_L1', 'dusme_kovani_kusbasi_L2'):
    koy(a, AD(ON9, UST6), '%s → alt sacın deliğine' % tr(a), grup_kaynak=(KAY(a[:-3] + '_boyuna_kaynak') if a.endswith('L2') else ()), sure_bekle=0.05)
for a in ('dusme_kovani_sos', 'dusme_kovani_harc', 'dusme_kovani_kiyma', 'dusme_kovani_kasar', 'dusme_kovani_sucuk'):
    koy(a, AD(UST6, ON9), 'Düşme kovanı → alt sacın deliğine', sure_bekle=0.05)
t = bitti() + 0.2
t = koy('pu_raf_esik', AD(UST6, lift=(100, 300)), 'PU raf levhası → kovanların üstünden alt saca')
for a in ('raf_kosebendi_sol', 'raf_kosebendi_sag'): koy(a, AD(UST6, ON9), '%s → levhanın kenar yuvasından alt saca; ön ve arka ucu yan iç saca TIG (kırmızı)' % tr(a), grup_kaynak=KAY(a + '_kaynak'))
for ad in ('kasar', 'sucuk'): koy('kaset_%s_mandal' % ad, AD(UST6), 'Kaset kilit mandalı → levhanın cebine', sure_bekle=0.05)
t = bitti()
t = koy('raf', AD(ON9, lift=(45, 50, 60, 100), yan=()) + AD(UST6, lift=(60, 100, 300)), 'Raf → önden, düşme kovanlarının üstünden PU levhanın üstüne iner, kenarları köşebentlere (punta)', pem=sorted(PEM_SAC['raf']), grup_kaynak=KAY('raf_arka_kose_dolgusu'))
# 5 Eki: arka dikiş perçinlerinin başı rafın arka kenarına 1,1 mm taşar → raf oturduktan sonra içeriden atılır
yakin(merkez(PER('arka_sol')[0]), 0.35, yon=(0.6, 0.3, 0.75), tt=t)
t = sira_tak(PER('arka_'), t, 25.0, 0.35, 0.05)
olay(t - 1.0, 'Kör perçin Ø3,2 × %d içeriden: arka iç sac → POM pul → yan / tavan iç sacın flanşı (raf yerindeyken)' % len(PER('arka_'))); t += 0.4
for a in sorted(a for a in P if a.endswith('_conta') and a.startswith(('kaset_', 'uno_')) and 'raf' not in a): koy(a, AD(UST6), 'Kovan contası → raf deliğine', sure_bekle=0.03)
t = bitti()
UPAB_ALT = sorted(a for a in P if a.startswith(('uno_tavuk_pabuc_', 'uno_kusbasi_pabuc_')) and P[a]['tur'] == 'mek')
t = pabuc_kaynak(UPAB_ALT, t, (0, 200, 0), 'UNO bağlama pabucu (3 mm L) → rafa, dış kenarı TIG (kırmızı)')
kamera_genel(['soguk_esik', 'dil_kanali_kasar'], yon=(0.3, 0.6, 0.9), olcek=0.7)
for a in ('dil_kanali_kasar', 'dil_kanali_sucuk'): t = koy(a, AD(ON9, UST6), '%s → rafın kesiğine' % tr(a))
t = koy('soguk_esik', AD(ON9, UST6), 'Eşik → rafın ön kenarına', grup_kaynak=KAY('raf_esik_yiv') + KAY('esik_on_yiv'))
for k in sorted(a for a in P if a.startswith('dil_kesik_kose_silikonu')): buyu(k, t, 0.4)
olay(t, 'Yiv dolgusu kaynak + taşlama · eşik kesiği köşe silikonu'); t += 0.9
# ---- 14 UNO'LAR, KASETLER, ÜST RAF
adim('UNO\'lar, kasetler, üst raf', 'Kaset rayları raf saplamalarına. Tavuk ve kuşbaşı UNO\'su (hazır ürün gövdesi) önden yukarıda gelir, rafa ve kovana iner. Üst raf köşebentleri + üst raf (3 mm, lazer → 2 büküm; 3 geçiş deliği + contaları). Lahmacun harcı, kıyma ve patates UNO gövdeleri önden yukarıda gelir, çıkış borusu üst raf deliğindeki contadan iner; kıyma çıkış dirseği (2 × 90°) yukarıdan UNO ağzına. Çıkış boruları alttan kovana, gıda hortumları üst raf deliğinden iner, raf altı flanş + kelepçe. Kaşar / sucuk çıkış ağzı alttan kovana; kasetler (hazır ürün) önden dil kanalında sürülür.',
     'kaset rayı × 2 · UNO × 5 · üst raf + köşebent × 2 + conta × 3 · kıyma dirseği · çıkış borusu × 3 · hortum × 3 · flanş × 3 · kelepçe × 3 · kaşar / sucuk çıkış ağzı + kaset')
kamera_genel(['uno_tavuk_on', 'uno_patates_on', 'kaset_kasar'], yon=(0.3, 0.45, 0.9), olcek=0.9)
ALT = [YOL((0, -150, 0)), YOL((0, 0, 700), (0, -150, 0)), YOL((0, 0, 700), (0, -120, 0))] + [YOL((0, 0, 700), (0, -d_, 0)) for d_ in (80, 90, 100, 110, 70, 60)]   # 5 Eki: X ekseni artık altta → önden, raf ön kenarının altından alçak gelir
INIS = dict(lift=(110, 120, 130, 140), yan=())
for ad in ('kasar', 'sucuk'): t = koy('kaset_ray_' + ad, AD(ON9, lift=(15, 20, 30)), 'Kaset rayı → raf saplamalarına')
for ad in ('tavuk', 'kusbasi'):
    t = koy('uno_%s_on' % ad, AD(ON9, **INIS), 'UNO %s → önden yukarıda gelir, pabuçların arasından rafa ve kovana iner' % UNO_TR[ad])
    t = vidala(['uno_%s_pabuc_sol_vida' % ad, 'uno_%s_pabuc_sag_vida' % ad], t, 25.0); olay(t - 0.8, 'UNO %s → pabuçlar: 2 × ISO 4762 M5 × 12 + pul yandan tabandaki M5 dişe' % UNO_TR[ad])
kamera_genel(['ust_raf'], yon=(0.3, 0.5, 0.9), olcek=0.8)
for a in ('ust_raf_kosebendi_sol', 'ust_raf_kosebendi_sag'): koy(a, AD(ON9), '%s → yan iç saca, alt kenarı boyunca TIG (kırmızı)' % tr(a), grup_kaynak=KAY(a + '_kaynak'))
t = bitti()
RC_ = sorted(a for a in P if a.endswith('_raf_conta'))   # 5 Eki: geçiş contaları tezgâhta üst rafın deliklerine takılır (yukarıda tavan var)
P['ust_raf']['tezgah'] = True
t = koy(['ust_raf'] + RC_, AD(ON9, lift=(20, 40)), 'Üst raf (geçiş contaları tezgâhta takılı) → köşebentlere (punta)')
t = bitti()
UPAB_UST = sorted(a for a in P if a.startswith(('uno_harc_pabuc_', 'uno_kiyma_pabuc_', 'uno_patates_pabuc_')) and P[a]['tur'] == 'mek')
t = pabuc_kaynak(UPAB_UST, t, (0, 150, 0), 'UNO bağlama pabucu (3 mm L) → üst rafa, dış kenarı TIG (kırmızı)')
for ad in ('harc', 'kiyma', 'patates'):
    if ad == 'kiyma':   # 5 Eki: gövde arkası burca, çıkışı dirseğe (z), dirseğin alt bacağı raf deliğine (y) → tezgâhta birleşik birim, tek iniş
        P['uno_kiyma_on']['tezgah'] = True; P['uno_kiyma_dirsek']['tezgah'] = True
        t = koy(['uno_kiyma_on', 'uno_kiyma_dirsek'], AD(ON9, lift=(30, 35, 28, 38), yan=()), 'UNO kıyma gövdesi + çıkış dirseği (2 × 90°, tezgâhta kelepçeyle birleşik) → önden yukarıda gelir, dirseğin alt bacağı üst raf contasından iner')
    else:
        t = koy('uno_%s_on' % ad, AD(ON9, lift=(40, 60, 80, 100), yan=()), 'UNO %s gövdesi → önden yukarıda gelir, çıkış borusu üst raf deliğindeki contadan iner' % UNO_TR[ad])
    t = vidala(['uno_%s_pabuc_sol_vida' % ad, 'uno_%s_pabuc_sag_vida' % ad], t, 25.0); olay(t - 0.8, 'UNO %s → pabuçlar: 2 × ISO 4762 M5 × 12 + pul yandan tabandaki M5 dişe' % UNO_TR[ad])
    t = koy('uno_%s_raf_flans' % ad, [YOL((0, -150, 0)), YOL((0, 0, 700), (0, -150, 0))], 'Üst raf altı hortum flanşı → alttan deliğe')
    t = koy('uno_%s_cikis' % ad, ALT, 'UNO %s çıkış borusu%s → alttan kovana' % (UNO_TR[ad], '' if ad == 'kiyma' else ' + yayıcı'))
    t = buyu('uno_%s_hortum' % ad, t, 0.8); olay(t - 0.8, 'Gıda hortumu → üst raf deliğinden boruya iner')
    t = koy('uno_%s_kelepce' % ad, AD(ON9, UST6, lift=(5, 10)), 'Kelepçe → boru ile hortumu birleştirir (elle kapatılır)')
for ad in ('kasar', 'sucuk'):
    t = koy('kaset_%s_cikis' % ad, ALT, '%s çıkış ağzı → alttan kovana' % {'kasar': 'Kaşar', 'sucuk': 'Sucuk'}[ad])
    t = koy('kaset_' + ad, AD(ON9, lift=(5, 10)), '%s kaseti (hazır ürün) → önden dil kanalında sürülür, mandal kilitler' % {'kasar': 'Kaşar', 'sucuk': 'Sucuk'}[ad])
# ---- 15 ARKA GRUPLAR
adim('Arkadan: burçlar, motorlar, silindirler', 'Servis sacı kapanmadan arkadan: POM duvar burçları ve kıyma burç kılıfı (evaporatör cebi ağzından) duvar deliklerine; kaset tahrik motorları (hazır) kaplini burçtan kasete; 5 UNO pnömatik silindiri, mili burçtan geçip pistona vidalanır. Motor sensörleri motorla gelir.',
     'POM burç × 7 · burç kılıfı · motor × 2 + sensör · UNO silindiri × 5')
kamera_genel(['motor_kasar', 'uno_tavuk_arka', 'uno_patates_arka'], yon=(0.35, 0.45, -0.85), olcek=0.9)
for a in sorted(a for a in P if a.startswith('burc_')): koy(a, AD(ARKA9), 'POM duvar burcu → arkadan duvar deliğine (sıkı geçme)' if a != 'burc_kilifi_kiyma' else 'Burç kılıfı → arkadan evaporatör cebi ağzından duvar deliğine', sure_bekle=0.05)
t = bitti() + 0.2
SENS = {'motor_kasar': ['elk_koyu_2083_1142'], 'motor_sucuk': ['elk_koyu_2356_1162', 'elk_koyu_2356_1266']}
for a in ('motor_kasar', 'motor_sucuk') + tuple('uno_%s_arka' % u for u in UNO):
    t = koy([a] + SENS.get(a, []), AD(ARKA9), ('Kaset motoru (hazır, sensörleriyle) → arkadan braketlerin arasına, kaplini burçtan kasete geçer' if a.startswith('motor') else 'UNO pnömatik silindiri → arkadan, mili burçtan geçip pistona vidalanır'))
    if a.startswith('motor'):
        ad_ = a.split('_')[1]
        for y_ in ('sol', 'sag'): koy('motor_%s_%s_dolgu' % (ad_, y_), AD((0, 0, -150), (0, 150, 0), (0, -150, 0), lift=(), yan=()), 'Ara dolgu (lazer) → braket bacağı ile motor gövdesi arasına', sure_bekle=0.05)
        t = bitti()
        t = vidala(['motor_%s_sol_vida' % ad_, 'motor_%s_sag_vida' % ad_], t, 25.0); olay(t - 0.8, 'Motor → braketler: 2 × ISO 4762 M5 × 16 + pul yandan gövdedeki M5 dişe')
buyu('yogusma_hortumu', t, 1.0); olay(t, 'Yoğuşma hortumu (esnek) → evaporatör tavalarından soğutma cebine, silindirlerin altından'); t += 1.2
# ---- 16 ÖN ÇERÇEVE
adim('Ön çerçeve', 'POM ısı kesici pullar iç sacın ön kenarlarına; ön çerçeve 430 (1,0 · manyetik fitil yüzü) önden dış sacın alnına (punta); 20 havşa başlı kör perçin çerçeveden (yüzeyle aynı düzlem); derz silikonu (yeşil) gıda tarafı iç köşelere ve çerçeve derzine.',
     'POM pul × 20 · ön çerçeve 430 · havşa kör perçin × 20 · derz silikonu')
kamera_genel(['on_cerceve_430'], yon=(0.3, 0.4, 0.9), olcek=0.75)
for i, a in enumerate(PUL('cerceve_')): tak(a, t + i * 0.04, 0.4, 200.0)
olay(t, 'POM ısı kesici pul × %d → iç sacın ön kenarlarına' % len(PUL('cerceve_'))); t = bitti() + 0.2
t = koy('on_cerceve_430', AD(ON9), 'Ön çerçeve 430 → soğuk oda önü (dış saca punta)') + 0.2
yakin(merkez(PER('cerceve_sol')[0]), 0.3, yon=(0.4, 0.3, 0.9), tt=t)
t = sira_tak(PER('cerceve_'), t, 25.0, 0.35, 0.05); olay(t - 1.0, 'Havşa başlı kör perçin Ø3,2 × %d çerçeveden (yüzeyle aynı düzlem, kapak fitili oturur)' % len(PER('cerceve_'))); t += 0.4
for a in sorted(a for a in P if a.startswith('derz_')): buyu(a, t, 0.8)
olay(t, 'Derz silikonu (yeşil) → gıda tarafı iç köşeler + çerçeve derzi'); t += 1.0
# ---- 17 HAVA + ELEKTRİK İÇ
adim('İç kanallar, fiş paneli, hortumlar, kablolar', 'İç kablo kanalları ve braketler; fiş paneli sağ yandaki uzun saplamalara içeriden. Hava hortumları (yeşil), güç (kırmızı) ve bilgi (mavi) kabloları kanal boyunca uzar.',
     'iç kanallar · fiş paneli · hortumlar · kablolar')
kamera_genel(['servis_cihaz', 'j1_panel'], yon=(0.35, 0.45, -0.85), olcek=1.0)
ELK = [a for a in P if a.startswith('elk_') and a not in sum(SENS.values(), []) and a != 'elk_rakor_1689_1099']
t = koy(['elk_kanal_2450_910', 'elk_rakor_2447_911'], AD(ARKA9, UST6, ON9, (-100, 0, 0)), 'Kablo kanalı + rakoru → sağ arka köşe')
for a in sorted(a for a in ELK if a not in ('elk_kanal_2450_910', 'elk_rakor_2447_911')):
    koy(a, AD(ARKA9, ON9, UST6, (-100, 0, 0), (100, 0, 0)) + [YOL((-40, 0, 0)), YOL((-15, 0, 0)), YOL((15, 0, 0))], '%s → yerine' % P[a]['ac'], sure_bekle=0.03)
t = bitti()
t = koy('j1_panel', [YOL((0, 0, -500), (-60, 0, 0))] + AD(ARKA9), 'Fiş paneli → sağ yanın uzun saplamalarına (içeriden)')
for a in ('hava_hortum', 'hava_giris', 'j1_kablo', 'kablo_guc', 'kablo_bilgi'): buyu(a, t, 1.0)
olay(t, 'Hava hortumları (yeşil) · güç (kırmızı) / bilgi (mavi) kabloları kanal boyunca'); t += 1.4
# ---- 18 SERVİS SACI ALT MONTAJI (tezgâhta, arkada)
adim('Arka servis sacı alt montajı', 'Arka servis sacı (1,5 mm, lazer, büküm yok; 17 çökertme) 9 saplama ile preslenir; pano kutusu, DIN plakası, sürücü kartları, kanallar ve filtre kapağı sacın saplamalarına tezgâhta (arkada) takılır.',
     'servis sacı + saplama M5 × 9 · pano + DIN + kartlar + kanallar (hazır)')
OFS_SV = np.array([0, 0, -700.0])
kamera_genel(['dis_arka_servis'], yon=(0.4, 0.4, -0.85), olcek=1.0, ofs=OFS_SV)
SV_PEM = sorted(PEM_SAC['dis_arka_servis'])
s_ = SAC['dis_arka_servis']
basla('dis_arka_servis', OFS_SV, t); olay(t, 'Arka servis sacı · LAZER: düz levha %.0f × %.0f mm (kontur + delikler + 17 çökertme)' % (s_.levha['boy'], s_.levha['en']))
ACN.append(dict(ad='dis_arka_servis', ac='Arka servis sacı 1,5', t=s_.t, t0=round(t, 3), t1=round(t + 1.0, 3), levha=[s_.levha['boy'], s_.levha['en']], bukum=[]))
for p in SV_PEM: basla(p, OFS_SV + np.asarray(P[p]['yan']) * 30.0, t + 0.45); git(p, OFS_SV, t + 0.45, 0.45); vurgu([p], t + 0.75, t + 1.4)
olay(t + 0.45, 'Arka servis sacı · PEM presleme: %d × saplama M5' % len(SV_PEM)); t += 1.2
basla('servis_cihaz', OFS_SV + np.array([0, 0, 250.0]), t); git('servis_cihaz', OFS_SV, t, 0.9); vurgu(['servis_cihaz'], t + 0.7, t + 1.6)
olay(t, 'Pano kutusu + DIN plakası + sürücü kartları + kanallar → servis sacının saplamalarına (tezgâhta)'); t += 1.4
P['dis_arka_servis']['tezgah'] = True; P['servis_cihaz']['tezgah'] = True
# ---- 19 SERVİS SACI KAPANIR
adim('Arka servis sacı kapanır', 'Servis sacı alt montajıyla birlikte arkadan gelir; 17 havşa başlı vida M5 × 12 çökertilmiş deliklerden yan, tavan ve taban dönüşlerinin iç yüzündeki kaynak burçlarına. Dış yüz düz; bakımda sac tek parça çıkar, evaporatörler tabana bağlı kalır.',
     'servis sacı alt montajı · havşa vida M5 × 12 × 17 → kaynak burcu')
SVG = ['dis_arka_servis', 'servis_cihaz'] + SV_PEM
kamera_genel(['dis_arka_servis'], yon=(0.4, 0.4, -0.85), olcek=0.95)
for a in SVG: git(a, np.zeros(3), t, 1.6)   # v6 adım 65: sensörün önündeki kanal 25 mm → düz girer
olay(t, 'Servis sacı alt montajı arkadan yerine'); t += 1.7
for a in SVG: YER[a] = t; YERINDE.append(a)
SVV = sorted(a for a in P if a.startswith('servis_arka') and a.endswith('_vida'))
t = sira_tak(SVV, t, 30.0, 0.45, 0.08); olay(t - 1.0, 'Havşa vida M5 × 12 × 17 → dönüşlerdeki kaynak burçları (baş dış yüzle aynı düzlemde)'); t += 0.5
# ---- 20 KAPAKLAR
adim('Ön braketler + kapaklar', 'Ön alt braket, gizli menteşe gövdeleri (alttakiler yan sactaki saplamalara, içten somun) ve bas-aç mandalları ön kasaya; kapak emniyet anahtarları tabana kaynaklı 2 mm braketlere (önden 2 × M4 → braketteki PEM somun). Kanatlar tezgâhta hazır: K1 emniyet aktüatörüyle, K2 orta kayıt + emniyet aktüatörü + iki kaset takozuyla — 90° açık, menteşe tarafından yaklaşır, pimlere iner ve kapanır. Kapak kapanınca takozlar kasetleri yerinde kilitler (kaset tam oturmamışsa kapak kapanmaz, emniyet anahtarı makineyi başlatmaz).',
     'ön alt braket · menteşe × 6 + somun × 4 · bas-aç × 4 · emniyet braketi × 2 + PEM somun × 4 · emniyet anahtarı × 2 + M4 × 4 · kanat K1 / K2 (K2: orta kayıt + kaset takozları)')
kamera_genel(['on_alt_braket'], yon=(0.3, 0.45, 0.9), olcek=0.75)
t = koy('on_alt_braket', [ON, YOL((0, 0, 300), (0, 30, 0))], 'Ön alt braket → taban saplamalarına')
for a in sorted(a for a in P if a.startswith(('mentese_', 'basac_')) and P[a]['tur'] == 'mek'): koy(a, [YOL((80, 0, 0)) if a == 'mentese_sol_893' else YOL((-80, 0, 0)) if a == 'mentese_sag_893' else YOL((0, 0, 80))], '%s → ön kasaya' % P[a]['ac'].split('(')[0].strip(), sure_bekle=0.03)
t = bitti()
MS_ = sorted(a for a in P if a.startswith('mentese_') and a.endswith('_somun'))
for i_, a_ in enumerate(MS_):
    tak(a_[:-6] + '_pul', t + i_ * 0.25, 0.4, 20.0); tak(a_, t + i_ * 0.25 + 0.3, 0.5, 20.0)
t = bitti(); olay(t - 0.8, 'Alt menteşeler: yan sactaki gömme başlı preslenmiş saplamalar (M4) menteşe gövdesinden geçer → içte pul + fiberli somun M4 (× 4)')
for k_ in ('K1', 'K2'):
    koy(['emniyet_%s_braket' % k_] + sorted(a for a in P if a.startswith('emniyet_%s_' % k_) and a.endswith('_somun')), [YOL((0, 0, 120)), YOL((0, 0, 120), (0, 40, 0))],
        'Emniyet sensörü braketi (2 mm L, 2 × PEM S-M4 tezgâhta preslenir) → dış tabana, ayağın arka kenarı TIG (kırmızı)', grup_kaynak=['emniyet_%s_braket_kaynak' % k_], sure_bekle=0.05)
t = bitti()
for e_ in sorted(a for a in P if a.startswith('emniyet_sensor_')): koy(e_, [YOL((0, 0, 120))], 'Kapak emniyet anahtarı (RSS36) → braketin önüne (M12 kablo kanal içinden)', sure_bekle=0.03)
t = bitti()
t = vidala(sorted(a for a in P if a.startswith('emniyet_K') and a.endswith('_vida')), t, 30.0); olay(t - 0.8, 'Emniyet sensörü → braket: 2 × ISO 4762 M4 × 20 önden sensörün gömme yuvasından braketteki preslenmiş somuna (M4) (× 2 sensör)'); t += 0.3
kam(t, ([1.0, 2.6, 3.6], [1.97, 1.4, 0.2]))
KAPGRUP = []
for kn, piv, aci in (('kanat_K2', (2.497, 0.079), 90.0), ('kanat_K1', (1.438, 0.079), -90.0)):   # v6: orta kayıt K2'de → önce K2 kapanır, K1 kayıtın önüne kapanır
    basla(kn, np.array([0, 25.0, 300.0]), t); KAPGRUP.append(kn)
    ROT[kn] = [[round(t - 0.01, 3), round(t, 3), aci, piv[0], piv[1]]]
    git(kn, np.array([0, 25.0, 0]), t, 1.0); git(kn, np.zeros(3), t + 1.1, 0.5)
    ROT[kn].append([round(t + 1.7, 3), round(t + 3.0, 3), -aci, piv[0], piv[1]])
    ROT[kn].append([round(t - 0.01, 3), round(t + 3.0, 3), 0.0, piv[0], piv[1]])
    olay(t, '%s: 90° açık, menteşe tarafından yaklaşır → pimlere iner → kapanır' % P[kn]['ac'].split('(')[0].strip())
    t += 3.2; YER[kn] = t; YERINDE.append(kn)
# ---- 21 HAT BAĞLANTISI
adim('Hat bağlantısı', 'Sahada: A (silik) solda — sol yandaki somunlara A içinden bağlanır, X ekseni ray tabanı A kaidesine (A sayfası). F (silik) sağda: 4 cıvata M8 × 16 + küçük pul F içinden sağ yandaki somunlara.',
     'A (silik) · F (silik) · cıvata M8 × 16 × 4 + pul → somun M8')
for a in ('cevre_A', 'cevre_F'): basla(a, np.zeros(3), t); YER[a] = t; YERINDE.append(a)
olay(t, 'A ve F (silik) yerinde'); kamera_genel(['dis_yan_sag'], yon=(0.8, 0.4, 0.5), olcek=0.8); t += 0.8
Fp = sorted(a for a in P if a.startswith('arayuz_m8_F') and a.endswith('_pul')); Fv = sorted(a for a in P if a.startswith('arayuz_m8_F') and not a.endswith('_pul'))
yakin(merkez(Fv[0]), 0.3, yon=(0.85, 0.3, 0.4), tt=t)
for i, (p, v) in enumerate(zip(Fp, Fv)): tak(p, t + i * 0.15, 0.45, 30.0); tak(v, t + 0.3 + i * 0.15, 0.55, 40.0)
olay(t, 'Küçük pul + cıvata M8 × 16 × 4: F içinden → TOPPING sağ yan somunları'); t = bitti() + 0.6
kam(t, ([3.6, 2.7, 2.6], [1.97, 1.3, -0.4]))
TOPLAM = round(bitti() + 2.0, 3)
# ---- sade Türkçe (ham parça adı / kod yok)
SADE = [(r'PEM SP-M(\d)(-\d)?', r'preslenmiş somun M\1'), (r'PEM FHS-M(\d)(-\d)?', r'preslenmiş saplama M\1'), (r'PEM S-M(\d)(-\d)?', r'preslenmiş somun M\1'), (r'PEM saplama', 'preslenmiş saplama'), (r'PEM somun', 'preslenmiş somun'), (r'PEM FHP-M5(-\d+)?', 'preslenmiş saplama M5'), (r"PEM'(ler|lere|in)", r'somun\1'),
        (r'\bPEM\b', 'preslenmiş somun'), (r'ISO 4762 ', 'cıvata '), (r'ISO 7092 ', 'küçük pul '), (r'DIN 7991 ', 'havşa vida '), (r'TEK ÜRÜN', 'hazır ürün'), (r'\bJ1\b', 'fiş paneli'),
        (r'Secop ', ''), (r'\bastar\b', 'iç sac'), (r'\bAstar\b', 'İç sac'), (r'kablo_sinyal', 'bilgi kablosu'), (r'\bkoyu \(iç\)', 'sensör (iç)'), (r'\bcelik \(iç\)', 'çelik braket (iç)'),
        (r'\bkanal \(iç\)', 'kablo kanalı (iç)'), (r'\brakor \(iç\)', 'kablo rakoru (iç)')]
def sade(x):
    for a_, b_ in SADE: x = _re.sub(a_, b_, x)
    return x
for x in ADIM: x['ad'] = sade(x['ad']); x['metin'] = sade(x['metin']); x['liste'] = sade(x['liste'])
OLAY = [[o[0], sade(o[1])] for o in OLAY]
for x in ACN: x['ac'] = sade(x['ac'])
for a in P: P[a]['ac'] = sade(P[a]['ac'])
exec(open(os.path.join(HERE, '_son.py'), encoding='utf-8').read().replace("'plan_a3.pkl'", "'plan_t5.pkl'").replace('OLC = 1.75', 'OLC = 1.0'))
