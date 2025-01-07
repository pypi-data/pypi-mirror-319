import locale
import sys

from PyQt5 import QtWidgets

locale.setlocale(locale.LC_ALL, "")

__version__ = "0.1.0.post1"

app = QtWidgets.QApplication(sys.argv)
