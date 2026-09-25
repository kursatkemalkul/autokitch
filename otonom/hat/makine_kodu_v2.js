// ══════════════════════════════════════════════════════════════════════════════════════════════
//  AUTOKITCH · TOPPING v2 (UNO'lu) — MAKİNE KONTROL YAZILIMI v2
//  Makineyi yöneten koddur: simülasyonda da gerçek makinede de aynı satırlar çalışır; tek fark en alttaki
//  SÜRÜCÜ KATI'nın nereye yazdığıdır (3B sahne ↔ step sürücüler + valf adası).
//  Sayılar sim_makine_v7.json'dan okunur; o dosya topping_v2_hesap_v1 (dozaj hesabı) + topping_uno_cad_v5 (model)
//  + topping_cad_v22 (tabla) üreteçlerinden yazılır. Burada tek bir sayı elle yazılmaz.
//
//  ÜÇ DOZAJ TİPİ
//    YAYICI (sos, harç)       UNO + yarıklı boru: tabla merkezi borunun iç ucunda, x'te durur, TAM 1 TUR döner,
//                             piston strokunu o turda bitirir. Yarık kama: debi yarıçapla orantılı → düzgün katman.
//    NOKTA  (kıyma, kuşbaşı)  UNO + yuvarlak ağız: tabla 35 dev/dk, araba x'te kayar → ağız pide üstünde spiral çizer.
//    KASET  (kaşar, sucuk)    bizim kaset: helezon sabit devirde, spiral yasası NOKTA ile aynı.
// ══════════════════════════════════════════════════════════════════════════════════════════════

export const EKSEN = { X: 0, TABLA: 0 };          // X mm (modül yereli) · TABLA derece (SÜREKLİ: tur sayılır)
export const MOTOR = {};                           // dönen miller: {ad: {rpm, aci}}
export const PISTON = {};                          // UNO pistonu: {kod: mm} 0 = ileri (silindir boş), strok = emiş sonu
export const VALF = {};                            // UNO döner valfi: {kod: 0..1} 0 = hazneye (emiş), 1 = ağıza (basma)
export const KESME = {};                           // yayıcının havalı kesme valfi: {kod: true = açık}
export let MAKINE = null;                          // sim_makine_v7.json
export let DOZ = null;                             // o an dozlayan istasyon: {kod, tip, g, ml, t0, T, h}
let IZ = () => {};
let DUR = false;

export function kur(makine, izle) {
  MAKINE = makine; IZ = izle || (() => {});
  EKSEN.X = makine.tabla.baslangic_x;
  for (const i of makine.istasyon) if (i.grup_piston) { PISTON[i.kod] = 0; VALF[i.kod] = 0; KESME[i.kod] = false; }
}
export function durdur() { DUR = true; }
const IST = kod => MAKINE.istasyon.find(i => i.kod === kod);
const HS = () => MAKINE.hesap;

// ──────────────────────────────────────────────────────────────────────────────────────────────
//  1 · SÜRÜCÜ KATI — her satır bir donanım hareketidir
// ──────────────────────────────────────────────────────────────────────────────────────────────

/*@eksenGit*/
export async function eksenGit(hedefX, mod) {
  // X ARABASI: GT3 kasnak turda 60 mm götürür, sürücü 1/16 adımda 3200 adım/tur → 0,01875 mm/adım.
  const X = MAKINE.x, hiz = MAKINE.tabla.x_gecis_hiz;
  const adim = Math.round(Math.abs(hedefX - EKSEN.X) / X.cozunurluk_mm);
  IZ({ satir: 'eksenGit', mesaj: `X ← ${hedefX.toFixed(1)} mm  (${mod} · ${hiz} mm/s · ${adim} adım)`, motor: 'X' });
  MOTOR.X = { rpm: (hiz / X.mm_tur) * 60 };
  await rampali(EKSEN.X, hedefX, hiz, v => { EKSEN.X = v; });
  delete MOTOR.X;
}

/*@motorAc*/
export function motorAc(ad, rpm) {
  // Sürekli dönen mil (tabla, kaset helezonu / karıştırıcısı). Sürücüye hız modunda komut gider.
  MOTOR[ad] = { rpm, aci: MOTOR[ad] ? MOTOR[ad].aci : 0 };
  IZ({ satir: 'motorAc', mesaj: `${ad} AÇIK · ${rpm.toFixed(1)} dev/dk`, motor: ad });
}

/*@motorKapat*/
export function motorKapat(ad) {
  delete MOTOR[ad];
  IZ({ satir: 'motorKapat', mesaj: `${ad} kapalı`, motor: ad });
}

/*@tablaRampa*/
export async function tablaRampa(rpm0, rpm1, sn) {
  // Tabla motoru (pancake NEMA23) S-rampayla hızlanır/yavaşlar. Rampada yayıcının kesme valfi KAPALI: ürün akmaz.
  if (!MOTOR.TABLA) MOTOR.TABLA = { rpm: rpm0, aci: 0 };
  const t0 = performance.now();
  await kare(() => { const u = Math.min(1, (performance.now() - t0) / 1000 / sn); MOTOR.TABLA.rpm = rpm0 + (rpm1 - rpm0) * u; return u >= 1; });
  if (rpm1 === 0) delete MOTOR.TABLA;
}

/*@valfCevir*/
export async function valfCevir(kod, konum) {
  // UNO döner valfi: 0 = hazneye (emiş), 1 = ağıza (basma). Pnömatik döner eyleyici, 90°.
  IZ({ satir: 'valfCevir', mesaj: `VALF ${kod} → ${konum ? 'AĞIZA (basma)' : 'HAZNEYE (emiş)'}`, motor: 'VALF_' + kod });
  const a = VALF[kod], t0 = performance.now(), T = HS().valf_sn;
  await kare(() => { const u = Math.min(1, (performance.now() - t0) / 1000 / T); VALF[kod] = a + (konum - a) * u; return u >= 1; });
}

/*@pistonGit*/
export async function pistonGit(kod, hedef, sn) {
  // UNO'nun hava silindiri (Ø32) ürün pistonunu sabit hızla sürer — hız valf adasındaki kısıcıyla ayarlanır.
  const a = PISTON[kod], t0 = performance.now();
  await kare(() => { const u = Math.min(1, (performance.now() - t0) / 1000 / sn); PISTON[kod] = a + (hedef - a) * u; return u >= 1; });
}

// ──────────────────────────────────────────────────────────────────────────────────────────────
//  2 · HESAP — topping_v2_hesap_v1.py ile AYNI formüller (karışıkta her doz için yeniden hesaplanır)
// ──────────────────────────────────────────────────────────────────────────────────────────────

/*@unoHesap*/
export function unoHesap(i, g) {
  const A = Math.PI / 4 * i.sil * i.sil, ml = g / HS().yog[i.kod], strok = ml * 1000 / A;
  return { ml, strok, strok_orani: strok / i.strok_max };
}

/*@yayiciHesap*/
export function yayiciHesap(i, g) {
  // dozaj = 1 TAM TUR. Tabla 30 dev/dk → 2,0 s. Piston bu sürede strokunu bitirir. Katman = hacim / kaplanan alan.
  const u = unoHesap(i, g), T = 60 / HS().rpm_yayici;
  return { ...u, sure: T, tur: 1, aci: 360, debi: u.ml / T, piston_hiz: u.strok / T, katman: u.ml * 1000 / HS().a_kap };
}

/*@spiralHesap*/
export function spiralHesap(i, g) {
  // Spiral: tabla 35 dev/dk (üstteki ürün kaymasın: r 125'te 0,17 g), ağızın pide merkezine uzaklığı r,
  // r² zamanla doğrusal azalır (eşit alan hızı → düzgün katman). Şerit = ağız iç çapı × 0,8.
  const H = HS(), b = H.serit * i.ic, r_dis = H.r_kap - b / 2, r_ic = H.r_ic;
  let T, N, ml, ek = {};
  if (i.tip === 'NOKTA') { N = H.tur_uno; T = N / H.rpm_nokta * 60; const u = unoHesap(i, g); ml = u.ml; ek = { ...u, piston_hiz: u.strok / T }; }
  else { T = g / (i.g_tur * i.rpm / 60); N = T * H.rpm_nokta / 60; ml = g / H.yog[i.kod]; ek = { helezon_rpm: i.rpm, helezon_tur: i.rpm * T / 60 }; }
  const C = (r_dis * r_dis - r_ic * r_ic) / (2 * N);
  return { ...ek, ml, sure: T, tur: N, aci: N * 360, r_dis, r_ic, serit: b, hatve_dis: C / r_dis, hatve_ic: C / r_ic, seyrek_r: C / b,
           debi: ml / T, katman: ml * 1000 / H.a_kap };
}

/*@rYasa*/
export function rYasa(d, t) {
  const u = Math.min(1, Math.max(0, t / d.sure));
  return Math.sqrt(d.r_dis * d.r_dis + (d.r_ic * d.r_ic - d.r_dis * d.r_dis) * u);
}

/*@tablaX*/
export function tablaX(i, r) {
  // UNO ağzı tabla ekseni hizasında (z −170) → x kaçıklığı = r. Kaset borusu 20 mm önde → √(r² − 20²).
  // TARAF: tabla ağzın solunda (−1) ya da sağında (+1). Kıymada sağ: solda pidenin kenarı harç borusunun (pideden 6 mm) altına giriyor.
  const dz = Math.abs(i.agiz_z - MAKINE.tabla.eksen_z);
  return i.x + i.taraf * Math.sqrt(Math.max(0, r * r - dz * dz));
}

export function hesapla(kod, g) {
  const i = IST(kod);
  return i.tip === 'YAYICI' ? yayiciHesap(i, g) : spiralHesap(i, g);
}

/*@karisik*/
export function karisik(secim) {
  // KARIŞIK (Kemal seçer): seçilen ETLER tek porsiyonu paylaşır (her biri kendi dozunun 1/n'i);
  // kaşar etle 90 g, tek başına 130 g; sos seçilirse 80 g. [V — Kemal'in onayına]
  const K = MAKINE.karisik, d = {};
  const et = Object.keys(K.et).filter(k => secim.includes(k));
  if (secim.includes('SOS')) d.SOS = K.sos;
  for (const k of et) d[k] = Math.round(K.et[k] / et.length * 10) / 10;
  if (secim.includes('KASAR')) d.KASAR = et.length ? K.kasar[1] : K.kasar[0];
  return d;
}

/*@sirala*/
export function sirala(doz) {
  // İstasyonlar SOLDAN SAĞA sıralanır: yüklü pide hiçbir zaman yayıcı borunun (pideden 6 mm) altından geri geçmez.
  return Object.keys(doz).sort((a, b) => IST(a).x - IST(b).x);
}

// ──────────────────────────────────────────────────────────────────────────────────────────────
//  3 · DOZ YORDAMLARI
// ──────────────────────────────────────────────────────────────────────────────────────────────

/*@emis*/
export async function emis(kodlar, doz) {
  // HAZIRLIK: reçetedeki UNO'lar açıcı çalışırken AYNI ANDA emer — valf hazneye, piston doz strokunca geri.
  IZ({ satir: 'emis', mesaj: `UNO'lar emiyor: ${kodlar.join(', ') || '—'}` });
  await Promise.all(kodlar.map(async k => {
    await valfCevir(k, 0);
    await pistonGit(k, unoHesap(IST(k), doz[k]).strok, 0.8);
  }));
}

/*@yayiciDoz*/
export async function yayiciDoz(kod, g) {
  const i = IST(kod), h = yayiciHesap(i, g), H = HS();
  IZ({ satir: 'yayiciDoz', mesaj: `▶ ${i.ad}: ${g} g = ${h.ml.toFixed(1)} ml · piston ${h.strok.toFixed(1)} mm · tabla 1 tur (${h.sure.toFixed(1)} s)`, kod, faz: 'basla' });
  await eksenGit(i.x, 'yayıcının altına: tabla merkezi borunun iç ucunda');
  await valfCevir(kod, 1);
  await tablaRampa(0, H.rpm_yayici, H.rampa_sn);                      // hızlanma — kesme valfi kapalı
  const a0 = EKSEN.TABLA;
  KESME[kod] = true;
  DOZ = { kod, tip: 'YAYICI', g, ml: h.ml, h, t0: performance.now(), T: h.sure, a0, strok: h.strok };
  IZ({ satir: 'yayiciDoz', mesaj: `kesme valfi AÇIK · piston ${h.piston_hiz.toFixed(1)} mm/s · debi ${h.debi.toFixed(1)} ml/s`, kod, faz: 'doz' });
  const bas = pistonGit(kod, 0, h.sure);
  await kare(() => EKSEN.TABLA - a0 >= 360);                          // TAM 1 TUR
  KESME[kod] = false;
  await bas;
  IZ({ satir: 'yayiciDoz', mesaj: `kesme valfi KAPALI · tabla ${(EKSEN.TABLA - a0).toFixed(0)}° döndü · katman ${h.katman.toFixed(2)} mm` });
  await tablaRampa(H.rpm_yayici, 0, H.rampa_sn);
  DOZ = null;
  IZ({ satir: 'yayiciDoz', mesaj: `✔ ${i.ad} tamam · ${g} g`, faz: 'bitti' });
}

/*@spiralDoz*/
export async function spiralDoz(kod, g) {
  const i = IST(kod), d = spiralHesap(i, g), H = HS();
  IZ({ satir: 'spiralDoz', mesaj: `▶ ${i.ad}: ${g} g · ${d.tur.toFixed(2)} tur spiral (${d.sure.toFixed(1)} s) · r ${d.r_dis.toFixed(0)} → ${d.r_ic}`, kod, faz: 'basla' });
  await eksenGit(tablaX(i, d.r_dis), 'dozaj başlangıcı: ağız pidenin dış şeridinde');
  if (i.tip === 'NOKTA') await valfCevir(kod, 1);
  await tablaRampa(0, H.rpm_nokta, H.rampa_sn);
  if (i.tip === 'KASET') { motorAc('HELEZON_' + kod, i.rpm); motorAc('KARISTIRICI_' + kod, 4); }
  DOZ = { kod, tip: i.tip, g, ml: d.ml, h: d, t0: performance.now(), T: d.sure, a0: EKSEN.TABLA, strok: d.strok };
  IZ({ satir: 'spiralDoz', mesaj: i.tip === 'NOKTA' ? `piston ${d.piston_hiz.toFixed(2)} mm/s (yavaş basma) · şerit ${d.serit.toFixed(0)} mm` : `helezon ${i.rpm} dev/dk · ${d.helezon_tur.toFixed(1)} tur`, kod, faz: 'doz' });
  const bas = i.tip === 'NOKTA' ? pistonGit(kod, 0, d.sure) : Promise.resolve();
  const t0 = performance.now();
  await kare(() => { const t = (performance.now() - t0) / 1000; EKSEN.X = tablaX(i, rYasa(d, t)); return t >= d.sure; });
  await bas;
  if (i.tip === 'KASET') {
    motorKapat('KARISTIRICI_' + kod);
    MOTOR['HELEZON_' + kod].rpm = -i.rpm; await bekle(15 / i.rpm);      // ¼ tur GERİ: boru ağzı damlamasın
    motorKapat('HELEZON_' + kod);
  } else await valfCevir(kod, 0);
  await tablaRampa(H.rpm_nokta, 0, H.rampa_sn);
  DOZ = null;
  IZ({ satir: 'spiralDoz', mesaj: `✔ ${i.ad} tamam · ${g} g · katman ${d.katman.toFixed(2)} mm`, faz: 'bitti' });
}

export async function dozla(kod, g) {
  return IST(kod).tip === 'YAYICI' ? yayiciDoz(kod, g) : spiralDoz(kod, g);
}

// ──────────────────────────────────────────────────────────────────────────────────────────────
//  4 · ÜRÜN
// ──────────────────────────────────────────────────────────────────────────────────────────────

/*@ac*/
// AÇICI — konili döner kafa hamuru YUVARLAYARAK Ø280'e açar (40–160 N). Açma anında tabla kilitli.
export async function ac() {
  const A = MAKINE.acici;
  await eksenGit(MAKINE.tabla.acici_x, 'açıcının altı');
  IZ({ satir: 'ac', mesaj: 'tabla kilitlendi · açıcı iniyor', faz: 'acma' });
  await bekle(A.in_sn);
  motorAc('ACICI', 60);
  IZ({ satir: 'ac', mesaj: `koniler dönüyor — hamur açılıyor (${A.ac_sn} s)`, acildi: true });
  await bekle(A.ac_sn);
  motorKapat('ACICI');
  IZ({ satir: 'ac', mesaj: 'hamur açıldı Ø280 · kafa kalkıyor' });
  await bekle(A.kalk_sn);
}

/*@aktar*/
export async function aktar() {
  IZ({ satir: 'aktar', mesaj: 'ürün fırın bandına aktarılıyor', faz: 'aktar' });
  await eksenGit(MAKINE.tabla.aktarma_x, 'banda aktarma');
  IZ({ satir: 'aktar', mesaj: 'ürün banda geçti — tabla boş', aktarildi: true });
  await bekle(0.5);
  IZ({ satir: 'aktar', mesaj: 'tabla açıcının altına dönüyor — park' });
  await eksenGit(MAKINE.tabla.acici_x, 'park');
}

/*@urunYap*/
export async function urunYap(doz) {
  DUR = false;
  const sira = sirala(doz), t0 = performance.now();
  IZ({ satir: 'urunYap', mesaj: `═ ÜRETİM — ${sira.map(k => k + ' ' + doz[k] + ' g').join(' · ')}`, faz: 'basla', yeniTepsi: true });
  const uno = sira.filter(k => IST(k).grup_piston);
  await eksenGit(MAKINE.x.home_x, 'HOME');
  await Promise.all([ac(), emis(uno, doz)]);                         // açıcı açarken UNO'lar emer
  for (const k of sira) { if (DUR) break; await dozla(k, doz[k]); }
  if (!DUR) await aktar();
  const sn = (performance.now() - t0) / 1000;
  IZ({ satir: 'urunYap', mesaj: `═ BİTTİ — ${sn.toFixed(1)} s · saatte ${Math.round(3600 / sn)} ürün`, faz: 'bitti', sure: sn });
  return sn;
}

// ──────────────────────────────────────────────────────────────────────────────────────────────
//  5 · YARDIMCILAR
// ──────────────────────────────────────────────────────────────────────────────────────────────
function kare(bitti) {
  return new Promise(res => { const a = () => { if (DUR || bitti()) return res(); requestAnimationFrame(a); }; a(); });
}

function rampali(bas, son, hiz, yaz) {
  // Gerçek sürücüde S-eğrisi rampa; burada 0,15 s hızlanma/yavaşlama ile aynı süre.
  const yol = son - bas, sure = Math.abs(yol) / hiz + MAKINE.tabla.rampa_x, t0 = performance.now();
  return kare(() => { const u = Math.min(1, (performance.now() - t0) / 1000 / sure); yaz(bas + yol * (u < 0.5 ? 2 * u * u : 1 - 2 * (1 - u) * (1 - u))); return u >= 1; });
}

export function bekle(sn) { return new Promise(r => setTimeout(r, sn * 1000)); }

// Her karede: dönen motorların açısını ilerletir (sahne okur). TABLA açısı sürekli toplanır (tur sayılır).
export function kareIsle(dt) {
  for (const ad in MOTOR) { const m = MOTOR[ad]; if (m.aci !== undefined) m.aci = m.aci + m.rpm * 6 * dt; }
  if (MOTOR.TABLA) EKSEN.TABLA += MOTOR.TABLA.rpm * 6 * dt;
}
