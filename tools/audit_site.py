#!/usr/bin/env python3
"""Dependency-free quality audit for the generated Big Bud Man publication."""
from __future__ import annotations
from html.parser import HTMLParser
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit
from datetime import datetime
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = (Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "_site").resolve()


class Inspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.h1 = 0
        self.description = ""
        self.canonical = ""
        self.links: list[str] = []
        self.anchors: list[str] = []
        self.ids: list[str] = []
        self.images: list[tuple[str, str | None]] = []
        self.image_attrs: list[dict[str, str | None]] = []
        self.forms: list[str] = []
        self.meta: list[dict[str, str | None]] = []
        self.jsonld: list[str] = []
        self._jsonld_buffer: list[str] | None = None
    def handle_starttag(self, tag: str, attrs) -> None:
        a = dict(attrs)
        if tag == "title": self._in_title = True
        elif tag == "h1": self.h1 += 1
        elif tag == "meta" and a.get("name") == "description": self.description = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href", "")
        if tag == "meta": self.meta.append(a)
        if tag == "script" and a.get("type") == "application/ld+json": self._jsonld_buffer = []
        if tag in {"a", "link"} and a.get("href"): self.links.append(a["href"])
        elif tag in {"script", "img", "source"} and a.get("src"): self.links.append(a["src"])
        if tag == "img":
            self.images.append((a.get("src", ""), a.get("alt")))
            self.image_attrs.append(a)
        if tag == "form": self.forms.append(a.get("action", ""))
        if tag == "a" and a.get("href"): self.anchors.append(a["href"])
        if a.get("id"): self.ids.append(a["id"])
    def handle_endtag(self, tag: str) -> None:
        if tag == "title": self._in_title = False
        if tag == "script" and self._jsonld_buffer is not None:
            self.jsonld.append("".join(self._jsonld_buffer))
            self._jsonld_buffer = None
    def handle_data(self, data: str) -> None:
        if self._in_title: self.title += data
        if self._jsonld_buffer is not None: self._jsonld_buffer.append(data)


def resolve_local(page: Path, target: str) -> Path | None:
    parts = urlsplit(target)
    if parts.scheme or target.startswith(("//", "mailto:", "tel:", "javascript:", "#", "data:")):
        return None
    clean = parts.path
    if not clean: return None
    resolved = ROOT / clean.lstrip("/") if clean.startswith("/") else (page.parent / clean).resolve()
    if clean.endswith("/") or resolved.is_dir(): resolved = resolved / "index.html"
    return resolved


def main() -> int:
    failures: list[str] = []
    html_files = sorted(ROOT.rglob("*.html"))
    if len(html_files) < 270: failures.append(f"Publication regressed below the 270-page baseline; found {len(html_files)}")
    try:
        batch = json.loads((ROOT / "publication-manifest.json").read_text())
        batch_date = datetime.strptime(batch.get("publication_date", ""), "%Y-%m-%d")
        batch_paths = {}
        for item in batch.get("pages", []):
            url = urlsplit(item.get("url", ""))
            if url.scheme != "https" or url.netloc != "bigbudman.com":
                failures.append(f"Publication manifest has an off-domain or non-HTTPS URL: {item.get('url')}")
                continue
            route = url.path.lstrip("/")
            batch_paths[(route + "index.html") if route.endswith("/") else route] = item
    except Exception as exc:
        batch = {}
        batch_date = None
        batch_paths = {}
        failures.append(f"Invalid publication manifest before page audit: {exc}")
    titles: dict[str, Path] = {}
    descriptions: dict[str, Path] = {}
    canonicals: dict[str, Path] = {}
    expected_sitemap: set[str] = set()
    expected_sitemap_dates: dict[str, str] = {}
    expected_search: set[str] = set()
    incoming: dict[str, int] = {}
    incoming_sources: dict[str, set[str]] = {}
    fragment_cache: dict[Path, set[str]] = {}
    honeypot_count = 0

    def document_ids(path: Path) -> set[str]:
        if path not in fragment_cache:
            target_parser = Inspector()
            target_parser.feed(path.read_text(encoding="utf-8"))
            fragment_cache[path] = set(target_parser.ids)
        return fragment_cache[path]

    for page in html_files:
        text = page.read_text(encoding="utf-8")
        parser = Inspector(); parser.feed(text)
        rel = page.relative_to(ROOT)
        if '<html lang="en-US">' not in text: failures.append(f"{rel}: missing en-US language")
        if parser.h1 != 1: failures.append(f"{rel}: expected one h1, found {parser.h1}")
        duplicate_ids = [value for value, count in Counter(parser.ids).items() if count > 1]
        if duplicate_ids: failures.append(f"{rel}: duplicate HTML id values: {', '.join(sorted(duplicate_ids))}")
        for section_number, related in enumerate(re.findall(r'<section class="related-section".*?</section>', text, re.S), start=1):
            destinations = re.findall(r'<a href="([^"]+)"', related)
            duplicates = sorted(target for target, count in Counter(destinations).items() if count > 1)
            if duplicates:
                failures.append(f"{rel}: related section {section_number} repeats destinations: {', '.join(duplicates)}")
        if not parser.title.strip(): failures.append(f"{rel}: missing title")
        if len(parser.title.strip()) > 60: failures.append(f"{rel}: title longer than 60 characters")
        if len(parser.description.strip()) < 60: failures.append(f"{rel}: description shorter than 60 characters")
        if len(parser.description.strip()) > 160: failures.append(f"{rel}: description longer than 160 characters")
        if not parser.canonical.startswith("https://bigbudman.com/"): failures.append(f"{rel}: invalid canonical")
        for value, collection, label in ((parser.title.strip(),titles,"title"),(parser.description.strip(),descriptions,"description"),(parser.canonical,canonicals,"canonical")):
            if value in collection: failures.append(f"{rel}: duplicate {label} also in {collection[value].relative_to(ROOT)}")
            collection[value] = page
        if rel.as_posix() not in {"404.html","thank-you/index.html"}:
            expected_sitemap.add(parser.canonical)
            rel_url = rel.as_posix()
            expected_search.add("/" if rel_url == "index.html" else f"/{rel_url[:-10]}" if rel_url.endswith("/index.html") else f"/{rel_url}")
        if re.search(r"\b(?:lorem ipsum|TODO|FIXME|coming soon)\b|\{name\}", text, re.I): failures.append(f"{rel}: placeholder text")
        for table_match in re.finditer(r"<table\b[^>]*>", text, re.I):
            table_tag = table_match.group(0)
            if 'aria-labelledby="' not in table_tag:
                failures.append(f"{rel}: data table is not section-labelled")
                continue
            if 'tabindex="0"' in table_tag:
                continue
            before = text[:table_match.start()]
            region_start = before.rfind('<div class="comparison-table"')
            if region_start <= before.rfind('</div>'):
                failures.append(f"{rel}: data table is not keyboard-focusable")
                continue
            region_end = text.find('>', region_start)
            region_tag = text[region_start:region_end + 1]
            if not all(marker in region_tag for marker in ('tabindex="0"', 'role="region"', 'aria-labelledby="')):
                failures.append(f"{rel}: data table scroll region is not keyboard-focusable and section-labelled")
        for honeypot_tag in re.findall(r'<input\b[^>]*class="honeypot"[^>]*>', text, re.I):
            honeypot_count += 1
            if 'tabindex="-1"' not in honeypot_tag or 'aria-hidden="true"' not in honeypot_tag:
                failures.append(f"{rel}: honeypot field is exposed to keyboard or assistive technology")
        if 'data-article' in text:
            if 'class="mobile-toc"' not in text or 'data-mobile-toc' not in text:
                failures.append(f"{rel}: article is missing mobile section navigation")
            elif '<details class="mobile-toc">' not in text or '<summary>Jump to a section</summary>' not in text:
                failures.append(f"{rel}: mobile section navigation is not a native disclosure")
            if 'data-copy-citation' not in text or 'data-citation-reviewed' not in text:
                failures.append(f"{rel}: article is missing the copy-citation control")
            if not re.search(r'Reviewed\s*<time datetime="\d{4}-\d{2}-\d{2}">[^<]+</time>', text):
                failures.append(f"{rel}: visible review date is not machine-readable")
        robots = next((item.get("content", "") for item in parser.meta if item.get("name") == "robots"), "")
        if rel.as_posix() in {"404.html", "thank-you/index.html"}:
            if "noindex" not in robots: failures.append(f"{rel}: utility page is indexable")
        elif "index" not in robots or "noindex" in robots:
            failures.append(f"{rel}: indexable page has invalid robots directive")
        required_social = {
            ("property", "og:title"), ("property", "og:description"), ("property", "og:url"),
            ("property", "og:image"), ("property", "og:image:width"), ("property", "og:image:height"),
            ("property", "og:image:alt"), ("name", "twitter:card"), ("name", "twitter:title"),
            ("name", "twitter:description"), ("name", "twitter:image"), ("name", "twitter:image:alt"),
        }
        for attr, value in required_social:
            if not any(item.get(attr) == value and item.get("content") for item in parser.meta):
                failures.append(f"{rel}: missing social metadata {value}")
        schemas = []
        for raw in parser.jsonld:
            try: schemas.append(json.loads(raw))
            except Exception as exc: failures.append(f"{rel}: invalid JSON-LD: {exc}")
        graph_schema = next((item for item in schemas if isinstance(item.get("@graph"), list)), None)
        graph_nodes = graph_schema.get("@graph", []) if graph_schema else []
        primary = next((item for item in graph_nodes if item.get("@type") == "Article"), None)
        if primary is None:
            primary = next((item for item in graph_nodes if item.get("@type") == "WebPage"), None)
        if primary is None:
            primary = next((item for item in schemas if item.get("@type") in {"Article", "WebPage"}), None)
        if primary is None:
            failures.append(f"{rel}: missing primary WebPage or Article schema")
        elif rel.as_posix() not in {"404.html", "thank-you/index.html"}:
            modified = primary.get("dateModified", "")
            try:
                modified_date = datetime.strptime(modified, "%Y-%m-%d")
                expected_sitemap_dates[parser.canonical] = modified
                if batch_date and modified_date > batch_date:
                    failures.append(f"{rel}: dateModified is after the current publication batch")
            except (TypeError, ValueError):
                failures.append(f"{rel}: primary schema has an invalid dateModified")
        if graph_schema:
            graph_ids = [item.get("@id") for item in graph_nodes if item.get("@id")]
            duplicate_graph_ids = [value for value, count in Counter(graph_ids).items() if count > 1]
            if duplicate_graph_ids:
                failures.append(f"{rel}: duplicate JSON-LD @id values: {', '.join(sorted(duplicate_graph_ids))}")
            canonical_value = parser.canonical
            required_ids = {
                f"https://bigbudman.com/#organization": "Organization",
                f"https://bigbudman.com/#website": "WebSite",
                f"{canonical_value}#webpage": "WebPage",
            }
            nodes_by_id = {item.get("@id"): item for item in graph_nodes if item.get("@id")}
            for node_id, node_type in required_ids.items():
                if nodes_by_id.get(node_id, {}).get("@type") != node_type:
                    failures.append(f"{rel}: missing {node_type} node {node_id}")
            if 'property="og:type" content="article"' in text:
                article_id = f"{canonical_value}#article"
                webpage_id = f"{canonical_value}#webpage"
                article_node = nodes_by_id.get(article_id, {})
                webpage_node = nodes_by_id.get(webpage_id, {})
                if article_node.get("@type") != "Article": failures.append(f"{rel}: missing separate Article node")
                if webpage_node.get("mainEntity", {}).get("@id") != article_id: failures.append(f"{rel}: WebPage mainEntity does not identify Article")
                if article_node.get("mainEntityOfPage", {}).get("@id") != webpage_id: failures.append(f"{rel}: Article mainEntityOfPage does not identify WebPage")
        elif schemas:
            failures.append(f"{rel}: primary structured data is not an @graph")
        if primary and primary.get("@type") == "Article":
            for field in ("author", "datePublished", "dateModified", "image", "mainEntityOfPage", "inLanguage", "publisher"):
                if not primary.get(field): failures.append(f"{rel}: Article schema missing {field}")
            if "<" in primary.get("headline", ""): failures.append(f"{rel}: Article headline contains HTML")
            review_match = re.search(r'Reviewed\s*<time datetime="([^"]+)">', text)
            if review_match and review_match.group(1) != primary.get("dateModified"):
                failures.append(f"{rel}: visible review date does not match Article dateModified")
        breadcrumb_nodes = [item for item in graph_nodes if item.get("@type") == "BreadcrumbList"]
        breadcrumb_nodes.extend(item for item in schemas if item.get("@type") == "BreadcrumbList")
        if rel.as_posix() not in {"404.html", "thank-you/index.html"}:
            if len(breadcrumb_nodes) != 1:
                failures.append(f"{rel}: expected one canonical BreadcrumbList, found {len(breadcrumb_nodes)}")
            else:
                trail = breadcrumb_nodes[0].get("itemListElement", [])
                positions = [item.get("position") for item in trail]
                if not trail or positions != list(range(1, len(trail) + 1)):
                    failures.append(f"{rel}: BreadcrumbList positions are missing or noncontiguous")
                elif trail[0].get("name") != "Home" or trail[0].get("item") != "https://bigbudman.com/":
                    failures.append(f"{rel}: BreadcrumbList does not begin at the canonical home page")
                elif trail[-1].get("item") != parser.canonical:
                    failures.append(f"{rel}: BreadcrumbList does not end at the page canonical")
                webpage_node = next((item for item in graph_nodes if item.get("@type") == "WebPage"), {})
                if webpage_node.get("breadcrumb", {}).get("@id") != breadcrumb_nodes[0].get("@id"):
                    failures.append(f"{rel}: WebPage does not identify its BreadcrumbList node")
        if rel.as_posix().startswith("strains/") and rel.as_posix() != "strains/index.html":
            has_representative_photo = "REPRESENTATIVE PHOTO" in text and "not proof of cultivar identity" in text
            has_withheld_photo = "IMAGE WITHHELD" in text and "No verified cultivar photograph" in text
            if not (has_representative_photo or has_withheld_photo):
                failures.append(f"{rel}: missing representative-photo disclosure")
        if "href=\"javascript:" in text.lower(): failures.append(f"{rel}: javascript link")
        for src, alt in parser.images:
            if alt is None: failures.append(f"{rel}: image {src} missing alt")
            if src.lower().endswith(".webp") and not (alt or "").strip(): failures.append(f"{rel}: editorial photo {src} has empty alt text")
        for image in parser.image_attrs:
            src = image.get("src", "")
            if not image.get("width") or not image.get("height"): failures.append(f"{rel}: image {src} missing intrinsic dimensions")
            if image.get("decoding") != "async": failures.append(f"{rel}: image {src} missing async decoding")
            if not src.endswith("logo-full.webp") and image.get("loading") not in {"lazy", "eager"}:
                failures.append(f"{rel}: image {src} missing loading hint")
        if re.search(r'<div\b(?=[^>]*\bclass=["\'][^"\']*\bcomparison-table\b)(?=[^>]*\btabindex=["\']0["\'])[^>]*>\s*<table\b(?=[^>]*\btabindex=["\']0["\'])', text, re.I):
            failures.append(f"{rel}: responsive table has redundant nested focus targets")
        for region in re.findall(r'<div\b(?=[^>]*\bclass=["\'][^"\']*\bcomparison-table\b)[^>]*>', text, re.I):
            if not re.search(r'\btabindex=["\']0["\']', region) or not re.search(r'\brole=["\']region["\']', region) or not re.search(r'\baria-labelledby=["\'][^"\']+["\']', region):
                failures.append(f"{rel}: responsive table wrapper is not a named keyboard-scroll region")
        for target in parser.links:
            local = resolve_local(page, target)
            if local is not None and not local.exists(): failures.append(f"{rel}: broken local reference {target}")
            parts = urlsplit(target)
            if parts.fragment and not parts.scheme and not target.startswith(("//", "mailto:", "tel:", "javascript:", "data:")):
                fragment_page = local if parts.path else page
                if fragment_page is not None and fragment_page.exists() and fragment_page.suffix == ".html":
                    fragment = unquote(parts.fragment)
                    if fragment not in document_ids(fragment_page):
                        failures.append(f"{rel}: broken local fragment {target}")
            if local is not None and local.exists() and local.name == "index.html":
                target_rel = local.relative_to(ROOT).as_posix()
                target_url = "/" if target_rel == "index.html" else f"/{target_rel[:-10]}"
                incoming[target_url] = incoming.get(target_url, 0) + 1
                source_rel = rel.as_posix()
                if source_rel not in {"site-index/index.html", "updates/index.html"} and source_rel != target_rel:
                    incoming_sources.setdefault(target_url, set()).add(source_rel)
        for action in parser.forms:
            if action and not action.startswith("https://formsubmit.co/"): failures.append(f"{rel}: unexpected form action {action}")
        if rel.as_posix() not in {"404.html", "thank-you/index.html"}:
            if 'aria-current="page"' not in text:
                failures.append(f"{rel}: missing semantic current-page navigation")
            if '<nav class="container breadcrumbs"' in text and not re.search(r'<nav class="container breadcrumbs"[^>]*>.*?<span aria-current="page">[^<]+</span>', text, re.S):
                failures.append(f"{rel}: breadcrumb does not identify the current page")
            is_collection_detail = rel.as_posix() != "guides/cannabis-terms-label-lab-glossary/index.html" and any(rel.as_posix().startswith(f"{section}/") and rel.as_posix() != f"{section}/index.html" for section in ("guides", "gear", "strains", "legal"))
            if is_collection_detail and 'aria-current="location"' not in text:
                failures.append(f"{rel}: collection navigation does not identify the current location")
        if rel.as_posix() in batch_paths:
            manifest_item = batch_paths[rel.as_posix()]
            visible = re.sub(r"<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>", " ", text, flags=re.I | re.S)
            words = re.findall(r"\b[\w’'-]+\b", visible)
            if manifest_item.get("department") in {"guides", "gear", "commercial"} and len(words) < 850:
                failures.append(f"{rel}: current article has only {len(words)} visible words")
            local_anchors = [href for href in parser.anchors if resolve_local(page, href) is not None]
            if len(local_anchors) < 3: failures.append(f"{rel}: fewer than three meaningful internal links")
            for marker in ('property="og:title"', 'property="og:description"', 'property="og:url"', 'property="og:image"', 'name="twitter:card"'):
                if marker not in text: failures.append(f"{rel}: missing social metadata marker {marker}")
            schema_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
            if not schema_match:
                failures.append(f"{rel}: missing JSON-LD")
            else:
                try:
                    schema = json.loads(schema_match.group(1))
                    if manifest_item.get("department") in {"guides", "gear", "commercial"}:
                        expected_date = batch_date.strftime("%Y-%m-%d") if batch_date else ""
                        article_schema = next((node for node in schema.get("@graph", []) if node.get("@type") == "Article"), None)
                        if article_schema is None: failures.append(f"{rel}: JSON-LD graph has no Article")
                        elif article_schema.get("dateModified") != expected_date: failures.append(f"{rel}: wrong JSON-LD dateModified")
                        if article_schema and article_schema.get("datePublished") and article_schema.get("datePublished") > expected_date: failures.append(f"{rel}: JSON-LD publication date is after the current batch")
                        if f'property="article:modified_time" content="{expected_date}"' not in text: failures.append(f"{rel}: wrong article:modified_time")
                except Exception as exc:
                    failures.append(f"{rel}: invalid JSON-LD: {exc}")
        if re.search(r'href="https?://[^\"]*(?:amazon\.|amzn\.|[?&](?:tag|aff(?:iliate)?_?id)=)', text, re.I):
            failures.append(f"{rel}: affiliate-looking URL present without an approved repository configuration")

    if honeypot_count != 6:
        failures.append(f"Expected six protected newsletter/contact honeypots, found {honeypot_count}")

    try:
        tree = ET.parse(ROOT / "sitemap.xml")
        ns = {"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
        sitemap_nodes = tree.findall(".//s:url", ns)
        sitemap_pairs = []
        for node in sitemap_nodes:
            loc = node.findtext("s:loc", default="", namespaces=ns)
            lastmod = node.findtext("s:lastmod", default="", namespaces=ns)
            sitemap_pairs.append((loc, lastmod))
            try:
                parsed_lastmod = datetime.strptime(lastmod, "%Y-%m-%d")
                if batch_date and parsed_lastmod > batch_date:
                    failures.append(f"Sitemap has a future lastmod for {loc}: {lastmod}")
            except ValueError:
                failures.append(f"Sitemap has an invalid lastmod for {loc}: {lastmod or '(missing)'}")
        sitemap_urls = {loc for loc, _ in sitemap_pairs}
        if len(sitemap_pairs) != len(sitemap_urls):
            failures.append("Sitemap contains duplicate loc records")
        if sitemap_urls != expected_sitemap:
            missing = expected_sitemap - sitemap_urls
            extra = sitemap_urls - expected_sitemap
            if missing: failures.append("Sitemap missing: " + ", ".join(sorted(missing)))
            if extra: failures.append("Sitemap extra: " + ", ".join(sorted(extra)))
        sitemap_dates = dict(sitemap_pairs)
        for loc, expected_date in expected_sitemap_dates.items():
            if sitemap_dates.get(loc) != expected_date:
                failures.append(f"Sitemap lastmod mismatch for {loc}: expected {expected_date}, found {sitemap_dates.get(loc, '(missing)')}")
        if (ROOT / "index.php").read_bytes() != (ROOT / "sitemap.xml").read_bytes():
            failures.append("Legacy Search Console sitemap payload differs from canonical sitemap.xml")
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        sitemap_directives = re.findall(r"^Sitemap:\s*(\S+)\s*$", robots, re.M | re.I)
        if sitemap_directives != ["https://bigbudman.com/sitemap.xml"]:
            failures.append(f"robots.txt must name the canonical HTTPS sitemap exactly once; found {sitemap_directives}")
    except Exception as exc:
        failures.append(f"Invalid sitemap.xml: {exc}")

    try:
        search_raw = (ROOT / "assets/js/search-index.js").read_text(encoding="utf-8").strip()
        prefix = "window.BBM_SEARCH_INDEX = "
        if not search_raw.startswith(prefix) or not search_raw.endswith(";"):
            raise ValueError("unexpected assignment wrapper")
        search_items = json.loads(search_raw[len(prefix):-1])
        search_urls = {item["url"] for item in search_items}
        if search_urls != expected_search:
            failures.append(f"Search index URL set mismatch: expected {len(expected_search)}, found {len(search_urls)}")
        if not any(item.get("url") == "/strains/lantz/" and "lance" in item.get("keywords", "").lower() for item in search_items):
            failures.append("Search index is missing the Lance alias for Lantz")
    except Exception as exc:
        failures.append(f"Invalid search index: {exc}")

    for route in sorted(expected_search):
        if route.startswith(("/strains/", "/legal/")) and route not in {"/strains/", "/legal/"} and incoming.get(route, 0) < 2:
            failures.append(f"{route}: fewer than two internal links")
        if route.startswith(("/guides/", "/gear/")) and route not in {"/guides/", "/gear/"} and len(incoming_sources.get(route, set())) < 2:
            failures.append(f"{route}: fewer than two distinct contextual or collection source pages")

    try:
        strain_hub = (ROOT / "strains/index.html").read_text(encoding="utf-8")
        if strain_hub.count("data-strain-card") != 118: failures.append("Strain hub does not contain exactly 118 cards")
        for marker in ('data-cannabinoid-filter="cbd"', 'data-cannabinoid-filter="cbg"', 'data-cannabinoid-filter="ratio"', 'lance ridgeline lantz'):
            if marker not in strain_hub: failures.append(f"Strain hub is missing expected marker: {marker}")
    except Exception as exc:
        failures.append(f"Invalid strain hub: {exc}")

    try:
        guides_hub = (ROOT / "guides/index.html").read_text(encoding="utf-8")
        guide_routes = re.findall(r'class="library-card"[^>]*href="([^"]+)"', guides_hub)
        guide_page = ROOT / "guides/index.html"
        hub_guide_files = {resolve_local(guide_page, href).relative_to(ROOT).as_posix() for href in guide_routes if resolve_local(guide_page, href) and resolve_local(guide_page, href).relative_to(ROOT).as_posix().startswith("guides/")}
        actual_guide_files = {path.relative_to(ROOT).as_posix() for path in (ROOT / "guides").glob("*/index.html")}
        if len(guide_routes) != len(set(guide_routes)) or hub_guide_files != actual_guide_files:
            failures.append(f"Guide hub/source mismatch: {len(hub_guide_files)} cards for {len(actual_guide_files)} detail pages")
        semantic_dates = re.findall(r'class="library-card__reviewed">Reviewed <time datetime="\d{4}-\d{2}-\d{2}">[^<]+</time>', guides_hub)
        if len(semantic_dates) != len(guide_routes):
            failures.append(f"Guide hub has {len(semantic_dates)} semantic review dates for {len(guide_routes)} cards")
        for marker in ("cbn-products-label-evidence-guide/", "cannabis-social-hosting-guest-safety-plan/", "Cannabis flower buying checklist", "cannabis-claim-fact-check-worksheet/", "Edible labels, timing, and buying", "Store cannabis safely by product type", "Tolerance, dependence, and withdrawal", "Rebuild the product", 'data-updated="2026-10-19"'):
            if marker not in guides_hub:
                failures.append(f"Guide hub is missing required discovery marker: {marker}")
    except Exception as exc:
        failures.append(f"Invalid guide hub: {exc}")

    try:
        gear_hub = (ROOT / "gear/index.html").read_text(encoding="utf-8")
        gear_routes = re.findall(r'data-gear-card[^>]*[^>]*href="([^"]+)"|href="([^"]+)"[^>]*data-gear-card', gear_hub)
        gear_hrefs = [left or right for left, right in gear_routes]
        gear_page = ROOT / "gear/index.html"
        hub_gear_files = {resolve_local(gear_page, href).relative_to(ROOT).as_posix() for href in gear_hrefs if resolve_local(gear_page, href)}
        actual_gear_files = {path.relative_to(ROOT).as_posix() for path in (ROOT / "gear").glob("*/index.html")}
        if len(gear_hrefs) != len(set(gear_hrefs)) or hub_gear_files != actual_gear_files:
            failures.append(f"Gear hub/source mismatch: {len(hub_gear_files)} cards for {len(actual_gear_files)} detail pages")
        if f'{len(actual_gear_files)} INDEPENDENT ACCESSORY GUIDES' not in gear_hub or f'All {len(actual_gear_files)}' not in gear_hub:
            failures.append("Gear hub displayed totals do not match generated gear detail pages")
    except Exception as exc:
        failures.append(f"Invalid gear hub: {exc}")

    try:
        legal_hub = (ROOT / "legal/index.html").read_text(encoding="utf-8")
        if legal_hub.count("data-state-card") != 50: failures.append("Legal hub does not contain exactly 50 state cards")
        for marker in ('data-state-filter="adult"', 'data-state-filter="medical"', 'data-state-filter="limited"', 'data-state-filter="restricted"', '50 STATE PAGES REVIEWED', 'cannabis-federal-property-rules-guide/'):
            if marker not in legal_hub: failures.append(f"Legal hub is missing expected marker: {marker}")
        state_routes = {f"legal/{state}/index.html" for state in [
            "alabama","alaska","arizona","arkansas","california","colorado","connecticut","delaware","florida","georgia","hawaii","idaho","illinois","indiana","iowa","kansas","kentucky","louisiana","maine","maryland","massachusetts","michigan","minnesota","mississippi","missouri","montana","nebraska","nevada","new-hampshire","new-jersey","new-mexico","new-york","north-carolina","north-dakota","ohio","oklahoma","oregon","pennsylvania","rhode-island","south-carolina","south-dakota","tennessee","texas","utah","vermont","virginia","washington","west-virginia","wisconsin","wyoming"
        ]}
        actual_routes = {path.relative_to(ROOT).as_posix() for path in (ROOT/"legal").glob("*/index.html")}
        if not state_routes.issubset(actual_routes): failures.append("Legal library is missing state routes: " + ", ".join(sorted(state_routes-actual_routes)))
    except Exception as exc:
        failures.append(f"Invalid legal hub: {exc}")

    for required in ["CNAME","robots.txt","sitemap.xml","index.php","feed.xml","site.webmanifest","publication-manifest.json","site-index/index.html","updates/index.html","assets/css/styles.css","assets/js/app.js","assets/js/search-index.js","assets/images/og-card.png","assets/images/logo-full.webp","assets/images/logo-mark.svg","assets/images/strain-cbd-flower.webp","assets/images/strain-balanced-cannabinoids.webp"]:
        if not (ROOT/required).exists(): failures.append(f"Missing required file: {required}")
    for image in sorted((ROOT/"assets/images").glob("*.webp")):
        raw=image.read_bytes()
        if len(raw) < 16 or raw[:4] != b"RIFF" or raw[8:12] != b"WEBP":
            failures.append(f"Invalid WebP header: {image.relative_to(ROOT)}")
            continue
        declared=int.from_bytes(raw[4:8],"little")+8
        if declared != len(raw): failures.append(f"Truncated WebP: {image.relative_to(ROOT)} declares {declared} bytes, found {len(raw)}")
    if (ROOT/"CNAME").exists() and (ROOT/"CNAME").read_text().strip() != "bigbudman.com": failures.append("CNAME is not bigbudman.com")
    try:
        manifest=json.loads((ROOT/"site.webmanifest").read_text())
        if manifest.get("name") != "Big Bud Man": failures.append("Manifest name mismatch")
    except Exception as exc: failures.append(f"Invalid manifest: {exc}")
    try:
        pages = batch.get("pages", [])
        actual_urls = [item.get("url") for item in pages]
        if batch.get("page_count") != len(pages) or len(pages) != 3:
            failures.append("Publication manifest does not describe exactly three new pages")
        if len(actual_urls) != len(set(actual_urls)):
            failures.append("Publication manifest contains duplicate URLs")
        if any(item.get("portfolio_label") not in {"Data-led", "Authority-expansion", "Exploration"} for item in pages):
            failures.append("Publication manifest contains an invalid portfolio label")
        for rel_path in batch_paths:
            if not (ROOT / rel_path).exists(): failures.append(f"Publication manifest target is missing: {rel_path}")
        if batch.get("monetization", {}).get("affiliate_links_added") != 0:
            failures.append("Publication manifest monetization count is not zero")
        if batch.get("image_qa", {}).get("editorial_placements") != 0 or batch.get("image_qa", {}).get("affiliate_or_product_images") != 0:
            failures.append("Publication manifest image-QA counts are incorrect")
    except Exception as exc: failures.append(f"Invalid publication manifest: {exc}")

    try:
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        for stack_number, stack in enumerate(re.findall(r'<div class="story-stack">(.*?)</div>', home, re.S), start=1):
            destinations = re.findall(r'<a href="([^"]+)"', stack)
            duplicates = sorted(target for target, count in Counter(destinations).items() if count > 1)
            if duplicates:
                failures.append(f"Homepage story stack {stack_number} repeats destinations: {', '.join(duplicates)}")
        if 'data-value="concentrate"' not in home:
            failures.append("Homepage Clear-Lane Finder is missing the concentrate route")
        app = (ROOT / "assets/js/app.js").read_text(encoding="utf-8")
        for marker in ("setGateIsolation", "node.inert = active", "trapAgeGateFocus", "event.key !== 'Tab'", "releaseAgeGate", "data-age-inert", "card.focus()"):
            if marker not in app: failures.append(f"Age-gate focus isolation is missing JavaScript marker: {marker}")
        for marker in ("ageDescription.id = 'age-description'", "ageCard.setAttribute('aria-describedby', ageDescription.id)"):
            if marker not in app: failures.append(f"Age-gate dialog description is missing JavaScript marker: {marker}")
        for marker in ("routes.concentrate", "cannabis-concentrates-dabs-label-safety-guide"):
            if marker not in app: failures.append(f"Homepage router is missing concentrate marker: {marker}")
        search_raw = (ROOT / "assets/js/search-index.js").read_text(encoding="utf-8")
        if '"url":"/guides/cannabis-concentrates-dabs-label-safety-guide/"' not in search_raw or 'shatter' not in search_raw:
            failures.append("Search index is missing the concentrate route or its shelf-language aliases")
        if 'data-value="beverage"' not in home:
            failures.append("Homepage Clear-Lane Finder is missing the beverage route")
        for marker in ("routes.beverage", "cannabis-beverages-label-timing-buying-guide"):
            if marker not in app: failures.append(f"Homepage router is missing beverage marker: {marker}")
        guide_hub = (ROOT / "guides/index.html").read_text(encoding="utf-8")
        for marker in ('data-guide-library', 'data-guide-search', 'data-guide-filter="format"', 'data-guide-card'):
            if marker not in guide_hub: failures.append(f"Guide library finder is missing marker: {marker}")
        collection_contracts = [
            ("guides/index.html", "guide-results", "data-guide-filter", "data-guide-search"),
            ("gear/index.html", "gear-results", "data-gear-filter", "data-gear-search"),
            ("strains/index.html", "strain-results", "data-filter|data-cannabinoid-filter", "data-strain-search"),
            ("legal/index.html", "state-results", "data-state-filter", "data-state-search"),
        ]
        for collection_path, result_id, button_pattern, search_marker in collection_contracts:
            collection_html = (ROOT / collection_path).read_text(encoding="utf-8")
            if f'id="{result_id}"' not in collection_html:
                failures.append(f"{collection_path} is missing the controlled result collection {result_id}")
            if not re.search(rf'<[^>]+{search_marker}[^>]+aria-controls="{result_id}"', collection_html):
                failures.append(f"{collection_path} search does not identify {result_id} as its result collection")
            filter_buttons = re.findall(rf'<button\b[^>]+(?:{button_pattern})[^>]*>', collection_html)
            if not filter_buttons:
                failures.append(f"{collection_path} has no auditable filter buttons")
            for button in filter_buttons:
                for required in ('type="button"', 'aria-pressed="', f'aria-controls="{result_id}"'):
                    if required not in button:
                        failures.append(f"{collection_path} filter button lacks {required}: {button[:140]}")
            if 'role="group"' not in collection_html:
                failures.append(f"{collection_path} filter controls are missing a named group")
        if "setAttribute('aria-pressed', String(selected))" not in app:
            failures.append("Collection filters do not synchronize live aria-pressed state")
        if '"url":"/guides/cannabis-beverages-label-timing-buying-guide/"' not in search_raw or 'seltzer' not in search_raw:
            failures.append("Search index is missing the beverage route or its shelf-language aliases")
        if 'data-value="recall"' not in home:
            failures.append("Homepage Clear-Lane Finder is missing the recall route")
        for marker in ("routes.recall", "cannabis-product-recall-batch-checker"):
            if marker not in app: failures.append(f"Homepage router is missing recall marker: {marker}")
        if 'data-value="lab"' not in home:
            failures.append("Homepage Clear-Lane Finder is missing the lab-report route")
        for marker in ("routes.lab", "cannabis-certificate-of-analysis-coa-guide"):
            if marker not in app: failures.append(f"Homepage router is missing lab-report marker: {marker}")
        if 'data-value="urgent"' not in home:
            failures.append("Homepage Clear-Lane Finder is missing the urgent exposure route")
        for marker in ("routes.urgent", "cannabis-overconsumption-poisoning-response"):
            if marker not in app: failures.append(f"Homepage router is missing urgent-response marker: {marker}")
        source_directory = (ROOT / "guides/cannabis-official-source-directory/index.html").read_text(encoding="utf-8")
        for marker in ("poison.org", "findtreatment.gov", "fda.gov/safety/medwatch", "cpsc.gov/Recalls", "reportfraud.ftc.gov", "nhtsa.gov", "transportation.gov/odapc", "tsa.gov/travel/security-screening/whatcanibring/all-list", "usda.gov/topics/hemp", "cannabis.ny.gov/consumers", "Run the six-part source test"):
            if marker not in source_directory: failures.append(f"Official-source directory is missing marker: {marker}")
        oral_comparison = (ROOT / "guides/cannabis-gummies-drinks-oils-capsules-comparison/index.html").read_text(encoding="utf-8")
        for marker in ("5 × 2 × 5 = 50 mg THC", "2 × 30 = 60 mg THC", "crosswalk-metrc-product-categories", "Compare three products without choosing for the reader", "No seller, brand, product, coupon, or affiliate link appears"):
            if marker not in oral_comparison: failures.append(f"Oral-format comparison is missing marker: {marker}")
        styles = (ROOT / "assets/css/styles.css").read_text(encoding="utf-8")
        if ".mobile-toc{display:block" not in styles or ".mobile-toc,.site-footer" not in styles:
            failures.append("Mobile section navigator lacks responsive or print behavior")
        if "data-mobile-toc" not in app:
            failures.append("Article script does not synchronize mobile section navigation")
        discovery_checks = {
            "index.html": ("guides/cannabis-next-day-impairment-evidence-guide/", "guides/cbn-products-label-evidence-guide/", "legal/cannabis-federal-property-rules-guide/", "guides/cannabis-social-hosting-guest-safety-plan/", "guides/terpenes/", "gear/cannabis-loupe-pocket-microscope-guide/", "guides/cannabis-cbd-chronic-pain-evidence-guide/", "guides/storage/", "gear/cannabis-accessibility-tools-buying-guide/"),
            "strains/index.html": ("stem-cell-cbg/", "118 STRAIN FIELD NOTES", "NO VERIFIED CULTIVAR IMAGE"),
            "guides/index.html": ("cannabis-next-day-impairment-evidence-guide/", "cannabis-cbd-chronic-pain-evidence-guide/", "cannabis-cbd-cancer-claims-evidence-guide/", "cannabis-menu-package-receipt-match-checklist/", "cannabis-exercise-workout-heat-safety/", "new-york-home-cannabis-pest-mold-ipm-guide/", "new-york-home-cannabis-harvest-drying-curing-log/", "cannabis-cbd-epilepsy-seizure-care-guide/", "cannabis-glaucoma-eye-pressure-vision-guide/", "cbd-patches-transdermal-label-evidence-guide/", "cannabis-package-seal-tamper-evidence-checklist/", "cannabis-dry-mouth-dental-oral-health-guide/", "cannabis-edible-label-math-checker/", "cbg-products-label-evidence-guide/", "cannabis-contaminant-test-results-guide/", "cannabis-child-resistant-packaging-home-storage-guide/", "cannabis-official-source-directory/", "cannabis-gummies-drinks-oils-capsules-comparison/", "cannabis-claim-fact-check-worksheet/", "Store cannabis safely by product type", "Thirty useful paths", "Comparing packaged cannabis flower", 'data-guide-sort', 'data-updated="2026-10-23"', 'data-guide-filter="health"', 'data-guide-filter="workplace"'),
            "gear/index.html": ("used-cannabis-accessory-buying-safety-guide/", "cannabis-accessibility-tools-buying-guide/", "smell-proof-storage/", "cannabis-rolling-tray-buying-guide/", "cannabis-rolling-paper-cone-guide/", "digital-scale-buying-calibration-guide/", "cannabis-tool-cleaning-kit/", "indoor-cannabis-grow-light-buying-cost-planner/", "cannabis-gear-comparison-worksheet/", "cannabis-accessory-return-warranty-recall-guide/", "dry-herb-vaporizer-dosing-capsule-guide/", "Screen used gear before handoff", "All 25"),
            "guides/read-a-label/index.html": ("Build a date chain", "Preserve a label-to-lot evidence card", "cannabis.ny.gov/part-128-guidance", "cannabis-certificate-of-analysis-coa-guide/", "cannabis-product-recall-batch-checker/"),
            "responsible-use/index.html": ("guides/cannabis-exercise-workout-heat-safety/",),
            "guides/cannabis-exercise-workout-heat-safety/index.html": ("cdc.gov/cannabis/health-effects/brain-health", "cdc.gov/heat-health/risk-factors/heat-and-athletes", "nhtsa.gov/risky-driving/drug-impaired-driving", "2026list_en_final_clean"),
            "gear/cannabis-rolling-paper-cone-guide/index.html": ("data-paper-comparison", "Cost per usable item", "No commercial link appears"),
            "gear/cannabis-ashtray-ember-disposal-guide/index.html": ("cannabis-lighter-flame-safety-guide/",),
            "guides/cannabis-cbd-medication-interactions/index.html": ("cannabis-cbd-chronic-pain-evidence-guide/", "cannabis-cbd-cancer-claims-evidence-guide/"),
            "guides/cannabis-before-surgery-anesthesia/index.html": ("cannabis-cbd-cancer-claims-evidence-guide/",),
            "guides/cbg-products-label-evidence-guide/index.html": ("stem-cell-cbg/",),
            "guides/storage/index.html": ("smell-proof-storage/", "Use five controls instead of one container", "No home method can certify"),
            "gear/cannabis-accessibility-tools-buying-guide/index.html": ("cannabis-gear-comparison-worksheet/", "exact blocked task", "No merchant or product link appears"),
            "guides/new-york-home-cannabis-grow-planner/index.html": ("new-york-home-cannabis-pest-mold-ipm-guide/", "new-york-home-cannabis-harvest-drying-curing-log/", "indoor-cannabis-grow-light-buying-cost-planner/"),
            "guides/new-york-home-cannabis-pest-mold-ipm-guide/index.html": ("new-york-home-cannabis-harvest-drying-curing-log/",),
            "guides/new-york-home-cannabis-harvest-drying-curing-log/index.html": ("Mass remaining (%)", "extension.oregonstate.edu", "blog.uvm.edu", "Do not smoke or ingest a sample"),
            "guides/cannabis-next-day-impairment-evidence-guide/index.html": ("Read the systematic review in both directions", "pubmed.ncbi.nlm.nih.gov/36475998", "self-checks cannot certify performance", "intentionally gives no waiting period"),
            "gear/indoor-cannabis-grow-light-buying-cost-planner/index.html": ("new-york-home-cannabis-pest-mold-ipm-guide/",),
            "guides/cannabis-contaminant-test-results-guide/index.html": ("new-york-home-cannabis-pest-mold-ipm-guide/",),
            "gear/cannabis-inventory-label-record-kit/index.html": ("digital-scale-buying-calibration-guide/",),
            "guides/full-spectrum-broad-spectrum-cbd-isolate/index.html": ("cbd-drinks-powders-label-buying-guide/", "cbd-hemp-flower-label-legal-guide/", "cannabis-drug-testing-thc-results-guide/"),
            "guides/cbd-oil-tincture-label-buying-guide/index.html": ("cannabis-cbd-epilepsy-seizure-care-guide/",),
            "guides/cannabis-101/index.html": ("delta-8-thc-label-safety-guide/",),
            "guides/flower/index.html": ("cannabis-flower-freshness-package-date-buying-guide/",),
            "legal/shop-legal/index.html": ("cannabis-menu-package-receipt-match-checklist/", "new-york-cannabis-delivery-online-order-verification-guide/"),
            "guides/cannabis-product-price-label-comparison-calculator/index.html": ("cannabis-menu-package-receipt-match-checklist/",),
            "guides/cbd-gummies-label-buying-guide/index.html": ("cannabis-edible-allergen-ingredient-label-guide/",),
            "guides/cannabis-product-complaint-adverse-event-reporting/index.html": ("cannabis-accessory-return-warranty-recall-guide/", "cannabis-menu-package-receipt-match-checklist/", "cannabis-edible-allergen-ingredient-label-guide/"),
            "guides/terpenes/index.html": ("1%", "10 mg/g", "pubmed.ncbi.nlm.nih.gov/40603590", "25-term descriptive vocabulary"),
            "gear/cannabis-loupe-pocket-microscope-guide/index.html": ("data-loupe-comparison", "data-loupe-fov-result", "$15.33", "Blank fields stay unknown"),
            "guides/cbn-products-label-evidence-guide/index.html": ("modified intention-to-treat", "pubmed.ncbi.nlm.nih.gov/37796540", "No product, brand, seller, coupon or affiliate link appears"),
            "legal/cannabis-federal-property-rules-guide/index.html": ("April 28, 2026", "36 CFR 2.35", "federalregister.gov/documents/2026/04/28/2026-08176"),
            "guides/cannabis-social-hosting-guest-safety-plan/index.html": ("1-800-222-1222", "original labeled package", "No cannabis seller, delivery service, party kit, product, coupon or affiliate link appears"),
            "gear/cannabis-lighter-flame-safety-guide/index.html": ("Compare three exact models before checkout", "U.S. CPSC: Recalls and Product Safety Warnings", "No merchant, product, price, coupon, ranking, or affiliate link appears"),
            "gear/used-cannabis-accessory-buying-safety-guide/index.html": ("Adjusted used cost", "cpsc.gov/Business--Manufacturing/Online-Sellers-Safety-Guide", "used-lithium-ion-batteries", "No marketplace, merchant, product, model, price, coupon, or affiliate link appears"),
            "editorial-policy/index.html": ("Sitemap date integrity", "legacy Search Console compatibility endpoint", "cannot be later than the current publication batch"),
            "updates/index.html": ("guides/cannabis-next-day-impairment-evidence-guide/", "guides/new-york-home-cannabis-harvest-drying-curing-log/", "gear/used-cannabis-accessory-buying-safety-guide/", "October 23, 2026"),
            "site-index/index.html": ("guides/cannabis-next-day-impairment-evidence-guide/", "guides/new-york-home-cannabis-harvest-drying-curing-log/", "gear/used-cannabis-accessory-buying-safety-guide/", "October 23, 2026", "updates/"),
        }
        for discovery_page, markers in discovery_checks.items():
            discovery_text = (ROOT / discovery_page).read_text(encoding="utf-8")
            for marker in markers:
                if marker not in discovery_text:
                    failures.append(f"{discovery_page}: missing current discovery marker {marker}")
        for marker in ("data-loupe-comparison", "data-loupe-device", "renderLoupeComparison", "Short ${Math.abs(margin)"):
            if marker not in app: failures.append(f"Loupe comparison script is missing marker: {marker}")
        if '"url":"/guides/terpenes/"' not in search_raw or 'mg g aroma limonene' not in search_raw.lower():
            failures.append("Search index is missing the expanded terpene guide or its panel vocabulary")
        if '"url":"/guides/cannabis-certificate-of-analysis-coa-guide/"' not in search_raw or 'reporting limit' not in search_raw.lower():
            failures.append("Search index is missing the certificate guide or its laboratory-report vocabulary")
        if '"url":"/guides/cannabinoid-hyperemesis-syndrome-warning-signs/"' not in search_raw or 'recurrent vomiting' not in search_raw.lower():
            failures.append("Search index is missing the CHS guide or its warning-sign vocabulary")
        if '"url":"/gear/cannabis-lighter-flame-safety-guide/"' not in search_raw or 'child resistant' not in search_raw.lower():
            failures.append("Search index is missing the lighter guide or its fire-safety vocabulary")
        if '"url":"/guides/cannabis-overconsumption-poisoning-response/"' not in search_raw or 'poison control' not in search_raw.lower():
            failures.append("Search index is missing the overconsumption guide or its response vocabulary")
        if '"url":"/gear/cannabis-gear-comparison-worksheet/"' not in search_raw or 'first-year cost' not in search_raw.lower():
            failures.append("Search index is missing the gear worksheet or its comparison vocabulary")
        if '"url":"/guides/cbd-capsules-softgels-label-buying-guide/"' not in search_raw or 'softgel' not in search_raw.lower():
            failures.append("Search index is missing the CBD capsule guide or its softgel vocabulary")
        if '"url":"/strains/auto-cbg/"' not in search_raw or 'day-neutral' not in search_raw.lower():
            failures.append("Search index is missing the Auto CBG field note or its day-neutral vocabulary")
        if '"url":"/gear/cannabis-inventory-label-record-kit/"' not in search_raw or 'original packaging' not in search_raw.lower():
            failures.append("Search index is missing the cannabis inventory kit or its package-record vocabulary")
        if '"url":"/guides/cbd-products-for-pets-veterinarian-label-guide/"' not in search_raw or 'veterinarian' not in search_raw.lower():
            failures.append("Search index is missing the pet CBD guide or its veterinarian vocabulary")
        if '"url":"/gear/cannabis-vape-battery-cartridge-disposal-guide/"' not in search_raw or 'e-waste' not in search_raw.lower():
            failures.append("Search index is missing the vape disposal guide or its e-waste vocabulary")
        if '"url":"/guides/dot-cannabis-cbd-drug-testing-safety-sensitive-workers/"' not in search_raw or 'return to duty' not in search_raw.lower():
            failures.append("Search index is missing the DOT guide or its return-to-duty vocabulary")
        if '"url":"/guides/cannabis-older-adults-medication-fall-safety/"' not in search_raw or 'falls dizziness' not in search_raw.lower():
            failures.append("Search index is missing the older-adult guide or its fall-safety vocabulary")
        if '"url":"/gear/indoor-cannabis-grow-light-buying-cost-planner/"' not in search_raw or 'ppfd' not in search_raw.lower():
            failures.append("Search index is missing the grow-light planner or its evidence vocabulary")
        if '"url":"/guides/cannabis-smoke-vape-lung-health-guide/"' not in search_raw or 'evali' not in search_raw.lower():
            failures.append("Search index is missing the lung-health guide or its vaping vocabulary")
        if '"url":"/guides/cannabis-pre-roll-infused-label-buying-guide/"' not in search_raw or 'infused pre-roll' not in search_raw.lower():
            failures.append("Search index is missing the pre-roll guide or its product vocabulary")
        if '"url":"/guides/cannabis-terms-label-lab-glossary/"' not in search_raw or 'ppm ppb' not in search_raw.lower():
            failures.append("Search index is missing the glossary or its laboratory vocabulary")
        if '"url":"/guides/cannabis-anxiety-paranoia-psychosis-warning-signs/"' not in search_raw or 'hallucinations delusions' not in search_raw.lower():
            failures.append("Search index is missing the mental-health guide or its warning-sign vocabulary")
        if '"url":"/guides/cannabis-product-price-label-comparison-calculator/"' not in search_raw or 'cost per 100 mg' not in search_raw.lower():
            failures.append("Search index is missing the package comparison calculator or its price vocabulary")
        if '"url":"/guides/cannabis-product-complaint-adverse-event-reporting/"' not in search_raw or 'medwatch' not in search_raw.lower():
            failures.append("Search index is missing the complaint guide or its reporting vocabulary")
        if '"url":"/guides/disposable-vape-vs-510-cartridge-comparison/"' not in search_raw or 'compatibility' not in search_raw.lower():
            failures.append("Search index is missing the vape comparison or its compatibility vocabulary")
        if '"url":"/guides/cbd-hemp-flower-label-legal-guide/"' not in search_raw or 'dry weight' not in search_raw.lower():
            failures.append("Search index is missing the CBD/hemp flower guide or its legal-basis vocabulary")
        if '"url":"/guides/cbd-drinks-powders-label-buying-guide/"' not in search_raw or 'drink mix' not in search_raw.lower():
            failures.append("Search index is missing the CBD drinks guide or its format vocabulary")
        if '"url":"/guides/delta-8-thc-label-safety-guide/"' not in search_raw or 'psychoactive' not in search_raw.lower():
            failures.append("Search index is missing the delta-8 guide or its safety vocabulary")
        if '"url":"/guides/cannabis-edible-allergen-ingredient-label-guide/"' not in search_raw or 'cross-contact' not in search_raw.lower():
            failures.append("Search index is missing the edible-allergen guide or its ingredient vocabulary")
        if '"url":"/guides/new-york-home-cannabis-harvest-drying-curing-log/"' not in search_raw or 'postharvest' not in search_raw.lower():
            failures.append("Search index is missing the harvest log or its post-harvest vocabulary")
        if '"url":"/gear/used-cannabis-accessory-buying-safety-guide/"' not in search_raw or 'secondhand' not in search_raw.lower():
            failures.append("Search index is missing the used-accessory guide or its secondhand vocabulary")
        if '"url":"/guides/cannabis-next-day-impairment-evidence-guide/"' not in search_raw or 'residual' not in search_raw.lower():
            failures.append("Search index is missing the next-day impairment guide or its residual-effect vocabulary")
        if '"url":"/guides/cannabis-child-resistant-packaging-home-storage-guide/"' not in search_raw or 'childproof' not in search_raw.lower():
            failures.append("Search index is missing the packaging guide or its child-safety vocabulary")
        if '"url":"/strains/stem-cell-cbg/"' not in search_raw or 'cbga' not in search_raw.lower():
            failures.append("Search index is missing the Stem Cell CBG field note or its chemistry vocabulary")
        if '"url":"/guides/cannabis-cbd-chronic-pain-evidence-guide/"' not in search_raw or 'neuropathic pain' not in search_raw.lower():
            failures.append("Search index is missing the chronic-pain guide or its evidence vocabulary")
        if '"url":"/guides/cannabis-cbd-liver-health-safety-guide/"' not in search_raw or 'liver enzymes' not in search_raw.lower():
            failures.append("Search index is missing the liver-health guide or its evidence vocabulary")
        delta8 = (ROOT / "guides/delta-8-thc-label-safety-guide/index.html").read_text(encoding="utf-8")
        for marker in ('FDA: 5 Things to Know About Delta-8 THC', 'CDC: Cannabis Frequently Asked Questions', 'Use a ten-gate product screen'):
            if marker not in delta8: failures.append(f"Delta-8 guide is missing authority marker: {marker}")
        allergens = (ROOT / "guides/cannabis-edible-allergen-ingredient-label-guide/index.html").read_text(encoding="utf-8")
        for marker in ('FDA: Food Allergies', 'New York OCM: Adopted Part 128 Regulations', 'Use the allergy-aware checkout screen'):
            if marker not in allergens: failures.append(f"Edible-allergen guide is missing authority marker: {marker}")
        packaging = (ROOT / "guides/cannabis-child-resistant-packaging-home-storage-guide/index.html").read_text(encoding="utf-8")
        for marker in ('CDC: Cannabis and Poisoning', 'U.S. CPSC: Poison Prevention Packaging Act Guidance', 'New York OCM: Part 128 Packaging and Labeling Guidance', 'Make the package-to-lock record'):
            if marker not in packaging: failures.append(f"Packaging guide is missing authority marker: {marker}")
        battery = (ROOT / "gear/510-thread-vape-battery-safety/index.html").read_text(encoding="utf-8")
        for marker in ('Build the cartridge–battery–charger record', 'U.S. CPSC: Recalls', 'U.S. EPA: Used Lithium-Ion Batteries', 'Will any 510 cartridge work with any 510 battery?'):
            if marker not in battery: failures.append(f"Battery guide is missing expanded marker: {marker}")
        stem_cell = (ROOT / "strains/stem-cell-cbg/index.html").read_text(encoding="utf-8")
        for marker in ('IMAGE WITHHELD', 'Oregon CBD: Cultivar Catalog', 'USDA AMS: Hemp Laboratory Testing Guidelines', 'Read CBG and CBGA as separate rows', 'Build the five-layer Stem Cell evidence chain', 'Use a lot record before a reputation', 'Check which evidence layers are actually present', 'data-cbg-evidence', 'data-cbg-progress'):
            if marker not in stem_cell: failures.append(f"Stem Cell CBG field note is missing authority marker: {marker}")
        flower = (ROOT / "guides/flower/index.html").read_text(encoding="utf-8")
        for marker in ('Run the twelve-point checkout screen', 'Keep the menu, package, and lot report as three records', 'New York OCM: Cannabis Laboratories', 'No affiliate link or approved tracking ID is configured', 'Price the whole flower system'):
            if marker not in flower: failures.append(f"Flower checklist is missing authority marker: {marker}")
        cancer_claims = (ROOT / "guides/cannabis-cbd-cancer-claims-evidence-guide/index.html").read_text(encoding="utf-8")
        for marker in ('National Cancer Institute: Cannabis and Cannabinoids', 'FDA: Health Fraud Product Database', 'Build the oncology conversation record', 'Run a ten-question cancer-claim screen', 'cannabis-claim-fact-check-worksheet/'):
            if marker not in cancer_claims: failures.append(f"Cancer-claims guide is missing authority marker: {marker}")
        claim_check = (ROOT / "guides/cannabis-claim-fact-check-worksheet/index.html").read_text(encoding="utf-8")
        for marker in ('FTC: Health Products Compliance Guidance', 'FDA: What to Know About Cannabis and CBD Products', 'NIH NCCIH: Cannabis and Cannabinoids', 'Run the nine-part evidence-transfer check', 'Use the one-page claim audit record'):
            if marker not in claim_check: failures.append(f"Claim fact-check worksheet is missing authority marker: {marker}")
        edibles = (ROOT / "guides/edibles/index.html").read_text(encoding="utf-8")
        for marker in ('Run the ten-gate checkout screen', 'New York OCM: Consumers', 'Keep the listing, package, receipt, and lot report separate', 'No brand, seller, product, price, discount, review score, or affiliate link appears'):
            if marker not in edibles: failures.append(f"Expanded edible guide is missing authority marker: {marker}")
        lockbox = (ROOT / "gear/smell-proof-storage/index.html").read_text(encoding="utf-8")
        for marker in ('data-lockbox-comparison', 'data-lock-load-width', 'data-lock-fit', 'data-lock-volume', 'data-lock-unit-cost', 'Math check:'):
            if marker not in lockbox: failures.append(f"Lockbox comparison is missing marker: {marker}")
        if lockbox.count('href="../../guides/cannabis-child-resistant-packaging-home-storage-guide/"') != 1:
            failures.append("Lockbox comparison has a missing or duplicated child-safety related link")
        pet_exposure = (ROOT / "guides/cannabis-and-pets-accidental-exposure/index.html").read_text(encoding="utf-8")
        for marker in ('The no-delay response card', 'Build one exposure handoff record', 'Track the case without running an experiment', 'ASPCA Animal Poison Control Center', 'Merck Veterinary Manual: THC Toxicosis'):
            if marker not in pet_exposure: failures.append(f"Pet exposure action guide is missing authority marker: {marker}")
        stash_jar = (ROOT / "gear/cannabis-stash-jar-buying-guide/index.html").read_text(encoding="utf-8")
        for marker in ('data-stash-jar-planner', 'data-jar-diameter', 'data-jar-working', 'data-jar-total', 'Math check:', 'New York OCM: Cannabis Storage Guide'):
            if marker not in stash_jar: failures.append(f"Stash-jar planner is missing marker: {marker}")
        disposal = (ROOT / "guides/cannabis-product-disposal-decision-guide/index.html").read_text(encoding="utf-8")
        for marker in ('Run the stop-before-disposal gate', 'Use the format-first disposal map', 'Copy the disposal handoff card', 'U.S. EPA: Used Lithium-Ion Batteries', 'Connecticut Cannabis: Safe Disposal'):
            if marker not in disposal: failures.append(f"Cannabis disposal guide is missing authority marker: {marker}")
        loyalty = (ROOT / "guides/cannabis-dispensary-loyalty-rewards-value-privacy-guide/index.html").read_text(encoding="utf-8")
        for marker in ('data-loyalty-value', 'data-loyalty-spend', 'data-loyalty-net', 'data-loyalty-break-even', 'New York OCM: Adopted Parts 128 and 129', 'Math check:'):
            if marker not in loyalty: failures.append(f"Cannabis loyalty guide is missing value or authority marker: {marker}")
        chronic_pain = (ROOT / "guides/cannabis-cbd-chronic-pain-evidence-guide/index.html").read_text(encoding="utf-8")
        for marker in ('CDC: Cannabis and Chronic Pain', 'AHRQ: Living Systematic Review—2025 Update', 'Build a clinician-ready pain, function, and product record', 'Do not turn population headlines into an opioid plan'):
            if marker not in chronic_pain: failures.append(f"Chronic-pain guide is missing authority marker: {marker}")
        tray = (ROOT / "gear/cannabis-rolling-tray-buying-guide/index.html").read_text(encoding="utf-8")
        for marker in ('data-tray-comparison', 'data-tray-task-width', 'data-tray-store-fit', 'data-tray-unit-cost', 'Math check:'):
            if marker not in tray: failures.append(f"Rolling-tray comparison is missing marker: {marker}")
        liver_health = (ROOT / "guides/cannabis-cbd-liver-health-safety-guide/index.html").read_text(encoding="utf-8")
        for marker in ('FDA: CBD Safety in a Randomized Trial', 'DailyMed: Current Epidiolex Label', 'Build one liver, medicine, and product record', 'Run the liver-claim stop screen'):
            if marker not in liver_health: failures.append(f"Liver-health guide is missing authority marker: {marker}")
        humidity = (ROOT / "gear/cannabis-humidity-pack-hygrometer-guide/index.html").read_text(encoding="utf-8")
        for marker in ('data-humidity-comparison', 'data-humidity-pack-cost', 'data-humidity-first', 'data-humidity-total', 'Math check:'):
            if marker not in humidity: failures.append(f"Humidity-system comparison is missing marker: {marker}")
        cbd_drinks = (ROOT / "guides/cbd-drinks-powders-label-buying-guide/index.html").read_text(encoding="utf-8")
        for marker in ('FDA: WHAT TO KNOW ABOUT CANNABIS AND CBD PRODUCTS', 'NIH NCCIH: CANNABIS AND CANNABINOIDS', 'CBD PACKAGE TOTAL', 'PACKAGE-TO-GLASS'):
            if marker not in cbd_drinks.upper(): failures.append(f"CBD drinks guide is missing authority marker: {marker}")
        grow_light = (ROOT / "gear/indoor-cannabis-grow-light-buying-cost-planner/index.html").read_text(encoding="utf-8")
        for marker in ('data-grow-light-comparison', 'data-grow-watts', 'data-grow-electricity', 'aria-live="polite"'):
            if marker not in grow_light: failures.append(f"Grow-light planner is missing marker: {marker}")
        older_adult = (ROOT / "guides/cannabis-older-adults-medication-fall-safety/index.html").read_text(encoding="utf-8")
        for marker in ('class="article-actions"', 'National Center for Complementary and Integrative Health'):
            if marker not in older_adult: failures.append(f"Older-adult guide is missing marker: {marker}")
        lung = (ROOT / "guides/cannabis-smoke-vape-lung-health-guide/index.html").read_text(encoding="utf-8")
        for marker in ('CDC: Cannabis and Lung Health', 'NIH/NIDA: Cannabis (Marijuana)', 'EPA: Secondhand Marijuana Smoke'):
            if marker not in lung: failures.append(f"Lung-health guide is missing source marker: {marker}")
        preroll = (ROOT / "guides/cannabis-pre-roll-infused-label-buying-guide/index.html").read_text(encoding="utf-8")
        for marker in ('data-preroll-planner', 'data-preroll-price', 'data-preroll-per-gram', 'aria-live="polite"'):
            if marker not in preroll: failures.append(f"Pre-roll worksheet is missing marker: {marker}")
        glossary = (ROOT / "guides/cannabis-terms-label-lab-glossary/index.html").read_text(encoding="utf-8")
        if glossary.count('data-glossary-term') != 48:
            failures.append("Glossary does not contain exactly 48 searchable terms")
        for marker in ('data-glossary-search', 'data-glossary-count', 'data-glossary-empty'):
            if marker not in glossary: failures.append(f"Glossary is missing marker: {marker}")
        mental_health = (ROOT / "guides/cannabis-anxiety-paranoia-psychosis-warning-signs/index.html").read_text(encoding="utf-8")
        for marker in ('CDC: Cannabis and Mental Health', 'SAMHSA: Cannabis Use Disorder in Primary Care', '988 Suicide &amp; Crisis Lifeline', 'SYMPTOM'):
            if marker not in mental_health: failures.append(f"Mental-health guide is missing marker: {marker}")
        comparison = (ROOT / "guides/cannabis-product-price-label-comparison-calculator/index.html").read_text(encoding="utf-8")
        for marker in ('data-package-comparison', 'data-compare-price', 'data-compare-per-unit', 'data-compare-per-quantity', 'data-compare-per-100', 'data-compare-reset'):
            if marker not in comparison: failures.append(f"Package comparison calculator is missing marker: {marker}")
        basics = (ROOT / "guides/cannabis-101/index.html").read_text(encoding="utf-8")
        for marker in ('CDC: About Cannabis', 'Build a first-purchase evidence card', 'Keep five label bases separate', 'Finish with storage and a response route'):
            if marker not in basics: failures.append(f"Cannabis 101 guide is missing authority marker: {marker}")
        gear_comparison = (ROOT / "gear/cannabis-gear-comparison-worksheet/index.html").read_text(encoding="utf-8")
        for marker in ('data-gear-cost-comparison', 'data-gear-price', 'data-gear-total', 'data-gear-per-use', 'Math check:'):
            if marker not in gear_comparison: failures.append(f"Gear comparison calculator is missing marker: {marker}")
        edible_math = (ROOT / "guides/cannabis-edible-label-math-checker/index.html").read_text(encoding="utf-8")
        for marker in ('data-edible-math', 'data-edible-thc-serving', 'data-edible-thc-unit', 'data-edible-status', 'data-edible-reset'):
            if marker not in edible_math: failures.append(f"Edible label math checker is missing marker: {marker}")
        vaporizer = (ROOT / "gear/dry-herb-vaporizer-buying-safety-guide/index.html").read_text(encoding="utf-8")
        for marker in ('data-vaporizer-cost', 'data-vape-device', 'data-vape-total', 'data-vape-recurring', 'CPSC: Recalls'):
            if marker not in vaporizer: failures.append(f"Dry-herb cost guide is missing marker: {marker}")
        oral_health = (ROOT / "guides/cannabis-dry-mouth-dental-oral-health-guide/index.html").read_text(encoding="utf-8")
        for marker in ('American Dental Association: Cannabis—Oral Health Effects', 'NIH/NIDCR: Dry Mouth', 'Do not arrive intoxicated', 'SYMPTOM'):
            if marker not in oral_health: failures.append(f"Oral-health guide is missing marker: {marker}")
        grinder = (ROOT / "gear/grinders/index.html").read_text(encoding="utf-8")
        for marker in ('data-grinder-cost', 'data-grinder-price', 'data-grinder-total', 'data-grinder-hours', 'FTC: Warranties', 'No grinder was purchased'):
            if marker not in grinder: failures.append(f"Grinder guide is missing marker: {marker}")
        eye_health = (ROOT / "guides/cannabis-glaucoma-eye-pressure-vision-guide/index.html").read_text(encoding="utf-8")
        for marker in ('NIH/National Eye Institute: Glaucoma and Marijuana Use', 'Start with the urgent-vision gate', 'Build one eye, product, and medicine record', 'temporary change in eye pressure'):
            if marker not in eye_health: failures.append(f"Eye-health guide is missing marker: {marker}")
        air_cleaner = (ROOT / "gear/air-purifier-cannabis-smoke-odor-guide/index.html").read_text(encoding="utf-8")
        for marker in ('data-air-cleaner-planner', 'data-air-cadr', 'data-air-needed', 'data-air-ach', 'data-air-total', 'Math check:'):
            if marker not in air_cleaner: failures.append(f"Air-cleaner planner is missing marker: {marker}")
        epilepsy = (ROOT / "guides/cannabis-cbd-epilepsy-seizure-care-guide/index.html").read_text(encoding="utf-8")
        for marker in ('CDC: First Aid for Seizures', 'Current Epidiolex Prescribing Information', 'Same molecule does not mean same medicine', 'Build one seizure, medicine, and product record'):
            if marker not in epilepsy: failures.append(f"Epilepsy and seizure-care guide is missing marker: {marker}")
        cleaning = (ROOT / "gear/cannabis-tool-cleaning-kit/index.html").read_text(encoding="utf-8")
        for marker in ('data-cleaning-cost', 'data-cleaning-cycle', 'data-cleaning-total', 'Run the eight-gate checkout screen', 'Math check:'):
            if marker not in cleaning: failures.append(f"Cleaning-kit planner is missing marker: {marker}")
        home_grow_ipm = (ROOT / "guides/new-york-home-cannabis-pest-mold-ipm-guide/index.html").read_text(encoding="utf-8")
        for marker in ('New York OCM: Home Cultivation FAQs', 'U.S. EPA: Integrated Pest Management Principles', 'U.S. EPA: Introduction to Pesticide Labels', 'U.S. EPA: Why Mold Is Growing in a Home', 'Use the IPM decision ladder', 'Run the pesticide-label stop gate'):
            if marker not in home_grow_ipm: failures.append(f"New York home-grow IPM guide is missing marker: {marker}")
        digital_scale = (ROOT / "gear/digital-scale-buying-calibration-guide/index.html").read_text(encoding="utf-8")
        for marker in ('data-scale-check', 'data-scale-reference', 'data-scale-reading', 'data-scale-tolerance-result', 'data-scale-total', 'Math check:'):
            if marker not in digital_scale: failures.append(f"Digital-scale planner is missing marker: {marker}")
        policy = (ROOT / "editorial-policy/index.html").read_text(encoding="utf-8")
        if "Publishing integrity" not in policy or "committed SHA-256 checksum" not in policy:
            failures.append("Editorial policy is missing the source synchronization standard")
        if "Link and section integrity" not in policy or "#section" not in policy:
            failures.append("Editorial policy is missing the URL-fragment validation standard")
        if "Structured-data identity" not in policy or "separate, stable identifiers" not in policy:
            failures.append("Editorial policy is missing the structured-data identity standard")
        if "CSS delivery integrity" not in policy or "render-blocking" not in policy:
            failures.append("Editorial policy is missing the CSS delivery standard")
        if "Breadcrumb identity" not in policy or "BreadcrumbList" not in policy:
            failures.append("Editorial policy is missing the breadcrumb identity standard")
        if "Accessible form defenses" not in policy or "assistive technology" not in policy:
            failures.append("Editorial policy is missing the accessible honeypot standard")
        if "Atom feed authorship" not in policy or "Big Bud Man Editorial Team" not in (ROOT / "feed.xml").read_text(encoding="utf-8"):
            failures.append("Editorial policy or Atom feed is missing the feed authorship standard")
        if "Age-gate focus isolation" not in policy:
            failures.append("Editorial policy is missing the age-gate focus-isolation standard")
        if "Contextual inbound-link floor" not in policy or "October 23, 2026" not in policy:
            failures.append("Editorial policy is missing the contextual inbound-link standard")
        deployed_css = (ROOT / "assets/css/styles.css").read_text(encoding="utf-8")
        if "@import" in deployed_css:
            failures.append("Production styles.css still contains a render-blocking CSS import")
        split_css = sorted((ROOT / "assets/css").glob("styles-*.css"))
        if split_css:
            failures.append("Production still contains split stylesheets: " + ", ".join(path.name for path in split_css))
        alcohol = (ROOT / "guides/cannabis-and-alcohol-mixing-risks/index.html").read_text(encoding="utf-8")
        for marker in ("Build the two-substance handoff record", "NIAAA: Alcohol Overdose", 'class="note-template"', "No reliable sober shortcut"):
            if marker not in alcohol: failures.append(f"Alcohol safety guide is missing authority marker: {marker}")
        grow_light = (ROOT / "gear/indoor-cannabis-grow-light-buying-cost-planner/index.html").read_text(encoding="utf-8")
        for marker in ("data-grow-light-comparison", "data-grow-price", "data-grow-electricity", "data-grow-total", "2,176.80"):
            if marker not in grow_light: failures.append(f"Grow-light comparison is missing calculator marker: {marker}")
        vape = (ROOT / "guides/vapes/index.html").read_text(encoding="utf-8")
        for marker in ("oil plus hardware", "Archived EVALI Investigation", "Keep one vape product-and-device record", "cannabis-vape-battery-cartridge-disposal-guide/"):
            if marker not in vape: failures.append(f"Expanded vape guide is missing marker: {marker}")
        returns = (ROOT / "gear/cannabis-accessory-return-warranty-recall-guide/index.html").read_text(encoding="utf-8")
        for marker in ("data-return-deadline", "data-return-purchase", "data-return-end", "FTC: Warranties", "SaferProducts.gov", "November 12, 2026"):
            if marker not in returns: failures.append(f"Accessory return guide is missing marker: {marker}")
        for marker in ("bbm-saved-reading-v1", "renderSaved", "[data-saved-clear]", "data-saved-copy", "data-saved-remove", "data-copy-citation", "Article citation copied.", "data-copy-checklists", "Article checklists copied", "data-paper-comparison", "renderPaperComparison", "data-paper-unit", "data-lockbox-comparison", "renderLockboxComparison", "data-lock-fit", "data-lock-unit-cost", "data-stash-jar-planner", "renderStashJar", "data-jar-working", "data-jar-total", "data-loyalty-value", "renderLoyaltyValue", "data-loyalty-net", "data-loyalty-break-even", "data-tray-comparison", "renderTrayComparison", "data-tray-task-fit", "data-tray-store-fit", "data-tray-unit-cost", "data-humidity-comparison", "renderHumidityComparison", "data-humidity-first", "data-humidity-total", "data-scale-check", "renderScaleCheck", "data-scale-tolerance-result", "data-cleaning-cost", "renderCleaningCost", "data-cleaning-cycle", "data-grow-light-comparison", "renderGrowComparison", "data-grow-electricity", "data-grow-total", "data-preroll-planner", "renderPreroll", "data-glossary", "renderGlossary", "setActiveToggle", "data-package-comparison", "renderComparison", "data-edible-math", "renderEdibleMath", "data-vaporizer-cost", "renderVaporizerCost", "data-grinder-cost", "renderGrinderCost", "data-air-cleaner-planner", "renderAirCleaner", "data-air-needed", "data-gear-cost-comparison", "renderGearCostComparison", "data-gear-per-use", "data-return-deadline", "renderReturnDeadline", "addMonthsClamped", "data-cbg-evidence", "renderCbgEvidence", "data-cbg-layer", "routes.mental", "routes.compare"):
            if marker not in app: failures.append(f"Site JavaScript is missing saved-reading or calculator marker: {marker}")
        if '"url":"/updates/"' not in search_raw:
            failures.append("Search index is missing publication updates")
        if '"url":"/site-index/"' not in search_raw:
            failures.append("Search index is missing the complete site index")
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        if "https://bigbudman.com/sitemap.xml" not in robots or "https://bigbudman.com/site-index/" not in robots or "https://bigbudman.com/updates/" not in robots:
            failures.append("robots.txt does not expose all crawl-discovery surfaces")
        if (ROOT / "index.php").read_text(encoding="utf-8") != (ROOT / "sitemap.xml").read_text(encoding="utf-8"):
            failures.append("Legacy Search Console sitemap endpoint does not mirror the canonical sitemap")
        if "site-index/" not in home:
            failures.append("Footer does not link to the complete site index")
        if "updates/" not in home or "feed.xml" not in home:
            failures.append("Footer does not link to publication updates and the Atom feed")
        atom = ET.parse(ROOT / "feed.xml").getroot()
        atom_ns = {"a":"http://www.w3.org/2005/Atom"}
        if atom.findtext("a:author/a:name", namespaces=atom_ns) != "Big Bud Man Editorial Team":
            failures.append("Atom feed is missing the editorial author name")
        if atom.findtext("a:author/a:uri", namespaces=atom_ns) != "https://bigbudman.com/about/":
            failures.append("Atom feed is missing the canonical editorial author URI")
        feed_links = {(link.get("rel", "alternate"), link.get("href")) for link in atom.findall("a:link", atom_ns)}
        if ("self", "https://bigbudman.com/feed.xml") not in feed_links or ("alternate", "https://bigbudman.com/") not in feed_links:
            failures.append("Atom feed is missing its canonical self or site link")
        entries = atom.findall("a:entry", atom_ns)
        if not entries or len(entries) > 30:
            failures.append(f"Atom feed has an invalid entry count: {len(entries)}")
        entry_dates = [entry.findtext("a:updated", namespaces=atom_ns) for entry in entries]
        if atom.findtext("a:updated", namespaces=atom_ns) != max(entry_dates):
            failures.append("Atom feed timestamp does not match its newest entry")
        for entry in entries:
            required = ("title", "id", "updated", "published", "summary")
            if any(not entry.findtext(f"a:{name}", namespaces=atom_ns) for name in required):
                failures.append("Atom feed contains an entry missing required publication metadata")
                break
            link = entry.find("a:link", atom_ns)
            if link is None or not (link.get("href") or "").startswith("https://bigbudman.com/"):
                failures.append("Atom feed contains an entry without a canonical Big Bud Man link")
                break
    except Exception as exc:
        failures.append(f"Invalid discovery surfaces: {exc}")

    if failures:
        print("STATIC SITE AUDIT: FAIL")
        for failure in failures: print(" -", failure)
        return 1
    print(f"STATIC SITE AUDIT: PASS — {len(html_files)} pages, {len(titles)} unique titles, 50 state law guides, and all local references valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
