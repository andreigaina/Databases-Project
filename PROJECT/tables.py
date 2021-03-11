import threading

import cx_Oracle
import re

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import *
from datetime import date

today = date.today()
connection = cx_Oracle.connect("andreibdp", "1234567", "localhost/xe")


class Studenti:
    f = open("A:\Andrei\Facultate\AN3SEM1\BD\Tema\judete.txt", "r")

    def __init__(self):
        self.dialogBox = None
        self.errPopUp = None
        self.displayWindow = None
        self.judete = self.f.read().split("\n")
        self.f.close()

    @staticmethod
    def loadData(displayWindow):
        query = ' SELECT NR_MATRICOL \"Numar matricol \", NUME_STUDENT \"Nume student\", DOMICILIU, ' \
                'LOCALITATE, JUDET, EMAIL_STUDENT \"Email\", TELEFON_STUDENT \"Telefon\", ' \
                'COD_FACULTATE \"Cod facultate\" FROM studenti '
        col_cnt = "select count(*) from USER_TAB_COLUMNS where TABLE_NAME='STUDENTI'"
        results = connection.cursor()
        results.execute(col_cnt)
        for i in results:
            displayWindow.setColumnCount(i[0])
        results.execute(query)
        displayWindow.setRowCount(0)
        for row_number, row_data in enumerate(results):
            displayWindow.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                displayWindow.setHorizontalHeaderItem(column_number,
                                                      QTableWidgetItem(str(results.description[column_number][0])))
                displayWindow.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self, dialogBox, errPopUp):
        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        query = 'SELECT COD_FACULTATE FROM FACULTATI'
        results = connection.cursor()
        results.execute(query)
        self.dialogBox.facultateBox.clear()
        for i in results:
            self.dialogBox.facultateBox.addItem(i[0])
        self.dialogBox.judetBox.clear()
        for i in self.judete:
            self.dialogBox.judetBox.addItem(i)
        if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
            self.dialogBox.okInsert.clicked.connect(self.verifyData)

    def verifyData(self):
        results = connection.cursor()
        judet = self.dialogBox.judetBox.currentText()
        cod_facultate = self.dialogBox.facultateBox.currentText()
        nume = re.search("^([a-zA-Z]{2,}\s[a-zA-Z]{1,}'?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)", self.dialogBox.numeEdit.text())
        domiciliu = re.search("^[a-zA-Z., 0-9-]+$", self.dialogBox.domiciliuEdit.toPlainText())
        localitate = re.search("^[A-Z][-A-Za-z-]+$", self.dialogBox.localitateEdit.text())
        telefon = re.search("^(07)\d{8}$", self.dialogBox.telefonEdit.text())
        email = re.search("[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}", self.dialogBox.emailEdit.text())
        telefon_uk_ck = 1
        if telefon is not None:
            telefon_uk = "SELECT TELEFON_STUDENT FROM STUDENTI WHERE TELEFON_STUDENT ='%s'" % telefon.string
            telefon_uk = results.execute(telefon_uk)
            for i in telefon_uk:
                if i:
                    telefon_uk_ck = 0

        email_uk_ck = 1
        if email is not None:
            email_uk = "SELECT EMAIL_STUDENT FROM STUDENTI WHERE EMAIL_STUDENT ='%s'" % email.string
            email_uk = results.execute(email_uk)
            for i in email_uk:
                if i:
                    email_uk_ck = 0

        if nume is not None and \
                domiciliu is not None and \
                localitate is not None and \
                telefon is not None and \
                telefon_uk_ck and email_uk_ck:
            if email is not None:
                command = "INSERT INTO STUDENTI VALUES (%s,'%s','%s','%s','%s','%s','%s','%s')" % ('NULL',
                                                                                                   nume.string,
                                                                                                   domiciliu.string,
                                                                                                   localitate.string,
                                                                                                   str(judet),
                                                                                                   email.string,
                                                                                                   telefon.string,
                                                                                                   str(cod_facultate))
            else:
                command = "INSERT INTO STUDENTI VALUES (%s,'%s','%s','%s','%s',%s,'%s','%s')" % ('NULL',
                                                                                                 nume.string,
                                                                                                 domiciliu.string,
                                                                                                 localitate.string,
                                                                                                 str(judet),
                                                                                                 'NULL',
                                                                                                 telefon.string,
                                                                                                 str(cod_facultate))
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            self.dialogBox.close()
        else:
            if telefon_uk_ck == 0:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                                      "Mai exista un student cu acelasi numar de telefon!")
                if email_uk_ck == 0:
                    self.errPopUp.eroareEdit.setPlainText(
                        "\t\tAtentie!\n\n        Mai exista un student cu acelasi numar de telefon!"
                        "\n De asemenea exista un student si cu aceeasi adresa de email!")
            elif email_uk_ck == 0:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n        "
                                                      "Mai exista un student cu aceeasi adresa de email!")
            else:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n\tAti uitat sa completati un camp cu date!"
                                                      "\n     Este posibil de asemenea sa fi completat un camp gresit!")

    @staticmethod
    def delete(displayWindow, errPopUp):
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            command = "DELETE FROM STUDENTI WHERE NR_MATRICOL= %s" % data[0]
            results.execute(command)
            displayWindow.removeRow(currentRow)
            results.execute('COMMIT WORK')  # tranzactie?
        else:
            errPopUp.show()
            errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                             "Trebuie sa selectati un row din tabela!")

    def updateData(self, dialogBox, errPopUp, displayWindow):
        self.displayWindow = displayWindow
        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            self.dialogBox.show()
            query = "SELECT NR_MATRICOL FROM STUDENTI"
            results.execute(query)
            self.dialogBox.nrMatricolBox.clear()
            for i in results:
                self.dialogBox.nrMatricolBox.addItem(str(i[0]))
            index = self.dialogBox.nrMatricolBox.findText(str(data[0]))
            self.dialogBox.nrMatricolBox.setCurrentIndex(index)

            query = 'SELECT COD_FACULTATE FROM FACULTATI'
            results.execute(query)
            self.dialogBox.facultateBox.clear()
            for i in results:
                self.dialogBox.facultateBox.addItem(i[0])
            index = self.dialogBox.facultateBox.findText(str(data[7]))
            self.dialogBox.facultateBox.setCurrentIndex(index)

            self.dialogBox.judetBox.clear()
            for i in self.judete:
                self.dialogBox.judetBox.addItem(i)
            index = self.dialogBox.judetBox.findText(str(data[4]))
            self.dialogBox.judetBox.setCurrentIndex(index)

            self.dialogBox.numeEdit.setText(data[1])
            self.dialogBox.domiciliuEdit.setPlainText(data[2])
            self.dialogBox.localitateEdit.setText(data[3])
            self.dialogBox.emailEdit.setText(data[5])
            self.dialogBox.telefonEdit.setText(data[6])
            self.dialogBox.nrMatricolBox.disconnect()
            self.dialogBox.nrMatricolBox.activated[str].connect(self.onActivated)
            if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
                self.dialogBox.okInsert.clicked.connect(self.verifyAndUpdate)
        else:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                                  "Trebuie sa selectati un row din tabela!")

    def verifyAndUpdate(self):
        results = connection.cursor()
        data = None
        query = 'SELECT * FROM STUDENTI WHERE NR_MATRICOL=%s' % int(self.dialogBox.nrMatricolBox.currentText())
        results.execute(query)
        self.errPopUp.eroareEdit.setPlainText("")
        for i in results:
            data = i
        modifications = False
        command = "UPDATE STUDENTI SET "
        if self.dialogBox.numeEdit.text() != data[1]:

            nume = re.search("^([a-zA-Z]{2,}\s[a-zA-Z]{1,}'?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)", self.dialogBox.numeEdit.text())
            if nume is not None:
                modifications = True
                command += "NUME_STUDENT = '%s'," % nume.string
            else:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                         "Nume invalid, acesta va ramane neschimbat!")
        if self.dialogBox.facultateBox.currentText() != data[7]:
            modifications = True
            command += "COD_FACULTATE = '%s'," % self.dialogBox.facultateBox.currentText()

        if self.dialogBox.domiciliuEdit.toPlainText() != data[2]:
            domiciliu = re.search("^[a-zA-Z., 0-9-]+$", self.dialogBox.domiciliuEdit.toPlainText())
            if domiciliu is not None:
                modifications = True
                command += "DOMICILIU='%s'," % domiciliu.string
            else:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                         "Domiciliul introdus este invalid."
                                                         "\n\tAcesta va ramane neschimbat!")
        if self.dialogBox.localitateEdit.text() != data[3]:
            localitate = re.search("^[A-Z][-A-Za-z-]+$", self.dialogBox.localitateEdit.text())

            if localitate is not None:
                modifications = True
                command += "LOCALITATE='%s'," % localitate.string
            else:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                         "Localitatea introdusa este invalida."
                                                         "\n\tAceasta va ramane neschimbata!")
        if self.dialogBox.judetBox.currentText() != data[4]:
            modifications = True
            command += "JUDET = '%s'," % self.dialogBox.judetBox.currentText()

        if self.dialogBox.telefonEdit.text() != data[6]:
            telefon = re.search("^(07)\d{8}$", self.dialogBox.telefonEdit.text())
            if telefon is not None:
                telefon_uk_ck = 1
                telefon_uk = "SELECT TELEFON_STUDENT FROM STUDENTI WHERE TELEFON_STUDENT ='%s'" % telefon.string
                telefon_uk = results.execute(telefon_uk)
                for i in telefon_uk:
                    if i:
                        telefon_uk_ck = 0
                        break
                if telefon_uk_ck:
                    modifications = True
                    command += "TELEFON_STUDENT='%s'," % telefon.string
                else:
                    self.errPopUp.show()
                    self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                    self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                             "Nr. de telefon introdus nu este unic.")
            else:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                         "Nr. de telefon introdus este invalid."
                                                         "\n\tAcesta va ramane neschimbat!")
        if self.dialogBox.emailEdit.text() != str(data[5]):
            email = re.search("[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}", self.dialogBox.emailEdit.text())
            if email is not None:
                email_uk_ck = 1
                email_uk = "SELECT EMAIL_STUDENT FROM STUDENTI" \
                           " WHERE EMAIL_STUDENT = '%s'" % email.string
                email_uk = results.execute(email_uk)
                for i in email_uk:
                    if i:
                        email_uk_ck = 0
                        break
                if email_uk_ck:
                    modifications = True
                    command += "EMAIL_STUDENT='%s'," % email.string
                else:
                    self.errPopUp.show()
                    self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                    self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                             "Email-ul introdus nu este unic.")
            else:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n"
                                                         "\tEmail-ul introdus este invalid."
                                                         "\n\tAcesta va ramane neschimbat!")

        if not modifications:
            # if not self.errPopUp.isVisible():
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Nu s-a modificat niciun camp.")
            self.dialogBox.close()
        else:
            command = command[:-1] + " WHERE NR_MATRICOL = %s" % int(self.dialogBox.nrMatricolBox.currentText())
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            self.dialogBox.close()
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Modificarile s-au efectuat cu succes!")
            self.loadData(self.displayWindow)

    def onActivated(self):
        query = "SELECT * FROM STUDENTI WHERE NR_MATRICOL = %s" % int(self.dialogBox.nrMatricolBox.currentText())
        results = connection.cursor()
        results.execute(query)
        for i in results:
            self.dialogBox.numeEdit.setText(i[1])
            self.dialogBox.domiciliuEdit.setPlainText(i[2])
            self.dialogBox.localitateEdit.setText(i[3])
            index = self.dialogBox.judetBox.findText(str(i[4]))
            self.dialogBox.judetBox.setCurrentIndex(index)
            self.dialogBox.emailEdit.setText(i[5])
            self.dialogBox.telefonEdit.setText(i[6])
            index = self.dialogBox.facultateBox.findText(str(i[7]))
            self.dialogBox.facultateBox.setCurrentIndex(index)

    def __repr__(self):
        return "STUDENTI"


class Acte:
    def __init__(self):
        self.dialogBox = None
        self.errPopUp = None
        self.displayWindow = None
        self.modifications = False
        self.thread = None
        self.currentTip = None

    @staticmethod
    def loadData(displayWindow):
        query = ' SELECT NR_MATRICOL \"Numar matricol\",(SELECT NUME_STUDENT FROM STUDENTI s ' \
                'WHERE s.NR_MATRICOL=ACTE.NR_MATRICOL ) \"Nume\",' \
                '(SELECT DENUMIRE_TIP_ACT FROM TIPURI_ACTE t WHERE acte.COD_TIP_ACT=t.COD_TIP_ACT) ' \
                ' \"Denumire act\",TO_CHAR(DATA_ACT,\'yyyy-mm-dd\') \"Data depunere act \",NR_ACT \"Serie&Numar\" ' \
                'FROM acte ORDER BY NR_MATRICOL'
        results = connection.cursor()
        col_cnt = "select count(*) from USER_TAB_COLUMNS where TABLE_NAME='ACTE'"

        results.execute(col_cnt)
        for i in results:
            displayWindow.setColumnCount(i[0])
        displayWindow.setColumnCount(displayWindow.columnCount() + 1)  # modificat
        results.execute(query)
        displayWindow.setRowCount(0)
        for row_number, row_data in enumerate(results):
            displayWindow.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                displayWindow.setHorizontalHeaderItem(column_number,
                                                      QTableWidgetItem(str(results.description[column_number][0])))
                displayWindow.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self, dialogBox, errPopUp):
        results = connection.cursor()
        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        query = 'SELECT DENUMIRE_TIP_ACT FROM TIPURI_ACTE'
        results.execute(query)
        self.dialogBox.denumireActBox.clear()
        for i in results:
            self.dialogBox.denumireActBox.addItem(i[0])
        self.currentTip = self.dialogBox.denumireActBox.currentText()
        query = "SELECT  s.NUME_STUDENT,s.NR_MATRICOL FROM STUDENTI s" \
                " minus select NUME_STUDENT,a.NR_MATRICOL from ACTE a, STUDENTI" \
                " where a.COD_TIP_ACT = (SELECT COD_TIP_ACT FROM TIPURI_ACTE WHERE DENUMIRE_TIP_ACT = '%s')" \
                " ORDER BY NR_MATRICOL" % self.dialogBox.denumireActBox.currentText()
        results.execute(query)
        self.dialogBox.nrMatricolBox.clear()
        for i in results:
            self.dialogBox.nrMatricolBox.addItem(re.sub(",", ' (Nr. matricol:', re.sub("[()']", '', str(i))) + ')')

        try:
            self.thread = threading.Thread(target=self.update)
            self.thread.start()
        except RuntimeError:
            print("Eroare la pornirea thread-ului!")
        if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
            dialogBox.okInsert.clicked.connect(self.verifyData)

    def update(self):
        results = connection.cursor()
        while True:
            if self.dialogBox.isVisible():
                if self.currentTip != self.dialogBox.denumireActBox.currentText():
                    self.dialogBox.nrMatricolBox.clear()
                    self.currentTip = self.dialogBox.denumireActBox.currentText()
                    query = "SELECT  s.NUME_STUDENT,s.NR_MATRICOL FROM STUDENTI s" \
                            " minus select NUME_STUDENT,a.NR_MATRICOL from ACTE a, STUDENTI" \
                            " where " \
                            "a.COD_TIP_ACT = (SELECT COD_TIP_ACT FROM TIPURI_ACTE WHERE DENUMIRE_TIP_ACT = '%s')" \
                            " ORDER BY NR_MATRICOL" % self.dialogBox.denumireActBox.currentText()
                    results.execute(query)
                    for i in results:
                        self.dialogBox.nrMatricolBox.addItem(
                            re.sub(",", ' (Nr. matricol:', re.sub("[()']", '', str(i))) + ')')
                    self.dialogBox.nrMatricolBox.setCurrentIndex(0)

            else:
                break

    def verifyData(self):
        if self.dialogBox.nrMatricolBox.currentIndex() != -1:
            results = connection.cursor()
            nr_matricol = re.sub("[a-zA-Z.:() ]+", '', self.dialogBox.nrMatricolBox.currentText())
            serie_act = re.search("^[A-Za-z0-9]{8}$", self.dialogBox.serieActEdit.text())
            date1 = str(self.dialogBox.dateEdit.date().toPyDate()).split('-')
            systemDate = today.strftime("%Y")
            serie_act_uk_ck = 1
            if serie_act is not None:
                serie_act_uk = "SELECT NR_ACT FROM ACTE WHERE NR_ACT ='%s'" % serie_act.string
                serie_act_uk = results.execute(serie_act_uk)
                for i in serie_act_uk:
                    if i:
                        serie_act_uk_ck = 0

            if serie_act is None:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n"
                                                      "\tSeria actului este incorecta!\n"
                                                      "\tDimensiunea acestui camp este de 8 caractere.")
            elif serie_act_uk_ck == 0:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n"
                                                      "\tSeria actului nu este unica!")
            elif date1[0] != str(systemDate) or int(date1[1]) != 9 or 11 > int(date1[2]) or int(date1[2]) > 19:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n"
                                                      "\tPerioada depunere acte expirata sau data invalida!\n"
                                                      "\tData depunerii actelor este in intervalul 11-19 Septembrie.")
            else:

                command = "INSERT INTO acte VALUES(" \
                          "(SELECT nr_matricol FROM studenti WHERE NR_MATRICOL = %s)," \
                          " (SELECT cod_tip_act FROM tipuri_acte WHERE denumire_tip_act= '%s')," \
                          "TO_DATE('%s-%s-%s', ' YYYY-MM-DD'),'%s')" \
                          % (int(nr_matricol), str(self.currentTip), int(date1[0]), int(date1[1]), int(date1[2]),
                             serie_act.string)
                results.execute(command)
                results.execute('COMMIT WORK')  # tranzactie?
                self.dialogBox.delete_close()
                if self.thread is not None:
                    self.thread.join()
                    # print(self.thread.is_alive())
        else:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\n\t\tAtentie!\n         "
                                                  "Nu mai sunt studenti care nu si-au ales optiunile!")

    @staticmethod
    def delete(displayWindow, errPopUp):
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            command = "DELETE FROM ACTE WHERE " \
                      "COD_TIP_ACT = (SELECT COD_TIP_ACT FROM TIPURI_ACTE WHERE DENUMIRE_TIP_ACT = '%s') AND " \
                      "NR_MATRICOL=%s" % (data[2], data[0])
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            displayWindow.removeRow(currentRow)
        else:
            errPopUp.show()
            errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                             "Trebuie sa selectati un row din tabela!")

    def updateData(self, dialogBox, errPopUp, displayWindow):

        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        self.displayWindow = displayWindow
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            self.dialogBox.show()
            query = ' SELECT DISTINCT (SELECT NUME_STUDENT FROM STUDENTI s WHERE s.NR_MATRICOL = o.NR_MATRICOL)' \
                    ' || \' (NR. MATRICOL:\' || NR_MATRICOL || \')\' FROM ACTE o '
            results.execute(query)
            self.dialogBox.nrMatricolBox.clear()
            for i in results:
                self.dialogBox.nrMatricolBox.addItem(i[0])
            index = self.dialogBox.nrMatricolBox.findText(str(data[1]) + ' (NR. MATRICOL:%s)' % data[0])
            self.dialogBox.nrMatricolBox.setCurrentIndex(index)
            query = 'SELECT (SELECT DENUMIRE_TIP_ACT FROM TIPURI_ACTE t WHERE t.COD_TIP_ACT = a.COD_TIP_ACT)' \
                    ' FROM ACTE a WHERE NR_MATRICOL=%s' % int(data[0])
            results.execute(query)
            self.dialogBox.denumireActBox.clear()
            for i in results:
                self.dialogBox.denumireActBox.addItem(i[0])
            index = self.dialogBox.denumireActBox.findText(str(data[2]))
            self.dialogBox.denumireActBox.setCurrentIndex(index)
            self.dialogBox.serieActEdit.setText(data[4])
            d = str(data[3]).split('-')
            self.dialogBox.dateEdit.setDate(QtCore.QDate(int(d[0]), int(d[1]), int(d[2])))
            self.dialogBox.nrMatricolBox.disconnect()
            self.dialogBox.denumireActBox.disconnect()
            self.dialogBox.nrMatricolBox.activated[str].connect(self.onActivated)
            self.dialogBox.denumireActBox.activated[str].connect(self.onActivated2)
            if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
                self.dialogBox.okInsert.clicked.connect(self.verifyAndUpdate)
            '''
            query = 'SELECT NR_ACT FROM ACTE WHERE NR_MATRICOL=%s AND COD_TIP_ACT = ' \
                    '(SELECT COD_TIP_ACT FROM TIPURI_ACTE WHERE DENUMIRE_TIP_ACT = \'%s\')' % (int(data[0]), data[2])
            results.execute(query)
            for i in results:
                self.dialogBox.serieActEdit.setText(i[0])
            '''
        else:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                                  "Trebuie sa selectati un row din tabela!")

    def verifyAndUpdate(self):
        results = connection.cursor()
        data = None
        query = "SELECT NR_MATRICOL,(SELECT DENUMIRE_TIP_ACT FROM TIPURI_ACTE WHERE COD_TIP_ACT=ACTE.COD_TIP_ACT), " \
                "DATA_ACT,NR_ACT FROM ACTE WHERE NR_MATRICOL=%s AND COD_TIP_ACT=" \
                "(SELECT COD_TIP_ACT FROM TIPURI_ACTE WHERE DENUMIRE_TIP_ACT='%s')" \
                % (int(re.sub("[a-zA-Z.(): ]+", '', self.dialogBox.nrMatricolBox.currentText())),
                   self.dialogBox.denumireActBox.currentText())
        results.execute(query)
        self.errPopUp.eroareEdit.setPlainText("")
        for i in results:
            data = i
        self.modifications = False
        command = "UPDATE ACTE SET "
        if self.dialogBox.serieActEdit.text() != str(data[3]):

            serie_act = re.search("^[A-Za-z0-9]{8}$", self.dialogBox.serieActEdit.text())
            if serie_act is None:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\t\tAtentie!\n\n"
                                                         "\tSeria actului este incorecta!\n"
                                                         "\tDimensiunea acestui camp este de 8 caractere.\n"
                                                         "\tSeria actului nu va fi actualizata.")
            else:
                self.modifications = True
                command += "NR_ACT = '%s'," % serie_act.string
        if str(self.dialogBox.dateEdit.date().toPyDate()) != str(data[2].date()):
            date1 = str(self.dialogBox.dateEdit.date().toPyDate()).split('-')
            systemDate = today.strftime("%Y")

            if date1[0] != str(systemDate) or int(date1[1]) != 9 or 11 > int(date1[2]) or int(date1[2]) > 19:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\t\tAtentie!\n\n"
                                                         "\tPerioada depunere acte expirata sau data invalida!\n\t"
                                                         "Data depunerii actelor este in intervalul 11-19 Septembrie.")
            else:
                self.modifications = True
                command += "DATA_ACT = TO_DATE('%s-%s-%s', ' YYYY-MM-DD')," \
                           % (int(date1[0]), int(date1[1]), int(date1[2]))
        if not self.modifications:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Nu s-a modificat niciun camp.")
            self.dialogBox.close()
        else:
            command = command[:-1] + " WHERE NR_MATRICOL=%s AND COD_TIP_ACT=" \
                                     "(SELECT COD_TIP_ACT FROM TIPURI_ACTE WHERE DENUMIRE_TIP_ACT='%s')" \
                      % (int(re.sub("[a-zA-Z.(): ]+", '', self.dialogBox.nrMatricolBox.currentText())),
                         self.dialogBox.denumireActBox.currentText())
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            self.dialogBox.close()
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Modificarea informatiilor s-a efectuat cu succes!")

            self.loadData(self.displayWindow)

    def onActivated(self):
        results = connection.cursor()
        query = 'SELECT (SELECT DENUMIRE_TIP_ACT FROM TIPURI_ACTE t WHERE t.COD_TIP_ACT = a.COD_TIP_ACT)' \
                ' FROM ACTE a WHERE NR_MATRICOL=%s' \
                % int(re.sub('[a-zA-Z.(): ]', '', self.dialogBox.nrMatricolBox.currentText()))
        results.execute(query)
        self.dialogBox.denumireActBox.clear()
        for i in results:
            self.dialogBox.denumireActBox.addItem(i[0])
        query = 'SELECT NR_ACT FROM ACTE WHERE NR_MATRICOL=%s AND COD_TIP_ACT = ' \
                '(SELECT COD_TIP_ACT FROM TIPURI_ACTE WHERE DENUMIRE_TIP_ACT = \'%s\')' % \
                (int(re.sub('[a-zA-Z.(): ]', '', self.dialogBox.nrMatricolBox.currentText())),
                 self.dialogBox.denumireActBox.currentText())
        results.execute(query)
        for i in results:
            self.dialogBox.serieActEdit.setText(i[0])
        query = 'SELECT DATA_ACT FROM ACTE WHERE NR_MATRICOL=%s AND COD_TIP_ACT = ' \
                '(SELECT COD_TIP_ACT FROM TIPURI_ACTE WHERE DENUMIRE_TIP_ACT = \'%s\')' % \
                (int(re.sub('[a-zA-Z.(): ]', '', self.dialogBox.nrMatricolBox.currentText())),
                 self.dialogBox.denumireActBox.currentText())
        results.execute(query)
        d = []
        for i in results:
            d.append(i[0])
        d = str(d[0]).split(' ')
        d = d[:-1]
        d = str(d[0]).split('-')
        self.dialogBox.dateEdit.setDate(QtCore.QDate(int(d[0]), int(d[1]), int(d[2])))

    def onActivated2(self):
        results = connection.cursor()
        query = 'SELECT NR_ACT FROM ACTE WHERE NR_MATRICOL=%s AND COD_TIP_ACT = ' \
                '(SELECT COD_TIP_ACT FROM TIPURI_ACTE WHERE DENUMIRE_TIP_ACT = \'%s\')' % \
                (int(re.sub('[a-zA-Z.(): ]', '', self.dialogBox.nrMatricolBox.currentText())),
                 self.dialogBox.denumireActBox.currentText())
        results.execute(query)
        for i in results:
            self.dialogBox.serieActEdit.setText(i[0])
        query = 'SELECT DATA_ACT FROM ACTE WHERE NR_MATRICOL=%s AND COD_TIP_ACT = ' \
                '(SELECT COD_TIP_ACT FROM TIPURI_ACTE WHERE DENUMIRE_TIP_ACT = \'%s\')' % \
                (int(re.sub('[a-zA-Z.(): ]', '', self.dialogBox.nrMatricolBox.currentText())),
                 self.dialogBox.denumireActBox.currentText())
        results.execute(query)
        d = []
        for i in results:
            d.append(i[0])
        d = str(d[0]).split(' ')
        d = d[:-1]
        d = str(d[0]).split('-')
        self.dialogBox.dateEdit.setDate(QtCore.QDate(int(d[0]), int(d[1]), int(d[2])))

    def __repr__(self):
        return "ACTE"


class Camine:
    @staticmethod
    def loadData(displayWindow):
        query = 'SELECT COD_CAMIN \"Cod camin\",' \
                '(SELECT NUME_ADMINISTRATOR FROM ADMINISTRATORI a WHERE CAMINE.ID_ADMINISTRATOR=a.ID_ADMINISTRATOR)' \
                ' \"Nume administrator\", ADRESA_CAMIN \"Adresa camin\",NR_CAMERE \"Numar total camere\"FROM CAMINE '

        col_cnt = "select count(*) from USER_TAB_COLUMNS where TABLE_NAME='CAMINE'"
        results = connection.cursor()
        results.execute(col_cnt)
        for i in results:
            displayWindow.setColumnCount(i[0])
        results.execute(query)
        displayWindow.setRowCount(0)
        for row_number, row_data in enumerate(results):
            displayWindow.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                displayWindow.setHorizontalHeaderItem(column_number,
                                                      QTableWidgetItem(str(results.description[column_number][0])))
                displayWindow.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    @staticmethod
    def delete(displayWindow, errPopUp):
        errPopUp.show()
        errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                         "Nu se poate efectua operatia de DELETE pentru aceasta tabela!")

    def __repr__(self):
        return "CAMINE"


class Administratori:
    def __init__(self):
        self.dialogBox = None
        self.errPopUp = None
        self.displayWindow = None
        self.modifications = False

    @staticmethod
    def loadData(displayWindow):
        query = ' SELECT NUME_ADMINISTRATOR \"Nume administrator\", EMAIL_ADMINISTRATOR \"Email\",' \
                'TELEFON_ADMINISTRATOR \"Telefon\" FROM administratori '
        col_cnt = "select count(*) from USER_TAB_COLUMNS where TABLE_NAME='ADMINISTRATORI'"
        results = connection.cursor()
        results.execute(col_cnt)
        for i in results:
            displayWindow.setColumnCount(i[0])
        displayWindow.setColumnCount(displayWindow.columnCount() - 1)
        results.execute(query)
        displayWindow.setRowCount(0)
        for row_number, row_data in enumerate(results):
            displayWindow.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                displayWindow.setHorizontalHeaderItem(column_number,
                                                      QTableWidgetItem(str(results.description[column_number][0])))
                displayWindow.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self, dialogBox, errPopUp):
        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
            dialogBox.okInsert.clicked.connect(self.verifyData)

    def verifyData(self):
        results = connection.cursor()
        nume = re.search("^([a-zA-Z]{2,}\s[a-zA-Z]{1,}'?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)", self.dialogBox.numeEdit.text())
        telefon = re.search("^(07)\d{8}$", self.dialogBox.telefonEdit.text())
        email = re.search("[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}", self.dialogBox.emailEdit.text())
        telefon_uk_ck = 1
        if telefon is not None:
            telefon_uk = "SELECT TELEFON_ADMINISTRATOR FROM ADMINISTRATORI" \
                         " WHERE TELEFON_ADMINISTRATOR ='%s'" % telefon.string
            telefon_uk = results.execute(telefon_uk)
            for i in telefon_uk:
                if i:
                    telefon_uk_ck = 0
                    break

        email_uk_ck = 1
        if email is not None:
            email_uk = "SELECT EMAIL_ADMINISTRATOR FROM ADMINISTRATORI WHERE EMAIL_ADMINISTRATOR ='%s'" % email.string
            email_uk = results.execute(email_uk)
            for i in email_uk:
                if i:
                    email_uk_ck = 0
                    break

        if nume is not None and \
                telefon is not None and \
                email is not None and \
                telefon_uk_ck and email_uk_ck:

            command = "INSERT INTO ADMINISTRATORI VALUES (%s,'%s','%s','%s')" % ('NULL',
                                                                                 nume.string,
                                                                                 email.string,
                                                                                 telefon.string)

            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            self.dialogBox.delete_close()
        else:
            if telefon_uk_ck == 0:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                                      "Mai exista un administrator cu acelasi numar de telefon!")
                if email_uk_ck == 0:
                    self.errPopUp.eroareEdit.setPlainText(
                        "\t\tAtentie!\n\n        Mai exista un administrator cu acelasi numar de telefon!"
                        "\n De asemenea exista un administrator si cu aceeasi adresa de email!")
            elif email_uk_ck == 0:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n        "
                                                      "Mai exista un administrator cu aceeasi adresa de email!")
            else:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n\tAti uitat sa completati un camp cu date!"
                                                      "\n     Este posibil de asemenea sa fi completat un camp gresit!")

    @staticmethod
    def delete(displayWindow, errPopUp):
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            command = "DELETE FROM ADMINISTRATORI WHERE TELEFON_ADMINISTRATOR= '%s'" % data[2]
            results.execute(command)
            displayWindow.removeRow(currentRow)
            results.execute('COMMIT WORK')  # tranzactie?
        else:
            errPopUp.show()
            errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                             "Trebuie sa selectati un row din tabela!")

    def updateData(self, dialogBox, errPopUp, displayWindow):

        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        self.displayWindow = displayWindow
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            self.dialogBox.show()
            self.dialogBox.numeEdit.setText(data[0])
            self.dialogBox.emailEdit.setText(data[1])
            self.dialogBox.telefonEdit.setText(data[2])
            # if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
            self.dialogBox.okInsert.disconnect()
            self.dialogBox.okInsert.clicked.connect(lambda: self.verifyAndUpdate(data[2]))
        else:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                                  "Trebuie sa selectati un row din tabela!")

    def verifyAndUpdate(self, telefon1):
        results = connection.cursor()
        data = None
        query = "SELECT NUME_ADMINISTRATOR,EMAIL_ADMINISTRATOR,TELEFON_ADMINISTRATOR" \
                " FROM ADMINISTRATORI WHERE TELEFON_ADMINISTRATOR= '%s'" \
                % telefon1
        results.execute(query)
        self.errPopUp.eroareEdit.setPlainText("")
        for i in results:
            data = i
        self.modifications = False
        command = "UPDATE ADMINISTRATORI SET "
        if self.dialogBox.numeEdit.text() != data[0]:
            nume = re.search("^([a-zA-Z]{2,}\s[a-zA-Z]{1,}'?-?[a-zA-Z]{2,}\s?([a-zA-Z]{1,})?)", self.dialogBox.numeEdit.text())
            if nume is None:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\t\tAtentie!"
                                                         "\n\tNume invalid!\n\tAcest camp nu va fi actualizat.")
            else:
                self.modifications = True
                command += " NUME_ADMINISTRATOR='%s'," % nume.string
        if self.dialogBox.emailEdit.text() != data[1]:

            email = re.search("[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}", self.dialogBox.emailEdit.text())
            if email is None:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\t\tAtentie!"
                                                         "\n\tEmail invalid!\n\tAcest camp nu va fi actualizat.")
            else:
                email_uk_ck = 1

                email_uk = "SELECT EMAIL_ADMINISTRATOR FROM ADMINISTRATORI WHERE EMAIL_ADMINISTRATOR ='%s'" \
                           % email.string
                email_uk = results.execute(email_uk)
                for i in email_uk:
                    if i:
                        email_uk_ck = 0
                        break
                if email_uk_ck:
                    self.modifications = True
                    command += " EMAIL_ADMINISTRATOR='%s'," % email.string
                else:
                    self.errPopUp.show()
                    self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                    self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n"
                                                             "\tEmail-ul introdus nu este unic.")
        if self.dialogBox.telefonEdit.text() != data[2]:
            telefon = re.search("^(07)\d{8}$", self.dialogBox.telefonEdit.text())
            if telefon is None:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\t\tAtentie!"
                                                         "\n\tTelefon invalid!\n\tAcest camp nu va fi actualizat.")
            else:
                telefon_uk_ck = 1
                telefon_uk = "SELECT TELEFON_ADMINISTRATOR FROM ADMINISTRATORI" \
                             " WHERE TELEFON_ADMINISTRATOR ='%s'" % telefon.string
                telefon_uk = results.execute(telefon_uk)
                for i in telefon_uk:
                    if i:
                        telefon_uk_ck = 0
                        break
                if telefon_uk_ck:
                    self.modifications = True
                    command += " TELEFON_ADMINISTRATOR='%s'," % telefon.string
                else:
                    self.errPopUp.show()
                    self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                    self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n"
                                                             "\tNr. de telefon introdus nu este unic.")
        if not self.modifications:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n"
                                                     "\tNu s-a efectuat nici o modificare")
            self.dialogBox.close()
        else:
            command = command[:-1] + " WHERE TELEFON_ADMINISTRATOR = '%s'" \
                      % telefon1
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            self.dialogBox.close()
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Modificarea informatiilor s-a efectuat cu succes!")
            self.loadData(self.displayWindow)

    def onActivated(self):
        pass

    def __repr__(self):
        return "ADMINISTRATORI"


class TipuriActe:
    @staticmethod
    def loadData(displayWindow):
        query = ' SELECT DENUMIRE_TIP_ACT \"Denumire act\" FROM tipuri_acte '
        col_cnt = "select count(*) from USER_TAB_COLUMNS where TABLE_NAME='TIPURI_ACTE'"
        results = connection.cursor()
        results.execute(col_cnt)
        for i in results:
            displayWindow.setColumnCount(i[0])
        displayWindow.setColumnCount(displayWindow.columnCount() - 1)
        results.execute(query)
        displayWindow.setRowCount(0)
        for row_number, row_data in enumerate(results):
            displayWindow.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                displayWindow.setHorizontalHeaderItem(column_number,
                                                      QTableWidgetItem(str(results.description[column_number][0])))
                displayWindow.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    @staticmethod
    def delete(displayWindow, errPopUp):
        errPopUp.show()
        errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                         "Nu se poate efectua operatia de DELETE pentru aceasta tabela!")

    def __repr__(self):
        return "TIPURI_ACTE"


class Camere:
    f = open("A:\Andrei\Facultate\AN3SEM1\BD\Tema\\baie_camere.txt", "r")
    f1 = open("A:\Andrei\Facultate\AN3SEM1\BD\Tema\preturi_camine.txt", "r")
    f2 = open("A:\Andrei\Facultate\AN3SEM1\BD\Tema\\nrLocuriCamera.txt", "r")

    def __init__(self):
        self.dialogBox = None
        self.errPopUp = None
        self.caminSelectat = None
        self.thread = None
        self.modifications = False
        self.displayWindow = None
        self.tipBaie_camere = self.f.read().split("\n")
        self.preturi_camine = self.f1.read().split("\n")
        self.nrLocuriCamera = self.f2.read().split("\n")
        self.f.close()
        self.f1.close()
        self.f2.close()

    @staticmethod
    def loadData(displayWindow):
        query = " SELECT COD_CAMIN \"Cod camin\", NR_CAMERA \"Numar camera\", NR_LOCURI \"Nr. locuri in camera\"," \
                " PRET_CAZARE \"Pret cazare\", BAIE \"Tip baie\" FROM camere " \
                "ORDER BY TO_NUMBER(regexp_replace( COD_CAMIN, '[^[:digit:]]', null ))"
        col_cnt = "select count(*) from USER_TAB_COLUMNS where TABLE_NAME='CAMERE'"
        results = connection.cursor()
        results.execute(col_cnt)
        for i in results:
            displayWindow.setColumnCount(i[0])
        displayWindow.setColumnCount(displayWindow.columnCount() - 1)
        results.execute(query)
        displayWindow.setRowCount(0)
        for row_number, row_data in enumerate(results):
            displayWindow.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                displayWindow.setHorizontalHeaderItem(column_number,
                                                      QTableWidgetItem(str(results.description[column_number][0])))
                displayWindow.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self, dialogBox, errPopUp):
        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        results = connection.cursor()
        query = "select COD_CAMIN from CAMINE ORDER BY TO_NUMBER(regexp_replace( COD_CAMIN, '[^[:digit:]]', null ))"
        results.execute(query)
        self.dialogBox.codCaminBox.clear()
        for i in results:
            self.dialogBox.codCaminBox.addItem(i[0])
        self.caminSelectat = self.dialogBox.codCaminBox.currentText()

        self.dialogBox.tipBaieBox.clear()
        for i in self.tipBaie_camere:
            if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                self.dialogBox.tipBaieBox.addItem(re.sub("[T0-9]+:", '', i))
                break

        query = "select COD_CAMIN,NR_CAMERE from CAMINE" \
                " ORDER BY TO_NUMBER(regexp_replace( COD_CAMIN, '[^[:digit:]]', null ))"
        results.execute(query)
        query2 = "SELECT NR_CAMERA FROM CAMERE c WHERE c.COD_CAMIN = '%s'" % self.dialogBox.codCaminBox.currentText()
        results2 = connection.cursor()
        results2.execute(query2)
        camere_ocupate = [i[0] for i in results2]
        self.dialogBox.nrCameraBox.clear()
        for i in results:
            if i[0] == self.dialogBox.codCaminBox.currentText():
                for j in range(1, i[1] + 1):
                    if j not in camere_ocupate:
                        self.dialogBox.nrCameraBox.addItem(str(j))
                break

        self.dialogBox.pretBox.clear()
        for i in self.preturi_camine:
            if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                self.dialogBox.pretBox.addItem(re.sub("[T0-9]+:", '', i))
                # break

        self.dialogBox.nrLocuriBox.clear()
        self.dialogBox.nrLocuriBox.addItem('1')
        for i in self.nrLocuriCamera:
            if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                self.dialogBox.nrLocuriBox.addItem(re.sub("[T0-9]+:", '', i))
                break

        try:
            self.thread = threading.Thread(target=self.update)
            self.thread.start()
        except RuntimeError:
            print("Eroare la pornirea thread-ului!")

        if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
            dialogBox.okInsert.clicked.connect(self.verifyData)

    def update(self):
        results = connection.cursor()
        query = "select COD_CAMIN,NR_CAMERE from CAMINE" \
                " ORDER BY TO_NUMBER(regexp_replace( COD_CAMIN, '[^[:digit:]]', null ))"
        while True:
            if self.dialogBox.isVisible():
                if self.dialogBox.codCaminBox.currentText() != self.caminSelectat:
                    self.caminSelectat = self.dialogBox.codCaminBox.currentText()
                    self.dialogBox.tipBaieBox.clear()
                    for i in self.tipBaie_camere:
                        if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                            self.dialogBox.tipBaieBox.addItem(re.sub("[T0-9]+:", '', i))
                            break
                    results.execute(query)
                    query2 = "SELECT NR_CAMERA FROM CAMERE c WHERE c.COD_CAMIN = '%s'" \
                             % self.dialogBox.codCaminBox.currentText()
                    results2 = connection.cursor()
                    results2.execute(query2)
                    camere_ocupate = [i[0] for i in results2]
                    self.dialogBox.nrCameraBox.clear()
                    for i in results:
                        if i[0] == self.dialogBox.codCaminBox.currentText():
                            for j in range(1, i[1] + 1):
                                if j not in camere_ocupate:
                                    self.dialogBox.nrCameraBox.addItem(str(j))
                            break
                    self.dialogBox.nrCameraBox.setCurrentIndex(0)

                    self.dialogBox.pretBox.clear()
                    for i in self.preturi_camine:
                        if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                            self.dialogBox.pretBox.addItem(re.sub("[T0-9]+:", '', i))
                            # break
                    self.dialogBox.pretBox.setCurrentIndex(0)
                    self.dialogBox.nrLocuriBox.clear()
                    self.dialogBox.nrLocuriBox.addItem('1')
                    for i in self.nrLocuriCamera:
                        if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                            self.dialogBox.nrLocuriBox.addItem(re.sub("[T0-9]+:", '', i))
                            break
                    self.dialogBox.nrLocuriBox.setCurrentIndex(0)
            else:
                break

    def verifyData(self):
        if self.dialogBox.nrLocuriBox.currentIndex() != -1:
            cod_camin = self.dialogBox.codCaminBox.currentText()
            nr_camera = self.dialogBox.nrCameraBox.currentText()
            nr_locuri = self.dialogBox.nrLocuriBox.currentText()
            tip_baie = self.dialogBox.tipBaieBox.currentText()
            pret = self.dialogBox.pretBox.currentText()
            command = "INSERT INTO CAMERE VALUES (%s,%s,%s,%s,'%s','%s')" \
                      % ('NULL', nr_camera, nr_locuri, pret, tip_baie, cod_camin)
            results = connection.cursor()
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            self.dialogBox.delete_close()
            if self.thread is not None:
                self.thread.join()
                # print(self.thread.is_alive())
        else:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\n\t\tAtentie!\n         "
                                                  "Nu mai sunt camere in camine!")

    @staticmethod
    def delete(displayWindow, errPopUp):
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            command = "DELETE FROM CAMERE WHERE COD_CAMIN = '%s' AND NR_CAMERA = %s" % (str(data[0]), int(data[1]))
            results.execute(command)
            displayWindow.removeRow(currentRow)
            results.execute('COMMIT WORK')  # tranzactie?
        else:
            errPopUp.show()
            errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                             "Trebuie sa selectati un row din tabela!")

    def updateData(self, dialogBox, errPopUp, displayWindow):
        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        self.displayWindow = displayWindow
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            self.dialogBox.show()
            query = "SELECT DISTINCT  COD_CAMIN FROM CAMERE" \
                    " ORDER BY TO_NUMBER(regexp_replace( COD_CAMIN, '[^[:digit:]]', null ))"
            results.execute(query)
            self.dialogBox.codCaminBox.clear()
            for i in results:
                self.dialogBox.codCaminBox.addItem(i[0])
            index = self.dialogBox.codCaminBox.findText(str(data[0]))
            self.dialogBox.codCaminBox.setCurrentIndex(index)
            query = "SELECT NR_CAMERA FROM CAMERE WHERE COD_CAMIN='%s' " \
                    "ORDER BY NR_CAMERA" % self.dialogBox.codCaminBox.currentText()
            results.execute(query)
            self.dialogBox.nrCameraBox.clear()
            for i in results:
                self.dialogBox.nrCameraBox.addItem(str(i[0]))
            self.dialogBox.nrLocuriBox.clear()
            self.dialogBox.nrLocuriBox.addItem('1')
            for i in self.nrLocuriCamera:
                if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                    self.dialogBox.nrLocuriBox.addItem(re.sub("[T0-9]+:", '', i))
                    break
            index = self.dialogBox.nrLocuriBox.findText(str(data[2]))
            self.dialogBox.nrLocuriBox.setCurrentIndex(index)
            self.dialogBox.tipBaieBox.clear()
            for i in self.tipBaie_camere:
                if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                    self.dialogBox.tipBaieBox.addItem(re.sub("[T0-9]+:", '', i))
                    break
            # index = self.dialogBox.tipBaieBox.findText(str(data[4]))
            self.dialogBox.tipBaieBox.setCurrentIndex(0)
            self.dialogBox.pretBox.clear()
            for i in self.preturi_camine:
                if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                    self.dialogBox.pretBox.addItem(re.sub("[T0-9]+:", '', i))
            index = self.dialogBox.pretBox.findText(str(data[3]))
            self.dialogBox.pretBox.setCurrentIndex(index)
            self.dialogBox.codCaminBox.disconnect()
            self.dialogBox.codCaminBox.activated[str].connect(self.onActivated)
            self.dialogBox.nrCameraBox.disconnect()
            self.dialogBox.nrCameraBox.activated[str].connect(self.onActivated2)
            if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
                self.dialogBox.okInsert.clicked.connect(self.verifyAndUpdate)
        else:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                                  "Trebuie sa selectati un row din tabela!")

    def verifyAndUpdate(self):
        results = connection.cursor()
        data = None
        query = "SELECT COD_CAMIN, NR_CAMERA, NR_LOCURI, PRET_CAZARE, BAIE FROM CAMERE" \
                " WHERE COD_CAMIN='%s' AND NR_CAMERA=%s" \
                % (self.dialogBox.codCaminBox.currentText(), self.dialogBox.nrCameraBox.currentText())
        results.execute(query)
        self.errPopUp.eroareEdit.setPlainText("")
        for i in results:
            data = i
        self.modifications = False
        command = "UPDATE CAMERE SET "
        if int(self.dialogBox.nrLocuriBox.currentText()) != int(data[2]):
            self.modifications = True
            command += " NR_LOCURI = %s," % self.dialogBox.nrLocuriBox.currentText()
        if self.dialogBox.tipBaieBox.currentText() != str(data[4]):
            self.modifications = True
            command += " BAIE = '%s'," % self.dialogBox.tipBaieBox.currentText()
        if int(self.dialogBox.pretBox.currentText()) != int(data[3]):
            self.modifications = True
            command += " PRET_CAZARE = %s," % self.dialogBox.pretBox.currentText()
        if not self.modifications:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Nu s-a modificat niciun camp.")
            self.dialogBox.close()
        else:
            command = command[:-1] + " WHERE COD_CAMIN = '%s' AND NR_CAMERA=%s" \
                      % (self.dialogBox.codCaminBox.currentText(), self.dialogBox.nrCameraBox.currentText())
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            self.dialogBox.close()
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Modificarea informatiilor s-a efectuat cu succes!")
            self.loadData(self.displayWindow)

    def onActivated(self):
        results = connection.cursor()
        query = "SELECT NR_CAMERA FROM CAMERE WHERE COD_CAMIN='%s' " \
                "ORDER BY NR_CAMERA" % self.dialogBox.codCaminBox.currentText()
        results.execute(query)
        self.dialogBox.nrCameraBox.clear()
        for i in results:
            self.dialogBox.nrCameraBox.addItem(str(i[0]))
        self.dialogBox.nrLocuriBox.clear()
        self.dialogBox.nrLocuriBox.addItem('1')
        for i in self.nrLocuriCamera:
            if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                self.dialogBox.nrLocuriBox.addItem(re.sub("[T0-9]+:", '', i))
                break
        self.dialogBox.tipBaieBox.clear()
        for i in self.tipBaie_camere:
            if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                self.dialogBox.tipBaieBox.addItem(re.sub("[T0-9]+:", '', i))
                break
        self.dialogBox.pretBox.clear()
        for i in self.preturi_camine:
            if re.search(self.dialogBox.codCaminBox.currentText() + ':', i) is not None:
                self.dialogBox.pretBox.addItem(re.sub("[T0-9]+:", '', i))
        self.onActivated2()

    def onActivated2(self):
        results = connection.cursor()
        if self.dialogBox.nrCameraBox.currentText() != '':
            query = "SELECT NR_LOCURI, BAIE, PRET_CAZARE FROM CAMERE WHERE COD_CAMIN='%s' AND NR_CAMERA= %s " \
                    % (self.dialogBox.codCaminBox.currentText(), self.dialogBox.nrCameraBox.currentText())
            results.execute(query)
            for i in results:
                index = self.dialogBox.nrLocuriBox.findText(str(i[0]))
                self.dialogBox.nrLocuriBox.setCurrentIndex(index)
                index = self.dialogBox.tipBaieBox.findText(str(i[1]))
                self.dialogBox.tipBaieBox.setCurrentIndex(index)
                index = self.dialogBox.pretBox.findText(str(i[2]))
                self.dialogBox.pretBox.setCurrentIndex(index)

    def __repr__(self):
        return "CAMERE"


class Facultati:
    @staticmethod
    def loadData(displayWindow):
        query = 'SELECT COD_FACULTATE "Cod facultate", DENUMIRE "Nume", ADRESA "Adresa" FROM FACULTATI '
        col_cnt = "select count(*) from USER_TAB_COLUMNS where TABLE_NAME='FACULTATI'"
        results = connection.cursor()
        results.execute(col_cnt)
        for i in results:
            displayWindow.setColumnCount(i[0])
        results.execute(query)
        displayWindow.setRowCount(0)
        for row_number, row_data in enumerate(results):
            displayWindow.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                displayWindow.setHorizontalHeaderItem(column_number,
                                                      QTableWidgetItem(str(results.description[column_number][0])))
                displayWindow.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    @staticmethod
    def delete(displayWindow, errPopUp):
        errPopUp.show()
        errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                         "Nu se poate efectua operatia de DELETE pentru aceasta tabela!")

    def __repr__(self):
        return "FACULTATI"


class Optiuni:
    def __init__(self):
        self.dialogBox = None
        self.errPopUp = None
        self.thread = None
        self.displayWindow = None
        self.modifications = False

    @staticmethod
    def loadData(displayWindow):

        query = ' SELECT (SELECT NUME_STUDENT FROM STUDENTI s WHERE s.NR_MATRICOL = o.NR_MATRICOL)' \
                ' || \' (Nr. matricol: \' || NR_MATRICOL || \')\' \"Nume & nr. matricol\", COD_CAMIN \"Cod camin\",' \
                '(SELECT NR_CAMERA  FROM CAMERE C WHERE c.ID_CAMERA=o.ID_CAMERA) \"Numar camera\",' \
                '(SELECT NUME_STUDENT || \' (Nr. matricol: \' || NR_MATRICOL || \')\' ' \
                ' FROM STUDENTI s WHERE s.NR_MATRICOL=o.COLEG1) \"Optiune Coleg 1\", ' \
                '(SELECT NUME_STUDENT || \' (Nr. matricol: \' || NR_MATRICOL || \')\' ' \
                ' FROM STUDENTI s WHERE s.NR_MATRICOL=o.COLEG2) \"Optiune Coleg 2\", ' \
                '(SELECT NUME_STUDENT || \' (Nr. matricol: \' || NR_MATRICOL || \')\' ' \
                ' FROM STUDENTI s WHERE s.NR_MATRICOL=o.COLEG3) \"Optiune Coleg 3\" FROM ' \
                'optiuni o '

        """
        query = ' SELECT NR_MATRICOL \"Numar matricol\", COD_CAMIN \"Cod camin\",' \
                '(SELECT NR_CAMERA  FROM CAMERE C WHERE c.ID_CAMERA=OPTIUNI.ID_CAMERA) \"Numar camera\",' \
                ' COLEG1 \"Optiunie Coleg 1\", COLEG2 \"Optiunie Coleg 2\", COLEG3 \"Optiunie Coleg 3\" FROM optiuni '
        """
        col_cnt = "select count(*) from USER_TAB_COLUMNS where TABLE_NAME='OPTIUNI'"
        results = connection.cursor()
        results.execute(col_cnt)
        for i in results:
            displayWindow.setColumnCount(i[0])
        results.execute(query)
        displayWindow.setRowCount(0)
        for row_number, row_data in enumerate(results):
            displayWindow.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                displayWindow.setHorizontalHeaderItem(column_number,
                                                      QTableWidgetItem(str(results.description[column_number][0])))
                displayWindow.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self, dialogBox, errPopUp):
        results = connection.cursor()
        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        query = "select COD_CAMIN from CAMINE ORDER BY TO_NUMBER(regexp_replace( COD_CAMIN, '[^[:digit:]]', null ))"
        results.execute(query)
        self.dialogBox.codCaminBox.clear()
        for i in results:
            self.dialogBox.codCaminBox.addItem(i[0])
        query = 'SELECT  s.NUME_STUDENT, s.NR_MATRICOL FROM STUDENTI s ' \
                'minus select NUME_STUDENT,o.NR_MATRICOL from OPTIUNI o, STUDENTI'
        results.execute(query)
        self.dialogBox.nrMatricolBox.clear()
        for i in results:
            self.dialogBox.nrMatricolBox.addItem(re.sub(",", ' (Nr. matricol:', re.sub("[()']", '', str(i))) + ')')
        # nr_matricol = re.sub("[A-Za-z:. -()]+",'', dialogBox.nrMatricolBox.currentText())
        # print(nr_matricol)

        query = 'SELECT  s.NUME_STUDENT, s.NR_MATRICOL FROM STUDENTI s '
        results.execute(query)
        self.dialogBox.coleg1Box.clear()
        self.dialogBox.coleg2Box.clear()
        self.dialogBox.coleg3Box.clear()
        self.dialogBox.coleg1Box.addItem('NULL')
        self.dialogBox.coleg2Box.addItem('NULL')
        self.dialogBox.coleg3Box.addItem('NULL')
        for i in results:
            self.dialogBox.coleg1Box.addItem(re.sub(",", ' (Nr. matricol:', re.sub("[()']", '', str(i))) + ')')
            self.dialogBox.coleg2Box.addItem(re.sub(",", ' (Nr. matricol:', re.sub("[()']", '', str(i))) + ')')
            self.dialogBox.coleg3Box.addItem(re.sub(",", ' (Nr. matricol:', re.sub("[()']", '', str(i))) + ')')

        query = "SELECT  c.COD_CAMIN, c.NR_CAMERA FROM CAMERE c where c.COD_CAMIN='%s'" \
                % dialogBox.codCaminBox.currentText()
        results.execute(query)
        self.dialogBox.nrCameraBox.clear()
        for i in results:
            self.dialogBox.nrCameraBox.addItem(re.sub(" ", " Camera:", re.sub("[()']", '', str(i))))

        self.dialogBox.codCaminBox.disconnect()
        self.dialogBox.codCaminBox.activated[str].connect(self.update)

        if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
            self.dialogBox.okInsert.clicked.connect(self.verifyData)

    def update(self):
        results = connection.cursor()
        camere_camin = re.sub(",[a-zA-Z0-9-. :]+", '', self.dialogBox.nrCameraBox.currentText())
        if self.dialogBox.codCaminBox.currentText() != camere_camin:
            query = "SELECT  c.COD_CAMIN, c.NR_CAMERA FROM CAMERE c where c.COD_CAMIN='%s'" \
                    % self.dialogBox.codCaminBox.currentText()
            results.execute(query)
            self.dialogBox.nrCameraBox.clear()
            for i in results:
                self.dialogBox.nrCameraBox.addItem(re.sub(" ", " Camera:", re.sub("[()']", '', str(i))))

    def verifyData(self):
        if self.dialogBox.nrMatricolBox.currentIndex() != -1:
            nr_matricol = self.dialogBox.nrMatricolBox.currentText()
            cod_camin = self.dialogBox.codCaminBox.currentText()
            nr_camera = self.dialogBox.nrCameraBox.currentText()
            coleg1 = self.dialogBox.coleg1Box.currentText()
            coleg2 = self.dialogBox.coleg2Box.currentText()
            coleg3 = self.dialogBox.coleg3Box.currentText()

            if nr_matricol == coleg1 or nr_matricol == coleg2 or nr_matricol == coleg3:
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n          "
                                                      "Trebuie sa alegeti un alt student ca si optiune!")

            elif (coleg1 != 'NULL' and coleg2 != 'NULL' and coleg1 == coleg2) or \
                    (coleg1 != 'NULL' and coleg3 != 'NULL' and coleg1 == coleg3) or \
                    (coleg2 != 'NULL' and coleg3 != 'NULL' and coleg2 == coleg3):
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n"
                                                      "\tTrebuie sa alegeti optiuni diferite!")
                '''
            elif cod_camin != re.sub(",[ a-zA-Z:0-9]+", '', nr_camera):
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n"
                                                      "\tCamera trebuie sa apartina caminului ales!")'''
            else:

                nr_matricol = re.sub("[ )]", '', re.sub("[a-zA-Z -.]+\\([a-zA-Z. ]+:", '', nr_matricol))
                if coleg1 != 'NULL':
                    coleg1 = re.sub("[ )]", '', re.sub("[a-zA-Z -.]+\\([a-zA-Z. ]+:", '', coleg1))
                if coleg2 != 'NULL':
                    coleg2 = re.sub("[ )]", '', re.sub("[a-zA-Z -.]+\\([a-zA-Z. ]+:", '', coleg2))
                if coleg3 != 'NULL':
                    coleg3 = re.sub("[ )]", '', re.sub("[a-zA-Z -.]+\\([a-zA-Z. ]+:", '', coleg3))
                if nr_camera != '':
                    nr_camera = re.sub("[a-zA-Z0-9, ]+:", '', nr_camera)
                    command = "INSERT INTO OPTIUNI VALUES (%s,'%s', \
                    (SELECT c.ID_CAMERA FROM CAMERE c WHERE c.COD_CAMIN = '%s' AND C.NR_CAMERA=%s)" \
                              ",%s,%s,%s)" % (nr_matricol, cod_camin, cod_camin, nr_camera, coleg1, coleg2, coleg3)
                else:
                    command = "INSERT INTO OPTIUNI VALUES (%s,'%s', %s,%s,%s,%s)" \
                              % (nr_matricol, cod_camin, 'NULL', coleg1, coleg2, coleg3)
                results = connection.cursor()
                results.execute(command)
                results.execute('COMMIT WORK')  # tranzactie?
                self.dialogBox.delete_close()
                if self.thread is not None:
                    self.thread.join()
                    # print(self.thread.is_alive())
        else:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\n\t\tAtentie!\n         "
                                                  "Nu mai sunt studenti care nu si-au ales optiunile!")

    def updateData(self, dialogBox, errPopUp, displayWindow):
        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        self.displayWindow = displayWindow
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            self.dialogBox.show()
            query = ' SELECT (SELECT NUME_STUDENT FROM STUDENTI s WHERE s.NR_MATRICOL = o.NR_MATRICOL)' \
                    ' || \' (Nr. matricol: \' || NR_MATRICOL || \')\' FROM optiuni o '
            results.execute(query)
            self.dialogBox.nrMatricolBox.clear()
            for i in results:
                self.dialogBox.nrMatricolBox.addItem(i[0])
            index = self.dialogBox.nrMatricolBox.findText(str(data[0]))
            self.dialogBox.nrMatricolBox.setCurrentIndex(index)
            query = "select COD_CAMIN from CAMINE ORDER BY TO_NUMBER(regexp_replace( COD_CAMIN, '[^[:digit:]]', null ))"
            results.execute(query)
            self.dialogBox.codCaminBox.clear()
            for i in results:
                self.dialogBox.codCaminBox.addItem(i[0])
            index = self.dialogBox.codCaminBox.findText(str(data[1]))
            self.dialogBox.codCaminBox.setCurrentIndex(index)
            self.dialogBox.codCaminBox.disconnect()
            self.dialogBox.codCaminBox.activated[str].connect(self.update)
            query = "SELECT  c.COD_CAMIN, c.NR_CAMERA FROM CAMERE c where c.COD_CAMIN='%s'" \
                    % dialogBox.codCaminBox.currentText()
            results.execute(query)
            self.dialogBox.nrCameraBox.clear()
            for i in results:
                self.dialogBox.nrCameraBox.addItem(re.sub(" ", " Camera:", re.sub("[()']", '', str(i))))
            index = self.dialogBox.nrCameraBox.findText(str(data[1] + ", Camera:" + data[2]))
            self.dialogBox.nrCameraBox.setCurrentIndex(index)
            query = 'SELECT  s.NUME_STUDENT, s.NR_MATRICOL FROM STUDENTI s '
            results.execute(query)
            self.dialogBox.coleg1Box.clear()
            self.dialogBox.coleg2Box.clear()
            self.dialogBox.coleg3Box.clear()
            self.dialogBox.coleg1Box.addItem('NULL')
            self.dialogBox.coleg2Box.addItem('NULL')
            self.dialogBox.coleg3Box.addItem('NULL')
            for i in results:
                self.dialogBox.coleg1Box.addItem(re.sub(",", ' (Nr. matricol:', re.sub("[()']", '', str(i))) + ')')
                self.dialogBox.coleg2Box.addItem(re.sub(",", ' (Nr. matricol:', re.sub("[()']", '', str(i))) + ')')
                self.dialogBox.coleg3Box.addItem(re.sub(",", ' (Nr. matricol:', re.sub("[()']", '', str(i))) + ')')
            if str(data[3]) != 'None':
                index = self.dialogBox.coleg1Box.findText(data[3])
                self.dialogBox.coleg1Box.setCurrentIndex(index)
            else:
                self.dialogBox.coleg1Box.setCurrentIndex(0)
            if str(data[4]) != 'None':
                index = self.dialogBox.coleg2Box.findText(str(data[4]))
                self.dialogBox.coleg2Box.setCurrentIndex(index)
            else:
                self.dialogBox.coleg2Box.setCurrentIndex(0)
            if str(data[5]) != 'None':
                index = self.dialogBox.coleg3Box.findText(str(data[5]))
                self.dialogBox.coleg3Box.setCurrentIndex(index)
            else:
                self.dialogBox.coleg3Box.setCurrentIndex(0)
            self.dialogBox.nrMatricolBox.disconnect()
            self.dialogBox.nrMatricolBox.activated[str].connect(self.onActivated)
            if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
                self.dialogBox.okInsert.clicked.connect(self.verifyAndUpdate)
        else:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                                  "Trebuie sa selectati un row din tabela!")

    def verifyAndUpdate(self):
        results = connection.cursor()
        data = None
        '''
        query = 'SELECT NR_MATRICOL,COD_CAMIN, (SELECT NR_CAMERA FROM CAMERE c WHERE c.ID_CAMERA=o.ID_CAMERA)' \
                ', COLEG1, COLEG2, COLEG3 FROM OPTIUNI o WHERE NR_MATRICOL=%s' \
                % int(re.sub("[a-zA-Z.(): ]+", '', self.dialogBox.nrMatricolBox.currentText()))
        '''
        query = ' SELECT (SELECT NUME_STUDENT FROM STUDENTI s WHERE s.NR_MATRICOL = o.NR_MATRICOL)' \
                ' || \' (Nr. matricol: \' || NR_MATRICOL || \')\' , COD_CAMIN ,' \
                '(SELECT NR_CAMERA  FROM CAMERE C WHERE c.ID_CAMERA=o.ID_CAMERA) ,' \
                '(SELECT NUME_STUDENT || \' (Nr. matricol: \' || NR_MATRICOL || \')\' ' \
                ' FROM STUDENTI s WHERE s.NR_MATRICOL=o.COLEG1) , ' \
                '(SELECT NUME_STUDENT || \' (Nr. matricol: \' || NR_MATRICOL || \')\' ' \
                ' FROM STUDENTI s WHERE s.NR_MATRICOL=o.COLEG2) , ' \
                '(SELECT NUME_STUDENT || \' (Nr. matricol: \' || NR_MATRICOL || \')\' ' \
                ' FROM STUDENTI s WHERE s.NR_MATRICOL=o.COLEG3)  FROM ' \
                'optiuni o WHERE NR_MATRICOL=%s' \
                % int(re.sub("[a-zA-Z.(): ]+", '', self.dialogBox.nrMatricolBox.currentText()))
        results.execute(query)
        self.errPopUp.eroareEdit.setPlainText("")
        for i in results:
            data = i
        self.modifications = False
        command = "UPDATE OPTIUNI SET "
        if self.dialogBox.codCaminBox.currentText() != str(data[1]):
            self.modifications = True
            command += " COD_CAMIN = '%s'," % self.dialogBox.codCaminBox.currentText()
        nr_camera = re.sub("[a-zA-Z0-9, ]+:", '', self.dialogBox.nrCameraBox.currentText())
        if nr_camera != str(data[2]):
            self.modifications = True
            if nr_camera != '':
                command += " ID_CAMERA = (SELECT ID_CAMERA FROM CAMERE WHERE COD_CAMIN='%s' AND NR_CAMERA=%s)," \
                           % (self.dialogBox.codCaminBox.currentText(), nr_camera)
            else:
                command += " ID_CAMERA = NULL,"
        nr_mat = self.dialogBox.nrMatricolBox.currentText()
        coleg1 = self.dialogBox.coleg1Box.currentText()
        coleg2 = self.dialogBox.coleg2Box.currentText()
        coleg3 = self.dialogBox.coleg3Box.currentText()
        if (coleg1 != 'NULL' and coleg2 != 'NULL' and coleg1 == coleg2) or \
                (coleg1 != 'NULL' and coleg3 != 'NULL' and coleg1 == coleg3) or \
                (coleg2 != 'NULL' and coleg3 != 'NULL' and coleg2 == coleg3) or \
                nr_mat == coleg1 or nr_mat == coleg2 or nr_mat == coleg3:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\t\tAtentie!\n\n"
                                                     "\tTrebuie sa alegeti optiuni diferite!")
        else:
            if coleg1 != str((lambda x: 'NULL' if str(x) == 'None' else str(x))(data[3])):
                self.modifications = True
                if coleg1 != 'NULL':
                    command += " COLEG1 = %s," % int(re.sub("[a-zA-Z.(): ]+", '', coleg1))
                else:
                    command += " COLEG1 = %s," % 'NULL'
            if coleg2 != str((lambda x: 'NULL' if str(x) == 'None' else str(x))(data[4])):
                self.modifications = True
                if coleg2 != 'NULL':
                    command += " COLEG2 = %s," % int(re.sub("[a-zA-Z.(): ]+", '', coleg2))
                else:
                    command += " COLEG2 = %s," % 'NULL'
            if coleg3 != str((lambda x: 'NULL' if str(x) == 'None' else str(x))(data[5])):
                self.modifications = True
                if coleg3 != 'NULL':
                    command += " COLEG3 = %s," % int(re.sub("[a-zA-Z.(): ]+", '', coleg3))
                else:
                    command += " COLEG3 = %s," % 'NULL'
        if not self.modifications:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Nu s-a modificat niciun camp.")
            self.dialogBox.close()
        else:
            command = command[:-1] + " WHERE NR_MATRICOL = %s" \
                      % int(re.sub("[a-zA-Z.(): ]+", '', self.dialogBox.nrMatricolBox.currentText()))
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            self.dialogBox.close()
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Modificarea informatiilor s-a efectuat cu succes!")
            self.loadData(self.displayWindow)

    def onActivated(self):
        results = connection.cursor()
        query = ' SELECT (SELECT NUME_STUDENT FROM STUDENTI s WHERE s.NR_MATRICOL = o.NR_MATRICOL)' \
                ' || \' (Nr. matricol: \' || NR_MATRICOL || \')\' \"Nume & nr. matricol\", COD_CAMIN \"Cod camin\",' \
                '(SELECT NR_CAMERA  FROM CAMERE C WHERE c.ID_CAMERA=o.ID_CAMERA) \"Numar camera\",' \
                '(SELECT NUME_STUDENT || \' (Nr. matricol: \' || NR_MATRICOL || \')\' ' \
                ' FROM STUDENTI s WHERE s.NR_MATRICOL=o.COLEG1) \"Optiune Coleg 1\", ' \
                '(SELECT NUME_STUDENT || \' (Nr. matricol: \' || NR_MATRICOL || \')\' ' \
                ' FROM STUDENTI s WHERE s.NR_MATRICOL=o.COLEG2) \"Optiune Coleg 2\", ' \
                '(SELECT NUME_STUDENT || \' (Nr. matricol: \' || NR_MATRICOL || \')\' ' \
                ' FROM STUDENTI s WHERE s.NR_MATRICOL=o.COLEG3) \"Optiune Coleg 3\" FROM ' \
                'optiuni o WHERE NR_MATRICOL=%s' \
                % (int(re.sub("[a-zA-Z.(): ]+", '', self.dialogBox.nrMatricolBox.currentText())))
        results.execute(query)
        for i in results:
            index = self.dialogBox.codCaminBox.findText(str(i[1]))
            self.dialogBox.codCaminBox.setCurrentIndex(index)
            self.dialogBox.nrCameraBox.clear()
            self.dialogBox.nrCameraBox.addItem(self.dialogBox.codCaminBox.currentText() + ", Camera:" + str(i[2]))
            if str(i[3]) != 'None':
                index = self.dialogBox.coleg1Box.findText(i[3])
                self.dialogBox.coleg1Box.setCurrentIndex(index)
            else:
                self.dialogBox.coleg1Box.setCurrentIndex(0)
            if str(i[4]) != 'None':
                index = self.dialogBox.coleg2Box.findText(str(i[4]))
                self.dialogBox.coleg2Box.setCurrentIndex(index)
            else:
                self.dialogBox.coleg2Box.setCurrentIndex(0)
            if str(i[5]) != 'None':
                index = self.dialogBox.coleg3Box.findText(str(i[5]))
                self.dialogBox.coleg3Box.setCurrentIndex(index)
            else:
                self.dialogBox.coleg3Box.setCurrentIndex(0)

    @staticmethod
    def delete(displayWindow, errPopUp):
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            command = "DELETE FROM OPTIUNI WHERE NR_MATRICOL= %s" % re.sub("[a-zA-Z.(): ]+", '', data[0])
            # print(re.sub("[a-zA-Z.(): ]", '', data[0]))
            results.execute(command)
            displayWindow.removeRow(currentRow)
            results.execute('COMMIT WORK')  # tranzactie?
        else:
            errPopUp.show()
            errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                             "Trebuie sa selectati un row din tabela!")

    def __repr__(self):
        return "OPTIUNI"


class Punctaje:
    def __init__(self):
        self.dialogBox = None
        self.errPopUp = None
        self.displayWindow = None
        self.thread = None
        self.modifications = False

    @staticmethod
    def loadData(displayWindow):
        query = ' SELECT (SELECT NUME_STUDENT FROM STUDENTI s WHERE s.NR_MATRICOL = p.NR_MATRICOL)' \
                '|| \' (NR. MATRICOL:\' ||NR_MATRICOL|| \')\' \"Nume & nr. matricol\",' \
                'PUNCTAJ_TOTAL \"Punctaj total\", BONUS,' \
                ' MEDIE_STUDENT \"Medie\", NUMAR_CREDITE \"Numar credite\", AN_STUDIU \"An studiu\" FROM punctaje p'
        col_cnt = "select count(*) from USER_TAB_COLUMNS where TABLE_NAME ='PUNCTAJE'"
        results = connection.cursor()
        results.execute(col_cnt)
        for i in results:
            displayWindow.setColumnCount(i[0])
        results.execute(query)
        displayWindow.setRowCount(0)

        for row_number, row_data in enumerate(results):
            displayWindow.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                displayWindow.setHorizontalHeaderItem(column_number,
                                                      QTableWidgetItem(str(results.description[column_number][0])))
                displayWindow.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def insertData(self, dialogBox, errPopUp):
        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        results = connection.cursor()
        query = 'SELECT  s.NUME_STUDENT, s.NR_MATRICOL FROM STUDENTI s ' \
                'minus select NUME_STUDENT,p.NR_MATRICOL from PUNCTAJE p, STUDENTI'
        results.execute(query)
        self.dialogBox.nrMatricolBox.clear()
        for i in results:
            self.dialogBox.nrMatricolBox.addItem(re.sub(",", ' (Nr. matricol:', re.sub("[()']", '', str(i))) + ')')
        self.dialogBox.anStudiuBox.clear()
        for i in range(1, 5):
            self.dialogBox.anStudiuBox.addItem(str(i))
        if int(self.dialogBox.anStudiuBox.currentText()) == 1:
            self.dialogBox.nrCrediteEdit.clear()
            self.dialogBox.nrCrediteEdit.setEnabled(False)
            self.dialogBox.bonusEdit.clear()
            self.dialogBox.bonusEdit.setEnabled(False)
        try:
            self.thread = threading.Thread(target=self.update)
            self.thread.start()
        except RuntimeError:
            print("Eroare la pornirea thread-ului!")
        if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
            dialogBox.okInsert.clicked.connect(self.verifyData)

    def update(self):
        while True:
            if self.dialogBox.isVisible():
                if int(self.dialogBox.anStudiuBox.currentText()) != 1:
                    self.dialogBox.nrCrediteEdit.setEnabled(True)
                    self.dialogBox.bonusEdit.setEnabled(True)
                else:
                    self.dialogBox.nrCrediteEdit.clear()
                    self.dialogBox.nrCrediteEdit.setEnabled(False)
                    self.dialogBox.bonusEdit.clear()
                    self.dialogBox.bonusEdit.setEnabled(False)
            else:
                break

    def verifyData(self):
        if self.dialogBox.nrMatricolBox.currentIndex() != -1:
            nr_matricol = re.sub("[a-zA-Z.:() ]+", '', self.dialogBox.nrMatricolBox.currentText())
            medie_student = re.search('^[0-9]+\\.[0-9]+$', self.dialogBox.medieStudentEdit.text())
            an_studiu = self.dialogBox.anStudiuBox.currentText()

            if self.dialogBox.bonusEdit.isEnabled():
                bonus = re.search('^[0-9]+\\.[0-9]$', self.dialogBox.bonusEdit.text())
            else:
                bonus = None
            if self.dialogBox.nrCrediteEdit.isEnabled():
                nr_credite = re.search('^[0-9]+$', self.dialogBox.nrCrediteEdit.text())
            else:
                nr_credite = None
            if (bonus is None and int(an_studiu) != 1) or (bonus is not None and float(bonus.string) > 10):
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n"
                                                      "\tCampul bonus este introdus gresit sau este gol!\n"
                                                      "\tFormat:NUMBER(3,1)\n"
                                                      "\tBonusul este cuprins intre 0-10.")
            elif medie_student is None or (medie_student is not None and float(medie_student.string) > 10):
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n "
                                                      "\tCampul medie student este introdus gresit sau este gol!\n"
                                                      "\tFormat:NUMBER(4,2)\n"
                                                      "\tMedia studentului este cuprinsa intre 0-10.")
            elif (nr_credite is None and int(an_studiu) != 1) or (nr_credite is not None
                                                                  and int(nr_credite.string) > (
                                                                          60 * (int(an_studiu) - 1))):
                self.errPopUp.show()
                self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n"
                                                      "\tCampul numar credite este introdus gresit sau este gol!\n"
                                                      "\tFormat:NUMBER(3)\n"
                                                      "\tNumarul de credite este cuprins intre 0-180, in functie"
                                                      " de anul de studiu.")
            else:
                if int(an_studiu) != 1:
                    command = "INSERT INTO PUNCTAJE VALUES (%s,%s,%s,%s,%s,%s)" % (int(nr_matricol), 'NULL',
                                                                                   float(bonus.string),
                                                                                   float(medie_student.string),
                                                                                   int(nr_credite.string),
                                                                                   int(an_studiu))
                else:
                    command = "INSERT INTO PUNCTAJE VALUES (%s,%s,%s,%s,%s,%s)" % (int(nr_matricol), 'NULL',
                                                                                   0.0,
                                                                                   float(medie_student.string),
                                                                                   0, int(an_studiu))
                results = connection.cursor()
                results.execute(command)
                results.execute('COMMIT WORK')  # tranzactie?
                self.dialogBox.delete_close()
                if self.thread is not None:
                    self.thread.join()
        else:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\n\t\tAtentie!\n         "
                                                  "Nu mai sunt studenti fara punctaje!")

    @staticmethod
    def delete(displayWindow, errPopUp):
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            command = "DELETE FROM PUNCTAJE WHERE NR_MATRICOL= %s" % re.sub("[a-zA-Z.(): ]+", '', data[0])
            results.execute(command)
            displayWindow.removeRow(currentRow)
            results.execute('COMMIT WORK')  # tranzactie?
        else:
            errPopUp.show()
            errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                             "Trebuie sa selectati un row din tabela!")

    def updateData(self, dialogBox, errPopUp, displayWindow):
        self.dialogBox = dialogBox
        self.errPopUp = errPopUp
        self.displayWindow = displayWindow
        results = connection.cursor()
        currentRow = displayWindow.currentRow()
        data = []
        for i in displayWindow.selectedItems():
            data.append(i.text())
        if currentRow != -1:
            self.dialogBox.show()
            query = 'SELECT (SELECT NUME_STUDENT FROM STUDENTI s where s.NR_MATRICOL = p.NR_MATRICOL) ' \
                    ' || \' (NR. MATRICOL:\' || NR_MATRICOL || \')\' \"Nume & nr. matricol\" FROM PUNCTAJE p'
            results.execute(query)
            self.dialogBox.nrMatricolBox.clear()
            for i in results:
                self.dialogBox.nrMatricolBox.addItem(i[0])
            index = self.dialogBox.nrMatricolBox.findText(str(data[0]))
            self.dialogBox.nrMatricolBox.setCurrentIndex(index)
            self.dialogBox.anStudiuBox.clear()
            for i in range(1, 5):
                self.dialogBox.anStudiuBox.addItem(str(i))
            index = self.dialogBox.anStudiuBox.findText(str(data[5]))
            self.dialogBox.anStudiuBox.setCurrentIndex(index)
            '''
            if int(self.dialogBox.anStudiuBox.currentText()) == 1:
                self.dialogBox.nrCrediteEdit.clear()
                self.dialogBox.nrCrediteEdit.setEnabled(False)
                self.dialogBox.bonusEdit.clear()
                self.dialogBox.bonusEdit.setEnabled(False)
            else:
            '''
            self.dialogBox.bonusEdit.setText(data[2])
            self.dialogBox.nrCrediteEdit.setText(data[4])
            self.dialogBox.medieStudentEdit.setText(data[3])

            self.dialogBox.nrMatricolBox.disconnect()
            self.dialogBox.nrMatricolBox.activated[str].connect(self.onActivated)

            if not self.dialogBox.isSignalConnected1(self.dialogBox.okInsert, 'clicked()'):
                self.dialogBox.okInsert.clicked.connect(self.verifyAndUpdate)
            if not self.dialogBox.isSignalConnected1(self.dialogBox.calculatePunctaj, 'clicked()'):
                self.dialogBox.calculatePunctaj.clicked.connect(self.calculatePunctaj)
        else:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                                  "Trebuie sa selectati un row din tabela!")

    def onActivated(self):
        query = ' SELECT * FROM punctaje p' \
                ' WHERE p.NR_MATRICOL = %s' \
                % int(re.sub("[a-zA-Z.(): ]", '', self.dialogBox.nrMatricolBox.currentText()))
        results = connection.cursor()
        results.execute(query)
        for i in results:
            self.dialogBox.bonusEdit.setText(str(i[2]))
            self.dialogBox.medieStudentEdit.setText(str(i[3]))
            self.dialogBox.nrCrediteEdit.setText(str(i[4]))
            index = self.dialogBox.anStudiuBox.findText(str(i[5]))
            self.dialogBox.anStudiuBox.setCurrentIndex(index)

    def verifyAndUpdate(self):
        results = connection.cursor()
        data = None
        query = 'SELECT * FROM PUNCTAJE WHERE NR_MATRICOL=%s' \
                % int(re.sub("[a-zA-Z.(): ]+", '', self.dialogBox.nrMatricolBox.currentText()))
        results.execute(query)
        self.errPopUp.eroareEdit.setPlainText("")
        for i in results:
            data = i
        self.modifications = False
        command = "UPDATE PUNCTAJE SET "
        if self.dialogBox.anStudiuBox.currentText() != str(data[5]):
            self.modifications = True
            an_studiu = self.dialogBox.anStudiuBox.currentText()
            command += "AN_STUDIU = %s," % int(an_studiu)
        if self.dialogBox.anStudiuBox.currentText() != 1:
            if self.dialogBox.bonusEdit.text() != str(data[2]):
                bonus = re.search('^[0-9]+\\.[0-9]$', self.dialogBox.bonusEdit.text())
                if (bonus is None and int(self.dialogBox.anStudiuBox.currentText()) != 1) \
                        or (bonus is not None and float(bonus.string) > 10):
                    self.errPopUp.show()
                    self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                    self.errPopUp.eroareEdit.insertPlainText("\t\tAtentie!\n\n"
                                                             "\tCampul bonus este introdus gresit sau este gol!\n"
                                                             "\tFormat:NUMBER(3,1)\n"
                                                             "\tBonusul este cuprins intre 0-10.\n"
                                                             "\tCampul bonus nu va fi actualizat.")
                elif bonus is not None:
                    self.modifications = True
                    command += "BONUS = %s," % float(bonus.string)
            if self.dialogBox.nrCrediteEdit.text() != str(data[4]):
                nr_credite = re.search('^[0-9]+$', self.dialogBox.nrCrediteEdit.text())
                if (nr_credite is None and int(self.dialogBox.anStudiuBox.currentText()) != 1) or (
                        nr_credite is not None
                        and int(nr_credite.string) > (
                                60 * (int(self.dialogBox.anStudiuBox.currentText()) - 1))):
                    self.errPopUp.show()
                    self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                    self.errPopUp.eroareEdit.insertPlainText("\t\tAtentie!\n\n"
                                                             "\tCampul numar credite este introdus gresit sau este "
                                                             "gol!\n "
                                                             "\tFormat:NUMBER(3)\n"
                                                             "\tNumarul de credite este cuprins intre 0-180, in functie"
                                                             " de anul de studiu.\n"
                                                             "\tCampul nr_credite nu va fi actualizat.")
                elif nr_credite is not None:
                    self.modifications = True
                    command += "NUMAR_CREDITE = %s," % float(nr_credite.string)
        if self.dialogBox.medieStudentEdit.text() != str(data[3]):
            medie_student = re.search('^[0-9]+\\.[0-9]+$', self.dialogBox.medieStudentEdit.text())
            if medie_student is None or (medie_student is not None and float(medie_student.string) > 10):
                self.errPopUp.show()
                self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
                self.errPopUp.eroareEdit.insertPlainText("\t\tAtentie!\n\n "
                                                         "\tCampul medie student este introdus gresit sau este gol!\n"
                                                         "\tFormat:NUMBER(4,2)\n"
                                                         "\tMedia studentului este cuprinsa intre 0-10.")
            elif medie_student is not None:
                self.modifications = True
                command += "MEDIE_STUDENT = %s," % float(medie_student.string)
        if not self.modifications:
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Nu s-a modificat niciun camp referitor"
                                                     " la informatiile necesare calcularii punctajelor.")
            # self.dialogBox.close()
        else:
            command = command[:-1] + " WHERE NR_MATRICOL = %s" \
                      % int(re.sub("[a-zA-Z.(): ]+", '', self.dialogBox.nrMatricolBox.currentText()))
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            # self.dialogBox.close()
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Modificarea informatiilor s-a efectuat cu succes!")
            self.onActivated()
            self.loadData(self.displayWindow)

    def calculatePunctaj(self):
        results = connection.cursor()
        if self.dialogBox.checkBox.isChecked():
            command = 'UPDATE punctaje ' \
                      'SET punctaj_total = CASE' \
                      ' WHEN an_studiu=1 THEN (medie_student * 10) ' \
                      'ELSE ' \
                      '(medie_student * (numar_credite*10/(60.0*(an_studiu-1)))+  (bonus)) ' \
                      'END'
            self.verifyAndUpdate()
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie?
            self.loadData(self.displayWindow)
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Modificarea punctajelor s-a realizat cu succes pentru toti "
                                                     "studentii!")
        else:
            command = 'UPDATE punctaje ' \
                      'SET punctaj_total = CASE' \
                      ' WHEN an_studiu=1 THEN (medie_student * 10) ' \
                      'ELSE ' \
                      '(medie_student * (numar_credite*10/(60.0*(an_studiu-1)))+  (bonus)) ' \
                      'END where NR_MATRICOL=%s' \
                      % int(re.sub("[a-zA-Z.(): ]+", '', self.dialogBox.nrMatricolBox.currentText()))
            self.verifyAndUpdate()
            results.execute(command)
            results.execute('COMMIT WORK')  # tranzactie
            self.loadData(self.displayWindow)
            self.errPopUp.show()
            self.errPopUp.eroareEdit.moveCursor(QTextCursor.End)
            self.errPopUp.eroareEdit.insertPlainText("\n\t\tAtentie!\n         "
                                                     "Update-ul punctajului curent s-a realizat cu succes!")

    def __repr__(self):
        return "PUNCTAJE"


class Studenti_Optiuni:
    @staticmethod
    def loadData(displayWindow):
        query = "SELECT nume_student \"Nume student\", o.cod_camin \"Cod camin\", nr_camera \"Numar camera\"," \
                "(SELECT nume_student FROM studenti m where m.nr_matricol=o.coleg1) \"Nume optiune coleg 1\", " \
                "(SELECT nume_student FROM studenti m WHERE m.nr_matricol=o.coleg2) \"Nume optiune coleg 2\"," \
                "(SELECT nume_student FROM studenti m WHERE m.nr_matricol=o.coleg3) \"Nume optiune coleg 3\" FROM " \
                "studenti s, optiuni o,camere c " \
                "WHERE s.nr_matricol = o.nr_matricol AND c.id_camera = o.id_camera "

        results = connection.cursor()
        results.execute(query)
        displayWindow.setColumnCount(10)
        displayWindow.setRowCount(0)
        columns = 1
        for row_number, row_data in enumerate(results):
            displayWindow.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if row_number == 0:
                    displayWindow.setColumnCount(columns)
                    columns += 1
                displayWindow.setHorizontalHeaderItem(column_number,
                                                      QTableWidgetItem(str(results.description[column_number][0])))
                displayWindow.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    @staticmethod
    def delete(displayWindow, errPopUp):
        errPopUp.show()
        errPopUp.eroareEdit.setPlainText("\t\tAtentie!\n\n         "
                                         "Nu se poate efectua operatia de DELETE pentru aceasta tabela!")

    def __repr__(self):
        return "STUDENTI_OPTIUNI"
