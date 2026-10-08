# BigBudMan.com

**Legal weed. Clear-headed guidance.**

Big Bud Man is a fast, zero-dependency editorial publication for adults 21+. It covers cannabis basics, labels, edibles, flower, vapes, terpenes, strain field notes, practical accessories, responsible use, and reviewed legal starting points for all 50 states. It does **not** sell cannabis.

## Included

- 271 indexable pages, including 118 strain field notes, 50 state-law guides, 64 practical guides, 21 gear guides, a chronological updates page, and a generated complete site index, plus custom thank-you and 404 pages
- 21+ age gate stored only in browser local storage
- Responsive editorial design with original studio imagery and custom graphics
- Client-side site search with an on-device saved-reading manager and copyable reading list, searchable topic-filtered guide and gear libraries, strain filters, a searchable status-filtered 50-state law library, and semantic current-page navigation
- Explicit representative-photo disclosures plus category-matched hemp, CBD-rich, CBG-dominant, and THC:CBD imagery
- Interactive Clear-Lane Finder
- Desktop and native mobile article tables of contents, reading progress, copy-link, citation, checklist-copy, and save-for-later controls, and clean print/PDF output
- Canonical URLs, search metadata, Open Graph, JSON-LD, XML sitemap, Atom update feed, robots, and web manifest
- Dependency-free Python generator and static-site audit
- GitHub Pages deployment and pull-request audit workflows
- Newsletter and contact forms routed through FormSubmit

## Local build

```bash
cat source/bbm-tools.xz.part-* > /tmp/bbm-tools.tar.xz
sha256sum --check source/bbm-tools.sha256
tar -tJf /tmp/bbm-tools.tar.xz >/dev/null
tar -xJf /tmp/bbm-tools.tar.xz
python tools/build_site.py
python tools/audit_site.py _site
python -m http.server 8000 -d _site
```

Then open `http://localhost:8000`.

## Publishing

A push to `main` verifies the deployable source archive against its committed SHA-256 checksum, tests the archive, restores the generator, builds the full publication, audits all pages, and deploys `_site` through GitHub Pages. A checksum or archive failure stops publication before the build.

## One-time launch items

1. In **Settings → Pages**, select **GitHub Actions** if it is not selected automatically.
2. Configure `bigbudman.com` as the custom domain and enable **Enforce HTTPS** after GitHub issues the certificate.
3. Submit either form once and approve FormSubmit’s activation email for `contact@bigbudman.com`. Until that activation is completed, messages will not deliver.
4. Add analytics only when a real site-specific token is available; no placeholder or fake analytics token is included.

## Editorial maintenance

Legal pages show a review date and link to the responsible state regulator, health department, commission, or legislature, plus the NCSL 50-state baseline and current DEA rulemaking record. Recheck every legal and health claim before materially changing those pages. See `/editorial-policy/` and `/affiliate-disclosure/` for publishing standards.
