/* Shared English / Chinese switch for every astrolab page (AGENTS.md, bilingual rule).
 *
 * Load synchronously in <head>:  <script src=".../atlas/web/i18n.js"></script>
 * Self-contained: injects its own hide rules and toggle button, no base.css needed.
 *
 *   Static text:      <span class="en">Hello</span><span class="zh">你好</span>
 *   Generated HTML:   i18n.L('Hello', '你好')      -> both spans, CSS shows one
 *   Plain text:       i18n.t('Hello', '你好')      -> string in the current language
 *                     (textContent, attributes, <option>, chart titles and hover text)
 *   Re-render hook:   i18n.onLangChange(lang => { ... })
 *   Page title (zh):  <html data-title-zh="...">   (English title = <title>)
 *
 * Language: ?lang=en|zh, else localStorage, else English (default).
 */
(function () {
  'use strict';
  var KEY = 'astrolab-lang', LANGS = ['en', 'zh'];
  var root = document.documentElement;
  var listeners = [];

  function readUrl() {
    try { return new URLSearchParams(location.search).get('lang'); } catch (e) { return null; }
  }
  function readStore() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function writeStore(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* private mode etc. */ }
  }
  var u = readUrl(), s = readStore();
  var lang = LANGS.indexOf(u) >= 0 ? u : LANGS.indexOf(s) >= 0 ? s : 'en';
  if (LANGS.indexOf(u) >= 0) writeStore(u);

  var style = document.createElement('style');
  style.textContent =
    'html[data-lang="en"] .zh, html[data-lang="zh"] .en { display: none !important; }' +
    '.i18n-toggle { position: fixed; top: 10px; right: 12px; z-index: 1000; font: 600 13px system-ui, sans-serif;' +
    ' padding: 4px 10px; border-radius: 999px; cursor: pointer; border: 1px solid currentColor;' +
    ' background: var(--surface, #fff); color: var(--accent, #2f5d8a); }' +
    '.i18n-toggle:hover { filter: brightness(1.1); }' +
    'html[data-lang="zh"] body { font-family: system-ui, -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif; }';
  (document.head || root).appendChild(style);

  var titleEn = null;
  var button = null;

  function apply() {
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang === 'zh' ? 'zh-CN' : 'en');
    if (titleEn === null && document.title) titleEn = document.title;
    var tz = root.getAttribute('data-title-zh');
    if (titleEn !== null) document.title = lang === 'zh' && tz ? tz : titleEn;
    if (button) {
      button.textContent = lang === 'zh' ? 'EN' : '中文';
      button.setAttribute('aria-label', lang === 'zh' ? 'Switch to English' : '切换到中文');
      button.title = button.getAttribute('aria-label');
    }
  }

  function syncUrl() {
    try {
      var url = new URL(location.href);
      if (url.searchParams.has('lang') || lang !== 'en') {
        url.searchParams.set('lang', lang);
        history.replaceState(history.state, '', url.toString());
      }
    } catch (e) { /* file:// or old browser: ignore */ }
  }

  function setLang(v) {
    if (LANGS.indexOf(v) < 0 || v === lang) return;
    lang = v;
    writeStore(v);
    syncUrl();
    apply();
    listeners.slice().forEach(function (fn) {
      try { fn(lang); } catch (e) { console.error('i18n listener failed', e); }
    });
  }

  // Carry the language across internal relative links, so it survives even without storage.
  document.addEventListener('click', function (ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a || a.target === '_blank') return;
    var href = a.getAttribute('href');
    if (!href || /^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(href)) return;  // external, mailto, anchors
    try {
      var url = new URL(a.href);
      if (url.origin !== location.origin) return;
      url.searchParams.set('lang', lang);
      a.href = url.toString();
    } catch (e) { /* ignore */ }
  }, true);

  function mount() {
    if (button || !document.body) return;
    button = document.createElement('button');
    button.type = 'button';
    button.className = 'i18n-toggle';
    button.addEventListener('click', function () { setLang(lang === 'zh' ? 'en' : 'zh'); });
    document.body.appendChild(button);
    apply();
  }

  apply();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();

  window.i18n = {
    lang: function () { return lang; },
    setLang: setLang,
    t: function (en, zh) { return lang === 'zh' && zh != null && zh !== '' ? zh : en; },
    L: function (en, zh) {
      if (zh == null || zh === '') return String(en);
      return '<span class="en">' + en + '</span><span class="zh">' + zh + '</span>';
    },
    onLangChange: function (fn) { listeners.push(fn); },
  };
})();
