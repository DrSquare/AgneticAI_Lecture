from pathlib import Path
b=Path('demo-runs/2026-10-17/demo1_competitive_intelligence/build')
p=b/'assemble-research.py'
s=p.read_text(encoding='utf-8').replace("c['primary_url']", "(c.get('primary_url') or c.get('secondary_url') or '')")
p.write_text(s,encoding='utf-8')
p=b/'build-artifacts.mjs'
s=p.read_text(encoding='utf-8').replace("const result=await finalizePresentation(", "process.env.RUNTIME_NODE_MODULES='C:/Users/h_min/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';\nconst result=await finalizePresentation(")
p.write_text(s,encoding='utf-8')
