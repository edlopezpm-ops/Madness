"""(kommiBo) Static publication and download integrity without executing browser code."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import struct
import unittest
import re

ROOT = Path(__file__).resolve().parents[1]


class PageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.context_disabled = False
        self.metadata = {}
        self.canonical = []
        self.brand_link = None
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta':
            key = attrs.get('property', attrs.get('name'))
            if key:
                if key in self.metadata:
                    raise ValueError('Duplicate metadata: ' + key)
                self.metadata[key] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href'))
        if tag == 'a' and attrs.get('class') == 'wordmark':
            self.brand_link = attrs.get('href')
        if tag == 'img':
            self.images.append(attrs.get('src'))
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag in ('a', 'link', 'script'):
            self.links.append(attrs.get('href', attrs.get('src', '')))
        if tag == 'fieldset' and attrs.get('id') == 'context-fields':
            self.context_disabled = 'disabled' in attrs


class PackageTests(unittest.TestCase):
    def test_header_uses_owner_brand_and_links_to_aekr_home(self):
        parser = PageLinks()
        parser.feed((ROOT / 'index.html').read_text())
        self.assertEqual(parser.brand_link, 'https://aekr.io/')
        self.assertIn('aekr-mark.png', parser.images)
        image = (ROOT / 'aekr-mark.png').read_bytes()
        self.assertEqual(image[:8], b'\x89PNG\r\n\x1a\n')
        self.assertEqual(struct.unpack('>II', image[16:24]), (256, 256))

    def test_social_card_is_public_raster_with_matching_metadata(self):
        parser = PageLinks()
        parser.feed((ROOT / 'index.html').read_text())
        public_url = 'https://aekr.io/weekly-leverage/'
        image_url = public_url + 'social-card.png'
        meta = parser.metadata
        self.assertEqual(parser.canonical, [public_url])
        self.assertEqual(meta['og:url'], public_url)
        self.assertEqual(meta['og:image'], image_url)
        self.assertEqual(meta['twitter:image'], image_url)
        self.assertEqual(meta['twitter:card'], 'summary_large_image')
        self.assertEqual(meta['og:image:type'], 'image/png')
        self.assertEqual(meta['og:image:width'], '1200')
        self.assertEqual(meta['og:image:height'], '630')
        self.assertEqual(meta['og:title'], meta['twitter:title'])
        self.assertEqual(meta['og:image:alt'], meta['twitter:image:alt'])
        self.assertIn('Built with AEKR', meta['og:image:alt'])
        for key in ('og:description', 'twitter:description'):
            self.assertTrue(meta[key])
        image = (ROOT / 'social-card.png').read_bytes()
        self.assertEqual(image[:8], b'\x89PNG\r\n\x1a\n')
        self.assertEqual(image[12:16], b'IHDR')
        self.assertEqual(struct.unpack('>II', image[16:24]), (1200, 630))
        self.assertLess(len(image), 5_000_000)

    def test_individual_downloads_match_all_three_language_manifests(self):
        english = json.loads((ROOT / 'prompts.json').read_text())
        english_ui = json.loads((ROOT / 'ui.json').read_text())
        for prefix in ['', 'locales/es/', 'locales/pt/']:
            base = ROOT / prefix
            prompts = json.loads((base / 'prompts.json').read_text())
            ui = json.loads((base / 'ui.json').read_text())
            self.assertEqual(set(ui), set(english_ui))
            self.assertEqual(len(prompts), 6)
            for key, value in ui.items():
                self.assertTrue(value.strip())
                self.assertEqual(re.findall(r'\{\w+\}', key), re.findall(r'\{\w+\}', value), key)
            for original, prompt in zip(english, prompts):
                self.assertEqual(prompt['id'], original['id'])
                self.assertEqual(prompt['file'], original['file'])
                self.assertEqual((base / 'prompts' / prompt['file']).read_text(), prompt['text'])
                self.assertEqual(re.findall(r'\d+', prompt['text']), re.findall(r'\d+', original['text']))

    def test_all_visible_copy_and_accessible_attributes_have_translations(self):
        class Copy(HTMLParser):
            def __init__(self):
                super().__init__(); self.stack = []; self.copy = set()
            def add(self, value):
                value = ' '.join(value.split())
                if any(c.isalpha() for c in value): self.copy.add(value)
            def handle_starttag(self, tag, attrs):
                if tag not in ('meta','link','input','img','br','hr','path','circle','rect'): self.stack.append(tag)
                for key, value in attrs:
                    if key in ('aria-label','placeholder'): self.add(value)
            def handle_endtag(self, tag):
                if tag in self.stack: self.stack = self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
            def handle_data(self, value):
                if not any(tag in self.stack for tag in ('head','script','style','textarea','noscript')): self.add(value)
        parser = Copy(); parser.feed((ROOT / 'index.html').read_text())
        english = json.loads((ROOT / 'ui.json').read_text())
        self.assertEqual(parser.copy - set(english) - {'English','Español','Português','EN','ES','PT','Auto','@__aekr'}, set())

    def test_only_prompt_downloads_and_central_policies_are_exposed_in_footer(self):
        class Links(HTMLParser):
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == 'a':
                    if 'download' in attrs: self.assert_download(attrs['href'])
                    if attrs.get('target') == '_blank':
                        self.assert_relation(attrs.get('rel',''))
        parser = Links()
        parser.assert_download = lambda href: self.assertRegex(href, r'^(locales/(es|pt)/)?prompts/[a-z0-9-]+\.txt$')
        parser.assert_relation = lambda rel: self.assertTrue({'noopener','noreferrer'} <= set(rel.split()))
        source = (ROOT / 'index.html').read_text(); parser.feed(source)
        self.assertNotIn('github.com', source)
        self.assertNotIn('.zip', source)
        for page in ['terms.html','privacy.html','cookies.html']:
            self.assertIn('https://aekr.io/' + page, source)
        self.assertIn('https://x.com/__aekr', source)
        self.assertIn('https://www.instagram.com/__aekr/', source)
        self.assertIn('href="aekr-mark.png" type="image/png"', source)
        self.assertNotIn('No account. No new app.', source)
        self.assertNotIn('Choose a moment. Add a little context.', source)

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

    def test_public_scripts_have_no_collection_cookie_or_external_request_paths(self):
        for filename in ('app.js','planner.mjs','i18n.mjs','theme.js'):
            source = (ROOT / filename).read_text()
            for forbidden in ('document.cookie','sessionStorage','indexedDB','sendBeacon','XMLHttpRequest','innerHTML','eval('):
                self.assertNotIn(forbidden, source)
        source = (ROOT / 'app.js').read_text()
        self.assertEqual(source.count('fetch('), 1)
        self.assertIn('new URL(prefix + file, import.meta.url)', source)
        self.assertIn('["ui.json", "prompts.json"]', source)
        self.assertIn('weekly-leverage-language', source)
        self.assertNotIn('localStorage', (ROOT / 'planner.mjs').read_text())


if __name__ == '__main__':
    unittest.main()
