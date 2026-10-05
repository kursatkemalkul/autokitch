"""Connection timing audit for six bench supports; geometric tooling separate."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[4];O=ROOT/'_local/codex_k_montaj';D=json.loads((O/'support_workshop.json').read_text(encoding='utf8'))
steps=D['events'];settled=set();pending={};parents={};clamp_part={};active=set();fail=[];trace=[]
def fixed(part,seen=None):
    seen=set() if seen is None else set(seen)
    if part in seen:return False
    seen.add(part)
    if any(unit in active and owner==part for unit,owner in clamp_part.items()):return True
    return part in parents and fixed(parents[part],seen)
def unit(name):
    for suffix in ('_govde','_mil','_pabuc'):
        if name.endswith(suffix):return name[:-len(suffix)]
    raise ValueError(name)
for e in steps:
    n=e['number'];op=e['operation']
    for loaded in e.get('loads',[]):
        if not fixed(loaded):fail.append({'step':n,'rule':'load on unfixed product','loaded':loaded})
    if op=='arrive':
        part=e['nodes'][0];settled.add(part)
        if e.get('temporary_supported'):
            due=e.get('fixed_at_step');text=e.get('warning','')
            if not due or due<=n or str(due) not in text:fail.append({'step':n,'rule':'missing exact temporary support warning','part':part})
            else:
                target=steps[due-1]
                if part not in target.get('fixes',[]):fail.append({'step':n,'rule':'warning points to unrelated fixing step','part':part})
                pending[part]=due
    if op=='clamp_close':
        key=unit(e['nodes'][0]);active.add(key)
        for part in e['fixes']:clamp_part[key]=part;pending.pop(part,None)
    if op=='clamp_open':active.discard(unit(e['nodes'][0]))
    if op=='weld':
        parent=e['onto']
        if not fixed(parent):fail.append({'step':n,'rule':'welding onto unfixed carrier','part':parent})
        for part in e['fixes']:parents[part]=parent;pending.pop(part,None)
        for seam in e['nodes']:settled.add(seam);parents[seam]=parent
    for part in settled:
        if not fixed(part) and part not in pending:fail.append({'step':n,'rule':'unfixed settled product without warning','part':part})
    trace.append({'step':n,'settled_product_count':len(settled),'active_clamp_count':len(active),'temporary_supported':dict(pending)})
final_unfixed=[part for part in settled if not fixed(part)]
report={'scope':'six bench support connection timing only','events':len(steps),'settled_product_parts':len(settled),'expected_product_parts':D['product_parts'],'failures':fail,'final_unfixed_parts':final_unfixed,'temporary_pending_at_end':pending,'trace':trace,
        'passed':not fail and not final_unfixed and not pending and len(settled)==D['product_parts'],'fixture_geometry_and_force_verified':False,'torch_paths_verified':False,'manufacturing_verified':False,'whole_K_release':False}
(O/'support_sequence_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in report.items() if k!='trace'},ensure_ascii=False));sys.exit(0 if report['passed'] else 2)
