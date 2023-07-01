from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication
import backend
from backend import *
from page import keypanel

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main = keypanel.Ui_MainWindow()
        self.main.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QApplication([])
    pencere = Application()
    pencere.show()
    sys.exit(app.exec_())