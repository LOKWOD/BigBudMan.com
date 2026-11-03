#!/usr/bin/env python3
"""Verify that the deployed discovery surfaces match the audited release."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = "https://bigbudman.com/"
USER_AGENT = "BigBudMan-Live-Release-Audit/1.0"
CANONICAL_RE = re.compile(
    r'<link\b(?=[^>]*\brel=["\']canonical["\'])(?=[^>]*\bhref=["\']([^"\']+)["\'])[^>]*>',
    re.IGNORECASE,
)


def request(url: str, timeout: int) -> tuple[bytes, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/xml,text/html,application/json,text/plain;q=0.8,*/*;q=0.5",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"{url}: expected HTTP 200, received {response.status}")
        return response.read(), response.headers.get("Content-Type", "")


def sitemap_records(payload: bytes, label: str) -> list[tuple[str, str]]:
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        raise RuntimeError(f"{label}: invalid XML: {exc}") from exc
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    records = []
    for node in root.findall("sm:url", namespace):
        loc = node.findtext("sm:loc", default="", namespaces=namespace).strip()
        lastmod = node.findtext("sm:lastmod", default="", namespaces=namespace).strip()
        if not loc or not lastmod:
            raise RuntimeError(f"{label}: every URL needs loc and lastmod")
        records.append((loc, lastmod))
    if not records:
        raise RuntimeError(f"{label}: no canonical URL records found")
    return records


def verify_once(base_url: str, timeout: int) -> str:
    expected_manifest = json.loads((ROOT / "publication-manifest.json").read_text(encoding="utf-8"))
    live_manifest_bytes, manifest_type = request(urljoin(base_url, "publication-manifest.json"), timeout)
    if "json" not in manifest_type.lower():
        raise RuntimeError(f"publication manifest: expected JSON content type, received {manifest_type!r}")
    try:
        live_manifest = json.loads(live_manifest_bytes)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"publication manifest: invalid live JSON: {exc}") from exc
    if live_manifest != expected_manifest:
        raise RuntimeError("publication manifest: live payload does not match the checked-in release")

    expected_sitemap = (ROOT / "sitemap.xml").read_bytes()
    live_sitemap, sitemap_type = request(urljoin(base_url, "sitemap.xml"), timeout)
    if "xml" not in sitemap_type.lower():
        raise RuntimeError(f"canonical sitemap: expected XML content type, received {sitemap_type!r}")
    expected_records = sitemap_records(expected_sitemap, "checked-in sitemap")
    live_records = sitemap_records(live_sitemap, "live canonical sitemap")
    if live_records != expected_records:
        raise RuntimeError("canonical sitemap: live URL/lastmod records do not match the checked-in release")

    robots_bytes, robots_type = request(urljoin(base_url, "robots.txt"), timeout)
    if not any(token in robots_type.lower() for token in ("text/plain", "text/")):
        raise RuntimeError(f"robots.txt: expected text content type, received {robots_type!r}")
    robots = robots_bytes.decode("utf-8")
    canonical_sitemap = f"Sitemap: {urljoin(DEFAULT_BASE, 'sitemap.xml')}"
    if robots.count(canonical_sitemap) != 1:
        raise RuntimeError("robots.txt: canonical sitemap declaration is missing or duplicated")

    checked = 0
    for url, expected_date in expected_manifest["freshness_surfaces"].items():
        parsed = urlsplit(url)
        path_url = urljoin(base_url, parsed.path.lstrip("/"))
        body, content_type = request(path_url, timeout)
        if "html" not in content_type.lower():
            raise RuntimeError(f"{url}: expected HTML content type, received {content_type!r}")
        html = body.decode("utf-8")
        canonical_match = CANONICAL_RE.search(html)
        expected_canonical = urljoin(DEFAULT_BASE, parsed.path.lstrip("/"))
        if not canonical_match or canonical_match.group(1) != expected_canonical:
            actual = canonical_match.group(1) if canonical_match else "missing"
            raise RuntimeError(f"{url}: canonical mismatch ({actual!r})")
        if expected_date not in html:
            raise RuntimeError(f"{url}: freshness date {expected_date} is not visible in the live HTML")
        checked += 1

    return f"manifest, robots, {len(live_records)} sitemap URLs, and {checked} freshness surfaces"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--interval", type=int, default=15)
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()
    if args.attempts < 1 or args.interval < 0 or args.timeout < 1:
        parser.error("attempts and timeout must be positive; interval cannot be negative")

    base_url = args.base_url.rstrip("/") + "/"
    last_error: Exception | None = None
    for attempt in range(1, args.attempts + 1):
        try:
            summary = verify_once(base_url, args.timeout)
        except (RuntimeError, UnicodeDecodeError, urllib.error.URLError) as exc:
            last_error = exc
            print(f"LIVE DISCOVERY AUDIT: attempt {attempt}/{args.attempts} pending — {exc}", flush=True)
            if attempt < args.attempts:
                time.sleep(args.interval)
            continue
        print(f"LIVE DISCOVERY AUDIT: PASS — {summary}")
        return 0
    print(f"LIVE DISCOVERY AUDIT: FAIL — {last_error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
