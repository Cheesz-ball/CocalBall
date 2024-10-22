from PySide6.QtWidgets import QApplication, QWidget
from cocoaball_main import Ui_Form
from PySide6.QtCore import Qt, QRect
class MainWindow(Ui_Form):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint
                           | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.setupUi(self)
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()