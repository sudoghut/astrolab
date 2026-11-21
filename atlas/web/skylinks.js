// "On the sky" box for a study page (T-053): lists the study's sky targets from the Atlas data, each
// linking to the Atlas sky view centred on it (?view=sky&focus=<name>&study=<id>), with its note.
// Usage in studies/<id>/web/index.html: <section id="skylinks"></section> and
// <script src="../../../atlas/web/skylinks.js"></script> (after i18n.js).
(function () {
  const ATLAS = '../../../atlas/web/';
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const api = window.i18n || { L: en => en, onLangChange() {} };
  const L = (en, zh) => api.L(en, zh);   // zh null: English in both languages
  const bare = n => String(n || '').replace(/\s*\(CCHP host\)\s*$/i, '');
  let study = null;

  function draw() {
    const box = document.getElementById('skylinks');
    if (!box || !study) return;
    const sky = (study.footprint && study.footprint.sky) || {};
    const targets = (sky.targets || []).filter(t => t && Number.isFinite(t.l) && Number.isFinite(t.b));
    const modes = sky.modes || [];
    const href = t => `${ATLAS}?view=sky&focus=${encodeURIComponent(bare(t.name))}&study=${encodeURIComponent(study.id)}`;
    let body = '';
    if (targets.length) {
      // with many targets, the note most of them share is shown once and only differing notes per item
      const tally = new Map();
      for (const t of targets) if (t.note) tally.set(t.note, (tally.get(t.note) || 0) + 1);
      let top = null; for (const [n, c] of tally) if (!top || c > tally.get(top)) top = n;
      const shared = targets.length > 5 && top && tally.get(top) * 2 >= targets.length ? targets.find(t => t.note === top) : null;
      const items = targets.map(t => `<li><a href="${esc(href(t))}">${esc(t.name)}</a>` +
        (t.note && !(shared && t.note === shared.note) ? ` — ${L(esc(t.note), t.note_zh ? esc(t.note_zh) : null)}` : '') + '</li>').join('');
      const common = shared ? `<p>${L(esc(shared.note), shared.note_zh ? esc(shared.note_zh) : null)}</p>` : '';
      body = common + `<ul class="skylinks-list">${items}</ul>`;
    }
    const where = [];
    if (modes.includes('all-sky')) where.push(L('all-sky', '全天'));
    if (modes.includes('survey') && sky.survey) where.push(L('survey', '巡天') + ': ' + esc(sky.survey.name));
    const head = `<h2>${L('On the sky', '天图上的位置')}</h2><p class="muted">${L(
      `Footprint: ${where.join('; ') || (targets.length ? 'targets' : 'none')}. ` + (targets.length ? 'Each name opens the Atlas sky view centred on it.' : ''),
      `足迹：${where.join('；') || (targets.length ? '目标天体' : '无')}。` + (targets.length ? '点名字即可在 Atlas 天图中定位到它。' : ''))}
      <a href="${ATLAS}?view=sky">${L('Open the sky view', '打开天图')}</a></p>`;
    box.innerHTML = head + body;
    box.hidden = false;
  }

  function start() {
    const m = location.pathname.match(/studies\/([^/]+)\/web\/?/);
    const box = document.getElementById('skylinks');
    if (!m || !box) return;
    fetch(ATLAS + 'data/atlas.json').then(r => r.json()).then(d => {
      study = (d.studies || []).find(s => s.id === decodeURIComponent(m[1])) || null;
      if (!study) { box.hidden = true; return; }
      draw();
    }).catch(() => { box.hidden = true; });
    api.onLangChange(draw);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
