// Run with Node and Playwright installed. Optional browser path via
// PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH. Evidence goes to .git/ui-refresh/.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const http=require('node:http');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'..');
const out=path.resolve(process.env.LECTURE_QA_OUTPUT||path.join(root,'.git/ui-refresh'));
fs.mkdirSync(out,{recursive:true});
const checks=[],errors=[],requests=[];
const pass=(name)=>{checks.push(name);console.log('PASS',name);};
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH?{executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH}:{})});
 const context=await browser.newContext({offline:true,viewport:{width:1440,height:1000},acceptDownloads:true});
 const page=await context.newPage();
 page.setDefaultTimeout(8000);
 page.on('pageerror',e=>errors.push(e.message));
 page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url());});
 let server;
 try{
  await page.clock.install();
  await page.goto(pathToFileURL(path.join(root,'LECTURE_DEMOS.html')).href);
  await page.locator('#app').waitFor({state:'visible'});
  assert.equal(await page.locator('.demo-link').count(),4);
  assert.equal(await page.locator('[data-step]').count(),6);
  assert.equal(await page.locator('#fallback').isVisible(),false);
  assert.equal(await page.locator('[data-step="5"]').innerText().then(s=>s.includes('pptx')),false);
  pass('Direct file:// loading, four demos, six real steps and PDF publication links');
  await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});

  for(let i=1;i<=4;i++){
   await page.click('[data-demo="'+i+'"]');
   for(const tab of ['files','evidence','prompt','walkthrough']){
    await page.click('[data-tab="'+tab+'"]');
    assert.equal(await page.locator('[data-tab="'+tab+'"]').getAttribute('aria-selected'),'true');
    assert.equal(await page.locator('#panel').getAttribute('aria-labelledby'),'tab-'+tab);
   }
   assert(await page.locator('[data-step]').count()>=5);
  }
  assert.equal(errors.length,0);
  pass('All sixteen demo/view combinations render without exceptions');

  await page.click('[data-demo="1"]');
  await page.click('[data-step="2"]');
  assert.match(await page.locator('.step-board').innerText(),/five differentiators/i);
  await page.click('#mark-step');
  assert.equal(await page.locator('#mark-step').getAttribute('aria-pressed'),'true');
  await page.reload();
  await page.click('[data-step="2"]');
  assert.equal(await page.locator('#mark-step').getAttribute('aria-pressed'),'true');
  await page.click('#clear-progress');
  assert.equal(await page.locator('progress').getAttribute('value'),'0');
  pass('Step selection, completion, persistence and clear progress');

  await page.locator('#pattern [data-read]').first().click();
  await page.locator('#reader').waitFor({state:'visible'});
  assert.match(await page.locator('#reader-body').innerText(),/Figure/i);
  assert(await page.locator('#reader-body h2,#reader-body h3').count()>0);
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('#reader').isVisible(),false);
  assert.equal(await page.evaluate(()=>document.activeElement.closest('#pattern')!==null),true);
  pass('Workflow nodes open formatted notes; Escape closes and restores focus');

  await page.click('#tab-files');
  await page.fill('#file-search','not-a-file-xyz');
  assert.match(await page.locator('#file-list').innerText(),/No matching files/);
  await page.click('#clear-search');
  await page.check('#search-all');
  await page.fill('#file-search','valuation');
  assert(await page.locator('.file-row').count()>0);
  assert.match(await page.locator('#file-list').innerText(),/Valuation/i);
  await page.fill('#file-search','');
  await page.selectOption('#file-type','PDF');
  const types=await page.locator('.file-row .file-type').allTextContents();
  assert(types.length>=3&&types.every(t=>t==='PDF'));
  await page.screenshot({path:path.join(out,'file-search.png'),fullPage:false});
  await page.selectOption('#file-type','XLSX');
  const downloadPromise=page.waitForEvent('download');
  await page.locator('.file-row a').first().click();
  const download=await downloadPromise;
  assert(download.suggestedFilename().endsWith('.xlsx'));
  assert.equal(await download.failure(),null);
  pass('File search, cross-demo scope, type filters, empty state and actual workbook download');

  await page.click('[data-demo="3"]');
  await page.click('#tab-evidence');
  const valuationStatus=await page.evaluate(()=>JSON.parse(document.getElementById('lecture-data').textContent).demos.find(d=>d.demo===3).status);
  assert.equal(await page.locator('#panel .panel-lead .badge').innerText(),{ready:'Ready',partial:'Needs review',unverified:'Unverified',blocked:'Blocked',running:'In progress'}[valuationStatus]);
  await page.locator('.evidence-section').nth(1).locator('summary').click();
  assert.match(await page.locator('#panel').innerText(),/Slide 30/);
  assert.doesNotMatch(await page.locator('#panel').innerText(),/\[object Object\]/);
  await page.screenshot({path:path.join(out,'evidence.png'),fullPage:false});
  pass('Readiness warnings and structured slide corrections remain readable');

  await page.click('#tab-prompt');
  // Exercise both a successful clipboard API and its denied-permission fallback.
  await page.evaluate(()=>{Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{window.__copied=text;}}});});
  await page.click('#copy-prompt');
  assert.match(await page.evaluate(()=>window.__copied),/Alphabet/);
  await page.evaluate(()=>{Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw Error('denied');}}});document.execCommand=()=>false;});
  await page.click('#copy-prompt');
  await page.locator('.copy-area').waitFor({state:'visible'});
  assert.match(await page.locator('.copy-area').inputValue(),/Alphabet/);
  await page.keyboard.press('Escape');
  pass('Copy prompt and a selectable-text fallback when clipboard access is denied');

  await page.click('#timer-toggle');
  await page.clock.runFor(2500);
  assert.equal(await page.locator('#timer').innerText(),'04:58');
  await page.click('#timer-toggle');
  await page.clock.fastForward(5000);
  assert.equal(await page.locator('#timer').innerText(),'04:58');
  await page.click('#timer-toggle');
  await page.clock.fastForward(300000);
  assert.equal(await page.locator('#timer').innerText(),'00:00');
  assert.equal(await page.locator('#timer-toggle').innerText(),'Restart');
  await page.click('#timer-reset');
  assert.equal(await page.locator('#timer').innerText(),'05:00');
  await page.click('#timer-toggle');
  await page.click('[data-demo="2"]');
  assert.equal(await page.locator('#timer-toggle').innerText(),'Start');
  pass('Timer start, pause, resume, expiry, reset and reset on demo change');

  await page.keyboard.press('4');
  assert.match(await page.locator('#demo-title').innerText(),/NVIDIA/);
  await page.locator('#tab-walkthrough').focus();
  await page.keyboard.press('ArrowRight');
  assert.equal(await page.locator('#tab-files').getAttribute('aria-selected'),'true');
  await page.keyboard.press('End');
  assert.equal(await page.locator('#tab-prompt').getAttribute('aria-selected'),'true');
  await page.keyboard.press('p');
  assert.equal(await page.locator('.rail').isVisible(),false);
  await page.screenshot({path:path.join(out,'presentation.png'),fullPage:false});
  await page.keyboard.press('Escape');
  assert.equal(await page.locator('.rail').isVisible(),true);
  pass('Keyboard demo navigation, roving tabs and presentation mode');

  await page.click('#tab-walkthrough');
  await page.evaluate(()=>{window.__printed=0;window.print=()=>window.__printed++;});
  await page.click('#print');
  assert.equal(await page.evaluate(()=>window.__printed),1);
  await page.emulateMedia({media:'print'});
  await page.pdf({path:path.join(out,'print.pdf'),format:'A4',printBackground:true});
  await page.emulateMedia({media:'screen',reducedMotion:'reduce'});
  pass('Print action, print layout and reduced-motion rendering');

  for(const width of [320,390,768,1024,1440]){
   await page.setViewportSize({width,height:900});
   for(let demo=1;demo<=4;demo++){
    await page.locator('[data-demo="'+demo+'"]').click();
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow at '+width+' demo '+demo);
   }
   if(width===390)await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
  }
  pass('All four demos at five viewport widths, including 320px, without page overflow');

  await page.goto(pathToFileURL(path.join(root,'LECTURE_DEMOS.html')).href+'#demo-3/evidence');
  assert.match(await page.locator('#demo-title').innerText(),/Alphabet/);
  assert.equal(await page.locator('#tab-evidence').getAttribute('aria-selected'),'true');
  assert.equal(requests.length,0);
  assert.deepEqual(errors,[]);
  pass('Direct deep links, zero external requests and zero uncaught browser errors');

  const fallback=await browser.newContext({javaScriptEnabled:false,offline:true});
  const fallbackPage=await fallback.newPage();
  await fallbackPage.goto(pathToFileURL(path.join(root,'LECTURE_DEMOS.html')).href);
  assert.equal(await fallbackPage.locator('#fallback').isVisible(),true);
  assert(await fallbackPage.locator('#fallback a').count()>30);
  await fallback.close();
  const locked=await browser.newContext({offline:true});
  await locked.addInitScript(()=>{Object.defineProperty(window,'localStorage',{get(){throw Error('blocked');}});});
  const lockedPage=await locked.newPage();
  await lockedPage.goto(pathToFileURL(path.join(root,'LECTURE_DEMOS.html')).href);
  await lockedPage.click('#mark-step');
  assert.equal(await lockedPage.locator('#mark-step').getAttribute('aria-pressed'),'true');
  await locked.close();
  pass('Usable no-JavaScript fallback and graceful storage-denied behavior');

  server=http.createServer((req,res)=>{
   const file=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]));
   if(!file.startsWith(root+path.sep)){res.writeHead(403);return res.end();}
   fs.readFile(file,(error,bytes)=>{res.writeHead(error?404:200,{'Content-Type':file.endsWith('.html')?'text/html':'application/octet-stream'});res.end(error?'Not found':bytes);});
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const online=await browser.newContext();const onlinePage=await online.newPage();
  await onlinePage.goto('http://127.0.0.1:'+server.address().port+'/LECTURE_DEMOS.html#demo-2/files');
  assert.match(await onlinePage.locator('#demo-title').innerText(),/Pitch/);
  await onlinePage.locator('.file-row [data-read]').first().click();
  assert.equal(await onlinePage.locator('#reader').isVisible(),true);
  await online.close();
  pass('Normal HTTP hosting also supports deep links and embedded notes');
 }catch(error){console.error(error);await page.screenshot({path:path.join(out,'failure.png'),fullPage:true}).catch(()=>{});process.exitCode=1;}
 finally{if(server)await new Promise(resolve=>server.close(resolve));fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify({passed:!process.exitCode,checks,errors,externalRequests:requests,browser:browser.version()},null,2));await browser.close();}
})();
