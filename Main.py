import sys
import MainGui
from PyQt5 import QtWidgets
# from PyQt5.QtGui import QIcon, QPixmap

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Poisson denoise With Total Variation")
    ex = MainGui.App()
    sys.exit(app.exec_())