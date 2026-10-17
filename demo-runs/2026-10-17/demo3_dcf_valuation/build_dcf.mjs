import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';

const root=path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1'));
const peerData=JSON.parse(await fs.readFile(path.join(root,'peer-inputs.json'),'utf8'));
const wb=Workbook.create();
const names=['README','Assumptions','Summary','Historicals','Projections','DCF','Sensitivity','Multiples'];
const sheets=Object.fromEntries(names.map(n=>[n,wb.worksheets.add(n)]));
const blue='#0000FF',green='#008000',black='#17212B',navy='#19334D',yellow='#FFF2CC';
const num='#,##0;(#,##0);"–"', pct='0.0%;(0.0%);"–"', price='$0.00;($0.00);"–"';
const sources={
S1:['Alphabet FY2025 10-K, income / cash flow / Note 2','https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm'],
S2:['Alphabet H1 2026 10-Q, June 30, 2026, Notes 2, 6, 11','https://www.sec.gov/Archives/edgar/data/1652044/000165204426000071/goog-20260630.htm'],
S3:['Alphabet Q2 2026 call, July 22, 2026, CFO outlook','https://alphabet2025ir.q4web.com/investor/events/event-details/2026/2026-Q2-Earnings-Call-2026-GgTAq7Is0z/default.aspx'],
S4:['Microsoft FY2026 release, year ended June 30','https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast'],
S5:['Meta Q2 2026 release, June 30, 2026','https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/'],
S6:['Meta FY2025 release, December 31, 2025','https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx'],
S7:['Amazon Q2 2026 release, June 30, 2026','https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Second-Quarter-Results/default.aspx'],
S8:['Amazon FY2025 release, December 31, 2025','https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx'],
S9:['Amazon Q2 2026 10-Q, debt Note 5','https://www.sec.gov/Archives/edgar/data/1018724/000101872426000026/amzn-20260630.htm'],
S10:['Meta Q2 2026 10-Q, June 30 balance sheet, Class A and B shares outstanding','https://www.sec.gov/Archives/edgar/data/1326801/000162828026050705/meta-20260630.htm'],
Q1:['GOOGL closing quote, October 16, 2026, Google Finance vendor display','https://www.google.com/finance/quote/GOOGL:NASDAQ'],
Q2:['MSFT closing quote, October 16, 2026, Google Finance vendor display','https://www.google.com/finance/quote/MSFT:NASDAQ'],
Q3:['META closing quote, October 16, 2026, Google Finance vendor display','https://www.google.com/finance/quote/META:NASDAQ'],
Q4:['AMZN closing quote, October 16, 2026, Google Finance vendor display','https://www.google.com/finance/quote/AMZN:NASDAQ'],
A1:['Author teaching assumptions, October 17, 2026; not company guidance','valuation-notes.md']};
const peerTickers=['GOOGL','MSFT','META','AMZN'];
peerTickers.forEach((ticker,i)=>{sources[`F${i+1}`]=[`${ticker} adjusted consensus EPS, updated October 16, 2026`,peerData.forward[ticker].url];});
peerTickers.forEach((ticker,i)=>{sources[`X${i+1}`]=[`${ticker} SEC XBRL facts; filing dates restricted to October 17, 2026 or earlier`,peerData.source_facts.find(x=>x.ticker===ticker).api_url];});
const inputs=[];
function v(s,cell,val,src){const r=sheets[s].getRange(cell);r.values=[[val]];if(typeof val==='number'||val instanceof Date){r.format.font.color=blue;inputs.push({sheet:s,cell,value:val,source:src||'User requested forecast period / model convention'});} }
function f(s,cell,formula){const r=sheets[s].getRange(cell);r.formulas=[[formula]];r.format.font.color=formula.includes('!')?green:black;}
function t(s,cell,text){v(s,cell,text);}
function row(s,r,label,vals,note=''){t(s,`C${r}`,label);vals.forEach((x,i)=>{if(x!==null)v(s,`${String.fromCharCode(68+i)}${r}`,x,note)});if(note)t(s,`J${r}`,note);}
function band(s,r,label){t(s,`C${r}`,label);sheets[s].getRange(`C${r}:H${r}`).format={fill:'#E7EDF3',font:{bold:true,color:navy}};}
function total(s,r){sheets[s].getRange(`C${r}:H${r}`).format.font.bold=true;sheets[s].getRange(`C${r}:H${r}`).format.borders={top:{style:'thin',color:'#B8C5D1'}};}
function note(s,r,text,end='J'){t(s,`C${r}`,text);sheets[s].getRange(`C${r}:${end}${r}`).merge();sheets[s].getRange(`C${r}:${end}${r}`).format.wrapText=true;sheets[s].getRange(`C${r}:${end}${r}`).format.rowHeight=30;}
for(const n of names){const s=sheets[n];s.showGridLines=false;s.getRange('A1:L190').format.font={name:'Arial',size:10,color:black};s.getRange('A1:B190').format.columnWidth=2.4;s.getRange('C1:C190').format.columnWidth=39;s.getRange('D1:H190').format.columnWidth=16;s.getRange('I1:I190').format.columnWidth=3;s.getRange('J1:J190').format.columnWidth=92;s.getRange('C1:J190').format.rowHeight=19;s.getRange('D1:H190').setNumberFormat(num);t(n,'C2',n==='README'?'Alphabet valuation teaching model':n);s.getRange('C2:H2').format.font={size:15,bold:true,color:navy};s.getRange('C2:H2').format.rowHeight=26;t(n,'C4','Case selected');if(n!=='Assumptions')f(n,'D4',"=CHOOSE('Assumptions'!$D$4,\"Base\",\"Bull\",\"Bear\")");s.getRange('D4').setNumberFormat('@');s.tabColor=['Summary','DCF'].includes(n)?navy:n==='Assumptions'?'#527493':n==='Historicals'?'#D6C8AC':'#AEBBC8';}

// README: source registry and precise scope.
const intro=[
'USD millions, except per-share values. Financials through June 30, 2026; valuation October 17, 2026.',
'Prices are October 16 closes from Google Finance. Exchange-direct verification was unavailable.',
'Blue = sourced numeric input. Yellow = editable key driver. Black = formula. Green = cross-sheet formula.',
'One forecast build responds to the Base / Bull / Bear selector in Assumptions!D4.',
'Low / active / high DCF values are discount-rate and growth bounds for the selected operating case.',
'SBC stays in EBIT and is never added back. D&A and capex are modeled separately.',
'The stub uses the remaining share of projected H2 cash flow; annual flows use mid-year discounting.',
'Terminal capex is normalized to D&A × the editable ratio. This dominates value and is not guidance.',
'Search, YouTube, Network and subscriptions EBIT margins are allocations, not disclosed segment profits.',
'Cash bridge uses June 30 balances with no July–October roll-forward. Equity stakes are treated explicitly.',
'Preferred stock is deducted at liquidation preference; conversion and capped calls are not option-priced.',
'Non-marketable investments are excluded in Base. Deferred tax and accrued legal claims are deducted.',
'Peer EV/EBITD = EV / (EBIT + PPE depreciation). This verified-input comparison replaces EBITDA; all intangible amortization stays expensed.',
'Forward P/E uses CY2027 adjusted consensus EPS dated Oct 16. Microsoft is calendarized from FY2027 / FY2028.',
'Teaching model, not investment advice. Market and scenario assumptions are dated and uncertain.'
];intro.forEach((x,i)=>note('README',6+i*2,x));
band('README',38,'Sources (IDs also appear beside the inputs)');
let sr=40;for(const [id,[label,url]] of Object.entries(sources)){t('README',`C${sr}`,id+' — '+label);sheets.README.getRange(`C${sr}:H${sr}`).merge();t('README',`C${sr+1}`,url);sheets.README.getRange(`C${sr+1}:J${sr+1}`).merge();sr+=3;}

// All historical inputs are reported values, except separate reconciliation rows.
row('Historicals',6,'Reported results',['FY2023','FY2024','FY2025','H1 2025','H1 2026'],'S1 annual; S2 interim. USD millions. Interim figures unaudited.');
sheets.Historicals.getRange('C6:H6').format={fill:navy,font:{color:'#FFFFFF',bold:true}};
const hist={
8:['Search & other',[175033,198084,224532,104892,123670]],9:['YouTube ads',[31510,36147,40367,18723,20938]],10:['Network',[31312,30359,29792,14610,14274]],11:['Subscriptions, platforms & devices',[34688,40340,48030,21582,25295]],12:['Google Cloud',[33088,43229,58705,25884,44796]],13:['Other Bets',[1527,1648,1537,823,793]],14:['Hedging gains / (losses)',[236,211,-127,148,-74]],15:['Reported revenue',[307394,350018,402836,186662,229692]],
18:['Cost of revenue',[133332,146306,162535,75400,87214]],19:['Research & development',[45427,49326,61087,27364,35251]],20:['Sales & marketing',[27917,27808,28693,13273,16009]],21:['General & administrative',[16425,14188,21482,8748,10752]],22:['Reported operating income',[84293,112390,129039,61877,80466]],25:['Income before tax',[85717,119815,158826,75722,216165]],26:['Income tax provision',[11922,19697,26656,12986,41394]],27:['Net income',[73795,100118,132170,62736,174771]],28:['Net income available to common',[73795,100118,132170,62736,174685]],29:['Diluted EPS',[5.80,8.04,10.81,5.12,14.24]],30:['PPE depreciation',[11946,15311,21136,9485,13586]],31:['Stock-based compensation',[22460,22785,24953,11514,14708]],32:['Cash from operations',[101746,125299,164713,63897,84859]],33:['Purchases of PPE (positive outflow)',[32251,52535,91447,39643,80598]],
36:['Accounts receivable',[null,null,62886,null,69175]],37:['Inventory',[null,null,2439,null,9991]],38:['Accounts payable',[null,null,12200,null,20258]],39:['Deferred revenue, current',[null,null,6578,null,7154]],42:['Cash, equivalents & marketable securities',[null,null,126843,null,242474]],43:['Long-term debt, carrying value',[null,null,46547,null,98165]],44:['Current portion of notes',[null,null,1996,null,1999]],45:['Fair value of notes',[null,null,45600,null,94900]],46:['Other long-term debt, face value',[null,null,0,null,1686]],47:['Common shares outstanding (all classes)',[null,null,12088,null,12230]],48:['Preferred depositary shares, millions',[null,null,0,null,385]],49:['Preference per depositary share, USD',[null,null,null,null,50]],50:['Non-marketable securities',[null,null,68687,null,131461]],51:['Deferred income tax liability',[null,null,919,null,22819]],52:['Accrued legal/regulatory claims',[null,null,null,null,17400]],53:['H1 intangible amortization',[null,null,null,246,545]],54:['Google Cloud backlog',[null,null,null,null,513900]]};
for(const [r,[label,vals]] of Object.entries(hist))row('Historicals',+r,label,vals,Number(r)>=36?'S2 balance sheet / notes; point in time. Blank = not collected.':'S1 annual; S2 H1. Reported, USD millions except EPS.');
for(const c of ['D','E','F','G','H']){f('Historicals',`${c}16`,`=SUM(${c}8:${c}14)-${c}15`);f('Historicals',`${c}23`,`=${c}15-SUM(${c}18:${c}21)`);f('Historicals',`${c}24`,`=${c}23-${c}22`);f('Historicals',`${c}34`,`=${c}32-${c}33`);}
t('Historicals','C16','Revenue reconciliation difference');t('Historicals','C23','Computed operating income');t('Historicals','C24','Operating income difference');t('Historicals','C34','Computed operating cash flow less capex');t('Historicals','C40','Computed trade NWC (AR + inventory − AP − deferred revenue)');
for(const c of ['F','H'])f('Historicals',`${c}40`,`=SUM(${c}36:${c}37)-SUM(${c}38:${c}39)`);
sheets.Historicals.getRange('D29:H29').setNumberFormat('0.00');for(const r of [16,24]){sheets.Historicals.getRange(`D${r}:H${r}`).setNumberFormat('0.00');sheets.Historicals.getRange(`D${r}:H${r}`).conditionalFormats.add('cellIs',{operator:'notEqual',formula:0,format:{fill:'#FCE4D6',font:{color:'#C00000'}}});}
for(const r of [15,22,23,27,34,40])total('Historicals',r);sheets.Historicals.freezePanes.freezeRows(6);

// Assumptions: single numeric selector and active row above each case group.
v('Assumptions','D4',1,'A1: 1 Base, 2 Bull, 3 Bear');sheets.Assumptions.getRange('D4').setNumberFormat('0');sheets.Assumptions.getRange('D4').dataValidation={rule:{type:'list',values:['1','2','3']}};f('Assumptions','F4','=CHOOSE(D4,"Base","Bull","Bear")');t('Assumptions','J4','1 Base / 2 Bull / 3 Bear. Change only this selector.');
const globals=[
[6,'Valuation date',new Date('2026-10-17T00:00:00Z'),'User requested date, America/Los_Angeles'],
[7,'GOOGL closing price',340.59,'Q1: October 16, 2026 close. Vendor quote, not exchange-direct.'],
[8,'Quote date',new Date('2026-10-16T00:00:00Z'),'Q1: last trading close before valuation date'],
[9,'Risk-free rate assumption',.045,'A1: rounded teaching assumption, not a verified current Treasury yield.'],
[10,'Beta assumption',1.2,'A1: teaching beta, not a regression estimate.'],
[11,'Equity risk premium assumption',.045,'A1: teaching ERP, not a market fact.'],
[12,'Pre-tax cost of debt proxy',.048,'S2 Note 6: Q1 USD issue weighted coupon 4.80%; current yield may differ.'],
[13,'Normalized tax rate',.20,'A1: operating tax assumption; H1 GAAP tax includes investment gains.'],
[14,'Terminal growth',.03,'A1: perpetual nominal growth, independent of forecast growth.'],
[15,'Terminal capex / D&A',1.15,'A1: capex exceeds D&A by 15% in steady state; normalized after AI buildout.'],
[16,'Non-marketable stake realization',0,'A1: exclude unlisted investments; no double count of marketable securities.'],
[17,'2026 capex guide low',195000,'S3: July 22, 2026 CFO guidance, USD millions.'],
[18,'2026 capex guide high',205000,'S3: July 22, 2026 CFO guidance, USD millions.'],
[20,'Preferred cost proxy',.0625,'S2 Note 11: coupon rate, used as market yield proxy.'],
[21,'WACC sensitivity step',.005,'A1: 0.5 percentage point grid interval.'],
[22,'Growth sensitivity step',.005,'A1: 0.5 percentage point grid interval.'],
[23,'Forecast hedging gain assumption',0,'A1: no forecast gains/losses; known H1 actual remains in 2026.']];
for(const [r,l,x,n] of globals){t('Assumptions',`C${r}`,l);v('Assumptions',`D${r}`,x,n);t('Assumptions',`J${r}`,n);sheets.Assumptions.getRange(`D${r}`).format.fill=yellow;}
t('Assumptions','C19','2026 capex guidance midpoint');f('Assumptions','D19','=AVERAGE(D17:D18)');
for(const r of [6,8])sheets.Assumptions.getRange(`D${r}`).setNumberFormat('yyyy-mm-dd');sheets.Assumptions.getRange('D7').setNumberFormat(price);for(const r of [9,11,12,13,14,16,20,21,22])sheets.Assumptions.getRange(`D${r}`).setNumberFormat(pct);sheets.Assumptions.getRange('D10').setNumberFormat('0.00x');sheets.Assumptions.getRange('D15').setNumberFormat('0.00x');
row('Assumptions',26,'Forecast drivers',['2026E','2027E','2028E','2029E','2030E'],'2026 revenue driver applies to H2 2025 comparable; later years apply to full year.');
sheets.Assumptions.getRange('C26:H26').format={fill:navy,font:{color:'#FFFFFF',bold:true}};
const groups=[
[28,'Search growth',[[.16,.12,.10,.08,.07],[.19,.15,.13,.11,.09],[.10,.08,.06,.05,.04]],'A1 / S2: H1 Search grew 17.9%; gradual moderation.'],
[33,'YouTube growth',[[.13,.12,.11,.10,.09],[.16,.15,.14,.12,.10],[.08,.07,.06,.05,.05]],'A1 / S2: H1 YouTube grew 11.8%; World Cup timing.'],
[38,'Network growth',[[-.02,-.02,-.01,0,0],[0,.01,.01,.01,.01],[-.05,-.05,-.04,-.03,-.02]],'A1 / S2: H1 Network contracted 2.3%.'],
[43,'Subscriptions & devices growth',[[.16,.15,.13,.12,.10],[.20,.18,.16,.14,.12],[.10,.09,.08,.07,.06]],'A1 / S2: H1 subscriptions/platforms/devices grew 17.2%.'],
[48,'Cloud growth',[[.70,.50,.35,.28,.22],[.85,.60,.45,.35,.28],[.45,.30,.25,.20,.15]],'A1 / S2 / S3: H1 Cloud +73.1%; $513.9bn backlog, timing uncertain.'],
[53,'Other Bets growth',[[.10,.15,.15,.15,.15],[.20,.30,.30,.25,.20],[0,.05,.05,.05,.05]],'A1: speculative growth; does not separately value Waymo.'],
[58,'Services EBIT margin',[[.41,.41,.42,.42,.42],[.43,.44,.45,.45,.45],[.38,.37,.37,.37,.37]],'A1 / S3: Q2 Services margin 41.8%; shared across four revenue categories.'],
[63,'Cloud EBIT margin',[[.34,.33,.34,.35,.36],[.36,.37,.38,.39,.40],[.28,.27,.28,.29,.30]],'A1 / S3: Q2 Cloud margin 35.6%; third-party capacity pressure.'],
[68,'Other Bets EBIT margin',[[-4.5,-4,-3,-2,-1],[-4,-3,-2,-1,0],[-5,-5,-4,-3,-2]],'A1 / S1: substantial losses persist; revenue is small.'],
[73,'Corporate cost / revenue',[[.05,.05,.045,.04,.04],[.045,.04,.035,.03,.03],[.06,.06,.06,.055,.05]],'A1 / S3: Q2 Alphabet-level loss $5.8bn, primarily shared AI R&D.'],
[78,'D&A / revenue',[[.07,.10,.12,.13,.13],[.065,.09,.11,.12,.12],[.08,.11,.13,.14,.14]],'A1 / S2: H1 PPE depreciation $13.6bn; forward burden increases.'],
[83,'Capex / revenue',[[null,.46,.36,.26,.19],[null,.40,.30,.22,.16],[null,.50,.42,.34,.26]],'A1 / S3: 2026 exact $200bn midpoint; 2027+ intensity assumptions.'],
[88,'Trade NWC / revenue',[[.10,.10,.10,.10,.10],[.09,.09,.09,.09,.09],[.12,.12,.12,.12,.12]],'A1 / S2: narrow trade NWC definition; excludes tax and legal balances.']];
for(const [r,label,cases,n] of groups){t('Assumptions',`C${r}`,label+' — active');t('Assumptions',`J${r}`,n);for(let j=0;j<5;j++){const c=String.fromCharCode(68+j);if(r===83&&j===0){t('Assumptions',`${c}${r}`,'Guide $200bn');continue;}f('Assumptions',`${c}${r}`,`=IF(ISNUMBER(CHOOSE($D$4,${c}${r+1},${c}${r+2},${c}${r+3})),CHOOSE($D$4,${c}${r+1},${c}${r+2},${c}${r+3}),"Missing input")`);}
for(let k=0;k<3;k++)row('Assumptions',r+1+k,['Base','Bull','Bear'][k],cases[k],n);sheets.Assumptions.getRange(`D${r}:H${r+3}`).setNumberFormat(pct);sheets.Assumptions.getRange(`D${r+1}:H${r+3}`).format.fill=yellow;total('Assumptions',r);}
sheets.Assumptions.freezePanes.freezeRows(26);

// Forecast revenue and EBIT by category, pooled capex / D&A allocated pro rata.
row('Projections',6,'USD millions',['2026E','2027E','2028E','2029E','2030E']);
const segs=['Search & other','YouTube ads','Network','Subscriptions & devices','Google Cloud','Other Bets'];
for(let j=0;j<5;j++){const c=String.fromCharCode(68+j),p=String.fromCharCode(67+j);for(let i=0;i<6;i++){const r=8+i,gr=28+i*5;f('Projections',`${c}${r}`,j===0?`='Historicals'!H${r}+('Historicals'!F${r}-'Historicals'!G${r})*(1+'Assumptions'!${c}${gr})`:`=${p}${r}*(1+'Assumptions'!${c}${gr})`);f('Projections',`${c}${19+i}`,`=${c}${r}*'Assumptions'!${c}${i<4?58:i===4?63:68}`);}
f('Projections',`${c}14`,j===0?"='Historicals'!H14+'Assumptions'!$D$23":"='Assumptions'!$D$23");f('Projections',`${c}15`,`=SUM(${c}8:${c}14)`);f('Projections',`${c}25`,`=-${c}15*'Assumptions'!${c}73`);f('Projections',`${c}26`,`=SUM(${c}19:${c}25)`);f('Projections',`${c}27`,`=${c}26/${c}15`);f('Projections',`${c}29`,`=${c}26*'Assumptions'!$D$13`);f('Projections',`${c}30`,`=${c}26-${c}29`);f('Projections',`${c}32`,`=${c}15*'Assumptions'!${c}78`);f('Projections',`${c}33`,j===0?"='Assumptions'!$D$19":`=${c}15*'Assumptions'!${c}83`);f('Projections',`${c}34`,`=${c}33/${c}15`);f('Projections',`${c}36`,`=${c}15*'Assumptions'!${c}88`);f('Projections',`${c}37`,j===0?"='Historicals'!F40":`=${p}36`);f('Projections',`${c}38`,`=${c}36-${c}37`);f('Projections',`${c}40`,`=${c}30+${c}32-${c}33-${c}38`);f('Projections',`${c}41`,`=${c}26+${c}32`);
for(let i=0;i<6;i++){const r=46+i*7;f('Projections',`${c}${r+1}`,`=${c}${8+i}/SUM(${c}$8:${c}$13)`);f('Projections',`${c}${r+2}`,`=${c}$32*${c}${r+1}`);f('Projections',`${c}${r+3}`,`=${c}$33*${c}${r+1}`);f('Projections',`${c}${r+4}`,`=${c}$38*${c}${r+1}`);f('Projections',`${c}${r+5}`,`=${c}${19+i}*(1-'Assumptions'!$D$13)+${c}${r+2}-${c}${r+3}-${c}${r+4}`);}
f('Projections',`${c}90`,`=SUM(${[51,58,65,72,79,86].map(r=>c+r).join(',')})+${c}25*(1-'Assumptions'!$D$13)-${c}40`);}
for(let i=0;i<6;i++){t('Projections',`C${8+i}`,segs[i]);t('Projections',`C${19+i}`,segs[i]+' EBIT');const r=46+i*7;band('Projections',r,segs[i]+' cash-flow allocation');['Revenue allocation weight','Allocated D&A','Allocated capex','Allocated trade ΔNWC','Allocated unlevered cash flow'].forEach((l,k)=>t('Projections',`C${r+k+1}`,l));sheets.Projections.getRange(`D${r+1}:H${r+1}`).setNumberFormat(pct);}
const plabels={14:'Hedging gains / (losses)',15:'Total revenue',25:'Alphabet-level costs',26:'Operating income',27:'Operating margin',29:'Normalized operating tax',30:'NOPAT',32:'D&A',33:'Cash capex',34:'Capex / revenue',36:'Ending trade NWC',37:'Beginning trade NWC',38:'Change in trade NWC',40:'Unlevered free cash flow',41:'EBITDA (forecast)',90:'Allocation reconciliation difference'};
for(const [r,l] of Object.entries(plabels))t('Projections',`C${r}`,l);for(const r of [15,26,30,40,41,90])total('Projections',r);for(const r of [27,34])sheets.Projections.getRange(`D${r}:H${r}`).setNumberFormat(pct);
note('Projections',43,'D&A and capex allocations are teaching assumptions. The capex test holds revenue and D&A drivers fixed.');
band('Projections',93,'2026 stub construction');
const stub=[ [94,'H1 normalized NOPAT',"='Historicals'!H22*(1-'Assumptions'!$D$13)"],[95,'H1 D&A',"=SUM('Historicals'!H30,'Historicals'!H53)"],[96,'H1 cash capex',"='Historicals'!H33"],[97,'H1 trade NWC change',"='Historicals'!H40-'Historicals'!F40"],[98,'H1 normalized unlevered FCF','=D94+D95-D96-D97'],[99,'Projected H2 unlevered FCF','=D40-D98'] ];for(const[r,l,x]of stub){t('Projections',`C${r}`,l);f('Projections',`D${r}`,x);}note('Projections',101,'H1 normalized unlevered FCF is derived with the assumed operating tax rate. It is not reported free cash flow.');sheets.Projections.freezePanes.freezeRows(6);

// DCF: market-value weights with explicitly dated proxies and year-end terminal value.
const dcfrows={6:['Common equity market value',"='Assumptions'!D7*'Historicals'!H47"],7:['Debt market value proxy',"=SUM('Historicals'!H45:H46)"],8:['Preferred market value proxy',"='Historicals'!H48*'Historicals'!H49"],9:['CAPM cost of common equity',"='Assumptions'!D9+'Assumptions'!D10*'Assumptions'!D11"],10:['After-tax debt cost',"='Assumptions'!D12*(1-'Assumptions'!D13)"],11:['Preferred cost',"='Assumptions'!D20"],12:['Common equity weight','=D6/SUM(D6:D8)'],13:['Debt weight','=D7/SUM(D6:D8)'],14:['Preferred weight','=D8/SUM(D6:D8)'],15:['WACC','=SUMPRODUCT(D9:D11,D12:D14)'],
29:['2031 revenue',"='Projections'!H15*(1+'Assumptions'!D14)"],30:['2031 NOPAT',"='Projections'!H30*(1+'Assumptions'!D14)"],31:['2031 D&A',"='Projections'!H32*(1+'Assumptions'!D14)"],32:['2031 normalized capex',"=D31*'Assumptions'!D15"],33:['2031 change in trade NWC',"='Projections'!H36*'Assumptions'!D14"],34:['Normalized terminal FCF','=D30+D31-D32-D33'],35:['Terminal value at end 2030',"=D34/(D15-'Assumptions'!D14)"],36:['Terminal discount time',"=(H18-'Assumptions'!D6)/365"],37:['Present value of terminal value','=D35/(1+D15)^D36'],38:['Present value of explicit FCF','=SUM(D25:H25)'],39:['Enterprise value','=SUM(D37:D38)'],40:['Terminal PV / enterprise value','=D37/D39'],42:['Cash and marketable securities',"='Historicals'!H42"],43:['Debt carrying value deduction',"=-SUM('Historicals'!H43:H44)"],44:['Preferred preference deduction','=-D8'],45:['Recognized non-marketable stakes',"='Historicals'!H50*'Assumptions'!D16"],46:['Deferred tax liability deduction',"=-'Historicals'!H51"],47:['Accrued legal claims deduction',"=-'Historicals'!H52"],48:['Net equity bridge adjustment','=SUM(D42:D47)'],49:['Common equity value','=D39+D48'],50:['Common shares, millions',"='Historicals'!H47"],51:['Value per common share','=D49/D50'],52:['Return vs closing price',"=D51/'Assumptions'!D7-1"]};
for(const[r,[l,x]]of Object.entries(dcfrows)){t('DCF',`C${r}`,l);f('DCF',`D${r}`,x);}for(const r of [9,10,11,12,13,14,15,40,52])sheets.DCF.getRange(`D${r}`).setNumberFormat(pct);sheets.DCF.getRange('D51').setNumberFormat(price);
row('DCF',17,'Cash-flow discounting',['2026 stub','2027E','2028E','2029E','2030E']);
for(let j=0;j<5;j++){const c=String.fromCharCode(68+j);v('DCF',`${c}18`,new Date(`${2027+j}-01-01T00:00:00Z`),'User requested annual forecast periods; exclusive period end');f('DCF',`${c}19`,j===0?"='Assumptions'!D6":`=DATE(YEAR(${c}18)-1,1,1)`);f('DCF',`${c}20`,`=(${c}18-${c}19)/365`);f('DCF',`${c}21`,`=((${c}18+${c}19)/2-'Assumptions'!D6)/365`);f('DCF',`${c}22`,`='Projections'!${c}40`);f('DCF',`${c}23`,j===0?"='Projections'!D99*(D18-D19)/(D18-DATE(2026,7,1))":`=${c}22`);f('DCF',`${c}24`,`=1/(1+$D$15)^${c}21`);f('DCF',`${c}25`,`=${c}23*${c}24`);}
for(const[r,l]of Object.entries({18:'Period end (exclusive)',19:'Period start',20:'Remaining years',21:'Midpoint discount time',22:'Full-year forecast FCF',23:'Cash flow valued',24:'Discount factor',25:'Present value of cash flow'}))t('DCF',`C${r}`,l);sheets.DCF.getRange('D18:H19').setNumberFormat('yyyy-mm-dd');sheets.DCF.getRange('D20:H21').setNumberFormat('0.000');sheets.DCF.getRange('D24:H24').setNumberFormat('0.000');for(const r of [15,25,34,39,48,49,51])total('DCF',r);note('DCF',55,'June balance sheet is held constant to the valuation date. Preferred conversion and equity-tax timing are simplified.');

// Direct formula sensitivities, required by dcf-model. All cells include live SUMPRODUCT and TV.
note('Sensitivity',6,'Same operating case. Rows vary WACC; columns vary growth. #N/A marks invalid WACC ≤ growth.','H');
for(let j=0;j<5;j++){const c=String.fromCharCode(68+j);f('Sensitivity',`${c}9`,`='Assumptions'!D14+(${j}-2)*'Assumptions'!D22`);}
for(let i=0;i<7;i++){const r=10+i;f('Sensitivity',`C${r}`,`='DCF'!D15+(${i}-3)*'Assumptions'!D21`);for(let j=0;j<5;j++){const c=String.fromCharCode(68+j);f('Sensitivity',`${c}${r}`,`=(SUMPRODUCT('DCF'!$D$23:$H$23,1/(1+$C${r})^'DCF'!$D$21:$H$21)+(('Projections'!$H$30+'Projections'!$H$32*(1-'Assumptions'!$D$15))*(1+${c}$9)-'Projections'!$H$36*${c}$9)/($C${r}-${c}$9)/(1+$C${r})^'DCF'!$D$36+'DCF'!$D$48)/'DCF'!$D$50`);}}
sheets.Sensitivity.getRange('D9:H9').setNumberFormat(pct);sheets.Sensitivity.getRange('C10:C16').setNumberFormat(pct);sheets.Sensitivity.getRange('D10:H16').setNumberFormat(price);sheets.Sensitivity.getRange('D10:H16').conditionalFormats.add('colorScale',{colors:['#F7E6E0','#FFFFFF','#C8DDE9'],thresholds:['min',{type:'percentile',value:50},'max']});
t('Sensitivity','C19','Grid center minus DCF');f('Sensitivity','D19',"=F13-'DCF'!D51");sheets.Sensitivity.getRange('D19').setNumberFormat('0.000000');t('Sensitivity','C21','Price');f('Sensitivity','D21',"='Assumptions'!D7");t('Sensitivity','C22','Required terminal FCF at base WACC');f('Sensitivity','D22',"=('Assumptions'!D7*'DCF'!D50-'DCF'!D48-'DCF'!D38)*(1+'DCF'!D15)^'DCF'!D36*('DCF'!D15-'Assumptions'!D14)");t('Sensitivity','C23','Required / modeled terminal FCF');f('Sensitivity','D23',"=D22/'DCF'!D34");sheets.Sensitivity.getRange('D23').setNumberFormat('0.00x');

// Peer data with aligned TTM periods and visible source arithmetic.
row('Multiples',6,'Peer inputs',['GOOGL','MSFT','META','AMZN'],'Quotes 2026-10-16; financials TTM through 2026-06-30. USD millions.');
const peerInput={8:['Closing price',[null,529.05,709.32,250],'GOOGL linked to Assumptions!D7. Q2 / Q3 / Q4 vendor closes 2026-10-16; exchange-direct unavailable.'],9:['Common shares, millions',[null,7427,null,10783],'GOOGL linked to Historicals!H47; S4 Microsoft period end; S10 Meta Class A + B (rows 68–69); S7 Amazon period end.'],11:['Cash & equivalents',[55911,20935,15462,78213],'S2 / S4 / S5 / S7 balance sheets, 2026-06-30.'],12:['Marketable securities',[186563,55908,74798,44775],'S2 / S4 / S5 / S7 balance sheets, 2026-06-30.'],13:['Debt non-current',[98165,31067,83664,128894],'S2 / S4 / S5 / S9 balance sheets. Excludes leases.'],14:['Debt current',[1999,9227,0,3330],'S2 / S4 / S5 no separate current debt disclosed / S9 Note 5.'],15:['Preferred liquidation preference',[19250,0,0,0],'S2 mandatory convertible preference; S4 / S5 / S7 no preferred claim reported.'],
20:['FY2025 revenue',[402836,null,200966,716924],'S1 / S6 / S8 calendar 2025. Microsoft direct TTM input below.'],21:['H1 2025 revenue',[186662,null,89830,323369],'S2 / S5 / S7, matched prior six months.'],22:['H1 2026 revenue',[229692,null,117111,382125],'S2 / S5 / S7, six months ended June 30.'],
25:['FY2025 operating income',[129039,null,83276,79975],'S1 / S6 / S8.'],26:['H1 2025 operating income',[61877,null,37997,37576],'S2 / S5 / S7.'],27:['H1 2026 operating income',[80466,null,41647,51313],'S2 / S5 / S7.'],
30:['FY2025 common net income',[132170,null,60458,77670],'S1 / S6 / S8, GAAP including investment and tax effects.'],31:['H1 2025 common net income',[62736,null,34981,35291],'S2 / S5 / S7.'],32:['H1 2026 common net income',[174685,null,42621,92902],'S2 common earnings after preferred dividends / S5 / S7.'],
35:['FY2025 PPE depreciation',peerTickers.map(x=>peerData.ppe_depreciation[x].fy2025??null),'X1 / X3 / X4: us-gaap:Depreciation, calendar FY2025.'],36:['H1 2025 PPE depreciation',peerTickers.map(x=>peerData.ppe_depreciation[x].h1_2025??null),'X1 / X3 / X4: us-gaap:Depreciation, six months ended June 30, 2025.'],37:['H1 2026 PPE depreciation',peerTickers.map(x=>peerData.ppe_depreciation[x].h1_2026??null),'X1 / X3 / X4: us-gaap:Depreciation, six months ended June 30, 2026.'],
40:['Direct TTM revenue',[null,331839,null,null],'S4 year ended June 30, 2026.'],41:['Direct TTM EBIT',[null,155237,null,null],'S4 year ended June 30, 2026.'],42:['Direct TTM net income',[null,133749,null,null],'S4 GAAP, year ended June 30, 2026.'],43:['Direct TTM PPE depreciation',[null,peerData.ppe_depreciation.MSFT.direct_ttm,null,null],'X2: us-gaap:Depreciation, July 1, 2025–June 30, 2026. Broad cash-flow addbacks are excluded.']};
for(const[r,[l,vals,n]]of Object.entries(peerInput))row('Multiples',+r,l,vals,n);
f('Multiples','D8',"='Assumptions'!D7");f('Multiples','D9',"='Historicals'!H47");
row('Multiples',68,'META Class A, period-end shares',[null,null,2206,null],'S10: June 30, 2026 balance sheet, shares in millions.');
row('Multiples',69,'META Class B, period-end shares',[null,null,342,null],'S10: June 30, 2026 balance sheet, shares in millions.');
f('Multiples','F9','=SUM(F68:F69)');
for(let i=0;i<4;i++){const c=String.fromCharCode(68+i);f('Multiples',`${c}10`,`=${c}8*${c}9`);f('Multiples',`${c}16`,`=${c}10+SUM(${c}13:${c}15)-SUM(${c}11:${c}12)`);for(const[out,start,direct]of [[23,20,40],[28,25,41],[33,30,42]])f('Multiples',`${c}${out}`,i===1?`=${c}${direct}`:`=${c}${start}-${c}${start+1}+${c}${start+2}`);f('Multiples',`${c}38`,i===1?`=${c}43`:`=${c}35-${c}36+${c}37`);f('Multiples',`${c}45`,`=${c}28+${c}38`);f('Multiples',`${c}47`,`=${c}10/${c}33`);f('Multiples',`${c}49`,`=${c}16/${c}23`);f('Multiples',`${c}50`,`=${c}16/${c}45`);}
const ml={10:'Equity market value proxy',16:'Enterprise value (excludes leases)',23:'TTM revenue',28:'TTM EBIT',33:'TTM common net income',38:'TTM PPE depreciation',45:'TTM EBITD (reported inputs)',47:'P/E, TTM GAAP',48:'Forward P/E',49:'EV / TTM sales',50:'EV / EBITD'};for(const[r,l]of Object.entries(ml))t('Multiples',`C${r}`,l);t('Multiples','J45','EBIT + PPE depreciation only for all. Reported source arithmetic in rows 35–43; bridge and policy in rows 84–95.');sheets.Multiples.getRange('D8:G8').setNumberFormat(price);sheets.Multiples.getRange('D47:G50').setNumberFormat('0.00x');
row('Multiples',53,'Peer valuation spread',['Low','Median','High'],'MSFT, META, AMZN only. GOOGL excluded from peer median.');
for(const [rr,pr,label]of [[54,47,'P/E'],[55,49,'EV/Sales'],[56,50,'EV/EBITD']]){t('Multiples',`C${rr}`,label);['MIN','MEDIAN','MAX'].forEach((fn,i)=>f('Multiples',`${String.fromCharCode(68+i)}${rr}`,`=${fn}(E${pr}:G${pr})`));}
sheets.Multiples.getRange('D54:F56').setNumberFormat('0.00x');
for(let i=0;i<3;i++){const c=String.fromCharCode(68+i);f('Multiples',`${c}59`,`=${c}54*$D$33/$D$9`);f('Multiples',`${c}60`,`=(${c}55*$D$23+'DCF'!$D$48)/$D$9`);f('Multiples',`${c}61`,`=(${c}56*$D$45+'DCF'!$D$48)/$D$9`);}t('Multiples','C59','P/E implied common value / share');t('Multiples','C60','EV/Sales implied value / share');t('Multiples','C61','EV/EBITD implied value / share');sheets.Multiples.getRange('D59:F61').setNumberFormat(price);note('Multiples',64,'GAAP P/E includes investment gains. EBITD adds only PPE depreciation for all issuers. Forward P/E uses adjusted consensus. Do not blend methods.');note('Multiples',66,'EV excludes leases for all. EBITD retains intangible amortization expense; no SBC, content, operating-lease or other cash-flow addbacks.');sheets.Multiples.freezePanes.freezeRows(6);

// Forward P/E: same calendar horizon, visible fiscal-year conversion and dated source inputs.
row('Multiples',72,'Forward earnings inputs',peerTickers,'F1–F4: S&P Global adjusted non-GAAP EPS via Stock Analysis; updated 2026-10-16.');
for(let i=0;i<4;i++){
 const ticker=peerTickers[i], c=String.fromCharCode(68+i), item=peerData.forward[ticker], src=`F${i+1}: ${item.url}; updated 2026-10-16; adjusted non-GAAP EPS.`;
 v('Multiples',`${c}73`,item.fy2027_eps,src+' FY2027 EPS.');
 v('Multiples',`${c}74`,new Date(item.fy2027_end+'T00:00:00Z'),src+' Fiscal year-end.');
 if(item.fy2028_eps!==null)v('Multiples',`${c}75`,item.fy2028_eps,src+' FY2028 EPS.');
 v('Multiples',`${c}76`,item.cy2027_first_fy_weight,'A1: calendarization weight; Microsoft uses equal halves of FY2027 and FY2028. Other companies have December year-end.');
 f('Multiples',`${c}77`,ticker==='MSFT'?`=${c}73*${c}76+${c}75*(1-${c}76)`:`=${c}73`);
 v('Multiples',`${c}78`,new Date('2026-10-16T00:00:00Z'),src+' Consensus update date.');
 f('Multiples',`${c}48`,`=${c}8/${c}77`);
}
for(const[r,l]of [[73,'FY2027 adjusted EPS'],[74,'FY2027 period end'],[75,'FY2028 adjusted EPS (MSFT)'],[76,'CY2027 weight from FY2027'],[77,'CY2027 adjusted EPS'],[78,'Consensus updated']])t('Multiples',`C${r}`,l);
for(const r of [73,75,77])sheets.Multiples.getRange(`D${r}:G${r}`).setNumberFormat(price);
for(const r of [74,78])sheets.Multiples.getRange(`D${r}:G${r}`).setNumberFormat('yyyy-mm-dd');
sheets.Multiples.getRange('D76:G76').setNumberFormat(pct);
t('Multiples','C48','Forward P/E (CY2027 adjusted)');
t('Multiples','J48','Price / CY2027 adjusted consensus EPS. See rows 72–82 for dated inputs and Microsoft calendarization.');
t('Multiples','C57','Forward P/E (CY2027 adjusted)');
['MIN','MEDIAN','MAX'].forEach((fn,i)=>{const c=String.fromCharCode(68+i);f('Multiples',`${c}57`,`=${fn}(E48:G48)`);f('Multiples',`${c}62`,`=${c}57*$D$77`);});
t('Multiples','C62','Forward P/E implied value / share');
sheets.Multiples.getRange('D57:F57').setNumberFormat('0.00x');sheets.Multiples.getRange('D62:F62').setNumberFormat(price);
note('Multiples',80,'MSFT CY2027 EPS = 50% FY2027 + 50% FY2028. Equal-half approximation; not a quarterly consensus forecast.');
note('Multiples',82,'Adjusted consensus EPS is distinct from historical GAAP earnings. Provider adjustments are retained; the DCF still expenses SBC.');

// Verified EBITD replaces EBITDA by the user's explicit lecture preference.
row('Multiples',84,'TTM bridge: Jul 2025–Jun 2026',peerTickers,'X1–X4: reported PP&E depreciation. Calendar issuers: FY2025 - H1 2025 + H1 2026. MSFT FY2026 matches TTM.');
for(const[r,l]of [[85,'TTM EBIT'],[86,'TTM PPE depreciation'],[87,'TTM EBITD = EBIT + PPE dep.'],[88,'EV / EBITD'],[89,'Headline reconciliation difference']])t('Multiples',`C${r}`,l);
for(const c of ['D','E','F','G']){f('Multiples',`${c}85`,`=${c}28`);f('Multiples',`${c}86`,`=${c}38`);f('Multiples',`${c}87`,`=${c}85+${c}86`);f('Multiples',`${c}88`,`=${c}16/${c}87`);f('Multiples',`${c}89`,`=${c}45-${c}87`);}
sheets.Multiples.getRange('D88:G88').setNumberFormat('0.00x');total('Multiples',87);
note('Multiples',91,'EBITD is deliberate: EBIT + PPE depreciation only. Intangible amortization stays expensed for every issuer; no estimates are introduced.');
note('Multiples',93,'No SBC, content, operating-lease asset or other cash-flow addbacks. EV excludes lease liabilities uniformly; lease mixes still differ.');
note('Multiples',95,'Full TTM intangible amortization is unavailable for GOOGL / AMZN. EBITD adds PP&E depreciation; intangible amortization stays expensed.');
for(const r of [72,84])sheets.Multiples.getRange(`C${r}:G${r}`).format={fill:navy,font:{color:'#FFFFFF',bold:true}};total('Multiples',77);

// Main output is links only. Sensitivity bounds do not pretend to be bull/bear captured scenarios.
t('Summary','C6','Valuation date');f('Summary','D6',"='Assumptions'!D6");sheets.Summary.getRange('D6').setNumberFormat('yyyy-mm-dd');t('Summary','F6','Closing price');f('Summary','G6',"='Assumptions'!D7");sheets.Summary.getRange('G6').setNumberFormat(price);
row('Summary',8,'Value per common share',['Low','Active / median','High','Market']);
const meth=['DCF','P/E (GAAP TTM)','EV / Sales','EV / EBITD'];for(let i=0;i<4;i++){const r=9+i;t('Summary',`C${r}`,meth[i]);f('Summary',`G${r}`,"='Assumptions'!D7");if(i===0){f('Summary','D9',"='Sensitivity'!E16");f('Summary','E9',"='DCF'!D51");f('Summary','F9',"='Sensitivity'!G10");}else for(let j=0;j<3;j++)f('Summary',`${String.fromCharCode(68+j)}${r}`,`='Multiples'!${String.fromCharCode(68+j)}${58+i}`);}
sheets.Summary.getRange('D9:G12').setNumberFormat(price);sheets.Summary.getRange('C8:G8').format={fill:navy,font:{color:'#FFFFFF',bold:true}};total('Summary',9);
for(const[r,l,x]of [[15,'Selected-case WACC',"='DCF'!D15"],[16,'Terminal growth',"='Assumptions'!D14"],[17,'Terminal value / EV',"='DCF'!D40"],[18,'DCF vs closing price',"='DCF'!D52"],[20,'2030 forecast revenue',"='Projections'!H15"],[21,'2027 capex intensity',"='Assumptions'!E83"],[22,'2027 unlevered cash flow',"='Projections'!E40"],[23,'Required / modeled terminal FCF',"='Sensitivity'!D23"]]){t('Summary',`C${r}`,l);f('Summary',`D${r}`,x);}for(const r of [15,16,17,18,21])sheets.Summary.getRange(`D${r}`).setNumberFormat(pct);sheets.Summary.getRange('D23').setNumberFormat('0.00x');
note('Summary',26,'DCF low/high: WACC ±1.5 pp, growth ±0.5 pp. Peer low/high: minimum/maximum multiples. These are not Bull/Bear cases.');note('Summary',28,'Forward P/E uses CY2027 adjusted consensus, with MSFT calendarized. GAAP P/E includes investment gains.');
t('Summary','C13','Forward P/E (CY2027 adjusted)');
for(const c of ['D','E','F'])f('Summary',`${c}13`,`='Multiples'!${c}62`);
f('Summary','G13',"='Assumptions'!D7");sheets.Summary.getRange('D13:G13').setNumberFormat(price);
note('Summary',30,'EV/EBITD = EV / (EBIT + PPE depreciation), using reported inputs. It replaces EBITDA; all intangible amortization remains expensed.');
sheets.DCF.getRange('D36').setNumberFormat('0.000');
t('Sensitivity','C9','WACC / terminal growth');
sheets.Sensitivity.getRange('D21').setNumberFormat(price);
t('Summary','C20','2030 revenue (USD millions)');
t('Summary','C22','2027 FCF (USD millions)');
t('Summary','C24','Terminal-value condition');f('Summary','D24',"=IF('DCF'!D15<='Assumptions'!D14,\"Growth must be below WACC\",\"WACC exceeds growth\")");sheets.Summary.getRange('D24:H24').merge();
// Guard the Gordon model's mathematical domain in the owning calculation and each grid cell.
f('DCF','D35',"=IF(D15<='Assumptions'!D14,NA(),D34/(D15-'Assumptions'!D14))");
for(let r=10;r<=16;r++)for(const c of ['D','E','F','G','H']){const original=sheets.Sensitivity.getRange(`${c}${r}`).formulas[0][0];f('Sensitivity',`${c}${r}`,`=IF($C${r}<=${c}$9,NA(),${original.slice(1)})`);}
const chart=sheets.Summary.charts.add('bar',[sheets.Summary.getRange('C8:C13'),sheets.Summary.getRange('E8:E13'),sheets.Summary.getRange('G8:G13')]);chart.title='Value per share and closing price';chart.titleTextStyle.typeface='Arial';chart.titleTextStyle.fontSize=13;chart.setPosition('J8','Q26');chart.legend={position:'top',textStyle:{typeface:'Arial'}};chart.xAxis={axisType:'textAxis',textStyle:{typeface:'Arial'}};chart.yAxis={numberFormatCode:'$0',numberFormatSourceLinked:false,textStyle:{typeface:'Arial'}};

// Audit all numeric hardcodes with a cell-level provenance manifest.
await fs.writeFile(path.join(root,'input-provenance.json'),JSON.stringify({as_of:'2026-10-17',sources,inputs},null,2));
wb.recalculate();
const diagnostics={engine:'@oai/artifact-tool',as_of:'2026-10-17',inspections:{},render_errors:[]};
for(const n of ['Summary','Historicals','DCF','Sensitivity'])diagnostics.inspections[n]=(await wb.inspect({kind:'table',range:`${n}!C6:H25`,include:'values,formulas',tableMaxRows:20,tableMaxCols:6,maxChars:8000})).ndjson;
diagnostics.formula_errors=(await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'Formula error scan'})).ndjson;
await fs.writeFile(path.join(root,'artifact-validation.json'),JSON.stringify(diagnostics,null,2));
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(root,'GOOGL_DCF_Valuation.xlsx'));
await fs.mkdir(path.join(root,'previews'),{recursive:true});
const renders=names.map(n=>[n,n,n==='Summary'?'C2:Q31':n==='README'?'C2:J36':n==='Assumptions'?'C26:H91':n==='Projections'?'C6:H41':n==='Historicals'?'C6:H34':n==='DCF'?'C6:H52':n==='Sensitivity'?'C6:H23':'C45:J66']);
renders.push(['Multiples','Multiples-forward','C68:J82'],['Multiples','Multiples-bridge','C84:J96']);
for(const[n,file,range]of renders){try{const png=await wb.render({sheetName:n,range,scale:1,format:'png'});await fs.writeFile(path.join(root,'previews',file+'.png'),new Uint8Array(await png.arrayBuffer()));}catch(e){diagnostics.render_errors.push({sheet:n,range,error:String(e)});}}
await fs.writeFile(path.join(root,'artifact-validation.json'),JSON.stringify(diagnostics,null,2));
console.log(JSON.stringify({output:'GOOGL_DCF_Valuation.xlsx',render_errors:diagnostics.render_errors,formula_errors:diagnostics.formula_errors}));
