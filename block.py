import time
import hashlib
import json
import random


blockchain = []

class Block:

    def __init__(self, transactions, previous_hash, nonce):
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()


    def calculate_hash(self):
        block_data = {
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }
        block_data_str = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_data_str).hexdigest()


    def mine_block(self, difficulty): # PoW
        target = "0" * int(difficulty)
        while True:
            self.nonce = random.randint(1, 1000000)
            computed_hash = self.calculate_hash()
            if computed_hash[:difficulty] == target:
                blockchain.append(self)
                print(f"Block #{len(blockchain)} mined with nonce {self.nonce}")
                break


def get_transaction_hash(transaction):
    transaction_data_str = json.dumps(transaction, sort_keys=True) 
    transaction_hash = hashlib.sha256(transaction_data_str.encode()).hexdigest()
    return transaction_hash


genesis_block = Block([], "0", 0)
blockchain.append(genesis_block)


difficulty = 4  
num_blocks_to_mine = 3
for _ in range(num_blocks_to_mine):
    new_block = Block([], blockchain[-1].hash, 0)
    new_block.mine_block(difficulty)


for index, block in enumerate(blockchain):
    print(f"Block #{index + 1}: ")
    print("\tTimestamp:", time.ctime(block.timestamp))
    print("\tPrevious Hash:", block.previous_hash)
    print("\tNonce:", block.nonce)
    print("\tHash:", block.hash)
    print("\tTransactions:")
    for transaction in block.transactions:
        print(json.dumps(transaction, indent=4))
    print("\n")
