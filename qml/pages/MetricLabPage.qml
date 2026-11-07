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
                eyebrow: "MATHEMATICAL WORKSPACE / 04"
                title: "Metric laboratory"
                description: "Explore metrics, open balls, closed balls, and the topology induced by a metric, following the Chapter 2 course material."
            }

            PanelCard {
                Layout.fillWidth: true
                Layout.preferredHeight: 242
                padding: 20
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 9
                    Text {
                        text: "METRIC DEFINITION"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.letterSpacing: 1.2
                        font.weight: Font.Bold
                    }
                    MathFormula {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 42
                        expression: "d:X\\times X\\to[0,\\infty)"
                        pointSize: 25
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        Text { text: "M1"; color: Palette.cyan; font.family: Palette.uiFont; font.pixelSize: 12; font.weight: Font.Bold }
                        MathFormula { Layout.fillWidth: true; Layout.preferredHeight: 31; expression: "d(x,y)=0\\Longleftrightarrow x=y"; pointSize: 18 }
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        Text { text: "M2"; color: Palette.cyan; font.family: Palette.uiFont; font.pixelSize: 12; font.weight: Font.Bold }
                        MathFormula { Layout.fillWidth: true; Layout.preferredHeight: 31; expression: "d(x,y)=d(y,x)"; pointSize: 18 }
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        Text { text: "M3"; color: Palette.cyan; font.family: Palette.uiFont; font.pixelSize: 12; font.weight: Font.Bold }
                        MathFormula { Layout.fillWidth: true; Layout.preferredHeight: 31; expression: "d(x,z)\\leq d(x,y)+d(y,z)"; pointSize: 18 }
                    }
                }
            }

            PanelCard {
                Layout.fillWidth: true
                Layout.preferredHeight: 156
                padding: 20
                ColumnLayout {
                    anchors.fill: parent
                    spacing: 9
                    Text {
                        text: "OPEN BALL"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.letterSpacing: 1.2
                        font.weight: Font.Bold
                    }
                    MathFormula {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 42
                        expression: "B_d(x,r)=\\{y\\in X:d(x,y)<r\\}"
                        pointSize: 23
                    }
                    Text {
                        text: "Interactive metric and ball calculations will be added after the finite-space engine."
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
