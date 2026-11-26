# TopoLab Project

An interactive topology-learning laboratory built with Python, PySide6, and Qt Quick (QML).

## Current development status

**Version 0.2.0 — finite set-theory core**

The first Chapter 1 mathematical engine is implemented in `topolab/core/sets.py`. It provides finite set operations, power sets, Cartesian products, finite-map images and preimages, injectivity, surjectivity, bijectivity, composition, and inverse bijections.

This is a foundation milestone, not a claim that all course material is complete. Infinite sets and symbolic real-variable or piecewise-function calculations are not enumerated by this finite engine. The set-theory workspace still needs to be connected to these operations in QML.

## Run the application

```bash
python -m pip install -r requirements.txt
python main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

The project is being developed against the supplied university topology course chapters. Mathematical coverage is expanded incrementally and verified with tests.
