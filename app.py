from mavrControl import mainGui
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
m = mainGui.mainGUI()
m.show()
app.exec_()