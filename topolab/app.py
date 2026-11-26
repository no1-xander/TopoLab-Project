
"""Create and run the TopoLab Qt Quick application."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QFont, QFontDatabase, QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from topolab.services.math_renderer import MathRenderer
from topolab.services.topology_controller import TopologyController
from topolab.services.basis_controller import BasisController

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QML_ENTRY_POINT = PROJECT_ROOT / "qml" / "Main.qml"
FONT_DIRECTORY = PROJECT_ROOT / "assets" / "fonts"


def load_application_fonts() -> None:
    """Register the fonts bundled with TopoLab."""
    font_files = [
        "Newsreader_14pt-Regular.ttf",
        "Newsreader_14pt-Bold.ttf",
        "PlusJakartaSans-Regular.ttf",
        "PlusJakartaSans-Bold.ttf",
    ]

    for filename in font_files:
        font_path = FONT_DIRECTORY / filename

        if not font_path.is_file():
            print(f"WARNING: Font file not found: {font_path}")
            continue

        font_id = QFontDatabase.addApplicationFont(str(font_path))

        if font_id == -1:
            print(f"WARNING: Could not load font: {filename}")


def main() -> int:
    """Start TopoLab and return the Qt event-loop exit code."""
    if not QML_ENTRY_POINT.is_file():
        print(f"ERROR: Could not find the QML entry point: {QML_ENTRY_POINT}")
        return 1

    app = QGuiApplication(sys.argv)
    app.setApplicationName("TopoLab")
    app.setOrganizationName("TopoLab")
    app.setApplicationVersion("0.1.1")

    load_application_fonts()

    ui_font = QFont("Plus Jakarta Sans")
    ui_font.setPointSize(10)
    app.setFont(ui_font)

    engine = QQmlApplicationEngine()
    math_renderer = MathRenderer()
    topology_controller = TopologyController()
    basis_controller = BasisController()

    engine.rootContext().setContextProperty("mathRenderer", math_renderer)
    engine.rootContext().setContextProperty(
        "topologyController", topology_controller
)
    engine.rootContext().setContextProperty(
        "basisController", basis_controller
)
    engine.load(QUrl.fromLocalFile(str(QML_ENTRY_POINT)))

    if not engine.rootObjects():
        print("ERROR: Qt could not load qml/Main.qml. Check the QML errors above.")
        return 1

    return app.exec()
