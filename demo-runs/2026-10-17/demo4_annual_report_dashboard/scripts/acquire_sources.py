from pathlib import Path
from urllib.request import Request,urlopen
from hashlib import sha256
import json,datetime
from pypdf import PdfReader
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
sources=[('annual_report','10K-NVDA.pdf','https://s201.q4cdn.com/141608511/files/doc_financials/2026/ar/2026-Annual-Report-Web.pdf'),('q4_release','q4-release.html','https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2026/default.aspx'),('q3_release','q3-release.html','https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Financial-Results-for-Third-Quarter-Fiscal-2026/default.aspx'),('q2_release','q2-release.html','https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2026/default.aspx'),('filing_index','filing-index.html','https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/0001045810-26-000021-index.htm')]
manifest=[]
for sid,name,url in sources:
 p=R/'inputs'/name
 try:
  if not p.exists():
   req=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; academic lecture verification)'})
   with urlopen(req,timeout=90) as response: p.write_bytes(response.read())
  data=p.read_bytes()
  manifest.append(dict(id=sid,file='inputs/'+name,url=url,sha256=sha256(data).hexdigest(),retrieved_on='2026-10-17',bytes=len(data)))
  if name.endswith('.html'):
   soup=BeautifulSoup(data,'html.parser')
   for t in soup(['script','style']): t.decompose()
   (p.with_suffix('.txt')).write_text(soup.get_text('\n',strip=True),encoding='utf-8')
  print(name,len(data),flush=True)
 except Exception as e:
  manifest.append(dict(id=sid,url=url,error=str(e)))
  print(name,repr(e),flush=True)
(R/'inputs'/'sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
reader=PdfReader(R/'inputs'/'10K-NVDA.pdf')
pages=[{'pdf_page':i+1,'pdf_index':i,'text':p.extract_text()} for i,p in enumerate(reader.pages)]
(R/'inputs'/'annual-report-pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'inputs'/'annual-report.txt').write_text('\n\n'.join('=== PDF page '+str(p['pdf_page'])+' (index '+str(p['pdf_index'])+') ===\n'+p['text'] for p in pages),encoding='utf-8')
print('PDF pages',len(pages))
print([(p['pdf_page'],p['text'][:100]) for p in pages if 'CONSOLIDATED STATEMENTS OF INCOME' in p['text'] or 'FORM 10-K' in p['text'][:300]])
