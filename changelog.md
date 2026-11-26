# TopoLab — Version History

This file records the project releases delivered so far. Append a new section whenever a new version is delivered.

## v0.3.0 — Interactive finite Set Toolkit

**Status:** Implementation committed; local test execution and Windows QML runtime verification remain to be performed.

### Added
- A SetController that parses the workspace's finite-set notation and calls the existing mathematical core.
- Interactive calculations for union, intersection, difference, complement relative to a universe, power sets, Cartesian products, subset, equality, and disjointness.
- Input validation for duplicate or malformed labels and for complements whose set is not contained in the universe.
- Explicit size limits for power-set and Cartesian-product rendering.
- A dedicated controller test module.

### Changed
- Connected the Set Toolkit QML page to the Python controller.
- Registered the controller in the Qt application.
- Updated the project version to 0.3.0 in application metadata and documentation.

### Scope and verification
- The interface works with finite sets of simple labels; intervals, infinite sets, and symbolic expressions are outside this workspace's current input grammar.
- The finite-map operations remain available in the Python core but are not yet exposed in the Set Toolkit page.
- Tests have been added but have not been executed in this environment. Run python -m unittest discover -s tests -v and launch the app on Windows to verify the Qt/QML runtime.

## v0.2.0 — Finite set-theory core

**Status:** Mathematical core committed; QML integration remains in progress.

### Added
- A reusable finite-set engine in topolab/core/sets.py.
- Subset and equality checks, power sets, union, intersection, difference, complements relative to an explicit universe, disjointness, indexed-family unions and intersections, Cartesian products, and finite cardinality.
- Finite-map image and preimage operations, injective/surjective/bijective checks, composition, and inverse functions for bijections.
- A dedicated test module covering the implemented operations and several image/preimage identities from Chapter 1.

### Mathematical scope
- The engine uses finite Python collections of hashable objects and immutable set results.
- Complements always require an explicit ambient universe.
- Preimages are supported for arbitrary finite maps; inverse functions are restricted to bijections.
- Infinite number systems and symbolic interval or piecewise-function calculations are not implemented by this finite engine.
- The Set Toolkit QML page has not yet been connected to these operations.

## v0.1.1 — Typography and mathematical notation

**Status:** Delivered as an update archive / patch.

### Added
- MathFormula.qml, a reusable QML component for displayed mathematical expressions.
- A Python math-rendering service using Matplotlib MathText and the STIX math font set.
- A clearer typography hierarchy using Segoe UI for interface text and Georgia for major headings.

### Changed
- Increased small interface text sizes and improved spacing to reduce clipping.
- Added Matplotlib to the project dependencies.
- Updated the README and project metadata to identify version 0.1.1.

### Notes
- MathText supports a TeX-like subset; it is not a complete LaTeX installation.
- The v0.1.1 archive is an update patch intended to be extracted over the v0.1.0 starter project. Preserve .venv when applying updates.

## v0.1.0 — Initial interface foundation

**Status:** Delivered as the initial starter project archive.

### Added
- Python application entry point and PySide6 / Qt Quick (QML) structure.
- Initial terracotta, espresso, parchment and cyan visual theme.
- Main window and sidebar navigation.
- Reusable navigation, panel, metric-card, action-button and page-heading components.
- Initial Overview, Space Explorer, Set Toolkit, Proof Laboratory and Metric Laboratory screens.
- Starter folders for the mathematical core, tests, examples and assets.

### Notes
- The screens are interface scaffolding only; topology calculations were not implemented in this release.
- The intended course scope is the Set Theory Reminder (Chapter 1) and Topological Spaces (Chapter 2).

---

## Versioning convention for future deliveries

- PATCH (for example, 0.2.0 → 0.2.1): fixes or small improvements that do not add a substantial capability.
- MINOR (for example, 0.2.0 → 0.3.0): a new mathematical module or substantial integrated capability.
- MAJOR (0.x → 1.0.0): a stable, integrated release suitable for the final university demonstration.

For each future delivery, update the version in pyproject.toml, topolab/app.py, and README.md, then append to this changelog. Clearly label an archive as either a complete project or a patch/update.
