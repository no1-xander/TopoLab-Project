import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../theme/Palette.js" as Palette
import "../components"

Item {
    id: root
    property var metricResult: ({})

    function calculateMetric() {
        metricResult = metricController.analyzeMetric(
            pointsField.text,
            distancesField.text,
            centerField.text,
            radiusField.text
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
                eyebrow: "CHAPTER 02 / METRIC SPACES"
                title: "Metric laboratory"
                description: "Enter a finite distance table, verify the metric axioms, and calculate open and closed balls and the induced topology."
            }

            PanelCard {
                Layout.fillWidth: true
                padding: 20
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 12

                    Text {
                        text: "01 / UNDERLYING SET"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.1
                    }
                    TextField {
                        id: pointsField
                        Layout.fillWidth: true
                        text: "a, b, c"
                        placeholderText: "a, b, c"
                        selectByMouse: true
                    }

                    Text {
                        text: "02 / DISTANCE TABLE"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.1
                    }
                    Text {
                        Layout.fillWidth: true
                        text: "Enter every ordered pair exactly once, one per line: x, y, d(x,y). The table must include both d(x,y) and d(y,x)."
                        color: Palette.textSecondary
                        font.family: Palette.uiFont
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                    TextArea {
                        id: distancesField
                        Layout.fillWidth: true
                        Layout.preferredHeight: 210
                        text: "a, a, 0\na, b, 1\na, c, 1\nb, a, 1\nb, b, 0\nb, c, 1\nc, a, 1\nc, b, 1\nc, c, 0"
                        selectByMouse: true
                        wrapMode: TextEdit.NoWrap
                        color: Palette.textPrimary
                        font.family: "Consolas"
                        font.pixelSize: 13
                        background: Rectangle {
                            color: Palette.sidebar
                            radius: 9
                            border.color: distancesField.activeFocus ? Palette.cyan : Palette.border
                            border.width: 1
                        }
                    }

                    GridLayout {
                        Layout.fillWidth: true
                        columns: width > 620 ? 2 : 1
                        columnSpacing: 14
                        rowSpacing: 10
                        ColumnLayout {
                            Layout.fillWidth: true
                            Text {
                                text: "BALL CENTRE"
                                color: Palette.textSecondary
                                font.family: Palette.uiFont
                                font.pixelSize: 10
                                font.weight: Font.Bold
                            }
                            TextField {
                                id: centerField
                                Layout.fillWidth: true
                                text: "a"
                                placeholderText: "a"
                                selectByMouse: true
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            Text {
                                text: "RADIUS r > 0"
                                color: Palette.textSecondary
                                font.family: Palette.uiFont
                                font.pixelSize: 10
                                font.weight: Font.Bold
                            }
                            TextField {
                                id: radiusField
                                Layout.fillWidth: true
                                text: "1"
                                placeholderText: "1"
                                selectByMouse: true
                            }
                        }
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        Button {
                            text: "Verify metric and calculate"
                            highlighted: true
                            onClicked: root.calculateMetric()
                        }
                        Button {
                            text: "Reset discrete example"
                            onClicked: {
                                pointsField.text = "a, b, c"
                                distancesField.text = "a, a, 0\na, b, 1\na, c, 1\nb, a, 1\nb, b, 0\nb, c, 1\nc, a, 1\nc, b, 1\nc, c, 0"
                                centerField.text = "a"
                                radiusField.text = "1"
                                root.calculateMetric()
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
                    Text {
                        text: "03 / AXIOM VERIFICATION"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.1
                    }
                    Text {
                        Layout.fillWidth: true
                        text: root.metricResult.message || "Run the verification to inspect the result."
                        color: root.metricResult.ok ? Palette.success : Palette.textSecondary
                        font.family: Palette.uiFont
                        font.pixelSize: 13
                        wrapMode: Text.WordWrap
                    }
                    Text {
                        Layout.fillWidth: true
                        visible: root.metricResult.ok === false && (root.metricResult.errors || []).length > 0
                        text: (root.metricResult.errors || []).join("\n")
                        color: Palette.warning
                        font.family: Palette.uiFont
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                    Text {
                        Layout.fillWidth: true
                        visible: root.metricResult.ok === true
                        text: "M1 checks: " + root.metricResult.separationChecks
                              + "    M2 checks: " + root.metricResult.symmetryChecks
                              + "    M3 checks: " + root.metricResult.triangleChecks
                        color: Palette.textSecondary
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                    }
                }
            }

            PanelCard {
                Layout.fillWidth: true
                padding: 20
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 11
                    Text {
                        text: "04 / METRIC BALLS"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.1
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        ColumnLayout {
                            Layout.fillWidth: true
                            Text { text: "OPEN BALL"; color: Palette.textSecondary; font.family: Palette.uiFont; font.pixelSize: 10; font.weight: Font.Bold }
                            Text { text: root.metricResult.openBall || "—"; color: Palette.textPrimary; font.family: Palette.displayFont; font.pixelSize: 18 }
                            MathFormula { Layout.fillWidth: true; Layout.preferredHeight: 32; expression: "d(x,y)<r"; pointSize: 16 }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            Text { text: "CLOSED BALL"; color: Palette.textSecondary; font.family: Palette.uiFont; font.pixelSize: 10; font.weight: Font.Bold }
                            Text { text: root.metricResult.closedBall || "—"; color: Palette.textPrimary; font.family: Palette.displayFont; font.pixelSize: 18 }
                            MathFormula { Layout.fillWidth: true; Layout.preferredHeight: 32; expression: "d(x,y)\\leq r"; pointSize: 16 }
                        }
                    }
                }
            }

            PanelCard {
                Layout.fillWidth: true
                padding: 20
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 9
                    Text {
                        text: "05 / INDUCED METRIC TOPOLOGY"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.1
                    }
                    Text {
                        Layout.fillWidth: true
                        visible: root.metricResult.ok === true
                        text: "For a finite metric space, each singleton is open. Therefore the induced metric topology is the discrete topology P(X)."
                        color: Palette.textSecondary
                        font.family: Palette.uiFont
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                    Repeater {
                        model: root.metricResult.metricTopology || []
                        delegate: Text {
                            required property string modelData
                            Layout.fillWidth: true
                            text: modelData
                            color: Palette.textPrimary
                            font.family: Palette.displayFont
                            font.pixelSize: 14
                        }
                    }
                    Text {
                        Layout.fillWidth: true
                        visible: root.metricResult.ok === true
                        text: root.metricResult.epsilonNetNote || ""
                        color: Palette.success
                        font.family: Palette.uiFont
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }
    }
}
