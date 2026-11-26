import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../theme/Palette.js" as Palette
import "../components"

Item {
    id: root
    property int selectedOption: -1
    property bool quizRevealed: false
    property string mode: "study"
    property var exampleResult: null

    function resetQuiz() {
        selectedOption = -1
        quizRevealed = false
        exerciseController.clearFeedback()
    }
    function resultText(r) {
        if (!r) return ""
        if (!r.valid) return r.message + "\n" + (r.errors || []).join("\n")
        return r.message + "\n\nOpen sets: " + r.openSets.join(", ")
            + "\nClosed sets: " + r.closedSets.join(", ")
            + "\nint(A) = " + r.interior + "\ncl(A) = " + r.closure
            + "\n∂A = " + r.boundary + "\nA′ = " + r.accumulationPoints
            + "\nIsolated points: " + r.isolatedPoints
            + "\nHausdorff: " + (r.hausdorff ? "Yes" : "No")
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 12
        PageHeading {
            Layout.fillWidth: true
            eyebrow: "COURSE WORKSPACE / EXERCISES N1–N2"
            title: "Exercise & quiz laboratory"
            description: "Study the supplied subquestions, practise each concept, and test your own finite examples."
        }
        RowLayout {
            Layout.fillWidth: true
            ComboBox {
                id: sheetPicker
                model: ["All exercises", "Sheet N1", "Sheet N2"]
                onActivated: { exerciseController.setSheet(["ALL", "N1", "N2"][currentIndex]); root.resetQuiz() }
            }
            Item { Layout.fillWidth: true }
            Button { text: "Study"; highlighted: root.mode === "study"; onClicked: { root.mode = "study"; root.resetQuiz() } }
            Button { text: "Quiz"; highlighted: root.mode === "quiz"; onClicked: { root.mode = "quiz"; root.resetQuiz() } }
            Button { text: "Example checker"; highlighted: root.mode === "example"; onClicked: { root.mode = "example"; root.resetQuiz() } }
        }
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 12
            Rectangle {
                Layout.preferredWidth: 235
                Layout.fillHeight: true
                radius: 10; color: Palette.panel; border.color: Palette.border
                ColumnLayout {
                    anchors.fill: parent; anchors.margins: 10
                    Text { text: "EXERCISE INDEX"; color: Palette.textSecondary; font.pixelSize: 10; font.weight: Font.Bold }
                    ListView {
                        Layout.fillWidth: true; Layout.fillHeight: true; clip: true
                        model: exerciseController.exercises
                        delegate: ItemDelegate {
                            width: ListView.view.width; height: 60
                            highlighted: modelData.id === exerciseController.currentExercise.id
                            onClicked: { exerciseController.selectExercise(modelData.id); root.resetQuiz() }
                            contentItem: Column {
                                spacing: 3
                                Text { text: modelData.sheet + " · EXERCISE " + modelData.number; color: Palette.cyan; font.pixelSize: 10; font.weight: Font.Bold }
                                Text { text: modelData.title; color: Palette.textPrimary; font.pixelSize: 12; wrapMode: Text.WordWrap }
                            }
                        }
                    }
                }
            }
            Rectangle {
                Layout.fillWidth: true; Layout.fillHeight: true
                radius: 10; color: Palette.panel; border.color: Palette.border
                ScrollView {
                    anchors.fill: parent; anchors.margins: 15; clip: true
                    contentWidth: availableWidth
                    ColumnLayout {
                        width: parent.width; spacing: 10
                        Text {
                            text: exerciseController.currentExercise.sheet + " · EXERCISE " + exerciseController.currentExercise.number
                            color: Palette.cyan; font.pixelSize: 10; font.weight: Font.Bold
                        }
                        Text {
                            text: exerciseController.currentExercise.title
                            color: Palette.textPrimary; font.family: Palette.displayFont; font.pixelSize: 23
                            wrapMode: Text.WordWrap; Layout.fillWidth: true
                        }
                        Text {
                            text: exerciseController.currentExercise.topic
                            color: Palette.textSecondary; font.pixelSize: 12; wrapMode: Text.WordWrap; Layout.fillWidth: true
                        }
                        Rectangle {
                            Layout.fillWidth: true; radius: 8; color: Palette.panelRaised; border.color: Palette.border
                            implicitHeight: statement.implicitHeight + 22
                            Text {
                                id: statement
                                anchors.fill: parent; anchors.margins: 11
                                text: exerciseController.currentExercise.statement
                                color: Palette.textPrimary; font.pixelSize: 14; wrapMode: Text.WordWrap
                            }
                        }
                        Repeater {
                            model: root.mode === "study" ? (exerciseController.currentExercise.parts || []) : []
                            delegate: Rectangle {
                                Layout.fillWidth: true; radius: 8; color: Palette.panelRaised; border.color: Palette.border
                                implicitHeight: partContent.implicitHeight + 20
                                Column {
                                    id: partContent
                                    anchors.fill: parent; anchors.margins: 10; spacing: 6
                                    Text { text: (index + 1) + ". " + modelData; color: Palette.textPrimary; font.pixelSize: 13; wrapMode: Text.WordWrap; width: parent.width }
                                    Text { text: "SOLUTION EXPLANATION"; color: Palette.cyan; font.pixelSize: 9; font.weight: Font.Bold }
                                    Text { text: (exerciseController.currentExercise.solutions || [])[index] || ""; color: Palette.textSecondary; font.pixelSize: 12; wrapMode: Text.WordWrap; width: parent.width }
                                    Text { text: "YOUR PROOF DRAFT · SAVED LOCALLY"; color: Palette.cyan; font.pixelSize: 9; font.weight: Font.Bold }
                                    TextArea {
                                        width: parent.width; height: 78
                                        text: exerciseController.draftFor(exerciseController.currentExercise.id, index)
                                        placeholderText: "Write your proof or reasoning here…"
                                        wrapMode: TextEdit.Wrap
                                        onTextChanged: exerciseController.saveDraft(exerciseController.currentExercise.id, index, text)
                                    }
                                    Text { text: "Saved on this device. The draft is not automatically proof-checked."; color: Palette.textSecondary; font.pixelSize: 10; wrapMode: Text.WordWrap; width: parent.width }
                                }
                            }
                        }
                        Rectangle {
                            visible: root.mode === "quiz"
                            Layout.fillWidth: true; radius: 8; color: Palette.panelRaised; border.color: Palette.border
                            implicitHeight: quizContent.implicitHeight + 22
                            ColumnLayout {
                                id: quizContent
                                anchors.fill: parent; anchors.margins: 12; spacing: 8
                                Text { text: "PRACTISE A SUBQUESTION"; color: Palette.cyan; font.pixelSize: 10; font.weight: Font.Bold }
                                ComboBox {
                                    Layout.fillWidth: true
                                    model: exerciseController.currentExercise.parts || []
                                    currentIndex: exerciseController.currentPartIndex
                                    onActivated: { exerciseController.setCurrentPart(currentIndex); root.resetQuiz() }
                                }
                                Text { text: exerciseController.currentQuiz.question || ""; color: Palette.textPrimary; font.pixelSize: 14; font.weight: Font.DemiBold; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                                Repeater {
                                    model: exerciseController.currentQuiz.options || []
                                    delegate: Button {
                                        Layout.fillWidth: true
                                        text: ["A. ", "B. ", "C. ", "D. "][index] + modelData
                                        enabled: !root.quizRevealed
                                        highlighted: root.selectedOption === index
                                        onClicked: root.selectedOption = index
                                    }
                                }
                                Button {
                                    text: "Check answer"; enabled: root.selectedOption >= 0 && !root.quizRevealed
                                    onClicked: { exerciseController.checkAnswer(root.selectedOption); root.quizRevealed = true }
                                }
                                Text {
                                    visible: root.quizRevealed
                                    text: exerciseController.feedback
                                    color: exerciseController.feedback.startsWith("Correct.") ? Palette.success : Palette.danger
                                    font.pixelSize: 12; wrapMode: Text.WordWrap; Layout.fillWidth: true
                                }
                                Text { text: "Attempts: " + exerciseController.progress.attempts + " · Correct: " + exerciseController.progress.correct; color: Palette.textSecondary; font.pixelSize: 11 }
                                Button { visible: root.quizRevealed; text: "Try again"; onClicked: root.resetQuiz() }
                            }
                        }
                        Rectangle {
                            visible: root.mode === "example"
                            Layout.fillWidth: true; radius: 8; color: Palette.panelRaised; border.color: Palette.border
                            implicitHeight: exampleContent.implicitHeight + 22
                            ColumnLayout {
                                id: exampleContent
                                anchors.fill: parent; anchors.margins: 12; spacing: 8
                                Text { text: "FINITE TOPOLOGICAL SPACE"; color: Palette.cyan; font.pixelSize: 10; font.weight: Font.Bold }
                                Text { text: "X: comma-separated labels. τ: separate open sets with semicolons; use ∅ for empty and X for the whole set. A: comma-separated subset."; color: Palette.textSecondary; font.pixelSize: 12; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                                TextField { id: universe; Layout.fillWidth: true; placeholderText: "X, e.g. a,b,c,d" }
                                TextField { id: topology; Layout.fillWidth: true; placeholderText: "τ, e.g. ∅;X;a;d;a,d" }
                                TextField { id: subset; Layout.fillWidth: true; placeholderText: "A, e.g. a,b,c" }
                                Button { text: "Validate and calculate"; onClicked: exampleResult = exerciseController.checkFiniteExample(universe.text, topology.text, subset.text) }
                                TextArea { Layout.fillWidth: true; height: 175; readOnly: true; wrapMode: TextEdit.Wrap; text: root.resultText(root.exampleResult); placeholderText: "Results will appear here." }
                                Text { text: "Exact finite-space calculations, up to 10 points. Infinite-space examples and free-form proof verification are not claimed."; color: Palette.textSecondary; font.pixelSize: 10; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                            }
                        }
                    }
                }
            }
        }
    }
}
