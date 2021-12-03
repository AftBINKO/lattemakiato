import sys

from PyQt5.QtWidgets import QDialog, QPushButton, QTableWidget, QLabel, QApplication, QComboBox, \
    QLineEdit, QDialogButtonBox


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(240, 320)
        self.label_7 = QLabel(self)
        self.label_7.setText('id =')
        self.label_7.move(150, 20)
        self.comboBox_3 = QComboBox(self)
        self.comboBox_3.setGeometry(180, 20, 50, 20)
        self.label = QLabel(self)
        self.label.move(10, 50)
        self.label_2 = QLabel(self)
        self.label_2.move(10, 80)
        self.label_3 = QLabel(self)
        self.label_3.move(10, 110)
        self.label_4 = QLabel(self)
        self.label_4.move(10, 140)
        self.label_5 = QLabel(self)
        self.label_5.move(10, 170)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(100, 50)
        self.lineEdit_3 = QLineEdit(self)
        self.lineEdit_3.move(100, 140)
        self.lineEdit_2 = QLineEdit(self)
        self.lineEdit_2.move(100, 170)
        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(100, 80, 130, 20)
        self.comboBox_2 = QComboBox(self)
        self.comboBox_2.setGeometry(100, 110, 130, 20)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.move(10, 270)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
