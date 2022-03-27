import sys
from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, Signal, Slot, QObject
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QTextEdit, QCheckBox, QSpinBox, QDateEdit)


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
        layout.setColumnMinimumWidth(spacer_col, 5)
        layout.setColumnStretch(1, 10)

        # Name
        self.nameEdit = QLineEdit()
        layout.addWidget(QLabel("Name:"), name_row, edit_label_col)
        layout.addWidget(self.nameEdit, name_row, edit_col)

        # Part
        self.partEdit = QLineEdit()
        layout.addWidget(QLabel("Part"), part_row, edit_label_col)
        layout.addWidget(self.partEdit, part_row, edit_col)

        # Quantity
        self.qtyEdit = QSpinBox()
        self.qtySetCheckbox = QCheckBox()
        layout.addWidget(QLabel("Quantity"), qty_row, edit_label_col)
        layout.addWidget(self.qtyEdit, qty_row, edit_col)
        layout.addWidget(QLabel("Sets"), qty_row, bool_label_col, Qt.AlignLeft)
        layout.addWidget(self.qtySetCheckbox, qty_row, bool_col)

        # Size
        self.sizeEdit = QSpinBox()
        self.mouldingCheck = QCheckBox()
        layout.addWidget(QLabel("Size"),     size_row, edit_label_col)
        layout.addWidget(self.sizeEdit,      size_row, edit_col)
        layout.addWidget(QLabel("Moulding"), size_row, bool_label_col, Qt.AlignLeft)
        layout.addWidget(self.mouldingCheck, size_row, bool_col)

        # Date
        self.dueDateBox = QDateEdit()
        layout.addWidget(QLabel("Due Date"), date_row, edit_label_col)
        layout.addWidget(self.dueDateBox, date_row, edit_col)

        # Comments
        self.commentBox = QTextEdit()
        layout.addWidget(QLabel("Comments"), comment_row, edit_label_col, Qt.AlignTop)
        layout.addWidget(self.commentBox, comment_row, edit_col)

        # Submit Button
        self.submitButton = QPushButton("Submit")
        self.cancelButton = QPushButton("Cancel")
        layout.addWidget(self.submitButton, submit_row,   0, 1, -1)
        layout.addWidget(self.cancelButton, submit_row+1, 0, 1, -1)

        self.setLayout(layout)

        # TODO implement cancel and submit properly

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Push for window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        self.w = CustomOrderWindow()
        self.w.show()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()