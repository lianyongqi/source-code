import json
import numpy as np
from matplotlib import pyplot as plt

experiments_names = ['minmal_steiner_vary_with_keywords_num',
                     'compare_head_tail_keywords_in_mashup',
                     'minmal_steiner_vary_with_keywords_num_in_mashup',
                     'compare_vary_with_keywords_num_in_mashup']

def load_result(filename):
    with open('../outputs/%s.json' % (filename), 'r') as f:
        dict = json.load(f)

        return np.array(dict['num_nodes']), np.array(dict['costs'])

def draw_convergence_with_times():
    num_nodes, costs = load_result(experiments_names[0])
    times = num_nodes.shape[1]

    average_of_count = np.average(num_nodes, axis = 1)
    print(num_nodes.shape, average_of_count.shape)

    average_num_nodes = [np.average(num_nodes[:, : i + 1], axis = 1) for i in range(times)]
    average_num_nodes = np.array(average_num_nodes)

    print(average_num_nodes.shape)
    plt.xlabel('repeated experiment times')
    plt.ylabel('number of nodes')
    plt.ylim(0, 15)
    for i in range(5):
        plt.plot(range(1, times + 1), average_num_nodes[:, i], label='l = %d' % (i + 2))
    plt.legend(loc = 'upper right')
    plt.savefig('../outputs/convergence.png')

def draw_nodes_found_by_minimal_steiner():
    num_nodes, costs = load_result(experiments_names[2])

    average_num_nodes = np.average(num_nodes, axis =2)
    average_costs = np.average(costs, axis = 1)

    keyword_num_options = [2, 3, 4, 5, 6]
    plt.xlabel('l: number of keywords')
    plt.xticks(keyword_num_options)
    plt.ylabel('number of nodes')
    plt.plot(keyword_num_options, average_num_nodes[0], marker='*')

    plt.savefig('../outputs/nodes_found_by_minimal.png')
    plt.show()

def draw_nodes_found_by_minimal_steiner_with_head_tail():
    num_nodes, costs = load_result(experiments_names[1])

    average_num_nodes = np.average(num_nodes[0], axis =1)

    keyword_num_options = [2, 3, 4, 5, 6]
    plt.xlabel('l: number of keywords')
    plt.xticks(keyword_num_options)
    plt.ylim(0, 4)
    plt.ylabel('number of nodes')
    plt.plot(keyword_num_options, average_num_nodes, marker='*')

    plt.savefig('../outputs/nodes_found_by_minimal_with_head_tail.png')
    plt.show()

def draw_costs_by_minimal_steiner_with_head_tail():
    num_nodes, costs = load_result(experiments_names[1])

    average_costs = np.average(costs[0], axis =1)

    keyword_num_options = [2, 3, 4, 5, 6]
    plt.xlabel('l: number of keywords')
    plt.xticks(keyword_num_options)
    plt.ylim(0, 0.1)
    plt.ylabel('computation time (s)')
    plt.plot(keyword_num_options, average_costs, marker='*')

    plt.savefig('../outputs/costs_by_minimal_with_head_tail.png')
    plt.show()


def draw_costs_by_minimal_steiner():
    num_nodes, costs = load_result(experiments_names[2])

    average_costs = np.average(costs, axis = 2)

    keyword_num_options = [2, 3, 4, 5, 6]
    plt.xlabel('l: number of keywords')
    plt.xticks(keyword_num_options)
    plt.ylabel('computation time (s)')
    plt.plot(keyword_num_options, average_costs[0], marker='*')

    plt.savefig('../outputs/costs_of_minimal_vary_with_keywords_num.png')


def draw_minimal_found_nodes_between_random_and_mashup_keywords():
    '''
    绘制minmimal steiner算法查询随机生成的keywords与mashup中的keywords的柱状图
    :return:
    '''
    num_nodes, costs = load_result(experiments_names[2])
    num_nodes2, costs2 = load_result(experiments_names[0])

    average_num_nodes = np.average(num_nodes, axis=2)
    average_num_nodes2 = np.average(num_nodes2, axis = 1)
    average_costs = np.average(costs, axis=2)

    keyword_num_options = np.array([2, 3, 4, 5, 6])

    total_width, n = 0.8, 2
    width = total_width/n

    # plt.rc('text', usetex=True)
    plt.xlabel('l:number of keywords')
    plt.ylabel('number of nodes')
    plt.bar(keyword_num_options - width, average_num_nodes[0], width = width, label='mashup keywords')
    plt.bar(keyword_num_options, average_num_nodes2, width=width, label='random keywords')

    plt.legend()
    plt.savefig('../outputs/nodes_of_minimal_between_random_and_mashup_keywords.png')

def draw_minimal_costs_between_random_and_mashup_keywords():
    '''
    绘制minmimal steiner算法查询随机生成的keywords与mashup中的keywords的消耗的时间的柱状图
    :return:
    '''
    num_nodes, costs = load_result(experiments_names[2])
    num_nodes2, costs2 = load_result(experiments_names[0])

    average_costs = np.average(costs, axis=2)
    average_costs2 = np.average(costs2, axis = 1)

    keyword_num_options = np.array([2, 3, 4, 5, 6])

    total_width, n = 0.8, 2
    width = total_width/n

    plt.xlabel('l: number of keywords')
    plt.ylabel('computation time (s)')
    plt.bar(keyword_num_options - width, average_costs[0], width = width, label='mashup keywords')
    plt.bar(keyword_num_options, average_costs2, width=width, label='random keywords')

    plt.legend()
    plt.savefig('../outputs/costs_of_minimal_between_random_and_mashup_keywords.png')


def draw_success_rate_between_random_and_mashup_keywords():
    '''
    绘制minmimal steiner算法查询随机生成的keywords与mashup中的keywords的消耗的时间的柱状图
    :return:
    '''
    sample_count = 50
    num_nodes, costs = load_result(experiments_names[2])
    num_nodes2, costs2 = load_result(experiments_names[0])

    keyword_num_options = np.array([2, 3, 4, 5, 6])

    success_rate = np.zeros((2, 5))
    for (idx, num) in enumerate(keyword_num_options):
        success_rate[0, idx] = np.sum(num_nodes[0, idx] <= num) * 100.0/sample_count
        success_rate[1, idx] = np.sum(num_nodes2[idx]  <= num * 2) * 100.0/sample_count

    total_width, n = 0.8, 2
    width = total_width/n

    plt.xlabel('l: number of keywords')
    plt.ylabel('success rate (%)')
    plt.ylim(0, 120)
    plt.yticks([20, 40, 60, 80, 100])
    plt.bar(keyword_num_options - width, success_rate[0], width = width, label='mashup keywords')
    plt.bar(keyword_num_options, success_rate[1], width=width, label='random keywords')

    plt.legend(loc='upper')#, bbox_to_anchor=(0.8, 1.2))
    plt.savefig('../outputs/success_rates_of_minimal_between_random_and_mashup_keywords_by2.png')
    plt.show()

def draw_nodes_with_different_methods():
    num_nodes, costs = load_result(experiments_names[3])

    average_num_nodes = np.average(num_nodes, axis=2)

    print(average_num_nodes)

    keyword_num_options = np.array([2, 3, 4, 5, 6])

    total_width, n = 0.8, 3
    width = total_width / n
    x = keyword_num_options - (total_width - width)/2.0

    plt.xlabel('l: number of keywords')
    plt.ylabel('number of nodes')
    plt.bar(x, average_num_nodes[0], width=width, label='WAR')
    plt.bar(x + width, average_num_nodes[2], width=width, label='Greedy')
    plt.bar(x + 2 * width, average_num_nodes[1], width=width, label='Random')

    plt.legend(loc='upper left')
    plt.savefig('../outputs/nodes_found_by_methods_with_head_tail.png')

def draw_success_rates_of_different_methods():
    num_nodes, costs = load_result(experiments_names[3])
    sample_count = 50
    success_rates = np.zeros((3, 5))

    keyword_num_options = np.array([2, 3, 4, 5, 6])

    for i in range(3):
        for (idx, num) in enumerate(keyword_num_options):
            success_rates[i, idx] = np.sum(num_nodes[i, idx, :] <= num * 3) * 100.0 / sample_count

    print(success_rates)
    total_width, n = 0.8, 3
    width = total_width / n
    x = keyword_num_options - (total_width - width)/2.0


    plt.xlabel('l: number of keywords')
    # plt.xlim(1, 8)
    plt.ylabel('success rate (%)')
    plt.ylim(0, 125)
    plt.yticks([20, 40, 60, 80, 100])
    plt.bar(x, success_rates[0], width=width, label='WAR')
    plt.bar(x + width, success_rates[2], width=width, label='Greedy')
    plt.bar(x + 2 * width, success_rates[1], width=width, label='Random')

    plt.legend(loc='upper right')
    # plt.savefig('../outputs/success_rates_of_methods_with_head_tail_by3.png')
    plt.show()

def draw_costs_with_different_methods():
    '''
    对比三种不同的方法，在给定mashup中的keywords的前提下，返回结果所花费的时间
    :param e_index: 1, 对比只给mashup中的第一个和最后一个keyword时查询的时间开销；
                    2，给出mashup所有的keyword的时间开销
    :return:
    '''
    num_nodes, costs = load_result(experiments_names[3])

    average_costs = np.average(costs, axis=2)
    log_average_costs = np.log(average_costs)

    keyword_num_options = np.array([2, 3, 4, 5, 6])

    plt.xlabel('l:number of keywords')
    plt.xticks(keyword_num_options)

    plt.ylabel(r'computation time ($log_2$)')
    plt.plot(keyword_num_options, log_average_costs[0], marker='*', label='WAR')
    plt.plot(keyword_num_options, log_average_costs[2], marker='*', label='Greedy')
    plt.plot(keyword_num_options, log_average_costs[1], marker='*', label='Random')
    plt.legend()
    # plt.show()
    plt.savefig('../outputs/log_costs_of_methods.png')


def draw_overlap_between_all_and_head_tail_keywords():
    '''
    比较在查询一个mashup中的所有keywords和只查询第一个和最后一个keywords时，三种方法返回的api数
    :return:
    '''
    num_nodes, _ = load_result(experiments_names[3])
    num_nodes2, _ = load_result(experiments_names[1])

    average_num_nodes = np.average(num_nodes, axis=2)
    average_num_nodes2 = np.average(num_nodes2, axis=2)

    keyword_num_options = np.array([2, 3, 4, 5, 6])

    total_width, n = 0.8, 3
    width = total_width / n
    x = keyword_num_options - (total_width - width) / 2.0

    plt.xlabel('l: number of keywords')
    plt.ylabel('number of found apis')
    plt.bar(x, average_num_nodes2[0], width=width)
    plt.bar(x, average_num_nodes[0], width=width, bottom=average_num_nodes2[0], label='Minimal Steiner')
    plt.bar(x + width, average_num_nodes2[2], width=width, label='Greedy Steiner2')
    plt.bar(x + width, average_num_nodes[2], width=width, bottom=average_num_nodes2[2], label='Greedy Steiner')
    plt.bar(x + 2 * width, average_num_nodes2[1], width=width, label='Random Steiner2')
    plt.bar(x + 2 * width, average_num_nodes[1], width=width, bottom=average_num_nodes2[1], label='Random Steiner')

    plt.legend(loc='upper')
    plt.savefig('../outputs/nodes_found_by_methods.png')

# draw_success_rate_between_random_and_mashup_keywords()
# draw_success_rates_of_different_methods()
draw_success_rates_of_different_methods()