import QtQuick
import "../theme/Palette.js" as Palette

Item {
    id: root

    property string label: "Continue"
    property bool primary: false
    property bool compact: false
    property bool enabled: true
    signal clicked()

    implicitWidth: buttonText.implicitWidth + (compact ? 30 : 42)
    implicitHeight: compact ? 38 : 46
    opacity: enabled ? 1.0 : 0.5

    Rectangle {
        id: surface
        anchors.fill: parent
        radius: 11
        color: root.primary
               ? (mouseArea.pressed ? Palette.terracotta : Palette.terracottaBright)
               : (mouseArea.containsMouse ? Palette.panelRaised : Palette.panel)
        border.width: root.primary ? 0 : 1
        border.color: Palette.border
        scale: mouseArea.pressed ? 0.98 : 1.0

        Text {
            id: buttonText
            anchors.centerIn: parent
            text: root.label
            color: Palette.textPrimary
            font.family: Palette.uiFont
            font.pixelSize: root.compact ? 12 : 14
            font.weight: Font.DemiBold
        }

        Behavior on color { ColorAnimation { duration: 130 } }
        Behavior on scale { NumberAnimation { duration: 90 } }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        enabled: root.enabled
        cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: root.clicked()
    }
}
