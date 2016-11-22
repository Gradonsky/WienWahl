__author__ = "Gradonski Janusz"
__version__ = "1.0"

from PySide.QtGui import *
class EditCommand(QUndoCommand):
     """ Edit the selected cell
     :var __model: QTableModel: Model for command
     :var __index: QModelIndex: selected cell
     :var __oldValue: string: value before redo command executed
     :var __newValue: string: value before undo command executed
     """
     def redo(self):
        self.__oldValue = self.__model.data(self.__index)
        self.__model.setData(self.__index, self.__newValue)
     def undo(self):
        self.__newValue = self.__model.data(self.__index)
        self.__model.setData(self.__index, self.__oldValue)
     def setText(self, *args, **kwargs):
        super().setText(*args, **kwargs)
     def __init__(self, model, index):
        """
        :param model: QTableModel
        :param index: QModelIndex
        :return: None
        """
        QUndoCommand.__init__(self)
        self.__newValue = None
        self.__model = model
        self.__index = index
        self.__oldValue = None
     def newValue(self, newValue):
        self.__newValue = newValue

class AddRowCommand(QUndoCommand):
    """
    Eine neue Zeile wird hinzugefügt
    """
    def redo(self):
        self.__model.insertRow(self.__currentrow+1)

    def undo(self):
        self.__model.takeRow(self.__currentrow+1)

    def __init__(self, model, currentrow):
        """
        :param model: QTableModel
        :param currentrow: QModelIndex
        :return:
        """
        QUndoCommand.__init__(self)
        self.__model = model
        self.__currentrow = currentrow


class DeleteCommand(QUndoCommand):
    """
    Eine Zeile wird gelöscht
    """
    def redo(self):
        self.__model.takeRow(self.__currentrow)

    def undo(self):
        self.__model.insertRow(self.__currentrow)
        for column in range(self.__model.columnCount()):
            index = self.__model.index(self.__currentrow, column)
            self.__model.setData(index, self.__data[column])

    def __init__(self, model, currentrow, data):
        """
        :param model: StandardItemModel
        :param currentrow: Zeile die gelöscht wird
        :param data: gesammtes Standarditemmodel als Liste
        :return: None
        """
        QUndoCommand.__init__(self)
        self.__model = model
        self.__currentrow = currentrow
        self.__data = data


class DuplicateCommand(QUndoCommand):
    """
    Zeile wird dupliziert
    """
    def redo(self):
        self.__model.insertRow(self.__currentrow)
        for column in range(self.__model.columnCount()):
            index = self.__model.index(self.__currentrow, column)
            self.__model.setData(index, self.__data[column])

    def undo(self):
        self.__model.takeRow(self.__currentrow)

    def __init__(self, model, currentrow, data):
        """
        :param model: StandardItemModel
        :param currentrow: Zeile die gelöscht wird
        :param data: gesammtes Standarditemmodel als Liste
        :return: None
        """
        QUndoCommand.__init__(self)
        self.__model = model
        self.__currentrow = currentrow
        self.__data = data

class PasteAction(QAction):
    """
    Erstllt die Einfüge-Funktion
    """
    def __init__(self, display, tableView, **kwargs):
        super(PasteAction, self).__init__(display, tableView)
        self.setShortcut(kwargs["shortcut"])
        self.setStatusTip(kwargs["statusTip"])
        self.undoStack = kwargs["undoStack"]
        self.triggered.connect(self.paste_clipboard_to_cell)
        self.tableView = tableView
        self.model = tableView.model()
    def paste_clipboard_to_cell(self):
        if len(self.tableView.selectionModel().selectedIndexes()) > 0:
            # get index of the selected cell
            sys_clip = QApplication.clipboard()
            value = str(sys_clip.text())
            index = self.tableView.selectionModel().selectedIndexes()[0]
            cmd = EditCommand(self.model, index)
            cmd.newValue(value)
            self.undoStack.push(cmd)


class CopyAction(QAction):
    """
    Erstellt die Kopierfunktion
    """
    def __init__(self, display, tableView, **kwargs):
        super(CopyAction, self).__init__(display, tableView)
        self.setShortcut(kwargs["shortcut"])
        self.setStatusTip(kwargs["statusTip"])
        self.undoStack = kwargs["undoStack"]
        self.triggered.connect(self.copy_cell_to_clipboard)
        self.tableView = tableView
        self.model = tableView.model()

    def copy_cell_to_clipboard(self):
        if len(self.tableView.selectionModel().selectedIndexes()) > 0:
            # get index of the selected cell
            index = self.tableView.selectionModel().selectedIndexes()[0]
            QApplication.clipboard().setText(self.model.data(index))
            cmd = EditCommand(self.model, index)
            cmd.newValue(self.model.data(index))
            self.undoStack.push(cmd)

class CutAction(QAction):
    """
    Erstellt die Ausschneide Funktion
    """
    def __init__(self, display, tableView, **kwargs):
        super(CutAction, self).__init__(display, tableView)
        self.setShortcut(kwargs["shortcut"])
        self.setStatusTip(kwargs["statusTip"])
        self.undoStack = kwargs["undoStack"]
        self.triggered.connect(self.cut_cell_to_clipboard)
        self.tableView = tableView
        self.model = tableView.model()

    def cut_cell_to_clipboard(self):
        if len(self.tableView.selectionModel().selectedIndexes()) > 0:
            # get index of the selected cell
            index = self.tableView.selectionModel().selectedIndexes()[0]
            QApplication.clipboard().setText(self.model.data(index))
            cmd = EditCommand(self.model, index)
            cmd.newValue("")
            self.undoStack.push(cmd)

class AddRowAction(QAction):
    """
    Erstellt die Funktion zum Einfügen einer Zeile
    """
    def __init__(self, display, tableView, **kwargs):
        super(AddRowAction, self).__init__(display, tableView)
        self.setShortcut(kwargs["shortcut"])
        self.setStatusTip(kwargs["statusTip"])
        self.undoStack = kwargs["undoStack"]
        self.triggered.connect(self.add_row_to_clipboard)
        self.tableView = tableView
        self.model = tableView.model()

    def add_row_to_clipboard(self):
        if len(self.tableView.selectionModel().selectedIndexes()) > 0:
            # get index of the selected cell
            index = self.tableView.selectionModel().selectedIndexes()[0]
            row = index.row()
            cmd = AddRowCommand(self.model, row)
            self.undoStack.push(cmd)

class DeleteAction(QAction):
    """
    Erstellt die Funktion zum Löschen einer Zeile
    """
    def __init__(self, display, tableView, **kwargs):
        super(DeleteAction, self).__init__(display, tableView)
        self.setShortcut(kwargs["shortcut"])
        self.setStatusTip(kwargs["statusTip"])
        self.undoStack = kwargs["undoStack"]
        self.triggered.connect(self.delete_row)
        self.tableView = tableView
        self.model = tableView.model()

    def delete_row(self):
        if len(self.tableView.selectionModel().selectedIndexes()) > 0:
            # get index of the selected cell
            index = self.tableView.selectionModel().selectedIndexes()[0]
            row = index.row()
            data = []

            for column in range(self.model.columnCount()):
                index = self.model.index(row, column)
                if self.model.data(index) is not None:
                    data.append(str(self.model.data(index)))
                else:
                    data.append("")

            cmd = DeleteCommand(self.model, row, data)
            self.undoStack.push(cmd)
class DuplicateAction(QAction):
    """
    Erstellt die Funktion zum Duplizieren einer Zeile
    """
    def __init__(self, display, tableView, **kwargs):
        super(DuplicateAction, self).__init__(display, tableView)
        self.setShortcut(kwargs["shortcut"])
        self.setStatusTip(kwargs["statusTip"])
        self.undoStack = kwargs["undoStack"]
        self.triggered.connect(self.duplicate_row)
        self.tableView = tableView
        self.model = tableView.model()

    def duplicate_row(self):
        if len(self.tableView.selectionModel().selectedIndexes()) > 0:
            # get index of the selected cell
            index = self.tableView.selectionModel().selectedIndexes()[0]
            row = index.row()
            data = []

            for column in range(self.model.columnCount()):
                index = self.model.index(row, column)
                if self.model.data(index) is not None:
                    data.append(str(self.model.data(index)))
                else:
                    data.append("")

            cmd = DuplicateCommand(self.model, row, data)
            self.undoStack.push(cmd)

