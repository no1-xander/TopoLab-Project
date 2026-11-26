
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../theme/Palette.js" as Palette
import "../components"

Item {
    id: root

    property var basisResult: ({})
    property var subbasisResult: ({})

    ScrollView {
        id: scrollView

        anchors.fill: parent
        clip: true
        contentWidth: availableWidth
        ScrollBar.vertical.policy: ScrollBar.AsNeeded

        ColumnLayout {
            width: scrollView.availableWidth
            spacing: 18

            PageHeading {
                Layout.fillWidth: true
                eyebrow: "MATHEMATICAL WORKSPACE / 06"
                title: "Basis laboratory"
                description: "Construct bases and subbases, verify their properties, and generate the topologies they induce."
            }

            // Underlying set
            PanelCard {
                Layout.fillWidth: true
                padding: 18

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Text {
                        text: "01 / UNDERLYING SET"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.2
                    }

                    Text {
                        text: "Define the universe X"
                        color: Palette.textPrimary
                        font.pixelSize: 17
                        font.weight: Font.DemiBold
                    }

                    TextField {
                        id: universeInput

                        Layout.fillWidth: true
                        text: "1, 2, 3"
                        placeholderText: "Example: 1, 2, 3"

                        font.family: Palette.uiFont
                        font.pixelSize: 15
                        color: Palette.textPrimary
                        selectByMouse: true

                        background: Rectangle {
                            radius: 9
                            color: Palette.sidebar
                            border.color: universeInput.activeFocus
                                          ? Palette.cyan
                                          : Palette.border
                            border.width: 1
                        }

                        onActiveFocusChanged: {
                            if (activeFocus)
                                mathPad.targetField = universeInput
                        }

                        onTextChanged: {
                            basisResult = ({})
                            subbasisResult = ({})
                        }
                    }

                    Text {
                        text: "Separate elements with commas. The elements must be letters, numbers, or underscores."
                        color: Palette.textSecondary
                        font.pixelSize: 11
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                }
            }

            // Basis laboratory
            PanelCard {
                Layout.fillWidth: true
                padding: 18

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Text {
                        text: "02 / BASIS LABORATORY"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.2
                    }

                    Text {
                        text: "Test a family of subsets"
                        color: Palette.textPrimary
                        font.pixelSize: 17
                        font.weight: Font.DemiBold
                    }

                    Text {
                        text: "Enter one subset per line. The application checks the covering and intersection conditions."
                        color: Palette.textSecondary
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }

                    TextArea {
                        id: basisInput

                        Layout.fillWidth: true
                        Layout.preferredHeight: 125

                        text: "{1, 2}\n{2, 3}\n{2}"
                        placeholderText: "{1, 2}\n{2, 3}\n{2}"

                        font.family: Palette.uiFont
                        font.pixelSize: 15
                        color: Palette.textPrimary
                        selectByMouse: true
                        wrapMode: TextEdit.NoWrap

                        background: Rectangle {
                            radius: 9
                            color: Palette.sidebar
                            border.color: basisInput.activeFocus
                                          ? Palette.cyan
                                          : Palette.border
                            border.width: 1
                        }

                        onActiveFocusChanged: {
                            if (activeFocus)
                                mathPad.targetField = basisInput
                        }

                        onTextChanged: basisResult = ({})
                    }

                    Button {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 43

                        text: "Check basis and generate topology"

                        onClicked: {
                            basisResult = basisController.analyzeBasis(
                                universeInput.text,
                                basisInput.text
                            )
                        }

                        contentItem: Text {
                            text: parent.text
                            color: Palette.parchment
                            font.family: Palette.uiFont
                            font.pixelSize: 13
                            font.weight: Font.DemiBold
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        background: Rectangle {
                            radius: 9
                            color: parent.down
                                   ? Palette.terracotta
                                   : Palette.panelRaised
                            border.color: Palette.terracotta
                            border.width: 1
                        }
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: basisResult.message !== undefined

                        text: basisResult.message || ""

                        color: basisResult.ok === false
                               ? Palette.warning
                               : basisResult.isBasis
                                 ? Palette.success
                                 : Palette.warning

                        font.family: Palette.uiFont
                        font.pixelSize: 13
                        font.weight: Font.DemiBold
                        wrapMode: Text.WordWrap
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: basisResult.isBasis === true

                        text: "GENERATED TOPOLOGY τ"

                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.1
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: topologyColumn.implicitHeight + 20
                        visible: basisResult.isBasis === true

                        radius: 9
                        color: Palette.sidebar
                        border.color: Palette.border
                        border.width: 1

                        ColumnLayout {
                            id: topologyColumn

                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 5

                            Repeater {
                                model: basisResult.generatedTopology || []

                                delegate: Text {
                                    required property string modelData

                                    Layout.fillWidth: true
                                    text: modelData
                                    color: Palette.textPrimary
                                    font.family: Palette.displayFont
                                    font.pixelSize: 15
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: basisResult.ok === false
                                 && basisResult.errors
                                 && basisResult.errors.length > 0

                        text: basisResult.errors
                              ? basisResult.errors.join("\n")
                              : ""

                        color: Palette.warning
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                }
            }

            // Subbasis laboratory
            PanelCard {
                Layout.fillWidth: true
                padding: 18

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Text {
                        text: "03 / SUBBASIS LABORATORY"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.2
                    }

                    Text {
                        text: "Generate a topology from a subbasis"
                        color: Palette.textPrimary
                        font.pixelSize: 17
                        font.weight: Font.DemiBold
                    }

                    Text {
                        text: "Enter a family of subsets. TopoLab calculates all distinct finite intersections, then generates the topology."
                        color: Palette.textSecondary
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }

                    TextArea {
                        id: subbasisInput

                        Layout.fillWidth: true
                        Layout.preferredHeight: 110

                        text: "{1, 2}\n{2, 3}"
                        placeholderText: "{1, 2}\n{2, 3}"

                        font.family: Palette.uiFont
                        font.pixelSize: 15
                        color: Palette.textPrimary
                        selectByMouse: true
                        wrapMode: TextEdit.NoWrap

                        background: Rectangle {
                            radius: 9
                            color: Palette.sidebar
                            border.color: subbasisInput.activeFocus
                                          ? Palette.cyan
                                          : Palette.border
                            border.width: 1
                        }

                        onActiveFocusChanged: {
                            if (activeFocus)
                                mathPad.targetField = subbasisInput
                        }

                        onTextChanged: subbasisResult = ({})
                    }

                    Button {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 43

                        text: "Generate topology from subbasis"

                        onClicked: {
                            subbasisResult = basisController.analyzeSubbasis(
                                universeInput.text,
                                subbasisInput.text
                            )
                        }

                        contentItem: Text {
                            text: parent.text
                            color: Palette.parchment
                            font.family: Palette.uiFont
                            font.pixelSize: 13
                            font.weight: Font.DemiBold
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        background: Rectangle {
                            radius: 9
                            color: parent.down
                                   ? Palette.terracotta
                                   : Palette.panelRaised
                            border.color: Palette.terracotta
                            border.width: 1
                        }
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: subbasisResult.message !== undefined

                        text: subbasisResult.message || ""

                        color: subbasisResult.ok === false
                               ? Palette.warning
                               : Palette.success

                        font.family: Palette.uiFont
                        font.pixelSize: 13
                        font.weight: Font.DemiBold
                        wrapMode: Text.WordWrap
                    }

                    // Finite intersections
                    Text {
                        Layout.fillWidth: true
                        visible: subbasisResult.ok === true

                        text: "FINITE INTERSECTIONS"

                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.1
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: intersectionsColumn.implicitHeight + 20
                        visible: subbasisResult.ok === true

                        radius: 9
                        color: Palette.sidebar
                        border.color: Palette.border
                        border.width: 1

                        ColumnLayout {
                            id: intersectionsColumn

                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 5

                            Repeater {
                                model: subbasisResult.finiteIntersections || []

                                delegate: Text {
                                    required property string modelData

                                    Layout.fillWidth: true
                                    text: modelData
                                    color: Palette.textPrimary
                                    font.family: Palette.displayFont
                                    font.pixelSize: 15
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }

                    // Generated topology
                    Text {
                        Layout.fillWidth: true
                        visible: subbasisResult.ok === true

                        text: "GENERATED TOPOLOGY τ"

                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.1
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        implicitHeight: subbasisTopologyColumn.implicitHeight + 20
                        visible: subbasisResult.ok === true

                        radius: 9
                        color: Palette.sidebar
                        border.color: Palette.border
                        border.width: 1

                        ColumnLayout {
                            id: subbasisTopologyColumn

                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 5

                            Repeater {
                                model: subbasisResult.generatedTopology || []

                                delegate: Text {
                                    required property string modelData

                                    Layout.fillWidth: true
                                    text: modelData
                                    color: Palette.textPrimary
                                    font.family: Palette.displayFont
                                    font.pixelSize: 15
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: subbasisResult.ok === false
                                 && subbasisResult.errors
                                 && subbasisResult.errors.length > 0

                        text: subbasisResult.errors
                              ? subbasisResult.errors.join("\n")
                              : ""

                        color: Palette.warning
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                }
            }

            // Mathematical keyboard
            PanelCard {
                Layout.fillWidth: true
                padding: 12

                MathPad {
                    id: mathPad

                    Layout.fillWidth: true
                    Layout.preferredHeight: 185
                }
            }
        }
    }
}
