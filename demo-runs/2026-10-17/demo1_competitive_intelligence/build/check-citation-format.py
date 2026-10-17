from pathlib import Path
import json,re
r=Path('demo-runs/2026-10-17/demo1_competitive_intelligence')
report=[]
for f in (r/'research').glob('*.md'):
 if f.name in ['summary.md','evidence-checks.md','handoffs.md']:continue
 s=f.read_text(encoding='utf-8-sig')
 body=re.split(r'^## (?:Sources|Source|References)',s,flags=re.M)[0]
 bullets=[x for x in body.splitlines() if x.startswith('- ')]
 bad=[x for x in bullets if not re.search(r'\*\s*\[\d+(?:,\s*\d+)*\]\.?\s*$',x)]
 report.append({'file':f.name,'bullet_count':len(bullets),'nonstandard_endings':bad})
print(json.dumps(report,indent=2,ensure_ascii=False))
d=json.loads((r/'build/support-content.json').read_text())
d['RUNBOOK.md']=d['RUNBOOK.md'].replace('Keep prior final decks under a revision name before rerunning: the finalizer deliberately refuses to overwrite a final output.','The builder creates fresh timestamped validation folders and receipts, then copies the checked deck to IC-pack.pptx. Archive the delivered workbook/deck first if you need to preserve a prior version.')
(r/'build/support-content.json').write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8')
(r/'RUNBOOK.md').write_text(d['RUNBOOK.md'],encoding='utf-8')
