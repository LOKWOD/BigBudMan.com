(() => {
  'use strict';

  const body = document.body;
  const prefix = body.dataset.prefix || '';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

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
        <img src="${prefix}assets/images/logo-mark.svg" alt="" width="76" height="76">
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

  const renderSearch = (items, query) => {
    if (!searchResults) return;
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      searchResults.innerHTML = '<p class="search-empty">Start typing to search the complete Big Bud Man library.</p>';
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
      flower: {title:'Use the flower quality guide', text:'Freshness, cure, source, and manageable potency matter more than chasing the biggest percentage.', url:'guides/flower/', cta:'Open flower guide'},
      vape: {title:'Check the vape source and hardware', text:'Concentrated oil and compact hardware reward deliberate pacing and licensed sourcing.', url:'guides/vapes/', cta:'Open vape guide'},
      label: {title:'Learn the label in ten minutes', text:'Separate package total from serving amount, then check traceability, ingredients, and batch information.', url:'guides/read-a-label/', cta:'Open label decoder'},
      legal: {title:'Check the law where you are', text:'Search all 50 states for possession, home grow, medical access, retail status, and the official source.', url:'legal/', cta:'Open 50-state library'},
      gear: {title:'Build a safer storage setup', text:'Use original packaging, an odor-resistant inner layer, and a locked outer location.', url:'gear/smell-proof-storage/', cta:'Open storage gear guide'},
      basics: {title:'Build the Cannabis 101 foundation', text:'Understand THC, CBD, formats, timing, potency, and why a strain name never tells the whole story.', url:'guides/cannabis-101/', cta:'Open Cannabis 101'}
    };
    const chooseRoute = () => {
      if (answers.priority === 'legal') return routes.legal;
      if (answers.priority === 'gear') return routes.gear;
      if (answers.priority === 'label') return routes.label;
      if (answers.format === 'edible') return routes.edible;
      if (answers.format === 'vape') return routes.vape;
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
    $$('[data-filter]', filterBar).forEach((button) => button.addEventListener('click', () => {
      activeFilter = button.dataset.filter || 'all';
      $$('[data-filter]', filterBar).forEach((item) => item.classList.toggle('is-active', item === button));
      renderStrains();
    }));
    $$('[data-cannabinoid-filter]', filterBar).forEach((button) => button.addEventListener('click', () => {
      activeCannabinoid = button.dataset.cannabinoidFilter || 'all';
      $$('[data-cannabinoid-filter]', filterBar).forEach((item) => item.classList.toggle('is-active', item === button));
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
    $$('[data-state-filter]', stateLibrary).forEach((button) => button.addEventListener('click', () => {
      activeStatus = button.dataset.stateFilter || 'all';
      $$('[data-state-filter]', stateLibrary).forEach((item) => item.classList.toggle('is-active', item === button));
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
      const links = $$('a', toc);
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
})();
