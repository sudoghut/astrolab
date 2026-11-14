/* Shared English / Chinese switch for every astrolab page (AGENTS.md, bilingual rule).
 *
 * Load synchronously in <head>, AFTER <title>:  <script src=".../atlas/web/i18n.js"></script>
 * Self-contained: injects its own hide rules and toggle button, no base.css needed.
 * L() does not escape: pass already-escaped HTML (esc() any text that comes from data files).
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
  function norm(v) { v = (v || '').toLowerCase(); return v.indexOf('zh') === 0 ? 'zh' : v === 'en' ? 'en' : null; }
  function isBackForward() {
    try { var n = performance.getEntriesByType('navigation')[0]; return !!n && n.type === 'back_forward'; }
    catch (e) { return false; }
  }
  var u = norm(readUrl()), s = norm(readStore());
  // A URL from history (Back/Forward) may be stale; the stored choice is the newer one.
  if (u && s && u !== s && isBackForward()) u = null;
  var lang = u || s || 'en';
  if (u) writeStore(u);
  syncUrl();  // drop a stale (back/forward) or non-canonical ?lang= so a refresh keeps `lang`

  var style = document.createElement('style');
  style.textContent =
    'html[data-lang="en"] .zh, html[data-lang="zh"] .en { display: none !important; }' +
    '.i18n-toggle { position: absolute; top: 10px; right: 12px; z-index: 1000; font: 600 13px system-ui, sans-serif;' +
    ' padding: 4px 10px; border-radius: 999px; cursor: pointer; border: 1px solid currentColor;' +
    ' background: var(--surface, #fff); color: var(--accent, #2f5d8a); }' +
    '.i18n-toggle:hover { filter: brightness(1.1); }' +
    '@media print { .i18n-toggle { display: none; } }' +
    'html[data-lang="zh"] body { font-family: var(--sans, system-ui, sans-serif), "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif; }';
  (document.head || root).appendChild(style);

  var titleEn = null;  // the page's own English <title>, captured once
  var button = null;

  function captureTitle(final) {
    if (titleEn !== null) return;
    var el = document.querySelector('title');
    if (el) titleEn = el.textContent;
    else if (final) titleEn = '';  // page has no <title>
  }

  function apply() {
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang === 'zh' ? 'zh-CN' : 'en');
    // Touch document.title only after the original is captured: setting it earlier would
    // create a <title> element ahead of the page's own one.
    if (titleEn !== null) {
      var tz = root.getAttribute('data-title-zh');
      document.title = lang === 'zh' && tz ? tz : titleEn;
    }
    if (button) {
      // The button speaks the language it switches to.
      button.textContent = lang === 'zh' ? 'EN' : '中文';
      button.lang = lang === 'zh' ? 'en' : 'zh-CN';
      button.title = lang === 'zh' ? 'EN: switch to English' : '中文：切换到中文';
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
  function carry(ev) {
    var a = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href || /^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(href)) return;  // external, mailto, anchors
    try {
      var url = new URL(a.href);
      if (url.origin !== location.origin) return;
      url.searchParams.set('lang', lang);
      a.href = url.toString();
    } catch (e) { /* ignore */ }
  }
  document.addEventListener('click', carry, true);
  document.addEventListener('auxclick', carry, true);   // middle-click / new tab
  document.addEventListener('contextmenu', carry, true); // "open in new tab" from the menu

  // Back/forward cache restores the page without rerunning this script; another tab may
  // also have switched language. Follow the stored choice in both cases.
  window.addEventListener('pageshow', function (ev) { if (ev.persisted) setLang(norm(readStore()) || lang); });
  window.addEventListener('storage', function (ev) { if (ev.key === KEY) setLang(norm(ev.newValue) || lang); });

  function mount() {
    if (button || !document.body) return;
    button = document.createElement('button');
    button.type = 'button';
    button.className = 'i18n-toggle';
    button.addEventListener('click', function () { setLang(lang === 'zh' ? 'en' : 'zh'); });
    document.body.insertBefore(button, document.body.firstChild);  // first tab stop
    captureTitle(true);
    apply();
  }

  captureTitle(false);
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
