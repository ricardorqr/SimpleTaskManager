import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from common.util import Util

Ui_MainWindow, QtBaseClass = uic.loadUiType(Util.find_file("taskManagerUI.ui"))
tick = QtGui.QImage(Util.find_file("tick.png"))


class TodoModel(QtCore.QAbstractListModel):

    def __init__(self, *args, todos=None, **kwargs):
        super(TodoModel, self).__init__(*args, **kwargs)
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.todos[index.row()]
            return text

        if role == Qt.DecorationRole:
            status, _ = self.todos[index.row()]
            if status:
                return tick

    def rowCount(self, index):
        return len(self.todos)


class TaskManagerController(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = TodoModel()
        self.load()
        self.listView.setModel(self.model)
        self.pushButtonAdd.pressed.connect(self.add)
        self.pushButtonDelete.pressed.connect(self.delete)
        self.pushButtonComplete.pressed.connect(self.complete)

    def add(self):
        text = self.lineEdit.text()
        if text:
            self.model.todos.append((False, text))
            self.model.layoutChanged.emit()
            self.lineEdit.setText("")
            self.save()

    def delete(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.listView.clearSelection()
            self.save()

    def complete(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal 
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.listView.clearSelection()
            self.save()

    def load(self):
        try:
            with open(Util.find_file('data.db'), 'r') as f:
                self.model.todos = json.load(f)
        except Exception:
            pass

    def save(self):
        with open(Util.find_file('data.db'), 'w') as f:
            data = json.dump(self.model.todos, f)
