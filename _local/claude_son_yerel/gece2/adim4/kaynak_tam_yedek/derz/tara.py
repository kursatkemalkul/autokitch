import json,sys
d=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'm8_parca.json'));P=d['parca']
R=[]
for i,p in enumerate(P):
  lo,hi=p['lo'],p['hi']
  if hi[2]>=70 and hi[0]-lo[0]>60 and hi[1]-lo[1]>60 and lo[1]>-50:
    R.append((i,p['ad'][:34],lo[0],hi[0],lo[1],hi[1],hi[2]))
# dedupe identical rect
seen={};RR=[]
for r in R:
  k=tuple(round(v,1) for v in r[2:6])
  if k in seen: continue
  seen[k]=1;RR.append(r)
R=RR
print(len(R),'on panel')
for r in sorted(R,key=lambda r:(r[2],r[4])): print('  %-34s x %7.1f-%7.1f y %7.1f-%7.1f z %.1f'%(r[1],r[2],r[3],r[4],r[5],r[6]))
out=[]
for a in R:
  for b in R:
    if a is b: continue
    # b ustte a altta: dikey komsu
    gy=b[4]-a[5]
    if 0<=gy<=8 and min(a[3],b[3])-max(a[2],b[2])>-30:
      for ea in (a[2],a[3]):
        for eb in (b[2],b[3]):
          if 0.4<abs(ea-eb)<25: out.append(('DIKEY derz kademe',round(eb-ea,2),a[1],round(ea,1),b[1],round(eb,1),'y~%.0f'%b[4]))
    gx=b[2]-a[3]
    if 0<=gx<=8 and min(a[5],b[5])-max(a[4],b[4])>-30:
      for ea in (a[4],a[5]):
        for eb in (b[4],b[5]):
          if 0.4<abs(ea-eb)<25: out.append(('YATAY derz kademe',round(eb-ea,2),a[1],round(ea,1),b[1],round(eb,1),'x~%.0f'%b[2]))
      if abs(gx-3)>0.4: out.append(('DIKEY derz genislik',round(gx,2),a[1],round(a[3],1),b[1],round(b[2],1),''))
    if 0<=gy<=8 and min(a[3],b[3])-max(a[2],b[2])>10 and abs(gy-3)>0.4: out.append(('YATAY derz genislik',round(gy,2),a[1],round(a[5],1),b[1],round(b[4],1),''))
print('== bulgular')
for o in sorted(set(out)): print(o)
