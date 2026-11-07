import QtQuick
import "../theme/Palette.js" as Palette

// Displays a TeX-style expression as a high-resolution, transparent image.
// Example: MathFormula { expression: "\\overline{A} = A \\cup A^{\\prime}" }
Item {
    id: root

    property string expression: ""
    property int pointSize: Palette.formulaSize
    property color formulaColor: Palette.textPrimary
    property bool centered: false

    property string renderedSource: root.expression.length > 0
                                     ? mathRenderer.render(root.expression, root.pointSize, root.formulaColor.toString())
                                     : ""

    implicitWidth: formulaImage.implicitWidth + 4
    implicitHeight: Math.max(pointSize * 1.8, formulaImage.implicitHeight + 8)

    Image {
        id: formulaImage
        anchors.fill: parent
        source: root.renderedSource
        fillMode: Image.PreserveAspectFit
        horizontalAlignment: root.centered ? Image.AlignHCenter : Image.AlignLeft
        verticalAlignment: Image.AlignVCenter
        smooth: true
        mipmap: true
    }

    Text {
        anchors.centerIn: parent
        visible: root.expression.length > 0 && root.renderedSource.length === 0
        text: "Formula could not be rendered"
        color: Palette.warning
        font.family: Palette.uiFont
        font.pixelSize: 11
    }
}
