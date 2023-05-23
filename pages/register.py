from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from pages.Ui_RegisterWindow import Ui_Form
from qfluentwidgets import setThemeColor
import sys


class Register(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        # self.setGeometry(650, 350, 300, 250)
        # self.setWindowTitle("登录页")

        self.setupUi(self)
        setThemeColor('#28afe9')

        self.label.setScaledContents(False)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap("./resource/img/background.jpg").scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Register()
    window.show()
    sys.exit(app.exec())
