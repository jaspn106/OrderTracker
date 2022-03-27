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
        super.__init__()
        self._data = data

    def data(self, index:PySide6.QtCore.QModelIndex, role:int=...) -> typing.Any:
        pass