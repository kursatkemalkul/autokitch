// Same circular-fillet rule as routing.py; preserve radius or fail.
export function rounded(raw,radius){
 const sub=(a,b)=>a.map((v,i)=>v-b[i]),plus=(a,b)=>a.map((v,i)=>v+b[i]),mul=(a,s)=>a.map(v=>v*s),dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),norm=a=>Math.hypot(...a);
 const edges=raw.slice(1).map((p,i)=>sub(p,raw[i])),length=edges.map(norm),u=edges.map((p,i)=>mul(p,1/length[i])),angles=raw.map(()=>0),trims=raw.map(()=>0),points=[raw[0]];
 for(let i=1;i<raw.length-1;i++){angles[i]=Math.acos(Math.max(-1,Math.min(1,dot(u[i-1],u[i]))));trims[i]=radius*Math.tan(angles[i]/2);}
 if(length.some((v,i)=>trims[i]+trims[i+1]>v+1e-9))throw Error('Insufficient straight for R'+radius+' '+JSON.stringify(raw));
 const line=q=>{const a=points.at(-1),e=sub(q,a),n=Math.max(2,Math.ceil(norm(e)/.006)+1);for(let j=1;j<n;j++)points.push(plus(a,mul(e,j/(n-1))));};
 for(let i=1;i<raw.length-1;i++){if(angles[i]<1e-8)continue;const start=sub(raw[i],mul(u[i-1],trims[i]));line(start);const n=mul(sub(u[i],mul(u[i-1],dot(u[i],u[i-1]))),1/Math.sin(angles[i])),centre=plus(start,mul(n,radius)),v=sub(start,centre),N=Math.ceil(angles[i]/.025);for(let j=1;j<=N;j++){const a=angles[i]*j/N;points.push(plus(centre,plus(mul(v,Math.cos(a)),mul(u[i-1],radius*Math.sin(a)))));}}
 line(raw.at(-1));return {points,minimum_radius_m:radius};
}
