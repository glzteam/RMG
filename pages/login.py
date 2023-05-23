from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from pages.Ui_LoginWindow import Ui_Form
from qfluentwidgets import setThemeColor
import sys


class Login(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        # self.setGeometry(650, 350, 300, 250)
        # self.setWindowTitle("登录页")

        # ---- 全新尝试 ----
        self.setupUi(self)
        setThemeColor('#28afe9')

        self.label.setScaledContents(False)
        # self.setWindowTitle('PyQt-Fluent-Widget')
        # self.setWindowIcon(QIcon(":/images/logo.png"))
        # self.resize(1000, 650)

        # desktop = QApplication.screens()[0].availableGeometry()
        # w, h = desktop.width(), desktop.height()
        # self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        # # ---- 初始化组件 ----
        # # 初始化标签
        # self.label_username = QLabel('用户名：')
        # self.label_password = QLabel('密码：')
        # # 初始化输入框
        # self.line_edit_username = LineEdit()
        # self.line_edit_username.setPlaceholderText('请输入用户名')
        # self.line_edit_password = LineEdit()
        # self.line_edit_password.setPlaceholderText('请输入密码')
        # self.line_edit_password.setEchoMode(QLineEdit.EchoMode.Password)
        # # 初始化按钮
        # self.push_button_login = QPushButton('确认')
        # self.push_button_new = QPushButton('注册')
        # self.qf_push_button_login = PrimaryPushButton('确认', self)
        # self.qf_push_button_new = PrimaryPushButton('注册', self)
        #
        # # 初始化图片
        # # 从本地读图
        # self.map = QLabel()
        # pixmap_map = QPixmap('resource/img/map.png')  # 按指定路径找到图片
        # self.map.setPixmap(pixmap_map)  # 在label上显示图片
        # self.ikun = QLabel()
        # pixmap_ikun = QPixmap('resource/img/ikun.png')  # 按指定路径找到图片
        # pixmap_ikun = pixmap_ikun.scaled(80, 80)  # 设置大小
        # self.ikun.setPixmap(pixmap_ikun)  # 在label上显示图片
        #
        # # 初始化布局
        # self.Vbox = QVBoxLayout()
        # self.Hbox_3 = QHBoxLayout()
        # self.Hbox_3.addWidget(self.label_username)
        # self.Hbox_3.addWidget(self.line_edit_username)
        # self.Hbox_4 = QHBoxLayout()
        # self.Hbox_4.addWidget(self.label_password)
        # self.Hbox_4.addWidget(self.line_edit_password)
        # self.Vbox.addWidget(self.ikun, 0, Qt.AlignmentFlag.AlignHCenter)
        # self.Vbox.addLayout(self.Hbox_3)
        # self.Vbox.addLayout(self.Hbox_4)
        # self.Vbox.addWidget(self.qf_push_button_login)
        # self.Vbox.addWidget(self.qf_push_button_new)
        #
        # # self.hbox_map = QHBoxLayout()
        # # self.hbox_map.addWidget(self.map)
        #
        # self.hbox = QHBoxLayout()
        # self.hbox.addWidget(self.map, 0, Qt.AlignmentFlag.AlignCenter)
        # self.hbox.addLayout(self.Vbox)
        #
        # self.setLayout(self.hbox)

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
    window = Login()
    window.show()
    sys.exit(app.exec())
