# TopoLab Project

An interactive topology-learning laboratory built with Python, PySide6, and Qt Quick (QML).

## Current development status

**Version 0.3.0 — interactive finite Set Toolkit**

The finite set-theory engine in topolab/core/sets.py is now connected to the Set Toolkit interface through topolab/services/set_controller.py.

The interactive workspace currently supports:
- Union, intersection, and difference of two finite sets.
- Complement relative to an explicitly entered universe.
- Power-set generation.
- Cartesian products as ordered pairs.
- Subset, equality, and disjointness checks.

### Mathematical and input scope

The current interface accepts finite sets of simple labels (letters, digits, and underscores), entered as comma-separated values such as a, b, c. It does not parse intervals, infinite sets, or symbolic expressions. Complement checks that the selected set is contained in the stated universe. The power-set display is limited to 8 elements and the Cartesian-product display to 100 ordered pairs to keep the interface responsive.

This is a focused integration milestone, not a claim that every Chapter 1 property or the full topology course is complete. The finite-map operations in the core are not yet exposed in the Set Toolkit interface.

## Run the application

```bash
python -m pip install -r requirements.txt
python main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

The tests cover the finite set engine and SetController input/calculation behavior. Run the command above in the project environment before treating the current revision as locally verified. QML rendering should also be checked by launching the app on Windows.
