import fs from 'node:fs/promises';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';
const root = 'C:/Users/h_min/repos/SNU_Agentic_AI_Lecture';
const out = root + '/demo-runs/2026-10-17/demo1_competitive_intelligence/build';
const p = await PresentationFile.importPptx(await FileBlob.load(out+'/reference-subset.pptx'));
console.log((await p.inspect({kind:'slide,textbox,layout',search:'Five profiles',maxChars:5000})).ndjson);
const png = await p.export({slide:p.slides.items[0],format:'png',scale:1});
await fs.writeFile(out+'/reference-slide24.png',new Uint8Array(await png.arrayBuffer()));
console.log('Reference rendered');
