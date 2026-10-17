from pathlib import Path
import zipfile, xml.etree.ElementTree as E
root=Path(__file__).resolve().parents[4]
src=root/'Agentic_AI_Define_Design_Build.pptx'
out=Path(__file__).parent/'reference-subset.pptx'
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with zipfile.ZipFile(src) as z, zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as w:
    tree=E.fromstring(z.read('ppt/presentation.xml'))
    ids=tree.find('p:sldIdLst',ns)
    keep=list(ids)[23]
    for el in list(ids):
        if el is not keep: ids.remove(el)
    for name in z.namelist():
        w.writestr(name,E.tostring(tree,encoding='utf-8',xml_declaration=True) if name=='ppt/presentation.xml' else z.read(name))
print(out)
