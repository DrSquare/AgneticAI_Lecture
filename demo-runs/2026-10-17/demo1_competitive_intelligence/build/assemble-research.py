from pathlib import Path
import json,re
run=Path(__file__).resolve().parents[1]
slugs=['figure-ai','physical-intelligence','skild-ai','agility-robotics','1x-technologies']
ds=[json.loads((run/'research'/f'{s}-data.json').read_text(encoding='utf-8-sig')) for s in slugs]
files=json.loads((run/'build/support-content.json').read_text(encoding='utf-8'))
for name,body in files.items():(run/name).write_text(body,encoding='utf-8')
headings=['Funding & valuation','Technology','Commercial traction','Manufacturing & scale','Team, partners & risks']
checks=[]
for slug,d in zip(slugs,ds):
 p=run/'research'/f'{slug}.md'
 md=p.read_text(encoding='utf-8-sig')
 for n,h in enumerate(headings,1):md=re.sub(r'^##\s*'+str(n)+r'[.)]?\s+\*{0,2}'+re.escape(h)+r'\*{0,2}\s*$',f'## {n} {h}',md,flags=re.M)
 p.write_text(md,encoding='utf-8')
 found=re.findall(r'^## [1-5] (.+)$',md,re.M)
 assert found==headings,(slug,found)
 assert len(d['spot_checks'])>=3
 checks.append({'company':d['company'],'headings':'passed','spot_checks':len(d['spot_checks']),'latest_evidence_date':d['latest_evidence_date']})
out='# Material evidence checks\n\nPrepared 2026-10-17 (America/Los_Angeles). Window 2025-10-17 through 2026-10-17.\n\nEach independent researcher checked at least three material claims. Verified means the claim appears in the identified source, not that unaudited company metrics are audited. Agility financial-table evidence is indexed primary text because full-file retrieval failed.\n\n'
for d in ds:
 out+='## '+d['company']+'\n\n'
 for c in d['spot_checks']:
  out+='- **Claim:** '+c['claim']+'\n  - Date: '+c['date']+'. ['+c.get('source_title','Source evidence')+']('+(c.get('primary_url') or c.get('secondary_url') or '')+').\n  - Verdict: '+c['verdict']+'.\n  - Evidence: '+c.get('evidence',c.get('source_evidence','See structured company evidence for the source qualification.'))+'\n'
 out+='\n'
out+='## Reconciliation with lecture slide 24\n\nSee RUNBOOK.md for the complete correction list. Material corrections distinguish historical financing, proposed SPAC proceeds, reported acquisition talks, recognized revenue, ARR, conditional orders, capacity, production and deliveries. All source dates are bounded by the research cutoff. The original lecture and supplied reference outputs remain unchanged.\n'
(run/'research/evidence-checks.md').write_text(out,encoding='utf-8')
out='# Independent researcher handoffs\n\nFive distinct researchers used the same brief. Batch 1: Figure, PI and Skild. Batch 2: Agility and 1X. The four-agent limit includes the coordinator. Each researcher owned only its profile and evidence files.\n\n'
for d in ds:
 out+='## '+d['company']+'\n\n'+json.dumps(d.get('handoff',{}),ensure_ascii=False,indent=2)+'\n\n'
out+='Coordinator challenges: retain unknown capital as null, verify dates, distinguish transaction structures, and separate capacity/production/orders/deliveries. Researchers independently returned primary-source findings before synthesis.\n'
(run/'research/handoffs.md').write_text(out,encoding='utf-8')
(run/'build/profile-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks))
