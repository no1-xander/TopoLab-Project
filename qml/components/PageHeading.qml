import QtQuick
import QtQuick.Layouts
import "../theme/Palette.js" as Palette

ColumnLayout {
    id: root
    property string eyebrow: "TOPOLAB WORKSPACE"
    property string title: "Page title"
    property string description: "A short explanation of this area."
    spacing: 8

    Text {
        text: root.eyebrow.toUpperCase()
        color: Palette.cyan
        font.family: Palette.uiFont
        font.pixelSize: 11
        font.letterSpacing: 1.6
        font.weight: Font.DemiBold
        Layout.fillWidth: true
    }
    Text {
        text: root.title
        color: Palette.textPrimary
        font.family: Palette.displayFont
        font.pixelSize: 31
        font.weight: Font.Medium
        lineHeight: 1.12
        wrapMode: Text.WordWrap
        Layout.fillWidth: true
    }
    Text {
        text: root.description
        color: Palette.textSecondary
        font.family: Palette.uiFont
        font.pixelSize: 14
        lineHeight: 1.18
        wrapMode: Text.WordWrap
        Layout.fillWidth: true
    }
}
