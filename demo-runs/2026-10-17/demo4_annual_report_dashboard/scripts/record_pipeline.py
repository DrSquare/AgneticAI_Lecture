from pathlib import Path
import json,hashlib,sys,datetime
from zoneinfo import ZoneInfo
R=Path(__file__).resolve().parents[1]
stage=int(sys.argv[1]); now=datetime.datetime.now(ZoneInfo('America/Los_Angeles')).isoformat()
names={1:('stage1_extract',['inputs/10K-NVDA.pdf','inputs/annual-report-pages.json','inputs/q2-release.html','inputs/q3-release.html','inputs/q4-release.html','inputs/filing-index.html','inputs/sources.json'],'financials.md'),2:('stage2_analyze',['financials.md'],'trends.md'),3:('stage3_board',['trends.md'],'exec-summary.md'),4:('stage4_dashboard',['financials.md','trends.md','exec-summary.md'],'dashboard.html')}
agent,inputs,out=names[stage]
def fingerprint(name):
 p=R/name
 return dict(path=name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
f=R/'evidence/pipeline-log.json'
log=json.loads(f.read_text()) if f.exists() else {'demo':4,'execution_date':'2026-10-17','timezone':'America/Los_Angeles','method':'Four sequential independent agents; each spawned with fork_turns=none and explicit input allowlist. Parent reviewed saved output before starting successor. Instruction-only skills are permitted.','gates':[]}
log['gates']=[g for g in log['gates'] if g['stage']!=stage]
log['gates'].append(dict(stage=stage,agent=agent,gate_recorded_at=now,inputs=[fingerprint(n) for n in inputs],output=fingerprint(out),review_note=' '.join(sys.argv[2:])))
f.write_text(json.dumps(log,indent=2),encoding='utf-8')
print('Recorded gate',stage,out)
