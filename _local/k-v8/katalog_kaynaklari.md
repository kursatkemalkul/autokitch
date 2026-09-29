# K station (cutting / spray) – verified catalogue data for CAD

Compiled 30 Sep 2026. Every value below was read from the manufacturer document linked in the row (PDF text extracted with PyMuPDF, drawings rendered to PNG and read visually). Local copies of all PDFs and the rendered pages are in this folder (`katalog/`).

Conventions:
- **DERIVED** = computed by me from verified catalogue numbers (the formula is given). It is not a catalogue value.
- **NOT VERIFIED** = not found in any document I could open. Do not model it from this file.
- Inch values are copied as printed. Where the sheet prints mm in brackets, that mm value is used.

---

## 1. Festo DGRF-C-63-125 – guided drive, clean design

Order code notes: size 63 comes only with PPV or PPS cushioning. "A" (sensing) and "R" (sensor rail) are always present for Ø32–63. Full code: `DGRF-C-GF-63-125-PPV-A-R` (or `-PPS-A-R`). Module no. 562221 ([F1] p.11; [F2] p.1).

Sources:
- [F1] Festo catalogue "Guided drives DGRF-C, clean design", edition 2022/06. Read from a distributor-hosted copy: https://5.imimg.com/data5/SELLER/Doc/2023/6/320852276/NP/UG/XK/2244951/festo-guided-dgrf-c-gf-50-actuator-sensors.PDF (the official https://media.festo.com/media/202791_documentation.pdf returned HTTP 403). Local copy: `festo_dgrf_c.pdf`.
- [F2] Festo data sheet, part no. 562221 "DGRF-C-GF-63-", dated 8/11/26: https://ftp.festo.com/Public/PNEUMATIC/SOFTWARE_SERVICE/Datasheet/EN_US/562221.pdf. Local copy: `festo_562221.pdf`.

Dimension letters are from the PPV/PPS drawing, size 63 row ([F1] p.10). Drawing orientation: the housing face on the H2 side sticks out 3 mm past the yoke plate, so that face is the mounting face. The sensor rail is on the opposite face.

| Quantity | Value | Unit | Source | Page |
|---|---|---|---|---|
| Piston Ø | 63 | mm | [F2] | 1 |
| Stroke range | 10 … 400 | mm | [F1] | 4, 11 |
| L1, yoke-plate front face → rear end-cap face, retracted | 207.3 (+1.7/−1.3) + stroke | mm | [F1] | 10 |
| L1 at stroke 125 | 332.3 | mm | DERIVED (207.3 + 125) | – |
| VA, rear centring spigot length beyond L1 | 4 | mm | [F1] | 10 |
| B, rear spigot Ø | 45 d11 | mm | [F1] | 10 |
| B1, overall width (yoke plate / housing) | 162 | mm | [F1] | 10 |
| H1, overall height incl. H2 | 84 | mm | [F1] | 10 |
| H2, step: housing past yoke plate on mounting face | 3 | mm | [F1] | 10 |
| Yoke plate height (H1 − H2) | 81 | mm | DERIVED from drawing geometry | – |
| H3, sensor-rail protrusion (‑R only) | 2 | mm | [F1] | 10 |
| H6, max. protrusion on sensor-rail side (small screw/fitting feature at mid-width, as drawn) | 9.3 | mm | [F1] | 10 |
| L3, housing length | 105 | mm | [F1] | 10 |
| L6, yoke plate thickness | 20 | mm | [F1] | 10 |
| WH, gap from yoke plate rear face to housing front face (retracted) | 11.5 (+0.8/−1) | mm | [F1] | 10 |
| Cylinder barrel + end cap behind housing (L1 − L6 − WH − L3) | 70.8 + stroke (195.8 at 125) | mm | DERIVED | – |
| D4, guide rod Ø | 25 | mm | [F1] | 10 |
| B2, guide rod centre distance | 125 | mm | [F1] | 10 |
| L2, guide rods protruding behind housing (retracted) | 7.5 + stroke (132.5 at 125) | mm | [F1] (+stroke DERIVED) | 10 |
| Piston rod Ø | NOT VERIFIED (not given). DERIVED ≈ 20 from the forces: (1870 − 1682) N / 0.6 MPa = 313 mm² | mm | [F1]/[F2] forces | 6 / 1 |
| Yoke plate payload threads D2 | 4 × M8 (drawn as through-thread in the section view; depth not tabulated) | – | [F1] | 10 |
| D2 pattern B4 × H4 | 80 × 40 | mm | [F1] | 10 |
| H5, mounting face → lower D2 row | 23.5 | mm | [F1] | 10 |
| Housing mounting threads D1 | 4 × M10 | – | [F1] | 10 |
| D1 pattern B3 × L5 | 80 (±0.02 between centring holes) × 40 | mm | [F1] | 10 |
| L7, housing front face → first D1 row | 18.5 | mm | [F1] | 10 |
| L4, yoke-plate front face → first D1 row (retracted) | 50 (+1.3/−1.2) | mm | [F1] | 10 |
| T2 / T1, thread depths from the two housing faces (through hole between) | 24 / 17 | mm | [F1] | 10 |
| D3 × T3, centring counterbore (for ZBH-12-B sleeve, 2 included) | Ø12 H7 × 2.6 | mm | [F1] | 10, 15 |
| End cap: E square / RT threads / TG pattern | 75 / 4 × M8 (female thread in the socket-head cap screws, item [1]) / 56.5 × 56.5 | mm | [F1] | 10 |
| BG / LA1 (end-cap thread-related depths, as drawn) | 17 / 6.1 | mm | [F1] | 10 |
| Ports EE (2×) | G3/8 | – | [F1] / [F2] | 5, 10 / 1 |
| PL1, front port: housing front face → port centre; J1 offset from centreline | 88; 6.3 | mm | [F1] | 10 |
| PL, rear port on end cap: end-cap face → port centre; J2 offset | 27.5; 6.3 | mm | [F1] | 10 |
| Cushion adjusting screw, wrench size | 4 | mm | [F1] | 10 |
| Cushioning length | 22 | mm | [F1] / [F2] | 5 / 1 |
| Theoretical force at 6 bar, advancing / retracting | 1870 / 1682 | N | [F1] / [F2] | 6 / 1 |
| Operating pressure | 1.5 … 12 (0.15 … 1.2 MPa) | bar | [F1] / [F2] | 5 / 1 |
| Max. impact energy in end positions | 1.3 | J | [F2] | 1 |
| Max. speed | NOT VERIFIED (only the formula v = √(2E/(m1+m2)) is given) | m/s | [F1] | 6 |
| Product weight at 0 mm stroke; per 10 mm stroke | 6405; 142.8 (catalogue: 143) | g | [F2] / [F1] | 1 / 6 |
| Weight at 125 mm stroke | ≈ 8190 | g | DERIVED (6405 + 12.5 × 142.8) | – |
| Moving mass at 0 mm; per 10 mm stroke | 2114; 101.7 | g | [F2] | 1 |
| Moving mass at 125 mm stroke | ≈ 3385 | g | DERIVED | – |
| Torsional backlash (retracted, no load) | 0.06 (0.061) | ° | [F1] / [F2] | 5 / 1 |
| Ambient temperature | −20 … +80 | °C | [F1] / [F2] | 5 / 1 |
| Corrosion resistance class | CRC 3 | – | [F1] / [F2] | 5 / 1 |
| IP rating | NOT VERIFIED (not stated in [F1] or [F2]) | – | – | – |
| Food / hygiene notes | "Food-safe → supplementary information on materials" (certificates at festo.com/sp). NSF H1-compliant lubrication. Resistant to common cleaning agents. Seal: TPE-U (PUR) modified for hydrolysis and cleaning; A3 variant uses a PE dry-running wiper. PWIS VDMA24364-B2-L. RoHS. | – | [F1] | 2, 5, 6 |
| Materials | Yoke plate and housing: anodised wrought Al. Guide and piston rods: high-alloy stainless steel. Barrel: anodised Al. Cover (Ø63): coated die-cast Al. | – | [F1] | 6 |
| Position sensing | SMT-C1 on rail, or CRSMT-8M with SMB-8-C. Min. stroke 30 mm to sense both ends (Ø63). | – | [F1] | 8, 12 |
| Hygiene plugs | DAMD-P-M10-16-R1 (housing threads Ø63); DAMD-PS-M8-16-R1 (end-cap threads Ø50/63) | – | [F1] | 15 |

---

## 2. Spraying Systems – PulsaJet AA10000AUH and UniJet TG

**Important:** the food version AA10000AUH-**104210** takes **TPU___PWMD low-profile dovetail flat-spray tips** and has a built-in 5° tip offset ([S1]). It is **not** a UniJet TG full-cone body. The standard **AA10000AUH-03** "accepts standard UniJet tip sizes up to -03 capacity" and the UniJet tip is ordered separately ([S2]). No sheet explicitly confirms that TG full-cone tips fit the -03. Food-contact conformity of the -03 is not stated on its sheet.

Sources:
- [S1] Data Sheet 104210, rev. 4, "PulsaJet AA_10000AUH-104210-__": https://www.spray.com/-/media/dam/industrial/usa/technical-documentation/product-data-sheet/10000auh-104210.pdf. Local: `ssco_aa10000auh_104210.pdf`, `ssco_104210_full.png`.
- [S2] Data Sheet 10000AUH-03, rev. 5: https://www.spray.com/-/media/dam/industrial/usa/technical-documentation/product-data-sheet/ds10000auh-03.pdf. Local: `ssco_ds10000auh_03.pdf`, `ssco_03_side.png`.
- [S3] Catalog 75, UniJet D/TG section (catalogue pages B36–B40): https://spray.widen.net/content/dxuisu7v2e/PDF/Catalog75_Hydraulic_Nozzles_US_Units_FullJet_TG_TG-W_TH-W.pdf. Local: `ssco_cat75_tg.pdf`.
- [S4] https://portal.spray.com/en-us/products/1-4tt-ss-tg-ss0-3 · [S5] https://portal.spray.com/en-us/products/tg-ss1 · [S6] https://portal.spray.com/en-us/models/t-tt · [S7] https://portal.spray.com/en-us/categories/unijet-nozzle-bodies-and-tip-retainers?ModelId=Cp1325
- [S8] Manual MI-10000AUH-03-Z1 (ATEX variant): https://www.spray.com/-/media/dam/industrial/usa/technical-documentation/owner-manual-maintenance-instructions/mi-10000auh-03-z1.pdf

### 2a. AA10000AUH-104210 (food version, e.g. AA10000AUH-104210-VIFC)

| Quantity | Value | Unit | Source | Page |
|---|---|---|---|---|
| Body height (top face → bottom face of body) | 1.53 [38.9] | in [mm] | [S1] | 1 |
| Height incl. tip nut (excl. connector) | 2.10 [53.3] | in [mm] | [S1] | 1 |
| Width across flats | 1.19 [30.1] | in [mm] | [S1] | 1 |
| Body Ø | NOT VERIFIED on this sheet (the -03 sheet gives Ø1.49 in [37.8 mm]) | – | – | – |
| Liquid inlet (top face) | 1/8" NPT, 1/8" BSPT or 1/8" BSPP | – | [S1] | 1 |
| Mounting threads (multiple points) | #8-32 (NPT version) / M4 × 0.7 (BSPT/BSPP versions) | – | [S1] | 1 |
| Rear-face hole offsets from centre | 0.44 [11.1] horizontal and 0.44 [11.1] vertical | in [mm] | [S1] | 1 |
| Side holes: spacing; top face → hole row | 0.50 [12.7]; 0.28 [7.1] | in [mm] | [S1] | 1 |
| Tip offset angle | 5 | ° | [S1] | 1 |
| Electrical connector | Integral 3-pole M8 male receptacle. Supplied with a 5 m straight, shielded M8 female cordset. Pins 1 (brown) and 3 (blue) only, polarity not important; shield to earth. -NC = no cable. | – | [S1] | 1 |
| Power | 0.36 A at 24 VDC | – | [S1] | 1 |
| Max. fluid pressure | 250 (17) with AutoJet Advanced controllers | psi (bar) | [S1] | 1 |
| Max. fluid temperature | 200 (93) | °F (°C) | [S1] | 1 |
| Weight | ≈ 9 oz (0.26 kg) | – | [S1] | 1 |
| Max. cycling | up to 15,000 cycles/min (AutoJet Advanced panels) | – | [S1] | 1 |
| Food version | CE, food-contact materials per EC 1935/2004. FDA/food-contact Viton or EPR seals. Fork-and-cup logo. | – | [S1] | 1 |
| Mounting kit for 1/2" rod | Data Sheet 50935 (not read) | – | [S1] | 1 |

### 2b. AA10000AUH-03 (standard body for UniJet tips)

| Quantity | Value | Unit | Source | Page |
|---|---|---|---|---|
| Overall length, tip front → end of M8 receptacle (approx., with tip) | 2.61 [66.2] | in [mm] | [S2] | 1 |
| Body Ø | 1.49 [37.8] | in [mm] | [S2] | 1 |
| Width across flats | 1.19 [30.1] | in [mm] | [S2] | 1 |
| Front-face mounting holes | 4 on a 0.86 × 0.86 [21.9 × 21.9] square (±0.43 [10.9] from centre) | in [mm] | [S2] | 1 |
| Rear-face holes | 2 at 0.88 [22.2] spacing (±0.44 [11.1]) plus 1 at 0.44 [11.1] below centre | in [mm] | [S2] | 1 |
| Side holes: spacing; offset from centreline | 0.50 [12.7]; 0.25 [6.4] | in [mm] | [S2] | 1 |
| Mounting thread (front, sides, back) | #8-32 UNC or M4 × 0.7 | – | [S2] | 1 |
| Inlet (rear centre) | 1/8 NPT [1/8 BSPT] [1/8 BSPP] | – | [S2] | 1 |
| Connector | 3-pole M8 male receptacle. Cordset with LED. Pin 1 brown +24 V, pin 3 blue 0 V, pin 4 unused. | – | [S2] | 1 |
| Power / max. pressure / max. fluid temp. | 24 VDC, 0.36 A / 100 psi (7 bar) / 200 °F (93 °C) | – | [S2] | 1 |
| Weight | ≈ 9 oz (0.26 kg) | – | [S2] | 1 |
| Max. cycling | up to 10,000 cycles/min (AutoJet controller) | – | [S2] | 1 |
| Wetted materials / seals | Stainless steel, PPS, zirconia ceramic / FKM, EPDM or FFKM | – | [S2] | 1 |
| Tips | Standard UniJet tips up to "-03" capacity, ordered separately | – | [S2] | 1 |
| Tip retaining cap | CP1325 is the "standard nozzle retaining cap for all UniJet style assemblies". The ATEX -03-Z1 lists CP1325-SS. Thread and hex size: NOT VERIFIED. | – | [S7] / [S8] | – / 9 |

### 2c. UniJet TG full-cone tip + TT body

| Quantity | Value | Unit | Source | Page |
|---|---|---|---|---|
| Assembly | TG tip is used with a T (female) or TT (male) body **and a tip retainer**. The tip has no thread of its own. | – | [S3] | B36 (PDF p.1) |
| TT(M) + TG, 1/4" inlet: length L / hex / net weight | 1.844 / 13/16 / 2.1 oz | in | [S3] | B40 (PDF p.4) |
| Same in mm | L 46.8 / hex 20.6 | mm | DERIVED (× 25.4) | – |
| 1/4TT-SS + TG-SS0.3: length / hex / weight / inlet | 1.84 in / 13/16 in / 2.3 oz / 1/4 in NPT male | – | [S4] | web |
| Tip-alone dimensions (Ø, height) | NOT VERIFIED | – | – | – |
| TG0.3: orifice / max. free passage | 0.020 / 0.016 | in | [S3] | B39 (PDF p.3) |
| TG0.3 flow at 20/40/80/100/150 psi | 0.041 / 0.057 / 0.078 / 0.087 / 0.10 | gpm | [S3] | B39 |
| TG0.3 spray angle at 20 / 80 psi | 50 / 61 | ° | [S3] | B39 |
| TG1: orifice / max. free passage | 0.036 / 0.025 | in | [S3] / [S5] | B39 |
| TG1 flow at 10/20/40/80/100/150 psi | 0.10 / 0.14 / 0.19 / 0.26 / 0.29 / 0.35 | gpm | [S3] | B39 |
| TG1 spray angle at 20 / 80 psi | 58 / 53 | ° | [S3] | B39 |
| UniJet D/TG operating pressure | up to 300 (20) | psi (bar) | [S3] | B36 |
| T/TT body pressure rating | up to 500 (35) | psi (bar) | [S6] | web |
| TG materials | Brass, 303 SS | – | [S3] | B37 |

---

## 3. HIWIN MGN12H (and MGN9H) miniature guide

Sources:
- [H1] HIWIN "MG Series – Miniature Linear Guideway" catalogue (scanned PDF), catalogue pp. 75–89: https://www.letromec.com/pdf/hiwin-linear-guideway-mg-series.pdf. The MGN dimension table is catalogue p.86 = PDF p.12; rail lengths are p.85 = PDF p.11. Local: `hiwin_mg_letromec.pdf`, `hiwin_mgn_table.png`, `hiwin_mgn_draw.png`, `hiwin_rail_len.png`.
- [H2] Cross-check, hiwin.de MGN12HZ0CM page: https://www.hiwin.de/en/Products/Linear-guideways/Blocks/Miniature-guides/MGN-HIRES-series/MGN12HZ0CM/p/MGN12HZ0CM

Symbols (from the drawing):
- H: rail bottom → block top
- H1: rail bottom → block bottom
- N: rail side → block side
- W, L: block width and length (L includes the end seals)
- L1: steel body length
- B × C: mounting-hole pattern
- B1: block side → hole
- M × l: thread × depth
- Gn: grease hole Ø
- H2: block top → grease-hole axis
- WR, HR: rail width and height
- D / h / d: counterbore Ø / counterbore depth / through-hole Ø
- P: hole pitch
- E: end distance

| Quantity | MGN12H | MGN9H | Unit | Source | Page |
|---|---|---|---|---|---|
| H (assembly height) | 13 | 10 | mm | [H1] ([H2] for 12H) | 86 |
| H1 | 3 | 2 | mm | [H1] | 86 |
| Block body height (H − H1) | 10 | 8 | mm | DERIVED | – |
| N | 7.5 | 5.5 | mm | [H1] | 86 |
| W (block width) | 27 | 20 | mm | [H1] | 86 |
| B (hole spacing across) | 20 | 15 | mm | [H1] | 86 |
| B1 | 3.5 | 2.5 | mm | [H1] | 86 |
| C (hole spacing along) | 20 | 16 | mm | [H1] | 86 |
| L1 (body) | 32.4 | 29.9 | mm | [H1] | 86 |
| L (overall block) | 45.4 | 39.9 | mm | [H1] | 86 |
| Gn (grease hole) | Ø2 | Ø1.4 | mm | [H1] | 86 |
| Block threads M × l (4×) | M3 × 3.5 | M3 × 3 | mm | [H1] | 86 |
| H2 | 2.5 | 1.8 | mm | [H1] | 86 |
| WR (rail width) | 12 | 9 | mm | [H1] | 86 |
| HR (rail height) | 8 | 6.5 | mm | [H1] | 86 |
| Rail hole D × h × d | 6 × 4.5 × 3.5 | 6 × 3.5 × 3.5 | mm | [H1] | 86 |
| Rail hole pitch P | 25 | 20 | mm | [H1] | 85, 86 |
| Standard end distance E | 10 | 7.5 | mm | [H1] | 85, 86 |
| Rail bolt | M3 × 8 | M3 × 8 | – | [H1] | 86 |
| Rail length rule | L = (n − 1)·P + 2E. E tolerance for standard rails ±0.5. | – | – | [H1] | 85 |
| Standard rail lengths | 70, 95, 120, 145, 170, 195, 220, 245, 270, 320, 370, 470, 570, 695 (max. std 1995, max. 2000) | 55, 75, 95, 115, 135, 155, 175, 195, 275, 375 (max. std 1195; max. 1200 SS / 1000 carbon steel) | mm | [H1] | 85 |
| C dyn / C0 | 3.72 / 5.88 | 2.55 / 4.02 | kN | [H1] ([H2] for 12H) | 86 |
| MR / MP / MY | 38.22 / 36.26 / 36.26 | 19.60 / 18.62 / 18.62 | N·m | [H1] | 86 |
| Block mass / rail mass | 0.054 kg / 0.65 kg/m ([H2] HIRES block: 0.05 kg) | 0.026 kg / 0.38 kg/m | – | [H1] | 86 |

---

## 4. SMC D-M9N / D-M9B auto switch on MY1B10

Sources:
- [M1] SMC catalogue MY1B, content2.smcetech.com/pdf/MY1B_2103.pdf: https://content2.smcetech.com/pdf/MY1B_2103.pdf. PDF p.6 = How to Order; p.11 = 8-11-21 (MY1B10G dimensions); p.24 = 8-11-101 (switches); p.27 = 8-11-104 (mounting position). Local: `SMC_MY1B_2103.pdf` (same MD5 as the fetched URL), `my1b_p24.png`, `my1b_p27.png`, `my1b_p27_zoom.png`, `my1b_p11.png`.
- [M2] SMC Best Pneumatics p.1199, "D-M9N/D-M9P/D-M9B": https://ca01.smcworld.com/catalog/BEST-5-8-en/pdf/8-p1199-1200-kousw_en.pdf (redirect target of www.smcworld.com/catalog/BEST-5-8-en/pdf/8-p1199-1200-kousw_en.pdf). Local: `smc_dm9_best.pdf`, `smc_dm9_dims.png`.
- [M3] Short type D-M9□-5 (15 mm long, option): https://content2.smcetech.com/pdf/D-M9Short.pdf

| Quantity | Value | Unit | Source | Page |
|---|---|---|---|---|
| Applicability | D-M9N(V)/M9P(V)/M9B(V) listed for MY1B bores 10, 16, 20 | – | [M1] | 24 (8-11-101) |
| MY1B10 type | "For ø10, only G is available" (centralized piping, MY1B10G). Overall length 110 + stroke. | mm | [M1] | 6, 11 |
| Mounting method | Direct mounting: the switch sits in the cylinder-tube switch groove and is fixed with its own M2.5 × 4L slotted set screw. SMC: use only the screw supplied on the switch body. | – | [M2] / [M1] | 1199 / 27 |
| Position A: left end face of MY1B10 → set-screw end of switch (stroke-end detection) | 24 | mm | [M1] | 27 (8-11-104) |
| Position B: set-screw end of 2nd switch → right end face | 86 | mm | [M1] | 27 |
| Operating range, D-M9 on MY1B10 (D-F9W: 3) | 2.5 | mm | [M1] | 27 |
| Switch body length | 22 | mm | [M2] | 1199 |
| Plan-view widths (as dimensioned) | 4 and 2.8 | mm | [M2] | 1199 |
| Height above groove axis (end view) | 2.6 | mm | [M2] | 1199 |
| Most-sensitive position from set-screw end | 6 | mm | [M2] | 1199 |
| Lead wire | Oil-proof heavy-duty, 2.7 × 3.2 ellipse, 0.15 mm². 3 cores (M9N/M9P), 2 cores (M9B). Min. bend radius 20 (ref.). Standard 0.5 m (Nil), 1 m (M), 3 m (L), 5 m (Z). | mm | [M2] | 1199 |
| D-M9N electrical | 3-wire NPN. Supply 5/12/24 VDC (4.5–28 V), ≤10 mA consumption. Load ≤28 VDC, ≤40 mA. Voltage drop ≤0.8 V at 10 mA (≤2 V at 40 mA). Leakage ≤100 µA. | – | [M2] | 1199 |
| D-M9B electrical | 2-wire, 24 VDC (10–28 VDC), load 2.5–40 mA, voltage drop ≤4 V, leakage ≤0.8 mA | – | [M2] | 1199 |
| Weight D-M9N (0.5/1/3/5 m) | 8 / 14 / 41 / 68 | g | [M2] | 1199 |
| Weight D-M9B (0.5/1/3/5 m) | 7 / 13 / 38 / 63 | g | [M2] | 1199 |
| Groove cross-section on MY1B10 tube | NOT VERIFIED (not dimensioned in [M1]) | – | – | – |

---

## 5. SMC SY3000 valve (SY3120 / SY3220) + SS5Y3-20 manifold (4 stations)

**Caveat:** the only SMC SY catalogues I could open are the **2005 edition** ([Y1]) and the 2003/04 edition ([Y2]). Both are pre-"new SY". Current-production parts may differ slightly, so check against current SMC CAD before release.

Sources:
- [Y1] SMC catalogue "Series SY3000/5000/7000/9000" (2005): https://content2.smcetech.com/pdf/SY3000.pdf. PDF p.7 = 1-4-12 (SY3120), p.8 = 1-4-13 (SY3220), p.19 = 1-4-42, p.21 = 1-4-44, p.22 = 1-4-45 (SS5Y3-20). Local: `smc_sy3000_new.pdf`, `smc_sy2005_p07.png`, `smc_sy2005_p08.png`, `smc_sy2005_p22.png`, `smc_ss5y3_zoom.png`.
- [Y2] SMC catalogue SY3000/5000/7000 (2003/04): https://content2.smcetech.com/pdf/SY_3000.pdf. PDF p.18 = 1.1-39, p.19 = 1.1-40 (same L1/L2 table and weight formula). Local: `smc_sy_3000.pdf`.

| Quantity | Value | Unit | Source | Page |
|---|---|---|---|---|
| SY3120 (single, grommet) overall length [AC] | 66.9 [69.1] | mm | [Y1] | 1-4-12 |
| SY3120 body length (without solenoid) | 44.7 | mm | [Y1] | 1-4-12 |
| SY3120 with L-plug connector / M-plug / M8 (WO) | 76.8 [79] / 67 [69.2] / 75.9 | mm | [Y1] | 1-4-12 |
| SY3220 (double, grommet) overall length [AC] | 88.8 [93.2] (half = 44.4) | mm | [Y1] | 1-4-13 |
| SY3220 with L-plug / M-plug / M8 (WO) | 108.6 [113] / 89 [93.4] / 106.8 | mm | [Y1] | 1-4-13 |
| Valve body width | 10 ((15) reference width in bottom view) | mm | [Y1] | 1-4-12 |
| Heights above valve bottom: body steps / top of C6 (N7) one-touch fitting / release ring | 16.9 and 18.5 / 33.6 (37.4) / + (3.2) | mm | [Y1] | 1-4-12 |
| Coil height (grommet): without / with light-surge suppressor [AC] | 25 / 28.5 [35.5] | mm | [Y1] | 1-4-12 |
| A/B fitting centre → body end (side view) | 22.5 | mm | [Y1] | 1-4-12 |
| 2 × Ø3.2 mounting holes: height above bottom / spacing / overall (bracket outline) | (32) / (27) / (35) | mm | [Y1] | 1-4-12 |
| Manifold fixing holes in valve / A–B fitting pitch | 2 × Ø2.2, 21.4 apart along the valve (as dimensioned) / 10.2 | mm | [Y1] | 1-4-12 |
| Bracket threads | 2 × M3 × 0.5 depth 3.5, spacing 9.5 | mm | [Y1] | 1-4-12 |
| Body-ported valve ports P, EA, EB (underside) | M5 × 0.8, EA–EB spacing 19 | mm | [Y1] | 1-4-12 |
| A/B ports | C4 / C6 one-touch (or M5) | – | [Y1] | 1-4-12 |
| SS5Y3-20 manifold pitch | 10.5 | mm | [Y1] | 1-4-45 |
| L1 (overall) / L2 (mounting holes), **4 stations** | 69.5 / 51.5 | mm | [Y1] / [Y2] | 1-4-45 / 1.1-40 |
| L1 / L2 for n stations | L1 = 48.5 + 10.5·(n − 2); L2 = L1 − 18 (table 2–20 stn) | mm | [Y1] (formula DERIVED from table) | 1-4-45 |
| End → first valve centre / end → mounting hole | 19 / 9 | mm | [Y1] | 1-4-45 |
| Base width / base height | 49 / 20 | mm | [Y1] | 1-4-45 |
| Base mounting | 4 × Ø4.5; across-width spacing 16 | mm | [Y1] | 1-4-45 |
| P, EA, EB (manifold end ports) | 1/8 (Rc; NPT/NPTF/G by suffix 00N/00T/00F), spacing 16.5 | mm | [Y1] | 1-4-42, 1-4-45 |
| P centreline → base edge (EB side) | 23.5 | mm | [Y1] | 1-4-45 |
| Heights on manifold: base bottom → valve top [AC] / → top of C6 (N7) fitting | 49 [56] / 54.1 (57.9), + (3.2) | mm | [Y1] | 1-4-45 |
| Single valve extends from P centreline to coil end [AC] | 44.4 [46.6] | mm | [Y1] | 1-4-45 |
| Transverse extent with double solenoid [AC] | 97.3 [101.7] | mm | [Y1] | 1-4-45 |
| Manifold base weight | W = 13n + 35 → 87 g for 4 stn | g | [Y1] / [Y2] (4 stn DERIVED) | 1-4-44 / 1.1-39 |
| Blanking plate / order example | SY3000-26-9A; SS5Y3-20-05 + SY3120-5G-C6 … | – | [Y1] | 1-4-42 |

---

## 6. SMC AW20 filter regulator and AS1201F speed controller

Sources:
- [W1] SMC AW10–40 (legacy series, matches the name "AW20-F01"): https://content2.smcetech.com/pdf/AW_Metric.pdf. PDF p.2 = 14-2-68 (specs), p.5 = 14-2-71 (dims). Local: `smc_aw_metric.pdf`, `smc_aw_p05.png`, `smc_aw_spec.png`, `smc_aw_legacy_zoom.png`.
- [W2] SMC AW10-A–AW40-A (current "-A" series, e.g. AW20-F01-A): https://content2.smcetech.com/pdf/AW_A.pdf. PDF p.3 = cat. 469, p.8 = cat. 474. Local: `smc_aw_a.pdf`, `smc_aw_a_p08.png`.
- [A1] SMC "Speed Controller with One-touch Fitting, Elbow Type" (EU, 2013): https://content2.smcetech.com/pdf/AS_1F-A_EU.pdf. PDF p.7 = cat. p.5. Local: `smc_as1f_a_eu.pdf`, `smc_as1f_p07.png`.

### AW20 (legacy, AW20-F01)

| Quantity | Value | Unit | Source | Page |
|---|---|---|---|---|
| Ports / gauge port | 1/8, 1/4 (F = G thread) / 1/8 | – | [W1] | 14-2-68 |
| A, body width | 40 | mm | [W1] | 14-2-71 |
| B, overall height (knob top → drain) / with auto-drain | 160 / 177 | mm | [W1] | 14-2-71 |
| C, knob top → IN/OUT port centreline | 73 | mm | [W1] | 14-2-71 |
| E, body depth (side view) | 40 | mm | [W1] | 14-2-71 |
| G, min. clearance below for maintenance | 40 | mm | [W1] | 14-2-71 |
| Bracket: M (axis → bracket face) / T / N / S / Q / U (thickness) / P / V | 30 / 55 / 34 / 15.4 / 5.4 / 2.3 / 44 / 30 | mm | [W1] | 14-2-71 |
| Other letters D / H (with gauge) / J / K | 52 / 63 / 27 / 5 (see drawing) | mm | [W1] | 14-2-71 |
| Panel mount W / Y / Z; plate thickness | 28.5 / 14 / 6; max. 3.5 | mm | [W1] | 14-2-71 |
| Max. operating / proof pressure; set range | 1.0 / 1.5 MPa; 0.05–0.85 MPa | – | [W1] | 14-2-68 |
| Filtration / drain capacity / bowl | 5 µm / 8 cm³ / polycarbonate | – | [W1] | 14-2-68 |
| Weight | 0.32 | kg | [W1] | 14-2-68 |

### AW20-A (current series)

| Quantity | Value | Unit | Source | Page |
|---|---|---|---|---|
| A (width) / B (port axis → bottom) / C (port axis → knob top, knob unlocked) | 40 / 87.6 / 67.4 | mm | [W2] | 474 |
| Overall height B + C | 155.0 | mm | DERIVED | – |
| D / F (panel nut thread) / G (maintenance clearance) / J | 22 / M36 × 1.5 / 25 / 22 | mm | [W2] | 474 |
| Bracket M / N / Q / R / S / T / U / V | 30 / 34 / 43.9 / 5.4 / 15.4 / 55 / 2.3 / 27.3 | mm | [W2] | 474 |
| Round gauge Ø / J with gauge | 37.5 / 58.5 | mm | [W2] | 474 |
| Ports / gauge port; set range; max. pressure; weight | 1/8, 1/4 / 1/8; 0.05–0.7 MPa; 1.0 MPa; 0.21 kg | – | [W2] | 469 |

### AS1201F-M5 (elbow, current "-A")

Symbols: T = thread, H = hex, D1 = fitting OD, D3 = needle knob Ø. L1, L2, L3, L4, A and M are drawing dimensions (see drawing).

| Quantity | AS1201F-M5-04A | AS1201F-M5-06A | Unit | Source | Page |
|---|---|---|---|---|---|
| Tube OD d | 4 | 6 | mm | [A1] | 5 |
| T / H (hex, AF) | M5 × 0.8 / 9 | M5 × 0.8 / 9 | mm | [A1] | 5 |
| D1 / D3 | 8.2 / 9 | 10.4 / 9 | mm | [A1] | 5 |
| L1 / L2 / L3 | 17.2 / 22 / 16.9 | 18.6 / 23.4 / 16.5 | mm | [A1] | 5 |
| L4, unlock / lock (ref.) | 26.5 / 25.4 | 26.5 / 25.4 | mm | [A1] | 5 |
| A after installation, unlock / lock (ref.) | 23.5 / 22.4 | 23.5 / 22.4 | mm | [A1] | 5 |
| M | 13.3 | 13.3 | mm | [A1] | 5 |
| Weight | 5 | 6 | g | [A1] | 5 |

---

## 7. Omron E3Z-D62, E3Z-LS61, E2E-X5ME1

Sources:
- [O1] Omron E3Z datasheet CSM_E3Z_DS_E_18_10: https://assets.omron.eu/downloads/latest/datasheet/en/e3z_compact_photoelectric_sensor_with_built-in_amplifier_datasheet_en.pdf. p.5 specs, p.7 common specs, p.15 dimensions. Local: `omron_e3z_eu.pdf`, `omron_e3z_p15_top.png`.
- [O2] Omron E3Z-LS datasheet CSM_E3Z-LS_DS_E_7_1 (RS mirror): https://docs.rs-online.com/2962/0900766b810051a9.pdf. p.2 specs, p.10 dimensions. Local: `omron_e3z_ls.pdf`, `omron_e3zls_p10.png`.
- [O3] Omron E2E standard datasheet: https://assets.omron.com/m/24413d8c320a900c/original/E2E-Standard-Proximity-Sensor-Datasheet.pdf. p.12 models, p.16 specs, p.27–28 dimensions (Diagram 6). Local: `omron_e2e_std.pdf`, `omron_e2e_diag6.png`.

| Quantity | E3Z-D62 | E3Z-LS61 | Unit | Source | Page |
|---|---|---|---|---|---|
| Housing W × H × D | 10.8 × 31 × 20 | 10.8 × 31 × 20 | mm | [O1] / [O2] | 15 / 10 |
| Protrusion on top (indicators/adjusters) | 2.1 | 2.1 | mm | [O1] / [O2] | 15 / 10 |
| Mounting | 2 × M3, pitch 25.4. Upper hole 2.8 below top and 3 behind lens face. | same | mm | [O1] / [O2] | 15 / 10 |
| Lenses | 2 × Ø7, centres 8 apart | 2 × Ø7, centres 8 apart | mm | [O1] / [O2] | 15 / 10 |
| Upper hole → emitter optical axis | 16.7 | 18.7 | mm | [O1] / [O2] | 15 / 10 |
| Cable | Ø4 PVC, 3 × 0.2 mm², 2 m | Ø4 PVC, 4 × 0.2 mm², 2 m (0.5 m option) | – | [O1] / [O2] | 15 / 10 |
| Sensing | 1 m (white paper 300 × 300 mm), IR LED 870 nm | BGS: 20 mm to set distance. Setting range 40–200 mm (white), 40–160 mm (black). Red LED 680 nm. | – | [O1] / [O2] | 5 / 2 |
| Supply / consumption | 12–24 VDC ±10% (ripple 10%) / 30 mA | 12–24 VDC ±10% / 30 mA | – | [O1] / [O2] | 7, 5 / 2 |
| Output / response | NPN open collector, 100 mA / 1 ms | NPN OC, 100 mA / 1 ms | – | [O1] / [O2] | 7, 5 / 2 |
| Protection / weight (packed, 2 m) | IP67 / ≈ 65 g | IP67 / ≈ 65 g | – | [O1] / [O2] | 5 / 2 |
| Case / lens | PBT / modified polyarylate (D62 lens is black) | PBT / modified polyarylate | – | [O1] / [O2] | 5, 15 / 2 |

| Quantity (E2E-X5ME1 2M, M12 **unshielded**, DC 3-wire NPN NO) | Value | Unit | Source | Page |
|---|---|---|---|---|
| Thread | M12 × 1 | – | [O3] | 28 |
| Housing length, sensing face → rear end | 38 | mm | [O3] | 28 |
| Cable protector behind housing | 9 (total to cable ≈ 47, DERIVED) | mm | [O3] | 28 |
| Unthreaded sensing head | Ø9 × 7 | mm | [O3] | 28 |
| Thread ends at (from face) | 33 | mm | [O3] | 28 |
| Nuts (2) + toothed washer | 17 (hex, end view), outer Ø21, nut thickness 4 | mm | [O3] | 28 |
| Cable | Ø4 PVC, 3 × 0.3 mm², 2 m | – | [O3] | 28 |
| Sensing distance / set distance | 5 ±10% / 0–4 | mm | [O3] | 16 |
| Supply / consumption / load | 12–24 VDC (10–40 VDC) / 13 mA / 200 mA | – | [O3] | 16 |
| Response frequency | 0.4 | kHz | [O3] | 16 |
| Protection / weight (packed) | IP67 (oil-resistant, pre-wired) / ≈ 75 g | – | [O3] | 16 |
| Case / sensing face | Nickel-plated brass / PBT | – | [O3] | 16 |

---

## 8. Food-grade PU/TPU conveyor belt, 2 mm, white

Habasit is verified. Ammeraal Beltech is **NOT VERIFIED**: ammeraalbeltech.com failed DNS, and a retry returned HTTP 403.

Sources:
- [B1] Habasit PDS "CD.F20-A-UW" (Cleandrive friction drive, released 09.05.2025): https://tdm.habasit.com/PDS/en-us/Habasit%20Cleandrive%20Friction%20Drive/CD.F20-A-UW-en-us.pdf. Local: `habasit_CD.F20-A-UW.pdf`.
- [B2] Alternative, non-reinforced transparent "CD.F20-N-FT+S/EH" (released 19.08.2026): https://tdm.habasit.com/PDS/en-us/Cleandrive%20friction%20drive%20unified/CD.F20-N-FT_S_EH-en-us.pdf

| Quantity | Habasit CD.F20-A-UW | Unit | Source | Page |
|---|---|---|---|---|
| Material / colour / surfaces | TPU, **white**, glossy both sides, aramid cords embedded (monolithic, no fabric) | – | [B1] | 1 |
| Thickness | 2.0 | mm | [B1] | 2 |
| Hardness / mass | 95 ShA / 2.4 kg/m² | – | [B1] | 2 |
| Min. pulley Ø (also with counter-flexion) | 25 | mm | [B1] | 2 |
| Operating temperature (continuous) | −20 … +80 | °C | [B1] | 2 |
| k1% static / relaxed; admissible tensile force (at max. temp.) | 9.5 / 7.0; 6.0 (3.0) | N/mm | [B1] | 2 |
| Cord spacing; min. belt width; seamless width | 15; 150; 1829 | mm | [B1] | 2 |
| Joining | Quickmelt | – | [B1] | 2 |
| Food conformity | EU: EC 1935/2004 and EU 10/2011 (see DoC). FDA: yes (DoC). USDA Dairy / NSF-3-A 14159-3 (edges sealed). Halal. | – | [B1] | 1 |
| Item number | H800006238 | – | [B1] | 3 |
| Alt. [B2] (transparent, no cords): thickness / hardness / temp. / food | 2.0 mm / 85 ShA / −20 … +60 °C / EU + FDA "Yes – check DoC". Min. pulley Ø not given. | – | [B2] | 1–2 |

---

## 9. Small stainless pressure tank (≈ 3–5 L) for liquid butter

**I found no Spraying Systems (or other) tank of 3–5 L with a verified food-contact declaration.** The only Spraying Systems food tank system I found, the AutoJet AccuGlaze Pressure Tank System 2850+, has a pressurised **50 L** tank ([T3]). The closest small tanks I could verify are the Walther Pilot MDG series (general-purpose stainless paint/material tanks). Their food suitability, heating option, air-inlet thread and weight are **NOT VERIFIED**.

Sources:
- [T1] https://walther-pilot.de/en/products/product/material-preparation/pressure-tanks/mdg-3/
- [T2] https://walther-pilot.de/en/products/product/material-preparation/pressure-tank/mdg-8/
- [T3] https://www.spray.com/en-eu/products/application-specific-automated-spray-systems/autojet-systems-for-food-applications/autojet-accuglaze-pressure-tank-system-2850

| Quantity | Walther Pilot MDG 3 | Walther Pilot MDG 8 | Unit | Source |
|---|---|---|---|---|
| Filling / usable capacity | 3.2 / 2.5 | 8.2 / 6.4 | L | [T1] / [T2] |
| Material | stainless steel | stainless steel | – | [T1] / [T2] |
| Pressure rating | vacuum / 3 bar / 6 bar (versions) | vacuum / 4 bar | – | [T1] / [T2] |
| Inside / outside Ø | 125 / 173 | 213 / 290 | mm | [T1] / [T2] |
| Total height without agitator | 454 (458 with pneumatic agitator) | 424 (upper outlet) / 455 (lower outlet) | mm | [T1] / [T2] |
| Material outlet (top / bottom) | 1/4" / 1/4" | 3/8" / 3/8" | – | [T1] / [T2] |
| Air inlet thread, weight, food approval, heating | NOT VERIFIED | NOT VERIFIED | – | – |

---

## 10. Siemens S7-1200 modules

Sources: official Siemens data sheets, read from automation24 mirrors (the Siemens apim.industry.siemens.cloud host failed DNS):
- [P1] 6ES7214-1AG40-0XB0: https://media.automation24.com/datasheet/en/6ES72141AG400XB0.pdf
- [P2] 6ES7221-1BF32-0XB0: https://media.automation24.com/datasheet/en/6ES72211BF320XB0.pdf
- [P3] 6ES7221-1BH32-0XB0: https://media.automation24.com/datasheet/en/6ES72211BH320XB0.pdf
- [P4] 6ES7222-1BF32-0XB0: https://media.automation24.com/datasheet/en/6ES72221BF320XB0.pdf
- [P5] 6ES7222-1BH32-0XB0: https://media.automation24.com/datasheet/en/6ES72221BH320XB0.pdf

| Module | W × H × D | Weight | Source | Page |
|---|---|---|---|---|
| CPU 1214C DC/DC/DC (6ES7214-1AG40-0XB0). 14 DI / 10 DO 24 VDC / 2 AI. Supply 24 VDC (20.4–28.8 V), IP20, DIN rail or wall. | 110 × 100 × 75 mm | ≈ 415 g | [P1] | 1, 7 |
| SM 1221 DI 8 × 24 VDC (6ES7221-1BF32-0XB0) | 45 × 100 × 75 mm | ≈ 170 g | [P2] | 2 |
| SM 1221 DI 16 × 24 VDC (6ES7221-1BH32-0XB0) | 45 × 100 × 75 mm | ≈ 210 g | [P3] | 2 |
| SM 1222 DQ 8 × 24 VDC / 0.5 A (6ES7222-1BF32-0XB0) | 45 × 100 × 75 mm | ≈ 180 g | [P4] | 2 |
| SM 1222 DQ 16 × 24 VDC / 0.5 A (6ES7222-1BH32-0XB0) | 45 × 100 × 75 mm | ≈ 220 g | [P5] | 3 |
| Relay SM 1222 variants | NOT VERIFIED (not read) | – | – | – |

---

## Open points (NOT VERIFIED)

- Festo DGRF-C-63: max. speed, IP rating, piston-rod Ø (only DERIVED ≈ 20 mm), rod-axis height above the mounting face (not dimensioned). Use Festo CAD for exact port and sensor-side orientation.
- PulsaJet: body Ø of the -104210 (only across-flats given). Whether TG tips fit the -03 is not stated explicitly. CP1325 retainer thread/hex not verified. -03 food-contact conformity not stated.
- UniJet TG tip-alone dimensions.
- SMC SY: data are from the 2005 and 2003/04 catalogue editions; confirm against current SMC CAD. MY1B10 switch-groove profile.
- Ammeraal Beltech belt: no data (site unreachable).
- Pressure tank: no food-certified 3–5 L tank verified.
