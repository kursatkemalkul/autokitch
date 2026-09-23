// ══════════════════════════════════════════════════════════════════════════════════════════════
//  AUTOKITCH · TOPPING MODÜLÜ — MAKİNE KONTROL YAZILIMI
//  Bu dosya makineyi GERÇEKTEN yöneten koddur. Simülasyonda da, gerçek makinede de aynı satırlar
//  çalışır; tek fark en alttaki SÜRÜCÜ KATI'nın nereye yazdığıdır:
//     · simülasyonda  → 3B sahnedeki eksen değerlerine
//     · makinede      → Modbus/EtherCAT üzerinden step sürücü kartlarına
//  Ölçüler ve devirler sim_makine.json'dan okunur; o dosya CAD'den (topping_cad_v10) türetilir.
//  Yani burada tek bir sayı elle yazılmaz — makine değişirse kod kendiliğinden ona uyar.
// ══════════════════════════════════════════════════════════════════════════════════════════════

export const EKSEN = { X: 0, TABLA: 0 };          // canlı eksen değerleri (X mm · TABLA derece)
export const MOTOR = {};                           // çalışan motorlar: {ad: {rpm, baslangic}}
export let MAKINE = null;                          // sim_makine.json
export let DOZ_YUVA = null;                        // o an dozlayan yuva (yoksa null)
let IZ = () => {};                                 // panel geri çağırması
let DUR = false;

export function kur(makine, izle) {
  MAKINE = makine; IZ = izle || (() => {});
  EKSEN.X = makine.tabla.baslangic_x;           // araba modelde çizildiği yerden başlar
}
export function durdur() { DUR = true; }

// ──────────────────────────────────────────────────────────────────────────────────────────────
//  1 · SÜRÜCÜ KATI — her satır bir donanım hareketidir
// ──────────────────────────────────────────────────────────────────────────────────────────────

/*@eksenGit*/
export async function eksenGit(hedefX, mod) {
  // X ARABASI. Sürücüye verilen şey adım sayısıdır: GT3 kasnak turda 60,00 mm götürür,
  // sürücü 1/16 adımda 3200 adım/tur sayar → 0,01875 mm/adım.
  const X = MAKINE.x, hiz = mod === 'doz' ? MAKINE.tabla.x_doz_hiz : MAKINE.tabla.x_gecis_hiz;
  const yol = Math.abs(hedefX - EKSEN.X), adim = Math.round(yol / X.cozunurluk_mm);
  IZ({ satir: 'eksenGit', mesaj: `X ← ${hedefX.toFixed(1)} mm  (${mod === 'doz' ? 'dozaj' : 'geçiş'} ${hiz} mm/s · ${adim} adım)`, motor: 'X' });
  MOTOR.X = { rpm: (hiz / X.mm_tur) * 60, yon: hedefX > EKSEN.X ? 1 : -1 };
  await rampali(EKSEN.X, hedefX, hiz, v => { EKSEN.X = v; });
  delete MOTOR.X;
}

/*@motorAc*/
export function motorAc(ad, rpm) {
  // Sürekli dönen mil (tabla ya da kasetin helezonu/pompası). Sürücüye hız modunda komut gider.
  MOTOR[ad] = { rpm, aci: MOTOR[ad] ? MOTOR[ad].aci : 0 };
  IZ({ satir: 'motorAc', mesaj: `${ad} motoru AÇIK · ${rpm} dev/dk`, motor: ad });
}

/*@motorKapat*/
export function motorKapat(ad) {
  delete MOTOR[ad];
  IZ({ satir: 'motorKapat', mesaj: `${ad} motoru kapalı`, motor: ad });
}

/*@homeAra*/
export async function homeAra() {
  // Başlangıçta referans arama: araba limit anahtarına kadar gider, sonra home sensörüne oturur.
  IZ({ satir: 'homeAra', mesaj: 'HOME aranıyor — araba limit+ yönünde yürüyor', motor: 'X' });
  await eksenGit(MAKINE.x.home_x, 'gecis');
  EKSEN.TABLA = 0;
  IZ({ satir: 'homeAra', mesaj: `HOME bulundu · X = ${MAKINE.x.home_x} mm (istasyon) · tabla açısı sıfırlandı` });
}

// ──────────────────────────────────────────────────────────────────────────────────────────────
//  2 · TABLA YASASI — ağzın pide merkezine uzaklığı zamanla nasıl değişir
//     Bu eğri kaşar/kuşbaşı akış modellerinden gelir (kasar_akis_model_v2 · YASA), burada
//     uydurulmaz. Dışta bekle → r² doğrusal azalarak içeri → ortada bekle.
// ──────────────────────────────────────────────────────────────────────────────────────────────

/*@rYasa*/
export function rYasa(t) {
  const T = MAKINE.tabla;
  if (t <= T.t_dis) return T.r_dis;
  if (t >= T.doz_sn - T.t_ic) return T.r_ic;
  const tm = T.doz_sn - T.t_dis - T.t_ic, u = (t - T.t_dis) / tm;
  return Math.sqrt(T.r_dis * T.r_dis + (T.r_ic * T.r_ic - T.r_dis * T.r_dis) * u);
}

/*@dxHesap*/
export function dxHesap(r) {
  // Tabla ekseni nozzle'dan z'de 20 mm geride. Ağzın pide merkezine uzaklığı r ise
  // arabanın x'te kaçık olması gereken mesafe √(r² − 20²) olur; r = 20'de tam nozzle altına gelir.
  const dz = Math.abs(MAKINE.tabla.r_ic);
  return Math.sqrt(Math.max(0, r * r - dz * dz));
}

// ──────────────────────────────────────────────────────────────────────────────────────────────
//  3 · BİR DOZ — Kemal'in tarifi: "tepsi kaşarın altına dönüp x'teki hareketini
//     kaşarın döküldüğüne göre ayarlıyor, sonra tamamlıyor"
// ──────────────────────────────────────────────────────────────────────────────────────────────

/*@dozla*/
export async function dozla(yuvaKodu) {
  const y = MAKINE.yuvalar.find(v => v.kod === yuvaKodu);
  const T = MAKINE.tabla;
  IZ({ satir: 'dozla', mesaj: `▶ ${y.urun} dozu başlıyor — ${y.doz_g} g`, urun: y.urun, kod: y.kod, faz: 'basla' });

  // 1) araba dozaj başlangıcına: ağız pidenin DIŞ kenarında olacak
  const x0 = y.x - dxHesap(T.r_dis);
  await eksenGit(x0, 'gecis');

  // 2) tabla dönmeye başlar, kasetin mili dönmeye başlar
  motorAc('TABLA', T.rpm);
  motorAc(y.pompa ? 'POMPA_' + y.kod : 'HELEZON_' + y.kod, y.helezon_rpm);
  // Karıştırıcı POMPALI kasette de döner: harç/sos çöker ve ayrışır, dozdan önce karışması gerekiyor.
  // (Pompalı kasette bu mil ALTTAKİ hazne paletidir, vidalıda ÜSTTEKİ karıştırıcıdır — sim_makine.json
  //  her yuva için grup_doz / grup_karis alanlarıyla hangisinin hangisi olduğunu söylüyor.)
  motorAc('KARISTIRICI_' + y.kod, 4);

  // 3) DOZ: tabla sabit hızda dönerken araba yasaya göre içeri kayar → ağız pide üstünde spiral çizer
  IZ({ satir: 'dozSpiral', mesaj: `dozaj — tabla ${T.rpm} dev/dk, araba ${T.x_doz_hiz} mm/s içeri`, kod: y.kod, faz: 'doz' });
  DOZ_YUVA = y.kod;                                  // sahne ürünü BU yuvadan döksün, en yakından değil
  await spiral(y);

  // 4) mil durur; helezonda çeyrek tur GERİ (damlamayı keser), pompada duckbill kendisi kapatır
  motorKapat(y.pompa ? 'POMPA_' + y.kod : 'HELEZON_' + y.kod);
  motorKapat('KARISTIRICI_' + y.kod);
  if (!y.pompa) { IZ({ satir: 'geriAl', mesaj: 'helezon ¼ tur GERİ — meme damlamasın' }); await bekle(0.35); }
  else IZ({ satir: 'geriAl', mesaj: 'pompa durdu — duckbill valf kendi elastikliğiyle kapandı' });
  motorKapat('TABLA');
  DOZ_YUVA = null;
  IZ({ satir: 'dozla', mesaj: `✔ ${y.urun} tamam · ${y.doz_g} g`, faz: 'bitti' });
}

/*@spiral*/
async function spiral(y) {
  const T = MAKINE.tabla, t0 = performance.now();
  return new Promise(res => {
    const adim = () => {
      if (DUR) return res();
      const t = (performance.now() - t0) / 1000;
      if (t >= T.doz_sn) { EKSEN.X = y.x; return res(); }
      EKSEN.X = y.x - dxHesap(rYasa(t));            // araba yasaya göre içeri
      requestAnimationFrame(adim);
    };
    adim();
  });
}

// ──────────────────────────────────────────────────────────────────────────────────────────────
//  4 · ÜRÜN — reçete sırayla dozlanır
// ──────────────────────────────────────────────────────────────────────────────────────────────

/*@ac*/
// AÇICI — konili döner kafa. Hamuru EZEREK değil YUVARLAYARAK açar; bu yüzden 40-160 N
// yeter (düz pres 3-12 kN isterdi ve o yük tablanın yatağına binerdi).
// Açma anında TABLA KİLİTLENİR: konilerin artık torku 3-5 N·m, tabla motorunun tutma
// torku 0,9 N·m — motor tutamaz, ayar bileziğindeki burca pim girer.
export async function ac() {
  const A = MAKINE.acici;
  await eksenGit(MAKINE.tabla.acici_x, 'gecis');
  IZ({ satir: 'ac', mesaj: 'tabla kilitlendi · açıcı iniyor', faz: 'acma' });
  await bekle(A.in_sn);
  motorAc('ACICI', 60);
  IZ({ satir: 'ac', mesaj: `koniler dönüyor — hamur açılıyor (${A.ac_sn} s)`, acildi: true });
  await bekle(A.ac_sn);
  motorKapat('ACICI');
  IZ({ satir: 'ac', mesaj: 'hamur açıldı Ø280 · kafa kalkıyor, kilit çözüldü' });
  await bekle(A.kalk_sn);
}

/*@aktar*/
// BANDA AKTARMA — tepsi yok, pideyi köprü alır. Araba sağa gider, pidenin ön kenarı
// köprüye çıkar, fırın bandı çeker. Ek motor ve sensör yok.
export async function aktar() {
  IZ({ satir: 'aktar', mesaj: 'pide fırın bandına aktarılıyor', faz: 'aktar' });
  await eksenGit(MAKINE.tabla.aktarma_x, 'gecis');
  IZ({ satir: 'aktar', mesaj: 'pide banda geçti — tabla boş (sensör doğruluyor)', aktarildi: true });
  await bekle(0.5);
}

export const RECETE = {
  kasarli:   { ad: 'Kaşarlı pide',    adim: ['KAŞAR_KABI'] },
  kiymali:   { ad: 'Kıymalı pide',    adim: ['KIYMA'] },
  kusbasili: { ad: 'Kuşbaşılı pide',  adim: ['KUŞBAŞI'] },
  sucuklu:   { ad: 'Sucuklu pide',    adim: ['KAŞAR_KABI', 'KÜP_SUCUK'] },   // kaşar ALTA: eriyip sucuğu tutar
  lahmacun:  { ad: 'Lahmacun',        adim: ['HARÇ_1'] },
  pizza:     { ad: 'Pizza',           adim: ['HARÇ_2', 'KAŞAR_KABI', 'KÜP_SUCUK'] },
};

/*@urunYap*/
export async function urunYap(adimlar) {
  DUR = false;
  const t0 = performance.now();
  IZ({ satir: 'urunYap', mesaj: `═ ÜRETİM BAŞLADI — ${adimlar.length} doz`, faz: 'basla' });

  // v20 · TEPSİ YOK. Robot hamur TOPUNU doğrudan çalışma diskine bırakır; açıcı orada açar.
  IZ({ satir: 'hamurAl', mesaj: 'robot hamur TOPUNU açıcıya bırakıyor (x = ' + MAKINE.tabla.acici_x + ')', yeniTepsi: true });
  await homeAra();
  await bekle(0.4);
  await ac();                                        // konili açıcı hamuru Ø280'e açar

  for (const kod of adimlar) {
    if (DUR) break;
    await dozla(kod);                                // ← her doz için aynı yordam
  }

  await aktar();                                     // pide fırın bandına
  const sn = (performance.now() - t0) / 1000;
  IZ({ satir: 'urunYap', mesaj: `═ BİTTİ — ${sn.toFixed(1)} s · saatte ${Math.round(3600 / sn)} tepsi`, faz: 'bitti', sure: sn });
  return sn;
}

// ──────────────────────────────────────────────────────────────────────────────────────────────
//  5 · YARDIMCILAR
// ──────────────────────────────────────────────────────────────────────────────────────────────

function rampali(bas, son, hiz, yaz) {
  // Gerçek sürücüde S-eğrisi rampa var; burada 0,15 s hızlanma/yavaşlama ile aynı süre çıkar.
  const yol = son - bas, sure = Math.abs(yol) / hiz + 0.3;
  const t0 = performance.now();
  return new Promise(res => {
    const adim = () => {
      if (DUR) return res();
      const u = Math.min(1, (performance.now() - t0) / 1000 / sure);
      yaz(bas + yol * (u < 0.5 ? 2 * u * u : 1 - 2 * (1 - u) * (1 - u)));
      u < 1 ? requestAnimationFrame(adim) : res();
    };
    adim();
  });
}

export function bekle(sn) { return new Promise(r => setTimeout(r, sn * 1000)); }

// Her karede çağrılır: dönen motorların açısını ilerletir (3B sahne bunu okur).
export function kareIsle(dt) {
  for (const ad in MOTOR) {
    const m = MOTOR[ad];
    if (m.aci !== undefined) m.aci = (m.aci + m.rpm * 6 * dt) % 360;   // rpm → derece/s
  }
  if (MOTOR.TABLA) EKSEN.TABLA = MOTOR.TABLA.aci;
}
