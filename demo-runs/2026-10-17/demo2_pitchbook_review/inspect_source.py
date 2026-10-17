from pathlib import Path
import hashlib,json,subprocess,shutil
from pypdf import PdfReader
from PIL import Image,ImageOps,ImageDraw
H=Path(__file__).resolve().parent
R=H.parents[2]
source=R/'Agentic_AI_Demos/demo2_pitchbook_review/inputs/pitch-deck.pdf'
E=H/'evidence';E.mkdir(exist_ok=True)
r=PdfReader(source)
pages=[{'page':i+1,'text':p.extract_text()} for i,p in enumerate(r.pages)]
(E/'deck-pages.json').write_text(json.dumps(pages,indent=2),encoding='utf-8')
(E/'deck-text.txt').write_text('\n\n'.join(f"PAGE {p['page']}\n{p['text']}" for p in pages),encoding='utf-8')
subprocess.run([shutil.which('pdftoppm'),'-png','-scale-to','1400',str(source),str(E/'deck')],check=True)
paths=sorted(E.glob('deck-*.png'))
thumbs=[]
for p in paths:
    im=Image.open(p).convert('RGB'); im.thumbnail((700,400))
    cell=Image.new('RGB',(720,435),'#e9edf0');cell.paste(im,((720-im.width)//2,25)); ImageDraw.Draw(cell).text((12,8),p.stem,fill='black');thumbs.append(cell)
contact=Image.new('RGB',(2160,435*4),'white')
for i,im in enumerate(thumbs):contact.paste(im,((i%3)*720,(i//3)*435))
contact.save(E/'deck-contact-sheet.png')
files=[source,R/'Agentic_AI_Demos/demo2_pitchbook_review/inputs/data-room/kpi-monthly.csv',R/'Agentic_AI_Demos/demo2_pitchbook_review/outputs/pitch-review.md']
(E/'source-manifest.json').write_text(json.dumps({'fictional_teaching_material':True,'data_as_of':'2026-09-30','pdf_page_count':len(r.pages),'rendered_page_count':len(paths),'hashes':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2),encoding='utf-8')
print(f'Extracted and rendered {len(pages)} pages; saved contact sheet and source hashes.')
