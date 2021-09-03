#pragma once
// the degree of btree
#define M 2
#define valuetype string
#include <vector>
#include <string>
using namespace std;

typedef struct btree_nodes {
	int k[2*M-1];

	struct btree_nodes *p[2*M];
	int num;
	bool is_leaf;
	struct btree_nodes *prev;  // 供B+Tree
	struct btree_nodes *next;  // 供B+Tree
	
} btree_node;


typedef struct StorageNode{
	btree_node bnode;
	int index[M];   // 索引集合:index_set 
}storage_node;

typedef struct StorageStruct{
	storage_node *snode;
	int len;
}storage_struct;
