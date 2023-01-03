"""
ActionSpace includes three variables:
b: block size
ti: time of append new block to chain
k: number of shard
"""


class ActionSpace:
    @staticmethod
    def create_action_space():
        b_list = [1, 2, 3, 4, 5, 6, 7, 8]
        ti_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        k_list = [1, 2, 3, 4, 5, 6, 7, 8]
        actions = []
        for i in range(len(b_list)):
            for j in range(len(ti_list)):
                for n in range(len(k_list)):
                    b = b_list[i]
                    ti = ti_list[j]
                    k = k_list[n]
                    actions.append([b, ti, k])
        return actions

