import sys
import csv

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QSpinBox, QTableView, QLabel


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('CcalCounter.ui', self)

        self.pushButton.clicked.connect(self.add)
        self.cb: QComboBox = self.comboBox
        self.sb: QSpinBox = self.spinBox
        self.tv: QTableView = self.tableView
        self.label: QLabel = self.label_4

        self.ingridients = []
        self.ccals = []
        self.fats = []
        self.proteins = []
        self.carbs = []

        self.cclas_all = 0
        self.fats_all = 0
        self.proteins_all = 0
        self.carbs_all = 0

        self.ingridient_counter = 0

        self.data = []

        with open("IngridientsDB.csv", 'r', encoding='utf-8') as file:
            all_ingridients = list(csv.DictReader(file, delimiter=',', quotechar='"'))

        for ingridient in all_ingridients:
            self.cb.addItem(ingridient['Ingredient'])
            self.ingridients.append((ingridient['Ingredient']))
            self.ccals.append(ingridient['Ccal'])
            self.fats.append(ingridient['Fats'])
            self.proteins.append(ingridient['Proteins'])
            self.carbs.append(ingridient['Carbs'])
    def add(self):
        grams = self.sb.value()
        h: float = 100
        self.data.append([self.ingridients[self.cb.currentIndex()], float(self.rm_symbol(self.ccals[self.cb.currentIndex()])) / h * grams, float(self.rm_symbol(self.proteins[self.cb.currentIndex()])) / h * grams, float(self.rm_symbol(self.fats[self.cb.currentIndex()])) / h * grams, float(self.rm_symbol(self.carbs[self.cb.currentIndex()])) / h * grams])
        self.model = TableModel(self.data)
        self.tv.setModel(self.model)
        self.cclas_all = self.cclas_all + float(self.rm_symbol(self.ccals[self.cb.currentIndex()])) / h * grams
        self.proteins_all = self.proteins_all + float(self.rm_symbol(self.proteins[self.cb.currentIndex()])) / h * grams
        self.fats_all = self.fats_all + float(self.rm_symbol(self.fats[self.cb.currentIndex()])) / h * grams
        self.carbs_all = self.carbs_all + float(self.rm_symbol(self.carbs[self.cb.currentIndex()])) / h * grams
        self.label.setText("Итого: Калории: " + str(self.cclas_all) + ", белки: " + str(self.proteins_all) + ", жиры: " + str(self.fats_all) + ", углеводы: " + str(self.carbs_all))

    def rm_symbol(self, value):
        res_str = value.replace(",", ".", 1)
        return res_str


app = QApplication(sys.argv)
ex = Window()
ex.show()
sys.exit(app.exec_())
