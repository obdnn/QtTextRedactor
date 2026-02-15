import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 700
    height: 600
    title: "Notes"

    Rectangle {
        anchors.fill: parent
        color: "#000000"
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        RowLayout {
            spacing: 10
            Layout.fillWidth: true

            Button {
                text: "➕ Create"
                onClicked: backend.createFile()

                background: Rectangle {
                    color: parent.pressed ? "#005BBB" : "#007AFF"
                    radius: 6
                }

                contentItem: Text {
                    text: parent.text
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }

            Button {
                text: "📁 Open"
                onClicked: backend.openFileDialog()

                background: Rectangle {
                    color: parent.pressed ? "#2a2a2a" : "#1a1a1a"
                    radius: 6
                    border.color: "#333333"
                    border.width: 1
                }

                contentItem: Text {
                    text: parent.text
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }

            Button {
                text: "💾 Save"
                onClicked: {
                    if (backend.currentFilePath) {
                        backend.saveFile("")
                    } else {
                        backend.saveFileDialog()
                    }
                }

                background: Rectangle {
                    color: parent.pressed ? "#2a2a2a" : "#1a1a1a"
                    radius: 6
                    border.color: "#333333"
                    border.width: 1
                }

                contentItem: Text {
                    text: parent.text
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }

            Item {
                Layout.fillWidth: true
            }

            Button {
                text: "🗑️ Delete"
                visible: backend.currentFilePath !== ""
                onClicked: deleteConfirmDialog.open()

                background: Rectangle {
                    color: parent.pressed ? "#cc0000" : "#ff3333"
                    radius: 6
                }

                contentItem: Text {
                    text: parent.text
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 60
            color: "#1a1a1a"
            radius: 8
            border.color: headerField.activeFocus ? "#007AFF" : "#333333"
            border.width: 2

            TextField {
                id: headerField
                anchors.fill: parent
                anchors.margins: 10
                text: backend.currentHeader
                font.pixelSize: 24
                font.bold: true
                selectByMouse: true
                placeholderText: "Note name..."
                placeholderTextColor: "#666666"
                color: "#ffffff"

                background: Rectangle {
                    color: "transparent"
                }

                onTextChanged: {
                    backend.currentHeader = text
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#1a1a1a"
            radius: 8
            border.color: noteField.activeFocus ? "#007AFF" : "#333333"
            border.width: 2

            ScrollView {
                anchors.fill: parent
                anchors.margins: 10
                clip: true

                TextArea {
                    id: noteField
                    font.pixelSize: 16
                    wrapMode: TextArea.Wrap
                    selectByMouse: true
                    placeholderText: "Start typing..."
                    placeholderTextColor: "#666666"
                    color: "#ffffff"

                    background: Rectangle {
                        color: "transparent"
                    }

                    text: backend.currentText

                    onTextChanged: {
                        if (text !== backend.currentText) {
                            backend.currentText = text
                        }
                    }
                }
            }
        }
    }
Dialog {
    id: deleteConfirmDialog
    title: "Delete Note"
    anchors.centerIn: parent
    modal: true
    width: 300

    standardButtons: Dialog.Yes | Dialog.No

    background: Rectangle {
        color: "#1a1a1a"
        radius: 8
        border.color: "#333333"
        border.width: 2
    }

    header: Rectangle {
        color: "#1a1a1a"
        height: 50
        width: parent.width

        Label {
            text: "Delete Note"
            color: "#ffffff"
            font.pixelSize: 18
            font.bold: true
            anchors.centerIn: parent
        }
    }

    contentItem: Rectangle {
        color: "transparent"
        implicitHeight: 80
        implicitWidth: 260

        Label {
            anchors.fill: parent
            text: "Are you sure you want to delete this note?"
            color: "#ffffff"
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    onAccepted: backend.deleteFile()
}
}