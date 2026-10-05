import json,struct,sys,re
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
s=json.dumps(J,ensure_ascii=False)
for m in re.finditer(r'salter|SALTER|iSW',s): print(s[max(0,m.start()-200):m.end()+200].replace('\n',' ')); print('==')
