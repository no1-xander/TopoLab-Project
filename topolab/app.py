"""Create and run the TopoLab Qt Quick application."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QFont, QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from topolab.services.math_renderer import MathRenderer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QML_ENTRY_POINT = PROJECT_ROOT / "qml" / "Main.qml"


def main() -> int:
    """Start TopoLab and return the Qt event-loop exit code."""
    if not QML_ENTRY_POINT.is_file():
        print(f"ERROR: Could not find the QML entry point: {QML_ENTRY_POINT}")
        return 1

    app = QGuiApplication(sys.argv)
    app.setApplicationName("TopoLab")
    app.setOrganizationName("TopoLab")
    app.setApplicationVersion("0.1.1")

    # Segoe UI is a clear, modern Windows UI font. Mathematical expressions
    # use a separate STIX serif renderer through MathFormula.qml.
    ui_font = QFont("Segoe UI")
    ui_font.setPointSize(10)
    app.setFont(ui_font)

    engine = QQmlApplicationEngine()
    math_renderer = MathRenderer()
    engine.rootContext().setContextProperty("mathRenderer", math_renderer)
    engine.load(QUrl.fromLocalFile(str(QML_ENTRY_POINT)))

    if not engine.rootObjects():
        print("ERROR: Qt could not load qml/Main.qml. Check the QML errors above.")
        return 1

    return app.exec()
