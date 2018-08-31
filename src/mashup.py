# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 20:20:48 2017
mashup基本操作，包括：
1. 预处理，去除包含没有category的api的mashup
2. 读取
3. 构建邻接矩阵
@author: Yanchao
"""
import numpy as np
import json
import random

def readMashup():
    with open('dataset/mashup_filtered.txt', "r", encoding='utf-8') as f:
        api_dict = dict()
        api_list = []
        i = 0;
        for line in f:
            fields = line.split('   ')
            apis = fields[1].split(',')
            #保存mashup的api序列到api_list数组
            api_list.append(apis)
            #通过api_dict为各api分配index
            for a in apis:
                if api_dict.get(a) is None:
                    api_dict[a] = i
                    i += 1
                    
        return api_list, api_dict
    
def preprocessMashup():
    lines = []
    filter_set = readInvalidApis()
    with open('dataset/mashup.txt', 'r', encoding='utf-8') as f:
        for line in f:
            valid_mashup = True
            fields = line.split('   ')
            apis = fields[1].split(',')
            for a in apis:
                if a in filter_set:
                    valid_mashup = False
                    break
            
            if valid_mashup == True:
                lines.append(line)
                
    with open('dataset/mashup_filtered.txt', 'w', encoding='utf-8') as wf:
        wf.writelines(lines)
        
def readInvalidApis():
    '''该方法读取没有category的api，
    我们需要根据该函数将包含这些api的mashup清除掉
    为了提高查询的速度，我们将这些api放到set中返回'''
    apis = set()
    with open('dataset/api_exception.txt', 'r', encoding = 'utf-8') as f:
        for line in f:
            apis.add(line[:-1])
            
    return apis
    
def constructGraph(api_list, api_dict):
    api_count = len(api_dict)
    print('api_count = ', api_count)
    matrix = np.zeros((api_count, api_count))
    for apis in api_list:
        c = len(apis)
        if c > 1:
            for i in range(c - 1):
                prev = api_dict[apis[i]]
                next = api_dict[apis[i + 1]]
                matrix[prev][next] = 1
                
    return matrix
             
    
    
    
def main():
    api_list,api_dict = readMashup()
    matrix = constructGraph(api_list, api_dict)
    edges = np.sum(matrix, axis = 1)
    total = 0;
    for i in range(37):
        num = len(edges[edges == i])
        total += num
        print(num)
    print('total = ', total)



def extractKeywords():
    categories = json.load(open('dataset/api_categories.json'))
    api_dict = json.load(open('dataset/connected_api_dict.json'))
    
    data = []
    total = 0
    count = 0
    with open('dataset/mashup_filtered.txt', 'r', encoding='utf-8') as f:
        for line in f:
            total += 1
            keywords = []
            fields = line.split("   ")
            apis = fields[1].split(',')
            ignored = False
            for a in apis:
                index = api_dict.get(a)
                if index is None:
                    ignored = True
                    break
                else:
                    for c in categories[index]:
                        if c not in keywords:
                            keywords.append(c)
                
            if ignored:
                continue
            
            count += 1
            data.append({'nodes':len(apis), 'keywords':keywords})
    
    print('total = ', total, ', count = ', count);        
    with open('dataset/test_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

def sample_categories_of_mashup(sample_count = 50, seed = 0):
    '''
    读取mahsup的category数组
    首先以字典的形式，将所有的category数组按category的个数组织
    其次，对不同个数的category数组，分别随机抽取50个category数组，并以json的形式存入文件
    该方法得到的数据作为实验的测试数据
    :param sample_count:
    :return:
    '''
    categories = json.load(open('../dataset/api_categories.json'))
    api_dict = json.load(open('../dataset/connected_api_dict.json'))
    dict = {}
    with open('E:/FangCloudSync/gtd/code/Python/steiner/dataset/mashup_filtered.txt', 'r', encoding='utf-8') as f:
        for line in f:
            fields = line.split('   ')
            apis = fields[1].split(',')

            keywords = []
            has_invalid_api = False
            has_same_keywords = True
            for a in apis:
                index = api_dict.get(a)
                if index is None:
                    # print('unidentified api %s' % (a))
                    has_invalid_api = True
                    break

                for c in categories[index]:
                    if c not in keywords:
                        keywords.append(c)
                        has_same_keywords = False
                        break

                if has_same_keywords:
                    break
            if not has_invalid_api and not has_same_keywords:
                k_num = len(keywords)
                if k_num > 6:
                    k_num = 7

                if dict.get(k_num) is None:
                    dict[k_num] = []
                dict[k_num].append(keywords)

    sample_dict = {}
    for num in range(2, 7):
        keywords = dict[num]
        c_num = len(keywords)

        if c_num < sample_count:
            print('%d has unsufficient instantces (%d)' % (num, c_num))
            sample_dict[num] = dict[num]
            continue

        random.seed(seed)
        indices = random.sample(range(c_num), sample_count)
        sample_dict[num] = (np.array(dict[num])[indices]).tolist()

    return sample_dict

# sample_categories_of_mashup()

