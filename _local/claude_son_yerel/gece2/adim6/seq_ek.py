
# ------------------------------------------------------------------ ortak: sac + üstündeki saplamalar · diğer parçalar
SAPLAMA_RX = r'(_saplama|_pem_?[ab]?|_pem_M\d.*|_pem_m8.*|pem_m8_.*|_pem)$'


def sahip_ata(panel_sira):
    """her saplama/PEM → zarfı onu içeren SON panel (K: arka sacın saplamaları yan sacın dönüş deliklerinden geçer)"""
    own = {}
    adaylar = [a for a in P if P[a]['kay'] == 'sac' and re.search(SAPLAMA_RX, a) and P[a]['tur'] != 'arayuz']
    for s in adaylar:
        c = cent(s)
        for pnl in panel_sira:
            lo, hi = bbox([pnl])
            if np.all(c >= lo - 0.004) and np.all(c <= hi + 0.004): own[s] = pnl
    return own


SAHIP = {}


def panel(sacs, d, t, metin, sure=1.4, somun_metin='Pul + fiberli somun içeriden', kamd=None):
    sap = sorted(s for s, p in SAHIP.items() if p in sacs and s not in GOR)
    olay(t, metin); kam(t, sacs, kamd or d)
    t = gel(list(sacs) + sap, d, t, sure, 0) + 0.1
    vs = [s for s in sap if s.endswith('_saplama')]
    if vs:
        olay(t, somun_metin); t = somunlar(vs, t)
    return t


NAD = {'E_SARJOR': 'şarjör + asansör', 'E_BESLEYICI': 'besleyici (vakum)', 'E_KALIP': 'katlama kalıbı', 'E_KOPRU': 'köprü', 'E_PISTON': 'piston',
       'E_PARMAK': 'ön parmak', 'E_KAPAK': 'kapak katlayıcı', 'E_KOSE': 'köşe katlayıcı + kaldırıcı', 'E_COP': 'robot çöpü', 'DUZ_E_OLUK': 'çöp oluğu',
       'B_SOGUTMA': 'soğutma grubu (Secop)', 'DUZ_B_SERPANTIN': 'evaporatör serpantini', 'B_DEPO': 'soğuk depo çekmecesi',
       'U_F_HAVALANDIRMA': 'havalandırma fanı + panjur', 'TOPPING_MODUL': 'açıcı', 'TOPPING_DONER': 'açıcı konisi', 'E_KUTU': 'kutu',
       'E_ELEKTRIK': 'E elektrik', 'U_F_GOVDE': 'U_F kapak elemanı'}


def sinif(a):
    p = P[a]; c = p['m']; dg = ANA_BILGI[a]['dugum']
    if c == 'urun': return 'urun'
    if ANA_BILGI[a]['kpk'] or c == 'kapak_s': return 'kapak'
    if c == 'hava': return 'hava'
    if c in ('guc', 'bilgi'): return 'kablo'
    if c == 'fis': return 'fis'
    if c == 'kanal': return 'kanal'
    if 'ELEKTRIK' in dg or dg.startswith('ELK_'): return 'elektrik'
    return 'mek'


def diger(t, no, adlar, mek_metin):
    """ana GLB gruplarını sırayla yerleştirir: mekanizmalar → elektrik kutusu + kanallar → kablolar + fiş → hava → kapaklar → ürün"""
    S = {}
    for a in adlar:
        if a in GOR or a in GIZLI: continue
        S.setdefault(sinif(a), []).append(a)
    if S.get('mek'):
        t0 = t; kam(t, S['mek'], (0, 0.2, 1))
        grp = {}
        for a in S['mek']: grp.setdefault(ANA_BILGI[a]['dugum'].split('__')[0], []).append(a)
        sira = sorted(grp, key=lambda k: (round(bbox(grp[k])[0][1], 1), bbox(grp[k])[0][0]))
        for k in sira:
            olay(t, '%s — ön açıklıktan içeri, PEM saplamalara pul + fiberli somunla' % NAD.get(k, k.replace('_', ' ').lower()))
            kam(t, grp[k], (0, 0.2, 1))
            t = gel(sorted(grp[k]), (0, 0.15, 0.85), t, 1.3) + 0.25
        adim(no, 'Mekanizmalar', t0, t + 0.3, mek_metin, ' · '.join(NAD.get(k, k) for k in sira)); t += 0.3; no += 1
    el = S.get('elektrik', []) + S.get('kanal', [])
    if el:
        t0 = t
        if S.get('elektrik'):
            olay(t, 'Elektrik kutusu / pano, DIN ray cihazları ve sensör braketleri yerine (PEM saplamalara)')
            kam(t, S['elektrik'], (0, 0.2, 1))
            t = gel(sorted(S['elektrik']), (0, 0.1, 0.7), t, 1.3, min(0.15, 3.0 / max(1, len(S['elektrik'])))) + 0.3
        if S.get('kanal'):
            olay(t, 'İç kablo kanalları duvar / tavan boyunca (PEM saplamalı kanal ayakları)')
            kam(t, S['kanal'], (0, 0.2, 1))
            t = gel(sorted(S['kanal']), (0, 0, 0.5), t, 1.2, 0.15) + 0.3
        adim(no, 'Elektrik kutusu + iç kanallar', t0, t + 0.3, "Elektrik kutusu (sürücüler, G/Ç, sigorta) istasyonun kendi gövdesinde, PEM saplamalara oturur. Kablolar yalnız kanal içinden yürür; kanal kapakları kablolar çekildikten sonra kapanır.",
             'elektrik kutusu · DIN ray cihazları · sensör braketleri · iç kanallar'); t += 0.3; no += 1
    kb = S.get('kablo', []) + S.get('fis', [])
    if kb:
        t0 = t
        guc = [a for a in S.get('kablo', []) if P[a]['m'] == 'guc']; bil = [a for a in S.get('kablo', []) if P[a]['m'] == 'bilgi']
        if S.get('fis'):
            olay(t, 'Gömme fiş paneli: Harting / M12 soketler + kablo rakorları (dışarıdan, contalı)')
            kam(t, S['fis'], (0, 0.1, 1))
            t = gel(sorted(S['fis']), (0, 0, 0.35), t, 1.0, 0.1) + 0.3
        if guc:
            olay(t, 'Güç kabloları (KIRMIZI) — fiş panelinden kutuya, kutudan motorlara, kanal içinden')
            kam(t, guc, (0, 0.2, 1)); t = gel(sorted(guc), (0, 0, 0.45), t, 1.4, 0.12) + 0.3
        if bil:
            olay(t, 'Bilgi kabloları (MAVİ) — sensör, enkoder, EtherCAT / G/Ç, ayrı kanal bölmesinden')
            kam(t, bil, (0, 0.2, 1)); t = gel(sorted(bil), (0, 0, 0.45), t, 1.4, 0.12) + 0.3
        adim(no, 'Kablolar + fiş paneli', t0, t + 0.3, "İstasyona dışarıdan yalnız gömme fiş panelinden girilir (Harting güç, M12 bilgi). İçeride güç (kırmızı) ve bilgi (mavi) kabloları ayrı kanal bölmelerinden yürür; uçlar yüksük + etiketle klemense.",
             'fiş paneli · güç kabloları (kırmızı) · bilgi kabloları (mavi)'); t += 0.3; no += 1
    if S.get('hava'):
        t0 = t; olay(t, 'Hava hortumları (YEŞİL) — valf adasından silindir / vakuma, kanal ve kelepçelerle')
        kam(t, S['hava'], (0, 0.2, 1)); t = gel(sorted(S['hava']), (0, 0, 0.45), t, 1.4, 0.12) + 0.6
        adim(no, 'Hava hattı', t0, t, "Basınçlı hava gömme rakordan girer, şartlandırıcı + valf adasından hortumlarla tüketicilere gider. Hortumlar kablo kanalının hava bölmesinden ve kelepçelerle.",
             'rakor · valf adası · hava hortumları (yeşil)'); no += 1
    if S.get('kapak'):
        t0 = t; olay(t, 'Kapak elemanları önden takılır (menteşe, bas-aç, fitil)')
        kam(t, S['kapak'], (0, 0.1, 1)); t = gel(sorted(S['kapak']), (0, 0, 0.5), t, 1.3, 0.12) + 0.6
        adim(no, 'Kapak elemanları', t0, t, "Kapak elemanları en son, iç montaj ve kablolama bittikten sonra takılır: menteşe yarıları, bas-aç mandalları ve fitiller.", 'menteşe · bas-aç · fitil'); no += 1
    if S.get('urun'):
        t0 = t; olay(t, 'Ürün / sarf yüklenir (görsel)')
        kam(t, S['urun'], (0, 1, 0.6)); t = gel(sorted(S['urun']), (0, 0.35, 0.2), t, 1.2, min(0.1, 3.0 / len(S['urun']))) + 0.6
        adim(no, 'Ürün', t0, t, "En son ürün ve sarf malzemesi yüklenir — devreye alma testi için.", 'ürün (görsel)'); no += 1
    return t, no


def seq_B():
    global SAHIP
    BASLIK.update(kod='B')
    SECIM[:] = [('dis_sol_yan', 1), ('dis_taban_1', 1), ('dis_arka_1', 1), ('dis_tavan_2', 1), ('ic_sol_duvar', 1), ('ic_taban_1', 1), ('bolme_1_sac_a', 1),
                ('isi_kalkani_u', 1), ('on_cerceve_1', 1), ('kosebent_sol_alt_2', 1)]
    t = kartlar(0.0, 'dış kabuk 2 parçalı + ek lamaları · iç kabuk · 9 bölme sacı · 14 kovan · ısı kalkanı · ön çerçeve 2 parça · 126 ray PEM SP-M5')
    PANEL = ['dis_taban_1', 'dis_taban_2', 'dis_sol_yan', 'dis_sag_yan', 'dis_arka_1', 'dis_arka_2', 'ic_taban_1', 'ic_taban_2', 'ic_sol_duvar', 'teknik_sol_duvar',
             'ic_arka_1', 'ic_arka_2'] + R(r'^bolme_\d_sac_[ab]$') + ['ic_tavan_1', 'ic_tavan_2', 'dis_tavan_1', 'dis_tavan_2']
    SAHIP = sahip_ata(PANEL)
    t4 = t; kam(t, None)
    olay(t, '14 ayarlı ayak zemine, terazide')
    t = gel(R(r'^M__B_KASA__celik'), (0, 0.25, 0), t, 1.0) + 0.1
    olay(t, "Alt şase + PU'ya gömülecek dikme / kirişler (B_MODULER) + GFRP pedler — ayakların üstüne")
    t = gel(R(r'^M__B_MODULER__'), (0, 0.5, 0), t, 1.5, 0.2) + 0.1
    olay(t, "Taşıyıcı (K'nın oturduğu çapraz kirişler)")
    t = gel(R(r'^M__B_TASIYICI__'), (0, 0.4, 0), t, 1.1) + 0.5
    adim(4, 'Ayaklar · alt şase · gömülü iskelet', t4, t,
         "B dolabı kendi şasesi üstünde kurulur: ayaklar, alt şase boyunaları, PU'ya gömülecek dikme ve kirişler (A ve K bunların üstüne oturur) ve aradaki GFRP ısı köprüsü pedleri. Sac kabuk bu iskeletin çevresine kapanır.",
         '14 ayak · alt şase + dikmeler (B_MODULER) · GFRP ped · taşıyıcı kirişler')
    t5 = t
    t = panel(['dis_taban_1', 'dis_taban_2'], (0, 0.4, 0), t, 'Dış taban 2 parça (ek x 2091) dikmelerin geçişlerinden iner')
    t = gel(['dis_taban_ek_lamasi'], (0, 0.15, 0), t, 0.7) + 0.1
    olay(t, '10 × M8 × 20 + DIN 9021 içeriden şaseye (köpüklemeden ÖNCE)')
    kam(t, R(r'^arayuz_sase'), (0, 1, 0.3))
    t = gel(R(r'^arayuz_sase.*_pul$'), (0, 0.12, 0), t, 0.45, 0.05)
    t = gel(R(r'^arayuz_sase'), (0, 0.18, 0), t, 0.5, 0.05) + 0.2
    olay(t, 'Alt köşebentler (yan sacı tabana bağlar)')
    t = gel(R(r'^kosebent_s(ol|ag)_alt'), (0, 0.2, 0), t, 0.7, 0.06) + 0.1
    t = panel(['dis_sol_yan'], (-0.6, 0, 0), t, 'Sol dış yan sac (yalnız arka dönüş) — köşebentlere')
    t = panel(['dis_sag_yan'], (0.6, 0, 0), t, 'Sağ dış yan sac — E kabuğuna yüz yüze, dış yüz düz')
    t = panel(['dis_arka_1', 'dis_arka_2'], (0, 0, -0.6), t, 'Dış arka 2 parça arkadan + ek laması')
    t = gel(['dis_arka_ek_lamasi'], (0, 0, -0.15), t, 0.7) + 0.1
    olay(t, 'Ek yerleri ve arka köşeler gıda silikonuyla kapatılır (köpük sızmasın)')
    t = yerinde(R(r'^ek_yeri_silikon_(taban|arka)$') + R(r'^arka_kose_silikonu'), t, 0.5, 0.15) + 0.4
    adim(5, 'Dış kabuk · taban → yanlar → arka', t5, t,
         "Dış kabuk iki parçalıdır (levha boyu 3000 sınırı): taban ve arka x 2091'de ek lamasıyla birleşir. Yan saclar tava değil, yalnız arka dönüşlü; tabana köşebentle bağlanır. Şase cıvataları köpüklemeden önce içeriden takılır.",
         'dış taban 2 + ek laması · 10 × M8 şase cıvatası · 8 alt köşebent · 2 yan · dış arka 2 + ek laması · silikon')
    t6 = t
    t = panel(['ic_taban_1', 'ic_taban_2'], (0, 0, 0.9), t, 'İç taban 2 parça önden — dikme geçişleri 31 × 31')
    t = panel(['ic_sol_duvar', 'teknik_sol_duvar'], (0, 0, 0.9), t, "İç sol duvar + teknik bölme duvarı — ray PEM'leri düz sacta basılı geldi")
    t = panel(['ic_arka_1', 'ic_arka_2'], (0, 0, 0.9), t, 'İç arka 2 parça · iç köşeler TIG + taşlama')
    olay(t, "Bölme sacları (çift cidar a/b) önden — her yüzde 3 ray PEM'i SP-M5")
    kam(t, R(r'^bolme_\d_sac'), (0, 0.3, 1))
    for b in sorted(set(re.sub(r'_sac_[ab]$', '', a) for a in R(r'^bolme_\d_sac_[ab]$'))):
        sacs = R(r'^%s_sac_[ab]$' % b)
        sap = sorted(s for s, p in SAHIP.items() if p in sacs and s not in GOR)
        t = gel(sacs + sap, (0, 0, 0.9), t, 1.0, 0) + 0.15
    olay(t, 'Kablo / gider kovanları (U, L) bölmelere · köpüğe açılan köşe ağızları TIG')
    t = gel(R(r'^bolme_\d_kovan_\d+(_ust_L)?$'), (0, 0.15, 0), t, 0.7, 0.05)
    t = kaynak(R(r'kovan_\d+_kose_kaynagi'), t) + 0.2
    t = panel(['ic_tavan_1', 'ic_tavan_2'], (0, 0, 0.9), t, 'İç tavan 2 parça önden')
    olay(t, 'Isı kalkanı (fırın altı): U sac + ışınım sacı + 12 PTFE / cam elyaf takoz')
    kam(t, R(r'^isi_kalkani'), (0, 0.4, 1))
    t = gel(R(r'^isi_kalkani_takozu'), (0, 0.15, 0), t, 0.5, 0.04)
    t = gel(R(r'^isi_kalkani_(u|isinim)'), (0, 0, 0.9), t, 1.2, 0.2) + 0.1
    t = gel(R(r'^tk_ara_arka_sac'), (0, 0, 0.6), t, 0.9) + 0.4
    adim(6, 'İç kabuk · bölmeler · kovanlar · ısı kalkanı', t6, t,
         "İç kabuk ve bölme ön kenarları ön çerçeveye ALIN gelir. Çekmece raylarının 126 PEM SP-M5'i duvar ve bölme saclarına düz hâlde basılmıştır. Bölmelerde kanal ve gider için 1 mm boşluklu U / L kovanlar; köpüğe açılan köşe ağızları kaynakla kapanır. Fırın altına ısı kalkanı.",
         'iç taban 2 · iç sol duvar · teknik duvar · iç arka 2 · 9 bölme sacı · 14 kovan · iç tavan 2 · ısı kalkanı + 12 takoz')
    t7 = t
    olay(t, 'Üst köşebentler')
    t = gel(R(r'^kosebent_s(ol|ag)_ust'), (0, 0.2, 0), t, 0.7, 0.06) + 0.1
    t = panel(['dis_tavan_1', 'dis_tavan_2'], (0, 0.5, 0), t, 'Dış tavan 2 parça üstten (A ve K bağlantı delikleri Ø9 hazır)')
    t = gel(R(r'^dis_tavan_ek_lamasi'), (0, 0.15, 0), t, 0.6, 0.08) + 0.1
    olay(t, 'Köpüklemeden önce: PEM gövdelerine PE köpük kapağı, ek yeri + gider silikonları')
    kam(t, None)
    t = yerinde(R(r'_kopuk_kapagi$'), t, 0.4, 0.01)
    t = yerinde(R(r'^ek_yeri_silikon_tavan$') + R(r'gider_silikonu'), t, 0.4, 0.08) + 0.3
    olay(t, 'PU köpükleme (SARI): kalıpta, iç / dış kabuk arası 40 kg/m³ — 24 saat kür')
    pu = [a for a in P if P[a]['tur'] == 'pu' and a not in GOR]
    t = yerinde(sorted(pu), t, 1.6, 0.12) + 0.6
    adim(7, 'Tavan · köpük hazırlığı · PU köpükleme', t7, t,
         "Tavan kapanınca gövde köpükleme kalıbına girer. Önce bütün PEM gövdelerine PE köpük kapağı, ek yerlerine ve gider halkalarına silikon; sonra iç ve dış kabuk arası PU ile doldurulur (sahnede sarı; normalde görünmez).",
         '7 üst köşebent · dış tavan 2 + 3 ek laması · 126 köpük kapağı · silikonlar · 19 PU bloğu')
    t8 = t
    olay(t, 'Ön çerçeve 2 parça (430) önden — ek x 2091 · 35 mm ek laması arkasında')
    kam(t, R(r'^on_cerceve'), (0, 0.2, 1))
    t = gel(['on_cerceve_ek_lamasi'], (0, 0, 0.5), t, 0.8) + 0.1
    t = gel(R(r'^on_cerceve_\d$'), (0, 0, 0.7), t, 1.3, 0.3) + 0.5
    adim(8, 'Ön çerçeve', t8, t, "Kalıptan çıkan gövdeye ön çerçeve takılır; iç kabuk ve bölmeler çerçeveye alın gelir (açık oluk / görünür PU yok).",
         'ön çerçeve 2 parça + ek laması')
    rest = R(r'^M__')
    raylar = [a for a in rest if re.match(r'^M__CEK_.*__celik__\d+$', a)]
    cek_govde = [a for a in rest if a.startswith('M__CEK_') and a not in raylar and P[a]['m'] not in ('urun', 'kapak_s') and not ANA_BILGI[a]['kpk']]
    cek_on = [a for a in rest if a.startswith('M__CEK_') and (P[a]['m'] == 'kapak_s' or ANA_BILGI[a]['kpk'])]
    no = 9
    t, no = diger(t, no, [a for a in rest if not a.startswith('M__CEK_') and sinif(a) == 'mek'],
                  "Soğutma grubu teknik bölmeye, evaporatör ve soğuk depo yerine; hepsi gövdedeki PEM saplamalara pul + fiberli somunla.")
    t, no = diger(t, no, [a for a in rest if not a.startswith('M__CEK_') and sinif(a) in ('elektrik', 'kanal', 'kablo', 'fis', 'hava')], '')
    t0 = t
    olay(t, '42 sabit çekmece rayı önden duvar / bölme yüzlerine')
    kam(t, raylar, (0, 0.3, 1))
    t = gel(sorted(raylar), (0, 0, 0.8), t, 1.0, 0.04) + 0.2
    olay(t, "Her ray 3 × DIN 7991 M5 × 10 havşa başlı — duvardaki PEM SP-M5'lere")
    t = gel(R(r'^arayuz_ray'), (0, 0, 0.12), t, 0.4, 0.008) + 0.4
    adim(no, 'Çekmece rayları', t0, t, "Sabit raylar duvar ve bölme saclarındaki PEM SP-M5'lere havşa başlı vidayla bağlanır (sacın arkası köpüklü olduğu için somun yok — PEM şart).",
         '42 sabit ray · 126 × M5 × 10 havşa başlı'); no += 1
    t0 = t
    olay(t, 'Çekmeceler (tahrik + kızak + kasa) önden raylara sürülür')
    kam(t, cek_govde, (0, 0.3, 1))
    grp = {}
    for a in cek_govde: grp.setdefault(ANA_BILGI[a]['dugum'].split('__')[0], []).append(a)
    for k in sorted(grp, key=lambda k: (bbox(grp[k])[0][0], bbox(grp[k])[0][1])):
        t = gel(sorted(grp[k]), (0, 0, 0.9), t, 0.9) + 0.1
    if cek_on:
        olay(t + 0.3, 'Çekmece ön kapakları + fitiller')
        t = gel(sorted(cek_on), (0, 0, 0.4), t + 0.3, 0.8, 0.05) + 0.4
    adim(no, 'Çekmeceler + ön kapaklar', t0, t, "Her çekmece kendi tahrik motoru ve kızağıyla hazır gelir, önden raya sürülür; ön kapak ve fitil en son.",
         '%d çekmece · ön kapaklar · fitiller' % len(grp)); no += 1
    t, no = diger(t, no, R(r'^M__'), '')
    olay(t, 'B tamam'); kam(t, None); t += 2.0
    for a in R(r'^arayuz_'): GIZLI.add(a)
    return t


def seq_E():
    global SAHIP
    BASLIK.update(kod='E')
    SECIM[:] = [('sol_sac_pizza_penceresi', 1), ('sag_sac', 1), ('arka_sac', 1), ('ust_sac', 1), ('taban_sac_3', 1), ('onyuz_kapak_E_ust_sol', 1),
                ('onyuz_kapak_E_alt_sag_ic_tava', 1), ('sarjor_yan_kapisi', 1), ('govde_kulak_sol_on_1100', 18)]
    t = kartlar(0.0, 'taban 3 mm · ön kasa 3 dikme + 2 kayıt · yan / arka / üst sac · 4 kapak dış + iç tava · şarjör yan kapısı · kulaklar')
    PANEL = ['taban_sac_3', 'sol_sac_pizza_penceresi', 'sag_sac', 'arka_sac', 'ust_sac']
    SAHIP = sahip_ata(PANEL)
    t4 = t; kam(t, None)
    olay(t, '6 ayarlı ayak (GN 20 sınıfı M12) + kontra somun')
    t = gel(R(r'^ayak_\d+(_kontra)?$'), (0, 0.2, 0), t, 0.8, 0.06) + 0.1
    olay(t, 'Kaide rayları (60 × 60) + kayıtlar (40 × 60) fikstürde · uç tapaları · TIG')
    t = gel(R(r'^kaide_e_ray_(on|arka)$'), (0, 0.4, 0), t, 1.0, 0.2)
    t = gel(R(r'^kaide_e_kayit_(sol|orta|sag)$'), (0, 0.4, 0), t, 1.0, 0.15)
    t = kaynak(R(r'^kaide_e_kayit_.*kaynak'), t)
    t = gel(R(r'^kaide_e_ray_.*_tapa'), (0, 0, 0.1), t, 0.5, 0.08)
    t = gel(R(r'^kaide_e_ayak_somunu'), (0, -0.1, 0), t, 0.5, 0.05) + 0.4
    adim(4, 'Ayaklar · kaynaklı kaide', t4, t, "Kaide 60 × 60 × 3 raylar ve 40 × 60 × 3 kayıtlardan kaynaklı çerçevedir; uçlar tapalı. Ayaklar kaide rayının altındaki somunlara vidalanır, terazide ayarlanır.",
         '6 ayak + kontra · 2 ray + 4 tapa · 3 kayıt · ayak somunları')
    t5 = t
    t = panel(['taban_sac_3'], (0, 0.4, 0), t, 'Taban sacı 3 mm kaideye')
    olay(t, 'Taban → kaide: M8 vida + somun')
    t = gel(R(r'^kaide_e_vida_'), (0, 0.15, 0), t, 0.5, 0.06)
    t = gel(R(r'^kaide_e_somun_'), (0, -0.12, 0), t, 0.5, 0.06) + 0.1
    olay(t, 'Ön kasa: 3 dikme (sol, orta, sağ) tabana · köşe dikişleri · tepe tapaları')
    kam(t, R(r'^onyuz_dikme_'), (0, 0.2, 1))
    t = gel(R(r'^onyuz_dikme_(sol|sag|orta)$'), (0, 0.6, 0), t, 1.0, 0.2)
    t = kaynak(R(r'^onyuz_dikme_.*taban_kaynagi'), t)
    t = gel(R(r'^onyuz_dikme_.*_tapa$'), (0, 0.15, 0), t, 0.5, 0.08)
    olay(t, 'Ön kayıtlar (y 788) dikmeler arasına')
    t = gel(R(r'^onyuz_kayit_788_(sol|sag)$'), (0, 0, 0.3), t, 0.8, 0.15)
    t = kaynak(R(r'^onyuz_kayit.*kaynak'), t) + 0.1
    olay(t, 'Panel kulakları: dikme arkasına (yan) ve tabana · kulak başına 2 dikiş')
    kam(t, R(r'^govde_kulak_'), (0, 0.3, 1))
    t = gel(R(r'^govde_kulak_sol_(on|taban)_\d+$'), (-0.25, 0, 0), t, 0.6, 0.05)
    t = gel(R(r'^govde_kulak_sag_(on|taban)_\d+$'), (0.25, 0, 0), t, 0.6, 0.05)
    t = gel(R(r'^govde_kulak_ust_(sol|orta|sag)$'), (0, 0.25, 0), t, 0.6, 0.08)
    t = kaynak(R(r'^govde_kulak_.*_kaynak_[ab]$'), t, 0.3, 0.03)
    t = gel(R(r'^govde_kosebent_[a-z_]+$'), (0.2, 0, 0), t, 0.6) + 0.4
    adim(5, 'Taban · ön kasa · kulaklar', t5, t, "Taban 3 mm sac kaideye cıvatalanır. Ön kasanın 3 dikmesi tabana kaynaklanır; y 788'de kayıtlar alt ve üst kapakları ayırır. Kulaklar yan ve üst sacı taşır.",
         'taban 3 mm · 7 M8 vida + somun · 3 dikme + tapa · 2 kayıt · 39 kulak · köşebent')
    t6 = t
    t = panel(['sol_sac_pizza_penceresi'], (-0.6, 0, 0), t, "Sol yan sac (pizza penceresi, K'dan gelen ürün için) — FHP saplamalar kulaklara")
    t = panel(['sag_sac'], (0.6, 0, 0), t, 'Sağ yan sac (şarjör kapısı açıklığı) — saplamalar kulaklara')
    t = panel(['arka_sac'], (0, 0, -0.6), t, 'Arka sac arkadan: taban üstünden başlar, alt iç dönüş tabana')
    t = panel(['ust_sac'], (0, 0.55, 0), t, 'Üst sac yan sacların ARASINA oturur (21,5 aşağı dönüş) · U_KE için 3 × PEM SP-M8')
    olay(t, 'Şarjör kapısı taşıyıcı lamaları (arka sacta menteşe, yan sacta bas-aç)')
    kam(t, R(r'^sarjor_yan_kapisi_(mentese|basac)_lamasi'), (1, 0, 0))
    t = gel(R(r'^sarjor_yan_kapisi_(mentese|basac)_lamasi$'), (0.2, 0, 0), t, 0.7, 0.1)
    vs = R(r'^govde_bag_kapi_.*_saplama$')
    t = gel(vs, (0.15, 0, 0), t, 0.5, 0.05)
    t = somunlar(vs, t)
    kal = R(r'_saplama$')
    if kal:
        olay(t, 'Kalan köşe bağlantıları (köşebent) · pul + somun')
        t = gel(kal, (0, 0, 0.1), t, 0.5, 0.05); t = somunlar(kal, t)
    t = yerinde(R(r'^govde_pem_m8_ust'), t, 0.4, 0.05) + 0.3
    adim(6, 'Paneller · yan → arka → üst', t6, t, "Yan saclar kulaklara preslenmiş FHP-M5 saplamalarla oturur, pul + fiberli somun içeriden (dışta iz yok). Arka sac arkadan, üst sac yan sacların arasına. Şarjör yan kapısının lamaları arka ve yan saca bağlanır.",
         'sol yan (pizza penceresi) · sağ yan · arka · üst · şarjör kapısı lamaları · M5 pul + fiberli somun')
    no = 7
    rest = R(r'^M__')
    t, no = diger(t, no, [a for a in rest if sinif(a) in ('mek', 'elektrik', 'kanal', 'kablo', 'fis', 'hava')],
                  "Mekanizmalar alttan yukarı sırayla ön açıklıktan girer (kapaklar daha takılmadı): her biri gövdedeki PEM saplamalara (ARAYÜZ listesi) pul + fiberli somunla bağlanır.")
    t0 = t
    olay(t, '12 gizli menteşe gövdesi dikmelere + 2 × M5 · 6 bas-aç orta dikmeye')
    kam(t, R(r'^onyuz_kapak_E_mentese_.*_sabit$'), (0, 0, 1))
    t = gel(R(r'^onyuz_kapak_E_mentese_(sol|sag)_\d+_sabit$'), (0, 0, 0.15), t, 0.6, 0.06)
    t = gel(R(r'^onyuz_kapak_E_mentese_(sol|sag)_\d+_sabit_vida_[ab]$'), (0, 0, 0.06), t, 0.4, 0.02)
    t = gel(R(r'^onyuz_kapak_E_basac_'), (0, 0, 0.12), t, 0.5, 0.06) + 0.2
    for kap_ad, taraf in [('onyuz_kapak_E_alt_sol', 'sol'), ('onyuz_kapak_E_alt_sag', 'sag'), ('onyuz_kapak_E_ust_sol', 'sol'), ('onyuz_kapak_E_ust_sag', 'sag')]:
        mn = '[012]' if '_alt_' in kap_ad else '[345]'
        rx_kanat = r'^onyuz_kapak_E_mentese_%s_%s_kanat$' % (taraf, mn)
        KAP = sorted(set([a for a in P if a.startswith(kap_ad) and a not in GOR] + R(rx_kanat)))
        t = kapak_alt(kap_ad, KAP, t, kap_ad + '_ic_tava', r'^%s_robot_agzi_kasa_\w+$' % kap_ad, r'^%s_karsilik_\d$' % kap_ad,
                      rx_kanat, r'^$', r'^%s_kose_kaynagi_\d$' % kap_ad, etiket='%s ' % kap_ad.replace('onyuz_kapak_E_', '').replace('_', ' '))
        piv = (4.402, 0.079) if taraf == 'sol' else (5.23, 0.079)
        KAPAK_PIV[kap_ad] = (KAP, piv, -100.0 if taraf == 'sol' else 100.0)
    olay(t, 'Kapaklar bas-aç ile açılır / kapanır — sol kanatlar x 4402, sağ kanatlar x 5230 ekseninde')
    kam(t, None, yon=(0.4, 0.5, 1.2))
    for kad, (KAP, piv, aci) in KAPAK_PIV.items(): kapak_doner(KAP, piv, aci, t, t + 2.0, t + 3.0, t + 5.0)
    t += 5.5
    olay(t, 'Şarjör yan kapısı: iç tava + dış tava, menteşeler arka sactaki lamaya, bas-aç yan sactaki lamaya')
    kam(t, ['sarjor_yan_kapisi'], (1, 0, 0))
    t = gel(R(r'^sarjor_yan_kapisi_mentese_?\d*$'), (0.12, 0, 0), t, 0.6, 0.1)
    t = gel(R(r'^sarjor_yan_kapisi'), (0.5, 0, 0), t, 1.2) + 0.5
    adim(no, 'Kapaklar · menteşe · bas-aç', t0, t, "4 ön kapak (2 × 2) tezgâhta kurulur: iç tava + karşılıklar + menteşe kanatları, üstüne dış tava (köşeler TIG); üst sol kapakta robot ağzı kasası. Kapaklar önden asılır, kulp yok, bas-aç ile açılır. Şarjör yan kapısı sağdan.",
         '12 gizli menteşe · 6 bas-aç · 4 kapak (dış + iç tava) · robot ağzı kasası · şarjör yan kapısı'); no += 1
    t, no = diger(t, no, R(r'^M__'), '')
    olay(t, 'E tamam'); kam(t, None); t += 2.0
    return t


def seq_U():
    global SAHIP
    BASLIK.update(kod='U')
    SECIM[:] = [('ust_f_taban_sac', 1), ('ust_f_yan_sol', 1), ('ust_f_arka_sac', 1), ('ust_f_tavan_sac', 1), ('ust_ke_tavan_sac', 1), ('f_ust_yan_sag', 1),
                ('f_ust_taban_levhasi', 1), ('f_ust_tavan_sac', 1), ('f_davlumbaz_bolme_duvari', 1), ('ust_f_giris_cebi', 1)]
    t = kartlar(0.0, 'F üst kabin 10 sac + 6 profil · U_F 6 sac · U_KE 5 sac · omega profiller · panjur lamelleri')
    PANEL = ['f_ust_taban_levhasi', 'f_ust_yan_sol', 'f_ust_yan_sag', 'f_ust_arka_sac', 'f_davlumbaz_bolme_duvari', 'f_ust_tavan_sac',
             'ust_f_taban_sac', 'ust_f_yan_sol', 'ust_f_yan_sag', 'ust_f_arka_sac', 'ust_f_tavan_sac', 'ust_f_giris_cebi',
             'ust_ke_taban_sac', 'ust_ke_yan_sol', 'ust_ke_yan_sag', 'ust_ke_arka_sac', 'ust_ke_tavan_sac']
    SAHIP = sahip_ata(PANEL)
    t4 = t; kam(t, R(r'^f_ust_|^onyuz_f_ust'), (0, 1, 0))
    olay(t, 'F üst kabini: 3 alt profil (ön, orta, arka) fikstürde · yan kaynaklar')
    t = gel(R(r'^f_ust_alt_profil_(on|orta|arka)$'), (0, 0.4, 0), t, 1.0, 0.2)
    t = kaynak(R(r'^f_ust_alt_profil_.*kaynagi'), t) + 0.1
    t = panel(['f_ust_taban_levhasi'], (0, 0.45, 0), t, 'Taban levhası profillerin üstüne · 15 delik kaynağı')
    t = kaynak(R(r'^f_ust_taban_levhasi_delik_kaynagi'), t, 0.35, 0.05)
    olay(t, 'Rakor + kablo kovanları tabandan; taş yünü yalıtım kılıf tavasına, kılıf perçinle tabana')
    t = gel(R(r'^f_ust_taban_(rakor|v2)_kovani$'), (0, -0.2, 0), t, 0.7, 0.15)
    t = yerinde(R(r'^f_ust_taban_yalitimi_'), t, 0.8, 0.2)
    t = gel(R(r'^f_ust_taban_yalitim_kilifi_'), (0, -0.3, 0), t, 1.0, 0.2)
    t = yerinde(R(r'^f_ust_kilif_percin_'), t, 0.3, 0.02) + 0.1
    olay(t, 'Ön üst kayıt + orta dikme + tavan kirişi (tapalı) · kaynaklar')
    t = gel(R(r'^onyuz_f_ust_ust_kayit$') + R(r'^onyuz_f_ust_dikme_\d$'), (0, 0, 0.35), t, 0.9, 0.2)
    t = gel(R(r'^f_ust_tavan_kirisi$'), (0, 0.3, 0), t, 0.8)
    t = gel(R(r'^f_ust_tavan_kirisi_tapa$'), (0, 0, -0.1), t, 0.5)
    t = kaynak(R(r'^onyuz_f_ust_.*kaynagi|^f_ust_tavan_kirisi_kaynagi'), t) + 0.4
    adim(4, 'F üst kabini · profiller · taban · yalıtım', t4, t, "F'nin üst kabini fırının üstündedir: 3 alt profil taban levhasını taşır, levhanın altı taş yünüyle yalıtılır (kılıf tavası perçinli). Önde üst kayıt ve orta dikme, üstte tavan kirişi.",
         '3 alt profil · taban levhası + 15 delik kaynağı · 2 kovan · taş yünü + kılıf · ön kayıt + dikme · tavan kirişi')
    t5 = t
    t = panel(['f_ust_yan_sol'], (-0.6, 0, 0), t, 'Sol yan sac (y 788–1862, fırın bölgesi dahil) — J1 ağzı')
    t = panel(['f_ust_yan_sag'], (0.6, 0, 0), t, "Sağ yan sac — K'dan gelen tartı / yağ hortumu geçişleri")
    t = panel(['f_ust_arka_sac'], (0, 0, -0.6), t, 'Arka sac arkadan · köşebent')
    t = gel(R(r'^govde_fu_kosebent_[a-z_]+$'), (0, 0, -0.2), t, 0.6) + 0.1
    t = panel(['f_davlumbaz_bolme_duvari'], (0, 0.45, 0), t, 'Davlumbaz bölme duvarı (atış kanalı ile ayrılır)')
    olay(t, 'Panjur lamelleri (2 × 8) havalandırma ağzına · lamel başına 2 dikiş')
    kam(t, R(r'^f_ust_panjur_lameli_\d_\d$'), (0, 0.3, -1))
    t = gel(R(r'^f_ust_panjur_lameli_\d_\d$'), (0, 0, -0.2), t, 0.5, 0.04)
    t = kaynak(R(r'^f_ust_panjur_lameli_.*_kaynak'), t, 0.3, 0.02)
    t = panel(['f_ust_tavan_sac'], (0, 0.5, 0), t, 'Tavan sacı üstten')
    kal = R(r'^govde_fu_.*_saplama$')
    if kal:
        olay(t, 'Kalan bağlantılar · pul + somun'); t = gel(kal, (0, 0, 0.1), t, 0.5, 0.03); t = somunlar(kal, t)
    t = yerinde(R(r'^govde_fu_pem'), t, 0.4, 0.05) + 0.3
    adim(5, 'F üst kabini · yanlar · arka · bölme · panjur · tavan', t5, t, "Yan saclar yalnız arka dönüşlü (J1/J2 kanalı için kısaltıldı); FHP saplamalı bağlantılar içeriden pul + fiberli somunla. Davlumbaz bölme duvarı, panjur lamelleri ve tavan sacı.",
         'sol / sağ yan · arka + köşebent · davlumbaz bölme duvarı · 16 panjur lameli · tavan')
    t6 = t
    for b, ad in (('f', 'U_F (F üstü, ana pano bölmesi)'), ('ke', 'U_KE (K + E üstü)')):
        t = panel(['ust_%s_taban_sac' % b], (0, 0.45, 0), t, '%s: taban sacı' % ad)
        t = panel(['ust_%s_yan_sol' % b], (-0.5, 0, 0), t, 'Sol yan sac')
        t = panel(['ust_%s_yan_sag' % b], (0.5, 0, 0), t, 'Sağ yan sac · taban yan kaynakları')
        t = kaynak(R(r'^ust_%s_taban_yan_kaynagi' % b), t, 0.3, 0.04)
        t = panel(['ust_%s_arka_sac' % b], (0, 0, -0.5), t, 'Arka sac arkadan')
        if b == 'f': t = panel(['ust_f_giris_cebi'], (0, 0, -0.3), t, 'Gömme bina giriş cebi (rakorlar cebin içinde)')
        olay(t, 'Omega profil (hazır haddeli) tavanın altına · punta')
        t = gel(R(r'^ust_%s_tavan_omegasi' % b), (0, 0.3, 0), t, 0.7)
        t = panel(['ust_%s_tavan_sac' % b], (0, 0.45, 0), t, 'Tavan yan sacların ARASINA, dört kenar dönüşlü')
        kal = R(r'^govde_%s_.*_saplama$' % b)
        if kal:
            olay(t, 'Kalan bağlantılar · pul + somun'); t = gel(kal, (0, 0, 0.1), t, 0.5, 0.03); t = somunlar(kal, t)
    olay(t, "U_F ↔ U_KE: 3 × M8 vida + 2 pul + somun · U_F → fırın PEM'leri")
    kam(t, R(r'^govde_f_ke_m8'), (0, 1, 0.4))
    t = gel(R(r'^govde_f_ke_m8.*_vida$'), (-0.12, 0, 0), t, 0.5, 0.1)
    t = gel(R(r'^govde_f_ke_m8.*_(pul\d|somun)$'), (0.12, 0, 0), t, 0.5, 0.05)
    t = yerinde(R(r'^govde_f_m8_firin|^govde_ke_m8_e'), t, 0.4, 0.06) + 0.4
    adim(6, 'U_F + U_KE kabinleri', t6, t, "Üst kabinler aynı düzende: taban → yanlar (taban yan kaynakları) → arka → omega + tavan. Tavan yan sacların arasına oturur. U_F'de bina beslemesi için gömme giriş cebi; U_F ile U_KE 3 × M8 ile birbirine bağlanır.",
         'U_F: taban, 2 yan, arka, giriş cebi, omega, tavan · U_KE: taban, 2 yan, arka, omega, tavan · 3 × M8')
    no = 7
    t, no = diger(t, no, R(r'^M__'), "Ana pano U_F'nin içinde bağımsız bir paslanmaz pano ürünüdür (ayakları U_F tabanındaki PEM'lere); havalandırma fanı ve panjuru U_F arka sacına.")
    olay(t, 'U tamam'); kam(t, None); t += 2.0
    return t
