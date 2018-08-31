import json
import random
import numpy as np
from apiGraph import apiGraph

def generate_category_list():
    '''
    为了避免每次生成的category list的顺序不同，我们将其写入文件
    以后直接读取该文件获取所有的category list
    ps: 本方法只运行一次，生成文件后以后就没有调用的必要了
    :return:
    '''
    categories = json.load(open('../dataset/api_categories.json'))
    category_list = []

    for c in categories:
        category_list.extend(c)

    category_list = list(set(category_list))

    with open('../dataset/category_list.json', 'w') as f:
        json.dump(category_list, f)

def prepare_data():
    '''
    加载关键词图结构，返回关键字图和类别列表
    :return:
    '''
    #加载预先生成的图结构
    graph = apiGraph(json.load(open('../dataset/graph.json')))

    categories = json.load(open('../dataset/api_categories.json'))

    category_list = json.load(open('../dataset/category_list.json'))

    return graph, categories, category_list



def generateKeywords(category_list, count, seed = 0):
    '''随机生成count个搜索关键词'''
    category_count = len(category_list)
    random.seed(seed)
    indices = random.sample(range(category_count), count)
    keywords = np.array(category_list)[indices]

    return keywords




