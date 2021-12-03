import sqlite3
import sys

from UI.main import Example
from UI.addEditCoffeeForm import Window
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog


class MyWidget(Example):
    def __init__(self):
        super().__init__()
        self.dialog, self.degreesOfRoasting, self.types, self.headers = None, None, None, None
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)
        self.pushButton_3.clicked.connect(self.update_result)
        self.update_result()

    def update_result(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.headers = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.degreesOfRoasting = cur.execute("SELECT * FROM degreesOfRoasting").fetchall()
        self.types = cur.execute("SELECT * FROM types").fetchall()
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                if j == 2:
                    val = cur.execute(f"""SELECT * FROM degreesOfRoasting
WHERE id = (
SELECT degreeOfRoasting FROM coffee
WHERE id = {elem[0]})""").fetchall()[0][1]
                elif j == 3:
                    val = cur.execute(f"""SELECT * FROM types
WHERE id = (
SELECT type FROM coffee
WHERE id = {elem[0]})""").fetchall()[0][1]
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        con.close()

    def add(self):
        self.dialog = Window(self.headers, self.degreesOfRoasting, self.types, True)
        self.dialog.show()

    def edit(self):
        self.dialog = Window(self.headers, self.degreesOfRoasting, self.types, False)
        self.dialog.show()


class Window(Window):
    def __init__(self, headers, degreesOfRoasting, types, new):
        super().__init__()
        self.headers, self.degreesOfRoasting, self.types = headers, degreesOfRoasting, types
        self.new = new
        self.initUi()

    def initUi(self):
        self.label.setText(self.headers[1])
        self.label_2.setText(self.headers[2])
        self.label_3.setText(self.headers[3])
        self.label_4.setText(self.headers[4])
        self.label_5.setText(self.headers[5])
        self.buttonBox.accepted.connect(self.add)
        if self.new:
            self.label_7.hide()
            self.comboBox_3.hide()
            for i in self.degreesOfRoasting:
                self.comboBox.addItem(i[1])
            for i in self.types:
                self.comboBox_2.addItem(i[1])
        else:
            con = sqlite3.connect("data/coffee.sqlite")
            cur = con.cursor()
            for i in cur.execute('SELECT id FROM coffee').fetchall():
                self.comboBox_3.addItem(str(i[0]))
            self.comboBox_3.currentTextChanged.connect(self.fill)
            self.fill()
            con.close()

    def fill(self):
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        self.comboBox.clear()
        self.comboBox_2.clear()
        result = cur.execute(f"""SELECT * FROM coffee
WHERE id = {self.comboBox_3.currentText()}""").fetchall()[0]
        self.lineEdit.setText(result[1])
        current = cur.execute(f"""SELECT degreeOfRoasting FROM degreesOfRoasting
WHERE id = {result[2]}""").fetchall()[0][0]
        elem = [current]
        self.comboBox.addItem(current)
        for i in cur.execute("""SELECT degreeOfRoasting FROM degreesOfRoasting""").fetchall():
            if i[0] not in elem:
                self.comboBox.addItem(i[0])
                elem.append(i[0])
        current = cur.execute(f"""SELECT type FROM types
WHERE id = {result[3]}""").fetchall()[0][0]
        elem = [current]
        self.comboBox_2.addItem(current)
        for i in cur.execute("""SELECT type FROM types""").fetchall():
            if i[0] not in elem:
                self.comboBox_2.addItem(i[0])
                elem.append(i[0])
        self.lineEdit_3.setText(result[4])
        self.lineEdit_2.setText(str(result[5]))

    def add(self):
        a, b = self.lineEdit.text() == '', self.lineEdit_2.text() == ''
        c = self.lineEdit_3.text() == ''
        flag = True
        if a or b or c:
            QMessageBox.critical(self, 'Ошибка', 'Вы должны были заполнить все поля')
            self.show()
            flag = False
        else:
            try:
                int(self.lineEdit_2.text())
            except ValueError:
                QMessageBox.critical(self, 'Ошибка',
                                     f'Поле {self.headers[5]} содержит некорректные значения')
                self.show()
                flag = False
        if flag:
            con = sqlite3.connect("data/coffee.sqlite")
            cur = con.cursor()
            d = cur.execute(f'''SELECT id FROM degreesOfRoasting
WHERE degreeOfRoasting = "{self.comboBox.currentText()}"''').fetchall()[0][0]
            t = cur.execute(f'''SELECT id FROM types
WHERE type = "{self.comboBox_2.currentText()}"''').fetchall()[0][0]
            if self.new:
                cur.execute(f"""INSERT INTO coffee(name,degreeOfRoasting,type,description,volume)
VALUES('{self.lineEdit.text()}',{d},{t},'{self.lineEdit_3.text()}',{self.lineEdit_2.text()})""")
            else:
                cur.execute(f"""UPDATE coffee
SET name = '{self.lineEdit.text()}'
WHERE id = {self.comboBox_3.currentText()}""")
                cur.execute(f"""UPDATE coffee
SET degreeOfRoasting = {d}
WHERE id = {self.comboBox_3.currentText()}""")
                cur.execute(f"""UPDATE coffee
SET type = {t}
WHERE id = {self.comboBox_3.currentText()}""")
                cur.execute(f"""UPDATE coffee
SET description = '{self.lineEdit_3.text()}'
WHERE id = {self.comboBox_3.currentText()}""")
                cur.execute(f"""UPDATE coffee
SET volume = {self.lineEdit_2.text()}
WHERE id = {self.comboBox_3.currentText()}""")
            con.commit()
            con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
