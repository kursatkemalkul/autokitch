# -*- coding: utf-8 -*-
"""TOPPING montaj v5 · parça çıkarımı: hat3_v9w (zincir 00–55) → t5_parca.pkl (mm, dünya)
Gövde (TOPPING_GOVDE__*, KAIDE_C, B perçin somunları): adım-37 ent parçaları (hat3_v9e_ent.json) v9e GLB'sindeki ÜÇGEN MERKEZLERİYLE eşlenir
(adım 50 sıkılaştırma indisleri kaydırdı, koordinatlar aynı). Adım 53'te delik açılan parçalar (üst raf, raf, alt sac, arka iç sac, raf PU)
bileşen düzeyinde: eşleşmeyen üçgenler bileşendeki kısmi eşleşen parçaya verilir. Hiç eşleşmeyen bileşenler = adım 53 yenileri (kıyma düşme kovanı sacı).
Ürünler: t5_bil.pkl bileşenleri (düğüm + mek + bağlı bileşen) → ürün grupları (yeni menü: Lahmacun harcı / Kıyma (orta) / Patates / Tavuk / Kuşbaşı / Kaşar / Sucuk).
Kullanım: python t5_parca.py"""
import sys, os, json, pickle, re, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G, bilesen
IS_A = os.path.join(HERE, '..', 't3', 'is_A')
ENT = json.load(open(os.path.join(IS_A, 'hat3_v9e_ent.json'), encoding='utf-8'))['parca']
BIL = pickle.load(open('t5_bil.pkl', 'rb'))
MEK = BIL['MEK']; L = BIL['L']
P = {}


def ekle(ad, V, F, m, tur, ac, **k):
    V = np.asarray(V, float); F = np.asarray(F, np.int64)
    u, inv = np.unique(np.round(V, 4), axis=0, return_inverse=True)
    assert ad not in P, ad
    P[ad] = dict(V=u, F=inv.reshape(-1)[F], m=m, tur=tur, ac=ac, **k)


def birles(LL):
    VV, FF, n = [], [], 0
    for o in LL: VV.append(o['V']); FF.append(np.asarray(o['F']) + n); n += len(o['V'])
    return np.vstack(VV), np.vstack(FF)


def key(C): return [tuple(x) for x in np.round(C, 2)]


# ---------------------------------------------------------------- gövde: v9e üçgen merkezleri → ent adı
GOVDE_DUG = sorted(set(v['dugum'] for v in ENT.values()))
# 5 Eki (bulut): hat3_v9e.glb push edilmedi → merkez_v9w.py aynı eşlemeyi v9w + v4 parça GLB'sinden kurar
if os.path.exists('merkez_v9w.pkl'):
    MERKEZ = pickle.load(open('merkez_v9w.pkl', 'rb'))
else:
    g9e = G(os.path.join(IS_A, 'hat3_v9e.glb'))
    MERKEZ = {}
    for d in GOVDE_DUG:
        ni = g9e.byname[d]; X, T, mek, mat, ex = g9e.tris(ni)[0]
        C = X[T].mean(1)
        for a, v in ENT.items():
            if v['dugum'] != d: continue
            s, n = v['indis']
            for kk in key(C[s // 3:(s + n) // 3]): MERKEZ[(d, kk)] = a
    del g9e
print('merkez', len(MERKEZ))
GOV = [o for o in L if o['dug'] in GOVDE_DUG and not (o['dug'] == 'B_MODULER__baglanti' and not (1430 < o['lo'][0] < 2500 and o['lo'][1] > 740))]
def sinif(a, v):
    t = v['tur']; bom = (v.get('bom') or [''])[0]
    if t == 'sac': m = 'sac'
    elif t == 'profil': m = 'profil'
    elif t == 'kaynak': m = 'kaynak'
    elif t == 'pu': m = 'pu'
    elif t == 'arayuz': m = 'baglanti'; t = 'baglanti'
    elif t == 'silikon' or 'silikonu' in a or a.startswith(('derz_', 'yapistirici')): m = 'yapistirici'; t = 'silikon'
    elif 'kopuk_kapagi' in a: m = 'koyu'
    elif a.startswith('dusme_kovani_k') and v['dugum'].endswith('pom'): m = 'koyu'
    else: m = 'baglanti'
    return m, t, bom
TOPLA = collections.defaultdict(list)          # ent adı → [(V, F)]
YENI = []
DEGISEN = ('raf', 'ust_raf', 'soguk_alt_sac', 'astar_arka', 'pu_raf_esik')
# 5 Eki: kesin atama — tek başına bileşen olan cıvatalar (yüzey teması yüzünden PEM / pul etiketi alıyordu) ve adım 53 kıyma düşme kovanı
CIV = {a: v for a, v in ENT.items() if v['tur'] == 'arayuz' and 'cıvata' in (v.get('bom') or [''])[0]}
KESIN = {}
for o in GOV:
    c = (o['lo'] + o['hi']) / 2; e = o['hi'] - o['lo']
    if o['dug'] == 'TOPPING_GOVDE__sac' and 1880 < o['lo'][0] < 1900 and 1105 < o['lo'][1] < 1115 and o['hi'][1] < 1152:
        KESIN[id(o)] = None; continue      # YENİ'ye → dusme_kovani_kiyma
    for a, v in CIV.items():
        if v['dugum'] != o['dug']: continue
        k = np.array(v['kutu']).reshape(3, 2); kc = k.mean(1); ke = k[:, 1] - k[:, 0]
        if np.all(np.abs(kc - c) < 6) and np.all(np.abs(ke - e) < 10) and np.sort(e)[1] > 10:
            KESIN[id(o)] = a; break
print('kesin atama', {a for a in KESIN.values()})
for o in GOV:
    if id(o) in KESIN:
        if KESIN[id(o)] is None: YENI.append(o)
        else: TOPLA[KESIN[id(o)]].append((o['V'], np.asarray(o['F'])))
        continue
    C = o['V'][o['F']].mean(1); lab = [MERKEZ.get((o['dug'], kk)) for kk in key(C)]
    say = collections.Counter(lab); yok = say.pop(None, 0)
    if not say:
        YENI.append(o); continue
    lab = np.array([x or '' for x in lab], dtype=object)
    if yok:
        # kısmi eşleşen parça: ent'teki üçgen sayısına göre eksik olan (adım 53'te yeniden ağlanan)
        # 5 Eki: eşleşmeyen üçgen (adım 53 delik duvarı, yeniden ağlanan yüzey) → bileşendeki en yakın etiketli üçgenin parçası
        from scipy.spatial import cKDTree as _K
        ad_m = lab != ''; bos = ~ad_m
        _, jj = _K(C[ad_m]).query(C[bos]); lab[np.where(bos)[0]] = lab[np.where(ad_m)[0][jj]]
        print('  kısmi (en yakın): %d eşleşmeyen üçgen (%s) → %s' % (yok, o['dug'], dict(collections.Counter(lab[np.where(bos)[0]]))))
    for a in set(lab):
        m = lab == a; Tc = o['F'][m]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True)
        TOPLA[a].append((o['V'][u], inv.reshape(-1, 3)))
# 5 Eki: pul etiketine düşen cıvata parçaları (cıvata başı pul yüzüne oturur → yüzey oyu) — boyu > 5 mm olan parça cıvatadır
for a in [a for a in list(TOPLA) if a.startswith('arayuz_kb_') and a.endswith('_pul') and a[:-4] in ENT]:
    kal = []
    for V_, F_ in TOPLA[a]:
        (TOPLA[a[:-4]] if np.ptp(V_[:, 1]) > 5 else kal).append((V_, F_))
    TOPLA[a] = kal
# 5 Eki: B perçin somunları (adım 47'de boy 17 → 21 mm) — eşleşmeyen B_MODULER__baglanti bileşenleri konumla ent'e
for o in list(YENI):
    if o['dug'] != 'B_MODULER__baglanti': continue
    c = (o['lo'] + o['hi']) / 2
    ad = [a for a in ENT if a.startswith('percin_somun_tb') and abs((ENT[a]['kutu'][0] + ENT[a]['kutu'][1]) / 2 - c[0]) < 2 and abs((ENT[a]['kutu'][4] + ENT[a]['kutu'][5]) / 2 - c[2]) < 2]
    if len(ad) == 1: TOPLA[ad[0]].append((o['V'], o['F'])); YENI.remove(o)
for a, v in ENT.items():
    if a not in TOPLA or not TOPLA[a]: print('  ENT EŞLEŞMEDİ', a, v['dugum']); continue
    VV, FF, n = [], [], 0
    for V, F in TOPLA[a]: VV.append(V); FF.append(F + n); n += len(V)
    m, t, bom = sinif(a, v)
    ekle(a, np.vstack(VV), np.vstack(FF), m, t, bom, dugum=v['dugum'])
print('gövde (ent)', len(P), '· yeni bileşen', len(YENI))
for o in YENI: print('  YENİ', o['dug'], np.round(o['lo'], 1).tolist(), np.round(o['hi'], 1).tolist(), len(o['F']))
# adım 53 yenileri (gövde düğümünde): kıyma (orta) düşme kovanı boru Ø38 × 3,5 (harç kovanı kopyası x −348)
for o in YENI:
    if o['dug'] == 'TOPPING_GOVDE__sac' and 1880 < o['lo'][0] < 1900 and 1105 < o['lo'][1] < 1115:
        ekle('dusme_kovani_kiyma', o['V'], o['F'], 'baglanti', 'baglanti', 'Düşme kovanı boru Ø38 × 3,5 AISI 304 (kıyma · alt sac + raf arasında)', dugum=o['dug'])
    elif o['dug'] == 'TOPPING_GOVDE__paslanmaz' and o['lo'][0] > 2480:          # adım 55: TOPPING → F pul ISO 7092 + cıvata 0,4 mm kaydı
        c = (o['lo'] + o['hi']) / 2; pul = (o['hi'][0] - o['lo'][0]) < 3
        ad = [a for a in ENT if a.startswith('arayuz_m8_F') and not a.endswith('_pul') and abs((ENT[a]['kutu'][2] + ENT[a]['kutu'][3]) / 2 - c[1]) < 2 and abs((ENT[a]['kutu'][4] + ENT[a]['kutu'][5]) / 2 - c[2]) < 2]
        assert len(ad) == 1, (ad, c); ad = ad[0] + ('_pul' if pul else '')
        ekle(ad, o['V'], o['F'], 'baglanti', 'baglanti', 'Küçük pul ISO 7092 M8 (Ø15)' if pul else 'Silindir başlı imbus cıvata ISO 4762 M8 × 16', dugum=o['dug'])
    else: print('  ATANMAYAN YENİ GÖVDE', o['dug'], np.round(o['lo']), np.round(o['hi']))
for a in list(P):
    if a.startswith('pu_levha_'): P[a]['ac'] = 'PU levha %s (40 kg/m³ · ölçüsünde kesilmiş, flanş / perçin yuvaları açık)' % {'arka': 'arka', 'sol': 'sol', 'sag': 'sağ', 'tavan': 'tavan'}[a.split('_')[2]]
    if a.startswith('yapistirici_'): P[a]['ac'] = 'Yapıştırıcı (PU levha → dış sac, 0,5 mm)'
    if a.startswith('derz_'): P[a]['ac'] = 'Derz silikonu (gıda tarafı)'
P['pu_raf_esik']['ac'] = 'PU levha raf (raf altı + eşik arkası · ölçüsünde kesilmiş)'
P['dusme_kovani_sos']['ac'] = 'Düşme kovanı boru Ø38 × 3,5 AISI 304 (patates)'; P['dusme_kovani_harc']['ac'] = 'Düşme kovanı boru Ø38 × 3,5 AISI 304 (lahmacun harcı)'
# ---------------------------------------------------------------- ürünler (bileşenler)
GOVIDS = set(id(o) for o in GOV)
KUL = [o for o in L if id(o) not in GOVIDS and not o['dug'].startswith('ACIL_STOP')]
def kod(o): return MEK[o['mek']]['kod'] if o['mek'] >= 0 else ''
def sec(f): return [o for o in KUL if f(o)]
ATANAN = set()
def grup(ad, LL, m, tur, ac, **k):
    LL = [o for o in LL if id(o) not in ATANAN]
    assert LL, ad
    for o in LL: ATANAN.add(id(o))
    ekle(ad, *birles(LL), m, tur, ac, **k)
def ic(o, lo, hi, tol=0.6): return np.all(o['lo'] >= np.array(lo) - tol) and np.all(o['hi'] <= np.array(hi) + tol)
def ex(o): return o['hi'] - o['lo']

# gövde mekanizması (mek TOPPING/Gövde, ent dışı)
G7 = sec(lambda o: kod(o) == 'TOPPING/Gövde')
kan = [o for o in G7 if o['dug'] == 'TOPPING_MODUL__on_seffaf']
grup('kanat_K1', [o for o in kan if o['hi'][2] > 39.5 and o['lo'][0] < 1966.5], 'kapak_s', 'kapak', 'Kanat K1 (çift cidar + PU + fitil · hazır alt montaj)')
grup('kanat_K2', [o for o in kan if o['hi'][2] > 39.5 and o['lo'][0] > 1966.5], 'kapak_s', 'kapak', 'Kanat K2 (çift cidar + PU + fitil · hazır alt montaj)')
grup('orta_kayit', [o for o in kan if o['lo'][0] > 1920 and o['lo'][1] > 1150] + [o for o in G7 if o['dug'] == 'TOPPING_MODUL__pom' and o['lo'][1] > 1150 and o['hi'][2] > 30],
     'kapak', 'mek', 'Orta kayıt (kanat dayama dikmesi + alt POM takozu · hazır)')
pas = [o for o in G7 if o['dug'] == 'TOPPING_MODUL__paslanmaz']
for o in sorted([o for o in pas if abs(ex(o)[1] - 70) < 1], key=lambda o: (o['lo'][0], o['lo'][1])):
    grup('mentese_%s_%d' % ('sol' if o['lo'][0] < 1900 else 'sag', round(o['lo'][1])), [o], 'mekanizma', 'mek', 'Gizli menteşe gövdesi (kaldır-çıkar · satın alınan)')
for o in sorted([o for o in pas if abs(ex(o)[0] - 30) < 1 and abs(ex(o)[2] - 13) < 1], key=lambda o: (o['lo'][0], o['lo'][1])):
    grup('basac_%d_%d' % (round(o['lo'][0]), round(o['lo'][1])), [o], 'koyu', 'mek', 'Bas-aç mandalı (satın alınan)')
grup('on_alt_braket', [o for o in pas if o['lo'][1] < 945 and o['lo'][2] > 0 and o['lo'][0] > 1900 and o['hi'][0] < 2020], 'mekanizma', 'mek', 'Ön alt braket (tabla sensör tutucu · hazır, saplamalarla)')
pom7 = [o for o in G7 if o['dug'] == 'TOPPING_MODUL__pom' and id(o) not in ATANAN]
for o in sorted([o for o in pom7 if abs(ex(o)[0] - 57.5) < 1], key=lambda o: (o['lo'][0], o['lo'][1], o['lo'][2])):
    grup('pom_burc_%s_%d_%d' % ('sol' if o['lo'][0] < 1900 else 'sag', round(o['lo'][1]), round(-o['lo'][2])), [o], 'koyu', 'mek', 'Raf askı burcu POM (duvar geçişi)', eks=(1.0 if o['lo'][0] < 1900 else -1.0, 0, 0))
for o in sorted([o for o in pom7 if id(o) not in ATANAN and o['lo'][2] < -600], key=lambda o: (o['lo'][0], o['lo'][1])):
    grup('pom_gecis_%d_%d' % (round(o['lo'][0]), round(o['lo'][1])), [o], 'koyu', 'mek', 'Arka duvar geçiş bloğu POM (hortum / kablo)')
kalan7 = [o for o in G7 if id(o) not in ATANAN]
print('gövde mek kalan', [(o['dug'], np.round(o['lo']).tolist(), np.round(o['hi']).tolist()) for o in kalan7])

# X ekseni (tek ürün; motor ayrı gelir)
XB = sec(lambda o: kod(o) == 'TOPPING/Tabla' and o['lo'][1] > 1040 and o['hi'][1] > 1100 and ex(o)[0] < 20)
for i_, o in enumerate(XB): grup('x_sensor_braket_%d' % i_, [o], 'mekanizma', 'mek', 'X ekseni sensör braketi (alt sacın saplamasına)')
grup('x_motor', sec(lambda o: kod(o) == 'TOPPING/Tabla' and id(o) not in ATANAN and o['lo'][0] > 2330 and o['hi'][2] < -385), 'motor', 'mek', 'X ekseni motoru + braketi + kasnak (ünitenin ayrı gelen parçası)')
grup('x_ekseni', sec(lambda o: kod(o) == 'TOPPING/Tabla' and id(o) not in ATANAN), 'mekanizma', 'mek', 'X ekseni (ray tabanı + 2 lineer ray + araba + bantlı tabla + kayış · hazır ürün)')

# soğutma
S17 = sec(lambda o: kod(o) == 'TOPPING/Soğutma')
grup('bakir_hat', [o for o in S17 if o['dug'] == 'TOPPING_MODUL__bakir'], 'alu', 'kablo', 'Bakır hatlar (emiş + sıvı · grup ↔ evaporatörler, lehimli)')
grup('yogusma_hortumu', [o for o in S17 if o['dug'] == 'TOPPING_MODUL__silikon' and ex(o)[0] > 300], 'hava', 'kablo', 'Yoğuşma hortumu (evaporatör tavaları → cep)')
grup('sogutma_grubu', [o for o in S17 if (o['dug'] == 'TOPPING_MODUL__motor' and o['lo'][1] < 900) or (o['dug'] == 'TOPPING_MODUL__silikon' and o['hi'][1] < 820)],
     'motor', 'mek', 'Soğutma grubu (kompresör + kondenser + fan · hazır ürün) + 4 silikon titreşim takozu')
grup('kondenser_braketi', [o for o in S17 if o['dug'] == 'TOPPING_MODUL__sac' and o['lo'][1] < 895 and 2090 < o['lo'][0] < 2110], 'mekanizma', 'mek', 'Kondenser kanalı alt braketi (dış tabanın saplamalarına)')
grup('kondenser_kanali', [o for o in S17 if id(o) not in ATANAN and (o['lo'][0] > 2010 and o['hi'][0] < 2280 and o['hi'][1] < 1400 and o['dug'] in ('TOPPING_MODUL__koyu', 'TOPPING_MODUL__celik', 'TOPPING_MODUL__sac'))],
     'mekanizma', 'mek', 'Kondenser hava kanalı + braketleri (grupla gelir · saplamalara)')
for nm, x0, x1 in (('evaporator_L', 1440, 1700), ('evaporator_R', 1750, 2230)):
    grup(nm, [o for o in S17 if o['lo'][0] >= x0 and o['hi'][0] <= x1 and o['lo'][1] > 1250] + [o for o in KUL if o['dug'] == 'ELK_TOPPING__rakor' and x0 <= o['lo'][0] <= x1 and o['lo'][1] > 1500],
         'alu', 'mek', 'Evaporatör kaseti %s (serpantin + fan + PU kaset + conta%s · hazır ürün)' % (nm[-1], ' + yalıtımlı silindir cebi' if nm[-1] == 'R' else ''))
kalan17 = [o for o in S17 if id(o) not in ATANAN]
print('soğutma kalan', [(o['dug'], np.round(o['lo']).tolist(), np.round(o['hi']).tolist()) for o in kalan17])

# kasetler + tahrik motorları
for kd, ad in (('TOPPING/Kaşar', 'kasar'), ('TOPPING/Sucuk', 'sucuk')):
    K_ = sec(lambda o: kod(o) == kd)
    grup('burc_motor_' + ad, [o for o in K_ if o['dug'] == 'TOPPING_MODUL__pom' and o['lo'][2] < -640 and o['hi'][2] > -570], 'koyu', 'mek', '%s motoru kaplin burcu POM (arka duvar geçişi)' % ad.capitalize())
    grup('motor_' + ad, [o for o in K_ if id(o) not in ATANAN and o['lo'][2] < -640 and o['hi'][2] < -500], 'motor', 'mek', '%s kaseti tahrik motoru (redüktör + flanş + kaplin · hazır ürün)' % ad.capitalize())
    grup('kaset_ray_' + ad, [o for o in K_ if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__paslanmaz' and o['lo'][1] > 1150 and o['hi'][1] < 1185 and o['lo'][2] < -500], 'mekanizma', 'mek', '%s kaseti rayı + 4 ayak (raf saplamalarına)' % ad.capitalize())
    grup('kaset_' + ad + '_mandal', [o for o in K_ if id(o) not in ATANAN and o['hi'][1] < 1161 and o['hi'][0] < (1980 if ad == 'kasar' else 2312)], 'koyu', 'mek', '%s kaseti kilit mandalı (POM yuva + yaylı dil · rafa gömülü)' % ad.capitalize())
    grup('kaset_' + ad + '_conta', [o for o in K_ if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__conta' and o['hi'][1] < 1153], 'yapistirici', 'mek', '%s kovanı raf contası' % ad.capitalize())
    grup('kaset_' + ad + '_cikis', [o for o in K_ if id(o) not in ATANAN and o['hi'][1] < 1150], 'mekanizma', 'mek', '%s çıkış ağzı (kovanın içinde sabit · alttan takılır)' % ad.capitalize())
    grup('kaset_' + ad, [o for o in K_ if id(o) not in ATANAN], 'alu', 'mek', '%s kaseti (hazne + helezon + karıştırıcı · hazır ürün, dil kanalından sürülür)' % ad.capitalize())

# UNO'lar (yeni menü): kod → kısa ad · düğüm eki
UNO = (('TOPPING/Tavuk', 'tavuk', 'KIYMA', 'tavuk'), ('TOPPING/Kuşbaşı', 'kusbasi', 'KUSBASI', 'kuşbaşı'), ('TOPPING/Patates', 'patates', 'SOS', 'patates'),
       ('TOPPING/Lahmacun harcı', 'harc', 'HARC', 'lahmacun harcı'), ('TOPPING/Kıyma', 'kiyma', 'KIYMA_ORTA', 'kıyma'))
for kd, ad, ek, tr_ in UNO:
    U = sec(lambda o: kod(o) == kd)
    grup('burc_uno_' + ad, [o for o in U if o['dug'] == 'TOPPING_MODUL__pom' and o['lo'][2] < -630 and o['hi'][2] > -570], 'koyu', 'mek', 'UNO %s piston burcu POM (arka duvar geçişi)' % tr_)
    if ad == 'kiyma':
        grup('burc_kilifi_kiyma', [o for o in U if id(o) not in ATANAN and o['lo'][2] < -629.9 and o['hi'][2] > -572 and o['dug'] == 'TOPPING_MODUL__paslanmaz' and o['hi'][1] < 1660], 'mekanizma', 'mek', 'Burç kılıfı (paslanmaz boru + ayak · evaporatör cebi ağzında)')
    arka = [o for o in U if id(o) not in ATANAN and (o['hi'][2] < -650 or (o['lo'][2] < -560 and o['hi'][2] < -440 and ex(o)[0] < 60 and o['lo'][1] > 1100)) and 'PISTON' not in o['dug']]
    arka += [o for o in U if id(o) not in ATANAN and 'PISTON' in o['dug'] and 'pom' not in o['dug']]   # 5 Eki: piston mili (duvar + burç + gövde içi) silindirle arkadan gelir, POM pistona vidalanır; POM piston ön grupta
    grup('uno_%s_arka' % ad, arka, 'alu', 'mek', 'UNO %s · arka grup (pnömatik silindir + piston + duvar flanşı · üründen ayrılmış)' % tr_)
    if ad in ('harc', 'patates', 'kiyma'):
        grup('uno_%s_conta' % ad, [o for o in U if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__conta' and o['hi'][1] < 1153], 'yapistirici', 'mek', 'UNO %s kovanı taban contası' % tr_)
        grup('uno_%s_raf_conta' % ad, [o for o in U if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__conta' and o['lo'][1] > 1560], 'yapistirici', 'mek', 'UNO %s üst raf geçiş contası' % tr_)
        grup('uno_%s_cikis' % ad, [o for o in U if id(o) not in ATANAN and o['hi'][1] < 1182.5 and o['lo'][1] > 1040], 'mekanizma', 'mek', 'UNO %s çıkış borusu + yayıcı (alttan kovana · üstte kelepçe)' % tr_)
        grup('uno_%s_hortum' % ad, [o for o in U if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__hortum_gida'], 'hava', 'kablo', 'UNO %s gıda hortumu (üst raf deliğinden kelepçeye)' % tr_)
        grup('uno_%s_kelepce' % ad, [o for o in U if id(o) not in ATANAN and o['lo'][1] > 1181.5 and o['hi'][1] < 1216.5], 'baglanti', 'mek', 'UNO %s kelepçe (boru ↔ hortum, tri-clamp)' % tr_)
        grup('uno_%s_raf_flans' % ad, [o for o in U if id(o) not in ATANAN and o['lo'][1] > 1530 and o['hi'][1] < 1556], 'mekanizma', 'mek', 'UNO %s üst raf altı hortum flanşı' % tr_)
    if ad == 'kiyma':
        grup('uno_kiyma_dirsek', [o for o in U if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__paslanmaz' and o['lo'][1] > 1540 and o['hi'][1] < 1660 and o['hi'][2] > -260 and o['lo'][0] < 1950], 'mekanizma', 'mek', 'UNO kıyma çıkış dirseği Ø35,6 × 1,8 (2 × 90° · üst rafın üstünde)')
    grup('uno_%s_on' % ad, [o for o in U if id(o) not in ATANAN], 'mekanizma', 'mek', 'UNO %s · ön grup (hazne + dozaj gövdesi + döner valf · hazır ürün gövdesi)' % tr_)

# hava
H = sec(lambda o: kod(o) == 'TOPPING/Hava')
grup('valf_adasi', [o for o in H if o['dug'] in ('TOPPING_MODUL__siyah',) or (o['dug'] == 'TOPPING_MODUL__aluminyum' and o['lo'][0] < 2000)], 'motor', 'mek', 'Valf adası (12 valf · hazır ürün)')
grup('hava_hortum', [o for o in H if o['dug'] == 'TOPPING_MODUL__hava_ana'], 'hava', 'kablo', 'Hava hortumları (valf adası → UNO pistonları)')
for o in sorted([o for o in H if o['dug'] == 'HAVA_IC__aski'], key=lambda o: (o['lo'][2], o['lo'][0], o['lo'][1])):
    grup('hava_aski_%d_%d' % (round(o['lo'][0]), round(o['lo'][1])), [o], 'kanal', 'mek', 'Hava kanalı askısı (saplamaya)')
for o in sorted([o for o in H if o['dug'] == 'HAVA_IC__kanal' and ex(o).max() > 50], key=lambda o: o['lo'][0]):
    grup('hava_kanal_%d_%d' % (round(o['lo'][0]), round(o['lo'][1])), [o], 'kanal', 'mek', 'Hava kanalı (askılara oturur)')
J1 = sec(lambda o: o['dug'].startswith('ELK_ZINCIR') and kod(o) in ('TOPPING/Elektrik', 'TOPPING/Hava'))
grup('j1_panel', [o for o in J1 if not (o['dug'].endswith(('kablo_guc', 'kablo_veri')) or (o['dug'] == 'ELK_ZINCIR__hava' and o['lo'][1] < 1200))], 'fis', 'mek', 'Fiş paneli (güç + bilgi fişleri + hava rakoru · hazır, gömme)')
grup('j1_kablo', [o for o in J1 if o['dug'].endswith(('kablo_guc', 'kablo_veri'))], 'guc', 'kablo', 'Fiş paneli iç bağlantı kabloları')
grup('hava_giris', [o for o in J1 if id(o) not in ATANAN] + [o for o in H if id(o) not in ATANAN], 'hava', 'kablo', 'Hava giriş hattı (fiş paneli rakoru → valf adası)')

# elektrik: servis sacına bağlı cihazlar (temas zinciri) · iç kanallar · kablolar
E = sec(lambda o: kod(o) == 'TOPPING/Elektrik' and not o['dug'].startswith('ELK_ZINCIR'))
KABLO = ('ELK_TOPPING__kablo', 'ELK_TOPPING__kablo_sinyal')
cih = [o for o in E if o['dug'] not in KABLO]
serv = [o for o in cih if o['lo'][2] < -826.0]
deg = True
while deg:
    deg = False
    for o in cih:
        if any(o is x for x in serv): continue
        if any(np.all(o['lo'] <= x['hi'] + 0.3) and np.all(o['hi'] >= x['lo'] - 0.3) for x in serv) and o['hi'][2] < -650:
            serv.append(o); deg = True
pomS = [o for o in kalan17 if o['dug'] == 'TOPPING_MODUL__pom' and o['lo'][2] < -827]
grup('servis_cihaz', serv + pomS, 'elektrik', 'mek', 'Servis sacı cihazları: pano kutusu + DIN plakası + sürücü kartları + kanallar + braketler + filtre kapağı (sacın saplamalarına · hazır)')
for o in sorted([o for o in cih if id(o) not in ATANAN], key=lambda o: (o['lo'][0], o['lo'][1])):
    grup('elk_%s_%d_%d' % (o['dug'].split('__')[-1], round(o['lo'][0]), round(o['lo'][1])), [o], 'kanal' if 'kanal' in o['dug'] else 'elektrik', 'mek', '%s (iç)' % o['dug'].split('__')[-1])
grup('kablo_guc', [o for o in E if o['dug'] == 'ELK_TOPPING__kablo'], 'guc', 'kablo', 'Güç kabloları (kırmızı · kanal boyunca)')
grup('kablo_bilgi', [o for o in E if o['dug'] == 'ELK_TOPPING__kablo_sinyal'], 'bilgi', 'kablo', 'Bilgi kabloları (mavi · kanal boyunca)')
for o in [o for o in kalan17 if id(o) not in ATANAN]:
    grup('sogutma_parca_%d_%d' % (round(o['lo'][0]), round(o['lo'][1])), [o], 'koyu', 'mek', '%s (soğutma)' % o['dug'].split('__')[-1])

# ---------------------------------------------------------------- çevre (silik)
def cev(ad, f, ac):
    LL = [o for o in KUL if id(o) not in ATANAN and f(o)]
    if not LL: return
    for o in LL: ATANAN.add(id(o))
    ekle(ad, *birles(LL), 'silik', 'cevre', ac)
cev('cevre_B', lambda o: o['dug'].startswith(('B_', 'CEK_', 'ELK_DOLAP', 'ELK_IC')) and o['hi'][1] < 800, 'B dolabı (silik çevre)')
cev('cevre_A', lambda o: o['dug'].startswith(('A_', 'KAIDE_A')), 'A (silik çevre · hat bağlantısında)')
cev('cevre_F', lambda o: o['dug'].startswith(('F_', 'U_', 'D_PIZZA', 'ELK_ZINCIR', 'ELK_ISTASYON', 'ELK_HAT', 'ELK_ZEMIN')), 'F (silik çevre · hat bağlantısında)')
kalan = [o for o in KUL if id(o) not in ATANAN]
print('ATANMAYAN', len(kalan), collections.Counter((o['dug'], kod(o)) for o in kalan))
for o in kalan[:30]: print('   ', o['dug'], kod(o), np.round(o['lo']).tolist(), np.round(o['hi']).tolist(), len(o['F']))
pickle.dump(dict(P=P, ENT=ENT), open('t5_parca.pkl', 'wb'))
for a in sorted(P):
    if not (a.startswith(('servis_arka', 'arayuz_', 'kaide_ust_plaka_delik')) or 'kaynak' in a or 'dolgu' in a or 'silikonu' in a):
        print('%-34s %-9s %6d  lo %s hi %s' % (a, P[a]['m'], len(P[a]['F']), np.round(P[a]['V'].min(0)).astype(int).tolist(), np.round(P[a]['V'].max(0)).astype(int).tolist()))
print('TOPLAM', len(P))
