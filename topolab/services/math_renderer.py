"""Render LaTeX-style mathematical expressions for the Qt Quick interface.

The renderer uses Matplotlib MathText. MathText supports a substantial TeX-like
math subset and its bundled STIX fonts, but it is not a complete LaTeX engine.
The expressions used in TopoLab's Chapter 1 and Chapter 2 screens are covered
by this renderer. If later course material needs unsupported LaTeX packages or
macros, the renderer can be replaced without changing the QML components.
"""

from __future__ import annotations

import hashlib
import sys
from io import BytesIO
from pathlib import Path

import matplotlib

# Use Matplotlib's non-interactive renderer: no plotting window is created.
matplotlib.use("Agg")
matplotlib.rcParams.update(
    {
        "mathtext.fontset": "stix",
        "figure.facecolor": "none",
        "savefig.facecolor": "none",
        "savefig.edgecolor": "none",
        "savefig.transparent": True,
    }
)

from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import math_to_image
from PySide6.QtCore import QObject, QStandardPaths, QUrl, Slot
from PySide6.QtGui import QColor


class MathRenderer(QObject):
    """Create cached, transparent PNGs for mathematical expressions.

    QML calls ``render(expression, point_size, color)`` and receives a local
    file URL. The output is rendered at high DPI so it stays crisp when scaled
    on high-resolution displays.
    """

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        cache_root = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.CacheLocation
        )
        if not cache_root:
            cache_root = str(Path.home() / ".cache" / "TopoLab")
        self._cache_directory = Path(cache_root) / "math"
        self._cache_directory.mkdir(parents=True, exist_ok=True)

    @Slot(str, int, str, result=str)
    def render(self, expression: str, point_size: int = 22, color: str = "#F8EDE4") -> str:
        """Return a local PNG URL for a TeX-style math expression."""
        source = expression.strip()
        if not source:
            return ""

        # Accept either a raw expression or an expression already wrapped in $.
        if not (source.startswith("$") and source.endswith("$")):
            source = f"${source}$"

        point_size = max(10, min(int(point_size), 48))
        parsed_color = QColor(color)
        if not parsed_color.isValid():
            parsed_color = QColor("#F8EDE4")
        color_hex = parsed_color.name()

        cache_key = hashlib.sha256(
            f"{source}|{point_size}|{color_hex}|stix|192".encode("utf-8")
        ).hexdigest()
        output_path = self._cache_directory / f"{cache_key}.png"

        if not output_path.exists():
            try:
                image_data = BytesIO()
                math_to_image(
                    source,
                    image_data,
                    prop=FontProperties(size=point_size),
                    dpi=192,
                    format="png",
                    color=color_hex,
                )
                output_path.write_bytes(image_data.getvalue())
            except Exception as exc:  # Keep an unsupported formula from closing the app.
                print(
                    f"TopoLab could not render this math expression: {source}\n{exc}",
                    file=sys.stderr,
                )
                return ""

        return QUrl.fromLocalFile(str(output_path)).toString()
