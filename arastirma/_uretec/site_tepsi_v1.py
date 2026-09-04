# -*- coding: utf-8 -*-
# otonom/index.html: ROBOT TEPSI UCU (Kemal, 4 Eyl 2026) — TOPPING v8, PRESS, OVEN, PACK, PICKUP notu, OMURGA + problem defterleri
import io, re
P = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\index.html"
t = io.open(P, encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:90])
    t = t.replace(o, n)
TD = '<td style="padding:8px 12px 8px 0;vertical-align:top;width:27%;font-weight:700;color:#1d7a4f;border-bottom:1px solid #d7e8dc">'
TD2 = '<td style="padding:8px 0;vertical-align:top;border-bottom:1px solid #d7e8dc">'
TB = '<td style="padding:8px 12px 8px 0;vertical-align:top;width:27%;font-weight:700;color:#1a49b8;border-bottom:1px solid #d3dff2">'
TB2 = '<td style="padding:8px 0;vertical-align:top;border-bottom:1px solid #d3dff2">'
OK = '<li style="margin:3px 0"><b style="color:#1d7a4f">✔ ÇÖZÜLDÜ</b> — '
ON = '<li style="margin:3px 0"><b style="color:#9a6b1f">◐ ÖNERİ</b> — '
AC = '<li style="margin:3px 0"><b style="color:#b3452b">○ AÇIK</b> — '

# ================= TOPPING =================
rep("+ her birinin altında <b>motorlu hücreli çark + kendi çıkışı</b> + <b>döner-kayar tabla</b> + altta <b>geçiş rafı</b> (robot kaset takası) ;",
    "+ her birinin altında <b>motorlu hücreli çark + kendi çıkışı</b> + altında <b>AÇIK dozaj boşluğu</b> (robot, pideyi TEPSİ ucuyla çıkışların altında gezdirir — <b>tabla YOK</b>) + <b>geçiş rafı</b> (robot kaset takası);")
rep('<img src="img/ist3_topping_detay_v7.png" alt="TOPPING istasyonu detay v7"', '<img src="img/ist3_topping_detay_v8.png" alt="TOPPING istasyonu detay v8"')
i = t.index(TD + "Döner + kayar tabla</td>"); j = t.index("</td></tr>", i) + len("</td></tr>")
t = t[:i] + TD + "Dozaj hareketi — ROBOT + TEPSİ (✔ Kemal, v8)</td>" + TD2 + "Döner-kayar tabla, kızak, 2 motor ve 2 sürücü <b>KALKTI</b>. Pide, robotun <b>tepsi ucunda</b> gelir; kol tepsiyi ilgili çıkışın altına götürür ve <b>kendisi gezdirir</b>: kaşar için köşeden merkeze spiral, sucuk için halka, kavurma için serpme — desen yazılımda (reçete = yol + cep sayısı). <b>Her haznenin KENDİ çıkışı</b>, 4 ayrı ağız, her biri kendi kasetinin altında; çıkış konumu artık serbest, tek sınır tepsinin duvara çarpmaması: tepsi Ø34 merkezi x 20-52 cm, arka duvara 17 cm; ön taraf AÇIK (robot tarafı, duvar yok). Çıkışlar buna göre içe çekildi (x 20 · 40 · 47 · 52; kaset kenarındakini koni 3-8 cm içeri taşır, boru değil). Dozaj boşluğu <b>soğutulmaz ve kapaksız</b>: çıkış ağızları soğuk kabinin izoleli tabanından 3 cm sarkar, robot 20 sn içeride kalsa da soğuk kaçmaz; geçiş rafı ayrı soğuk bölme, arka duvardan hava kanalı.</td></tr>" + t[j:]
rep('Tablanın altı "yedek deposu" değil <b>geçiş rafı</b>', 'Dozaj boşluğunun altı "yedek deposu" değil <b>geçiş rafı</b>')
rep(TD2 + "1) kol basılmış tabanı tablaya koyar → 2) BEYİN reçeteyi açar (kaşarlı = H2 4 cep; karışık = H1 3 + H2 4 + H3 3 cep) → 3) tabla ilgili çıkışın altına kayar + döner, o çark cep cep bırakır → 4) kol pideyi fırına götürür. Toplam ~20-30 sn.</td>",
    TD2 + "1) taban zaten TEPSİDE gelir (press'ten beri) → 2) BEYİN reçeteyi açar (kaşarlı = 4 cep; karışık = 3+4+3 cep) → 3) kol tepsiyi ilgili çıkışın altında gezdirir, çark cep cep bırakır (spiral/halka/merkez) → 4) kol pideyi tepsiyle fırına götürür. Dozaj ~20 sn.</td>")
rep("kaset takasında kaset yıkanır; tabla silinir. Hazne bölgesi kapalı ve soğuk", "kaset takasında kaset yıkanır; dozaj boşluğu (açık, soğutulmaz) günlük silinir. Hazne bölgesi kapalı ve soğuk")
rep(OK + "Kasetler farklı boyda olunca çıkışlar pidenin üstüne simetrik gelmiyordu (Kemal): 4 çıkış tablanın kayma ekseni üzerine dizildi (±3 cm), tabla kayar+döner → merkez dahil spiral; simetri gerekmez.</li>",
    OK + "Kasetler farklı boyda olunca çıkışlar pidenin üstüne simetrik gelmiyordu (Kemal): v8'de tabla kalktı, ROBOT tepsiyi çıkışın altında gezdiriyor → çıkış konumu serbest; tek sınır tepsi merkezi x 20-52 (yan duvar), y ≥17 (arka), ön açık — Blender'daki sağ uç çarpması buna göre çözüldü.</li>" +
    OK + "Tabla + kızak + 2 motor + 2 sürücü (Kemal tepsi konsepti): hareket robota geçti, mekanizma tamamen kalktı; dozaj deseni yazılımda.</li>" +
    ON + "Dozaj boşluğu açık ve soğutulmaz: çıkış ağzında bekleyen 1-2 cep oda sıcaklığında — önemsiz; yine de pilotta 1 saat beklemiş cep tartılır.</li>")

# ================= PRESS (STORE karti icinde) =================
rep("bant ~100-300 bin TL, teklifle netleşir.</td>",
    "bant ~100-300 bin TL, teklifle netleşir. <b>TEPSİ İÇİNDE BASMA (✔ Kemal, 4 Eyl):</b> robotun tepsi ucu (Ø34, delikli alüminyum) press'in alt plakasında bekler; kol pençeyle topu tepsiye koyar, üst plaka iner, taban <b>tepsinin içinde</b> şekillenir; kol pençeyi bırakıp tepsiye kilitlenir, pide artık kutuya kadar tepsiden çıkmaz. Şart: üst plaka Ø29 olmalı (Ø40 plaka tepsi bordürüne çarpar) — Fersah'a kalıp/plaka sorusu; tepsi alt plakaya tam oturduğu için darbe yayılır, eğilmez.</td>")
rep(OK + "STORE buzluğu TOPPING'in donmuş kavurma/kuşbaşı kasetlerini de taşır (≈36 L, boş büyüme rafı) — robot erişimi hamurla aynı kapıdan.</li>",
    OK + "STORE buzluğu TOPPING'in donmuş kavurma/kuşbaşı kasetlerini de taşır (≈36 L, boş büyüme rafı) — robot erişimi hamurla aynı kapıdan.</li>" +
    AC + "PRESS — tepsi içinde basma: PZP-400 üst plakası Ø40 → Ø29 plaka/kalıp ve tepsi bordürü (12 mm) ile uyum, ısıtmalı plakanın tepsiyle temas süresi — Fersah'a soru + pilot.</li>")

# ================= OVEN =================
rep(TD2 + "motorlu kapak açılır → kol küreğiyle tabanı sürer → kapak kapanır → süre dolunca açılır, kol alır. Kol zaten hattın ortasında; koy-al toplam ~10 saniye.</td>",
    TD2 + "<b>Kürek YOK — pide TEPSİYLE girer (✔ Kemal):</b> motorlu kapak açılır → kol tepsiyi (pide üstünde) taşın üstüne koyar, <b>uç kilidini açar, çekilir</b> → kapak kapanır → süre dolunca açılır, kol tepsiye yeniden kilitlenir, alır. Sıyırma yok, pideye temas yok. Tepsi 3 mm <b>delikli alüminyum</b> (pizza screen mantığı: taşın ısısı ve buhar deliklerden tabana geçer) + seramik yapışmaz kaplama (400 °C; teflon 350 °C fırında olmaz). Koy-al toplam ~10 sn.</td>")
rep(OK + "Sprey nozülü tıkanması: ısıtmalı tank + hat; haftalık kontrol eleman listesinde.</li>",
    OK + "Sprey nozülü tıkanması: ısıtmalı tank + hat; haftalık kontrol eleman listesinde.</li>" +
    OK + "Kürekle taşa sürme / pişmiş pideyi alma hassasiyeti: pide tepsiyle giriyor, robot sadece kilit açıp kapıyor (Kemal tepsi konsepti).</li>" +
    ON + "Delikli tepside alt kabuk taş kadar çıtır olur mu: pizza screen sektör standardı, pilotta taş-tepsi karşılaştırması; gerekirse delik oranı artırılır.</li>" +
    AC + "Tepsi malzemesi 350 °C fırın + 150 °C press + yıkama döngüsünde kaç tur dayanır (kaplama, düzlem) — pilot 200 tur.</li>")

# ================= PACK =================
rep("Robot bıçak tutmaz. Kesim, hazır çoklu bıçak kafasının motorla bastırılmasıdır; kesilen pide itici plakayla kutuya kayar — kesim ve kutulama tek istasyonda, robotun bir taşıma hareketi silinir.",
    "Robot bıçak tutmaz. Pide fırından çıkıp spreyden geçtikten sonra hâlâ <b>robotun tepsi ucundadır</b>: kol tepsiyi kesim yuvasına oturtur (uç takılı kalır), hazır çoklu bıçak kafası motorla iner, sonra kol tepsiyi <b>eğer</b>, pide tepsinin açık ön ağzından kutuya kayar — itici plaka kalktı; kesim ve kutulama tek istasyonda, robotun hiçbir taşıma hareketi yok.")
rep(TD2 + "kol yerine 24V elektrikli lineer piston (~2.000-3.000 N) — PLC \"kes\" der, kafa 1 saniyede iner; kompresör gerekmez.</td>",
    TD2 + "kol yerine 24V elektrikli lineer piston — PLC \"kes\" der, kafa 1 saniyede iner; kompresör gerekmez. Kuvvet <b>kesim yuvasına</b> gider, robota gelmez (tepsi yuvaya oturur). Kemal: \"birebir kesmesine gerek yok, bıçak izi yeter\" → kuvvet düşük, bıçak tepsi kaplamasını çizmez (0,5 mm durdurucu).</td>")
i = t.index(TD + "Kutuya itme</td>"); j = t.index("</td></tr>", i) + len("</td></tr>")
t = t[:i] + TD + "Kutuya aktarma — robot tepsiyi EĞER (✔ Kemal)</td>" + TD2 + "itici yok: kesim yuvası kutu ağzıyla aynı hizada; kol tepsiyi 15-20° eğer, dilimlenmiş pide tepsinin <b>13 cm açık ön ağzından</b> kutuya kayar (kesim tam değil, izli — dilimler bir arada iner). Boş tepsi kirli tepsi rafına, kol pençe ucuna döner, kutuyu kapatıp göze taşır.</td></tr>" + t[j:]
rep(OK + "Saçet unutulması: kutuyu eleman katlarken içine koyuyor (ıslak mendil) — makine işi değil.</li>",
    OK + "Saçet unutulması: kutuyu eleman katlarken içine koyuyor (ıslak mendil) — makine işi değil.</li>" +
    OK + "İtici dilimleri dağıtır mı: itici kalktı; pide tepsiden eğilerek kayar, kesim izli olduğu için bütün iner (Kemal tepsi konsepti).</li>" +
    ON + "Bıçak yıldızı tepsi bordürüne (Ø32 iç) sığmalı: Cancan 1330 yıldızı Ø30'a göre seçilir/kestirilir; bıçak-tepsi hizası kesim yuvasının pimleriyle.</li>")

# ================= PICKUP — robot eli notu =================
i = t.index(TD + "Robot eli (omurga notu)</td>"); j = t.index("</td></tr>", i) + len("</td></tr>")
t = t[:i] + TD + "Robot uçları (omurga notu)</td>" + TD2 + "<b>Uç değiştirici</b> (PRESS kabinindeki uç yuvası) + iki uç: <b>TEPSİ ucu</b> (Ø34 kilitli tepsi — pide press'ten kutuya kadar tepside, robot pideye hiç dokunmaz) ve <b>PENÇE ucu</b> (gıda silikonu soft parmaklı adaptif pençe 0-140 mm — hamur topu, kutu, kutu kola, 1 L şişe, tatlı paketi, kaset kulbu). Kürek yüzü ve kombine el kalktı. Kol sınıfı <b>≥12 kg</b> (15 kg kaşar kaseti + tutucu): UR16e · Fanuc CRX-20iA/L · Doosan H2017 — kol 700 bin-2 mln TL, 3-4 m ray 150-300 bin, uç değiştirici + 2 uç + kamera 100-200 bin. Hat beyni (Siemens S7-1200 sınıfı PLC + yazılım) 150-400 bin; şasi + pano + montaj 100-200 bin TL.</td></tr>" + t[j:]

# ================= OMURGA =================
rep('<img src="img/kombine_el_detay.png" alt="Kombine el: tek uç dört yük"', '<img src="img/robot_tepsi_el_v1.png" alt="Robot tepsi ucu: pide press\'ten kutuya kadar tepside"')
rep("3-4 m lineer ray üstünde 6 eksenli, 10 kg sınıfı cobot — hattaki her istasyona kayarak ulaşır. Adaylar: Dobot CR10 (ekonomik) · Fanuc CRX-10iA/L · UR10e. Zaman bütçesi doğrulandı: pide başına ~50 sn kol işi → pik saatte (30 pide) doluluk <b>%42</b> — tek kol bol bol yeter; ara konveyör ihtiyacının tamamını siler.",
    "3-4 m lineer ray üstünde 6 eksenli, <b>≥12 kg sınıfı</b> cobot (15 kg kaset takası) — hattaki her istasyona kayarak ulaşır. Adaylar: UR16e · Fanuc CRX-20iA/L · Doosan H2017 (Dobot CR16 ekonomik). Zaman bütçesi (tepsi kurgusuyla): pide başına ~103 sn kol işi (dozaj gezdirme ve 2 uç değişimi kolda) → pik saatte (30 pide) doluluk <b>~%85</b> — tek kol yeter, pay azaldı; fırın zaten 25-35/saat tavanı. Ara konveyör yok.")
i = t.index(TB + "Kombine el</td>"); j = t.index("</td></tr>", i) + len("</td></tr>")
t = t[:i] + TB + "Robot uçları — TEPSİ + PENÇE (✔ Kemal, 4 Eyl)</td>" + TB2 + "<b>Kombine el kalktı.</b> Bilekte <b>uç değiştirici</b> (SMARTSHIFT / RSP CoboShift sınıfı: pim + burç + kilit, 2-3 sn, ±0,1 mm; uç yuvası PRESS kabininde). <b>1 · TEPSİ ucu:</b> Ø34 kulplu tepsi robotun aksesuar ucudur — kulp paslanmaz 30×20×120 = kilit pimi (350 °C'lik tepsiyi silikon pençe tutamaz, metal-metal kilit şart). Taban 3 mm <b>delikli alüminyum</b> + seramik yapışmaz kaplama, bordür 12 mm, <b>13 cm açık ön ağız</b> (kutuya kayma), ~0,8 kg. Pide press'te tepsinin içinde basılır, topping'de kol tepsiyi çıkışların altında gezdirir, fırına tepsiyle girer (kilit açılır), sıcak pideye sprey (yağ erir), kesim tepsi içinde (yuvaya oturur), kutuya eğilerek kayar. Malzeme: taş OLMAZ (2,3 kg + press darbesinde çatlar), teflon OLMAZ (fırın 350 °C). <b>2 · PENÇE ucu:</b> 2 mafsallı adaptif pençe 0-140 mm (Robotiq 2F-140 sınıfı; paralel · sarma · iç), gıda silikonu soft parmak (mGrip / DoughGripper sınıfı) — hamur topu (çukur hendeğinden), kutu, kutu kola (Ø6,6), 1 L şişe (Ø9), tatlı paketi, <b>kaset kulbu</b> (tepsi kulbuyla aynı profil). Bilekte kamera. <b>Kalkanlar:</b> kürek yüzü, bilek çevirme, TOPPING tablası + kızak + 2 motor, PACK iticisi, pideye doğrudan temas. Vakum YOK.</td></tr>" + t[j:]
rep(TB2 + "dondurucu→buzdolabı top aktarımı (min-max kuralı, gün içi boş anlarda) · tepsiden top→pres · taban→dozaj tablası · tabla→fırın · fırından al→sprey altından geçir→kesime bırak · kapalı kutu→göz · içecek→aynı göz.</td>",
    TB2 + "<b>Pençe ucuyla:</b> dondurucu→buzdolabı top aktarımı (min-max, boş anlarda) · çukurlu tepsiden top→press'teki tepsiye · <b>uç değiştir</b> → <b>Tepsi ucuyla:</b> press'ten al → TOPPING çıkışları altında gezdir → fırına koy (kilit aç) … pişince kilitle, al → sprey altından geçir → kesim yuvası → kutuya eğ → boş tepsiyi kirli rafa · <b>uç değiştir</b> → <b>Pençeyle:</b> kapalı kutu→göz · içecek→aynı göz · kaset takası (geçiş rafı ↔ üst hazne, STORE buzluğu → çözülme yuvası).</td>")
rep("Model M'de kişi pik saatte kürekle manuel devralabilir.", "Model M'de kişi pik saatte tepsiyle manuel devralabilir.")
rep(ON + "Kol arızası: yedek kombine el uç istasyonunda (robot kendisi takar); mekanik arızada makine \"servis dışı\" — entegratör servis sözleşmesi (SLA) şart.</li>",
    ON + "Kol arızası: yedek pençe + yedek tepsiler uç yuvasında (robot kendisi takar); mekanik arızada makine \"servis dışı\" — entegratör servis sözleşmesi (SLA) şart.</li>" +
    OK + "Pideye doğrudan temas / hijyen ve hizalama: pide press'ten kutuya kadar TEPSİDE, robot yalnız kulbu kilitler (Kemal tepsi konsepti, 4 Eyl).</li>" +
    OK + "Kürek + pençe kombine el, bilek çevirme: kalktı — uç değiştirici + tepsi ucu + pençe ucu.</li>" +
    ON + "Sıcak tepsi (fırından 350 °C, kutuya kadar ~150 °C): kilit metal-metal, pençe sıcak tepsiye hiç dokunmaz; uç yuvasında sıcak tepsi rafı ısıya dayanıklı.</li>" +
    AC + "Tepsi havuzu ve yıkama: hatta 4-5 tepsi, toplam 8-10; günde ~80 yıkama (bulaşık 60×60, eleman 3-4 sepet); kirli/temiz tepsi rafı yeri — Kemal ile ayrıca konuşulacak.</li>" +
    AC + "Kol doluluğu ~%85 (103 sn/pide): dozaj gezdirme süresi ve uç değişimi pilotta zaman etüdüyle doğrulanacak; 35/saat üstünde ikinci uç yuvası / hızlı dozaj gerekir.</li>")

# kalan acik isler
rep("robot istasyonu (uç istasyonunun kesin yeri + kaset takası için kobot yük sınıfı) · yerleşim planı (istasyonlar bitince).",
    "robot istasyonu (uç yuvası yeri, tepsi rafı, kobot yük sınıfı) · tepsi havuzu / yıkama döngüsü · Fersah'a Ø29 plaka sorusu · yerleşim planı (istasyonlar bitince).")

io.open(P, 'w', encoding='utf-8', newline='\n').write(t)
print('site ok · v8 img:', t.count('ist3_topping_detay_v8.png'), '· tepsi img:', t.count('robot_tepsi_el_v1.png'), '· kutu:', t.count('PROBLEM DEFTERİ'))

# ================= PROBLEMLER.md dosyalari =================
A = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
def add_rows(path, rows, replaces=()):
    m = io.open(path, encoding='utf-8').read()
    for o, n in replaces:
        assert m.count(o) == 1, (path, o[:50]); m = m.replace(o, n)
    lines = m.split('\n')
    last = max(k for k, L in enumerate(lines) if L.startswith('|'))
    lines[last+1:last+1] = rows
    io.open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print('md ok:', path.split('\\')[-2])
add_rows(A + r"\3_TOPPING\PROBLEMLER.md",
    ["| T15 | Döner-kayar tabla + kızak + 2 motor | ÇÖZÜLDÜ (v8) | Kemal tepsi konsepti: robot pideyi TEPSİ ucuyla çıkışların altında gezdirir; tabla ve sürücüleri kalktı; dozaj boşluğu açık, soğutulmaz |",
     "| T16 | Tepsi yan duvara çarpar (Blender, sağ uç) | ÇÖZÜLDÜ (v8) | Tepsi merkezi x 20-52, y ≥17, ön açık → çıkışlar içe çekildi (20·40·47·52), koni 3-8 cm içe taşır |"],
    [("| T13 | Farklı boy kasetlerde çıkışlar pideye simetrik gelmiyor | ÇÖZÜLDÜ (v7) | 4 çıkış tabla kayma ekseni üzerinde (±3 cm, x 30·39·45,5·53,5); tabla Ø36 kayar+döner → merkezden kenara spiral |",
      "| T13 | Farklı boy kasetlerde çıkışlar pideye simetrik gelmiyor | ÇÖZÜLDÜ (v8) | v7: eksen kuralı; v8: tabla kalktı, robot gezdirir → çıkış konumu serbest (bkz. T16) |")])
add_rows(A + r"\4_OVEN\PROBLEMLER.md",
    ["| F-T1 | Kürekle taşa sürme / pişmiş pideyi alma | ÇÖZÜLDÜ (4 Eyl) | Pide TEPSİYLE fırına girer (delikli alüminyum, pizza screen); robot kilit açar/kapar, sıyırma yok |",
     "| F-T2 | Delikli tepside alt kabuk taş kadar çıtır mı | ÖNERİ VAR | Pilotta taş-tepsi karşılaştırması; gerekirse delik oranı artar |",
     "| F-T3 | Tepsi malzemesi ısı döngüsü (350 °C fırın + 150 °C press + yıkama) | AÇIK | Seramik kaplama + 3 mm alüminyum; pilot 200 tur |"])
add_rows(A + r"\5_PACK\PROBLEMLER.md",
    ["| P-T1 | İtici dilimleri dağıtır | ÇÖZÜLDÜ (4 Eyl) | İtici kalktı: robot tepsiyi eğer, pide 13 cm açık ön ağızdan kutuya kayar; kesim izli, bütün iner |",
     "| P-T2 | Bıçak kuvveti robota gelir | ÇÖZÜLDÜ (4 Eyl) | Tepsi kesim yuvasına oturur (uç takılı), kuvvet yuvaya; 'iz yeter' → kuvvet düşük |",
     "| P-T3 | Bıçak yıldızı tepsi bordürüne sığmalı | ÖNERİ VAR | Cancan yıldızı Ø30'a göre; kesim yuvası pimleri hizalar |"])
add_rows(A + r"\FULL_MAKINE\PROBLEMLER.md",
    ["| R-T1 | Pideye doğrudan temas / hizalama | ÇÖZÜLDÜ (4 Eyl, Kemal) | Pide press'ten kutuya kadar TEPSİDE; robot tepsi ucu (kilitli) + pençe ucu, uç değiştirici |",
     "| R-T2 | Sıcak tepsi ile uç | ÖNERİ VAR | Metal-metal kilit; silikon pençe sıcak tepsiye dokunmaz |",
     "| R-T3 | Tepsi havuzu / yıkama (8-10 tepsi, ~80/gün) | AÇIK | Kemal ile ayrıca |",
     "| R-T4 | Kol doluluğu ~%85 (103 sn/pide) | AÇIK | Pilot zaman etüdü |"])
