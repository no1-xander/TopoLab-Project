import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../theme/Palette.js" as Palette
import "../components"

Item {
    id: root
    property var operationFormulas: [
        "A \\cup B", "A \\cap B", "A \\setminus B",
        "E \\setminus A", "\\mathcal{P}(A)", "A \\times B",
        "A \\subseteq B", "A = B", "A \\cap B = \\varnothing"
    ]
    property var resultData: ({
        "ok": false, "result": "",
        "message": "Choose an operation and calculate.", "explanation": ""
    })

    function runCalculation() {
        resultData = setController.calculate(
            operationBox.currentIndex, firstSetField.text,
            secondSetField.text, universeField.text
        )
    }

    ScrollView {
        anchors.fill: parent
        clip: true
        contentWidth: availableWidth
        ScrollBar.vertical.policy: ScrollBar.AsNeeded
        ColumnLayout {
            width: parent.width
            spacing: 18

            PageHeading {
                Layout.fillWidth: true
                eyebrow: "CHAPTER 01 / INTERACTIVE WORKSPACE"
                title: "Set theory toolkit"
                description: "Calculate finite set operations directly with the Chapter 1 mathematical engine. Enter elements separated by commas, for example: a, b, c."
            }

            PanelCard {
                Layout.fillWidth: true
                padding: 20
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 14
                    Text {
                        text: "OPERATION"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.2
                    }
                    ComboBox {
                        id: operationBox
                        Layout.fillWidth: true
                        model: [
                            "Union  ·  A ∪ B",
                            "Intersection  ·  A ∩ B",
                            "Difference  ·  A \\ B",
                            "Complement  ·  E \\ A",
                            "Power set  ·  P(A)",
                            "Cartesian product  ·  A × B",
                            "Subset test  ·  A ⊆ B",
                            "Equality test  ·  A = B",
                            "Disjointness test"
                        ]
                        onCurrentIndexChanged: root.resultData = ({
                            "ok": false, "result": "",
                            "message": "Press Calculate to run the selected operation.",
                            "explanation": ""
                        })
                    }
                    MathFormula {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 48
                        expression: root.operationFormulas[operationBox.currentIndex] || ""
                        pointSize: 25
                        formulaColor: Palette.cyan
                    }
                    GridLayout {
                        Layout.fillWidth: true
                        columns: width > 680 ? 2 : 1
                        columnSpacing: 14
                        rowSpacing: 12
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 6
                            Text {
                                text: "SET A"
                                color: Palette.textSecondary
                                font.family: Palette.uiFont
                                font.pixelSize: 11
                                font.weight: Font.DemiBold
                            }
                            TextField {
                                id: firstSetField
                                Layout.fillWidth: true
                                text: "a, b"
                                placeholderText: "a, b, c"
                                selectByMouse: true
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            visible: operationBox.currentIndex !== 3
                                     && operationBox.currentIndex !== 4
                            spacing: 6
                            Text {
                                text: "SET B"
                                color: Palette.textSecondary
                                font.family: Palette.uiFont
                                font.pixelSize: 11
                                font.weight: Font.DemiBold
                            }
                            TextField {
                                id: secondSetField
                                Layout.fillWidth: true
                                text: "b, c"
                                placeholderText: "b, c"
                                selectByMouse: true
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            visible: operationBox.currentIndex === 3
                            spacing: 6
                            Text {
                                text: "UNIVERSE E"
                                color: Palette.textSecondary
                                font.family: Palette.uiFont
                                font.pixelSize: 11
                                font.weight: Font.DemiBold
                            }
                            TextField {
                                id: universeField
                                Layout.fillWidth: true
                                text: "a, b, c, d"
                                placeholderText: "a, b, c, d"
                                selectByMouse: true
                            }
                        }
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        Button {
                            text: "Calculate"
                            highlighted: true
                            onClicked: root.runCalculation()
                        }
                        Button {
                            text: "Reset example"
                            onClicked: {
                                firstSetField.text = "a, b"
                                secondSetField.text = "b, c"
                                universeField.text = "a, b, c, d"
                                operationBox.currentIndex = 0
                                root.runCalculation()
                            }
                        }
                    }
                }
            }

            PanelCard {
                Layout.fillWidth: true
                padding: 20
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 10
                    RowLayout {
                        Layout.fillWidth: true
                        Text {
                            text: "RESULT"
                            color: Palette.cyan
                            font.family: Palette.uiFont
                            font.pixelSize: 11
                            font.weight: Font.Bold
                            font.letterSpacing: 1.2
                        }
                        Item { Layout.fillWidth: true }
                        Rectangle {
                            radius: 8
                            color: root.resultData.ok ? Palette.cyanSoft : Palette.panelRaised
                            implicitWidth: statusLabel.implicitWidth + 18
                            implicitHeight: statusLabel.implicitHeight + 8
                            Text {
                                id: statusLabel
                                anchors.centerIn: parent
                                text: root.resultData.ok ? "CALCULATED" : "READY"
                                color: root.resultData.ok ? Palette.success : Palette.textSecondary
                                font.family: Palette.uiFont
                                font.pixelSize: 9
                                font.weight: Font.Bold
                            }
                        }
                    }
                    Text {
                        Layout.fillWidth: true
                        text: root.resultData.message || ""
                        color: root.resultData.ok ? Palette.success : Palette.warning
                        font.family: Palette.uiFont
                        font.pixelSize: 13
                        wrapMode: Text.WordWrap
                    }
                    TextArea {
                        Layout.fillWidth: true
                        Layout.preferredHeight: Math.max(110, contentHeight + 28)
                        readOnly: true
                        selectByMouse: true
                        wrapMode: TextEdit.Wrap
                        text: root.resultData.result || "Your result will appear here."
                        color: Palette.textPrimary
                        font.family: Palette.uiFont
                        font.pixelSize: 14
                        background: Rectangle {
                            color: Palette.sidebar
                            radius: 10
                            border.color: Palette.border
                            border.width: 1
                        }
                    }
                    Text {
                        Layout.fillWidth: true
                        visible: (root.resultData.explanation || "").length > 0
                        text: root.resultData.explanation || ""
                        color: Palette.textSecondary
                        font.family: Palette.uiFont
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                }
            }

            PanelCard {
                Layout.fillWidth: true
                padding: 16
                Text {
                    Layout.fillWidth: true
                    text: "Scope note: this workspace currently computes finite sets whose elements are simple labels. It does not enumerate infinite sets, intervals, or symbolic expressions. The power-set and Cartesian-product views include size limits to keep the interface responsive."
                    color: Palette.parchmentMuted
                    font.family: Palette.uiFont
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                }
            }
        }
    }
}
