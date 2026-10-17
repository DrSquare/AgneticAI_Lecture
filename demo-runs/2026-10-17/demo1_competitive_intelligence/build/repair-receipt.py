from pathlib import Path
import shutil
p=Path('demo-runs/2026-10-17/demo1_competitive_intelligence/build/build-artifacts.mjs')
s=p.read_text(encoding='utf-8')
old="const final=build+'/validated-v2/IC-pack.pptx'; await fs.mkdir(build+'/validated-v2',{recursive:true});"
new="const stamp=Date.now(); const finalDir=build+'/validated-'+stamp; const final=finalDir+'/IC-pack.pptx'; const receiptPath=build+'/IC-pack-'+stamp+'.validation.json'; await fs.mkdir(finalDir,{recursive:true});"
assert old in s
s=s.replace(old,new).replace("receiptPath:build+'/IC-pack.validation.json'","receiptPath")
s=s.replace("await fs.copyFile(final,run+'/IC-pack.pptx');","await fs.copyFile(receiptPath,build+'/IC-pack.validation.json');\nawait fs.copyFile(final,run+'/IC-pack.pptx');")
p.write_text(s,encoding='utf-8')
b=p.parent
shutil.copyfile(b/'IC-pack.validation.json',b/'IC-pack.v1.validation.json')
