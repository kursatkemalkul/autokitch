import sys, json, struct, numpy as np
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
print('nodes',len(J['nodes']),'anims',len(J.get('animations',[])))
for a in J.get('animations',[]):
    tg={}
    for c in a['channels']:
        n=J['nodes'][c['target']['node']].get('name'); tg.setdefault(n,set()).add(c['target']['path'])
    print(a.get('name'), len(a['channels']))
    for n,s in tg.items():
        if 'TOPPING' in n: print('   ',n,s)
for i,nd in enumerate(J['nodes']):
    n=nd.get('name','')
    if 'TOPPING' in n and ('DONER' in n or 'PISTON' in n): print(i,n,{k:nd[k] for k in nd if k in('translation','rotation','children','mesh')})
print(J['scenes'][0].get('extras',{}).keys())
