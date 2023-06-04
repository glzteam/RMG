from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from qfluentwidgets import PrimaryPushButton
import sys


class Home(QWidget):
    def __init__(self, username='默认用户', credit='-', curdif='-'):
        super().__init__()
        # self.setGeometry(650, 350, 300, 250)
        # self.setWindowTitle("首页")

        # 添加用户名和积分
        font = QFont()
        font.setPointSize(15)
        self.label_username = QLabel(self)
        self.label_username.setText('用户名：' + username)
        self.label_username.setFont(font)
        self.label_username.move(50, 50)
        self.label_username.adjustSize()
        # self.resize(400, 50)
        # self.label_username.setStyleSheet("background-color: white; border-radius: 10px;padding:5px")

        self.label_username.size()
        self.label_credit = QLabel(self)
        self.label_credit.setText('积分：' + str(credit))
        self.label_credit.setFont(font)
        self.label_credit.move(50, 90)

        self.label_difficulty = QLabel(self)
        self.label_difficulty.setText('关数：' + str(curdif))
        self.label_difficulty.setFont(font)
        self.label_difficulty.move(50, 130)
        self.label_difficulty.adjustSize()

        # 初始化图片
        self.label_game = QLabel('迷宫游戏')
        # 加载一张图片
        pixmap = QPixmap('./resource/img/logo.png')
        # 将图片设置为QLabel的内容
        self.label_game.setPixmap(pixmap)
        # 调整QLabel的大小以适应图片
        self.label_game.resize(pixmap.width(), pixmap.height())

        # 初始化按钮
        # self.push_button_start = QPushButton('开始游戏')
        # self.push_button_credit = QPushButton('查看积分')
        # self.push_button_help = QPushButton('关于')
        # self.push_button_quit_account = QPushButton('退出当前账号')

        self.qf_push_button_start = PrimaryPushButton('   开始游戏   ', self)
        self.qf_push_button_credit = PrimaryPushButton('   查看积分   ', self)
        self.qf_push_button_help = PrimaryPushButton('      关于      ', self)
        self.qf_push_button_quit_account = PrimaryPushButton('退出当前账号', self)

        # 初始化布局
        self.Vbox = QVBoxLayout()
        self.Hbox_label_game = QHBoxLayout()
        self.Hbox_label_game.addWidget(self.label_game)
        self.Hbox_label_game.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.Vbox.addLayout(self.Hbox_label_game)
        self.Vbox.addWidget(self.qf_push_button_start, 0, Qt.AlignmentFlag.AlignHCenter)
        self.Vbox.addWidget(self.qf_push_button_credit, 0, Qt.AlignmentFlag.AlignHCenter)
        self.Vbox.addWidget(self.qf_push_button_help, 0, Qt.AlignmentFlag.AlignHCenter)
        self.Vbox.addWidget(self.qf_push_button_quit_account, 0, Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(self.Vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec())
