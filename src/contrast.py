# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 11:20:15 2018
对比实验，每一步随机取值
@author: YanChao
"""

from apiGraph import apiGraph
# from contrastAlgorithm2 import RandomAlgorithm2
# from contrastAlgorithm import RandomAlgorithm
from algorithm import MinimalSteinerTree
from algorithm_new import MinimalSteinerTree2
from randomSteiner import RandomSteinerTree
from contrastAlgorithm import RandomAlgorithm
# from randomPrim import RandomPrim
from greedyPrim import GreedyPrim
import json
import numpy as np
import time
import random

class ContrastTest:
    def __init__(self):
        self.graph = apiGraph(json.load(open('../dataset/graph.json')))
        self.categories = json.load(open('../dataset/api_categories.json'))
        self.api_dict = json.load(open('../dataset/connected_api_dict.json'))
        self.reverseApiDict()
        self.combineCategoryList()
        
        print('total vertexes:', self.graph.dimension)
        
    def reverseApiDict(self):
        '''
        初始化动作
        该方法将api_dict中的key和value交换，形成一个新的词典
        '''
        self.api_dict_reverse = {}
        for key in self.api_dict:
            self.api_dict_reverse[self.api_dict[key]] = key
            
    def combineCategoryList(self):
        '''初始化动作，将所有的类别合并为一个list'''
        #合并categoriy_list
        category_set = set()
        for c in self.categories:
            category_set = category_set.union(set(c))
            
        self.category_list = list(category_set)
        
    def generateKeywords(self, count):
        '''随机生成count个搜索关键词'''
        category_count = len(self.category_list)
        indices = random.sample(range(category_count), count)
        keywords = np.array(self.category_list)[indices]
        
        return keywords
    
    def contrastWithNKeywords(self, n, times = 1):
        '''对比n个keywords的实验结果，执行times次'''
        totalWeight = np.array([0.0, 0.0, 0.0]) # totalWeight[0]: Minimal, totalWeight[1]: Random
        totalTime = np.array([0.0, 0.0, 0.0]) # totalTime[0]: Minimal, totalTime[1]: Random 
        
        for i in range(times):
            #Greedy Prim
            keywords = self.generateKeywords(n)
            weight,t = self.testWithRandomAlgorithm(keywords)
            totalWeight[0] += weight;
            totalTime[0] += t;
#            print(weight, ',', t)
            #Random SteinerTree
            weight,t = self.testWithMinimalSteinerTree2(keywords)
            totalWeight[1] += weight
            totalTime[1] += t
            
            #Minimal Steiner Tree
            weight,t = self.testWithMinimalSteinerTree(keywords)
            totalWeight[2] += weight
            totalTime[2] += t
            
        return totalWeight/times, totalTime/times
    
    def contrastWithMashupDataset(self):
        test_data = json.load(open('dataset/test_dataset.json'))
        nodes = {}
        times = {}
        
        counter = 0
        count_6 = 0
        for t in test_data:
            keywords = t['keywords']
            numOfKeywords = len(keywords)
            
            if numOfKeywords == 6:
                count_6 += 1
            
            if numOfKeywords > 9:
                continue
            
            if nodes.get(numOfKeywords) is None:
                nodes[numOfKeywords] = [[], [], []]
            count = nodes[numOfKeywords]
            
            if times.get(numOfKeywords) is None:
                times[numOfKeywords] = [[], [], []]
            time = times[numOfKeywords]
            
#            w,t = self.testWithMinimalSteinerTree(keywords)
#            if w is None:  #如何出现找不到最小斯坦纳树的情况，则不进行统计
#                print('w is none')
#                continue 
            w,t = 0, 0
            count[0].append(w)
            time[0].append(t)
#            w,t = self.testWithRandomSteinerTree(keywords)
            w,t = self.testWithRandomPrim(keywords)
            count[1].append(w)
            time[1].append(t)
                
            w,t = self.testWithGreedyPrim(keywords)
#            w,t = self.testWithRandomSteinerTree2(keywords)            
            count[2].append(w)
            time[2].append(t)
            counter += 1
            if counter % 50 == 0:
                print('>', end = '')
            
            
        with open('dataset/result_data_nodes.csv', 'w', encoding='utf-8') as f:
            for k in nodes:
                print(k, ':', len(nodes[k][0]))
                for v in nodes[k]:
                    f.write(str(np.average(v)))
                    f.write('\t')
                f.write(str(k))
                f.write('\n')
        
        with open('dataset/result_data_time.csv', 'w', encoding='utf-8') as f:
            for k in times:
                for v in times[k]:
                    f.write(str(np.average(v)))
                    f.write('\t')
                f.write(str(k))
                f.write('\n')
                
            
    def contrastSuccessRateWithMashup(self):
        test_data = json.load(open('dataset/test_dataset.json'))
        count = [[], [], []]
        num = 0
        
        for t in test_data:
            all_keywords = t['keywords']
            max_nodes = t['nodes']
            
            keywords = [all_keywords[0], all_keywords[-1]]
            
            w,t = self.testWithMinimalSteinerTree(keywords)
            if w is None:  #如何出现找不到最小斯坦纳树的情况，则不进行统计
                continue
            if w <= max_nodes:
                count[0].append(1)
            else:
                count[0].append(0)

            w,t = self.testWithGreedyPrim(keywords)
            if w <= max_nodes:
                count[1].append(1)
            else:
                count[1].append(0)
            w,t = self.testWithRandomPrim(keywords)
            if w <= max_nodes:
                count[1].append(1)
            else:
                count[1].append(0)
            #显示进度
            num += 1
            print('>', end = '')
            if num % 50 == 0:
                print('')
            
        print('total = ', len(count[0]))
        print(sum(count[0]), sum(count[1]), sum(count[2]))            
                
    def testWithMinimalSteinerTree(self, keywords, display = False):
        '''
        采用MinimalSteinerTree实现包含keyword的api的查询
        返回tree的结点数及运行时间
        '''
        begin = time.time()
        algorithm = MinimalSteinerTree(self.graph, keywords, 
                                       self.categories);
        minTree = algorithm.run();
        
        if minTree is None:
            return None, time.time() - begin
        
        if display:
            minTree.display(self.api_dict_reverse)
            
        return minTree.weight, time.time()-begin

    def testWithMinimalSteinerTree2(self, keywords, display=False):
        '''
        采用MinimalSteinerTree实现包含keyword的api的查询
        返回tree的结点数及运行时间
        '''
        begin = time.time()
        algorithm = MinimalSteinerTree2(self.graph, keywords,
                                       self.categories);
        minTree = algorithm.run();

        if minTree is None:
            return None, time.time() - begin

        if display:
            minTree.display(self.api_dict_reverse)

        return minTree.weight, time.time() - begin
    
    def testWithRandomSteinerTree(self, keywords, display = False):
        '''
        采用MinimalSteinerTree实现包含keyword的api的查询
        返回tree的结点数及运行时间
        '''
        begin = time.time()
        algorithm = RandomSteinerTree(self.graph, keywords, 
                                       self.categories);
        weight,nodes = algorithm.run();
        
#        if tree is None:
#            return None, time.time() - begin
#        
#        if display:
#            tree.display(self.api_dict_reverse)
            
        return weight, time.time()-begin
    
    def testWithRandomSteinerTree2(self, keywords, display = False):
        '''
        采用MinimalSteinerTree实现包含keyword的api的查询
        返回tree的结点数及运行时间
        '''
        begin = time.time()
        algorithm = RandomAlgorithm2(self.graph, keywords, 
                                       self.categories);
        minTree = algorithm.run();
        
        if display:
            minTree.display(self.api_dict_reverse)
        return minTree.weight, time.time()-begin
    
    def testWithRandomAlgorithm(self, keywords, display = False):
        '''
        采用MinimalSteinerTree实现包含keyword的api的查询
        返回tree的结点数及运行时间
        '''
        begin = time.time()
        algorithm = RandomAlgorithm(self.graph, keywords, 
                                       self.categories);
        minTree = algorithm.run();
        
        if display:
            minTree.display(self.api_dict_reverse)
        return minTree.weight, time.time()-begin
    
    def testWithRandomPrim(self, keywords, display = False):
        '''
        采用prim生成最小生成树的方法
        返回tree的节点数及运行时间
        '''
        begin = time.time()
        algorithm = RandomPrim(self.graph, self.categories)
        
        minTree = algorithm.run(keywords) #这个算法的生成树是用数组表示的，没有采用SteinerTree树结构
        
        return len(minTree), time.time() - begin
    
    def testWithGreedyPrim(self, keywords, display = False):
        '''
        采用prim生成最小生成树的方法
        返回tree的节点数及运行时间
        '''
        begin = time.time()
        algorithm = GreedyPrim(self.graph, self.categories)
        
        minTree = algorithm.run(keywords) #这个算法的生成树是用数组表示的，没有采用SteinerTree树结构
        
        return len(minTree), time.time() - begin
    
        
test = ContrastTest()

#print(test.contrastWithNKeywords(5, times = 20))
counts = [4, 5, 6, 7, 8]
for i in counts:
    avgWeight, avgTime = test.contrastWithNKeywords(i, times = 1)
    print('=========', i, ' keywords=========')
    print(avgWeight)
    print(avgTime)
#test.contrastWithMashupDataset()
#test.contrastSuccessRateWithMashup()

#keywords = ['Search', 'Reference', 'Viewer']
#keywords = ['URL Shortener', 'URLs']
#keywords = ['Shipping',  'eCommerce']
#keywords = ['Email', 'Analytics', 'Social', 'Travel', 'Weather', 'Music']
#keywords = ['Reporting', 'OAuth', 'Lyrics',  'Romanian']
#keywords = ['Comparisons', 'eCommerce', 'Classifieds']
#print(test.testWithRandomSteinerTree(keywords, False))
#keywords = ['Search', 'Sales']
#print(test.testWithGreedyPrim(keywords, display=False))
#print(test.testWithRandomSteinerTree(keywords, True))
#keywords = ['Messaging', 'Text', 'Applications', 'Telephony', 'Voice']
#test.testWithMinimalSteinerTree(keywords, display=True)
#test.testWithRandomSteinerTree(keywords, display=True)


            

