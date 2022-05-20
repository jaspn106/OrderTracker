from time import strftime

import sys
from datetime import datetime
from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import QAction, QIcon
import time

import GSheet
import MVC


class PresetOrderWindow(QWidget):
    def __init__(self):
        super(PresetOrderWindow, self).__init__()

        self.setWindowTitle("New Order")

        self._COLUMNS = 10
        self.presets = QButtonGroup(self)
        self.index = 0
        self.custom_order_window = CustomOrderWindow()

        # Layouts
        main_layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        button_layout = QHBoxLayout()

        # Widgets
        add_new_preset = QPushButton("Add New Preset")
        add_new_custom = QPushButton("Custom Order")

        # Adding Widgets to Layouts
        button_layout.addWidget(add_new_preset)
        button_layout.addWidget(add_new_custom)

        # Set Layout
        main_layout.addLayout(button_layout)
        main_layout.addLayout(self.grid_layout)
        self.setLayout(main_layout)

        # Connect things
        add_new_preset.clicked.connect(self.create_preset_order)
        add_new_custom.clicked.connect(self.add_custom_order)
        self.presets.idClicked.connect(self.add_preset_order)

    @Slot()
    def add_order_btn(self):
        for i in range(self.index,self.index+10):
            strb = "testing/"
            stri = '.png'
            numb = self.index % 10
            mix = strb + str(numb) + stri
            print(mix)

            self.presets.addButton(QPushButton(str(self.index)), self.index)
            self.presets.addButton(QPushButton(QIcon(mix), str(self.index)), self.index)
            # self.presets.button(self.index).clicked.connect(self.create_preset_order)
            self.grid_layout.addWidget(self.presets.button(self.index),
                                       (self.index / self._COLUMNS),
                                       (self.index % self._COLUMNS))
            self.index += 1
            print("ButtonID: ", self.index-1 % 2)

    @Slot()
    def create_preset_order(self, order_id):
        print(order_id)
        preset_question_grid = QGridLayout()

        size_group = QButtonGroup()
        size_default_in = QRadioButton("Inch", self)
        size_default_ft = QRadioButton("Foot", self)
        size_group.addButton(size_default_ft)
        size_group.addButton(size_default_in)

        moulding_group = QButtonGroup()
        moulding_default_never = QRadioButton("Never", self)
        moulding_default_maybe = QRadioButton("Maybe", self)
        moulding_group.addButton(moulding_default_maybe)
        moulding_group.addButton(moulding_default_never)

        quantity_group = QButtonGroup()
        quantity_default_never = QRadioButton("Never", self)
        quantity_default_maybe = QRadioButton("Maybe", self)
        quantity_group.addButton(quantity_default_maybe)
        quantity_group.addButton(quantity_default_never)

        preset_question_grid.addWidget(QLabel("Size default: "), 0, 0)
        preset_question_grid.addWidget(size_default_ft, 0, 1)
        preset_question_grid.addWidget(size_default_in, 0, 2)

        preset_question_grid.addWidget(QLabel("Moulding default: "), 1, 0)
        preset_question_grid.addWidget(moulding_default_maybe, 1, 1)
        preset_question_grid.addWidget(moulding_default_never, 1, 2)

        preset_question_grid.addWidget(QLabel("Quantity default: "), 2, 0)
        preset_question_grid.addWidget(quantity_default_maybe, 2, 1)
        preset_question_grid.addWidget(quantity_default_never, 2, 2)

        self.add_preset_window = QWidget()
        self.add_preset_window.setLayout(preset_question_grid)
        self.add_preset_window.show()

    @Slot()
    def add_preset_order(self, order_id):
        pass

    @Slot()
    def add_custom_order(self):
        self.custom_order_window.show()

class CustomOrderWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New Custom Order")

        layout = QVBoxLayout()
        form_layout = QFormLayout()
        button_box = QHBoxLayout()

        self.nameEdit = QLineEdit()
        self.partEdit = QLineEdit()
        self.qtyEdit = QSpinBox()
        self.qtySetCheckbox = QCheckBox()
        self.sizeEdit = QSpinBox()
        self.mouldingCheck = QCheckBox()
        self.dueDateBox = QDateEdit()
        self.commentBox = QLineEdit()
        self.submitButton = QPushButton("Submit")
        self.cancelButton = QPushButton("Cancel")

        # Special sauce to make calender not show Jan 1st, 2000 as default and current date and end date
        # Make due date average 1 weeks after added
        self.dueDateBox.setDisplayFormat('MM/dd/yyyy')
        self.dueDateBox.setDate(QDate.currentDate().addMonths(1))
        self.dueDateBox.setCalendarPopup(1)
        self.dueDateBox.setMinimumDate(QDate.currentDate())

        # Create the form
        form_layout.addRow("Name: ", self.nameEdit)
        form_layout.addRow("Part: ", self.partEdit)
        form_layout.addRow("Quantity: ", self.qtyEdit)
        form_layout.addRow("Set: ", self.qtySetCheckbox)
        form_layout.addRow("Size: ", self.sizeEdit)
        form_layout.addRow("Moulding: ", self.mouldingCheck)
        form_layout.addRow("Due date: ", self.dueDateBox)
        form_layout.addRow("Special notes: ", self.commentBox)

        # Assemble button box
        button_box.addWidget(self.submitButton)
        button_box.addWidget(self.cancelButton)

        #
        layout.addLayout(form_layout)
        layout.addLayout(button_box)
        self.setLayout(layout)

        # TODO implement cancel and submit properly\
        self.submitButton.clicked.connect(self.send_order)
        # self.submitButton.clicked.connect(self.submitButton.parentWidget().close())
        # self.cancelButton.clicked.connect()

    @Slot()
    def send_order(self, order = False):
        if order is False:
            order = self.add_order()
        print("Sending", order)
        GSheet.send_data(order)

    def add_order(self):
        # Adds appropriate post-affix to the sets for readability in GSheets
        qty = self.qtyEdit.text()
        if self.qtySetCheckbox.isChecked():
            if qty == '1':
                qty += " Set"
            else:
                qty += " Sets"

        order = ["",                                                  # Delivered
                 self.nameEdit.text() if self.nameEdit.text() else "Unknown",      # Customer Name
                 '',                                                  # Part Number
                 qty,                                                 # Quantity
                 self.partEdit.text(),                                # Part Ordered
                 self.sizeEdit.text(),             # Size of part ordered
                 str(self.mouldingCheck.isChecked()),                 # Moulding check
                 "False", "False", "False",                           # Internal use indicators (Made, Cut, Pretty)
                 "False",                                             # TODO: Shipping or Painting toggle/radio check
                 "False",                                             # ^
                 str(datetime.today().date().strftime("%m/%d/%Y")),   # Ordered date
                 self.dueDateBox.text(),                              # Due Date
                 "",                                                  # SO Reference
                 self.commentBox.text()                               # Comments
                 ]

        return order


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(800,600)
        self.table = QtWidgets.QTableView()
        self.table.verticalHeader().hide()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.model = MVC.TableModel(GSheet.get_data())
        self.table.setModel(self.model)

        self.addPresetWindow = PresetOrderWindow()

        self.setCentralWidget(self.table)

        # Create and add toolbar
        tool_bar = QToolBar(self)
        self.addToolBar(tool_bar)

        # Create and add actions
        add_order_action = QAction(QIcon("icons8-plus-+-50.png"), "New Order", self)
        tool_bar.addAction(add_order_action)
        add_order_action.triggered.connect(self.show_add_preset_window)

        refresh_action = QAction(QIcon('refresh2.png'), "Refresh", self)
        tool_bar.addAction(refresh_action)
        refresh_action.triggered.connect(self.refresh)

    @Slot()
    def show_add_preset_window(self):
        self.addPresetWindow.show()

    @Slot()
    def refresh(self):
        self.table.resizeColumnsToContents()
        self.model = MVC.TableModel(GSheet.get_data())
        self.table.setModel(self.model)
        print("Refresh")


app = QApplication(sys.argv)
app.setStyle("fusion")
w = MainWindow()
w.show()
app.exec_()
