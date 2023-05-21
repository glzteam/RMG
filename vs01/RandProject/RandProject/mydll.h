#pragma once

const int N = 1010;

//声明导出函数
#ifdef BUILD_MYDLL
#define API_SYMBOL _declspec(dllexport)
#else
#define API_SYMBOL _declspec(dllimport)
#endif

extern "C" API_SYMBOL bool generate(
	int(*MP)[N],
	int x_size_,	//x方向大小
	int y_size_,	//y方向大小
	int room_R_,	//房间半径上限
	int room_r_, //房间半径下限
	int room_num_,	//房间数量
	int room_edge_,	//与地图边缘的最小距离
	double room_min_dis_,	//房间之间最小距离（圆心）
	double path_r_, //路径半宽度
	double path_step_,	//路径生成步长
	int max_path_len_,	//最长路径长度
	int ring_path_num_	//生成树完成之后增加的路径数量
);