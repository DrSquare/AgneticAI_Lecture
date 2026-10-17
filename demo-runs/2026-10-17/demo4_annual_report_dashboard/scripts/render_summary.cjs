const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('C:/Users/h_min/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..');
const esc=x=>x.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const inline=x=>esc(x).replace(/\[([^\]]+)\]\((https?:[^\s)]+)\)/g,'<a href="$2">$1</a>').replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>');
let html='',list=false;
for(const line of fs.readFileSync(path.join(root,'exec-summary.md'),'utf8').split(/\r?\n/)){
 if(/^[-*] |^\d+\. /.test(line)){if(!list){html+='<ul>';list=true;}html+='<li>'+inline(line.replace(/^[-*] |^\d+\. /,''))+'</li>';continue;}
 if(list){html+='</ul>';list=false;}
 if(/^#{1,3} /.test(line)){const n=line.match(/^#+/)[0].length;html+=`<h${n}>${inline(line.slice(n+1))}</h${n}>`;}
 else if(line.trim()&&!/^---+$/.test(line))html+='<p>'+inline(line)+'</p>';
}
if(list)html+='</ul>';
const doc=`<!doctype html><html lang="en"><meta charset="utf-8"><title>NVIDIA FY2026 Board brief</title><style>@page{size:A4;margin:12mm 14mm}body{font-family:Arial,sans-serif;color:#183044;font-size:10pt;line-height:1.3;margin:0}h1{font-size:20pt;line-height:1.1;margin:0 0 7pt;color:#17334a}h2{font-size:11.5pt;margin:9pt 0 3pt;border-bottom:1px solid #bccdd7;padding-bottom:2pt}h3{font-size:10.5pt;margin:7pt 0 2pt}p{margin:3pt 0}ul{margin:2pt 0;padding-left:15pt}li{margin:0 0 4pt;break-inside:avoid}a{color:inherit;text-decoration:none}strong{color:#102b40}</style><body>${html}</body></html>`;
fs.writeFileSync(path.join(root,'evidence','exec-summary-print.html'),doc);
(async()=>{const b=await chromium.launch({headless:true,executablePath:'C:/Users/h_min/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe'});const c=await b.newContext({offline:true});const p=await c.newPage();await p.setContent(doc);await p.pdf({path:path.join(root,'exec-summary.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true});await b.close();console.log('Saved exec-summary.pdf');})();
