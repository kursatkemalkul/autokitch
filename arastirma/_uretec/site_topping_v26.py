# -*- coding: utf-8 -*-
# Site: TOPPING bolumu -> v26 (Picnic tipi kap) + v25 (catal/kizak/L raf) + 4 Picnic referans karesi (modelleme); HAT gorseli v45 -> v46
import io, os, shutil
ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
for src, dst in (("arastirma/3_TOPPING/ist3_topping_detay_v26.png", "otonom/img/ist3_topping_detay_v26.png"),
                 ("arastirma/3_TOPPING/ist3_topping_detay_v25.png", "otonom/img/ist3_topping_detay_v25.png"),
                 ("arastirma/FULL_MAKINE/hat_on_gorunus_teknik_v46.png", "otonom/img/hat_on_gorunus_teknik_v46.png")):
    shutil.copyfile(os.path.join(ROOT, src), os.path.join(ROOT, dst))
p = os.path.join(ROOT, 'otonom', 'index.html')
t = io.open(p, encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)
Q = chr(39)
rep('İSTASYON 3 · TOPPING — MALZEME DOZAJI — ✔ KARAR v24 (5 Eyl 2026): TEK KAP TİPİ · 3 KAT</div>',
    'İSTASYON 3 · TOPPING — MALZEME DOZAJI — ✔ KARAR v26 (5 Eyl 2026): PICNIC TİPİ KAP · ÇATALLA TAŞIMA · 3 KAT</div>')
IMG = 'style="width:100%;max-width:1100px;display:block;margin:6px auto 12px;border:1px solid #d7e8dc;border-radius:12px" loading="lazy"'
FIG = 'style="width:100%;border:1px solid #d7e8dc;border-radius:12px" loading="lazy"'
CAP = 'style="font-size:12px;color:#68758a;margin-top:5px"'
new = (
 '<div style="margin:6px 0 10px;padding:10px 14px;background:#eef7f1;border:1px solid #cfe5d6;border-radius:10px;font-size:13.5px;line-height:1.6;color:#22304a">'
 '<b style="color:#1d7a4f">GÜNCEL KARAR — 5 Eyl 2026 (v26): KAP = PICNIC TİPİ.</b> Kemal' + Q + 'in kararı: Picnic' + Q + 'in kaşar haznesi gibi kuruluyor — '
 '<b>dairesel duvar</b> (R 6,5; köprü kırıcı tarağın süpürmesiyle eş merkezli, ölü köşe yok), altta <b>plastik milli helezon</b> (POM, Ø70, hatve 50, boy 60, arka uçta tırtıllı topuz → duvardaki yaylı sokete), '
 'üstte <b>omurgalı çubuk tarak</b> (4 çubuk Ø6 boydan boya, göbek z 14, arka + ön omurga), <b>şeffaf polikarbonat gövde</b> (seviye görünür). '
 'Ölçüler bizim istasyona uyarlı: kap dışı <b>14×68</b>, kızakla 26 → kat 27; hacim brüt 16,3 L / kullanılabilir 14,0 L → kaşar 5,8 kg (1,3 gün; iki pozisyon 2,6), kıyma 8,4 kg (2,9 gün), sucuk 7,7 kg (6,4 gün), kuşbaşı 4,3 kg (3 gün). Robot haftada ≈ 12 kap değişimi. '
 '<b>v25 (aynı gün): kap taşıma tek çözüm</b> — kabın altında 2 içi boş kızak (çatal cebi), kabinde 2 L raf, robot ucu ÇATAL (forklift: gir 50 → kaldır 0,5 → çek 70); kap arkaya dayalı (ara mil yok); ALT beşik yerine aynı L raflar, soğutma grubu ALT dibinde; STORE −18 sol modül klapeli kaset katı (4 kap, çekmece yok) — STORE v5 önerisi onay bekliyor. '
 '<span style="color:#9a6b1f">Açık: kol yükü 15,4 kg → 16–20 kg kobot + menzil ≥ 130 · ağız altına Picnic yayıcı plakası mı, spiral süpürme mi · kap başına 2 motor mu tek motor + kayış mı · gramaj prototipi.</span></div>'
 '<img src="img/ist3_topping_detay_v26.png" alt="TOPPING kap v26 — Picnic tipi: dairesel duvar, plastik helezon, çubuk tarak, şeffaf PC" ' + IMG + '>'
 '<div style="font-size:12.5px;color:#22304a;margin:4px 0 6px"><b style="color:#1d7a4f">Modelleme referansı — Picnic Works kareleri (Kemal, 5 Eyl):</b> kabı modellerken bakılacak dört kare.</div>'
 '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin:4px auto 14px;max-width:1100px">'
 '<figure style="margin:0"><img src="img/picnic_kap_helezon.webp" alt="Picnic topping kabı altından: boydan boya beyaz plastik helezon ve uçta kavrama topuzu" ' + FIG + '><figcaption ' + CAP + '>Kabın altı: yalakta boydan boya <b>beyaz plastik milli helezon</b>, uçta elle takılan tırtıllı kavrama topuzu — bizde POM Ø70, hatve 50, topuz Ø50 → yaylı soket.</figcaption></figure>'
 '<figure style="margin:0"><img src="img/picnic_kap_tarak.webp" alt="Picnic kaşar haznesi: şarap kadehi şekli, ortada tarak göbeği, altta helezon gövdesi" ' + FIG + '><figcaption ' + CAP + '>Kaşar haznesi: <b>şarap kadehi</b> kesit — göbeğin etrafında daire duvar, üstte geniş dik depo, altta boğaz ve helezon gövdesi; ağız ön uçta, altta mavi yayıcı plaka.</figcaption></figure>'
 '<figure style="margin:0"><img src="img/picnic_tarak_detay.png" alt="Picnic köprü kırıcı tarak: göbek, omurga ve omurgaya dik ince çubuklar" ' + FIG + '><figcaption ' + CAP + '>Köprü kırıcı: <b>göbek + omurga + omurgaya dik ince çubuklar</b>, arka duvardan tahrik — bizde 4 çubuk Ø6 × 630, r 57/43/29/14 mm, göbek z 14, 10–20 dev/dk.</figcaption></figure>'
 '<figure style="margin:0"><img src="img/picnic_reload_pepp.png" alt="Picnic ekranı: pepperoni şarjörü değiştirme adımları" ' + FIG + '><figcaption ' + CAP + '>Pepperoni şarjörü değiştirme ekranı: malzeme kendi karton kutusuyla eğik şarjöre takılıyor — bizde dilim/kesme yok (sucuk KÜP gelir), ama <b>eleman ekranı adım adım</b> fikri alınacak.</figcaption></figure>'
 '</div>'
 '<div style="font-size:12.5px;color:#22304a;margin:4px 0 6px"><b style="color:#1d7a4f">v25 — kap taşıma (çatal + kızak + L raf), aynı gün:</b></div>'
 '<img src="img/ist3_topping_detay_v25.png" alt="TOPPING v25 — kap taşıma tek çözüm: çatal, cepli kızak, L raf, STORE −18 kaset katı" ' + IMG + '>'
 '<div style="font-size:12px;color:#9a6b1f;margin:10px 0 4px"><b>Önceki tur (v24, aynı gün) — istasyon yerleşimi geçerli:</b> 3 kat × 2 kap, kat 1 kaşar A + sucuk, kat 2 kaşar B + boş, kat 3 kıyma + kuşbaşı, tepsi düzlemleri 158/117/76. Aşağıdaki v24 metnindeki kap ölçüsü (16×54), beşikler ve STORE çekmecesi v25–v26 ile değişti.</div>'
)
old_img = '<img src="img/ist3_topping_detay_v24.png" alt="TOPPING istasyonu v24 — tek kap tipi, 3 kat, üst görünüm" ' + IMG + '>'
assert t.count(old_img) == 1
# v24 karar kutusunu 'önceki tur' yap, yeni bloğu üstüne koy
old_box_start = '<div style="margin:6px 0 10px;padding:10px 14px;background:#eef7f1;border:1px solid #cfe5d6;border-radius:10px;font-size:13.5px;line-height:1.6;color:#22304a"><b style="color:#1d7a4f">GÜNCEL KARAR — 5 Eyl 2026 (v24):</b>'
rep(old_box_start, new + '<div style="margin:6px 0 10px;padding:10px 14px;background:#fbf7ef;border:1px solid #e7dcc3;border-radius:10px;font-size:13px;line-height:1.6;color:#4a4a4a"><b style="color:#9a6b1f">v24 metni (yerleşim):</b>')
rep('Görev: basılmış tabana malzeme dozajı — güncel karar aşağıdaki yeşil kutuda (v24).', 'Görev: basılmış tabana malzeme dozajı — güncel karar aşağıdaki yeşil kutuda (v26 kap + v25 taşıma).')
# HAT v45 -> v46
rep('<img src="img/hat_on_gorunus_teknik_v45.png" alt="Hat genel görünüm v45 — tüm istasyonlar son versiyon"', '<img src="img/hat_on_gorunus_teknik_v46.png" alt="Hat genel görünüm v46 — tüm istasyonlar son versiyon"')
i0 = t.index('HAT v45 (5 Eyl 2026) — STORE v4'); i1 = t.index('</div>', i0)
t = t[:i0] + 'HAT v46 (5 Eyl 2026) — STORE v4 (+ v5 öneri: −18 klapeli kaset katı) · PRESS v8 (Ø32, çatal yuvası) · TOPPING v25 yerleşimi (kap 14×68, L raf, çatal, soğutma dipte) · OVEN tank+pompa (② 44) · PACK 116 · robot 16–20 kg, menzil ≥ 130 · KONTROL 13 madde (② ⑤ ⑦ ⑩ ⑫ açık). Kap iç şekli v26 ile değişti, dış ölçü aynı.' + t[i1:]
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('index.html guncellendi')
