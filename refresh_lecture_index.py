"""Build the offline lecture workspace from saved runs (standard library only)."""
from pathlib import Path
from datetime import datetime
import html
import json
import sys
from lecture_launcher.rendering import markdown, walkthrough, reusable_prompt

ROOT = Path(__file__).resolve().parent
RUN_ROOT = ROOT / 'demo-runs' / '2026-10-17'
DEMOS = [
    dict(demo=1, title='Robotics competitive intelligence', short='Robotics research', pattern='Fan-out', slides='20–24', folder='demo1_competitive_intelligence', thread_id='01a14a9b-c4e5-72d1-b020-3a0efab24f47',
         description='One shared brief. Five independent researchers. A comparison you can trace back to its sources.',
         takeaway='Parallel research works when every researcher uses the same questions and evidence rules.',
         primary=['research/summary.md', 'research/competitor-matrix.xlsx', 'IC-pack.pdf'],
         extras=['research/figure-ai.md', 'research/physical-intelligence.md', 'research/skild-ai.md', 'research/agility-robotics.md', 'research/1x-technologies.md', 'research/evidence-checks.md', 'research/handoffs.md'],
         nodes=[['Figure AI', 'research/figure-ai.md'], ['Physical Intelligence', 'research/physical-intelligence.md'], ['Skild AI', 'research/skild-ai.md'], ['Agility Robotics', 'research/agility-robotics.md'], ['1X Technologies', 'research/1x-technologies.md']],
         flow_note='Five researchers, run in two batches. Select a company to read its saved profile.'),
    dict(demo=2, title='Pitch review panel', short='Pitch review', pattern='Panel', slides='25–27', folder='demo2_pitchbook_review', thread_id='01a14a9c-78e1-7c33-bb73-ef435ba9b7d8',
         description='Three reviewers challenge the same pitch. Follow the disagreements all the way to a decision.',
         takeaway='Independent perspectives are useful when disagreements are resolved against shared evidence.',
         primary=['pitch-review.md', 'founder-email.md'],
         extras=['partner-briefing.pdf', 'partner-briefing.md', 'review-narrative.md', 'review-numbers.md', 'review-devils-advocate.md', 'conflicts-log.md', 'calculation-results.md', 'lecture-slide27-corrections.md', 'forward-burn-sensitivity.csv'],
         nodes=[['Narrative', 'review-narrative.md'], ['Numbers', 'review-numbers.md'], ["Devil’s advocate", 'review-devils-advocate.md']],
         flow_note='Fictional company and data. Select a reviewer to read the actual saved review.'),
    dict(demo=3, title='Alphabet valuation model', short='Valuation model', pattern='Single pass + skill', slides='28–30', folder='demo3_dcf_valuation', thread_id='01a14aab-bc68-7a90-96d3-b876141cbd11',
         description='A reusable valuation skill becomes a working model. Change an assumption and inspect what moves.',
         takeaway='A reusable skill needs explicit inputs, formula checks and a clear boundary around missing evidence.',
         primary=['GOOGL_DCF_Valuation.xlsx', 'valuation-notes.md'],
         extras=['validation-report.md', 'validation-report.json', 'lecture-slide30-corrections.md', 'input-provenance.json'],
         nodes=[['Sourced inputs', 'input-provenance.json'], ['Live workbook', 'GOOGL_DCF_Valuation.xlsx'], ['Validation', 'validation-report.md']],
         flow_note='Open the workbook in Excel for live recalculation. Compare DCF, forward P/E and EV/EBITD with their stated assumptions.'),
    dict(demo=4, title='NVIDIA annual report dashboard', short='Report to dashboard', pattern='Pipeline', slides='31–35', folder='demo4_annual_report_dashboard', thread_id='01a14abb-11b4-7872-a117-2c57fea568f8',
         description='An annual report becomes evidence, analysis, a Board brief and an interactive dashboard.',
         takeaway='Sequential handoffs make each stage inspectable before the next stage starts.',
         primary=['dashboard.html', 'financials.md', 'trends.md', 'exec-summary.md', 'inputs/10K-NVDA.pdf'],
         extras=['exec-summary.pdf', 'inputs/sources.json'],
         nodes=[['Extract', 'financials.md'], ['Analyze', 'trends.md'], ['Summarize', 'exec-summary.md'], ['Build', 'dashboard.html']],
         flow_note='Historical FY2026 report. Select a stage to inspect its saved handoff.'),
]
LABELS = {'RUNBOOK.md': 'Presenter runbook', 'readiness.json': 'Readiness report', 'research/summary.md': 'Research synthesis', 'research/competitor-matrix.xlsx': 'Competitor matrix', 'IC-pack.pdf': 'Investment committee slides', 'pitch-review.md': 'Consolidated pitch review', 'founder-email.md': 'Founder email draft (unsent)', 'partner-briefing.pdf': 'Partner briefing', 'GOOGL_DCF_Valuation.xlsx': 'Alphabet DCF workbook', 'valuation-notes.md': 'Valuation notes', 'dashboard.html': 'Interactive NVIDIA dashboard', 'financials.md': 'Extracted financial evidence', 'trends.md': 'Trend analysis', 'exec-summary.md': 'Board summary', 'exec-summary.pdf': 'Board summary PDF', 'inputs/10K-NVDA.pdf': 'NVIDIA annual report', 'input-provenance.json': 'Input provenance', 'prompt.md': 'Original demo prompt'}
ALLOWED = {'.md', '.json', '.pdf', '.xlsx', '.html', '.csv', '.png'}


def text_value(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and 'replacement' in value:
        return f"Slide {value.get('slide', '')}: {value['replacement']} (Replaces: {value.get('existing', '')})"
    return json.dumps(value, ensure_ascii=False)


def inspect_demo(config):
    run = RUN_ROOT / config['folder']
    result = dict(config, status='unverified', limitations=[], slide_corrections=[], checks=[], sources_as_of=None, available=[], missing=[])
    manifest = run / 'readiness.json'
    if manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding='utf-8-sig'))
            if not isinstance(data, dict):
                raise ValueError('Expected a JSON object')
            result['status'] = data.get('status', 'unverified')
            if result['status'] not in ('ready', 'partial', 'blocked', 'running', 'unverified'):
                result['status'] = 'partial'
                result['limitations'].append('Readiness report contains an unknown status.')
            for field in ('limitations', 'slide_corrections', 'checks'):
                values = data.get(field, [])
                if not isinstance(values, list):
                    raise ValueError(field + ' must be a list')
                result[field].extend(values if field == 'checks' else [text_value(v) for v in values])
            result['sources_as_of'] = data.get('sources_as_of')
        except (ValueError, OSError) as exc:
            result['status'] = 'partial'
            result['limitations'].append('Could not read readiness report: ' + str(exc))
    else:
        result['limitations'].append('No final readiness report is saved. Available outputs can be explored; final acceptance is not confirmed.')
    required = ['RUNBOOK.md'] + config['primary']
    for relative in dict.fromkeys(required + config['extras'] + ['readiness.json']):
        path = (run / relative).resolve()
        if not path.is_relative_to(ROOT.resolve()) or path.suffix.lower() not in ALLOWED:
            continue
        if path.is_file() and path.stat().st_size:
            result['available'].append({'name': relative, 'label': LABELS.get(relative, Path(relative).stem.replace('-', ' ').replace('_', ' ').capitalize()), 'path': path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size, 'type': path.suffix[1:].upper(), 'primary': relative in config['primary']})
        elif relative in required:
            result['missing'].append(relative)
    if result['status'] == 'ready' and result['missing']:
        result['status'] = 'partial'
        result['limitations'].append('Missing expected artifacts: ' + ', '.join(result['missing']))
    if result['status'] == 'ready' and any(isinstance(c, dict) and str(c.get('status', '')).lower() in ('fail', 'failed', 'error') for c in result['checks']):
        result['status'] = 'partial'
        result['limitations'].append('At least one recorded validation check failed.')
    runbook = run / 'RUNBOOK.md'
    text = runbook.read_text(encoding='utf-8-sig') if runbook.is_file() else ''
    result['steps'] = walkthrough(text, runbook, ROOT)
    for step in result['steps']:
        # The saved runbook can refer to editable local sources. The launcher
        # presents their published PDF equivalent when that file exists.
        for artifact in result['available']:
            if artifact['type'] == 'PDF':
                original = str(Path(artifact['name']).with_suffix('.pptx')).replace('\\', '/')
                for field in ('action', 'label'):
                    step[field] = step[field].replace(original, artifact['name'])
        step['artifacts'] = [a['name'] for a in result['available'] if a['name'] in step['label'] or Path(a['name']).name in step['label']]
    result['prompt'] = reusable_prompt(text)
    prompt = ROOT / 'Agentic_AI_Demos' / config['folder'] / 'prompt.md'
    if prompt.is_file():
        result['available'].append({'name': 'prompt.md', 'label': LABELS['prompt.md'], 'path': prompt.relative_to(ROOT).as_posix(), 'bytes': prompt.stat().st_size, 'type': 'MD', 'primary': False})
    return result


def build():
    results = [inspect_demo(d) for d in DEMOS]
    summary = [{'demo': d['demo'], 'status': d['status'], 'missing': d['missing']} for d in results]
    if '--check' in sys.argv:
        print(json.dumps({'demos': summary}, indent=2))
        return 0 if all(d['status'] == 'ready' for d in results) else 2
    snapshot = datetime.now().astimezone().isoformat(timespec='seconds')
    payload = {'run_date': '2026-10-17', 'snapshot_timestamp': snapshot, 'project': 'Agentic AI Lecture', 'demos': results}
    documents = {}
    artifacts = [a for d in results for a in d['available']] + [{'path': 'Agentic_AI_Demos/README.md'}]
    for artifact in artifacts:
        path = ROOT / artifact['path']
        if path.suffix.lower() in ('.md', '.json') and path.stat().st_size <= 500_000:
            text = path.read_text(encoding='utf-8-sig')
            documents[artifact['path']] = {'text': text, 'html': markdown(text, path, ROOT) if path.suffix == '.md' else '<pre><code>' + html.escape(text) + '</code></pre>'}
    payload['documents'] = documents
    notes = ['# Lecture presenter notes', '', 'Run date: 17 October 2026. Allow about five minutes per demo. Readiness comes from saved reports and a required-file check.', '']
    fallback = ['<h1>Agentic AI lecture demos</h1><p>Enable JavaScript for the interactive workspace, or open these saved files directly.</p>']
    for d in results:
        notes.extend([f"## Demo {d['demo']} — {d['title']}", '', f"Status: **{d['status']}**. Pattern: {d['pattern']}. Source slides: {d['slides']}.", ''])
        fallback.append(f"<section><h2>{html.escape(d['title'])}</h2><p>Status: {html.escape(d['status'])}</p><ul>")
        for a in d['available']:
            fallback.append('<li><a href="' + html.escape(a['path'], quote=True) + '">' + html.escape(a['label']) + '</a></li>')
            if a['name'] != 'prompt.md':
                notes.append('- [' + a['label'] + '](' + d['folder'] + '/' + a['name'] + ')')
        fallback.append('</ul></section>')
        notes.extend(['', '### Limitations', ''] + (['- ' + v for v in d['limitations']] or ['None recorded.']) + ['', '### Slide corrections', ''] + (['- ' + v for v in d['slide_corrections']] or ['None recorded.']) + [''])
    embedded = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    template = (ROOT / 'lecture_launcher' / 'template.html').read_text(encoding='utf-8')
    (ROOT / 'LECTURE_DEMOS.html').write_text(template.replace('__FALLBACK__', '\n'.join(fallback)).replace('__PAYLOAD__', embedded), encoding='utf-8')
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    (RUN_ROOT / 'lecture-index.json').write_text(json.dumps({k: v for k, v in payload.items() if k != 'documents'}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (RUN_ROOT / 'presenter-notes.md').write_text('\n'.join(notes) + '\n', encoding='utf-8')
    print(json.dumps({'launcher': str(ROOT / 'LECTURE_DEMOS.html'), 'embedded_documents': len(documents), 'demos': summary}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(build())
