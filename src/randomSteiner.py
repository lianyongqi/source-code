# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 11:12:46 2018
随机斯坦纳树实现，找到任意包含所有关键词的节点
基于这些节点构造一颗树
@author: Yanchao
"""
import numpy as np
from apiGraph import apiGraph

class RandomSteinerTree:
    def __init__(self, graph, categories):
        self.graph = graph
        self.numOfNodes = graph.dimension
        self.categories = categories
        self.trees_dict = {}
        
    def run(self, keywords):
        '''
        寻找包含keywords的随机斯坦纳树
        graph: 图的邻接矩阵
        keywords: 关键字的list
        categories: 各api包含的categories的list
        '''
        num_of_keyword = len(keywords)

        visited = np.zeros(self.numOfNodes, dtype=int)
        explored = np.zeros(self.numOfNodes)
        
        all_in = (1 << num_of_keyword) - 1
        
        for i in range(num_of_keyword):
            for v in range(self.numOfNodes):
                if keywords[i] in self.categories[v]:
                    visited[v] |= (1 << i)
                    break
        
        branches = set()
        for v in range(self.numOfNodes):
            if visited[v] != 0:
                branches.add(visited[v])
        branches = list(branches)
        
        index = 0
        while True:
            cur_branch = branches[index]
            branch = self.extend(cur_branch, visited, explored, branches)
            
            if branch == all_in:
                nodes = []
                for v in range(self.numOfNodes):
                    if visited[v] == all_in:
                        nodes.append(v)
                        
                return len(visited[visited == branch]), nodes
            
            if branch == cur_branch:
                index = (index + 1) % len(branches)
            else:
                index = 0
                
        return 0, []
        
    def extend(self, cur_branch, visited, explored, branches):
        for v in range(self.numOfNodes):
            if visited[v] == cur_branch and explored[v] == 0:
#                print('cur_branch:', cur_branch)
                cur_node = v
                
                neighbors = self.graph.neighbors(v)
                
                for n in neighbors:
                    if visited[n] == 0:
                        visited[n] = cur_branch
                        cur_node = n
                        return cur_branch
                    elif visited[n] != cur_branch: #可以合并
                        branch = visited[n]
                        new_branch = cur_branch | branch
#                        print('cur_branch:', cur_branch, 
#                              'branch:', branch,
#                              'new_branch', new_branch)
                        
                        for u in range(self.numOfNodes):
                            if visited[u] == cur_branch or visited[u] == branch:
                                visited[u] = new_branch
                        branches.remove(cur_branch)
                        branches.remove(branch)
                        branches.append(new_branch)
                        
                        return new_branch
                
                explored[cur_node] = 1
                return cur_branch
                    
        
def self_test():
    '''自己构造测试数据，检查算法运行是否正确'''
              #v1 v2 v3 v4 v5 v6 v7 v8 v9 v10v11v12v13v14
    matrix = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], #v1
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], #v2
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], #v3
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], #v4
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0], #v5
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0], #v6
              [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], #v7
              [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], #v8
              [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0], #v9
              [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0], #v10
              [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0], #v11
              [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1], #v12
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1], #v13
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]  #v14
              ];
    graph = apiGraph(matrix)
    #category数据写在了文件中
    categories = []
    with open('dataset/test_category.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line[:-1] #去除换行符
            fields = line.split('\t')
            categories.append(fields[1:])
            
    keywords = ['k1', 'k2']
    algorithm = RandomSteinerTree(graph, keywords, categories)
    weight, nodes = algorithm.run();
    
    print(weight)
    print(nodes)
    
#self_test()
