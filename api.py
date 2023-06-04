import requests
import json


class User(object):
    def __init__(self, category, username, password, nickname=""):
        # JWT字符串
        self.Authorization = ""
        self.res = {}
        self.username = ""

        # 登录
        if category == 0:
            response = requests.post("http://localhost:85/user/login", data={
                "username": str(username),
                "password": str(password)
            })

            if response.status_code == 200:
                res = json.loads(response.text)

                if res["status"] == 0:
                    self.Authorization = res["token"]
                    self.username = str(username)
                self.res = res
            else:
                print("请求失败，错误码：", response.status_code)
        # 注册
        elif category == 1:
            response = requests.post("http://localhost:85/user/register", data={
                "username": str(username),
                "nickname": str(nickname),
                "password": str(password)
            })

            if response.status_code == 200:
                res = json.loads(response.text)

                if res["status"] == 0:
                    self.Authorization = res["token"]
                    self.username = str(username)
                self.res = res
            else:
                print("请求失败，错误码：", response.status_code)

    def get_all_credit(self):
        response = requests.get("http://localhost:85/credit/getall", headers={"Authorization": self.Authorization})

        if response.status_code == 200:
            return json.loads(response.text)["data"]

        else:
            print("请求失败，错误码：", response.status_code)

    def get_own_credit(self):
        response = requests.get("http://localhost:85/credit/getown", params={"username": self.username},
                                headers={"Authorization": self.Authorization})

        if response.status_code == 200:
            return json.loads(response.text)["data"]["credit"]

        else:
            print("请求失败，错误码：", response.status_code)

    def add_credit(self, credit):
        response = requests.post("http://localhost:85/credit/add",
                                 data={"username": self.username, "credit": str(credit)},
                                 headers={"Authorization": self.Authorization})

        if response.status_code == 200:
            return json.loads(response.text)["status"]

        else:
            print("请求失败，错误码：", response.status_code)

    def get_difficulty(self):
        response = requests.get("http://localhost:85/difficulty/get", params={"username": self.username},
                                headers={"Authorization": self.Authorization})

        if response.status_code == 200:
            res = json.loads(response.text)
            if res["status"] == 0:
                return res["data"]["curdif"]

        else:
            print("请求失败，错误码：", response.status_code)

    def add_difficulty(self):
        response = requests.post("http://localhost:85/difficulty/add", data={"username": self.username},
                                 headers={"Authorization": self.Authorization})

        if response.status_code == 200:
            res = json.loads(response.text)
            print(res["message"])

        else:
            print("请求失败，错误码：", response.status_code)

    def clear_difficulty(self):
        response = requests.post("http://localhost:85/difficulty/clear", data={"username": self.username},
                                 headers={"Authorization": self.Authorization})

        if response.status_code == 200:
            res = json.loads(response.text)
            print(res["message"])

        else:
            print("请求失败，错误码：", response.status_code)


if __name__ == "__main__":
    # try:
    #     user = User(0, "test4", "000000", "测试4号")
    #     print(user.res)
    # except Exception as e:
    #     print(e)
    user = User(0, "test", "000000", "测试4号")
    print(user.clear_difficulty())
