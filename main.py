import sys
from controller.taskManagerController import TaskManagerController
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
window = TaskManagerController()
window.show()
app.exec_()
