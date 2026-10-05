"""K-only scheduling adapter: stop evaluating an already failed candidate.
Unchanged v6 serbest/CCD and tolerances test every segment of an accepted path.
No geometry, exemption or safety tolerance changes; shared infrastructure stays intact.
"""
def install(ns):
    original=ns['yol_sec']
    def select(adlar, adaylar, denetle=True):
        first=None;tried=[]
        for ci,path in enumerate(adaylar):
            bad=[];checked=0
            if denetle:
                for p,q in zip(path[:-1],path[1:]):
                    checked+=1
                    bad=ns['serbest'](adlar,p,ns['YERINDE'],ofs2=q)
                    if bad:break
            if first is None:first=(path,bad)
            tried.append((ns['np'].round(path[0]).tolist(),sorted(set(b for _,b in bad))[:3]))
            if not bad:
                assert not denetle or checked==len(path)-1
                return path
        ns['PLAN_SORUN'].append(dict(parca=list(adlar)[:4],sorun=first[1][:4],tum=tried[:8],failed_candidates_short_circuited=True))
        return first[0]
    ns['yol_sec']=select
    return original
