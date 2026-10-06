"""Bind cap fabrication motion evidence; preserve outstanding release gates."""
from pathlib import Path
import hashlib
import json

H = Path(__file__).resolve().parent
def read(name):
    return json.loads((H / name).read_text(encoding='utf-8-sig'))
def sha(name):
    return hashlib.sha256((H / name).read_bytes()).hexdigest()

baseline = read('catalog_motion_audit.json')
integration = read('cap_bench_integration_audit.json')
binding = read('cap_plan_source_binding_audit.json')
plan = read('cap_plan_audit.json')
bench = read('cap_bench_prototype_audit.json')
ccd = read('full_ccd_plan_k_cap_full.json')
dense = read('cap_dense_bend_morph_audit.json')
display = read('cap_weld_display_audit.json')
interfaces = read('catalog_supplier_interfaces.json')
torch = read('cap_torch_access.json')
model = baseline['source_model_sha256']
full_hash = sha('plan_k_cap_full.pkl')
assert integration['source_model_sha256'] == binding['source_model_sha256'] == ccd['source_model_sha256'] == model
assert display['source_model_sha256'] == torch['source_model_sha256'] == model
assert binding['source_plan_sha256'] == integration['source_plan_sha256'] == sha('plan_k_cap_candidate.pkl')
assert integration['combined_plan_sha256'] == ccd['source_plan_sha256'] == dense['source_plan_sha256'] == display['source_plan_sha256'] == full_hash
assert not plan['plan_problems'] and not plan['unplanned']
assert len(bench['groups']) == 28 and all(not g['plan_problems'] for g in bench['groups'])
assert ccd['parts'] == integration['parts'] == display['physical_product_part_count'] == 1009
assert ccd['rigid_path_passed'] and not ccd['path_issues'] and ccd['step_mm'] == 2
assert dense['bend_morph_sampling_passed'] and dense['dense_plan_sha256'] == sha('plan_k_cap_dense.pkl')
assert display['physical_product_geometry_unchanged'] and display['common_player_unchanged'] and display['glb_round_trip_passed']
assert display['marker_count'] == 32
assert all(c['maximum_surface_distance_mm'] <= .01 and c['same_motion_as_real_cap'] for c in display['source_surface_checks'])
assert interfaces['remaining_count'] == 212
files = ['cap_plan_source_binding_audit.json', 'cap_plan_audit.json', 'cap_bench_prototype_audit.json', 'cap_bench_integration_audit.json', 'full_ccd_plan_k_cap_full.json', 'cap_dense_bend_morph_audit.json', 'cap_weld_display_audit.json', 'cap_torch_access.json', 'catalog_supplier_interfaces.json']
result = {
    'source_model_sha256': model,
    'source_plan_sha256': full_hash,
    'parts': 1009,
    'bench_groups': 28,
    'tested_pairs': ccd['tested_pairs'],
    'rigid_paths_passed': True,
    'bend_sampling_passed': True,
    'flush_cap_weld_operations': 4,
    'display_surface_markers': 32,
    'display_hook_checked': True,
    'whole_animation_rendered_in_browser': False,
    'remaining_connection_records': 212,
    'connection_inventory_reference_plan_sha256': sha('plan_k_catalog_full.pkl'),
    'connection_inventory_rebound_to_cap_plan': False,
    'artifacts_sha256': {name: sha(name) for name in files},
    'actual_torch_and_fixture_verified': False,
    'whole_station_connections_verified': False,
    'manufacturing_release': False,
    'production_release': False,
    'canonical_source_changed': False,
    'k_completed': False,
    'u_started': False,
}
(H / 'cap_motion_audit.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print('CAP_MOTION_BOUND', result['parts'], result['tested_pairs'], 'release', False)
