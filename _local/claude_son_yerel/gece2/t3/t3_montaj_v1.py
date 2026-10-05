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
punta_dizi('yan_sol_taban', [(1436.75, y, 39.0) for y in (897.0, 905.0)], (0, 0, 1), 'TIG: dış yan sol ↔ dış taban (köşe)')
punta_dizi('yan_sag_taban', [(2499.25, y, 39.0) for y in (897.0, 905.0)], (0, 0, 1), 'TIG: dış yan sağ ↔ dış taban (köşe)')
punta_dizi('tavan_yanlar', [(x, 2199.0, z) for x in (1440.0, 2496.0) for z in (-700.0, -300.0, 20.0)], (0, 1, 0), 'TIG: dış tavan ↔ yan saclar (üst köşe)')
# astar iç köşe TIG (soğuk oda içinden, astar yüzlerinde)
punta_dizi('astar_sol', [(1496.0, y, -569.9) for y in (1300.0, 1700.0, 2100.0)], (0, 0, 1), 'TIG: astar sol ↔ astar arka (iç köşe R3)')
punta_dizi('astar_sag', [(2440.0, y, -569.9) for y in (1300.0, 1700.0, 2100.0)], (0, 0, 1), 'TIG: astar sağ ↔ astar arka (iç köşe R3)')
punta_dizi('astar_tavan', [(x, 2139.9, -569.0) for x in (1700.0, 2000.0, 2300.0)] + [(1497.0, 2139.9, z) for z in (-300.0, 0.0)] + [(2439.0, 2139.9, z) for z in (-300.0, 0.0)],
           (0, -1, 0), 'TIG: astar tavan ↔ arka / yan astarlar (iç köşe)')
print('üretilen işaret', sum(len(v) for v in PUNTA.values()))

exec(open(os.path.join(HERE, '_altyapi.py'), encoding='utf-8').read())

# ------------------------------------------------------------------ çevre + beyanlı plan istisnaları
for a in CEVRE:
    if a == 'cevre_B': basla(a, np.zeros(3), 0.0); YER[a] = 0.0; YERINDE.append(a)
for s_, L_ in PEM_SAC.items():
    for p in L_: HARIC_PLAN.add((p, s_))
HARIC_PLAN.add(('pem_M8_A_1300_300_kopuk_kapagi', 'pem_M8_A_1300_300')); HARIC_PLAN.add(('pem_M8_A_2000_300_kopuk_kapagi', 'pem_M8_A_2000_300'))
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
M6 = sorted(a for a in P if a.startswith('arayuz_kaide_M6'))
yakin(merkez(M6[0]), 0.3, yon=(0.4, 0.8, 0.5), tt=t)
t = sira_tak(M6, t, 40.0, 0.55, 0.25); olay(t - 0.5, 'ISO 4762 M6 × 12 × 2: dış taban Ø6,6 → kaide plakası PEM SP-M6'); t += 0.5
# ---- 6 DIŞ YAN + TAVAN
adim('Dış kabuk: yanlar + tavan', 'Sol yan (A tarafı): lazer → 1 büküm → 4 × PEM SP-M8 (A bağlantısı) + 2 × PEM SP-M5 (servis) → tabana TIG; A tarafındaki 2 PEM\'in iç yüzüne köpük kapağı. Sağ yan (F tarafı, J1 ağzı): lazer → 1 büküm → 4 × PEM SP-M8 (F) + 6 × PEM SP-M5 + 2 × FHP-M5-25 (J1) + 4 × FHP-M5 → TIG. Tavan: lazer → 3 büküm → 5 × PEM SP-M5 → yanlara TIG.',
     'dış yan sol + 6 PEM + 2 köpük kapağı · dış yan sağ + 16 PEM / saplama · dış tavan + 5 PEM · TIG köşe')
kamera_genel(['dis_yan_sol', 'dis_taban'], yon=(-0.6, 0.45, 0.65), olcek=0.75)
t = koy('dis_yan_sol', [SOL, UST], 'Dış yan sol → dış tabana (köşe TIG)', pem=sorted(PEM_SAC['dis_yan_sol']), grup_kaynak=PUNTA['yan_sol_taban'])
KK = sorted(a for a in P if a.endswith('kopuk_kapagi'))
yakin(merkez(KK[0]), 0.3, yon=(0.8, 0.3, 0.5), tt=t)
for i, a in enumerate(KK): tak(a, t + i * 0.2, 0.5, 40.0)
olay(t, 'Köpük kapağı × 2 → A tarafı PEM SP-M8\'lerin iç yüzüne (köpük girmesin)'); t = bitti() + 0.3
kamera_genel(['dis_yan_sag', 'dis_taban'], yon=(0.6, 0.45, 0.65), olcek=0.75)
t = koy('dis_yan_sag', [SAG, UST], 'Dış yan sağ → dış tabana (köşe TIG)', pem=sorted(PEM_SAC['dis_yan_sag']), grup_kaynak=PUNTA['yan_sag_taban'])
kamera_genel(['dis_tavan', 'dis_yan_sol'], yon=(0.45, 0.85, 0.6), olcek=0.75)
t = koy('dis_tavan', [UST], 'Dış tavan → yan sacların üstüne (köşe TIG)', pem=sorted(PEM_SAC['dis_tavan']), grup_kaynak=PUNTA['tavan_yanlar'])
t += 0.3
# ---- 7 KURU BÖLME
adim('Kuru (teknik) bölme', 'Soğuk odanın altındaki kuru bölme: soğutma cebi (lazer → 3 büküm → 4 × PEM SP-M8 titreşim takozu) taban ağzından cep taşıyıcılara iner; ayırma perdesi; teknik ön perde (2 büküm) ve teknik sağ perde; kuru bölme tabanı (2 büküm + 5 × FHP-M5) üstlerine. Birleşimler punta.',
     'soğutma cebi + PEM SP-M8 × 4 · ayırma perdesi · teknik ön / sağ perde · kuru bölme tabanı + FHP-M5 × 5')
kamera_genel(['sogutma_cebi', 'teknik_on_perde'], yon=(0.35, 0.6, -0.75), olcek=0.8)
t = koy('sogutma_cebi', [ARKA, UST], 'Soğutma cebi → cep taşıyıcılara (punta)', pem=sorted(PEM_SAC['sogutma_cebi']))
for a in ('ayirma_perdesi_cep_sol', 'teknik_on_perde', 'teknik_sag_perde'): t = koy(a, [ARKA, UST, ON], '%s → (punta)' % tr(a))
t = koy('kuru_bolme_tabani', [ARKA, UST], 'Kuru bölme tabanı → perdelerin üstüne (punta)', pem=sorted(PEM_SAC['kuru_bolme_tabani']))
t += 0.3
# ---- 8 SOĞUK ODA İÇ KABUĞU
adim('Soğuk oda iç kabuğu', 'Soğuk odanın tabanı (alt sac, 2 × FHP-M5) ve arka dış sacı (12 × FHP-M5, evaporatör kanal ağızları açık) yerine girer; 4 evaporatör kanal kovanı iki L sacın boyuna TIG dikişiyle, arka dış sacın ağızlarına; arka duvara 3 POM geçiş bloğu.',
     'alt sac · arka dış sac · 4 kanal kovanı (8 L + 8 TIG) · POM geçiş bloğu × 3')
kamera_genel(['soguk_alt_sac', 'soguk_arka_dis_sac'], yon=(0.35, 0.5, 0.85), olcek=0.75)
t = koy('soguk_alt_sac', [ON, UST], 'Soğuk oda alt sacı → teknik perdelerin üstüne (punta)', pem=sorted(PEM_SAC['soguk_alt_sac']))
t = koy('soguk_arka_dis_sac', [ON, UST, ARKA], 'Soğuk oda arka dış sacı → alt sac + yanlar (punta)', pem=sorted(PEM_SAC['soguk_arka_dis_sac']))
for k in range(4):
    for j in (1, 2):
        koy('evap_kanal_kovani_%d_L%d' % (k, j), [ON], '%s → arka dış sacın ağzına' % tr('evap_kanal_kovani_%d_L%d' % (k, j)),
            grup_kaynak=(KAY('evap_kanal_kovani_%d_boyuna_kaynak' % k) if j == 2 else ()), sure_bekle=0.05)
    t += 0.4
t = bitti() + 0.2
for a in sorted(a for a in P if a.startswith('pom_gecis')): koy(a, [ON], 'POM geçiş bloğu → arka dış sac')
t = bitti() + 0.5
# ---- 9 YALITIM LEVHALARI + ASTAR
adim('Yalıtım levhaları + astar', 'Yüzey yüzey: ölçüsünde kesilmiş PU yalıtım levhası (delikleri / cepleri açılmış) önden girer, kovanların ve blokların üstünden geçip dış saca yaslanır; hemen üstüne o yüzün astar sacı (1,0) kapanır. Sıra: arka → sol → sağ → tavan. Astarlar iç köşelerde TIG ile birbirine bağlanır.',
     'PU levha arka + astar arka · PU levha sol + astar sol · PU levha sağ + astar sağ · PU levha tavan + astar tavan · iç köşe TIG')
for pu, ast, yol_pu, pnt in (('pu_levha_arka', 'astar_arka', [ON], None), ('pu_levha_sol', 'astar_sol', [YOL((0, 0, 900), (80, 0, 0)), ON], 'astar_sol'),
                              ('pu_levha_sag', 'astar_sag', [YOL((0, 0, 900), (-80, 0, 0)), ON], 'astar_sag'), ('pu_levha_tavan', 'astar_tavan', [ON, YOL((0, 0, 900), (0, -60, 0))], 'astar_tavan')):
    kamera_genel([pu, ast], yon=(0.25, 0.4, 0.9), olcek=0.7)
    t = koy(pu, yol_pu, '%s → dış saca yaslanır' % P[pu]['ac'].split('(')[0].strip())
    t = koy(ast, [ON] + yol_pu, '%s → levhanın önüne%s' % (tr(ast), ' · iç köşe TIG' if pnt else ''), grup_kaynak=PUNTA[pnt] if pnt else ())
t += 0.3
kamera_genel(['astar_sol'], yon=(0.6, 0.4, 0.75), olcek=0.8)
BURC = sorted(a for a in P if a.startswith('pom_burc'))
for i, a in enumerate(BURC):
    e_ = np.asarray(P[a]['eks'], float); tak(a, t + i * 0.08, 0.5, 80.0) if False else None
    basla(a, -e_ * 80.0, t + i * 0.08); git(a, np.zeros(3), t + i * 0.08, 0.5); vurgu([a], t + i * 0.08 + 0.3, t + i * 0.08 + 1.2); YER[a] = t + i * 0.08 + 0.5; YERINDE.append(a)
olay(t, 'Raf askı burcu POM × 16 → astar + PU deliklerinden içeriden (sıkı geçme)'); t = bitti() + 0.5
# ---- 10 RAF + EŞİK + KOVANLAR
adim('Raf, kovanlar, eşik, üst raf', 'Raf köşebentleri alt saca; PU raf levhası; raf (3 mm, lazer → 4 büküm → 4 × FHP-M5) levhanın üstüne kapanır, arka köşe dolgu kaynağı. Düşme kovanları raftan geçer (kıyma / kuşbaşı iki L + TIG, sos / harç boru, kaşar / sucuk POM). Dil kanalları, eşik (3 büküm), yiv dolguları ve köşe silikonu. Üst raf köşebentleri + üst raf (2 büküm). Ön çerçeve 430 köpük boşluğunu kapatır.',
     'raf köşebendi × 2 · PU raf levhası · raf + 4 FHP · 6 düşme kovanı · dil kanalı × 2 · eşik · yiv dolgusu × 10 · silikon × 8 · üst raf + 2 köşebent · ön çerçeve 430')
kamera_genel(['raf', 'raf_kosebendi_sol'], yon=(0.35, 0.7, 0.75), olcek=0.75)
for a in ('raf_kosebendi_sol', 'raf_kosebendi_sag'): koy(a, [ON, UST], '%s → alt saca (punta)' % tr(a))
t = bitti()
t = koy('pu_raf_esik', [ON, UST], 'PU raf levhası → alt sacın üstüne')
t = koy('raf', [YOL((0, 0, 900), (0, 60, 0)), ON, UST], 'Raf → PU levhanın üstüne, büküm kenarları köşebentlere (punta)', pem=sorted(PEM_SAC['raf']), grup_kaynak=KAY('raf_arka_kose_dolgusu'))
for a in ('dusme_kovani_kiyma_L1', 'dusme_kovani_kiyma_L2', 'dusme_kovani_kusbasi_L1', 'dusme_kovani_kusbasi_L2'):
    koy(a, [UST, YOL((0, 400, 0))], '%s → raf deliğine' % tr(a), grup_kaynak=(KAY(a[:-3] + '_boyuna_kaynak') if a.endswith('L2') else ()), sure_bekle=0.05)
for a in ('dusme_kovani_sos', 'dusme_kovani_harc', 'dusme_kovani_kasar', 'dusme_kovani_sucuk'):
    koy(a, [UST, YOL((0, 400, 0))], '%s → raf deliğine' % P[a]['ac'].split('·')[0].strip(), sure_bekle=0.05)
t = bitti() + 0.2
kamera_genel(['soguk_esik', 'dil_kanali_kasar'], yon=(0.3, 0.6, 0.9), olcek=0.7)
for a in ('dil_kanali_kasar', 'dil_kanali_sucuk'): t = koy(a, [ON, UST], '%s → rafın kesiğine' % tr(a))
t = koy('soguk_esik', [ON, UST], 'Eşik → rafın ön kenarına', grup_kaynak=KAY('raf_esik_yiv') + KAY('esik_on_yiv'))
for k in sorted(a for a in P if a.startswith('dil_kesik_kose_silikonu')): buyu(k, t, 0.4)
olay(t, 'Yiv dolgusu TIG + taşlama × 10 · eşik kesiği köşe silikonu × 8'); t += 0.9
kamera_genel(['ust_raf'], yon=(0.3, 0.5, 0.9), olcek=0.8)
for a in ('ust_raf_kosebendi_sol', 'ust_raf_kosebendi_sag'): koy(a, [ON], '%s → yan astarlara (punta)' % tr(a))
t = bitti()
t = koy('ust_raf', [ON, YOL((0, 0, 900), (0, 40, 0))], 'Üst raf → köşebentlere (punta)')
kamera_genel(['on_cerceve_430'], yon=(0.3, 0.4, 0.9), olcek=0.75)
t = koy('on_cerceve_430', [ON], 'Ön çerçeve 430 → soğuk oda önü (punta)') + 0.3
# ---- 11 SOĞUTMA
adim('Soğutma', 'Arka açıkken: soğutma grubu (Secop, TEK ÜRÜN) arkadan cebe iner, 4 silikon titreşim takozu cebin PEM SP-M8\'lerine; kondenser kanalı braketleriyle taban saplamalarına; iki evaporatör kaseti (TEK ÜRÜN) arkadan kanal kovanı ağızlarına. Bakır hatlar ve yoğuşma hortumu yerinde uzar.',
     'soğutma grubu + 4 takoz · kondenser kanalı · evaporatör L · evaporatör R · bakır hatlar · yoğuşma hortumu')
kamera_genel(['sogutma_grubu', 'evaporator_L', 'evaporator_R'], yon=(0.35, 0.45, -0.85), olcek=0.8)
for a in ('sogutma_grubu', 'kondenser_kanali', 'evaporator_L', 'evaporator_R'):
    t = koy(a, [ARKA, YOL((0, 0, -900), (0, 40, 0)), YOL((0, 0, -900), (0, 120, 0))], '%s → arkadan' % P[a]['ac'].split('(')[0].strip())
for a in ('bakir_hat', 'yogusma_hortumu'): buyu(a, t, 1.0)
olay(t, 'Bakır hatlar (lehim) + yoğuşma hortumu: grup ↔ evaporatörler'); t += 1.4
# ---- 12 TAHRİK MOTORLARI + UNO ARKA GRUPLARI
adim('Tahrik motorları + UNO arka grupları', 'Kaşar ve sucuk kaseti tahrik motorları arkadan, kaplin yuvası arka duvar burcundan geçer. Dört UNO\'nun arka grubu (pnömatik silindir + piston + duvar flanşı) üründen ayrılmış olarak arkadan girer; mil duvar burcundan soğuk odaya geçer, flanş arka dış sacın FHP-M5 saplamasına.',
     'kaşar motoru · sucuk motoru · UNO arka grubu × 4 (kıyma, kuşbaşı, sos, harç)')
kamera_genel(['motor_kasar', 'uno_kiyma_arka', 'uno_sos_arka'], yon=(0.35, 0.45, -0.85), olcek=0.9)
for a in ('motor_kasar', 'motor_sucuk', 'uno_kiyma_arka', 'uno_kusbasi_arka', 'uno_sos_arka', 'uno_harc_arka'):
    t = koy(a, [ARKA, YOL((0, 0, -500), (0, 30, 0))], '%s → arkadan' % P[a]['ac'].split('(')[0].strip())
# ---- 13 HAVA + ELEKTRİK İÇ
adim('Valf adası, hava kanalı, iç kanallar, J1', 'Hava kanalı askıları arka dış sacın ve kuru tabanın FHP-M5 saplamalarına, hava kanalları üstlerine; valf adası (12 valf, TEK ÜRÜN). İç kablo kanalları ve braketler; J1 gömme fiş paneli sağ yandaki FHP-M5-25 saplamalarına içeriden. Hava hortumları ve kablolar kanal boyunca uzar.',
     'hava askısı × 13 · hava kanalı × 3 · valf adası · iç kanallar · J1 paneli · hortumlar · kablolar')
kamera_genel(['valf_adasi', 'hava_kanal_2014_1259'], yon=(0.35, 0.45, -0.85), olcek=1.0)
for a in sorted(a for a in P if a.startswith('hava_aski')): koy(a, [ARKA, YOL((0, 0, -400), (0, 20, 0))], 'Hava askısı → FHP-M5 saplamaya', sure_bekle=0.03)
t = bitti()
for a in sorted(a for a in P if a.startswith('hava_kanal')): t = koy(a, [ARKA, YOL((0, 0, -400), (0, 25, 0))], 'Hava kanalı → askılara')
t = koy('valf_adasi', [ARKA, YOL((0, 0, -400), (0, 25, 0))], 'Valf adası → arkadan')
for a in sorted(a for a in P if a.startswith('elk_')): koy(a, [ARKA, YOL((0, 0, -400), (0, 25, 0)), ON], '%s → yerine' % P[a]['ac'], sure_bekle=0.03)
t = bitti()
t = koy('j1_panel', [YOL((0, 0, -500), (-60, 0, 0)), ARKA], 'J1 gömme fiş paneli → sağ yanın FHP-M5-25 saplamalarına (içeriden)')
for a in ('hava_hortum', 'hava_giris', 'j1_kablo', 'kablo_guc', 'kablo_bilgi'): buyu(a, t, 1.0)
olay(t, 'Hava hortumları (YEŞİL) · güç (KIRMIZI) / bilgi (MAVİ) kabloları kanal boyunca'); t += 1.4
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
# ---- 15 UNO ÖN GRUPLARI + KASETLER
adim('UNO ön grupları + kasetler', 'Dört UNO\'nun ön grubu (hazne + dozaj gövdesi + döner valf) önden rafa sürülür, arka grubun miline geçer; çıkış ağzı + yayıcı raf kovanından aşağıdan takılır. Kaşar ve sucuk kaseti (TEK ÜRÜN) önden dil kanalına sürülür, kaplin motora geçer.',
     'UNO ön grubu × 4 · çıkış ağzı + yayıcı × 4 · kaşar kaseti · sucuk kaseti')
kamera_genel(['uno_kiyma_on', 'uno_sos_on', 'kaset_kasar'], yon=(0.3, 0.45, 0.9), olcek=0.9)
for ad in ('kiyma', 'kusbasi', 'sos', 'harc'):
    t = koy('uno_%s_on' % ad, [ON, YOL((0, 0, 900), (0, 15, 0))], 'UNO %s ön grubu → rafa, arka grubun miline' % ad)
    t = koy('uno_%s_cikis' % ad, [YOL((0, -250, 0)), YOL((0, 0, 700), (0, -250, 0)), YOL((0, -200, 300), (0, -60, 0))], 'UNO %s çıkış ağzı + yayıcı → raf kovanından' % ad)
for a in ('kaset_kasar', 'kaset_sucuk'): t = koy(a, [ON, YOL((0, 0, 900), (0, 10, 0))], '%s → dil kanalından, kaplin motora' % P[a]['ac'].split('(')[0].strip())
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
t = koy('x_ekseni', [ON, YOL((0, 0, 900), (0, 10, 0))], 'X ekseni ünitesi → tabla açıklığına')
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
