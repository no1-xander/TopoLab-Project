
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../theme/Palette.js" as Palette

Item {
    id: root

    // The input field currently receiving mathematical symbols.
    property var targetField: null

    property string selectedCategory: "Sets"

    property var categories: ["Sets", "Editing"]

    property var symbolGroups: ({
        "Sets": ["∅", "{", "}", ",", "X"],
        "Editing": ["⌫", "Clear"]
    })

    implicitHeight: keyboardLayout.implicitHeight

    function handleKey(value) {
        if (targetField === null)
            return

        if (value === "Clear") {
            targetField.clear()
            return
        }

        if (value === "⌫") {
            if (targetField.selectedText.length > 0) {
                var start = targetField.selectionStart
                var end = targetField.selectionEnd

                targetField.remove(start, end)
                targetField.cursorPosition = start
            } else if (targetField.cursorPosition > 0) {
                var position = targetField.cursorPosition

                targetField.remove(position - 1, position)
                targetField.cursorPosition = position - 1
            }

            return
        }

        // Replace selected text before inserting the new symbol.
        if (targetField.selectedText.length > 0) {
            var selectionStart = targetField.selectionStart
            var selectionEnd = targetField.selectionEnd

            targetField.remove(selectionStart, selectionEnd)
            targetField.cursorPosition = selectionStart
        }

        targetField.insert(targetField.cursorPosition, value)
    }

    Rectangle {
        anchors.fill: parent
        radius: 14
        color: Palette.panel
        border.color: Palette.border
        border.width: 1
    }

    ColumnLayout {
        id: keyboardLayout

        anchors.fill: parent
        anchors.margins: 14
        spacing: 12

        RowLayout {
            Layout.fillWidth: true

            Text {
                text: "MATHPAD"
                color: Palette.textPrimary
                font.family: Palette.uiFont
                font.pixelSize: 12
                font.weight: Font.Bold
                font.letterSpacing: 1.2
            }

            Item {
                Layout.fillWidth: true
            }

            Text {
                text: "MATHEMATICAL INPUT"
                color: Palette.textSecondary
                font.pixelSize: 10
                font.letterSpacing: 0.8
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 7

            Repeater {
                model: root.categories

                delegate: Button {
                    required property string modelData

                    Layout.fillWidth: true
                    Layout.preferredHeight: 34

                    text: modelData
                    flat: true

                    onClicked: {
                        root.selectedCategory = modelData
                    }

                    contentItem: Text {
                        text: parent.text
                        color: root.selectedCategory === modelData
                               ? Palette.parchment
                               : Palette.textSecondary
                        font.family: Palette.uiFont
                        font.pixelSize: 12
                        font.weight: Font.DemiBold
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8
                        color: root.selectedCategory === modelData
                               ? Palette.terracotta
                               : Palette.panelRaised
                        border.color: Palette.border
                        border.width: 1
                    }
                }
            }
        }

        GridLayout {
            Layout.fillWidth: true
            columns: 6
            rowSpacing: 7
            columnSpacing: 7

            Repeater {
                model: root.symbolGroups[root.selectedCategory]

                delegate: Button {
                    required property string modelData

                    Layout.fillWidth: true
                    Layout.preferredHeight: 42

                    text: modelData
                    enabled: root.targetField !== null

                    onClicked: root.handleKey(modelData)

                    contentItem: Text {
                        text: parent.text
                        color: Palette.textPrimary
                        font.family: Palette.displayFont
                        font.pixelSize: 19
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        radius: 8
                        color: parent.down
                               ? Palette.terracotta
                               : Palette.panelRaised
                        border.color: Palette.border
                        border.width: 1
                    }
                }
            }
        }

        Text {
            Layout.fillWidth: true
            text: root.targetField === null
                  ? "Select an input field to use MathPad."
                  : "Choose a symbol to insert it at the cursor."
            color: Palette.textSecondary
            font.family: Palette.uiFont
            font.pixelSize: 11
            wrapMode: Text.WordWrap
        }
    }
}
