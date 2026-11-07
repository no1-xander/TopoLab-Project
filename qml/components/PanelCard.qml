import QtQuick
import "../theme/Palette.js" as Palette

Rectangle {
    id: root

    property int padding: 18
    property color surfaceColor: Palette.panel
    property color outlineColor: Palette.border
    default property alias contentData: content.data

    radius: 17
    color: surfaceColor
    border.width: 1
    border.color: outlineColor

    Item {
        id: content
        anchors.fill: parent
        anchors.margins: root.padding
    }
}
