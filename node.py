"""
Initializes the properties of the node：
self.node_num：Number of nodes
self.mal_node_p：The probability of malicious nodes
id_list：Generate a number of nodes with different random numbers from 1000-2000, which are later used as the binary ID of the node
node_id_list：node_list:[index,node_id,node_power,mal_node]
power：Cmputing power of the node, ranging from 10GHz to 30GHz
node_power：A collection of node computing power
rate：Transmission rate between nodes, ranging from 10 to 100Mbps
start_h_list：Consensus history of nodes，initialized as 0
"""
import random
import math
import numpy as np
# np.random.seed(1)
node_num = 20
mal_node_p = 0

class Node(object):


    @staticmethod
    def create_node():
        node_list = []
        id_list = random.sample(range(1000, 2000), node_num)
        for i in range(0, node_num):
            node_list.append([i, bin(id_list[i]), 0, 0])
        p_node = math.floor(mal_node_p * node_num)
        p_node_id = random.sample(range(0, node_num - 1), p_node)
        for i in range(0, p_node):
            node_list[p_node_id[i]][3] = 1
        return node_list

    def node_power(self, node_list):
        power_list = []
        for i in range(0, node_num):
            power = random.randint(10, 30)
            power_list.append(power)
            node_list[i][2] = power
        return node_list, power_list

    @staticmethod
    def transmission():
        rate = np.random.randint(10, 101, (node_num, node_num))
        return rate

    @staticmethod
    def start_h():
        start_h_list = []
        for i in range(0, node_num):
            start_h_list.append(0)
        return start_h_list


