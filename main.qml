import QtQuick 2.0

Rectangle {
    width: 200
    height: 200
    color: "green"

    Text {
        id: element
        y: 0
        text: qsTr("Welcome to cup pong!!")
        font.pixelSize: 20
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
