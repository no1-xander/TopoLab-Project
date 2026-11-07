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
            spacing: 19

            PageHeading {
                Layout.fillWidth: true
                eyebrow: "MATHEMATICAL WORKSPACE / 03"
                title: "Proof laboratory"
                description: "A place for definitions, theorem statements, and transparent reasoning. The first proof templates will follow Exercise 7."
            }

            Repeater {
                model: [
                    {tag: "INTERIOR", formula: "\\operatorname{int}(A)=\\bigcup_{U\\in\\tau,\ U\\subseteq A}U", note: "The interior is the largest open subset contained in A."},
                    {tag: "CLOSURE", formula: "\\overline{A}=\\bigcap_{F\\supseteq A,\ F\\text{ closed}}F", note: "The closure is the smallest closed set containing A."},
                    {tag: "COMPLEMENT", formula: "\\operatorname{int}(X\\setminus A)=X\\setminus\\overline{A}", note: "Connect interior and closure through complements."},
                    {tag: "ACCUMULATION", formula: "\\overline{A}=A\\cup A^{\\prime}", note: "Separate points in A from accumulation points."},
                    {tag: "BOUNDARY", formula: "\\partial A=\\overline{A}\\setminus\\operatorname{int}(A)", note: "Compare the closure with the interior."}
                ]
                delegate: PanelCard {
                    required property var modelData
                    Layout.fillWidth: true
                    Layout.preferredHeight: 143
                    padding: 18
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 8
                        Text {
                            text: modelData.tag
                            color: Palette.cyan
                            font.family: Palette.uiFont
                            font.pixelSize: 11
                            font.letterSpacing: 1.2
                            font.weight: Font.Bold
                        }
                        MathFormula {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 42
                            expression: modelData.formula
                            pointSize: 20
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
    }
}
