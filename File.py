__author__ = "Gradonski Janusz"
__version__ = "1.0"

from PySide import QtGui
import csv
from CSV_Methods import CSV_Methods
from PySide import QtGui
class File(object):
    """
    Klasse die alle File-Methoden zu Verfügung stellt
    """
    def __init__(self,  myform, model):
        """
        Konstruktor
        :param myform: das Fenster
        :param model: das Standarditemmodel im Fenster
        """
        self.myform = myform
        self.model = model
        self.csv1 = CSV_Methods()
        self.isSaved = True
        self.filename = ''
        self.fileOpen = False


    def openFile(self):

        """
        Öffnet ein File. Der Dateipfad kann angegeben werden
        """
        if self.fileOpen == True and self.isSaved == False:
            self.safeFileAs()

        name = QtGui.QFileDialog.getOpenFileName(self.myform.centralwidget, 'Open file')
        self.filename = name[0]
        self.isSaved = True

        if self.fileOpen == True:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Wollen Sie das File an das Andere anfügen?")
            msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            msgBox.setDefaultButton(QtGui.QMessageBox.Save)
            ret = msgBox.exec_()

            if ret == QtGui.QMessageBox.No:
              self.model.clear()

        file = self.csv1.openFile(self.filename,'r')
        dialect = self.csv1.sniffDialect(file)


        for row in csv.reader(file, dialect):
            items = [
                QtGui.QStandardItem(field)
                for field in row
            ]
            self.model.appendRow(items)


        self.fileOpen = True




    def newFile(self):
        """
        Erstellt ein neues File mit 10x10
        """
        firstRow = [
            "T", "WV", "WK", "BZ", "SPR", "WBER", "ABG", "UNG", "SPOE",
            "FPOE", "OEVP", "GRUE", "NEOS", "WWW", "ANDAS", "GFW", "SLP", "WIFF", "M", "FREIE"
        ]

        if self.fileOpen == True and self.isSaved == True:
            self.safeFileAs()
        self.isSaved = True
        self.model.clear()
        self.model.setColumnCount(20)
        self.model.setRowCount(400)
        for i in range(20):
            self.model.setData(self.model.index(0, i), firstRow[i])

        self.fileOpen = True



    def safe(self):
        list = []

        for i in range(self.model.rowCount()):
            list.append([])
            for j in range(self.model.columnCount()):
                list[i].append(self.model.data(self.model.index(i,j)))


        out = self.csv1.openFile(self.filename,'w')
        self.csv1.writeFile(out,list,'Semikolon',';')
        self.isSaved = True

    def safeFile(self):
        """
        Speichert das File ohne Frage nach Namen und Dateipfad
        """
        if self.isSaved:
            self.safe()
        else:
            name = QtGui.QFileDialog.getSaveFileName(self.myform.centralwidget,'Save file', '')
            self.filename = name[0]
            self.safe()
            self.isSaved = True

    def safeFileAs(self):
        """
        Speichert das File mit Frage nach Namen und Dateipfad
        """
        name = QtGui.QFileDialog.getSaveFileName(self.myform.centralwidget,'Save file', '')
        self.filename = name[0]
        self.safeFile()
        self.isSaved = True









