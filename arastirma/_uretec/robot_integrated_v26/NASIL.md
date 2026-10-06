# v26 / step95 — compact shop

Append shop to v25 step94 output; all machine/QR/robot geometry bytes and 14 animation clips remain unchanged. Two full runs are byte-identical. The browser panel reads the existing v25 order/recipe JSON and the new v26 model/manifest.

Units: metres, Y up, +Z towards customer. Interior X0.636..5.360, Z-0.880..3.553: 4.724 x 4.433 m, 20.941 m2. Architectural walls are outline-only. Partition Z2.133, desk front Z2.933 and storefront Z3.553. Left entrance and robot-area door each have 900mm net opening. Main entrance opens outward; inner door opens into the staff area.

800mm seated pocket is not a passage behind the chair; access remains via the 900mm left bay. Desk is 770mm high with a true open knee/foot bay, 800mm width and 615mm foot depth. Sink bay is 500 x 620 x 900mm, with empty 300 x 300 x 150mm bowl, elbow mixer, hot/cold lines, trap and 32mm waste. Generic dimensioned furniture/plumbing, not manufacturer CAD. No human avatar is added.

Run: set AUTOKITCH_NODE to installed Node and Python with Shapely available, then python arastirma/_uretec/robot_integrated_v26/run.py SOURCE --repeat 2 --output OUTPUT. Existing vendor/meshopt and v25 public assets are reused read-only. No native 800MB rebuild required.

Checks: incoming binary, nodes, geometry accessors and animations preserved; only retired floor/right outline roots replaced; all171 new meshes closed; new fixtures stay beyond conservative recorded robot front boundary. Full pre-existing robot/station collision, actual guarding and interlocks, building door/egress approval, pipe installation/drain fall and slab penetration approvals remain open. This is a dimensioned layout, not a construction permit or commissioned safety system.
