# TopoLab — Version History

This file records the project releases delivered so far. Keep it in the root of the `TopoLab Project` folder and append a new section whenever a new version is delivered.

## v0.1.1 — Typography and mathematical notation

**Status:** Delivered as an update archive / patch.

### Added
- `MathFormula.qml`, a reusable QML component for displayed mathematical expressions.
- A Python math-rendering service using Matplotlib MathText and the STIX math font set.
- A clearer typography hierarchy using Segoe UI for interface text and Georgia for major headings.

### Changed
- Increased small interface text sizes and improved spacing to reduce clipping.
- Added Matplotlib to the project dependencies.
- Updated the README and project metadata to identify version 0.1.1.

### Notes
- MathText supports a TeX-like subset; it is not a complete LaTeX installation.
- The current interface remains a visual scaffold. Mathematical calculations are not yet implemented.
- The v0.1.1 archive is an update patch intended to be extracted over the v0.1.0 starter project. Preserve `.venv` when applying updates.

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

- **PATCH** (`0.1.1` → `0.1.2`): fixes, typography adjustments, small UI improvements or corrections that do not add a major capability.
- **MINOR** (`0.1.1` → `0.2.0`): a new module or substantial capability, such as the first working set-theory engine.
- **MAJOR** (`0.x` → `1.0.0`): a stable, integrated release suitable for the final university demonstration.

For each future delivery, update the version in `pyproject.toml` and `README.md`, append to this changelog, and clearly label the archive as either a complete project or a patch/update.
