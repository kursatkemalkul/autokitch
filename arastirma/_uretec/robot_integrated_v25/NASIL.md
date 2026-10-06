# Main scene v25 / terminal chain step94

SI units: metres, radians, seconds. Web is Y-up; native robot is Isaac Z-up with a -90 degree X display rotation. Unchanged v10l machine stations and accepted pickup/release poses. Native UR10e, igus rail at Z=0.960m, mount Y=0.130m, 3684mm concept stroke. OEM stroke/load confirmation remains open.

12 QR bays unchanged. Customer QR/keypad column is now on the left/away from the right wall: X3.597..3.757, Y0..2.050, Z1.750..2.083m. It shares the cabinet's 333mm depth and uses the unchanged Storm supplier STEP. FM430 is catalogue-envelope geometry, not OEM CAD. Cables enter the lower control module and rise inside this column.

The box is withdrawn into the corridor, carried left on the rail, turned horizontally away from the wall, then approached to the original QR insertion pose. `box_inward.mjs` solves each sample with native IK, preserves payload level and retimes to the configured velocity/acceleration caps. `motion_bounds.mjs` checks conservative moving mesh bounds at every recorded frame. `order_v25.json` feeds all eight recipes and the downloadable Isaac records. Ideal grasp is an animation assumption; no physical grasp certification.

Measured wall inner X5.360m; floor outer X5.640m. Four corner lines only. Recorded body/payload boundary clearance56.09mm; cabinet latch clearance72.07mm. The unchanged 250mm-deep cabinet is recessed200mm in a280mm proposed wall, projects50mm plus14mm latch, and remains aligned with rail depth. Actual building recess/structural approval is pending. Flush floor covers at Y=0; one connected trench, hollow bends and equipment openings, separate routes checked by `route_audit.py`.

Set AUTOKITCH_NODE to Node executable and PYTHONPATH to the existing Shapely runtime. Run `run.py <canonical-machine.glb-or-gzip> --repeat 2`. Manufacturer STEP is `_local/codex_robot_v25/igus_ZLW_20200_3000.stp`; cached tessellation is `rail_cad.json`. Terminal94 must read the final machine-only input, not a prior robot-added GLB. If Claude E/K changes merge later, regenerate94 from their combined machine output.

Open the same `otonom/hat/makine.html`. Select recipe/task/named step; Play, pause and Baştan work as before. Full latest-machine collision, all12bay motion paths, physical unlock/safety circuit and electrical sizing remain declared open. No station generators or shared assembly player are changed.
