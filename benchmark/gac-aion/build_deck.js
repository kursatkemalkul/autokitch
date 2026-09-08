// GAC / AION interior benchmark board - 50" x 12.38", 3 slides
// Photo frames left empty on purpose - the designer drops press images in.
const pptxgen = require("pptxgenjs");

const W = 50, H = 12.38;
const M = 0.6;
const CW = W - 2 * M;

const INK   = "15181C";
const INK2  = "3E434A";
const MUTED = "8B8F96";
const FAINT = "B9BCC0";
const GHOST = "D5D7DA";
const LINE  = "E2E1DD";
const PANEL = "F4F4F1";
const PANEL2= "EBEBE7";
const WHITE = "FFFFFF";
const AION  = "0B63F6";
const TRU   = "B23A2C";
const PREM  = "2B2A45";
const OK    = "0F7B6C";

const FS = "Arial";
const FQ = "Cambria";

// price / positioning ladder
const SEG = {
  ENTRY:      "A9AEB4",
  MID:        "6E7681",
  "UPPER-MID":"3E434A",
  PREMIUM:    "2B2A45",
  LUXURY:     "8A6D3B",
  FLAGSHIP:   "15181C"
};

const pres = new pptxgen();
pres.defineLayout({ name: "BOARD", width: W, height: H });
pres.layout = "BOARD";
pres.author = "Interior Design";
pres.title = "GAC x AION Interior Benchmark";

/* ---------- helpers ---------- */
function T(s, text, o) {
  s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: FS, valign: "top" }, o));
}
function box(s, o) {
  s.addShape(pres.ShapeType.roundRect, Object.assign({ rectRadius: 0.04, line: { width: 0 } }, o));
}
function rect(s, o) {
  s.addShape(pres.ShapeType.rect, Object.assign({ line: { width: 0 } }, o));
}
function micro(s, x, y, w, text, color) {
  T(s, text, { x, y, w, h: 0.13, fontSize: 7, bold: true, charSpacing: 1.1, color: color || MUTED });
}
function chip(s, x, y, text, fill, color) {
  const w = 0.085 * text.length + 0.24;
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.20, rectRadius: 0.10,
    fill: { color: fill }, line: { width: 0 } });
  T(s, text, { x, y: y + 0.035, w, h: 0.15, fontSize: 7, bold: true, charSpacing: 0.8,
               color: color || WHITE, align: "center" });
  return w;
}
function heading(s, x, y, w, kicker, title) {
  micro(s, x, y, w, kicker, MUTED);
  T(s, title, { x, y: y + 0.17, w, h: 0.32, fontSize: 17, bold: true, color: INK });
}
function spec(s, x, y, w, label, value, h, fs) {
  micro(s, x, y, w, label, FAINT);
  T(s, value, { x, y: y + 0.15, w, h: h || 0.60, fontSize: fs || 8.5, color: INK2,
                lineSpacingMultiple: 1.08 });
}
function bullets(s, x, y, w, items, o) {
  o = o || {};
  const arr = items.map((t, i) => ({
    text: t,
    options: { bullet: { code: "2022", indent: 10 }, breakLine: i !== items.length - 1 }
  }));
  T(s, arr, { x, y, w, h: o.h || 1.0, fontSize: o.fs || 8.6, color: o.color || INK2,
              lineSpacingMultiple: o.ls || 1.14, paraSpaceAfter: o.gap === undefined ? 5 : o.gap });
}
function footer(s, text) {
  T(s, text, { x: M, y: H - 0.60, w: CW, h: 0.34, fontSize: 7.4, color: FAINT,
               lineSpacingMultiple: 1.12 });
}
function header(s, num, kicker, title, sub) {
  T(s, num, { x: M, y: 0.42, w: 1.4, h: 0.36, fontSize: 26, bold: true, color: FAINT });
  micro(s, M + 0.62, 0.52, 14, kicker, MUTED);
  T(s, title, { x: M + 0.62, y: 0.70, w: 32, h: 0.56, fontSize: 33, bold: true, color: INK });
  T(s, sub, { x: M + 0.62, y: 1.31, w: 34, h: 0.34, fontSize: 10.5, color: MUTED,
              lineSpacingMultiple: 1.12 });
}
function kpi(s, x, y, w, value, label, color) {
  T(s, value, { x, y, w, h: 0.42, fontSize: 25, bold: true, color: color || INK });
  T(s, label, { x, y: y + 0.44, w, h: 0.38, fontSize: 8, color: MUTED, lineSpacingMultiple: 1.08 });
}

/* ---------- empty photo frame (16:9) ---------- */
function photoFrame(s, x, y, w, h, model, shot) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.02,
    fill: { color: "FBFBFA" }, line: { color: "D6D4CF", width: 1, dashType: "dash" } });
  // corner crop marks
  const t = 0.22, lw = 0.9;
  [[x, y, 1, 1], [x + w, y, -1, 1], [x, y + h, 1, -1], [x + w, y + h, -1, -1]].forEach(c => {
    s.addShape(pres.ShapeType.line, { x: Math.min(c[0], c[0] + c[2] * t), y: c[1],
      w: t, h: 0, line: { color: GHOST, width: lw } });
    s.addShape(pres.ShapeType.line, { x: c[0], y: Math.min(c[1], c[1] + c[3] * t),
      w: 0, h: t, line: { color: GHOST, width: lw } });
  });
  T(s, model, { x, y: y + h / 2 - 0.34, w, h: 0.24, fontSize: 11, bold: true, charSpacing: 1.6,
                color: GHOST, align: "center" });
  T(s, shot, { x: x + 0.5, y: y + h / 2 - 0.04, w: w - 1.0, h: 0.34, fontSize: 8.5,
               color: GHOST, align: "center", lineSpacingMultiple: 1.1 });
  T(s, "16:9", { x: x + w - 0.72, y: y + h - 0.28, w: 0.56, h: 0.16, fontSize: 7,
                 color: GHOST, align: "right" });
}

/* ---------- model card ---------- */
const CARD_W = 11.9, CARD_H = 4.68, COL_GAP = 0.4;
const colX = i => M + i * (CARD_W + COL_GAP);

function modelCard(s, x, y, d) {
  box(s, { x, y, w: CARD_W, h: CARD_H, fill: { color: PANEL } });
  const px = x + 0.28;

  T(s, d.name, { x: px, y: y + 0.20, w: 7.4, h: 0.32, fontSize: 17, bold: true, color: INK });
  const segW = 0.085 * d.seg.length + 0.24;
  chip(s, x + CARD_W - 0.28 - segW, y + 0.24, d.seg, SEG[d.seg]);
  if (d.flag) {
    const fw = chip(s, x + CARD_W - 0.28 - segW - (0.085 * d.flag.length + 0.24) - 0.14,
                    y + 0.24, d.flag, d.accent);
  }
  T(s, d.meta, { x: px, y: y + 0.58, w: CARD_W - 0.56, h: 0.22, fontSize: 8.5, color: MUTED });

  photoFrame(s, px, y + 0.88, 6.6, 3.55, d.name, d.shot);

  const rx = x + 7.10, rw = CARD_W - 7.10 - 0.28;
  let ry = y + 0.88;
  spec(s, rx, ry, rw, "SCREENS", d.screens, 0.62); ry += 0.90;
  spec(s, rx, ry, rw, "MATERIALS · COLOUR", d.cmf, 0.62); ry += 0.90;
  spec(s, rx, ry, rw, "SEAT · COMFORT", d.seat, 0.62); ry += 0.90;
  spec(s, rx, ry, rw, "WHO IT IS FOR", d.who, 0.62);
}

function readCard(s, x, y, title, kicker, items, cost, accent) {
  box(s, { x, y, w: CARD_W, h: CARD_H, fill: { color: INK } });
  const px = x + 0.34, pw = CARD_W - 0.68;
  T(s, title, { x: px, y: y + 0.26, w: pw, h: 0.62, fontSize: 19, bold: true, color: WHITE,
                lineSpacingMultiple: 1.04 });
  micro(s, px, y + 1.02, pw, kicker, accent);
  bullets(s, px, y + 1.26, pw, items, { fs: 9, color: "D6D8DC", ls: 1.16, h: 2.00, gap: 6 });
  rect(s, { x: px, y: y + CARD_H - 1.28, w: pw, h: 0.006, fill: { color: "3A3F46" } });
  micro(s, px, y + CARD_H - 1.10, pw, "WHAT IT COSTS THEM", accent);
  T(s, cost, { x: px, y: y + CARD_H - 0.90, w: pw, h: 0.72, fontSize: 8.8, color: "9CA2AA",
               lineSpacingMultiple: 1.14 });
}

const ROW1 = 2.02, ROW2 = 6.92;

/* =========================================================================
   SLIDE 1 - AION
   ========================================================================= */
const s1 = pres.addSlide();
s1.background = { color: WHITE };

header(s1, "01", "INTERIOR BENCHMARK · GAC GROUP · SEPTEMBER 2026",
  "AION — the cabins on sale",
  "Seven battery-electric models, read as interiors: screen architecture, materials and colour, seat hardware, and the occupant each cabin is drawn for.\nPrices are China MSRP bands in RMB. Image frames are left empty for press photography.");

const k1 = 34.0, kg = 4.1;
kpi(s1, k1,          0.62, 3.8, "74,100", "AION retail, Q1 2026\n+57.3% year on year", AION);
kpi(s1, k1 + kg,     0.62, 3.8, "+62.5%", "April 2026 alone\n38,000+ units", AION);
kpi(s1, k1 + kg * 2, 0.62, 3.8, '14.6"', "centre-screen floor\nright across the range", INK);
kpi(s1, k1 + kg * 3, 0.62, 3.8, "32", "ambient colours, standard\non almost everything", INK);

micro(s1, M, 1.84, 30, "ENTRY  →  CORE  —  “FASHIONABLE, INTELLIGENT, REASSURING” · SOLD ON COLOUR AND ONE BIG TILE", AION);

const AIONS = [
  { name: "AION UT", seg: "ENTRY", accent: AION,
    meta: "B-segment hatch · BEV · China ≈¥70–105k · 4,270 mm",
    shot: "dashboard, ¾ from the driver door — cream or dusky pink trim on doors and dash",
    screens: '14.6" centre tile with an 8.8" driver cluster. Climate, mirrors and driver aids all live in the tile — almost no physical switchgear survives.',
    cmf: "PVC upholstery in cream or dusky pink, carried up onto the door cards and the dash. Padded dash top; soft-touch continues to the rear door cards.",
    seat: "Manual adjustment, no comfort electronics. The party trick is that every seat folds into a full-length flat bed.",
    who: "First-car urban buyer, 22–28. Colour is the product — they choose the cabin before they choose the car." },

  { name: "AION RT", seg: "MID", accent: AION,
    meta: "Mid-size fastback sedan · BEV · ¥85.8–123.8k · 4,865 / 2,775 mm",
    shot: "dashboard straight on, plus a close-up of the suede seat facing",
    screens: '14.6" centre + 8.8" cluster. Minimalist, function-first surfacing — the dash reads as one horizontal plane.',
    cmf: "100% leather-wrap on every high-contact surface; suede-finished “zero-pressure” seats. The brand does not name this colourway.",
    seat: "Suede zero-pressure seats. Rear knee room quoted at two fists behind a 175 cm driver.",
    who: "Value-led tech buyer cross-shopping a Model 3. Wants the sparse cabin, not the luxury cues." },

  { name: "AION Y PLUS", seg: "MID", accent: AION,
    meta: "Compact SUV · BEV · ¥99.8–153.8k · refreshed 2025 · CLTC up to 610 km",
    shot: "green cabin theme — screen rotated to portrait, then to landscape",
    screens: '14.6" rotating centre screen, switching between portrait and landscape on demand.',
    cmf: "Vegan leather. The green cabin theme is briefed as “healing” relief from urban stress — the clearest colour-as-message case anywhere in the range.",
    seat: "Comfort-led, no massage. Wireless charging pad that actually holds a phone through a corner.",
    who: "Young family buying their first EV. Space per yuan is the pitch; the colour is what closes it." },

  { name: "AION N60", seg: "MID", accent: AION, flag: "APR 2026",
    meta: "Compact SUV · BEV 610 km · ¥109.8–129.8k · 4,615 / 2,775 mm",
    shot: "all three named themes side by side; zero-gravity passenger seat reclined",
    screens: '15.6" 2.5K single tile on ADiGO 6.0 — AI voice model, Huawei Nebula ecosystem, iOS and Android casting. Cluster deleted.',
    cmf: "Three named themes: Soft Light White, Caramel Warm Velvet, Morning Mist Cool Grey. 2.38 m² panoramic roof, 35 stowage points, 447→1,947 L.",
    seat: "Zero-gravity front passenger seat as standard. Front heating, ventilation, massage and memory. Rear backrest 117–137°.",
    who: "Young family — priced at entry, specified like a mid. The car that dragged premium seating below ¥130k, with LiDAR standard." },

  { name: "AION i60", seg: "MID", accent: AION,
    meta: "Compact crossover · BEV 650 km / EREV 1,240 km · from ≈¥115.8k",
    shot: "dual-tone split across the IP; front seat cushion structure",
    screens: '14.6" on ADiGO 5.0, with GSD highway navigation assist and smart parking.',
    cmf: "Dual-tone split cabin with 32-colour ambient lighting. Colourway names not published.",
    seat: "“Eight-layer comfort sofa” front seats — 8-point massage, ventilation, heating and memory.",
    who: "Range-anxious family buyer. One body, two powertrains, one identical cabin — the interior never tells you which you bought." },

  { name: "AION V", seg: "UPPER-MID", accent: AION,
    meta: "Mid-size SUV · BEV · 2nd generation 2024 · the export flagship",
    shot: "black standard trim vs the cream / tan leather option, same angle",
    screens: '14.6" centre runs climate, mirrors and ADAS settings; the 8.8" cluster is retained.',
    cmf: "Black faux leather standard; genuine leather in cream or tan for a small premium. Soft leather-like uppers, well-damped switchgear, 32-colour ambient.",
    seat: "Comfort-led. Nine-speaker 360 W audio and a two-metre-plus panoramic roof with a powered blind.",
    who: "The car GAC exports. This is the cabin that has to survive European and Australian press scrutiny." },

  { name: "AION RAY 7", seg: "PREMIUM", accent: AION, flag: "UNVEILED 19 AUG 2026",
    meta: "Mid-large fastback · BEV ≈700 km · expected ¥200–250k · 4,960 / 2,920 mm",
    shot: "any interior frame from the Chengdu unveil — this cabin is the open question",
    screens: "Not disclosed at the unveil. The exterior signature is the new illuminated AION logo inside a full-width star-ring light bar.",
    cmf: "Not published. Watch this one: it is the first interior of the post-rebrand AION design language.",
    seat: "Not published.",
    who: "Launch model of the new “Ray” series, aimed squarely at young buyers. Huawei DriveONE 180 kW." }
];

AIONS.forEach((d, i) => {
  const col = i % 4, row = Math.floor(i / 4);
  modelCard(s1, colX(col), row === 0 ? ROW1 : ROW2, d);
});

readCard(s1, colX(3), ROW2,
  "AION — one recipe,\nseven cars",
  "WHAT THE BOARD ABOVE ADDS UP TO", [
    '14.6" is the floor; 15.6" 2.5K is the new step and it deletes the cluster.',
    "One tile runs climate, mirrors and ADAS. The switchgear does not survive.",
    "32-colour ambient is assumed rather than sold.",
    "Materials climb PVC → vegan leather → suede with price, in that order.",
    "Zero-gravity seating and massage crossed below ¥130k in April 2026.",
    "Colour — cream, dusky pink, caramel, green — does the differentiating that surface form no longer does."
  ],
  "Every climate and mirror adjustment is a menu dive. Seven cars share one cabin grammar, so the range reads as a single product offered at seven sizes.",
  "6FA8FF");

footer(s1, "Image frames are intentionally empty — drop press photography in and the layout holds.   ·   Sources: GAC / AION press material and Auto China 2026 releases; CnEVPost; CarNewsChina; Gasgoo; BitAuto; CarExpert, Chasing Cars, What Car?, Electrifying, RACV, zecar. Compiled September 2026. Prices are China MSRP bands and move with promotion. Fields marked “not published” were not found in a primary or reputable secondary source — measure them on the vehicle.");

/* =========================================================================
   SLIDE 2 - TRUMPCHI + HYPTEC
   ========================================================================= */
const s2 = pres.addSlide();
s2.background = { color: WHITE };

header(s2, "02", "INTERIOR BENCHMARK · GAC GROUP · SEPTEMBER 2026",
  "TRUMPCHI + HYPTEC — the cabins on sale",
  "The comfort half of the group: six Trumpchi models plus the Hyptec flagship, read the same way. Where AION sells colour, this side of the house sells the second row.\nPrices are China MSRP bands in RMB. Image frames are left empty for press photography.");

kpi(s2, k1,          0.62, 3.8, "92,100", "TRUMPCHI retail, Q1 2026\n+33.1% year on year", TRU);
kpi(s2, k1 + kg,     0.62, 3.8, "137°", "rear recline already at\n¥170k (Xiangwang S7)", TRU);
kpi(s2, k1 + kg * 2, 0.62, 3.8, "7", "screens in collaboration\nin the M8 Xiangwang cabin", INK);
kpi(s2, k1 + kg * 3, 0.62, 3.8, "6,536", "mm of ambient light run\nin the Hyptec A800", PREM);

micro(s2, M, 1.84, 34, "ENTRY  →  FLAGSHIP  —  TRUMPCHI: “FAMILY MOBILITY” · SOLD ON THE SECOND ROW      │      HYPTEC: PREMIUM TECH · THE GROUP'S CEILING", TRU);

const TRUS = [
  { name: "TRUMPCHI GS3 EMZOOM", seg: "ENTRY", accent: TRU,
    meta: "Small SUV · 1.5T petrol · the brand's youth entry point",
    shot: "driver-side IP and the sport seat bolster",
    screens: '12.3" centre screen — the smallest display anywhere in the group.',
    cmf: "32-colour ambient lighting even at the entry point. Driver-focused, sport-flavoured trim with conventional switchgear kept in place.",
    seat: "Sport-bolstered fronts. No comfort electronics at this level.",
    who: "Under-30 first-car buyer who still wants an engine. The only Trumpchi not sold on rear-seat comfort." },

  { name: "TRUMPCHI GS8", seg: "MID", accent: TRU,
    meta: "Large 7-seat SUV · 2.0T 252 hp / hybrid · from ≈¥159.8k",
    shot: "second and third rows from the tailgate, folded and upright",
    screens: "Screen sizes are not published in English-language sources — measure these on the car.",
    cmf: "Conventional twin-display architecture. This is the classic family flagship the whole brand is now being rebuilt around.",
    seat: "2+3+2. The second and third rows are what make the sale.",
    who: "Three-generation family. Bought on seat count, boot space and running cost, not on screen inches." },

  { name: "TRUMPCHI XIANGWANG S7", seg: "UPPER-MID", accent: TRU,
    meta: "Mid-size PHEV SUV · Mar 2025 · guide ¥209.8–249.8k · 4.90 m, five seats",
    shot: "rear seat fully reclined with the leg rest out and the ceiling screen down",
    screens: 'Snapdragon 8295P on ADiGO 6.0. A 17.3" ceiling-mounted screen folds down for the rear passengers.',
    cmf: "Warm, light-toned luxury trim. 4.90 m long but only five seats — all the space goes into the second row.",
    seat: "Ventilation, heating and massage: six modes at three intensities. Rear reclines to 137° on a zero-gravity “cloud” leg rest.",
    who: "A family SUV sold on the bench, not on the driver's seat. Buyers who would rather be driven at the weekend." },

  { name: "TRUMPCHI XIANGWANG S9", seg: "PREMIUM", accent: TRU,
    meta: "Full-size SUV · five- or six-seat · Huawei HarmonySpace cabin",
    shot: "six-seat layout — second-row captain chairs with their own console",
    screens: 'Three screens in total, with a 12.3" cluster behind the wheel. Huawei HarmonySpace is the cabin backbone; the other diagonals are not published.',
    cmf: "Positioned above the S7. Choosing five or six seats changes the entire second-row architecture, not just the seat count.",
    seat: "Six-seat form gets second-row captain chairs that recline and carry their own climate and media controls — a second cockpit, not a bench.",
    who: "The GS8 owner trading up, buying the Huawei cabin badge as much as the car." },

  { name: "TRUMPCHI E9", seg: "LUXURY", accent: TRU,
    meta: "Luxury PHEV MPV · 2023 · from ≈US$47k · the Alphard answer",
    shot: "second-row armrest touch pad, and the ceiling screen deployed",
    screens: 'Four displays: 14.6" centre, 12.3" cluster, 12.3" front passenger and 15.6" in the ceiling.',
    cmf: "Light, champagne-toned cabin. Control physically moves out of the driver's seat and into the second row.",
    seat: "2+2+3 with second-row captain chairs, each carrying its own 5\" touch pad in the armrest to drive its own seat.",
    who: "Chauffeur-driven business use, cross-shopped directly against the Toyota Alphard." },

  { name: "TRUMPCHI M8 XIANGWANG", seg: "LUXURY", accent: TRU,
    meta: "Full-size MPV · 2026 model year · the brand's ceiling",
    shot: "welcome projection at the door; third row powered flat",
    screens: 'HarmonySpace 5 on a 15.6" centre screen, running seven-screen collaboration across the cabin.',
    cmf: "Cabin grades are sold by name — Qiankun Max Luxury Cabin, Qiankun Ultra First-Class Cabin — with a welcome projection at the door.",
    seat: "Power-adjustable third row in a 2+2+3 layout. Ceremony is engineered here, not implied.",
    who: "Business travel where the owner sits in row two and the car is part of the meeting." },

  { name: "HYPTEC A800", seg: "FLAGSHIP", accent: PREM,
    meta: "Flagship EREV sedan · pre-order Dec 2025 · the group's ceiling",
    shot: "wraparound console, and the 27\" W-HUD in the driver's eye line",
    screens: '“Interstellar Cockpit”: wraparound console with a 10.25" cluster, 14.6" centre and a 27" W-HUD. HarmonySpace 5 on a flagship Qualcomm chip, 0.3 s response.',
    cmf: "A 6,536 mm ambient light run — claimed the longest in the world. Seamless wraparound surfacing with active noise cancellation.",
    seat: "Eight-way power front seats with three massage modes.",
    who: "Premium technology early adopter. Huawei Qiankun ADS 4 Ultra, with L3 on the highway." }
];

TRUS.forEach((d, i) => {
  const col = i % 4, row = Math.floor(i / 4);
  modelCard(s2, colX(col), row === 0 ? ROW1 : ROW2, d);
});

readCard(s2, colX(3), ROW2,
  "TRUMPCHI + HYPTEC —\none recipe, seven cars",
  "WHAT THE BOARD ABOVE ADDS UP TO", [
    "Comfort is quantified and sold: recline angle, massage modes, screens per seat.",
    "Screens multiply rather than grow — cluster, centre, passenger, ceiling, armrest.",
    "Huawei is the cabin brand above ¥200k: HarmonySpace 5 and Qiankun ADS.",
    "Ceremony does the premium work — welcome projection, named cabin grades.",
    'The 27" W-HUD is the new flagship signature, not a bigger centre screen.'
  ],
  "Cabin identity is increasingly Huawei's rather than Trumpchi's. Below ¥170k the interior story thins out fast — Emzoom and GS8 are a full generation behind their own flagship.",
  "E3A08F");

footer(s2, "Image frames are intentionally empty — drop press photography in and the layout holds.   ·   Sources: GAC / Trumpchi / Hyptec press material; Auto China 2026 and Auto Guangzhou releases; CarNewsChina; BitAuto; Gasgoo; CnEVPost. Compiled September 2026. Prices are China MSRP bands. Fields marked “not published” were not found in a primary or reputable secondary source — measure them on the vehicle.");

/* =========================================================================
   SLIDE 3 - the read
   ========================================================================= */
const s3 = pres.addSlide();
s3.background = { color: WHITE };

header(s3, "03", "INTERIOR BENCHMARK · GAC GROUP · SEPTEMBER 2026",
  "What it means for us",
  "The two boards read together: the design doctrines, the CMF and comfort ladders, the occupants GAC is drawing for, and where Changan's cabins actually stand.");

const RA = 2.02, RAH = 4.32;
const RB = 6.62, RBH = 4.98;

/* ---- A1 doctrines ---- */
const a1x = M, a1w = 15.0;
heading(s3, a1x, RA, a1w, "DOCTRINE", "What each brand believes a cabin is");
const DOC = [
  { t: "AION", sub: "“Fashionable, intelligent, reassuring”", c: AION,
    d: "One screen, soft surfaces and colour. Design VP Fan Zhang frames it as “the aesthetics of man–machine symbiosis” — adapting to the occupant rather than impressing them.",
    moves: 'One 14.6–15.6" tile · 32-colour ambient · named vegan-leather colourways · flat-fold bed mode · zero-gravity co-pilot',
    first: "The colourway — seen from the pavement, before the door is opened." },
  { t: "TRUMPCHI", sub: "“Family mobility”", c: TRU,
    d: "Comfort you can count. The cabin is specified in numbers a buyer can repeat in a showroom: recline angle, massage modes, screens per seat.",
    moves: "Second-row captain chairs · zero-gravity leg rests · ceiling screen · welcome projection · Huawei HarmonySpace",
    first: "The second row." },
  { t: "HYPTEC · AISTALAND", sub: "Premium tech", c: PREM,
    d: "The cabin as an instrument. “Organic modernism” on Hyper GT, “Interstellar Cockpit” on the A800. Light and horizon replace trim as the luxury material.",
    moves: '27" W-HUD · wraparound console · 6,536 mm ambient run · 18-point massage · zero-gravity at 127.5°',
    first: "The HUD horizon, before the seat." }
];
const docW = (a1w - 2 * 0.24) / 3, docY = RA + 0.58, docH = 2.44;
DOC.forEach((d, i) => {
  const dx = a1x + i * (docW + 0.24);
  box(s3, { x: dx, y: docY, w: docW, h: docH, fill: { color: PANEL } });
  const px = dx + 0.24, pw = docW - 0.48;
  chip(s3, px, docY + 0.18, d.t, d.c);
  T(s3, d.sub, { x: px, y: docY + 0.46, w: pw, h: 0.26, fontSize: 9, bold: true, color: INK,
                 lineSpacingMultiple: 1.05 });
  T(s3, d.d, { x: px, y: docY + 0.76, w: pw, h: 0.62, fontSize: 8.6, color: INK,
               lineSpacingMultiple: 1.1 });
  spec(s3, px, docY + 1.42, pw, "SIGNATURE MOVES", d.moves, 0.30, 8);
  spec(s3, px, docY + 1.94, pw, "WHAT THE BUYER SEES FIRST", d.first, 0.30, 8);
});
const qY = docY + docH + 0.12;
box(s3, { x: a1x, y: qY, w: a1w, h: RA + RAH - qY, fill: { color: INK } });
T(s3, "“Form language lasts for one generation in China.”",
  { x: a1x + 0.30, y: qY + 0.18, w: a1w - 0.60, h: 0.30, fontSize: 15, italic: true,
    fontFace: FQ, color: WHITE });
T(s3, "Fan Zhang, Vice President of Design, GAC — which is why the group renews cabin architecture on a roughly four-year clock and lets colour, not surface form, carry the model-year difference.",
  { x: a1x + 0.30, y: qY + 0.56, w: a1w - 0.60, h: 0.44, fontSize: 8.4, color: "9CA2AA",
    lineSpacingMultiple: 1.12 });

/* ---- A2 CMF ---- */
const a2x = 16.0, a2w = 9.5;
heading(s3, a2x, RA, a2w, "CMF", "Colourways actually on sale");
T(s3, "Every swatch below is a shipping option, not a show car. AION names its interiors; Trumpchi names its seats.",
  { x: a2x, y: RA + 0.50, w: a2w, h: 0.30, fontSize: 8, color: MUTED, lineSpacingMultiple: 1.1 });
const SW = [
  { h: "F2EFE9", n: "Soft Light White", m: "AION N60 · named theme" },
  { h: "9A6A45", n: "Caramel Warm Velvet", m: "AION N60 · named theme" },
  { h: "9BA1A4", n: "Morning Mist Cool Grey", m: "AION N60 · named theme" },
  { h: "E8DFCB", n: "Cream", m: "AION UT seats, doors and dash · AION V option" },
  { h: "CBA0A2", n: "Dusky Pink", m: "AION UT · the boldest shipping colour in the range" },
  { h: "8FA98A", n: "Healing Green", m: "AION Y Plus · briefed as urban stress relief" }
];
let sy = RA + 0.88;
SW.forEach(sw => {
  s3.addShape(pres.ShapeType.roundRect, { x: a2x, y: sy, w: 0.80, h: 0.32, rectRadius: 0.05,
    fill: { color: sw.h }, line: { color: "D9D7D2", width: 0.5 } });
  T(s3, sw.n, { x: a2x + 0.96, y: sy - 0.01, w: a2w - 0.96, h: 0.18, fontSize: 8.8, bold: true, color: INK });
  T(s3, sw.m, { x: a2x + 0.96, y: sy + 0.16, w: a2w - 0.96, h: 0.18, fontSize: 7.6, color: MUTED });
  sy += 0.36;
});
T(s3, "Also shipping: Tan (AION V genuine-leather option) · Suede grey (AION RT zero-pressure seats) · Black faux leather, the standard fit almost everywhere.",
  { x: a2x, y: sy + 0.04, w: a2w, h: 0.28, fontSize: 7.8, color: MUTED, lineSpacingMultiple: 1.1 });
box(s3, { x: a2x, y: sy + 0.38, w: a2w, h: RA + RAH - sy - 0.38, fill: { color: PANEL } });
micro(s3, a2x + 0.24, sy + 0.54, a2w - 0.48, "THE READ", AION);
T(s3, "AION has turned colour into the product. Three named themes per car means a model-year change can be a CMF change — cheap, fast and visible in a showroom photograph. Trumpchi has no equivalent naming discipline and loses that lever entirely.",
  { x: a2x + 0.24, y: sy + 0.72, w: a2w - 0.48, h: 0.52, fontSize: 8.4, color: INK,
    lineSpacingMultiple: 1.12 });

/* ---- A3 comfort ladder ---- */
const a3x = 25.9, a3w = 10.4;
heading(s3, a3x, RA, a3w, "COMFORT", "What each price step buys");
const LAD = [
  { p: "¥70–110k", m: "AION UT", c: AION,
    t: "Fixed seats, manual recline. The differentiator is a flat-fold bed across the whole cabin, not adjustment." },
  { p: "¥110–130k", m: "AION N60", c: AION,
    t: "Zero-gravity co-pilot seat standard. Front heating, ventilation, massage and memory. Rear backrest 117–137°." },
  { p: "¥115–160k", m: "AION i60", c: AION,
    t: "“Eight-layer comfort sofa” fronts with 8-point massage; dual-tone split and 32-colour ambient." },
  { p: "¥170–250k", m: "TRUMPCHI XIANGWANG S7", c: TRU,
    t: "Rear reclines to 137° on a zero-gravity cloud leg rest. Massage in six modes at three intensities. 17.3\" ceiling screen." },
  { p: "¥250k +", m: "HYPTEC HL · A800", c: PREM,
    t: "2+2+2, second-row captain chairs, 18-point massage, 12-way power, zero-gravity at 127.5°. At the A800: 27\" W-HUD, 6,536 mm ambient run, ANC, L3 on the highway." }
];
let ly = RA + 0.56;
LAD.forEach((l, i) => {
  rect(s3, { x: a3x, y: ly + 0.03, w: 0.08, h: 0.38, fill: { color: l.c } });
  T(s3, l.p, { x: a3x + 0.22, y: ly, w: 2.4, h: 0.20, fontSize: 9.5, bold: true, color: INK });
  T(s3, l.m, { x: a3x + 2.7, y: ly + 0.025, w: a3w - 2.7, h: 0.18, fontSize: 7.8, bold: true,
               color: l.c, align: "right" });
  T(s3, l.t, { x: a3x + 0.22, y: ly + 0.23, w: a3w - 0.22, h: 0.30, fontSize: 8.4, color: INK2,
               lineSpacingMultiple: 1.1 });
  ly += 0.52;
  if (i < LAD.length - 1) rect(s3, { x: a3x, y: ly - 0.07, w: a3w, h: 0.006, fill: { color: LINE } });
});
box(s3, { x: a3x, y: ly + 0.06, w: a3w, h: RA + RAH - ly - 0.06, fill: { color: INK } });
micro(s3, a3x + 0.26, ly + 0.22, a3w - 0.52, "THE LINE THAT MOVED", "6FA8FF");
T(s3, "Massage and zero-gravity seating crossed below ¥130k in April 2026.",
  { x: a3x + 0.26, y: ly + 0.38, w: a3w - 0.52, h: 0.24, fontSize: 12, bold: true, color: WHITE });
T(s3, "A zero-gravity front passenger seat was a ¥250k feature until the AION N60. It now ships on a ¥109,800 compact SUV that also carries LiDAR as standard — so every comfort assumption below ¥150k needs re-baselining against that car.",
  { x: a3x + 0.26, y: ly + 0.66, w: a3w - 0.52, h: 0.46, fontSize: 8.4, color: "9CA2AA",
    lineSpacingMultiple: 1.12 });

/* ---- A4 screen strategy ---- */
const a4x = 36.7, a4w = 12.7;
heading(s3, a4x, RA, a4w, "ARCHITECTURE", "Screen strategy, counted");
T(s3, "Sum of stated display diagonals per car, including head-up, ceiling and armrest screens. Read it as inventory, not as quality.",
  { x: a4x, y: RA + 0.50, w: a4w, h: 0.30, fontSize: 8, color: MUTED, lineSpacingMultiple: 1.1 });
const LEAGUE = [
  { n: "CHANGAN DEEPAL L06", v: 65.6, c: OK, d: '15.6" adaptive + 50" AR-HUD' },
  { n: "TRUMPCHI E9", v: 64.8, c: TRU, d: '12.3 + 14.6 + 12.3 + 15.6" ceiling + 2×5" armrest' },
  { n: "HYPTEC A800", v: 51.85, c: PREM, d: '10.25 + 14.6 + 27" W-HUD' },
  { n: "AION UT / RT / V", v: 23.4, c: AION, d: '8.8" cluster + 14.6" centre' },
  { n: "TRUMPCHI XIANGWANG S7", v: 17.3, c: TRU, d: '17.3" ceiling (dash sizes not published)' },
  { n: "AION N60", v: 15.6, c: AION, d: '15.6" 2.5K, single tile' },
  { n: "TRUMPCHI GS3 EMZOOM", v: 12.3, c: TRU, d: '12.3" centre only' }
];
const barX = a4x + 4.9, barW = a4w - 4.9 - 4.5, LMAX = 70;
let gy2 = RA + 0.90;
LEAGUE.forEach(l => {
  T(s3, l.n, { x: a4x, y: gy2, w: 4.7, h: 0.18, fontSize: 8.2, bold: true, color: l.c === OK ? OK : INK });
  rect(s3, { x: barX, y: gy2 + 0.02, w: barW * (l.v / LMAX), h: 0.15, fill: { color: l.c } });
  T(s3, l.v.toFixed(1) + '"', { x: barX + barW * (l.v / LMAX) + 0.08, y: gy2 + 0.015, w: 0.9, h: 0.16,
    fontSize: 7.4, bold: true, color: l.c });
  T(s3, l.d, { x: a4x + a4w - 4.4, y: gy2 + 0.015, w: 4.4, h: 0.18, fontSize: 7.2, color: MUTED,
               align: "right" });
  gy2 += 0.34;
});
box(s3, { x: a4x, y: gy2 + 0.10, w: a4w, h: RA + RAH - gy2 - 0.10, fill: { color: PANEL } });
micro(s3, a4x + 0.26, gy2 + 0.26, a4w - 0.52, "TWO ANSWERS TO THE SAME BRIEF", OK);
T(s3, "GAC adds displays — up to seven-screen collaboration in the M8, four physical panels in the E9. Changan's Deepal deletes the cluster and puts the area into projection instead. Both reach a similar total; only one of them keeps the driver's eyes up. That difference is a design position worth defending, not a cost saving to be traded away.",
  { x: a4x + 0.26, y: gy2 + 0.44, w: a4w - 0.52, h: 0.80, fontSize: 8.4, color: INK,
    lineSpacingMultiple: 1.12 });

/* ---- B1 personas ---- */
const b1x = M, b1w = 28.0;
heading(s3, b1x, RB, b1w, "OCCUPANTS", "The five characters GAC designs for");
const PERS = [
  { n: "LIN", a: "24 · Guangzhou · first car", b: "¥70–110k", seg: "ENTRY", c: AION,
    cars: "AION UT · AION Y PLUS",
    touch: "The door card colour, from the pavement.",
    win: "Cream or dusky pink carried onto the dash. A cabin that folds flat for a weekend. Phone casting that works first time.",
    lose: "Hard shiny plastic where the elbow lands." },
  { n: "WEI", a: "31 · new parent", b: "¥110–160k", seg: "MID", c: AION,
    cars: "AION N60 · AION i60",
    touch: "The rear bench and the ISOFIX anchor.",
    win: "117–137° rear recline, 35 stowage points, wipe-clean vegan leather, a 2.38 m² roof over the child seat.",
    lose: "Climate buried three menus deep with a baby crying." },
  { n: "ZHAO", a: "38 · small business owner", b: "¥170–250k", seg: "UPPER-MID", c: TRU,
    cars: "TRUMPCHI XIANGWANG S7 · S9",
    touch: "The second-row leg rest, before the driver's seat.",
    win: "137° recline, six-mode massage, a 17.3\" ceiling screen for the children, second-row climate control.",
    lose: "A third row an adult cannot sit in." },
  { n: "CHEN", a: "46 · chauffeur-driven", b: "¥250–400k", seg: "LUXURY", c: TRU,
    cars: "TRUMPCHI M8 XIANGWANG · E9 · HYPTEC HL",
    touch: "The 5\" pad in the armrest.",
    win: "2+2+2, 18-point massage, zero-gravity at 127.5°, welcome projection, silence.",
    lose: "Having to lean forward to reach anything." },
  { n: "YU", a: "33 · technology-first", b: "¥350k +", seg: "FLAGSHIP", c: PREM,
    cars: "HYPTEC A800 · AISTALAND GT7 · AION RAY 7",
    touch: "The HUD horizon, before the seat.",
    win: "27\" W-HUD, wraparound console, a 6,536 mm light run, Huawei continuity from phone to car, L3 on the highway.",
    lose: "A cabin that reads the same as the ¥130k car one brand down." }
];
const pw = (b1w - 4 * 0.30) / 5;
PERS.forEach((p, i) => {
  const x = b1x + i * (pw + 0.30), y = RB + 0.56, h = RBH - 0.56;
  box(s3, { x, y, w: pw, h, fill: { color: PANEL } });
  const px = x + 0.26, iw = pw - 0.52;
  T(s3, p.n, { x: px, y: y + 0.20, w: iw - 1.5, h: 0.32, fontSize: 17, bold: true, color: p.c });
  T(s3, p.b, { x: px + iw - 1.6, y: y + 0.28, w: 1.6, h: 0.20, fontSize: 8.6, bold: true,
               color: INK, align: "right" });
  T(s3, p.a, { x: px, y: y + 0.56, w: iw, h: 0.19, fontSize: 8, color: MUTED });
  chip(s3, px, y + 0.82, p.seg, SEG[p.seg]);
  rect(s3, { x: px, y: y + 1.14, w: iw, h: 0.006, fill: { color: LINE } });
  T(s3, p.cars, { x: px, y: y + 1.26, w: iw, h: 0.34, fontSize: 8.2, bold: true, color: INK,
                  lineSpacingMultiple: 1.08 });
  let yy = y + 1.70;
  spec(s3, px, yy, iw, "TOUCHES FIRST", p.touch, 0.36, 8.4); yy += 0.66;
  spec(s3, px, yy, iw, "WHAT WINS THEM", p.win, 0.90, 8.4); yy += 1.18;
  spec(s3, px, yy, iw, "WHAT THEY WILL NOT FORGIVE", p.lose, 0.50, 8.4);
});

/* ---- B2 gap + actions ---- */
const b2x = 29.0, b2w = 20.4;
heading(s3, b2x, RB, b2w, "OUR POSITION", "GAC against Changan — and what we do about it");
const COLS = [3.2, 4.7, 4.5, 8.0];
let gy = RB + 0.58;
micro(s3, b2x, gy, COLS[0], "DIMENSION", FAINT);
micro(s3, b2x + COLS[0], gy, COLS[1], "GAC · AION + TRUMPCHI + HYPTEC", TRU);
micro(s3, b2x + COLS[0] + COLS[1], gy, COLS[2], "CHANGAN · NEVO + DEEPAL + AVATR", OK);
micro(s3, b2x + COLS[0] + COLS[1] + COLS[2], gy, COLS[3], "READ", FAINT);
gy += 0.20;
rect(s3, { x: b2x, y: gy, w: b2w, h: 0.008, fill: { color: LINE } });
gy += 0.10;
const VERD = { ahead: OK, behind: TRU, level: MUTED };
const GAPTBL = [
  ["Centre display", '14.6" floor; 15.6" 2.5K on the newest (N60)', 'Nevo 15.7" 2.5K, Q05 15.6"; Deepal L06 15.6" adaptive', "Parity. Screen size has stopped being a differentiator.", "level"],
  ["Cluster", 'Retained at 8.8–12.3" on almost everything', "Nevo keeps 9.8–10.17\"; Deepal L06 deletes it", "We are ahead on deletion. Commit to it as a design position, not a cost saving.", "ahead"],
  ["Head-up display", '27" W-HUD, flagship only (A800)', '50" AR-HUD already at Deepal L06, mid-range', "Our clearest lead. Push AR-HUD down into Nevo before Hyptec spreads theirs.", "ahead"],
  ["Ambient light", "32 colours standard; 6,536 mm run at flagship", "Present, not merchandised as a number", "They made ambient a spec-sheet figure. Answer with a named light architecture, not a bigger number.", "behind"],
  ["Seat comfort", "Zero-gravity and massage below ¥130k; 18-point at premium", "Strong at Avatr, thinner below ¥150k", "The fastest-moving line on this board. Re-baseline the comfort budget now.", "behind"],
  ["Cabin OS", "ADiGO 6.0 on Aion; Huawei on Trumpchi, Hyptec, Aistaland", "Huawei on Avatr; MediaTek MT8676 across Nevo", "Both groups run dual-track. Our silicon choice is the cost lever — protect it.", "level"],
  ["CMF", "Three named themes per car, refreshed per model year", "Colourways specified, rarely named or storied", "They sell colour as product. Ours needs names, a story and a launch moment.", "behind"]
];
GAPTBL.forEach((g, i) => {
  const rh = 0.34;
  if (i % 2 === 0) rect(s3, { x: b2x - 0.10, y: gy - 0.04, w: b2w + 0.20, h: rh + 0.02,
                              fill: { color: "FAFAF8" } });
  T(s3, g[0], { x: b2x, y: gy, w: COLS[0] - 0.2, h: 0.34, fontSize: 8.4, bold: true, color: INK,
                lineSpacingMultiple: 1.05 });
  T(s3, g[1], { x: b2x + COLS[0], y: gy, w: COLS[1] - 0.2, h: 0.34, fontSize: 7.8, color: INK2,
                lineSpacingMultiple: 1.06 });
  T(s3, g[2], { x: b2x + COLS[0] + COLS[1], y: gy, w: COLS[2] - 0.2, h: 0.34, fontSize: 7.8,
                color: INK2, lineSpacingMultiple: 1.06 });
  T(s3, g[3], { x: b2x + COLS[0] + COLS[1] + COLS[2], y: gy, w: COLS[3], h: 0.34, fontSize: 7.8,
                color: VERD[g[4]], bold: g[4] !== "level", lineSpacingMultiple: 1.06 });
  gy += rh;
});

const actY = gy + 0.16;
box(s3, { x: b2x, y: actY, w: b2w, h: RB + RBH - actY, fill: { color: INK } });
micro(s3, b2x + 0.30, actY + 0.22, b2w - 0.60, "SIX THINGS TO PUT IN THE NEXT INTERIOR BRIEF", "6FA8FF");
const ACT = [
  "Name the colourways. Three named themes per car is a cheap, visible model-year lever we are not using.",
  "Re-baseline comfort under ¥150k. Zero-gravity and massage crossed below ¥130k in April 2026.",
  "Defend the HUD lead — get AR-HUD out of Deepal L06 and into the Nevo Q-series before Hyptec spreads its 27\" W-HUD.",
  "Above ¥170k, design the second row first. Every Trumpchi over that line is sold on recline angle, leg rest and rear screen.",
  "Do not chase screen count. Ours is one adaptive screen plus projection — and the switchgear GAC deleted.",
  "Get a rear ceiling screen into the family plan. 15.6–17.3\" ceiling displays are now standard above ¥170k."
];
const acw = (b2w - 0.60 - 2 * 0.40) / 3;
ACT.forEach((a, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const ax = b2x + 0.30 + col * (acw + 0.40), ay = actY + 0.46 + row * 0.46;
  T(s3, String(i + 1), { x: ax, y: ay, w: 0.26, h: 0.20, fontSize: 9, bold: true, color: "6FA8FF" });
  T(s3, a, { x: ax + 0.28, y: ay, w: acw - 0.28, h: 0.42, fontSize: 8.4, color: "D6D8DC",
             lineSpacingMultiple: 1.1 });
});

footer(s3, "Changan reference points: Nevo 15.7\" 2.5K + 9.8\" cluster on MediaTek MT8676; Nevo Q05 15.6\" 2.5K + 10.17\" cluster; Nevo Q06 800V / 6C; Deepal S07 single-screen layout; Deepal L06 15.6\" adaptive “Sunflower” screen with 50\" AR-HUD; Avatr on Huawei.   ·   Sources as slides 01–02, plus CnEVPost, CarNewsChina, Gasgoo, MarkLines and 36Kr reporting on Auto China 2026, Panyu Action and GAC interim results. Public-domain, unaudited figures — verify against a benchmark teardown before any of it enters a specification.");

pres.writeFile({ fileName: "GAC_AION_Interior_Benchmark.pptx" })
  .then(f => console.log("written:", f));
