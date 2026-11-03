"""(kommiBo) Static publication and download integrity without executing browser code."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.context_disabled = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag in ('a', 'link', 'script'):
            self.links.append(attrs.get('href', attrs.get('src', '')))
        if tag == 'fieldset' and attrs.get('id') == 'context-fields':
            self.context_disabled = 'disabled' in attrs


class PackageTests(unittest.TestCase):
    def test_individual_downloads_json_and_zip_match_exactly(self):
        prompts = json.loads((ROOT / 'prompts.json').read_text())
        self.assertEqual(len(prompts), 6)
        with zipfile.ZipFile(ROOT / 'weekly-leverage-prompts.zip') as pack:
            self.assertEqual(len(pack.namelist()), 7)
            self.assertEqual(pack.read('weekly-leverage/START-HERE.txt'), (ROOT / 'USE-NOTES.txt').read_bytes())
            for prompt in prompts:
                content = (ROOT / 'prompts' / prompt['file']).read_bytes()
                self.assertEqual(content.decode('utf-8'), prompt['text'])
                self.assertEqual(content, pack.read('weekly-leverage/' + prompt['file']))

    def test_local_page_links_and_anchors_resolve(self):
        parser = PageLinks()
        parser.feed((ROOT / 'index.html').read_text())
        for link in parser.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            if url.path:
                target = (ROOT / unquote(url.path)).resolve()
                self.assertTrue(target.is_relative_to(ROOT), link)
                self.assertTrue(target.is_file(), link)
            elif url.fragment:
                self.assertIn(url.fragment, parser.ids)

    def test_context_cannot_submit_when_javascript_is_unavailable(self):
        parser = PageLinks()
        parser.feed((ROOT / 'index.html').read_text())
        self.assertTrue(parser.context_disabled)

    def test_published_scripts_have_no_persistent_storage_or_external_request_endpoints(self):
        for filename in ('app.js', 'planner.mjs'):
            source = (ROOT / filename).read_text()
            for forbidden in ('localStorage', 'sessionStorage', 'indexedDB', 'sendBeacon', 'XMLHttpRequest'):
                self.assertNotIn(forbidden, source)
        source = (ROOT / 'app.js').read_text()
        self.assertEqual(source.count('fetch('), 1)
        self.assertRegex(source, r'''new URL\(["']\./prompts\.json["'],\s*import\.meta\.url\)''')


if __name__ == '__main__':
    unittest.main()
