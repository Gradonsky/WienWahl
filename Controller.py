__author__ = "Gradonski Janusz"
__version__ = "1.0"

from PySide import QtCore, QtGui
from File import File
from Table_Actions import *
import sys
import View
import view_database
from Connection import Connection

from PySide.QtGui import *
class MyController(QMainWindow):
    """ MVC pattern: Creates a controller - mvc pattern.
        Ruft die Klasse auf, welche das Fenster erzeugt.

    """
    def __init__(self, parent=None):
        """
        Konstrukotr der Klasse MyController
        """

        super().__init__(parent)
        self.myForm = View.Ui_MainWindow()
        self.dbcon = view_database.Ui_MainWindow()

        self.myForm.setupUi(self)
        self.model = QtGui.QStandardItemModel(self)

        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(0, 0, 981, 581))
        self.tableView.setModel(self.model)
        self.tableView.setObjectName("tableView")
        self.setCentralWidget(self.centralwidget)

        self.undoStack = QUndoStack()

        self.copyAct = CopyAction("&Copy", self.tableView,
                               shortcut=QKeySequence.Copy,
                               undoStack=self.undoStack,
                               statusTip="Kopieren")
        self.pasteAct = PasteAction("&Paste", self.tableView,
                                 shortcut=QKeySequence.Paste,
                                 undoStack=self.undoStack,
                                 statusTip="Einfügen")
        self.cutAct = CutAction("&Cut", self.tableView,
                                 shortcut=QKeySequence.Cut,
                                 undoStack=self.undoStack,
                                 statusTip="Ausschneiden")
        self.rowAct = AddRowAction("&Add Row", self.tableView,
                                 shortcut='',
                                 undoStack=self.undoStack,
                                 statusTip="Zeile Einfügen")
        self.delAct = DeleteAction("&Delete Row", self.tableView,
                                 shortcut='',
                                 undoStack=self.undoStack,
                                 statusTip="Zeile Löschen")
        self.dupAct = DuplicateAction("&Duplicate Row", self.tableView,
                                 shortcut='',
                                 undoStack=self.undoStack,
                                 statusTip="Zeile Duplizieren")

        self.undoAction = self.undoStack.createUndoAction(self, self.tr("&Undo"))
        self.undoAction.setShortcuts(QKeySequence.Undo)
        self.undoAction.setStatusTip("undo the last action")
        self.redoAction = self.undoStack.createRedoAction(self, self.tr("&Redo"))
        self.redoAction.setShortcuts(QKeySequence.Redo)
        self.redoAction.setStatusTip("redo the last action")


        self.f = File(self,self.model)
        QtCore.QObject.connect(self.myForm.actionOpen, QtCore.SIGNAL("activated()"), self.f.openFile)
        QtCore.QObject.connect(self.myForm.actionSave, QtCore.SIGNAL("activated()"), self.f.safeFile)
        QtCore.QObject.connect(self.myForm.actionSave_As, QtCore.SIGNAL("activated()"), self.f.safeFileAs)
        QtCore.QObject.connect(self.myForm.actionNew, QtCore.SIGNAL("activated()"), self.f.newFile)
        QtCore.QObject.connect(self.myForm.actionConnect, QtCore.SIGNAL("activated()"),self.db)




        self.myForm.menuEdit.addAction(self.undoAction)
        self.myForm.menuEdit.addAction(self.redoAction)
        self.myForm.menuEdit.addSeparator()
        self.myForm.menuEdit.addAction(self.cutAct)
        self.myForm.menuEdit.addAction(self.copyAct)
        self.myForm.menuEdit.addAction(self.pasteAct)
        self.myForm.menuEdit.addSeparator()
        self.myForm.menuEdit.addAction(self.rowAct)
        self.myForm.menuEdit.addAction(self.delAct)
        self.myForm.menuEdit.addAction(self.dupAct)


    def db(self):
        """
        Ruft ein Fenster zum Verbinden zur Datenbank auf
        """

        self.window = QtGui.QMainWindow()
        self.dbcon.setupUi(self.window)
        self.window.show()
        self.dbcon.pushButton.clicked.connect(self.listener)




    def listener(self):
        """
        Listener des Button "Connect"
        """

        ip = self.dbcon.lineEdit.text()
        um = self.dbcon.lineEdit_2.text()
        pw = self.dbcon.lineEdit_3.text()
        db = self.dbcon.lineEdit_4.text()

        """ip = 'localhost'
        um = 'ww'
        pw = 'ww'
        db = 'wienwahl'"""
        dbms = 'MYSQL'



        if dbms == 'MYSQL':
            link = 'mysql+mysqldb://'
        link += um + ':' + pw + '@' + ip + '/' + db + '?charset=utf8'





        self.conn = Connection(link,self.model)
        self.conn.connect()
        self.window.close()









if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = MyController()
    c.show()
    sys.exit(app.exec_())