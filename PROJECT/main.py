import os
import sys

# noinspection PyUnresolvedReferences
from PyQt5.uic import loadUi
# noinspection PyUnresolvedReferences

from tables import *


class Connections:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.listOfTableObjects = [Studenti(), Acte(), Optiuni(), Administratori(), Camine(), Camere(), TipuriActe(),
                                   Facultati(), Punctaje(), Studenti_Optiuni()]
        self.listOfInsertPopUp = [StudentiInsertPopUp(self.mainWindow), OptiuniInsertPopUp(self.mainWindow),
                                  AdministratoriInsertPopUp(self.mainWindow), ActeInsertPopUp(self.mainWindow),
                                  CamereInsertPopUp(self.mainWindow), PunctajeInsertPopUp(self.mainWindow)]
        self.listOfUpdatePopUp = [StudentiUpdatePopUp(self.mainWindow), OptiuniUpdatePopUp(self.mainWindow),
                                  PunctajeUpdatePopUp(self.mainWindow), ActeUpdatePopUp(self.mainWindow),
                                  AdministratoriUpdatePopUp(self.mainWindow), CamereUpdatePopUp(self.mainWindow)]
        self.errPopUp = EroarePopUp(self.mainWindow)

    def procedureDisplay(self):
        tableName = self.mainWindow.selectTableBox.currentText()
        for i in self.listOfTableObjects:
            if str(i) == tableName:

                i.loadData(self.mainWindow.displayWindow)

    def procedureInsert(self):
        found = False
        insertPopUp = self.mainWindow.selectTableBox.currentText()
        for i in self.listOfInsertPopUp:
            if str(i) == insertPopUp:
                i.show()
                for j in self.listOfTableObjects:
                    if str(j) == insertPopUp:
                        found = True
                        j.insertData(i, self.errPopUp)
        if not found:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                                  "Nu se poate face INSERT in aceasta tabela!")

    def procedureUpdate(self):
        found = False
        updatePopUp = self.mainWindow.selectTableBox.currentText()
        for i in self.listOfUpdatePopUp:
            if str(i) == updatePopUp:
                for j in self.listOfTableObjects:
                    if str(j) == updatePopUp:
                        j.updateData(i, self.errPopUp, self.mainWindow.displayWindow)
                        found = True
        if not found:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                                  "Nu se poate face UPDATE la aceasta tabela!")

    def procedureDelete(self):
        tableName = self.mainWindow.selectTableBox.currentText()
        for i in self.listOfTableObjects:
            if str(i) == tableName:
                i.delete(self.mainWindow.displayWindow, self.errPopUp)


class StudentiInsertPopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'studentiInsertPopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.facultateBox.clear()
        self.judetBox.clear()
        self.numeEdit.clear()
        self.domiciliuEdit.clear()
        self.telefonEdit.clear()
        self.emailEdit.clear()
        self.localitateEdit.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "STUDENTI"


class OptiuniInsertPopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'optiuniInsertPopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.nrMatricolBox.clear()
        self.nrCameraBox.clear()
        self.codCaminBox.clear()
        self.coleg1Box.clear()
        self.coleg2Box.clear()
        self.coleg3Box.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "OPTIUNI"


class AdministratoriInsertPopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'adminInsertPopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.numeEdit.clear()
        self.telefonEdit.clear()
        self.emailEdit.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "ADMINISTRATORI"


class ActeInsertPopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'acteInsertPopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.nrMatricolBox.clear()
        self.denumireActBox.clear()
        self.serieActEdit.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "ACTE"


class CamereInsertPopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'camereInsertPopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.codCaminBox.clear()
        self.nrCameraBox.clear()
        self.nrLocuriBox.clear()
        self.tipBaieBox.clear()
        self.pretBox.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "CAMERE"


class PunctajeInsertPopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'punctajeInsertPopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.nrMatricolBox.clear()
        self.bonusEdit.clear()
        self.medieStudentEdit.clear()
        self.nrCrediteEdit.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "PUNCTAJE"


class StudentiUpdatePopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'updateStudenti.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.nrMatricolBox.clear()
        self.facultateBox.clear()
        self.judetBox.clear()
        self.numeEdit.clear()
        self.domiciliuEdit.clear()
        self.telefonEdit.clear()
        self.emailEdit.clear()
        self.localitateEdit.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "STUDENTI"


class OptiuniUpdatePopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'updateOptiuni.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.nrMatricolBox.clear()
        self.nrCameraBox.clear()
        self.codCaminBox.clear()
        self.coleg1Box.clear()
        self.coleg2Box.clear()
        self.coleg3Box.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "OPTIUNI"


class PunctajeUpdatePopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'updatePunctajePopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.nrMatricolBox.clear()
        self.bonusEdit.clear()
        self.medieStudentEdit.clear()
        self.nrCrediteEdit.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "PUNCTAJE"


class ActeUpdatePopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'updateActePopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.nrMatricolBox.clear()
        self.denumireActBox.clear()
        self.serieActEdit.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "ACTE"


class AdministratoriUpdatePopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'updateAdminPopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.numeEdit.clear()
        self.telefonEdit.clear()
        self.emailEdit.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "ADMINISTRATORI"


class CamereUpdatePopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'updateCamerePopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.cancelInsert.clicked.connect(self.delete_close)

    def delete_close(self):
        self.codCaminBox.clear()
        self.nrCameraBox.clear()
        self.nrLocuriBox.clear()
        self.tipBaieBox.clear()
        self.pretBox.clear()
        self.close()

    @staticmethod
    def isSignalConnected1(obj, name):
        index = obj.metaObject().indexOfMethod(name)
        if index > -1:
            method = obj.metaObject().method(index)
            if method:
                return obj.isSignalConnected(method)
        return False

    def __repr__(self):
        return "CAMERE"


class EroarePopUp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.ui_path = os.path.join(self.ROOT_DIR, 'eroarePopUp.ui')
        loadUi(self.ui_path, self)
        self.file_path = None
        self.okButton.clicked.connect(self.delete_close)

    def delete_close(self):
        self.eroareEdit.clear()
        self.close()

    def __repr__(self):
        return "EROARE"


class MainWindow(QMainWindow):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super(MainWindow, self).__init__()
        ui_path = os.path.join(self.ROOT_DIR, 'mainWindow.ui')
        loadUi(ui_path, self)
        self.file_path = None
        self.connections = Connections(self)

        self.displayTable.clicked.connect(self.connections.procedureDisplay)
        self.clearDisplay.clicked.connect(self.clearTable)
        self.insertIntoTable.clicked.connect(self.connections.procedureInsert)
        self.updateTable.clicked.connect(self.connections.procedureUpdate)
        self.deleteFromTable.clicked.connect(self.connections.procedureDelete)
        self.deselect.clicked.connect(self.clearSelection2)
        self.displayWindow.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.fillSelectTableBox()

    def fillSelectTableBox(self):
        query = " SELECT TABLE_NAME FROM cat WHERE TABLE_TYPE = 'TABLE'"
        result = connection.cursor()
        result.execute(query)
        for i in result:
            self.selectTableBox.addItem(i[0])
        # self.selectTableBox.addItem("STUDENTI_OPTIUNI")
        self.selectTableBox.activated[str].connect(self.onActivated)

    def onActivated(self):
        self.clearTable()

    def clearTable(self):
        self.displayWindow.clear()
        self.displayWindow.setRowCount(0)
        self.displayWindow.setColumnCount(0)

    def clearSelection2(self):
        self.displayWindow.clearSelection()
        self.displayWindow.setCurrentCell(-1, -1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.raise_()
    sys.exit(app.exec_())
