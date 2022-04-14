import sys
from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, Signal, Slot, QObject
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QTextEdit, QCheckBox, QSpinBox, QDateEdit)


import GSheet, MVC


class CustomOrderWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Custom Order")

        bool_label_col = 4
        bool_col = 3
        spacer_col = 2
        edit_label_col = 0
        edit_col = 1

        name_row = 0
        part_row = 1
        qty_row = 2
        size_row = 3
        date_row = 4
        comment_row = 5
        submit_row = 7

        layout = QGridLayout()
        # layout.setColumnMinimumWidth(spacer_col, 5)
        layout.setColumnStretch(1, 10)

        self.nameEdit = QLineEdit()
        self.partEdit = QLineEdit()
        self.qtyEdit = QSpinBox()
        self.qtySetCheckbox = QCheckBox()
        self.sizeEdit = QSpinBox()
        self.mouldingCheck = QCheckBox()
        self.dueDateBox = QDateEdit()
        self.commentBox = QTextEdit()


        # Name
        layout.addWidget(QLabel("Name:"), name_row, edit_label_col)
        layout.addWidget(self.nameEdit, name_row, edit_col)

        # Part
        layout.addWidget(QLabel("Part"), part_row, edit_label_col)
        layout.addWidget(self.partEdit, part_row, edit_col)

        # Quantity
        layout.addWidget(QLabel("Quantity"), qty_row, edit_label_col)
        layout.addWidget(self.qtyEdit, qty_row, edit_col)
        layout.addWidget(QLabel("Set(s)"), qty_row, bool_label_col, Qt.AlignLeft)
        layout.addWidget(self.qtySetCheckbox, qty_row, bool_col)

        # Size
        layout.addWidget(QLabel("Size"),     size_row, edit_label_col)
        layout.addWidget(self.sizeEdit,      size_row, edit_col)
        layout.addWidget(QLabel("Moulding"), size_row, bool_label_col, Qt.AlignLeft)
        layout.addWidget(self.mouldingCheck, size_row, bool_col)

        # Date
        layout.addWidget(QLabel("Due Date"), date_row, edit_label_col)
        layout.addWidget(self.dueDateBox, date_row, edit_col)

        # Comments
        layout.addWidget(QLabel("Comments"), comment_row, edit_label_col, Qt.AlignTop)
        layout.addWidget(self.commentBox, comment_row, edit_col)

        # Submit Button
        self.submitButton = QPushButton("Submit")
        self.cancelButton = QPushButton("Cancel")
        layout.addWidget(self.submitButton, submit_row,   0, 1, -1)
        layout.addWidget(self.cancelButton, submit_row+1, 0, 1, -1)

        self.setLayout(layout)

        # TODO implement cancel and submit properly\
        self.submitButton.clicked.connect(self.print_order)
        # self.cancelButton.clicked.connect()

    @Slot()
    def print_order(self):
        order = [self.nameEdit.text()]
        qty = self.qtyEdit.text()
        if self.qtySetCheckbox.isChecked():
            if qty == '1':
                qty += " Set"
            else:
                qty += " Sets"
        order.append(qty)
        order.append(self.partEdit.text())
        order.append(self.sizeEdit.text())
        # TODO Finish the appends
        print(order)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        # data = [
        #     ['FALSE', 'Trae Eklund', '', '1', 'KW Bowtie Style Visor', '', 'TRUE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'TRUE', '3/28/2022'],
        #     ['FALSE', 'Stock', '', '1', 'Fiberglass standup airbox', '', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'TRUE', '3/28/2022'],
        #     ['FALSE', 'Stock', '', '1', '6 ft Deckplate Section', '', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'FALSE', 'TRUE', '3/28/2022', '', '', 'test']
        # ]

        self.model = MVC.TableModel(GSheet.get_data())
        self.table.setModel(self.model)

        self.button = QPushButton("Push for window")
        self.button.clicked.connect(self.show_new_window)
        self.central_widget = QWidget()
        self.addCustomWindow = CustomOrderWindow()
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        self.central_layout.addWidget(self.table)
        self.central_layout.addWidget(self.button)

    def show_new_window(self, checked):
        self.addCustomWindow.show()


# print(GSheet.print_data())
app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()