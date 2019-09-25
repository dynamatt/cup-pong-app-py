# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl

class CupPong(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setSource(QUrl('qrc:///main.qml'))

    def init_ui(self):
        self.resize(480, 320)

if __name__ == "__main__":
    app = QApplication([])
    #window = CupPong()
    #window.show()

    view = QQuickView()
    view.setSource(QUrl('main.qml'))
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.show()

    sys.exit(app.exec_())
