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
                eyebrow: "MATHEMATICAL WORKSPACE / 02"
                title: "Set theory toolkit"
                description: "The shared set operations used throughout the topology course. This page is the UI shell; calculation controls will be wired to Python in the next milestone."
            }

            GridLayout {
                Layout.fillWidth: true
                columns: width > 760 ? 2 : 1
                columnSpacing: 14
                rowSpacing: 14

                Repeater {
                    model: [
                        {formula: "A \\cup B", title: "Union", note: "Elements belonging to A or B."},
                        {formula: "A \\cap B", title: "Intersection", note: "Elements common to A and B."},
                        {formula: "A \\setminus B", title: "Difference", note: "Elements in A that are not in B."},
                        {formula: "A^{c}", title: "Complement", note: "Elements of the universe outside A."},
                        {formula: "\\mathcal{P}(X)", title: "Power set", note: "The family of every subset of X."},
                        {formula: "A \\times B", title: "Cartesian product", note: "Ordered pairs with first and second coordinates."}
                    ]
                    delegate: PanelCard {
                        required property var modelData
                        Layout.fillWidth: true
                        Layout.preferredHeight: 151
                        padding: 18
                        ColumnLayout {
                            anchors.fill: parent
                            spacing: 8
                            MathFormula {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 43
                                expression: modelData.formula
                                pointSize: 25
                                formulaColor: Palette.cyan
                            }
                            Text {
                                text: modelData.title
                                color: Palette.textPrimary
                                font.family: Palette.uiFont
                                font.pixelSize: 15
                                font.weight: Font.DemiBold
                            }
                            Text {
                                text: modelData.note
                                color: Palette.textSecondary
                                font.family: Palette.uiFont
                                font.pixelSize: 13
                                wrapMode: Text.WordWrap
                                Layout.fillWidth: true
                            }
                        }
                    }
                }
            }

            PanelCard {
                Layout.fillWidth: true
                Layout.preferredHeight: 112
                padding: 18
                Text {
                    anchors.fill: parent
                    verticalAlignment: Text.AlignVCenter
                    text: "Design rule: sets will be represented consistently in the Python core, so the same operations can be reused by every topology module."
                    color: Palette.parchmentMuted
                    font.family: Palette.uiFont
                    font.pixelSize: 13
                    wrapMode: Text.WordWrap
                }
            }
        }
    }
}
