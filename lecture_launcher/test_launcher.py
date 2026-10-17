"""Regression tests for readiness, note safety and the generated artifact links."""
import copy
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

import refresh_lecture_index as launcher
from lecture_launcher.rendering import markdown, link_target, walkthrough, reusable_prompt


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.extend(value for key, value in attrs if key == 'href')


class LauncherTests(unittest.TestCase):
    def test_required_audience_files_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            run_root = root / 'runs'
            config = copy.deepcopy(launcher.DEMOS[0])
            run = run_root / config['folder']
            run.mkdir(parents=True)
            (root / 'lecture_launcher').mkdir()
            (root / 'lecture_launcher/audience.json').write_text('{"1":{"sources":[]}}')
            with patch.object(launcher, 'ROOT', root), patch.object(launcher, 'RUN_ROOT', run_root):
                self.assertIn('IC-pack.pdf', launcher.inspect_demo(config)['missing'])
                for item in ['GUIDE.md'] + config['primary']:
                    p = run / item; p.parent.mkdir(parents=True, exist_ok=True); p.write_text('saved')
                self.assertEqual(launcher.inspect_demo(config)['missing'], [])
                (run/'readiness.json').write_text('{"status":"ready","private_note":"internal"}')
                self.assertNotIn('private_note', str(launcher.inspect_demo(config)))

    def test_preparation_records_cannot_be_published(self):
        from lecture_launcher.public_policy import is_public_path
        for path in ['RUNBOOK.md', 'readiness.json', 'REVIEW.md', 'lecture-slide30-corrections.md', 'x/evidence/log.json', 'x/build/check.txt', '.git/config', 'slides.pptx']:
            self.assertFalse(is_public_path(path), path)
        for path in ['GUIDE.md', 'review-numbers.md', 'financials.md', 'inputs/sources.json']:
            self.assertTrue(is_public_path(path), path)
        page = (launcher.ROOT/'LECTURE_DEMOS.html').read_text('utf8')
        data = json.loads(re.search(r'<script type="application/json" id="lecture-data">(.*?)</script>', page, re.S)[1])
        for demo in data['demos']:
            self.assertFalse(set(demo) & {'checks','slide_corrections','thread_id','limitations','status'})
            for artifact in demo['available']:
                self.assertTrue(is_public_path(artifact['path']), artifact['path'])
        for path,doc in data['documents'].items():
            self.assertTrue(is_public_path(path), path)
            self.assertNotRegex(doc['text'], r'(?i)presenter|readiness|genuine reviewer exchange|genuine reviewer challenge|checks performed|actual reviewer exchanges')

    def test_note_renderer_escapes_and_restricts_links(self):
        root = launcher.ROOT
        source = root / 'README.md'
        output = markdown('<script>alert(1)</script>\n\n[bad](javascript:alert)\n\n[good](https://example.com)\n\n| A | B |\n|---|---|\n| **bold** | `code` |', source, root)
        self.assertNotIn('<script>', output)
        self.assertNotIn('href="javascript:', output)
        self.assertIn('<table>', output)
        self.assertIn('<strong>bold</strong>', output)
        self.assertIn('<code>code</code>', output)
        self.assertIsNone(link_target('../../outside.txt', source, root))
        self.assertIsNone(link_target('file:///C:/private.txt', source, root))
        self.assertIsNone(link_target('//evil.example/x', source, root))
        self.assertIsNone(link_target('missing.pdf', source, root))

    def test_walkthrough_and_prompt_are_from_audience_guides(self):
        for config in launcher.DEMOS:
            path = launcher.RUN_ROOT / config['folder'] / 'GUIDE.md'
            text = path.read_text(encoding='utf-8-sig')
            steps = walkthrough(text, path, launcher.ROOT)
            self.assertGreaterEqual(len(steps), 5)
            self.assertLessEqual(len(steps), 8)
            self.assertIn('0:00', steps[0]['time'])
            self.assertTrue(all('](' not in s['label'] for s in steps))
            self.assertIn('5:00', steps[-1]['time'])
            prompt = reusable_prompt(text)
            if prompt:
                self.assertGreater(len(prompt), 200)
            else:
                self.assertTrue((launcher.ROOT/'Agentic_AI_Demos'/config['folder']/'prompt.md').is_file())
        self.assertEqual(walkthrough('No timed steps', launcher.ROOT/'README.md', launcher.ROOT), [])

    def test_generated_links_exist_and_no_powerpoint_is_linked(self):
        page = (launcher.ROOT/'LECTURE_DEMOS.html').read_text(encoding='utf8')
        embedded = re.search(r'<script type="application/json" id="lecture-data">(.*?)</script>', page, re.S)[1]
        data = json.loads(embedded)
        self.assertNotIn('</script', embedded.lower())
        parser = Links(); parser.feed(page)
        for doc in data['documents'].values():
            parser.feed(doc['html'])
        for demo in data['demos']:
            for artifact in demo['available']:
                self.assertTrue((launcher.ROOT/artifact['path']).is_file(), artifact['path'])
                self.assertNotEqual(Path(artifact['path']).suffix.lower(), '.pptx')
        for href in parser.links:
            url = urlsplit(href)
            if url.scheme or not url.path:
                continue
            path = launcher.ROOT / unquote(url.path)
            self.assertTrue(path.is_file(), href)
            self.assertNotEqual(path.suffix.lower(), '.pptx', href)



if __name__ == '__main__':
    unittest.main()
