from pathlib import Path
import json, re
R=Path(__file__).resolve().parents[1]
t=(R/'financials.md').read_text(encoding='utf-8')
blocks=re.findall(r'```json\s*\n(.*?)\n```',t,re.S)
data=json.loads(blocks[0])
print('JSON type',type(data).__name__)
print('JSON keys',list(data)[:20] if isinstance(data,dict) else 'array')
rows=data if isinstance(data,list) else data.get('metrics',data.get('rows',[]))
print('Rows',len(rows),'first row',rows[0] if rows else '')
v=json.loads((R/'evidence/stage1-validation.json').read_text())
print('Validation top keys',list(v))
for key in ['row_count','counts','checks','reconciliations','validation','summary','issues','missing_disclosures']:
 if key in v: print(key,json.dumps(v[key],ensure_ascii=False)[:9000])
print('Missing rows',json.dumps([x for x in rows if x.get('status')=='not disclosed'],ensure_ascii=False)[:9000])
print('Metadata and caveats',t[t.find('## Extraction caveats'):t.find('```json')][:10000])
