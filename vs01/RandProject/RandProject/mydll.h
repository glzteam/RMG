#pragma once

const int N = 1010;

//������������
#ifdef BUILD_MYDLL
#define API_SYMBOL _declspec(dllexport)
#else
#define API_SYMBOL _declspec(dllimport)
#endif

extern "C" API_SYMBOL bool generate(
	int(*MP)[N],
	int x_size_,	//x�����С
	int y_size_,	//y�����С
	int room_R_,	//����뾶����
	int room_r_, //����뾶����
	int room_num_,	//��������
	int room_edge_,	//���ͼ��Ե����С����
	double room_min_dis_,	//����֮����С���루Բ�ģ�
	double path_r_, //·������
	double path_step_,	//·�����ɲ���
	int max_path_len_,	//�·������
	int ring_path_num_	//���������֮�����ӵ�·������
);