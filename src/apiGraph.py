# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 11:09:32 2017
该文件定义了aGraph类，包含了生成steiner树时所需的一些图的方法
@author: Yanchao
"""

class apiGraph:
    def __init__(self, matrix):
        self.matrix = matrix
        self.dimension = len(self.matrix)
        
    def neighbors(self, u):
        neighbors = []
        for i in range(self.dimension):
            if self.matrix[u][i] == 1:
                neighbors.append(i)
                
        return neighbors
    
    

