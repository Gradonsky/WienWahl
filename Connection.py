__author__ = "Gradonski Janusz"
__version__ = "1.0"

from sqlalchemy import *
from sqlalchemy.ext.automap import *
from sqlalchemy.orm import *
import time
import datetime
from Hochrechnung import Hochrechnung

class Connection(object):
    """
    Die Verbindung zur Datenbank
    """
    def __init__(self,link,model):
        """
        Konstruktor
        :param link: link der zur Verbindung der Datenbank benötigt wird
        :param model: das Standarditemmodel das im View angezeigt wird
        """
        self.link = link
        self.model = model
    def connect(self):
        """
        Verbindet sich zur Datenbank und liest die Datein des Csv-Files ein
        :return:
        """
        self.date = '2015-10-11'
        engine = create_engine(self.link)
        conn = engine.connect()
        # create declarative base class
        Base = automap_base()
        # create declarative classes from dbms
        Base.prepare(engine, reflect=True)
        # create references for all reflected tables

        ts = time.time()
        st1 = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        wahl = Base.classes.wahl
        parteistimmen = Base.classes.parteistimmen
        sprengel = Base.classes.sprengel
        kandidatur = Base.classes.kandidatur
        s = Session(engine)

        s.add(wahl(termin = self.date, mandate= 100))


        for i in range(self.model.rowCount()-1):
            s.add(sprengel(snr=self.model.data(self.model.index(i+1, 4)), bnr=self.model.data(self.model.index(i+1, 3)),
                           termin=self.date, abgstimmen=self.model.data(self.model.index(i+1, 6)),
                           wber=self.model.data(self.model.index(i+1, 5)),
                           ung=self.model.data(self.model.index(i+1, 7))))




        for i in range(self.model.rowCount()-1):
            i1 = self.model.data(self.model.index(i+1, 3))
            i2 = self.model.data(self.model.index(i+1, 4))
            j2 = 8
            for j in range(12):
                i3 = self.model.data(self.model.index(i+1, j2))
                s.add(parteistimmen(bnr=i1, snr=i2, pname=self.model.data(self.model.index(0, j2)),
                                    termin=self.date, gstimmen=i3))
                j2 += 1
        wnr = 0

        j2 = 8
        if wnr != self.model.data(self.model.index(i+1, 2)):
            for j in range(12):
                s.add(kandidatur(pname=self.model.data(self.model.index(0, j2)),
                wnr=self.model.data(self.model.index(i+1, 2)),
                termin=self.date, listenplatz=j))
                j2 += 1















        s.commit()

        s.execute("Call erzeugeHochrechnung('" + self.date + "', '" + st1 + "');")

        r = s.execute("SELECT * FROM hochrechnungsdaten ORDER BY prozent DESC Limit 5;")

        s.commit()

        h = Hochrechnung(r)









