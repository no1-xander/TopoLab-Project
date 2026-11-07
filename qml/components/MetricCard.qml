import QtQuick
import QtQuick.Layouts
import "../theme/Palette.js" as Palette

Rectangle {
    id: root

    property string eyebrow: "LABEL"
    property string value: "—"
    property string detail: "Description"
    property string glyph: "◈"
    property color accent: Palette.cyan

    Layout.fillWidth: true
    Layout.preferredHeight: 128
    radius: 16
    color: Palette.panel
    border.width: 1
    border.color: Palette.border

    Rectangle {
        width: 3
        height: 62
        radius: 2
        anchors.left: parent.left
        anchors.leftMargin: 1
        anchors.verticalCenter: parent.verticalCenter
        color: root.accent
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.leftMargin: 18
        anchors.rightMargin: 16
        anchors.topMargin: 15
        anchors.bottomMargin: 14
        spacing: 5

        RowLayout {
            Layout.fillWidth: true
            Text {
                text: root.eyebrow.toUpperCase()
                color: Palette.textSecondary
                font.family: Palette.uiFont
                font.pixelSize: 10
                font.letterSpacing: 1.1
                font.weight: Font.DemiBold
            }
            Item { Layout.fillWidth: true }
            Text {
                text: root.glyph
                color: root.accent
                font.family: Palette.uiFont
                font.pixelSize: 19
            }
        }

        Text {
            text: root.value
            color: Palette.textPrimary
            font.family: Palette.displayFont
            font.pixelSize: 28
            font.weight: Font.Medium
        }

        Text {
            text: root.detail
            color: Palette.textSecondary
            font.family: Palette.uiFont
            font.pixelSize: 12
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }
    }
}
