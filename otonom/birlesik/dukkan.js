/* İKİZ · DÜKKÂN ÖN BÖLGESİ (cephe, hücre duvarı + kapısı, personel + müşteri bölgesi, tezgâh, evye, kiosk, bekleme TV'si, dış şerit ekran, kaldırım).
   YERLEŞİM 9 Eki — SEÇENEK 3c (YÖNETİCİ; Kemal: "müşteri koltuğu yok, tezgâh arkasına personel taburesi, cephe makineye daha yakın"; 3b'nin YERİNE).
   Makine / robot / QR AYNI (hat3_v11q). Metre, +y yukarı, +z sokak:
     HÜCRE DUVARI z 1,750 (20 mm panel 1,750–1,770; h 2,05) · hücre kapısı x 0,686–1,586 (ana GLB'deki eski DUKKAN26 duvar / kapı gizlenir)
     CEPHE DÜZ iç z 2,883 / dış 2,983 tüm genişlik (QR önü 800)
       personel / kurye kapısı x 0,686–1,586 · tezgâh penceresi x 1,77–3,07 (y 1,00–2,00) · dış şerit pencerenin üstünde z 2,983–3,03
       MÜŞTERİ KAPISI x 4,31–5,21 SÜRGÜLÜ, kanatlar dışta SOLDA toplanır x 3,84–4,31 (ray x 3,81–5,21)
     personel bölgesi x 0,636–3,497 · müşteri bölgesi x 3,597–5,360 (z 2,083–2,883) · ayırıcı x 3,497–3,597, z 1,750 → 2,883
     TEZGÂH x 1,736–3,497 · z 2,433–2,883 (450) · üst y 0,74–0,77 · gövdede x 2,00–2,60 DİZ BOŞLUĞU (yalnız üst tabla)
     EVYE L'nin kolu, ayırıcı boyunca x 2,947–3,497 · z 1,770–2,433, önü −x, havuz ortada
     10 Eki (PAKET_10EKI): TABURE KALKTI (K11) · POS tableti ayakta kullanım eğimi 0,96 rad (model = CSS3D) · sipariş panosu (49" şerit) hücre duvarının personel yüzünde x 1,80–3,03 y 1,66–2,02 z 1,770–1,830, sokağa bakar
     KIOSK (duvar tipi 45 × 104 × 14, 32" portre) ayırıcının müşteri yüzünde x 3,597–3,737 · z 2,25–2,70 · y 0,85–1,89, +x'e bakar
     TV 43" DİKEY sağ duvarda x 5,290–5,360 · y 1,10–2,07 · z 2,20–2,76, −x'e bakar (CSS3D 720 × 1280)
     7" teslim ekranı x 3,612–3,742 · y 1,47–1,57 · z 2,083–2,093 (+z)
   ÜRÜN ÖLÇÜLERİ [katalog]: 32" portre aktif alan 0,398 × 0,708 m · 43" 16:9 aktif 0,941 × 0,529 m (dikey 0,529 × 0,941) · 7" 16:10 aktif 0,154 × 0,086 m · 49" şerit (3840 × 1080) aktif 1,21 × 0,34 m.
   Bu parçalar ANA MODELDE yok (ikiz-v1 = web v28; dükkân ana modele Kemal onayından sonra girer) → burada üretilir, `IKIZ.dukkan` altında listelenir. */
/* A · PERSONEL TARAFI (10 Eki): tezgâh + L kolu gerçek üniteler (üreteç arastirma/_uretec/personel_taraf_v1.py → ../ikiz_personel/) */
/* v2 (YÖNETİCİ (d), 11 Eki): ekipman evyesi Blanco E 7x6x3 + MEIKO (L kolu 830) · el lavabosu Delabie LAVANDO sol duvarda */
import { PERSONEL } from './personel_v2.js';
import { GLTFLoader } from './vendor/GLTFLoader.js';
import { dukkanV4, EKRAN } from './dukkan_v4.js';
export const D = {
  CEPHE_IC: 2.883, CEPHE_DIS: 2.983,              // düz cephe (tüm genişlik; QR önü 800)
  HUCRE_DUVAR: 1.750, HUCRE_PANEL: 0.020, HUCRE_Y: 2.05, HUCRE_KAPI: [0.686, 1.586], HUCRE_KAPI_Y: 2.03,
  QR_YUZ: 2.083, X0: 0.636, X1: 5.36, TAVAN: 2.80,
  KAPI_P: [0.686, 1.586], PENCERE: [1.77, 3.07, 1.00, 2.00], KAPI_M: [4.31, 5.21], KAPI_M_KANAT: [3.84, 4.31], KAPI_M_RAY: [3.81, 5.21], KAPI_Y: 2.10,
  AYIRICI: [3.497, 3.597],
  TEZGAH: [1.736, 3.497, 2.433, 2.883, 0.74, 0.77], DIZ: [2.00, 2.60],
  EVYE: [2.667, 3.497, 1.770, 2.878],             // v2: L kolu 830 (ekipman evyesi + MEIKO) — personel_v2
  EL_LAVABO: [0.636, 0.936, 2.275, 2.725],         // v2: Delabie LAVANDO 121370 sol duvarda (450 × 300 × 135)
  POS_EGIM: 0.96,                                   // IKIZ-ARAYUZ-6 (10 Eki): ayakta kullanım — göz 1,65 / şerit z 2,10 → atan(0,695 / 0,49) = 0,96 rad (ekran yatayla 35°); tablet modeli + CSS3D AYNI dönüşüm
  KIOSK: [3.597, 3.737, 2.25, 2.70, 0.85, 1.89],
  TV: [5.290, 5.360, 1.10, 1.10 + 0.9695, 2.4800 - 0.2789, 2.4800 + 0.2789],   // R24 D2: Samsung QB43C dikey 557,8 × 969,5 (föy); x 5,290 askı + ekran 28,5
  SERIT: [2.415 - 0.46115, 2.415 + 0.46115, 1.84 - 0.14415, 1.84 + 0.14415, 1.770, 1.770 + 0.030 + 0.0435],   // R24 D2: LG 37BH7N-H 922,3 × 288,3 × 43,5 (49" 32:9 yok) · IKIZ-ARAYUZ-5 (10 Eki): hücre duvarının personel yüzünde, sokağa (+z) bakar — pencereden görünür (McD tipi pano)
};

/* Ana GLB'deki eski dükkân (Codex v26, DUKKAN26_*) ön bölge parçaları: yeni yerleşimle çakışır → ikizde gizlenir (ana modele dokunulmaz).
   Desen: hücre ara duvarı + robot alanı kapısı (eski z 2,133), eski ön duvar / dükkân kapısı (z 3,553), eski oturma tezgâhı, masa, sandalye, lavabo takımı, yan duvar çizgileri.
   Ek kural: dünya kutusu yeni cephenin dışını (z > 2,983) aşan HER DUKKAN26 parçası (eski ZEMIN_0 dahil → hücre zemini burada çizilir). Arka duvar kalır. */
export const ESKI_DUKKAN_DESEN = /^DUKKAN26_(ARA_DUVAR|ROBOT_ALANI_GIRIS|ON_DUVAR|DUKKAN_GIRIS|OTURMA_TEZGAHI|MASA_|SANDALYE_|LAVABO_|EL_YIKAMA|BATARYA|SOGUK_SU|SICAK_SU|SU_KESME|SABUNLUK|KAGIT_HAVLULUK|SOL_DUVAR_1_[23]|SAG_DUVAR_1_[23]|SOL_DUVAR_2_|SAG_DUVAR_2_)/;
export function eskiDukkanGizle(kok, THREE) {
  const gizlenen = [], kutu = THREE ? new THREE.Box3() : null;
  kok.updateMatrixWorld(true);
  kok.traverse(o => {
    if (!o.name || !o.name.startsWith('DUKKAN26_') || !o.visible) return;
    const disari = kutu && o.isMesh && kutu.setFromObject(o).max.z > D.CEPHE_DIS + 0.005;
    if (ESKI_DUKKAN_DESEN.test(o.name) || disari) { o.visible = false; gizlenen.push(o.name); }
  });
  return gizlenen;
}

export function dukkanKur(THREE, scene) {
  const g = new THREE.Group(); g.name = 'IKIZ_DUKKAN'; scene.add(g);
  const liste = [];
  const M = (renk, ek = {}) => new THREE.MeshStandardMaterial({ color: renk, roughness: 0.75, metalness: 0.05, ...ek });
  const MAT = {
    duvar: M(0xe9e6e0), panel: M(0xd9dde2, { metalness: 0.2 }), zemin_ic: M(0xb9b4ab, { roughness: 0.9 }), kaldirim: M(0x9a9da2, { roughness: 0.95 }), cam: M(0xbfd6e6, { transparent: true, opacity: 0.25, roughness: 0.05, metalness: 0.1 }),
    kasa: M(0x2e3238, { metalness: 0.4, roughness: 0.5 }), paslanmaz: M(0xc8ccd0, { metalness: 0.75, roughness: 0.3 }), siyah: M(0x121417, { roughness: 0.4 }), ekran: M(0x0b0d10, { roughness: 0.2, metalness: 0.2 }),
    ahsap: M(0x8a6a4a), kapi: M(0x3a3f46, { metalness: 0.3 }),
  };
  function kutu(ad, x0, x1, y0, y1, z0, z1, mat, tur = 'parca') {
    const m = new THREE.Mesh(new THREE.BoxGeometry(Math.abs(x1 - x0), Math.abs(y1 - y0), Math.abs(z1 - z0)), mat);
    m.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2); m.name = 'DUKKAN__' + ad; g.add(m);
    liste.push({ ad, tur, kutu: [x0, x1, y0, y1, z0, z1].map(v => +v.toFixed(3)) }); return m;
  }
  function silindir(ad, x, z, r, y0, y1, mat, tur = 'parca') {                     // düşey silindir (tabure)
    const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, y1 - y0, 32), mat);
    m.position.set(x, (y0 + y1) / 2, z); m.name = 'DUKKAN__' + ad; g.add(m);
    liste.push({ ad, tur, kutu: [x - r, x + r, y0, y1, z - r, z + r].map(v => +v.toFixed(3)) }); return m;
  }
  const { CEPHE_IC: CI, CEPHE_DIS: CD, HUCRE_DUVAR: HD, HUCRE_PANEL: HP, X0, X1, TAVAN } = D;
  const HDi = HD + HP;                                                   // hücre duvarının personel yüzü
  const [a0, a1] = D.AYIRICI;
  /* zeminler */
  kutu('ZEMIN_HUCRE', X0, X1, -0.011, -0.001, -0.882, HD, MAT.zemin_ic, 'zemin');      // eski DUKKAN26_ZEMIN_0 (z 3,613'e uzanıyordu) gizlendi
  kutu('ZEMIN_PERSONEL', X0, a0, -0.01, 0, HDi, CI, MAT.zemin_ic, 'zemin');
  kutu('ZEMIN_MUSTERI', a1, X1, -0.01, 0, D.QR_YUZ, CI, MAT.zemin_ic, 'zemin');
  kutu('KALDIRIM', -0.6, 6.8, -0.012, 0, CD, 8.2, MAT.kaldirim, 'zemin');
  kutu('ESIK_CEPHE', X0, X1, -0.01, 0, CI, CD, MAT.zemin_ic, 'zemin');
  /* hücre duvarı z 1,750 (QR arka yüzü hizası; 20 mm panel, h 2,05) + hücre kapısı (menteşeli, kapalı çizilir; DOLDURMA rolü geçer) */
  const [h0, h1] = D.HUCRE_KAPI;
  kutu('HUCRE_DUVAR_1', X0, h0, 0, D.HUCRE_Y, HD, HDi, MAT.panel, 'duvar');
  kutu('HUCRE_DUVAR_2', h1, a0, 0, D.HUCRE_Y, HD, HDi, MAT.panel, 'duvar');
  kutu('HUCRE_KAPI_UST', h0, h1, D.HUCRE_KAPI_Y, D.HUCRE_Y, HD, HDi, MAT.panel, 'duvar');
  kutu('HUCRE_KAPI_KASA_SOL', h0, h0 + 0.03, 0, D.HUCRE_KAPI_Y, HD - 0.01, HDi + 0.01, MAT.kasa, 'kapi');
  kutu('HUCRE_KAPI_KASA_SAG', h1 - 0.03, h1, 0, D.HUCRE_KAPI_Y, HD - 0.01, HDi + 0.01, MAT.kasa, 'kapi');
  kutu('HUCRE_KAPI_KANAT', h0 + 0.03, h1 - 0.03, 0.01, D.HUCRE_KAPI_Y - 0.01, HD + 0.004, HDi - 0.004, MAT.cam, 'kapi');
  /* cephe z 2,883 düz (iki kapı + tezgâh penceresi) */
  const [p0, p1] = D.KAPI_P, [w0, w1, wy0, wy1] = D.PENCERE, [m0, m1] = D.KAPI_M;
  kutu('CEPHE_1', X0 - 0.1, p0, 0, TAVAN, CI, CD, MAT.duvar, 'duvar');
  kutu('CEPHE_2', p1, w0, 0, TAVAN, CI, CD, MAT.duvar, 'duvar');
  kutu('CEPHE_PENCERE_ALT', w0, w1, 0, wy0, CI, CD, MAT.duvar, 'duvar');
  kutu('CEPHE_PENCERE_UST', w0, w1, wy1, TAVAN, CI, CD, MAT.duvar, 'duvar');
  kutu('CEPHE_3', w1, m0, 0, TAVAN, CI, CD, MAT.duvar, 'duvar');
  kutu('CEPHE_4', m1, X1 + 0.1, 0, TAVAN, CI, CD, MAT.duvar, 'duvar');
  kutu('CEPHE_KAPI_UST_P', p0, p1, D.KAPI_Y, TAVAN, CI, CD, MAT.duvar, 'duvar');
  kutu('CEPHE_KAPI_UST_M', m0, m1, D.KAPI_Y, TAVAN, CI, CD, MAT.duvar, 'duvar');
  kutu('PENCERE_CAM_SURME', w0 + 0.01, w1 - 0.01, wy0 + 0.01, wy1 - 0.01, CI + 0.04, CI + 0.05, MAT.cam, 'cam');
  /* kapılar: personel kapısı dışa açılır (ikizde geçiş açık) · müşteri kapısı SÜRGÜLÜ: 2 cam kanat teleskopik, açık konumda soldaki cephenin dış yüzünde toplanır (ray üstte) */
  kutu('KAPI_PERSONEL_KASA', p0, p1, D.KAPI_Y - 0.04, D.KAPI_Y, CI, CD, MAT.kasa, 'kapi');
  kutu('KAPI_MUSTERI_KASA', m0, m1, D.KAPI_Y - 0.04, D.KAPI_Y, CI, CD, MAT.kasa, 'kapi');
  const [kk0, kk1] = D.KAPI_M_KANAT, [ry0, ry1] = D.KAPI_M_RAY;
  kutu('KAPI_MUSTERI_RAY', ry0, ry1, D.KAPI_Y, D.KAPI_Y + 0.08, CD, CD + 0.06, MAT.kasa, 'kapi');
  kutu('KAPI_MUSTERI_SURGU_1', kk0, kk1, 0.01, D.KAPI_Y - 0.01, CD + 0.01, CD + 0.02, MAT.cam, 'kapi');
  kutu('KAPI_MUSTERI_SURGU_2', kk0 + 0.01, kk1 + 0.01, 0.01, D.KAPI_Y - 0.01, CD + 0.035, CD + 0.045, MAT.cam, 'kapi');
  /* yan duvarlar (ön bölge) + ayırıcı z 1,750 → 2,883 */
  kutu('DUVAR_SOL', X0 - 0.1, X0, 0, TAVAN, HD, CD, MAT.duvar, 'duvar');
  kutu('DUVAR_SAG', X1, X1 + 0.1, 0, TAVAN, D.QR_YUZ, CD, MAT.duvar, 'duvar');
  kutu('AYIRICI_DUVAR', a0, a1, 0, TAVAN, HD, CI, MAT.duvar, 'duvar');
  /* tezgâh + L kolu = GERÇEK ÜNİTELER (10 Eki, A · PERSONEL TARAFI): MEIKO M-iClean US (L kolunda, önü −x, kapak tezgâh altı açık bölmeye) + el evyesi dolabı
     (hücre duvarı ucu) + deterjan / parlatıcı dolabı (köşe) + tezgâh (dar kilitli dolap + açık bölme) → ../ikiz_personel/personel_v1.glb. Yer tutucu kutular kalktı;
     liste'ye birim kutuları girer (TEZGAH_UST / EVYE_UST adları korunur). Ölçüler + bağlantılar: PERSONEL (personel_v1.js). */
  const [, , tz0, , , ty1] = D.TEZGAH;
  for (const p of PERSONEL.liste) liste.push({ ...p });
  const pg = new THREE.Group(); pg.name = 'DUKKAN__PERSONEL'; g.add(pg);
  new GLTFLoader().load('../ikiz_personel/' + PERSONEL.glb + '?v=' + PERSONEL.sha256.slice(0, 12),   // sayfa /ikiz/ → /ikiz_personel/ (köprü otonom/hat'ı sunar)
   
    gl => { pg.add(gl.scene); pg.userData.parca = gl.scene.children.length; }, undefined, e => console.error('personel GLB: ' + (e && e.message || e)));
  /* personel taburesi KALDIRILDI (K11 · IKIZ-ARAYUZ-6, 10 Eki: oturmaya gerek yok, tezgâh arkası şeridi kesintisiz) */
  /* POS tableti (tezgâhta, personele dönük) — Samsung Tab Active5 + masa standı [kat.] */
  const posX = 2.45, posZ = tz0 + 0.16;
  kutu('POS_STAND', posX - 0.06, posX + 0.06, ty1, ty1 + 0.12, posZ - 0.04, posZ + 0.04, MAT.kasa, 'cihaz');
  const PE = EKRAN.POS, posT = kutu('POS_TABLET', posX - PE.g / 2, posX + PE.g / 2, ty1 + 0.185 - PE.y / 2, ty1 + 0.185 + PE.y / 2, posZ - PE.d / 2, posZ + PE.d / 2, MAT.siyah, 'cihaz');   /* R24 D2: Tab Active5 föy */ posT.rotation.set(-D.POS_EGIM, Math.PI, 0, 'YXZ');   // CSS3D ile aynı (eski −0,35 X ↔ CSS3D ters eğim 'iç içe' görünüyordu)
  /* kiosk (duvar tipi, ayırıcının müşteri yüzünde, +x'e bakar) */
  const [kx0, kx1, kz0, kz1, ky0, ky1] = D.KIOSK;
  /* R24 D2: ekran Samsung QM32C portre (föy 421,9 × 727,3 × 28,5) + VESA 100 duvar askısı; altında ödeme terminali yuvası + fiş ağzı (gövde föyü YOK → VARSAYIM, RAPOR) */
  const KE = EKRAN.KIOSK, kzm = (kz0 + kz1) / 2, kyE0 = ky0 + 0.30;
  kutu('KIOSK_ASKI_VESA100', kx0, kx0 + 0.030, kyE0 + KE.y / 2 - 0.06, kyE0 + KE.y / 2 + 0.06, kzm - 0.06, kzm + 0.06, MAT.kasa, 'cihaz');
  kutu('KIOSK_EKRAN_QM32C', kx0 + 0.030, kx0 + 0.030 + KE.d, kyE0, kyE0 + KE.y, kzm - KE.g / 2, kzm + KE.g / 2, MAT.siyah, 'cihaz');
  kutu('KIOSK_GOVDE', kx0, kx0 + 0.060, ky0, kyE0 - 0.01, kz0, kz1, MAT.kasa, 'cihaz');   // alt ödeme / fiş gövdesi [VARSAYIM]
  kutu('KIOSK_POS_YUVA', kx0 + 0.058, kx0 + 0.10, ky0 + 0.10, ky0 + 0.20, kz0 + 0.12, kz1 - 0.12, MAT.siyah, 'cihaz');
  kutu('KIOSK_FIS_AGZI', kx0 + 0.056, kx0 + 0.064, ky0 + 0.235, ky0 + 0.245, kz0 + 0.14, kz1 - 0.14, MAT.siyah, 'cihaz');
  /* QR-5 (10 Eki, K6): QR kolonundaki 7" ekran KALKTI — teslim yalnız FM430 QR okuyucu + Storm tuş takımı (ikizde tuşlar tıklanır: gezinti.js) */
  /* bekleme TV'si 43" DİKEY (sağ duvar iç yüzü, −x) */
  const TV = D.TV, TE = EKRAN.TV; kutu('TV_43', TV[1] - 0.035 - TE.d, TV[1] - 0.035, TV[2], TV[3], TV[4], TV[5], MAT.siyah, 'cihaz'); kutu('TV_ASKI', TV[1] - 0.035, TV[1], (TV[2] + TV[3]) / 2 - 0.13, (TV[2] + TV[3]) / 2 + 0.13, (TV[4] + TV[5]) / 2 - 0.13, (TV[4] + TV[5]) / 2 + 0.13, MAT.kasa, 'cihaz');   // QB43C + VESA 200 askı
  /* sipariş panosu 49" şerit (hücre duvarının personel yüzü, +z; VESA askı yalnız personel yüzündeki taşıyıcı profile — koruyucu panel delinmez, ISO 14120) */
  const S = D.SERIT; kutu('SERIT_49', S[0], S[1], S[2], S[3], S[4] + 0.030, S[5], MAT.siyah, 'cihaz'); kutu('SERIT_ASKI', (S[0] + S[1]) / 2 - 0.22, (S[0] + S[1]) / 2 + 0.22, (S[2] + S[3]) / 2 - 0.12, (S[2] + S[3]) / 2 + 0.12, S[4], S[4] + 0.030, MAT.kasa, 'cihaz');   // LG 37BH7N-H + VESA 400 × 200 askı (ad SERIT_49 korunur: testler / saydam)
  /* Kemal R24 (10 Eki gece, YÖNETİCİ onayı D1–D8): aydınlatma, kapı donanımı + açılış, süpürgelik / tavan kenarı / tabela alanı, tesisat uçları, interkom, QR oku, AZM40 → dukkan_v4.js */
  const v4 = dukkanV4(THREE, scene, g, D, kutu, MAT); for (const p of v4.ek) liste.push(p);
  /* dışarıdan bakışta (orbit) duvarlar yarı saydam: makine görünsün; gezintide tam opak */
  const saydamlar = g.children.filter(m => /^DUKKAN__(CEPHE|DUVAR|AYIRICI|HUCRE_DUVAR|HUCRE_KAPI_UST|SERIT_49|SERIT_ASKI|TV_43|TV_ASKI|TABELA|TAVAN_KENAR|SUPURGELIK)/.test(m.name));
  for (const m of saydamlar) m.material = m.material.clone();
  function gorunum(ic) { for (const m of saydamlar) { m.material.transparent = !ic; m.material.opacity = ic ? 1 : 0.28; m.material.depthWrite = ic; m.renderOrder = ic ? 0 : -1; m.material.needsUpdate = true; } }   // C E15: saydam duvar diğer saydamlardan (QR kapak camı %16) ÖNCE çizilir — cam 'yok' görünmesin
  gorunum(false);
  return { grup: g, liste, gorunum, guncelle: v4.guncelle, v4: v4.say };
}

/* CSS3D ekran yerleri (merkez, genişlik m, yön): ekranlar 3B içinde bu noktalarda gerçek sayfayı gösterir */
export function ekranYerleri() {
  const K = D.KIOSK, TV = D.TV, S = D.SERIT, TZ = D.TEZGAH;
  return [
    { id: 'kiosk', ad: 'Kiosk (32" portre)', konum: [K[0] + 0.030 + EKRAN.KIOSK.d + 0.002, K[4] + 0.30 + EKRAN.KIOSK.y / 2, (K[2] + K[3]) / 2], genislik: EKRAN.KIOSK.aktif[0], en: 540, boy: 960, yon: Math.PI / 2, url: '../musteri/index.html?mod=kiosk&hmi=yok', rol: 'musteri' },
    { id: 'tv', ad: 'Bekleme ekranı (43" dikey)', konum: [TV[1] - 0.035 - EKRAN.TV.d - 0.002, (TV[2] + TV[3]) / 2, (TV[4] + TV[5]) / 2], genislik: EKRAN.TV.aktif[0], en: 720, boy: 1280, yon: -Math.PI / 2, url: '../musteri/bekleme.html?hmi=yok', rol: 'musteri' },
    { id: 'serit', ad: 'Sipariş panosu (37" şerit, LG 37BH7N-H)', konum: [(S[0] + S[1]) / 2, (S[2] + S[3]) / 2, S[5] + 0.002], genislik: EKRAN.SERIT.aktif[0], en: 3840, boy: 1080, yon: 0, url: '../musteri/dis-ekran.html?hmi=yok', rol: 'musteri' },
    { id: 'pos', ad: 'Kasa tableti (POS)', konum: [2.45, TZ[5] + 0.185 + 0.007 * Math.sin(D.POS_EGIM), TZ[2] + 0.16 - 0.007 * Math.cos(D.POS_EGIM)], genislik: EKRAN.POS.aktif[0], en: 1024, boy: 720, yon: Math.PI, egim: D.POS_EGIM, url: null, rol: 'personel', arka: 'tablet' },
  ];
}

/* Yürünebilir alanlar (göz noktası; duvar / mobilya + 0,2 m pay). Robot hücresi (z < 1,750) yalnız DOLDURMA rolünde, hücre kapısından.
   3c: cephe iç 2,883 / dış 2,983 · müşteri z 2,283 … 2,683 · kiosk önü x ≥ 3,937 · TV önü x ≤ 5,09 · müşteri kapısı geçişi x 4,51–5,01
   · tezgâh arkası z 1,97 … 2,233 · evye x 2,947 − 0,2 · personel kapısı geçişi x 0,886–1,386 */
export function yurunur(rol) {
  const A = [
    [-0.4, 3.183, 6.6, 8.0],         // kaldırım (cephe dışı + 0,2)
    [3.937, 2.283, 5.09, 2.683],     // müşteri bölgesi (kiosk önü … TV önü; QR + 0,2 … cephe iç − 0,2)
    [4.51, 2.60, 5.01, 3.20],        // müşteri kapısı geçişi (sürgülü, x 4,31–5,21)
  ];
  if (rol === 'personel' || rol === 'doldurma' || rol === 'patron') {
    A.push([0.85, 1.97, PERSONEL.yurunur_tezgah_arkasi_x1, 2.233]);  // tezgâh arkası (hücre duvarı + 0,2 … L kolu tablası − 0,2; personel_v1)
    A.push([0.85, 1.97, 1.536, 2.075]);  // tezgâh solu (el lavabosunun hücre tarafı: lavabo z 2,275 − 0,2)
    A.push([1.136, 1.97, 1.536, 2.683]); // tezgâh solu → personel kapısı (el lavabosu x 0,936 + 0,2)
    A.push([1.136, 2.60, 1.386, 3.20]);  // personel kapısı geçişi (el lavabosu x 0,936 + 0,2)
  }
  if (rol === 'doldurma') {
    A.push([0.85, 1.20, 1.45, 2.10]);  // robot hücresi kapısı (x 0,686–1,586, z 1,750)
    A.push([0.85, 1.10, 5.10, 1.55]);  // hücre içi, makine önü (hat duruyorken; hücre duvarı − 0,2)
  }
  return (x, z) => A.some(([x0, z0, x1, z1]) => x >= x0 && x <= x1 && z >= z0 && z <= z1);   // tabure kalktı → tezgâh arkası x 0,85–2,747 kesintisiz
}
