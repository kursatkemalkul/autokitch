import sys; sys.argv=['x']
exec(open('hesap.py',encoding='utf-8').read().split('R = {}')[0])
top=[(1753,-560),(1943,-560),(1943,-201),(1879.1,-201),(1879.1,-120),(1753,-120)]
print('cep(L-kesit) alt2', round(hazne(1848,0,0,180,35,top=top)[0],2))
print('harc 2129 (ust +30)', round(hazne(1722,1532,1912,180,242)[0],2))
print('alt1 on +60 (z -60)', round(hazne(1596,1501,1691,180,35,top=rect(1501,1691,-560,-60))[0],2))
