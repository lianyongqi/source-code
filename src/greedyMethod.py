# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 11:12:46 2018
随机斯坦纳树实现，找到任意包含所有关键词的节点
基于这些节点构造一颗树

该方法修改对一些关键词出现死循环，如 ['Mapping', 'Viewer']
@author: Yanchao
"""
import numpy as np
from apiGraph import apiGraph

class GreedyMethod:
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

        index = -1
        while True:
            branch = self.merge(visited, explored, branches)

            if branch == all_in:
                nodes = []
                for v in range(self.numOfNodes):
                    if visited[v] == all_in:
                        nodes.append(v)

                return len(visited[visited == branch]), nodes

            index = (index + 1) % len(branches)
            cur_branch = branches[index]
            branch = self.extend(cur_branch, visited, explored, branches)

            # if branch == cur_branch:  # 执行的是grow操作
            #     index = (index + 1) % len(branches)
            # else:  # 执行了merge操作后重新开始循环
            #     index = 0

        return 0, []

    def merge(self, visited, explored, branches):
        min_branch = -1
        min_node = -1
        min_neighbor = -1
        cur_min_weight = np.iinfo(np.int32).max

        for cur_branch in branches:
            for v in range(self.numOfNodes):
                if visited[v] == cur_branch and explored[v] == 0:
                    cur_node = v
                    neighbors = self.graph.neighbors(v)

                    # 贪婪区别于随机steiner的地方在于，每一次扩展前他会优先考虑合并包含关键字的邻居节点
                    # 先找所有可能合并的邻居中，合并后的节点数（weight）最小的
                    # min_neighbor = -1
                    for n in neighbors:
                        if visited[n] != 0 and visited[n] != cur_branch:  # 可以合并
                            branch = visited[n]
                            weight = 0
                            for u in range(self.numOfNodes):
                                if visited[u] == branch or visited[u] == cur_branch:
                                    weight += 1

                            if weight < cur_min_weight:
                                cur_min_weight = weight
                                min_neighbor = n
                                min_branch = cur_branch

        if min_neighbor > -1:
            branch = visited[min_neighbor]
            new_branch = min_branch | branch

            for u in range(self.numOfNodes):
                if visited[u] == min_branch or visited[u] == branch:
                    visited[u] = new_branch
            branches.remove(min_branch)
            branches.remove(branch)
            branches.append(new_branch)

            return new_branch

        return 0


    def extend(self, cur_branch, visited, explored, branches):
        for v in range(self.numOfNodes):
            if visited[v] == cur_branch and explored[v] == 0:
                cur_node = v
                neighbors = self.graph.neighbors(v)

                # 增长
                for n in neighbors:
                    if visited[n] == 0:
                        visited[n] = cur_branch
                        cur_node = n
                        return cur_branch

                explored[cur_node] = 1  # 说明cur_node没有可以利用的邻居了，避免进入死循环
                for n in neighbors:
                    if visited[n] != cur_branch:
                        explored[cur_node] = 0
                        break

                return cur_branch


def self_test():
    '''自己构造测试数据，检查算法运行是否正确'''
    # v1 v2 v3 v4 v5 v6 v7 v8 v9 v10v11v12v13v14
    matrix = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],  # v1
              [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],  # v2
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],  # v3
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],  # v4
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],  # v5
              [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],  # v6
              [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],  # v7
              [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],  # v8
              [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],  # v9
              [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],  # v10
              [0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],  # v11
              [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1],  # v12
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],  # v13
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]  # v14
              ];
    graph = apiGraph(matrix)
    # category数据写在了文件中
    categories = []
    with open('../dataset/test_category.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line[:-1]  # 去除换行符
            fields = line.split('\t')
            categories.append(fields[1:])

    keywords = ['k1', 'k2']
    algorithm = GreedyMethod(graph, categories)
    weight, nodes = algorithm.run(keywords);

    print(weight)
    print(nodes)

# self_test()
