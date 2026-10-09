// Same length-preserving tip illustration as finger_bend.py; not a pressure law.
export function bendAngle(shift){
 if(shift < -11.000001 || shift > 5.000001)throw Error('Uç hareketi sınır dışında');
 if(Math.abs(shift)<1e-10)return 0;
 let lo=0,hi=85*Math.PI/180;
 for(let i=0;i<48;i++){const a=(lo+hi)/2,travel=.006/a*(1-Math.cos(a))+.0092*Math.sin(a);if(travel<Math.abs(shift)*.001)lo=a;else hi=a;}
 return Math.sign(shift)*(lo+hi)/2;
}
export function bendVertex(x,y,z,a){
 if(z<=.026||Math.abs(a)<1e-10)return [x,y,z];
 const t=Math.max(0,Math.min(.006,z-.026)),theta=a*t/.006,r=.006/a,tail=Math.max(0,z-.032);
 return [-.0105-r*(1-Math.cos(theta))+(x+.0105)*Math.cos(theta)-tail*Math.sin(theta),y,.026+r*Math.sin(theta)+(x+.0105)*Math.sin(theta)+tail*Math.cos(theta)];
}
