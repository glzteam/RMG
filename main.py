from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import re
import sys
from qfluentwidgets import MessageBox, InfoBar, InfoBarPosition, setThemeColor

from python_game.Main import Game
from api import User

from pages.login import Login  # 登录页
from pages.home import Home  # 首页
from pages.credit import Credit  # 积分排行
from pages.help import Help  # 帮助页
from pages.register import Register  # 注册页


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        setThemeColor('#28afe9')
        self.setWindowTitle('PyQt-Fluent-Widget')
        self.setWindowIcon(QIcon("./resource/img/logo.png"))
        self.resize(1000, 650)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)  # 这三行代码将窗口移至正中间
        self.setWindowTitle('迷宫游戏')

        # 创建 QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 添加页面
        self.login_page = Login()
        self.stacked_widget.addWidget(self.login_page)
        self.credit_page = None
        self.help_page = Help()
        self.stacked_widget.addWidget(self.help_page)
        self.register_page = Register()
        self.stacked_widget.addWidget(self.register_page)

        # 信号与插槽连接
        self.login_page.pushButton_login.clicked.connect(self.login)
        self.login_page.pushButton_register.clicked.connect(self.go_to_register)
        self.register_page.pushButton_register.clicked.connect(self.register)
        self.register_page.pushButton_exit.clicked.connect(self.go_to_login)
        self.help_page.qf_push_button_return.clicked.connect(self.go_to_home)
        self.login_page.lineEdit_username.clear()
        self.login_page.lineEdit_password.clear()

        # 显示登录页
        self.stacked_widget.setCurrentWidget(self.login_page)

        self.user = None

    def login(self):
        """
        登录
        :return: 无返回值
        """
        username = self.login_page.lineEdit_username.text()
        password = self.login_page.lineEdit_password.text()

        # 检查用户名是否为空
        if not username:
            InfoBar.warning(
                title='提示',
                content="请输入用户名",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return

        pattern_username = re.compile(r'^[a-zA-Z0-9]{1,10}$')
        if not bool(pattern_username.match(username)):
            InfoBar.warning(
                title='提示',
                content="用户名只能包含英文与数字,且长度为1-10",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return

        # 检查密码是否为空
        if not password:
            InfoBar.warning(
                title='提示',
                content="请输入密码",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return
        pattern_password = re.compile(r'^[a-zA-Z0-9]{6,12}$')
        if not bool(pattern_password.match(password)):
            InfoBar.warning(
                title='提示',
                content="密码只能包含英文与数字,且长度为6-12",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return

        # 发起登录请求
        self.user = User(0, username, password)
        if self.user.res["status"] == 1:
            InfoBar.warning(
                title='提示',
                content=self.user.res["message"],
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            # 获取玩家积分与难度
            self.credit = self.user.get_own_credit()
            self.curdif = self.user.get_difficulty()
            self.username = username  # 存储当前用户名全局使用

            title = '提示'
            content = '登陆成功'
            w = MessageBox(title, content, self)
            if w.exec():
                self.login_page.lineEdit_username.clear()
                self.login_page.lineEdit_password.clear()

                # 生成首页
                self.home_page = Home(username, self.credit, self.curdif)
                self.stacked_widget.addWidget(self.home_page)
                self.home_page.qf_push_button_start.clicked.connect(self.start_game)
                self.home_page.qf_push_button_quit_account.clicked.connect(self.go_to_login)
                self.home_page.qf_push_button_credit.clicked.connect(self.go_to_credit)
                self.home_page.qf_push_button_help.clicked.connect(self.go_to_help)

                # 跳转到首页
                self.stacked_widget.setCurrentWidget(self.home_page)
            else:
                self.login_page.lineEdit_username.clear()
                self.login_page.lineEdit_password.clear()

                # 生成首页
                self.home_page = Home(username, self.credit, self.curdif)
                self.stacked_widget.addWidget(self.home_page)
                self.home_page.qf_push_button_start.clicked.connect(self.start_game)
                self.home_page.qf_push_button_quit_account.clicked.connect(self.go_to_login)
                self.home_page.qf_push_button_credit.clicked.connect(self.go_to_credit)
                self.home_page.qf_push_button_help.clicked.connect(self.go_to_help)

                # 跳转到首页
                self.stacked_widget.setCurrentWidget(self.home_page)

    def go_to_register(self):
        """
        跳转到注册页面
        :return:无返回值
        """
        self.login_page.lineEdit_username.clear()
        self.login_page.lineEdit_password.clear()
        self.stacked_widget.setCurrentWidget(self.register_page)

    def go_to_credit(self):
        """
        跳转到积分页面
        :return:无返回值
        """
        users = self.user.get_all_credit()
        self.credit_page = Credit(users)  # 先积分创建页面
        self.stacked_widget.addWidget(self.credit_page)  # 将积分页面添加至页面栈
        self.credit_page.qf_push_button_return.clicked.connect(self.go_to_home)  # 信号与插槽连接
        self.stacked_widget.setCurrentWidget(self.credit_page)  # 页面跳转

    def go_to_help(self):
        """
        跳转到帮助页面
        :return:无返回值
        """
        self.stacked_widget.setCurrentWidget(self.help_page)

    def register(self):
        """
        注册账号
        :return: 无返回值
        """
        # 获取文本框中的文本
        username = self.register_page.lineEdit_username.text()
        nickname = self.register_page.lineEdit_nickname.text()
        password = self.register_page.lineEdit_password.text()
        confirm = self.register_page.lineEdit_confirm.text()

        # 检查用户名是否为空
        if not username:
            InfoBar.warning(
                title='提示',
                content="请输入用户名",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return

        pattern_username = re.compile(r'^[a-zA-Z0-9]{1,10}$')
        if not bool(pattern_username.match(username)):
            InfoBar.warning(
                title='提示',
                content="用户名只能包含英文与数字,且长度为1-10",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return

        # 检查昵称是否为空
        if not nickname:
            InfoBar.warning(
                title='提示',
                content="请输入昵称",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return

        pattern_nickname = re.compile(r'^.{1,10}$')
        if not bool(pattern_nickname.match(nickname)):
            InfoBar.warning(
                title='提示',
                content="昵称的长度为1-10",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return

        # 检查密码是否为空
        if not password:
            InfoBar.warning(
                title='提示',
                content="请输入密码",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return
        pattern_password = re.compile(r'^[a-zA-Z0-9]{6,12}$')
        if not bool(pattern_password.match(password)):
            InfoBar.warning(
                title='提示',
                content="密码只能包含英文与数字,且长度为6-12",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return

        # 检查确认密码是否为空
        if not confirm:
            InfoBar.warning(
                title='提示',
                content="请确认密码",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return

        # 检查两次输入的密码是否一致
        if password != confirm:
            InfoBar.error(
                title='错误',
                content="密码不一致",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            return

        # 发起注册请求
        self.user = User(1, username, password, nickname)
        if self.user.res["status"] == 1:
            InfoBar.warning(
                title='提示',
                content=self.user.res["message"],
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:
            self.show_alert('注册成功！请牢记用户名，丢失则无法登录')
            self.register_page.lineEdit_username.clear()
            self.register_page.lineEdit_nickname.clear()
            self.register_page.lineEdit_password.clear()
            self.register_page.lineEdit_confirm.clear()

            # 保存用户名、积分、难度供后续使用
            self.username = username
            self.credit = 0
            self.curdif = 1

            # 生成首页
            self.home_page = Home(self.username, '0', '1')
            self.stacked_widget.addWidget(self.home_page)
            self.home_page.qf_push_button_start.clicked.connect(self.start_game)
            self.home_page.qf_push_button_quit_account.clicked.connect(self.go_to_login)
            self.home_page.qf_push_button_credit.clicked.connect(self.go_to_credit)
            self.home_page.qf_push_button_help.clicked.connect(self.go_to_help)

            # 跳转到首页
            self.stacked_widget.setCurrentWidget(self.home_page)

    def start_game(self):
        """
        开始游戏
        :return: 无返回值
        """
        try:
            # 获取难度
            difficulty = self.user.get_difficulty()
            game = Game(difficulty)
            game.run_game()
            while True:
                game.check_game_time()
                game.check_game_keys()
                game.check_end()
        except Exception as e:
            if game.identification == 1:
                """
                直接退出
                """
                return
            elif game.identification == 2:
                """
                游戏成功
                """
                # 根据难度增加积分
                if difficulty == 1:
                    self.user.add_credit(1)
                    self.credit = self.credit + 1
                elif difficulty == 2:
                    self.user.add_credit(2)
                    self.credit = self.credit + 2
                elif difficulty == 3:
                    self.user.add_credit(3)
                    self.credit = self.credit + 3
                else:
                    self.user.add_credit(5)
                    self.credit = self.credit + 5

                # 增加难度
                self.user.add_difficulty()
                self.curdif = self.curdif + 1

                # 更新文案
                self.home_page.label_credit.setText('积分：' + str(self.credit))  # 更改积分文案
                self.home_page.label_difficulty.setText('关数：' + str(self.curdif))  # 更改难度文案

                # 提示通关，询问是否进入下一关
                title = '通关'
                content = '恭喜你通关了，要进入下一关吗'
                w = MessageBox(title, content, self)
                if w.exec():
                    self.start_game()
                else:
                    return
            elif game.identification == 3:
                """
                游戏失败
                """
                # 清空难度
                self.user.clear_difficulty()  # 清空数据库
                self.home_page.label_difficulty.setText('关数：1')  # 更改难度文案

                # 失败提示
                title = '失败'
                content = '抱歉，你失败了，请重头再来'
                w = MessageBox(title, content, self)
                if w.exec():
                    self.start_game()
                else:
                    return

    def go_to_home(self):
        """
        返回首页
        :return: 无返回值
        """
        self.stacked_widget.setCurrentWidget(self.home_page)

    def go_to_login(self):
        """
        跳转到登录页
        :return: 无返回值
        """
        self.user = None
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.register_page.lineEdit_username.clear()
        self.register_page.lineEdit_nickname.clear()
        self.register_page.lineEdit_password.clear()
        self.register_page.lineEdit_confirm.clear()

    def show_alert(self, content):
        """
        弹出提示框
        :param content: 提示信息
        :return: 无
        """
        title = '提示'
        w = MessageBox(title, content, self)
        if w.exec():
            pass
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
