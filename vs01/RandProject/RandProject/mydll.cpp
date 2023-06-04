#define BUILD_MYDLL
#include"pch.h"
#include "mydll.h"
#include "cstdlib"
#include "ctime"
#include "cmath"
#include "queue"
#include "vector"
#include "cstring"
using namespace std;
const double eps = 1e-6;
const double pi = 3.1415926535;
const int INF = 1e9 + 10;

int mp[N][N];
int mp_[N][N];

//生成参数
int x_size;	//x方向大小
int y_size;	//y方向大小
int room_R;	//房间半径上限
int room_r; //房间半径下限
int room_num;	//房间数量
int room_edge;	//与地图边缘的最小距离
double room_min_dis;	//房间之间最小距离（圆心）

//int room_x, room_y;	//调试生成房间用

double path_r; //路径半宽度
double path_step;	//路径生成步长
int max_path_len;	//最长路径长度
int ring_path_num;	//生成树完成之后增加的路径数量


//--------------
int dx[] = { -1,1,0,0 };
int dy[] = { 0,0,-1,1 };

struct node {
	int x;
	int y;
};
queue <node> q;

int sgn(double x)
{
	if (x > eps)return 1;
	else if (x < -eps)return -1;
	return 0;
}

double random_f(double a, double b, int ratio)//生成浮点随机数（a<=b）
{
	if (sgn(a - b) == 0)return a;
	int p = rand() % (ratio + 1);
	return (b - a) * p / ratio + a;
}

int rounding(double x)
{
	return (int)(x + 0.5);
}

//-------------------------计算几何---------------------------//
struct vec {
	double x;
	double y;
};
vec operator + (vec a, vec b) { return { a.x + b.x,a.y + b.y }; }
vec operator - (vec a, vec b) { return { a.x - b.x,a.y - b.y }; }
bool operator == (vec a, vec b) { return (sgn(a.x - b.x) == 0) && (sgn(a.y - b.y) == 0); }
double x_mult(vec a, vec b) { return a.x * b.y - b.x * a.y; }
double d_mult(vec a, vec b) { return a.x * b.x + a.y * b.y; }
vec n_mult(double a, vec b) { return { b.x * a,b.y * a }; }


double dis(vec a, vec b)
{
	return sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y));
}
vec rotate(vec a, double deg)//将向量a逆时针旋转deg 
{
	return { a.x * cos(deg) - a.y * sin(deg),a.y * cos(deg) + a.x * sin(deg) };
}

struct angle {
	double deg1;
	double deg2;
};
bool is_in(double deg, angle a)//判断某角度是否在角内
{
	if (sgn(deg - a.deg1) == 0 || sgn(deg - a.deg2) == 0)return true;
	//bool ans = (sgn(deg - a.deg1) == 1) && (sgn(a.deg2 - deg) == 1);
	if (sgn(a.deg2 - a.deg1) != -1)return ((sgn(deg - a.deg1) == 1) && (sgn(a.deg2 - deg) == 1));
	return !((sgn(deg - a.deg2) == 1) && (sgn(a.deg1 - deg) == 1));
}
bool is_ins(angle a, angle b)//判断两角是否有交
{
	if (is_in(a.deg1, b) || is_in(a.deg2, b) || is_in(b.deg1, a) || is_in(b.deg2, a))return true;
	return false;
}
angle get_ins(angle a, angle b)//求两角交集
{
	if (is_in(a.deg1, b))
	{
		if (is_in(a.deg2, b))return a;
		return { a.deg1,b.deg2 };
	}
	if (is_in(b.deg1, a))
	{
		if (is_in(b.deg2, a))return b;
		return { b.deg1,a.deg2 };
	}
	return { NULL,NULL };
}
double nlz(double x)//normalization,角度归一化
{
	while (sgn(x - pi) == 1)x -= pi * 2;
	while (sgn(x + pi) != 1)x += pi * 2;
	return x;
}

struct seg {
	vec d1;
	vec d2;
};
double dot_seg_dis(vec a, seg b)
{
	if (sgn(d_mult(b.d2 - b.d1, a - b.d1)) != 1)return dis(a, b.d1);
	if (sgn(d_mult(b.d1 - b.d2, a - b.d2)) != 1)return dis(a, b.d2);
	return abs(x_mult(a - b.d1, b.d2 - b.d1)) / dis(b.d1, b.d2);
}
bool is_on_seg(vec a, seg b)//点a是否在线段b上 
{
	if (sgn(x_mult(a - b.d1, a - b.d2)) != 0)return false;
	if (sgn(a.x - b.d1.x) * sgn(a.x - b.d2.x) != 1 && sgn(a.y - b.d1.y) * sgn(a.y - b.d2.y) != 1)return true;
	return false;
}
bool is_jc_seg(seg a, seg b)//线段a、b是否相交 
{

	if (sgn(x_mult(a.d2 - a.d1, b.d1 - a.d1)) * sgn(x_mult(a.d2 - a.d1, b.d2 - a.d1)) == 1)return false;
	if (sgn(x_mult(b.d2 - b.d1, a.d1 - b.d1)) * sgn(x_mult(b.d2 - b.d1, a.d2 - b.d1)) == 1)return false;

	if (sgn(x_mult(a.d2 - a.d1, b.d2 - b.d1)) == 0)
	{
		if (is_on_seg(b.d1, a) || is_on_seg(b.d2, a))return true;
		if (is_on_seg(a.d1, b) || is_on_seg(a.d2, b))return true;
		return false;
	}
	return true;
}
double seg_seg_dis(seg a, seg b)
{
	if (is_jc_seg(a, b))return 0;
	double ans1 = min(dot_seg_dis(a.d1, b), dot_seg_dis(a.d2, b));
	double ans2 = min(dot_seg_dis(b.d1, a), dot_seg_dis(b.d2, a));
	return min(ans1, ans2);
}

vec node_to_vec(node a)
{
	return { (double)a.x,(double)a.y };
}
node vec_to_node(vec a)
{
	return { rounding(a.x),rounding(a.y) };
}


vector <vec> path[10010];
int cnt_path;

node room_lis[1010];
vector<vec> room_lis_vec;

vector<vec> next_gen[110];

vector<vec> room_lis_vec_tmp;

void map_refresh()
{
	int k, i, j;
	for (k = 0; k <= x_size + 1; k++)
	{
		for (i = 0; i <= y_size + 1; i++)
		{
			mp[k][i] = 1;
		}
	}
	return;
}
void map_save()
{
	int k, i, j;
	for (k = 0; k <= x_size + 1; k++)
	{
		for (i = 0; i <= y_size + 1; i++)
		{
			mp_[k][i] = mp[k][i];
		}
	}
	return;
}
void map_read()
{
	int k, i, j;
	for (k = 0; k <= x_size + 1; k++)
	{
		for (i = 0; i <= y_size + 1; i++)
		{
			mp[k][i] = mp_[k][i];
		}
	}
	return;
}


void init_map(
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
)//地图初始化、参数设定
{
	srand(time(0));
	x_size = x_size_;
	y_size = y_size_;
	room_R = room_R_;
	room_r = room_r_;
	room_num = room_num_;
	room_edge = room_edge_;
	room_min_dis = room_min_dis_;

	path_r = path_r_;
	path_step = path_step_;
	max_path_len = max_path_len_;
	ring_path_num = ring_path_num_;

	map_refresh();

	return;
}

bool is_legal(node a)
{
	if (a.x<1 || a.x>x_size || a.y<1 || a.y>y_size)return false;
	return true;
}
bool is_circle_empty(vec a, double r)//判断圆形区域内mp是否全1
{
	int k, i, j;
	int b, c;
	int x_, y_;
	for (k = ceil(-r); k <= r; k++)
	{
		b = ceil(sqrt((r + 1) * (r + 1) - k * k)) - 1;
		for (i = -b; i <= b; i++)
		{
			x_ = rounding(a.x + k);
			y_ = rounding(a.y + i);
			if (!is_legal({ x_,y_ }))continue;
			if (mp[x_][y_] == 0)return false;
		}
	}
	/*int x = rounding(a.x);
	int y = rounding(a.y);
	int r_ = ceil(r);

	for (k = -r_; k <= r_; k++)
	{
		b = ceil(sqrt((r_ + 1) * (r_ + 1) - k * k)) - 1;
		for (i = -b; i <= b; i++)
		{
			if (!is_legal({ x + k,y + i }))continue;
			if (mp[x + k][y + i] == 0)return false;
		}
	}*/

	return true;
}

//--------------------房间生成--------------------//
bool check(int x, int y)//元胞自动机check
{
	int k, i, j;
	int a, b, c;
	int cnt = 0;
	for (k = -1; k <= 1; k++)
	{
		for (i = -1; i <= 1; i++)
		{
			a = x + k; b = y + i;
			if (a == x && b == y)continue;
			if (mp[a][b] == 1)cnt++;
		}
	}
	if (cnt >= 5)return true;
	return false;

}
void make_empty(int x, int y, int r)//圆形空置
{
	int k, i, j;
	int a, b, c;
	for (k = -r; k <= r; k++)
	{
		a = ceil(sqrt((r + 1) * (r + 1) - k * k)) - 1;
		for (i = -a; i <= a; i++)
		{
			if (!is_legal({ x + k,y + i }))continue;
			mp[x + k][y + i] = 0;
		}
	}
	return;
}
void make_random(int x, int y, int r)//圆形随机
{
	int k, i, j;
	int a, b, c;
	int p;
	//srand(time(0));
	for (k = -r; k <= r; k++)
	{
		a = ceil(sqrt((r + 1) * (r + 1) - k * k)) - 1;
		for (i = -a; i <= a; i++)
		{
			if (!is_legal({ x + k,y + i }))continue;
			if (mp[x + k][y + i] == 0)continue;
			p = rand() % 100 + 1;
			if (p <= 40)mp[x + k][y + i] = 0;
			else mp[x + k][y + i] = 1;
		}
	}
	return;
}
void cell_iter(int x, int y, int r)//元胞自动机
{
	int k, i, j;
	int a, b, c;

	for (j = 1; j <= 2; j++)
	{
		for (k = -r; k <= r; k++)
		{
			a = ceil(sqrt((r + 1) * (r + 1) - k * k)) - 1;
			for (i = -a; i <= a; i++)
			{
				if (!is_legal({ x + k,y + i }))continue;
				if (check(x + k, y + i))mp_[x + k][y + i] = 1;
				else mp_[x + k][y + i] = 0;
				//mp[x + k][y + i] = 0;
			}
		}
		for (k = -r; k <= r; k++)
		{
			a = ceil(sqrt((r + 1) * (r + 1) - k * k)) - 1;
			for (i = -a; i <= a; i++)
			{
				if (!is_legal({ x + k,y + i }))continue;
				mp[x + k][y + i] = mp_[x + k][y + i];
			}
		}
	}

	return;
}
void pruning(int x, int y, int r)//优化剪枝（bfs）
{
	int k, i, j;
	int a, b, c;
	int x_, y_;

	node tmp;
	while (!q.empty())q.pop();

	for (k = -r; k <= r; k++)
	{
		a = ceil(sqrt((r + 1) * (r + 1) - k * k)) - 1;
		for (i = -a; i <= a; i++)
		{
			if (!is_legal({ x + k,y + i }))continue;
			mp_[x + k][y + i] = 1;
		}
	}

	q.push({ x,y });
	mp_[x][y] = 0;
	while (!q.empty())
	{
		//if (q.empty())break;
		tmp = q.front(); q.pop();
		for (k = 0; k < 4; k++)
		{
			x_ = tmp.x + dx[k];
			y_ = tmp.y + dy[k];
			if (!is_legal({ x_,y_ }))continue;
			if (dis(node_to_vec({ x,y }), node_to_vec({ x_,y_ })) > room_R + 1)continue;
			if (mp[x_][y_] == 0 && mp_[x_][y_] == 1)
			{
				mp_[x_][y_] = 0;
				q.push({ x_,y_ });
			}
		}
	}

	for (k = -r; k <= r; k++)
	{
		a = ceil(sqrt((r + 1) * (r + 1) - k * k)) - 1;
		for (i = -a; i <= a; i++)
		{
			if (!is_legal({ x + k,y + i }))continue;
			mp[x + k][y + i] = mp_[x + k][y + i];
		}
	}
	return;
}
void add_room(int x, int y)//添加房间根函数
{
	int k, i, j;
	int a, b, c;

	make_random(x, y, room_R);
	make_empty(x, y, room_r);
	cell_iter(x, y, room_R);
	pruning(x, y, room_R);


	return;
}


bool generate_room_lis1()//法一：纯随机
{
	int k, i, j, g, h;
	int x, y;

	int up1 = 20;
	int up2 = 10;

	for (k = 1; k <= up1; k++)
	{
		for (i = 1; i <= room_num; i++)
		{
			for (j = 1; j <= up2; j++)
			{
				x = rand() % (x_size - 2 * room_edge) + room_edge;
				y = rand() % (y_size - 2 * room_edge) + room_edge;
				for (g = 1; g < i; g++)
				{
					if (dis(node_to_vec({ x,y }), node_to_vec(room_lis[g])) <= room_min_dis + 1)break;
				}
				if (g == i)break;
			}
			if (j == up2 + 1)break;
			room_lis[i] = { x,y };
		}
		if (i == room_num + 1)return true;
	}
	return false;
}

//---------两种进阶生成方式---------//
bool is_legal_vec(vec a)
{
	if (a.x >= room_edge && a.x <= x_size - room_edge && a.y >= room_edge && a.y <= y_size - room_edge)return true;
	return false;
}//房间坐标是否合法
double min_room_dis(vector<vec> lis)//平面最近点对
{
	int k, i, j;
	double ans = INF;
	for (k = 0; k < lis.size() - 1; k++)
	{
		for (i = k + 1; i < lis.size(); i++)
		{
			ans = min(ans, dis(lis[k], lis[i]));
		}
	}
	return ans;
}

bool room_gen_iter1()
{
	int k, i, j;
	double deg;
	vec e, v;
	int gen_size = 50;


	for (k = 1; k <= gen_size; k++)
	{
		next_gen[k].clear();
		for (i = 0; i < room_num; i++)
		{
			for (j = 0; j < 20; j++)
			{
				deg = random_f(0, pi * 2, 1000);
				e = { cos(deg),sin(deg) };
				v = room_lis_vec[i] + e;
				if (is_legal_vec(v))break;
			}
			if (j == 20)v = room_lis_vec[i];
			next_gen[k].push_back(v);
		}
	}

	int next_;
	double a = 0, b;



	for (k = 1; k <= gen_size; k++)
	{
		b = min_room_dis(next_gen[k]);
		if (b > a)
		{
			next_ = k;
			a = b;
		}
	}

	for (k = 0; k < room_num; k++)room_lis_vec[k] = next_gen[next_][k];

	if (a >= room_min_dis + 1)return true;
	return false;

}
bool generate_room_lis2()//法二：梯度下降/遗传算法
{
	int k, i, j;
	int x, y;

	for (k = 1; k <= room_num; k++)
	{
		for (i = 0; i < 20; i++)
		{
			x = rand() % (x_size - 2 * room_edge) + room_edge;
			y = rand() % (y_size - 2 * room_edge) + room_edge;
			for (j = 1; j < k; j++)
			{
				if (x == room_lis[j].x && y == room_lis[j].y)break;
			}
			if (j == k)break;
		}
		if (i == 20)return false;
		room_lis[k] = { x,y };

	}
	room_lis_vec.clear();
	for (k = 1; k <= room_num; k++)room_lis_vec.push_back(node_to_vec(room_lis[k]));
	for (k = 0; k < 100; k++)
	{
		if (room_gen_iter1())break;
	}
	if (k == 100)return false;

	for (k = 1; k <= room_num; k++)room_lis[k] = vec_to_node(room_lis_vec[k - 1]);
	return true;
}

bool room_gen_iter2()
{
	int k, i, j;
	bool pd;
	vec v;
	double d;

	pd = true;
	room_lis_vec_tmp.clear();
	for (k = 0; k < room_lis_vec.size(); k++)
	{
		v = { 0,0 };

		for (i = 0; i < room_lis_vec.size(); i++)
		{
			if (i == k)continue;
			d = dis(room_lis_vec[k], room_lis_vec[i]);
			if (d > room_min_dis)continue;
			pd = false;
			v = v + n_mult(room_min_dis - d, room_lis_vec[k] - room_lis_vec[i]);

		}
		if (v.x == 0 && v.y == 0)
		{
			room_lis_vec_tmp.push_back(room_lis_vec[k]);
			continue;
		}
		d = dis({ 0,0 }, v);
		if (d > 1)v = n_mult(0.1, v);
		else v = n_mult(0.05, v);

		while (!is_legal_vec(room_lis_vec[k] + v))
		{
			v = n_mult(0.5, v);
			if (dis({ 0,0 }, v) < 1.0)
			{
				v = { 0,0 };
				break;
			}
		}

		room_lis_vec_tmp.push_back(room_lis_vec[k] + v);

	}

	for (k = 0; k < room_num; k++)room_lis_vec[k] = room_lis_vec_tmp[k];

	return pd;
}
bool generate_room_lis3()//法三：斥力平衡
{
	int k, i, j;
	int x, y;

	room_lis[1] = { room_edge,room_edge };
	room_lis[2] = { x_size - room_edge,y_size - room_edge };

	for (k = 3; k <= room_num; k++)
	{
		for (i = 0; i < 20; i++)
		{
			x = rand() % (x_size - 2 * room_edge) + room_edge;
			y = rand() % (y_size - 2 * room_edge) + room_edge;
			for (j = 1; j < k; j++)
			{
				if (x == room_lis[j].x && y == room_lis[j].y)break;
			}
			if (j == k)break;
		}
		if (i == 20)return false;
		room_lis[k] = { x,y };

	}
	room_lis_vec.clear();
	for (k = 1; k <= room_num; k++)room_lis_vec.push_back(node_to_vec(room_lis[k]));

	int up = 500;

	for (k = 0; k < up; k++)
	{
		if (room_gen_iter2())break;
	}
	if (k == up)return false;

	for (k = 1; k <= room_num; k++)room_lis[k] = vec_to_node(room_lis_vec[k - 1]);
	return true;

}

//--------------------路径生成--------------------//
bool new_path(vector<vec>& path_, vec st, vec ed, double step, double deg1, double deg2)//degree_from, degree_to
{
	int k, i, j;
	int a, b, c;

	vec last = st;
	vec now = st;
	vec v1, v2, v;

	angle a1, a2;

	double deg;
	double d;

	path_.clear();
	path_.push_back(st);


	//while (true)
	int up = dis(st, ed) / step * 2;
	int up2 = 20;
	for (k = 0; k < up; k++)
	{
		if (dis(now, ed) <= step)
		{
			path_.push_back(ed);
			return true;
		}
		v1 = rotate(now - last, -deg1);
		v2 = rotate(ed - now, -deg2);

		if (last == now)a1 = { atan2(v2.y,v2.x),nlz(atan2(v2.y,v2.x) + 2.0 * deg2) };
		else
		{

			a1 = { atan2(v1.y,v1.x),nlz(atan2(v1.y,v1.x) + 2.0 * deg1) };
			a2 = { atan2(v2.y,v2.x),nlz(atan2(v2.y,v2.x) + 2.0 * deg2) };
			if (!is_ins(a1, a2))return false;
			a1 = get_ins(a1, a2);
		}
		if (sgn(a1.deg1 - a1.deg2) == 1)a1.deg2 += pi * 2;



		d = max((double)room_R + 2.0 * path_r, 3.0 * path_r);
		for (i = 0; i < up2; i++)
		{
			deg = random_f(a1.deg1, a1.deg2, 100);
			v = { step * cos(deg),step * sin(deg) };
			v = v + now;
			if (!is_legal_vec(v))continue;

			if (dis(v, st) <= d || dis(v, ed) <= d || is_circle_empty(v, path_r + 1.0))break;
		}
		if (i == up2)return false;

		path_.push_back(v);

		last = now;
		now = v;
	}
	return false;
}


void show_one_seg_bfs(seg sg, double r)
{
	int k, i, j;
	int x_, y_;
	node a;
	vec v;

	while (!q.empty())q.pop();
	//q.push({ rounding(sg.d1.x),rounding(sg.d1.y) });
	//q.push({ rounding(sg.d2.x),rounding(sg.d2.y) });

	for (k = 0; k <= path_step; k++)
	{
		v = sg.d1 + n_mult(1.0 * k / path_step, sg.d2 - sg.d1);
		a = vec_to_node(v);
		mp[a.x][a.y] = 0;
		q.push(vec_to_node(v));
	}


	while (!q.empty())
	{
		a = q.front(); q.pop();
		for (k = 0; k < 4; k++)
		{
			x_ = a.x + dx[k]; y_ = a.y + dy[k];
			if ((!is_legal({ x_,y_ })) || mp[x_][y_] == 0)continue;

			v = { (double)x_, (double)y_ };
			if (sgn(dot_seg_dis(v, sg) - r) == 1)continue;
			mp[x_][y_] = 0;
			q.push({ x_,y_ });
		}
	}

	return;
}
void show_one_path(vector<vec> path_, double r)
{
	int k, i, j;
	int len = path_.size();

	//for (k = 0; k < len; k++)mp[rounding(path_[k].x)][rounding(path_[k].y)] = 0;
	for (k = 1; k < len; k++)show_one_seg_bfs({ path_[k - 1],path_[k] }, r);

	return;
}

void show_path()
{
	int k, i, j;
	int a, b, c;

	for (k = 1; k <= cnt_path; k++)show_one_path(path[k], path_r);

	return;
}

struct r_pair {
	int a;
	int b;
};
vector<r_pair> pair_lis;	//全部可能房间对
vector<r_pair> slt_pair_lis;	//路径选用房间对
bool vis[1010][1010];

int fa[1010];
int find(int x)
{
	int k = x, i;
	while (fa[k] != k)k = fa[k];
	while (fa[x] != k)
	{
		i = fa[x]; fa[x] = k; x = i;
	}
	return k;
}

bool path_check(int a, int b)
{
	int k, i, j;
	seg sg = { {(double)room_lis[a].x,(double)room_lis[a].y},{(double)room_lis[b].x,(double)room_lis[b].y} };
	if (dis(sg.d1, sg.d2) > max_path_len)return false;
	for (k = 1; k <= room_num; k++)
	{
		if (k == a || k == b)continue;
		if (dot_seg_dis({ (double)room_lis[k].x,(double)room_lis[k].y }, sg) <= room_R)return false;
	}
	return true;
}
bool generate_path()
{
	int k, i, j;
	int a, b, c;
	seg seg1, seg2;

	pair_lis.clear();
	slt_pair_lis.clear();

	for (k = 1; k < room_num; k++)
	{
		for (i = k + 1; i <= room_num; i++)
		{
			if (path_check(k, i))pair_lis.push_back({ k,i });
		}
	}

	if (pair_lis.size() < room_num - 1 + ring_path_num)return false;
	random_shuffle(pair_lis.begin(), pair_lis.end());
	cnt_path = 0;

	memset(vis, false, sizeof(vis));

	for (k = 1; k <= room_num; k++)fa[k] = k;

	for (k = 0; k < pair_lis.size(); k++)
	{
		a = find(pair_lis[k].a);
		b = find(pair_lis[k].b);
		if (a == b)continue;

		seg1 = { node_to_vec(room_lis[pair_lis[k].a]),node_to_vec(room_lis[pair_lis[k].b]) };
		for (i = 0; i < slt_pair_lis.size(); i++)
		{
			seg2 = { node_to_vec(room_lis[slt_pair_lis[i].a]),node_to_vec(room_lis[slt_pair_lis[i].b]) };
			if ((pair_lis[k].a != slt_pair_lis[i].a) && (pair_lis[k].b != slt_pair_lis[i].b))
			{
				//if (seg_seg_dis(seg1, seg2) <= path_r * 2)break;
				if (is_jc_seg(seg1, seg2))break;
			}

		}
		if (i < slt_pair_lis.size())continue;


		for (i = 0; i < 20; i++)
		{
			if (!new_path(path[++cnt_path], node_to_vec(room_lis[pair_lis[k].a]), node_to_vec(room_lis[pair_lis[k].b]),
				path_step, pi / 6, pi / 6))
			{
				cnt_path--;
			}
			else break;
		}
		if (i == 20)continue;


		slt_pair_lis.push_back(pair_lis[k]);
		fa[a] = b;

		vis[pair_lis[k].a][pair_lis[k].b] = true;

		show_one_path(path[cnt_path], path_r);

		if (cnt_path == room_num - 1)break;

	}

	if (cnt_path != room_num - 1)return false;

	for (k = 0; k < pair_lis.size(); k++)
	{

		if (cnt_path == room_num - 1 + ring_path_num)return true;
		if (vis[pair_lis[k].a][pair_lis[k].b])continue;

		for (i = 0; i < 20; i++)
		{
			if (!new_path(path[++cnt_path], node_to_vec(room_lis[pair_lis[k].a]), node_to_vec(room_lis[pair_lis[k].b]),
				path_step, pi / 6, pi / 6))
			{
				cnt_path--;
			}
			else break;
		}
		if (i == 20)continue;
		show_one_path(path[cnt_path], path_r);

	}

	return false;


}



//-----------------------效果展示/调试/整体生成------------------------//


bool generate_map()
{
	int k, i, j;
	int a, b, c;

	for (k = 0; k < 20; k++)
	{
		if (generate_room_lis3())break;
	}
	if (k == 20)return false;

	for (k = 1; k <= room_num; k++)add_room(room_lis[k].x, room_lis[k].y);

	map_save();
	for (k = 0; k < 20; k++)
	{
		if (!generate_path())map_read();
		else break;
	}
	if (k == 20)return false;

	return true;

}

bool generate(
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
)
{
	int k, i, j;

	init_map(
		x_size_,	//x方向大小
		y_size_,	//y方向大小
		room_R_,	//房间半径上限
		room_r_, //房间半径下限
		room_num_,	//房间数量
		room_edge_,	//与地图边缘的最小距离
		room_min_dis_,	//房间之间最小距离（圆心）
		path_r_, //路径半宽度
		path_step_,	//路径生成步长
		max_path_len_,	//最长路径长度
		ring_path_num_	//生成树完成之后增加的路径数量
	);

	if (!generate_map())return false;


	for (k = 0; k <= x_size + 1; k++)
	{
		for (i = 0; i <= y_size + 1; i++)
		{
			MP[k][i] = mp[k][i];
		}
	}

	return true;
}






