"""Publication boundary for lecture materials."""
from pathlib import PurePosixPath
import re

INTERNAL_NAMES = {'runbook.md', 'readiness.json', 'presenter-notes.md', 'review.md', 'handoffs.md', 'conflicts-log.md', 'design.md', 'design-plan.md'}
INTERNAL_PARTS = {'evidence', 'build', 'previews', '.git', '__pycache__'}

def is_public_path(path):
    p = PurePosixPath(str(path).replace('\\', '/'))
    return not (any(part.lower() in INTERNAL_PARTS or part.startswith('.') for part in p.parts)
                or p.name.lower() in INTERNAL_NAMES
                or re.search(r'correction|validation|visual-review|visual-qa|readiness', p.name, re.I)
                or p.suffix.lower() in {'.pptx', '.zip', '.ndjson'})


def validate_public_data(data):
    """Fail the build if preparation prose enters the embedded public documents."""
    import json
    text = json.dumps(data, ensure_ascii=False)
    pattern = r"(?i)RUNBOOK\.md|readiness\.json|presenter notes|presenter runbook|lecture readiness|genuine reviewer exchange|genuine reviewer challenge|actual reviewer exchanges|researcher handoff|research handoff|slide.corrections"
    match = re.search(pattern, text)
    if match:
        raise ValueError('Preparation content in public payload: ' + match.group())
    for doc in data['documents']:
        if not is_public_path(doc):
            raise ValueError('Internal document in public payload: ' + doc)


def validate_public_file(path):
    if path.suffix.lower() == '.xlsx':
        from zipfile import ZipFile
        with ZipFile(path) as archive:
            for name in archive.namelist():
                if name.endswith('.xml') and ('sharedStrings' in name or 'comments' in name):
                    text = archive.read(name).decode('utf-8')
                    if re.search(r'(?i)presenter|readiness|visual.review|reviewer.exchange', text):
                        raise ValueError('Preparation text in workbook: ' + str(path))
