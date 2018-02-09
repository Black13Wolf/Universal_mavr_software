from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
class mainGUI(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.mainWidget = QWidget()
        self.mainLayout = QGridLayout()
        self.label = QLabel('LINUX MAVR SOFTWARE. VER: {}'.format(__version__))
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    g = GUI()
    g.show()
    app.exec_()