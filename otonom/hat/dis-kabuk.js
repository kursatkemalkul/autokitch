/* v69 exterior-only view. Original GLB and all original geometries stay intact.
 * Export combines parts by material: use the existing CAD part bounding boxes
 * to trim mixed meshes, not a blanket "all steel is exterior" rule.
 */
(() => {
  'use strict';
  const mv = document.getElementById('mv'), button = document.getElementById('dis-kabuk');
  const status = document.getElementById('dis-kabuk-durum');
  let data, scene, entries = [], active = false, saved, controls = [], door;
  function exterior(unit, name, front) {
    if (front) return true;
    if (unit === 'TOPPING_MODUL') return /^(dis_(taban|tavan|yan_sol|yan_sag|arka)$|onyuz_|soguk_duvar_|kabin_(sol|sag)_duvar_PU|yalitim_blogu$|alt_yalitim_|raf_kosebendi_|tasiyici_raf|raf_(on|arka)_bukumu|gecis_blogu_yalitim|.*_yarik_dili$)/.test(name);
    if (unit === 'B_KASA') return /^(onyuz_|ayak_|kasa_yan_|tavan_|taban_|arka_|yan_(ic|pu)_|bolme_|isi_kalkani_(ayirma_saci|sol_sac|sag_sac|isinim_saci))/.test(name);
    if (unit === 'A_GOVDE') return /^(a_govde_|a_kose_|a_ust_kusak_|onyuz_cerceve_)/.test(name);
    if (unit === 'A_ONYUZ') return !/sensor|isik_perdesi/.test(name);
    if (unit === 'K_GOVDE' || unit === 'E_GOVDE') return /^(ayak_|taban_sac|arka_sac|ust_sac|sol_sac|sag_sac|onyuz_|sarjor_yan_kapisi|kose_dikmesi|agiz_ust_kirisi)/.test(name);
    if (unit === 'F_TP10_GOVDE') return /^(govde_kabugu|tunel_kaplamasi|yalitim_tasyunu|ust_etiket_bandi|ekran_|ana_salter|servis_plakasi|panel_vidasi|giris_duvari_saci)/.test(name);
    if (unit === 'F_UST_KABIN') return /^(f_ust_(yan|tavan|arka|panjur)|onyuz_f_ust_(kayit|dikme))/.test(name);
    if (unit === 'F_UST_KAPAK' || unit === 'F_DAVLUMBAZ') return true;
    if (unit === 'QR_GOVDE') return !/fan|motor|kablo/.test(name);
    if (unit === 'TEZGAH_GOVDE') return !/raf/.test(name);
    if (unit === 'QR_GOZLER') return /kapak|on_panel|musteri/.test(name) && !/motor|sensor|isitici/.test(name);
    return false;
  }
  function boxes(unit) {
    return (data.parca[unit] || []).map(p => {
      const b = p.slice(2,8).map(v => v / 1000);
      return {b, keep: exterior(unit, p[0], p[1]), volume: Math.max(1e-12,(b[1]-b[0])*(b[3]-b[2])*(b[5]-b[4]))};
    });
  }
  // Triangle bounds must fit a named CAD part. Prefer the smallest containing
  // part to prevent an oven-body box from also keeping enclosed heaters/fans.
  function fits(b, t, eps = .0003) {
    return t[0]>=b[0]-eps && t[1]<=b[1]+eps && t[2]>=b[2]-eps && t[3]<=b[3]+eps && t[4]>=b[4]-eps && t[5]<=b[5]+eps;
  }
  function filtered(mesh) {
    const mats = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
    if (mats.length !== 1 || !mats[0]) return null;
    const name = mats[0].name;
    if (/^(MC_TOPPING_MODUL__yalitim_gorunur|MB_B_KASA__pu)$/.test(name)) return mesh.geometry;
    if (/__on_seffaf$/.test(name) || name === 'MS_QR_GOZLER__kapak_pc') return mesh.geometry;
    const match = /^M[A-Z]_([^]*?)__/.exec(name);
    if (!match || /__(motor|kart|siemens|hamur|harc|sos|kasar|kiyma|kusbasi|sucuk|kablo|kayis|sensor)$/.test(name)) return null;
    const unit = match[1], parts = boxes(unit).sort((a,b) => a.volume-b.volume);
    const shell=parts.filter(p=>p.keep);
    if (!shell.length) return null;
    const g = mesh.geometry, pos = g.getAttribute('position'), idx = g.getIndex();
    if (!pos || !idx) return null;
    // Non-front articulated meshes are mechanisms; boxes are in CAD world coords.
    if (/__(ARABA|ACICI|VALF|HELEZON|KARISTIRICI|PISTON|CEKMECE|RULO|KOL|PARMAK)/.test(mesh.name)) return null;
    // Keep entire connected surface components. Per-triangle bbox subtraction
    // used to punch holes in solid foam wherever a smaller part box overlapped.
    const parent = Array.from({length:idx.count/3},(_,i)=>i), vertices=new Map();
    function root(i){while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i];}return i;}
    for(let i=0;i<idx.count;i++){
      const j=idx.getX(i),key=[pos.getX(j),pos.getY(j),pos.getZ(j)].map(v=>Math.round(v*1e6)).join(',');
      const t=Math.floor(i/3),previous=vertices.get(key);
      if(previous!==undefined)parent[root(t)]=root(previous);else vertices.set(key,t);
    }
    const groups=new Map(), kept=[];
    for (let i=0;i<idx.count;i+=3) {
      const r=root(i/3);if(!groups.has(r))groups.set(r,{indices:[],b:[Infinity,-Infinity,Infinity,-Infinity,Infinity,-Infinity]});
      const c=groups.get(r);for(let k=0;k<3;k++){const j=idx.getX(i+k);c.indices.push(j);const xyz=[pos.getX(j),pos.getY(j),pos.getZ(j)];for(let a=0;a<3;a++){c.b[2*a]=Math.min(c.b[2*a],xyz[a]);c.b[2*a+1]=Math.max(c.b[2*a+1],xyz[a]);}}
    }
    for(const c of groups.values()){
      const candidates=parts.filter(p=>fits(p.b,c.b));
      // Exact component envelope beats unrelated objects enclosed by a large box.
      const best=candidates[0];
      // Joined sheet corners can connect multiple exterior parts. If there is
      // no single containing CAD box, require every face to belong to the shell.
      const joinedShell=!best && c.indices.every((_,i)=>{
        if(i%3)return true;const t=c.indices.slice(i,i+3),b=[];
        for(const get of ['getX','getY','getZ']){const v=t.map(j=>pos[get](j));b.push(Math.min(...v),Math.max(...v));}
        return shell.some(p=>fits(p.b,b));
      });
      if(best?.keep || joinedShell)for(const i of c.indices)kept.push(i);
    }
    if (!kept.length) return null;
    if (kept.length === idx.count) return g;
    const reduced=g.clone();reduced.setIndex(kept);reduced.computeBoundingBox();reduced.computeBoundingSphere();return reduced;
  }
  function build() {
    if (!data || !mv.loaded || entries.length) return;
    scene=mv[Object.getOwnPropertySymbols(mv).find(s=>s.description==='scene')];
    if (!scene) { status.textContent='Dış kabuk görünümü bu görüntüleyicide açılamadı.';return; }
    scene.traverse(mesh=>{if(mesh.isMesh && !mesh.userData.yalitimKesit && mesh.geometry && mesh.material) entries.push({mesh,original:mesh.geometry,outer:filtered(mesh),visible:mesh.visible});});
    button.disabled=false;status.textContent='Motor, kaset ve iç mekanizmaları gizler.';
  }
  function restore() {
    for(const e of entries){e.mesh.geometry=e.original;e.mesh.visible=e.visible;}
    if(door){door.value=saved.door;door.dispatchEvent(new Event('input',{bubbles:true}));}
    controls.forEach(([e,disabled])=>e.disabled=disabled);
    mv.currentTime=saved.time;if(!saved.paused)mv.play();
    active=false;button.setAttribute('aria-pressed','false');button.textContent='Sadece dış kabuk';
    status.textContent='Önceki görünüm geri yüklendi.';scene.queueRender();
  }
  button.addEventListener('click',()=>{
    if(active){restore();return;}
    door=[...document.querySelectorAll('.m3ar input[type="range"]')].find(e=>e.title.includes('metal kapak'));
    saved={time:mv.currentTime,paused:mv.paused,door:door?.value};mv.pause();mv.currentTime=0;
    controls=[...document.querySelectorAll('#sip button,#adim button,#oy,#tz,.m3 .ar'),...(door?[door]:[])].map(e=>[e,e.disabled]);
    controls.forEach(([e])=>e.disabled=true);
    if(door){door.value='100';door.dispatchEvent(new Event('input',{bubbles:true}));}
    for(const e of entries){e.visible=e.mesh.visible;e.mesh.visible=!!e.outer && e.visible;if(e.outer)e.mesh.geometry=e.outer;}
    active=true;button.setAttribute('aria-pressed','true');button.textContent='Tüm parçaları geri göster';
    status.textContent='Dış kabuk açık · iç parçalar gizli · animasyon durduruldu.';scene.queueRender();
  });
  mv.addEventListener('load',()=>{if(active)restore();for(const e of entries)if(e.outer&&e.outer!==e.original)e.outer.dispose();entries=[];build();});
  fetch('../hat3d/parca_kutulari.json?v=69').then(r=>{if(!r.ok)throw Error('Parça listesi yüklenemedi');return r.json();}).then(d=>{data=d;build();}).catch(e=>{status.textContent=e.message;});
  const timer=setInterval(()=>{build();if(entries.length)clearInterval(timer);},300);
})();
