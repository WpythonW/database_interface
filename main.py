import sys
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QHeaderView
from mysqlConn import Sql


class MainWindow(QDialog):
    def __init__(self):
        self.sql = Sql()
        self.list_of_tables = [i[0] for i in self.sql.get_all_tables()]
        super(MainWindow, self).__init__()
        self.ui = loadUi("interface.ui", self)
        self.ui.get_tabl.clicked.connect(self.output_T)
        self.ui.change_table.clicked.connect(self.change_T)
        self.ui.delete_row.clicked.connect(self.del_row_from_T)
        self.ui.add_row.clicked.connect(self.add_row_T)
        self.ui.tables_list.currentTextChanged.connect(self.get_Col)
        self.ui.tables_list.addItems(self.list_of_tables)

    def add_row_T(self):
        row = ""
        t_name = self.ui.tables_list.currentText()
        row += self.ui.input_row_data.text()
        try:
            self.sql.add_row(t_name, row)  # ('Кирдяшкин В.В', 'Радиоэлектроника, инфокоммуникации и информационная безопасность', '4')
        except:
            self.tableWidget.setRowCount(1)
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Ошибка! Введите значения"))
            self.tableWidget.setColumnWidth(0, 300)
            return 0

    def del_row_from_T(self):
        t_name = self.ui.tables_list.currentText()
        cr_field = self.ui.column_list.currentText()
        cr_value = self.ui.column_value.text()
        self.sql.delete_row(t_name, cr_field, cr_value)

    def get_Col(self):
        rows = [i[0] for i in self.sql.get_columns(self.ui.tables_list.currentText())]
        self.ui.column_list.clear()
        self.ui.column_list.addItems(rows)
        self.ui.new_v_col_list.clear()
        self.ui.new_v_col_list.addItems(rows)
        self.ui.input_row_data.setPlaceholderText('(' + ', '.join(rows) + ')')

    def change_T(self):
        t_name = self.ui.tables_list.currentText()
        cr_field = self.ui.column_list.currentText()
        cr_value = self.ui.column_value.text()
        new_field = self.ui.new_v_col_list.currentText()
        new_val = self.ui.new_value.text()
        self.sql.change_table(t_name, cr_field, cr_value, new_field, new_val)
        # print(t_name, field, value)

    def output_T(self):
        t_name = self.ui.tables_list.currentText()
        try:
            columns, rows = self.sql.get_table(t_name)
        except:
            self.tableWidget.setRowCount(1)
            self.tableWidget.setColumnCount(1)
            self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Какая-то ошибка"))
            self.tableWidget.setColumnWidth(0, 300)
            return 0

        # Row count
        self.tableWidget.setRowCount(len(rows))

        # Column count
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(columns)

        for i in range(len(rows)):
            for j in range(len(rows[i])):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(rows[i][j])))


app = QApplication(sys.argv)
mainWindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedHeight(1013)
widget.setFixedWidth(1713)
widget.show()
sys.exit(app.exec_())
