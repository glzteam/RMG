import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from python_game.Main import Game


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建标签
        label = QLabel('Hello World!', self)
        label.move(50, 50)

        # 创建按钮
        button = QPushButton('Click me', self)
        button.move(50, 80)
        button.clicked.connect(self.playGame)

        # 设置窗口
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('My PyQt6 App')
        self.show()

    def playGame(self):

        try:
            game = Game()
            game.run_game()
            while True:
                game.game_main()
                game.check_end()
                game.exit_game()
        except Exception as e:
            print("Error:", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())