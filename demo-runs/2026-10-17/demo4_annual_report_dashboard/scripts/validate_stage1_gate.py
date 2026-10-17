from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1]
t=(R/'financials.md').read_text(encoding='utf-8')
rows=json.loads(re.search(r'```json\s*\n(.*?)\n```',t,re.S).group(1))
v=json.loads((R/'evidence/stage1-validation.json').read_text())
checks=[]
def check(name,passed,evidence):
 checks.append(dict(name=name,status='pass' if passed else 'fail',evidence=evidence))
check('Unique metric IDs',len({r['id'] for r in rows})==len(rows),len(rows))
check('Missing values stay null',all(r['value'] is None for r in rows if r['status']=='not disclosed'),'No missing disclosure is represented by zero')
check('Reported/calc values numeric',all(isinstance(r['value'],(int,float)) for r in rows if r['status']!='not disclosed'),'Numeric schema')
check('Every row resolves to source map',all(s.strip() in v['source_map'] for r in rows for s in r['source'].split(';')),'Exact PDF pages or earnings-release headings')
check('Every calculated row has formula',all(r['formula'] for r in rows if r['status']=='calc'),'Formula inputs preserved')
check('Stage1 reconciliation results',all(c['passed'] for c in v['checks']),len(v['checks']))
lookup={r['id']:r for r in rows}
check('Rendered revenue agrees',lookup['revenue_fy26']['value']==215938,'evidence/source-pdf-139.png; printed51')
check('No source-copy reference output',v['source_scope'].startswith('Approved official'),'Agent provenance statement; original source hash recorded')
out=dict(stage=1,metric_count=len(rows),checks=checks,passed=all(c['status']=='pass' for c in checks),financials_sha256=hashlib.sha256((R/'financials.md').read_bytes()).hexdigest())
(R/'evidence/parent-stage1-gate.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
assert out['passed']
