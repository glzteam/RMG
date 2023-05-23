from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from qfluentwidgets import PrimaryPushButton
import sys


class Failed(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(200, 200, 300, 250)
        self.setWindowTitle("游戏结算")

        self.label_failed = QLabel('游戏结束')
        self.push_button_restart = QPushButton('重新开始')

        # signal connect
        self.push_button_restart.clicked.connect(self.restart_game)

        self.Vbox = QVBoxLayout()
        self.Hbox_1 = QHBoxLayout()
        self.Hbox_1.addWidget(self.label_failed)
        self.Hbox_1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.Hbox_2 = QHBoxLayout()
        self.Hbox_2.addWidget(self.push_button_restart)
        self.Hbox_2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.Vbox.addLayout(self.Hbox_1)
        self.Vbox.addLayout(self.Hbox_2)

        self.setLayout(self.Vbox)

    def restart_game(self):
        print('重新开始游戏')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Failed()
    window.show()
    sys.exit(app.exec())
