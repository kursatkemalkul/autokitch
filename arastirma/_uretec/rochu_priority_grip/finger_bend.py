"""Tip-only kinematic illustration on the supplied, unscaled STEP tessellation.

The housing and thick shoulder (local z <= 26 mm) are immutable. A 6 mm
neck bends in an arc, followed by the straight 9.2 mm distal pad. This is
NOT a material/pressure law: the catalogue gives unloaded travel, not FEM.
Positive shift closes this reversed mounting. Dimensions are in metres.
The browser uses the identical equations in finger-bend.js.
"""
import numpy as np
from functools import lru_cache

START=.026
NECK=.006
END=.0412
AXIS_X=-.0105
MIN_SHIFT=-11.
MAX_SHIFT=5.

@lru_cache(maxsize=512)
def bend_angle(shift):
    shift=float(shift)
    if not MIN_SHIFT-1e-6 <= shift <= MAX_SHIFT+1e-6:
        raise ValueError('Requested tip displacement exceeds the illustrative catalogue interval')
    if abs(shift)<1e-10:return 0.
    # Solve displacement of the distal centreline, preserving its length.
    lo,hi=0.,np.deg2rad(85.)
    for _ in range(48):
        a=(lo+hi)/2
        travel=NECK/a*(1-np.cos(a))+(END-START-NECK)*np.sin(a)
        if travel<abs(shift)*.001:lo=a
        else:hi=a
    return float(np.copysign((lo+hi)/2,shift))

def deform(vertices,shift):
    v=np.asarray(vertices);out=v.copy();a=bend_angle(round(float(shift),8))
    if abs(a)<1e-10:return out
    moving=v[:,2]>START
    t=np.clip(v[:,2]-START,0,NECK);theta=a*t/NECK
    r=NECK/a;tail=np.maximum(v[:,2]-START-NECK,0)
    x=AXIS_X-r*(1-np.cos(theta))+(v[:,0]-AXIS_X)*np.cos(theta)-tail*np.sin(theta)
    z=START+r*np.sin(theta)+(v[:,0]-AXIS_X)*np.sin(theta)+tail*np.cos(theta)
    out[moving,0]=x[moving];out[moving,2]=z[moving]
    return out
