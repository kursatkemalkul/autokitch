import pickle,sys
R=pickle.load(open('_bulgu.pkl','rb'))
tt=sys.argv[1:]
for b in R['B']:
    if any(b['tur'].startswith(t) for t in tt):
        print(b['tur'][:22].ljust(22),b['istasyon'][:5].ljust(5),b['bilesen'][:30].ljust(30),str(b['parca'])[:36].ljust(36),b['konum_mm'],b['aciklama'][:170])
