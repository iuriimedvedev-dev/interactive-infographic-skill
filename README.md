# Interactive Infographic & Agentic Judge Skill

## Purpose

A high-freedom Design System, CSS/JS component catalog, and copy-and-customize HTML template skill for creating interactive, animated technical infographics and CSP-sandboxed Agentic Judge evaluation reports.
Instead of constraining AI agents with a rigid Python JSON-to-HTML serializer, this skill empowers agents to directly author bespoke, beautiful, and accessible HTML reports using the Nord color palette.

## Key Features

- High-Freedom Authoring: Author custom HTML layouts, SVG topologies, interactive calculators, lifecycle steppers, and comparison matrices without schema bottlenecks.
- Complete Nord Design System: Includes `assets/nord-design-system.css` containing dark and light themes, 3-card metric grids, table wrappers, callout boxes, and status pills.
- Zero Bullet Lists (Strict Invariant): Bullet lists (`<ul><li>...</li></ul>`) are replaced by colored Nord mini-cards (`.nord-mini-card` with green, blue, yellow, purple, orange, and red border accents).
- Zero Emojis: Replaces emojis with clean monochrome SVG symbols and crisp textual badges.
- Animated SVG Flow Topologies: Provides `.diagram-flow` with smooth SVG pulse animations (`.flow-pulse`) and responsive horizontal/vertical transitions.
- Interactive 10-Phase Lifecycle: Accessible stepper with normalized phase matching and keyboard arrow navigation.
- CSP-Sandboxed Agentic Judge Verdicts: Includes `assets/template-judge-report.html` for scriptless, isolated, and evidence-grounded evaluation reports.
- Standalone Invariant Linter: Includes `lint.py` to enforce the 4 design invariants and safety heuristics before publication.

## Repository Layout

- `SKILL.md`: Complete agent instructions, narrative structure guides, and component recipes.
- `lint.py`: Standalone Python utility that verifies the 4 hard design invariants.
- `assets/nord-design-system.css`: Extracted, dependency-free CSS design system.
- `assets/template-infographic.html`: Self-contained interactive report boilerplate with sidebar TOC, animated SVG flows, lifecycle stepper, and modals.
- `assets/template-judge-report.html`: Self-contained CSP-sandboxed Agentic Judge verdict boilerplate.
- `references/design-system.md`: In-depth token specifications, color palettes, and contrast ratios.
- `tests/`: Automated unit and headless Chrome integration tests.

## Usage

### Authoring an Interactive Infographic

1. Copy `assets/template-infographic.html` to your target HTML file.
2. Customize the narrative following the structure described in `SKILL.md`:
   Hero 3-Card KPI Grid -> Collapsible Left TOC Sidebar -> Animated SVG Flow -> Interactive Lifecycle -> Colored Mini-Cards -> Color-Coded Comparison Matrices -> Clickable Modal Deep-Dives.
3. Replace sample text and SVG nodes with domain-specific verified facts.
4. Verify that no `<ul>` tags or emojis are present.

### Authoring an Agentic Judge Verdict

1. Copy `assets/template-judge-report.html` to your target HTML file.
2. Fill in the verdict pill (`.pill-good`, `.pill-warn`, `.pill-bad`), overall score, KPI metrics, progress bars, and case comparison table.
3. List multi-point findings using colored `.nord-mini-card` elements inside `.card-mini-stack`.
4. Keep the CSP meta tag to ensure sandboxed, safe delivery.

### Linting and Testing

Run the linter to verify an authored report:

```sh
python3 lint.py <path-to-report.html>
```

Run automated tests:

```sh
python3 -m unittest discover -s tests -v
```

## Attribution and License

The code and documentation are available under the MIT license.
Embedded inline Font Awesome Free SVG icons are by Fonticons, Inc. and licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Retain this attribution in redistributed copies.
