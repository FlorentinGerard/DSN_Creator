from PyQt5.QtWidgets import *
from ReadDsnNorm import *
from BlockConfWidget import BlockConfWidget
import sys

app = QApplication(sys.argv)
mainWindow = QMainWindow()
mainWindow.resize(1200, 800)

sa = QScrollArea()
sa.setWidgetResizable(True)
sa.setFrameStyle(QFrame.NoFrame)
mainWindow.setCentralWidget(sa)
w = QWidget()
sa.setWidget(w)
wLayout = QVBoxLayout()
b = BlockConfWidget(wLayout, bcr, 0)
w.setLayout(wLayout)
mainWindow.show()
app.exec_()
