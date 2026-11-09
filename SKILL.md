---
name: interactive-infographic-report
description: Design and generate interactive, animated Nord-palette HTML infographics, architecture reports, and CSP-sandboxed Agentic Judge evaluation reports with collapsible TOC sidebars, SVG flow animations, interactive lifecycle steppers, and color-coded comparison matrices. Use when creating technical reports, benchmark presentations, architecture overviews, or final judge evaluation reports.
---

# Interactive Infographic & Agentic Judge Design System

## Overview and Philosophy

This skill provides a high-freedom Design System, CSS/JS component catalog, and copy-and-customize HTML templates.
It is not a rigid Python data-to-HTML serializer.
AI agents and Agentic Judge LLMs author custom HTML directly using the Nord Design System building blocks.
You have full creative freedom to build custom SVG topologies, interactive calculators, bespoke lifecycle steppers, modal deep-dives, and domain-specific evaluation dashboards.
All artifacts remain 100% self-contained, dependency-free, and usable offline.

## Core Templates and Assets

- `assets/template-infographic.html`: Full interactive infographic and technical narrative boilerplate with dark/light themes, collapsible sidebar TOC, animated SVG data flow, 10-phase interactive lifecycle stepper, diagram panels, color-coded comparison tables, colored mini-cards, and keyboard-accessible modals.
- `assets/template-judge-report.html`: CSP-sandboxed Agentic Judge evaluation report boilerplate with decision summary, overall score, 3-card KPI grid, phase progress bars, evidence comparison table, multi-point findings as colored Nord mini-cards, and diagnostic callouts.
- `assets/nord-design-system.css`: Complete, standalone Nord design system stylesheet with dark/light CSS custom properties, responsive grids, diagram components, tables, mini-cards, and status pills.
- `references/design-system.md`: In-depth token specifications, contrast ratios, and design guidelines.
- `lint.py`: Verification utility that validates the 4 hard design invariants and safety heuristics.

## Recommended Narrative Structure

When authoring an interactive report, organize content into a compelling visual hierarchy:

1. Hero 3-Card KPI Grid: Introduce the subject with an eyebrow kicker, a prominent heading, introductory narrative, primary action buttons, and a 3-card metric grid (`.metric-grid` or `.card-grid`).
2. Collapsible Left TOC Sidebar: Provide instant navigation through `<nav id="tocSidebar">` containing `<div class="toc-list">` and `.toc-link` anchors, backed by an IntersectionObserver scroll-spy and mobile drawer support.
3. Animated SVG Architecture Flow: Illustrate movement between components with `.diagram-flow`, featuring embedded SVGs (`.flow-svg`) and animated pulse indicators (`.flow-pulse`) along horizontal or vertical paths.
4. Interactive 10-Phase Lifecycle Stepper / Calculator: Break multi-stage processes or algorithms into discrete steps using `.lifecycle`, `.lc-steps`, and `.lc-step` buttons, with keyboard arrow navigation and an active `.lc-detail` card.
5. Colored `.nord-mini-card` Grids: Present multi-point lists, recommendations, or architecture notes as colored mini-cards (`.nord-mini-card` with border modifiers) arranged in `.nord-card-grid` or `.card-mini-stack`.
6. Color-Coded `.compare-table` Matrices: Detail trade-offs, scenario outcomes, or model benchmarks with `table.compare-table`, applying `.row-selected`, `.row-evaluated`, or `.row-rejected` for clear visual distinction.
7. Clickable Modal Deep-Dives: Offer supplementary technical context or provenance details via `.modal-layer` and `.modal`, preserving focus trapping and Escape-to-close accessibility.

## Building Blocks and Component Recipes

### 1. Hero 3-Card KPI Grid

Use `.metric-grid`, `.interactive-grid`, or `.nord-card-grid` with three equal columns on desktop.
Cards stretch to match row height, and any lone trailing card spans the full width:

```html
<div class="card-grid metric-grid" aria-label="Key indicators">
  <article class="hero-card">
    <span class="card-label">Latency</span>
    <strong>180ms</strong>
    <p>Average round-trip response time.</p>
  </article>
  <article class="hero-card">
    <span class="card-label">Reliability</span>
    <strong>99.98%</strong>
    <p>Success rate over 10,000 runs.</p>
  </article>
  <article class="hero-card">
    <span class="card-label">Coverage</span>
    <strong>24 / 24</strong>
    <p>All benchmark scenarios verified.</p>
  </article>
</div>
```

### 2. Collapsible Left TOC Sidebar (Zero `<ul>` Lists)

In navigation sidebars, render links inside `<div class="toc-list">` without `<ul>` or `<li>` tags:

```html
<nav class="sidebar" id="tocSidebar" aria-label="Table of contents">
  <p class="sidebar-title">On this page</p>
  <div class="toc-list">
    <a class="toc-link" href="#overview"><span>01</span> Overview</a>
    <a class="toc-link" href="#architecture"><span>02</span> Architecture</a>
    <a class="toc-link" href="#evaluation"><span>03</span> Evaluation</a>
  </div>
</nav>
```

### 3. Animated SVG Architecture Flow

Represent data pipelines with SVG paths and animated pulses:

```html
<div class="diagram">
  <div class="diagram-header">
    <strong>Execution Pipeline</strong>
    <span class="diagram-caption">Signal to verdict</span>
  </div>
  <div class="diagram-flow" aria-label="Pipeline stages">
    <svg class="flow-svg flow-horizontal" viewBox="0 0 600 54" preserveAspectRatio="none" aria-hidden="true">
      <path class="flow-line" d="M 0 27 H 600"/>
      <circle class="flow-pulse" cx="0" cy="27" r="5"/>
    </svg>
    <div class="flow-node"><strong>Ingest</strong><small>Normalize inputs</small></div>
    <div class="flow-node"><strong>Analyze</strong><small>Verify assertions</small></div>
    <div class="flow-node"><strong>Score</strong><small>Produce verdict</small></div>
  </div>
</div>
```

### 4. Colored Nord Mini-Cards (Bullet List Replacement)

Bullet lists (`<ul><li>...</li></ul>`) are strictly forbidden across cards, sections, and modals.
Render multi-point findings as colored Nord mini-cards:

```html
<div class="card-mini-stack">
  <div class="nord-mini-card border-green">
    <p><strong>Verified Correctness:</strong> Deterministic checks passed on all test cases.</p>
  </div>
  <div class="nord-mini-card border-blue">
    <p><strong>Context Efficiency:</strong> Token utilization remained within optimal bounds.</p>
  </div>
  <div class="nord-mini-card border-yellow">
    <p><strong>Latency Variance:</strong> Failover path required higher negotiation time.</p>
  </div>
  <div class="nord-mini-card border-red">
    <p><strong>Known Limitation:</strong> Deep recursion requires manual approval gates.</p>
  </div>
</div>
```

Available border color modifiers:
- `.border-green`: Success, passed checks, confirmed strengths (`#a3be8c`).
- `.border-blue`: Primary informational points, neutral observations (`#88c0d0`).
- `.border-yellow`: Warnings, partial results, cautionary notices (`#ebcb8b`).
- `.border-purple`: Secondary structural notes, lifecycle hints (`#b48ead`).
- `.border-orange`: Moderate anomalies, performance cautions (`#d08770`).
- `.border-red`: Failures, detected defects, critical risks (`#bf616a`).

### 5. Color-Coded Comparison Matrices

Structure comparative benchmarks and case outcomes with `.compare-table`:

```html
<div class="table-wrap" role="region" aria-label="Option comparison" tabindex="0">
  <table class="compare-table">
    <thead>
      <tr>
        <th scope="col">Candidate</th>
        <th scope="col">Status</th>
        <th scope="col">Assessment</th>
      </tr>
    </thead>
    <tbody>
      <tr class="row-selected">
        <td><span class="cell-title">Model A</span><span class="cell-sub">Recommended</span></td>
        <td><span class="status-pill pill-good">Selected</span></td>
        <td>High accuracy, lowest latency, zero policy violations.</td>
      </tr>
      <tr class="row-evaluated">
        <td><span class="cell-title">Model B</span><span class="cell-sub">Fallback</span></td>
        <td><span class="status-pill pill-warn">Evaluated</span></td>
        <td>Acceptable precision, but higher inference cost.</td>
      </tr>
      <tr class="row-rejected">
        <td><span class="cell-title">Model C</span><span class="cell-sub">Disqualified</span></td>
        <td><span class="status-pill pill-bad">Rejected</span></td>
        <td>Exceeded allowed execution timeout during stress tests.</td>
      </tr>
    </tbody>
  </table>
</div>
```

## Emitting Agentic Judge HTML Verdicts

When an Agentic Judge LLM generates a final evaluation verdict:

1. Base the verdict on `assets/template-judge-report.html`.
2. Keep the strict Content Security Policy meta tag: `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:">`.
3. Do not run any scripts inside the judge document; render all scores, progress bars, and matrices directly as static HTML.
4. Structure the report with Decision Summary (`.summary.panel`), Key Indicators (`.kpi-grid`), Coverage Progress (`.progress-panel`), Evidence (`.compare-table`), Findings (`.nord-mini-card`), and Diagnostics (`.callout`).
5. Ensure all 4 design invariants are honored.

## The 4 Hard Design Invariants

Before delivering any authored HTML report, verify these 4 hard invariants:

1. Zero `<ul>` bullet lists: `<ul><li>...</li></ul>` tags are forbidden everywhere in content, navigation, and modals. Use colored `.nord-mini-card` components or `<div class="toc-list">` navigation.
2. Zero emojis: Emojis are forbidden in text, headings, and labels. Use clean monochrome SVG icons (such as embedded SVG symbols) or concise text labels.
3. Zero ASCII box-drawing in `.code-block`: Box-drawing characters (`┌─┐`, `│`, `└─┘`) are forbidden in code panels. Use graphical `.diagram-flow`, `.diagram-panels`, or embedded SVGs instead.
4. Valid `.compare-table` and `.nord-mini-card` CSS classes: Ensure the document includes or links the Nord Design System stylesheet with valid rules for comparison tables and mini-cards.

## Verification with `lint.py`

Run the included standalone linter from Python:

```sh
python3 lint.py <path-to-report.html>
```

The linter exits with code `0` if all invariants and safety checks pass, or exits with code `1` and prints specific line-level findings to stderr.
You can also run automated unit tests across the repository:

```sh
python3 -m unittest discover -s tests -v
```
