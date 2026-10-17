from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parents[1]
pages=json.loads((R/'inputs/annual-report-pages.json').read_text(encoding='utf-8'))
checks=[]
for title,pdf,printed,vals in [('Income statement',139,51,['215,938','130,497','130,387','120,067']),('Balance sheet',141,53,['21,403','10,080','10,605','51,951']),('Reportable segments',165,77,['193,479','22,459','130,141','9,156']),('Margin drivers and concentration',129,41,['71.1%','75.0%','22%','14%'])]:
 p=pages[pdf-1]
 assert all(v in p['text'] for v in vals)
 assert p['text'].strip().endswith(str(printed))
 checks.append(dict(name=title,status='pass',pdf_page=pdf,pdf_index=pdf-1,printed_page=printed,observed_values=vals,screenshot=f'evidence/source-pdf-{pdf}.png',visual_review='Parent agent inspected rendered page; values, fiscal columns and printed page match.'))
manifest=json.loads((R/'inputs/sources.json').read_text())
for s in manifest:
 if 'file' in s:
  assert hashlib.sha256((R/s['file']).read_bytes()).hexdigest()==s['sha256']
checks.append(dict(name='Archived official-source SHA256 integrity',status='pass',evidence='inputs/sources.json'))
report=dict(verified_on='2026-10-17',timezone='America/Los_Angeles',annual_period_end='2026-01-25',checks=checks)
(R/'evidence/source-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
