import sys
from datetime import datetime
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, Signal, Slot, QObject
import random
from datetime import datetime

HEADER_LABELS = ["Customer", "Quantity", "Part", "Size", "Moulding", "Shipping", "Painting", "Ordered Date", "Due Date", "Comments"]


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]

            # Preform per-type checks and render accordingly
            if isinstance(value, datetime):
                # Render time to MM-DD-YYYY
                return value.strftime("%m-%d-%Y")

            # Default
            return value

        if role == Qt.TextAlignmentRole:
            value = self._data[index.row()][index.column()]

            if index.column() == 1:
                return Qt.AlignRight

        if role == Qt.DecorationRole:
            value = self._data[index.row()][index.column()]

            if isinstance(value, datetime):
                return QtGui.QIcon("calender.png")

            if isinstance(value, bool):
                if value:
                    return QtGui.QIcon("green-check.png")


    def rowCount(self, index):
        # The Length of the outer list
        return len(self._data)

    def columnCount(self, index):
        # The Following takes the first sub-list, and returns
        # the length (only works if all rows are equal length)
        # return len(self._data[0])
        # TODO test if [code below] this works and replace the line above
        length = 0
        for row in self._data:
            if len(row) > length:
                length = len(row)
        return length

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            try:
                return HEADER_LABELS[section]
            except:
                pass

    # def setData(self, index, value, role):
    #     pass
