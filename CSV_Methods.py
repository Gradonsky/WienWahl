__author__ = "Gradonski Janusz"
__version__ = "1.0"

import csv

class CSV_Methods(object):
    """
    Klasse die alle möglichen Methoden für Files zu Verfügung stellt
    """
    def openFile(self, file, rw):
        """
        Öffnet ein File
        :param file: das File
        :param rw: Lese oder Schreibrechte
        :return: gibt das File zurück
        """
        file = open(file, rw, newline='')
        return file
    def sniffDialect(self, file):
        """
        Sucht den Dialect des Files
        :param file: das File in dem der Dialect gesucht wird
        :return: git den Dialect zurück
        """
        dialect = csv.Sniffer().sniff(file.read(1024))
        file.seek(0)
        return dialect
    def writeFile(self,file,list,dialcet, delimiter):
        """
        Schreib in ein File
        :param file: das File in welches geschrieben wird
        :param list: eine Liste in der der Text steht
        :param dialcet: der Dialcet der verwendet werden soll
        :param delimiter: der Delimiter des Dialects
        """
        csv.register_dialect(dialcet, delimiter=delimiter)
        writer = csv.writer(file, dialect=dialcet, quoting=csv.QUOTE_NONE, quotechar='')
        for all in list:
            writer.writerow(all)
    def readFile(self,file,dialect):
        """
        Das File wird gelesen und in eine Liste geschrieben
        :param file: das File welches gelesen wird
        :param dialect: der Dialect des Files
        :return: die Liste
        """
        list = []
        for row in csv.reader(file, dialect):
            list.append(row)
        return list
    def closeFile(self, file):
        """
        Schließt ein File
        :param file: das File welches geschlossen wird
        """
        file.close




