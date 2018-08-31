# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 11:20:15 2018
对比实验，每一步随机取值
@author: YanChao
"""
import json
import numpy as np
import time
import random

from apiGraph import apiGraph
from algorithm import MinimalSteinerTree
from randomSteiner import RandomSteinerTree
from greedySteiner import GreedySteinerTree

import mashup
from util import prepare_data, generateKeywords, generateNeighborKeywords

def testWithMinimalSteinerTree(graph, categories, keywords):
    '''
    采用MinimalSteinerTree实现包含keyword的api的查询
    返回查询的结点数及运行时间
    '''
    minimal_steiner = MinimalSteinerTree(graph, categories)
    begin = time.time()
    min_tree = minimal_steiner.run(keywords);

    if min_tree is None:
        return None, time.time() - begin

    return min_tree.weight, time.time() - begin


def testWithRandomSteinerTree(graph, categories, keywords):
    '''
    采用RandomSteinerTree实现包含keyword的api的查询
    返回查询的结点数及运行时间
    '''
    random_steiner = RandomSteinerTree(graph, categories)
    begin = time.time()
    weight, _ = random_steiner.run(keywords);

    return weight, time.time() - begin


def testWithGreedySteinerTree(graph, categories, keywords):
    '''
    采用GreedySteinerTree实现包含keyword的api的查询
    返回查询的结点数及运行时间
    '''
    greedy_steiner = GreedySteinerTree(graph, categories)
    begin = time.time()
    weight, _ = greedy_steiner.run(keywords);

    return weight, time.time() - begin

def testWithGreedySteinerTree(graph, categories, keywords):
    '''
    采用GreedySteinerTree实现包含keyword的api的查询
    返回查询的结点数及运行时间
    '''
    greedy_steiner = GreedySteinerTree(graph, categories)
    begin = time.time()
    weight, _ = greedy_steiner.run(keywords);

    return weight, time.time() - begin

def minimal_steiner_vary_with_keywords_num(times = 20):
    '''
    测试minimal steiner tree算法在查找不同个数的关键词下返回的查询结果个数和运行时间的差别
    :return:
    '''
    graph, categories, category_list = prepare_data()

    count_options = [2, 3, 4, 5, 6]
    num_of_options = len(count_options)

    num_nodes = np.zeros((num_of_options, times))
    costs = np.zeros((num_of_options, times))

    dict = {}

    for (i, count) in enumerate(count_options):
        for j in range(times):
            # keywords = generateNeighborKeywords(graph, categories, count, i*10 + j ) #seed = j
            keywords = generateKeywords(categories, count, i * 100 + j)
            num_nodes[i, j], costs[i, j] = testWithMinimalSteinerTree(graph, categories, keywords)
            if (j + 1) % 10 == 0:
                print('>')
            else:
                print('>', end = '')
        print('==================%dkeyword finshed===============' % count)

    dict['num_nodes'] = num_nodes.tolist()
    dict['costs'] = costs.tolist()

    with open('../outputs/minmal_steiner_vary_with_random_neighbor_keywords.json', 'w') as f:
        json.dump(dict, f)


def compare_vary_with_keywords_num(times = 50):
    '''
    测试minimal steiner tree算法在查找不同个数的关键词下返回的查询结果个数和运行时间的差别
    :return:
    '''
    graph, categories, category_list = prepare_data()

    count_options = [2, 3, 4, 5, 6]
    num_of_options = len(count_options)

    num_nodes = np.zeros((3, num_of_options, times))
    costs = np.zeros((3, num_of_options, times))

    dict = {}

    for (i, count) in enumerate(count_options):
        for j in range(times):
            keywords = generateKeywords(category_list, count, i*10 + j ) #seed = j
            num_nodes[0, i, j], costs[0, i, j] = testWithMinimalSteinerTree(graph, categories, keywords)
            num_nodes[1, i, j], costs[1, i, j] = testWithRandomSteinerTree(graph, categories, keywords)
            num_nodes[2, i, j], costs[2, i, j] = testWithGreedySteinerTree(graph, categories, keywords)

            if (j + 1) % 10 == 0:
                print('>')
            else:
                print('>', end = '')
        print('==================%dkeyword finshed===============' % count)

    print(np.average(num_nodes, axis = 2))
    print(np.average(costs, axis = 2))
    # dict['num_nodes'] = num_nodes.tolist()
    # dict['costs'] = costs.tolist()
    #
    # with open('../outputs/compare_vary_with_keywords_num.json', 'w') as f:
    #     json.dump(dict, f)

def minimal_steiner_vary_with_keywords_num_in_mashup(sample_count = 50):
    '''
    以mashup中调用的api的类别（每个api取一个category）为关键词，测试返回的节点数和时间
    对一个每一组mashup中的api类别，我们采用两种形式检索，如要检索的关键词为ABCD，我们会分别检索ABCD和AD两种形式的关键词
    查看其返回的节点数和花费时间
    因为apiGraph就是按mashup来的，因此返回的节点数应该小于或等于mashup中调用的api的个数
    :param sample_count:
    :return:
    '''
    sample_dict = mashup.sample_categories_of_mashup(sample_count)

    graph, categories, _ = prepare_data()

    count_options = [2, 3, 4, 5, 6]
    num_of_options = len(count_options)

    num_nodes = np.zeros((2, num_of_options, sample_count))
    costs = np.zeros((2, num_of_options, sample_count))

    for (i, count) in enumerate(count_options):
        keywords_array = sample_dict[count]
        for j in range(sample_count):
            num_nodes[0, i, j], costs[0, i, j] = testWithMinimalSteinerTree(graph, categories, keywords_array[j])
            customed_keywords = [keywords_array[j, 0], keywords_array[j, -1]]
            num_nodes[1, i, j], costs[1, i, j] = testWithMinimalSteinerTree(graph, categories, customed_keywords)
            if (j + 1) % 10 == 0:
                print('>')
            else:
                print('>', end='')
        print('==================%dkeyword finshed===============' % count)

    dict = {}
    dict['num_nodes'] = num_nodes.tolist()
    dict['costs'] = costs.tolist()

    with open('../outputs/minmal_steiner_vary_with_keywords_num_in_mashup.json', 'w') as f:
        json.dump(dict, f)


def compare_vary_with_keywords_num_in_mashup(sample_count = 50):
    '''
    以mashup中调用的api的类别（每个api取一个category）为关键词，测试返回的节点数和时间
    对一个每一组mashup中的api类别，我们采用两种形式检索，如要检索的关键词为ABCD，我们会分别检索ABCD和AD两种形式的关键词
    查看其返回的节点数和花费时间
    因为apiGraph就是按mashup来的，因此返回的节点数应该小于或等于mashup中调用的api的个数
    :param sample_count:
    :return:
    '''
    sample_dict = mashup.sample_categories_of_mashup(sample_count)

    graph, categories, _ = prepare_data()

    count_options = [2, 3, 4, 5, 6]
    num_of_options = len(count_options)

    num_nodes = np.zeros((3, num_of_options, sample_count))
    costs = np.zeros((3, num_of_options, sample_count))

    for (i, count) in enumerate(count_options):
        keywords_array = sample_dict[count]
        for j in range(sample_count):
            print(keywords_array[j])
            num_nodes[0, i, j], costs[0, i, j] = testWithMinimalSteinerTree(graph, categories, keywords_array[j])
            num_nodes[1, i, j], costs[1, i, j] = testWithRandomSteinerTree(graph, categories, keywords_array[j])
            num_nodes[2, i, j], costs[2, i, j] = testWithGreedySteinerTree(graph, categories, keywords_array[j])
            if (j + 1) % 10 == 0:
                print('>')
            else:
                print('>', end='')
        print('==================%dkeyword finshed===============' % count)

    dict = {}
    dict['num_nodes'] = num_nodes.tolist()
    dict['costs'] = costs.tolist()

    with open('../outputs/compare_vary_with_keywords_num_in_mashup.json', 'w') as f:
        json.dump(dict, f)

def compare_head_tail_keyword_in_mashup(sample_count = 50):
    '''
    以mashup中调用的api的类别（每个api取一个category）为关键词，测试返回的节点数和时间
    对一个每一组mashup中的api类别，我们采用两种形式检索，如要检索的关键词为ABCD，我们会分别检索ABCD和AD两种形式的关键词
    查看其返回的节点数和花费时间
    因为apiGraph就是按mashup来的，因此返回的节点数应该小于或等于mashup中调用的api的个数
    :param sample_count:
    :return:
    '''
    sample_dict = mashup.sample_categories_of_mashup(sample_count)

    graph, categories, _ = prepare_data()

    count_options = [2, 3, 4, 5, 6]
    num_of_options = len(count_options)

    num_nodes = np.zeros((3, num_of_options, sample_count))
    costs = np.zeros((3, num_of_options, sample_count))

    for (i, count) in enumerate(count_options):
        keywords_array = sample_dict[count]
        for j in range(sample_count):
            keywords = [keywords_array[j][0], keywords_array[j][-1]]
            num_nodes[0, i, j], costs[0, i, j] = testWithMinimalSteinerTree(graph, categories, keywords)
            num_nodes[1, i, j], costs[1, i, j] = testWithRandomSteinerTree(graph, categories, keywords)
            num_nodes[2, i, j], costs[2, i, j] = testWithGreedySteinerTree(graph, categories, keywords)
            if (j + 1) % 10 == 0:
                print('>')
            else:
                print('>', end='')
        print('==================%dkeyword finshed===============' % count)

    dict = {}
    dict['num_nodes'] = num_nodes.tolist()
    dict['costs'] = costs.tolist()

    with open('../outputs/compare_head_tail_keywords_in_mashup.json', 'w') as f:
        json.dump(dict, f)




# compare_greedy_steiner_with_greedy(1)
# compare_head_tail_keyword_in_mashup()
# compare_vary_with_keywords_num_in_mashup()
# generate_category_list()
# compare_random_steiner_with_greedy()
minimal_steiner_vary_with_keywords_num()