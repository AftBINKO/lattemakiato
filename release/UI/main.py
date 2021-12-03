from PyQt5.QtWidgets import QMainWindow, QPushButton, QTableWidget


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(640, 480)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(10, 10, 620, 380)
        self.pushButton = QPushButton(self)
        self.pushButton.setText('Добавить')
        self.pushButton.move(520, 400)
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setText('Изменить')
        self.pushButton_2.move(420, 400)
        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setText('Обновить')
        self.pushButton_3.move(320, 400)
