# -*- coding: utf-8 -*-
"""K (KESME) MONTAJ ANİMASYONU — Claude planı (6 Eki 2026 · Codex devri üstüne, kendi yöntemi)
Girdi: k_parca_c.pkl (zincir 86 sonrası model · ad aktarımlı) · k_deg.json (bağlantı elemanı → değdiği taşıyıcılar) ·
       veri/86_k_baglanti.json (yeni bağlantı elemanlarının giriş ekseni) · plan_k_clip_full.pkl (Codex: mevcut elemanların giriş ekseni)
Çıktı: plan_k_c.pkl → k_cikti_c.py
Kemal (6 Eki): "parçaları bütün olarak alma, her parça üretilip montajlanacak". Kural: her parça TEK TEK gelir; sac önce açınım → büküm;
bağlantı elemanı (vida / somun / pul / perçin / PEM / pim) değdiği taşıyıcıların hepsi yerindeyken TEK TEK kendi ekseninde; kaynak dikişi
birleştiği parçalar yerindeyken belirir. Yalnız pano grubu tezgâhta (arka sac + burçlar + pano + DIN + cihazlar + valf adası) — tezgâhta da
parça parça kurulur, sonra bütün olarak arkadan girer (KURALLAR §2.3 kural 12)."""
import sys, os, json, pickle, math, time, collections, re as _re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, '_local', 'claude_son_yerel', 'gece2', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
from scipy.spatial import cKDTree
T0 = time.time()
D0 = pickle.load(open('k_parca_c.pkl', 'rb')); P = D0['P']
DEG = json.load(open('k_deg.json', encoding='utf-8'))
V86 = json.load(open(os.path.join(ROOT, 'arastirma', '_uretec', 'h3', 'yama_v9', 'veri', '86_k_baglanti.json'), encoding='utf-8'))
CP = pickle.load(open('plan_k_clip_full.pkl', 'rb'))
for a in [a for a in P if a.startswith('cevre_') and a not in ('cevre_B', 'cevre_F', 'cevre_U', 'cevre_diger')]: del P[a]

# ------------------------------------------------------------------ sac: Codex kaynak büküm verisi (KD eşleme; delik köşeleri en yakın kaynak köşeyi izler)
SAC = {}
try:
    SRC = os.path.join(ROOT, 'arastirma', '_uretec', 'codex', 'k_montaj', 'bend_paths.py')
    ns = {'__file__': SRC}; exec(compile(open(SRC, encoding='utf-8').read().split('rows=[]')[0], SRC, 'exec'), ns); _decode = ns['decode']
    BEND = json.load(open('current_sheet_bending_head.json', encoding='utf-8'))
    INV = json.load(open(os.path.join(ROOT, '_local', 'codex_k_montaj', 'source_cad_inventory.json'), encoding='utf-8'))
    FLAT = {s['name']: s['flat'] for s in INV['sheets']}
    ALIAS = {'onyuz_kapak_K': ['k_govde_on_seffaf_0', 'k_govde_on_seffaf_2', 'k_govde_on_seffaf_3'], 'onyuz_kapak_K_ic_tava': ['k_govde_on_seffaf_1']}
    class Sac:
        def __init__(s, rec, V, idx, flat):
            s.rec = rec; s.V = V; s.idx = idx; s.t = rec['t']
            by = {b['number']: b for b in rec['bends']}
            s.bukum = [{'no': i + 1, 'aci': abs(float(np.degrees(by[n]['angle']))), 'R': float(by[n]['BA'] / abs(by[n]['angle']) - by[n]['K'] * rec['t']), 'ad': 'büküm %d' % n}
                       for i, n in enumerate(rec['order'])]
            if 'levha' in flat: s.levha = {'boy': flat['levha']['boy'], 'en': flat['levha']['en']}
            else:
                v = _decode(rec, 0.); sp = np.ptp(v, axis=0); ax = np.argsort(sp)[-2:]; s.levha = {'boy': float(sp[ax[1]]), 'en': float(sp[ax[0]])}
        def yerel(s, st): return _decode(s.rec, sum(st.get(b['no'], 0.) for b in s.bukum) / max(1, len(s.bukum)))
        def dunya(s, loc):
            m = np.asarray(s.rec['root']); w = loc @ m[:3, :3].T + m[:3, 3] + np.asarray(s.rec['source_offset']); return w[s.idx]
    for rec in BEND['sheets']:
        for a in rec.get('target_parts', ALIAS.get(rec['name'], [rec['name']])):
            if a not in P: continue
            V = np.asarray(P[a]['V']); d, idx = cKDTree(np.asarray(rec['vertices'])).query(V)
            if d.max() > 2.5 or not rec.get('bends'): continue
            SAC[a] = Sac(rec, V, idx, FLAT.get(rec['name'], {}))
except Exception as ex:
    print('sac büküm verisi yok:', ex)
print('bükümlü sac', len(SAC))

AD_TR = [(r'^taban_sac$', 'Taban sacı 3 mm'), (r'^taban_sac_tasiyici', 'Taban taşıyıcı profil'), (r'^kose_dikmesi_\d+_-?\d+$', 'Köşe dikmesi 30 × 30'),
         (r'^onyuz_kayit', 'Kayıt profili'), (r'^kopru_kirisi_yan', 'Köprü yan kirişi'), (r'^kopru_kirisi', 'Köprü kirişi'), (r'^govde_kulak', 'Panel kulağı 3 mm'),
         (r'^k71_alt_flans', 'Destek alt flanşı'), (r'^k71_dik_destek', 'Dik destek'), (r'^k71_disli_ust_kapak', 'Destek üst kapağı (dişli)'), (r'^k71_istasyon_rafi', 'İstasyon rafı'),
         (r'^k71_raf_yan_sac', 'Raf yan sacı'), (r'^itici_sabit_plaka', 'X taban plakası 6082 6 mm'), (r'^itici_X_ray', 'HIWIN MGNR15R ray (X)'), (r'^itici_X_blok', 'HIWIN MGN15H blok (X)'),
         (r'^itici_Z_ray', 'HIWIN MGNR15R ray (Z)'), (r'^itici_Z_blok', 'HIWIN MGN15H blok (Z)'), (r'^itici_X_ara', 'X ara plakası'), (r'^itici_Z_plaka', 'Z taban plakası'),
         (r'^itici_Z_yukseltme', 'Z yükseltmesi'), (r'^itici_Z_kopru', 'Z köprüsü'), (r'^itici_[XZ]_MY1B10G-\d+_uc_kapagi', 'MY1B silindir uç kapağı'),
         (r'^itici_[XZ]_MY1B10G-\d+_profil', 'SMC MY1B rodless silindir'), (r'^itici_[XZ]_MY1B10G-\d+_masa', 'MY1B silindir arabası'), (r'^itici_X_durdurucu', 'X durdurucu braketi'),
         (r'^itici_one_kol', 'İtici kolu (öne)'), (r'^itici_dusey_kol', 'İtici kolu (düşey)'), (r'^itici_yatay_kol', 'İtici kolu (yatay)'), (r'^itici_yuz$', 'POM itici yüzü'),
         (r'^bant_yan', 'Bant yan profili'), (r'^bant_traversi', 'Bant traversi'), (r'^kayma_tablasi', 'UHMW kayma tablası'), (r'^cit_braketi', 'Çit braketi'), (r'^cit_', 'POM kılavuz çit'),
         (r'^kafa_plakasi', 'Kesici kafa plakası'), (r'^kafa_adaptoru', 'Kafa adaptörü'), (r'^ara_dikme', 'Kafa ara dikmesi'), (r'^bicak_gobek', 'Bıçak seti göbeği'), (r'^bicak_\d', 'Bıçak dilimi'),
         (r'^bicak_koruma', 'Bıçak koruma halkası'), (r'^koruma_braketi', 'Koruma braketi'), (r'^DGRF', 'Festo DGRF kesici silindiri'), (r'^yag_pompa_rafi', 'Yağ pompası rafı'),
         (r'^pano_plakasi', 'Pano plakası'), (r'^arka_sac', 'Arka sac 1,5'), (r'^ust_sac', 'Üst sac 1,5'), (r'^sol_sac', 'Sol sac (ürün girişi)'), (r'^sag_sac', 'Sağ sac (E penceresi)')]
def bk(x): return x.replace('_', ' ')
def tr(a):
    for d_, t_ in AD_TR:
        if _re.search(d_, a): return t_
    ac = str(P[a].get('ac', a)) if a in P else a
    return ac.split('·')[0].split(';')[0].strip()[:60]
CEVRE = [a for a in P if a.startswith('cevre')]
def kutu(a): return P[a]['V'].min(0), P[a]['V'].max(0)

# ------------------------------------------------------------------ bağlantı elemanı giriş ekseni (eks): 86 verisi · Codex hareketi · geometri
EKS86 = {e['ad']: e for e in V86['eleman']}
for a in P:
    if P[a]['tur'] not in ('baglanti',): continue
    if a in EKS86 and 'eks' in EKS86[a]:
        P[a]['eks'] = np.asarray(EKS86[a]['eks'], float); continue
    h = CP['HAR'].get(a) or []
    if h:
        v = -np.asarray(h[-1][2:5], float)
        if np.linalg.norm(v) > 1e-9: P[a]['eks'] = v / np.linalg.norm(v); continue
    l, hh = kutu(a); ax = int(np.argmax(hh - l)); v = np.zeros(3); v[ax] = -1.0; P[a]['eks'] = v
PEM_SAC = {}
def pem_bagla(p, s, yan, ad):
    P[p]['sac'] = s; P[p]['yan'] = np.asarray(yan, float); P[p]['pem_ad'] = ad; PEM_SAC.setdefault(s, []).append(p)
for a in P:
    if P[a]['tur'] != 'baglanti': continue
    if _re.search(r'PEM|FHP|_pem_|saplama', a) and DEG.get(a):
        sacs = [b for b in DEG[a] if P[b]['tur'] == 'sac']
        if sacs and not a.startswith('kb_bicak') and 'avara' not in a:
            pem_bagla(a, sacs[0], -P[a]['eks'], 'preslenmiş saplama / somun')

exec(open(os.path.join(HERE, '_altyapi_c.py'), encoding='utf-8').read())
_sk = sac_kareleri
def sac_kareleri(a):                                                             # son kare = model (delik köşeleri en yakın kaynak köşeyi izler)
    k = _sk(a)
    if not k: return k
    r = k[-1]
    return [x - r for x in k]

# ------------------------------------------------------------------ plan yardımcıları
for s_, L_ in PEM_SAC.items():
    for p in L_: HARIC_PLAN.add((p, s_))
def haric(a, b, neden): HARIC_PLAN.add((a, b)); HARIC_NEDEN[(a, b)] = neden
UST6, ON9, ARKA9, SOL7, SAG7 = (0, 650, 0), (0, 0, 900), (0, 0, -900), (-700, 0, 0), (700, 0, 0)
SON = [(0, 30, 0), (0, 15, 0), (0, -15, 0), (15, 0, 0), (-15, 0, 0), (0, 0, 15), (0, 0, -15), (30, 0, 0), (-30, 0, 0), (0, 0, 30), (0, 0, -30)]
def AD(*yon, lift=(20, 60, 150), yan=(), son=SON):
    L_ = [YOL(d) for d in yon]
    for d in yon:
        for e in son: L_.append(YOL(d, e))
        for h in lift: L_.append(YOL(d, (0, h, 0)))
        for x in yan: L_.append(YOL(d, (x, 0, 0)))
    return L_
YERLESEN = set(CEVRE); BEKLEYEN = [a for a in P if P[a]['tur'] in ('baglanti', 'kaynak', 'silikon') and a not in PEM_SAC.get(P[a].get('sac'), [])]
PEM_SET = set(p for L_ in PEM_SAC.values() for p in L_)
BEKLEYEN = [a for a in BEKLEYEN if a not in PEM_SET]
def sira(a):
    return (0 if '_pul' in a else (1 if _re.search(r'vida|civata|saplama|pim|M\d+x', a) else 2), a)
def baglantilar(t0, ofs0=None, grup=None):
    """yerindeki taşıyıcılara değen ve hepsi yerinde olan bağlantı elemanlarını takar / kaynakları büyütür → bitiş zamanı"""
    global BEKLEYEN
    tt = t0; hazir = []
    kume = YERLESEN if grup is None else set(grup)
    for f in BEKLEYEN:
        d = DEG.get(f) or []
        if d and all(x in kume for x in d): hazir.append(f)
    if not hazir: return tt
    hs = set(hazir); BEKLEYEN = [f for f in BEKLEYEN if f not in hs]
    vid = sorted([f for f in hazir if P[f]['tur'] == 'baglanti'], key=sira); kay = [f for f in hazir if P[f]['tur'] != 'baglanti']
    for i, f in enumerate(vid):
        tt = max(tt, tak(f, t0 + i * 0.08, 0.4, 20.0, ofs0=ofs0)); YERLESEN.add(f)
        if ofs0 is not None and grup is not None: grup.append(f)
    for f in kay:
        if ofs0 is None: buyu(f, tt, 0.5)
        else:
            basla(f, ofs0, tt); ISTISNA.add(f); MF[f] = dict(buyu=[round(tt, 3), round(tt + 0.5, 3)]); VU[f].append([round(tt, 3), round(tt + 1.2, 3)])
            if grup is not None: grup.append(f)
        YERLESEN.add(f)
    if kay: tt += 0.5
    if vid: olay(t0, '%d bağlantı elemanı (%s)' % (len(vid), ', '.join(sorted(set(tr(f)[:28] for f in vid))[:3])))
    if kay: olay(t0, '%d kaynak dikişi / punta' % len(kay))
    return tt
def koy1(a, adaylar, metin=None, bekle=0.1):
    """tek parça: (sacsa açınım + büküm + PEM) → yerine; ardından hazır bağlantı elemanları"""
    global t
    pem = sorted(PEM_SAC.get(a, []))
    t = yerlestir([a], adaylar, t, metin or '%s → yerine' % tr(a), pem=pem, sure_bekle=bekle)
    YERLESEN.add(a); YERLESEN.update(pem)
    t = baglantilar(t)
    return t
def tezgah(adlar, adaylar, metin):
    """tezgâh grubu: parçalar tezgâhta tek tek (bağlantıları, kaynakları), sonra grup yolu boyunca yerine"""
    global t
    yol = yol_sec(adlar, adaylar); ofs = yol[0]; tt = t; grup = []
    for a in adlar:
        basla(a, ofs + np.array([0, 150.0, 0]), tt); git(a, ofs, tt, 0.35); vurgu([a], tt + 0.2, tt + 0.9)
        for p in PEM_SAC.get(a, []): basla(p, ofs, tt + 0.1); grup.append(p)
        grup.append(a); tt += 0.3
        tt = baglantilar(tt, ofs0=ofs, grup=grup)
    olay(t, metin + ' · tezgâhta')
    L = float(sum(np.linalg.norm(b - a) for a, b in zip(yol[:-1], yol[1:]))); su_t = max(0.4 * (len(yol) - 1), L / 1000.0)
    for p0, p1 in zip(yol[:-1], yol[1:]):
        su = max(su_t * float(np.linalg.norm(p1 - p0)) / max(L, 1e-6), 0.3)
        for a in grup: git(a, CUR[a] + (p1 - p0), tt, su)
        tt += su
    for a in grup: YER[a] = tt
    YERINDE.extend(grup); YERLESEN.update(grup)
    olay(tt - 0.2, metin + ' → yerine')
    t = baglantilar(tt)
    return t
def sec(*desen, haric_=()):
    L_ = [a for a in P if any(_re.search(d, a) for d in desen) and P[a]['tur'] not in ('baglanti', 'kaynak', 'silikon', 'kablo') and a not in YERLESEN and not any(_re.search(h, a) for h in haric_)]
    return sorted(L_, key=lambda a: (kutu(a)[0][1], kutu(a)[0][0], kutu(a)[0][2]))
def adim_parca(ad, metin, desenler, adaylar, kamera=None, haric_=()):
    global t
    adim(ad, metin, ', '.join(sorted(set(tr(a) for a in sec(*desenler, haric_=haric_))))[:300])
    L_ = sec(*desenler, haric_=haric_)
    if not L_: return
    kamera_genel(kamera or L_, yon=(0.45, 0.5, 0.75), olcek=1.6)
    for a in L_: koy1(a, adaylar)
    t += 0.2
KAM.append([0.0, [5.0, 2.6, 2.4], [4.2, 1.2, -0.4]])
basla('cevre_B', np.zeros(3), 0.0); YER['cevre_B'] = 0.0; YERINDE.append('cevre_B')
t = 0.4
TEPE = AD(UST6, lift=(), son=SON)
ONDEN = AD(ON9, UST6, lift=(20, 60), son=SON)
ARKADAN = AD(ARKA9, UST6, lift=(20, 60), son=SON)
HER = AD(UST6, ON9, ARKA9, lift=(20, 60), son=SON)
# ================================================================== PLAN
adim_parca('Taban ve taşıyıcılar', 'Taban sacı (3 mm) B dolabının üstüne; altındaki taşıyıcı profiller ve kovanlar yerinde TIG.',
           [r'^taban_sac'], TEPE)
adim_parca('Destekler', '6 destek: alt flanş tabandaki saplamalara (pul + somun), dik destek ve dişli üst kapak üstüne TIG.',
           [r'^k71_alt_flans', r'^k71_dik_destek', r'^k71_disli_ust_kapak'], TEPE)
adim_parca('İstasyon rafı', 'İstasyon rafı ve yan sacları desteklere (havşa vidalar), yan kaynaklar; raf PEM somunları preslenmiş gelir.',
           [r'^k71_istasyon_rafi', r'^k71_raf_yan_sac', r'^k_govde_conta'], TEPE)
adim_parca('Çerçeve', 'Köşe dikmeleri, kayıtlar, köprü kirişleri ve panel kulakları: parça parça yerinde TIG; dikme tapaları.',
           [r'^kose_dikmesi', r'^onyuz_kayit', r'^kopru_kirisi', r'^govde_kulak'], HER)
adim_parca('İtici ve bant ayakları', 'İtici taban / üst plakaları, ayaklar, bant ayakları, flanşlar, dişli plakalar ve tapalar (raf üstüne vidalı, yerinde TIG).',
           [r'^k72_', r'^itici_taban', r'^k_itici_sac', r'^bant_ayagi', r'^k79_bant'], HER)
adim_parca('Bant', 'Bant yan profilleri, traversler (TIG), UHMW kayma tablası (havşa M5), avara mili + rulo (mil ucu somunla), tahrik rulosu, ölü plaka.',
           [r'^bant_yan', r'^bant_traversi', r'^kayma_tablasi', r'^avara_mili', r'^avara_rulosu', r'^tahrik_rulosu', r'^olu_plaka'], HER)
adim_parca('Çit ve ürün sensörleri', 'Çit braketleri ve sensör L braketleri bant profiline TIG; POM çitler M3, fotoseller M3 ile.',
           [r'^cit_', r'^urun_sensoru'], HER)
adim_parca('İtici X ekseni', 'X taban plakası (4 × M5), HIWIN raylar (M3 × 40 adım), bloklar, MY1B silindir (uç kapakları alttan M4), durdurucular, şok emiciler, hız valfleri, oto svicler, ara plakalar, yüzer bağlantı.',
           [r'^itici_sabit_plaka', r'^itici_X_'], HER)
adim_parca('İtici Z ekseni ve kol', 'Z plakası, yükseltmeler (perçin somun), raylar, bloklar, Z silindiri, köprü, yüzer pim, itici kolu (kaynaklı: öne + düşey + yatay + kılavuz kovanı), POM itici yüzü.',
           [r'^itici_Z_', r'^itici_yuzer', r'^itici_one_kol', r'^itici_dusey_kol', r'^itici_yatay_kol', r'^itici_yuz'], HER)
adim_parca('Kesici silindiri', 'Festo DGRF-C-63 silindiri köprü kirişine bağlantı plakasıyla (4 × M10), kılavuz milleri, boyunduruk, sensör rayı ve sensörler, rakorlar.',
           [r'^DGRF'], HER)
adim_parca('Kesici kafa', 'Kafa adaptörü boyunduruğa (4 × M8 havşa), ara dikmeler, kafa plakası (3 × M8 havşa), bıçak seti (göbek: merkez M8 saplama + 2 pim, kelebek somun — aletsiz söküm), koruma braketleri + halkası (TIG).',
           [r'^kafa_adaptoru', r'^k79_kafa_adaptor', r'^ara_dikme', r'^kafa_plakasi', r'^k79_kafa_ust', r'^bicak', r'^kelebek_somun', r'^koruma_braketi'], HER)
adim_parca('Yan saclar', 'Sol sac (ürün girişi) ve sağ sac (E penceresi): kulaklara pul + fiberli somun; nozül braketi, kapama yaması.',
           [r'^sol_sac', r'^sag_sac', r'^k_e4_sol_yama'], AD(SOL7, SAG7, UST6, lift=(20,), son=SON))
adim_parca('Sprey nozülü', 'Nozül braketi sol saca (PEM saplama + somun), kelepçe bloğu (2 × M4), PulsaJet nozül + uç + kapak + dirsek + M8 soket.',
           [r'^nozul_', r'^PulsaJet'], HER)
adim_parca('Yağ sistemi', 'Pompa rafı + köşebentler (yan saclara saplama), pompa plakası, portallar (kaynaklı ayaklar), dişli pompa, emiş filtresi, borular, T parçası, basınç sensörü, geri basınç regülatörü.',
           [r'^yag_pompa_rafi', r'^k79_yag_raf', r'^yag_pompa_plakasi', r'^k79_', r'^yag_pompasi', r'^yag_emis_filtresi', r'^yag_boru', r'^yag_T', r'^yag_basinc', r'^yag_geri'], HER)
adim_parca('Tartı ve teneke', 'Damlama tavası F rafına, tartı tabanı; alt takoz + yük hücresi (alttan 2 × M6), üst takoz + platform (üstten 2 × M6), 18 L teneke, kapak adaptörü, emme lansı, kaplinler.',
           [r'^yag_damlama', r'^yag_tarti', r'^yag_tenekesi', r'^k_yag_pom', r'^yag_emme', r'^d3_', r'^k76_'], AD(UST6, ON9, SOL7, lift=(20, 60), son=SON))
PANO = sec(r'^arka_sac', r'^pano_ara_burcu', r'^pano_plakasi', r'^din_rayi', r'^plc_', r'^guc_', r'^sigorta', r'^klemens', r'^valf_', r'^sartlandirici', r'^elk_k_celik', r'^k_elektrik_sac')
adim('Arka sac ve pano', 'Tezgâhta: arka sac, burçlar, pano plakası (havşa M5), DIN raylar (M5), PLC + tartı modülü + güç kaynağı + sigorta + klemens (DIN rayına geçme), valf adası + valfler (M3) + rakorlar, şartlandırıcı; elektrik sacı mesafe braketlerine (M5). Grup arkadan.',
     'arka sac + pano grubu')
kamera_genel(PANO, yon=(0.4, 0.45, -0.85), olcek=1.3)
tezgah(PANO, AD(ARKA9, lift=(5, 20), son=()), 'Arka sac + pano grubu')
adim_parca('Kanallar ve fiş paneli', 'Kablo kanalları (M4 bombe başlı), fiş paneli (mesafe parçaları TIG, Harting tabanları M4, başlıklar kilit koluyla, M12 soketler ve rakorlar kendi somunlarıyla), etiketler, kablo bağı tabanları.',
           [r'^elk_', r'^hava_ic_', r'^emniyet_sari'], HER)
adim('Kablolar ve hortumlar', 'Güç (kırmızı), bilgi (mavi) kabloları, hava ve yağ hortumları, PU bant kanallar boyunca.', 'kablolar · hortumlar · bant')
for a in sorted(a for a in P if P[a]['tur'] == 'kablo' and a not in YERLESEN): buyu(a, t, 1.0); YERLESEN.add(a)
olay(t, 'Kablolar ve hortumlar yerinde'); t += 1.2
t = baglantilar(t)
adim_parca('Üst sac', 'Üst sac (tavan bağlantı plakaları kaynaklı) yukarıdan, kulaklara somunlar.', [r'^ust_sac', r'^k73_'], TEPE)
adim_parca('Ön kapak', 'Menteşe gövdeleri, bas-aç mandalları, kapak (dış + iç tava) menteşe kanatlarıyla önden; karşılıklar punta, aktüatör M4.',
           [r'^onyuz_kapak_K', r'^k_govde_on_seffaf', r'^emniyet_siyah'], ONDEN)
KALAN = sec(r'.')
if KALAN:
    adim_parca('Kalan parçalar', 'Planda grubu olmayan parçalar.', [r'.'], HER)
adim('Hat bağlantısı', 'Sahada: F (silik) solda, E (silik) sağda, U üstte.', 'F · E · U (silik)')
for a in ('cevre_F', 'cevre_U', 'cevre_diger'):
    if a in P: basla(a, np.zeros(3), t); YER[a] = t; YERINDE.append(a)
t = baglantilar(t + 0.5, ofs0=None)
olay(t, 'Komşu istasyonlar (silik) yerinde'); t += 1.0
kam(t, ([5.2, 2.8, 2.6], [4.2, 1.2, -0.4]))
TOPLAM = round(bitti() + 2.0, 3)
print('bekleyen bağlantı elemanı', len(BEKLEYEN), BEKLEYEN[:15])
KAPGRUP = []
exec(open(os.path.join(HERE, '_son_c.py'), encoding='utf-8').read().replace("'plan_a3.pkl'", "'plan_k_c.pkl'").replace('OLC = 1.75', 'OLC = 1.0'))
