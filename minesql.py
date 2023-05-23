import mysql.connector as mc
import hashlib


class Minesql(object):
    """
    封装数据库操作
    """
    def __init__(self, host='localhost', user='root', password='123456', database='rmg'):
        """
        数据库初始化
        :param host: 主机名
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名称
        """
        self.mydb = mc.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.credits = []

    def login(self, username, password):
        """
        玩家进行登录
        :param username: 玩家用户名
        :param password: 玩家密码
        :return: 0 表示该用户不存在，1 表示密码错误，2 表示登录成功
        """
        try:
            # 数据库操作
            my_cursor = self.mydb.cursor()
            query = "select `password` from `users` where `username`=%s"
            values = (username,)
            my_cursor.execute(query, values)
            password_result = my_cursor.fetchone()  # 接收密码

            if password_result is not None:
                password_result = password_result[0]  # 接收密码
                password_md5 = hashlib.md5(password.encode()).hexdigest()  # 将本地密码进行 md5 哈希

                if password_result == password_md5:
                    return 2  # 表示登录成功
                else:
                    return 1  # 表示密码错误
            else:
                return 0  # 表示用户不存在
        except mc.Error as e:
            print('数据库错误：', e)

    def register(self, username, nickname, password):
        """
        玩家注册
        :param username: 玩家用户名
        :param nickname: 玩家昵称
        :param password: 玩家密码
        :return: 0 表示该用户已存在，1 表示注册成功
        """
        try:
            # 判断数据库中是否存在该用户
            my_cursor = self.mydb.cursor()
            query = "select count(*) from `users` where `username`=%s"
            values = (username,)
            my_cursor.execute(query, values)
            user_exists = my_cursor.fetchone()[0]  # 返回值为 1，用户存在，返回值为 0，用户不存在

            if user_exists:
                return 0  # 表示用户已存在，请直接登录

            # 注册流程
            password_md5 = hashlib.md5(password.encode()).hexdigest()
            query = "INSERT INTO `users` (`username`, `nickname`, `password`) VALUES (%s, %s, %s)"  # 使用参数化查询来避免SQL注入攻击
            values = (username, nickname, password_md5)  # 参数
            my_cursor.execute(query, values)  # 发起请求
            self.mydb.commit()  # 提交插入操作

            # 注册成功，弹出提示框
            return 1  # 表示注册成功
        except mc.Error as e:
            print('数据库错误：', e)

    def get_credits(self):
        """
        获取全部积分，用于排名
        :return: 全部数据：数组：每一项有用户名、昵称、积分
        """
        try:
            my_cursor = self.mydb.cursor()
            query = "select `username`,`nickname`,`credit` from `users`"
            my_cursor.execute(query)
            users = my_cursor.fetchall()
            return users

        except mc.Error as e:
            print('数据库错误：', e)

    def get_own_credit(self, username):
        """
        获取自己积分
        :param username: 需要查询的用户名
        :return: 积分
        """
        try:
            my_cursor = self.mydb.cursor()
            query = "select `credit` from `users` where `username`=%s"
            data = [username, ]
            my_cursor.execute(query, data)
            users = my_cursor.fetchall()
            return users[0][0]
        except mc.Error as e:
            print('数据库查询出错了！', e.msg)

    def add_credit(self, username, credit_add):
        """
        增加积分
        :param username: 用户名
        :param credit_add: 积分增加量
        :return: 无
        """
        try:
            credit_current = self.get_own_credit(username)  # 获取原积分
            credit = int(credit_current) + int(credit_add)  # 获取总积分

            my_cursor = self.mydb.cursor()
            query = "update `users` set `credit`=%s where `username`=%s"
            data = [credit, username]
            my_cursor.execute(query, data)
            self.mydb.commit()  # 提交更新操作

            return
        except mc.Error as e:
            print('数据库查询出错了！', e.msg)

    def get_own_difficulty(self, username):
        """
        获取自己难度
        :param username: 需要查询的用户名
        :return: 难度
        """
        try:
            my_cursor = self.mydb.cursor()
            query = "select `curdif` from `users` where `username`=%s"
            data = [username, ]
            my_cursor.execute(query, data)
            users = my_cursor.fetchall()
            return users[0][0]
        except mc.Error as e:
            print('数据库查询出错了！', e.msg)

    def add_difficulty(self, username):
        """
        增加难度
        :param username: 用户名
        :return: 无
        """
        try:
            difficulty_current = self.get_own_difficulty(username)  # 获取原积分
            difficulty = int(difficulty_current) + 1  # 获取总积分

            my_cursor = self.mydb.cursor()
            query = "update `users` set `curdif`=%s where `username`=%s"
            data = [difficulty, username]
            my_cursor.execute(query, data)
            self.mydb.commit()  # 提交更新操作

            return
        except mc.Error as e:
            print('数据库查询出错了！', e.msg)

    def clear_difficulty(self, username):
        """
        清空难度
        :param username: 用户名
        :return: 无
        """
        try:
            my_cursor = self.mydb.cursor()
            query = "update `users` set `curdif`=%s where `username`=%s"
            data = ['0', username]
            my_cursor.execute(query, data)
            self.mydb.commit()  # 提交更新操作

            return
        except mc.Error as e:
            print('数据库查询出错了！', e.msg)


if __name__ == '__main__':
    mine_sql = Minesql()
    print(mine_sql.get_credits())
