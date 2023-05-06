#pragma once

//声明导出函数
#ifdef BUILD_MYDLL
#define API_SYMBOL _declspec(dllexport)
#else
#define API_SYMBOL _declspec(dllimport)
#endif

extern "C" API_SYMBOL int** matxier(int row, int col);