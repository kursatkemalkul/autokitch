import test from 'node:test';
import assert from 'node:assert/strict';
import {RobotQRInterlock} from '../../../otonom/hat/robot-safety-v1/interlock.mjs';
import {createGuardedRunner} from '../../../otonom/hat/robot-safety-v1/adapter.mjs';
const healthy = () => ({sampleMs:0, sequence:0, safetyHealthy:true, externalPermit:[true,true],
  cellDoorClosed:[true,true], cellOccupied:false, standstill:[true,true], robotZones:[],
  bays:Array.from({length:12},()=>({closed:[true,true],locked:[true,true]})),
  zoneClear:Array.from({length:12},()=>[true,true])});
function setup() {
  const ctrl = new RobotQRInterlock(), input = healthy(); let time=0;
  const step = (cmd={}) => {input.sampleMs=++time; input.sequence++; return ctrl.tick(input,time,cmd);};
  return {ctrl,input,step};
}
function running() {const s=setup(); s.step({reset:true}); assert.equal(s.step({start:true}).robotMotionPermit,true);return s;}
test('startup, reset then distinct start, no auto restart after cell opening',()=>{
  const {input,step}=setup();
  assert.equal(step({start:true}).robotMotionPermit,false);
  assert.equal(step({reset:true,start:true}).robotMotionPermit,false);
  step(); assert.equal(step({start:true}).robotMotionPermit,true);
  input.cellDoorClosed=[false,false];assert.equal(step().safeguardStopDemand,true);
  input.cellDoorClosed=[true,true];assert.equal(step().robotMotionPermit,false);
  assert.equal(step({start:true}).robotMotionPermit,false);
  step({reset:true});assert.equal(step({start:true}).robotMotionPermit,true);
});
for(let bay=0;bay<12;bay++) {
  test(`bay ${bay}: reserve, no unlock during robot presence, lock loss stops`,()=>{
    const {input,step}=running();let o=step({requestRobotBay:bay});
    assert.equal(o.entryPermits[bay],true);
    input.robotZones=[bay];input.zoneClear[bay]=[false,false];input.standstill=[false,false];
    o=step({requestCustomer:bay});assert.equal(o.robotMotionPermit,false);
    assert.equal(o.lockCommands[bay],true);assert.equal(o.customerUnlockPermits[bay],false);
    input.bays[bay].locked=[false,true];o=step();
    assert.ok(o.faults.includes('ACTIVE_BAY_LOCK_LOST'));assert.equal(o.safeguardStopDemand,true);
  });
  test(`bay ${bay}: all closed/locked before entry; customer may unlock only after stop and exit`,()=>{
    const {input,step}=running();
    input.standstill=[false,false];let o=step({requestCustomer:bay});
    assert.equal(o.lockCommands[bay],true);
    input.standstill=[true,true];o=step();assert.equal(o.customerUnlockPermits[bay],true);
    assert.equal(o.lockCommands.filter(x=>!x).length,1);
    input.bays[bay]={closed:[false,false],locked:[false,false]};
    assert.equal(step().robotMotionPermit,false);
    input.bays[bay]={closed:[true,true],locked:[false,false]};
    assert.equal(step({finishCustomer:true,reset:true}).robotMotionPermit,false);
    input.bays[bay].locked=[true,true];step({finishCustomer:true});step({reset:true});
    assert.equal(step({start:true}).robotMotionPermit,true);
  });
  test(`bay ${bay}: opening any customer guard stops global motion`,()=>{
    const {input,step}=running();input.bays[bay].closed=[false,true];
    assert.equal(step().robotMotionPermit,false);
  });
  test(`bay ${bay}: robot exit must be confirmed, not just commanded`,()=>{
    const {input,step}=running();step({requestRobotBay:bay});
    input.robotZones=[bay];input.zoneClear[bay]=[false,false];
    assert.equal(step({finishRobotBay:true}).activeBay,bay);
    input.robotZones=[];input.zoneClear[bay]=[true,true];
    assert.equal(step({finishRobotBay:true}).activeBay,null);
  });
}
for(const [name,mutate] of [
  ['gate channel loss',i=>i.cellDoorClosed=[true,false]],
  ['controller fault',i=>i.safetyHealthy=false],
  ['external stop',i=>i.externalPermit=[false,false]],
  ['person present',i=>i.cellOccupied=true],
  ['person unknown',i=>delete i.cellOccupied],
  ['missing bay',i=>i.bays.pop()],
  ['missing zones',i=>delete i.zoneClear],
  ['unknown zone channel',i=>i.zoneClear[0]=[true,false]],
  ['unreserved entry',i=>{i.robotZones=[4];i.zoneClear[4]=[false,false];}],
  ['invalid zone',i=>i.robotZones=[12]],
  ['unknown presence',i=>i.zoneClear[8]=[false,false]],
  ['lock channel loss',i=>i.bays[5].locked=[true,false]],
]) test(name,()=>{const {input,step}=running();mutate(input);assert.equal(step().robotMotionPermit,false);});
test('freshness, sequence reuse, stale/future data, backwards time fail closed',()=>{
  for(const change of [i=>i.sampleMs=-1000,i=>i.sampleMs=9999,i=>i.sequence=-1,i=>i.sequence=0]){
    const {input,ctrl}=running();change(input);assert.equal(ctrl.tick(input,10).robotMotionPermit,false);
  }
  const {input,ctrl}=running();assert.equal(ctrl.tick(input,0).robotMotionPermit,false);
});
test('commands cannot bypass sensor truth',()=>{
  const {input,step}=running();input.bays[1].locked=[false,false];
  const o=step({requestRobotBay:1,start:true,reset:true});assert.equal(o.entryPermits.some(Boolean),false);
});
test('scene adapter does not apply a frame with a stop demand',()=>{
  let applied=0,frozen=0,time=0;const input=healthy();
  const runner=createGuardedRunner({clock:()=>time,readSafety:()=>input,
    applyFrame:()=>applied++,freeze:()=>frozen++,writeGuardOutputs:()=>{}});
  function step(cmd){input.sampleMs=++time;input.sequence++;return runner.step({},cmd);}
  step();step({reset:true});step({start:true});assert.equal(applied,1);
  input.cellDoorClosed=[false,false];step();assert.equal(applied,1);assert.equal(frozen,3);
});
