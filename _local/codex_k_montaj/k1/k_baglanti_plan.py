# -*- coding: utf-8 -*-
"""K bağlantı planı (Claude, 6 Eki 2026) — Codex devrinin 212 bağlantısız parçası için gerçek bağlantı tasarımı.
Girdi: plan_k_clip_full.pkl (parça üçgenleri, dünya mm) · k_temas.json (oturduğu yüzey)
Çıktı: k_baglanti_plan.json → zincir adımı 86 (86_k_baglanti.py) bu dosyadaki geometriyi kurar:
  vida   : baş + gövde (+ somun / PEM / perçin somun) silindirleri · delik_ac ile a ve b'de geçiş / dişli delik
  kaynak : TIG / punta işareti (iki parçanın temas yüzeyinde)
  tasi   : parçayı oturduğu yüzeye yaslar (model boşluğu kapanır)
  beyan  : dişli bağlantı / DIN raya geçme / oluk sensörü / kelepçe / rulman mil / satın alınan ürünün iç parçası / elle çıkan — karşı parçaya
           gerçek temas DOĞRULANIR (≤ 0,3 mm), yoksa açık kalır
Her vida için: baş, anahtar yolu, somun hacmi boş · gövde yalnız a ve b'den geçer · diş tutuşu ≥ 1 × d · katalog boyu (ISO 4762 / 7380 / DIN 7991)."""
import json, pickle, re, math, sys
import numpy as np
import trimesh

D = pickle.load(open('plan_k_clip_full.pkl', 'rb')); P = D['P']
TEMAS = json.load(open('k_temas.json'))
LO = {a: P[a]['V'].min(0) for a in P}; HI = {a: P[a]['V'].max(0) for a in P}
TM = {}
def tm(a):
    if a not in TM: TM[a] = trimesh.Trimesh(P[a]['V'], P[a]['F'], process=False)
    return TM[a]
KATALOG = [6, 8, 10, 12, 16, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80, 90, 100]
ADIM_P = {3: 0.5, 4: 0.7, 5: 0.8, 6: 1.0, 8: 1.25}
ENGEL = [a for a in P if P[a]['tur'] not in ('kablo',) and not a.startswith('cevre_diger')]

# ------------------------------------------------------------------ yöntem tablosu (sıra önemli: ilk tutan)
# (desen, yöntem, parametre)  yöntem: VIDA / TIG / PUNTA / BEYAN:<tür> / SAPLAMA_KELEBEK / TASI+...
KURAL = [
    (r'^DGRF_SMT-8M_\d$', 'BEYAN:OLUK', dict(karsi='DGRF_sensor_rayi', neden='Festo SMT-8M sensörü sensör rayının oluğuna kendi tespit vidasıyla')),
    (r'^DGRF_piston$', 'BEYAN:URUN', dict(karsi='DGRF_silindir_borusu', neden='Festo DGRF silindirin iç parçası (piston borunun içinde, satın alınan ürün)')),
    (r'^DGRF_port_(on|arka)_QSL$', 'BEYAN:DIS', dict(neden='Festo QSL-G3/8 rakor silindir portuna dişli (G3/8)')),
    (r'^PulsaJet_AAB', 'BEYAN:KELEPCE', dict(karsi='nozul_kelepce_blogu', neden='nozül gövdesi iki yarım kelepçe bloğunun arasında sıkılır (2 × M4)')),
    (r'^PulsaJet_(M8_kablo|M8_soketi|giris_dirsegi|kapak|uc)', 'BEYAN:DIS', dict(neden='nozülün dişli parçası (M8 soket / 1/8 BSPT dirsek / kapak / uç)')),
    (r'^avara_mili_\d$', 'MIL_UCU', dict(d=8, destek='bant_yan', std='ISO 4762', neden='avara mili bant yan sacına dıştan M6 (milin ucunda diş)')),
    (r'^avara_rulosu_', 'BEYAN:MIL', dict(karsi='avara_mili_0', neden='rulmanlı avara rulosu iki mil ucuna takılı (Interroll · milde döner)')),
    (r'^bant_traversi_\d$', 'TIG', dict(destek=['bant_yan_-3', 'bant_yan_-421'], neden='bant traversi iki yan profile TIG (uçlar)')),
    (r'^bicak_\d$', 'BEYAN:URUN', dict(karsi='bicak_gobek_halkasi', neden='yıldız bıçak seti tek ürün: 6 dilim göbeğe fabrikada kaynaklı (set olarak sökülür, yıkanır)')),
    (r'^bicak_gobek_halkasi$', 'SAPLAMA_KELEBEK', dict(d=8, neden='bıçak seti göbeği: merkez M8 saplama kafa plakasından geçer, üstte kelebek somun (aletsiz söküm, yıkama) · 2 × Ø6 pim dönmeyi engeller')),
    (r'^bicak_koruma_halkasi$', 'TIG', dict(minp=1, destek=['koruma_braketi_%d' % i for i in range(6)], neden='koruma halkası 6 brakete TIG')),
    (r'^koruma_braketi_\d$', 'TIG', dict(minp=1, tasi='kafa_plakasi_8', destek=['kafa_plakasi_8', 'bicak_koruma_halkasi'], neden='koruma braketi kafa plakası kenarına yaslanır, plakaya ve koruma halkasına TIG')),
    (r'^cit_(on|arka_a|arka_b)$', 'VIDA', dict(d=3, n=2, destek='cit_braketi', std='ISO 7380', bas='b', dis_a=True, neden='POM çit brakete M3 bombe başlı (baş braket dışında, POM çitte dişli delik)')),
    (r'^cit_giris_-?1$', 'BEYAN:TEK_PARCA', dict(neden='çit giriş eğimi aynı POM çit çubuğunun ısıyla bükülmüş ucu (tek parça)')),
    (r'^cit_braketi_\d$', 'TIG', dict(destek=['bant_yan_-3', 'bant_yan_-421'], neden='çit braketi bant yan profiline TIG')),
    (r'^d3_kaplin_(emis|donus)$', 'BEYAN:DIS', dict(karsi=None, neden='CPC hızlı kaplin duvar geçiş bileziğinde, hortuma geçme (kapamalı)')),
    (r'^d3_seviye_salteri_M12_fis$', 'BEYAN:DIS', dict(neden='M12 fiş karşı sokete dişli')),
    (r'^din_rayi_\d$', 'BEYAN:MEVCUT', dict(neden='DIN ray pano plakasına 2 × M5 havşa (k_din_M5, mevcut)')),
    (r'^elk_ic_kanal_[45]$', 'BEYAN:GECME', dict(neden='kanal ek / dirsek parçası: kanalın içine geçer')),
    (r'^elk_ic_kanal_\d$', 'VIDA', dict(d=4, n=2, std='ISO 7380', tasi=True, yapisal=True, neden='kablo kanalı duvara M4 bombe başlı (perçin somun)')),
    (r'^elk_k_celik_\d$', 'TIG', dict(neden='elektrik taşıyıcı braketi gövdeye TIG')),
    (r'^elk_k_tarti_celik_\d$', 'TIG', dict(neden='tartı kablo braketi TIG')),
    (r'^elk_zincir_(etiket|kod_kirmizi|kod_mavi)_\d$', 'BEYAN:ETIKET', dict(neden='yapışkan etiket / renk kodu halkası')),
    (r'^elk_zincir_(m12|rakor)_\d$', 'BEYAN:DIS', dict(neden='panel tipi M12 soket / kablo rakoru: kendi kilit somunuyla panel deliğine')),
    (r'^elk_zincir_harting_[12]$', 'BEYAN:GECME', dict(neden='Harting başlık tabana kilit koluyla kilitlenir')),
    (r'^elk_zincir_harting_[03]$', 'VIDA', dict(d=4, n=2, std='ISO 7380', sonra_desen='harting_[12]', neden='Harting taban panele 2 × M4')),
    (r'^elk_zincir_paslanmaz_[0-36-9]$', 'TIG', dict(neden='panel mesafe parçası yan saca TIG')),
    (r'^elk_zincir_paslanmaz_[45]$', 'VIDA', dict(d=4, n=2, std='ISO 7380', destek=None, neden='fiş paneli mesafe parçalarına M4')),
    (r'^elk_zincir_kanal_\d$', 'VIDA', dict(d=4, n=2, std='ISO 7380', yapisal=True, neden='kablo kanalı saca M4 (perçin somun)')),
    (r'^emniyet_sari_\d$', 'VIDA', dict(d=4, n=2, neden='kapı emniyet sensörü dikmeye 2 × M4 (perçin somun)')),
    (r'^emniyet_siyah_\d$', 'VIDA', dict(d=4, n=2, bas='a', neden='aktüatör kapı iç tavasına 2 × M4 (PEM)')),
    (r'^(guc_24V|plc_|sigorta_C10|klemens_sirasi)', 'BEYAN:DIN', dict(karsi=None, neden='DIN raya yaylı tırnakla geçer (EN 60715)')),
    (r'^hava_ic_aski_\d+$', 'BEYAN:YAPISTIRMA', dict(neden='kendinden yapışkanlı kablo bağı tabanı (hortum askısı)')),
    (r'^hava_ic_kanal_\d$', 'BEYAN:KABLO', dict(neden='hava hortumu: askılar boyunca uzar (kablo / hortum istisnası)')),
    (r'^itici_X_ray_-?\d+$', 'RAY', dict(d=3, adim=40.0, gomme=5.5, destek='itici_sabit_plaka', neden='HIWIN MGNR15R ray X taban plakasına M3 × 40 adım (dişli delik)')),
    (r'^itici_Z_ray_\d+$', 'RAY', dict(d=3, adim=40.0, gomme=5.5, destek=None, neden='HIWIN MGNR15R ray Z yükseltmesine M3 × 40 adım')),
    (r'^itici_[XZ]_blok_-?\d+$', 'BEYAN:KIZAK', dict(neden='HIWIN MGN15H blok rayda (bilyeli kızak); üst yüzü 4 × M3 ile taşıdığı plakaya')),
    (r'^itici_X_ara_-?\d+$', 'VIDA', dict(d=3, n=4, destek=['itici_X_blok_-645', 'itici_X_blok_-755'], bas='a', neden='X ara plakası bloğa 4 × M3')),
    (r'^itici_Z_kopru$', 'VIDA', dict(d=3, n=4, destek=['itici_Z_blok_53', 'itici_Z_blok_97'], bas='a', neden='Z köprüsü iki bloğa 4 × M3')),
    (r'^itici_Z_plaka$', 'VIDA', dict(d=4, n=2, destek=['itici_X_ara_-645', 'itici_X_ara_-755'], bas='a', neden='Z taban plakası X ara plakalarına 2 × M4')),
    (r'^itici_Z_yukseltme_\d+$', 'VIDA', dict(d=4, n=3, destek='itici_Z_plaka', bas='b', dis_a=True, neden='Z yükseltme Z plakasına alttan 3 × M4')),
    (r'^itici_[XZ]_MY1B10G-\d+_(profil|masa)$', 'BEYAN:URUN', dict(neden='SMC MY1B rodless silindirin gövdesi / arabası (satın alınan ürün)')),
    (r'^itici_X_MY1B10G-250_uc_kapagi_\d$', 'VIDA', dict(d=4, n=2, destek='itici_sabit_plaka', bas='b', dis_a=True, neden='silindir uç kapağı taban plakasına alttan 2 × M4 (kapakta diş)')),
    (r'^itici_Z_MY1B10G-350_uc_kapagi_\d$', 'VIDA', dict(d=4, n=2, destek='itici_Z_plaka', bas='b', dis_a=True, neden='silindir uç kapağı Z plakasına alttan 2 × M4')),
    (r'^itici_[XZ]_MY1B10G-\d+_AS1201F_\d$', 'BEYAN:DIS', dict(neden='SMC AS1201F hız ayar valfi silindir portuna M5 dişli')),
    (r'^itici_[XZ]_MY1B10G-\d+_D-M9N_\d$', 'BEYAN:OLUK', dict(neden='SMC D-M9N oto svic silindir yan oluğuna kendi vidasıyla')),
    (r'^itici_X_RB0805_\d$', 'BEYAN:DIS', dict(neden='SMC RB0805 şok emici durdurucuya M8 × 0,75 dişli + kontra somun')),
    (r'^itici_X_durdurucu_\d$', 'VIDA', dict(d=5, n=2, destek='itici_sabit_plaka', bas='a', neden='durdurucu braketi taban plakasına 2 × M5')),
    (r'^itici_X_MY-J10_blok_\d$', 'VIDA', dict(d=4, n=2, destek='itici_X_merkez_yukseltme', bas='a', neden='MY-J10 yüzer bağlantı bloğu yükseltmeye 2 × M4')),
    (r'^itici_X_MY-J10_pim_\d$', 'BEYAN:URUN', dict(neden='SMC MY-J10 yüzer bağlantının pimi (ürünün parçası)')),
    (r'^itici_sabit_plaka$', 'VIDA', dict(d=5, n=4, destek=None, bas='a', yapisal=True, neden='X taban plakası itici sacına 4 × M5')),
    (r'^itici_yuzer_baglanti$', 'BEYAN:PIM', dict(neden='Ø8 yüzer pim: silindir arabasına sıkı geçme, köprüde ±1 mm boşluklu')),
    (r'^itici_one_kol$', 'VIDA', dict(d=5, n=2, destek='itici_Z_kopru', bas='a', neden='itici kolu Z köprüsüne 2 × M5')),
    (r'^itici_(dusey_kol|yatay_kol|yuz_kilavuz_kovani)$', 'TIG', dict(neden='itici kolu kaynaklı grup (304): kollar + kılavuz kovanı TIG')),
    (r'^itici_yuzer_kilavuz$', 'BEYAN:PIM', dict(karsi='itici_yuz', neden='kılavuz pimi POM itici yüzüne sıkı geçme, kovanda yüzer')),
    (r'^itici_yuz$', 'BEYAN:KIZAK', dict(karsi='itici_yuzer_kilavuz', neden='POM itici yüzü kılavuz pimlerinde düşey 15 mm yüzer (bilerek)')),
    (r'^itici_alt_dudak$', 'BEYAN:TEK_PARCA', dict(neden='alt dudak itici yüzüyle aynı POM plakadan işlenir (tek parça)')),
    (r'^k_e4_sol_yama', 'PUNTA', dict(neden='kapama yaması sol saca punta')),
    (r'^k_elektrik_sac_\d$', 'VIDA', dict(d=5, n=4, destek=['elk_k_celik_0', 'elk_k_celik_4', 'elk_k_celik_5', 'elk_k_celik_8'], bas='a', neden='elektrik sacı mesafe braketlerine 4 × M5')),
    (r'^k_yag_pom_\d$', 'BEYAN:DIS', dict(neden='teneke kapak adaptörü tenekenin ağzına vidalı')),
    (r'^kayma_tablasi$', 'VIDA', dict(d=5, n=2, destek=['bant_traversi_0', 'bant_traversi_1'], std='DIN 7991', bas='a', neden='UHMW kayma tablası traverslere havşa M5 (perçin somun)')),
    (r'^kopru_kirisi_', 'TIG', dict(neden='köprü kirişi yan kirişlere TIG')),
    (r'^kose_dikmesi_.*_tapa$', 'TIG', dict(neden='dikme tapası çevresel TIG, taşlanır')),
    (r'^nozul_braketi$', 'VIDA', dict(d=5, n=2, destek='sol_sac_urun_girisi', bas='a', neden='nozül braketi sol saca 2 × M5 (sacda PEM)')),
    (r'^nozul_kelepce_blogu$', 'VIDA', dict(d=4, n=2, destek='nozul_braketi', bas='a', neden='kelepçe bloğu brakete 2 × M4')),
    (r'^olu_plaka$', 'TIG', dict(neden='çıkış ölü plakası TIG')),
    (r'^onyuz_kapak_K_karsilik_\d$', 'PUNTA', dict(neden='bas-aç karşılığı kapı iç tavasına punta')),
    (r'^sartlandirici_braketi$', 'BEYAN:URUN_MONTAJ', dict(karsi='pano_plakasi', neden='SMC B240A braketi pano plakasına 2 × M5 — braketin kendi kulak delikleri regülatör izinin dışında; modeldeki braket sadeleştirilmiş (AÇIK NOT: gerçek braket geometrisi)')),
    (r'^sartlandirici_AW20', 'BEYAN:DIS', dict(karsi='sartlandirici_braketi', neden='AW20 braket halka somunuyla (gövde dişine)')),
    (r'^tahrik_rulosu_EC5000_kablo$', 'BEYAN:DIS', dict(neden='EC5000 M8 fişi motor soketine dişli')),
    (r'^urun_sensoru_.*_braket_\d$', 'TIG', dict(neden='sensör L braketi bant yan profiline TIG')),
    (r'^urun_sensoru_.*_(alici|verici)$', 'VIDA', dict(d=3, n=2, bas='a', neden='E3Z fotosel brakete 2 × M3 + somun')),
    (r'^valf_SY3120_\d$', 'VIDA', dict(d=3, n=2, destek='valf_adasi_SS5Y3-20-04', bas='a', neden='SY3120 valf manifolda 2 × M3 (ürünle gelen)')),
    (r'^valf_kor_plaka$', 'VIDA', dict(d=3, n=2, destek='valf_adasi_SS5Y3-20-04', bas='a', neden='kör plaka manifolda 2 × M3')),
    (r'^valf_SY3120_\d_rakor_\d$', 'BEYAN:DIS', dict(neden='C6 geçme rakor valf portuna')),
    (r'^yag_(T_parcasi|basinc_sensoru|boru_|emis_filtresi)', 'BEYAN:DIS', dict(neden='1/4" paslanmaz hat: dişli / sıkma rakorlu bağlantı')),
    (r'^yag_geri_basinc_regulatoru', 'VIDA', dict(d=5, n=2, destek='yag_pompa_plakasi', bas='a', neden='geri basınç regülatörü plakaya 2 × M5 (panel montaj)')),
    (r'^yag_pompasi_', 'BEYAN:KELEPCE', dict(karsi='k79_pompa_ust_pad_0', neden='pompa iki portal ile plakaya sıkılır (portallar 4 × M5)')),
    (r'^yag_damlama_tavasi_F$', 'BEYAN:SOKULUR', dict(neden='damlama tavası F rafına oturur, temizlik için elle çıkar')),
    (r'^yag_tarti_taban_plakasi$', 'BEYAN:SOKULUR', dict(neden='tartı tabanı damlama tavasında oturur (tartı serbest durmalı), elle çıkar')),
    (r'^yag_tarti_alt_takozu$', 'VIDA', dict(d=8, n=2, destek='yag_tarti_taban_plakasi', bas='a', neden='yük hücresi alt takozu taban plakasına 2 × M8')),
    (r'^yag_tarti_yuk_hucresi', 'VIDA', dict(d=6, n=2, destek='yag_tarti_alt_takozu', bas='a', neden='yük hücresi alt takoza 2 × M6')),
    (r'^yag_tarti_ust_takozu$', 'VIDA', dict(d=6, n=2, destek='yag_tarti_yuk_hucresi_PW15AH', bas='a', std='DIN 7991', neden='üst takoz yük hücresine 2 × M6')),
    (r'^yag_tarti_platformu$', 'VIDA', dict(d=6, n=2, destek='yag_tarti_ust_takozu', bas='a', neden='platform üst takoza 2 × M6')),
    (r'^yag_tenekesi_18L$', 'BEYAN:SOKULUR', dict(neden='18 L teneke platforma oturur, boşalınca elle değişir')),
    (r'^yag_emme_lansi', 'BEYAN:SOKULUR', dict(karsi='k_yag_pom_0', neden='emme lansı tenekeye daldırılır, kapak adaptöründen geçer')),
]


def yontem(a):
    for d_, y, p in KURAL:
        if re.search(d_, a): return y, p
    return None, None


def sample(a, n=4000):
    S = trimesh.sample.sample_surface_even(tm(a), n, seed=3)[0] if len(P[a]['F']) else np.zeros((0, 3))
    return np.vstack([S, P[a]['V']])


def patch(a, b, tol=0.3, minp=3):
    S = sample(a)
    S = S[np.all(S >= LO[b] - 1, 1) & np.all(S <= HI[b] + 1, 1)]
    if not len(S): return None
    cp, d, tri = trimesh.proximity.closest_point(tm(b), S)
    m = d < tol
    if m.sum() < minp: return None
    n = tm(b).face_normals[tri[m]]
    e = n.mean(0); e /= np.linalg.norm(e) + 1e-12
    ca = (LO[a] + HI[a]) / 2
    if (ca - S[m].mean(0)) @ e < 0 and np.ptp(P[a]['V'] @ e) > 0.5: e = -e        # normal b'den a'ya baksın
    return S[m], e


def ray_ilk(a, o, e, maks=200.0):
    """o noktasından e yönünde a ağına ilk çarpma uzaklığı (yoksa None)"""
    loc, ri, _ = tm(a).ray.intersects_location([o], [e], multiple_hits=True)
    if not len(loc): return None
    d = (loc - o) @ e
    d = d[d > 0.2]
    return float(d.min()) if len(d) and d.min() < maks else None


def silindir_noktalar(p0, p1, r, n_ax=8, n_r=3, n_t=12):
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); e = p1 - p0; L = np.linalg.norm(e); e /= L
    u = np.cross(e, [1, 0, 0] if abs(e[0]) < 0.9 else [0, 1, 0]); u /= np.linalg.norm(u); v = np.cross(e, u)
    out = []
    for s in np.linspace(0, 1, n_ax):
        c = p0 + e * L * s; out.append(c)
        for rr in np.linspace(r / n_r, r, n_r):
            for t in np.linspace(0, 2 * math.pi, n_t, endpoint=False): out.append(c + rr * (math.cos(t) * u + math.sin(t) * v))
    return np.array(out)


def engel_var(p0, p1, r, haric):
    """silindir hacminde (a, b dışındaki) parça var mı → [ad]"""
    Q = silindir_noktalar(p0, p1, r)
    lo = Q.min(0) - 0.5; hi = Q.max(0) + 0.5; out = []
    for c in ENGEL:
        if c in haric: continue
        if np.any(LO[c] > hi) or np.any(HI[c] < lo): continue
        # c'nin köşeleri silindirde mi · silindir noktaları c yüzeyine çok yakın mı
        V = P[c]['V']; e = np.asarray(p1, float) - np.asarray(p0, float); L = np.linalg.norm(e); e /= L
        w = V - p0; s = w @ e; rad = np.linalg.norm(w - np.outer(s, e), axis=1)
        if np.any((s > 0.05) & (s < L - 0.05) & (rad < r - 0.05)): out.append(c); continue
        Qc = Q[np.all(Q >= LO[c] - 0.5, 1) & np.all(Q <= HI[c] + 0.5, 1)]
        if len(Qc):
            _, d, _ = trimesh.proximity.closest_point(tm(c), Qc)
            if d.min() < 0.05: out.append(c)
    return out


def merkezler(S, e, n, d):
    """temas yamasında n bağlantı noktası (kenardan ≥ d uzak, birbirinden uzak)"""
    c0 = S.mean(0); u = np.cross(e, [1, 0, 0] if abs(e[0]) < 0.9 else [0, 1, 0]); u /= np.linalg.norm(u); v = np.cross(e, u)
    X = np.c_[(S - c0) @ u, (S - c0) @ v]
    w, V = np.linalg.eigh(np.cov(X.T) + 1e-9 * np.eye(2)); ana = V[:, 1]; yan = V[:, 0]
    tA = X @ ana; tY = X @ yan
    aday = []
    from scipy.spatial import cKDTree
    kd = cKDTree(X); sp = max(0.6, math.sqrt(max(1e-6, np.ptp(tA) * max(np.ptp(tY), 1.0)) / max(len(X), 1)) * 2.5)
    for fa in np.linspace(0.08, 0.92, 15):
        for fy in (0.5, 0.3, 0.7):
            q = ana * (tA.min() + fa * np.ptp(tA)) + yan * (tY.min() + fy * np.ptp(tY))
            cev = [q + 0.9 * d * np.array([math.cos(t), math.sin(t)]) for t in np.linspace(0, 2 * math.pi, 12, endpoint=False)] + [q]
            dd, _ = kd.query(np.array(cev))
            if np.all(dd < sp): aday.append((fa, q)); break
    if not aday: return []
    if n >= len(aday): sec = aday
    elif n == 1: sec = [aday[len(aday) // 2]]
    else:
        idx = np.linspace(0, len(aday) - 1, n).round().astype(int)
        sec = [aday[i] for i in sorted(set(idx))]
    return [c0 + q[0] * u + q[1] * v for _, q in sec]


def katalog_ust(L):
    for k in KATALOG:
        if k >= L - 1e-6: return k
    return KATALOG[-1]


def katalog_alt(L):
    k0 = None
    for k in KATALOG:
        if k <= L + 1e-6: k0 = k
    return k0


def vida_tasarla(a, b, p, e, d, bas='a', dis_a=False, dis_b=False, std='ISO 4762', no=0, gomme=0.0, sonra=()):
    """p: temas noktası, e: b → a birim (temas yüzeyinin normali). bas='a': baş a'nın dış yüzünde, b'ye; bas='b': baş b'nin dış yüzünde, a'ya."""
    h_bas = {'ISO 4762': d * 1.0, 'ISO 7380': d * 0.55, 'DIN 7991': 0.0}[std]
    r_bas = {'ISO 4762': d * 0.75, 'ISO 7380': d * 0.88, 'DIN 7991': d}[std]
    P_ = ADIM_P[d]; somun_tur = 'altigen'
    ust, alt = (a, b) if bas == 'a' else (b, a)
    eu = e if bas == 'a' else -e                                                  # baş tarafına doğru
    t_ust = ray_ilk(ust, p - eu * 0.05, eu)                                       # üst parçanın kalınlığı (temastan dış yüzüne)
    t_alt = ray_ilk(alt, p + eu * 0.05, -eu)                                      # alt parçanın kalınlığı
    if t_ust is None or t_alt is None: return None, 'ışın kalınlık bulamadı'
    t_ust = t_ust - gomme                                                         # baş üst parçanın havşa yuvasında (ör. HIWIN ray: 5,5)
    bas0 = p + eu * t_ust                                                         # baş oturma yüzeyi
    dis_alt = ((dis_b if bas == 'a' else dis_a) and t_alt >= 1.0 * d + P_) or t_alt >= 1.5 * d + P_   # alt parçada dişli delik (yeterli et varsa)
    if dis_alt:
        L = katalog_alt(t_ust + min(t_alt - P_, 2.0 * d))
        if L is None or L < t_ust + 1.0 * d: return None, 'diş tutuşu < 1d (alt kalınlık %.1f)' % t_alt
        uc = bas0 - eu * L; somun = None
    else:
        L = katalog_ust(t_ust + t_alt + 0.8 * d + 2 * P_)
        uc = bas0 - eu * L
        somun = (p - eu * t_alt, p - eu * (t_alt + 0.8 * d), d * 0.9)          # altıgen somun ≈ Ø1,8d silindir
        ikinci = ray_ilk(alt, p - eu * (t_alt + 0.3), -eu, 60.0)
        if t_alt <= 3.0 and ikinci is not None:                                   # içi boş profil / boru: kör perçin somun (dıştan takılır)
            L = katalog_ust(t_ust + t_alt + 1.5 * d)
            uc = bas0 - eu * L
            somun = (p - eu * t_alt, p - eu * (t_alt + 1.5 * d), d * 0.75)
            somun_tur = 'percin'
    if std == 'DIN 7991':
        bas_sil = None                                                           # havşa baş üst parçanın içinde (delik_ac havşayı açar)
    else:
        bas_sil = (bas0, bas0 + eu * h_bas, r_bas)
    # boş hacim denetimi
    hr = [a, b] + list(sonra)
    if bas_sil:
        x = engel_var(bas_sil[0] + eu * 0.05, bas_sil[1] + eu * (8.0 if not gomme else 0.5), r_bas + 0.3, hr)   # baş + anahtar yolu 8 mm
        if x: return None, 'baş / anahtar yolu dolu: %s' % x[:3]
    g = engel_var(bas0 - eu * 0.05, uc, d / 2 + 0.2, hr)
    if g and not dis_alt and re.match(r'(sol_sac|sag_sac|arka_sac|ust_sac)', alt) and bas == 'a':
        # dış sac (arkası komşu istasyon): sacın dış yüzünde gömme başlı PEM FHS saplama, a'dan geçer, a'nın üstünde pul + somun
        s0 = p - eu * t_alt; s1 = bas0 + eu * (0.8 * d + 2 * P_)
        if engel_var(bas0 + eu * 0.05, s1 + eu * 3.0, d * 0.9 + 0.3, hr): return None, 'saplama somunu hacmi dolu'
        ad = 'kb_%s_%d' % (a, no)
        return [dict(ad=ad + '_saplama', tip='saplama', d=d, govde=[list(map(float, s0)), list(map(float, s1)), d / 2], eks=list(map(float, eu)), parca=[a, b],
                     pem_sac=alt, bom='PEM FHS-M%d saplama (dış sac, baş yüzeyle aynı)' % d),
                dict(ad=ad + '_somun', tip='somun', d=d, sil=[list(map(float, bas0)), list(map(float, bas0 + eu * 0.8 * d)), float(d * 0.9)], eks=list(map(float, -eu)),
                     parca=[a, b], somun_tur='altigen', bom='ISO 10511 fiberli somun M%d + ISO 7089 pul' % d)], 'ok (PEM saplama dış sacta)'
    if g: return None, 'gövde başka parçadan geçiyor: %s' % g[:3]
    if somun:
        x = engel_var(somun[0] - eu * 0.05, somun[1] - eu * (3.0 if somun_tur == 'altigen' else 0.5), somun[2] + 0.3, hr)
        if x: return None, 'somun hacmi dolu: %s' % x[:3]
    ad = 'kb_%s_%d' % (a, no)
    vida = dict(ad=ad + '_vida', tip='vida', d=d, std=std, L=L, bas=None if bas_sil is None else [list(map(float, bas_sil[0])), list(map(float, bas_sil[1])), float(bas_sil[2])],
                govde=[list(map(float, bas0)), list(map(float, uc)), d / 2], eks=list(map(float, -eu)), parca=[a, b],
                havsa=std == 'DIN 7991', bom='%s M%d × %d A2-70%s' % (std, d, L, '' if dis_alt else (' + ISO 4032 somun' if somun_tur == 'altigen' else ' + kör perçin somun')))
    out = [vida]
    if somun:
        out.append(dict(ad=ad + '_somun', tip='somun', d=d, sil=[list(map(float, somun[0])), list(map(float, somun[1])), float(somun[2])], eks=list(map(float, eu)),
                        parca=[a, b], somun_tur=somun_tur, bom=('ISO 4032 somun M%d A2' % d) if somun_tur == 'altigen' else ('Kör perçin somun M%d A2 (kapalı uç)' % d)))
    return out, 'ok (%s, L %d, %s)' % (std, L, 'dişli delik' if dis_alt else 'somun')


def destekler(a, p):
    d = p.get('destek')
    if d is None:
        L = [x for x in TEMAS.get(a, []) if x[1] < 0.3 and x[2] > 0]
        if p.get('yapisal'):
            L = [x for x in L if not re.search(r'kanal|aski|harting|rakor|m12|kod_|etiket|kablo', x[0])] or L
        return [x[0] for x in L] if p.get('yapisal') else ([L[0][0]] if L else [])
    if isinstance(d, str):
        return [b for b in P if b == d or b.startswith(d + '_') or b.startswith(d)] if d not in P else [d]
    return [x for x in d if x in P]


TASI = {}; SIL = []
def tasi(a, b):
    """a'yı b'ye en kısa yoldan yaslar (en yakın nokta çifti) → öteleme vektörü, P[a] güncellenir"""
    S = sample(a, 3000)
    cp, d, _ = trimesh.proximity.closest_point(tm(b), S)
    i = int(np.argmin(d))
    if d[i] < 0.05: return None
    v = cp[i] - S[i]
    P[a] = dict(P[a], V=P[a]['V'] + v); LO[a] = P[a]['V'].min(0); HI[a] = P[a]['V'].max(0); TM.pop(a, None)
    return [float(x) for x in v]
SONUC = {}; ACIK = []
for a in sorted(TEMAS):
    y, p = yontem(a)
    if y is None: ACIK.append((a, 'yöntem tablosunda yok')); continue
    if y.startswith('BEYAN'):
        k = p.get('karsi')
        kars = [x for x in TEMAS[a] if x[1] < 0.3 and (k is None or x[0] == k)]
        if y in ('BEYAN:KABLO', 'BEYAN:YAPISTIRMA', 'BEYAN:SOKULUR', 'BEYAN:MEVCUT', 'BEYAN:ETIKET') or kars or (y == 'BEYAN:DIS' and p.get('karsi', 0) is None):
            SONUC[a] = dict(yontem=y, neden=p['neden'], karsi=kars[0][0] if kars else None)
        else:
            ACIK.append((a, '%s: karşı parçaya temas yok (%s)' % (y, k)))
        continue
    if y in ('TIG', 'PUNTA'):
        dl = destekler(a, p) if p.get('destek') else [x[0] for x in TEMAS[a] if x[1] < 0.3 and x[2] > 0][:2]
        el = []
        if p.get('tasi'):
            v_ = tasi(a, p['tasi'])
            if v_ is not None: TASI[a] = v_
        for b in dl:
            pt = patch(a, b, minp=p.get('minp', 3))
            if pt is None: continue
            S, e = pt
            for j, c in enumerate((merkezler(S, e, 2, 1.5) if len(S) >= 3 else []) or [S.mean(0)]):
                el.append(dict(ad='kb_%s_%s_%d_kaynak' % (a, b, j), tip='kaynak', yontem=y, merkez=list(map(float, c)), eks=list(map(float, e)), parca=[a, b],
                               bom=('TIG 141 köşe dikişi a 2 · ER308LSi · 2 × 20 mm' if y == 'TIG' else 'Punta (direnç) Ø5')))
        if el: SONUC[a] = dict(yontem=y, neden=p['neden'], eleman=el)
        else: ACIK.append((a, '%s: temas yaması yok %s' % (y, dl)))
        continue
    if y == 'SAPLAMA_KELEBEK':
        # 3 kelebek somun proxy'si bıçakların arasında, altında karşı parça yok → TEK merkez saplama + 2 pim (dönmez) + tek kelebek somun
        c = (LO[a] + HI[a]) / 2
        k0 = 'kelebek_somun_0'; kc = (LO[k0] + HI[k0]) / 2
        v_ = np.array([c[0] - kc[0], 0.0, c[2] - kc[2]])
        P[k0] = dict(P[k0], V=P[k0]['V'] + v_); LO[k0] = P[k0]['V'].min(0); HI[k0] = P[k0]['V'].max(0); TM.pop(k0, None); TASI[k0] = [float(x) for x in v_]
        SIL.extend(['kelebek_somun_1', 'kelebek_somun_2'])
        y0 = HI[a][1] - 8.0; y1 = HI[k0][1] - 1.0
        q0 = np.array([c[0], y0, c[2]]); q1 = np.array([c[0], y1, c[2]])
        hr = [a, 'kafa_plakasi_8', 'k79_kafa_ust_plaka_2', k0] + [x for x in P if x.startswith('bicak_')]
        x_ = engel_var(q0, q1, 4.2, hr)
        el = [dict(ad='kb_%s_saplama' % a, tip='saplama', d=8, govde=[list(map(float, q0)), list(map(float, q1)), 4.0], eks=[0, 1.0, 0],
                   parca=[a, 'kafa_plakasi_8', k0], bom='Saplama M8 × %d A2 (bıçak seti göbeğine dişli + Loctite 2701, kafa plakasından geçer · üstte DIN 315 kelebek somun)' % round(y1 - y0))]
        for j, dx in enumerate((-12.0, 12.0)):
            r0 = np.array([c[0] + dx, HI[a][1] - 8.0, c[2]]); r1 = np.array([c[0] + dx, HI[a][1] + 4.0, c[2]])
            x_ += engel_var(r0, r1, 3.2, hr)
            el.append(dict(ad='kb_%s_pim_%d' % (a, j), tip='pim', d=6, govde=[list(map(float, r0)), list(map(float, r1)), 3.0], eks=[0, 1.0, 0],
                           parca=[a, 'kafa_plakasi_8'], bom='ISO 8734 silindirik pim Ø6 × 12 A1 (göbekte sıkı, plakada kaygan: dönmeyi engeller)'))
        if x_: ACIK.append((a, 'merkez saplama / pim hacmi dolu %s' % sorted(set(x_))[:4])); continue
        SONUC[a] = dict(yontem='SAPLAMA_KELEBEK', neden=p['neden'], eleman=el)
        continue
    if y == 'MIL_UCU':
        # avara mili ucu M8 dişli: bant yanının gergi deliğinden geçer, dışta ISO 10511 fiberli somun + pul (gergi ayarı)
        el = []
        for b in destekler(a, p):
            pt = patch(a, b, tol=0.3, minp=1)
            if pt is None: continue
            S, e = pt
            ax = int(np.argmax(np.abs(e))); c = (LO[a] + HI[a]) / 2; c[ax] = S.mean(0)[ax]
            t_b = ray_ilk(b, c + e * 0.05, -e) or 2.0
            q0 = c + e * 0.0; q1 = c - e * (t_b + 8.0 + 2.0)
            n0 = c - e * t_b; n1 = c - e * (t_b + 8.0)
            x_ = engel_var(q0 - e * 0.05, q1, 4.2, [a, b]) + engel_var(n0 - e * 0.05, n1 - e * 3, 6.8, [a, b])
            if x_: continue
            el += [dict(ad='kb_%s_saplama' % a, tip='saplama', d=8, govde=[list(map(float, c + e * 6.0)), list(map(float, q1)), 4.0], eks=list(map(float, -e)), parca=[a, b],
                        bom='Avara mili ucu M8 dişli (milin parçası, gergi deliğinden geçer)'),
                   dict(ad='kb_%s_somun' % a, tip='somun', d=8, sil=[list(map(float, n0)), list(map(float, n1)), 6.5], eks=list(map(float, e)), parca=[a, b], somun_tur='altigen',
                        bom='ISO 10511 fiberli somun M8 A2 + ISO 7089 pul (gergi)')]
            break
        if el: SONUC[a] = dict(yontem='VIDA', neden='avara mili ucu M8 bant yanından geçer, dıştan fiberli somun (gergi)', eleman=el)
        else: ACIK.append((a, 'mil ucu: temas / hacim yok'))
        continue
    if y == 'RAY':
        b = destekler(a, p)
        b = b[0] if b else [x[0] for x in TEMAS[a] if x[1] < 0.3][0]
        pt = patch(a, b)
        if pt is None: ACIK.append((a, 'ray: temas yok')); continue
        S, e = pt
        lo, hi = LO[a], HI[a]; ax = int(np.argmax(hi - lo)); L_ = hi[ax] - lo[ax]
        n_ = int(L_ // p['adim']); c = (lo + hi) / 2
        el = []; neden = []
        for j in range(n_ + 1):
            q = c.copy(); q[ax] = lo[ax] + (L_ - n_ * p['adim']) / 2 + j * p['adim']
            if q[ax] < lo[ax] + 5 or q[ax] > hi[ax] - 5: continue
            # temas düzlemine indir
            s = (S.mean(0) - q) @ e; q = q + e * s
            r, m = vida_tasarla(a, b, q, e, p['d'], bas='a', dis_b=True, no=j, gomme=p.get('gomme', 0.0))
            if r: el += r
            else: neden.append(m)
        if el: SONUC[a] = dict(yontem='VIDA', neden=p['neden'], eleman=el, not_=neden[:3])
        else: ACIK.append((a, 'ray vidası: %s' % neden[:3]))
        continue
    if y == 'VIDA':
        dl = destekler(a, p)
        el = []; neden = []
        for b in dl:
            pt = patch(a, b, tol=0.3 if not p.get('tasi') else 3.0)
            if pt is None: neden.append('%s temas yok' % b); continue
            S, e = pt
            n_ = p.get('n', 2) if len(dl) == 1 else max(1, p.get('n', 2) // len(dl))
            ad_ = [S.mean(0)] if p.get('merkez') else merkezler(S, e, 15, p['d'])
            iyi = []
            sonra = [x for x in P if p.get('sonra_desen') and re.search(p['sonra_desen'], x)]
            b0 = p.get('bas', 'a')
            for bas_ in (b0, 'b' if b0 == 'a' else 'a'):
                for c in ad_:
                    r, m = vida_tasarla(a, b, c, e, p['d'], bas=bas_, dis_a=p.get('dis_a', False) if bas_ == b0 else p.get('dis_b', False),
                                        dis_b=p.get('dis_b', False) if bas_ == b0 else p.get('dis_a', False), std=p.get('std', 'ISO 4762'), no=len(el) + len(iyi), sonra=sonra)
                    if r: iyi.append((c, r))
                    else: neden.append(m)
                if len(iyi) >= n_: break
            if iyi:
                idx = np.linspace(0, len(iyi) - 1, min(n_, len(iyi))).round().astype(int)
                for k_ in sorted(set(idx)):
                    r = iyi[k_][1]
                    for x in r: x['ad'] = x['ad'].rsplit('_', 2)[0] + '_%d_%s' % (len(el), x['tip'])
                    el += r
            if len(el) >= p.get('n', 2) and not p.get('destek'): break
        if el: SONUC[a] = dict(yontem='VIDA', neden=p['neden'], eleman=el, not_=neden[:3])
        else: ACIK.append((a, 'vida: %s' % neden[:4]))
        continue
    ACIK.append((a, 'yöntem işlenmedi %s' % y))
json.dump(dict(sonuc=SONUC, acik=ACIK, tasi=TASI, sil=SIL), open('k_baglanti_plan.json', 'w'), ensure_ascii=False, indent=0, default=float)
import collections
print('ÇÖZÜLEN', len(SONUC), collections.Counter(v['yontem'] for v in SONUC.values()))
print('ELEMAN', collections.Counter(e['tip'] for v in SONUC.values() for e in v.get('eleman', [])))
print('AÇIK', len(ACIK))
for a, m in ACIK: print('  ', a, '·', m)
