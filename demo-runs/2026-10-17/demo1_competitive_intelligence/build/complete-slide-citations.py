from pathlib import Path
p=Path('demo-runs/2026-10-17/demo1_competitive_intelligence/build/build-artifacts.mjs')
s=p.read_text(encoding='utf-8')
s=s.replace("x.primary_url+'\\n'", "(x.primary_url||x.secondary_url||'Unconfirmed source')+'\\n'")
old=".join('\\n\\n');\nfunction table"
new=".join('\\n\\n')+'\\n\\nSource bibliography:\\n'+(await Promise.all(slugs.map(async slug=>(await fs.readFile(run+'/research/'+slug+'.md','utf8')).split('\\n').filter(line=>line.includes('http')).join('\\n')))).join('\\n\\n');\nfunction table"
assert old in s
s=s.replace(old,new)
s=s.replace("build+'/validated/IC-pack.pptx'","build+'/validated-v2/IC-pack.pptx'").replace("fs.mkdir(build+'/validated'","fs.mkdir(build+'/validated-v2'")
p.write_text(s,encoding='utf-8')
