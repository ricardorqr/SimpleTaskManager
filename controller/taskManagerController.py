import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from common.util import Util

Ui_MainWindow, QtBaseClass = uic.loadUiType(Util.find_file("taskManagerUI.ui"))
tick = QtGui.QImage(Util.find_file("tick.png"))


class TaskModel(QtCore.QAbstractListModel):

    def __init__(self, *args, task=None, **kwargs):
        super(TaskModel, self).__init__(*args, **kwargs)
        self.task = task or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.task[index.row()]
            return text

        if role == Qt.DecorationRole:
            status, _ = self.task[index.row()]
            if status:
                return tick

    def rowCount(self, index):
        return len(self.task)


class TaskManagerController(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.__model = TaskModel()
        self.__load()

        # TaskManagerUi widget components
        self.setupUi(self)
        self.listView.setModel(self.__model)
        self.pushButtonAdd.pressed.connect(self.__add)
        self.pushButtonDelete.pressed.connect(self.__delete)
        self.pushButtonComplete.pressed.connect(self.__complete)
        self.pushButtonIncomplete.pressed.connect(self.__incomplete)

    def __add(self):
        text = self.lineEdit.text()
        if text:
            self.__model.task.append((False, text))
            self.__model.layoutChanged.emit()
            self.lineEdit.setText("")
            self.__save()

    def __delete(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self.__model.task[index.row()]
            self.__model.layoutChanged.emit()
            self.listView.clearSelection()
            self.__save()

    def __complete(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.__model.task[row]
            self.__model.task[row] = (True, text)
            self.__model.dataChanged.emit(index, index)
            self.listView.clearSelection()
            self.__save()

    def __incomplete(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.__model.task[row]
            self.__model.task[row] = (False, text)
            self.__model.dataChanged.emit(index, index)
            self.listView.clearSelection()
            self.__save()

    def __load(self):
        try:
            with open(Util.find_file('data.db'), 'r') as file:
                self.__model.task = json.load(file)
        except Exception:
            pass

    def __save(self):
        with open(Util.find_file('data.db'), 'w') as file:
            json.dump(self.__model.task, file)
