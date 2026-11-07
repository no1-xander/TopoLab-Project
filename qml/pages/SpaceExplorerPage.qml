import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../theme/Palette.js" as Palette
import "../components"

Item {
    ScrollView {
        anchors.fill: parent
        clip: true
        contentWidth: availableWidth
        ScrollBar.vertical.policy: ScrollBar.AsNeeded

        ColumnLayout {
            width: parent.width
            spacing: 20

            PageHeading {
                Layout.fillWidth: true
                eyebrow: "MATHEMATICAL WORKSPACE / 01"
                title: "Space explorer"
                description: "Define the underlying set and the proposed family of open sets. The next milestone will add topology validation and editable set input."
            }

            PanelCard {
                Layout.fillWidth: true
                Layout.preferredHeight: 236
                padding: 20
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 10
                    Text {
                        text: "SPACE DEFINITION"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.letterSpacing: 1.3
                        font.weight: Font.Bold
                    }
                    Text {
                        text: "Start with the underlying set X"
                        color: Palette.textPrimary
                        font.family: Palette.uiFont
                        font.pixelSize: 18
                        font.weight: Font.DemiBold
                    }
                    Text { text: "Example format"; color: Palette.textSecondary; font.pixelSize: 12 }
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 57
                        radius: 11
                        color: Palette.sidebar
                        border.color: Palette.border
                        border.width: 1
                        MathFormula {
                            anchors.fill: parent
                            anchors.leftMargin: 16
                            expression: "X = \\{a,b,c\\}"
                            pointSize: 23
                            formulaColor: Palette.parchment
                            centered: false
                        }
                    }
                    Text {
                        text: "Input controls will be connected to the Python finite-space model after the interface foundation is approved."
                        color: Palette.textSecondary
                        font.pixelSize: 13
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                }
            }

            PanelCard {
                Layout.fillWidth: true
                Layout.preferredHeight: 181
                padding: 20
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 10
                    Text {
                        text: "TOPOLOGY FAMILY"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.letterSpacing: 1.3
                        font.weight: Font.Bold
                    }
                    MathFormula {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 43
                        expression: "\\tau = \\{\\varnothing, \\{a\\}, \\{a,b\\}, X\\}"
                        pointSize: 23
                    }
                    Text {
                        text: "A topology is not accepted merely because it is a list of subsets. It must satisfy the three topology axioms from your Chapter 2 material."
                        color: Palette.textSecondary
                        font.pixelSize: 13
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                }
            }
        }
    }
}
