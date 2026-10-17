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
    def test_readiness_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            run_root = root / 'runs'
            config = copy.deepcopy(launcher.DEMOS[0])
            run = run_root / config['folder']
            run.mkdir(parents=True)
            with patch.object(launcher, 'ROOT', root), patch.object(launcher, 'RUN_ROOT', run_root):
                self.assertEqual(launcher.inspect_demo(config)['status'], 'unverified')
                (run / 'readiness.json').write_text('{broken', encoding='utf8')
                self.assertEqual(launcher.inspect_demo(config)['status'], 'partial')
                (run / 'readiness.json').write_text(json.dumps({'status':'ready'}))
                result = launcher.inspect_demo(config)
                self.assertEqual(result['status'], 'partial')
                self.assertIn('IC-pack.pdf', result['missing'])
                for item in ['RUNBOOK.md'] + config['primary']:
                    p = run / item; p.parent.mkdir(parents=True, exist_ok=True); p.write_text('saved')
                self.assertEqual(launcher.inspect_demo(config)['status'], 'ready')
                (run / 'readiness.json').write_text(json.dumps({'status':'ready','checks':[{'status':'failed'}]}))
                self.assertEqual(launcher.inspect_demo(config)['status'], 'partial')
                (run / 'readiness.json').write_text(json.dumps({'status':'ready','limitations':None}))
                self.assertEqual(launcher.inspect_demo(config)['status'], 'partial')

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

    def test_walkthrough_and_prompt_are_from_saved_runbooks(self):
        for config in launcher.DEMOS:
            path = launcher.RUN_ROOT / config['folder'] / 'RUNBOOK.md'
            text = path.read_text(encoding='utf-8-sig')
            steps = walkthrough(text, path, launcher.ROOT)
            self.assertGreaterEqual(len(steps), 5)
            self.assertLessEqual(len(steps), 8)
            self.assertIn('0:00', steps[0]['time'])
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
        corrections = data['demos'][2]['slide_corrections']
        self.assertTrue(all(isinstance(item, str) for item in corrections))
        self.assertTrue(any('Slide 30' in item for item in corrections))


if __name__ == '__main__':
    unittest.main()
