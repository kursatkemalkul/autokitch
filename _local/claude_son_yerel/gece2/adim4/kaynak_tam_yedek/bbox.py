import re,sys
for f in sys.argv[1:]:
    s=open(f,'r',errors='ignore').read()
    pts=re.findall(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*,\s*([-\d.E+]+)\s*\)",s,re.I)
    if not pts: print(f,'no pts'); continue
    xs=[float(p[0]) for p in pts]; ys=[float(p[1]) for p in pts]; zs=[float(p[2]) for p in pts]
    unit='MM' if re.search(r"SI_UNIT\s*\(\s*\.MILLI\.\s*,\s*\.METRE\.",s) else ('INCH?' if 'INCH' in s.upper() else '?')
    print(f.split('/')[-1], len(pts),'pts', unit, 'X %.2f..%.2f (%.2f)'%(min(xs),max(xs),max(xs)-min(xs)), 'Y %.2f..%.2f (%.2f)'%(min(ys),max(ys),max(ys)-min(ys)), 'Z %.2f..%.2f (%.2f)'%(min(zs),max(zs),max(zs)-min(zs)))
