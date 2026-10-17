from pathlib import Path
import json,subprocess
from pypdf import PdfReader

R=Path(__file__).resolve().parents[1]
pdf=R/'evidence/dashboard-print.pdf'
renderer=Path('C:/Users/h_min/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
count=len(PdfReader(pdf).pages)
subprocess.run([str(renderer),'-scale-to','1500','-png',str(pdf),str(R/'evidence/dashboard-print-page')],check=True)
pages=sorted((R/'evidence').glob('dashboard-print-page-*.png'))
assert len(pages)==count,(len(pages),count)
result={'pdf':'evidence/dashboard-print.pdf','pages':count,'rendered_pages':[p.relative_to(R).as_posix() for p in pages],'renderer':str(renderer),'scale_to':1500,'visual_review_pending':True}
(R/'evidence/dashboard-print-render.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
