# TopoLab — Version History

## v0.6.0 — Per-part quizzes, saved drafts, and finite examples

### Added
- 40 distinct multiple-choice questions, one for every subquestion in Sheets N1 and N2.
- Per-subquestion explanatory feedback and persisted attempt/correct counters.
- Atomic local JSON persistence for proof drafts, restored per exercise part.
- User-entered finite topology validation and calculations: open/closed sets, interior, closure, boundary, accumulation points, isolated points, and Hausdorff status (up to 10 points).
- Tests for quiz coverage, persistence, and finite example calculations.

### Scope
- The finite example checker does not decide arbitrary infinite-space claims.
- Free-form proof drafts are saved but are not formally proof-checked.
- N1 Exercise 3, part 2, has two sets that are not neighborhoods of 2: [2,4) and (2,4); the quiz tests the complete classification.



## v0.5.0 — Course exercise and quiz laboratory

### Added
- A source-grounded exercise bank containing all 10 exercises from Sheet N1 and all 4 exercises from Sheet N2, including all 40 listed subparts.
- Part-by-part study explanations for all supplied exercise parts.
- Quiz mode with one multiple-choice check per numbered exercise (14 checks total), answer checking, and explanatory feedback.
- ExerciseController and tests for source-bank completeness and quiz structure.

### Scope and verification
- The currently attached exercise sheets are N1 and N2; no separate Sheet N3 was present in the supplied files.
- This release does not formally verify free-form proof text. Quiz answers are checked against explicit keys.
- The source for compactness exercises is Sheet N2, supported by the supplied Chapter 3 notes.
- Free-form proof drafts are not persisted across restarts; per-exercise concrete example validation is not yet integrated.



## v0.4.0 — Finite metric-space laboratory

**Status:** Implementation committed; run the test suite and verify the Qt/QML runtime on Windows.

### Added
- FiniteMetricSpace with validation of the three metric axioms: separation, symmetry, and triangle inequality.
- Explicit completeness checks for the ordered-pair distance table.
- Open-ball and closed-ball calculations.
- Generation of the induced topology, with the finite-space result that every finite metric space is discrete.
- Finite epsilon-net construction and a total-boundedness check for a requested epsilon.
- MetricController and controller tests.

### Changed
- Replaced the Metric Laboratory's display-only placeholder with an interactive finite metric workspace.
- Registered MetricController with the Qt application.
- Updated application and project metadata to v0.4.0.

### Scope and verification
- The interactive page accepts at most 10 labelled points and requires all ordered-pair distances.
- Distances are numerical; the triangle-inequality comparison uses a small floating-point tolerance.
- Infinite metric spaces and symbolic distance functions are not implemented.
- Tests are included but must be run locally. Windows QML rendering remains to be checked.

## v0.3.0 — Interactive finite Set Toolkit

**Status:** Implemented; user reported 95 tests successful after this release.

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
- The finite-map operations remain available in the core but are not yet exposed in the Set Toolkit page.

## v0.2.0 — Finite set-theory core
- Added finite set operations, finite-family unions/intersections, Cartesian products, cardinality, and finite-map image/preimage and map properties.
- Added tests for the finite set engine.

## v0.1.1 — Typography and mathematical notation
- Added reusable mathematical formula rendering and improved typography.

## v0.1.0 — Initial interface foundation
- Added the PySide6 / Qt Quick application shell, navigation, reusable components, and initial workspace pages.

---

## Versioning convention
- PATCH: fixes and small refinements.
- MINOR: a substantial new mathematical capability or module.
- MAJOR: a stable, integrated release suitable for the final university demonstration.
