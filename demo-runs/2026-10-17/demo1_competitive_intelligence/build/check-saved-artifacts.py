from pathlib import Path
import json,zipfile,xml.etree.ElementTree as E,hashlib
r=Path('demo-runs/2026-10-17/demo1_competitive_intelligence')
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(r/'research/competitor-matrix.xlsx') as z:
 root=E.fromstring(z.read('xl/worksheets/sheet1.xml'))
 fs=[{'cell':c.get('r'),'formula':c.find('s:f',ns).text,'cached_value':(c.find('s:v',ns).text if c.find('s:v',ns) is not None else None)} for c in root.findall('.//s:c',ns) if c.find('s:f',ns) is not None]
 assert len(fs)==10,len(fs)
 vals={c['cell']:c['cached_value'] for c in fs}
 assert [vals['H'+str(n)] for n in range(6,11)]==['17','4','18','2','52'],vals
 for n in range(6,11):assert vals['E'+str(n)]=='Not comparable'
 for c in root.findall('.//s:c',ns):
  if c.get('r') in ['B6','B7','B8','B9','B10','I7','I8','I9','I10']:assert c.get('t') not in ['s','str','inlineStr']
 report={'formula_count':len(fs),'formulas':fs,'numeric_input_storage':'passed','excel_ui_recalculation':'not performed','package_crc_check':z.testzip()}
(r/'build/saved-xlsx-checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
extra=[
{'company':'Figure AI','date':'2026-04-29','url':'https://www.figure.ai/news/ramping-figure-03-production','finding':'Coordinator opened primary release and confirmed >350 production/output with internal allocations, not verified paid customer deliveries.'},
{'company':'Physical Intelligence','date':'2026-10-13','url':'https://www.pi.website/blog/api-beta','finding':'Coordinator confirmed dated API beta and named collaborators, with network connectivity caveat.'},
{'company':'Skild AI','date':'2026-01-14','url':'https://skild.ai/blogs/series-c','finding':'Coordinator confirmed $1.4B round, >$14B valuation, and January revenue wording that must not become ARR.'}]
(r/'build/coordinator-source-checks.json').write_text(json.dumps(extra,indent=2),encoding='utf-8')
print(json.dumps(report))
print('Deck exists:',(r/'IC-pack.pptx').exists())
print('Final render count:',len(list((r/'build').glob('slide-*.png'))))
