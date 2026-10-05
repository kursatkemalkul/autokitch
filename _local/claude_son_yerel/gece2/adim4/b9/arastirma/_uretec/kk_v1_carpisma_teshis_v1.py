"""Read-only geometry audit of KK v1; writes a separate diagnostic report.

Broad phase covers every distinct moving group against all other parts.
Narrow phase proves collisions, never treats untested candidates as passes.
This is sampled geometry, NOT continuous collision detection or a safety test.
"""
import json
import os
import time
from collections import defaultdict
import numpy as np
import kk_kompakt_v1 as M


def run(source_name='kk_kompakt_v1.py'):
    start = time.monotonic()
    M.build()
    print('Built', len(M.P), 'parts', flush=True)
    names = [p['name'] for p in M.P]
    groups = [p['group'] for p in M.P]
    corners = []
    for p in M.P:
        b = p['shape'].BoundingBox()
        corners.append(np.array([[x, y, z, 1] for x in (b.xmin, b.xmax)
            for y in (b.ymin, b.ymax) for z in (b.zmin, b.zmax)]))
    times = np.unique(np.r_[np.arange(0, 19.301, .25),
        [.55, 1.8, 2.15, 2.45, 2.8, 3.2, 3.35, 4.25, 5.5, 6.8,
         7.5, 10.1, 11.5, 12.6, 13.8, 14.4, 15.2, 16.2, 17.6, 18.2]])
    matrices = {float(t): {g: M.transform(g, float(t)) for g in M.G} for t in times}
    moving = {g for g in M.G if any(not np.allclose(matrices[float(t)][g], matrices[0.][g]) for t in times)}
    candidates = defaultdict(dict)
    for t in times:
        lo, hi, active = [], [], []
        for i, p in enumerate(M.P):
            mat = matrices[float(t)][groups[i]].copy()
            active.append(abs(np.linalg.det(mat[:3, :3])) > .5)
            mat[:3, 3] -= mat[:3, :3] @ M.G[groups[i]]['pivot']
            v = (mat @ corners[i].T).T[:, :3]
            lo.append(v.min(0)); hi.append(v.max(0))
        lo, hi = np.array(lo), np.array(hi)
        overlap = np.minimum(hi[:, None, :], hi[None, :, :]) - np.maximum(lo[:, None, :], lo[None, :, :])
        mask = np.triu(np.all(overlap > .1, axis=2), 1)
        for i, j in zip(*np.where(mask)):
            a, b = groups[i], groups[j]
            if not active[i] or not active[j] or a == b or 'SPRAY' in (a, b):
                continue
            if a not in moving and b not in moving:
                continue
            key = tuple(sorted((a, b)))
            score = float(np.prod(overlap[i, j]))
            prev = candidates[key].get((i, j))
            if prev is None or score > prev['aabb_overlap_mm3']:
                candidates[key][i, j] = dict(a=names[i], b=names[j], time=float(t), aabb_overlap_mm3=score)
    print('Broad phase:', len(times), 'poses;', len(moving), 'moving groups;',
          len(candidates), 'group-pair candidates', flush=True)
    proofs, unresolved, tested = [], [], 0
    # Each group pair gets a proof search; group ordering is independent of rendering.
    for key, pairs in sorted(candidates.items()):
        proved = False
        for (i, j), hit in sorted(pairs.items(), key=lambda q: -q[1]['aabb_overlap_mm3'])[:8]:
            if tested >= 160 or time.monotonic() - start > 200:
                break
            tested += 1
            try:
                vol = M.world_shape(M.P[i], hit['time']).intersect(M.world_shape(M.P[j], hit['time'])).Volume()
                if vol > 1:
                    proofs.append(dict(groups=key, **hit, volume_mm3=round(vol, 3),
                        classification='REVIEW_REQUIRED: intentional contact not automatically excluded'))
                    print('INTERSECTION', key, hit['time'], hit['a'], '/', hit['b'], round(vol, 1), flush=True)
                    proved = True
                    break
            except Exception as exc:
                print('BOOL_ERROR', key, type(exc).__name__, flush=True)
        if not proved:
            unresolved.append(dict(groups=key, candidates=len(pairs), status='UNRESOLVED_NOT_A_PASS'))
    report = dict(status='INVALID_LAYOUT_IF_UNINTENDED_INTERSECTIONS',
        source=source_name, sampled_poses=times.tolist(),
        moving_groups=sorted(moving), group_pair_candidates=len(candidates),
        exact_boolean_tests=tested, intersection_proofs=proofs, unresolved_group_pairs=unresolved,
        broad_phase_candidates=[dict(groups=k, candidates=list(v.values())) for k, v in sorted(candidates.items())],
        limitations=['No continuous collision certification', 'Same rigid group and static-static pairs excluded',
                    'Food/cutter and pin/bearing contacts require semantic review',
                    'At most eight representative part-pairs per group pair; untested pairs not passed'],
        elapsed_seconds=round(time.monotonic()-start, 2))
    path = M.OUT / 'carpisma_teshis_v1.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('REPORT', path, 'PROOFS', len(proofs), 'TESTS', tested, 'TIME', report['elapsed_seconds'], flush=True)


if __name__ == '__main__':
    run()
    os._exit(0)
