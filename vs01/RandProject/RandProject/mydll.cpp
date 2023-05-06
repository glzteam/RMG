#define BUILD_MYDLL
#include"pch.h"
#include "mydll.h"
#include<iostream>
#include <stdlib.h>
#include <time.h> 
using namespace std;

int** matxier(int row, int col){
	srand((unsigned)time(NULL));
	int** data = 0;     
	data = new int* [row];   
	for (int i = 0; i < row; i++){
		*(data + i) = new int[col];   
	}
	for (int i = 0; i < row; i++)
		for (int j = 0; j < col; j++)
			data[i][j] = rand() % 2;
	return data;
}
