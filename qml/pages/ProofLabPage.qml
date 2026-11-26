import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../theme/Palette.js" as Palette
import "../components"

Item {
    id: root
    property int selectedPart: 0
    property int selectedOption: -1
    property bool quizRevealed: false
    property string mode: "study"

    function resetQuiz() {
        selectedOption = -1
        quizRevealed = false
        exerciseController.clearFeedback()
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 14

        PageHeading {
            Layout.fillWidth: true
            eyebrow: "COURSE WORKSPACE / EXERCISES N1–N2"
            title: "Exercise & quiz laboratory"
            description: "Study every supplied exercise, review its reasoning, or test your understanding with instant explanations."
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10
            ComboBox {
                id: sheetPicker
                model: ["All exercises", "Sheet N1", "Sheet N2"]
                currentIndex: 0
                onActivated: {
                    exerciseController.setSheet(["ALL", "N1", "N2"][currentIndex])
                    root.selectedPart = 0
                    root.resetQuiz()
                }
            }
            Item { Layout.fillWidth: true }
            Button {
                text: "Study mode"
                highlighted: root.mode === "study"
                onClicked: { root.mode = "study"; root.resetQuiz() }
            }
            Button {
                text: "Quiz mode"
                highlighted: root.mode === "quiz"
                onClicked: { root.mode = "quiz"; root.resetQuiz() }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 14

            Rectangle {
                Layout.preferredWidth: 250
                Layout.fillHeight: true
                radius: 12
                color: Palette.panel
                border.color: Palette.border
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 12
                    Text {
                        text: "EXERCISE INDEX"
                        color: Palette.textSecondary
                        font.pixelSize: 10
                        font.weight: Font.Bold
                        font.letterSpacing: 1
                    }
                    ListView {
                        id: exerciseList
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        model: exerciseController.exercises
                        delegate: ItemDelegate {
                            width: ListView.view.width
                            height: 64
                            highlighted: modelData.id === exerciseController.currentExercise.id
                            onClicked: {
                                exerciseController.selectExercise(modelData.id)
                                root.selectedPart = 0
                                root.resetQuiz()
                            }
                            contentItem: Column {
                                spacing: 3
                                Text {
                                    text: modelData.sheet + " · EXERCISE " + modelData.number
                                    color: Palette.cyan
                                    font.pixelSize: 10
                                    font.weight: Font.Bold
                                }
                                Text {
                                    text: modelData.title
                                    color: Palette.textPrimary
                                    font.pixelSize: 12
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: 12
                color: Palette.panel
                border.color: Palette.border
                ScrollView {
                    anchors.fill: parent
                    anchors.margins: 18
                    clip: true
                    contentWidth: availableWidth
                    ColumnLayout {
                        width: parent.width
                        spacing: 12
                        Text {
                            text: exerciseController.currentExercise.sheet + " · EXERCISE " + exerciseController.currentExercise.number
                            color: Palette.cyan
                            font.pixelSize: 10
                            font.weight: Font.Bold
                            font.letterSpacing: 1
                        }
                        Text {
                            text: exerciseController.currentExercise.title
                            color: Palette.textPrimary
                            font.family: Palette.displayFont
                            font.pixelSize: 25
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                        Text {
                            text: exerciseController.currentExercise.topic
                            color: Palette.textSecondary
                            font.pixelSize: 12
                            wrapMode: Text.WordWrap
                            Layout.fillWidth: true
                        }
                        Rectangle {
                            Layout.fillWidth: true
                            radius: 9
                            color: Palette.panelRaised
                            border.color: Palette.border
                            implicitHeight: statementText.implicitHeight + 24
                            Text {
                                id: statementText
                                anchors.fill: parent
                                anchors.margins: 12
                                text: exerciseController.currentExercise.statement
                                color: Palette.textPrimary
                                font.pixelSize: 14
                                wrapMode: Text.WordWrap
                            }
                        }

                        Text {
                            text: root.mode === "study" ? "EXERCISE PARTS & EXPLANATIONS" : "KNOWLEDGE CHECK"
                            color: Palette.textSecondary
                            font.pixelSize: 10
                            font.weight: Font.Bold
                            font.letterSpacing: 1
                        }

                        Repeater {
                            model: root.mode === "study" ? (exerciseController.currentExercise.parts || []) : []
                            delegate: Rectangle {
                                Layout.fillWidth: true
                                radius: 9
                                color: Palette.panelRaised
                                border.color: Palette.border
                                implicitHeight: partColumn.implicitHeight + 22
                                Column {
                                    id: partColumn
                                    anchors.fill: parent
                                    anchors.margins: 11
                                    spacing: 7
                                    Text {
                                        text: (index + 1) + ". " + modelData
                                        color: Palette.textPrimary
                                        font.pixelSize: 13
                                        wrapMode: Text.WordWrap
                                        width: parent.width
                                    }
                                    Text {
                                        text: "EXPLANATION"
                                        color: Palette.cyan
                                        font.pixelSize: 9
                                        font.weight: Font.Bold
                                    }
                                    Text {
                                        text: (exerciseController.currentExercise.solutions || [])[index] || ""
                                        color: Palette.textSecondary
                                        font.pixelSize: 12
                                        wrapMode: Text.WordWrap
                                        width: parent.width
                                    }
                                }
                            }
                        }

                        { /* Quiz content is rendered only in quiz mode. */ }
                        Rectangle {
                            visible: root.mode === "quiz"
                            Layout.fillWidth: true
                            radius: 10
                            color: Palette.panelRaised
                            border.color: Palette.border
                            implicitHeight: quizColumn.implicitHeight + 24
                            ColumnLayout {
                                id: quizColumn
                                anchors.fill: parent
                                anchors.margins: 13
                                spacing: 9
                                Text {
                                    text: (exerciseController.quizQuestion().question || "")
                                    color: Palette.textPrimary
                                    font.pixelSize: 14
                                    font.weight: Font.DemiBold
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }
                                Repeater {
                                    model: exerciseController.quizOptions()
                                    delegate: Button {
                                        Layout.fillWidth: true
                                        text: ["A. ", "B. ", "C. ", "D. "][index] + modelData
                                        enabled: !root.quizRevealed
                                        highlighted: root.selectedOption === index
                                        onClicked: root.selectedOption = index
                                    }
                                }
                                Button {
                                    text: "Check answer"
                                    enabled: root.selectedOption >= 0 && !root.quizRevealed
                                    onClicked: {
                                        exerciseController.checkAnswer(root.selectedOption)
                                        root.quizRevealed = true
                                    }
                                }
                                Text {
                                    visible: root.quizRevealed
                                    text: exerciseController.feedback
                                    color: Palette.success
                                    font.pixelSize: 12
                                    wrapMode: Text.WordWrap
                                    Layout.fillWidth: true
                                }
                                Button {
                                    visible: root.quizRevealed
                                    text: "Try this question again"
                                    onClicked: root.resetQuiz()
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
