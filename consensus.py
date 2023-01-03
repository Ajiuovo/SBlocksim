"""
calculating time of communications and consensus between nodes
DC consenses and group consensus processes are both composed of the classic PBFT four-part processes
t_in_pre_prepare_list：process of pre_prepare in shard
t_in_prepare_list：process of prepare in shard
t_in_commit_list：process of commit in shard
"""
import random


class Consensus:
    @staticmethod
    def latency(dc_list, nodelist, r_list, b, ti, k):
        n = len(dc_list) + len(nodelist)
        t_limit = 10.0  # set timeout
        m_batch = 3
        x = 2.0
        y = 1.0
        t_in_pre_prepare_list = []            # Declare and store the maximum value of t_in_pre_prepare in each shard
        t_in_prepare_list = []                # Declare and store the maximum value of t_in_prepare in each shard
        t_in_commit_list = []                 # Declare and store the maximum value of t_in_commit in each shard
        t_in_prop_list = []
        t_in_val_list = []
        t_request_list = []
        t_f_pre_prepare_list = []
        t_f_prepare_list = []
        t_f_commit_list = []
        t_f_reply_list = []

        for i in range(0, k):                         # Number of cycles = number of shards
            shard_list = nodelist[i]                    # DC_i
            node_num = len(shard_list)                        # the number of nodes in DC_i
            first_node = shard_list[0][0]                       #choose the first node as the primary node
            last_node = shard_list[node_num-1][0]
            block_node_id = random.randint(0, node_num-1)
            block_node = shard_list[block_node_id][0]            # choose the blocknode as the primary node randomly

            # print("************************************************* consensus process of preprepare in shard")
            t_in_pre_prepare = []                           # time of communication between primary node and others
            if block_node_id == 0:
                for j in range(1, node_num):                        # Number of cycles = number of nodes in DC_i - 1
                    replica_node_id = shard_list[j][0]
                    rij = r_list[first_node][replica_node_id]
                    t_in_pre_prepare.append((m_batch*b)/(rij*0.125))  # time of transmission between primary node and others

            elif block_node_id == (node_num-1):
                for j in range(0, node_num-1):
                    replica_node_id = shard_list[j][0]
                    rij = r_list[last_node][replica_node_id]
                    t_in_pre_prepare.append((m_batch*b)/(rij*0.125))  # time of transmission between primary node and others
            else:
                for j in range(0, block_node_id):                      # Number of cycles = number of nodes in DC_i - 1
                    replica_node_id = shard_list[j][0]
                    rij = r_list[block_node][replica_node_id]
                    t_in_pre_prepare.append((m_batch*b)/(rij*0.125))

                for j in range(block_node_id+1, node_num):
                    replica_node_id = shard_list[j][0]
                    rij = r_list[block_node][replica_node_id]
                    t_in_pre_prepare.append((m_batch*b)/(rij*0.125))   # time of transmission between primary node and others

            t_max = max(t_in_pre_prepare)
            t_min = min(t_max, t_limit)              # Maximum transfer time between nodes
            t_in_pre_prepare_list.append(t_min)        #time of consensus process of preprepare in shard

            # print("*************************************************** consensus process of prepare in shard")
            t_in_prepare = []
            for j in range(0, node_num):
                node_id = shard_list[j][0]
                if node_id == block_node:
                    continue
                else:
                    for m in range(0, node_num):
                        other_node_id = shard_list[m][0]
                        if other_node_id == node_id:
                            continue
                        else:
                            rij = r_list[node_id][other_node_id]
                            t_in_prepare.append((m_batch*b)/(rij*0.125))
            t_max = max(t_in_prepare)
            t_min = min(t_max, t_limit)
            t_in_prepare_list.append(t_min)   #time of consensus process of prepare in shard

            # print("****************************************************** consensus process of commit in shard")
            t_in_commit = []
            for j in range(0, node_num):
                node_id = shard_list[j][0]
                for m in range(0, node_num):
                    other_node_id = shard_list[m][0]
                    if other_node_id == node_id:
                        continue
                    else:
                        rij = r_list[node_id][other_node_id]
                        t_in_commit.append((m_batch*b)/(rij*0.125))
            t_max = max(t_in_commit)
            t_min = min(t_max, t_limit)
            t_in_commit_list.append(t_min)           #time of consensus process of commit in shard

            # print("******************************************** consensus process of reply in shard")
            c = len(dc_list)
            t_in_replica = []
            t_in_val = []
            t_primary = 0
            for j in range(0, node_num):
                if j == block_node_id:
                    power = shard_list[j][2]
                    t_primary = ((m_batch * x) + ((m_batch * (1 + c)) + 4*(node_num - 1)) * y) / (power*1000)
                else:
                    power = shard_list[j][2]
                    t_in_replica.append(((m_batch * x) + ((m_batch * c) + 4*(node_num - 1)) * y) / (power*1000))
            t_replica = max(t_in_replica)
            t_in_val.append(max(t_primary, t_replica))
            t_in_val_max = max(t_in_val)                        #time of consensus process in shard
            t_in_val_list.append(t_in_val_max)

            # print("-----------------------------------------------time of consensus process of request in DC")
            for j in range(0, node_num):
                shard_node_id = shard_list[j][0]
                dc_num = len(dc_list)
                for m in range(0, dc_num):
                    rij = r_list[shard_node_id][m]
                    t_request_list.append((m_batch*b)/(rij*0.125))
        t_request_max = max(t_request_list)
        t_request = (min(t_request_max, t_limit))

        # print("--------------------------------------------------- time of consensus process of preprepare in DC")
        dc_num = len(dc_list)
        dc_block_id = random.randint(0, dc_num-1)
        if dc_block_id == dc_list[0][0]:
            for i in range(1, dc_num):
                rij = r_list[0][i]
                t_f_pre_prepare_list.append((m_batch*b)/(rij*0.125))
        elif dc_block_id == dc_list[dc_num-1][0]:
            for i in range(0, dc_num-1):
                rij = r_list[dc_num-1][i]
                t_f_pre_prepare_list.append((m_batch*b)/(rij*0.125))
        else:
            for i in range(0, dc_block_id):
                rij = r_list[dc_block_id][i]
                t_f_pre_prepare_list.append((m_batch*b)/(rij*0.125))
            for i in range(dc_block_id, dc_num-1):
                rij = r_list[dc_block_id][i+1]
                t_f_pre_prepare_list.append((m_batch*b)/(rij*0.125))
        t_f_pre_prepare_max = max(t_f_pre_prepare_list)
        t_f_pre_prepare = min(t_f_pre_prepare_max, t_limit)

        # print("----------------------------------------------------- time of consensus process of prepare in DC")
        for i in range(0, dc_num):
            dc_node_id = dc_list[i][0]
            if dc_node_id == dc_block_id:
                continue
            else:
                for j in range(0, dc_num):
                    dc_other_id = dc_list[j][0]
                    if dc_node_id == dc_other_id:
                        continue
                    else:
                        rij = r_list[dc_node_id][j]
                        t_f_prepare_list.append((m_batch*b)/(rij*0.125))
        t_f_prepare_max = max(t_f_prepare_list)
        t_f_prepare = min(t_f_prepare_max, t_limit)

        # print("----------------------------------------------------- time of consensus process of commit in DC")
        for i in range(0, dc_num):
            dc_node_id = dc_list[i][0]
            for j in range(0, dc_num):
                if dc_node_id == dc_list[j][0]:
                    continue
                else:
                    rij = r_list[dc_node_id][j]
                    t_f_commit_list.append((m_batch*b)/(rij*0.125))
        t_f_commit_max = max(t_f_commit_list)
        t_f_commit = min(t_f_commit_max, t_limit)

        # print("------------------------------------------------------time of consensus process of reply in DC")
        for i in range(0, dc_num):
            dc_node_id = dc_list[i][0]
            for j in range(0, k):
                shard_list = nodelist[j]
                shard_node_num = len(shard_list)
                for m in range(0, shard_node_num):
                    rij = r_list[dc_node_id][shard_list[m][0]]
                    t_f_reply_list.append((k*m_batch*b)/(rij*0.125))
        t_f_reply_max = max(t_f_reply_list)
        t_f_reply = min(t_f_reply_max, t_limit)

        # print("------------------------------------------------------verification time in DC")
        dc_num = len(dc_list)
        t_replica_list = []
        t_primary = 0
        for i in range(0, dc_num):
            if i == dc_block_id:
                power = dc_list[i][2]
                t_primary = ((k*m_batch*x) + (k*m_batch + 4*(dc_num-1) + (n-dc_num) * m_batch) * y) / (power*1000)
            else:
                power = dc_list[i][2]
                t_replica_list.append(((k*m_batch*x) + (4*(dc_num - 1) + (n - dc_num) * m_batch) * y) / (power * 1000))
        t_replica = max(t_replica_list)
        t_f_val = (max(t_primary, t_replica))

        # print("****************************************************************************** whole time consumption")
        for i in range(0, k):
            t_in_prop_list.append((t_in_pre_prepare_list[i]+t_in_prepare_list[i]+t_in_commit_list[i]))
        t_in_prop = (1/m_batch)*max(t_in_prop_list)
        t_in_avl = (1/m_batch)*max(t_in_val_list)
        t_in_tra = t_in_prop + t_in_avl

        t_f_prop = (1/m_batch)*(t_request + t_f_pre_prepare + t_f_prepare + t_f_commit + t_f_reply)
        t_f_in_al = t_f_prop + (1/m_batch)*t_f_val

        t_con = t_in_tra + t_f_in_al

        t_latency = ti + t_con

        return t_latency





