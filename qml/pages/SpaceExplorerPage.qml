
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../theme/Palette.js" as Palette
import "../components"

Item {
    id: root

    property var validationResult: ({})
    property var analysisResult: ({})
    property var pointResult: ({})
    property var hausdorffResult: ({})

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
                eyebrow: "MATHEMATICAL WORKSPACE / 01"
                title: "Space explorer"
                description: "Define a finite topological space, validate its topology, and explore its topological operators."
            }

            // Underlying set
            PanelCard {
                Layout.fillWidth: true
                padding: 18

                ColumnLayout {
                    anchors.fill: parent
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
                        placeholderText: "Example: a, b, c"
                        text: "a, b, c"
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
                    }

                    Text {
                        text: "Separate elements using commas. Example: a, b, c"
                        color: Palette.textSecondary
                        font.pixelSize: 11
                    }
                }
            }

            // Proposed topology
            PanelCard {
                Layout.fillWidth: true
                padding: 18

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Text {
                        text: "02 / TOPOLOGY FAMILY"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.2
                    }

                    Text {
                        text: "Define the family of open sets τ"
                        color: Palette.textPrimary
                        font.pixelSize: 17
                        font.weight: Font.DemiBold
                    }

                    Text {
                        text: "Enter one subset per line. Use ∅ for the empty set and X for the universe."
                        color: Palette.textSecondary
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }

                    TextArea {
                        id: topologyInput

                        Layout.fillWidth: true
                        Layout.preferredHeight: 135

                        text: "∅\n{a}\n{a,b}\nX"
                        placeholderText: "∅\n{a}\n{a,b}\nX"

                        font.family: Palette.uiFont
                        font.pixelSize: 15
                        color: Palette.textPrimary
                        selectByMouse: true
                        wrapMode: TextEdit.NoWrap

                        background: Rectangle {
                            radius: 9
                            color: Palette.sidebar
                            border.color: topologyInput.activeFocus
                                          ? Palette.cyan
                                          : Palette.border
                            border.width: 1
                        }

                        onActiveFocusChanged: {
                            if (activeFocus)
                                mathPad.targetField = topologyInput
                        }
                    }

                    Button {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 43

                        text: "Validate topology"

                        onClicked: {
                            validationResult =
                                topologyController.validateTopology(
                                    universeInput.text,
                                    topologyInput.text
                                )

                            analysisResult = ({})
                            pointResult = ({})
                            hausdorffResult = ({})
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
                        visible: validationResult.message !== undefined

                        text: validationResult.message || ""
                        color: validationResult.isTopology
                               ? Palette.success
                               : Palette.warning
                        font.family: Palette.uiFont
                        font.pixelSize: 13
                        font.weight: Font.DemiBold
                        wrapMode: Text.WordWrap
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: validationResult.errors
                                 && validationResult.errors.length > 0

                        text: validationResult.errors
                              ? validationResult.errors.join("\n")
                              : ""

                        color: Palette.textSecondary
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                }
            }

            // Subset analysis
            PanelCard {
                Layout.fillWidth: true
                padding: 18

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Text {
                        text: "03 / TOPOLOGICAL OPERATORS"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.2
                    }

                    Text {
                        text: "Explore a subset A"
                        color: Palette.textPrimary
                        font.pixelSize: 17
                        font.weight: Font.DemiBold
                    }

                    TextField {
                        id: subsetInput

                        Layout.fillWidth: true
                        placeholderText: "Example: {b}"
                        text: "{b}"
                        font.family: Palette.uiFont
                        font.pixelSize: 15
                        color: Palette.textPrimary
                        selectByMouse: true

                        background: Rectangle {
                            radius: 9
                            color: Palette.sidebar
                            border.color: subsetInput.activeFocus
                                          ? Palette.cyan
                                          : Palette.border
                            border.width: 1
                        }

                        onActiveFocusChanged: {
                            if (activeFocus)
                                mathPad.targetField = subsetInput
                        }
                    }

                    Button {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 43

                        text: "Calculate operators"
                        enabled: validationResult.isTopology === true

                        onClicked: {
                            analysisResult =
                                topologyController.analyzeSubset(
                                    universeInput.text,
                                    topologyInput.text,
                                    subsetInput.text
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
                            color: parent.enabled
                                   ? Palette.terracotta
                                   : Palette.panelRaised
                            border.color: Palette.border
                            border.width: 1
                        }
                    }

                    GridLayout {
                        Layout.fillWidth: true
                        columns: 3
                        columnSpacing: 8
                        rowSpacing: 8
                        visible: analysisResult.ok === true

                        Repeater {
                            model: [
                                { label: "INTERIOR", value: analysisResult.interior || "—" },
                                { label: "CLOSURE", value: analysisResult.closure || "—" },
                                { label: "BOUNDARY", value: analysisResult.boundary || "—" }
                            ]

                            delegate: Rectangle {
                                required property var modelData

                                Layout.fillWidth: true
                                Layout.preferredHeight: 90

                                radius: 9
                                color: Palette.sidebar
                                border.color: Palette.border
                                border.width: 1

                                ColumnLayout {
                                    Layout.fillWidth: true
                                    anchors.margins: 9
                                    spacing: 7

                                    Text {
                                        text: modelData.label
                                        color: Palette.cyan
                                        font.pixelSize: 9
                                        font.weight: Font.Bold
                                    }

                                    Text {
                                        text: modelData.value
                                        color: Palette.textPrimary
                                        font.family: Palette.displayFont
                                        font.pixelSize: 16
                                        wrapMode: Text.WordWrap
                                    }
                                }
                            }
                        }
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: root.analysisResult.ok === true
                        text:
                            "COMPLEMENT: " + root.analysisResult.complement +
                            "\nOPEN: " + (root.analysisResult.isOpen ? "Yes" : "No") +
                            "\nCLOSED: " + (root.analysisResult.isClosed ? "Yes" : "No") +
                            "\nCLOPEN: " + (root.analysisResult.isClopen ? "Yes" : "No") +
                            "\nACCUMULATION POINTS: " + root.analysisResult.accumulationPoints +
                            "\nISOLATED POINTS: " + root.analysisResult.isolatedPoints +
                            "\nALL CLOSED SETS: " + (root.analysisResult.closedSets || []).join(", ")

                        color: Palette.textSecondary
                        font.family: Palette.uiFont
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: analysisResult.ok === false

                        text: analysisResult.errors
                              ? analysisResult.errors.join("\n")
                              : analysisResult.message || ""

                        color: Palette.warning
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                }
            }

            // Neighborhood laboratory
            PanelCard {
                Layout.fillWidth: true
                padding: 18

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Text {
                        text: "04 / NEIGHBORHOOD LABORATORY"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.2
                    }

                    Text {
                        text: "Explore the neighborhoods of a point"
                        color: Palette.textPrimary
                        font.pixelSize: 17
                        font.weight: Font.DemiBold
                    }

                    TextField {
                        id: pointInput
                        Layout.fillWidth: true

                        text: "b"
                        placeholderText: "Example: b"

                        font.family: Palette.uiFont
                        font.pixelSize: 15
                        color: Palette.textPrimary
                        selectByMouse: true

                        background: Rectangle {
                            radius: 9
                            color: Palette.sidebar
                            border.color: pointInput.activeFocus
                                          ? Palette.cyan
                                          : Palette.border
                            border.width: 1
                        }

                        onActiveFocusChanged: {
                            if (activeFocus)
                                mathPad.targetField = pointInput
                        }
                    }

                    Button {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 43

                        text: "Calculate neighborhoods"
                        enabled: root.validationResult.isTopology === true

                        onClicked: {
                            root.pointResult = topologyController.analyzePoint(
                                universeInput.text,
                                topologyInput.text,
                                pointInput.text
                            )
                        }

                        contentItem: Text {
                            text: parent.text
                            color: Palette.parchment
                            font.family: Palette.uiFont
                            font.pixelSize: 13
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        background: Rectangle {
                            radius: 9
                            color: parent.enabled
                                   ? Palette.terracotta
                                   : Palette.panelRaised
                            border.color: Palette.border
                            border.width: 1
                        }
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: root.pointResult.ok === true

                        text: "Neighborhoods of " + root.pointResult.point +
                              ":\n" + root.pointResult.neighborhoods.join("\n")

                        color: Palette.success
                        font.family: Palette.uiFont
                        font.pixelSize: 13
                        wrapMode: Text.WordWrap
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: root.pointResult.ok === false

                        text: root.pointResult.errors
                              ? root.pointResult.errors.join("\n")
                              : ""

                        color: Palette.warning
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                }
            }


            PanelCard {
                Layout.fillWidth: true
                padding: 18

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Text {
                        text: "05 / HAUSDORFF LABORATORY"
                        color: Palette.cyan
                        font.family: Palette.uiFont
                        font.pixelSize: 11
                        font.weight: Font.Bold
                        font.letterSpacing: 1.2
                    }

                    Text {
                        text: "Test the separation property"
                        color: Palette.textPrimary
                        font.pixelSize: 17
                        font.weight: Font.DemiBold
                    }

                    Text {
                        text: "Check whether every pair of distinct points has disjoint open neighborhoods."
                        color: Palette.textSecondary
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }

                    Button {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 43

                        text: "Check Hausdorff property"
                        enabled: root.validationResult.isTopology === true

                        onClicked: {
                            root.hausdorffResult = topologyController.analyzeHausdorff(
                                universeInput.text,
                                topologyInput.text
                            )
                        }

                        contentItem: Text {
                            text: parent.text
                            color: Palette.parchment
                            font.family: Palette.uiFont
                            font.pixelSize: 13
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        background: Rectangle {
                            radius: 9
                            color: parent.enabled
                                   ? Palette.terracotta
                                   : Palette.panelRaised
                            border.color: Palette.border
                            border.width: 1
                        }
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: root.hausdorffResult.ok === true

                        text: root.hausdorffResult.message +
                              (root.hausdorffResult.isHausdorff
                               ? "\nAll distinct pairs have been separated."
                               : "\nPairs that cannot be separated: " +
                                 (root.hausdorffResult.inseparablePairs || []).join(", "))

                        color: root.hausdorffResult.isHausdorff
                               ? Palette.success
                               : Palette.warning

                        font.family: Palette.uiFont
                        font.pixelSize: 13
                        wrapMode: Text.WordWrap
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: root.hausdorffResult.ok === false

                        text: root.hausdorffResult.errors
                              ? root.hausdorffResult.errors.join("\n")
                              : ""

                        color: Palette.warning
                        font.family: Palette.uiFont
                        font.pixelSize: 12
                        wrapMode: Text.WordWrap
                    }
                }
            }


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
