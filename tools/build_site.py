#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from shutil import copy2, copytree, rmtree
from html import escape
from datetime import datetime
import json

from site_core import (
    Page, DOMAIN, CONTACT_EMAIL, OCM, OCM_VERIFY, article_main, breadcrumbs,
    clean_text, footer, header, head, icon, layout, local, prefix_for, render_article,
    render_standard, search_dialog, age_gate, optimize_images, write_svg_assets, write_text,
)
from content_guides import GUIDE_PAGES
from content_strains import CANNABINOID_LABELS, STRAINS, STRAIN_PAGES
from content_other import OTHER_ARTICLES, STANDARD_PAGES
from content_daily import DAILY_GEAR, DAILY_GUIDES
from content_sep26 import DAILY_GEAR as SEP26_GEAR, DAILY_GUIDES as SEP26_GUIDES
from content_sep27 import DAILY_GEAR as SEP27_GEAR, DAILY_GUIDES as SEP27_GUIDES
from content_sep28 import DAILY_GEAR as SEP28_GEAR, DAILY_GUIDES as SEP28_GUIDES
from content_sep29 import DAILY_GEAR as SEP29_GEAR, DAILY_GUIDES as SEP29_GUIDES
from content_sep30 import DAILY_GEAR as SEP30_GEAR, DAILY_GUIDES as SEP30_GUIDES
from content_oct1 import DAILY_GEAR as OCT1_GEAR, DAILY_GUIDES as OCT1_GUIDES
from content_oct2 import DAILY_GEAR as OCT2_GEAR, DAILY_GUIDES as OCT2_GUIDES
from content_oct3 import DAILY_GUIDES as OCT3_GUIDES, GEAR_OVERRIDES as OCT3_GEAR_OVERRIDES
from content_oct4 import DAILY_GUIDES as OCT4_GUIDES, GEAR_OVERRIDES as OCT4_GEAR_OVERRIDES
from content_oct5 import DAILY_GUIDES as OCT5_GUIDES, GEAR_OVERRIDES as OCT5_GEAR_OVERRIDES
from content_oct6 import DAILY_GUIDES as OCT6_GUIDES, GEAR_OVERRIDES as OCT6_GEAR_OVERRIDES
from content_oct7 import DAILY_GUIDES as OCT7_GUIDES, GEAR_OVERRIDES as OCT7_GEAR_OVERRIDES
from content_oct8 import DAILY_GUIDES as OCT8_GUIDES, GEAR_OVERRIDES as OCT8_GEAR_OVERRIDES, STRAIN_OVERRIDES as OCT8_STRAIN_OVERRIDES
from content_oct9 import DAILY_GUIDES as OCT9_GUIDES, GEAR_OVERRIDES as OCT9_GEAR_OVERRIDES
from content_oct10 import DAILY_GUIDES as OCT10_GUIDES, GEAR_OVERRIDES as OCT10_GEAR_OVERRIDES
from content_oct11 import DAILY_GUIDES as OCT11_GUIDES, GUIDE_OVERRIDES as OCT11_GUIDE_OVERRIDES, GEAR_OVERRIDES as OCT11_GEAR_OVERRIDES
from content_oct12 import GUIDE_OVERRIDES as OCT12_GUIDE_OVERRIDES, GEAR_OVERRIDES as OCT12_GEAR_OVERRIDES
from content_oct13 import GUIDE_OVERRIDES as OCT13_GUIDE_OVERRIDES, NEW_GEAR as OCT13_GEAR
from content_oct14 import GUIDE_OVERRIDES as OCT14_GUIDE_OVERRIDES, GEAR_OVERRIDES as OCT14_GEAR_OVERRIDES
from content_oct15 import GUIDE_OVERRIDES as OCT15_GUIDE_OVERRIDES, STRAIN_OVERRIDES as OCT15_STRAIN_OVERRIDES
from content_oct15_new import NEW_GUIDES as OCT15_NEW_GUIDES, NEW_GEAR as OCT15_NEW_GEAR
from content_oct16 import GUIDE_OVERRIDES as OCT16_GUIDE_OVERRIDES, NEW_GUIDES as OCT16_NEW_GUIDES
from content_oct17 import GUIDE_OVERRIDES as OCT17_GUIDE_OVERRIDES, NEW_GEAR as OCT17_GEAR
from content_oct18 import GUIDE_OVERRIDES as OCT18_GUIDE_OVERRIDES, GEAR_OVERRIDES as OCT18_GEAR_OVERRIDES
from content_oct19 import GUIDE_OVERRIDES as OCT19_GUIDE_OVERRIDES, GEAR_OVERRIDES as OCT19_GEAR_OVERRIDES
from content_oct20 import GUIDE_OVERRIDES as OCT20_GUIDE_OVERRIDES
from content_oct21 import GUIDE_OVERRIDES as OCT21_GUIDE_OVERRIDES, GEAR_OVERRIDES as OCT21_GEAR_OVERRIDES
from content_oct22 import GUIDE_OVERRIDES as OCT22_GUIDE_OVERRIDES, NEW_GUIDES as OCT22_NEW_GUIDES
from content_oct23 import GUIDE_OVERRIDES as OCT23_GUIDE_OVERRIDES, GEAR_OVERRIDES as OCT23_GEAR_OVERRIDES, NEW_GEAR as OCT23_GEAR, NEW_GUIDES as OCT23_GUIDES
from content_state_laws import DEA_SOURCE, NCSL_SOURCE, REVIEW_DATE, STATE_LAWS, STATUS_DESCRIPTIONS, STATUS_LABELS

SOURCE = Path(__file__).resolve().parents[1]
OUT = SOURCE / "_site"

# Daily additions live in a small source module so the evergreen catalog files
# remain readable. They join the same build, search, sitemap, feed, and audit
# paths as every established article.
GUIDE_PAGES = GUIDE_PAGES + DAILY_GUIDES + SEP26_GUIDES + SEP27_GUIDES + SEP28_GUIDES + SEP29_GUIDES + SEP30_GUIDES + OCT1_GUIDES + OCT2_GUIDES + OCT3_GUIDES + OCT4_GUIDES + OCT5_GUIDES + OCT6_GUIDES + OCT7_GUIDES + OCT8_GUIDES + OCT9_GUIDES + OCT10_GUIDES + OCT11_GUIDES
_oct11_guides = {item["path"]: item for item in OCT11_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct11_guides.get(item["path"], item) for item in GUIDE_PAGES]
_oct12_guides = {item["path"]: item for item in OCT12_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct12_guides.get(item["path"], item) for item in GUIDE_PAGES]
OTHER_ARTICLES = OTHER_ARTICLES + DAILY_GEAR + SEP26_GEAR + SEP27_GEAR + SEP28_GEAR + SEP29_GEAR + SEP30_GEAR + OCT1_GEAR + OCT2_GEAR
_oct3_gear = {item["path"]: item for item in OCT3_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct3_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct4_gear = {item["path"]: item for item in OCT4_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct4_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct5_gear = {item["path"]: item for item in OCT5_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct5_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct6_gear = {item["path"]: item for item in OCT6_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct6_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct7_gear = {item["path"]: item for item in OCT7_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct7_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct8_gear = {item["path"]: item for item in OCT8_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct8_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct9_gear = {item["path"]: item for item in OCT9_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct9_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct10_gear = {item["path"]: item for item in OCT10_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct10_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct11_gear = {item["path"]: item for item in OCT11_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct11_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct12_gear = {item["path"]: item for item in OCT12_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct12_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct13_guides = {item["path"]: item for item in OCT13_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct13_guides.get(item["path"], item) for item in GUIDE_PAGES]
OTHER_ARTICLES = OTHER_ARTICLES + OCT13_GEAR
_oct14_guides = {item["path"]: item for item in OCT14_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct14_guides.get(item["path"], item) for item in GUIDE_PAGES]
_oct14_gear = {item["path"]: item for item in OCT14_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct14_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct8_strains = {item["path"]: item for item in OCT8_STRAIN_OVERRIDES}
STRAIN_PAGES = [_oct8_strains.get(item["path"], item) for item in STRAIN_PAGES]
_oct15_guides = {item["path"]: item for item in OCT15_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct15_guides.get(item["path"], item) for item in GUIDE_PAGES]
_oct15_strains = {item["path"]: item for item in OCT15_STRAIN_OVERRIDES}
STRAIN_PAGES = [_oct15_strains.get(item["path"], item) for item in STRAIN_PAGES]
GUIDE_PAGES = GUIDE_PAGES + OCT15_NEW_GUIDES
OTHER_ARTICLES = OTHER_ARTICLES + OCT15_NEW_GEAR
_oct16_guides = {item["path"]: item for item in OCT16_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct16_guides.get(item["path"], item) for item in GUIDE_PAGES]
GUIDE_PAGES = GUIDE_PAGES + OCT16_NEW_GUIDES
_oct17_guides = {item["path"]: item for item in OCT17_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct17_guides.get(item["path"], item) for item in GUIDE_PAGES]
OTHER_ARTICLES = OTHER_ARTICLES + OCT17_GEAR
_oct18_guides = {item["path"]: item for item in OCT18_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct18_guides.get(item["path"], item) for item in GUIDE_PAGES]
_oct18_gear = {item["path"]: item for item in OCT18_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct18_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct19_guides = {item["path"]: item for item in OCT19_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct19_guides.get(item["path"], item) for item in GUIDE_PAGES]
_oct19_gear = {item["path"]: item for item in OCT19_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct19_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct20_guides = {item["path"]: item for item in OCT20_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct20_guides.get(item["path"], item) for item in GUIDE_PAGES]
_oct21_guides = {item["path"]: item for item in OCT21_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct21_guides.get(item["path"], item) for item in GUIDE_PAGES]
_oct21_gear = {item["path"]: item for item in OCT21_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct21_gear.get(item["path"], item) for item in OTHER_ARTICLES]
_oct22_guides = {item["path"]: item for item in OCT22_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct22_guides.get(item["path"], item) for item in GUIDE_PAGES] + OCT22_NEW_GUIDES
_oct23_guides = {item["path"]: item for item in OCT23_GUIDE_OVERRIDES}
GUIDE_PAGES = [_oct23_guides.get(item["path"], item) for item in GUIDE_PAGES] + OCT23_GUIDES
_oct23_gear = {item["path"]: item for item in OCT23_GEAR_OVERRIDES}
OTHER_ARTICLES = [_oct23_gear.get(item["path"], item) for item in OTHER_ARTICLES] + OCT23_GEAR

# Publishing integrity is part of the public editorial standard: the source
# archive is checksum-verified and tested before publication.
for _policy in STANDARD_PAGES:
    if _policy["path"] == "editorial-policy/index.html":
        _policy["updated"] = "October 16, 2026"
        _policy["body"] = _policy["body"].replace(
            '<p class="update-line">Policy reviewed August 26, 2026</p>',
            '<p class="update-line">Policy reviewed October 16, 2026</p>',
        ) + '''<h2>Publishing integrity</h2><p>The page generator and source modules are stored in a versioned deployable archive. Automated publication checks verify that archive against its committed SHA-256 checksum, test that it can be read, and stop deployment before extraction when either check fails. The same build then checks unique titles and descriptions, canonical and social metadata, structured data, internal references, sitemap and search coverage, accessible table behavior, responsive safeguards, and the dated publication manifest. Passing automation does not prove a health, legal, laboratory, or product claim; it makes the published source and discovery surfaces reproducible and easier to audit.</p>'''
        _policy["body"] += '''<h2>Link and section integrity</h2><p>Publication checks now validate the destination document and the named section for every local link that contains a URL fragment. This includes same-page jump navigation and links from one article to a specific section of another. A link can no longer pass merely because the file exists while its <code>#section</code> target is missing. The check decodes the fragment, reads the generated destination's IDs, and stops publication on a mismatch.</p>'''
        _policy["body"] += '''<h2>Structured-data identity</h2><p>Every generated page publishes separate, stable identifiers for the organization, website, webpage, and—when present—the article. The webpage identifies the article as its main entity, while the article points back to the webpage that contains it. Automated checks reject duplicate identifiers, missing identity nodes, an article that reuses the webpage identifier, or a broken main-entity relationship. Structured data describes the published page for machines; it does not add evidence, expertise, endorsement, ratings, or claims that readers cannot see.</p>'''
        _policy["body"] += '''<h2>CSS delivery integrity</h2><p>The production build bundles the site's maintained style modules into one deployable stylesheet and removes the development chunks. This prevents the browser from discovering a chain of additional render-blocking <code>@import</code> requests after the first stylesheet arrives. The publication audit rejects a deployed stylesheet that still contains CSS imports or split <code>styles-*.css</code> files. Bundling changes delivery, not the visual rules or editorial content.</p>'''
        _policy["body"] += '''<h2>Breadcrumb identity</h2><p>Every indexable page now includes a machine-readable breadcrumb trail that mirrors its visible collection path: home, the relevant guide, gear, strain, or legal library, and the current page. The trail uses canonical HTTPS URLs and names already visible on the site. Automated checks reject missing, malformed, or noncanonical breadcrumb nodes. Breadcrumb markup describes site organization; it does not add claims, ratings, authorship, or endorsements.</p>'''
        _policy["body"] += '''<h2>Accessible form defenses</h2><p>Spam-trap fields remain outside the keyboard focus order and are also hidden from assistive technology. This prevents a field that is intentionally meaningless to people from being announced as an unexplained form control. Publication checks inspect every deployed honeypot field and stop the build unless both safeguards are present. This changes accessibility semantics without weakening form delivery or collecting additional information.</p>'''
        _policy["updated"] = "October 17, 2026"
        _policy["body"] = _policy["body"].replace(
            '<p class="update-line">Policy reviewed October 16, 2026</p>',
            '<p class="update-line">Policy reviewed October 17, 2026</p>',
        )
        _policy["body"] += '''<h2>Single-stop responsive tables</h2><p>Wide tables are placed inside keyboard-focusable, labeled regions so keyboard users can reach and horizontally scroll them on narrow screens. When an author has already provided that region, the generator does not add a second focus stop to the nested table. Publication checks reject redundant nested focus targets and require the wrapper to expose a named region. This keeps the full table and its semantic rows and columns intact while making the interaction less repetitive.</p>'''
        _policy["updated"] = "October 18, 2026"
        _policy["body"] = _policy["body"].replace(
            '<p class="update-line">Policy reviewed October 17, 2026</p>',
            '<p class="update-line">Policy reviewed October 18, 2026</p>',
        )
        _policy["body"] += '''<h2>Current-page and current-location navigation</h2><p>The breadcrumb identifies the exact page with <code>aria-current="page"</code>. On detail pages, the primary navigation identifies the containing library with <code>aria-current="location"</code> instead of incorrectly claiming that the library hub is the current page. The exact hub continues to use <code>aria-current="page"</code>. Publication checks reject a missing current breadcrumb or a detail page whose collection context is not exposed. This gives assistive technology two accurate levels of orientation without changing URLs or visible labels.</p>'''
        _policy["updated"] = "October 19, 2026"
        _policy["body"] = _policy["body"].replace(
            '<p class="update-line">Policy reviewed October 18, 2026</p>',
            '<p class="update-line">Policy reviewed October 19, 2026</p>',
        )
        _policy["body"] += '''<h2>Atom feed authorship</h2><p>The publication feed carries one explicit editorial author at feed level so every entry inherits a named, linked source identity under the Atom format. The feed remains a machine-readable discovery surface, not proof that an article is correct. Publication checks parse the XML, require the canonical feed and site links, require the editorial author name and About-page URI, and reject entries without the required title, identifier, link, update time, and summary fields.</p>'''
        _policy["updated"] = "October 20, 2026"
        _policy["body"] = _policy["body"].replace(
            '<p class="update-line">Policy reviewed October 19, 2026</p>',
            '<p class="update-line">Policy reviewed October 20, 2026</p>',
        )
        _policy["body"] += '''<h2>Accessible collection filters</h2><p>The guide, gear, strain, and 50-state libraries expose each filter group by name, identify every filter as a button, publish its initial pressed state, and point search, sort, and filter controls to the result collection they change. The live script keeps <code>aria-pressed</code> synchronized with the visible selection and the polite result count announces changes without moving focus. Publication checks reject missing result IDs, unlinked controls, absent initial state, or filter buttons that could submit a surrounding form. These semantics describe the existing interaction; they do not hide results from search engines or create a separate assistive-technology experience.</p>'''
        _policy["updated"] = "October 21, 2026"
        _policy["body"] = _policy["body"].replace(
            '<p class="update-line">Policy reviewed October 20, 2026</p>',
            '<p class="update-line">Policy reviewed October 21, 2026</p>',
        )
        _policy["body"] += '''<h2>Age-gate focus isolation</h2><p>When the adult confirmation is visible, the page outside its modal dialog is removed from the keyboard and assistive-technology interaction path with the browser's inert behavior. Tab and Shift+Tab remain inside the dialog, the question is programmatically described, the declined state receives focus, and admitting an adult restores the page and the prior focus target. Publication checks reject a deployment that loses the isolation, focus loop, described dialog, decline focus, or release path. The confirmation remains a browser-local access prompt; it does not establish identity, location, legal eligibility, or a purchase right.</p>'''
        _policy["updated"] = "October 22, 2026"
        _policy["body"] = _policy["body"].replace(
            '<p class="update-line">Policy reviewed October 21, 2026</p>',
            '<p class="update-line">Policy reviewed October 22, 2026</p>',
        )
        _policy["body"] += '''<h2>Contextual inbound-link floor</h2><p>Every guide and gear detail page must receive links from at least two distinct HTML pages: its complete collection hub and one or more contextual pages. The publication audit builds the generated link graph, ignores the mechanical site index and update log for this check, counts unique source documents rather than repeated links, and stops deployment when a detail page is reachable only through its hub. This protects crawl discovery and reader orientation without manufacturing unrelated links or treating link count as authority.</p>'''
        _policy["updated"] = "October 23, 2026"
        _policy["body"] = _policy["body"].replace(
            '<p class="update-line">Policy reviewed October 22, 2026</p>',
            '<p class="update-line">Policy reviewed October 23, 2026</p>',
        )
        _policy["body"] += '''<h2>Sitemap date integrity</h2><p>The canonical XML sitemap and the legacy Search Console compatibility endpoint must contain the same complete URL and last-modified records. Each date must be valid, must match the page's visible and structured review date, and cannot be later than the current publication batch. The robots directive must name the canonical HTTPS sitemap. Publication checks reject duplicate locations, missing or malformed dates, a legacy payload that drifts from the canonical file, or a page-to-sitemap date mismatch. A last-modified date records a material editorial or publication change; it is not an instruction to rank a page or proof that a search engine has recrawled it.</p>'''

# Keep new reference pages inside established topic clusters. These reciprocal
# links are editorial navigation, not an attempt to manufacture link signals.
RECIPROCAL_RELATED = {
    "guides/full-spectrum-broad-spectrum-cbd-isolate/index.html": [
        ("guides/cbd-drinks-powders-label-buying-guide/", "CBD DRINKS", "Apply spectrum language to a beverage lot"),
        ("guides/cbd-hemp-flower-label-legal-guide/", "HEMP FLOWER", "Verify the package, lot, total THC, and rule"),
        ("guides/cannabis-drug-testing-thc-results-guide/", "TESTING", "Understand CBD and THC test risk"),
    ],
    "guides/cannabis-101/index.html": [
        ("guides/delta-8-thc-label-safety-guide/", "DELTA-8 THC", "Separate intoxicating THC from hemp and CBD framing"),
        ("guides/cannabis-terms-label-lab-glossary/", "GLOSSARY", "Decode 48 cannabis terms"),
    ],
    "guides/read-a-label/index.html": [
        ("guides/cannabis-edible-label-math-checker/", "EDIBLE MATH", "Cross-check serving, unit, and package totals"),
        ("guides/cannabis-edible-allergen-ingredient-label-guide/", "INGREDIENTS + ALLERGENS", "Run the food-safety check before the cannabinoid math"),
        ("guides/cannabis-product-price-label-comparison-calculator/", "PRICE MATH", "Normalize three like-for-like packages"),
        ("guides/cannabis-package-seal-tamper-evidence-checklist/", "PACKAGE CONDITION", "Check the seal, closure, label, lot, and complaint route before opening"),
    ],
    "guides/cbd-gummies-label-buying-guide/index.html": [("guides/cannabis-gummies-drinks-oils-capsules-comparison/", "COMPARE FORMATS", "Compare gummies with drinks, oils, capsules, lozenges, sprays, and powders"),("guides/cannabis-edible-allergen-ingredient-label-guide/", "ALLERGEN CHECK", "Read ingredients and cross-contact language")],
    "guides/cannabis-product-complaint-adverse-event-reporting/index.html": [
        ("guides/cannabis-official-source-directory/", "SOURCE DIRECTORY", "Choose the agency or service that owns each part of the problem"),
        ("guides/delta-8-thc-label-safety-guide/", "DELTA-8 THC", "Preserve the exact cannabinoid, product, lot, and route"),
        ("guides/cannabis-edible-allergen-ingredient-label-guide/", "ALLERGEN RECORD", "Keep the reaction, label, lot, and product problem separate"),
    ],
    "guides/cannabis-beverages-label-timing-buying-guide/index.html": [("guides/cannabis-gummies-drinks-oils-capsules-comparison/", "COMPARE FORMATS", "Keep route, timing, label units, ingredients, and value together"),("guides/cbd-drinks-powders-label-buying-guide/", "CBD FORMAT", "Audit CBD drinks and powders separately from THC beverages")],
    "guides/cbd-oil-tincture-label-buying-guide/index.html": [("guides/cannabis-gummies-drinks-oils-capsules-comparison/", "COMPARE FORMATS", "Compare oil with solid units, drinks, lozenges, sprays, and powders"),("guides/cbd-drinks-powders-label-buying-guide/", "DRINK FORMAT", "Rebuild the serving math for a beverage or powder")],
    "guides/cbd-capsules-softgels-label-buying-guide/index.html": [("guides/cannabis-gummies-drinks-oils-capsules-comparison/", "COMPARE FORMATS", "Compare fixed units with drinks, oils, lozenges, sprays, and powders")],
    "guides/edibles/index.html": [("guides/cannabis-edible-label-math-checker/", "CHECK THE MATH", "Reconcile serving, piece, and package totals"),("guides/cannabis-gummies-drinks-oils-capsules-comparison/", "COMPARE FORMATS", "Compare gummies and other edibles with drinks, oils, capsules, lozenges, sprays, and powders")],
    "guides/vapes/index.html": [
        ("guides/disposable-vape-vs-510-cartridge-comparison/", "DEVICE CHOICE", "Compare an integrated pen with a 510 system"),
        ("guides/cannabis-smoke-vape-lung-health-guide/", "LUNG HEALTH", "Compare smoke, aerosol, and warning signs"),
        ("gear/510-thread-vape-battery-safety/", "BATTERY SAFETY", "Match the cartridge, battery, charger, controls, and recall record"),
    ],
    "guides/flower/index.html": [
        ("guides/cannabis-flower-freshness-package-date-buying-guide/", "FRESHNESS", "Audit dates, seal, lot evidence, condition, and recall status"),
        ("guides/cannabis-pre-roll-infused-label-buying-guide/", "PRE-ROLLS", "Compare plain and infused products"),
    ],
    "guides/cannabis-certificate-of-analysis-coa-guide/index.html": [
        ("guides/cannabis-contaminant-test-results-guide/", "CONTAMINANTS", "Decode pesticide, microbial, metal, solvent, and physical-chemistry panels"),
        ("guides/cannabis-edible-label-math-checker/", "PACKAGE MATH", "Keep label arithmetic separate from lot-level test results"),
        ("guides/cbg-products-label-evidence-guide/", "CBG PRODUCTS", "Keep CBG and CBGA attached to the exact lot and basis"),
    ],
    "guides/cannabis-overconsumption-poisoning-response/index.html": [("guides/cannabis-child-resistant-packaging-home-storage-guide/", "PREVENTION", "Audit the original package, lock, placement, and handoff routine"), ("guides/cannabis-anxiety-paranoia-psychosis-warning-signs/", "MENTAL HEALTH", "Separate fear, paranoia, and psychosis warning signs")],
    "guides/cannabis-smoke-vape-lung-health-guide/index.html": [("gear/air-purifier-cannabis-smoke-odor-guide/", "AIR CLEANER MATH", "Size particle filtration without treating it as source control"), ("guides/cannabis-dry-mouth-dental-oral-health-guide/", "ORAL HEALTH", "Connect route and exposure history to the dental record")],
    "guides/cannabis-older-adults-medication-fall-safety/index.html": [("guides/cannabis-glaucoma-eye-pressure-vision-guide/", "VISION + GLAUCOMA", "Keep eye treatment, measurements, products, and falls in one record"), ("guides/cannabis-dry-mouth-dental-oral-health-guide/", "ORAL HEALTH", "Add medicines, dryness, and dental symptoms to the review")],
    "guides/cannabis-before-surgery-anesthesia/index.html": [("guides/cannabis-dry-mouth-dental-oral-health-guide/", "DENTAL VISITS", "Prepare the exact product, route, and last-use record")],
    "guides/storage/index.html": [("guides/cannabis-child-resistant-packaging-home-storage-guide/", "CHILD RESISTANCE", "Audit the package, lock, placement, and household routine"), ("gear/cannabis-stash-jar-buying-guide/", "SECONDARY JAR", "Measure capacity, headspace, costs, claims, identity, and locked fit"), ("guides/cannabis-and-pets-accidental-exposure/", "PET EXPOSURE", "Prepare the call record and close the access route")],
    "guides/cannabis-and-pets-accidental-exposure/index.html": [("guides/cannabis-child-resistant-packaging-home-storage-guide/", "HOUSEHOLD ACCESS", "Add package and lock layers for children, visitors, and pets")],
    "guides/cbd-products-for-pets-veterinarian-label-guide/index.html": [("guides/cannabis-and-pets-accidental-exposure/", "ACCIDENTAL EXPOSURE", "Call promptly and preserve the exact product, ingredient, and timing record")],
    "gear/smell-proof-storage/index.html": [("gear/cannabis-stash-jar-buying-guide/", "JAR PLANNER", "Measure capacity, headspace, claims, and ownership cost"), ("guides/cannabis-child-resistant-packaging-home-storage-guide/", "PACKAGE + LOCK", "Keep child resistance and household access as separate layers"), ("guides/storage/", "STORAGE SYSTEM", "Match each format to temperature, light, air, moisture, and access controls")],
    "guides/cannabis-tolerance-dependence-withdrawal/index.html": [("guides/cannabis-anxiety-paranoia-psychosis-warning-signs/", "MENTAL HEALTH", "Record recurrent symptoms and functional change")],
    "guides/cannabis-product-recall-batch-checker/index.html": [
        ("guides/cannabis-contaminant-test-results-guide/", "TEST RESULTS", "Read the panel, limit, unit, qualifier, and lot status"),
        ("guides/cannabis-official-source-directory/", "SOURCE DIRECTORY", "Separate recall, regulator, health, accessory, and fraud routes"),
        ("guides/cannabis-product-complaint-adverse-event-reporting/", "REPORT A PROBLEM", "Preserve the evidence and use the right route"),
    ],
    "legal/shop-legal/index.html": [
        ("guides/new-york-cannabis-delivery-online-order-verification-guide/", "DELIVERY", "Verify the license, domain, order, handoff, and receipt"),
        ("guides/cannabis-product-complaint-adverse-event-reporting/", "AFTER PURCHASE", "Report a product, seller, or adverse-event concern"),
    ],
    "gear/510-thread-vape-battery-safety/index.html": [("guides/disposable-vape-vs-510-cartridge-comparison/", "COMPARE SYSTEMS", "Choose between an integrated pen and a reusable battery")],
    "guides/cannabis-cbd-medication-interactions/index.html": [("guides/cannabis-glaucoma-eye-pressure-vision-guide/", "EYE MEDICINES", "Bring drops, products, routes, and last use into the same review")],
    "guides/cannabis-heart-rate-blood-pressure-safety/index.html": [("guides/cannabis-glaucoma-eye-pressure-vision-guide/", "EYE PRESSURE", "Separate blood pressure from intraocular pressure and optic-nerve care")],
    "guides/cbd-topicals-label-buying-guide/index.html": [("guides/cbd-patches-transdermal-label-evidence-guide/", "PATCHES", "Separate the patch format, skin-contact system, lot evidence, and delivery claim")],
    "guides/cannabis-child-resistant-packaging-home-storage-guide/index.html": [("guides/cannabis-package-seal-tamper-evidence-checklist/", "SEAL + TAMPER EVIDENCE", "Inspect the unopened package before the storage routine begins")],
    "guides/secondhand-cannabis-smoke-indoor-air/index.html": [("gear/air-purifier-cannabis-smoke-odor-guide/", "SIZE FILTRATION", "Estimate room CADR, air changes, filters, and ownership cost"), ("guides/cannabis-smoke-vape-lung-health-guide/", "PERSONAL EXPOSURE", "Build a route and symptom record")],
    "gear/cannabis-vape-battery-cartridge-disposal-guide/index.html": [("guides/disposable-vape-vs-510-cartridge-comparison/", "BEFORE PURCHASE", "Include the end-of-life route in the device decision")],
    "strains/auto-cbg/index.html": [("guides/cbg-products-label-evidence-guide/", "CBG PRODUCTS", "Separate the label, lot, evidence, and claims from a cultivar name")],
}

# October 5 strengthens a distinct seizure-care cluster and the product-neutral
# maintenance path without displacing established related reading.
RECIPROCAL_RELATED["guides/cannabis-cbd-medication-interactions/index.html"] = [
    ("guides/cannabis-cbd-epilepsy-seizure-care-guide/", "SEIZURE CARE", "Keep prescription cannabidiol, retail CBD, medicines, monitoring, and first aid separate"),
    ("guides/cannabis-glaucoma-eye-pressure-vision-guide/", "EYE MEDICINES", "Bring drops, products, routes, and last use into the same review"),
]
RECIPROCAL_RELATED["guides/cbd-oil-tincture-label-buying-guide/index.html"] = [
    ("guides/cannabis-cbd-epilepsy-seizure-care-guide/", "PRESCRIPTION BOUNDARY", "Do not treat a retail CBD oil as prescription cannabidiol"),
    ("guides/cannabis-gummies-drinks-oils-capsules-comparison/", "COMPARE FORMATS", "Compare oil with solid units, drinks, lozenges, sprays, and powders"),
]
RECIPROCAL_RELATED["guides/cannabis-official-source-directory/index.html"] = [
    ("guides/cannabis-cbd-epilepsy-seizure-care-guide/", "EPILEPSY + CBD", "Route seizure first aid, medicine labeling, evidence, and product questions correctly"),
]
RECIPROCAL_RELATED["gear/grinders/index.html"] = [
    ("gear/cannabis-tool-cleaning-kit/", "CLEANING COST", "Price compatible brushes, cleaner, parts, and maintenance time"),
]
RECIPROCAL_RELATED["gear/cannabis-glass-pipe-water-pipe-buying-guide/index.html"] = [
    ("gear/cannabis-tool-cleaning-kit/", "CARE ROUTINE", "Build a compatible cleaning kit before buying glassware"),
]
RECIPROCAL_RELATED["gear/cannabis-gear-comparison-worksheet/index.html"] = [
    ("gear/cannabis-tool-cleaning-kit/", "MAINTENANCE COST", "Turn cleaning supplies, replacement parts, and time into ownership cost"),
]
# October 15 corrective publication: three genuinely new, non-overlapping
# pages after the earlier maintenance-only batch. Reciprocal links attach each
# page to an established cluster rather than leaving isolated URLs.
RECIPROCAL_RELATED["strains/stem-cell-cbg/index.html"] = [
    ("guides/cbg-dominant-cannabis-chemotype-guide/", "CBG CHEMOTYPE", "Separate plant chemistry, cultivar provenance, package identity, and lot evidence"),
    ("strains/white-cbg/", "WHITE CBG", "Compare names without transferring identity or chemistry"),
    ("guides/cbg-products-label-evidence-guide/", "CBG PRODUCTS", "Audit the exact label, lot, ingredients, evidence, and claims"),
]
RECIPROCAL_RELATED["guides/cbg-products-label-evidence-guide/index.html"] = [
    ("guides/cbg-dominant-cannabis-chemotype-guide/", "PLANT CHEMISTRY", "Keep chemotype and cultivar evidence separate from the retail product"),
    ("strains/stem-cell-cbg/", "NAMED CULTIVAR", "Apply the evidence chain to Stem Cell CBG"),
    ("guides/cannabis-certificate-of-analysis-coa-guide/", "LOT REPORT", "Match the final product, lot, units, basis, and panel scope"),
]
RECIPROCAL_RELATED["gear/dry-herb-vaporizer-buying-safety-guide/index.html"] = [
    ("gear/dry-herb-vaporizer-dosing-capsule-guide/", "DOSING CAPSULES", "Verify exact-model fit, adapter, care rule, storage, and ownership cost"),
    ("gear/cannabis-tool-cleaning-kit/", "CLEANING", "Match cleaner, contact time, tools, and drying to every material"),
    ("gear/cannabis-accessory-return-warranty-recall-guide/", "AFTER SALE", "Preserve return, warranty, support, and recall routes"),
]
RECIPROCAL_RELATED["guides/cannabis-driving-impairment-sober-timer/index.html"] = [
    ("guides/cannabis-intoxication-impairment-detection/", "TERMS + EVIDENCE", "Keep intoxication, impairment, detection, poisoning, and legal conclusions separate"),
    ("guides/cannabis-and-alcohol-mixing-risks/", "ALCOHOL + CANNABIS", "Keep both exposure clocks visible and remove driving"),
    ("guides/cannabis-overconsumption-poisoning-response/", "URGENT RESPONSE", "Separate supportive care, Poison Control, and 911"),
]
RECIPROCAL_RELATED["guides/cannabis-drug-testing-thc-results-guide/index.html"] = [
    ("guides/cannabis-intoxication-impairment-detection/", "DETECTION BOUNDARY", "Separate a measured analyte from function and the governing rule"),
    ("guides/dot-cannabis-cbd-drug-testing-safety-sensitive-workers/", "DOT RULES", "Use the exact federal safety-sensitive program"),
    ("guides/full-spectrum-broad-spectrum-cbd-isolate/", "CBD LABELS", "Do not turn spectrum language into a testing guarantee"),
]
RECIPROCAL_RELATED["guides/cannabis-cbd-and-sleep/index.html"] = [
    ("guides/cbn-products-label-evidence-guide/", "CBN PRODUCTS", "Audit the label, lot, ingredients and actual human sleep evidence"),
    ("guides/cannabis-cbd-medication-interactions/", "MEDICINES", "Build the complete pharmacist and clinician record"),
    ("guides/cannabis-cbd-liver-health-safety-guide/", "LIVER SAFETY", "Keep products, medicines, alcohol, symptoms and labs together"),
]
RECIPROCAL_RELATED["guides/cannabis-driving-impairment-sober-timer/index.html"] = [
    ("guides/cannabis-social-hosting-guest-safety-plan/", "SOCIAL HOSTING", "Build the sober ride, product control and emergency plan before guests arrive"),
    ("guides/cannabis-overconsumption-poisoning-response/", "URGENT RESPONSE", "Separate supportive care, Poison Control and 911"),
    ("guides/cannabis-exercise-workout-heat-safety/", "EXERCISE + HEAT", "Plan around function, environment and sober transport"),
]
RECIPROCAL_RELATED["legal/flying-with-cannabis-cbd-tsa-rules/index.html"] = [
    ("legal/cannabis-federal-property-rules-guide/", "FEDERAL PROPERTY", "Identify the managing agency, boundary and current rule"),
    ("legal/mailing-cannabis-cbd-usps-rules/", "MAILING", "Check product, documentation, carrier and destination"),
    ("legal/", "STATE LIBRARY", "Check origin and destination rules separately"),
]
# October 6 connects the identification-first home-grow workflow to the
# established planning cluster and the scale worksheet to inventory records.
RECIPROCAL_RELATED["guides/new-york-home-cannabis-grow-planner/index.html"] = [
    ("guides/new-york-home-cannabis-pest-mold-ipm-guide/", "PESTS + MOISTURE", "Build an identification-first scouting and IPM record"),
    ("gear/indoor-cannabis-grow-light-buying-cost-planner/", "LIGHT + LOAD", "Document light coverage, electrical load, and operating cost"),
]
RECIPROCAL_RELATED["gear/indoor-cannabis-grow-light-buying-cost-planner/index.html"] = [
    ("guides/new-york-home-cannabis-pest-mold-ipm-guide/", "GROW-SPACE IPM", "Connect observations to moisture, airflow, and lawful controls"),
]
RECIPROCAL_RELATED["guides/cannabis-contaminant-test-results-guide/index.html"] = [
    ("guides/new-york-home-cannabis-pest-mold-ipm-guide/", "HOME-GROW RECORD", "Keep field observations separate from finished-product laboratory evidence"),
]
RECIPROCAL_RELATED["gear/cannabis-inventory-label-record-kit/index.html"] = [
    ("gear/digital-scale-buying-calibration-guide/", "MEASUREMENT RECORD", "Screen repeatability and keep the scale, tare, unit, and date attached"),
]
# October 15 turns the thin flower overview into a complete purchase-decision
# hub and reinforces the one supported Search Console strain signal.
RECIPROCAL_RELATED["guides/cannabis-flower-freshness-package-date-buying-guide/index.html"] = [
    ("guides/flower/", "FLOWER CHECKOUT", "Run the complete seller, package, lot, condition, storage, and exit screen"),
    ("guides/cannabis-product-recall-batch-checker/", "RECALL CHECK", "Match the exact producer, product, and lot before acting"),
    ("guides/cannabis-certificate-of-analysis-coa-guide/", "LOT REPORT", "Confirm identity, status, units, basis, qualifiers, and panel scope"),
]
RECIPROCAL_RELATED["gear/cannabis-gear-comparison-worksheet/index.html"] = [
    ("guides/flower/", "FLOWER SYSTEM", "Define the storage, preparation, care, and exit job before comparing exact models"),
    ("gear/cannabis-tool-cleaning-kit/", "MAINTENANCE COST", "Turn cleaning supplies, replacement parts, and time into ownership cost"),
]
RECIPROCAL_RELATED["strains/white-cbg/index.html"] = [
    ("strains/stem-cell-cbg/", "STEM CELL CBG", "Compare the evidence chain without transferring identity or chemistry between names"),
    ("guides/cbg-products-label-evidence-guide/", "CBG PRODUCTS", "Separate a cultivar name from the exact retail product and its evidence"),
]
RECIPROCAL_RELATED["strains/auto-cbg/index.html"] = [
    ("strains/stem-cell-cbg/", "STEM CELL CBG", "Keep breeder, producer, package, lot report, and current rule as separate layers"),
    ("guides/cbg-products-label-evidence-guide/", "CBG PRODUCTS", "Separate the label, lot, evidence, and claims from a cultivar name"),
]
# October 7 gives exercise decisions a responsible-use, cardiovascular, and
# transport route, while the paper comparison stays inside the preparation
# cluster instead of creating an isolated commercial page.
RECIPROCAL_RELATED["responsible-use/index.html"] = [
    ("guides/cannabis-exercise-workout-heat-safety/", "EXERCISE + HEAT", "Plan coordination, symptoms, weather, supervision, and a sober trip home"),
]
RECIPROCAL_RELATED["guides/cannabis-heart-rate-blood-pressure-safety/index.html"] = [
    ("guides/cannabis-exercise-workout-heat-safety/", "EXERCISE", "Keep activity, heart symptoms, heat, products, and medicines in one record"),
    ("guides/cannabis-glaucoma-eye-pressure-vision-guide/", "EYE PRESSURE", "Separate blood pressure from intraocular pressure and optic-nerve care"),
]
RECIPROCAL_RELATED["guides/cannabis-driving-impairment-sober-timer/index.html"] = [
    ("guides/cannabis-exercise-workout-heat-safety/", "ACTIVITY + TRANSPORT", "Do not turn a workout, bike, or familiar route into a sobriety test"),
]
RECIPROCAL_RELATED["gear/cannabis-rolling-machine-buying-guide/index.html"] = [
    ("gear/cannabis-rolling-paper-cone-guide/", "PAPER COST + FIT", "Compare dimensions, disclosure, delivered price, and usable count"),
]
RECIPROCAL_RELATED["gear/cannabis-pre-roll-tube-case-buying-guide/index.html"] = [
    ("gear/cannabis-rolling-paper-cone-guide/", "PAPER + CONE", "Carry exact dimensions, condition, and product identity into storage"),
]
# October 8 connects the cancer-claim evidence boundary to medication and
# procedure records, and turns the established storage page into a measurable
# package-fit path without treating geometry as security certification.
RECIPROCAL_RELATED["guides/cannabis-cbd-medication-interactions/index.html"] = [
    ("guides/cannabis-cbd-cancer-claims-evidence-guide/", "CANCER CLAIMS", "Separate treatment, symptom support, interactions, and product evidence"),
    ("guides/cannabis-cbd-epilepsy-seizure-care-guide/", "SEIZURE CARE", "Keep prescription cannabidiol, retail CBD, medicines, monitoring, and first aid separate"),
]
RECIPROCAL_RELATED["guides/cannabis-before-surgery-anesthesia/index.html"] = [
    ("guides/cannabis-cbd-cancer-claims-evidence-guide/", "ONCOLOGY + PROCEDURES", "Bring the exact product, current regimen, last use, and care-team plan together"),
    ("guides/cannabis-dry-mouth-dental-oral-health-guide/", "DENTAL VISITS", "Prepare the exact product, route, and last-use record"),
]
RECIPROCAL_RELATED["guides/cbg-products-label-evidence-guide/index.html"] = [
    ("strains/stem-cell-cbg/", "STEM CELL CBG", "Apply the breeder-to-producer-to-package-to-lot evidence chain"),
]
RECIPROCAL_RELATED["guides/storage/index.html"] = [
    ("gear/smell-proof-storage/", "LOCKBOX FIT", "Compare usable interior dimensions before judging locks and odor claims"),
    ("guides/cannabis-child-resistant-packaging-home-storage-guide/", "CHILD RESISTANCE", "Audit the package, lock, placement, and household routine"),
]
RECIPROCAL_RELATED["legal/shop-legal/index.html"] = [
    ("guides/cannabis-menu-package-receipt-match-checklist/", "MENU → PACKAGE → RECEIPT", "Preserve the complete transaction record before opening the package"),
    ("guides/new-york-cannabis-delivery-online-order-verification-guide/", "DELIVERY + VERIFICATION", "Match the license, website, order, handoff, and receipt"),
]
RECIPROCAL_RELATED["guides/cannabis-product-price-label-comparison-calculator/index.html"] = [
    ("guides/cannabis-menu-package-receipt-match-checklist/", "CHECKOUT RECORD", "Carry the menu claim and final price into the package-and-receipt check"),
]
RECIPROCAL_RELATED["guides/cannabis-product-complaint-adverse-event-reporting/index.html"] = [
    ("guides/cannabis-menu-package-receipt-match-checklist/", "PRESERVE THE TRANSACTION", "Keep menu, cart, package, lot, price, and receipt evidence together"),
    ("guides/delta-8-thc-label-safety-guide/", "DELTA-8 THC", "Separate psychoactive identity, lot evidence, legal context, and help routes"),
    ("guides/cannabis-edible-allergen-ingredient-label-guide/", "ALLERGENS + INGREDIENTS", "Preserve the ingredient panel, cross-contact language, and lot"),
]
# October 9 keeps the chronic-pain evidence record connected to medicine,
# function, topical-claim, and procedure decisions. The tray calculator stays
# inside the existing preparation-and-storage cluster rather than becoming an
# isolated commercial page.
RECIPROCAL_RELATED["guides/cannabis-cbd-medication-interactions/index.html"] = [
    ("guides/cannabis-cbd-chronic-pain-evidence-guide/", "CHRONIC PAIN", "Match the condition, exact product, function, harms, and review plan"),
    ("guides/cannabis-cbd-cancer-claims-evidence-guide/", "CANCER CLAIMS", "Separate treatment, symptom support, interactions, and product evidence"),
]
RECIPROCAL_RELATED["guides/cannabis-older-adults-medication-fall-safety/index.html"] = [
    ("guides/cannabis-cbd-chronic-pain-evidence-guide/", "PAIN + FUNCTION", "Track mobility, alertness, falls, medicines, benefit, and stop rules"),
    ("guides/cannabis-glaucoma-eye-pressure-vision-guide/", "VISION + GLAUCOMA", "Keep eye treatment, measurements, products, and falls in one record"),
]
RECIPROCAL_RELATED["guides/cbd-topicals-label-buying-guide/index.html"] = [
    ("guides/cannabis-cbd-chronic-pain-evidence-guide/", "PAIN CLAIMS", "Do not transfer oral or sublingual evidence to a topical product"),
    ("guides/cbd-patches-transdermal-label-evidence-guide/", "PATCHES", "Separate the patch format, skin-contact system, lot evidence, and delivery claim"),
]
RECIPROCAL_RELATED["gear/cannabis-gear-comparison-worksheet/index.html"] = [
    ("gear/cannabis-rolling-tray-buying-guide/", "TRAY FIT", "Compare task space, hand clearance, storage fit, area, and delivered cost"),
    ("gear/cannabis-tool-cleaning-kit/", "MAINTENANCE COST", "Turn cleaning supplies, replacement parts, and time into ownership cost"),
]
RECIPROCAL_RELATED["gear/smell-proof-storage/index.html"] = [
    ("gear/cannabis-rolling-tray-buying-guide/", "TRAY STORAGE", "Check the complete tray body against the locked interior"),
]
# October 10 makes the liver-health record part of the established medicine,
# prescription-CBD, capsule, and complaint paths. The humidity calculator stays
# inside the storage and model-comparison cluster.
RECIPROCAL_RELATED["guides/cannabis-cbd-medication-interactions/index.html"] = [
    ("guides/cannabis-cbd-liver-health-safety-guide/", "LIVER HEALTH", "Keep products, medicines, alcohol, symptoms, labs, and decisions together"),
    ("guides/cannabis-cbd-cancer-claims-evidence-guide/", "CANCER CLAIMS", "Separate treatment, symptom support, interactions, and product evidence"),
    ("guides/cannabis-cbd-chronic-pain-evidence-guide/", "CHRONIC PAIN", "Match the condition, exact product, function, harms, and review plan"),
]
RECIPROCAL_RELATED["guides/cannabis-cbd-epilepsy-seizure-care-guide/index.html"] = [
    ("guides/cannabis-cbd-liver-health-safety-guide/", "LIVER MONITORING", "Separate prescription cannabidiol monitoring from retail-product uncertainty"),
]
RECIPROCAL_RELATED["guides/cbd-capsules-softgels-label-buying-guide/index.html"] = [
    ("guides/cannabis-cbd-liver-health-safety-guide/", "CBD + LIVER", "Carry the exact product, medicines, symptoms, and laboratory context to the care team"),
]
RECIPROCAL_RELATED["guides/cannabis-product-complaint-adverse-event-reporting/index.html"] = [
    ("guides/cannabis-menu-package-receipt-match-checklist/", "PRESERVE THE TRANSACTION", "Keep menu, cart, package, lot, price, and receipt evidence together"),
    ("guides/delta-8-thc-label-safety-guide/", "DELTA-8 THC", "Separate psychoactive identity, lot evidence, legal context, and help routes"),
    ("guides/cannabis-edible-allergen-ingredient-label-guide/", "ALLERGENS + INGREDIENTS", "Preserve the ingredient panel, cross-contact language, and lot"),
]
RECIPROCAL_RELATED["gear/cannabis-gear-comparison-worksheet/index.html"] = [
    ("gear/cannabis-humidity-pack-hygrometer-guide/", "HUMIDITY SYSTEM", "Compare recurring packs, meters, service, and ownership cost"),
    ("gear/cannabis-rolling-tray-buying-guide/", "TRAY FIT", "Compare task space, hand clearance, storage fit, area, and delivered cost"),
]
# October 11 connects the terpene evidence guide to established label and
# certificate paths and the loupe planner to the neutral model worksheet.
RECIPROCAL_RELATED["guides/cannabis-certificate-of-analysis-coa-guide/index.html"] = [
    ("guides/terpenes/", "TERPENE PANELS", "Keep analyte scope, units, aroma, and effect claims separate"),
    ("guides/cannabis-contaminant-test-results-guide/", "CONTAMINANTS", "Decode pesticide, microbial, metal, solvent, and physical-chemistry panels"),
    ("guides/cannabis-edible-label-math-checker/", "PACKAGE MATH", "Keep label arithmetic separate from lot-level test results"),
]
RECIPROCAL_RELATED["guides/flower/index.html"] = [
    ("guides/terpenes/", "AROMA + EVIDENCE", "Read the exact-batch panel without turning scent into an effect"),
    ("guides/cannabis-flower-freshness-package-date-buying-guide/", "FRESHNESS", "Audit dates, seal, lot evidence, condition, and recall status"),
    ("guides/cannabis-pre-roll-infused-label-buying-guide/", "PRE-ROLLS", "Compare plain and infused products"),
]
RECIPROCAL_RELATED["gear/cannabis-gear-comparison-worksheet/index.html"] = [
    ("gear/cannabis-accessory-return-warranty-recall-guide/", "EXIT PLAN", "Capture return, warranty, support and recall evidence before checkout"),
    ("gear/cannabis-loupe-pocket-microscope-guide/", "INSPECTION FIT", "Compare field of view, working distance, setup, and ownership cost"),
    ("gear/cannabis-humidity-pack-hygrometer-guide/", "HUMIDITY SYSTEM", "Compare recurring packs, meters, service, and ownership cost"),
]
RECIPROCAL_RELATED["guides/vapes/index.html"] = [
    ("guides/disposable-vape-vs-510-cartridge-comparison/", "COMPARE SYSTEMS", "Separate integrated disposables from reusable 510 hardware"),
    ("gear/510-thread-vape-battery-safety/", "POWER SYSTEM", "Match cartridge, battery, settings, charger and recall identity"),
    ("gear/cannabis-vape-battery-cartridge-disposal-guide/", "DISPOSAL", "Separate residue, electronics and battery waste"),
]
RECIPROCAL_RELATED["gear/510-thread-vape-battery-safety/index.html"] = [
    ("guides/vapes/", "OIL + HARDWARE", "Audit the product, source, ingredients, lot, symptoms and stop-use signs"),
    ("gear/cannabis-accessory-return-warranty-recall-guide/", "AFTER-SALE PLAN", "Preserve the model, terms, receipt, support and recall route"),
    ("guides/disposable-vape-vs-510-cartridge-comparison/", "COMPARE SYSTEMS", "Choose between an integrated pen and reusable battery"),
]
RECIPROCAL_RELATED["gear/cannabis-vape-battery-cartridge-disposal-guide/index.html"] = [
    ("guides/vapes/", "BEFORE USE", "Identify the oil, lot, hardware, condition and symptom plan"),
    ("gear/cannabis-accessory-return-warranty-recall-guide/", "RETURN OR RECALL", "Keep a safety remedy separate from the waste route"),
    ("guides/disposable-vape-vs-510-cartridge-comparison/", "BEFORE PURCHASE", "Include end-of-life in the device decision"),
]
RECIPROCAL_RELATED["guides/cannabis-product-complaint-adverse-event-reporting/index.html"] = [
    ("gear/cannabis-accessory-return-warranty-recall-guide/", "ACCESSORY PROBLEM", "Separate seller return, warranty, recall and safety reporting"),
    ("guides/cannabis-menu-package-receipt-match-checklist/", "PRESERVE THE TRANSACTION", "Keep menu, cart, package, lot, price, and receipt evidence together"),
    ("guides/cannabis-edible-allergen-ingredient-label-guide/", "ALLERGENS + INGREDIENTS", "Preserve the ingredient panel, cross-contact language, and lot"),
]
# October 14 gives the rebuilt alcohol handoff record direct routes from the
# established transport and hosting pages, and connects the three-model light
# comparison to the lawful home-grow and neutral gear-comparison paths.
RECIPROCAL_RELATED["guides/cannabis-driving-impairment-sober-timer/index.html"] = [
    ("guides/cannabis-and-alcohol-mixing-risks/", "ALCOHOL + CANNABIS", "Keep both exposure clocks visible and remove driving before either substance"),
    ("guides/cannabis-social-hosting-guest-safety-plan/", "SOCIAL HOSTING", "Build the sober ride, product control, and emergency plan before guests arrive"),
    ("guides/cannabis-overconsumption-poisoning-response/", "URGENT RESPONSE", "Separate supportive care, Poison Control, and 911"),
]
RECIPROCAL_RELATED["guides/cannabis-social-hosting-guest-safety-plan/index.html"] = [
    ("guides/cannabis-and-alcohol-mixing-risks/", "TWO-SUBSTANCE RECORD", "Prepare the exposure and emergency handoff record"),
    ("guides/cannabis-driving-impairment-sober-timer/", "TRANSPORT", "Remove driving before the gathering begins"),
    ("guides/cannabis-overconsumption-poisoning-response/", "RESPONSE", "Choose supportive care, Poison Control, or 911"),
]
RECIPROCAL_RELATED["guides/new-york-home-cannabis-grow-planner/index.html"] = [
    ("gear/indoor-cannabis-grow-light-buying-cost-planner/", "LIGHT COMPARISON", "Compare three exact systems and their light-only ownership cost"),
    ("guides/new-york-home-cannabis-pest-mold-ipm-guide/", "PESTS + MOISTURE", "Build an identification-first scouting and IPM record"),
]
RECIPROCAL_RELATED["gear/cannabis-gear-comparison-worksheet/index.html"] = [
    ("gear/indoor-cannabis-grow-light-buying-cost-planner/", "GROW LIGHTS", "Compare load, energy, required setup, maintenance, and horizon cost"),
    ("gear/cannabis-accessory-return-warranty-recall-guide/", "EXIT PLAN", "Capture return, warranty, support, and recall evidence before checkout"),
    ("gear/cannabis-loupe-pocket-microscope-guide/", "INSPECTION FIT", "Compare field of view, working distance, setup, and ownership cost"),
]
# October 16 adds a claim-auditing authority asset and rebuilds the edible
# purchase path. Reciprocal links connect them to established evidence,
# complaint, label-math, allergen, and storage pages without creating a
# separate duplicate topic cluster.
RECIPROCAL_RELATED["guides/cannabis-official-source-directory/index.html"] = [
    ("guides/cannabis-claim-fact-check-worksheet/", "FACT-CHECK A CLAIM", "Match the source, product, route, people, outcome, time, rule, and certainty"),
    ("guides/cannabis-product-complaint-adverse-event-reporting/", "REPORTING", "Preserve the person, package, lot, problem, and correct route"),
    ("guides/cannabis-product-recall-batch-checker/", "RECALLS", "Match the exact lot to the current official notice"),
]
RECIPROCAL_RELATED["guides/cannabis-cbd-cancer-claims-evidence-guide/index.html"] = [
    ("guides/cannabis-claim-fact-check-worksheet/", "CLAIM AUDIT", "Test product, route, population, outcome, duration, harms, and certainty"),
    ("guides/cannabis-cbd-medication-interactions/", "MEDICINES", "Bring the exact product and complete medicine list to the care team"),
    ("guides/cannabis-official-source-directory/", "SOURCE ROUTER", "Use the authority that owns each question"),
]
RECIPROCAL_RELATED["guides/edibles/index.html"] = [
    ("guides/cannabis-edible-label-math-checker/", "CHECK THE MATH", "Reconcile serving, piece, and package totals without dose advice"),
    ("guides/cannabis-edible-allergen-ingredient-label-guide/", "INGREDIENTS", "Keep allergen and cross-contact evidence separate from cannabinoid testing"),
    ("guides/cannabis-child-resistant-packaging-home-storage-guide/", "PACKAGE TO LOCK", "Audit the package, reclosure, enclosure, placement, and routine"),
]
# October 17 rebuilds the cross-format storage reference and adds an
# accessibility-first equipment decision path. Reciprocal links keep original
# packaging, locked access, label identity, and honest gear comparison joined.
RECIPROCAL_RELATED["guides/cannabis-child-resistant-packaging-home-storage-guide/index.html"] = [
    ("guides/storage/", "STORAGE BY FORMAT", "Carry identity, condition, environment, access, and routine across every product type"),
    ("gear/cannabis-accessibility-tools-buying-guide/", "ACCESSIBLE ROUTINE", "Reduce opening, reading, reach, grip, and lock barriers without defeating package safety"),
    ("guides/cannabis-package-seal-tamper-evidence-checklist/", "SEAL + CLOSURE", "Inspect the unopened package and preserve the evidence trail"),
]
RECIPROCAL_RELATED["gear/cannabis-gear-comparison-worksheet/index.html"] = [
    ("gear/cannabis-accessibility-tools-buying-guide/", "ACCESSIBILITY FIT", "Test the exact task, package, full use cycle, reclosure, lock, care, and exit terms"),
    ("gear/indoor-cannabis-grow-light-buying-cost-planner/", "GROW LIGHTS", "Compare load, energy, required setup, maintenance, and horizon cost"),
    ("gear/cannabis-accessory-return-warranty-recall-guide/", "EXIT PLAN", "Capture return, warranty, support, and recall evidence before checkout"),
]
# October 18 attaches the rebuilt tolerance record to established safety and
# medication pages, and returns the grinder checkout path from established
# comparison and maintenance pages.
RECIPROCAL_RELATED.setdefault("responsible-use/index.html", []).append(
    ("guides/cannabis-tolerance-dependence-withdrawal/", "PATTERN RECORD", "Map exposure, function, change attempts, and support routes without self-diagnosis")
)
RECIPROCAL_RELATED.setdefault("guides/cannabis-cbd-medication-interactions/index.html", []).append(
    ("guides/cannabis-tolerance-dependence-withdrawal/", "TOLERANCE + WITHDRAWAL", "Bring products, medicines, other substances, symptoms, and change attempts into one review")
)
RECIPROCAL_RELATED.setdefault("gear/cannabis-gear-comparison-worksheet/index.html", []).insert(
    0, ("gear/grinders/", "GRINDER FIT", "Run exact models through dry fit, materials, cleaning, service, recall, and return gates")
)
RECIPROCAL_RELATED.setdefault("gear/cannabis-tool-cleaning-kit/index.html", []).append(
    ("gear/grinders/", "GRINDER CARE", "Match brushes, cleaners, inspection, drying, and replacement rules to the exact model")
)
# October 19 connects the rebuilt label field guide back from the lot-report
# and official-source authorities, and routes exact lighter comparisons from
# the neutral gear worksheet and fire-safe disposal page.
RECIPROCAL_RELATED.setdefault("guides/cannabis-certificate-of-analysis-coa-guide/index.html", []).insert(
    0, ("guides/read-a-label/", "PACKAGE RECORD", "Reconcile identity, quantity basis, ingredients, warnings, lot, dates, and report route")
)
RECIPROCAL_RELATED.setdefault("guides/cannabis-official-source-directory/index.html", []).insert(
    0, ("guides/read-a-label/", "LABEL FIELD GUIDE", "Build the package-to-lot evidence card before interpreting claims")
)
RECIPROCAL_RELATED.setdefault("gear/cannabis-gear-comparison-worksheet/index.html", []).insert(
    0, ("gear/cannabis-lighter-flame-safety-guide/", "IGNITION TOOL", "Compare exact models by job, controls, hand fit, recall route, storage, and cost")
)
RECIPROCAL_RELATED.setdefault("gear/cannabis-ashtray-ember-disposal-guide/index.html", []).insert(
    0, ("gear/cannabis-lighter-flame-safety-guide/", "IGNITION SOURCE", "Verify the exact model, intended job, controls, condition, and storage")
)
# October 21 makes the pet-exposure response and jar planner discoverable from
# established veterinary, storage, package-access, and odor-control references.
RECIPROCAL_RELATED["guides/storage/index.html"] = [
    ("guides/cannabis-and-pets-accidental-exposure/", "PET EXPOSURE", "Prepare the call record and close the exact access route"),
    ("gear/cannabis-stash-jar-buying-guide/", "SECONDARY JAR", "Measure capacity, headspace, costs, claims, identity, and locked fit"),
    ("gear/smell-proof-storage/", "LOCKBOX FIT", "Keep odor language, access control, and usable interior fit separate"),
]
RECIPROCAL_RELATED["guides/cbd-products-for-pets-veterinarian-label-guide/index.html"] = [
    ("guides/cannabis-and-pets-accidental-exposure/", "ACCIDENTAL EXPOSURE", "Call promptly and preserve the exact product, ingredient, and timing record"),
]
RECIPROCAL_RELATED["gear/smell-proof-storage/index.html"] = [
    ("gear/cannabis-stash-jar-buying-guide/", "JAR PLANNER", "Measure capacity, headspace, claims, and ownership cost"),
    ("guides/cannabis-child-resistant-packaging-home-storage-guide/", "PACKAGE + LOCK", "Keep child resistance and household access as separate layers"),
    ("guides/storage/", "STORAGE SYSTEM", "Match each format to identity, environment, and access controls"),
]
# October 22 strengthens discovery with contextual links for two new guides and
# repairs the four remaining guide routes that depended on their hub alone.
RECIPROCAL_RELATED.setdefault("guides/cannabis-product-recall-batch-checker/index.html", []).insert(
    0, ("guides/cannabis-product-disposal-decision-guide/", "DISPOSAL", "Preserve the remedy first, then separate product, battery, glass, and package routes")
)
RECIPROCAL_RELATED.setdefault("guides/cannabis-product-complaint-adverse-event-reporting/index.html", []).insert(
    0, ("guides/cannabis-product-disposal-decision-guide/", "SAFE HANDOFF", "Keep evidence until the responsible service gives a safe disposal route")
)
RECIPROCAL_RELATED.setdefault("guides/cannabis-product-price-label-comparison-calculator/index.html", []).insert(
    0, ("guides/cannabis-dispensary-loyalty-rewards-value-privacy-guide/", "REWARDS", "Subtract expiry, fees, price differences, and data tradeoffs from headline points")
)
RECIPROCAL_RELATED.setdefault("guides/cannabis-menu-package-receipt-match-checklist/index.html", []).insert(
    0, ("guides/cannabis-dispensary-loyalty-rewards-value-privacy-guide/", "PROGRAM TERMS", "Keep the rewards account separate from the product and receipt record")
)
RECIPROCAL_RELATED.setdefault("guides/cannabis-overconsumption-poisoning-response/index.html", []).insert(
    0, ("guides/cannabinoid-hyperemesis-syndrome-warning-signs/", "REPEATED VOMITING", "Recognize the recurrent pattern that needs clinical assessment")
)
RECIPROCAL_RELATED.setdefault("guides/vapes/index.html", []).insert(
    0, ("guides/cannabis-concentrates-dabs-label-safety-guide/", "CONCENTRATES", "Separate extract identity, potency labels, heat, and equipment risk")
)
RECIPROCAL_RELATED.setdefault("guides/cannabis-before-surgery-anesthesia/index.html", []).insert(
    0, ("guides/cannabis-pregnancy-breastfeeding-guidance/", "PREGNANCY", "Use current CDC and FDA guidance and disclose every product")
)
RECIPROCAL_RELATED.setdefault("guides/cbg-products-label-evidence-guide/index.html", []).insert(
    0, ("guides/cbg-dominant-cannabis-chemotype-guide/", "CHEMOTYPE", "Separate a CBG-dominant batch record from a finished-product claim")
)
# October 23 connects the post-harvest batch log and secondhand equipment
# screen from established, genuinely adjacent decision pages.
RECIPROCAL_RELATED.setdefault("guides/new-york-home-cannabis-grow-planner/index.html", []).insert(
    0, ("guides/new-york-home-cannabis-harvest-drying-curing-log/", "POST-HARVEST", "Carry plant identity, room safety, moisture, condition, and possession into one batch log")
)
RECIPROCAL_RELATED.setdefault("guides/new-york-home-cannabis-pest-mold-ipm-guide/index.html", []).insert(
    0, ("guides/new-york-home-cannabis-harvest-drying-curing-log/", "HARVEST RECORD", "Keep moisture, contamination, condition, and disposition attached after cutting")
)
RECIPROCAL_RELATED.setdefault("gear/cannabis-gear-comparison-worksheet/index.html", []).insert(
    0, ("gear/used-cannabis-accessory-buying-safety-guide/", "SECONDHAND", "Keep recall, residue, battery, missing-part, warranty, and adjusted-cost unknowns visible")
)
RECIPROCAL_RELATED.setdefault("gear/cannabis-accessory-return-warranty-recall-guide/index.html", []).insert(
    0, ("gear/used-cannabis-accessory-buying-safety-guide/", "USED GEAR", "Screen exact identity, condition, transferability, and the return path before handoff")
)
for _item in GUIDE_PAGES + OTHER_ARTICLES:
    if _item["path"] in RECIPROCAL_RELATED:
        _candidates = RECIPROCAL_RELATED[_item["path"]] + list(_item["related"])
        _seen_related: set[str] = set()
        _item["related"] = []
        for _related in _candidates:
            if _related[0] in _seen_related:
                continue
            _seen_related.add(_related[0])
            _item["related"].append(_related)
            if len(_item["related"]) == 4:
                break


def make_page(data: dict, kind: str = "article") -> Page:
    keys = {"path","title","description","category","h1","dek","updated","read_time","published"}
    values = {key:value for key,value in data.items() if key in keys}
    values.setdefault("updated", "August 17, 2026")
    values.setdefault("read_time", "8 min read")
    values["body"] = ""
    values["kind"] = kind
    return Page(**values)


def crumb_for(path: str, title: str) -> list[tuple[str, str | None]]:
    if path.startswith("guides/"):
        return [("Guides", "guides/"), (title, None)]
    if path.startswith("strains/"):
        return [("Strains", "strains/"), (title, None)]
    if path.startswith("gear/"):
        return [("Gear", "gear/"), (title, None)]
    if path.startswith("legal/"):
        return [("Legal", "legal/"), (title, None)]
    return [(title, None)]


def render_policy_pulse(item: dict) -> str:
    story=item["policy_pulse"]
    tone=story["direction"].lower()
    return f'''<div class="policy-pulse policy-pulse--{tone}"><div class="policy-pulse__top"><span class="direction-badge">{escape(story['direction'])}</span><span>{escape(story['date'])} · {escape(story['status'])}</span></div><h3><a href="{story['url']}" rel="noopener">{escape(story['title'])} ↗</a></h3><p>{escape(story['summary'])}</p><small>Source: {escape(story['source'])}</small></div><p class="micro">Window reviewed: March 1–September 1, 2026. A proposal, ballot campaign, veto, or stalled bill is not current law; the operative rules remain in the sections above.</p>'''


def render_purchase_access(item: dict) -> str:
    adult=item["adult_access"]
    medical=item["patient_access"]
    note=f'<p class="access-note">{escape(medical["note"])}</p>' if medical["note"] else ""
    return f'''<div class="purchase-access"><article><span>ADULT-USE / RECREATIONAL</span><h3>{escape(adult['label'])}</h3><p>{escape(adult['detail'])}</p></article><article><span>MEDICAL PROGRAM</span><h3>{escape(medical['label'])}</h3><p><b>How to qualify:</b> {escape(medical['how'])}</p>{note}<p><b>At the dispensary:</b> {escape(medical['bring'])}</p><a href="{medical['url']}" rel="noopener">Open the official patient instructions ↗</a></article></div><div class="callout callout--warning"><div>{icon('alert')}</div><div><h3>Do not buy a generic “medical card” online</h3><p>Only the credential, certification, recommendation, or registry process recognized by this state can authorize medical purchasing. Private evaluation services do not replace state approval where approval is required.</p></div></div>'''


def render_home() -> tuple[Page, str]:
    page = Page(
        path="index.html", title="Big Bud Man | Legal Cannabis, Without the Haze",
        description="Independent cannabis guides for adults 21+: strains, edibles, labels, gear, responsible use, and reviewed legal starting points for all 50 states.",
        category="Home", h1="Legal weed. Clear-headed guidance.",
        dek="Independent cannabis education for adults 21+.", body="", updated="October 23, 2026", kind="website",
    )
    main = f'''<main id="main-content">
<section class="hero"><div class="hero-noise"></div><div class="container hero-grid">
  <div class="hero-copy"><p class="eyebrow"><span class="live-dot"></span> INDEPENDENT · ADULTS 21+ · NO CANNABIS SOLD</p>
    <h1>LEGAL WEED.<br><em>CLEAR-HEADED GUIDANCE.</em></h1>
    <p class="hero-dek">The legal market got bigger. The useful information did not. We decode labels, formats, famous strain names, gear, safety, and the legal edges in all 50 states.</p>
    <div class="hero-actions"><a class="button button--primary" href="start-here/">Start here {icon('arrow')}</a><a class="button button--outline" href="guides/">Browse every guide</a></div>
    <div class="trust-row"><span>{icon('shield')} Legal-market focus</span><span>{icon('book')} Sources before stories</span><span>{icon('heart')} Responsible-use built in</span></div>
  </div>
  <div class="hero-art"><img src="assets/images/hero-bud-v2.webp" alt="Macro photograph of a cannabis flower under controlled studio lighting"><div class="hero-stamp"><em>FOR</em><b>21+</b><em>ADULTS</em></div><div class="hero-caption"><span>01</span><p><b>THE BIG BUD RULE</b><br>The batch in your hand matters more than the legend on the menu.</p></div></div>
</div></section>
<div class="manifesto-strip"><div class="marquee">READ THE LABEL <i>✦</i> KNOW THE SOURCE <i>✦</i> WAIT FOR THE FORMAT <i>✦</i> LOCK IT UP <i>✦</i> NEVER DRIVE HIGH</div></div>
<section class="container lane-section"><div class="section-head section-head--split"><div><p class="eyebrow">PICK A LANE</p><h2>Three better ways in</h2></div><p>Skip the endless menu. Start with the decision you actually need to make.</p></div>
<div class="lane-grid">
<a class="lane-card lane-card--lime" href="start-here/"><span>01</span><div>{icon('book')}<h3>New or returning?</h3><p>Formats, timing, labels, and the six decisions that keep a first session boring—in the good way.</p><b>Open start here {icon('arrow')}</b></div></a>
<a class="lane-card lane-card--amber" href="guides/read-a-label/"><span>02</span><div>{icon('tag')}<h3>Holding a package?</h3><p>Separate the serving from the package total, then find the batch, date, ingredients, and test link.</p><b>Decode the label {icon('arrow')}</b></div></a>
<a class="lane-card lane-card--cream" href="legal/"><span>03</span><div>{icon('scale')}<h3>Checking your state?</h3><p>Search all 50 states for adult-use, medical, limited-CBD, possession, home-grow, and official-source basics.</p><b>Open the law library {icon('arrow')}</b></div></a>
</div></section>
<section class="quiz-section"><div class="container quiz-grid"><div class="quiz-intro"><p class="eyebrow">CLEAR-LANE FINDER</p><h2>Tell us the decision.<br>We’ll point to the guide.</h2><p>Three clicks. No account, no saved cannabis profile, no fake recommendation engine.</p><div class="quiz-counter"><b data-quiz-count>01</b><span>/ 03</span></div></div>
<div class="quiz-card" data-quiz>
<div class="quiz-step is-active" data-step="1"><p class="quiz-label">QUESTION ONE</p><h3>How familiar are you?</h3><div class="choice-grid"><button data-answer="experience" data-value="new">Brand new</button><button data-answer="experience" data-value="returning">Returning after years</button><button data-answer="experience" data-value="current">Current consumer</button><button data-answer="experience" data-value="research">Just researching</button></div></div>
<div class="quiz-step" data-step="2"><p class="quiz-label">QUESTION TWO</p><h3>Which format is in front of you?</h3><div class="choice-grid"><button data-answer="format" data-value="edible">Edible or gummy</button><button data-answer="format" data-value="beverage">Cannabis beverage</button><button data-answer="format" data-value="flower">Flower or pre-roll</button><button data-answer="format" data-value="vape">Vape</button><button data-answer="format" data-value="concentrate">Concentrate or dab</button><button data-answer="format" data-value="basics">Not sure yet</button></div></div>
<div class="quiz-step" data-step="3"><p class="quiz-label">QUESTION THREE</p><h3>What matters right now?</h3><div class="choice-grid"><button data-answer="priority" data-value="urgent">Too much or accidental exposure</button><button data-answer="priority" data-value="mental">Anxiety, paranoia, or losing touch</button><button data-answer="priority" data-value="compare">Compare package price and labels</button><button data-answer="priority" data-value="recall">Check a recall</button><button data-answer="priority" data-value="lab">Read the lab report</button><button data-answer="priority" data-value="label">Read the label</button><button data-answer="priority" data-value="legal">Know the law</button><button data-answer="priority" data-value="gear">Compare gear</button><button data-answer="priority" data-value="basics">Build the basics</button></div></div>
<div class="quiz-result" data-quiz-result><div data-quiz-result-content></div><button class="text-button" type="button" data-quiz-reset>Start over</button></div>
</div></div></section>
<section class="container featured-section"><div class="section-head section-head--split"><div><p class="eyebrow">FAMOUS NAMES, HONEST CAVEATS</p><h2>Strain field notes</h2></div><a class="text-link" href="strains/">Explore all {len(STRAINS)} {icon('arrow')}</a></div>
<div class="strain-feature-grid">
<a class="strain-feature strain-feature--blue" href="strains/blue-dream/"><div class="strain-orbit"><img src="assets/images/strain-blue-dream.webp" alt="Representative macro cannabis flower photograph for the Blue Dream field note"><span>BALANCED SHORTHAND</span></div><div><h3>Blue Dream</h3><p>Berry-haze folklore meets years of producer and batch variation.</p><div class="meter"><span>NAME RELIABILITY</span><i><b style="width:38%"></b></i></div></div></a>
<a class="strain-feature strain-feature--yellow" href="strains/sour-diesel/"><div class="strain-orbit"><img src="assets/images/strain-sour-diesel.webp" alt="Representative macro cannabis flower photograph for the Sour Diesel field note"><span>BRIGHT SHORTHAND</span></div><div><h3>Sour Diesel</h3><p>Fuel-forward reputation, high-potency caution, no guarantee of energy.</p><div class="meter"><span>AROMA FAME</span><i><b style="width:86%"></b></i></div></div></a>
<a class="strain-feature strain-feature--violet" href="strains/northern-lights/"><div class="strain-orbit"><img src="assets/images/strain-northern-lights.webp" alt="Representative macro cannabis flower photograph for the Northern Lights field note"><span>HEAVY SHORTHAND</span></div><div><h3>Northern Lights</h3><p>Old-school name, modern batch: nostalgia is not a potency reading.</p><div class="meter"><span>HISTORY DEPTH</span><i><b style="width:78%"></b></i></div></div></a>
</div></section>
<section class="ny-section"><div class="container ny-grid"><div class="ny-map"><img src="assets/images/new-york-v2.svg" alt="Editorial map graphic of New York State with Central New York highlighted"><span class="map-pin"><b>SYRACUSE</b><br>CENTRAL NY VIEW</span></div><div class="ny-copy"><p class="eyebrow">NEW YORK LEGAL BASICS</p><h2>Know the edges.</h2><p>Adults 21+ may possess up to three ounces of cannabis and 24 grams of concentrate under New York law. That does not legalize unlicensed sales, vehicle use, impaired driving, state-line travel, or federal-property possession.</p><div class="number-grid"><div><b>21+</b><span>adult use</span></div><div><b>3 oz</b><span>cannabis</span></div><div><b>24 g</b><span>concentrate</span></div></div><a class="button button--dark" href="legal/new-york/">Open the New York guide</a><p class="micro">Reviewed August 26, 2026. Always confirm current rules with OCM.</p></div></div></section>
<section class="container library-preview"><div class="section-head section-head--split"><div><p class="eyebrow">THE LIBRARY</p><h2>Useful before exhaustive</h2></div><a class="text-link" href="guides/">Browse all guides {icon('arrow')}</a></div><div class="library-preview-grid">
<a class="big-story" href="guides/edibles/"><div><p class="kicker">FORMAT GUIDE</p><h3>Edibles without the classic mistake</h3><p>The mistake is not mysterious: taking more because the first serving has not announced itself yet.</p><b>Read the timing guide {icon('arrow')}</b></div><img src="assets/images/edible-timing.webp" alt="Studio still life of a single gummy beside an analog timer"></a>
<div class="story-stack"><a href="guides/delta-8-thc-label-safety-guide/"><p class="kicker">DELTA-8 THC + SAFETY</p><h3>Separate intoxicating THC from hemp and CBD framing</h3>{icon('arrow')}</a><a href="guides/cannabis-edible-allergen-ingredient-label-guide/"><p class="kicker">EDIBLES + ALLERGENS</p><h3>Read ingredients and cross-contact language before checkout</h3>{icon('arrow')}</a><a href="strains/stem-cell-cbg/"><p class="kicker">CBG CULTIVAR + EVIDENCE</p><h3>Separate Stem Cell's breeder record from the current product and lot</h3>{icon('arrow')}</a><a href="guides/cbd-drinks-powders-label-buying-guide/"><p class="kicker">CBD DRINKS + POWDERS</p><h3>Reconcile format, serving math, ingredients, lot evidence, and claims</h3>{icon('arrow')}</a><a href="guides/cannabis-product-complaint-adverse-event-reporting/"><p class="kicker">PRODUCT PROBLEM + REPORTING</p><h3>Preserve the person, package, lot, evidence, and correct complaint route</h3>{icon('arrow')}</a><a href="guides/disposable-vape-vs-510-cartridge-comparison/"><p class="kicker">VAPE SYSTEM + BUYING</p><h3>Compare integrated pens and 510 systems beyond the oil</h3>{icon('arrow')}</a><a href="guides/cbd-hemp-flower-label-legal-guide/"><p class="kicker">CBD + HEMP FLOWER</p><h3>Verify identity, total THC, lot evidence, and the rule that applies</h3>{icon('arrow')}</a><a href="guides/cannabis-anxiety-paranoia-psychosis-warning-signs/"><p class="kicker">MENTAL HEALTH + RESPONSE</p><h3>Separate fear, paranoia, disorientation, and psychosis warning signs</h3>{icon('arrow')}</a><a href="guides/cannabis-product-price-label-comparison-calculator/"><p class="kicker">PRICE + LABEL WORKSHEET</p><h3>Normalize three packages without turning potency into quality</h3>{icon('arrow')}</a><a href="guides/cannabis-smoke-vape-lung-health-guide/"><p class="kicker">LUNG HEALTH + ROUTES</p><h3>Separate smoke, aerosol, symptoms, and evidence limits</h3>{icon('arrow')}</a><a href="guides/cannabis-pre-roll-infused-label-buying-guide/"><p class="kicker">PRE-ROLL + CHECKOUT</p><h3>Compare plain and infused packs on identity, lot, and honest math</h3>{icon('arrow')}</a><a href="guides/cannabis-terms-label-lab-glossary/"><p class="kicker">48-TERM GLOSSARY</p><h3>Decode labels, laboratory notation, formats, and plant language</h3>{icon('arrow')}</a><a href="guides/cannabis-certificate-of-analysis-coa-guide/"><p class="kicker">LAB REPORT + BUYING</p><h3>Match the lot before trusting the pass badge</h3>{icon('arrow')}</a><a href="legal/shop-legal/"><p class="kicker">CHECKOUT VERIFICATION</p><h3>Verify the seller, product, certificate, and receipt</h3>{icon('arrow')}</a></div>
</div></section>
<section class="rules-section"><div class="container"><div class="section-head"><p class="eyebrow">THE SIX NON-NEGOTIABLES</p><h2>A responsible-use baseline</h2></div><ol class="rules-grid"><li><span>01</span><p><b>Adults only.</b><br>No access, use, or youth-targeted packaging.</p></li><li><span>02</span><p><b>No impaired driving.</b><br>Cars, boats, machinery, and ladders can wait.</p></li><li><span>03</span><p><b>Wait for the format.</b><br>Delayed products do not care that you are impatient.</p></li><li><span>04</span><p><b>Keep the package.</b><br>Identity and emergency information matter.</p></li><li><span>05</span><p><b>Lock every product.</b><br>Out of sight is not secure.</p></li><li><span>06</span><p><b>Notice the pattern.</b><br>Use should not quietly shrink the rest of life.</p></li></ol></div></section>
{newsletter('')}
</main>'''
    main = main.replace(
        '<a href="strains/stem-cell-cbg/"><p class="kicker">CBG CULTIVAR + EVIDENCE</p><h3>Separate Stem Cell\'s breeder record from the current product and lot</h3>'+icon('arrow')+'</a>',
        '',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/cannabis-101/"><p class="kicker">CANNABIS 101 + FIRST DECISIONS</p><h3>Build the product, label, safety, storage, and response record</h3>'+icon('arrow')+'</a><a href="gear/cannabis-gear-comparison-worksheet/"><p class="kicker">GEAR OWNERSHIP + COST</p><h3>Compare three exact models beyond the sticker price</h3>'+icon('arrow')+'</a>',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/cbn-products-label-evidence-guide/"><p class="kicker">CBN PRODUCTS + EVIDENCE</p><h3>Audit the label, lot, ingredients and actual sleep research</h3>'+icon('arrow')+'</a><a href="legal/cannabis-federal-property-rules-guide/"><p class="kicker">FEDERAL PROPERTY + 2026 LAW</p><h3>Identify the managing agency before crossing the boundary</h3>'+icon('arrow')+'</a><a href="guides/cannabis-social-hosting-guest-safety-plan/"><p class="kicker">SOCIAL HOSTING + SAFETY</p><h3>Plan consent, product control, sober rides and emergency response</h3>'+icon('arrow')+'</a>',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/terpenes/"><p class="kicker">TERPENE PANELS + CLAIMS</p><h3>Read the lot, units, aroma, human evidence, and limits</h3>'+icon('arrow')+'</a><a href="gear/cannabis-loupe-pocket-microscope-guide/"><p class="kicker">OPTICS FIT + OWNERSHIP COST</p><h3>Compare field of view, working distance, setup, and service</h3>'+icon('arrow')+'</a>',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/cannabis-cbd-liver-health-safety-guide/"><p class="kicker">CBD + LIVER HEALTH</p><h3>Separate the product, medicines, alcohol, symptoms, labs, and evidence</h3>'+icon('arrow')+'</a><a href="gear/cannabis-humidity-pack-hygrometer-guide/"><p class="kicker">HUMIDITY SYSTEM + COST</p><h3>Compare recurring packs, instruments, service, and ownership cost</h3>'+icon('arrow')+'</a>',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/cannabis-cbd-chronic-pain-evidence-guide/"><p class="kicker">CHRONIC PAIN + EVIDENCE</p><h3>Match the condition, exact product, function, harms, and review plan</h3>'+icon('arrow')+'</a><a href="gear/cannabis-rolling-tray-buying-guide/"><p class="kicker">ROLLING TRAY FIT + COST</p><h3>Compare task clearance, locked-storage fit, usable area, and delivered cost</h3>'+icon('arrow')+'</a><a href="guides/cannabis-cbd-cancer-claims-evidence-guide/"><p class="kicker">CANCER CLAIMS + EVIDENCE</p><h3>Separate treatment claims, symptom support, interactions, and the exact product</h3>'+icon('arrow')+'</a><a href="gear/smell-proof-storage/"><p class="kicker">LOCKBOX FIT + STORAGE</p><h3>Compare three usable interiors before judging the lock and odor claims</h3>'+icon('arrow')+'</a><a href="strains/stem-cell-cbg/"><p class="kicker">STEM CELL CBG + LOT EVIDENCE</p><h3>Trace the breeder, producer, package, report, and current rule</h3>'+icon('arrow')+'</a><a href="guides/cannabis-exercise-workout-heat-safety/"><p class="kicker">EXERCISE + HEAT SAFETY</p><h3>Plan the activity, symptoms, weather, supervision, and sober trip home</h3>'+icon('arrow')+'</a>',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/cannabis-cbd-epilepsy-seizure-care-guide/"><p class="kicker">CBD + EPILEPSY</p><h3>Separate prescription cannabidiol, retail CBD, seizure first aid, and the care record</h3>'+icon('arrow')+'</a><a href="gear/cannabis-tool-cleaning-kit/"><p class="kicker">CLEANING KIT + COST</p><h3>Match compatible supplies and calculate the real maintenance burden</h3>'+icon('arrow')+'</a><a href="guides/cannabis-glaucoma-eye-pressure-vision-guide/"><p class="kicker">EYE HEALTH + GLAUCOMA</p><h3>Separate a temporary pressure effect from proven optic-nerve care</h3>'+icon('arrow')+'</a><a href="guides/cbd-patches-transdermal-label-evidence-guide/"><p class="kicker">CBD PATCHES + EVIDENCE</p><h3>Separate the patch, skin-contact system, lot, and delivery claim</h3>'+icon('arrow')+'</a><a href="guides/cannabis-package-seal-tamper-evidence-checklist/"><p class="kicker">PACKAGE SEAL + TAMPER EVIDENCE</p><h3>Inspect the unopened package and preserve the evidence</h3>'+icon('arrow')+'</a><a href="gear/air-purifier-cannabis-smoke-odor-guide/"><p class="kicker">AIR CLEANER SIZING + COST</p><h3>Calculate room CADR, air changes, filters, electricity, and ownership cost</h3>'+icon('arrow')+'</a>',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/cannabis-edible-label-math-checker/"><p class="kicker">EDIBLE LABEL MATH</p><h3>Cross-check serving, piece, and package totals without inventing a dose</h3>'+icon('arrow')+'</a><a href="guides/cannabis-child-resistant-packaging-home-storage-guide/"><p class="kicker">PACKAGING + HOME SAFETY</p><h3>Audit child resistance, reclosure, locked storage, and the household routine</h3>'+icon('arrow')+'</a>',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/cannabis-official-source-directory/"><p class="kicker">OFFICIAL SOURCE DIRECTORY</p><h3>Use the agency or service that can actually answer the question</h3>' + icon('arrow') + '</a><a href="guides/cannabis-gummies-drinks-oils-capsules-comparison/"><p class="kicker">ORAL FORMAT COMPARISON</p><h3>Compare route, units, ingredients, handling, and value</h3>' + icon('arrow') + '</a><a href="guides/new-york-cannabis-delivery-online-order-verification-guide/"><p class="kicker">NEW YORK DELIVERY + VERIFICATION</p><h3>Match the license, website, order, handoff, and receipt</h3>' + icon('arrow') + '</a><a href="guides/cannabis-flower-freshness-package-date-buying-guide/"><p class="kicker">FLOWER FRESHNESS + DATES</p><h3>Audit the package and lot before trusting “fresh”</h3>' + icon('arrow') + '</a>',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/vapes/"><p class="kicker">VAPE OIL + HARDWARE</p><h3>Audit the source, label, lot, device, symptoms, and disposal route</h3>'+icon('arrow')+'</a><a href="gear/cannabis-accessory-return-warranty-recall-guide/"><p class="kicker">RETURNS + WARRANTIES + RECALLS</p><h3>Capture the exact terms and calculate early review checkpoints</h3>'+icon('arrow')+'</a>',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/cannabis-and-alcohol-mixing-risks/"><p class="kicker">ALCOHOL + CANNABIS SAFETY</p><h3>Keep both exposure clocks visible and prepare an emergency handoff record</h3>'+icon('arrow')+'</a><a href="gear/indoor-cannabis-grow-light-buying-cost-planner/"><p class="kicker">GROW-LIGHT COST + EVIDENCE</p><h3>Compare three exact systems across load, setup, support, and ownership cost</h3>'+icon('arrow')+'</a>',
        1,
    )
    main = main.replace(
        '<div class="story-stack">',
        '<div class="story-stack"><a href="guides/cannabis-next-day-impairment-evidence-guide/"><p class="kicker">NEXT-DAY FUNCTION + EVIDENCE</p><h3>Separate residual symptoms, task demands, testing, and what the research cannot certify</h3>'+icon('arrow')+'</a><a href="guides/storage/"><p class="kicker">STORAGE BY PRODUCT TYPE</p><h3>Keep identity, condition, environment, access, and routine in one chain</h3>'+icon('arrow')+'</a><a href="gear/cannabis-accessibility-tools-buying-guide/"><p class="kicker">ACCESSIBILITY + GEAR FIT</p><h3>Reduce grip, vision, tremor, reach, and one-handed barriers without defeating package safety</h3>'+icon('arrow')+'</a>',
        1,
    )
    return page, layout(page, main)


def newsletter(prefix: str) -> str:
    return f'''<section class="newsletter"><div><p class="eyebrow">THE CLEAR-HEADED DROP</p><h2>One useful email.<br>No dispensary confetti.</h2><p>New guides, law-review reminders, and practical gear notes.</p></div><form class="newsletter-form" action="https://formsubmit.co/{CONTACT_EMAIL}" method="post"><label class="sr-only" for="newsletter-email">Email address</label><input id="newsletter-email" type="email" name="email" placeholder="you@example.com" required><input type="hidden" name="_subject" value="Big Bud Man newsletter signup"><input type="hidden" name="_next" value="{DOMAIN}/thank-you/"><input type="text" name="_honey" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="button button--primary" type="submit">Join the list</button><p>Form delivery requires one-time inbox activation after launch. Unsubscribe requests are honored.</p></form></section>'''


def card(route: str, category: str, title: str, desc: str, icon_name: str = "book", prefix: str = "") -> str:
    search_text = f"{title} {desc} {category}".lower()
    path = route.rstrip("/") + "/index.html"
    source = next((item for item in GUIDE_PAGES + OTHER_ARTICLES if item["path"] == path), None)
    reviewed = source.get("updated", "August 17, 2026") if source else "August 17, 2026"
    reviewed_iso = datetime.strptime(reviewed, "%B %d, %Y").strftime("%Y-%m-%d")
    return f'''<a class="library-card" data-guide-card data-category="{escape(category.lower())}" data-search="{escape(search_text)}" data-title="{escape(title.lower())}" data-updated="{reviewed_iso}" href="{local(prefix, route)}"><div class="library-card__icon">{icon(icon_name)}</div><span>{escape(category)}</span><small class="library-card__reviewed">Reviewed <time datetime="{reviewed_iso}">{escape(reviewed)}</time></small><h2>{escape(title)}</h2><p>{escape(desc)}</p><b>Read guide {icon('arrow')}</b></a>'''


def render_guides_hub() -> tuple[Page,str]:
    page=Page("guides/index.html","Practical Cannabis Guides | Big Bud Man","Search practical cannabis guides for official sources, product formats, labels, safety, testing, storage, and responsible use.","Guide library","The guide library.","Search by the decision in front of you, then sort by editorial order, recent review date, or title.","",updated="October 23, 2026",kind="website")
    p="../"
    cards="".join([
      card("guides/cannabis-next-day-impairment-evidence-guide/","SCIENCE + RESPONSIBLE USE","Cannabis next-day impairment evidence","Separate residual symptoms, driving and work demands, testing, sleep and co-use, evidence limits, and a conservative morning decision gate.","shield",p),
      card("guides/new-york-home-cannabis-harvest-drying-curing-log/","SAFETY + HOME GROW","New York harvest, drying, and curing log","Keep one batch identity, room and condition record, narrow mass-change trend, container transition, stop gate, and final storage trail.","leaf",p),
      card("guides/cannabis-product-disposal-decision-guide/","SAFETY + WASTE","Cannabis product disposal decision guide","Separate recall evidence, product, battery electronics, glass or sharps, packaging, and chemical residue into locally verified routes.","alert",p),
      card("guides/cannabis-dispensary-loyalty-rewards-value-privacy-guide/","BUYING + PRIVACY","Loyalty rewards value and privacy","Calculate usable rewards and break-even spend, then audit expiry, exclusions, current rules, data collection, consent, and exit.","search",p),
      card("guides/storage/","HOME + STORAGE","Store cannabis safely by product type","Keep the original package, lot, condition, exact handling instructions, environment, locked access, household routine, and exit route together.","lock",p),
      card("guides/cannabis-claim-fact-check-worksheet/","EVIDENCE + SOURCES","Cannabis claim fact-check worksheet","Match the exact claim, product, source, study, limits, conflicting evidence, current rule, and unresolved gaps before acting.","search",p),
      card("guides/cbg-dominant-cannabis-chemotype-guide/","CBD + CANNABINOIDS","CBG-dominant cannabis","Separate chemotype, cultivar provenance, package identity, exact-lot CBG and CBGA results, claims, and legal category.","search",p),
      card("guides/cannabis-intoxication-impairment-detection/","SCIENCE + RESPONSIBLE USE","Intoxication, impairment, and detection","Keep acute effects, task function, toxicology findings, poisoning response, and legal conclusions in separate evidence lanes.","shield",p),
      card("guides/cbn-products-label-evidence-guide/","CBD + CANNABINOIDS","CBN products: labels and evidence","Reconcile CBN, THC, CBD and other ingredients; match the lot; audit sleep claims against the actual human study.","search",p),
      card("guides/cannabis-social-hosting-guest-safety-plan/","RESPONSIBLE USE + HOME","Cannabis social hosting","Plan adult-only access, consent, product control, locked storage, sober rides, urgent response and cleanup.","shield",p),
      card("guides/cannabis-cbd-liver-health-safety-guide/","HEALTH + CBD","Cannabis, CBD, and liver health","Separate the new CBD liver-enzyme evidence, prescription monitoring, retail uncertainty, medicines, alcohol, symptoms, labs, and clinician decisions.","heart",p),
      card("guides/cannabis-cbd-chronic-pain-evidence-guide/","HEALTH + EVIDENCE","Cannabis, CBD, and chronic pain","Match the condition, exact product, route, evidence, function, harms, medicine plan, and review date without inventing a treatment recommendation.","heart",p),
      card("guides/cannabis-cbd-cancer-claims-evidence-guide/","HEALTH + EVIDENCE","Cannabis, CBD, and cancer claims","Separate cancer-treatment claims, symptom-support questions, approved-medicine boundaries, interactions, exact-product evidence, and oncology decisions.","heart",p),
      card("guides/cannabis-menu-package-receipt-match-checklist/","BUYING + VERIFICATION","Menu-to-package match checklist","Match the seller, menu, cart, substitution, sealed package, lot evidence, final price, and receipt before opening.","tag",p),
      card("guides/cannabis-exercise-workout-heat-safety/","HEALTH + RESPONSIBLE USE","Cannabis, exercise, and heat safety","Plan around coordination, heart symptoms, heat, hydration, equipment, medicines, transport, and competition rules without performance claims.","heart",p),
      card("guides/new-york-home-cannabis-pest-mold-ipm-guide/","SAFETY + HOME GROW","New York home-grow pests, mold, and IPM","Build a dated scouting record, separate look-alikes, correct moisture and prevention failures, and stop at the exact pesticide label.","leaf",p),
      card("guides/cannabis-cbd-epilepsy-seizure-care-guide/","HEALTH + CBD","Cannabis, CBD, epilepsy, and seizure care","Use seizure first aid, separate prescription cannabidiol from retail CBD, and prepare one medicine, product, event, and monitoring record.","heart",p),
      card("guides/cannabis-glaucoma-eye-pressure-vision-guide/","HEALTH + EYE CARE","Cannabis, glaucoma, and eye symptoms","Separate a temporary pressure effect from proven treatment; record symptoms, products, medicines, measurements, and urgent signs.","heart",p),
      card("guides/cbd-patches-transdermal-label-evidence-guide/","CBD + BUYING","CBD patches and transdermal products","Compare classification, per-patch math, ingredients, skin instructions, lot evidence, delivery claims, and pharmacist questions.","search",p),
      card("guides/cannabis-package-seal-tamper-evidence-checklist/","PACKAGING + BUYING","Package seal and tamper evidence","Inspect the unopened seal, closure, label, lot, condition, report, recall, and complaint route without destroying the trail.","shield",p),
      card("guides/cbda-on-cannabis-hemp-labels/","CBD + LAB REPORTS","CBDA on cannabis and hemp labels","Separate CBDA from CBD, read compatible units and total-CBD calculations, and keep a cannabinoid row from becoming a medical claim.","search",p),
      card("guides/cannabis-dry-mouth-dental-oral-health-guide/","HEALTH + ORAL CARE","Cannabis, dry mouth, and dental visits","Build a symptom, route, product, medicine, and last-use record; know urgent signs and prepare for the dental visit.","heart",p),
      card("guides/cannabis-edible-label-math-checker/","BUYING + LABELS","Edible label math checker","Cross-check THC and CBD per serving, per piece, package totals, and a selected number of pieces without turning math into dose advice.","search",p),
      card("guides/cbg-products-label-evidence-guide/","CBD + CANNABINOIDS","CBG products: label and evidence","Identify the form, reconcile CBG and CBGA with the exact lot, and separate early human research from retail promises.","search",p),
      card("guides/cannabis-contaminant-test-results-guide/","LAB REPORTS + SAFETY","Cannabis contaminant test results","Read microbial, mycotoxin, pesticide, metal, solvent, physical-chemistry, and foreign-material panels without inventing zero or safe.","shield",p),
      card("guides/cannabis-child-resistant-packaging-home-storage-guide/","PACKAGING + HOME SAFETY","Child-resistant packaging and storage","Audit the retail package, reclosure, locked enclosure, placement, visitor routine, and accidental-exposure plan.","lock",p),
      card("guides/cannabis-official-source-directory/","SAFETY + SOURCES","Cannabis official source directory","Route emergencies, health evidence, product problems, recalls, fraud, driving, workplace testing, travel, hemp, and state rules to the source that owns the question.","shield",p),
      card("guides/cannabis-gummies-drinks-oils-capsules-comparison/","FORMAT + BUYING","Gummies, drinks, oils, and capsules","Compare intended route, label unit, timing uncertainty, ingredients, measuring steps, storage, exact-lot evidence, and total cost.","search",p),
      card("guides/new-york-cannabis-delivery-online-order-verification-guide/","BUYING + NEW YORK","New York delivery and online orders","Verify the license, website, payment, service area, ID check, handoff, receipt, package, and complaint route.","search",p),
      card("guides/cannabis-flower-freshness-package-date-buying-guide/","FLOWER + BUYING","Flower freshness and package dates","Compare dates, seal, exact-lot report, moisture evidence, condition, storage, recalls, and return policy.","leaf",p),
      card("guides/delta-8-thc-label-safety-guide/","SAFETY + LABELS","Delta-8 THC labels and safety","Separate psychoactive THC from hemp and CBD framing; check identity, exact-lot evidence, claims, household safety, and help routes.","alert",p),
      card("guides/cannabis-edible-allergen-ingredient-label-guide/","BUYING + ALLERGENS","Edible allergens and ingredients","Check gummies, chocolates, baked goods, drinks, and capsules for ingredients, major allergens, cross-contact language, and label gaps.","tag",p),
      card("guides/cbd-drinks-powders-label-buying-guide/","CBD + BUYING","CBD drinks and powders","Compare ready-to-drink products, concentrates, and powders by serving math, ingredients, lot evidence, claims, and storage.","search",p),
      card("guides/cannabis-product-complaint-adverse-event-reporting/","SAFETY + REPORTING","Product complaint and adverse-event reporting","Protect the person, preserve the package and lot, classify the problem, and use the official route that can act on it.","alert",p),
      card("guides/disposable-vape-vs-510-cartridge-comparison/","FORMAT + BUYING","Disposable vape versus 510 cartridge","Compare product identity, battery, compatibility, serviceability, ownership cost, storage, and end-of-life routes.","search",p),
      card("guides/cbd-hemp-flower-label-legal-guide/","CBD + HEMP","CBD flower and hemp flower","Verify the package, lot, total-THC basis, report, state rule, smoke risk, claims, and drug-testing uncertainty.","leaf",p),
      card("guides/cannabis-anxiety-paranoia-psychosis-warning-signs/","HEALTH + SAFETY","Anxiety, paranoia, and psychosis warning signs","Use the crisis gate, separate symptoms without diagnosing, preserve the product record, and prepare a useful clinical handoff.","heart",p),
      card("guides/cannabis-product-price-label-comparison-calculator/","BUYING + LABELS","Product price and label calculator","Compare three like-for-like packages by count, net quantity, and labeled cannabinoid total without ranking potency as quality.","search",p),
      card("guides/cannabis-smoke-vape-lung-health-guide/","HEALTH + SAFETY","Smoke, vaping, and lung health","Compare smoke, aerosol, dabs, and non-inhaled routes; use the symptom gate and build a clinician-ready exposure record.","heart",p),
      card("guides/cannabis-pre-roll-infused-label-buying-guide/","FORMAT + BUYING","Pre-roll and infused pre-rolls","Separate flower from added concentrate, match the lot, normalize package math, and reject fake quality signals.","search",p),
      card("guides/cannabis-terms-label-lab-glossary/","TERMS + LAB REPORTS","Cannabis terms and label glossary","Search 48 plain-language definitions across cannabinoids, labels, lab notation, formats, plant terms, and safety.","book",p),
      card("guides/cannabis-overconsumption-poisoning-response/","SAFETY + URGENT RESPONSE","Too much or accidental exposure","Use the emergency gate, contact Poison Control, preserve the product record, skip fake antidotes, and repair the prevention failure.","alert",p),
      card("guides/new-york-home-cannabis-grow-planner/","SAFETY + HOME GROW","New York home-grow planner","Check plant limits, residence and access rules, electrical load, moisture, starter sources, records, and harvest storage before starting.","leaf",p),
      card("guides/cannabis-older-adults-medication-fall-safety/","HEALTH + SAFETY","Cannabis and older adults","Connect the exact product to medicines, standing dizziness, falls, driving, daily function, caregiver boundaries, and clinician review.","heart",p),
      card("guides/cannabis-101/","CANNABIS BASICS","Cannabis 101","THC, CBD, formats, potency, categories, quality, and the questions worth asking.","book",p),
      card("guides/read-a-label/","BUYING + LABELS","Rebuild the product from the label","Use the identity, serving and package math, potency basis, dates, ingredients, warnings, batch code, and exact-lot report as one evidence record.","tag",p),
      card("guides/cannabis-certificate-of-analysis-coa-guide/","BUYING + LAB REPORTS","Read a certificate of analysis","Match the exact lot, then interpret units, reporting limits, panels, status, and report dates.","search",p),
      card("guides/cannabis-product-recall-batch-checker/","SAFETY + BUYING","Recall and batch checker","Match producer, product, lot, package, dates, and jurisdiction to the current official notice.","alert",p),
      card("guides/cannabis-drug-testing-thc-results-guide/","WORKPLACE + TESTING","Cannabis drug-test results","Understand specimens, screens, confirmation, THC metabolites, CBD risk, result records, and why no universal countdown exists.","search",p),
      card("guides/dot-cannabis-cbd-drug-testing-safety-sensitive-workers/","WORKPLACE + TESTING","DOT cannabis and CBD testing","Separate safety-sensitive scope, CBD label risk, laboratory review, removal, and the return-to-duty process.","shield",p),
      card("guides/terpenes/","AROMA","Terpenes without astrology","Use aroma chemistry without turning it into a guaranteed personality forecast.","spark",p),
      card("guides/edibles/","FORMAT + BUYING","Edible labels, timing, and buying","Audit serving and package math, ingredients, timing uncertainty, exact-lot evidence, the licensed seller, storage, and an exit plan.","clock",p),
      card("guides/cannabis-beverages-label-timing-buying-guide/","FORMAT + BUYING","Cannabis beverages","Read THC per serving and container, ingredients, timing claims, batch evidence, storage, and the no-alcohol rule.","clock",p),
      card("guides/cbd-gummies-label-buying-guide/","CBD + BUYING","CBD gummies","Compare per-piece and package math, ingredients, lot evidence, THC risk, claims, and locked storage.","search",p),
      card("guides/cbd-capsules-softgels-label-buying-guide/","CBD + BUYING","CBD capsules and softgels","Compare per-unit math, shell and carrier ingredients, lot evidence, THC risk, claims, and storage.","search",p),
      card("guides/flower/","FORMAT + BUYING","Cannabis flower buying checklist","Verify the seller, package, lot report, dates, condition, storage fit, route, exit plan, and complete ownership needs.","leaf",p),
      card("guides/vapes/","FORMAT","Vape red flags","Oil, potency, licensing, hardware, heat, batteries, and lung symptoms.","alert",p),
      card("guides/cannabis-concentrates-dabs-label-safety-guide/","FORMAT + BUYING","Concentrates and dabs","Decode wax, shatter, rosin, resin, potency, batch evidence, equipment heat, and storage.","alert",p),
      card("responsible-use/","SAFETY","Responsible use","The checklist for driving, pacing, storage, emergencies, and honest patterns.","shield",p),
      card("guides/cannabis-cbd-medication-interactions/","SAFETY","Cannabis and medications","A better pharmacist conversation about CBD, THC, labels, sedation, and interaction risk.","heart",p),
      card("guides/cannabis-tolerance-dependence-withdrawal/","RESPONSIBLE USE","Tolerance, dependence, and withdrawal","Separate the terms, audit the real-life pattern, and know when professional help is efficient.","shield",p),
      card("guides/cannabis-cbd-and-sleep/","SCIENCE","Cannabis, CBD, and sleep","Separate sleepiness from sleep quality, morning function, durable benefit, and treatment claims.","clock",p),
      card("guides/cannabis-before-surgery-anesthesia/","HEALTH + SAFETY","Cannabis before surgery","Build the exact product record, disclose recent use, and get the stop-and-resume plan from the surgical team.","heart",p),
      card("guides/secondhand-cannabis-smoke-indoor-air/","RESPONSIBLE USE","Secondhand smoke and indoor air","Build a no-indoor-smoke rule and understand what ventilation and filtration cannot promise.","shield",p),
      card("guides/full-spectrum-broad-spectrum-cbd-isolate/","CBD + HEMP","Full-spectrum, broad-spectrum, or isolate","Use the ingredients and batch report to test the spectrum badge, THC claim, and drug-test risk.","search",p),
      card("guides/thca-vs-thc-cannabis-labels/","SCIENCE + LABELS","THCA versus THC","Separate the analytes, total-THC formula, dry-weight basis, uncertainty, and legal rule.","tag",p),
      card("guides/cannabis-and-pets-accidental-exposure/","PET SAFETY","Cannabis and pets","Call promptly, preserve the package evidence, recognize urgent signs, and prevent the next exposure.","shield",p),
      card("guides/cbd-products-for-pets-veterinarian-label-guide/","CBD + PET SAFETY","CBD products for pets","Start with the veterinarian, then audit product identity, lot evidence, ingredients, claims, monitoring, and storage.","heart",p),
      card("guides/cbd-topicals-label-buying-guide/","CBD + HEMP","CBD topical labels","Audit intended use, ingredients, batch evidence, spectrum language, skin tolerance, and treatment claims.","search",p),
      card("guides/cannabis-and-alcohol-mixing-risks/","RESPONSIBLE USE","Cannabis and alcohol","Understand combined impairment, mismatched timing, transportation, distress response, and myth-free stop rules.","alert",p),
      card("guides/cbd-oil-tincture-label-buying-guide/","CBD + HEMP","CBD oil and tincture labels","Compare concentration, serving math, ingredients, lot evidence, THC risk, claims, and storage.","search",p),
      card("guides/hemp-seed-oil-vs-cbd-oil/","CBD + HEMP","Hemp seed oil versus CBD oil","Use ingredients, cannabinoid amounts, lot evidence, and intended use to separate two products that share the word hemp.","tag",p),
      card("guides/cannabis-driving-impairment-sober-timer/","RESPONSIBLE USE","Cannabis and driving","Why no timer, blood number, or feeling can certify driving readiness—and how to plan the ride.","alert",p),
      card("guides/cannabis-pregnancy-breastfeeding-guidance/","PUBLIC HEALTH","Cannabis, pregnancy, and breastfeeding","Current CDC and FDA guidance on routes, evidence limits, CBD, disclosure, household safety, and professional support.","heart",p),
      card("guides/cannabis-heart-rate-blood-pressure-safety/","HEART + SAFETY","Cannabis, heart rate, and blood pressure","Separate immediate cardiovascular effects, evidence limits, emergency signs, home measurements, and clinician questions.","heart",p),
      card("guides/cannabinoid-hyperemesis-syndrome-warning-signs/","HEALTH + SAFETY","Cannabinoid hyperemesis syndrome","Recognize recurrent-vomiting warning signs, emergency red flags, evidence limits, hot-water risks, and the role of cessation.","alert",p),
    ])
    guide_count = cards.count('data-guide-card')
    main=f'''<main id="main-content"><section class="hub-hero"><div class="container"><p class="eyebrow">PRACTICAL CANNABIS EDUCATION</p><h1>THE GUIDE<br><em>LIBRARY.</em></h1><p>No endless blog roll. Every page answers a decision an adult can actually have in front of them.</p></div></section><section class="container hub-feature"><a href="../start-here/"><div><p class="kicker">THE BEST FIRST PAGE</p><h2>Start here. Skip the folklore.</h2><p>Six decisions for new and returning adults: purpose, format, batch, context, storage, and exit plan.</p><b>Open the orientation {icon('arrow')}</b></div><img src="../assets/images/guide-field-notes.webp" alt="Unbranded cannabis package, sample jar, notebook, and magnifying glass arranged for close inspection"></a></section><section class="container guide-library" data-guide-library><div class="guide-tools"><label><span>FIND A GUIDE</span><input type="search" data-guide-search placeholder="Try: delivery, package date, lab report…" autocomplete="off"></label><div class="guide-filters" aria-label="Filter guide library"><button class="is-active" type="button" data-guide-filter="all">All guides</button><button type="button" data-guide-filter="format">Formats</button><button type="button" data-guide-filter="buying">Buying &amp; labels</button><button type="button" data-guide-filter="safety">Safety</button><button type="button" data-guide-filter="cbd">CBD &amp; hemp</button></div><label class="guide-sort"><span>SORT</span><select data-guide-sort><option value="editorial">Editorial order</option><option value="recent">Recently reviewed</option><option value="title">Title A–Z</option></select></label><p aria-live="polite"><span data-guide-count>{guide_count}</span> guides shown</p></div><p class="guide-empty" data-guide-empty hidden>No guide matched that search and filter. Clear the search or choose all guides.</p><div class="library-grid">{cards}</div></section><section class="container guide-paths"><div class="section-head"><p class="eyebrow">READ IN ORDER</p><h2>Thirty useful paths</h2></div><div class="path-list"><a href="../start-here/"><span>New or returning after years</span><b>START HERE → CANNABIS 101 → LABEL</b></a><a href="flower/"><span>Comparing packaged cannabis flower</span><b>SELLER → PACKAGE → LOT REPORT → CONDITION → STORAGE → EXIT</b></a><a href="new-york-home-cannabis-grow-planner/"><span>Planning a New York home grow</span><b>LAW → SPACE → LOAD → STARTER SOURCE → RECORDS → STORAGE</b></a><a href="new-york-home-cannabis-harvest-drying-curing-log/"><span>Carrying a lawful New York home grow through harvest</span><b>BATCH ID → ROOM → CONDITION LOG → CONTAINER → STORAGE</b></a><a href="cannabis-certificate-of-analysis-coa-guide/"><span>Holding a certificate of analysis or QR-linked lab report</span><b>PACKAGE → LOT MATCH → UNITS → PANELS → STATUS</b></a><a href="cbd-capsules-softgels-label-buying-guide/"><span>Comparing CBD capsules or softgels</span><b>UNIT MATH → FORMULA → LOT → CLAIMS → STORAGE</b></a><a href="cannabinoid-hyperemesis-syndrome-warning-signs/"><span>Repeated nausea or vomiting with frequent cannabis use</span><b>STOP USE → URGENCY CHECK → DISCLOSE → CLINICAL FOLLOW-UP</b></a><a href="cannabis-drug-testing-thc-results-guide/"><span>Facing a workplace, home, or program drug test</span><b>POLICY → SPECIMEN → SCREEN → CONFIRM → REVIEW</b></a><a href="cannabis-product-recall-batch-checker/"><span>Checking a recall, quarantine, or safety notice</span><b>PRESERVE PACKAGE → MATCH LOT → FOLLOW OFFICIAL ACTION</b></a><a href="edibles/"><span>Holding a gummy or chocolate</span><b>EDIBLES → LABEL → STORAGE</b></a><a href="cannabis-beverages-label-timing-buying-guide/"><span>Comparing a cannabis seltzer, tonic, or drink</span><b>BEVERAGES → LABEL → LICENSE → STORAGE</b></a><a href="vapes/"><span>Holding a cart or disposable</span><b>VAPES → SHOP LEGAL → RESPONSIBLE USE</b></a><a href="cannabis-concentrates-dabs-label-safety-guide/"><span>Comparing wax, shatter, rosin, resin, or dabs</span><b>CONCENTRATES → LABEL → LICENSE → STORAGE</b></a></div></section>{newsletter('../')}</main>'''
    main = main.replace("Twenty-nine useful paths", "Useful paths through the library")
    main = main.replace('<div class="path-list">', '<div class="path-list"><a href="cannabis-cbd-epilepsy-seizure-care-guide/"><span>Sorting prescription cannabidiol from retail CBD in seizure care</span><b>FIRST AID → MEDICINE → PRODUCT → INTERACTIONS → PLAN</b></a>', 1)
    main = main.replace('<div class="path-list">', '<div class="path-list"><a href="cannabis-claim-fact-check-worksheet/"><span>Checking a cannabis health, safety, product, legal, or comparative claim</span><b>CLAIM → SPEAKER → PRODUCT → SOURCE → MATCH → LIMITS → RULE</b></a>', 1)
    main = main.replace('<div class="path-list">', '<div class="path-list"><a href="cannabis-cbd-liver-health-safety-guide/"><span>Checking a cannabis, CBD, or liver-health claim</span><b>SYMPTOMS → EXACT PRODUCT → MEDICINES → LAB CONTEXT → CLINICIAN</b></a><a href="cannabis-cbd-chronic-pain-evidence-guide/"><span>Checking a cannabis or CBD chronic-pain claim</span><b>URGENCY → CONDITION → EVIDENCE → FUNCTION → HARMS → REVIEW</b></a>', 1)
    main = main.replace('<div class="path-list">', '<div class="path-list"><a href="cannabis-cbd-cancer-claims-evidence-guide/"><span>Checking a cannabis, CBD, or cannabinoid cancer claim</span><b>URGENT PLAN → EXACT CLAIM → EVIDENCE RUNG → PRODUCT → ONCOLOGY TEAM</b></a>', 1)
    main = main.replace('<div class="path-list">', '<div class="path-list"><a href="cannabis-exercise-workout-heat-safety/"><span>Planning exercise, outdoor activity, or a workout around cannabis</span><b>FUNCTION → SETTING → SYMPTOMS → HEAT → TRANSPORT → RULES</b></a>', 1)
    main = main.replace('<div class="path-list">', '<div class="path-list"><a href="new-york-home-cannabis-pest-mold-ipm-guide/"><span>Investigating pests, moisture, or mold in a New York home grow</span><b>LAW → OBSERVE → IDENTIFY → PREVENT → LABEL GATE → VERIFY</b></a>', 1)
    main = main.replace('<div class="path-list">', '<div class="path-list"><a href="cbd-patches-transdermal-label-evidence-guide/"><span>Comparing a CBD patch or transdermal claim</span><b>CLASSIFY → LABEL MATH → INGREDIENTS → LOT → CLAIMS → PHARMACIST</b></a><a href="cannabis-package-seal-tamper-evidence-checklist/"><span>Inspecting a seal or damaged cannabis package</span><b>STOP GATE → SEAL → CLOSURE → LOT → REPORT → EXIT ROUTE</b></a><a href="cannabis-glaucoma-eye-pressure-vision-guide/"><span>Checking a cannabis-and-glaucoma claim or preparing for an eye visit</span><b>URGENCY → SYMPTOM → PRODUCT → MEDICINES → MEASUREMENT → EYE CARE</b></a><a href="cannabis-dry-mouth-dental-oral-health-guide/"><span>Preparing for a dental visit or persistent dry mouth</span><b>URGENCY → SYMPTOM → ROUTE → PRODUCT → MEDICINES → DENTIST</b></a><a href="cannabis-edible-label-math-checker/"><span>Checking an edible label that lists servings and pieces</span><b>SERVING → UNIT → PACKAGE → LOT → SOURCE</b></a><a href="cbg-products-label-evidence-guide/"><span>Checking a CBG oil, gummy, capsule, flower, or other product</span><b>FORM → LABEL → LOT → EVIDENCE → CLAIMS</b></a><a href="cannabis-contaminant-test-results-guide/"><span>Reading a pesticide, microbial, metal, solvent, or other contaminant panel</span><b>PRODUCT → LOT → PANEL → LIMIT → STATUS → LIVE CHECK</b></a><a href="cannabis-child-resistant-packaging-home-storage-guide/"><span>Auditing cannabis packaging and household access</span><b>PACKAGE → RECLOSE → LOCK → PLACE → ROUTINE → RESPONSE</b></a><a href="cannabis-official-source-directory/"><span>Looking for the agency or service that owns a cannabis question</span><b>QUESTION → SOURCE OWNER → JURISDICTION → STATUS → EXIT ROUTE</b></a><a href="cannabis-gummies-drinks-oils-capsules-comparison/"><span>Comparing gummies, drinks, oils, capsules, lozenges, sprays, or powders</span><b>ROUTE → UNIT → INGREDIENTS → LOT → CONTROL → VALUE</b></a>', 1)
    main = main.replace('<b>START HERE → CANNABIS 101 → LABEL</b></a><a href="new-york-home-cannabis-grow-planner/">', '<b>START HERE → CANNABIS 101 → LABEL</b></a><a href="new-york-cannabis-delivery-online-order-verification-guide/"><span>Ordering cannabis delivery in New York</span><b>LICENSE → DOMAIN → CART → PAYMENT → HANDOFF → RECEIPT</b></a><a href="cannabis-flower-freshness-package-date-buying-guide/"><span>Comparing flower freshness and package dates</span><b>IDENTITY → DATES → SEAL → LOT → CONDITION → RETURN</b></a><a href="new-york-home-cannabis-grow-planner/">')
    main = main.replace(
        '<button class="is-active" type="button" data-guide-filter="all">All guides</button><button type="button" data-guide-filter="format">Formats</button><button type="button" data-guide-filter="buying">Buying &amp; labels</button><button type="button" data-guide-filter="safety">Safety</button><button type="button" data-guide-filter="cbd">CBD &amp; hemp</button>',
        '<button class="is-active" type="button" data-guide-filter="all" aria-pressed="true">All guides</button><button type="button" data-guide-filter="health" aria-pressed="false">Health</button><button type="button" data-guide-filter="format" aria-pressed="false">Formats</button><button type="button" data-guide-filter="buying" aria-pressed="false">Buying &amp; labels</button><button type="button" data-guide-filter="safety" aria-pressed="false">Safety</button><button type="button" data-guide-filter="responsible" aria-pressed="false">Responsible use</button><button type="button" data-guide-filter="workplace" aria-pressed="false">Workplace</button><button type="button" data-guide-filter="cbd" aria-pressed="false">CBD &amp; hemp</button>',
    )
    main = main.replace(
        '<b>START HERE → CANNABIS 101 → LABEL</b></a><a href="new-york-home-cannabis-grow-planner/">',
        '<b>START HERE → CANNABIS 101 → LABEL</b></a><a href="cannabis-anxiety-paranoia-psychosis-warning-signs/"><span>Responding to anxiety, paranoia, disorientation, or losing touch with reality</span><b>SAFETY GATE → EXACT SYMPTOM → PRODUCT RECORD → HELP → FOLLOW-UP</b></a><a href="cannabis-product-price-label-comparison-calculator/"><span>Comparing prices across like-for-like cannabis packages</span><b>FORMAT → LABEL BASIS → PRICE MATH → LOT EVIDENCE → CHECKOUT</b></a><a href="cannabis-smoke-vape-lung-health-guide/"><span>Comparing cannabis smoke, vaping, or another route</span><b>SYMPTOMS → ROUTE → PRODUCT → EVIDENCE → CLINICIAN</b></a><a href="cannabis-pre-roll-infused-label-buying-guide/"><span>Comparing plain and infused pre-rolls</span><b>IDENTITY → INGREDIENTS → WEIGHT → LOT → CHECKOUT</b></a><a href="cannabis-terms-label-lab-glossary/"><span>Decoding an unfamiliar label or laboratory term</span><b>TERM → OBJECT → UNIT → CAVEAT → PRIMARY SOURCE</b></a><a href="cannabis-older-adults-medication-fall-safety/"><span>Reviewing cannabis for an older adult</span><b>PRODUCT → MEDICINES → FALLS → FUNCTION → FOLLOW-UP</b></a><a href="cbd-products-for-pets-veterinarian-label-guide/"><span>Considering a CBD product for a dog, cat, or other pet</span><b>VETERINARIAN → ANIMAL → PRODUCT → LOT → MONITORING</b></a><a href="dot-cannabis-cbd-drug-testing-safety-sensitive-workers/"><span>Working in a DOT safety-sensitive role</span><b>SCOPE → POLICY → CBD RISK → REVIEW → RETURN TO DUTY</b></a><a href="new-york-home-cannabis-grow-planner/">',
    )
    main = main.replace(
        '<b>START HERE → CANNABIS 101 → LABEL</b></a><a href="cannabis-anxiety-paranoia-psychosis-warning-signs/">',
        '<b>START HERE → CANNABIS 101 → LABEL</b></a><a href="delta-8-thc-label-safety-guide/"><span>Checking a delta-8 THC product</span><b>IDENTITY → INTOXICATION → LOT → PANELS → RULE → HELP</b></a><a href="cannabis-edible-allergen-ingredient-label-guide/"><span>Checking an edible for allergens and ingredients</span><b>EMERGENCY PLAN → INGREDIENTS → ALLERGENS → LOT → CHECKOUT</b></a><a href="cbd-drinks-powders-label-buying-guide/"><span>Comparing a CBD drink, liquid concentrate, or powder</span><b>FORMAT → SERVING MATH → INGREDIENTS → LOT → STORAGE</b></a><a href="cannabis-product-complaint-adverse-event-reporting/"><span>Reporting a product problem, label mismatch, seller concern, or adverse event</span><b>SAFETY GATE → PERSON → PACKAGE → LOT → ROUTE → CASE</b></a><a href="disposable-vape-vs-510-cartridge-comparison/"><span>Choosing between an integrated vape pen and a 510 cartridge system</span><b>SOURCE → IDENTITY → COMPATIBILITY → SUPPORT → EXIT</b></a><a href="cbd-hemp-flower-label-legal-guide/"><span>Comparing CBD flower or hemp flower</span><b>PACKAGE → LOT → TOTAL THC → RULE → SMOKE + TEST RISK</b></a><a href="cannabis-anxiety-paranoia-psychosis-warning-signs/">',
    )
    main = main.replace('data-guide-search placeholder=', 'data-guide-search aria-controls="guide-results" placeholder=')
    main = main.replace('<div class="guide-filters" aria-label="Filter guide library">', '<div class="guide-filters" role="group" aria-label="Filter guide library">')
    main = main.replace('aria-pressed="true">All guides', 'aria-pressed="true" aria-controls="guide-results">All guides')
    main = main.replace('aria-pressed="false">', 'aria-pressed="false" aria-controls="guide-results">')
    main = main.replace('<select data-guide-sort>', '<select data-guide-sort aria-controls="guide-results">')
    main = main.replace('<p aria-live="polite"><span data-guide-count>', '<p id="guide-result-status" aria-live="polite"><span data-guide-count>')
    main = main.replace('<div class="library-grid">', '<div class="library-grid" id="guide-results">', 1)
    path_block = main.split('<div class="path-list">', 1)[1].split('</div>', 1)[0]
    main = main.replace('Twenty-nine useful paths', f'{path_block.count("<a href=")} useful paths')
    return page, layout(page, main, [("Guides",None)])


def render_strains_hub() -> tuple[Page,str]:
    page=Page("strains/index.html",f"{len(STRAINS)} Cannabis Strain Field Notes | Big Bud Man",f"Search {len(STRAINS)} honest cannabis strain field notes, including THC-dominant, CBD-rich, hemp, and mixed-ratio names with lineage and batch caveats.","Strain library","Famous names.<br>Honest caveats.","Strain culture is useful history and terrible quality control. Use the name to begin the question—not end it.","",updated="October 20, 2026",kind="website")
    items=[]
    for strain in sorted(STRAINS, key=lambda item: item["name"].lower()):
      aliases = " ".join(strain.get("aliases", []))
      cannabinoid_label = CANNABINOID_LABELS[strain["cannabinoid"]]
      search_text = f"{strain['name']} {aliases} {strain['shorthand']} {strain['lineage']} {strain['era']} {cannabinoid_label}".lower()
      if strain["cannabinoid"] == "cbd":
          photo_alt = f"Representative CBD-rich hemp flower photograph for the {strain['name']} field note; not a verified cultivar or batch image"
      elif strain["cannabinoid"] == "cbg":
          photo_alt = f"Representative hemp flower photograph for the {strain['name']} field note; not a verified cultivar or batch image"
      elif strain["cannabinoid"] == "ratio":
          photo_alt = f"Representative mixed THC and CBD cannabis flower photograph for the {strain['name']} field note; not a verified cultivar or batch image"
      else:
          photo_alt = f"Representative cannabis flower photograph for the {strain['name']} field note; not a verified cultivar or batch image"
      if strain["image"]:
          card_art=f'''<div class="strain-card__art"><img src="../assets/images/{strain['image']}" alt="{photo_alt}" loading="lazy" decoding="async"><span>{cannabinoid_label.upper()}</span><small>REPRESENTATIVE PHOTO</small></div>'''
      else:
          card_art=f'''<div class="strain-card__art strain-card__art--no-image"><span>{cannabinoid_label.upper()}</span><b>NO VERIFIED CULTIVAR IMAGE</b><small>EVIDENCE-FIRST PROFILE</small></div>'''
      items.append(f'''<a class="strain-card strain-card--{strain['color']}" data-strain-card data-lean="{strain['lean']}" data-cannabinoid="{strain['cannabinoid']}" data-search="{escape(search_text)}" href="{strain['slug']}/">{card_art}<div><p class="kicker">FIELD NOTE</p><h2>{strain['name']}</h2><b>{strain['lean'].upper()} RETAIL SHORTHAND · {strain['shorthand']}</b><p>{strain['reality']}</p><em>Read the honest note {icon('arrow')}</em></div></a>''')
    main=f'''<main id="main-content"><section class="hub-hero strain-hub-hero"><div class="container"><p class="eyebrow">{len(STRAINS)} STRAIN FIELD NOTES</p><h1>FAMOUS NAMES.<br><em>HONEST CAVEATS.</em></h1><p>History, aroma language, reputation, cannabinoid context, batch questions, and the warning every strain page should carry.</p><div class="strain-disclaimer">{icon('alert')}<span>No strain name guarantees an effect, potency, cannabinoid ratio, lineage, or medical outcome. Products vary by producer, batch, format, storage, and person.</span></div></div></section><section class="container strain-library"><div class="cbd-library-note"><div><span>HEMP IS IN THE LIBRARY</span><h2>CBD-rich, CBG-dominant, and mixed-ratio flower belongs in the same honest conversation.</h2></div><p>Use the cannabinoid filter to find CBD-forward, CBG-dominant, and THC:CBD ratio names. Then verify the current certificate of analysis: the cultivar name cannot prove cannabinoid content, legality, or a medical outcome.</p></div><div class="strain-tools" data-strain-filter><label class="strain-search"><span>SEARCH THE LIBRARY</span><input type="search" data-strain-search placeholder="Try Lantz, CBG, citrus, Kush…" autocomplete="off"></label><div class="filter-bar"><div class="strain-filter-groups"><div class="filter-group"><span>RETAIL SHORTHAND</span><button class="is-active" data-filter="all">All effects</button><button data-filter="balanced">Balanced</button><button data-filter="bright">Bright</button><button data-filter="heavy">Heavy</button></div><div class="filter-group"><span>CANNABINOID PROFILE</span><button class="is-active" data-cannabinoid-filter="all">All profiles</button><button data-cannabinoid-filter="thc">THC-dominant</button><button data-cannabinoid-filter="cbd">CBD-rich</button><button data-cannabinoid-filter="cbg">CBG-dominant</button><button data-cannabinoid-filter="ratio">THC:CBD ratio</button></div></div><p aria-live="polite"><span data-strain-count>{len(STRAINS)}</span> field notes</p></div></div><p class="strain-empty" data-strain-empty hidden>No field note matched that combination. Clear a filter or try a family, aroma word, or alternate spelling.</p><div class="strain-grid">{''.join(items)}</div></section><section class="container strain-method"><div class="section-head"><p class="eyebrow">THE METHOD</p><h2>How to use a strain page</h2></div><div class="method-grid"><div><span>01</span><h3>Read the story</h3><p>Learn why the name matters culturally.</p></div><div><span>02</span><h3>Check the caveat</h3><p>See where standardization ends.</p></div><div><span>03</span><h3>Inspect the batch</h3><p>Producer, format, potency, date, aroma.</p></div><div><span>04</span><h3>Write your note</h3><p>Record what actually happened in context.</p></div></div></section>{newsletter('../')}</main>'''
    main = main.replace('data-strain-search placeholder=', 'data-strain-search aria-controls="strain-results" placeholder=')
    main = main.replace('<div class="filter-group"><span>RETAIL SHORTHAND</span>', '<div class="filter-group" role="group" aria-label="Filter by retail shorthand"><span>RETAIL SHORTHAND</span>')
    main = main.replace('<div class="filter-group"><span>CANNABINOID PROFILE</span>', '<div class="filter-group" role="group" aria-label="Filter by cannabinoid profile"><span>CANNABINOID PROFILE</span>')
    main = main.replace('<button class="is-active" data-filter="all">', '<button class="is-active" type="button" data-filter="all" aria-pressed="true" aria-controls="strain-results">')
    main = main.replace('<button data-filter="', '<button type="button" aria-pressed="false" aria-controls="strain-results" data-filter="')
    main = main.replace('<button class="is-active" data-cannabinoid-filter="all">', '<button class="is-active" type="button" data-cannabinoid-filter="all" aria-pressed="true" aria-controls="strain-results">')
    main = main.replace('<button data-cannabinoid-filter="', '<button type="button" aria-pressed="false" aria-controls="strain-results" data-cannabinoid-filter="')
    main = main.replace('<p aria-live="polite"><span data-strain-count>', '<p id="strain-result-status" aria-live="polite"><span data-strain-count>')
    main = main.replace('<div class="strain-grid">', '<div class="strain-grid" id="strain-results">')
    return page, layout(page, main, [("Strains",None)])


def render_gear_hub() -> tuple[Page,str]:
    items = [
        ("used-cannabis-accessory-buying-safety-guide/","compare powered care","SECONDHAND + RECALLS","Screen used gear before handoff","Verify exact identity, recall status, residue, wear, battery condition, missing parts, warranty transfer, adjusted cost, and exit route.","check",None,None),
        ("cannabis-accessibility-tools-buying-guide/","compare storage preparation care","ACCESSIBILITY + FIT","Choose an accessibility aid without defeating package safety","Compare the exact task, package fit, full use cycle, reclosure, locked storage, cleaning, support, returns, and delivered cost.","check",None,None),
        ("dry-herb-vaporizer-dosing-capsule-guide/","compare preparation powered care","COMPATIBILITY + COST","Choose a dosing capsule system","Verify exact-device fit, adapter, loading, single-use or reuse instructions, cleaning, storage, recalls, and total cost.","check",None,None),
        ("cannabis-accessory-return-warranty-recall-guide/","compare care","RETURNS + WARRANTY + RECALLS","Plan the after-sale exit","Capture exact-model return terms, warranty coverage, recall identity, evidence, support, and early date checkpoints.","check",None,None),
        ("cannabis-gear-comparison-worksheet/","compare","COMPARISON + CHECKOUT","Compare gear honestly","Put three exact models through the same fit, materials, safety, care, support, recall, and first-year-cost screen.","check",None,None),
        ("indoor-cannabis-grow-light-buying-cost-planner/","compare powered","HOME GROW + ENERGY","Compare a grow light and its cost","Audit actual watts, maps, controls, mounting, environment, support, total load, and estimated light-only energy cost.","spark",None,None),
        ("cannabis-inventory-label-record-kit/","storage care","INVENTORY + LABELS","Build an inventory and record kit","Preserve original packaging, lot identity, dates, reports, receipts, photos, and a private locked-location code.","tag",None,None),
        ("smell-proof-storage/","storage compare","LOCKBOX FIT + STORAGE","Compare lockbox fit and storage","Compare three usable interiors, upright package clearance, delivered cost, lock design, odor claims, child-resistance scope, and placement.","lock","../assets/images/lockbox-v2.webp","Matte black lockbox photographed in a dark studio"),
        ("cannabis-stash-jar-buying-guide/","storage","SECONDARY STORAGE","Choose a stash jar","Compare usable volume, opening, materials, closure claims, light control, cleaning, labeling, and child safety.","lock",None,None),
        ("cannabis-pre-roll-tube-case-buying-guide/","storage","PORTABLE STORAGE","Choose a pre-roll tube or case","Check interior fit, crush protection, closure claims, materials, cleaning, labeling, locked storage, and travel limits.","lock",None,None),
        ("cannabis-humidity-pack-hygrometer-guide/","compare storage care","HUMIDITY SYSTEM + COST","Compare a hygrometer and humidity-pack system","Compare three exact systems by pack use, package rounding, instruments, service, ownership cost, specifications, and safety limits.","clock",None,None),
        ("grinders/","compare preparation care","PREPARATION + OWNERSHIP","Choose a grinder","Compare grip, chambers, contact surfaces, teeth, threads, screens, cleaning, warranty, recalls, total cost, and maintenance time.","gear","../assets/images/grinder-v2.webp","Open four-piece metal grinder photographed in a dark studio"),
        ("cannabis-rolling-tray-buying-guide/","compare preparation storage","PREPARATION FIT + COST","Compare rolling tray fit","Compare three trays by task clearance, locked-storage fit, usable area, delivered cost, materials, cleaning, and safety limits.","gear",None,None),
        ("cannabis-rolling-paper-cone-guide/","compare preparation","CONSUMABLE + COST","Compare rolling papers and cones","Compare dimensions, material and gum disclosure, delivered price, usable count, storage, smoke limits, and the fire-safety gate.","leaf",None,None),
        ("cannabis-rolling-machine-buying-guide/","preparation","PREPARATION FIT","Choose a rolling machine","Match bed length, paper dimensions, roller diameter, apron tension, cleaning, replacement parts, and storage.","gear",None,None),
        ("cannabis-loupe-pocket-microscope-guide/","compare preparation care","INSPECTION FIT + COST","Compare a loupe or pocket microscope","Compare three exact models by field of view, working distance, setup, annual service, ownership cost, and evidence limits.","search",None,None),
        ("digital-scale-buying-calibration-guide/","preparation care","MEASUREMENT + COST","Check repeatability and ownership cost","Compare capacity and five readings, then calculate mean, spread, maximum deviation, tolerance fit, and ownership cost.","scale",None,None),
        ("cannabis-tool-cleaning-kit/","compare care","MAINTENANCE + COST","Plan a cleaning kit and its cost","Match supplies to the exact tool, compare evidence, and calculate first-year cost, recurring cost, and maintenance time.","gear",None,None),
        ("air-purifier-cannabis-smoke-odor-guide/","powered care","INDOOR AIR","Choose an air purifier","Compare smoke CADR, room volume, HEPA, activated carbon, ozone, noise, filter cost, placement, and hard limits.","spark",None,None),
        ("510-thread-vape-battery-safety/","powered","BATTERY SAFETY","Choose a 510-thread battery","Verify compatibility, documented protections, charging, damage signs, locked storage, and responsible recycling.","alert",None,None),
        ("cannabis-vape-battery-cartridge-disposal-guide/","powered care","VAPE END OF LIFE","Dispose of a vape responsibly","Separate the battery, device, cartridge, residue, packaging, damage status, recall, and local acceptance route.","alert",None,None),
        ("dry-herb-vaporizer-buying-safety-guide/","powered","HEATED HARDWARE","Choose a dry-herb vaporizer","Compare operating format, materials, controls, temperature claims, batteries, cleaning, parts, and legal limits.","alert",None,None),
        ("cannabis-lighter-flame-safety-guide/","powered","IGNITION + FIRE SAFETY","Choose and store a lighter","Check intended use, child resistance, fuel or battery design, condition, clear zones, storage, and disposal.","alert",None,None),
        ("cannabis-ashtray-ember-disposal-guide/","care","FIRE-SAFE DISPOSAL","Choose an ashtray","Compare stability, depth, materials, wind, placement, extinguishing, cleaning, waste, and smoke-exposure limits.","alert",None,None),
        ("cannabis-glass-pipe-water-pipe-buying-guide/","preparation care","GLASSWARE","Choose a pipe or water pipe","Check format, material claims, joint fit, stability, cleaning access, replacement parts, and smoke-exposure limits.","search",None,None),
    ]
    page=Page("gear/index.html","Cannabis Gear Guides | Big Bud Man",f"Search {len(items)} independent cannabis accessory guides by job, including comparison, storage, accessibility, disposal, powered hardware, returns, warranties, and care.","Gear library","Gear that solves<br> a real problem.","Start with the job, then compare fit, accessibility, materials, safety evidence, maintenance, disposal, support, returns, warranty, recalls, and total cost—without affiliate pressure.","",updated="October 23, 2026",kind="website")
    cards=[]
    for href, categories, kicker, title, description, icon_name, image_src, image_alt in items:
        art = f'<div><img src="{image_src}" alt="{image_alt}"></div>' if image_src else f'<div class="gear-card__icon-art" aria-hidden="true">{icon(icon_name)}</div>'
        search = escape(f"{kicker} {title} {description} {categories}".lower(), quote=True)
        cards.append(f'''<a class="gear-card" data-gear-card data-category="{categories}" data-search="{search}" href="{href}">{art}<span class="kicker">{kicker}</span><h2>{title}</h2><p>{description}</p><b>Open guide {icon('arrow')}</b></a>''')
    job_paths='''<section class="container guide-paths gear-job-map"><div class="section-head"><p class="eyebrow">JOB-FIRST SHOPPING MAP</p><h2>Start with the problem. Keep “buy nothing” on the table.</h2><p>Choose the lane that describes the job in front of you. Each path ends in measured fit, evidence, total cost, and a safe exit—not a sponsored ranking.</p></div><div class="comparison-grid"><div><span>COMPARE OPTIONS</span><h3>Three exact models</h3><p>Use one record for fit, materials, safety scope, recalls, support, and first-year cost.</p><a href="cannabis-gear-comparison-worksheet/">Open the comparison worksheet →</a></div><div><span>CONTROL ACCESS</span><h3>Lock and organize</h3><p>Preserve the original package, measure usable interior space, and separate odor claims from security.</p><a href="smell-proof-storage/">Compare locked storage →</a></div><div><span>USE THE PACKAGE</span><h3>Improve hand access</h3><p>Name the exact opening, measuring, gripping, seeing, or organizing task without defeating reclosure.</p><a href="cannabis-accessibility-tools-buying-guide/">Match an accessibility aid →</a></div><div><span>MAINTAIN WHAT EXISTS</span><h3>Clean before replacing</h3><p>Check the maker's compatible method, hidden surfaces, drying, wear parts, and retirement line.</p><a href="cannabis-tool-cleaning-kit/">Build a maintenance plan →</a></div><div><span>POWER + HEAT</span><h3>Verify the whole system</h3><p>Match battery, charger, device, controls, damage signs, instructions, storage, and recalls.</p><a href="510-thread-vape-battery-safety/">Audit battery compatibility →</a></div><div><span>END OF LIFE</span><h3>Dispose without hiding the hazard</h3><p>Separate battery, device, residue, packaging, recall status, and the local collection route.</p><a href="cannabis-vape-battery-cartridge-disposal-guide/">Plan responsible disposal →</a></div></div><p class="micro">No affiliate links, sponsored placements, merchant rankings, prices, coupons, or stock claims appear in this map because the repository has no approved affiliate program or tracking ID.</p></section>'''
    main=f'''<main id="main-content"><section class="hub-hero gear-hero"><div class="container"><p class="eyebrow">{len(items)} INDEPENDENT ACCESSORY GUIDES</p><h1>GEAR THAT SOLVES<br><em>A REAL PROBLEM.</em></h1><p>Search by task. Compare the exact model. Keep affiliate math out of the conclusion.</p></div></section><section class="container gear-principles"><div><span>01</span><h2>Name the job</h2><p>Storage, records, preparation, measurement, cleaning, access control, or powered hardware—not “cannabis lifestyle.”</p></div><div><span>02</span><h2>Match the evidence</h2><p>Dimensions, materials, instructions, safety scope, warranty, recalls, and replacement parts must belong to the exact model.</p></div><div><span>03</span><h2>Price ownership</h2><p>Include required accessories, filters, batteries, cleaning, consumables, parts, and realistic service life.</p></div></section>{job_paths}<section class="container guide-paths"><div class="section-head"><p class="eyebrow">SECONDHAND DECISION</p><h2>A used price does not erase a used history.</h2><p>Before a marketplace handoff, match the exact model and serial, search recalls, keep residue and battery unknowns visible, price missing parts and care, and preserve a real return and disposal path.</p></div><p><a class="inline-cta" href="used-cannabis-accessory-buying-safety-guide/">Open the used-accessory identity, safety, and adjusted-cost screen <span>→</span></a></p></section><section class="container gear-library" data-gear-library><div class="guide-tools"><label><span>FIND GEAR BY JOB OR FEATURE</span><input type="search" data-gear-search aria-controls="gear-results" placeholder="Try: label, lock, battery, cleaning…" autocomplete="off"></label><div class="guide-filters" role="group" aria-label="Filter cannabis gear guides"><button class="is-active" type="button" data-gear-filter="all" aria-pressed="true" aria-controls="gear-results">All {len(items)}</button><button type="button" data-gear-filter="compare" aria-pressed="false" aria-controls="gear-results">Compare</button><button type="button" data-gear-filter="storage" aria-pressed="false" aria-controls="gear-results">Storage</button><button type="button" data-gear-filter="preparation" aria-pressed="false" aria-controls="gear-results">Preparation</button><button type="button" data-gear-filter="powered" aria-pressed="false" aria-controls="gear-results">Powered</button><button type="button" data-gear-filter="care" aria-pressed="false" aria-controls="gear-results">Care</button></div><p id="gear-result-status" aria-live="polite"><span data-gear-count>{len(items)}</span> guides shown</p></div><p class="guide-empty" data-gear-empty hidden>No gear guide matched that job or feature. Clear the search or choose all guides.</p><div class="gear-grid" id="gear-results">{''.join(cards)}</div></section><section class="container review-code"><div><p class="eyebrow">REVIEW CODE</p><h2>What earns a recommendation</h2></div><ol><li><b>Clear purpose</b><span>Solves a real problem better than a simpler option.</span></li><li><b>Safe materials</b><span>Construction and finish are appropriate for intended contact and care.</span></li><li><b>Scoped claims</b><span>Security, filtration, heat, calibration, and durability claims say exactly what they cover.</span></li><li><b>Serviceable</b><span>The owner can inspect, clean, maintain, and replace realistic wear parts.</span></li><li><b>Fair total cost</b><span>Value includes ownership cost, not a cannabis-themed markup or invented discount.</span></li></ol></section>{newsletter('../')}</main>'''
    return page, layout(page, main, [("Gear",None)])


def render_legal_hub() -> tuple[Page,str]:
    page=Page("legal/index.html","Cannabis Laws in All 50 States (2026) | Big Bud Man","Search reviewed cannabis laws for all 50 states plus federal-property, mailing and flying rules, with current official sources.","50-state legal library","Know your state.<br>Then verify it.","A practical 50-state starting point for possession, home grow, medical access, retail status, federal property, mailing, air travel, and official sources.","",updated="October 20, 2026",kind="website")
    cards=[]
    for item in STATE_LAWS:
        search_text=(item['name']+' '+item['code']+' '+STATUS_LABELS[item['status']]+' '+item['summary']+' '+item['policy_pulse']['direction']).lower()
        cards.append(f'''<a class="state-card state-card--{item['status']}" data-state-card data-status="{item['status']}" data-search="{escape(search_text)}" href="{item['slug']}/"><div class="state-card__top"><b>{item['code']}</b><span>{STATUS_LABELS[item['status']]}</span></div><span class="state-card__signal">Six-month signal · {escape(item['policy_pulse']['direction'])}</span><h2>{item['name']}</h2><p>{escape(item['summary'])}</p><em>Open state guide {icon('arrow')}</em></a>''')
    counts={key:sum(item["status"]==key for item in STATE_LAWS) for key in STATUS_LABELS}
    main=f'''<main id="main-content"><section class="hub-hero legal-hero"><div class="container"><p class="eyebrow">ALL 50 STATES · OFFICIAL LINKS · PURCHASE CREDENTIALS</p><h1>KNOW YOUR STATE.<br><em>THEN VERIFY IT.</em></h1><p>Every state page now separates recreational ID rules from medical cards, certifications, registry enrollment, official application steps, and states where patient retail is not actually available.</p><span class="legal-date">50 STATE PAGES REVIEWED <b>{REVIEW_DATE.upper()}</b></span></div></section>
<section class="container legal-overview"><div class="legal-summary"><div><b>{counts['adult']}</b><span>adult-use states</span></div><div><b>{counts['medical']}</b><span>medical-only states</span></div><div><b>{counts['limited']}</b><span>limited CBD / defense</span></div><div><b>{counts['restricted']}</b><span>no public program</span></div></div><div class="federal-banner">{icon('alert')}<p><b>Federal law changed narrowly on April 28, 2026.</b> FDA-approved marijuana products and marijuana covered by qualifying state medical licenses moved to Schedule III. General adult-use and unlicensed marijuana remain federally prohibited; interstate transport is still restricted. Read the <a href="https://www.justice.gov/opa/pr/justice-department-places-fda-approved-marijuana-products-and-products-containing-marijuana" rel="noopener">DOJ announcement</a> and <a href="{DEA_SOURCE}" rel="noopener">DEA record</a>.</p></div></section>
<section class="container state-library" data-state-library><div class="state-tools"><label><span>FIND A STATE</span><input type="search" data-state-search placeholder="Type a state or abbreviation…" autocomplete="off"></label><div class="state-filters" aria-label="Filter states by cannabis law status"><button class="is-active" data-state-filter="all">All 50</button><button data-state-filter="adult">Adult use</button><button data-state-filter="medical">Medical only</button><button data-state-filter="limited">Limited CBD</button><button data-state-filter="restricted">No public program</button></div><p aria-live="polite"><span data-state-count>50</span> state guides</p></div><p class="state-empty" data-state-empty hidden>No state matched that search and filter.</p><div class="state-grid">{''.join(cards)}</div></section>
<section class="container legal-method"><div><p class="eyebrow">HOW TO READ THE MAP</p><h2>Legal is not one switch.</h2></div><div class="legal-method__grid">{''.join(f'<article><span>{STATUS_LABELS[key]}</span><p>{STATUS_DESCRIPTIONS[key]}</p></article>' for key in STATUS_LABELS)}</div></section>
<section class="container legal-sources"><div><p class="eyebrow">RESEARCH BASELINE</p><h2>Current law first. Direction second.</h2><p>Program categories were cross-checked against NCSL and every page points to a state regulator, health department, commission, statute, or legislature. The six-month signal covers March 1–September 1, 2026 and labels proposals, vetoes, failed bills, and implementation separately from current law.</p></div><a class="button button--dark" href="{NCSL_SOURCE}" rel="noopener">Open the NCSL 50-state report {icon('arrow')}</a></section>
<section class="container legal-grid legal-grid--secondary"><a class="legal-card legal-card--feature" href="new-york/"><div><img src="../assets/images/new-york-v2.svg" alt="Editorial map graphic of New York State with Central New York highlighted"></div><span>DEEP DIVE · NEW YORK</span><h2>Adult-use basics</h2><p>Age, possession, sales, public use, vehicles, travel, growing, work, and housing.</p><b>Open New York guide {icon('arrow')}</b></a><a class="legal-card" href="shop-legal/"><div class="legal-card__icon">{icon('check')}</div><span>NEW YORK LICENSED MARKET</span><h2>Verify a shop</h2><p>Match the exact name and address on OCM’s live list, then verify the product.</p><b>Open verification guide {icon('arrow')}</b></a><a class="legal-card" href="cannabis-federal-property-rules-guide/"><div class="legal-card__icon">{icon('alert')}</div><span>FEDERAL PROPERTY · 2026</span><h2>Crossing a federal boundary?</h2><p>Identify the managing agency, exact product, current schedule and property-specific rule.</p><b>Open federal-property guide {icon('arrow')}</b></a><a class="legal-card" href="mailing-cannabis-cbd-usps-rules/"><div class="legal-card__icon">{icon('alert')}</div><span>FEDERAL MAIL RULES</span><h2>Can you mail cannabis or CBD?</h2><p>Separate controlled substances from qualifying domestic hemp, then check records and the international ban.</p><b>Open mailing explainer {icon('arrow')}</b></a><a class="legal-card" href="flying-with-cannabis-cbd-tsa-rules/"><div class="legal-card__icon">{icon('alert')}</div><span>FEDERAL AIR TRAVEL</span><h2>Flying with cannabis or CBD</h2><p>Separate TSA screening from federal status, airport jurisdiction, destination law, airline policy, and battery safety.</p><b>Open flying explainer {icon('arrow')}</b></a></section>
<section class="container legal-warning"><div>{icon('alert')}</div><div><h2>Education, not legal advice</h2><p>Laws, regulations, court decisions, local rules, tribal law, property policies, employer policies, and federal consequences can change the answer. These pages identify the issue and official source; they do not replace a lawyer.</p></div></section>{newsletter('../')}</main>'''
    main = main.replace('data-state-search placeholder=', 'data-state-search aria-controls="state-results" placeholder=')
    main = main.replace('<div class="state-filters" aria-label="Filter states by cannabis law status">', '<div class="state-filters" role="group" aria-label="Filter states by cannabis law status">')
    main = main.replace('<button class="is-active" data-state-filter="all">', '<button class="is-active" type="button" data-state-filter="all" aria-pressed="true" aria-controls="state-results">')
    main = main.replace('<button data-state-filter="', '<button type="button" aria-pressed="false" aria-controls="state-results" data-state-filter="')
    main = main.replace('<p aria-live="polite"><span data-state-count>', '<p id="state-result-status" aria-live="polite"><span data-state-count>')
    main = main.replace('<div class="state-grid">', '<div class="state-grid" id="state-results">')
    return page, layout(page, main, [("Legal",None)])


def render_state_page(item: dict) -> tuple[Page,str]:
    label=STATUS_LABELS[item["status"]]
    page=Page(
        f"legal/{item['slug']}/index.html",
        f"{item['name']} Cannabis Laws (2026) | Big Bud Man",
        f"{item['name']} cannabis laws for 2026: {label.lower()}, purchase and medical-card rules, possession, home grow, retail access, and official state sources.",
        f"{item['name']} cannabis law",
        f"{item['name']}<br>cannabis laws.",
        item["summary"],
        "",
        updated=REVIEW_DATE,
        read_time="7 min read",
    )
    status_box=f'''<div class="state-status state-status--{item['status']}"><div><span>STATE</span><b>{item['code']}</b></div><div><span>STATUS</span><b>{label}</b></div><div><span>ADULT POSSESSION</span><b>{'Legal within limits' if item['status']=='adult' else 'Not generally legal'}</b></div><div><span>HOME GROW</span><b>{escape(item['home_grow_label'])}</b></div></div>'''
    sections=[
        ("status", "The status, in one screen", f'''{status_box}<p>{escape(item['summary'])}</p><div class="callout"><div>{icon('scale')}</div><div><h3>What this label does—and does not—mean</h3><p>{escape(STATUS_DESCRIPTIONS[item['status']])} It does not answer public use, driving, employment, housing, federal property, tribal jurisdiction, or a city's business rules.</p></div></div>'''),
        ("possession", "Possession and use", f'''<p>{escape(item['possession'])}</p><ul class="checklist"><li>Public consumption can remain prohibited even when possession is legal.</li><li>Never drive, bike in traffic, boat, or operate machinery while impaired.</li><li>Keep products in their original package and outside the passenger area when transporting within the state.</li><li>Local ordinances and property policies can add restrictions without changing statewide status.</li></ul>'''),
        ("home-grow", "Home cultivation", f'''<p>{escape(item['home_grow'])}</p><p>Plant counts are only the first layer. Lease terms, owner permission, visibility, locked-area rules, nuisance law, processing limits, and possession of harvested cannabis can each change the practical answer.</p>'''),
        ("medical", "Medical access", f'''<p>{escape(item['medical'])}</p><p>A recommendation, registry card, out-of-state card, or diagnosis does not create identical rights everywhere. Confirm patient eligibility, reciprocity, purchase limits, approved forms, renewal rules, and caregiver rights with the official program.</p>'''),
        ("market", "Buying and retail status", f'''<p>{escape(item['market'])}</p><p>Use the state regulator's live license lookup where available. A website, delivery claim, hemp label, social-media account, or storefront sign is not proof of a marijuana license.</p>'''),
        ("purchase-access", "What you need to buy legally", render_purchase_access(item)),
        ("travel", "Travel, work, housing, and federal edges", f'''<ul class="red-list"><li><b>STATE LINES</b><span>Do not take cannabis across a state border—even between two adult-use states.</span></li><li><b>FEDERAL PROPERTY</b><span>State permission does not control federal buildings, lands, installations, or federal transportation rules.</span></li><li><b>WORK</b><span>Legal possession does not guarantee workplace use or protection from a lawful drug policy.</span></li><li><b>HOUSING</b><span>Smoking, cultivation, and possession can be restricted by leases, federal housing rules, or property policy.</span></li><li><b>TRIBAL LAND</b><span>Tribal law and jurisdiction can differ from the surrounding state; verify with the relevant tribal authority.</span></li></ul>'''),
        ("direction", "Six-month legal direction", render_policy_pulse(item)),
        ("sources", "Official sources", f'''<div class="official-links"><a href="{item['source_url']}" rel="noopener"><b>{escape(item['source_label'])}</b><span>Primary state source for current program rules and updates ↗</span></a><a href="{NCSL_SOURCE}" rel="noopener"><b>National Conference of State Legislatures</b><span>50-state program classification and statutory overview ↗</span></a><a href="{DEA_SOURCE}" rel="noopener"><b>U.S. Drug Enforcement Administration</b><span>Current federal marijuana scheduling actions and records ↗</span></a></div><p class="micro">Research review: {REVIEW_DATE}. Check the linked agency again before acting; laws and implementation can change after review.</p>'''),
    ]
    peers=[peer for peer in STATE_LAWS if peer["status"] == item["status"]]
    peer_position=next(index for index, peer in enumerate(peers) if peer["code"] == item["code"])
    previous=peers[(peer_position - 1) % len(peers)]
    following=peers[(peer_position + 1) % len(peers)]
    related=[
        (f"legal/{previous['slug']}/", "SAME STATUS", f"{previous['name']} cannabis laws"),
        (f"legal/{following['slug']}/", "SAME STATUS", f"{following['name']} cannabis laws"),
        ("legal/", "ALL 50 STATES", "Return to the law library"),
    ]
    notice=f'''<span class="live-dot"></span> Reviewed {REVIEW_DATE}. Educational overview, not legal advice. Verify current rules with <a href="{item['source_url']}" rel="noopener">{escape(item['source_label'])}</a>.'''
    html=render_article(page,[item["summary"],item["possession"],item["home_grow"]],sections,related,[("Legal","legal/"),(item["name"],None)],notice)
    return page,html


def render_contact() -> tuple[Page,str]:
    page=Page("contact/index.html","Contact Big Bud Man","Contact Big Bud Man with a correction, legal update, guide suggestion, gear question, partnership inquiry, or general message.","Contact","Say the useful thing.","Corrections, guide ideas, gear questions, partnerships, and legal updates are welcome. Cannabis sales requests are not.","",updated="October 16, 2026",kind="website")
    p="../"
    main=f'''<main id="main-content"><section class="contact-hero"><div class="container contact-grid"><div><p class="eyebrow">CONTACT BIG BUD MAN</p><h1>SAY THE<br>USEFUL THING.</h1><p>Include the page URL, the exact statement, and the best source you have when submitting a correction.</p><div class="contact-direct"><span>DIRECT EMAIL</span><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><p>Do not send medical records, ID, payment details, confidential legal information, or requests to buy cannabis.</p></div></div><form class="contact-form" action="https://formsubmit.co/{CONTACT_EMAIL}" method="post"><input type="hidden" name="_subject" value="Big Bud Man contact form"><input type="hidden" name="_next" value="{DOMAIN}/thank-you/"><input type="text" name="_honey" class="honeypot" tabindex="-1" autocomplete="off" aria-hidden="true"><label>Name<input name="name" autocomplete="name" required></label><label>Email<input type="email" name="email" autocomplete="email" required></label><label>Topic<select name="topic" required><option value="">Choose one</option><option>Correction</option><option>Legal update</option><option>Guide idea</option><option>Gear question</option><option>Partnership</option><option>General message</option></select></label><label>Message<textarea name="message" rows="7" required></textarea></label><label class="consent-check"><input type="checkbox" required><span>I understand this form is not for buying or selling cannabis and does not create a medical, legal, or professional relationship.</span></label><button class="button button--primary" type="submit">Send message</button><p class="micro">FormSubmit requires a one-time activation email before messages deliver.</p></form></div></section></main>'''
    return page, layout(page, main, [("Contact",None)])


def render_site_index(pages: list[Page]) -> tuple[Page, str]:
    latest_date = max(datetime.strptime(item.updated, "%B %d, %Y") for item in pages if item.kind == "article")
    latest_label = latest_date.strftime("%B %d, %Y").replace(" 0", " ")
    page = Page(
        "site-index/index.html",
        "Complete Site Index | Big Bud Man",
        "Browse every indexable Big Bud Man guide, strain field note, gear page, legal resource, and publication page from one crawlable index.",
        "Site index",
        "Every useful page.<br>One clean index.",
        "A human-readable crawl path for the complete publication, grouped by the decision or collection it belongs to.",
        "",
        updated=latest_label,
        kind="website",
    )
    visible = [item for item in pages if item.path not in {"404.html", "thank-you/index.html"}]
    groups = [
        ("Guides and responsible use", lambda item: item.path.startswith("guides/") or item.path in {"start-here/index.html", "responsible-use/index.html"}),
        ("Gear", lambda item: item.path.startswith("gear/")),
        ("Law and licensed access", lambda item: item.path.startswith("legal/")),
        ("Strain field notes", lambda item: item.path.startswith("strains/")),
        ("About, policies, and contact", lambda item: not any((item.path.startswith("guides/"), item.path.startswith("gear/"), item.path.startswith("legal/"), item.path.startswith("strains/"))) and item.path not in {"start-here/index.html", "responsible-use/index.html", "index.html"}),
    ]

    def route_for(item: Page) -> str:
        if item.path == "index.html":
            return "../"
        return f"../{item.path[:-10]}" if item.path.endswith("/index.html") else f"../{item.path}"

    sections = []
    for heading, predicate in groups:
        members = sorted((item for item in visible if predicate(item)), key=lambda item: clean_text(item.title).lower())
        links = "".join(f'<li><a href="{route_for(item)}">{escape(clean_text(item.title).removesuffix(" | Big Bud Man"))}</a></li>' for item in members)
        sections.append(f'<section><h2>{heading} <small>({len(members)})</small></h2><ul class="checklist">{links}</ul></section>')
    body = f'''<p class="update-line">Generated from the publication source · {latest_label}</p><p>This page is built from the same source list as search and the XML sitemap. It gives readers and crawlers a direct route to every indexable collection page and article without relying on JavaScript.</p>{"".join(sections)}<section><h2>Machine-readable discovery</h2><p><a class="inline-cta" href="../sitemap.xml">Open the XML sitemap <span>→</span></a></p><p><a class="inline-cta" href="../feed.xml">Open the Atom update feed <span>→</span></a></p></section>'''
    main = f'''<main id="main-content"><header class="standard-hero"><div class="container"><p class="eyebrow">SITE INDEX</p><h1>{page.h1}</h1><p>{page.dek}</p></div></header><div class="container standard-shell"><article class="prose prose--standard">{body}</article></div></main>'''
    return page, layout(page, main, [("Site index", None)])


def render_updates(pages: list[Page]) -> tuple[Page, str]:
    latest_date = max(datetime.strptime(item.updated, "%B %d, %Y") for item in pages if item.kind == "article")
    latest_label = latest_date.strftime("%B %d, %Y").replace(" 0", " ")
    page = Page(
        "updates/index.html",
        "Publication Updates | Big Bud Man",
        "See newly published and materially reviewed Big Bud Man guides, gear resources, legal explainers, and collection updates in date order.",
        "Publication updates",
        "What changed.<br>And when.",
        "A dated, crawlable record of new and materially reviewed pages—without requiring an account, social feed, or JavaScript.",
        "",
        updated=latest_label,
        kind="website",
    )
    recent = sorted(
        (item for item in pages if item.kind == "article" and datetime.strptime(item.updated, "%B %d, %Y") >= datetime(2026, 9, 4)),
        key=lambda item: (datetime.strptime(item.updated, "%B %d, %Y"), clean_text(item.title)),
        reverse=True,
    )
    grouped: dict[str, list[Page]] = {}
    for item in recent:
        grouped.setdefault(item.updated, []).append(item)

    sections = []
    for date_label, items in grouped.items():
        entries = "".join(
            f'<li><a href="../{item.path[:-10]}"><b>{escape(clean_text(item.title).removesuffix(" | Big Bud Man"))}</b><span>{escape(item.description)}</span></a></li>'
            for item in sorted(items, key=lambda item: clean_text(item.title).lower())
        )
        sections.append(f'<section><h2>{escape(date_label)}</h2><ul class="update-list">{entries}</ul></section>')
    body = f'''<p class="update-line">Source-generated · Last refreshed {latest_label}</p><p>This record uses each page's editorial review date. Small formatting-only changes are excluded; new pages and material content reviews are included.</p><p><a class="inline-cta" href="../feed.xml">Subscribe with the Atom feed <span>→</span></a></p>{"".join(sections)}'''
    main = f'''<main id="main-content"><header class="standard-hero"><div class="container"><p class="eyebrow">PUBLICATION UPDATES</p><h1>{page.h1}</h1><p>{page.dek}</p></div></header><div class="container standard-shell"><article class="prose prose--standard">{body}</article></div></main>'''
    return page, layout(page, main, [("Updates", None)])


def render_thanks() -> tuple[Page,str]:
    page=Page("thank-you/index.html","Message Received | Big Bud Man","Your Big Bud Man contact or newsletter form has been submitted. Return to the guide library or continue reading practical cannabis education.","Thank you","Message received.","Your submission left this site through the configured form service.","",kind="website")
    p="../"
    main=f'''<main id="main-content" class="thanks-page"><div class="container"><div class="thanks-mark">{icon('check')}</div><p class="eyebrow">FORM SUBMITTED</p><h1>MESSAGE RECEIVED.</h1><p>If this is the first submission after launch, the recipient inbox may need to approve FormSubmit’s activation email before delivery begins.</p><div class="hero-actions"><a class="button button--primary" href="{p}guides/">Browse guides</a><a class="button button--outline" href="{p}">Return home</a></div></div></main>'''
    return page, layout(page, main)


def render_404() -> tuple[Page,str]:
    page=Page("404.html","Page Not Found | Big Bud Man","The requested Big Bud Man page could not be found. Search the cannabis guide library or return to the home page.","Not found","That page wandered off.","Use search or head back to a page that exists.","",kind="website")
    main=f'''<main id="main-content" class="not-found"><div class="container"><p class="eyebrow">ERROR 404</p><div class="error-code">4<img src="assets/images/logo-mark.svg" alt="">4</div><h1>THAT PAGE WANDERED OFF.</h1><p>The URL may be old, mistyped, or too high to find its way home.</p><div class="hero-actions"><a class="button button--primary" href="./">Return home</a><button class="button button--outline" type="button" data-search-open>Search the library</button></div></div></main>'''
    return page, layout(page, main)


def write_page(page: Page, html: str) -> None:
    write_text(OUT, page.path, optimize_images(OUT, page.path, html))


def bundle_stylesheets(output_root: Path) -> None:
    """Ship one CSS request and remain safe to rerun on an existing bundle."""
    css_dir = output_root / "assets" / "css"
    entry = css_dir / "styles.css"
    chunks = sorted(
        css_dir.glob("styles-*.css"),
        key=lambda path: int(path.stem.rsplit("-", 1)[-1]),
    )
    if not chunks:
        if entry.exists() and "@import" in entry.read_text(encoding="utf-8"):
            raise RuntimeError("styles.css imports chunks that are not available to bundle")
        return
    bundle = ["/* Production bundle generated from the maintained styles-*.css modules. */\n"]
    for chunk in chunks:
        bundle.append(f"\n/* {chunk.name} */\n")
        bundle.append(chunk.read_text(encoding="utf-8").rstrip() + "\n")
    entry.write_text("".join(bundle), encoding="utf-8")
    for chunk in chunks:
        chunk.unlink()


def build() -> None:
    if OUT.exists():
        rmtree(OUT)
    OUT.mkdir(parents=True)
    source_assets=SOURCE/"assets"
    if source_assets.exists():
        copytree(source_assets, OUT/"assets", dirs_exist_ok=True)
        # The stash-jar planner ships with the October 21 interaction and
        # age-gate accessibility work. Give that page a versioned bundle so a
        # previously cached app.js cannot leave the new controls inert during
        # the normal GitHub Pages/CDN cache window.
        copy2(source_assets/"js/app.js", OUT/"assets/js/app-20261021.js")
        copy2(source_assets/"js/app.js", OUT/"assets/js/app-20261022.js")
    write_svg_assets(OUT)
    bundle_stylesheets(OUT)

    pages: list[Page] = []
    page, html = render_home(); write_page(page,html); pages.append(page)

    for data in GUIDE_PAGES + STRAIN_PAGES + OTHER_ARTICLES:
        page=make_page(data)
        label=page.h1.replace("<br>"," ").replace(".","").strip()
        sections=data["sections"]
        if page.path == "legal/new-york/index.html":
            ny=next(item for item in STATE_LAWS if item["code"] == "NY")
            sections=list(sections)
            sections.insert(-1, ("purchase-access", "What you need to buy legally", render_purchase_access(ny)))
            sections.insert(-1, ("direction", "Six-month legal direction", render_policy_pulse(ny)))
        html=render_article(page,data["takeaways"],sections,data["related"],crumb_for(page.path,label),data.get("notice",""))
        if page.path == "gear/cannabis-stash-jar-buying-guide/index.html":
            html = html.replace("assets/js/app.js", "assets/js/app-20261021.js")
        if page.path == "guides/cannabis-dispensary-loyalty-rewards-value-privacy-guide/index.html":
            html = html.replace("assets/js/app.js", "assets/js/app-20261022.js")
        write_page(page,html); pages.append(page)

    for data in STANDARD_PAGES:
        page=make_page(data,kind="website")
        label=page.h1.replace("<br>"," ").replace(".","").strip()
        html=render_standard(page,data["body"],crumb_for(page.path,label))
        write_page(page,html); pages.append(page)

    # New York keeps its deeper editorial page; the other 49 state summaries
    # complete the national library without creating a duplicate route.
    for item in STATE_LAWS:
        if item["code"] == "NY":
            continue
        page,html=render_state_page(item); write_page(page,html); pages.append(page)

    for renderer in (render_guides_hub,render_strains_hub,render_gear_hub,render_legal_hub,render_contact,render_thanks,render_404):
        page,html=renderer(); write_page(page,html); pages.append(page)

    page, html = render_updates(pages)
    write_page(page, html)
    pages.append(page)

    page, html = render_site_index(pages)
    write_page(page, html)
    pages.append(page)

    write_text(OUT,"CNAME","bigbudman.com\n")
    write_text(OUT,".nojekyll","\n")
    write_text(OUT,"robots.txt",f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n# Human-readable index: {DOMAIN}/site-index/\n# Publication updates: {DOMAIN}/updates/\n")
    manifest={"name":"Big Bud Man","short_name":"Big Bud Man","start_url":"/","display":"standalone","background_color":"#101712","theme_color":"#101712","icons":[{"src":"/assets/images/favicon.svg","sizes":"any","type":"image/svg+xml"}]}
    write_text(OUT,"site.webmanifest",json.dumps(manifest,indent=2)+"\n")
    publication_manifest={
        "publication_date":"2026-10-23",
        "page_count":3,
        "pages":[
            {"title":"New York Cannabis Harvest, Drying and Curing Log","url":"https://bigbudman.com/guides/new-york-home-cannabis-harvest-drying-curing-log/","department":"guides","portfolio_label":"Authority-expansion","search_intent":"give lawful New York home growers a traceable batch, room, environment, condition, container-transition, storage, and stop-use record after harvest"},
            {"title":"Used Cannabis Accessory Buying Guide","url":"https://bigbudman.com/gear/used-cannabis-accessory-buying-safety-guide/","department":"commercial","portfolio_label":"Exploration","search_intent":"screen secondhand cannabis accessories by exact identity, recall status, residue, wear, battery condition, missing parts, warranty transfer, adjusted cost, and safe exit"},
            {"title":"Cannabis Next-Day Impairment: Evidence Guide","url":"https://bigbudman.com/guides/cannabis-next-day-impairment-evidence-guide/","department":"science and responsible use","portfolio_label":"Exploration","search_intent":"separate residual symptoms, driving and safety-critical work, testing, sleep and co-use, evidence limits, and a conservative next-morning decision gate without inventing a clearance timer"},
        ],
        "monetization":{"affiliate_links_added":0,"reason":"No approved affiliate program or tracking ID is configured in the repository. The used-accessory guide adds an independent no-go screen, exact-object packet, adjusted-cost comparison, secondhand acceptance card, prominent gear-hub path, and contextual routes into existing model-specific buying guides. No merchant, marketplace, product, model, price, coupon, ranking, product image, or affiliate link was added."},
        "image_qa":{"editorial_placements":0,"affiliate_or_product_images":0,"note":"All three new pages use semantic text, tables, checklists, and existing brand interface assets. No editorial, product, affiliate, stock, or generated image was added or changed."},
        "search_console":{"report_date":"2026-10-21","decision":"The September 21–October 18 report showed 1,093 impressions, three clicks, 0.274% CTR, and average position 19.199. The canonical sitemap remained pending with one error and the legacy endpoint showed two errors, so today's only Data-led item adds URL-and-lastmod parity, page-date matching, nonfuture-date, robots-directive, and legacy-payload publication gates. Stem Cell CBG at 19 impressions, one click, and position 6.0 was not reinforced again because it was materially expanded October 15. One-impression legal queries, Montana cannabis at two impressions, About at 11 impressions, Contact at nine impressions, and Blue Dream terms around positions 48–70 were ignored as too small, navigational, or outside the supported 4–20 opportunity range."},
        "authority":{"action":"Published a citation-worthy New York post-harvest batch log with a room-readiness matrix, durable identity chain, repeatable environment and condition log, narrow mass-change math, container-transition record, hard-stop gate, and final storage/disposition record grounded in OCM, EPA, and university-extension sources. Reciprocal links strengthen the home-grow planner and pest/mold IPM cluster. The next-day guide also strengthens the driving, impairment, and sleep evidence cluster; one qualified National Safety Council resource opportunity was logged, and no outreach was sent."},
        "surfaces":["homepage story module","guide library, New York home-grow/IPM/post-harvest cluster, and driving/impairment/sleep cluster","gear library, secondhand feature path, comparison and returns cluster","editorial policy and sitemap integrity audit","publication updates","Atom feed","complete site index","search index","canonical XML sitemap","legacy Search Console sitemap compatibility URL","robots sitemap directive","checksum-verified source archive and publication gates"],
    }
    write_text(OUT,"publication-manifest.json",json.dumps(publication_manifest,indent=2)+"\n")
    indexable=[p for p in pages if p.path not in {"404.html","thank-you/index.html"}]
    strain_aliases = {
        f"strains/{strain['slug']}/index.html": " ".join(strain.get("aliases", []))
        for strain in STRAINS
    }
    editorial_keywords = {
        data["path"]: data.get("keywords", "")
        for data in GUIDE_PAGES + STRAIN_PAGES + OTHER_ARTICLES + STANDARD_PAGES
    }
    search_entries = [{
        "title": clean_text(page.title).removesuffix(" | Big Bud Man"),
        "description": clean_text(page.description),
        "category": clean_text(page.category),
        "keywords": " ".join(filter(None, (strain_aliases.get(page.path, ""), editorial_keywords.get(page.path, "")))),
        "url": "/" if page.path == "index.html" else f"/{page.path[:-10]}" if page.path.endswith("/index.html") else f"/{page.path}",
    } for page in indexable]
    write_text(OUT,"assets/js/search-index.js",f"window.BBM_SEARCH_INDEX = {json.dumps(search_entries, ensure_ascii=False, separators=(',', ':'))};\n")
    sitemap='''<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'''+"".join(f"  <url><loc>{canonical(p.path)}</loc><lastmod>{datetime.strptime(p.updated, '%B %d, %Y').strftime('%Y-%m-%d')}</lastmod></url>\n" for p in sorted(indexable,key=lambda x:x.path))+"</urlset>\n"
    write_text(OUT,"sitemap.xml",sitemap)
    # Search Console still lists the site's former WordPress sitemap endpoint.
    # GitHub Pages serves this static XML payload at that exact path (the query
    # string does not change the file lookup), so a future recrawl can recover
    # without weakening the canonical sitemap or robots.txt discovery path.
    write_text(OUT,"index.php",sitemap)
    feed_items = sorted(
        (p for p in pages if p.kind == "article"),
        key=lambda p: (datetime.strptime(p.updated, "%B %d, %Y"), clean_text(p.title)),
        reverse=True,
    )[:30]
    feed_entries = "".join(
        f'''  <entry>\n    <title>{escape(clean_text(p.title).removesuffix(" | Big Bud Man"))}</title>\n    <id>{canonical(p.path)}</id>\n    <link href="{canonical(p.path)}"/>\n    <updated>{datetime.strptime(p.updated, "%B %d, %Y").strftime("%Y-%m-%dT00:00:00Z")}</updated>\n    <published>{datetime.strptime(p.published, "%B %d, %Y").strftime("%Y-%m-%dT00:00:00Z")}</published>\n    <summary>{escape(p.description)}</summary>\n  </entry>\n'''
        for p in feed_items
    )
    feed_updated = max(datetime.strptime(p.updated, "%B %d, %Y") for p in feed_items).strftime("%Y-%m-%dT00:00:00Z")
    atom = f'''<?xml version="1.0" encoding="UTF-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">\n  <title>Big Bud Man updates</title>\n  <id>{DOMAIN}/</id>\n  <link href="{DOMAIN}/feed.xml" rel="self"/>\n  <link href="{DOMAIN}/"/>\n  <updated>{feed_updated}</updated>\n  <author><name>Big Bud Man Editorial Team</name><uri>{DOMAIN}/about/</uri></author>\n  <subtitle>New and materially reviewed cannabis guides, gear resources, and legal explainers.</subtitle>\n{feed_entries}</feed>\n'''
    write_text(OUT,"feed.xml",atom)
    print(f"Built {len(pages)} HTML pages in {OUT}")


def canonical(path: str) -> str:
    if path=="index.html": return f"{DOMAIN}/"
    if path.endswith("/index.html"): return f"{DOMAIN}/{path[:-10]}"
    return f"{DOMAIN}/{path}"


if __name__ == "__main__":
    build()
