# Last local R&D state: step 55 / v9w

The filename hat3_v8.glb on the main website is the lossless meshopt copy of the final LOCAL step55 hat3_v9w.glb. It is not an older model. All 5655 accessors and all JSON metadata outside buffer layout are equal, including animation and extras.

Use this directory's hat3_v9w.glb.gz as the working input. Decompress with Python gzip to a new work directory and verify raw SHA256 in manifest.json. Do not recreate the machine from an earlier h3 version or undo steps 1-55. Make any new model correction as the next recorded step starting from this native v9w.

Read KUYRUK3.md, MONTAJ_ANIMASYON_KURALLARI.md, RAPOR.md and arastirma/_uretec/h3/yama_v9/SIRA.md. The full exact source archive is _local/claude-site-20261005/h3-source; the current h3 generators are arastirma/_uretec/h3. Session/task logs are _local/claude_oturum. Native runtime dependencies and Windows paths must be checked before execution.

Completed: queue 0 seven-product TOPPING placement (step53), step54 straight-sided diced-meat hopper, queue1 standard consistency/washers (step55).
Pending: queue2 TOPPING assembly animation, then F/K/E/U, A+drawer check, B weld visibility, full electrical+data view, final audit. QR+counter assembly animation was cancelled by Kemal. Existing animations are not evidence of assembly feasibility. Retain the documented mechanical open items.

No engineering change or new site deployment is made by this backup.

## 5 Eki güncelleme (bulut oturumu)
Working input is now hat3_v9y.glb.gz (step 57, SHA256 49fc7520579156828c3ee31c05b36aba774f99e88d0e77be5557dc2ae34dda54), not v9w. Steps 56 (evaporator foot) and 57 (service cable channel cut) are registered in zincir.py. Step 56 = 56_evap_ayak.py (registered in zincir.py, SIRA.md).
Queue item 2 (TOPPING assembly v5) done with open items listed in KUYRUK3.md; pipeline: gece2/t5 (t5_cikar → merkez_v9w → t5_parca → t5_montaj → t5_cikti). Large .pkl intermediates are not committed; rerun the pipeline.

## 5 Eki öğleden sonra — adım 58 (tek acil stop)
- Kemal: "tek bir acil butonu, o da şalterin önündeki kapakta" → F sağ üst kapağı (3625, 1600). Zincir 58: hat3_v9y → **hat3_v9z.glb.gz** (bu klasör), SHA256 (açık GLB) 94dccd07e404dd18567cb5629f78384a1ce889b6aa166734f2042e8fdca385a4, iki koşu bayt aynı.
- Ana şalter yüksekliği + servis açıklığı: Kemal "boşver" → değişmez.
- Sıradaki (branch claude/standart-makine): kapı kilit anahtarları (TOPPING, K, F, E) · A ışık perdesi kablosu · pnömatik boşaltma + yumuşak başlatma · R290 bölmesi · F davlumbaz filtresi önden · hijyen noktaları.
- Site (meshopt / mekanizma json: yeni ACIL_STOP__*__KAPAK_F_SAG düğümleri kapakla döner) henüz güncellenmedi.
