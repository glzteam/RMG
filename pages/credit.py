from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, \
    QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from minesql import Minesql
from qfluentwidgets import PrimaryPushButton, TableWidget
import sys


class Credit(QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(650, 350, 300, 250)
        # self.setWindowTitle("游戏结算")

        # 获取积分表数据
        mine_sql = Minesql()
        users = mine_sql.get_credits()
        length = len(users)

        # 创建表格
        self.table_credit = TableWidget(self)
        # 设置表格行列数
        self.table_credit.setRowCount(length)
        self.table_credit.setColumnCount(2)
        # 设置表头
        self.table_credit.setHorizontalHeaderLabels(['昵称', '积分'])
        # 添加数据
        data = {}
        for user in users:
            data[user[1]] = user[2]

        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        for i, (user, score) in enumerate(sorted_data):
            user_item = QTableWidgetItem(user)
            score_item = QTableWidgetItem(str(score))
            self.table_credit.setItem(i, 0, user_item)
            self.table_credit.setItem(i, 1, score_item)

        self.label_credit = QLabel('积分排行')
        # self.push_button_return = QPushButton('返回')
        self.qf_push_button_return = PrimaryPushButton('返回', self)

        self.Hbox_1 = QHBoxLayout()
        self.Hbox_1.addWidget(self.label_credit)
        self.Hbox_1.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.Vbox = QVBoxLayout()
        self.Vbox.addLayout(self.Hbox_1)
        self.Vbox.addWidget(self.table_credit)
        self.Vbox.addWidget(self.qf_push_button_return, 0, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.Vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Credit()
    window.show()
    sys.exit(app.exec())
