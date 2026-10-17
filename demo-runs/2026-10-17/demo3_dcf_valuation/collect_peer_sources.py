from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request, json, hashlib, re, html
ROOT=Path(__file__).resolve().parent/'sources'/'peer-refresh'
ROOT.mkdir(parents=True,exist_ok=True)
SOURCES={**{f'forecast_{t}':f'https://stockanalysis.com/stocks/{t.lower()}/forecast/' for t in ['GOOGL','MSFT','META','AMZN']},
 **{f'facts_{t}':f'https://data.sec.gov/api/xbrl/companyfacts/CIK{c:010d}.json' for t,c in [('GOOGL',1652044),('MSFT',789019),('META',1326801),('AMZN',1018724)]}}
def fetch(item):
 name,url=item
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (educational valuation research)'}),timeout=25) as r: raw=r.read()
  ext='.json' if url.endswith('.json') else '.html'
  (ROOT/(name+ext)).write_bytes(raw)
  if ext=='.html':
   (ROOT/(name+'.txt')).write_text(re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',raw.decode('utf8',errors='replace')))),encoding='utf8')
  return dict(id=name,url=url,status='downloaded',sha256=hashlib.sha256(raw).hexdigest())
 except Exception as e: return dict(id=name,url=url,status='download_failed',error=str(e))
results=list(ThreadPoolExecutor(max_workers=4).map(fetch,SOURCES.items()))
(ROOT/'manifest.json').write_text(json.dumps(results,indent=2),encoding='utf8')
for r in results: print(r['id'],r['status'],r.get('error',''))
for path in ROOT.glob('facts_*.json'):
 data=json.loads(path.read_text(encoding='utf8'));facts=data.get('facts',{}).get('us-gaap',{})
 for name in ['AmortizationOfIntangibleAssets','Depreciation','DepreciationDepletionAndAmortization','FinanceLeaseLiabilityCurrent','FinanceLeaseLiabilityNoncurrent']:
  if name not in facts: continue
  vals=[x for x in facts[name]['units'].get('USD',[]) if x.get('end','')>='2025-01-01' and x.get('filed','')<='2026-10-17']
  print(path.stem,name,json.dumps(vals[-16:]))
