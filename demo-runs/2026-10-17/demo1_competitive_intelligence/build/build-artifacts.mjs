import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {Workbook,SpreadsheetFile,Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
const run='C:/Users/h_min/repos/SNU_Agentic_AI_Lecture/demo-runs/2026-10-17/demo1_competitive_intelligence';
const build=run+'/build',root='C:/Users/h_min/repos/SNU_Agentic_AI_Lecture';
const presSkill='C:/Users/h_min/.codex/plugins/cache/openai-primary-runtime/presentations/26.1013.11914/skills/presentations';
const python='C:/Users/h_min/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const slugs=['figure-ai','physical-intelligence','skild-ai','agility-robotics','1x-technologies'];
const data=await Promise.all(slugs.map(async x=>JSON.parse((await fs.readFile(run+'/research/'+x+'-data.json','utf8')).replace(/^\uFEFF/,''))));
const url=x=>typeof x==='string'?x:x?.url||'Not disclosed';
const asOf=new Date('2026-10-17T00:00:00Z');
const shortLayers=['Full-stack humanoid','Robot foundation model','Model + acquired operations','Logistics humanoid','Home humanoid'];
const bases=['Historical post-money','Investor baseline, basis unclear','Greater-than endpoint','Proposed pre-money SPAC','Reported talks, unconfirmed'];
const valDates=['2025-09-16','2025-11','2026-01-14','2026-06-24','2026-08-26'];
const revenue=['Not disclosed. BMW pilot and Catalyst agreement.','Not disclosed. API beta and partner deployments.','>$100M ARR, company-reported in Sep 2026.','FY2025 sales $1.782M, indexed SEC table.','Not disclosed. Preorders, external deliveries unverified.'];
const momentum=['Gaining on technical/customer milestones','Gaining on model and API distribution','Gaining on reported commercial adoption','Under pressure from financing conditions','Holding pending independent delivery evidence'];
const roundAmount=[null,0.6,1.4,0.1,0.1];
const roundBasis=['Sep 2026 strategic equity, amount undisclosed','Nov 2025 verified Series B, $B','Jan 2026 Series C, $B','July 2026 SAFEs, $B','Jan 2024 Series B, $B (outside window)'];
if(process.argv[2]!=='deck'){
const checks=[];
const wb=Workbook.create(),matrix=wb.worksheets.add('Matrix'),land=wb.worksheets.add('Landscape');
for(const s of [matrix,land]){s.showGridLines=false;s.getRange('A1:L30').format.font={name:'Arial',size:11};s.getRange('A1:L30').format.verticalAlignment='center';}
matrix.tabColor='#10243A';
matrix.getRange('A2').values=[['Embodied AI financing comparison']];
matrix.getRange('A2').format.font={name:'Arial',size:17,bold:true,color:'#10243A'};
matrix.getRange('A3:B3').values=[['As of',asOf]];matrix.getRange('B3').setNumberFormat('yyyy-mm-dd');
matrix.getRange('C3').values=[['Window: 2025-10-17 to 2026-10-17']];
matrix.getRange('A5:J5').values=[['Company','Valuation ($B)','Valuation basis','Total capital ($B)','Valuation / capital','Ratio eligible','Latest evidence','Age (days)','Verified round ($B)','Round basis and date']];
matrix.getRange('L5').values=[['Input source URLs and dates']];
[180,110,210,115,125,100,115,90,125,245,24,620].forEach((w,i)=>matrix.getRangeByIndexes(0,i,30,1).format.columnWidthPx=w);
matrix.getRange('A5:J5').format={fill:'#10243A',font:{name:'Arial',bold:true,color:'#FFFFFF',size:11},wrapText:true,horizontalAlignment:'center'};
matrix.getRange('L5').format={fill:'#10243A',font:{name:'Arial',bold:true,color:'#FFFFFF',size:11}};
matrix.getRange('A5:L5').format.rowHeightPx=48;
for(let i=0;i<5;i++){const r=i+6,d=data[i];
matrix.getRange('A'+r+':D'+r).values=[[d.company,d.valuation_usd_billion??null,bases[i],null]];
matrix.getRange('E'+r).formulas=[['=IF(OR(B'+r+'="",D'+r+'="",D'+r+'=0,F'+r+'<>TRUE),"Not comparable",B'+r+'/D'+r+')']];
matrix.getRange('F'+r+':J'+r).values=[[false,new Date(d.latest_evidence_date+'T00:00:00Z'),null,roundAmount[i],roundBasis[i]]];
matrix.getRange('H'+r).formulas=[['=$B$3-G'+r]];
matrix.getRange('A'+r+':L'+r).format.rowHeightPx=125;matrix.getRange('A'+r+':J'+r).format.fill=i%2?'#F0F4F5':'#FFFFFF';matrix.getRange('A'+r+':L'+r).format.wrapText=true;
matrix.getRange('L'+r).values=[['Valuation ('+valDates[i]+'): '+url(d.valuation_source)+'\nCapital: not verified in this run.\nRound: '+url(d.latest_round_source)+'\nLatest evidence: '+d.latest_evidence_date+'. See dated profile for publication context.']];}
matrix.getRange('B6:B10').setNumberFormat('0.0');matrix.getRange('D6:E10').setNumberFormat('0.00');matrix.getRange('G6:G10').setNumberFormat('yyyy-mm-dd');matrix.getRange('H6:H10').setNumberFormat('0');matrix.getRange('I6:I10').setNumberFormat('0.000');
matrix.getRange('B6:D10').format.font.color='#0000FF';matrix.getRange('F6:G10').format.font.color='#0000FF';matrix.getRange('I6:I10').format.font.color='#0000FF';
['Blank capital inputs mean unavailable, not zero. Blue numeric cells are inputs.','Ratio eligible stays FALSE until valuation and capital are exact and measured on a comparable basis.','Reported, proposed and lower-bound figures are endpoints with qualifiers, not interchangeable company values.','The 1X round is historical. Figure has newer strategic equity with an undisclosed amount.','The $B unit applies to financing only. Revenue definitions and dates appear on Landscape.'].forEach((x,i)=>matrix.getRange('A'+(12+i)).values=[[x]]);
matrix.freezePanes.freezeRows(5);matrix.freezePanes.freezeColumns(1);
land.getRange('A2').values=[['Operating landscape']];land.getRange('A2').format.font={name:'Arial',size:17,bold:true,color:'#10243A'};
land.getRange('A3').values=[['Prepared 2026-10-17. Momentum is analyst judgment, not a measured market-share ranking.']];
land.getRange('A5:H5').values=[['Company','Layer','Flagship','Revenue signal','Customers / partners','Manufacturing and scale','Main diligence risk','Momentum']];
[180,180,250,260,320,390,320,230].forEach((w,i)=>land.getRangeByIndexes(0,i,15,1).format.columnWidthPx=w);
land.getRange('A5:H5').format={fill:'#10243A',font:{name:'Arial',bold:true,color:'#FFFFFF',size:11},horizontalAlignment:'center',wrapText:true};land.getRange('A5:H5').format.rowHeightPx=42;
data.forEach((d,i)=>{let r=i+6;land.getRange('A'+r+':H'+r).values=[[d.company,shortLayers[i],d.flagship,revenue[i],d.customers,d.scale,d.top_risk,momentum[i]]];land.getRange('A'+r+':H'+r).format={wrapText:true,fill:i%2?'#F0F4F5':'#FFFFFF'};land.getRange('A'+r+':H'+r).format.rowHeightPx=165;});
land.getRange('A12').values=[['Sources: company profiles and evidence JSON in research/. Financing URLs sit beside inputs on Matrix.']];
land.getRange('A13').values=[['Company-reported metrics are unaudited. Capacity, orders and deliveries differ.']];
land.freezePanes.freezeRows(5);land.freezePanes.freezeColumns(1);
wb.recalculate();
await fs.writeFile(build+'/workbook-inspection.ndjson',(await wb.inspect({kind:'table',range:'Matrix!A5:J10',include:'values,formulas',tableMaxRows:6,tableMaxCols:10,maxChars:13000})).ndjson);
const initial=matrix.getRange('H6:H10').values.flat(),expected=data.map(d=>Math.round((asOf-new Date(d.latest_evidence_date+'T00:00:00Z'))/86400000));
if(JSON.stringify(initial)!==JSON.stringify(expected))throw new Error('Source-age formulas disagree '+JSON.stringify({initial,expected}));
checks.push({name:'Five evidence-age formulas',status:'passed',evidence:{actual:initial,expected}});
const originalDate=matrix.getRange('G6').values;
matrix.getRange('G6').values=[[new Date(new Date(data[0].latest_evidence_date+'T00:00:00Z').getTime()+86400000)]];wb.recalculate();
if(matrix.getRange('H6').values[0][0]!==expected[0]-1)throw new Error('Date sensitivity failed');
matrix.getRange('G6').values=originalDate;
matrix.getRange('D6').values=[[1]];matrix.getRange('F6').values=[[true]];wb.recalculate();
if(matrix.getRange('E6').values[0][0]!==39)throw new Error('Ratio sensitivity failed');
matrix.getRange('D6').values=[[0]];wb.recalculate();
if(matrix.getRange('E6').values[0][0]!=='Not comparable')throw new Error('Zero guard failed');
matrix.getRange('D6').values=[[null]];matrix.getRange('F6').values=[[false]];wb.recalculate();
checks.push({name:'Recalculation and missing-data boundaries',status:'passed',evidence:'Date +1 reduces age by 1. Temporary comparable capital 1 produces 39x. Zero and blank suppress ratio. Original inputs restored.'});
await fs.writeFile(build+'/workbook-error-scan.ndjson',(await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:300},summary:'Final formula error scan'})).ndjson);
await fs.writeFile(build+'/workbook-checks.json',JSON.stringify(checks,null,2));
await (await SpreadsheetFile.exportXlsx(wb)).save(run+'/research/competitor-matrix.xlsx');
for(const [sheetName,range,file] of [['Matrix','A1:J17','matrix'],['Matrix','L5:L10','matrix-sources'],['Landscape','A1:D13','landscape-left'],['Landscape','E5:H10','landscape-right']]){
const img=await wb.render({sheetName,range,scale:1.5,format:'png'});await fs.writeFile(build+'/'+file+'.png',new Uint8Array(await img.arrayBuffer()));}
console.log('WORKBOOK_COMPLETE');
}
const p=Presentation.create({slideSize:{width:1280,height:720}});
const font='IBM Plex Sans',navy='#10243A',green='#1B6F69',gray='#3B4856';
function txt(s,text,x,y,w,h,size=24,color=gray,bold=false){const o=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});o.text=text;o.text.style={typeface:font,fontSize:size,color,bold};return o;}
function base(title,sub){const s=p.slides.add();s.background.fill='#FFFFFF';txt(s,title,58,48,1164,64,40,navy,true);txt(s,sub,60,116,1160,44,19,gray);txt(s,'IC discussion / Research cutoff 17 Oct 2026',60,670,1160,24,14,'#6B7785');return s;}
const notes=data.map((d,i)=>d.company+'\n'+(d.spot_checks||[]).map(x=>x.date+': '+x.claim+'\n'+(x.primary_url||x.secondary_url||'Unconfirmed source')+'\n'+x.verdict).join('\n')+'\nProfile: research/'+slugs[i]+'.md').join('\n\n')+'\n\nSource bibliography:\n'+(await Promise.all(slugs.map(async slug=>(await fs.readFile(run+'/research/'+slug+'.md','utf8')).split('\n').filter(line=>line.includes('http')).join('\n')))).join('\n\n');
function table(s,values,widths,y,height){const t=s.tables.add({rows:values.length,columns:values[0].length,left:60,top:y,width:1160,height,columnWidths:widths,values});t.borders.assign({fill:'#D8E1E7',width:0.7,style:'solid'});t.cells.block({row:0,column:0,rowCount:values.length,columnCount:values[0].length}).assign({textStyle:{typeface:font,fontSize:20,color:gray},margins:{left:14,right:12,top:6,bottom:6},anchor:'center'});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){t.getCell(r,c).fill=r===0?navy:(r%2?'#FFFFFF':'#EEF5F4');if(r===0)t.getCell(r,c).text.style={typeface:font,fontSize:20,bold:true,color:'#FFFFFF'};}return t;}
let s=base('Five companies, different routes to adoption','Financing benchmarks use different dates and transaction structures');
table(s,[['Company / layer','Financing reference','Commercial evidence'],['Figure AI\nFull-stack humanoid','$39B post-money\nSep 2025, outside window','BMW confirms pilot contribution.\nRevenue not disclosed.'],['Physical Intelligence\nRobot foundation model','$5.6B investor baseline\nNov 2025, basis unspecified','API beta, Oct 2026.\nRevenue not disclosed.'],['Skild AI\nModel + operations','>$14B valuation\nJan 2026','>$100M ARR, Sep 2026.\nCompany-reported, unaudited.'],['Agility Robotics\nLogistics humanoid','$2.5B proposed SPAC\nVote scheduled 2 Nov 2026','$1.782M FY2025 net sales.\nIndexed SEC table evidence.'],['1X Technologies\nHome humanoid','~$6B reported talks\nUnconfirmed acquisition value','Preorders. External customer\nunit count remains unverified.']],[325,380,455],180,430);
txt(s,'A proposed or reported valuation does not establish a closed transaction or current market value.',60,625,1150,32,17,green);
s.speakerNotes.text='Landscape sources and qualification:\n'+notes+'\nAgility full SEC filing was not retrieved. Amount corroborated from indexed primary table. No claim of a full filing audit.';
s=base('The differentiators shape the diligence agenda','Hardware, model distribution and target environments require different evidence');
table(s,[['Company','Distinctive position','Evidence the IC still needs'],['Figure AI','Integrated humanoid + proprietary AI,\nwith a customer-confirmed BMW pilot','Paid fleet size, autonomy across shifts,\nand service cost per productive hour'],['Physical Intelligence','Model research and hosted API\nacross partner robot platforms','Conversion of beta/partners to paying\nuse, intervention and hosting economics'],['Skild AI','Commercial model deployments plus\nacquired mobile-robot operations','ARR reconciliation, customer retention,\nand acquired hardware obligations'],['Agility Robotics','Defined logistics workflows and\nSPAC financial disclosure','Conditional order conversion,\nliquidity through transaction close'],['1X Technologies','Home use and teleoperation-supported\nlearning, with manufacturing ramp','External deliveries, supervision cost,\nand home privacy controls']],[245,445,470],180,430);
txt(s,'These business models require different proof of adoption and operating economics.',60,625,1150,32,17,green);
s.speakerNotes.text='Analyst interpretation grounded in company profiles. Risk questions are diligence requests, not verified defects.\n'+notes;
s=base('Three implications for the investment committee','Analyst judgment based on the inspected public evidence');
const imp=[['1  Commercial evidence should drive underwriting','Request contracts, cash collections and retention. Separate recognized revenue from ARR, pilot activity, preorders and conditional order value.'],['2  Financing comparisons need a common basis','Keep historical priced rounds, proposed SPAC values and reported talks separate. Revisit Agility after the vote and any closing, without presuming either outcome.'],['3  Autonomy economics deserve a dedicated workstream','Measure interventions, productive utilization and service costs at customer sites. Capacity targets and model demonstrations cannot establish delivery economics.']];
imp.forEach((a,i)=>{const y=188+i*145;txt(s,a[0],60,y,1160,44,28,green,true);txt(s,a[1],60,y+49,1135,75,24,gray);});
s.speakerNotes.text='Diligence implications. No recurring task is activated.\n'+notes;
const candidate=build+'/IC-pack-draft.pptx';await (await PresentationFile.exportPptx(p)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(presSkill+'/container_tools/artifact_tool_utils.mjs').href);
const stamp=Date.now(); const finalDir=build+'/validated-'+stamp; const final=finalDir+'/IC-pack.pptx'; const receiptPath=build+'/IC-pack-'+stamp+'.validation.json'; await fs.mkdir(finalDir,{recursive:true});
process.env.RUNTIME_NODE_MODULES='C:/Users/h_min/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const result=await finalizePresentation({workspaceDir:run,candidatePath:candidate,finalPath:final,pythonExecutable:python,integrityValidatorPath:presSkill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:presSkill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','1','--require-native-table-slide','2'],explicitTotalSlideCount:3,requiredNativeTableOwnerSlides:[1,2],fontPolicy:{basis:'reference',families:[font],referencePath:root+'/Agentic_AI_Define_Design_Build.pptx',referenceSha256:crypto.createHash('sha256').update(await fs.readFile(root+'/Agentic_AI_Define_Design_Build.pptx')).digest('hex')},verifyArtifactToolImport:true,receiptPath});
await fs.copyFile(receiptPath,build+'/IC-pack.validation.json');
await fs.copyFile(final,run+'/IC-pack.pptx');
const finalP=await PresentationFile.importPptx(await FileBlob.load(final));
for(let i=0;i<3;i++){const img=await finalP.export({slide:finalP.slides.items[i],format:'png',scale:1.5});await fs.writeFile(build+'/slide-'+(i+1)+'.png',new Uint8Array(await img.arrayBuffer()));}
await fs.writeFile(build+'/deck-inspection.ndjson',(await finalP.inspect({kind:'slide,table,notes',maxChars:30000})).ndjson);
console.log('DECK_COMPLETE',JSON.stringify(result));
