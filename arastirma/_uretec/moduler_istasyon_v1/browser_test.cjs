const {chromium}=require('C:/Users/Kemal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',args:['--enable-unsafe-swiftshader']});
 const page=await browser.newPage({viewport:{width:1600,height:1050},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>{errors.push(e.message);console.log('PAGE ERROR',e.message)});
 page.on('requestfailed',r=>console.log('REQUEST FAIL',r.url(),r.failure()));
 await page.goto('http://127.0.0.1:8779/otonom/hat/moduler-v1/',{waitUntil:'domcontentloaded',timeout:60000});
 console.log('NAVIGATED');
 setTimeout(async()=>{try{console.log('STATE',await page.evaluate(()=>({loaded:document.querySelector('#mv').loaded,status:document.querySelector('#status').textContent,defined:!!customElements.get('model-viewer')})))}catch(e){}},15000);
 await page.waitForFunction(()=>document.querySelector('#mv').loaded&&document.querySelector('#status').textContent.includes('hazır'),null,{timeout:120000});
 const out=path.resolve(__dirname,'../../MODULER_ISTASYON_v1');
 await page.screenshot({path:path.join(out,'kurulu.png'),fullPage:true});
 await page.locator('#transport').click();
 await page.waitForTimeout(800);
 await page.screenshot({path:path.join(out,'ayri-moduller.png'),fullPage:true});
 const transport=await page.locator('#transport').getAttribute('aria-pressed');
 await page.locator('#module').selectOption('B');await page.locator('#assembled').click();await page.locator('#inside').click();await page.locator('#added').click();
 await page.waitForTimeout(800);await page.screenshot({path:path.join(out,'B-ic-duzen.png'),fullPage:true});
 const scene=await page.evaluate(()=>{const mv=document.querySelector('#mv'),sc=mv[Object.getOwnPropertySymbols(mv).find(s=>s.description==='scene')];let visible=0,hidden=0;sc.traverse(o=>{if(o.isMesh)o.visible?visible++:hidden++});return {visible,hidden,status:document.querySelector('#status').textContent}});
 for(const id of ['step','bom']){const url=await page.locator('#'+id).getAttribute('href');const r=await page.request.get(new URL(url,page.url()).href);if(!r.ok())errors.push(id+' '+r.status());}
 const result={errors,transport,scene};
 require('fs').writeFileSync(path.join(out,'browser_results.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify(result,null,2));
 await browser.close();if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
