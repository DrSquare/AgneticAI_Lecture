from pathlib import Path
p=Path('demo-runs/2026-10-17/demo1_competitive_intelligence/build/build-artifacts.mjs')
s=p.read_text(encoding='utf-8')
s=s.replace("const final=run+'/IC-pack.pptx';","const final=build+'/validated/IC-pack.pptx'; await fs.mkdir(build+'/validated',{recursive:true});")
s=s.replace("const finalP=await PresentationFile.importPptx","await fs.copyFile(final,run+'/IC-pack.pptx');\nconst finalP=await PresentationFile.importPptx")
p.write_text(s,encoding='utf-8')
