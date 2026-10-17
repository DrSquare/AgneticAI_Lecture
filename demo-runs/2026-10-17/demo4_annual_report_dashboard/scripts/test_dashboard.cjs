// Browser acceptance test for the local, self-contained lecture artifact.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/h_min/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..'),ev=path.join(root,'evidence');
const executable='C:/Users/h_min/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe';
const block=file=>JSON.parse(fs.readFileSync(path.join(root,file),'utf8').match(/```json\s*\n([\s\S]*?)\n```/)[1]);
const checks=[],errors=[],network=[];
function pass(name,evidence){checks.push({name,status:'pass',evidence});console.log('PASS',name);}
function csvParse(s){const out=[];let row=[],field='',quoted=false;for(let i=0;i<s.length;i++){let c=s[i];if(c==='"'){if(quoted&&s[i+1]==='"'){field+='"';i++;}else quoted=!quoted;}else if(c===','&&!quoted){row.push(field);field='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&s[i+1]==='\n')i++;row.push(field);if(row.some(Boolean))out.push(row);row=[];field='';}else field+=c;}if(field||row.length){row.push(field);out.push(row);}return out;}
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:executable});
 const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true,offline:true});
 const page=await context.newPage();
 page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url());});
 try {
  await page.goto(pathToFileURL(path.join(root,'dashboard.html')).href);await page.waitForSelector('#kpi-cards [data-kpi]');
  assert.equal(errors.length,0);assert.equal(network.length,0);pass('Offline file:// operation',{networkRequests:network.length,browser:browser.version(),executable});
  const dependencies=await page.evaluate(()=>[...document.querySelectorAll('script[src],link[rel="stylesheet"],img[src]')].map(e=>e.getAttribute('src')||e.getAttribute('href')).filter(x=>!x.startsWith('data:')));
  assert.equal(dependencies.length,0);pass('Single HTML has no separate script, stylesheet or image assets',{dependencies});
  const canonical=block('financials.md');const embedded=await page.evaluate(()=>window.dashboardData.financials);
  assert.deepEqual(embedded,canonical);pass('All financials rows embedded without modification',{rows:canonical.length});
  const trendCanonical=block('trends.md');const trendEmbedded=await page.evaluate(()=>window.dashboardData.trends);
  assert.deepEqual(trendEmbedded,trendCanonical);pass('All trend calculations embedded without modification',{rows:trendCanonical.length});
  const order=()=>page.locator('#kpi-cards [data-kpi]').evaluateAll(es=>es.map(e=>e.dataset.kpi));
  const board=await order();assert.equal(board.length,8);
  await page.selectOption('#view-as','CFO');const cfo=await order();assert.notDeepEqual(cfo,board);assert.deepEqual([...cfo].sort(),[...board].sort());
  await page.selectOption('#view-as','Investor');const investor=await order();assert.notDeepEqual(investor,board);assert.notDeepEqual(investor,cfo);assert.deepEqual([...investor].sort(),[...board].sort());
  pass('Role selector reorders the same eight cards',{Board:board,CFO:cfo,Investor:investor});
  await page.selectOption('#view-as','Board');await page.screenshot({path:path.join(ev,'dashboard-board.png'),fullPage:false});
  const amountBefore=await page.locator('#annual-amounts').innerText();const ratioBefore=await page.locator('#annual-ratios').innerText();
  const card=k=>page.locator(`#kpi-cards [data-kpi="${k}"]`);
  const groupPairs={revenue:[215938,130497],'gross-margin':[71.1,75],'operating-income':[130387,81453],'net-income':[120067,72880],eps:[4.9,2.94],fcf:[96575,60724],cash:[62556,43210],inventories:[21403,10080]};
  const segmentPairs={'Compute & Networking':{revenue:[193479,116193],'operating-income':[130141,82875]},Graphics:{revenue:[22459,14304],'operating-income':[9156,5085]}};
  const checkedCards=[];
  for(const scope of ['All','Compute & Networking','Graphics']){
   await page.selectOption('#segment-filter',scope);
   for(const [key,groupPair] of Object.entries(groupPairs)){
    const pair=segmentPairs[scope]?.[key]||groupPair;
    const actual=await card(key).evaluate(e=>({current:e.dataset.currentValue,previous:e.dataset.previousValue,change:e.dataset.changeValue,groupOnly:e.dataset.groupOnly,refs:e.querySelectorAll('.refs a').length}));
    assert.equal(Number(actual.current),pair[0],`${scope} ${key} current`);assert.equal(Number(actual.previous),pair[1],`${scope} ${key} prior`);
    const change=key==='gross-margin'?pair[0]-pair[1]:(pair[0]/pair[1]-1)*100;
    assert(Math.abs(Number(actual.change)-change)<0.000001,`${scope} ${key} change: ${actual.change} vs ${change}`);
    if(scope!=='All')assert.equal(actual.groupOnly,String(!segmentPairs[scope][key]),`${scope} ${key} group-only flag`);
    assert(actual.refs>0,`${scope} ${key} source references`);checkedCards.push({scope,key,current:pair[0],previous:pair[1],change:Number(actual.change)});
   }
  }
  pass('Every KPI current/prior/change and source link reconciles in all three scopes',{cards:checkedCards.length,checks:checkedCards});
  await page.selectOption('#segment-filter','All');
  assert.equal(Number(await card('revenue').getAttribute('data-current-value')),215938);
  await page.selectOption('#segment-filter','Graphics');
  assert.equal(Number(await card('revenue').getAttribute('data-current-value')),22459);assert.equal(Number(await card('operating-income').getAttribute('data-current-value')),9156);
  assert.equal(Number(await card('gross-margin').getAttribute('data-current-value')),71.1);assert.equal(await card('gross-margin').getAttribute('data-group-only'),'true');
  assert.notEqual(await page.locator('#annual-amounts').innerText(),amountBefore);assert.notEqual(await page.locator('#annual-ratios').innerText(),ratioBefore);
  assert.match(await page.locator('#segment-table').innerText(),/Graphics/);assert.doesNotMatch(await page.locator('#segment-table tbody').innerText(),/Compute & Networking/);
  assert.match(await page.locator('#quarterly-amounts').innerText(),/group.only|consolidated/i);assert.match(await page.locator('#platform-table').innerText(),/group.only|consolidated/i);
  pass('Graphics filter updates cards, annual charts and segment table; group metrics stay labeled',{revenue:22459,operatingIncome:9156,groupGrossMargin:71.1});
  await page.selectOption('#view-as','CFO');await page.screenshot({path:path.join(ev,'dashboard-cfo-graphics.png'),fullPage:false});
  await page.selectOption('#segment-filter','Compute & Networking');assert.equal(Number(await card('revenue').getAttribute('data-current-value')),193479);assert.equal(Number(await card('operating-income').getAttribute('data-current-value')),130141);
  pass('Compute & Networking filter',{revenue:193479,operatingIncome:130141});
  await page.selectOption('#segment-filter','All');await page.selectOption('#view-as','Board');
  await page.locator('#performance').screenshot({path:path.join(ev,'dashboard-performance.png')});
  await page.locator('#outlook').screenshot({path:path.join(ev,'dashboard-outlook.png')});
  assert.match(await page.locator('#board').innerText(),/USD million/);
  const chartBounds=()=>page.locator('.quarter-chart').evaluateAll(charts=>charts.map(chart=>{const r=chart.getBoundingClientRect();return {chart:chart.parentElement.id,top:r.top,bottom:r.bottom,children:[...chart.querySelectorAll('.quarter-value,.quarter-stick,.quarter-label')].map(e=>{const c=e.getBoundingClientRect();return {kind:e.className,top:c.top,bottom:c.bottom};})};}));
  function assertChartBounds(bounds,media){for(const chart of bounds)for(const c of chart.children)assert(c.top>=chart.top-1&&c.bottom<=chart.bottom+1,`${media} ${chart.chart} ${c.kind} extends outside plot`);}
  assertChartBounds(await chartBounds(),'screen');
  const total=await page.locator('#evidence-table tbody tr').count();assert(total>=385);
  await page.fill('#evidence-search','H20');const found=await page.locator('#evidence-table tbody tr').count();assert(found>0&&found<total);assert.match(await page.locator('#evidence-table tbody').innerText(),/H20/i);
  await page.locator('#evidence-table').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(ev,'dashboard-evidence-search.png')});
  pass('Search filters evidence',{allRows:total,H20Rows:found});
  await page.fill('#evidence-search','q4_revenue_beat_pct');
  const formula=await page.locator('#evidence-table tbody tr[data-row-id="q4_revenue_beat_pct"]').innerText();
  assert.match(formula,/68,?127/);assert.match(formula,/65,?000/);assert.match(formula,/Inputs:/);assert.doesNotMatch(formula,/\[object Object\]/);
  pass('Calculated evidence exposes numerical expression and named inputs',{id:'q4_revenue_beat_pct',expression:'(68,127 / 65,000 - 1) * 100'});
  await page.fill('#evidence-search','no-matching-evidence-zzzz');assert.equal(await page.locator('#evidence-table tbody tr[data-row-id]').count(),0);await page.fill('#evidence-search','');
  const valueButton=page.locator('#evidence-table button[data-sort="value"]');await valueButton.click();
  const values=()=>page.locator('#evidence-table tbody tr[data-row-id]').evaluateAll(es=>es.map(e=>e.dataset.value).filter(v=>v!==''&&v!==undefined&&v!=='null').map(Number));
  const asc=await values();assert(asc.every((v,i)=>i===0||v>=asc[i-1]));await valueButton.click();const desc=await values();assert(desc.every((v,i)=>i===0||v<=desc[i-1]));
  pass('Evidence numeric sorting handles numbers and missing values',{numericRows:asc.length});
  await page.selectOption('#segment-filter','Graphics');await page.fill('#evidence-search','Revenue');
  const visible=await page.locator('#evidence-table tbody tr[data-row-id]').count();const downloadPromise=page.waitForEvent('download');await page.click('#export-csv');const download=await downloadPromise;
  const csvFile=path.join(ev,'export-graphics-revenue.csv');await download.saveAs(csvFile);const parsed=csvParse(fs.readFileSync(csvFile,'utf8').replace(/^\uFEFF/,''));
  assert.equal(parsed.length-1,visible);assert(parsed[0].some(x=>/formula/i.test(x)));assert(parsed[0].some(x=>/source|page/i.test(x)));assert(parsed.slice(1).every(row=>!row.includes('Compute & Networking')));
  pass('CSV export downloads the currently filtered evidence with formula/source columns',{rows:visible,file:'evidence/export-graphics-revenue.csv'});
  await page.selectOption('#segment-filter','All');await page.fill('#evidence-search','');
  await page.evaluate(()=>{window.__printCalls=0;window.print=()=>window.__printCalls++;});await page.click('#print-dashboard');assert.equal(await page.evaluate(()=>window.__printCalls),1);
  await page.emulateMedia({media:'print'});const printBounds=await chartBounds();assertChartBounds(printBounds,'print');pass('Quarterly bars, values and labels stay inside plots on screen and print',{printBounds});await page.screenshot({path:path.join(ev,'dashboard-print-media.png'),fullPage:true});
  await page.pdf({path:path.join(ev,'dashboard-print.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true});
  pass('Print button and Chromium print rendering',{file:'evidence/dashboard-print.pdf',note:'Headless print-media/PDF validation; native print dialog not exercised.'});
  await page.emulateMedia({media:'screen'});await page.setViewportSize({width:390,height:844});await page.evaluate(()=>window.scrollTo(0,0));
  await page.screenshot({path:path.join(ev,'dashboard-mobile.png'),fullPage:false});
  await page.locator('#kpi-cards').screenshot({path:path.join(ev,'dashboard-mobile-cards.png')});
  const overflow=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth}));assert(overflow.scroll<=overflow.client+1);pass('Mobile page width',{...overflow});
  assert.equal(network.length,0);assert.equal(errors.length,0);pass('No external requests or uncaught JavaScript errors',{network,errors});
 } catch(e){checks.push({name:'Browser acceptance failure',status:'fail',evidence:e.stack});console.error(e);await page.screenshot({path:path.join(ev,'dashboard-test-failure.png'),fullPage:false}).catch(()=>{});process.exitCode=1;}
 finally {fs.writeFileSync(path.join(ev,'browser-tests.json'),JSON.stringify({checked_at:new Date().toISOString(),browser:browser.version(),executable,offline:true,checks,errors,network,passed:checks.every(x=>x.status==='pass')},null,2));await browser.close();}
})();
