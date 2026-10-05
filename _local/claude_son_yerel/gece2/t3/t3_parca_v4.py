# -*- coding: utf-8 -*-
"""TOPPING montaj v4 (üreteç h3_topping_sac_v2: dimple · bükümlü iç sac + perçin + POM pul · PU levha + yapıştırıcı · evaporatör ayağı · kanal kapağı)
Kullanım: python t3_parca_v4.py <glb (zincir 37–49 çıktısı, sıkılaştırma öncesi)> <t_bil.pkl> <hat3_v9e_ent.json>
ESKİ: TOPPING montaj v3 · parça çıkarımı: <glb> (= ajan zincirinin son GLB'si + zincir_T_tamamla.py) → t3_parca.pkl (mm, dünya)
Gövde: adım-37 ent aralıkları (hat3_v9e_ent.json · üçgen sayıları birebir). PU köpük bloğu (pu_soguk_duvar) yüzey yüzey kesilmiş levhalara
bölünür (manifold kesişimi: birleşimi = model). Diğerleri: t_bil.pkl bileşenleri (düğüm + mek + bağlı bileşen) → ürün grupları.
Kullanım: python t3_parca.py <glb> <t_bil.pkl>"""
import sys, os, json, pickle, re, collections
import numpy as np
import manifold3d as mf
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g = G(sys.argv[1])
ENT = json.load(open(sys.argv[3], encoding='utf-8'))['parca']
BIL = pickle.load(open(sys.argv[2], 'rb'))
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


NT = {}
def node_tri(d):
    if d not in NT: NT[d] = g.tris(g.byname[d])[0][:2]
    return NT[d]


# ---------------------------------------------------------------- gövde (ent)
for a, v in ENT.items():
    X, T = node_tri(v['dugum']); s, n = v['indis']; Tt = T[s // 3:(s + n) // 3]
    u, inv = np.unique(Tt.reshape(-1), return_inverse=True)
    bom = (v.get('bom') or [''])[0]; t = v['tur']
    if t == 'sac': m = 'sac'
    elif t == 'profil': m = 'profil'
    elif t == 'kaynak': m = 'kaynak'
    elif t == 'pu': m = 'pu'
    elif t == 'arayuz': m = 'baglanti'; t = 'baglanti'
    elif t == 'silikon' or 'silikonu' in a or a.startswith(('derz_', 'yapistirici')): m = 'yapistirici'; t = 'silikon'
    elif 'kopuk_kapagi' in a: m = 'koyu'
    elif a.startswith('dusme_kovani_k') and v['dugum'].endswith('pom'): m = 'koyu'
    else: m = 'baglanti'
    ekle(a, X[u], inv.reshape(-1, 3), m, t, bom, dugum=v['dugum'])
print('gövde (ent)', len(P))

# ---------------------------------------------------------------- v4: PU levhalar / yapıştırıcı / derz silikonu üreteçte ayrı parça (T2 bölme yok)
for a in list(P):
    if a.startswith('pu_levha_'): P[a]['ac'] = 'PU levha %s (40 kg/m³ · ölçüsünde kesilmiş, flanş / perçin yuvaları açık)' % {'arka': 'arka', 'sol': 'sol', 'sag': 'sağ', 'tavan': 'tavan'}[a.split('_')[2]]
    if a.startswith('yapistirici_'): P[a]['ac'] = 'Yapıştırıcı (PU levha → dış sac, 0,5 mm)'
    if a.startswith('derz_'): P[a]['ac'] = 'Derz silikonu (gıda tarafı)'
P['pu_raf_esik']['ac'] = 'PU levha raf (raf altı + eşik arkası · ölçüsünde kesilmiş)'
# ---------------------------------------------------------------- ürünler (t_bil bileşenleri)
GOVDE_DUG = set(v['dugum'] for v in ENT.values())
KUL = [o for o in L if o['dug'] not in GOVDE_DUG and not o['dug'].startswith('ACIL_STOP')]
def kod(o): return MEK[o['mek']]['kod'] if o['mek'] >= 0 else ''
def sec(f): return [o for o in KUL if f(o)]
ATANAN = set()
def grup(ad, LL, m, tur, ac, **k):
    LL = [o for o in LL if id(o) not in ATANAN]
    assert LL, ad
    for o in LL: ATANAN.add(id(o))
    ekle(ad, *birles(LL), m, tur, ac, **k)
def ic(o, lo, hi, tol=0.6): return np.all(o['lo'] >= np.array(lo) - tol) and np.all(o['hi'] <= np.array(hi) + tol)

# gövde mekanizması (mek TOPPING/Gövde, ent dışı)
G7 = sec(lambda o: kod(o) == 'TOPPING/Gövde')
kan = [o for o in G7 if o['dug'] == 'TOPPING_MODUL__on_seffaf']
grup('kanat_K1', [o for o in kan if o['hi'][2] > 39.5 and o['lo'][0] < 1966.5], 'kapak_s', 'kapak', 'Kanat K1 (çift cidar + PU + fitil · hazır alt montaj)')
grup('kanat_K2', [o for o in kan if o['hi'][2] > 39.5 and o['lo'][0] > 1966.5], 'kapak_s', 'kapak', 'Kanat K2 (çift cidar + PU + fitil · hazır alt montaj)')
grup('orta_kayit', [o for o in kan if o['lo'][0] > 1920 and o['lo'][1] > 1150] + [o for o in G7 if o['dug'] == 'TOPPING_MODUL__pom' and o['lo'][1] > 1150 and o['hi'][2] > 30],
     'kapak', 'mek', 'Orta kayıt (kanat dayama dikmesi + alt POM takozu · hazır)')
pas = [o for o in G7 if o['dug'] == 'TOPPING_MODUL__paslanmaz']
for o in sorted([o for o in pas if abs((o['hi'] - o['lo'])[1] - 70) < 1], key=lambda o: (o['lo'][0], o['lo'][1])):
    grup('mentese_%s_%d' % ('sol' if o['lo'][0] < 1900 else 'sag', round(o['lo'][1])), [o], 'mekanizma', 'mek', 'Gizli menteşe gövdesi (kaldır-çıkar · satın alınan)')
for o in sorted([o for o in pas if abs((o['hi'] - o['lo'])[0] - 30) < 1 and abs((o['hi'] - o['lo'])[2] - 13) < 1], key=lambda o: (o['lo'][0], o['lo'][1])):
    grup('basac_%d_%d' % (round(o['lo'][0]), round(o['lo'][1])), [o], 'koyu', 'mek', 'Bas-aç mandalı (satın alınan)')
grup('on_alt_braket', [o for o in pas if o['lo'][1] < 945 and o['lo'][2] > 0 and o['lo'][0] > 1900 and o['hi'][0] < 2020], 'mekanizma', 'mek', 'Ön alt braket (tabla sensör tutucu · hazır, saplamalarla)')
pom7 = [o for o in G7 if o['dug'] == 'TOPPING_MODUL__pom' and id(o) not in ATANAN]
for o in sorted([o for o in pom7 if abs((o['hi'] - o['lo'])[0] - 57.5) < 1], key=lambda o: (o['lo'][0], o['lo'][1], o['lo'][2])):
    grup('pom_burc_%s_%d_%d' % ('sol' if o['lo'][0] < 1900 else 'sag', round(o['lo'][1]), round(-o['lo'][2])), [o], 'koyu', 'mek', 'Raf askı burcu POM (duvar geçişi)', eks=(1.0 if o['lo'][0] < 1900 else -1.0, 0, 0))
for o in sorted([o for o in pom7 if id(o) not in ATANAN and o['lo'][2] < -600], key=lambda o: (o['lo'][0], o['lo'][1])):
    grup('pom_gecis_%d_%d' % (round(o['lo'][0]), round(o['lo'][1])), [o], 'koyu', 'mek', 'Arka duvar geçiş bloğu POM (hortum / kablo · köpük öncesi)')
kalan7 = [o for o in G7 if id(o) not in ATANAN]
print('gövde mek kalan', [(o['dug'], np.round(o['lo']).tolist(), np.round(o['hi']).tolist()) for o in kalan7])

# X ekseni (tek ürün)
XB = sec(lambda o: kod(o) == 'TOPPING/Tabla' and o['lo'][1] > 1040 and o['hi'][1] > 1100 and (o['hi'] - o['lo'])[0] < 20)
for i_, o in enumerate(XB): grup('x_sensor_braket_%d' % i_, [o], 'mekanizma', 'mek', 'X ekseni sensör braketi (soğuk oda alt sacının FHP-M5 saplamasına)')
grup('x_motor', sec(lambda o: kod(o) == 'TOPPING/Tabla' and id(o) not in ATANAN and o['lo'][0] > 2330 and o['hi'][2] < -385), 'motor', 'mek', 'X ekseni motoru + braketi + kasnak (ünitenin ayrı gelen parçası)')
grup('x_ekseni', sec(lambda o: kod(o) == 'TOPPING/Tabla' and id(o) not in ATANAN), 'mekanizma', 'mek', 'X ekseni (ray tabanı + 2 lineer ray + araba + bantlı tabla + kayış · hazır)')

# soğutma
S17 = sec(lambda o: kod(o) == 'TOPPING/Soğutma')
grup('bakir_hat', [o for o in S17 if o['dug'] == 'TOPPING_MODUL__bakir'], 'alu', 'kablo', 'Bakır hatlar (emiş + sıvı · grup ↔ evaporatörler, lehimli)')
grup('yogusma_hortumu', [o for o in S17 if o['dug'] == 'TOPPING_MODUL__silikon' and (o['hi'] - o['lo'])[0] > 300], 'hava', 'kablo', 'Yoğuşma hortumu (evaporatör tavaları → cep)')
grup('sogutma_grubu', [o for o in S17 if (o['dug'] == 'TOPPING_MODUL__motor' and o['lo'][1] < 900) or (o['dug'] == 'TOPPING_MODUL__silikon' and o['hi'][1] < 820)],
     'motor', 'mek', 'Soğutma grubu Secop (kompresör + kondenser + fan · TEK ÜRÜN) + 4 silikon titreşim takozu')
grup('kondenser_braketi', [o for o in S17 if o['dug'] == 'TOPPING_MODUL__sac' and o['lo'][1] < 895 and 2090 < o['lo'][0] < 2110], 'mekanizma', 'mek', 'Kondenser kanalı alt braketi (dış tabanın FHP-M5 saplamalarına)')
grup('kondenser_kanali', [o for o in S17 if id(o) not in ATANAN and (o['lo'][0] > 2010 and o['hi'][0] < 2280 and o['hi'][1] < 1400 and o['dug'] in ('TOPPING_MODUL__koyu', 'TOPPING_MODUL__celik', 'TOPPING_MODUL__sac'))],
     'mekanizma', 'mek', 'Kondenser hava kanalı + braketleri (grupla gelir · FHP-M5 saplamalara)')
for nm, x0, x1 in (('evaporator_L', 1440, 1700), ('evaporator_R', 1750, 2230)):
    grup(nm, [o for o in S17 if o['lo'][0] >= x0 and o['hi'][0] <= x1 and o['lo'][1] > 1250] + [o for o in KUL if o['dug'] == 'ELK_TOPPING__rakor' and x0 <= o['lo'][0] <= x1 and o['lo'][1] > 1500], 'alu', 'mek', 'Evaporatör kaseti %s (serpantin + fan + PU kaset + conta · TEK ÜRÜN)' % nm[-1])
kalan17 = [o for o in S17 if id(o) not in ATANAN]
print('soğutma kalan', [(o['dug'], np.round(o['lo']).tolist(), np.round(o['hi']).tolist()) for o in kalan17])

# kasetler + tahrik motorları
for kd, ad in (('TOPPING/Kaşar', 'kasar'), ('TOPPING/Sucuk', 'sucuk')):
    K_ = sec(lambda o: kod(o) == kd)
    grup('burc_motor_' + ad, [o for o in K_ if o['dug'] == 'TOPPING_MODUL__pom' and o['lo'][2] < -640 and o['hi'][2] > -570], 'koyu', 'mek', '%s motoru kaplin burcu POM (arka duvar geçişi)' % ad.capitalize())
    grup('motor_' + ad, [o for o in K_ if id(o) not in ATANAN and o['lo'][2] < -640 and o['hi'][2] < -500], 'motor', 'mek', '%s kaseti tahrik motoru (redüktör + flanş + kaplin · TEK ÜRÜN)' % ad.capitalize())
    grup('kaset_ray_' + ad, [o for o in K_ if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__paslanmaz' and o['lo'][1] > 1150 and o['hi'][1] < 1185 and o['lo'][2] < -500], 'mekanizma', 'mek', '%s kaseti rayı + 4 ayak (raf FHP-M5 saplamalarına)' % ad.capitalize())
    grup('kaset_' + ad + '_mandal', [o for o in K_ if id(o) not in ATANAN and o['hi'][1] < 1161 and o['hi'][0] < (1980 if ad == 'kasar' else 2312)], 'koyu', 'mek', '%s kaseti kilit mandalı (POM yuva + yaylı dil · rafa gömülü)' % ad.capitalize())
    grup('kaset_' + ad + '_conta', [o for o in K_ if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__conta' and o['hi'][1] < 1153], 'yapistirici', 'mek', '%s kovanı raf contası' % ad.capitalize())
    grup('kaset_' + ad + '_cikis', [o for o in K_ if id(o) not in ATANAN and o['hi'][1] < 1150], 'mekanizma', 'mek', '%s çıkış ağzı (kovanın içinde sabit · alttan takılır)' % ad.capitalize())
    grup('kaset_' + ad, [o for o in K_ if id(o) not in ATANAN], 'alu', 'mek', '%s kaseti (hazne + helezon + karıştırıcı · TEK ÜRÜN, dil kanalından sürülür)' % ad.capitalize())

# UNO'lar: arka grup (silindir + piston + duvar flanşı + burç) · ön grup (raf üstü) · çıkış (raftan aşağı)
for kd, ad in (('TOPPING/Kıyma', 'kiyma'), ('TOPPING/Kuşbaşı', 'kusbasi'), ('TOPPING/Sos', 'sos'), ('TOPPING/Harç', 'harc')):
    U = sec(lambda o: kod(o) == kd)
    grup('burc_uno_' + ad, [o for o in U if o['dug'] == 'TOPPING_MODUL__pom' and o['lo'][2] < -630 and o['hi'][2] > -570], 'koyu', 'mek', 'UNO %s piston burcu POM (arka duvar geçişi)' % ad)
    arka = [o for o in U if id(o) not in ATANAN and (o['hi'][2] < -650 or (o['lo'][2] < -560 and o['hi'][2] < -440 and (o['hi'] - o['lo'])[0] < 60 and o['lo'][1] > 1100)) and o['dug'] != 'TOPPING_MODUL__pom__PISTON_' + ad.upper()]
    arka = [o for o in arka if 'pom__PISTON' not in o['dug']]
    grup('uno_%s_arka' % ad, arka, 'alu', 'mek', 'UNO %s · arka grup (pnömatik silindir + piston + duvar flanşı + burç · üründen ayrılmış)' % ad)
    alt = [o for o in U if id(o) not in ATANAN and o['hi'][1] < 1182.5 and o['dug'] != 'TOPPING_MODUL__conta'] if ad in ('harc', 'sos') else []
    if ad in ('harc', 'sos'): grup('uno_%s_conta' % ad, [o for o in U if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__conta' and o['hi'][1] < 1153], 'yapistirici', 'mek', 'UNO %s kovanı raf contası' % ad)
    if alt: grup('uno_%s_cikis' % ad, alt, 'mekanizma', 'mek', 'UNO %s çıkış borusu + yayıcı (alttan kovana · üstte kelepçe)' % ad)
    if ad in ('harc', 'sos'):
        grup('uno_%s_hortum' % ad, [o for o in U if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__hortum_gida'], 'hava', 'kablo', 'UNO %s gıda hortumu (üst raf deliğinden kelepçeye)' % ad)
        grup('uno_%s_kelepce' % ad, [o for o in U if id(o) not in ATANAN and o['lo'][1] > 1181.5 and o['hi'][1] < 1216.5], 'baglanti', 'mek', 'UNO %s kelepçe (boru ↔ hortum, tri-clamp)' % ad)
    grup('uno_%s_on' % ad, [o for o in U if id(o) not in ATANAN], 'mekanizma', 'mek', 'UNO %s · ön grup (hazne + dozaj gövdesi + döner valf · TEK ÜRÜN gövdesi)' % ad)

# hava
H = sec(lambda o: kod(o) == 'TOPPING/Hava')
grup('valf_adasi', [o for o in H if o['dug'] in ('TOPPING_MODUL__siyah',) or (o['dug'] == 'TOPPING_MODUL__aluminyum' and o['lo'][0] < 2000)], 'motor', 'mek', 'Valf adası (12 valf · TEK ÜRÜN)')
grup('hava_hortum', [o for o in H if o['dug'] == 'TOPPING_MODUL__hava_ana'], 'hava', 'kablo', 'Hava hortumları (valf adası → UNO pistonları)')
for o in sorted([o for o in H if o['dug'] == 'HAVA_IC__aski'], key=lambda o: (o['lo'][2], o['lo'][0], o['lo'][1])):
    grup('hava_aski_%d_%d' % (round(o['lo'][0]), round(o['lo'][1])), [o], 'kanal', 'mek', 'Hava kanalı askısı (FHP-M5 saplamaya)')
for o in sorted([o for o in H if o['dug'] == 'HAVA_IC__kanal' and (o['hi'] - o['lo']).max() > 50], key=lambda o: o['lo'][0]):
    grup('hava_kanal_%d_%d' % (round(o['lo'][0]), round(o['lo'][1])), [o], 'kanal', 'mek', 'Hava kanalı (askılara oturur)')
J1 = sec(lambda o: o['dug'].startswith('ELK_ZINCIR') and kod(o) in ('TOPPING/Elektrik', 'TOPPING/Hava'))
grup('j1_panel', [o for o in J1 if not (o['dug'].endswith(('kablo_guc', 'kablo_veri')) or (o['dug'] == 'ELK_ZINCIR__hava' and o['lo'][1] < 1200))], 'fis', 'mek', 'J1 gömme fiş paneli (Harting güç + M12 bilgi + hava rakoru · hazır)')
grup('j1_kablo', [o for o in J1 if o['dug'].endswith(('kablo_guc', 'kablo_veri'))], 'guc', 'kablo', 'J1 iç bağlantı kabloları')
grup('hava_giris', [o for o in J1 if id(o) not in ATANAN] + [o for o in H if id(o) not in ATANAN], 'hava', 'kablo', 'Hava giriş hattı (J1 rakoru → valf adası)')

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
grup('kablo_guc', [o for o in E if o['dug'] == 'ELK_TOPPING__kablo'], 'guc', 'kablo', 'Güç kabloları (KIRMIZI · kanal boyunca)')
grup('kablo_bilgi', [o for o in E if o['dug'] == 'ELK_TOPPING__kablo_sinyal'], 'bilgi', 'kablo', 'Bilgi kabloları (MAVİ · kanal boyunca)')
for o in [o for o in kalan17 if id(o) not in ATANAN]:
    grup('sogutma_parca_%d_%d' % (round(o['lo'][0]), round(o['lo'][1])), [o], 'koyu', 'mek', '%s (soğutma)' % o['dug'].split('__')[-1])

# ---------------------------------------------------------------- çevre (silik)
CV = [o for o in KUL if id(o) not in ATANAN]
def cev(ad, f, ac):
    LL = [o for o in CV if id(o) not in ATANAN and f(o)]
    if not LL: return
    for o in LL: ATANAN.add(id(o))
    ekle(ad, *birles(LL), 'silik', 'cevre', ac)
cev('cevre_B', lambda o: o['dug'].startswith(('B_', 'CEK_', 'ELK_DOLAP', 'ELK_IC')) and o['hi'][1] < 800, 'B dolabı (silik çevre)')
cev('cevre_A', lambda o: o['dug'].startswith(('A_', 'KAIDE_A')), 'A (silik çevre · hat bağlantısında)')
cev('cevre_F', lambda o: o['dug'].startswith(('F_', 'U_', 'D_PIZZA', 'ELK_ZINCIR', 'ELK_ISTASYON')), 'F (silik çevre · hat bağlantısında)')
kalan = [o for o in KUL if id(o) not in ATANAN]
print('ATANMAYAN', len(kalan), collections.Counter((o['dug'], kod(o)) for o in kalan))
pickle.dump(dict(P=P, ENT=ENT), open('t3_parca_v4.pkl', 'wb'))
for a in sorted(P):
    if not (a.startswith(('servis_arka', 'arayuz_', 'kaide_ust_plaka_delik')) or 'kaynak' in a or 'dolgu' in a or 'silikonu' in a):
        print('%-34s %-9s %6d  lo %s hi %s' % (a, P[a]['m'], len(P[a]['F']), np.round(P[a]['V'].min(0)).astype(int).tolist(), np.round(P[a]['V'].max(0)).astype(int).tolist()))
print('TOPLAM', len(P))
