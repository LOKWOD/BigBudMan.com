# BigBudMan.com

**Legal weed. Clear-headed guidance.**

Big Bud Man is a fast, zero-dependency editorial publication for adults 21+. It covers cannabis basics, labels, edibles, flower, vapes, terpenes, strain field notes, practical accessories, responsible use, and reviewed legal starting points for all 50 states. It does **not** sell cannabis.

## Included

- 191 indexable pages, including 109 strain field notes and 50 state-law guides, plus custom thank-you and 404 pages
- 21+ age gate stored only in browser local storage
- Responsive editorial design with original studio imagery and custom graphics
- Client-side library search with strain filters and a searchable, status-filtered 50-state law library
- Explicit representative-photo disclosures plus category-matched hemp, CBD-rich, CBG-dominant, and THC:CBD imagery
- Interactive Clear-Lane Finder
- Article table of contents, reading progress, and copy-link controls
- Canonical URLs, search metadata, Open Graph, JSON-LD, sitemap, robots, and web manifest
- Dependency-free Python generator and static-site audit
- GitHub Pages deployment and pull-request audit workflows
- Newsletter and contact forms routed through FormSubmit

## Local build

```bash
cat source/bbm-tools.xz.part-* > /tmp/bbm-tools.tar.xz
tar -xJf /tmp/bbm-tools.tar.xz
python tools/build_site.py
python tools/audit_site.py _site
python -m http.server 8000 -d _site
```

Then open `http://localhost:8000`.

## Publishing

A push to `main` restores the generator, builds the full publication, audits all pages, and deploys `_site` through GitHub Pages.

## One-time launch items

1. In **Settings → Pages**, select **GitHub Actions** if it is not selected automatically.
2. Configure `bigbudman.com` as the custom domain and enable **Enforce HTTPS** after GitHub issues the certificate.
3. Submit either form once and approve FormSubmit’s activation email for `contact@bigbudman.com`. Until that activation is completed, messages will not deliver.
4. Add analytics only when a real site-specific token is available; no placeholder or fake analytics token is included.

## Editorial maintenance

Legal pages show a review date and link to the responsible state regulator, health department, commission, or legislature, plus the NCSL 50-state baseline and current DEA rulemaking record. Recheck every legal and health claim before materially changing those pages. See `/editorial-policy/` and `/affiliate-disclosure/` for publishing standards.
