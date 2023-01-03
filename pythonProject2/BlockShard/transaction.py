"""
def create_transaction_size()：Transactions arriving at the current moment
n：Number of transactions arriving at the current moment
transaction：Size of the transaction at the current moment
def calculate_transaction(t_size, p_size, b, k)：Calculate the size of the outstanding transaction at the current moment
block_size：block size
block_header：block header size
"""
import random
random.seed(10)


class Transaction(object):

    @staticmethod
    def create_transaction_size():
        n = random.randint(100000, 200000)
        t_size = 0
        for i in range(n):
            transaction = random.randint(150, 250)
            t_size = t_size + transaction
        return t_size

    @staticmethod
    def calculate_transaction(t_size, p_size, b, k):
        block_size = b
        block_header = 80
        deal_transaction = (block_size*1024*1024 - block_header) * k
        p_size = t_size + p_size - deal_transaction
        return p_size


