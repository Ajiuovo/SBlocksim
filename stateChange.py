from BlockShard import node as nd
from BlockShard import shard as shard
from BlockShard import transaction as transaction
from BlockShard import trust as trust
from BlockShard import consensus as consensus
from BlockShard import reward as reward


class State(object):

    def __init__(self):
        self.n_actions = 8*16*8
        self.n_states = 40401
        self.t_size = transaction.Transaction.create_transaction_size()
        self.p_size = self.t_size

    def start_state(self):
        node_id_list = nd.Node.create_node()

        rate = nd.Node.transmission()

        power = nd.Node()
        node_list, power_list = power.node_power(node_id_list)

        history_list = nd.Node.start_h()

        p = 0

        # t_size = transaction.Transaction.create_transaction_size()

        p_size = 0
        start_state = []
        N = len(node_id_list)
        for i in range(0, N):
            for j in range(0, N):
                start_state.append(rate[i][j])
        start_state = start_state + power_list + history_list

        start_state.append(p)
        # start_state.append(self.t_size)
        # start_state.append(p_size)

        return start_state


    def StateChange(self, B, TI, K):
        node_id_list = nd.Node.create_node()

        rate = nd.Node.transmission()

        power = nd.Node()
        node_list, power_list = power.node_power(node_id_list)

        dc_list, shard_node_list = shard.Shard.node_shard(node_id_list, K)
        print(dc_list, shard_node_list)
        history_list, p = trust.Trust.probability(dc_list, shard_node_list, K)

        t_size = transaction.Transaction.create_transaction_size()

        p_size = self.p_size

        p_size = transaction.Transaction.calculate_transaction(t_size, p_size, B, K)
        self.p_size = p_size

        t_latency = consensus.Consensus.latency(dc_list, shard_node_list,  rate, B, TI, K)

        n = len(node_id_list)
        r = reward.Reward.calculate_reward(B, TI, K, n, p, t_latency)

        next_state = []
        for i in range(0, n):
            for j in range(0, n):
                next_state.append(rate[i][j])
        next_state = next_state + power_list + history_list
        next_state.append(p)
        # next_state.append(t_size)
        # next_state.append(p_size)
        return next_state, r

