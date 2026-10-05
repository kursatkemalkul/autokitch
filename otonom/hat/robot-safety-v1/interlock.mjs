// Functional reference for web/Isaac adapters. NOT a certified safety controller.
// Physical motion permission must come from validated safety-rated hardware.
export const BAY_COUNT = 12;
const pairOK = p => Array.isArray(p) && p.length === 2 && p.every(v => v === true);
const copy = v => structuredClone(v);

export class RobotQRInterlock {
  constructor({maxAgeMs = 100} = {}) {
    if (!Number.isFinite(maxAgeMs) || maxAgeMs <= 0) throw Error('maxAgeMs');
    this.maxAgeMs = maxAgeMs; // Simulation watchdog; hardware timing remains unvalidated.
    this.mode = 'STOPPED';
    this.reason = 'INITIAL_RESET_REQUIRED';
    this.activeBay = null;
    this.customerBay = null;
    this.resetRequired = true;
    this.previousReset = false;
    this.previousStart = false;
    this.lastNow = -Infinity;
    this.lastSequence = -1;
    this.lastSnapshot = null;
  }

  stop(reason) {
    this.mode = 'STOPPED';
    this.reason = reason;
    this.resetRequired = true;
    // Keep the active bay reserved and locked during braking / a fault.
  }

  validIndex(i) { return Number.isInteger(i) && i >= 0 && i < BAY_COUNT; }

  tick(input, nowMs, command = {}) {
    const resetEdge = command.reset === true && !this.previousReset;
    const startEdge = command.start === true && !this.previousStart;
    this.previousReset = command.reset === true;
    this.previousStart = command.start === true;
    const faults = [];
    if (!Number.isFinite(nowMs) || nowMs < this.lastNow) faults.push('CLOCK_INVALID');
    else this.lastNow = nowMs;
    if (!input || !Number.isFinite(input.sampleMs) || input.sampleMs > nowMs ||
        nowMs - input.sampleMs > this.maxAgeMs || !Number.isInteger(input.sequence) ||
        input.sequence < 0 || input.sequence < this.lastSequence) faults.push('INPUT_STALE_OR_INVALID');
    // Replaying a sequence with changed values is not a fresh safety measurement.
    if (input && input.sequence === this.lastSequence && JSON.stringify(input) !== this.lastSnapshot)
      faults.push('INPUT_SEQUENCE_REUSED');
    if (input && Number.isInteger(input.sequence) && input.sequence > this.lastSequence) {
      this.lastSequence = input.sequence;
      this.lastSnapshot = JSON.stringify(input);
    }
    if (input?.safetyHealthy !== true) faults.push('SAFETY_DEVICE_FAULT');
    if (!pairOK(input?.externalPermit)) faults.push('EXTERNAL_SAFETY_STOP');
    if (!pairOK(input?.cellDoorClosed)) faults.push('CELL_DOOR_OPEN_OR_FAULT');
    if (input?.cellOccupied !== false) faults.push('CELL_OCCUPIED_OR_UNKNOWN');
    if (!Array.isArray(input?.bays) || input.bays.length !== BAY_COUNT) faults.push('BAY_INPUT_COUNT');
    if (!Array.isArray(input?.zoneClear) || input.zoneClear.length !== BAY_COUNT) faults.push('ZONE_INPUT_COUNT');
    const allClosed = input?.bays?.length === BAY_COUNT && input.bays.every(b => pairOK(b.closed));
    const allLocked = input?.bays?.length === BAY_COUNT && input.bays.every(b => pairOK(b.locked));
    const allClear = input?.zoneClear?.length === BAY_COUNT && input.zoneClear.every(pairOK);
    const stopped = pairOK(input?.standstill);
    const zones = input?.robotZones;
    if (!Array.isArray(zones) || zones.some(i => !this.validIndex(i)) || new Set(zones).size !== zones.length)
      faults.push('ROBOT_ZONE_INVALID');
    else if (zones.some(i => i !== this.activeBay)) faults.push('UNRESERVED_ZONE_ENTRY');
    if (Array.isArray(zones) && zones.some(i => pairOK(input?.zoneClear?.[i])))
      faults.push('ZONE_FEEDBACK_CONTRADICTION');
    if (Array.isArray(input?.zoneClear) && input.zoneClear.some(p =>
        !Array.isArray(p) || p.length !== 2 || !p.every(v => typeof v === 'boolean') || p[0] !== p[1]))
      faults.push('ZONE_CHANNEL_FAULT');
    if (this.mode === 'RUNNING' && Array.isArray(input?.zoneClear) && input.zoneClear.some((p, i) =>
        !pairOK(p) && !zones?.includes(i))) faults.push('ZONE_PRESENCE_UNKNOWN');
    if (this.mode === 'RUNNING' && (!allClosed || !allLocked)) faults.push('CUSTOMER_GUARD_NOT_SECURED');
    // A retained occupied bay always needs both closed AND locked feedback.
    if (this.activeBay !== null && (!pairOK(input?.bays?.[this.activeBay]?.closed) ||
        !pairOK(input?.bays?.[this.activeBay]?.locked))) faults.push('ACTIVE_BAY_LOCK_LOST');
    if (faults.length) this.stop(faults[0]);

    if (command.requestCustomer !== undefined) {
      const i = command.requestCustomer;
      if (this.validIndex(i) && (this.customerBay === null || this.customerBay === i)) {
        // First request stop. Unlock is permitted only AFTER measured standstill.
        this.customerBay = i;
        this.stop('CUSTOMER_ACCESS_REQUESTED');
      } else this.stop('CUSTOMER_REQUEST_INVALID');
    }
    if (command.finishRobotBay === true) {
      if (this.activeBay !== null && pairOK(input?.zoneClear?.[this.activeBay]) && zones?.length === 0)
        this.activeBay = null;
      else this.stop('ROBOT_EXIT_NOT_CONFIRMED');
    }
    if (command.finishCustomer === true) {
      if (this.customerBay !== null && pairOK(input?.bays?.[this.customerBay]?.closed) &&
          pairOK(input?.bays?.[this.customerBay]?.locked)) this.customerBay = null;
      // Re-lock and measure before reset. No implicit resume.
    }
    const guardsReady = faults.length === 0 && allClosed && allLocked && allClear &&
      stopped && zones?.length === 0 && this.customerBay === null && this.activeBay === null;
    if (resetEdge && guardsReady) {
      this.resetRequired = false;
      this.mode = 'ARMED';
      this.reason = 'EXPLICIT_START_REQUIRED';
    }
    // Reset and start on the same edge cannot start motion.
    if (startEdge && !resetEdge && !this.resetRequired && this.mode === 'ARMED' && guardsReady) {
      this.mode = 'RUNNING';
      this.reason = 'RUNNING';
    }
    if (command.requestRobotBay !== undefined) {
      const i = command.requestRobotBay;
      if (this.validIndex(i) && this.mode === 'RUNNING' && allClosed && allLocked &&
          this.customerBay === null && (this.activeBay === null || this.activeBay === i)) this.activeBay = i;
      else this.stop('ROBOT_BAY_REQUEST_DENIED');
    }
    const unlock = this.customerBay !== null && this.activeBay === null && stopped && allClear &&
      zones?.length === 0 && faults.length === 0 && this.mode === 'STOPPED';
    const permit = this.mode === 'RUNNING' && faults.length === 0 && allClosed && allLocked &&
      this.customerBay === null && !this.resetRequired;
    return copy({mode: this.mode, reason: this.reason, faults, resetRequired: this.resetRequired,
      activeBay: this.activeBay, customerBay: this.customerBay,
      robotMotionPermit: permit, safeguardStopDemand: !permit,
      lockCommands: Array.from({length: BAY_COUNT}, (_, i) => !(unlock && i === this.customerBay)),
      entryPermits: Array.from({length: BAY_COUNT}, (_, i) => permit && i === this.activeBay),
      customerUnlockPermits: Array.from({length: BAY_COUNT}, (_, i) => unlock && i === this.customerBay),
      physicalSafetyCertified: false});
  }
}
