"""
n：number of nodes
shard_n：number of shards
dc_num：number of nodes in DC
dc_list：collection of DC nodes
power_list：collection of node computing power
shard_l：number of bits of shards number
shard_node_list：collection of shards
ex_nodelist：store the extra nodes for each shard
shard_node_num：number of nodes in shard
shard_nodelist：collection of nodes in shard divided in the first time,
"""
import math


class Shard(object):
    @staticmethod
    def node_shard(node_list, k):
        n = len(node_list)
        power_list = []
        dc_list = []
        shard_n = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011',
                   '1100', '1101', '1110', '1111']
        # select DC nodes by power
        dc_num = math.floor(n / (k + 1))
        for i in range(0, n):
            power_list.append(node_list[i][2])
            print(power_list)
        for i in range(0, dc_num):
            max_power = max(power_list)
            dc_node_id = power_list.index(max_power)
            dc_list.append(node_list[dc_node_id])
            power_list.pop(dc_node_id)
            node_list.pop(dc_node_id)

        if k == 1:
            shard_l = 1
        else:
            shard_l = math.ceil(math.log2(k))

        shard_node_list = []
        ex_nodelist = []

        # Number of nodes for sharding
        node_num = len(node_list)
        # sharding
        for i in range(0, k):
            # Number of nodes in shard
            shard_node_num = math.floor(node_num / k)
            shard_nodelist = []
            shard_node = []
            for j in range(0, node_num):
                # Get the binary index of the node
                index = node_list[j][1]
                # If the last l bits of the node index are the same as the last l bits of the shard number, put it into the shard
                if index[-shard_l:] == shard_n[i][-shard_l:]:
                    shard_nodelist.append(node_list[j])
            # If the actual number of nodes in the shard > the calculated number of nodes in the shard, put the extra nodes into ex_shard_node
            if len(shard_nodelist) > shard_node_num:
                # Put the specified number of nodes into the shard_node
                for m in range(0, shard_node_num):
                    shard_node.append(shard_nodelist[m])
                # Put shard into the shard_node_list
                shard_node_list.append(shard_node)
                # Put the extra nodes in the shard into ex_nodelist
                for n in range(shard_node_num, len(shard_nodelist)):
                    ex_nodelist.append(shard_nodelist[n])
            else:
                shard_node_list.append(shard_nodelist)

        # if the number of shards is odd or even
        if (2 ** shard_l) - k != 0:
            for i in range(k, 2**shard_l):
                for j in range(0, node_num):
                    index = node_list[j][1]
                    if index[-shard_l:] == shard_n[i][-shard_l:]:
                        ex_nodelist.append(node_list[j])

        # Put the extra nodes in the ex_nodelist into shard
        for i in range(0, k):
            n = node_num % k
            shard_node_num = math.floor(node_num / k)
            if n != 0:
                if i < n:
                    if len(shard_node_list[i]) < shard_node_num + 1:
                        for j in range(0, shard_node_num+1-len(shard_node_list[i])):
                            shard_node_list[i].append(ex_nodelist[0])
                            ex_nodelist.pop(0)
                else:
                    if len(shard_node_list[i]) < shard_node_num:
                        for j in range(0, shard_node_num-len(shard_node_list[i])):
                            shard_node_list[i].append(ex_nodelist[0])
                            ex_nodelist.pop(0)
            else:
                if len(shard_node_list[i]) < shard_node_num:
                    for j in range(0, shard_node_num-len(shard_node_list[i])):
                        shard_node_list[i].append(ex_nodelist[0])
                        ex_nodelist.pop(0)
        return dc_list, shard_node_list



























