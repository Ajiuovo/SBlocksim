import math


class Reward(object):

    @staticmethod
    def calculate_reward(b, ti, k, n, p, t_latency):
        u = 6
        b = 200
        bh = 80
        reward = []
        if k < (n * (1 - 3 * p) - 1) / (3 * n * p + 1):
            if k < ((2 * n) / (3 * (n * p + 1))) - 1:
                if t_latency <= (u*ti):
                    reward.append(((k * math.ceil((b*1024*1024-bh)/b))/ti)/10000)
                    return reward
                else:
                    # print("Constraint S1 is not satisfied")
                    reward.append(0)
                    return reward
            else:
                # print("Constraint S2 is not satisfied")
                reward.append(0)
                return reward
        else:
            # print("Time constraints are not met")
            reward.append(0)
            return reward

