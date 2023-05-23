from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from qfluentwidgets import PrimaryPushButton
import sys


class Help(QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(650, 350, 300, 250)
        # self.setWindowTitle("帮助")

        # ---- 初始化组件 ----
        # 创建标签
        self.label_title = QLabel('迷宫游戏')
        self.label_purpose = QLabel('该应用程序由葛震鹏开发\n游戏由张永记开发\n地图随机生成算法由李知拙编写\n目的旨在展示地图随机生成算法\n代码在xxx，欢迎提交issue')
        # 排列方式设置
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.label_purpose.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        # 开启换行
        self.label_purpose.setWordWrap(True)

        # 初始化按钮
        self.qf_push_button_return = PrimaryPushButton('返回', self)

        # ---- 初始化布局 ----
        self.Vbox = QVBoxLayout()
        self.Vbox.addWidget(self.label_title)
        self.Vbox.addWidget(self.label_purpose)
        self.Vbox.addWidget(self.qf_push_button_return, 0, Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.Vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Help()
    window.show()
    sys.exit(app.exec())
