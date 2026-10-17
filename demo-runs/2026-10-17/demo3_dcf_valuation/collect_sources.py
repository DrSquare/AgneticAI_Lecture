from pathlib import Path
import urllib.request, json, hashlib, re, zipfile
import html
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
SOURCES={
'alphabet_2025_10k':'https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm',
'alphabet_h1_2026_10q':'https://www.sec.gov/Archives/edgar/data/1652044/000165204426000071/goog-20260630.htm',
'alphabet_q2_2026_call':'https://alphabet2025ir.q4web.com/investor/events/event-details/2026/2026-Q2-Earnings-Call-2026-GgTAq7Is0z/default.aspx',
'microsoft_fy2026':'https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast',
'microsoft_2026_10k':'https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm',
'meta_h1_2026':'https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/',
'meta_fy2025':'https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Fourth-Quarter-and-Full-Year-2025-Results/default.aspx',
'amazon_h1_2026':'https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Second-Quarter-Results/default.aspx',
'amazon_fy2025':'https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Fourth-Quarter-Results/default.aspx',
**{f'quote_{t}':f'https://www.google.com/finance/quote/{t}:NASDAQ' for t in ['GOOGL','MSFT','META','AMZN']}}
out=ROOT/'sources';out.mkdir(exist_ok=True)
manifest=[]
for name,url in SOURCES.items():
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (educational valuation research)'})
        with urllib.request.urlopen(req,timeout=25) as r: raw=r.read()
        (out/(name+'.html')).write_bytes(raw)
        content=raw.decode('utf8',errors='replace')
        clean=lambda s: re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',s))).strip()
        txt=clean(content)
        (out/(name+'.txt')).write_text(txt,encoding='utf8')
        manifest.append(dict(id=name,url=url,status='downloaded',retrieved='2026-10-17',sha256=hashlib.sha256(raw).hexdigest()))
        tables=[]
        for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',content,re.S|re.I):
            t=' | '.join(clean(x) for x in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',row,re.S|re.I))
            if re.search('Total revenue|Total net sales|Net income|Operating income|Depreciation|Cash and cash|Short-term investments|Long-term debt|Current portion|Total debt|Common stock|Amortization expense',t,re.I): tables.append(t)
        (out/(name+'-selected-rows.txt')).write_text('\n'.join(tables),encoding='utf8')
        print(name,'OK',len(raw),flush=True)
    except Exception as e:
        manifest.append(dict(id=name,url=url,status='download_failed',error=str(e),verification='This collector does not verify failed downloads. Inspect the source separately before using its values.'))
        print(name,str(e),flush=True)
(out/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
deck=ROOT.parents[2]/'Agentic_AI_Define_Design_Build.pptx'
with zipfile.ZipFile(deck) as z:
    xml=ET.fromstring(z.read('ppt/slides/slide30.xml'))
    text='\n'.join(t.text or '' for t in xml.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'))
    (out/'slide30-text.txt').write_text(text,encoding='utf8')
print('SLIDE30',text)
