"""Deterministic circular fillets. Never reduce a specified bend radius silently."""
import numpy as np
import math

def rounded(raw,radius):
    p=np.asarray(raw,float);u=np.diff(p,axis=0);length=np.linalg.norm(u,axis=1);u=u/length[:,None]
    trims=np.zeros(len(p));angles=np.zeros(len(p))
    for i in range(1,len(p)-1):
        angles[i]=math.acos(float(np.clip(u[i-1]@u[i],-1,1)))
        trims[i]=radius*math.tan(angles[i]/2)
    if np.any(trims[:-1]+trims[1:]>length+1e-9):
        raise ValueError(f'Insufficient straight for R={radius}: {raw}')
    points=[p[0]];arcs=[]
    def line(q):
        a=points[-1];d=np.linalg.norm(q-a)
        if d>1e-10:points.extend(a+(q-a)*t for t in np.linspace(0,1,max(2,math.ceil(d/.008)+1))[1:])
    for i in range(1,len(p)-1):
        if angles[i]<1e-8:continue
        start=p[i]-u[i-1]*trims[i];line(start)
        n=(u[i]-(u[i]@u[i-1])*u[i-1])/math.sin(angles[i]);centre=start+n*radius;v=start-centre
        first=len(points)-1
        for a in np.linspace(0,angles[i],math.ceil(angles[i]/.025)+1)[1:]:points.append(centre+v*math.cos(a)+u[i-1]*radius*math.sin(a))
        arcs.append({'radius_m':radius,'first':first,'last':len(points)-1,'angle_rad':angles[i]})
    line(p[-1]);return {'points':np.asarray(points).tolist(),'arcs':arcs,'minimum_radius_m':radius}

def ramp(end=(3.018,.058,1.185),radius=.065,dy=.080):
    x,y,z=end;theta=math.acos(1-dy/(2*radius));span=2*radius*math.sin(theta);x0=x-span;y0=y-dy
    a=[[x0+radius*math.sin(t),y0+radius*(1-math.cos(t)),z] for t in np.linspace(0,theta,49)]
    a.extend([[x-radius*math.sin(t),y-radius+radius*math.cos(t),z] for t in np.linspace(theta,0,49)[1:]])
    return {'points':a,'arcs':[{'radius_m':radius,'first':0,'last':48,'angle_rad':theta},{'radius_m':radius,'first':48,'last':96,'angle_rad':theta}],'minimum_radius_m':radius}
