import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const r=spawnSync(process.execPath,['--test','--test-reporter=tap',path.join(dir,'interlock.test.mjs')],{encoding:'utf8'});
const n=key=>Number(r.stdout.match(new RegExp('^# '+key+' (\\d+)','m'))?.[1]??0);
const result={version:3,base:'cb7d1ecf59b2be6b30f65e3006aadfe2b01b1a1d',
  tests:n('tests'),pass:n('pass'),fail:n('fail'),process_exit:r.status,
  function_reference_passed:r.status===0&&n('tests')>0&&n('fail')===0,
  machine_changed:false,chain_changed:false,geometry_changed:true,schematic_created:false,
  physical_safety_certified:false,installed_in_live_viewer:false,production_ready:false,
  physical_mounting_audit:'mechanical_audit.json: new CAD overlaps; reach_audit.json: saved QR poses; production details remain open',
  open:['remaining mechanical details recorded in NASIL.md','safety circuit and PL calculation',
    'robot and rail safe standstill / safe clearance','human presence and escape provision',
    'final robot identity FR5 versus UR10e','live scene integration']};
fs.writeFileSync(path.join(dir,'audit.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));
if(!result.function_reference_passed) {console.error(r.stdout,r.stderr);process.exit(1);}
