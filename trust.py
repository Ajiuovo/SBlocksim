"""
ti_list：A set of standard entropy, if valid votes are equal to invalid votes, the standard entropy value is 1
        If the voting results are exactly the same (whether it is the number of valid votes or the number of valid votes), the standard entropy value is 0
        In other cases, the standard entropy value needs to be calculated: PM=(1-Pm), where Pm represents the consensus situation

"""
import math
import numpy as np


class Trust(object):
    @staticmethod
    def probability(dc_list, nodelist, k):
        ti_list = []
        h_list = []
        # calculate consensus in shard
        for i in range(0, k):
            mal_node = 0
            shard_list = nodelist[i]
            node_num = len(shard_list)
            for j in range(0, node_num):
                h = shard_list[j][2]
                h_list.append(h)
                if h == 0:
                    mal_node = mal_node + 1
                else:
                    continue
            if mal_node == node_num:
                ii = 0
                ti_list.append(ii)
            elif mal_node == 0:
                ii = 0
                ti_list.append(ii)
            elif mal_node == node_num/2:
                ii = 1
                ti_list.append(ii)
            else:
                pm = mal_node/node_num
                ii = (-pm) * math.log2(pm) - (1-pm)*math.log2(1-pm)
                ti_list.append(ii)
        # calculate consensus in DC
        mal_node = 0
        pu = 0
        dc_num = len(dc_list)
        for i in range(0, dc_num):
            h = dc_list[i][2]
            h_list.append(h)
            if h == 0:
                mal_node = mal_node + 1
            else:
                continue
        if mal_node == dc_num:
            idc = 0
        elif mal_node == 0:
            idc = 0
        elif mal_node == dc_num / 2:
            idc = 1
        else:
            pm = mal_node/dc_num
            idc = (-pm) * math.log2(pm) - (1-pm)*math.log2(1-pm)
        # whole consensus reputation U
        i = 0
        for i in range(0, k):
            i = i + ti_list[i]
        u = (1/(k+1))*(i+idc)
        p_list = np.linspace(0.00001, 1.0, num=100000)
        for i in range(0, 100000):
            pu = p_list[i]
            v = (-pu) * math.log2(pu) - (1 - pu) * math.log2(1 - pu)
            n = u - v
            if n < 0.0000001:
                break
            else:
                continue
        p = min(pu, 1-pu)

        return h_list, p








