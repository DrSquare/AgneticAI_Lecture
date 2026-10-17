from pathlib import Path
import re,json
r=Path('demo-runs/2026-10-17/demo1_competitive_intelligence')
results=[]
for slug in ['figure-ai','physical-intelligence','skild-ai','agility-robotics','1x-technologies']:
 s=(r/'research'/f'{slug}.md').read_text(encoding='utf-8')
 body=re.split(r'^## (?:Sources|Source|References)',s,flags=re.M)[0]
 bullets=[x for x in body.splitlines() if x.startswith('- ')]
 bad=[x for x in bullets if not re.search(r'\*\s*(?:\[\d+(?:,\s*\d+)*\])+\s*\.?$',x)]
 assert not bad,(slug,bad)
 results.append({'company':slug,'dated_cited_bullets':len(bullets),'status':'passed'})
(r/'build/citation-format-checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results))
