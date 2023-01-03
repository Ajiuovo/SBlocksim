import random
import math

class Shard(object):
    def NodeShard(node, K):
        # self.node = node
        N = len(node)
        shardNum = K
        DCnum = math.floor(N/(shardNum+1))                          # the number of DC nodes
        DCList = []
        for i in range(0, DCnum):
            DCList.append(node[i])
        nodeNum = math.ceil((N-DCnum)/shardNum)                     # the number of nodes in each shard
        nodeList = [node[i:i+nodeNum]for i in range(DCnum, len(node), nodeNum)]   # Sharding nodes which are not in DC
        return DCList, nodeList                           # return the id and power list of DC






