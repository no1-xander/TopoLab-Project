import QtQuick
import "../theme/Palette.js" as Palette

Item {
    id: root

    property string label: "Navigation item"
    property string glyph: "•"
    property bool active: false
    signal activated()

    implicitWidth: 224
    implicitHeight: 49
    opacity: enabled ? 1.0 : 0.48

    Rectangle {
        id: surface
        anchors.fill: parent
        radius: 12
        color: root.active ? "#493026" : (mouseArea.containsMouse && root.enabled ? "#302019" : "transparent")
        border.width: root.active ? 1 : 0
        border.color: root.active ? "#80513D" : "transparent"

        Rectangle {
            width: 3
            height: 25
            radius: 2
            anchors.left: parent.left
            anchors.leftMargin: 1
            anchors.verticalCenter: parent.verticalCenter
            color: Palette.cyan
            visible: root.active
        }

        Row {
            anchors.fill: parent
            anchors.leftMargin: 15
            anchors.rightMargin: 12
            spacing: 13

            Text {
                width: 24
                anchors.verticalCenter: parent.verticalCenter
                text: root.glyph
                color: root.active ? Palette.cyan : Palette.textSecondary
                font.family: Palette.uiFont
                font.pixelSize: 20
                horizontalAlignment: Text.AlignHCenter
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: root.label
                color: root.active ? Palette.textPrimary : Palette.textSecondary
                font.family: Palette.uiFont
                font.pixelSize: 14
                font.weight: root.active ? Font.DemiBold : Font.Medium
            }

            Item { width: 1; height: 1 }
        }

        Behavior on color { ColorAnimation { duration: 150 } }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        enabled: root.enabled
        cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: root.activated()
    }
}
