# -*- coding: utf-8 -*-
import os, sys, pickle, numpy as np, json
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y, trimesh, sac_morf_t5 as SM
P = pickle.load(open('t5_parca.pkl', 'rb'))['P']
s = SM.Sac('astar_arka'); X = s.dunya(s.yerel({})); tv = trimesh.Trimesh(P['astar_arka']['V'], P['astar_arka']['F'], process=False)
d = trimesh.proximity.closest_point(tv, X)[1]; far = X[d > 1.0]; print('astar_arka uzak açınım köşeleri', len(far), np.round(far.min(0), 1) if len(far) else '', np.round(far.max(0), 1) if len(far) else '')
VEK = {}
def tri(a):
    if a not in VEK: VEK[a] = Y._vekil(P[a]['V'] / 1000.0, np.asarray(P[a]['F']))
    return VEK[a]
LO = {a: P[a]['V'].min(0) for a in P}; HI = {a: P[a]['V'].max(0) for a in P}
def serbest(adlar, ofs, yerinde, ofs2=None):
    ofs = np.asarray(ofs, float); ofs2 = np.zeros(3) if ofs2 is None else np.asarray(ofs2, float)
    v = (ofs2 - ofs) / 1000.0; sorun = []
    for a in adlar:
        A0 = tri(a) + ofs / 1000.0
        l = (np.minimum(LO[a] + ofs2, LO[a] + ofs)) / 1000.0; h = (np.maximum(HI[a] + ofs2, HI[a] + ofs)) / 1000.0
        for b in yerinde:
            if b in adlar: continue
            if np.any(LO[b] / 1000.0 > h + 1e-4) or np.any(HI[b] / 1000.0 < l - 1e-4): continue
            B = tri(b)
            amn = np.minimum(A0.min(1), (A0 + v).min(1)); amx = np.maximum(A0.max(1), (A0 + v).max(1))
            sa = np.all(amn <= HI[b] / 1000.0 + 1e-4, 1) & np.all(amx >= LO[b] / 1000.0 - 1e-4, 1)
            if not sa.any(): continue
            smn = amn[sa].min(0); smx = amx[sa].max(0)
            sb = np.all(B.min(1) <= smx + 1e-4, 1) & np.all(B.max(1) >= smn - 1e-4, 1)
            if not sb.any(): continue
            lam = Y.ccd(np.ascontiguousarray(A0[sa]), np.ascontiguousarray(B[sb]), v.astype(np.float64), Y.SINIR)
            m = lam < 1.5
            if not m.any(): continue
            pts = lam[m][:, None] * v[None, :]
            der = np.minimum(np.linalg.norm(pts - v[None, :], axis=1), np.linalg.norm(pts, axis=1))
            if der.max() > Y.OTURMA:
                k = int(np.argmax(der)); hit = (A0[sa][m][k] + pts[k]).mean(0) * 1000
                sorun.append((a, b, round(float(der.max()) * 1000, 1), np.round(hit, 1).tolist()))
    return sorun
def test(baslik, adlar, yerinde, yollar):
    print('==', baslik)
    for y in yollar:
        s = serbest(adlar, np.array(y, float), yerinde)
        print('   yön', y, 'TEMİZ' if not s else s[:6])
KABUK = ['dis_taban', 'dis_yan_sol', 'dis_yan_sag', 'dis_tavan', 'kaide_ust_plaka_4'] + [a for a in P if a.startswith(('arayuz_mek_taban', 'arayuz_mek_yan', 'servis_arka_taban', 'servis_arka_yan', 'pem_M8', 'kaide_plaka_pem'))]
test('teknik_on_perde', ['teknik_on_perde'], KABUK, [(0, 600, 0), (0, 0, -900), (0, 0, 900), (0, 300, -900), (0, 300, 900)])
Vt = P['dis_taban']['V']; Vp = P['teknik_on_perde']['V']
print('perde y', Vp[:, 1].min(), 'taban üst y (orta)', Vt[(Vt[:, 2] > -480) & (Vt[:, 2] < -450) & (Vt[:, 0] > 1600) & (Vt[:, 0] < 1700)][:, 1].max())
for a in sorted(a for a in P if a.startswith('arayuz_mek_taban')): print('  ', a, np.round(LO[a]).tolist(), np.round(HI[a]).tolist())
test('astar_sol+pu_sol önden (yerinde: arka PU + dış)', ['astar_sol', 'pu_levha_sol'], ['pu_levha_arka', 'yapistirici_arka', 'soguk_arka_dis_sac', 'dis_tavan', 'dis_yan_sol', 'soguk_alt_sac'], [(0, 0, 900), (0, 2, 900), (0, -2, 900), (0, 5, 900)])
test('astar_sol tek önden (yerinde: 4 PU)', ['astar_sol'], ['pu_levha_arka', 'pu_levha_sol', 'pu_levha_tavan', 'soguk_arka_dis_sac', 'dis_tavan', 'dis_yan_sol', 'soguk_alt_sac'], [(0, 0, 900), (0, 2, 900), (0, -2, 900), (30, 0, 900), (-30, 0, 900)])
test('pu_levha_tavan önden (yerinde: astar sol/sag)', ['pu_levha_tavan'], ['astar_sol', 'astar_sag', 'pu_levha_arka', 'dis_tavan', 'pu_levha_sol', 'pu_levha_sag'], [(0, 0, 900), (0, -2, 900)])
test('pu_levha_tavan önden (yerinde: yalnız PU)', ['pu_levha_tavan'], ['pu_levha_arka', 'dis_tavan', 'pu_levha_sol', 'pu_levha_sag', 'yapistirici_tavan'], [(0, 0, 900), (0, -2, 900)])
test('astar_tavan önden (yerinde: 4 PU)', ['astar_tavan'], ['pu_levha_arka', 'pu_levha_sol', 'pu_levha_sag', 'pu_levha_tavan', 'soguk_arka_dis_sac', 'dis_tavan'], [(0, 0, 900), (0, 2, 900), (0, -2, 900)])
test('astar_tavan önden (yerinde: 4 PU + astar sol/sag)', ['astar_tavan'], ['pu_levha_arka', 'pu_levha_sol', 'pu_levha_sag', 'pu_levha_tavan', 'astar_sol', 'astar_sag'], [(0, 0, 900), (0, 2, 900), (0, -2, 900)])
test('astar_sol önden (yerinde: 4 PU + astar_tavan)', ['astar_sol'], ['pu_levha_arka', 'pu_levha_sol', 'pu_levha_tavan', 'astar_tavan', 'soguk_alt_sac'], [(0, 0, 900), (0, 2, 900), (0, -2, 900)])
test('astar_arka önden (yerinde: 4 PU + 3 astar)', ['astar_arka'], ['pu_levha_arka', 'pu_levha_sol', 'pu_levha_sag', 'pu_levha_tavan', 'astar_sol', 'astar_sag', 'astar_tavan', 'soguk_alt_sac'], [(0, 0, 900), (0, 0, 300)])
test('pu_levha_sol önden (yerinde: arka PU, dış)', ['pu_levha_sol'], ['pu_levha_arka', 'dis_tavan', 'dis_yan_sol', 'soguk_alt_sac', 'yapistirici_sol'], [(0, 0, 900)])
test('pu_levha_arka önden', ['pu_levha_arka'], ['soguk_arka_dis_sac', 'dis_tavan', 'dis_yan_sol', 'dis_yan_sag', 'soguk_alt_sac', 'yapistirici_arka'] + [a for a in P if a.startswith('evap_kanal_kovani')], [(0, 0, 900)])
test('raf_kosebendi_sol üstten (yerinde: pu_raf_esik)', ['raf_kosebendi_sol'], ['pu_raf_esik', 'soguk_alt_sac', 'astar_sol'], [(0, 600, 0), (0, 0, 900)])
test('pu_raf_esik üstten (yerinde: köşebentler, kovanlar)', ['pu_raf_esik'], ['raf_kosebendi_sol', 'raf_kosebendi_sag', 'soguk_alt_sac', 'astar_sol', 'astar_sag', 'astar_arka'] + [a for a in P if a.startswith('dusme_kovani')], [(0, 600, 0), (0, 0, 900), (0, 100, 900)])
test('pu_raf_esik üstten (yerinde: yalnız kovanlar)', ['pu_raf_esik'], ['soguk_alt_sac', 'astar_sol', 'astar_sag', 'astar_arka'] + [a for a in P if a.startswith('dusme_kovani')], [(0, 600, 0), (0, 0, 900)])
test('raf üstten (yerinde: pu_raf, köşebent, kovan, astar)', ['raf'], ['pu_raf_esik', 'raf_kosebendi_sol', 'raf_kosebendi_sag', 'soguk_alt_sac', 'astar_sol', 'astar_sag', 'astar_arka'] + [a for a in P if a.startswith('dusme_kovani')], [(0, 600, 0), (0, 0, 900), (0, 60, 900), (0, 100, 900)])
test('ust_raf önden (yerinde: astar, köşebent)', ['ust_raf'], ['ust_raf_kosebendi_sol', 'ust_raf_kosebendi_sag', 'astar_sol', 'astar_sag', 'astar_arka'], [(0, 0, 900), (0, 20, 900), (0, 40, 900)])
UNOY = ['ust_raf', 'astar_tavan', 'astar_arka', 'astar_sol', 'astar_sag', 'raf', 'pu_levha_tavan', 'uno_kiyma_dirsek']
for u in ('uno_patates_on', 'uno_harc_on', 'uno_kiyma_on'):
    test(u + ' önden', [u], [x for x in UNOY if x != u], [(0, 0, 900), (0, 37, 900), (0, 40, 900), (0, 45, 900), (0, 60, 900), (0, 100, 900), (0, 0, 300)])
test('uno_kiyma_dirsek önden (yerinde: ust_raf, uno_kiyma_on)', ['uno_kiyma_dirsek'], ['ust_raf', 'uno_kiyma_on', 'astar_arka', 'uno_kiyma_raf_conta'], [(0, 0, 900), (0, 20, 900), (0, 50, 900)])
test('uno_kiyma_on önden (yerinde: dirsek yok)', ['uno_kiyma_on'], ['ust_raf', 'astar_tavan', 'astar_arka', 'uno_harc_on', 'uno_patates_on'], [(0, 0, 900), (0, 40, 900)])
test('x_ekseni A tarafından', ['x_ekseni'], ['dis_yan_sol', 'dis_yan_sag', 'dis_taban', 'uno_patates_cikis', 'uno_harc_cikis', 'uno_kiyma_cikis', 'x_motor', 'kaset_kasar_cikis', 'kaset_sucuk_cikis', 'soguk_alt_sac', 'on_alt_braket', 'teknik_on_perde'] + [a for a in P if a.startswith('arayuz_mek_taban')], [(-1700, 0, 0), (-1700, 5, 0), (-1700, 10, 0), (0, 0, 900), (0, 10, 900)])
test('x_ekseni+x_motor A tarafından', ['x_ekseni', 'x_motor'], ['dis_yan_sol', 'dis_yan_sag', 'dis_taban', 'uno_patates_cikis', 'uno_harc_cikis', 'uno_kiyma_cikis', 'kaset_kasar_cikis', 'kaset_sucuk_cikis', 'soguk_alt_sac', 'teknik_on_perde', 'ayirma_perdesi_cep_sol', 'teknik_sag_perde'] + [a for a in P if a.startswith(('arayuz_mek_taban', 'arayuz_mek_yan'))], [(-1700, 0, 0), (-1700, 5, 0), (0, 0, 900), (0, 10, 900)])
test('evaporator_L arkadan', ['evaporator_L', 'evaporator_ayagi_0', 'evaporator_ayagi_1'], ['dis_yan_sol', 'dis_tavan', 'kuru_bolme_tabani', 'soguk_arka_dis_sac', 'dis_taban'] + [a for a in P if a.startswith(('evap_kanal_kovani', 'pem_M8_A', 'servis_arka_yan_sol', 'arayuz_mek_kuru'))], [(0, 0, -900), (0, 20, -900), (30, 0, -900)])
test('evaporator_R arkadan', ['evaporator_R', 'evaporator_ayagi_2', 'evaporator_ayagi_3'], ['dis_yan_sag', 'dis_tavan', 'kuru_bolme_tabani', 'soguk_arka_dis_sac', 'dis_taban', 'burc_kilifi_kiyma', 'burc_uno_kiyma'] + [a for a in P if a.startswith(('evap_kanal_kovani', 'arayuz_mek_kuru', 'arayuz_mek_soguk'))], [(0, 0, -900), (0, 20, -900)])
test('elk_kanal_2385_915', ['elk_kanal_2385_915'], ['dis_yan_sag', 'dis_taban', 'soguk_alt_sac', 'teknik_sag_perde'] + [a for a in P if a.startswith(('arayuz_mek_yan', 'pem_M8_F', 'arayuz_j1'))], [(0, 0, -900), (0, 0, 900), (0, 600, 0), (-100, 0, 0), (-100, 0, 900)])
print(sorted(a for a in P if a.startswith('elk_')))
