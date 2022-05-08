from time import strftime

import sys
from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import GSheet
import MVC


class CustomOrderWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Custom Order")

        bool_label_col = 4
        bool_col = 3
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
        layout.setColumnStretch(1, 10)

        self.nameEdit = QLineEdit()
        self.partEdit = QLineEdit()
        self.qtyEdit = QSpinBox()
        self.qtySetCheckbox = QCheckBox()
        self.sizeEdit = QSpinBox()
        self.mouldingCheck = QCheckBox()
        self.dueDateBox = QDateEdit()
        self.commentBox = QLineEdit()

        # Make due date average 2 weeks after added
        self.dueDateBox.setDisplayFormat('MM/dd/yyyy')
        self.dueDateBox.setDate(QDate.currentDate().addMonths(1))
        self.dueDateBox.setCalendarPopup(1)
        self.dueDateBox.setMinimumDate(QDate.currentDate())

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
        self.submitButton.clicked.connect(self.add_order)
        self.submitButton.clicked.connect(self.submitButton.parentWidget().close)
        # self.cancelButton.clicked.connect()

    @Slot()
    def add_order(self):
        # Adds appropriate post-affix to the sets for readability in GSheets
        qty = self.qtyEdit.text()
        if self.qtySetCheckbox.isChecked():
            if qty == '1':
                qty += " Set"
            else:
                qty += " Sets"

        order = ["",                                                  # Delivered
                 self.nameEdit.text() if not ' ' else "Unknown",      # Customer Name
                 '',                                                  # Part Number
                 qty,                                                 # Quantity
                 self.partEdit.text(),                                # Part Ordered
                 self.sizeEdit.text() if not '0' else '',             # Size of part ordered
                 str(self.mouldingCheck.isChecked()),                 # Moulding check
                 "False", "False", "False",                           # Internal use indicators (Made, Cut, Pretty)
                 "False",                                             # TODO: Shipping or Painting toggle/radio check
                 "False",                                             # ^
                 str(datetime.today().date().strftime("%m/%d/%Y")),   # Ordered date
                 self.dueDateBox.text(),                              # Due Date
                 "",                                                  # SO Reference
                 self.commentBox.text()                               # Comments
                 ]

        GSheet.send_data(order)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.model = MVC.TableModel(GSheet.get_data())
        self.table.setModel(self.model)

        self.order_button = QPushButton("Add Order")

        self.order_button.clicked.connect(self.show_new_window)
        self.central_widget = QWidget()
        self.addCustomWindow = CustomOrderWindow()
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        self.central_layout.addWidget(self.table)
        self.central_layout.addWidget(self.order_button)

        self.status_bar = QStatusBar(self)
        self.refresh_btn = QToolButton(self.status_bar)
        self.refresh_btn.setToolTip("Refresh")
        self.refresh_btn.setText("Refresh")
        self.setStatusBar(self.status_bar)

        self.refresh_btn.clicked.connect(self.refresh)

    def show_new_window(self):
        self.addCustomWindow.show()

    @Slot()
    def refresh(self):
        self.model = MVC.TableModel(GSheet.get_data())
        self.model.layoutChanged.emit()
        print("Refresh")


app = QApplication(sys.argv)
app.setStyle("fusion")
w = MainWindow()
w.show()
app.exec_()
