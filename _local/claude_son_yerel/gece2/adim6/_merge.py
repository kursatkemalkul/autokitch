s=open('g6_montaj.py',encoding='utf-8').read()
ek=open('seq_ek.py',encoding='utf-8').read()
k="SEQ = {'A': seq_A}"
i=s.index(k)
s=s[:i]+ek+"\n\nSEQ = {'A': seq_A, 'B': seq_B, 'E': seq_E, 'U': seq_U}"+s[i+len(k):]
open('g6_montaj.py','w',encoding='utf-8').write(s)
