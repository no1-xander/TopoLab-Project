import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../theme/Palette.js" as Palette
import "../components"

Item {
    id: root

    ScrollView {
        id: scroll
        anchors.fill: parent
        clip: true
        contentWidth: availableWidth
        ScrollBar.vertical.policy: ScrollBar.AsNeeded

        ColumnLayout {
            width: scroll.availableWidth
            spacing: 20

            RowLayout {
                Layout.fillWidth: true
                Layout.topMargin: 3
                spacing: 18

                PageHeading {
                    Layout.fillWidth: true
                    eyebrow: "YOUR MATHEMATICAL WORKSPACE"
                    title: "Explore the structure of spaces."
                    description: "Build a space, inspect its topology, and follow each result back to its definition."
                }

                Rectangle {
                    Layout.preferredWidth: 174
                    Layout.preferredHeight: 42
                    radius: 11
                    color: Palette.cyanSoft
                    border.width: 1
                    border.color: "#287485"
                    Row {
                        anchors.centerIn: parent
                        spacing: 8
                        Rectangle {
                            width: 7; height: 7; radius: 4
                            anchors.verticalCenter: parent.verticalCenter
                            color: Palette.success
                        }
                        Text {
                            text: "LOCAL WORKSPACE"
                            color: Palette.parchment
                            font.pixelSize: 11
                            font.letterSpacing: 0.8
                            font.weight: Font.DemiBold
                        }
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 12
                MetricCard {
                    eyebrow: "COURSE FOUNDATION"
                    value: "02 chapters"
                    detail: "Set theory and topological spaces"
                    glyph: "∑"
                    accent: Palette.terracottaBright
                }
                MetricCard {
                    eyebrow: "EXERCISE TARGETS"
                    value: "10 exercises"
                    detail: "Mapped from Exercise Sheet No. 1"
                    glyph: "⌘"
                    accent: Palette.cyan
                }
                MetricCard {
                    eyebrow: "BUILD STATUS"
                    value: "UI milestone"
                    detail: "Mathematical engine comes next"
                    glyph: "◷"
                    accent: Palette.warning
                }
            }

            GridLayout {
                Layout.fillWidth: true
                columns: width >= 900 ? 2 : 1
                columnSpacing: 14
                rowSpacing: 14

                PanelCard {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 360
                    padding: 19

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 11

                        RowLayout {
                            Layout.fillWidth: true
                            ColumnLayout {
                                spacing: 3
                                Text {
                                    text: "INCLUSION DIAGRAM"
                                    color: Palette.textPrimary
                                    font.pixelSize: 14
                                    font.weight: Font.DemiBold
                                    font.letterSpacing: 0.5
                                }
                                Text {
                                    text: "Sample on X = {a, b, c} · not an input yet"
                                    color: Palette.textSecondary
                                    font.pixelSize: 12
                                }
                            }
                            Item { Layout.fillWidth: true }
                            Rectangle {
                                radius: 8
                                color: "#4A2B20"
                                border.color: Palette.border
                                border.width: 1
                                width: 62; height: 25
                                Text {
                                    anchors.centerIn: parent
                                    text: "SAMPLE"
                                    color: Palette.parchmentMuted
                                    font.pixelSize: 10
                                    font.weight: Font.DemiBold
                                    font.letterSpacing: 1
                                }
                            }
                        }

                        Item {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            Layout.minimumHeight: 210

                            Canvas {
                                id: diagramLines
                                anchors.fill: parent
                                onPaint: {
                                    var ctx = getContext("2d")
                                    ctx.clearRect(0, 0, width, height)
                                    var cx = width * 0.50
                                    var y = [height * 0.20, height * 0.40, height * 0.60, height * 0.80]
                                    ctx.strokeStyle = "#16AFCB"
                                    ctx.lineWidth = 1.7
                                    ctx.setLineDash([4, 5])
                                    for (var i = 0; i < 3; i++) {
                                        ctx.beginPath()
                                        ctx.moveTo(cx, y[i] + 17)
                                        ctx.lineTo(cx, y[i + 1] - 17)
                                        ctx.stroke()
                                    }
                                    ctx.setLineDash([])
                                }
                            }

                            Column {
                                anchors.horizontalCenter: parent.horizontalCenter
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 8

                                Repeater {
                                    model: ["X", "\\{a,b\\}", "\\{a\\}", "\\varnothing"]
                                    delegate: Rectangle {
                                        required property string modelData
                                        required property int index
                                        width: 132
                                        height: 34
                                        radius: 10
                                        color: index === 0 ? Palette.terracotta : Palette.panelRaised
                                        border.width: 1
                                        border.color: index === 0 ? "#D47A56" : Palette.border
                                        MathFormula {
                                            anchors.fill: parent
                                            anchors.margins: 4
                                            expression: modelData
                                            pointSize: 16
                                            formulaColor: Palette.textPrimary
                                            centered: true
                                        }
                                    }
                                }
                            }

                            Row {
                                anchors.left: parent.left
                                anchors.bottom: parent.bottom
                                spacing: 7
                                MathFormula {
                                    width: 54
                                    height: 22
                                    expression: "U\\subseteq V"
                                    pointSize: 14
                                    formulaColor: Palette.textSecondary
                                    centered: true
                                }
                                Text {
                                    anchors.verticalCenter: parent.verticalCenter
                                    text: "order by inclusion"
                                    color: Palette.textSecondary
                                    font.pixelSize: 12
                                }
                            }
                        }
                    }
                }

                PanelCard {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 360
                    padding: 19

                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 13

                        Text {
                            text: "PROJECT ROADMAP"
                            color: Palette.textPrimary
                            font.pixelSize: 14
                            font.weight: Font.DemiBold
                            font.letterSpacing: 0.5
                        }
                        Text {
                            text: "A careful build, one mathematical layer at a time."
                            color: Palette.textSecondary
                            font.pixelSize: 12
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                        }

                        Repeater {
                            model: [
                                {number: "01", title: "Set foundations", detail: "Sets, subsets, operations and functions", state: "NEXT", color: Palette.cyan},
                                {number: "02", title: "Finite spaces", detail: "Represent X and validate topology axioms", state: "PLANNED", color: Palette.warning},
                                {number: "03", title: "Topological operators", detail: "Interior, closure and boundary", state: "PLANNED", color: Palette.textSecondary},
                                {number: "04", title: "Course extensions", detail: "Bases, continuity, metrics and more", state: "PLANNED", color: Palette.textSecondary}
                            ]
                            delegate: RowLayout {
                                required property var modelData
                                Layout.fillWidth: true
                                spacing: 11
                                Rectangle {
                                    width: 30; height: 30; radius: 9
                                    color: "#4A2B20"
                                    border.color: Palette.border; border.width: 1
                                    Text {
                                        anchors.centerIn: parent
                                        text: modelData.number
                                        color: modelData.color
                                        font.pixelSize: 12
                                        font.weight: Font.Bold
                                    }
                                }
                                ColumnLayout {
                                    Layout.fillWidth: true
                                    spacing: 3
                                    Text { text: modelData.title; color: Palette.textPrimary; font.pixelSize: 13; font.weight: Font.DemiBold }
                                    Text { text: modelData.detail; color: Palette.textSecondary; font.pixelSize: 11; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                                }
                                Text {
                                    text: modelData.state
                                    color: modelData.color
                                    font.pixelSize: 10
                                    font.weight: Font.Bold
                                }
                            }
                        }

                        Item { Layout.fillHeight: true }
                        Rectangle {
                            Layout.fillWidth: true
                            height: 1
                            color: Palette.border
                        }
                        Text {
                            text: "Scope is based on the two course chapters and Exercise Sheet No. 1."
                            color: Palette.textSecondary
                            font.pixelSize: 11
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                    }
                }
            }

            PanelCard {
                Layout.fillWidth: true
                Layout.preferredHeight: 104
                surfaceColor: "#2B2020"
                outlineColor: "#75412F"
                padding: 17
                RowLayout {
                    anchors.fill: parent
                    spacing: 15
                    Rectangle {
                        width: 42; height: 42; radius: 13
                        color: Palette.cyanSoft
                        Text { anchors.centerIn: parent; text: "∴"; color: Palette.cyan; font.pixelSize: 24 }
                    }
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 4
                        Text { text: "A mathematical tool, not just a calculator."; color: Palette.textPrimary; font.pixelSize: 14; font.weight: Font.DemiBold }
                        Text { text: "Every computed result will be connected to its definition and, where appropriate, a step-by-step explanation."; color: Palette.textSecondary; font.pixelSize: 12; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                    }
                }
            }

            Item { Layout.preferredHeight: 8 }
        }
    }
}
