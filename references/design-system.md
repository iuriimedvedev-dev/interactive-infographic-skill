# Nord Design System Reference

A reusable dark/light design system based on the Nord palette. This guide provides actionable implementation guidance with illustrative CSS, HTML, and JavaScript examples. All examples are internally consistent and intended to be copied into a project as a starting point.

---

## Core Colors

The Nord palette defines seven core colors used throughout the system.

| Role | Token | Description |
|------|-------|-------------|
| Polar Night 1 | `#2E3440` | Background base |
| Polar Night 2 | `#3B4252` | Surface elevation |
| Frost Blue | `#88C0D0` | Primary accent |
| Frost Green | `#A3BE8C` | Success state |
| Frost Yellow | `#EBCB8B` | Warning state |
| Frost Red | `#BF616A` | Error/danger state |
| Frost Purple | `#B48EAD` | Tertiary accent |

---

## CSS Custom Properties

### Dark Theme (Default)

The dark theme is the document default. Apply it at the `:root` level so every element inherits the values.

```css
:root {
  /* --- Core palette --- */
  --nord-polar-night-1: #2E3440;
  --nord-polar-night-2: #3B4252;
  --nord-frost-blue: #88C0D0;
  --nord-frost-green: #A3BE8C;
  --nord-frost-yellow: #EBCB8B;
  --nord-frost-red: #BF616A;
  --nord-frost-purple: #B48EAD;

  /* --- Semantic surfaces --- */
  --surface-base: var(--nord-polar-night-1);
  --surface-raised: var(--nord-polar-night-2);
  --surface-overlay: rgba(46, 52, 64, 0.85);

  /* --- Semantic text --- */
  --text-primary: #ECEFF4;
  --text-secondary: #D8DEE9;
  --text-muted: #4C566A;
  --text-inverse: var(--nord-polar-night-1);

  /* --- Semantic borders --- */
  --border-default: var(--nord-polar-night-2);
  --border-strong: #4C566A;
  --border-focus: var(--nord-frost-blue);

  /* --- Semantic accents --- */
  --accent-primary: var(--nord-frost-blue);
  --accent-secondary: var(--nord-frost-purple);
  --accent-tertiary: var(--nord-frost-green);

  /* --- Semantic states --- */
  --state-success: var(--nord-frost-green);
  --state-warning: var(--nord-frost-yellow);
  --state-error: var(--nord-frost-red);
  --state-info: var(--nord-frost-blue);

  /* --- Typography --- */
  --font-family: system-ui, sans-serif;
  --font-mono: monospace;
  --text-base: 1rem;
  --text-sm: 0.875rem;
  --text-lg: 1.125rem;
  --text-xl: 1.5rem;

  /* --- Spacing --- */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;

  /* --- Border radius --- */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;

  /* --- Transitions --- */
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
}
```

### Light Theme Override

The light theme is activated by the attribute `data-theme="light"` on the `<html>` element. Only values that differ from the dark default need to be overridden.

```css
[data-theme="light"] {
  --surface-base: #ECEFF4;
  --surface-raised: #FFFFFF;
  --surface-overlay: rgba(236, 239, 244, 0.85);

  --text-primary: #2E3440;
  --text-secondary: #3B4252;
  --text-muted: #4C566A;
  --text-inverse: #ECEFF4;

  --border-default: #D8DEE9;
  --border-strong: #4C566A;
  --border-focus: #2E3440;

  --accent-primary: #345879;
  --accent-secondary: #B48EAD;
  --accent-tertiary: #A3BE8C;
}
```

### Contrast-Aware Usage

- **Text on `--surface-base`**: Use `--text-primary` for body copy and `--text-secondary` for captions and subtitles (`.cell-sub`). Both meet WCAG AA 4.5:1 against their respective surface in dark and light themes.
- **Text on accent backgrounds**: Use `--text-primary` for text on lightly tinted pill backgrounds in both themes. For the red pill specifically, `--text-primary` provides sufficient contrast in both dark and light themes. Do not assume a single hardcoded dark tint works on every state color.
- **Muted text**: `--text-muted` is intended for decorative or disabled states only. Do not use it for required reading content or meaningful diagrams.
- **Focus indicators**: All `:focus-visible` outlines must meet WCAG AA 3:1 contrast against the adjacent surface. The light theme uses `--border-focus: #2E3440` and the dark theme uses `--border-focus: #88C0D0` to satisfy this requirement against their respective surfaces.
- **Text color requirements**: Require 4.5:1 for normal text and 3:1 for focus indicators against adjacent colors.
- **Verification**: Run automated contrast checks during CI to catch regressions when tokens change.

### Theme Persistence

Store the user's theme preference in `localStorage`. Default to dark. Always guard `localStorage` access (some browsers block it in private mode) and only accept valid theme values.

```html
<script>
(function () {
  var storageKey = "nord-theme";
  var theme = "dark";

  try {
    var stored = localStorage.getItem(storageKey);
    if (stored === "dark" || stored === "light") {
      theme = stored;
    }
  } catch (e) {
    // localStorage unavailable (e.g., private browsing)
  }

  if (theme !== "dark") {
    document.documentElement.setAttribute("data-theme", theme);
  }
})();
</script>
```

Toggle function for a theme switch control:

```html
<script>
function toggleTheme() {
  var current = document.documentElement.getAttribute("data-theme");
  var next = current === "light" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", next);
  try {
    localStorage.setItem("nord-theme", next);
  } catch (e) {
    // localStorage unavailable
  }
}
</script>
```

Tradeoff: Reading `localStorage` synchronously before the page paints avoids a flash of wrong theme. The cost is a minimal blocking script in the `<head>`. For projects that cannot place inline scripts due to CSP, a same-origin synchronous external script in the `<head>` can read `localStorage` and set `data-theme` before render, preventing flash without requiring `unsafe-inline`.

---

## Icons

Icons are monochrome FontAwesome 6 `fa-solid` icons implemented as self-contained inline SVG. No externally hosted fonts, icon libraries, or links are permitted. Never use emoji anywhere in the interface.

### Implementation Pattern

Each icon is an inline `<svg>` with `role="img"` and an accessible label. The SVG uses `currentColor` so it inherits the surrounding text color.

```html
<!-- fa-solid: check -->
<svg class="icon icon-check" role="img" aria-label="Check"
     viewBox="0 0 448 512" width="1em" height="1em">
  <path fill="currentColor"
        d="M438.6 105.4c12.5 12.5 12.5 32.8 0 45.3l-224 224c-12.5 12.5-32.8 12.5-45.3 0l-96-96c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L192 306.7 393.4 105.4c12.5-12.5 32.8-12.5 45.3 0z"/>
</svg>
```

Reuse this icon where a check mark is needed. For other icons, use text-only labeled buttons or substitute the correct FontAwesome 6 `fa-solid` path data.

### Accessibility Guidance

- Every decorative icon wrapped in a button or link must have `aria-hidden="true"` on the `<svg>` and a visible or `aria-label` text alternative on the parent.
- Standalone icons that convey meaning must carry `role="img"` and `aria-label` directly on the `<svg>`.
- Size icons with `width` and `height` set to `1em` so they scale with the parent font size.
- Do not rely on color alone to convey icon meaning; pair with text labels where possible.

### Sizing Classes

```css
.icon-sm { width: 0.875em; height: 0.875em; }
.icon-md { width: 1em; height: 1em; }
.icon-lg { width: 1.25em; height: 1.25em; }
.icon-xl { width: 1.5em; height: 1.5em; }
```

---

## Grid Layouts

Three grid classes are defined for card-based layouts. All use equal-height flex cards and a no-orphan-row strategy.

### Grid Definitions

```css
.metric-grid,
.interactive-grid,
.nord-card-grid {
  display: grid;
  gap: var(--space-lg);
  grid-template-columns: repeat(3, minmax(0, 1fr));
}
```

The `minmax(0, 1fr)` pattern prevents columns from overflowing their container when content is inflexible (e.g., long unbreakable text). The `0` lower bound allows the column to shrink below its minimum content size, relying on the overflow handling inside each card.

### Equal-Height Flex Cards

Each card inside the grid uses flexbox to distribute space and push footers to the bottom.

```css
.nord-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: var(--surface-raised);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  min-width: 0;
  overflow-wrap: anywhere;
}

.nord-card__body {
  flex: 1 1 auto;
}

.nord-card__footer {
  flex: 0 0 auto;
  margin-top: var(--space-md);
}
```

The `min-width: 0` on the card allows the flex child to shrink below its minimum content size, preventing grid columns from overflowing. The `overflow-wrap: anywhere` ensures long unbreakable text wraps within the card instead of being clipped.

### No-Orphan-Row Strategy

An orphan row occurs when the last row of a grid contains fewer cards than columns, leaving empty space. On desktop the grid always uses exactly 3 columns (`repeat(3, minmax(0, 1fr))`). Never change the desktop column count with JavaScript.

**Content contract**: Prefer groups of three real cards, including the three-card hero. A lone final card can span the full row. Do not invent, duplicate, or hide content to fill a row. The supplied template switches directly to one column on narrow screens.

```css
@media (max-width: 900px) {
  .metric-grid,
  .interactive-grid,
  .nord-card-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 560px) {
  .metric-grid,
  .interactive-grid,
  .nord-card-grid {
    grid-template-columns: 1fr;
  }
}
```

If adopting the optional two-column breakpoint shown above, arrange complete rows or span a lone final card. At one column every card occupies a full row by definition.

**Example layout pattern**:

```html
<!-- Strict grid: contains only complete rows (6n cards for 3-col and 2-col) -->
<div class="nord-card-grid">
  <div class="nord-card">Card 1</div>
  <div class="nord-card">Card 2</div>
  <div class="nord-card">Card 3</div>
  <div class="nord-card">Card 4</div>
  <div class="nord-card">Card 5</div>
  <div class="nord-card">Card 6</div>
</div>

<!-- Remainder items as a labeled ordered list (when total is not 6n) -->
<section aria-label="Additional items">
  <ol>
    <li>Card 7</li>
    <li>Card 8</li>
  </ol>
</section>
```

### Accessible Narrower Responsive Layouts

At narrow widths, the grid collapses to a single column. Ensure that:

- Card content remains readable without horizontal scroll.
- Touch targets inside cards are at least 44x44 CSS pixels.
- The `gap` value is sufficient to separate cards on small screens (at least `var(--space-md)`).

---

## Zero Bullet Lists — Colored Nord Mini-Cards

Bullet lists (`<ul><li>...</li></ul>`) are strictly forbidden in content cards, sections, and modals. Unstyled or generic bullet points degrade visual hierarchy, look unfinished, and break responsive scannability.

Instead, all multi-point items must be rendered as colored Nord mini-cards (`.nord-mini-card` with border modifiers `border-green`, `border-blue`, `border-yellow`, `border-purple`, `border-orange`, `border-red`) inside `.nord-card-grid` (for multi-column layouts) or `.card-mini-stack` (for vertical callout stacks).

### CSS Rules

```css
.card-mini-stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm, 10px);
  margin-top: var(--space-md, 14px);
}

.nord-mini-card {
  padding: 12px 16px;
  border: 1px solid var(--border-default, var(--border));
  border-left: 4px solid var(--accent-primary, var(--accent));
  border-radius: 8px;
  background: var(--surface-raised, var(--surface-soft));
  font-size: 13px;
  color: var(--text-primary, var(--text));
}

.nord-mini-card p {
  margin: 0;
  color: var(--text-primary, var(--text));
  font-size: 13px;
}

.nord-mini-card.border-green  { border-left-color: var(--state-success, var(--green, #a3be8c)); }
.nord-mini-card.border-blue   { border-left-color: var(--accent-primary, var(--accent, #88c0d0)); }
.nord-mini-card.border-yellow { border-left-color: var(--state-warning, var(--amber, #ebcb8b)); }
.nord-mini-card.border-purple { border-left-color: var(--accent-secondary, var(--nord-purple, #b48ead)); }
.nord-mini-card.border-orange { border-left-color: #d08770; }
.nord-mini-card.border-red    { border-left-color: var(--state-error, var(--nord-red, #bf616a)); }
```

### HTML Structure

```html
<!-- Vertical stack of multi-point items -->
<div class="card-mini-stack">
  <div class="nord-mini-card border-blue">
    <p>Describe the intent before the mechanics.</p>
  </div>
  <div class="nord-mini-card border-green">
    <p>Make the current state visible.</p>
  </div>
  <div class="nord-mini-card border-purple">
    <p>Revisit assumptions as you learn.</p>
  </div>
</div>
```

In tables of contents (`#tocSidebar`), navigation links must be rendered directly inside `<nav id="tocSidebar"><div class="toc-list"><a class="toc-link" ...></div></nav>` without `<ul>` or `<li>` tags.

---

## Responsive Sidebar

The sidebar provides a table of contents with scroll-spy highlighting, keyboard accessibility, and persistent state. On narrow screens it overlays the content with a backdrop; on wider screens it can remain permanently visible.

### HTML Structure

```html
<button id="tocToggle" type="button" aria-expanded="false"
        aria-controls="tocSidebar">
  Table of contents
</button>

<nav id="tocSidebar" aria-label="Table of contents" hidden>
  <div class="toc-list">
    <a href="#core-colors" class="toc-link">Core Colors</a>
    <a href="#css-custom-properties" class="toc-link">CSS Custom Properties</a>
    <a href="#icons" class="toc-link">Icons</a>
    <a href="#grid-layouts" class="toc-link">Grid Layouts</a>
  </div>
</nav>

<div id="tocBackdrop" hidden></div>
```

The `hidden` attribute on both sidebar and backdrop removes them from the accessibility tree and from layout when closed. The toggle button uses visible text as its accessible name, paired with `aria-expanded` to convey state.

### Sidebar Styles

```css
#tocSidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 280px;
  height: 100vh;
  background: var(--surface-raised);
  border-right: 1px solid var(--border-default);
  padding: var(--space-xl) var(--space-lg);
  overflow-y: auto;
  z-index: 1000;
}

#tocSidebar[hidden] {
  display: none;
}

#tocSidebar a {
  display: block;
  padding: var(--space-sm) 0;
  color: var(--text-secondary);
  text-decoration: none;
  border-left: 2px solid transparent;
  padding-left: var(--space-md);
}

#tocSidebar a:hover,
#tocSidebar a:focus-visible {
  color: var(--accent-primary);
}

#tocSidebar a[aria-current="true"] {
  color: var(--accent-primary);
  border-left-color: var(--accent-primary);
  font-weight: 600;
}

#tocBackdrop {
  position: fixed;
  inset: 0;
  background: var(--surface-overlay);
  z-index: 999;
}

#tocBackdrop[hidden] {
  display: none;
}

#tocToggle {
  position: fixed;
  top: var(--space-md);
  left: var(--space-md);
  z-index: 1001;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  min-height: 44px;
  background: var(--surface-raised);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: var(--text-primary);
  padding: var(--space-sm) var(--space-md);
}

@media (prefers-reduced-motion: reduce) {
  #tocSidebar,
  #tocBackdrop {
    transition: none;
  }
}
```

### Sidebar JavaScript

```html
<script>
(function () {
  var sidebar = document.getElementById("tocSidebar");
  var backdrop = document.getElementById("tocBackdrop");
  var toggle = document.getElementById("tocToggle");
  var previousFocus = null;
  var storageKey = "nord-sidebar";
  var isOpen = false;

  function isNarrow() {
    return window.matchMedia("(max-width: 900px)").matches;
  }

  function showSidebar() {
    isOpen = true;
    sidebar.removeAttribute("hidden");
    toggle.setAttribute("aria-expanded", "true");
    if (isNarrow()) {
      backdrop.removeAttribute("hidden");
    }
    try { localStorage.setItem(storageKey, "open"); } catch (e) {}
  }

  function hideSidebar() {
    isOpen = false;
    sidebar.setAttribute("hidden", "");
    backdrop.setAttribute("hidden", "");
    toggle.setAttribute("aria-expanded", "false");
    try { localStorage.setItem(storageKey, "closed"); } catch (e) {}
    if (previousFocus && document.body.contains(previousFocus)) {
      previousFocus.focus();
    }
  }

  function openSidebar() {
    previousFocus = document.activeElement;
    showSidebar();
    var firstLink = sidebar.querySelector("a");
    if (firstLink) firstLink.focus();
  }

  function closeSidebar() {
    hideSidebar();
  }

  toggle.addEventListener("click", function () {
    if (isOpen) {
      closeSidebar();
    } else {
      openSidebar();
    }
  });

  backdrop.addEventListener("click", closeSidebar);

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && isOpen) {
      closeSidebar();
    }
  });

  var lastNarrow = isNarrow();
  window.addEventListener("resize", function () {
    var narrow = isNarrow();
    if (narrow && !lastNarrow && isOpen) {
      var containedFocus = sidebar.contains(document.activeElement);
      isOpen = false;
      sidebar.hidden = true;
      backdrop.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
      if (containedFocus) toggle.focus();
    } else if (!narrow && isOpen) {
      backdrop.hidden = true;
    }
    lastNarrow = narrow;
  });

  // On initial load: restore saved open preference only on desktop.
  // On narrow screens, default to closed (no auto-open).
  try {
    var saved = localStorage.getItem(storageKey);
    if (saved === "open" && !isNarrow()) {
      showSidebar();
    }
  } catch (e) {}
})();
</script>
```

The sidebar state is persisted in `localStorage` with a try/catch guard. On page load, a saved "open" preference is restored only on desktop (wider than 900px). On narrow screens the sidebar defaults to closed. Focus is saved before explicit open and restored on explicit close. The backdrop is shown only on narrow screens. When the viewport resizes from wide to narrow, entering narrow mode closes the sidebar immediately, without changing the saved preference; focus returns to the toggle only if it was inside the sidebar. The saved desktop preference is not overwritten on resize.

### Scroll-Spy Highlighting

Highlight the active section link as the user scrolls. Use `aria-current="true"` on the active link for screen readers. Compute the current active link by checking all section positions on each callback and on initial load, not just the entries in the current callback.

```html
<script>
(function () {
  var links = document.querySelectorAll("#tocSidebar a");
  var sections = [];

  links.forEach(function (link) {
    var href = link.getAttribute("href");
    if (!href || href.charAt(0) !== "#") return;
    var id = href.slice(1);
    var section = document.getElementById(id);
    if (section) sections.push({ link: link, section: section });
  });

  if (sections.length === 0) return;

  function setActive(link) {
    sections.forEach(function (s) {
      s.link.removeAttribute("aria-current");
    });
    link.setAttribute("aria-current", "true");
    try {
      localStorage.setItem("nord-toc-active", link.getAttribute("href"));
    } catch (e) {}
  }

  function computeActive() {
    var scrollPos = window.scrollY + window.innerHeight * 0.2;
    var active = sections[0];
    sections.forEach(function (s) {
      if (s.section.offsetTop <= scrollPos) active = s;
    });
    setActive(active.link);
  }

  try {
    var observer = new IntersectionObserver(function () {
      computeActive();
    }, { rootMargin: "-20% 0px -60% 0px" });

    sections.forEach(function (s) { observer.observe(s.section); });
  } catch (e) {
    // IntersectionObserver not supported; fall back to scroll event
    window.addEventListener("scroll", computeActive, { passive: true });
  }

  // On initial load, compute active from scroll position (not from stored value)
  // to avoid restoring a stale highlight over the actual viewport.
  computeActive();
})();
</script>
```

The scroll-spy computes the active link from all section positions on each IntersectionObserver callback and on initial load, ensuring the highlight always reflects the actual viewport. A single `aria-current="true"` is maintained. Guarded `localStorage` stores the active href but is not restored on load to avoid stale highlights.

---

## Graphical Diagrams

Diagrams are rendered with CSS and HTML, not with box-drawing Unicode characters. The `.code-block` class must never contain box-drawing diagrams.

### Diagram Base Styles

```css
.diagram {
  background: var(--surface-raised);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: var(--space-xl);
  overflow-x: auto;
}
```

### Flow Diagram

Use `.diagram-flow` for left-to-right process diagrams.

```css
.diagram-flow {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  flex-wrap: wrap;
}

.diagram-flow__node {
  background: var(--surface-base);
  border: 2px solid var(--accent-primary);
  border-radius: var(--radius-md);
  padding: var(--space-md) var(--space-lg);
  text-align: center;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
}

.diagram-flow__arrow {
  display: flex;
  align-items: center;
  color: var(--text-secondary);
  font-size: 1.5rem;
  user-select: none;
}
```

```html
<div class="diagram diagram-flow">
  <div class="diagram-flow__node">Input</div>
  <div class="diagram-flow__arrow" aria-hidden="true">&#8594;</div>
  <div class="diagram-flow__node">Process</div>
  <div class="diagram-flow__arrow" aria-hidden="true">&#8594;</div>
  <div class="diagram-flow__node">Output</div>
</div>
```

### Sequence Diagram

Use `.diagram-sequence` for timed or ordered interactions.

```css
.diagram-sequence {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.diagram-sequence__step {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-sm) 0;
}

.diagram-sequence__actor {
  min-width: 80px;
  font-weight: 600;
  color: var(--accent-primary);
  text-align: right;
}

.diagram-sequence__action {
  flex: 1;
  padding: var(--space-xs) var(--space-md);
  background: var(--surface-base);
  border-left: 3px solid var(--border-strong);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
}

.diagram-sequence__target {
  min-width: 80px;
  font-weight: 600;
  color: var(--text-primary);
}
```

```html
<div class="diagram diagram-sequence">
  <div class="diagram-sequence__step">
    <span class="diagram-sequence__actor">Client</span>
    <span class="diagram-sequence__action">Send request</span>
    <span class="diagram-sequence__target">Server</span>
  </div>
  <div class="diagram-sequence__step">
    <span class="diagram-sequence__actor">Server</span>
    <span class="diagram-sequence__action">Process data</span>
    <span class="diagram-sequence__target">Client</span>
  </div>
</div>
```

### Panels Diagram

Use `.diagram-panels` for side-by-side comparison layouts.

```css
.diagram-panels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-lg);
}

.diagram-panels__panel {
  background: var(--surface-base);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
}

.diagram-panels__title {
  font-weight: 600;
  color: var(--accent-primary);
  margin-bottom: var(--space-sm);
}
```

```html
<div class="diagram diagram-panels">
  <div class="diagram-panels__panel">
    <div class="diagram-panels__title">Option A</div>
    <p>Description of the first approach.</p>
  </div>
  <div class="diagram-panels__panel">
    <div class="diagram-panels__title">Option B</div>
    <p>Description of the second approach.</p>
  </div>
</div>
```

---

## Tables

### Table Wrapper and Compare Table

Tables are wrapped in `.table-wrap` for horizontal scroll on narrow screens. The `.compare-table` class provides structured comparison styling.

```css
.table-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
}

table.compare-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}

table.compare-table th,
table.compare-table td {
  padding: 1rem 1.15rem;
  text-align: left;
  border-bottom: 1px solid var(--border-default);
}

table.compare-table th {
  background: var(--surface-raised);
  font-weight: 600;
  color: var(--text-primary);
  position: sticky;
  top: 0;
}

table.compare-table td {
  color: var(--text-secondary);
}
```

### Row State Bars

Rows can carry a tinted left bar to indicate evaluation state. The bar appears only on the first cell of each row to avoid visual duplication.

```css
table.compare-table tr.row-selected td:first-child {
  border-left: 4px solid var(--state-success);
}

table.compare-table tr.row-evaluated td:first-child {
  border-left: 4px solid var(--state-warning);
}

table.compare-table tr.row-rejected td:first-child {
  border-left: 4px solid var(--state-error);
}

/* Tinted background on the entire row */
table.compare-table tr.row-selected td {
  background: color-mix(in srgb, var(--state-success) 8%, transparent);
}

table.compare-table tr.row-evaluated td {
  background: color-mix(in srgb, var(--state-warning) 8%, transparent);
}

table.compare-table tr.row-rejected td {
  background: color-mix(in srgb, var(--state-error) 8%, transparent);
}
```

Fallback for browsers that do not support `color-mix()`:

```css
@supports not (background: color-mix(in srgb, red, transparent)) {
  table.compare-table tr.row-selected td { background: rgba(163, 190, 140, 0.08); }
  table.compare-table tr.row-evaluated td { background: rgba(235, 203, 139, 0.08); }
  table.compare-table tr.row-rejected td { background: rgba(191, 97, 106, 0.08); }
}
```

### Cell Typography

```css
.cell-title {
  font-weight: 600;
  color: var(--text-primary);
}

.cell-sub {
  display: block;
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-top: 2px;
}
```

Use `--text-secondary` for `.cell-sub` to ensure readability in both themes. Do not use `--text-muted` for meaningful text.

### Status Pills

Compact inline badges for row-level status. Each pill uses a tinted background with `--text-primary` for text in both themes, ensuring adequate contrast against lightly tinted backgrounds.

```css
.status-pill {
  display: inline-block;
  padding: 0.15em 0.6em;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  line-height: 1.4;
}

.pill-good {
  background: color-mix(in srgb, var(--state-success) 20%, transparent);
  color: var(--text-primary);
}

.pill-warn {
  background: color-mix(in srgb, var(--state-warning) 20%, transparent);
  color: var(--text-primary);
}

.pill-bad {
  background: color-mix(in srgb, var(--state-error) 20%, transparent);
  color: var(--text-primary);
}

.pill-info {
  background: color-mix(in srgb, var(--state-info) 20%, transparent);
  color: var(--text-primary);
}

/* Fallback for browsers that do not support color-mix() */
@supports not (background: color-mix(in srgb, red, transparent)) {
  .pill-good { background: rgba(163, 190, 140, 0.2); }
  .pill-warn { background: rgba(235, 203, 139, 0.2); }
  .pill-bad { background: rgba(191, 97, 106, 0.2); }
  .pill-info { background: rgba(136, 192, 208, 0.2); }
}
```

---

## Lifecycle and Flow Animations

### Lifecycle Steps

The `.lifecycle` component normalizes phase comparison across a horizontal step indicator. All options share the same canonical phases so positions and widths are consistent even when some steps are absent. Each step carries an accessible label.

```css
.lifecycle {
  display: flex;
  gap: 0;
  position: relative;
}

.lc-steps {
  display: flex;
  flex: 1;
  position: relative;
}

.lc-steps::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--border-default);
  transform: translateY(-50%);
  z-index: 0;
}

.lc-step {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
  position: relative;
  z-index: 1;
}

.lc-step__circle {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: var(--surface-raised);
  border: 2px solid var(--border-strong);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: var(--text-sm);
  color: var(--text-secondary);
  transition: border-color var(--transition-fast), color var(--transition-fast);
}

.lc-step.is-complete .lc-step__circle {
  border-color: var(--state-success);
  color: var(--text-primary);
}

.lc-step.is-current .lc-step__circle {
  border-color: var(--accent-primary);
  color: var(--text-primary);
  box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent-primary) 30%, transparent);
}

.lc-step__label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  text-align: center;
}
```

```html
<div class="lifecycle" role="navigation" aria-label="Process steps">
  <div class="lc-steps">
    <div class="lc-step is-complete">
      <span class="lc-step__circle" aria-label="Planning, completed">1</span>
      <span class="lc-step__label">Planning (completed)</span>
    </div>
    <div class="lc-step is-current">
      <span class="lc-step__circle" aria-label="Development, current step">2</span>
      <span class="lc-step__label">Development (current step)</span>
    </div>
    <div class="lc-step">
      <span class="lc-step__circle" aria-label="Review, not applicable">3</span>
      <span class="lc-step__label">Review — not applicable</span>
    </div>
    <div class="lc-step">
      <span class="lc-step__circle" aria-label="Deploy, pending">4</span>
      <span class="lc-step__label">Deploy — pending</span>
    </div>
  </div>
</div>
```

When comparing multiple options, render each option with the same set of phase slots. If an option lacks a particular step, mark it explicitly as **Not applicable** (e.g., `aria-label="Step 3: Review, not applicable"`) rather than leaving it visually ambiguous. Use the `is-pending` class for steps that are not yet reached and reserve neutral styling only for genuinely pending states.

### Two-Option Canonical Comparison

For side-by-side comparison of two options, use equal-width columns so each phase aligns:

```html
<div class="diagram diagram-panels">
  <div class="diagram-panels__panel">
    <div class="diagram-panels__title">Option A</div>
    <div class="lifecycle" role="navigation" aria-label="Option A steps">
      <div class="lc-steps">
        <div class="lc-step is-complete">
          <span class="lc-step__circle" aria-label="Planning, completed">1</span>
          <span class="lc-step__label">Planning (completed)</span>
        </div>
        <div class="lc-step is-current">
          <span class="lc-step__circle" aria-label="Development, current">2</span>
          <span class="lc-step__label">Development (current)</span>
        </div>
        <div class="lc-step">
          <span class="lc-step__circle" aria-label="Review, not applicable">3</span>
          <span class="lc-step__label">Review — not applicable</span>
        </div>
      </div>
    </div>
  </div>
  <div class="diagram-panels__panel">
    <div class="diagram-panels__title">Option B</div>
    <div class="lifecycle" role="navigation" aria-label="Option B steps">
      <div class="lc-steps">
        <div class="lc-step is-complete">
          <span class="lc-step__circle" aria-label="Planning, completed">1</span>
          <span class="lc-step__label">Planning (completed)</span>
        </div>
        <div class="lc-step">
          <span class="lc-step__circle" aria-label="Development, pending">2</span>
          <span class="lc-step__label">Development — pending</span>
        </div>
        <div class="lc-step">
          <span class="lc-step__circle" aria-label="Review, pending">3</span>
          <span class="lc-step__label">Review — pending</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

### Flow Pulse Animation

The `.flow-svg` class provides a container for SVG-based flow diagrams. The `.flow-pulse` class adds a subtle animated indicator. When motion is reduced, the pulse communicates equivalent information through a static visual distinction (solid fill with a ring) instead of animation.

```css
.flow-svg {
  width: 100%;
  height: auto;
  display: block;
}

.flow-pulse {
  animation: flow-pulse-anim 2s ease-in-out infinite;
}

@keyframes flow-pulse-anim {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .flow-pulse {
    animation: none;
    opacity: 1;
    stroke: var(--surface-raised);
    stroke-width: 2;
  }
}
```

Example SVG usage:

```html
<svg class="flow-svg" viewBox="0 0 400 100" role="img"
     aria-label="Flow diagram: stage 1 complete, stage 2 current, stage 3 pending">
  <line x1="40" y1="50" x2="360" y2="50"
        stroke="var(--border-strong)" stroke-width="2"/>
  <circle cx="40" cy="50" r="8" fill="var(--state-success)"/>
  <circle cx="200" cy="50" r="8" fill="var(--accent-primary)" class="flow-pulse"/>
  <circle cx="360" cy="50" r="8" fill="var(--text-secondary)"/>
</svg>
```

Because `role="img"` flattens child element names, the `aria-label` on the `<svg>` itself must describe the complete, current, and pending states explicitly.

---

## Accessible Modals

Use the native `<dialog>` element for modals. It provides built-in focus containment, Escape-to-close, inert background, and automatic return focus. No hand-rolled focus trap is needed.

### HTML Structure

```html
<!-- Opening button -->
<button type="button" class="btn btn-primary" id="openConfirm">Open Confirmation</button>

<dialog id="confirmDialog" aria-labelledby="dlg-title">
  <div class="modal-header">
    <h2 id="dlg-title" class="modal-title">Confirm Action</h2>
    <button type="button" class="modal-close" data-dialog-close aria-label="Close dialog">Close</button>
  </div>
  <div class="modal-body">
    <p>Are you sure you want to proceed?</p>
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-secondary" data-dialog-close id="dlg-cancel">Cancel</button>
    <button type="button" class="btn btn-primary" id="dlg-confirm">Confirm</button>
  </div>
</dialog>
```

The `<dialog>` element carries `aria-labelledby` pointing to the title for an accessible name. Both Cancel and the Close button use `data-dialog-close` for declarative close behavior.

### Modal Styles

```css
dialog {
  background: var(--surface-raised);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  max-width: 560px;
  width: calc(100% - 2rem);
  max-height: 80vh;
  overflow-y: auto;
  color: inherit;
  padding: 0;
}

dialog::backdrop {
  background: var(--surface-overlay);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-lg);
  border-bottom: 1px solid var(--border-default);
}

.modal-title {
  margin: 0;
  font-size: var(--text-xl);
  color: var(--text-primary);
}

.modal-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: none;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: var(--text-secondary);
}

.modal-close:hover,
.modal-close:focus-visible {
  color: var(--text-primary);
  border-color: var(--border-default);
}

.modal-body {
  padding: var(--space-lg);
  color: var(--text-secondary);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-sm);
  padding: var(--space-lg);
  border-top: 1px solid var(--border-default);
}
```

### Modal JavaScript

```html
<script>
(function () {
  var dialog = document.getElementById("confirmDialog");
  var openBtn = document.getElementById("openConfirm");
  var cancelBtn = document.getElementById("dlg-cancel");
  var triggerElement = null;

  // Open the modal
  function openDialog() {
    // Save the current focus target before showModal() shifts it
    triggerElement = document.activeElement;
    dialog.showModal();
    // Focus the Cancel (non-destructive) button
    if (cancelBtn) cancelBtn.focus();
  }

  // Close the modal
  function closeDialog() {
    dialog.close();
  }

  // Wire up the opening button
  if (openBtn) {
    openBtn.addEventListener("click", openDialog);
  }

  // Close on data-dialog-close buttons
  dialog.addEventListener("click", function (e) {
    var closeBtn = e.target.closest("[data-dialog-close]");
    if (closeBtn) {
      closeDialog();
    }
  });

  // Close on Escape is handled natively by <dialog>

  // Restore focus after close
  dialog.addEventListener("close", function () {
    if (triggerElement && document.body.contains(triggerElement)) {
      triggerElement.focus();
    } else {
      // Fallback: focus the explicit fallback heading
      var fallback = document.getElementById("fallback-heading");
      if (fallback) fallback.focus();
    }
    triggerElement = null;
  });
})();
</script>
```

Place an explicit fallback heading near the top of the page so focus restoration has a safe target when the trigger element is removed:

```html
<h1 id="fallback-heading" tabindex="-1">Page Title</h1>
```

The `<dialog>` element handles focus containment natively while open. The dialog closes on Escape or when an explicit close button (marked with `data-dialog-close`) is activated. Before `showModal()` shifts focus, we save `document.activeElement`. After opening, focus goes to Cancel (the non-destructive control). On close, focus is safely restored to the trigger if it remains in the DOM; otherwise we fall back to the explicit fallback heading identified by `id="fallback-heading"`.

### Reduced Motion for Modals

```css
@media (prefers-reduced-motion: reduce) {
  dialog {
    animation: none;
  }
}
```

### Theme Behavior

The dialog inherits all CSS custom properties from the document. No additional theme logic is required. When `data-theme="light"` is set on `<html>`, the dialog automatically uses light-theme tokens.

---

## Content Security Policy

For static judge reports use exactly `default-src 'none'; style-src 'unsafe-inline'; img-src data:`. Embed in an iframe with an empty `sandbox` attribute for additional isolation. The optional policy below applies only to separately hosted interactive reports, not the static judge template.

### Recommended CSP Header

```
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';
```

### Safe Deployment of Scripts

- All JavaScript examples in this guide are external snippets. In production, bundle them into external `.js` files hosted on the same origin (`'self'`). No `unsafe-inline` is needed.
- A same-origin synchronous external script placed in the `<head>` can read `localStorage` and set `data-theme` before render, preventing flash of wrong theme without requiring `unsafe-inline`.
- If inline scripts are unavoidable, use nonces (`script-src 'self' 'nonce-<base64-value>'`) rather than hashes. Nonces are a random base64 value generated server-side per request and placed on each `<script>` tag. Do not use actual secret keys; the nonce is a short-lived per-request token. Rotate nonces on every response.

### Safe Deployment of Styles

- All CSS examples in this guide are external snippets. In production, place them in external `.css` files hosted on the same origin.
- Inline `style` attributes are not used by the design system. If dynamic styles are required (e.g., CSS variable overrides), apply them via a `<style>` tag in the document head with a matching nonce, or set the variables on `:root` through JavaScript `document.documentElement.style.setProperty()`.

### Tradeoffs

| Approach | Pros | Cons |
|----------|------|------|
| External script for theme | CSP-friendly, no inline scripts; reads localStorage synchronously before paint | Requires a synchronous same-origin script in the `<head>` |
| Nonced inline scripts | Keeps the synchronous localStorage read | Requires server-side nonce generation and rotation |

---

## Buttons

```css
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 0.5em 1.2em;
  font-size: var(--text-base);
  font-weight: 600;
  font-family: inherit;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background var(--transition-fast), border-color var(--transition-fast);
  text-decoration: none;
}

.btn-primary {
  background: var(--accent-primary);
  color: #2E3440;
  border-color: var(--accent-primary);
}

.btn-primary:hover,
.btn-primary:focus-visible {
  filter: brightness(1.1);
}

/* Light theme: primary button text is white for contrast against --accent-primary (#345879) */
[data-theme="light"] .btn-primary {
  color: #FFFFFF;
}

.btn-secondary {
  background: var(--surface-base);
  color: var(--text-primary);
}

.btn-secondary:hover,
.btn-secondary:focus-visible {
  background: var(--surface-raised);
  border-color: var(--border-strong);
}

.btn:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .btn,
  .lc-step__circle {
    transition: none;
  }
}
```

---

## Focus and Visibility

All interactive elements must have a visible focus indicator. The design system uses a consistent `:focus-visible` ring.

```css
:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
}
```

Screen reader-only content can be hidden visually while remaining accessible:

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## Code Blocks

Code blocks use the `.code-block` class. Box-drawing Unicode characters are prohibited inside `.code-block`.

```css
.code-block {
  background: var(--surface-base);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  line-height: 1.6;
  color: var(--text-secondary);
}
```

---

## Summary of Key Selectors

| Selector | Purpose |
|----------|---------|
| `.metric-grid` | 3-column metric card grid |
| `.interactive-grid` | 3-column interactive element grid |
| `.nord-card-grid` | 3-column card grid |
| `.nord-card` | Equal-height flex card |
| `.nord-mini-card` | Colored mini-card with colored left border for list items |
| `.card-mini-stack` | Vertical stack container for mini-cards |
| `#tocSidebar` | Table of contents sidebar |
| `#tocToggle` | Sidebar toggle button |
| `#tocBackdrop` | Sidebar overlay backdrop |
| `.diagram` | Diagram container |
| `.diagram-flow` | Flow diagram layout |
| `.diagram-sequence` | Sequence diagram layout |
| `.diagram-panels` | Panels comparison diagram |
| `.table-wrap` | Horizontally scrollable table wrapper |
| `.compare-table` | Structured comparison table |
| `.row-selected` | Green-tinted row state |
| `.row-evaluated` | Amber-tinted row state |
| `.row-rejected` | Red-tinted row state |
| `.cell-title` | Bold cell text |
| `.cell-sub` | Subtitle cell text |
| `.status-pill` | Inline status badge |
| `.pill-good` | Green status pill |
| `.pill-warn` | Amber status pill |
| `.pill-bad` | Red status pill |
| `.pill-info` | Blue status pill |
| `.lifecycle` | Lifecycle step container |
| `.lc-steps` | Normalized phase steps |
| `.flow-svg` | SVG flow diagram container |
| `.flow-pulse` | Animated pulse indicator |
| `dialog` | Native modal dialog element |
| `dialog::backdrop` | Modal backdrop pseudo-element |
| `.code-block` | Preformatted code container |
| `.btn` | Base button style |
| `.btn-primary` | Primary accent button |
| `.btn-secondary` | Secondary outline button |
| `.sr-only` | Screen-reader-only text |
| `[data-theme="light"]` | Light theme override |

---

## Edge Cases and Tradeoffs

- **`color-mix()` support**: The function is not available in all browsers. Always provide a fallback using explicit `rgba()` values for row tints and status pills, guarded with `@supports not (background: color-mix(in srgb, red, transparent))`.
- **Grid orphan rows**: Use groups of three or span a lone final card; stack cards on narrow screens and never add fictitious content.
- **Theme flash**: Synchronous `localStorage` reads in `<head>` prevent flash but block parsing. A same-origin synchronous external script in the `<head>` achieves the same result without inline scripts. Guard all `localStorage` access with try/catch.
- **IntersectionObserver rootMargin**: The value `-20% 0px -60% 0px` creates a narrow trigger band near the top of the viewport. Adjust based on actual section heights and header overlap. A passive scroll fallback is provided if the observer is unavailable.
- **Dialog focus restoration**: If the element that opened the `<dialog>` is no longer in the DOM when the dialog closes, focus falls back to an explicit heading element with `id="fallback-heading"` and `tabindex="-1"`. Place this heading near the top of the page. Do not rely on querying `h1` generically, as `h1` elements without `tabindex` cannot receive focus.
- **Reduced motion**: All animations and transitions must respect `prefers-reduced-motion: reduce`. The design system provides media queries for flow pulse, dialog, sidebar, button, and lifecycle step transitions. Add similar queries for any custom animations.