// Hemingway — apply a JSON pattern to text and surface a conformant rewrite + grade.

(function () {
  const cfg = window.HEMINGWAY_CONFIG;
  const libraryCache = {};

  const els = {
    librarySelect: document.getElementById("library-select"),
    patternHint: document.getElementById("pattern-hint"),
    input: document.getElementById("input-text"),
    rewriteBtn: document.getElementById("rewrite-btn"),
    status: document.getElementById("status"),
    outputArea: document.getElementById("output-area"),
    rewriteOutput: document.getElementById("rewrite-output"),
    gradeOutput: document.getElementById("grade-output"),
    libraryCount: document.getElementById("library-count"),
  };

  // --- Library loading -----------------------------------------------------

  async function loadPattern(name) {
    if (libraryCache[name]) return libraryCache[name];
    const res = await fetch(`library/${name}.json`);
    if (!res.ok) throw new Error(`Failed to load pattern: ${name}`);
    const data = await res.json();
    libraryCache[name] = data;
    return data;
  }

  function describePattern(pattern) {
    const scope = pattern.scope && pattern.scope.applies_to;
    return scope ? scope : pattern.standard || "";
  }

  // --- Client-side grader --------------------------------------------------
  // Mechanical checks only. LLM-judgment checks (BLUF, role-awareness, etc.)
  // come from the server-side rewrite response when MODE === "api".

  function gradeMechanical(text, pattern) {
    const checks = [];

    // Sentence count
    const max = (pattern.constraints && pattern.constraints.max_sentences) || 5;
    const sentenceCount = (text.match(/[.!?]+(\s|$)/g) || []).length;
    checks.push({
      label: `Under ${max} sentences (${sentenceCount} detected)`,
      pass: sentenceCount > 0 && sentenceCount <= max,
    });

    // Link presence — required if pattern declares action/reminder semantics.
    const hasMarkdownLink = /\[[^\]]+\]\([^)]+\)/.test(text);
    const hasRawUrl = /https?:\/\/\S+/.test(text);
    checks.push({
      label: "Contains a link (required for action/reminder types)",
      pass: hasMarkdownLink || hasRawUrl,
    });

    // Em-dash aside test — one of the explicit rules in the notifications pattern.
    if ((pattern.rules || []).some((r) => /em dash/i.test(r))) {
      const hasEmDashAside = /\s—\s|\s–\s/.test(text);
      checks.push({
        label: "No mid-sentence em-dash asides",
        pass: !hasEmDashAside,
      });
    }

    // Subject-line length, if a separate subject field is implied (skipped for v0
    // since the textarea is body-only). Surface as informational.

    return checks;
  }

  function renderGrade(checks, serverNotes) {
    els.gradeOutput.innerHTML = "";
    checks.forEach((c) => {
      const li = document.createElement("li");
      const mark = document.createElement("span");
      mark.className = c.pass ? "pass-mark" : "fail-mark";
      mark.textContent = c.pass ? "✓" : "✗";
      const label = document.createElement("span");
      label.textContent = c.label;
      li.appendChild(mark);
      li.appendChild(label);
      els.gradeOutput.appendChild(li);
    });
    if (serverNotes && serverNotes.length) {
      const sep = document.createElement("li");
      sep.style.marginTop = "0.75rem";
      sep.style.color = "var(--text-soft)";
      sep.style.fontStyle = "italic";
      sep.textContent = "Server notes:";
      els.gradeOutput.appendChild(sep);
      serverNotes.forEach((note) => {
        const li = document.createElement("li");
        const mark = document.createElement("span");
        mark.className = "pass-mark";
        mark.textContent = "•";
        const label = document.createElement("span");
        label.textContent = note;
        li.appendChild(mark);
        li.appendChild(label);
        els.gradeOutput.appendChild(li);
      });
    }
  }

  // --- Rewrite -------------------------------------------------------------

  async function rewrite(input, libraryName, pattern) {
    if (cfg.MODE === "api" && cfg.API_ENDPOINT) {
      const res = await fetch(cfg.API_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ library: libraryName, pattern, input }),
      });
      if (!res.ok) {
        const body = await res.text();
        throw new Error(`API ${res.status}: ${body}`);
      }
      return await res.json();
    }
    // Mock mode — no LLM call. Returns a placeholder that looks shaped like
    // a conformant notification so the UI is usable while the API is being set up.
    return {
      rewrite:
        "[MOCK] Complete your open reviews at your [certifications page](https://www.internalfb.com/certifications) by May 30. " +
        "Late submissions delay your team's certification and trigger sub-certifier escalation.",
      notes: [
        "MOCK mode: real LLM call not configured. Set API_ENDPOINT in config.js and switch MODE to \"api\".",
        "Original input length: " + input.length + " chars.",
      ],
    };
  }

  // --- Wire up -------------------------------------------------------------

  function setStatus(msg) {
    els.status.textContent = msg || "";
  }

  async function refreshPatternHint() {
    const name = els.librarySelect.value;
    try {
      const pattern = await loadPattern(name);
      els.patternHint.textContent = describePattern(pattern);
    } catch (e) {
      els.patternHint.textContent = `(failed to load: ${e.message})`;
    }
  }

  async function onRewriteClick() {
    const input = els.input.value.trim();
    if (!input) {
      setStatus("Enter a draft or brief first.");
      return;
    }
    const name = els.librarySelect.value;
    els.rewriteBtn.disabled = true;
    setStatus(cfg.MODE === "api" ? "Calling rewrite API..." : "Generating mock rewrite...");
    try {
      const pattern = await loadPattern(name);
      const result = await rewrite(input, name, pattern);
      els.rewriteOutput.textContent = result.rewrite || "(no rewrite returned)";
      const checks = gradeMechanical(result.rewrite || "", pattern);
      renderGrade(checks, result.notes || []);
      els.outputArea.hidden = false;
      setStatus("");
    } catch (e) {
      setStatus("Error: " + e.message);
    } finally {
      els.rewriteBtn.disabled = false;
    }
  }

  function init() {
    if (cfg.LIBRARY_ENTRIES) {
      els.libraryCount.textContent = cfg.LIBRARY_ENTRIES.length;
    }
    els.librarySelect.addEventListener("change", refreshPatternHint);
    els.rewriteBtn.addEventListener("click", onRewriteClick);
    refreshPatternHint();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
