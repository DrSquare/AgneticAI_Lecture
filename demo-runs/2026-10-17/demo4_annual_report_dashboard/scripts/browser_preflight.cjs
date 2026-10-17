const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const runtime='C:/Users/h_min/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright';
const {chromium}=require(runtime);
(async()=>{const b=await chromium.launch({headless:true,executablePath:'C:/Users/h_min/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe'});const p=await b.newPage();await p.setContent('<!doctype html><html><body><h1>Local browser ready</h1></body></html>');const out={browser:await b.version(),executable:'C:/Users/h_min/AppData/Local/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-win64/chrome-headless-shell.exe',runtime,heading:await p.locator('h1').innerText()};fs.writeFileSync(path.join(root,'evidence','browser-environment.json'),JSON.stringify(out,null,2));console.log(out);await b.close();})();


