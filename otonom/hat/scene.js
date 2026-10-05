
// AUTOKITCH hat/scene.js — basit kutu modeli, hover = grup vurgusu, tık = sayfa. Ölçüler cm. x: soldan sağa, y: önden (sokak) arkaya, z: yukarı.
function buildScene(el, items, opts){
  opts=opts||{}; const W=el.clientWidth, H=el.clientHeight;
  const scene=new THREE.Scene(); scene.background=new THREE.Color(0xf7f8fa);
  const cam=new THREE.PerspectiveCamera(38, W/H, 1, 6000); const c=opts.center||[210,132,90];
  const D=(opts.depth||264); cam.position.set(c[0]+(opts.camOff?opts.camOff[0]:0), c[2]+(opts.camOff?opts.camOff[2]:420), D/2+(opts.camOff?opts.camOff[1]:620));
  const ren=new THREE.WebGLRenderer({antialias:true}); ren.setPixelRatio(Math.min(devicePixelRatio,2)); ren.setSize(W,H); el.appendChild(ren.domElement);
  const ctr=new THREE.OrbitControls(cam, ren.domElement); ctr.target.set(c[0],c[2],D/2); ctr.enableDamping=true; ctr.maxPolarAngle=Math.PI/2.05; ctr.update();
  scene.add(new THREE.HemisphereLight(0xffffff,0xd9dde3,1.05)); const dl=new THREE.DirectionalLight(0xffffff,.55); dl.position.set(300,600,400); scene.add(dl);
  const grid=new THREE.GridHelper(1400,28,0xdde3ea,0xe9edf2); grid.position.y=-0.5; scene.add(grid);
  const meshes=[]; const byItem={};
  function toWorld(x,y,z){ return [x, z, (opts.depth||264)-y]; }   // y (derinlik) → -Z: sokak (y=0) kameraya yakın (Z=depth)
  items.forEach(it=>{
    byItem[it.id]={item:it,meshes:[]};
    (it.boxes||[]).forEach(b=>{
      const [x,y,z,w,d,h]=b; const geo=new THREE.BoxGeometry(w,h,d);
      const mat=new THREE.MeshStandardMaterial({color:new THREE.Color(it.color||'#cfd3d8'),roughness:.6,metalness:.05,transparent:!!it.opacity,opacity:it.opacity||1});
      const m=new THREE.Mesh(geo,mat); const p=toWorld(x+w/2,y+d/2,z+h/2); m.position.set(p[0],p[1],p[2]); m.userData.item=it; scene.add(m);
      const eg=new THREE.LineSegments(new THREE.EdgesGeometry(geo),new THREE.LineBasicMaterial({color:0x1d2430,transparent:true,opacity:it.opacity?0.25:0.55})); m.add(eg);
      if(it.href){meshes.push(m)} byItem[it.id].meshes.push(m);
    });
  });
  // GERÇEK MODEL (opts.glb): makinenin üretim GLB'si (m, x · y yukarı · z sokağa doğru) sahneye ölçekli oturur; parçanın adı
  // parca_kutulari.json'dan (hat_montaj_v62) bulunur; şeffaf ön kapaklar ışında atlanır. Kutu öğeleriyle aynı etiket / tık düzeni.
  let glbRoot=null, PK=null, M2K={}, PB={}, glbSecili=false;
  if(opts.glb&&THREE.GLTFLoader){
    const yukle=g=>{
      glbRoot=g.scene; glbRoot.scale.setScalar(opts.glb.scale); glbRoot.position.set(opts.glb.pos[0],opts.glb.pos[1],opts.glb.pos[2]);
      glbRoot.traverse(o=>{ if((opts.glb.gizle||[]).some(n=>o.name.indexOf(n)===0)) o.visible=false;
        // bu sahnede ortam haritası yok → metal (paslanmaz, sac) PBR'da siyah görünür: metalikliği kıs, rengi koru
        if(o.material) [].concat(o.material).forEach(m=>{ if(m.metalness!==undefined){ m.metalness=Math.min(m.metalness,0.15); m.roughness=Math.max(m.roughness,0.55); } }); });
      scene.add(glbRoot); if(opts.glb.yuklendi) opts.glb.yuklendi();
    };
    const hata=()=>{ if(opts.glb.hata) opts.glb.hata(); };
    const L=new THREE.GLTFLoader(); if(self.MeshoptDecoder&&L.setMeshoptDecoder) L.setMeshoptDecoder(self.MeshoptDecoder);
    if(/\.gz(\?|$)/.test(opts.glb.url)){   // gzip taşıma (makine sayfasıyla aynı dosya): indir → aç → ayrıştır
      fetch(opts.glb.url).then(r=>{ if(!r.ok) throw Error(r.status); return new Response(r.body.pipeThrough(new DecompressionStream('gzip'))).arrayBuffer(); })
        .then(buf=>L.parse(buf,'',yukle,hata)).catch(hata);
    } else L.load(opts.glb.url, yukle, undefined, hata);
    if(opts.glb.parca) fetch(opts.glb.parca).then(r=>r.json()).then(D=>{PK=D.parca; PB=D.birim; Object.keys(PB).forEach(k=>{M2K[PB[k].mal]=k;});}).catch(()=>{});
  }
  const gorunur=o=>{ for(;o;o=o.parent){ if(!o.visible) return false; } return true; };
  function glbParca(h){
    if(!PK) return null;
    const p=glbRoot.worldToLocal(h.point.clone()).multiplyScalar(1000), P=[p.x,p.y,p.z];
    const mn=(h.object.material&&h.object.material.name)||''; if(mn.indexOf('insan')===0) return null;
    const kod=M2K[mn.split('__')[0]], hac=k=>(k[3]-k[2])*(k[5]-k[4])*(k[7]-k[6]);
    const ic=k=>P[0]>=k[2]-3&&P[0]<=k[3]+3&&P[1]>=k[4]-3&&P[1]<=k[5]+3&&P[2]>=k[6]-3&&P[2]<=k[7]+3;
    let en=null; const bak=(kd)=>(PK[kd]||[]).forEach(k=>{ if(ic(k)&&(!en||hac(k)<hac(en[1]))) en=[kd,k]; });
    if(kod) bak(kod); if(!en) Object.keys(PK).forEach(bak);
    return en?{ad:en[1][0].replace(/_/g,' '),birim:(PB[en[0]]||{}).ad||''}:null;
  }
  const tip=document.createElement('div'); tip.className='tip'; el.appendChild(tip);
  const ray=new THREE.Raycaster(); const mouse=new THREE.Vector2(); let hover=null;
  function setHover(it){
    if(hover===it) return;
    if(hover){ byItem[hover.id].meshes.forEach(m=>{m.material.color.set(hover.color||'#cfd3d8'); m.material.emissive.set(0x000000)}); }
    hover=it;
    if(hover){ byItem[hover.id].meshes.forEach(m=>{m.material.color.set(hover.hover||hover.color); m.material.emissive.set(hover.hover||hover.color); m.material.emissiveIntensity=.35}); el.style.cursor=hover.href?'pointer':'default'; }
    else el.style.cursor='default';
  }
  el.addEventListener('pointermove',e=>{
    const r=el.getBoundingClientRect(); mouse.x=((e.clientX-r.left)/r.width)*2-1; mouse.y=-((e.clientY-r.top)/r.height)*2+1;
    ray.setFromCamera(mouse,cam); const hit=ray.intersectObjects(meshes,false)[0];
    const gh=glbRoot?ray.intersectObject(glbRoot,true).find(h=>gorunur(h.object)&&!((h.object.material&&h.object.material.name)||'').endsWith('__on_seffaf')):null;
    glbSecili=false;
    if(gh&&(!hit||gh.distance<hit.distance)){
      setHover(null); glbSecili=!!opts.glb.href; el.style.cursor=glbSecili?'pointer':'default';
      const pr=glbParca(gh); tip.style.display='block'; tip.style.left=(e.clientX-r.left)+'px'; tip.style.top=(e.clientY-r.top)+'px';
      tip.textContent=(pr?pr.ad+'  ·  '+pr.birim.slice(0,70):opts.glb.name)+(glbSecili?'  →':'');
    }
    else if(hit){ setHover(hit.object.userData.item); tip.style.display='block'; tip.style.left=(e.clientX-r.left)+'px'; tip.style.top=(e.clientY-r.top)+'px'; tip.textContent=hover.name+(hover.href?'  →':''); }
    else { setHover(null); tip.style.display='none'; }
  });
  el.addEventListener('pointerleave',()=>{setHover(null); tip.style.display='none'});
  let down=null; el.addEventListener('pointerdown',e=>{down=[e.clientX,e.clientY]});
  el.addEventListener('pointerup',e=>{ if(down&&Math.hypot(e.clientX-down[0],e.clientY-down[1])<6){ if(hover&&hover.href) location.href=hover.href; else if(glbSecili) location.href=opts.glb.href; } down=null; });
  window.addEventListener('resize',()=>{const W=el.clientWidth,H=el.clientHeight; cam.aspect=W/H; cam.updateProjectionMatrix(); ren.setSize(W,H)});
  (function loop(){ requestAnimationFrame(loop); ctr.update(); ren.render(scene,cam); })();
}
