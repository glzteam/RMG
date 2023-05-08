import ctypes, ctypes.util


class Settings():
    # 游戏参数的设定
    def __init__(self):
        self.length = 30  # 地图的长度
        self.width = 40  # 地图的宽度
        self.cur_dif = 5  # 游戏的难度，即是游戏关数

    def find_dll(self, dll_name):
        # 查找dll
        return ctypes.util.find_library(dll_name)

    def load_dll(self, dll_path):
        try:
            # 加载动态库，若失败则抛出异常
            vc_dll = ctypes.CDLL(dll_path)
            # 获取动态库的函数
            vc_func = vc_dll.matxier
            # 做类型适配
            # vc_func.argtypes = [ctypes.c_int, ctypes.c_int]
            vc_func.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))
            # 该处是调用C++的函数，设置欲传递的参数，传入后得到预期的结果
            m = self.length
            n = self.width
            matrix_ptr = vc_func(m, n)
            # 将二维矩阵转换为 Python 中的列表
            matrix = [[matrix_ptr[i][j] for j in range(n)] for i in range(m)]
            return matrix

        except OSError as e:
            print(e, "加载dll失败")

    # 设置类的成员函数，用于实例化后调取生成地图的基础二维矩阵
    def out_matrix(self):
        dll_path = self.find_dll("C:\\Users\\27142\\Desktop\\vspy01\\RandProject.dll")
        if dll_path:
            return self.load_dll(dll_path)

