import QtQuick 2.12
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.1

Rectangle {
    visible: true
    width: 480
    height: 320
    color: "#000000"

    ColumnLayout {
        anchors.fill: parent

        Label {
            id: headingText
            color: "#ea4848"
            text: qsTr("Select a game")
            lineHeight: 1.5
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            Layout.fillWidth: true
            styleColor: "#ee3737"
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            font.pixelSize: 18
        }

        SwipeView {
            id: view
            font.bold: true
            currentIndex: 0
            Layout.fillHeight: true
            Layout.fillWidth: true

            Item {
                id: classicBeerPongPage

                Text {
                    id: element
                    color: "#ee3737"
                    text: qsTr("Beer Pong")
                    font.pixelSize: 12
                }

                Text {
                    id: element1
                    x: 48
                    y: 88
                    width: 272
                    height: 15
                    color: "#db3535"
                    text: qsTr("The classic beer-pong game where the first player to sink all 10 cups wins")
                    wrapMode: Text.WordWrap
                    font.pixelSize: 12
                }
            }

            Item {
                id: territoryPongPage

                Text {
                    text: qsTr("Territory Pong")
                    font.pixelSize: 12
                }

                Text {
                    x: 40
                    y: 79
                    width: 348
                    height: 15
                    color: "#f90606"
                    text: qsTr("Players compete over the same cups - sink a cup to claim it, but if the other player sinks it to it will become theirs")
                    wrapMode: Text.WordWrap
                    font.pixelSize: 12
                }
            }
        }

        PageIndicator {
            id: indicator
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
            Layout.row: 1
            count: view.count
            currentIndex: view.currentIndex
        }

        Button {
            id: playButton
            text: qsTr("PLAY")
            Layout.fillWidth: true
            font.pixelSize: 30
        }
    }
}
