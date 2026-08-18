# BigBudMan.com

**Legal weed. Clear-headed guidance.**

Big Bud Man is a fast, zero-dependency editorial publication for adults 21+. It covers cannabis basics, labels, edibles, flower, vapes, terpenes, strain field notes, practical accessories, responsible use, and New York legal basics. It does **not** sell cannabis.

## Included

- 30 indexable pages plus custom thank-you and 404 pages
- 21+ age gate stored only in browser local storage
- Responsive editorial design and original SVG illustrations
- Client-side library search and strain filters
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
mkdir -p assets/images
cat source/og-card.part-* > assets/images/og-card.png
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

Legal pages show a review date and link directly to New York State’s Office of Cannabis Management. Recheck legal and health guidance before materially changing those pages. See `/editorial-policy/` and `/affiliate-disclosure/` for publishing standards.
