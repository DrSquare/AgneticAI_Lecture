"""Extract only verified, dated facts from the archived peer-refresh sources."""
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'sources'/'peer-refresh'
CUTOFF='2026-10-17'
CIKS={'GOOGL':1652044,'MSFT':789019,'META':1326801,'AMZN':1018724}
data={'as_of':CUTOFF,'consensus_as_of':'2026-10-16','forward_horizon':'CY2027',
      'eps_basis':'S&P Global adjusted non-GAAP consensus, via Stock Analysis',
      'microsoft_calendarization':'0.5 * FY2027 EPS + 0.5 * FY2028 EPS; equal-half earnings assumption, not quarterly consensus',
      'forward':{},'ppe_depreciation':{},'amortization':{},'source_facts':[]}
for ticker in CIKS:
 text=(SRC/f'forecast_{ticker}.txt').read_text(encoding='utf8')
 assert 'Last updated: Oct 16, 2026' in text
 assert 'EPS and Forward PE are based on non-GAAP adjusted numbers.' in text
 current=float(re.search(r'EPS This Year\s+([0-9.]+)',text)[1])
 following=float(re.search(r'EPS Next Year\s+([0-9.]+)',text)[1])
 data['forward'][ticker]={'fy2027_eps':current if ticker=='MSFT' else following,
                         'fy2028_eps':following if ticker=='MSFT' else None,
                         'fy2027_end':'2027-06-30' if ticker=='MSFT' else '2027-12-31',
                         'cy2027_first_fy_weight':0.5 if ticker=='MSFT' else 1,
                         'url':f'https://stockanalysis.com/stocks/{ticker.lower()}/forecast/'}
 facts=json.loads((SRC/f'facts_{ticker}.json').read_text())['facts']['us-gaap']
 def fact(tag,start,end):
  rows=[r for r in facts[tag]['units']['USD'] if r.get('start')==start and r['end']==end and r['filed']<=CUTOFF]
  assert rows,(ticker,tag,start,end)
  item=max(rows,key=lambda r:r['filed'])
  record={'ticker':ticker,'taxonomy':'us-gaap:'+tag,**item,'value_usd_millions':item['val']/1e6,
          'api_url':f'https://data.sec.gov/api/xbrl/companyfacts/CIK{CIKS[ticker]:010d}.json'}
  data['source_facts'].append(record)
  return record['value_usd_millions']
 if ticker=='MSFT':
  data['ppe_depreciation'][ticker]={'direct_ttm':fact('Depreciation','2025-07-01','2026-06-30')}
 else:
  data['ppe_depreciation'][ticker]={'fy2025':fact('Depreciation','2025-01-01','2025-12-31'),
                                  'h1_2025':fact('Depreciation','2025-01-01','2025-06-30'),
                                  'h1_2026':fact('Depreciation','2026-01-01','2026-06-30')}
 if ticker=='GOOGL':
  data['amortization'][ticker]={'h1_2025':fact('AmortizationOfIntangibleAssets','2025-01-01','2025-06-30'),
                               'h1_2026':fact('AmortizationOfIntangibleAssets','2026-01-01','2026-06-30'),
                               'status':'incomplete TTM: excluded from the selected EBITD metric'}
 elif ticker=='MSFT':
  data['amortization'][ticker]={'direct_ttm':fact('AmortizationOfIntangibleAssets','2025-07-01','2026-06-30'),'status':'reported'}
 elif ticker=='META':
  data['amortization'][ticker]={'total_da_fy2025':fact('DepreciationDepletionAndAmortization','2025-01-01','2025-12-31'),
                               'total_da_h1_2025':fact('DepreciationDepletionAndAmortization','2025-01-01','2025-06-30'),
                               'total_da_h1_2026':fact('DepreciationDepletionAndAmortization','2026-01-01','2026-06-30'),
                               'status':'derived: reported total D&A less rounded PP&E depreciation; total EBITDA exact to reported D&A'}
 else:
  data['amortization'][ticker]={'fy2025':fact('AmortizationOfIntangibleAssets','2025-01-01','2025-12-31'),
                               'status':'FY2025 only: excluded from the selected EBITD metric'}
data['selected_peer_metric']='EV/EBITD: user-selected substitute for incomplete TTM EBITDA; EBIT + reported PPE depreciation only'
data['unavailable_exact_ttm_inputs']=[
 'Alphabet FY2025 intangible amortization is not separately supplied in the filing facts; H1 figures alone cannot reconstruct TTM.',
 'Amazon interim intangible amortization is not separately supplied; FY2025 amortization cannot be treated as TTM actuals.',
 'Broad cash-flow addbacks are not interchangeable with PP&E depreciation plus intangible amortization.'
]
(ROOT/'peer-inputs.json').write_text(json.dumps(data,indent=2),encoding='utf8')
print(json.dumps({'forward':data['forward'],'ppe_depreciation':data['ppe_depreciation']},indent=2))
