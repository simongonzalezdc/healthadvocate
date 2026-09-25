/* HealthAdvocate i18n frame — local-first, zero dependencies.
 *
 * Adding a language is ONE file: create static/i18n/<lang>.js with
 *   HA.i18n.register('<lang>', { 'key': 'translated string', ... });
 * plus one <script> tag next to the other catalogs. The header switcher
 * picks registered languages up automatically and cycles through them.
 *
 * Three static bindings (declare the key, get the translation):
 *   data-i18n="<key>"             → textContent
 *   data-i18n-placeholder="<key>" → placeholder
 *   data-i18n-aria="<key>"        → aria-label
 * JS-built markup calls HA.t('key', { var: value }) with {var} slots.
 * A missing key falls back to English, then to the key itself — a
 * partial catalog never renders blanks.
 */
(() => {
  const catalogs = {};
  const order = [];
  let lang = null;

  function register(code, cat) {
    catalogs[code] = cat || {};
    if (!order.includes(code)) order.push(code);
  }

  function current() {
    if (!lang) {
      const saved = localStorage.getItem('ha-lang');
      lang = saved && catalogs[saved] ? saved : (catalogs.en ? 'en' : order[0]);
    }
    return lang;
  }

  function t(key, vars) {
    let s = (catalogs[current()] || {})[key];
    if (s === undefined) s = (catalogs.en || {})[key];
    if (s === undefined) s = key;
    if (vars) for (const [k, v] of Object.entries(vars)) s = s.split(`{${k}}`).join(String(v));
    return s;
  }

  /* Re-translate every statically bound node in an optional subtree */
  function apply(root) {
    const scope = root || document;
    document.documentElement.lang = current();
    scope.querySelectorAll('[data-i18n]').forEach((el) => { el.textContent = t(el.dataset.i18n); });
    scope.querySelectorAll('[data-i18n-placeholder]').forEach((el) => { el.placeholder = t(el.dataset.i18nPlaceholder); });
    scope.querySelectorAll('[data-i18n-aria]').forEach((el) => { el.setAttribute('aria-label', t(el.dataset.i18nAria)); });
    document.dispatchEvent(new CustomEvent('ha:lang', { detail: { lang: current() } }));
  }

  function nextLang() {
    if (order.length < 2) return current();
    return order[(order.indexOf(current()) + 1) % order.length];
  }

  function setLang(next) {
    if (!catalogs[next]) return;
    lang = next;
    localStorage.setItem('ha-lang', next);
    apply();
    const btn = document.getElementById('btn-lang');
    if (btn) {
      btn.textContent = nextLang().toUpperCase();
      btn.setAttribute('aria-label', 'Switch language to ' + nextLang());
    }
  }

  function init() {
    const btn = document.getElementById('btn-lang');
    if (btn) {
      btn.textContent = order.length > 1 ? nextLang().toUpperCase() : '';
      btn.setAttribute('aria-label', 'Switch language to ' + nextLang());
      btn.addEventListener('click', () => setLang(nextLang()));
    }
    apply();
  }

  HA.i18n = { register, t, apply, setLang, init, langs: () => order.slice(), get lang() { return current(); } };
})();
