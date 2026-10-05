import {RobotQRInterlock} from './interlock.mjs';

// Hook for a future live scene runner. The existing machine and GLB are untouched.
// render/applyFrame is never called without permission; freeze is not physical braking.
export function createGuardedRunner({readSafety, applyFrame, freeze, writeGuardOutputs, clock}) {
  if (![readSafety, applyFrame, freeze, writeGuardOutputs, clock].every(f => typeof f === 'function'))
    throw Error('Required safety/animation adapter missing');
  const interlock = new RobotQRInterlock();
  return {
    step(frame, command = {}) {
      const outputs = interlock.tick(readSafety(), clock(), command);
      writeGuardOutputs(outputs);
      if (outputs.robotMotionPermit) applyFrame(frame);
      else freeze(outputs.reason);
      return outputs;
    }
  };
}
