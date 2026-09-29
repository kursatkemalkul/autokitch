// Concept geometry in millimetres, based on live v75 / kesme_cad_v6.
export const P=Object.freeze({W:400,D:909,H:1862,front:79,back:-830,band:996,oven:998,box:937.6,mould:981.5,R:150,guard:158,cutStroke:125,cutX:200,cutZ:-170,boxX:660,boxZ:-206,shoulderX:210,shoulderZ:-670,L1:180,L2:430,period:20});
const clamp=x=>Math.max(0,Math.min(1,x));
export const ease=(a,b,t)=>{let u=clamp((t-a)/(b-a));return u*u*(3-2*u)};
export function ik(x,z){let dx=x-P.shoulderX,dz=z-P.shoulderZ,d=Math.hypot(dx,dz);let c=(P.L1**2+d*d-P.L2**2)/(2*P.L1*d);if(Math.abs(c)>1)throw Error('Kol erişimi dışı');let q=Math.atan2(dz,dx)+Math.acos(c);return {x:P.shoulderX+P.L1*Math.cos(q),z:P.shoulderZ+P.L1*Math.sin(q),q};}
export function state(t){
 t=Math.max(0,Math.min(P.period,t));
 let cut=125*ease(4,5.4,t)*(1-ease(5.7,6.5,t));
 let push=ease(8.5,10.1,t),back=ease(11.6,13.7,t),approach=ease(6.6,7.8,t);
 let fx=30+15*approach+5*ease(8.3,8.5,t)+460*push;
 let fz=-350+180*approach-36*ease(8.5,8.9,t);
 let lift=60*(1-ease(7.95,8.3,t))+60*ease(11.2,11.6,t);
 if(t>=10.4)fx=510-160*ease(10.4,11.2,t);
 if(t>=11.6){fx=350+(30-350)*back;fz=-206+(-350+206)*back;lift=60;}
 let x=-170+370*ease(.3,2.3,t);if(t>=8.5)x=200+460*push;
 let z=-170-36*ease(8.5,8.9,t),y=996;
 if(x-150>397)y=996-14.5*clamp((x-150-397)/53);
 if(t>=10.1)y=981.5-43.9*ease(10.1,10.4,t);
 let drop=14.5*clamp((x-150-397)/53)*(1-ease(11.2,11.6,t));
 let phase=t<2.3?'01 · Fırından K bandına':t<3.8?'02 · Tereyağı spreyi':t<6.5?'03 · Kesme ve kafayı kaldırma':t<8.5?'04 · Katlanır itici arkaya yerleşir':t<10.1?'05 · Kutuya itme':t<13.7?'06 · İticiyi kaldırıp geri toplama':'07 · Yeni ürünü bekleme';
 return {t,cut,fx,fz,lift:lift-drop,elbow:ik(fx-12,fz),x,y,z,phase,spray:t>=2.6&&t<3.8,marks:t>=5.4,visible:t<15};
}
