# -*- coding: utf-8 -*-
"""TOPPING MONTAJ ANİMASYONU v3 — çekmece v3 / B v3 / A v3 yöntemiyle (plan_TOPPING.md) · 4 Eki 2026 · yerel
Girdi: t3_parca.pkl (ajan GLB'si + zincir_T_tamamla), acinim_TOPPING (sac_morf_t) · Çıktı: plan_t3.pkl → t3_cikti.py (denetim + GLB/JSON)
Altyapı (zaman çizelgesi, plan anı yol denetimi, yerleştirici) a3_montaj.py'den birebir (_altyapi.py)."""
import sys, os, json, pickle, math, time, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
import sac_morf_t as SM
T0 = time.time()
D0 = pickle.load(open('t3_parca.pkl', 'rb')); P = D0['P']; ENT = D0['ENT']

# ------------------------------------------------------------------ 1. sac parçaları: açınımdan ağ
SAC = {}
for f in sorted(os.listdir(SM.ACN_DIR)):
    ad = f[:-5]; s = SM.Sac(ad); SAC[ad] = s
    old = P[ad]
    V, F = (s.dunya(s.yerel({})), s.F) if s.bukum else (old['V'], old['F'])
    P[ad] = dict(old, V=V, F=F, model_lo=old['V'].min(0), model_hi=old['V'].max(0))
print('sac', len(SAC))
AD_TR = {'dis_yan_sol': 'Dış yan sol 1,5', 'dis_yan_sag': 'Dış yan sağ 1,5', 'dis_tavan': 'Dış tavan 1,5', 'dis_taban': 'Dış taban 1,5', 'dis_arka_servis': 'Arka servis sacı 1,5',
         'soguk_alt_sac': 'Soğuk oda alt sacı 1,5', 'soguk_arka_dis_sac': 'Soğuk oda arka dış sacı 1,5', 'astar_arka': 'Astar arka 1,0', 'astar_sol': 'Astar sol 1,0', 'astar_sag': 'Astar sağ 1,0',
         'astar_tavan': 'Astar tavan 1,0', 'raf': 'Raf 3,0', 'ust_raf': 'Üst raf 3,0', 'soguk_esik': 'Eşik 1,2', 'on_cerceve_430': 'Ön çerçeve 430 1,0', 'kuru_bolme_tabani': 'Kuru bölme tabanı 1,5',
         'teknik_on_perde': 'Teknik ön perde 1,5', 'teknik_sag_perde': 'Teknik sağ perde 1,5', 'ayirma_perdesi_cep_sol': 'Ayırma perdesi 1,5', 'sogutma_cebi': 'Soğutma cebi 1,5',
         'kaide_ust_plaka_4': 'Kaide plakası 4 mm', 'kaide_on_perde_menfezli': 'Menfezli ön perde C 2,0', 'kaide_enine_lama_6': 'Kaide enine lama 6', 'dil_kanali_kasar': 'Dil kanalı kaşar 1,0',
         'dil_kanali_sucuk': 'Dil kanalı sucuk 1,0', 'raf_kosebendi_sol': 'Raf köşebendi sol 3,0', 'raf_kosebendi_sag': 'Raf köşebendi sağ 3,0', 'ust_raf_kosebendi_sol': 'Üst raf köşebendi sol 3,0',
         'ust_raf_kosebendi_sag': 'Üst raf köşebendi sağ 3,0', 'kaide_cep_tasiyici_0': 'Cep taşıyıcı L (arka)', 'kaide_cep_tasiyici_1': 'Cep taşıyıcı L (ön)'}
BK = {}
def bk(x): return x.replace('_', ' ')
def tr(a):
    if a in AD_TR: return AD_TR[a]
    m = __import__('re').match(r'evap_kanal_kovani_(\d)_L(\d)', a)
    if m: return 'Evaporatör kanal kovanı %s · L%s 1,0' % (m.group(1), m.group(2))
    m = __import__('re').match(r'dusme_kovani_(\w+)_L(\d)', a)
    if m: return 'Düşme kovanı %s · L%s 3,0' % (m.group(1), m.group(2))
    return P[a]['ac'].split('·')[0].strip() if a in P else a
CEVRE = [a for a in P if a.startswith('cevre')]
def kutu(a): return P[a]['V'].min(0), P[a]['V'].max(0)
def merkez(a): l, h = kutu(a); return (l + h) / 2

# ------------------------------------------------------------------ PEM / saplama → sac
PEM_SAC = {}
def pem_bagla(p, s, yan, ad):
    P[p]['sac'] = s; P[p]['yan'] = np.asarray(yan, float); P[p]['pem_ad'] = ad; PEM_SAC.setdefault(s, []).append(p)
for a in list(P):
    if a.startswith('kaide_plaka_pem_M6'): pem_bagla(a, 'kaide_ust_plaka_4', (0, -1.0, 0), 'PEM SP-M6-2')
    elif a.startswith('servis_arka_') and a.endswith('_pem'):
        s = {'yan_sol': 'dis_yan_sol', 'yan_sag': 'dis_yan_sag', 'tavan': 'dis_tavan', 'taban': 'dis_taban'}['_'.join(a.split('_')[2:4]) if a.split('_')[2] == 'yan' else a.split('_')[2]]
        pem_bagla(a, s, (0, 0, 1.0), 'PEM SP-M5-2')
    elif a.startswith('pem_M8_A') and not a.endswith('kapagi'): pem_bagla(a, 'dis_yan_sol', (1.0, 0, 0), 'PEM SP-M8-1')
    elif a.startswith('pem_M8_F'): pem_bagla(a, 'dis_yan_sag', (-1.0, 0, 0), 'PEM SP-M8-1')
    elif a.startswith('cep_takoz_pem'): pem_bagla(a, 'sogutma_cebi', (0, -1.0, 0), 'PEM SP-M8-1')
    elif a.startswith(('arayuz_mek_', 'arayuz_j1_')):
        k = a.split('_')[2]
        s = {'yan': 'dis_yan_sag', 'taban': 'dis_taban', 'arka': 'dis_arka_servis', 'soguk': 'soguk_arka_dis_sac', 'raf': 'raf', 'alt': 'soguk_alt_sac', 'kuru': 'kuru_bolme_tabani', 'burc': 'dis_yan_sag'}[k]
        l, h = kutu(a); e = int(np.argmax(h - l)); ls, hs = kutu(s); cs = (ls[e] + hs[e]) / 2
        yan = np.zeros(3); yan[e] = -1.0 if abs(l[e] - cs) < abs(h[e] - cs) else 1.0      # baş sac tarafında → presleme baş tarafından
        pem_bagla(a, s, yan, 'PEM FHP-M5-25' if '_j1_' in a else 'PEM FHP-M5-12')
        P[a]['eks_sap'] = -yan
print('PEM / saplama', {k: len(v) for k, v in PEM_SAC.items()})
for a in list(P):
    if a.startswith('arayuz_kb_'): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.startswith('arayuz_kaide_M6'): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.startswith('arayuz_m8_F'): P[a]['eks'] = np.array([-1.0, 0, 0])
    elif a.startswith('servis_arka') and a.endswith('_vida'): P[a]['eks'] = np.array([0, 0, 1.0])
    elif a.startswith('percin_somun'): P[a]['eks'] = np.array([0, -1.0, 0])
    elif a.endswith('kopuk_kapagi'): P[a]['eks'] = np.array([-1.0, 0, 0])
    elif a.startswith('pom_burc'): pass

# ------------------------------------------------------------------ 2. animasyonda üretilen punta / TIG işaretleri (modelde dikiş yok · 0,1 mm · beyanlı)
def punta(ad, p, eks, ac):
    V, F = G.mesh(G.silindir(p, eks, 2.0, 0.1, 16)); P[ad] = dict(V=V, F=F, m='kaynak', tur='kaynak', ac=ac, uretilen=True)
PUNTA = collections.OrderedDict()
def punta_dizi(anah, noktalar, eks, ac):
    L_ = []
    for i, p in enumerate(noktalar):
        ad = 'punta_%s_%d' % (anah, i); punta(ad, p, eks, ac); L_.append(ad)
    PUNTA[anah] = L_
# dış kabuk köşe TIG (ön alın yüzünde, z 39,0 → 39,1; kanatlar x 1438'den başlar, çerçeve y 964'ten)
Vt = P['dis_taban']['V']
xl = Vt[(Vt[:, 0] < 1445) & (Vt[:, 1] > 900)][:, 0].max(); xr = Vt[(Vt[:, 0] > 2490) & (Vt[:, 1] > 900)][:, 0].min()
punta_dizi('yan_sol_taban', [(xl, 902.0, z) for z in (-780.0, -600.0)], (1, 0, 0), 'TIG: dış taban yan dönüşü ↔ dış yan sol')
punta_dizi('yan_sag_taban', [(xr - 0.1, 902.0, z) for z in (-780.0, -600.0)], (1, 0, 0), 'TIG: dış taban yan dönüşü ↔ dış yan sağ')
punta_dizi('tavan_yanlar', [(x, 2200.0, z) for x in (1440.0, 2496.0) for z in (-700.0, -300.0, 20.0)], (0, 1, 0), 'TIG: dış tavan ↔ yan saclar (üst köşe)')
# astar iç köşe TIG (soğuk oda içinden, astar yüzlerinde)
punta_dizi('astar_sol', [(1496.0, y, -569.9) for y in (1300.0, 1700.0, 2100.0)], (0, 0, 1), 'TIG: astar sol ↔ astar arka (iç köşe R3)')
punta_dizi('astar_sag', [(2440.0, y, -569.9) for y in (1300.0, 1700.0, 2100.0)], (0, 0, 1), 'TIG: astar sağ ↔ astar arka (iç köşe R3)')
punta_dizi('astar_tavan', [(x, 2139.9, -566.5) for x in (1700.0, 2000.0, 2300.0)] + [(1497.0, 2139.9, z) for z in (-300.0, 0.0)] + [(2439.0, 2139.9, z) for z in (-300.0, 0.0)],
           (0, -1, 0), 'TIG: astar tavan ↔ arka / yan astarlar (iç köşe)')
print('üretilen işaret', sum(len(v) for v in PUNTA.values()))

exec(open(os.path.join(HERE, '_altyapi.py'), encoding='utf-8').read())

# ------------------------------------------------------------------ çevre + beyanlı plan istisnaları
for a in CEVRE:
    if a == 'cevre_B': basla(a, np.zeros(3), 0.0); YER[a] = 0.0; YERINDE.append(a)
for s_, L_ in PEM_SAC.items():
    for p in L_: HARIC_PLAN.add((p, s_))
HARIC_PLAN.add(('pem_M8_A_1300_300_kopuk_kapagi', 'pem_M8_A_1300_300')); HARIC_PLAN.add(('pem_M8_A_2000_300_kopuk_kapagi', 'pem_M8_A_2000_300'))
for b_ in [a for a in P if a.startswith('burc_')]:
    for w_ in ('soguk_arka_dis_sac', 'pu_levha_arka', 'astar_arka', 'yapistirici_arka'): HARIC_PLAN.add((b_, w_)); HARIC_NEDEN[(b_, w_)] = 'POM burç duvar deliğine sıkı geçme (delik Ø = burç Ø; çokgen farkı ≤ 0,4 mm)'
for ad_ in ('kasar', 'sucuk'):
    HARIC_PLAN.add(('motor_' + ad_, 'burc_motor_' + ad_)); HARIC_NEDEN[('motor_' + ad_, 'burc_motor_' + ad_)] = 'kaplin burcun içinden geçer (yuva = kaplin, sıfır boşluk)'
    HARIC_PLAN.add(('motor_' + ad_, 'kaset_' + ad_)); HARIC_NEDEN[('motor_' + ad_, 'kaset_' + ad_)] = 'kaplin kasetin kaplinine geçer (geçme)'
for ad_ in ('kiyma', 'kusbasi', 'sos', 'harc'):
    for b_ in ('burc_uno_' + ad_, 'uno_%s_on' % ad_):
        HARIC_PLAN.add(('uno_%s_arka' % ad_, b_)); HARIC_NEDEN[('uno_%s_arka' % ad_, b_)] = 'piston mili burçtan geçer, ucu pistona vidalanır (sıfır boşluk)'
for k_ in ('sol', 'sag', 'arka', 'tavan'):
    HARIC_PLAN.add(('pu_levha_' + k_, 'yapistirici_' + k_)); HARIC_NEDEN[('pu_levha_' + k_, 'yapistirici_' + k_)] = 'levha yapıştırıcı katmanına bastırılır (yüzey teması)'
for pu_ in ('pu_levha_sol', 'pu_levha_sag', 'pu_levha_arka', 'yapistirici_arka', 'yapistirici_sol', 'yapistirici_sag', 'pu_levha_tavan', 'yapistirici_tavan'):
    HARIC_PLAN.add((pu_, 'dis_tavan')); HARIC_NEDEN[(pu_, 'dis_tavan')] = 'levha üst yüzü dış tavanın alt yüzüne sıfır boşlukla temas (yüzey boyunca kayma)'
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

# ================================================================== PLAN
KAM.append([0.0, [3.4, 2.6, 2.4], [1.97, 1.2, -0.4]])
t = 0.4
# ---- 1 B TAVANI HAZIRLIĞI
adim('B tavanı: perçin somunlar', 'TOPPING, B dolabının (silik) tavanına kurulur. Önce B üst kirişinin deliklerine 4 × M8 kapalı uçlu perçin somun takılır ve perçin tabancasıyla sıkılır (kiriş içinden dişli yuva).',
     'M8 kapalı perçin somun × 4 → B üst kirişi (GFRP + kiriş Ø11)')
PS = sorted(a for a in P if a.startswith('percin_somun'))
yakin(merkez(PS[0]) + np.array([0, 40, 0]), 0.4, tt=t)
t = sira_tak(PS, t, 60.0, 0.6, 0.2); olay(t - 0.6, 'Perçin somun M8 × 4 → B kirişi deliklerine · perçin tabancasıyla sıkılır'); t += 0.6
# ---- 2 KAİDE ÇERÇEVESİ
adim('Kaide çerçevesi', 'Kaide 304 dikdörtgen borudan (kesim boyunda): arka boru (100 × 40), sol / sağ / enine boru (40 × 100), aralarına 3 boyuna boru ve 6 mm enine lama. Uçlar karşı boruya TIG köşe dikişiyle kaynaklanır.',
     'arka boru · sol / sağ / enine boru · boyuna boru × 3 · enine lama 6 · TIG köşe dikişi × 14')
kamera_genel(['kaide_arka_boru', 'kaide_sol_boru', 'kaide_sag_boru'], yon=(0.45, 0.75, 0.75), olcek=0.7)
t = koy('kaide_arka_boru', [UST], 'Kaide arka boru (100 × 40 × 2, kesim boyu 1064) → B tavanı üstüne', sure_bekle=0.1)
for a in ('kaide_sol_boru', 'kaide_sag_boru', 'kaide_enine_boru'):
    koy(a, [UST], '%s ↔ arka boru: TIG köşe dikişi' % tr(a).capitalize(), grup_kaynak=KAY(a + '_kaynak_arka'), sure_bekle=0.05)
t = bitti() + 0.2
yakin(merkez('kaide_sol_boru_kaynak_arka_0'), 0.35, yon=(0.5, 0.75, 0.45), tt=t - 0.6)
koy('kaide_enine_lama_6', [UST], 'Enine lama 6 mm → arka boru ile ön perde arasına')
for a in ('kaide_boyuna_boru_1', 'kaide_boyuna_boru_2', 'kaide_boyuna_boru_3'):
    koy(a, [UST], '%s ↔ yan / enine boru: TIG köşe dikişi' % tr(a).capitalize(), grup_kaynak=KAY(a + '_kaynak'), sure_bekle=0.05)
t = bitti() + 0.5
# ---- 3 KAİDE PLAKASI + PERDE + CEP TAŞIYICI
adim('Kaide: cep taşıyıcı, ön perde, plaka', 'İki cep taşıyıcı L (3 mm, lazer → 1 büküm) borulara oturur; menfezli ön perde C (2 mm, lazer → 2 büküm) önden boruların uçlarına; 4 mm kaide plakası lazerde kesilir, altından 2 × PEM SP-M6 preslenir, borulara iner ve 17 delik kaynağıyla bağlanır.',
     'cep taşıyıcı L × 2 · menfezli ön perde C · kaide plakası 4 mm · PEM SP-M6 × 2 · delik kaynağı × 17')
kamera_genel(['kaide_cep_tasiyici_0', 'kaide_cep_tasiyici_1'], yon=(0.4, 0.8, 0.6), olcek=0.9)
for a in ('kaide_cep_tasiyici_0', 'kaide_cep_tasiyici_1'): t = koy(a, [UST], '%s → borular arasına (uç punta)' % tr(a))
kamera_genel(['kaide_on_perde_menfezli'], yon=(0.3, 0.45, 0.9), olcek=0.9)
t = koy('kaide_on_perde_menfezli', [ON, UST], 'Menfezli ön perde C → boruların ön uçlarına (punta)')
kamera_genel(['kaide_ust_plaka_4'], yon=(0.4, 0.8, 0.7), olcek=0.8)
t = koy('kaide_ust_plaka_4', [YOL((0, 420, 0))], 'Kaide plakası → borular (PEM\'ler altta)', pem=sorted(PEM_SAC['kaide_ust_plaka_4']))
yakin(merkez('kaide_ust_plaka_delik_kaynagi_0'), 0.42, yon=(0.35, 0.85, 0.4), tt=t - 0.2)
for k in KAY('kaide_ust_plaka_delik_kaynagi'): buyu(k, t, 0.6)
olay(t, 'Delik kaynağı × 17: plaka yarıkları ↔ kaide boruları (TIG, yüz taşlanır)'); t += 1.0
# ---- 4 TOPPING → B
adim('TOPPING → B bağlantısı', '4 × ISO 4762 M8 × 25 + ISO 7092 M8 pul (Ø15) kaide plakası ve boru üst duvarındaki Ø16 servis deliğinden boru içine iner; baş boru alt duvarına oturur, cıvata B dış tavanından (Ø9) ve GFRP pedden geçip kirişteki perçin somuna girer.',
     'ISO 4762 M8 × 25 × 4 · ISO 7092 M8 pul × 4 → B kirişi M8 perçin somun')
KBp = sorted(a for a in P if a.startswith('arayuz_kb_') and a.endswith('_pul')); KBv = sorted(a for a in P if a.startswith('arayuz_kb_') and not a.endswith('_pul'))
yakin(merkez(KBv[0]) + np.array([0, 60, 0]), 0.42, tt=t)
for i, (p, v) in enumerate(zip(KBp, KBv)): tak(p, t + i * 0.15, 0.6, 130.0); tak(v, t + 0.35 + i * 0.15, 0.7, 140.0)
olay(t, 'Pul ISO 7092 M8 (Ø15) + ISO 4762 M8 × 25: Ø16 servis deliğinden → boru alt duvarı Ø9 → B dış tavanı → perçin somun (alyan 6)')
t = bitti() + 0.5
# ---- 5 DIŞ TABAN
adim('Dış taban', 'Dış taban (1,5 mm) lazerde kesilir, abkantta 3 kenarı yukarı bükülür; arka dönüşe servis sacı için 4 × PEM SP-M5, mekanizma için 4 × PEM FHP-M5 preslenir. Kaide plakasına iner; 2 × ISO 4762 M6 × 12 tabandan plakadaki PEM SP-M6\'ya.',
     'dış taban · 3 büküm · PEM SP-M5 × 4 · PEM FHP-M5 × 4 · ISO 4762 M6 × 12 × 2 → PEM SP-M6')
kamera_genel(['dis_taban'], yon=(0.45, 0.8, 0.65), olcek=0.8)
t = koy('dis_taban', [YOL((0, 450, 0))], 'Dış taban → kaide plakası', pem=sorted(PEM_SAC['dis_taban']))
def AD(*yon, lift=(20, 40, 120, 300, 500), yan=(30, -30)):
    """aday yollar: her ana yön için düz, sonra kaldırılmış (önce yukarıda gelir, sonra iner) ve yandan kaydırılmış"""
    L_ = []
    for d in yon: L_.append(YOL(d))
    for d in yon:
        for h in lift: L_.append(YOL(d, (0, h, 0)))
        for x in yan: L_.append(YOL(d, (x, 0, 0)))
    return L_
ON9, ARKA9, UST6 = (0, 0, 900), (0, 0, -900), (0, 600, 0)
# ---- 6 DIŞ YAN SAĞ
adim('Dış yan sağ', 'Sağ yan sac (F tarafı, J1 ağzı) lazerde kesilir, abkantta 1 büküm; 4 × PEM SP-M8 (F bağlantısı), 6 × PEM SP-M5 (servis), 2 × FHP-M5-25 (J1) ve 4 × FHP-M5 preslenir. Dış tabanın yan dönüşüne oturur, içeriden TIG.',
     'dış yan sağ · 1 büküm · 16 PEM / saplama · TIG')
kamera_genel(['dis_yan_sag', 'dis_taban'], yon=(0.6, 0.45, 0.65), olcek=0.75)
t = koy('dis_yan_sag', AD((700, 0, 0), UST6), 'Dış yan sağ → dış tabanın yan dönüşüne (TIG)', pem=sorted(PEM_SAC['dis_yan_sag']), grup_kaynak=PUNTA['yan_sag_taban'])
# ---- 7 KURU BÖLME + SOĞUTMA GRUBU
adim('Kuru bölme + soğutma grubu', 'Soğutma cebi (lazer → 3 büküm → 4 × PEM SP-M8) taban ağzından cep taşıyıcılara iner; soğutma grubu (Secop, TEK ÜRÜN) arkadan yukarıda gelir, cebe iner, 4 silikon takoz PEM\'lere; kondenser kanalı braketiyle taban saplamalarına. Ayırma perdesi, teknik ön / sağ perde, kuru bölme tabanı (2 büküm + 5 × FHP-M5) üstlerine; birleşimler punta.',
     'soğutma cebi + 4 PEM · soğutma grubu + 4 takoz · kondenser kanalı · ayırma perdesi · teknik perde × 2 · kuru bölme tabanı + 5 FHP')
kamera_genel(['sogutma_cebi', 'teknik_on_perde'], yon=(0.35, 0.6, -0.75), olcek=0.8)
t = koy('sogutma_cebi', AD(ARKA9, UST6), 'Soğutma cebi → cep taşıyıcılara (punta)', pem=sorted(PEM_SAC['sogutma_cebi']))
for a in ('sogutma_grubu',): t = koy(a, AD(ARKA9, UST6), '%s → arkadan, cebe iner' % P[a]['ac'].split('(')[0].strip())
for a in ('ayirma_perdesi_cep_sol', 'teknik_on_perde', 'teknik_sag_perde'): t = koy(a, AD(ARKA9, UST6, ON9), '%s → yerine (punta)' % tr(a))
M6 = sorted(a for a in P if a.startswith('arayuz_kaide_M6'))
yakin(merkez(M6[0]), 0.3, yon=(0.4, 0.8, 0.5), tt=t)
t = sira_tak(M6, t, 40.0, 0.55, 0.25); olay(t - 0.5, 'ISO 4762 M6 × 12 × 2: teknik perde deliğinden → dış taban Ø6,6 → kaide plakası PEM SP-M6'); t += 0.5
t = koy('kondenser_kanali', AD(ARKA9), 'Kondenser kanalı → arkadan, braketi taban saplamalarına')
t = koy('kuru_bolme_tabani', AD(UST6, ARKA9, lift=(300, 500)), 'Kuru bölme tabanı → yukarıdan, perdelerin üstüne (punta)', pem=sorted(PEM_SAC['kuru_bolme_tabani']))
# ---- 8 SOĞUK ODA ARKA DUVARI
adim('Soğuk oda: taban + arka duvar', 'Soğuk oda alt sacı (2 × FHP-M5) ve arka dış sacı (12 × FHP-M5, kanal ağızları açık) yerine girer; 4 evaporatör kanal kovanı (iki L + boyuna TIG) ağızlara; arka duvara 3 POM geçiş bloğu ve 6 POM duvar burcu (UNO pistonları + kaset motorları); ölçüsünde kesilmiş PU arka levhası önden kovanların ve burçların üstünden geçer, astar arka (1,0) üstüne kapanır.',
     'alt sac · arka dış sac · 4 kanal kovanı · POM geçiş bloğu × 3 · POM duvar burcu × 6 · PU levha arka · astar arka')
kamera_genel(['soguk_alt_sac', 'soguk_arka_dis_sac'], yon=(0.35, 0.5, 0.85), olcek=0.75)
t = koy('soguk_alt_sac', AD(ON9, ARKA9, UST6), 'Soğuk oda alt sacı → teknik perdelerin üstüne (punta)', pem=sorted(PEM_SAC['soguk_alt_sac']))
t = koy('soguk_arka_dis_sac', AD(ARKA9, ON9, UST6), 'Soğuk oda arka dış sacı → alt sac + yanlar (punta)', pem=sorted(PEM_SAC['soguk_arka_dis_sac']))
for k in range(4):
    for j in (1, 2):
        koy('evap_kanal_kovani_%d_L%d' % (k, j), AD(ON9), '%s → arka dış sacın ağzına' % tr('evap_kanal_kovani_%d_L%d' % (k, j)),
            grup_kaynak=(KAY('evap_kanal_kovani_%d_boyuna_kaynak' % k) if j == 2 else ()), sure_bekle=0.05)
    t += 0.4
t = bitti() + 0.2
for a in sorted(a for a in P if a.startswith('pom_gecis')): koy(a, AD(ON9, ARKA9), '%s → arka duvara' % P[a]['ac'].split('(')[0].strip(), sure_bekle=0.05)
t = bitti() + 0.3
kamera_genel(['pu_levha_arka', 'astar_arka'], yon=(0.25, 0.4, 0.9), olcek=0.7)
buyu('yapistirici_arka', t, 0.6); olay(t, 'Yapıştırıcı (YEŞİL) → arka dış sacın iç yüzüne'); t += 0.8
t = koy('pu_levha_arka', AD(ON9), 'PU levha arka (ölçüsünde kesilmiş) → yapıştırıcıya bastırılır')
t = koy('astar_arka', AD(ON9), 'Astar arka 1,0 → levhanın önüne')
for a in ('evaporator_L', 'evaporator_R'): t = koy(a, AD(ARKA9), '%s → arkadan kanal kovanı ağzına (conta arka dış saca)' % P[a]['ac'].split('(')[0].strip())
# ---- 9 DIŞ YAN SOL + TAVAN
adim('Dış yan sol + dış tavan', 'Sol yan (A tarafı): lazer → 1 büküm → 4 × PEM SP-M8 (A) + 2 × PEM SP-M5 → tabanın yan dönüşüne, içeriden TIG; A tarafındaki 2 PEM\'in iç yüzüne köpük kapağı. Dış tavan: lazer → 3 büküm → 5 × PEM SP-M5 → yan sacların üstüne, TIG.',
     'dış yan sol + 6 PEM · köpük kapağı × 2 · dış tavan + 5 PEM · TIG')
kamera_genel(['dis_yan_sol', 'dis_taban'], yon=(-0.6, 0.45, 0.65), olcek=0.75)
t = koy('dis_yan_sol', AD((-700, 0, 0), UST6), 'Dış yan sol → dış tabanın yan dönüşüne (TIG)', pem=sorted(PEM_SAC['dis_yan_sol']), grup_kaynak=PUNTA['yan_sol_taban'])
KK = sorted(a for a in P if a.endswith('kopuk_kapagi'))
yakin(merkez(KK[0]), 0.3, yon=(0.8, 0.3, 0.5), tt=t)
for i, a in enumerate(KK): tak(a, t + i * 0.2, 0.5, 40.0)
olay(t, 'Köpük kapağı × 2 → A tarafı PEM SP-M8\'lerin iç yüzüne'); t = bitti() + 0.3
kamera_genel(['dis_tavan', 'dis_yan_sol'], yon=(0.45, 0.85, 0.6), olcek=0.75)
t = koy('dis_tavan', AD(UST6), 'Dış tavan → yan sacların üstüne (TIG)', pem=sorted(PEM_SAC['dis_tavan']), grup_kaynak=PUNTA['tavan_yanlar'])
# ---- 10 YALITIM + ASTAR (sol, sağ, tavan)
adim('Yalıtım levhaları + astar', 'Yüzey yüzey: ölçüsünde kesilmiş PU levha (delikleri ve cepleri açılmış) önden girer, dış saca yaslanır; hemen önüne o yüzün astar sacı (1,0) kapanır ve iç köşede astar arkaya TIG ile bağlanır. Sıra: sol → sağ → tavan. Raf askı burçları (POM) astar ve levha deliklerinden içeriden.',
     'yapıştırıcı · PU levha + astar (sol, sağ, tavan) · iç köşe TIG · POM burç × 16 · derz silikonu')
for pu, ast, d in (('pu_levha_sol', 'astar_sol', 80), ('pu_levha_sag', 'astar_sag', -80), ('pu_levha_tavan', 'astar_tavan', 0)):
    kamera_genel([pu, ast], yon=(0.25, 0.4, 0.9), olcek=0.7)
    yp = ([YOL(ON9, (d, 0, 0))] if d else []) + AD(ON9)
    yk = 'yapistirici_' + pu.split('_')[-1]; buyu(yk, t, 0.6); olay(t, 'Yapıştırıcı (YEŞİL) → dış sacın iç yüzüne'); t += 0.8
    t = koy(pu, yp, '%s → yapıştırıcıya bastırılır' % P[pu]['ac'].split('(')[0].strip())
    t = koy(ast, AD(ON9) + yp, '%s → levhanın önüne · iç köşe TIG' % tr(ast), grup_kaynak=PUNTA[ast])
t += 0.3
kamera_genel(['astar_sol'], yon=(0.6, 0.4, 0.75), olcek=0.8)
BURC = sorted(a for a in P if a.startswith('pom_burc'))
for i, a in enumerate(BURC):
    e_ = np.asarray(P[a]['eks'], float); t_ = t + i * 0.08
    basla(a, -e_ * 80.0, t_); git(a, np.zeros(3), t_, 0.5); vurgu([a], t_ + 0.3, t_ + 1.2); YER[a] = t_ + 0.5; YERINDE.append(a)
olay(t, 'Raf askı burcu POM × 16 → astar + levha deliklerinden içeriden (sıkı geçme)'); t = bitti() + 0.5
buyu('derz_silikonu', t, 0.8); olay(t, 'Derz silikonu (YEŞİL) → gıda tarafı iç köşeler'); t += 1.0
# ---- 11 RAF
adim('Raf, kovanlar, eşik', 'Raf köşebentleri ve 6 düşme kovanı (kıyma / kuşbaşı iki L + TIG, sos / harç boru, kaşar / sucuk POM) alt saca; PU raf levhası yukarıdan kovanların üstünden iner; raf (3 mm, lazer → 4 büküm → 4 × FHP-M5) levhanın üstüne kapanır, arka köşe dolgu kaynağı. Dil kanalları, eşik (3 büküm), yiv dolguları + köşe silikonu.',
     'raf köşebendi × 2 · düşme kovanı × 6 · PU raf levhası · raf + 4 FHP · dil kanalı × 2 · eşik · yiv dolgusu × 10 · silikon × 8')
kamera_genel(['raf', 'raf_kosebendi_sol'], yon=(0.35, 0.7, 0.75), olcek=0.75)
for a in ('raf_kosebendi_sol', 'raf_kosebendi_sag'): koy(a, AD(ON9, UST6), '%s → alt saca (punta)' % tr(a))
t = bitti()
for a in ('dusme_kovani_kiyma_L1', 'dusme_kovani_kiyma_L2', 'dusme_kovani_kusbasi_L1', 'dusme_kovani_kusbasi_L2'):
    koy(a, AD(ON9, UST6), '%s → alt sacın deliğine' % tr(a), grup_kaynak=(KAY(a[:-3] + '_boyuna_kaynak') if a.endswith('L2') else ()), sure_bekle=0.05)
for a in ('dusme_kovani_sos', 'dusme_kovani_harc', 'dusme_kovani_kasar', 'dusme_kovani_sucuk'):
    koy(a, AD(ON9, UST6), '%s → alt sacın deliğine' % P[a]['ac'].split('·')[0].strip(), sure_bekle=0.05)
t = bitti() + 0.2
t = koy('pu_raf_esik', AD(UST6, ON9, lift=(100, 300, 500)), 'PU raf levhası → kovanların üstünden alt saca')
t = koy('raf', AD(UST6, ON9, lift=(60, 100, 300, 500)), 'Raf → PU levhanın üstüne, kenarları köşebentlere (punta)', pem=sorted(PEM_SAC['raf']), grup_kaynak=KAY('raf_arka_kose_dolgusu'))
kamera_genel(['soguk_esik', 'dil_kanali_kasar'], yon=(0.3, 0.6, 0.9), olcek=0.7)
for a in ('dil_kanali_kasar', 'dil_kanali_sucuk'): t = koy(a, AD(ON9, UST6), '%s → rafın kesiğine' % tr(a))
t = koy('soguk_esik', AD(ON9, UST6), 'Eşik → rafın ön kenarına', grup_kaynak=KAY('raf_esik_yiv') + KAY('esik_on_yiv'))
for k in sorted(a for a in P if a.startswith('dil_kesik_kose_silikonu')): buyu(k, t, 0.4)
olay(t, 'Yiv dolgusu TIG + taşlama × 10 · eşik kesiği köşe silikonu × 8'); t += 0.9
# ---- 12 SOĞUTMA + MOTORLAR + UNO ARKA
adim('Soğutma hatları', 'Bakır hatlar (emiş + sıvı, lehimli) ve yoğuşma hortumu soğutma grubu ile evaporatörler arasında yerinde uzar.', 'bakır hatlar · yoğuşma hortumu')
kamera_genel(['evaporator_L', 'evaporator_R'], yon=(0.35, 0.45, -0.85), olcek=0.8)

for a in ('bakir_hat', 'yogusma_hortumu'): buyu(a, t, 1.0)
olay(t, 'Bakır hatlar (lehim) + yoğuşma hortumu: grup ↔ evaporatörler'); t += 1.4
# ---- 13 HAVA + ELEKTRİK İÇ
adim('Valf adası, hava kanalı, iç kanallar, J1', 'Hava kanalı askıları arka dış sacın ve kuru tabanın FHP-M5 saplamalarına, hava kanalları üstlerine; valf adası (12 valf, TEK ÜRÜN). İç kablo kanalları ve braketler; J1 gömme fiş paneli sağ yandaki FHP-M5-25 saplamalarına içeriden. Hava hortumları ve kablolar kanal boyunca uzar.',
     'hava askısı × 13 · hava kanalı × 3 · valf adası · iç kanallar · J1 paneli · hortumlar · kablolar')
kamera_genel(['valf_adasi', 'hava_kanal_2014_1259'], yon=(0.35, 0.45, -0.85), olcek=1.0)
for a in sorted(a for a in P if a.startswith('hava_aski')): koy(a, AD(ARKA9), 'Hava askısı → FHP-M5 saplamaya', sure_bekle=0.03)
t = bitti()
for a in sorted(a for a in P if a.startswith('hava_kanal')): t = koy(a, AD(ARKA9), 'Hava kanalı → askılara')
t = koy('valf_adasi', AD(ARKA9), 'Valf adası → arkadan')
for a in sorted(a for a in P if a.startswith('elk_')): koy(a, AD(ARKA9, ON9), '%s → yerine' % P[a]['ac'], sure_bekle=0.03)
t = bitti()
t = koy('j1_panel', [YOL((0, 0, -500), (-60, 0, 0))] + AD(ARKA9), 'J1 gömme fiş paneli → sağ yanın FHP-M5-25 saplamalarına (içeriden)')
for a in ('hava_hortum', 'hava_giris', 'j1_kablo', 'kablo_guc', 'kablo_bilgi'): buyu(a, t, 1.0)
olay(t, 'Hava hortumları (YEŞİL) · güç (KIRMIZI) / bilgi (MAVİ) kabloları kanal boyunca'); t += 1.4
# ---- UNO ÖN + KASET + ÜST RAF + ÇERÇEVE
adim('UNO\'lar, kasetler, üst raf', 'Kaset rayları raf saplamalarına. Kıyma ve kuşbaşı UNO ön grubu (hazne + dozaj gövdesi + döner valf, içinde piston) önden yukarıda gelir, rafa iner; üst raf (2 büküm) köşebentlerine; sos ve harç UNO ön grubu üst raf deliğinden iner. Kaşar / sucuk kaseti (TEK ÜRÜN) rayından sürülür. Çıkış ağızları tabla açıklığından kovanlara. Arkadan: 6 POM duvar burcu, kaset motorları (kaplin kasete geçer) ve UNO arka grupları (silindir + mil; mil burçtan geçip pistona vidalanır). Ön çerçeve 430 köpük boşluğunu kapatır.',
     'kaset rayı × 2 · UNO ön grubu × 4 · üst raf + 2 köşebent · kaşar / sucuk kaseti · çıkış ağzı × 6 · POM duvar burcu × 6 · kaset motoru × 2 · UNO arka grubu × 4 · ön çerçeve 430')
kamera_genel(['uno_kiyma_on', 'uno_sos_on', 'kaset_kasar'], yon=(0.3, 0.45, 0.9), olcek=0.9)
ALT = [YOL((0, 0, 700), (0, -150, 0)), YOL((0, 0, 700), (0, -120, 0)), YOL((0, -150, 0))]
INIS = dict(lift=(110, 120, 130, 140), yan=())
for ad in ('kasar', 'sucuk'): t = koy('kaset_ray_' + ad, AD(ON9, lift=(15, 20, 30)), '%s → raf saplamalarına' % P['kaset_ray_' + ad]['ac'].split('(')[0].strip())
for ad in ('kiyma', 'kusbasi'):
    t = koy('uno_%s_on' % ad, AD(ON9, **INIS), 'UNO %s ön grubu → önden yukarıda gelir, rafa ve kovana iner' % ad)
kamera_genel(['ust_raf'], yon=(0.3, 0.5, 0.9), olcek=0.8)
for a in ('ust_raf_kosebendi_sol', 'ust_raf_kosebendi_sag'): koy(a, AD(ON9), '%s → yan astarlara (punta)' % tr(a))
t = bitti()
t = koy('ust_raf', AD(ON9, lift=(20, 40)), 'Üst raf → köşebentlere (punta)')
for ad in ('sos', 'harc'):
    t = koy('uno_%s_on' % ad, AD(ON9, **INIS), 'UNO %s ön grubu → üst raf deliğinden rafa iner' % ad)
for ad in ('kasar', 'sucuk'):
    t = koy('kaset_' + ad, AD(ON9, lift=(5, 10)), '%s → rayından sürülür' % P['kaset_' + ad]['ac'].split('(')[0].strip())
for ad in ('harc',):
    t = koy('uno_%s_cikis' % ad, ALT, 'UNO %s çıkış ağzı + yayıcı → raf kovanına (alttan)' % ad)
for ad in ('kasar', 'sucuk'):
    t = koy('kaset_%s_cikis' % ad, ALT, '%s → kovana (alttan)' % P['kaset_%s_cikis' % ad]['ac'].split('(')[0].strip())
kamera_genel(['motor_kasar', 'uno_kiyma_arka', 'uno_sos_arka'], yon=(0.35, 0.45, -0.85), olcek=0.9)
for a in sorted(a for a in P if a.startswith('burc_')): koy(a, AD(ARKA9), '%s → arkadan duvar deliğine (sıkı geçme)' % P[a]['ac'].split('(')[0].strip(), sure_bekle=0.05)
t = bitti() + 0.2
for a in ('motor_kasar', 'motor_sucuk', 'uno_kiyma_arka', 'uno_kusbasi_arka', 'uno_sos_arka', 'uno_harc_arka'):
    t = koy(a, AD(ARKA9), '%s → arkadan, burçtan geçer' % P[a]['ac'].split('(')[0].strip())
kamera_genel(['on_cerceve_430'], yon=(0.3, 0.4, 0.9), olcek=0.75)
t = koy('on_cerceve_430', AD(ON9), 'Ön çerçeve 430 → soğuk oda önü (punta)') + 0.3
# ---- 14 SERVİS SACI ALT MONTAJI (havada, arkada)
adim('Arka servis sacı alt montajı', 'Arka servis sacı (1,5 mm, lazer, büküm yok) 9 × FHP-M5 ile preslenir; pano kutusu, DIN plakası, sürücü kartları, kanallar ve kapak sacın saplamalarına havada (arkada) takılır.',
     'servis sacı + FHP-M5 × 9 · pano + DIN + kartlar + kanallar (hazır)')
OFS_SV = np.array([0, 0, -700.0])
kamera_genel(['dis_arka_servis'], yon=(0.4, 0.4, -0.85), olcek=1.0, ofs=OFS_SV)
SV_PEM = sorted(PEM_SAC['dis_arka_servis'])
s_ = SAC['dis_arka_servis']
basla('dis_arka_servis', OFS_SV, t); olay(t, 'Arka servis sacı · LAZER: düz levha %.0f × %.0f mm (kontur + delikler)' % (s_.levha['boy'], s_.levha['en']))
ACN.append(dict(ad='dis_arka_servis', ac='Arka servis sacı 1,5', t=s_.t, t0=round(t, 3), t1=round(t + 1.0, 3), levha=[s_.levha['boy'], s_.levha['en']], bukum=[]))
for p in SV_PEM: basla(p, OFS_SV + np.asarray(P[p]['yan']) * 30.0, t + 0.45); git(p, OFS_SV, t + 0.45, 0.45); vurgu([p], t + 0.75, t + 1.4)
olay(t + 0.45, 'Arka servis sacı · PEM presleme: %d × PEM FHP-M5-12' % len(SV_PEM)); t += 1.2
basla('servis_cihaz', OFS_SV + np.array([0, 0, 250.0]), t); git('servis_cihaz', OFS_SV, t, 0.9); vurgu(['servis_cihaz'], t + 0.7, t + 1.6)
olay(t, 'Pano kutusu + DIN plakası + sürücü kartları + kanallar → servis sacının saplamalarına (havada)'); t += 1.4
# ---- 16 SERVİS SACI KAPANIR
adim('Arka servis sacı kapanır', 'Servis sacı alt montajıyla birlikte arkadan gelir; 17 × DIN 7991 M5 × 6 havşa vida yan, tavan ve taban dönüşlerindeki PEM SP-M5\'lere. Bakımda sac tek parça çıkar.',
     'servis sacı alt montajı · DIN 7991 M5 × 6 × 17')
SVG = ['dis_arka_servis', 'servis_cihaz'] + SV_PEM
kamera_genel(['dis_arka_servis'], yon=(0.4, 0.4, -0.85), olcek=0.95)
for a in SVG: git(a, np.zeros(3), t, 1.6)
olay(t, 'Servis sacı alt montajı arkadan yerine'); t += 1.7
for a in SVG: YER[a] = t; YERINDE.append(a)
SVV = sorted(a for a in P if a.startswith('servis_arka') and a.endswith('_vida'))
t = sira_tak(SVV, t, 30.0, 0.45, 0.08); olay(t - 1.0, 'DIN 7991 M5 × 6 × 17 → dönüşlerdeki PEM SP-M5'); t += 0.5
# ---- 17 X EKSENİ + KAPAKLAR
adim('X ekseni + kapaklar', 'X ekseni ünitesi (ray + araba + bantlı tabla + motor, TEK ÜRÜN) önden tabla açıklığına sürülür. Ön alt braket, orta kayıt, gizli menteşe gövdeleri ve bas-aç mandalları ön kasaya; kanatlar K1 / K2 havada 90° açık, menteşe tarafından yaklaşır, pimlere iner ve kapanır.',
     'X ekseni · ön alt braket · orta kayıt · menteşe × 6 · bas-aç × 4 · kanat K1 / K2')
kamera_genel(['x_ekseni'], yon=(0.3, 0.45, 0.9), olcek=0.75)
t = koy('x_ekseni', AD(ON9, lift=(-10, -12, -15, -20, 5, 10)), 'X ekseni ünitesi → tabla açıklığına')
t = koy('on_alt_braket', [ON, YOL((0, 0, 300), (0, 30, 0))], 'Ön alt braket → taban saplamalarına')
t = koy('orta_kayit', [ON, YOL((0, 0, 300), (0, 20, 0))], 'Orta kayıt → raf önü')
for a in sorted(a for a in P if a.startswith(('mentese_', 'basac_'))): koy(a, [YOL((0, 0, 80))], '%s → ön kasaya' % P[a]['ac'].split('(')[0].strip(), sure_bekle=0.03)
t = bitti() + 0.3
kam(t, ([1.0, 2.6, 3.6], [1.97, 1.4, 0.2]))
KAPGRUP = []
for kn, piv, aci in (('kanat_K1', (1.438, 0.079), -90.0), ('kanat_K2', (2.497, 0.079), 90.0)):
    basla(kn, np.array([0, 25.0, 300.0]), t); KAPGRUP.append(kn)
    ROT[kn] = [[round(t - 0.01, 3), round(t, 3), aci, piv[0], piv[1]]]
    git(kn, np.array([0, 25.0, 0]), t, 1.0); git(kn, np.zeros(3), t + 1.1, 0.5)
    ROT[kn].append([round(t + 1.7, 3), round(t + 3.0, 3), -aci, piv[0], piv[1]])
    ROT[kn].append([round(t - 0.01, 3), round(t + 3.0, 3), 0.0, piv[0], piv[1]])
    olay(t, '%s: 90° açık, menteşe tarafından yaklaşır → pimlere iner → kapanır' % P[kn]['ac'].split('(')[0].strip())
    t += 3.2; YER[kn] = t; YERINDE.append(kn)
# ---- 18 HAT BAĞLANTISI
adim('Hat bağlantısı', 'Sahada: A (silik) solda — A, sol yandaki PEM SP-M8\'lere A içinden bağlanır (A sayfası). F (silik) sağda: 4 × ISO 4762 M8 × 16 + pul F içinden sağ yandaki PEM SP-M8\'lere.',
     'A (silik) · F (silik) · ISO 4762 M8 × 16 × 4 + pul → PEM SP-M8')
for a in ('cevre_A', 'cevre_F'): basla(a, np.zeros(3), t); YER[a] = t; YERINDE.append(a)
olay(t, 'A ve F (silik) yerinde'); kamera_genel(['dis_yan_sag'], yon=(0.8, 0.4, 0.5), olcek=0.8); t += 0.8
Fp = sorted(a for a in P if a.startswith('arayuz_m8_F') and a.endswith('_pul')); Fv = sorted(a for a in P if a.startswith('arayuz_m8_F') and not a.endswith('_pul'))
for a in Fp + Fv: P[a]['eks'] = np.array([-1.0, 0, 0])
yakin(merkez(Fv[0]), 0.3, yon=(0.85, 0.3, 0.4), tt=t)
for i, (p, v) in enumerate(zip(Fp, Fv)): tak(p, t + i * 0.15, 0.45, 30.0); tak(v, t + 0.3 + i * 0.15, 0.55, 40.0)
olay(t, 'Pul + ISO 4762 M8 × 16 × 4: F içinden → TOPPING sağ yan PEM SP-M8'); t = bitti() + 0.6
kam(t, ([3.6, 2.7, 2.6], [1.97, 1.3, -0.4]))
TOPLAM = round(bitti() + 2.0, 3)
exec(open(os.path.join(HERE, '_son.py'), encoding='utf-8').read().replace("'plan_a3.pkl'", "'plan_t3.pkl'").replace('OLC = 1.75', 'OLC = 1.0'))
