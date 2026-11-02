(() => {
  'use strict';

  const body = document.body;
  const prefix = body.dataset.prefix || '';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const setActiveToggle = (buttons, active) => {
    buttons.forEach((button) => {
      const selected = button === active;
      button.classList.toggle('is-active', selected);
      button.setAttribute('aria-pressed', String(selected));
    });
  };

  const toast = (message) => {
    const node = $('[data-toast]');
    if (!node) return;
    node.textContent = message;
    node.classList.add('is-visible');
    window.clearTimeout(toast.timer);
    toast.timer = window.setTimeout(() => node.classList.remove('is-visible'), 2600);
  };

  // Footer year.
  $$('[data-year]').forEach((node) => { node.textContent = String(new Date().getFullYear()); });

  // Mobile navigation.
  const menuButton = $('[data-menu-toggle]');
  const mobileNav = $('[data-mobile-nav]');
  if (menuButton && mobileNav) {
    const closeMenu = () => {
      menuButton.setAttribute('aria-expanded', 'false');
      mobileNav.classList.remove('is-open');
      body.classList.remove('menu-open');
    };
    menuButton.addEventListener('click', () => {
      const opening = menuButton.getAttribute('aria-expanded') !== 'true';
      menuButton.setAttribute('aria-expanded', String(opening));
      mobileNav.classList.toggle('is-open', opening);
      body.classList.toggle('menu-open', opening);
    });
    $$('a', mobileNav).forEach((link) => link.addEventListener('click', closeMenu));
    window.addEventListener('resize', () => { if (window.innerWidth > 1100) closeMenu(); });
  }

  // Age confirmation. The page remains in the DOM for accessibility and search indexing.
  const ageGate = $('[data-age-gate]');
  if (ageGate) {
    const ageCard = $('.age-card', ageGate);
    const ageDescription = $('h2 + p', ageCard);
    if (ageCard && ageDescription) {
      ageDescription.id = 'age-description';
      ageCard.setAttribute('aria-describedby', ageDescription.id);
    }
    const pageRegions = [...body.children].filter((node) => node !== ageGate && node.tagName !== 'SCRIPT');
    const focusableInGate = () => $$('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])', ageGate)
      .filter((node) => !node.hidden && node.getClientRects().length);
    let priorFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const setGateIsolation = (active) => {
      pageRegions.forEach((node) => {
        if (!(node instanceof HTMLElement)) return;
        node.inert = active;
        if (active) node.setAttribute('data-age-inert', '');
        else node.removeAttribute('data-age-inert');
      });
    };
    const releaseAgeGate = () => {
      ageGate.hidden = true;
      body.classList.remove('modal-open');
      setGateIsolation(false);
      if (priorFocus?.isConnected) priorFocus.focus();
    };
    const trapAgeGateFocus = (event) => {
      if (ageGate.hidden || event.key !== 'Tab') return;
      const nodes = focusableInGate();
      if (!nodes.length) {
        event.preventDefault();
        ageGate.focus();
        return;
      }
      const first = nodes[0];
      const last = nodes[nodes.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      } else if (!ageGate.contains(document.activeElement)) {
        event.preventDefault();
        first.focus();
      }
    };
    let admitted = false;
    try { admitted = localStorage.getItem('bbm-age-21') === 'yes'; } catch (_) { admitted = false; }
    if (!admitted) {
      priorFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
      ageGate.hidden = false;
      body.classList.add('modal-open');
      setGateIsolation(true);
      window.setTimeout(() => $('[data-age-yes]', ageGate)?.focus(), 50);
    }
    document.addEventListener('keydown', trapAgeGateFocus);
    $('[data-age-yes]', ageGate)?.addEventListener('click', () => {
      try { localStorage.setItem('bbm-age-21', 'yes'); } catch (_) { /* private browsing can block storage */ }
      releaseAgeGate();
    });
    $('[data-age-no]', ageGate)?.addEventListener('click', () => {
      const card = $('.age-card', ageGate);
      if (!card) return;
      card.classList.add('age-denied');
      card.setAttribute('tabindex', '-1');
      card.innerHTML = `
        <img src="${prefix}assets/images/logo-full.webp" alt="Big Bud Man" width="920" height="499">
        <p class="eyebrow">NOT TODAY</p>
        <h2 id="age-title">This site is for adults 21+.</h2>
        <p>Thanks for being straight with us. You can close this tab or visit a general public-health resource.</p>
        <p><a href="https://www.samhsa.gov/find-help" rel="noopener">Find health information at SAMHSA â†—</a></p>`;
      window.setTimeout(() => card.focus(), 0);
    });
  }

  // Search, loaded only when requested.
  const searchDialog = $('[data-search-dialog]');
  const searchInput = $('[data-search-input]');
  const searchResults = $('[data-search-results]');
  let indexLoading = null;

  const loadSearchIndex = () => {
    if (window.BBM_SEARCH_INDEX) return Promise.resolve(window.BBM_SEARCH_INDEX);
    if (indexLoading) return indexLoading;
    indexLoading = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = `${prefix}assets/js/search-index.js`;
      script.onload = () => resolve(window.BBM_SEARCH_INDEX || []);
      script.onerror = reject;
      document.head.appendChild(script);
    });
    return indexLoading;
  };

  const localHref = (url) => url === '/' ? prefix || './' : `${prefix}${url.replace(/^\//, '')}`;
  const escapeHtml = (value) => String(value).replace(/[&<>'"]/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
  const articleActions = $('.article-actions');
  let saveButton = $('[data-save-article]');
  if (articleActions && !saveButton) {
    saveButton = document.createElement('button');
    saveButton.className = 'share-button';
    saveButton.type = 'button';
    saveButton.setAttribute('data-save-article', '');
    saveButton.setAttribute('aria-pressed', 'false');
    saveButton.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A3.5 3.5 0 0 1 7.5 2H11v17H7.5A3.5 3.5 0 0 0 4 22V5.5ZM20 5.5A3.5 3.5 0 0 0 16.5 2H13v17h3.5A3.5 3.5 0 0 1 20 22V5.5Z"></path></svg> <span>Save for later</span>';
    articleActions.prepend(saveButton);
  }
  const searchTip = $('.search-tip', searchDialog);
  let savedReading = $('[data-saved-reading]');
  if (searchDialog && searchTip && !savedReading) {
    savedReading = document.createElement('section');
    savedReading.className = 'saved-reading';
    savedReading.setAttribute('data-saved-reading', '');
    savedReading.setAttribute('aria-labelledby', 'saved-reading-title');
    savedReading.innerHTML = '<div class="saved-reading__head"><div><p class="eyebrow">THIS DEVICE ONLY</p><h3 id="saved-reading-title">Saved reading <small data-saved-count>0</small></h3></div><div class="saved-reading__tools"><button type="button" data-saved-copy>Copy list</button><button type="button" data-saved-clear>Clear all</button></div></div><div data-saved-results aria-live="polite"><p class="search-empty">No pages saved on this device yet.</p></div>';
    searchDialog.insertBefore(savedReading, searchTip);
  }
  const savedResults = $('[data-saved-results]');
  const savedCount = $('[data-saved-count]');
  const savedKey = 'bbm-saved-reading-v1';
  const pagePath = window.location.pathname.endsWith('/') ? window.location.pathname : `${window.location.pathname}/`;

  const getSaved = () => {
    try {
      const value = JSON.parse(localStorage.getItem(savedKey) || '[]');
      return Array.isArray(value) ? value.filter((item) => typeof item === 'string').slice(0, 30) : [];
    } catch (_) { return []; }
  };
  const setSaved = (items) => {
    try { localStorage.setItem(savedKey, JSON.stringify([...new Set(items)].slice(0, 30))); }
    catch (_) { toast('This browser could not save the reading list.'); }
  };
  const updateSaveButton = () => {
    if (!saveButton) return;
    const saved = getSaved().includes(pagePath);
    saveButton.setAttribute('aria-pressed', String(saved));
    const label = $('span', saveButton);
    if (label) label.textContent = saved ? 'Saved on this device' : 'Save for later';
  };
  const renderSaved = (items) => {
    if (!savedResults) return;
    const paths = getSaved();
    const byUrl = new Map(items.map((item) => [item.url, item]));
    const matches = paths.map((path) => byUrl.get(path)).filter(Boolean);
    if (savedCount) savedCount.textContent = String(matches.length);
    if (!matches.length) {
      savedResults.innerHTML = '<p class="search-empty">No pages saved on this device yet. Open an article and choose â€œSave for later.â€</p>';
      return;
    }
    savedResults.innerHTML = matches.map((item) => `
      <div class="saved-reading__item">
        <a class="search-result" href="${localHref(item.url)}">
          <span>${escapeHtml(item.category)}</span>
          <div><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.description)}</p></div>
        </a>
        <button type="button" data-saved-remove="${escapeHtml(item.url)}" aria-label="Remove ${escapeHtml(item.title)} from saved reading">Remove</button>
      </div>`).join('');
  };

  const renderSearch = (items, query) => {
    if (!searchResults) return;
    const normalized = query.trim().toLowerCase();
    if (savedReading) savedReading.hidden = Boolean(normalized);
    if (!normalized) {
      searchResults.innerHTML = '<p class="search-empty">Start typing to search the complete Big Bud Man library.</p>';
      renderSaved(items);
      return;
    }
    const words = normalized.split(/\s+/).filter(Boolean);
    const scored = items.map((item) => {
      const title = item.title.toLowerCase();
      const description = item.description.toLowerCase();
      const category = item.category.toLowerCase();
      const keywords = (item.keywords || '').toLowerCase();
      let score = 0;
      for (const word of words) {
        if (title.includes(word)) score += 8;
        if (category.includes(word)) score += 4;
        if (description.includes(word)) score += 2;
        if (keywords.includes(word)) score += 6;
      }
      if (title.startsWith(normalized)) score += 6;
      return {item, score};
    }).filter(({score}) => score > 0).sort((a, b) => b.score - a.score).slice(0, 9);

    if (!scored.length) {
      searchResults.innerHTML = `<p class="search-empty">No guide matched â€œ${escapeHtml(query)}.â€ Try a broader word such as â€œlabel,â€ â€œflower,â€ or â€œlegal.â€</p>`;
      return;
    }
    searchResults.innerHTML = scored.map(({item}) => `
      <a class="search-result" href="${localHref(item.url)}">
        <span>${escapeHtml(item.category)}</span>
        <div><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.description)}</p></div>
      </a>`).join('');
  };

  const openSearch = async () => {
    if (!searchDialog) return;
    try {
      if (!searchDialog.open) searchDialog.showModal();
      body.classList.add('modal-open');
      const items = await loadSearchIndex();
      searchInput?.focus();
      renderSearch(items, searchInput?.value || '');
    } catch (_) {
      if (searchResults) searchResults.innerHTML = '<p class="search-empty">Search could not load. Browse the Guides or Strains library instead.</p>';
    }
  };
  const closeSearch = () => {
    if (searchDialog?.open) searchDialog.close();
    body.classList.remove('modal-open');
  };
  $$('[data-search-open]').forEach((button) => button.addEventListener('click', openSearch));
  $('[data-search-close]')?.addEventListener('click', closeSearch);
  searchDialog?.addEventListener('click', (event) => { if (event.target === searchDialog) closeSearch(); });
  searchDialog?.addEventListener('close', () => body.classList.remove('modal-open'));
  searchInput?.addEventListener('input', async (event) => renderSearch(await loadSearchIndex(), event.target.value));
  saveButton?.addEventListener('click', async () => {
    const saved = getSaved();
    const exists = saved.includes(pagePath);
    setSaved(exists ? saved.filter((item) => item !== pagePath) : [pagePath, ...saved]);
    updateSaveButton();
    toast(exists ? 'Removed from saved reading.' : 'Saved on this device.');
    try { renderSaved(await loadSearchIndex()); } catch (_) { /* search remains optional */ }
  });
  $('[data-saved-clear]')?.addEventListener('click', async () => {
    setSaved([]);
    updateSaveButton();
    try { renderSaved(await loadSearchIndex()); } catch (_) { /* search remains optional */ }
    toast('Saved reading cleared.');
  });
  savedResults?.addEventListener('click', async (event) => {
    const button = event.target.closest('[data-saved-remove]');
    if (!button) return;
    setSaved(getSaved().filter((item) => item !== button.dataset.savedRemove));
    updateSaveButton();
    try { renderSaved(await loadSearchIndex()); } catch (_) { /* search remains optional */ }
    toast('Removed from saved reading.');
  });
  $('[data-saved-copy]')?.addEventListener('click', async () => {
    try {
      const items = await loadSearchIndex();
      const byUrl = new Map(items.map((item) => [item.url, item]));
      const matches = getSaved().map((path) => byUrl.get(path)).filter(Boolean);
      if (!matches.length) { toast('Save a page before copying the list.'); return; }
      const text = matches.map((item) => `${item.title} â€” ${window.location.origin}${item.url}`).join('\n');
      await navigator.clipboard.writeText(text);
      toast(`${matches.length} saved ${matches.length === 1 ? 'page' : 'pages'} copied.`);
    } catch (_) { toast('The saved list could not be copied.'); }
  });
  updateSaveButton();
  document.addEventListener('keydown', (event) => {
    if (event.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName || '')) {
      event.preventDefault(); openSearch();
    }
  });

  // Homepage guide router.
  const quiz = $('[data-quiz]');
  if (quiz) {
    const answers = {};
    const count = $('[data-quiz-count]');
    const result = $('[data-quiz-result]', quiz);
    const resultContent = $('[data-quiz-result-content]', quiz);
    const routes = {
      start: {title:'Start with the calm orientation', text:'Modern potency and formats can surprise new and returning adults. Begin with the six decisions that matter.', url:'start-here/', cta:'Open Start Here'},
      edible: {title:'Read the edible patience guide', text:'Delayed onset is the central issue. Learn the timeline and serving math before the first bite.', url:'guides/edibles/', cta:'Open edible guide'},
      beverage: {title:'Read the cannabis beverage label first', text:'Can size is not a THC serving. Compare per-serving and per-container amounts, ingredients, batch evidence, timing claims, and storage.', url:'guides/cannabis-beverages-label-timing-buying-guide/', cta:'Open beverage guide'},
      flower: {title:'Use the flower quality guide', text:'Freshness, cure, source, and manageable potency matter more than chasing the biggest percentage.', url:'guides/flower/', cta:'Open flower guide'},
      vape: {title:'Check the vape source and hardware', text:'Concentrated oil and compact hardware reward deliberate pacing and licensed sourcing.', url:'guides/vapes/', cta:'Open vape guide'},
      concentrate: {title:'Decode the concentrate before the device', text:'Translate wax, shatter, rosin, resin, and dabs; then verify potency units, the exact batch, lawful source, equipment, and storage.', url:'guides/cannabis-concentrates-dabs-label-safety-guide/', cta:'Open concentrate guide'},
      urgent: {title:'Use the exposure response plan', text:'Separate 911 warning signs from poison-center questions, preserve the exact product record, and skip fake antidotes.', url:'guides/cannabis-overconsumption-poisoning-response/', cta:'Open response guide'},
      mental: {title:'Use the mental-health safety gate', text:'Separate anxiety, panic, paranoia, disorientation, hallucinations, and losing touch with reality; then choose the right crisis route and preserve the exact record.', url:'guides/cannabis-anxiety-paranoia-psychosis-warning-signs/', cta:'Open warning-sign guide'},
      compare: {title:'Normalize the package, not the hype', text:'Compare three like-for-like products by price, count, net quantity, and labeled cannabinoid total while keeping quality and safety gates separate.', url:'guides/cannabis-product-price-label-comparison-calculator/', cta:'Open comparison calculator'},
      recall: {title:'Match the recall to the exact batch', text:'Preserve the package, use the official notice, and match producer, product, lot, size, dates, and jurisdiction before acting.', url:'guides/cannabis-product-recall-batch-checker/', cta:'Open recall checker'},
      lab: {title:'Match and read the laboratory report', text:'Confirm the exact lot, then keep every result attached to its unit, basis, reporting limit, panel, and status.', url:'guides/cannabis-certificate-of-analysis-coa-guide/', cta:'Open CoA guide'},
      label: {title:'Learn the label in ten minutes', text:'Separate package total from serving amount, then check traceability, ingredients, and batch information.', url:'guides/read-a-label/', cta:'Open label decoder'},
      legal: {title:'Check the law where you are', text:'Search all 50 states for possession, home grow, medical access, retail status, and the official source.', url:'legal/', cta:'Open 50-state library'},
      gear: {title:'Compare the gear on evidence', text:'Put fit, materials, safety scope, cleaning, support, recalls, and first-year cost in the same worksheet.', url:'gear/cannabis-gear-comparison-worksheet/', cta:'Open comparison worksheet'},
      basics: {title:'Build the Cannabis 101 foundation', text:'Understand THC, CBD, formats, timing, potency, and why a strain name never tells the whole story.', url:'guides/cannabis-101/', cta:'Open Cannabis 101'}
    };
    const chooseRoute = () => {
      if (answers.priority === 'urgent') return routes.urgent;
      if (answers.priority === 'mental') return routes.mental;
      if (answers.priority === 'compare') return routes.compare;
      if (answers.priority === 'recall') return routes.recall;
      if (answers.priority === 'lab') return routes.lab;
      if (answers.priority === 'legal') return routes.legal;
      if (answers.priority === 'gear') return routes.gear;
      if (answers.priority === 'label') return routes.label;
      if (answers.format === 'beverage') return routes.beverage;
      if (answers.format === 'edible') return routes.edible;
      if (answers.format === 'vape') return routes.vape;
      if (answers.format === 'concentrate') return routes.concentrate;
      if (answers.format === 'flower') return routes.flower;
      if (answers.experience === 'new' || answers.experience === 'returning') return routes.start;
      return routes.basics;
    };
    $$('[data-answer]', quiz).forEach((button) => button.addEventListener('click', () => {
      answers[button.dataset.answer] = button.dataset.value;
      const step = Number(button.closest('[data-step]')?.dataset.step || 1);
      $(`[data-step="${step}"]`, quiz)?.classList.remove('is-active');
      if (step < 3) {
        $(`[data-step="${step + 1}"]`, quiz)?.classList.add('is-active');
        if (count) count.textContent = String(step + 1).padStart(2, '0');
      } else {
        const route = chooseRoute();
        if (resultContent) resultContent.innerHTML = `<div class="result-icon">${document.querySelector('.lane-card svg')?.outerHTML || ''}</div><h3>${route.title}</h3><p>${route.text}</p><a class="button button--primary" href="${route.url}">${route.cta} â†’</a>`;
        result?.classList.add('is-active');
      }
    }));
    $('[data-quiz-reset]', quiz)?.addEventListener('click', () => {
      Object.keys(answers).forEach((key) => delete answers[key]);
      $$('.quiz-step', quiz).forEach((step) => step.classList.remove('is-active'));
      $('[data-step="1"]', quiz)?.classList.add('is-active');
      result?.classList.remove('is-active');
      if (count) count.textContent = '01';
    });
  }

  // Guide-library search and topic filters.
  const guideLibrary = $('[data-guide-library]');
  if (guideLibrary) {
    const guideInput = $('[data-guide-search]', guideLibrary);
    const guideCards = $$('[data-guide-card]', guideLibrary);
    const guideEmpty = $('[data-guide-empty]', guideLibrary);
    const guideCount = $('[data-guide-count]', guideLibrary);
    const guideSort = $('[data-guide-sort]', guideLibrary);
    const guideGrid = $('.library-grid', guideLibrary);
    guideCards.forEach((card, index) => { card.dataset.order = String(index); });
    let activeGuideFilter = 'all';
    const renderGuides = () => {
      const sort = guideSort?.value || 'editorial';
      const ordered = [...guideCards].sort((a, b) => {
        if (sort === 'recent') return (b.dataset.updated || '').localeCompare(a.dataset.updated || '') || Number(a.dataset.order) - Number(b.dataset.order);
        if (sort === 'title') return (a.dataset.title || '').localeCompare(b.dataset.title || '');
        return Number(a.dataset.order) - Number(b.dataset.order);
      });
      ordered.forEach((card) => guideGrid?.append(card));
      const query = (guideInput?.value || '').trim().toLowerCase();
      let visible = 0;
      guideCards.forEach((card) => {
        const category = card.dataset.category || '';
        const matchesFilter = activeGuideFilter === 'all' || category.includes(activeGuideFilter);
        const matchesQuery = !query || (card.dataset.search || '').includes(query);
        const show = matchesFilter && matchesQuery;
        card.hidden = !show;
        if (show) visible += 1;
      });
      if (guideCount) guideCount.textContent = String(visible);
      if (guideEmpty) guideEmpty.hidden = visible !== 0;
    };
    const guideButtons = $$('[data-guide-filter]', guideLibrary);
    setActiveToggle(guideButtons, guideButtons.find((button) => button.classList.contains('is-active')) || guideButtons[0]);
    guideButtons.forEach((button) => button.addEventListener('click', () => {
      activeGuideFilter = button.dataset.guideFilter || 'all';
      setActiveToggle(guideButtons, button);
      renderGuides();
    }));
    guideInput?.addEventListener('input', renderGuides);
    guideSort?.addEventListener('change', renderGuides);
  }

  // Gear-library search and job filters.
  const gearLibrary = $('[data-gear-library]');
  if (gearLibrary) {
    const gearInput = $('[data-gear-search]', gearLibrary);
    const gearCards = $$('[data-gear-card]', gearLibrary);
    const gearEmpty = $('[data-gear-empty]', gearLibrary);
    const gearCount = $('[data-gear-count]', gearLibrary);
    let activeGearFilter = 'all';
    const renderGear = () => {
      const query = (gearInput?.value || '').trim().toLowerCase();
      let visible = 0;
      gearCards.forEach((card) => {
        const categories = card.dataset.category || '';
        const matchesFilter = activeGearFilter === 'all' || categories.split(' ').includes(activeGearFilter);
        const matchesQuery = !query || (card.dataset.search || '').includes(query);
        const show = matchesFilter && matchesQuery;
        card.hidden = !show;
        if (show) visible += 1;
      });
      if (gearCount) gearCount.textContent = String(visible);
      if (gearEmpty) gearEmpty.hidden = visible !== 0;
    };
    const gearButtons = $$('[data-gear-filter]', gearLibrary);
    setActiveToggle(gearButtons, gearButtons.find((button) => button.classList.contains('is-active')) || gearButtons[0]);
    gearButtons.forEach((button) => button.addEventListener('click', () => {
      activeGearFilter = button.dataset.gearFilter || 'all';
      setActiveToggle(gearButtons, button);
      renderGear();
    }));
    gearInput?.addEventListener('input', renderGear);
  }

  // Strain library filters.
  const filterBar = $('[data-strain-filter]');
  const strainCards = $$('[data-strain-card]');
  if (filterBar && strainCards.length) {
    const strainInput = $('[data-strain-search]', filterBar);
    const emptyState = $('[data-strain-empty]');
    let activeFilter = 'all';
    let activeCannabinoid = 'all';
    const renderStrains = () => {
      const query = (strainInput?.value || '').trim().toLowerCase();
      let visible = 0;
      strainCards.forEach((card) => {
        const matchesFilter = activeFilter === 'all' || card.dataset.lean === activeFilter;
        const matchesCannabinoid = activeCannabinoid === 'all' || card.dataset.cannabinoid === activeCannabinoid;
        const matchesQuery = !query || (card.dataset.search || '').includes(query);
        const show = matchesFilter && matchesCannabinoid && matchesQuery;
        card.hidden = !show;
        if (show) visible += 1;
      });
      const count = $('[data-strain-count]');
      if (count) count.textContent = String(visible);
      if (emptyState) emptyState.hidden = visible !== 0;
    };
    const leanButtons = $$('[data-filter]', filterBar);
    const cannabinoidButtons = $$('[data-cannabinoid-filter]', filterBar);
    setActiveToggle(leanButtons, leanButtons.find((button) => button.classList.contains('is-active')) || leanButtons[0]);
    setActiveToggle(cannabinoidButtons, cannabinoidButtons.find((button) => button.classList.contains('is-active')) || cannabinoidButtons[0]);
    leanButtons.forEach((button) => button.addEventListener('click', () => {
      activeFilter = button.dataset.filter || 'all';
      setActiveToggle(leanButtons, button);
      renderStrains();
    }));
    cannabinoidButtons.forEach((button) => button.addEventListener('click', () => {
      activeCannabinoid = button.dataset.cannabinoidFilter || 'all';
      setActiveToggle(cannabinoidButtons, button);
      renderStrains();
    }));
    strainInput?.addEventListener('input', renderStrains);
  }

  // Fifty-state legal library search and status filters.
  const stateLibrary = $('[data-state-library]');
  const stateCards = $$('[data-state-card]');
  if (stateLibrary && stateCards.length) {
    const stateInput = $('[data-state-search]', stateLibrary);
    const emptyState = $('[data-state-empty]', stateLibrary);
    let activeStatus = 'all';
    const renderStates = () => {
      const query = (stateInput?.value || '').trim().toLowerCase();
      let visible = 0;
      stateCards.forEach((card) => {
        const matchesStatus = activeStatus === 'all' || card.dataset.status === activeStatus;
        const matchesQuery = !query || (card.dataset.search || '').includes(query);
        const show = matchesStatus && matchesQuery;
        card.hidden = !show;
        if (show) visible += 1;
      });
      const count = $('[data-state-count]', stateLibrary);
      if (count) count.textContent = String(visible);
      if (emptyState) emptyState.hidden = visible !== 0;
    };
    const stateButtons = $$('[data-state-filter]', stateLibrary);
    setActiveToggle(stateButtons, stateButtons.find((button) => button.classList.contains('is-active')) || stateButtons[0]);
    stateButtons.forEach((button) => button.addEventListener('click', () => {
      activeStatus = button.dataset.stateFilter || 'all';
      setActiveToggle(stateButtons, button);
      renderStates();
    }));
    stateInput?.addEventListener('input', renderStates);
  }

  // Article table of contents and reading progress.
  const article = $('[data-article]');
  const toc = $('[data-toc]');
  if (article && toc) {
    const headings = $$('h2[id]', article);
    toc.innerHTML = headings.map((heading) => `<a href="#${heading.id}">${escapeHtml(heading.textContent.trim())}</a>`).join('');
    if ('IntersectionObserver' in window) {
      const links = [...$$('a', toc), ...$$('a', $('[data-mobile-toc]'))];
      const observer = new IntersectionObserver((entries) => {
        const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
        if (!visible) return;
        links.forEach((link) => link.classList.toggle('is-active', link.getAttribute('href') === `#${visible.target.id}`));
      }, {rootMargin:'-20% 0px -68% 0px', threshold:0});
      headings.forEach((heading) => observer.observe(heading));
    }
  }
  const progress = $('[data-reading-progress]');
  if (progress && article) {
    const updateProgress = () => {
      const start = article.getBoundingClientRect().top + window.scrollY - 140;
      const end = start + article.offsetHeight - window.innerHeight;
      const ratio = Math.min(1, Math.max(0, (window.scrollY - start) / Math.max(1, end - start)));
      progress.style.width = `${ratio * 100}%`;
    };
    updateProgress();
    window.addEventListener('scroll', updateProgress, {passive:true});
    window.addEventListener('resize', updateProgress);
  }

  // Share link.
  $('[data-copy-link]')?.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      toast('Article link copied.');
    } catch (_) {
      window.prompt('Copy this link:', window.location.href);
    }
  });

  const citationButton = $('[data-copy-citation]');
  citationButton?.addEventListener('click', async () => {
    const accessed = new Intl.DateTimeFormat('en-US', {month:'long', day:'numeric', year:'numeric'}).format(new Date());
    const citation = `Big Bud Man. â€œ${citationButton.dataset.citationTitle}.â€ Reviewed ${citationButton.dataset.citationReviewed}. ${window.location.href} Accessed ${accessed}.`;
    try {
      await navigator.clipboard.writeText(citation);
      toast('Article citation copied.');
    } catch (_) {
      window.prompt('Copy this citation:', citation);
    }
  });

  // Articles with checklist markup get one portable, plain-text copy action.
  // The export keeps each section heading and includes the review date and
  // canonical URL so a shopping, appointment, or safety note keeps its source.
  const checklistLists = article ? $$('ul.checklist', article) : [];
  let checklistButton = $('[data-copy-checklists]');
  if (checklistLists.length && !checklistButton) {
    const actions = $('.article-actions');
    checklistButton = document.createElement('button');
    checklistButton.className = 'share-button';
    checklistButton.type = 'button';
    checklistButton.dataset.copyChecklists = '';
    checklistButton.textContent = 'Copy checklists';
    actions?.insertBefore(checklistButton, $('[data-print-article]', actions));
  }
  checklistButton?.addEventListener('click', async () => {
    const groups = checklistLists.map((list) => {
      const section = list.closest('section');
      const heading = $('h2', section)?.textContent.trim() || 'Checklist';
      const items = $$(':scope > li', list).map((item) => `- ${item.textContent.replace(/\s+/g, ' ').trim()}`);
      return `${heading}\n${items.join('\n')}`;
    });
    const canonical = $('link[rel="canonical"]')?.href || window.location.href;
    const title = citationButton?.dataset.citationTitle || document.title.replace(/\s*\|\s*Big Bud Man\s*$/, '');
    const reviewed = citationButton?.dataset.citationReviewed || 'review date shown on page';
    const text = `${title}\nReviewed ${reviewed}\n${canonical}\n\n${groups.join('\n\n')}`;
    try {
      await navigator.clipboard.writeText(text);
      toast(`Article checklists copied (${checklistLists.length}).`);
    } catch (_) {
      window.prompt('Copy these checklists:', text);
    }
  });

  $('[data-print-article]')?.addEventListener('click', () => window.print());

  // Compare three exact grow-light ownership records. This deliberately does
  // not approve a circuit, model plant response, or estimate crop yield.
  const growComparison = $('[data-grow-light-comparison]');
  if (growComparison) {
    const read = (root, selector, maximum = Number.POSITIVE_INFINITY) => {
      const node = $(selector, root);
      const raw = node?.value.trim();
      if (!raw) return null;
      const value = Number(raw);
      return Number.isFinite(value) ? Math.min(maximum, Math.max(0, value)) : null;
    };
    const money = (value) => value.toLocaleString(undefined, {style:'currency', currency:'USD'});
    const renderGrowComparison = () => {
      const hours = read(growComparison, '[data-grow-hours]', 24);
      const days = read(growComparison, '[data-grow-days]', 366);
      const rate = read(growComparison, '[data-grow-rate]');
      const years = read(growComparison, '[data-grow-years]');
      const sharedComplete = hours !== null && days !== null && rate !== null && years !== null && years > 0;
      let complete = 0;
      const columns = ['A', 'B', 'C'];
      const priceNodes = $$('[data-grow-price]', growComparison);
      const countNodes = $$('[data-grow-count]', growComparison);
      const wattsNodes = $$('[data-grow-watts]', growComparison);
      const setupNodes = $$('[data-grow-setup]', growComparison);
      const maintenanceNodes = $$('[data-grow-maintenance]', growComparison);
      const loadNodes = $$('[data-grow-load]', growComparison);
      const energyNodes = $$('[data-grow-energy]', growComparison);
      const electricityNodes = $$('[data-grow-electricity]', growComparison);
      const acquisitionNodes = $$('[data-grow-acquisition]', growComparison);
      const totalNodes = $$('[data-grow-total]', growComparison);
      const annualizedNodes = $$('[data-grow-annualized]', growComparison);
      columns.forEach((_, index) => {
        const values = [priceNodes, countNodes, wattsNodes, setupNodes, maintenanceNodes].map((nodes) => {
          const raw = nodes[index]?.value.trim();
          if (!raw) return null;
          const value = Number(raw);
          return Number.isFinite(value) ? Math.max(0, value) : null;
        });
        const optionComplete = sharedComplete && values.every((value) => value !== null) && values[1] > 0;
        if (!optionComplete) {
          [loadNodes, energyNodes, electricityNodes, acquisitionNodes, totalNodes, annualizedNodes].forEach((nodes) => {
            nodes[index].textContent = 'â€”';
          });
          return;
        }
        complete += 1;
        const [price, count, watts, setup, maintenance] = values;
        const load = watts * count;
        const annualEnergy = load * hours * days / 1000;
        const annualElectricity = annualEnergy * rate;
        const acquisition = price * count + setup;
        const total = acquisition + (annualElectricity + maintenance) * years;
        loadNodes[index].textContent = `${load.toLocaleString(undefined, {maximumFractionDigits:1})} W`;
        energyNodes[index].textContent = `${annualEnergy.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})} kWh`;
        electricityNodes[index].textContent = money(annualElectricity);
        acquisitionNodes[index].textContent = money(acquisition);
        totalNodes[index].textContent = money(total);
        annualizedNodes[index].textContent = money(total / years);
      });
      const status = $('[data-grow-status]', growComparison);
      status.textContent = !sharedComplete
        ? 'Complete the shared operating assumptions and use a planning horizon above zero.'
        : complete
          ? `${complete} complete exact-model option${complete === 1 ? '' : 's'} calculated. Blank or partial columns remain unknown.`
          : 'Complete at least one option. Enter zero only when a documented cost is truly zero.';
    };
    $$('input', growComparison).forEach((input) => input.addEventListener('input', renderGrowComparison));
    $('[data-grow-reset]', growComparison)?.addEventListener('click', () => {
      $$('input', growComparison).forEach((input) => { input.value = ''; });
      $('[data-grow-days]', growComparison).value = '365';
      $('[data-grow-years]', growComparison).value = '3';
      renderGrowComparison();
    });
    renderGrowComparison();
  }

  // Pre-roll package arithmetic. It normalizes labeled quantity and receipt
  // price only; it deliberately does not estimate inhaled dose or quality.
  const prerollPlanner = $('[data-preroll-planner]');
  if (prerollPlanner) {
    const number = (selector) => {
      const value = Number($(selector, prerollPlanner)?.value || 0);
      return Number.isFinite(value) ? Math.max(0, value) : 0;
    };
    const money = (value) => value.toLocaleString(undefined, {style:'currency', currency:'USD'});
    const renderPreroll = () => {
      const price = number('[data-preroll-price]');
      const count = number('[data-preroll-count]');
      const grams = number('[data-preroll-grams]');
      $('[data-preroll-unit]', prerollPlanner).textContent = `${(count > 0 ? grams / count : 0).toFixed(2)} g`;
      $('[data-preroll-each]', prerollPlanner).textContent = money(count > 0 ? price / count : 0);
      $('[data-preroll-per-gram]', prerollPlanner).textContent = money(grams > 0 ? price / grams : 0);
    };
    $$('input', prerollPlanner).forEach((input) => input.addEventListener('input', renderPreroll));
    renderPreroll();
  }

  // Rolling-paper and cone arithmetic compares delivered price with the
  // usable quantity received. It does not estimate consumption, combustion
  // performance, exposure, or product quality.
  const paperComparison = $('[data-paper-comparison]');
  if (paperComparison) {
    const readAt = (nodes, index) => {
      const raw = nodes[index]?.value.trim();
      if (!raw) return null;
      const value = Number(raw);
      return Number.isFinite(value) ? Math.max(0, value) : null;
    };
    const money = (value) => value === null ? 'â€”' : value.toLocaleString(undefined, {style:'currency', currency:'USD'});
    const prices = $$('[data-paper-price]', paperComparison);
    const fees = $$('[data-paper-fees]', paperComparison);
    const counts = $$('[data-paper-count]', paperComparison);
    const unusable = $$('[data-paper-unusable]', paperComparison);
    const delivered = $$('[data-paper-delivered]', paperComparison);
    const usable = $$('[data-paper-usable]', paperComparison);
    const unit = $$('[data-paper-unit]', paperComparison);
    const loss = $$('[data-paper-loss]', paperComparison);
    const renderPaperComparison = () => {
      let complete = 0;
      for (let index = 0; index < 3; index += 1) {
        const price = readAt(prices, index);
        const fee = readAt(fees, index) ?? 0;
        const count = readAt(counts, index);
        const damaged = readAt(unusable, index) ?? 0;
        const hasOption = price !== null || count !== null || readAt(fees, index) !== null || readAt(unusable, index) !== null;
        const deliveredCost = price !== null ? price + fee : null;
        const usableCount = count !== null ? Math.max(0, count - damaged) : null;
        const perUsable = deliveredCost !== null && usableCount > 0 ? deliveredCost / usableCount : null;
        const lossRate = count > 0 ? Math.min(1, damaged / count) : null;
        delivered[index].textContent = hasOption ? money(deliveredCost) : 'â€”';
        usable[index].textContent = usableCount === null ? 'â€”' : usableCount.toLocaleString(undefined, {maximumFractionDigits:2});
        unit[index].textContent = money(perUsable);
        loss[index].textContent = lossRate === null ? 'â€”' : `${(lossRate * 100).toFixed(1)}%`;
        if (price !== null && count > 0 && usableCount > 0) complete += 1;
      }
      const status = $('[data-paper-status]', paperComparison);
      if (status) status.textContent = complete ? `${complete} complete option${complete === 1 ? '' : 's'} updated locally. Compare fit, disclosure, condition, seller, and safety before cost.` : 'Enter the delivered price and pack count for each option you want to compare. Blank options stay unknown.';
    };
    $$('input', paperComparison).forEach((input) => input.addEventListener('input', renderPaperComparison));
    $('[data-paper-reset]', paperComparison)?.addEventListener('click', () => {
      $$('input', paperComparison).forEach((input) => { input.value = ''; });
      renderPaperComparison();
      prices[0]?.focus();
    });
    renderPaperComparison();
  }

  // Product comparison arithmetic. The rows normalize only entered checkout
  // and label values; blanks remain unknown and no result scores quality.
  const packageComparison = $('[data-package-comparison]');
  if (packageComparison) {
    const money = (value) => value.toLocaleString(undefined, {style:'currency', currency:'USD'});
    const numberAt = (nodes, index) => {
      const field = nodes[index];
      if (!field || field.value.trim() === '') return null;
      const value = Number(field.value);
      return Number.isFinite(value) ? Math.max(0, value) : null;
    };
    const prices = $$('[data-compare-price]', packageComparison);
    const taxes = $$('[data-compare-tax]', packageComparison);
    const fees = $$('[data-compare-fees]', packageComparison);
    const counts = $$('[data-compare-count]', packageComparison);
    const quantities = $$('[data-compare-quantity]', packageComparison);
    const milligrams = $$('[data-compare-mg]', packageComparison);
    const totals = $$('[data-compare-total]', packageComparison);
    const perUnit = $$('[data-compare-per-unit]', packageComparison);
    const perQuantity = $$('[data-compare-per-quantity]', packageComparison);
    const perHundred = $$('[data-compare-per-100]', packageComparison);
    const status = $('[data-compare-status]', packageComparison);
    const renderComparison = () => {
      let completed = 0;
      for (let index = 0; index < 3; index += 1) {
        const price = numberAt(prices, index);
        const tax = numberAt(taxes, index);
        const fee = numberAt(fees, index);
        const count = numberAt(counts, index);
        const quantity = numberAt(quantities, index);
        const mg = numberAt(milligrams, index);
        // A checkout total is only comparable when every checkout component
        // is known. Treating a blank tax or fee as zero would manufacture a
        // lower total and contradict the worksheet's blank-as-unknown rule.
        const total = price !== null && tax !== null && fee !== null ? price + tax + fee : null;
        if (total !== null) completed += 1;
        totals[index].textContent = total === null ? 'â€”' : money(total);
        perUnit[index].textContent = total !== null && count > 0 ? money(total / count) : 'â€”';
        perQuantity[index].textContent = total !== null && quantity > 0 ? money(total / quantity) : 'â€”';
        perHundred[index].textContent = total !== null && mg > 0 ? money(total * 100 / mg) : 'â€”';
      }
      if (status) status.textContent = completed ? `${completed} checkout total${completed === 1 ? '' : 's'} updated locally. Blanks remain unknown.` : 'Worksheet ready. Blank fields remain unknown.';
    };
    $$('input', packageComparison).forEach((input) => input.addEventListener('input', renderComparison));
    $('[data-compare-reset]', packageComparison)?.addEventListener('click', () => {
      $$('input', packageComparison).forEach((input) => { input.value = ''; });
      renderComparison();
      if (status) status.textContent = 'Worksheet cleared.';
      $$('input', packageComparison)[0]?.focus();
    });
    renderComparison();
  }

  // Edible label arithmetic checks whether serving, unit, and package fields
  // reconcile. It deliberately does not suggest a dose or infer accuracy.
  const edibleMath = $('[data-edible-math]');
  if (edibleMath) {
    const number = (selector) => {
      const node = $(selector, edibleMath);
      if (!node || node.value.trim() === '') return null;
#}zâÚ$z{-®éÜj×FW"F†RW†7BÖöFVÎ(	—26Öö¶R4E"FòW7F–ÖFRFVÆ—fW&VB—"6†ævW2âs°¢VÇ6R–b‚–V'2’7FGW2çFW‡D6öçFVçBÒu6—¦–ær—2f–Æ&ÆRâVçFW"æöç¦W&òÆææ–ær†÷&—¦öâf÷"F÷FÂæBæçVÆ—¦VB6÷7Bâs°¢VÇ6R7FGW2çFW‡D6öçFVçBÒ6G"ãÒæVVFVBòtÖF‚WFFVBÆö6ÆÇ’âF†RVçFW&VB6Öö¶R4E"ÖVWG2F†R&ööÒ×föÇVÖRÖF§W7FVB7F'F–ærö–çC²fW&–g’F†R&F–ærB7VVB–÷Rv–ÆÂ'Vââr¢tÖF‚WFFVBÆö6ÆÇ’âF†RVçFW&VB6Öö¶R4E"—2&VÆ÷rF†R&ööÒ×föÇVÖRÖF§W7FVB7F'F–ærö–çC²6ö×&Ræ÷F†W"7VVBÂVæ—BÂ÷"6öæf–wW&F–öââs°¢Ð¢Ó°¢BB‚v–çWBrÂ—$6ÆVæW"’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW$—$6ÆVæW"’“°¢B‚u¶FFÖ—"×&W6WEÒrÂ—$6ÆVæW"“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂ—$6ÆVæW"’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢&VæFW$—$6ÆVæW"‚“°¢B‚u¶FFÖ—"ÖÆVæwF…ÒrÂ—$6ÆVæW"“òæfö7W2‚“°¢Ò“°¢&VæFW$—$6ÆVæW"‚“°¢Ð ¢òò&öGV7BÖæWWG&Â6ÆVæ–ærÖ¶—B&—F†ÖWF–2â—B&–6W2F†R&÷WF–æR'WBFöW0¢òòæ÷BFV6–FRÖFW&–Â6ö×F–&–Æ—G’Â6ÆVæÆ–æW72Â&W—"Â÷"6fWG’à¢6öç7B6ÆVæ–æt6÷7BÒB‚u¶FFÖ6ÆVæ–ærÖ6÷7EÒr“°¢–b†6ÆVæ–æt6÷7B’°¢6öç7BçVÖ&W"Ò‡6VÆV7F÷"’Óâ°¢6öç7BfÇVRÒçVÖ&W"‚B‡6VÆV7F÷"Â6ÆVæ–æt6÷7B“òçfÇVRÇÂ“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢°¢Ó°¢6öç7BÖöæW’Ò‡fÇVR’ÓâfÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ·7G–ÆS¢v7W'&Væ7’rÂ7W'&Væ7“¢uU4BwÒ“°¢6öç7BFV6–ÖÂÒ‡fÇVR’ÓâfÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ¶Ö†–×VÔg&7F–öäF–v—G3£'Ò“°¢6öç7B&VæFW$6ÆVæ–æt6÷7BÒ‚’Óâ°¢6öç7B¶—BÒçVÖ&W"‚u¶FFÖ6ÆVæ–ærÖ¶—EÒr“°¢6öç7BFööÇ2ÒçVÖ&W"‚u¶FFÖ6ÆVæ–ær×FööÇ5Òr“°¢6öç7B&÷GFÆRÒçVÖ&W"‚u¶FFÖ6ÆVæ–ærÖ&÷GFÆUÒr“°¢6öç7B––VÆD6÷VçBÒçVÖ&W"‚u¶FFÖ6ÆVæ–ær×––VÆEÒr“°¢6öç7Bg&WVVæ7’ÒçVÖ&W"‚u¶FFÖ6ÆVæ–ærÖg&WVVæ7•Òr“°¢6öç7B'G2ÒçVÖ&W"‚u¶FFÖ6ÆVæ–ær×'G5Òr“°¢6öç7BÖ–çWFW2ÒçVÖ&W"‚u¶FFÖ6ÆVæ–ærÖÖ–çWFW5Òr“°¢6öç7B–V'2ÒçVÖ&W"‚u¶FFÖ6ÆVæ–ær×–V'5Òr“°¢6öç7B7–6ÆRÒ––VÆD6÷VçBâò&÷GFÆRò––VÆD6÷VçB¢°¢6öç7B6÷VçBÒg&WVVæ7’¢#°¢6öç7B&V7W'&–ærÒ7–6ÆR¢6÷VçB²'G3°¢6öç7Bf—'7BÒ¶—B²FööÇ2²&V7W'&–æs°¢6öç7BF÷FÂÒ¶—B²FööÇ2²&V7W'&–ær¢–V'3°¢6öç7B†÷W'2ÒÖ–çWFW2¢6÷VçBòc°¢B‚u¶FFÖ6ÆVæ–ærÖ7–6ÆUÒrÂ6ÆVæ–æt6÷7B’çFW‡D6öçFVçBÒ––VÆD6÷VçBâòÖöæW’†7–6ÆR’¢~(	Bs°¢B‚u¶FFÖ6ÆVæ–ærÖ6÷VçEÒrÂ6ÆVæ–æt6÷7B’çFW‡D6öçFVçBÒFV6–ÖÂ†6÷VçB“°¢B‚u¶FFÖ6ÆVæ–ærÖf—'7EÒrÂ6ÆVæ–æt6÷7B’çFW‡D6öçFVçBÒÖöæW’†f—'7B“°¢B‚u¶FFÖ6ÆVæ–ær×F÷FÅÒrÂ6ÆVæ–æt6÷7B’çFW‡D6öçFVçBÒ–V'2âòÖöæW’‡F÷FÂ’¢~(	Bs°¢B‚u¶FFÖ6ÆVæ–ærÖæçVÅÒrÂ6ÆVæ–æt6÷7B’çFW‡D6öçFVçBÒ–V'2âòÖöæW’‡F÷FÂò–V'2’¢~(	Bs°¢B‚u¶FFÖ6ÆVæ–ærÖ†÷W'5ÒrÂ6ÆVæ–æt6÷7B’çFW‡D6öçFVçBÒG¶FV6–ÖÂ††÷W'2—Ò†÷W'6°¢6öç7B7FGW2ÒB‚u¶FFÖ6ÆVæ–ær×7FGW5ÒrÂ6ÆVæ–æt6÷7B“°¢–b‡7FGW2’°¢–b‚––VÆD6÷VçBbb&÷GFÆRâ’7FGW2çFW‡D6öçFVçBÒtVçFW"æöç¦W&òW7F–ÖFVBçVÖ&W"öb6ÆVæ–æw2W"6öçF–æW"Fò6Æ7VÆFR6ÆVæW"6÷7BW"7–6ÆRâs°¢VÇ6R–b‚–V'2’7FGW2çFW‡D6öçFVçBÒtVçFW"æöç¦W&òÆææ–ær†÷&—¦öâFò6Æ7VÆFRF÷FÂæBæçVÆ—¦VB6÷7Bâs°¢VÇ6R7FGW2çFW‡D6öçFVçBÒtÖF‚WFFVBÆö6ÆÇ’âfW&–g’6ö×F–&–Æ—G’Â&WÆ6VÖVçB–çFW'fÇ2ÂæBWfW'’–çWBf÷"F†RW†7BFööÂæB7WÆ–W2âs°¢Ð¢Ó°¢BB‚v–çWBrÂ6ÆVæ–æt6÷7B’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW$6ÆVæ–æt6÷7B’“°¢B‚u¶FFÖ6ÆVæ–ær×&W6WEÒrÂ6ÆVæ–æt6÷7B“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂ6ÆVæ–æt6÷7B’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢&VæFW$6ÆVæ–æt6÷7B‚“°¢B‚u¶FFÖ6ÆVæ–ærÖ¶—EÒrÂ6ÆVæ–æt6÷7B“òæfö7W2‚“°¢Ò“°¢&VæFW$6ÆVæ–æt6÷7B‚“°¢Ð ¢òòf—fR×&VF–ær†öÖR67&VVâ6W&FW2&WVF&–Æ—G’g&öÒ&–2æB&–6W0¢òòF†R6ö×ÆWFR÷væW'6†—7—7FVÒâ—BFöW2æ÷B6Æ–'&FR÷"6W'F–g’66ÆRà¢6öç7B66ÆT6†V6²ÒB‚u¶FF×66ÆRÖ6†V6µÒr“°¢–b‡66ÆT6†V6²’°¢6öç7B–çWDçVÖ&W"Ò‡6VÆV7F÷"’Óâ°¢6öç7B–çWBÒB‡6VÆV7F÷"Â66ÆT6†V6²“°¢6öç7BfÇVRÒçVÖ&W"†–çWCòçfÇVRÇÂ“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢°¢Ó°¢6öç7BÖöæW’Ò‡fÇVR’ÓâfÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ·7G–ÆS¢v7W'&Væ7’rÂ7W'&Væ7“¢uU4BwÒ“°¢6öç7BFV6–ÖÂÒ‡fÇVR’ÓâfÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ¶Ö–æ–×VÔg&7F–öäF–v—G3£2ÂÖ†–×VÔg&7F–öäF–v—G3£7Ò“°¢6öç7B&VæFW%66ÆT6†V6²Ò‚’Óâ°¢6öç7B&VfW&Væ6RÒ–çWDçVÖ&W"‚u¶FF×66ÆR×&VfW&Væ6UÒr“°¢6öç7BFöÆW&æ6T–çWBÒB‚u¶FF×66ÆR×FöÆW&æ6UÒrÂ66ÆT6†V6²“°¢6öç7BFöÆW&æ6RÒ–çWDçVÖ&W"‚u¶FF×66ÆR×FöÆW&æ6UÒr“°¢6öç7B&VF–æt–çWG2ÒBB‚u¶FF×66ÆR×&VF–æuÒrÂ66ÆT6†V6²“°¢6öç7B&VF–æw2Ò&VF–æt–çWG0¢æf–ÇFW"‚†–çWB’Óâ–çWBçfÇVRçG&–Ò‚’ÓÒrrbbçVÖ&W"æ—4f–æ—FR„çVÖ&W"†–çWBçfÇVR’’bbçVÖ&W"†–çWBçfÇVR’ãÒ¢æÖ‚†–çWB’ÓâçVÖ&W"†–çWBçfÇVR’“°¢6öç7B6ö×ÆWFRÒ&VfW&Væ6Râbb&VF–æw2æÆVæwF‚ÓÓÒS°¢6öç7BÖVâÒ6ö×ÆWFRò&VF–æw2ç&VGV6R‚‡7VÒÂfÇVR’Óâ7VÒ²fÇVRÂ’ò&VF–æw2æÆVæwF‚¢°¢6öç7B7&VBÒ6ö×ÆWFRòÖF‚æÖ‚‚ââç&VF–æw2’ÒÖF‚æÖ–â‚ââç&VF–æw2’¢°¢6öç7BFWf–F–öâÒ6ö×ÆWFRòÖF‚æÖ‚‚ââç&VF–æw2æÖ‚‡fÇVR’ÓâÖF‚æ'2‡fÇVRÒ&VfW&Væ6R’’’¢°¢6öç7B†5FöÆW&æ6RÒ&ööÆVâ‡FöÆW&æ6T–çWCòçfÇVRçG&–Ò‚’“°¢6öç7B&–6RÒ–çWDçVÖ&W"‚u¶FF×66ÆR×&–6UÒr“°¢6öç7BvV–v‡BÒ–çWDçVÖ&W"‚u¶FF×66ÆR×vV–v‡BÖ6÷7EÒr“°¢6öç7B÷vW"Ò–çWDçVÖ&W"‚u¶FF×66ÆR×÷vW%Òr“°¢6öç7B–V'2Ò–çWDçVÖ&W"‚u¶FF×66ÆR×–V'5Òr“°¢6öç7Bf—'7BÒ&–6R²vV–v‡B²÷vW#°¢6öç7BF÷FÂÒ&–6R²vV–v‡B²÷vW"¢–V'3°¢B‚u¶FF×66ÆRÖÖVåÒrÂ66ÆT6†V6²’çFW‡D6öçFVçBÒ6ö×ÆWFRòG¶FV6–ÖÂ†ÖVâ—Òv¢~(	Bs°¢B‚u¶FF×66ÆR×7&VEÒrÂ66ÆT6†V6²’çFW‡D6öçFVçBÒ6ö×ÆWFRòG¶FV6–ÖÂ‡7&VB—Òv¢~(	Bs°¢B‚u¶FF×66ÆRÖFWf–F–öåÒrÂ66ÆT6†V6²’çFW‡D6öçFVçBÒ6ö×ÆWFRòG¶FV6–ÖÂ†FWf–F–öâ—Òv¢~(	Bs°¢B‚u¶FF×66ÆR×FöÆW&æ6R×&W7VÇEÒrÂ66ÆT6†V6²’çFW‡D6öçFVçBÒ6ö×ÆWFRbb†5FöÆW&æ6Rò†FWf–F–öâÃÒFöÆW&æ6R²RÓ’òuv—F†–âVçFW&VBFöÆW&æ6Rr¢t÷WG6–FRVçFW&VBFöÆW&æ6Rr’¢~(	Bs°¢B‚u¶FF×66ÆRÖf—'7EÒrÂ66ÆT6†V6²’çFW‡D6öçFVçBÒÖöæW’†f—'7B“°¢B‚u¶FF×66ÆR×F÷FÅÒrÂ66ÆT6†V6²’çFW‡D6öçFVçBÒ–V'2âòÖöæW’‡F÷FÂ’¢~(	Bs°¢B‚u¶FF×66ÆRÖæçVÅÒrÂ66ÆT6†V6²’çFW‡D6öçFVçBÒ–V'2âòÖöæW’‡F÷FÂò–V'2’¢~(	Bs°¢6öç7B7FGW2ÒB‚u¶FF×66ÆR×7FGW5ÒrÂ66ÆT6†V6²“°¢–b‡7FGW2’°¢–b‚&VfW&Væ6RÇÂ&VF–æw2æÆVæwF‚ÓÒR’7FGW2çFW‡D6öçFVçBÒtVçFW"æöç¦W&ò&VfW&Væ6RæBÆÂf—fR&VF–æw2Fò6Æ7VÆFRF†R&WVF&–Æ—G’67&VVââs°¢VÇ6R–b‚†5FöÆW&æ6R’7FGW2çFW‡D6öçFVçBÒu&VF–ærÖF‚—2f–Æ&ÆRâVçFW"F†RW†7BÖ¶W"FöÆW&æ6R–b–÷RvçBFöÆW&æ6R67&VVââs°¢VÇ6R–b‚–V'2’7FGW2çFW‡D6öçFVçBÒu&VF–ærÖF‚—2f–Æ&ÆRâVçFW"æöç¦W&òÆææ–ær†÷&—¦öâf÷"F÷FÂæBæçVÆ—¦VB6÷7Bâs°¢VÇ6R7FGW2çFW‡D6öçFVçBÒtÖF‚WFFVBÆö6ÆÇ’âF†—2—2öæR×ö–çB†öÖR67&VVâÂæ÷B6Æ–'&F–öâÂ6W'F–f–6F–öâÂ÷"v†öÆR×&ævRW&f÷&Öæ6RWf–FVæ6Râs°¢Ð¢Ó°¢BB‚v–çWBrÂ66ÆT6†V6²’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW%66ÆT6†V6²’“°¢B‚u¶FF×66ÆR×&W6WEÒrÂ66ÆT6†V6²“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂ66ÆT6†V6²’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢&VæFW%66ÆT6†V6²‚“°¢B‚u¶FF×66ÆR×&VfW&Væ6UÒrÂ66ÆT6†V6²“òæfö7W2‚“°¢Ò“°¢&VæFW%66ÆT6†V6²‚“°¢Ð ¢òòÆö6¶&÷‚ÖF‚6†V6·2âW&–v‡B&V7FæwVÆ"6¶vRÆöBv–ç7B7FFV@¢òòW6&ÆR–çFW&–÷"F–ÖVç6–öç2â—BFVÆ–&W&FVÇ’FöW2æ÷B66÷&R6V7W&—G’À¢òò6†–ÆB&W6—7Fæ6RÂöF÷"6öçG&öÂÂÖFW&–Ç2Â÷"—'&VwVÆ"ö'7G'V7F–öç2à¢6öç7BÆö6¶&÷„6ö×&—6öâÒB‚u¶FFÖÆö6¶&÷‚Ö6ö×&—6öåÒr“°¢–b†Æö6¶&÷„6ö×&—6öâ’°¢6öç7B&VBÒ‡6VÆV7F÷"’Óâ°¢6öç7B–çWBÒB‡6VÆV7F÷"ÂÆö6¶&÷„6ö×&—6öâ“°¢6öç7B&rÒ–çWCòçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7B&VDBÒ†æöFW2Â–æFW‚’Óâ°¢6öç7B&rÒæöFW5¶–æFW…ÓòçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7Bv–GF‡2ÒBB‚u¶FFÖÆö6²×v–GF…ÒrÂÆö6¶&÷„6ö×&—6öâ“°¢6öç7BFWF‡2ÒBB‚u¶FFÖÆö6²ÖFWF…ÒrÂÆö6¶&÷„6ö×&—6öâ“°¢6öç7B†V–v‡G2ÒBB‚u¶FFÖÆö6²Ö†V–v‡EÒrÂÆö6¶&÷„6ö×&—6öâ“°¢6öç7B6÷7G2ÒBB‚u¶FFÖÆö6²Ö6÷7EÒrÂÆö6¶&÷„6ö×&—6öâ“°¢6öç7Bf—G2ÒBB‚u¶FFÖÆö6²Öf—EÒrÂÆö6¶&÷„6ö×&—6öâ“°¢6öç7BÖ&v–ç2ÒBB‚u¶FFÖÆö6²ÖÖ&v–åÒrÂÆö6¶&÷„6ö×&—6öâ“°¢6öç7BföÇVÖW2ÒBB‚u¶FFÖÆö6²×föÇVÖUÒrÂÆö6¶&÷„6ö×&—6öâ“°¢6öç7BVæ—D6÷7G2ÒBB‚u¶FFÖÆö6²×Væ—BÖ6÷7EÒrÂÆö6¶&÷„6ö×&—6öâ“°¢6öç7BÖöæW’Ò‡fÇVR’ÓâfÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ·7G–ÆS¢v7W'&Væ7’rÂ7W'&Væ7“¢uU4BwÒ“°¢6öç7B&VæFW$Æö6¶&÷„6ö×&—6öâÒ‚’Óâ°¢6öç7BÆöEv–GF‚Ò&VB‚u¶FFÖÆö6²ÖÆöB×v–GF…Òr“°¢6öç7BÆöDFWF‚Ò&VB‚u¶FFÖÆö6²ÖÆöBÖFWF…Òr“°¢6öç7BÆöD†V–v‡BÒ&VB‚u¶FFÖÆö6²ÖÆöBÖ†V–v‡EÒr“°¢6öç7B6ÆV&æ6RÒ&VB‚u¶FFÖÆö6²Ö6ÆV&æ6UÒr’óò°¢6öç7BÆöD6ö×ÆWFRÒÆöEv–GF‚âbbÆöDFWF‚âbbÆöD†V–v‡Bâ°¢6öç7B&WV—&VBÒÆöD6ö×ÆWFRò¶ÆöEv–GF‚²6ÆV&æ6RÂÆöDFWF‚²6ÆV&æ6RÂÆöD†V–v‡B²6ÆV&æ6UÒ¢çVÆÃ°¢ÆWBF–ÖVç6–öæÄ÷F–öç2Ò°¢ÆWBf—GF–æt÷F–öç2Ò°¢f÷"†ÆWB–æFW‚Ò²–æFW‚Â3²–æFW‚³Ò’°¢6öç7Bv–GF‚Ò&VDB‡v–GF‡2Â–æFW‚“°¢6öç7BFWF‚Ò&VDB†FWF‡2Â–æFW‚“°¢6öç7B†V–v‡BÒ&VDB††V–v‡G2Â–æFW‚“°¢6öç7B6÷7BÒ&VDB†6÷7G2Â–æFW‚“°¢6öç7BF–ÖVç6–öç46ö×ÆWFRÒv–GF‚âbbFWF‚âbb†V–v‡Bâ°¢6öç7BföÇVÖRÒF–ÖVç6–öç46ö×ÆWFRòv–GF‚¢FWF‚¢†V–v‡B¢ãc3ƒs¢çVÆÃ°¢ÆWBf—BÒçVÆÃ°¢ÆWBÖ&v–âÒçVÆÃ°¢ÆWB÷&–VçFF–öâÒrs°¢–b†F–ÖVç6–öç46ö×ÆWFRbb&WV—&VB’°¢6öç7BVçFW&VDÖ&v–ç2Ò·v–GF‚Ò&WV—&VE³ÒÂFWF‚Ò&WV—&VE³ÒÂ†V–v‡BÒ&WV—&VE³%ÕÓ°¢6öç7B&÷FFVDÖ&v–ç2Ò·v–GF‚Ò&WV—&VE³ÒÂFWF‚Ò&WV—&VE³ÒÂ†V–v‡BÒ&WV—&VE³%ÕÓ°¢6öç7BVçFW&VDf—G2ÒVçFW&VDÖ&v–ç2æWfW'’‚‡fÇVR’ÓâfÇVRãÒÓRÓ’“°¢6öç7B&÷FFVDf—G2Ò&÷FFVDÖ&v–ç2æWfW'’‚‡fÇVR’ÓâfÇVRãÒÓRÓ’“°¢f—BÒVçFW&VDf—G2ÇÂ&÷FFVDf—G3°¢–b†f—B’°¢6öç7B6æF–FFW2ÒµÓ°¢–b†VçFW&VDf—G2’6æF–FFW2çW6‚‡¶Æ&VÃ¢tVçFW&VB&6RrÂÖ&v–ã¤ÖF‚æÖ–â‚ââæVçFW&VDÖ&v–ç2—Ò“°¢–b‡&÷FFVDf—G2’6æF–FFW2çW6‚‡¶Æ&VÃ¢t&6R&÷FFVB“+rÂÖ&v–ã¤ÖF‚æÖ–â‚ââç&÷FFVDÖ&v–ç2—Ò“°¢6öç7B&W7BÒ6æF–FFW2ç6÷'B‚†Â"’Óâ"æÖ&v–âÒæÖ&v–â•³Ó°¢Ö&v–âÒ&W7BæÖ&v–ã°¢÷&–VçFF–öâÒ&W7BæÆ&VÃ°¢f—GF–æt÷F–öç2³Ò°¢Ð¢Ð¢–b†F–ÖVç6–öç46ö×ÆWFR’F–ÖVç6–öæÄ÷F–öç2³Ò°¢f—G5¶–æFW…ÒçFW‡D6öçFVçBÒf—BÓÓÒçVÆÂò~(	Br¢f—Bòf—G2+rG¶÷&–VçFF–öçÖ¢tFöW2æ÷Bf—Bs°¢Ö&v–ç5¶–æFW…ÒçFW‡D6öçFVçBÒÖ&v–âÓÓÒçVÆÂò~(	Br¢G¶Ö&v–âçFôf—†VBƒ"—Ò–æ°¢föÇVÖW5¶–æFW…ÒçFW‡D6öçFVçBÒföÇVÖRÓÓÒçVÆÂò~(	Br¢G·föÇVÖRçFôf—†VBƒ"—ÒÆ°¢Væ—D6÷7G5¶–æFW…ÒçFW‡D6öçFVçBÒföÇVÖRâbb6÷7BÓÒçVÆÂòG¶ÖöæW’†6÷7BòföÇVÖR—ÒôÆ¢~(	Bs°¢Ð¢6öç7B7FGW2ÒB‚u¶FFÖÆö6²×7FGW5ÒrÂÆö6¶&÷„6ö×&—6öâ“°¢–b‚7FGW2’&WGW&ã°¢–b‚ÆöD6ö×ÆWFR’7FGW2çFW‡D6öçFVçBÒF–ÖVç6–öæÄ÷F–öç2òt–çFW&–÷"föÇVÖRæB6÷7B&R6†÷vââVçFW"ÆÂF‡&VRæöç¦W&ò6¶vRÖÆöBF–ÖVç6–öç2Fò6†V6²W&–v‡Bf—Bâr¢tVçFW"F†RÖV7W&VBW&–v‡B6¶vRÆöBæBâW†7BÖöFVÅÂw2W6&ÆR–çFW&–÷"F–ÖVç6–öç2â&Ææ²÷F–öç27F’Væ¶æ÷vââs°¢VÇ6R–b‚F–ÖVç6–öæÄ÷F–öç2’7FGW2çFW‡D6öçFVçBÒu6¶vRÆöB&V6÷&FVBâVçFW"ÖöFVÅÂw2F‡&VRæöç¦W&òW6&ÆR–çFW&–÷"F–ÖVç6–öç2Fò6†V6²f—Bâs°¢VÇ6R7FGW2çFW‡D6öçFVçBÒG¶f—GF–æt÷F–öç7ÒöbG¶F–ÖVç6–öæÄ÷F–öç7Ò6ö×ÆWFR÷F–öâG¶F–ÖVç6–öæÄ÷F–öç2ÓÓÒòrr¢w2wÒf—BF†RVçFW&VBW&–v‡BÆöB–âBÆV7BöæR&6R÷&–VçFF–öââ6V7W&—G’7F–ÆÂæVVG26W&FR&Wf–Wræ°¢Ó°¢BB‚v–çWBrÂÆö6¶&÷„6ö×&—6öâ’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW$Æö6¶&÷„6ö×&—6öâ’“°¢B‚u¶FFÖÆö6²×&W6WEÒrÂÆö6¶&÷„6ö×&—6öâ“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂÆö6¶&÷„6ö×&—6öâ’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢&VæFW$Æö6¶&÷„6ö×&—6öâ‚“°¢B‚u¶FFÖÆö6²ÖÆöB×v–GF…ÒrÂÆö6¶&÷„6ö×&—6öâ“òæfö7W2‚“°¢Ò“°¢&VæFW$Æö6¶&÷„6ö×&—6öâ‚“°¢Ð ¢òò7F6‚Ö¦"Æææ–ærW6W26–×ÆR7–Æ–æG&–6Â–çFW&–÷"æBVçFW&VB6÷7G2à¢òò—BæWfW"6öçfW'G2föÇVÖRFò6ææ&—2vV–v‡BÂF÷6RÂg&W6†æW72Â÷"VÆ—G’à¢6öç7B7F6„¦%ÆææW"ÒB‚u¶FF×7F6‚Ö¦"×ÆææW%Òr“°¢–b‡7F6„¦%ÆææW"’°¢6öç7B&VBÒ‡6VÆV7F÷"’Óâ°¢6öç7B&rÒB‡6VÆV7F÷"Â7F6„¦%ÆææW"“òçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7BÖöæW’Ò‡fÇVR’ÓâfÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ·7G–ÆS¢v7W'&Væ7’rÂ7W'&Væ7“¢uU4BwÒ“°¢6öç7BföÇVÖUFW‡BÒ‡fÇVR’ÓâG·fÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ¶Ö–æ–×VÔg&7F–öäF–v—G3£ÂÖ†–×VÔg&7F–öäF–v—G3£Ò—ÒÔÆ°¢6öç7B&VæFW%7F6„¦"Ò‚’Óâ°¢6öç7BF–ÖWFW"Ò&VB‚u¶FFÖ¦"ÖF–ÖWFW%Òr“°¢6öç7B†V–v‡BÒ&VB‚u¶FFÖ¦"Ö†V–v‡EÒr“°¢6öç7Bf–ÆÂÒ&VB‚u¶FFÖ¦"Öf–ÆÅÒr“°¢6öç7B&–6RÒ&VB‚u¶FFÖ¦"×&–6UÒr“°¢6öç7BæçVÂÒ&VB‚u¶FFÖ¦"ÖæçVÅÒr“°¢6öç7B–V'2Ò&VB‚u¶FFÖ¦"×–V'5Òr“°¢6öç7BF–ÖVç6–öç46ö×ÆWFRÒF–ÖWFW"âbb†V–v‡Bâ°¢6öç7Bf–ÆÄ6ö×ÆWFRÒf–ÆÂâbbf–ÆÂÃÒ°¢6öç7B6÷7G46ö×ÆWFRÒ&–6RÓÒçVÆÂbbæçVÂÓÒçVÆÂbb–V'2â°¢6öç7BföÇVÖRÒF–ÖVç6–öç46ö×ÆWFRòÖF‚å’¢†F–ÖWFW"ò"’¢¢"¢†V–v‡B¢çVÆÃ°¢6öç7Bv÷&¶–ærÒföÇVÖRÓÒçVÆÂbbf–ÆÄ6ö×ÆWFRòföÇVÖR¢f–ÆÂò¢çVÆÃ°¢6öç7B†VG76RÒföÇVÖRÓÒçVÆÂbbv÷&¶–ærÓÒçVÆÂòföÇVÖRÒv÷&¶–ær¢çVÆÃ°¢6öç7BF÷FÂÒ6÷7G46ö×ÆWFRò&–6R²æçVÂ¢–V'2¢çVÆÃ°¢B‚u¶FFÖ¦"×föÇVÖUÒrÂ7F6„¦%ÆææW"’çFW‡D6öçFVçBÒföÇVÖRÓÓÒçVÆÂò~(	Br¢föÇVÖUFW‡B‡föÇVÖR“°¢B‚u¶FFÖ¦"×v÷&¶–æuÒrÂ7F6„¦%ÆææW"’çFW‡D6öçFVçBÒv÷&¶–ærÓÓÒçVÆÂò~(	Br¢föÇVÖUFW‡B‡v÷&¶–ær“°¢B‚u¶FFÖ¦"Ö†VG76UÒrÂ7F6„¦%ÆææW"’çFW‡D6öçFVçBÒ†VG76RÓÓÒçVÆÂò~(	Br¢föÇVÖUFW‡B††VG76R“°¢B‚u¶FFÖ¦"Öf—'7EÒrÂ7F6„¦%ÆææW"’çFW‡D6öçFVçBÒ6÷7G46ö×ÆWFRòÖöæW’‡&–6R²æçVÂ’¢~(	Bs°¢B‚u¶FFÖ¦"×F÷FÅÒrÂ7F6„¦%ÆææW"’çFW‡D6öçFVçBÒF÷FÂÓÓÒçVÆÂò~(	Br¢ÖöæW’‡F÷FÂ“°¢B‚u¶FFÖ¦"ÖæçVÆ—¦VEÒrÂ7F6„¦%ÆææW"’çFW‡D6öçFVçBÒF÷FÂÓÓÒçVÆÂò~(	Br¢ÖöæW’‡F÷FÂò–V'2“°¢6öç7B7FGW2ÒB‚u¶FFÖ¦"×7FGW5ÒrÂ7F6„¦%ÆææW"“°¢–b‚F–ÖVç6–öç46ö×ÆWFR’7FGW2çFW‡D6öçFVçBÒtVçFW"æöç¦W&òW6&ÆRF–ÖWFW"æB†V–v‡Bâ6÷7Bf–VÆG2Ö’&R¦W&òöæÇ’v†VâF†BFö7VÖVçFVB6÷7B—2G'VÇ’¦W&òâs°¢VÇ6R–b‚f–ÆÄ6ö×ÆWFR’7FGW2çFW‡D6öçFVçBÒtVçFW"ÆææVBf–ÆÂg&öÒRF‡&÷Vv‚RâÆW72F†âR&W6W'fW2ÖV7W&VB†VG76Râs°¢VÇ6R–b‚6÷7G46ö×ÆWFR’7FGW2çFW‡D6öçFVçBÒuföÇVÖR6Æ7VÆFVBâVçFW"FVÆ—fW&VB6÷7BÂ–V&Ç’7W÷'FVB'G2æB6&RÂæBæöç¦W&òÆææ–ær†÷&—¦öâf÷"6÷7B&W7VÇG2âs°¢VÇ6R7FGW2çFW‡D6öçFVçBÒt66—G’æBVçFW&VB÷væW'6†—6÷7G26Æ7VÆFVBâfW&–g’F†R&VÂ6f—G’Â÷Væ–ærÂÆ–B–çG'W6–öâÂÖFW&–Ç2Â6Æ÷7W&RWf–FVæ6RÂæBÆö6¶VB×7F÷&vRf—Bâs°¢Ó°¢BB‚v–çWBrÂ7F6„¦%ÆææW"’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW%7F6„¦"’“°¢B‚u¶FFÖ¦"×&W6WEÒrÂ7F6„¦%ÆææW"“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂ7F6„¦%ÆææW"’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢B‚u¶FFÖ¦"Öf–ÆÅÒrÂ7F6„¦%ÆææW"’çfÇVRÒssRs°¢B‚u¶FFÖ¦"×–V'5ÒrÂ7F6„¦%ÆææW"’çfÇVRÒs2s°¢&VæFW%7F6„¦"‚“°¢B‚u¶FFÖ¦"ÖF–ÖWFW%ÒrÂ7F6„¦%ÆææW"“òæfö7W2‚“°¢Ò“°¢&VæFW%7F6„¦"‚“°¢Ð ¢òò&öÆÆ–ær×G&’ÖF‚¶VW2F†R&W&F–öâF6²æBF†RÆö6¶VB×7F÷&vP¢òò&ö&ÆVÒ6W&FRâ—B6†V6·26–×ÆR&V7FævÆW2öæÇ’æBæWfW"GW&ç2f—B÷ ¢òòVæ—B6÷7B–çFòÖFW&–Ç2Â7F&–Æ—G’Â6fWG’Â÷"VÆ—G’66÷&Rà¢6öç7BG&”6ö×&—6öâÒB‚u¶FF×G&’Ö6ö×&—6öåÒr“°¢–b‡G&”6ö×&—6öâ’°¢6öç7B&VBÒ‡6VÆV7F÷"’Óâ°¢6öç7B&rÒB‡6VÆV7F÷"ÂG&”6ö×&—6öâ“òçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7B&VDBÒ†æöFW2Â–æFW‚’Óâ°¢6öç7B&rÒæöFW5¶–æFW…ÓòçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7BW6&ÆUv–GF‡2ÒBB‚u¶FF×G&’×W6&ÆR×v–GF…ÒrÂG&”6ö×&—6öâ“°¢6öç7BW6&ÆTFWF‡2ÒBB‚u¶FF×G&’×W6&ÆRÖFWF…ÒrÂG&”6ö×&—6öâ“°¢6öç7B÷fW&ÆÅv–GF‡2ÒBB‚u¶FF×G&’Ö÷fW&ÆÂ×v–GF…ÒrÂG&”6ö×&—6öâ“°¢6öç7B÷fW&ÆÄFWF‡2ÒBB‚u¶FF×G&’Ö÷fW&ÆÂÖFWF…ÒrÂG&”6ö×&—6öâ“°¢6öç7B÷fW&ÆÄ†V–v‡G2ÒBB‚u¶FF×G&’Ö÷fW&ÆÂÖ†V–v‡EÒrÂG&”6ö×&—6öâ“°¢6öç7B6÷7G2ÒBB‚u¶FF×G&’Ö6÷7EÒrÂG&”6ö×&—6öâ“°¢6öç7BF6´f—G2ÒBB‚u¶FF×G&’×F6²Öf—EÒrÂG&”6ö×&—6öâ“°¢6öç7B7F÷&Tf—G2ÒBB‚u¶FF×G&’×7F÷&RÖf—EÒrÂG&”6ö×&—6öâ“°¢6öç7B&V2ÒBB‚u¶FF×G&’Ö&VÒrÂG&”6ö×&—6öâ“°¢6öç7BVæ—D6÷7G2ÒBB‚u¶FF×G&’×Væ—BÖ6÷7EÒrÂG&”6ö×&—6öâ“°¢6öç7BÖöæW’Ò‡fÇVR’ÓâfÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ·7G–ÆS¢v7W'&Væ7’rÂ7W'&Væ7“¢uU4BwÒ“°¢6öç7B&V7FævÆTf—G2Ò†÷WFW%v–GF‚Â÷WFW$FWF‚Â–ææW%v–GF‚Â–ææW$FWF‚’Óà¢†÷WFW%v–GF‚ÃÒ–ææW%v–GF‚²RÓ’bb÷WFW$FWF‚ÃÒ–ææW$FWF‚²RÓ’’ÇÀ¢†÷WFW$FWF‚ÃÒ–ææW%v–GF‚²RÓ’bb÷WFW%v–GF‚ÃÒ–ææW$FWF‚²RÓ’“°¢6öç7B&VæFW%G&”6ö×&—6öâÒ‚’Óâ°¢6öç7BF6µv–GF‚Ò&VB‚u¶FF×G&’×F6²×v–GF…Òr“°¢6öç7BF6´FWF‚Ò&VB‚u¶FF×G&’×F6²ÖFWF…Òr“°¢6öç7B6ÆV&æ6RÒ&VB‚u¶FF×G&’Ö6ÆV&æ6UÒr’óò°¢6öç7B7F÷&Uv–GF‚Ò&VB‚u¶FF×G&’×7F÷&R×v–GF…Òr“°¢6öç7B7F÷&TFWF‚Ò&VB‚u¶FF×G&’×7F÷&RÖFWF…Òr“°¢6öç7B7F÷&T†V–v‡BÒ&VB‚u¶FF×G&’×7F÷&RÖ†V–v‡EÒr“°¢6öç7BF6´6ö×ÆWFRÒF6µv–GF‚âbbF6´FWF‚â°¢6öç7B7F÷&T6ö×ÆWFRÒ7F÷&Uv–GF‚âbb7F÷&TFWF‚âbb7F÷&T†V–v‡Bâ°¢6öç7B&WV—&VEv–GF‚ÒF6´6ö×ÆWFRòF6µv–GF‚²6ÆV&æ6R¢"¢çVÆÃ°¢6öç7B&WV—&VDFWF‚ÒF6´6ö×ÆWFRòF6´FWF‚²6ÆV&æ6R¢"¢çVÆÃ°¢ÆWBVçFW&VBÒ°¢ÆWBF6µ76W2Ò°¢ÆWB7F÷&U76W2Ò°¢f÷"†ÆWB–æFW‚Ò²–æFW‚Â3²–æFW‚³Ò’°¢6öç7BW6&ÆUv–GF‚Ò&VDB‡W6&ÆUv–GF‡2Â–æFW‚“°¢6öç7BW6&ÆTFWF‚Ò&VDB‡W6&ÆTFWF‡2Â–æFW‚“°¢6öç7B÷fW&ÆÅv–GF‚Ò&VDB†÷fW&ÆÅv–GF‡2Â–æFW‚“°¢6öç7B÷fW&ÆÄFWF‚Ò&VDB†÷fW&ÆÄFWF‡2Â–æFW‚“°¢6öç7B÷fW&ÆÄ†V–v‡BÒ&VDB†÷fW&ÆÄ†V–v‡G2Â–æFW‚“°¢6öç7B6÷7BÒ&VDB†6÷7G2Â–æFW‚“°¢6öç7BW6&ÆT6ö×ÆWFRÒW6&ÆUv–GF‚âbbW6&ÆTFWF‚â°¢6öç7B÷fW&ÆÄ6ö×ÆWFRÒ÷fW&ÆÅv–GF‚âbb÷fW&ÆÄFWF‚âbb÷fW&ÆÄ†V–v‡Bâ°¢6öç7B†4÷F–öâÒW6&ÆT6ö×ÆWFRÇÂ÷fW&ÆÄ6ö×ÆWFRÇÂ6÷7BÓÒçVÆÃ°¢–b††4÷F–öâ’VçFW&VB³Ò°¢6öç7BF6´f—BÒF6´6ö×ÆWFRbbW6&ÆT6ö×ÆWFRò&V7FævÆTf—G2‡&WV—&VEv–GF‚Â&WV—&VDFWF‚ÂW6&ÆUv–GF‚ÂW6&ÆTFWF‚’¢çVÆÃ°¢6öç7B7F÷&Tf—BÒ7F÷&T6ö×ÆWFRbb÷fW&ÆÄ6ö×ÆWFRò÷fW&ÆÄ†V–v‡BÃÒ7F÷&T†V–v‡B²RÓ’bb&V7FævÆTf—G2†÷fW&ÆÅv–GF‚Â÷fW&ÆÄFWF‚Â7F÷&Uv–GF‚Â7F÷&TFWF‚’¢çVÆÃ°¢6öç7B&VÒW6&ÆT6ö×ÆWFRòW6&ÆUv–GF‚¢W6&ÆTFWF‚¢çVÆÃ°¢–b‡F6´f—B’F6µ76W2³Ò°¢–b‡7F÷&Tf—B’7F÷&U76W2³Ò°¢F6´f—G5¶–æFW…ÒçFW‡D6öçFVçBÒF6´f—BÓÓÒçVÆÂò~(	Br¢F6´f—Bòtf—G2r¢tFöW2æ÷Bf—Bs°¢7F÷&Tf—G5¶–æFW…ÒçFW‡D6öçFVçBÒ7F÷&Tf—BÓÓÒçVÆÂò~(	Br¢7F÷&Tf—Bòtf—G2fÆBr¢tFöW2æ÷Bf—BfÆBs°¢&V5¶–æFW…ÒçFW‡D6öçFVçBÒ&VÓÓÒçVÆÂò~(	Br¢G¶&VçFôf—†VBƒ—Ò–ì+&°¢Væ—D6÷7G5¶–æFW…ÒçFW‡D6öçFVçBÒ&Vâbb6÷7BÓÒçVÆÂòG¶ÖöæW’†6÷7Bò&V—Òö–ì+&¢~(	Bs°¢Ð¢6öç7B7FGW2ÒB‚u¶FF×G&’×7FGW5ÒrÂG&”6ö×&—6öâ“°¢–b‚7FGW2’&WGW&ã°¢–b‚VçFW&VB’7FGW2çFW‡D6öçFVçBÒtVçFW"F†RF6²Â†æB6ÆV&æ6RÂÆö6¶VB×7F÷&vR–çFW&–÷"ÂæBç’W†7BÖöFVÂ–÷RvçBFò6ö×&Râ&Ææ²÷F–öç27F’Væ¶æ÷vââs°¢VÇ6R–b‚F6´6ö×ÆWFRÇÂ7F÷&T6ö×ÆWFR’7FGW2çFW‡D6öçFVçBÒtf–Æ&ÆR&VæB6÷7B&R6†÷vââ6ö×ÆWFRF†Ræöç¦W&òF6²æB7F÷&vRF–ÖVç6–öç2Fò'Vâ&÷F‚f—B6†V6·2âs°¢VÇ6R7FGW2çFW‡D6öçFVçBÒG·F6µ76W7ÒöbG¶VçFW&VGÒVçFW&VB÷F–öâG¶VçFW&VBÓÓÒòrr¢w2wÒ72F†RF6²&V7FævÆS²G·7F÷&U76W7Ò72F†R6–×ÆRfÆB×7F÷&vR6†V6²â&Wf–Wr&VÂ6ÆV&æ6W2ÂÖFW&–Ç2Â7F&–Æ—G’ÂæB6&R6W&FVÇ’æ°¢Ó°¢BB‚v–çWBrÂG&”6ö×&—6öâ’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW%G&”6ö×&—6öâ’“°¢B‚u¶FF×G&’×&W6WEÒrÂG&”6ö×&—6öâ“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂG&”6ö×&—6öâ’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢&VæFW%G&”6ö×&—6öâ‚“°¢B‚u¶FF×G&’×F6²×v–GF…ÒrÂG&”6ö×&—6öâ“òæfö7W2‚“°¢Ò“°¢&VæFW%G&”6ö×&—6öâ‚“°¢Ð ¢òò‡VÖ–F—G’×7—7FVÒÖF‚6ö×&W2F†R6öç7VÖ&ÆRæB–ç7G'VÖVçB77V×F–öç0¢òòVçFW&VB'’F†R&VFW"â—BFöW2æ÷B6†ö÷6RF&vWBÂ&VF–7B6²Æ–fRÀ¢òò6Æ–'&FR6Vç6÷"Â÷"FV6–FRv†WF†W"&öGV7B—26fRà¢6öç7B‡VÖ–F—G”6ö×&—6öâÒB‚u¶FFÖ‡VÖ–F—G’Ö6ö×&—6öåÒr“°¢–b†‡VÖ–F—G”6ö×&—6öâ’°¢6öç7B&VBÒ‡6VÆV7F÷"’Óâ°¢6öç7B&rÒB‡6VÆV7F÷"Â‡VÖ–F—G”6ö×&—6öâ“òçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7B&VDBÒ†æöFW2Â–æFW‚’Óâ°¢6öç7B&rÒæöFW5¶–æFW…ÓòçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7BÖöæW’Ò‡fÇVR’ÓâfÇVRÓÓÒçVÆÂò~(	Br¢fÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ·7G–ÆS¢v7W'&Væ7’rÂ7W'&Væ7“¢uU4BwÒ“°¢6öç7B6´6÷7G2ÒBB‚u¶FFÖ‡VÖ–F—G’×6²Ö6÷7EÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7B6´6÷VçG2ÒBB‚u¶FFÖ‡VÖ–F—G’×6²Ö6÷VçEÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7B7F—fU6·2ÒBB‚u¶FFÖ‡VÖ–F—G’Ö7F—fR×6·5ÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7B–çFW'fÇ2ÒBB‚u¶FFÖ‡VÖ–F—G’Ö–çFW'fÅÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7BÖWFW$6÷VçG2ÒBB‚u¶FFÖ‡VÖ–F—G’ÖÖWFW"Ö6÷VçEÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7BÖWFW$6÷7G2ÒBB‚u¶FFÖ‡VÖ–F—G’ÖÖWFW"Ö6÷7EÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7B6W'f–6T6÷7G2ÒBB‚u¶FFÖ‡VÖ–F—G’×6W'f–6RÖ6÷7EÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7B6·5–V"ÒBB‚u¶FFÖ‡VÖ–F—G’×6·2×–V%ÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7B6¶vW5–V"ÒBB‚u¶FFÖ‡VÖ–F—G’×6¶vW2×–V%ÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7Bf—'7D6÷7G2ÒBB‚u¶FFÖ‡VÖ–F—G’Öf—'7EÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7BF÷FÄ6÷7G2ÒBB‚u¶FFÖ‡VÖ–F—G’×F÷FÅÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7BæçVÄ6÷7G2ÒBB‚u¶FFÖ‡VÖ–F—G’ÖæçVÅÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢6öç7B&VæFW$‡VÖ–F—G”6ö×&—6öâÒ‚’Óâ°¢6öç7B–V'2Ò&VB‚u¶FFÖ‡VÖ–F—G’×–V'5Òr“°¢ÆWBVçFW&VBÒ°¢ÆWB6ö×ÆWFRÒ°¢f÷"†ÆWB–æFW‚Ò²–æFW‚Â3²–æFW‚³Ò’°¢6öç7B6´6÷7BÒ&VDB‡6´6÷7G2Â–æFW‚“°¢6öç7B6´6÷VçBÒ&VDB‡6´6÷VçG2Â–æFW‚“°¢6öç7B7F—fRÒ&VDB†7F—fU6·2Â–æFW‚“°¢6öç7B–çFW'fÂÒ&VDB†–çFW'fÇ2Â–æFW‚“°¢6öç7BÖWFW'2Ò&VDB†ÖWFW$6÷VçG2Â–æFW‚’óò°¢6öç7BÖWFW$6÷7BÒ&VDB†ÖWFW$6÷7G2Â–æFW‚’óò°¢6öç7B6W'f–6RÒ&VDB‡6W'f–6T6÷7G2Â–æFW‚’óò°¢6öç7B†4÷F–öâÒ6´6÷7BÓÒçVÆÂÇÂ6´6÷VçBÓÒçVÆÂÇÂ7F—fRÓÒçVÆÂÇÂ–çFW'fÂÓÒçVÆÂÇÂ&VDB†ÖWFW$6÷VçG2Â–æFW‚’ÓÒçVÆÂÇÂ&VDB†ÖWFW$6÷7G2Â–æFW‚’ÓÒçVÆÂÇÂ&VDB‡6W'f–6T6÷7G2Â–æFW‚’ÓÒçVÆÃ°¢–b††4÷F–öâ’VçFW&VB³Ò°¢6öç7B&V7W'&–æt6ö×ÆWFRÒ6´6÷7BÓÒçVÆÂbb6´6÷VçBâbb7F—fRÓÒçVÆÂbb–çFW'fÂâ°¢6öç7BW%–V"Ò&V7W'&–æt6ö×ÆWFRò7F—fR¢S"ò–çFW'fÂ¢çVÆÃ°¢6öç7B–V%6¶vW2ÒW%–V"ÓÓÒçVÆÂòçVÆÂ¢ÖF‚æ6V–Â‡W%–V"ò6´6÷VçB“°¢6öç7Bf—'7BÒ&V7W'&–æt6ö×ÆWFRò–V%6¶vW2¢6´6÷7B²ÖWFW'2¢ÖWFW$6÷7B²6W'f–6R¢çVÆÃ°¢6öç7B†÷&—¦öå6¶vW2Ò&V7W'&–æt6ö×ÆWFRbb–V'2âòÖF‚æ6V–Â‡W%–V"¢–V'2ò6´6÷VçB’¢çVÆÃ°¢6öç7BF÷FÂÒ†÷&—¦öå6¶vW2ÓÓÒçVÆÂòçVÆÂ¢†÷&—¦öå6¶vW2¢6´6÷7B²ÖWFW'2¢ÖWFW$6÷7B²6W'f–6R¢–V'3°¢6öç7BæçVÂÒF÷FÂÓÒçVÆÂbb–V'2âòF÷FÂò–V'2¢çVÆÃ°¢6·5–V%¶–æFW…ÒçFW‡D6öçFVçBÒW%–V"ÓÓÒçVÆÂò~(	Br¢W%–V"çFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ¶Ö†–×VÔg&7F–öäF–v—G3£'Ò“°¢6¶vW5–V%¶–æFW…ÒçFW‡D6öçFVçBÒ–V%6¶vW2ÓÓÒçVÆÂò~(	Br¢–V%6¶vW2çFôÆö6ÆU7G&–ær‚“°¢f—'7D6÷7G5¶–æFW…ÒçFW‡D6öçFVçBÒÖöæW’†f—'7B“°¢F÷FÄ6÷7G5¶–æFW…ÒçFW‡D6öçFVçBÒÖöæW’‡F÷FÂ“°¢æçVÄ6÷7G5¶–æFW…ÒçFW‡D6öçFVçBÒÖöæW’†æçVÂ“°¢–b‡&V7W'&–æt6ö×ÆWFRbb–V'2â’6ö×ÆWFR³Ò°¢Ð¢6öç7B7FGW2ÒB‚u¶FFÖ‡VÖ–F—G’×7FGW5ÒrÂ‡VÖ–F—G”6ö×&—6öâ“°¢–b‚7FGW2’&WGW&ã°¢–b‚VçFW&VB’7FGW2çFW‡D6öçFVçBÒtVçFW"æöç¦W&ò†÷&—¦öâæBç’W†7BÖÖöFVÂ77V×F–öç2–÷RvçBFò6ö×&Râ&Ææ²÷F–öç27F’Væ¶æ÷vââs°¢VÇ6R–b‚‡–V'2â’’7FGW2çFW‡D6öçFVçBÒtf—'7B×–V"W7F–ÖFW2&Rf–Æ&ÆRf÷"6ö×ÆWFR÷F–öç2âVçFW"æöç¦W&òÆææ–ær†÷&—¦öâf÷"F÷FÂæBæçVÆ—¦VB6÷7Bâs°¢VÇ6R7FGW2çFW‡D6öçFVçBÒG¶6ö×ÆWFWÒ6ö×ÆWFR÷F–öâG¶6ö×ÆWFRÓÓÒòrr¢w2wÒWFFVBÆö6ÆÇ’â6ö×&R7V6–f–6F–öç2Â6Æ–'&F–öâF‚Â6öçF–æW"f—BÂ6öæF—F–öâ7VW2ÂæB6fWG’Æ–Ö—G2&Vf÷&R6÷7Bæ°¢Ó°¢BB‚v–çWBrÂ‡VÖ–F—G”6ö×&—6öâ’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW$‡VÖ–F—G”6ö×&—6öâ’“°¢B‚u¶FFÖ‡VÖ–F—G’×&W6WEÒrÂ‡VÖ–F—G”6ö×&—6öâ“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂ‡VÖ–F—G”6ö×&—6öâ’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢&VæFW$‡VÖ–F—G”6ö×&—6öâ‚“°¢B‚u¶FFÖ‡VÖ–F—G’×–V'5ÒrÂ‡VÖ–F—G”6ö×&—6öâ“òæfö7W2‚“°¢Ò“°¢&VæFW$‡VÖ–F—G”6ö×&—6öâ‚“°¢Ð ¢òòF†RvVæW&ÂvV"6ö×&—6öâ&–6W2öæÇ’F†RW†7B–çWG27WÆ–VB'’F†P¢òò&VFW"âf—BÂÖFW&–Ç2Â–ç7G'V7F–öç2Â&V6ÆÇ2ÂæB7W÷'B&VÖ–âvFW2à¢6öç7BvV$6÷7D6ö×&—6öâÒB‚u¶FFÖvV"Ö6÷7BÖ6ö×&—6öåÒr“°¢–b†vV$6÷7D6ö×&—6öâ’°¢6öç7B&VBÒ‡6VÆV7F÷"’Óâ°¢6öç7B&rÒB‡6VÆV7F÷"ÂvV$6÷7D6ö×&—6öâ“òçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7B&VDBÒ†æöFW2Â–æFW‚’Óâ°¢6öç7B&rÒæöFW5¶–æFW…ÓòçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7BÖöæW’Ò‡fÇVR’ÓâfÇVRÓÓÒçVÆÂò~(	Br¢fÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ·7G–ÆS¢v7W'&Væ7’rÂ7W'&Væ7“¢uU4BwÒ“°¢6öç7B&–6W2ÒBB‚u¶FFÖvV"×&–6UÒrÂvV$6÷7D6ö×&—6öâ“°¢6öç7B6WGWÒBB‚u¶FFÖvV"×6WGWÒrÂvV$6÷7D6ö×&—6öâ“°¢6öç7B&V7W'&–ærÒBB‚u¶FFÖvV"×&V7W'&–æuÒrÂvV$6÷7D6ö×&—6öâ“°¢6öç7Bf—'7E&W7VÇG2ÒBB‚u¶FFÖvV"Öf—'7EÒrÂvV$6÷7D6ö×&—6öâ“°¢6öç7BF÷FÅ&W7VÇG2ÒBB‚u¶FFÖvV"×F÷FÅÒrÂvV$6÷7D6ö×&—6öâ“°¢6öç7BæçVÅ&W7VÇG2ÒBB‚u¶FFÖvV"ÖæçVÅÒrÂvV$6÷7D6ö×&—6öâ“°¢6öç7BW%W6U&W7VÇG2ÒBB‚u¶FFÖvV"×W"×W6UÒrÂvV$6÷7D6ö×&—6öâ“°¢6öç7B&VæFW$vV$6÷7D6ö×&—6öâÒ‚’Óâ°¢6öç7B–V'2Ò&VB‚u¶FFÖvV"×–V'5Òr“°¢6öç7BW6W2Ò&VB‚u¶FFÖvV"×W6W5Òr“°¢ÆWBVçFW&VBÒ°¢ÆWB6ö×ÆWFRÒ°¢f÷"†ÆWB–æFW‚Ò²–æFW‚Â3²–æFW‚³Ò’°¢6öç7B&–6RÒ&VDB‡&–6W2Â–æFW‚“°¢6öç7B6WGW6÷7BÒ&VDB‡6WGWÂ–æFW‚“°¢6öç7B&V7W'&–æt6÷7BÒ&VDB‡&V7W'&–ærÂ–æFW‚“°¢–b…·&–6RÂ6WGW6÷7BÂ&V7W'&–æt6÷7EÒç6öÖR‚‡fÇVR’ÓâfÇVRÓÒçVÆÂ’’VçFW&VB³Ò°¢6öç7Bf—'7BÒ&–6RÓÒçVÆÂbb6WGW6÷7BÓÒçVÆÂbb&V7W'&–æt6÷7BÓÒçVÆÂò&–6R²6WGW6÷7B²&V7W'&–æt6÷7B¢çVÆÃ°¢6öç7BF÷FÂÒf—'7BÓÒçVÆÂbb–V'2âò&–6R²6WGW6÷7B²&V7W'&–æt6÷7B¢–V'2¢çVÆÃ°¢6öç7BæçVÆ—¦VBÒF÷FÂÓÒçVÆÂbb–V'2âòF÷FÂò–V'2¢çVÆÃ°¢6öç7BW%W6RÒF÷FÂÓÒçVÆÂbb–V'2âbbW6W2âòF÷FÂò‡–V'2¢W6W2’¢çVÆÃ°¢f—'7E&W7VÇG5¶–æFW…ÒçFW‡D6öçFVçBÒÖöæW’†f—'7B“°¢F÷FÅ&W7VÇG5¶–æFW…ÒçFW‡D6öçFVçBÒÖöæW’‡F÷FÂ“°¢æçVÅ&W7VÇG5¶–æFW…ÒçFW‡D6öçFVçBÒÖöæW’†æçVÆ—¦VB“°¢W%W6U&W7VÇG5¶–æFW…ÒçFW‡D6öçFVçBÒÖöæW’‡W%W6R“°¢–b‡F÷FÂÓÒçVÆÂ’6ö×ÆWFR³Ò°¢Ð¢6öç7B7FGW2ÒB‚u¶FFÖvV"×7FGW5ÒrÂvV$6÷7D6ö×&—6öâ“°¢–b‚7FGW2’&WGW&ã°¢–b‚VçFW&VB’7FGW2çFW‡D6öçFVçBÒtVçFW"F†RÆææ–ær†÷&—¦öâæBç’6ö×ÆWFRW†7BÖÖöFVÂ6÷7G2â&Ææ²f–VÆG27F’Væ¶æ÷vã²VçFW"öæÇ’v†Vâ&VÂ6÷7B—2¦W&òâs°¢VÇ6R–b‚‡–V'2â’’7FGW2çFW‡D6öçFVçBÒtf—'7B×–V"W7F–ÖFW2&Rf–Æ&ÆRf÷"6ö×ÆWFR÷F–öç2âVçFW"æöç¦W&ò†÷&—¦öâf÷"F÷FÂæBæçVÆ—¦VB6÷7Bâs°¢VÇ6R–b‚‡W6W2â’’7FGW2çFW‡D6öçFVçBÒG¶6ö×ÆWFWÒ÷væW'6†—W7F–ÖFRG¶6ö×ÆWFRÓÓÒòrr¢w2wÒ6ö×ÆWFRâVçFW"æöç¦W&òW‡V7FVBW6W2W"–V"öæÇ’–b6÷7BW"W6R†VÇ2F†—2FV6—6–öâæ°¢VÇ6R7FGW2çFW‡D6öçFVçBÒG¶6ö×ÆWFWÒ6ö×ÆWFR÷F–öâG¶6ö×ÆWFRÓÓÒòrr¢w2wÒWFFVBÆö6ÆÇ’âÇ’f—BÂÖFW&–Ç2Â6fWG’Â6&RÂ7W÷'BÂv'&çG’ÂæB&V6ÆÂvFW2&Vf÷&R6ö×&–ær6÷7Bæ°¢Ó°¢BB‚v–çWBrÂvV$6÷7D6ö×&—6öâ’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW$vV$6÷7D6ö×&—6öâ’“°¢B‚u¶FFÖvV"×&W6WEÒrÂvV$6÷7D6ö×&—6öâ“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂvV$6÷7D6ö×&—6öâ’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢&VæFW$vV$6÷7D6ö×&—6öâ‚“°¢B‚u¶FFÖvV"×–V'5ÒrÂvV$6÷7D6ö×&—6öâ“òæfö7W2‚“°¢Ò“°¢&VæFW$vV$6÷7D6ö×&—6öâ‚“°¢Ð ¢òò&WGW&âæBv'&çG’FFW2&RÆææ–ær6†V6·ö–çG2öæÇ’âF†Rw&—GFVà¢òòFW&×2FV6–FRF†R6öçG&öÆÆ–ærWfVçBÂ6÷VçF–ær'VÆRÂ7WFöfbæB&VÖVG’à¢6öç7B&WGW&äFVFÆ–æRÒB‚u¶FF×&WGW&âÖFVFÆ–æUÒr“°¢–b‡&WGW&äFVFÆ–æR’°¢6öç7B'6TFFRÒ‡&r’Óâ°¢–b‚õåÆG³GÒÕÆG³'ÒÕÆG³'ÒBòçFW7B‡&rÇÂrr’’&WGW&âçVÆÃ°¢6öç7B·–V"ÂÖöçF‚ÂF•ÒÒ&rç7Æ—B‚rÒr’æÖ„çVÖ&W"“°¢6öç7BfÇVRÒæWrFFR„FFRåUD2‡–V"ÂÖöçF‚ÒÂF’’“°¢&WGW&âfÇVRævWEUD4gVÆÅ–V"‚’ÓÓÒ–V"bbfÇVRævWEUD4ÖöçF‚‚’ÓÓÒÖöçF‚ÒbbfÇVRævWEUD4FFR‚’ÓÓÒF’òfÇVR¢çVÆÃ°¢Ó°¢6öç7B&VD6÷VçBÒ‡6VÆV7F÷"’Óâ°¢6öç7B&rÒB‡6VÆV7F÷"Â&WGW&äFVFÆ–æR“òçfÇVRçG&–Ò‚“°¢–b‡&rÓÓÒrr’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4–çFVvW"‡fÇVR’bbfÇVRãÒòfÇVR¢çVÆÃ°¢Ó°¢6öç7BFDF—2Ò†FFRÂF—2’ÓâæWrFFR†FFRævWEF–ÖR‚’²F—2¢ƒcC“°¢6öç7BFDÖöçF‡46Æ×VBÒ†FFRÂÖöçF‡2’Óâ°¢6öç7BF&vWDÖöçF‚ÒFFRævWEUD4ÖöçF‚‚’²ÖöçF‡3°¢6öç7BF&vWE–V"ÒFFRævWEUD4gVÆÅ–V"‚’²ÖF‚æfÆö÷"‡F&vWDÖöçF‚ò"“°¢6öç7Bæ÷&ÖÆ—¦VDÖöçF‚Ò‚‡F&vWDÖöçF‚R"’²"’R#°¢6öç7BÆ7DF’ÒæWrFFR„FFRåUD2‡F&vWE–V"Âæ÷&ÖÆ—¦VDÖöçF‚²Â’’ævWEUD4FFR‚“°¢&WGW&âæWrFFR„FFRåUD2‡F&vWE–V"Âæ÷&ÖÆ—¦VDÖöçF‚ÂÖF‚æÖ–â†FFRævWEUD4FFR‚’ÂÆ7DF’’’“°¢Ó°¢6öç7Bf÷&ÖDFFRÒ†FFR’ÓâFFRòFFRçFôÆö6ÆTFFU7G&–ær‡VæFVf–æVBÂ·–V#¢vçVÖW&–2rÂÖöçFƒ¢vÆöærrÂF“¢vçVÖW&–2rÂF–ÖU¦öæS¢uUD2wÒ’¢~(	Bs°¢6öç7B&VæFW%&WGW&äFVFÆ–æRÒ‚’Óâ°¢6öç7B7F'BÒ'6TFFR‚B‚u¶FF×&WGW&â×W&6†6UÒrÂ&WGW&äFVFÆ–æR“òçfÇVR“°¢6öç7BF—2Ò&VD6÷VçB‚u¶FF×&WGW&âÖF—5Òr“°¢6öç7BÖöçF‡2Ò&VD6÷VçB‚u¶FF×&WGW&âÖÖöçF‡5Òr“°¢B‚u¶FF×&WGW&â×7F'EÒrÂ&WGW&äFVFÆ–æR’çFW‡D6öçFVçBÒf÷&ÖDFFR‡7F'B“°¢B‚u¶FF×&WGW&âÖVæEÒrÂ&WGW&äFVFÆ–æR’çFW‡D6öçFVçBÒf÷&ÖDFFR‡7F'BbbF—2ÓÒçVÆÂòFDF—2‡7F'BÂF—2’¢çVÆÂ“°¢B‚u¶FF×v'&çG’ÖVæEÒrÂ&WGW&äFVFÆ–æR’çFW‡D6öçFVçBÒf÷&ÖDFFR‡7F'BbbÖöçF‡2ÓÒçVÆÂòFDÖöçF‡46Æ×VB‡7F'BÂÖöçF‡2’¢çVÆÂ“°¢6öç7B7FGW2ÒB‚u¶FF×&WGW&â×7FGW5ÒrÂ&WGW&äFVFÆ–æR“°¢–b‚7FGW2’&WGW&ã°¢–b‚7F'B’7FGW2çFW‡D6öçFVçBÒtVçFW"fÆ–BFFRæBöæÇ’FW&×2–÷R6âfW&–g’â&Ææ²f–VÆG27F’Væ¶æ÷vââs°¢VÇ6R–b†F—2ÓÓÒçVÆÂbbÖöçF‡2ÓÓÒçVÆÂ’7FGW2çFW‡D6öçFVçBÒu7F'BFFR&V6÷&FVBâFBfW&–f–VB&WGW&âv–æF÷r÷"v'&çG’FW&ÒFò6Æ7VÆFRâV&Ç’&Wf–Wr6†V6·ö–çBâs°¢VÇ6R7FGW2çFW‡D6öçFVçBÒuÆææ–ær6†V6·ö–çG2WFFVBÆö6ÆÇ’â6öæf—&ÒF†Rw&—GFVâFW&×2Â6÷VçF–ær'VÆRÂF–ÖR¦öæRÂW†6ÇW6–öç2æB&WV—&VBæ÷F–6S²6WBâV&Æ–W"&VÖ–æFW"âs°¢Ó°¢BB‚v–çWBrÂ&WGW&äFVFÆ–æR’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW%&WGW&äFVFÆ–æR’“°¢B‚u¶FF×&WGW&â×&W6WEÒrÂ&WGW&äFVFÆ–æR“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂ&WGW&äFVFÆ–æR’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢&VæFW%&WGW&äFVFÆ–æR‚“°¢B‚u¶FF×&WGW&â×W&6†6UÒrÂ&WGW&äFVFÆ–æR“òæfö7W2‚“°¢Ò“°¢&VæFW%&WGW&äFVFÆ–æR‚“°¢Ð ¢òòF†RÆ÷WR6ö×&—6öâ6†V6·2öæÇ’F†RFö7VÖVçFVBF–ÖVç6–öç2æB6÷7G2F†P¢òò&VFW"VçFW'2â—BFöW2æ÷BfW&–g’â÷F–6Â6Æ–Ò÷"6W'F–g’FWf–6Rà¢6öç7BÆ÷WT6ö×&—6öâÒB‚u¶FFÖÆ÷WRÖ6ö×&—6öåÒr“°¢–b†Æ÷WT6ö×&—6öâ’°¢6öç7B&VBÒ‡6VÆV7F÷"’Óâ°¢6öç7B&rÒB‡6VÆV7F÷"ÂÆ÷WT6ö×&—6öâ“òçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7B&VDBÒ†æöFW2Â–æFW‚’Óâ°¢6öç7B&rÒæöFW5¶–æFW…ÓòçfÇVRçG&–Ò‚“°¢–b‚&r’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7BÖöæW’Ò‡fÇVR’ÓâfÇVRÓÓÒçVÆÂò~(	Br¢fÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ·7G–ÆS¢v7W'&Væ7’rÂ7W'&Væ7“¢uU4BwÒ“°¢6öç7BÖ–ÆÆ–ÖWFW'2Ò†7GVÂÂ&WV—&VBÂ÷6—F—fTÆ&VÂ’Óâ°¢–b†7GVÂÓÓÒçVÆÂÇÂ&WV—&VBÓÓÒçVÆÂ’&WGW&â~(	Bs°¢6öç7BÖ&v–âÒ7GVÂÒ&WV—&VC°¢&WGW&âÖ&v–âãÒòG·÷6—F—fTÆ&VÇÒ‚²G¶Ö&v–âçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ¶Ö†–×VÔg&7F–öäF–v—G3£Ò—ÒÖÒ–¢6†÷'BG´ÖF‚æ'2†Ö&v–â’çFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ¶Ö†–×VÔg&7F–öäF–v—G3£Ò—ÒÖÖ°¢Ó°¢6öç7BFWf–6W2ÒBB‚u¶FFÖÆ÷WRÖFWf–6UÒrÂÆ÷WT6ö×&—6öâ“°¢6öç7B66W76÷&–W2ÒBB‚u¶FFÖÆ÷WRÖ66W76÷&–W5ÒrÂÆ÷WT6ö×&—6öâ“°¢6öç7BæçVÄ6÷7G2ÒBB‚u¶FFÖÆ÷WRÖæçVÂÖ6÷7EÒrÂÆ÷WT6ö×&—6öâ“°¢6öç7Bf–VÆG2ÒBB‚u¶FFÖÆ÷WRÖf÷eÒrÂÆ÷WT6ö×&—6öâ“°¢6öç7BF—7Fæ6W2ÒBB‚u¶FFÖÆ÷WR×v÷&¶–ærÖF—7Fæ6UÒrÂÆ÷WT6ö×&—6öâ“°¢6öç7Bf–VÆE&W7VÇG2ÒBB‚u¶FFÖÆ÷WRÖf÷b×&W7VÇEÒrÂÆ÷WT6ö×&—6öâ“°¢6öç7BF—7Fæ6U&W7VÇG2ÒBB‚u¶FFÖÆ÷WRÖF—7Fæ6R×&W7VÇEÒrÂÆ÷WT6ö×&—6öâ“°¢6öç7Bf—'7E&W7VÇG2ÒBB‚u¶FFÖÆ÷WRÖf—'7EÒrÂÆ÷WT6ö×&—6öâ“°¢6öç7BF÷FÅ&W7VÇG2ÒBB‚u¶FFÖÆ÷WR×F÷FÅÒrÂÆ÷WT6ö×&—6öâ“°¢6öç7BæçVÅ&W7VÇG2ÒBB‚u¶FFÖÆ÷WRÖæçVÅÒrÂÆ÷WT6ö×&—6öâ“°¢6öç7B&VæFW$Æ÷WT6ö×&—6öâÒ‚’Óâ°¢6öç7BF&vWBÒ&VB‚u¶FFÖÆ÷WR×F&vWEÒr“°¢6öç7B6ÆV&æ6RÒ&VB‚u¶FFÖÆ÷WRÖ6ÆV&æ6UÒr“°¢6öç7B–V'2Ò&VB‚u¶FFÖÆ÷WR×–V'5Òr“°¢ÆWBVçFW&VBÒ°¢ÆWBF–ÖVç6–öä6ö×ÆWFRÒ°¢ÆWB6÷7D6ö×ÆWFRÒ°¢f÷"†ÆWB–æFW‚Ò²–æFW‚Â3²–æFW‚³Ò’°¢6öç7BFWf–6RÒ&VDB†FWf–6W2Â–æFW‚“°¢6öç7B66W76÷'’Ò&VDB†66W76÷&–W2Â–æFW‚“°¢6öç7BæçVÄ6÷7BÒ&VDB†æçVÄ6÷7G2Â–æFW‚“°¢6öç7Bf–VÆBÒ&VDB†f–VÆG2Â–æFW‚“°¢6öç7BF—7Fæ6RÒ&VDB†F—7Fæ6W2Â–æFW‚“°¢–b…¶FWf–6RÂ66W76÷'’ÂæçVÄ6÷7BÂf–VÆBÂF—7Fæ6UÒç6öÖR‚‡fÇVR’ÓâfÇVRÓÒçVÆÂ’’VçFW&VB³Ò°¢6öç7Bf—'7BÒFWf–6RÓÒçVÆÂbb66W76÷'’ÓÒçVÆÂbbæçVÄ6÷7BÓÒçVÆÂòFWf–6R²66W76÷'’²æçVÄ6÷7B¢çVÆÃ°¢6öç7BF÷FÂÒFWf–6RÓÒçVÆÂbb66W76÷'’ÓÒçVÆÂbbæçVÄ6÷7BÓÒçVÆÂbb–V'2âòFWf–6R²66W76÷'’²æçVÄ6÷7B¢–V'2¢çVÆÃ°¢6öç7BæçVÆ—¦VBÒF÷FÂÓÒçVÆÂbb–V'2âòF÷FÂò–V'2¢çVÆÃ°¢f–VÆE&W7VÇG5¶–æFW…ÒçFW‡D6öçFVçBÒÖ–ÆÆ–ÖWFW'2†f–VÆBÂF&vWBÂtf—G2r“°¢F—7Fæ6U&W7VÇG5¶–æFW…ÒçFW‡D6öçFVçBÒÖ–ÆÆ–ÖWFW'2†F—7Fæ6RÂ6ÆV&æ6RÂtf—G2r“°¢f—'7E&W7VÇG5¶–æFW…ÒçFW‡D6öçFVçBÒÖöæW’†f—'7B“°¢F÷FÅ&W7VÇG5¶–æFW…ÒçFW‡D6öçFVçBÒÖöæW’‡F÷FÂ“°¢æçVÅ&W7VÇG5¶–æFW…ÒçFW‡D6öçFVçBÒÖöæW’†æçVÆ—¦VB“°¢–b†f–VÆBÓÒçVÆÂbbF—7Fæ6RÓÒçVÆÂbbF&vWBÓÒçVÆÂbb6ÆV&æ6RÓÒçVÆÂ’F–ÖVç6–öä6ö×ÆWFR³Ò°¢–b‡F÷FÂÓÒçVÆÂ’6÷7D6ö×ÆWFR³Ò°¢Ð¢6öç7B7FGW2ÒB‚u¶FFÖÆ÷WR×7FGW5ÒrÂÆ÷WT6ö×&—6öâ“°¢–b‚7FGW2’&WGW&ã°¢–b‚VçFW&VB’7FGW2çFW‡D6öçFVçBÒtVçFW"F†R¦ö"æBç’W†7BÖÖöFVÂf7G2â&Ææ²f–VÆG27F’Væ¶æ÷vã²VçFW"v†Vâ&VÂ6÷7B—2¦W&òâs°¢VÇ6R–b‡F&vWBÓÓÒçVÆÂÇÂ6ÆV&æ6RÓÓÒçVÆÂÇÂ‡–V'2â’’7FGW2çFW‡D6öçFVçBÒtVçFW&VB&÷w2&R&W6W'fVBâFBF&vWBv–GF‚ÂÖ–æ–×VÒv÷&¶–ærF—7Fæ6RÂæBæöç¦W&ò†÷&—¦öâFò6ö×ÆWFR&÷F‚f—BæB÷væW'6†—67&VVç2âs°¢VÇ6R7FGW2çFW‡D6öçFVçBÒG¶F–ÖVç6–öä6ö×ÆWFWÒF–ÖVç6–öæÂ67&VVâG¶F–ÖVç6–öä6ö×ÆWFRÓÓÒòrr¢w2wÒæBG¶6÷7D6ö×ÆWFWÒ÷væW'6†—W7F–ÖFRG¶6÷7D6ö×ÆWFRÓÓÒòrr¢w2wÒ&R6ö×ÆWFRâ&Wf–Wr÷F–72Â7F&–Æ—G’ÂÆ–v‡F–ærÂ6ögGv&RÂ6&RÂ7W÷'BÂæBWf–FVæ6RÆ–Ö—G26W&FVÇ’æ°¢Ó°¢BB‚v–çWBrÂÆ÷WT6ö×&—6öâ’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW$Æ÷WT6ö×&—6öâ’“°¢B‚u¶FFÖÆ÷WR×&W6WEÒrÂÆ÷WT6ö×&—6öâ“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂÆ÷WT6ö×&—6öâ’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢&VæFW$Æ÷WT6ö×&—6öâ‚“°¢B‚u¶FFÖÆ÷WR×F&vWEÒrÂÆ÷WT6ö×&—6öâ“òæfö7W2‚“°¢Ò“°¢&VæFW$Æ÷WT6ö×&—6öâ‚“°¢Ð ¢òò7FVÒ6VÆÂ4$rWf–FVæ6RÆ—FW&7’FööÂâ—B&V6÷&G2&W6Væ6Rö'6Væ6RöæÇ“°¢òò—BæWfW"GW&ç2F†Rf—fR–æFWVæFVçB&V6÷&G2–çFòVÆ—G’66÷&Rà¢6öç7B6&tWf–FVæ6RÒB‚u¶FFÖ6&rÖWf–FVæ6UÒr“°¢–b†6&tWf–FVæ6R’°¢6öç7BÆ–W'2ÒBB‚u¶FFÖ6&rÖÆ–W%ÒrÂ6&tWf–FVæ6R“°¢6öç7B6÷VçBÒB‚u¶FFÖ6&rÖ6÷VçEÒrÂ6&tWf–FVæ6R“°¢6öç7B&öw&W72ÒB‚u¶FFÖ6&r×&öw&W75ÒrÂ6&tWf–FVæ6R“°¢6öç7B7FGW2ÒB‚u¶FFÖ6&r×7FGW5ÒrÂ6&tWf–FVæ6R“°¢6öç7B&VæFW$6&tWf–FVæ6RÒ‚’Óâ°¢6öç7B6†V6¶VBÒÆ–W'2æf–ÇFW"‚†Æ–W"’ÓâÆ–W"æ6†V6¶VB’æÆVæwFƒ°¢–b†6÷VçB’6÷VçBçFW‡D6öçFVçBÒG¶6†V6¶VGÒöbG¶Æ–W'2æÆVæwF‡Ö°¢–b‡&öw&W72’°¢&öw&W72çfÇVRÒ6†V6¶VC°¢&öw&W72çFW‡D6öçFVçBÒG¶6†V6¶VGÒöbG¶Æ–W'2æÆVæwF‡Ö°¢Ð¢–b‚7FGW2’&WGW&ã°¢–b†6†V6¶VBÓÓÒ’7FGW2çFW‡D6öçFVçBÒtæòWf–FVæ6RÆ–W"†2&VVâÖ&¶VB&W6VçBâÖ—76–ær—2&W7VÇN(	Fæ÷BW&Ö—76–öâFòwVW72âs°¢VÇ6R–b†6†V6¶VBÓÓÒÆ–W'2æÆVæwF‚’7FGW2çFW‡D6öçFVçBÒtÆÂf—fRWf–FVæ6RÆ–W'2&RÖ&¶VB&W6VçBâ&W6öÇfRç’6öæfÆ–7B÷"7F÷6–vâ6W&FVÇ“²F†—2—2æ÷BVÆ—G’÷"6fWG’66÷&Râs°¢VÇ6R7FGW2çFW‡D6öçFVçBÒG¶6†V6¶VGÒöbG¶Æ–W'2æÆVæwF‡ÒWf–FVæ6RÆ–W'2Ö&¶VB&W6VçBâF†R&VÖ–æ–ærÆ–W'27F’Væç7vW&VBæ°¢Ó°¢Æ–W'2æf÷$V6‚‚†Æ–W"’ÓâÆ–W"æFDWfVçDÆ—7FVæW"‚v6†ævRrÂ&VæFW$6&tWf–FVæ6R’“°¢B‚u¶FFÖ6&r×&W6WEÒrÂ6&tWf–FVæ6R“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢Æ–W'2æf÷$V6‚‚†Æ–W"’Óâ²Æ–W"æ6†V6¶VBÒfÇ6S²Ò“°¢&VæFW$6&tWf–FVæ6R‚“°¢Æ–W'5³Óòæfö7W2‚“°¢Ò“°¢&VæFW$6&tWf–FVæ6R‚“°¢Ð ¢òò&Wv&G2ÖF‚7F—2æ6†÷&VBFò7VæF–ærF†R&VFW"Ç&VG’ÆææVBâ—@¢òòFöW2æ÷B÷F–Ö—¦R7VæBÂ6†ö÷6R&öGV7G2ÂfÇVRW'6öæÂFFÂ÷"fW&–g¢òòF†B&öw&Ò—2ÆvgVÂ÷"67W&FVÇ’GfW'F—6VBà¢6öç7BÆ÷–ÇG•fÇVRÒB‚u¶FFÖÆ÷–ÇG’×fÇVUÒr“°¢–b†Æ÷–ÇG•fÇVR’°¢6öç7B&VBÒ‡6VÆV7F÷"’Óâ°¢6öç7B&rÒB‡6VÆV7F÷"ÂÆ÷–ÇG•fÇVR“òçfÇVRçG&–Ò‚“°¢–b‡&rÓÓÒrr’&WGW&âçVÆÃ°¢6öç7BfÇVRÒçVÖ&W"‡&r“°¢&WGW&âçVÖ&W"æ—4f–æ—FR‡fÇVR’òÖF‚æÖ‚ƒÂfÇVR’¢çVÆÃ°¢Ó°¢6öç7BÖöæW’Ò‡fÇVR’ÓâfÇVRÓÓÒçVÆÂò~(	Br¢fÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ·7G–ÆS¢v7W'&Væ7’rÂ7W'&Væ7“¢uU4BwÒ“°¢6öç7BW&6VçBÒ‡fÇVR’ÓâfÇVRÓÓÒçVÆÂò~(	Br¢G·fÇVRçFôÆö6ÆU7G&–ær‡VæFVf–æVBÂ¶Ö†–×VÔg&7F–öäF–v—G3£'Ò—ÒV°¢6öç7B&VæFW$Æ÷–ÇG•fÇVRÒ‚’Óâ°¢6öç7B7VæBÒ&VB‚u¶FFÖÆ÷–ÇG’×7VæEÒr“°¢6öç7B&FRÒ&VB‚u¶FFÖÆ÷–ÇG’×&FUÒr“°¢6öç7B&VFV×F–öâÒ&VB‚u¶FFÖÆ÷–ÇG’×&VFVVÕÒr“°¢6öç7BfVRÒ&VB‚u¶FFÖÆ÷–ÇG’ÖfVUÒr“°¢6öç7B&VÖ—VÒÒ&VB‚u¶FFÖÆ÷–ÇG’×&VÖ—VÕÒr“°¢6öç7BfÆ–EW&6VçFvW2Ò&FRÓÒçVÆÂbb&FRÃÒbb&VFV×F–öâÓÒçVÆÂbb&VFV×F–öâÃÒ°¢6öç7B6ö×ÆWFRÒ7VæBÓÒçVÆÂbbfÆ–EW&6VçFvW2bbfVRÓÒçVÆÂbb&VÖ—VÒÓÒçVÆÃ°¢6öç7Bf6RÒ6ö×ÆWFRò7VæB¢&FRò¢çVÆÃ°¢6öç7BW6&ÆU&FRÒ6ö×ÆWFRò&FRò¢&VFV×F–öâò¢çVÆÃ°¢6öç7BW6&ÆRÒf6RÓÒçVÆÂòf6R¢&VFV×F–öâò¢çVÆÃ°¢6öç7BæWBÒW6&ÆRÓÒçVÆÂòW6&ÆRÒfVRÒ&VÖ—VÒ¢çVÆÃ°¢6öç7BVffV7F—fRÒæWBÓÒçVÆÂbb7VæBâòæWBò7VæB¢¢çVÆÃ°¢6öç7B'&V´WfVâÒW6&ÆU&FRâò†fVR²&VÖ—VÒ’òW6&ÆU&FR¢çVÆÃ°¢B‚u¶FFÖÆ÷–ÇG’Öf6UÒrÂÆ÷–ÇG•fÇVR’çFW‡D6öçFVçBÒÖöæW’†f6R“°¢B‚u¶FFÖÆ÷–ÇG’×W6&ÆUÒrÂÆ÷–ÇG•fÇVR’çFW‡D6öçFVçBÒÖöæW’‡W6&ÆR“°¢B‚u¶FFÖÆ÷–ÇG’ÖæWEÒrÂÆ÷–ÇG•fÇVR’çFW‡D6öçFVçBÒÖöæW’†æWB“°¢B‚u¶FFÖÆ÷–ÇG’ÖVffV7F—fUÒrÂÆ÷–ÇG•fÇVR’çFW‡D6öçFVçBÒW&6VçB†VffV7F—fR“°¢B‚u¶FFÖÆ÷–ÇG’Ö'&V²ÖWfVåÒrÂÆ÷–ÇG•fÇVR’çFW‡D6öçFVçBÒÖöæW’†'&V´WfVâ“°¢6öç7B7FGW2ÒB‚u¶FFÖÆ÷–ÇG’×7FGW5ÒrÂÆ÷–ÇG•fÇVR“°¢–b‚7FGW2’&WGW&ã°¢–b‡&FRÓÒçVÆÂbb&FRâÇÂ&VFV×F–öâÓÒçVÆÂbb&VFV×F–öââ’°¢7FGW2çFW‡D6öçFVçBÒu&Wv&B&FRæB&VÆ—7F–2&VFV×F–öâ×W7BV6‚7F’&WGvVVâRæBRâs°¢ÒVÇ6R–b‚6ö×ÆWFR’°¢7FGW2çFW‡D6öçFVçBÒt6ö×ÆWFRÆÂf—fRf–VÆG2g&öÒFFVBFW&×2æB6ö×F–&ÆR&–6R&6VÆ–æRâ&Ææ²f–VÆG27F’Væ¶æ÷vââs°¢ÒVÇ6R–b‚‡7VæBâ’ÇÂ‡W6&ÆU&FRâ’’°¢7FGW2çFW‡D6öçFVçBÒtæò÷6—F—fRVffV7F—fR&Wv&B&FR—2f–Æ&ÆRg&öÒF†W6R–çWG2â&—f7’Â'VÆRÂ&öGV7BÂæBW†—B6†V6·27F–ÆÂÇ’âs°¢ÒVÇ6R–b†æWBÂ’°¢7FGW2çFW‡D6öçFVçBÒtW7F–ÖFVBæWBfÇVR—2æVvF—fRgFW"fVW2æBF†RVçFW&VB&–6R&VÖ—VÒâFòæ÷B–æ7&V6R7VæF–ærFò&W—"F†R&W7VÇBâs°¢ÒVÇ6R°¢7FGW2çFW‡D6öçFVçBÒtW7F–ÖFRWFFVBÆö6ÆÇ’âfW&–g’VÆ–v–&–Æ—G’ÂW‡—'’Â6öçfW'6–öâÂ7W'&VçBÆrÂ&–6R&6—2Â&—f7’FW&×2ÂæBF†Ræò×&öw&Ò÷F–öâ&Vf÷&RFV6–F–ærâs°¢Ð¢Ó°¢BB‚v–çWBrÂÆ÷–ÇG•fÇVR’æf÷$V6‚‚†–çWB’Óâ–çWBæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW$Æ÷–ÇG•fÇVR’“°¢B‚u¶FFÖÆ÷–ÇG’×&W6WEÒrÂÆ÷–ÇG•fÇVR“òæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢BB‚v–çWBrÂÆ÷–ÇG•fÇVR’æf÷$V6‚‚†–çWB’Óâ²–çWBçfÇVRÒrs²Ò“°¢6öç7B&VFV×F–öâÒB‚u¶FFÖÆ÷–ÇG’×&VFVVÕÒrÂÆ÷–ÇG•fÇVR“°¢6öç7BfVRÒB‚u¶FFÖÆ÷–ÇG’ÖfVUÒrÂÆ÷–ÇG•fÇVR“°¢6öç7B&VÖ—VÒÒB‚u¶FFÖÆ÷–ÇG’×&VÖ—VÕÒrÂÆ÷–ÇG•fÇVR“°¢–b‡&VFV×F–öâ’&VFV×F–öâçfÇVRÒssRs°¢–b†fVR’fVRçfÇVRÒss°¢–b‡&VÖ—VÒ’&VÖ—VÒçfÇVRÒss°¢&VæFW$Æ÷–ÇG•fÇVR‚“°¢B‚u¶FFÖÆ÷–ÇG’×7VæEÒrÂÆ÷–ÇG•fÇVR“òæfö7W2‚“°¢Ò“°¢&VæFW$Æ÷–ÇG•fÇVR‚“°¢Ð ¢òòvÆ÷76'’f–ÇFW&–ær¶VW2WfW'’FVf–æ—F–öâ–âF†R…DÔÂæBöæÇ’æ'&÷w0¢òòF†Rf—6–&ÆR6WBâv—F†÷WB¦f67&—BF†R6ö×ÆWFR&VfW&Væ6R&VÖ–ç2W6&ÆRà¢6öç7BvÆ÷76'’ÒB‚u¶FFÖvÆ÷76'•Òr“°¢–b†vÆ÷76'’’°¢6öç7BvÆ÷76'”–çWBÒB‚u¶FFÖvÆ÷76'’×6V&6…ÒrÂvÆ÷76'’“°¢6öç7BFW&×2ÒBB‚u¶FFÖvÆ÷76'’×FW&ÕÒrÂvÆ÷76'’“°¢6öç7B6÷VçBÒB‚u¶FFÖvÆ÷76'’Ö6÷VçEÒrÂvÆ÷76'’“°¢6öç7BV×G’ÒB‚u¶FFÖvÆ÷76'’ÖV×G•ÒrÂvÆ÷76'’“°¢ÆWB7F—fT6FVv÷'’ÒvÆÂs°¢6öç7B&VæFW$vÆ÷76'’Ò‚’Óâ°¢6öç7Bv÷&G2Ò†vÆ÷76'”–çWCòçfÇVRÇÂrr’çG&–Ò‚’çFôÆ÷vW$66R‚’ç7Æ—B‚õÇ2²ò’æf–ÇFW"„&ööÆVâ“°¢ÆWBf—6–&ÆRÒ°¢FW&×2æf÷$V6‚‚‡FW&Ò’Óâ°¢6öç7B6FVv÷&–W2Ò‡FW&ÒæFF6WBæ6FVv÷'’ÇÂrr’ç7Æ—B‚rr“°¢6öç7B†—7F6²ÒFW&ÒæFF6WBç6V&6‚ÇÂrs°¢6öç7BÖF6†W46FVv÷'’Ò7F—fT6FVv÷'’ÓÓÒvÆÂrÇÂ6FVv÷&–W2æ–æ6ÇVFW2†7F—fT6FVv÷'’“°¢6öç7BÖF6†W5v÷&G2Òv÷&G2æWfW'’‚‡v÷&B’Óâ†—7F6²æ–æ6ÇVFW2‡v÷&B’“°¢6öç7B6†÷rÒÖF6†W46FVv÷'’bbÖF6†W5v÷&G3°¢FW&Òæ†–FFVâÒ6†÷s°¢–b‡6†÷r’f—6–&ÆR³Ò°¢Ò“°¢–b†6÷VçB’6÷VçBçFW‡D6öçFVçBÒ7G&–ær‡f—6–&ÆR“°¢–b†V×G’’V×G’æ†–FFVâÒf—6–&ÆRÓÒ°¢Ó°¢6öç7BvÆ÷76'”'WGFöç2ÒBB‚u¶FFÖvÆ÷76'’Öf–ÇFW%ÒrÂvÆ÷76'’“°¢6WD7F—fUFövvÆR†vÆ÷76'”'WGFöç2ÂvÆ÷76'”'WGFöç2æf–æB‚†'WGFöâ’Óâ'WGFöâæ6Æ74Æ—7Bæ6öçF–ç2‚v—2Ö7F—fRr’’ÇÂvÆ÷76'”'WGFöç5³Ò“°¢vÆ÷76'”'WGFöç2æf÷$V6‚‚†'WGFöâ’Óâ'WGFöâæFDWfVçDÆ—7FVæW"‚v6Æ–6²rÂ‚’Óâ°¢7F—fT6FVv÷'’Ò'WGFöâæFF6WBævÆ÷76'”f–ÇFW"ÇÂvÆÂs°¢6WD7F—fUFövvÆR†vÆ÷76'”'WGFöç2Â'WGFöâ“°¢&VæFW$vÆ÷76'’‚“°¢Ò’“°¢vÆ÷76'”–çWCòæFDWfVçDÆ—7FVæW"‚v–çWBrÂ&VæFW$vÆ÷76'’“°¢&VæFW$vÆ÷76'’‚“°¢Ð§Ò’‚“°