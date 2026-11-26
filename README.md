# TopoLab Project

An interactive topology-learning laboratory built with Python, PySide6, and Qt Quick (QML).

## Current development status

**Version 0.5.0 — course exercise and quiz laboratory**

The Proof Laboratory is now an Exercise & Quiz Laboratory containing all 14 exercises from the supplied Sheets N1 and N2, with part-by-part study explanations and an objectively keyed multiple-choice check for each exercise.

The Set Toolkit and finite topological-space explorer are connected to Python mathematical modules. Version 0.4.0 adds a finite metric engine and connects it to the Metric Laboratory.

### Exercise & Quiz Laboratory

- Browse all 10 exercises from Sheet N1 and all 4 exercises from Sheet N2.
- Read each original exercise statement and every listed sub-question.
- Study concise solution explanations for each part.
- Switch to quiz mode, select an answer, and receive immediate correctness feedback and an explanation.
- The exercise bank is local and works without an AI service or internet connection.

**Proof-checking limitation:** written proof text is not yet formally verified. The explanations are study solutions, while quiz questions are checked against explicit answer keys. The application does not label a student's free-form proof mathematically correct.

### Metric Laboratory capabilities

- Checks the metric axioms M1 (separation), M2 (symmetry), and M3 (triangle inequality).
- Requires an explicit distance for every ordered pair in the finite underlying set.
- Calculates open and closed balls for a selected centre and positive radius.
- Generates the metric topology of a finite metric space.
- Constructs finite epsilon-nets, supporting later compactness work.

### Mathematical scope

This release handles finite metric spaces with at most 10 labelled points in the interactive interface. Distances are entered as rows of the form \`x, y, d(x,y)\`; both ordered pairs must be supplied. The core uses numerical real distances and a small floating-point tolerance when checking triangle inequalities. It does not represent arbitrary infinite metric spaces or symbolic distance functions.

A finite metric space is discrete: each singleton is open, so its metric topology is the power set. This is a mathematical consequence of finiteness, not a restriction imposed by the interface.

### Existing finite-set workspace

The Set Toolkit supports union, intersection, difference, complement relative to an explicit universe, power sets, Cartesian products, subset, equality, and disjointness for finite sets of simple labels.

## Run the application

\`\`\`bash
python -m pip install -r requirements.txt
python main.py
\`\`\`

## Run tests

\`\`\`bash
python -m unittest discover -s tests -v
\`\`\`

Run the test suite in the project environment and launch the application on Windows to verify the Qt/QML runtime before treating a revision as locally verified.
