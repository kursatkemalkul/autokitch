// GAC / AION interior benchmark - 50" x 12.38", 3 slides, dark luxury board
// Image frames are left empty on purpose.
const pptxgen = require("pptxgenjs");

const W = 50, H = 12.38;
const M = 0.6;
const CW = W - 2 * M;

/* dark luxury palette */
const BG     = "0A0B0D";
const FRAME  = "14161A";
const FRAMEL = "262A30";
const HAIR   = "23262B";
const TEXT   = "F4F2EE";
const SUB    = "9DA1A8";
const FAINT  = "5E636A";
const BODY   = "C6C9CE";
const AION   = "5C93FF";
const TRU    = "E07B62";
const GOLD   = "C4AC7A";

const SEG = {
  ENTRY:       "6E737A",
  MID:         "8B9098",
  "UPPER-MID": "A9AEB6",
  PREMIUM:     "C4AC7A",
  LUXURY:      "D4BE8E",
  FLAGSHIP:    "F0E4C6"
};

const FS = "Arial";      // body
const FD = "Cambria";    // display

const pres = new pptxgen();
pres.defineLayout({ name: "BOARD", width: W, height: H });
pres.layout = "BOARD";
pres.author = "Interior Design";
pres.title = "GAC x AION Interior Benchmark";

/* ---------- helpers ---------- */
function T(s, t, o) {
  s.addText(t, Object.assign({ isTextBox: true, margin: 0, fontFace: FS, valign: "top" }, o));
}
function rect(s, o) {
  s.addShape(pres.ShapeType.rect, Object.assign({ line: { width: 0 } }, o));
}
function micro(s, x, y, w, t, c, fs) {
  T(s, t, { x, y, w, h: 0.13, fontSize: fs || 6.8, bold: true, charSpacing: 1.4,
            color: c || FAINT });
}
function hairline(s, x, y, w, c) {
  rect(s, { x, y, w, h: 0.014, fill: { color: c || HAIR } });
}
/* outlined chip - reads as metal on black */
function chip(s, x, y, t, c, align) {
  const w = 0.075 * t.length + 0.30;
  const xx = align === "right" ? x - w : x;
  s.addShape(pres.ShapeType.roundRect, { x: xx, y, w, h: 0.21, rectRadius: 0.10,
    fill: { color: BG }, line: { color: c, width: 0.75 } });
  T(s, t, { x: xx, y: y + 0.045, w, h: 0.15, fontSize: 6.6, bold: true, charSpacing: 1.0,
            color: c, align: "center" });
  return w;
}
/* empty image frame with crop marks */
function frame(s, x, y, w, h, label, want) {
  rect(s, { x, y, w, h, fill: { color: FRAME }, line: { color: FRAMEL, width: 0.75 } });
  const t = 0.26;
  [[x, y, 1, 1], [x + w, y, -1, 1], [x, y + h, 1, -1], [x + w, y + h, -1, -1]].forEach(c => {
    rect(s, { x: c[2] > 0 ? c[0] : c[0] - t, y: c[3] > 0 ? c[1] : c[1] - 0.004,
              w: t, h: 0.004, fill: { color: "3A3F47" } });
    rect(s, { x: c[2] > 0 ? c[0] : c[0] - 0.004, y: c[3] > 0 ? c[1] : c[1] - t,
              w: 0.004, h: t, fill: { color: "3A3F47" } });
  });
  micro(s, x, y + h / 2 - 0.26, w, label, "525862", 7.4);
  T(s, want, { x: x + 0.34, y: y + h / 2 - 0.06, w: w - 0.68, h: 0.36, fontSize: 7.6,
               color: "4A505A", align: "center", italic: true, lineSpacingMultiple: 1.12 });
}
function slideHeader(s, num, kicker, title, sub, read, readC) {
  rect(s, { x: 0, y: 0, w: W, h: H, fill: { color: BG } });
  T(s, num, { x: M, y: 0.40, w: 1.4, h: 0.40, fontSize: 26, bold: true, fontFace: FD, color: "343941" });
  micro(s, M + 0.72, 0.50, 16, kicker, FAINT);
  T(s, title, { x: M + 0.70, y: 0.66, w: 30, h: 0.60, fontSize: 32, fontFace: FD, color: TEXT });
  T(s, sub, { x: M + 0.72, y: 1.30, w: 30, h: 0.24, fontSize: 9.6, color: SUB });
  T(s, read, { x: M + 0.72, y: 1.56, w: 30, h: 0.24, fontSize: 9.6, italic: true, color: readC });
}
function kpi(s, x, y, w, v, l, c) {
  T(s, v, { x, y, w, h: 0.44, fontSize: 26, fontFace: FD, color: c || TEXT });
  T(s, l, { x, y: y + 0.48, w, h: 0.38, fontSize: 7.6, color: FAINT, lineSpacingMultiple: 1.1 });
}
function footer(s, t) {
  hairline(s, M, H - 0.74, CW);
  T(s, t, { x: M, y: H - 0.60, w: CW, h: 0.32, fontSize: 7, color: "494E55",
            lineSpacingMultiple: 1.14 });
}

/* ---------- model column ---------- */
const NCOL = 7, GAPC = 0.34;
const COLW = (CW - (NCOL - 1) * GAPC) / NCOL;
const colX = i => M + i * (COLW + GAPC);

const TOP    = 2.14;
const FR_H   = 3.26;              // 2:1 cinematic crop
const FR1_Y  = TOP + 0.78;
const FR2_Y  = FR1_Y + FR_H + 0.16;
const SPEC_Y = FR2_Y + FR_H + 0.20;

function modelColumn(s, i, d) {
  const x = colX(i);
  T(s, d.name, { x, y: TOP, w: COLW - 1.5, h: 0.30, fontSize: 13, bold: true, charSpacing: 0.7,
                 color: TEXT });
  chip(s, x + COLW, TOP + 0.03, d.seg, SEG[d.seg], "right");
  T(s, d.meta, { x, y: TOP + 0.34, w: COLW, h: 0.20, fontSize: 7.6, color: SUB });
  hairline(s, x, TOP + 0.64, COLW, d.accent);

  frame(s, x, FR1_Y, COLW, FR_H, "DASHBOARD / IP", d.shot1);
  frame(s, x, FR2_Y, COLW, FR_H, "CABIN DETAIL", d.shot2);

  let y = SPEC_Y;
  [["SCREENS", d.screens], ["MATERIAL · COLOUR", d.cmf],
   ["SEAT · COMFORT", d.seat], ["FOR WHOM", d.who]].forEach(r => {
    micro(s, x, y, COLW, r[0], FAINT);
    T(s, r[1], { x, y: y + 0.14, w: COLW, h: 0.28, fontSize: 8, color: BODY,
                 lineSpacingMultiple: 1.08 });
    y += 0.42;
  });
}

/* =========================================================================
   SLIDE 1 — AION
   ========================================================================= */
const s1 = pres.addSlide();
slideHeader(s1, "01", "INTERIOR BENCHMARK · GAC GROUP · SEPTEMBER 2026",
  "AION",
  "Seven battery-electric cabins on sale in China. Prices are MSRP bands in RMB.",
  "One big tile, soft surfaces, named colour. Colour is the product.", AION);

kpi(s1, 34.6, 0.60, 4.6, "74,100", "AION retail, Q1 2026\n+57.3% year on year", AION);
kpi(s1, 39.6, 0.60, 4.6, '14.6"', "the centre-screen floor\nright across the range", TEXT);
kpi(s1, 44.6, 0.60, 4.8, "32", "ambient colours, standard\non almost everything", TEXT);

const AIONS = [
  { name: "AION UT", seg: "ENTRY", accent: AION,
    meta: "B-segment hatch · BEV · ≈¥70–105k · 4,270 mm",
    shot1: "IP straight on — cream or dusky pink carried onto the dash",
    shot2: "door card and seat facing, or the flat-fold bed mode",
    screens: '14.6" centre tile + 8.8" driver cluster. Climate, mirrors and driver aids all sit in the tile.',
    cmf: "PVC in cream or dusky pink, carried onto doors and dash. Padded dash top, soft-touch to the rear doors.",
    seat: "Manual adjustment, no comfort electronics. Every seat folds to a full-length flat bed.",
    who: "First-car urban buyer, 22–28. Chooses the cabin before the car." },

  { name: "AION RT", seg: "MID", accent: AION,
    meta: "Mid-size fastback · BEV · ¥85.8–123.8k · 4,865 / 2,775 mm",
    shot1: "IP straight on — single horizontal plane, minimal switchgear",
    shot2: "suede seat facing, close up",
    screens: '14.6" centre + 8.8" cluster. Function-first surfacing; the dash reads as one plane.',
    cmf: "100% leather-wrap on every high-contact surface. Suede-finished seats. Colourway not named by the brand.",
    seat: "Suede “zero-pressure” seats. Rear knee room quoted at two fists behind a 175 cm driver.",
    who: "Value-led tech buyer cross-shopping a Model 3. Wants sparse, not luxurious." },

  { name: "AION Y PLUS", seg: "MID", accent: AION,
    meta: "Compact SUV · BEV · ¥99.8–153.8k · CLTC up to 610 km",
    shot1: "IP with the screen rotated to portrait, then landscape",
    shot2: "green cabin theme across seats and doors",
    screens: '14.6" rotating centre screen — portrait or landscape on demand.',
    cmf: "Vegan leather. The green theme is briefed as “healing” relief from urban stress — colour as message.",
    seat: "Comfort-led, no massage. Wireless pad that holds a phone through a corner.",
    who: "Young family, first EV. Space per yuan is the pitch; colour closes it." },

  { name: "AION N60", seg: "MID", accent: AION,
    meta: "Compact SUV · BEV 610 km · ¥109.8–129.8k · April 2026",
    shot1: "IP — 15.6\" tile with no cluster behind the wheel",
    shot2: "the three named themes side by side; zero-gravity seat reclined",
    screens: '15.6" 2.5K single tile on ADiGO 6.0 — AI voice, Huawei Nebula, iOS and Android casting. Cluster deleted.',
    cmf: "Three named themes: Soft Light White, Caramel Warm Velvet, Morning Mist Cool Grey. 2.38 m² roof, 35 stowage points.",
    seat: "Zero-gravity front passenger seat standard. Front heat, ventilation, massage, memory. Rear 117–137°.",
    who: "Young family. Priced at entry, specified like a mid — with LiDAR standard." },

  { name: "AION i60", seg: "MID", accent: AION,
    meta: "Compact crossover · BEV 650 km / EREV 1,240 km · from ≈¥115.8k",
    shot1: "IP — dual-tone split across the fascia",
    shot2: "front seat cushion structure; ambient lighting at night",
    screens: '14.6" on ADiGO 5.0, with GSD highway navigation assist and smart parking.',
    cmf: "Dual-tone split cabin, 32-colour ambient lighting. Colourway names not published.",
    seat: "“Eight-layer comfort sofa” fronts — 8-point massage, ventilation, heating, memory.",
    who: "Range-anxious family buyer. Two powertrains, one identical cabin." },

  { name: "AION V", seg: "UPPER-MID", accent: AION,
    meta: "Mid-size SUV · BEV · 2nd generation 2024 · the export flagship",
    shot1: "IP — black standard trim",
    shot2: "the cream or tan leather option, same angle",
    screens: '14.6" centre runs climate, mirrors and ADAS settings; 8.8" cluster retained.',
    cmf: "Black faux leather standard; genuine leather in cream or tan for a small premium. 32-colour ambient standard.",
    seat: "Comfort-led. Nine-speaker 360 W audio, two-metre-plus panoramic roof with powered blind.",
    who: "The car GAC exports — the cabin that faces European and Australian press." },

  { name: "AION RAY 7", seg: "PREMIUM", accent: AION,
    meta: "Mid-large fastback · BEV ≈700 km · expected ¥200–250k · unveiled 19 Aug 2026",
    shot1: "any interior frame from the Chengdu unveil",
    shot2: "the new illuminated AION logo in the star-ring light bar",
    screens: "Not disclosed at the unveil — the single biggest unknown on this board.",
    cmf: "Not published. First interior of the post-rebrand AION design language.",
    seat: "Not published.",
    who: "Launch model of the new Ray series for young buyers. Huawei DriveONE 180 kW." }
];
AIONS.forEach((d, i) => modelColumn(s1, i, d));

footer(s1, "Image frames are intentionally empty — drop press photography in and the grid holds.   ·   Sources: GAC / AION press material and Auto China 2026 releases; CnEVPost; CarNewsChina; Gasgoo; BitAuto; CarExpert, Chasing Cars, What Car?, Electrifying, RACV, zecar. Compiled September 2026. Prices are China MSRP bands and move with promotion; fields marked “not published” were not found in a primary or reputable secondary source.");

/* =========================================================================
   SLIDE 2 — TRUMPCHI + HYPTEC
   ========================================================================= */
const s2 = pres.addSlide();
slideHeader(s2, "02", "INTERIOR BENCHMARK · GAC GROUP · SEPTEMBER 2026",
  "TRUMPCHI  ·  HYPTEC",
  "Six Trumpchi cabins and the Hyptec flagship. Prices are MSRP bands in RMB.",
  "Comfort you can count — recline angle, massage modes, screens per seat.", TRU);

kpi(s2, 34.6, 0.60, 4.6, "92,100", "TRUMPCHI retail, Q1 2026\n+33.1% year on year", TRU);
kpi(s2, 39.6, 0.60, 4.6, "137°", "rear recline already at\n¥170k (Xiangwang S7)", TEXT);
kpi(s2, 44.6, 0.60, 4.8, "6,536", "mm of ambient light run\nin the Hyptec A800", GOLD);

const TRUS = [
  { name: "GS3 EMZOOM", seg: "ENTRY", accent: TRU,
    meta: "Small SUV · 1.5T petrol · the brand's youth entry point",
    shot1: "driver-side IP",
    shot2: "sport seat bolster and ambient lighting",
    screens: '12.3" centre screen — the smallest display anywhere in the group.',
    cmf: "32-colour ambient even at the entry point. Driver-focused, sport-flavoured trim.",
    seat: "Sport-bolstered fronts. No comfort electronics at this level.",
    who: "Under-30 first-car buyer who still wants an engine." },

  { name: "GS8", seg: "MID", accent: TRU,
    meta: "Large 7-seat SUV · 2.0T 252 hp / hybrid · from ≈¥159.8k",
    shot1: "IP and centre console",
    shot2: "second and third rows from the tailgate, folded and upright",
    screens: "Diagonals not published in English-language sources — measure on the car. Conventional twin-display layout.",
    cmf: "The classic family flagship the whole brand is now being rebuilt around.",
    seat: "2+3+2. The second and third rows make the sale.",
    who: "Three-generation family. Bought on seat count and boot space." },

  { name: "XIANGWANG S7", seg: "UPPER-MID", accent: TRU,
    meta: "Mid-size PHEV SUV · Mar 2025 · guide ¥209.8–249.8k · 4.90 m, five seats",
    shot1: "IP — Snapdragon 8295P cockpit on ADiGO 6.0",
    shot2: "rear seat reclined, leg rest out, ceiling screen down",
    screens: 'ADiGO 6.0 on Snapdragon 8295P, plus a 17.3" ceiling-mounted screen that folds down for the rear.',
    cmf: "Warm, light-toned luxury trim. 4.90 m long but only five seats — the space goes into row two.",
    seat: "Ventilation, heating and massage: six modes at three intensities. Rear reclines to 137° on a zero-gravity leg rest.",
    who: "A family SUV sold on the bench, not the driver's seat." },

  { name: "XIANGWANG S9", seg: "PREMIUM", accent: TRU,
    meta: "Full-size SUV · five- or six-seat · Huawei HarmonySpace cabin",
    shot1: 'IP — 12.3" cluster and the HarmonySpace centre screen',
    shot2: "six-seat layout, second-row captain chairs with their own console",
    screens: 'Three screens in total, 12.3" cluster behind the wheel. Huawei HarmonySpace is the backbone; other diagonals not published.',
    cmf: "Positioned above the S7. Five or six seats changes the whole second-row architecture.",
    seat: "Six-seat form gets captain chairs that recline and carry their own climate and media controls.",
    who: "The GS8 owner trading up, buying the Huawei cabin badge." },

  { name: "E9", seg: "LUXURY", accent: GOLD,
    meta: "Luxury PHEV MPV · 2023 · from ≈US$47k · the Alphard answer",
    shot1: 'IP — 14.6" centre, 12.3" cluster and 12.3" passenger screen',
    shot2: "second-row armrest touch pad; ceiling screen deployed",
    screens: 'Four displays: 14.6" centre, 12.3" cluster, 12.3" front passenger, 15.6" in the ceiling.',
    cmf: "Light champagne cabin. Control physically moves out of the driver's seat into row two.",
    seat: "2+2+3 with captain chairs, each carrying its own 5\" armrest touch pad to drive that seat.",
    who: "Chauffeur-driven business use, cross-shopped against the Toyota Alphard." },

  { name: "M8 XIANGWANG", seg: "LUXURY", accent: GOLD,
    meta: "Full-size MPV · 2026 model year · the brand's ceiling",
    shot1: 'IP — HarmonySpace 5 on the 15.6" centre screen',
    shot2: "welcome projection at the door; third row powered flat",
    screens: 'HarmonySpace 5 on a 15.6" centre screen, running seven-screen collaboration across the cabin.',
    cmf: "Cabin grades sold by name — Qiankun Max Luxury, Qiankun Ultra First-Class — with welcome projection at the door.",
    seat: "Power-adjustable third row in 2+2+3. Ceremony is engineered, not implied.",
    who: "Business travel where the owner sits in row two." },

  { name: "HYPTEC A800", seg: "FLAGSHIP", accent: GOLD,
    meta: "Flagship EREV sedan · pre-order Dec 2025 · the group's ceiling",
    shot1: "wraparound console and the 27\" W-HUD in the driver's eye line",
    shot2: "the 6,536 mm ambient light run at night",
    screens: '“Interstellar Cockpit”: 10.25" cluster + 14.6" centre + 27" W-HUD. HarmonySpace 5 on a flagship Qualcomm chip, 0.3 s response.',
    cmf: "A 6,536 mm ambient light run — claimed the longest in the world. Seamless wraparound surfacing, active noise cancellation.",
    seat: "Eight-way power front seats with three massage modes.",
    who: "Premium technology early adopter. Huawei Qiankun ADS 4 Ultra, L3 on the highway." }
];
TRUS.forEach((d, i) => modelColumn(s2, i, d));

footer(s2, "Image frames are intentionally empty — drop press photography in and the grid holds.   ·   Sources: GAC / Trumpchi / Hyptec press material; Auto China 2026 and Auto Guangzhou releases; CarNewsChina; BitAuto; Gasgoo; CnEVPost. Compiled September 2026. Prices are China MSRP bands; fields marked “not published” were not found in a primary or reputable secondary source.");

/* =========================================================================
   SLIDE 3 — CMF + comfort ladder
   ========================================================================= */
const s3 = pres.addSlide();
slideHeader(s3, "03", "INTERIOR BENCHMARK · GAC GROUP · SEPTEMBER 2026",
  "Colour  ·  Comfort",
  "What GAC actually ships in the cabin, and what each price step buys.",
  "Two levers they are pulling and we are not.", GOLD);

const BY = 2.14, BH = 7.30;

/* --- CMF --- */
const cx = M, cw = 23.6;
micro(s3, cx, BY, cw, "COLOURWAYS ACTUALLY ON SALE", FAINT);
T(s3, "Every swatch is a shipping option, not a show car. AION names its interiors; Trumpchi names its seats.",
  { x: cx, y: BY + 0.20, w: cw, h: 0.22, fontSize: 8.6, color: SUB });

const SW = [
  { h: "F2EFE9", n: "SOFT LIGHT WHITE",      m: "AION N60 · named theme" },
  { h: "9A6A45", n: "CARAMEL WARM VELVET",   m: "AION N60 · named theme" },
  { h: "9BA1A4", n: "MORNING MIST COOL GREY",m: "AION N60 · named theme" },
  { h: "E8DFCB", n: "CREAM",                 m: "AION UT seats, doors, dash · AION V option" },
  { h: "CBA0A2", n: "DUSKY PINK",            m: "AION UT · the boldest colour in the range" },
  { h: "8FA98A", n: "HEALING GREEN",         m: "AION Y Plus · briefed as urban stress relief" },
  { h: "A9714A", n: "TAN",                   m: "AION V · genuine-leather option" },
  { h: "5E6470", n: "SUEDE GREY",            m: "AION RT · zero-pressure seat finish" },
  { h: "24262A", n: "BLACK FAUX LEATHER",    m: "AION V · the standard fit almost everywhere" }
];
const swW = (cw - 2 * 0.40) / 3, swTop = BY + 0.62, swRow = 2.24;
SW.forEach((s_, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const x = cx + col * (swW + 0.40), y = swTop + row * swRow;
  rect(s3, { x, y, w: swW, h: 1.34, fill: { color: s_.h },
             line: { color: s_.h === "24262A" ? "3A3F47" : s_.h, width: 0.75 } });
  T(s3, s_.n, { x, y: y + 1.46, w: swW, h: 0.20, fontSize: 9, bold: true, charSpacing: 0.9,
                color: TEXT });
  T(s3, s_.m, { x, y: y + 1.70, w: swW, h: 0.30, fontSize: 7.8, color: FAINT,
                lineSpacingMultiple: 1.1 });
});

/* --- comfort ladder --- */
const lx = 25.4, lw = W - M - 25.4;
micro(s3, lx, BY, lw, "WHAT EACH PRICE STEP BUYS", FAINT);
T(s3, "Read off the shipping specification, not the brochure copy.",
  { x: lx, y: BY + 0.20, w: lw, h: 0.22, fontSize: 8.6, color: SUB });

const LAD = [
  { p: "¥70 – 110k", m: "AION UT", c: AION,
    t: "Fixed seats, manual recline. The differentiator is a flat-fold bed across the whole cabin, not adjustment." },
  { p: "¥110 – 130k", m: "AION N60", c: AION,
    t: "Zero-gravity co-pilot seat standard. Front heating, ventilation, massage and memory. Rear backrest 117–137°." },
  { p: "¥115 – 160k", m: "AION i60", c: AION,
    t: "“Eight-layer comfort sofa” fronts with 8-point massage; dual-tone split and 32-colour ambient." },
  { p: "¥170 – 250k", m: "TRUMPCHI XIANGWANG S7", c: TRU,
    t: "Rear reclines to 137° on a zero-gravity cloud leg rest. Massage in six modes at three intensities. 17.3\" ceiling screen." },
  { p: "¥250k +", m: "HYPTEC HL  ·  A800", c: GOLD,
    t: "2+2+2, captain chairs, 18-point massage, 12-way power, zero-gravity at 127.5°. At the A800: 27\" W-HUD, 6,536 mm ambient run, ANC, L3 on the highway." }
];
let ly = BY + 0.66;
const lStep = 1.32;
LAD.forEach((l, i) => {
  T(s3, l.p, { x: lx, y: ly, w: 6.0, h: 0.40, fontSize: 20, fontFace: FD, color: TEXT });
  T(s3, l.m, { x: lx + 6.2, y: ly + 0.12, w: lw - 6.2, h: 0.22, fontSize: 8.4, bold: true,
               charSpacing: 0.8, color: l.c, align: "right" });
  T(s3, l.t, { x: lx, y: ly + 0.52, w: lw, h: 0.44, fontSize: 9, color: BODY,
               lineSpacingMultiple: 1.14 });
  ly += lStep;
  if (i < LAD.length - 1) hairline(s3, lx, ly - 0.20, lw);
});

/* --- takeaway band --- */
const tbY = BY + BH + 0.20;
hairline(s3, M, tbY, CW, "3A3F47");
micro(s3, M, tbY + 0.20, CW, "WHAT WE TAKE FROM IT", GOLD);
const TAKE = [
  ["Colour is the model year.",
   "AION ships three named cabin themes per car, so a CMF change does the work a facelift used to — cheap, fast, visible in a showroom photograph. Our colourways have no names and no launch moment. Give them both."],
  ["Comfort moved down a segment.",
   "Zero-gravity seating and massage crossed below ¥130k in April 2026 — the AION N60 at ¥109,800, with LiDAR standard. Every comfort assumption under ¥150k has to be re-baselined against that car, not last year's segment."],
  ["Above ¥170k, the second row is the product.",
   "Every Trumpchi over that line is sold on recline angle, leg rest and a 17.3\" ceiling screen. Design the rear seat first and the dashboard second."]
];
const tw = (CW - 2 * 0.9) / 3;
TAKE.forEach((t, i) => {
  const x = M + i * (tw + 0.9);
  T(s3, t[0], { x, y: tbY + 0.44, w: tw, h: 0.30, fontSize: 15, fontFace: FD, color: TEXT });
  T(s3, t[1], { x, y: tbY + 0.84, w: tw, h: 0.62, fontSize: 8.8, color: SUB,
                lineSpacingMultiple: 1.16 });
});

footer(s3, "Sources as slides 01–02, plus CnEVPost, CarNewsChina, Gasgoo, MarkLines and 36Kr reporting on Auto China 2026 and the Panyu Action reform. Swatch colours are approximations of the published interior themes for layout use — match to a physical sample before any of this enters a specification.");

pres.writeFile({ fileName: "GAC_AION_Interior_Benchmark.pptx" })
  .then(f => console.log("written:", f));
