/* HealthAdvocate — Frontend Application */

const HA = {
  /* ── API helpers ── */

  async api(endpoint, data) {
    let response;
    try {
      response = await fetch(`/api/${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
    } catch (e) {
      throw new Error('We could not reach the server. Please check your internet connection and try again.');
    }
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(err.detail || response.statusText);
    }
    return response.json();
  },

  async apiGet(endpoint) {
    let response;
    try {
      response = await fetch(`/api/${endpoint}`);
    } catch (e) {
      throw new Error('We could not reach the server. Please check your internet connection and try again.');
    }
    if (!response.ok) throw new Error(response.statusText);
    return response.json();
  },

  _VALID_ENTITY_CLASSES: new Set(['disease', 'drug', 'anatomy', 'pii', 'procedure', 'symptom']),

  safeEntityClass(cat) {
    const c = (cat || '').toLowerCase();
    return this._VALID_ENTITY_CLASSES.has(c) ? c : 'entity';
  },

  /* ── Honesty rendering (audit E1/E2/D5/D3/B3, 2026-09-24) ── */

  /* E2: the only human contacts HealthAdvocate will ever name — two
     widely published US crisis lines plus links to find real help.
     Nothing scraped, nothing invented. Rendered with every NEEDS_HUMAN
     banner and on the Help view (index.html carries the same list). */
  HUMAN_RESOURCES_HTML: `
      <div class="human-resources">
        <p><strong>Talk to a real person:</strong></p>
        <ul>
          <li>988 Suicide &amp; Crisis Lifeline — call or text <strong>988</strong> (US)</li>
          <li>SAMHSA National Helpline — <strong>1-800-662-4357</strong> (1-800-662-HELP, US)</li>
        </ul>
        <p><strong>Find help near you:</strong></p>
        <ul>
          <li><a href="https://localhelp.healthcare.gov" target="_blank" rel="noopener noreferrer">Local health insurance help — HealthCare.gov navigator finder</a></li>
          <li><a href="https://www.naic.org" target="_blank" rel="noopener noreferrer">Your state insurance department — NAIC lookup</a></li>
          <li>Ask the hospital for the <strong>Patient Advocate / Patient Relations</strong> office.</li>
        </ul>
      </div>`,

  /* E1/D3: find a typed decision wrapper (HA-JEV DecisionOutcome shape)
     that refused to decide for the person. Generic on purpose — any
     payload key whose value carries `outcome: NEEDS_HUMAN` qualifies
     (allowed_next_steps is rendered defensively, never required for
     detection), so surfaces beyond symptoms can adopt without new
     plumbing. A refusal must never silently disappear because its steps
     key was missing or malformed. */
  needsHumanDecision(payload) {
    for (const value of Object.values(payload || {})) {
      if (value && typeof value === 'object' && !Array.isArray(value)
        && String(value.outcome || '').toUpperCase() === 'NEEDS_HUMAN') {
        return value;
      }
    }
    return null;
  },

  needsHumanHtml(payload) {
    const decision = this.needsHumanDecision(payload);
    if (!decision) return '';
    let stepsHtml;
    const raw = decision.allowed_next_steps;
    if (Array.isArray(raw) && raw.length) {
      const steps = raw.map(s => `<li>${this.escapeHtml(String(s))}</li>`).join('');
      stepsHtml = `<p>HealthAdvocate would not answer this on its own. Allowed next steps:</p>
      <ul>${steps}</ul>`;
    } else if (typeof raw === 'string' && raw.trim()) {
      stepsHtml = `<p>HealthAdvocate would not answer this on its own. Allowed next steps:</p>
      <ul><li>${this.escapeHtml(raw)}</li></ul>`;
    } else {
      stepsHtml = `<p>HealthAdvocate would not answer this on its own, and no allowed next steps were attached — treat this as a decision for a person.</p>`;
    }
    /* why it refused + gate state ride along when the typed wrapper
       carries them (restored 2026-09-24 — the banner had dropped both) */
    const reason = typeof decision.reason === 'string' && decision.reason.trim()
      ? `<p class="needs-human-reason">${this.escapeHtml(decision.reason)}</p>`
      : '';
    const gate = typeof decision.gate_state === 'string' && decision.gate_state.trim()
      ? `<p class="muted">gate: ${this.escapeHtml(decision.gate_state)}</p>`
      : '';
    return `<div class="flag-item flag-danger needs-human-banner" role="alert" data-testid="needs-human-banner">
      <p><strong>This needs a human decision.</strong></p>
      ${reason}
      ${stepsHtml}
      ${gate}
      ${this.HUMAN_RESOURCES_HTML}
    </div>`;
  },

  /* D5: an urgency verdict is rendered ONLY for a real low/medium/high
     pick. "unavailable" is the honest model-off state; any other
     missing, null, or unrecognized value is an honest absence too —
     never coerced into a confident MEDIUM badge (an absent verdict is
     not a medium verdict). Neutral notice, no urgency badge class, no
     high/red styling, in every landing order. */
  urgencyBadgeHtml(value) {
    const u = String(value ?? '').trim().toLowerCase();
    if (u === 'unavailable') {
      return `<span class="flag-item flag-info urgency-unavailable" data-testid="urgency-unavailable">Model unavailable — no urgency assessment was made.</span>`;
    }
    if (!['low', 'medium', 'high'].includes(u)) {
      return `<span class="flag-item flag-info urgency-unavailable" data-testid="urgency-unavailable">No urgency assessment was made.</span>`;
    }
    return `<span class="urgency-badge urgency-${u}">${u.toUpperCase()}</span>`;
  },

  safeTrackStatus(value) {
    const status = (value || '').toLowerCase();
    return ['active', 'monitoring', 'resolved'].includes(status) ? status : 'active';
  },

  escapeHtml(str) {
    if (typeof str !== 'string') return '';
    return str.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  },

  /* i18n shorthand for JS-built markup (the i18n frame registers HA.i18n;
     before it loads, or in bare-sandbox tests, fall back to the key) */
  t(key, vars) {
    return this.i18n ? this.i18n.t(key, vars) : key;
  },

  /* ── View Routing ── */

  /* Move focus into a revealed view or panel (WCAG 2.4.3): the control that
     triggered the switch is hidden with the content it belonged to, which
     would otherwise strand keyboard focus on document.body with the new
     content unannounced. Prefer the first heading; fall back to the container. */
  focusInto(container) {
    if (!container) return;
    /* focus management follows modality: keyboard users get focus moved
       (and the visible indicator); after a pointer click, moving focus to
       the heading only paints a selection-style ring — skip it */
    if (this._modality !== 'keyboard') return;
    const target = container.querySelector('h1, h2, h3') || container;
    target.tabIndex = -1;
    target.focus();
  },

  _modality: 'pointer',

  showView(name) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    const target = document.getElementById(`view-${name}`);
    if (target) target.classList.add('active');

    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    const btn = document.querySelector(`.nav-btn[data-view="${name}"]`);
    if (btn) btn.classList.add('active');
    const homeBtn = document.getElementById('btn-home');
    if (homeBtn) homeBtn.classList.toggle('active', name === 'home');

    if (name === 'family') this.loadFamilyProfiles();
    if (name === 'tracks') this.loadTrackDashboard();
    if (name === 'coverage') this.loadCoverageView();
    if (name === 'library') this.renderLibrary();
    if (name === 'directory') this.renderDirectory();
    if (name === 'recorder') this.renderRecentRecordings();
    if (name === 'home') {
      this.loadDashStrip();
      this.renderReminders();
      this.renderHomeLibrary();
      this.initScrollReveal();
    }

    this.focusInto(target);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  /* ── Coverage Continuity (low-energy workflow) ── */

  _coverageCaseId: null,

  setCoverageStatus(message) {
    const el = document.getElementById('coverage-status');
    if (el) el.textContent = message || '';
  },

  async createCoverageCase(e) {
    const btn = e?.currentTarget;
    const titleInput = document.getElementById('coverage-title');
    const title = (titleInput?.value || '').trim() || 'Synthetic coverage case';
    try {
      if (btn) btn.disabled = true;
      const caseData = await this.api('coverage/cases', {
        title,
        next_action: 'Review deadlines and list provider and medication targets',
      });
      this._coverageCaseId = caseData.case_id;
      this.setCoverageStatus('Coverage Case created (synthetic only).');
      await this.loadCoverageView();
      this.focusInto(document.getElementById('coverage-panel'));
    } catch (err) {
      this.setCoverageStatus(err.message || 'Could not create case.');
    } finally {
      if (btn) btn.disabled = false;
    }
  },

  async loadCoverageView() {
    const panel = document.getElementById('coverage-panel');
    if (!this._coverageCaseId) {
      if (panel) panel.hidden = true;
      return;
    }
    try {
      const view = await this.apiGet(`coverage/cases/${this._coverageCaseId}/view`);
      if (panel) panel.hidden = false;
      const primary = document.getElementById('coverage-primary-action');
      if (primary) primary.textContent = view.primary_action?.label || '';
      const riskList = document.getElementById('coverage-risk-list');
      if (riskList) {
        riskList.innerHTML = (view.risks || []).map(r => {
          const status = this.safeRiskStatus(r.status);
          return `<li><span class="risk-chip risk-${status}">${this.escapeHtml(status)}</span> ${this.escapeHtml(r.label)} ${this.escapeHtml(r.due || '')}</li>`;
        }).join('') || '<li><span class="risk-chip risk-unknown">unknown</span> No risks recorded yet</li>';
      }
      const evidence = document.getElementById('coverage-evidence');
      if (evidence) {
        evidence.innerHTML = (view.evidence || []).map(ev =>
          `<div class="muted">${this.escapeHtml(ev.title || '')}: ${this.escapeHtml(ev.summary || '')}</div>`
        ).join('') || '<div class="muted">No evidence yet</div>';
      }
      const contacts = document.getElementById('coverage-contacts');
      if (contacts) {
        contacts.innerHTML = (view.contacts || []).map(c =>
          `<div class="muted">${this.escapeHtml(c.occurred_at || '')} — ${this.escapeHtml(c.summary || '')}</div>`
        ).join('') || '<div class="muted">No contacts yet</div>';
      }
      const targets = document.getElementById('coverage-targets');
      if (targets) {
        targets.innerHTML = (view.targets || []).map(t =>
          `<div class="muted">${this.escapeHtml(t.kind || '')}: ${this.escapeHtml(t.name || '')}</div>`
        ).join('') || '<div class="muted">No continuity targets yet</div>';
      }
    } catch (err) {
      this.setCoverageStatus(err.message || 'Could not load coverage view.');
    }
  },

  safeRiskStatus(value) {
    const s = (value || '').toLowerCase();
    return ['overdue', 'approaching', 'unknown', 'stale', 'conflicted', 'scheduled'].includes(s)
      ? s
      : 'unknown';
  },

  async loadCoverageScript(kind) {
    if (!this._coverageCaseId) {
      this.setCoverageStatus('Create a Coverage Case first.');
      return;
    }
    try {
      const script = await this.apiGet(`coverage/cases/${this._coverageCaseId}/scripts/${kind}`);
      const steps = document.getElementById('coverage-script-steps');
      const note = document.getElementById('coverage-script-note');
      if (steps) {
        steps.innerHTML = (script.steps || []).map(s => `<li>${this.escapeHtml(s)}</li>`).join('');
      }
      if (note) note.textContent = script.commitment_note || script.unknown_fields_policy || '';
    } catch (err) {
      this.setCoverageStatus(err.message || 'Could not load script.');
    }
  },

  async checkCoverageGate() {
    const select = document.getElementById('coverage-intent');
    const intent = select?.value || 'payment';
    const out = document.getElementById('coverage-gate-result');
    try {
      const result = await this.api('coverage/commitment-gate', { intent });
      if (out) {
        out.textContent = `${result.gate_state}: ${result.reason}`;
      }
    } catch (err) {
      if (out) out.textContent = err.message || 'Gate check failed.';
    }
  },

  /* ── Theme Toggle (default: light) ── */

  initTheme() {
    const saved = localStorage.getItem('ha-theme');
    document.documentElement.setAttribute('data-theme', saved === 'light' ? 'light' : 'dark');
    this.updateThemeIcon();
  },

  toggleTheme() {
    /* dark-first home mode: the attribute is always explicit (light|dark);
       the pre-paint head script sets dark unless the user chose light */
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
    const next = isDark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('ha-theme', next);
    this.updateThemeIcon();
  },

  updateThemeIcon() {
    const icon = document.getElementById('theme-icon');
    const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
    const btn = document.getElementById('btn-theme');
    if (isDark) {
      icon.innerHTML = '<path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>';
      btn.setAttribute('aria-label', 'Switch to light theme');
    } else {
      icon.innerHTML = '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>';
      btn.setAttribute('aria-label', 'Switch to dark theme');
    }
  },

  /* ── Scroll Reveal (IntersectionObserver) ── */

  initScrollReveal() {
    if (this._scrollObserver) this._scrollObserver.disconnect();
    this._scrollObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.setAttribute('data-reveal', 'revealed');
          this._scrollObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });

    /* Content is visible by default; JS marks ONLY offscreen elements as
       pending, after the observer exists — no-JS and bfcache restores never
       hide the hero (micro-motion law). */
    document.querySelectorAll('.reveal').forEach(el => {
      if (el.getAttribute('data-reveal') === 'revealed') return;
      /* only mark content clearly below the fold (plus a grace band) —
         near-fold sections stay visible on first paint so home never
         reads as an empty page */
      const below = el.getBoundingClientRect().top > window.innerHeight * 1.2;
      if (below) el.setAttribute('data-reveal', 'pending');
      this._scrollObserver.observe(el);
    });
  },

  /* ── Dashboard Strip ── */

  async loadDashStrip() {
    try {
      const [tracks, profiles] = await Promise.all([
        this.apiGet('tracks/dashboard').catch(() => null),
        this.apiGet('family/profiles').catch(() => []),
      ]);
      let active = 0, resolved = 0, family = 0;
      if (tracks) {
        active = tracks.active || 0;
        resolved = tracks.resolved || 0;
        document.getElementById('dash-active').textContent = active;
        document.getElementById('dash-resolved').textContent = resolved;
      }
      if (Array.isArray(profiles)) {
        family = profiles.length;
        document.getElementById('dash-family').textContent = family;
      }
      /* an untouched night-table shows no empty ledgers: all-zero counts
         read as a broken demo, not as calm */
      const strip = document.querySelector('.dash-strip');
      if (strip && active + resolved + family === 0) strip.hidden = true;
    } catch (err) {
      console.warn('Dashboard strip load failed:', err.message);
    }
  },

  /* ── Loading / Errors ── */

  setLoading(el) {
    el.innerHTML = `<div class="skeleton-wrap" role="status">
      <p class="condition-confidence" style="margin-bottom:12px">Working on this device — local analysis can take a few seconds.</p>
      <div class="skeleton-line h-xl"></div>
      <div class="skeleton-line w-100"></div>
      <div class="skeleton-line w-80"></div>
      <div class="skeleton-line w-60"></div>
    </div>`;
  },

  _setBtnBusy(btn, busy) {
    if (!btn) return;
    btn.disabled = busy;
    if (busy && !btn.dataset.originalText) {
      btn.dataset.originalText = btn.textContent;
      btn.textContent = 'Analyzing...';
    } else if (!busy && btn.dataset.originalText) {
      btn.textContent = btn.dataset.originalText;
      delete btn.dataset.originalText;
    }
  },

  showError(el, msg) {
    el.innerHTML = `<div class="flag-item flag-danger">${this.escapeHtml(msg)}</div>`;
  },

  showEmpty(el, msg) {
    el.innerHTML = `<div class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      <p>${this.escapeHtml(msg)}</p>
    </div>`;
  },

  /* ── Symptom Assessment ── */

  async assessSymptoms(event) {
    const btn = event?.currentTarget;
    const symptoms = document.getElementById('symptom-input').value;
    const el = document.getElementById('symptom-results');
    if (!symptoms.trim()) { this.showEmpty(el, 'Describe your symptoms to get started.'); return; }
    this.setLoading(el);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('symptoms/assess', { symptoms });
      this.renderSymptoms(data, el);
    } catch (err) {
      this.showError(el, err.message);
    } finally {
      this._setBtnBusy(btn, false);
    }
  },

  renderSymptoms(data, el) {
    /* E1: the typed wrapper's refusal leads — before any urgency color,
       so a NEEDS_HUMAN answer can never read as an assessment. */
    let html = this.needsHumanHtml(data);
    html += `
      <div class="result-section"><h3>Urgency Level</h3>
        ${this.urgencyBadgeHtml(data.urgency)}
      </div>
      <div class="result-section"><h3>Explanation</h3>
        <p class="result-text">${this.escapeHtml(data.explanation)}</p>
      </div>`;

    if (data.conditions?.length) {
      /* dictionary name-matches, honestly labeled — recognition is not
         a diagnosis (GLM-5.3-Flash honesty receipt r1: confident-looking
         percentages under a needs-human banner read as an answer) */
      html += `<div class="result-section"><h3>Name Matches — Not a Diagnosis</h3>
        <p class="condition-confidence" style="margin-bottom:10px">These are dictionary name matches found in your text. They are not an assessment${data.urgency === 'unavailable' ? ' — no urgency assessment was made either' : ''}.</p>`;
      for (const c of data.conditions) {
        html += `<div class="condition-item">
          <span class="condition-name">${this.escapeHtml(c.name)}</span>
          <span class="condition-confidence">(name match, ${Math.round(c.confidence * 100)}% string similarity)</span>
        </div>`;
      }
      html += `</div>`;
    }
    if (data.possible_conditions?.length) {
      html += `<div class="result-section"><h3>LLM Assessment</h3>`;
      for (const c of data.possible_conditions) {
        html += `<div class="condition-item">
          <span class="condition-name">${this.escapeHtml(c.name || '')}</span>
          <span class="condition-confidence">(${this.escapeHtml(c.likelihood || '')})</span>
        </div>`;
      }
      html += `</div>`;
    }
    if (data.action_items?.length) {
      html += `<div class="result-section"><h3>Action Items</h3><ol>`;
      for (const a of data.action_items) html += `<li class="result-text">${this.escapeHtml(a)}</li>`;
      html += `</ol></div>`;
    }
    if (data.red_flags?.length) {
      html += `<div class="result-section"><h3>Red Flags</h3>`;
      for (const r of data.red_flags) html += `<div class="flag-item flag-danger">${this.escapeHtml(r)}</div>`;
      html += `</div>`;
    }
    if (data.validation) {
      /* B3: this number is informal name overlap between two extraction
         methods — honest label, never presented as clinical validation. */
      html += `<div class="result-section"><h3>Name overlap (informal)</h3>
        <div class="condition-item"><span class="condition-name">Name overlap</span> <span class="condition-confidence">${this.escapeHtml(data.validation.reliability || 'N/A')}</span></div>
        <p class="condition-confidence">An informal overlap check between two extraction methods — not a check of clinical accuracy.</p>
        ${data.validation.urgency_disagreement ? '<div class="flag-item flag-danger">Urgency disagreement detected — upgraded to HIGH for safety.</div>' : ''}
      </div>`;
    }
    el.innerHTML = html;
  },

  /* ── Document Decoder ── */

  async decodeDocument(event) {
    const btn = event?.currentTarget;
    const text = document.getElementById('doc-input').value;
    const el = document.getElementById('doc-results');
    if (!text.trim()) { this.showEmpty(el, 'Paste a medical document to decode.'); return; }
    this.setLoading(el);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('documents/decode', { text });
      this.renderDocument(data, el);
    } catch (err) { this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  async shareSafe(event) {
    const btn = event?.currentTarget;
    const src = document.getElementById(btn?.dataset.shareSource || 'doc-input');
    const out = document.getElementById(btn?.dataset.shareOut || 'doc-results');
    if (!src || !src.value.trim()) { this.showEmpty(out, 'Nothing to make share-safe yet.'); return; }
    this.setLoading(out);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('privacy/share-safe', { text: src.value });
      this.renderShareSafe(data, out);
    } catch (err) { this.showError(out, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  renderShareSafe(data, out) {
    const countsLine = data.total === 0
      ? HA.t('sharesafe.nothing', null, 'Nothing personal found — this text was already safe to share.')
      : HA.t('sharesafe.removed', { n: data.total }, 'Removed {n} personal details.');
    const detail = Object.entries(data.counts || {}).map(([k, v]) => `${v} × ${k}`).join(' · ');
    out.innerHTML = `<div class="result-section share-safe-box">
      <h3>${HA.t('sharesafe.title', null, 'Share-safe copy')}</h3>
      <p class="condition-confidence">${countsLine}</p>
      ${detail ? `<p class="share-safe-detail">${this.escapeHtml(detail)}</p>` : ''}
      <textarea id="share-safe-out" rows="6" readonly>${this.escapeHtml(data.clean_text)}</textarea>
      <div class="row-actions">
        <button type="button" class="btn-ghost btn-sm" data-action="share-safe-copy">${HA.t('sharesafe.copy', null, 'Copy clean text')}</button>
        <button type="button" class="btn-ghost btn-sm" data-action="share-safe-download">${HA.t('sharesafe.download', null, 'Download .txt')}</button>
        <button type="button" class="btn-ghost btn-sm" data-action="share-safe-back">${HA.t("sharesafe.back", null, "Back to results")}</button>
      </div>
      <p class="hand-note">${HA.t('sharesafe.note', null, 'removed on this device — nothing was sent anywhere.')}</p>
    </div>`;
  },

  renderDocument(data, el) {
    let html = `<div class="result-section"><h3>Summary</h3><p class="result-text">${this.escapeHtml(data.explanation)}</p></div>`;
    if (data.urgency) {
      html += `<div class="result-section"><h3>Urgency</h3>
        ${this.urgencyBadgeHtml(data.urgency)}</div>`;
    }
    if (data.entities?.length) {
      html += `<div class="result-section"><h3>Medical Entities</h3><div class="entity-list">`;
      for (const e of data.entities) html += `<span class="entity-chip ${this.safeEntityClass(e.category)}">${this.escapeHtml(e.text)} <small>(${this.escapeHtml(e.category)})</small></span>`;
      html += `</div></div>`;
    }
    if (data.medical_terms_explained?.length) {
      html += `<div class="result-section"><h3>Terms Explained</h3>`;
      for (const t of data.medical_terms_explained) html += `<div class="condition-item"><strong>${this.escapeHtml(t.term)}</strong>: ${this.escapeHtml(t.explanation)}</div>`;
      html += `</div>`;
    }
    if (data.action_items?.length) {
      html += `<div class="result-section"><h3>Action Items</h3><ol>`;
      for (const a of data.action_items) html += `<li class="result-text">${this.escapeHtml(a)}</li>`;
      html += `</ol></div>`;
    }
    if (data.red_flags?.length) {
      html += `<div class="result-section"><h3>Red Flags</h3>`;
      for (const r of data.red_flags) html += `<div class="flag-item flag-danger">${this.escapeHtml(r)}</div>`;
      html += `</div>`;
    }
    /* B3: honest PII reporting. `pii_found_and_masked` is true ONLY when
       the scan found and masked personal information; false/absent means
       none was found — never a guarantee that none slipped through.
       (DEPRECATED fallback: `pii_scrubbed` is kept one release; it read
       like a confirmation.) */
    const piiMasked = data.pii_found_and_masked !== undefined
      ? data.pii_found_and_masked
      : data.pii_scrubbed;
    if (data.pii_found?.length) {
      html += `<div class="result-section"><h3>Personal Information Detected</h3>`;
      for (const p of data.pii_found) html += `<div class="flag-item flag-warning">Found ${this.escapeHtml(p.category || 'PII')}: "${this.escapeHtml(p.text)}"</div>`;
      if (piiMasked === true) html += `<p class="condition-confidence">These items were found and masked before analysis.</p>`;
      html += `</div>`;
    } else if (piiMasked === false) {
      html += `<div class="result-section"><h3>Personal Information</h3>
        <p class="condition-confidence">No personal information was found by the automated scan — this is not a guarantee.</p>
      </div>`;
    }
    el.innerHTML = html;
  },

  /* ── Bill Decoder ── */

  async decodeBill(event) {
    const btn = event?.currentTarget;
    const bill_text = document.getElementById('bill-input').value;
    const el = document.getElementById('bill-results');
    if (!bill_text.trim()) { this.showEmpty(el, 'Paste a medical bill to analyze.'); return; }
    this.setLoading(el);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('bills/decode', { bill_text });
      this.renderBill(data, el);
    } catch (err) { this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  renderBill(data, el) {
    let html = '';
    if (data.total) html += `<div class="result-section"><h3>Total</h3><div class="bill-total">${this.escapeHtml(data.total)}</div></div>`;
    if (data.urgency) {
      html += `<div class="result-section"><h3>Urgency</h3>
        ${this.urgencyBadgeHtml(data.urgency)}</div>`;
    }
    if (data.explanation) html += `<div class="result-section"><h3>Explanation</h3><p class="result-text">${this.escapeHtml(data.explanation)}</p></div>`;
    if (data.action_items?.length) {
      html += `<div class="result-section"><h3>Action Items</h3><ol>`;
      for (const a of data.action_items) html += `<li class="result-text">${this.escapeHtml(a)}</li>`;
      html += `</ol></div>`;
    }
    if (data.suspicious_charges?.length) {
      html += `<div class="result-section"><h3>Suspicious Charges</h3>`;
      for (const c of data.suspicious_charges) html += `<div class="flag-item flag-warning">${this.escapeHtml(c)}</div>`;
      html += `</div>`;
    }
    if (data.red_flags?.length) {
      html += `<div class="result-section"><h3>Red Flags</h3>`;
      for (const r of data.red_flags) html += `<div class="flag-item flag-danger">${this.escapeHtml(r)}</div>`;
      html += `</div>`;
    }
    if (data.billing_rights?.length) {
      html += `<div class="result-section"><h3>Your Billing Rights</h3><ul>`;
      for (const r of data.billing_rights) html += `<li class="result-text">${this.escapeHtml(r)}</li>`;
      html += `</ul></div>`;
    }
    if (!data.explanation && !data.suspicious_charges?.length && !data.red_flags?.length) html = '<p class="result-text">No bill issues detected. Try pasting a more detailed bill.</p>';
    /* F1a: the bill is evidence — offer to carry it into the appeal studio */
    html += `<div class="cat-links" style="margin-top:12px">
      <button type="button" class="btn-secondary" data-action="appeal-from-bill">${this.escapeHtml(this.t('appeal.from_bill'))}</button>
    </div>`;
    el.innerHTML = html;
  },

  /* ── Insurance Denial Fighter ── */

  async fightDenial(event) {
    const btn = event?.currentTarget;
    const denial_text = document.getElementById('denial-input').value;
    const el = document.getElementById('denial-results');
    if (!denial_text.trim()) { this.showEmpty(el, 'Paste a denial letter to analyze.'); return; }
    const patient_info = document.getElementById('denial-patient-info')?.value || '';
    this.setLoading(el);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('insurance/fight', { denial_text, patient_info });
      this.renderDenial(data, el);
    } catch (err) { this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  renderDenial(data, el) {
    let html = this.needsHumanHtml(data.denial_reason_decision ? { ...data, urgency_decision: data.denial_reason_decision } : data);
    if (data.urgency) {
      html += `<div class="result-section"><h3>Urgency</h3>
        ${this.urgencyBadgeHtml(data.urgency)}</div>`;
    }
    if (data.explanation) html += `<div class="result-section"><h3>What This Denial Means</h3><p class="result-text">${this.escapeHtml(data.explanation)}</p></div>`;
    if (data.denial_reason) html += `<div class="result-section"><h3>Denial Reason</h3><p class="result-text">${this.escapeHtml(data.denial_reason)}</p></div>`;
    if (data.red_flags?.length) {
      html += `<div class="result-section"><h3>Red Flags</h3>`;
      for (const r of data.red_flags) html += `<div class="flag-item flag-danger">${this.escapeHtml(r)}</div>`;
      html += `</div>`;
    }
    if (data.appeal_arguments?.length) {
      html += `<div class="result-section"><h3>Arguments for Your Appeal</h3><ol>`;
      for (const a of data.appeal_arguments) html += `<li class="result-text">${this.escapeHtml(a)}</li>`;
      html += `</ol></div>`;
    }
    if (data.action_items?.length) {
      html += `<div class="result-section"><h3>Action Items</h3><ol>`;
      for (const a of data.action_items) html += `<li class="result-text">${this.escapeHtml(a)}</li>`;
      html += `</ol></div>`;
    }
    if (data.draft_appeal) html += `<div class="result-section"><h3>Draft Appeal Letter</h3><div class="appeal-letter">${this.escapeHtml(data.draft_appeal)}</div></div>`;
    if (data.entities_found) {
      html += `<div class="result-section"><h3>Medical Entities Found</h3>`;
      if (data.entities_found.conditions?.length) {
        html += `<div class="condition-item"><strong>Conditions:</strong> ${this.escapeHtml(data.entities_found.conditions.map(c => c.text).join(', '))}</div>`;
      }
      if (data.entities_found.medications?.length) {
        html += `<div class="condition-item"><strong>Medications:</strong> ${this.escapeHtml(data.entities_found.medications.map(m => m.text).join(', '))}</div>`;
      }
      html += `</div>`;
    }
    el.innerHTML = html;
  },

  /* ── F1a: Appeal Letter Studio (case file → editable letter) ── */

  async generateAppealLetter(event) {
    const btn = event?.currentTarget;
    const denial = document.getElementById('denial-input')?.value || '';
    const el = document.getElementById('appeal-letter-results');
    if (!el) return;
    if (!denial.trim()) { this.showEmpty(el, this.t('appeal.needs_denial')); return; }
    const record_text = document.getElementById('appeal-record-input')?.value || '';
    const user_words = document.getElementById('appeal-words-input')?.value || '';
    this.setLoading(el);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('insurance/appeal-letter', { denial_text: denial, record_text, user_words });
      this._appealLetterData = data;
      this.renderAppealLetter(data, el);
    } catch (err) { this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  renderAppealLetter(data, el) {
    if (!data.letter) {
      el.innerHTML = `<div class="flag-item flag-warning">${this.escapeHtml(data.note || this.t('appeal.needs_denial'))}</div>`;
      return;
    }
    const chip = data.model_generated
      ? this.provChip('inferred', this.t('appeal.inferred_label'))
      : this.provChip('extracted', this.t('appeal.assembled_label'));
    const originNote = data.model_generated
      ? `<p class="condition-confidence">${this.escapeHtml(this.t('appeal.model_note'))}</p>`
      : `<p class="condition-confidence">${this.escapeHtml(data.note || this.t('appeal.assembled_note'))}</p>`;
    const needsHuman = data.needs_human
      ? `<div class="flag-item flag-danger" role="alert" data-testid="appeal-needs-human">
           <p><strong>${this.escapeHtml(this.t('appeal.needs_human_head'))}</strong></p>
           <p>${this.escapeHtml(this.t('appeal.needs_human_body'))}</p>
         </div>`
      : '';
    const citations = (data.citations || []).map(c =>
      `<li>${this.escapeHtml(c.fact)} — <em>${this.escapeHtml(c.source)}</em></li>`).join('');
    el.innerHTML = `
      <div class="result-section">
        <h3>${this.escapeHtml(this.t('appeal.letter_head'))} ${chip}</h3>
        ${originNote}
        ${needsHuman}
        <label class="field-label" for="appeal-letter-text">${this.escapeHtml(this.t('appeal.edit_label'))}</label>
        <textarea id="appeal-letter-text" class="intake-sheet" rows="14">${this.escapeHtml(data.letter)}</textarea>
        <div class="cat-links" style="margin-top:10px">
          <button type="button" class="btn-primary btn-sm" data-action="appeal-letter-download">${this.escapeHtml(this.t('appeal.download'))}</button>
          <button type="button" class="btn-secondary" data-action="appeal-letter-print">${this.escapeHtml(this.t('appeal.print'))}</button>
        </div>
      </div>
      <div class="result-section">
        <h3>${this.escapeHtml(this.t('appeal.citations_head'))}</h3>
        <p class="condition-confidence">${this.escapeHtml(this.t('appeal.citations_note'))}</p>
        <ol>${citations}</ol>
      </div>`;
  },

  downloadAppealLetter() {
    const text = document.getElementById('appeal-letter-text')?.value
      || this._appealLetterData?.letter || '';
    if (!text) return;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'healthadvocate-appeal-letter.txt';
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    this.toast(this.t('appeal.downloaded'));
  },

  printAppealLetter() {
    const text = document.getElementById('appeal-letter-text')?.value
      || this._appealLetterData?.letter || '';
    if (!text) return;
    const w = window.open('', '_blank');
    if (!w) { this.toast(this.t('appeal.print_blocked')); return; }
    w.document.write(`<pre style="font-family:Georgia,serif;font-size:12pt;white-space:pre-wrap;margin:2cm">${this.escapeHtml(text)}</pre>`);
    w.document.close();
    w.focus();
    w.print();
  },

  appealFromBill() {
    const billText = document.getElementById('bill-input')?.value || '';
    const record = document.getElementById('appeal-record-input');
    if (record && billText.trim() && !record.value.trim()) record.value = billText;
    this.showView('insurance');
    this.toast(this.t('appeal.bill_attached'));
    const studio = document.getElementById('appeal-letter-results');
    if (studio) this.focusInto(studio.closest('.appeal-studio') || studio);
  },

  appealFromLibrary(item) {
    const denial = document.getElementById('denial-input');
    if (denial && !denial.value.trim()) {
      denial.value = `${item.title} — ${item.desc}`;
    }
    this.showView('insurance');
    this.toast(this.t('appeal.denial_attached'));
  },

  /* ── Drug Checker ── */

  async checkDrug(event) {
    const btn = event?.currentTarget;
    const drug_name = document.getElementById('drug-input').value;
    const el = document.getElementById('drug-results');
    if (!drug_name.trim()) { this.showEmpty(el, 'Enter a drug name to check.'); return; }
    this.setLoading(el);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('drugs/check', { drug_name });
      this.renderDrug(data, el);
    } catch (err) { this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  renderDrug(data, el) {
    let html = `<div class="result-section"><h3>${this.escapeHtml(data.drug)}</h3><div class="drug-class">${this.escapeHtml(data.drug_class)}</div>`;
    /* B3: name matching, honestly labeled — a dictionary name match is
       recognition, not verification. (DEPRECATED fallback: `ner_verified`
       is kept one release; it overstated the check.) */
    const nameMatch = data.ner_name_match !== undefined ? data.ner_name_match : data.ner_verified;
    if (nameMatch === true) {
      html += `<p class="condition-confidence">This name was recognized by name matching against the medical dictionary.</p>`;
    } else if (nameMatch === false) {
      html += `<p class="condition-confidence">This name was not recognized by name matching — treat the information below with extra caution.</p>`;
    }
    if (data.generic_available === true) html += `<div class="drug-generic">${this.escapeHtml(data.generic_name)}</div>`;
    else if (data.generic_available === "Unknown") html += `<p class="result-text">Generic availability unknown. ${this.escapeHtml(data.cost_note || '')}</p>`;
    /* honesty law (GLM-5.3-Flash receipt r1): a name-match-only response
       must never read like a completed drug review */
    if (data.generic_available !== true && !(data.alternatives || []).length && !data.cost_note) {
      html += `<div class="flag-item flag-info urgency-unavailable">No drug details were generated — the optional model is off. Only the name match above is real; this is not a drug review.</div>`;
    }
    if (data.alternatives?.length) {
      html += `<h4 style="margin-top:14px;font-size:11px;text-transform:uppercase;letter-spacing:0.06em;color:var(--text-3)">Alternatives</h4><ul class="alt-list">`;
      for (const a of data.alternatives) html += `<li>${this.escapeHtml(a)}</li>`;
      html += `</ul>`;
    }
    if (data.cost_note) html += `<p class="result-text" style="margin-top:14px">${this.escapeHtml(data.cost_note)}</p>`;
    html += `</div>`;
    el.innerHTML = html;
  },

  /* ── Appointment Prep ── */

  async prepareAppointment(event) {
    const btn = event?.currentTarget;
    const symptoms = document.getElementById('appt-symptoms').value;
    const el = document.getElementById('appt-results');
    if (!symptoms.trim()) { this.showEmpty(el, 'Describe your symptoms or reason for the visit.'); return; }
    const concern = document.getElementById('appt-concern').value;
    this.setLoading(el);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('appointments/prepare', { symptoms, concern });
      this.renderAppointment(data, el);
    } catch (err) { this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  renderAppointment(data, el) {
    let html = '';
    if (data.talking_points?.length) {
      html += `<div class="result-section"><h3>Talking Points</h3><ol>`;
      for (const tp of data.talking_points) html += `<li class="result-text">${this.escapeHtml(tp)}</li>`;
      html += `</ol></div>`;
    }
    if (data.questions_to_ask?.length) {
      html += `<div class="result-section"><h3>Questions to Ask</h3><ol>`;
      for (const q of data.questions_to_ask) html += `<li class="result-text">${this.escapeHtml(q)}</li>`;
      html += `</ol></div>`;
    }
    if (data.advocacy_script) html += `<div class="result-section"><h3>Your Advocacy Script</h3><div class="script-block">${this.escapeHtml(data.advocacy_script)}</div></div>`;
    el.innerHTML = html;
  },

  /* ── Discharge Translator ── */

  async translateDischarge(event) {
    const btn = event?.currentTarget;
    const text = document.getElementById('discharge-input').value;
    const el = document.getElementById('discharge-results');
    if (!text.trim()) { this.showEmpty(el, 'Paste discharge instructions to translate.'); return; }
    this.setLoading(el);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('discharge/translate', { text });
      this.renderDischarge(data, el);
    } catch (err) { this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  renderDischarge(data, el) {
    let html = '';
    if (data.urgency) {
      html += `<div class="result-section"><h3>Urgency</h3>
        ${this.urgencyBadgeHtml(data.urgency)}</div>`;
    }
    if (data.explanation) html += `<div class="result-section"><h3>Plain Language Summary</h3><div class="plain-language">${this.escapeHtml(data.explanation)}</div></div>`;
    if (data.medication_instructions?.length) {
      html += `<div class="result-section"><h3>Medication Instructions</h3><ul>`;
      for (const m of data.medication_instructions) html += `<li class="result-text">${this.escapeHtml(m)}</li>`;
      html += `</ul></div>`;
    }
    if (data.warning_signs?.length) {
      html += `<div class="result-section"><h3>Warning Signs — When to Go Back to the ER</h3>`;
      for (const w of data.warning_signs) html += `<div class="flag-item flag-danger">${this.escapeHtml(w)}</div>`;
      html += `</div>`;
    }
    if (data.red_flags?.length) {
      html += `<div class="result-section"><h3>Red Flags</h3>`;
      for (const r of data.red_flags) html += `<div class="flag-item flag-danger">${this.escapeHtml(r)}</div>`;
      html += `</div>`;
    }
    if (data.follow_up_steps?.length) {
      html += `<div class="result-section"><h3>Follow-Up Steps</h3><ol>`;
      for (const f of data.follow_up_steps) html += `<li class="result-text">${this.escapeHtml(f)}</li>`;
      html += `</ol></div>`;
    }
    if (data.action_items?.length) {
      html += `<div class="result-section"><h3>Action Items</h3><ol>`;
      for (const a of data.action_items) html += `<li class="result-text">${this.escapeHtml(a)}</li>`;
      html += `</ol></div>`;
    }
    if (data.medications_detected?.length) {
      html += `<div class="result-section"><h3>Medications Detected</h3><div class="entity-list">`;
      for (const m of data.medications_detected) html += `<span class="entity-chip drug">${this.escapeHtml(m.name)}</span>`;
      html += `</div></div>`;
    }
    el.innerHTML = html;
  },

  /* ── Second Opinion ── */

  async createSecondOpinion(event) {
    const btn = event?.currentTarget;
    const records = document.getElementById('secondop-input').value;
    const el = document.getElementById('secondop-results');
    if (!records.trim()) { this.showEmpty(el, 'Paste medical records to create a brief.'); return; }
    this.setLoading(el);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('second-opinion/create', { records });
      this.renderSecondOpinion(data, el);
    } catch (err) { this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  renderSecondOpinion(data, el) {
    let html = '';
    if (data.urgency) {
      html += `<div class="result-section"><h3>Urgency</h3>
        ${this.urgencyBadgeHtml(data.urgency)}</div>`;
    }
    if (data.explanation) html += `<div class="result-section"><h3>Summary for Second Opinion</h3><p class="result-text">${this.escapeHtml(data.explanation)}</p></div>`;
    if (data.conditions?.length) {
      html += `<div class="result-section"><h3>Conditions</h3><div class="entity-list">`;
      for (const c of data.conditions) html += `<span class="entity-chip disease">${this.escapeHtml(c.text)}</span>`;
      html += `</div></div>`;
    }
    if (data.medications?.length) {
      html += `<div class="result-section"><h3>Medications</h3><div class="entity-list">`;
      for (const m of data.medications) html += `<span class="entity-chip drug">${this.escapeHtml(m.text)}</span>`;
      html += `</div></div>`;
    }
    if (data.key_questions?.length) {
      html += `<div class="result-section"><h3>Key Questions for the Specialist</h3><ol>`;
      for (const q of data.key_questions) html += `<li class="result-text">${this.escapeHtml(q)}</li>`;
      html += `</ol></div>`;
    }
    if (data.records_to_bring?.length) {
      html += `<div class="result-section"><h3>Records to Bring</h3><ul>`;
      for (const r of data.records_to_bring) html += `<li class="result-text">${this.escapeHtml(r)}</li>`;
      html += `</ul></div>`;
    }
    if (data.treatment_concerns?.length) {
      html += `<div class="result-section"><h3>Treatment Concerns</h3>`;
      for (const c of data.treatment_concerns) html += `<div class="flag-item flag-warning">${this.escapeHtml(c)}</div>`;
      html += `</div>`;
    }
    if (data.action_items?.length) {
      html += `<div class="result-section"><h3>Action Items</h3><ol>`;
      for (const a of data.action_items) html += `<li class="result-text">${this.escapeHtml(a)}</li>`;
      html += `</ol></div>`;
    }
    if (data.deidentified_records) html += `<div class="result-section"><h3>De-identified Records (safe to share)</h3><div class="plain-language">${this.escapeHtml(data.deidentified_records)}</div></div>`;
    el.innerHTML = html;
  },

  /* ── Community Health Scanner ── */

  async scanCommunity(event) {
    const btn = event?.currentTarget;
    const text = document.getElementById('community-input').value;
    const el = document.getElementById('community-results');
    if (!text.trim()) { this.showEmpty(el, 'Paste a health bulletin to scan.'); return; }
    this.setLoading(el);
    this._setBtnBusy(btn, true);
    try {
      const data = await this.api('community/scan', { text });
      this.renderCommunity(data, el);
    } catch (err) { this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  renderCommunity(data, el) {
    let html = '';
    if (data.urgency) {
      html += `<div class="result-section"><h3>Urgency</h3>
        ${this.urgencyBadgeHtml(data.urgency)}</div>`;
    }
    if (data.explanation) html += `<div class="result-section"><h3>Summary</h3><p class="result-text">${this.escapeHtml(data.explanation)}</p></div>`;
    if (data.credibility) {
      const credClass = data.credibility === 'low' ? 'flag-danger' : data.credibility === 'high' ? 'flag-info' : 'flag-warning';
      html += `<div class="result-section"><h3>Credibility</h3><div class="flag-item ${credClass}">Credibility: ${this.escapeHtml(String(data.credibility).toUpperCase())}</div></div>`;
    }
    if (data.scientific_context) html += `<div class="result-section"><h3>Scientific Context</h3><p class="result-text">${this.escapeHtml(data.scientific_context)}</p></div>`;
    if (data.recommended_action) html += `<div class="result-section"><h3>Recommended Action</h3><p class="result-text">${this.escapeHtml(data.recommended_action)}</p></div>`;
    if (data.red_flags?.length) {
      html += `<div class="result-section"><h3>Red Flags</h3>`;
      for (const r of data.red_flags) html += `<div class="flag-item flag-danger">${this.escapeHtml(r)}</div>`;
      html += `</div>`;
    }
    if (data.action_items?.length) {
      html += `<div class="result-section"><h3>Action Items</h3><ol>`;
      for (const a of data.action_items) html += `<li class="result-text">${this.escapeHtml(a)}</li>`;
      html += `</ol></div>`;
    }
    if (data.conditions_detected?.length) {
      html += `<div class="result-section"><h3>Conditions Detected</h3><div class="entity-list">`;
      for (const c of data.conditions_detected) html += `<span class="entity-chip disease">${this.escapeHtml(c.name)}</span>`;
      html += `</div></div>`;
    }
    if (data.treatments_detected?.length) {
      html += `<div class="result-section"><h3>Treatments Detected</h3><div class="entity-list">`;
      for (const t of data.treatments_detected) html += `<span class="entity-chip drug">${this.escapeHtml(t.name)}</span>`;
      html += `</div></div>`;
    }
    if (!html) html = '<p class="result-text">No significant findings detected in this text.</p>';
    el.innerHTML = html;
  },

  /* ── Family Tracker ── */

  async createFamilyProfile(event) {
    const btn = event?.currentTarget;
    const name = document.getElementById('family-name').value;
    const relationship = document.getElementById('family-relationship').value;
    const el = document.getElementById('family-list');
    if (!name.trim()) return;
    this._setBtnBusy(btn, true);
    try {
      await this.api('family/profiles', { name, relationship });
      document.getElementById('family-name').value = '';
      this.loadFamilyProfiles();
    } catch (err) { this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  async loadFamilyProfiles() {
    const el = document.getElementById('family-list');
    if (!el) return;
    try {
      const profiles = await this.apiGet('family/profiles');
      this.renderFamilyProfiles(profiles, el);
    } catch (err) {
      el.innerHTML = '<p class="result-text" style="color:var(--text-3)">Could not load family profiles.</p>';
    }
  },

  renderFamilyProfiles(profiles, el) {
    if (!profiles.length) {
      this.showEmpty(el, 'No family members added yet. Add someone above.');
      return;
    }
    let html = '';
    for (const p of profiles) {
      const conds = p.conditions.map(c => c.name).join(', ') || 'None';
      const meds = p.medications.map(m => m.name).join(', ') || 'None';
      html += `<div class="profile-card">
        <span class="profile-name">${this.escapeHtml(p.name)}</span>
        <span class="profile-relationship"> (${this.escapeHtml(p.relationship)})</span>
        <div class="profile-detail"><strong>Conditions:</strong> ${this.escapeHtml(conds)}</div>
        <div class="profile-detail"><strong>Medications:</strong> ${this.escapeHtml(meds)}</div>
        <div style="margin-top:10px">
          <input type="text" id="cond-${p.id}" placeholder="Add condition" aria-label="Add condition for ${this.escapeHtml(p.name)}" style="width:45%;font-size:13px">
          <button class="btn-ghost btn-sm" data-action="add-condition" data-profile-id="${p.id}">Add</button>
        </div>
      </div>`;
    }
    el.innerHTML = html;
  },

  async addCondition(profileId) {
    const input = document.getElementById(`cond-${profileId}`);
    if (!input?.value.trim()) return;
    try {
      await this.api(`family/profiles/${profileId}/conditions`, { condition: input.value });
      this.loadFamilyProfiles();
    } catch (err) {
      const el = document.getElementById('family-list');
      if (el) this.showError(el, err.message);
    }
  },

  /* ── Health Tracks ── */

  async createTrack(event) {
    const btn = event?.currentTarget;
    const concern = document.getElementById('track-concern').value;
    const category = document.getElementById('track-category').value;
    const el = document.getElementById('track-dashboard');
    if (!concern.trim()) return;
    this._setBtnBusy(btn, true);
    try {
      await this.api('tracks', { concern, category });
      document.getElementById('track-concern').value = '';
      this.loadTrackDashboard();
    } catch (err) { if (el) this.showError(el, err.message); } finally { this._setBtnBusy(btn, false); }
  },

  async loadTrackDashboard() {
    const el = document.getElementById('track-dashboard');
    if (!el) return;
    try {
      const data = await this.apiGet('tracks/dashboard');
      this.renderTrackDashboard(data, el);
    } catch {
      el.innerHTML = '<p class="result-text" style="color:var(--text-3)">Could not load tracks.</p>';
    }
  },

  renderTrackDashboard(data, el) {
    let html = `<div class="dashboard-stats">
      <div class="stat-card"><div class="stat-number">${this.escapeHtml(String(data.active))}</div><div class="stat-label">Active</div></div>
      <div class="stat-card"><div class="stat-number">${this.escapeHtml(String(data.monitoring))}</div><div class="stat-label">Monitoring</div></div>
      <div class="stat-card"><div class="stat-number">${this.escapeHtml(String(data.resolved))}</div><div class="stat-label">Resolved</div></div>
    </div>`;

    if (data.tracks?.length) {
      for (const t of data.tracks) {
        const safeStatus = this.safeTrackStatus(t.status);
        const statusClass = this.escapeHtml(safeStatus);
        html += `<div class="track-item">
          <div><span class="track-concern">${this.escapeHtml(t.concern)}</span><small style="color:var(--text-3);margin-left:6px">${this.escapeHtml(t.category)}</small></div>
          <div style="display:flex;align-items:center;gap:6px">
            <span class="track-status ${statusClass}">${statusClass}</span>
            ${safeStatus !== 'resolved' ? `<button class="btn-ghost btn-sm" data-action="update-track" data-track-id="${t.id}" data-status="resolved">Resolve</button>` : ''}
            ${safeStatus === 'active' ? `<button class="btn-ghost btn-sm" data-action="update-track" data-track-id="${t.id}" data-status="monitoring">Monitor</button>` : ''}
          </div>
        </div>`;
      }
    } else {
      this.showEmpty(el, 'No health tracks yet. Start tracking a concern above.');
      return;
    }
    el.innerHTML = html;
  },

  async updateTrackStatus(trackId, status) {
    try {
      await this.api(`tracks/${trackId}`, { status });
      this.loadTrackDashboard();
    } catch (err) {
      const el = document.getElementById('track-dashboard');
      if (el) this.showError(el, err.message);
    }
  },

  /* ── Toast (role=status, bottom-center; never the only record) ── */

  toast(message) {
    const region = document.getElementById('toast-region');
    if (!region) return;
    const el = document.createElement('div');
    el.className = 'ha-toast';
    el.setAttribute('role', 'status');
    el.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg><span>${this.escapeHtml(message)}</span>`;
    region.appendChild(el);
    setTimeout(() => el.remove(), 4000);
  },

  /* ── Provenance chips (analysis + directory honesty) ── */

  provChip(kind, label) {
    return `<span class="prov-chip prov-${this.escapeHtml(kind)}">${this.escapeHtml(label)}</span>`;
  },

  /* ── Reminders / "What's coming up" (demo data, local-only) ── */

  REMINDERS: [
    {
      id: 'r1', state: 'due-soon',
      title: 'Appeal deadline — Aetna MRI denial',
      context: 'Matter: MRI denial (Aetna) · detected in the Sep 24 call',
      when: { top: 'FRI', main: '26' },
      contact: { name: 'Aetna member services', phone: '+1-800-555-0142' },
      gotoView: 'library',
      prov: ['extracted', 'from the call'],
    },
    {
      id: 'r2', state: 'upcoming',
      title: 'Appointment with Dr. Patel',
      context: 'Follow-up · 9:40 AM · bring the imaging CD',
      when: { top: 'SEP', main: '30' },
      contact: { name: 'Dr. Maya Patel', phone: '+1-555-010-7788' },
      gotoView: 'appointments',
    },
    {
      id: 'r3', state: 'overdue',
      title: 'Refill metformin',
      context: 'Pharmacy says the prescription expired 4 days ago',
      when: { top: 'SEP', main: '20' },
      contact: { name: 'Corner Pharmacy', phone: '+1-555-010-4432' },
      gotoView: 'drugs',
    },
    {
      id: 'r4', state: 'done',
      title: 'Ask billing about the $1,200 charge',
      context: 'Resolved in the Sep 24 call — itemized bill requested',
      when: { top: 'SEP', main: '24' },
      contact: null,
      gotoView: 'bills',
    },
  ],

  reminderStateLabel: { 'upcoming': 'Upcoming', 'due-soon': 'Due soon', 'overdue': 'Overdue', 'done': 'Done' },

  renderReminders() {
    const list = document.getElementById('reminder-list');
    const panel = document.getElementById('coming-up');
    if (!list || !panel) return;
    list.innerHTML = this.REMINDERS.map(r => {
      const call = r.contact && r.state !== 'done'
        ? `<div class="reminder-actions">
             <a class="contact-action" href="tel:${this.escapeHtml(r.contact.phone.replace(/[^+\d]/g, ''))}">
               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
               Call ${this.escapeHtml(r.contact.name)}
             </a>
             <button type="button" class="xref-chip" data-goto="${this.escapeHtml(r.gotoView || 'library')}">Open</button>
           </div>` : '';
      return `<article class="reminder-card" data-state="${this.escapeHtml(r.state)}">
        <span class="reminder-when"><strong>${this.escapeHtml(r.when.main)}</strong>${this.escapeHtml(r.when.top)}</span>
        <span class="reminder-body">
          <span class="reminder-title">${this.escapeHtml(r.title)}</span>
          <span class="reminder-context">${this.escapeHtml(r.context)}</span>
          ${r.prov ? `<span class="reminder-prov">${this.provChip(r.prov[0], r.prov[1])}</span>` : ''}
          ${call}
        </span>
        <span class="reminder-state ${this.escapeHtml(r.state)}">${this.reminderStateLabel[r.state]}</span>
      </article>`;
    }).join('');
    panel.hidden = false;
    const dueCount = this.REMINDERS.filter(r => r.state === 'due-soon').length;
    const badge = document.getElementById('due-badge');
    const count = document.getElementById('due-badge-count');
    const words = badge ? badge.querySelector('.due-badge-words') : null;
    if (badge) {
      if (dueCount > 0) {
        if (count) count.textContent = String(dueCount);
        if (words) words.textContent = dueCount === 1 ? ' reminder due soon' : ' reminders due soon';
        badge.hidden = false;
      } else {
        badge.hidden = true;
      }
    }
  },

  /* ── From your library (home panel — recent items, demo data) ── */

  renderHomeLibrary() {
    const el = document.getElementById('home-lib-list');
    if (!el) return;
    const recent = this.CATALOG.slice(0, 3);
    el.innerHTML = recent.map(it => `
      <button type="button" class="home-lib-item" data-goto="library" aria-label="Open ${this.escapeHtml(it.title)} in the library">
        <span class="cat-kind ${this.escapeHtml(it.kind)}" aria-hidden="true">${this.KIND_ICON[it.kind] || ''}</span>
        <span class="home-lib-body">
          <span class="home-lib-title">${this.escapeHtml(it.title)}</span>
          <span class="home-lib-meta">${this.escapeHtml(it.matter)} · ${this.escapeHtml(it.when)}</span>
        </span>
      </button>`).join('');
  },

  /* ── Library / Catalog (demo data) ── */

  CATALOG: [
    {
      id: 'c1', kind: 'call', when: 'Sep 24 · 11:02', matter: 'MRI denial (Aetna)',
      title: 'Aetna — MRI denial call',
      desc: '12 min · full transcript on device. Rep confirmed the appeal address and said a callback is expected with the reference number.',
      entities: [['denial — not medically necessary', 'disease'], ['$1,200.00', 'pii'], ['Dr. M. Patel', 'pii'], ['appeal window', 'pii']],
      links: [['Insurance', 'insurance'], ['Bills', 'bills']],
      tags: ['denial'],
    },
    {
      id: 'c2', kind: 'appointment', when: 'Sep 30 · 9:40', matter: 'Knee treatment',
      title: 'Dr. Patel — orthopedic follow-up',
      desc: 'Recorded with consent. Transcript marked: bring imaging CD, ask about PT vs. MRI.',
      entities: [['Dr. Maya Patel', 'pii'], ['physical therapy', 'procedure'], ['Sep 30', 'pii']],
      links: [['Appointments', 'appointments']],
    },
    {
      id: 'c3', kind: 'voicemail', when: 'Sep 22 · 15:20', matter: 'Annual screening',
      title: 'Riverside Imaging — results ready',
      desc: 'Transcribed on device. Results available; ask for the written report at pickup.',
      entities: [['Riverside Imaging', 'pii'], ['screening results', 'disease']],
      links: [['Documents', 'documents']],
    },
    {
      id: 'c4', kind: 'reminder', when: 'Oct 8', matter: 'MRI denial (Aetna)',
      title: 'Appeal window closes (computed)',
      desc: 'The letter states a 30-day window from the Sep 8 notice; the app computed Oct 8. Confirm the exact date with the insurer.',
      entities: [['30-day appeal window', 'pii'], ['Aetna', 'pii']],
      links: [['Insurance', 'insurance']],
      prov: ['inferred', 'computed from the letter'],
      tags: ['denial'],
    },
  ],

  KIND_LABEL: { call: 'Call', appointment: 'Appointment', voicemail: 'Voicemail', reminder: 'Reminder' },

  KIND_ICON: {
    call: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>',
    appointment: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    voicemail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="5.5" cy="11.5" r="4.5"/><circle cx="18.5" cy="11.5" r="4.5"/><line x1="5.5" y1="16" x2="18.5" y2="16"/></svg>',
    reminder: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 01-3.46 0"/></svg>',
  },

  _libFilter: 'all',
  _libQuery: '',

  renderLibrary() {
    const list = document.getElementById('lib-list');
    const timeline = document.getElementById('matter-timeline');
    if (!list) return;
    const q = this._libQuery.trim().toLowerCase();
    const items = this.CATALOG.filter(it =>
      (this._libFilter === 'all' || it.kind === this._libFilter) &&
      (!q || (it.title + ' ' + it.matter + ' ' + it.desc + ' ' + it.entities.map(e => e[0]).join(' ')).toLowerCase().includes(q))
    );
    if (!items.length) {
      list.innerHTML = `<div class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <p>Nothing matches that search.</p>
        <p class="empty-hint">Try a provider name, a medication, or clear the filters.</p>
      </div>`;
      if (timeline) timeline.hidden = true;
      return;
    }
    const hasDerived = this.CATALOG.some(it => it.prov && it.prov[0] !== 'extracted');
    const derivedNote = hasDerived
      ? `<p class="condition-confidence" style="margin-bottom:12px"><strong>Machine-derived items:</strong> anything marked INFERRED or UNVERIFIED was computed by the app, not quoted — confirm it before relying on it.</p>`
      : '';
    list.innerHTML = derivedNote + items.map(it => `<article class="cat-card" data-cat-id="${this.escapeHtml(it.id)}">
      <div class="cat-card-head">
        <span class="cat-kind ${this.escapeHtml(it.kind)}">${this.KIND_ICON[it.kind] || ''}</span>
        <span class="cat-title">${this.escapeHtml(it.title)}</span>
        ${it.prov ? this.provChip(it.prov[0], it.prov[1]) : ''}
        <span class="cat-when">${this.escapeHtml(it.when)}</span>
      </div>
      <p class="cat-desc">${this.escapeHtml(it.matter)} — ${this.escapeHtml(it.desc)}</p>
      <div class="cat-links">
        ${it.entities.map(e => `<span class="entity-chip ${this.safeEntityClass(e[1])}">${this.escapeHtml(e[0])}</span>`).join('')}
        ${it.links.map(l => `<button type="button" class="xref-chip" data-goto="${this.escapeHtml(l[1])}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
          ${this.escapeHtml(l[0])}
        </button>`).join('')}
        ${(it.tags || []).includes('denial') ? `<button type="button" class="xref-chip" data-action="appeal-from-library" data-cat-id="${this.escapeHtml(it.id)}">${this.escapeHtml(this.t('appeal.from_library'))}</button>` : ''}
        ${it.kind === 'call' ? `<button type="button" class="xref-chip xref-danger" data-action="recorder-delete" data-cat-id="${this.escapeHtml(it.id)}" aria-label="Delete ${this.escapeHtml(it.title)}">Delete</button>` : ''}
      </div>
    </article>`).join('');
    if (timeline) {
      timeline.hidden = false;
      const byMatter = {};
      for (const it of this.CATALOG) (byMatter[it.matter] = byMatter[it.matter] || []).push(it);
      const matter = Object.keys(byMatter).find(m => byMatter[m].length > 1) || Object.keys(byMatter)[0];
      timeline.innerHTML = `<h3>Matter timeline — ${this.escapeHtml(matter)}</h3>` + (byMatter[matter] || []).map(it => `
        <div class="tl-item kind-${this.escapeHtml(it.kind)}">
          <div class="tl-when">${this.escapeHtml(it.when)}</div>
          <div class="tl-title">${this.escapeHtml(it.title)}</div>
          <div class="tl-note">${this.KIND_LABEL[it.kind] || 'Item'} · ${this.escapeHtml(it.desc)}</div>
        </div>`).join('');
    }
  },

  deleteCatalogItem(id) {
    this.CATALOG = this.CATALOG.filter(it => it.id !== id);
    this.renderLibrary();
    this.renderRecentRecordings();
    this.toast('Deleted (demo — nothing was really stored).');
  },

  /* ── Directory (self-building provider cards, demo data) ── */

  DIRECTORY: [
    {
      id: 'p1', name: 'Dr. Maya Patel', klass: 'doctor', classLabel: 'Doctor · Orthopedics',
      sources: ['Appointment card (Sep 12)', 'Call transcript (Sep 24)', 'Bill decode (Aug 30)'],
      fields: [
        { k: 'Phone', v: '+1-555-010-7788', href: 'tel:+15550107788', prov: 'confirmed' },
        { k: 'Address', v: '410 Center St, Bldg C, Portland OR', prov: 'extracted', from: 'bill decode' },
        { k: 'Email', v: 'scheduling@patelortho.example', href: 'mailto:scheduling@patelortho.example', prov: 'inferred', from: 'pattern' },
      ],
    },
    {
      id: 'p2', name: 'Riverside Imaging', klass: 'imaging', classLabel: 'Imaging center',
      sources: ['Voicemail transcript (Sep 22)', 'Document decode (Sep 3)'],
      fields: [
        { k: 'Phone', v: '+1-555-022-8090', href: 'tel:+15550228090', prov: 'extracted', from: 'voicemail' },
        { k: 'Address', v: '88 River Rd, Portland OR', prov: 'extracted', from: 'document' },
        { k: 'Hours', v: 'Mon–Fri 7:00–19:00 · Sat 8:00–14:00', prov: 'inferred', from: 'voicemail' },
      ],
    },
    {
      id: 'p3', name: 'Aetna member services', klass: 'insurer', classLabel: 'Insurer',
      sources: ['Call transcript (Sep 24)'],
      fields: [
        { k: 'Phone', v: '+1-800-555-0142', href: 'tel:+18005550142', prov: 'extracted', from: 'call' },
        { k: 'Appeals fax', v: '+1-800-555-0177', href: 'tel:+18005550177', prov: 'inferred', from: 'letter' },
      ],
    },
    {
      id: 'p4', name: 'Corner Pharmacy', klass: 'pharmacy', classLabel: 'Pharmacy',
      sources: ['You confirmed every field'],
      fields: [
        { k: 'Phone', v: '+1-555-010-4432', href: 'tel:+15550104432', prov: 'confirmed' },
        { k: 'Address', v: '12 Alder Ave, Portland OR', prov: 'confirmed' },
        { k: 'Hours', v: 'Daily 8:00–21:00', prov: 'confirmed' },
      ],
    },
  ],

  _dirFilter: 'all',
  _dirQuery: '',

  renderDirectory() {
    const list = document.getElementById('dir-list');
    if (!list) return;
    const q = this._dirQuery.trim().toLowerCase();
    const contacts = this.DIRECTORY.filter(c =>
      (this._dirFilter === 'all' || c.klass === this._dirFilter) &&
      (!q || (c.name + ' ' + c.classLabel + ' ' + c.fields.map(f => f.v).join(' ')).toLowerCase().includes(q))
    );
    if (!contacts.length) {
      list.innerHTML = `<div class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>
        <p>No providers match.</p>
        <p class="empty-hint">The directory fills itself as you record calls and decode documents — or clear the filters.</p>
      </div>`;
      return;
    }
    const PROV_LABEL = { confirmed: 'you confirmed', extracted: 'from a call', inferred: 'inferred' };
    list.innerHTML = contacts.map(c => `<article class="contact-card">
      <div class="contact-head">
        <span class="contact-kind ${this.escapeHtml(c.klass)}" aria-hidden="true">${this.KIND_ICON.appointment}</span>
        <span class="contact-name">${this.escapeHtml(c.name)}</span>
        <span class="contact-class">${this.escapeHtml(c.classLabel)}</span>
      </div>
      <p class="contact-merge-note">Merged from ${c.sources.length === 1 ? 'one source' : c.sources.length + ' sources'}: ${c.sources.map(s => this.escapeHtml(s)).join(' · ')}</p>
      <div class="contact-fields">
        ${c.fields.map(f => `<div class="contact-field">
          <span class="k">${this.escapeHtml(f.k)}</span>
          <span class="v">${f.href ? `<a href="${this.escapeHtml(f.href)}">${this.escapeHtml(f.v)}</a>` : this.escapeHtml(f.v)}
          ${f.prov === 'confirmed' ? this.provChip('confirmed', PROV_LABEL.confirmed)
            : f.prov === 'extracted' ? this.provChip('extracted', f.from || PROV_LABEL.extracted)
            : this.provChip('inferred', (f.from ? 'inferred · ' + f.from : PROV_LABEL.inferred))}</span>
          <span class="row-actions">${f.prov !== 'confirmed' ? `<button type="button" class="xref-chip" data-action="dir-confirm-field" data-contact="${this.escapeHtml(c.id)}" data-field="${this.escapeHtml(f.k)}">Confirm</button>` : ''}</span>
        </div>`).join('')}
      </div>
      <div class="contact-actions">
        ${(c.fields.find(f => f.k === 'Phone') || {}).href ? `<a class="contact-action" href="${this.escapeHtml((c.fields.find(f => f.k === 'Phone') || {}).href)}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>
          Call</a>` : ''}
        <button type="button" class="xref-chip" data-goto="library">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>
          Items in Library
        </button>
      </div>
    </article>`).join('');
  },

  confirmDirectoryField(contactId, fieldKey) {
    const contact = this.DIRECTORY.find(c => c.id === contactId);
    const field = contact && contact.fields.find(f => f.k === fieldKey);
    if (!field) return;
    field.prov = 'confirmed';
    delete field.from;
    this.renderDirectory();
    this.toast('Confirmed — this now overrides anything the app inferred.');
  },

  /* ── Call Recorder (DEMO MODE — synthetic script, no audio) ── */

  _recState: 'idle',       /* idle | recording | summarized */
  _recElapsed: 0,          /* script seconds — the timer AND the turn schedule
                              run on the same clock, so displayed timestamps can
                              never disagree (round-1 vision finding) */
  _recRate: 3.5,           /* script seconds per real second (demo pacing) */
  _recTimerInt: null,
  _recTurnIdx: 0,

  REC_SCRIPT: [
    { t: '00:03', tSec: 3, who: 'you', text: 'Hi, I\'m calling about the denial letter for my knee MRI — reference A-2291.' },
    { t: '00:11', tSec: 11, who: 'other', text: 'Thank you. I see the denial was issued September 8th as not medically necessary.' },
    { t: '00:24', tSec: 24, who: 'you', text: 'My doctor documented six weeks of physical therapy first. That\'s in the records I submitted.' },
    { t: '00:39', tSec: 39, who: 'other', text: 'I do see the PT notes. You can file a first-level appeal within thirty days of the letter.' },
    { t: '00:58', tSec: 58, who: 'other', text: 'The appeal can be submitted by mail or fax, and we will acknowledge it in writing.' },
    { t: '01:10', tSec: 70, who: 'gap', text: '[inaudible] …reference number for the appeal…' },
    { t: '01:22', tSec: 82, who: 'you', text: 'Can you also send an itemized bill? The hospital total was one thousand two hundred dollars and I want to check it.' },
    { t: '01:41', tSec: 101, who: 'other', text: 'Certainly, the itemized statement will be mailed within five business days.' },
    { t: '01:55', tSec: 115, who: 'other', text: 'A case manager will call you back by Friday with the appeal reference number.' },
    { t: '02:06', tSec: 126, who: 'you', text: 'Thank you. I\'ll send the appeal with the therapy records this week.' },
  ],

  recorderStart() {
    if (this._recState === 'recording') return;
    this._recState = 'recording';
    this._recElapsed = 0;
    this._recTurnIdx = 0;
    const consent = document.getElementById('rec-consent');
    const live = document.getElementById('rec-live');
    const summary = document.getElementById('rec-summary');
    const recent = document.getElementById('rec-recent');
    const transcript = document.getElementById('rec-transcript');
    const wave = document.getElementById('rec-waveform');
    if (consent) consent.hidden = true;
    if (summary) summary.hidden = true;
    if (recent) recent.hidden = true;
    if (live) live.hidden = false;
    if (transcript) transcript.innerHTML = '';
    if (wave) {
      wave.innerHTML = '';
      for (let i = 0; i < 28; i++) {
        const bar = document.createElement('span');
        bar.style.animationDelay = (i % 7) * 0.09 + 's';
        bar.style.animationDuration = (0.8 + ((i * 37) % 9) / 12) + 's';
        bar.style.opacity = (0.35 + ((i * 53) % 10) / 16).toFixed(2);
        wave.appendChild(bar);
      }
    }
    document.body.classList.add('is-recording');
    const sticky = document.getElementById('rec-sticky');
    if (sticky) sticky.setAttribute('aria-hidden', 'false');
    const a = document.getElementById('rec-timer');
    if (a) a.textContent = '00:00';
    const b = document.getElementById('rec-sticky-timer');
    if (b) b.textContent = '00:00';
    this._recTimerInt = setInterval(() => {
      this._recElapsed += 0.1 * this._recRate;
      const t = this._fmtRecTime(this._recElapsed);
      if (a) a.textContent = t;
      if (b) b.textContent = t;
      /* turns appear exactly when the displayed clock passes their timestamp */
      while (this._recTurnIdx < this.REC_SCRIPT.length
             && this.REC_SCRIPT[this._recTurnIdx].tSec <= this._recElapsed) {
        this._recRenderTurn(this.REC_SCRIPT[this._recTurnIdx]);
        this._recTurnIdx += 1;
      }
      if (this._recTurnIdx >= this.REC_SCRIPT.length
          && this._recElapsed >= this.REC_SCRIPT[this.REC_SCRIPT.length - 1].tSec + 2) {
        this.recorderStop();
      }
    }, 100);
    this.toast('Demo recording started — synthetic script, no microphone is used.');
  },

  _fmtRecTime(s) {
    const total = Math.floor(s);
    const m = Math.floor(total / 60).toString().padStart(2, '0');
    const ss = (total % 60).toString().padStart(2, '0');
    return `${m}:${ss}`;
  },

  _recRenderTurn(turn) {
    const transcript = document.getElementById('rec-transcript');
    if (!transcript) return;
    /* interim draft first — visually distinct, never final */
    const row = document.createElement('div');
    row.className = `turn ${turn.who === 'you' ? 'you' : 'other'} interim`;
    row.innerHTML = `<span class="turn-time">${this.escapeHtml(turn.t)}</span>
      <span><span class="turn-speaker">${turn.who === 'you' ? 'You' : 'Insurer rep'}</span>
      <span class="turn-text">${this.escapeHtml(turn.text.slice(0, Math.max(8, Math.floor(turn.text.length * 0.6))))}…</span></span>`;
    transcript.appendChild(row);
    row.scrollIntoView({ block: 'end' });
    setTimeout(() => {
      row.classList.remove('interim');
      const txt = row.querySelector('.turn-text');
      if (txt) txt.textContent = turn.text;
      if (turn.who === 'gap') {
        row.classList.add('gap');
        const sp = row.querySelector('.turn-speaker');
        if (sp) sp.textContent = 'Unclear';
      }
    }, 700);
  },

  recorderStop() {
    if (this._recState !== 'recording') return;
    this._recState = 'summarized';
    clearInterval(this._recTimerInt);
    document.body.classList.remove('is-recording');
    const sticky = document.getElementById('rec-sticky');
    if (sticky) sticky.setAttribute('aria-hidden', 'true');
    const live = document.getElementById('rec-live');
    if (live) live.hidden = true;
    const recent = document.getElementById('rec-recent');
    if (recent) recent.hidden = false;
    this._renderRecSummary();
    const id = 'c9';
    if (!this.CATALOG.some(it => it.id === id)) {
      this.CATALOG.unshift({
        id, kind: 'call', when: 'Sep 24 · today', matter: 'MRI denial (Aetna)',
        title: 'Aetna — appeal call (demo recording)',
        desc: 'Recorded in demo mode. Synthetic transcript saved to the Library with analysis.',
        entities: [['appeal — 30 days', 'pii'], ['$1,200.00', 'pii'], ['itemized bill', 'pii']],
        links: [['Insurance', 'insurance'], ['Appointments', 'appointments']],
      });
    }
    this.renderRecentRecordings();
    this.toast('Saved to the Library (demo — synthetic only).');
  },

  _renderRecSummary() {
    const el = document.getElementById('rec-summary');
    if (!el) return;
    el.hidden = false;
    el.innerHTML = `
      <div class="result-section">
        <h3>Call summary <span class="demo-badge">Demo · synthetic</span></h3>
        <p class="result-text">You called Aetna about the knee MRI denial (ref A-2291). The rep confirmed a first-level appeal is possible within 30 days of the September 8 letter, and that an itemized bill will be mailed within five business days. A case manager will call back with the appeal reference number. Generated on this device from the demo transcript.</p>
      </div>
      <div class="result-section rec-summary-section">
        <h3>Commitments people made</h3>
        <div class="analysis-item"><span>“A case manager will call you back by Friday with the appeal reference number.”</span>${this.provChip('extracted', 'from transcript')}</div>
        <div class="analysis-item"><span>“The itemized statement will be mailed within five business days.”</span>${this.provChip('extracted', 'from transcript')}</div>
      </div>
      <div class="result-section rec-summary-section">
        <h3>Deadlines detected</h3>
        <div class="analysis-item"><span class="when">Oct 8</span><span>Appeal window closes — 30 days from the September 8 denial letter.</span>${this.provChip('extracted', 'from transcript')}</div>
        <div class="analysis-item unverified-row"><span class="when">no date</span><span>A second-level deadline was mentioned, but the rep\'s wording was unclear — no date could be read reliably from the audio.</span>${this.provChip('unverified', 'unverified')}</div>
        <div class="flag-item flag-danger needs-human-banner" role="alert" data-testid="unverified-deadline">
          <p><strong>This needs a human decision.</strong></p>
          <p>The unverified deadline is not shown as certain anywhere. Confirm the second-level deadline in writing with Aetna before relying on it.</p>
        </div>
      </div>
      <div class="result-section rec-summary-section">
        <h3>Suggested actions</h3>
        <div class="analysis-item"><span>Send the appeal with the six weeks of therapy records this week.</span>${this.provChip('inferred', 'model-inferred')}</div>
        <div class="analysis-item"><span>Check the itemized bill against the $1,200 total when it arrives.</span>${this.provChip('inferred', 'model-inferred')}</div>
      </div>
      <div class="result-section rec-summary-section">
        <h3>Use this call</h3>
        <div class="cat-links">
          <button type="button" class="btn-secondary" data-action="recorder-feed-appt">Prepare for the callback</button>
          <button type="button" class="btn-secondary" data-action="recorder-feed-doc">Decode as document</button>
          <button type="button" class="btn-secondary" data-goto="library">Open in Library</button>
        </div>
      </div>`;
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    this.focusInto(el);
  },

  renderRecentRecordings() {
    const el = document.getElementById('rec-recent');
    if (!el) return;
    const calls = this.CATALOG.filter(it => it.kind === 'call');
    el.hidden = calls.length === 0;
    el.innerHTML = `<div class="result-section rec-summary-section">
      <h3>Your recordings (demo)</h3>
      ${calls.map(it => `<div class="analysis-item">
        <span>${this.escapeHtml(it.title)} — ${this.escapeHtml(it.when)}</span>
        <span style="display:flex;gap:8px;flex-wrap:wrap">
          <button type="button" class="btn-ghost btn-sm" data-goto="library">Library</button>
          <button type="button" class="btn-danger btn-sm" data-action="recorder-delete" data-cat-id="${this.escapeHtml(it.id)}">Delete</button>
        </span>
      </div>`).join('')}
      <div class="analysis-item">
        <span>Start over with the synthetic call script.</span>
        <button type="button" class="btn-ghost btn-sm" data-action="recorder-reset">Replay the demo call</button>
      </div>
    </div>`;
  },

  recorderFeedAppt() {
    const input = document.getElementById('appt-symptoms');
    if (input && !input.value.trim()) {
      input.value = 'Callback expected from Aetna case manager about MRI appeal reference A-2291; appointment with Dr. Patel Sep 30.';
    }
    this.showView('appointments');
  },

  recorderFeedDoc() {
    const input = document.getElementById('doc-input');
    if (input && !input.value.trim()) {
      input.value = 'Denial letter (dictated from the call): MRI of right knee denied as not medically necessary on Sep 8; first-level appeal must be filed within 30 days; PT notes for six weeks submitted; itemized bill to follow.';
    }
    this.showView('documents');
  },

  recorderReset() {
    if (this._recState === 'recording') this.recorderStop();
    this._recState = 'idle';
    this._recTurnIdx = 0;
    const consent = document.getElementById('rec-consent');
    const live = document.getElementById('rec-live');
    const summary = document.getElementById('rec-summary');
    if (consent) consent.hidden = false;
    if (live) live.hidden = true;
    if (summary) summary.hidden = true;
    const check = document.getElementById('rec-consent-check');
    if (check) check.checked = false;
    const start = document.getElementById('rec-start');
    if (start) start.disabled = true;
  },

  openDeleteDialog(catId) {
    const dlg = document.getElementById('rec-delete-dialog');
    if (!dlg) { this.deleteCatalogItem(catId); return; }
    dlg.dataset.catId = catId;
    if (typeof dlg.showModal === 'function') dlg.showModal();
    else this.deleteCatalogItem(catId);
  },
};

/* ── Initialize ── */

document.addEventListener('DOMContentLoaded', () => {
  /* input modality tracking (drives focusInto) */
  document.addEventListener('keydown', () => { HA._modality = 'keyboard'; }, true);
  document.addEventListener('mousedown', () => { HA._modality = 'pointer'; }, true);
  document.addEventListener('touchstart', () => { HA._modality = 'pointer'; }, true);

  /* the mobile scroll hint points at the shelf, then leaves when you arrive */
  const navEl = document.getElementById('main-nav');
  const hint = document.getElementById('nav-scroll-hint');
  if (navEl && hint) {
    const update = () => { hint.style.opacity = (navEl.scrollLeft + navEl.clientWidth >= navEl.scrollWidth - 8) ? '0' : ''; };
    navEl.addEventListener('scroll', update, { passive: true });
    update();
  }

  /* the More disclosure: the reference shelf stays out of the way until asked */
  const navMore = document.getElementById('nav-more');
  const navRow = document.getElementById('nav-more-row');
  if (navMore && navRow) {
    navMore.addEventListener('click', () => {
      const open = navRow.hidden;
      navRow.hidden = !open;
      navMore.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !navRow.hidden) {
        navRow.hidden = true;
        navMore.setAttribute('aria-expanded', 'false');
        navMore.focus();
      }
    });
  }

  HA.initTheme();
  HA.loadDashStrip();
  HA.renderReminders();
  HA.renderHomeLibrary();
  HA.renderDirectory();
  HA.renderRecentRecordings();

  /* Scroll reveal for home view elements */
  HA.initScrollReveal();

  /* bfcache restore: never leave content hidden as pending */
  window.addEventListener('pageshow', () => {
    document.querySelectorAll('.reveal[data-reveal="pending"]').forEach(el => {
      if (el.getBoundingClientRect().top <= window.innerHeight) el.setAttribute('data-reveal', 'revealed');
    });
  });

  /* PWA: offline shell for static assets ONLY. /api/* is never cached —
     no patient data in the service worker, by law. */
  if ('serviceWorker' in navigator
      && (location.protocol === 'https:' || ['localhost', '127.0.0.1'].includes(location.hostname))) {
    navigator.serviceWorker.register('/sw.js').catch(() => { /* offline shell is optional */ });
  }

  /* Navigation */
  document.getElementById('main-nav').addEventListener('click', (e) => {
    if (!e.target.classList.contains('nav-btn')) return;
    HA.showView(e.target.dataset.view);
  });

  document.getElementById('btn-home').addEventListener('click', () => HA.showView('home'));
  document.getElementById('btn-theme').addEventListener('click', () => HA.toggleTheme());

  /* Bilingual frame: bind static strings, then re-render dynamic views
     when the language changes (their templates build with HA.t) */
  if (HA.i18n) {
    HA.i18n.init();
    document.addEventListener('ha:lang', () => {
      const active = document.querySelector('.view.active');
      if (active) HA.showView(active.id.replace('view-', ''));
    });
  }

  /* Color themes: four plush palettes, per-person, both light and dark */
  const palRow = document.querySelector('.pal-row');
  if (palRow) {
    const applyPal = (v, focus) => {
      if (v) document.documentElement.setAttribute('data-palette', v);
      else document.documentElement.removeAttribute('data-palette');
      localStorage.setItem('ha-palette', v);
      palRow.querySelectorAll('.pal-swatch').forEach(b => {
        const on = b.dataset.palette === v;
        b.classList.toggle('on', on);
        b.setAttribute('aria-checked', String(on));
        if (focus && on) b.focus();
      });
    };
    applyPal(localStorage.getItem('ha-palette') || '');
    palRow.addEventListener('click', (e) => {
      const b = e.target.closest('.pal-swatch');
      if (b) applyPal(b.dataset.palette);
    });
    /* radios navigate by arrow keys (WAI-ARIA radiogroup pattern) */
    palRow.addEventListener('keydown', (e) => {
      const swatches = [...palRow.querySelectorAll('.pal-swatch')];
      const i = swatches.indexOf(document.activeElement);
      if (i < 0) return;
      let next = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') next = swatches[(i + 1) % swatches.length];
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') next = swatches[(i - 1 + swatches.length) % swatches.length];
      if (next) { e.preventDefault(); applyPal(next.dataset.palette, true); }
    });
  }

  /* Example chips: tap one to start the intake sheet with that sentence */
  document.addEventListener('click', (e) => {
    const chip = e.target.closest('.example-chip');
    if (!chip) return;
    const ta = document.getElementById('symptom-input');
    if (ta) { ta.value = chip.dataset.example; ta.focus(); }
  });

  /* Entry card clicks (cards that are themselves controls; the featured
     first card delegates to its CTA button instead) */
  document.querySelectorAll('.entry-card[data-goto]').forEach(card => {
    const go = () => HA.showView(card.dataset.goto);
    card.addEventListener('click', go);
    card.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
  });

  /* Consent checkbox gates the demo recorder */
  const consentCheck = document.getElementById('rec-consent-check');
  if (consentCheck) {
    consentCheck.addEventListener('change', () => {
      const start = document.getElementById('rec-start');
      if (start) start.disabled = !consentCheck.checked;
    });
  }

  /* Library + Directory search */
  const libSearch = document.getElementById('lib-search');
  if (libSearch) libSearch.addEventListener('input', () => { HA._libQuery = libSearch.value; HA.renderLibrary(); });
  const dirSearch = document.getElementById('dir-search');
  if (dirSearch) dirSearch.addEventListener('input', () => { HA._dirQuery = dirSearch.value; HA.renderDirectory(); });

  /* Delegated click handler for app actions. */
  document.addEventListener('click', (e) => {
    /* generic in-app navigation (entry cards, xref chips, reminders) */
    const gotoEl = e.target.closest('[data-goto]');
    if (gotoEl && !gotoEl.classList.contains('entry-card')) {
      HA.showView(gotoEl.dataset.goto);
      return;
    }
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;
    const buttonEvent = { currentTarget: btn };
    if (action === 'assess-symptoms') {
      HA.assessSymptoms(buttonEvent);
    } else if (action === 'decode-document') {
      HA.decodeDocument(buttonEvent);
    } else if (action === 'decode-bill') {
      HA.decodeBill(buttonEvent);
    } else if (action === 'fight-denial') {
      HA.fightDenial(buttonEvent);
    } else if (action === 'generate-appeal-letter') {
      HA.generateAppealLetter(buttonEvent);
    } else if (action === 'appeal-letter-download') {
      HA.downloadAppealLetter();
    } else if (action === 'appeal-letter-print') {
      HA.printAppealLetter();
    } else if (action === 'share-safe-run') {
      HA.shareSafe(buttonEvent);
    } else if (action === 'share-safe-copy') {
      const t = document.getElementById('share-safe-out');
      if (t) { t.select(); document.execCommand('copy'); t.setSelectionRange(0, 0); }
    } else if (action === 'share-safe-download') {
      const t = document.getElementById('share-safe-out');
      if (t) { const a = document.createElement('a');
        a.href = URL.createObjectURL(new Blob([t.value], { type: 'text/plain' }));
        a.download = 'share-safe.txt'; a.click(); URL.revokeObjectURL(a.href); }
    } else if (action === 'share-safe-back') {
      HA.decodeDocument(buttonEvent);
    } else if (action === 'appeal-from-bill') {
      HA.appealFromBill();
    } else if (action === 'appeal-from-library') {
      const item = HA.CATALOG.find(it => it.id === btn.dataset.catId);
      if (item) HA.appealFromLibrary(item);
    } else if (action === 'check-drug') {
      HA.checkDrug(buttonEvent);
    } else if (action === 'prepare-appointment') {
      HA.prepareAppointment(buttonEvent);
    } else if (action === 'translate-discharge') {
      HA.translateDischarge(buttonEvent);
    } else if (action === 'create-second-opinion') {
      HA.createSecondOpinion(buttonEvent);
    } else if (action === 'scan-community') {
      HA.scanCommunity(buttonEvent);
    } else if (action === 'create-family-profile') {
      HA.createFamilyProfile(buttonEvent);
    } else if (action === 'create-track') {
      HA.createTrack(buttonEvent);
    } else if (action === 'coverage-create') {
      HA.createCoverageCase(buttonEvent);
    } else if (action === 'coverage-focus-primary') {
      HA.setCoverageStatus('Focus on the primary next action above. Secondary details stay collapsed.');
      document.getElementById('coverage-primary-action')?.focus?.();
    } else if (action === 'coverage-script') {
      HA.loadCoverageScript(btn.dataset.script || 'county');
    } else if (action === 'coverage-gate') {
      HA.checkCoverageGate();
    } else if (action === 'add-condition') {
      const profileId = btn.dataset.profileId;
      if (profileId) HA.addCondition(profileId);
    } else if (action === 'update-track') {
      const trackId = btn.dataset.trackId;
      const status = btn.dataset.status;
      if (trackId && status) HA.updateTrackStatus(trackId, status);
    } else if (action === 'recorder-start') {
      HA.recorderStart();
    } else if (action === 'recorder-stop') {
      HA.recorderStop();
    } else if (action === 'recorder-feed-appt') {
      HA.recorderFeedAppt();
    } else if (action === 'recorder-feed-doc') {
      HA.recorderFeedDoc();
    } else if (action === 'recorder-delete') {
      const catId = btn.dataset.catId;
      if (catId) HA.openDeleteDialog(catId);
    } else if (action === 'recorder-delete-confirm') {
      const dlg = document.getElementById('rec-delete-dialog');
      const catId = dlg && dlg.dataset.catId;
      if (dlg && typeof dlg.close === 'function') dlg.close();
      if (catId) HA.deleteCatalogItem(catId);
    } else if (action === 'recorder-delete-cancel') {
      const dlg = document.getElementById('rec-delete-dialog');
      if (dlg && typeof dlg.close === 'function') dlg.close();
    } else if (action === 'recorder-reset') {
      HA.recorderReset();
    } else if (action === 'dir-confirm-field') {
      HA.confirmDirectoryField(btn.dataset.contact, btn.dataset.field);
    }
  });

  /* Library + Directory filter chips (aria-pressed group) */
  document.addEventListener('click', (e) => {
    const libChip = e.target.closest('[data-lib-filter]');
    if (libChip) {
      document.querySelectorAll('[data-lib-filter]').forEach(c => c.setAttribute('aria-pressed', String(c === libChip)));
      HA._libFilter = libChip.dataset.libFilter;
      HA.renderLibrary();
      return;
    }
    const dirChip = e.target.closest('[data-dir-filter]');
    if (dirChip) {
      document.querySelectorAll('[data-dir-filter]').forEach(c => c.setAttribute('aria-pressed', String(c === dirChip)));
      HA._dirFilter = dirChip.dataset.dirFilter;
      HA.renderDirectory();
    }
  });
});
