# -*- coding: utf-8 -*-
# CadQuery montajı → gölgeli SVG önizleme (bağımlılıksız: tessellate + painter's algorithm)
import io, math

def render(asm, path, size=(1500,1150), eye=(1.0,-1.35,0.75), up=(0,0,1), margin=60, bg='#f6f7f9', light=(0.35,-0.75,0.62)):
    ex,ey,ez = eye; n=math.sqrt(ex*ex+ey*ey+ez*ez); f=(-ex/n,-ey/n,-ez/n)       # eye = kamera KONUMU yönü; f = bakış yönü (kamera → sahne)
    ux,uy,uz = up
    rx,ry,rz = f[1]*uz-f[2]*uy, f[2]*ux-f[0]*uz, f[0]*uy-f[1]*ux                # right = f × up
    rn=math.sqrt(rx*rx+ry*ry+rz*rz); r=(rx/rn,ry/rn,rz/rn)
    ux,uy,uz = r[1]*f[2]-r[2]*f[1], r[2]*f[0]-r[0]*f[2], r[0]*f[1]-r[1]*f[0]     # true up = right × f
    u=(ux,uy,uz)
    ln=math.sqrt(sum(c*c for c in light)); L=tuple(c/ln for c in light)
    tris=[]
    for ch in asm.traverse():
        obj = ch[1] if isinstance(ch,tuple) else ch
        shape = getattr(obj,'obj',None)
        if shape is None: continue
        try: shape = shape.val() if hasattr(shape,'val') else shape
        except Exception: pass
        loc = obj.loc
        try: sh = shape.moved(loc) if hasattr(shape,'moved') else shape
        except Exception: sh = shape
        col = obj.color.toTuple()[:3] if getattr(obj,'color',None) else (0.78,0.79,0.81)
        try: vs, ts = sh.tessellate(0.6)
        except Exception: continue
        P=[(v.x,v.y,v.z) for v in vs]
        for a,b,c in ts:
            tris.append((P[a],P[b],P[c],col))
    if not tris: raise RuntimeError('tessellate bos')
    def proj(p): return (p[0]*r[0]+p[1]*r[1]+p[2]*r[2], p[0]*u[0]+p[1]*u[1]+p[2]*u[2])
    def depth(p): return p[0]*f[0]+p[1]*f[1]+p[2]*f[2]
    pts=[proj(p) for t in tris for p in t[:3]]
    x0=min(p[0] for p in pts); x1=max(p[0] for p in pts); y0=min(p[1] for p in pts); y1=max(p[1] for p in pts)
    W,H=size; s=min((W-2*margin)/(x1-x0), (H-2*margin)/(y1-y0)); ox=(W-(x1-x0)*s)/2-x0*s; oy=(H-(y1-y0)*s)/2+y1*s
    def sc(p): q=proj(p); return (ox+q[0]*s, oy-q[1]*s)
    tris.sort(key=lambda t: -(depth(t[0])+depth(t[1])+depth(t[2]))/3.0)   # uzaktan yakına
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="%s"/>'%(W,H,W,H,W,H,bg)]
    for a,b,c,col in tris:
        nx=(b[1]-a[1])*(c[2]-a[2])-(b[2]-a[2])*(c[1]-a[1]); ny=(b[2]-a[2])*(c[0]-a[0])-(b[0]-a[0])*(c[2]-a[2]); nz=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        nn=math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0; nx,ny,nz=nx/nn,ny/nn,nz/nn
        if nx*f[0]+ny*f[1]+nz*f[2] > 0: nx,ny,nz=-nx,-ny,-nz                     # kameraya bak
        d=max(0.0, -(nx*L[0]+ny*L[1]+nz*L[2])); sh=0.34+0.66*d
        rgb=tuple(max(0,min(255,int(255*ch*sh))) for ch in col)
        p1,p2,p3=sc(a),sc(b),sc(c)
        out.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="rgb(%d,%d,%d)" stroke="rgb(%d,%d,%d)" stroke-width="0.35"/>'%(p1[0],p1[1],p2[0],p2[1],p3[0],p3[1],rgb[0],rgb[1],rgb[2],rgb[0],rgb[1],rgb[2]))
    out.append('</svg>')
    io.open(path,'w',encoding='utf-8').write('\n'.join(out))
    return path
