# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 11:01:53 2017
Steiner Tree类
核心的算法主要包括grow和merge方法
事实上对树的修改主要包括这两个方法
@author: Yanchao
"""

import queue

class Tree:
    '''steiner树基类，提供了一些通用的功能'''
    def __init__(self, keySet, root, weight):
        self.keySet = keySet  #为了提高效率，将keySet看作一个位串
        self.root = root
        self.children = None
        self.weight = weight
        
    
    def display(self, api_dict = None):
        root_name = api_dict[self.root] if api_dict is not None \
                                        else self.root
        print('root:', root_name, 
              ', keySet:', self.keySet, 
              'weight:', self.weight, 'children:{',  root_name, 
                      ' ', end = '');
        self.displayChildren(api_dict)
        print('}')
        
    def displayChildren(self, api_dict):
        if len(self.children) == 0:
            return;
            
        for t in self.children:
            root_name = api_dict[t.root] if api_dict is not None \
                                        else t.root
            print(root_name, end = ' ')
            t.displayChildren(api_dict)
        
class STree(Tree):
    def __init__(self, keySet, root, weight = 1):
        super(STree, self).__init__(keySet, root, weight)
        self.children = []
    
    def grow(self, v, keySet):
        '''
        grow操作，生成一个以v为根的新树
        '''
        newTree = STree(self.keySet, v, self.weight+1)
        newTree.keySet |= keySet
        newTree.children.append(self)
        #keyset不变
        return newTree
         
         
    def merge(self, tree):
        '''merge操作：生成一个新的树'''
        keySet = self.keySet | tree.keySet
        weight = self.weight + tree.weight - 1
        
        newTree = STree(keySet, self.root, weight)
        newTree.children.extend(self.children)
        newTree.children.extend(tree.children)
            
        return newTree
    
    def __lt__(self, other):
        # if self.weight != other.weight:
        #     return self.weight < other.weight
        #
        # return other.keySet - self.keySet
        return self.weight < other.weight
    
    # def __le__(self, other):
    #
    #     return self.weight <= other.weight
    
    def __eq__(self, other):
        return len(self.succeedings - other.succeedings) == 0 and \
            len(other.succeedings - self.succeedings) == 0
    def __hash__(self):
        return hash(len(self.succeedings))

class RTree(Tree):
    '''
    区别于STree，二者的grow操作和merge操作有很大的不同
    RTree更像一个普通的树，为了防止重复，其子树用set表示
    另外，因为每次操作后均不比较节点数，所以这里每次grow操作之前
    需要先判断节点是否已经在树中存在，因此树需要为此一个所有
    节点的set类型变量nodes
    '''
    def __init__(self, keySet, root, weight = 1):
        super(RTree, self).__init__(keySet, root, weight)
        self.nodes = {root}
        self.children = set()
        
    def grow(self, v, keyword):
        '''
        生成一个以v根的新树
        如果v已经在当前树中存在，则返回None
        '''
        if v in self.nodes:
            return None
        
        newTree = RTree(keyword, v, self.weight + 1);
        
        newTree.nodes = newTree.nodes.union(self.nodes)
        newTree.keySet |= self.keySet
        newTree.children.add(self)
        
        return newTree
    
    def merge(self, tree):
        '''
        合并生成一个新的树
        '''
        #如果除了根节点相同外还有其他节点，则不进行合并
        if len(self.nodes.intersection(tree.nodes)) > 1:
            return None
        
        keySet = self.keySet | tree.keySet
        newTree = RTree(keySet, self.root)
        newTree.nodes = self.nodes.union(tree.nodes)
        newTree.weight = len(newTree.nodes)
        newTree.children = newTree.children.union(self.children)
        newTree.children = newTree.children.union(tree.children)
        
        return newTree
    
    def __eq__(self, other):
        '''该函数将在该类型对象添加到set时调用'''
        d1 = self.nodes - other.nodes
        d2 = other.nodes - self.nodes
        return d1 is None and d2 is None
    
    def __hash__(self):
        '''该函数将在该类型对象添加到set时调用'''
        return hash(len(self.nodes))

    
    
class SteinerTreeQueue:
    def __init__(self):
        self.trees_dict = {} #weight: queue of trees
        self.min_weight = 99999
        
    
    def empty(self):
        if len(self.trees_dict) == 0:
            return True
        return False
    
    def get(self):
        _queue = self.trees_dict.get(self.min_weight)
        s_tree = _queue.get()
        
        if _queue.empty():
            self.trees_dict.pop(self.min_weight)            
            weights = self.trees_dict.keys()
            self.min_weight = 99999
            for w in weights:
                if w < self.min_weight:
                    self.min_weight = w;
    
        return s_tree
    
    def put(self, s_tree):
        _queue = self.trees_dict.get(s_tree.weight)
        if _queue is None:
            _queue = queue.Queue()
            self.trees_dict[s_tree.weight] = _queue
            if self.min_weight >= s_tree.weight:
                self.min_weight = s_tree.weight
            
        _queue.put(s_tree)
            
   

#que = SteinerTreeQueue()
#que.put(STree(1, 1))
#que.get()
#print(que.empty())     
#        


