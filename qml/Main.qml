import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import "theme/Palette.js" as Palette
import "components"

ApplicationWindow {
    id: window
    visible: true
    width: 1440
    height: 920
    minimumWidth: 1080
    minimumHeight: 700
    title: "TopoLab — Interactive Topology Laboratory"
    color: Palette.canvas

    property int activePage: 0
    property var pageTitles: ["Overview", "Space explorer", "Set toolkit", "Proof laboratory", "Metric laboratory"]
    property var pageSubtitles: [
        "A workspace for mathematical exploration",
        "Define X and inspect a proposed topology",
        "Build the set operations used throughout topology",
        "Follow definitions, theorems, and proof structures",
        "Explore distances, balls, and metric topologies"
    ]
    property var pageFiles: [
        "pages/OverviewPage.qml",
        "pages/SpaceExplorerPage.qml",
        "pages/SetToolkitPage.qml",
        "pages/ProofLabPage.qml",
        "pages/MetricLabPage.qml"
    ]

    Rectangle {
        anchors.fill: parent
        color: Palette.canvas

        RowLayout {
            anchors.fill: parent
            spacing: 0

            // Left navigation rail.
            Rectangle {
                id: sidebar
                Layout.preferredWidth: 252
                Layout.minimumWidth: 252
                Layout.fillHeight: true
                color: Palette.sidebar
                border.width: 0

                ColumnLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 18
                    anchors.rightMargin: 18
                    anchors.topMargin: 21
                    anchors.bottomMargin: 16
                    spacing: 0

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 11
                        Rectangle {
                            width: 39; height: 39; radius: 12
                            color: Palette.terracotta
                            border.color: "#D17A58"; border.width: 1
                            Text { anchors.centerIn: parent; text: "τ"; color: Palette.textPrimary; font.pixelSize: 27; font.family: Palette.displayFont }
                        }
                        ColumnLayout {
                            spacing: 1
                            Text { text: "TopoLab"; color: Palette.textPrimary; font.pixelSize: 21; font.weight: Font.DemiBold; font.letterSpacing: 0.2 }
                            Text { text: "INTERACTIVE TOPOLOGY LAB"; color: Palette.textSecondary; font.pixelSize: 10; font.letterSpacing: 1.1 }
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.topMargin: 21
                        Layout.bottomMargin: 18
                        height: 1
                        color: Palette.border
                    }

                    Text {
                        text: "WORKSPACE"
                        color: "#8F7567"
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.5
                        Layout.leftMargin: 8
                        Layout.bottomMargin: 9
                    }

                    NavItem { Layout.fillWidth: true; label: "Overview"; glyph: "⌂"; active: window.activePage === 0; onActivated: window.activePage = 0 }

                    Text {
                        text: "MATHEMATICAL TOOLS"
                        color: "#8F7567"
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.5
                        Layout.leftMargin: 8
                        Layout.topMargin: 21
                        Layout.bottomMargin: 9
                    }

                    NavItem { Layout.fillWidth: true; label: "Space explorer"; glyph: "◎"; active: window.activePage === 1; onActivated: window.activePage = 1 }
                    NavItem { Layout.fillWidth: true; label: "Set toolkit"; glyph: "∪"; active: window.activePage === 2; onActivated: window.activePage = 2 }
                    NavItem { Layout.fillWidth: true; label: "Proof laboratory"; glyph: "∴"; active: window.activePage === 3; onActivated: window.activePage = 3 }
                    NavItem { Layout.fillWidth: true; label: "Metric laboratory"; glyph: "⊙"; active: window.activePage === 4; onActivated: window.activePage = 4 }

                    Item { Layout.fillHeight: true }

                    Rectangle {
                        Layout.fillWidth: true
                        height: 1
                        color: Palette.border
                        Layout.bottomMargin: 13
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 76
                        radius: 12
                        color: "#2B1A14"
                        border.color: Palette.border
                        border.width: 1
                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 11
                            spacing: 4
                            RowLayout {
                                Text { text: "BUILD STATUS"; color: Palette.textSecondary; font.pixelSize: 10; font.letterSpacing: 1.1; font.weight: Font.Bold }
                                Item { Layout.fillWidth: true }
                                Rectangle { width: 6; height: 6; radius: 3; color: Palette.warning }
                            }
                            Text { text: "Interface foundation"; color: Palette.textPrimary; font.pixelSize: 12; font.weight: Font.DemiBold }
                            Text { text: "Mathematical engine: next"; color: Palette.textSecondary; font.pixelSize: 11 }
                        }
                    }
                    Text {
                        text: "TOPOLAB  ·  VERSION 0.1.1"
                        color: "#80685C"
                        font.pixelSize: 10
                        font.letterSpacing: 0.8
                        Layout.topMargin: 13
                        Layout.leftMargin: 3
                    }
                }
            }

            // Main content region.
            ColumnLayout {
                id: mainArea
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 0

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 78
                    color: "#2D1913"
                    border.width: 0

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 27
                        anchors.rightMargin: 28
                        spacing: 14

                        ColumnLayout {
                            spacing: 3
                            Text {
                                text: window.pageTitles[window.activePage]
                                color: Palette.textPrimary
                                font.family: Palette.displayFont
                                font.pixelSize: 20
                                font.weight: Font.DemiBold
                            }
                            Text {
                                text: window.pageSubtitles[window.activePage]
                                color: Palette.textSecondary
                                font.pixelSize: 12
                            }
                        }

                        Item { Layout.fillWidth: true }

                        Rectangle {
                            Layout.preferredWidth: 205
                            Layout.preferredHeight: 35
                            radius: 9
                            color: Palette.sidebar
                            border.color: Palette.border
                            border.width: 1
                            RowLayout {
                                anchors.fill: parent
                                anchors.leftMargin: 10
                                anchors.rightMargin: 10
                                Text { text: "⌕"; color: Palette.textSecondary; font.pixelSize: 19 }
                                Text { text: "Search workspace"; color: "#90796C"; font.pixelSize: 12; Layout.fillWidth: true }
                                Text { text: "⌘ K"; color: "#90796C"; font.pixelSize: 10 }
                            }
                        }

                        Rectangle {
                            width: 35; height: 35; radius: 11
                            color: Palette.panelRaised
                            border.color: Palette.border; border.width: 1
                            Text { anchors.centerIn: parent; text: "?"; color: Palette.parchmentMuted; font.pixelSize: 16; font.weight: Font.DemiBold }
                        }
                    }

                    Rectangle {
                        anchors.bottom: parent.bottom
                        width: parent.width
                        height: 1
                        color: Palette.border
                    }
                }

                Loader {
                    id: pageLoader
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.margins: 25
                    source: window.pageFiles[window.activePage]
                    asynchronous: false
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 29
                    color: "#21130F"
                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 27
                        anchors.rightMargin: 27
                        Text { text: "READY"; color: Palette.success; font.pixelSize: 10; font.weight: Font.Bold; font.letterSpacing: 1 }
                        Text { text: "·"; color: Palette.textSecondary; font.pixelSize: 11 }
                        Text { text: "Local session"; color: Palette.textSecondary; font.pixelSize: 10 }
                        Item { Layout.fillWidth: true }
                        Text { text: "CHAPTERS 01–02  /  FOUNDATION BUILD"; color: "#8F7567"; font.pixelSize: 10; font.letterSpacing: 0.7 }
                    }
                }
            }
        }
    }
}
