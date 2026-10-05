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
    let admitted = false;
    try { admitted = localStorage.getItem('bbm-age-21') === 'yes'; } catch (_) { admitted = false; }
    if (!admitted) {
      ageGate.hidden = false;
      body.classList.add('modal-open');
      window.setTimeout(() => $('[data-age-yes]', ageGate)?.focus(), 50);
    }
    $('[data-age-yes]', ageGate)?.addEventListener('click', () => {
      try { localStorage.setItem('bbm-age-21', 'yes'); } catch (_) { /* private browsing can block storage */ }
      ageGate.hidden = true;
      body.classList.remove('modal-open');
    });
    $('[data-age-no]', ageGate)?.addEventListener('click', () => {
      const card = $('.age-card', ageGate);
      if (!card) return;
      card.classList.add('age-denied');
      card.innerHTML = `
        <img src="${prefix}assets/images/logo-full.webp" alt="Big Bud Man" width="920" height="499">
        <p class="eyebrow">NOT TODAY</p>
        <h2>This site is for adults 21+.</h2>
        <p>Thanks for being straight with us. You can close this tab or visit a general public-health resource.</p>
        <p><a href="https://www.samhsa.gov/find-help" rel="noopener">Find health information at SAMHSA ↗</a></p>`;
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
      savedResults.innerHTML = '<p class="search-empty">No pages saved on this device yet. Open an article and choose “Save for later.”</p>';
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
      searchResults.innerHTML = `<p class="search-empty">No guide matched “${escapeHtml(query)}.” Try a broader word such as “label,” “flower,” or “legal.”</p>`;
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
      const text = matches.map((item) => `${item.title} — ${window.location.origin}${item.url}`).join('\n');
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
        if (resultContent) resultContent.innerHTML = `<div class="result-icon">${document.querySelector('.lane-card svg')?.outerHTML || ''}</div><h3>${route.title}</h3><p>${route.text}</p><a class="button button--primary" href="${route.url}">${route.cta} →</a>`;
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
    const citation = `Big Bud Man. “${citationButton.dataset.citationTitle}.” Reviewed ${citationButton.dataset.citationReviewed}. ${window.location.href} Accessed ${accessed}.`;
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

  // Grow-light energy arithmetic. This intentionally does not estimate circuit
  // capacity, environmental loads, crop response, or yield.
  const growPlanner = $('[data-grow-light-planner]');
  if (growPlanner) {
    const number = (selector, maximum = Number.POSITIVE_INFINITY) => {
      const value = Number($(selector, growPlanner)?.value || 0);
      return Number.isFinite(value) ? Math.min(maximum, Math.max(0, value)) : 0;
    };
    const renderGrowPlan = () => {
      const watts = number('[data-grow-watts]');
      const count = number('[data-grow-count]');
      const hours = number('[data-grow-hours]', 24);
      const days = number('[data-grow-days]', 366);
      const rate = number('[data-grow-rate]');
      const totalWatts = watts * count;
      const dailyKwh = totalWatts * hours / 1000;
      const periodKwh = dailyKwh * days;
      const cost = periodKwh * rate;
      $('[data-grow-total-watts]', growPlanner).textContent = `${totalWatts.toLocaleString(undefined, {maximumFractionDigits:1})} W`;
      $('[data-grow-daily-kwh]', growPlanner).textContent = `${dailyKwh.toFixed(2)} kWh`;
      $('[data-grow-period-kwh]', growPlanner).textContent = `${periodKwh.toFixed(2)} kWh`;
      $('[data-grow-cost]', growPlanner).textContent = cost.toLocaleString(undefined, {style:'currency', currency:'USD'});
    };
    $$('input', growPlanner).forEach((input) => input.addEventListener('input', renderGrowPlan));
    renderGrowPlan();
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

  // Product comparison arithmetic. The rows deliberately normalize only the
  // label and receipt values entered; they do not score potency or quality.
  const packageComparison = $('[data-package-comparison]');
  if (packageComparison) {
    const money = (value) => value.toLocaleString(undefined, {style:'currency', currency:'USD'});
    const numberAt = (nodes, index) => {
      const value = Number(nodes[index]?.value || 0);
      return Number.isFinite(value) ? Math.max(0, value) : 0;
    };
    const prices = $$('[data-compare-price]', packageComparison);
    const counts = $$('[data-compare-count]', packageComparison);
    const quantities = $$('[data-compare-quantity]', packageComparison);
    const milligrams = $$('[data-compare-mg]', packageComparison);
    const perUnit = $$('[data-compare-per-unit]', packageComparison);
    const perQuantity = $$('[data-compare-per-quantity]', packageComparison);
    const perHundred = $$('[data-compare-per-100]', packageComparison);
    const status = $('[data-compare-status]', packageComparison);
    const renderComparison = () => {
      for (let index = 0; index < 3; index += 1) {
        const price = numberAt(prices, index);
        const count = numberAt(counts, index);
        const quantity = numberAt(quantities, index);
        const mg = numberAt(milligrams, index);
        perUnit[index].textContent = money(count > 0 ? price / count : 0);
        perQuantity[index].textContent = money(quantity > 0 ? price / quantity : 0);
        perHundred[index].textContent = money(mg > 0 ? price * 100 / mg : 0);
      }
      if (status) status.textContent = 'Results updated locally.';
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
      const value = Number(node.value);
      return Number.isFinite(value) ? Math.max(0, value) : null;
    };
    const mg = (value) => value === null ? '—' : `${value.toLocaleString(undefined, {maximumFractionDigits:2})} mg`;
    const renderEdibleMath = () => {
      const thcServing = number('[data-edible-thc-serving]');
      const cbdServing = number('[data-edible-cbd-serving]');
      const servings = number('[data-edible-servings]');
      const units = number('[data-edible-units]');
      const labelThc = number('[data-edible-thc-total]');
      const labelCbd = number('[data-edible-cbd-total]');
      const selected = number('[data-edible-selected]');
      const thcPackage = thcServing !== null && servings !== null ? thcServing * servings : null;
      const cbdPackage = cbdServing !== null && servings !== null ? cbdServing * servings : null;
      const thcUnit = thcPackage !== null && units > 0 ? thcPackage / units : null;
      const cbdUnit = cbdPackage !== null && units > 0 ? cbdPackage / units : null;
      $('[data-edible-thc-unit]', edibleMath).textContent = mg(thcUnit);
      $('[data-edible-cbd-unit]', edibleMath).textContent = mg(cbdUnit);
      $('[data-edible-thc-package]', edibleMath).textContent = mg(thcPackage);
      $('[data-edible-cbd-package]', edibleMath).textContent = mg(cbdPackage);
      $('[data-edible-thc-selected]', edibleMath).textContent = mg(thcUnit !== null && selected !== null ? thcUnit * selected : null);
      $('[data-edible-cbd-selected]', edibleMath).textContent = mg(cbdUnit !== null && selected !== null ? cbdUnit * selected : null);
      const notes = [];
      if (labelThc !== null && thcPackage !== null) notes.push(`THC printed total differs from calculated total by ${mg(Math.abs(labelThc - thcPackage))}.`);
      if (labelCbd !== null && cbdPackage !== null) notes.push(`CBD printed total differs from calculated total by ${mg(Math.abs(labelCbd - cbdPackage))}.`);
      const status = $('[data-edible-status]', edibleMath);
      if (status) status.textContent = notes.length ? notes.join(' ') + ' Resolve any unexpected difference with the exact package and official source.' : 'Results updated locally. A matching calculation is not a dose, quality score, or accuracy certification.';
    };
    $$('input', edibleMath).forEach((input) => input.addEventListener('input', renderEdibleMath));
    $('[data-edible-reset]', edibleMath)?.addEventListener('click', () => {
      $$('input', edibleMath).forEach((input) => { input.value = ''; });
      renderEdibleMath();
      $('[data-edible-thc-serving]', edibleMath)?.focus();
    });
    renderEdibleMath();
  }

  // Dry-herb device ownership arithmetic compares documented costs only. It
  // does not rank exposure, performance, durability, or personal value.
  const vaporizerCost = $('[data-vaporizer-cost]');
  if (vaporizerCost) {
    const number = (selector) => {
      const value = Number($(selector, vaporizerCost)?.value || 0);
      return Number.isFinite(value) ? Math.max(0, value) : 0;
    };
    const money = (value) => value.toLocaleString(undefined, {style:'currency', currency:'USD'});
    const renderVaporizerCost = () => {
      const device = number('[data-vape-device]');
      const accessories = number('[data-vape-accessories]');
      const recurring = number('[data-vape-parts]') + number('[data-vape-cleaning]');
      const years = number('[data-vape-years]');
      const exit = number('[data-vape-exit]');
      const first = device + accessories + recurring;
      const total = device + accessories + recurring * years + exit;
      $('[data-vape-first]', vaporizerCost).textContent = money(first);
      $('[data-vape-total]', vaporizerCost).textContent = years > 0 ? money(total) : '—';
      $('[data-vape-annual]', vaporizerCost).textContent = years > 0 ? money(total / years) : '—';
      $('[data-vape-recurring]', vaporizerCost).textContent = years > 0 && total > 0 ? `${(recurring * years / total * 100).toFixed(1)}%` : '—';
      const status = $('[data-vape-status]', vaporizerCost);
      if (status) status.textContent = years > 0 ? 'Results updated locally. Verify every input for the exact model and seller.' : 'Enter a nonzero service horizon to calculate total and annualized cost.';
    };
    $$('input', vaporizerCost).forEach((input) => input.addEventListener('input', renderVaporizerCost));
    $('[data-vape-reset]', vaporizerCost)?.addEventListener('click', () => {
      $$('input', vaporizerCost).forEach((input) => { input.value = ''; });
      renderVaporizerCost();
      $('[data-vape-device]', vaporizerCost)?.focus();
    });
    renderVaporizerCost();
  }

  // Grinder ownership arithmetic keeps purchase cost and maintenance burden
  // visible without converting either into a product score or durability claim.
  const grinderCost = $('[data-grinder-cost]');
  if (grinderCost) {
    const number = (selector) => {
      const value = Number($(selector, grinderCost)?.value || 0);
      return Number.isFinite(value) ? Math.max(0, value) : 0;
    };
    const money = (value) => value.toLocaleString(undefined, {style:'currency', currency:'USD'});
    const renderGrinderCost = () => {
      const price = number('[data-grinder-price]');
      const accessories = number('[data-grinder-accessories]');
      const recurring = number('[data-grinder-parts]') + number('[data-grinder-cleaning]');
      const years = number('[data-grinder-years]');
      const minutes = number('[data-grinder-minutes]');
      const frequency = number('[data-grinder-frequency]');
      const first = price + accessories + recurring;
      const total = price + accessories + recurring * years;
      const hours = minutes * frequency * 12 / 60;
      $('[data-grinder-first]', grinderCost).textContent = money(first);
      $('[data-grinder-total]', grinderCost).textContent = years > 0 ? money(total) : '—';
      $('[data-grinder-annual]', grinderCost).textContent = years > 0 ? money(total / years) : '—';
      $('[data-grinder-hours]', grinderCost).textContent = `${hours.toLocaleString(undefined, {maximumFractionDigits:2})} hours`;
      const status = $('[data-grinder-status]', grinderCost);
      if (status) status.textContent = years > 0 ? 'Results updated locally. Verify each input for the exact grinder and seller.' : 'Enter a nonzero service horizon to calculate total and annualized cost.';
    };
    $$('input', grinderCost).forEach((input) => input.addEventListener('input', renderGrinderCost));
    $('[data-grinder-reset]', grinderCost)?.addEventListener('click', () => {
      $$('input', grinderCost).forEach((input) => { input.value = ''; });
      renderGrinderCost();
      $('[data-grinder-price]', grinderCost)?.focus();
    });
    renderGrinderCost();
  }

  // Air-cleaner arithmetic compares room sizing, documented smoke CADR, and
  // ownership inputs. It does not estimate exposure, health protection, odor
  // removal, or permission to generate smoke indoors.
  const airCleaner = $('[data-air-cleaner-planner]');
  if (airCleaner) {
    const number = (selector) => {
      const value = Number($(selector, airCleaner)?.value || 0);
      return Number.isFinite(value) ? Math.max(0, value) : 0;
    };
    const money = (value) => value.toLocaleString(undefined, {style:'currency', currency:'USD'});
    const decimal = (value, places = 1) => value.toLocaleString(undefined, {maximumFractionDigits:places});
    const renderAirCleaner = () => {
      const length = number('[data-air-length]');
      const width = number('[data-air-width]');
      const height = number('[data-air-height]');
      const cadr = number('[data-air-cadr]');
      const price = number('[data-air-price]');
      const filterCount = number('[data-air-filter-count]');
      const filterCost = number('[data-air-filter-cost]');
      const watts = number('[data-air-watts]');
      const hours = Math.min(24, number('[data-air-hours]'));
      const rate = number('[data-air-rate]');
      const years = number('[data-air-years]');
      const area = length * width;
      const volume = area * height;
      const needed = area > 0 && height > 0 ? area * (2 / 3) * (height / 8) : 0;
      const ach = volume > 0 ? cadr * 60 / volume : 0;
      const yearlyFilters = filterCount * filterCost;
      const yearlyElectricity = watts / 1000 * hours * 365 * rate;
      const recurring = yearlyFilters + yearlyElectricity;
      const first = price + recurring;
      const total = price + recurring * years;
      $('[data-air-area]', airCleaner).textContent = area > 0 ? `${decimal(area)} sq ft` : '—';
      $('[data-air-volume]', airCleaner).textContent = volume > 0 ? `${decimal(volume)} cu ft` : '—';
      $('[data-air-needed]', airCleaner).textContent = needed > 0 ? `${decimal(needed)} cfm` : '—';
      $('[data-air-ach]', airCleaner).textContent = volume > 0 && cadr > 0 ? `${decimal(ach, 2)} ACH` : '—';
      $('[data-air-first]', airCleaner).textContent = money(first);
      $('[data-air-total]', airCleaner).textContent = years > 0 ? money(total) : '—';
      $('[data-air-annual]', airCleaner).textContent = years > 0 ? money(total / years) : '—';
      const status = $('[data-air-status]', airCleaner);
      if (status) {
        if (!area || !height) status.textContent = 'Enter nonzero room dimensions to calculate area, volume, and a smoke-CADR starting point.';
        else if (!cadr) status.textContent = 'Room sizing is available. Enter the exact model’s smoke CADR to estimate delivered air changes.';
        else if (!years) status.textContent = 'Sizing is available. Enter a nonzero planning horizon for total and annualized cost.';
        else status.textContent = cadr >= needed ? 'Math updated locally. The entered smoke CADR meets the room-volume-adjusted starting point; verify the rating at a speed you will run.' : 'Math updated locally. The entered smoke CADR is below the room-volume-adjusted starting point; compare another speed, unit, or configuration.';
      }
    };
    $$('input', airCleaner).forEach((input) => input.addEventListener('input', renderAirCleaner));
    $('[data-air-reset]', airCleaner)?.addEventListener('click', () => {
      $$('input', airCleaner).forEach((input) => { input.value = ''; });
      renderAirCleaner();
      $('[data-air-length]', airCleaner)?.focus();
    });
    renderAirCleaner();
  }

  // Product-neutral cleaning-kit arithmetic. It prices the routine but does
  // not decide material compatibility, cleanliness, repair, or safety.
  const cleaningCost = $('[data-cleaning-cost]');
  if (cleaningCost) {
    const number = (selector) => {
      const value = Number($(selector, cleaningCost)?.value || 0);
      return Number.isFinite(value) ? Math.max(0, value) : 0;
    };
    const money = (value) => value.toLocaleString(undefined, {style:'currency', currency:'USD'});
    const decimal = (value) => value.toLocaleString(undefined, {maximumFractionDigits:2});
    const renderCleaningCost = () => {
      const kit = number('[data-cleaning-kit]');
      const tools = number('[data-cleaning-tools]');
      const bottle = number('[data-cleaning-bottle]');
      const yieldCount = number('[data-cleaning-yield]');
      const frequency = number('[data-cleaning-frequency]');
      const parts = number('[data-cleaning-parts]');
      const minutes = number('[data-cleaning-minutes]');
      const years = number('[data-cleaning-years]');
      const cycle = yieldCount > 0 ? bottle / yieldCount : 0;
      const count = frequency * 12;
      const recurring = cycle * count + parts;
      const first = kit + tools + recurring;
      const total = kit + tools + recurring * years;
      const hours = minutes * count / 60;
      $('[data-cleaning-cycle]', cleaningCost).textContent = yieldCount > 0 ? money(cycle) : '—';
      $('[data-cleaning-count]', cleaningCost).textContent = decimal(count);
      $('[data-cleaning-first]', cleaningCost).textContent = money(first);
      $('[data-cleaning-total]', cleaningCost).textContent = years > 0 ? money(total) : '—';
      $('[data-cleaning-annual]', cleaningCost).textContent = years > 0 ? money(total / years) : '—';
      $('[data-cleaning-hours]', cleaningCost).textContent = `${decimal(hours)} hours`;
      const status = $('[data-cleaning-status]', cleaningCost);
      if (status) {
        if (!yieldCount && bottle > 0) status.textContent = 'Enter a nonzero estimated number of cleanings per container to calculate cleaner cost per cycle.';
        else if (!years) status.textContent = 'Enter a nonzero planning horizon to calculate total and annualized cost.';
        else status.textContent = 'Math updated locally. Verify compatibility, replacement intervals, and every input for the exact tool and supplies.';
      }
    };
    $$('input', cleaningCost).forEach((input) => input.addEventListener('input', renderCleaningCost));
    $('[data-cleaning-reset]', cleaningCost)?.addEventListener('click', () => {
      $$('input', cleaningCost).forEach((input) => { input.value = ''; });
      renderCleaningCost();
      $('[data-cleaning-kit]', cleaningCost)?.focus();
    });
    renderCleaningCost();
  }

  // Glossary filtering keeps every definition in the HTML and only narrows
  // the visible set. Without JavaScript the complete reference remains usable.
  const glossary = $('[data-glossary]');
  if (glossary) {
    const glossaryInput = $('[data-glossary-search]', glossary);
    const terms = $$('[data-glossary-term]', glossary);
    const count = $('[data-glossary-count]', glossary);
    const empty = $('[data-glossary-empty]', glossary);
    let activeCategory = 'all';
    const renderGlossary = () => {
      const words = (glossaryInput?.value || '').trim().toLowerCase().split(/\s+/).filter(Boolean);
      let visible = 0;
      terms.forEach((term) => {
        const categories = (term.dataset.category || '').split(' ');
        const haystack = term.dataset.search || '';
        const matchesCategory = activeCategory === 'all' || categories.includes(activeCategory);
        const matchesWords = words.every((word) => haystack.includes(word));
        const show = matchesCategory && matchesWords;
        term.hidden = !show;
        if (show) visible += 1;
      });
      if (count) count.textContent = String(visible);
      if (empty) empty.hidden = visible !== 0;
    };
    const glossaryButtons = $$('[data-glossary-filter]', glossary);
    setActiveToggle(glossaryButtons, glossaryButtons.find((button) => button.classList.contains('is-active')) || glossaryButtons[0]);
    glossaryButtons.forEach((button) => button.addEventListener('click', () => {
      activeCategory = button.dataset.glossaryFilter || 'all';
      setActiveToggle(glossaryButtons, button);
      renderGlossary();
    }));
    glossaryInput?.addEventListener('input', renderGlossary);
    renderGlossary();
  }
})();
