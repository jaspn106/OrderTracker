import sys
from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, Signal, Slot, QObject
import random

HEADER_LABELS = ["Name", "Quantity", "Part", "Size", "Moulding", "Due Date", "Comments", "Ordered Date"]

TEST_ORDER = [
    "Jeff ",  # Name
    "1 Set",  # Quantity
    random.randint(0, 2),  # Part
    random.randint(1, 6),  # Size
    'True',  # Moulding?
    datetime.today(),  # Due date
    "With dip",  # Comment
    datetime.today(),  # Ordered date
]


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list
            # .col() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The Length of the outer list
        return len(self._data)

    def columnCount(self, index):
        # The Following takes the first sub-list, and returns
        # the length (only works if all rows are equal length)
        return len(self._data[0])
        # TODO test if [code below] this works and replace the line above
        # length = 0
        # for row in self._data:
        #     if len(row) > length:
        #         length = len(row)
        # return length

